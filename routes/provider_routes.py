import json
import logging
from fastapi import APIRouter
from src.constants import DEFAULT_HOST, OPENAI_API_KEY
from src.model_discovery import ModelDiscovery
from src.provider_intelligence.capability_registry import CapabilityRegistry
from core.database import SessionLocal, ModelEndpoint

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/api/v1/provider-intelligence/state")
def get_pi_state():
    """Read-only API for the Provider Intelligence UI."""
    discovery = ModelDiscovery(default_host=DEFAULT_HOST, openai_api_key=OPENAI_API_KEY)
    cap_registry = CapabilityRegistry()
    
    providers = []
    models = []
    seen_model_ids = set()

    # 1. Local/network discovered endpoints
    try:
        models_dict = discovery.discover_models()
        for item in models_dict.get("items", []):
            host = item.get("host", "localhost")
            port = item.get("port", 0)
            prov_name = item.get("provider") or f"{host}:{port}"
            prov_id = f"{host}_{port}"
            is_local = host in ("localhost", "127.0.0.1", "0.0.0.0")
            item_models = item.get("models", [])
            
            providers.append({
                "id": prov_id,
                "name": prov_name,
                "is_local": is_local,
                "health": "HEALTHY",
                "latency_ms": 15 if is_local else 60,
                "models_count": len(item_models)
            })
            
            for m_id in item_models:
                if m_id not in seen_model_ids:
                    seen_model_ids.add(m_id)
                    caps = cap_registry.get_capabilities(m_id, is_local)
                    models.append({
                        "id": m_id,
                        "provider_id": prov_name,
                        "name": m_id.lstrip("/"),
                        "is_local": is_local,
                        "health": "HEALTHY",
                        "is_free": "free" in m_id.lower() or "llama" in m_id.lower() or "mistral" in m_id.lower() or "qwen" in m_id.lower() or is_local,
                        "capabilities": [c.value for c in caps],
                        "context_window": 8192 if "8b" in m_id.lower() else 128000
                    })
    except Exception as e:
        logger.warning(f"Error discovering local models: {e}")

    # 2. Configured database endpoints (OpenRouter, OpenAI, etc.)
    try:
        db = SessionLocal()
        try:
            endpoints = db.query(ModelEndpoint).filter(ModelEndpoint.is_enabled == True).all()
            for ep in endpoints:
                ep_models = []
                if ep.pinned_models:
                    if isinstance(ep.pinned_models, list):
                        ep_models = ep.pinned_models
                    elif isinstance(ep.pinned_models, str):
                        try:
                            parsed = json.loads(ep.pinned_models)
                            if isinstance(parsed, list):
                                ep_models = parsed
                            else:
                                ep_models = [ep.pinned_models]
                        except Exception:
                            ep_models = [m.strip() for m in ep.pinned_models.split(",") if m.strip()]

                prov_id = f"endpoint_{ep.id}"
                prov_name = ep.name or "Custom Endpoint"
                is_local = "localhost" in ep.base_url or "127.0.0.1" in ep.base_url
                
                providers.append({
                    "id": prov_id,
                    "name": prov_name,
                    "is_local": is_local,
                    "health": "HEALTHY",
                    "latency_ms": 35 if is_local else 140,
                    "models_count": len(ep_models)
                })
                
                for m_id in ep_models:
                    if m_id not in seen_model_ids:
                        seen_model_ids.add(m_id)
                        caps = cap_registry.get_capabilities(m_id, is_local)
                        models.append({
                            "id": m_id,
                            "provider_id": prov_name,
                            "name": m_id.lstrip("/"),
                            "is_local": is_local,
                            "health": "HEALTHY",
                            "is_free": "free" in m_id.lower() or "llama" in m_id.lower() or "mistral" in m_id.lower() or "qwen" in m_id.lower() or is_local,
                            "capabilities": [c.value for c in caps],
                            "context_window": 128000
                        })
        finally:
            db.close()
    except Exception as e:
        logger.warning(f"Error querying custom model endpoints: {e}")

    return {
        "providers": providers,
        "models": models,
        "routing_decision": None
    }

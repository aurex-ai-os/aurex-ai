import re

with open("routes/chat_routes.py", "r") as f:
    content = f.read()

# Replace the _foreground_candidates assignment inside the stream route
old_candidates_code = """            _foreground_candidates = build_foreground_model_candidates(
                sess.endpoint_url,
                sess.model,
                sess.headers,
                owner=_user,
                policy=_foreground_policy,
            )"""

new_candidates_code = """            # PHASE 4 MIGRATION: Intercept with ProviderIntelligence
            _legacy_candidates = build_foreground_model_candidates(
                sess.endpoint_url,
                sess.model,
                sess.headers,
                owner=_user,
                policy=_foreground_policy,
            )
            
            try:
                from src.provider_intelligence.provider_registry import ProviderRegistry
                from src.provider_intelligence.model_registry import ModelRegistry
                from src.provider_intelligence.health_manager import HealthManager
                from src.provider_intelligence.quota_manager import QuotaManager
                from src.provider_intelligence.candidate_selector import CandidateSelector
                from src.provider_intelligence.routing_engine import RoutingEngine
                from src.provider_intelligence.models import TaskRequirements, Capability, PrivacyLevel
                from src.provider_intelligence.adapters.legacy_adapter import sync_legacy_to_registry
                
                p_reg = ProviderRegistry()
                m_reg = ModelRegistry()
                
                sync_legacy_to_registry(p_reg, m_reg, {}, sess.endpoint_url, sess.model, _legacy_candidates[1:] if len(_legacy_candidates)>1 else [])
                
                selector = CandidateSelector(p_reg, m_reg, HealthManager(), QuotaManager())
                engine = RoutingEngine(selector)
                
                req = TaskRequirements(
                    hard_capabilities={Capability.TEXT_GENERATION},
                    privacy_requirement=PrivacyLevel.LOCAL_ONLY if "localhost" in sess.endpoint_url else PrivacyLevel.ALLOW_REMOTE
                )
                
                # Check if task requires tools
                if len(body.get("tools", [])) > 0:
                    req.hard_capabilities.add(Capability.TOOL_CALLING)
                    
                decision = engine.select_route(req)
                
                if decision.route_type != "FAILED":
                    # Filter legacy candidates to only those that match valid fallback decisions
                    valid_cands = [decision.selected_model_id] + [f.split("::")[1] for f in decision.fallback_candidates]
                    _foreground_candidates = [c for c in _legacy_candidates if c[1] in valid_cands]
                else:
                    _foreground_candidates = _legacy_candidates
            except Exception as e:
                logger.warning(f"[ProviderIntelligence] Stream Routing failed, falling back to legacy: {e}")
                _foreground_candidates = _legacy_candidates"""

content = content.replace(old_candidates_code, new_candidates_code)

with open("routes/chat_routes.py", "w") as f:
    f.write(content)

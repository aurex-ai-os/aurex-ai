import re

with open("routes/chat_routes.py", "r") as f:
    content = f.read()

# Replace the foreground_candidates assignment inside the chat route
old_candidates_code = """        foreground_candidates = build_foreground_model_candidates(
            sess.endpoint_url,
            sess.model,
            sess.headers,
            owner=owner,
            policy=foreground_policy,
        )"""

new_candidates_code = """        # PHASE 4 MIGRATION: Intercept with ProviderIntelligence
        legacy_candidates = build_foreground_model_candidates(
            sess.endpoint_url,
            sess.model,
            sess.headers,
            owner=owner,
            policy=foreground_policy,
        )
        
        try:
            from src.provider_intelligence.provider_registry import ProviderRegistry
            from src.provider_intelligence.model_registry import ModelRegistry
            from src.provider_intelligence.health_manager import HealthManager
            from src.provider_intelligence.quota_manager import QuotaManager
            from src.provider_intelligence.candidate_selector import CandidateSelector
            from src.provider_intelligence.routing_engine import RoutingEngine
            from src.provider_intelligence.models import TaskRequirements, Capability
            from src.provider_intelligence.adapters.legacy_adapter import sync_legacy_to_registry
            
            p_reg = ProviderRegistry()
            m_reg = ModelRegistry()
            
            sync_legacy_to_registry(p_reg, m_reg, {}, sess.endpoint_url, sess.model, legacy_candidates[1:] if len(legacy_candidates)>1 else [])
            
            selector = CandidateSelector(p_reg, m_reg, HealthManager(), QuotaManager())
            engine = RoutingEngine(selector)
            
            req = TaskRequirements(hard_capabilities={Capability.TEXT_GENERATION})
            decision = engine.select_route(req)
            
            if decision.route_type != "FAILED":
                # Reconstruct candidate list putting selected model first
                # (For now, we map back to the legacy tuple structure)
                selected_cand = None
                for c in legacy_candidates:
                    if c[1] == decision.selected_model_id:
                        selected_cand = c
                        break
                
                if selected_cand:
                    foreground_candidates = [selected_cand] + [c for c in legacy_candidates if c != selected_cand]
                else:
                    foreground_candidates = legacy_candidates
            else:
                foreground_candidates = legacy_candidates
        except Exception as e:
            logger.warning(f"[ProviderIntelligence] Routing failed, falling back to legacy: {e}")
            foreground_candidates = legacy_candidates"""

content = content.replace(old_candidates_code, new_candidates_code)

with open("routes/chat_routes.py", "w") as f:
    f.write(content)

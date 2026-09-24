from typing import Dict, List, Tuple
from src.provider_intelligence.provider_registry import ProviderRegistry
from src.provider_intelligence.model_registry import ModelRegistry
from src.provider_intelligence.models import ProviderDefinition, ModelDefinition, ProviderType, Capability

def sync_legacy_to_registry(
    provider_registry: ProviderRegistry, 
    model_registry: ModelRegistry,
    legacy_models: Dict[str, List[Dict]], 
    primary_url: str, 
    primary_model: str, 
    fallback_entries: List[tuple]
):
    """
    Synchronizes Aurex's legacy discovery data and the user's current session
    into the canonical ProviderIntelligence registries.
    """
    # 1. Register the primary session endpoint as a provider if not present
    if "primary" not in [p.id for p in provider_registry.get_all_providers()]:
        is_local = "localhost" in primary_url or "127.0.0.1" in primary_url
        provider_registry.register_provider(ProviderDefinition(
            id="primary",
            display_name="Primary Provider",
            provider_type=ProviderType.LOCAL if is_local else ProviderType.OPENAI_COMPAT,
            endpoint_url=primary_url,
            is_local=is_local,
            priority=100  # Highest priority for explicit primary
        ))
        
        # Register the primary model
        model_registry.register_model(ModelDefinition(
            id=primary_model,
            provider_id="primary",
            name=primary_model,
            display_name=primary_model,
            is_local=is_local,
            # We assume the primary model can handle text at least
            capabilities={Capability.TEXT_GENERATION, Capability.TOOL_CALLING}
        ))
        
    # 2. Register legacy fallbacks
    for idx, fallback in enumerate(fallback_entries):
        f_url, f_model, _ = fallback
        p_id = f"fallback_{idx}"
        is_local = "localhost" in f_url or "127.0.0.1" in f_url
        
        provider_registry.register_provider(ProviderDefinition(
            id=p_id,
            display_name=f"Fallback {idx}",
            provider_type=ProviderType.LOCAL if is_local else ProviderType.OPENAI_COMPAT,
            endpoint_url=f_url,
            is_local=is_local,
            priority=80 - idx
        ))
        
        model_registry.register_model(ModelDefinition(
            id=f_model,
            provider_id=p_id,
            name=f_model,
            display_name=f_model,
            is_local=is_local,
            capabilities={Capability.TEXT_GENERATION, Capability.TOOL_CALLING}
        ))

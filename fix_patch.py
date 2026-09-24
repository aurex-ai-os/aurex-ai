import re

with open("routes/chat_routes.py", "r") as f:
    content = f.read()

old_code = """                if selected_cand:
                    foreground_candidates = [selected_cand] + [c for c in legacy_candidates if c != selected_cand]
                else:
                    foreground_candidates = legacy_candidates"""

new_code = """                if selected_cand:
                    # Filter to only valid fallbacks approved by Provider Intelligence
                    valid_cands = [decision.selected_model_id] + [f.split("::")[1] for f in decision.fallback_candidates]
                    foreground_candidates = [c for c in legacy_candidates if c[1] in valid_cands]
                else:
                    foreground_candidates = legacy_candidates"""

content = content.replace(old_code, new_code)

with open("routes/chat_routes.py", "w") as f:
    f.write(content)

import re
with open("static/aurex-theme.css", "r") as f:
    text = f.read()

# Make the border stand out more in dark mode by using a semi-transparent white/gray
new_capsule = r"""
.chat-input-bar {
  position: absolute !important;
  bottom: 30px !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  width: 90% !important;
  max-width: 760px !important;
  border-radius: 28px !important;
  
  /* Make shadow much wider and add a subtle ambient glow using the accent color */
  box-shadow: 0 30px 60px rgba(0,0,0,0.8), 0 0 120px var(--aurex-accent-soft) !important;
  
  background: color-mix(in srgb, var(--aurex-surface-raised) 75%, transparent) !important;
  backdrop-filter: blur(24px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
  
  /* Distinct glass rim-lighting */
  border: 1px solid color-mix(in srgb, var(--aurex-text) 15%, transparent) !important;
  border-top: 1px solid color-mix(in srgb, var(--aurex-text) 30%, transparent) !important;
  
  z-index: 100 !important;
  padding: 12px 16px !important;
  transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
}

.chat-input-bar:focus-within {
  /* Intensify the glow when focused */
  box-shadow: 0 35px 70px rgba(0,0,0,0.9), 0 0 150px color-mix(in srgb, var(--aurex-accent) 25%, transparent), 0 0 0 1px var(--aurex-accent-soft) !important;
  transform: translateX(-50%) translateY(-6px) !important;
  background: var(--aurex-surface-raised) !important;
  border-top: 1px solid color-mix(in srgb, var(--aurex-accent) 50%, transparent) !important;
}
"""

# Replace everything from .chat-input-bar { to the end of .chat-input-bar:focus-within { ... }
text = re.sub(r'\.chat-input-bar \{.*?\.chat-input-bar:focus-within \{.*?\}', new_capsule.strip(), text, flags=re.DOTALL)

with open("static/aurex-theme.css", "w") as f:
    f.write(text)

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
  
  /* Radiant Neon Glow using the dynamic theme accent color */
  box-shadow: 
    0 20px 40px rgba(0,0,0,0.8),
    0 0 15px color-mix(in srgb, var(--aurex-accent) 60%, transparent), 
    0 0 45px color-mix(in srgb, var(--aurex-accent) 30%, transparent),
    inset 0 0 10px color-mix(in srgb, var(--aurex-accent) 15%, transparent) !important;
  
  background: color-mix(in srgb, var(--aurex-surface-raised) 85%, transparent) !important;
  backdrop-filter: blur(24px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
  
  /* Glowing Border */
  border: 1px solid color-mix(in srgb, var(--aurex-accent) 40%, transparent) !important;
  border-top: 1px solid color-mix(in srgb, var(--aurex-accent) 80%, transparent) !important;
  
  z-index: 100 !important;
  padding: 12px 16px !important;
  transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
}

.chat-input-bar:focus-within {
  /* Intensify the Neon Glow when focused */
  box-shadow: 
    0 25px 50px rgba(0,0,0,0.9),
    0 0 25px color-mix(in srgb, var(--aurex-accent) 80%, transparent), 
    0 0 70px color-mix(in srgb, var(--aurex-accent) 50%, transparent),
    0 0 100px color-mix(in srgb, var(--aurex-accent) 30%, transparent),
    inset 0 0 15px color-mix(in srgb, var(--aurex-accent) 30%, transparent) !important;
    
  transform: translateX(-50%) translateY(-6px) !important;
  background: color-mix(in srgb, var(--aurex-surface-raised) 95%, transparent) !important;
  border: 1px solid color-mix(in srgb, var(--aurex-accent) 80%, transparent) !important;
  border-top: 1px solid var(--aurex-accent) !important;
}
"""

text = re.sub(r'\.chat-input-bar \{.*?\.chat-input-bar:focus-within \{.*?\}', new_capsule.strip(), text, flags=re.DOTALL)

with open("static/aurex-theme.css", "w") as f:
    f.write(text)

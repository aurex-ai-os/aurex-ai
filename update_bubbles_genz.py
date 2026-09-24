import re
with open("static/aurex-theme.css", "r") as f:
    text = f.read()

new_bubbles = r"""
/* 18. Human vs AI Message Card Redesign */
.msg-user {
  /* High-Aesthetic / Arc Browser style vibrant pill */
  background: linear-gradient(135deg, var(--aurex-accent), color-mix(in srgb, var(--aurex-accent) 40%, #ff007f)) !important;
  border: none !important;
  border-radius: 32px !important;
  border-bottom-right-radius: 8px !important;
  padding: 16px 24px !important;
  color: #ffffff !important; 
  font-weight: 500 !important;
  letter-spacing: 0.01em !important;
  line-height: 1.5 !important;
  box-shadow: 0 12px 30px color-mix(in srgb, var(--aurex-accent) 35%, transparent) !important;
}

.msg-ai {
  /* VisionOS / Bento style frosted card */
  background: color-mix(in srgb, var(--aurex-text) 3%, transparent) !important;
  backdrop-filter: blur(40px) saturate(200%) !important;
  -webkit-backdrop-filter: blur(40px) saturate(200%) !important;
  border: 1px solid color-mix(in srgb, var(--aurex-text) 6%, transparent) !important;
  border-top: 1px solid color-mix(in srgb, var(--aurex-text) 12%, transparent) !important;
  border-radius: 32px !important;
  border-top-left-radius: 8px !important;
  padding: 20px 28px !important;
  color: var(--aurex-text) !important;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2) !important;
  margin: 16px 0 !important;
  max-width: 95% !important;
  line-height: 1.6 !important;
}

/* Ensure code blocks inside the new AI bubble fit the aesthetic */
.msg-ai pre {
  border-radius: 16px !important;
  margin-top: 16px !important;
  background: color-mix(in srgb, var(--aurex-bg) 60%, transparent) !important;
  border: 1px solid color-mix(in srgb, var(--aurex-text) 5%, transparent) !important;
}
"""

text = re.sub(r'/\* 18\. Human vs AI Message Card Redesign \*/.*?\.msg-ai pre \{.*?\}', new_bubbles.strip(), text, flags=re.DOTALL)

with open("static/aurex-theme.css", "w") as f:
    f.write(text)

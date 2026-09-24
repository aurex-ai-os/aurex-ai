import re
with open("static/aurex-theme.css", "r") as f:
    text = f.read()

new_bubbles = r"""
/* 18. Human vs AI Message Card Redesign */
.msg-user {
  /* Vibrant user bubble using the theme accent */
  background: linear-gradient(135deg, color-mix(in srgb, var(--aurex-accent) 90%, black), color-mix(in srgb, var(--aurex-accent) 70%, white)) !important;
  border: 1px solid color-mix(in srgb, var(--aurex-accent) 50%, white) !important;
  border-radius: 24px !important;
  border-bottom-right-radius: 6px !important;
  padding: 14px 20px !important;
  color: #ffffff !important; /* Force high-contrast text on the colored bubble */
  text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
  box-shadow: 0 8px 24px color-mix(in srgb, var(--aurex-accent) 25%, transparent) !important;
}

.msg-ai {
  /* Dedicated Glassmorphic AI Bubble */
  background: color-mix(in srgb, var(--aurex-surface-raised) 60%, transparent) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1px solid color-mix(in srgb, var(--aurex-border) 60%, white) !important;
  border-radius: 24px !important;
  border-top-left-radius: 6px !important;
  padding: 16px 24px !important;
  color: var(--aurex-text) !important;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
  margin: 16px 0 !important;
  width: auto !important;
  max-width: 95% !important;
}

/* Ensure code blocks inside the new AI bubble don't break the rounded corners */
.msg-ai pre {
  border-radius: 12px !important;
  margin-top: 12px !important;
}
"""

text = re.sub(r'/\* 18\. Human vs AI Message Card Redesign \*/.*?\.msg-ai \{.*?\}', new_bubbles.strip(), text, flags=re.DOTALL)

with open("static/aurex-theme.css", "w") as f:
    f.write(text)

import re
with open("static/aurex-theme.css", "r") as f:
    text = f.read()

new_colors = r"""
/* 20. Fix Contrast for Text and Tools inside the Vibrant User Bubble */
.msg-user {
  color: color-mix(in srgb, var(--aurex-accent) 8%, white) !important;
}

.msg-user .role {
  color: color-mix(in srgb, var(--aurex-accent) 12%, white) !important;
  opacity: 1 !important;
  font-weight: 600 !important;
}

.msg-user .body, 
.msg-user .body p, 
.msg-user .body span, 
.msg-user .body div {
  color: color-mix(in srgb, var(--aurex-accent) 5%, white) !important;
}

.msg-user .msg-footer,
.msg-user .msg-footer span,
.msg-user .msg-footer div,
.msg-user .timestamp {
  color: color-mix(in srgb, var(--aurex-accent) 25%, rgba(255, 255, 255, 0.75)) !important;
}

/* Edit, Delete, Copy buttons inside user bubble */
.msg-user button, 
.msg-user .msg-action-btn,
.msg-user .copy-btn {
  color: color-mix(in srgb, var(--aurex-accent) 20%, rgba(255, 255, 255, 0.85)) !important;
  background: transparent !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}

.msg-user button:hover, 
.msg-user .msg-action-btn:hover,
.msg-user .copy-btn:hover {
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.2) !important;
}

/* Links inside user bubble */
.msg-user a {
  color: color-mix(in srgb, var(--aurex-accent) 15%, white) !important;
  text-decoration: underline !important;
  text-decoration-color: rgba(255,255,255,0.6) !important;
}
"""

text = re.sub(r'/\* 20\. Fix Contrast for Text and Tools inside the Vibrant User Bubble \*/.*?\.msg-user a \{.*?\}', new_colors.strip(), text, flags=re.DOTALL)

with open("static/aurex-theme.css", "w") as f:
    f.write(text)

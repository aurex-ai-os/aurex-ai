import re

with open('static/aurex-theme.css', 'r') as f:
    css = f.read()

# Replace the right: 24px with right: calc(24px + var(--right-dock-w, 0px))
old_block = """#minimized-dock {
  top: 70px !important;
  bottom: auto !important;
  right: 24px !important;
  left: auto !important;
  transform: none !important;
  flex-direction: column !important;
  align-items: flex-end !important;
}

@media (max-width: 768px) {
  #minimized-dock {
    top: 60px !important;
    right: 12px !important;
  }
}"""

new_block = """#minimized-dock {
  top: 70px !important;
  bottom: auto !important;
  right: calc(24px + var(--right-dock-w, 0px)) !important;
  left: auto !important;
  transform: none !important;
  flex-direction: column !important;
  align-items: flex-end !important;
  transition: right 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}

@media (max-width: 768px) {
  #minimized-dock {
    top: 60px !important;
    right: calc(12px + var(--right-dock-w, 0px)) !important;
  }
}"""

if old_block in css:
    css = css.replace(old_block, new_block)
    with open('static/aurex-theme.css', 'w') as f:
        f.write(css)
    print("Patched dock position for split panels")
else:
    print("Could not find old block")

import re

with open("static/aurex-theme.css", "r") as f:
    css = f.read()

# Replace the pi-modal-content dimensions
old_w = "width: min(1100px, 95vw) !important;"
new_w = "width: min(1040px, 94vw) !important;"

old_h = "height: min(750px, 90vh) !important;"
new_h = "height: 80vh !important;\n  max-height: 800px !important;"

css = css.replace(old_w, new_w)
css = css.replace(old_h, new_h)

# Add media query for mobile to fix resolution on small screens
mobile_css = """
@media (max-width: 768px) {
  .pi-modal-content {
    width: 100% !important;
    height: 90dvh !important;
    max-height: none !important;
    border-radius: 14px 14px 0 0 !important;
    align-self: flex-end;
  }
  .pi-layout {
    flex-direction: column;
  }
  .pi-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--aurex-border);
    flex-direction: row;
    overflow-x: auto;
    padding: 12px;
  }
  .pi-nav-btn {
    white-space: nowrap;
  }
  .pi-detail-panel {
    width: 100%;
  }
}
"""

if "@media (max-width: 768px) {\n  .pi-modal-content {" not in css:
    css += mobile_css

with open("static/aurex-theme.css", "w") as f:
    f.write(css)

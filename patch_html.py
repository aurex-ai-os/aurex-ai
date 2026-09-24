import re
with open("static/index.html", "r") as f:
    text = f.read()

new_html = r"""
              <div id="set-searchUrlRow" class="settings-row">
                <label class="settings-label">URL</label>
                <div style="flex:1; display:flex; gap: 8px;">
                  <input id="set-searchUrl" type="text" placeholder="http://localhost:8080 (optional)" class="settings-select" style="flex:1;">
                  <button id="set-searchAutohostBtn" class="settings-action-btn" title="1-Click Self-Host with Docker">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:4px;"><path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z"/></svg>
                    Self-Host
                  </button>
                </div>
              </div>
"""

text = re.sub(r'              <div id="set-searchUrlRow" class="settings-row">\n                <label class="settings-label">URL</label>\n                <input id="set-searchUrl" type="text" placeholder="http://localhost:8080 \(optional\)" class="settings-select">\n              </div>', new_html.strip('\n'), text)

with open("static/index.html", "w") as f:
    f.write(text)

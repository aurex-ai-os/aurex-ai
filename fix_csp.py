import re

# 1. Clean up index.html
with open("static/index.html", "r") as f:
    html = f.read()

html = html.replace('onclick="runAutoHost()"', '')
html = re.sub(r'<script>\s*async function runAutoHost\(\).*?</script>\n', '', html, flags=re.DOTALL)

with open("static/index.html", "w") as f:
    f.write(html)

# 2. Add the listener to settings.js
with open("static/js/settings.js", "r") as f:
    js = f.read()

event_listener = """
// --- 1-Click Autohost ---
document.addEventListener('DOMContentLoaded', () => {
  const autohostBtn = document.getElementById('set-searchAutohostBtn');
  if (autohostBtn) {
    autohostBtn.addEventListener('click', async () => {
      const urlInput = document.getElementById('set-searchUrl');
      autohostBtn.innerHTML = '<span class="spinner" style="display:inline-block;margin-right:4px;">&#8987;</span> Starting...';
      autohostBtn.disabled = true;
      try {
        const res = await fetch('/api/search/autohost', { method: 'POST' });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Failed');
        urlInput.value = data.url;
        urlInput.dispatchEvent(new Event('change'));
        autohostBtn.innerHTML = '&#10003; Running';
        alert('SearXNG successfully launched via Docker! URL has been auto-filled.');
      } catch (err) {
        alert("Autohost failed: " + err.message + "\\n\\nPlease ensure Docker Desktop is installed and running on your machine.");
        autohostBtn.innerHTML = 'Self-Host';
      } finally {
        autohostBtn.disabled = false;
      }
    });
  }
});
"""

if "1-Click Autohost" not in js:
    with open("static/js/settings.js", "a") as f:
        f.write("\n" + event_listener)


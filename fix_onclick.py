import re
with open("static/index.html", "r") as f:
    text = f.read()

# First, remove the script tag I added earlier at the bottom
text = re.sub(r'<script>\n  document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{\n    // --- 1-Click Autohost ---.*?</script>\n', '', text, flags=re.DOTALL)

# Now, add onclick inline to the button
inline_js = """
async function runAutoHost() {
  const btn = document.getElementById('set-searchAutohostBtn');
  const urlInput = document.getElementById('set-searchUrl');
  btn.innerHTML = 'Starting...';
  btn.disabled = true;
  try {
    const res = await fetch('/api/search/autohost', { method: 'POST' });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed');
    urlInput.value = data.url;
    urlInput.dispatchEvent(new Event('change'));
    btn.innerHTML = '&#10003; Running';
    alert('SearXNG successfully launched via Docker! URL has been auto-filled.');
  } catch (err) {
    alert("Autohost failed: " + err.message);
    btn.innerHTML = 'Self-Host';
  } finally {
    btn.disabled = false;
  }
}
"""

# Replace the button to have onclick
text = text.replace(
    '<button id="set-searchAutohostBtn" class="theme-io-btn" style="height:32px; padding:0 12px; cursor:pointer;" title="1-Click Self-Host with Docker">',
    '<button id="set-searchAutohostBtn" class="theme-io-btn" style="height:32px; padding:0 12px; cursor:pointer;" title="1-Click Self-Host with Docker" onclick="runAutoHost()">'
)

# Insert the script at the end of body
text = text.replace('</body>', f'<script>{inline_js}</script>\n</body>')

with open("static/index.html", "w") as f:
    f.write(text)

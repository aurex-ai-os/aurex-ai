import re
with open("static/js/settings.js", "r") as f:
    text = f.read()

new_logic = r"""
  // --- 1-Click Autohost ---
  const autohostBtn = document.getElementById('set-searchAutohostBtn');
  if (autohostBtn) {
    autohostBtn.addEventListener('click', async () => {
      autohostBtn.innerHTML = '<span class="spinner" style="display:inline-block;margin-right:4px;">&#8987;</span> Starting...';
      autohostBtn.disabled = true;
      try {
        const res = await fetch('/api/search/autohost', { method: 'POST' });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Failed to start Docker');
        urlInput.value = data.url;
        autohostBtn.innerHTML = '&#10003; Running';
        msg.textContent = 'SearXNG successfully launched via Docker!';
        msg.style.color = 'var(--aurex-accent, #337AFF)';
      } catch (err) {
        alert("Autohost failed: " + err.message + "\n\nPlease ensure Docker Desktop is installed and running on your machine.");
        autohostBtn.innerHTML = 'Self-Host';
      } finally {
        autohostBtn.disabled = false;
      }
    });
  }
}
"""

text = re.sub(r'  load\(\);\n\}', '  load();\n' + new_logic, text)

with open("static/js/settings.js", "w") as f:
    f.write(text)

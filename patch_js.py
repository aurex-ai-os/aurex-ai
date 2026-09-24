import re
with open("static/js/settings.js", "r") as f:
    text = f.read()

new_js = r"""
  if (provSel) {
    provSel.addEventListener('change', function() {
      var val = provSel.value;
      if (val === 'custom') {
        alert('Custom search provider selected');
      } else {
        urlRow.style.display = (val === 'searxng') ? 'flex' : 'none';
        keyRow.style.display = _searchNeedsKey[val] ? 'flex' : 'none';
        cxRow.style.display = (val === 'google_pse') ? 'flex' : 'none';
        hint.innerHTML = _searchProviderHints[val] || '';
      }
    });
  }

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
        document.getElementById('set-searchUrl').value = data.url;
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
"""

text = re.sub(r'  if \(provSel\) \{\n    provSel\.addEventListener\(\'change\', function\(\) \{\n      var val = provSel\.value;\n      if \(val === \'custom\'\) \{\n        alert\(\'Custom search provider selected\'\);\n      \} else \{\n        urlRow\.style\.display = \(val === \'searxng\'\) \? \'flex\' : \'none\';\n        keyRow\.style\.display = _searchNeedsKey\[val\] \? \'flex\' : \'none\';\n        cxRow\.style\.display = \(val === \'google_pse\'\) \? \'flex\' : \'none\';\n        hint\.innerHTML = _searchProviderHints\[val\] \|\| \'\';\n      \}\n    \}\);\n  \}', new_js.strip('\n'), text)

with open("static/js/settings.js", "w") as f:
    f.write(text)

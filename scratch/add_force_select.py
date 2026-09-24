content = open("static/js/modelPicker.js").read()
if "aurex:force-select-model" not in content:
    idx = content.find("document.addEventListener('aurex:auto-select-model'")
    if idx != -1:
        new_code = """
  document.addEventListener('aurex:force-select-model', async (e) => {
    const detail = (e && e.detail) || {};
    const items = window.modelsModule && window.modelsModule.getCachedItems ? window.modelsModule.getCachedItems() : [];
    const targetModel = detail.modelId || '';
    let match = null;
    for (const item of items) {
      if (item.offline) continue;
      const models = (item.models || []).concat(item.models_extra || []);
      const displays = (item.models_display || []).concat(item.models_extra_display || []);
      const idx = models.indexOf(targetModel);
      if (idx >= 0) {
        match = {
          mid: targetModel,
          url: item.base_url || item.url || '',
          endpointId: item.endpoint_id || item.id || '',
          display: displays[idx] || targetModel
        };
        break;
      }
    }
    if (match) _pick(match);
  });
"""
        content = content[:idx] + new_code + "\n" + content[idx:]
        with open("static/js/modelPicker.js", "w") as f:
            f.write(content)
        print("Added aurex:force-select-model")
    else:
        print("Could not find insertion point")
else:
    print("Already added")

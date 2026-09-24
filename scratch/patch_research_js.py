import re

with open('static/js/chat.js', 'r') as f:
    chat_js = f.read()

# Patch 1: checkPendingResearch
old_block1 = """      const res = await fetch(`${API_BASE}/api/research/status/${sessionId}`);
      if (!res.ok) {
        if (sessionModule && sessionModule.clearResearching) sessionModule.clearResearching(sessionId);
        return; // 404 = no research for this session
      }
      const data = await res.json();"""

new_block1 = """      const res = await fetch(`${API_BASE}/api/research/status/${sessionId}`);
      if (!res.ok) {
        if (sessionModule && sessionModule.clearResearching) sessionModule.clearResearching(sessionId);
        return;
      }
      const data = await res.json();
      if (data.status === 'none' || data.active === false) {
        if (sessionModule && sessionModule.clearResearching) sessionModule.clearResearching(sessionId);
        return;
      }"""

chat_js = chat_js.replace(old_block1, new_block1)

# Patch 2: poll interval
old_block2 = """          const pollRes = await fetch(`${API_BASE}/api/research/status/${sessionId}`);
          if (!pollRes.ok) {
            clearInterval(pollInterval);
            spinner.destroy();
            _clearResearchTimer();
            _researchingStreamIds.delete(sessionId);
            if (sessionModule && sessionModule.clearResearching) sessionModule.clearResearching(sessionId);
            return;
          }"""

new_block2 = """          const pollRes = await fetch(`${API_BASE}/api/research/status/${sessionId}`);
          if (!pollRes.ok) {
            clearInterval(pollInterval);
            spinner.destroy();
            _clearResearchTimer();
            _researchingStreamIds.delete(sessionId);
            if (sessionModule && sessionModule.clearResearching) sessionModule.clearResearching(sessionId);
            return;
          }
          const pollData = await pollRes.clone().json().catch(() => ({}));
          if (pollData.status === 'none' || pollData.active === false) {
            clearInterval(pollInterval);
            spinner.destroy();
            _clearResearchTimer();
            _researchingStreamIds.delete(sessionId);
            if (sessionModule && sessionModule.clearResearching) sessionModule.clearResearching(sessionId);
            return;
          }"""

chat_js = chat_js.replace(old_block2, new_block2)

with open('static/js/chat.js', 'w') as f:
    f.write(chat_js)

print("Patched chat.js for research/status")

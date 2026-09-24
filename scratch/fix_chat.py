with open('static/js/chat.js', 'r') as f:
    chat_js = f.read()

# Replace the duplicate declaration
old_block = """          const pollData = await pollRes.clone().json().catch(() => ({}));
          if (pollData.status === 'none' || pollData.active === false) {
            clearInterval(pollInterval);
            spinner.destroy();
            _clearResearchTimer();
            _researchingStreamIds.delete(sessionId);
            if (sessionModule && sessionModule.clearResearching) sessionModule.clearResearching(sessionId);
            return;
          }
          const pollData = await pollRes.json();"""

new_block = """          const pollData = await pollRes.json().catch(() => ({}));
          if (pollData.status === 'none' || pollData.active === false) {
            clearInterval(pollInterval);
            spinner.destroy();
            _clearResearchTimer();
            _researchingStreamIds.delete(sessionId);
            if (sessionModule && sessionModule.clearResearching) sessionModule.clearResearching(sessionId);
            return;
          }"""

chat_js = chat_js.replace(old_block, new_block)

with open('static/js/chat.js', 'w') as f:
    f.write(chat_js)
print("Fixed chat.js syntax")

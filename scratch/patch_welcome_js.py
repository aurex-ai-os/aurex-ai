with open('static/index.html', 'r') as f:
    html = f.read()

script = """
      <script>
        document.addEventListener('DOMContentLoaded', () => {
          document.querySelectorAll('.welcome-card').forEach(card => {
            card.addEventListener('click', () => {
              const prompt = card.getAttribute('data-prompt');
              const textarea = document.getElementById('chat-input');
              if (textarea) {
                textarea.value = prompt;
                textarea.focus();
                // trigger input event to auto-resize
                textarea.dispatchEvent(new Event('input', { bubbles: true }));
              }
            });
          });
        });
      </script>"""

# Insert right after the welcome-setup-grid div
idx = html.find('        </div>\n      </div>')
if idx != -1:
    idx += len('        </div>\n      </div>')
    html = html[:idx] + script + html[idx:]
    with open('static/index.html', 'w') as f:
        f.write(html)
    print("Injected JS for welcome cards")
else:
    print("Could not find insertion point")

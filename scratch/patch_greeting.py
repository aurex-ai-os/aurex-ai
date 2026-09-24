with open('static/index.html', 'r') as f:
    html = f.read()

greeting_script = """
      <script>
        (function(){
          const hour = new Date().getHours();
          let greeting = "New chat ready.";
          if (hour < 12) greeting = "Good morning! Ready to tackle today's tasks?";
          else if (hour < 18) greeting = "Good afternoon! How can I help?";
          else greeting = "Late night coding session? I'm here to help.";
          const sub = document.getElementById('welcome-sub');
          if (sub) sub.textContent = greeting;
        })();
      </script>"""

idx = html.find('<div class="welcome-sub" id="welcome-sub">New chat ready.</div>')
if idx != -1:
    idx += len('<div class="welcome-sub" id="welcome-sub">New chat ready.</div>')
    html = html[:idx] + greeting_script + html[idx:]
    with open('static/index.html', 'w') as f:
        f.write(html)
    print("Patched welcome greeting")
else:
    print("Could not find welcome-sub")

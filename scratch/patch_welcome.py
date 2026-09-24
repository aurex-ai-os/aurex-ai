import re

with open('static/index.html', 'r') as f:
    html = f.read()

# Replace <div id="welcome-setup" style="display:none"></div>
new_welcome = """      <div id="welcome-setup" class="welcome-setup-grid" style="display:none; margin-top: 32px;">
        <div class="welcome-grid-cards">
          <div class="welcome-card" data-prompt="Help me debug a complex issue in my code. I'll provide the snippets.">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            <div class="welcome-card-text">
              <h4>Debug Code</h4>
              <p>Find bugs and fix errors</p>
            </div>
          </div>
          <div class="welcome-card" data-prompt="Explain a complex technical concept to me as if I'm a beginner.">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            <div class="welcome-card-text">
              <h4>Explain Concept</h4>
              <p>Break down complex topics</p>
            </div>
          </div>
          <div class="welcome-card" data-prompt="Help me brainstorm ideas and outline a new project.">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M2 12h20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            <div class="welcome-card-text">
              <h4>Brainstorm</h4>
              <p>Generate ideas and outlines</p>
            </div>
          </div>
          <div class="welcome-card" data-prompt="Review this pull request or code diff for best practices and security.">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M6 9v12"/><path d="M18 15V9a6 6 0 0 0-6-6H6"/></svg>
            <div class="welcome-card-text">
              <h4>Code Review</h4>
              <p>Analyze diffs for quality</p>
            </div>
          </div>
        </div>
      </div>"""

html = html.replace('<div id="welcome-setup" style="display:none"></div>', new_welcome)

# Wait, we need to show the grid. Let's remove the style="display:none;" in python string but I already set it to display:none above.
# I'll just change it to display:flex or block!
html = html.replace('class="welcome-setup-grid" style="display:none; margin-top: 32px;"', 'class="welcome-setup-grid" style="display:flex; justify-content:center; margin-top: 32px;"')

with open('static/index.html', 'w') as f:
    f.write(html)
print("Added welcome grid HTML")

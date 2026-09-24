import re

with open("static/index.html", "r") as f:
    html = f.read()

# I will extract the pi-detail-panel and put it inside pi-modal-content, right before its closing div.
# First, find pi-detail-panel block
panel_start = html.find('<!-- MODEL DETAIL PANEL (Slides in over the content) -->')
# find the end of the detail panel div
# Since it doesn't have nested complex divs, we can search for the next '</div>' that closes it.
# Actually it has nested divs. Let's just use regex or manual slicing.
panel_end_str = '</div>\n</div>\n<!-- Provider Intelligence UI Injected -->'

# It was inserted right before settings-modal
settings_modal = '<div id="settings-modal" class="modal hidden">'

# Let's just use string replacement carefully
old_block = """    </div>
  </div>
</div>

<!-- MODEL DETAIL PANEL (Slides in over the content) -->
<div class="pi-detail-panel hidden" id="pi-model-detail">
  <div class="pi-detail-header">
    <button class="pi-detail-back" id="pi-detail-back-btn">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
    </button>
    <h3>Model Details</h3>
  </div>
  <div class="pi-detail-body" id="pi-model-detail-body">
    <!-- Populated by JS -->
  </div>
</div>"""

new_block = """      <!-- MODEL DETAIL PANEL (Slides in over the content) -->
      <div class="pi-detail-panel hidden" id="pi-model-detail">
        <div class="pi-detail-header">
          <button class="pi-detail-back" id="pi-detail-back-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
          </button>
          <h3>Model Details</h3>
        </div>
        <div class="pi-detail-body" id="pi-model-detail-body">
          <!-- Populated by JS -->
        </div>
      </div>
    </div>
  </div>
</div>"""

if old_block in html:
    html = html.replace(old_block, new_block)
else:
    print("Could not find the exact old block")

with open("static/index.html", "w") as f:
    f.write(html)

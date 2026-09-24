import re

with open('static/index.html', 'r') as f:
    html = f.read()

# I will extract the blocks for Compare, Cookbook, Deep Research, Gallery
# and put them into a new details block.

def extract_block(html, btn_id):
    start = html.find(f'<div class="list-item" id="{btn_id}">')
    if start == -1: return None, html
    # find the next <div class="list-item" or <div class="section"
    next_div = html.find('<div class="list-item"', start + 1)
    if next_div == -1: next_div = html.find('<div class="section"', start + 1)
    if next_div == -1: next_div = html.find('</div>\n      </div>', start + 1) # end of tools-section
    
    block = html[start:next_div]
    html = html[:start] + html[next_div:]
    return block, html

compare_block, html = extract_block(html, 'tool-compare-btn')
cookbook_block, html = extract_block(html, 'tool-cookbook-btn')
research_block, html = extract_block(html, 'tool-research-btn')
gallery_block, html = extract_block(html, 'tool-gallery-btn')

details_html = f"""
        <details class="advanced-tools-details" style="margin-top: 8px;">
          <summary class="list-item" style="cursor:pointer; opacity: 0.8;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
            <span class="grow" style="font-weight: 500; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">Advanced</span>
            <svg class="chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </summary>
          <div class="advanced-tools-content" style="padding-left: 12px; border-left: 1px solid var(--border); margin-left: 18px; margin-top: 4px; margin-bottom: 8px;">
{compare_block}{cookbook_block}{research_block}{gallery_block}          </div>
        </details>
"""

# insert details_html at the end of tools-section (before the closing div of tools-section)
# we need to find the end of tools-section
tools_end = html.find('      </div>\n      <!-- Hidden dropdown for session actions -->')
if tools_end != -1:
    html = html[:tools_end] + details_html + html[tools_end:]
    with open('static/index.html', 'w') as f:
        f.write(html)
    print("Grouped successfully!")
else:
    print("Failed to find tools_end")


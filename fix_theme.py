import re

with open("static/aurex-theme.css", "r") as f:
    css = f.read()

# I will replace the pi- specific css colors.
# Find the start of the PI block
pi_start = css.find("/* =========================================================================")
if pi_start != -1:
    pi_block = css[pi_start:]
    
    # Replace colors
    pi_block = pi_block.replace("background: #0A0A0A", "background: var(--aurex-bg)")
    pi_block = pi_block.replace("background: #141414", "background: var(--aurex-surface)")
    pi_block = pi_block.replace("color: #fff", "color: var(--aurex-text)")
    pi_block = pi_block.replace("rgba(255, 255, 255, 0.08)", "var(--aurex-border)")
    pi_block = pi_block.replace("rgba(255, 255, 255, 0.05)", "var(--aurex-border)")
    pi_block = pi_block.replace("rgba(255, 255, 255, 0.06)", "var(--aurex-border)")
    pi_block = pi_block.replace("rgba(255, 255, 255, 0.1)", "var(--aurex-border)")
    pi_block = pi_block.replace("rgba(255, 255, 255, 0.12)", "var(--aurex-border-hover)")
    pi_block = pi_block.replace("rgba(255, 255, 255, 0.5)", "var(--aurex-text-muted)")
    pi_block = pi_block.replace("rgba(255, 255, 255, 0.4)", "var(--aurex-text-subtle)")
    pi_block = pi_block.replace("rgba(255, 255, 255, 0.6)", "var(--aurex-text-muted)")
    pi_block = pi_block.replace("rgba(255, 255, 255, 0.7)", "var(--aurex-text)")
    pi_block = pi_block.replace("rgba(255, 255, 255, 0.2)", "var(--aurex-border)")
    
    # Also replace accent overrides
    pi_block = re.sub(r"var\(--accent,\s*#337AFF\)", "var(--aurex-accent)", pi_block)
    pi_block = re.sub(r"rgba\(var\(--accent-rgb,\s*51,\s*122,\s*255\),\s*0\.1\)", "var(--aurex-accent-soft)", pi_block)

    # Some missed variations
    pi_block = pi_block.replace("rgba(255,255,255,0.05)", "var(--aurex-border)")
    pi_block = pi_block.replace("rgba(255,255,255,0.08)", "var(--aurex-border)")
    pi_block = pi_block.replace("rgba(255,255,255,0.1)", "var(--aurex-border)")
    pi_block = pi_block.replace("rgba(255,255,255,0.5)", "var(--aurex-text-muted)")
    pi_block = pi_block.replace("rgba(255,255,255,0.4)", "var(--aurex-text-subtle)")
    pi_block = pi_block.replace("rgba(255,255,255,0.6)", "var(--aurex-text-muted)")

    css = css[:pi_start] + pi_block

with open("static/aurex-theme.css", "w") as f:
    f.write(css)


import os
import sys

# Try to use python to read the svg and save as ico and png
try:
    from PIL import Image
    import cairosvg
    import io
    
    # Read SVG
    with open("static/index.html", "r") as f:
        html = f.read()
    
    # Extract the SVG logo we injected
    import re
    match = re.search(r'<svg class="welcome-boat" viewBox="0 0 32 32".*?</svg>', html, re.DOTALL)
    if match:
        svg_content = match.group(0)
        # Add xmlns
        svg_content = svg_content.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ')
        
        # Convert SVG to PNG in memory
        png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), output_width=256, output_height=256)
        
        # Open with PIL
        img = Image.open(io.BytesIO(png_data))
        
        # Save as ICO (Windows)
        img.save("static/icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        print("Generated static/icon.ico")
        
        # Save as PNG (Linux/Mac)
        img.save("static/icon.png", format="PNG")
        print("Generated static/icon.png")
        
        # For Mac ICNS, we can just use the PNG for now, or create an ICNS if supported
        try:
            # Not natively supported by PIL for writing ICNS easily, but we can try
            img.save("static/icon.icns", format="ICNS")
            print("Generated static/icon.icns")
        except Exception:
            print("Pillow cannot save ICNS directly, saving as png fallback")
            
except Exception as e:
    print(f"Error: {e}")


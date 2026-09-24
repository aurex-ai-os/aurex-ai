import sys
import os
import subprocess
import time

try:
    import webview
except ImportError:
    print("Please install pywebview: pip install pywebview")
    sys.exit(1)

# Ensure the server is running or start it
# For now, we just point to the existing server
url = "http://localhost:7000"

window = webview.create_window(
    'Aurex Desktop', 
    url, 
    width=1280, 
    height=800,
    min_size=(800, 600),
    background_color='#0D0D0F'
)

webview.start()

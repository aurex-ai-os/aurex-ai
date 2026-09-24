import re

with open('launcher.py', 'r') as f:
    content = f.read()

# Replace the open_browser logic and uvicorn run logic
old_block = """    if getattr(sys, 'frozen', False):
        # Start browser manager thread
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()
        # Start system tray manager thread
        threading.Thread(target=setup_system_tray, args=(url,), daemon=True).start()

    uvicorn.run(app, host=bind_host, port=bind_port, log_level="info")"""

new_block = """    if getattr(sys, 'frozen', False):
        # Start system tray manager thread
        threading.Thread(target=setup_system_tray, args=(url,), daemon=True).start()
        
        # Start Uvicorn in a background thread
        server_thread = threading.Thread(
            target=uvicorn.run, 
            args=(app,), 
            kwargs={"host": bind_host, "port": bind_port, "log_level": "info"}, 
            daemon=True
        )
        server_thread.start()
        
        # Open Dedicated App Window on the main thread
        import time
        time.sleep(1.5)  # Wait for server to boot
        try:
            import webview
            window = webview.create_window('Aurex', url, width=1280, height=800, background_color='#0D0D0F')
            webview.start()
        except ImportError:
            import webbrowser
            webbrowser.open(url)
            server_thread.join()
    else:
        uvicorn.run(app, host=bind_host, port=bind_port, log_level="info")"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('launcher.py', 'w') as f:
        f.write(content)
    print("Patched launcher.py for PyWebView")
else:
    print("Could not find block in launcher.py")

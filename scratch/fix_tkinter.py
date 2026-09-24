import re

with open('launcher.py', 'r') as f:
    content = f.read()

# Move import tkinter into the try block
old_code = """    import tkinter as tk

    def show_splash_instantly():
        global splash_root
        try:
            splash_root = tk.Tk()"""

new_code = """    def show_splash_instantly():
        global splash_root
        try:
            import tkinter as tk
            splash_root = tk.Tk()"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('launcher.py', 'w') as f:
        f.write(content)
    print("Fixed launcher.py")
else:
    print("Could not find old code in launcher.py")

with open('static/index.html', 'r') as f:
    html = f.read()

html = html.replace('<script>', '<script nonce="{{CSP_NONCE}}">')

with open('static/index.html', 'w') as f:
    f.write(html)
print("Fixed CSP nonces")

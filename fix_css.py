import re

files = ['Nota_KAFA_Aqil.html', 'index.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add new variable --bg-tabs
    content = content.replace('--bg-card: #FFFFFF;', '--bg-card: #FFFFFF;\n            --bg-tabs: rgba(255,255,255,0.95);')
    content = content.replace('--bg-card: #2D3748;', '--bg-card: #2D3748;\n            --bg-tabs: rgba(26,32,44,0.95);')
    
    # Replace hardcoded white backgrounds (except inside print media queries which usually have !important)
    # We will just replace exactly "background: white;" and "background-color: white;" where applicable.
    content = content.replace('background: white;', 'background: var(--bg-card);')
    
    # Fix mode-tabs background
    content = content.replace('background: rgba(255,255,255,0.95);', 'background: var(--bg-tabs);')

    # Fix version badge
    content = content.replace('background: rgba(255, 255, 255, 0.15);', 'background: var(--bg-card);\n            opacity: 0.8;')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("CSS fixed for dark mode!")

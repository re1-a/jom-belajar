import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract VOCAB_DATA object
match = re.search(r'const VOCAB_DATA = ({.*?});\s*// ==================', content, re.DOTALL)
if match:
    # It's not pure JSON, so we have to do some regex parsing or just parse it manually
    data_str = match.group(1)
    
    topics = re.findall(r'([a-z]+):\s*{\s*title:\s*"([^"]+)",\s*titleAr:\s*"([^"]+)",\s*emoji:\s*"([^"]+)",.*?items:\s*\[(.*?)\]\s*}', data_str, re.DOTALL)
    
    md = "# Silibus Lughatul Arabiyyah (KAFA Darjah 2)\n\n"
    md += "Nota ini menyenaraikan keseluruhan 80 perkataan bahasa Arab mengikut sukatan rasmi KAFA Selangor Darjah 2.\n\n"
    
    for key, title, titleAr, emoji, items_str in topics:
        md += f"## {emoji} {title} ({titleAr})\n\n"
        md += "| Bil | Bahasa Melayu | Rumi | Bahasa Arab |\n"
        md += "|---|---|---|---|\n"
        
        items = re.findall(r'{\s*bm:\s*"([^"]+)",\s*rumi:\s*"([^"]+)",\s*arab:\s*"([^"]+)",\s*emoji:\s*"([^"]+)"\s*}', items_str)
        
        for i, (bm, rumi, arab, i_emoji) in enumerate(items):
            md += f"| {i+1} | {i_emoji} {bm} | {rumi} | {arab} |\n"
            
        md += "\n"
        
    print(md)

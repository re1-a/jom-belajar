import re

js_path = 'sains-darjah2/script.js'

with open(js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to remove `, image: 'images/fox_...png?v=2'` from script.js
# This regex will find and remove `, image: 'images/fox_[a-zA-Z0-9_]+.png\?v=2'`
content = re.sub(r", image: 'images/fox_[^']+\.png\?v=2'", "", content)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed all fox images from quiz data successfully!")

import json
import base64
import re
from gtts import gTTS
import os

# Read index.html to extract VOCAB_DATA
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract rumi and arab pairs using regex globally
items = re.findall(r'rumi:\s*"([^"]+)",\s*arab:\s*"([^"]+)"', content)

audio_data = {}
for rumi, arab in items:
    print(f"Generating audio for {rumi} ({arab})...")
    # Clean up any invisible characters or weird spaces if any
    arab_clean = arab.strip()
    
    tts = gTTS(arab_clean, lang='ar')
    tmp_file = "tmp.mp3"
    tts.save(tmp_file)
    with open(tmp_file, "rb") as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
        audio_data[rumi] = f"data:audio/mp3;base64,{b64}"

with open("audio_db.js", "w", encoding='utf-8') as f:
    f.write("const AUDIO_DB = " + json.dumps(audio_data, ensure_ascii=False) + ";\n")

if os.path.exists("tmp.mp3"):
    os.remove("tmp.mp3")
print("Successfully generated audio_db.js with native Arabic TTS!")

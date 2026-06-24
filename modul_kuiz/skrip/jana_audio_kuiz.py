import re
import json
import base64
import os
from gtts import gTTS

subjects = {
    "tauhid": "../tauhid/tauhid.html",
    "feqah": "../feqah/feqah.html",
    "bahasa-arab": "../bahasa-arab/bahasa-arab.html"
}

# Ensure we're running from the skrip directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

for subject, html_path in subjects.items():
    if not os.path.exists(html_path):
        print(f"Skipping {subject}, file not found at {html_path}")
        continue
    
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract all questions and options using regex
    questions = re.findall(r'q:\s*"([^"]+)"', content)
    options_raw = re.findall(r'options:\s*\[(.*?)\]', content)
    
    options = []
    for opt_str in options_raw:
        opts = re.findall(r'"([^"]+)"', opt_str)
        options.extend(opts)
        
    all_texts = list(set(questions + options))
    
    if not all_texts:
        print(f"No quiz data found for {subject}")
        continue
        
    print(f"Found {len(all_texts)} audio items for {subject}. Generating audio...")
    
    audio_db = {}
    for i, text in enumerate(all_texts):
        # Phonetic cleanup for Malay/Indo TTS
        clean_text = text.replace("'", " ")
        clean_text = re.sub(r'qa', 'qo', clean_text, flags=re.I)
        
        try:
            # Using 'id' (Indonesian) because it often pronounces Arabic/Malay words better than 'ms'
            tts = gTTS(clean_text, lang='id')
            tmp_file = f"tmp_{subject}.mp3"
            tts.save(tmp_file)
            
            with open(tmp_file, "rb") as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')
                # Use base64 string of the text as a safe dictionary key for JS
                key = base64.b64encode(text.encode('utf-8')).decode('utf-8')
                audio_db[key] = f"data:audio/mp3;base64,{b64}"
                
            os.remove(tmp_file)
        except Exception as e:
            print(f"Error generating audio for '{text}': {e}")
            
    # Save the generated audio dictionary to audio_db.js
    db_path = os.path.join(os.path.dirname(html_path), "audio_db.js")
    with open(db_path, "w", encoding="utf-8") as f:
        f.write("const AUDIO_DB = " + json.dumps(audio_db) + ";\n")
    print(f"SUCCESS: Saved audio database for {subject} at {db_path}\n")

print("All audio generation complete.")

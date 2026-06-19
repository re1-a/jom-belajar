import json
import base64
import re
from gtts import gTTS
import os

vocab = [
    "Wahidun", "Ithnani", "Thalathatun", "Arba'atun", "Khamsatun", "Sittatun", "Sab'atun", "Thamaniyatun", "Tis'atun", "'Asharatun",
    "Ahada 'Asyara", "Ithna 'Asyara", "Thalathata 'Asyara", "Arba'ata 'Asyara", "Khamsata 'Asyara", "'Isyruna", "Thalathuna", "Arba'una", "Khamsuna", "Mi'atun", "Mi'atani",
    "Ahmaru", "Azraqu", "Asfaru", "Akhdaru", "Aswadu", "Abyadu", "Burtuqaliyyun", "Banafsajiyyun", "Ramadiyyun", "Bunniyyun", "Wardiyyun",
    "Qittun", "Arnabun", "Dajajatun", "Samakatun", "Tairun", "Kharufun", "Baqaratun", "Hisanun", "Jamalun", "Asadun", "Filun", "Farashatun",
    "Kuratul Qadami", "Kuratur Rishati", "Kuratus Sallati", "Kuratut Ta'irati", "As-Sibahatu", "Ar-Rimayatu", "Rukubul Khaili", "Al-Jaryu", "Asy-Syitranju", "Kuratul Midrabi", "Kuratul Tawilati", "Kuratul Yadi",
    "Qamisun", "Thawbun", "Khimarun", "Hiza'un", "Sirwalun", "Jawrabun", "'Imamatun", "Qalansuwatun", "Na'lun", "Izarun", "Hizamun", "Minsyafatun",
    "Jazarun", "Khiyarun", "Tamatimun", "Thaumun", "Basalun", "Bazinjanun", "Filfilun", "Batatisun", "Dhurratun", "Fitrun",
    "Tuffahatun", "Mawzatun", "Burtuqalatun", "'Inabun", "Battikhun", "Laymunun", "Ananasun", "Farawlatun", "Manja", "Kummathra",
    "Aruzzun", "Khubzun", "Ma'un", "Halibun", "Shayun", "Lahmun", "Samakun", "Baydatun", "Syukulatatun", "Ka'kun", "'Asirun", "Biskuitun"
]

audio_data = {}
for word in vocab:
    # Phonetic cleanup for Indonesian Google TTS
    text = word.replace("'", " ")
    text = re.sub(r'qa', 'qo', text, flags=re.I)
    
    tts = gTTS(text, lang='id')
    tmp_file = "tmp.mp3"
    tts.save(tmp_file)
    with open(tmp_file, "rb") as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
        audio_data[word] = f"data:audio/mp3;base64,{b64}"

with open("audio_db.js", "w") as f:
    f.write("const AUDIO_DB = " + json.dumps(audio_data) + ";\n")

if os.path.exists("tmp.mp3"):
    os.remove("tmp.mp3")
print("Generated audio_db.js")

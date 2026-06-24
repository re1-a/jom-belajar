#!/usr/bin/env python3
# ==========================================================
# generate_sains_audio.py
# Pra-jana audio Bahasa Melayu untuk Sains Explorer v2 — versi STATIK
# sesuai untuk dikongsi di GitHub Pages.
#
# Output:
#   audio/<hash>.mp3            <- klip individu (cache, load bila perlu)
#   js/sains_audio_db.js        <- manifest: { "teks": "audio/<hash>.mp3", ... }
#
# Aplikasi auto-guna manifest ni kalau wujud; kalau teks tiada klip, ia
# fallback ke suara browser. Commit folder audio/ + js/sains_audio_db.js
# ke repo, dan semua pelawat dapat suara yang sama tanpa setup.
#
# Cara guna (di mesin anda yang ada internet):
#   pip install gtts
#   python3 generate_sains_audio.py
#
# Nak suara lebih natural? Tukar ENGINE = "gemini" dan set GEMINI_API_KEY.
# (Kos token sekali sahaja masa jana; output kekal statik & percuma untuk pelawat.)
# ==========================================================

import os, re, json, base64, hashlib, sys

HERE     = os.path.dirname(os.path.abspath(__file__))
NOTES_JS = os.path.join(HERE, 'js', 'notes_data.js')
AUDIO_DIR= os.path.join(HERE, 'audio')
OUT_JS   = os.path.join(HERE, 'js', 'sains_audio_db.js')

ENGINE   = "gtts"          # "gtts" (percuma) atau "gemini" (lebih natural, perlu key)
LANG     = "ms"            # gTTS: Bahasa Melayu sahaja.
GEMINI_VOICE = "Kore"      # hanya untuk ENGINE="gemini" (cuba juga "Puck", "Aoede")
GEMINI_MODEL = "gemini-2.5-flash-preview-tts"   # model TTS Gemini
# Arahan gaya — di sinilah "happy/excited" datang (Gemini boleh ikut emosi):
GEMINI_STYLE = "Sebut dengan ceria, mesra dan penuh semangat macam cikgu tadika bercerita kepada kanak-kanak 7 tahun"

EMOJI_RE = re.compile('[\U0001F000-\U0001FFFF☀-➿]', flags=re.UNICODE)

def clean(text):
    """Mesti SAMA dengan AudioFX cleaning dalam js/audio.js supaya kunci sepadan."""
    return EMOJI_RE.sub('', str(text)).strip()

def extract_field(blob, field):
    return re.findall(field + r"\s*:\s*'((?:[^'\\]|\\.)*)'", blob)

def collect_strings(blob):
    s = set()
    for fld in ['frontQuestion', 'frontTitle', 'backTitle', 'backAnswer', 'trivia']:
        for v in extract_field(blob, fld):
            s.add(clean(v))
    answers = extract_field(blob, 'backAnswer')
    trivias = extract_field(blob, 'trivia')
    fronts  = extract_field(blob, 'frontTitle')
    titles  = extract_field(blob, 'backTitle')
    for a, t in zip(answers, trivias):
        s.add(clean(a + ' 💡 ' + t))
    for fr, ti in zip(fronts, titles):
        s.add(clean(fr + ': ' + ti))
    s.update(clean(x) for x in [
        'Betul atau salah?', 'Betul', 'Salah',
        'Hai! Saya Boti. Jom terokai pulau sains!',
        'Wah, hebatnya!', 'Betul! Kamu memang bijak!', 'Pandai!',
        'Tak apa, cuba lagi ya!', 'Hampir betul! Jangan putus asa.',
    ])
    return sorted(x for x in s if x)

# ---- enjin TTS ----
def tts_gtts(text, path):
    from gtts import gTTS
    gTTS(text, lang=LANG).save(path)

def tts_gemini(text, path):
    # Guna Gemini TTS (perlu: pip install google-genai ; export GEMINI_API_KEY=...)
    from google import genai
    from google.genai import types
    import wave
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=f"{GEMINI_STYLE}: {text}",
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=GEMINI_VOICE)))))
    pcm = resp.candidates[0].content.parts[0].inline_data.data
    wav_path = path.replace('.mp3', '.wav')
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    # cuba tukar ke mp3 kalau ffmpeg ada; kalau tak, simpan .wav
    if os.system(f'ffmpeg -y -loglevel quiet -i "{wav_path}" "{path}"') == 0:
        os.remove(wav_path)
    else:
        return wav_path
    return path

def main():
    if not os.path.exists(NOTES_JS):
        sys.exit("Tak jumpa: " + NOTES_JS)
    with open(NOTES_JS, encoding='utf-8') as f:
        blob = f.read()
    strings = collect_strings(blob)

    engine = {"gtts": tts_gtts, "gemini": tts_gemini}.get(ENGINE)
    if not engine:
        sys.exit("ENGINE tak sah: " + ENGINE)
    os.makedirs(AUDIO_DIR, exist_ok=True)

    print(f"Menjana {len(strings)} klip (engine={ENGINE})...")
    manifest = {}
    for i, s in enumerate(strings, 1):
        h = hashlib.md5(s.encode('utf-8')).hexdigest()[:12]
        fname = h + '.mp3'
        fpath = os.path.join(AUDIO_DIR, fname)
        try:
            result = engine(s, fpath)
            rel = os.path.relpath(result if result else fpath, HERE).replace(os.sep, '/')
            manifest[s] = rel
            print(f"  [{i}/{len(strings)}] OK  {rel}")
        except Exception as e:
            print(f"  [{i}/{len(strings)}] GAGAL: {e}")

    with open(OUT_JS, 'w', encoding='utf-8') as f:
        f.write('window.SAINS_AUDIO_DB = ' + json.dumps(manifest, ensure_ascii=False, indent=0) + ';\n')

    total = sum(os.path.getsize(os.path.join(HERE, p)) for p in manifest.values() if os.path.exists(os.path.join(HERE, p)))
    print(f"Siap → {len(manifest)} klip, jumlah {total/1024/1024:.1f} MB")
    print("Commit folder audio/ + js/sains_audio_db.js ke repo anda.")

if __name__ == '__main__':
    main()

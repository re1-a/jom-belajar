from gtts import gTTS
import base64
tts = gTTS('أَحْمَرُ', lang='ar')
tts.save('test_ahmaru.mp3')
with open('test_ahmaru.mp3', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')
    with open('test_ahmaru_b64.txt', 'w') as out:
        out.write('data:audio/mp3;base64,' + b64)

html_content = f'''<!DOCTYPE html>
<html>
<head>
<meta charset=\"utf-8\">
<style>
  body {{ font-family: sans-serif; text-align: center; padding: 50px; background: #f0fdf4; }}
  button {{ padding: 20px 40px; font-size: 24px; background: #22c55e; color: white; border: none; border-radius: 12px; cursor: pointer; }}
</style>
</head>
<body>
  <h2>Test Suara Merah (Google Arabic - أَحْمَرُ)</h2>
  <button onclick=\"playAudio()\">🔊 Dengar Merah</button>
  <script>
    function playAudio() {{
      const audio = new Audio('data:audio/mp3;base64,{b64}');
      audio.play();
    }}
  </script>
</body>
</html>
'''
with open('test_suara.html', 'w') as f:
    f.write(html_content)

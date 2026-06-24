import os

html_files = [
    "../tauhid/tauhid.html",
    "../feqah/feqah.html",
    "../bahasa-arab/bahasa-arab.html"
]

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

css_injection = """
        .audio-btn {
            background: rgba(139, 92, 246, 0.1);
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            margin-right: 8px;
            padding: 4px 8px;
            transition: transform 0.2s;
        }
        .audio-btn:hover {
            transform: scale(1.2);
            background: rgba(139, 92, 246, 0.2);
        }
"""

js_injection = """
        // Play Audio Function
        function playAudio(base64text) {
            if (typeof AUDIO_DB !== 'undefined' && AUDIO_DB[base64text]) {
                const audio = new Audio(AUDIO_DB[base64text]);
                audio.play();
            } else {
                console.warn("Audio not found");
            }
        }
"""

for html_path in html_files:
    if not os.path.exists(html_path):
        continue
    
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Inject <script src="audio_db.js"></script>
    if '<script src="audio_db.js"></script>' not in content:
        content = content.replace('<script>', '<script src="audio_db.js"></script>\n    <script>', 1)
        
    # 2. Inject CSS
    if '.audio-btn' not in content:
        content = content.replace('</style>', f'{css_injection}</style>', 1)
        
    # 3. Inject playAudio function
    if 'function playAudio' not in content:
        content = content.replace('<script src="audio_db.js"></script>\n    <script>', f'<script src="audio_db.js"></script>\n    <script>\n{js_injection}')

    # 4. Modify renderQuizQuestion HTML template
    
    # Options injection
    old_opt = "optionsHtml += `<div class=\"quiz-option\" onclick=\"selectAnswer(${idx}, ${q.answer})\">${opt}</div>`;"
    new_opt = "optionsHtml += `<div class=\"quiz-option\" onclick=\"selectAnswer(${idx}, ${q.answer})\"><button class=\"audio-btn\" onclick=\"playAudio(btoa(unescape(encodeURIComponent(opt)))); event.stopPropagation();\">🔊</button> ${opt}</div>`;"
    content = content.replace(old_opt, new_opt)

    # Question injection
    old_q = "<div class=\"quiz-question\">${q.q}</div>"
    new_q = "<div class=\"quiz-question\"><button class=\"audio-btn\" onclick=\"playAudio(btoa(unescape(encodeURIComponent(q.q))))\">🔊</button> ${q.q}</div>"
    content = content.replace(old_q, new_q)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("HTML injection complete.")

import json

html_content = """<!DOCTYPE html>
<html lang="ms" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bijak KAFA — Nota Tauhid Darjah 2</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&family=Amiri:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #FDF6E3;
            --bg-card: #FFFFFF;
            --bg-tabs: rgba(255,255,255,0.95);
            --bg-header: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
            --text-primary: #2D3748;
            --text-secondary: #4A5568;
            --text-light: #718096;
            --border: #E2E8F0;
            --shadow: 0 4px 20px rgba(0,0,0,0.08);
            --radius: 16px;
            --radius-sm: 10px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            
            --correct-bg: #C6F6D5;
            --correct: #48BB78;
            --wrong-bg: #FED7D7;
            --wrong: #F56565;
        }

        body {
            font-family: 'Lexend', sans-serif;
            background-color: var(--bg-main);
            color: var(--text-primary);
            line-height: 1.8;
            font-size: 16px;
            margin: 0;
            padding: 0;
            -webkit-font-smoothing: antialiased;
        }

        .app-header {
            position: relative;
            background: var(--bg-header);
            color: white;
            padding: 28px 24px;
            text-align: center;
            box-shadow: 0 4px 30px rgba(139, 92, 246, 0.4);
        }

        .app-header h1 { font-size: 28px; margin: 0 0 4px 0; }
        .app-header .subtitle { font-size: 14px; opacity: 0.9; }
        
        .btn-home-header {
            position: absolute;
            top: 12px;
            left: 16px;
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 13px;
            text-decoration: none;
            font-weight: bold;
            border: 1px solid rgba(255,255,255,0.3);
        }

        .version-badge {
            position: absolute;
            top: 12px;
            right: 16px;
            background: var(--bg-card);
            color: #8b5cf6;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
        }

        .mode-tabs {
            display: flex;
            justify-content: center;
            gap: 8px;
            padding: 16px 24px;
            background: var(--bg-tabs);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .mode-tab {
            padding: 10px 24px;
            border: 2px solid var(--border);
            border-radius: 50px;
            background: var(--bg-card);
            font-family: 'Lexend', sans-serif;
            font-size: 15px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
        }

        .mode-tab.active {
            background: linear-gradient(135deg, #8b5cf6, #6d28d9);
            color: white;
            border-color: transparent;
        }

        .topic-filters {
            display: flex;
            gap: 8px;
            padding: 16px 24px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .topic-pill {
            padding: 8px 18px;
            border-radius: 50px;
            border: 2px solid var(--border);
            background: var(--bg-card);
            font-family: 'Lexend', sans-serif;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            color: var(--text-secondary);
        }

        .topic-pill.active {
            background: #8b5cf6;
            color: white;
            border-color: transparent;
        }

        .content-area {
            max-width: 900px;
            margin: 0 auto;
            padding: 8px 20px 40px;
        }

        .nota-card {
            background: var(--bg-card);
            border-radius: var(--radius);
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: var(--shadow);
            border: 1px solid var(--border);
        }

        .nota-card h2 {
            color: #6d28d9;
            margin-top: 0;
            border-bottom: 2px solid var(--border);
            padding-bottom: 10px;
        }

        .nota-card h3 {
            color: #8b5cf6;
            margin-bottom: 8px;
        }

        .nota-card ul {
            padding-left: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }

        table, th, td {
            border: 1px solid var(--border);
        }

        th, td {
            padding: 12px;
            text-align: left;
        }

        th {
            background-color: rgba(139, 92, 246, 0.1);
            color: #6d28d9;
        }

        .hidden {
            display: none !important;
        }

        /* Quiz Styles */
        .quiz-card {
            background: var(--bg-card);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 32px 24px;
            text-align: center;
            border: 2px solid var(--border);
            max-width: 600px;
            margin: 0 auto;
        }

        .quiz-question {
            font-size: 22px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 24px;
        }

        .quiz-options {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }

        .quiz-option {
            padding: 16px;
            border: 2px solid var(--border);
            border-radius: var(--radius-sm);
            background: var(--bg-main);
            font-family: 'Lexend', sans-serif;
            font-size: 18px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition);
        }

        .quiz-option:hover:not(.disabled) {
            border-color: #8b5cf6;
            transform: scale(1.02);
        }

        .quiz-option.correct {
            border-color: var(--correct);
            background: var(--correct-bg);
        }

        .quiz-option.wrong {
            border-color: var(--wrong);
            background: var(--wrong-bg);
        }

        .quiz-option.disabled {
            cursor: default;
            opacity: 0.7;
        }

        .quiz-next-btn {
            margin-top: 20px;
            padding: 14px 40px;
            background: linear-gradient(135deg, #8b5cf6, #6d28d9);
            color: white;
            border: none;
            border-radius: 50px;
            font-family: 'Lexend', sans-serif;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            display: none;
        }

        .quiz-next-btn.show { display: inline-block; }
    </style>
</head>
<body>
    <header class="app-header">
        <a href="index.html" class="btn-home-header">🏠 Menu Utama</a>
        <span class="version-badge">v1.5.0</span>
        <h1>🕋 Bijak KAFA — Tauhid Darjah 2</h1>
        <div class="subtitle">Nota Lengkap & Kuiz Mengikut Silibus JAIS</div>
    </header>

    <div style="background: var(--bg-tabs); position: sticky; top: 0; z-index: 100;">
        <nav class="mode-tabs">
            <button class="mode-tab active" data-mode="browse" id="tab-browse">📖 Nota Lengkap</button>
            <button class="mode-tab" data-mode="quiz" id="tab-quiz">🧠 Kuiz</button>
        </nav>
    </div>

    <div class="topic-filters" id="topic-filters">
        <button class="topic-pill active" data-topic="sifat">✨ Sifat Allah</button>
        <button class="topic-pill" data-topic="malaikat">👼 Malaikat</button>
        <button class="topic-pill" data-topic="kitab">📖 Kitab</button>
    </div>

    <main class="content-area">
        <div id="browse-view">
            <!-- Nota Content Injected by JS -->
        </div>

        <div id="quiz-view" class="hidden">
            <div id="quiz-container">
                <!-- Quiz Injected by JS -->
            </div>
        </div>
    </main>

    <script>
        const notaData = {
            sifat: `
                <div class="nota-card">
                    <h2>Pelajaran 1: Sifat-Sifat Allah SWT (Wajib dan Mustahil)</h2>
                    <p>Mengenali sifat Allah adalah asas dalam memantapkan akidah. Allah mempunyai sifat-sifat yang wajib bagi-Nya dan mustahil bagi-Nya mempunyai sifat lawan kepada sifat wajib tersebut.</p>
                    
                    <h3>1. Sifat Qidam (قِدَم)</h3>
                    <ul>
                        <li><strong>Maksud:</strong> Sedia ada. Allah SWT sedia ada dan tiada permulaan bagi adanya.</li>
                        <li><strong>Sifat Lawan:</strong> Hudus (حُدُوث) yang bermaksud baharu (ada permulaan).</li>
                        <li><strong>Hukum:</strong> Wajib bagi Allah bersifat Qidam dan mustahil bagi Allah bersifat baharu.</li>
                        <li><strong>Dalil Naqli:</strong> Firman Allah SWT dalam Surah Al-Hadid, ayat 3.</li>
                        <li><strong>Faedah Mengenal Sifat Qidam:</strong>
                            <ol>
                                <li>Iman akan menjadi semakin kukuh.</li>
                                <li>Sentiasa taat kepada perintah Allah SWT.</li>
                                <li>Sentiasa berakhlak mulia dalam kehidupan.</li>
                            </ol>
                        </li>
                    </ul>

                    <h3>2. Sifat Baqa' (بَقَاء)</h3>
                    <ul>
                        <li><strong>Maksud:</strong> Kekal. Allah SWT tetap ada dan tidak akan binasa atau berakhir.</li>
                        <li><strong>Sifat Lawan:</strong> Fanaa (فَنَاء) yang bermaksud binasa.</li>
                        <li><strong>Dalil Naqli:</strong> Surah Ar-Rahman, ayat 26-27 yang menerangkan bahawa segala yang ada di bumi akan binasa, manakala Zat Tuhan yang mempunyai Kebesaran dan Kemuliaan akan tetap kekal.</li>
                        <li><strong>Faedah Mengenal Sifat Baqa':</strong>
                            <ol>
                                <li>Mengakui kebesaran dan kekuasaan Allah SWT.</li>
                                <li>Sentiasa mengingati mati dan melakukan persiapan akhirat.</li>
                            </ol>
                        </li>
                    </ul>

                    <h3>3. Sifat Mukhalafatuhu Lilhawadisi (مُخَالَفَتُهُ لِلْحَوَادِثِ)</h3>
                    <ul>
                        <li><strong>Maksud:</strong> Bersalahan Allah SWT dengan segala yang baharu (makhluk). Allah tidak serupa dengan apa yang dicipta-Nya.</li>
                        <li><strong>Sifat Lawan:</strong> Mumathalatuhu Lilhawadisi (مُمَاثَلَتُهُ لِلْحَوَادِثِ) yang bermaksud persamaan Allah dengan makhluk.</li>
                        <li><strong>Hukum:</strong> Wajib bagi Allah bersifat berbeza dengan makhluk dan mustahil Allah menyerupai makhluk.</li>
                    </ul>

                    <h3>4. Sifat Qiyamuhu Binafsihi (قِيَامُهُ بِنَفْسِهِ)</h3>
                    <ul>
                        <li><strong>Maksud:</strong> Allah SWT berdiri dengan sendiri-Nya tanpa memerlukan bantuan atau tempat daripada yang lain.</li>
                        <li><strong>Sifat Lawan:</strong> Ihtiyajuhu Lighairihi (إِحْتِيَاجُهُ لِغَيْرِهِ) yang bermaksud Allah memerlukan bantuan yang lain.</li>
                    </ul>

                    <h3>5. Sifat Wahdaniyyah (وَحْدَانِيَّة)</h3>
                    <ul>
                        <li><strong>Maksud:</strong> Tunggal atau Esa. Allah SWT itu satu pada zat, sifat, dan perbuatan-Nya.</li>
                        <li><strong>Sifat Lawan:</strong> Ta'addud (تَعَدُّد) yang bermaksud berbilang-bilang.</li>
                        <li><strong>Faedah Mengenal Sifat Wahdaniyyah:</strong>
                            <ol>
                                <li>Tidak menyembah tuhan selain daripada Allah SWT.</li>
                                <li>Ketaatan kepada perintah Allah menjadi lebih mantap.</li>
                                <li>Iman bertambah kukuh dan teguh.</li>
                            </ol>
                        </li>
                    </ul>
                </div>
            `,
            malaikat: `
                <div class="nota-card">
                    <h2>Pelajaran 2: Beriman kepada Malaikat</h2>
                    <p>Beriman kepada Malaikat merupakan rukun iman yang kedua. Pelajar perlu memahami sifat dan tugas makhluk Allah yang mulia ini.</p>
                    
                    <h3>Pengertian dan Hukum</h3>
                    <ul>
                        <li><strong>Pengertian:</strong> Malaikat adalah makhluk Allah SWT yang diciptakan daripada cahaya (nur). Mereka tidak mempunyai jantina (lelaki atau perempuan), tidak makan, tidak minum, dan tidak tidur.</li>
                        <li><strong>Hukum:</strong> Wajib bagi setiap umat Islam beriman kepada Malaikat.</li>
                    </ul>

                    <h3>Senarai 10 Malaikat dan Tugasnya</h3>
                    <table>
                        <tr><th>Bil</th><th>Nama Malaikat</th><th>Tugas Utama</th></tr>
                        <tr><td>1</td><td>Jibril</td><td>Menyampaikan wahyu kepada para Nabi dan Rasul.</td></tr>
                        <tr><td>2</td><td>Mikail</td><td>Menguruskan rezeki dan menurunkan hujan.</td></tr>
                        <tr><td>3</td><td>Israfil</td><td>Meniup sangkakala apabila tiba hari kiamat.</td></tr>
                        <tr><td>4</td><td>Izrail</td><td>Mencabut nyawa setiap makhluk yang bernyawa.</td></tr>
                        <tr><td>5</td><td>Raqib</td><td>Mencatat segala amalan baik manusia.</td></tr>
                        <tr><td>6</td><td>Atid</td><td>Mencatat segala amalan buruk manusia.</td></tr>
                        <tr><td>7</td><td>Munkar</td><td>Menyoal orang mati di dalam kubur.</td></tr>
                        <tr><td>8</td><td>Nakir</td><td>Menyoal orang mati di dalam kubur.</td></tr>
                        <tr><td>9</td><td>Ridzwan</td><td>Menjaga pintu syurga.</td></tr>
                        <tr><td>10</td><td>Malik</td><td>Menjaga pintu neraka.</td></tr>
                    </table>

                    <h3>Perbandingan Sifat Malaikat dan Manusia</h3>
                    <table>
                        <tr><th>Perkara</th><th>Malaikat</th><th>Manusia</th></tr>
                        <tr><td>Asal Kejadian</td><td>Dicipta daripada cahaya (nur).</td><td>Dicipta daripada tanah dan air mani.</td></tr>
                        <tr><td>Sifat Fizikal</td><td>Tidak berjantina.</td><td>Berjantina (lelaki dan perempuan).</td></tr>
                        <tr><td>Keperluan Asas</td><td>Tidak makan, tidak minum, tidak tidur.</td><td>Perlu makan, minum, dan tidur.</td></tr>
                        <tr><td>Ketaatan</td><td>Sentiasa taat dan patuh.</td><td>Ada yang taat dan ada yang ingkar.</td></tr>
                    </table>
                </div>
            `,
            kitab: `
                <div class="nota-card">
                    <h2>Pelajaran 3: Beriman kepada Kitab</h2>
                    <p>Beriman kepada kitab-kitab Allah merupakan rukun iman yang ketiga. Allah SWT menurunkan kitab-kitab sebagai panduan hidup kepada manusia melalui para Rasul.</p>
                    
                    <h3>Pengertian dan Hukum</h3>
                    <ul>
                        <li><strong>Pengertian:</strong> Kitab-kitab Allah merupakan kalam Allah (kata-kata Allah) yang diwahyukan kepada para Rasul untuk disampaikan kepada umat manusia.</li>
                        <li><strong>Hukum:</strong> Wajib dipercayai bahawa Allah telah menurunkan kitab-kitab suci kepada para Rasul tertentu.</li>
                    </ul>

                    <h3>Senarai 4 Kitab Suci dan Rasul Penerimanya</h3>
                    <table>
                        <tr><th>Bil</th><th>Nama Kitab</th><th>Rasul yang Menerimanya</th></tr>
                        <tr><td>1</td><td>Taurat</td><td>Nabi Musa AS</td></tr>
                        <tr><td>2</td><td>Zabur</td><td>Nabi Daud AS</td></tr>
                        <tr><td>3</td><td>Injil</td><td>Nabi Isa AS</td></tr>
                        <tr><td>4</td><td>Al-Quran</td><td>Nabi Muhammad SAW</td></tr>
                    </table>

                    <h3>Nota Tambahan:</h3>
                    <ul>
                        <li>Al-Quran adalah kitab terakhir yang diturunkan oleh Allah SWT dan ia merupakan pelengkap serta penyempurna kepada kitab-kitab sebelumnya.</li>
                        <li>Membaca dan memahami isi kandungan Al-Quran adalah dituntut dalam Islam sebagai panduan kehidupan seharian.</li>
                    </ul>
                </div>
            `
        };

        const quizData = {
            sifat: [
                { q: "Apakah maksud sifat Qidam?", options: ["Sedia ada", "Baharu", "Kekal"], answer: 0 },
                { q: "Apakah sifat lawan bagi Baqa'?", options: ["Hudus", "Fanaa", "Ta'addud"], answer: 1 },
                { q: "Wahdaniyyah bermaksud?", options: ["Esa / Tunggal", "Berbilang-bilang", "Kekal"], answer: 0 }
            ],
            malaikat: [
                { q: "Malaikat diciptakan daripada apa?", options: ["Api", "Tanah", "Cahaya (Nur)"], answer: 2 },
                { q: "Siapakah malaikat yang bertugas mencabut nyawa?", options: ["Jibril", "Izrail", "Mikail"], answer: 1 },
                { q: "Malaikat Munkar dan Nakir bertugas untuk?", options: ["Menjaga pintu syurga", "Menyoal orang mati dalam kubur", "Mencatat amalan"], answer: 1 }
            ],
            kitab: [
                { q: "Kitab Taurat diturunkan kepada nabi?", options: ["Nabi Musa AS", "Nabi Daud AS", "Nabi Isa AS"], answer: 0 },
                { q: "Kitab apakah yang diturunkan kepada Nabi Muhammad SAW?", options: ["Zabur", "Injil", "Al-Quran"], answer: 2 }
            ]
        };

        // UI State
        let currentMode = 'browse';
        let currentTopic = 'sifat';
        let currentQuizIndex = 0;
        let score = 0;

        // Elements
        const browseView = document.getElementById('browse-view');
        const quizView = document.getElementById('quiz-view');
        const quizContainer = document.getElementById('quiz-container');
        
        // Tab Switching
        document.getElementById('tab-browse').addEventListener('click', () => setMode('browse'));
        document.getElementById('tab-quiz').addEventListener('click', () => setMode('quiz'));

        // Topic Switching
        document.querySelectorAll('.topic-pill').forEach(pill => {
            pill.addEventListener('click', (e) => {
                document.querySelectorAll('.topic-pill').forEach(p => p.classList.remove('active'));
                e.target.classList.add('active');
                currentTopic = e.target.getAttribute('data-topic');
                renderContent();
            });
        });

        function setMode(mode) {
            currentMode = mode;
            document.getElementById('tab-browse').classList.toggle('active', mode === 'browse');
            document.getElementById('tab-quiz').classList.toggle('active', mode === 'quiz');
            
            if (mode === 'browse') {
                browseView.classList.remove('hidden');
                quizView.classList.add('hidden');
            } else {
                browseView.classList.add('hidden');
                quizView.classList.remove('hidden');
                startQuiz();
            }
            renderContent();
        }

        function renderContent() {
            if (currentMode === 'browse') {
                browseView.innerHTML = notaData[currentTopic];
            }
        }

        function startQuiz() {
            currentQuizIndex = 0;
            score = 0;
            renderQuizQuestion();
        }

        function renderQuizQuestion() {
            const questions = quizData[currentTopic];
            if (currentQuizIndex >= questions.length) {
                // Quiz complete
                quizContainer.innerHTML = \`
                    <div class="quiz-card">
                        <h2>Kuiz Tamat!</h2>
                        <div style="font-size: 48px; color: #8b5cf6; font-weight: bold;">\${score} / \${questions.length}</div>
                        <button class="quiz-next-btn show" onclick="startQuiz()" style="margin-top: 20px;">Cuba Lagi</button>
                    </div>
                \`;
                return;
            }

            const q = questions[currentQuizIndex];
            let optionsHtml = '';
            q.options.forEach((opt, idx) => {
                optionsHtml += \`<div class="quiz-option" onclick="selectAnswer(\${idx}, \${q.answer})">\${opt}</div>\`;
            });

            quizContainer.innerHTML = \`
                <div class="quiz-card">
                    <div style="text-align: left; color: #718096; margin-bottom: 10px;">Soalan \${currentQuizIndex + 1} daripada \${questions.length}</div>
                    <div class="quiz-question">\${q.q}</div>
                    <div class="quiz-options">
                        \${optionsHtml}
                    </div>
                    <button class="quiz-next-btn" id="next-btn" onclick="nextQuestion()">Seterusnya ➡️</button>
                </div>
            \`;
        }

        window.selectAnswer = function(selectedIdx, correctIdx) {
            const options = document.querySelectorAll('.quiz-option');
            if (options[0].classList.contains('disabled')) return; // already answered

            options.forEach((opt, idx) => {
                opt.classList.add('disabled');
                if (idx === correctIdx) {
                    opt.classList.add('correct');
                } else if (idx === selectedIdx && selectedIdx !== correctIdx) {
                    opt.classList.add('wrong');
                }
            });

            if (selectedIdx === correctIdx) {
                score++;
            }

            document.getElementById('next-btn').classList.add('show');
        }

        window.nextQuestion = function() {
            currentQuizIndex++;
            renderQuizQuestion();
        }

        // Initialize
        renderContent();
    </script>
</body>
</html>
"""

with open('/Users/re1/Documents/antigravity/modest-bohr/tauhid.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

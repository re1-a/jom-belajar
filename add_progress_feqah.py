import re

file_path = "/Users/re1/Documents/antigravity/modest-bohr/feqah.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add CSS
css_addition = """
        /* Progress Styles */
        .progress-container {
            max-width: 600px;
            margin: 0 auto;
        }
        .progress-card {
            background: var(--bg-card);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .progress-info {
            flex: 1;
            margin-right: 20px;
        }
        .progress-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 8px;
            text-transform: capitalize;
        }
        .progress-bar-track {
            background: #EDF2F7;
            border-radius: 10px;
            height: 12px;
            width: 100%;
            overflow: hidden;
        }
        [data-theme="dark"] .progress-bar-track {
            background: #4A5568;
        }
        .progress-bar-value {
            height: 100%;
            background: linear-gradient(135deg, #059669, #047857);
            border-radius: 10px;
            transition: width 0.8s ease;
        }
        .progress-stats {
            font-size: 20px;
            font-weight: 700;
            color: #059669;
            min-width: 80px;
            text-align: right;
        }
        .progress-total {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: var(--bg-card);
            border-radius: var(--radius);
            border: 2px solid var(--border);
        }
        .progress-total h3 {
            margin: 0 0 10px 0;
            color: var(--text-secondary);
        }
        .progress-total .big-score {
            font-size: 48px;
            font-weight: 800;
            color: #059669;
        }
        .reset-btn {
            display: block;
            width: 100%;
            padding: 14px;
            margin-top: 20px;
            background: transparent;
            color: #E53E3E;
            border: 2px solid #E53E3E;
            border-radius: 50px;
            font-family: 'Lexend', sans-serif;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        .reset-btn:hover {
            background: #E53E3E;
            color: white;
        }
    </style>"""
content = content.replace("    </style>", css_addition)

# 2. HTML tab
tab_old = '<button class="mode-tab" data-mode="quiz" id="tab-quiz">Kuiz</button>'
tab_new = '<button class="mode-tab" data-mode="quiz" id="tab-quiz">Kuiz</button>\n            <button class="mode-tab" data-mode="progress" id="tab-progress">📊 Progress</button>'
content = content.replace(tab_old, tab_new)

# 3. HTML View
view_old = """        <div id="quiz-view" class="hidden">
            <div id="quiz-container">
                <!-- Quiz Injected by JS -->
            </div>
        </div>"""
view_new = """        <div id="quiz-view" class="hidden">
            <div id="quiz-container">
                <!-- Quiz Injected by JS -->
            </div>
        </div>

        <div id="progress-view" class="hidden">
            <!-- Progress Injected by JS -->
        </div>"""
content = content.replace(view_old, view_new)

# 4. JS state and elements
js_state_old = """        let currentMode = 'browse';
        let currentTopic = 'istinjak';
        let currentQuizIndex = 0;
        let score = 0;

        // Elements
        const browseView = document.getElementById('browse-view');
        const quizView = document.getElementById('quiz-view');
        const quizContainer = document.getElementById('quiz-container');"""

js_state_new = """        let currentMode = 'browse';
        let currentTopic = 'istinjak';
        let currentQuizIndex = 0;
        let score = 0;
        
        let quizState = { topicScores: {} };

        // Elements
        const browseView = document.getElementById('browse-view');
        const quizView = document.getElementById('quiz-view');
        const progressView = document.getElementById('progress-view');
        const quizContainer = document.getElementById('quiz-container');"""
content = content.replace(js_state_old, js_state_new)

# 5. Tab logic
tab_logic_old = """        // Tab Switching
        document.getElementById('tab-browse').addEventListener('click', () => setMode('browse'));
        document.getElementById('tab-quiz').addEventListener('click', () => setMode('quiz'));

        // Topic Switching"""
tab_logic_new = """        // Tab Switching
        document.getElementById('tab-browse').addEventListener('click', () => setMode('browse'));
        document.getElementById('tab-quiz').addEventListener('click', () => setMode('quiz'));
        document.getElementById('tab-progress').addEventListener('click', () => setMode('progress'));

        // Topic Switching"""
content = content.replace(tab_logic_old, tab_logic_new)

# 6. setMode logic
setMode_old = """        function setMode(mode) {
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
        }"""
setMode_new = """        function setMode(mode) {
            currentMode = mode;
            document.getElementById('tab-browse').classList.toggle('active', mode === 'browse');
            document.getElementById('tab-quiz').classList.toggle('active', mode === 'quiz');
            document.getElementById('tab-progress').classList.toggle('active', mode === 'progress');
            
            browseView.classList.add('hidden');
            quizView.classList.add('hidden');
            progressView.classList.add('hidden');
            
            if (mode === 'browse') {
                browseView.classList.remove('hidden');
                document.getElementById('topic-filters').classList.remove('hidden');
            } else if (mode === 'quiz') {
                quizView.classList.remove('hidden');
                document.getElementById('topic-filters').classList.remove('hidden');
                startQuiz();
            } else if (mode === 'progress') {
                progressView.classList.remove('hidden');
                document.getElementById('topic-filters').classList.add('hidden');
                renderProgressView();
            }
            renderContent();
        }"""
content = content.replace(setMode_old, setMode_new)

# 7. selectAnswer progress tracking
select_old = """            if (selectedIdx === correctIdx) {
                score++;
            } else {
                if (q.explanation) {
                    const explBox = document.getElementById('explanation-box');
                    explBox.style.display = 'block';
                    explBox.innerHTML = '<strong>💡 Tahukah anda?</strong><br>' + q.explanation;
                }
            }

            document.getElementById('next-btn').classList.add('show');"""
select_new = """            if (!quizState.topicScores[currentTopic]) {
                quizState.topicScores[currentTopic] = { correct: 0, total: 0 };
            }
            quizState.topicScores[currentTopic].total++;

            if (selectedIdx === correctIdx) {
                score++;
                quizState.topicScores[currentTopic].correct++;
            } else {
                if (q.explanation) {
                    const explBox = document.getElementById('explanation-box');
                    explBox.style.display = 'block';
                    explBox.innerHTML = '<strong>💡 Tahukah anda?</strong><br>' + q.explanation;
                }
            }

            saveProgress();
            document.getElementById('next-btn').classList.add('show');"""
content = content.replace(select_old, select_new)

# 8. Progress logic functions
init_old = """        // Initialize
        renderContent();"""
init_new = """        function loadProgress() {
            const saved = localStorage.getItem('kafa_feqah_progress');
            if (saved) {
                try {
                    quizState.topicScores = JSON.parse(saved);
                } catch(e) {}
            }
        }

        function saveProgress() {
            localStorage.setItem('kafa_feqah_progress', JSON.stringify(quizState.topicScores));
        }

        function renderProgressView() {
            loadProgress();
            const scores = quizState.topicScores;
            const topics = ['istinjak', 'wuduk', 'najis', 'hadas', 'mandiwajib', 'mandisunat'];
            const topicNames = {
                'istinjak': 'Istinjak',
                'wuduk': 'Wuduk',
                'najis': 'Najis',
                'hadas': 'Hadas',
                'mandiwajib': 'Mandi Wajib',
                'mandisunat': 'Mandi Sunat'
            };

            let totalCorrect = 0;
            let totalAttempted = 0;
            let html = '<div class="progress-container">';

            let cardsHtml = '';
            topics.forEach(t => {
                const s = scores[t] || { correct: 0, total: 0 };
                totalCorrect += s.correct;
                totalAttempted += s.total;
                
                let pct = 0;
                if (s.total > 0) pct = Math.round((s.correct / s.total) * 100);
                
                cardsHtml += `
                    <div class="progress-card">
                        <div class="progress-info">
                            <div class="progress-title">${topicNames[t]}</div>
                            <div class="progress-bar-track">
                                <div class="progress-bar-value" style="width: ${pct}%;"></div>
                            </div>
                        </div>
                        <div class="progress-stats">${pct}%</div>
                    </div>
                `;
            });

            let overallPct = 0;
            if (totalAttempted > 0) overallPct = Math.round((totalCorrect / totalAttempted) * 100);

            html += `
                <div class="progress-total">
                    <h3>Pencapaian Keseluruhan</h3>
                    <div class="big-score">${overallPct}%</div>
                    <div style="color: var(--text-light); font-size: 14px;">${totalCorrect} betul daripada ${totalAttempted} cubaan</div>
                </div>
            `;
            
            html += cardsHtml;
            
            if (totalAttempted > 0) {
                html += `<button class="reset-btn" onclick="resetProgress()">Set Semula Rekod</button>`;
            } else {
                html += `<div style="text-align:center; color:var(--text-light); margin-top:20px;">Belum ada sebarang rekod kuiz dijawab.</div>`;
            }

            html += '</div>';
            progressView.innerHTML = html;
        }

        window.resetProgress = function() {
            if(confirm('Anda pasti mahu memadam semua rekod pencapaian Feqah?')) {
                localStorage.removeItem('kafa_feqah_progress');
                quizState.topicScores = {};
                renderProgressView();
            }
        }

        // Initialize
        loadProgress();
        renderContent();"""
content = content.replace(init_old, init_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Progress tracker injected.")

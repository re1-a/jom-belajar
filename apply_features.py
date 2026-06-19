import os
import re

files_to_process = ['index.html', 'Nota_KAFA_Aqil.html']

for filepath in files_to_process:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Chart.js to HEAD
    if '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>' not in content:
        content = content.replace('</head>', '    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n</head>')

    # 2. Add "Laporan Prestasi" button to Header
    if 'id="btn-dashboard"' not in content:
        # Insert button inside .app-header
        header_btn = '''
        <div style="position: absolute; top: 15px; right: 15px;">
            <button id="btn-dashboard" class="nav-btn" onclick="openDashboard()" style="padding: 8px 15px; font-size: 14px; background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.5);">📊 Laporan Prestasi</button>
        </div>'''
        content = content.replace('<div class="app-header">', f'<div class="app-header">{header_btn}')

    # 3. Add module-status to Topic Pills
    if 'class="module-status"' not in content:
        # Regex to find <button class="topic-pill"...>Text</button>
        # We want to change it to <button class="topic-pill"...>Text <div class="module-status"></div></button>
        # And we need to make .topic-pill flex column
        content = re.sub(r'(<button class="topic-pill"[^>]*>)([^<]*)(</button>)', r'\1<span>\2</span><div class="module-status module-status-\2"></div>\3', content)
        # Fix the data-topic matching for the status divs to have an ID or class matching the topic
        content = re.sub(r'<button class="topic-pill(?: active)?" data-topic="([^"]+)"><span>([^<]*)</span><div class="module-status module-status-[^"]+"></div></button>', 
                         r'<button class="topic-pill" data-topic="\1" style="display:flex;flex-direction:column;align-items:center;gap:4px;"><span>\2</span><div class="module-status" id="status-\1"></div></button>', content)

    # 4. Add Quiz Counter
    if 'id="quiz-counter"' not in content:
        quiz_counter_html = '<div id="quiz-counter" style="text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 20px;">Soalan: 0/15</div>'
        content = content.replace('<div id="quiz-question" class="quiz-question"></div>', f'{quiz_counter_html}\n            <div id="quiz-question" class="quiz-question"></div>')

    # 5. Add Modals HTML
    if 'id="dashboard-modal"' not in content:
        modals_html = '''
    <!-- ============================================
         MODALS
         ============================================ -->
    <!-- Quiz Summary Modal -->
    <div id="quiz-summary-modal" class="modal hidden">
        <div class="modal-content text-center">
            <h2>🎉 Sesi Selesai!</h2>
            <div class="score-display">Markah Anda: <span id="summary-score">0/15</span></div>
            <div class="score-percent" id="summary-percent">0%</div>
            <button class="nav-btn" onclick="closeQuizSummary()">Kembali ke Menu Utama</button>
        </div>
    </div>

    <!-- Dashboard Modal -->
    <div id="dashboard-modal" class="modal hidden">
        <div class="modal-content" style="max-width: 800px; width: 95%;">
            <span class="close-btn" onclick="closeDashboard()">&times;</span>
            <h2>📊 Laporan Prestasi (Ibu Bapa)</h2>
            <div class="dashboard-tabs">
                <button class="dash-tab active" id="tab-dash-chart" onclick="switchDashTab('chart')">📈 Graf Ketepatan</button>
                <button class="dash-tab" id="tab-dash-history" onclick="switchDashTab('history')">📜 Sejarah Rekod</button>
            </div>
            
            <div id="dash-chart-view">
                <div style="margin: 15px 0;">
                    <label for="chart-filter"><strong>Penapis Modul: </strong></label>
                    <select id="chart-filter" onchange="renderChart()" style="padding: 5px; border-radius: 5px;">
                        <option value="all">Semua Topik</option>
                        <option value="nombor">Nombor</option>
                        <option value="warna">Warna</option>
                        <option value="haiwan">Haiwan</option>
                        <option value="sukan">Sukan</option>
                        <option value="pakaian">Pakaian</option>
                        <option value="sayur">Sayur</option>
                        <option value="buah">Buah</option>
                        <option value="makanan">Makanan</option>
                    </select>
                </div>
                <canvas id="performanceChart"></canvas>
            </div>

            <div id="dash-history-view" class="hidden">
                <div class="table-container">
                    <table id="historyTable" class="history-table">
                        <thead>
                            <tr>
                                <th>Tarikh</th>
                                <th>Modul</th>
                                <th>Markah</th>
                                <th>Peratus</th>
                            </tr>
                        </thead>
                        <tbody id="history-tbody"></tbody>
                    </table>
                </div>
                <button class="nav-btn" style="background: var(--wrong); margin-top: 15px;" onclick="clearHistory()">🗑️ Padam Semua Rekod</button>
            </div>
        </div>
    </div>
'''
        content = content.replace('</body>', modals_html + '\n</body>')

    # 6. Add CSS
    if '/* Modals and Dashboard */' not in content:
        css = '''
        /* Modals and Dashboard */
        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; }
        .modal-content { background: var(--bg-card); padding: 30px; border-radius: var(--radius); width: 90%; max-width: 500px; max-height: 90vh; overflow-y: auto; position: relative; }
        .close-btn { position: absolute; top: 15px; right: 20px; font-size: 28px; cursor: pointer; color: var(--text-secondary); }
        .score-display { font-size: 24px; font-weight: bold; margin: 20px 0; color: var(--text-primary); }
        .score-percent { font-size: 48px; font-weight: bold; color: var(--correct); margin-bottom: 30px; }
        .dashboard-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid var(--border); padding-bottom: 10px; }
        .dash-tab { padding: 10px 15px; border: none; background: none; font-size: 16px; font-weight: bold; color: var(--text-secondary); cursor: pointer; border-radius: var(--radius-sm); }
        .dash-tab.active { background: var(--bg-header); color: white; }
        .history-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .history-table th, .history-table td { border: 1px solid var(--border); padding: 10px; text-align: left; }
        .history-table th { background: rgba(0,0,0,0.05); }
        .table-container { overflow-x: auto; max-height: 350px; overflow-y: auto; }
        .module-status { font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 12px; display: inline-block; background: var(--bg-main); color: var(--text-light); border: 1px solid var(--border); }
        .status-green { background: #C6F6D5; color: #22543D; border-color: #9AE6B4; }
        .status-yellow { background: #FEFCBF; color: #744210; border-color: #FAF089; }
        .status-red { background: #FED7D7; color: #742A2A; border-color: #FEB2B2; }
        [data-theme="dark"] .status-green { background: rgba(72,187,120,0.2); color: #9AE6B4; border-color: rgba(72,187,120,0.5); }
        [data-theme="dark"] .status-yellow { background: rgba(236,201,75,0.2); color: #FAF089; border-color: rgba(236,201,75,0.5); }
        [data-theme="dark"] .status-red { background: rgba(245,101,101,0.2); color: #FEB2B2; border-color: rgba(245,101,101,0.5); }
        @media print { .modal, #btn-dashboard { display: none !important; } }
'''
        content = content.replace('/* ============================================', css + '\n        /* ============================================', 1)

    # 7. Modify Quiz JS Flow
    content = content.replace('quizState.questions = shuffled.slice(0, 4); // example options logic', 'quizState.questions = shuffled.slice(0, 4);')
    
    # In startQuiz:
    old_start_quiz = '''        quizState.currentIndex = 0;
        quizState.score = 0;
        quizState.answered = false;

        renderQuestion();
        document.getElementById('quiz-result').classList.add('hidden');
        document.getElementById('next-btn').classList.add('hidden');'''
    new_start_quiz = '''        // LIMIT TO 15 QUESTIONS PER SESSION
        if (quizState.questions.length > 15) {
            quizState.questions = quizState.questions.slice(0, 15);
        }
        quizState.totalQuestions = quizState.questions.length;
        quizState.currentIndex = 0;
        quizState.score = 0;
        quizState.answered = false;

        renderQuestion();
        document.getElementById('quiz-result').classList.add('hidden');
        document.getElementById('next-btn').classList.add('hidden');'''
    content = content.replace(old_start_quiz, new_start_quiz)

    # In renderQuestion:
    old_render_q = "const q = quizState.questions[quizState.currentIndex];"
    new_render_q = "const q = quizState.questions[quizState.currentIndex];\n        document.getElementById('quiz-counter').innerText = `Soalan: ${quizState.currentIndex + 1}/${quizState.totalQuestions}`;"
    if "document.getElementById('quiz-counter').innerText" not in content:
        content = content.replace(old_render_q, new_render_q)

    # In nextQuestion:
    old_next_q = '''    function nextQuestion() {
        quizState.currentIndex++;
        if (quizState.currentIndex < quizState.questions.length) {
            quizState.answered = false;
            renderQuestion();
            document.getElementById('quiz-result').classList.add('hidden');
            document.getElementById('next-btn').classList.add('hidden');
        } else {
            // Re-shuffle and start again if end reached
            startQuiz();
        }
    }'''
    new_next_q = '''    function nextQuestion() {
        quizState.currentIndex++;
        if (quizState.currentIndex < quizState.totalQuestions) {
            quizState.answered = false;
            renderQuestion();
            document.getElementById('quiz-result').classList.add('hidden');
            document.getElementById('next-btn').classList.add('hidden');
        } else {
            endQuizSession();
        }
    }'''
    content = content.replace(old_next_q, new_next_q)

    # 8. Add New JS Functions
    if 'function endQuizSession()' not in content:
        new_js = '''
    // =============================================
    // PERFORMANCE DASHBOARD & SESSION LOGIC
    // =============================================
    let chartInstance = null;

    function endQuizSession() {
        // Record session to localStorage
        const percentage = Math.round((quizState.score / quizState.totalQuestions) * 100);
        const topicName = currentTopic === 'all' ? 'Semua Topik' : VOCAB_DATA[currentTopic].title;
        
        const sessionRecord = {
            date: new Date().toISOString(),
            module: topicName,
            topicKey: currentTopic,
            correct: quizState.score,
            total: quizState.totalQuestions,
            percent: percentage
        };

        let sessions = JSON.parse(localStorage.getItem('kafa_sessions') || '[]');
        sessions.push(sessionRecord);
        localStorage.setItem('kafa_sessions', JSON.stringify(sessions));

        // Show Summary Modal
        document.getElementById('summary-score').innerText = `${quizState.score}/${quizState.totalQuestions}`;
        document.getElementById('summary-percent').innerText = `${percentage}%`;
        document.getElementById('quiz-summary-modal').classList.remove('hidden');

        updateMenuCards();
    }

    function closeQuizSummary() {
        document.getElementById('quiz-summary-modal').classList.add('hidden');
        // Go back to browse mode by clicking the tab
        document.getElementById('tab-browse').click();
    }

    function updateMenuCards() {
        const sessions = JSON.parse(localStorage.getItem('kafa_sessions') || '[]');
        
        // Find latest session per module
        const latestSessions = {};
        sessions.forEach(s => {
            // Overwrite with newer session (since array is chronological)
            latestSessions[s.topicKey] = s.percent;
        });

        // Update each status badge
        document.querySelectorAll('.topic-pill').forEach(btn => {
            const topicKey = btn.dataset.topic;
            const badge = btn.querySelector('.module-status');
            if (!badge) return;

            // Reset classes
            badge.className = 'module-status';

            if (latestSessions.hasOwnProperty(topicKey)) {
                const p = latestSessions[topicKey];
                badge.innerText = `Terakhir: ${p}%`;
                if (p >= 80) badge.classList.add('status-green');
                else if (p >= 50) badge.classList.add('status-yellow');
                else badge.classList.add('status-red');
            } else {
                badge.innerText = `⚪ Belum Cuba`;
            }
        });
    }

    function openDashboard() {
        document.getElementById('dashboard-modal').classList.remove('hidden');
        switchDashTab('chart');
        renderHistory();
    }

    function closeDashboard() {
        document.getElementById('dashboard-modal').classList.add('hidden');
    }

    function switchDashTab(tabName) {
        document.getElementById('tab-dash-chart').classList.remove('active');
        document.getElementById('tab-dash-history').classList.remove('active');
        document.getElementById('dash-chart-view').classList.add('hidden');
        document.getElementById('dash-history-view').classList.add('hidden');

        if (tabName === 'chart') {
            document.getElementById('tab-dash-chart').classList.add('active');
            document.getElementById('dash-chart-view').classList.remove('hidden');
            renderChart();
        } else {
            document.getElementById('tab-dash-history').classList.add('active');
            document.getElementById('dash-history-view').classList.remove('hidden');
        }
    }

    function renderChart() {
        const sessions = JSON.parse(localStorage.getItem('kafa_sessions') || '[]');
        const filterVal = document.getElementById('chart-filter').value;
        
        let filtered = sessions;
        if (filterVal !== 'all') {
            filtered = sessions.filter(s => s.topicKey === filterVal);
        } else {
            // If "all" selected, maybe just show sessions where topicKey === 'all'
            // or show literally everything. The requirement says filter by module.
            filtered = sessions.filter(s => s.topicKey === 'all');
        }

        // Prepare data for Chart.js
        const labels = filtered.map((s, idx) => `Sesi ${idx + 1}`);
        const dataPoints = filtered.map(s => s.percent);

        const ctx = document.getElementById('performanceChart').getContext('2d');
        
        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ketepatan Markah (%)',
                    data: dataPoints,
                    borderColor: '#667EEA',
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    function renderHistory() {
        const sessions = JSON.parse(localStorage.getItem('kafa_sessions') || '[]');
        const tbody = document.getElementById('history-tbody');
        tbody.innerHTML = '';

        // Reverse to show newest first
        [...sessions].reverse().forEach(s => {
            const dateObj = new Date(s.date);
            const dateStr = dateObj.toLocaleDateString('ms-MY') + ' ' + dateObj.toLocaleTimeString('ms-MY', {hour: '2-digit', minute:'2-digit'});
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${dateStr}</td>
                <td>${s.module}</td>
                <td>${s.correct}/${s.total}</td>
                <td>${s.percent}%</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function clearHistory() {
        if (confirm("Adakah anda pasti mahu memadam SEMUA rekod prestasi?")) {
            localStorage.removeItem('kafa_sessions');
            renderHistory();
            renderChart();
            updateMenuCards();
        }
    }
'''
        # Inject new JS before `initModeTabs`
        content = content.replace('function initModeTabs() {', new_js + '\n    function initModeTabs() {')
        
    # Call updateMenuCards() inside DOMContentLoaded
    if 'updateMenuCards();' not in content and 'document.addEventListener(\'DOMContentLoaded\', () => {' in content:
        content = content.replace('renderBrowseView();', 'renderBrowseView();\n        updateMenuCards();')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Features applied successfully!")

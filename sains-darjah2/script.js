// ==========================================
// STATE MANAGEMENT & CONFIGURATION
// ==========================================
let currentScore = 0;
let currentGame = '';
let currentAnswer = null; // Can be string, or array (for drag/drop)
let currentExplanation = '';
let canProceed = false;
let currentQuestionIndex = 0;
let maxQuestions = 10;
let sessionCorrect = 0;

// Data persistence
let sainsHistory = JSON.parse(localStorage.getItem('sains_history') || '[]');
let isDarkMode = localStorage.getItem('sains_theme') === 'dark';

// Audio elements
const audioCorrect = document.getElementById('audio-correct');
const audioWrong = document.getElementById('audio-wrong');
const audioComplete = document.getElementById('audio-complete');

// Game Titles Mapping
const gameTitles = {
    'unit1': 'Unit 1: Kemahiran Saintifik',
    'unit2': 'Unit 2: Peraturan Bilik Sains',
    'unit3': 'Unit 3: Manusia',
    'unit4': 'Unit 4: Haiwan',
    'unit5': 'Unit 5: Tumbuh-tumbuhan',
    'unit6': 'Unit 6: Terang dan Gelap',
    'unit7': 'Unit 7: Elektrik',
    'unit8': 'Unit 8: Campuran',
    'unit9': 'Unit 9: Bumi',
    'unit10': 'Unit 10: Teknologi'
};

// Menu generation (Cards)
const kemahiranModules = ['unit1', 'unit2'];
const penerokaanModules = ['unit3', 'unit4', 'unit5', 'unit6', 'unit7', 'unit8', 'unit9', 'unit10'];

const moduleIcons = {
    'unit1': 'fa-search', 'unit2': 'fa-shield-alt', 'unit3': 'fa-child',
    'unit4': 'fa-paw', 'unit5': 'fa-leaf', 'unit6': 'fa-lightbulb',
    'unit7': 'fa-bolt', 'unit8': 'fa-blender', 'unit9': 'fa-earth-asia', 'unit10': 'fa-robot'
};

const moduleDesc = {
    'unit1': 'Kemahiran Saintifik', 'unit2': 'Peraturan Bilik Sains',
    'unit3': 'Manusia', 'unit4': 'Haiwan',
    'unit5': 'Tumbuh-tumbuhan', 'unit6': 'Terang dan Gelap',
    'unit7': 'Elektrik', 'unit8': 'Campuran',
    'unit9': 'Bumi', 'unit10': 'Teknologi'
};

// ==========================================
// INITIALIZATION
// ==========================================
window.onload = () => {
    initTheme();
    document.body.setAttribute('data-mode', currentMode);
    updateMenuCards();
};

let currentMode = 'nota'; // 'nota' or 'kuiz'

function switchMode(mode) {
    currentMode = mode;
    document.body.setAttribute('data-mode', mode);
    document.getElementById('tab-nota').classList.toggle('active', mode === 'nota');
    document.getElementById('tab-kuiz').classList.toggle('active', mode === 'kuiz');
}

function initTheme() {
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.getElementById('theme-toggle').innerHTML = '<i class="fas fa-sun"></i>';
    }
}

function toggleDarkMode() {
    isDarkMode = !isDarkMode;
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.getElementById('theme-toggle').innerHTML = '<i class="fas fa-sun"></i>';
        localStorage.setItem('sains_theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        document.getElementById('theme-toggle').innerHTML = '<i class="fas fa-moon"></i>';
        localStorage.setItem('sains_theme', 'light');
    }
    // Update charts if dashboard is open
    if(window.dailyChart) window.dailyChart.update();
    if(window.moduleChart) window.moduleChart.update();
}

function updateMenuCards() {
    const gridKemahiran = document.getElementById('grid-kemahiran');
    const gridPenerokaan = document.getElementById('grid-penerokaan');
    gridKemahiran.innerHTML = '';
    gridPenerokaan.innerHTML = '';

    const buildCard = (mod) => {
        const stats = getModuleStats(mod);
        let badgeClass = 'badge-none';
        let badgeText = 'Belum Cuba';
        
        if (stats.attempts > 0) {
            if (stats.accuracy >= 80) { badgeClass = 'badge-good'; badgeText = 'Sangat Baik 🟢'; }
            else if (stats.accuracy >= 50) { badgeClass = 'badge-ok'; badgeText = 'Sederhana 🟡'; }
            else { badgeClass = 'badge-bad'; badgeText = 'Perlu Latihan 🔴'; }
        }

        return `
            <div class="menu-card" onclick="handleCardClick('${mod}')">
                <div class="icon-wrap" style="font-size: 2rem; margin: 0 auto 15px auto; width: 60px; height: 60px;">
                    <i class="fas ${moduleIcons[mod]}"></i>
                </div>
                <h3>Unit ${mod.replace('unit','')}</h3>
                <p style="font-size: 0.9rem; margin-top: 5px;">${moduleDesc[mod]}</p>
                <div class="module-status">
                    <span class="status-badge ${badgeClass}">${badgeText}</span>
                </div>
            </div>
        `;
    };

    kemahiranModules.forEach(mod => gridKemahiran.innerHTML += buildCard(mod));
    penerokaanModules.forEach(mod => gridPenerokaan.innerHTML += buildCard(mod));
}

// ==========================================
// NAVIGATION & GAME FLOW
// ==========================================
function goHome() {
    document.getElementById('game-screen').classList.remove('active');
    document.getElementById('notes-screen').classList.remove('active');
    document.getElementById('main-menu').classList.add('active');
    updateMenuCards();
}

// ==========================================
// NOTES & FLASHCARDS FLOW
// ==========================================
let currentNotes = [];
let currentFlashcardIndex = 0;

function handleCardClick(gameId) {
    if (currentMode === 'nota') {
        openNotes(gameId);
    } else {
        startGame(gameId);
    }
}

function openNotes(gameId) {
    currentGame = gameId;
    // Get notes from unit data or fallback if not ready
    if(typeof unitNotesData !== 'undefined' && unitNotesData[gameId]) {
        currentNotes = unitNotesData[gameId];
    } else {
        currentNotes = [
            { frontEmoji: '🚧', frontTitle: 'Belum Tersedia', frontQuestion: 'Nota untuk unit ini sedang dibina.', backEmoji: '🛠️', backTitle: 'Sabar Ya!', backAnswer: 'Sila kembali nanti.', trivia: 'Kerja-kerja penyelenggaraan sedang berjalan!' }
        ];
    }
    
    currentFlashcardIndex = 0;
    document.getElementById('main-menu').classList.remove('active');
    document.getElementById('notes-screen').classList.add('active');
    document.getElementById('notes-title-text').innerText = 'Nota ' + gameTitles[gameId].split(':')[0];
    
    renderFlashcard();
}

function renderFlashcard() {
    const card = currentNotes[currentFlashcardIndex];
    const container = document.getElementById('flashcard-container');
    
    container.innerHTML = `
        <div class="flashcard-scene" onclick="this.querySelector('.flashcard-inner').classList.toggle('flipped')">
            <div class="flashcard-inner">
                <div class="flashcard-front">
                    ${card.image 
                        ? `<img src="${card.image}" class="flashcard-img" alt="Sains Darjah 2 Visual">` 
                        : `<div class="flashcard-emoji">${card.frontEmoji}</div>`
                    }
                    <h3 class="flashcard-title">${card.frontTitle}</h3>
                    <p class="flashcard-text">${card.frontQuestion}</p>
                    <div class="click-hint">(Klik untuk jawapan)</div>
                </div>
                <div class="flashcard-back">
                    ${card.backEmoji.includes('flashcard-bg-img') ? card.backEmoji : `<div class="flashcard-emoji">${card.backEmoji}</div>`}
                    <h3 class="flashcard-title">${card.backTitle}</h3>
                    <p class="flashcard-detail">${card.backAnswer}</p>
                    <div class="trivia-box">${card.trivia}</div>
                </div>
            </div>
        </div>
    `;
    
    // Update dots
    const dotsContainer = document.getElementById('flashcard-dots');
    dotsContainer.innerHTML = '';
    for(let i=0; i<currentNotes.length; i++) {
        dotsContainer.innerHTML += `<div class="dot ${i === currentFlashcardIndex ? 'active' : ''}"></div>`;
    }
    
    // Update buttons
    document.getElementById('btn-prev-card').disabled = currentFlashcardIndex === 0;
    document.getElementById('btn-next-card').disabled = currentFlashcardIndex === currentNotes.length - 1;
}

function nextCard() {
    if(currentFlashcardIndex < currentNotes.length - 1) {
        currentFlashcardIndex++;
        renderFlashcard();
    }
}

function prevCard() {
    if(currentFlashcardIndex > 0) {
        currentFlashcardIndex--;
        renderFlashcard();
    }
}

function startQuizFromNotes() {
    document.getElementById('notes-screen').classList.remove('active');
    startGame(currentGame);
}

let currentQuizData = [];

// Fisher-Yates Shuffle
function shuffleArray(array) {
    let currentIndex = array.length, randomIndex;
    while (currentIndex > 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }
    return array;
}

function startGame(gameId) {
    currentGame = gameId;
    currentScore = 0;
    sessionCorrect = 0;
    currentQuestionIndex = 0;
    
    const dataMap = {
        'unit1': typeof unit1Data !== 'undefined' ? unit1Data : [],
        'unit2': typeof unit2Data !== 'undefined' ? unit2Data : [],
        'unit3': typeof unit3Data !== 'undefined' ? unit3Data : [],
        'unit4': typeof unit4Data !== 'undefined' ? unit4Data : [],
        'unit5': typeof unit5Data !== 'undefined' ? unit5Data : [],
        'unit6': typeof unit6Data !== 'undefined' ? unit6Data : [],
        'unit7': typeof unit7Data !== 'undefined' ? unit7Data : [],
        'unit8': typeof unit8Data !== 'undefined' ? unit8Data : [],
        'unit9': typeof unit9Data !== 'undefined' ? unit9Data : [],
        'unit10': typeof unit10Data !== 'undefined' ? unit10Data : []
    };
    
    currentQuizData = shuffleArray([...dataMap[gameId]]);
    maxQuestions = currentQuizData.length;

    document.getElementById('score').innerText = '0';
    document.getElementById('main-menu').classList.remove('active');
    document.getElementById('game-screen').classList.add('active');
    
    document.getElementById('game-title').innerText = moduleDesc[gameId] || 'Kuiz Sains';
    nextQuestion();
}

function nextQuestion() {
    if (currentQuestionIndex >= maxQuestions) {
        endGame();
        return;
    }

    currentQuestionIndex++;
    document.getElementById('current-question-num').innerText = currentQuestionIndex;
    
    const progressPercent = ((currentQuestionIndex - 1) / maxQuestions) * 100;
    document.getElementById('progress-bar').style.width = progressPercent + '%';

    document.getElementById('feedback-area').classList.add('hidden');
    document.getElementById('explanation-box').classList.add('hidden');
    canProceed = false;

    const gameArea = document.getElementById('game-area');
    gameArea.innerHTML = '';
    
    executeQuestion(currentQuizData[currentQuestionIndex - 1]);
}

function proceedToNext() {
    if (!canProceed) return;
    nextQuestion();
}

// ==========================================
// UTILITY RENDERERS
// ==========================================

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// 1. Render standard MCQ
function renderMCQ(question, options, correctAnswer, explanation, image) {
    currentAnswer = correctAnswer;
    currentExplanation = explanation;
    
    let html = '';
    if (image) {
        html += `<div style="text-align: center;"><img src="${image}" class="quiz-img" alt="Soalan Bergambar" draggable="false"></div>`;
    }
    html += `<h3 style="text-align: center; margin-bottom: 20px; font-size: 1.5rem;">${question}</h3>`;
    html += `<div class="options-container" id="mcq-options" style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;"></div>`;
    document.getElementById('game-area').innerHTML = html;
    
    const container = document.getElementById('mcq-options');
    options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'btn btn-secondary';
        btn.style.width = '100%';
        btn.style.maxWidth = '300px';
        btn.style.padding = '15px';
        btn.style.fontSize = '1.2rem';
        btn.innerText = opt;
        btn.onclick = () => checkAnswer(opt, btn);
        container.appendChild(btn);
    });
}

// 2. Render True/False
function renderTrueFalse(question, isTrue, explanation, image) {
    currentAnswer = isTrue ? "Betul" : "Salah";
    currentExplanation = explanation;
    
    let html = '';
    if (image) {
        html += `<div style="text-align: center;"><img src="${image}" class="quiz-img" alt="Soalan Bergambar" draggable="false"></div>`;
    }
    html += `<h3 style="text-align: center; margin-bottom: 30px; font-size: 1.5rem; line-height: 1.4;">${question}</h3>`;
    html += `<div style="display: flex; gap: 20px; justify-content: center;">`;
    document.getElementById('game-area').innerHTML = html;
    
    const gameArea = document.getElementById('game-area');
    const btnBox = document.createElement('div');
    btnBox.style.display = 'flex';
    btnBox.style.gap = '20px';
    btnBox.style.justifyContent = 'center';
    
    const btnTrue = document.createElement('button');
    btnTrue.className = 'btn btn-secondary';
    btnTrue.innerHTML = '<i class="fas fa-check" style="font-size:2rem; color:var(--success-color); display:block; margin-bottom:10px;"></i> Betul';
    btnTrue.style.width = '150px';
    btnTrue.onclick = () => checkAnswer("Betul", btnTrue);
    
    const btnFalse = document.createElement('button');
    btnFalse.className = 'btn btn-secondary';
    btnFalse.innerHTML = '<i class="fas fa-times" style="font-size:2rem; color:var(--danger-color); display:block; margin-bottom:10px;"></i> Salah';
    btnFalse.style.width = '150px';
    btnFalse.onclick = () => checkAnswer("Salah", btnFalse);
    
    btnBox.appendChild(btnTrue);
    btnBox.appendChild(btnFalse);
    gameArea.appendChild(btnBox);
}

// ==========================================
// ANSWER CHECKING & FEEDBACK
// ==========================================
function checkAnswer(selected, btnElement) {
    if (canProceed) return; // Prevent multiple clicks
    
    const isCorrect = Array.isArray(currentAnswer) 
        ? currentAnswer.includes(selected) // for arrays if needed
        : selected === currentAnswer;

    if (btnElement) {
        if (isCorrect) {
            btnElement.classList.add('correct');
            btnElement.style.background = 'var(--success-color)';
            btnElement.style.color = 'white';
            btnElement.style.animation = 'popIn 0.5s ease';
        } else {
            btnElement.classList.add('wrong');
            btnElement.style.background = 'var(--danger-color)';
            btnElement.style.color = 'white';
            btnElement.style.animation = 'shake 0.5s ease';
            
            // Highlight correct answer if it's a standard MCQ
            const btns = document.querySelectorAll('#mcq-options button');
            btns.forEach(b => {
                if(b.innerText === currentAnswer) {
                    b.style.background = 'var(--success-color)';
                    b.style.color = 'white';
                }
            });
        }
    }

    // Disable all buttons
    const allBtns = document.querySelectorAll('#game-area button');
    allBtns.forEach(b => b.disabled = true);

    showFeedback(isCorrect, selected);
}

function showFeedback(isCorrect, selected) {
    canProceed = true;
    const feedbackArea = document.getElementById('feedback-area');
    const feedbackIcon = document.getElementById('feedback-icon');
    const feedbackTitle = document.getElementById('feedback-title');
    const feedbackMessage = document.getElementById('feedback-message');
    const explanationBox = document.getElementById('explanation-box');
    const explanationText = document.getElementById('explanation-text');
    
    feedbackArea.classList.remove('hidden');
    
    if (isCorrect) {
        audioCorrect.play().catch(e => console.log('Audio blocked', e));
        sessionCorrect++;
        currentScore += 10;
        document.getElementById('score').innerText = currentScore;
        createConfetti();
        
        feedbackArea.className = 'feedback-area correct';
        feedbackIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
        feedbackTitle.innerText = 'Tepat Sekali!';
        feedbackMessage.innerText = 'Bagus, jawapan anda betul.';
        explanationBox.classList.add('hidden');
    } else {
        audioWrong.play().catch(e => console.log('Audio blocked', e));
        
        feedbackArea.className = 'feedback-area wrong';
        feedbackIcon.innerHTML = '<i class="fas fa-times-circle"></i>';
        feedbackTitle.innerText = 'Kurang Tepat';
        feedbackMessage.innerText = `Jawapan yang betul ialah: ${currentAnswer}`;
        
        if (currentExplanation) {
            explanationBox.classList.remove('hidden');
            explanationText.innerText = currentExplanation;
        } else {
            explanationBox.classList.add('hidden');
        }
    }

    // Auto scroll to feedback
    feedbackArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Confetti Effect
function createConfetti() {
    for (let i = 0; i < 30; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.animationDuration = (Math.random() * 2 + 1) + 's';
        confetti.style.backgroundColor = ['#FD79A8', '#00B894', '#FDCB6E', '#0984E3'][Math.floor(Math.random() * 4)];
        document.body.appendChild(confetti);
        
        setTimeout(() => {
            confetti.remove();
        }, 3000);
    }
}

// ==========================================
// END GAME & DASHBOARD
// ==========================================
function endGame() {
    audioComplete.play().catch(e => console.log('Audio blocked', e));
    document.getElementById('progress-bar').style.width = '100%';
    
    const percentage = Math.round((sessionCorrect / maxQuestions) * 100);
    
    document.getElementById('summary-modal').style.display = 'flex';
    document.getElementById('final-score').innerText = percentage;
    
    const summaryMsg = document.getElementById('summary-message');
    if (percentage >= 80) summaryMsg.innerText = "Cemerlang! Anda sangat mahir topik ini.";
    else if (percentage >= 50) summaryMsg.innerText = "Bagus! Teruskan latihan untuk jadi lebih baik.";
    else summaryMsg.innerText = "Jangan putus asa! Mari ulang kaji dan cuba lagi.";

    recordSession(percentage);
}

function recordSession(percentage) {
    const record = {
        date: new Date().toISOString(),
        module: currentGame,
        correct: sessionCorrect,
        total: maxQuestions,
        score: percentage
    };
    sainsHistory.push(record);
    localStorage.setItem('sains_history', JSON.stringify(sainsHistory));
}

function closeSummaryAndHome() {
    document.getElementById('summary-modal').style.display = 'none';
    goHome();
}

function closeSummaryAndRestart() {
    document.getElementById('summary-modal').style.display = 'none';
    startGame(currentGame);
}

// Dashboard functions
function getModuleStats(mod) {
    const sessions = sainsHistory.filter(s => s.module === mod);
    if (sessions.length === 0) return { attempts: 0, accuracy: 0 };
    
    const totalScore = sessions.reduce((sum, s) => sum + s.score, 0);
    return { attempts: sessions.length, accuracy: Math.round(totalScore / sessions.length) };
}

function openDashboard() {
    document.getElementById('dashboard-modal').style.display = 'flex';
    switchTab(null, 'tab-daily');
    setTimeout(renderCharts, 100);
}

function closeDashboard() {
    document.getElementById('dashboard-modal').style.display = 'none';
}

function switchTab(e, tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    
    if (e && e.currentTarget) {
        e.currentTarget.classList.add('active');
    } else {
        const btn = document.querySelector(`.tab-btn[onclick*="${tabId}"]`);
        if (btn) btn.classList.add('active');
    }
    
    document.getElementById(tabId).classList.add('active');
    
    if (tabId === 'tab-history') {
        renderHistory();
    }
}

let dailyChartInstance = null;
let moduleChartInstance = null;

function renderCharts() {
    const ctxDaily = document.getElementById('dailyChart');
    const ctxModule = document.getElementById('moduleChart');
    if (!ctxDaily || !ctxModule) return;

    if (dailyChartInstance) dailyChartInstance.destroy();
    if (moduleChartInstance) moduleChartInstance.destroy();

    // Prepare Daily Data (Last 7 Sessions)
    const recentSessions = [...sainsHistory].slice(-7);
    const labels = recentSessions.map((_, i) => `Sesi ${i+1}`);
    const data = recentSessions.map(s => s.score);

    dailyChartInstance = new Chart(ctxDaily, {
        type: 'line',
        data: {
            labels: labels.length ? labels : ['Tiada Data'],
            datasets: [{
                label: 'Markah (%)',
                data: data.length ? data : [0],
                borderColor: '#00B894',
                backgroundColor: 'rgba(0, 184, 148, 0.2)',
                tension: 0.4,
                fill: true
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true, max: 100 } } }
    });

    // Prepare Module Data
    const allModules = [...kemahiranModules, ...penerokaanModules];
    const modLabels = allModules.map(m => m.replace('unit', 'Unit '));
    const modData = allModules.map(m => getModuleStats(m).accuracy);

    moduleChartInstance = new Chart(ctxModule, {
        type: 'bar',
        data: {
            labels: modLabels,
            datasets: [{
                label: 'Purata Markah (%)',
                data: modData,
                backgroundColor: '#FDCB6E'
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true, max: 100 } } }
    });
}

function renderHistory() {
    const tbody = document.getElementById('history-body');
    tbody.innerHTML = '';
    
    const sorted = [...sainsHistory].sort((a,b) => new Date(b.date) - new Date(a.date));
    
    if (sorted.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center">Belum ada rekod.</td></tr>';
        return;
    }
    
    sorted.slice(0, 50).forEach(record => {
        const d = new Date(record.date);
        const dateStr = d.toLocaleDateString('ms-MY') + ' ' + d.toLocaleTimeString('ms-MY', {hour: '2-digit', minute:'2-digit'});
        const modName = gameTitles[record.module] || record.module;
        
        let color = 'var(--danger-color)';
        if (record.score >= 80) color = 'var(--success-color)';
        else if (record.score >= 50) color = 'var(--warning-color)';
        
        tbody.innerHTML += `
            <tr>
                <td>${dateStr}</td>
                <td>${modName}</td>
                <td style="color:${color}; font-weight:bold;">${record.score}%</td>
            </tr>
        `;
    });
}

// Unit Placeholders (To be implemented)

// 3. Render Drag & Drop
function renderDragDrop(question, items, zones, correctMapping, explanation, image) {
    currentAnswer = correctMapping;
    currentExplanation = explanation;
    
    let html = '';
    if (image) {
        html += `<div style="text-align: center;"><img src="${image}" class="quiz-img" alt="Soalan Bergambar" draggable="false"></div>`;
    }
    html += `<h3 style="text-align: center; margin-bottom: 20px;">${question}</h3>`;
    html += `<div class="drag-container">`;
    html += `<div class="draggable-items-wrapper" id="drag-items">`;
    items.forEach(item => {
        let classNames = 'draggable';
        if(item.type === 'emoji') classNames += ' emoji-drag';
        html += `<div class="${classNames}" draggable="true" id="${item.id}" ondragstart="drag(event)">${item.text}</div>`;
    });
    html += `</div>`;
    html += `<div class="drop-zones-wrapper" id="drop-zones">`;
    zones.forEach(zone => {
        html += `<div class="drop-zone" id="${zone.id}" ondrop="drop(event)" ondragover="allowDrop(event)" ondragenter="dragEnter(event)" ondragleave="dragLeave(event)">
                    <h4>${zone.text}</h4>
                 </div>`;
    });
    html += `</div>`;
    html += `<button class="btn btn-primary" style="margin-top:20px; align-self:center;" onclick="checkDragDrop()">Semak Jawapan</button>`;
    html += `</div>`;
    
    document.getElementById('game-area').innerHTML = html;
}

function allowDrop(ev) { ev.preventDefault(); }
function dragEnter(ev) { ev.preventDefault(); ev.currentTarget.classList.add('over'); }
function dragLeave(ev) { ev.currentTarget.classList.remove('over'); }
function drag(ev) { ev.dataTransfer.setData("text", ev.target.id); }
function drop(ev) {
    ev.preventDefault();
    let target = ev.currentTarget;
    target.classList.remove('over');
    var data = ev.dataTransfer.getData("text");
    let item = document.getElementById(data);
    if(item && (target.classList.contains('drop-zone') || target.id === 'drag-items')) {
        target.appendChild(item);
    }
}

function checkDragDrop() {
    if(canProceed) return;
    let isAllCorrect = true;
    const remainingItems = document.getElementById('drag-items').children;
    if(remainingItems.length > 0) {
        alert("Sila letakkan semua item ke dalam kumpulan yang disediakan.");
        return;
    }
    const dragContainer = document.querySelector('.drag-container');
    const items = dragContainer.querySelectorAll('.draggable');
    items.forEach(item => {
        const itemId = item.id;
        const droppedZoneId = item.parentElement.id;
        const correctZoneId = currentAnswer[itemId];
        
        if(droppedZoneId === correctZoneId) {
            item.style.background = 'var(--success-color)';
            item.style.color = 'white';
        } else {
            item.style.background = 'var(--danger-color)';
            item.style.color = 'white';
            isAllCorrect = false;
        }
        item.draggable = false;
    });
    
    const btn = dragContainer.querySelector('button');
    if(btn) btn.disabled = true;
    
    showFeedback(isAllCorrect, "Sila rujuk penerangan");
}

// ==========================================
// UNIT GENERATORS
// ==========================================

function executeQuestion(q) {
    if (q.type === 'mcq') {
        renderMCQ(q.q, shuffleArray([...q.options]), q.answer, q.exp, q.image);
    } else if (q.type === 'tf') {
        renderTrueFalse(q.q, q.answer, q.exp, q.image);
    } else if (q.type === 'drag') {
        renderDragDrop(q.q, shuffleArray([...q.items]), q.zones, q.mapping, q.exp, q.image);
    }
}

// UNIT 1: Kemahiran Saintifik
const unit1Data = [
    { type: 'mcq', q: 'Pilih deria yang digunakan untuk membuat pemerhatian terhadap sekeping roti.', options: ['Sentuhan, rasa dan bau', 'Penglihatan, sentuhan, rasa dan bau', 'Pendengaran, sentuhan, rasa dan bau'], answer: 'Penglihatan, sentuhan, rasa dan bau', exp: 'Kita melihat rupa roti, menyentuh kelembutannya, merasa kelazatannya, dan menghidu baunya.', image: 'images/u1_bread.png?v=1' },
    { type: 'mcq', q: 'Shahil pergi bercuti ke pantai. Apakah deria yang digunakan apabila berehat di tepi pantai?', options: ['Rasa dan bau', 'Sentuhan dan rasa', 'Pendengaran dan penglihatan'], answer: 'Pendengaran dan penglihatan', exp: 'Mendengar bunyi deruan ombak dan melihat keindahan laut.', image: 'images/u1_beach.png?v=1' },
    { type: 'mcq', q: 'Apakah alat yang sesuai digunakan untuk mengukur lilit kepala selain pita pengukur?', options: ['Sudu', 'Pembaris', 'Tali benang'], answer: 'Tali benang', exp: 'Tali benang boleh dililit pada bentuk bulat kepala, kemudian diukur panjangnya pada pembaris lurus.', image: 'images/u1_measuring.png?v=1' },
    { type: 'mcq', q: 'Apakah alat pengukur untuk mengukur masa larian dengan paling tepat?', options: ['Jam lama', 'Jam randik', 'Jam dinding'], answer: 'Jam randik', exp: 'Jam randik direka khas untuk mengira saat dan minit larian secara tepat.', image: 'images/u1_stopwatch.png?v=1' },
    { type: 'mcq', q: 'Apakah kemahiran manipulatif apabila kita melukis objek yang dikaji (contoh: daun)?', options: ['Membersihkan alatan', 'Melakar spesimen dengan betul', 'Mengendalikan spesimen'], answer: 'Melakar spesimen dengan betul', exp: 'Melukis bahan/objek kajian seperti daun atau serangga dipanggil melakar spesimen.' },
    { type: 'mcq', q: 'Apakah kemahiran proses sains yang digunakan semasa menimbang berat buah menggunakan alat penimbang?', options: ['Berkomunikasi', 'Membuat inferens', 'Mengukur dan menggunakan nombor'], answer: 'Mengukur dan menggunakan nombor', exp: 'Alat penimbang mengeluarkan bacaan berat dalam bentuk nombor (contohnya Gram).', image: 'images/u1_scale.png?v=1' },
    { type: 'tf', q: 'Memerhati hanya menggunakan deria penglihatan sahaja.', answer: false, exp: 'Memerhati menggunakan kelima-lima deria manusia!' },
    { type: 'drag', q: 'Padankan deria dengan organ yang betul', 
      items: [{id:'i1',text:'<img src="images/mascot_1_seeing.png" class="drag-icon"> Melihat',type:'text'}, {id:'i2',text:'<img src="images/mascot_2_hearing.png" class="drag-icon"> Mendengar',type:'text'}, {id:'i3',text:'<img src="images/mascot_3_touching.png" class="drag-icon"> Menyentuh',type:'text'}, {id:'i4',text:'<img src="images/mascot_4_smelling.png" class="drag-icon"> Menghidu',type:'text'}, {id:'i5',text:'<img src="images/mascot_5_tasting.png" class="drag-icon"> Merasa',type:'text'}],
      zones: [{id:'z1',text:'👁️ Mata'}, {id:'z2',text:'👂 Telinga'}, {id:'z3',text:'✋ Kulit'}, {id:'z4',text:'👃 Hidung'}, {id:'z5',text:'👅 Lidah'}],
      mapping: {'i1':'z1', 'i2':'z2', 'i3':'z3', 'i4':'z4', 'i5':'z5'},
      exp: 'Mata untuk melihat, telinga untuk mendengar, kulit untuk menyentuh, hidung untuk menghidu, dan lidah untuk merasa.' },
    { type: 'mcq', q: 'Mengasingkan daun mengikut bentuk ialah proses...', options: ['Mengukur', 'Mengelas', 'Berkomunikasi'], answer: 'Mengelas', exp: 'Mengelas bermaksud mengasingkan atau mengumpulkan benda mengikut ciri yang sama.', image: 'images/u1_leaves.png?v=1' },
    { type: 'tf', q: 'Menulis keputusan eksperimen dalam jadual ialah kemahiran berkomunikasi.', answer: true, exp: 'Berkomunikasi boleh dilakukan dengan bercakap, menulis, melukis, atau menggunakan jadual/graf.' }
];



// UNIT 2: Peraturan Bilik Sains
const unit2Data = [
    { type: 'mcq', q: 'Di manakah sisa pepejal perlu dibuang di Bilik Sains?', options: ['Di lantai', 'Di dalam singki', 'Di dalam bakul sampah'], answer: 'Di dalam bakul sampah', exp: 'Sisa pepejal seperti mancis, kayu, dan kertas tidak boleh dibuang dalam singki kerana akan menyumbatkannya.' },
    { type: 'mcq', q: 'Mengapa murid perlu melaporkan kecederaan (contoh: luka kecil) kepada guru?', options: ['Untuk mengelakkan dimarahi', 'Untuk mendapatkan rawatan segera', 'Untuk bermain di luar kelas'], answer: 'Untuk mendapatkan rawatan segera', exp: 'Guru perlu dimaklumkan segera supaya murid boleh dirawat dan bahan berbahaya di tempat kejadian dapat dibersihkan.' },
    { type: 'tf', q: 'Murid boleh masuk ke dalam Bilik Sains tanpa kebenaran guru jika tiada siapa di dalam.', answer: false, exp: 'Kita mesti beratur dan tunggu kebenaran guru sebelum masuk untuk mengelakkan bahaya.' },
    { type: 'tf', q: 'Makan dan minum dilarang sama sekali di dalam Bilik Sains.', answer: true, exp: 'Makanan dan minuman boleh tercemar dengan wap bahan kimia beracun.' },
    { type: 'mcq', q: 'Apakah yang perlu dilakukan jika buret atau bikar kaca pecah?', options: ['Kutip dengan tangan', 'Laporkan kepada guru', 'Buang dalam bakul sampah segera'], answer: 'Laporkan kepada guru', exp: 'Guru akan membersihkannya menggunakan cara yang selamat. Jangan kutip guna tangan kosong.' },
    { type: 'drag', q: 'Kelaskan perbuatan berikut di dalam Bilik Sains',
      items: [{id:'i1',text:'🏃 Berlari',type:'text'}, {id:'i2',text:'🪟 Buka Tingkap',type:'text'}, {id:'i3',text:'💧 Bermain air',type:'text'}, {id:'i4',text:'🪑 Susun kerusi',type:'text'}],
      zones: [{id:'z1',text:'👍 Amalan Baik'}, {id:'z2',text:'👎 Dilarang'}],
      mapping: {'i1':'z2', 'i2':'z1', 'i3':'z2', 'i4':'z1'},
      exp: 'Membuka tingkap untuk pengudaraan dan menyusun kerusi adalah amalan yang baik.' },
    { type: 'mcq', q: 'Mengapakah tingkap dan pintu perlu dibuka semasa berada di Bilik Sains?', options: ['Supaya nyamuk masuk', 'Untuk pengudaraan yang baik', 'Kerana panas'], answer: 'Untuk pengudaraan yang baik', exp: 'Supaya udara segar dapat masuk dan gas atau bau bahan kimia dapat keluar.' },
    { type: 'tf', q: 'Sampah cecair yang selamat boleh dibuang ke dalam singki dengan membuka air paip.', answer: true, exp: 'Cecair yang dibenarkan oleh guru sahaja boleh masuk singki.' },
    { type: 'mcq', q: 'Apakah tindakan yang betul sebelum meninggalkan Bilik Sains?', options: ['Tinggalkan kerusi bersepah', 'Tutup suis kipas dan lampu', 'Biar radas tidak dicuci'], answer: 'Tutup suis kipas dan lampu', exp: 'Pastikan keadaan selamat, kemas, dan menjimatkan elektrik.' },
    { type: 'drag', q: 'Di manakah tempat buangan yang betul?',
      items: [{id:'i1',text:'📄 Kertas koyak',type:'text'}, {id:'i2',text:'🚰 Air paip lebihan',type:'text'}],
      zones: [{id:'z1',text:'Bakul Sampah'}, {id:'z2',text:'Singki'}],
      mapping: {'i1':'z1', 'i2':'z2'},
      exp: 'Pepejal ke dalam bakul sampah, air ke dalam singki.' }
];



// UNIT 3: Manusia
const unit3Data = [
    { type: 'mcq', q: 'Manakah urutan peringkat tumbesaran manusia yang betul?', options: ['Kanak-kanak → Bayi → Dewasa → Remaja', 'Bayi → Kanak-kanak → Remaja → Dewasa', 'Remaja → Kanak-kanak → Bayi → Dewasa'], answer: 'Bayi → Kanak-kanak → Remaja → Dewasa', exp: 'Manusia mula hidup sebagai Bayi, kemudian membesar jadi Kanak-Kanak, Remaja, dan akhirnya Dewasa.' },
    { type: 'mcq', q: 'Apakah perubahan utama apabila tumbesaran manusia meningkat?', options: ['Kematangan mental sahaja', 'Saiz, berat, dan tinggi bertambah', 'Warna kulit berubah'], answer: 'Saiz, berat, dan tinggi bertambah', exp: 'Fizikal kita berubah apabila membesar. Saiz badan bertambah besar, berat bertambah, dan tinggi makin bertambah.' },
    { type: 'mcq', q: 'Ciri manakah yang boleh diwarisi daripada ibu bapa atau keturunan kita?', options: ['Saiz kasut', 'Cara berjalan', 'Warna iris mata'], answer: 'Warna iris mata', exp: 'Warna mata, jenis rambut, dan warna kulit adalah genetik yang diwarisi daripada ibu bapa.' },
    { type: 'mcq', q: 'Manusia membiak secara...', options: ['Melahirkan anak', 'Bertelur', 'Biji benih'], answer: 'Melahirkan anak', exp: 'Manusia adalah kumpulan mamalia yang membiak dengan cara melahirkan anak.' },
    { type: 'drag', q: 'Susun peringkat tumbesaran manusia',
      items: [{id:'i1',text:'👦 Kanak-kanak',type:'text'}, {id:'i2',text:'👶 Bayi',type:'text'}, {id:'i3',text:'👨 Dewasa',type:'text'}, {id:'i4',text:'🧑 Remaja',type:'text'}],
      zones: [{id:'z1',text:'Peringkat 1'}, {id:'z2',text:'Peringkat 2'}, {id:'z3',text:'Peringkat 3'}, {id:'z4',text:'Peringkat 4'}],
      mapping: {'i2':'z1', 'i1':'z2', 'i4':'z3', 'i3':'z4'},
      exp: 'Bayi -> Kanak-kanak -> Remaja -> Dewasa' },
    { type: 'tf', q: 'Semakin kita membesar, saiz baju yang kita pakai pada waktu bayi akan menjadi ketat.', answer: true, exp: 'Ini kerana tumbesaran menyebabkan saiz badan, tinggi, dan berat kita bertambah.' },
    { type: 'tf', q: 'Anak mungkin mempunyai jenis rambut yang keriting seperti datuknya walaupun rambut bapanya lurus.', answer: true, exp: 'Ciri keturunan (pewarisan) juga boleh diwarisi daripada datuk atau nenek moyang kita.' },
    { type: 'drag', q: 'Kelaskan ciri-ciri manusia di bawah',
      items: [{id:'i1',text:'👁️ Warna Mata',type:'text'}, {id:'i2',text:'⚖️ Berat Badan',type:'text'}, {id:'i3',text:'💇 Jenis Rambut',type:'text'}, {id:'i4',text:'📚 Hobi Membaca',type:'text'}],
      zones: [{id:'z1',text:'Boleh Diwarisi (Genetik)'}, {id:'z2',text:'Bukan Diwarisi'}],
      mapping: {'i1':'z1', 'i3':'z1', 'i2':'z2', 'i4':'z2'},
      exp: 'Warna mata dan jenis rambut adalah ciri pewarisan. Berat badan dan hobi banyak bergantung kepada gaya hidup.' },
    { type: 'mcq', q: 'Seseorang individu yang tidak mewarisi ciri fizikal ibu bapanya secara terus, mungkin mewarisi ciri tersebut daripada...', options: ['Kawan rapat', 'Datuk atau Nenek', 'Jiran tetangga'], answer: 'Datuk atau Nenek', exp: 'Ciri-ciri ini dinamakan pewarisan keturunan dalam salasilah keluarga.' },
    { type: 'tf', q: 'Warna kulit seseorang adalah contoh ciri pewarisan.', answer: true, exp: 'Warna kulit dipengaruhi kuat oleh genetik ibu bapa.' }
];



// UNIT 4: Haiwan
const unit4Data = [
    { type: 'mcq', q: 'Haiwan manakah yang mempunyai kepak dan berkaki dua?', options: ['Itik', 'Tenuk', 'Cacing'], answer: 'Itik', exp: 'Itik ialah contoh burung yang mempunyai kepak dan dua kaki.' },
    { type: 'mcq', q: 'Haiwan manakah yang melahirkan anak dalam bilangan sedikit?', options: ['Arnab', 'Kucing', 'Ikan lumba-lumba'], answer: 'Ikan lumba-lumba', exp: 'Paus dan ikan lumba-lumba melahirkan anak yang sedikit berbanding arnab dan kucing yang melahirkan banyak anak.' },
    { type: 'mcq', q: 'Apakah persamaan antara arnab dan kucing dalam cara membiak?', options: ['Bertelur sedikit', 'Melahirkan anak sedikit', 'Melahirkan anak banyak'], answer: 'Melahirkan anak banyak', exp: 'Kucing dan arnab kedua-duanya melahirkan banyak anak (beberapa ekor sekaligus) pada satu-satu masa.' },
    { type: 'mcq', q: 'Apakah kepentingan haiwan mengeram dan menjaga telurnya di dalam sarang?', options: ['Supaya boleh dijual', 'Supaya telur nampak cantik', 'Supaya tidak dimakan haiwan lain'], answer: 'Supaya tidak dimakan haiwan lain', exp: 'Sarang dan penjagaan rapi melindungi telur daripada bahaya cuaca serta musuh.' },
    { type: 'mcq', q: 'Haiwan apakah yang bertelur dalam kuantiti yang sangat banyak?', options: ['Kucing', 'Penyu', 'Ayam'], answer: 'Penyu', exp: 'Penyu bertelur beratus-ratus biji kerana kebarangkalian telurnya dimakan haiwan pemangsa lain adalah tinggi.' },
    { type: 'drag', q: 'Kelaskan haiwan mengikut cara pembiakan',
      items: [{id:'i1',text:'🐸 Katak',type:'text'}, {id:'i2',text:'🦁 Singa',type:'text'}, {id:'i3',text:'🐄 Lembu',type:'text'}, {id:'i4',text:'🐍 Ular',type:'text'}],
      zones: [{id:'z1',text:'Bertelur'}, {id:'z2',text:'Melahirkan Anak'}],
      mapping: {'i1':'z1', 'i4':'z1', 'i2':'z2', 'i3':'z2'},
      exp: 'Singa dan lembu melahirkan anak. Katak dan ular pula bertelur.' },
    { type: 'mcq', q: 'Kitaran hidup rama-rama bermula daripada peringkat...', options: ['Pupa', 'Telur', 'Beluncas'], answer: 'Telur', exp: 'Kitaran: Telur -> Beluncas (Larva) -> Pupa (Kepompong) -> Rama-rama.', image: 'images/butterfly.png?v=4' },
    { type: 'drag', q: 'Susun kitaran hidup katak mengikut urutan',
      items: [{id:'i1',text:'Berudu',type:'text'}, {id:'i2',text:'🥚 Telur',type:'text'}, {id:'i3',text:'🐸 Katak Dewasa',type:'text'}, {id:'i4',text:'🐸 Anak Katak',type:'text'}],
      zones: [{id:'z1',text:'Mula'}, {id:'z2',text:'Kedua'}, {id:'z3',text:'Ketiga'}, {id:'z4',text:'Akhir'}],
      mapping: {'i2':'z1', 'i1':'z2', 'i4':'z3', 'i3':'z4'},
      exp: 'Bermula dari Telur -> Berudu -> Anak Katak -> Katak Dewasa', image: 'images/frog.png?v=4' },
    { type: 'tf', q: 'Semua anak haiwan di dunia ini menyerupai rupa ibu bapanya sejurus dilahirkan.', answer: false, exp: 'Contohnya berudu lansung tidak menyerupai katak dewasa, begitu juga beluncas yang tidak sama dengan rama-rama.' },
    { type: 'drag', q: 'Padankan anak dengan ibunya',
      items: [{id:'i1',text:'Berudu',type:'text'}, {id:'i2',text:'🐛 Beluncas',type:'text'}],
      zones: [{id:'z1',text:'Rama-rama'}, {id:'z2',text:'Katak'}],
      mapping: {'i1':'z2', 'i2':'z1'},
      exp: 'Berudu membesar menjadi katak. Beluncas akan membesar menjadi rama-rama.' }
];



// UNIT 5: Tumbuh-tumbuhan
const unit5Data = [
    { type: 'mcq', q: 'Tumbuh-tumbuhan sangat penting kerana ia membekalkan...', options: ['Pakaian dan elektrik', 'Oksigen dan makanan', 'Plastik'], answer: 'Oksigen dan makanan', exp: 'Tumbuhan menghasilkan oksigen dan menjadi sumber makanan untuk manusia serta haiwan.' },
    { type: 'tf', q: 'Biji benih memerlukan cahaya matahari untuk mula bercambah.', answer: false, exp: 'Biji benih HANYA memerlukan air, udara dan suhu yang sesuai untuk bercambah. Cahaya matahari belum diperlukan sehingga ia mempunyai daun.' },
    { type: 'drag', q: 'Kelaskan keperluan asas',
      items: [{id:'i1',text:'💧 Air',type:'text'}, {id:'i2',text:'💨 Udara',type:'text'}, {id:'i3',text:'🌡️ Suhu Sesuai',type:'text'}, {id:'i4',text:'☀️ Cahaya',type:'text'}],
      zones: [{id:'z1',text:'Untuk Tumbesaran Pokok'}, {id:'z2',text:'Untuk Percambahan Biji Benih'}],
      mapping: {'i4':'z1', 'i1':'z2', 'i2':'z2', 'i3':'z2'},
      exp: 'Biji benih perlukan air, udara, suhu. Pokok perlukan air, udara, cahaya matahari.' },
    { type: 'mcq', q: 'Apakah yang akan bertambah apabila pokok membesar?', options: ['Jumlah daun', 'Warna bunga', 'Jenis buah'], answer: 'Jumlah daun', exp: 'Bila pokok membesar, jumlah daun, saiz daun, lilitan batang dan tingginya bertambah.' },
    { type: 'drag', q: 'Susun urutan tumbesaran pokok',
      items: [{id:'i1',text:'🌱 Biji Benih',type:'text'}, {id:'i2',text:'🌿 Anak Pokok',type:'text'}, {id:'i3',text:'🌸 Pokok Berbunga',type:'text'}],
      zones: [{id:'z1',text:'Mula'}, {id:'z2',text:'Kedua'}, {id:'z3',text:'Akhir'}],
      mapping: {'i1':'z1', 'i2':'z2', 'i3':'z3'},
      exp: 'Biji Benih -> Percambahan -> Anak Pokok -> Pokok Dewasa -> Pokok Berbunga.' },
    { type: 'tf', q: 'Tumbuhan yang tidak disiram air akan mati layu.', answer: true, exp: 'Air merupakan keperluan asas yang sangat penting.' },
    { type: 'mcq', q: 'Jika anak pokok ditutup rapat dengan kotak plastik jernih tanpa lubang, apakah yang akan berlaku?', options: ['Pokok tumbuh tinggi', 'Pokok akan mati', 'Pokok berbunga lebat'], answer: 'Pokok akan mati', exp: 'Ia mati kerana ketiadaan udara segar (karbon dioksida) untuk membuat makanan.' },
    { type: 'tf', q: 'Pokok menghasilkan makanannya sendiri.', answer: true, exp: 'Proses ini dipanggil fotosintesis, menggunakan cahaya matahari.' },
    { type: 'mcq', q: 'Apakah urutan yang betul tumbesaran buah tembikai?', options: ['Biji -> Bunga -> Buah', 'Biji -> Anak pokok -> Bunga -> Buah', 'Bunga -> Biji -> Buah'], answer: 'Biji -> Anak pokok -> Bunga -> Buah', exp: 'Ini adalah kitaran hidup tumbuhan yang berbuah.' },
    { type: 'tf', q: 'Semasa membesar, batang pokok menjadi semakin besar (lilitan bertambah).', answer: true, exp: 'Ya, lilitan batang pokok adalah salah satu penunjuk bahawa ia membesar.' }
];



// UNIT 6: Terang dan Gelap
const unit6Data = [
    { type: 'mcq', q: 'Sumber cahaya yang utama untuk bumi ialah...', options: ['Matahari', 'Bulan', 'Lampu suluh'], answer: 'Matahari', exp: 'Matahari ialah sumber cahaya semula jadi yang paling besar dan utama.' },
    { type: 'tf', q: 'Bulan adalah sumber cahaya semula jadi.', answer: false, exp: 'Bulan tidak mengeluarkan cahaya sendiri, ia memantulkan cahaya matahari.' },
    { type: 'drag', q: 'Kelaskan sumber cahaya ini',
      items: [{id:'i1',text:'💡 Lampu',type:'text'}, {id:'i2',text:'🔥 Api',type:'text'}, {id:'i3',text:'🪨 Batu',type:'text'}, {id:'i4',text:'☀️ Matahari',type:'text'}],
      zones: [{id:'z1',text:'Sumber Cahaya'}, {id:'z2',text:'Bukan Sumber Cahaya'}],
      mapping: {'i1':'z1', 'i2':'z1', 'i4':'z1', 'i3':'z2'},
      exp: 'Batu tidak mengeluarkan sebarang cahaya.' },
    { type: 'mcq', q: 'Bayang-bayang terbentuk apabila cahaya...', options: ['Masuk ke dalam mata', 'Dihalang oleh objek', 'Dipantulkan oleh cermin'], answer: 'Dihalang oleh objek', exp: 'Cahaya bergerak lurus. Apabila ia dihalang oleh objek legap, bayang-bayang terhasil di sebalik objek tersebut.', image: 'images/shadow.png?v=4' },
    { type: 'tf', q: 'Dalam keadaan terang, kita lebih mudah melihat objek berbanding dalam keadaan gelap.', answer: true, exp: 'Mata memerlukan cahaya untuk melihat sesuatu objek.' },
    { type: 'mcq', q: 'Apakah yang terjadi kepada bayang-bayang apabila lampu suluh didekatkan kepada objek?', options: ['Menjadi kecil', 'Menjadi besar', 'Hilang'], answer: 'Menjadi besar', exp: 'Semakin dekat sumber cahaya dengan objek, semakin besar saiz bayang-bayang.' },
    { type: 'drag', q: 'Permainan bayang-bayang selalunya menggunakan...',
      items: [{id:'i1',text:'💡 Lampu',type:'text'}, {id:'i2',text:'✋ Tangan',type:'text'}, {id:'i3',text:'💧 Air',type:'text'}],
      zones: [{id:'z1',text:'Perlu'}, {id:'z2',text:'Tidak Perlu'}],
      mapping: {'i1':'z1', 'i2':'z1', 'i3':'z2'},
      exp: 'Permainan bayang-bayang memerlukan sumber cahaya dan objek penghalang.' },
    { type: 'tf', q: 'Bayang-bayang bagi bola akan berbentuk bulat.', answer: true, exp: 'Bentuk bayang-bayang menyerupai bentuk objek yang menghalang cahaya.' },
    { type: 'mcq', q: 'Objek yang paling jelas menghasilkan bayang-bayang gelap dinamakan...', options: ['Objek Lut Sinar', 'Objek Legap', 'Objek Kaca'], answer: 'Objek Legap', exp: 'Objek legap (seperti kayu atau logam) menghalang seluruh cahaya daripada melaluinya.' },
    { type: 'tf', q: 'Membaca di tempat gelap boleh membuatkan mata kita berasa cepat letih.', answer: true, exp: 'Kekurangan cahaya menyebabkan mata terpaksa bekerja lebih keras.' }
];



// UNIT 7: Elektrik
const unit7Data = [
    { type: 'mcq', q: 'Komponen yang membekalkan tenaga dalam litar ringkas ialah...', options: ['Wayar', 'Suis', 'Sel Kering (Bateri)'], answer: 'Sel Kering (Bateri)', exp: 'Sel kering berfungsi sebagai pembekal tenaga elektrik.', image: 'images/circuit.png?v=4' },
    { type: 'drag', q: 'Padankan fungsi komponen elektrik',
      items: [{id:'i1',text:'🔌 Menyambung/Memutuskan litar',type:'text'}, {id:'i2',text:'💡 Mengeluarkan cahaya',type:'text'}],
      zones: [{id:'z1',text:'Mentol'}, {id:'z2',text:'Suis'}],
      mapping: {'i1':'z2', 'i2':'z1'},
      exp: 'Suis mengawal aliran elektrik. Mentol bercahaya jika ada elektrik.' },
    { type: 'tf', q: 'Lampu akan menyala jika litar elektrik adalah litar terbuka (suis ditutup/off).', answer: false, exp: 'Lampu hanya menyala dalam litar TERTUTUP (suis dipasang/on) di mana arus elektrik boleh mengalir.' },
    { type: 'mcq', q: 'Jika mentol dalam litar tidak menyala, apakah puncanya?', options: ['Wayar disambung dengan betul', 'Sel kering baharu', 'Mentol telah rosak/terbakar'], answer: 'Mentol telah rosak/terbakar', exp: 'Mentol yang rosak atau sel kering yang kehabisan tenaga menyebabkan litar tidak berfungsi.' },
    { type: 'tf', q: 'Alat permainan kereta kawalan jauh selalunya menggunakan kuasa elektrik daripada sel kering (bateri).', answer: true, exp: 'Ia menggunakan bateri untuk membekalkan elektrik.' },
    { type: 'drag', q: 'Kelaskan barangan',
      items: [{id:'i1',text:'📺 Televisyen',type:'text'}, {id:'i2',text:'🪑 Kerusi',type:'text'}, {id:'i3',text:'🧺 Mesin Basuh',type:'text'}, {id:'i4',text:'📖 Buku',type:'text'}],
      zones: [{id:'z1',text:'Guna Elektrik'}, {id:'z2',text:'Tidak Guna Elektrik'}],
      mapping: {'i1':'z1', 'i3':'z1', 'i2':'z2', 'i4':'z2'},
      exp: 'Barang elektrik memudahkan urusan harian kita.' },
    { type: 'mcq', q: 'Bahan manakah yang BUKAN merupakan konduktor elektrik (tidak membenarkan elektrik mengalir)?', options: ['Paku Besi', 'Sudu Besi', 'Pemadam Getah'], answer: 'Pemadam Getah', exp: 'Getah, plastik dan kayu adalah penebat (penghalang) elektrik.' },
    { type: 'tf', q: 'Kita tidak boleh menyentuh suis dengan tangan yang basah.', answer: true, exp: 'Air ialah konduktor elektrik yang boleh menyebabkan kita terkena renjatan elektrik.' },
    { type: 'mcq', q: 'Apakah fungsi wayar dalam litar elektrik?', options: ['Menyambungkan komponen litar', 'Membekalkan cahaya', 'Mematikan elektrik'], answer: 'Menyambungkan komponen litar', exp: 'Wayar membenarkan arus elektrik mengalir menghubungkan komponen.' },
    { type: 'tf', q: 'Sel kering mempunyai dua terminal iaitu terminal positif (+) dan terminal negatif (-).', answer: true, exp: 'Pemasangan bateri mesti selari dengan terminal yang betul supaya elektrik dapat mengalir.' }
];



// UNIT 8: Campuran
const unit8Data = [
    { type: 'mcq', q: 'Proses memisahkan serbuk besi daripada pasir boleh dilakukan menggunakan...', options: ['Tapis', 'Magnet', 'Tangan'], answer: 'Magnet', exp: 'Magnet menarik serbuk besi dan meninggalkan pasir.' },
    { type: 'tf', q: 'Garam akan hilang (larut) jika dikacau di dalam air.', answer: true, exp: 'Garam adalah bahan yang boleh larut di dalam air.' },
    { type: 'drag', q: 'Kelaskan bahan ini jika dicampurkan dalam air',
      items: [{id:'i1',text:'🍬 Gula',type:'text'}, {id:'i2',text:'🏖️ Pasir',type:'text'}, {id:'i3',text:'🪨 Batu',type:'text'}, {id:'i4',text:'☕ Serbuk Milo',type:'text'}],
      zones: [{id:'z1',text:'Boleh Larut'}, {id:'z2',text:'Tidak Larut'}],
      mapping: {'i1':'z1', 'i4':'z1', 'i2':'z2', 'i3':'z2'},
      exp: 'Gula dan milo akan larut di dalam air.' },
    { type: 'mcq', q: 'Cara terbaik untuk mempercepatkan gula larut di dalam air ialah dengan menggunakan air...', options: ['Air Sejuk', 'Air Panas', 'Air Paip Biasa'], answer: 'Air Panas', exp: 'Bahan larut lebih cepat di dalam air panas berbanding air sejuk.' },
    { type: 'tf', q: 'Kita boleh memisahkan campuran campuran kacang hijau dan tepung dengan menapisnya.', answer: true, exp: 'Tepung akan melepasi penapis kerana saiznya kecil, manakala kacang terperangkap.' },
    { type: 'mcq', q: 'Apakah alat yang paling sesuai digunakan untuk mencampurkan warna cecair?', options: ['Sudu (Kacauan)', 'Pisau', 'Gunting'], answer: 'Sudu (Kacauan)', exp: 'Mengacau mempercepatkan campuran sebati.' },
    { type: 'drag', q: 'Padankan kaedah pemisahan',
      items: [{id:'i1',text:'Guna Penapis',type:'text'}, {id:'i2',text:'🖐️ Guna Tangan',type:'text'}],
      zones: [{id:'z1',text:'Kelikir & Pasir'}, {id:'z2',text:'Air Kelapa & Hampas'}],
      mapping: {'i1':'z2', 'i2':'z1'},
      exp: 'Guna tangan/mengutip sesuai untuk objek besar yang mudah dilihat.' },
    { type: 'tf', q: 'Minyak akan bercampur sebati dengan air jika dikacau dengan lama.', answer: false, exp: 'Minyak tidak larut di dalam air. Ia akan sentiasa timbul di atas air.' },
    { type: 'mcq', q: 'Apakah yang terjadi jika kita memasukkan sehelai daun ke dalam air?', options: ['Daun larut', 'Daun tenggelam', 'Daun timbul (terapung)'], answer: 'Daun timbul (terapung)', exp: 'Daun lebih ringan dan kurang tumpat daripada air.' },
    { type: 'tf', q: 'Sudu besi akan tenggelam kerana ia lebih tumpat daripada air.', answer: true, exp: 'Bahan yang berat dan padat seperti besi akan tenggelam.' }
];



// UNIT 9: Bumi
const unit9Data = [
    { type: 'mcq', q: 'Sumber air semula jadi untuk bumi datang dari mana?', options: ['Paip rumah', 'Hujan dan sungai', 'Kolam renang'], answer: 'Hujan dan sungai', exp: 'Hujan turun ke bumi dan mengalir ke sungai, tasik, dan laut sebagai sumber air semula jadi.' },
    { type: 'tf', q: 'Air sungai biasanya akan mengalir menuju ke laut.', answer: true, exp: 'Air mengalir dari kawasan tinggi ke kawasan rendah seperti laut.' },
    { type: 'drag', q: 'Susun urutan kitaran air',
      items: [{id:'i1',text:'♨️ Wap Air',type:'text'}, {id:'i2',text:'☁️ Awan',type:'text'}, {id:'i3',text:'🌧️ Hujan',type:'text'}],
      zones: [{id:'z1',text:'Pertama'}, {id:'z2',text:'Kedua'}, {id:'z3',text:'Ketiga'}],
      mapping: {'i1':'z1', 'i2':'z2', 'i3':'z3'},
      exp: 'Air menyejat jadi wap air -> membentuk awan -> awan berat turun hujan.' },
    { type: 'mcq', q: 'Kawasan yang dipenuhi air masin yang sangat luas dinamakan...', options: ['Tasik', 'Laut', 'Sungai'], answer: 'Laut', exp: 'Laut membekalkan air masin yang meliputi 70% bumi.' },
    { type: 'tf', q: 'Udara wujud di sekeliling kita walaupun kita tidak boleh melihatnya.', answer: true, exp: 'Udara tidak boleh dilihat tetapi boleh dirasai apabila angin bertiup.' },
    { type: 'drag', q: 'Kelaskan keadaan udara',
      items: [{id:'i1',text:'🫁 Bernafas',type:'text'}, {id:'i2',text:'💨 Angin Kipas',type:'text'}, {id:'i3',text:'🪑 Kerusi',type:'text'}],
      zones: [{id:'z1',text:'Udara Bergerak / Angin'}, {id:'z2',text:'Bukan Udara'}],
      mapping: {'i1':'z1', 'i2':'z1', 'i3':'z2'},
      exp: 'Pernafasan dan angin kipas adalah pergerakan udara.' },
    { type: 'mcq', q: 'Apakah yang terjadi apabila angin bertiup kencang?', options: ['Pokok bergoyang', 'Bulan bersinar', 'Hujan berhenti'], answer: 'Pokok bergoyang', exp: 'Angin kencang menyebabkan pokok bergoyang kuat dan kadangkala boleh tumbang.' },
    { type: 'tf', q: 'Angin yang bertiup perlahan dipanggil bayu.', answer: true, exp: 'Angin sepoi-sepoi bahasa atau bayu sangat nyaman dirasai.' },
    { type: 'mcq', q: 'Angin ialah...', options: ['Cahaya dari matahari', 'Udara yang bergerak', 'Air yang mengalir'], answer: 'Udara yang bergerak', exp: 'Angin kuat boleh menyebabkan ombak dan tiupan pokok.' },
    { type: 'tf', q: 'Bumi adalah planet yang bulat yang dipenuhi banyak air dan tanah.', answer: true, exp: 'Bentuk bumi adalah sfera (bulat) dan diliputi lebih banyak air daripada daratan.' }
];



// UNIT 10: Teknologi
const unit10Data = [
    { type: 'mcq', q: 'Apakah alat yang paling sesuai dipasang untuk membentuk sebuah kereta mainan maya?', options: ['Sayap', 'Tayar (Roda)', 'Bumbung rumah'], answer: 'Tayar (Roda)', exp: 'Tayar atau roda sangat penting untuk membolehkan kenderaan bergerak.' },
    { type: 'tf', q: 'Set binaan perlu dipasang mengikut arahan manual supaya bentuknya menjadi betul.', answer: true, exp: 'Manual bergambar disediakan sebagai panduan asas.' },
    { type: 'drag', q: 'Kelaskan bentuk asas binaan',
      items: [{id:'i1',text:'🏠 Bumbung',type:'text'}, {id:'i2',text:'🛞 Tayar',type:'text'}, {id:'i3',text:'🏛️ Tiang',type:'text'}],
      zones: [{id:'z1',text:'Segi Tiga'}, {id:'z2',text:'Bulat'}, {id:'z3',text:'Silinder'}],
      mapping: {'i1':'z1', 'i2':'z2', 'i3':'z3'},
      exp: 'Bumbung selalu piramid/segitiga, tayar itu bulat, dan tiang adalah silinder tinggi.' },
    { type: 'mcq', q: 'Komponen yang digunakan untuk memutarkan tayar dalam set binaan robotik selalunya ialah...', options: ['Motor elektrik', 'Mentol', 'Kertas'], answer: 'Motor elektrik', exp: 'Motor menggunakan elektrik (bateri) untuk menghasilkan pergerakan pusingan.' },
    { type: 'tf', q: 'Selepas selesai bermain set binaan, kita boleh membiarkannya bersepah di atas lantai.', answer: false, exp: 'Komponen perlu dileraikan dan disimpan semula dengan kemas di dalam kotak.' },
    { type: 'mcq', q: 'Apakah faedah membina menggunakan set binaan?', options: ['Meningkatkan selera makan', 'Melatih pemikiran kreatif', 'Membuat mata rabun'], answer: 'Melatih pemikiran kreatif', exp: 'Membina rekaan dapat melatih otak dan tangan bekerjasama.' },
    { type: 'drag', q: 'Padankan fungsi',
      items: [{id:'i1',text:'📖 Buku Manual',type:'text'}, {id:'i2',text:'📦 Kotak Penyimpanan',type:'text'}],
      zones: [{id:'z1',text:'Simpan Komponen'}, {id:'z2',text:'Panduan Pemasangan'}],
      mapping: {'i1':'z2', 'i2':'z1'},
      exp: 'Manual untuk rujukan, kotak untuk simpanan selamat.' },
    { type: 'tf', q: 'Set binaan hanya ada satu cara sahaja untuk dipasang.', answer: false, exp: 'Walaupun ada manual, kita boleh gunakan imaginasi untuk mencipta pelbagai bentuk lain.' },
    { type: 'mcq', q: 'Komponen berbentuk ____ sangat sesuai dijadikan badan kereta mainan.', options: ['Bebola', 'Segi empat', 'Cincin'], answer: 'Segi empat', exp: 'Bentuk blok kuboid (segi empat) stabil sebagai badan kenderaan.' },
    { type: 'tf', q: 'Bahagian yang tajam dalam set binaan perlu dipasang dengan berhati-hati supaya tidak cedera.', answer: true, exp: 'Keselamatan sentiasa diutamakan.' }
];



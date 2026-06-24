// ==========================================
// SAINS EXPLORER v2 — ENGINE
// Self-guided, dyslexia-friendly. Reuses ../sains-darjah2/notes_data.js (content untouched)
// ==========================================

const STATE_KEY = 'sains_explorer_v2';

const UNITS = [
    { id: 'unit1',  emoji: '🔬', name: 'Kemahiran Saintifik',  island: 'Pulau Saintis',     color: '#5DADE2', badge: '🔬' },
    { id: 'unit2',  emoji: '🛑', name: 'Peraturan Bilik Sains', island: 'Pulau Keselamatan', color: '#AAB7B8', badge: '🛡️' },
    { id: 'unit3',  emoji: '👶', name: 'Manusia',               island: 'Pulau Manusia',     color: '#EC7063', badge: '🧬' },
    { id: 'unit4',  emoji: '🐾', name: 'Haiwan',                island: 'Pulau Haiwan',      color: '#58D68D', badge: '🦋' },
    { id: 'unit5',  emoji: '🌱', name: 'Tumbuh-tumbuhan',       island: 'Pulau Hijau',       color: '#48C9B0', badge: '🌳' },
    { id: 'unit6',  emoji: '💡', name: 'Terang dan Gelap',      island: 'Pulau Cahaya',      color: '#F4D03F', badge: '☀️' },
    { id: 'unit7',  emoji: '⚡', name: 'Elektrik',              island: 'Pulau Kuasa',       color: '#AF7AC5', badge: '🔋' },
    { id: 'unit8',  emoji: '🧪', name: 'Campuran',              island: 'Pulau Campuran',    color: '#EB984E', badge: '🧫' },
    { id: 'unit9',  emoji: '🌍', name: 'Bumi',                  island: 'Pulau Bumi',        color: '#5DADE2', badge: '🌊' },
    { id: 'unit10', emoji: '🤖', name: 'Teknologi',             island: 'Pulau Robot',       color: '#85929E', badge: '🚀' }
];

// ========================================== STATE
function createDefaultState() {
    return { streak: 0, lastLoginDate: null, completedUnits: [], badges: [], quizScores: {}, totalProgress: 0 };
}
function loadState() {
    try {
        const s = localStorage.getItem(STATE_KEY);
        if (s) return { ...createDefaultState(), ...JSON.parse(s) };
    } catch (e) {}
    return createDefaultState();
}
function saveState(state) { localStorage.setItem(STATE_KEY, JSON.stringify(state)); }

// ========================================== STREAK (only counts a real attempt)
function checkStreak() { return loadState(); } // streak now bumped on quiz finish, not page open

function bumpStreakOnActivity() {
    const state = loadState();
    const today = new Date().toDateString();
    if (state.lastLoginDate !== today) {
        const y = new Date(); y.setDate(y.getDate() - 1);
        state.streak = (state.lastLoginDate === y.toDateString()) ? state.streak + 1 : 1;
        state.lastLoginDate = today;
        saveState(state);
    }
    return state;
}

// ========================================== GENEROUS UNLOCKING
// A unit unlocks once the PREVIOUS one has been *attempted at all* (any score).
// No one gets hard-locked by a low score. Unit 1 always open.
function isUnitUnlocked(unitId) {
    const idx = UNITS.findIndex(u => u.id === unitId);
    if (idx === 0) return true;
    const state = loadState();
    const prev = UNITS[idx - 1];
    return !!state.quizScores[prev.id] || state.completedUnits.includes(prev.id);
}
function getUnitStatus(unitId) {
    const state = loadState();
    if (state.completedUnits.includes(unitId)) return 'completed';
    if (isUnitUnlocked(unitId)) return 'unlocked';
    return 'locked';
}
function completeUnit(unitId) {
    const state = loadState();
    const def = UNITS.find(u => u.id === unitId);
    if (!state.completedUnits.includes(unitId)) state.completedUnits.push(unitId);
    if (def && !state.badges.includes(def.badge)) state.badges.push(def.badge);
    state.totalProgress = Math.round((state.completedUnits.length / UNITS.length) * 100);
    saveState(state);
    return state;
}
function saveQuizScore(unitId, pct) {
    const state = loadState();
    if (!state.quizScores[unitId]) state.quizScores[unitId] = { best: 0, attempts: 0 };
    state.quizScores[unitId].attempts += 1;
    state.quizScores[unitId].best = Math.max(state.quizScores[unitId].best, pct);
    saveState(state);
}
function starsFor(pct) { return pct >= 80 ? 3 : pct >= 60 ? 2 : pct >= 1 ? 1 : 0; }

// ========================================== QUIZ GENERATION (3 types)
function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
}
function allNotesFlat() {
    const out = [];
    if (typeof unitNotesData === 'undefined') return out;
    Object.values(unitNotesData).forEach(arr => arr.forEach(n => out.push(n)));
    return out;
}

function generateQuiz(unitId) {
    if (typeof unitNotesData === 'undefined' || !unitNotesData[unitId]) return [];
    const notes = unitNotesData[unitId];
    const globalPool = allNotesFlat();
    const questions = [];

    // pick a varied type per note, cycling so every quiz mixes formats
    const cycle = ['mcq', 'emoji', 'tf'];

    notes.forEach((note, idx) => {
        const type = cycle[idx % cycle.length];

        if (type === 'emoji') {
            // Low reading load: pick the emoji that matches the answer
            const correct = note.backEmoji || note.frontEmoji;
            const distract = shuffle(globalPool.map(n => n.backEmoji || n.frontEmoji)
                .filter(e => e && e !== correct))
                .filter((e, i, self) => self.indexOf(e) === i)
                .slice(0, 3);
            while (distract.length < 3) distract.push(['❓','⭐','🌟','✨'][distract.length]);
            const opts = shuffle([correct, ...distract]);
            questions.push({
                type: 'emoji',
                emoji: note.frontEmoji,
                question: note.frontQuestion,
                speak: note.frontQuestion,
                options: opts,
                correctIndex: opts.indexOf(correct),
                explanation: note.backAnswer + (note.trivia ? ' 💡 ' + note.trivia : '')
            });
        } else if (type === 'tf') {
            // Show a statement that's sometimes right, sometimes wrong. Kid picks Betul/Salah.
            const makeFalse = Math.random() < 0.5;
            let statement, isTrue;
            if (makeFalse) {
                const other = shuffle(globalPool.filter(n => n.backTitle !== note.backTitle))[0] || note;
                statement = `${note.frontTitle}: ${other.backTitle}`;
                isTrue = false;
            } else {
                statement = `${note.frontTitle}: ${note.backTitle}`;
                isTrue = true;
            }
            // options fixed: index 0 = Betul, 1 = Salah
            questions.push({
                type: 'tf',
                emoji: note.frontEmoji,
                question: 'Betul atau salah?',
                statement: statement,
                speak: statement,
                correctIndex: isTrue ? 0 : 1,
                explanation: note.backAnswer + (note.trivia ? ' 💡 ' + note.trivia : '')
            });
        } else {
            // Standard MCQ — answer is the key phrase (backTitle)
            const correct = note.backTitle;
            let distract = shuffle(notes.filter((_, i) => i !== idx).map(n => n.backTitle));
            if (distract.length < 3) {
                const extra = shuffle(globalPool.map(n => n.backTitle).filter(t => t !== correct && !distract.includes(t)));
                distract = distract.concat(extra);
            }
            distract = distract.filter((t, i, self) => self.indexOf(t) === i).slice(0, 3);
            while (distract.length < 3) distract.push(['Tidak pasti', 'Semua betul', 'Tiada jawapan'][distract.length] || '—');
            const opts = shuffle([correct, ...distract]);
            questions.push({
                type: 'mcq',
                emoji: note.frontEmoji,
                question: note.frontQuestion,
                speak: note.frontQuestion,
                options: opts,
                correctIndex: opts.indexOf(correct),
                explanation: note.backAnswer + (note.trivia ? ' 💡 ' + note.trivia : '')
            });
        }
    });

    return shuffle(questions);
}

// ========================================== PARENT
function getParentStats() { return loadState(); }
function clearAllData() { localStorage.removeItem(STATE_KEY); location.reload(); }

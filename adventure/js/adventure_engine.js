// ==========================================
// ADVENTURE ENGINE v2 — Sains Darjah 2
// Self-Guided, Dyslexia-Friendly
// ==========================================

const STATE_KEY = 'sains_adventure_v2';

// Unit definitions (10 units from Sains Darjah 2)
const UNITS = [
    { id: 'unit1', emoji: '🔬', name: 'Kemahiran Saintifik', island: 'Pulau Saintis', color: '#85C1E9', badge: '🔬' },
    { id: 'unit2', emoji: '🛑', name: 'Peraturan Bilik Sains', island: 'Pulau Keselamatan', color: '#AEB6BF', badge: '🛡️' },
    { id: 'unit3', emoji: '👶', name: 'Manusia', island: 'Pulau Manusia', color: '#F1948A', badge: '🧬' },
    { id: 'unit4', emoji: '🐾', name: 'Haiwan', island: 'Pulau Haiwan', color: '#82E0AA', badge: '🦋' },
    { id: 'unit5', emoji: '🌱', name: 'Tumbuh-tumbuhan', island: 'Pulau Hijau', color: '#73C6B6', badge: '🌳' },
    { id: 'unit6', emoji: '💡', name: 'Terang dan Gelap', island: 'Pulau Cahaya', color: '#F7DC6F', badge: '☀️' },
    { id: 'unit7', emoji: '⚡', name: 'Elektrik', island: 'Pulau Kuasa', color: '#BB8FCE', badge: '🔋' },
    { id: 'unit8', emoji: '🧪', name: 'Campuran', island: 'Pulau Campuran', color: '#F0B27A', badge: '🧫' },
    { id: 'unit9', emoji: '🌍', name: 'Bumi', island: 'Pulau Bumi', color: '#76D7C4', badge: '🌊' },
    { id: 'unit10', emoji: '🤖', name: 'Teknologi', island: 'Pulau Robot', color: '#AEB6BF', badge: '🚀' }
];

// Default state
function createDefaultState() {
    return {
        streak: 0,
        lastLoginDate: null,
        completedUnits: [],   // e.g. ['unit1', 'unit2']
        badges: [],           // e.g. ['🔬', '🛡️']
        quizScores: {},       // e.g. { unit1: { best: 80, attempts: 3 } }
        totalProgress: 0      // 0..100
    };
}

function loadState() {
    try {
        const saved = localStorage.getItem(STATE_KEY);
        if (saved) {
            const parsed = JSON.parse(saved);
            // Merge with defaults for forward-compatibility
            return { ...createDefaultState(), ...parsed };
        }
    } catch (e) { /* corrupted, reset */ }
    return createDefaultState();
}

function saveState(state) {
    localStorage.setItem(STATE_KEY, JSON.stringify(state));
}

// ==========================================
// STREAK
// ==========================================
function checkStreak() {
    const state = loadState();
    const today = new Date().toDateString();

    if (state.lastLoginDate !== today) {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);

        if (state.lastLoginDate === yesterday.toDateString()) {
            state.streak += 1;
        } else if (state.lastLoginDate !== null) {
            state.streak = 1;
        } else {
            state.streak = 1;
        }
        state.lastLoginDate = today;
        saveState(state);
    }
    return state;
}

// ==========================================
// LEVEL UNLOCKING LOGIC
// ==========================================
function isUnitUnlocked(unitId) {
    // Unit 1 always unlocked
    const idx = UNITS.findIndex(u => u.id === unitId);
    if (idx === 0) return true;

    // Previous unit must be completed
    const state = loadState();
    const prevUnit = UNITS[idx - 1];
    return state.completedUnits.includes(prevUnit.id);
}

function getUnitStatus(unitId) {
    const state = loadState();
    if (state.completedUnits.includes(unitId)) return 'completed';
    if (isUnitUnlocked(unitId)) return 'unlocked';
    return 'locked';
}

function completeUnit(unitId) {
    const state = loadState();
    const unitDef = UNITS.find(u => u.id === unitId);

    if (!state.completedUnits.includes(unitId)) {
        state.completedUnits.push(unitId);
    }

    // Award badge
    if (unitDef && unitDef.badge && !state.badges.includes(unitDef.badge)) {
        state.badges.push(unitDef.badge);
    }

    // Recalculate progress
    state.totalProgress = Math.round((state.completedUnits.length / UNITS.length) * 100);

    saveState(state);
    return state;
}

function saveQuizScore(unitId, scorePercent) {
    const state = loadState();
    if (!state.quizScores[unitId]) {
        state.quizScores[unitId] = { best: 0, attempts: 0 };
    }
    state.quizScores[unitId].attempts += 1;
    state.quizScores[unitId].best = Math.max(state.quizScores[unitId].best, scorePercent);
    saveState(state);
}

// ==========================================
// QUIZ DATA GENERATOR
// Uses the existing notes_data (unitNotesData) to auto-generate MCQ
// ==========================================
function generateQuizFromNotes(unitId) {
    if (typeof unitNotesData === 'undefined' || !unitNotesData[unitId]) return [];

    const notes = unitNotesData[unitId];
    const quizzes = [];

    notes.forEach((note, idx) => {
        // Generate an MCQ from the flashcard
        // Question = frontQuestion
        // Correct answer = key phrase from backAnswer
        // Distractors = from other notes' backAnswers

        const correctAnswer = note.backTitle;
        const distractors = notes
            .filter((_, i) => i !== idx)
            .map(n => n.backTitle)
            .sort(() => Math.random() - 0.5)
            .slice(0, 3);

        // If not enough distractors, pad with generic ones
        const genericFills = ['Tidak pasti', 'Semuanya', 'Tiada yang betul'];
        while (distractors.length < 3) {
            distractors.push(genericFills[distractors.length]);
        }

        const options = shuffleArray([correctAnswer, ...distractors]);

        quizzes.push({
            emoji: note.frontEmoji,
            question: note.frontQuestion,
            options: options,
            correctIndex: options.indexOf(correctAnswer),
            explanation: note.backAnswer + (note.trivia ? '\n\n💡 ' + note.trivia : '')
        });
    });

    return shuffleArray(quizzes);
}

function shuffleArray(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

// ==========================================
// PARENT STATS
// ==========================================
function getParentStats() {
    return loadState();
}

function clearAllData() {
    localStorage.removeItem(STATE_KEY);
    location.reload();
}

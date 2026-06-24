let currentScore = 0;
let currentGame = '';
let currentAnswer = null;
let currentExplanation = '';
let canProceed = false;

// Session Variables
let currentQuestionIndex = 0;
const maxQuestions = 15;
let sessionCorrect = 0;

// Audio elements
const audioCorrect = document.getElementById('audio-correct');
const audioWrong = document.getElementById('audio-wrong');

function playSound(type) {
    try {
        if (type === 'correct') {
            audioCorrect.currentTime = 0;
            audioCorrect.play().catch(() => {});
        } else if (type === 'wrong') {
            audioWrong.currentTime = 0;
            audioWrong.play().catch(() => {});
        }
    } catch (e) {}
}

function updateScore() {
    document.getElementById('score-display').innerText = currentScore;
}

function startGame(gameId) {
    currentGame = gameId;
    currentScore = 0;
    currentQuestionIndex = 0;
    sessionCorrect = 0;
    updateScore();
    document.getElementById('main-menu').classList.remove('active');
    document.getElementById('game-screen').classList.add('active');
    
    const titles = {
        'nilai-tempat': 'Nilai Tempat & Digit',
        'banding-nombor': 'Banding Nombor',
        'bundar': 'Bundar Nombor',
        'cerakin': 'Cerakin Nombor',
        'ejaan': 'Ejaan Nombor',
        'darab-bahagi': 'Darab & Bahagi',
        'susun-nombor': 'Susun Nombor',
        'pola-nombor': 'Pola Nombor',
        'tambah': 'Tambah',
        'tolak': 'Tolak',
        'anggar': 'Anggar Nombor'
    };
    document.getElementById('game-title').innerText = titles[gameId];
    
    nextQuestion();
}

function goHome() {
    document.getElementById('game-screen').classList.remove('active');
    document.getElementById('main-menu').classList.add('active');
    document.getElementById('feedback-area').classList.add('hidden');
    updateMenuCards();
}

function nextQuestion() {
    if (currentQuestionIndex >= maxQuestions) {
        endGame();
        return;
    }
    
    currentQuestionIndex++;
    document.getElementById('session-progress').innerText = `Soalan: ${currentQuestionIndex} / ${maxQuestions}`;
    
    document.getElementById('feedback-area').classList.add('hidden');
    const gameArea = document.getElementById('game-area');
    gameArea.innerHTML = '';
    currentExplanation = '';

    if (currentGame === 'nilai-tempat') generateNilaiTempat();
    else if (currentGame === 'banding-nombor') generateBandingNombor();
    else if (currentGame === 'bundar') generateBundar();
    else if (currentGame === 'cerakin') generateCerakin();
    else if (currentGame === 'ejaan') generateEjaan();
    else if (currentGame === 'tolak') generateTolak();
    else if (currentGame === 'darab') generateDarab();
    else if (currentGame === 'bahagi') generateBahagi();
    else if (currentGame === 'susun-nombor') generateSusunNombor();
    else if (currentGame === 'pola-nombor') generatePolaNombor();
    else if (currentGame === 'tambah') generateTambah();
    else if (currentGame === 'tolak') generateTolak();
    else if (currentGame === 'anggar') generateAnggar();
}

// Allow Enter key to proceed to next question when feedback is shown
document.addEventListener('keydown', (e) => {
    const feedbackArea = document.getElementById('feedback-area');
    if (e.key === 'Enter' && feedbackArea && !feedbackArea.classList.contains('hidden') && canProceed) {
        // Pre-empt dashboard modal check
        const dashboard = document.getElementById('dashboard-modal');
        if (!dashboard || dashboard.classList.contains('hidden')) {
            nextQuestion();
        }
    }
});

function generateRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Helper: generate a 3-digit number where all digits are unique AND non-zero (1-9)
function generateUniqueDigitNumber() {
    let num;
    do {
        num = generateRandomNumber(111, 999);
        const s = num.toString();
        var allUnique = s[0] !== s[1] && s[1] !== s[2] && s[0] !== s[2];
        var noZero = !s.includes('0');
    } while (!allUnique || !noZero);
    return num;
}

// Helper: generate a 3-digit number with no zero digits
function generateNonZeroDigitNumber() {
    let num;
    do {
        num = generateRandomNumber(111, 999);
    } while (num.toString().includes('0'));
    return num;
}


// ===========================
// 1. NILAI TEMPAT & DIGIT
// ===========================
function generateNilaiTempat() {
    const num = generateUniqueDigitNumber();
    const numStr = num.toString();
    const position = generateRandomNumber(0, 2);
    const targetDigit = numStr[position];
    
    const isNilaiTempat = Math.random() > 0.5;
    
    const instruction = document.getElementById('game-instruction');
    const questionText = document.createElement('div');
    questionText.className = 'question-text';
    questionText.innerText = num;
    
    let htmlExplanation = `
        <div class="explanation-step">Nombor: <strong>${num}</strong></div>
        <div class="explanation-step">
            <span style="color:var(--primary-color)">Ratus</span>: ${numStr[0]} | 
            <span style="color:var(--success-color)">Puluh</span>: ${numStr[1]} | 
            <span style="color:var(--danger-color)">Sa</span>: ${numStr[2]}
        </div>
    `;
    
    if (isNilaiTempat) {
        instruction.innerText = `Apakah NILAI TEMPAT bagi digit ${targetDigit} dalam nombor di bawah?`;
        currentAnswer = position === 0 ? 'ratus' : (position === 1 ? 'puluh' : 'sa');
        
        currentExplanation = htmlExplanation + `
            <div class="explanation-step" style="margin-top:0.5rem">
                Digit <strong>${targetDigit}</strong> berada di tempat <strong>${currentAnswer.toUpperCase()}</strong>.
            </div>
        `;
        
        const options = shuffleArray(['ratus', 'puluh', 'sa']);
        document.getElementById('game-area').appendChild(questionText);
        renderOptions(options);
    } else {
        instruction.innerText = `Apakah NILAI DIGIT bagi digit ${targetDigit} dalam nombor di bawah?`;
        let answerVal = parseInt(targetDigit);
        let place = '';
        if (position === 0) { answerVal *= 100; place = 'ratus'; }
        else if (position === 1) { answerVal *= 10; place = 'puluh'; }
        else { place = 'sa'; }
        
        currentAnswer = answerVal.toString();
        
        currentExplanation = htmlExplanation + `
            <div class="explanation-step" style="margin-top:0.5rem">
                Digit <strong>${targetDigit}</strong> berada di tempat <strong>${place}</strong>.<br>
                Oleh itu, nilainya ialah <strong>${currentAnswer}</strong>.
            </div>
        `;
        
        let wrongOptions = new Set();
        wrongOptions.add(currentAnswer);
        [1, 10, 100].forEach(mult => {
            wrongOptions.add((parseInt(targetDigit) * mult).toString());
        });
        wrongOptions.delete(currentAnswer);
        let wrongs = Array.from(wrongOptions).slice(0, 2);
        while (wrongs.length < 2) {
            let fallback = generateRandomNumber(1, 9) * [1, 10, 100][generateRandomNumber(0, 2)];
            if (fallback.toString() !== currentAnswer && !wrongs.includes(fallback.toString())) {
                wrongs.push(fallback.toString());
            }
        }
        
        let options = shuffleArray([currentAnswer, ...wrongs]);
        document.getElementById('game-area').appendChild(questionText);
        renderOptions(options);
    }
}

// ===========================
// 2. BANDING NOMBOR
// ===========================
function generateBandingNombor() {
    const isBesar = Math.random() > 0.5;
    document.getElementById('game-instruction').innerText = isBesar ? 'Pilih nombor yang paling BESAR' : 'Pilih nombor yang paling KECIL';
    
    let n1 = generateRandomNumber(100, 999);
    let n2 = generateRandomNumber(100, 999);
    while (n1 === n2) n2 = generateRandomNumber(100, 999);
    
    currentAnswer = isBesar ? Math.max(n1, n2).toString() : Math.min(n1, n2).toString();
    
    let s1 = n1.toString();
    let s2 = n2.toString();
    let compareStep = '';
    
    if (s1[0] !== s2[0]) {
        compareStep = `Bandingkan nilai <strong>ratus</strong>: ${s1[0]} ratus lawan ${s2[0]} ratus.`;
    } else if (s1[1] !== s2[1]) {
        compareStep = `Nilai ratus sama (${s1[0]}). Bandingkan nilai <strong>puluh</strong>: ${s1[1]} puluh lawan ${s2[1]} puluh.`;
    } else {
        compareStep = `Nilai ratus dan puluh sama. Bandingkan nilai <strong>sa</strong>: ${s1[2]} sa lawan ${s2[2]} sa.`;
    }
    
    currentExplanation = `
        <div class="explanation-step">Nombor: <strong>${n1}</strong> dan <strong>${n2}</strong></div>
        <div class="explanation-step">${compareStep}</div>
        <div class="explanation-step" style="margin-top:0.5rem">
            Nombor yang lebih ${isBesar ? 'besar' : 'kecil'} ialah <strong>${currentAnswer}</strong>.
        </div>
    `;
    
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'compare-container';
    
    let options = shuffleArray([n1.toString(), n2.toString()]);
    options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'option-btn compare-btn';
        btn.innerText = opt;
        btn.onclick = () => checkAnswer(opt, btn);
        optionsContainer.appendChild(btn);
    });
    
    document.getElementById('game-area').appendChild(optionsContainer);
}


// ===========================
// 3. BUNDAR NOMBOR
// ===========================
function generateBundar() {
    const isRatus = Math.random() > 0.5;
    const num = isRatus ? generateRandomNumber(150, 850) : generateRandomNumber(115, 985);
    
    document.getElementById('game-instruction').innerText = isRatus ? 'Bundarkan kepada RATUS terdekat' : 'Bundarkan kepada PULUH terdekat';
    
    const questionText = document.createElement('div');
    questionText.className = 'question-text';
    questionText.innerText = num;
    document.getElementById('game-area').appendChild(questionText);
    
    let ans;
    if (isRatus) {
        ans = Math.round(num / 100) * 100;
    } else {
        ans = Math.round(num / 10) * 10;
    }
    currentAnswer = ans.toString();
    
    let tensOrHundreds = isRatus ? 'RATUS' : 'PULUH';
    let numStrForRound = num.toString();
    let roundingDigit = isRatus ? numStrForRound[1] : numStrForRound[2];
    let rule = parseInt(roundingDigit) >= 5 ? 'tambah 1 ke sebelah kiri' : 'kekal sifar';
    currentExplanation = `
        <div class="explanation-step">Nombor: <strong>${num}</strong></div>
        <div class="explanation-step">Bundar kepada ${tensOrHundreds} terdekat: Lihat digit jiran di sebelah kanan iaitu <strong>${roundingDigit}</strong>.</div>
        <div class="explanation-step">Jika 0-4, nilai kekal. Jika 5-9, tambah 1.</div>
        <div class="explanation-step">Oleh kerana digit jiran ialah ${roundingDigit}, kita <strong>${rule}</strong>.</div>
        <div class="explanation-step" style="margin-top:0.5rem">Jawapannya ialah <strong>${currentAnswer}</strong>.</div>
    `;
    
    let wrong1, wrong2;
    if (isRatus) {
        wrong1 = ans + 100;
        wrong2 = ans - 100;
    } else {
        wrong1 = ans + 10;
        wrong2 = ans - 10;
    }
    if (wrong2 < 0) wrong2 = 0;
    if (wrong1 > 1000) wrong1 = ans - (isRatus ? 200 : 20);
    
    let options = shuffleArray([currentAnswer, wrong1.toString(), wrong2.toString()]);
    renderOptions(options);
}


// ===========================
// 4. CERAKIN NOMBOR
// ===========================
function generateCerakin() {
    const num = generateNonZeroDigitNumber();
    const numStr = num.toString();
    const isNilaiTempat = Math.random() > 0.5;
    
    document.getElementById('game-instruction').innerText = isNilaiTempat
        ? 'Cerakinkan mengikut NILAI TEMPAT (digit sahaja)'
        : 'Cerakinkan mengikut NILAI DIGIT (nilai penuh)';
    
    const questionText = document.createElement('div');
    questionText.className = 'question-text';
    questionText.innerText = num;
    document.getElementById('game-area').appendChild(questionText);
    
    const cerakinContainer = document.createElement('div');
    cerakinContainer.className = 'cerakin-inputs';
    
    if (isNilaiTempat) {
        currentAnswer = [numStr[0], numStr[1], numStr[2]];
        const labels = [' ratus', ' puluh', ' sa'];
        
        for (let i = 0; i < 3; i++) {
            if (i > 0) {
                let plus = document.createElement('span');
                plus.innerText = ' + ';
                cerakinContainer.appendChild(plus);
            }
            let input = document.createElement('input');
            input.type = 'text';
            input.className = 'cerakin-input';
            input.id = 'cerakin-' + i;
            input.maxLength = 1;
            input.inputMode = 'numeric';
            cerakinContainer.appendChild(input);
            
            let label = document.createElement('span');
            label.innerText = labels[i];
            cerakinContainer.appendChild(label);
        }
    } else {
        currentAnswer = [
            (parseInt(numStr[0]) * 100).toString(),
            (parseInt(numStr[1]) * 10).toString(),
            numStr[2]
        ];
        
        for (let i = 0; i < 3; i++) {
            if (i > 0) {
                let plus = document.createElement('span');
                plus.innerText = ' + ';
                cerakinContainer.appendChild(plus);
            }
            let input = document.createElement('input');
            input.type = 'text';
            input.className = 'cerakin-input';
            input.id = 'cerakin-' + i;
            input.inputMode = 'numeric';
            input.style.width = i === 0 ? '100px' : (i === 1 ? '80px' : '60px');
            cerakinContainer.appendChild(input);
        }
    }
    
    document.getElementById('game-area').appendChild(cerakinContainer);
    
    const hintText = document.createElement('p');
    hintText.style.color = 'var(--text-light)';
    hintText.style.marginTop = '1rem';
    hintText.style.fontSize = '0.9rem';
    hintText.innerText = isNilaiTempat ? 'Contoh: 456 = 4 ratus + 5 puluh + 6 sa' : 'Contoh: 456 = 400 + 50 + 6';
    document.getElementById('game-area').appendChild(hintText);
    
    const submitBtn = document.createElement('button');
    submitBtn.className = 'btn-primary';
    submitBtn.style.marginTop = '1.5rem';
    submitBtn.innerText = 'Semak Jawapan ✓';
    submitBtn.onclick = () => {
        let a = document.getElementById('cerakin-0').value.trim();
        let b = document.getElementById('cerakin-1').value.trim();
        let c = document.getElementById('cerakin-2').value.trim();
        
        if (a === '' || b === '' || c === '') {
            submitBtn.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => submitBtn.style.animation = '', 500);
            return;
        }
        
        currentExplanation = `
            <div class="explanation-step">Nombor: <strong>${num}</strong></div>
            <div class="explanation-step">Pecahkan ikut ${isNilaiTempat ? 'Nilai Tempat' : 'Nilai Digit'}:</div>
            <div class="explanation-step" style="color:var(--primary-color)">Ratus: <strong>${currentAnswer[0]}</strong></div>
            <div class="explanation-step" style="color:var(--success-color)">Puluh: <strong>${currentAnswer[1]}</strong></div>
            <div class="explanation-step" style="color:var(--danger-color)">Sa: <strong>${currentAnswer[2]}</strong></div>
        `;
        
        if (a === currentAnswer[0] && b === currentAnswer[1] && c === currentAnswer[2]) {
            showFeedback(true, '', currentExplanation);
        } else {
            showFeedback(false, `Jawapan betul: ${currentAnswer[0]} + ${currentAnswer[1]} + ${currentAnswer[2]}`, currentExplanation);
        }
    };
    document.getElementById('game-area').appendChild(submitBtn);
}


// ===========================
// 5. EJAAN NOMBOR
// ===========================
const ones = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'lapan', 'sembilan'];
const belas = ['sepuluh', 'sebelas', 'dua belas', 'tiga belas', 'empat belas', 'lima belas', 'enam belas', 'tujuh belas', 'lapan belas', 'sembilan belas'];

function numberToWords(num) {
    if (num === 0) return 'sifar';
    let words = '';
    
    let r = Math.floor(num / 100);
    let rem = num % 100;
    
    if (r > 0) {
        if (r === 1) words += 'seratus ';
        else words += ones[r] + ' ratus ';
    }
    
    if (rem > 0) {
        if (rem < 10) {
            words += ones[rem];
        } else if (rem < 20) {
            words += belas[rem - 10];
        } else {
            let p = Math.floor(rem / 10);
            let s = rem % 10;
            words += ones[p] + ' puluh ';
            if (s > 0) words += ones[s];
        }
    }
    return words.trim();
}

function generateEjaan() {
    const num = generateRandomNumber(100, 999);
    const isAngkaKePerkataan = Math.random() > 0.5;
    const numWords = numberToWords(num);
    
    document.getElementById('game-instruction').innerText = isAngkaKePerkataan
        ? 'Pilih ejaan yang betul bagi nombor ini'
        : 'Pilih angka yang betul bagi ejaan ini';
    
    const questionText = document.createElement('div');
    questionText.className = 'question-text';
    
    if (isAngkaKePerkataan) {
        questionText.innerText = num;
        currentAnswer = numWords;
        
        let wrongSet = new Set();
        wrongSet.add(numWords);
        while (wrongSet.size < 3) {
            wrongSet.add(numberToWords(generateRandomNumber(100, 999)));
        }
        wrongSet.delete(numWords);
        let wrongs = Array.from(wrongSet).slice(0, 2);
        
        let options = shuffleArray([currentAnswer, ...wrongs]);
        document.getElementById('game-area').appendChild(questionText);
        
        currentExplanation = `
            <div class="explanation-step">Nombor: <strong>${num}</strong></div>
            <div class="explanation-step">Sebut nilai ratus: <strong>${numberToWords(Math.floor(num/100)*100)}</strong></div>
            <div class="explanation-step">Sebut nilai puluh & sa: <strong>${numberToWords(num%100) || 'sifar'}</strong></div>
            <div class="explanation-step" style="margin-top:0.5rem">Ejaan penuh: <strong>${numWords}</strong></div>
        `;
        
        renderOptions(options, true);
    } else {
        questionText.innerText = numWords;
        questionText.style.fontSize = '1.8rem';
        currentAnswer = num.toString();
        
        let wrongSet = new Set();
        wrongSet.add(num);
        const digits = num.toString().split('');
        wrongSet.add(parseInt(digits[0] + digits[2] + digits[1]));
        wrongSet.add(parseInt(digits[1] + digits[0] + digits[2]));
        wrongSet.add(num + generateRandomNumber(1, 20));
        wrongSet.add(num - generateRandomNumber(1, 20));
        
        wrongSet.delete(num);
        let wrongs = Array.from(wrongSet).filter(n => n >= 100 && n <= 999).slice(0, 2);
        while (wrongs.length < 2) {
            let w = generateRandomNumber(100, 999);
            if (w !== num && !wrongs.includes(w)) wrongs.push(w);
        }
        
        let options = shuffleArray([currentAnswer, ...wrongs.map(w => w.toString())]);
        document.getElementById('game-area').appendChild(questionText);
        
        currentExplanation = `
            <div class="explanation-step">Ejaan: <strong>${numWords}</strong></div>
            <div class="explanation-step">Gabungkan nilai digit menjadi angka: <strong>${num}</strong>.</div>
        `;
        
        renderOptions(options);
    }
}


// ===========================
// 6. DARAB
// ===========================
function generateDarab() {
    document.getElementById('game-instruction').innerText = 'Selesaikan operasi darab';
    const sifir = [2, 3, 4, 5, 10];
    let n1 = sifir[generateRandomNumber(0, sifir.length - 1)];
    let n2 = generateRandomNumber(1, 9);
    let ans = n1 * n2;
    document.getElementById('game-area').innerHTML = `<div class="question-text">${n2} &times; ${n1} = ?</div>`;
    
    currentAnswer = ans.toString();
    
    let wrongSet = new Set();
    wrongSet.add(ans);
    wrongSet.add(ans + generateRandomNumber(1, 3));
    wrongSet.add(Math.max(0, ans - generateRandomNumber(1, 3)));
    wrongSet.add(ans + generateRandomNumber(4, 7));
    wrongSet.delete(ans);
    let wrongs = Array.from(wrongSet).filter(n => n >= 0).slice(0, 2);
    
    let options = shuffleArray([currentAnswer, ...wrongs.map(w => w.toString())]);
    
    currentExplanation = `
        <div class="explanation-step">Darab ialah tambah berulang.</div>
        <div class="explanation-step">${n2} &times; ${n1} bermaksud <strong>${n2} kumpulan ${n1}</strong>.</div>
        <div class="explanation-step">${Array(n2).fill(n1).join(' + ')} = <strong>${ans}</strong></div>
    `;
    
    renderOptions(options);
}

// ===========================
// 6.1 BAHAGI
// ===========================
function generateBahagi() {
    document.getElementById('game-instruction').innerText = 'Selesaikan operasi bahagi';
    const sifir = [2, 3, 4, 5, 10];
    let n2 = sifir[generateRandomNumber(0, sifir.length - 1)];
    let n = generateRandomNumber(1, 9);
    let n1 = n * n2;
    let ans = n;
    document.getElementById('game-area').innerHTML = `<div class="question-text">${n1} &divide; ${n2} = ?</div>`;
    
    currentAnswer = ans.toString();
    
    let wrongSet = new Set();
    wrongSet.add(ans);
    wrongSet.add(ans + generateRandomNumber(1, 3));
    wrongSet.add(Math.max(0, ans - generateRandomNumber(1, 3)));
    wrongSet.add(ans + generateRandomNumber(4, 7));
    wrongSet.delete(ans);
    let wrongs = Array.from(wrongSet).filter(n => n >= 0).slice(0, 2);
    
    let options = shuffleArray([currentAnswer, ...wrongs.map(w => w.toString())]);
    
    currentExplanation = `
        <div class="explanation-step">Bahagi berkait rapat dengan darab.</div>
        <div class="explanation-step">${n1} &divide; ${n2} bermaksud: Berapa darab ${n2} dapat ${n1}?</div>
        <div class="explanation-step">Oleh kerana <strong>${ans}</strong> &times; ${n2} = ${n1}, maka jawapannya ialah <strong>${ans}</strong>.</div>
    `;
    
    renderOptions(options);
}


// ===========================
// 7. SUSUN NOMBOR (NEW)
// ===========================
function generateSusunNombor() {
    const isMenaik = Math.random() > 0.5;
    document.getElementById('game-instruction').innerText = isMenaik
        ? 'Klik nombor mengikut tertib MENAIK (kecil ke besar)'
        : 'Klik nombor mengikut tertib MENURUN (besar ke kecil)';
    
    // Generate 5 unique random numbers
    let numbers = new Set();
    while (numbers.size < 5) {
        numbers.add(generateRandomNumber(100, 999));
    }
    numbers = Array.from(numbers);
    
    // The correct order
    const sorted = [...numbers].sort((a, b) => isMenaik ? a - b : b - a);
    currentAnswer = sorted.map(n => n.toString());
    
    // Track user selections
    let userOrder = [];
    
    // Shuffle for display
    const shuffled = shuffleArray([...numbers]);
    
    // Source buttons
    const sourceDiv = document.createElement('div');
    sourceDiv.className = 'susun-source';
    sourceDiv.id = 'susun-source';
    
    shuffled.forEach(num => {
        const btn = document.createElement('button');
        btn.className = 'susun-btn';
        btn.innerText = num;
        btn.dataset.value = num;
        btn.onclick = () => {
            userOrder.push(num.toString());
            btn.classList.add('used');
            
            // Add to target
            const targetDiv = document.getElementById('susun-target');
            if (targetDiv.children.length > 0) {
                const arrow = document.createElement('span');
                arrow.className = 'susun-arrow';
                arrow.innerHTML = '&rarr;';
                targetDiv.appendChild(arrow);
            }
            const placed = document.createElement('span');
            placed.className = 'susun-placed';
            placed.innerText = num;
            targetDiv.appendChild(placed);
            
            // Check if all placed
            if (userOrder.length === 5) {
                const isCorrect = userOrder.every((val, idx) => val === currentAnswer[idx]);
                
                currentExplanation = `
                    <div class="explanation-step">Untuk menyusun secara <strong>${isMenaik ? 'MENAIK' : 'MENURUN'}</strong>, kita susun dari nilai paling ${isMenaik ? 'kecil' : 'besar'} ke paling ${isMenaik ? 'besar' : 'kecil'}.</div>
                    <div class="explanation-step">Bandingkan nilai ratus, kemudian puluh, kemudian sa.</div>
                    <div class="explanation-step" style="margin-top:0.5rem">Susunan yang betul:</div>
                    <div class="explanation-step" style="font-size:1.3rem; font-weight:800; color:var(--primary-color)">${currentAnswer.join(' &rarr; ')}</div>
                `;
                
                setTimeout(() => showFeedback(isCorrect, isCorrect ? '' : `Tertib betul: ${currentAnswer.join(' → ')}`, currentExplanation), 500);
            }
        };
        sourceDiv.appendChild(btn);
    });
    
    // Target area
    const targetDiv = document.createElement('div');
    targetDiv.className = 'susun-target';
    targetDiv.id = 'susun-target';
    
    const label = document.createElement('span');
    label.style.color = 'var(--text-light)';
    label.style.fontSize = '0.9rem';
    label.innerText = isMenaik ? '← kecil ... besar →' : '← besar ... kecil →';
    targetDiv.appendChild(label);
    
    document.getElementById('game-area').appendChild(sourceDiv);
    document.getElementById('game-area').appendChild(targetDiv);
    
    // Reset button
    const resetBtn = document.createElement('button');
    resetBtn.className = 'btn-primary';
    resetBtn.style.marginTop = '1rem';
    resetBtn.style.background = 'var(--text-light)';
    resetBtn.style.boxShadow = 'none';
    resetBtn.style.fontSize = '0.9rem';
    resetBtn.style.padding = '0.5rem 1.5rem';
    resetBtn.innerText = '↺ Mula Semula';
    resetBtn.onclick = () => {
        userOrder = [];
        document.querySelectorAll('.susun-btn').forEach(b => b.classList.remove('used'));
        const t = document.getElementById('susun-target');
        t.innerHTML = '';
        const lbl = document.createElement('span');
        lbl.style.color = 'var(--text-light)';
        lbl.style.fontSize = '0.9rem';
        lbl.innerText = isMenaik ? '← kecil ... besar →' : '← besar ... kecil →';
        t.appendChild(lbl);
    };
    document.getElementById('game-area').appendChild(resetBtn);
}


// ===========================
// 8. POLA NOMBOR
// ===========================

// All available patterns
const allPatterns = [
    { step: 1, label: 'Menaik satu-satu (+1)' },
    { step: 2, label: 'Menaik dua-dua (+2)' },
    { step: 3, label: 'Menaik tiga-tiga (+3)' },
    { step: 5, label: 'Menaik lima-lima (+5)' },
    { step: 10, label: 'Menaik sepuluh-sepuluh (+10)' },
    { step: -1, label: 'Menurun satu-satu (-1)' },
    { step: -2, label: 'Menurun dua-dua (-2)' },
    { step: -3, label: 'Menurun tiga-tiga (-3)' },
    { step: -5, label: 'Menurun lima-lima (-5)' },
    { step: -10, label: 'Menurun sepuluh-sepuluh (-10)' }
];

function generatePolaNombor() {
    // Randomly pick Jenis A or Jenis B
    const isJenisA = Math.random() > 0.5;
    
    // Pick a random pattern
    const patternIdx = generateRandomNumber(0, allPatterns.length - 1);
    const pattern = allPatterns[patternIdx];
    
    // Generate starting number
    let start;
    if (pattern.step > 0) {
        start = generateRandomNumber(100, 500);
    } else {
        start = generateRandomNumber(500, 900);
    }
    
    // Generate sequence of 6 numbers
    const sequence = [];
    for (let i = 0; i < 6; i++) {
        sequence.push(start + (pattern.step * i));
    }
    
    if (isJenisA) {
        generatePolaJenisA(sequence, pattern);
    } else {
        generatePolaJenisB(sequence, pattern);
    }
}

// Jenis A: Isi nombor kosong sahaja
function generatePolaJenisA(sequence, pattern) {
    document.getElementById('game-instruction').innerText = 'Lengkapkan nombor yang kosong dalam rangkaian ini';
    
    const blankPositions = [4, 5];
    
    const seqDiv = document.createElement('div');
    seqDiv.className = 'pola-sequence';
    
    sequence.forEach((num, idx) => {
        if (idx > 0) {
            const arrow = document.createElement('span');
            arrow.className = 'pola-arrow';
            arrow.innerHTML = '→';
            seqDiv.appendChild(arrow);
        }
        
        if (blankPositions.includes(idx)) {
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'pola-blank';
            input.id = 'pola-' + idx;
            input.inputMode = 'numeric';
            seqDiv.appendChild(input);
        } else {
            const span = document.createElement('span');
            span.className = 'pola-num';
            span.innerText = num;
            seqDiv.appendChild(span);
        }
    });
    
    document.getElementById('game-area').appendChild(seqDiv);
    
    currentAnswer = {
        type: 'blanks',
        nums: [sequence[4].toString(), sequence[5].toString()]
    };
    
    const submitBtn = document.createElement('button');
    submitBtn.className = 'btn-primary';
    submitBtn.style.marginTop = '1.5rem';
    submitBtn.innerText = 'Semak Jawapan ✓';
    submitBtn.onclick = () => {
        const a4 = document.getElementById('pola-4').value.trim();
        const a5 = document.getElementById('pola-5').value.trim();
        
        if (a4 === '' || a5 === '') {
            submitBtn.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => submitBtn.style.animation = '', 500);
            return;
        }
        
        currentExplanation = `
            <div class="explanation-step">Untuk cari pola, tolak dua nombor yang bersebelahan:</div>
            <div class="explanation-step">${Math.max(sequence[0], sequence[1])} − ${Math.min(sequence[0], sequence[1])} = ${Math.abs(pattern.step)}</div>
            <div class="explanation-step">Oleh kerana nombor semakin ${pattern.step > 0 ? 'besar' : 'kecil'}, polanya ialah <strong>${pattern.label}</strong>.</div>
        `;
        
        if (a4 === currentAnswer.nums[0] && a5 === currentAnswer.nums[1]) {
            showFeedback(true, '', currentExplanation);
        } else {
            showFeedback(false, `Jawapan betul: ${currentAnswer.nums[0]} dan ${currentAnswer.nums[1]}`, currentExplanation);
        }
    };
    document.getElementById('game-area').appendChild(submitBtn);
}

// Jenis B: Semua nombor ditunjukkan, pilih pola dari 4 pilihan
function generatePolaJenisB(sequence, pattern) {
    document.getElementById('game-instruction').innerText = 'Apakah pola bagi rangkaian nombor ini?';
    
    const seqDiv = document.createElement('div');
    seqDiv.className = 'pola-sequence';
    
    sequence.forEach((num, idx) => {
        if (idx > 0) {
            const arrow = document.createElement('span');
            arrow.className = 'pola-arrow';
            arrow.innerHTML = '→';
            seqDiv.appendChild(arrow);
        }
        const span = document.createElement('span');
        span.className = 'pola-num';
        span.innerText = num;
        seqDiv.appendChild(span);
    });
    
    document.getElementById('game-area').appendChild(seqDiv);
    
    // Build 4 unique options including the correct one
    currentAnswer = pattern.label;
    
    let wrongSet = new Set();
    wrongSet.add(pattern.label);
    while (wrongSet.size < 4) {
        const rIdx = generateRandomNumber(0, allPatterns.length - 1);
        wrongSet.add(allPatterns[rIdx].label);
    }
    wrongSet.delete(pattern.label);
    let wrongs = Array.from(wrongSet).slice(0, 3);
    
    let options = shuffleArray([currentAnswer, ...wrongs]);
    
    currentExplanation = `
        <div class="explanation-step">Tolak dua nombor yang bersebelahan:</div>
        <div class="explanation-step">${Math.max(sequence[0], sequence[1])} − ${Math.min(sequence[0], sequence[1])} = ${Math.abs(pattern.step)}</div>
        <div class="explanation-step">Oleh kerana nombor semakin ${pattern.step > 0 ? 'besar' : 'kecil'}, polanya ialah <strong>${pattern.label}</strong>.</div>
    `;
    
    renderOptions(options, true);
}


// ===========================
// 9. TAMBAH (NEW)
// ===========================
function generateTambah() {
    // Mix of 2-number and 3-number addition
    const isThreeNumbers = Math.random() > 0.6;
    
    if (isThreeNumbers) {
        document.getElementById('game-instruction').innerText = 'Selesaikan operasi tambah tiga nombor';
        const a = generateRandomNumber(100, 300);
        const b = generateRandomNumber(100, 300);
        const c = generateRandomNumber(10, 200);
        const ans = a + b + c;
        currentAnswer = ans.toString();
        
        const mathDiv = document.createElement('div');
        mathDiv.className = 'math-vertical';
        mathDiv.innerHTML = `
            <div class="math-row"><span>${formatNum(a)}</span></div>
            <div class="math-row"><span>${formatNum(b)}</span></div>
            <div class="math-row"><span class="math-operator">+</span> <span>${formatNum(c)}</span></div>
            <div class="math-line"></div>
        `;
        document.getElementById('game-area').appendChild(mathDiv);
        
        currentExplanation = `
            <div class="explanation-step">Kira dalam bentuk lazim dari <strong>sa</strong>, kemudian <strong>puluh</strong>, hingga <strong>ratus</strong>.</div>
            <div class="explanation-step">Tambahkan digit bagi setiap nilai tempat untuk ketiga-tiga nombor.</div>
            <div class="explanation-step">Jika hasil tambah bagi sesuatu lajur lebih dari 9, kumpul semula (bawa naik ke lajur sebelah kiri).</div>
            <div class="explanation-step" style="margin-top:0.5rem">Jawapan sebenar ialah <strong>${currentAnswer}</strong>.</div>
        `;
    } else {
        document.getElementById('game-instruction').innerText = 'Selesaikan operasi tambah';
        const a = generateRandomNumber(100, 500);
        const b = generateRandomNumber(100, 499);
        const ans = a + b;
        currentAnswer = ans.toString();
        
        const mathDiv = document.createElement('div');
        mathDiv.className = 'math-vertical';
        mathDiv.innerHTML = `
            <div class="math-row"><span>${formatNum(a)}</span></div>
            <div class="math-row"><span class="math-operator">+</span> <span>${formatNum(b)}</span></div>
            <div class="math-line"></div>
        `;
        document.getElementById('game-area').appendChild(mathDiv);
        
        currentExplanation = `
            <div class="explanation-step">Kira dalam bentuk lazim dari <strong>sa</strong>, kemudian <strong>puluh</strong>, hingga <strong>ratus</strong>.</div>
            <div class="explanation-step">Tambahkan digit bagi setiap nilai tempat.</div>
            <div class="explanation-step">Jika hasil lebih dari 9, kumpul semula (bawa 1 ke rumah sebelah kiri).</div>
            <div class="explanation-step" style="margin-top:0.5rem">Jawapan sebenar ialah <strong>${currentAnswer}</strong>.</div>
        `;
    }
    
    renderMathInput();
}


// ===========================
// 10. TOLAK (NEW)
// ===========================
function generateTolak() {
    const isBerturut = Math.random() > 0.7;
    
    if (isBerturut) {
        document.getElementById('game-instruction').innerText = 'Selesaikan operasi tolak berturut-turut';
        const a = generateRandomNumber(500, 999);
        const b = generateRandomNumber(100, 200);
        const c = generateRandomNumber(10, 100);
        const ans = a - b - c;
        currentAnswer = ans.toString();
        
        const mathDiv = document.createElement('div');
        mathDiv.className = 'math-vertical';
        mathDiv.innerHTML = `
            <div class="math-row"><span>${formatNum(a)}</span></div>
            <div class="math-row"><span class="math-operator">−</span> <span>${formatNum(b)}</span></div>
            <div class="math-row"><span class="math-operator">−</span> <span>${formatNum(c)}</span></div>
            <div class="math-line"></div>
        `;
        document.getElementById('game-area').appendChild(mathDiv);
        
        currentExplanation = `
            <div class="explanation-step">Kira dalam bentuk lazim dari <strong>sa</strong>, kemudian <strong>puluh</strong>, hingga <strong>ratus</strong>.</div>
            <div class="explanation-step">Tolak nombor kedua dahulu, dapatkan jawapan, kemudian tolak pula nombor ketiga.</div>
            <div class="explanation-step">Jika nombor di atas lebih kecil dari nombor di bawah, pinjam dari rumah di sebelah kirinya.</div>
            <div class="explanation-step" style="margin-top:0.5rem">Jawapan sebenar ialah <strong>${currentAnswer}</strong>.</div>
        `;
    } else {
        document.getElementById('game-instruction').innerText = 'Selesaikan operasi tolak';
        const a = generateRandomNumber(300, 999);
        const b = generateRandomNumber(100, a - 1);
        const ans = a - b;
        currentAnswer = ans.toString();
        
        const mathDiv = document.createElement('div');
        mathDiv.className = 'math-vertical';
        mathDiv.innerHTML = `
            <div class="math-row"><span>${formatNum(a)}</span></div>
            <div class="math-row"><span class="math-operator">−</span> <span>${formatNum(b)}</span></div>
            <div class="math-line"></div>
        `;
        document.getElementById('game-area').appendChild(mathDiv);
        
        currentExplanation = `
            <div class="explanation-step">Kira dalam bentuk lazim dari <strong>sa</strong>, kemudian <strong>puluh</strong>, hingga <strong>ratus</strong>.</div>
            <div class="explanation-step">Jika digit di atas lebih kecil dari digit di bawah, pinjam dari rumah di sebelah kirinya.</div>
            <div class="explanation-step" style="margin-top:0.5rem">Jawapan sebenar ialah <strong>${currentAnswer}</strong>.</div>
        `;
    }
    
    renderMathInput();
}


// ===========================
// 11. ANGGAR NOMBOR (NEW)
// ===========================
// ===========================
// 11. ANGGAR NOMBOR (NEW)
// ===========================
function generateAnggar() {
    document.getElementById('game-instruction').innerText = 'Anggarkan bilangan objek di dalam bekas B';
    
    const scenarios = [
        { full: 100, half: 50, quarter: 25 },
        { full: 200, half: 100, quarter: 50 },
        { full: 40, half: 20, quarter: 10 },
        { full: 80, half: 40, quarter: 20 },
        { full: 500, half: 250, quarter: null }
    ];
    
    const sc = scenarios[generateRandomNumber(0, scenarios.length - 1)];
    const isHalf = sc.quarter === null ? true : Math.random() > 0.5;
    
    const ans = isHalf ? sc.half : sc.quarter;
    const heightPercent = isHalf ? 50 : 25;
    
    const container = document.createElement('div');
    container.className = 'anggar-container';
    
    // Jar A
    const jarA = document.createElement('div');
    jarA.className = 'anggar-jar-wrapper';
    jarA.innerHTML = `
        <div class="anggar-jar">
            <div class="anggar-fill" style="height: 100%;"></div>
            <div class="anggar-jar-label">A</div>
        </div>
        <div class="anggar-qty">${sc.full} biji</div>
    `;
    
    // Jar B
    const jarB = document.createElement('div');
    jarB.className = 'anggar-jar-wrapper';
    jarB.innerHTML = `
        <div class="anggar-jar">
            <div class="anggar-fill" style="height: ${heightPercent}%;"></div>
            <div class="anggar-jar-label" style="color: ${heightPercent < 30 ? 'var(--text-main)' : 'white'};">B</div>
        </div>
        <div class="anggar-qty">?</div>
    `;
    
    container.appendChild(jarA);
    container.appendChild(jarB);
    document.getElementById('game-area').appendChild(container);
    
    currentAnswer = 'Lebih kurang ' + ans.toString();
    
    // Generate wrong options
    let wrongSet = new Set();
    wrongSet.add(ans);
    
    if (isHalf) {
        if (sc.quarter) wrongSet.add(sc.quarter);
        wrongSet.add(ans + 20);
    } else {
        wrongSet.add(sc.half);
        wrongSet.add(ans + 15);
    }
    
    while(wrongSet.size < 3) {
        let w = ans + (generateRandomNumber(1, 4) * 10 * (Math.random() > 0.5 ? 1 : -1));
        if(w > 0 && w !== sc.full && !wrongSet.has(w)) wrongSet.add(w);
    }
    
    wrongSet.delete(ans);
    let wrongs = Array.from(wrongSet).slice(0, 2);
    
    let options = shuffleArray([
        currentAnswer, 
        'Lebih kurang ' + wrongs[0], 
        'Lebih kurang ' + wrongs[1]
    ]);
    
    currentExplanation = `
        <div class="explanation-step">Lihat Bekas A. Kuantiti penuh ialah <strong>${sc.full}</strong>.</div>
        <div class="explanation-step">Bekas B nampak lebih kurang <strong>${isHalf ? 'separuh' : 'suku'}</strong> daripada Bekas A.</div>
        <div class="explanation-step">Oleh itu, anggaran yang munasabah ialah <strong>${currentAnswer}</strong>.</div>
    `;
    
    renderOptions(options, true);
}


// ===========================
// UTILS & FEEDBACK
// ===========================

function formatNum(n) {
    return n.toString().split('').join(' ');
}

function renderMathInput() {
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'math-answer-input';
    input.id = 'math-answer';
    input.inputMode = 'numeric';
    input.placeholder = '?';
    document.getElementById('game-area').appendChild(input);
    
    const submitBtn = document.createElement('button');
    submitBtn.className = 'btn-primary';
    submitBtn.style.marginTop = '1.5rem';
    submitBtn.innerText = 'Semak Jawapan ✓';
    submitBtn.onclick = () => {
        const val = document.getElementById('math-answer').value.trim();
        if (val === '') {
            submitBtn.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => submitBtn.style.animation = '', 500);
            return;
        }
        if (val === currentAnswer) {
            showFeedback(true, '', currentExplanation);
        } else {
            showFeedback(false, `Jawapan betul: ${currentAnswer}`, currentExplanation);
        }
    };
    document.getElementById('game-area').appendChild(submitBtn);
    
    // Allow Enter key
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') submitBtn.click();
    });
    
    input.focus();
}

function renderOptions(options, blockStyle = false) {
    const container = document.createElement('div');
    container.className = 'options-container';
    if (blockStyle) {
        container.style.flexDirection = 'column';
        container.style.alignItems = 'center';
    }
    
    options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        if (blockStyle) btn.style.width = '80%';
        btn.innerText = opt;
        btn.onclick = () => checkAnswer(opt, btn);
        container.appendChild(btn);
    });
    
    document.getElementById('game-area').appendChild(container);
}

function checkAnswer(selected, btnElement) {
    const btns = document.querySelectorAll('.option-btn');
    btns.forEach(b => b.style.pointerEvents = 'none');
    
    if (selected === currentAnswer) {
        btnElement.classList.add('correct');
        showFeedback(true, '', currentExplanation);
    } else {
        btnElement.classList.add('wrong');
        btns.forEach(b => {
            if (b.innerText === currentAnswer) b.classList.add('correct');
        });
        showFeedback(false, '', currentExplanation);
    }
}

function showFeedback(isCorrect, extraInfo = '', explanationHTML = '') {
    const feedback = document.getElementById('feedback-area');
    const icon = document.getElementById('feedback-icon');
    const msg = document.getElementById('feedback-message');
    const explanationDiv = document.getElementById('feedback-explanation');
    
    feedback.classList.remove('hidden');
    explanationDiv.classList.add('hidden');
    explanationDiv.innerHTML = '';
    
    canProceed = false;
    setTimeout(() => { canProceed = true; }, 500);
    
    if (document.activeElement) {
        document.activeElement.blur();
    }
    
    if (isCorrect) {
        playSound('correct');
        icon.innerHTML = '<i class="fas fa-check-circle" style="color: var(--success-color);"></i>';
        msg.innerText = 'Tahniah! Jawapan tepat! 🌟';
        msg.style.color = 'var(--success-color)';
        currentScore += 10;
        updateScore();
        createConfetti();
    } else {
        playSound('wrong');
        icon.innerHTML = '<i class="fas fa-times-circle" style="color: var(--danger-color);"></i>';
        let message = 'Alamak! Cuba lagi selepas ini.';
        if (extraInfo) message += '\n' + extraInfo;
        msg.innerText = message;
        msg.style.color = 'var(--danger-color)';
        
        if (explanationHTML) {
            explanationDiv.innerHTML = `
                <div class="explanation-title"><i class="fas fa-lightbulb"></i> Mari Belajar</div>
                ${explanationHTML}
            `;
            explanationDiv.classList.remove('hidden');
        }
    }
    
    if (isCorrect) {
        sessionCorrect++;
    }
}

function endGame() {
    document.getElementById('feedback-area').classList.add('hidden');
    document.getElementById('summary-score').innerText = `${sessionCorrect}/${maxQuestions}`;
    
    const percentage = Math.round((sessionCorrect / maxQuestions) * 100);
    const summaryText = document.getElementById('summary-text');
    if (percentage >= 80) summaryText.innerText = `Syabas Aqil! Sangat hebat! (${percentage}%)`;
    else if (percentage >= 50) summaryText.innerText = `Bagus! Boleh tingkatkan lagi! (${percentage}%)`;
    else summaryText.innerText = `Terus berlatih ya! Jangan putus asa! (${percentage}%)`;
    
    document.getElementById('summary-modal').classList.remove('hidden');
    
    recordSession(sessionCorrect, maxQuestions);
}

function closeSummaryAndHome() {
    document.getElementById('summary-modal').classList.add('hidden');
    goHome();
}

function closeSummaryAndRestart() {
    document.getElementById('summary-modal').classList.add('hidden');
    startGame(currentGame);
}

function shuffleArray(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

function createConfetti() {
    for (let i = 0; i < 30; i++) {
        let conf = document.createElement('div');
        conf.style.position = 'absolute';
        conf.style.width = '10px';
        conf.style.height = '10px';
        conf.style.backgroundColor = ['#FD79A8', '#00B894', '#FDCB6E', '#6C5CE7'][Math.floor(Math.random() * 4)];
        conf.style.top = '0px';
        conf.style.left = Math.random() * 100 + '%';
        conf.style.borderRadius = '50%';
        conf.style.zIndex = '100';
        conf.style.animation = `fall ${Math.random() * 2 + 1}s linear forwards`;
        document.getElementById('game-screen').appendChild(conf);
        setTimeout(() => conf.remove(), 3000);
    }
}

const confettiStyle = document.createElement('style');
confettiStyle.innerHTML = `@keyframes fall { to { transform: translateY(100vh) rotate(720deg); opacity: 0; } }`;
document.head.appendChild(confettiStyle);

// ===========================
// DASHBOARD & LOCALSTORAGE
// ===========================

function getGameTitle(id) {
    const titles = {
        'nilai-tempat': 'Nilai Tempat & Digit',
        'banding-nombor': 'Banding Nombor',
        'bundar': 'Bundar Nombor',
        'cerakin': 'Cerakin Nombor',
        'ejaan': 'Ejaan Nombor',
        'darab-bahagi': 'Darab & Bahagi',
        'susun-nombor': 'Susun Nombor',
        'pola-nombor': 'Pola Nombor',
        'tambah': 'Tambah',
        'tolak': 'Tolak',
        'anggar': 'Anggar Nombor'
    };
    return titles[id] || id;
}

function recordSession(correctCount, totalCount) {
    let history = JSON.parse(localStorage.getItem('math_history')) || [];
    
    // Clear old data format if encountered
    if (history.length > 0 && history[0].total === undefined) {
        history = [];
    }
    
    const record = {
        date: new Date().toISOString(),
        module: getGameTitle(currentGame),
        correct: correctCount,
        total: totalCount
    };
    
    history.push(record);
    localStorage.setItem('math_history', JSON.stringify(history));
}

// Modal controls
function openDashboard() {
    document.getElementById('dashboard-modal').classList.remove('hidden');
    renderHistory();
    renderChart();
    renderModuleChart();
}

function closeDashboard() {
    document.getElementById('dashboard-modal').classList.add('hidden');
}

function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    if(tab === 'chart') {
        document.querySelectorAll('.tab-btn')[0].classList.add('active');
        document.getElementById('tab-chart').classList.add('active');
    } else if (tab === 'module') {
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
        document.getElementById('tab-module').classList.add('active');
    } else {
        document.querySelectorAll('.tab-btn')[2].classList.add('active');
        document.getElementById('tab-history').classList.add('active');
    }
}

function clearHistory() {
    if(confirm('Anda pasti mahu memadam semua rekod prestasi Aqil?')) {
        localStorage.removeItem('math_history');
        renderHistory();
        renderChart();
        renderModuleChart();
    }
}

function renderHistory() {
    const tbody = document.getElementById('history-tbody');
    tbody.innerHTML = '';
    
    let history = JSON.parse(localStorage.getItem('math_history')) || [];
    
    // Show latest first
    history.slice().reverse().forEach(record => {
        const tr = document.createElement('tr');
        
        const dateObj = new Date(record.date);
        const dateStr = dateObj.toLocaleDateString('ms-MY') + ' ' + dateObj.toLocaleTimeString('ms-MY', {hour: '2-digit', minute:'2-digit'});
        
        tr.innerHTML = `
            <td>${dateStr}</td>
            <td>${record.module}</td>
            <td>
                <span style="color: ${record.correct >= (record.total * 0.8) ? 'var(--success-color)' : (record.correct >= (record.total * 0.5) ? 'var(--warning-color)' : 'var(--danger-color)')}; font-weight:bold;">
                    ${record.correct} / ${record.total} (${Math.round((record.correct/record.total)*100)}%)
                </span>
            </td>
        `;
        tbody.appendChild(tr);
    });
    
    if(history.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; padding: 2rem;">Belum ada rekod. Sila main dahulu!</td></tr>';
    }
}

let accuracyChartInstance = null;

function renderChart() {
    const ctx = document.getElementById('accuracyChart');
    if (!ctx) return;
    
    let history = JSON.parse(localStorage.getItem('math_history')) || [];
    
    const filter = document.getElementById('module-filter').value;
    
    // Filter history based on selected module
    if (filter !== 'all') {
        history = history.filter(r => r.module === filter);
    }
    
    // Map sessions to labels and data
    const labels = [];
    const dataPoints = [];
    
    history.forEach((r, idx) => {
        labels.push(`Sesi ${idx + 1}`);
        dataPoints.push(Math.round((r.correct / r.total) * 100));
    });
    
    if (accuracyChartInstance) {
        accuracyChartInstance.destroy();
    }
    
    if(labels.length === 0) {
        // Dummy data if empty
        accuracyChartInstance = new Chart(ctx, {
            type: 'line',
            data: { labels: ['Tiada Data'], datasets: [{ label: 'Ketepatan (%)', data: [0] }] },
            options: { scales: { y: { min: 0, max: 100 } } }
        });
        return;
    }
    
    accuracyChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Peratusan Ketepatan (%)',
                data: dataPoints,
                borderColor: '#6C5CE7',
                backgroundColor: 'rgba(108, 92, 231, 0.2)',
                borderWidth: 3,
                pointBackgroundColor: '#FD79A8',
                pointRadius: 6,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            color: document.documentElement.getAttribute('data-theme') === 'dark' ? '#d2dae2' : '#666',
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Ketepatan (%)', color: document.documentElement.getAttribute('data-theme') === 'dark' ? '#d2dae2' : '#666' },
                    ticks: { color: document.documentElement.getAttribute('data-theme') === 'dark' ? '#d2dae2' : '#666' },
                    grid: { color: document.documentElement.getAttribute('data-theme') === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)' }
                },
                x: {
                    ticks: { color: document.documentElement.getAttribute('data-theme') === 'dark' ? '#d2dae2' : '#666' },
                    grid: { color: document.documentElement.getAttribute('data-theme') === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)' }
                }
            },
            plugins: {
                legend: { display: true, position: 'top', labels: { color: document.documentElement.getAttribute('data-theme') === 'dark' ? '#d2dae2' : '#666' } },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y + '% Betul';
                        }
                    }
                }
            }
        }
    });
}

let moduleChartInstance = null;

function renderModuleChart() {
    const ctx = document.getElementById('moduleChart');
    if (!ctx) return;
    
    let history = JSON.parse(localStorage.getItem('math_history')) || [];
    
    // Group by Module
    let grouped = {};
    history.forEach(r => {
        if(!grouped[r.module]) grouped[r.module] = { total: 0, correct: 0 };
        grouped[r.module].total += r.total;
        grouped[r.module].correct += r.correct;
    });
    
    // Sort by accuracy (ascending, so weakest modules appear first/highest concern or descending)
    // Let's sort by module name for consistent ordering, or by accuracy ascending to highlight weak points.
    // Sorting by accuracy ascending highlights the weakest modules at the top/left.
    const labels = Object.keys(grouped).sort((a, b) => {
        const accA = grouped[a].correct / grouped[a].total;
        const accB = grouped[b].correct / grouped[b].total;
        return accA - accB; // Lowest accuracy first
    });
    
    const dataPoints = labels.map(m => {
        return Math.round((grouped[m].correct / grouped[m].total) * 100);
    });
    
    // Determine colors based on accuracy (Red < 50%, Yellow 50-80%, Green > 80%)
    const bgColors = dataPoints.map(acc => {
        if(acc < 50) return 'rgba(255, 118, 117, 0.7)'; // Danger Red
        if(acc < 80) return 'rgba(253, 203, 110, 0.7)'; // Warning Yellow
        return 'rgba(0, 184, 148, 0.7)'; // Success Green
    });
    
    const borderColors = dataPoints.map(acc => {
        if(acc < 50) return '#d63031';
        if(acc < 80) return '#e17055';
        return '#00b894';
    });
    
    if (moduleChartInstance) {
        moduleChartInstance.destroy();
    }
    
    if(labels.length === 0) {
        // Dummy data if empty
        moduleChartInstance = new Chart(ctx, {
            type: 'bar',
            data: { labels: ['Tiada Data'], datasets: [{ label: 'Ketepatan (%)', data: [0] }] },
            options: { scales: { y: { min: 0, max: 100 } } }
        });
        return;
    }
    
    moduleChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Peratusan Ketepatan (%) mengikut Modul',
                data: dataPoints,
                backgroundColor: bgColors,
                borderColor: borderColors,
                borderWidth: 2,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Ketepatan (%)' }
                },
                x: {
                    ticks: {
                        autoSkip: false,
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            plugins: {
                legend: { display: false }, // Hide legend since colors explain it
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y + '% Betul';
                        }
                    }
                }
            }
        }
    });
}

// Update menu cards with latest performance
function updateMenuCards() {
    let history = JSON.parse(localStorage.getItem('math_history')) || [];
    const cards = document.querySelectorAll('.menu-card');
    
    cards.forEach(card => {
        const moduleId = card.getAttribute('data-id');
        const title = getGameTitle(moduleId);
        const statusDiv = card.querySelector('.module-status');
        if (!statusDiv) return;
        
        // Find latest session for this module
        // History is appended, so the last match is the latest
        const moduleHistory = history.filter(r => r.module === title);
        
        if (moduleHistory.length === 0) {
            statusDiv.innerHTML = `<span class="status-badge badge-none">⚪ Belum Cuba</span>`;
        } else {
            const latest = moduleHistory[moduleHistory.length - 1];
            const pct = Math.round((latest.correct / latest.total) * 100);
            
            let badgeClass = 'badge-bad';
            let icon = '🔴';
            if (pct >= 80) { badgeClass = 'badge-good'; icon = '🟢'; }
            else if (pct >= 50) { badgeClass = 'badge-ok'; icon = '🟡'; }
            
            statusDiv.innerHTML = `<span class="status-badge ${badgeClass}">${icon} Terakhir: ${pct}%</span>`;
        }
    });
}

// ===========================
// DARK MODE
// ===========================
function initTheme() {
    if (localStorage.getItem('math_theme') === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        const btn = document.getElementById('btn-dark-mode');
        if (btn) btn.innerHTML = '<i class="fas fa-sun"></i> Terang';
    }
}

function toggleDarkMode() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const btn = document.getElementById('btn-dark-mode');
    
    if (isDark) {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('math_theme', 'light');
        if (btn) btn.innerHTML = '<i class="fas fa-moon"></i> Gelap';
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('math_theme', 'dark');
        if (btn) btn.innerHTML = '<i class="fas fa-sun"></i> Terang';
    }
    
    // Update chart colors if it's currently rendered
    if (document.getElementById('dashboard-modal').classList.contains('hidden') === false) {
        renderChart();
    }
}

// Call on init
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    updateMenuCards();
});

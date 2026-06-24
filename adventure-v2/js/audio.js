// ==========================================
// AUDIO LAYER — read-aloud, sound effects, confetti
// Strategy: use pre-generated natural gTTS clips if present (window.SAINS_AUDIO_DB),
// otherwise fall back to the browser's built-in voice (Web Speech API).
// ==========================================

const AudioFX = (() => {
    const SOUND_KEY = 'sains_explorer_sound';
    let soundOn = localStorage.getItem(SOUND_KEY) !== 'off';
    let bestVoice = null;
    let currentClip = null;

    // Naikkan pitch sikit supaya bunyi lebih ceria/muda (tala di sini).
    // 1.0 = asal · 1.08 = ceria · 1.12 = sangat peppy
    const CHEER_RATE = 1.08;

    // ---- pick the best Malay/Indonesian voice for Web Speech fallback ----
    function pickVoice() {
        if (!('speechSynthesis' in window)) return;
        const voices = speechSynthesis.getVoices();
        // Bahasa Melayu SAHAJA — jangan jatuh ke suara Indonesia.
        bestVoice =
            voices.find(v => /ms[-_]?MY/i.test(v.lang)) ||
            voices.find(v => /^ms/i.test(v.lang)) ||
            voices.find(v => /\bmelayu\b|\bmalay\b/i.test(v.name)) ||
            null;
    }
    if ('speechSynthesis' in window) {
        pickVoice();
        speechSynthesis.onvoiceschanged = pickVoice;
    }

    function stop() {
        if ('speechSynthesis' in window) speechSynthesis.cancel();
        if (currentClip) { currentClip.pause(); currentClip = null; }
    }

    // ---- speak a string (auto-chooses pre-gen clip vs browser voice) ----
    function speak(text) {
        if (!soundOn || !text) return;
        stop();
        const clean = String(text).replace(/[\u{1F000}-\u{1FFFF}\u{2600}-\u{27BF}]/gu, '').trim();
        if (!clean) return;

        // 1) pre-generated natural audio (best quality)
        if (window.SAINS_AUDIO_DB && window.SAINS_AUDIO_DB[clean]) {
            currentClip = new Audio(window.SAINS_AUDIO_DB[clean]);
            // raise pitch a touch -> cheerier voice (preservesPitch off = pitch follows rate)
            currentClip.preservesPitch = false;
            currentClip.mozPreservesPitch = false;
            currentClip.webkitPreservesPitch = false;
            currentClip.playbackRate = CHEER_RATE;
            currentClip.play().catch(() => {});
            return;
        }
        // 2) browser voice (robotic-ish — upgrade by running generate_sains_audio.py)
        if ('speechSynthesis' in window) {
            const u = new SpeechSynthesisUtterance(clean);
            if (bestVoice) u.voice = bestVoice;
            u.lang = bestVoice ? bestVoice.lang : 'ms-MY';
            u.rate = 0.95;   // clear but a bit livelier
            u.pitch = 1.25;  // higher = more cheerful/excited
            speechSynthesis.speak(u);
        }
    }

    function toggle() {
        soundOn = !soundOn;
        localStorage.setItem(SOUND_KEY, soundOn ? 'on' : 'off');
        if (!soundOn) stop();
        return soundOn;
    }
    function isOn() { return soundOn; }

    // ---- WebAudio sound effects (no files, fully offline) ----
    let ctx = null;
    function ac() { if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)(); return ctx; }
    function tone(freq, start, dur, type = 'sine', vol = 0.18) {
        const a = ac(); const o = a.createOscillator(); const g = a.createGain();
        o.type = type; o.frequency.value = freq;
        o.connect(g); g.connect(a.destination);
        const t = a.currentTime + start;
        g.gain.setValueAtTime(0, t);
        g.gain.linearRampToValueAtTime(vol, t + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
        o.start(t); o.stop(t + dur);
    }
    function correctChime() { if (!soundOn) return; try { tone(659, 0, 0.15, 'triangle'); tone(988, 0.12, 0.22, 'triangle'); } catch(e){} }
    function wrongBuzz()   { if (!soundOn) return; try { tone(196, 0, 0.25, 'sine', 0.15); } catch(e){} }

    return { speak, stop, toggle, isOn, correctChime, wrongBuzz };
})();

// ==========================================
// CONFETTI — lightweight canvas burst, no library
// ==========================================
const Confetti = (() => {
    let canvas, c, pieces = [], raf = null;
    const colors = ['#5DADE2', '#58D68D', '#F4D03F', '#EC7063', '#AF7AC5', '#EB984E'];

    function ensure() {
        if (canvas) return;
        canvas = document.createElement('canvas');
        canvas.id = 'confetti-canvas';
        document.body.appendChild(canvas);
        c = canvas.getContext('2d');
        resize(); window.addEventListener('resize', resize);
    }
    function resize() { if (!canvas) return; canvas.width = innerWidth; canvas.height = innerHeight; }

    function burst() {
        ensure();
        for (let i = 0; i < 90; i++) {
            pieces.push({
                x: innerWidth / 2, y: innerHeight / 3,
                vx: (Math.random() - 0.5) * 12, vy: Math.random() * -10 - 4,
                size: Math.random() * 8 + 4, color: colors[i % colors.length],
                rot: Math.random() * 6, vr: (Math.random() - 0.5) * 0.3, life: 1
            });
        }
        if (!raf) loop();
    }
    function loop() {
        c.clearRect(0, 0, canvas.width, canvas.height);
        pieces.forEach(p => {
            p.vy += 0.35; p.x += p.vx; p.y += p.vy; p.rot += p.vr; p.life -= 0.008;
            c.save(); c.globalAlpha = Math.max(p.life, 0);
            c.translate(p.x, p.y); c.rotate(p.rot);
            c.fillStyle = p.color; c.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
            c.restore();
        });
        pieces = pieces.filter(p => p.life > 0 && p.y < canvas.height + 40);
        if (pieces.length) { raf = requestAnimationFrame(loop); }
        else { c.clearRect(0, 0, canvas.width, canvas.height); raf = null; }
    }
    return { burst };
})();

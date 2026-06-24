import json
import re

file_path = "/Users/re1/Documents/antigravity/modest-bohr/feqah.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Explanations for the 60 questions (15 per topic)
explanations = {
    "najis": [
        "Najis dari segi istilah merujuk kepada sesuatu yang kotor dan menghalang sahnya ibadat seperti solat.",
        "Terdapat 3 jenis najis iaitu Mukhaffafah (ringan), Mutawassitah (pertengahan), dan Mughallazah (berat).",
        "Arak, darah, dan babi adalah contoh najis. Pasir dan lumpur hanyalah kotoran biasa, bukan najis.",
        "Muntah dan darah adalah najis Mutawassitah (pertengahan).",
        "Umat Islam diwajibkan untuk membersihkan najis pada badan, pakaian, dan tempat solat agar ibadat sah.",
        "Mukhaffafah bermaksud ringan. Ia merujuk kepada air kencing bayi lelaki yang berumur 2 tahun ke bawah.",
        "Air kencing bayi lelaki (2 tahun ke bawah) yang hanya minum susu ibu adalah najis Mukhaffafah.",
        "Najis Mukhaffafah hanya perlu direnjis dengan air mutlak ke kawasan yang terkena najis selepas dilap kering.",
        "Mutawassitah bermaksud pertengahan. Ia meliputi majoriti najis seperti darah, nanah, dan tahi.",
        "Darah, nanah, dan muntah dikategorikan sebagai najis Mutawassitah (pertengahan).",
        "Syarat suci daripada najis Mutawassitah ialah hilangnya bau, warna, dan rasa najis tersebut.",
        "Mughallazah bermaksud berat. Ia adalah kategori najis yang paling berat cara penyuciannya.",
        "Anjing, babi, dan segala keturunannya merupakan najis Mughallazah.",
        "Cara menyucikan najis Mughallazah dinamakan sebagai sertu.",
        "Sertu dilakukan dengan membasuh kawasan yang terkena najis dengan 1 kali basuhan air bercampur tanah, diikuti 6 kali basuhan air mutlak."
    ],
    "hadas": [
        "Hadas kecil perlu disucikan dengan mengambil wuduk. Jika tiada air, boleh diganti dengan tayamum.",
        "Hilang akal (gila, pitam, mabuk) merupakan sebab hadas kecil, bukannya hadas besar.",
        "Tidur yang tidak tetap punggung boleh membatalkan wuduk, yang menyebabkan seseorang itu berhadas kecil.",
        "Tawaf di Kaabah adalah diharamkan sama sekali ketika berada dalam keadaan berhadas besar.",
        "Hadas besar hanya boleh disucikan melalui mandi wajib.",
        "Hadas terbahagi kepada dua kategori iaitu hadas kecil dan hadas besar.",
        "Perbuatan kentut atau buang air (keluar sesuatu dari qubul/dubur) membatalkan wuduk dan menyebabkan hadas kecil.",
        "Hilang akal menyebabkan seseorang itu berada dalam keadaan berhadas kecil dan wuduknya terbatal.",
        "Bersentuh kulit berlainan jantina (bukan mahram) tanpa berlapik membatalkan wuduk (hadas kecil).",
        "Sesiapa yang berada dalam keadaan hadas besar wajib melaksanakan mandi wajib untuk membolehkannya kembali beribadat.",
        "Haid dan nifas adalah fitrah khusus yang berlaku kepada kaum perempuan, menyebabkan mereka berhadas besar.",
        "Wiladah adalah istilah syarak bagi perbuatan melahirkan anak.",
        "Bersetubuh antara suami dan isteri mewajibkan kedua-duanya untuk mandi wajib kerana berhadas besar.",
        "Orang yang mati syahid tidak perlu dimandikan dan tidak perlu disolatkan jenazahnya.",
        "Solat memerlukan wuduk. Tanpa wuduk (berhadas kecil), solat tidak sah."
    ],
    "mandiwajib": [
        "Mandi wajib adalah diwajibkan bagi menyucikan diri daripada hadas besar.",
        "Niat mandi wajib hanya sah jika dibaca ketika air pertama kali mula menyentuh mana-mana bahagian anggota badan.",
        "Lafaz 'Nawaitu raf'al hadathil akbar' bermaksud 'Sahaja aku mengangkat hadas besar'.",
        "Terdapat 2 rukun mandi wajib: niat dan meratakan air ke seluruh anggota badan.",
        "Mengerjakan solat dan tawaf memerlukan seseorang itu bebas daripada sebarang hadas (kecil dan besar).",
        "Istilah yang tepat untuk perbuatan tersebut ialah mandi wajib.",
        "Hukumnya adalah wajib, kerana ibadah fardu tidak sah tanpa mandi wajib.",
        "Menurut silibus, terdapat 2 rukun utama: niat, dan meratakan air ke seluruh badan (termasuk menghilangkan najis jika ada).",
        "Setiap ibadah mesti dimulakan dengan niat.",
        "Ini adalah niat umum untuk mandi wajib (mengangkat hadas besar).",
        "Air mestilah menyerap dan terkena pada seluruh kulit dan setiap helaian rambut/bulu pada badan.",
        "Berzikir dibenarkan dan sangat digalakkan walaupun ketika dalam keadaan berhadas besar.",
        "Al-Quran adalah kitab suci yang haram disentuh atau dibaca oleh mereka yang berhadas besar.",
        "Masjid adalah tempat suci yang haram untuk orang yang berhadas besar berhenti atau berehat di dalamnya.",
        "Air mutlak (seperti air paip, air hujan, air perigi) adalah satu-satunya jenis air yang sah untuk bersuci."
    ],
    "mandisunat": [
        "Mandi sunat memberikan ganjaran pahala. Jika tidak dibuat, ia tidak mendatangkan dosa.",
        "Sangat digalakkan mandi sunat pada pagi hari Jumaat sebelum bergerak menunaikan solat Jumaat.",
        "Lafaz tersebut secara spesifik bermaksud niat mandi sunat untuk hadir solat Jumaat ('sunnatan lillahi taala').",
        "1 Syawal adalah tarikh sambutan Hari Raya Aidilfitri.",
        "Mandi selepas keluar darah haid adalah mandi wajib, bukan mandi sunat.",
        "Oleh kerana ia berstatus sunat, maka tidak berdosa jika ditinggalkan.",
        "Setahun ada dua hari raya utama bagi umat Islam (Aidilfitri dan Aidiladha).",
        "Jemaah digalakkan mandi sunat ihram sebelum mula berniat dan memakai kain ihram.",
        "Mandi sunat gerhana (Kusuf/Khusuf) digalakkan sebelum mendirikan solat sunat gerhana.",
        "Islam menggalakkan kita untuk membersihkan diri dengan mandi sunat setelah selesai menguruskan dan memandikan jenazah.",
        "Mandi sunat memeluk Islam digalakkan sebagai simbolik membersihkan diri memulakan hidup baru.",
        "Ia bukan sahaja memberikan pahala, tetapi badan akan rasa lebih segar dan tenang untuk beribadah.",
        "Niat khusus tersebut dibaca pada hari raya Aidiladha (Hari Raya Korban).",
        "Selain kebersihan badan, memakai wangi-wangian dan pakaian bersih adalah sunnah ke masjid.",
        "Semua perbuatan mandi yang bermatlamat untuk bersuci dan ibadah perlulah menggunakan air mutlak."
    ]
}

# Regex to find the quizData block
quiz_block_pattern = re.compile(r'const quizData = (\{.*?\});', re.DOTALL)
match = quiz_block_pattern.search(content)
if match:
    pass

# A simpler way: we'll just reconstruct the quizData block
new_quiz_data_str = "const quizData = {\\n"
for topic in explanations.keys():
    new_quiz_data_str += f'            {topic}: [\\n'
    # we need to find the lines for this topic to extract the q, options, answer
    topic_regex = re.compile(f'{topic}: \\[(.*?)\\]', re.DOTALL)
    t_match = topic_regex.search(match.group(1))
    
    if t_match:
        questions_str = t_match.group(1)
        # find all { ... }
        q_objs = re.findall(r'\{([^}]+)\}', questions_str)
        for i, q_obj in enumerate(q_objs):
            # q_obj is like: q: "...", options: [...], answer: X
            # Add explanation: "..."
            expl = explanations[topic][i]
            # carefully append explanation
            new_line = f'                {{{q_obj}, explanation: "{expl}"}}'
            if i < len(q_objs) - 1:
                new_line += ','
            new_quiz_data_str += new_line + "\\n"
    new_quiz_data_str += '            ]'
    if topic != "mandisunat":
         new_quiz_data_str += ',\\n'
    else:
         new_quiz_data_str += '\\n'
new_quiz_data_str += '        };'

content = content.replace(match.group(0), new_quiz_data_str)

# Update renderQuizQuestion
render_old = """                    <div class="quiz-options">
                        ${optionsHtml}
                    </div>
                    <button class="quiz-next-btn" id="next-btn" onclick="nextQuestion()">Seterusnya ➡️</button>"""
render_new = """                    <div class="quiz-options">
                        ${optionsHtml}
                    </div>
                    <div id="explanation-box" style="display:none; margin-top:15px; padding:12px; border-radius:8px; background-color:#fee2e2; color:#991b1b; font-size:14px; border-left:4px solid #ef4444; line-height:1.4;"></div>
                    <button class="quiz-next-btn" id="next-btn" onclick="nextQuestion()">Seterusnya ➡️</button>"""
content = content.replace(render_old, render_new)

# Update selectAnswer
select_old = """            if (selectedIdx === correctIdx) {
                score++;
            }

            document.getElementById('next-btn').classList.add('show');"""
select_new = """            const q = quizData[currentTopic][currentQuizIndex];

            if (selectedIdx === correctIdx) {
                score++;
            } else {
                if (q.explanation) {
                    const explBox = document.getElementById('explanation-box');
                    explBox.style.display = 'block';
                    explBox.innerHTML = '<strong>💡 Tahukah anda?</strong><br>' + q.explanation;
                }
            }

            document.getElementById('next-btn').classList.add('show');"""
content = content.replace(select_old, select_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("done")

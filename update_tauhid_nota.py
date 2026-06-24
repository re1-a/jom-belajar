import re

with open('/Users/re1/Documents/antigravity/modest-bohr/tauhid.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_sifat = """
                <div class="nota-card">
                    <h2>Pelajaran Pertama: Sifat Allah SWT yang Wajib dan Mustahil</h2>
                    <p>Mengenali sifat Allah SWT adalah asas dalam memantapkan akidah. Setiap sifat yang <strong>wajib</strong> bagi Allah mempunyai sifat lawannya yang <strong>mustahil</strong> bagi Allah. Pelajaran ini mengandungi lima (5) sifat.</p>

                    <h3>Unit 1: Qidam (قِدَمٌ) — lawannya Hudus (حُدُوثٌ)</h3>
                    <ul>
                        <li><strong>Maksud:</strong> Sedia ada. Allah SWT sedia ada dan tiada permulaan bagi kewujudan-Nya.</li>
                        <li><strong>Sifat Lawan (Mustahil):</strong> Hudus (حُدُوثٌ) bermaksud baharu, iaitu ada permulaan.</li>
                        <li><strong>Hukum:</strong> Wajib bagi Allah SWT bersifat Qidam dan mustahil bagi Allah bersifat Hudus (baharu).</li>
                        <li><strong>Dalil Naqli:</strong> Surah Al-Hadid, ayat 3:
                            <blockquote style="font-family: 'Amiri', serif; font-size: 26px; direction: rtl; margin: 10px 0; background: rgba(139, 92, 246, 0.05); padding: 15px; border-radius: 8px; border-right: 4px solid #8b5cf6;">هُوَ ٱلْأَوَّلُ وَٱلْءَاخِرُ وَٱلظَّاهِرُ وَٱلْبَاطِنُ ۖ وَهُوَ بِكُلِّ شَىْءٍ عَلِيمٌ</blockquote>
                            <em>"Dialah Yang Awal dan Yang Akhir, Yang Zahir dan Yang Batin; dan Dia Maha Mengetahui akan tiap-tiap sesuatu."</em><br>
                            <small>(Perkataan <strong>"Yang Awal"</strong> menunjukkan Allah tiada permulaan — inilah maksud Qidam.)</small>
                        </li>
                        <li><strong>Faedah mengenal sifat Qidam:</strong>
                            <ol>
                                <li>Iman menjadi semakin kukuh.</li>
                                <li>Sentiasa taat kepada perintah Allah SWT.</li>
                                <li>Sentiasa berakhlak mulia dalam kehidupan.</li>
                            </ol>
                        </li>
                    </ul>

                    <h3>Unit 2: Baqa' (بَقَاءٌ) — lawannya Fanaa' (فَنَاءٌ)</h3>
                    <ul>
                        <li><strong>Maksud:</strong> Kekal. Allah SWT tetap ada dan tidak akan binasa atau berakhir.</li>
                        <li><strong>Sifat Lawan (Mustahil):</strong> Fanaa' (فَنَاءٌ) bermaksud binasa.</li>
                        <li><strong>Hukum:</strong> Wajib bagi Allah SWT bersifat Baqa' dan mustahil bagi Allah bersifat Fanaa' (binasa).</li>
                        <li><strong>Dalil Naqli:</strong> Surah Ar-Rahman, ayat 26–27:
                            <blockquote style="font-family: 'Amiri', serif; font-size: 26px; direction: rtl; margin: 10px 0; background: rgba(139, 92, 246, 0.05); padding: 15px; border-radius: 8px; border-right: 4px solid #8b5cf6;">كُلُّ مَنْ عَلَيْهَا فَانٍ وَيَبْقَىٰ وَجْهُ رَبِّكَ ذُو ٱلْجَلَالِ وَٱلْإِكْرَامِ</blockquote>
                            <em>"Segala yang ada di bumi itu akan binasa. Dan akan kekal Zat Tuhanmu yang mempunyai Kebesaran dan Kemuliaan."</em>
                        </li>
                        <li><strong>Faedah mengenal sifat Baqa':</strong>
                            <ol>
                                <li>Mengakui kebesaran dan kekuasaan Allah SWT.</li>
                                <li>Sentiasa mengingati mati dan membuat persiapan untuk akhirat.</li>
                            </ol>
                        </li>
                    </ul>

                    <h3>Unit 3: Mukhalafatuhu lil-Hawadith (مُخَالَفَتُهُ تَعَالَى لِلْحَوَادِثِ) — lawannya Mumathalatuhu lil-Hawadith (مُمَاثَلَتُهُ تَعَالَى لِلْحَوَادِثِ)</h3>
                    <ul>
                        <li><strong>Maksud:</strong> Berbeza Allah SWT dengan segala yang baharu (makhluk). Allah tidak serupa dengan apa yang dicipta-Nya.</li>
                        <li><strong>Sifat Lawan (Mustahil):</strong> Mumathalatuhu lil-Hawadith bermaksud Allah menyerupai makhluk.</li>
                        <li><strong>Hukum:</strong> Wajib bagi Allah SWT berbeza dengan makhluk dan mustahil Allah menyerupai makhluk.</li>
                        <li><strong>Dalil Naqli:</strong> Surah Asy-Syura, ayat 11:
                            <blockquote style="font-family: 'Amiri', serif; font-size: 26px; direction: rtl; margin: 10px 0; background: rgba(139, 92, 246, 0.05); padding: 15px; border-radius: 8px; border-right: 4px solid #8b5cf6;">لَيْسَ كَمِثْلِهِ شَىْءٌ ۖ وَهُوَ ٱلسَّمِيعُ ٱلْبَصِيرُ</blockquote>
                            <em>"Tiada sesuatu pun yang serupa dengan-Nya, dan Dialah Yang Maha Mendengar lagi Maha Melihat."</em>
                        </li>
                        <li><strong>Faedah mengenal sifat ini:</strong>
                            <ol>
                                <li>Mengenali keagungan Allah yang tiada tolok bandingnya.</li>
                                <li>Tidak menggambarkan Allah SWT seperti makhluk ciptaan-Nya.</li>
                            </ol>
                        </li>
                    </ul>

                    <h3>Unit 4: Qiyamuhu binafsihi (قِيَامُهُ تَعَالَى بِنَفْسِهِ) — lawannya Qiyamuhu bighairihi (قِيَامُهُ تَعَالَى بِغَيْرِهِ)</h3>
                    <ul>
                        <li><strong>Maksud:</strong> Allah SWT berdiri dengan sendiri-Nya, tidak memerlukan bantuan, tempat, atau sesuatu yang lain.</li>
                        <li><strong>Sifat Lawan (Mustahil):</strong> Qiyamuhu bighairihi (قِيَامُهُ بِغَيْرِهِ) bermaksud Allah berdiri (bergantung) dengan yang lain.</li>
                        <li><strong>Hukum:</strong> Wajib bagi Allah SWT berdiri dengan sendiri-Nya dan mustahil Allah berdiri dengan yang lain.</li>
                        <li><strong>Dalil Naqli:</strong> Surah Al-'Ankabut, ayat 6:
                            <blockquote style="font-family: 'Amiri', serif; font-size: 26px; direction: rtl; margin: 10px 0; background: rgba(139, 92, 246, 0.05); padding: 15px; border-radius: 8px; border-right: 4px solid #8b5cf6;">إِنَّ ٱللَّهَ لَغَنِىٌّ عَنِ ٱلْعَالَمِينَ</blockquote>
                            <em>"Sesungguhnya Allah Maha Kaya (tidak berhajat kepada sesuatu) daripada sekalian alam."</em>
                        </li>
                        <li><strong>Faedah mengenal sifat ini:</strong>
                            <ol>
                                <li>Menyedari Allah SWT Maha Kaya dan tidak bergantung kepada sesiapa.</li>
                                <li>Menambah keyakinan terhadap kekuasaan Allah SWT.</li>
                            </ol>
                        </li>
                    </ul>

                    <h3>Unit 5: Wahdaniyyah (وَحْدَانِيَّةٌ) — lawannya Ta'addud (تَعَدُّدٌ)</h3>
                    <ul>
                        <li><strong>Maksud:</strong> Esa atau tunggal. Allah SWT satu pada zat, sifat, dan perbuatan-Nya.</li>
                        <li><strong>Sifat Lawan (Mustahil):</strong> Ta'addud (تَعَدُّدٌ) bermaksud berbilang-bilang.</li>
                        <li><strong>Hukum:</strong> Wajib bagi Allah SWT bersifat Esa dan mustahil Allah bersifat berbilang.</li>
                        <li><strong>Dalil Naqli:</strong> Surah Al-Ikhlas, ayat 1:
                            <blockquote style="font-family: 'Amiri', serif; font-size: 26px; direction: rtl; margin: 10px 0; background: rgba(139, 92, 246, 0.05); padding: 15px; border-radius: 8px; border-right: 4px solid #8b5cf6;">قُلْ هُوَ ٱللَّهُ أَحَدٌ</blockquote>
                            <em>"Katakanlah (wahai Muhammad): Dialah Allah Yang Maha Esa."</em>
                        </li>
                        <li><strong>Faedah mengenal sifat Wahdaniyyah:</strong>
                            <ol>
                                <li>Tidak menyembah tuhan selain Allah SWT.</li>
                                <li>Ketaatan kepada perintah Allah menjadi lebih mantap.</li>
                                <li>Iman bertambah kukuh dan teguh.</li>
                            </ol>
                        </li>
                    </ul>
                </div>
"""

new_malaikat = """
                <div class="nota-card">
                    <h2>Pelajaran Kedua: Beriman kepada Malaikat</h2>
                    <p>Beriman kepada Malaikat merupakan <strong>rukun iman yang kedua</strong>.</p>
                    
                    <h3>Unit 1: Pengertian, Hukum dan Dalil Beriman kepada Malaikat</h3>
                    <ul>
                        <li><strong>Pengertian:</strong> Malaikat ialah makhluk Allah SWT yang diciptakan daripada cahaya (nur). Mereka tidak mempunyai jantina (bukan lelaki atau perempuan), tidak makan, tidak minum, dan tidak tidur.</li>
                        <li><strong>Hukum:</strong> Wajib bagi setiap umat Islam beriman kepada Malaikat.</li>
                        <li><strong>Dalil Naqli:</strong> Surah Al-Baqarah, ayat 285:
                            <blockquote style="font-family: 'Amiri', serif; font-size: 26px; direction: rtl; margin: 10px 0; background: rgba(139, 92, 246, 0.05); padding: 15px; border-radius: 8px; border-right: 4px solid #8b5cf6;">كُلٌّ ءَامَنَ بِٱللَّهِ وَمَلَـٰئِكَتِهِ وَكُتُبِهِ وَرُسُلِهِ</blockquote>
                            <em>"Semuanya beriman kepada Allah, malaikat-malaikat-Nya, kitab-kitab-Nya, dan rasul-rasul-Nya."</em>
                        </li>
                    </ul>

                    <h3>Unit 2: Nama, Tugas dan Sifat Malaikat</h3>
                    <p><strong>Sepuluh (10) Malaikat dan tugasnya:</strong></p>
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

                    <p><strong>Perbandingan sifat Malaikat dan manusia:</strong></p>
                    <table>
                        <tr><th>Perkara</th><th>Malaikat</th><th>Manusia</th></tr>
                        <tr><td>Asal kejadian</td><td>Dicipta daripada cahaya (nur).</td><td>Dicipta daripada tanah (bagi Nabi Adam) dan air mani.</td></tr>
                        <tr><td>Sifat fizikal</td><td>Tidak berjantina.</td><td>Berjantina (lelaki dan perempuan).</td></tr>
                        <tr><td>Keperluan asas</td><td>Tidak makan, tidak minum, dan tidak tidur.</td><td>Perlu makan, minum, dan tidur.</td></tr>
                        <tr><td>Ketaatan</td><td>Sentiasa taat dan patuh kepada perintah Allah.</td><td>Ada yang taat dan ada yang ingkar.</td></tr>
                    </table>
                </div>
"""

new_kitab = """
                <div class="nota-card">
                    <h2>Pelajaran Ketiga: Beriman kepada Kitab</h2>
                    <p>Beriman kepada kitab-kitab Allah merupakan <strong>rukun iman yang ketiga</strong>.</p>
                    
                    <h3>Unit 1: Pengertian, Hukum dan Dalil Beriman kepada Kitab</h3>
                    <ul>
                        <li><strong>Pengertian:</strong> Kitab-kitab Allah ialah kalam Allah (kata-kata Allah) yang diwahyukan kepada para Rasul untuk disampaikan kepada umat manusia sebagai panduan hidup.</li>
                        <li><strong>Hukum:</strong> Wajib dipercayai bahawa Allah telah menurunkan kitab-kitab suci kepada para Rasul tertentu.</li>
                        <li><strong>Bilangan kitab</strong> yang wajib diketahui ialah <strong>empat (4)</strong>.</li>
                        <li><strong>Dalil Naqli:</strong> Surah An-Nisa', ayat 136:
                            <blockquote style="font-family: 'Amiri', serif; font-size: 26px; direction: rtl; margin: 10px 0; background: rgba(139, 92, 246, 0.05); padding: 15px; border-radius: 8px; border-right: 4px solid #8b5cf6;">ءَامِنُوا۟ بِٱللَّهِ وَرَسُولِهِ وَٱلْكِتَـٰبِ ٱلَّذِى نَزَّلَ عَلَىٰ رَسُولِهِ وَٱلْكِتَـٰبِ ٱلَّذِىٓ أَنزَلَ مِن قَبْلُ</blockquote>
                            <em>"Berimanlah kamu kepada Allah dan Rasul-Nya, dan kepada Kitab yang diturunkan kepada Rasul-Nya, serta Kitab yang diturunkan sebelumnya."</em>
                        </li>
                    </ul>

                    <h3>Unit 2: Kitab yang Diturunkan Allah kepada Para Rasul</h3>
                    <table>
                        <tr><th>Bil</th><th>Nama Kitab</th><th>Rasul yang Menerimanya</th></tr>
                        <tr><td>1</td><td>Taurat</td><td>Nabi Musa AS</td></tr>
                        <tr><td>2</td><td>Zabur</td><td>Nabi Daud AS</td></tr>
                        <tr><td>3</td><td>Injil</td><td>Nabi Isa AS</td></tr>
                        <tr><td>4</td><td>Al-Quran</td><td>Nabi Muhammad SAW</td></tr>
                    </table>

                    <h3>Nota tambahan:</h3>
                    <ul>
                        <li>Al-Quran ialah kitab terakhir yang diturunkan oleh Allah SWT dan menjadi pelengkap serta penyempurna kepada kitab-kitab sebelumnya.</li>
                        <li>Membaca dan memahami isi kandungan Al-Quran dituntut dalam Islam sebagai panduan kehidupan seharian.</li>
                    </ul>
                </div>
"""

new_nota_data = f"""const notaData = {{
            sifat: `{new_sifat}`,
            malaikat: `{new_malaikat}`,
            kitab: `{new_kitab}`
        }};"""

# Replace the notaData block
html = re.sub(r'const notaData = {.*?};\s*const quizData = {', new_nota_data + '\n\n        const quizData = {', html, flags=re.DOTALL)

with open('/Users/re1/Documents/antigravity/modest-bohr/tauhid.html', 'w', encoding='utf-8') as f:
    f.write(html)

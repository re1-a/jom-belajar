import re

file_path = "/Users/re1/Documents/antigravity/modest-bohr/feqah.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Topic Pills
pills_old = '<button class="topic-pill active" data-topic="najis">Najis</button>'
pills_new = '<button class="topic-pill active" data-topic="istinjak">Istinjak</button>\n        <button class="topic-pill" data-topic="wuduk">Wuduk</button>\n        <button class="topic-pill" data-topic="najis">Najis</button>'
content = content.replace(pills_old, pills_new)
# Since 'najis' might not be active if we change the default, wait, I just replaced the active one.
# Let's change let currentTopic = 'najis'; to 'istinjak';
content = content.replace("let currentTopic = 'najis';", "let currentTopic = 'istinjak';")

# 2. Add to notaData
nota_istinjak = """
            istinjak: `
                <div class="nota-card">
                    <h2>Pelajaran: Istinjak (إستنجاء)</h2>
                    <p>Menjaga kebersihan diri selepas membuang air adalah tuntutan agama.</p>
                    
                    <h3>Pengertian & Hukum</h3>
                    <ul>
                        <li><strong>Pengertian:</strong> Membersihkan qubul (kemaluan depan) atau dubur (kemaluan belakang) selepas membuang air kecil atau air besar.</li>
                        <li><strong>Hukum:</strong> <strong>Wajib</strong> ke atas setiap orang Islam.</li>
                    </ul>

                    <h3>Alat-alat Istinjak</h3>
                    <ul>
                        <li><strong>Alat Utama:</strong> Air Mutlak (paling afdal).</li>
                        <li><strong>Alat Tambahan (Benda Kesat):</strong> Batu, daun kering, kertas tisu, kulit kayu dan kain.</li>
                        <li><strong>Benda Haram Beristinjak:</strong> Kertas yang mengandungi ayat al-Quran/Hadis, makanan, tulang, benda licin (kaca/plastik/buluh).</li>
                    </ul>

                    <h3>Syarat Beristinjak Dengan Benda Kesat</h3>
                    <p>Jika ketiadaan air, kita boleh menggunakan benda kesat dengan syarat:</p>
                    <ol>
                        <li>Najis tersebut belum kering.</li>
                        <li>Najis tidak meleleh atau merebak ke tempat lain.</li>
                        <li>Mesti menyapu sekurang-kurangnya <strong>tiga kali</strong> sapuan (atau menggunakan 3 ketul batu / 1 batu yang ada 3 bucu).</li>
                    </ol>

                    <h3>Adab Qada' Hajat (Masuk Tandas)</h3>
                    <ul>
                        <li>Masuk ke tandas mendahulukan <strong>kaki kiri</strong>. Keluar mendahulukan <strong>kaki kanan</strong>.</li>
                        <li>Membaca doa masuk tandas.</li>
                        <li>Jangan bercakap, menyanyi atau makan minum di dalam tandas.</li>
                    </ul>
                </div>
            `,"""

nota_wuduk = """
            wuduk: `
                <div class="nota-card">
                    <h2>Pelajaran: Wuduk (وضوء)</h2>
                    
                    <h3>Pengertian & Hukum</h3>
                    <ul>
                        <li><strong>Pengertian:</strong> Membersihkan anggota badan tertentu dengan air mutlak berserta niat.</li>
                        <li><strong>Hukum Wajib:</strong> Untuk mendirikan solat, tawaf, dan menyentuh/membaca al-Quran.</li>
                        <li><strong>Hukum Sunat:</strong> Untuk tidur, membaca al-Quran (tanpa sentuh), dan masuk ke masjid.</li>
                    </ul>

                    <h3>Rukun Wuduk (6 Perkara)</h3>
                    <p>Rukun wajib dilakukan, jika tertinggal salah satu maka wuduk tidak sah:</p>
                    <ol>
                        <li><strong>Niat:</strong> <em>"Nawaitul wudu'a lillahi taala"</em> (Sahaja aku mengambil wuduk kerana Allah Taala).</li>
                        <li>Membasuh <strong>muka</strong>.</li>
                        <li>Membasuh kedua-dua <strong>tangan</strong> hingga ke siku.</li>
                        <li>Menyapu sedikit air ke atas bahagian <strong>kepala</strong>.</li>
                        <li>Membasuh kedua-dua <strong>kaki</strong> hingga ke buku lali.</li>
                        <li><strong>Tertib:</strong> Melakukan mengikut urutan yang betul di atas.</li>
                    </ol>

                    <h3>Perkara Sunat Wuduk</h3>
                    <ul>
                        <li>Membaca Bismillah.</li>
                        <li>Membasuh kedua-dua tapak tangan.</li>
                        <li>Berkumur-kumur dan memasukkan air ke dalam hidung.</li>
                        <li>Menyapu air ke seluruh telinga luar dan dalam.</li>
                        <li>Menghadap ke arah kiblat.</li>
                    </ul>

                    <h3>Perkara Yang Membatalkan Wuduk</h3>
                    <ul>
                        <li>Keluar sesuatu dari qubul atau dubur (kentut, kencing, berak).</li>
                        <li>Tidur tidak tetap punggung (tidur baring / mengiring).</li>
                        <li>Hilang akal (gila, pitam, mabuk).</li>
                        <li>Menyentuh kemaluan (qubul/dubur) dengan tapak tangan.</li>
                        <li>Bersentuh kulit antara lelaki dan perempuan bukan mahram tanpa berlapik.</li>
                    </ul>
                </div>
            `,"""

content = content.replace('const notaData = {', 'const notaData = {\n' + nota_istinjak + nota_wuduk)

# 3. Add to quizData
quiz_istinjak = """
            istinjak: [
                { q: "Maksud istinjak ialah membersihkan kubul atau ____ selepas membuang air.", options: ["Kaki", "Dubur", "Tangan", "Muka"], answer: 1, explanation: "Istinjak ialah perbuatan membersihkan kubul (depan) dan dubur (belakang) daripada najis." },
                { q: "Hukum beristinjak bagi setiap orang Islam adalah _____.", options: ["Sunat", "Haram", "Makruh", "Wajib"], answer: 3, explanation: "Setiap umat Islam wajib bersihkan diri (beristinjak) selepas membuang air kecil/besar." },
                { q: "Alat yang paling utama dan afdal digunakan untuk beristinjak ialah ____.", options: ["Kertas tisu", "Batu", "Air mutlak", "Daun kering"], answer: 2, explanation: "Walaupun benda kesat boleh digunakan, air mutlak adalah alat bersuci yang paling afdal (terbaik)." },
                { q: "Selain air, kita dibenarkan beristinjak menggunakan benda-benda yang ____.", options: ["Tajam", "Kesat", "Licin", "Wangi"], answer: 1, explanation: "Benda kesat (seperti batu/tisu) boleh menanggalkan najis dengan efektif berbanding benda licin." },
                { q: "Antara berikut, yang manakah BOLEH digunakan untuk beristinjak?", options: ["Kaca", "Kertas surat khabar", "Plastik", "Batu atau kertas tisu"], answer: 3, explanation: "Batu dan kertas tisu adalah benda kesat yang sah digunakan." },
                { q: "Manakah antara berikut HARAM digunakan untuk beristinjak?", options: ["Daun kering", "Kulit kayu", "Makanan dan tulang", "Kertas kosong"], answer: 2, explanation: "Kita diharamkan beristinjak menggunakan makanan (membazir) dan tulang haiwan." },
                { q: "Berapakah bilangan sapuan paling minimum jika beristinjak menggunakan benda kesat?", options: ["1 kali", "2 kali", "3 kali", "7 kali"], answer: 2, explanation: "Syarat istinjak benda kesat: Mesti guna 3 ketul batu yang berlainan atau 1 batu yang ada 3 bucu (3 kali sapuan)." },
                { q: "Boleh ke beristinjak menggunakan kertas surat khabar yang ada ayat al-Quran?", options: ["Boleh jika darurat", "Sunat", "Haram dan berdosa", "Makruh"], answer: 2, explanation: "Haram dan berdosa besar menggunakan helaian yang tertulis padanya ayat al-Quran atau nama-nama Allah." },
                { q: "Syarat beristinjak menggunakan benda kesat ialah najis tersebut mestilah belum ____.", options: ["Kering", "Disiram", "Dilihat", "Busuk"], answer: 0, explanation: "Jika najis itu telah kering atau sudah merebak melepasi kawasan dubur/kubul, maka wajib guna air mutlak." },
                { q: "Kita dilarang beristinjak menggunakan benda yang _____ seperti plastik dan kaca.", options: ["Keras", "Licin", "Kecil", "Berwarna"], answer: 1, explanation: "Benda licin tidak dapat menanggalkan kotoran najis dengan baik." },
                { q: "Apabila masuk ke dalam tandas, kita disunatkan melangkah dengan kaki _____.", options: ["Kanan", "Kiri", "Kedua-duanya", "Lompat"], answer: 1, explanation: "Sunnah Nabi SAW: Masuk tempat kotor (tandas) kaki kiri, keluar kaki kanan." },
                { q: "Apabila keluar dari tandas, kita disunatkan melangkah dengan kaki _____.", options: ["Kiri", "Kanan", "Bebas", "Tengkuk"], answer: 1, explanation: "Sunnah Nabi SAW: Masuk tempat kotor (tandas) kaki kiri, keluar kaki kanan." },
                { q: "Apakah hukum bercakap, menyanyi atau makan di dalam tandas?", options: ["Sunat", "Haram", "Makruh", "Wajib"], answer: 2, explanation: "Makruh bermaksud perbuatan yang tidak disukai Allah, tetapi tidaklah sampai berdosa." },
                { q: "Beristinjak menggunakan tulang binatang adalah _____.", options: ["Sunat", "Harus", "Makruh", "Haram dan tidak sah"], answer: 3, explanation: "Tulang binatang adalah makanan jin, dan nabi melarang kita menggunakan makanan untuk beristinjak." },
                { q: "Doa masuk tandas ialah memohon perlindungan Allah daripada gangguan _____.", options: ["Pencuri", "Syaitan jantan dan betina", "Penyakit", "Gelap"], answer: 1, explanation: "'Allahumma inni a\\'uzubika minal khubuthi wal khabaith' - berlindung dari syaitan jantan dan betina." }
            ],"""

quiz_wuduk = """
            wuduk: [
                { q: "Wuduk dari segi syarak bermaksud membersihkan anggota badan tertentu dengan air mutlak berserta ____.", options: ["Sabun", "Niat", "Tuala", "Syampu"], answer: 1, explanation: "Setiap ibadat dalam Islam mesti disertakan dengan niat untuk membezakannya dengan adat kebiasaan (mandi biasa)." },
                { q: "Hukum mengambil wuduk sebelum menunaikan solat fardu adalah ____.", options: ["Wajib", "Sunat", "Makruh", "Harus"], answer: 0, explanation: "Solat sama sekali tidak sah jika dilakukan tanpa wuduk." },
                { q: "Rukun wuduk mengandungi _____ perkara.", options: ["Empat", "Lima", "Enam", "Tujuh"], answer: 2, explanation: "Ada 6 rukun wuduk: Niat, Muka, Tangan, Kepala, Kaki, Tertib." },
                { q: "Rukun wuduk yang pertama ialah ____.", options: ["Kumur-kumur", "Basuh tangan", "Niat", "Basuh kaki"], answer: 2, explanation: "Niat dibaca di dalam hati serentak dengan air mula menyentuh bahagian muka." },
                { q: "Anggota wuduk yang wajib dibasuh selepas membasuh muka ialah ____.", options: ["Telinga", "Kedua-dua tangan hingga siku", "Kaki", "Kepala"], answer: 1, explanation: "Selepas muka, rukun ketiga ialah membasuh kedua-dua tangan hingga ke paras siku." },
                { q: "Menyapu sedikit air ke atas ____ merupakan salah satu rukun wuduk.", options: ["Kepala", "Telinga", "Hidung", "Mata"], answer: 0, explanation: "Rukun yang keempat ialah menyapu sedikit air ke bahagian kepala (rambut/kulit kepala)." },
                { q: "Batas membasuh kaki ketika berwuduk adalah wajib hingga ke paras ____.", options: ["Lutut", "Paha", "Buku lali", "Tumit"], answer: 2, explanation: "Air mesti diratakan sekurang-kurangnya sehingga melepasi buku lali pada kedua-dua belah kaki." },
                { q: "Rukun wuduk yang terakhir (keenam) ialah _____.", options: ["Tertib", "Doa", "Kumur", "Sapu telinga"], answer: 0, explanation: "Tertib bermaksud melakukan setiap perbuatan di atas mengikut susunan (urutan) yang betul." },
                { q: "Apakah maksud tertib?", options: ["Buat laju-laju", "Melakukan mengikut urutan yang betul", "Berdoa", "Buang air"], answer: 1, explanation: "Tertib bermaksud tidak boleh langkau. Muka dahulu, baru tangan, baru kepala, barulah kaki." },
                { q: "Membasuh telinga, berkumur dan memasukkan air ke hidung adalah perbuatan _____ wuduk.", options: ["Rukun", "Wajib", "Sunat", "Makruh"], answer: 2, explanation: "Perbuatan ini sangat digalakkan (dapat pahala) tetapi wuduk tetap sah jika tidak melakukannya." },
                { q: "Perbuatan kentut atau buang air akan menyebabkan wuduk kita ____.", options: ["Kotor", "Batal", "Sah", "Wangi"], answer: 1, explanation: "Keluar sesuatu dari kubul (depan) atau dubur (belakang) membatalkan wuduk." },
                { q: "Wuduk seseorang akan terbatal jika dia tidur dalam keadaan _____.", options: ["Duduk tetap punggung", "Tidur tidak tetap punggung (baring)", "Bersila tegak", "Berdiri"], answer: 1, explanation: "Tidur baring / mengiring membatalkan wuduk kerana seseorang itu hilang kawalan dan mudah terkentut tanpa sedar." },
                { q: "Menyentuh atau memegang al-Quran bagi orang yang tiada wuduk adalah _____.", options: ["Makruh", "Harus", "Haram", "Sunat"], answer: 2, explanation: "Kita diwajibkan (harus berwuduk) sebelum menyentuh mushaf al-Quran sebagai tanda hormat." },
                { q: "Bolehkah kita mengambil wuduk menggunakan air kopi atau air teh?", options: ["Boleh", "Sunat", "Tidak sah (mesti air mutlak)", "Makruh"], answer: 2, explanation: "Air kopi adalah air bercampur (bukan air mutlak). Wuduk hanya sah menggunakan air mutlak seperti air paip/hujan." },
                { q: "Pitam, gila atau mabuk menyebabkan seseorang itu hilang ____ dan wuduknya serta-merta terbatal.", options: ["Akal", "Harta", "Tenaga", "Ingatan"], answer: 0, explanation: "Hilang akal menyebabkan batalnya wuduk kerana individu tersebut tidak sedar apa yang berlaku pada badannya." }
            ],"""

content = content.replace('const quizData = {', 'const quizData = {\n' + quiz_istinjak + quiz_wuduk)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated feqah.html")

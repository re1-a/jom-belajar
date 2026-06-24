import codecs

new_js = """
// 3. Render Drag & Drop
function renderDragDrop(question, items, zones, correctMapping, explanation) {
    currentAnswer = correctMapping;
    currentExplanation = explanation;
    
    let html = `<h3 style="text-align: center; margin-bottom: 20px;">${question}</h3>`;
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
        renderMCQ(q.q, shuffleArray([...q.options]), q.answer, q.exp);
    } else if (q.type === 'tf') {
        renderTrueFalse(q.q, q.answer, q.exp);
    } else if (q.type === 'drag') {
        renderDragDrop(q.q, shuffleArray([...q.items]), q.zones, q.mapping, q.exp);
    }
}

// UNIT 1: Kemahiran Saintifik
const unit1Data = [
    { type: 'mcq', q: 'Aqil melihat seekor rama-rama yang cantik. Apakah kemahiran yang digunakan?', options: ['Memerhati', 'Mengelas', 'Meramal'], answer: 'Memerhati', exp: 'Melihat adalah salah satu cara untuk memerhati.' },
    { type: 'tf', q: 'Memerhati hanya menggunakan deria penglihatan sahaja.', answer: false, exp: 'Memerhati menggunakan semua deria: melihat, mendengar, merasa, menyentuh, dan menghidu.' },
    { type: 'drag', q: 'Padankan deria dengan organ yang betul', 
      items: [{id:'i1',text:'Melihat',type:'text'}, {id:'i2',text:'Mendengar',type:'text'}, {id:'i3',text:'Menyentuh',type:'text'}],
      zones: [{id:'z1',text:'👁️ Mata'}, {id:'z2',text:'👂 Telinga'}, {id:'z3',text:'✋ Kulit'}],
      mapping: {'i1':'z1', 'i2':'z2', 'i3':'z3'},
      exp: 'Mata untuk melihat, telinga untuk mendengar, kulit untuk menyentuh.' },
    { type: 'mcq', q: 'Mengasingkan daun mengikut bentuk ialah proses...', options: ['Mengukur', 'Mengelas', 'Berkomunikasi'], answer: 'Mengelas', exp: 'Mengelas bermaksud mengasingkan atau mengumpulkan benda mengikut ciri yang sama.' },
    { type: 'tf', q: 'Meramal bermaksud kita meneka sesuatu yang belum berlaku berdasarkan pemerhatian.', answer: true, exp: 'Meramal ialah membuat jangkaan tentang sesuatu kejadian yang akan berlaku.' },
    { type: 'mcq', q: 'Alat apakah yang sesuai untuk mengukur panjang meja?', options: ['Pembaris', 'Bikar', 'Penimbang'], answer: 'Pembaris', exp: 'Pembaris digunakan untuk mengukur panjang.' },
    { type: 'tf', q: 'Menulis keputusan eksperimen dalam jadual ialah kemahiran berkomunikasi.', answer: true, exp: 'Berkomunikasi boleh dilakukan dengan bercakap, menulis, melukis, atau menggunakan jadual/graf.' },
    { type: 'drag', q: 'Kelaskan alat mengikut kegunaannya',
      items: [{id:'i1',text:'Pembaris',type:'text'}, {id:'i2',text:'Pita Pengukur',type:'text'}, {id:'i3',text:'Penimbang',type:'text'}, {id:'i4',text:'Bikar',type:'text'}],
      zones: [{id:'z1',text:'Ukut Panjang'}, {id:'z2',text:'Bukan Ukur Panjang'}],
      mapping: {'i1':'z1', 'i2':'z1', 'i3':'z2', 'i4':'z2'},
      exp: 'Pembaris dan pita pengukur mengukur panjang. Penimbang ukur berat, bikar ukur isipadu.' },
    { type: 'mcq', q: 'Apakah alat untuk mengukur isipadu air yang paling tepat?', options: ['Sudu', 'Cawan', 'Silinder penyukat'], answer: 'Silinder penyukat', exp: 'Silinder penyukat mempunyai senggatan yang piawai.' },
    { type: 'tf', q: 'Kita boleh meramal hujan akan turun jika cuaca mendung gelap.', answer: true, exp: 'Ini adalah satu contoh kemahiran meramal berdasarkan pengalaman lepas.' }
];

function generateUnit1() {
    executeQuestion(unit1Data[currentQuestionIndex - 1]);
}

// UNIT 2: Peraturan Bilik Sains
const unit2Data = [
    { type: 'tf', q: 'Murid boleh masuk ke dalam Bilik Sains tanpa kebenaran guru.', answer: false, exp: 'Kita mesti beratur dan tunggu arahan guru sebelum masuk.' },
    { type: 'tf', q: 'Makan dan minum dilarang sama sekali di dalam Bilik Sains.', answer: true, exp: 'Makanan dan minuman boleh tercemar dengan bahan kimia.' },
    { type: 'mcq', q: 'Apakah yang perlu dilakukan jika buret atau bikar kaca pecah?', options: ['Kutip dengan tangan', 'Laporkan kepada guru', 'Buang dalam bakul sampah segera'], answer: 'Laporkan kepada guru', exp: 'Guru akan membersihkannya menggunakan cara yang selamat.' },
    { type: 'drag', q: 'Kelaskan perbuatan berikut di dalam Bilik Sains',
      items: [{id:'i1',text:'Berlari',type:'text'}, {id:'i2',text:'Buka Tingkap',type:'text'}, {id:'i3',text:'Bermain air',type:'text'}, {id:'i4',text:'Susun kerusi',type:'text'}],
      zones: [{id:'z1',text:'👍 Betul'}, {id:'z2',text:'👎 Salah'}],
      mapping: {'i1':'z2', 'i2':'z1', 'i3':'z2', 'i4':'z1'},
      exp: 'Membuka tingkap untuk pengudaraan dan menyusun kerusi adalah amalan yang baik.' },
    { type: 'mcq', q: 'Mengapakah tingkap dan pintu perlu dibuka semasa di Bilik Sains?', options: ['Supaya nyamuk masuk', 'Untuk pengudaraan yang baik', 'Kerana panas'], answer: 'Untuk pengudaraan yang baik', exp: 'Supaya udara segar dapat masuk dan gas atau bau bahan dapat keluar.' },
    { type: 'tf', q: 'Sampah cecair seperti bahan kimia boleh dibuang ke dalam singki dengan sesuka hati.', answer: false, exp: 'Bahan kimia mesti dibuang ke dalam bekas khas yang disediakan oleh guru.' },
    { type: 'tf', q: 'Bahan pepejal seperti mancis yang telah digunakan perlu dibuang ke dalam bakul sampah.', answer: true, exp: 'Sampah pepejal tidak boleh dibuang ke dalam singki kerana akan menyumbat singki.' },
    { type: 'mcq', q: 'Apakah tindakan yang betul sebelum meninggalkan Bilik Sains?', options: ['Tinggalkan kerusi bersepah', 'Tutup suis kipas dan lampu', 'Biar radas tidak dicuci'], answer: 'Tutup suis kipas dan lampu', exp: 'Pastikan keadaan selamat, kemas, dan menjimatkan elektrik.' },
    { type: 'drag', q: 'Kelaskan barangan ini',
      items: [{id:'i1',text:'Kertas',type:'text'}, {id:'i2',text:'Bahan Kimia',type:'text'}],
      zones: [{id:'z1',text:'Bakul Sampah'}, {id:'z2',text:'Jangan buang sembarangan'}],
      mapping: {'i1':'z1', 'i2':'z2'},
      exp: 'Kertas dibuang di bakul sampah. Bahan kimia mesti diuruskan oleh guru.' },
    { type: 'tf', q: 'Murid perlu memakai pakaian yang kemas dan bertutup semasa melakukan eksperimen tertentu.', answer: true, exp: 'Ini untuk mengelakkan kecederaan akibat terkena bahan berbahaya.' }
];

function generateUnit2() {
    executeQuestion(unit2Data[currentQuestionIndex - 1]);
}

// UNIT 3: Manusia
const unit3Data = [
    { type: 'mcq', q: 'Manusia membiak secara...', options: ['Melahirkan anak', 'Bertelur', 'Biji benih'], answer: 'Melahirkan anak', exp: 'Manusia adalah kumpulan mamalia yang melahirkan anak.' },
    { type: 'drag', q: 'Susun peringkat tumbesaran manusia',
      items: [{id:'i1',text:'Kanak-kanak',type:'text'}, {id:'i2',text:'Bayi',type:'text'}, {id:'i3',text:'Dewasa',type:'text'}, {id:'i4',text:'Remaja',type:'text'}],
      zones: [{id:'z1',text:'Peringkat 1'}, {id:'z2',text:'Peringkat 2'}, {id:'z3',text:'Peringkat 3'}, {id:'z4',text:'Peringkat 4'}],
      mapping: {'i2':'z1', 'i1':'z2', 'i4':'z3', 'i3':'z4'},
      exp: 'Bayi -> Kanak-kanak -> Remaja -> Dewasa' },
    { type: 'tf', q: 'Semakin kita membesar, saiz baju yang kita pakai akan menjadi semakin kecil.', answer: false, exp: 'Tumbesaran menyebabkan saiz badan, tinggi, dan berat kita bertambah.' },
    { type: 'mcq', q: 'Ciri-ciri pewarisan manusia bermaksud kita mewarisi ciri daripada...', options: ['Kawan-kawan', 'Ibu bapa dan keturunan', 'Guru'], answer: 'Ibu bapa dan keturunan', exp: 'Ciri pewarisan seperti warna kulit, jenis rambut, dan warna iris mata diwarisi daripada keturunan kita.' },
    { type: 'tf', q: 'Anak mungkin mempunyai jenis rambut yang keriting seperti datuknya.', answer: true, exp: 'Ciri keturunan juga boleh diwarisi daripada datuk atau nenek.' },
    { type: 'drag', q: 'Kelaskan ciri-ciri manusia',
      items: [{id:'i1',text:'Warna Mata',type:'text'}, {id:'i2',text:'Berat Badan',type:'text'}, {id:'i3',text:'Jenis Rambut',type:'text'}, {id:'i4',text:'Suka Main Bola',type:'text'}],
      zones: [{id:'z1',text:'Diwarisi (Genetik)'}, {id:'z2',text:'Bukan Diwarisi (Genetik)'}],
      mapping: {'i1':'z1', 'i3':'z1', 'i2':'z2', 'i4':'z2'},
      exp: 'Warna mata dan jenis rambut adalah ciri pewarisan. Berat badan dan hobi berubah mengikut gaya hidup.' },
    { type: 'mcq', q: 'Apakah bukti bahawa manusia membesar?', options: ['Menjadi semakin ringan', 'Ketinggian bertambah', 'Suka makan'], answer: 'Ketinggian bertambah', exp: 'Pertambahan tinggi adalah tanda fizikal kita membesar.' },
    { type: 'tf', q: 'Saiz tapak tangan bayi adalah sama dengan saiz tapak tangan orang dewasa.', answer: false, exp: 'Saiz anggota badan juga membesar.' },
    { type: 'mcq', q: 'Seseorang individu yang tidak mewarisi ciri ibu bapanya secara terus, mungkin mewarisi ciri tersebut daripada...', options: ['Kawan rapat', 'Datuk atau Nenek', 'Jiran'], answer: 'Datuk atau Nenek', exp: 'Ciri-ciri ini dinamakan pewarisan keturunan.' },
    { type: 'tf', q: 'Warna kulit seseorang adalah contoh ciri pewarisan.', answer: true, exp: 'Warna kulit dipengaruhi oleh genetik ibu bapa.' }
];

function generateUnit3() {
    executeQuestion(unit3Data[currentQuestionIndex - 1]);
}

// UNIT 4: Haiwan
const unit4Data = [
    { type: 'mcq', q: 'Haiwan apakah yang bertelur dalam kuantiti yang banyak?', options: ['Kucing', 'Penyu', 'Ayam'], answer: 'Penyu', exp: 'Penyu bertelur dalam jumlah yang banyak, kadang-kadang beratus biji, kerana telurnya sering dimakan haiwan lain.' },
    { type: 'tf', q: 'Gajah adalah haiwan yang melahirkan anak.', answer: true, exp: 'Gajah adalah mamalia, jadi ia melahirkan anak.' },
    { type: 'drag', q: 'Kelaskan haiwan mengikut cara pembiakan',
      items: [{id:'i1',text:'Katak',type:'text'}, {id:'i2',text:'Singa',type:'text'}, {id:'i3',text:'Lembu',type:'text'}, {id:'i4',text:'Ular',type:'text'}],
      zones: [{id:'z1',text:'Bertelur'}, {id:'z2',text:'Melahirkan Anak'}],
      mapping: {'i1':'z1', 'i4':'z1', 'i2':'z2', 'i3':'z2'},
      exp: 'Singa dan lembu melahirkan anak. Katak dan ular bertelur.' },
    { type: 'mcq', q: 'Kitaran hidup rama-rama bermula daripada...', options: ['Pupa', 'Telur', 'Beluncas'], answer: 'Telur', exp: 'Kitaran: Telur -> Beluncas (Larva) -> Pupa (Kepompong) -> Rama-rama.' },
    { type: 'drag', q: 'Susun kitaran hidup katak',
      items: [{id:'i1',text:'Berudu',type:'text'}, {id:'i2',text:'Telur',type:'text'}, {id:'i3',text:'Katak Dewasa',type:'text'}, {id:'i4',text:'Anak Katak',type:'text'}],
      zones: [{id:'z1',text:'Mula'}, {id:'z2',text:'Kedua'}, {id:'z3',text:'Ketiga'}, {id:'z4',text:'Akhir'}],
      mapping: {'i2':'z1', 'i1':'z2', 'i4':'z3', 'i3':'z4'},
      exp: 'Telur -> Berudu -> Anak Katak -> Katak Dewasa' },
    { type: 'tf', q: 'Semua anak haiwan menyerupai ibu bapanya sejurus dilahirkan.', answer: false, exp: 'Tidak semua. Contohnya berudu tidak menyerupai katak dewasa, dan beluncas tidak menyerupai rama-rama.' },
    { type: 'mcq', q: 'Anak lembu menyerupai ibunya tetapi...?', options: ['Mempunyai sayap', 'Lebih kecil saiznya', 'Tiada kaki'], answer: 'Lebih kecil saiznya', exp: 'Anak lembu serupa ibunya secara fizikal, cuma saiznya kecil.' },
    { type: 'tf', q: 'Kucing melahirkan anak yang banyak dalam satu masa.', answer: true, exp: 'Kucing melahirkan beberapa ekor anak secara purata 3 hingga 5 ekor sekaligus.' },
    { type: 'drag', q: 'Padankan anak dengan ibunya',
      items: [{id:'i1',text:'Berudu',type:'text'}, {id:'i2',text:'Beluncas',type:'text'}],
      zones: [{id:'z1',text:'Rama-rama'}, {id:'z2',text:'Katak'}],
      mapping: {'i1':'z2', 'i2':'z1'},
      exp: 'Berudu ialah anak katak. Beluncas ialah anak rama-rama.' },
    { type: 'mcq', q: 'Mengapakah burung mengeramkan telurnya?', options: ['Untuk bermain', 'Untuk memanaskan telur supaya menetas', 'Untuk menyorok telur'], answer: 'Untuk memanaskan telur supaya menetas', exp: 'Suhu yang panas membolehkan embrio berkembang dan menetas.' }
];

function generateUnit4() {
    executeQuestion(unit4Data[currentQuestionIndex - 1]);
}

// UNIT 5: Tumbuh-tumbuhan
const unit5Data = [
    { type: 'mcq', q: 'Tumbuh-tumbuhan sangat penting kerana ia membekalkan...', options: ['Pakaian dan elektrik', 'Oksigen dan makanan', 'Plastik'], answer: 'Oksigen dan makanan', exp: 'Tumbuhan menghasilkan oksigen dan menjadi sumber makanan untuk manusia serta haiwan.' },
    { type: 'tf', q: 'Biji benih memerlukan cahaya matahari untuk mula bercambah.', answer: false, exp: 'Biji benih HANYA memerlukan air, udara dan suhu yang sesuai untuk bercambah. Cahaya matahari belum diperlukan sehingga ia mempunyai daun.' },
    { type: 'drag', q: 'Kelaskan keperluan asas',
      items: [{id:'i1',text:'Air',type:'text'}, {id:'i2',text:'Udara',type:'text'}, {id:'i3',text:'Suhu Sesuai',type:'text'}, {id:'i4',text:'Cahaya',type:'text'}],
      zones: [{id:'z1',text:'Untuk Tumbesaran Pokok'}, {id:'z2',text:'Untuk Percambahan Biji Benih'}],
      mapping: {'i4':'z1', 'i1':'z2', 'i2':'z2', 'i3':'z2'},
      exp: 'Biji benih perlukan air, udara, suhu. Pokok perlukan air, udara, cahaya matahari.' },
    { type: 'mcq', q: 'Apakah yang akan bertambah apabila pokok membesar?', options: ['Jumlah daun', 'Warna bunga', 'Jenis buah'], answer: 'Jumlah daun', exp: 'Bila pokok membesar, jumlah daun, saiz daun, lilitan batang dan tingginya bertambah.' },
    { type: 'drag', q: 'Susun urutan tumbesaran pokok',
      items: [{id:'i1',text:'Biji Benih',type:'text'}, {id:'i2',text:'Anak Pokok',type:'text'}, {id:'i3',text:'Pokok Berbunga',type:'text'}],
      zones: [{id:'z1',text:'Mula'}, {id:'z2',text:'Kedua'}, {id:'z3',text:'Akhir'}],
      mapping: {'i1':'z1', 'i2':'z2', 'i3':'z3'},
      exp: 'Biji Benih -> Percambahan -> Anak Pokok -> Pokok Dewasa -> Pokok Berbunga.' },
    { type: 'tf', q: 'Tumbuhan yang tidak disiram air akan mati layu.', answer: true, exp: 'Air merupakan keperluan asas yang sangat penting.' },
    { type: 'mcq', q: 'Jika anak pokok ditutup rapat dengan kotak plastik jernih tanpa lubang, apakah yang akan berlaku?', options: ['Pokok tumbuh tinggi', 'Pokok akan mati', 'Pokok berbunga lebat'], answer: 'Pokok akan mati', exp: 'Ia mati kerana ketiadaan udara segar (karbon dioksida) untuk membuat makanan.' },
    { type: 'tf', q: 'Pokok menghasilkan makanannya sendiri.', answer: true, exp: 'Proses ini dipanggil fotosintesis, menggunakan cahaya matahari.' },
    { type: 'mcq', q: 'Apakah urutan yang betul tumbesaran buah tembikai?', options: ['Biji -> Bunga -> Buah', 'Biji -> Anak pokok -> Bunga -> Buah', 'Bunga -> Biji -> Buah'], answer: 'Biji -> Anak pokok -> Bunga -> Buah', exp: 'Ini adalah kitaran hidup tumbuhan yang berbuah.' },
    { type: 'tf', q: 'Semasa membesar, batang pokok menjadi semakin besar (lilitan bertambah).', answer: true, exp: 'Ya, lilitan batang pokok adalah salah satu penunjuk bahawa ia membesar.' }
];

function generateUnit5() {
    executeQuestion(unit5Data[currentQuestionIndex - 1]);
}

// UNIT 6: Terang dan Gelap
const unit6Data = [
    { type: 'mcq', q: 'Sumber cahaya yang utama untuk bumi ialah...', options: ['Matahari', 'Bulan', 'Lampu suluh'], answer: 'Matahari', exp: 'Matahari ialah sumber cahaya semula jadi yang paling besar dan utama.' },
    { type: 'tf', q: 'Bulan adalah sumber cahaya semula jadi.', answer: false, exp: 'Bulan tidak mengeluarkan cahaya sendiri, ia memantulkan cahaya matahari.' },
    { type: 'drag', q: 'Kelaskan sumber cahaya ini',
      items: [{id:'i1',text:'Lampu',type:'text'}, {id:'i2',text:'Api',type:'text'}, {id:'i3',text:'Batu',type:'text'}, {id:'i4',text:'Matahari',type:'text'}],
      zones: [{id:'z1',text:'Sumber Cahaya'}, {id:'z2',text:'Bukan Sumber Cahaya'}],
      mapping: {'i1':'z1', 'i2':'z1', 'i4':'z1', 'i3':'z2'},
      exp: 'Batu tidak mengeluarkan sebarang cahaya.' },
    { type: 'mcq', q: 'Bayang-bayang terbentuk apabila cahaya...', options: ['Masuk ke dalam mata', 'Dihalang oleh objek', 'Dipantulkan oleh cermin'], answer: 'Dihalang oleh objek', exp: 'Cahaya bergerak lurus. Apabila ia dihalang oleh objek legap, bayang-bayang terhasil di sebalik objek tersebut.' },
    { type: 'tf', q: 'Dalam keadaan terang, kita lebih mudah melihat objek berbanding dalam keadaan gelap.', answer: true, exp: 'Mata memerlukan cahaya untuk melihat sesuatu objek.' },
    { type: 'mcq', q: 'Apakah yang terjadi kepada bayang-bayang apabila lampu suluh didekatkan kepada objek?', options: ['Menjadi kecil', 'Menjadi besar', 'Hilang'], answer: 'Menjadi besar', exp: 'Semakin dekat sumber cahaya dengan objek, semakin besar saiz bayang-bayang.' },
    { type: 'drag', q: 'Permainan bayang-bayang selalunya menggunakan...',
      items: [{id:'i1',text:'Lampu',type:'text'}, {id:'i2',text:'Tangan',type:'text'}, {id:'i3',text:'Air',type:'text'}],
      zones: [{id:'z1',text:'Perlu'}, {id:'z2',text:'Tidak Perlu'}],
      mapping: {'i1':'z1', 'i2':'z1', 'i3':'z2'},
      exp: 'Permainan bayang-bayang memerlukan sumber cahaya dan objek penghalang.' },
    { type: 'tf', q: 'Bayang-bayang bagi bola akan berbentuk bulat.', answer: true, exp: 'Bentuk bayang-bayang menyerupai bentuk objek yang menghalang cahaya.' },
    { type: 'mcq', q: 'Objek yang paling jelas menghasilkan bayang-bayang gelap dinamakan...', options: ['Objek Lut Sinar', 'Objek Legap', 'Objek Kaca'], answer: 'Objek Legap', exp: 'Objek legap (seperti kayu atau logam) menghalang seluruh cahaya daripada melaluinya.' },
    { type: 'tf', q: 'Membaca di tempat gelap boleh merosakkan mata.', answer: true, exp: 'Kekurangan cahaya menyebabkan mata terpaksa bekerja lebih keras dan cepat letih.' }
];

function generateUnit6() {
    executeQuestion(unit6Data[currentQuestionIndex - 1]);
}

// UNIT 7: Elektrik
const unit7Data = [
    { type: 'mcq', q: 'Komponen yang membekalkan tenaga dalam litar ringkas ialah...', options: ['Wayar', 'Suis', 'Sel Kering (Bateri)'], answer: 'Sel Kering (Bateri)', exp: 'Sel kering berfungsi sebagai pembekal tenaga elektrik.' },
    { type: 'drag', q: 'Padankan fungsi komponen elektrik',
      items: [{id:'i1',text:'Menyambung/Memutuskan litar',type:'text'}, {id:'i2',text:'Mengeluarkan cahaya',type:'text'}],
      zones: [{id:'z1',text:'Mentol'}, {id:'z2',text:'Suis'}],
      mapping: {'i1':'z2', 'i2':'z1'},
      exp: 'Suis mengawal aliran elektrik. Mentol bercahaya jika ada elektrik.' },
    { type: 'tf', q: 'Lampu akan menyala jika litar elektrik adalah litar terbuka (suis ditutup/off).', answer: false, exp: 'Lampu hanya menyala dalam litar TERTUTUP (suis dipasang/on) di mana arus elektrik boleh mengalir.' },
    { type: 'mcq', q: 'Jika mentol dalam litar tidak menyala, apakah puncanya?', options: ['Wayar disambung dengan betul', 'Sel kering baharu', 'Mentol telah rosak/terbakar'], answer: 'Mentol telah rosak/terbakar', exp: 'Mentol yang rosak atau sel kering yang kehabisan tenaga menyebabkan litar tidak berfungsi.' },
    { type: 'tf', q: 'Alat permainan kereta kawalan jauh selalunya menggunakan kuasa elektrik daripada sel kering (bateri).', answer: true, exp: 'Ia menggunakan bateri untuk membekalkan elektrik.' },
    { type: 'drag', q: 'Kelaskan barangan',
      items: [{id:'i1',text:'Televisyen',type:'text'}, {id:'i2',text:'Kerusi',type:'text'}, {id:'i3',text:'Mesin Basuh',type:'text'}, {id:'i4',text:'Buku',type:'text'}],
      zones: [{id:'z1',text:'Guna Elektrik'}, {id:'z2',text:'Tidak Guna Elektrik'}],
      mapping: {'i1':'z1', 'i3':'z1', 'i2':'z2', 'i4':'z2'},
      exp: 'Barang elektrik memudahkan urusan harian kita.' },
    { type: 'mcq', q: 'Bahan manakah yang BUKAN merupakan konduktor elektrik (tidak membenarkan elektrik mengalir)?', options: ['Paku Besi', 'Sudu Besi', 'Pemadam Getah'], answer: 'Pemadam Getah', exp: 'Getah, plastik dan kayu adalah penebat (penghalang) elektrik.' },
    { type: 'tf', q: 'Kita tidak boleh menyentuh suis dengan tangan yang basah.', answer: true, exp: 'Air ialah konduktor elektrik yang boleh menyebabkan kita terkena renjatan elektrik.' },
    { type: 'mcq', q: 'Apakah fungsi wayar dalam litar elektrik?', options: ['Menyambungkan komponen litar', 'Membekalkan cahaya', 'Mematikan elektrik'], answer: 'Menyambungkan komponen litar', exp: 'Wayar membenarkan arus elektrik mengalir menghubungkan komponen.' },
    { type: 'tf', q: 'Sel kering mempunyai dua terminal iaitu terminal positif (+) dan terminal negatif (-).', answer: true, exp: 'Pemasangan bateri mesti selari dengan terminal yang betul supaya elektrik dapat mengalir.' }
];

function generateUnit7() {
    executeQuestion(unit7Data[currentQuestionIndex - 1]);
}

// UNIT 8: Campuran
const unit8Data = [
    { type: 'mcq', q: 'Proses memisahkan serbuk besi daripada pasir boleh dilakukan menggunakan...', options: ['Tapis', 'Magnet', 'Tangan'], answer: 'Magnet', exp: 'Magnet menarik serbuk besi dan meninggalkan pasir.' },
    { type: 'tf', q: 'Garam akan hilang (larut) jika dikacau di dalam air.', answer: true, exp: 'Garam adalah bahan yang boleh larut di dalam air.' },
    { type: 'drag', q: 'Kelaskan bahan ini jika dicampurkan dalam air',
      items: [{id:'i1',text:'Gula',type:'text'}, {id:'i2',text:'Pasir',type:'text'}, {id:'i3',text:'Batu',type:'text'}, {id:'i4',text:'Serbuk Milo',type:'text'}],
      zones: [{id:'z1',text:'Boleh Larut'}, {id:'z2',text:'Tidak Larut'}],
      mapping: {'i1':'z1', 'i4':'z1', 'i2':'z2', 'i3':'z2'},
      exp: 'Gula dan milo akan larut di dalam air.' },
    { type: 'mcq', q: 'Cara terbaik untuk mempercepatkan gula larut di dalam air ialah dengan menggunakan air...', options: ['Air Sejuk', 'Air Panas', 'Air Paip Biasa'], answer: 'Air Panas', exp: 'Bahan larut lebih cepat di dalam air panas berbanding air sejuk.' },
    { type: 'tf', q: 'Kita boleh memisahkan campuran campuran kacang hijau dan tepung dengan menapisnya.', answer: true, exp: 'Tepung akan melepasi penapis kerana saiznya kecil, manakala kacang terperangkap.' },
    { type: 'mcq', q: 'Apakah alat yang paling sesuai digunakan untuk mencampurkan warna cecair?', options: ['Sudu (Kacauan)', 'Pisau', 'Gunting'], answer: 'Sudu (Kacauan)', exp: 'Mengacau mempercepatkan campuran sebati.' },
    { type: 'drag', q: 'Padankan kaedah pemisahan',
      items: [{id:'i1',text:'Guna Penapis',type:'text'}, {id:'i2',text:'Guna Tangan',type:'text'}],
      zones: [{id:'z1',text:'Kelilik & Pasir'}, {id:'z2',text:'Air Kelapa & Hampas'}],
      mapping: {'i1':'z2', 'i2':'z1'},
      exp: 'Guna tangan/mengutip sesuai untuk objek besar yang mudah dilihat.' },
    { type: 'tf', q: 'Minyak akan bercampur sebati dengan air jika dikacau dengan lama.', answer: false, exp: 'Minyak tidak larut di dalam air. Ia akan sentiasa timbul di atas air.' },
    { type: 'mcq', q: 'Apakah yang terjadi jika kita memasukkan sehelai daun ke dalam air?', options: ['Daun larut', 'Daun tenggelam', 'Daun timbul (terapung)'], answer: 'Daun timbul (terapung)', exp: 'Daun lebih ringan dan kurang tumpat daripada air.' },
    { type: 'tf', q: 'Sudu besi akan tenggelam kerana ia lebih tumpat daripada air.', answer: true, exp: 'Bahan yang berat dan padat seperti besi akan tenggelam.' }
];

function generateUnit8() {
    executeQuestion(unit8Data[currentQuestionIndex - 1]);
}

// UNIT 9: Bumi
const unit9Data = [
    { type: 'mcq', q: 'Sumber air semula jadi untuk bumi datang dari mana?', options: ['Paip rumah', 'Hujan dan sungai', 'Kolam renang'], answer: 'Hujan dan sungai', exp: 'Hujan turun ke bumi dan mengalir ke sungai, tasik, dan laut sebagai sumber air semula jadi.' },
    { type: 'tf', q: 'Air sungai biasanya akan mengalir menuju ke laut.', answer: true, exp: 'Air mengalir dari kawasan tinggi ke kawasan rendah seperti laut.' },
    { type: 'drag', q: 'Susun urutan kitaran air',
      items: [{id:'i1',text:'Wap Air',type:'text'}, {id:'i2',text:'Awan',type:'text'}, {id:'i3',text:'Hujan',type:'text'}],
      zones: [{id:'z1',text:'Pertama'}, {id:'z2',text:'Kedua'}, {id:'z3',text:'Ketiga'}],
      mapping: {'i1':'z1', 'i2':'z2', 'i3':'z3'},
      exp: 'Air menyejat jadi wap air -> membentuk awan -> awan berat turun hujan.' },
    { type: 'mcq', q: 'Kawasan yang dipenuhi air masin yang sangat luas dinamakan...', options: ['Tasik', 'Laut', 'Sungai'], answer: 'Laut', exp: 'Laut membekalkan air masin yang meliputi 70% bumi.' },
    { type: 'tf', q: 'Udara wujud di sekeliling kita walaupun kita tidak boleh melihatnya.', answer: true, exp: 'Udara tidak boleh dilihat tetapi boleh dirasai apabila angin bertiup.' },
    { type: 'drag', q: 'Kelaskan keadaan udara',
      items: [{id:'i1',text:'Bernafas',type:'text'}, {id:'i2',text:'Angin Kipas',type:'text'}, {id:'i3',text:'Kerusi',type:'text'}],
      zones: [{id:'z1',text:'Udara Bergerak / Angin'}, {id:'z2',text:'Bukan Udara'}],
      mapping: {'i1':'z1', 'i2':'z1', 'i3':'z2'},
      exp: 'Pernafasan dan angin kipas adalah pergerakan udara.' },
    { type: 'mcq', q: 'Tumbuhan memerlukan udara jenis apa untuk membuat makanan (fotosintesis)?', options: ['Oksigen', 'Karbon Dioksida', 'Helium'], answer: 'Karbon Dioksida', exp: 'Tumbuhan menyerap gas karbon dioksida dan membebaskan gas oksigen.' },
    { type: 'tf', q: 'Manusia bernafas menggunakan gas karbon dioksida.', answer: false, exp: 'Manusia bernafas menyedut oksigen dan membuang karbon dioksida.' },
    { type: 'mcq', q: 'Angin ialah...', options: ['Cahaya dari matahari', 'Udara yang bergerak', 'Air yang mengalir'], answer: 'Udara yang bergerak', exp: 'Angin kuat boleh menyebabkan ombak dan tiupan pokok.' },
    { type: 'tf', q: 'Bumi adalah planet yang bulat yang dipenuhi banyak air dan tanah.', answer: true, exp: 'Bentuk bumi adalah sfera (bulat) dan diliputi lebih banyak air daripada daratan.' }
];

function generateUnit9() {
    executeQuestion(unit9Data[currentQuestionIndex - 1]);
}

// UNIT 10: Teknologi
const unit10Data = [
    { type: 'mcq', q: 'Apakah alat yang paling sesuai dipasang untuk membentuk sebuah kereta mainan maya?', options: ['Sayap', 'Tayar (Roda)', 'Bumbung rumah'], answer: 'Tayar (Roda)', exp: 'Tayar atau roda sangat penting untuk membolehkan kenderaan bergerak.' },
    { type: 'tf', q: 'Set binaan perlu dipasang mengikut arahan manual supaya bentuknya menjadi betul.', answer: true, exp: 'Manual bergambar disediakan sebagai panduan asas.' },
    { type: 'drag', q: 'Kelaskan bentuk asas binaan',
      items: [{id:'i1',text:'Bumbung',type:'text'}, {id:'i2',text:'Tayar',type:'text'}, {id:'i3',text:'Tiang',type:'text'}],
      zones: [{id:'z1',text:'Segi Tiga'}, {id:'z2',text:'Bulat'}, {id:'z3',text:'Silinder'}],
      mapping: {'i1':'z1', 'i2':'z2', 'i3':'z3'},
      exp: 'Bumbung selalu piramid/segitiga, tayar itu bulat, dan tiang adalah silinder tinggi.' },
    { type: 'mcq', q: 'Komponen yang digunakan untuk memutarkan tayar dalam set binaan robotik selalunya ialah...', options: ['Motor elektrik', 'Mentol', 'Kertas'], answer: 'Motor elektrik', exp: 'Motor menggunakan elektrik (bateri) untuk menghasilkan pergerakan pusingan.' },
    { type: 'tf', q: 'Selepas selesai bermain set binaan, kita boleh membiarkannya bersepah di atas lantai.', answer: false, exp: 'Komponen perlu dileraikan dan disimpan semula dengan kemas di dalam kotak.' },
    { type: 'mcq', q: 'Apakah faedah membina menggunakan set binaan?', options: ['Meningkatkan selera makan', 'Melatih pemikiran kreatif', 'Membuat mata rabun'], answer: 'Melatih pemikiran kreatif', exp: 'Membina rekaan dapat melatih otak dan tangan bekerjasama.' },
    { type: 'drag', q: 'Padankan fungsi',
      items: [{id:'i1',text:'Buku Manual',type:'text'}, {id:'i2',text:'Kotak Penyimpanan',type:'text'}],
      zones: [{id:'z1',text:'Simpan Komponen'}, {id:'z2',text:'Panduan Pemasangan'}],
      mapping: {'i1':'z2', 'i2':'z1'},
      exp: 'Manual untuk rujukan, kotak untuk simpanan selamat.' },
    { type: 'tf', q: 'Set binaan hanya ada satu cara sahaja untuk dipasang.', answer: false, exp: 'Walaupun ada manual, kita boleh gunakan imaginasi untuk mencipta pelbagai bentuk lain.' },
    { type: 'mcq', q: 'Komponen berbentuk ____ sangat sesuai dijadikan badan kereta mainan.', options: ['Bebola', 'Segi empat', 'Cincin'], answer: 'Segi empat', exp: 'Bentuk blok kuboid (segi empat) stabil sebagai badan kenderaan.' },
    { type: 'tf', q: 'Bahagian yang tajam dalam set binaan perlu dipasang dengan berhati-hati supaya tidak cedera.', answer: true, exp: 'Keselamatan sentiasa diutamakan.' }
];

function generateUnit10() {
    executeQuestion(unit10Data[currentQuestionIndex - 1]);
}
"""

with codecs.open('update_script.py', 'w', encoding='utf-8') as f:
    f.write(f"""
import codecs
with codecs.open('sains-darjah2/script.js', 'a', encoding='utf-8') as f:
    f.write('''{new_js}''')
""")

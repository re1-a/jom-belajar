import re

with open('/Users/re1/Documents/antigravity/modest-bohr/tauhid.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_quiz_data = """const quizData = {
            sifat: [
                { q: "Berapakah bilangan sifat wajib bagi Allah?", options: ["Dua puluh", "Sebelas", "Sepuluh"], answer: 0 },
                { q: "Apakah maksud Wujud?", options: ["Sedia ada", "Ada", "Kekal"], answer: 1 },
                { q: "Qidam ertinya?", options: ["Kekal", "Esa", "Sedia ada"], answer: 2 },
                { q: "Lawan sifat Baqa' ialah?", options: ["Fana'", "Qidam", "Hudus"], answer: 0 },
                { q: "\\"Allah itu Esa\\" adalah pengertian bagi sifat?", options: ["Ta'addud", "Qidam", "Wahdaniyyah"], answer: 2 }
            ],
            malaikat: [
                { q: "Apakah pengertian malaikat?", options: ["Lelaki merdeka yang dipilih Allah", "Makhluk Allah yang dicipta daripada cahaya", "Makhluk yang mempunyai jantina"], answer: 1 },
                { q: "Apakah hukum beriman dengan kewujudan malaikat?", options: ["Sunat", "Wajib", "Harus"], answer: 1 },
                { q: "Berapakah bilangan malaikat yang wajib kita tahu?", options: ["Sepuluh", "Sebelas", "Dua puluh"], answer: 0 },
                { q: "Malaikat yang menyampaikan wahyu ialah?", options: ["Mikail", "Jibril", "Israfil"], answer: 1 },
                { q: "Mencabut nyawa segala makhluk adalah tugas malaikat?", options: ["Mikail", "Izrail", "Raqib"], answer: 1 }
            ],
            kitab: [
                { q: "Kitab suci yang wajib diketahui ada?", options: ["Dua", "Tujuh", "Empat"], answer: 2 },
                { q: "Kitab diturunkan kepada nabi dan?", options: ["Jin", "Rasul", "Malaikat"], answer: 1 },
                { q: "Wajib mengamalkan isi kandungan ___ dengan ikhlas.", options: ["Buku cerita", "Al-Quran", "Majalah"], answer: 1 },
                { q: "Kitab Az-Zabur diturunkan kepada Nabi?", options: ["Nabi Musa AS", "Nabi Daud AS", "Nabi Isa AS"], answer: 1 },
                { q: "Suhuf dari segi bahasa bermaksud?", options: ["Buku tebal", "Lembaran", "Surat khabar"], answer: 1 }
            ]
        };"""

# Replace the quizData block
html = re.sub(r'const quizData = {.*?};', new_quiz_data, html, flags=re.DOTALL)

with open('/Users/re1/Documents/antigravity/modest-bohr/tauhid.html', 'w', encoding='utf-8') as f:
    f.write(html)

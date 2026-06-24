# Workspace Rules

- Selepas setiap kali ubah kod, WAJIB naikkan nombor versi di penjuru atas (contoh: v1.2.1 -> v1.2.2).
  - Naikkan digit terakhir (Patch) untuk baiki *bug* atau ubah teks (contoh: v1.2.2 -> v1.2.3).
  - Naikkan digit tengah (Minor) untuk tambah fungsi/butang baru (contoh: v1.2.3 -> v1.3.0).
  - Naikkan digit pertama (Major) kalau buat *website* tu dari kosong balik (contoh: v1.3.0 -> v2.0.0).

# STYLE LOCK v1.2
# (Mesti IDENTIK di Antigravity agent.md & arahan Google Flow)

0. REFERENS WATAK (sumber utama rupa):
   - DALAM FLOW: WAJIB lampirkan fail referens ni setiap kali jana watak. Imej ini sumber kebenaran utama untuk rupa/likeness.
   - DALAM ANTIGRAVITY (tiada imej): Rujuk seksyen 7 untuk deskripsi bertulis yang sangat terperinci.
   - PENTING: Ikut imej untuk REKA BENTUK & WARNA sahaja — BUKAN pose. Pose mesti berubah ikut arahan prompt.

1. ESTETIK: Mascot anime 2D comel, flat cel shading, line art bersih, warna cerah/tepu. Tiada elemen/tekstur 3D, tiada gradient realistik.

2. OUTLINE: Coklat gelap suam, ketebalan sederhana (BUKAN hitam, bukan navy). Outline mesti cukup JELAS untuk define tepi watak — supaya watak warna cerah (cth fox cream/perut putih) tak hilang atau wash out bila diletak atas latar terang (light mode).

3. PALET (sama untuk semua aset): cream/ivory (badan utama), oren karat / rust-orange (aksen), biru lembut (signature — cth scarf fox).

4. OBJEK TAK BERNYAWA: JANGAN letak muka/ciri wajah pada buah, pokok, alat, prop. Mesti nampak natural.

5. TIADA TEKS DALAM IMEJ: Jangan jana sebarang perkataan/huruf/label/angka dalam gambar. Semua teks ditulis natif dalam kod web (HTML/CSS).
   - **Wajib masuk dalam prompt**: "Absolutely NO text, NO letters, NO numbers, NO written symbols anywhere in the image." (Khasnya kalau ada objek papan hitam/buku).

6. LATAR BELAKANG:
   - **Aset Tunggal (Ikon)**: Latar SOLID HIJAU TERANG (chroma key), tiada bayang. Titik. (Gunakan latar hijau terang untuk SEMUA aset tunggal tanpa pengecualian).
   - **Pemandangan Penuh (Scene/Backdrop)**: Mesti tenang dan tidak berserabut. **Wajib masuk dalam prompt**: "simple, soft, uncluttered background — the Fox and the key object are the clear focal point".

7. WATAK & KONSISTENSI (deskripsi bertulis — wajib dimasukkan dalam prompt):
   - **Fox (Musang Fennec)**: badan gebu cream/ivory, perut putih, telinga besar (luar oren karat, dalam pink lembut), ekor besar gebu hujung oren karat, bintik oren kecil di dahi, mata amber besar berkilat, outline coklat suam, scarf biru WAJIB ada (signature). Muka, proporsi, warna kekal sama.
   - **Boy & Girl**: avatar murid; hanya untuk senario aksi.
   - **Peraturan Penggunaan**: Fox SOLO secara lalai (default) untuk kad nota/kuiz/konsep. PENGECUALIAN: Konsep 'perbandingan' atau 'pewarisan' dibenarkan mempunyai watak Fennec kedua (contoh: dua Fennec berbeza saiz, atau ibu & anak Fennec) untuk mengilustrasikan konsep. Kurangkan bilangan watak serentak untuk elak drift.

8. KESESUAIAN MOD (Light / Dark Mode):
   - Setiap aset imej lutsinar (transparent) **WAJIB diuji dan dipastikan kontrasnya jelas** di atas latar belakang cerah (Light Mode) DAN gelap (Dark Mode). Jika tenggelam warna, ubah warna latar komponen.

9. BOLEH BERUBAH: hanya POSE & EKSPRESI. Reka bentuk watak & gaya kekal tetap.

---
description: Periksa, perbaiki, atau tulis ulang teks bahasa Indonesia menurut EYD V
argument-hint: "[review|fix|rewrite] [file atau teks]"
---

Muat skill `puebi`.

Argumen: $ARGUMENTS

Tentukan mode dari **kata pertama saja**:

- `review` atau `periksa`: periksa ejaan tanpa mengubah file.
- `fix` atau `perbaiki`: perbaiki ejaan dengan perubahan minimal.
- `rewrite` atau `tulis ulang`: tulis ulang agar jelas dan wajar, sambil memperbaiki ejaan.
- Tanpa kata mode, atau kata pertama bukan salah satu di atas: pakai `review` sebagai pilihan aman.

Jika tidak ada argumen, minta teks atau path file, lalu berhenti.

Aturan semua mode:

- Jangan mengubah nama, kutipan, blok kode, kode dalam kalimat, perintah shell, path, URL, alamat email, ID, versi, frontmatter, tujuan tautan, atau isi tabel.
- Jangan menambah fakta, angka, tanggal, kutipan, atau sumber.
- Jika yang diperiksa file dan skrip tersedia, jalankan `python <direktori-skill>/scripts/audit.py <file>`. Gunakan skrip dari direktori skill PUEBI, bukan `scripts/audit.py` dari direktori kerja pengguna.
- Sebutkan kaidah untuk setiap perubahan atau temuan, misalnya `Huruf Kapital 16` atau `KBBI`.

Mode `review`: jangan menyunting file. Kembalikan tabel lokasi, bentuk yang perlu diperbaiki, usulan perbaikan, dan kaidahnya.

Mode `fix`: sunting file langsung, atau kembalikan teks terkoreksi jika argumen berupa teks tempelan. Laporkan path, jumlah perubahan, dan temuan yang belum pasti.

Mode `rewrite`: pertahankan makna, fakta, nada, dan istilah wajib. Rapikan kalimat yang kaku atau bertele-tele. Utamakan kata serapan yang akrab; jangan membuat bentuk serapan baru.

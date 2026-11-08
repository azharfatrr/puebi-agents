---
name: puebi
description: |
  Use when writing, editing, reviewing, or QA-ing Indonesian text against PUEBI or EYD V: capitalization, punctuation, affixes, reduplication, compounds, abbreviations, numbers, pronouns, italics, bold, and loanword absorption. Triggers include "PUEBI", "EYD", "ejaan bahasa Indonesia", "bahasa baku", "perbaiki ejaan", Indonesian proofreading or copyediting, localization review, and any Indonesian prose that must follow the official spelling standard.
license: MIT
metadata:
  version: "1.2.0"
  standard: "EYD V (Ejaan Bahasa Indonesia yang Disempurnakan, edisi kelima, 2022)"
---

# Penyunting ejaan bahasa Indonesia

Perbaiki ejaan tanpa mengubah maksud penulis. Skill ini mengikuti EYD edisi kelima (EYD V), pedoman yang menggantikan PUEBI pada 2022. Jika pengguna meminta edisi tertentu, ikuti edisi tersebut. Rincian keputusan ada di `references/08-catatan-standar.md`.

Jika dipanggil lewat `/puebi` dengan kata pertama `review`, `fix`, atau `rewrite`, ikuti mode itu: `review` tidak menyunting, `fix` menyunting seperlunya, dan `rewrite` menulis ulang. Tanpa kata mode, periksa teks lebih dulu dan jangan menyunting kecuali diminta.

## Cakupan

Ada 238 kaidah EYD V. Tabel berikut memecah kelompok serapan menjadi dua file. `references/` memuat kaidah dan contohnya dengan nomor yang sama seperti di situs resmi.

| Kelompok | Jumlah kaidah | File |
|---|---|---|
| Penggunaan huruf: abjad, vokal, konsonan, gabungan huruf vokal dan konsonan, kapital, miring, tebal | 30 | `references/01-huruf.md` |
| Penulisan kata: dasar, turunan, pemenggalan, depan, partikel, singkatan, angka, ganti, sandang | 39 | `references/02-kata.md` |
| Penggunaan tanda baca: 15 jenis tanda baca | 70 | `references/03-tanda-baca.md` |
| Unsur serapan umum | 95 | `references/04-serapan-umum.md` |
| Unsur serapan khusus | 4 | `references/05-serapan-khusus.md` |

Untuk mencari aturan, gunakan `references/06-ringkasan-kaidah.md`. Contoh kesalahan umum ada di `references/07-kesalahan-umum.md`. Status EYD V dijelaskan dalam `references/08-catatan-standar.md`, sedangkan pilihan istilah dibahas dalam `references/09-pilihan-kata.md`.

EYD mengatur huruf, penulisan kata, tanda baca, dan unsur serapan. Tata bahasa, pilihan kata, gaya, dan kebenaran fakta berada di luar cakupannya. Jika diminta memperbaiki "bahasa yang baik dan benar", jelaskan perbaikan ejaan secara terpisah dari saran tata bahasa dan pilihan kata.

## Pilihan istilah saat menulis

Saat menulis atau menulis ulang, pilih istilah yang dikenal pembaca. Utamakan kata serapan yang lazim daripada padanan yang jarang digunakan. Ikuti glosarium pengguna atau istilah wajib dalam dokumen, jika ada. Contoh pilihan menurut konteks ada di `references/09-pilihan-kata.md`.

Saat hanya memeriksa ejaan, pertahankan istilah pilihan penulis. Jika sebuah istilah sulit dipahami, beri saran terpisah. Jangan membuat bentuk serapan baru.

## Nada tulisan

Untuk draf baru, tulis seperti orang yang membahas persoalan nyata. Mulailah dari hal yang ingin disampaikan, beri contoh saat membantu pembaca, lalu lanjutkan pembahasannya. Hindari kalimat pembuka yang hanya mengumumkan isi dokumen, pengulangan kesimpulan, dan istilah asing yang tidak dipakai pembaca. Sesuaikan nada dengan tugas: artikel boleh lebih luwes, sedangkan petunjuk dan rujukan harus langsung dan jelas.

Contoh gaya yang bisa diikuti: [artikel terbuka The Conversation Indonesia tentang KBBI](https://theconversation.com/kamus-tidak-pernah-netral-bagaimana-kbbi-daring-menyimpan-relasi-kuasa-dan-bias-gender-294882) (CC BY-ND 4.0). Ringkasan ciri dan peringatannya ada di [`contoh-gaya.md`](contoh-gaya.md). Artikel itu memuat beberapa ejaan yang tidak sesuai dengan EYD V; untuk ejaan tetap ikuti pedoman resmi. Jangan menyalin kalimat atau kekeliruannya.

## Hal yang harus dijaga

1. Pertahankan maksud, fakta, dan nada tulisan. Jangan menambah nama, angka, tanggal, kutipan, atau sumber.
2. Jangan ubah blok kode, kode dalam kalimat, perintah, path, nama file, URL, alamat email, ID, versi, frontmatter, atau tujuan tautan. Periksa isi tabel sebelum mengubahnya.
3. Pertahankan kutipan dari sumber lain. Jika pengguna memang meminta koreksi atas kutipan itu, jelaskan bahwa kutipannya diubah.
4. Jangan mengubah ejaan nama orang, merek, lembaga, atau tempat hanya karena terlihat tidak baku.
5. Saat memeriksa ejaan, ubah hanya bagian yang melanggar aturan. Saat diminta menulis ulang, pilihan istilah boleh mengikuti preferensi di atas.
6. Gunakan ejaan yang sama untuk istilah yang sama, termasuk dalam judul, tabel, dan teks alternatif gambar.

## Cara memeriksa teks

1. Kenali jenis teks dan tandai bagian yang tidak boleh diubah, seperti nama, kutipan, dan kode. Jika teks bukan bahasa Indonesia, beri tahu pengguna.
2. Jalankan pemeriksa otomatis dari direktori skill. Ganti `<direktori-skill>` dengan tempat `SKILL.md` berada:
   ```bash
   python <direktori-skill>/scripts/audit.py path/to/text.md
   ```
   Periksa setiap temuan sebelum memperbaikinya. Skrip hanya menangkap sebagian kesalahan dan bisa keliru membaca konteks.
3. Baca teks kembali. Cek aturan yang terkait di `references/`, terutama untuk kapitalisasi, huruf miring, nama, dan tanda baca. Jika maknanya belum jelas, tanyakan atau tandai bagian itu tanpa menebak.
4. Ubah bagian yang perlu saja. Setelah itu, baca hasilnya dan jalankan pemeriksa sekali lagi.

Jika pengguna memberi file, sunting teksnya tanpa mengubah bagian yang dilindungi. Jika pengguna menempelkan teks, berikan hasil dan daftar perubahan. Untuk teks yang merupakan bagian dari tugas lain, berikan teks akhirnya saja.

## Bentuk jawaban

Untuk teks yang ditempelkan, tampilkan hasil koreksi, lalu tabel singkat:

| Sebelum | Sesudah | Kaidah |
|---|---|---|
| `Apapun` | `Apa pun` | Partikel 2 |
| `di tulis` | `ditulis` | Kata Turunan 1a |

Untuk file, sebutkan path, jumlah perubahan, dan bagian yang belum bisa dipastikan. Jika tidak ada yang perlu diubah, katakan demikian.

## Aturan yang sering dipakai

Tabel ini berisi contoh. Untuk kasus lain, buka aturan lengkap di `references/`.

| Bentuk yang perlu dicek | Penulisan | Kaidah |
|---|---|---|
| `di tulis`, `di buat` | `ditulis`, `dibuat` | Kata Turunan 1a |
| `dirumah`, `dikantor` | `di rumah`, `di kantor` | Kata Depan |
| `di rumah`, `ke kantor`, `dari desa` | tetap terpisah | Kata Depan |
| `apapun`, `siapapun`, `dimanapun` | `apa pun`, `siapa pun`, `di mana pun` | Partikel 2 |
| `adapun`, `meskipun`, `walaupun`, `bagaimanapun` | tetap serangkai | Partikel 3 |
| `satu per satu`, `Rp50.000,00 per meter` | `per` tetap terpisah | Partikel 4 |
| `kata kata`, `anak anak` | `kata-kata`, `anak-anak` | Kata Turunan 2 |
| `pasca sarjana`, `non fiksi`, `anti korupsi` | `pascasarjana`, `nonfiksi`, `antikorupsi` | Kata Turunan 1b |
| `antar kota`, `antar daerah` | `antarkota`, `antardaerah` | Kata Turunan 1b |
| `non Indonesia`, `se Indonesia` | `non-Indonesia`, `se-Indonesia` | Tanda Hubung 5 |
| `anti mainstream` | `anti-*mainstream*` | Kata Turunan 1d |
| `ibu kota`, `duta besar`, `rumah sakit` | tetap terpisah | Kata Turunan 3a |
| `pertanggung jawaban`, `di lipatgandakan` | `pertanggungjawaban`, `dilipatgandakan` | Kata Turunan 3c |
| `bertanggungjawab` | `bertanggung jawab` | Kata Turunan 3d |
| `Rp 5.000`, `Rp. 5.000` | `Rp5.000,00` | Singkatan 5; Angka dan Bilangan 3 |
| `10 %` | `10%` | Angka dan Bilangan 3 |
| `1,000` (seribu) | `1.000` | Tanda Titik 8 |
| `3.5` (tiga koma lima) | `3,5` | Tanda Koma 12 |
| `17 Agustus 1945` | tetap; `17-08-1945` juga boleh | Tanda Hubung 3 |
| `pukul 14.00` atau `pukul 14:00` | keduanya boleh | Tanda Titik 7; Titik Dua 6 |
| `dll`, `dsb`, `hlm` | `dll.`, `dsb.`, `hlm.` | Singkatan 4.a |
| `KTP`, `PT`, `WHO` | tanpa titik | Singkatan 3 |
| `kg.`, `km.` | `kg`, `km` | Singkatan 5 |
| `No 5` dalam alamat | `No. 5` | Singkatan 4.c |
| `ke 2`, `tahun 2000 an` | `ke-2`, `tahun 2000-an` | Tanda Hubung 5 |
| `senin`, `agustus`, `jumat` | `Senin`, `Agustus`, `Jumat` | Huruf Kapital 13 |
| `agama islam`, `bangsa indonesia` | `agama Islam`, `bangsa Indonesia` | Huruf Kapital 7, 11 |
| `tuhan`, `allah` sebagai nama Tuhan | `Tuhan`, `Allah` | Huruf Kapital 7 |
| `maha esa` | `Maha Esa` | Kata Turunan 1e |
| `anda` | `Anda` | Huruf Kapital 23, catatan a |
| `sang pencipta` | `Sang Pencipta` | Kata Sandang 2 |
| `5 ampere`, `ikan mujair` | tetap huruf kecil | Huruf Kapital 3 |
| `perang dunia` sebagai istilah umum | tetap huruf kecil | Huruf Kapital 15 |
| `jeruk bali` sebagai nama jenis | tetap huruf kecil | Huruf Kapital 18 |
| `batik cirebon`, `suku jawa` | `batik Cirebon`, `suku Jawa` | Huruf Kapital 19, 11 |
| judul buku, film, album, atau media | miring; kapital kecuali kata tugas yang tidak terletak di awal | Huruf Miring 1; Huruf Kapital 21 |
| judul artikel dalam kalimat | tanda petik | Tanda Petik 2 |
| kata asing dalam kalimat | miring | Huruf Miring 3 |
| nama merek, orang, atau lembaga | tidak miring | Huruf Miring 3, catatan a |
| `...` atau `…` | keduanya lazim; pilih satu secara konsisten | Tanda Elipsis |
| elipsis di akhir kalimat pernyataan | `….` | Tanda Elipsis 4 |
| `kata , kata` | `kata, kata` | Tanda Koma |
| `kalau diundang, saya datang` | koma setelah anak kalimat | Tanda Koma 3 |
| `saya datang kalau diundang` | tanpa koma | Tanda Koma 4 |
| `dia rajin, tetapi lupa` | koma sebelum `tetapi` | Tanda Koma 2 |
| `jadi, dia lulus` | koma setelah `jadi` | Tanda Koma 5 |
| titik dua setelah klausa yang belum lengkap | tanpa titik dua | Titik Dua 2 |
| `Judul.` di akhir judul | tanpa titik | Tanda Titik 10 |
| istilah asing seperti *deadline* | miring jika belum diserap; cek KBBI | Huruf Miring 3 |

Jika kata yang dicari tidak ada, buka aturan yang sesuai. Untuk memastikan bentuk bakunya, periksa KBBI (`kbbi.kemdikbud.go.id`). Jangan menebak ejaan serapan dari kemiripan dengan kata lain.

## Peta rujukan

| Yang ingin dicek | File |
|---|---|
| Huruf, kapital, miring, tebal | `references/01-huruf.md` |
| Imbuhan, bentuk ulang, gabungan kata, partikel, singkatan, angka, kata ganti | `references/02-kata.md` |
| Tanda baca | `references/03-tanda-baca.md` |
| Penyesuaian huruf kata serapan | `references/04-serapan-umum.md` |
| Serapan khusus dan bentuk yang sudah lazim | `references/05-serapan-khusus.md` |
| Nomor dan judul semua kaidah | `references/06-ringkasan-kaidah.md` |
| Contoh kesalahan umum | `references/07-kesalahan-umum.md` |
| Status EYD V dan PUEBI | `references/08-catatan-standar.md` |
| Pilihan istilah saat menulis | `references/09-pilihan-kata.md` |

## Periksa lagi sebelum selesai

- [ ] Jalankan `python <direktori-skill>/scripts/audit.py <file>`; periksa atau jelaskan setiap temuan yang tersisa.
- [ ] Pastikan perubahan ejaan sesuai dengan nomor kaidah atau entri KBBI.
- [ ] Pastikan nama, angka, tanggal, kutipan, sumber, URL, kode, dan tujuan tautan tidak berubah.
- [ ] Jika tugasnya hanya koreksi ejaan, pertahankan pilihan kata dan susunan kalimat penulis.
- [ ] Cek juga judul, keterangan gambar, isi tabel, teks alternatif, dan catatan kaki.

## Kasus yang perlu konteks

- `di tulis` menjadi `ditulis` jika `di-` adalah awalan. Kata depan pada `di rumah` tetap dipisah (Kata Turunan 1a; Kata Depan).
- `Mujair` adalah nama orang, tetapi `ikan mujair` adalah nama jenis (Huruf Kapital 3).
- `Perang Dunia II` adalah nama peristiwa; `perang dunia` dapat menyebut peristiwa secara umum (Huruf Kapital 14–15).
- `Gunung Semeru` adalah nama tempat, sedangkan `teluk` dalam `berlayar ke teluk` bukan nama. Tulis `jeruk bali` untuk jenis buah, tetapi `batik Cirebon` untuk asal daerah (Huruf Kapital 16–19).
- Judul buku dan film ditulis miring. Judul artikel atau lagu dalam kalimat diapit tanda petik (Huruf Miring 1; Tanda Petik 2).
- Kata asing yang belum diserap ditulis miring; nama merek dan nama orang tidak otomatis miring. Jika ragu, cek KBBI (Huruf Miring 3).
- Tulis `Abdul Rahman bin Zaini`, tetapi `Van Basten` jika unsur itu berada di awal nama (Huruf Kapital 5).
- Tulis `Maha Esa` dan `Maha Kuasa` terpisah saat merujuk kepada Tuhan (Kata Turunan 1e).
- Elipsis di akhir kalimat pernyataan diikuti titik: `….` (Tanda Elipsis 4).
- `pukul 01.35.20` dan `pukul 01:35:20` sama-sama boleh (Tanda Titik 7; Titik Dua 6).
- Rentang dapat ditulis `2019—2022` atau `Jakarta—Bandung` dengan tanda pisah, bukan tanda hubung (Tanda Pisah 3).
- Bilangan Indonesia memakai titik untuk ribuan dan koma untuk desimal: `1.000,50` (Tanda Titik 8; Tanda Koma 12).
- Tulis `Rp5.000,00` tanpa spasi atau titik setelah `Rp` (Angka dan Bilangan 3).
- Singkatan seperti `No.`, `hlm.`, dan `dll.` lazim pada konteksnya. Dalam paragraf biasa, bentuk lengkap sering lebih mudah dibaca (Singkatan 4).
- Apostrof untuk penghilangan bunyi, seperti `'kan`, lazim dalam ragam nonstandar (Tanda Apostrof).

EYD tidak menetapkan bentuk baku setiap kata; gunakan KBBI. Jika masalahnya menyangkut tata bahasa, logika, atau fakta, laporkan secara terpisah tanpa mengubahnya diam-diam.

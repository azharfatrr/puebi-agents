# PUEBI

[<kbd>English</kbd>](README.md) | **Bahasa Indonesia**

Skill agen untuk memeriksa ejaan bahasa Indonesia berdasarkan **EYD V**. Bisa dipakai untuk mengoreksi teks yang sudah ada atau memandu penulisan baru.

## Apa kegunaannya

Skill ini memeriksa ejaan bahasa Indonesia berdasarkan **EYD V**, pedoman yang menggantikan PUEBI. Anda bisa memakainya untuk mengoreksi teks yang sudah ada atau sebagai panduan saat menulis. Saat menyusun draf, skill mengutamakan kata serapan yang akrab bagi pembaca daripada padanan yang jarang dipakai.

Pada mode review dan fix, ejaan diperbaiki tanpa mengubah maksud penulis. Pada mode rewrite, susunan kalimat boleh dirapikan asalkan maknanya tetap. Cakupannya meliputi huruf, kapitalisasi, huruf miring, huruf tebal, pembentukan kata, imbuhan, bentuk ulang, gabungan kata, kata depan, partikel, singkatan, akronim, angka, kata ganti, kata sandang, tanda baca, dan unsur serapan.

Acuannya **EYD V** (Ejaan Bahasa Indonesia yang Disempurnakan, edisi kelima), ditetapkan pada 16 Agustus 2022 melalui Keputusan Kepala Badan Pengembangan dan Pembinaan Bahasa Nomor 0424/I/BS.00.01/2022. Nama PUEBI tetap dipakai karena masih dikenal banyak orang.

> [!WARNING]
> **Disclaimer:** Proyek ini dikelola oleh seorang pengembang, bukan ahli bahasa atau praktisi bahasa. Kaidah dan contoh disalin dari situs resmi EYD V, dan masih mungkin ada kekeliruan. Untuk keputusan penting, cocokkan dengan situs resmi EYD V atau KBBI. Koreksi dari praktisi bahasa sangat diterima.

## Sebelum dan sesudah

**Sebelum:**

> ## 5 Tips Menulis Yang Baik.
>
> Menulis adalah keterampilan yang penting , baik untuk pekerjaan maupun kehidupan sehari hari. Banyak orang menganggap bahwa menulis hanya untuk penulis professional, padahal setiap orang bisa menulis.
>
> Apapun profesi anda, luangkan waktu 15 menit setiap hari untuk menulis.

**Sesudah:**

> ## 5 Tips Menulis yang Baik
>
> Menulis adalah keterampilan yang penting, baik untuk pekerjaan maupun kehidupan sehari-hari. Banyak orang menganggap bahwa menulis hanya untuk penulis profesional, padahal setiap orang bisa menulis.
>
> Apa pun profesi Anda, luangkan waktu 15 menit setiap hari untuk menulis.

Saat pengguna hanya meminta pemeriksaan ejaan, skill mempertahankan kata-kata penulis. Preferensi istilah serapan berlaku saat menulis, menulis ulang, atau memilih istilah. Misalnya, `prototipe` bisa lebih mudah dikenali daripada `purwarupa`, tetapi istilah yang diwajibkan pengguna atau dokumen tetap diutamakan. Contoh lain ada di [`references/09-pilihan-kata.md`](references/09-pilihan-kata.md).

## Instalasi

Butuh Node.js 22.20 atau lebih baru untuk `npx skills` dan Python 3.9 atau lebih baru untuk skrip.

Dari repositori ini:

```bash
npx skills add . --global --agent '*'
```

Setelah dipublikasikan, ganti `.` dengan nama repositori:

```bash
npx skills add <pemilik>/<repo> --global --agent '*'
```

Untuk memasang hanya pada satu agen, ganti `'*'` dengan nama agen, misalnya `claude-code` atau `codex`. Anda juga dapat menyalin direktori ini ke direktori skill agen, misalnya `~/.config/opencode/skills/puebi` atau `~/.claude/skills/puebi`.

Lalu pasang perintah garis miring:

```bash
python scripts/install_commands.py --global --agent both
```

Gunakan `--agent opencode` atau `--agent claude` untuk satu agen. Untuk memasang ke proyek tertentu, tambahkan `--scope project --project-dir <path>`. Penginstal tidak menimpa perintah yang sudah ada kecuali diberi `--force`.

Plugin Claude Code menambahkan perintah `/puebi:puebi`. Untuk nama pendek, pakai perintah global `/puebi`.

## Perintah

Hanya ada satu perintah: `/puebi`.

| Argumen | Fungsi |
|---|---|
| tanpa mode | Periksa ejaan, tidak menyunting file. |
| `review` | Sama seperti tanpa mode. |
| `fix` | Perbaiki ejaan dengan perubahan minimal. |
| `rewrite` | Tulis ulang agar jelas dan wajar, ejaan ikut diperbaiki. |

Contoh:

```text
/puebi docs/panduan.md
/puebi review docs/panduan.md
/puebi fix "Kami akan meeting besok."
/puebi rewrite laporan.md
```

Anda juga dapat meminta langsung tanpa perintah:

```text
Perbaiki ejaan docs/panduan.md sesuai EYD V.
```

## Pemeriksa otomatis

Skrip ini menemukan kesalahan ejaan yang bisa diputuskan tanpa membaca seluruh kalimat:

```bash
python scripts/audit.py text.md
python scripts/audit.py text.md --json
python scripts/audit.py text.md --fix
```

`--fix` menerapkan perbaikan mekanis. Periksa hasilnya, terutama jika kata atau angka punya lebih dari satu makna. Skrip melewati blok kode, kode dalam kalimat, frontmatter, URL, alamat email, dan tujuan tautan. Pemeriksaan nama, konteks tanda baca, huruf miring, dan bentuk baku kata tetap memerlukan pembacaan manusia dan KBBI.

Kode keluar `0` berarti tidak ada temuan, `1` berarti masih ada temuan, dan `2` berarti file gagal dibaca.

## Pengujian

```bash
python -m unittest scripts/test_audit.py scripts/test_commands.py -v
python scripts/run_evals.py
python scripts/validate-package.py
```

Kasus di `evals/` memasangkan teks yang perlu dikoreksi dengan hasil yang diharapkan. `run_evals.py` memastikan teks awal memunculkan temuan dan hasilnya lolos pemeriksa otomatis. Perilaku agen masih perlu dibandingkan secara manual dengan file hasil yang diharapkan.

## Batas cakupan

EYD mengatur ejaan, bukan mutu seluruh tulisan. KBBI menentukan bentuk baku suatu kata. Tata bahasa, pilihan kata, terjemahan, dan pemeriksaan fakta memerlukan pekerjaan terpisah. Jika membutuhkan PUEBI edisi lama, sebutkan edisi yang dimaksud.

## Disclaimer

Proyek ini dikelola oleh seorang developer, bukan ahli bahasa atau praktisi bahasa. Kaidah dan contoh disalin dari situs resmi EYD V, dan masih mungkin ada kekeliruan. Untuk keputusan penting, cocokkan dengan [situs resmi EYD V](https://ejaan.kemendikdasmen.go.id/) atau [KBBI](https://kbbi.kemdikbud.go.id/). Koreksi dari guru bahasa, editor, penerjemah, dan pembaca lain sangat diterima.

## Kontribusi

Kontribusi terbuka untuk siapa saja, terutama yang berlatar belakang bahasa Indonesia, linguistik, penyuntingan, atau pengajaran.

- Laporkan kaidah, contoh, atau penjelasan yang keliru dengan nomor kaidah dan tautan sumber.
- Kirim pull request untuk perbaikan ejaan, kalimat, atau format.
- Pertahankan bunyi kaidah EYD V. Jelaskan setiap perubahan pada kaidah atau contoh.
- Jalankan pengujian sebelum membuka pull request.
- Untuk perubahan besar, buka issue lebih dulu agar arahnya bisa dibahas.


## Sumber dan lisensi

- [EYD V](https://ejaan.kemendikdasmen.go.id/)
- [Surat keputusan](https://ejaan.kemendikdasmen.go.id/eyd/surat-keputusan/)
- [KBBI Daring](https://kbbi.kemdikbud.go.id/)

Lisensi MIT berlaku untuk kode dan prosa asli. Teks EYD V yang disalin dan kutipan CC BY-ND tidak termasuk; lihat [NOTICE.md](NOTICE.md).

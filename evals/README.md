# Kasus uji

Setiap folder memuat teks awal dalam `input.md` dan hasil koreksi ejaan dalam `expected.md`.
Jalankan `python scripts/run_evals.py` dari direktori proyek untuk memastikan teks awal memunculkan temuan dan hasilnya tidak memunculkan temuan.

Untuk menguji agen, muat `SKILL.md`, minta agen mengoreksi `input.md`, lalu bandingkan dengan `expected.md`. Periksa juga apakah makna dan bagian yang dilindungi tetap utuh.

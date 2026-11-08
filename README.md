# PUEBI

An agent skill for checking Indonesian spelling against **EYD V**, the standard that replaced PUEBI. It can proofread existing text or guide new writing. When drafting, it prefers familiar loanwords over rare native coinages.

In review and fix modes, it corrects spelling without changing what the text says. In rewrite mode, it may also reorganize sentences for clarity.

**English** | [Bahasa Indonesia](#bahasa-indonesia)

## English

### What it does

The skill corrects spelling without changing what the text says in review and fix modes. It covers letters, capitalization, italics, bold, word formation, affixes, reduplication, compounds, prepositions, particles, abbreviations, acronyms, numbers, pronouns, articles, punctuation, and loanword absorption.

It follows **EYD V** (Ejaan Bahasa Indonesia yang Disempurnakan, fifth edition), set out in Keputusan Kepala Badan Pengembangan dan Pembinaan Bahasa Nomor 0424/I/BS.00.01/2022 on 16 August 2022. PUEBI remains the familiar name, so it stays in the project title.

### Before and after

**Before:**

> ## 5 Tips Menulis Yang Baik.
>
> Menulis adalah keterampilan yang penting , baik untuk pekerjaan maupun kehidupan sehari hari. Banyak orang menganggap bahwa menulis hanya untuk penulis professional, padahal setiap orang bisa menulis.
>
> Apapun profesi anda, luangkan waktu 15 menit setiap hari untuk menulis.

**After:**

> ## 5 Tips Menulis yang Baik
>
> Menulis adalah keterampilan yang penting, baik untuk pekerjaan maupun kehidupan sehari-hari. Banyak orang menganggap bahwa menulis hanya untuk penulis profesional, padahal setiap orang bisa menulis.
>
> Apa pun profesi Anda, luangkan waktu 15 menit setiap hari untuk menulis.

During pure proofreading, the skill keeps the writer's words. The loanword preference applies when writing, rewriting, or choosing terms. For example, `prototipe` may be easier to recognize than `purwarupa`, but terminology required by the user or a document comes first. See [`references/09-pilihan-kata.md`](references/09-pilihan-kata.md).

### Install

Requires Node.js 22.20 or newer for `npx skills` and Python 3.9 or newer for the scripts.

From this repository:

```bash
npx skills add . --global --agent '*'
```

After publication, replace `.` with the repository name:

```bash
npx skills add <owner>/<repo> --global --agent '*'
```

To install only for one agent, replace `'*'` with a name such as `claude-code` or `codex`. You can also copy this directory into an agent skill directory, such as `~/.config/opencode/skills/puebi` or `~/.claude/skills/puebi`.

Then install the slash command:

```bash
python scripts/install_commands.py --global --agent both
```

Use `--agent opencode` or `--agent claude` for one agent. To install into a specific project, add `--scope project --project-dir <path>`. The installer does not overwrite existing commands unless you pass `--force`.

The Claude Code plugin adds the command `/puebi:puebi`. Use the global `/puebi` command for the short name.

### Command

There is one command: `/puebi`.

| Argument | Behavior |
|---|---|
| no mode | Check spelling without editing files. |
| `review` | Same as no mode. |
| `fix` | Fix spelling with minimal changes. |
| `rewrite` | Rewrite for clarity while fixing spelling. |

Examples:

```text
/puebi docs/guide.md
/puebi review docs/guide.md
/puebi fix "Kami akan meeting besok."
/puebi rewrite report.md
```

You can also ask in plain language:

```text
Fix the spelling in docs/guide.md according to EYD V.
```

### Automated checker

The script finds spelling errors that can be decided without reading the whole sentence:

```bash
python scripts/audit.py text.md
python scripts/audit.py text.md --json
python scripts/audit.py text.md --fix
```

`--fix` applies mechanical fixes. Review the result, especially when a word or number has more than one interpretation. The script skips code blocks, inline code, frontmatter, URLs, email addresses, and link targets. Names, punctuation context, italics, and standard word forms still need human review and KBBI.

Exit code `0` means no findings, `1` means findings remain, and `2` means a file could not be read.

### Tests

```bash
python -m unittest scripts/test_audit.py scripts/test_commands.py -v
python scripts/run_evals.py
python scripts/validate-package.py
```

The cases in `evals/` pair text that needs correction with the expected result. `run_evals.py` checks that the input produces findings and the expected file passes the checker. Agent behavior still needs a manual comparison with the expected files.

### Scope and limits

EYD regulates spelling, not the quality of an entire piece of writing. KBBI determines whether a word form is standard. Grammar, word choice, translation, and fact-checking are separate jobs. If you need the older PUEBI edition, say which edition applies.

### Disclaimer

This project is maintained by a developer, not a linguist or language professional. The rules and examples were transcribed from the official EYD V website, and mistakes may remain. When a correction matters, verify it against the [official EYD V site](https://ejaan.kemendikdasmen.go.id/) or [KBBI](https://kbbi.kemdikbud.go.id/). Corrections from language teachers, editors, translators, and other readers are welcome.

### Contributing

Contributions are welcome, especially from people with a background in Indonesian language, linguistics, editing, or teaching.

- Report a wrong rule, example, or explanation with the rule number and a source link.
- Send a pull request for spelling, wording, or formatting fixes.
- Keep quoted EYD V rules faithful. Explain any change to a rule or example.
- Run the tests before opening a pull request.
- For large changes, open an issue first so the direction can be discussed.

You do not need to be a linguist to contribute. Clear examples and careful proofreading help just as much.

### Sources and license

- [EYD V](https://ejaan.kemendikdasmen.go.id/)
- [Decree](https://ejaan.kemendikdasmen.go.id/eyd/surat-keputusan/)
- [KBBI Daring](https://kbbi.kemdikbud.go.id/)

MIT covers the original code and prose. Copied EYD V material and the CC BY-ND excerpt are excluded; see [NOTICE.md](NOTICE.md).

## Bahasa Indonesia

### Apa kegunaannya

Skill ini memeriksa ejaan bahasa Indonesia berdasarkan **EYD V**, pedoman yang menggantikan PUEBI. Anda bisa memakainya untuk mengoreksi teks yang sudah ada atau sebagai panduan saat menulis. Saat menyusun draf, skill mengutamakan kata serapan yang akrab bagi pembaca daripada padanan yang jarang dipakai.

Skill ini mengoreksi ejaan tanpa mengubah maksud penulis pada mode review dan fix. Pada mode rewrite, susunan kalimat boleh dirapikan asalkan maknanya tetap. Cakupannya meliputi huruf, kapitalisasi, huruf miring, huruf tebal, pembentukan kata, imbuhan, bentuk ulang, gabungan kata, kata depan, partikel, singkatan, akronim, angka, kata ganti, kata sandang, tanda baca, dan unsur serapan.

Acuannya **EYD V** (Ejaan Bahasa Indonesia yang Disempurnakan, edisi kelima), ditetapkan pada 16 Agustus 2022 melalui Keputusan Kepala Badan Pengembangan dan Pembinaan Bahasa Nomor 0424/I/BS.00.01/2022. Nama PUEBI tetap dipakai karena masih dikenal banyak orang.

### Sebelum dan sesudah

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

### Instalasi

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

### Perintah

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

### Pemeriksa otomatis

Skrip ini menemukan kesalahan ejaan yang bisa diputuskan tanpa membaca seluruh kalimat:

```bash
python scripts/audit.py text.md
python scripts/audit.py text.md --json
python scripts/audit.py text.md --fix
```

`--fix` menerapkan perbaikan mekanis. Periksa hasilnya, terutama jika kata atau angka punya lebih dari satu makna. Skrip melewati blok kode, kode dalam kalimat, frontmatter, URL, alamat email, dan tujuan tautan. Pemeriksaan nama, konteks tanda baca, huruf miring, dan bentuk baku kata tetap memerlukan pembacaan manusia dan KBBI.

Kode keluar `0` berarti tidak ada temuan, `1` berarti masih ada temuan, dan `2` berarti file gagal dibaca.

### Pengujian

```bash
python -m unittest scripts/test_audit.py scripts/test_commands.py -v
python scripts/run_evals.py
python scripts/validate-package.py
```

Kasus di `evals/` memasangkan teks yang perlu dikoreksi dengan hasil yang diharapkan. `run_evals.py` memastikan teks awal memunculkan temuan dan hasilnya lolos pemeriksa otomatis. Perilaku agen masih perlu dibandingkan secara manual dengan file hasil yang diharapkan.

### Batas cakupan

EYD mengatur ejaan, bukan mutu seluruh tulisan. KBBI menentukan bentuk baku suatu kata. Tata bahasa, pilihan kata, terjemahan, dan pemeriksaan fakta memerlukan pekerjaan terpisah. Jika membutuhkan PUEBI edisi lama, sebutkan edisi yang dimaksud.

### Disclaimer

Proyek ini dikelola oleh seorang pengembang, bukan ahli bahasa atau praktisi bahasa. Kaidah dan contoh disalin dari situs resmi EYD V, dan masih mungkin ada kekeliruan. Untuk keputusan penting, cocokkan dengan [situs resmi EYD V](https://ejaan.kemendikdasmen.go.id/) atau [KBBI](https://kbbi.kemdikbud.go.id/). Koreksi dari guru bahasa, editor, penerjemah, dan pembaca lain sangat diterima.

### Kontribusi

Kontribusi terbuka untuk siapa saja, terutama yang berlatar belakang bahasa Indonesia, linguistik, penyuntingan, atau pengajaran.

- Laporkan kaidah, contoh, atau penjelasan yang keliru dengan nomor kaidah dan tautan sumber.
- Kirim pull request untuk perbaikan ejaan, kalimat, atau format.
- Pertahankan bunyi kaidah EYD V. Jelaskan setiap perubahan pada kaidah atau contoh.
- Jalankan pengujian sebelum membuka pull request.
- Untuk perubahan besar, buka issue lebih dulu agar arahnya bisa dibahas.

Tidak perlu berlatar belakang linguistik untuk ikut berkontribusi. Contoh yang jelas dan pemeriksaan yang teliti sama berharganya.

### Sumber dan lisensi

- [EYD V](https://ejaan.kemendikdasmen.go.id/)
- [Surat keputusan](https://ejaan.kemendikdasmen.go.id/eyd/surat-keputusan/)
- [KBBI Daring](https://kbbi.kemdikbud.go.id/)

Lisensi MIT berlaku untuk kode dan prosa asli. Teks EYD V yang disalin dan kutipan CC BY-ND tidak termasuk; lihat [NOTICE.md](NOTICE.md).

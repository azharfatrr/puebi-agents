#!/usr/bin/env python3
"""Audit Indonesian prose for mechanical PUEBI/EYD V violations.

The script is deliberately conservative. It reports only rules that can be
decided without reading the whole sentence, and it never touches protected
material such as code, URLs, frontmatter, or link targets.

Usage:
    python scripts/audit.py FILE [FILE ...]
    python scripts/audit.py FILE --fix
    python scripts/audit.py FILE --json

Exit status: 0 when clean, 1 when findings remain, 2 on a read error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

MASK = "\x01"

INLINE_PROTECTED = [
    r"`[^`\n]*`",
    r"https?://[^\s<>\"']+",
    r"www\.[^\s<>\"']+",
    r"[\w.+-]+@[\w.-]+\.\w+",
    r"\]\([^)\n]*\)",
    r"<[^>\n]+>",
    r"&[a-zA-Z]+;|&#\d+;",
]

FENCE_RE = re.compile(r"^\s*(```|~~~)")
TABLE_RULE_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")

PUN_JOINED = {
    "adapun",
    "andaipun",
    "ataupun",
    "bagaimanapun",
    "biarpun",
    "jikapun",
    "kalaupun",
    "kendatipun",
    "maupun",
    "meskipun",
    "sekalipun",
    "sementangpun",
    "sungguhpun",
    "walaupun",
}

DI_VERBS = [
    "tulis", "buat", "jual", "beli", "ambil", "beri", "berikan", "guna", "gunakan",
    "kerjakan", "makan", "minum", "baca", "lihat", "dengar", "kirim", "terima",
    "ubah", "pilih", "simpan", "hapus", "tambah", "kurangi", "hitung", "catat",
    "laporkan", "serahkan", "tunjukkan", "jelaskan", "kembangkan", "tingkatkan",
    "hasilkan", "ciptakan", "bangun", "susun", "atur", "kelola", "jalankan",
    "pasang", "lepas", "bersihkan", "periksa", "uji", "coba", "mulai", "akhiri",
    "selesaikan", "tutup", "buka", "minta", "tetapkan", "gunakan", "sediakan",
    "sampaikan", "tawarkan", "temukan", "kunjungi", "hubungi", "bayar", "tagih",
    "masukkan", "keluarkan", "pindahkan", "salin", "tempel", "unduh", "unggah",
    "lakukan", "pakai", "tetapkan",
]

PLACE_WORDS = [
    "rumah", "kantor", "sekolah", "kampus", "kota", "kabupaten", "provinsi",
    "desa", "kelurahan", "kecamatan", "jalan", "pasar", "toko", "masjid", "gereja",
    "pura", "hotel", "bandara", "stasiun", "terminal", "pelabuhan", "lapangan",
    "taman", "museum", "perpustakaan", "laboratorium", "ruang", "gedung", "lantai",
    "sini", "sana", "mana", "dalam", "luar", "atas", "bawah", "antara", "depan",
    "belakang", "samping", "sekitar", "seluruh", "indonesia", "jakarta", "bandung",
    "surabaya", "yogyakarta", "medan", "makassar", "semarang", "denpasar",
]

BOUND_PAIRS = {
    "pasca sarjana": "pascasarjana",
    "pasca panen": "pascapanen",
    "non fiksi": "nonfiksi",
    "non aktif": "nonaktif",
    "anti korupsi": "antikorupsi",
    "anti kekerasan": "antikekerasan",
    "multi bahasa": "multibahasa",
    "multi lateral": "multilateral",
    "sub bagian": "subbagian",
    "ekstra kurikuler": "ekstrakurikuler",
    "infra struktur": "infrastruktur",
    "super cepat": "supercepat",
    "ultra modern": "ultramodern",
    "pra sejarah": "prasejarah",
    "pra jabatan": "prajabatan",
    "pramu saji": "pramusaji",
    "pramu wisata": "pramuwisata",
    "tuna karya": "tunakarya",
    "swa daya": "swadaya",
    "nir laba": "nirlaba",
    "manca negara": "mancanegara",
    "makro ekonomi": "makroekonomi",
    "mikro biologi": "mikrobiologi",
    "semi profesional": "semiprofesional",
    "trans migrasi": "transmigrasi",
    "tri tunggal": "tritunggal",
    "dwi warna": "dwiwarna",
    "eka bahasa": "ekabahasa",
    "nara pidana": "narapidana",
    "pari purna": "paripurna",
    "sapta krida": "saptakrida",
    "wira usaha": "wirausaha",
    "antar kota": "antarkota",
    "antar daerah": "antardaerah",
    "antar bangsa": "antarbangsa",
    "antar golongan": "antargolongan",
    "antar warga": "antarwarga",
    "antar budaya": "antarbudaya",
    "antar umat": "antarumat",
}

REDUPLICATIONS = {
    "kata kata": "kata-kata",
    "anak anak": "anak-anak",
    "buku buku": "buku-buku",
    "orang orang": "orang-orang",
    "rumah rumah": "rumah-rumah",
    "sama sama": "sama-sama",
    "hati hati": "hati-hati",
    "masing masing": "masing-masing",
    "terus menerus": "terus-menerus",
    "porak poranda": "porak-poranda",
    "mondar mandir": "mondar-mandir",
    "sayur mayur": "sayur-mayur",
    "lauk pauk": "lauk-pauk",
    "ramah tamah": "ramah-tamah",
    "serba serbi": "serba-serbi",
    "tunggang langgang": "tunggang-langgang",
    "kupu kupu": "kupu-kupu",
    "cumi cumi": "cumi-cumi",
    "kura kura": "kura-kura",
    "sehari hari": "sehari-hari",
}

LEXICAL = {
    "terimakasih": "terima kasih",
    "silahkan": "silakan",
    "ijasah": "ijazah",
    "ijin": "izin",
    "jaman": "zaman",
    "jendral": "jenderal",
    "karir": "karier",
    "kwalitas": "kualitas",
    "kwitansi": "kuitansi",
    "obyek": "objek",
    "praktek": "praktik",
    "propinsi": "provinsi",
    "resiko": "risiko",
    "sistim": "sistem",
    "tehnik": "teknik",
    "tehnologi": "teknologi",
    "analisa": "analisis",
    "hipotesa": "hipotesis",
    "frekwensi": "frekuensi",
    "aktifitas": "aktivitas",
    "kreatifitas": "kreativitas",
    "produktifitas": "produktivitas",
    "efektifitas": "efektivitas",
    "subyek": "subjek",
    "kongkrit": "konkret",
    "nasehat": "nasihat",
    "hutang": "utang",
    "insyaf": "insaf",
    "hakekat": "hakikat",
    "azas": "asas",
    "managemen": "manajemen",
    "standarisasi": "standardisasi",
    "professional": "profesional",
}

DAYS_MONTHS = [
    "senin", "selasa", "rabu", "kamis", "jumat", "sabtu",
    "januari", "februari", "maret", "april", "mei", "juni", "juli",
    "agustus", "september", "oktober", "november", "desember",
]

ABBREVIATIONS = ["dll", "dsb", "dst", "dkk", "hlm", "ttd", "ybs", "yth"]


@dataclass
class Finding:
    line: int
    column: int
    code: str
    message: str
    suggestion: str = ""
    severity: str = "error"


def is_fence(line: str) -> bool:
    return bool(FENCE_RE.match(line))


def inline_mask(line: str) -> list[bool]:
    protected = [False] * len(line)
    for pattern in INLINE_PROTECTED:
        for match in re.finditer(pattern, line):
            for index in range(match.start(), match.end()):
                protected[index] = True
    return protected


def segments(line: str) -> list[tuple[int, str]]:
    """Return (start, text) for unprotected runs of a line."""
    mask = inline_mask(line)
    result: list[tuple[int, str]] = []
    start = None
    for index, char in enumerate(line):
        if mask[index]:
            if start is not None:
                result.append((start, line[start:index]))
                start = None
        elif start is None:
            start = index
    if start is not None:
        result.append((start, line[start:]))
    return result


def fix_segment(text: str) -> str:
    text = re.sub(r"(?<!\.)\.\.\.(?!\.)", "…", text)

    for wrong, right in LEXICAL.items():
        text = re.sub(rf"\b{wrong}\b", right, text, flags=re.IGNORECASE)

    for wrong, right in BOUND_PAIRS.items():
        text = re.sub(rf"\b{wrong}\b", right, text, flags=re.IGNORECASE)

    for wrong, right in REDUPLICATIONS.items():
        text = re.sub(rf"\b{wrong}\b", right, text, flags=re.IGNORECASE)

    text = re.sub(r"\s+(?=[,.;:!?])", "", text)
    text = re.sub(r"([,;:])(?=[^\s\d)\]}\"'”’»])", r"\1 ", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"(?<=\d)\s+%", "%", text)
    text = re.sub(r"\bRp\.?\s+(?=\d)", "Rp", text)
    text = re.sub(r"\bRp\.(?=\d)", "Rp", text)
    text = re.sub(r"(?<=\d)\.(?=\d+\s*%)", ",", text)

    def split_pun(match: re.Match[str]) -> str:
        word = match.group(1)
        if word.lower() in PUN_JOINED or word.lower() == "pun":
            return match.group(0)
        return f"{word[:-3]} pun"

    text = re.sub(r"\b([A-Za-z]+pun)\b", split_pun, text, flags=re.IGNORECASE)

    verbs = "|".join(sorted(DI_VERBS, key=len, reverse=True))
    text = re.sub(
        rf"\b([Dd])i\s+({verbs})\b",
        lambda m: ("Di" if m.group(1) == "D" else "di") + m.group(2),
        text,
    )

    places = "|".join(sorted(PLACE_WORDS, key=len, reverse=True))
    text = re.sub(
        rf"\bdi({places})\b",
        lambda m: "di " + m.group(1),
        text,
        flags=re.IGNORECASE,
    )

    for word in ABBREVIATIONS:
        text = re.sub(rf"\b({word})(?!\.)(?![A-Za-z])", r"\1.", text)

    text = re.sub(r"\banda\b", "Anda", text)
    for name in DAYS_MONTHS:
        text = re.sub(rf"\b{name}\b", name.capitalize(), text)

    text = re.sub(
        r"\bke\s+(\d+)\s+(abad|tingkat|kalinya|kali|bab|halaman)\b",
        r"ke-\1 \2",
        text,
    )
    text = re.sub(r"\b(\d{4})\s+an\b", r"\1-an", text)
    text = re.sub(r"\bse\s+(Indonesia|ASEAN)\b", r"se-\1", text)
    text = re.sub(r"\b(non|anti|pro|pasca|pan)\s+([A-Z])", r"\1-\2", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


def analyze(text: str, filename: str = "<text>") -> list[Finding]:
    findings: list[Finding] = []
    lines = text.split("\n")
    in_fence = False
    in_frontmatter = False

    for number, raw in enumerate(lines, start=1):
        body = raw[:-1] if raw.endswith("\r") else raw

        if number == 1 and body.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if body.strip() == "---":
                in_frontmatter = False
            continue

        if in_fence:
            if is_fence(body):
                in_fence = False
            continue
        if is_fence(body):
            in_fence = True
            continue

        if "|" in body and TABLE_RULE_RE.match(body):
            continue

        for start, segment in segments(body):
            def add(match: re.Match[str], code: str, message: str, suggestion: str = "", severity: str = "error") -> None:
                findings.append(
                    Finding(number, start + match.start() + 1, code, message, suggestion, severity)
                )

            for match in re.finditer(r"\s+([,.;:!?])", segment):
                add(match, "spasi-sebelum-tanda-baca", "Ada spasi sebelum tanda baca.", "Hapus spasi.")
            for match in re.finditer(r"([,;:])(?=[^\s\d)\]}\"'”’»])", segment):
                add(match, "spasi-setelah-tanda-baca", "Tanda baca langsung diikuti kata.", "Tambahkan satu spasi.")
            for match in re.finditer(r"(?<!\.)\.\.\.(?!\.)", segment):
                add(match, "elipsis-titik", "Elipsis ditulis dengan tiga titik.", "Gunakan karakter … (U+2026).")
            for match in re.finditer(r"(?<=\d)\s+%", segment):
                add(match, "persen-spasi", "Ada spasi sebelum lambang persen.", "Rapatkan: 10%.")
            for match in re.finditer(r"\bRp\.?\s+(?=\d)|\bRp\.(?=\d)", segment):
                add(match, "rupiah-spasi", "Rupiah ditulis tanpa spasi dan tanpa titik.", "Gunakan Rp5.000,00.")
            for match in re.finditer(r"\b\d{1,3}(?:,\d{3})+\b", segment):
                add(
                    match,
                    "ribuan-koma",
                    "Pemisah ribuan tampak memakai koma gaya Inggris.",
                    "Periksa nilainya; bentuk Indonesia memakai titik: 1.000.",
                    "review",
                )
            for match in re.finditer(r"(?<=\d)\.(?=\d+\s*%)", segment):
                add(match, "desimal-persen", "Desimal memakai titik.", "Gunakan koma: 3,5%.")
            for match in re.finditer(r"(?<![\d.])\d+\.\d{1,2}(?![\d.])", segment):
                add(
                    match,
                    "desimal-titik",
                    "Desimal tampak memakai titik gaya Inggris.",
                    "Gunakan koma bila ini bilangan desimal Indonesia.",
                    "review",
                )
            for match in re.finditer(
                r"\b\d+\.\d+\s*(?:kg|km|cm|mm|gram|meter|liter|ml|ha|jam|menit|detik)\b",
                segment,
            ):
                add(match, "desimal-titik", "Desimal memakai titik.", "Gunakan koma: 3,5 km.", "review")

            def check_pun(match: re.Match[str]) -> None:
                word = match.group(1)
                if word.lower() not in PUN_JOINED and word.lower() != "pun":
                    add(match, "partikel-pun", "Partikel pun ditulis terpisah.", f"Tulis: {word[:-3]} pun.")

            for match in re.finditer(r"\b([A-Za-z]+pun)\b", segment, flags=re.IGNORECASE):
                check_pun(match)

            verbs = "|".join(sorted(DI_VERBS, key=len, reverse=True))
            for match in re.finditer(rf"\b[Dd]i\s+({verbs})\b", segment):
                add(match, "di-verba", "Awalan di- ditulis serangkai dengan verba.", "Rapatkan: ditulis.")

            places = "|".join(sorted(PLACE_WORDS, key=len, reverse=True))
            for match in re.finditer(rf"\bdi({places})\b", segment, flags=re.IGNORECASE):
                add(match, "di-tempat", "Kata depan di ditulis terpisah dari tempat.", "Pisahkan: di rumah.")

            for wrong, right in BOUND_PAIRS.items():
                for match in re.finditer(rf"\b{wrong}\b", segment, flags=re.IGNORECASE):
                    add(match, "bentuk-terikat", "Bentuk terikat ditulis serangkai.", f"Tulis: {right}.")

            for wrong, right in REDUPLICATIONS.items():
                for match in re.finditer(rf"\b{wrong}\b", segment, flags=re.IGNORECASE):
                    add(match, "bentuk-ulang", "Bentuk ulang memakai tanda hubung.", f"Tulis: {right}.")

            for word in ABBREVIATIONS:
                for match in re.finditer(rf"\b{word}(?!\.)(?![A-Za-z])", segment):
                    add(match, "singkatan-titik", "Singkatan ini diikuti tanda titik.", f"Tulis: {word}.")

            for match in re.finditer(r"\banda\b", segment):
                add(match, "anda-kapital", "Kata Anda ditulis dengan huruf awal kapital.", "Tulis: Anda.")

            for name in DAYS_MONTHS:
                for match in re.finditer(rf"\b{name}\b", segment):
                    add(match, "hari-bulan-kapital", "Nama hari dan bulan ditulis kapital.", f"Tulis: {name.capitalize()}.")

            for match in re.finditer(r"[ \t]{2,}", segment):
                add(match, "spasi-ganda", "Ada spasi ganda.", "Gunakan satu spasi.")

        heading = re.match(r"^(#{1,6}\s+.+?)\.\s*$", body)
        if heading:
            findings.append(
                Finding(number, len(heading.group(1)) + 1, "judul-titik", "Judul tidak diakhiri tanda titik.", "Hapus titik.")
            )

    return findings


def fix_text(text: str) -> str:
    lines = text.split("\n")
    result: list[str] = []
    in_fence = False
    in_frontmatter = False

    for number, raw in enumerate(lines, start=1):
        newline = "\r" if raw.endswith("\r") else ""
        body = raw[:-1] if newline else raw

        if number == 1 and body.strip() == "---":
            in_frontmatter = True
            result.append(raw)
            continue
        if in_frontmatter:
            if body.strip() == "---":
                in_frontmatter = False
            result.append(raw)
            continue

        if in_fence:
            if is_fence(body):
                in_fence = False
            result.append(raw)
            continue
        if is_fence(body):
            in_fence = True
            result.append(raw)
            continue

        if "|" in body and TABLE_RULE_RE.match(body):
            result.append(raw)
            continue

        parts: list[str] = []
        cursor = 0
        for start, segment in segments(body):
            parts.append(body[cursor:start])
            parts.append(fix_segment(segment))
            cursor = start + len(segment)
        parts.append(body[cursor:])
        fixed = "".join(parts)

        heading = re.match(r"^(#{1,6}\s+.+?)\.\s*$", fixed)
        if heading:
            fixed = heading.group(1)

        result.append(fixed + newline)

    return "\n".join(result)


def format_finding(path: str, finding: Finding) -> str:
    location = f"{path}:{finding.line}:{finding.column}"
    suffix = f" {finding.suggestion}" if finding.suggestion else ""
    return f"{location}: {finding.severity} {finding.code}: {finding.message}{suffix}"


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8-sig")


def write_text(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Indonesian prose for mechanical EYD V violations.")
    parser.add_argument("paths", nargs="+", type=Path, help="files to audit")
    parser.add_argument("--fix", action="store_true", help="apply safe mechanical fixes in place")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    args = parser.parse_args(argv)

    all_findings: list[dict[str, object]] = []
    status = 0

    for path in args.paths:
        try:
            text = read_text(path)
        except (OSError, UnicodeDecodeError) as error:
            print(f"{path}: cannot read: {error}", file=sys.stderr)
            status = 2
            continue

        findings = analyze(text, str(path))
        if args.fix and findings:
            write_text(path, fix_text(text))
            findings = analyze(read_text(path), str(path))

        for finding in findings:
            all_findings.append({"path": str(path), **asdict(finding)})
            if not args.json:
                print(format_finding(str(path), finding))

        if findings:
            status = max(status, 1)

    if args.json:
        print(json.dumps(all_findings, ensure_ascii=False, indent=2))

    if not args.json:
        count = len(all_findings)
        files = len(args.paths)
        print(f"\n{count} temuan pada {files} berkas." if count else f"Bersih: {files} berkas.")

    return status


if __name__ == "__main__":
    raise SystemExit(main())

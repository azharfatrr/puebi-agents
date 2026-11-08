#!/usr/bin/env python3
"""Tests for the PUEBI audit script. Run: python -m unittest scripts/test_audit.py"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit  # noqa: E402


class AuditTests(unittest.TestCase):
    def codes(self, text: str) -> list[str]:
        return [finding.code for finding in audit.analyze(text)]

    def fixed(self, text: str) -> str:
        return audit.fix_text(text)

    def assertClean(self, text: str) -> None:
        self.assertEqual(self.codes(text), [], f"expected clean text, got {self.codes(text)}")

    def test_clean_text_is_clean(self) -> None:
        self.assertClean(
            "Menulis adalah keterampilan yang penting, baik untuk pekerjaan maupun "
            "kehidupan sehari-hari. Apa pun profesi Anda, luangkan waktu 15 menit."
        )

    def test_spacing_before_punctuation(self) -> None:
        self.assertEqual(self.fixed("kata , kata ."), "kata, kata.")
        self.assertIn("spasi-sebelum-tanda-baca", self.codes("kata , kata"))

    def test_spacing_after_punctuation(self) -> None:
        self.assertEqual(self.fixed("satu,dua;tiga"), "satu, dua; tiga")

    def test_ellipsis(self) -> None:
        self.assertEqual(self.fixed("Tunggu..."), "Tunggu…")
        self.assertIn("elipsis-titik", self.codes("Tunggu..."))

    def test_percent_and_rupiah(self) -> None:
        self.assertEqual(self.fixed("naik 10 % dan Rp 5.000"), "naik 10% dan Rp5.000")
        self.assertEqual(self.fixed("Rp. 5.000"), "Rp5.000")

    def test_decimal_percent(self) -> None:
        self.assertEqual(self.fixed("naik 3.5%"), "naik 3,5%")

    def test_thousands_is_review_only(self) -> None:
        findings = audit.analyze("Total 1,000 orang.")
        self.assertEqual([f.code for f in findings], ["ribuan-koma"])
        self.assertEqual(findings[0].severity, "review")
        self.assertEqual(self.fixed("Total 1,000 orang."), "Total 1,000 orang.")

    def test_particle_pun(self) -> None:
        self.assertEqual(self.fixed("Apapun yang terjadi."), "Apa pun yang terjadi.")
        self.assertEqual(self.fixed("Meskipun hujan."), "Meskipun hujan.")
        self.assertEqual(self.fixed("dimanapun"), "di mana pun")

    def test_di_prefix_and_preposition(self) -> None:
        self.assertEqual(self.fixed("di tulis"), "ditulis")
        self.assertEqual(self.fixed("Di buat"), "Dibuat")
        self.assertEqual(self.fixed("dirumah"), "di rumah")
        self.assertEqual(self.fixed("di rumah"), "di rumah")

    def test_reduplication(self) -> None:
        self.assertEqual(self.fixed("kata kata"), "kata-kata")
        self.assertEqual(self.fixed("terus menerus"), "terus-menerus")

    def test_bound_forms(self) -> None:
        self.assertEqual(self.fixed("pasca sarjana"), "pascasarjana")
        self.assertEqual(self.fixed("antar kota"), "antarkota")

    def test_abbreviations(self) -> None:
        self.assertEqual(self.fixed("dll dan dsb"), "dll. dan dsb.")
        self.assertEqual(self.fixed("dll. sudah benar"), "dll. sudah benar")

    def test_capitalization(self) -> None:
        self.assertEqual(self.fixed("anda dan senin"), "Anda dan Senin")
        self.assertEqual(self.fixed("bulan agustus"), "bulan Agustus")

    def test_ordinal_and_year_suffix(self) -> None:
        self.assertEqual(self.fixed("ke 2 abad"), "ke-2 abad")
        self.assertEqual(self.fixed("tahun 2000 an"), "tahun 2000-an")
        self.assertEqual(self.fixed("se Indonesia"), "se-Indonesia")

    def test_heading_period(self) -> None:
        self.assertEqual(self.fixed("## Judul."), "## Judul")

    def test_lexical_forms(self) -> None:
        self.assertEqual(self.fixed("ijasah dan resiko"), "ijazah dan risiko")
        self.assertEqual(self.fixed("terimakasih"), "terima kasih")

    def test_code_and_urls_untouched(self) -> None:
        text = (
            "```\n"
            "di tulis , apapun ... 10 %\n"
            "```\n"
            "Pakai `di tulis` dan https://example.com/a,b,apapun\n"
        )
        self.assertEqual(self.fixed(text), text)
        self.assertEqual(self.codes(text), [])

    def test_frontmatter_untouched(self) -> None:
        text = "---\ntitle: apapun , di tulis\n---\n\nTeks apapun.\n"
        self.assertEqual(self.fixed(text), "---\ntitle: apapun , di tulis\n---\n\nTeks apa pun.\n")

    def test_markdown_table_rule_untouched(self) -> None:
        text = "| a | b |\n|---|---|\n| di tulis | apapun |\n"
        fixed = self.fixed(text)
        self.assertIn("|---|---|", fixed)
        self.assertIn("| ditulis | apa pun |", fixed)

    def test_link_destination_untouched(self) -> None:
        text = "[di tulis](https://example.com/di,tulis)"
        fixed = self.fixed(text)
        self.assertIn("https://example.com/di,tulis", fixed)

    def test_idempotent(self) -> None:
        text = "Apapun , di tulis 10 % pada 3.5% ..."
        once = self.fixed(text)
        self.assertEqual(self.fixed(once), once)

    def test_windows_line_endings_preserved(self) -> None:
        text = "kata , kata\r\napapun\r\n"
        self.assertEqual(self.fixed(text), "kata, kata\r\napa pun\r\n")


if __name__ == "__main__":
    unittest.main()

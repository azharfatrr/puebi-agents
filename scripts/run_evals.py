"""Check that each eval has findings and its expected output is clean."""

from pathlib import Path

from audit import analyze

ROOT = Path(__file__).resolve().parent.parent
cases = sorted((ROOT / "evals").glob("*/input.md"))
assert cases, "No evaluation cases found"
for source in cases:
    expected = source.with_name("expected.md")
    assert expected.is_file(), f"Missing {expected}"
    before = source.read_text(encoding="utf-8")
    after = expected.read_text(encoding="utf-8")
    assert analyze(before), f"No findings in {source}"
    assert not analyze(after), f"Findings remain in {expected}: {analyze(after)}"
    print(f"OK: {source.parent.name}")
print(f"{len(cases)} cases checked")

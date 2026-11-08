"""Validate the agent-skill package without third-party dependencies."""

import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
errors = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


skill = (root / "SKILL.md").read_text(encoding="utf-8")
check(skill.startswith("---\n"), "SKILL.md: frontmatter tidak ditemukan")
check(bool(re.search(r"^name:\s*puebi\s*$", skill, re.M)), "SKILL.md: name harus puebi")
check(bool(re.search(r"^description:\s*\|", skill, re.M)), "SKILL.md: description blok tidak ditemukan")

version = re.search(r'^\s{2}version:\s*"([^"]+)"', skill, re.M)
check(version is not None, "SKILL.md: metadata.version tidak ditemukan")

references = ["01-huruf", "02-kata", "03-tanda-baca", "04-serapan-umum", "05-serapan-khusus", "06-ringkasan-kaidah", "07-kesalahan-umum", "08-catatan-standar", "09-pilihan-kata"]
for name in references:
    check((root / "references" / f"{name}.md").is_file(), f"references/{name}.md tidak ditemukan")

plugin = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
marketplace = json.loads((root / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
check(plugin.get("name") == "puebi", "plugin.json: name harus puebi")
check(plugin.get("version") == (version.group(1) if version else None), "plugin.json: version tidak sama dengan SKILL.md")
check(bool(plugin.get("description")), "plugin.json: description kosong")
check(bool(marketplace.get("description")), "marketplace.json: description kosong")
check(bool(marketplace.get("plugins")), "marketplace.json: plugins kosong")

for key in ("skills", "commands"):
    for entry in plugin.get(key, []):
        path = (root / entry).resolve()
        check(path.exists(), f"plugin.json: path {entry} tidak ditemukan")

command = root / "commands" / "puebi.md"
text = command.read_text(encoding="utf-8")
check(text.startswith("---\n"), "commands/puebi.md: frontmatter tidak ditemukan")
check("description:" in text.split("---", 2)[1], "commands/puebi.md: description tidak ditemukan")
check("$ARGUMENTS" in text, "commands/puebi.md: $ARGUMENTS tidak ditemukan")
mirror = root / ".opencode" / "commands" / "puebi.md"
check(mirror.is_file(), ".opencode/commands/puebi.md tidak ditemukan")
if mirror.is_file():
    check(mirror.read_text(encoding="utf-8") == text, ".opencode/commands/puebi.md tidak sama dengan commands/puebi.md")

rules = (root / "references" / "06-ringkasan-kaidah.md").read_text(encoding="utf-8")
rows = sum(1 for line in rules.splitlines() if line.startswith("| `"))
check(rows == 238, f"06-ringkasan-kaidah.md: {rows} baris, seharusnya 238")

if errors:
    for message in errors:
        print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)

print("PUEBI package valid: 238 indexed rules, nine reference files, one command")

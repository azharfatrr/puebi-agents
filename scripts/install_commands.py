"""Install the PUEBI slash command for OpenCode and Claude Code."""

import argparse
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "commands"
COMMANDS = {"puebi.md": "puebi.md"}


def config_home() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME")
    return Path(xdg) if xdg else Path.home() / ".config"


def target_dirs(agent: str, scope: str, project_dir: Path) -> list[Path]:
    home = Path.home()
    dirs = []
    if agent in ("opencode", "both"):
        base = project_dir / ".opencode" if scope == "project" else config_home() / "opencode"
        dirs.append(base / "commands")
    if agent in ("claude", "both"):
        base = project_dir / ".claude" if scope == "project" else home / ".claude"
        dirs.append(base / "commands")
    return dirs


def write_atomic(dest: Path, data: bytes) -> None:
    handle = tempfile.NamedTemporaryFile(delete=False, dir=dest.parent)
    try:
        handle.write(data)
        handle.close()
        os.replace(handle.name, dest)
    except BaseException:
        handle.close()
        Path(handle.name).unlink(missing_ok=True)
        raise


def install(dest: Path, force: bool, dry_run: bool) -> list[str]:
    messages = []
    if dest.exists() and not dest.is_dir():
        return [f"error    {dest}: bukan direktori"]
    if not dry_run:
        try:
            dest.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            return [f"error    {dest}: {error}"]

    for source_name, target_name in COMMANDS.items():
        source = SOURCE / source_name
        target = dest / target_name
        if target.is_symlink():
            messages.append(f"error    {target}: symlink ditolak")
            continue
        if target.exists() and not target.is_file():
            messages.append(f"error    {target}: bukan file biasa")
            continue
        if target.exists():
            try:
                same = target.read_bytes() == source.read_bytes()
            except OSError as error:
                messages.append(f"error    {target}: {error}")
                continue
            if same:
                messages.append(f"ok       {target}")
                continue
            if not force:
                messages.append(f"skip     {target} (sudah ada; pakai --force untuk menimpa)")
                continue

        if dry_run:
            messages.append(f"would install {target}")
            continue

        try:
            write_atomic(target, source.read_bytes())
            messages.append(f"install  {target}")
        except OSError as error:
            messages.append(f"error    {target}: {error}")
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=["opencode", "claude", "both"], default="both")
    parser.add_argument("--scope", choices=["global", "project"], default="global")
    parser.add_argument("--global", dest="scope", action="store_const", const="global")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    for name in COMMANDS:
        if not (SOURCE / name).is_file():
            print(f"error: {SOURCE / name} tidak ditemukan", file=sys.stderr)
            return 1

    project_dir = args.project_dir.resolve()
    if args.scope == "project" and not project_dir.is_dir():
        print(f"error: direktori proyek tidak ditemukan: {project_dir}", file=sys.stderr)
        return 1

    failed = False
    for dest in target_dirs(args.agent, args.scope, project_dir):
        for message in install(dest, args.force, args.dry_run):
            print(message)
            failed = failed or message.startswith("error")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

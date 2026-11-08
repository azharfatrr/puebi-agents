"""Tests for the command installer."""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import install_commands  # noqa: E402


class InstallCommandsTests(unittest.TestCase):
    def test_project_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dirs = install_commands.target_dirs("both", "project", root)
            self.assertEqual(
                dirs,
                [root / ".opencode" / "commands", root / ".claude" / "commands"],
            )

    def test_opencode_uses_xdg_config_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": tmp}):
                dirs = install_commands.target_dirs("opencode", "global", Path(tmp))
            self.assertEqual(dirs, [Path(tmp) / "opencode" / "commands"])

    def test_install_skip_and_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "commands"
            messages = install_commands.install(dest, False, False)
            self.assertEqual(len(messages), len(install_commands.COMMANDS))
            self.assertTrue(all("install" in line for line in messages))
            self.assertTrue(all("ok" in line for line in install_commands.install(dest, False, False)))

            target = dest / "puebi.md"
            target.write_text("custom", encoding="utf-8")
            self.assertIn("skip", install_commands.install(dest, False, False)[0])

            install_commands.install(dest, True, False)
            self.assertEqual(target.read_bytes(), (install_commands.SOURCE / "puebi.md").read_bytes())

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "commands"
            messages = install_commands.install(dest, False, True)
            self.assertTrue(any("would install" in line for line in messages))
            self.assertFalse(dest.exists())

    def test_target_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "commands"
            (dest / "puebi.md").mkdir(parents=True)
            messages = install_commands.install(dest, True, False)
            self.assertTrue(any(line.startswith("error") for line in messages))


if __name__ == "__main__":
    unittest.main()

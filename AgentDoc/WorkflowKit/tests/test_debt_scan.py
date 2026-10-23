"""Exercise the bundled debt skill's Git scan on real tracked/ignored fixtures."""
from pathlib import Path
import subprocess
import tempfile
import unittest


class DebtScanTests(unittest.TestCase):
    def test_current_legacy_and_untracked_markers_respect_git_ignores(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(['git', 'init', str(root)], check=True, capture_output=True)
            files = {'.gitignore': 'cache/\n',
                     'src/new.py': '# shortcut: bounded data, reassess on latency limit\n',
                     'src/legacy.c': '// ponytail: one client, reassess for multiple clients\n',
                     'cache/generated.py': '# shortcut: ignored fixture, never scanned\n',
                     'README.md': 'shortcut: prose is not a code comment\n'}
            for name, text in files.items():
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text)
            subprocess.run(['git', '-C', str(root), 'add', 'src/legacy.c'], check=True)
            result = subprocess.run(
                ['git', '-C', str(root), 'grep', '--no-index', '--exclude-standard', '-nE',
                 '(#|//|/[*]) ?(shortcut|ponytail):'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('src/new.py', result.stdout)
            self.assertIn('src/legacy.c', result.stdout)
            self.assertNotIn('generated.py', result.stdout)
            self.assertNotIn('README.md', result.stdout)
            self.assertEqual(len(result.stdout.splitlines()), 2)

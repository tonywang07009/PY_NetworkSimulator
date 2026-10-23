"""Upgrade through the installer interface without overwriting local decisions."""
import json
import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import install

CLI = Path(install.__file__).resolve()


class UpgradeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.kit = self.root / 'kit'
        self.repo = self.root / 'project with spaces'
        self.repo.mkdir()
        for name, text in {
            'skills/example/SKILL.md': 'original skill\n',
            'docs/guide.md': 'original guide\n',
            'management/template.md': 'template\n',
            '初次下提示詞模板.txt': 'starter\n',
        }.items():
            p = self.kit / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding='utf-8')
        self.patch = patch.object(install, '__file__', str(self.kit / 'install.py'))
        self.patch.start()
        self.addCleanup(self.patch.stop)
        install.install(self.repo)
        self.skill = self.repo / '.agents/skills/example/SKILL.md'
        self.manifest = self.repo / '.agents/workflow-kit/installation.json'
        self.skill_key = '.agents/skills/example/SKILL.md'

    def change_skill(self):
        (self.kit / 'skills/example/SKILL.md').write_text('new skill\n', encoding='utf-8')

    def snapshot(self):
        return {str(p.relative_to(self.repo)): p.read_bytes()
                for p in self.repo.rglob('*') if p.is_file()}

    def test_fresh_install_records_version_and_deployed_file_hashes(self):
        record = json.loads(self.manifest.read_text())
        self.assertEqual(record['schema_version'], 1)
        self.assertEqual(len(record['package_version']), 64)
        self.assertIn(self.skill_key, record['files'])
        self.assertNotIn('.agents/workflow-kit/installation.json', record['files'])
        for name, digest in record['files'].items():
            self.assertEqual(hashlib.sha256((self.repo / name).read_bytes()).hexdigest(), digest)

    def test_preview_is_read_only_and_update_keeps_backup(self):
        self.change_skill()
        before = self.snapshot()
        preview = install.upgrade(self.repo, dry_run=True)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(preview['actions'][self.skill_key]['action'], 'update')
        self.assertIn('new skill', preview['actions'][self.skill_key]['diff'])
        result = install.upgrade(self.repo)
        self.assertEqual(self.skill.read_text(), 'new skill\n')
        self.assertEqual((Path(result['backup']) / self.skill_key).read_text(), 'original skill\n')

    def test_local_changes_block_writes_until_specific_resolution(self):
        self.change_skill()
        self.skill.write_text('my custom rule\n')
        before = self.snapshot()
        with self.assertRaises(ValueError):
            install.upgrade(self.repo)
        self.assertEqual(self.snapshot(), before)
        install.upgrade(self.repo, keep_local=[self.skill_key])
        self.assertEqual(self.skill.read_text(), 'my custom rule\n')
        self.assertEqual(install.upgrade(self.repo, dry_run=True)['actions'][self.skill_key]['action'],
                         'review')

    def test_explicit_replacement_preserves_reviewed_local_content_in_backup(self):
        self.change_skill()
        self.skill.write_text('custom\n')
        result = install.upgrade(self.repo, replace=[self.skill_key])
        self.assertEqual(self.skill.read_text(), 'new skill\n')
        self.assertEqual((Path(result['backup']) / self.skill_key).read_text(), 'custom\n')

    def test_missing_baseline_requires_review_not_assumed_clean(self):
        self.manifest.unlink()
        self.change_skill()
        before = self.snapshot()
        plan = install.upgrade(self.repo, dry_run=True)
        self.assertFalse(plan['baseline_known'])
        self.assertEqual(plan['actions'][self.skill_key]['action'], 'review')
        with self.assertRaises(ValueError):
            install.upgrade(self.repo)
        self.assertEqual(self.snapshot(), before)

    def test_added_removed_and_locally_deleted_files(self):
        (self.kit / 'docs/new.md').write_text('new\n')
        (self.kit / 'management/template.md').unlink()
        self.skill.unlink()
        with self.assertRaises(ValueError):
            install.upgrade(self.repo)
        result = install.upgrade(self.repo, keep_local=[self.skill_key])
        self.assertFalse(self.skill.exists())
        self.assertTrue((self.repo / '.agents/workflow-kit/docs/new.md').is_file())
        self.assertFalse((self.repo / '.agents/workflow-kit/management/template.md').exists())
        self.assertTrue((Path(result['backup']) /
                         '.agents/workflow-kit/management/template.md').is_file())

    def test_corrupt_or_escaping_manifest_is_rejected_without_writes(self):
        self.change_skill()
        for content in ['{', json.dumps({'schema_version': 1, 'package_version': '0' * 64,
                                        'files': {'../../outside': '0' * 64}})]:
            self.manifest.write_text(content)
            before = self.snapshot()
            with self.assertRaises(ValueError):
                install.upgrade(self.repo)
            self.assertEqual(self.snapshot(), before)

    def test_upgrade_failure_rolls_back_files_and_manifest(self):
        self.change_skill()
        before = self.snapshot()
        real_replace = install.os.replace
        def fail_manifest(src, dst):
            if Path(dst) == self.manifest:
                raise OSError('fixture failure')
            return real_replace(src, dst)
        with patch.object(install.os, 'replace', side_effect=fail_manifest):
            with self.assertRaises(OSError):
                install.upgrade(self.repo)
        self.assertEqual(self.skill.read_bytes(), before[self.skill_key])
        self.assertEqual(self.manifest.read_bytes(),
                         before['.agents/workflow-kit/installation.json'])

    def test_busy_install_lock_and_noop_do_not_change_existing_files(self):
        lock = self.repo / '.agents/.workflow-kit-install.lock'
        lock.write_text('another installer')
        before = self.snapshot()
        with self.assertRaises(ValueError):
            install.upgrade(self.repo)
        self.assertEqual(self.snapshot(), before)
        lock.unlink()
        before = self.snapshot()
        self.assertFalse(install.upgrade(self.repo)['changed'])
        self.assertEqual(self.snapshot(), before)

    def test_symlink_destination_is_rejected(self):
        outside = self.root / 'outside.md'
        outside.write_text('keep')
        self.skill.unlink()
        try:
            self.skill.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f'Symlink privilege unavailable: {exc}')
        self.change_skill()
        with self.assertRaises(ValueError):
            install.upgrade(self.repo)
        self.assertEqual(outside.read_text(), 'keep')

    def test_deployed_link_rewrite_preserves_crlf_and_manifest_hash(self):
        source = self.kit / 'docs/guide.md'
        source.write_bytes(b'[skill](../skills/example/SKILL.md)\r\nsecond line\r\n')
        install.upgrade(self.repo)
        target = self.repo / '.agents/workflow-kit/docs/guide.md'
        self.assertEqual(target.read_bytes(), b'[skill](../../skills/example/SKILL.md)\r\nsecond line\r\n')
        record = json.loads(self.manifest.read_text())
        self.assertEqual(record['files']['.agents/workflow-kit/docs/guide.md'],
                         hashlib.sha256(target.read_bytes()).hexdigest())

    def test_invalid_resolution_and_overlapping_choices_preserve_files(self):
        self.change_skill()
        self.skill.write_text('custom\n')
        for options in [{'keep_local': ['../../outside']},
                        {'keep_local': [self.skill_key], 'replace': [self.skill_key]}]:
            before = self.snapshot()
            with self.assertRaises(ValueError):
                install.upgrade(self.repo, **options)
            self.assertEqual(self.snapshot(), before)

    def test_upgrade_preserves_agent_settings_unmanaged_files_and_external_tools(self):
        untouched = {'AGENTS.md': 'user rules', '.codex/config.toml': 'user config',
                     '.mcp.json': '{"mcpServers":{}}',
                     '.agents/skills/example/user-note.md': 'custom addition',
                     '.tools/external/version.txt': 'keep installed version'}
        for name, text in untouched.items():
            p = self.repo / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        self.change_skill()
        install.upgrade(self.repo)
        for name, text in untouched.items():
            self.assertEqual((self.repo / name).read_text(), text)

    @unittest.skipIf(os.name == 'nt', 'POSIX permission bits')
    def test_existing_file_permissions_survive_update(self):
        self.skill.chmod(0o640)
        self.change_skill()
        install.upgrade(self.repo)
        self.assertEqual(stat.S_IMODE(self.skill.stat().st_mode), 0o640)

    def test_cli_install_and_read_only_upgrade_preview(self):
        repo = self.root / 'CLI project with spaces'
        repo.mkdir()
        installed = subprocess.run([sys.executable, '-B', str(CLI), str(repo)],
                                   capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(installed.returncode, 0, installed.stderr)
        before = {str(p.relative_to(repo)): p.read_bytes() for p in repo.rglob('*') if p.is_file()}
        preview = subprocess.run([sys.executable, '-B', str(CLI), str(repo), '--upgrade', '--dry-run'],
                                 capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertTrue(json.loads(preview.stdout)['baseline_known'])
        self.assertEqual(before, {str(p.relative_to(repo)): p.read_bytes()
                                  for p in repo.rglob('*') if p.is_file()})

    def test_empty_or_missing_target_is_rejected_without_side_effects(self):
        before = self.snapshot()
        for target in (None, '', self.root / 'missing'):
            with self.assertRaises(ValueError):
                install.upgrade(target)
        self.assertEqual(self.snapshot(), before)

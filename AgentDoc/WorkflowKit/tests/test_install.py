"""Installation must deliver references without activating project templates."""
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import install


class InstallTests(unittest.TestCase):
    def test_skills_and_resource_pack_install_without_live_project_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / 'AGENTS.md').write_text('Existing project rules', encoding='utf-8')
            self.assertEqual(install.install(repo), 18)
            self.assertTrue((repo / '.agents/workflow-kit/management/openspec-project/toolbox.md').is_file())
            self.assertTrue((repo / '.agents/workflow-kit/docs/tools.md').is_file())
            self.assertEqual((repo / '.agents/workflow-kit/docs/install.md').read_bytes(),
                             (Path(install.__file__).parent / 'docs/install.md').read_bytes())
            self.assertTrue((repo / '.agents/skills/llm-wiki/SKILL.md').is_file())
            self.assertTrue((repo / '.agents/skills/write-reviewable-pr/references/pr-structure.md').is_file())
            authoring = repo / '.agents/skills/writing-for-agents'
            for name in ('SKILL.md', 'SKILL-MECHANICS.md', 'LICENSE', 'agents/openai.yaml'):
                self.assertEqual((authoring / name).read_bytes(),
                                 (Path(install.__file__).parent / 'skills/writing-for-agents' / name).read_bytes())
            self.assertEqual((repo / '.agents/workflow-kit/docs/output-examples.zh-TW.md').read_bytes(),
                             (Path(install.__file__).parent / 'docs/output-examples.zh-TW.md').read_bytes())
            self.assertEqual((repo / '.agents/workflow-kit/docs/output.md').read_bytes(),
                             (Path(install.__file__).parent / 'docs/output.md').read_bytes())
            self.assertEqual((repo / '.agents/workflow-kit/初次下提示詞模板.txt').read_bytes(),
                             (Path(install.__file__).parent / '初次下提示詞模板.txt').read_bytes())
            self.assertEqual((repo / 'AGENTS.md').read_text(), 'Existing project rules')
            for document in (repo / '.agents/workflow-kit/docs').rglob('*.md'):
                text = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', document.read_text(), flags=re.M | re.S)
                for target in re.findall(r'\]\(([^)]+)\)', text):
                    if '://' not in target and not target.startswith('#'):
                        self.assertTrue((document.parent / target.split('#', 1)[0]).is_file(),
                                        (document.name, target))
            for name in ('openspec', 'wiki', '.workflow', 'interview', '.tools'):
                self.assertFalse((repo / name).exists())

    def test_pr_skill_collision_refuses_before_any_installation(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            existing = repo / '.agents/skills/write-reviewable-pr'
            existing.mkdir(parents=True)
            (existing / 'SKILL.md').write_text('User-owned skill')
            with self.assertRaises(ValueError):
                install.install(repo)
            self.assertEqual((existing / 'SKILL.md').read_text(), 'User-owned skill')
            self.assertEqual(list(existing.parent.iterdir()), [existing])
            self.assertFalse((repo / '.agents/workflow-kit').exists())

    def test_prompt_copy_failure_rolls_back_and_preserves_user_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / 'mine.txt').write_text('Keep')
            with patch.object(install.shutil, 'copy2', side_effect=OSError('Prompt copy failed')):
                with self.assertRaises(OSError):
                    install.install(repo)
            self.assertFalse((repo / '.agents/workflow-kit').exists())
            self.assertEqual(list((repo / '.agents/skills').iterdir()), [])
            self.assertEqual((repo / 'mine.txt').read_text(), 'Keep')

    def test_resource_collision_refuses_before_installing_any_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            resources = repo / '.agents/workflow-kit'
            resources.mkdir(parents=True)
            (resources / 'mine.md').write_text('Keep', encoding='utf-8')
            with self.assertRaises(ValueError):
                install.install(repo)
            self.assertFalse((repo / '.agents/skills').exists())
            self.assertEqual((resources / 'mine.md').read_text(), 'Keep')

    def test_resource_copy_failure_rolls_back_only_new_installation(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / 'mine.md').write_text('Keep', encoding='utf-8')
            real_copy = install.shutil.copytree
            def fail_docs(src, dst, *args, **kwargs):
                if Path(src).name == 'docs':
                    raise OSError('Fixture copy failure')
                return real_copy(src, dst, *args, **kwargs)
            with patch.object(install.shutil, 'copytree', side_effect=fail_docs):
                with self.assertRaises(OSError):
                    install.install(repo)
            self.assertFalse((repo / '.agents/workflow-kit').exists())
            self.assertEqual(list((repo / '.agents/skills').iterdir()), [])
            self.assertEqual((repo / 'mine.md').read_text(), 'Keep')

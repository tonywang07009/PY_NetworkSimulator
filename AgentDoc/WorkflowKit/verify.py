"""Offline integrity, reference topology, generated UI and installation checks."""
from pathlib import Path
import hashlib
import json
import re
import tempfile
import install

root = Path(__file__).resolve().parent
provenance = json.loads((root / 'PROVENANCE.json').read_text(encoding='utf-8'))
lessons = json.loads((root / 'course/lesson.json').read_text(encoding='utf-8'))
assert len(lessons) == 8 and sum(c['minutes'] for c in lessons) == 90
assert len({c['id'] for c in lessons}) == 8
for c in lessons:
    for key in ['goal', 'points', 'demo', 'prompt', 'output', 'stop', 'question', 'answer', 'notes']:
        assert c[key], (c['id'], key)
    for source in c['sources']:
        assert (root / 'course/sources' / source).is_file()
    for ref in c['references']:
        assert (root / ref['path']).is_file(), ref

skills = sorted((root / 'skills').glob('*/SKILL.md'))
assert len(skills) == 18
for entry in skills:
    text = entry.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---', text, re.S)
    assert match, entry
    assert re.search(r'^name: ' + re.escape(entry.parent.name) + r'$', match[1], re.M), entry
    assert re.search(r'^description: .+', match[1], re.M), entry

# Check real local Markdown links, not paths illustrated in inline code/fences.
for base in ('skills', 'docs', 'management'):
    for document in (root / base).rglob('*.md'):
        text = document.read_text(encoding='utf-8')
        text = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in target or target.startswith('#'):
                continue
            target = target.split('#', 1)[0]
            assert (document.parent / target).is_file(), (document, target)
for name in ('workflow', 'llm-wiki', 'skill-evolution'):
    for document in (root / 'skills' / name).rglob('*.md'):
        assert not re.search(r'[\u3400-\u9fff]', document.read_text(encoding='utf-8')), document

index = (root / 'index.html').read_text(encoding='utf-8')
embedded = re.search(r'<script id="lesson-data" type="application/json">(.*?)</script>', index, re.S)
assert embedded and json.loads(embedded[1]) == lessons, 'Run course/build.py'
flow = json.loads((root / 'course/workflow.archify.json').read_text(encoding='utf-8'))
viewer_path = root / 'course/workflow.html'
viewer = viewer_path.read_text(encoding='utf-8')
assert flow['schema_version'] == 2 and flow['diagram_type'] == 'workflow'
assert flow['meta']['quality_profile'] == 'showcase'
ids = [node['id'] for node in flow['nodes']]
assert ids and len(ids) == len(set(ids))
assert set(re.findall(r'<g id="node-[^"]+" data-node-id="([^"]+)"', viewer)) == set(ids)
for edge in flow['edges']:
    assert edge['from'] in ids and edge['to'] in ids
receipt = json.loads((root / 'course/workflow.delivery.json').read_text(encoding='utf-8'))
finalize_path = provenance.get('workflow_quality_and_upgrade', {}).get('archify', {}).get(
    'finalize_receipt', 'course/workflow.finalize.json')
finalize_file = (root / finalize_path).resolve()
assert finalize_file.is_relative_to(root)
finalized = json.loads(finalize_file.read_text(encoding='utf-8'))
assert finalized['ok'] and all(stage['status'] == 'pass' for stage in finalized['stages'].values())
delivery = finalized['stages']['deliver']['receipt']
for name, file in [('specification', root / 'course/workflow.archify.json'), ('artifact', viewer_path)]:
    data = file.read_bytes()
    assert receipt[name]['sha256'] == hashlib.sha256(data).hexdigest(), name
    assert receipt[name]['bytes'] == len(data), name
    assert delivery[name] == receipt[name], name
assert receipt['status'] == 'current' and delivery['ok']
assert delivery['validation']['checksPassed'] == 9
assert delivery['validation']['errors'] == delivery['validation']['warnings'] == 0
# Parse actual HTML elements, excluding JavaScript string templates.
from html.parser import HTMLParser
class LocalLinks(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, url in attrs:
            if key not in ('href', 'src') or not url or ':' in url or url.startswith('#'):
                continue
            assert (self.base / url.split('#', 1)[0].split('?', 1)[0]).is_file(), url
for base, page in [(root, index), (root / 'course', viewer)]:
    parser = LocalLinks()
    parser.base = base
    parser.feed(page)
assert not (root / 'openspec').exists()
assert not (root / 'wiki').exists()

with tempfile.TemporaryDirectory() as tmp:
    repo = Path(tmp)
    assert install.install(repo) == 18
    for source in (root / 'skills').rglob('*'):
        if source.is_file() and '__pycache__' not in source.parts and source.suffix != '.pyc':
            assert (repo / '.agents' / source.relative_to(root)).read_bytes() == source.read_bytes()
    for folder in ('docs', 'management'):
        for source in (root / folder).rglob('*'):
            if source.is_file():
                target = repo / '.agents/workflow-kit' / source.relative_to(root)
                expected = source.read_bytes()
                if folder == 'docs' and source.suffix == '.md':
                    expected = source.read_bytes().decode('utf-8').replace('](../skills/', '](../../skills/').encode('utf-8')
                assert target.read_bytes() == expected
    for name in ('openspec', 'wiki', '.workflow', 'interview', '.tools', 'AGENTS.md'):
        assert not (repo / name).exists()
    assert (repo / '.agents/workflow-kit/初次下提示詞模板.txt').read_bytes() == (root / '初次下提示詞模板.txt').read_bytes()
    before = {str(p.relative_to(repo)): p.read_bytes() for p in repo.rglob('*') if p.is_file()}
    try:
        install.install(repo)
        raise AssertionError('Collision should refuse')
    except ValueError:
        pass
    assert before == {str(p.relative_to(repo)): p.read_bytes() for p in repo.rglob('*') if p.is_file()}
    try:
        install.install(repo / 'missing')
        raise AssertionError('Missing target should refuse')
    except ValueError:
        pass

manifest = root / 'SHA256SUMS'
for line in manifest.read_text(encoding='utf-8').splitlines():
    digest, relative = line.split('  ', 1)
    assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == digest, relative
provenance = json.loads((root / 'PROVENANCE.json').read_text(encoding='utf-8'))
for record in provenance['files']:
    assert hashlib.sha256((root / record['file']).read_bytes()).hexdigest() == record['package_sha256'], record['file']
print('PASS: 8 chapters / 90 minutes / 18 skills / references / generated UI / install / refusal paths / hashes / provenance')

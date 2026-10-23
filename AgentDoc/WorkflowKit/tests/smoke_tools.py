"""External CLI checks in temporary fixtures; no host MCP or personal state."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def run(command, cwd):
    result = subprocess.run([str(arg) for arg in command], cwd=cwd, capture_output=True,
                            text=True, encoding='utf-8', timeout=180,
                            env={**os.environ, 'OPENSPEC_TELEMETRY': '0'})
    if result.returncode:
        raise RuntimeError(f'{command[0]} failed ({result.returncode}):\n{result.stdout}\n{result.stderr}')
    return result.stdout


def smoke(openspec_root=None, archify_root=None):
    node = shutil.which('node')
    symdex = shutil.which('symdex')
    openspec = (Path(openspec_root) / 'node_modules/.bin' /
                ('openspec.cmd' if os.name == 'nt' else 'openspec')) if openspec_root else shutil.which('openspec')
    if not all((node, symdex, openspec)):
        raise ValueError('Node, SymDex and OpenSpec must be installed for this check')
    with tempfile.TemporaryDirectory(prefix='workflow-cli-smoke-') as tmp:
        root = Path(tmp)
        # All generated project files and the SymDex registry stay in this fixture.
        run([openspec, '--version'], root)
        run([openspec, 'init', '--tools', 'none'], root)
        changes = json.loads(run([openspec, 'list', '--json'], root))
        if changes.get('changes') != []:
            raise AssertionError('Expected an empty fixture OpenSpec change list')
        (root / 'app.py').write_text('def workflow_smoke(value):\n    return value + 1\n', encoding='utf-8')
        state = root / '.symdex'
        run([symdex, '--state-dir', state, 'index', root, '--repo', 'workflow-smoke', '--no-embed'], root)
        found = run([symdex, '--state-dir', state, 'find', 'workflow_smoke', '--repo', 'workflow-smoke', '--json'], root)
        if 'workflow_smoke' not in json.dumps(json.loads(found)):
            raise AssertionError('SymDex did not find the fixture symbol')
        checks = ['OpenSpec init/list', 'SymDex index/symbol lookup without embeddings']
        if archify_root:
            cli = Path(archify_root).resolve() / 'archify/bin/archify.mjs'
            spec = Path(__file__).resolve().parents[1] / 'course/workflow.archify.json'
            result = json.loads(run([node, cli, 'validate', 'workflow', spec,
                                     '--quality', 'showcase', '--json'], root))
            if result.get('ok') is not True:
                raise AssertionError('Archify rejected the shipped diagram specification')
            checks.append('Archify specification validation (not browser/render proof)')
        return {'status': 'PASS', 'platform': os.name, 'checks': checks,
                'limits': 'No MCP registration, agent invocation, RTK or native browser acceptance'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--openspec-root', type=Path)
    parser.add_argument('--archify-root', type=Path)
    args = parser.parse_args()
    print(json.dumps(smoke(args.openspec_root, args.archify_root), ensure_ascii=False))

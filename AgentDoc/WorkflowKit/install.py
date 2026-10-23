"""Install the classroom skills without replacing existing skills."""
import argparse
from contextlib import contextmanager
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
import shutil
import sys


MANIFEST = '.agents/workflow-kit/installation.json'


def _root(repo):
    if repo is None or not str(repo).strip():
        raise ValueError('An existing target repository is required')
    repo = Path(repo).expanduser().resolve()
    if not repo.is_dir():
        raise ValueError('Target repository must already exist')
    return repo


def _target(repo, relative):
    parts = PurePosixPath(relative)
    if (not isinstance(relative, str) or not relative or '\\' in relative
            or parts.is_absolute() or '..' in parts.parts or parts.as_posix() != relative):
        raise ValueError('Invalid installation path')
    path = repo
    for part in parts.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError('Installation paths must not contain symlinks')
    if not path.resolve().is_relative_to(repo):
        raise ValueError('Installation path escaped target repository')
    return path


@contextmanager
def _lock(repo):
    lock = _target(repo, '.agents/.workflow-kit-install.lock')
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        stream = lock.open('x', encoding='utf-8')
    except FileExistsError:
        raise ValueError('Another installer is active; inspect its lock before retrying') from None
    try:
        with stream:
            stream.write(str(os.getpid()))
        yield
    finally:
        lock.unlink()


def _package():
    kit = Path(__file__).resolve().parent
    files = {}
    skills = sorted(p for p in (kit / 'skills').iterdir() if (p / 'SKILL.md').is_file())
    roots = [(p, '.agents/skills/' + p.name) for p in skills]
    roots += [(kit / name, '.agents/workflow-kit/' + name) for name in ('docs', 'management')]
    if not skills or any(not folder.is_dir() for folder, _ in roots):
        raise ValueError('Incomplete kit')
    for folder, prefix in roots:
        if folder.is_symlink():
            raise ValueError('Kit source must not contain symlinks')
        for source in sorted(folder.rglob('*')):
            if '__pycache__' in source.parts or source.suffix == '.pyc':
                continue
            if source.is_symlink():
                raise ValueError('Kit source must not contain symlinks')
            if source.is_file():
                data = source.read_bytes()
                if prefix.endswith('/docs') and source.suffix == '.md':
                    data = data.decode('utf-8').replace('](../skills/', '](../../skills/').encode('utf-8')
                files[prefix + '/' + source.relative_to(folder).as_posix()] = data
    prompt = kit / '初次下提示詞模板.txt'
    if not prompt.is_file() or prompt.is_symlink():
        raise ValueError('Starter prompt required as a regular file')
    files['.agents/workflow-kit/' + prompt.name] = prompt.read_bytes()
    return files


def _manifest(files):
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}
    version = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    return {'schema_version': 1, 'package_version': version, 'files': hashes}


def _atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
    try:
        temporary.write_bytes(data)
        if path.exists():
            temporary.chmod(stat.S_IMODE(path.stat().st_mode))
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _json_bytes(record):
    return (json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')


def install(repo):
    repo = _root(repo)
    with _lock(repo):
        return _install(repo)


def _install(repo):
    payload = _package()
    if not repo.is_dir():
        raise ValueError('Target repository must already exist')
    kit = Path(__file__).resolve().parent
    source = kit / 'skills'
    folders = sorted(p for p in source.iterdir() if (p / 'SKILL.md').is_file())
    prompt = kit / '初次下提示詞模板.txt'
    if not folders or not prompt.is_file() or not all((kit / name).is_dir() for name in ('docs', 'management')):
        raise ValueError('Incomplete kit: skills, docs, management and starter prompt are required')
    target = _target(repo, '.agents/skills')
    resources = _target(repo, '.agents/workflow-kit')
    if not target.resolve().is_relative_to(repo) or not resources.resolve().is_relative_to(repo):
        raise ValueError('Installation paths must stay inside the target repository')
    conflicts = [p.name for p in folders if (target / p.name).exists() or (target / p.name).is_symlink()]
    if resources.exists() or resources.is_symlink():
        conflicts.append('.agents/workflow-kit')
    if conflicts:
        raise ValueError('No files changed; existing skills: ' + ', '.join(conflicts))
    target.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for folder in folders:
            dest = target / folder.name
            dest.mkdir()  # Exclusive create also rejects a concurrent installer.
            created.append(dest)
            shutil.copytree(folder, dest, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        resources.mkdir()
        created.append(resources)
        for name in ('docs', 'management'):
            shutil.copytree(kit / name, resources / name)
        # Shared docs move one level farther from skills in the resource pack.
        for document in (resources / 'docs').rglob('*.md'):
            text = document.read_bytes().decode('utf-8')
            relocated = text.replace('](../skills/', '](../../skills/')
            if relocated != text:
                document.write_bytes(relocated.encode('utf-8'))
        shutil.copy2(prompt, resources / prompt.name)
        _atomic(resources / 'installation.json', _json_bytes(_manifest(payload)))
    except Exception:
        for dest in reversed(created):
            if not dest.resolve().is_relative_to(repo):
                raise ValueError('Rollback path escaped target repository')
            shutil.rmtree(dest)
        raise
    return len(folders)


def _baseline(repo):
    path = _target(repo, MANIFEST)
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_text(encoding='utf-8'))
        if (not isinstance(record, dict) or type(record.get('schema_version')) is not int
                or record.get('schema_version') != 1
                or not isinstance(record.get('files'), dict)
                or not re.fullmatch('[0-9a-f]{64}', str(record.get('package_version', '')))):
            raise ValueError('Invalid installation manifest')
        for name, digest in record['files'].items():
            if (not name.startswith(('.agents/skills/', '.agents/workflow-kit/'))
                    or name == MANIFEST or not isinstance(digest, str)
                    or not re.fullmatch('[0-9a-f]{64}', digest)):
                raise ValueError('Invalid managed file')
            _target(repo, name)
        fingerprint = hashlib.sha256(json.dumps(record['files'], sort_keys=True).encode()).hexdigest()
        if fingerprint != record['package_version']:
            raise ValueError('Installation manifest fingerprint does not match its file records')
        return record
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError('Invalid installation manifest; preserve it for inspection') from exc


def _contents(path):
    if path.exists() and not path.is_file():
        raise ValueError(f'Expected a regular managed file: {path}')
    return path.read_bytes() if path.exists() else None


def _plan(repo, keep_local, replace):
    payload = _package()
    baseline = _baseline(repo)
    old = baseline['files'] if baseline else {}
    keep_local, replace = set(keep_local), set(replace)
    if keep_local & replace:
        raise ValueError('A path cannot be both kept and replaced')
    plan = {'baseline_known': baseline is not None,
            'package_version': _manifest(payload)['package_version'], 'actions': {}}
    originals = {}
    for name in sorted(set(old) | set(payload)):
        local = _contents(_target(repo, name))
        originals[name] = local
        desired = payload.get(name)
        digest = hashlib.sha256(local).hexdigest() if local is not None else None
        if local == desired:
            action = 'identical'
        elif name not in old and local is None:
            action = 'add'
        elif name in old and digest == old[name]:
            action = 'remove' if desired is None else 'update'
        else:
            action = 'review'
        if name in keep_local | replace:
            if action != 'review':
                raise ValueError(f'Resolution no longer applies; inspect a fresh preview: {name}')
            action = 'keep' if name in keep_local else ('remove' if desired is None else 'update')
        item = {'action': action, 'baseline': old.get(name), 'local': digest,
                'incoming': hashlib.sha256(desired).hexdigest() if desired is not None else None}
        if local != desired:
            try:
                item['diff'] = ''.join(difflib.unified_diff(
                    (local or b'').decode('utf-8').splitlines(keepends=True),
                    (desired or b'').decode('utf-8').splitlines(keepends=True),
                    fromfile='local/' + name, tofile='incoming/' + name))
            except UnicodeDecodeError:
                item['diff'] = 'Binary content differs; compare hashes and files.'
        plan['actions'][name] = item
    if (keep_local | replace) - set(plan['actions']):
        raise ValueError('Resolution references a file outside this upgrade')
    return plan, payload, baseline, originals


def upgrade(repo, *, dry_run=False, keep_local=(), replace=()):
    """Preview or apply an explicitly requested kit upgrade; never update tools."""
    repo = _root(repo)
    if dry_run:
        return _plan(repo, keep_local, replace)[0]
    with _lock(repo):
        manifest_before = _contents(_target(repo, MANIFEST))
        plan, payload, baseline, originals = _plan(repo, keep_local, replace)
        pending = [name for name, item in plan['actions'].items() if item['action'] == 'review']
        if pending:
            raise ValueError('No files changed; review local/unknown files with --dry-run: '
                             + ', '.join(pending))
        changes = [name for name, item in plan['actions'].items()
                   if item['action'] in ('add', 'update', 'remove')]
        manifest = _manifest(payload)
        plan['changed'] = bool(changes or baseline != manifest)
        if not plan['changed']:
            return plan
        backup_root = _target(repo, '.agents/workflow-kit-backups')
        backup_root.mkdir(parents=True, exist_ok=True)
        backup = Path(tempfile.mkdtemp(prefix='upgrade-', dir=backup_root))
        plan['backup'] = str(backup)
        for name in changes + [MANIFEST]:
            data = originals.get(name) if name != MANIFEST else manifest_before
            if data is not None:
                destination = backup / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                shutil.copymode(_target(repo, name), destination)
        # Recheck after backup so an intervening edit cannot be silently overwritten.
        for name, data in originals.items():
            if _contents(_target(repo, name)) != data:
                raise ValueError(f'File changed during upgrade; inspect backup {backup}: {name}')
        applied = []
        try:
            for name in changes:
                path = _target(repo, name)
                data = payload.get(name)
                if _contents(path) != originals[name]:
                    raise ValueError(f'File changed during upgrade: {name}')
                if data is None:
                    path.unlink()
                else:
                    _atomic(path, data)
                applied.append(name)
            manifest_path = _target(repo, MANIFEST)
            if _contents(manifest_path) != manifest_before:
                raise ValueError('Installation manifest changed during upgrade')
            _atomic(manifest_path, _json_bytes(manifest))
        except Exception as error:
            for name in reversed(applied):
                path = _target(repo, name)
                if _contents(path) != payload.get(name):
                    raise RuntimeError(f'Concurrent edit prevents rollback; inspect {backup}: {name}')
                if originals[name] is None:
                    path.unlink()
                else:
                    _atomic(path, originals[name])
                    shutil.copymode(backup / name, path)
            if hasattr(error, 'add_note'):
                error.add_note(f'Applied files rolled back; recovery backup: {backup}')
            raise
        return plan


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo')
    parser.add_argument('--upgrade', action='store_true')
    parser.add_argument('--dry-run', action='store_true', help='Read-only upgrade preview')
    parser.add_argument('--keep-local', action='append', default=[], metavar='PATH')
    parser.add_argument('--replace', action='append', default=[], metavar='PATH',
                        help='Replace only this reviewed local/unknown file; explicit consent required')
    args = parser.parse_args()
    if (args.dry_run or args.keep_local or args.replace) and not args.upgrade:
        parser.error('Upgrade options require --upgrade')
    try:
        if args.upgrade:
            print(json.dumps(upgrade(args.repo, dry_run=args.dry_run,
                                     keep_local=args.keep_local, replace=args.replace),
                             ensure_ascii=False, indent=2))
        else:
            print(f'Installed {install(args.repo)} skills; no existing skills replaced.')
    except (ValueError, OSError) as exc:
        sys.exit('\n'.join([str(exc)] + getattr(exc, '__notes__', [])))

#!/usr/bin/env python3
"""Sync this repository to a GitHub repo through the GitHub Contents API.

Useful when normal `git push` is blocked by local network TLS issues but `gh api`
still works.

Usage:
  tools/sync_github_contents.py wangliguo123321/personal-book-skills --branch main
"""
from __future__ import annotations
import argparse, base64, json, mimetypes, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXCLUDES = {'.git', '.DS_Store', '__pycache__'}

def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & DEFAULT_EXCLUDES:
        return True
    if path.suffix in {'.pyc', '.pyo'}:
        return True
    return False

def gh_json(args: list[str], input_obj: dict | None = None, check: bool = True):
    cmd = ['gh', 'api', *args]
    data = None
    if input_obj is not None:
        data = json.dumps(input_obj).encode()
    p = subprocess.run(cmd, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise RuntimeError(f"gh api failed: {' '.join(cmd)}\n{p.stderr.decode(errors='ignore')}")
    if p.returncode != 0:
        return None
    if not p.stdout.strip():
        return None
    return json.loads(p.stdout)

def existing_sha(repo: str, rel: str, branch: str) -> str | None:
    res = gh_json([f'repos/{repo}/contents/{rel}?ref={branch}'], check=False)
    return res.get('sha') if isinstance(res, dict) else None

def sync_file(repo: str, path: Path, branch: str, message_prefix: str) -> None:
    rel = path.relative_to(ROOT).as_posix()
    content = base64.b64encode(path.read_bytes()).decode()
    body = {
        'message': f'{message_prefix}: {rel}',
        'content': content,
        'branch': branch,
    }
    sha = existing_sha(repo, rel, branch)
    if sha:
        body['sha'] = sha
    gh_json(['-X', 'PUT', f'repos/{repo}/contents/{rel}', '--input', '-'], body)
    kind = mimetypes.guess_type(path.name)[0] or 'file'
    print(f'synced {rel} ({kind})')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', help='owner/repo')
    ap.add_argument('--branch', default='main')
    ap.add_argument('--message-prefix', default='Sync book skills')
    args = ap.parse_args()
    files = [p for p in ROOT.rglob('*') if p.is_file() and not should_skip(p.relative_to(ROOT))]
    for p in sorted(files):
        sync_file(args.repo, p, args.branch, args.message_prefix)
    print(f'OK synced {len(files)} files to {args.repo}@{args.branch}')

if __name__ == '__main__':
    main()

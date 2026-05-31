#!/usr/bin/env python3
"""Ingest a new book version into libraries/<book>/sources/<version>/.

Usage:
  tools/ingest_book.py tire-buying-guide v3 /path/to/book.pdf --title '轮胎选购指南-V3'

Requires pdftotext for PDF text extraction.
"""
from __future__ import annotations
import argparse, hashlib, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('book')
    ap.add_argument('version')
    ap.add_argument('source')
    ap.add_argument('--title', default=None)
    args = ap.parse_args()
    src = Path(args.source).expanduser().resolve()
    dest = ROOT / 'libraries' / args.book / 'sources' / args.version
    dest.mkdir(parents=True, exist_ok=True)
    out_pdf = dest / ('source' + src.suffix.lower())
    shutil.copy2(src, out_pdf)
    if src.suffix.lower() == '.pdf':
        txt = dest / 'source.txt'
        subprocess.run(['pdftotext', '-layout', str(out_pdf), str(txt)], check=True)
    print({'book': args.book, 'version': args.version, 'source': str(out_pdf), 'sha256': sha256(out_pdf), 'next': 'extract claims, diff versions, update manifest'})
if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Lightweight regression checks for skill packaging.

This is intentionally deterministic: it validates that eval prompts reference
existing files and that critical safety phrases appear in the generated refs.
It does not call an LLM; use it as a guardrail before publishing.
"""
from __future__ import annotations
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / 'evals' / 'tire-buying-guide.yaml'
SKILL = ROOT / 'skills' / 'tire-buying-guide'


def parse_eval_file(path: Path):
    items=[]; cur=None
    for raw in path.read_text(encoding='utf-8').splitlines():
        if not raw.strip() or raw.lstrip().startswith('#') or raw.strip() == 'evals:':
            continue
        line=raw.rstrip()
        if line.startswith('  - '):
            if cur: items.append(cur)
            cur={}
            rest=line[4:]
            if rest and ':' in rest:
                k,v=rest.split(':',1); cur[k.strip()]=parse_value(v)
        elif cur is not None and line.startswith('    ') and ':' in line:
            k,v=line.strip().split(':',1); cur[k.strip()]=parse_value(v)
    if cur: items.append(cur)
    return items


def parse_value(v: str):
    v=v.strip()
    if v.startswith('[') and v.endswith(']'):
        inside=v[1:-1].strip()
        return [] if not inside else [x.strip().strip('"\'') for x in inside.split(',')]
    return v.strip('"\'')


def main():
    errors=[]
    refs_text='\n'.join(p.read_text(encoding='utf-8') for p in (SKILL/'references').glob('*.md'))
    for item in parse_eval_file(EVAL):
        eid=item.get('id','<missing id>')
        for ref in item.get('references',[]):
            ref_path = SKILL / ref
            if not ref_path.exists():
                errors.append(f'{eid}: missing reference {ref}')
        for phrase in item.get('must_include',[]):
            # Normalize very lightly: exact phrase or phrase without spaces.
            if phrase not in refs_text and phrase.replace(' ', '') not in refs_text.replace(' ', ''):
                errors.append(f'{eid}: must_include phrase not found in refs: {phrase}')
    if errors:
        print('\n'.join(errors)); sys.exit(1)
    print(f'OK {len(parse_eval_file(EVAL))} eval specs')

if __name__ == '__main__':
    main()

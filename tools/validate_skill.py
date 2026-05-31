#!/usr/bin/env python3
from pathlib import Path
import sys, re
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for skill in (ROOT/'skills').glob('*/SKILL.md'):
    text=skill.read_text()
    if not text.startswith('---'):
        errors.append(f'{skill}: missing frontmatter')
    if not re.search(r'^name:\s*\S+', text, re.M):
        errors.append(f'{skill}: missing name')
    if not re.search(r'^description:\s*.+', text, re.M):
        errors.append(f'{skill}: missing description')
for manifest in (ROOT/'libraries').glob('*/manifest.yaml'):
    if 'current_version:' not in manifest.read_text():
        errors.append(f'{manifest}: missing current_version')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('OK')

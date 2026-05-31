#!/usr/bin/env python3
"""Simple text diff helper for two imported source.txt files.

This is a baseline. For production updates, combine this with structured YAML
entity diffs and human review.
"""
from __future__ import annotations
import argparse, difflib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('book'); ap.add_argument('old'); ap.add_argument('new')
    args=ap.parse_args()
    a=(ROOT/'libraries'/args.book/'sources'/args.old/'source.txt').read_text(errors='ignore').splitlines()
    b=(ROOT/'libraries'/args.book/'sources'/args.new/'source.txt').read_text(errors='ignore').splitlines()
    for line in difflib.unified_diff(a,b,fromfile=args.old,tofile=args.new,n=3):
        print(line)
if __name__=='__main__': main()

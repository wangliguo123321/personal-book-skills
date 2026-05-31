#!/usr/bin/env python3
"""Build skill reference markdown files from canonical YAML.

Uses a tiny parser for this repository's simple YAML subset, so no third-party
Python dependency is required.
"""
from __future__ import annotations
from pathlib import Path
import ast, re

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "libraries" / "tire-buying-guide" / "canonical"
REF = ROOT / "skills" / "tire-buying-guide" / "references"

def split_top_level_commas(s: str):
    parts=[]; cur=[]; depth=0
    for ch in s:
        if ch in '[{(':
            depth += 1
        elif ch in ']})' and depth:
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(''.join(cur).strip()); cur=[]
        else:
            cur.append(ch)
    if cur or s.endswith(','):
        parts.append(''.join(cur).strip())
    return [p for p in parts if p]

def parse_inline_value(v: str):
    v = v.strip()
    if not v:
        return ""
    if v.startswith('[') and v.endswith(']'):
        inside = v[1:-1].strip()
        return [] if not inside else [x.strip().strip('"\'') for x in split_top_level_commas(inside)]
    if v.startswith('{') and v.endswith('}'):
        inside = v[1:-1].strip()
        d = {}
        if inside:
            for part in split_top_level_commas(inside):
                if ':' not in part:
                    continue
                k, val = part.split(':', 1)
                d[k.strip()] = val.strip().strip('"\'')
        return d
    if v.isdigit():
        return int(v)
    return v.strip('"\'')

def parse_list_file(path: Path, root_key: str):
    items=[]; cur=None
    for raw in path.read_text().splitlines():
        if not raw.strip() or raw.lstrip().startswith('#') or raw.strip()==f'{root_key}:':
            continue
        line=raw.rstrip()
        if line.startswith('  - '):
            if cur: items.append(cur)
            cur={}
            rest=line[4:]
            if rest:
                k,v=rest.split(':',1); cur[k.strip()]=parse_inline_value(v)
        elif cur is not None and line.startswith('    '):
            k,v=line.strip().split(':',1); cur[k.strip()]=parse_inline_value(v)
    if cur: items.append(cur)
    return items

def parse_map_file(path: Path, root_key: str):
    result={}; cur_key=None
    for raw in path.read_text().splitlines():
        if not raw.strip() or raw.lstrip().startswith('#') or raw.strip()==f'{root_key}:':
            continue
        line=raw.rstrip()
        m=re.match(r'^  ([A-Za-z0-9_]+):\s*$', line)
        if m:
            cur_key=m.group(1); result[cur_key]={}; continue
        if cur_key and line.startswith('    '):
            k,v=line.strip().split(':',1); result[cur_key][k.strip()]=parse_inline_value(v)
    return result

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n")

def fmt_source(src) -> str:
    src = src if isinstance(src, dict) else {}
    return f"来源：{src.get('version','?')}，{src.get('chapter','?')}，页码 {src.get('page_range','?')}"

def join(v):
    return ', '.join(v) if isinstance(v, list) else str(v)

def build_safety():
    rules = parse_list_file(LIB / "safety-rules.yaml", "rules")
    lines = ["# 安全规则", "", "遇到安全问题先按本文件处理；安全结论优先于省钱和舒适性。", ""]
    for r in rules:
        lines += [f"## {r['trigger']}", "", f"- 严重级别：`{r['severity']}`", f"- 建议：{r['recommendation']}", f"- 原因：{r['rationale']}", f"- {fmt_source(r.get('source'))}", ""]
    write(REF / "safety-rules.md", "\n".join(lines))

def build_decision():
    scenarios = parse_map_file(LIB / "decision-tree.yaml", "scenarios")
    lines = ["# 快速决策树", "", "先匹配用户场景，再给 2-4 个候选方向并说明代价。", ""]
    for key, s in scenarios.items():
        lines += [f"## {key}", "", f"- 用户信号：{join(s['user_signals'])}", f"- 推荐方向：{s['recommend']}", f"- 候选：{join(s['candidates'])}", f"- 取舍：{s['tradeoff']}", f"- {fmt_source(s.get('source'))}", ""]
    write(REF / "quick-decision.md", "\n".join(lines))

def build_brands():
    brands = parse_map_file(LIB / "brand-profiles.yaml", "brands")
    lines = ["# 品牌速查", "", "用于品牌选择、品牌对比、按场景推荐时。", ""]
    for bid, b in brands.items():
        lines += [f"## {b['zh_name']} `{bid}`", "", f"- 梯队：{b['tier']}", f"- 强项：{join(b['strengths'])}", f"- 弱项：{join(b['weaknesses'])}", f"- 适合：{join(b['suitable_for'])}", f"- 避免：{join(b['avoid_if'])}", f"- {fmt_source(b.get('source'))}", ""]
    write(REF / "brand-cheatsheet.md", "\n".join(lines))

def build_traps():
    traps = parse_list_file(LIB / "consumer-traps.yaml", "traps")
    lines = ["# 消费避坑", "", "用于识别营销溢价、错误认知和隐藏成本。", ""]
    for t in traps:
        lines += [f"## {t['name']}", "", f"- 可能收益：{t['benefit']}", f"- 风险/代价：{t['risk']}", f"- {fmt_source(t.get('source'))}", ""]
    write(REF / "consumer-traps.md", "\n".join(lines))

def build_concepts():
    concepts = parse_map_file(LIB / "concept-map.yaml", "concepts")
    lines = ["# 概念地图", "", "用于回答跨章节问题，先调用可复用模型，再按需回查证据。", ""]
    for cid, c in concepts.items():
        lines += [
            f"## {c['title']} `{cid}`",
            "",
            f"- 核心判断：{c['thesis']}",
            f"- 支撑点：{join(c['load_bearing_points'])}",
            f"- 触发场景：{join(c['use_when'])}",
            f"- {fmt_source(c.get('source'))}",
            "",
        ]
    write(REF / "concept-map.md", "\n".join(lines))

def build_evidence():
    evidence = parse_list_file(LIB / "evidence-index.yaml", "evidence")
    lines = ["# 证据索引", "", "用于需要溯源、核对结论或更新版本时。quote 只作为定位线索，不要大段复制原文。", ""]
    for ev in evidence:
        lines += [
            f"## {ev['id']}",
            "",
            f"- 主题：{ev['topic']}",
            f"- 结论：{ev['claim']}",
            f"- 支持对象：{join(ev['supports'])}",
            f"- 置信度：{ev['confidence']}",
            f"- {fmt_source(ev.get('source'))}",
            "",
        ]
    write(REF / "evidence-index.md", "\n".join(lines))

def main():
    build_safety(); build_decision(); build_brands(); build_traps(); build_concepts(); build_evidence()
    print(f"Built references in {REF}")
if __name__ == "__main__": main()

#!/usr/bin/env python3
"""Descriptive prose diagnostics for approved TLD archive or candidate Markdown.
Counts are editorial signals, never an AI detector or an authorship judgment.
"""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

WORD = re.compile(r"\b[\w]+(?:[’'-][\w]+)*\b")
PATTERNS = {
    'directional_look': r'\b(?:looked|glanced|stared) (?:at|toward|over|down|up)\b',
    'phone': r'\bphone\b',
    'recognition': r'\b(?:realized|understood|noticed|recognized)\b',
    'clock': r'\b\d{1,2}:\d{2}\b',
    'then': r'\bthen\b',
    'still': r'\bstill\b',
    'knew': r'\bknew\b',
}


def measure(text):
    body = '\n'.join(line for line in text.splitlines() if not line.startswith('#'))
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', body)
                  if p.strip() and p.strip() not in ('---', '***', '* * *')]
    return {'words': len(WORD.findall(body)), 'paragraphs': len(paragraphs),
            'short_paragraphs': sum(len(p.split()) <= 5 for p in paragraphs),
            **{key: len(re.findall(pattern, body, re.I)) for key, pattern in PATTERNS.items()}}


def aggregate(rows):
    counts = {key: sum(row[key] for row in rows) for key in measure('')}
    counts['units'] = len(rows)
    counts['words_per_paragraph'] = round(counts['words'] / max(1, counts['paragraphs']), 2)
    counts['short_paragraph_share'] = round(counts['short_paragraphs'] / max(1, counts['paragraphs']), 4)
    return counts


def audit(path):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if path.suffix.lower() == '.zip':
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise ValueError('ZIP CRC failure')
            names = sorted(n for n in archive.namelist() if re.fullmatch(r'approved/CH\d+(?:\.\d+)?/chapter_final\.md', n))
            if not names:
                raise ValueError('No approved chapter_final.md entries')
            units = {n.split('/')[1]: measure(archive.read(n).decode('utf-8')) for n in names}
    else:
        units = {'candidate': measure(path.read_text(encoding='utf-8'))}
    report = {'sha256': digest, 'units': units, 'aggregate': aggregate(list(units.values()))}
    for label, low, high in [('main_1_6', 1, 6), ('main_7_13', 7, 13)]:
        selected = [v for k, v in units.items() if re.fullmatch(r'CH\d+', k) and low <= int(k[2:]) <= high]
        if selected:
            report[label] = aggregate(selected)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.path), indent=2))

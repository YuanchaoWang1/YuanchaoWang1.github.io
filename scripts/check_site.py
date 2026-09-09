#!/usr/bin/env python3
"""Check local destinations, fragment targets, SVG structure, and publication coverage."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.refs, self.ids, self.errors = [], set(), []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                self.errors.append('Duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        for attr in ('href', 'src'):
            if a.get(attr):
                self.refs.append(a[attr])
        if a.get('srcset'):
            self.refs.extend(x.strip().split()[0] for x in a['srcset'].split(','))
        if tag == 'img' and not a.get('alt'):
            self.errors.append('Image is missing alternative text')


def main():
    docs = {p.resolve(): Document(p.read_text(encoding='utf-8')) for p in DIST.rglob('*.html')}
    errors = []
    for path, doc in docs.items():
        errors.extend(str(path.relative_to(DIST)) + ': ' + e for e in doc.errors)
        for ref in doc.refs:
            u = urlsplit(ref)
            if u.scheme or u.netloc:
                continue
            target = (path.parent / unquote(u.path)).resolve() if u.path else path
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                errors.append(f'{path.relative_to(DIST)}: missing {ref}')
            elif u.fragment and target in docs and unquote(u.fragment) not in docs[target].ids:
                errors.append(f'{path.relative_to(DIST)}: missing fragment {ref}')
    for p in DIST.rglob('*.svg'):
        ET.parse(p)
    papers = json.loads((ROOT/'content/papers.json').read_text(encoding='utf-8'))
    if len({p['id'] for p in papers}) != len(papers):
        errors.append('Duplicate paper IDs')
    for paper in papers:
        if not paper.get('has_diagram', True):
            continue
        for suffix in ('', '-mobile'):
            if not (DIST/'assets/diagrams'/f'{paper["id"]}{suffix}.svg').is_file():
                errors.append('Missing diagram: ' + paper['id'] + suffix)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'OK: {len(docs)} HTML routes, {len(papers)} papers, {len(list(DIST.rglob("*.svg")))} SVG assets; all local links and fragments resolve.')


if __name__ == '__main__':
    main()

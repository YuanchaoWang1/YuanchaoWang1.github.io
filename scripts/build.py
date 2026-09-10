#!/usr/bin/env python3
"""Generate the static site using Python 3.10+ and the standard library only."""
from pathlib import Path
from html import escape
import json
import os

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
SITE = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
PAPERS = json.loads((ROOT / 'content/papers.json').read_text(encoding='utf-8'))
E = escape


def link(url, label):
    return f'<a href="{E(url, quote=True)}">{E(label)}</a>'


def page(title, body, route=''):
    prefix = '../' if route else ''
    page_class = 'page-' + (route or 'home')
    nav = []
    for name, target in [('Home', ''), ('Publications', 'publications'), ('Projects', 'projects')]:
        href = prefix + (target + '/' if target else '') + 'index.html'
        active = ' aria-current="page"' if target == route else ''
        nav.append(f'<a href="{href}"{active}>{name}</a>')
    socials = link('mailto:' + SITE['email'], 'Email') + ''.join(link(x['url'], x['label']) for x in SITE['links'])
    canonical_base = os.environ.get('SITE_URL', SITE['site_url']).rstrip('/')
    canonical = canonical_base + '/' + (route + '/' if route else '')
    meta = f'<link rel="canonical" href="{E(canonical)}"><meta property="og:url" content="{E(canonical)}">' if canonical_base else ''
    full_title = SITE['name'] if not route else f'{title} | {SITE["name"]}'
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full_title)}</title>
<meta name="description" content="{E(SITE['description'])}">
<meta name="author" content="{E(SITE['name'])}">
<meta property="og:title" content="{E(full_title)}"><meta property="og:description" content="{E(SITE['description'])}">
<meta property="og:type" content="website">{meta}
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body class="{page_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead"><div class="masthead-inner">
<a class="wordmark" href="{prefix}index.html">{E(SITE['name'])}</a>
<nav aria-label="Main navigation">{''.join(nav)}</nav>
</div></header>
<div class="layout">
<aside class="profile" aria-label="Profile">
<img class="portrait" src="{prefix}assets/portrait.png" alt="{E(SITE['name'])}" width="180" height="220">
<h2>{E(SITE['name'])}</h2><p>{E(SITE['role'])}<br>{E(SITE['institution'])}</p>
<hr class="profile-rule"><div class="profile-links">{socials}</div>
</aside>
<main id="main">{body}</main>
</div>
<footer class="footer"><span>© 2026 {E(SITE['name'])}</span><span>Updated {E(SITE['updated'])}</span></footer>
</body></html>
'''
    target = DIST / route / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding='utf-8')


def records(items):
    return ''.join(f'<div class="record"><div><strong>{E(x["organization"])}</strong><p>{E(x["detail"])}</p></div><span class="date">{E(x["date"])}</span></div>' for x in items)


def home():
    body = '<p class="eyebrow">About</p><h1>' + E(SITE['name']) + '</h1>'
    for i, paragraph in enumerate(SITE['bio']):
        body += f'<p class="{"intro" if i == 0 else "bio"}">{E(paragraph)}</p>'
    body += f'<p class="research-question">{E(SITE["research_question"])}</p><p>{E(SITE["research_text"])}</p>'
    if SITE.get('trajectory'):
        body += '<h2>Research trajectory</h2><ul class="trajectory">'
        for item in SITE['trajectory']:
            body += '<li><strong>' + link('projects/index.html#'+item['id'],item['label']) + '.</strong> ' + E(item['text']) + '</li>'
        body += '</ul>'
    body += '<p>Read my <a href="publications/index.html">publications</a> or explore the ideas behind my <a href="projects/index.html">projects</a>.</p>'
    body += '<h2>Education</h2>' + records(SITE['education'])
    body += '<h2>Experience</h2>' + records(SITE['experience'])
    body += '<h2>Recognition</h2><ul class="compact-list">'
    body += ''.join(f'<li>{link(x["url"], x["title"])}<br><span class="muted">{E(x["detail"])}</span></li>' for x in SITE['recognition'])
    body += '</ul><h2>Professional service</h2><p>' + E(SITE['service']) + '</p>'
    page('Home', body)


def paper_links(p, project_link=True):
    links = ''.join(link(x['url'], x['label']) for x in p['links'])
    if project_link:
        links += link('../projects/index.html#' + p['id'], 'Project overview')
    return '<div class="paper-links">' + links + '</div>' if links else ''


def publications():
    body = '<h1>Publications</h1><p class="publication-intro">Conference papers, manuscripts, and preprints.</p><section class="publication-list" aria-label="Publication list">'
    for p in sorted(PAPERS, key=lambda paper: paper['year'], reverse=True):
        authors = ', '.join(f'<strong>{E(a)}</strong>' if a == SITE['name'] else E(a) for a in p['authors'])
        # Link updated project names to their matching overview, not to an older differently titled PDF.
        title_url = '../projects/index.html#' + p['id'] if p['id'] == 'shellood' or not p['links'] else p['links'][0]['url']
        body += f'<article class="publication" id="{E(p["id"])}"><h2>{link(title_url,p["title"])}</h2>'
        if authors:
            body += f'<p class="authors">{authors}</p>'
        body += f'<p class="venue">{E(p["venue"])}</p>'
        if p['venue_detail']:
            body += '<p class="venue-detail">' + E(p['venue_detail']) + '</p>'
        body += paper_links(p)
        if p['note']:
            body += '<p class="paper-note">' + E(p['note']) + '</p>'
        body += '</article>'
    body += '</section>'
    page('Publications', body, 'publications')


def projects():
    body = '<h1>Projects</h1><p>' + E(SITE['research_question']) + '</p>'
    order = ['ood-tv-irm', 'ectr', 'shellood', 'cross', 'attention-trees']
    papers = {p['id']: p for p in PAPERS}
    body += '<nav class="project-index" aria-label="Project index">' + ''.join(link('#' + key, papers[key]['short_title']) for key in order) + '</nav>'
    for key in order:
        p = papers[key]
        body += f'<article class="project" id="{key}"><p class="project-topic">{E(p["topic"])}</p><h2>{E(p["project_title"])}</h2>'
        body += f'<p class="venue">{E(p["venue"])}</p>'
        body += paper_links(p, False)
        body += f'<p class="project-description">{E(p["summary"])}</p>'
        if p.get('has_diagram', True):
            diagram = p.get('diagram', f'{key}.svg')
            mobile_diagram = p.get('diagram_mobile')
            if mobile_diagram is None and 'diagram' not in p:
                mobile_diagram = f'{key}-mobile.svg'
            source = f'<source media="(max-width: 960px)" srcset="../assets/diagrams/{E(mobile_diagram, quote=True)}">' if mobile_diagram else ''
            width = p.get('diagram_width', 800)
            height = p.get('diagram_height', 480)
            body += f'<figure><picture>{source}<img class="diagram" src="../assets/diagrams/{E(diagram, quote=True)}" alt="{E(p["diagram_alt"])}" loading="lazy" width="{width}" height="{height}"></picture><figcaption>{E(p["caption"])}</figcaption></figure>'
        body += f'<p class="takeaway"><strong>Core idea.</strong> {E(p["takeaway"])}</p>'
        if p.get('has_diagram', True):
            diagram = p.get('diagram', f'{key}.svg')
            body += f'<a class="diagram-link" href="../assets/diagrams/{E(diagram, quote=True)}">Open full-size diagram</a>'
        elif p.get('availability'):
            body += f'<p class="paper-note">{E(p["availability"])}</p>'
        body += '</article>'
    page('Projects', body, 'projects')


def redirects():
    # Preserve the old research route as a compatibility alias.
    (DIST / 'research').mkdir(exist_ok=True)
    (DIST / 'research/index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0;url=../publications/index.html"><title>Publications | Yuanchao Wang</title></head><body><p><a href="../publications/index.html">Continue to Publications</a></p></body></html>\n', encoding='utf-8')
    (DIST / '.nojekyll').touch()


if __name__ == '__main__':
    home()
    publications()
    projects()
    redirects()
    print('Generated Home, Publications, Projects, and the /research/ redirect.')

#!/usr/bin/env python3
"""Editable, schematic algorithm figures. No external Python dependencies.

Run: python scripts/draw_diagrams.py
All figures have desktop and mobile compositions. They contain no measured data.
"""
from pathlib import Path
from html import escape
from math import cos, sin, pi

OUT = Path(__file__).resolve().parents[1] / 'dist/assets/diagrams'
INK, MUTED, BLUE, ORANGE = '#202831', '#596674', '#245895', '#a85b14'
PALE_BLUE, PALE_ORANGE, LINE = '#eaf1fa', '#fff2e3', '#b8c5d4'


class SVG:
    def __init__(self, title, desc, mobile=False):
        self.w, self.h = (420, 700) if mobile else (800, 480)
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
                      '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#728497"/></marker></defs>',
                      f'<rect width="{self.w}" height="{self.h}" fill="#f7f9fc"/>',
                      '<g font-family="Arial, Helvetica, sans-serif">']

    def text(self, x, y, lines, size=19, color=INK, anchor='middle', weight=400):
        if isinstance(lines, str):
            lines = [lines]
        for i, line in enumerate(lines):
            self.parts.append(f'<text x="{x}" y="{y+i*(size+8)}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(line)}</text>')

    def rect(self, x, y, w, h, fill='#fff', stroke=LINE, radius=8):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

    def box(self, x, y, w, h, lines, fill='#fff', color=INK, size=19):
        self.rect(x, y, w, h, fill)
        lines = [lines] if isinstance(lines, str) else lines
        self.text(x+w/2, y+h/2-(len(lines)-1)*(size+8)/2+size*.35, lines, size, color)

    def path(self, d, arrow=True, dashed=False):
        self.parts.append(f'<path d="{d}" fill="none" stroke="#728497" stroke-width="2"'+ (' stroke-dasharray="5 5"' if dashed else '') + (' marker-end="url(#arrow)"' if arrow else '') + '/>')

    def line(self, x1, y1, x2, y2, arrow=True, dashed=False):
        self.path(f'M{x1},{y1} L{x2},{y2}', arrow, dashed)

    def dot(self, x, y, r=6, fill=BLUE, stroke='none'):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')

    def header(self, title, subtitle=None):
        self.text(25, 33, title, 20, BLUE, 'start', 600)
        if subtitle:
            self.text(25, 59, subtitle, 16, MUTED, 'start')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text('\n'.join(self.parts + ['</g></svg>'])+'\n', encoding='utf-8')


def environment(s, x, y, w, label, weighted=False):
    s.rect(x, y, w, 95)
    s.text(x+15, y+28, label, 18, INK, 'start', 600)
    for i in range(5):
        s.dot(x+25+i*(w-50)/4, y+64, [4, 5, 6, 9, 13][i] if weighted else 6, ORANGE if i == 4 else BLUE)


def ood_tv(mobile=False):
    s = SVG('OOD-TV-IRM: primal-dual invariant learning', 'Training environments feed a shared model. Primal descent updates features; dual ascent updates the learned TV multiplier.', mobile)
    s.header('OOD-TV-IRM', 'Learn the invariance penalty together with the model.') if not mobile else s.header('OOD-TV-IRM')
    if mobile:
        s.box(35, 65, 350, 65, 'Multiple training environments')
        s.line(210,130,210,160)
        s.box(65,160,290,70,['Shared feature extractor', 'and prediction risks'], PALE_BLUE)
        s.line(210,230,210,270)
        s.box(35,270,350,90,['Prediction risk', '+ learned weight × TV penalty'], size=19)
        s.path('M210,360 L210,400 L110,400 L110,430')
        s.path('M210,400 L310,400 L310,430')
        s.box(25,430,175,100,['Primal descent','Update features'], PALE_BLUE, BLUE, 18)
        s.box(220,430,175,100,['Dual ascent','Update penalty'], PALE_ORANGE, ORANGE, 18)
        s.path('M110,530 L110,565 L310,565 L310,530', False)
        s.text(210,605,['Alternate the two updates', 'to couple prediction and invariance.'],18,MUTED)
        s.text(210,668,'Known-environment form · Schematic',15,MUTED)
    else:
        for x,lab in [(25,'Environment 1'),(285,'Environment 2'),(545,'Environment 3')]:
            s.box(x,82,230,55,lab)
        s.path('M140,137 L140,159 L400,159 L400,180')
        s.line(400,137,400,180)
        s.path('M660,137 L660,159 L400,159',False)
        s.box(245,180,310,62,'Shared feature extractor',PALE_BLUE,BLUE)
        s.line(400,242,400,275)
        s.box(170,275,460,72,['Prediction risk + learned weight × TV penalty'],size=18)
        s.path('M300,347 L300,373 L225,373 L225,395')
        s.path('M500,347 L500,373 L575,373 L575,395')
        s.box(65,395,320,60,['Primal descent: update features'],PALE_BLUE,BLUE,18)
        s.box(415,395,320,60,['Dual ascent: update penalty'],PALE_ORANGE,ORANGE,18)
        s.path('M65,425 L40,425 L40,211 L245,211',dashed=True)
        s.path('M735,425 L765,425 L765,311 L630,311',dashed=True)
    s.save('ood-tv-irm'+('-mobile' if mobile else '')+'.svg')


def ectr(mobile=False):
    s = SVG('ECTR: shared environment-conditioned tail risks', 'An adversary weights hard samples within each environment. Both supervised risk and TV stationarity use the resulting tail risks, with environment-wise KL regularization.', mobile)
    s.header('ECTR', 'Expose hard samples before testing invariance.') if not mobile else s.header('ECTR')
    if mobile:
        environment(s,25,68,175,'Environment 1')
        environment(s,220,68,175,'Environment 2')
        s.path('M112,163 L112,185 L210,185 L210,205')
        s.path('M308,163 L308,185 L210,185',False)
        s.box(45,205,330,95,['Tail adversary', 'Normalize within each environment'],PALE_BLUE,BLUE,18)
        s.path('M210,300 L210,317 L112,317 L112,335')
        s.path('M210,317 L308,317 L308,335')
        environment(s,25,335,175,'Tail risk 1',True)
        environment(s,220,335,175,'Tail risk 2',True)
        s.path('M112,430 L112,452 L210,452 L210,477')
        s.path('M308,430 L308,452 L210,452',False)
        s.box(30,477,360,95,['The same reweighted risks', 'Prediction loss + TV penalty'],PALE_BLUE,BLUE,19)
        s.box(30,600,360,60,'KL controls weight concentration',PALE_ORANGE,ORANGE,18)
        s.text(210,685,'Dot size = sample weight',15,MUTED)
    else:
        environment(s,25,98,190,'Environment 1')
        environment(s,25,238,190,'Environment 2')
        s.path('M215,145 L238,145 L238,215 L265,215')
        s.path('M215,285 L238,285 L238,215',False)
        s.box(265,151,240,130,['Tail adversary', 'Normalize weights', 'within each environment'],PALE_BLUE,BLUE,18)
        s.path('M505,216 L535,216 L535,145 L565,145')
        s.path('M535,216 L535,285 L565,285')
        environment(s,565,98,210,'Tail risk 1',True)
        environment(s,565,238,210,'Tail risk 2',True)
        s.path('M775,145 L788,145 L788,355 L670,355',False)
        s.path('M670,333 L670,355 L400,355 L400,380')
        s.text(25,81,'Dot size = sample weight',15,MUTED,'start')
        s.box(215,380,560,70,['The same tail risks feed prediction loss + TV penalty'],PALE_BLUE,BLUE,18)
        s.box(25,375,165,80,['KL regularizer', 'controls weights'],PALE_ORANGE,ORANGE,17)
        s.path('M105,375 L105,352 L385,352 L385,281',dashed=True)
    s.save('ectr'+('-mobile' if mobile else '')+'.svg')


def shell_geometry(s, cx, cy, r):
    for radius, color in [(r,BLUE),(r*.68,LINE),(r*.43,LINE)]:
        s.dot(cx,cy,radius,'none',color)
    s.dot(cx,cy,3,MUTED)
    for a,color in [(-pi/2,BLUE),(pi/6,'#387d7a'),(5*pi/6,'#605492')]:
        x,y=cx+cos(a)*r,cy+sin(a)*r
        for dx,dy in [(0,0),(-7,4),(6,6)]:
            s.dot(x+dx,y+dy,5,color)
    for a,scale in [(0.3,.63),(1.9,.4),(3.8,.65),(5.2,.38)]:
        s.dot(cx+cos(a)*r*scale,cy+sin(a)*r*scale,6,ORANGE)


def shellood(mobile=False):
    s = SVG('ShellOOD: radius-shell self-supervision', 'ID-only warm-up establishes a reference radius. Cross-class feature mixup and an auxiliary shell head train synthetic features toward inner shells. Only the classifier and backbone are used at inference.', mobile)
    s.header('ShellOOD', 'Use ID feature geometry to teach OOD awareness.') if not mobile else s.header('ShellOOD')
    if mobile:
        shell_geometry(s,210,170,90)
        s.text(210,57,'Warm up on ID data',18,BLUE)
        s.text(210,295,'Outer radius: typical ID features',17,BLUE)
        s.text(210,322,'Inner shells: synthetic features',17,ORANGE)
        s.box(45,350,330,60,'Cross-class feature mixup',PALE_ORANGE,ORANGE)
        s.line(210,410,210,438)
        s.box(45,438,330,73,['Auxiliary shell supervision', 'Joint training with ID classification'],PALE_BLUE,BLUE,18)
        s.line(210,511,210,541)
        s.box(45,541,330,95,['Inference: backbone + classifier', 'Standard post-hoc OOD score', 'Discard the auxiliary shell head'],size=17)
        s.text(210,674,'ID data only · Geometry is schematic',16,MUTED)
    else:
        s.rect(25,89,280,353)
        shell_geometry(s,165,230,98)
        s.text(165,116,'Centered feature space',18,INK,weight=600)
        s.text(165,360,'Typical ID radius',18,BLUE)
        s.text(165,389,'Inner pseudo-OOD shells',17,ORANGE)
        s.text(165,419,'Schematic geometry',15,MUTED)
        s.box(350,90,420,65,'Warm up on ID data',PALE_BLUE,BLUE)
        s.line(560,155,560,184)
        s.box(350,184,420,65,'Cross-class feature mixup',PALE_ORANGE,ORANGE)
        s.line(560,249,560,278)
        s.box(350,278,420,65,['ID classification + shell supervision'],PALE_BLUE,BLUE,18)
        s.line(560,343,560,372)
        s.box(350,372,420,78,['Inference: standard post-hoc OOD score', 'Backbone + classifier; discard shell head'],size=17)
    s.save('shellood'+('-mobile' if mobile else '')+'.svg')


def matrix(s,x,y,cell=12):
    # A purely illustrative alignment pattern, not experimental attention values.
    for row in range(5):
        for col in range(8):
            color = BLUE if abs(col-row-1)<1 else ('#9fb9dc' if abs(col-row-1)<2 else '#e6ecf4')
            s.rect(x+col*cell,y+row*cell,cell-2,cell-2,color,'none',1)


def tree(s,cx,y,spread=45):
    s.line(cx,y,cx-spread,y+40,False)
    s.line(cx,y,cx+spread,y+40,False)
    s.dot(cx,y,8,BLUE)
    s.dot(cx-spread,y+40,8,BLUE)
    s.dot(cx+spread,y+40,8,ORANGE)


def attention(mobile=False):
    s = SVG('Attention explained with decision trees', 'Attention matrices from a trained speech recognizer are binned into ten levels. Previous states predict high or low attention using Silas decision trees; conditions and influence scores are analyzed.', mobile)
    s.header('Attention & decision trees', 'Probe temporal structure in a speech recognizer.') if not mobile else s.header('Attention & decision trees')
    if mobile:
        s.box(40,65,340,65,'Trained TIMIT speech recognizer',PALE_BLUE,BLUE,18)
        s.line(210,130,210,157)
        s.rect(40,157,340,110)
        matrix(s,60,182)
        s.text(260,197,['Extract attention', 'Bin into 10 levels'],18)
        s.line(210,267,210,297)
        s.box(40,297,340,66,'Previous attention states as features')
        s.line(210,363,210,393)
        s.rect(40,393,340,113,PALE_BLUE)
        tree(s,105,421,28)
        s.text(263,432,['Silas decision trees', 'Predict high / low'],18,BLUE)
        s.line(210,506,210,536)
        s.box(40,536,340,72,['Inspect decision conditions', 'and temporal influence scores'])
        s.text(210,650,['Observed: nearby states', 'carry the strongest influence.'],18,MUTED)
    else:
        s.box(25,102,225,80,['Trained TIMIT', 'speech recognizer'],PALE_BLUE,BLUE)
        s.line(250,142,290,142)
        s.rect(290,89,235,147)
        s.text(407,116,'Extract attention',18,INK,weight=600)
        matrix(s,357,134)
        s.text(407,218,'Bin weights into 10 levels',16,MUTED)
        s.line(525,159,565,159)
        s.box(565,102,210,112,['History features', 'from preceding', 'attention states'],size=18)
        s.path('M670,214 L670,261 L550,261 L550,300')
        s.rect(340,300,430,122,PALE_BLUE)
        tree(s,403,329,32)
        s.text(611,337,['Silas decision trees', 'Predict high / low attention'],18,BLUE)
        s.text(556,398,'Analyze decision conditions and influence',16,MUTED)
        s.line(340,361,293,361)
        s.box(25,300,268,122,['Observed in this model:', 'Nearby states have', 'the strongest influence.'],size=18)
        s.text(25,457,'Illustrative attention pattern; no measured values shown.',15,MUTED,'start')
    s.save('attention-trees'+('-mobile' if mobile else '')+'.svg')


if __name__ == '__main__':
    for mobile in (False,True):
        for draw in (ood_tv,ectr,shellood,attention):
            draw(mobile)
    print('Generated four algorithm diagrams with desktop and mobile versions.')

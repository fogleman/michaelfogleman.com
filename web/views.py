from flask import render_template, redirect
from functools import partial
from web import app

VIEWS = [
    'projects',
    'resume',
    'craft',
    'dcpu',
    'gps',
    'hirise',
    'imeme',
    'phrases',
    'ricochet',
    'scale',
    'star_rocket',
]

for name in VIEWS:
    hyphenated = name.replace('_', '-')
    func = partial(render_template, '%s.html' % hyphenated)
    app.add_url_rule('/%s/' % hyphenated, name, func)

REDIRECTS = [
    ('wang_tiling', 'https://github.com/fogleman/WangTiling'),
    ('dr_mario', 'https://github.com/fogleman/DrMario'),
    ('pt', 'https://github.com/fogleman/pt'),
    ('sync', 'http://www.michaelfogleman.com/static/fireflies/'),
    ('feed_notifier', 'http://www.feednotifier.com/'),
    ('game_frame', 'https://github.com/fogleman/GameFrame'),
    ('quads', 'https://github.com/fogleman/Quads'),
    ('tiling', 'https://github.com/fogleman/Tiling'),
    ('field', 'https://github.com/fogleman/Field'),
    ('manhattan', 'https://github.com/fogleman/Manhattan'),
    ('mapper', 'http://www.michaelfogleman.com/mapper/'),
    ('piet', 'https://github.com/fogleman/Piet'),
    ('pirate_map', 'https://github.com/fogleman/PirateMap'),
    ('mister_queen', 'https://github.com/fogleman/MisterQueen'),
    ('wug', 'http://www.michaelfogleman.com/wug/'),
    ('nes', 'https://github.com/fogleman/nes'),
    ('wooden_map', 'https://medium.com/@fogleman/a-wooden-map-of-north-carolina-a2b21ca47ca2'),
]

for name, url in REDIRECTS:
    hyphenated = name.replace('_', '-')
    func = partial(redirect, url)
    app.add_url_rule('/%s/' % hyphenated, name, func)

@app.route('/')
def index():
    return render_template('index.html')

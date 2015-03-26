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
    ('pt', 'https://github.com/fogleman/pt'),
    ('sync', 'http://www.michaelfogleman.com/static/fireflies/'),
    ('feed_notifier', 'http://www.feednotifier.com/'),
    ('game_frame', 'https://github.com/fogleman/GameFrame'),
    ('quads', 'https://github.com/fogleman/Quads'),
    ('tiling', 'https://github.com/fogleman/Tiling'),
    ('field', 'https://github.com/fogleman/Field'),
    ('piet', 'https://github.com/fogleman/Piet'),
    ('mister_queen', 'https://github.com/fogleman/MisterQueen'),
    ('wug', 'http://www.michaelfogleman.com/wug/'),
    ('nes', 'https://github.com/fogleman/nes'),
]

for name, url in REDIRECTS:
    hyphenated = name.replace('_', '-')
    func = partial(redirect, url)
    app.add_url_rule('/%s/' % hyphenated, name, func)

@app.route('/')
def index():
    return render_template('index.html')

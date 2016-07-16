from collections import namedtuple
from flask import url_for
from functools import wraps
from operator import itemgetter
from web import app
from werkzeug.contrib.cache import SimpleCache
import os
import requests

def static(path, bust=False):
    if bust:
        file_path = os.path.join(app.root_path, app.static_folder, path)
        modified = int(os.stat(file_path).st_mtime)
        return url_for('static', filename=path, bust=modified)
    else:
        return url_for('static', filename=path)

@app.context_processor
def context_processor():
    try:
        repos = get_repos()
    except Exception:
        repos = []
    try:
        highlights = get_highlights()
    except Exception:
        highlights = []
    articles = get_articles()
    return dict(
        static=static, repos=repos, highlights=highlights, articles=articles)

class CacheDecorator(object):
    cache = SimpleCache()
    def __init__(self, timeout=300):
        self.timeout = timeout
    def __call__(self, func, timeout=None):
        timeout = timeout or self.timeout
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = '%s_%s_%s' % (func.__name__, args, kwargs)
            result = CacheDecorator.cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                CacheDecorator.cache.set(key, result, timeout)
            return result
        return wrapper

cached = CacheDecorator

@cached(3600)
def get_repos():
    url = 'https://api.github.com/users/fogleman/repos?per_page=100'
    response = requests.get(url)
    repos = response.json()
    repos.sort(key=itemgetter('watchers'), reverse=True)
    repos = [x for x in repos if not x['fork'] and not x['private']]
    return repos

@cached(60)
def get_highlights():
    exts = set(['.png', '.jpg', '.jpeg'])
    path = app.config['GALLERY_DIR']
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    names = sorted(os.listdir(path), key=mtime, reverse=True)
    names = [x for x in names if os.path.splitext(x)[1].lower() in exts]
    return names

Article = namedtuple('Article', ['date', 'url', 'template', 'endpoint'])

@cached(60)
def get_articles():
    directory = os.path.join(app.root_path, app.template_folder, 'articles')
    paths = sorted(os.listdir(directory), reverse=True)
    paths = [x for x in paths if x.endswith('.html')]
    articles = []
    for i, path in enumerate(paths):
        date = path[:10]
        name = path[11:][:-5]
        url = '/articles/%s/%s/' % (date, name)
        template = 'articles/%s' % path
        endpoint = 'article%d' % i
        articles.append(Article(date, url, template, endpoint))
    return articles

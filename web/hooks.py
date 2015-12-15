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
    return dict(static=static, repos=repos, highlights=highlights)

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

@cached(600)
def get_highlights():
    url = 'https://api.imgur.com/3/album/nutJt'
    headers = {'Authorization': 'Client-ID 0da49bd373fcbcd'}
    response = requests.get(url, headers=headers)
    images = response.json()['data']['images']
    images.sort(key=lambda x: x['datetime'], reverse=True)
    return [x['id'] for x in images]

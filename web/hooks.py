from flask import url_for
from functools import wraps
from operator import itemgetter
from web import app
from werkzeug.contrib.cache import SimpleCache
import requests
import urlparse

def static(path):
    root = app.config.get('STATIC_ROOT')
    if app.debug or root is None:
        return url_for('static', filename=path)
    else:
        return urlparse.urljoin(root, path)

@app.context_processor
def context_processor():
    repos = get_repos()
    return dict(static=static, repos=repos)

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

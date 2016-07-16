SECRET_KEY = 'CHANGE_ME'

GALLERY_DIR = 'web/static/gallery'
GALLERY_URL = '/static/gallery'

try:
    from config_local import *
except ImportError:
    pass

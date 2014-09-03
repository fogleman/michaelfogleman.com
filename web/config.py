SECRET_KEY = 'CHANGE_ME'
STATIC_ROOT = None

try:
    from config_local import *
except ImportError:
    pass

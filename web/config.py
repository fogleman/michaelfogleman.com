SECRET_KEY = 'CHANGE_ME'

try:
    from config_local import *
except ImportError:
    pass

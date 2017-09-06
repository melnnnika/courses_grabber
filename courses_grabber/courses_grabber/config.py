PORT = 7900

IS_DEBUG = False


try:
    from local_config import *
except ImportError:
    pass

__project__ = 'intercessor'
__version__ = '0.0.0'

VERSION = "{0} v{1}".format(__project__, __version__)

from pysistence import make_dict


class Intercessor(object):
    def __init__(self):
        self._db = make_dict()
        self._registry = {}

    def dispatch(self, event):
        if event[0] in self._registry:
            handler = self._registry[event[0]]
            fx = handler[0](make_dict({'db': self._db}), event)
            if 'db' in fx:
                self._db = fx['db']
        else:
            pass

    def reg_event_fx(self, event_name):
        def handler(h):
            self._registry[event_name] = [h]
            return h
        return handler

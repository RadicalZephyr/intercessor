__project__ = 'intercessor'
__version__ = '0.0.0'

VERSION = "{0} v{1}".format(__project__, __version__)

from pysistence import make_dict


class Intercessor(object):
    def __init__(self):
        self._db = make_dict()
        self._registry = {}

    def dispatch(self, event):
        handler = self._registry[event[0]]
        if handler:
            fx = handler[0](make_dict({'db': self._db}), event)
            if "db" in fx:
                self._db = fx["db"]
            ## TODO: to make this test work I actually need a full
            ## single interceptor thing working, and to write a
            ## wrapper that turns an event_db handler into an event_fx
            ## handler. Probably simpler to start with event_fx
            ## handler

    def reg_event_fx(self, event_name):
        def handler(h):
            self._registry[event_name] = [h]
            return h
        return handler

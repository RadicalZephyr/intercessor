__project__ = 'intercessor'
__version__ = '0.0.0'

VERSION = "{0} v{1}".format(__project__, __version__)
import log
from pysistence import make_dict

def _identity(x):
    x

class Interceptor(object):
    def __init__(self, *,
                 id = None,
                 before = None,
                 after = None):
        self.id = id
        self.before = before or _identity
        self.after = after or _identity


def fx_handler_to_interceptor(handler_fn):
    def fx_handler_fn(context):
        coeffects = context['coeffects']
        event = coeffects['event']
        effects = handler_fn(coeffects, event)
        return context.using(effects=effects)

    return Interceptor(id="fx-handler", before=fx_handler_fn)

class Intercessor(object):
    def __init__(self):
        self._db = make_dict()
        self._registry = {}

    def _make_context(self, event):
        return make_dict(coeffects=make_dict(db=self._db, event=event))

    def dispatch(self, event):
        if event[0] in self._registry:
            context = self._make_context(event)
            handler = self._registry[event[0]]
            ctx = handler[0].before(context)
            fx = ctx['effects']

            if 'db' in fx:
                self._db = fx['db']
        else:
            log.info('There is no handler registered for event "{}"'.format(event[0]))

    def reg_event_fx(self, event_name):
        def register(h):
            self._registry[event_name] = [fx_handler_to_interceptor(h)]
            return h
        return register

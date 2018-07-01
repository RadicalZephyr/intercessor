__project__ = 'intercessor'
__version__ = '0.0.0'

VERSION = "{0} v{1}".format(__project__, __version__)
import log
from pysistence import make_dict, make_list

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

    def _make_context(self, event, db, interceptors):
        coeffects = make_dict(db=self._db, event=event)
        return make_dict(coeffects=coeffects,
                         queue=make_list(*interceptors),
                         stack=make_list())

    def dispatch(self, event):
        if event[0] in self._registry:
            interceptors = self._registry[event[0]]
            context = self._make_context(event, self._db, interceptors)

            while context['queue'].first is not None:
                next_interceptor = context['queue'].first
                context = context.using(queue=context['queue'].rest)
                next_interceptor.before(context)
                context = context.using(stack=context['stack'].cons(next_interceptor))

            ctx = handler[0].before(context)
            fx = ctx['effects']

            if 'db' in fx:
                self._db = fx['db']
        else:
            log.info('There is no handler registered for event "{}"'.format(event[0]))

    def reg_event_fx(self, event_name):
        def register(h):
            interceptors = [fx_handler_to_interceptor(h)]
            self._registry[event_name] = interceptors
            h._interceptors = interceptors
            return h
        return register

    def with_after(self, after_fn):
        def push_interceptor(h):
            interceptor = Interceptor(id='before-fn', after=after_fn)
            h._interceptors.insert(0, interceptor)
            return h
        return push_interceptor

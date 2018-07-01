from intercessor import Intercessor

from pysistence import make_dict

def describe_app_creation():

    def test_reg_event_fx_decorator(expect):
        app = Intercessor()
        @app.reg_event_fx('set-foo')
        def handle_foo(cfx, event):
            return make_dict({'db': cfx['db'].using(foo=event[1])})

        app.dispatch(['set-foo', 1])

        expect(app._db['foo']) == 1

    def test_reg_fx_fn(expect):
        app = Intercessor()
        app.reg_event_fx('set-bar')(lambda cfx, event: make_dict({'db': cfx['db'].using(bar=event[1])}))

        app.dispatch(['set-bar', 10])

        expect(app._db['bar']) == 10

    def test_dispatch_unregistered_event(expect):
        app = Intercessor()

        app.dispatch(['not-an-event'])

        expect(app._db) == {}

    def test_reg_event_fx_with_interceptor(expect):
        app = Intercessor()

        def inc_foo(ctx):
            db = ctx['coeffects']['db']
            ctx.using(coeffects=ctx['coeffects'].using(db=db.using(foo=db['foo']+1)))

        @app.with_after(inc_foo)
        @app.reg_event_fx('set-foo')
        def handle_foo(cfx, event):
            return make_dict(db=cfx['db'].using(foo=event[1]))

        app.dispatch(['set-foo', 1])

        expect(app._db['foo']) == 2

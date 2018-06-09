from intercessor import Intercessor

from pysistence import make_dict

def describe_app_creation():

    def test_reg_event_fx(expect):
        app = Intercessor()
        @app.reg_event_fx("set-foo")
        def handle_foo(cfx, event):
            return make_dict({'db': cfx['db'].using(foo=event[1])})

        app.dispatch(("set-foo", 1))
        expect(app._db["foo"]) == 1

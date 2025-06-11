import threading
import types
import pytest
from core.tick.tick_engine import TickEngine

def test_register_and_list_subsystems():
    engine = TickEngine()
    called = []
    def handler1(delta):
        called.append(('h1', delta))
    def handler2(delta):
        called.append(('h2', delta))
    engine.register_subsystem('a', handler1, priority=2)
    engine.register_subsystem('b', handler2, priority=1)
    names = engine.list_subsystems()
    assert names == ['b', 'a']

def test_tick_dispatches_to_handlers():
    engine = TickEngine()
    flag = {'called': False}
    def handler(delta):
        flag['called'] = True
        flag['delta'] = delta
    engine.register_subsystem('x', handler, priority=0)
    engine.tick(42.0)
    assert flag['called']
    assert flag['delta'] == 42.0

def test_tick_dispatches_to_tick_method():
    engine = TickEngine()
    class Stub:
        def __init__(self):
            self.called = False
            self.delta = None
        def tick(self, delta):
            self.called = True
            self.delta = delta
    stub = Stub()
    engine.register_subsystem('stub', stub, priority=0)
    engine.tick(3.14)
    assert stub.called
    assert stub.delta == 3.14

def test_unregister_subsystem():
    engine = TickEngine()
    def handler(delta):
        pass
    engine.register_subsystem('foo', handler, priority=0)
    engine.unregister_subsystem('foo')
    assert 'foo' not in engine.list_subsystems() 
from neon.normalize import auto_assign
from neon.memoize import memoize, MEMO

class Foo:
    @auto_assign("test")
    def __init__(self, test):
        pass

def test_auto_assign():
    """tests that a test exists"""
    foo = Foo("Thing")
    assert hasattr(foo, "test")
    assert foo.test == "Thing"

@memoize
def fib(i):
    if i < 2:
        return 1
    return fib(i-1) + fib(i-2)

def test_memoize():
    assert fib(0) == 1
    assert fib(1) == 1
    assert fib(2) == 2
    assert fib(28) == 514229
    assert fib(29) == (2**3)*5*11*31*61

@memoize
def foo(bar):
    return bar

def test_dont_memoize():
    assert foo({}) == {}
    assert foo not in MEMO
    assert any([m.__name__ == "fib" for m in MEMO])

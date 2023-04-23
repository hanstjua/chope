from chope.functions.function import Function
from chope.css import px


def test_should_render_correctly():
    class test_func(Function):
        def __init__(self, arg_1: str, arg_2: int, arg_3: float):
            super().__init__(arg_1, arg_2, arg_3)

    assert test_func(px/1, 2, 3.0).render() == 'test_func(1px, 2, 3.0)'

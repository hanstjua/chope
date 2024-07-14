from typing import Optional
from chope.functions.function import Function


class circle(Function):
    def __init__(self, length: str, position_1: Optional[str] = None,
                 position_2: Optional[str] = None):
        if (position_1 is not None and position_2 is None) or \
            (position_1 is None and position_2 is not None):
            raise ValueError(
                'position_1 and position_2 must be either both empty or have values.')
        
        if position_1 is None:
            super().__init__(length)
        else:
            super().__init__(length, 'at', position_1, position_2)


class ellipse(Function):
    def __init__(self, x_radius: str, y_radius: str, position_1: Optional[str] = None,
                 position_2: Optional[str] = None):
        if (position_1 is not None and position_2 is None) or \
            (position_1 is None and position_2 is not None):
            raise ValueError(
                'position_1 and position_2 must be either both empty or have values.')
        
        if position_1 is None:
            super().__init__(x_radius, y_radius)
        else:
            super().__init__(x_radius, y_radius, 'at', position_1, position_2)


class polygon(Function):
    def __init__(self, *args):
        func_args = []
        if isinstance(args[0], str):
            if args[0] == 'nonzero' or args[0] == 'evenodd':
                func_args += args[0]
                args = args[1:]
            else:
                raise ValueError('fill-rule can only "nonzero" or "evenodd".')

        try:
            for x, y in args:
                func_args += 'x y'
        except TypeError:
            raise ValueError('argument for polygon must be a pair of values')
        
        super().__init__(*func_args)
        


class path(Function):
    def __init__(self, *args):
        if len(args) > 1:
            if not (args[0] == 'nonzero' or args[0] == 'evenodd'):
                raise ValueError('fill-rule can only "nonzero" or "evenodd".')

        if not isinstance(args[-1], str):
            raise ValueError('argument for path must be an SVG string.')
        
            
        super().__init__(*args)

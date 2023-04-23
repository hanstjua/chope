from typing import Optional, Union
from chope.functions.function import Function


class transformX(Function):
    def __init__(self, length: Union[int, str]):
        super().__init__(length)


class transformY(Function):
    def __init__(self, length: Union[int, str]):
        super().__init__(length)


class transformZ(Function):
    def __init__(self, length: Union[int, str]):
        super().__init__(length)


class translate(Function):
    def __init__(self, length_1: Union[int, str],
                 length_2: Optional[Union[int, str]] = None):
        if length_2 is not None:
            super().__init__(length_1, length_2)
        else:
            super().__init__(length_1)


class translate3d(Function):
    def __init__(self, tx: Union[int, str], ty: Optional[Union[int, str]] = None,
                 tz: Optional[Union[int, str]] = None):
        if (ty is None and tz is not None) or (tz is None and ty is not None):
            raise ValueError(
                'ty and tz must either be both None or both with values.')
        
        if '%' in tz:
            raise ValueError('tz cannot be percentage.')
        
        if ty is None and tz is None:
            super().__init__(tx)
        else:
            super().__init__(tx, ty, tz)

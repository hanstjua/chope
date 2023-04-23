from typing import Optional, Union
from chope.functions.function import Function


class rgb(Function):
    def __init__(self, red: int, green: int, blue: int,
                 alpha: Optional[Union[int, str]] = None):
        if isinstance(alpha, str) and '%' not in alpha:
            raise ValueError('alpha must be an integer or a percentage.')
        
        if alpha is not None:
            super().__init__(red, green, blue, alpha)
        else:
            super().__init__(red, green, blue)


class hsl(Function):
    def __init__(self, hue: Union[int, str], saturation: str, lightness: str,
                 alpha: Optional[Union[int, str]] = None):
        if isinstance(hue, str) and \
            'deg' not in hue and \
            'rad' not in hue and \
            'grad' not in hue and \
            'turn' not in hue:
            raise ValueError('hue must be an integer or an angle.')
        
        if '%' not in saturation:
            raise ValueError('saturation must be a percentage.')
        
        if '%' not in lightness:
            raise ValueError('lightness must be a percentage.')
        
        if isinstance(alpha, str) and \
            '%' not in alpha:
            raise ValueError('alpha must be an integer or a percentage.')
        
        if alpha is not None:
            super().__init__(hue, saturation, lightness, alpha)
        else:
            super().__init__(hue, saturation, lightness)

    
class hwb(Function):
    def __init__(self, hue: Union[int, str], whiteness: str, blackness: str,
                 alpha: Optional[Union[int, str]] = None):
        if isinstance(hue, str) and \
            'deg' not in hue and \
            'rad' not in hue and \
            'grad' not in hue and \
            'turn' not in hue:
            raise ValueError('hue must be an integer or an angle.')
        
        if '%' not in whiteness:
            raise ValueError('whiteness must be a percentage.')
        
        if '%' not in blackness:
            raise ValueError('blackness must be a percentage.')
        
        if isinstance(alpha, str) and \
            '%' not in alpha:
            raise ValueError('alpha must be an integer or a percentage.')
        
        if alpha is not None:
            super().__init__(hue, whiteness, blackness, alpha)
        else:
            super().__init__(hue, whiteness, blackness)

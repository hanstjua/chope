from typing import Iterable, List, Union


class Rule:
    def __init__(self, name: str, declarations: List[dict]):
        self.__declarations = declarations
        self.__name = name

    def render(self, indent: int = 2) -> str:
        nl = '\n'
        indented = indent > 0
        declarations_str = ''
        for property, value in self.__declarations.items():
            if isinstance(value, Iterable) and not isinstance(value, str):
                value = ' '.join(value)

            declarations_str += \
                f'{" " * indent}{property.replace("_", "-")}: {value};{nl * indented}'

        return f'{self.__name} {{{nl * indented}{declarations_str}}}'


class Css:
    def __init__(self, rules: List[Rule]):
        self._rules = rules

    def __class_getitem__(cls, items: Union[slice, Iterable[slice]]) -> 'Css':
        if isinstance(items, slice):
            rules = [Rule(items.start.replace('_', '-'), items.stop)]
        else:
            rules = [Rule(item.start.replace('_', '-'), item.stop)
                     for item in items]

        return cls(rules)

    def render(self, indent: int = 2) -> str:
        indented = indent > 0
        return ('\n\n' * indented).join((rule.render(indent) for rule in self._rules))


class Unit:
    def __init__(self, name: str):
        self.__name = name

    def __truediv__(self, value) -> str:
        return str(value) + self.__name


cm = Unit('cm')
ch = Unit('ch')
em = Unit('em')
ex = Unit('ex')
in_ = Unit('in')
mm = Unit('mm')
pc = Unit('pc')
percent = Unit('%')
pt = Unit('pt')
px = Unit('px')
rem = Unit('rem')
vh = Unit('vh')
vmax = Unit('vmax')
vmin = Unit('vmin')
vw = Unit('vw')

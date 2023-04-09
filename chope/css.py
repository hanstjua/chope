from typing import Dict, Iterable, Union


class Rule:
    def __init__(self, **kwargs):
        self.__declarations = kwargs

    def render(self, indent: int = 2) -> str:
        ret = ''

        for property, value in self.__declarations.items():
            if isinstance(value, Iterable) and not isinstance(value, str):
                value = ' '.join(value)

            ret += f'{" " * indent}{property.replace("_", "-")}: {value};\n'

        return ret


class Css:
    def __init__(self, rules: Dict[str, Rule]) -> None:
        self._rules = rules

    def __class_getitem__(cls, rules: Union[slice, Iterable[slice]]) -> 'Css':
        rules_dict = {}

        if isinstance(rules, slice):
            rules_dict[rules.start.replace('_', '-')] = rules.stop
        else:
            for r in rules:
                rules_dict[r.start.replace('_', '-')] = r.stop

        return cls(rules_dict)

    def render(self, indent: int = 2) -> str:
        rules_str = [
            f'{k} {{\n{v.render(indent)}}}' for k, v in self._rules.items()]

        return '\n\n'.join(rules_str)


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

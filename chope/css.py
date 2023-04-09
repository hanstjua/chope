from typing import Dict, Iterable, Union


class rule:
    def __init__(self, **kwargs):
        self.__declarations = kwargs

    def render(self, indent: int = 2) -> str:
        ret = ''

        for k, v in self.__declarations.items():
            if isinstance(v, Iterable) and not isinstance(v, str):
                v = ' '.join(v)

            ret += f'{" " * indent}{k.replace("_", "-")}: {v};\n'

        return ret


class css:
    def __init__(self, rules: Dict[str, rule]) -> None:
        self._rules = rules

    def __class_getitem__(cls, rules: Union[slice, Iterable[slice]]) -> 'css':
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


em = Unit('em')
px = Unit('px')
rem = Unit('rem')

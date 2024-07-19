from functools import reduce
from typing import Any, Dict, Iterable, List, Set, Union

from chope.variable import Var


class RenderError(Exception):
    pass


class Rule:
    def __init__(self, name: str, declarations: List[dict]):
        self.__declarations = declarations
        self.__name = name

    def __eq__(self, __value: object) -> bool:
        return self.__declarations == __value.__declarations \
            and self.__name == __value.__name

    def render(self, indent: int = 2) -> str:
        nl = '\n'
        indented = indent > 0
        declarations_str = ''

        def get_value(var: Any) -> Any:
            if isinstance(var, Dict):
                return var
            elif isinstance(var, Var):
                return get_value(var.value)
            else:
                return var

        declarations = get_value(self.__declarations)

        if not isinstance(declarations, dict):
            raise RenderError(f"Invalid declaration {declarations} in rule '{self.__name}'. Declarations must be a dict object.")
        
        for property, value in declarations.items():
            value = get_value(value)
            if isinstance(value, Iterable) and not isinstance(value, str):
                value = ' '.join(value)

            declarations_str += \
                f'{" " * indent}{property.replace("_", "-")}: {value};{nl * indented}'

        return f'{self.__name} {{{nl * indented}{declarations_str}}}'
    
    def get_vars(self) -> Set[str]:
        def get_var(var: Var) -> Set[str]:
            if isinstance(var.value, Var):
                return {var.name}.union(get_var(var.value))
            else:
                return {var.name}
            
        if isinstance(self.__declarations, Var):
            return get_var(self.__declarations)
        elif isinstance(self.__declarations, dict):
            return reduce(lambda out, s: out.union(s), (get_var(d) for d in self.__declarations.values()), set())
        else:
            return set()
    
    def set_vars(self, values: Dict[str, Any]) -> 'Rule':
        def set_var(comp: Any, values: Dict[str, Any]) -> Any:
            if isinstance(comp, Var):
                new_var = comp.set_value(values)
                if new_var == comp and isinstance(new_var.value, Var):
                    return Var(new_var.name, new_var.value.set_vars(values))
                else:
                    return new_var
            else:
                return comp
            
        if isinstance(self.__declarations, dict):
            new_declarations = {attr : set_var(value, values) for attr, value in self.__declarations.items()}
        elif isinstance(self.__declarations, Var):
            old_var = self.__declarations
            new_var = set_var(old_var, values)
            new_declarations = self if new_var == old_var else Var(old_var.name, new_var.value)
        else:
            new_declarations = self.__declarations

        return self if new_declarations == self.__declarations else Rule(self.__name, new_declarations)


class Css:
    def __init__(self, rules: List[Rule]):
        self._rules = rules

    def __eq__(self, __value: object) -> bool:
        return self._rules == __value._rules

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
    
    def get_vars(self) -> Set[str]:
        return reduce(lambda out, s: out.union(s), (rule.get_vars() for rule in self._rules), set())
    
    def set_vars(self, values: Dict[str, Any]) -> 'Css':
        # shoutout to Dua Lipa
        new_rules = [rule.set_vars(values) for rule in self._rules]
        return self if new_rules == self._rules else Css(new_rules)


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

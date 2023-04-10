from typing import Iterable, Union

from chope.css import Css


class Element:
    def __init__(self, **kwargs):
        self._components: Iterable[Component] = []
        self._attributes = kwargs

    def __class_getitem__(cls, comps: Union['Component', Iterable['Component']]) \
            -> 'Element':
        inst = cls()
        if isinstance(comps, Component.__args__):
            inst._components = (comps,)
        else:
            inst._components = comps

        return inst

    def __getitem__(self, comps: Union['Component', Iterable['Component']]) \
            -> 'Element':
        if isinstance(comps, Component.__args__):
            self._components = (comps,)
        else:
            self._components = comps

        return self

    def render(self, indent: int = 2) -> str:
        nl = '\n'
        indented = indent > 0

        comp_str = nl * indented
        for comp in self._components:
            if isinstance(comp, str):
                comp_str += f'{" " * indent}{comp}{nl * indented}'
            else:
                _comp_str = comp.render(indent).replace(
                    nl, f'{nl * indented}{" " * indent}')
                comp_str += f'{" " * indent}{_comp_str}{nl * indented}'

        name = self.__class__.__name__

        attrs_str = ''
        for attr, val in self._attributes.items():
            val = f'"{val}"' if isinstance(val, str) else str(val)

            attrs_str += f' {attr.replace("_", "")}={val}'

        return f'<{name}{attrs_str}>{comp_str}</{name}>'


Component = Union[str, Element, Css]

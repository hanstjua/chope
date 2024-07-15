import re
from typing import Any, Dict, Iterable, Union
from chope.variable import Var

from chope.css import Css


class Element:
    def __init__(self, *args, **kwargs):
        self._components: Iterable[Component] = []
        self._attributes = kwargs
        self._classes = self._attributes.pop('class_', '')
        self._id = self._attributes.pop('id', '')

        if args:
            selector_pattern = \
                r'^(?:#([^\s\.#]+))?(?:\.([^\s#]+))?'  ## #id.class1.class2
            
            id, classes = re.findall(selector_pattern, args[0])[0]

            if id and self._id:
                raise ValueError(
                    f'id declared twice: #{id} and id="{self._id}"')

            self._id = id
            self._classes = f'{classes.replace(".", " ")} {self._classes}'.strip()

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
                _comp = comp.replace('\n', '<br>')
                comp_str += f'{" " * indent}{_comp}{nl * indented}'
            elif isinstance(comp, Var):
                _comp = comp.default.replace('\n', '<br>')
                comp_str += f'{" " * indent}{_comp}{nl * indented}'
            else:
                _comp_str = comp.render(indent).replace(
                    nl, f'{nl * indented}{" " * indent}')
                comp_str += f'{" " * indent}{_comp_str}{nl * indented}'

        name = self.__class__.__name__

        attrs_str = f' id="{self._id}"' if self._id else ''
        attrs_str += f' class="{self._classes}"' if self._classes else ''

        for attr, val in self._attributes.items():
            if isinstance(val, bool):
                attrs_str += f' {attr}'
            else:
                val = f'"{val}"' if isinstance(val, str) else str(val)

                attrs_str += f' {attr}={val}'

        return f'<{name}{attrs_str}>{comp_str}</{name}>'
    
    def set_vars(self, values: Dict[str, Any]) -> 'Component':
        def set_var(comp: Component, values: Dict[str, Any]) -> Component:
            if isinstance(comp, (Element, Css)):
                return comp.set_vars(values)
            elif isinstance(comp, Var):
                return comp.to_value(values)
            else:
                return comp
            
        ret = self.__class__(
            id=set_var(self._id, values),
            class_=set_var(self._classes, values),
            **{key: set_var(value, values) for key, value in self._attributes.items()}
        )
        ret._components = tuple(set_var(comp, values) for comp in self._components)

        return ret


Component = Union[str, Element, Css, Var]

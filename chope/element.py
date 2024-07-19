from ast import literal_eval
from functools import reduce
import re
from typing import Any, Dict, Iterable, Set, Union
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

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Element) \
            and self._components == __value._components \
            and self._attributes == __value._attributes \
            and self._classes == __value._classes \
            and self._id == __value._id

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
        def render_var(value, quote_str=False) -> str:
            if isinstance(value, (Element, Css)):
                return value.render(indent=indent).replace('\n', f'\n{" " * indent}')
            elif isinstance(value, Var):
                return render_var(value.value, quote_str=quote_str)
            elif isinstance(value, str):
                return '"' + value.replace('\n', '<br>') + '"' if quote_str else value.replace('\n', '<br>')
            else:
                return str(value)
                    
        nl = '\n'
        indented = indent > 0

        comp_str = nl * indented
        for comp in self._components:
            if isinstance(comp, str):
                _comp = comp.replace('\n', '<br>')
                comp_str += f'{" " * indent}{_comp}{nl * indented}'
            elif isinstance(comp, Var):    
                comp_str += f'{" " * indent}{render_var(comp)}{nl * indented}'
            else:
                _comp_str = comp.render(indent).replace(
                    nl, f'{nl * indented}{" " * indent}')
                comp_str += f'{" " * indent}{_comp_str}{nl * indented}'

        name = self.__class__.__name__

        attrs_str = f' id={render_var(self._id, True)}' if self._id else ''
        attrs_str += f' class={render_var(self._classes, True)}' if self._classes else ''

        for attr, val in self._attributes.items():
            if isinstance(val, bool):
                attrs_str += f' {attr}'
            else:
                attrs_str += f' {attr}={render_var(val, True)}'

        return f'<{name}{attrs_str}>{comp_str}</{name}>'
    
    def get_vars(self) -> Set[str]:
        ret = set()
        if isinstance(self._id, Var):
            ret.add(self._id.name)

        if isinstance(self._classes, Var):
            ret.add(self._classes.name)

        ret.update({val.name for val in self._attributes.values() if isinstance(val, Var)})

        def get_var(comp):
            if isinstance(comp, (Element, Css)):
                return comp.get_vars()
            elif isinstance(comp, Var):
                if isinstance(comp.value, Var):
                    return {comp.name}.union(get_var(comp.value))
                elif isinstance(comp.value, (Element, Css)):
                    return {comp.name}.union(comp.value.get_vars())
                else:
                    return {comp.name}
            else:
                return set()
            
        ret.update(reduce(lambda res, comp: res.union(get_var(comp)), self._components, set()))

        return ret
    
    def set_vars(self, values: Dict[str, Any]) -> 'Component':
        def set_var(comp: Component, values: Dict[str, Any]) -> Component:
            if isinstance(comp, (Element, Css)):
                return comp.set_vars(values)
            elif isinstance(comp, Var):
                new_var = comp.set_value(values)
                if new_var == comp and isinstance(new_var.value, (Element, Css)):
                    return Var(new_var.name, new_var.value.set_vars(values))
                else:
                    return new_var
            else:
                return comp
            
        id = set_var(self._id, values)
        classes = set_var(self._classes, values)
        attributes = {key: set_var(value, values) for key, value in self._attributes.items()}
        components = tuple(set_var(comp, values) for comp in self._components)

        if id == self._id \
            and classes == self._classes \
            and attributes == self._attributes \
            and components == self._components:
            return self
        
        else:
            ret = self.__class__(
                id=id,
                class_=classes,
                **attributes
            )[
                components
            ]

            return ret
    
    def __str__(self) -> str:
        return self.render(0)
    
    def __repr__(self) -> str:
        return self.__str__()


Component = Union[str, Element, Css, Var]

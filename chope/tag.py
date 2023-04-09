from typing import Iterable, Union


Component = Union[str, 'tag']


class tag:
    def __init__(self, **kwargs):
        self._components: Iterable[Component] = []
        self._attributes = kwargs

    def __class_getitem__(cls, comps: Union[Component, Iterable[Component]]) -> 'tag':
        inst = cls()
        if isinstance(comps, str) or isinstance(comps, tag):
            inst._components = (comps,)
        else:
            inst._components = comps

        return inst
    
    def __getitem__(self, comps: Union[Component, Iterable[Component]]) -> 'tag':
        if isinstance(comps, str) or isinstance(comps, tag):
            self._components = (comps,)
        else:
            self._components = comps

        return self
    
    def render(self, indent: int = 2) -> str:
        comp_str = '\n'
        for comp in self._components:
            if isinstance(comp, str):
                comp_str += f'{" " * indent}{comp}\n'
            else:
                _comp_str = comp.render(indent).replace("\n", f"\n{' ' * indent}")
                comp_str += f'{" " * indent}{_comp_str}\n'

        name = self.__class__.__name__

        attrs_str = ''
        for k, v in self._attributes.items():
            v = f'"{v}"' if isinstance(v, str) else str(v)

            attrs_str += f' {k}={v}'

        return f'<{name}{attrs_str}>{comp_str}</{name}>'
        
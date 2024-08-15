import re
from functools import reduce
from itertools import chain
from typing import Any, Dict, Iterable, Set, Tuple, Union

from chope.css import Css
from chope.variable import Var


class DuplicateAttributeError(Exception):
    pass


class Element:
    def __init__(self, *args, **kwargs):
        self._components: Tuple[Component, ...] = ()

        self._classes = ""
        self._id = ""
        self._attributes = {}

        if args:
            selector_id, selector_classes = (
                self.__get_id_classes_from_selector(args[0])
                if len(args) % 2
                else ("", "")
            )
            self._classes = selector_classes

            tuple_id, tuple_classes, tuple_attrs = (
                self.__get_id_classes_attrs_from_tuple(args[len(args) % 2 :])
            )

            if selector_id and tuple_id:
                raise DuplicateAttributeError(
                    f"id declared twice: id={selector_id} and id={tuple_id}"
                )

            self._id = selector_id or tuple_id
            self._classes = (
                f"{self._classes} {tuple_classes}".strip()
                if tuple_classes
                else self._classes
            )

            self._attributes.update(tuple_attrs)

        if self._id and "id" in kwargs:
            raise DuplicateAttributeError(
                f'id declared twice: id={self._id} and id={kwargs["id"]}'
            )

        self._classes = (
            f'{self._classes} {kwargs.pop("class_")}'.strip()
            if "class_" in kwargs
            else self._classes
        )
        self._id = kwargs.pop("id", self._id)
        self._attributes.update(
            {key.replace("_", "-"): value for key, value in kwargs.items()}
        )

    @staticmethod
    def __get_id_classes_from_selector(selector: str) -> Tuple[str, str]:
        selector_pattern = r"^(?:#([^\s\.#]+))?(?:\.([^\s#]+))?"  # id.class1.class2

        results = re.findall(selector_pattern, selector)[0]
        if results:
            id, classes = results
            return id, f'{classes.replace(".", " ")}'.strip()
        else:
            return "", ""

    @staticmethod
    def __get_id_classes_attrs_from_tuple(
        tuple_: Tuple[str, ...],
    ) -> Tuple[str, str, dict]:
        attrs = {tuple_[i - 1]: tuple_[i] for i in range(1, len(tuple_), 2)}

        id = attrs.pop("id", "")
        classes = f'{attrs.pop("class")}'.strip() if "class" in attrs else ""

        return id, classes, attrs

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, Element)
            and self._components == __value._components
            and self._attributes == __value._attributes
            and self._classes == __value._classes
            and self._id == __value._id
        )

    def __class_getitem__(
        cls, comps: Union["Component", Iterable["Component"], Tuple[Any, ...]]
    ) -> "Element":
        inst = cls()
        if isinstance(comps, Component.__args__):
            inst._components = (comps,)
        else:

            def as_tuple(x):
                return (
                    (x,)
                    if isinstance(x, str) or not isinstance(x, Iterable)
                    else tuple(x)
                )

            comps_lists = (as_tuple(comp) for comp in comps)
            inst._components = reduce(lambda l1, l2: l1 + l2, comps_lists)

        return inst

    def __getitem__(
        self, comps: Union["Component", Iterable["Component"], Tuple[Any, ...]]
    ) -> "Element":
        if isinstance(comps, Component.__args__):
            self._components = (comps,)
        else:

            def as_tuple(x):
                return (
                    (x,)
                    if isinstance(x, str) or not isinstance(x, Iterable)
                    else tuple(x)
                )

            comps_lists = (as_tuple(comp) for comp in comps)
            self._components = reduce(lambda l1, l2: l1 + l2, comps_lists)

        return self
    
    def __call__(self, *args, **kwargs) -> 'Element':
        ret = self.__class__()
        updated_element = self.__class__(*args, **kwargs)
        ret._components = self._components
        ret._id = updated_element._id if updated_element._id else self._id
        ret._classes = updated_element._classes if updated_element._classes else self._classes
        ret._attributes = updated_element._attributes if updated_element._attributes else self._attributes

        return ret

    def render(self, indent: int = 2) -> str:
        nl = "\n"
        indented = indent > 0

        def render_var(value, quote_str=False) -> str:
            if isinstance(value, (Element, Css)):
                return value.render(indent=indent).replace(nl, f'{nl}{" " * indent}')
            elif isinstance(value, Var):
                return render_var(value.value, quote_str=quote_str)
            elif isinstance(value, str):
                return (
                    '"' + value.replace(nl, "<br>") + '"'
                    if quote_str
                    else value.replace(nl, "<br>")
                )
            elif isinstance(value, Iterable):
                return f'{nl * indented}{" " * indent}'.join((render_var(i) for i in value))
            else:
                return str(value)

        comp_str = nl * indented
        for comp in self._components:
            if isinstance(comp, str):
                _comp = comp.replace("\n", "<br>")
                comp_str += f'{" " * indent}{_comp}{nl * indented}'
            elif isinstance(comp, Var):
                comp_str += f'{" " * indent}{render_var(comp)}{nl * indented}'
            else:
                _comp_str = comp.render(indent).replace(
                    nl, f'{nl * indented}{" " * indent}'
                )
                comp_str += f'{" " * indent}{_comp_str}{nl * indented}'

        name = self.__class__.__name__

        attrs_str = f" id={render_var(self._id, True)}" if self._id else ""
        attrs_str += (
            f" class={render_var(self._classes, True)}" if self._classes else ""
        )

        for attr, val in self._attributes.items():
            attrs_str += (
                f" {attr}"
                if isinstance(val, bool)
                else f" {attr}={render_var(val, True)}"
            )

        return f"<{name}{attrs_str}>{comp_str}</{name}>"

    def get_vars(self) -> Set[str]:
        ret = set()
        if isinstance(self._id, Var):
            ret.add(self._id.name)

        if isinstance(self._classes, Var):
            ret.add(self._classes.name)

        ret.update(
            {val.name for val in self._attributes.values() if isinstance(val, Var)}
        )

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

        return ret.union(
            reduce(lambda res, comp: res.union(get_var(comp)), self._components, set())
        )

    def set_vars(self, values_: Dict[str, Any] = {}, **kwargs) -> "Component":
        combined_values = {k: v for k, v in chain(values_.items(), kwargs.items())}

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

        id = set_var(self._id, combined_values)
        classes = set_var(self._classes, combined_values)
        attributes = {
            key: set_var(value, combined_values)
            for key, value in self._attributes.items()
        }
        components = tuple(set_var(comp, combined_values) for comp in self._components)

        if (
            id == self._id
            and classes == self._classes
            and attributes == self._attributes
            and components == self._components
        ):
            return self

        else:
            return self.__class__(id=id, class_=classes, **attributes)[components]

    def __str__(self) -> str:
        return self.render(0)

    def __repr__(self) -> str:
        return self.__str__()


Component = Union[str, Element, Css, Var]

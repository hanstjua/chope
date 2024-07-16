from typing import Any, Dict


class Var:
    def __init__(self, name: str, value: Any = '') -> None:
        self._name = name
        self._value = value

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Var) and self._name == __value._name and self._value == __value._value

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Any:
        return self._value
    
    def set_value(self, values: Dict[str, Any]) -> 'Var':
        return self if self._name not in values else Var(self._name, values[self._name])

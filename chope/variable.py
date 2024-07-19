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
        if self._name in values:
            return Var(self._name, values[self._name])
        else:
            new_value = self._value.set_value(values) if isinstance(self._value, Var) else self._value
            if new_value != self._value:
                return Var(self._name, new_value)
            else:
                return self
            
    def __str__(self) -> str:
        return f'Var["{self.name}","{self.value}"]'
    
    def __repr__(self) -> str:
        return self.__str__()

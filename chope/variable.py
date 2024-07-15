from typing import Any, Dict


class Var:
    def __init__(self, name: str, default: Any = '') -> None:
        self._name = name
        self._default = default

    @property
    def name(self) -> str:
        return self._name

    @property
    def default(self) -> Any:
        return self._default

    def to_value(self, values: Dict[str, Any]) -> Any:
        return values.get(self._name, self._default)

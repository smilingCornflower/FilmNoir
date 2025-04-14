from abc import ABC, abstractmethod
from typing import Any


class AbstractMapper(ABC):
    @abstractmethod
    def map(self, *args: Any, **kwargs: Any) -> Any:
        pass

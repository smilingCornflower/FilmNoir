from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.ports.filter import AbstractFilter
from domain.ports.model import AbstractModel
from domain.value_objects.common import Id

T = TypeVar("T", bound=AbstractModel)
F = TypeVar("F", bound=AbstractFilter)


class AbstractRepository(ABC, Generic[T, F]):
    @abstractmethod
    def get_by_id(self, id_: Id) -> T:
        pass

    @abstractmethod
    def get_all(self, filter_: F) -> list[T]:
        pass

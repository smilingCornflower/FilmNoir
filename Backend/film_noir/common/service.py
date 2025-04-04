from abc import abstractmethod
from common.value_objects import ContentQueryParamsVo
from common.models.base_content import BaseContent


class BaseContentService[T: BaseContent, P: ContentQueryParamsVo]:
    @classmethod
    @abstractmethod
    def get(cls, params: P) -> list[T]:
        raise NotImplementedError

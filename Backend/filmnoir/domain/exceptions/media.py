from domain.exceptions import BaseDomainException


class MediaException(BaseDomainException):
    pass


class MovieNotFound(MediaException):
    pass

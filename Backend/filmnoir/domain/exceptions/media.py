from domain.exceptions import DomainException


class MediaException(DomainException):
    pass


class MovieNotFound(MediaException):
    pass

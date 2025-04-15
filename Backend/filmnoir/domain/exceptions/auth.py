from domain.exceptions import DomainException


class AuthException(DomainException):
    pass


class InvalidCredentialsException(AuthException):
    pass


class InvalidTokenException(AuthException):
    pass


class InvalidAccessTokenException(InvalidTokenException):
    pass


class InvalidRefreshTokenException(InvalidTokenException):
    pass

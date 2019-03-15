
class NotFoundError(Exception):
    pass


class NotAllowedError(Exception):
    pass


class AuthorizationFailedError(Exception):
    pass


class RequestException(Exception):
    pass


class AuthorizationTargetError(Exception):
    pass

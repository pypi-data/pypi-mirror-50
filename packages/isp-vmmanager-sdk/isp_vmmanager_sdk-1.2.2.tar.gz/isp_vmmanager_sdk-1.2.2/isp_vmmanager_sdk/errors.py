class ApiException(Exception):
    pass


class AuthException(Exception):
    pass


class NeedPasswordOrKey(Exception):
    pass


class BadAuthError(Exception):
    pass

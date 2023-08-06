class FechoException(Exception):
    pass


class InvalidCookie(FechoException):
    pass


class InvalidURL(FechoException):
    pass

class ReturnedNoData(FechoException):
    pass

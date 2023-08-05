class InfinityCoinError(Exception):
    """ Базовый класс """

class Unauthorized(InfinityCoinError):
    """ Неверный ключ API """

class MethodNotFound(InfinityCoinError):
    """ Попытка вызова несуществующего метода """

class InvalidGETParam(InfinityCoinError):
    """ Переданы неверные GET параметры """
INTERNAL_SERVER_ERROR = 'Internal Server Error'


class MyException(Exception):
    """Base HTTP Exception
    """
    msg_fmt = "An unknown exception occurred."
    code = 500
    headers = {}
    safe = False
    title = INTERNAL_SERVER_ERROR

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        self.__dict__.update(self.kwargs)

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.msg_fmt % kwargs

            except Exception:
                message = self.msg_fmt

        self.message = message
        super().__init__(message)

    def final_message(self):
        msg = {
            'error': {
                'message': self.message,
                'code': self.code,
                'title': self.title
            }
        }
        return msg

    def __repr__(self):
        dict_repr = self.__dict__
        dict_repr['class'] = self.__class__.__name__
        return str(dict_repr)


# Basic Exceptions:
class BadRequest(MyException):
    msg_fmt = 'Bad request'
    title = 'Bad request'
    code = 400


class NotFound(MyException):
    msg_fmt = 'Resource could not be found.'
    title = 'Not Found'
    code = 404


class Conflict(MyException):
    msg_fmt = 'Resource already exist.'
    title = 'Conflict'
    code = 409


class InternalCommunication(MyException):
    msg_fmt = 'Internal communication error'


class InvalidJsonScheme(BadRequest):
    msg_fmt = '%(scheme_error)s'


# Specific exceptions
class ProjectNotFound(NotFound):
    msg_fmt = 'Project %(project_name)s could not be found.'


class PackageNotFound(NotFound):
    msg_fmt = 'Package %(package_name)s could not be found.'

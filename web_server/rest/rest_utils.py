import functools
import my_exception
from my_log import LOG


def normal_response(code: int):
    """Attaches response code to a method.

    This decorator appends error code to the response, in case the returned value is
    """

    def decorator_func(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            retval = func(*args, **kwargs)
            if isinstance(retval, tuple):
                return retval
            # Return special HTTP error code
            return retval, code

        return wrapper_func

    return decorator_func


def expected_errors(*errors: int):
    """
    Specifies expected exceptions.

    Specify which exceptions may occur when an API method is called. If an
    unexpected exception occurs then return a 500 instead and ask the user
    of the API to file a bug report.

    :type errors: array of int
    :param errors: List of expected HTTP status code.
    :return:
    """

    def decorator_func(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                rv = func(*args, **kwargs)
                if rv is None:
                    msg = f'INVALID RETURN VALUE FROM FUNCTION <{func.__name__}>!'
                    LOG.error(msg)
                    return {'message': msg}, 500
                return rv
            except my_exception.MyException as exc:
                if exc.code not in errors:
                    msg = f'Unexpected error code {exc.code} {exc.final_message()}!!!'
                    print(msg)
                    LOG.exception(msg)
                    return {'message': msg}, 500
                return exc.final_message(), exc.code
            except Exception as exc:
                msg = f'Unexpected error code {str(exc)}!!!'
                print(msg)
                LOG.exception(msg)
                return {'message': msg}, 500

        return wrapper_func

    return decorator_func

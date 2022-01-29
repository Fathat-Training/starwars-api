

# ------------------------------
#  Module Imports
# ------------------------------
import sys


def reraise(exc_type, exc_value, exc_traceback=None):
    """
        Reraise the error with appropriate stack trace
    :param exc_type: exception type
    :param exc_value: the message and function name
    :param exc_traceback: the traceback
    :return:
    """

    if exc_value is None:
        exc_value = exc_type()
    try:    
        if exc_value.__traceback__ is not exc_traceback:
            raise exc_value.with_traceback(exc_traceback)
    except:
        pass

    raise exc_value


def handle_error(e, msg, where):
    """
    Framework independent error handler - We don't need flask to handle some script errors

    Can be called as     except Exception as e:
        msg = 'Some Error ---> ' + str(e)
        handle_error(e, msg, inspect.currentframe().f_code.co_name)

    :param e: the exception
    :param msg: the message
    :param where: function error occurred in
    :return:
    """
    reraise(type(e)(str(e) +msg + ' ---> at %s' % where), sys.exc_info()[2])

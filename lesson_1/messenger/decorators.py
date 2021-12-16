"""Декоратор"""

import sys
import logging
import logs.config_server_log
import logs.config_client_log
import traceback

if 'server.' in sys.argv[0]:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(log_func):
    def wrap(*args, **kwargs):
        res = log_func(*args, **kwargs)
        LOGGER.debug(f'функция {log_func.__name__} (параметры:{args}, {kwargs}). '
                     f'вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}.')
        return res

    return wrap


class LogClass:
    """вариант декоратора через класс"""
    def __call__(self, log_func):
        def wrap(*args, **kwargs):
            res = log_func(*args, **kwargs)
            LOGGER.debug(f'функция {log_func.__name__} (параметры:{args}, {kwargs}). '
                         f'вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}.')
            return res

        return wrap

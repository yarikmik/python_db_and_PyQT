"""Программа-сервер"""

import socket
import sys
import json
import logging
import argparse
import select
import time
import logs.config_server_log
from descriptors import Port
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS, MESSAGE, MESSAGE_TEXT, \
    RESPONSE_400, DESTINATION, RESPONSE_200, EXIT, SENDER
from common.utils import get_message, send_message
from errors import IncorrectDataRecivedError
from decorators import log, LogClass
from metaclasses import ServerVerifier

# Инициализируем серверный логгер
SERVER_LOGGER = logging.getLogger('server')


# @log
@LogClass()
def process_client_message(message, messages_list, client, clients, names):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
    проверяет корректность, отправляет словарь-ответ в случае необходимости.
    :param message:
    :param messages_list:
    :param client:
    :param clients:
    :param names:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # Если это сообщение о присутствии, принимаем и отвечаем
    if ACTION in message and message[ACTION] == PRESENCE and \
            TIME in message and USER in message:
        # Если такой пользователь ещё не зарегистрирован,
        # регистрируем, иначе отправляем ответ и завершаем соединение.
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    # Если это сообщение, то добавляем его в очередь сообщений.
    # Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            DESTINATION in message and TIME in message \
            and SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    # Если клиент выходит
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    # Иначе отдаём Bad request
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен.'
        send_message(client, response)
        return


# @log
@LogClass()
def process_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_socks:
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                           f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


# @log
@LogClass()
def get_argv():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    server.py -p 8888 -a 127.0.0.1
    :return:
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    # if not 1023 < listen_port < 65536:
    #     SERVER_LOGGER.critical(
    #         f'Попытка запуска сервера с указанием неподходящего порта '
    #         f'{listen_port}. Допустимы адреса с 1024 до 65535.')
    #     sys.exit(1)

    return listen_address, listen_port


class ServerSocket(metaclass=ServerVerifier):
    # __slots__ = ('listen_port', 'listen_address')
    listen_port = Port()

    # @log
    # @LogClass()
    def __init__(self, ip='', port=''):
        self.listen_port = port
        self.listen_address = ip
        SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {self.listen_port}, '
                           f'адрес с которого принимаются подключения: {self.listen_address}.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def print_server_params(self):
        print(f'Слушаем порт:{self.listen_port}, адрес:{self.listen_address}')

    # @log
    # @LogClass()
    def server_init(self):
        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))
        transport.settimeout(1)  # задержка

        # Слушаем порт
        self.sock = transport
        self.sock.listen(MAX_CONNECTIONS)
        # transport.listen(MAX_CONNECTIONS)

        # Словарь, содержащий имена пользователей и соответствующие им сокеты.
        names = dict()

        # список клиентов , очередь сообщений
        clients = []
        messages = []
        err_lst = []
        while True:
            try:
                client, client_address = transport.accept()
            except OSError:
                pass
            else:
                SERVER_LOGGER.info(f'Установлено соедение с {client_address}')
                clients.append(client)

            recv_data_lst = []
            send_data_lst = []

            # Проверяем на наличие ждущих клиентов
            try:
                if clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass

            # принимаем сообщения и если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        process_client_message(get_message(client_with_message),
                                               messages, client_with_message, clients, names)
                    except Exception:
                        SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                           f'отключился от сервера.')
                        clients.remove(client_with_message)

            # Если есть сообщения, обрабатываем каждое.
            for i in messages:
                try:
                    process_message(i, names, send_data_lst)
                except Exception:
                    SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                    clients.remove(names[i[DESTINATION]])
                    del names[i[DESTINATION]]
            messages.clear()


if __name__ == '__main__':
    ip, port = get_argv()

    server = ServerSocket(ip, port)
    server.print_server_params()
    server.server_init()
#
# ip, port = get_argv()
# server = ServerSocket(ip, port)
# server.server_init()

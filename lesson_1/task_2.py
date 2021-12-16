"""

2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. Меняться должен только последний
октет каждого адреса. По результатам проверки должно выводиться соответствующее сообщение.
"""

import platform
from subprocess import Popen, PIPE
from ipaddress import ip_address


def host_ping(address):
    """
    функция для проверки доступности адреса
    :param address:
    :return:
    """

    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '1', address]
    ping_process = Popen(args, stdout=PIPE, stderr=PIPE)
    code = ping_process.wait()
    print(f'Узел "{address}" доступен\n') if code == 0 else print(f'Узел "{address}" недоступен\n')


def host_range_ping():
    while True:
        addr = input('Введите ip: ')
        try:
            ipv4_addr = ip_address(addr)
            break
        except Exception as err:
            print(f'Ошибка преобразования, невозможно преобразовать {addr} в ip адрес')

    last_octet = int(ipv4_addr.compressed.split('.')[-1])
    while True:
        try:
            hosts = int(input('Введите колличество хостов: '))
            if hosts <= 255 - last_octet:
                break
            else:
                print(f'Должно быть число, не больше {255 - last_octet}')
        except Exception:
            print(f'Должно быть число')

    for iter in range(hosts):
        #добавляем хост, переводим в строку и проверям на доступность
        host_ping((ipv4_addr+iter).compressed)





# address_list = ['ya.ru']
host_range_ping()

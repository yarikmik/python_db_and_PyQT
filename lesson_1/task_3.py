"""
3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, п
редставленным в табличном формате (использовать модуль tabulate).
"""

import platform
from subprocess import Popen, PIPE
from ipaddress import ip_address
from tabulate import tabulate


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
    # print(f'Узел "{address}" доступен\n') if code == 0 else print(f'Узел "{address}" недоступен\n')
    # return True if code == 0 else False

    if code == 0:
        dict_for_table.append({'Reachable': address})
    else:
        dict_for_table.append({'Unreachable': address})


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

    # добавляем хост, переводим в строку и проверям на доступность
    for i in range(hosts):
        address = (ipv4_addr + i).compressed
        host_ping(address)


dict_for_table = []
host_range_ping()
print(tabulate(dict_for_table, headers='keys', tablefmt="pipe"))

"""
Введите ip: 192.168.1.105
Введите колличество хостов: 10
| Reachable     | Unreachable   |
|:--------------|:--------------|
| 192.168.1.105 |               |
| 192.168.1.106 |               |
| 192.168.1.107 |               |
| 192.168.1.108 |               |
| 192.168.1.109 |               |
| 192.168.1.110 |               |
| 192.168.1.111 |               |
| 192.168.1.112 |               |
|               | 192.168.1.113 |
| 192.168.1.114 |               |
"""

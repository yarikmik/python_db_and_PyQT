"""
3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, п
редставленным в табличном формате (использовать модуль tabulate).
"""

import platform
from subprocess import Popen, PIPE, call
from ipaddress import ip_address
from tabulate import tabulate
import threading
import time
import chardet


def host_ping(address):
    """
    функция для проверки доступности адреса
    :param address:
    :return:
    """
    # global dict_for_table
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '1', address]
    with Popen(args, stdout=PIPE, stderr=PIPE) as ping_process:
        out = ping_process.stdout.read()
        coding = chardet.detect(out)
        result = out.decode(coding['encoding'])
        code = ping_process.wait()
    # time.sleep(1)
    # print(f'Узел "{address}" доступен\n') if code == 0 else print(f'Узел "{address}" недоступен\n')
    # return True if code == 0 else False

    if code == 0 and 'TTL' in result:
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

    hosts_list = [(ipv4_addr + i).compressed for i in range(hosts)]
    threads = []
    for ip in hosts_list:
        ping_tread = threading.Thread(target=host_ping, args=(ip,))
        # ping_tread.daemon = True
        ping_tread.start()
        threads.append(ping_tread)

    for thread in threads:
        thread.join()
    return


dict_for_table = list()

host_range_ping()
# time.sleep(5)
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

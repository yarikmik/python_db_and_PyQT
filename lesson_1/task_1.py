"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»).
При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""

import platform
from subprocess import Popen, PIPE


def host_ping(addr_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    for address in addr_list:
        args = ['ping', param, '2', address]
        ping_process = Popen(args, stdout=PIPE, stderr=PIPE)
        # print(ping_process)
        code = ping_process.wait()
        print(f'Узел "{address}" доступен\n') if code == 0 else print(f'Узел "{address}" недоступен\n')


addr_list = ['ya.ru', '8.8.8.8', '172.0.0.1', 'ussr.com', 'abirvalg.gt']
host_ping(addr_list)

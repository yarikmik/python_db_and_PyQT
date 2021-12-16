"""Unit-тесты утилит"""

import sys
import os, signal
import unittest
import platform
import subprocess
import time

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, \
    PRESENCE, ENCODING, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from client import ClientSocket


class TestClass(unittest.TestCase):
    client = ClientSocket(DEFAULT_IP_ADDRESS, DEFAULT_PORT)

    """setUpClass срабатывает один раз перед всеми тестами, setUp срабатывает перед каждым тестом
    setUpClass удобнее в моем случае, подключится к серверу достаточно один раз а не перед каждым тестом
    """

    @classmethod
    def setUpClass(cls):
        """стартуем сервер"""
        cls.process = subprocess.Popen([sys.executable, '../server.py'], shell=False)
        print('Старт сервера, процесс - ', cls.process.pid)

    @classmethod
    def tearDownClass(cls):
        """стопаем процес сервера"""
        # subprocess.Popen.kill(self.process)
        # os.kill(self.process.pid, signal.CTRL_BREAK_EVENT)
        # subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.process.pid))
        if platform.system() != 'Windows':
            os.killpg(os.getpgid(cls.process.pid), signal.SIGKILL)
            cls.process.wait()
        else:
            os.kill(cls.process.pid, signal.SIGTERM)
            cls.process.wait()

        print('Тест завершен. Стоп процесс сервера - ', cls.process.pid)
        # time.sleep(1)

    def test_send_assertTrue(self):
        """провал теста при значении False"""
        # print('Test1')
        self.assertTrue(isinstance(self.client.get_sent_message(), dict))

    def test_equal(self):
        '''провал теста при неравенстве элементов'''
        # print('Test2')
        self.assertEqual(self.client.get_answer_message(), '200 : OK')

    def test_not_eqal(self):
        """провал теста при равенстве элементов"""
        # print('Test3')
        self.assertNotEqual(self.client.get_answer_message(), '400 : Bad Request')


if __name__ == '__main__':
    unittest.main()

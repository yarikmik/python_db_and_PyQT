"""Unit-тесты клиента"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import create_message, server_ans


class TestClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_eqal(self):
        '''провал теста при неравенстве элементов'''
        self.assertEqual(server_ans({RESPONSE: 200}), '200 : OK')

    def test_not_eqal(self):
        """провал теста при равенстве элементов"""
        self.assertNotEqual(server_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '200 : OK')

    def test_almost_eqal(self):
        """assertAlmostEqual и assertNotAlmostEqual смысла тут не имеют, функция возвращает строку"""
        pass

    def test_raises(self):
        """провал теста в случае если функция не возвращает исключение"""
        self.assertRaises((ValueError, TypeError), server_ans, 0)

    def test_failIf(self):
        """провал теста если элемент расценивается как True"""
        self.failIf(not isinstance(server_ans({RESPONSE: 200}), str))  # изврат какой то получился))

    def test_fail(self):
        """Просто вызывает ошибку тестирования"""
        self.fail('Просто ошибка')


if __name__ == '__main__':
    unittest.main()

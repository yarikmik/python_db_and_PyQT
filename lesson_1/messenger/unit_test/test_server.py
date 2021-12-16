"""Unit-тесты сервера"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import process_client_message


class TestClass(unittest.TestCase):
    error = {RESPONSE: 400, ERROR: 'Bad Request'}
    ok = {RESPONSE: 200}

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equal(self):
        '''провал теста при неравенстве элементов'''
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok)

    def test_not_equal(self):
        """провал теста при равенстве элементов"""
        self.assertNotEqual(process_client_message({ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}}),
                            self.error)

    def test_almost_equal(self):
        """провал теста при не совпадении чисел до знака после запятой"""
        """даже показывает разницу AssertionError: 200.0 != 400.0 within 1 places (200.0 difference)"""
        msg_code = process_client_message({ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}})[RESPONSE]
        err_code = self.error[RESPONSE]
        self.assertAlmostEqual(float(msg_code), float(err_code), 1)

    def test_raises(self):
        """провал теста в случае если функция не возвращает исключение"""
        self.assertRaises(TypeError, process_client_message, 0)

    def test_failIf(self):
        """провал теста если элемент расценивается как True"""

        """тут пишет что устарел failIf: DeprecationWarning: Please use assertFalse instead."""
        self.failIf(isinstance(process_client_message({ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}}), str))

    # def test_fail(self):
    #     """Просто вызывает ошибку тестирования"""
    #     self.fail('Просто ошибка')

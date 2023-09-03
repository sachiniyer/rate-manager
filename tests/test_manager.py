import unittest
from src import Manager


class TestManager(unittest.TestCase):
    """
    Test manager class.

    Contains all the tests for the manager class.
    """
    def test_function1(self):
        manager = Manager({1: 1}, "log.txt")
        self.assertEqual(len(manager.rates), 1)

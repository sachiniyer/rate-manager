import unittest
from unittest.mock import patch
from src import Manager
import os


class TestManager(unittest.TestCase):
    """
    Test manager class.

    Contains all the tests for the manager class.
    """
    @classmethod
    def setUpClass():
        # delete all files in tests/logs/temp
        for file in os.listdir("tests/logs/temp"):
            os.remove("tests/logs/temp/" + file)

    def test_creation(self):
        manager = Manager({1: 1}, "tests/logs/temp/log_creation.txt")
        self.assertEqual(len(manager.rates), 1)

    def test_check(self):
        manager = Manager({100: 1}, "tests/logs/temp/log_check.txt")
        self.assertEqual(manager.check_time(), 0)
        self.assertNotEqual(manager.check_time(), 0)

    def test_multiple(self):
        manager = Manager({100: 3}, "tests/logs/temp/log_multiple.txt")
        self.assertEqual(manager.check_time(), 0, "First check")
        self.assertEqual(manager.check_time(), 0, "Second check")
        self.assertEqual(manager.check_time(), 0, "Third check")
        self.assertNotEqual(manager.check_time(), 0, "Fourth check")

    @patch('time.time')
    def test_replace(self, mock_time):
        mock_time.return_value = 10.0
        manager = Manager({100: 1}, "tests/logs/temp/log_replace.txt")
        self.assertEqual(manager.check_time(), 0, "First check")
        mock_time.return_value = 110.1
        self.assertEqual(manager.check_time(), 0, "Second check")

    @patch('time.time')
    def test_delay(self, mock_time):
        mock_time.return_value = 10.0
        manager = Manager({100: 2}, "tests/logs/temp/log_delay.txt")
        self.assertEqual(manager.check_time(), 0, "First check")
        mock_time.return_value = 11.1
        self.assertEqual(manager.check_time(), 0, "Second check")

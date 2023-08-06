"""
This file tests that the utility functions work as intended.
"""
import unittest

from util import is_ascii, strip_non_ascii


class TestUtility(unittest.TestCase):

    def testIsAscii(self):
        self.assertFalse(is_ascii('س'))  # Arabic 'x' or 's'
        self.assertTrue(is_ascii('x'))  # English 'x'
        self.assertFalse(is_ascii('χ'))  # Greek 'Chi'

    def testStripNonAscii(self):
        self.assertEqual(strip_non_ascii('hello'), "hello")
        self.assertEqual(strip_non_ascii('I am so happy! 😋 Hooray!'), 'I am so happy!  Hooray!')  # Emoji
        self.assertEqual(strip_non_ascii('hello also means مرحبا'), 'hello also means ')  # hello in arabic

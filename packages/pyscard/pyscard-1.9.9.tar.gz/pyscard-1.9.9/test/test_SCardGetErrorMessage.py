#! /usr/bin/env python
# -*- coding: utf-8 -*-

# to execute:
# $ cd test
# $ python -m unittest

import unittest
from smartcard.scard import SCardGetErrorMessage
from smartcard.scard import SCARD_S_SUCCESS, SCARD_F_INTERNAL_ERROR
from distutils.util import get_platform


class TestError(unittest.TestCase):

    def test_SCardGetErrorMessage(self):
        res = SCardGetErrorMessage(SCARD_S_SUCCESS)

        # do not test on Windows
        # the error messages are different and localized
        if get_platform() in ('win32', 'win-amd64'):
            return

        expected = "Command successful."
        self.assertEqual(res, expected)

        res = SCardGetErrorMessage(SCARD_F_INTERNAL_ERROR)
        expected = "Internal error."
        self.assertEqual(res, expected)

        res = SCardGetErrorMessage(1)
        expected = "Unknown error: 0x00000001"
        # macOS bug not yet fixed
        if get_platform().startswith('macosx-'):
            version = get_platform()  # something like 'macosx-10.14-x86_64'
            version = version.split('-')[1]  # '10.14'
            major, minor = map(int, version.split('.'))  # (10, 14)
            if major == 10 and minor < 13:
                expected = "Unkown error: 0x00000001"

        self.assertEqual(res, expected)


if __name__ == '__main__':
    unittest.main()

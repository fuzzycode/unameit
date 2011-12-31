# -*- coding: utf-8 -*-

# Copyright (C) 2011  Björn Larsson, develop@bjornlarsson.net
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import sys
from unameit.options import Options


class TestOptions(unittest.TestCase):
    def setUp(self):
        self.options = Options()

    def tearDown(self):
        self.options.clear()

    def test_item(self):
        """It should be possible to access items in the options instance"""
        option = Options(foo="bar", test=42)

        self.assertEqual(option["foo"], "bar")
        self.assertEqual(option["test"], 42)

    def test_invalid_item(self):
        """Options should raise KeyError if accessing an invalid item"""
        option = Options(foo="bar", test=42)

        self.assertRaises(KeyError, option.__getitem__, "laba")

    def test_borg(self):
        """All options instances should share state"""
        option = Options(foo="bar", test=42)
        option2 = Options()

        self.assertEqual(option["test"], option2["test"])

    def test_length(self):
        """It should be possible to get the length of a group"""
        option = Options(foo="bar", test=42)

        self.assertEqual(len(option), 2)

    def test_iteration(self):
        """It should be possible to iterate over the group"""
        option = Options(foo="bar", test=42)

        for _ in option:
            pass


#Run all tests
if __name__ == "__main__":
    sys.exit(unittest.main())

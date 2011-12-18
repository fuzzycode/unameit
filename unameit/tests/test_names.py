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
from unameit import names


class TestCleanName(unittest.TestCase):
    def test_dot_under(self):
        """All dots and underscores should be removed from the name"""

        self.assertEqual(names.clean_name('How.I.Met.Your.Mother'),
            'How I Met Your Mother')
        self.assertEqual(names.clean_name('How_I_Met_Your_Mother'),
            'How I Met Your Mother')
        self.assertEqual(names.clean_name('How.I.Met.Your.Mother_'),
            'How I Met Your Mother')
        self.assertEqual(names.clean_name('How.I.Met.Your.Mother.'),
            'How I Met Your Mother')
        self.assertEqual(names.clean_name('_How.I.Met.Your.Mother'),
            'How I Met Your Mother')
        self.assertEqual(names.clean_name('.How.I.Met.Your.Mother_'),
            'How I Met Your Mother')
        self.assertEqual(names.clean_name('How_I.Met_Your.Mother'),
            'How I Met Your Mother')

    def test_decimal_numbers(self):
        """Dots in decimal numbers should not be removed"""
        self.assertEqual(names.clean_name('foo.bar.1.2'), 'foo bar 1.2')
        self.assertEqual(names.clean_name('foo_bar_1.2'), 'foo bar 1.2')


class TestCapitalize(unittest.TestCase):
    def test_capitalize(self):
        """Letters should be properly capitalized"""
        self.assertEqual(names.capitalize("they're bill's friends"),
            "They're Bill's Friends")

        self.assertEqual(names.capitalize("hello world. My name is"),
            "Hello World. My Name Is")

        self.assertEqual(names.capitalize("Hello"), "Hello")

    def test_all_capitals(self):
        """Words in all uppercase should not be changed"""

        self.assertEqual(names.capitalize("Born in the USA"),
            "Born In The USA")
        self.assertEqual(names.capitalize("USA-EU cooperation is OK"),
            "USA-EU Cooperation Is OK")


if __name__ == "__main__":
    sys.exit(unittest.main())

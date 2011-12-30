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
import unameit

class TestPackage(unittest.TestCase):
    def test_version_format(self):
        """The package version string should be properly formatted"""
        import re

        format = r'^\d{1,2}\.\d{1,2}(?:\.\d{1,2})?$'

        m = re.match(format, unameit.version())
        self.assertNotEqual(m, None)

#Run all tests
if __name__ == "__main__":
    sys.exit(unittest.main())

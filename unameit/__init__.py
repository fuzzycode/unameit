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

"""
A flexible and easy to use tool for renaming media files.
"""

from __future__ import absolute_import, print_function, unicode_literals

import logging

try:
    from logging import NullHandler
except ImportError:
    from unameit.backport import NullHandler

__NAME__ = "unameit"
__AUTHOR__ = "Björn Larsson"
__EMAIL__ = "develop@bjornlarsson.net"
__VERSION__ = (0, 1, 0)


def version():
    """Returns the version as a string"""
    return '.'.join([str(d) for d in __VERSION__])

# Make sure that we have a null handler on the base logger for the package
logging.getLogger(__name__).addHandler(NullHandler())

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
Module managing file names and file names related functions.
"""

import re
import logging

logger = logging.getLogger( __name__ )

def clean_name( name ):
    """
    :param name: The name to be cleaned
    :return: string.

    Removes . and _ between words in the file names, but leaves dots intact
    within decimal numbers.
    """

    new_name, num_subs = re.subn( r'(?<!\d)[\._]|[\._]$|^[\._]', ' ', name )
    if num_subs:
        logger.debug("Changed string {0} => {1}".format(name, new_name))
    return new_name.strip()

def capitalize( s ):
    """
    A modified version of the solution found in the Python
    `documentation
    <http://docs.python.org/library/stdtypes.html#string-methods>`_

    Words in all UPPERCASE are left unchanged.

    :param s: The string to be capitalized
    :return: The capitalized string
    """

    def cb(mo):
        group = mo.group(0)

        if group.isupper():
            return group
        else:
            return group[0].upper() + group[1:].lower()

    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", cb, s)


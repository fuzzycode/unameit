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
A utility module wrapping up those odd bits and pieces that don't fit
elsewhere and should not be exposed in the public interface of the package.
"""


class Borg(object):
    """
    The Borg implementation suggested at:
    http://code.activestate.com/recipes/66531/#c20
    """
    _state = {}

    def __new__(cls, *p, **kwargs):
        self = object.__new__(cls, *p, **kwargs)
        self.__dict__ = cls._state
        return self

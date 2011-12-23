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
A module for managing the command line options passed by the user.
"""

import logging
import collections

from unameit.utils import Borg

logger = logging.getLogger(__name__)

class Options(collections.Mapping, Borg):
    """
    A dictionary like object for storing command-line options using the Borg
    pattern to share state across instances.
    """

    def __init__(self, **kwargs):
        super(Options, self).__init__()
        if not hasattr(self, "_data"):
            logger.debug("No data found, creating new")
            self._data = dict(kwargs)
        else:
            logger.debug("Extending existing data")
            self._data.update(kwargs)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, item):
        return self._data[item]

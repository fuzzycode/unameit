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
A module for reading and managing configuration files for **unameit**.
Provides functionality to read and merge the config files and to validate the
 correctness of the configurations.
"""

import logging
import os
import yaml

__all__ = ['Group', 'read', 'validate', 'ConfigError']

logger = logging.getLogger(__name__)

class ConfigError(Exception):
    """Raised if there were errors reading a configuration file"""
    pass


class Group(object):
    """
    Holds data for a configuration group
    """

    def __init__(self, name, data):
        self._name = name
        self._data = data

    def __getattr__(self, item):
        try:
            return self._data[item]
        except KeyError:
            raise AttributeError("Group has no attribute {0}".format(item))

    def __repr__(self):
        return "<Group {0}>".format(self._name)


def read(files):
    """
    :param files: A path or an iterable of paths to read
    :return: A list of :class:`Group` objects. Could be empty

    Takes a string or a list/tuple of strings to be file paths.

    Files are precessed in the order provided and later values will overwrite
    previous values.

    Files that are not found will be ignored so it is possible to provide a
    list of default locations to look in and any files not found are
    automatically ignored.

    The function returns a list of :class:`Group` objects. The default
    section of a file will not be included in the result. If selected in the
    config file, the group will be merged with the default section before
    returning.
    """

    #Make sure that we have an iterable containing at least 1 file
    if not hasattr(files, "__iter__"):
        files = [files]

    logger.debug("Processing {0} files".format(len(files)))

    #Parse all files in the order provided and merge into 1 dict holding the
    #merged content
    file_data = dict()
    for path in files:
        if not os.path.isabs(path):
            _old = path
            path = os.path.abspath(os.path.join(os.getcwd(), path))
            logger.debug("Making {0} absolute => {1}".format(_old, path))

        path = os.path.normpath(path)

        if os.path.isfile(path):
            data = _read_file(path)
            file_data = _merge(file_data, data)
        else:
            logger.info("{0} not found. Was ignored.".format(path))

    #process all groups and merge with default data if required
    default = file_data.get("default", dict())
    #filter out the default section
    data = dict((k, v) for k, v in file_data.items() if k != "default")

    groups = list()
    for name, data in data.items():
        merge = data.get("use_defaults", False)

        if merge:
            groups.append(Group(name, _merge(data, default)))
        else:
            groups.append(Group(name, data))

    return groups


def validate(required, data):
    pass


def _read_file(path):
    """
    :param path: The absolute path to the file to load
    :return: A dictionary
    :raise: :class:`ConfigError`

    Reads a YAML formatted file and returns the data as a dictionary.

    Raises :class:`ConfigError` if the file is not found or if it containes
    formatting errors.
    """
    assert os.path.isabs(path), "Path should be absolute"

    try:
        with open(path, "rt") as config:
            data = yaml.safe_load(config)
    except IOError:
        logger.error("Unable to read {0}".format(path))
        raise ConfigError("Unable to read {0}".format(path))
    except yaml.YAMLError as e:
        if hasattr(e, "problem_mark"):
            line = e.problem_mark.line + 1
            column = e.problem_mark.column + 1
            logger.error("Problem found in {0} at ({1} : {2})".
            format(path, line, column))
        else:
            logger.error("Error found while parsing {0}".format(path))

        raise ConfigError("Error parsing {0}".format(path))

    return data


def _merge(left, right):
    """
    :param left: Left hand side
    :param right: Right hand side
    :return:

    Merges the left and right argument. Dictionaries are merged recursively,
    lists are extended and made unique.

    .. Note: In case of a conflict, values in *right* will overwrite values
    in *left*.
    """

    if isinstance(left, dict) and isinstance(right, dict):
        for key, value in list(left.items()):
            if key not in right:
                right[key] = value
            else:
                right[key] = _merge(value, right[key])
    elif isinstance(left, list) and isinstance(right, list):
        right.extend(left)
        right = list(set(right))

    return right




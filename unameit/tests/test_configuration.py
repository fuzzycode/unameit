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

from __future__ import with_statement

import unittest
import sys
import os

from unameit.configuration import _merge, _read_file, read, ConfigError


class WorkingDir(object):
    def __init__(self, dir):
        self._dir = dir
        self._old = os.getcwd()
        os.chdir(self._dir)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        os.chdir(self._old)


class TestMerge(unittest.TestCase):
    """Tests the merging of two dictionaries"""

    def test_merge(self):
        """It should be possible to merge 2 dicts"""
        d1 = {"a": 10, "b": 20}
        d2 = {"b": 30, "c": 40}

        merged = _merge(d1, d2)
        self.assertEqual(merged, {"a": 10, "b": 30, "c": 40})

    def test_dicts(self):
        """It should be possible to merge nested dict"""
        d1 = {"a": {"b": 10, "c": 20}}
        d2 = {"a": {"d": 30, "e": "foo"}}

        result = _merge(d1, d2)
        self.assertEqual(result, {"a": {"b": 10, "c": 20, "d": 30,
                                        "e": "foo"}})

    def test_lists(self):
        """it should be possible to merge lists"""
        l1 = [10, 4.5, 11]
        l2 = [7, 14, 21]
        l3 = ["hello", "world"]
        l4 = ["foo", "bar"]

        result = sorted(_merge(l1, l2))
        self.assertEqual(result, [4.5, 7, 10, 11, 14, 21])

        result = sorted(_merge(l3, l4))
        self.assertEqual(result, ["bar", "foo", "hello", "world"])

    def test_nested_lists(self):
        """It should be possible to merge nested lists"""
        d1 = {"a": [10, 20]}
        d2 = {"a": [30, 40]}

        result = _merge(d1, d2)
        result["a"] = sorted(result["a"])

        self.assertEqual(result, {"a": [10, 20, 30, 40]})

    def test_unique_list(self):
        """Dupes should be removed from merged lists"""
        l1 = [20, 12, 70]
        l2 = [4, 9, 20]

        result = _merge(l1, l2)
        self.assertEqual(sorted(result), [4, 9, 12, 20, 70])

    def test_values(self):
        """It should be possible to merge 2 values"""
        self.assertEqual(_merge(2, 5), 5)
        self.assertEqual(_merge("hello", "world"), "world")


class TestReadFile(unittest.TestCase):
    """test the reading of a single file"""

    def setUp(self):
        super(TestReadFile, self).setUp()
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.data_path = os.path.join(self.path, "data")

    def test_reading(self):
        """It should be possible to read a config file"""
        config = os.path.join(self.data_path, "first_conf.cfg")
        data = _read_file(config)

        self.assertEqual(data["default"], {"language": "en"})

    def test_yaml_error(self):
        """
        Function should raise ConfigError if reading an invalid config file
        """
        config = os.path.join(self.data_path, "invalid.cfg")
        self.assertRaises(ConfigError, _read_file, config)

    def test_read_error(self):
        """
        Function should raise ConfigError if the file could not be opened
        """
        config = os.path.join(self.data_path, "first_config.cfg")
        self.assertRaises(ConfigError, _read_file, config)

    def test_non_absolute_path(self):
        """Function should raise an error if path is not absolute"""
        self.assertRaises(AssertionError, _read_file, "first_conf.cfg")


class TestReadFiles(unittest.TestCase):
    """Tests the reading of multiple files"""

    def setUp(self):
        super(TestReadFiles, self).setUp()
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.data_path = os.path.join(self.path, "data")

    def test_single_file(self):
        """
        It should be possible to load a single file by providing the path as
        a string.
        """
        config = os.path.join(self.data_path, "first_conf.cfg")
        data = read(config)

        self.assertEqual(len(data), 1)

    def test_multiple_files(self):
        """
        It should be possible to load several files by providing a iterable
        containing the paths.
        """

        config1 = os.path.join(self.data_path, "first_conf.cfg")
        config2 = os.path.join(self.data_path, "second_conf.cfg")
        data = read([config1, config2])

        self.assertEqual(len(data), 2)

    def test_invalid_files(self):
        """Files that could not be found should be ignored when reading"""
        config = os.path.join(self.data_path, "first_conf.cfg")
        data = read([config, os.path.expanduser("~/conf.cfg")])

        self.assertEqual(len(data), 1)

    def test_relative_path(self):
        """It should be possible to load files with a relative path"""
        with WorkingDir(self.path):
            data = read("./data/first_conf.cfg")
            self.assertEqual(len(data), 1)


class TestGroup(unittest.TestCase):
    def setUp(self):
        super(TestGroup, self).setUp()
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.data_path = os.path.join(self.path, "data")

    def test_attribute(self):
        """It should be able to access the attributes of the group"""
        config = os.path.join(self.data_path, "first_conf.cfg")
        data = read(config)
        group = data[0]

        self.assertEqual(group.input, "/etc/")
        self.assertEqual(group.language, "en")

    def test_invalid_attribute(self):
        """
        The group should raise AttributeError when accessing invalid
        attributes
        """
        config = os.path.join(self.data_path, "first_conf.cfg")
        data = read(config)
        group = data[0]

        self.assertRaises(AttributeError, group.__getattr__, "foo")
        self.assertRaises(AttributeError, group.__getattr__, "bar")

    def test_representation(self):
        """The group representation should be properly formatted"""


#Run all tests
if __name__ == "__main__":
    sys.exit(unittest.main())

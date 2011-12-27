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
Manages the generation of option parser instances.
"""

from __future__ import with_statement
import logging
import optparse
import os
import tempfile

from unameit import __NAME__, version

logger = logging.getLogger(__name__)  # pylint: disable=C0103


class ParserGroup(object):
    """
    A context handler for parser groups to enable nice and compact with
    syntax for the parser groups.

    Idea taken from
    https://github.com/dbr/tvnamer/blob/master/tvnamer/cliarg_parser.py
    """

    def __init__(self, parser, name):
        self.name = name
        self.parser = parser
        self.group = optparse.OptionGroup(self.parser, self.name)

        logger.debug("Generating group ({0})".format(name))

    def __enter__(self):
        return self.group

    def __exit__(self, *args, **kwargs):
        self.parser.add_option_group(self.group)


def get_parser():
    """
    Creates and returns a new option parser object to be used for parsing the
    command line argument passed.

    :return: A new parser object
    """
    parser = optparse.OptionParser(usage="%prog [options]", version=version())

    with ParserGroup(parser, "Logging") as group:
        tmp_dir = tempfile.gettempdir()
        group.add_option('-f', '--log-file', metavar="FILE", action="store",
            dest="log_file", help="The logfile to use",
            default=os.path.join(tmp_dir, "{0}.log".format(__NAME__)))

        group.add_option('-o', '--std-out', action="store_true",
            dest='use_stdout', default=False,
            help="If set, also log to stdout.")

        group.add_option('-v', action="store_const", dest="level",
            const=logging.DEBUG, default=logging.INFO,
            help="Print extra information. Useful for debugging.")

        group.add_option('-q', action="store_const", dest="level",
            const=logging.WARNING, default=logging.INFO,
            help="Print less information")

    with ParserGroup(parser, "Config") as group:
        group.add_option("-C", "--config", action="append", dest="configs",
            metavar="FILE", default=[],
            help="Add a config file to use. Can be specified multiple times "\
                 "to add more files. Can be an absolute or relative path.")

    return parser

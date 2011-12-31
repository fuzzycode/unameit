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
Main entry point for the package.
"""

import logging
import sys
from unameit.options import Options

from unameit.parser import get_parser


def main():
    """
    Main entry point for the application
    """

    parser = get_parser()
    options, _ = parser.parse_args()

    #configure the logger
    logging.basicConfig(
        level=options.level,
        format='%(asctime)s : %(levelname)-8s : %(message)s',
        datefmt='%m-%d %H:%M:%S',
        filename=options.log_file,
        filemode='wt')

    #If requested, add stdout logging
    if options.use_stdout:
        stream = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter("%(levelname)s : %(message)s")
        stream.setFormatter(formatter)
        stream.setLevel(options.level)
        logging.root.addHandler(stream)

    #Initialize the Borg structure with the options data
    Options(**options.__dict__)

    return 0

if __name__ == "__main__":
    sys.exit(main())

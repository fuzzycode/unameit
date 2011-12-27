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

try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup

    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages

from unameit.__init__ import __NAME__, __AUTHOR__, __EMAIL__, version

def get_description():
    try:
        return open("README.rst").read() + '\n' + open("CHANGES.txt").read()
    except Exception:
        return "No description"

setup(
    name=__NAME__,
    author=__AUTHOR__,
    version=version(),
    author_email=__EMAIL__,
    license="GPLv3",
    platforms=["any"],
    install_requires=["pytvdbapi, pyaml"],
    packages=find_packages(),
    test_suite='unameit.tests',
    description="A flexible and easy to use tool for renaming media files.",
    long_description=get_description()

)
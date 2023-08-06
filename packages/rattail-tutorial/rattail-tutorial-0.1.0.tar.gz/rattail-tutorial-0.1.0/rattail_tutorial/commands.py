# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2019 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Rattail Tutorial commands
"""

import sys

from rattail import commands

from rattail_tutorial import __version__


def main(*args):
    """
    Main entry point for Rattail Tutorial command system
    """
    args = list(args or sys.argv[1:])
    cmd = Command()
    cmd.run(*args)


class Command(commands.Command):
    """
    Main command for Rattail Tutorial
    """
    name = 'rattail_tutorial'
    version = __version__
    description = "Rattail Tutorial (custom Rattail system)"
    long_description = ''


class HelloWorld(commands.Subcommand):
    """
    The requisite 'hello world' example
    """
    name = 'hello'
    description = __doc__.strip()

    def run(self, args):
        self.stdout.write("hello world!\n")

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
Custom config
"""

from rattail.config import ConfigExtension


class Rattail_tutorialConfig(ConfigExtension):
    """
    Rattail config extension for Rattail Tutorial
    """
    key = 'rattail_tutorial'

    def configure(self, config):

        # set some default config values
        config.setdefault('rattail.mail', 'emails', 'rattail_tutorial.emails')
        config.setdefault('tailbone', 'menus', 'rattail_tutorial.web.menus')

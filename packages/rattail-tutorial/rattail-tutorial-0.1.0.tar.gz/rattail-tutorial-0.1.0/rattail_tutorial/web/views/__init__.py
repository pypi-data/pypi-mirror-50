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
Views
"""


def includeme(config):

    # core views
    config.include('rattail_tutorial.web.views.common')
    config.include('tailbone.views.auth')
    config.include('tailbone.views.tables')
    config.include('tailbone.views.upgrades')
    config.include('tailbone.views.progress')

    # main table views
    config.include('tailbone.views.brands')
    config.include('tailbone.views.customers')
    config.include('tailbone.views.customergroups')
    config.include('tailbone.views.datasync')
    config.include('tailbone.views.departments')
    config.include('tailbone.views.email')
    config.include('tailbone.views.employees')
    config.include('tailbone.views.messages')
    config.include('tailbone.views.people')
    config.include('tailbone.views.products')
    config.include('tailbone.views.reportcodes')
    config.include('tailbone.views.roles')
    config.include('tailbone.views.settings')
    config.include('tailbone.views.shifts')
    config.include('tailbone.views.stores')
    config.include('tailbone.views.subdepartments')
    config.include('tailbone.views.users')
    config.include('tailbone.views.vendors')

    # batch views
    config.include('tailbone.views.handheld')
    config.include('tailbone.views.inventory')

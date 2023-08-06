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
Web Menus
"""


def simple_menus(request):
    url = request.route_url

    menus = [
        {
            'title': "Products",
            'type': 'menu',
            'items': [
                {
                    'title': "Products",
                    'url': url('products'),
                    'perm': 'products.list',
                },
                {
                    'title': "Brands",
                    'url': url('brands'),
                    'perm': 'brands.list',
                },
                {
                    'title': "Report Codes",
                    'url': url('reportcodes'),
                    'perm': 'reportcodes.list',
                },
            ],
        },
        {
            'title': "Vendors",
            'type': 'menu',
            'items': [
                {
                    'title': "Vendors",
                    'url': url('vendors'),
                    'perm': 'vendors.list',
                },
                {'type': 'sep'},
                {
                    'title': "Catalogs",
                    'url': url('vendorcatalogs'),
                    'perm': 'vendorcatalogs.list',
                },
                {
                    'title': "Upload New Catalog",
                    'url': url('vendorcatalogs.create'),
                    'perm': 'vendorcatalogs.create',
                },
            ],
        },
        {
            'title': "Company",
            'type': 'menu',
            'items': [
                {
                    'title': "Stores",
                    'url': url('stores'),
                    'perm': 'stores.list',
                },
                {
                    'title': "Departments",
                    'url': url('departments'),
                    'perm': 'departments.list',
                },
                {
                    'title': "Subdepartments",
                    'url': url('subdepartments'),
                    'perm': 'subdepartments.list',
                },
                {'type': 'sep'},
                {
                    'title': "Employees",
                    'url': url('employees'),
                    'perm': 'employees.list',
                },
                {'type': 'sep'},
                {
                    'title': "Customers",
                    'url': url('customers'),
                    'perm': 'customers.list',
                },
                {
                    'title': "Customer Groups",
                    'url': url('customergroups'),
                    'perm': 'customergroups.list',
                },
            ],
        },
        {
            'title': "Batches",
            'type': 'menu',
            'items': [
                {
                    'title': "Handheld",
                    'url': url('batch.handheld'),
                    'perm': 'batch.handheld.list',
                },
                {
                    'title': "Inventory",
                    'url': url('batch.inventory'),
                    'perm': 'batch.inventory.list',
                },
            ],
        },
        {
            'title': "Admin",
            'type': 'menu',
            'items': [
                {
                    'title': "Users",
                    'url': url('users'),
                    'perm': 'users.list',
                },
                {
                    'title': "User Events",
                    'url': url('userevents'),
                    'perm': 'userevents.list',
                },
                {
                    'title': "Roles",
                    'url': url('roles'),
                    'perm': 'roles.list',
                },
                {'type': 'sep'},
                {
                    'title': "App Settings",
                    'url': url('appsettings'),
                    'perm': 'settings.list',
                },
                {
                    'title': "Email Settings",
                    'url': url('emailprofiles'),
                    'perm': 'emailprofiles.list',
                },
                {
                    'title': "Email Attempts",
                    'url': url('email_attempts'),
                    'perm': 'email_attempts.list',
                },
                {
                    'title': "Raw Settings",
                    'url': url('settings'),
                    'perm': 'settings.list',
                },
                {'type': 'sep'},
                {
                    'title': "DataSync Changes",
                    'url': url('datasyncchanges'),
                    'perm': 'datasync.list',
                },
                {
                    'title': "Tables",
                    'url': url('tables'),
                    'perm': 'tables.list',
                },
                {
                    'title': "Rattail Tutorial Upgrades",
                    'url': url('upgrades'),
                    'perm': 'upgrades.list',
                },
            ],
        },
    ]

    return menus

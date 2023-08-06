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
Rattail core data model extensions
"""

import sqlalchemy as sa
from sqlalchemy import orm

from rattail.db import model
from rattail.db.core import uuid_column


class Rattail_tutorialCustomer(model.Base):
    """
    Rattail Tutorial extensions to core Customer model
    """
    __tablename__ = 'rattail_tutorial_customer'
    __table_args__ = (
        sa.ForeignKeyConstraint(['uuid'], ['customer.uuid'], name='rattail_tutorial_customer_fk_customer'),
    )

    uuid = uuid_column(default=None)

    customer = orm.relationship(
        model.Customer,
        doc="""
        Customer to which this extension record pertains.
        """,
        backref=orm.backref(
            '_rattail_tutorial',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Rattail Tutorial-specific extension record for the customer.
            """),
    )

    mail_list_synced = sa.Column(sa.Boolean(), nullable=False, default=False, doc="""
    Flag indicating whether the customer's email address has been synced to the
    general mailing list.
    """)

#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2019 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Schema Elements for Entity Prototypes
-------------------------------------
"""

from tendril.schema.base import NakedSchemaObject
from tendril.schema.helpers import SchemaObjectList

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class LabelDeclaration(NakedSchemaObject):
    def elements(self):
        e = super(LabelDeclaration, self).elements()
        e.update({
            'desc': self._p(('desc',), required=True),
            'type': self._p(('type',), required=True),
        })
        return e

    def __repr__(self):
        return "<LabelDeclaration {0}, {1}>" \
               "".format(self.desc, self.type)


class LabelListing(SchemaObjectList):
    _objtype = LabelDeclaration


def load(manager):
    pass

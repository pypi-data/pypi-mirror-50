#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2017 Chintalagiri Shashank
#
# This file is part of tendril-connector-tally.
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
Docstring for stock
"""

from lxml import etree
from warnings import warn

from . import TallyReport
from . import TallyRequestHeader
from . import TallyNotAvailable
from . import TallyElement
from . import yesorno


class TallyStockGroup(TallyElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'narration': ('narration', str, True),
        'costingmethod': ('costingmethod', str, True),
        'valuationmethod': ('valuationmethod', str, True),
        '_baseunits': ('baseunits', str, True),
        '_additionalunits': ('additionalunits', str, True),
        'isbatchwiseon': ('isbatchwiseon', yesorno, True),
        'isperishableon': ('isperishableon', yesorno, True),
        'isaddable': ('isaddable', yesorno, True),
        'ignorephysicaldifference': ('ignorephysicaldifference', yesorno, True),
        'ignorenegativestock': ('ignorenegativestock', yesorno, True),
        'treatsalesasmanufactured': ('treatsalesasmanufactured', yesorno, True),
        'treatpurchasesasconsumed': ('treatpurchasesasconsumed', yesorno, True),
        'treatrejectsasscrap': ('treatrejectsasscrap', yesorno, True),
        'hasmfgdate': ('hasmfgdate', yesorno, True),
        'allowuseofexpireditems': ('allowuseofexpireditems', yesorno, True),
        'ignorebatches': ('ignorebatches', yesorno, True),
        'ignoregodowns': ('ignoregodowns', yesorno, True),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self._ctx.stockgroups[self._parent]

    @property
    def path(self):
        if self.parent and self.parent.path:
            return self.parent.path + [self.name]
        else:
            return [self.name]

    @property
    def baseunits(self):
        if self._baseunits:
            try:
                return self._ctx.units[self._baseunits]
            except KeyError:
                return None

    @property
    def additionalunits(self):
        if self._additionalunits:
            return self._ctx.units[self._additionalunits]

    def __repr__(self):
        return "<TallyStockGroup {0}>".format(self.name)


class TallyStockCategory(TallyElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'narration': ('narration', str, True),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self._ctx.stockcategories[self._parent]

    def __repr__(self):
        return "<TallyStockCategory {0}>".format(self.name)


class TallyStockItem(TallyElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'narration': ('narration', str, True),
        '_category': ('category', str, False),
        'taxclassificationname': ('taxclassificationname', str, False),
        'ledgername': ('ledgername', str, False),
        '_costingmethod': ('costingmethod', str, True),
        '_valuationmethod': ('valuationmethod', str, True),
        '_baseunits': ('baseunits', str, True),
        '_additionalunits': ('additionalunits', str, True),
        'description': ('description', str, True),
        'natureofitem': ('natureofitem', str, True),
        'isbatchwiseon': ('isbatchwiseon', yesorno, True),  # TODO Inherit
        'isperishableon': ('isperishableon', yesorno, True),  # TODO Inherit
        'iscostcentreson': ('iscostcentreson', yesorno, False),
        'isentrytaxapplicable': ('isentrytaxapplicable', yesorno, False),
        'iscosttrackingon': ('iscosttrackingon', yesorno, False),
        'ignorephysicaldifference': ('ignorephysicaldifference', yesorno, True),  # TODO Inherit
        'ignorenegativestock': ('ignorenegativestock', yesorno, True),  # TODO Inherit
        'treatsalesasmanufactured': ('treatsalesasmanufactured', yesorno, True),  # TODO Inherit
        'treatpurchasesasconsumed': ('treatpurchasesasconsumed', yesorno, True),  # TODO Inherit
        'treatrejectsasscrap': ('treatrejectsasscrap', yesorno, True),  # TODO Inherit
        'hasmfgdate': ('hasmfgdate', yesorno, True),  # TODO Inherit
        'allowuseofexpireditems': ('allowuseofexpireditems', yesorno, True),  # TODO Inherit
        'ignorebatches': ('ignorebatches', yesorno, True),  # TODO Inherit
        'ignoregodowns': ('ignoregodowns', yesorno, True),  # TODO Inherit
        'calconmrp': ('calconmrp', yesorno, False),  # TODO Inherit
        'excludejrnlforvaluation': ('excludejrnlforvaluation', yesorno, True),  # TODO Inherit
        '_openingbalance': ('openingbalance', str, True),
        '_openingvalue': ('openingvalue', str, True),
        '_openingrate': ('openingrate', str, True),
        '_godownname': ('godownname', str, False),
        'batchname': ('batchname', str, False),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            try:
                return self._ctx.stockgroups[self._parent]
            except KeyError:
                print(self.name)
                print(self._parent)
                print(self._ctx.stockgroups.keys())
                raise

    @property
    def catgory(self):
        if self._parent and self._parent != self.name:
            return self._ctx.stockcategories[self._parent]

    @property
    def baseunits(self):
        if self._baseunits:
            try:
                return self._ctx.units[self._baseunits]
            except KeyError:
                return None

    @property
    def additionalunits(self):
        if self._additionalunits:
            return self._ctx.units[self._additionalunits]

    @property
    def costingmethod(self):
        if self._costingmethod:
            return self._costingmethod
        if self.parent:
            return self.parent.costingmethod

    @property
    def valuationmethod(self):
        if self._valuationmethod:
            return self._valuationmethod
        if self.parent:
            return self.parent.valuationmethod

    @property
    def openingbalance(self):
        raise NotImplementedError

    @property
    def openingrate(self):
        raise NotImplementedError

    @property
    def openingvalue(self):
        raise NotImplementedError

    @property
    def godowns(self):
        if self._godownname:
            if ':' in self._godownname:
                names = set(self._godownname.split(':'))
            else:
                names = [self._godownname]
            return [self._ctx.godowns[x] for x in names]
        else:
            return []

    @property
    def path(self):
        if self.parent and self.parent.path:
            return self.parent.path + [self.name]
        else:
            return [self.name]

    def __repr__(self):
        return "<TallyStockItem {0}>".format(self.name)


class TallyGodown(TallyElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'narration': ('narration', str, True),
        'hasnospace': ('hasnospace', yesorno, False),
        'hasnostock': ('hasnostock', yesorno, False),
        'isexternal': ('isexternal', yesorno, False),
        'isinternal': ('isinternal', yesorno, False),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self._ctx.godowns[self._parent]

    def __repr__(self):
        return "<TallyGodown {0}>".format(self.name)


class TallyVoucherType(TallyElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        'mailingname': ('mailingname', str, True),
        'numberingmethod': ('numberingmethod', str, True),
        'isdeemedpositive': ('isdeemedpositive', yesorno, False),
        'affectsstock': ('affectsstock', yesorno, False),
        'preventduplicates': ('preventduplicates', yesorno, False),
        'prefillzero': ('prefillzero', yesorno, False),
        'printaftersave': ('printaftersave', yesorno, False),
        'formalreceipt': ('formalreceipt', yesorno, False),
        'isoptional': ('isoptional', yesorno, False),
        'asmfgjrnl': ('asmfgjrnl', yesorno, False),
        'effectivedate': ('effectivedate', yesorno, False),
        'commonnarration': ('commonnarration', yesorno, False),
        'multinarration': ('multinarration', yesorno, False),
        'istaxinvoice': ('istaxinvoice', yesorno, False),
        'useforposinvoice': ('useforposinvoice', yesorno, False),
        'useforexcisetraderinvoice': ('useforexcisetraderinvoice', yesorno, False),  # noqa
        'useforexcise': ('useforexcise', yesorno, False),
        'useforjobwork': ('useforjobwork', yesorno, False),
        'isforjobworkin': ('isforjobworkin', yesorno, False),
        'allowconsumption': ('allowconsumption', yesorno, False),
    }

    @property
    def parent(self):
        if self._parent and self._parent != self.name:
            return self._ctx.vouchertypes[self._parent]


class TallyUnit(TallyElement):
    elements = {
        'name': ('name', str, True),
        'originalname': ('originalname', str, False),
        'decimalplaces': ('decimalplaces', int, True),
        'issimpleunit': ('issimpleunit', yesorno, True),
        'additionalunits': ('additionalunits', str, False),
        'conversion': ('conversion', float, False)
    }

    def __repr__(self):
        return "<TallyUnit {0}>".format(self.name)


class TallyStockMaster(TallyReport):
    _cachename = 'TallyStockMaster'

    def _build_request_body(self):
        r = etree.Element('EXPORTDATA')
        rd = etree.SubElement(r, 'REQUESTDESC')
        rn = etree.SubElement(rd, 'REPORTNAME')
        rn.text = 'List of Accounts'
        sv = etree.SubElement(rd, 'STATICVARIABLES')
        self._set_request_staticvariables(sv)
        at = etree.SubElement(sv, 'ACCOUNTTYPE')
        at.text = 'All Inventory Masters'
        return etree.ElementTree(r)

    _content = {
        'stockitems': ('stockitem', TallyStockItem),
        'stockgroups': ('stockgroup', TallyStockGroup),
        'stockcategories': ('stockcatogory', TallyStockCategory),
        'godowns': ('godown', TallyGodown),
        'vouchertypes': ('vouchertype', TallyVoucherType),
        'units': ('unit', TallyUnit)
    }


class TallyStockItemPosition(TallyElement):
    elements = {
        'name': ('name', str, True),
        '_parent': ('parent', str, True),
        '_baseunits': ('baseunits', str, True),
        'closingbalance': ('closingbalance', str, True),
        'closingvalue': ('closingvalue', str, True),
        'closingrate': ('closingrate', str, True),
    }

    @property
    def parent(self):
        try:
            return get_master(self._ctx.company_name).stockgroups[self._parent]
        except KeyError:
            warn("Could not find Parent {0} for {1}"
                 "".format(self._parent, self.name))
            return self._parent

    @property
    def baseunits(self):
        if getattr(self, '_baseunits', None):
            try:
                return get_master(self._ctx.company_name).units[self._baseunits]
            except KeyError:
                return None


class TallyStockPosition(TallyReport):
    _cachename = 'TallyStockPosition'
    _header = TallyRequestHeader(1, 'Export', 'Collection',
                                 'All items under Groups')

    def _build_request_body(self):
        r = etree.Element('DESC')
        sv = etree.SubElement(r, 'STATICVARIABLES')
        self._set_request_staticvariables(sv)
        self._set_request_date(sv)
        tdl = etree.SubElement(r, 'TDL')
        tdlmessage = etree.SubElement(tdl, 'TDLMESSAGE')
        collection = etree.SubElement(tdlmessage, 'COLLECTION', ISMODIFY='No',
                                      NAME="All items under Groups")
        colltype = etree.SubElement(collection, 'TYPE')
        colltype.text = 'stock item'
        fetchlist = ['Name', 'Parent', 'BaseUnits',
                     'ClosingBalance', 'ClosingRate', 'ClosingValue']
        self._build_fetchlist(collection, fetchlist)
        return etree.ElementTree(r)

    _container = 'collection'
    _content = {
        'stockitems': ('stockitem', TallyStockItemPosition)
    }


def get_master(company_name, force=False):
    global _masters
    if not force and company_name in _masters.keys():
        return _masters[company_name]
    try:
        _masters[company_name] = TallyStockMaster(company_name)
    except TallyNotAvailable:
        _masters[company_name] = None
    return _masters[company_name]


_masters = {}


def get_position(company_name, force=False):
    global _positions
    if not force and company_name in _positions.keys():
        return _positions[company_name]
    try:
        _positions[company_name] = TallyStockPosition(company_name)
    except TallyNotAvailable:
        _positions[company_name] = None
    return _positions[company_name]


_positions = {}

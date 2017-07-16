# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import comtypes


class GUIDBase(object):

    def __init__(self, target, guid=None):
        self.target = target
        if guid is None:
            guid = comtypes.GUID.create_new()
        else:
            try:
                guid = comtypes.GUID(guid)
            except WindowsError:
                guid = comtypes.GUID.create_new()
        self.guid = str(guid)

    def __repr__(self):
        return "eg.GUID('%s')" % self.guid

    def __str__(self):
        return self.guid

    def __unicode__(self):
        return unicode(self.guid)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if hasattr(self.target, item):
            return getattr(self.target, item)

        raise AttributeError('%r does not have attribute %r' % (self, item))

    def __call__(self):
        return self.target


class GuidException(Exception):

    def __init__(self, guid):
        self.guid = guid

    def __str__(self):
        return 'No GUID %r exists' % self.guid


class GUID(object):

    GuidException = GuidException

    def __init__(self):
        self.guidObjects = {}

    def NewId(self, target):
        guid = GUIDBase(target)
        self.guidObjects[guid.guid] = guid
        return guid

    def AddId(self, target, guid):
        if guid in self.guidObjects:
            self.guidObjects[guid].target = target
            return self.guidObjects[guid]
        else:
            guid = GUIDBase(target, guid)
            self.guidObjects[str(guid)] = guid
            return guid

    def __call__(self, guid):
        if guid in self.guidObjects:
            return self.guidObjects[guid]
        try:
            return self.guidObjects[guid.guid]
        except AttributeError:
            guid = self.AddId(None, guid)
            return guid
        except KeyError:
            raise self.GuidException(guid)


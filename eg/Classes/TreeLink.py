# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
import wx


class TreeLink(object):
    currentXmlId = 0
    id2target = {}
    sessionId2target = {}
    unresolvedIds = {}
    linkList = []
    inUndo = False
    __slots__ = ["target", "owner", "xmlId"]

    def __init__(self, owner):
        self.target = None
        self.owner = owner
        self.xmlId = -1


    @classmethod
    @eg.LogIt
    def StartLoad(cls):
        cls.currentXmlId = 0
        cls.id2target.clear()
        cls.unresolvedIds.clear()
        cls.sessionId2target.clear()


    @classmethod
    def StopLoad(cls):
        for link, xmlId in cls.linkList:
            if xmlId is not None and xmlId != -1:
                if xmlId in cls.sessionId2target:
                    target = cls.sessionId2target[xmlId]
                elif xmlId in cls.id2target:
                    target = cls.id2target[xmlId]
                else:
                    eg.PrintDebugNotice("target id %d not found" % xmlId)
                    continue
                cls.id2target[target.xmlId] = target
                link.xmlId = target.xmlId
                link.target = target
                if target.dependants is None:
                    target.dependants = [link]
                else:
                    target.dependants.append(link)
                wx.CallAfter(eg.Notify, "NodeChanged", link.owner)
        del cls.linkList[:]


    @classmethod
    def NewXmlId(cls, xmlId, obj):
        if TreeLink.inUndo:
            if xmlId != -1:
                cls.id2target[xmlId] = obj
                if xmlId in cls.unresolvedIds:
                    obj.dependants = cls.unresolvedIds[xmlId]
                    for link in obj.dependants:
                        link.target = obj
                        if link.owner:
                            link.owner.Refresh()
                return xmlId
        if xmlId != -1:
            cls.sessionId2target[xmlId] = obj
        cls.currentXmlId += 1
        return cls.currentXmlId


    @classmethod
    def StartUndo(cls):
        cls.inUndo = True


    @classmethod
    def StopUndo(cls):
        cls.inUndo = False
        notFoundLinks = []
        for link, xmlId in cls.linkList:
            if xmlId is not None and xmlId != -1:
                if xmlId not in cls.id2target:
                    notFoundLinks.append((link, xmlId))
                    continue
                target = cls.id2target[xmlId]

                link.xmlId = target.xmlId
                link.target = target
                if target.dependants is None:
                    target.dependants = [link]
                else:
                    target.dependants.append(link)
                eg.Notify("NodeChanged", link.owner)
        cls.linkList = notFoundLinks


    @classmethod
    def RemoveDependants(cls, target):
        for link in target.dependants:
            link.target = None
            if link.owner:
                eg.Notify("NodeChanged", link.owner)
        cls.unresolvedIds[target.xmlId] = target.dependants
        target.dependants = None


    @classmethod
    def CreateFromArgument(cls, owner, xmlId):
        self = TreeLink(owner)
        cls.linkList.append((self, xmlId))
        return self


    def SetTarget(self, target):
        if target == self.target:
            return
        if self.target:
            self.target.dependants.remove(self)
        self.target = target
        if target:
            if target.dependants is None:
                target.dependants = [self]
            else:
                target.dependants.append(self)
            self.xmlId = target.xmlId
            self.id2target[target.xmlId] = target
        eg.Notify("NodeChanged", self.owner)


    def Refresh(self):
        eg.Notify("NodeChanged", self.owner)


    def Delete(self):
        if self.target:
            self.target.dependants.remove(self)
        self.target = None


    def __repr__(self):
        return "XmlIdLink(%d)" % self.xmlId


    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass


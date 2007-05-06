# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import eg
import types

    
class TreeLink(object):
    currentXmlId = 0
    id2target = {}
    sessionId2target = {}
    unresolvedIds = {}
    linkList = []
    inUndo = False
    __slots__ = ["target", "owner", "id"]
    
    def __init__(self, owner):
        self.target = None
        self.owner = owner
        self.id = -1
        
        
    @classmethod
    @eg.LogIt
    def StartLoad(cls):
        cls.currentXmlId = 0
        cls.id2target.clear()
        cls.unresolvedIds.clear()
        cls.sessionId2target.clear()
        
        
    @classmethod
    def StopLoad(cls):
        for link, id in cls.linkList:
            if id is not None and id != -1:
                if id in cls.sessionId2target:
                    target = cls.sessionId2target[id]
                elif id in cls.id2target:
                    target = cls.id2target[id]
                else:
                    eg.Notice("target id %d not found" % id)
                    continue
                cls.id2target[target.xmlId] = target
                link.id = target.xmlId
                link.target = target
                if target.dependants is None:
                    target.dependants = [link]
                else:
                    target.dependants.append(link)
                link.owner.Refresh()
        del cls.linkList[:]
    
    
    @classmethod
    def NewXmlId(cls, id, obj):
        if TreeLink.inUndo:
            if id != -1:
                cls.id2target[id] = obj
                if id in cls.unresolvedIds:
                    obj.dependants = cls.unresolvedIds[id]
                    for link in obj.dependants:
                        link.target = obj
                        if link.owner:
                            link.owner.Refresh()
                return id
        if id != -1:
            cls.sessionId2target[id] = obj
        cls.currentXmlId += 1
        return cls.currentXmlId


    @classmethod
    def StartUndo(cls):
        cls.inUndo = True
    
        
    @classmethod
    def StopUndo(cls):
        cls.inUndo = False
        notFoundLinks = []
        for link, id in cls.linkList:
            if id is not None and id != -1:
                if id not in cls.id2target:
                    notFoundLinks.append((link, id))
                    continue
                target = cls.id2target[id]
                
                link.id = target.xmlId
                link.target = target
                if target.dependants is None:
                    target.dependants = [link]
                else:
                    target.dependants.append(link)
                link.owner.Refresh()
        cls.linkList = notFoundLinks
    
        
    @classmethod
    def RemoveDependants(cls, target):
        for link in target.dependants:
            link.target = None
            if link.owner:
                link.owner.Refresh()
        cls.unresolvedIds[target.xmlId] = target.dependants
        #del cls.id2target[target.xmlId] # = None
        target.dependants = None
        
        
    @classmethod
    def CreateFromArgument(cls, owner, id):
        self = TreeLink(owner)
        cls.linkList.append((self, id))
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
            self.id = target.xmlId
            self.id2target[target.xmlId] = target
        self.owner.Refresh()
    
    
    def Refresh(self):
        self.owner.Refresh()
        
        
    def Delete(self):
        if self.target:
            self.target.dependants.remove(self)
        self.target = None


    def __repr__(self):
        return "XmlIdLink(%d)" % self.id
        

    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass

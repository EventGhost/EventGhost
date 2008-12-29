# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2008-07-15 18:55:54 +0200 (Di, 15 Jul 2008) $
# $LastChangedRevision: 452 $
# $LastChangedBy: bitmonster $

    
class NotificationHandler(object):
    __slots__ = ["value", "listeners"]
    
    def __init__(self, initialValue=None):
        self.value = initialValue
        self.listeners = []
        
        
    def Fire(self, value=None):
        self.value = value
        for listener in self.listeners:
            listener(value)
        
        
    def Subscribe(self, listener):
        self.listeners.append(listener)
        return self.value        
    
    
    def UnSubscribe(self, listener):
        self.listeners.remove(listener)


    def GetValue(self):
        return self.value
    
    
    
        

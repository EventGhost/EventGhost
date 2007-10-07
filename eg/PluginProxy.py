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
# $LastChangedDate: 2007-09-03 16:52:03 +0200 (Mon, 03 Sep 2007) $
# $LastChangedRevision: 223 $
# $LastChangedBy: bitmonster $



class PluginProxy(object):
    
    def __init__(self, plugin):
        self.plugin = plugin
        self.actions = plugin.info.actions
        
    
    def __getattr__(self, name):
        return self.actions[name]
        
        
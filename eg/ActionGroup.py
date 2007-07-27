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
import new
import types

from ActionClass import ActionClass
from Utils import SetClass



class ActionInfo(object):
    icon = eg.Icons.ACTION_ICON
    
    def __init__(self, icon):
        self.icon = icon
        
        
    
    
    
def CreateAction(actionCls, plugin):
    if not issubclass(actionCls, ActionClass):
        eg.DebugNote("creating new action class from " + str(actionCls))
        actionCls = new.classobj(
            actionCls.__name__,
            (actionCls, ActionClass), 
            {}
        )
    action = actionCls.__new__(actionCls)
    action.plugin = plugin
    icon = plugin.info.icon
    if action.iconFile:
        try:
            path = plugin.info.path + action.iconFile + ".png"
            icon = eg.Icons.PathIcon(path)
        except:
            eg.PrintError(
                "Error while loading icon file %s" % action.iconFile
            )

    text = actionCls.text
    if text is None:
        text = getattr(plugin.text, actionCls.__name__, None)
        if text is None:
            class text:
                pass
            text = text()
            setattr(plugin.text, actionCls.__name__, text)
    elif type(text) == types.ClassType:        
        translation = getattr(plugin.text, actionCls.__name__, None)
        if translation is None:
            translation = text()
        SetClass(translation, text)
        text = translation
        setattr(plugin.text, actionCls.__name__, text)
    textCls = text.__class__
    if not hasattr(textCls, "name"):
        name = actionCls.name
        textCls.name = actionCls.__name__ if name is None else name
    
    if not hasattr(textCls, "description"):
        description = actionCls.description
        textCls.description = textCls.name if description is None else description
        
    actionCls.text = text
    action.name = text.name
    action.description = text.description
    action.info = ActionInfo(icon)
    action.__init__()
    return action
    
    
                
class ActionGroup:
    plugin = None
    name = None
    description = None
    icon = eg.Icons.FOLDER_ICON
    
    def __init__(self, plugin, name=None, description=None, iconFile=None):
        self.plugin = plugin
        self.expanded = False
        self.name = name or plugin.name
        self.description = description or plugin.description
        if iconFile is None:
            self.icon = plugin.info.icon
        else:
            self.icon = eg.Icons.PathIcon(plugin.info.path + iconFile + ".png")
        self.actionList = []
        
        
    def AddGroup(self, name=None, description=None, iconFile=None):
        group = ActionGroup(self.plugin, name, description, iconFile)
        self.actionList.append(group)
        return group
    
    
    def AddAction(self, actionClass, hidden=False):
        action = CreateAction(actionClass, self.plugin)
        setattr(self.plugin, actionClass.__name__, action)
        if not hidden:
            self.actionList.append(action)
        return action
    



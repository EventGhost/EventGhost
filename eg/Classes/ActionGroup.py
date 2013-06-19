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

from types import ClassType

from eg.Utils import SetClass

ActionClass = eg.ActionClass


class ActionInfo(object):
    __slots__ = ["icon"]
    
    def __init__(self, icon):
        self.icon = icon
            
    
                
class ActionGroup(object):
    __slots__ = [
        "plugin", "name", "description", "icon", "actionList", "expanded"
    ]
    
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
        action = self.CreateAction(actionClass, self.plugin)
        if not hidden:
            self.actionList.append(action)
        return action
    

    @classmethod
    def CreateAction(cls, actionCls, plugin):
        pluginInfo = plugin.info
        actionClsName = actionCls.__name__
        if not issubclass(actionCls, ActionClass):
            eg.PrintDebugNotice("creating new action class from " + str(actionCls))
            actionCls = ClassType(
                actionClsName,
                (actionCls, ActionClass), 
                {}
            )
        icon = pluginInfo.icon
        if actionCls.iconFile:
            try:
                path = pluginInfo.path + actionCls.iconFile + ".png"
                icon = eg.Icons.PathIcon(path)
            except:
                eg.PrintError(
                    "Error while loading icon file %s" % actionCls.iconFile
                )
        if icon == eg.Icons.PLUGIN_ICON:
            icon = eg.Icons.ACTION_ICON
        else:
            icon = eg.Icons.ActionSubIcon(icon)
        
        text = actionCls.text
        if text is None:
            text = getattr(plugin.text, actionClsName, None)
            if text is None:
                class text:
                    pass
                text = text()
                setattr(plugin.text, actionClsName, text)
        elif type(text) == ClassType:        
            translation = getattr(plugin.text, actionClsName, None)
            if translation is None:
                translation = text()
            SetClass(translation, text)
            text = translation
            setattr(plugin.text, actionClsName, text)
        textCls = text.__class__
        if not hasattr(textCls, "name"):
            name = actionCls.name
            textCls.name = actionClsName if name is None else name
        
        if not hasattr(textCls, "description"):
            description = actionCls.description
            textCls.description = textCls.name if description is None else description
            
        actionCls = ClassType(
            actionClsName,
            (actionCls, ), 
            dict(
                name=text.name,
                description=text.description,
                plugin=plugin,
                info=ActionInfo(icon),
                text=text,
                Exceptions=eg.Exceptions
            )
        )
        pluginInfo.actions[actionClsName] = actionCls
        actionCls.OnAddAction()
        return actionCls
    

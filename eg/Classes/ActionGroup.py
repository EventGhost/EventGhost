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
        "plugin", "name", "description", "icon", "items", "expanded"
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
        self.items = []
        
        
    def AddGroup(self, name, description=None, iconFile=None, identifier=None):
        """
        Create and add a new sub-group.
        """
        plugin = self.plugin
        if identifier is not None:
            class Text:
                pass
            Text.name = name
            if description is None:
                Text.description = name
            else:
                Text.description = description
            text = getattr(plugin.text, identifier, None)
            if text is None:
                text = Text()
            else:        
                SetClass(text, Text)
            setattr(plugin.text, identifier, text)
            name = text.name
            description = text.description
        group = ActionGroup(plugin, name, description, iconFile)
        self.items.append(group)
        return group
        

    def AddAction(self, actionCls, clsName=None, name=None, description=None, value=None, hidden=False):
        if not issubclass(actionCls, ActionClass):
            raise Exception("Actions must be subclasses of eg.ActionClass")
        if clsName is not None:
            actionCls = ClassType(
                clsName,
                (actionCls, ),
                dict(name=name, description=description, value=value),
            )
        plugin = self.plugin
        pluginInfo = plugin.info
        actionClsName = actionCls.__name__
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
        if not hidden:
            self.items.append(actionCls)
        return actionCls
    

    def AddActionsFromList(self, theList, defaultAction=None):
        def Recurse(theList, group):
            for parts in theList:
                if isinstance(parts, type):
                    group.AddAction(parts)
                    continue
                length = len(parts)
                if parts[0] is eg.ActionGroup:
                    # this is a new sub-group
                    aList = parts[-1]
                    cls, clsName, name, description = parts[0:4]
                    if len(parts) == 6:
                        iconFile = parts[3]
                    else:
                        iconFile = None
                    newGroup = group.AddGroup(name, description, iconFile, identifier=clsName)
                    Recurse(aList, newGroup)
                    continue
                if length == 4:
                    # this is a new default action
                    actionCls = defaultAction
                    clsName, name, description, value = parts
                elif length == 5:
                    # this is a new sub-action
                    actionCls, clsName, name, description, value = parts
                else:
                    raise Exception("Wrong number of fields in the list", parts)
                       
                group.AddAction(actionCls, clsName, name, description, value)
                
        Recurse(theList, self)

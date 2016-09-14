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

from os.path import join
from types import ClassType

# Local imports
import eg
from eg.Utils import SetDefault

class ActionGroup(object):
    __slots__ = [
        "plugin", "name", "description", "icon", "items", "expanded",
    ]

    def __init__(self, plugin, name=None, description=None, iconFile=None):
        self.plugin = plugin
        self.expanded = False
        self.name = name or plugin.name
        self.description = description or plugin.description
        if iconFile is None:
            self.icon = plugin.info.icon
        else:
            self.icon = eg.Icons.PathIcon(
                join(plugin.info.path, iconFile + ".png")
            )
        self.items = []

    def AddAction(
        self,
        actionCls,
        clsName=None,
        name=None,
        description=None,
        value=None,
        hidden=False
    ):
        if not issubclass(actionCls, eg.ActionBase):
            raise Exception("Actions must be subclasses of eg.ActionBase")
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
                path = join(pluginInfo.path, actionCls.iconFile + ".png")
                icon = eg.Icons.PathIcon(path)
            except:
                eg.PrintError(
                    "Error while loading icon file %s" % actionCls.iconFile
                )
        if icon == eg.Icons.PLUGIN_ICON:
            icon = eg.Icons.ACTION_ICON
        else:
            icon = eg.Icons.ActionSubIcon(icon)

        text = self.Translate(plugin, actionCls, actionClsName)
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
                    clsName, name, description = parts[1:4]
                    if len(parts) == 6:
                        iconFile = parts[3]
                    else:
                        iconFile = None
                    newGroup = group.AddGroup(
                        name,
                        description,
                        iconFile,
                        identifier=clsName
                    )
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
                    raise Exception(
                        "Wrong number of fields in the list",
                        parts
                    )
                group.AddAction(actionCls, clsName, name, description, value)

        Recurse(theList, self)

    def AddGroup(self, name, description=None, iconFile=None, identifier=None):
        """
        Create and add a new sub-group.
        """
        plugin = self.plugin
        if identifier is not None:
            description = name if description is None else description
            defaultText = ClassType(
                identifier,
                (),
                {"name": name, "description": description}
            )
            translatedText = getattr(plugin.text, identifier, None)
            if translatedText is None:
                translatedText = ClassType(identifier, (), {})
                setattr(plugin.text, identifier, translatedText)
            SetDefault(translatedText, defaultText)
            name = translatedText.name
            description = translatedText.description
        group = ActionGroup(plugin, name, description, iconFile)
        self.items.append(group)
        return group

    def Translate(self, plugin, actionCls, actionClsName):
        defaultText = actionCls.text
        if defaultText is None:
            defaultText = ClassType(actionClsName, (), {})
        translatedText = getattr(plugin.text, actionClsName, None)
        if translatedText is None:
            translatedText = ClassType(actionClsName, (), {})
            setattr(plugin.text, actionClsName, translatedText)
        SetDefault(translatedText, defaultText)
        if not hasattr(translatedText, "name"):
            name = actionCls.name
            translatedText.name = actionClsName if name is None else name
        if not hasattr(translatedText, "description"):
            description = actionCls.description
            translatedText.description = (
                translatedText.name if description is None else description
            )
        return translatedText


class ActionInfo(object):
    __slots__ = ["icon"]

    def __init__(self, icon):
        self.icon = icon

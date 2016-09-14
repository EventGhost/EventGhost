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

"""
Definition of the abstract plugin class.
"""

import wx
from threading import Lock

# Local imports
import eg

gTriggerEventLock = Lock()

class PluginBase(object):
    """
    Base class of every EventGhost plugin written in Python.

    .. attribute:: name

        The (localised) name of the plugin.

    .. attribute:: description

        The (localised) description of the plugin.

    .. attribute:: info

        Internally used house keeping data. Don't try to manipulate
        this yourself.

    .. attribute:: text

        Assign a class with text strings to this field to get them localised.
        For more information read the section about
        :ref:`internationalisation`.
    """
    name = None
    description = None
    info = None
    text = None
    Exceptions = None

    __metaclass__ = eg.PluginMetaClass

    # used for automatic documentation creation
    __docsort__ = (
        "__start__, __stop__, __close__, Configure, GetLabel, AddAction, "
        "AddGroup, TriggerEvent, TriggerEnduringEvent, EndLastEvent"
    )

    def __init__(self):
        """
        Override this if the plugin needs some code to be executed directly
        after its instantiation.

        This is also the right place to add all actions the plugin wants to
        publish with calls to :meth:`!AddAction` and :meth:`!AddGroup`.
        """
        pass

    class Exception(eg.Exception):
        pass

    def __close__(self):
        """
        Gets called, if the plugin is about to be closed.

        Override this if you have to do some cleanup before your plugin gets
        unloaded.
        """
        pass

    def __start__(self, *args):
        """
        Start/Enable the plugin.

        If your plugin is loaded and enabled by the user, this method will be
        called from EventGhost. Plugins should start its operation now.

        The plugin will also receive its parameters (if it has any) through
        this method. To make a plugin that has parameters, you will have to
        overwrite the :meth:`!Configure` method also.
        """
        pass

    def __stop__(self):
        """
        Stop/Disable the plugin.

        If the user disables the plugin, this method will be called. The
        plugin should from now on not trigger any events anymore, till it
        gets another call to its :meth:`!__start__` method.
        """
        pass

    def AddAction(
        self,
        actionCls,
        clsName=None,
        name=None,
        description=None,
        value=None,
        hidden=False
    ):
        """
        Adds an :class:`eg.ActionBase` subclass to this plugin.

        The action will then be visible in the AddActionDialog of EventGhost
        for this plugin (except *hidden* is set to True).

        Through the usage of the *clsName*, *name* and *description*
        parameters, you can add the same action class multiple times with
        different names and descriptions. You can then also use the *value*
        parameter, to assign some arbitrary data to the action, that the
        action can then query through its self.value attribute.

        :param actionCls: The action class to add
        :param clsName: Overrides the actions class name with a string
        :param name: Overrides the actions name with a string
        :param description: Overrides the actions description with a string
        :param value: Some data that you would like to assign to the action
        :param hidden: If set to True, the action will not show up in the
            AddActionDialog but is otherwise fully functional.
        """
        # Here it is only defined as an abstract method.
        # The real AddAction method will be assigned shortly before the plugin
        # is instantiated (for speed purposes).
        pass

    def AddActionsFromList(self, theList, defaultAction=None):
        self.info.actionGroup.AddActionsFromList(theList, defaultAction)

    def AddEvents(self, *eventList):
        self.info.eventList = eventList

    def AddGroup(self, name=None, description=None, iconFile=None):
        """
        Adds a new sub-group to the AddActionDialog of EventGhost for this
        plugin.

        This group will appear under the group of the plugin. To add actions
        to this group, store the returned object and call AddAction on it.
        You can also call AddGroup on the returned object to create even
        deeper nested sub-groups.

        :param name: Name of the sub-group
        :param description: Description of the sub-group. Can include HTML
            tags.
        :returns: The new sub-group instance
        :rtype: eg.ActionGroup instance

        """
        # Here it is only defined as an abstract method.
        # The real AddGroup method will be assigned shortly before the plugin
        # is instantiated (for speed purposes).
        pass

    def Configure(self, *args):
        """
        This should be overridden in a subclass, if the plugin wants to have
        a configuration dialog.

        When the plugin is freshly added by the user to the configuration tree
        there are no *\*args* and you must therefore supply sufficient
        default arguments.
        If the plugin is reconfigured by the user, this method will be called
        with the same arguments as the :meth:`!__start__` method would receive.
        """
        panel = eg.ConfigPanel()
        panel.dialog.buttonRow.applyButton.Enable(False)
        label = panel.StaticText(
            eg.text.General.noOptionsPlugin,
            style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE
        )
        panel.sizer.Add((0, 0), 1, wx.EXPAND)
        panel.sizer.Add(label, 0, wx.ALIGN_CENTRE)
        panel.sizer.Add((0, 0), 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult()

    def EndLastEvent(self):
        """
        End the last event that was generated through
        :meth:`!TriggerEnduringEvent`.
        """
        self.info.lastEvent.SetShouldEnd()

    def GetLabel(self, *args):
        """
        Returns the label that should be displayed in the configuration tree
        with the current arguments.

        The default method simply shows the plugin name. If you want to have
        a different behaviour, you can override it. This method gets called
        with the same parameters as the :meth:`!__start__`  method.
        """
        return self.name

    def OnComputerResume(self, suspendType):
        """
        Prepares the plugin for resumption of the computer.
        """
        pass

    def OnComputerSuspend(self, suspendType):
        """
        Prepares the plugin for suspension of the computer.
        """
        pass

    def OnDelete(self):
        """
        Will be called if the user deletes the plugin instance from his
        configuration.
        """
        pass

    def PrintError(self, msg):
        """
        Print an error message to the logger.

        Prefer to use self.PrintError instead of eg.PrintError, since this
        method gives the user better information about the source of the error.

        :param msg: The error string you want to have printed to the logger
        """
        eg.PrintError(msg, source=self.info.treeItem)

    def TriggerEnduringEvent(self, suffix, payload=None):
        """
        Trigger an enduring event.

        Does nearly the same as :meth:`!TriggerEvent` but the event will not be
        ended immediately. This is used for devices that can have longer
        enduring events, like a remote, where you can press and hold a button.

        The plugin has to call :meth:`!EndLastEvent` to end the event. The last
        event will also be ended, if another event will be generated through
        :meth:`!TriggerEvent` or :meth:`!TriggerEnduringEvent`. This will
        ensure, that only one event per plugin can be active at the same time.
        """
        with gTriggerEventLock:
            info = self.info
            info.lastEvent.SetShouldEnd()
            event = eg.TriggerEnduringEvent(
                suffix,
                payload,
                info.eventPrefix,
                self
            )
            info.lastEvent = event
            return event

    def TriggerEvent(self, suffix, payload=None):
        """
        Trigger an event.

        If the plugin wants to trigger an event in EventGhost, it should call
        self.TriggerEvent with the event name as *suffix* parameter. It can
        also post optional additional data through the *payload* parameter.

        Keep in mind, that an event generated through this method will also
        automatically be ended immediately. If the plugin wants to generate
        an event with a longer duration, it has to use
        :meth:`!TriggerEnduringEvent`.
        """
        with gTriggerEventLock:
            info = self.info
            info.lastEvent.SetShouldEnd()
            event = eg.TriggerEvent(suffix, payload, info.eventPrefix, self)
            info.lastEvent = event
            return event

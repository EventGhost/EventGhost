# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <lpv@eventghost.org>
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

""" Definition of the abstract PluginClass. """

import eg
import wx
from PluginMetaClass import PluginMetaClass
from ActionGroup import CreateAction
        
       
class PluginClass(object):
    """ 
    Base class of every EventGhost-Plugin written in Python 
    """
    
    #: 'name' is a read-only field. Don't set or manipulate
    #: it yourself. It will be set from the information you supplied in 
    #: the __info__.py and might get translated to the user's current language.
    name = None
    #: 'description' is a read-only field. Don't set or manipulate
    #: it yourself. It will be set from the information you supplied in 
    #: the __info__.py and might get translated to the user's current language.
    description = None
    
    #: If your plugin supports more than one instance in the 
    #: configuration-tree, set 'canMultiLoad' to True in your class-definition.
    canMultiLoad = False
    
    #: don't try to manipulate this private variable yourself.
    info = None
    #: don't try to manipulate this private variable yourself.
    text = None
    #: don't try to manipulate this private variable yourself.
    __metaclass__ = PluginMetaClass 


    def __init__(self):
        """
        Override this if the plugin needs some code to be executed directly 
        after its instantiation.
        
        This is also the right place to add all actions the plugin wants to 
        publish with calls to AddAction and AddGroup.
        """
        self.AddAllActions()
        
        
    def __start__(self, *args):
        """
        Start/Enable the plugin.
        
        If your plugin is loaded and enabled by the user, this method will be 
        called from EventGhost. Plugins should start their operation now and
        should not generate events before they are started this way.
        
        The plugin will also receive its parameters (if it has any) through 
        this method. To make a plugin that has parameters, you will have to 
        write a 'Configure' method also (see below).
        """
        pass
        
        
    def __stop__(self):
        """
        Stop/Disable the plugin.
        
        If the user disables the plugin, this method will be called. The 
        plugin should from now on not trigger any events anymore, till it
        gets another call to its __start__ method.
        """
        pass
        
        
    def __close__(self):
        """
        Close the plugin.
        
        Override this if you have to do some cleanup before your plugin gets
        unloaded.
        """
        pass
        
                            
    def TriggerEvent(self, suffix, payload=None):
        """
        Trigger an event.
        
        If the plugin wants to trigger an event in EventGhost, it should call
        self.TriggerEvent with the event name as parameter. It can also post
        optional additional data through the payload parameter.
        
        Keep in mind, that an event generated through TriggerEvent will also
        automatically be ended immediately. If the plugin wants to generate an
        event with a longer duration, it has to use TriggerEnduringEvent.
        """
        info = self.info
        info.lastEvent.SetShouldEnd()
        event = eg.TriggerEvent(suffix, payload, info.eventPrefix, self)
        info.lastEvent = event
        return event
        
        
    def TriggerEnduringEvent(self, suffix, payload=None):
        """
        Trigger an enduring event.
        
        Does nearly the same as TriggerEvent but the event will not be ended 
        immediately. This is used for devices that can have longer enduring 
        events, like a remote, where you can press and hold a button.
        
        The plugin has to call EndLastEvent to end the event. The last event 
        will also be ended, if another event will be generated through
        TriggerEvent or TriggerEnduringEvent. This will ensure, that only
        one event per plugin can be active at the same time.
        """
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
        
        
    def EndLastEvent(self):
        """
        End the last event that was generated through TriggerEnduringEvent.
        """
        self.info.lastEvent.SetShouldEnd()
        
        
    def AddAction(self, action, hidden=False):
        """
        Add an action to the AddActionDialog of EventGhost for this plugin.
        
        :Parameters:
          `action` : eg.ActionClass subclass
            The ActionClass to add
          `hidden` : bool
            If set to True, the action will not show up in the AddActionDialog
            but is otherwise fully functional.
        """
        action = CreateAction(action, self)
        setattr(self, action.__class__.__name__, action)
        actionList = self.info.actionList
        if actionList is None:
            actionList = []
            eg.actionList.append(self)
            self.info.actionList = actionList
        if not hidden:
            actionList.append(action)
        return action
    
    
    def AddGroup(self, name=None, description=None, iconFile=None):
        """
        Add an new sub-group to the AddActionDialog of EventGhost for this
        plugin.
        
        This group will appear under the group of the plugin. To add actions
        to this group, store the returned object and call AddAction on it.
        You can also call AddGroup on the returned object to create even 
        deeper nested sub-groups.
        
        :Parameters:
            `name` : string
                Name of the sub-group
            `description` : string
                Description of the sub-group. Can include HTML tags.
            
        :return: The new sub-group instance
        :rtype: <instance of eg.ActionGroup>
            
        """
        actionList = self.info.actionList
        if actionList is None:
            actionList = []
            eg.actionList.append(self)
            self.info.actionList = actionList
        group = eg.ActionGroup(self, name, description, iconFile)
        actionList.append(group)
        return group
    
    
    def AddAllActions(self):
        for actionClass in self.info.actionClassList:
            self.AddAction(
                actionClass, 
                issubclass(actionClass, eg.HiddenAction)
            )
    
    
    def GetLabel(self, *args):
        """
        Return the label that should be displayed in the configuration tree
        with the current arguments.
        
        This default method simply shows the plugin name. If you want to have 
        a different behaviour, you can override it.
        
        This method gets called with the same parameters as the __start__
        method.
        """
        return self.name
        
        
    def PrintError(self, msg):
        """
        Print an error message to the logger.
        
        Prefer to use self.PrintError instead of eg.PrintError, since this
        method gives the user better information about the source of the error.
        
        :Parameters:
          `msg` : string
            The error message you want to have printed to the logger
        """
        eg.log.DoItemPrint(msg, 1, self.info.treeItem)
        
        
    def Configure(self, *args):
        """
        This should be overridden in a subclass, if the plugin wants to have 
        a configuration dialog.
        
        When the plugin is freshly added by the user to the configuration tree
        there are no "args" and you must therefor supply sufficent
        default arguments.
        If the plugin is reconfigured by the user, this method will be called
        with the same arguments as the __start__ method would receive.
        """
        dialog = eg.ConfigurationDialog(self)
        label = wx.StaticText(dialog, -1, eg.text.General.noOptionsPlugin)
        dialog.sizer.Add(label)
        dialog.AffirmedShowModal()
        
        

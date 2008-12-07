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
""" 
Definition of the abstract PluginClass. 
"""

import eg
        
       
class PluginClass(object):
    """ 
    Base class of every EventGhost plug-in written in Python.
        
    .. attribute:: name
    
        The (localized) name of the plug-in.
        
    .. attribute:: description
    
        The (localized) description of the plug-in.
        
    .. attribute:: info
        
        Internally used house keeping data. Don't try to manipulate
        this yourself.
        
    .. attribute:: text
    
        Assign a class with text strings to this field to get them localized.
    """
    
    name = None
    description = None
    info = None
    text = None
    __metaclass__ = eg.PluginMetaClass 
    # used for automatic documentation creation
    __docsort__ = ( 
        "__start__, __stop__, __close__, Configure, AddAction, AddGroup, "
        "TriggerEvent, TriggerEnduringEvent, EndLastEvent"
    )
    
    def __init__(self):
        """
        Override this if the plug-in needs some code to be executed directly 
        after its instantiation.
        
        This is also the right place to add all actions the plug-in wants to 
        publish with calls to AddAction and AddGroup.
        """
        pass
        
        
    def __start__(self, *args):
        """
        Start/Enable the plug-in.
        
        If your plug-in is loaded and enabled by the user, this method will be 
        called from EventGhost. Plug-ins should start their operation now and
        should not generate events before they are started this way.
        
        The plug-in will also receive its parameters (if it has any) through 
        this method. To make a plug-in that has parameters, you will have to 
        write a 'Configure' method also (see below).
        """
        pass
        
        
    def __stop__(self):
        """
        Stop/Disable the plug-in.
        
        If the user disables the plug-in, this method will be called. The 
        plug-in should from now on not trigger any events anymore, till it
        gets another call to its __start__ method.
        """
        pass
        
        
    def __close__(self):
        """
        Gets called, if the plug-in is about to be closed.
        
        Override this if you have to do some cleanup before your plug-in gets
        unloaded.
        """
        pass
        
                            
    def SetArguments(self, *args):
        pass
    
    
    def RegisterEvents(self, eventList):
        self.info.eventList = eventList

            
    def GetEvents(self):
        return None
    
    
    def TriggerEvent(self, suffix, payload=None):
        """
        Trigger an event.
        
        If the plug-in wants to trigger an event in EventGhost, it should call
        self.TriggerEvent with the event name as *suffix* parameter. It can 
        also post optional additional data through the *payload* parameter.
        
        Keep in mind, that an event generated through this method will also
        automatically be ended immediately. If the plug-in wants to generate 
        an event with a longer duration, it has to use 
        :meth:`TriggerEnduringEvent`.
        """
        info = self.info
        info.lastEvent.SetShouldEnd()
        event = eg.TriggerEvent(suffix, payload, info.eventPrefix, self)
        info.lastEvent = event
        return event
        
        
    def TriggerEnduringEvent(self, suffix, payload=None):
        """
        Trigger an enduring event.
        
        Does nearly the same as :meth:`TriggerEvent` but the event will not be 
        ended immediately. This is used for devices that can have longer 
        enduring events, like a remote, where you can press and hold a button.
        
        The plug-in has to call :meth:`EndLastEvent` to end the event. The last 
        event will also be ended, if another event will be generated through
        :meth:`TriggerEvent` or :meth:`TriggerEnduringEvent`. This will 
        ensure, that only one event per plug-in can be active at the same time.
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
        End the last event that was generated through 
        :meth:`TriggerEnduringEvent`.
        """
        self.info.lastEvent.SetShouldEnd()
        
        
    def AddAction(self, actionCls, clsName=None, name=None, description=None, value=None, hidden=False):
        """
        Add an action to the AddActionDialog of EventGhost for this plug-in.
        
        :param action: The ActionClass to add
        :param hidden: If set to True, the action will not show up in the 
            AddActionDialog but is otherwise fully functional.
        """
        # Here it is only defined as an abstract method. 
        # The real AddAction method will be assigned shortly before the plug-in
        # is instantiated (for speed purposes).
        pass
        
    
    def AddGroup(self, name=None, description=None, iconFile=None):
        """
        Add an new sub-group to the AddActionDialog of EventGhost for this
        plugin.
        
        This group will appear under the group of the plug-in. To add actions
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
    
    
    def GetLabel(self, *dummyArgs):
        """
        Return the label that should be displayed in the configuration tree
        with the current arguments.
        
        This default method simply shows the plug-in name. If you want to have 
        a different behavior, you can override it.
        
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
        eg.PrintError(msg, source=self.info.treeItem)
        
        
    def Configure(self, *dummyArgs):
        """
        This should be overridden in a subclass, if the plug-in wants to have 
        a configuration dialog.
        
        When the plug-in is freshly added by the user to the configuration tree
        there are no "args" and you must therefore supply sufficient
        default arguments.
        If the plug-in is reconfigured by the user, this method will be called
        with the same arguments as the __start__ method would receive.
        """
        panel = eg.ConfigPanel(self)
        panel.dialog.buttonRow.applyButton.Enable(False)
        label = panel.StaticText(eg.text.General.noOptionsPlugin)
        panel.sizer.Add(label)
        while panel.Affirmed():
            panel.SetResult()
        
        
    class Exception(eg.Exception):
        pass
    
    
    def OnComputerSuspend(self, suspendType):
        """
        Prepares the plug-in for suspension of the computer.
        """
        pass
    
    
    def OnComputerResume(self, suspendType):
        """
        Prepares the plug-in for resumption of the computer.
        """
        pass
    
    
    def OnDelete(self):
        """
        Will be called if the user deletes the plug-in instance from his
        configuration.
        """
        pass
        
    
    def AddActionsFromList(self, theList, defaultAction=None):
        self.info.actionGroup.AddActionsFromList(theList, defaultAction)


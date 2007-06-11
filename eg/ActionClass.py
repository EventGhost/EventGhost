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
from ActionMetaClass import ActionMetaClass


class ActionClass(object):
    """ 
    Base class of every action of a EventGhost-Plugin written in Python 
    """
    
    # Set these to descriptive values in your class definition. 
    # They might get translated by PluginClass.AddAction to the user's 
    # language if a translation is found.
    name = None
    description = None
    
    # This will be set from PluginClass.AddAction for convenience, so every 
    # action can access its own plugin instance through this member variable.
    plugin = None
    
    # Name of a icon-file if any. Use a 16x16-PNG and drop it inside your
    # plugin's folder. Only specify the name of the file without extension.
    iconFile = None
    
    # Don't try to manipulate these variables yourself:
    info = None
    text = None
    __metaclass__ = ActionMetaClass
    
    
    def __call__(self, *args):
        """
        Do the actual work. Will in most cases be overwritten in subclasses.
        """
        # This Compile call is only here to support calls of pre-compiled 
        # actions (see below) from PythonScript/PythonCommand actions. 
        # Normally all actions will overwrite this __call__ method completely.
        self.Compile(*args)()
    
    
    def GetLabel(self, *args):
        """
        Return the label that should be displayed in the configuration tree
        with the current arguments.
        
        This default method simply shows the action name and
        the first parameter if there is any. If you want to have a different 
        behaviour, override it.
        
        This method gets called with the same parameters as the __call__
        method.
        """
        s = self.name
        if args:
            s += ': ' + unicode(args[0])
        return s
        
        
    def PrintError(self, msg):
        """
        Print an error message to the logger.
        
        Prefer to use self.PrintError instead of eg.PrintError, since this
        method might be enhanced in the future to give the user better
        information about the source of the error.
        """
        eg.PrintError(msg)
        
        
    def Configure(self, *args):
        """
        This should be overridden in a subclass, if the action wants to have 
        a configuration dialog.
        
        When the action is freshly added by the user to the configuration tree
        there are no "args" and you must therefor supply sufficent
        default arguments.
        If the action is reconfigured by the user, this method will be called
        with the same arguments as the __call__ method.
        """
        dialog = eg.ConfigurationDialog(self)
        label = wx.StaticText(dialog, -1, eg.text.General.noOptionsAction)
        dialog.sizer.Add(label)
        if dialog.AffirmedShowModal():
            pass
    
    
# An ActionClass will only define a "Compile" method, if it uses a special 
# way to implement its action. These actions receive a call to Compile
# everytime their parameters change (the user has reconfigured the action)
# or in the moment the configuration file is loaded and an action of this 
# type is created because it was saved in the tree. 
# The Compile method should return a "callable" object, that will be called 
# without any arguments. This "callable" will then be called instead of the
# the actions __call__ method.
# This way actions can be build that need considerable time to compute
# somthing out of the parameters but need less time for the actual execution 
# of the action. One example of such action is the PythonScript action, that 
# compiles the Python source everytime it changes and then this compiled
# code object gets called instead of doing compile&run in the __call__ method.
#
#
#    def Compile(self, *args):
#        """
#        Special implementation for actions with pre-compiled parameters.
#        """
#        raise NotImplementedError
#    
    
    
import wx
    
class ActionWithStringParameter(ActionClass):
    """
    Simple ActionClass subclass, that only has a single string parameter.
    """
    #: Set parameterDescription to a descriptive string of the one and only
    #: parameter this action has.
    parameterDescription = None
    
    def Configure(self, s=""):
        """
        Simple configuration dialog with a single TextCtrl to edit the
        the string parameter of this action.
        """
        dialog = eg.ConfigurationDialog(self, resizeable=True)

        parameterDescription = None
        if self.parameterDescription:
            parameterDescription = self.parameterDescription
        elif (
            hasattr(self, "text")
            and hasattr(self.text, "parameterDescription")
        ):
            parameterDescription = self.text.parameterDescription

        if parameterDescription:    
            labelCtrl = wx.StaticText(dialog, -1, parameterDescription)
            dialog.sizer.Add(labelCtrl, 0, wx.EXPAND)
            dialog.sizer.Add((5, 5))
        parameterCtrl = wx.TextCtrl(dialog, -1, s)
        dialog.sizer.Add(parameterCtrl, 0, wx.EXPAND)
        parameterCtrl.SetFocus()
        wx.CallAfter(parameterCtrl.SetInsertionPointEnd)
        
        if dialog.AffirmedShowModal():
            return (parameterCtrl.GetValue(), )


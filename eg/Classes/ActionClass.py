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
from types import ClassType


class ActionClass(object):
    """ 
    Base class of every action of a EventGhost plugin written in Python 
    
    .. attribute:: name
    
        Set this to descriptive name in your class definition. 
        It might get translated by PluginClass.AddAction() to the user's 
        language if a translation is found.
    
    .. attribute:: description
    
        Set this to descriptive description in your class definition. 
        It might get translated by PluginClass.AddAction() to the user's 
        language if a translation is found.
    
    .. attribute:: iconFile
    
        Name of an icon file if any. Use a 16x16-PNG and drop it inside your
        plugin's folder. Only specify the name of the file without extension.
     
    .. attribute:: text
    
        Assign a class with text strings to this field to get them localised.

    .. attribute:: plugin
    
        This will be set from PluginClass.AddAction() for convenience, so 
        every action can access its own plugin instance through this member 
        variable.
     
    .. attribute:: info
     
        Internally used house keeping data. Don't try to manipulate
        this yourself.
    """
    
    name = None
    description = None
    iconFile = None
    
    # Don't try to manipulate these variables yourself.
    # Will be set later by AddAction.
    plugin = None
    info = None
    text = None
    Exceptions = None 
    
    
    def __call__(self, *args):
        """
        Do the actual work. Will in most cases be overwritten in subclasses.
        """
        # This Compile call is only here to support calls of pre-compiled 
        # actions (see below) like PythonScript/PythonCommand actions. 
        # Normally all actions will overwrite this __call__ method completely.
        if self.Compile.im_func != ActionClass.Compile.im_func:
            self.Compile(*args)()
        else:
            raise NotImplementedError
    
    
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
        label = self.name
        if args:
            label += ': ' + unicode(args[0])
        return label
        
        
    def PrintError(self, msg):
        """
        Print an error message to the logger.
        
        Prefer to use :meth:`self.PrintError <eg.ActionClass.PrintError>` 
        instead of eg.PrintError, since this method might be enhanced in the 
        future to give the user better information about the source of the 
        error.
        """
        eg.PrintError(msg)
        
        
    def Configure(self, *dummyArgs):
        """
        This should be overridden in a subclass, if the action wants to have 
        a configuration dialog.
        
        When the action is freshly added by the user to the configuration tree
        there are no "args" and you must therefore supply sufficient
        default arguments.
        If the action is reconfigured by the user, this method will be called
        with the same arguments as the __call__ method.
        """
        panel = eg.ConfigPanel(self)
        label = panel.StaticText(eg.text.General.noOptionsAction)
        panel.dialog.buttonRow.applyButton.Enable(False)
        panel.sizer.Add(label)
        while panel.Affirmed():
            panel.SetResult()
    
    
    @classmethod
    def OnAddAction(cls):
        """test"""
        pass
    
    
    def Compile(self, *args):
        """
        Implementation of pre-compiled parameters.

        An ActionClass will only override the "Compile" method, if it uses a 
        special way to implement its action. An action receives a call to 
        Compile every time their parameters change (the user has reconfigured 
        the action) or in the moment the configuration file is loaded and an 
        action of this type is created because it was saved in the tree. 
        The Compile method should return a "callable" object, that will be 
        called without any arguments. This "callable" will then be called 
        instead of the the actions __call__ method.
        This way actions can be build that need considerable time to compute
        something out of the parameters but need less time for the actual 
        execution of the action. One example of such action is the 
        PythonScript action, that compiles the Python source every time it 
        changes and then this compiled code object gets called instead of 
        doing compile&run in the __call__ method.
        """
        def CallWrapper():
            return self(*args)
        return CallWrapper
    
    
    class Exception(eg.Exception):
        pass
    
    @classmethod
    def AddActionFactory(
        cls, 
        parent, 
        clsName, 
        name, 
        description=None, 
        value=None
    ):
        actionCls = ClassType(
            clsName,
            (cls, ),
            dict(name=name, description=description, value=value),
        )
        parent.AddAction(actionCls)


# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg


class ActionBase(object):
    """
    Base class of every action of a EventGhost plugin written in Python

    .. attribute:: name

        Set this to descriptive name in your class definition.
        It might get translated by :meth:`eg.PluginBase.AddAction` to the
        user's language if a translation is found.

    .. attribute:: description

        Set this to descriptive description in your class definition.
        It might get translated by :meth:`eg.PluginBase.AddAction` to the
        user's language if a translation is found.

    .. attribute:: iconFile

        Name of an icon file if any. Use a 16x16-PNG and drop it inside your
        plugin's folder. Only specify the name of the file without extension.

    .. attribute:: text

        Assign a class with text strings to this field to get them localised.
        For more information read the section about
        :ref:`internationalisation`.

    .. attribute:: plugin

        This will be set from :meth:`eg.PluginBase.AddAction` for convenience,
        so every action can access its own plugin instance through this member
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

    __docsort__ = (
        "__call__, Configure, GetLabel, Compile, PrintError, Exception"
    )

    def __call__(self, *args):
        """
        Do the actual work. Will in most cases be overwritten in subclasses.
        """
        # This Compile call is only here to support calls of pre-compiled
        # actions (see below) like PythonScript/PythonCommand actions.
        # Normally all actions will overwrite this __call__ method completely.
        if self.__class__.Compile != ActionBase.Compile:
            self.Compile(*args)()
        else:
            raise NotImplementedError(
                "Action has no __call__ method implemented."
            )


    def GetLabel(self, *args):
        """
        Returns the label that should be displayed in the configuration tree
        with the current arguments.

        The default method simply shows the action name and the first
        parameter if there is any. If you want to have a different behaviour,
        you can override it.

        This method gets called with the same parameters as the
        :meth:`!__call__` method.
        """
        label = self.name
        if args:
            label += ': ' + unicode(args[0])
        return label


    def PrintError(self, msg):
        """
        Print an error message to the logger.

        Prefer to use :meth:`!self.PrintError`
        instead of :meth:`eg.PrintError`, since this method gives the
        user better information about the source of the error.
        """
        eg.PrintError(msg)


    def Configure(self, *args):
        """
        If the action should get a configuration dialog, you should override
        this method.

        When the action is freshly added by the user to the configuration tree,
        there are no *args* and you must therefore supply sufficient
        default arguments.
        If the action is reconfigured by the user, this method will be called
        with the same arguments as the :meth:`!__call__` method.
        """
        panel = eg.ConfigPanel()
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

        An action class will only override this method, if it uses a special
        way to implement its action. An action receives a call to
        :meth:`!Compile` every time their parameters change (the user has
        reconfigured the action) or in the moment the configuration file is
        loaded and an action of this type is created because it was saved in
        the tree. The :meth:`!Compile` method should return a "callable"
        object, that can be called without any arguments. This "callable" will
        then be called instead of the the actions :meth:`!__call__` method.

        This way actions can be build that need considerable time to compute
        something out of the parameters but need less time for the actual
        execution of the action. One example of such action is the
        PythonScript action, that compiles the Python source every time it
        changes and then this compiled code object gets called instead of
        doing compile&run in the :meth:`!__call__` method.
        """
        def CallWrapper():
            return self(*args)
        return CallWrapper


    class Exception(eg.Exception):
        pass


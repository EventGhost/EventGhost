# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import sys, os
import stackless

# the following three import are needed if we are running from source and the
# Python distribution was not installed by the installer. See the following
# link for details:
# http://www.voidspace.org.uk/python/movpy/reference/win32ext.html#id10
import pywintypes
import pythoncom
import win32api

import Cli
from Utils import *


class DynamicModule(object):

    def __init__(self):
        mod = sys.modules[__name__]
        self.__dict__ = mod.__dict__
        self.__orignal_module__ = mod
        sys.modules[__name__] = self

        import __builtin__
        __builtin__.eg = self


    def __getattr__(self, name):
        mod = __import__("eg.Classes." + name, None, None, [name], 0)
        self.__dict__[name] = attr = getattr(mod, name)
        return attr


    def __repr__(self):
        return "<dynamic-module '%s'>" % self.__name__


    def RaiseAssignments(self):
        """
        After this method is called, creation of new attributes will raise
        AttributeError.

        This is meanly used to find unintended assignments while debugging.
        """
        def __setattr__(self, name, value):
            if not name in self.__dict__:
                raise AttributeError("Assignment to new attribute %s" % name)
            object.__setattr__(self, name, value)
        self.__class__.__setattr__ = __setattr__


    def Main(self):
        if Cli.args.install:
            return
        if Cli.args.translate:
            eg.LanguageEditor()
        elif Cli.args.pluginFile:
            eg.PluginInstall.Import(Cli.args.pluginFile)
            return
        else:
            eg.Init.InitGui()
        if eg.debugLevel:
            eg.Init.ImportAll()
        eg.Tasklet(eg.app.MainLoop)().run()
        stackless.run()


eg = DynamicModule()
# This is only here to make pylint happy. It is never really imported
if "pylint" in sys.modules:
    from Init import ImportAll
    ImportAll()
    from StaticImports import *
    from Core import *
import Core
if eg.debugLevel:
    eg.RaiseAssignments()


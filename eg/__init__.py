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

import sys, os
import stackless

import Cli
from Utils import *

# This is only here to make pylint happy. It is never really imported
if "pylint" in sys.modules:
    from StaticImports import *


class DynamicModule(object):

    def __init__(self):
        mod = sys.modules[__name__]
        self.__dict__ = mod.__dict__
        self.__orignal_module__ = mod
        sys.modules[__name__] = self

        import __builtin__
        __builtin__.eg = self


    def __getattr__(self, name):
        try:
            mod = __import__("eg.Classes." + name, None, None, [name], 0)
        except ImportError:
            raise AttributeError("'eg' object has not attribute '%s'" % name)
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
        else:
            eg.Init.InitGui()
        eg.Tasklet(eg.app.MainLoop)().run()
        stackless.run()


eg = DynamicModule()
import Core
if eg.debugLevel:
    eg.RaiseAssignments()


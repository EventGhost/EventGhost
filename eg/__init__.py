# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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

import sys, os
from types import ModuleType
import stackless

import Cli

## This is only here to make pylint happy. It is never really imported
#if "pylint" in sys.modules:
#    from Classes import *
#    import Core
#    import StaticImports
    

class LazyModule(ModuleType):
    
    def __init__(self):
        #import sys
        
        self._ORIGINAL_MODULE = sys.modules[__name__]
        # let ourself look like a package
        self.__name__ = __name__
        self.__path__ = __path__
        self.__file__ = __file__
        sys.modules[__name__] = self
        
        import __builtin__
        __builtin__.eg = self

        
    def __getattr__(self, name):
        mod = __import__("eg.Classes." + name, None, None, [name], 0)
        self.__dict__[name] = attr = getattr(mod, name)
        return attr
    
    
    def __repr__(self):
        return "<eg>"


    def Main(self):
        if Cli.args.install:
            return
        if Cli.args.translate:
            eg.LanguageEditor()
        else:
            eg.Init.InitGui()
        #eg.app.MainLoop()
        eg.Tasklet(eg.app.MainLoop)().run()
        stackless.run()
        print "mainloop end"


eg = LazyModule()
import Utils
for attrName in Utils.__all__:
    setattr(eg, attrName, getattr(Utils, attrName))
import Core

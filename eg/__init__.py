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

import sys

_ORIGINAL_MODULE = sys.modules[__name__]

class _ModuleProxy(object):
    
    def __init__(self):
        self.__name__ = __name__
        self.__path__ = _ORIGINAL_MODULE.__path__
        self.__file__ = _ORIGINAL_MODULE.__file__
        sys.modules["eg"] = self
        
        import __builtin__
        __builtin__.__dict__["eg"] = self

        
    def __getattr__(self, name):
        mod = __import__("eg.Classes." + name, None, None, [name], 0)
        self.__dict__[name] = attr = getattr(mod, name)
        return attr
    
    def __repr__(self):
        return "eg"


_eg = _ModuleProxy()

import os
if os.path.basename(sys.argv[0]) == "sphinx-build-script.py":
    _eg.Init()
    
# this is only here to make pylint happy
if False:
    from StaticImports import *
    

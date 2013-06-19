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

# start the main program
import sys
import imp
from os.path import dirname, abspath

if hasattr(sys, "frozen"):
    path = dirname(sys.executable)
else:
    path = abspath(dirname(sys.argv[0])) 
    
imp.load_source("Main", path + "/eg/Main.py")

print "should never come here"
# The "imports" module file is created by the tools/MakeImports.py script
# and is located in the "tools" directory also.
# It includes all modules the program might need. This way we force py2exe
# to include them in the distribution.
import imports


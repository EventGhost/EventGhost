# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import sys

if hasattr(sys, "frozen"):
    from os.path import dirname
    FSE = sys.getfilesystemencoding()
    filePath = sys.executable.encode(FSE) if isinstance(sys.executable, unicode) else sys.executable
    sys.path.append(dirname(filePath))
#    sys.path.append(dirname(sys.executable.encode('mbcs')))

if len(sys.argv) > 2 and sys.argv[1] == "-execfile":
    import imp
    import os
    filename = sys.argv[2]
    # we need a reference to the old module, otherwise we get garbage collected
    oldMainModule = sys.modules['__main__']
    # Create a new module to serve as __main__
    mainModule = imp.new_module('__main__')
    mainModule.__file__ = filename
    mainModule.__builtins__ = sys.modules['__builtin__']
    sys.modules['__main__'] = mainModule
    # Set sys.argv and the path element properly.
    sys.argv = sys.argv[2:]
    sys.path.append(os.path.dirname(filename))
    try:
        source = open(filename, 'rU').read()
    except IOError:
        raise Exception("No file to run: %r" % filename)
    exec compile(source, filename, "exec") in mainModule.__dict__
else:
    if __name__ == "__main__":
        from multiprocessing import freeze_support
        freeze_support()
        import __main__
        __main__.isMain = True
        import eg
        eg.Main()

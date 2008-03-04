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

import sys
import os
import imp
import traceback
import inspect
import weakref

    
class PythonScript(eg.ActionClass):
    name = "Python Script"
    description = "Full featured Python script." 
    iconFile = "icons/PythonScript"

    class ConfigDefaults:
        size = (600, 420)
        position = (10, 10)
    config = eg.GetConfig("plugins.EventGhost.PythonScript", ConfigDefaults)

        
    def GetLabel(self, pythonstring=None):
        return self.name


    def Configure(self, sourceCode=""):
        panel = eg.ConfigPanel(self, resizeable=True)
        editCtrl = eg.PythonEditorCtrl(panel, value=sourceCode)
        panel.sizer.Add(editCtrl, 1, wx.EXPAND)
        panel.FinishSetup()
        panel.dialog.SetPosition(self.config.position)
        panel.dialog.SetSize(self.config.size)
        while panel.Affirmed():
            panel.SetResult(editCtrl.GetValue())
        if not panel.dialog.IsMaximized():
            self.config.size = panel.dialog.GetSizeTuple()
            self.config.position = panel.dialog.GetPositionTuple()
        

    class Compile:
        idCounter = 0
        scriptDict = weakref.WeakValueDictionary()

        def __init__(self, sourceCode=""):
            id = self.__class__.idCounter
            self.__class__.idCounter += 1
            mod = imp.new_module(str(id))
            self.mod = mod
            self.sourceCode = sourceCode
            try:
                self.code = compile(sourceCode + "\n", str(id), "exec")
            except:
                self.code = None
                eg.PrintError("Error compiling script.")
                self.PrintTraceback()
            self.scriptDict[id] = self
            
            
        def __call__(self):
            if self.code is None:
                self.__init__(self.sourceCode)
                if self.code is None:
                    return
            mod = self.mod
            oldResult = eg.result
            mod.result = oldResult
            try:
                exec(self.code, mod.__dict__)
            except SystemExit:
                pass
            except:
                self.PrintTraceback()
            if eg.result is not oldResult:
                return eg.result
            else:
                return mod.result


        def PrintTraceback(self):
            eg.PrintError("Traceback (most recent call last):")
            lines = self.sourceCode.splitlines()
            tb_type, tb_value, tb_traceback = sys.exc_info() 
            for entry in traceback.extract_tb(tb_traceback)[1:]:
                file, linenum, func, source = entry
                try:
                    filenum = int(file)
                except:
                    filenum = None
                if source is None and filenum is not None:
                    eg.PrintError(
                        '  Python script "%s", line %d, in %s' % (
                            file, linenum, func
                        )
                    )
                    lines = self.scriptDict[int(file)].sourceCode.splitlines()
                    eg.PrintError('    ' + lines[linenum-1].lstrip())
                else:
                    eg.PrintError(
                        '  File "%s", line %d, in %s' % (
                            file, linenum, func
                        )
                    )
                    if source is not None:
                        eg.PrintError('    ' + source.lstrip())
            name = tb_type if type(tb_type) == type("") else tb_type.__name__
            eg.PrintError(str(name) + ': ' + str(tb_value))
                
            
        @eg.LogIt
        def __del__(self):
            pass
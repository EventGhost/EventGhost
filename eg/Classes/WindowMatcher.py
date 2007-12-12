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


from re import compile, escape
from types import StringTypes
from time import clock
from win32gui import EnumWindows, EnumChildWindows, IsWindowVisible
from win32gui import GetWindowText, GetClassName
from eg.WinAPI.Utils import GetHwndProcessName


class MatchSingleChar:
    # just a named object
    pass
    
    
class MatchAny:
    # just a named object
    pass
    

def CompileString(pattern):
    if pattern is None:
        return None
    res = []
    startPos = 0
    tmp = ""
    endPos = pattern.find('{')
    useRegex = False
    while endPos != -1:
        tmp += pattern[startPos:endPos]
        endPos += 1
        if len(pattern)-1 < endPos:
            raise SyntaxError("unmatched curly-brace at end")
        elif pattern[endPos] == "{":
            tmp += "{"
            endPos += 1
        else:
            wordStartPos = endPos
            endPos = pattern.find('}', wordStartPos)
            if endPos == -1:
                raise SyntaxError("unmatched curly-brace")
            word = pattern[wordStartPos:endPos]
            if word == "*":
                if tmp != "":
                    res.append(tmp)
                    tmp = ""
                useRegex = True
                res.append(MatchAny)
            elif word == "?":
                if tmp != "":
                    res.append(tmp)
                    tmp = ""
                useRegex = True
                res.append(MatchSingleChar)
            endPos += 1
        startPos = endPos
        endPos = pattern.find('{', startPos)
    tmp += pattern[startPos:]
    res.append(tmp)
    if useRegex:
        pattern = "^"
        for tmp in res:
            if type(tmp) in StringTypes:
                pattern += escape(tmp)
            elif tmp == MatchSingleChar:
                pattern += "."
            elif tmp == MatchAny:
                pattern += ".*"
        pattern += "$"
        return compile(pattern).match
    else:
        return lambda s: s == pattern
            
    

class WindowMatcher:
    """
    Returns a list of window handles matching a number of criteria.
    
    An instance of this class can be used as a better win32api.FindWindow
    replacement. It allows to confine the windows to find by the process name,
    window name, window class and some other criteria. Wildcards can be used 
    in the search strings. The idea behind this class is to compile the 
    parameters at the instantiation of the class to some fast regular 
    expressions and do the actual enumeration of all desktop windows, if the
    the instance is called.
    """
    
    def __init__(
        self, 
        program, 
        winName=None, 
        winClass=None, 
        childName=None,
        childClass=None, 
        matchNum=0, 
        includeInvisible=False, 
        timeout=0, 
        dummyArg = None,
    ):
        self.timeout = timeout
        self.matchNum = matchNum or 0
        dummy = (lambda x: True)
        if not includeInvisible:
            self.invisibleMatch = IsWindowVisible
        else:
            self.invisibleMatch = dummy
            
        def GetMatcher(value):
            if value is not None:
                return CompileString(value.encode(eg.systemEncoding)) 
            else:
                return dummy
            
        if program:
            program = program.upper()
        self.program = program
        self.programMatch = GetMatcher(program)
        self.winNameMatch = GetMatcher(winName)
        self.winClassMatch = GetMatcher(winClass)
        self.scanChilds = False
        if (childName is not None) or (childClass is not None):
            self.scanChilds = True
            self.childNameMatch = GetMatcher(childName)
            self.childClassMatch = GetMatcher(childClass)
        if matchNum:
            self.Enumerate = self.FindMatch
        else:
            self.Enumerate = self.Find
        if timeout > 0:
            self.__call__ = self.FindWait
        else:
            self.__call__ = self.Enumerate
    
    
    def EnumWindowsProc(self, hwnd, add):
        if not self.invisibleMatch(hwnd):
            return True
        if not self.winClassMatch(GetClassName(hwnd)):
            return True
        if not self.winNameMatch(GetWindowText(hwnd)):
            return True
        add(hwnd)
        return True
    
    
    def EnumChildsProc(self, hwnd, add):
        if not self.invisibleMatch(hwnd):
            return True
        if not self.childClassMatch(GetClassName(hwnd)):
            return True
        if not self.childNameMatch(GetWindowText(hwnd)):
            return True
        add(hwnd)
        return True
        
        
    def Find(self):
        topWindowsHwnds = []
        EnumWindows(self.EnumWindowsProc, topWindowsHwnds.append)
        if self.program:
            topWindowsHwnds = [
                hwnd for hwnd in topWindowsHwnds 
                    if self.programMatch(GetHwndProcessName(hwnd).upper())
            ]
        if not self.scanChilds:
            return topWindowsHwnds
        childHwnds = []
        for hwnd in topWindowsHwnds:
            EnumChildWindows(hwnd, self.EnumChildsProc, childHwnds.append)
        return childHwnds


    def FindMatch(self):
        hwnds = self.Find()
        matchNum = self.matchNum
        if matchNum and len(hwnds) >= matchNum:
            return [hwnds[matchNum-1]]
        else:
            return []
        

    def FindWait(self):
        endtime = clock() + self.timeout
        while 1:
            hwnds = self.Enumerate()
            if hwnds:
                return hwnds
            if clock() >= endtime:
                return []
            eg.Wait(0.05)
                
        
    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass
                
                

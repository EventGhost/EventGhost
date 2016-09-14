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

from re import compile, escape
from time import clock
from types import StringTypes

# Local imports
import eg
from eg.WinApi.Utils import GetWindowProcessName
from eg.WinApi import (
    GetTopLevelWindowList, GetWindowChildsList, GetWindowText, GetClassName
)

class WindowMatcher:
    """
    Returns a list of window handles matching a number of criteria.

    An instance of this class can be used as a better win32.FindWindow
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
        self.includeInvisible = bool(includeInvisible)

        dummy = (lambda x: True)

        def GetMatcher(value):
            if value is not None:
                return CompileString(value)
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

    def __call__(self):
        raise NotImplementedError

    if eg.debugLevel:
        @eg.LogIt
        def __del__(self):
            pass

    def Find(self):
        winClassMatch = self.winClassMatch
        winNameMatch = self.winNameMatch
        programMatch = self.programMatch
        includeInvisible = self.includeInvisible
        topWindowsHwnds = [
            hwnd for hwnd in GetTopLevelWindowList(includeInvisible)
            if (
                winClassMatch(GetClassName(hwnd)) and
                winNameMatch(GetWindowText(hwnd))
            )
        ]
        if self.program:
            topWindowsHwnds = [
                hwnd for hwnd in topWindowsHwnds
                if programMatch(GetWindowProcessName(hwnd).upper())
            ]
        if not self.scanChilds:
            return topWindowsHwnds
        childClassMatch = self.childClassMatch
        childNameMatch = self.childNameMatch
        childHwnds = [
            childHwnd for parentHwnd in topWindowsHwnds
            for childHwnd in GetWindowChildsList(
                parentHwnd, includeInvisible
            ) if (
                childClassMatch(GetClassName(childHwnd)) and
                childNameMatch(GetWindowText(childHwnd))
            )
        ]
        return childHwnds

    def FindMatch(self):
        hwnds = self.Find()
        matchNum = self.matchNum
        if matchNum and len(hwnds) >= matchNum:
            return [hwnds[matchNum - 1]]
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


class MatchAny:
    # just a named object
    pass


class MatchSingleChar:
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
        if len(pattern) - 1 < endPos:
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

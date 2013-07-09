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

__all__ = ["Bunch", "NotificationHandler", "LogIt", "LogItWithReturn",
    "TimeIt", "AssertNotMainThread", "AssertNotActionThread", "ParseString",
    "SetDefault", "EnsureVisible", "VBoxSizer", "HBoxSizer", "EqualizeWidths",
    "AsTasklet", "ExecFile", "GetTopLevelWindow",
]

import eg
import wx
import sys
import threading
import time
import inspect
from types import ClassType
from functools import update_wrapper
from docutils.core import publish_parts as ReSTPublishParts
from docutils.writers.html4css1 import Writer



class Bunch(object):
    """
    Universal collection of a bunch of named stuff.

    Often we want to just collect a bunch of stuff together, naming each
    item of the bunch. A dictionary is OK for that; however, when names are
    constants and to be used just like variables, the dictionary-access syntax
    ("if bunch['squared'] > threshold", etc) is not maximally clear. It takes
    very little effort to build a little class, as in this 'Bunch', that will
    both ease the initialisation task and provide elegant attribute-access
    syntax ("if bunch.squared > threshold", etc).

    Usage is simple::

        point = eg.Bunch(x=100, y=200)

        # and of course you can read/write the named
        # attributes you just created, add others, del
        # some of them, etc, etc:
        point.squared = point.x * point.y
        if point.squared > threshold:
            point.isok = True
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)



class NotificationHandler(object):
    __slots__ = ["value", "listeners"]

    def __init__(self, initialValue=None):
        self.value = initialValue
        self.listeners = []



def GetMyRepresentation(value):
    """
    Give a shorter representation of some wx-objects. Returns normal repr()
    for everything else. Also adds a "=" sign at the beginning to make it
    useful as a "formatvalue" function for inspect.formatargvalues().
    """
    typeString = repr(type(value))
    if typeString.startswith("<class 'wx._core."):
        return "=<wx.%s>" % typeString[len("<class 'wx._core."): -2]
    if typeString.startswith("<class 'wx._controls."):
        return "=<wx.%s>" % typeString[len("<class 'wx._controls."): -2]
    return "=" + repr(value)


def GetFuncArgString(func, args, kwargs):
    classname = ""
    argnames = inspect.getargspec(func)[0]
    start = 0
    if argnames:
        if argnames[0] == "self":
            classname = args[0].__class__.__name__ + "."
            start = 1
    res = []
    append = res.append
    for key, value in zip(argnames, args)[start:]:
        append(str(key) + GetMyRepresentation(value))
    for key, value in kwargs.items():
        append(str(key) + GetMyRepresentation(value))
    fname = classname + func.__name__
    return fname, "(" + ", ".join(res) + ")"


def LogIt(func):
    """Logs the function call, if eg.debugLevel is set."""
    if not eg.debugLevel:
        return func

    if func.func_code.co_flags & 0x20:
        raise TypeError("Can't wrap generator function")

    def LogItWrapper(*args, **kwargs):
        funcName, argString = GetFuncArgString(func, args, kwargs)
        eg.PrintDebugNotice(funcName + argString)
        return func(*args, **kwargs)
    return update_wrapper(LogItWrapper, func)


def LogItWithReturn(func):
    """Logs the function call and return, if eg.debugLevel is set."""
    if not eg.debugLevel:
        return func

    def LogItWithReturnWrapper(*args, **kwargs):
        funcName, argString = GetFuncArgString(func, args, kwargs)
        eg.PrintDebugNotice(funcName + argString)
        result = func(*args, **kwargs)
        eg.PrintDebugNotice(funcName + " => " + repr(result))
        return result
    return update_wrapper(LogItWithReturnWrapper, func)


def TimeIt(func):
    """ Decorator to measure the execution time of a function.

    Will print the time to the log.
    """
    if not eg.debugLevel:
        return func
    def TimeItWrapper(*args, **kwargs):
        startTime = time.clock()
        funcName, _ = GetFuncArgString(func, args, kwargs)
        res = func(*args, **kwargs)
        eg.PrintDebugNotice(funcName + " :" + repr(time.clock() - startTime))
        return res
    return update_wrapper(TimeItWrapper, func)


def AssertNotMainThread(func):
    if not eg.debugLevel:
        return func
    def AssertWrapper(*args, **kwargs):
        assert eg.mainThread == threading.currentThread()
        return func(*args, **kwargs)
    return update_wrapper(AssertWrapper, func)


def AssertNotActionThread(func):
    if not eg.debugLevel:
        return func
    def AssertWrapper(*args, **kwargs):
        assert eg.actionThread == threading.currentThread()
        return func(*args, **kwargs)
    return update_wrapper(AssertWrapper, func)


def AsTasklet(func):
    def Wrapper(*args, **kwargs):
        eg.Tasklet(func)(*args, **kwargs).run()
    return update_wrapper(Wrapper, func)


def ParseString(text, filterFunc=None):
    start = 0
    chunks = []
    last = len(text) - 1
    while 1:
        pos = text.find('{', start)
        if pos < 0:
            break
        if pos == last:
            break
        chunks.append(text[start:pos])
        if text[pos+1] == '{':
            chunks.append('{')
            start = pos + 2
        else:
            start = pos + 1
            end = text.find('}', start)
            if end == -1:
                raise SyntaxError("unmatched bracket")
            word = text[start:end]
            res = None
            if filterFunc:
                res = filterFunc(word)
            if res is None:
                res = eval(word, {}, eg.globals.__dict__)
            chunks.append(unicode(res))
            start = end + 1
    chunks.append(text[start:])
    return "".join(chunks)



USER_CLASSES = (type, ClassType)

def SetDefault(targetCls, defaultCls):
    targetDict = targetCls.__dict__
    for defaultKey, defaultValue in defaultCls.__dict__.iteritems():
        if defaultKey not in targetDict:
            setattr(targetCls, defaultKey, defaultValue)
        elif type(defaultValue) in USER_CLASSES:
            SetDefault(targetDict[defaultKey], defaultValue)


def GetTopLevelWindow(window):
    """
    Returns the top level parent window of a wx.Window. This is in most
    cases a wx.Dialog or wx.Frame.
    """
    result = window
    while True:
        parent = result.GetParent()
        if parent is None:
            return result
        result = parent


def EnsureVisible(window, center=False):
    """
    Ensures the given wx.TopLevelWindow is visible on the screen.
    Moves and resizes it if necessary.
    """
    from eg.WinApi.Dynamic import (
        GetMonitorInfo, MONITORINFO,
        sizeof, byref, RECT, MonitorFromRect, MONITOR_DEFAULTTONULL, 
        GetWindowRect, MONITOR_DEFAULTTONEAREST, MonitorFromWindow
    )
    windowRect = RECT()
    hwnd = window.GetHandle()
    GetWindowRect(window.GetHandle(), byref(windowRect))
   # hMonitor = MonitorFromRect(byref(windowRect), MONITOR_DEFAULTTONULL)
    #if hMonitor:
    #    return
    parent = window.GetParent()
    if parent:
        hwnd = parent.GetHandle()
    hMonitor = MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)
    
    monInfo = MONITORINFO()
    monInfo.cbSize = sizeof(MONITORINFO)
    
    GetMonitorInfo(hMonitor, byref(monInfo))
    displayRect = monInfo.rcWork
    w = displayRect.right - displayRect.left
    h = displayRect.bottom - displayRect.top
    
    left = windowRect.left
    right = windowRect.right
    top = windowRect.top
    bottom = windowRect.bottom
    
    # shift the window horizontally into the display area
    if left < displayRect.left:
        right += (displayRect.left - left)
        left = displayRect.left
        if right > displayRect.right:
            right = displayRect.right
    elif right > displayRect.right:
        left += (displayRect.right - right)
        right = displayRect.right
        if left < displayRect.left:
            left = displayRect.left

    # shift the window vertically into the display area
    if top < displayRect.top:
        bottom += (displayRect.top - top)
        top = displayRect.top
        if bottom > displayRect.bottom:
            bottom = displayRect.bottom
    elif bottom > displayRect.bottom:
        top += (displayRect.bottom - bottom)
        bottom = displayRect.bottom
        if top < displayRect.top:
            top = displayRect.top

    # set the new position and size
    window.SetRect((left, top, right - left, bottom - top))


class VBoxSizer(wx.BoxSizer): #IGNORE:R0904

    def __init__(self, *items):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.AddMany(items)



class HBoxSizer(wx.BoxSizer): #IGNORE:R0904

    def __init__(self, *items):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.AddMany(items)


def EqualizeWidths(ctrls):
    maxWidth = max((ctrl.GetBestSize()[0] for ctrl in ctrls))
    for ctrl in ctrls:
        ctrl.SetMinSize((maxWidth, -1))


DOC_WRITER_TEMPLATE = """\
%(head_prefix)s
%(head)s
%(stylesheet)s
%(body_prefix)s
%(body_pre_docinfo)s
%(docinfo)s
%(body)s
%(body_suffix)s
"""

class MyHtmlDocWriter(Writer):

    def apply_template(self):
        return DOC_WRITER_TEMPLATE % self.interpolation_dict()


HTML_DOC_WRITER = MyHtmlDocWriter()


def DecodeReST(source):
    #print repr(source)
    res = ReSTPublishParts(
        source=PrepareDocstring(source),
        writer=HTML_DOC_WRITER,
        settings_overrides={"stylesheet_path": ""}
    )
    #print repr(res)
    return res['body']


def PrepareDocstring(s):
    """
    Convert a docstring into lines of parseable reST.  Return it as a list of
    lines usable for inserting into a docutils ViewList (used as argument
    of nested_parse().)  An empty line is added to act as a separator between
    this docstring and following content.
    """
    lines = s.expandtabs().splitlines()
    # Find minimum indentation of any non-blank lines after first line.
    margin = sys.maxint
    for line in lines[1:]:
        content = len(line.lstrip())
        if content:
            indent = len(line) - content
            margin = min(margin, indent)
    # Remove indentation.
    if lines:
        lines[0] = lines[0].lstrip()
    if margin < sys.maxint:
        for i in range(1, len(lines)):
            lines[i] = lines[i][margin:]
    # Remove any leading blank lines.
    while lines and not lines[0]:
        lines.pop(0)
    # make sure there is an empty line at the end
    if lines and lines[-1]:
        lines.append('')
    return "\n".join(lines)


def GetFirstParagraph(text):
    """
    Return the first paragraph of a description string.

    The string can be encoded in HTML or reStructuredText.
    The paragraph is returned as HTML.
    """
    text = text.lstrip()
    pos = text.find("<rst>")
    if pos != -1:
        text = text[pos+5:]
        text = DecodeReST(text)
        start = text.find("<p>")
        end = text.find("</p>")
        return text[start+3:end].replace("\n", " ")
    else:
        result = ""
        for line in text.splitlines():
            if line == "":
                break
            result += " " + line
        return ' '.join(result.split())


def ExecFile(filename, globals=None, locals=None):
    """
    Replacement for the Python built-in execfile() function, but handles
    unicode filenames right.
    """
    return execfile(
        filename.encode(sys.getfilesystemencoding()),
        globals,
        locals
    )


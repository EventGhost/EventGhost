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

__all__ = ["Bunch", "NotificationHandler", "LogIt", "LogItWithReturn",
    "TimeIt", "AssertNotMainThread", "AssertNotActionThread", "ParseString",
    "SetDefault", "EnsureVisible", "AsGreenlet",
    "VBoxSizer", "HBoxSizer", "EqualizeWidths",
]
    
import eg
import wx
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


def AsGreenlet(func):
    def Wrapper(*args, **kwargs):
        greenlet = eg.Greenlet(func)
        return greenlet.switch(*args, **kwargs)
    return update_wrapper(Wrapper, func)


def EnsureVisible(window):
    """ 
    Ensures the given wx.TopLevelWindow is visible on the screen. 
    Moves and resizes it if necessary.
    """
    # get all display rectangles
    displayRects = [
        wx.Display(i).GetClientArea() 
        for i in range(wx.Display.GetCount())
    ]
            
    # wx.Display.GetFromPoint doesn't take GetClientArea into account, so
    # we have to define our own function
    def GetDisplayFromPoint(point):
        for displayNum, displayRect in enumerate(displayRects):
            if displayRect.Contains(point):
                return displayNum
        else:
            return wx.NOT_FOUND
        
    windowRect = window.GetScreenRect()
    
    # if the entire window is contained on the display, take a quick exit
    if (
        GetDisplayFromPoint(windowRect.TopLeft) != wx.NOT_FOUND
        and GetDisplayFromPoint(windowRect.BottomRight) != wx.NOT_FOUND
    ):
        return
    
    # get the nearest display
    displayNum = wx.Display.GetFromWindow(window)
    if displayNum == wx.NOT_FOUND:
        displayNum = 0
        parent = window.GetParent()
        if parent:
            displayNum = wx.Display.GetFromWindow(parent)
    
    displayRect = displayRects[displayNum]

    # shift the dialog horizontally into the display area
    if windowRect.Left < displayRect.Left:
        windowRect.Right += (displayRect.Left - windowRect.Left)
        windowRect.Left = displayRect.Left
        if windowRect.Right > displayRect.Right:
            windowRect.Right = displayRect.Right
    elif windowRect.Right > displayRect.Right:
        windowRect.Left += (displayRect.Right - windowRect.Right)
        windowRect.Right = displayRect.Right
        if windowRect.Left < displayRect.Left:
            windowRect.Left = displayRect.Left
            
    # shift the dialog vertically into the display area
    if windowRect.Top < displayRect.Top:
        windowRect.Bottom += (displayRect.Top - windowRect.Top)
        windowRect.Top = displayRect.Top
        if windowRect.Bottom > displayRect.Bottom:
            windowRect.Bottom = displayRect.Bottom
    elif windowRect.Bottom > displayRect.Bottom:
        windowRect.Top += (displayRect.Bottom - windowRect.Bottom)
        windowRect.Bottom = displayRect.Bottom
        if windowRect.Top < displayRect.Top:
            windowRect.Top = displayRect.Top
            
    # set the new position and size
    window.SetRect(windowRect)



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
        source=source, 
        writer=HTML_DOC_WRITER, 
        settings_overrides={"stylesheet_path": ""}
    )
    #print repr(res)
    return res['body']


def GetFirstParagraph(text):
    """
    Return the first paragraph of a description string.
    
    The string can be encoded in HTML or reStructuredText.
    The paragraph is returned as HTML.
    """
    text = text.lstrip()
    pos = text.find("<rst>")
    if pos != -1:
        text = text[pos+5:].lstrip()
        text = DecodeReST(text)
        start = text.find("<p>")
        end = text.find("</p>")
        return text[start+3:end]
    else:
        result = ""
        for line in text.splitlines():
            if line == "":
                break
            result += " " + line
        return result


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

import inspect
import os
import sys
import threading
import time
import warnings
import wx
from CommonMark import commonmark
from ctypes import c_ulonglong, windll
from datetime import datetime as dt, timedelta as td
from docutils.core import publish_parts as ReSTPublishParts
from docutils.writers.html4css1 import Writer
from functools import update_wrapper
from os.path import abspath, dirname, exists, join
from types import ClassType

# Local imports
import eg

# Make sure our deprecation warnings will be shown
warnings.filterwarnings(
    action="always",
    category=DeprecationWarning,
    module='^eg\..*'
)

__all__ = [
    "Bunch", "NotificationHandler", "LogIt", "LogItWithReturn", "TimeIt",
    "AssertInMainThread", "AssertInActionThread", "ParseString", "SetDefault",
    "EnsureVisible", "VBoxSizer", "HBoxSizer", "EqualizeWidths", "AsTasklet",
    "ExecFile", "GetTopLevelWindow",
]

USER_CLASSES = (type, ClassType)

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


class HBoxSizer(wx.BoxSizer):  #IGNORE:R0904
    def __init__(self, *items):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.AddMany(items)


class MyHtmlDocWriter(Writer):
    def apply_template(self):
        return """\
%(head_prefix)s
%(head)s
%(stylesheet)s
%(body_prefix)s
%(body_pre_docinfo)s
%(docinfo)s
%(body)s
%(body_suffix)s
""" % self.interpolation_dict()

HTML_DOC_WRITER = MyHtmlDocWriter()


class NotificationHandler(object):
    __slots__ = ["listeners"]

    def __init__(self):
        self.listeners = []


class VBoxSizer(wx.BoxSizer):  #IGNORE:R0904
    def __init__(self, *items):
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        self.AddMany(items)


def AppUrl(description, url):
    if url:
        txt = '<p><div align=right><i><font color="#999999" size=-1>%s <a href="%s">%s</a>.</font></i></div></p>' % (
            eg.text.General.supportSentence,
            url,
            eg.text.General.supportLink
        )
    else:
        return description
    if description.startswith("<md>"):
        description = description[4:]
        description = DecodeMarkdown(description)
    elif description.startswith("<rst>"):
        description = description[5:]
        description = DecodeReST(description)
    return description + txt

def AssertInActionThread(func):
    if not eg.debugLevel:
        return func

    def AssertWrapper(*args, **kwargs):
        if eg.actionThread._ThreadWorker__thread != threading.currentThread():
            raise AssertionError(
                "Called outside ActionThread: %s() in %s" %
                (func.__name__, func.__module__)
            )
        return func(*args, **kwargs)
        return func(*args, **kwargs)

    return update_wrapper(AssertWrapper, func)

def AssertInMainThread(func):
    if not eg.debugLevel:
        return func

    def AssertWrapper(*args, **kwargs):
        if eg.mainThread != threading.currentThread():
            raise AssertionError(
                "Called outside MainThread: %s in %s" %
                (func.__name__, func.__module__)
            )
        return func(*args, **kwargs)

    return update_wrapper(AssertWrapper, func)

def AsTasklet(func):
    def Wrapper(*args, **kwargs):
        eg.Tasklet(func)(*args, **kwargs).run()
    return update_wrapper(Wrapper, func)

def CollectGarbage():
    import gc
    #gc.set_debug(gc.DEBUG_SAVEALL)
    #gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
    from pprint import pprint
    print "threshold:", gc.get_threshold()
    print "unreachable object count:", gc.collect()
    garbageList = gc.garbage[:]
    for i, obj in enumerate(garbageList):
        print "Object Num %d:" % i
        pprint(obj)
        #print "Referrers:"
        #print(gc.get_referrers(o))
        #print "Referents:"
        #print(gc.get_referents(o))
    print "Done."
    #print "unreachable object count:", gc.collect()
    #from pprint import pprint
    #pprint(gc.garbage)

def DecodeMarkdown(source):
    return commonmark(source)

def DecodeReST(source):
    #print repr(source)
    res = ReSTPublishParts(
        source=PrepareDocstring(source),
        writer=HTML_DOC_WRITER,
        settings_overrides={"stylesheet_path": ""}
    )
    #print repr(res)
    return res['body']

def EnsureVisible(window):
    """
    Ensures the given wx.TopLevelWindow is visible on the screen.
    Moves and resizes it if necessary.
    """
    from eg.WinApi.Dynamic import (
        sizeof, byref, GetMonitorInfo, MonitorFromWindow, GetWindowRect,
        MONITORINFO, RECT, MONITOR_DEFAULTTONEAREST,
        # MonitorFromRect, MONITOR_DEFAULTTONULL,
    )

    hwnd = window.GetHandle()
    windowRect = RECT()
    GetWindowRect(hwnd, byref(windowRect))

    #hMonitor = MonitorFromRect(byref(windowRect), MONITOR_DEFAULTTONULL)
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

def EqualizeWidths(ctrls):
    maxWidth = max((ctrl.GetBestSize()[0] for ctrl in ctrls))
    for ctrl in ctrls:
        ctrl.SetMinSize((maxWidth, -1))

def ExecFile(filename, globals=None, locals=None):
    """
    Replacement for the Python built-in execfile() function, but handles
    unicode filenames right.
    """
    FSE = sys.getfilesystemencoding()
    flnm = filename.encode(FSE) if isinstance(filename, unicode) else filename
    return execfile(flnm, globals, locals)

def GetBootTimestamp(unix_timestamp = True):
    """
    Returns the time of the last system boot.
    If unix_timestamp == True, result is a unix temestamp.
    Otherwise it is in human readable form.
    """
    now = time.time()
    GetTickCount64 = windll.kernel32.GetTickCount64
    GetTickCount64.restype = c_ulonglong
    up = GetTickCount64() / 1000.0
    if not unix_timestamp:
        st = str(dt.fromtimestamp(now - up))
        return st if "." not in st else st[:st.index(".")]
    return now - up

def GetClosestLanguage():
    """
    Returns the language file closest to system locale.
    """
    langDir = join(dirname(abspath(sys.executable)), "languages")
    if exists(langDir):
        locale = wx.Locale()
        name = locale.GetLanguageCanonicalName(locale.GetSystemLanguage())
        if exists(join(langDir, name + ".py")):
            return name
        else:
            for f in [f for f in os.listdir(langDir) if f.endswith(".py")]:
                if f.startswith(name[0:3]):
                    return f[0:5]
    return "en_EN"

def GetFirstParagraph(text):
    """
    Return the first paragraph of a description string.

    The string can be encoded in HTML or reStructuredText.
    The paragraph is returned as HTML.
    """
    text = text.lstrip()
    if text.startswith("<md>"):
        text = text[4:]
        text = DecodeMarkdown(text)
        start = text.find("<p>")
        end = text.find("</p>")
        return text[start + 3:end].replace("\n", " ")
    elif text.startswith("<rst>"):
        text = text[5:]
        text = DecodeReST(text)
        start = text.find("<p>")
        end = text.find("</p>")
        return text[start + 3:end].replace("\n", " ")
    else:
        result = ""
        for line in text.splitlines():
            if line == "":
                break
            result += " " + line
        return ' '.join(result.split())

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
        elif isinstance(parent, wx.TopLevelWindow):
            return parent
        result = parent

def GetUpTime(seconds = True):
    """
    Returns a runtime of system in seconds.
    If seconds == False, returns the number of days, hours, minutes and seconds.
    """
    GetTickCount64 = windll.kernel32.GetTickCount64
    GetTickCount64.restype = c_ulonglong
    ticks = GetTickCount64() / 1000.0
    if not seconds:
        delta = str(td(seconds = ticks))
        return delta if "." not in delta else delta[:delta.index(".")]
    return ticks

def IsVista():
    """
    Determine if we're running Vista or higher.
    """
    warnings.warn(
        "eg.Utils.IsVista() is deprecated. "
        "Use eg.WindowsVersion >= 'Vista' instead",
        DeprecationWarning,
        stacklevel=2
    )
    return eg.WindowsVersion >= 'Vista'

def IsXP():
    """
    Determine if we're running XP or higher.
    """
    warnings.warn(
        "eg.Utils.IsXP() is deprecated. "
        "Use eg.WindowsVersion >= 'XP' instead",
        DeprecationWarning,
        stacklevel=2
    )
    return eg.WindowsVersion >= 'XP'

def LogIt(func):
    """
    Logs the function call, if eg.debugLevel is set.
    """
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
    """
    Logs the function call and return, if eg.debugLevel is set.
    """
    if not eg.debugLevel:
        return func

    def LogItWithReturnWrapper(*args, **kwargs):
        funcName, argString = GetFuncArgString(func, args, kwargs)
        eg.PrintDebugNotice(funcName + argString)
        result = func(*args, **kwargs)
        eg.PrintDebugNotice(funcName + " => " + repr(result))
        return result
    return update_wrapper(LogItWithReturnWrapper, func)

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
        if text[pos + 1] == '{':
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

def PrepareDocstring(docstring):
    """
    Convert a docstring into lines of parseable reST.  Return it as a list of
    lines usable for inserting into a docutils ViewList (used as argument
    of nested_parse()). An empty line is added to act as a separator between
    this docstring and following content.
    """
    lines = docstring.expandtabs().splitlines()
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

def Reset():
    eg.stopExecutionFlag = True
    eg.programCounter = None
    del eg.programReturnStack[:]
    eg.eventThread.ClearPendingEvents()
    eg.actionThread.ClearPendingEvents()
    eg.PrintError("Execution stopped by user")

def SetDefault(targetCls, defaultCls):
    targetDict = targetCls.__dict__
    for defaultKey, defaultValue in defaultCls.__dict__.iteritems():
        if defaultKey not in targetDict:
            setattr(targetCls, defaultKey, defaultValue)
        elif type(defaultValue) in USER_CLASSES:
            SetDefault(targetDict[defaultKey], defaultValue)

def SplitFirstParagraph(text):
    """
    Split the first paragraph of a description string.

    The string can be encoded in HTML or reStructuredText.
    The paragraph is returned as HTML.
    """
    text = text.lstrip()
    if text.startswith("<md>"):
        text = text[4:]
        text = DecodeMarkdown(text)
        start = text.find("<p>")
        end = text.find("</p>")
        return (
            text[start + 3:end].replace("\n", " "),
            text[end + 4:].replace("\n", " ")
        )
    elif text.startswith("<rst>"):
        text = text[5:]
        text = DecodeReST(text)
        start = text.find("<p>")
        end = text.find("</p>")
        return (
            text[start + 3:end].replace("\n", " "),
            text[end + 4:].replace("\n", " ")
        )
    else:
        result = ""
        remaining = ""
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line.strip() == "":
                remaining = " ".join(lines[i:])
                break
            result += " " + line
        return ' '.join(result.split()), remaining

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

def UpdateStartupShortcut(create):
    from eg import Shortcut

    path = os.path.join(
        eg.folderPath.Startup,
        eg.APP_NAME + ".lnk"
    )

    if os.path.exists(path):
        os.remove(path)

    if create:
        if not os.path.exists(eg.folderPath.Startup):
            os.makedirs(eg.folderPath.Startup)

        Shortcut.Create(
            path=path,
            target=os.path.abspath(sys.executable),
            arguments="-h -e OnInitAfterBoot",
            startIn=os.path.dirname(os.path.abspath(sys.executable)),
        )

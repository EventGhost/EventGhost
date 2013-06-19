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

__all__ = ["Bunch", "EventHook", "LogIt", "LogItWithReturn",
    "TimeIt", "AssertNotMainThread", "AssertNotActionThread", "ParseString",
    "SetClass", "EnsureVisible", "namedtuple"
]
    

import threading
import time
import inspect
import types



class Bunch:
    """The simple but handy "collector of a bunch of named stuff" class.
    
    Often we want to just collect a bunch of stuff together, naming each 
    item of the bunch; a dictionary's OK for that, but a small do-nothing 
    class is even handier, and prettier to use.
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    
    #def __call__(self):
    #    return self.__dict__
    
    
    
class EventHook(object):
    __lastValues = ()
    
    def __init__(self):
        self.__handlers = []
        
        
    def Bind(self, handler):
        self.__handlers.append(handler)
        
        
    def Unbind(self, handler):
        self.__handlers.remove(handler)
        
        
    def Fire(self, *args):
        self.__lastValues = args
        for handler in self.__handlers:
            handler(*args)
            
            
    def Get(self):
        return self.__lastValues


    
def GetMyRepresentation(value):
    """
    Give a shorter representation of some wx-objects. Returns normal repr()
    for everything else. Also adds a "=" sign at the beginning to make it
    useful as a "formatvalue" function for inspect.formatargvalues().
    """
    t = repr(type(value))
    if t.startswith("<class 'wx._core."):
        return "=<wx.%s>" % t[len("<class 'wx._core."): -2]
    if t.startswith("<class 'wx._controls."):
        return "=<wx.%s>" % t[len("<class 'wx._controls."): -2]
    return "=" + repr(value)
                
                        
def GetFuncArgString(func, args, kwargs):
    classname = ""
    argnames, varargs, varkw, defaults = inspect.getargspec(func)
    start = 0
    if argnames:
        if argnames[0] == "self":
            classname = args[0].__class__.__name__ + "."
            start = 1
    res = []
    append = res.append
    for k, v in zip(argnames, args)[start:]:
        append(str(k) + GetMyRepresentation(v))
    for k, v in kwargs.items():
        append(str(k) + GetMyRepresentation(v))
    fname = classname + func.__name__
    return fname, "(" + ", ".join(res) + ")"


def LogIt(func):
    """Logs the function call, if eg.debugLevel is set."""
    if not eg.debugLevel:
        return func
    
    if func.func_code.co_flags & 0x20:
        raise "Can't wrap generator function"
    
    def LogItWrapper(*args, **kwargs):
        fname, argString = GetFuncArgString(func, args, kwargs)
        eg.PrintDebugNotice(fname + argString)
        return func(*args, **kwargs)
    return LogItWrapper
        

def LogItWithReturn(func):
    """Logs the function call and return, if eg.debugLevel is set."""
    if not eg.debugLevel:
        return func
    
    def LogItWithReturnWrapper(*args, **kwargs):
        fname, argString = GetFuncArgString(func, args, kwargs)
        eg.PrintDebugNotice(fname + argString)
        res = func(*args, **kwargs)
        eg.PrintDebugNotice(fname + " => " + repr(res))
        return res
    return LogItWithReturnWrapper
        

def TimeIt(func):
    """ Decorator to measure the execution time of a function.
    
    Will print the time to the log.
    """
    if not eg.debugLevel:
        return func
    def TimeItWrapper(*args, **kwargs):
        startTime = time.clock()
        fname, argString = GetFuncArgString(func, args, kwargs)
        res = func(*args, **kwargs)
        eg.PrintDebugNotice(fname + " :" + repr(time.clock() - startTime))
        return res
    return TimeItWrapper


def AssertNotMainThread(func):
    if not eg.debugLevel:
        return func
    def AssertWrapper(*args, **kwargs):
        assert eg.mainThread == threading.currentThread()
        return func(*args, **kwargs)
    return AssertWrapper

    
def AssertNotActionThread(func):
    if not eg.debugLevel:
        return func
    def AssertWrapper(*args, **kwargs):
        assert eg.actionThread == threading.currentThread()
        return func(*args, **kwargs)
    return AssertWrapper

    
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


def SetClass(obj, cls):
    for k, v in cls.__dict__.items():
        if type(v) == types.ClassType:
            if k in obj.__dict__:
                newValue = getattr(obj, k)
            else:
                newValue = v()
            SetClass(newValue, v)
            setattr(obj, k, newValue)
    obj.__class__ = cls
    

# TODO: find a better place for EnsureVisible


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
    windowTopLeft = windowRect.GetTopLeft()
    windowBottomRight = windowRect.GetBottomRight()
    
    # if the entire window is contained on the display, take a quick exit
    if GetDisplayFromPoint(windowTopLeft) != wx.NOT_FOUND:
        if GetDisplayFromPoint(windowBottomRight) != wx.NOT_FOUND:
            return
    
    # get the nearest display
    displayNum = wx.Display.GetFromWindow(window)
    if displayNum == wx.NOT_FOUND:
        displayNum = 0
        parent = window.GetParent()
        if parent:
            displayNum = wx.Display.GetFromWindow(parent)
    
    displayRect = displayRects[displayNum]

    displayLeft, displayTop = displayRect.GetTopLeft().Get()
    displayRight, displayBottom = displayRect.GetBottomRight().Get()
    
    windowLeft, windowTop = windowTopLeft.Get()
    windowRight, windowBottom = windowBottomRight.Get()
    
    # shift the dialog horizontally into the display area
    if windowLeft < displayLeft:
        windowRight += (displayLeft - windowLeft)
        windowLeft = displayLeft
        if windowRight > displayRight:
            windowRight = displayRight
    elif windowRight > displayRight:
        windowLeft += (displayRight - windowRight)
        windowRight = displayRight
        if windowLeft < displayLeft:
            windowLeft = displayLeft
            
    # shift the dialog vertically into the display area
    if windowTop < displayTop:
        windowBottom += (displayTop - windowTop)
        windowTop = displayTop
        if windowBottom > displayBottom:
            windowBottom = displayBottom
    elif windowBottom > displayBottom:
        windowTop += (displayBottom - windowBottom)
        windowBottom = displayBottom
        if windowTop < displayTop:
            windowTop = displayTop
            
    # set the new position and size
    newRect = wx.RectPP((windowLeft, windowTop), (windowRight, windowBottom))
    window.SetRect(newRect)


from operator import itemgetter as _itemgetter
from keyword import iskeyword as _iskeyword
import sys as _sys

def namedtuple(typename, field_names, verbose=False):
    """Returns a new subclass of tuple with named fields.

    >>> Point = namedtuple('Point', 'x y')
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # works just like the tuple (11, 22)
    33
    >>> x, y = p                        # unpacks just like a tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessable by name
    33
    >>> d = p.__asdict__()              # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p.__replace__(x=100)            # __replace__() is like str.replace() but targets named fields
    Point(x=100, y=22)

    """

    # Parse and validate the field names
    if isinstance(field_names, basestring):
        field_names = field_names.replace(',', ' ').split() # names separated by whitespace and/or commas
    field_names = tuple(field_names)
    for name in (typename,) + field_names:
        if not name.replace('_', '').isalnum():
            raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a keyword: %r' % name)
        if name[0].isdigit():
            raise ValueError('Type names and field names cannot start with a number: %r' % name)
    seen_names = set()
    for name in field_names:
        if name.startswith('__') and name.endswith('__'):
            raise ValueError('Field names cannot start and end with double underscores: %r' % name)
        if name in seen_names:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen_names.add(name)

    # Create and fill-in the class template
    argtxt = repr(field_names).replace("'", "")[1:-1]   # tuple repr without parens or quotes
    reprtxt = ', '.join('%s=%%r' % name for name in field_names)
    template = '''class %(typename)s(tuple):
        '%(typename)s(%(argtxt)s)'
        __slots__ = ()
        __fields__ = property(lambda self: %(field_names)r)
        def __new__(cls, %(argtxt)s):
            return tuple.__new__(cls, (%(argtxt)s))
        def __repr__(self):
            return '%(typename)s(%(reprtxt)s)' %% self
        def __asdict__(self, dict=dict, zip=zip):
            'Return a new dict mapping field names to their values'
            return dict(zip(%(field_names)r, self))
        def __replace__(self, **kwds):
            'Return a new %(typename)s object replacing specified fields with new values'
            return %(typename)s(**dict(zip(%(field_names)r, self), **kwds))  \n''' % locals()
    for i, name in enumerate(field_names):
        template += '        %s = property(itemgetter(%d))\n' % (name, i)
    if verbose:
        print template

    # Execute the template string in a temporary namespace
    namespace = dict(itemgetter=_itemgetter)
    try:
        exec template in namespace
    except SyntaxError, e:
        raise SyntaxError(e.message + ':\n' + template)
    result = namespace[typename]

    # For pickling to work, the __module__ variable needs to be set to the frame
    # where the named tuple is created.  Bypass this step in enviroments where
    # sys._getframe is not defined (Jython for example).
    if hasattr(_sys, '_getframe'):
        result.__module__ = _sys._getframe(1).f_globals['__name__']

    return result

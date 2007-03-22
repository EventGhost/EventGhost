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

import threading
import sys
import time
import inspect
import types

import wx
import eg


class Bunch:
    
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


    
        
def hexstring(text):
    """
    Returns representation of the bytes in a string as a nicely formatted 
    hex-digits-string.
    """
    return " ".join([("%0.2X" % ord(c)) for c in text]) 


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
                
                
def Notice(*args):
    t = threading.currentThread()
    s = [time.strftime("%H:%M:%S:")]
    s.append(str(t.getName()) + ":")

    for arg in args:
        s.append(str(arg))
    sys.stderr.write(" ".join(s) + "\n")

        
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
    if not eg.debugLevel:
        return func
    
    def LogItWrapper(*args, **kwargs):
        fname, argString = GetFuncArgString(func, args, kwargs)
        Notice(fname + argString)
        return func(*args, **kwargs)
    return LogItWrapper
        

def LogItWithReturn(func):
    if not eg.debugLevel:
        return func
    
    def LogItWrapper(*args, **kwargs):
        fname, argString = GetFuncArgString(func, args, kwargs)
        Notice(fname + argString)
        res = func(*args, **kwargs)
        Notice(fname + " => " + repr(res))
        return res
    return LogItWrapper
        

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
            if obj.__dict__.has_key(k):
                newValue = getattr(obj, k)
            else:
                newValue = v()
            SetClass(newValue, v)
            setattr(obj, k, newValue)
    obj.__class__ = cls
    




# $LastChangedDate$
# $Rev$


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
    
    
    def __call__(self):
        return self.__dict__
    
    
    
class EventHook(object):
    
    def __init__(self):
        self.__handlers = []
        
        
    def Bind(self, handler):
        self.__handlers.append(handler)
        
        
    def Fire(self, *args, **kwargs):
        for handler in self.__handlers:
            handler(*args, **kwargs)


    
        
def hexstring(text):
    """
    Returns representation of the bytes in a string as a nicely formatted 
    hex-digits-string.
    """
    return " ".join([("%0.2X" % ord(c)) for c in text]) 


def notice(*args):
    t = threading.currentThread()
    s = [time.strftime("%H:%M:%S:")]
    s.append(str(t.getName()) + ":")

    for arg in args:
        s.append(str(arg))
    sys.stderr.write(" ".join(s) + "\n")

        
def whoami(mesg=""):
    classname = ""
    frame = sys._getframe(1)
    args, varargs, varkw, locals = inspect.getargvalues(frame)
    if args:
        if args[0] == "self":
            classname = locals["self"].__class__.__name__ + "."
            del args[0]
    def test(value):
        t = repr(type(value))
        if t.startswith("<class 'wx._core."):
            s = "wx." + t[len("<class 'wx._core."): -2]
            return "=<" + s + ">"
        if t.startswith("<class 'wx._controls."):
            s = "wx." + t[len("<class 'wx._controls."): -2]
            return "=<" + s + ">"
       
        return "=" + repr(value)
        
    s = inspect.formatargvalues(
        args, varargs, varkw, locals, formatvalue=test
    )
    eg.notice(classname + frame.f_code.co_name + s, mesg)




def logit(level=1, print_return=False):
    def wrapper2(func):
        def wrapper(*oargs, **okwargs):
            classname = ""
            args, varargs, varkw, defaults = inspect.getargspec(func)
            start = 0
            if args:
                if args[0] == "self":
                    classname = oargs[0].__class__.__name__ + "."
                    start = 1
                    
            def test(value):
                t = repr(type(value))
                if t.startswith("<class 'wx._core."):
                    s = "wx." + t[len("<class 'wx._core."): -2]
                    return "<" + s + ">"
                if t.startswith("<class 'wx._controls."):
                    s = "wx." + t[len("<class 'wx._controls."): -2]
                    return "<" + s + ">"
                return repr(value)
                
            res = []
            add = res.append
            for k,v in zip(args, oargs)[start:]:
                add(str(k) + '=' + test(v))
            for k,v in okwargs.items():
                add(str(k) + '=' + test(v))
            fname = classname + func.__name__
            notice(fname + "(" + ", ".join(res) + ")")
            res = func(*oargs, **okwargs)
            if print_return:
                notice(fname + " => " + repr(res))
            return res
        
        if eg._debug >= level:
            return wrapper
        else:
            return func
    return wrapper2


def ParseString(text, filterFunc=None):
    start = 0
    chunks = []
    last = len(text) - 1
    while 1:
        pos = text.find('{', start)
        if pos == -1:
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
                raise "unmatched bracket"
            word = text[start:end]
            res = None
            if filterFunc:
                res = filterFunc(word)
            if res is None:	
                res = eval(word, {}, eg.globals.__dict__)
            chunks.append(str(res))
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
    



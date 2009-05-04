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

import eg
import wx
#import codecs
import sys
import traceback
import codecs
from weakref import ref
from threading import currentThread
from collections import deque
from types import UnicodeType
from time import time, strftime

_oldStdOut = sys.stdout
_oldStdErr = sys.stderr

oldStdOut = codecs.lookup("ascii").streamwriter(_oldStdOut, 'backslashreplace')
oldStdErr = codecs.lookup("ascii").streamwriter(_oldStdErr, 'backslashreplace')

INFO_ICON = eg.Icons.INFO_ICON
ERROR_ICON = eg.Icons.ERROR_ICON
NOTICE_ICON = eg.Icons.NOTICE_ICON



class DummyLogCtrl(object):
    
    def WriteLine(self, line, icon, wRef, when, indent):
        oldStdOut.write("%s\n" % line)
    
    
    
class Log(object):
    
    def __init__(self):
        self.buffer = ""
        self.data = deque()
        self.maxlength = 5000
        self.ctrl = DummyLogCtrl()
        log = self
        if eg.debugLevel:
            class StdOut:
                def write(self, data):
                    log.Write(data, INFO_ICON)
                    oldStdOut.write(data)
            
            class StdErr:
                def write(self, data):
                    oldStdErr.write(data.decode("mbcs"))
                    #self.Write(data, ERROR_ICON)
        else:
            class StdOut:
                def write(self, data):
                    log.Write(data, INFO_ICON)
            
            class StdErr:
                def write(self, data):
                    log.Write(data, ERROR_ICON)
        
        sys.stdout = StdOut()
        sys.stderr = StdErr()
        if eg.debugLevel == 2:
            _oldStdErr._displayMessage = False
        if eg.debugLevel:
            import warnings
            warnings.simplefilter('error', UnicodeWarning)
            self.PrintDebugNotice("----------------------------------------")
            self.PrintDebugNotice("        EventGhost started")
            self.PrintDebugNotice("----------------------------------------")
            self.PrintDebugNotice("Version:", eg.Version.string)
            
        # redirect all wxPython error messages to our log
        class MyLog(wx.PyLog):
            def DoLog(self, level, msg, dummyTimestamp):
                if (level >= 6):
                    return
                sys.stderr.write("Error%d: %s\n" % (level, msg))
        wx.Log.SetActiveTarget(MyLog())


    
    def SetCtrl(self, logCtrl):
        if logCtrl is not None:
            self.ctrl = logCtrl
        else:
            self.ctrl = DummyLogCtrl()
        
        
    @eg.LogIt
    def GetData(self, numLines=-1):
        if numLines == -1:
            start = 0
            end = len(self.data)
        elif numLines > len(self.data):
            numLines = len(self.data)
        data = list(self.data)
        return data[start:end]
    
    
    def _WriteLine(self, line, icon, wRef, when, indent):
        self.ctrl.WriteLine(line, icon, wRef, when, indent)
    
    
    def Write(self, text, icon, wRef=None, indent=0):
        try:
            lines = (self.buffer + text).split("\n")
        except UnicodeDecodeError:
            lines = (self.buffer + text.decode("mbcs")).split("\n")
        self.buffer = lines[-1]
        data = self.data
        when = time()
        for line in lines[:-1]:
            data.append((line, icon, wRef, when, eg.indent))
            wx.CallAfter(self._WriteLine, line, icon, wRef, when, eg.indent)
            if len(data) >= self.maxlength:
                data.popleft()

        
    def _Print(
        self, args, sep=" ", end="\n", icon=INFO_ICON, source=None, indent=0
    ):
        if source is not None:
            source = ref(source)
        strs = [unicode(arg) for arg in args]
        self.Write(sep.join(strs) + end, icon, source, indent)


    def Print(self, *args, **kwargs):
        self._Print(args, **kwargs)
    
        
    def PrintError(self, *args, **kwargs):
        """
        Prints an error message to the logger. The message will get a special
        icon and a red colour, so the user can easily identify it as an error
        message.
        """
        kwargs.setdefault("icon", ERROR_ICON)
        self._Print(args, **kwargs)

#        def convert(s):
#            if type(s) == type(u""):
#                return s
#            else:
#                return str(s)
#        text = " ".join([convert(arg) for arg in args])
#        self.Write(text + "\n", ERROR_ICON, None)
        
        
    def PrintNotice(self, *args, **kwargs):
        kwargs.setdefault("icon", NOTICE_ICON)
        self._Print(args, **kwargs)
#        text = " ".join([str(arg) for arg in args])
#        self.Write(text + "\n", NOTICE_ICON, None)
        
        
    def PrintTraceback(self, msg=None, skip=0, source=None):
        if msg:
            self.PrintError(msg, source=source)
        tbType, tbValue, tbTraceback = sys.exc_info() 
        slist = ['Traceback (most recent call last) (%d):\n' % eg.revision]
        if tbTraceback:
            slist += traceback.format_tb(tbTraceback)[skip:]
        slist += traceback.format_exception_only(tbType, tbValue)
        
        error = "".join(slist)
        if source is not None:
            source = ref(source)
        self.Write(error.rstrip() + "\n", ERROR_ICON, source)
        if eg.debugLevel:
            sys.stderr.write(error)
            

    def PrintStack(self, skip=0):
        strs = ['Stack trace (most recent call last) (%d):\n' % eg.revision]
        strs += traceback.format_stack(sys._getframe().f_back)[skip:]
        error = "".join(strs)
        self.Write(error.rstrip() + "\n", ERROR_ICON)
        if eg.debugLevel:
            sys.stderr.write(error)
            

    if eg.debugLevel:
        def PrintDebugNotice(self, *args):
            """Logs a message if eg.debugLevel is set."""
            threadName = str(currentThread().getName())
            taskletName = str(eg.Tasklet.GetCurrentId())
            strs = [strftime("%H:%M:%S:")]
            strs.append(taskletName + " " + threadName + ":")
        
            for arg in args:
                strs.append(str(arg))
            sys.stderr.write(" ".join(strs) + "\n")
    else:
        def PrintDebugNotice(self, *args):
            pass


    def LogEvent(self, event):
        """Store and display an EventGhostEvent in the logger."""
        payload = event.payload
        eventstring = event.string
        if payload is not None:
            if type(payload) == UnicodeType:
                mesg = eventstring + ' u"' + payload + '"'
            else:
                mesg = eventstring + ' ' + repr(payload)
        else:
            mesg = eventstring
        self.Write(mesg + "\n", eg.EventItem.icon, eventstring)
        

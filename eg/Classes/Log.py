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

import eg
import wx
import sys
import codecs
from collections import deque
from threading import currentThread
from time import time, strftime
from traceback import format_exception_only, format_stack, extract_tb
from types import UnicodeType
from weakref import ref

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
        self.logListeners = []
        self.eventListeners = []
        self.NativeLog = True
        self.buffer = ""
        self.data = deque()
        self.maxlength = 5000
        self.ctrl = DummyLogCtrl()
        log = self
        if eg.debugLevel:
            class StdOut:
                def write(self, data):
                    log.Write(data, INFO_ICON)
                    try:
                        oldStdOut.write(data)
                    except:
                        oldStdOut.write(data.decode('mbcs'))

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

        if eg.startupArguments.isMain:
            sys.stdout = StdOut()
            sys.stderr = StdErr()
        if eg.debugLevel == 2:
            if hasattr(_oldStdErr, "_displayMessage"):
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
                sys.stderr.write("wxError%d: %s\n" % (level, msg))
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

   
    def AddLogListener(self, listener):
        if listener not in self.logListeners:
            self.logListeners.append(listener)


    def RemoveLogListener(self, listener):
        if listener in self.logListeners:
            self.logListeners.remove(listener)
            
            
    def AddEventListener(self, listener):
        if listener not in self.eventListeners:
            self.eventListeners.append(listener)


    def RemoveEventListener(self, listener):
        if listener in self.eventListeners:
            self.eventListeners.remove(listener)
   

    def _WriteLine(self, line, icon, wRef, when, indent):
        if self.NativeLog:
            self.ctrl.WriteLine(line, icon, wRef, when, indent)
        for listener in self.logListeners:
            listener.WriteLine(line, icon, wRef, when, indent)


    def NativeLogOn(self, value):
        self.NativeLog = value


    def Write(self, text, icon, wRef=None):
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


    def _Print(self, args, sep=" ", end="\n", icon=INFO_ICON, source=None):
        if source is not None:
            source = ref(source)
        #strs = [unicode(arg) for arg in args]
        self.Write(sep.join(args) + end, icon, source)


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


    def PrintNotice(self, *args, **kwargs):
        kwargs.setdefault("icon", NOTICE_ICON)
        self._Print(args, **kwargs)


    def PrintTraceback(self, msg=None, skip=0, source=None, excInfo=None):
        if msg:
            self.PrintError(msg, source=source)
        if excInfo is None:
            excInfo = sys.exc_info()
        tbType, tbValue, tbTraceback = excInfo
        slist = ['Traceback (most recent call last) (%d):\n' % eg.revision]
        if tbTraceback:
            decode = codecs.getdecoder('mbcs')
            for fname, lno, funcName, text in extract_tb(tbTraceback)[skip:]:
                slist.append(
                    u'  File "%s", line %d, in %s\n' % (
                        decode(fname)[0], lno, funcName
                    )
                )
                if text:
                    slist.append("    %s\n" % text)
        for line in format_exception_only(tbType, tbValue):
            slist.append(decode(line)[0])
        error = "".join(slist)
        if source is not None:
            source = ref(source)
        self.Write(error.rstrip() + "\n", ERROR_ICON, source)
        if eg.debugLevel:
            oldStdErr.write(error)


    def PrintStack(self, skip=0):
        strs = ['Stack trace (most recent call last) (%d):\n' % eg.revision]
        strs += format_stack(sys._getframe().f_back)[skip:]
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


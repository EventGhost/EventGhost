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

import stackless
import wx

# Local imports
import eg

class TaskletDialog(wx.Dialog, eg.ControlProviderMixin):
    __tasklet = None
    __isModal = False
    __processingChannel = None
    __resultsChannel = None

    @eg.LogItWithReturn
    def __init__(self, *args, **kwargs):
        self.__lastEventId = None
        self.__done = False
        self.setupFinished = False
        wx.Dialog.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        eg.Notify("DialogCreate", self)

    def __iter__(self):
        while True:
            event, args = self.GetEvent()
            if event is None:
                raise StopIteration
            try:
                yield event, args
            except GeneratorExit:
                while True:
                    event, args = self.GetEvent()
                    if event is None:
                        return

    @eg.LogItWithReturn
    def Affirmed(self):
        if self.__isModal:
            if self.__lastEventId is False:
                return False
            self.__processingChannel.send("dummy")
            return self.__lastEventId
        else:
            if not self.setupFinished:
                self.FinishSetup()
            return self.__processingChannel.receive()

    @classmethod
    @eg.LogItWithReturn
    def Create(cls, *args, **kwargs):
        self = cls.__new__(cls, *args, **kwargs)
        self.__processingChannel = stackless.channel()
        self.__resultsChannel = stackless.channel()
        self.__tasklet = eg.Tasklet(self.ProcessingTask)(*args, **kwargs)
        self.__tasklet.run()
        return self

    def Configure(self, *args):
        raise NotImplementedError

    @eg.LogIt
    def Destroy(self):
        eg.Notify("DialogDestroy", self)
        wx.Dialog.Destroy(self)

    @eg.LogItWithReturn
    def DispatchEvent(self, event, eventId):
        #event.Skip()
        self.__lastEventId = eventId
        if self.__isModal:
            if eventId == wx.ID_CANCEL:
                self.__lastEventId = False
                self.EndModal(wx.ID_CANCEL)
            if not self.__tasklet.blocked:
                self.__tasklet.run()
            else:
                self.__processingChannel.receive()
                self.__tasklet.run()
        else:
            if eventId == wx.ID_CANCEL:
                self.__processingChannel.send(False)
            elif eventId == wx.ID_OK:
                self.__processingChannel.send(wx.ID_OK)
                if self.__done:
                    self.__processingChannel.send(None)
            else:
                self.__processingChannel.send(eventId)

    @eg.LogIt
    def FinishSetup(self):
        self.setupFinished = True
        self.Center()
        eg.Utils.EnsureVisible(self)
        self.Show()

    @eg.LogItWithReturn
    def GetEvent(self):
        event, args = self.__resultsChannel.receive()
        if event is None:
            self.__tasklet.run()
        return event, args

    @classmethod
    @eg.LogItWithReturn
    def GetModalResult(cls, *args, **kwargs):
        self = cls.__new__(cls, *args, **kwargs)
        self.__processingChannel = stackless.channel()
        self.result = None
        self.__isModal = True
        self.__tasklet = eg.Tasklet(self.Configure)(*args, **kwargs)
        self.__tasklet.run()
        self.__processingChannel.receive()
        #self.CenterOnParent()
        eg.Utils.EnsureVisible(self)
        self.ShowModal()
        self.Destroy()
        return self.result

    @classmethod
    def GetResult(cls, *args):
        for event, result in cls.Create(*args):
            if event == wx.ID_OK:
                return result
        return None

    @eg.LogItWithReturn
    def OnApply(self, event):
        self.DispatchEvent(event, wx.ID_APPLY)

    @eg.LogItWithReturn
    def OnCancel(self, event):
        self.DispatchEvent(event, wx.ID_CANCEL)

    @eg.LogItWithReturn
    def OnClose(self, event):
        self.DispatchEvent(event, wx.ID_CANCEL)

    @eg.LogItWithReturn
    def OnOK(self, event):
        self.DispatchEvent(event, wx.ID_OK)

    @eg.LogItWithReturn
    def ProcessingTask(self, *args, **kwargs):
        try:
            self.Configure(*args, **kwargs)
        except:
            eg.PrintTraceback()
        self.__done = True
        self.__resultsChannel.send((None, None))
        self.Destroy()

    @eg.LogItWithReturn
    def SetResult(self, *args):
        if self.__isModal:
            self.__lastEventId = False
            self.result = args
            self.EndModal(wx.ID_CANCEL)
        else:
            if self.__lastEventId == wx.ID_OK:
                self.__done = True
            self.__resultsChannel.send((self.__lastEventId, args))

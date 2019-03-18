# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
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
#
# Revision history:
# -----------------
# 2013-01-01 version 0.1  - Initial version
# 2013-01-13 version 0.2  - Handling unicode characters in the Application/Event/Description/Message fields
#                           Replaced tabs with spaces
#===============================================================================

import eg


eg.RegisterPlugin(
    name = "Prowl",
    author = "Mickelin",
    guid = "{6147991b-f074-4e20-9c96-fb853db4709b}",
    version = "0.1",
    kind="other",
    canMultiLoad = False,
    description = u"""<rst>
Push messages to your iPhone(s)/iPad(s) through Prowl. 

Go to **www.prowlapp.com** to register an account and generate an API Key.
Enter the API Key and other parameters in the plugin configuration. 
Get the Prowl app from App Store and install on you iOS device(s). Start the app and log in.\n\n
Use the QuickPush action to send a 
message using default message parameters from the plugin configuration.\n
Use the Push action to send a message using event specific message parameters.""",
icon = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJ"
    "bWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdp"
    "bj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6"
    "eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEz"
    "NDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJo"
    "dHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlw"
    "dGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAv"
    "IiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RS"
    "ZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpD"
    "cmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlE"
    "PSJ4bXAuaWlkOkRDMkY0RDY1NTRCQjExRTI4MUE4ODJFMjI3Qjg4MDc3IiB4bXBNTTpEb2N1bWVu"
    "dElEPSJ4bXAuZGlkOkRDMkY0RDY2NTRCQjExRTI4MUE4ODJFMjI3Qjg4MDc3Ij4gPHhtcE1NOkRl"
    "cml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6REMyRjRENjM1NEJCMTFFMjgxQTg4"
    "MkUyMjdCODgwNzciIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6REMyRjRENjQ1NEJCMTFFMjgx"
    "QTg4MkUyMjdCODgwNzciLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1l"
    "dGE+IDw/eHBhY2tldCBlbmQ9InIiPz7R98zUAAADbElEQVR42ixT22tcRRz+Zs59z+nuJuTWZqNJ"
    "06wh1RRSMYKKGBCRom/eijQ++OIfIAVBfBBEiooiioIKgu2D+iAtWH2x2tAHobDdElu7pN3suql7"
    "69nbuezZc+aMc4Izw/zgN/wu3zffj3DOkawwCoxWtzYfcyZTQrkkS5xFjIBSTsQ7iyLhppxSymbG"
    "FkqEEJbEyclV3vvr4S9/fvNrO7q7KEUqTVkK7hQ8np4mJPdQlg/uuQi9iOiWhmjE4oP6kcLrJ95/"
    "bWp87jZhLFLePfvy1m7jxvqpZ95Co1XBxatnce2CDYkymLMmzAzBwtoYFAPw2h56Tgcbq6/++Mbz"
    "H7xA+549HsTO4tsnz2Ft/ils25fQrgeYtCjOvLeEOZHk1y928f07d1C8aKNV45AwDjuoPBjHsUSD"
    "kY/V+Q12+NAxXC9dRtutI78+haGl46vPqsgt6Mjns/jk0yPYPDGB0i82ug1fQAkFezGRWRwRQ84k"
    "PGEim4PEVFAlwhOnZvH7N3Wc/7COlMpx7ts9HMjomDlmIrdsgHEi2CeQVUVDrbMNzhmWcsdxcv00"
    "rlR+gqxQvHR6Givr09i52kY8SaAdTmFtUYLvDqGnNCQpqCrrfLe7zS9c+xyypuCx/IsYFZdQPD9A"
    "87aLmfssLD8+iSdfmcPBRR1+ZwSn5cHteUkDkIUOyLA/JD/89jFulreQUmZwqXAZ+UczKBdGyOUt"
    "tGsOZlfEF0YMhqGLQoAubKIhmQjRWGmLh4aDqluCou5g9TkTQZ8JiiK0Gg6a1T5inhXfSjEYOPA8"
    "D5NzQkpUHJEGLIzBA2FdAjaUYE3JKG93MbGk4p8dG3t/OwhDwHUCmNmU4EeB1/U4xKb7EPwhwmAE"
    "RafQDAmN0gBOx4M1JqFa6KB68x6aFReyRNBtDqAdUKGZ2j4ECkKgWzo10ykwxtBrOuj+m1SScWtL"
    "VC/1wRnH1ndlgVve79br+SAyl5JYqisplwTKsNPqwbVDpDIGBFcgsZiRYgfhiEHXVewWeugIhZpp"
    "FcOBBzVO9wQnjGqaMdg4uvlRHEqgWgTf9wR5LhqVPhq1LiIewfN9BAJit92DHw6h8bHR00c3z4gy"
    "Qk7/j3Px1p/P7uxdP85jLhJz3r3LYNc9Mb77nYrFcWjZpKohhSv3P/LHAwurVxLvfwIMAMxZq3Iq"
    "CVgyAAAAAElFTkSuQmCC"
    ),
)

import Prowllib.prowlpy
import wx

class Text:
    applicationLabel = "Application:"
    eventLabel = "Event:"
    apikeyLabel = "API Key:"
    priorityLabel = "Priority:"
    urlLabel = "url:"
    settingsBox = "Settings"
    prioBox = "Priority"
    
class Notify:
        parameterDescription = "Message to send"


class Prowl(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddAction(QuickPush)
        self.AddAction(Push)


    def __start__(self, application, event, apikey, url, prio):
        self.application = application
        self.event = event
        self.apikey = apikey
        self.url = url
        self.prio = prio


    def Configure(self, application="EventGhost", event="{eg.event.string}", apikey="Generate an API Key at www.prowlapp.com", url="", priority=0):
        p = priority
        text = self.text
        panel = eg.ConfigPanel(self)
        applicationLabel = wx.StaticText(panel, -1, text.applicationLabel)
        eventLabel = wx.StaticText(panel, -1, text.eventLabel)
        apikeyLabel = wx.StaticText(panel, -1, text.apikeyLabel)
        urlLabel = wx.StaticText(panel, -1, text.urlLabel)
        priorityLabel = wx.StaticText(panel, -1, text.priorityLabel)
        applicationCtrl = wx.TextCtrl(panel, -1, application)
        eventCtrl = wx.TextCtrl(panel, -1, event)
        apikeyCtrl = wx.TextCtrl(panel, -1, apikey)
        urlCtrl = wx.TextCtrl(panel, -1, url)
        priorityCtrl = wx.Slider(
            panel,
            -1,
            0,-2,2,
            style = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS | wx.SL_INVERSE | wx.SL_TOP 
        )
        priorityCtrl.SetValue(priority) 

        def sliderUpdate(evt):
            if not panel.dialog.buttonRow.applyButton.IsEnabled():
                panel.dialog.buttonRow.applyButton.Enable(evt.GetInt() != p)
            evt.Skip()
        priorityCtrl.Bind(wx.EVT_SLIDER, sliderUpdate)

        sizer = wx.FlexGridSizer(6, 2, 8, 8)
        sizer.AddGrowableCol(1)
        panel.sizer.Add(sizer,1,wx.EXPAND)
        sizer.Add(applicationLabel,0,wx.TOP,10)
        sizer.Add(applicationCtrl,1,wx.EXPAND|wx.TOP,10)
        sizer.Add(eventLabel,0)
        sizer.Add(eventCtrl,1,wx.EXPAND)
        sizer.Add(apikeyLabel,0)
        sizer.Add(apikeyCtrl,1,wx.EXPAND)
        sizer.Add(urlLabel,0)
        sizer.Add(urlCtrl,1,wx.EXPAND)
        sizer.Add(priorityLabel,0,wx.TOP,10)
        sizer.Add(priorityCtrl,0,wx.EXPAND|wx.BOTTOM,6)

        while panel.Affirmed():
            panel.SetResult(
                applicationCtrl.GetValue(),
                eventCtrl.GetValue(),
                apikeyCtrl.GetValue(),
                urlCtrl.GetValue(),
                priorityCtrl.GetValue()
            )


    def Push(self, application, event, description, url, prio):
        p = Prowllib.prowlpy.Prowl(self.apikey)
        try:
    	    p.post(
                application.encode('utf-8'),
                event.encode('utf-8'),
                description.encode('utf-8'),
                prio,
                None,
                url
            )
        except Exception,msg:
    	    print msg

    def QuickPush(self, message):
        application = eg.ParseString(self.application)
        event = eg.ParseString(self.event)
        p = Prowllib.prowlpy.Prowl(self.apikey)
        try:
    	    p.post(
                application.encode('utf-8'),
                event.encode('utf-8'),
                message.encode('utf-8'),
                self.prio,
                None,
                self.url
            )
        except Exception,msg:
    	    print msg

class Push(eg.ActionBase):
    name = "Push"
    description = "Sends a message to iPhone/iPad using specified parameters."

    class text:
        applicationLabel = "Application:"
        eventLabel = "Event:"
        messageLabel = "Message:"
        urlLabel = "url:"
        priorityLabel = "Priority:"


    def __call__(
        self,
        application = "",
        event = "",
        message = "",
        url = "",
        priority = 0
        ):
        res = self.plugin.Push(
	    eg.ParseString(application),
	    eg.ParseString(event),
	    eg.ParseString(message),
	    eg.ParseString(url),
	    priority
	)
        return res


    def GetLabel(
        self,
        application,
        event,
        message,
        url,
        priority
        ):
        return "%s: %s: %s: %s %s: %s" % (self.name, application, event, message, url, priority)


    def Configure(
        self,
        application = "",
        event = "",
        message = "",
        url = "",
        priority = 0
        ):
        self.p = priority
        text = self.text
        panel = eg.ConfigPanel(self)
        applicationLabel = wx.StaticText(panel, -1, text.applicationLabel)
        eventLabel = wx.StaticText(panel, -1, text.eventLabel)
        messageLabel = wx.StaticText(panel, -1, text.messageLabel)
        urlLabel = wx.StaticText(panel, -1, text.urlLabel)
        priorityLabel = wx.StaticText(panel, -1, text.priorityLabel)
        applicationCtrl = wx.TextCtrl(panel, -1, application)
        eventCtrl = wx.TextCtrl(panel, -1, event)
        messageCtrl = wx.TextCtrl(panel, -1, message)
        urlCtrl = wx.TextCtrl(panel, -1, url)
        priorityCtrl = wx.Slider(
            panel,
            -1,
            0,-2,2,
            style = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS | wx.SL_INVERSE | wx.SL_TOP 
        )
        priorityCtrl.SetValue(priority) 

        def sliderUpdate(evt):
            if not panel.dialog.buttonRow.applyButton.IsEnabled():
                panel.dialog.buttonRow.applyButton.Enable(evt.GetInt() != self.p)
            evt.Skip()
        priorityCtrl.Bind(wx.EVT_SLIDER, sliderUpdate)

        sizer = wx.FlexGridSizer(6, 2, 8, 8)
        sizer.AddGrowableCol(1)
        panel.sizer.Add(sizer,1,wx.EXPAND)
        sizer.Add(applicationLabel,0,wx.TOP,10)
        sizer.Add(applicationCtrl,1,wx.EXPAND|wx.TOP,10)
        sizer.Add(eventLabel,0)
        sizer.Add(eventCtrl,1,wx.EXPAND)
        sizer.Add(messageLabel,0)
        sizer.Add(messageCtrl,1,wx.EXPAND)
        sizer.Add(urlLabel,0)
        sizer.Add(urlCtrl,1,wx.EXPAND)
        sizer.Add(priorityLabel,0,wx.TOP,10)
        sizer.Add(priorityCtrl,0,wx.EXPAND|wx.BOTTOM,6)

        while panel.Affirmed():
            panel.SetResult(
                applicationCtrl.GetValue(),
                eventCtrl.GetValue(),
                messageCtrl.GetValue(),
                urlCtrl.GetValue(),
                priorityCtrl.GetValue()
            )


class QuickPush(eg.ActionBase):
    name = "QuickPush"
    description = "Sends a message to iPhone/iPad using default parameters."
    class text:
        messageLabel = "Message:"


    def __call__(self, message):
        res = self.plugin.QuickPush(eg.ParseString(message))
        return res


    def GetLabel(
        self,
        message
        ):
        return "%s: %s" % (self.name, message)


    def Configure(
        self,
        message = "{eg.event.payload}"
        ):
        text = self.text
        panel = eg.ConfigPanel(self)
        messageLabel = wx.StaticText(panel, -1, text.messageLabel)
        messageCtrl = wx.TextCtrl(panel, -1, message)

        sizer = wx.FlexGridSizer(6, 2, 8, 8)
        sizer.AddGrowableCol(1)
        panel.sizer.Add(sizer,1,wx.EXPAND)
        sizer.Add(messageLabel,0)
        sizer.Add(messageCtrl,1,wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                messageCtrl.GetValue(),
            )
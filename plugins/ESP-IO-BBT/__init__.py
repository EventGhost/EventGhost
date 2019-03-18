# -*- coding: utf-8 -*-
version = "0.0.1"

# plugins/ESP-IO-BBT/__init__.py
#
# Copyright (C) 2017  Pako <lubos.ruckl@gmail.com>
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
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.1 by Pako 2017-09-25 17:45 GMT+1
#     - first public version
#===============================================================================

eg.RegisterPlugin(
    name = "ESP-IO-BBT",
    author = "Pako",
    version = version,
    kind = "external",
    guid = "{DC76F746-E922-4F9B-8975-09FDE49F8D8C}",
    createMacrosOnAdd = True,
    canMultiLoad = True,
    icon = (
        "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"
        "AABJRU5ErkJggg=="
    ),
    description = ur'''<rst>
Plugin for control ESP-12F_ (a mini wifi board with 4MB flash based on 
ESP-8266EX).

The project assumes the use of `NodeMcu 1.0`_ or `WeMos D1 mini`_ boards with
FW "ESP-IO-BBT".

The device may be in a completely different network than EventGhost. 
Only Internet connectivity at both ends is a condition. 
No public IP or VPN or port redirection is needed. 
This is possible thanks to the Beebotte_ service.

.. image:: NodeMcu700x525.png
.. image:: WeMos403x345.png

Changing to one of the GPIO will trigger an event in EventGhost.

Plugin uses libraries bbt_python_ and paho.mqtt.python_.

Plugin version: %s

.. _ESP-12F:           https://en.wikipedia.org/wiki/ESP8266
.. _`NodeMcu 1.0`:     https://en.wikipedia.org/wiki/NodeMCU
.. _`WeMos D1 mini`:   https://wiki.wemos.cc/products:d1:d1_mini
.. _Beebotte:          https://beebotte.com
.. _bbt_python:        https://github.com/beebotte/bbt_python
.. _paho.mqtt.python:  https://github.com/eclipse/paho.mqtt.python
''' % version,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=9841",
)

import paho.mqtt.client as mqtt
from time import time as ttime
from threading import Thread
from base64 import b64encode
from copy import deepcopy as cpy
from json import loads
from random import randrange
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from os.path import split, abspath
mod_pth = abspath(split(__file__)[0])
from sys import path as syspath
syspath.append(mod_pth + "\\lib")
from beebotte import *
import time
import paho.mqtt.client as mqtt

#from locale import setlocale, strcoll, LC_ALL
#import logging
#logging.basicConfig()
#setlocale(LC_ALL, "")

ACV           = wx.ALIGN_CENTER_VERTICAL
WATCHDOG_TIME  = 35.0
PINSTATES     = ("LOW", "HIGH")
MQTT_HOST     = "mqtt.beebotte.com"
MQTT_PORT     = 1883
SLEEP_TIME    = 60
#===============================================================================

class Text:
    debug = "Logging level:"
    debug2 = "(the higher the number, the more message writes ...)"
    prefix = "Event prefix:"
    password = "Password:"
    label = "Beebotte settings"
    channel = "Channel"
    cmdrsrc = "Command resource"
    msgrsrc = "Message resource"
    apikey = "API key"
    secretkey = "Secret key"
    token = "Channel token"
    cancel = "Cancel"
    ok = "OK"
    headers = (
        "Host:",
        "Port:",
        "Username:",
        "Password:",
    )
    proxyInfo = """If the proxy server does not require authentication, 
leave the Username and Password entries blank."""
    proxyTitle = "Proxy settings"
    connlost = 'ConnectionLost'
    config = "ConfigLoaded"
    addLstnr = 'Adding MQTT messaging listener'
    unknmsg = '%s: Unknown message: "%s"'
    input = '%s: Pin "%s" is input !'
#===============================================================================

class ESP_IO_BBT(eg.PluginClass):
    client = None
    text = Text
    prefix = None
    lastMessage = 0
    watchdog = None
    debug = 3
    proxy = ("",)
    gpios = {}
    queryData = {}
    cfgFlag = False
    connFlag = False

    def __init__(self):
        self.AddActionsFromList(ACTIONS)

    def GetToken(self):
        flag = True
        while flag: 
            token = format(randrange(16777216), '06x')
            flag = token in self.queryData
        event = CreateEvent(None, 0, 0, None)
        self.queryData[token] = event
        return token


    def SendPinCommand(self, cmd, pin, value):
        gpio = None
        for key, val in self.gpios.items():
            if val[0] == pin:
                gpio = key
                break
        if gpio is None:
            return
        token = self.GetToken()
        evt = self.queryData[token]
        msg = {"command":cmd,"id":gpio, "token":token}
        if value is not None:
            msg["value"] = value
        if cmd == "getpinstate" or self.gpios[gpio][1]:  #get value or pin is output ?
            try:
                self.resource.publish(msg)
                eg.actionThread.WaitOnEvent(evt)
                data = self.queryData[token]
                del self.queryData[token]
            except:
                del self.queryData[token] 
                data = {}
            return data
        else:
            eg.PrintError(self.text.input % (self.info.eventPrefix, pin))



    def startClient(self):
        if self.client is not None:
            try:
                self.client.unsubscribe(str("%s/%s" % (self.channel, self.msgrsrc)))
            except:
                pass
            try:
                self.client.disconnect()
            except:
                pass
        self.client = None
        del self.client

        #Will be called upon reception of CONNACK response from the server.
        def on_connect(client, data, rc):
            client.subscribe(str("%s/%s" % (self.channel, self.msgrsrc)), 1)
            self.cfgFlag = True

        def on_message(client, data, msg):
            pld = loads(msg.payload)
            if isinstance(pld, dict) and "data" in pld:
                if isinstance(pld["data"], dict) and 'message' in pld["data"]:
                    m = pld["data"]
                    mssg = m['message']
                    self.Log('message: %s' % m['message'], 5)
                    self.lastMessage = ttime()
                    if "token" in m:
                        token = m['token']
                        event = self.queryData[token]
                        del m["token"]
                        self.queryData[token] = m
                        SetEvent(event)
                        return
                    if mssg == 'nop':
                        if self.cfgFlag:
                            self.resource.publish({'command':'getconf'})
                    elif mssg == 'configfile':
                        if 'gpios' in m:
                            self.gpios = {}
                            for item in m['gpios']:
                                if item[1] and item[0] != m['wled']:
                                    self.gpios[item[0]] = (item[2], item[3]) # title, out
                            self.cfgFlag = False
                            self.connFlag = True
                            self.TriggerEvent(self.text.config)
                    #elif mssg == 'pinlist':
                    #    pass
                    #elif mssg == 'pinstate':
                    #    pass
                    elif mssg == 'change':
                        suffix = m['title']
                        if m['id'] != 'A0':
                            suffix += ".%s" % PINSTATES[m['value']]
                        self.TriggerEvent(suffix, payload=m['value'])
                    else:
                        eg.PrintNotice(self.text.unknmsg % (self.info.eventPrefix, repr(m)))
                else:
                    eg.PrintNotice(self.text.unknmsg % (self.info.eventPrefix, repr(pld["data"])))
            else:
                eg.PrintNotice(self.text.unknmsg % (self.info.eventPrefix, repr(pld)))

        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message         
        self.client.username_pw_set("token:%s" % self.TOKEN)
        try:
            self.client.connect(MQTT_HOST, MQTT_PORT, SLEEP_TIME)
        except  Exception, exc:
            eg.PrintError("%s: %s" % (self.info.eventPrefix, exc.args[1]))
        self.client.loop_start()


    def __start__(
        self,
        prefix = None,
        debug = 3,
        channel = "",
        cmdrsrc = "",
        msgrsrc = "",
        bbt_tkn = "",
        bbt_api = "",
        bbt_secret = "",
        dummy = "",
        proxy = ["", 0, "", ""]
    ):
        prefix = self.name if prefix is None else prefix
        self.info.eventPrefix = prefix
        self.debug = debug
        self.proxy = proxy
        self.cfgFlag = False
        self.lastMessage = ttime()
        self.queryData = {}
        self.channel = channel
        self.msgrsrc = msgrsrc
        if not isinstance(bbt_tkn, eg.Password):
            tkn = eg.Password(None)
            tkn.Set(bbt_tkn)
        else:
            tkn = bbt_tkn
        self.TOKEN = tkn.Get()

        if not isinstance(bbt_api, eg.Password):
            api = eg.Password(None)
            api.Set(bbt_api)
        else:
            api = bbt_api
        API_KEY = api.Get()

        if not isinstance(bbt_secret, eg.Password):
            secret = eg.Password(None)
            secret.Set(bbt_secret)
        else:
            secret = bbt_secret
        SECRET_KEY = secret.Get()
        bbt = BBT(API_KEY, SECRET_KEY)
        self.resource = Resource(bbt, self.channel, cmdrsrc)
        self.watchdog = eg.scheduler.AddTask(WATCHDOG_TIME, self.watcher)
        self.startClient()


    def stopWatchdog(self):
        if self.watchdog:
            try:
                eg.scheduler.CancelTask(self.watchdog)
            except:
                pass


    def OnComputerResume(self, dummy):
        self.cfgFlag = False
        self.connFlag = False
        self.gpios = {}
        self.watchdog = eg.scheduler.AddTask(5.0, self.watcher)


    def OnComputerSuspend(self, dummy):
        self.stopWatchdog()
  

    def __stop__(self):
        self.stopWatchdog()
        try:
            self.client.unsubscribe(str("%s/%s" % (self.channel, self.msgrsrc)))
        except:
            pass
        try:
            self.client.disconnect()
        except:
            pass
        self.client = None


    def Log(self, message, level):
        if self.debug >= level:
            print "%s: %s" % (self.info.eventPrefix, message)


    def watcher(self):
        if not self.info.isStarted:
            return
        self.stopWatchdog()
        if (ttime() - self.lastMessage) > WATCHDOG_TIME:
            if self.connFlag:
                self.TriggerEvent(self.text.connlost)
                self.gpios = {}
                self.connFlag = False
            self.startClient()
        self.watchdog = eg.scheduler.AddTask(WATCHDOG_TIME, self.watcher)


    def Configure(
        self,
        prefix = None,
        debug = 3,
        channel = "",
        cmdrsrc = "",
        msgrsrc = "",
        bbt_tkn = "",
        bbt_api = "",
        bbt_secret = "",
        dummy = "",
        proxy = ["", 0, "", ""]
    ):
        prefix = self.name if prefix is None else prefix
        if not isinstance(proxy[3], eg.Password):
            p = eg.Password(None)
            p.Set("")
            proxy[3] = p
        if not isinstance(bbt_tkn, eg.Password):
            tkn = eg.Password(None)
            tkn.Set("")
            bbt_tkn = tkn
        tkn = bbt_tkn
        if not isinstance(bbt_api, eg.Password):
            api = eg.Password(None)
            api.Set("")
            bbt_api = api
        api = bbt_api
        if not isinstance(bbt_secret, eg.Password):
            secret = eg.Password(None)
            secret.Set("")
            bbt_secret = secret
        secret = bbt_secret
        text = self.text
        panel = eg.ConfigPanel(self)
        panel.proxy = cpy(proxy)

        debugLabel2 = wx.StaticText(panel, -1, text.debug2)
        debugCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            debug,
            min = 1,
            max = 5
        )
        debugSizer = wx.BoxSizer(wx.HORIZONTAL)
        debugSizer.Add(debugCtrl, 0, wx.RIGHT, 5)
        debugSizer.Add( debugLabel2, 0, flag = ACV)
        prefixCtrl = panel.TextCtrl(prefix)
        labels = (
            panel.StaticText(text.prefix),
            panel.StaticText(text.debug),
            panel.StaticText(text.channel),
            panel.StaticText(text.cmdrsrc),
            panel.StaticText(text.msgrsrc),
            panel.StaticText(text.apikey),
            panel.StaticText(text.secretkey),
            panel.StaticText(text.token)
        )
        channelCtrl = wx.TextCtrl(panel, -1, channel)
        cmdrsrcCtrl = wx.TextCtrl(panel, -1, cmdrsrc)
        msgrsrcCtrl = wx.TextCtrl(panel, -1, msgrsrc)
        apiCtrl = wx.TextCtrl(panel, -1, bbt_api.Get(), style = wx.TE_PASSWORD)
        secretCtrl = wx.TextCtrl(panel, -1, bbt_secret.Get(), style = wx.TE_PASSWORD)
        tokenCtrl = wx.TextCtrl(panel, -1, bbt_tkn.Get(), style = wx.TE_PASSWORD)
        eg.EqualizeWidths(labels) 
        topSizer = wx.FlexGridSizer(6, 2, 5, 5)
        topSizer.Add(labels[0], 0, ACV|wx.LEFT,10)
        topSizer.Add(prefixCtrl,0,wx.EXPAND|wx.LEFT,5)
        topSizer.Add(labels[1], 0, ACV|wx.LEFT,10)
        topSizer.Add(debugSizer,0,wx.EXPAND|wx.LEFT,5)
        sizer = wx.FlexGridSizer(6, 2, 5, 5)
        sizer.AddGrowableCol(1)        
        sizer.Add(labels[2], 0, ACV)
        sizer.Add(channelCtrl,0,wx.EXPAND)
        sizer.Add(labels[3], 0, ACV)
        sizer.Add(cmdrsrcCtrl,0,wx.EXPAND)
        sizer.Add(labels[4], 0, ACV)
        sizer.Add(msgrsrcCtrl,0,wx.EXPAND)
        sizer.Add(labels[5], 0, ACV)
        sizer.Add(apiCtrl,0,wx.EXPAND)
        sizer.Add(labels[6], 0, ACV)
        sizer.Add(secretCtrl,0,wx.EXPAND)
        sizer.Add(labels[7], 0, ACV)
        sizer.Add(tokenCtrl,0,wx.EXPAND)
        staticBox = wx.StaticBox(panel, label=text.label)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        panel.sizer.Add(topSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM,5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)
        proxyBtn = wx.Button(panel.dialog, -1, text.proxyTitle)

        def onProxyBtn(evt):
            dlg = ProxyDialog(
                parent = panel,
                plugin = self,
                labels = text.headers,
                data = panel.proxy,
            )
            wx.CallAfter(
                dlg.ShowProxyDlg, text.proxyTitle
            )
            evt.Skip()
        proxyBtn.Bind(wx.EVT_BUTTON, onProxyBtn)
        panel.dialog.buttonRow.Add(proxyBtn)
        while panel.Affirmed():
            oldTkn = tkn.Get()
            newTkn = tokenCtrl.GetValue()
            if oldTkn != newTkn:
                tkn.Set(newTkn)
                dummy = str(ttime())
            oldApi = api.Get()
            newApi = apiCtrl.GetValue()
            if oldApi != newApi:
                api.Set(newApi)
                dummy = str(ttime())
            oldSecret = secret.Get()
            newSecret = secretCtrl.GetValue()
            if oldSecret != newSecret:
                secret.Set(newSecret)
                dummy = str(ttime())
            if proxy[3].Get() != panel.proxy[3].Get():
                dummy = str(ttime())
            panel.SetResult(
                prefixCtrl.GetValue(),
                debugCtrl.GetValue(),
                channelCtrl.GetValue(),
                cmdrsrcCtrl.GetValue(),
                msgrsrcCtrl.GetValue(),
                tkn,
                api,
                secret,
                dummy,
                panel.proxy
           )
#===============================================================================

class ProxyDialog(wx.Frame):
    def __init__(
        self,
        parent,
        plugin,
        labels,
        data,
    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL|wx.RESIZE_BORDER,
            name="ProxyDialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.labels = labels
        self.data = data


    def ShowProxyDlg(self, title):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)
        text = self.plugin.text
        panel = wx.Panel(self)

        def wxst(label):
            return wx.StaticText(panel, -1, label)

        labels = self.labels
        data = self.data
        rows = len(labels)
        sizer = wx.GridBagSizer(5, 5)
        for row in range(rows):
            sizer.Add(wxst(labels[row]), (row, 0), flag = ACV)
            if row not in (1, 3):
                txtCtrl = wx.TextCtrl(panel, -1, data[row])
            elif row == 1:
                txtCtrl = eg.SpinIntCtrl(
                    panel,
                    -1,
                    data[row],
                    min = 0,
                    max = 65535
                )
            elif row == 3:
                self.password = eg.Password(data[row])
                txtCtrl = wx.TextCtrl(
                    panel,
                    -1,
                    self.password.Get(),
                    style = wx.TE_PASSWORD
                )
            sizer.Add(txtCtrl, (row, 1), flag = wx.EXPAND)
        sizer.AddGrowableCol(1)
        info = wxst(text.proxyInfo)
        info.Enable(False)
        sizer.Add(info, (rows, 0), (1, 2), flag = ACV) 

        line = wx.StaticLine(
            panel,
            -1,
            style = wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer,1,wx.ALL|wx.EXPAND,5)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        mainSizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        mainSizer.Add((1,6))
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)


        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)


        def onOk(evt):
            data = []
            children = sizer.GetChildren()
            for child in range(1, len(children), 2):
                ctrl = children[child].GetWindow()
                if child != 7:
                    data.append(ctrl.GetValue())
                else:
                    self.password.Set(ctrl.GetValue())
                    data.append(self.password)
            self.GetParent().proxy = data
            self.Close()
        btn1.Bind(wx.EVT_BUTTON, onOk)


        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)

        mainSizer.Layout()
        w, h = self.GetSize()
        self.SetSize((max(w, 300), h))
        self.SetMinSize((max(w, 300), h))
        self.Raise()
        self.MakeModal(True)
        self.Centre()
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

#===============================================================================

class pinCommand(eg.ActionBase):

    class text:
        pin = "Pin:"
        val = "State:"
        

    def __call__(self, pin = "", val = 0):
        pin = eg.ParseString(pin)
        data = self.plugin.SendPinCommand(
            self.value, 
            pin, 
            val if self.value == "setpinstate" else None
        )
        if data is not None:
            if pin != self.plugin.gpios["A0"][0]:
                return PINSTATES[data['value']]
            else:
                return data['value']

    def GetLabel(self, pin = "", val = 0):
        if self.value == "setpinstate":
            return "%s: %s %s" % (self.name, pin, PINSTATES[val])
        else:
            return "%s: %s" % (self.name, pin)


    def Configure(self, pin = "", val = 0):
        text = self.text
        panel = eg.ConfigPanel()
        pinLabel = wx.StaticText(panel, -1, text.pin)
        if len(self.plugin.gpios.values()):
            if self.value == "getpinstate":
                choices = [item[0] for item in self.plugin.gpios.values()]
            else:
                choices = [item[0] for item in self.plugin.gpios.values() if item[1]]
            choices.sort()
        else:
            choices = () #TEST AND DISABLE ?
        pinCombo = wx.ComboBox(
            panel,
            -1,
            choices = choices,
        )
        pinCombo.SetStringSelection(pin)

        if self.value == "setpinstate":
            valLabel = wx.StaticText(panel, -1, text.val)
            valCtrl = wx.Choice(panel, -1, choices=PINSTATES)
            valCtrl.SetSelection(val)

        sizer = wx.FlexGridSizer(2 if self.value == "setpinstate" else 1, 2, 10, 10)
        sizer.Add(pinLabel, 0, ACV)
        sizer.Add(pinCombo)

        if self.value == "setpinstate":
            sizer.Add(valLabel,0,ACV)
            sizer.Add(valCtrl)
        panel.sizer.Add(sizer,0,wx.ALL,10)

        while panel.Affirmed():
            panel.SetResult(
                pinCombo.GetValue(),
                valCtrl.GetSelection() if self.value == "setpinstate" else None,
            )
#===============================================================================

ACTIONS = (    
    (pinCommand,
        "GetPinState",
        "Get pin state",
        "Get pin state.",
        "getpinstate"
    ),
    (pinCommand,
        "TogglePinState",
        "Toggle pin state",
        "Toggles pin state.",
        "toggle"
    ),
    (pinCommand,
        "SetPinState",
        "Set pin state",
        "Set pin state",
        "setpinstate"
    ),
)
#===============================================================================

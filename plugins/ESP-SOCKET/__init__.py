# -*- coding: utf-8 -*-
version = "0.0.1"

# plugins/ESP-SOCKET/__init__.py
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
# 0.0.1 by Pako 2018-03-21 16:12 GMT+1
#     - first public version
#===========================================================================

eg.RegisterPlugin(
    name = "ESP-SOCKET",
    author = "Pako",
    version = version,
    kind = "external",
    guid = "{3FF216DB-647F-43C6-9D34-C71AE619B386}",
    createMacrosOnAdd = True,
    canMultiLoad = True,
    icon = (
        "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"
        "YII="
    ),
    description = ur'''<rst>
Plugin for control ESP-12F_ (a mini wifi board with 4MB flash based on 
ESP-8266EX).

The project assumes the use of `NodeMcu 1.0`_ or `WeMos D1 mini`_ boards with
FW "ESP-SOCKET".

.. image:: NodeMcu700x525.png
.. image:: WeMos403x345.png

A chenge of state will trigger an event in EventGhost.

Plugin uses libraries websocket-client_ .

Plugin version: %s

.. _ESP-12F:           https://en.wikipedia.org/wiki/ESP8266
.. _`NodeMcu 1.0`:     https://en.wikipedia.org/wiki/NodeMCU
.. _`WeMos D1 mini`:   https://wiki.wemos.cc/products:d1:d1_mini
.. _websocket-client:  https://pypi.python.org/pypi/websocket-client
''' % version,
    #url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=XXXX",
)

from time import time as ttime
from threading import Thread
from base64 import b64encode
from copy import deepcopy as cpy
from json import loads, dumps
from random import randrange
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from os.path import split, abspath
mod_pth = abspath(split(__file__)[0])
from sys import path as syspath
syspath.append(mod_pth + "\\lib")
from websocket_0440S import WebSocketApp
from beebotte_050S import *
import paho.mqtt.client as mqtt

#from locale import setlocale, strcoll, LC_ALL
#import logging
#logging.basicConfig()
#setlocale(LC_ALL, "")

ACV            = wx.ALIGN_CENTER_VERTICAL
DEFAULT_WAIT   = 35.0
PINSTATES      = ("OFF","ON")
MQTT_HOST      = "mqtt.beebotte.com"
MQTT_PORT      = 1883
SLEEP_TIME     = 60
WATCHDOG_TIME  = 35.0
#===============================================================================

class WebSocketClient(WebSocketApp):
    def __init__(self, url, plugin):
        WebSocketApp.__init__(
            self,
            url,
            on_open = plugin.on_open,
            on_message = plugin.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
        )
        self.plugin = plugin
        

    def on_error(self, _, error):
        eg.PrintError(self.plugin.text.wsError % (self.plugin.info.eventPrefix, error))
        self.plugin.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(5.0, self.plugin.watcher)


    def on_close(self, _):
        if self.plugin.connFlag:
            self.plugin.TriggerEvent(self.plugin.text.wsClosedEvt)
            self.plugin.connFlag = False

    def start(self):
        auth = None
        if self.plugin.proxy[0] != "":
            host = str(self.plugin.proxy[0])
            port = self.plugin.proxy[1]
            if self.plugin.proxy[2] != "":
                auth = (
                    str(self.plugin.proxy[2]),
                    str(self.plugin.proxy[3].Get())
                ) 
        else:
            host = None
            port = None
        self.run_forever(
            http_proxy_host = host,
            http_proxy_port = port,
            http_proxy_auth = auth
        )        
#===============================================================================

class Text:
    debug = "Logging level:"
    debug2 = "(the higher the number, the more message writes ...)"
    prefix = "Event prefix:"
    host = "Host address:"
    port = "TCP/IP port:"
    password = "Password:"
    channel = "Channel:"
    cmdrsrc = "Command resource:"
    msgrsrc = "Message resource:"
    apikey = "API key:"
    secretkey = "Secret key:"
    token = "Channel token:"
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
    reconnect = "Haven't seen a nop lately, reconnecting"
    connected = "Connected"
    disconnected = "Disconnected"
    wsOpenedEvt = "WebSocketOpened"
    wsClosedEvt = "WebSocketClosed"
    wsError = u"%s: WebSocket error: %s"
    wsMssg = "WebSocket message: %s"
    unknmsg = '%s: Unknown message: %s'
    mode = 'Connection method:'
    mode0 = 'Locale LAN (websocket)'
    mode1 = 'Beebotte (MQTT)'
    addLstnr = "addLstnr"
#===============================================================================

class ESP_SOCKET(eg.PluginClass):
    client = None
    wsC = None
    text = Text
    prefix = None
    connFlag = False
    msgWait = 0
    lastMessage = 0
    watchdog = None
    debug = 5
    proxy = ("",)
    queryData = {}

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


    def SendCommand(self, cmd, value):
        token = self.GetToken()
        evt = self.queryData[token]
        msg = {"command":cmd, "token":token}
        if value is not None:
            msg["state"] = value
        msg = dumps(msg)
        try:
            self.wsC.send(msg)
            eg.actionThread.WaitOnEvent(evt)
            data = self.queryData[token]
            del self.queryData[token]
        except:
            del self.queryData[token] 
            data = {}
        return data


    def normalizeURL(self, url, port):
        if not url.startswith("ws://"):
            if url.startswith("http://"):
                url = url.replace("http://","ws://")
            else:
                url = "ws://" + url
        if not url.endswith("/ws") and not url.endswith("/ws/"):
            if url.endswith("/"):
                url += "ws"
            else:
                url += "/ws"
        elif url.endswith("/ws/"):
            url = url[:-1]
        return url.replace("/ws",":%i/ws" % port)      


    def SendMessage(self, cmd, message):
        token = self.GetToken()
        evt = self.queryData[token]
        msg = {"command":cmd, "token":token}
        if message is not None:
            msg["value"] = message
        try:
            self.resource.publish(msg)
            eg.actionThread.WaitOnEvent(evt)
            data = self.queryData[token]
            del self.queryData[token]
            return data
        except:
            del self.queryData[token] 
            eg.PrintTraceback()
            return {}  


    def stopClient(self):
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
        self.connFlag = False


    def startClient(self):
        self.stopClient()
        #Will be called upon reception of CONNACK response from the server.
        def on_connect(client, data, rc):
            client.subscribe(str("%s/%s" % (self.channel, self.msgrsrc)), 1)
            if self.connFlag:
                self.TriggerEvent(self.text.disconnected)
                self.connFlag = False
            self.resource.publish({'command':'getinitstate'})

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
                        #return
                    if mssg == 'nop':
                        pass
                    elif mssg == 'initstate':
                            self.connFlag = True
                            self.TriggerEvent(
                                self.text.connected,
                                payload = m['state']
                            )
                    elif mssg == "change" and m['change']:
                        self.TriggerEvent(
                            "Change.%s" % PINSTATES[m['state']],
                            payload = m['state']
                        )
                    elif mssg == 'button':
                        self.TriggerEvent("Button")
                    elif mssg == 'connected':
                        if self.connFlag:
                            self.TriggerEvent(self.text.disconnected)
                        self.connFlag = False
                        self.resource.publish({'command':'getinitstate'})
                    elif mssg == 'state':
                        pass
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
        mode = 0,
        host = "ws://",
        port = 80,
        password = "",
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
        self.prefix = prefix
        self.debug = debug
        self.proxy = proxy
        self.connFlag = False
        self.msgWait = DEFAULT_WAIT
        self.lastMessage = ttime()
        self.queryData = {}
        self.debug = debug
        self.mode = mode
        if mode:
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
            self.stopWatchdog()
            self.watchdog = eg.scheduler.AddTask(WATCHDOG_TIME, self.watcher)
            self.startClient()
        else:
            _ = eg.scheduler.AddTask(1.0, self.establishSubscriber)
            self.url = self.normalizeURL(host, port)
            self.port = port
            if not isinstance(password, eg.Password):
                passw = eg.Password(None)
                passw.Set(password)
            else:
                passw = password
            self.password = b64encode(passw.Get())


    def stopWatchdog(self):
        if self.watchdog:
            try:
                eg.scheduler.CancelTask(self.watchdog)
            except:
                pass
        self.watchdog = None


    def OnComputerResume(self, dummy):
        self.watchdog = eg.scheduler.AddTask(15.0, self.watcher)


    def OnComputerSuspend(self, dummy):
        self.stopWatchdog()
        self.stopClient()
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.ct = None
  

    def __stop__(self):
        self.stopWatchdog()
        self.stopClient()
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.ct = None


    def Log(self, message, level):
        if self.debug >= level:
            print "%s: %s" % (self.info.eventPrefix, message)


    def watcher(self):
        if not self.info.isStarted:
            return
        if (ttime() - self.lastMessage) > self.msgWait:
            if self.connFlag:
                self.TriggerEvent(self.text.disconnected)
            self.Log(self.text.reconnect, 2)
            self.lastMessage = ttime()
            if self.mode: #MQTT
                self.startClient()
            else:
                self.refreshWebSocket()
        self.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(5.0, self.watcher)


    def on_open(self, _):
        self.connFlag = True
        self.TriggerEvent(self.text.wsOpenedEvt)


    def establishSubscriber(self): 
        if self.wsC: 
            return
        self.wsC = WebSocketClient(self.url, self)
        self.ct = Thread(target = self.wsC.start)
        self.ct.start()
        self.lastMessage = ttime() 
        self.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(0.01, self.watcher)
        self.Log(self.text.addLstnr, 4)


    def refreshWebSocket(self):
        self.msgWait = DEFAULT_WAIT
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.establishSubscriber()
        self.connFlag = False


    def on_message(self, _, m):
        if not self.info.isStarted:
            if self.wsC:
                self.wsC.close()
        if m is None:
            return
        try:
            m = loads(m)
            if 'command' in m and m['command'] == 'configfile':
                del m['apwd']
                del m['pswd']
            self.Log(self.text.wsMssg % repr(m), 5)
            self.lastMessage = ttime()
            self.msgWait = DEFAULT_WAIT
        except:
            eg.PrintTraceback()
            self.refreshWebSocket()
            return
        if "token" in m:
            token = m['token']
            event = self.queryData[token]
            del m["token"]
            self.queryData[token] = m
            SetEvent(event)
            #return  # ToDo: make it optional
        if 'command' in m:
            cmd = m['command']
            if cmd == 'nop':
                pass
            elif cmd == 'password':
                self.wsC.send("{'command':'password','password':'%s'}" % self.password)
            elif cmd == 'authorized':
                self.wsC.send("{'command':'getconf'}")
                self.TriggerEvent(self.text.connected) 
            elif cmd == 'configfile':
                pass
            elif cmd == 'button':
                self.TriggerEvent("Button")
            elif cmd == 'change':
                if m['change']:
                    self.TriggerEvent(
                        "Change.%s" % PINSTATES[m['state']],
                        payload=m['state']
                    )
        else:
            eg.PrintNotice(unknmsg % (self.info.eventPrefix, repr(m)))


    def Configure(
        self,
        prefix = None,
        debug = 3,
        mode = 0,
        host = "ws://",
        port = 80,
        password = "",
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
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        panel.proxy = cpy(proxy)

        if not isinstance(password, eg.Password):
            passw = eg.Password(None)
            passw.Set(password)
        else:
            passw = password
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
        rb0=panel.RadioButton(mode==0,self.text.mode0, style=wx.RB_GROUP)
        rb1 = panel.RadioButton(mode==1, self.text.mode1)
        modeSizer = wx.BoxSizer(wx.HORIZONTAL)
        modeSizer.Add(rb0)
        modeSizer.Add(rb1, 0, wx.LEFT, 10)
        labels = (
            panel.StaticText(text.prefix),
            panel.StaticText(text.debug),
            panel.StaticText(text.mode)
        )
        eg.EqualizeWidths(labels) 
        topSizer = wx.FlexGridSizer(3, 2, 10, 5)
        topSizer.Add(labels[0], 0, ACV|wx.LEFT,10)
        topSizer.Add(prefixCtrl,0,wx.EXPAND|wx.LEFT,5)
        topSizer.Add(labels[1], 0, ACV|wx.LEFT,10)
        topSizer.Add(debugSizer,0,wx.EXPAND|wx.LEFT,5)
        topSizer.Add(labels[2], 0, ACV|wx.LEFT,10)
        topSizer.Add(modeSizer,0,wx.EXPAND|wx.LEFT,5)
        sizer = wx.FlexGridSizer(10, 2, 8, 5)
        sizer.AddGrowableCol(1)        
        labels0 = (
            panel.StaticText(text.host),
            panel.StaticText(text.port),
            panel.StaticText(text.password)
        )
        labels1 = (
            panel.StaticText(text.channel),
            panel.StaticText(text.cmdrsrc),
            panel.StaticText(text.msgrsrc),
            panel.StaticText(text.apikey),
            panel.StaticText(text.secretkey),
            panel.StaticText(text.token)
        )
        ctrls0 = (
            panel.TextCtrl(host),
            panel.SpinIntCtrl(port, min = 1, max = 65535),
            wx.TextCtrl(panel, -1, passw.Get(), style = wx.TE_PASSWORD)
        )
        ctrls1 = (
            wx.TextCtrl(panel, -1, channel),
            wx.TextCtrl(panel, -1, cmdrsrc),
            wx.TextCtrl(panel, -1, msgrsrc),
            wx.TextCtrl(panel, -1, bbt_api.Get(), style = wx.TE_PASSWORD),
            wx.TextCtrl(panel, -1, bbt_secret.Get(), style = wx.TE_PASSWORD),
            wx.TextCtrl(panel, -1, bbt_tkn.Get(), style = wx.TE_PASSWORD)        
        )
        sizer.Add((-1,1))
        sizer.Add((-1,1))
        for i in range(len(labels0)):
            sizer.Add(labels0[i], 0, ACV)
            sizer.Add(ctrls0[i], 0, wx.EXPAND)
        for i in range(len(labels1)):
            sizer.Add(labels1[i], 0, ACV)
            sizer.Add(ctrls1[i], 0, wx.EXPAND)

        staticBox = wx.StaticBox(panel, label="")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        panel.sizer.Add(topSizer, 0, wx.EXPAND|wx.TOP,5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
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

        # ONLY FOR DIALOG FITTING
        for item in labels0:    #
            item.Show(False)    #
        for item in ctrls0:     #
            item.Show(False)    #   
        # ONLY FOR DIALOG FITTING

        def redrawDialog(evt):
            md = 0 if rb0.GetValue() else 1
            for item in labels1:
                item.Show(md)
            for item in ctrls1:
                item.Show(md) 
            md = not md
            for item in labels0:
                item.Show(md)
            for item in ctrls0:
                item.Show(md)
            panel.sizer.Layout()        
            evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, redrawDialog)
        rb1.Bind(wx.EVT_RADIOBUTTON, redrawDialog)
        panel.dialog.Bind(wx.EVT_SHOW, redrawDialog)

        while panel.Affirmed():
            oldPassw = passw.Get()
            newPassw = ctrls0[2].GetValue()
            if oldPassw != newPassw:
                passw.Set(newPassw)
                dummy = str(ttime())
            if proxy[3].Get() != panel.proxy[3].Get():
                dummy = str(ttime())
            oldTkn = tkn.Get()
            newTkn = ctrls1[5].GetValue()
            if oldTkn != newTkn:
                tkn.Set(newTkn)
                dummy = str(ttime())
            oldApi = api.Get()
            newApi = ctrls1[3].GetValue()
            if oldApi != newApi:
                api.Set(newApi)
                dummy = str(ttime())
            oldSecret = secret.Get()
            newSecret = ctrls1[4].GetValue()
            if oldSecret != newSecret:
                secret.Set(newSecret)
                dummy = str(ttime())
            if proxy[3].Get() != panel.proxy[3].Get():
                dummy = str(ttime())                
            panel.SetResult(
                prefixCtrl.GetValue(),
                debugCtrl.GetValue(),
                int(rb1.GetValue()),
                ctrls0[0].GetValue(),
                ctrls0[1].GetValue(),
                passw,
                ctrls1[0].GetValue(),
                ctrls1[1].GetValue(),
                ctrls1[2].GetValue(),
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
        info = wxst(text.proxyInfo)
        info.Enable(False)
        sizer.Add(info, (rows, 0), (1, 2), flag = ACV) 
        sizer.AddGrowableCol(1)

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
        val = "State:"
        

    def __call__(self, val = 0):
        if self.plugin.mode:
            data = self.plugin.SendMessage(
                self.value, 
                val if self.value == "setstate" else None
            )
            if data is not None:
                if isinstance(data, dict) and "state" in data:
                    return PINSTATES[data['state']]
        else:
            data = self.plugin.SendCommand(
                self.value, 
                val if self.value == "setstate" else None
            )
            if data is not None:
                if isinstance(data, dict) and "state" in data:
                    return PINSTATES[data['state']]


    def GetLabel(self, val = 0):
        if self.value == "setstate":
            return "%s: %s" % (self.name, PINSTATES[val])
        else:
            return "%s" % self.name


    def Configure(self, val = 0):
        text = self.text
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.plugin.info.icon.GetWxIcon())
        if self.value == "setstate":
            valLabel = wx.StaticText(panel, -1, text.val)
            valCtrl = wx.Choice(panel, -1, choices=PINSTATES)
            valCtrl.SetSelection(val)

        sizer = wx.FlexGridSizer(2 if self.value == "setstate" else 1, 2, 10, 10)

        if self.value == "setstate":
            sizer.Add(valLabel,0,ACV)
            sizer.Add(valCtrl)
        panel.sizer.Add(sizer,0,wx.ALL,10)

        while panel.Affirmed():
            panel.SetResult(
                valCtrl.GetSelection() if self.value == "setstate" else None,
            )
#===============================================================================

ACTIONS = (    
    (pinCommand,
        "GetState",
        "Get state",
        "Get state.",
        "getstate"
    ),
    (pinCommand,
        "ToggleState",
        "Toggle state",
        "Toggles state.",
        "toggle"
    ),
    (pinCommand,
        "SetState",
        "Set state",
        "Set state",
        "setstate"
    ),
)
#===============================================================================

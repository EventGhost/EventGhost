# -*- coding: utf-8 -*-

version = "0.0.1"

# plugins/AndroidNotifier/__init__.py
#
# Copyright (C) 2013  Pako <lubos.ruckl@quick.cz>
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.1 by Pako 2013-01-20 17:22 GMT+1
#     - support link (EG forum) added
# 0.0.0 by Pako 2013-01-20 13:38 GMT+1
#     - initial version
#===============================================================================

import eg
from socket import socket, AF_INET, SOCK_DGRAM
from socket import error as socket_error
from asyncore import dispatcher
from locale import getdefaultlocale as localeEncoding
from hashlib import md5
from Crypto.Cipher import AES
from struct import unpack

eg.RegisterPlugin(
    name = "Android Notifier",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{B662DD8C-7E6D-44A5-BC30-B01D40B2601D}",
    description = ur"""<rst>
Receives notifications from **Remote Notifier for Android**.

This plugin receives notifications from 
the `Remote Notifier for Android`__ by **Rodrigo Damazio**.

If you are using **Tasker** (or **Locale**) also, you can also take advantage 
of the **Tasker/Locale** plugin `Locale Remote Notifier Plug-in`__.

This plugin support only UDP broadcast.

Encryption of notifications is supported (optional).
You MUST also configure the Android application for this.

__ https://play.google.com/store/apps/details?id=org.damazio.notifier
__ https://play.google.com/store/apps/details?id=org.damazio.notifier.locale.notify
""",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADrElEQVR42r2WbWwURRjH"
        "/7N7faMNKTYFgiHUD75E40ui4aUmSkAL1iYWW9vaVHut6YciRApGJBRC+dAqEBUaYrEE"
        "am1qUi400TQGEgOpqdo0VnNRoQkgqTGYA6730r273Z2dcbbXKzS06c1S+1w2u3d7M89v"
        "/8/8n1lytOt7NT0ttY4xnoeFCgIuPgO6QftIw6GepnEttp9a1oLltyMjPZWrRCkgtfs6"
        "POJ7yYJmnwxKrQMC4EsPIfIAVtSPB7MMxAwTfrYUSkqaNIBJaRN5Z78AAJkAIOLgibtk"
        "8szv/B4/cxBB/MwKC+6qMoTDYXzc5kGYLU56vH1lX+vUjAMohEgr8Hr+Cmx6eQNM08SR"
        "tq9x3a9IK6Cbhg3QKQDkSmAr8Nra5XilYOMEwKftPbh6k8tMMQlgOgOwY/OzudhStAm6"
        "ruNwWw/+DhDZKRIA8RJM408UbDYFxPHiE9moLC3C+Pg4Wj734GbElfT4xBxTAETahgRr"
        "Hs5EbWUxxsbG0NzWi5CRKq2AYbvAtqFsCewHfHplGurdJfD5fGhu74PO5G1o2C6oEY1I"
        "XgHgkWUqGurKMDo6isOdF0GRIg1g2gDuxtMSAHfMvWoJsHtrBUZGRtDq+QUMydjwruYg"
        "rk0qbFi999RUI5KJpZkWGreV4dffvOg4fwWcy9uQmnoTeXvPSdGK5QEyXAz1Jasx5L2C"
        "Hy4FpJPHAYQCb334hSMFRDfCA1kpiOhM7AfUGYBdgqoPRCN3AjAPQakoQeX7xx0pwPUg"
        "VmYzhCM6xngOFMWJC4QCFQ2tjtbAC49lorqqHMFgEM2tX+FWbJEzBcp3fCb9QmJvRsXP"
        "P4TS4kJomoaPjnfjmk+XTE/ia+CN7Uc8kFVAOC43OwPrnspDIKRh8I9/xN4u/0o34YIt"
        "9S1nVEUtlR5tP4Po4TaMkx5gRywW2Udeqti5dVFW9jFFVdXZ5J59a+OOk1MjpoUDt9eT"
        "/FdriKK6NiguNW8mqbMW5zSmpKbfc49zhkg40GcY0d65tt6Z5rUoHRz49uTvcw4trN47"
        "JNR5bnpyDi3k79YjWt1P33VEHEmQUHiuP2yu2i0AXFMAnFk8HLx9wtSjDYPnumL3kzwp"
        "gII3d00BMIsyv+9GC2PmweELZ4z7TZ4UwMay9yYAGDVpRAvt+evPy5/8e/1nNh/JkwJY"
        "X/LuEGfsyagW2kFj0RPD/WedLXunAOsK3f3CMaLmerd34Jt5TZ4UwKP5hY+ngVzy/tg3"
        "78mTAvi/4z/YZ60RGjvYkAAAAABJRU5ErkJggg=="
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5208",
)
#===============================================================================

class Text:
    eventPrefix = "Event prefix:"
    remIP = "Android IP address:"
    port = "UDP port:"
    password = "Passphrase (optional):"
    listens = "Android Notifier (plugin) listens on port %i"
    released  = "Android Notifier (plugin) released port %i"
#===============================================================================

class udpReceiver(dispatcher):

    def __init__(self, address, port, plugin):
        self.lastNotId = None
        self.remAddress=address
        self.plugin=plugin
        key = self.plugin.password.Get()
        if key:
            for i in range(10):
                h = md5()
                h.update(key)
                key = h.digest()
        self.key = key
        dispatcher.__init__(self)
        self.create_socket(AF_INET, SOCK_DGRAM)
        eg.RestartAsyncore()
        self.bind(('', port))
        

    def writable(self):
        return False  # we don't have anything to send !


    def handle_connect(self):
        pass
        

    def handle_close(self):
        self.close()
 

    def handle_expt(self):
        self.close()


    def unpadd(self, data):
        return data[0:-ord(data[-1])]


    def handle_read(self):
        payload, address = self.socket.recvfrom(512)
        key = self.key
        if key:
            iv = payload[:16]
            data = payload[16:]
            payload = self.unpadd(AES.new(key, AES.MODE_CBC, iv).decrypt(data))
        selfAddr = self.remAddress
        if not selfAddr or selfAddr == "0.0.0.0" or selfAddr == address[0]:
            mess = payload[:-1].split("/")
            if len(mess) > 3: 
                if mess[0] =='v2':
                    DEVICE_ID = mess[1]
                    notId = mess[2]
                    evtTyp = mess[3]
                    data = mess[4] if not evtTyp =='USER' else None
                    cont = mess[5:] if not evtTyp =='USER' else mess[4:]
                elif key:
                    DEVICE_ID = mess[0]
                    notId = mess[1]
                    evtTyp = mess[2]
                    data = mess[3] if not evtTyp =='USER' else None
                    cont = mess[4:] if not evtTyp =='USER' else mess[3:]
                else:
                    DEVICE_ID = mess[0]
                    notId = mess[1]
                    evtTyp = mess[2]
                    cont = mess[3:]
                    data = None
                if self.lastNotId != notId:
                    self.lastNotId = notId
                    TriggEvent = eg.TriggerEvent
                    prefix = "%s.%s" % (self.plugin.prefix, evtTyp)
                    suffix = cont[0].decode('utf-8')
                    payload = []
                    for part in cont[1:]:
                        payload.append(part.decode('utf-8'))
                    if len(cont) == 1:
                        TriggEvent(suffix, prefix = prefix)
                    if len(cont) > 1:
                        TriggEvent(suffix, prefix = prefix, payload = payload)
#ToDo: handle "DEVICE_ID" and "data" ?
#Note: Handle the DEVICE_ID is impossible, 
#      because inside Android Notifier is probably a bug.
#      If encryption is turned on, it is overwritten beginning of the message.
#===============================================================================

class AndroidNotifier(eg.PluginBase):
    text = Text

    def __start__(
        self,
        prefix="Android",
        port=10600,
        remAddress="0.0.0.0",
        password = ""
    ):
        self.prefix = prefix
        self.port = port
        self.password = password
        try:
            self.receiver = udpReceiver(remAddress, port, self)
            eg.PrintNotice(self.text.listens % self.port)
        except socket_error, exc:
            raise self.Exception(exc[1].decode(localeEncoding()[1]))
        

    def __stop__(self):
        if self.receiver:
            self.receiver.close()
            eg.PrintNotice(self.text.released % self.port)
        self.receiver = None

        
    def Configure(
        self,
        prefix="Android",
        port=10600,
        remAddress="0.0.0.0",
        password = ""
        ):
        panel = eg.ConfigPanel(self)
        mainSizer = wx.FlexGridSizer(4,2,15,10)
        prefixLabel = wx.StaticText(panel, -1, self.text.eventPrefix)
        prefixCtrl = panel.TextCtrl(prefix)
        ipAddressLabel = wx.StaticText(panel, -1, self.text.remIP)
        ipAddressCtrl = panel.TextCtrl(remAddress)
        locPortLabel = wx.StaticText(panel, -1, self.text.port)
        locPortLabel.Enable(False)
        locPortCtrl = panel.SpinIntCtrl(port, min = 1, max = 65535)
        locPortCtrl.Enable(False)
        passwordLabel = wx.StaticText(panel, -1, self.text.password)
        password = eg.Password(password)
        passwordCtrl = wx.TextCtrl(
            panel,
            -1,
            password.Get(),
            style = wx.TE_PASSWORD
        )
        eg.EqualizeWidths((prefixCtrl, ipAddressCtrl, passwordCtrl))
        mainSizer.Add(prefixLabel,0,wx.TOP,4)
        mainSizer.Add(prefixCtrl)
        mainSizer.Add(ipAddressLabel,0,wx.TOP,4)
        mainSizer.Add(ipAddressCtrl)
        mainSizer.Add(locPortLabel,0,wx.TOP,4)
        mainSizer.Add(locPortCtrl)
        mainSizer.Add(passwordLabel,0,wx.TOP,4)
        mainSizer.Add(passwordCtrl)
        panel.sizer.Add(mainSizer,1,wx.EXPAND|wx.ALL,15)
        
        while panel.Affirmed():
            password.Set(passwordCtrl.GetValue())
            panel.SetResult(
                prefixCtrl.GetValue(), 
                int(locPortCtrl.GetValue()),
                ipAddressCtrl.GetValue(),
                password
            )
#===============================================================================

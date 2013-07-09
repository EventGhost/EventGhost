# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2010 Lars-Peter Voss <bitmonster@eventghost.org>
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
import pickle
import ctypes
import hashlib
import weakref
import struct
from comtypes import GUID
from Crypto.Cipher import AES
from eg.WinApi.Dynamic import GetVolumeInformation, DWORD, byref


def GetMachineKey():
    # Get the volume serial number of the system drive
    volumeSerialBuffer = DWORD()
    GetVolumeInformation(
        "C:\\", None, 0, byref(volumeSerialBuffer), None, None, None, 0
    )
    value = volumeSerialBuffer.value
    volumeSerial = (
        chr((value >> 24) & 0xFF)
        + chr((value >> 16) & 0xFF)
        + chr((value >> 8) & 0xFF)
        + chr(value & 0xFF)
    )
    # The last 6 bytes of the UUID returned from UuidCreateSequential contain
    # the hardware MAC address.
    uuid = ctypes.create_string_buffer(16)
    ctypes.windll.rpcrt4.UuidCreateSequential(uuid)
    mac = uuid.raw[-6:]
    return volumeSerial + mac

MACHINE_KEY = GetMachineKey()



class MasterPasswordDialog(wx.Dialog):

    def __init__(self):
        self.result = None
        wx.Dialog.__init__(self, eg.document.frame)
        staticText = wx.StaticText(
            self, -1, "Please enter your master password:"
        )
        self.passwordCtrl = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(staticText, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.passwordCtrl, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        sizer.Add(self.buttonRow.sizer, 0, wx.ALIGN_CENTER)
        self.SetSizerAndFit(sizer)


    def OnOK(self, event):
        self.result = self.passwordCtrl.GetValue()
        event.Skip()



class Password(object):
    database = {}
    instances = weakref.WeakKeyDictionary()
    masterkey = "EventGhost"

    def __new__(cls, *args, **kwargs):
        self = super(Password, cls).__new__(cls)
        cls.instances[self] = 1
        return self


    def __init__(self, guid=None, content=None):
        if guid is None:
            guid = str(GUID.create_new())
        elif isinstance(guid, Password):
            guid = guid.guid
        if content is not None:
            self.database[guid] = content
        self.guid = guid


    def Get(self):
        try:
            return self.database[self.guid]
        except KeyError:
            return ""


    def Set(self, password):
        self.database[self.guid] = password


    def __repr__(self):
        return "eg.Password(%r)" % self.guid


    def __unicode__(self):
        return self.Get()


    def __str__(self):
        return self.Get()


    @classmethod
    def GetDatabaseContent(cls):
        newDatabase = {}
        for instance in cls.instances.keys():
            guid = instance.guid
            try:
                newDatabase[guid] = cls.database[guid]
            except KeyError:
                pass
        if len(newDatabase) == 0:
            return ""
        text = pickle.dumps(newDatabase)
        key = cls.masterkey
        # The length of the key must be a multiple of 16
        key = key + "X" * (16 - len(key) % 16)
        hashObj = hashlib.md5()
        hashObj.update(text)
        textHash = hashObj.digest()
        length = len(textHash + text) + 4
        padding = ("X" * (32 - length % 32))
        paddedString = textHash + struct.pack("L", length) + text + padding
        return AES.new(key, AES.MODE_ECB).encrypt(paddedString)


    @classmethod
    def SetDatabaseContent(cls, data):
        if not data:
            cls.database = {}
            return
        key = cls.masterkey
        # The length of the key must be a multiple of 16
        key = key + "X" * (16 - (len(key) % 16))
        paddedString = AES.new(key, AES.MODE_ECB).decrypt(data)
        textHash = paddedString[:16]
        length = struct.unpack("L", paddedString[16:20])[0]
        plaintext = paddedString[20:length]
        hashObj = hashlib.md5()
        hashObj.update(plaintext)
        hash2 = hashObj.digest()
        if textHash != hash2:
            eg.PrintError("Decryption error.")
            cls.database = {}
            return
        cls.database = pickle.loads(plaintext)


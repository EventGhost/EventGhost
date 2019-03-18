#
# SoundGraph iMON HID V0.3
# ================
# Written by Pavel Ivanov aka Johnson, <johnsik@gmail.com>
# Based on "Generic HID" 1.5.1221 by Bartman.
#
# Special Thanks for MediaPortal project!
# Code from source file "Imon USB Receivers.cs" was used for this plugin.
#
# Public Domain
#
# Revision history:
# -----------------
# 0.1 - (22.02.09)	initial
# 0.2 - (02.03.09)	add LCD Contrast, Auto Color, Auto Adjust, LCD Brightness and LCD Reset events
#   add set/get LCD Contrast, set/get LCD Brightness, do Auto Color, do Auto Adjust, do LCD Reset actions
#   add action to switch iMON PAD / MCE remotes
#   add support for Antec Fusion Remote
#   code reorganization
#   some bugs corrected
# 0.3 - (28.03.09)	event name system changed
#   add support for front buttons
#   renamed to SoundGraph iMON HID
#   code reorganization
#   remove custom label for plugin
#   some bugs corrected

import eg

eg.RegisterPlugin(
    name="SoundGraph iMON HID",
    guid='{84533F03-89D4-4D05-A7CB-610C7A1B6CBC}',
    author="Johnson",
    version="0.3",
    kind="remote",
    canMultiLoad=True,
    description='Communication with SoundGraph iMON HID devices.',
    createMacrosOnAdd=True,
)

IMON_PAD = 0x1000
IMON_PAD_PAD = 0x2000
IMON_82 = 0x3000
IMON_FRONT = 0x4000
IMON_FRONT_KNOB = 0x5000

IMON_PAD_BUTTON_DOWN = 0xF8
IMON_PAD_BUTTON_LEFT = 0xF6
IMON_PAD_BUTTON_RIGHT = 0xF4
IMON_PAD_BUTTON_UP = 0xFA

import binascii
import sys
import threading
from array import array
from Queue import Queue, Empty, Full
from eg.WinApi.HID import HIDThread, GetDevicePath, GetDeviceDescriptions, DeviceDescription, IsDeviceName


class conf:
    keyPadSensitivity = 11
    PADButtonwaitTime = 0.5
    PADPADwaitTime = 0.08
    FRONTwaitTime = 0.05


class current:
    KeyboardMode = False


class Text:
    manufacturer = "Manufacturer"
    deviceName = "Device Name"
    connected = "Connected"
    eventName = "Event prefix (optional):"
    yes = "Yes"
    no = "No"
    multipleDeviceOptions = "Options for multiple same devices"
    noOtherPort = "Use selected device only if connected to current port"
    useDeviceIndex = "Use the device with index"
    errorFind = "Error finding iMON device: "
    vendorID = "Vendor ID "
    deviceID = "Device ID"
    versionID = "Version ID"


IMON_PAD_PAD_REMOTE_TABLE = {
    IMON_PAD_BUTTON_DOWN: 'Down',
    IMON_PAD_BUTTON_LEFT: 'Left',
    IMON_PAD_BUTTON_RIGHT: 'Right',
    IMON_PAD_BUTTON_UP: 'Up'
}

IMON_PAD_REMOTE_TABLE = {
    0x02: 'App. Exit',
    0x10: 'Power',
    0x40: 'Record',
    0x80: 'Play',
    0x90: 'Pause',
    0xDC: 'Stop',
    0x72: 'Open',
    0xD0: 'Prev',
    0x42: 'Next',
    0x82: 'Rewind',
    0xC0: 'F.Forward',
    0x50: 'Mouse/Keyboard',
    0x56: 'Eject',
    0xB2: 'Quick Launch',
    0x7C: 'App. Launcher',
    0x96: 'Task Switcher',
    0xDA: 'Mute',
    0x26: 'VOL+',
    0x2A: 'VOL-',
    0x16: 'CH+',
    0x0E: 'CH-',
    0xC6: 'Timer',
    0xC8: 'Red (Videos)',
    0x52: 'Green (Music)',
    0xE0: 'Blue (Pictures)',
    0x28: 'Yellow (TV)',
    0x08: 'Bookmark',
    0xBC: 'Thumbnail',
    0x6A: 'Zoom',
    0xA6: 'Full Screen',
    0x66: 'DVD',
    0xE6: 'Menu',
    0x4A: 'Subtitle',
    0xCA: 'Audio'
}

IMON_82_TABLE = {
    0x02: 'TouchLCDContrast',
    0x03: 'TouchLCDAutoColor',
    0x04: 'TouchLCDAutoAdjust',
    0x05: 'TouchLCDBrightness',
    0x07: 'TouchLCDReset'
}

IMON_FRONT_TABLE = {
    0x01: 'Mute',
    0x0F: 'MCE',
    0x12: 'Up',
    0x13: 'Down',
    0x14: 'Left',
    0x15: 'Right',
    0x16: 'Enter',
    0x17: 'Back',
    0x2B: 'App. Exit',
    0x2C: 'Start',
    0x2D: 'Menu'
}


class PAD_MCE(eg.ActionClass):
    def __call__(self):
        self.plugin.thread.Write('\x00' + chr(self.cmd) + '\x00\x00\x00\x00\x00\x00\x86', 0)


class MouseKeyboardAction(eg.ActionClass):
    def __call__(self):
        self.plugin.thread.Write('\x00' + chr(int(self.KeyboardMode)) + '\x00\x00\x00\x00\x00\x00\x80', 0)
        current.KeyboardMode = self.KeyboardMode


class ToggleMouseKeyboardAction(eg.ActionClass):
    def __call__(self):
        self.plugin.thread.Write('\x00' + chr(int(not current.KeyboardMode)) + '\x00\x00\x00\x00\x00\x00\x80', 0)
        current.KeyboardMode = not current.KeyboardMode


class LCDdoAction(eg.ActionClass):
    def __call__(self):
        self.plugin.thread.Write('\x00' + chr(self.cmd) + '\x00\x00\x00\x00\x00\x00\x82', 0)


class LCDgetAction(eg.ActionClass):
    def __call__(self):
        self.plugin.thread.Write('\x00' + chr(self.cmd | 0x80) + '\x00\x00\x00\x00\x00\x00\x82', 0)


class LCDsetAction(eg.ActionWithStringParameter):
    def __call__(self, data):
        self.plugin.thread.Write('\x00' + chr(self.cmd) + chr(int(data)) + '\x00\x00\x00\x00\x00\x82', 0)


class iMON(eg.PluginClass):
    def __init__(self):
        self.thread = None
        self.messlist = []
        self.repThread = None

        group = self.AddGroup('iMON PAD/MCE')

        class Action(PAD_MCE):
            name = 'iMON PAD remote'
            cmd = 0x00

        Action.__name__ = 'iMON_PADremote'
        group.AddAction(Action)

        class Action(PAD_MCE):
            name = 'MCE remote'
            cmd = 0x01

        Action.__name__ = 'MCEremote'
        group.AddAction(Action)

        group = self.AddGroup('Mouse/Keyboard')

        class Action(MouseKeyboardAction):
            name = 'PAD as mouse'
            KeyboardMode = False

        Action.__name__ = 'PADasMouse'
        group.AddAction(Action)

        class Action(MouseKeyboardAction):
            name = 'PAD as keyboard'
            KeyboardMode = True

        Action.__name__ = 'PADasKeyboard'
        group.AddAction(Action)

        class Action(ToggleMouseKeyboardAction):
            name = 'Toggle Mouse/Keyboard'

        Action.__name__ = 'ToggleMouseKeyboard'
        group.AddAction(Action)
        # group.items.append('ddd')

        group = self.AddGroup('Touch LCD')

        class Action(LCDdoAction):
            name = 'Auto Color'
            cmd = 0x03

        Action.__name__ = 'AutoColor'
        group.AddAction(Action)

        class Action(LCDdoAction):
            name = 'Auto Adjust'
            cmd = 0x04

        Action.__name__ = 'AutoAdjust'
        group.AddAction(Action)

        class Action(LCDdoAction):
            name = 'LCD Reset'
            cmd = 0x07

        Action.__name__ = 'LCDReset'
        group.AddAction(Action)

        class Action(LCDgetAction):
            name = 'get LCD Contrast'
            cmd = 0x02

        Action.__name__ = 'getLCDContrast'
        group.AddAction(Action)

        class Action(LCDgetAction):
            name = 'get LCD Brightness'
            cmd = 0x05

        Action.__name__ = 'getLCDBrightness'
        group.AddAction(Action)

        class Action(LCDsetAction):
            name = 'set LCD Contrast'
            cmd = 0x02
            parameterDescription = 'Value: (1 - 255)'

        Action.__name__ = 'setLCDContrast'
        group.AddAction(Action)

        class Action(LCDsetAction):
            name = 'set LCD Brightness'
            cmd = 0x05
            parameterDescription = 'Value: (1 - 255)'

        Action.__name__ = 'setLCDBrightness'
        group.AddAction(Action)

    class iMONevent:
        "iMON event"
        code = None
        up = None
        arg1 = None

    def RawCallback(self, data):
        if (len(data) != 9):
            eg.PrintError('Unexpected length of message: ' + binascii.hexlify(data).upper())
            return

        mess = array('B', data[:])
        if (mess[0] != 0x00) or (mess[6] != 0x00):
            eg.PrintError('Unexpected format of message: ' + binascii.hexlify(data).upper())
            return

        event = self.iMONevent()

        if (mess[8] == 0x01):
            if (mess[4] != 0xB7) or (mess[5] != 0x00):
                eg.PrintError('Unexpected format of 01 message: ' + binascii.hexlify(data).upper())
                return

            if ((mess[1] & 0xFC) == 0x28):
                keyCode = ((mess[1] & 0x03) << 6) | (mess[2] & 0x30) | ((mess[2] & 0x06) << 1) | ((mess[3] & 0xC0) >> 6)

                event.code = (keyCode & 0xFE) + IMON_PAD
                event.up = bool(keyCode & 0x01)

            elif ((mess[1] & 0xFC) == 0x68):
                # filter out invalid reports
                if ((mess[1] & 0x01) == ((mess[2] & 0x80) >> 7)): self.PrintError(
                    'invalid position data: ' + binascii.hexlify(data).upper())
                if ((mess[2] & 0x04) == ((mess[2] & 0x02) << 1)): self.PrintError(
                    'invalid right click: ' + binascii.hexlify(data).upper())
                if ((mess[2] & 0x01) == ((mess[3] & 0x80) >> 7)): self.PrintError(
                    'invalid left click: ' + binascii.hexlify(data).upper())

                dx = (mess[2] & 0x08) | ((mess[2] & 0x10) >> 2) | ((mess[2] & 0x20) >> 4) | ((mess[2] & 0x40) >> 6)
                if (mess[1] & 0x02) != 0: dx -= 16

                dy = (mess[3] & 0x08) | ((mess[3] & 0x10) >> 2) | ((mess[3] & 0x20) >> 4) | ((mess[3] & 0x40) >> 6)
                if (mess[1] & 0x01) != 0: dy -= 16

                keyCode = self.TranslateMouseToKeypress(dx, dy)
                if not keyCode: return

                event.code = keyCode + IMON_PAD_PAD

            else:
                return

        elif (mess[8] == 0x82):
            if ((mess[1] & 0x80) == 0x00) or (mess[3] != 0x00) or (mess[4] != 0x00) or (mess[5] != 0x00):
                eg.PrintError('Unexpected format of 82 message: ' + binascii.hexlify(data).upper())
                return

            keyCode = mess[1] & 0x7F

            event.code = keyCode + IMON_82
            if keyCode in [2, 5]:
                event.arg1 = mess[2]

        elif (mess[8] == 0x86):
            return  # Touch LCD display touch events not implemented yet

        elif (mess[8] == 0xAE):
            return  # MCE remote button events not implemented yet

        elif (mess[8] == 0xBE):
            return  # MCE Keyboard key press events not implemented yet

        elif (mess[8] == 0xCE):
            return  # MCE Keyboard mouse move/button events not implemented yet

        elif (mess[8] == 0xEE):
            if (mess[3] != 0x00) or (mess[5] != 0x00):
                eg.PrintError('Unexpected format of EE message: ' + binascii.hexlify(data).upper())
                return

            if (mess[4] == 0x00):
                if ((mess[1] != 0x00) and (mess[2] != 0x00)) or ((mess[1] == 0x00) and (mess[2] == 0x00)) or (
                    (mess[1] + mess[2]) > 4):
                    return

                event.code = IMON_FRONT_KNOB
                event.arg1 = mess[2] - mess[1]
            else:
                keyCode = mess[4]
                event.code = keyCode + IMON_FRONT

        else:
            eg.PrintError('Unknown source: ' + binascii.hexlify(data).upper())
            return

        try:
            self.EventsQueue.put(event)
        except Full:
            eg.PrintError('Internal events queue if full')

    def repThreadLoop(self):
        lastkeyCode = None
        waitTime = None
        while True:
            try:
                event = self.EventsQueue.get(True, waitTime)
            except Empty:
                lastEvent.SetShouldEnd()
                lastkeyCode = None
                waitTime = None
                continue

            if (event is None):
                break

            elif ((event.code == lastkeyCode) and event.up):
                lastEvent.SetShouldEnd()
                lastkeyCode = None
                waitTime = None

            elif (event.code != lastkeyCode) and not event.up:

                keyType = event.code & (~0xFFF)
                keyCode = event.code & 0xFFF
                waitTime = None

                if (keyType == IMON_PAD):
                    keyName = ''
                    if (keyCode in IMON_PAD_REMOTE_TABLE):
                        keyName += IMON_PAD_REMOTE_TABLE[keyCode]
                    else:
                        keyName += 'PAD_0x' + format(keyCode, '02X')
                    waitTime = conf.PADButtonwaitTime

                elif (keyType == IMON_PAD_PAD):
                    keyName = ''
                    if (keyCode in IMON_PAD_PAD_REMOTE_TABLE):
                        keyName += IMON_PAD_PAD_REMOTE_TABLE[keyCode]
                    else:
                        keyName += 'PAD_PAD_0x' + format(keyCode, '02X')
                    waitTime = conf.PADPADwaitTime

                elif (keyType == IMON_82):
                    keyName = '82.'
                    if (keyCode in IMON_82_TABLE):
                        keyName += IMON_82_TABLE[keyCode]
                    else:
                        keyName += '82_0x' + format(keyCode, '02X')

                elif (keyType == IMON_FRONT):
                    keyName = 'Front.'
                    if (keyCode in IMON_FRONT_TABLE):
                        keyName += IMON_FRONT_TABLE[keyCode]
                    else:
                        keyName += 'BUTTON_0x' + format(keyCode, '02X')
                    waitTime = conf.FRONTwaitTime

                elif (keyType == IMON_FRONT_KNOB):
                    keyName = 'Front.Volume'

                if (waitTime is not None) and waitTime:
                    lastEvent = self.TriggerEnduringEvent(keyName, payload=event.arg1)
                    lastkeyCode = event.code
                else:
                    lastEvent = self.TriggerEvent(keyName, payload=event.arg1)
                    lastkeyCode = None
                    waitTime = None

            self.EventsQueue.task_done()

    def TranslateMouseToKeypress(self, dx, dy):
        dxAbs = abs(dx)
        dyAbs = abs(dy)
        if (max(dxAbs, dyAbs) > conf.keyPadSensitivity):
            if (dxAbs > dyAbs):  # horizontal movement is larger, so it has preference
                if (dx == dxAbs):
                    return IMON_PAD_BUTTON_RIGHT
                else:
                    return IMON_PAD_BUTTON_LEFT
            elif (dxAbs < dyAbs):  # vertical movement is larger, so it has preference
                if (dy == dyAbs):
                    return IMON_PAD_BUTTON_DOWN
                else:
                    return IMON_PAD_BUTTON_UP
            else:
                return 0
        else:
            return 0

    def StopCallback(self):
        self.TriggerEvent("Stopped")
        self.thread = None

    def GetMyDevicePath(self):
        path = GetDevicePath(
            self.devicePath,
            self.vendorID,
            self.productID,
            self.versionNumber,
            self.useDeviceIndex,
            self.deviceIndex,
            self.noOtherPort)
        return path;

    def SetupHidThread(self, newDevicePath):
        # create thread
        self.thread = HIDThread(self.vendorString + " " + self.productString, newDevicePath)
        self.thread.start()
        self.thread.SetStopCallback(self.StopCallback)
        self.thread.SetRawCallback(self.RawCallback)

    def ReconnectDevice(self, event):
        # method to reconnect a disconnect device
        if self.thread == None:
            if not IsDeviceName(event.payload, self.vendorID, self.productID):
                return

            # check if the right device was connected
            # getting devicePath
            newDevicePath = self.GetMyDevicePath()
            if not newDevicePath:
                # wrong device
                return

            self.SetupHidThread(newDevicePath)

    def __start__(self,
                  eventName,
                  noOtherPort,
                  devicePath,
                  vendorID,
                  vendorString,
                  productID,
                  productString,
                  versionNumber,
                  useDeviceIndex=False,
                  deviceIndex=0
                  ):
        # saving parameters so they can be used to reconnect a device
        self.eventName = eventName
        self.noOtherPort = noOtherPort
        self.devicePath = devicePath
        self.vendorID = vendorID
        self.vendorString = vendorString
        self.productID = productID
        self.productString = productString
        self.versionNumber = versionNumber
        self.useDeviceIndex = useDeviceIndex
        self.deviceIndex = deviceIndex
        self.oldValues = {}

        if eventName:
            self.info.eventPrefix = eventName
        else:
            self.info.eventPrefix = "iMON"

        # Bind plug in to RegisterDeviceNotification message
        eg.Bind("System.DeviceAttached", self.ReconnectDevice)

        newDevicePath = self.GetMyDevicePath()
        if not newDevicePath:
            # device not found
            self.PrintError(Text.errorFind)
        else:
            self.SetupHidThread(newDevicePath)

        self.EventsQueue = Queue(5)
        self.repThread = threading.Thread(
            target=self.repThreadLoop,
            name="repThread",
        )
        self.repThread.start()

    def __stop__(self):
        if self.thread:
            self.thread.AbortThread()

        # unbind from RegisterDeviceNotification message
        eg.Unbind("System.DeviceAttached", self.ReconnectDevice)

        if self.repThread:
            self.EventsQueue.put(None)

    def Configure(self,
                  eventName="",
                  noOtherPort=False,
                  devicePath=None,
                  vendorID=None,
                  vendorString=None,
                  productID=None,
                  productString=None,
                  versionNumber=None,
                  useDeviceIndex=False,
                  deviceIndex=0
                  ):
        deviceList = GetDeviceDescriptions()
        panel = eg.ConfigPanel(self, resizable=True)

        # building dialog
        hidList = wx.ListCtrl(panel, -1, pos=wx.DefaultPosition,
                              size=wx.DefaultSize, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        # create GUI
        hidList.InsertColumn(0, Text.deviceID)
        hidList.InsertColumn(1, Text.versionID)
        hidList.InsertColumn(2, Text.connected)

        path = GetDevicePath(
            devicePath,
            vendorID,
            productID,
            versionNumber,
            useDeviceIndex,
            deviceIndex,
            noOtherPort,
            deviceList)

        # fill list
        devices = {}
        idx = 0
        for item in deviceList:
            if (item.vendorId == 0x15C2):
                idx = hidList.InsertStringItem(sys.maxint, format(item.productId, '04X'))
                hidList.SetStringItem(idx, 1, format(item.versionNumber, '04X'))
                hidList.SetStringItem(idx, 2, Text.yes)
                if item.devicePath == path:
                    hidList.Select(idx)
                devices[idx] = item

        # add not connected device to bottom of list
        if not path and devicePath:
            item = DeviceDescription(
                devicePath,
                vendorID,
                vendorString,
                productID,
                productString,
                versionNumber)
            idx = hidList.InsertStringItem(sys.maxint, format(item.productId, '04X'))
            hidList.SetStringItem(idx, 1, format(item.versionNumber, '04X'))
            hidList.SetStringItem(idx, 2, Text.no)
            hidList.Select(idx)
            devices[idx] = item

        # no device selected, disable ok and apply button
        panel.EnableButtons(hidList.GetFirstSelected() != -1)

        # layout
        for i in range(hidList.GetColumnCount()):
            hidList.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            size = hidList.GetColumnWidth(i)
            hidList.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            hidList.SetColumnWidth(i, max(size, hidList.GetColumnWidth(i) + 5))

        panel.sizer.Add(hidList, 1, flag=wx.EXPAND)

        # sizers
        optionsSizer = wx.GridBagSizer(0, 5)

        # eventname
        optionsSizer.Add(
            wx.StaticText(panel, -1, Text.eventName),
            (0, 0),
            flag=wx.ALIGN_CENTER_VERTICAL)
        eventNameCtrl = wx.TextCtrl(panel, value=eventName)
        eventNameCtrl.SetMaxLength(32)
        optionsSizer.Add(eventNameCtrl, (0, 1), (1, 2), flag=wx.EXPAND)

        # text
        optionsSizer.Add(
            wx.StaticText(panel, -1, Text.multipleDeviceOptions),
            (3, 0), (1, 3),
            flag=wx.ALIGN_CENTER_VERTICAL)

        # checkbox for use first device
        useDeviceIndexCtrl = wx.CheckBox(panel, -1, Text.useDeviceIndex)
        useDeviceIndexCtrl.SetValue(useDeviceIndex)
        optionsSizer.Add(useDeviceIndexCtrl, (4, 0), (1, 2), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        # device index spin control
        deviceIndexCtrl = eg.SpinIntCtrl(panel, -1, deviceIndex, 0, 99, size=(100, -1))
        optionsSizer.Add(deviceIndexCtrl, (4, 2), (1, 1))

        # checkbox for no other port option
        noOtherPortCtrl = wx.CheckBox(panel, -1, Text.noOtherPort)
        noOtherPortCtrl.SetValue(noOtherPort)
        optionsSizer.Add(noOtherPortCtrl, (5, 0), (1, 3))

        panel.sizer.Add(optionsSizer, 0, wx.TOP, 10)

        def OnHidListSelect(event):
            panel.EnableButtons(hidList.GetFirstSelected() != -1)
            event.Skip()

        def OnUseDeviceIndexCtrlChange(event):
            noOtherPortCtrl.Enable(not useDeviceIndexCtrl.GetValue())
            deviceIndexCtrl.Enable(useDeviceIndexCtrl.GetValue())
            event.Skip()

        def OnNoOtherPortChange(event):
            useDeviceIndexCtrl.Enable(not noOtherPortCtrl.GetValue())
            deviceIndexCtrl.Enable(not noOtherPortCtrl.GetValue())
            event.Skip()

        OnUseDeviceIndexCtrlChange(wx.CommandEvent())
        OnNoOtherPortChange(wx.CommandEvent())
        useDeviceIndexCtrl.Bind(wx.EVT_CHECKBOX, OnUseDeviceIndexCtrlChange)
        noOtherPortCtrl.Bind(wx.EVT_CHECKBOX, OnNoOtherPortChange)
        hidList.Bind(wx.EVT_LIST_ITEM_SELECTED, OnHidListSelect)
        hidList.Bind(wx.EVT_LIST_ITEM_DESELECTED, OnHidListSelect)

        while panel.Affirmed():
            device = devices[hidList.GetFirstSelected()]
            panel.SetResult(
                eventNameCtrl.GetValue(),
                noOtherPortCtrl.GetValue(),
                device.devicePath,
                device.vendorId,
                device.vendorString,
                device.productId,
                device.productString,
                device.versionNumber,
                useDeviceIndexCtrl.GetValue(),
                deviceIndexCtrl.GetValue(),
            )

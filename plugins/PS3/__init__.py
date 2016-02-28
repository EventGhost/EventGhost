README = """\
<u><b>1) Bluetooth</b></u>

Tested succesfully working with Bluetooth Software :
WIDCOMM Bluetooth Software 5.1.0.1100.

5.1.0.1100 is not the last version, but it's the most versatile version and
works with most of Bluetooth adapter in a patched version.
See <a href"http://forum.gsmhosting.com/vbb/forumdisplay.php?f=237">
this thread</a> to help about patched WIDCOMM Bluetooth Software 5.1.0.1100
(Restart PC, right click on bluetooth icon in task bar and stop/start bluetooth
device can help)

On remote, to activate discoverable mode, press simultaneously "start+enter".
On PC choose "Next (no code)"

Check in "Device Manager" / "Human Interface Devices" that the
PS3 Remote appears as "HID-compliant game controller".
If not, if it appears as "HID Keyboard Device" in "Keyboards",
delete it, right click on bluetooth icon in task bar and
stop/start bluetooth device to force new device detection.
This time should appears as "HID-compliant game controller"

<u><b>2) Plugin</b></u>

The plugin will also automatically re-detect the PS3 remote after being in standby mode.

<u><b>3) Changelog</b></u>

4.0.2:<br>
Added support for 5 new BT buttons on 2011 PS3 remote:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. '-/--'<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. 'ChanUp'<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. 'ChanDown'<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. 'InstantNext'<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. 'InstantPrev'<br>

4.0.3:<br>
Added Blu-Link Universal/PS3 Remote support (VID=0x609/PID=0x306).

4.0.4:<br>
Fix batteryLevel "out of range" error.

"""

eg.RegisterPlugin(
    name = "PlayStation 3 Bluetooth Remote",
    author = (
        "Thierry Couquillou",
        "Tim Delaney",
        "Chris Heitkamp",
        "Peter Mathiasson",
        "Eric Hodgerson",
    ),
    version = "4.0.4",
    kind = "remote",
    guid = "{7224079E-1823-48B0-8ED6-30973BDDC96D}",
    url = "http://www.eventghost.org/forum/viewtopic.php?t=640",
    description = "Hardware plugin for the PS3 Bluetooth Remote (based on the HID code of Bartman)",
    canMultiLoad = True,
    help = README,
    createMacrosOnAdd = True,
)

import time
import binascii
import sys
import wx.lib.mixins.listctrl as listmix
from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import GetDeviceDescriptions
from eg.WinApi.HID import DeviceDescription

class Text:
    manufacturer = "Manufacturer"
    deviceName = "Device Name"
    connected = "Connected"
    eventName = "Event prefix (optional):"
    yes = "Yes"
    no = "No"
    enduringEvents = "Trigger enduring events for buttons"
    multipleDeviceOptions = "Options for multiple same devices"
    noOtherPort = "Use selected device only if connected to current port"
    useDeviceIndex = "Use the device with index"
    errorFind = "Error finding HID device: "
    vendorID = "Vendor ID "
    batteryLevel= [
        "empty",
        "almost  empty",
        "low",
        "good",
        "almost full",
        "full"
    ]
    eventsSettings = "Remote Events Settings"
    ps3Settings = "PS3 Remote Events Settings"
    ps3Release = "Generate PS3 Remote Button.None event"
    sleepTime = "Sleep event generated after"
    hibernateTime = "Hibernate event generated after"
    seconds = "seconds"
    enteredLowPower = "%s entered low-power mode"
    exitedLowPower = "%s exited low-power mode"


class PS3Remote:
    """Helper class. Contains only button and button mask definitions"""
    button = {
        0x00: 'Num1',
        0x01: 'Num2',
        0x02: 'Num3',
        0x03: 'Num4',
        0x04: 'Num5',
        0x05: 'Num6',
        0x06: 'Num7',
        0x07: 'Num8',
        0x08: 'Num9',
        0x09: 'Num0',
        0x0B: 'Enter',
        0x0C: '-/--',  #2011 remote
        0x0E: 'Return',
        0x0F: 'Clear',
        0x10: 'ChanUp',  #2011 remote
        0x11: 'ChanDown',  #2011 remote
        0x16: 'Eject',
        0x1A: 'TopMenu',
        0x28: 'Time',
        0x30: 'Prev',
        0x31: 'Next',
        0x32: 'Play',
        0x33: 'ScanBack',
        0x34: 'ScanFwd',
        0x38: 'Stop',
        0x39: 'Pause',
        0x40: 'PopUpMenu',
        0x43: 'PS',
        0x50: 'Select',
        0x51: 'L3',
        0x52: 'R3',
        0x53: 'Start',
        0x54: 'Up',
        0x55: 'Right',
        0x56: 'Down',
        0x57: 'Left',
        0x58: 'L2',
        0x59: 'R2',
        0x5A: 'L1',
        0x5B: 'R1',
        0x5C: 'Triangle',
        0x5D: 'Circle',
        0x5E: 'Cross',
        0x5F: 'Square',
        0x60: 'StepBack',
        0x61: 'StepFwd',
        0x63: 'Subtitle',
        0x64: 'Audio',
        0x65: 'Angle',
        0x70: 'Display',
        0x75: 'InstantNext',  #2011 remote
        0x76: 'InstantPrev',  #2011 remote
        0x80: 'Blue',
        0x81: 'Red',
        0x82: 'Green',
        0x83: 'Yellow',
    }

    maskbit = {
        0x00: 'PS',
        0x03: 'Enter',
        0x08: 'L2',
        0x09: 'R2',
        0x0A: 'L1',
        0x0B: 'R1',
        0x0C: 'Triangle',
        0x0D: 'Circle',
        0x0E: 'Cross',
        0x0F: 'Square',
        0x10: 'Select',
        0x11: 'L3',
        0x12: 'R3',
        0x13: 'Start',
        0x14: 'Top',
        0x15: 'Right',
        0x16: 'Down',
        0x17: 'Left',
    }


class PS3ParseError(Exception):
    def __init__(self, what, expected, received):
        self.what= what
        self.expected= expected
        self.received= received

    def __str__(self):
        return 'Parse error! Errornous %s. Received: %s - Expected: %s' % (
            str(self.what),
            str(self.received),
            str(self.expected)
        )


class HIDPS3(eg.PluginClass):
    def __init__(self):
        self.text = Text
        self.thread = None
        self.PS3Remote = PS3Remote
        self.batteryLevel = None
        self.AddAction(GetBatteryLevel)

    def RawCallback(self, data):
        #hexdata= binascii.hexlify(data).upper()
        #eg.PrintNotice( hexdata )

        try:
            if len(data) != 12:
                raise PS3ParseError( 'length', 12, len(data) )

            start= ord( data[0] )
            mask= ord( data[1] )<<16 | ord( data[2] )<<8 | ord( data[3] )
            code= ord( data[4] )
            dummy= data[5:10]
            state= ord( data[10] )
            battery= ord( data[11] )

            if start != 0x01:
                raise PS3ParseError( 'data[0]', '0x01', hex(start) )

            if dummy != "\xff\xff\xff\xff\xff":
                raise PS3ParseError( 'data[5:10]', '0xffffffffff', hex(dummy) )

            if battery > 0x05:
                raise PS3ParseError( 'battery level', '0-5', battery )

            if( battery < 0x02 ):
                eg.PrintNotice(
                    'PS3 Remote: Battery Level: ' +
                        self.text.batteryLevel[battery]
                )

            #self.TriggerEvent(
            #    'Code: ' + hex(code) +
            #        ' State: ' + hex(state) +
            #        ' Battery Level: ' + str(battery) + ':' +
            #        self.text.batteryLevel[battery] +
            #        '  Mask: ' + bin(mask),
            #    payload= ( battery, self.text.batteryLevel[battery] )
            #)

            if( code != 0xff and code not in self.PS3Remote.button ):
                raise PS3ParseError( 'Key code', 'various', hex(code) )

            btnPressed = []

            if( code != 0xff ):
                # single button pressed
                btnPressed.append( self.PS3Remote.button[code] )
            else:
                # multiple buttons pressed
                if( mask != 0x00 ):
                    for bit in range( 24 ):
                        if( mask & 1<<bit ):
                            if( bit not in self.PS3Remote.maskbit ):
                                PS3ParseError( 'Mask', 'various', bin(mask) )
                            btnPressed.append( self.PS3Remote.maskbit[bit] )
                    if btnPressed == []:
                        PS3ParseError( 'Mask', 'various','Empty Mask' )

            if btnPressed != []:
                evtName = 'Button.' + '+'.join(btnPressed)
                if self.enduringEvents:
                    self.TriggerEnduringEvent(evtName)
                else:
                    self.TriggerEvent(evtName)
            elif self.enduringEvents:
                #no buttons pressed anymore
                self.EndLastEvent()
            elif self.ps3Release:
                #trigger event so that releasing all buttons
                #can get noticed even w/o enduring events
                self.TriggerEvent( 'Button.None' )

            self.batteryLevel= battery

        except PS3ParseError as catchedError:
            eg.PrintError(
                'PS3-HID Plugin: ' + catchedError +
                '  Data: 0x' + binascii.hexlify(data).lower()
            )

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
        #create thread
        self.thread = HIDThread(
            self.vendorString + " " + self.productString, newDevicePath
        )
        self.thread.start()
        self.thread.SetStopCallback(self.StopCallback)
        self.thread.SetRawCallback(self.RawCallback)

    def ReconnectDevice(self, event):
        """method to reconnect a disconnect device"""
        if self.thread == None:
            #updating device list

            #check if the right device was connected
            #getting devicePath
            newDevicePath = self.GetMyDevicePath()
            if not newDevicePath:
                #wrong device
                return

            self.SetupHidThread(newDevicePath)

    def GetLabel(self,
        eventName,
        enduringEvents,
        rawDataEvents,
        ps3DataEvents,
        ps3Release,
        ps3Zone,
        shortKeyTime,
        longKeyTime,
        sleepTime,
        hibernateTime,
        noOtherPort,
        devicePath,
        vendorID,
        vendorString,
        productID,
        productString,
        versionNumber,
        # For backwards-compatibility with 2.0.2 and 3.0.0 - if a new config option is added this can just be replaced
        dummy = None,
        useDeviceIndex = False,
        deviceIndex = 0
    ):
        prefix = "PS3: "
        #one or both strings empty should not happen
        if not vendorString or not productString:
            return "PS3"

        #productString already contains manufacturer or vendor id only
        if productString.find(vendorString) != -1 or\
            vendorString[0:len(self.text.vendorID)] == self.text.vendorID:
            return prefix + productString

        return prefix + vendorString + " " + productString

    def __start__(self,
        eventName,
        enduringEvents,
        rawDataEvents,
        ps3DataEvents,
        ps3Release,
        ps3Zone,
        shortKeyTime,
        longKeyTime,
        sleepTime,
        hibernateTime,
        noOtherPort,
        devicePath,
        vendorID,
        vendorString,
        productID,
        productString,
        versionNumber,
        # For backwards-compatibility with 2.0.2 and 3.0.0 - if a new config option is added this can just be replaced
        dummy = None,
        useDeviceIndex = False,
        deviceIndex = 0
    ):

        #saving parameters so they can be used to reconnect a device
        self.eventName = eventName
        self.enduringEvents = enduringEvents
        self.noOtherPort = noOtherPort
        self.devicePath = devicePath
        self.vendorID = vendorID
        self.vendorString = vendorString
        self.productID = productID
        self.productString = productString
        self.versionNumber = versionNumber
        self.useDeviceIndex = useDeviceIndex
        self.deviceIndex = deviceIndex
        self.ps3Release = ps3Release
        self.oldValues = {}

        if eventName:
            self.info.eventPrefix = eventName
        else:
            self.info.eventPrefix = "PS3"

        #Bind plug in to RegisterDeviceNotification message
        eg.Bind("System.DeviceAttached", self.ReconnectDevice)

        newDevicePath = self.GetMyDevicePath()
        if not newDevicePath:
            #device not found
            self.PrintError(Text.errorFind)
        else:
            self.SetupHidThread(newDevicePath)

    def __stop__(self):
        if self.thread:
            self.thread.AbortThread()

        #unbind from RegisterDeviceNotification message
        eg.Unbind("System.DeviceAttached", self.ReconnectDevice)

    def Configure(self,
        eventName = "",
        enduringEvents = True,
        rawDataEvents = False, # no longer used
        ps3DataEvents = False, # no longer used
        ps3Release = False,
        ps3Zone = False, # no longer used
        shortKeyTime = 0.0, # no longer used
        longKeyTime = 0.0, # no longer used
        sleepTime = 5.0,
        hibernateTime = 60.0,
        noOtherPort = False,
        devicePath = None,
        vendorID = None,
        vendorString = None,
        productID = None,
        productString = None,
        versionNumber = None,
        # For backwards-compatibility with 2.0.2 and 3.0.0 - if a new config option is added this can just be replaced
        dummy = None,
        useDeviceIndex = False,
        deviceIndex = 0
    ):
        deviceList = GetDeviceDescriptions()
        panel = eg.ConfigPanel(self, resizable=True)

        #building dialog
        hidList = wx.ListCtrl(panel, -1, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        #create GUI
        hidList.InsertColumn(0, self.text.deviceName)
        hidList.InsertColumn(1, self.text.manufacturer)
        hidList.InsertColumn(2, self.text.connected)

        path = GetDevicePath(
            devicePath,
            vendorID,
            productID,
            versionNumber,
            noOtherPort,
            useDeviceIndex,
            deviceIndex,
            deviceList)

        #fill list
        devices = {}
        idx = 0
        for item in deviceList:
            # eg.Print("VID=%X, PID=%X, name=%s" %(item.vendorId, item.productId, item.productString))
            # filter device list - list only match VID:PID
            if(
                ( ( item.vendorId == 0x054C or item.vendorId == 0x609 ) and item.productId == 0x0306 ) or
                item.devicePath == path
            ):
                idx = hidList.InsertStringItem(sys.maxint, item.productString)
                hidList.SetStringItem(idx, 1, item.vendorString)
                hidList.SetStringItem(idx, 2, self.text.yes)
                if item.devicePath == path:
                    hidList.Select(idx)
                devices[idx] = item

        #add not connected device to bottom of list
        if not path and devicePath:
            item = DeviceDescription(
                devicePath,
                vendorID,
                vendorString,
                productID,
                productString,
                versionNumber)
            idx = hidList.InsertStringItem(sys.maxint, item.productString)
            hidList.SetStringItem(idx, 1, item.vendorString)
            hidList.SetStringItem(idx, 2, self.text.no)
            hidList.Select(idx)
            devices[idx] = item

        #no device selected, disable ok and apply button
        panel.EnableButtons(hidList.GetFirstSelected() != -1)

        #layout
        for i in range(hidList.GetColumnCount()):
            hidList.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            size = hidList.GetColumnWidth(i)
            hidList.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            hidList.SetColumnWidth(i, max(size, hidList.GetColumnWidth(i) + 5))

        panel.sizer.Add(hidList, 1, flag = wx.EXPAND)

        #sizers
        optionsSizer = wx.GridBagSizer(0, 5)

        #eventname
        optionsSizer.Add(
            wx.StaticText(panel, -1, self.text.eventName),
            (0, 0),
            flag = wx.ALIGN_CENTER_VERTICAL)
        eventNameCtrl = wx.TextCtrl(panel, value = eventName)
        eventNameCtrl.SetMaxLength(32)
        optionsSizer.Add(eventNameCtrl, (0, 1), (1, 2), flag = wx.EXPAND)

        #checkbox for enduring event option
        enduringEventsCtrl = wx.CheckBox(panel, -1, self.text.enduringEvents)
        enduringEventsCtrl.SetValue(enduringEvents)
        optionsSizer.Add(enduringEventsCtrl, (1, 0), (1, 3))

        #text
        optionsSizer.Add(
            wx.StaticText(panel, -1, self.text.multipleDeviceOptions),
            (3, 0), (1, 3),
            flag = wx.ALIGN_CENTER_VERTICAL)

        #checkbox for use first device
        useDeviceIndexCtrl = wx.CheckBox(panel, -1, self.text.useDeviceIndex)
        useDeviceIndexCtrl.SetValue(useDeviceIndex)
        optionsSizer.Add(useDeviceIndexCtrl, (4, 0), (1, 2), flag = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        #device index spin control
        deviceIndexCtrl = eg.SpinIntCtrl(panel, -1, deviceIndex, 0, 99, size=(100,-1))
        optionsSizer.Add(deviceIndexCtrl, (4, 2), (1, 1))

        #checkbox for no other port option
        noOtherPortCtrl = wx.CheckBox(panel, -1, self.text.noOtherPort)
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

        ######################################################################

        panel.sizer.Add((15,15))

        #sizers
        ps3GroupSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, self.text.ps3Settings),
            wx.VERTICAL
        )

        ps3Sizer = wx.GridBagSizer(0, 5)

        #checkbox for ps3 release event
        ps3ReleaseCtrl = wx.CheckBox(panel, -1, self.text.ps3Release)
        ps3ReleaseCtrl.SetValue(ps3Release)
        ps3Sizer.Add(ps3ReleaseCtrl, (0, 0), (1, 3))

        #sleep time
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.sleepTime),
            (2, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        sleepTimeCtrl = eg.SpinNumCtrl(
            panel, -1, sleepTime, size=(200,-1), integerWidth=7, increment=1.00
        )
        ps3Sizer.Add(sleepTimeCtrl, (2, 1), flag = wx.EXPAND)
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.seconds),
            (2, 2), (1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL)

        #hibernate time
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.hibernateTime),
            (3, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        hibernateTimeCtrl = eg.SpinNumCtrl(
            panel, -1, hibernateTime, size=(200,-1), integerWidth=7, increment=1.00
        )
        ps3Sizer.Add(hibernateTimeCtrl, (3, 1), flag = wx.EXPAND)
        ps3Sizer.Add(
            wx.StaticText(panel, -1, self.text.seconds),
            (3, 2), (1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL)

        ps3GroupSizer.Add(ps3Sizer, 0, wx.ALL, 10)
        panel.sizer.Add(ps3GroupSizer, 0, wx.EXPAND)

        def OnEnduringEventsChange(event):
            ps3ReleaseCtrl.Enable( not enduringEventsCtrl.GetValue() )
            event.Skip()

        OnEnduringEventsChange(wx.CommandEvent())

        enduringEventsCtrl.Bind(wx.EVT_CHECKBOX, OnEnduringEventsChange)

        ######################################################################

        while panel.Affirmed():
            device = devices[hidList.GetFirstSelected()]
            panel.SetResult(
                eventNameCtrl.GetValue(),
                enduringEventsCtrl.GetValue(),
                False,
                True,
                ps3ReleaseCtrl.GetValue(),
                False,
                0.0,
                0.0,
                sleepTimeCtrl.GetValue(),
                hibernateTimeCtrl.GetValue(),
                noOtherPortCtrl.GetValue(),
                device.devicePath,
                device.vendorId,
                device.vendorString,
                device.productId,
                device.productString,
                device.versionNumber,
                useDeviceIndexCtrl.GetValue(),
            )


class GetBatteryLevel(eg.ActionClass):
    name = "Get battery level"
    description = """Returns last send battery level
        Possible values are 0..5 (empty..full)
        or None, if no keypress received up to now"""

    def __call__(self):
        return self.plugin.batteryLevel

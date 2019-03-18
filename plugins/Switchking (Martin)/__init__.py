import eg

eg.RegisterPlugin(
    name="Switchking",
    guid='{610D5619-E6DB-47A2-9CF5-634E80785457}',
    author="Martin Engstrom",
    version="0.0.4",
    canMultiLoad=True,
    kind="external",
    url="http://code.google.com/p/eventghost-switchking-plugin/",
    description='Plugin to control TellStick devices via Switchking REST API. Author: Martin Engstrom. Thanks Telldus for making great products and Switchking for making Tellsticks even more useful.',
)

import re, htmlentitydefs
import httplib
import base64
from xml.dom.minidom import parseString


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is

    return re.sub("&#?\w+;", fixup, text)


class swki:

    def __init__(self):
        self.headers = {}
        self.user = ''
        self.password = ''
        self.host = ''
        self.port = ''
        self.ids = {}
        self.lst = []
        self.dimlst = []
        self.grpids = {}
        self.grplst = []
        self.scenids = {}
        self.scenlst = []
        self.dsids = {}
        self.dslst = []

    def Prime(self, host, port, user, password):
        self.user = user
        self.password = password
        self.host = host
        self.port = unicode(port)
        self.headers["Authorization"] = "Basic {0}".format(base64.b64encode("{0}:{1}".format(user, password)))
        self.headers["Connection"] = "Keep-Alive"

    #        self.headers["Accept-Encoding"] = "*/*"

    def GetDevices(self):
        self.ids = {}
        self.lst = []
        self.dimlst = []
        conn = httplib.HTTPConnection(self.host + ":" + self.port)
        conn.request('GET', "http://" + self.host + ":" + self.port + '/devices', None, self.headers)
        resp = conn.getresponse()
        content = resp.read()
        dom = parseString(content)
        devices = dom.getElementsByTagName("RESTDevice")
        for device in devices:
            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
            dev_nm = unescape(device.getElementsByTagName("Name")[0].childNodes[0].data)
            dimmer = device.getElementsByTagName("SupportsAbsoluteDimLvl")[0].childNodes[0].data
            if (dimmer == "true"):
                self.dimlst.append(dev_nm)
            self.ids[dev_nm] = dev_id
            self.lst.append(dev_nm)
        return self.lst, self.dimlst

    def GetDeviceGroups(self):
        self.grpids = {}
        self.grplst = []
        conn = httplib.HTTPConnection(self.host + ":" + self.port)
        conn.request('GET', "http://" + self.host + ":" + self.port + '/devicegroups', None, self.headers)
        resp = conn.getresponse()
        content = resp.read()
        dom = parseString(content)
        devices = dom.getElementsByTagName("RESTDeviceGroup")
        for device in devices:
            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
            if (dev_id == "-1"):
                continue
            dev_nm = device.getElementsByTagName("Name")[0].childNodes[0].data
            dev_nm = unescape(dev_nm)
            self.grpids[dev_nm] = dev_id
            self.grplst.append(dev_nm)
        return self.grplst

    def GetScenarios(self):
        self.scenids = {}
        self.scenlst = []
        conn = httplib.HTTPConnection(self.host + ":" + self.port)
        conn.request('GET', "http://" + self.host + ":" + self.port + '/scenarios', None, self.headers)
        resp = conn.getresponse()
        content = resp.read()
        dom = parseString(content)
        devices = dom.getElementsByTagName("RESTScenario")
        for device in devices:
            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
            dev_nm = unescape(device.getElementsByTagName("Name")[0].childNodes[0].data)
            self.scenids[dev_nm] = dev_id
            self.scenlst.append(dev_nm)
        return self.scenlst

    def GetDataSources(self):
        self.dsids = {}
        self.dslst = []
        conn = httplib.HTTPConnection(self.host + ":" + self.port)
        conn.request('GET', "http://" + self.host + ":" + self.port + '/datasources', None, self.headers)
        resp = conn.getresponse()
        content = resp.read()
        dom = parseString(content)
        devices = dom.getElementsByTagName("RESTDataSource")
        for device in devices:
            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
            dev_nm = unescape(device.getElementsByTagName("Name")[0].childNodes[0].data)
            self.dsids[dev_nm] = dev_id
            self.dslst.append(dev_nm)
        return self.dslst

    def SetDevice(self, devnm, command):
        devid = self.ids[devnm]
        headers = self.headers
        user = self.user
        password = self.password
        host = self.host
        port = self.port
        conn = httplib.HTTPConnection(host + ":" + port)
        conn.request('GET', "http://" + host + ":" + port + '/devices/' + devid + '/' + command, None, headers)

    def SetDeviceGroup(self, grpnm, command):
        devid = self.grpids[grpnm]
        headers = self.headers
        user = self.user

        host = self.host
        port = self.port
        conn = httplib.HTTPConnection(host + ":" + port)
        conn.request('GET', "http://" + host + ":" + port + '/devicegroups/' + devid + '/' + command, None, headers)

    def SetScenario(self, grpnm):
        devid = self.scenids[grpnm]
        headers = self.headers
        user = self.user
        password = self.password
        host = self.host
        port = self.port
        conn = httplib.HTTPConnection(host + ":" + port)
        conn.request('GET',
                     "http://" + host + ":" + port + '/commandqueue?operation=changescenario&target=' + devid + '&param1=&param2=&param3=',
                     None, headers)

    def SetDataSource(self, grpnm, value):
        devid = self.dsids[grpnm]
        headers = self.headers
        user = self.user
        password = self.password
        host = self.host
        port = self.port
        conn = httplib.HTTPConnection(host + ":" + port)
        conn.request('GET', "http://" + host + ":" + port + '/datasources/' + devid + '/addvalue?value=' + value, None,
                     headers)


class SwitchkingTellStick(eg.PluginClass):

    def __init__(self):
        self.AddAction(DevTurnOn)
        self.AddAction(DevTurnOff)
        self.AddAction(DevDim)
        self.AddAction(DevGrpTurnOn)
        self.AddAction(DevGrpTurnOff)
        self.AddAction(ScenAct)
        self.AddAction(DSSet)
        self.sk = swki()

    def __start__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.sk.Prime(host, port, user, password)
        dummy = self.sk.GetDevices()
        dummy = self.sk.GetDeviceGroups()
        dummy = self.sk.GetScenarios()
        dummy = self.sk.GetDataSources()

    def Configure(self, host="localhost", port=8800, user="", password=""):
        panel = eg.ConfigPanel()

        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        userCtrl = panel.TextCtrl(user)
        passwordCtrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)
        st1 = panel.StaticText("Host:")
        st2 = panel.StaticText("Port:")
        st3 = panel.StaticText("User:")
        st4 = panel.StaticText("Password:")
        eg.EqualizeWidths((st1, st2, st3, st4))
        box1 = panel.BoxedGroup("Server", (st1, hostCtrl), (st2, portCtrl))
        box2 = panel.BoxedGroup("Credentials", (st3, userCtrl), (st4, passwordCtrl))

        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND | wx.TOP, 10),
        ])

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                userCtrl.GetValue(),
                passwordCtrl.GetValue(),
            )


class DevTurnOn(eg.ActionClass):
    name = "Device ON"
    description = "Turns on a TellStick device."
    iconFile = "DeviceOn"

    def __init__(self):
        self.devicename = ""
        self.selection = 0

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDevice(devicename, "turnon")

    def Configure(self, devicename="", selection=0):
        panel = eg.ConfigPanel()
        self.selection = selection
        dl, dummy = self.plugin.sk.GetDevices()
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        deviceControl.Select(selection)
        while panel.Affirmed():
            panel.SetResult(deviceControl.GetStringSelection(), deviceControl.GetSelection())


class DevTurnOff(eg.ActionClass):
    name = "Device OFF"
    description = "Turns off a TellStick device."
    iconFile = "DeviceOff"

    def __init__(self):
        self.devicename = ""
        self.selection = 0

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDevice(devicename, "turnoff")

    def Configure(self, devicename="", selection=0):
        panel = eg.ConfigPanel()
        # self.selection = selection
        dl, dummy = self.plugin.sk.GetDevices()
        # __init__(self, parent, id, pos, size, choices, style, validator, name)
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        deviceControl.Select(selection)
        while panel.Affirmed():
            panel.SetResult(deviceControl.GetStringSelection(), deviceControl.GetSelection())


class DevGrpTurnOn(eg.ActionClass):
    name = "Device Group ON"
    description = "Turns on a Switchking device group."
    iconFile = "DeviceGroupOn"

    def __init__(self):
        self.devicename = ""
        self.selection = 0

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDeviceGroup(devicename, "turnon")

    def Configure(self, devicename="", selection=0):
        panel = eg.ConfigPanel()
        self.selection = selection
        dl = self.plugin.sk.GetDeviceGroups()
        # __init__(self, parent, id, pos, size, choices, style, validator, name)
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        deviceControl.Select(selection)
        while panel.Affirmed():
            panel.SetResult(deviceControl.GetStringSelection(), deviceControl.GetSelection())


class DevGrpTurnOff(eg.ActionClass):
    name = "Device Group OFF"
    description = "Turns off a Switchking device group."
    iconFile = "DeviceGroupOff"

    def __init__(self):
        self.devicename = ""
        self.selection = 0

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDeviceGroup(devicename, "turnoff")

    def Configure(self, devicename="", selection=0):
        panel = eg.ConfigPanel()
        self.selection = selection
        dl = self.plugin.sk.GetDeviceGroups()
        # __init__(self, parent, id, pos, size, choices, style, validator, name)
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        deviceControl.Select(selection)
        while panel.Affirmed():
            panel.SetResult(deviceControl.GetStringSelection(), deviceControl.GetSelection())


class ScenAct(eg.ActionClass):
    name = "Scenario Activate"
    description = "Activates a Switchking scenario."
    iconFile = "Scenario"

    def __init__(self):
        self.devicename = ""
        self.selection = 0

    def __call__(self, devicename, selection):
        self.plugin.sk.SetScenario(devicename)

    def Configure(self, devicename="", selection=0):
        panel = eg.ConfigPanel()
        self.selection = selection
        dl = self.plugin.sk.GetScenarios()
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        deviceControl.Select(selection)
        while panel.Affirmed():
            panel.SetResult(deviceControl.GetStringSelection(), deviceControl.GetSelection())


class DSSet(eg.ActionClass):
    name = "Datasource, Set Value"
    description = "Set a value to a Switchking data source."
    iconFile = "DataSource"

    def __init__(self):
        self.devicename = ""
        self.value = ""
        self.selction = 0

    def __call__(self, dummy, devicename, value, selection):
        self.plugin.sk.SetDataSource(devicename, value)

    def Configure(self, dummy="", devicename="", value="0", selection=0):
        panel = eg.ConfigPanel()
        self.value = value
        self.selection = selection
        dl = self.plugin.sk.GetDataSources()

        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        deviceControl.Select(selection)
        valueEdit = panel.TextCtrl(value)
        panel.AddLine("Value: ", valueEdit)
        while panel.Affirmed():
            name = deviceControl.GetStringSelection() + ": " + unicode(valueEdit.GetValue())
            panel.SetResult(name, deviceControl.GetStringSelection(), valueEdit.GetValue(),
                            deviceControl.GetSelection())


class DevDim(eg.ActionClass):
    name = "Device Dim"
    description = "Dims a TellStick device."
    iconFile = "DeviceDim"

    def __init__(self):
        self.devicename = ""
        self.value = 0
        self.selction = 0

    def __call__(self, dummy, devicename, value, selection):
        self.plugin.sk.SetDevice(devicename, "dim/" + unicode(value))

    def Configure(self, dummy="", devicename="", value=0, selection=0):
        self.value = value
        self.selection = selection
        panel = eg.ConfigPanel()
        dummy, dl = self.plugin.sk.GetDevices()
        dimControl = panel.SpinIntCtrl(self.value, min=0, max=100)
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        deviceControl.Select(selection)
        panel.sizer.Add(dimControl, 0)
        # valueEdit=panel.TextCtrl(value)
        # panel.AddLine("Value: ", valueEdit)
        while panel.Affirmed():
            name = deviceControl.GetStringSelection() + ": " + unicode(dimControl.GetValue()) + "%"
            panel.SetResult(name, deviceControl.GetStringSelection(), dimControl.GetValue(),
                            deviceControl.GetSelection())

import eg

PLUGIN_ICON = (
    "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"
    "dPVxXeF60vWdm7Obwu2o26/uNu5p7ofcn8w0nymeWTNz0MPIQ+BR5dE/C5+VMGvfrH5PQ"
    "0+BZ7XnIy9jL5FXrdewt6V3qvdh7xc+9j5yn+M+4zw33jLeWV/MN8C3yLfLT8Nvnl+F30"
    "N/I/9k/3r/0QCngCUBZwOJgUGBWwL7+Hp8Ib+OPzrbZfay2e1BjKC5QRVBj4KtguXBrSF"
    "oyOyQrSH355jOkc5pDoVQfujW0Adh5mGLw34MJ4WHhVeGP45wiFga0TGXNXfR3ENz30T6"
    "RJZE3ptnMU85ry1KNSo+qi5qPNo3ujS6P8YuZlnM1VidWElsSxw5LiquNm5svt/87fOH4"
    "p3iC+N7F5gvyF1weaHOwvSFpxapLhIsOpZATIhOOJTwQRAqqBaMJfITdyWOCnnCHcJnIi"
    "/RNtGI2ENcKh5O8kgqTXqS7JG8NXkkxTOlLOW5hCepkLxMDUzdmzqeFpp2IG0yPTq9MYO"
    "SkZBxQqohTZO2Z+pn5mZ2y6xlhbL+xW6Lty8elQfJa7OQrAVZLQq2QqboVFoo1yoHsmdl"
    "V2a/zYnKOZarnivN7cyzytuQN5zvn//tEsIS4ZK2pYZLVy0dWOa9rGo5sjxxedsK4xUFK"
    "4ZWBqw8uIq2Km3VT6vtV5eufr0mek1rgV7ByoLBtQFr6wtVCuWFfevc1+1dT1gvWd+1Yf"
    "qGnRs+FYmKrhTbF5cVf9go3HjlG4dvyr+Z3JS0qavEuWTPZtJm6ebeLZ5bDpaql+aXDm4"
    "N2dq0Dd9WtO319kXbL5fNKNu7g7ZDuaO/PLi8ZafJzs07P1SkVPRU+lQ27tLdtWHX+G7R"
    "7ht7vPY07NXbW7z3/T7JvttVAVVN1WbVZftJ+7P3P66Jqun4lvttXa1ObXHtxwPSA/0HI"
    "w6217nU1R3SPVRSj9Yr60cOxx++/p3vdy0NNg1VjZzG4iNwRHnk6fcJ3/ceDTradox7rO"
    "EH0x92HWcdL2pCmvKaRptTmvtbYlu6T8w+0dbq3nr8R9sfD5w0PFl5SvNUyWna6YLTk2f"
    "yz4ydlZ19fi753GDborZ752PO32oPb++6EHTh0kX/i+c7vDvOXPK4dPKy2+UTV7hXmq86"
    "X23qdOo8/pPTT8e7nLuarrlca7nuer21e2b36RueN87d9L158Rb/1tWeOT3dvfN6b/fF9"
    "/XfFt1+cif9zsu72Xcn7q28T7xf9EDtQdlD3YfVP1v+3Njv3H9qwHeg89HcR/cGhYPP/p"
    "H1jw9DBY+Zj8uGDYbrnjg+OTniP3L96fynQ89kzyaeF/6i/suuFxYvfvjV69fO0ZjRoZf"
    "yl5O/bXyl/erA6xmv28bCxh6+yXgzMV70VvvtwXfcdx3vo98PT+R8IH8o/2j5sfVT0Kf7"
    "kxmTk/8EA5jz/GMzLdsAAAAgY0hSTQAAeiUAAICDAAD5/wAAgOkAAHUwAADqYAAAOpgAA"
    "Bdvkl/FRgAAA6JJREFUeNo8zNtPWwUAwOFfT3tKe0rphbbc6kYZt5GBAhPcEtHpJDyQuR"
    "gvMZkPy0xc8FGjTzMa9YUsxumWYaKLxsxpZkyWLCy7hQyDhXGnGwgyCi23DugFunLanp7"
    "jk35/wKe7H3hIQlab4rF4tWhgq8hecL/A6UrEkrssz01/bxKVjqzo/Lx6X9V3mpbELEnI"
    "aTNGQwaBLMLEzPyF5ZXwaJ6ou7IUXruVlLMHthIxW2R6NBDJc5yazz9YZjYbe6ZG/rwoK"
    "yo2i4SqavxHSMrZLqfJhNtuob3t0Lso2fn12cBc0Fp54MtJiQ8vz9ITduCuqD0dnn1wc3"
    "0zjr3A+n+i84+MpVcex4w3hgNUl9h/f7bc3dS7U1pxdjQFySRYDRDZpam5nM+aQQnN9pf"
    "VtR7xFlvV7e0YQg6dUWcUWQ2vYFGzr1+T91Sc9e9AIgGaCrE0SAbGhh7xwWAW7anqttD0"
    "4L2tWAxJktCfeO/9tWx6d6DWKR4NlB7m3O0IxBNYfR7ebK2gZb+L0qIC5pI5tiZCDOldH"
    "K937AlOjTxnzHdf1vWPjhMPLYzeEaqavrkXhfg2bx97mmPuXYZHx8ghYLNaqGtsontwk7"
    "Fbs+xvr6O7bofdyNp5fWdH+8CEWtTSPZaD1U3eOt7Aa851fvjtOvW1Vfg8djIY8AdmeOd"
    "QBWFRYnJgkcceH0c86RZDSm8p+2JahI04BdVFvOBIce6XXr79+DSNXisTM0Geaajl6tA/"
    "/DX1NycaaxgOLHC37xHlr3iigq/p8ItlQiqLkuH5ei/jgQe0tTTT6CvhZ3+QqOig1z/NG"
    "611uB1WZmaCOJwiCCnSJum6YLFZF4dOVlY1FEYfPllbRsjmKLQYAFgX7fyxpJK2lwAgqg"
    "qLoTDGjMxXr3p+uni05KSwsLzJpioteSv2TgYWI9itEjfH5wDQa3DhfB9VdgmA+c0kxW4"
    "bGxtRWry22/lKXBUSyV1WUhqio8iyFcrirqqjpsTFR5du0LbXxiddB7GaNLou3cVrl0hb"
    "HahpgRjm6IZiRtB0OjQ1hyLLRsxmvh7YoOPll0jIMj9eu0N5botPf+3DJoLOWMCVvjCUF"
    "COjT8UUDaHUbsLnsmAxaXmoKsuLO3RemkYq3YfFVUrfQhyTkEcgrnDmagCUPNCbkPLEjF"
    "4wYPA4bRgkA6daKs9EIil3MCmXKxhzPf5VpcaW0xXmS7pQKKGtP1FVX71PNQpiprOhuL/"
    "S65mIZgT+HQBG+5db3h2cPQAAAABJRU5ErkJggg=="
)

eg.RegisterPlugin(
    name="AxialControlHA",
    guid='{D4CF1DC1-B589-4DCE-A5D7-D121E2989B55}',
    author="yokel22",
    version="1.0.1",
    kind="program",
    createMacrosOnAdd=True,
    canMultiLoad=True,
    description=(
        "This is a plugin for AxialControl Home Automation Software (Formerly "
        "called InControl). <a href='http://www.axialcontrol.com'>AxialControl"
        "Homepage</a>"),
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=9528",
    icon=PLUGIN_ICON,
)


import httplib
import json
import threading
import time
from datetime import datetime

import requests


class PollingThread():

    def __init__(self, plugin, interval):
        self.plugin = plugin
        self.interval = interval
        self.event = threading.Event()

    def Start(self):
        self.pollThread = threading.Thread(
            name="AxialPollingThread",
            target=self.Poller
        )
        self.pollThread.start()

    def Stop(self):
        self.event.set()
        eg.PrintNotice("AxialControl Event Polling Stopped")

    def Poller(self):
        waitTime = self.interval
        self.event.clear()

        while not self.event.isSet():
            self.event.wait(waitTime)
            self.plugin.checkChange()


class AxialControlHA(eg.PluginBase):
    """ A plugin to control AxialControl Home Automation Software """

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 1178
        self.password = "password"
        self.polling = False
        self.pollingtime = 5
        self.connected = False
        self.getdevices = ""
        self.scenesdict = {}

        info = self.AddGroup(
            "Information Retrieval",
            "Actions for Information Retrieval"
        )
        info.AddAction(GetSingleDevice)
        info.AddAction(ListAllDevices)
        info.AddAction(ListScenes)

        byType = info.AddGroup(
            "Group Information Retrieval",
            "Actions for Group Type Information Retrieval"
        )
        byType.AddAction(ListLights)
        byType.AddAction(ListDimmers)
        byType.AddAction(ListOutlets)
        byType.AddAction(ListLocks)
        byType.AddAction(ListEnergyDisplayers)
        byType.AddAction(ListLevelDisplayers)
        byType.AddAction(ListMultiLevelSensors)
        byType.AddAction(ListMotion)
        byType.AddAction(ListBinary)
        byType.AddAction(ListGarageDoorOpeners)
        byType.AddAction(ListFans)
        byType.AddAction(ListColorBulb)
        byType.AddAction(ListIrrigation)
        byType.AddAction(ListWaterSensor)
        byType.AddAction(ListNestHomeAway)
        byType.AddAction(ListThermostat)

        actions = self.AddGroup(
            "Actions",
            "Actions to change device states"
        )
        actions.AddAction(TurnSwitchOn)
        actions.AddAction(TurnSwitchOff)
        actions.AddAction(ToggleSwitch)
        actions.AddAction(TurnOutletOn)
        actions.AddAction(TurnOutletOff)
        actions.AddAction(ToggleOutlet)
        actions.AddAction(SetDimmerLevel)
        actions.AddAction(OpenGarageDoor)
        actions.AddAction(CloseGarageDoor)
        actions.AddAction(UnLockDoor)
        actions.AddAction(LockDoor)
        actions.AddAction(ActivateScene)
        actions.AddAction(SetThermostatLevel)

    def Configure(
        self,
        host="127.0.0.1",
        port=1178,
        password="password",
        polling=False,
        pollingtime=15
    ):

        panel = eg.ConfigPanel()
        helpString = panel.StaticText(
            "Enter Your AxialControl Server Credentials"
        )
        spaceString = panel.StaticText("")
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        passwordCtrl = panel.TextCtrl(password)
        pollingCtrl = panel.CheckBox(polling)
        pollingtimeCtrl = panel.SpinIntCtrl(pollingtime, min=1)

        networkBox = panel.BoxedGroup(
            "Network",
            ("IP:", hostCtrl),
            ("Port:", portCtrl)
        )
        securityBox = panel.BoxedGroup(
            "Security",
            ("Password:", passwordCtrl)
        )
        pollingBox = panel.BoxedGroup(
            "Events",
            ("Enable Event Polling:", pollingCtrl),
            ("Polling time in Seconds:", pollingtimeCtrl)
        )
        panel.sizer.Add(helpString, 0, wx.EXPAND)
        panel.sizer.Add(spaceString, 0, wx.EXPAND)
        panel.sizer.Add(networkBox, 0, wx.EXPAND)
        panel.sizer.Add(securityBox, 0, wx.TOP | wx.EXPAND, 10)
        panel.sizer.Add(pollingBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                passwordCtrl.GetValue(),
                pollingCtrl.GetValue(),
                pollingtimeCtrl.GetValue()
            )

    def __start__(self, host, port, password, polling, pollingtime):

        self.host = host
        self.password = password
        self.port = port
        self.polling = polling
        self.pollingtime = pollingtime
        self.token = self.host + ":" + str(self.port)

        # Check for Server Connection
        data = self.getDevices()
        self.startDict = {}
        self.startDict = self.devicedict

        if data != False:
            if self.polling == True:
                eg.PrintNotice("Now Connected to AxialControlHA Server, Event Polling Enabled")
                PollingThread(self, self.pollingtime).Start()
            else:
                eg.PrintNotice("Now Connected to AxialControlHA Server, Event Polling Disabled")
                PollingThread(self, self.pollingtime).Stop()
        else:
            eg.PrintError("AxialControl Connection error, wrong IP or Server not accessible")

    def __stop__(self):
        pass

    def req(self, page, method='GET', body=''):
        data = False
        if body != '': body = json.dumps(body)

        server = httplib.HTTPConnection(self.host + ":" + str(self.port))
        try:
            server.request(method, page, body)
        except:
            data = False
        else:
            try:
                response = server.getresponse()

            except:
                data = False
            else:
                if response.status == 200:
                    try:
                        data = response.read()
                    except:
                        data = False
                    else:
                        data = json.loads(data)
                else:
                    data = False
                return data
            server.close()

    def putCmd(self, url, payload):
        headers = {'content-type': 'application/json'}
        send = requests.put(url, data=json.dumps(payload), headers=headers)

        return send

    def getCmd(self, url):
        headers = {'content-type': 'application/json'}
        payload = {}
        send = requests.get(url, data=json.dumps(payload), headers=headers)

    def postCmd(self, url, payload):
        headers = {'content-type': 'application/json'}
        send = requests.post(url, data=json.dumps(payload), headers=headers)

    def getDevices(self):

        adress = 'http://' + self.token + '/zwave/devices?password=' + self.password
        data = self.req(adress)
        self.switchdict = {}
        self.outletdict = {}
        self.dimmerdict = {}
        self.thermostatdict = {}
        self.unknowndict = {}
        self.binarydict = {}
        self.zoneplayerdict = {}
        self.motiondict = {}
        self.multileveldict = {}
        self.lockdict = {}
        self.leveldisplayerdict = {}
        self.ipcamdict = {}
        self.energymonitordict = {}
        self.alarmdict = {}
        self.fandict = {}
        self.nestawaydict = {}
        self.garagedooropenerdict = {}
        self.colorbulbdict = {}
        self.irrigationdict = {}
        self.watersensordict = {}
        self.devicedict = {}
        self.devices = []

        try:
            for x in data:
                DeviceName = x['deviceName']
                DeviceType = x['deviceType']
                Visible = x['visible']
                RoomID = str(x['roomId'])
                DisplayOrder = str(x['displayOrder'])
                NodeID = str(x['nodeId'])
                Battery = str(x['bl'])
                Name = x['name']
                CurrLevel = str(x['level'])
                DeviceID = str(x['deviceId'])
                sr = str(x['sr'])

                LastChange = self.convert_time((str(x['lastLevelUpdate'])))

                self.devicedict[Name] = {'sr': sr, 'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                         'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                         'roomID': RoomID}

                if DeviceType == 0 and Visible == True:
                    self.switchdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                             'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                             'roomID': RoomID}
                if DeviceType == 1 and Visible == True:
                    self.dimmerdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                             'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                             'roomID': RoomID}
                if DeviceType == 2 and Visible == True:
                    self.outletdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                             'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                             'roomID': RoomID}
                if DeviceType == 3 and Visible == True:
                    self.thermostatdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                                 'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                                 'roomID': RoomID}
                if DeviceType == 5 and Visible == True:
                    self.unknowndict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                              'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                              'roomID': RoomID}
                if DeviceType == 6 and Visible == True:
                    self.binarydict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                             'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                             'roomID': RoomID}
                if DeviceType == 7 and Visible == True:
                    self.zoneplayerdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                                 'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                                 'roomID': RoomID}
                if DeviceType == 8 and Visible == True:
                    self.motiondict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                             'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                             'roomID': RoomID}
                if DeviceType == 9 and Visible == True:
                    self.multileveldict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                                 'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                                 'roomID': RoomID}
                if DeviceType == 10 and Visible == True:
                    self.lockdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                           'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                           'roomID': RoomID}
                if DeviceType == 11 and Visible == True:
                    self.leveldisplayerdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                                     'lastUpdate': LastChange, 'type': DeviceType,
                                                     'batteryLevel': Battery, 'roomID': RoomID}
                if DeviceType == 12 and Visible == True:
                    self.testbulbdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                               'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                               'roomID': RoomID}
                if DeviceType == 13 and Visible == True:
                    self.ipcamdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                            'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                            'roomID': RoomID}
                if DeviceType == 14 and Visible == True:
                    self.energymonitordict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                                    'lastUpdate': LastChange, 'type': DeviceType,
                                                    'batteryLevel': Battery, 'roomID': RoomID}
                if DeviceType == 15 and Visible == True:
                    self.alarmdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                            'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                            'roomID': RoomID}
                if DeviceType == 16 and Visible == True:
                    self.fandict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                          'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                          'roomID': RoomID}
                if DeviceType == 17 and Visible == True:
                    self.colorbulbdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                                'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                                'roomID': RoomID}
                if DeviceType == 19 and Visible == True:
                    self.nestawaydict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                               'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                               'roomID': RoomID}
                if DeviceType == 20 and Visible == True:
                    self.garagedooropenerdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                                       'lastUpdate': LastChange, 'type': DeviceType,
                                                       'batteryLevel': Battery, 'roomID': RoomID}
                if DeviceType == 21 and Visible == True:
                    self.watersensordict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                                  'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                                  'roomID': RoomID}
                if DeviceType == 25 and Visible == True:
                    self.irrigationdict[Name] = {'name': Name, 'deviceID': DeviceID, 'value': CurrLevel,
                                                 'lastUpdate': LastChange, 'type': DeviceType, 'batteryLevel': Battery,
                                                 'roomID': RoomID}

            self.devices = {'Switch': self.switchdict, 'WaterSensor': self.watersensordict,
                            'Irrigation': self.irrigationdict, 'ColorBulb': self.colorbulbdict,
                            'Dimmer': self.dimmerdict, 'Outlet': self.outletdict, 'Thermostat': self.thermostatdict,
                            'Unknown': self.unknowndict, 'Binary': self.binarydict, 'Motion': self.motiondict,
                            'MultiLevel': self.multileveldict, 'Lock': self.lockdict,
                            'LevelDisplayer': self.leveldisplayerdict, 'EnergyMonitor': self.energymonitordict,
                            'Alarm': self.alarmdict, 'Fan': self.fandict, 'NestAwayMode': self.nestawaydict,
                            'GarageDoorOpener': self.garagedooropenerdict}

            return self.devices

        except TypeError:
            return False

    def getScenes(self):
        url = 'http://' + self.token + '/zwave/getScenes'
        payload = {"password": self.password, "sceneName": "", "activate": 1}
        self.scenesdict = {}

        scrape = self.putCmd(url, payload)
        parsed_json = json.loads(scrape.content)

        for scene in parsed_json:
            visible = scene['mobileVisible']

            if visible == True:
                sceneID = scene['sceneId']
                name = scene['sceneName']
                self.scenesdict[name] = {'sceneID': sceneID}

        return self.scenesdict

    def checkChange(self):
        startDict = {}
        currDict = {}
        startDict = self.startDict
        self.getDevices()
        currDict = self.devicedict

        diffkeys = [device for device in startDict if startDict[device]['value'] != currDict[device]['value']]
        for device in diffkeys:
            name = currDict[device]['name']
            value = currDict[device]['value']
            deviceid = currDict[device]['deviceID']
            devicetype = currDict[device]['type']
            changeDict = {}
            changeDict = {"value": value, "deviceID": deviceid, "type": devicetype}
            self.TriggerEvent(name, changeDict)

        self.startDict = currDict

    def convert_EVTtime(self, devicetime):
        dTime = devicetime
        convertTime = datetime.strptime(dTime, '%m/%d/%Y %H:%M:%S %p').strftime('%I:%M:%m:%d')
        return convertTime

    def convert_time(self, lastUpdate):
        lastUpdate = lastUpdate.split('-')
        hroffset = lastUpdate[1].split(')')
        lastUpdate = lastUpdate[0].split('(')
        lastUpdate = int(lastUpdate[1])
        offset = str(hroffset[0][0]) + str(hroffset[0][1])
        ts = time.time()

        st = datetime.fromtimestamp(ts).strftime('%m/%d/%Y %H:%M:%S %p')
        starttime = time.strftime('%m/%d/%Y %H:%M:%S %p', time.localtime(lastUpdate / 1000.))
        '08/28/2012 00:45:17 AM'

        convertTime = datetime.strptime(st, '%m/%d/%Y %H:%M:%S %p') - datetime.strptime(starttime,
                                                                                        '%m/%d/%Y %H:%M:%S %p')
        timedif = str(convertTime)
        return timedif


### Plugin Actions ###

class ListLights(eg.ActionBase):
    name = "Get Switches"
    description = "Returns Switches Dictionary"

    def __call__(self):
        items = self.plugin.switchdict
        return items


class ListDimmers(eg.ActionBase):
    name = "Get Dimmers"
    description = "Returns Dimmers Dictionary"

    def __call__(self):
        items = self.plugin.dimmerdict
        return items


class ListOutlets(eg.ActionBase):
    name = "Get Outlets"
    description = "Returns Outlets Dictionary"

    def __call__(self):
        items = self.plugin.outletdict
        return items


class ListLocks(eg.ActionBase):
    name = "Get Locks"
    description = "Returns Locks Dictionary"

    def __call__(self):
        items = self.plugin.lockdict
        return items


class ListLevelDisplayers(eg.ActionBase):
    name = "Get Level Displayers"
    description = "Returns LevelDisplayers Dictionary"

    def __call__(self):
        items = self.plugin.leveldisplayerdict
        return items


class ListMultiLevelSensors(eg.ActionBase):
    name = "Get MultiLevel Sensors"
    description = "Returns MultiLevelSensors Dictionary"

    def __call__(self):
        items = self.plugin.multileveldict
        return items


class ListBinary(eg.ActionBase):
    name = "Get Binary Sensors"
    description = "Returns Binary Sensors Dictionary"

    def __call__(self):
        items = self.plugin.binarydict
        return items


class ListMotion(eg.ActionBase):
    name = "Get Motion Sensors"
    description = "Returns Motion Sensors Dictionary"

    def __call__(self):
        items = self.plugin.motiondict
        return items


class ListEnergyDisplayers(eg.ActionBase):
    name = "Get Energy Displayers"
    description = "Returns EnergyDisplayers Dictionary"

    def __call__(self):
        items = self.plugin.energymonitordict
        return items


class ListGarageDoorOpeners(eg.ActionBase):
    name = "Get Garage Door Openers"
    description = "Returns Garage Door Openers Dictionary"

    def __call__(self):
        items = self.plugin.garagedooropenerdict
        return items


class ListFans(eg.ActionBase):
    name = "Get Fans"
    description = "Returns Fans Dictionary"

    def __call__(self):
        items = self.plugin.fandict
        return items


class ListColorBulb(eg.ActionBase):
    name = "Get Color Bulbs"
    description = "Returns Colr Bulb Dictionary"

    def __call__(self):
        items = self.plugin.colorbulbdict
        return items


class ListIrrigation(eg.ActionBase):
    name = "Get Irrigation Controllers"
    description = "Returns Irrigation Dictionary"

    def __call__(self):
        items = self.plugin.irrigationdict
        return items


class ListWaterSensor(eg.ActionBase):
    name = "Get Water Sensors"
    description = "Returns Water Sensor Dictionary"

    def __call__(self):
        items = self.plugin.watersensordict
        return items


class ListNestHomeAway(eg.ActionBase):
    name = "Get Nest Home/Away"
    description = "Returns Nest Home/Away Mode Dictionary"

    def __call__(self):
        items = self.plugin.nestawaydict
        return items


class ListThermostat(eg.ActionBase):
    name = "Get Thermostat"
    description = "Returns Thermostat Dictionary"

    def __call__(self):
        items = self.plugin.thermostatdict
        return items


class ListAllDevices(eg.ActionBase):
    name = "Get All Devices"
    description = "Returns All Devices Dictionary"

    def __call__(self):
        cmd = self.plugin.getDevices()
        items = self.plugin.devicedict

        return items


class GetSingleDevice(eg.ActionBase):
    name = "Get Single Device"
    description = "Returns a Single Device"

    class text:
        label_tree = "Get Device: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        cmd = self.plugin.getDevices()
        items = self.plugin.devicedict[deviceName]

        return items

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()

        deviceDict = self.plugin.devicedict
        deviceNameChoices = sorted(deviceDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = deviceDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Device",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                deviceDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class ListScenes(eg.ActionBase):
    name = "Get Scenes"
    description = "Returns Scenes Dictionary"

    def __call__(self):
        a = self.plugin.getScenes()
        scenes = self.plugin.scenesdict

        return scenes


class TurnSwitchOn(eg.ActionBase):
    name = "Turn On Switch"
    description = "Sets Selected Switch to On"

    class text:
        label_tree = "Turn Light Switch On: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.token + '/zwave/setDevicePower'
        payload = {"password": self.plugin.password, "deviceId": device, "powered": "true"}

        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()

        switchDict = self.plugin.switchdict
        deviceNameChoices = sorted(switchDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = switchDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Switch",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                switchDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class TurnSwitchOff(eg.ActionBase):
    name = "Turn Off Switch"
    description = "Sets Selected Switch to Off"

    class text:
        label_tree = "Turn Light Switch Off: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.token + '/zwave/setDevicePower'
        payload = {"password": self.plugin.password, "deviceId": device, "powered": "false"}

        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, device, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()

        switchDict = self.plugin.switchdict
        deviceNameChoices = sorted(switchDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = switchDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Switch",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                switchDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class ToggleSwitch(eg.ActionBase):
    name = "Toggle Switch"
    description = "Toggles Selected Switch On/Off"

    class text:
        label_tree = "Toggle Light Switch: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.token + '/zwave/setDevicePower'
        cmd = self.plugin.getDevices()

        state = self.plugin.switchdict[deviceName]['value']
        if state == "255":
            powered = "false"
        else:
            powered = "true"

        payload = {"password": self.plugin.password, "deviceId": device, "powered": powered}

        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName='', value=''):
        panel = eg.ConfigPanel()

        switchDict = self.plugin.switchdict
        deviceNameChoices = sorted(switchDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = switchDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Switch",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                switchDict[deviceNameCtrl.GetStringSelection()]['deviceID'],
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class TurnOutletOn(eg.ActionBase):
    name = "Turn On Outlet"
    description = "Sets Selected Outlet to On"

    class text:
        label_tree = "Turn Outlet On: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.token + '/zwave/setDevicePower'
        payload = {"password": self.plugin.password, "deviceId": device, "powered": "true"}

        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()

        outletDict = self.plugin.outletdict
        deviceNameChoices = sorted(outletDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = outletDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Outlet",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                outletDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class TurnOutletOff(eg.ActionBase):
    name = "Turn Off Outlet"
    description = "Sets Selected Outlet to Off"

    class text:
        label_tree = "Turn Outlet Off: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.token + '/zwave/setDevicePower'
        payload = {"password": self.plugin.password, "deviceId": device, "powered": "false"}

        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()

        outletDict = self.plugin.outletdict
        deviceNameChoices = sorted(outletDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = outletDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Outlet",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                outletDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class ToggleOutlet(eg.ActionBase):
    name = "Toggle Outlet"
    description = "Toggles Selected Outlet On/Off"

    class text:
        label_tree = "Toggle Outlet: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.token + '/zwave/setDevicePower'
        cmd = self.plugin.getDevices()

        state = self.plugin.outletdict[deviceName]['value']
        if state == "255":
            powered = "false"
        else:
            powered = "true"

        payload = {"password": self.plugin.password, "deviceId": device, "powered": powered}

        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName='', value=''):
        panel = eg.ConfigPanel()

        outletDict = self.plugin.outletdict
        deviceNameChoices = sorted(outletDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = outletDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Switch",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                outletDict[deviceNameCtrl.GetStringSelection()]['deviceID'],
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class OpenGarageDoor(eg.ActionBase):
    name = "Open Garage Door"
    description = "Opens Selected Garage Door"

    class text:
        label_tree = "Open Garage Door: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.token + '/zwave/setDevicePower'
        payload = {"password": self.plugin.password, "deviceId": device, "powered": "true"}

        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()

        garagedooropenerDict = self.plugin.garagedooropenerdict
        deviceNameChoices = sorted(garagedooropenerDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = garagedooropenerDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Garage Door",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                garagedooropenerDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class CloseGarageDoor(eg.ActionBase):
    name = "Close Garage Door"
    description = "Closes Selected Garage Door"

    class text:
        label_tree = "Close Garage Door: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.token + '/zwave/setDevicePower'
        payload = {"password": self.plugin.password, "deviceId": device, "powered": "false"}

        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()

        garagedooropenerDict = self.plugin.garagedooropenerdict
        deviceNameChoices = sorted(garagedooropenerDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = garagedooropenerDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Garage Door",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                garagedooropenerDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class UnLockDoor(eg.ActionBase):
    name = "UnLock Door"
    description = "UnLocks Selected Door"

    class text:
        label_tree = "UnLock Door: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.token + '/zwave/setDevicePower'
        payload = {"password": self.plugin.password, "deviceId": device, "powered": "false"}

        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()

        lockDict = self.plugin.lockdict
        deviceNameChoices = sorted(lockDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = lockDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Lock",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                lockDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class LockDoor(eg.ActionBase):
    name = "Lock Door"
    description = "Locks Selected Door"

    class text:
        label_tree = "Lock Door: "
        label_conf = "Device Name"

    def __call__(self, device, deviceName):
        url = 'http://' + self.plugin.token + '/zwave/setDevicePower'
        payload = {"password": self.plugin.password, "deviceId": device, "powered": "true"}

        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, deviceID, deviceName):
        return self.text.label_tree + deviceName

    def Configure(self, deviceID="Device ID", deviceName=''):
        panel = eg.ConfigPanel()

        lockDict = self.plugin.lockdict
        deviceNameChoices = sorted(lockDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = lockDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)

        deviceBox = panel.BoxedGroup(
            "Choose Lock",
            ("Name: ", deviceNameCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                lockDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class ActivateScene(eg.ActionBase):
    name = "Activate Scene"
    description = "Activates Selected AxialControl Scene"

    class text:
        label_tree = "Activate Scene: "
        label_conf = "Scene Name"

    def __call__(self, scene):
        url = 'http://' + self.plugin.token + '/zwave/activateScene'
        payload = {"password": self.plugin.password, "sceneName": scene, "activate": 1}
        send = self.plugin.putCmd(url, payload)

    def GetLabel(self, scene):
        return self.text.label_tree + scene

    def Configure(self, scene="Scene Name"):
        panel = eg.ConfigPanel()
        try:
            self.plugin.getScenes()
        except requests.ConnectionError:
            pass
        keyChoicesList = sorted(self.plugin.scenesdict.keys())
        if keyChoicesList:
            keySelection = keyChoicesList[0]
            choiceKeyCtrl = panel.Choice(keyChoicesList.index(keySelection), keyChoicesList)
        else:
            choiceKeyCtrl = panel.Choice(0, [])

        panel.AddLine("Select Scene: ", choiceKeyCtrl)
        while panel.Affirmed():
            panel.SetResult(
                choiceKeyCtrl.GetStringSelection()
            )


class SetDimmerLevel(eg.ActionBase):
    name = "Set Dimmer Level"
    description = "Sets Selected Dimmer to Selected Value"

    class text:
        label_tree = "Set Dimmer Switch Level: "
        label_conf = "Device Name"

    def __call__(self, device, deviceValue, deviceName):
        if deviceValue == 0:
            powered = "False"
        else:
            powered = "True"
        self.adress = 'http://' + self.plugin.token + '/zwave/setDeviceState?NODEID=' + device + '&Powered=' + powered + '&Level=' + str(
            deviceValue) + '&Password=' + self.plugin.password
        r = self.plugin.getCmd(self.adress)

    def GetLabel(self, deviceID, deviceValue, deviceName):
        return self.text.label_tree + deviceName + ' ' + str(deviceValue) + '%'

    def Configure(self, deviceID="Device ID", deviceValue=66, deviceName=''):
        panel = eg.ConfigPanel()

        dimmerDict = self.plugin.dimmerdict
        deviceNameChoices = sorted(dimmerDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = dimmerDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)
        deviceValueCtrl = panel.SpinIntCtrl(
            deviceValue,
            max=100,
        )

        deviceBox = panel.BoxedGroup(
            "Choose Dimmer Switch",
            ("Name: ", deviceNameCtrl),
            ("Value: ", deviceValueCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                dimmerDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceValueCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )


class SetThermostatLevel(eg.ActionBase):
    name = "Set Thermostat Level"
    description = "Sets Selected Thermostat to Selected Value in Degrees"

    class text:
        label_tree = "Set Thermostat Level: "
        label_conf = "Device Name"

    def __call__(self, device, deviceValue, deviceName):
        self.adress = 'http://' + self.plugin.token + '/zwave/thermoSetPoint?NODEID=' + device + '&setPointName=' + "heating1" + '&temperatureValue=' + str(
            deviceValue) + '&Password=' + self.plugin.password
        r = self.plugin.getCmd(self.adress)

    def GetLabel(self, deviceID, deviceValue, deviceName):
        return self.text.label_tree + deviceName + ' ' + str(deviceValue) + '%'

    def Configure(self, deviceID="Device ID", deviceValue=66, deviceName=''):
        panel = eg.ConfigPanel()

        thermostatDict = self.plugin.thermostatdict
        deviceNameChoices = sorted(thermostatDict.keys())

        if deviceName in deviceNameChoices:
            deviceSelection = deviceNameChoices.index(deviceName)
            deviceName = thermostatDict[deviceName]['deviceID']
        else:
            deviceSelection = 0

        deviceNameCtrl = panel.Choice(
            deviceSelection,
            deviceNameChoices
        )
        deviceIDCtrl = panel.TextCtrl(deviceName)
        deviceValueCtrl = panel.SpinIntCtrl(
            deviceValue,
            max=100,
        )

        deviceBox = panel.BoxedGroup(
            "Choose Thermostat",
            ("Name: ", deviceNameCtrl),
            ("Value: ", deviceValueCtrl),
            (deviceIDCtrl)
        )

        def OnChoice(event):
            deviceIDCtrl.SetValue(
                thermostatDict[deviceNameCtrl.GetStringSelection()]['deviceID']
            )
            event.Skip()

        deviceNameCtrl.Bind(wx.EVT_CHOICE, OnChoice)

        eg.EqualizeWidths(tuple(deviceBox.GetColumnItems(0)))
        panel.sizer.Add(deviceBox, 0, wx.EXPAND | wx.ALL, 10)
        deviceIDCtrl.Hide()

        while panel.Affirmed():
            panel.SetResult(
                deviceIDCtrl.GetValue(),
                deviceValueCtrl.GetValue(),
                deviceNameCtrl.GetStringSelection()
            )

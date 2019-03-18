import eg

eg.RegisterPlugin(
    name="Energenie EG-PM(S)2",
    guid='{F92DC776-F875-4384-9343-214BAC85397F}',
    author="EssKaa",
    version="1.0",
    kind="external",
    # We don't auto load macros because they are not configured yet.
    createMacrosOnAdd=True,
    canMultiLoad=False,
    description="Control Energenie PM(S)2-LAN - Webstite: http://energenie.com/item.aspx?id=7416"
)


import socket
import struct
import time
from threading import Thread


class EGPM(eg.PluginBase):
    def __init__(self):
        self.AddAction(SetSocketAOn, clsName="Socket 1 - ON", description="Turn on socket 1")
        self.AddAction(SetSocketAOff, clsName="Socket 1 - OFF", description="Turn off socket 1")
        self.AddAction(SetSocketAToggle, clsName="Socket 1 - TOGGLE", description="Toggle socket 1")
        self.AddAction(SetSocketBOn, clsName="Socket 2 - ON", description="Turn on socket 2")
        self.AddAction(SetSocketBOff, clsName="Socket 2 - OFF", description="Turn off socket 2")
        self.AddAction(SetSocketBToggle, clsName="Socket 2 - TOGGLE", description="Toggle socket 2")
        self.AddAction(SetSocketCOn, clsName="Socket 3 - ON", description="Turn on socket 3")
        self.AddAction(SetSocketCOff, clsName="Socket 3 - OFF", description="Turn off socket 3")
        self.AddAction(SetSocketCToggle, clsName="Socket 3 - TOGGLE", description="Toggle socket 3")
        self.AddAction(SetSocketDOn, clsName="Socket 4 - ON", description="Turn on socket 4")
        self.AddAction(SetSocketDOff, clsName="Socket 4 - OFF", description="Turn off socket 4")
        self.AddAction(SetSocketDToggle, clsName="Socket 4 - TOGGLE", description="Toggle socket 4")
        self.AddAction(StartBackgroundUpdate, clsName="Start monitor", description="Not fully implemented")
        self.AddAction(StopBackgroundUpdate, clsName="Stop monitor", description="Not fully implemented")

    def __start__(self, ip_address="", password="", event=True):
        self.egpmIp = ip_address
        self.egpmPw = password
        self.egpmUpdate = True
        self.egpmEvent = event
        eg.globals.egpmCurrentState = [0, 0, 0, 0]

    def Configure(self, ip_address="", password="", event=True):
        x_start = 10
        x_padding = 70
        y_start = 10
        y_padding = 22
        label_padding = 3
        i = 0

        panel = eg.ConfigPanel()
        labelIpAddress = wx.StaticText(panel, label="Device IP",
                                       pos=(x_start, y_start + label_padding + (i * y_padding)))
        textControlIpAddress = wx.TextCtrl(panel, -1, ip_address,
                                           (x_start + (x_padding * 2), y_start + (i * y_padding)), (150, -1))

        i += 1
        labelPassword = wx.StaticText(panel, label="Password", pos=(x_start, y_start + label_padding + (i * y_padding)))
        textControlPassword = wx.TextCtrl(panel, -1, password, (x_start + (x_padding * 2), y_start + (i * y_padding)),
                                          (150, -1))

        i += 1
        labelEvent = wx.StaticText(panel, label="Event on EG command?",
                                   pos=(x_start, y_start + label_padding + (i * y_padding)))
        checkBoxEvent = wx.CheckBox(panel, -1, "", (x_start + (x_padding * 2), y_start + (i * y_padding + 4)),
                                    (150, -1))
        checkBoxEvent.SetValue(event)

        while panel.Affirmed():
            panel.SetResult(textControlIpAddress.GetValue(), textControlPassword.GetValue(), checkBoxEvent.GetValue())


class ActionBase(eg.ActionClass):

    def egpmResponse(self, t, k):
        v1 = ((t[0] ^ k[2]) * k[0]) ^ (k[6] | (k[4] << 8)) ^ t[2]
        v2 = ((t[1] ^ k[3]) * k[1]) ^ (k[7] | (k[5] << 8)) ^ t[3]
        return struct.pack(">BBBB", v1 % 256, v1 >> 8, v2 % 256, v2 >> 8)

    def egpmDecrypt(self, d, k, t):
        r = [0, 0, 0, 0]
        for i in range(0, 4):
            x = d[i]
            x -= k[1]
            x ^= k[0]
            x -= t[3]
            x ^= t[2]
            r[3 - i] = 0xff & x
        return r

    def egpmEncrypt(self, d, k, t):
        r = [0, 0, 0, 0]
        for i in range(0, 4):
            x = d[3 - i]
            x ^= t[2]
            x += t[3]
            x ^= k[0]
            x += k[1]
            r[i] = 0xff & x
        return struct.pack(">BBBB", r[0], r[1], r[2], r[3])

    def egpmSetSocketStateWrapper(self, host, password, socketNr, action, debug=False):
        sent = False
        while not sent:
            status = self.egpmSetSocketState(host, password, socketNr, action, debug)
            if status != None:
                sent = True
        return

    def egpmSetSocketState(self, host, password, socketNr, action, debug=False):
        if socketNr < 0 or socketNr > 3:
            raise Exception("socketNr can only be between 0 - 3")
        # password has to be 8 chars long, fill up with spaces
        while len(password) < 8:
            password = password + chr(32)
        key = struct.unpack_from(">BBBBBBBB", password)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((host, 5000))
        except:
            return None

        try:
            s.send('\x11')
        except:
            return None

        try:
            recvTask = s.recv(4)
        except:
            return None

        task = struct.unpack_from(">BBBB", recvTask)
        sendResonse = self.egpmResponse(task, key)

        try:
            s.sendall(sendResonse)
        except:
            return None

        try:
            recvData = s.recv(4)
        except:
            return None

        data = struct.unpack_from(">BBBB", recvData)

        curState = self.egpmDecrypt(data, key, task)
        # initialize control - 4 means do nothing
        control = [4, 4, 4, 4]

        # turn off socket unless already off
        if (action == 0) & (curState[socketNr] != 130):
            control[socketNr] = 2

        # turn on socket unless already on
        if (action == 1) & (curState[socketNr] != 65):
            control[socketNr] = 1

        # toggle socket
        if action == 2:
            control[socketNr] = (curState[socketNr] & 1) + 1
            if control[socketNr] == 2:
                print "EGPM: Socket%s - State: %s" % (str(socketNr + 1), "OFF")
            if control[socketNr] == 1:
                print "EGPM: Socket%s - State: %s" % (str(socketNr + 1), "ON")

        # send commands
        sendControl = self.egpmEncrypt(control, key, task)
        try:
            s.sendall(sendControl)
        except:
            return None

        try:
            recvData = s.recv(4)
        except:
            return None

        data = struct.unpack_from(">BBBB", recvData)
        newState = self.egpmDecrypt(data, key, task)

        if newState[socketNr] != eg.globals.egpmCurrentState[socketNr]:
            eg.globals.egpmCurrentState = newState

        try:
            s.sendall("\x01\x02\x03\x04")
        except:
            return None
        s.close()
        if self.plugin.egpmEvent:
            if newState[socketNr] == 130:
                eg.TriggerEvent(prefix="EGPM", suffix="Socket%s.OFF" % str(socketNr + 1))
            if newState[socketNr] == 65:
                eg.TriggerEvent(prefix="EGPM", suffix="Socket%s.ON" % str(socketNr + 1))
        return True

    def egpmStatusThread(self, updateInterval=1):
        while self.plugin.egpmUpdate:
            sent = False
            while not sent:
                status = self.egpmGetSocketState(host=self.plugin.egpmIp, password=self.plugin.egpmPw)
                if status != None:
                    sent = True
                    self.egpmCheckEvent(status, asEvent=True)
            time.sleep(updateInterval)
        return

    def egpmStartStatusThread(self):
        t = Thread(target=self.egpmStatusThread)
        t.daemon = True
        t.start()
        return

    def egpmStopStatusThread(self):
        self.plugin.egpmUpdate = False

    def egpmGetSocketState(self, host, password, debug=False):
        while len(password) < 8:
            password = password + chr(32)
        key = struct.unpack_from(">BBBBBBBB", password)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((host, 5000))
        except:
            return None

        try:
            s.sendall('\x11')
        except:
            return None

        try:
            recvTask = s.recv(4)
        except:
            return None

        task = struct.unpack_from(">BBBB", recvTask)
        sendResonse = self.egpmResponse(task, key)

        try:
            s.sendall(sendResonse)
        except:
            return None

        try:
            recvData = s.recv(4)
        except:
            return None

        data = struct.unpack_from(">BBBB", recvData)

        try:
            s.send("\x01\x02\x03\x04")
        except:
            return None
        s.close()
        return self.egpmDecrypt(data, key, task)

    def egpmCheckEvent(self, chkState, socketNumber=None, asEvent=False):
        for i in range(0, 4):
            if chkState[i] != eg.globals.egpmCurrentState[i]:
                if chkState[i] == 130:
                    if asEvent:
                        eg.TriggerEvent(prefix="EGPM", suffix="Socket%s.OFF" % str(i + 1))
                    elif not asEvent:
                        print "EGPM: Socket%s - OFF" % str(i + 1)
                if chkState[i] == 65:
                    if asEvent:
                        eg.TriggerEvent(prefix="EGPM", suffix="Socket%s.ON" % str(i + 1))
                    elif not asEvent:
                        print "EGPM: Socket%s - ON" % str(i + 1)
        eg.globals.egpmCurrentState = chkState
        return


class SetSocketAOn(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=0,
                                              action=1)


class SetSocketAOff(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=0,
                                              action=0)


class SetSocketAToggle(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=0,
                                              action=2)


class SetSocketBOn(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=1,
                                              action=1)


class SetSocketBOff(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=1,
                                              action=0)


class SetSocketBToggle(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=1,
                                              action=2)


class SetSocketCOn(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=2,
                                              action=1)


class SetSocketCOff(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=2,
                                              action=0)


class SetSocketCToggle(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=2,
                                              action=2)


class SetSocketDOn(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=3,
                                              action=1)


class SetSocketDOff(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=3,
                                              action=0)


class SetSocketDToggle(ActionBase):
    def __call__(self):
        return self.egpmSetSocketStateWrapper(host=self.plugin.egpmIp, password=self.plugin.egpmPw, socketNr=3,
                                              action=2)


class StartBackgroundUpdate(ActionBase):
    def __call__(self):
        return self.egpmStartStatusThread()


class StopBackgroundUpdate(ActionBase):
    def __call__(self):
        return self.egpmStopStatusThread()

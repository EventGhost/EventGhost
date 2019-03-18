
# This file is part of an Eventghost plugin to control the Marantz M-CR511 amplifier.
# This plugin was developed by using the specification of the
# TCP/IP control protocol of the Marantz M-CR511 Receiver provided by Marantz.
# Marantz was not involved in the development this plugin.
# Copyright (C) 2015  Kevin Smith <smith.kb@hotmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import eg

eg.RegisterPlugin(
    name="Marantz M-CR511",
    guid='{E2E9F66F-716B-4559-B34A-D18C16B099BC}',
    author="Kevin Smith",
    version="0.1.0",
    kind="external",
    description='Control the Marantz M-CR511 (and M-CR611) amplifier via the TCP/IP control protocol. \n \n \
    The plugin should also work for the previous models M-CR510/610, as well as other amplifiers \n \
    using the same or very similar TCP/IP control protocol (as many Marantz & Denon amplifiers/receivers do).'
)

# import
import socket
from select import select
from threading import Event, Thread, RLock
from time import sleep, time


class Amp(eg.PluginBase):
    def __init__(self):

        #actions
        group_Connection = self.AddGroup("Connection", "Connect and disconnect to/from Amplifier")
        group_Connection.AddAction(ConnectToAmp)
        group_Connection.AddAction(DisconnectFromAmp)

        group_TimerClock = self.AddGroup("Timer, Clock & Sleep", "Set Timer, switch it On/Off and show the Clock")
        group_TimerClock.AddAction(TimerOn)
        group_TimerClock.AddAction(TimerOff)
        group_TimerClock.AddAction(Clock)
        group_TimerClock.AddAction(setSleep)

        group_Power = self.AddGroup("Power", "Actions regarding the Power State of the amplifier")
        group_Power.AddAction(PowerOn)
        group_Power.AddAction(PowerOff)
        group_Power.AddAction(MakeAmpReadyForMP)

        group_Vol = self.AddGroup("Volume", "Actions regarding the Volume")
        group_Vol.AddAction(setVolumeTo)
        group_Vol.AddAction(VolUp)
        group_Vol.AddAction(VolDown)
        group_Vol.AddAction(VolPct)
        group_Vol.AddAction(gradualVolChange)
        group_Vol.AddAction(stopGradualVolChange)
        group_Vol.AddAction(NormalMode)
        group_Vol.AddAction(StadiumMode)
        group_Vol.AddAction(NightMode)
        group_Vol.AddAction(NextAudioMode)
        group_Vol.AddAction(NightModeIfNoStadiumMode)

        group_Other = self.AddGroup("Other",
                                    "Other Stuff like Reading the display, calling Favourites, setting the display's brightness, etc.")
        group_Other.AddAction(PrintCurrentParameters)
        group_Other.AddAction(ReadAmpDisplay)
        group_Other.AddAction(Favourite)
        group_Other.AddAction(setDisplayBrightness)
        group_Other.AddAction(sendCustomCommand)





        #available commands
        self.available_commands = [
            ('PWON', "Power On"),
            ('PWOFF', "Power Off"),
            ('PW?', "Request Power Status"),

            ('MVUP', "Volume Up"),
            ('MVDOWN', "Volume Down"),
            ('MV[0-9][0-9]', "Volume %s"),
            ('MV?', "Request Volume Status"),
            ('MVVOAUP', "Volume Up"),
            ('MVVOADOWN', "Volume Down"),
            ('MVVOA[0-9][0-9]', "Volume %s"),
            ('MVVOA?', "Digital In"),

            ('MUON', "Mute"),
            ('MUOFF', "Mute Off"),
            ('MU?', "Request Mute Status"),
            ('MUVOAON', "Mute"),
            ('MUVOAOFF', "Mute Off"),
            ('MUVOA?', "Request Mute Status"),

            ('SIIRADIO', "Internet Radio"),
            ('SIBLUETOOTH', "Bluetooth"),
            ('SISERVER', "Server"),
            ('SIUSB', "USB"),
            ('SIREARUSB', "Rear USB"),
            ('SIDIGITALIN1', "Digital In"),
            ('SIANALOGIN', "Analog In"),

            ('SLPOFF', "Sleep Off"),
            ('SLP[0-9][0-9][0-9]', "Sleep %s"),
            ('SLP?', "Request Sleep Status"),

            ('TSONCE @**##-@$$%% [F] [N] VV O', "Timer Once Off"),
            ('TEVERY @**##-@$$%% [F] [N] VV O', "Timer Every Off"),
            ('TSONCE @**##-@$$%% [F] [N] VV O', "Timer Once set to %s "),
            ('TEVERY @**##-@$$%% [F] [N] VV O', "Timer Every set to %s "),

            ('CLK', "toggle Clock"),

            ('FV $$', "Favourite %s"),
            ('FVMEM [0-9][0-9]', "Set to Favourite %s"),
            ('FVDEL [0-9][0-9]', "Delete Favourite %s"),
            ('FV ?', "Request Favourite List"),

            ('PSBAS UP', "Bass Up"),
            ('PSBAS DOWN', "Bass Down"),
            ('PSBAS [0-9][0-9]', "Set Bass to %s"),
            ('PSBAS ?', "Request Bass Level"),
            ('PSTRE UP', "Treble Up"),
            ('PSTRE DOWN', "Treble Down"),
            ('PSTRE [0-9][0-9]', "Set Treble to %s"),
            ('PSTRE ?', "Request Treble Level"),
            ('PSBAL LEFT', "Balance left"),
            ('PSBAL RIGHT', "Balance right"),
            ('PSBAL [0-9][0-9]', "Set Balance to %s"),
            ('PSBAL ?', "Request Balance Level"),
            ('PSSDB ON', "Dynamic Bass Boost On"),
            ('PSSDB OFF', "Dynamic Bass Boost Off"),
            ('PSSDB ?', "Request Dynamic Bass Boost Status"),
            ('PSSDI ON', "Source Direct On"),
            ('PSSDI OFF', "Source Direct Off"),
            ('PSSDI ?', "Request Source Direct Status")
        ]

    def __start__(self, IP_str,
                  Input_str1,
                  Input_str2,
                  Input_str3,
                  Input_str4,
                  Input_str5,
                  Input_str6,
                  Input_str7):
        print "starting"

        #set the configuration variables
        self.HOST = IP_str

        #initiate the dict for the status variables
        self.status_variables = {
            "Power": None,
            "Input": "N/A",
            "Volume": None,
            "Mute": None,
            "SourceDirect": None,
            "Treble": None,
            "Bass": None,
            "Balance": None,
            "Timer": (None, None),  #(once, every)
            "DynamicBassBoost": None,
            "Sleep": None,
            "AudioMode": None,  # 0 is Normal, 1 is Night, 2 is Stadium
            "ConnectStatus": 0,
            "Display": [""] * 9
        }

        # Names for Inputs (for outputting)
        self.InputNames = {
            "Internet Radio": Input_str1,
            "Bluetooth": Input_str2,
            "Server": Input_str3,
            "USB": Input_str4,
            "Rear USB": Input_str5,
            "Digital In": Input_str6,
            "Analog In": Input_str7
        }

        # a dictionary for values which cannot be set at the moment of the command, because the amplifier is switched off
        self.remember = {}

        # connect to the application
        self.start_connection()

    def __stop__(self):
        print "stopping plugin"
        self.stop_connection()

    def __close__(self):
        print "closing plugin"

    def OnComputerSuspend(self):
        self.stop_connection()

    def OnComputerResume(self):
        self.start_connection()

    def start_connection(self):

        #initiate the socket & lock
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sockLock = RLock()

        #connect to the amplifier
        port = 23
        self.sock.connect((self.HOST, port))

        # Start the Thread for Receiving
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadLoop,
            args=(self.stopThreadEvent, )
        )
        thread.start()

        self.status_variables["ConnectStatus"] = 1

        self.request_status_variables_update()

    def stop_connection(self):
        #stop the ThreadLoop
        self.stopThreadEvent.set()
        #shut down the socket connection
        self.sock.close()

        self.status_variables["ConnectStatus"] = 0
        print "done"

    def Configure(self, IP_str="192.168.1.197",
                  Input_str1="Internet Radio",
                  Input_str2="Bluetooth",
                  Input_str3="Server",
                  Input_str4="USB",
                  Input_str5="Rear USB",
                  Input_str6="Digital In",
                  Input_str7="Analog In"):


        panel = eg.ConfigPanel()

        IP_str_Control2 = panel.TextCtrl(IP_str)
        Input_str1_Ctrl = panel.TextCtrl(Input_str1)
        Input_str2_Ctrl = panel.TextCtrl(Input_str2)
        Input_str3_Ctrl = panel.TextCtrl(Input_str3)
        Input_str4_Ctrl = panel.TextCtrl(Input_str4)
        Input_str5_Ctrl = panel.TextCtrl(Input_str5)
        Input_str6_Ctrl = panel.TextCtrl(Input_str6)
        Input_str7_Ctrl = panel.TextCtrl(Input_str7)

        panel.AddLine("IP address of Amplifier: ", IP_str_Control2)
        panel.AddLine("Customised Names for the various Inputs:")
        panel.AddLine("Internet Radio: ", Input_str1_Ctrl)
        panel.AddLine("Bluetooth: ", Input_str2_Ctrl)
        panel.AddLine("Server: ", Input_str3_Ctrl)
        panel.AddLine("USB: ", Input_str4_Ctrl)
        panel.AddLine("Rear USB: ", Input_str5_Ctrl)
        panel.AddLine("Digital In: ", Input_str6_Ctrl)
        panel.AddLine("Analog In: ", Input_str7_Ctrl)

        while panel.Affirmed():
            panel.SetResult(IP_str_Control2.GetValue(),
                Input_str1_Ctrl.GetValue(),
                Input_str2_Ctrl.GetValue(),
                Input_str3_Ctrl.GetValue(),
                Input_str4_Ctrl.GetValue(),
                Input_str5_Ctrl.GetValue(),
                Input_str6_Ctrl.GetValue(),
                Input_str7_Ctrl.GetValue()
            )

    def ThreadLoop(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            received_data_in_cur_round = False  #if we received data, we do not want to wait for the next round
            self.sockLock.acquire()
            readable, writable, exceptional = select([self.sock], [], [self.sock], 0)
            if readable:
                receive_data = self.sock.recv(1024)
                self.sockLock.release()
                received_data_in_cur_round = True
                receive_data = receive_data.split("\r")
                for msg in receive_data:
                    if not msg:
                        continue  #only messages with content
                    self.handle_rcv_content(msg)
            else:
                self.sockLock.release()

            if exceptional:
                print "error in socket"
                print exceptional

            if not received_data_in_cur_round:
                stopThreadEvent.wait(0.1)

    #define a function to handle responses
    def receive_responses(self, exp_nb_responses=1):
        #TODO: maybe I should get rid of this function. Is it really needed? (Currently not in use)

        #try four times (last try has to be after some time t>200milliseconds)
        #after exp_nb_responses or more responses the cycle breaks
        n_responses = 0
        for recvTry in range(4):
            readable, writable, exceptional = select([self.plugin.sock], [], [self.plugin.sock], 0)
            if readable:
                receive_data = self.sock.recv(1024)
                receive_data = receive_data.split("\r")
                for msg in receive_data:
                    if not msg:
                        continue  #only messages with content
                    self.handle_rcv_content(msg)
                    print msg
                    n_responses += 1
                if n_responses >= exp_nb_responses:
                    break
            sleep(0.07)
        sleep(0.01)

    def handle_rcv_content(self, msg):
        #print msg

        if msg.startswith("MVVOA"):
            self.status_variables["Volume"] = int(msg[5:7])
            self.TriggerEvent("Vol", payload=str(self.status_variables["Volume"]))
        elif msg.startswith("MV"):
            self.status_variables["Volume"] = int(msg[2:4])
            self.TriggerEvent("Vol", payload=str(self.status_variables["Volume"]))

        elif msg.startswith("MU"):
            if msg == "MUON":
                self.status_variables["Mute"] = True
            elif msg == "MUOFF":
                self.status_variables["Mute"] = False
            #trigger Event
            self.TriggerEvent("Mute", payload=str(self.status_variables["Mute"]))

        elif msg.startswith("PW"):
            if msg == "PWON":
                self.status_variables["Power"] = True
                if len(self.remember) > 0:
                    sleep(4)
                    self.execute_remembered_values()
            elif msg == "PWSTANDBY":
                self.status_variables["Power"] = False
            #trigger Event
            self.TriggerEvent("Power." + str(self.status_variables["Power"]))

        elif msg.startswith("SI"):
            if msg == "SIIRADIO":
                self.status_variables["Input"] = self.InputNames["Internet Radio"]
            elif msg == "SIBLUETOOTH":
                self.status_variables["Input"] = self.InputNames["Bluetooth"]
            elif msg == "SISERVER":
                self.status_variables["Input"] = self.InputNames["Server"]
            elif msg == "SIUSB":
                self.status_variables["Input"] = self.InputNames["USB"]
            elif msg == "SIREARUSB":
                self.status_variables["Input"] = self.InputNames["Rear USB"]
            elif msg == "SIDIGITALIN1":
                self.status_variables["Input"] = self.InputNames["Digital In"]
            elif msg == "SIANALOGIN":
                self.status_variables["Input"] = self.InputNames["Analog In"]
            #trigger Event
            self.TriggerEvent("Input", payload=self.status_variables["Input"])

        elif msg.startswith("PS"):
            if msg.startswith("PSTRE"):
                self.status_variables["Treble"] = int(msg[6:8])
            elif msg.startswith("PSBAS"):
                self.status_variables["Bass"] = int(msg[6:8])
            elif msg.startswith("PSBAL"):
                self.status_variables["Balance"] = int(msg[6:8])
            elif msg.startswith("PSSDB"):
                if msg == "PSSDB ON":
                    self.status_variables["DynamicBassBoost"] = True
                elif msg == "PSSDB OFF":
                    self.status_variables["DynamicBassBoost"] = False
            elif msg.startswith("PSSDI"):
                if msg == "PSSDI ON":
                    self.status_variables["SourceDirect"] = True
                elif msg == "PSSDI OFF":
                    self.status_variables["SourceDirect"] = False

        elif msg.startswith("SLP"):
            if msg.startswith("SLPOFF"):
                self.status_variables["Sleep"] = 0
            else:
                self.status_variables["Sleep"] = int(msg[3:6])
            #trigger Event
            self.TriggerEvent("SLP", payload=str(self.status_variables["Sleep"]))

        elif msg.startswith("NSE"):
            self.status_variables["Display"][int(msg[3:4])] = msg[4:len(msg)]

    def execute_remembered_values(self):
        if "AudioMode" in self.remember:
            self.activateAudioMode(self.remember["AudioMode"])
            self.remember.pop("AudioMode", None)
        if len(self.remember) > 0:
            print "there are remembered values which have not been executed"

    def request_status_variables_update(self):
        #TODO: Check how large the buffer is (and how it interacts with the 1024 recv length). Maybe need to do a sockLock pause
        with self.sockLock:
            self.sock.sendall(b'PW?\r')
            self.sock.sendall(b'SI?\r')
            self.sock.sendall(b'MV?\r')
            self.sock.sendall(b'MU?\r')
            self.sock.sendall(b'PSSDI ?\r')
            self.sock.sendall(b'PSBAS ?\r')
            self.sock.sendall(b'PSTRE ?\r')
            self.sock.sendall(b'PSBAL ?\r')
            self.sock.sendall(b'PSSDB ?\r')
            self.sock.sendall(b'SLP?\r')
            self.sock.sendall(b'TS?\r')  #TODO: Check Timer request command
            self.sock.sendall(b'NSE\r')

    def activateAudioMode(self, mode):
        #first check whether the AudioMode is already active. If yes, then nothing has to be done
        if not (self.status_variables["AudioMode"] == mode):
            #check if the Power is On, if not, then we cannot change the Audio Mode. In this case, we remember, that we need to set it as soon as the amplifier is switched on again.
            if not self.status_variables["Power"]:
                self.remember["AudioMode"] = mode
                #trigger Event
                self.TriggerEvent("AudioMode", payload="R" + str(mode))
            else:
                if mode == 0:  #normal
                    with self.sockLock:
                        self.sock.sendall(b'PSSDI ON\r')
                        self.sock.sendall(b'SSDIM100\r')
                        self.sock.sendall(b'PSBAS 50\r')
                        self.sock.sendall(b'PSTRE 50\r')
                        self.sock.sendall(b'PSBAL 50\r')
                        self.sock.sendall(b'PSSDB OFF\r')
                    self.status_variables["AudioMode"] = 0

                elif mode == 1:  #night
                    with self.sockLock:
                        self.sock.sendall(b'PSSDI OFF\r')
                        self.sock.sendall(b'PSBAS 40\r')
                        self.sock.sendall(b'PSTRE 52\r')
                        self.sock.sendall(b'SSDIM050\r')
                    self.status_variables["AudioMode"] = 1

                elif mode == 2:  #stadium
                    with self.sockLock:
                        self.sock.sendall(b'PSSDI OFF\r')
                        self.sock.sendall(b'PSBAS 52\r')
                        self.sock.sendall(b'PSTRE 58\r')
                        self.sock.sendall(b'SSDIM050\r')
                    self.status_variables["AudioMode"] = 2

                #trigger Event
                self.TriggerEvent("AudioMode", payload=str(self.status_variables["AudioMode"]))

    def switchToNextAudioMode(self):
        if self.status_variables["AudioMode"] is None:
            self.activateAudioMode(0)
        else:
            newAudioMode = (self.status_variables["AudioMode"] + 1) % 3
            self.activateAudioMode(newAudioMode)

    def sendCommand(self, cmd):
        with self.sockLock:
            self.sock.sendall(cmd)

    def repeatCommandThread(self, stopRepeatingCommand, cmd_str, interval, nb_loops, end_event_string):
        for loop_cur in range(nb_loops):
            if stopRepeatingCommand.isSet():
                break
            self.sendCommand(cmd_str)
            stopRepeatingCommand.wait(interval)
        stopRepeatingCommand.set()
        self.TriggerEvent(end_event_string)


###########
## Actions
###########

#
# Connection
#
class ConnectToAmp(eg.ActionBase):
    def __call__(self):
        sleep(5)  #seems to work with 10seconds
        self.plugin.start_connection()


class DisconnectFromAmp(eg.ActionBase):
    def __call__(self):
        self.plugin.stop_connection()


#
# Power
#
class PowerOn(eg.ActionBase):
    name = "Power On"
    description = "Switch the amplifier on. (There is a 3sec wait after it to ensure the amplifier is ready to receive new commands)"

    def __call__(self):
        if not self.plugin.status_variables["Power"]:
            with self.plugin.sockLock:
                self.plugin.sendCommand(b'PWON\r')
                sleep(3)


class PowerOff(eg.ActionBase):
    name = "Power Off"
    description = "Switch the amplifier off"

    def __call__(self):
        if self.plugin.status_variables["Power"]:
            self.plugin.sendCommand(b'PWOFF\r')
            sleep(5)


class MakeAmpReadyForMP(eg.ActionBase):
    name = "Make Amp Ready For Digital In"
    description = "If needed, switch amplifier on and choose Digital In as Input"

    def __call__(self):
        if not self.plugin.status_variables["Power"]:
            self.plugin.sendCommand(b'PWON\r')
            sleep(4)
        if not self.plugin.status_variables["Input"] == self.plugin.InputNames["Digital In"]:
            self.plugin.sendCommand(b'SIDIGITALIN1\r')


#
# Volume & Tone Actions
#
class setVolumeTo(eg.ActionBase):
    name = "Set Volume Level"
    description = "Set the volume level to a specified value"

    def __call__(self, VolumeLevel):
        cmd_str = b'MV%02d\r' % VolumeLevel
        self.plugin.sendCommand(cmd_str)

    def Configure(self, VolumeLevel=10):
        panel = eg.ConfigPanel()
        VolumeLevelCtrl = panel.SpinIntCtrl(VolumeLevel, max=60)
        panel.AddLine("Volume Level: ", VolumeLevelCtrl)
        while panel.Affirmed():
            panel.SetResult(VolumeLevelCtrl.GetValue())


class VolUp(eg.ActionBase):
    name = "Volume up"
    description = "Increase volume by one step"

    def __call__(self):
        self.plugin.sendCommand(b'MVUP\r')


class VolDown(eg.ActionBase):
    name = "Volume down"
    description = "Decrease volume by one step"

    def __call__(self):
        self.plugin.sendCommand(b'MVDOWN\r')


class VolPct(eg.ActionBase):
    name = "Volume Pct"
    description = "Increase/Decrease volume by a percentage amount of the current volume"

    def __call__(self, incDec, pctChange):
        newVolume = round(float(self.plugin.status_variables["Volume"]) * (1 + float(pctChange) / 100. * (incDec-0.5)*2))
        newVolume = int(min(60, newVolume))
        print newVolume
        cmd_str = b'MV%0d\r' % newVolume
        self.plugin.sendCommand(cmd_str)

    def Configure(self, incDec=0, pctChange=0):
        panel = eg.ConfigPanel()
        incDec_Ctrl = panel.Choice(incDec, choices=("decrease", "increase"))
        pctChangeCtrl = panel.SpinIntCtrl(pctChange, max=200)

        panel.AddLine(incDec_Ctrl, " by ", pctChangeCtrl, "%")
        while panel.Affirmed():
            panel.SetResult(incDec_Ctrl.GetValue(),
                pctChangeCtrl.GetValue())


class gradualVolChange(eg.ActionBase):
    def __call__(self, endVol, interval, up_down_both):
        #if there is a gradualVol_thread already running, cancel it
        if hasattr(self.plugin, 'stopGradualVolChange'):
            self.plugin.stopGradualVolChange.set()
            sleep(0.2)

        curVol = self.plugin.status_variables["Volume"]

        #set the cmd_str and nb of loops according to the up_down_both parameter
        if up_down_both == 0:
            nb_loops = max(endVol - curVol, 0)
            cmd_str = b'MVUP\r'
        elif up_down_both == 1:
            nb_loops = max(curVol - endVol, 0)
            cmd_str = b'MVDOWN\r'
        else:
            if curVol > endVol:
                cmd_str = b'MVDOWN\r'
            else:
                cmd_str = b'MVUP\r'
            nb_loops = abs(curVol - endVol)

        interval = max(interval, 0.2)  #'make sure the interval is at least 200msec'
        end_event_string = "GradualVolChange.Finished"

        self.plugin.stopGradualVolChange = Event()
        self.plugin.gradualVol_thread = Thread(
            target=self.plugin.repeatCommandThread,
            args=(self.plugin.stopGradualVolChange,
                  cmd_str,
                  interval,
                  nb_loops,
                  end_event_string)
        )
        self.plugin.gradualVol_thread.start()
        print "gradually changing volume from %0d to %0d using %0dsec intervals" % (curVol, endVol, interval)

    def Configure(self, endVol=10, interval=5, up_down_both=2):
        panel = eg.ConfigPanel()
        endVol_Ctrl = panel.SpinIntCtrl(endVol, max=60)
        interval_Ctrl = panel.SpinIntCtrl(interval, max=600)

        up_down_both_Ctrl = panel.Choice(up_down_both, choices=("only from below", "only from above", "no matter what direction"))

        panel.AddLine("Gradually change volume to: ", endVol_Ctrl)
        panel.AddLine("Change volume by 1 step every: ", interval_Ctrl, "sec.")
        panel.AddLine("Direction: ", up_down_both_Ctrl)


        while panel.Affirmed():
            panel.SetResult(endVol_Ctrl.GetValue(),
                interval_Ctrl.GetValue(),
                up_down_both_Ctrl.GetValue()
            )


class stopGradualVolChange(eg.ActionBase):
    def __call__(self):
        if hasattr(self.plugin, 'stopGradualVolChange'):
            self.plugin.stopGradualVolChange.set()
            sleep(0.2)










class NormalMode(eg.ActionBase):
    name = "Normal AudioMode"
    description = "Source Direct Input = True, Bass & Treble = default"

    def __call__(self):
        self.plugin.activateAudioMode(0)


class NightMode(eg.ActionBase):
    name = "Night AudioMode"
    description = "cut bass out"

    def __call__(self):
        self.plugin.activateAudioMode(1)


class StadiumMode(eg.ActionBase):
    name = "Stadium AudioMode"
    description = "push bass and treble"

    def __call__(self):
        self.plugin.activateAudioMode(2)


class NextAudioMode(eg.ActionBase):
    def __call__(self):
        self.plugin.switchToNextAudioMode()


class SwitchBetweenNormalAndNightAudioMode(eg.ActionBase):
    def __call__(self):
        if self.plugin.status_variables["AudioMode"] == 0:
            self.plugin.activateAudioMode(1)
        else:
            self.plugin.activateAudioMode(0)


class NightModeIfNoStadiumMode(eg.ActionBase):
    def __call__(self):
        if self.plugin.status_variables["AudioMode"] != 2:
            self.plugin.activateAudioMode(1)


#
# Timer & Clock
#
class TimerOn(eg.ActionBase):
    name = "Timer On"
    description = "Configure the timer and switch it on. Either once or every day."

    def __call__(self, start_h, start_min, end_h, end_min, vol, favouriteNb, timer_type):

        if timer_type == 0:
            timer_type_cmd = "ONCE"
        else:
            timer_type_cmd = "EVERY"

        if start_h > 11:
            start_h -= 12
            start_am_pm = "P"
        else:
            start_am_pm = "A"

        if end_h > 11:
            end_h -= 12
            end_am_pm = "P"
        else:
            end_am_pm = "A"

        cmd_str = b'TS%s %s%02d%02d-%s%02d%02d FA%02d %02d 1\r' % (timer_type_cmd,
                                                                   start_am_pm, start_h, start_min,
                                                                   end_am_pm, end_h, end_min,
                                                                   favouriteNb,
                                                                   vol)
        print cmd_str
        self.plugin.sendCommand(cmd_str)

    def Configure(self, start_h=7, start_min=30, end_h=7, end_min=45, vol=10, favouriteNb=1, timer_type=0):
        panel = eg.ConfigPanel()
        start_h_Ctrl = panel.SpinIntCtrl(start_h, max=23)
        start_min_Ctrl = panel.SpinIntCtrl(start_min, max=59)
        end_h_Ctrl = panel.SpinIntCtrl(end_h, max=23)
        end_min_Ctrl = panel.SpinIntCtrl(end_min, max=59)
        vol_Ctrl = panel.SpinIntCtrl(vol, max=60)
        favouriteNb_Ctrl = panel.SpinIntCtrl(favouriteNb, max=50)
        timer_typeCtrl = panel.Choice(timer_type, choices=("once", "every day"))

        panel.AddLine("Timer Type: ", timer_typeCtrl)
        panel.AddLine("Start time: ", start_h_Ctrl, "h", start_min_Ctrl, "min")
        panel.AddLine("End time: ", end_h_Ctrl, "h", end_min_Ctrl, "min")
        panel.AddLine("Volume level: ", vol_Ctrl)
        panel.AddLine("Favourite Number to call: ", favouriteNb_Ctrl)

        while panel.Affirmed():
            panel.SetResult(start_h_Ctrl.GetValue(),
                start_min_Ctrl.GetValue(),
                end_h_Ctrl.GetValue(),
                end_min_Ctrl.GetValue(),
                vol_Ctrl.GetValue(),
                favouriteNb_Ctrl.GetValue(),
                timer_typeCtrl.GetValue()
            )


class TimerOff(eg.ActionBase):
    name = "Timer Off"
    description = "Switch either the 'every day'- or 'once' timer off"

    def __call__(self, timer_type):
        if timer_type == 0:
            timer_type_cmd = "ONCE"
        else:
            timer_type_cmd = "EVERY"

        cmd_str = b'TS%s A0730-A0735 FA01 09 0\r' % timer_type_cmd
        self.plugin.sendCommand(cmd_str)

    def Configure(self, timer_type=0):
        panel = eg.ConfigPanel()
        timer_typeCtrl = panel.Choice(timer_type, choices=("once", "every day"))
        panel.AddLine("Timer Type to switch off: ", timer_typeCtrl)

        while panel.Affirmed():
            panel.SetResult(timer_typeCtrl.GetValue())


class Clock(eg.ActionBase):
    def __call__(self):
        self.plugin.sendCommand(b'CLK\r')


class setSleep(eg.ActionBase):
    name = "Set sleep"
    description = "Set the sleep mode of the amplifier"

    def __call__(self, sleep_min):
        if sleep_min == 0:
            cmd_str = b'SLPOFF\r'
        else:
            cmd_str = b'SLP%03d\r' % sleep_min
        self.plugin.sendCommand(cmd_str)

    def Configure(self, sleep_min=0):
        panel = eg.ConfigPanel()
        sleep_minCtrl = panel.SpinIntCtrl(sleep_min, max=90)
        panel.AddLine("Sleep time:", sleep_minCtrl, "min")
        while panel.Affirmed():
            panel.SetResult(sleep_minCtrl.GetValue())


#
# Favourites
#
class Favourite(eg.ActionBase):
    name = "Go to Favourite"
    description = "Go to a specified Favourite"

    def __call__(self, favouriteNb):
        cmd_str = b'FV %02d\r' % favouriteNb
        self.plugin.sendCommand(cmd_str)

    def Configure(self, favouriteNb=1):
        panel = eg.ConfigPanel()
        favouriteNbCtrl = panel.SpinIntCtrl(favouriteNb, max=50)
        panel.AddLine("Favourite Number:", favouriteNbCtrl)
        while panel.Affirmed():
            panel.SetResult(favouriteNbCtrl.GetValue())


#
# Read Amp's Display
#
class ReadAmpDisplay(eg.ActionBase):
    def __call__(self):
        self.plugin.sendCommand(b'NSE\r')
        sleep(1)

        if self.plugin.status_variables["Input"] == self.plugin.InputNames["Digital In"]:
            display_output = "Input: " + self.plugin.InputNames["Digital In"]
        else:
            display_output_list = [line.strip() for line in self.plugin.status_variables["Display"] if (line.strip())]

            if not self.plugin.status_variables["Input"] == "Internet Radio":
                if display_output_list[0] == "Now Playing":
                    display_output_list[2] = display_output_list[2] + " - " + display_output_list[1]
                    display_output_list = display_output_list[2:len(display_output_list)]

            display_output = ""
            for line in display_output_list:
                display_output += line + "\n"
            display_output = display_output[0:len(display_output) - 1]  #remove the last "\n"

        self.plugin.TriggerEvent("Display", payload=display_output)


class PrintCurrentParameters(eg.ActionBase):
    def __call__(self):
        for variable in self.plugin.status_variables:
            print variable, ": ", self.plugin.status_variables[variable]


class setDisplayBrightness(eg.ActionBase):
    name = "Set Display Brightness"
    description = "Set the brightness of the display to a specified value"

    def __call__(self, brightness_pct):
        cmd_str = b'SSDIM%03d\r' % brightness_pct
        self.plugin.sendCommand(cmd_str)

    def Configure(self, brightness_pct=100):
        panel = eg.ConfigPanel()
        brightness_pctCtrl = panel.SpinIntCtrl(brightness_pct, max=100)
        panel.AddLine("Brightness in percent:", brightness_pctCtrl, "%")
        while panel.Affirmed():
            panel.SetResult(brightness_pctCtrl.GetValue())


class sendCustomCommand(eg.ActionBase):
    name = "send custom command"
    description = "Send any specified command to the amplifier. The <CR> is automatically added at the end."

    def __call__(self, cmd_str_raw):
        cmd_str = cmd_str_raw + "\r"
        self.plugin.sendCommand(cmd_str)

    def Configure(self, cmd_str_raw="PWON"):
        panel = eg.ConfigPanel()
        cmd_str_rawCtrl = panel.TextCtrl(cmd_str_raw)
        panel.AddLine("Command (without <CR>):", cmd_str_rawCtrl)
        while panel.Affirmed():
            panel.SetResult(cmd_str_rawCtrl.GetValue())


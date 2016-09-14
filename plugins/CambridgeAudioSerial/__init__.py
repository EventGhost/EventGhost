# -*- coding: utf-8 -*-
#
# plugins/CambridgeAudioSerial/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.
#
# CambridgeAudioSerial V0.2
# ================
# Written by Pavel Ivanov aka Johnson, <johnsik@gmail.com>
# Public Domain
#
# Revision history:
# -----------------
# 0.1 - (29.10.09)	initial
# 0.2 - (20.02.09)	completely rewriting code for 'Volume Up until event end'/'Volume Down until event end' actions
#							new 'Toggle Mute' action
#							correct range for 'InputSelect' action

help = '''\
Small trivial plugin to control Cambridge Audio AMPs via RS-232.
Developed and tested with an AMP 840A V2 only, but must work with
AMPs 840A V1 and 840E also.

Replies, Updates and Errors from the AMP are turned into events. Description of
commands and their replies can be found in the document
'AP194942azur840AERS232CSerialControlProtocolV1-1.pdf', which is available from the
Cambridge Audio websites.'''

eg.RegisterPlugin(
    name = 'CambridgeAudio Amps Serial',
    author = 'Johnson',
    version = '0.2',
    kind = 'external',
    guid = "{C1B266B0-005B-4A97-8F33-8D12512A2050}",
    description = 'Control Cambridge Audio Amps via RS232',
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1990",
    help = help,
    canMultiLoad = True,
    createMacrosOnAdd = True,
)


import threading
import time
import re


class conf:
    FirstVolumeRepeatPause = 0.3
    NextVolumeRepeatPause = 0.110


class current:
    Volume = 50
    Mute = False


cmdList = (
('Power', None, None, None),
('PowerOn', 'Power On', '1,11,1', None),
('PowerOff', 'Power Standby', '1,11,0', None),

('Volume', None, None, None),
('MuteOff', 'Mute Off', '1,12,0', None),
('MuteOn', 'Mute On', '1,12,1', None),
('VolumeGoto', 'Goto Volume x (00-96, 96=0dB)', '1,13,x', '00-96'),
('VolumeUp', 'Volume Up', '1,14,', None),
('VolumeDown', 'Volume Down', '1,15,', None),
('VolumeStop', 'Volume Stop', '1,16,', None),
('BalanceSet', 'Set Balance Level x (00-16, 00:max left, 08:neutral, 16:max right)', '1,17,x', '00-16'),
('BalanceRight', 'Balance Right', '1,18,', None),
('BalanceLeft', 'Balance Left', '1,19,', None),

('Inputs/Routing', None, None, None),
('InputSelect', 'Select Input x (01-07)', '1,x,', '01-07'),
('TapeMonitorOff', 'Tape Monitor Off', '1,08,0', None),
('TapeMonitorOn', 'Tape Monitor On', '1,08,1', None),
('InputUp', 'Main Input Up', '1,09,', None),
('InputDown', 'Main Input Down', '1,10,', None),
('SpeakerSelect', 'Select Speaker (0-2, 0:A, 1:AB, 2:B)', '1,21,x', '0-2'),
('AbusInputSelect', 'Select Abus Input (1-8)', '1,23,x', '1-8'),
('Input1NameSet', 'Set Input x Name (1-8,Name[8])', '2,03,x', '1-8,Name'),

('Parameters', None, None, None),
('LCDBrightnessSet', 'Set LCD Brightness (0-2, 0:Off, 1:Dim, 2:Bright)', '1,20,x', '0-2'),
('BassSet', 'Set Bass (00-30, 00:min, 15:neutral, 30:max)', '1,24,x', '00-30'),
('TrebleSet', 'Set Treble (00-30, 00:min, 15:neutral, 30:max)', '1,25,x', '00-30'),
('DirectOff', 'Set Direct Off', '1,26,0', None),
('DirectOn', 'Set Direct On', '1,26,1', None),
('SoftwareVersionGet', 'Get Software Version', '2,01,', None),
('ProtocolVersionGet', 'Get Protocol Version', '2,02,', None),

(None,None,None,None),
)

EventList = {
    '3':{
        'content':'Setup',
        '01':'SoftwareVersion',
        '02':'ProtocolVersion',
        '03':'InputNameChanged'
    },
    '4':{
        'content':'Update',
        '01':'Input1Selected',
        '02':'Input2Selected',
        '03':'Input3Selected',
        '04':'Input4Selected',
        '05':'Input5Selected',
        '06':'Input6Selected',
        '07':'Input7Selected',
        '08':'TapeMonitorChanged',
        '11':'PowerStateChanged',
        '12':'MuteStateChanged',
        '13':'VolumeChanged',
        '14':'Volume+',
        '15':'Volume-',
        '16':'VolumeStopped',
        '17':'BalanceChanged',
        '20':'LCDBrightnessChanged',
        '21':'SpeakerSelectionChanged',
        '22':'HeadphonesInOut',
        '23':'A-BUSInputSourceChanged',
        '24':'BassLevelChanged',
        '25':'TrebleLevelChanged',
        '26':'DirectStateChanged'
    },
    '5':{
        'content':'Error',
        '01':'Overload',
        '02':'DCOffset',
        '03':'OverTemperature',
        '04':'Clipping',
        '05':'MainsFail',
        '06':'SpeakerFail',
        '07':'CommandGroupUnknown',
        '08':'CommandNumberUnknown',
        '09':'CommandData'
    }
}



class CmdAction(eg.ActionClass):
    '''Base class for all argumentless actions'''

    def __call__(self):
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write('#' + self.cmd + chr(13))
        self.plugin.serialThread.ResumeReadEvents()



class ValueAction(eg.ActionWithStringParameter):
    '''Base class for all actions with adjustable argument'''

    def __call__(self, data):
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write('#' + self.cmdLeft + str(data) + self.cmdRight + chr(13))
        self.plugin.serialThread.ResumeReadEvents()



class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'

    def __call__(self, data):
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(str(data) + chr(13))
        self.plugin.serialThread.ResumeReadEvents()



class VolumeAction(eg.ActionClass):
    def __call__(self):
        self.VolumeThread = threading.Thread(
            target=self.VolumeThreadLoop,
            name="VolumeThread",
            args=(eg.event, current.Volume, self.increment,)
        )
        self.VolumeThread.start()


    def VolumeThreadLoop(self, event, vol, increment):
        firstLoop = True
        while not event.isEnded:
            vol += increment
            if (vol < 1) or (vol > 96): break
            self.plugin.serialThread.SuspendReadEvents()
            self.plugin.serialThread.Write('#1,13,' + format(vol, '02d') + chr(13))
            self.plugin.serialThread.ResumeReadEvents()
            if firstLoop:
                time.sleep(conf.FirstVolumeRepeatPause)
                firstLoop = False
            else:
                time.sleep(conf.NextVolumeRepeatPause)



class ToggleMuteAction(eg.ActionClass):
    def __call__(self):
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write('#1,12,' + str(int(not current.Mute)) + chr(13))
        self.plugin.serialThread.ResumeReadEvents()



class CambridgeAudioSerial(eg.PluginClass):

    def __init__(self):
        self.serialThread = eg.SerialThread()

        group = self
        for cmd_name, cmd_text, cmd_cmd, cmd_rangespec in cmdList:
            if cmd_text is None:
                # New subgroup, or back up
                if cmd_name is None:
                    group = self
                else:
                    group = self.AddGroup(cmd_name)
                if cmd_name == 'Volume': groupVolume = group
            elif cmd_rangespec is not None:
                # Command with argument
                actionName, paramDescr = cmd_text.split('(')
                actionName = actionName.strip()
                paramDescr = paramDescr[:-1]
                _cmdLeft, _cmdRight = cmd_cmd.split('x')

                class Action(ValueAction):
                    name = actionName
                    cmd = cmd_cmd
                    parameterDescription = 'Value: (%s)' % paramDescr
                    cmdLeft = _cmdLeft
                    cmdRight = _cmdRight
                Action.__name__ = cmd_name
                group.AddAction(Action)
            else:
                # Argumentless command
                class Action(CmdAction):
                    name = cmd_text
                    cmd = cmd_cmd
                Action.__name__ = cmd_name
                group.AddAction(Action)

        group.AddAction(Raw)

        class Action(VolumeAction):
            name = 'Volume Up until event end'
            increment = 1
        Action.__name__ = 'VolumeUpUntilEnd'
        groupVolume.AddAction(Action)

        class Action(VolumeAction):
            name = 'Volume Down until event end'
            increment = -1
        Action.__name__ = 'VolumeDownUntilEnd'
        groupVolume.AddAction(Action)

        class Action(ToggleMuteAction):
            name = 'Toggle Mute'
        Action.__name__ = 'ToggleMute'
        groupVolume.AddAction(Action)



    def __start__(self, port):
        self.port = port
        self.serialThread.parmre = re.compile('#(\d),(\d\d),(([^,]+)?(,(.*))?)??$')
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, 9600, '8N1')
        self.serialThread.SetRts(0)
        self.serialThread.Start()
        current.Volume = 50


    def __stop__(self):
        self.serialThread.Close()


    def Configure(self, port=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine('Port:', portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())


    def OnReceive(self, serial):
        buffer = ''
        while True:
            ch = serial.Read(1, 0.1)
            if (ch == ''): return		# nothing received inside timeout, possibly indicates erroneous data

            if (ch != '\r'):
                buffer += ch
                continue

            m = self.serialThread.parmre.match(buffer)
            if (m is not None) and (m.group(1) in EventList) and (m.group(2) in EventList[m.group(1)]):

                if (EventList[m.group(1)][m.group(2)] == 'VolumeChanged'):
                    current.Volume = int(m.group(3))
                elif (EventList[m.group(1)][m.group(2)] == 'MuteStateChanged'):
                    current.Mute = bool(int(m.group(3)))

                self.TriggerEvent(EventList[m.group(1)]['content'] + '.' + EventList[m.group(1)][m.group(2)], payload = m.group(3))
            else:
                self.TriggerEvent('Unknown(' + buffer + ')')
            return

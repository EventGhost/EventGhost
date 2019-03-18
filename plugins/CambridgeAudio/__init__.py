# -*- coding: latin-1 -*-
#
# Cambridge Audio v0.5
# ================
# Written by Craig Haskins, <craig.r.haskins@gmail.com>
# Public Domain
#
# Control Cambridge Audio AV Receivers via Serial Port
#
# This plugin is based on the YamahaSerial plugin by Mark Clarkson which
# itself was based on DenonSerial by Oliver Wagner.  Credit is due to
# all those who came before.
#
# This plugin has been developed using the document
# "Azur 540R v3 Serial Control Protocol V1.0" and has been tested on a 
# 340R Receiver.  Should work on both 540R and 640R receivers although
# the latter has a few extra commands (that could easily be added)
#
# Responses are turned into Events of the form Group.Command.State
# eg. for volume up you'll see and event such as 
#    CambridgeAudio.Amplifier.VolumeUp.-43dB
#
# Revision history:
# -----------------
# 0.5 Initial Rev

import eg

eg.RegisterPlugin(
    name="Cambridge Audio",
    guid='{870EDFC0-B7A8-43CB-9A9F-C6E5EDF37DE6}',
    author="Craig Haskins",
    version="0.5." + "$LastChangedRevision: 314 $".split()[1],
    kind="external",
    url="",
    description="Control Cambridge Audio 340R AV Receiver",
    canMultiLoad=True,
    createMacrosOnAdd=True,
)

import re
import thread
import wx


Commands = (
    ('Amplifier', '1', 'Amplifier control commands',
     (
         ('Power', 'Stanby / On',
          (
              ('On', '01', '1'),
              ('Off', '01', '0'),
          ),
          ),
         ('Volume', 'Main Volume Up/Down ',
          (
              ('Up', '02', ''),
              ('Down', '03', ''),
          ),
          ),
         ('Bass', 'Tone Controls',
          (
              ('Up', '04', ''),
              ('Down', '05', ''),
          ),
          ),
         ('Treble', 'Tone Controls',
          (
              ('Up', '06', ''),
              ('Down', '07', ''),
          ),
          ),
         ('Subwoofer', 'Subwoofer On/Off',
          (
              ('On', '08', ''),
              ('Off', '09', ''),
          ),
          ),
         ('LFE Trim', 'Subwoofer Attenuation',
          (
              ('0dB', '10', '0'),
              ('-1dB', '10', '1'),
              ('-2dB', '10', '2'),
              ('-3dB', '10', '3'),
              ('-4dB', '10', '4'),
              ('-5dB', '10', '5'),
              ('-6dB', '10', '6'),
              ('-7dB', '10', '7'),
              ('-8dB', '10', '8'),
              ('-9dB', '10', '9'),
              ('-10dB', '10', '10'),
          ),
          ),
         ('Mute', 'Output Mute',
          (
              ('On', '11', '1'),
              ('Off', '11', '0'),
          ),
          ),
         ('DRC', 'Dynamic Range Control',
          (
              ('0/4', '12', '0'),
              ('1/4', '12', '1'),
              ('2/4', '12', '2'),
              ('3/4', '12', '3'),
              ('4/4', '12', '4'),
          ),
          ),
         ('OSD', 'On Screen Display Navigation',
          (
              ('On', '13', ''),
              ('Off', '14', ''),
              ('Up', '15', ''),
              ('Down', '16', ''),
              ('Left', '17', ''),
              ('Right', '18', ''),
              ('Enter', '19', ''),
          ),
          ),
     ),
     ),
    ('Source', '2', 'Source Selection Commands',
     (
         ('Input', 'Input Selection',
          (
              ('Up', '02', ''),
              ('Down', '03', ''),
              ('DVD', '01', '1'),
              ('Video 1', '01', '2'),
              ('Tuner', '01', '3'),
              ('Video 2', '01', '4'),
              ('Video 3', '01', '5'),
              ('Tape', '01', '6'),
              ('CD/Aux', '01', '7'),
              ('Direct In', '01', '8'),
          )
          ),
         ('Mode', 'Analog / Digital Selection',
          (
              ('Analog', '04', '0'),
              ('Digital', '04', '1'),
          ),
          ),
     ),
     ),
    ('Tuner', '3', 'Tuner Commands',
     (
         ('Mode', 'Mono / Stereo',
          (
              ('Mono', '01', '1'),
              ('Stereo', '01', '0'),
          ),
          ),
         ('Frequency', 'Frequency & Band',
          (
              ('Up', '02', ''),
              ('Down', '03', ''),
              ('FM', '09', '0'),
              ('AM', '09', '1'),
          ),
          ),
         ('Control', 'Tunner Control',
          (
              ('Up', '04', ''),
              ('Down', '05', ''),
              ('Frequency', '06', '1'),
              ('Search', '06', '2'),
              ('Preset', '06', '3'),
          ),
          ),
         ('Preset', 'Preset Selection',
          (
              ('1', '12', '1'),
              ('2', '12', '1'),
              ('3', '12', '1'),
              ('4', '12', '1'),
              ('5', '12', '1'),
              ('6', '12', '1'),
          ),
          ),
         ('Query', 'Info Commands',
          (
              ('Frequency', '14', ''),
              ('Name', '15', ''),
              ('PTY', '16', ''),
          ),
          ),
     ),
     ),
    ('Processing', '4', 'Signal Processing',
     (
         ('Stereo', 'Stereo Modes',
          (
              ('Stereo', '01', '0'),
              ('Stero+Sub', '01', '1'),
          ),
          ),
         ('DSP', 'Prologic, DTS & DSP Effects',
          (
              ('Prologic II/Neo/DSP', '02', ''),
              ('DD/DTS', '03', ''),
              ('Effect', '06', ''),
          ),
          ),
         ('Query', 'Mode Query',
          (
              ('Progloic', '04', ''),
              ('DTS', '05', ''),
          ),
          ),
     ),
     ),
    ('Version', '5', 'Version Info',
     (
         (' ', ' ',
          (
              ('Software', '01', ''),
              ('Protocol', '02', ''),
          ),
          ),
     ),
     ),
)

Responses = {'6': ('Amplifier',
                   {'01': ('Power', ('Standby', 'On')),
                    '02': ('VolumeUp', 'dB'),
                    '03': ('VolumeDown', 'dB'),
                    '04': ('BassUp', 'dB'),
                    '05': ('BassDown', 'dB'),
                    '06': ('TrebleUp', 'dB'),
                    '07': ('TrebleDown', 'dB'),
                    '08': ('SubOn', ''),
                    '09': ('SubOff', ''),
                    '10': ('LFETrim', 'dB'),
                    '11': ('Mute', ('Off', 'On')),
                    '12': ('DRC', ''),
                    '13': ('OSDOn', ''),
                    '14': ('OSDOff', ''),
                    '15': ('OSDUp', ''),
                    '16': ('OSDDown', ''),
                    '17': ('OSDLeft', ''),
                    '18': ('OSDRight', ''),
                    '19': ('OSDEnter', ''),
                    }
                   ),
             '7': ('Source',
                   {'01': ('Input', ('', 'DVD', 'Video1', 'Tuner', 'Video2', 'Video3', 'Tape', 'CD', 'Direct')),
                    '02': ('InputUp', ''),
                    '03': ('InputDown', ''),
                    '04': ('Mode', ('Analog', 'Digital')),
                    }
                   ),
             '9': ('Processing',
                   {'01': ('Stereo', ('Stereo', 'Stereo+Sub')),
                    '02': ('PLII', ''),
                    '03': ('DTS', ''),
                    '04': ('PLII', ''),
                    '05': ('DTS', ''),
                    '06': ('DSP', '')
                    }
                   )
             }


class CambridgeAudio(eg.PluginClass):
    canMultiLoad = True

    def __init__(self):
        self.serial = None
        group = self
        self.currentVolume = -99
        self.TypList = {
            '0': 'RS232',
            '1': 'IR',
            '2': 'Keys',
            '3': 'System',
            '4': 'Encoder'
        }
        self.GRDList = {
            '0': 'NoGuard',
            '1': 'GuardBySystem',
            '2': 'GuardBySetting'
        }

        def createWriter(cmd):
            def write(self):
                # print cmd
                self.plugin.serial.write(cmd)
                self.plugin.serial.write('\r')

            return write

        for group_name, group_num, group_desc, cmdList in Commands:
            print group_name
            group = self.AddGroup(group_name)
            for cmd_name, cmd_desc, stateList in cmdList:
                print '  ' + cmd_desc
                cmd_group = group.AddGroup(cmd_name)
                for state_desc, cmd_num, cmd_data in stateList:
                    full_cmd = group_name + '_' + cmd_name + '_' + state_desc
                    print '    ' + state_desc

                    class Handler(eg.ActionClass):
                        name = cmd_name + ' ' + state_desc
                        description = cmd_name
                        cmd_cmd = '#' + group_num + ',' + cmd_num + ',' + cmd_data
                        __call__ = createWriter(cmd_cmd)

                    cmdify = re.compile('(\\+|\\ |&|\\\\|/)')
                    full_cmd = cmdify.sub('_', full_cmd)
                    print 'cmd: ' + full_cmd
                    Handler.__name__ = full_cmd
                    cmd_group.AddAction(Handler)

    # Serial port reader
    def reader(self):
        line = ""
        while self.readerkiller is False:
            ch = self.serial.read()
            if ch == '\r':
                # print('line: ' + line)
                if len(line.split(',')) == 3:
                    group, cmd, data = line.split(',')
                else:
                    group, cmd = line.split(',')
                    data = ''

                group = group[1]

                print('group: ' + group + ' cmd: ' + cmd + ' data: ' + data)

                group_name, cmd_dict = Responses[group]
                cmd_name, data_label = cmd_dict[cmd]
                # print(group_name + ': ' + cmd_name + ' ' + data + data_label)
                if isinstance(data_label, tuple):
                    self.TriggerEvent(group_name + '.' + cmd_name + '.' + data_label[int(data)])
                else:
                    if len(data) > 0:
                        self.TriggerEvent(group_name + '.' + cmd_name + '.' + data + data_label)
                    else:
                        self.TriggerEvent(group_name + '.' + cmd_name)

                line = ""
            else:
                line += ch
        self.readerkiller = None

    def __start__(self, port):
        self.serial = eg.SerialPort(port)
        self.serial.baudrate = 9600
        self.serial.timeout = 30.0
        self.serial.setDTR(1)
        self.serial.setRTS(1)
        self.readerkiller = False
        thread.start_new_thread(self.reader, ());

    def __stop__(self):
        self.readerkiller = True
        while self.readerkiller is not None:
            wx.MilliSleep(100)
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    def Configure(self, port=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Port:", portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())

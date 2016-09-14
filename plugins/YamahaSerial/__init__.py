# -*- coding: latin-1 -*-
#
# YamahaSerial V0.0.1
# ================
# Written by Mark Clarkson, <mark@hollowhills.net>
# Public Domain
#
# Small trivial plugin to control Yamaha RX-V1000 AMP via RS-232
#
# Data from the AVR is turned into events. Description of
# commands and their replies can be found in the document
# "RS232C.PDF", which is available from the Yamaha.  The document
# was once available on the Yamaha website, but now is only available
# by request.
#
# Credit is due Oliver Wagner, <owagner@hometheatersoftware.com> who
# developed the DenonSerial plug-in for EG, and upon who'se code this
# plug-in is based.
# Credit is also due to Jens Samuelson who developed the Yamaha RX-V1500
# lua script for Girder 4.  I originally adapted Mr. Samuelson's code to
# control the RX-V1000 in Girder 4, and have adapted it again here for EG.
#
# Obviously, this code has been patched together from the work of others;
# it may not be perfect, but it works (please cut me some slack, I'm an
# engineer, not a programmer).
#
# I have not implemented all of the functionality included in the original
# code upon which this plug-in is based; I don't need it right now. Items
# not included, but that I may add sometime in the future:
#   Decode power-on response    - Now I only identify that power
#                               has been turned on
#   Tuner control               - I don't use the tuner, so have not included any
#                               of the tuner functions
#   Error Checking              - I have included no error checking/handling at all;
#                               neither for the script, not for the RX-V1000
#   Direct volume control       - Mr. Wagner's DenonSerial plug-in incorporates
#                               direct volume control and a fader.
#   String Hex Processing       - A better way to handle string hex --> int conversion
#
# Revision history:
# -----------------
# 0.0.1 - initial
#


eg.RegisterPlugin(
    name = "Yamaha RX-V1000 Serial",
    author = "Mark Clarkson",
    version = "0.1.1093",
    kind = "external",
    guid = "{A961D3D4-5AE2-4F76-B88C-7D8865C56C23}",
    url = "http://www.eventghost.org/forum/viewtopic.php?t=123",
    description = "Control Yamaha RX-V1000 receivers using RS232.",
    canMultiLoad = True,
    createMacrosOnAdd = True,
)

import thread
import time
import re


cmdList = (
('PowerOn', 'Power On', '07a1d', None),
('PowerOff', 'Power Standby', '07a1e', None),

('ReadyCmd', 'Ready Command', '\x11000\x03', None),
('ResetCmd', 'Reset all RS232 controlled settings', '\x13\x7f\x7f\x7f\x03', None),

('System Commands', None, None, None),
('RequestTuningFreq','Request Tuning Frequency', '22000', None),
('RequestMainVol','Request Main Volume', '22001', None),
('RequestInputName','Request Input Name', '22003', None),
('RequestZone2InputName','Request Zone 2 Input Name', '22004', None),

('Volume Controls', None, None, None),
('MasterUp', 'Master Volume Up', '07a1a', None),
('MasterDown', 'Master Volume Down', '07a1b', None),
('MuteOn', 'Mute On', '07ea2', None),
('MuteOff', 'Mute Off', '07ea3', None),

('Inputs/Routing', None, None, None),
('InputPhono', 'Input Phono', '07a14', None),
('InputCD', 'Input CD', '07a15', None),
('InputTuner', 'Input Tuner', '07a16', None),
('InputCDR', 'Input CD-R', '07a19', None),
('InputMDTape', 'Input MD/TAPE', '07ac9', None),
('InputDVD', 'Input DVD', '07ac1', None),
('InputDTVLD', 'Input DTV/LD', '07a54', None),
('InputCable', 'Input Cable/Sat', '07ac0', None),
('InputVCR1', 'Input VCR-1', '07a0f', None),
('InputVCR2DVR', 'Input VCR-2/DVR', '07a13', None),
('InputAux', 'Input Aux', '07a55', None),

('Input Mode', None, None, None),
('InputAuto', 'Auto Audio Signal Mode', '07ea6', None),
('InputDTS', 'DTS Audio Signal Mode', '07ea8', None),
('InputAnalog', 'Analog Audio Signal Mode', '07eaa', None),

('OSD', None, None, None),
('OSDOff', 'OSD Off', '07eb0', None),
('OSDShort', 'Short OSD', '07eb1', None),
('OSDFull', 'Full OSD', '07eb2', None),

('DSP', None, None, None),
('DSPOff', 'DSP Effect Off', '07ee0', None),
('DSPHall1', 'DSP - Concert Hall 1', '07ee1', None),
('DSPHall2', 'DSP - Concert Hall 2', '07ee4', None),
('DSPChurch', 'DSP - Church', '07ee5', None),
('DSPJazz', 'DSP - Jazz Club', '07ee8', None),
('DSPRock', 'DSP - Rock Concert', '07ee9', None),
('DSPStadium', 'DSP - Stadium', '07ebb', None),
('DSPDisco', 'DSP - Disco', '07eed', None),
('DSPGame', 'DSP - Game', '07ee1', None),
('DSP6ch', 'DSP - 6ch Stereo', '07eef', None),
('DSPTVSports', 'DSP - TV Sports', '07ef1', None),
('DSPMonoMovie', 'DSP - Mono Movie', '07ef2', None),
('DSP70mmSpectacle', 'DSP - 70mm Spectacle', '07ef4', None),
('DSP70mmSciFi', 'DSP - 70mm Sci-Fi', '07ef5', None),
('DSP70mmAdventure', 'DSP - 70mm Adventure', '07ef6', None),
('DSP70mmGeneral', 'DSP - 70mm General', '07ef7', None),
('DSPDTSNormal', 'DSP - Normal DTS', '07ef8', None),
('DSPDTSEnhanced', 'DSP - Enhanced DTS', '07ef9', None),

(None,None,None,None),
('Raw', 'Send Raw command', '', '*'),
)

class YamahaSerial(eg.PluginClass):

    def __init__(self):
        self.serial = None
        group = self
        self.currentVolume = -99
        self.TypList = {
            '0':'RS232',
            '1':'IR',
            '2':'Keys',
            '3':'System',
            '4':'Encoder'
        }
        self.GRDList = {
            '0':'NoGuard',
            '1':'GuardBySystem',
            '2':'GuardBySetting'
        }

        self.EventList = {
            '00':{
                'content':'NoGuard',
                '00':'Ok',
                '01':'Busy',
                '02':'PowerOff'
                },
            '01':{
                'content':'Warning',
                '00':'OverCurrent',
                '01':'DCDetect',
                '02':'PowerTrouble',
                '03':'OverHeat'
                },
            '10':{
                'content':'Playback',
                '00':'ExternalDecoder',
                '01':'Analog',
                '02':'PCM',
                '03':'DD',
                '04':'DD20',
                '05':'DDKaraoke',
                '06':'DD61',
                '07':'DTS',
                '08':'DTSES',
                '09':'Digital'
                },
            '11':{
                'content':'Fs',
                '00':'Analog',
                '01':'32kHz',
                '02':'441kHz',
                '03':'48kHz',
                '04':'64kHz',
                '05':'882kHz',
                '06':'96kHz',
                '07':'Unknown'
                },
            '12':{
                'content':'61ES',
                '00':'On',
                '01':'Off'
                },
            '13':{
                'content':'ThrBypass',
                '00':'Normal',
                '01':'Bypass'
                },
            '14':{
                'content':'REDDTS',
                '00':'Release',
                '01':'Wait'
                },
            '15':{
                'content':'Tuner',
                '00':'NotTuned',
                '01':'Tuned'
                },
            '20':{
                'content':'Power',
                '00':'Off',
                '01':'On'
                },
            '21':{
                'content':'Input',
# 0x is for 6ch off, 1x is for 6ch on
                '00':'Phono',
                '01':'CD',
                '02':'Tuner',
                '03':'CDR',
                '04':'MDTape',
                '05':'DVD',
                '06':'DTVLD',
                '07':'Cable',
                '09':'VCR1',
                '0A':'VCR2',
                '0B':'VAux',
                '10':'Phono',
                '11':'CD',
                '12':'Tuner',
                '13':'CDR',
                '14':'MDTape',
                '15':'DVD',
                '16':'DTVLD',
                '17':'Cable',
                '19':'VCR1',
                '1A':'VCR2',
                '1B':'VAux'
                },
            '22':{
                'content':'InputMode',
                '00':'Auto',
                '02':'DTS',
                '04':'Analog',
                '05':'AnalogOnly'
                },
            '23':{
                'content':'Mute',
                 '00':'Off',
                 '01':'On'
                },
            '24':{
                'content':'Zone2Input',
                '00':'Phono',
                '01':'CD',
                '02':'Tuner',
                '03':'CDR',
                '04':'MDTape',
                '05':'DVD',
                '06':'DTVLD',
                '07':'Cable',
                '09':'VCR1',
                '0A':'VCR2',
                '0B':'VAux'
                },
            '25':{
                'content':'Zone2Mute',
                '00':'Off',
                '01':'On'
                },
            '26':{
                'content':'MasterVolume'
                },
            '28':{
                'content':'DSP',
                '80':'Off',
                '00':'Hall1',
                '05':'Hall2',
                '08':'Church',
                '0D':'Jazz',
                '10':'Rock',
                '14':'Stadium',
                '18':'Disco',
                '19':'Game',
                '1A':'6chStereo',
                '1D':'TVSports',
                '20':'MonoMovie',
                '24':'70mmSpectacle',
                '25':'70mmSciFi',
                '28':'70mmAdventure',
                '29':'70mmGeneral',
                '2C':'Normal',
                '2D':'Enhanced'
                },
            '29':{
                'content':'TunerPage',
                '00':'A',
                '01':'B',
                '02':'C',
                '03':'D',
                '04':'E'
                },
            '2A':{
                'content':'TunerPreset',
                '00':'1',
                '01':'2',
                '02':'3',
                '03':'4',
                '04':'5',
                '05':'6',
                '06':'7',
                '07':'8'
                },
            '2B':{
                'content':'OSD',
                '00':'Full',
                '01':'Short',
                '02':'Off'
                },
            '2C':{
                'content':'Sleep',
                '00':'120',
                '01':'90',
                '02':'60',
                '03':'30',
                '04':'Off'
                },
            '2D':{
                'content':'61ESKey',
                '00':'Off',
                '01':'On'
                },
            '2E':{
                'content':'SpkrRelayA',
                '00':'Off',
                '01':'On'
                },
            '2F':{
                'content':'SpkrRelayB',
                '00':'Off',
                '01':'On'
                },
            '30':{
                'content':'HomeBank',
                '00':'Main',
                '01':'A',
                '02':'B',
                '03':'C'
                },
            '31':{
                'content':'HomePreset',
                '00':'A',
                '01':'B',
                '02':'C'
                },
            '32':{
                'content':'VolumeBank',
                '00':'Main',
                '01':'A',
                '02':'B',
                '03':'C'
                },
            '33':{
                'content':'VolumePreset',
                '00':'A',
                '01':'B',
                '02':'C'
                },
            '34':{
                'content':'Headphone',
                '00':'Off',
                '01':'On'
                },
            '35':{
                'content':'FMAM',
                '00':'FM',
                '01':'AM'
                }
            }

        def createWriter(cmd):
            def write(self):
                if not('\x11' in cmd or '\x12' in cmd or '\x13' in cmd or '\x03' in cmd or '\x02' in cmd):
                    self.plugin.serial.write('\x02')
                #print cmd
                self.plugin.serial.write(cmd)
                self.plugin.serial.write('\x03')
            return write

        for cmd_name, cmd_text, cmd_cmd, cmd_rangespec in cmdList:
            if cmd_text is None:
                # New subgroup, or back up
                if cmd_name is None:
                    group = self
                else:
                    group = self.AddGroup(cmd_name)
            else:
                # Argumentless command
                class Handler(eg.ActionClass):
                    name = cmd_name
                    description = cmd_text
                    __call__ = createWriter(cmd_cmd)
                Handler.__name__ = cmd_name
                group.AddAction(Handler)

    def hexToDec(self, hexstring):
        hexconv = {'0':0,'1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15}
        result = hexconv[hexstring[0]]*16+hexconv[hexstring[1]]
        return result

    #Process volume from hex string to -dB
    def processVolume(self, volstring):
        volumeChange = 'NC'
        step = 0.5
        newdbValue = self.hexToDec(volstring)*step - 99.5
        if newdbValue < self.currentVolume:
            volumeChange = 'Down'
        elif newdbValue > self.currentVolume:
            volumeChange = 'Up'
        else:
            volumeChange = 'None'

        self.TriggerEvent('MasterVolume' + '.' + str(newdbValue))

        self.currentVolume = newdbValue

        return volumeChange

    # Serial port reader
    def reader(self):
        line=""
        parmre=re.compile('(.)(.)(.)(..)(..)')
        while self.readerkiller is False:
            ch=self.serial.read()
            if ch=='\x03':
                #print('line: '+line)
                if line[0]=='\x12' and len(line)==43:
                    #print('Power On')
                    self.TriggerEvent('PowerOn')
                elif line[0]=='\x02' and len(line)==7:
                    #print('General Report')
                    m=parmre.match(line)
                    if m is not None:
                        #Process volume separately
                        if self.EventList[m.group(4)]['content']=='MasterVolume':
                            self.TriggerEvent(self.EventList[m.group(4)]['content'] + '.' + self.processVolume(m.group(5)))
                        else:
                            self.TriggerEvent(self.EventList[m.group(4)]['content'] + '.' + self.EventList[m.group(4)][m.group(5)])
                else:
                    print('Unrecognised Report')
                line=""
            else:
                line+=ch

    def __start__(self, port):
        self.serial = eg.SerialPort(port)
        self.serial.baudrate = 9600
        self.serial.timeout = 30.0
        self.serial.setDTR(1)
        self.serial.setRTS(1)
        self.readerkiller = False
        thread.start_new_thread(self.reader,());
        # Do an initial master volume query so we can track it
        #self.serial.write('\x02' + '22001' + '\x03');


    def __stop__(self):
        self.readerkiller = True
        if self.serial is not None:
            self.serial.close()
            self.serial = None


    def Configure(self, port=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Port:", portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())


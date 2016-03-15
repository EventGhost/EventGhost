#
# DenonSerial V0.5
# ================
# Written by Oliver Wagner, <owagner@hometheatersoftware.com>
# Public Domain
#
#
# Revision history:
# -----------------
# 0.1 - initial
# 0.2 - fixed config dialog
# 0.3 - FadeTo command is now protected against being called again
#       while a fade is in progress
# 0.4 - Added missing InputVAUX and RecordVAUX commands, for
#       selecting the front inputs
# 0.5 - EventGhost 0.3.1+ compatibility
# 0.6 - EventGhost 0.3.6+ compatibility (by bitmonster)

help = """\
Small trivial plugin to control Denon AVRs and AMPs via RS-232.
Developed and tested with an AVR 3806 only, but might work with
different devices. YMMV.

Replies from the AVR are turned into events. Description of
commands and their replies can be found in the document
"AVR3806_PROTOCOL.PDF", which is available from the Denon
websites.

The events are slightly rewritten in order to be
more useful within EventGhosts's event matching system:
<ul>
<li> Replies with trailing numbers have a "." prefixed to the number.
   This allows to match on the Event "DenonSerial.EVENTNAME.*", and
   parse the parameter. Trailing spaces are removed. Example:<br>
   MV70 -> MV.70<br>
   MVMAX 80 -> MVMAX.80</li>
<li>Similarily, ":" are replaced with ".":<br>
   PSSB:ON -> PSSB.ON</li>
</ul>

The plugin keeps track of the current master volume in order to
support the FadeTo command."""

eg.RegisterPlugin(
    name = "Denon AV Serial",
    author = "Oliver Wagner",
    version = "0.6.1093",
    kind = "external",
    guid = "{12103708-40A0-46AE-856F-711D07912CD1}",
    description = "Control Denon A/V Amps/Receivers via RS232",
    help = help,
    canMultiLoad = True,
    createMacrosOnAdd = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAA"
        "AAd0SU1FB9YDBAsPCqtpoiUAAAAWdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCAyLjZsqHS1"
        "AAADe0lEQVQ4T02TXVCUZRSAPyZsxpnqoovum+miq+6qFUJYQP7cogS2VpGFAAlKpyAC"
        "EVh+4k80WGADQWlxZRfZACH5ECVY5TdHiEbAIQVkHRzUCZK/ZWGXp10SxjPzXrzvvM9z"
        "zpw5xwUQXg7ndX1jw3VkYmrzycK/gusrgrB3z17hvXfffv2tN99YcXHEi///g07Bznkw"
        "+9i1yvAbqvJKolRJhJ2KQp4ZQWTWd5wsV9Ni6sWybn3tZWYXvjt531V1tgJF8lcEZbij"
        "MLgRbTpAVHcgyk5/QnSefHrmc7QdV1hbX9+VbAvuTk67ZpfVIDsWgu/ZfURfD+TElVBy"
        "m4+TooshvDaAL697EPOHLzK1L9prbayuWbYlwsLzFZfCql+Qx8XhqfoAZUsIhsEGLGsW"
        "Nm12FlZtTM0/w2DSEmn0dEgclRSFcFG8wcamTRAqtO0kpRficdQLpV5Gr7mf3qFHzC1u"
        "YF61MvrIztD0OsP3F6m/ZUDZ7klosxfxJZn0j04hpJ+uIvZ4EpJvJKhvFWOzW1lc2qT/"
        "zznuzdnoGnlG+8BDWnvMDE7M8q1eQcygN6GFkWj0nQgp+WUcilTyUaIHzRPtWKx2rLYt"
        "5hfXHBnMNIjDtHbfY3RmmcdLdkrEfKIHDyDLPYS6vhnhh9wSgiPCcYvbT+3gNQbGluib"
        "WOTG8EOaTGOY/nrKwPgynXdm+H3gCZkNeQ6BP0GnZGgMRoTUnDMcSfgaiUJKWuPP6MRx"
        "LhjvUN3Qh671NnVNQ1y9Oe2YgUmaeqY4WnMEpSgl5ORhzhmaEFRFpSTnOpool+GXFoa6"
        "sQNNXReVupucv9zHeWM3Gl0HNY0mci7VEtF2EJ+8fSTkpSP23EaYmpl1ySgowk8ehiTc"
        "i6iiExRcNKC+0IlG20m5XqRCK5J9qYxoMZSgail+scEUn6vn+bJFImxtbQkl5dWoCkvx"
        "Cg3k/Uh3grKCSahJJln3E8n1BSQ2JhArHuSTUgneET6kFWno6h3GyW5P4sqqRUhMLSCn"
        "uJQA+cdIFYF8GC3F/Xs3vDM8kaZ4sP+YD/4RX5B+Wk1l3SXnkG2zu7uwZrHuqa1rILuw"
        "hNSsfOSxsQQoPkN2WI4iPp7EzBx+dPRLb7zK0orl1Z2FEmwvTM4HZ0kzZvM7hqZfMbaJ"
        "jEw8YHh8kvrGFmr1euaf/iPZAW12uzD2t1n4DwtSpLoLWTYZAAAAAElFTkSuQmCC"
    ),
)


import thread
import time
import re


cmdList = (
('PowerOn', 'Power On', 'PWON', None),
('PowerOff', 'Power Standby', 'PWSTANDBY', None),

('Volume', None, None, None),
('MasterUp', 'Master Volume Up', 'MVUP', None),
('MasterDown', 'Master Volume Down', 'MVDOWN', None),
('MasterSet', 'Master Volume Set (0-99, 80=0dB, 99=---/MIN)', 'MV', '0-99'),
('MuteOn', 'Mute On', 'MUON', None),
('MuteOff', 'Mute Off', 'MUOFF', None),

('FrontLeftUp', 'Front Left Channel Up', 'CVFL UP', None),
('FrontLeftDown', 'Front Left Channel Down', 'CVFL DOWN', None),
('FrontLeftSet', 'Front Left Channel Set (38-62, 50=0dB)', 'CVFL ', '36-62'),

('FrontRightUp', 'Front Right Channel Up', 'CVFR UP', None),
('FrontRightDown', 'Front Right Channel Down', 'CVFR DOWN', None),
('FrontRightSet', 'Front Right Channel Set (38-62, 50=0dB)', 'CVFR ', '36-62'),

('CenterUp', 'Center Channel Up', 'CVC UP', None),
('CenterDown', 'Center Channel Down', 'CVC DOWN', None),
('CenterSet', 'Center Channel Set (38-62, 50=0dB)', 'CVC ', '36-62'),

('SubwooferUp', 'Subwoofer Channel Up', 'CVSW UP', None),
('SubwooferDown', 'Subwoofer Channel Down', 'CVSW DOWN', None),
('SubwooferSet', 'Subwoofer Channel Set (38-62, 50=0dB, 00=OFF)', 'CVSW ', '36-62,00'),

('SurroundLeftUp', 'Surround Left Channel Up', 'CVSL UP', None),
('SurroundLeftDown', 'Surround Left Channel Down', 'CVSL DOWN', None),
('SurroundLeftSet', 'Surround Left Channel Set (38-62, 50=0dB)', 'CVSL ', '36-62'),

('SurroundRightUp', 'Surround Right Channel Up', 'CVSR UP', None),
('SurroundRightDown', 'Surround Right Channel Down', 'CVSR DOWN', None),
('SurroundRightSet', 'Surround Right Channel Set (38-62, 50=0dB)', 'CVSR ', '36-62'),

('SurroundBackLeftUp', 'SurroundBack Left Channel Up', 'CVSBL UP', None),
('SurroundBackLeftDown', 'SurroundBack Left Channel Down', 'CVSBL DOWN', None),
('SurroundBackLeftSet', 'SurroundBack Left Channel Set (38-62, 50=0dB)', 'CVSBL ', '36-62'),

('SurroundBackRightUp', 'SurroundBack Right Channel Up', 'CVSBR UP', None),
('SurroundBackRightDown', 'SurroundBack Right Channel Down', 'CVSBR DOWN', None),
('SurroundBackRightSet', 'SurroundBack Right Channel Set (38-62, 50=0dB)', 'CVSBR ', '36-62'),

('SurroundBackSingleUp', 'SurroundBack Single Channel Up', 'CVSB UP', None),
('SurroundBackSingleDown', 'SurroundBack Single Channel Down', 'CVSB DOWN', None),
('SurroundBackSingleSet', 'SurroundBack Single Channel Set (38-62, 50=0dB)', 'CVSB ', '36-62'),

('MainZoneOn', 'Main Zone On', 'ZMON', None),
('MainZoneOff', 'Main Zone Off', 'ZMOFF', None),

('Inputs/Routing', None, None, None),
('InputPhono', 'Input Phono', 'SIPHONO', None),
('InputCD', 'Input CD', 'SICD', None),
('InputTuner', 'Input Tuner', 'SITUNER', None),
('InputDVD', 'Input DVD', 'SIDVD', None),
('InputVDP', 'Input VDP', 'SIVDP', None),
('InputTV', 'Input TV', 'SITV', None),
('InputDBS', 'Input DBS', 'SIDBS', None),
('InputAux', 'Input Aux', 'SIV.AUX', None),
('InputVCR1', 'Input VCR-1', 'SIVCR-1', None),
('InputVCR2', 'Input VCR-2', 'SIVCR-2', None),
('InputVCR3', 'Input VCR-3', 'SIVCR-3', None),
('InputCDR', 'Input CDR/TAPE', 'SICDR/TAPE', None),

('RecordSource', 'Record from Source', 'SRSOURCE', None),
('RecordPhono', 'Record Phono', 'SRPHONO', None),
('RecordCD', 'Record CD', 'SRCD', None),
('RecordTuner', 'Record Tuner', 'SRTUNER', None),
('RecordDVD', 'Record DVD', 'SRDVD', None),
('RecordVDP', 'Record VDP', 'SRVDP', None),
('RecordTV', 'Record TV', 'SRTV', None),
('RecordDBS', 'Record DBS', 'SRDBS', None),
('RecordAux', 'Record Aux', 'SRV.AUX', None),
('RecordVCR1', 'Record VCR-1', 'SRVCR-1', None),
('RecordVCR2', 'Record VCR-2', 'SRVCR-2', None),
('RecordVCR3', 'Record VCR-3', 'SRVCR-3', None),
('RecordCDR', 'Record CDR/TAPE', 'SRCDR/TAPE', None),

('VideoSource', 'Video from Source', 'SVSOURCE', None),
('VideoDVD', 'Video DVD', 'SVDVD', None),
('VideoVDP', 'Video VDP', 'SVVDP', None),
('VideoTV', 'Video TV', 'SVTV', None),
('VideoDBS', 'Video DBS', 'SVDBS', None),
('VideoVCR1', 'Video VCR-1', 'SVVCR-1', None),
('VideoVCR2', 'Video VCR-2', 'SVVCR-2', None),
('VideoVCR3', 'Video VCR-3', 'SVVCR-3', None),
('VideoAux', 'Video Aux', 'SVV.AUX', None),

('DigitalInAuto', 'Digital Input AUTO MODE', 'SDAUTO', None),
('DigitalPCM', 'Digital Input Force PCM', 'SDPCM', None),
('DigitalDTS', 'Digital Input Force DTS', 'SDDTS', None),
('DigitalRF', 'Digital Input RF Input', 'SDRF', None),
('Analog', 'Force Analog Input', 'SDANALOG', None),
('External1', 'External Input 1', 'SDEXT.IN-1', None),
('External2', 'External Input 2', 'SDEXT.IN-2', None),

('Surround Modes', None, None, None),

('SMDirect','Surround Mode DIRECT','MSDIRECT', None),
('SMPureDirect','Surround Mode PURE DIRECT','MSPURE DIRECT', None),
('SMStereo','Surround Mode STEREO','MSSTEREO', None),
('SMMultiChIn','Surround Mode MULTI CH IN','MSMULTI CH IN', None),
('SMMultiChDirect','Surround Mode MULTI CH DIRECT','MSMULTI CH DIRECT', None),
('SMMultiChPure','Surround Mode MULTI CH PURE','MSMULTI CH PURE', None),
('SMDolbyProLogic','Surround Mode DOLBY PRO LOGIC','MSDOLBY PRO LOGIC', None),
('SMDolbyPLII','Surround Mode DOLBY PL2','MSDOLBY PL2', None),
('SMDolbyPLIIx','Surround Mode DOLBY PL2X','MSDOLBY PL2X', None),
('SMDolbyDigital','Surround Mode DOLBY DIGITAL','MSDOLBY DIGITAL', None),
('SMDolbyDigitalEx','Surround Mode DOLBY D EX','MSDOLBY D EX', None),
('SMDTSNEO6','Surround Mode DTS NEO:6','MSDTS NEO:6', None),
('SMDTSSURROUND','Surround Mode DTS SURROUND','MSDTS SURROUND', None),
('SMDTSESDiscrete','Surround Mode DTS ES DSCRT6.1','MSDTS ES DSCRT6.1', None),
('SMDTSESMatrix','Surround Mode DTS ES MTRX6.1','MSDTS ES MTRX6.1', None),
('SMDolbyHP','Surround Mode DOLBY H/P','MSDOLBY H/P', None),
('SMDTSDolbyHP','Surround Mode DTS+DOLBY H/P','MSDTS+DOLBY H/P', None),
('SMHOMETHXCINEMA','Surround Mode HOME THX CINEMA','MSHOME THX CINEMA', None),
('SMTHX51','Surround Mode THX5.1','MSTHX5.1', None),
('SMTHXU2Cinema','Surround Mode THX U2 CINEMA','MSTHX U2 CINEMA', None),
('SMTHXMusicMode','Surround Mode THX MUSIC MODE','MSTHX MUSIC MODE', None),
('SMTHXGamesMode','Surround Mode THX GAMES MODE','MSTHX GAMES MODE', None),
('SMTHX61','Surround Mode THX6.1','MSTHX6.1', None),
('SMTHXSurroundEx','Surround Mode THX SURROUND EX','MSTHX SURROUND EX', None),
('SMWideScreen','Surround Mode WIDE SCREEN','MSWIDE SCREEN', None),
('SM5CHStereo','Surround Mode 5CH STEREO','MS5CH STEREO', None),
('SM7CHStereo','Surround Mode 7CH STEREO','MS7CH STEREO', None),
('SM9CHStereo','Surround Mode 9CH STEREO','MS9CH STEREO', None),
('SMSuperStadium','Surround Mode SUPER STADIUM','MSSUPER STADIUM', None),
('SMRockArena','Surround Mode ROCK ARENA','MSROCK ARENA', None),
('SMJazzClub','Surround Mode JAZZ CLUB','MSJAZZ CLUB', None),
('SMClassiConcert','Surround Mode CLASSIC CONCERT','MSCLASSIC CONCERT', None),
('SMMonoMovie','Surround Mode MONO MOVIE','MSMONO MOVIE', None),
('SMatrix','Surround Mode MATRIX','MSMATRIX', None),
('SMVideoGame','Surround Mode VIDEO GAME','MSVIDEO GAME', None),
('SMVirtual','Surround Mode VIRTUAL','MSVIRTUAL', None),
('SMMPEG2AAC','Surround Mode MPEG2 AAC','MSMPEG2 AAC', None),
('SMAACDolbyEX','Surround Mode AAC+DOLBY EX','MSAAC+DOLBY EX', None),
('SMUSER1','Surround Mode USER1','MSUSER1', None),
('SMUSER2','Surround Mode USER2','MSUSER2', None),
('SMUSER3','Surround Mode USER3','MSUSER3', None),
('SMUSER1Memory','Surround Mode USER1 MEMORY','MSUSER1 MEMORY', None),
('SMUSER2Memory','Surround Mode USER2 MEMORY','MSUSER2 MEMORY', None),
('SMUSER3Memory','Surround Mode USER3 MEMORY','MSUSER3 MEMORY', None),

('Parameters', None, None, None),
('ToneDefeatOn', 'Tone Defeat On', 'PSTONE DEFEAT ON', None),
('ToneDefeatOff', 'Tone Defeat Off', 'PSTONE DEFEAT OFF', None),

('SBMatrixOn', 'Surround Back Matrix', 'PSSB:MTRX ON', None),
('SBMatrixOff', 'Surround Back Non-Matrix', 'PSSB:MTRX OFF', None),
('SBPL2XCinema', 'Surround Back Prologic IIx-Cinema', 'PSSB:PL2X CINEMA', None),
('SBPL2XMusic', 'Surround Back Prologic IIx-Music', 'PSSB:PL2X MUSIC', None),
('SBOff', 'Surround Back Off', 'PSSB:OFF', None),

('ModeMusic', 'Programm Mode Music', 'PSMODE:MUSIC', None),
('ModeCinema', 'Programm Mode Cinema', 'PSMODE:CINEMA', None),
('ModeGame', 'Programm Mode Game', 'PSMODE:GAME', None),
('ModePLOld', 'Programm Mode ProLogic (old)', 'PSMODE:PRO LOGIC', None),

('RoomEqAudyssey', 'Room EQ Mode Audyssey', 'PSROOM EQ:AUDYSSEY', None),
('RoomEqFront', 'Room EQ Mode Front', 'PSROOM EQ:FRONT', None),
('RoomEqFlat', 'Room EQ Mode Flat', 'PSROOM EQ:FKAT', None),
('RoomEqManual', 'Room EQ Mode Manual', 'PSROOM EQ:MANUAL', None),
('RoomEqOff', 'Room EQ Off', 'PSROOM EQ:OFF', None),

('DelayUp', 'Audio Delay Increasse', 'PSDELAY UP', None),
('DelayDown', 'Audio Delay Decrease', 'PSDELAY DOWN', None),
('DelaySet', 'Audio Delay Set (0-999)', 'PSDELAY ', '0-999'),

('NightModeOn', 'Night Mode On', 'PSNIGHT ON', None),
('NightModeOff', 'Night Mode Off', 'PSNIGHT OFF', None),

('Zone 2', None, None, None),
('Z2On', 'Zone 2 On', 'Z2ON', None),
('Z2Off', 'Zone 2 Off', 'Z2OFF', None),
('Z2Source', 'Zone 2 Source', 'Z2SOURCE', None),
('Z2VolUp', 'Zone 2 Volume Up', 'Z2UP', None),
('Z2VolDown', 'Zone 2 Volume Down', 'Z2DOWN', None),
('Z2VolSet', 'Zone 2 Volume Set (10-99, 80=0dB, 99=---/MIN)', 'Z2', '0-99'),
('Z2MuteOn', 'Zone 2 Mute On', 'Z2MUON', None),
('Z2MuteOff', 'Zone 2 Mute Off', 'Z2MUOFF', None),
('Z2InputPhono', 'Zone 2 Input Phono', 'Z2PHONO', None),
('Z2InputCD', 'Zone 2 Input CD', 'Z2CD', None),
('Z2InputTuner', 'Zone 2 Input Tuner', 'Z2TUNER', None),
('Z2InputDVD', 'Zone 2 Input DVD', 'Z2DVD', None),
('Z2InputVDP', 'Zone 2 Input VDP', 'Z2VDP', None),
('Z2InputTV', 'Zone 2 Input TV', 'Z2TV', None),
('Z2InputDBS', 'Zone 2 Input DBS', 'Z2DBS', None),
('Z2InputVCR1', 'Zone 2 Input VCR-1', 'Z2VCR-1', None),
('Z2InputVCR2', 'Zone 2 Input VCR-2', 'Z2VCR-2', None),
('Z2InputVCR3', 'Zone 2 Input VCR-3', 'Z2VCR-3', None),
('Z2InputCDR', 'Zone 2 Input CDR/TAPE', 'Z2CDR/TAPE', None),

('Zone 3', None, None, None),
('Z3On', 'Zone 3 On', 'Z3ON', None),
('Z3Off', 'Zone 3 Off', 'Z3OFF', None),
('Z3Source', 'Zone 3 Source', 'Z3SOURCE', None),
('Z3VolUp', 'Zone 3 Volume Up', 'Z3UP', None),
('Z3VolDown', 'Zone 3 Volume Down', 'Z3DOWN', None),
('Z3VolSet', 'Zone 3 Volume Set (10-99, 80=0dB, 99=---/MIN)', 'Z3', '0-99'),
('Z3MuteOn', 'Zone 3 Mute On', 'Z3MUON', None),
('Z3MuteOff', 'Zone 3 Mute Off', 'Z3MUOFF', None),
('Z3InputPhono', 'Zone 3 Input Phono', 'Z3PHONO', None),
('Z3InputCD', 'Zone 3 Input CD', 'Z3CD', None),
('Z3InputTuner', 'Zone 3 Input Tuner', 'Z3TUNER', None),
('Z3InputDVD', 'Zone 3 Input DVD', 'Z3DVD', None),
('Z3InputVDP', 'Zone 3 Input VDP', 'Z3VDP', None),
('Z3InputTV', 'Zone 3 Input TV', 'Z3TV', None),
('Z3InputDBS', 'Zone 3 Input DBS', 'Z3DBS', None),
('Z3InputVCR1', 'Zone 3 Input VCR-1', 'Z3VCR-1', None),
('Z3InputVCR3', 'Zone 3 Input VCR-3', 'Z3VCR-3', None),
('Z3InputVCR3', 'Zone 3 Input VCR-3', 'Z3VCR-3', None),
('Z3InputCDR', 'Zone 3 Input CDR/TAPE', 'Z3CDR/TAPE', None),

(None,None,None,None),
)

class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        self.plugin.serial.write(self.cmd + chr(13))



class ValueAction(eg.ActionWithStringParameter):
    """Base class for all actions with adjustable argument"""

    def __call__(self, data):
        self.plugin.serial.write(self.cmd + str(data) + chr(13))



class MasterFade(eg.ActionWithStringParameter):
    name = "Fade MasterVol To"
    description = "Fade MasterVol To (actual dB value)"

    fadeLock = thread.allocate_lock()

    def __call__(self, data):
        thread.start_new_thread(self.FadeFunc, (data,))


    def FadeFunc(self, data):
        destVol = float(data)
        self.fadeLock.acquire()
        cv = self.plugin.currentVolume
        if destVol > cv:
            steps = (destVol - cv) * 2
            while steps > 0:
                self.plugin.serial.write("MVUP\r")
                time.sleep(0.15)
                steps -= 1
        elif cv > destVol:
            steps = (cv - destVol) * 2
            while steps > 0:
                self.plugin.serial.write("MVDOWN\r")
                time.sleep(0.15)
                steps -= 1
        self.fadeLock.release()



class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'

    def __call__(self, data):
        self.plugin.serial.write(str(data) + chr(13))





class DenonSerial(eg.PluginClass):

    def __init__(self):
        self.serial = None
        group = self

        for cmd_name, cmd_text, cmd_cmd, cmd_rangespec in cmdList:
            if cmd_text is None:
                # New subgroup, or back up
                if cmd_name is None:
                    group = self
                else:
                    group = self.AddGroup(cmd_name)
                    # Special hack for the FadeTo action
                    if cmd_name == 'Volume':
                        group.AddAction(MasterFade)
            elif cmd_rangespec is not None:
                # Command with argument
                actionName, paramDescr = cmd_text.split("(")
                actionName = actionName.strip()
                paramDescr = paramDescr[:-1]
                minValue, maxValue = cmd_rangespec.split("-")

                class Action(ValueAction):
                    name = actionName
                    cmd = cmd_cmd
                    parameterDescription = "Value: (%s)" % paramDescr
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


    # Serial port reader
    def reader(self):
        line = ""
        parmre = re.compile('(.+?)([0-9]{2,3})$')
        while self.readerkiller is False:
            ch = self.serial.read()
            if ch == '\r':
                m = parmre.match(line)
                if m is not None:
                    line = m.group(1).rstrip() + '.' + m.group(2)
                line = line.replace(':', '.')
                self.TriggerEvent(line)
                # Is it the master volume spec?
                if m is not None and m.group(1) == "MV":
                    if len(m.group(2)) == 3:
                        self.currentVolume = float(m.group(2)) / 10
                    else:
                        self.currentVolume = float(m.group(2))
                    if self.currentVolume == 99:
                        self.currentVolume = -80.5
                    else:
                        self.currentVolume -= 80
#                    self.TriggerEvent("CurrentVol "+str(self.currentVolume));
                line = ""
            else:
                line += ch


    def __start__(self, port):
        try:
            self.serial = eg.SerialPort(port)
        except:
            raise eg.Exception("Can't open serial port.")
        self.serial.baudrate = 9600
        self.serial.timeout = 30.0
        self.serial.setDTR(1)
        self.serial.setRTS(1)
        self.readerkiller = False
        thread.start_new_thread(self.reader, ());
        # Do an initial master volume query so we can track it
        self.serial.write("MV?\r")


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


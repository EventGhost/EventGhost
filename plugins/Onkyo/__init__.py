#
# OnkyoSerial
# ================
# Modified version of Denon Plugin originaly vritten by
# Oliver Wagner, <owagner@hometheatersoftware.com>
# Public Domain
#
#
# Revision history:
# -----------------
# 0.1 - initial
# 

help = """\
Small plugin to control Onkyo AVR via RS-232.
Developed for TX-SR804, but should work with 
different Onkyo AV recivers.

Replies from the AVR are turned into events. Description of
commands and their replies can be found in the document
Integra Serial Communication Protocol for AV Reciver v 1.07

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
"""
 
eg.RegisterPlugin(
    name = "Onkyo AV Serial",
    author = "prostetnic",
    version = "0.1." + "$LastChangedRevision: 348 $".split()[1],
    kind = "external",
    description = "Control Onkyo A/V Receivers via RS232",
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
	('Power', None, None, None),
		('PowerOn', 'Power On', 'PWR01', None),
		('PowerOff', 'Power Standby', 'PWR00', None),
		('SleepSett', 'Set sleep time (0-5A, 1-90 in Hex, )', 'SLP', '01-5A'),
		('SleepOff', 'Sleep time off', 'SLPOFF', None),
		('Sleep', 'Sleep timer toggle', 'SLPUP', None),
	('Volume', None, None, None),
		('MasterUp', 'Master Volume Up', 'MVLUP', None),
		('MasterDown', 'Master Volume Down', 'MVLDOWN', None),
		('MasterSet', 'Set Master Volume (0-64, 0-100 in Hex, 0=---/MIN)', 'MVL', '0-64'),
		('MuteOn', 'Mute On', 'AMT01', None),
		('MuteOff', 'Mute Off', 'AMT00', None),
		('MuteToggle', 'Mute Toggle', 'AMTTG', None),
	('VDF Dimmer' , None, None ,None),
		('VdfDimBright', 'VDF Display Bright and Volume LED On', 'DIM00', None),
		('VdfDimBrightLedOff', 'VDF Display Bright and Volume LED Off', 'DIM08', None),
		('VdfDimDim', 'VDF Display Dim', 'DIM01', None),
		('VdfDimDark', 'VDF Display Dark', 'DIM02', None),
		('VdfDimOff', 'VDF Display Off', 'DIM02', None),
		('VdfDimToggle', 'VDF Display Off', 'DIMDIM', None),
	('Input select', None, None, None),
		('InputVCR1', 'Input Video1', 'SLI00', None),
		('InputVCR2', 'Input Video2', 'SLI01', None),
		('InputVCR3', 'Input Video3', 'SLI02', None),
		('InputCDR', 'Input Video4', 'SLI03', None),
		('InputDVD', 'Input DVD', 'SLI10', None),
		('InputCD', 'Input CD', 'SLI23', None),
		('InputPhono', 'Input Phono', 'SLI22', None),
		('InputTuner', 'Input Tuner', 'SLI26', None),
		('InputFM', 'Input FM', 'SLI24', None),
		('InputAM', 'Input AM', 'SLI25', None),
		('InputMultiCH', 'Input Multi Ch', 'SLI30', None),
		('InputNext', 'Next Input', 'SLIUP', None),
		('InputPrev', 'Prevoius Input', 'SLIDOWN', None),
	('Listening Modes', None, None, None),
		('LMDirect','Direct, passthrough mode','LMD01', None),
		('LMStereo','Stereo','LMD00', None),
		('LMPureAudio','Pure Audio','LMD11', None),
		('LMSurround','Surround Mode','LMD02', None),
		('LMTHX','THX','LMD04', None),
		('LMMonoMovie','Mono Movie','LMD07', None),
		('LMOrchestra','Orchestra','LMD08', None),
		('LMUnplugged','Unplugged','LMD09', None),
		('LMStudioMix','Studio-mix mode','LMD0A', None),
		('LMTvLogic','TV Logic','LMD0B', None),
		('LMAllChStereo','All Ch Stereo','LMD0C', None),
		('LMMono','Mono','LMD0F', None),
		('LMDFullMono','Full Mono','LMD13', None),
		('LMDSurround51ch','5.1ch Surround','LMD40', None),
		('LMDDolbyEX','Dolby EX/DTS ES','LMD41', None),
		('LMDTHXCinema','THX Cinema','LMD42', None),
		('LMDTHXSurroundEX','THX Surround EX','LMD43', None),
		('LMCinema2','U2/S2 Cinema/Cinema2','LMD50', None),
		('LMMusicMode','Music Mode','LMD51', None),
		('LMGamesMode','Games Mode','LMD52', None),
		('LMPLIIMovie','PLII/PLIIx Movie','LMD80', None),
		('LMPLIIMusic','PLII/PLIIx Music','LMD81', None),
		('LMNeo6Cinema','Neo:6 Cinema','LMD82', None),
		('LMNeo6Music','Neo:6 Music','LMD83', None),
		('LMPLIITHXCinema','PLII/PLIIx THX Cinema','LMD84', None),
		('LMNeo6THXCinema','Neo:6 THX Cinema','LMD85', None),
		('LMPLIIGame','PLII/PLIIx Game','LMD86', None),
	('Parameters', None, None, None),
		('LateNightOff', 'Late Night Mode Off', 'LTN00', None),
		('LateNightLow', 'Late Night Mode Low', 'LTN01', None),
		('LateNightHigh', 'Late Night Mode High', 'LTN02', None),
		('ReEqOff', 'Re-EQ Off', 'RAS00', None),
		('ReEqOn', 'Re-EQ On', 'RAS01', None),
	('Tuner', None, None, None),
 
	('Zone 2', None, None, None),
		('Z2PowerOn', 'Zone 2 Power On', 'ZPW01', None),
		('Z2PowerOff', 'Zone 2 Power Standby', 'ZPW00', None),
		('Z2VolumeUp', 'Zone 2 Volume Up', 'ZVLUP', None),
		('Z2VolumeDown', 'Zone 2 Volume Down', 'ZVLDOWN', None),
		('Z2VolumeSet', 'Set Zone 2 Volume (0-64, 0-100 in Hex, 0=---/MIN)', 'ZLV', '0-64'),
		('Z2MuteOn', 'Mute On', 'ZMT01', None),
		('Z2MuteOff', 'Mute Off', 'ZMT00', None),
		('Z2InputVCR1', 'Input Video1', 'SLZ00', None),
		('Z2InputVCR2', 'Input Video2', 'SLZ01', None),
		('Z2InputVCR3', 'Input Video3', 'SLZ02', None),
		('Z2InputCDR', 'Input Video4', 'SLZ03', None),
		('Z2InputDVD', 'Input DVD', 'SLZ10', None),
		('Z2InputCD', 'Input CD', 'SLZ23', None),
		('Z2InputPhono', 'Input Phono', 'SLZ22', None),
		('Z2InputTuner', 'Input Tuner', 'SLZ26', None),
		('Z2InputFM', 'Input FM', 'SLZ24', None),
		('Z2InputAM', 'Input AM', 'SLZ25', None),
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
                self.plugin.serial.write("!1MVLUP\r")
                time.sleep(0.15)
                steps -= 1
        elif cv > destVol:
            steps = (cv - destVol) * 2
            while steps > 0:
                self.plugin.serial.write("!1MVLDOWN\r")
                time.sleep(0.15)
                steps -= 1
        self.fadeLock.release()
        
        
        
class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'
    
    def __call__(self, data):
        self.plugin.serial.write("!1" + str(data) + chr(13))
		



        
class OnkyoSerial(eg.PluginClass):

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
            elif cmd_rangespec is not None:
                # Command with argument
                actionName, paramDescr = cmd_text.split("(")
                actionName = actionName.strip()
                paramDescr = paramDescr[:-1]
                minValue, maxValue = cmd_rangespec.split("-")
                
                class Action(ValueAction):
                    name = actionName
                    cmd = "!1" + cmd_cmd
                    parameterDescription = "Value: (%s)" % paramDescr
                Action.__name__ = cmd_name
                group.AddAction(Action)
            else:
                # Argumentless command
                class Action(CmdAction):
                    name = cmd_text
                    cmd ="!1" + cmd_cmd
                Action.__name__ = cmd_name
                group.AddAction(Action)
                
        group.AddAction(Raw)


    # Serial port reader
 # debug   def reader(self):
 # debug       line = ""
 # debug       parmre = re.compile('(.+?)([0-9]{2,3})$')
 # debug       while self.readerkiller is False:
 # debug           ch = self.serial.read()
 # debug           if ch == '\r':
 # debug               m = parmre.match(line)
 # debug               if m is not None:
 # debug        		line = m.group(1).rstrip() + '.' + m.group(2)
 # debug               	line = line.replace(':', '.')
 # debug               	self.TriggerEvent(line)
                # Is it the master volume spec?
 # debug               if m is not None and m.group(1) == "MVL":
 # debug                   if len(m.group(2)) == 3:
 # debug                       self.currentVolume = float(m.group(2)) / 10
 # debug                   else:
 # debug                       self.currentVolume = float(m.group(2))
 # debug                   if self.currentVolume == 99:
 # debug                       self.currentVolume = -80.5
 # debug                   else:
 # debug                       self.currentVolume -= 80
 #                    self.TriggerEvent("CurrentVol "+str(self.currentVolume));
 # debug               line = ""
 # debug            else:
 # debug               line += ch
 
 # Serial port reader
    def reader(self):
        line=""
        while self.readerkiller is False:
            ch=self.serial.read()
            if ch=='\n':				
                continue;
            if ch=='\r':
                if line != "":
                    self.TriggerEvent(line)
                    line=""
            else:
                line+=ch

				
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
        # debug self.serial.write("!1MVLQSTN\r")
        
        
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
                    

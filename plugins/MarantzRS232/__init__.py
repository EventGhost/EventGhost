# -*- coding: utf-8 -*-

import eg

eg.RegisterPlugin(
    name="Marantz RS232",
    author="VJ",
    version="1.0." + "$LastChangedRevision: 1093 $".split()[1],
    kind="external",
    guid="{EDEAC623-F109-45A6-9733-D5CE336CAB1F}",
    url="http://www.eventghost.net/forum/viewtopic.php?t=747",
    description=('This plugin allows you to control your <a href="http://www.marantz.com">Marantz</a> \
                    SR-series receiver through it\'s serial port.\n\n\
                    <p>The plugin can send the commands directly to the serial port as well as to \
                    the <a href="http://daniel.vvtp.tudelft.nl/marantzcontrol/">MarantzControl</a> application.</p>\n\
                    <p>The plugin has been confirmed to work with at least one USB-RS232 adapter (Delock).</p>\
                    <br><br>\
                    <p><b>Notes:</b></p>\
                    <p>Modified from the original MarantzSerial plugin supplied by Dexter</p>\
                    <br>\
					<p>The code of the plugin is still similar to the original MarantzSerial plugin, but the commands are not compatible.\
                    Most actions and statuses have been added, using this <a href="http://us.marantz.com/us/Products/Pages/ProductDetails.aspx?Catid=AVReceivers&SubCatId=0&ProductId=SR6003">Marantz RS232 reference</a>.\
                    Some commands contain annotations in the description, mainly if the command is different for an SR6001.</p>\
                    <br>\
                    <p>The plugin does not process events coming from the Marantz.</p>\
					<br>\
                    <p>Not all commands were tested yet. Take precautions when testing, and verify the actions first: e.g. test commands that set values directly (e.g. volume) without anything playing to avoid too loud settings.</p>\
					<br>\
                    <p><b>Error messages:</b></p>\
                    <p><i>Unable to open serial port</i><br>The serial port could not be opened. Make sure the port is not used by another application.</p>\
                    <p><i>No response</i><br>The command was sent succesfully, but no response was received. Check if the serial cable is connected, \
                    if the correct serial port is selected and if the receiver is switched on.</p>\
                    <p><i>Bad response</i><br>An incorrect response was received. Make sure you connect to a Marantz SR-series receiver.</p>\
                    <p><i>Command not available in this mode</i><br>The command is not supported by this method (via MarantzSerial or directly to serial port.</p>\
                    <p><i>MarantzSerial application not found</i><br>The MarantzSerial application was not found. Make sure the application is started.</p>\
                    <p><i>Unable to send command to MarantzSerial</i><br>The MarantzSerial application is located, but an error occured while sending a message.</p>'),
)

import new
# Now we import some other things we will need later
import time
import wx
from ctypes import WinDLL
from ctypes.wintypes import ATOM, LPCSTR

from win32con import SMTO_ABORTIFHUNG, SMTO_BLOCK, WM_APP
from win32gui import FindWindow, GetWindowText, SendMessageTimeout

# Export GlobalAddAtom function
_kernel32 = WinDLL("kernel32")
GlobalAddAtomA = _kernel32.GlobalAddAtomA
GlobalAddAtomA.restype = ATOM
GlobalAddAtomA.argtypes = [LPCSTR]
GlobalAddAtom = GlobalAddAtomA  # alias

# Define commands
# (name, title, description (same as title if None), command)
commandsList = (
    ('Power',
     (('PowerToggle', 'Power toggle', None, '/power toggle', '@PWR:0'),
      ('PowerOff', 'Power off', None, '/power off', '@PWR:1'),
      ('PowerOn', 'Power on', None, '/power on', '@PWR:2')
      )),

    ('Audio ATT',
     (('AudioATTToggle', 'Audio attenuation (ATT) toggle', 'Toggles audio attenuation (ATT)', None, '@ATT:0'),
      ('AudioATTOff', 'Audio attenuation (ATT) off', 'Sets the audio attenuation (ATT) off', None, '@ATT:1'),
      ('AudioATTOn', 'Audio attenuation (ATT) on', 'Sets the audio attenuation (ATT) on', None, '@ATT:2')
      )),

    ('Audio Mute',
     (('AudioMuteToggle', 'Audio Mute toggle', None, '/mute toggle', '@AMT:0'),
      ('AudioMuteOff', 'Audio Mute off', None, '/mute off', '@AMT:1'),
      ('AudioMuteOn', 'Audio Mute on', None, '/mute on', '@AMT:2')
      )),

    ('Video Mute',
     (('VideoMuteToggle', 'Video Mute toggle', None, None, '@VMT:0'),
      ('VideoMuteOff', 'Video Mute off', None, None, '@VMT:1'),
      ('VideoMuteOn', 'Video Mute on', None, None, '@VMT:2')
      )),

    ('Main Volume',
     (('VolumeUp', 'Main volume up', None, None, '@VOL:1'),
      ('VolumeDown', 'Main volume down', None, None, '@VOL:2'),
      ('VolumeUpFast', 'Main volume up fast', None, None, '@VOL:3'),
      ('VolumeDownFast', 'Main volume down fast', None, None, '@VOL:4')
      )),

    ('Tone Bass',
     (('ToneBassUp', 'Tone Bass up', None, None, '@TOB:1'),
      ('ToneBassDown', 'Tone Bass down', None, None, '@TOB:2')
      )),

    ('Tone Trebble',
     (('ToneTrebbleUp', 'Tone Trebble up', None, None, '@TOT:1'),
      ('ToneTrebbleDown', 'Tone Trebble down', None, None, '@TOT:2')
      )),

    ('Main Source Select',
     (('SourceTV', 'Select TV source', None, '/input tv', '@SRC:1'),
      ('SourceDVD', 'Select DVD source', None, '/input dvd', '@SRC:2'),
      ('SourceVCR1', 'Select VCR1 source', None, '/input vcr1', '@SRC:3'),
      ('SourceVCR2', 'Select VCR2 source', 'not on SR6001', '/input vcr2', '@SRC:4'),
      ('SourceDSS', 'Select DSS source', None, '/input dss', '@SRC:5'),
      ('SourceLD', 'Select LD source', 'not on SR6001', '/input ld', '@SRC:6'),
      ('SourceNetUSB', 'Select Network/USB source', 'not on SR6001', '/input netusb', '@SRC:8'),
      ('SourceAux1', 'Select Aux 1 source', None, '/input aux1', '@SRC:9'),
      ('SourceAux2', 'Select Aux 2 source', None, '/input aux2', '@SRC:A'),
      ('SourceCD', 'Select CD source', 'not on SR6001', '/input cd', '@SRC:B'),
      ('SourceCDR', 'Select CD-R source', None, '/input cdr', '@SRC:C'),
      ('SourceTape', 'Select Tape source', 'not on SR6001', '/input tape', '@SRC:D'),
      ('SourceTuner1', 'Select Tuner 1 source', 'tape on SR6001', '/input tuner1', '@SRC:E'),
      ('SourceTuner1FM', 'Select Tuner 1 FM source', 'tuner on SR6001', '/input tuner1fm', '@SRC:F'),
      ('SourceTuner1AM', 'Select Tuner 1 AM source', 'fm on SR6001', '/input tuner1am', '@SRC:G'),
      ('SourceTuner2', 'Select Tuner 2 source', 'am on SR6001', '/input tuner2', '@SRC:H'),
      ('SourceTuner2FM', 'Select Tuner 2 FM source', 'not on SR6001', '/input tuner2fm', '@SRC:I'),
      ('SourceTuner2AM', 'Select Tuner 2 AM source', 'not on SR6001', '/input tuner2am', '@SRC:J'),
      ('SourceSirius', 'Select Sirius source', 'not on SR6001', '/input sirius', '@SRC:K'),
      ('SourcePhono', 'Select Phono source', 'not on SR6001', '/input phono', '@SRC:L')
      )),

    ('IPconverter',
     (('IpConverterOff', 'I/P converter off', None, None, '@IPC:1'),
      ('IpConverterOn', 'I/P converter on', None, None, '@IPC:2')
      )),

    ('7.1 Channel Input',
     (('InputChannel71Toggle', '7.1 channel input toggle', 'Toggles the 7.1 channel input', None, '@71C:0'),
      ('InputChannel71Off', '7.1 channel input off', 'Sets the 7.1 channel input off', None, '@71C:1'),
      ('InputChannel71On', '7.1 channel input on', 'Sets the 7.1 channel input on', None, '@71C:2')
      )),

    ('Input A/D Select',
     (('InputADAuto', 'Input A/D auto', None, '/inputmode auto', '@INP:0'),
      ('InputADAnalog', 'Input A/D analog', None, '/inputmode analog', '@INP:1'),
      ('InputADDigital', 'Input A/D digital', None, '/inputmode digital', '@INP:2'),
      ('InputAD-', 'Input A/D iLink', 'HDMI on sr6001', None, '@INP:3'),
      ('InputADHDMI', 'Input A/D HDMI', 'not on SR6001', None, '@INP:4'),
      ('InputADSelect', 'Input A/D Select', 'same as RC', None, '@INP:F')
      )),

    ('Speaker select',
     (('SpeakerAOff', 'Speaker A off', 'Switches Speaker A off', None, '@SPK:1'),
      ('SpeakerAOn', 'Speaker A on', 'Switches Speaker A on', None, '@SPK:2'),
      ('SpeakerBOff', 'Speaker B off', 'Switches Speaker B off', None, '@SPK:3'),
      ('SpeakerBOn', 'Speaker B on', 'Switches Speaker B on', None, '@SPK:4')
      )),

    ('Display',
     (('DisplaySelect', 'Changes display mode', 'same as RC', None, '@DIP:0'),
      ('DisplayMode1', 'Display Mode 1 (source)', 'display source', None, '@DIP:1'),
      ('DisplayMode2', 'Display Mode 2 (a/d)', 'display input a/d', None, '@DIP:2'),
      ('DisplayMode3', 'Display Mode 3 (surround)', 'display surround mode', None, '@DIP:3'),
      ('DisplayMode4', 'Display Mode 4 (auto off)', 'display auto off', None, '@DIP:4'),
      ('DisplayMode5', 'Display Mode 5 (off)', 'display off', None, '@DIP:5')
      )),

    ('OSD',
     (('OSDToggle', 'OSD toggle', None, None, '@OSD:0'),
      ('OSDOff', 'OSD off', None, None, '@OSD:1'),
      ('OSDOn', 'OSD on', None, None, '@OSD:2')
      )),

    ('Menu',
     (('MenuToggle', 'Menu toggle', None, None, '@MNU:0'),
      ('MenuOff', 'Menu off', None, None, '@MNU:1'),
      ('MenuOn', 'Menu on', None, None, '@MNU:2'),
      ('MenuEnter', 'Menu enter', None, None, '@MNU:3'),
      ('MenuTop', 'Menu Top', 'not on SR6001', None, '@MNU:4'),
      )),

    ('Cursor',
     (('Cursor', 'Cursor ?', 'no function', None, '@CUR:0'),
      ('CursorUp', 'Cursor up', None, None, '@CUR:1'),
      ('CursorDown', 'Cursor down', None, None, '@CUR:2'),
      ('CursorLeft', 'Cursor left', None, None, '@CUR:3'),
      ('CursorRight', 'Cursor right', None, None, '@CUR:4')
      )),

    ('DCTrigger',
     (('DCTrigger1off', 'DC Trigger 1 off', None, None, '@DCT:11'),
      ('DCTrigger1on', 'DC Trigger 1 on', None, None, '@DCT:12'),
      ('DCTrigger2off', 'DC Trigger 2 off', 'not on SR6001', None, '@DCT:21'),
      ('DCTrigger2on', 'DC Trigger 2 on', 'not on SR6001', None, '@DCT:22'),
      ('DCTrigger3off', 'DC Trigger 3 off', 'not on SR6001', None, '@DCT:31'),
      ('DCTrigger3on', 'DC Trigger 3 on', 'not on SR6001', None, '@DCT:32'),
      ('DCTrigger4off', 'DC Trigger 4 off', 'not on SR6001', None, '@DCT:41'),
      ('DCTrigger4on', 'DC Trigger 4 on', 'not on SR6001', None, '@DCT:42')
      )),

    ('FrontKeyLock',
     (('FrontKeyLockToggle', 'Front key lock toggle', 'same as RC', None, '@FKL:0'),
      ('FrontKeyLockOff', 'Front key lock off', None, None, '@FKL:1'),
      ('FrontKeyLockOn', 'Front key lock on', None, None, '@FKL:2')
      )),

    ('Simple Setup',
     (('SimpleSetupToggle', 'Simple Setup toggle', 'same as RC', None, '@SSU:0'),
      ('SimpleSetupOff', 'Simple Setup off', None, None, '@SSU:1'),
      ('SimpleSetupOn', 'Simple Setup on', None, None, '@SSU:2'),
      ('SimpleSetupEnter', 'Simple Setup enter', None, None, '@SSU:3')
      )),

    ('Surround mode',
     (('SurroundAuto', 'Select Auto surround mode', None, '/surround auto', '@SUR:00'),
      ('SurroundStereo', 'Select Stereo surround mode', None, '/surround stereo', '@SUR:01'),
      ('SurroundDolby', 'Select Dolby surround mode', None, '/surround dolby', '@SUR:02'),
      ('SurroundDolbyProLogic2xMovie', 'Select Dolby ProLogic II(x) Movie surround mode', None, '/surround dpl2xmv',
       '@SUR:03'),
      ('SurroundDolbyProLogic2Movie', 'Select Dolby ProLogic II Movie surround mode', 'not on SR6001',
       '/surround dpl2mv', '@SUR:04'),
      ('SurroundDolbyProLogic2xMusic', 'Select Dolby ProLogic II(x) Music surround mode', None, '/surround dpl2xms',
       '@SUR:05'),
      ('SurroundDolbyProLogic2Music', 'Select Dolby ProLogic II Music surround mode', 'not on SR6001',
       '/surround dpl2ms', '@SUR:06'),
      ('SurroundDolbyProLogic2xGame', 'Select Dolby ProLogic II(x) Game surround mode', None, '/surround dpl2xgm',
       '@SUR:07'),
      ('SurroundDolbyProLogic2Game', 'Select Dolby ProLogic II Game surround mode', 'not on SR6001', '/surround dpl2gm',
       '@SUR:08'),
      ('SurroundDolbyProLogic', 'Select Dolby ProLogic surround mode', None, '/surround dpl', '@SUR:09'),
      ('SurroundDolbyDigitalEx', 'Select Dolby Digital EX/ES surround mode', None, '/surround ddex', '@SUR:0A'),
      ('SurroundVirtual61', 'Select Virtual 6.1 surround mode', 'not on SR6001', '/surround virtual61', '@SUR:0B'),
      ('SurroundDTSES', 'Select DTS ES surround mode', None, '/surround dtses', '@SUR:0E'),
      ('SurroundDTSNeo6Cinema', 'Select DTS Neo6 Cinema surround mode', None, '/surround neo6cinema', '@SUR:0F'),
      ('SurroundDTSNeo6Music', 'Select DTS Neo6 Music surround mode', None, '/surround neo6music', '@SUR:0G'),
      ('SurroundMulti', 'Select Multi Channel Stereo surround mode', None, '/surround multi', '@SUR:0H'),
      ('SurroundCS2Cinema', 'Select CircleSurround II Cinema surround mode', None, '/surround cs2cinema', '@SUR:0I'),
      ('SurroundCS2Music', 'Select CircleSurround II Music surround mode', None, '/surround cs2music', '@SUR:0J'),
      ('SurroundCS2Mono', 'Select CircleSurround II Mono surround mode', None, '/surround cs2mono', '@SUR:0K'),
      ('SurroundVirtual', 'Select Virtual surround mode', None, '/surround virtual', '@SUR:0L'),
      ('SurroundDTS', 'Select DTS surround mode', None, '/surround dts', '@SUR:0M'),
      ('SurroundDolbyDigitalPL2Movie', 'Select DolbyDigital+ PLII x Movie surround mode', None, '/surround ddpl2mv',
       '@SUR:0O'),
      ('SurroundDolbyDigitalPL2Music', 'Select DolbyDigital+ PLII x Music surround mode', None, '/surround ddpl2ms',
       '@SUR:0P'),
      ('SurroundSourceDirect', 'Select Source Direct surround mode', None, '/surround sourcedirect', '@SUR:0T'),
      ('SurroundPureDirect', 'Select Pure Direct surround mode', None, '/surround puredirect', '@SUR:0U'),
      ('SurroundNext', 'Select next surround mode', None, '/surround next', '@SUR:1'),
      ('SurroundPrevious', 'Select previous surround mode', None, '/surround prev', '@SUR:2')
      )),

    ('RE-EQ(HT-EQ)',
     (('REEQToggle', 'RE-EQ(HT-EQ) toggle', None, None, '@REQ:0'),
      ('REEQOff', 'RE-EQ(HT-EQ) off', None, None, '@REQ:1'),
      ('REEQOn', 'RE-EQ(HT-EQ) on', None, None, '@REQ:2')
      )),

    ('Bilingual setting',
     (('Bilingual toggle', 'Bilingual toggle (same as RC)', None, None, '@BIL:0'),
      ('Bilingual main', 'Set to main', None, None, '@BIL:1'),
      ('Bilingual sub', 'Set to sub', None, None, '@BIL:1'),
      ('Bilingual main+sub', 'Set to main+sub', None, None, '@BIL:2')
      )),

    ('Equalizer mode',
     (('Off', 'Equalizer off', None, None, '@EQM:0'),
      ('Preset 1', 'Equalizer preset 1', None, None, '@EQM:1'),
      ('Preset 2', 'Equalizer preset 2', 'Not on SR6001', None, '@EQM:2'),
      ('Front curve', 'Front equalizer off', None, None, '@EQM:3'),
      ('Flat curve', 'Flat equalizer', None, None, '@EQM:4'),
      ('Audyssey curve', 'Audyssey curve', None, None, '@EQM:5'),
      ('Toggle', 'Toggle', None, None, '@EQM:6'),
      ('Next', 'Next curve', None, None, '@EQM:7'),
      ('Previous', 'Previous curve', None, None, '@EQM:8')
      )),

    ('Night mode',
     (('NightModeToggle', 'Nightmode toggle', 'Toggles night mode (dynamic range compression)', None, '@NGT:0'),
      ('NightModeOff', 'Nightmode off', 'Switches night mode (dynamic range compression) off', None, '@NGT:1'),
      ('NightModeOn', 'Nighmode on', 'Switches night mode (dynamic range compression) on', None, '@NGT:2')
      )),

    ('ChannelLevel',
     (('ChannelLevelFrontLeftUp', 'Level Front Left up', None, None, '@CHL:12'),
      ('ChannelLevelFrontLeftDown', 'Level Front Left Down', None, None, '@CHL:22'),
      ('ChannelLevelFrontRightUp', 'Level Front Right up', None, None, '@CHL:13'),
      ('ChannelLevelFrontRightDown', 'Level Front Right Down', None, None, '@CHL:23'),
      ('ChannelLevelCenterUp', 'Level Center up', None, None, '@CHL:14'),
      ('ChannelLevelCenterDown', 'Level Center Down', None, None, '@CHL:24'),
      ('ChannelLevelSurroundLeftUp', 'Level Surround Left up', None, None, '@CHL:16'),
      ('ChannelLevelSurroundLeftDown', 'Level Surround Left Down', None, None, '@CHL:26'),
      ('ChannelLevelSurroundRightUp', 'Level Surround Right up', None, None, '@CHL:17'),
      ('ChannelLevelSurroundRightDown', 'Level Surround Right Down', None, None, '@CHL:27'),
      ('ChannelLevelBackLeftUp', 'Level Back Left up', None, None, '@CHL:19'),
      ('ChannelLevelBackLeftDown', 'Level Back Left Down', None, None, '@CHL:29'),
      ('ChannelLevelBackRightUp', 'Level Back Right up', None, None, '@CHL:1A'),
      ('ChannelLevelBackRightDown', 'Level Back Right Down', None, None, '@CHL:2A'),
      ('ChannelLevelSubwooferUp', 'Level Subwoofer up', None, None, '@CHL:1B'),
      ('ChannelLevelSubwooferDown', 'Level Subwoofer Down', None, None, '@CHL:2B')
      )),

    ('Multi Room (zone A) Power',
     (('MultiRoomAToggle', 'Multiroom A toggle', 'Toggles multiroom output A', None, '@MPW:0'),
      ('MultiRoomAOff', 'Multiroom A off', 'Switches multiroom output A off', None, '@MPW:1'),
      ('MultiRoomAOn', 'Multiroom A on', 'Switches multiroom output A on', None, '@MPW:2')
      )),

    ('Multi Room (zone A) Audio mute',
     (('MultiRoomAAudioMuteToggle', 'Multiroom A mute toggle', 'Toggles audio mute for multiroom A', None, '@MAM:0'),
      ('MultiRoomAAudioMuteOff', 'Multiroom A mute off', 'Switches audio mute for multiroom A off', None, '@MAM:1'),
      ('MultiRoomAAudioMuteOn', 'Multiroom A mute on', 'Switches audio mute for multiroom A on', None, '@MAM:2')
      )),

    ('Multi Room (zone A) Volume',
     (('MultiRoomAVolumeUp', 'Multiroom A volume up', None, None, '@MVL:1'),
      ('MultiRoomAVolumeDown', 'Multiroom A volume down', None, None, '@MVL:2')
      )),

    ('Multi Room (zone A) Volume set',
     (('MultiRoomAVolumVariable', 'Multiroom A volume variable', None, None, '@MVS:1'),
      ('MultiRoomAVolumeFixed', 'Multiroom A volume fixed', None, None, '@MVS:2'),
      )),

    ('Select source Zone A',
     (('ZoneASourceTV', 'Zone A TV source', None, None, '@MSC:1'),
      ('ZoneASourceDVD', 'Zone A DVD source', None, None, '@MSC:2'),
      ('ZoneASourceVCR1', 'Zone A VCR1 source', None, None, '@MSC:3'),
      ('ZoneASourceVCR2', 'Zone A VCR2 source', 'not on SR6001', None, '@MSC:4'),
      ('ZoneASourceDSS', 'Zone A DSS source', None, None, '@MSC:5'),
      ('ZoneASourceLD', 'Zone A LD source', 'not on SR6001', None, '@MSC:6'),
      ('ZoneASourceNetUSB', 'Zone A Network/USB source', 'not on SR6001', None, '@MSC:8'),
      ('ZoneASourceAux1', 'Zone A Aux 1 source', None, None, '@MSC:9'),
      ('ZoneASourceAux2', 'Zone A Aux 2 source', None, None, '@MSC:A'),
      ('ZoneASourceCD', 'Zone A CD source', 'not on SR6001', None, '@MSC:B'),
      ('ZoneASourceCDR', 'Zone A CD-R source', None, None, '@MSC:C'),
      ('ZoneASourceTape', 'Zone A Tape source', 'not on SR6001', None, '@MSC:D'),
      ('ZoneASourceTuner1', 'Zone A Tuner 1 source', 'tape on SR6001', None, '@MSC:E'),
      ('ZoneASourceTuner1FM', 'Zone A Tuner 1 FM source', 'tuner on SR6001', None, '@MSC:F'),
      ('ZoneASourceTuner1AM', 'Zone A Tuner 1 AM source', 'fm on SR6001', None, '@MSC:G'),
      ('ZoneASourceTuner2', 'Zone A Tuner 2 source', 'am on SR6001', None, '@MSC:H'),
      ('ZoneASourceTuner2FM', 'Zone A Tuner 2 FM source', 'not on SR6001', None, '@MSC:I'),
      ('ZoneASourceTuner2AM', 'Zone A Tuner 2 AM source', 'not on SR6001', None, '@MSC:J'),
      ('ZoneASourceSirius', 'Zone A Sirius source', 'not on SR6001', None, '@MSC:K'),
      ('ZoneASourcePhono', 'Zone A Phono source', 'not on SR6001', None, '@MSC:L')
      )),

    ('Multi Room (zone A) Speaker',
     (('MultiRoomASpeakerToggle', 'Multi Room A speaker toggle', None, None, '@MSP:0'),
      ('MultiRoomASpeakerOff', 'Multi Room A speaker off', None, None, '@MSP:1'),
      ('MultiRoomASpeakerOn', 'Multi Room A speaker on', None, None, '@MSP:2')
      )),

    ('Multi Room (zone A) Speaker Audio mute',
     (('MultiRoomASpeakerAudioMuteToggle', 'Multi Room A speaker mute toggle', None, None, '@MSM:0'),
      ('MultiRoomASpeakerAudioMuteOff', 'Multi Room A speaker mute off', None, None, '@MSM:1'),
      ('MultiRoomASpeakerAudioMuteOn', 'Multi Room A speaker mute on', None, None, '@MSM:2')
      )),

    ('Multi Room (zone A) Speaker Volume',
     (('MultiRoomASpeakerVolumeUp', 'Multi Room A speaker volume up', None, None, '@MSV:1'),
      ('MultiRoomASpeakerVolumeDown', 'Multi Room A speaker volume down', None, None, '@MSV:2')
      )),

    ('Multi Room (zone A) Speaker Volume set',
     (('MultiRoomASpeakerVolumVariable', 'Multi Room A speaker volume variable', None, None, '@MSS:1'),
      ('MultiRoomASpeakerVolumeFixed', 'Multi Room A speaker volume fixed', None, None, '@MSS:2'),
      )),

    ('Multi Room (zone A) mono',
     (('MultiRoomAMonoToggle', 'Multiroom A mono toggle', 'Toggles multiroom output A between mono and stereo', None,
       '@MST:0'),
      ('MultiRoomAStereo', 'Multiroom A stereo', 'Switches multiroom output A to stereo', None, '@MST:1'),
      ('MultiRoomAMono', 'Multiroom A mono', 'Switches multiroom output A to mono', None, '@MST:2')
      )),
)

# Define statuses
# (name, title, description (same as title if None), command, dict with key (string) and values)
statusList = (
    ('GetPower', 'Get power status', None, 'PWR', dict([
        ('1', 'power off'),
        ('2', 'power on')])),
    ('GetAttenuation', 'Get attenuation status', None, 'ATT', dict([
        ('1', 'attenuation off'),
        ('2', 'attenuation on')])),
    ('GetAudioMute', 'Get audio mute status', None, 'AMT', dict([
        ('1', 'audio mute off'),
        ('2', 'audio mute on')])),
    ('GetVideoMute', 'Get video mute status', None, 'VMT', dict([
        ('1', 'video mute off'),
        ('2', 'video mute on')])),

    ('Get71ChannelInput', 'Get 7.1 channel input status', None, '71C', dict([
        ('1', '7.1 ch input off'),
        ('2', '7.1 ch input on')])),
    ('GetInputSignalAD', 'Get input signal', None, 'ISG', dict([
        ('1', 'analog'),
        ('2', 'digital'),
        ('3', 'iLink/HDMI'),
        ('4', 'HDMI'),
        ('5', 'auto - analog'),
        ('6', 'auto - digital/hdmi')])),
    ('GetDisplaymode', 'Get display mode', None, 'DIP', dict([
        ('1', 'source'),
        ('2', 'input a/d'),
        ('3', 'surround mode'),
        ('4', 'auto off'),
        ('5', 'off')])),

    ('GetIPconverter', 'Get I/P converter status', None, 'IPC', dict([
        ('1', 'I/P converter off'),
        ('2', 'I/P converter on'),
    ])),

    ('GetOSDmode', 'Get OSD status', None, 'OSD', dict([
        ('1', 'off'),
        ('2', 'on')])),

    ('GetMenuStatus', 'Get menu status', None, 'MNU', dict([
        ('1', 'not in menu'),
        ('2', 'in menu')])),
    ('GetSimpleSetupMenuStatus', 'Get simple setup menu status', None, 'SSU', dict([
        ('1', 'not in simple setup'),
        ('2', 'in simple setup')])),

    ('GetSurroundMode', 'Get current surround mode', None, 'SUR', dict([
        ('0', 'Auto'),
        ('1', 'Stereo'),
        ('2', 'Dolby'),
        ('3', 'Dolby ProLogic II(x) Movie'),
        ('4', 'Dolby ProLogic II Movie'),
        ('5', 'Dolby ProLogic II(x) Music'),
        ('6', 'Dolby ProLogic II Music'),
        ('7', 'Dolby ProLogic II(x) Game'),
        ('8', 'Dolby ProLogic II Game'),
        ('9', 'Dolby ProLogic'),
        ('A', 'Dolby Digital EX/ES'),
        ('B', 'Virtual 6.1'),
        ('E', 'DTS ES'),
        ('F', 'DTS Neo6 Cinema'),
        ('G', 'DTS Neo6 Music'),
        ('H', 'Multi Channel Stereo'),
        ('I', 'CircleSurround II Cinema'),
        ('J', 'CircleSurround II Music'),
        ('K', 'CircleSurround II Mono'),
        ('L', 'Virtual'),
        ('M', 'DTS'),
        ('O', 'DolbyDigital+ PLII x Movie'),
        ('P', 'DolbyDigital+ PLII x Music'),
        ('T', 'Source Direct'),
        ('U', 'Pure Direct')])),

    ('GetEqualizerMode', 'Get equalizer mode', None, 'EQM', dict([
        ('0', 'Equalizer off'),
        ('1', 'Equalizer preset 1'),
        ('2', 'Equalizer preset 2'),
        ('3', 'Front equalizer off'),
        ('4', 'Flat equalizer'),
        ('5', 'Audyssey curve')
    ])),

    ('GetNightMode', 'Get night mode (dynamic range compression) status', None, 'NGT', dict([
        ('1', 'Night mode off'),
        ('2', 'Night mode on')])),
    ('GetREEQ', 'Get RE-EQ (HT-EQ) status', None, 'REQ', dict([
        ('1', ' off'),
        ('2', 'OSD on')])),
    ('GetBilingualSetting', 'Get bilingual setting', None, 'BIL', dict([
        ('1', ' main'),
        ('2', 'sub'),
        ('3', 'main + sub')])),

    ('GetSamplingFrequency', 'Get digital input samply frequency', None, 'SFQ', dict([
        ('0', 'Out of range'),
        ('1', '32kHz'),
        ('2', '44.1kHz'),
        ('3', '48kHz'),
        ('4', '88.2kHz'),
        ('5', '96kHz'),
        ('6', '176.4kHz'),
        ('7', '192kHz'),
        ('F', 'input is not digital')])),

    ('GetMultiroomAPower', 'Get zone A power status', None, 'MPW', dict([
        ('1', 'power off'),
        ('2', 'power on')])),
    ('GetMultiroomAAudioMute', 'Get zone A audio mute status', None, 'MAM', dict([
        ('1', 'audio mute off'),
        ('2', 'audio mute on')])),
    ('GetMultiroomAVolumeset', 'Get zone A volume setting', None, 'MVS', dict([
        ('1', 'variable'),
        ('2', 'fixed')])),

    ('GetMultiroomASpeakerPower', 'Get zone A speaker power status', None, 'MSP', dict([
        ('1', 'power off'),
        ('2', 'power on')])),
    ('GetMultiroomASpeakerAudioMute', 'Get zone A speaker audio mute status', None, 'MSM', dict([
        ('1', 'audio mute off'),
        ('2', 'audio mute on')])),
    ('GetMultiroomASpeakerVolumeSet', 'Get zone A speaker volume setting', None, 'MSS', dict([
        ('1', 'variable'),
        ('2', 'fixed')])),

)

# Define statuses that return a value
# (name, title, description (same as title if None), command)
valueStatusList = (
    ('GetVolumeValue', 'Get volume', None, 'VOL'),
    ('GetToneBassValue', 'Get Tone bass', None, 'TOB'),
    ('GetToneTrebbleValue', 'Get Tone trebble', None, 'TOT'),
    ('GetLipSyncValue', 'Get lipsync delay (ms)', None, 'LIP'),
    ('GetMultiroomAVolumeValue', 'Get Multiroom A volume', None, 'MVL'),
    ('GetMultiroomASpeakersVolumeValue', 'Get Multiroom A speakers volume', None, 'MSV'),
)

# Define values that can be set
# (name, title, description (same as title if None), command, min value, max value, default)
valueSetList = (
    ('SetVolume', 'Sets the volume', 'final value between -80 and 18)', 'VOL', -70, 18, -71),
    ('SetToneBass', 'Set tone bass', 'final value between -6 and +6', 'TOB', -6, 6, 0),
    ('SetToneTrebble', 'Set tone trebble', 'final value between -6 and +6', 'TOT', -6, 6, 0),
    (
    'SetLipSyncValue', 'Set lip sync', 'final value between 0 and 20, in steps of 10ms: 1=10 ms, 2=20ms, ...', 'LIP', 0,
    20, 0),
    ('SetMultiroomAVolumeValue', 'Set Multiroom A volume', 'final value between 0 and 90', 'MVL', 0, 90, 0),
    ('SetMultiroomASpeakerVolumeValue', 'Set Multiroom A speaker volume', 'final value between 0 and 90', 'MSV', 0, 90,
     0),
)

# Define the channels status commands
# (name, title, description (same as title if None), bitpattern)
byteEncodedOnOff = dict([('1', 'Off'), ('2', 'On')])

channelStatusList = (
    ('Get1Status', 'Get channel 1 status', None, '0x80', byteEncodedOnOff),
    ('GetLFEStatus', 'Get LFE status', None, '0x40', byteEncodedOnOff),
    ('GetSurrLeftStatus', 'Get surround left status', None, '0x20', byteEncodedOnOff),
    ('GetSurrRightStatus', 'Get surround right statuts', None, '0x10', byteEncodedOnOff),
    ('GetSurrBackStatus', 'Get surround back status', None, '0x08', byteEncodedOnOff),
    ('GetFrontLeftStatus', 'Get front left status', None, '0x04', byteEncodedOnOff),
    ('GetFrontRightStatus', 'Get front right status', None, '0x02', byteEncodedOnOff),
    ('GetCenterStatus', 'Get center status', None, '0x01', byteEncodedOnOff)
)

# Define statuses that return a value that is byte encoded, additional parameter is which byte is requested
# (name, title, description (same as title if None), command)
byteEncodedSourcesSR6001 = dict([
    ('1', 'TV'),
    ('2', 'DVD'),
    ('3', 'VCR1'),
    ('4', 'VCR2'),
    ('5', 'DSS'),
    ('6', 'LD'),
    ('8', 'Network/USB'),
    ('9', 'AUX1'),
    ('A', 'AUX2'),
    ('B', 'CD'),
    ('C', 'CD-R'),
    ('E', 'Tape'),
    ('F', 'Tuner'),
    ('G', 'FM'),
    ('H', 'AM')
])

# Define byte encoded statuses
# (name, title, description (same as title if None), command, byte, text translation)
byteEncodedStatusList = (
    ('GetSourceCodeMainVideo', 'Get main video source', None, 'SRC', 0, byteEncodedSourcesSR6001),
    ('GetSourceCodeMainAudio', 'Get main audio source', None, 'SRC', 1, byteEncodedSourcesSR6001),
    ('GetSourceCodeZoneAVideo', 'Get zone A video source', None, 'MSC', 0, byteEncodedSourcesSR6001),
    ('GetSourceCodeZoneAAudio', 'Get zone A video source', None, 'MSC', 1, byteEncodedSourcesSR6001),
    ('GetSpeakersA', 'Get Speakers A status', None, 'SPK', 0, byteEncodedOnOff),
    ('GetSpeakersB', 'Get Speakers B status', None, 'SPK', 1, byteEncodedOnOff),
)


class MarantzRS232Action(eg.ActionClass):
    def __call__(self):
        self.plugin.SendCommand(self.appcmd, self.serialcmd)


class MarantzRS232StatusCode(eg.ActionClass):
    def __call__(self):
        return self.plugin.GetStatusCode(self.serialcmd)


class MarantzRS232StatusText(eg.ActionClass):
    def __call__(self):
        return self.statustext[self.plugin.GetStatusCode(self.serialcmd)]


class MarantzRS232ChannelStatusCode(eg.ActionClass):
    def __call__(self):
        return self.plugin.GetChannelStatusCode(self.bitspec)


class MarantzRS232ChannelStatusText(eg.ActionClass):
    def __call__(self):
        return self.statustext[self.plugin.GetChannelStatusCode(self.bitspec)]


class MarantzRS232ByteStatusCode(eg.ActionClass):
    def __call__(self):
        return self.plugin.GetByteStatusCode(self.serialcmd, self.bytespec)


class MarantzRS232ByteStatusText(eg.ActionClass):
    def __call__(self):
        return self.statustext[self.plugin.GetByteStatusCode(self.serialcmd, self.bytespec)]


class MarantzRS232SetValue(eg.ActionWithStringParameter):
    def __call__(self, value):
        return self.plugin.SetValue(self.relative, self.serialcmd, value, self.minvalue, self.maxvalue)

    def Configure(self, value=None, min=None, max=None):
        panel = eg.ConfigPanel(self)
        if self.relative:
            value = 0
        else:
            value = self.default
        valueCtrl = panel.SpinIntCtrl(value, min=self.minvalue, max=self.maxvalue)
        panel.AddLine(self.description + " to:", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class MarantzRS232SetVolumeAbsolute(eg.ActionWithStringParameter):
    name = 'Set absolute volume'
    description = 'Sets the absolute volume'

    def __call__(self, volume):
        return self.plugin.SetVolume(volume, False)

    def GetLabel(self, volume):
        return "Set Absolute Volume to %d" % volume

    def Configure(self, volume=-40):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(volume, min=-70, max=10)
        panel.AddLine("Set absolute volume to", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class MarantzRS232SetVolumeRelative(eg.ActionWithStringParameter):
    name = 'Set relative volume'
    description = 'Sets the relative volume'

    def __call__(self, volume):
        return self.plugin.SetVolume(volume, True)

    def GetLabel(self, volume):
        return "Set Relative Volume to %d" % volume

    def Configure(self, volume=0):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(volume, min=-100, max=100)
        panel.AddLine("Set relative volume to", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class MarantzRS232(eg.PluginClass):

    def __init__(self):
        self.serial = None
        self.response = None
        self.method = 0
        self.hwndMarantzControl = None

        # add the actions
        for groupname, list in commandsList:
            group = self.AddGroup(groupname)
            for classname, title, desc, app, serial in list:
                if desc is None:
                    desc = title
                clsAttributes = dict(name=title, description=desc, appcmd=app, serialcmd=serial)
                cls = new.classobj(classname, (MarantzRS232Action,), clsAttributes)
                group.AddAction(cls)

        group = self.AddGroup('Volume')
        group.AddAction(MarantzRS232SetVolumeAbsolute)
        group.AddAction(MarantzRS232SetVolumeRelative)

        # add the status commands that return a code
        group = self.AddGroup('Status')
        for classname, title, desc, serial, list in statusList:
            if desc is None:
                desc = title
            clsAttributes = dict(name=title + "-code", description=desc + " (code)", serialcmd=serial)
            cls = new.classobj(classname + "StatusCode", (MarantzRS232StatusCode,), clsAttributes)
            group.AddAction(cls)
            clsAttributes1 = dict(name=title + "-text", description=desc + " (text)", serialcmd=serial, statustext=list)
            cls1 = new.classobj(classname + "StatusText", (MarantzRS232StatusText,), clsAttributes1)
            group.AddAction(cls1)

        # add the status commands that return a value
        for classname, title, desc, serial in valueStatusList:
            if desc is None:
                desc = title
            clsAttributes = dict(name=title + "-value", description=desc + " (value)", serialcmd=serial)
            cls = new.classobj(classname + "Value", (MarantzRS232StatusCode,), clsAttributes)
            group.AddAction(cls)

        # status for the different output channels
        for classname, title, desc, channelspec, list in channelStatusList:
            if desc is None:
                desc = title
            clsAttributes = dict(name=title + "-code", description=desc + " (code)", bitspec=channelspec)
            cls = new.classobj(classname + "Code", (MarantzRS232ChannelStatusCode,), clsAttributes)
            group.AddAction(cls)
            clsAttributes1 = dict(name=title + "-text", description=desc + " (text)", bitspec=channelspec,
                                  statustext=list)
            cls1 = new.classobj(classname + "Text", (MarantzRS232ChannelStatusText,), clsAttributes1)
            group.AddAction(cls1)

        # status for the byte encoded statusses
        for classname, title, desc, serial, statusspec, list in byteEncodedStatusList:
            if desc is None:
                desc = title
            clsAttributes = dict(name=title + "-code", description=desc + " (code)", serialcmd=serial,
                                 bytespec=statusspec)
            cls = new.classobj(classname + "Code", (MarantzRS232ByteStatusCode,), clsAttributes)
            group.AddAction(cls)
            clsAttributes1 = dict(name=title + "-text", description=desc + " (text)", serialcmd=serial,
                                  bytespec=statusspec, statustext=list)
            cls1 = new.classobj(classname + "Text", (MarantzRS232ByteStatusText,), clsAttributes1)
            group.AddAction(cls1)

        # add the value setters
        group = self.AddGroup('Set values')
        for classname, title, desc, serial, minallowedvalue, maxallowedvalue, defaultvalue in valueSetList:
            if desc is None:
                desc = title
            clsAttributes = dict(name=title + "-abs", description=desc + " absolute", relative=False, serialcmd=serial,
                                 minvalue=minallowedvalue, maxvalue=maxallowedvalue, default=defaultvalue)
            cls = new.classobj(classname + "Absolute", (MarantzRS232SetValue,), clsAttributes)
            group.AddAction(cls)
            clsAttributes1 = dict(name=title + "-rel", description=desc + " relative", relative=True, serialcmd=serial,
                                  minvalue=minallowedvalue, maxvalue=maxallowedvalue, default=defaultvalue)
            cls1 = new.classobj(classname + "Relative", (MarantzRS232SetValue,), clsAttributes1)
            group.AddAction(cls1)

    def FindMarantzWindow(self):
        # Old handle still valid?
        if self.hwndMarantzControl is not None:
            if GetWindowText(self.hwndMarantzControl) == 'MarantzControl':
                return True

        # Search for window
        self.hwndMarantzControl = FindWindow(None, 'MarantzControl')
        if self.hwndMarantzControl != 0:
            return True

        # Nothing found
        return False

    def SendCommandApp(self, cmd):
        try:
            if self.FindMarantzWindow():
                hAtom = GlobalAddAtom(cmd)
                SendMessageTimeout(
                    self.hwndMarantzControl,
                    WM_APP + 102,
                    hAtom,
                    0,
                    SMTO_BLOCK | SMTO_ABORTIFHUNG,
                    500  # Wait at most 500ms
                )
                time.sleep(0.1)  # Wait 100ms for command to be processed by MarantzSerial
                return False

            else:
                self.PrintError("MarantzControl application not found")
                return True

        except:
            self.PrintError("Unable to send command to MarantzControl")
            return True

    def SendCommandSerial(self, cmd):
        if self.serial is None:
            return True

        # Send command
        cmd += '\r'
        self.serial.write(cmd)

        # Wait for response (if any)
        self.response = ""
        while True:

            # Wait for next char
            ch = self.serial.read(1)

            # Timeout occured?
            if ch == '':
                self.response = None
                self.PrintError("No response")
                return True

            # End-of-response?
            elif ch == '\r':
                break

            # Add received char
            self.response += ch

        # Seperator found?
        seppos = self.response.find(':')
        if seppos == -1:
            self.PrintError("Bad response")
            return True

        # Is this response a response on the sent command?
        seppos += 1  # (include ':')
        if cmd[0:seppos] != self.response[0:seppos]:
            self.PrintError("Bad response")
            return True

        # Strip anything before seperator and return ok
        self.response = self.response[seppos:].strip()
        return False

    def GetResponseInt(self):
        if (self.response[0] == '-' or self.response[0] == '+'):
            if not self.response[1:].isdigit():
                self.PrintError("Bad response")
                return None

        elif not self.response.isdigit():
            self.PrintError("Bad response")
            return None

        return int(self.response)

    def SendCommand(self, appcmd, serialcmd):
        if self.method == 0:
            if appcmd is None:
                self.PrintError("Command not available in this mode")
                return True
            result = self.SendCommandApp(appcmd)

        elif self.method == 1:
            if serialcmd is None:
                self.PrintError("Command not available in this mode")
                return True
            result = self.SendCommandSerial(serialcmd)

        return result

    def SetValue(self, relative, serialcmd, value, minvalue, maxvalue):
        if relative:
            if self.SendCommandSerial("@" + serialcmd + ":?"):
                return
            current = self.GetResponseInt()
            if current is None:
                return
            value += current

        if value > maxvalue:
            value = maxvalue
        elif value < minvalue:
            value = minvalue

        print "command @" + serialcmd + ":0%+.2d" % (value)
        self.SendCommandSerial("@" + serialcmd + ":0%+.2d" % (value))
        return value

    def SetVolume(self, volume, relative):
        if self.method == 0:
            if relative:
                self.SendCommandApp("/volume %d" % volume)

        elif self.method == 1:
            if relative:
                if self.SendCommandSerial("@VOL:?"):
                    return
                current = self.GetResponseInt()
                if current is None:
                    return
                volume += current

            if volume > 10:
                volume = 10
            elif volume < -70:
                volume = -70
            self.SendCommandSerial("@VOL:0%+.2d" % (volume))
            return volume

    def GetStatusCode(self, serialcmd):
        if self.method == 0:
            return;
        elif self.method == 1:
            if self.SendCommandSerial("@" + serialcmd + ":?"):
                return
            current = self.response
            print "command @" + serialcmd + ":? = " + current
            if current is None:
                return
            return current

    def GetByteStatusCode(self, serialcmd, bytenumber):
        if self.method == 0:
            return;
        elif self.method == 1:
            current = self.GetStatusCode(serialcmd)
            print "command @" + serialcmd + ":? = " + current + "  byte " + str(bytenumber) + " = " + current[
                bytenumber]
            if current is None:
                return
            return current[bytenumber]

    def GetChannelStatusCode(self, channelspec):
        if self.method == 0:
            return;
        elif self.method == 1:
            if self.SendCommandSerial("@CHS:?"):
                return
            print "command @CHS:? = " + self.response
            current = int(self.response, 16)
            if current is None:
                return
            elif current & int(channelspec, 16) == 0:
                return '1'
            return '2'

    def __start__(self, method=0, port=0):
        self.method = method
        if method == 1:
            try:
                self.serial = eg.SerialPort(port)
                self.serial.baudrate = 9600
                self.serial.timeout = 0.5
                self.serial.setDTR(1)
                self.serial.setRTS(1)
            except:
                self.PrintError("Unable to open serial port")

    def __stop__(self):
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    def Configure(self, method=0, port=0):
        methodCtrl = None
        portCtrl = None

        def OnMethodChange(self):
            if methodCtrl.GetValue() == 1:
                portCtrl.Enable()
            else:
                portCtrl.Disable()

        panel = eg.ConfigPanel(self)
        methodCtrl = panel.Choice(method, choices=("Via MarantzControl", "Directly to serial port"))
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Method:", methodCtrl)
        panel.AddLine("Port:", portCtrl)

        methodCtrl.Bind(wx.EVT_CHOICE, OnMethodChange)
        OnMethodChange(self)

        while panel.Affirmed():
            panel.SetResult(methodCtrl.GetValue(), portCtrl.GetValue())

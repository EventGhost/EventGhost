# -*- coding: utf-8 -*-

help = """\

The Plugin can set and get current status on all commands through the LG-TV:s serial port.
settings like Brightness and Volume uses real values like 1-100.

Every command generates an event with payload to be used in custom scripts:
LG.Contrast '90'    (eg.event.string = LG.Contrast and eg.event.payload = 90)

Settings like Inputs and Power have events and payload too:
LG.Power 'ON'	(eg.event.string = LG.Power and eg.event.payload = ON)

If some settings don't work it will result in an event with .error at the end
This can happend if the value is out of range or the setting don't exist on your TV.

If anyone adds something good or change something in the plugin plz send it to my mail or add it yourself
woggy81@gmail.com

"""

eg.RegisterPlugin(
    name = "LG TV Serial",
    guid = '{1BCFC2C1-BEC7-4DF9-928E-B154B2AA6F68}',
    author = u"Niclas H\xe5kansson",
    version = "1.5",
    kind = "external",
    description = "Control LG TV via RS232, LCD and Plasma",
    help = help,
    canMultiLoad = True,
    createMacrosOnAdd = True,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=3041",
    icon = (
	"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"

    ),
)



import thread
import time
import re

cmdList = (

('Raw Codes', None, None, None),
    ('ex: mc 01 02',        'Raw Code',                          '',               '0-100'),



('IR Codes', None, None, None),
    ('',                    'Custom IR Code',                           'mc 01 ',         '0-100'),
    ('CH +',                'CH up',                                     'mc 01 00',         None ),
    ('CH -',                'CH down',                                     'mc 01 01',         None ),
    ('VOL +',               'VOL up',                                    'mc 01 02',         None ),
    ('VOL -',               'VOL down',                                    'mc 01 03',         None ),
    ('',                    'Right',                                    'mc 01 06',         None ),
    ('',                    'Left',                                     'mc 01 07',         None ),
    ('',                    'Up',                                       'mc 01 40',         None ),
    ('',                    'Down',                                     'mc 01 41',         None ),
    ('',                    'On/Off',                                   'mc 01 08',         None ),
    ('',                    'Mute/Delete',                              'mc 01 09',         None ),
    ('',                    'Input',                                    'mc 01 0B',         None ),
    ('',                    'TV',                                       'mc 01 0F',         None ),
    ('',                    'Key 0',  	                                'mc 01 10',         None ),
    ('',                    'Key 1',                                    'mc 01 11',         None ),
    ('',                    'Key 2',                                    'mc 01 12',         None ),
    ('',                    'Key 3',                                    'mc 01 13',         None ),
    ('',                    'Key 4',                                    'mc 01 14',         None ),
    ('',                    'Key 5',                                    'mc 01 15',         None ),
    ('',                    'Key 6',                                    'mc 01 16',         None ),
    ('',                    'Key 7',                                    'mc 01 17',         None ),
    ('',                    'Key 8',                                    'mc 01 18',         None ),
    ('',                    'Key 9',                                    'mc 01 19',         None ),
    ('',                    'Flashbk',                                  'mc 01 1A',         None ),
    ('',                    'Fav/Mark',                                 'mc 01 1E',         None ),
    ('',                    'Back',                                     'mc 01 28',         None ),
    ('',                    'AV Mode',                                  'mc 01 30',         None ),
    ('',                    'Menu',                                     'mc 01 43',         None ),
    ('',                    'Enter',                                    'mc 01 44',         None ),
    ('',                    'Q Menu',                                   'mc 01 45',         None ),
    ('',                    'List',                                     'mc 01 4C',         None ),
    ('',                    'Exit',                                     'mc 01 5B',         None ),
    ('',                    'Widgets',                                  'mc 01 58',         None ),
    ('',                    'Netcast',                                  'mc 01 59',         None ),
    ('',                    'Blue, L/R Select',                         'mc 01 61',         None ),
    ('',                    'Yellow',                                   'mc 01 63',         None ),
    ('',                    'Green',                                    'mc 01 71',         None ),
    ('',                    'Red',                                      'mc 01 72',         None ),
    ('',                    'Ratio',                                    'mc 01 79',         None ),
    ('',                    'Simplink',                                 'mc 01 7E',         None ),
    ('',                    'Rew',                                      'mc 01 8F',         None ),
    ('',                    'Fwd',                                      'mc 01 8E',         None ),
    ('',                    'Energy Saving',                            'mc 01 95',         None ),
    ('',                    'Info',                                     'mc 01 AA',         None ),
    ('',                    'Play',                                     'mc 01 B0',         None ),
    ('',                    'Stop',                                     'mc 01 B1',         None ),
    ('',                    'Pause',                                    'mc 01 BA',         None ),
    ('',                    'TV',                                       'mc 01 D6',         None ),
    ('',                    'Power On',                                 'mc 01 C4',         None ),
    ('',                    'Power Off',                                'mc 01 C5',         None ),
    ('',                    'AV1',                                      'mc 01 5A',         None ),
    ('',                    'AV2',                                      'mc 01 D0',         None ),
    ('',                    'Component1',                               'mc 01 BF',         None ),
    ('',                    'Component2',                               'mc 01 D4',         None ),
    ('RGB-PC',              'RGB PC',                                   'mc 01 D5',         None ),
    ('',                    'HDMI1',                                    'mc 01 CE',         None ),
    ('',                    'HDMI2',                                    'mc 01 CC',         None ),
    ('',                    'HDMI3',                                    'mc 01 E9',         None ),
    ('',                    'HDMI4',                                    'mc 01 DA',         None ),
    ('Ratio 4:3',           'Ratio 43',                                 'mc 01 76',         None ),
    ('Ratio 16:9',          'Ratio 169',                                'mc 01 77',         None ),
    ('',                    'Ratio Zoom',                               'mc 01 AF',         None ),
    ('',                    'Key 3D',                                   'mc 01 DC',         None ),



('Power Settings', None, None, None),
    ('',                    'Power ON',                                 'ka 01 01',         None ),
    ('',                    'Power OFF',                                'ka 01 00',         None ),
    ('',                    'Power Status',                             'ka 01 FF',         None ),
    ('',                    'Energy Savings Off',                       'jq 00 00',         None ),
    ('',                    'Energy Savings Minimum',                   'jq 00 01',         None ),
    ('',                    'Energy Savings Medium',                    'jq 00 02',         None ),
    ('',                    'Energy Savings Maximum',                   'jq 00 03',         None ),
    ('',                    'Energy Savings Auto',                      'jq 00 04',         None ),
    ('',                    'Energy Savings Screen OFF',                'jq 00 05',         None ),
    ('',                    'Energy Savings Status',                    'jq 00 FF',         None ),

('Sound', None, None, None),
    ('0-100',               'Volume Set Value',                         'kf 01 ',           '0-100'),
    ('',                    'Volume Status',                            'kf 01 FF',         None ),
    ('',                    'Volume Upp',                               'mc 01 02',         None ),
    ('',                    'Volume Down',                              'mc 01 03',         None ),
    ('',                    'Volume Mute ON',                           'ke 01 00',         None ),
    ('',                    'Volume Mute OFF',                          'ke 01 01',         None ),
    ('',                    'Volume Mute Status',                       'ke 01 FF',         None ),
    ('0-100',               'Treble Set Value',                         'kr 00 ',           '0-100'),
    ('',                    'Treble Status',                            'kr 00 ff',         None ),
    ('0-100',               'Bass Set Value',                           'ks 00 ',           '0-100'),
    ('',                    'Bass Status',                              'ks 00 ff',         None ),        
    ('0-100',               'Balance Set Value',                        'kt 00 ',           '0-100'),
    ('',                    'Balance Status',                           'kt 00 ff',         None ),        


('Picture', None, None, None),
    ('0-100',               'Contrast Set Value',                       'kg 01 ',           '0-100'),
    ('',                    'Contrast Status',                          'kg 01 FF',         None),
    ('0-100',               'Brightness Set Value',                     'kh 01 ',           '0-100'),
    ('',                    'Brightness Status',                        'kh 01 FF',         None),
    ('0-100',               'Color Set Value',                          'ki 01 ',           '0-100'),
    ('',                    'Color Status',                             'ki 01 FF',         None),
    ('0-100',               'Sharpness Set Value',                      'kk 01 ',           '0-100'),
    ('',                    'Sharpness Status',                         'kk 01 FF',         None),
    ('0-100',               'Tint Set Value',                           'kj 01 ',           '0-100'),
    ('',                    'Tint Status',                              'kj 01 FF',         None),
    ('0-100',               'Color Tempeature Set Value',               'xu 01 ',           '0-100'),
    ('0-100',               'Set Color Tempeature 2',                   'ku 01 01',         None ),
    ('0-100',               'Set Color Tempeature 3',                   'ku 01 02',         None ),
    ('',                    'Color Temperature Status',                 'xu 01 ff',         None ),
    ('Only works with RGB PC',      'Auto Configuration',               'ju 01 01',         None ),



('Aspect Ratio', None, None, None),
    ('',                    'Aspect Ratio Status',                      'kc 01 FF',         None ),
    ('Aspect Ratio 4:4',    'Aspect Ratio 43',                          'kc 01 01',         None ),
    ('Aspect Ratio 16:9',   'Aspect Ratio 169',                         'kc 01 02',         None ),
    ('Aspect Ratio 14:9',   'Aspect Ratio 149',                         'kc 01 07',         None ),
    ('',                    'Aspect Ratio Zoom',                        'kc 01 04',         None ),
    ('',                    'Aspect Ratio Set by Program',              'kc 01 06',         None ),
    ('',                    'Aspect Ratio Just Scan ',                  'kc 01 09',         None ),
    ('',                    'Aspect Ratio Full Width',                  'kc 01 0b',         None ),
    ('1-16',                'Aspect Ratio Cinema Zoom Set Value',       'kc 01 ',           '10-16' ),


('Screen Mute', None, None, None),
    ('Video-out Mute OFF',  'Screen Mute OFF',                          'kd 01 00',         None ),
    ('',                    'Screen Mute ON',                           'kd 01 01',         None ),
    ('',                    'Screen Mute Status',                       'kd 01 FF',         None ),
    ('',                    'Screen Videoout Mute ON',                  'kd 01 10',         None ),


('Inputs', None, None, None),
    ('',                    'Input Status',                             'xb 01 FF',         None ),
    ('',                    'Input DTV Antenna',                        'xb 01 00',         None ),
    ('',                    'Input DTV Cable',                          'xb 01 01',         None ),
    ('',                    'Input Analog Antenna',                     'xb 01 10',         None ),
    ('',                    'Input Analog Cable',                       'xb 01 11',         None ),
    ('',                    'Input AV 1',                               'xb 01 20',         None ),
    ('',                    'Input AV 2',                               'xb 01 21',         None ),
    ('',                    'Input Component 1',                        'xb 01 40',         None ),
    ('',                    'Input Component 2',                        'xb 01 41',         None ),
    ('',                    'Input Component 3',                        'xb 01 42',         None ),
    ('VGA',                 'Input RGB PC',                             'xb 01 60',         None ),
    ('',                    'Input HDMI 1',                             'xb 01 90',         None ),
    ('',                    'Input HDMI 2',                             'xb 01 91',         None ),
    ('',                    'Input HDMI 3',                             'xb 01 92',         None ),
    ('',                    'Input HDMI 4',                             'xb 01 93',         None ),


('LCD Settings', None, None, None),
    ('0-100',               'Backlight Set Value',                      'mg 01 ',           '0-100'),
    ('',                    'Backlight Status',                         'mg 01 FF',         None ),


('Plasma Settings', None, None, None),
    ('',                    'Screen Saver Orbiter',                     'jp 00 02',         None ),
    ('',                    'Screen Saver Normal',                      'jp 00 08',         None ),
    ('',                    'Screen Saver White Wash',                  'jp 00 04',         None ),
    ('',                    'Screen Saver Color Wash',                  'jp 00 20',         None ),
    ('',                    'Screen Saver Status',                      'jp 00 FF',         None ),    
    ('',                    'Intelligent Sensor Low',                   'jq 00 10',         None ),
    ('',                    'Intelligent Sensor Medium',                'jq 00 11',         None ),
    ('',                    'Intelligent Sensor Maximum',               'jq 00 12',         None ),


('Remote Control Lock', None, None, None),
    ('',                    'Remote Lock On',                           'km 00 01',         None ),
    ('',                    'Remote Lock Off',                          'km 00 00',         None ),
    ('',                    'Remote Lock Status',                       'km 00 FF',         None ),

('OSD', None, None, None),
    ('',                    'OSD ON',                                   'kl 00 01',         None ),            
    ('',                    'OSD OFF',                                  'kl 00 00',         None ),        
    ('',                    'OSD Status',                               'kl 00 ff',         None ),

)

BAUDRATES = [
    '2400', '9600', '115200'
]  

class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        self.plugin.serial.write(self.cmd+chr(13))
        global Gname
        global Gcmd
        Gcmd = self.cmd
        Gname = str(self.name)
        time.sleep(0.07)

class ValueAction(eg.ActionWithStringParameter):
    """Base class for all actions with adjustable argument"""
    
    def __call__(self,data):
        if self.name == "Aspect Ratio Cinema Zoom Set Value":
            data2 = int(data) +15
            data2 = hex(int(data2))[2:]
            self.plugin.serial.write(self.cmd+str(data2)+chr(13))
        elif self.name == "Custom IR Code":
            self.plugin.serial.write(self.cmd+str(data)+chr(13))
        elif self.name == "Raw Code":
            self.plugin.serial.write(self.cmd+str(data)+chr(13))
        else:
            data2 = hex(int(data))[2:]
            self.plugin.serial.write(self.cmd+str(data2)+chr(13))
        global Gname
        global Gcmd
        global Gdata
        Gdata = data
        Gcmd = self.cmd
        Gname = str(self.name)
        time.sleep(0.07)
        
        
class LG(eg.PluginClass):
    def __init__(self):
        self.serial = None
        self.readerkiller = False
        group = topGroup = self
        for  cmd_text, cmd_name, cmd_cmd, cmd_rangespec in cmdList:
            if cmd_name is not None:
                line = str(cmd_name.replace(' ', ''))
            if cmd_name != "":
                test = str(cmd_text)
            if cmd_name == "":
                test = str(cmd_name)
            if cmd_name is None:
                # New subgroup, or back up
                if cmd_text is None:
                    group = topGroup
                else:
                    group = topGroup.AddGroup(cmd_text)
            elif cmd_rangespec is not None:
                # Command with argument
                class Action(ValueAction):
                    name = str(cmd_name)
                    description = test
                    cmd = cmd_cmd
                Action.__name__ = line
                group.AddAction(Action)
            else:
                # Argumentless command
                class Action(CmdAction):
                    name = str(cmd_name)
                    description = test
                    cmd = cmd_cmd
                Action.__name__ = line
                group.AddAction(Action)

    # Serial port reader
    def reader(self):
        line=""
        while self.readerkiller is False:
            ch=self.serial.read()
            if ch=='x':
                if line != "":
                    parts = line.split(" ")
                    status = parts[2][:2]
                    type = parts[0]
                    value = int(parts[2][2:4], 16)
                    line=""
                    hexval = hex(value)[2:]
                    eventname = ""
                    eventnamepayload = ""
                    statusname = "" 
                    groupname = ""
                 
                    if status == "NG":
                        statusname = ".Error"
                    if status == "OK":
                        statusname = ""
                    if type == "a":
                        if value == 1:
                            eventname = "ON"
                        if value == 0:
                            eventname = "OFF"
                        newname = eventname.replace('.', ' ')
                        groupname = "Power"

                    if type == "q":
                        if value == 0:
                            eventname = "Off"
                        if value == 1:
                            eventname = "Minimum"
                        if value == 2:
                            eventname = "Medium"
                        if value == 3:
                            eventname = "Maximum"
                        if value == 4:
                            eventname = "Auto"
                        if value == 5:
                            eventname = "Screen OFF"
                        newname = eventname.replace('.', ' ')
                        groupname = "Energy.Savings"

                    if type == "b":
                        if value == 0:
                            eventname = "DTV Antenna"
                        if value == 1:
                            eventname = "DTV Cable"
                        if value == 16:
                            eventname = "Analog Antenna" 
                        if value == 17:
                            eventname = "Analog Cable"
                        if value == 32:
                            eventname = "AV 1"
                        if value == 33:
                            eventname = "AV 2"
                        if value == 64 :
                            eventname = "Component 1" 
                        if value == 65 :
                            eventname = "Component 2"
                        if value == 66 :
                            eventname = "Component 3"
                        if value == 96 :
                            eventname = "RGB-PC"
                        if value == 144 :
                            eventname = "HDMI 1"
                        if value == 145 :
                            eventname = "HDMI 2"
                        if value == 146 :
                            eventname = "HDMI 3"
                        if value == 147 :
                            eventname = "HDMI 4"
                        newname = eventname.replace('.', ' ')
                        groupname = "Input"


                    if (type == "c") and (Gname[:4] == "Aspe") and (Gname != "Aspect Ratio Cinema Zoom Set Value"):
                        if value == 1:
                            eventname = "4:3"
                        if value == 2:
                            eventname = "16:9"
                        if value == 4:
                            eventname = "Zoom"
                        if value == 6:
                            eventname = "Set by Program"
                        if value == 9:
                            eventname = "Just Scan"
                        if value >= 16 and value <= 31:
                            eventname = "Cinema Zoom " + str(Gdata)
                        groupname = "Aspect"
                        newname = eventname.replace('.', ' ')


                    if type == "m" and Gname[:4] == "Remo" :
                        if value == 0:
                            eventname = "OFF"
                        if value == 1:
                            eventname = "ON"
                        newname = eventname.replace('.', ' ')
                        groupname = "Remote.Lock"

                    if type == "d" and Gname[:4] == "Scre" :
                        if value == 0:
                            eventname = "OFF"
                        if value == 1:
                            eventname = "ON"
                        if value == 16:
                            eventname = "Videoout Mute ON"
                        newname = eventname.replace('.', ' ')
                        groupname = "Screen.Mute"


                    if type == "e" and Gname[:4] == "Volu" :
                        if value == 0:
                            eventname = "ON"
                        if value == 1:
                            eventname = "OFF"
                        newname = eventname.replace('.', ' ')
                        groupname = "Volume.Mute"

                    if type == "l" and Gname[:3] == "OSD" :
                        if value == 0:
                            eventname = "OFF"
                        if value == 1:
                            eventname = "ON"
                        newname = eventname.replace('.', ' ')
                        groupname = "OSD"


                    if type == "g" and Gname[:4] == "Back" :
                        eventnamepayload = "Backlight"

                    if type == "g" and Gname[:4] == "Cont" :
                        eventnamepayload = "Contrast"

                    if type == "f" and Gname[:4] == "Volu" :
                        eventnamepayload = "Volume"

                    if type == "h" and Gname[:4] == "Brig" :
                        eventnamepayload = "Brightness"

                    if type == "j" and Gname[:4] == "Tint" :
                        eventnamepayload = "Tint"  
                                          
                    if type == "i" and Gname[:4] == "Colo" :
                        eventnamepayload = "Color" 

                    if type == "k" and Gname[:4] == "Shar" :
                        eventnamepayload = "Sharpnes"

                    if type == "r" and Gname[:4] == "Treb" :
                        eventnamepayload = "Treble"  
                                          
                    if type == "s" and Gname[:4] == "Bass" :
                        eventnamepayload = "Bass" 

                    if type == "k" and Gname[:4] == "Bala" :
                        eventnamepayload = "Balance"


                    if groupname != "" and Gname[:4] != "Cust":
                        self.TriggerEvent(groupname + statusname, payload=eventname)
                    if eventnamepayload != "" and Gname[:4] != "Cust":
                        self.TriggerEvent(eventnamepayload + statusname, payload=value)
                    if eventnamepayload == "" and groupname == "" and Gname[:4] != "Cust":
                        self.TriggerEvent(Gname.replace(' ', '.') + statusname, payload=value)
                    if Gname[:4] == "Cust":
                        self.TriggerEvent(Gname.replace(' ', '.') + statusname, payload=Gdata)
            else:
                line+=ch
        self.readerkiller = None


    def __start__(self, port, baudrate):
        try:
            self.serial = eg.SerialPort(port,baudrate=baudrate)
        except:
            raise eg.Exception("Can't open serial port.")
        self.serial.timeout = 30.0
        self.serial.setDTR(1)
        self.serial.setRTS(1)
        self.readerkiller = False
        thread.start_new_thread(self.reader,());
        
        
    def __stop__(self):
        self.readerkiller = True
        while self.readerkiller is not None:
            wx.MilliSleep(100)
        if self.serial is not None:
            self.serial.close()
            self.serial = None
    
          
            
    def Configure(self, port=0, baudrate=9600):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        baudrateCtrl = panel.ComboBox(
            str(baudrate),
            BAUDRATES,
            style=wx.CB_DROPDOWN,
            validator=eg.DigitOnlyValidator()
        )
     
        
        panel.AddLine("Port:", portCtrl)
        panel.AddLine("Baudrate:", baudrateCtrl)
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                int(baudrateCtrl.GetValue()),
            )


version="0.1.3" 

# Plugins/ScreamerRadio/__init__.py
#
# Copyright (C)  2008 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


# Every EventGhost plugin should start with the import of 'eg' and the 
# definition of an eg.PluginInfo subclass.

eg.RegisterPlugin(
    name = "Screamer Radio",
    author = "Pako",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control the <a href="http://www.screamer-radio.com/">'
        'Screamer radio</a>.'
    ),
    createMacrosOnAdd = True,    
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=840",
    icon = (
        "R0lGODlhEAAQAPcAAKQCBPyCBPzGjPzCBNRKDPzSRPS6RLxCVPyiBOzCxPz+RMQmBPzi"
        "BPxqBPyOJPzixPzKLPzGdPySBMxOJMxmRPyqNKwuPPzehPyyBPzaBPzmbPz65MxybPzW"
        "XPyuZPz2bPSKBPzGFMQWBPxaBPyqBOzS1MQ2BPx2BPzaZMxeLLQ6TPzqrPz69Pz+dPzW"
        "hPzGXPyyVPzaPPyaBMxmXPy6BNR6dPyKDPzefPzKBOzKzPzyNPxyBPyaPPzyzPzOPLQ2"
        "TPzmlNR2dPzeTPy+fPyOBPzGHKQSHMxaFPSuBLw6BPziZMxiPPz+/Pz6fPzSnKQGFPyG"
        "BPzGDNRODPzSTPS6TLxGVPymBOzGxMQuBPzqBPxuBPyOLPzONPyWBMxWJMxmTLQuPPze"
        "jPy2BPzWHPzudPz67Mx2bPy2bPz+ZPyKBMweBPTa3Px6BPzabMxiNLQ+VPzyvPz+9Pza"
        "jPzSVPyyXPyeBMxqXPy+BPz23PziXPzKHMxaHPyuBMQ6BPz+fAAAfNIdgOYAb4EAGXwA"
        "AJhjAEYAABUAAAAAAErwB+PqAIESAHwAAKBGAHfQAFAmAABbAJgQAEZAYAE4GQAAAGsF"
        "AAAAAAAAAAAAAJxKAOgTABIAAAAAAAB4AADqAAASAAAAAAiFAPwrABKDAAB8ABgAaO4A"
        "npAAgHwAfHAA/wUA/5EA/3wA//8AYP8Anv8AgP8AfG0pKgW3AJGSAHx8AEqAKvRvAIAZ"
        "AHwAAAA0WABk8RWDEgB8AAD//wD//wD//wD//5gAAEYAABUAAAAAAABcpAHq6wASEgAA"
        "AAA09gBkOACDTAB8AFcIhPT864ASEnwAAIgYd+ruEBKQTwB8AJgAuEa36xWSEgB8AKD/"
        "NAD/ZAD/gwD/fB+AWgBv7AAZEgAAABE01ABk/wCD/wB8fwSgMADr7AASEgAAAAPngABk"
        "bwCDGQB8AACINABkZACDgwB8fAABgAAAbwAAGQAAAAQxSgAAEwAAAAAAAAMBAAAAAAAA"
        "AAAAAAAajQAA4gAARwAAACH5BAAAAAAALAAAAAAQABAABwj/AJkIZLKmxhc3KSiYKTGw"
        "YZUkSvy0QKNgTB8VDZkYMdBEQ4c5U9oIycDnycADBsig6MCkAxcIPVbgsPKDoIkPKAqw"
        "YAIByAoxGzrcwZIjSIw8BW4wKQChyA0gJJggsGJniQIfEJgACaEnCg0mXeLU4TNhj447"
        "eJjciTJgAIYLCOTA6CLlSJYpTAbcaXuHxIsKETykIZCCQRmefDCIwVAngg0nDohM4ECD"
        "jwsmeGRIkBHgwQgWWgLMKLFAjAwZAumEdsDjTAA1CZi8SYOAyIkhTFjsYGMjgBYwA5+w"
        "6RKgARsBOwIQ2QEgowoRASQQSSPhNfCMTHLYmUCAwIQZVxoGAQQAOw=="
    ),
)


class Text:
    filemask = "screamer.exe|screamer.exe|All-Files (*.*)|*.*"
    label = "Path to screamer.exe:"
    version = "Version: "
    text1 = "Couldn't find Screamer Radio window !"


import os
import win32api
from win32gui import GetWindowText
import xml.sax as sax
from xml.sax.handler import ContentHandler
from eg.WinApi import SendMessageTimeout
from eg.WinApi.Dynamic import PostMessage
from time import sleep
BM_CLICK      = 245
WM_COMMAND    = 273
WM_SYSCOMMAND = 274
TBM_GETPOS    = 1024
#TBM_SETPOS    = 1029
SC_MINIMIZE   = 61472
SC_CLOSE      = 61536
SC_RESTORE    = 61728

Actions = (
    ("Play","Play","","Play","Play last playing station."),
    ("Stop","Stop","","Stop","Stop."),
    ("PlayStop","Play","Stop","Play/Stop","Play/Stop."),
    ("Next","Next","","Next stream","Next stream."),
    ("Prev","Prev","","Previous stream","Previous stream."),
    ("RecOff","RecOff","","Rec On","Rec On."),
    ("RecOn","RecOn","","Rec Off","Rec Off."),
    ("RecOnOff","RecOn","RecOff","Rec On/Off","Rec On/Off."),
    ("MuteOff","MuteOff","","Mute On","Mute On."),
    ("MuteOn","MuteOn","","Mute Off","Mute Off."),
    ("MuteOnOff","MuteOn","MuteOff","Mute On/Off","Mute On/Off."),
    )
FindScreamer1 = eg.WindowMatcher(
    u'screamer.exe',
    None,
    u'#32770',
    None,
    None,
    1,
    True,
    0.0,
    0
)
FindScreamer2 = eg.WindowMatcher(
    u'screamer.exe',
    None,
    u'#32770',
    None,
    None,
    2,
    True,
    0.0,
    0
)


#my xmlhandler1
class my_xml_handler1(ContentHandler):
    def startDocument( self):
        self.document = {}
        self._recent_text = ''

    def endElement( self, name):
        if name=="LanguageFile":
            self.document[name] = self._recent_text.strip()
        if name=="NotPlaying":
            self.document[name] = self._recent_text.strip()
        for item in Actions:
            if name==item[0]:
                self.document[name] = self._recent_text.strip()
                break
        self._recent_text = ''

    def characters( self, content):
        self._recent_text += content

    
#my xmlhandler2
class my_xml_handler2(ContentHandler):
    favorite = None
    item = None
    first = None
    def startDocument(self):
        self.counter = -1
        self.temp = None
    
    def startElement(self, name, attrs):  
        if name == "Station":
            self.temp = attrs.get("title")       
            self.counter += 1
            if self.counter==0:
                self.first=self.temp
            if self.item == self.counter:
                self.favorite=self.temp
        
        

class ScreamerRadio(eg.PluginClass):
    text=Text
    ScreamerPath = None
    
    def __init__(self):
        text=Text
        fav_num=None
        ScreamerPath = ""
        self.AddAction(Run)
        self.AddAction(WindowControl)

        for myTuple in Actions:
            class tmpActionClass(eg.ActionClass):
                name = myTuple[3]
                description = myTuple[4]
                key1 = myTuple[1]
                key2 = myTuple[2]
                if myTuple[0] != "PlayStop":
                    def __call__(self):
                        key = eval("self.plugin.dh.document[self.key1]")
                        FindAction = eg.WindowMatcher(
                            u'screamer.exe',
                            None,
                            u'#32770',
                            key,
                            u'Button',
                            1,
                            True,
                            0.0,
                            0
                        )
                        hwnds=FindAction()
                        if self.key2 != "": #for toggle actions
                            ret = "0"
                            if len(hwnds) == 0:
                                key = eval("self.plugin.dh.document[self.key2]")
                                FindAction = eg.WindowMatcher(
                                    u'screamer.exe',
                                    None,
                                    u'#32770',
                                    key,
                                    u'Button',
                                    1,
                                    True,
                                    0.0,
                                    0
                                )
                                hwnds=FindAction()
                                ret = "1"
                        else:
                            ret = " "
                        if len(hwnds) != 0:
                            SendMessageTimeout(hwnds[0], BM_CLICK, 0, 0)
                            return ret
                        else:
                            self.PrintError(self.plugin.text.text1)
                            return self.plugin.text.text1
                else:
                    def __call__(self):
                        Status = eg.WindowMatcher(
                            u'screamer.exe',
                            None,
                            u'#32770',
                            self.plugin.dh.document['NotPlaying'],
                            u'Static',
                            1,
                            True,
                            0.0,
                            0
                        )
                        hwnds = Status()
                        if len(hwnds) !=0: #Not playing
                            key = eval("self.plugin.dh.document[self.key1]")
                            ret = "1"
                        else:              #Playing
                            key = eval("self.plugin.dh.document[self.key2]")
                            ret = "0"
                        FindAction = eg.WindowMatcher(
                            u'screamer.exe',
                            None,
                            u'#32770',
                            key,
                            u'Button',
                            1,
                            True,
                            0.0,
                            0
                        )
                        hwnds=FindAction()
                        if len(hwnds) != 0:
                            SendMessageTimeout(hwnds[0], BM_CLICK, 0, 0)
                            return ret
                        else:
                            self.PrintError(self.plugin.text.text1)
                            return self.plugin.text.text1
                    
            tmpActionClass.__name__ = myTuple[0]
            self.AddAction(tmpActionClass)        
        self.AddAction(VolumeUp)
        self.AddAction(VolumeDown)
        self.AddAction(GetVolume)
        self.AddAction(SetVolume)
        self.AddAction(SelectFav)
        self.AddAction(NextFav)
        self.AddAction(PreviousFav)
        self.AddAction(GetPlayingTitle)

    def __start__(self, ScreamerPath):
        self.ScreamerPath = ScreamerPath
        xmltoparse = os.path.split(ScreamerPath)[0]+'\\screamer.xml'
        self.dh = my_xml_handler1()
        sax.parse(xmltoparse, self.dh)
        xmltoparse = self.dh.document['LanguageFile']
        sax.parse(xmltoparse, self.dh)
                   

    def Configure(self, ScreamerPath=None):
        if ScreamerPath is None:
            ScreamerPath = os.path.join(
                eg.folderPath.ProgramFiles, 
                "Screamer", 
                "screamer.exe"
            )
        panel = eg.ConfigPanel(self)
        VersionText = wx.StaticText(
            panel,
            -1,
            self.text.version+version,
            style=wx.ALIGN_LEFT
        )
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            size=(320,-1),
            initialValue=ScreamerPath, 
            startDirectory=eg.folderPath.ProgramFiles,
            fileMask = self.text.filemask,
            buttonText=eg.text.General.browse
        )
        panel.sizer.Add(VersionText, 0, wx.EXPAND)
        panel.sizer.Add((5, 20))
        panel.AddLabel(self.text.label)
        panel.AddCtrl(filepathCtrl)
        
        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue())

class Run(eg.ActionClass):
    name = "Run Screamer"
    description = "Run Screamer with its default settings."    
    class text:
        text2="Couldn't find file screamer.exe !" 
        play = "Automatic play selected favorite after start"
        label = "Select favorite:"
        over = "Too large number (%s > %s) !"
        alt_ret = "No autostart"
    def __call__(self, play, fav):
        flag=True
        try:
            head, tail = os.path.split(self.plugin.ScreamerPath)
            return win32api.ShellExecute(
                0, 
                None, 
                tail,
                None, 
                head, 
                1
            )
        except:
            flag=False
        finally:
            if flag:
                if play:
                    for n in range(50):                
                        sleep(.2)
                        hwnds = FindScreamer1()
                        if len(hwnds) != 0:
                            if GetWindowText(hwnds[0]) == "Screamer Log":
                                hwnds = FindScreamer2()
                        if len(hwnds) != 0:
                            flag = False
                            break
                    if not flag:
                        sleep(2)
                        ScreamerPath = self.plugin.ScreamerPath
                        xmltoparse = os.path.split(ScreamerPath)[0]+\
                            '\\favorites.xml'
                        self.dh2 = my_xml_handler2()
                        self.dh2.item=fav-1
                        sax.parse(xmltoparse, self.dh2)
                        if fav <= self.dh2.counter+1:
                            self.plugin.fav_num=fav-1
                            PostMessage(hwnds[0], WM_COMMAND, 9216+fav, 0)
                            return str(fav)+": "+self.dh2.favorite
                        else:
                            return self.text.over % (str(fav),\
                                str(self.dh2.counter+1))
                    else:
                        return self.plugin.text.text1
                else:
                    return self.text.alt_ret                    
            else:
                return self.text.text2
            
            
    def Configure(self, play=False, fav=1):
        panel=eg.ConfigPanel(self)
        sizerAdd=panel.sizer.Add
        playChkBoxCtrl = wx.CheckBox(panel, label=self.text.play)
        sizerAdd(playChkBoxCtrl,0,wx.TOP,15)		
        playChkBoxCtrl.SetValue(play)
        favLbl=wx.StaticText(panel, -1, self.text.label)
        sizerAdd(favLbl,0,wx.TOP,25)
        favCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            fav,
            fractionWidth=0,
            min=1,
            max=999,
        )
        favCtrl.SetValue(fav)
        sizerAdd(favCtrl,0,wx.TOP,5)
        def OnAutostart(evt=None):
            enbl=playChkBoxCtrl.GetValue()
            favLbl.Enable(enbl)
            favCtrl.Enable(enbl)
            if evt is not None:
                evt.Skip()
        playChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnAutostart)
        OnAutostart()
                
        while panel.Affirmed():
            panel.SetResult(
                playChkBoxCtrl.GetValue(),
                favCtrl.GetValue()
            )
                                
 
class VolumeUp(eg.ActionClass):
    name = "Volume up"
    description = "Volume up."
    def __call__(self):       
        FindSlider = eg.WindowMatcher(
            u'screamer.exe',
            None,
            u'#32770',
            u'Slider1',
            u'msctls_trackbar32',
            1,
            True,
            0.0,
            0
        )
        hwnds=FindSlider()        
        if len(hwnds) != 0:
            volume=SendMessageTimeout(hwnds[0], TBM_GETPOS, 0, 0)
            if volume>0:
                eg.SendKeys(hwnds[0], u'{Up}', False)
                #PostMessage(hwnds[0], TBM_SETPOS, 1, volume-1)
            else:
                volume=1
            return 100-5*(volume-1)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1

        
class VolumeDown(eg.ActionClass):
    name = "Volume down"
    description = "Volume down."
    def __call__(self):       
        FindSlider = eg.WindowMatcher(
            u'screamer.exe',
            None,
            u'#32770',
            u'Slider1',
            u'msctls_trackbar32',
            1,
            True,
            0.0,
            0
        )
        hwnds=FindSlider()        
        if len(hwnds) != 0:
            volume=SendMessageTimeout(hwnds[0], TBM_GETPOS, 0, 0)
            if volume<20:
                eg.SendKeys(hwnds[0], u'{Down}', False)
                #PostMessage(hwnds[0], TBM_SETPOS, 1, volume+1)
            else:
                volume=19
            return 100-5*(volume+1)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1

            
class GetVolume(eg.ActionClass):
    name = "Get volume"
    description = "Get volume."
    def __call__(self):       
        FindSlider = eg.WindowMatcher(
            u'screamer.exe',
            None, u'#32770',
            u'Slider1',
            u'msctls_trackbar32',
            1,
            True,
            0.0,
            0
        )
        hwnds=FindSlider()        
        if len(hwnds) != 0:
            return 100-5*SendMessageTimeout(hwnds[0], TBM_GETPOS, 0, 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
            
class SetVolume(eg.ActionClass):
    name = "Set volume"
    description = "Set volume."
    class text:
        label="Set volume (0-100%):"
        
    def __call__(self,volume):       
        FindSlider = eg.WindowMatcher(
            u'screamer.exe',
            None, u'#32770',
            u'Slider1',
            u'msctls_trackbar32',
            1,
            True,
            0.0,
            0
        )
        hwnds=FindSlider()        
        if len(hwnds) != 0:
            #PostMessage(hwnds[0], TBM_SETPOS, True, 20-volume/5)
            vol=SendMessageTimeout(hwnds[0], TBM_GETPOS, 0, 0)
            step = -20+vol+volume/5
            if step<>0:
                key = u'{Up}' if step>0 else u'{Down}'
                for n in range(abs(step)):
                    #sleep(.1)
                    eg.SendKeys(hwnds[0], key, False)
            


        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
            
    def Configure(self, volume=100):
        panel=eg.ConfigPanel(self)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.label))
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            volume,
            fractionWidth=0,
            increment=5,
            min=0,
            max=100,
            style=wx.TE_READONLY,
        )
        volumeCtrl.SetValue(volume)
        panel.sizer.Add(volumeCtrl,0,wx.TOP,10)
        
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())

class SelectFav(eg.ActionClass):
    name = "Select favorite"
    description = "Select favorite by order"    
    class text:
        label="Select favorite:"
        over = "Too large number (%s > %s) !"
    def __call__(self,fav):
        hwnds = FindScreamer1()
        if len(hwnds) != 0:
            if GetWindowText(hwnds[0]) == "Screamer Log":
                hwnds = FindScreamer2()
        if len(hwnds) != 0:
            ScreamerPath = self.plugin.ScreamerPath
            xmltoparse = os.path.split(ScreamerPath)[0]+'\\favorites.xml'
            self.dh2 = my_xml_handler2()
            self.dh2.item=fav-1
            sax.parse(xmltoparse, self.dh2)
            if fav <= self.dh2.counter+1:
                self.plugin.fav_num=fav-1
                PostMessage(hwnds[0], WM_COMMAND, 9216+fav, 0)
                return str(fav)+": "+self.dh2.favorite
            else:
                self.PrintError(
                    self.text.over % (str(fav),str(self.dh2.counter+1)))
                return self.text.over % (str(fav),str(self.dh2.counter+1))
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
            
    def Configure(self, fav=1):
        panel=eg.ConfigPanel(self)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.label))
        favCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            fav,
            fractionWidth=0,
            min=1,
            max=999,
        )
        favCtrl.SetValue(fav)
        panel.sizer.Add(favCtrl,0,wx.TOP,10)
        
        while panel.Affirmed():
            panel.SetResult(favCtrl.GetValue())

        
class NextFav(eg.ActionClass):
    name = "Next favorite"
    description = "Next favorite"    
    class text:
        over = "Too large number (%s > %s) !"
    def __call__(self):
        hwnds = FindScreamer1()
        if len(hwnds) != 0:
            if GetWindowText(hwnds[0]) == "Screamer Log":
                hwnds = FindScreamer2()
        if len(hwnds) != 0:
            ScreamerPath = self.plugin.ScreamerPath
            xmltoparse = os.path.split(ScreamerPath)[0]+'\\favorites.xml'
            self.dh2 = my_xml_handler2()
            try:
                self.dh2.item = self.plugin.fav_num+1
            except:
                self.plugin.fav_num=-1
                self.dh2.item = 1
            sax.parse(xmltoparse, self.dh2)
            if self.plugin.fav_num <= self.dh2.counter:        
                self.plugin.fav_num += 1
                if self.plugin.fav_num == self.dh2.counter+1:
                    self.plugin.fav_num = 0
                PostMessage(hwnds[0], WM_COMMAND, 9217+self.plugin.fav_num, 0)
                return (str(self.plugin.fav_num+1)+\
                    ": "+self.dh2.favorite) if self.plugin.fav_num >0 else \
                    "1: "+self.dh2.first
            else:
                self.PrintError(self.text.over % (str(self.plugin.fav_num+1),\
                    str(self.dh2.counter+1)))
                self.plugin.fav_num = 0
                PostMessage(hwnds[0], WM_COMMAND, 9217, 0)
                return "1: "+self.dh2.first
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
        
        
class PreviousFav(eg.ActionClass):
    name = "Previous favorite"
    description = "Previous favorite"    
    class text:
        over = "Too large number (%s > %s) !"
    def __call__(self):
        hwnds = FindScreamer1()
        if len(hwnds) != 0:
            if GetWindowText(hwnds[0]) == "Screamer Log":
                hwnds = FindScreamer2()
        if len(hwnds) != 0:
            ScreamerPath = self.plugin.ScreamerPath
            xmltoparse = os.path.split(ScreamerPath)[0]+'\\favorites.xml'
            self.dh2 = my_xml_handler2()
            try:
                self.dh2.item = self.plugin.fav_num-1
            except:
                self.plugin.fav_num=1
                self.dh2.item = 0
            sax.parse(xmltoparse, self.dh2)
            if self.plugin.fav_num <= self.dh2.counter:        
                self.plugin.fav_num -= 1
                if self.plugin.fav_num == -1:
                    self.plugin.fav_num = self.dh2.counter
                PostMessage(hwnds[0], WM_COMMAND, 9217+self.plugin.fav_num, 0)
                return (str(self.plugin.fav_num+1)+": "+self.dh2.favorite) if \
                    self.plugin.fav_num <self.dh2.counter else \
                    str(self.dh2.counter+1)+": "+self.dh2.temp
            else:
                self.PrintError(self.text.over % (str(self.plugin.fav_num+1),\
                    str(self.dh2.counter+1)))
                self.plugin.fav_num = 0
                PostMessage(hwnds[0], WM_COMMAND, 9217, 0)
                return "1: "+self.dh2.first
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
        
        
class GetPlayingTitle(eg.ActionClass):
    name = "Get currently playing title"
    description = "Gets the name of currently playing title."    
    def __call__(self):
        def GetWinTitle(hwnd):
            if ( hwnd is not None ):
                WinTitle = GetWindowText(hwnd[0])
                return WinTitle
        hwnd = FindScreamer1()
        WinTitle=GetWinTitle(hwnd)
        if WinTitle == "Screamer Log":
            hwnd = FindScreamer2()
            return GetWinTitle(hwnd)
        else:
            return WinTitle

class WindowControl(eg.ActionClass):
    name = "Window control"
    description = "Window control."
    class text:
        label="Select action for Screamer window:"
        win = "Window"
        class Actions:
            Minimize = "Minimize"
            Restore = "Restore"
            Close = "Close"

            
    def __init__(self):
        text=self.text
        self.actionsList=(
            (SC_MINIMIZE,"Minimize"),
            (SC_RESTORE,"Restore"),
            (SC_CLOSE,"Close"),
        )
        
        
    def __call__(self, i):
        hwnds = FindScreamer1()
        if len(hwnds) != 0:
            if GetWindowText(hwnds[0]) == "Screamer Log":
                hwnds = FindScreamer2()
        if len(hwnds) != 0:
            SendMessageTimeout(
                hwnds[0], WM_SYSCOMMAND, self.actionsList[i][0], 0)
        else:
            self.PrintError(self.plugin.text.text1)
            return self.plugin.text.text1
 
    def GetLabel(self, i):
        return self.text.win+" "+eval(
            "self.text.Actions."+self.actionsList[i][1])

    def Configure(self, i=0):
        choices=[eval("self.text.Actions."+tpl[1]) for tpl in self.actionsList]
        panel=eg.ConfigPanel(self)
        panel.sizer.Add(wx.StaticText(panel, -1, self.text.label))
        actionCtrl=wx.Choice(
            panel,
            choices=choices,
        )
        actionCtrl.SetSelection(i)
        panel.sizer.Add(actionCtrl,0,wx.TOP,10)
        
        while panel.Affirmed():
            panel.SetResult(actionCtrl.GetSelection())

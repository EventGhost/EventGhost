version="0.1.2"

# Plugins/MediaMonkey/__init__.py
#
# Copyright (C)  2007 Pako  <lubos.ruckl@quick.cz>
#
# This file is part of EventGhost.
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
#
#Last change: 2007-11-02 13:43

import eg

eg.RegisterPlugin(
    name = "MediaMonkey",
    author = "Pako",
    version = version,
    kind = "program",
    createMacrosOnAdd = True,
    description = (
        'Adds support functions to control '
        '<a href="http://www.MediaMonkey.com/">MediaMonkey</a>. \n\n<P>'
        '<BR><B>Note:</B><BR>'
        'To make functional event triggering from MediaMonkey, you must install'
        '<BR>file "EventGhost.vbs" to MediaMonkey/Scripts/Auto folder.'
    ),
    icon = (
        "R0lGODlhEAAQAPcAAAQCBMSORFxKLLSupExKVOy2ZKRiLCwyZJyGbERCRHRiXNzOlPTmpO"
        "QCpCwqLCQynOSmXGRifGRSNPzejNTe3KSWZJRKFJxiPIR6XCwyVNS2jCwyfLSejNTW1LRO"
        "XGxKPIQ6DJxyXHxCHCw6ZOTWnPz+/KRyTNSudNyeTNS+pDxCdPzWjPz+tFQ6JCQ6nPTenO"
        "Tm3MyWXJxqTNTGjHxKLAwKBNyWRNS2dMRiJBwqdERKTNzWjEQqJGxSRPTelLRaHJxqRJR6"
        "ZMy2nHRKTKx6XLSujCQ6pNSeXMSOTLS2rGxSVOy+bKxiLCwybLSObHRiZOzezOSuXGxihN"
        "ze5KRiPIx6XHQuVNS2lCwyhLSmjNTW3NRKhGxKRIQ6FHxKHDQ6ZNS+rDxCfPz+vOTm5NSW"
        "XIRKLBQKBExKTOTWlFQyJGRaTPzelKxaJKx6ZLyujCw6pAD98wAAAAAAvgAAAgAwBADqAA"
        "ASAAAAAADQ4gA8BBUlAABbAGDYYOnqnhISgAAAfNLzwOYAK4EAFnwAADi+APYCABkAAAAA"
        "AErwB+PqAIESAHwAAKBgAHfaAFAlAABbADjYAPbqIAESFgAAAGsDAAAAAAAAAAAAAJxKAO"
        "h4ABIAAAAAAAB4AADqAAASAAAAAAiFAPwrABKDAAB8ABgAaO4AnpAAgHwAfHAA/wUA/5EA"
        "/3wA//8AYP8Anv8AgP8AfG0pKAW3AJGSAHx8AErAKPQrAIAWAHwAAAA0WABk8RWDEgB8AA"
        "D//wD//wD//wD//zgAAPYAABkAAAAAAABcpAHq6wASEgAAAAA09gBkOACDTAB8AFcIhPT8"
        "64ASEnwAAIgYd+ruEBKQTwB8ADgAuPa36xmSEgB8AKD/NAD/ZAD/gwD/fB/AWAAr7AAWEg"
        "AAABE01gBk/wCD/wB8fwSgMADr7AASEgAAAAPnwABkKwCDFgB8AACINABkZACDgwB8fAAB"
        "wAAAKwAAFgAAAAQxSgAAeAAAAAAAAAMBAAAAAAAAAAAAAAAajQAA4gAARwAAACH5BAEAAA"
        "AALAAAAAAQABAABwjfAAEIHOigoIOBCBEeFHIFwMGEBC2w+fHDgIWHCROAMEEFBw4DJkAk"
        "yNgDSIkxbNiMKSHjw0iBCjLwSEGBQhsiFDqASZPhCQAEGw60gHLGgRs3Ds5AaXEASxAlRk"
        "bw4OBmBgsxM9xk4XHAiBIuD5qo2cGAxIIFaBig6XHgQY8yOVT4qDJgzBgYMJJgeKEiBw0n"
        "XKRMqJAgQcEEZypMiPDBiZMuXk6sMIOwxoobIkQ4ERgiwAQBVrZssSJgQoAQCUNAWOKhQQ"
        "MPS6KghqjBRgEyZAqgaAhR4JUYR47E4D0wIAA7"
    ),
)
    
        
import wx
from win32com.client import Dispatch
#import new


#====================================================================
class Text:
    errorNoWindow = "Couldn't find MediaMonkey window"    
    errorConnect = "MediaMonkey is not running or connected"    
    mainGrpName = "Main control of MediaMonkey"
    mainGrpDescr = "Here you find actions for main control of MediaMonkey."
    levelGrpName = "Another control of MediaMonkey"
    levelGrpDescr = (
        "Here you find further actions for control of MediaMonkey"
        " (volume, balance, seek)."
    )
    extrGrpName = "Writing to database MM"
    extrGrpDescr = (
        "Here is action for writing some one parameters to database MediaMonkey."
    )
    infoGrpName = "Information retrieval"
    infoGrpDescr = (
        "Here you find actions for information retrieval"
        " from MediaMonkey."
    )
#====================================================================
class MediaMonkey(eg.PluginClass):
    text = Text
    
    def __init__(self):
        group = self.AddGroup(
            self.text.mainGrpName, 
            self.text.mainGrpDescr
        )
        group.AddAction(Start)
        group.AddAction(Exit)
        group.AddAction(Play)
        group.AddAction(TogglePlay)
        group.AddAction(DiscretePause)
        group.AddAction(Stop)
        group.AddAction(Next)
        group.AddAction(Previous)

        group = self.AddGroup(
            self.text.levelGrpName, 
            self.text.levelGrpDescr
        )
        group.AddAction(ToggleMute)
        group.AddAction(SetVolume)
        group.AddAction(VolumeUp)
        group.AddAction(VolumeDown)
        group.AddAction(SetBalance)
        group.AddAction(BalanceRight)
        group.AddAction(BalanceLeft)
        group.AddAction(Seek)

        group = self.AddGroup(
            self.text.extrGrpName, 
            self.text.extrGrpDescr
        )
        group.AddAction(WritingToMM)

        group = self.AddGroup(
            self.text.infoGrpName, 
            self.text.infoGrpDescr
        )
        group.AddAction(GetVolume)
        group.AddAction(GetBalance)
        group.AddAction(GetStatus)
        group.AddAction(GetRepeat)
        group.AddAction(GetShuffle)
        group.AddAction(GetPosition)
        group.AddAction(GetBasicSongInfo)
        group.AddAction(GetDetailSongInfo)
        group.AddAction(GetClassificationInfo)
        group.AddAction(GetTechnicalSongInfo)
        group.AddAction(GetUniversal)

    def __start__(self):
        self.MM=None
        self.volume=None
        self.muted=False
            
    def __stop__(self):
        try:
            if self.MM:
                del self._MM
        except:
            pass

    def getMM(self, command):
        try:
            if self.MM.IsRunning:
                return eval("self.MM." + command)
            else:
                self.PrintError(self.text.errorConnect)
                return
        except:
            self.PrintError(self.text.errorConnect)
            return
            
    def setMM(self, command):
        try:
            if self.MM.IsRunning:
                exec "self.MM." + command 
            else:
                self.PrintError(self.text.errorConnect)
        except:
            self.PrintError(self.text.errorConnect)

#====================================================================
#====================================================================
class Start(eg.ActionClass):
    name = "Start/Connect MediaMonkey"
    description = "Start or Connect MediaMonkey through COM-API."
    class text:
        error = "Couldn't connect to MediaMonkey"

    def __call__(self):
        self.plugin.MM=Dispatch("SongsDB.SDBApplication")
        self.plugin.MM.ShutdownAfterDisconnect=False

#====================================================================
class Exit(eg.ActionClass):
    name = "Exit MediaMonkey"
    description = "Exit MediaMonkey."
    
    def __call__(self):
        try:
            if self.plugin.MM:
                del self.plugin.MM
        except:
            pass
        eg.plugins.Window.FindWindow(
            u'MediaMonkey.exe',
            u'{*}MediaMonkey{*}',
            u'TFMainWindow',
            None,
            None,
            1,
            True,
            1.0,
            0
        )
        eg.plugins.Window.Close()

#====================================================================
class Play(eg.ActionClass):
    name = "Play"
    description = "Play."

    def __call__(self):
        self.plugin.setMM("Player.Play()")

#====================================================================
class TogglePlay(eg.ActionClass):
    name = "Toggle Play"
    description = "Toggles between play and pause of MediaMonkey."
    
    def __call__(self):
        if  not self.plugin.getMM("Player.isPlaying"):
            # Play
            return self.plugin.getMM("Player.Play()")
        else:
            # Toggle Play/Pause
            return self.plugin.getMM("Player.Pause()")

#====================================================================
class DiscretePause(eg.ActionClass):
    name = "Discrete Pause"
    description = (
        "Pauses MediaMonkey if it is playing, but won't do anything if "
        "MediaMonkey is already paused."
    )
    
    def __call__(self):
        if (self.plugin.getMM("Player.isPlaying")):
            if (not self.plugin.getMM("Player.isPaused")):
                return self.plugin.getMM("Player.Pause()")

#====================================================================
class Stop(eg.ActionClass):
    name = "Stop"
    description = "Simulate a press on the stop button."
    
    def __call__(self):
        return self.plugin.getMM("Player.Stop()")
        
        
#====================================================================
class Next(eg.ActionClass):
    name = "Next"
    description = "Next."

    def __call__(self):
        self.plugin.setMM("Player.Next()")

#====================================================================
class Previous(eg.ActionClass):
    name = "Previous"
    description = "Previous."

    def __call__(self):
        self.plugin.setMM("Player.Previous()")


#====================================================================
class ToggleMute(eg.ActionClass):
    name = "Toggle Mute"
    description = "Toggle Mute."

    def __call__(self):
        if not self.plugin.muted:
            self.plugin.volume=self.plugin.getMM("Player.Volume")
            self.plugin.setMM("Player.Volume=0")
            self.plugin.muted=True
        else:
            self.plugin.setMM("Player.Volume="+str(self.plugin.volume))
            self.plugin.muted=False


#====================================================================
class SetVolume(eg.ActionClass):
    name = "Set Volume Level"
    description = "Sets the volume to a percentage (%)."
    class text:
        label_tree="Set volume "
        label_conf="Volume Level:"
    def __call__(self, volume):
        self.plugin.setMM("Player.Volume = "+str(volume/100))
        if volume!=0:
            self.plugin.muted=False

    def GetLabel(self, volume):
        return self.text.label_tree+str(int(volume))+"%"

    def Configure(self, volume=100.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            volume,
            max=100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(volumeCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())
            
            
#====================================================================
class VolumeUp(eg.ActionClass):
    name = "Volume up "
    description = "Volume up x%."
    class text:
        label_tree="Volume up "
        label_conf="Volume step:"

    def __call__(self, step):
        if step>0:
            self.plugin.muted=False
            volume=self.plugin.getMM("Player.Volume")
            if volume<1:
                if volume>(1-step/100):
                    volume=1
                else:
                    volume+=step/100
                self.plugin.setMM("Player.Volume="+str(volume))

    def GetLabel(self, step):
        return self.text.label_tree+str(int(step))+"%"

    def Configure(self, step=10.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl(panel, -1, step, max=100.0,fractionWidth=1)
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(volumeCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())

#====================================================================
class VolumeDown(eg.ActionClass):
    name = "Volume down "
    description = "Volume down x%."
    class text:
        label_tree="Volume down "
        label_conf="Volume step:"
    def __call__(self, step):
        volume=self.plugin.getMM("Player.Volume")
        if volume>0:
            if volume<abs(step)/100:
                volume=0
            else:
                volume+=step/100
            self.plugin.setMM("Player.Volume="+str(volume))

    def GetLabel(self, step):
        return self.text.label_tree+str(abs(int(step)))+"%"

    def Configure(self, step=-10.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            max=0.0,
            min=-100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(volumeCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())

#====================================================================
class SetBalance(eg.ActionClass):
    name = "Set Balance"
    description = "Sets the balance."
    class text:
        label_tree="Set balance "
        label_conf = "Balance (-100 ... 100):"
    def __call__(self, balance):
        self.plugin.setMM("Player.Panning = "+str(balance/100))

    def GetLabel(self, balance):
        return self.text.label_tree+str(int(balance))+"%"

    def Configure(self, balance=0.0):
        panel = eg.ConfigPanel(self)
        balanceCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            balance,
            max=100.0,
            min=-100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(balanceCtrl)
        while panel.Affirmed():
            panel.SetResult(balanceCtrl.GetValue())

#====================================================================
class BalanceRight(eg.ActionClass):
    name = "Balance Right x%"
    description = "Balance Right x%."
    class text:
        label_tree="Balance right "
        label_conf = "Balance step:"
    def __call__(self, step):
        if step>0:
            balance=self.plugin.getMM("Player.Panning")
            if balance<1:
                if balance>(1-step/100):
                    balance=1
                else:
                    balance+=step/100
                self.plugin.setMM("Player.Panning="+str(balance))

    def GetLabel(self, step):
        return self.text.label_tree+str(int(step))+"%"

    def Configure(self, step=10.0):
        panel = eg.ConfigPanel(self)
        balanceCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            max=100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(balanceCtrl)
        while panel.Affirmed():
            panel.SetResult(balanceCtrl.GetValue())

#====================================================================
class BalanceLeft(eg.ActionClass):
    name = "Balance Left x%"
    description = "Balance Left x%."
    class text:
        label_tree="Balance left "
        label_conf = "Balance step:"
    def __call__(self, step):
        if step>0:
            balance=self.plugin.getMM("Player.Panning")
            if balance>-1:
                if balance<(step/100-1):
                    balance=-1
                else:
                    balance+=-step/100
                self.plugin.setMM("Player.Panning="+str(balance))

    def GetLabel(self, step):
        return self.text.label_tree+str(int(step))+"%"

    def Configure(self, step=10.0):
        panel = eg.ConfigPanel(self)
        balanceCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            max=100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(balanceCtrl)
        while panel.Affirmed():
            panel.SetResult(balanceCtrl.GetValue())

#====================================================================
class Seek(eg.ActionClass):
    name = "Seek Forward or Backward x%"
    description = "Seek Forward or Backward x%."
    class text:
        radiobox = "Seek direction"
        btnForward = "Forward"
        btnBackward = "Backward"
        label = "Seek step (%):"
        tree_lab1 = "Seek "
        tree_lab2 = "backward"
        tree_lab3 = "forward"
    def __call__(self, step, direction):
        length=self.plugin.getMM("Player.CurrentSongLength")
        pos=self.plugin.getMM("Player.PlaybackTime")
        if direction: #Backward
            if pos>length*step/100:
                self.plugin.setMM(
                    "Player.PlaybackTime="+str(pos-length*step/100)
                )
            else:
                self.plugin.setMM("Player.PlaybackTime=0")
        else:         #Forward   
            if pos<length-length*step/100:
                self.plugin.setMM(
                    "Player.PlaybackTime="+str(pos+length*step/100)
                )
            else:
                self.plugin.setMM("Player.PlaybackTime="+str(length-500))
            
    def GetLabel(self, step, direction):
        return self.text.tree_lab1\
            +(self.text.tree_lab2 if direction else self.text.tree_lab3)\
            +" "+str(int(step))+"%"
        
    def Configure(self, step=10.0, direction=0):
        text=Text
        panel = eg.ConfigPanel(self)
        seekCtrl = eg.SpinNumCtrl(panel, -1, step, max=100.0, fractionWidth=1)
        radioBox = wx.RadioBox(
            panel, 
            -1, 
            self.text.radiobox, 
            choices=[self.text.btnForward, self.text.btnBackward], 
            style=wx.RA_SPECIFY_ROWS
        )
        panel.AddLabel(self.text.label)
        panel.AddCtrl(seekCtrl)
        radioBox.SetSelection(direction)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(seekCtrl.GetValue(),radioBox.GetSelection())
            

#====================================================================
class GetVolume(eg.ActionClass):
    name = "Get Volume"
    description = "Get Volume."
    def __call__(self):
        return 100*self.plugin.getMM("Player.Volume")


#====================================================================
class GetBalance(eg.ActionClass):
    name = "Get Balance"
    description = "Get Balance."
    def __call__(self):
        return 100*self.plugin.getMM("Player.Panning")

#====================================================================
class GetStatus(eg.ActionClass):
    name = "Get Status"
    description = "Get Status (return string Playing, Paused or Stoped)."
    def __call__(self):
        playing=self.plugin.getMM("Player.isPlaying")
        paused=self.plugin.getMM("Player.isPaused")
        if not playing:
            return "Stoped"
        elif playing and not paused:
            return "Playing"
        elif playing and paused:
            return "Paused"

#====================================================================
class GetRepeat(eg.ActionClass):
    name = "Get Repeat"
    description = "Get Repeat Status."
    def __call__(self):
        return self.plugin.getMM("Player.isRepeat")

#====================================================================
class GetShuffle(eg.ActionClass):
    name = "Get Shuffle"
    description = "Get Shuffle Status."
    def __call__(self):
        return self.plugin.getMM("Player.isShuffle")


#====================================================================
class GetPosition(eg.ActionClass):
    name = "Get Position in ms"
    description = "Get Position in ms."
    def __call__(self):
        return self.plugin.getMM("Player.PlaybackTime")

#====================================================================
class GetBasicSongInfo(eg.ActionClass):
    name = "Get basic song info"
    description = "Get basic song info."
    class text:
        filepath = "File path"
        filename = "File name"
        tracktitle = "Track title"
        artist = "Artist"
        album = "Album"
        albumartist = "Album artist"
        year = "Year"
        track = "Track #"
        genre = "Genre"
        rating = "Rating"
        comment = "Comment"

    def __call__(self,arrayInfo):
        path=self.plugin.getMM("Player.CurrentSong.Path")
        indx=path.rfind("\\")+1
        result=path[:indx]+"," if arrayInfo[0] else ""
        result+=path[indx:]+"," if arrayInfo[1] else ""
        listPropert=(
            "Title",
            "ArtistName",
            "AlbumName",
            "AlbumArtistName",
            "Year",
            "TrackOrder",
            "Genre",
            "Rating",
            "Comment"
        )
        listNum=(
            False,
            False,
            False,
            False,
            True,
            True,
            False,
            True,
            False
        )
        for propert,cond,numeric in zip(listPropert,arrayInfo[2:],listNum):
            if numeric:
                result+=str(self.plugin.getMM("Player.CurrentSong."+propert))\
                    +"," if cond else ""
            else:
                result+=self.plugin.getMM("Player.CurrentSong."+propert)\
                    +"," if cond else ""
        return result[:-1]        


    def GetLabel(self, arrayInfo):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*11
    ):
        text=self.text
        panel = eg.ConfigPanel(self)
        filepathCtrl = wx.CheckBox(panel, -1, self.text.filepath)
        filepathCtrl.SetValue(arrayInfo[0])
        filenameCtrl = wx.CheckBox(panel, -1, self.text.filename)
        filenameCtrl.SetValue(arrayInfo[1])
        tracktitleCtrl = wx.CheckBox(panel, -1, self.text.tracktitle)
        tracktitleCtrl.SetValue(arrayInfo[2])
        artistCtrl = wx.CheckBox(panel, -1, self.text.artist)
        artistCtrl.SetValue(arrayInfo[3])
        albumCtrl = wx.CheckBox(panel, -1, self.text.album)
        albumCtrl.SetValue(arrayInfo[4])
        albumartistCtrl = wx.CheckBox(panel, -1, self.text.albumartist)
        albumartistCtrl.SetValue(arrayInfo[5])
        yearCtrl = wx.CheckBox(panel, -1, self.text.year)
        yearCtrl.SetValue(arrayInfo[6])
        trackCtrl = wx.CheckBox(panel, -1, self.text.track)
        trackCtrl.SetValue(arrayInfo[7])
        genreCtrl = wx.CheckBox(panel, -1, self.text.genre)
        genreCtrl.SetValue(arrayInfo[8])
        ratingCtrl = wx.CheckBox(panel, -1, self.text.rating)
        ratingCtrl.SetValue(arrayInfo[9])
        commentCtrl = wx.CheckBox(panel, -1, self.text.comment)
        commentCtrl.SetValue(arrayInfo[10])

        panel.AddCtrl(filepathCtrl)
        panel.AddCtrl(filenameCtrl)
        panel.AddCtrl(tracktitleCtrl)
        panel.AddCtrl(artistCtrl)
        panel.AddCtrl(albumCtrl)
        panel.AddCtrl(albumartistCtrl)
        panel.AddCtrl(yearCtrl)
        panel.AddCtrl(trackCtrl)
        panel.AddCtrl(genreCtrl)
        panel.AddCtrl(ratingCtrl)
        panel.AddCtrl(commentCtrl)


        while panel.Affirmed():
            arrayInfo=[
                filepathCtrl.GetValue(),
                filenameCtrl.GetValue(),
                tracktitleCtrl.GetValue(),
                artistCtrl.GetValue(),
                albumCtrl.GetValue(),
                albumartistCtrl.GetValue(),
                yearCtrl.GetValue(),
                trackCtrl.GetValue(),
                genreCtrl.GetValue(),
                ratingCtrl.GetValue(),
                commentCtrl.GetValue()
            ]
            panel.SetResult(arrayInfo)


#====================================================================
class GetDetailSongInfo(eg.ActionClass):
    name = "Get detail song info"
    description = "Get detail song info."
    class text:
        composer = "Composer"
        lyricist = "Lyricist"
        involvedpeople = "Involved people"
        originaltitle = "Original title"
        originalartist = "Original artist"
        originallyricist = "Original lyricist"
        originalyear = "Original year"
        BPM = "BPM"
        ISRC = "ISRC"
        publisher = "Publisher"
        encoder = "Encoder"
        copyright = "Copyright"

    def __call__(self, arrayInfo):
        listPropert=(
        "MusicComposer",
        "Lyricist",
        "InvolvedPeople",
        "OriginalTitle",
        "OriginalArtist",
        "OriginalLyricist",
        "OriginalYear",
        "BPM",
        "ISRC",
        "Publisher",
        "Encoder",
        "Copyright"
        )
        listNum=(
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            False,
            False
        )
        result=""
        for propert,cond,numeric in zip(listPropert,arrayInfo,listNum):
            if numeric:
                result+=str(self.plugin.getMM("Player.CurrentSong."+propert))\
                    +"," if cond else ""
            else:    
                result+=self.plugin.getMM("Player.CurrentSong."+propert)\
                    +"," if cond else ""
        return result[:-1]

    def GetLabel(self, arrayInfo):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*12
    ):
        text=self.text
        panel = eg.ConfigPanel(self)
        composerCtrl = wx.CheckBox(panel, -1, self.text.composer)
        composerCtrl.SetValue(arrayInfo[0])
        lyricistCtrl = wx.CheckBox(panel, -1, self.text.lyricist)
        lyricistCtrl.SetValue(arrayInfo[1])
        involvedpeopleCtrl = wx.CheckBox(panel, -1, self.text.involvedpeople)
        involvedpeopleCtrl.SetValue(arrayInfo[2])
        originaltitleCtrl = wx.CheckBox(panel, -1, self.text.originaltitle)
        originaltitleCtrl.SetValue(arrayInfo[3])
        originalartistCtrl = wx.CheckBox(panel, -1, self.text.originalartist)
        originalartistCtrl.SetValue(arrayInfo[4])
        originallyricistCtrl = wx.CheckBox(
            panel,
            -1,
            self.text.originallyricist
        )
        originallyricistCtrl.SetValue(arrayInfo[5])
        originalyearCtrl = wx.CheckBox(panel, -1, self.text.originalyear)
        originalyearCtrl.SetValue(arrayInfo[6])
        BPMCtrl = wx.CheckBox(panel, -1, self.text.BPM)
        BPMCtrl.SetValue(arrayInfo[7])
        ISRCCtrl = wx.CheckBox(panel, -1, self.text.ISRC)
        ISRCCtrl.SetValue(arrayInfo[8])
        publisherCtrl = wx.CheckBox(panel, -1, self.text.publisher)
        publisherCtrl.SetValue(arrayInfo[9])
        encoderCtrl = wx.CheckBox(panel, -1, self.text.encoder)
        encoderCtrl.SetValue(arrayInfo[10])
        copyrightCtrl = wx.CheckBox(panel, -1, self.text.copyright)
        copyrightCtrl.SetValue(arrayInfo[11])

        panel.AddCtrl(composerCtrl)
        panel.AddCtrl(lyricistCtrl)
        panel.AddCtrl(involvedpeopleCtrl)
        panel.AddCtrl(originaltitleCtrl)
        panel.AddCtrl(originalartistCtrl)
        panel.AddCtrl(originallyricistCtrl)
        panel.AddCtrl(originalyearCtrl)
        panel.AddCtrl(BPMCtrl)
        panel.AddCtrl(ISRCCtrl)
        panel.AddCtrl(publisherCtrl)
        panel.AddCtrl(encoderCtrl)
        panel.AddCtrl(copyrightCtrl)


        while panel.Affirmed():
            arrayInfo=[
                composerCtrl.GetValue(),
                lyricistCtrl.GetValue(),
                involvedpeopleCtrl.GetValue(),
                originaltitleCtrl.GetValue(),
                originalartistCtrl.GetValue(),
                originallyricistCtrl.GetValue(),
                originalyearCtrl.GetValue(),
                BPMCtrl.GetValue(),
                ISRCCtrl.GetValue(),
                publisherCtrl.GetValue(),
                encoderCtrl.GetValue(),
                copyrightCtrl.GetValue()
            ]
            panel.SetResult(arrayInfo)


#====================================================================
class GetClassificationInfo(eg.ActionClass):
    name = "Get classification song info"
    description = "Get classification song info."
    class text:
        tempo = "Tempo"
        mood = "Mood"
        occasion = "Occasion"
        quality = "Quality"
        custom1 = "Custom 1"
        custom2 = "Custom 2"
        custom3 = "Custom 3"

    def __call__(self,arrayInfo):
        listPropert=(
            "Tempo",
            "Mood",
            "Occasion",
            "Quality",
            "Custom1",
            "Custom2",
            "Custom3"
        )
        result=""
        for propert,cond in zip(listPropert,arrayInfo):
            result+=self.plugin.getMM("Player.CurrentSong."+propert)\
                +"," if cond else ""
        return result[:-1]

    def GetLabel(self, arrayInfo):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*7
    ):
        text=self.text
        panel = eg.ConfigPanel(self)
        tempoCtrl = wx.CheckBox(panel, -1, self.text.tempo)
        tempoCtrl.SetValue(arrayInfo[0])
        moodCtrl = wx.CheckBox(panel, -1, self.text.mood)
        moodCtrl.SetValue(arrayInfo[1])
        occasionCtrl = wx.CheckBox(panel, -1, self.text.occasion)
        occasionCtrl.SetValue(arrayInfo[2])
        qualityCtrl = wx.CheckBox(panel, -1, self.text.quality)
        qualityCtrl.SetValue(arrayInfo[3])
        custom1Ctrl = wx.CheckBox(panel, -1, self.text.custom1)
        custom1Ctrl.SetValue(arrayInfo[4])
        custom2Ctrl = wx.CheckBox(panel, -1, self.text.custom2)
        custom2Ctrl.SetValue(arrayInfo[5])
        custom3Ctrl = wx.CheckBox(panel, -1, self.text.custom3)
        custom3Ctrl.SetValue(arrayInfo[6])

        panel.AddCtrl(tempoCtrl)
        panel.AddCtrl(moodCtrl)
        panel.AddCtrl(occasionCtrl)
        panel.AddCtrl(qualityCtrl)
        panel.AddCtrl(custom1Ctrl)
        panel.AddCtrl(custom2Ctrl)
        panel.AddCtrl(custom3Ctrl)

        while panel.Affirmed():
            arrayInfo=[
                tempoCtrl.GetValue(),
                moodCtrl.GetValue(),
                occasionCtrl.GetValue(),
                qualityCtrl.GetValue(),
                custom1Ctrl.GetValue(),
                custom2Ctrl.GetValue(),
                custom3Ctrl.GetValue()
            ]
            panel.SetResult(arrayInfo)
#====================================================================
class GetTechnicalSongInfo(eg.ActionClass):
    name = "Get technical song info"
    description = "Get technical song info."
    class text:
        length = "Length"
        bitrate = "Bitrate"
#        seekable = "Seekable"
        frequency = "Frequency"
        stereo = "Stereo"
#        copyrighted = "Copyrighted"
#        original = "Original"
        counter = "Play counter"
        lastplayed = "Last played"
        filesize = "File size"
        VBR = "VBR"
        leveling = "Leveling"

    def __call__(self, arrayInfo):
        listPropert=(
            "SongLength",
            "Bitrate",
            "SampleRate",
            "Channels",
            "PlayCounter",
            "LastPlayed",
            "FileLength",
            "VBR",
            "Leveling"
        )
        result=""
        for propert,cond in zip(listPropert,arrayInfo):
            result+=str(self.plugin.getMM("Player.CurrentSong."+propert))\
                +"," if cond else ""
        return result[:-1]

    def GetLabel(self, arrayInfo):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*9
    ):
        text=self.text
        panel = eg.ConfigPanel(self)
        lengthCtrl = wx.CheckBox(panel, -1, self.text.length)
        lengthCtrl.SetValue(arrayInfo[0])
        bitrateCtrl = wx.CheckBox(panel, -1, self.text.bitrate)
        bitrateCtrl.SetValue(arrayInfo[1])
#        seekableCtrl = wx.CheckBox(panel, -1, self.text.seekable)
#        seekableCtrl.SetValue(seekable)
        frequencyCtrl = wx.CheckBox(panel, -1, self.text.frequency)
        frequencyCtrl.SetValue(arrayInfo[2])
        stereoCtrl = wx.CheckBox(panel, -1, self.text.stereo)
        stereoCtrl.SetValue(arrayInfo[3])
#        copyrightedCtrl = wx.CheckBox(panel, -1, self.text.copyrighted)
#        copyrightedCtrl.SetValue(copyrighted)
#        originalCtrl = wx.CheckBox(panel, -1, self.text.original)
#        originalCtrl.SetValue(original)
        counterCtrl = wx.CheckBox(panel, -1, self.text.counter)
        counterCtrl.SetValue(arrayInfo[4])
        lastplayedCtrl = wx.CheckBox(panel, -1, self.text.lastplayed)
        lastplayedCtrl.SetValue(arrayInfo[5])
        filesizeCtrl = wx.CheckBox(panel, -1, self.text.filesize)
        filesizeCtrl.SetValue(arrayInfo[6])
        VBRCtrl = wx.CheckBox(panel, -1, self.text.VBR)
        VBRCtrl.SetValue(arrayInfo[7])
        levelingCtrl = wx.CheckBox(panel, -1, self.text.leveling)
        levelingCtrl.SetValue(arrayInfo[8])

        panel.AddCtrl(lengthCtrl)
        panel.AddCtrl(bitrateCtrl)
#        panel.AddCtrl(seekableCtrl)
        panel.AddCtrl(frequencyCtrl)
        panel.AddCtrl(stereoCtrl)
#        panel.AddCtrl(copyrightedCtrl)
#        panel.AddCtrl(originalCtrl)
        panel.AddCtrl(counterCtrl)
        panel.AddCtrl(lastplayedCtrl)
        panel.AddCtrl(filesizeCtrl)
        panel.AddCtrl(VBRCtrl)
        panel.AddCtrl(levelingCtrl)

        while panel.Affirmed():
            arrayInfo=[
                lengthCtrl.GetValue(),
                bitrateCtrl.GetValue(),
#                seekableCtrl.GetValue(),
                frequencyCtrl.GetValue(),
                stereoCtrl.GetValue(),
#                copyrightedCtrl.GetValue(),
#                originalCtrl.GetValue(),
                counterCtrl.GetValue(),
                lastplayedCtrl.GetValue(),
                filesizeCtrl.GetValue(),
                VBRCtrl.GetValue(),
                levelingCtrl.GetValue(),
            ]
            panel.SetResult(arrayInfo)



#====================================================================
class GetUniversal(eg.ActionClass):
    name = "Get Universal"
    description = "Get Universal."
    class text:
        label="Select requested property:"
        get = "Get "
        class Properties:
            AlbumName = "Album Name"
            AlbumLength = "AlbumLength"
            AlbumLengthString = "Album Length String"
            AlbumArtistName = "Album Artist Name"
            AlbumArtCount = "Album Art Count"
            ArtistName = "Artist Name"
            ArtistCount = "Artist Count"
            Author = "Author"
            Band = "Band"
            Bitrate = "Bitrate"
            BPM = "BPM"
            Comment = "Comment"
            Conductor = "Conductor"
            Copyright = "Copyright"
            Custom1 = "Custom 1"
            Custom2 = "Custom 2"
            Custom3 = "Custom 3"
            DateAdded = "Date Added"
            Encoder = "Encoder"
            FileLength = "File Length"
            FileModified = "File Modified"
            Genre = "Genre"
            Channels = "Stereo"
            InvolvedPeople = "Involved People"
            IsntInDB = "Is not in DB"
            ISRC = "ISRC"
            LastPlayed = "Last Played"
            Leveling = "Leveling"
            Lyricist = "Lyricist"
            Lyrics = "Lyrics"
            MediaDriveLetter = "Media Drive Letter"
            MediaDriveType = "Media Drive Type"
            MediaSerialNumber = "Media Serial Number"
            MediaLabel = "Media Label"
            Mood = "Mood"
            MusicComposer = "Music Composer"
            Occasion = "Occasion"
            OriginalArtist = "Original Artist"
            OriginalLyricist = "Original Lyricist"
            OriginalTitle = "Original Title"
            OriginalYear = "Original Year"
            Path = "Path"
            PeakValue = "Peak Value"
            PlayCounter = "Play Counter"
            PlaylistOrder = "Playlist Order"
            PreviewPath = "Preview Path"
            Preview = "Preview"
            Publisher = "Publisher"
            Quality = "Quality"
            Rating = "Rating"
            RatingString = "Rating String"
            SampleRate = "Sample Rate"
            SongLength = "Song Length"
            SongLengthString = "Song Length String"
            Tempo = "Tempo"
            Title = "Title"
            TrackOrder = "Track Order"
            VBR = "VBR"
            Year = "Year"
    def __init__(self):
        text=self.text
        txt=text.Properties
        self.infoList=(
            ("AlbumName",txt.AlbumName),
            ("Album.AlbumLength",txt.AlbumLength),
            ("Album.AlbumLengthString",txt.AlbumLengthString),
            ("AlbumArtistName",txt.AlbumArtistName),
            ("AlbumArt.Count",txt.AlbumArtCount),
            ("ArtistName",txt.ArtistName),
            ("Artist.Count",txt.ArtistCount),
            ("Author",txt.Author),
            ("Band",txt.Band),
            ("Bitrate",txt.Bitrate),
            ("BPM",txt.BPM),
            ("Comment",txt.Comment),
            ("Conductor",txt.Conductor),
            ("Copyright",txt.Copyright),
            ("Custom1",txt.Custom1),
            ("Custom2",txt.Custom2),
            ("Custom3",txt.Custom3),
            ("DateAdded",txt.DateAdded),
            ("Encoder",txt.Encoder),
            ("FileLength",txt.FileLength),
            ("FileModified",txt.FileModified),
            ("Genre",txt.Genre),
            ("Channels",txt.Channels),
            ("InvolvedPeople",txt.InvolvedPeople),
            ("IsntInDB",txt.IsntInDB),
            ("ISRC",txt.ISRC),
            ("LastPlayed",txt.LastPlayed),
            ("Leveling",txt.Leveling),
            ("Lyricist",txt.Lyricist),
            ("Lyrics",txt.Lyrics),
            ("Media.DriveLetter",txt.MediaDriveLetter),
            ("Media.DriveType",txt.MediaDriveType),
            ("Media.SerialNumber",txt.MediaSerialNumber),
            ("MediaLabel",txt.MediaLabel),
            ("Mood",txt.Mood),
            ("MusicComposer",txt.MusicComposer),
            ("Occasion",txt.Occasion),
            ("OriginalArtist",txt.OriginalArtist),
            ("OriginalLyricist",txt.OriginalLyricist),
            ("OriginalTitle",txt.OriginalTitle),
            ("OriginalYear",txt.OriginalYear),
            ("Path",txt.Path),
            ("PeakValue",txt.PeakValue),
            ("PlayCounter",txt.PlayCounter),
            ("PlaylistOrder",txt.PlaylistOrder),
            ("PreviewPath",txt.PreviewPath),
            ("Preview",txt.Preview),
            ("Publisher",txt.Publisher),
            ("Quality",txt.Quality),
            ("Rating",txt.Rating),
            ("RatingString",txt.RatingString),
            ("SampleRate",txt.SampleRate),
            ("SongLength",txt.SongLength),
            ("SongLengthString",txt.SongLengthString),
            ("Tempo",txt.Tempo),
            ("Title",txt.Title),
            ("TrackOrder",txt.TrackOrder),
            ("VBR",txt.VBR),
            ("Year",txt.Year),
        )
    def __call__(self, i):
        return self.plugin.getMM("Player.CurrentSong."+self.infoList[i][0])

    def GetLabel(self, i):
        return self.text.get+self.infoList[i][1]
        
    def Configure(self, i=0):
        #text=Text
        choices=[tpl[1] for tpl in self.infoList]
        panel=eg.ConfigPanel(self)
        panel.AddLabel(self.text.label)
        infoCtrl=wx.Choice(
            panel,
            choices=choices,
        )
        infoCtrl.SetSelection(i)
        panel.AddCtrl(infoCtrl)
        while panel.Affirmed():
            panel.SetResult(infoCtrl.GetSelection())


#====================================================================
class WritingToMM(eg.ActionClass):
    name = "Writing to database MM"
    description = "Writing some one parameters to database MediaMonkey."
    class text:
        label="Select requested property:"
        set = "Set "
        checkboxlabel = "Make entry to ID3 tag too"
        class Properties:
            Comment = "Comment"
            Custom1 = "Custom 1"
            Custom2 = "Custom 2"
            Custom3 = "Custom 3"
            Genre = "Genre"
            Mood = "Mood"
            Occasion = "Occasion"
            Quality = "Quality"
            Rating = "Rating"
            Tempo = "Tempo"
    def __init__(self):
        text=self.text
        txt=text.Properties
        self.listCtrl=(
            "wx.TextCtrl(panel, -1, arrayValue0[%s])",
            (
                "eg.SpinNumCtrl(panel,-1,arrayValue0[%s],max=100.0,min=0.0,"
                "fractionWidth=1,increment=10,style=wx.TE_READONLY)"
            )
        )
        self.infoList=(
            ("Tempo",txt.Tempo,0,False),
            ("Mood",txt.Mood,0,False),
            ("Occasion",txt.Occasion,0,False),
            ("Quality",txt.Quality,0,False),
            ("Custom1",txt.Custom1,0,False),
            ("Custom2",txt.Custom2,0,False),
            ("Custom3",txt.Custom3,0,False),
            ("Comment",txt.Comment,0,True),
            ("Genre",txt.Genre,0,True),
            ("Rating",txt.Rating,1,True),
        )
    def __call__(self, i, arrayValue0, arrayValue1):
        if self.infoList[i][2]==0:
            self.plugin.setMM("Player.CurrentSong."+self.infoList[i][0]\
                +'=u"'+arrayValue0[i]+'"')
        else:
            self.plugin.setMM("Player.CurrentSong."+self.infoList[i][0]\
                +"="+str(arrayValue0[i]))
        self.plugin.setMM("Player.CurrentSong.UpdateDB()")
        if arrayValue1[i]:
            self.plugin.setMM("Player.CurrentSong.WriteTags()")
        
    def GetLabel(self, i, arrayValue0, arrayValue1):
        if self.infoList[i][2]==0:
            result = self.text.set+self.infoList[i][1]+"="+arrayValue0[i]
        else:
            result = self.text.set+self.infoList[i][1]+"="+str(int(arrayValue0[i]))
        if arrayValue1[i]:
            result += " (+ID3)"
        return result
        

    def Configure(
        self,
        i=0,
        arrayValue0=[
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            50,
        ],
        arrayValue1 = [False] * 10
    ):
        #text=Text
        choices=[tpl[1] for tpl in self.infoList]
        panel = eg.ConfigPanel(self)
        choiceLbl=wx.StaticText(panel, -1, self.text.label)
        choiceCtrl=wx.Choice(
            panel,
            choices=choices,
        )
        choiceCtrl.SetSelection(i)
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        choiceSizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        choiceSizer.Add(choiceLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        choiceSizer.Add(choiceCtrl, 0, wx.EXPAND)
        mainSizer.Add(choiceSizer, 0, wx.EXPAND|wx.ALL, 10)
        dynSizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5) 
        mainSizer.Add(dynSizer, 0, wx.EXPAND|wx.BOTTOM, 10)        
        panel.sizer.Add(mainSizer)

        def onChoiceChange(event=None):
            dynSizer.Clear(True)
            dynLbl = wx.StaticText(
                panel,
                -1,
                self.infoList[choiceCtrl.GetSelection()][1]+":"
            )
            indx=self.infoList[choiceCtrl.GetSelection()][2]
            dummy = arrayValue0[0] # otherwise error:
# >>>  NameError: name 'arrayValue0' is not defined  <<<   ??????????????????????
            dynCtrl = eval(self.listCtrl[indx] % str(choiceCtrl.GetSelection()))
            dynSizer.Add(dynLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            dynSizer.Add(dynCtrl, 0, wx.EXPAND)
            if self.infoList[choiceCtrl.GetSelection()][3]:
                chkBoxCtrl = wx.CheckBox(panel, label=self.text.checkboxlabel)
                chkBoxCtrl.SetValue(arrayValue1[choiceCtrl.GetSelection()])
                dynSizer.Add((5,5))
                dynSizer.Add(chkBoxCtrl, 0, wx.EXPAND)
            mainSizer.Layout()
            if event:
                event.Skip()
        choiceCtrl.Bind(wx.EVT_CHOICE, onChoiceChange)
        onChoiceChange()
        while panel.Affirmed():
            arrayValue0[choiceCtrl.GetSelection()]=\
                dynSizer.GetChildren()[1].GetWindow().GetValue()
            if self.infoList[choiceCtrl.GetSelection()][3]:
                arrayValue1[choiceCtrl.GetSelection()]=\
                    dynSizer.GetChildren()[3].GetWindow().GetValue()
            panel.SetResult(choiceCtrl.GetSelection(),arrayValue0, arrayValue1 )

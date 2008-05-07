version="0.3.3" 

# Plugins/Billy/__init__.py
#
# Copyright (C)  2007 Pako  (lubos.ruckl@quick.cz)
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
#import eg

eg.RegisterPlugin(
    name = "Billy Player",
    author = "Pako",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control the <a href="http://www.sheepfriends.com/?page=billy">'
        'Billy</a> audio player. \n\n<p>'
        '<BR><B>ATTENTION !<BR>Properly works only for beta version 1.04b of Billy !</B>'
        '<BR>The plugin will work with older versions of Billy only in limited mode!</p>'
    ),
    createMacrosOnAdd = True,    
    url = "http://www.eventghost.org/forum/viewtopic.php?t=537",
    icon = (
        "R0lGODlhEAAQAPcAAAQCBMz+tPz+/AAAABkEFSEAAAAAAAAAAGECDR4AAAAAAAAAAAAADQAAABUA"
        "AAAAAA0AyAAAHgAAEAAAagAAXQIABAAAhQAAAwAAFwMAAAAAAAAAAIgBAeIAABIAAAAAAOkaGeUA"
        "AIEAAHwAAAAAEQAAAAEAAAAAAFYA0QAAOQAAJQAAW5AVhOEAABIAAAAAAHMViAAAFgAAKAAAW7AN"
        "FeIAABIAAAAAABgNTe4AAJAAAHwAAHDIlQUeOZEQJXxqW/9dYP8EQP+FOP8DAG0X/gUAEZEAHnwA"
        "AIUBUOcAQIEAOHwAAAAZ2wAAGhUAJQAAW1gR/AMA8gAAEgAAAHABEIUA9xkARQAAAIgHhEIAABUA"
        "AAAAAAAI/gAAEQAAHgAAAH4JhAAAAAAAAMAAAAAiAAAcAAABAACSAP8ATf8AAP8Awf8AAP+IBP/j"
        "AP8SAP8AAADQ4gA8BAAlAABbAABIcQBB1QA4NgAAfgBNAAAAABUAAAAAAMDBYOIAnhIAgAAAfNJI"
        "+ObkVIESFnwAAIhGAELQABUmAABbAEpIB+NBAIE4AHwAAMAFAHYAAFAAAAAAAIj+AEIRUAEeFgAA"
        "AGtQAABAAAA4AAAAAPyJAOFaABIAAAAAAADYAADjAAASAAAAAPiFAPcrABKDAAB8ABgAaO4AnpAA"
        "gHwAfHAA/wUA/5EA/3wA//8AYP8Anv8AgP8AfG0pIAW3AJGSAHx8AEr4IPRUAIAWAHwAAAA0SABk"
        "6xWDEgB8AAD//wD//wD//wD//4gAAEIAABUAAAAAAAC8BAHj5QASEgAAAAA0vgBkOwCDTAB8AFf4"
        "5PT35IASEnwAAOgYd+PuEBKQTwB8AIgAGEK35RWSEgB8ABH/NAD/ZAD/gwD/fAT4qABU5QAWEgAA"
        "AAM03gBk/wCD/wB8fwAAiADl5QASEgAAAADn+ABkVACDFgB8AASINABkZACDgwB8fAMB+AAAVAAA"
        "FgAAAAAxiQAAWgAAAAAAAAAAAAAAAAAAAAAAAAoA6QAAzgAARwAAACH5BAEAAAIALAAAAAAQABAA"
        "BwhEAAUIHEiwoMGDBgEoXMhQIUEAASJKnAjg4cSLASoOhIhRokaBHDtmtChy5MaSJkGi/CggZEeW"
        "LjHCXPmwoU2EOHMeDAgAOw=="
    ),
)


class Text:
    filemask = "Billy.exe|Billy.exe|All-Files (*.*)|*.*"
    label = "Path to Billy.exe:"
    title = "Written by Pako in accordance with some MonsterMagnet's and Bitmonster's plugins"
    version = "Version: "
    text1 = "Couldn't find Billy window !"
    grpName1 = "Main"
    grpName2 = "Playlist"
    grpName3 = "Extras"
    grpName4 = "Favorites"
    grpDescription1 = "Adds actions to main control Billy"
    grpDescription2 = "Adds actions to control of playlist Billy"
    grpDescription3 = "Adds extra actions to control Billy"
    grpDescription4 = "Adds actions to control Favorites of Billy"

    class Run:
        text2="Couldn't find file Billy.exe !"
 

#import wx

# Now import some other modules that are needed for the special purpose of this plugin.
import os
import win32api
from win32gui import GetWindowText

Actions = ((
    ("Play","Play","Play selected file.",u'{Enter}'),
    #("Pause","Pause","Pause.",u'{0}'),
    ("PausePlay","Pause/Play","Pause/Play.",u'{Space}'),
    ("Stop","Stop","Stop.",u'{0}{0}'),
    ("Next","Next","Next.",u'{Tab}'),
    ("Previous","Previous","Previous.",u'{Shift+Tab}'),
    ("ToStart","Jump to start","Jump to start of playing file.",u'{Backspace}'),
    #("SeekLeft","Seek Left","Seek in track left.",u'{Left}'),
    #("SeekRight","Seek Right","Seek in track Right.",u'{Right}'),
    #("SeekLeftBig","Seek Left Big","Seek 60s in track left.",u'{Ctrl+Left}'),
    #("SeekRightBig","Seek Right Big","Seek 60s in track Right.",u'{Ctrl+Right}'),
    #("VolumeUp","Volume Up","Volume Up.",u'{Add}'),
    #("VolumeDown","Volume Down","Volume Down.",u'{Subtract}'),
),(
    ("TogglePlayMode","Toggle play mode","Toggle play mode.",u'{F9}'),
    ("ToggleViewMode","Toggle view mode","Toggle layout list all.",u'{F8}'),
    ("OpenFolder","Open Folder","Open a dir with music files.",u'{F4}'), 
    ("AddFolder","Add Folder","Add a dir with music files.",u'{F3}'), 
    ("AddFile","Add File(s)","Add File(s).",u'{Ctrl+L}'), 
    ("AddURL","Add Internet radio stream","Add Internet radio stream.",u'{Ctrl+R}'), 
    ("OpenPlaylist","Open Playlist","Load Billy Playlist.",u'{Ctrl+O}'), 
    ("SavePlaylist","Save Playlist","Save Playlist.",u'{Ctrl+S}'), 
    #("MoveItemsUp","Move Items Up","Move Items Up.",u'{Ctrl+Up}'),
    #("MoveItemsDown","Move Items Down","Move Items Down.",u'{Ctrl+Down}'),
    #("SelectAll","Select All","Select All.",u'{Ctrl+A}'),
    ("Remove","Remove file from list","Remove file from list.",u'{Del}'),
    ("Delete","Delete file to recycle bin","Delete file to recycle bin.",u'{Shift+Del}'),
    ("ClearList","Clear list","Clear list.",u'{Ctrl+N}'),
    ("CheckNewFiles","Check for new files","Check for new files.",u'{F5}'),
    #("SelectPlayingItem","Select playing item","Select playing item.",u';'),
    ("Queue","Queue","Add selected file to Queue.",u'{Ins}'),
    ("CropQueued","Crop selected or queued items","Crop selected or queued items.",u'{Ctrl+Del}'),
    ("ClearHistory","Clear shuffle/queue history","Clear shuffle/queue history.",u'{Shift+Ctrl+C}'),
    #("RemoveMissing","Remove missing files from list","Remove missing files from list.",u'{Alt+Del}'),
    ("CutEntry","Cut playlist entry","Cut playlist entry.",u'{Ctrl+X}'),
    ("CopyEntry","Copy playlist entry","Copy playlist entry.",u'{Ctrl+C}'),
    ("PasteEntry","Paste playlist entry","Paste playlist entry.",u'{Ctrl+V}'),
    ("EditEntry","Edit playlist entry","Edit playlist entry.",u'{Shift+F2}'),
),(
    ("ExitBilly","Exit Billy","Exit Billy.",u'{Esc}'),
    ("Properties","Properties","Properties or multiple filename renamer (on multiple selection).",u'{F2}'),
    ("Explore","Explore","Open Explorer in file folder.",u'{Ctrl+E}'),
    ("Find","Find","Find file in active list.",u'{Ctrl+F}'),
    ("Record","Record Internet Radio","Record.",u'{Multiply}'),
    #("Restore","Restore","Maximize, Restore.",u'{F12}'),
    ("Minimize","Minimize to Tray","Minimize to tray.",u'{F11}'),
    #("SoftMute","Soft Mute","Soft mute (30% of volume).",u'{Pause}'),
    #("ExploreApplPath","Explore Billy Directory","Explore from Billy Directory.",u'{Alt+Ctrl+E}'),
    ("ResetMixer","Reset Windows Mixer","Reset Windows Mixer.",u'{Ctrl+Space}'),
    #("PlayingLength","Playing Length","Calculate total playlist time.",u'{Ctrl+Alt+T}'),
    #("SleepTimer","Sleep Timer","Sleep Timer.",u'{Alt+T}'),
    ("Settings","Settings","Settings menu Billy.",u'{F6}'),
),(
    ("AddPlistToFav","Add playlist to favorites","Add playlist to favorites.",u'{Ctrl+D}'),
    ("OrganizeFav","Organize favorites","Organize favorites.",u'{Ctrl+B}'),
    ("LoadFav1","Load Favorite 1","Load Favorite playlist 1.",u'{Ctrl+1}'),
    ("LoadFav2","Load Favorite 2","Load Favorite playlist 2.",u'{Ctrl+2}'),
    ("LoadFav3","Load Favorite 3","Load Favorite playlist 3.",u'{Ctrl+3}'),
    ("LoadFav4","Load Favorite 4","Load Favorite playlist 4.",u'{Ctrl+4}'),
    ("LoadFav5","Load Favorite 5","Load Favorite playlist 5.",u'{Ctrl+5}'),
    ("LoadFav6","Load Favorite 6","Load Favorite playlist 6.",u'{Ctrl+6}'),
    ("LoadFav7","Load Favorite 7","Load Favorite playlist 7.",u'{Ctrl+7}'),
    ("LoadFav8","Load Favorite 8","Load Favorite playlist 8.",u'{Ctrl+8}'),
    ("LoadFav9","Load Favorite 9","Load Favorite playlist 9.",u'{Ctrl+9}'),
))

FindBilly = eg.WindowMatcher(u'Billy.exe', u'{*}Billy{*}', u'TAppBilly', None, None, 1, True, 0.0, 0)

# Now we can start to define the plugin by subclassing eg.PluginClass
class Billy(eg.PluginClass):
    text=Text
    BillyPath = None
    
    def __init__(self):
        text=Text
        self.GroupNames = (
            self.text.grpName1,
            self.text.grpName2,
            self.text.grpName3,
            self.text.grpName4,
        )    
        self.GroupDescr = (
            self.text.grpDescription1,
            self.text.grpDescription2,
            self.text.grpDescription3,
            self.text.grpDescription4,
        )

        self.AddAction(Run)
        self.AddAction(GetPlayingFile)
        BillyPath = ""
        
        # And now begins the tricky part. We will loop through every tuple in
        # our list to get the needed values.
        for grpTuple,grpName,grpDescr in zip(Actions,self.GroupNames,self.GroupDescr):
            group=self.AddGroup(grpName, grpDescr)
            for tmpClassName, tmpName, tmpDescription, tmpHotKey in grpTuple:
                # Then we will create a subclass of eg.ActionClass on every
                # iteration and assign the values to the class-variables.
                class tmpActionClass(eg.ActionClass):
                    name = tmpName
                    description = tmpDescription
                    HotKey=tmpHotKey
                    # Every action needs a workhorse.
                    def __call__(self):
                        hwnds = FindBilly()
                        if len(hwnds) != 0:
                            eg.SendKeys(hwnds[0], self.HotKey, False)
                        else:
                            self.PrintError(self.plugin.text.text1)
                        return

                # We also have to change the classname of the action to a unique
                # value, otherwise we would overwrite our newly created action
                # on the next iteration.
                tmpActionClass.__name__ = tmpClassName
                # Finally we cann add the new ActionClass to our plugin
                group.AddAction(tmpActionClass)

    def __start__(self, BillyPath=None):
        self.BillyPath = BillyPath    
                     
    def Configure(self, BillyPath=None):
        if BillyPath is None:
            BillyPath = os.path.join(
                eg.folderPath.ProgramFiles, 
                "Billy", 
                "Billy.exe"
            )
        panel = eg.ConfigPanel(self)
        TitleText = wx.StaticText(panel, -1, self.text.title, style=wx.ALIGN_LEFT)
        VersionText = wx.StaticText(panel, -1, self.text.version+version, style=wx.ALIGN_LEFT)
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            size=(320,-1),
            initialValue=BillyPath, 
            startDirectory=eg.folderPath.ProgramFiles,
            fileMask = self.text.filemask,
            buttonText=eg.text.General.browse
        )
        panel.sizer.Add(TitleText, 0, wx.EXPAND)
        panel.sizer.Add(VersionText, 0, wx.EXPAND)
        panel.sizer.Add((5, 20))
        panel.AddLabel(self.text.label)
        panel.AddCtrl(filepathCtrl)
        
        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue())

class Run(eg.ActionClass):
    name = "Run or Restore"
    description = "Run Billy with its default settings or restore window."
    
    def __call__(self):
        try:
            head, tail = os.path.split(self.plugin.BillyPath)
            return win32api.ShellExecute(
                0, 
                None, 
                tail,
                None, 
                head, 
                1
            )
        except:
            # Some error-checking is always fine.
            self.PrintError(self.text.text2)
         
# new since 0.3.3:
class GetPlayingFile(eg.ActionClass):
    name = "Get Currently Playing File"
    description = "Gets the name of currently playing file."
    
    def __call__(self):
        strBillyTitle = ""
        hwnds = FindBilly()
        if ( hwnds is not None ):
            strBillyTitle = GetWindowText(hwnds[0])
            strBillyTitle = strBillyTitle.replace(" - Billy", "")
        return strBillyTitle        
        

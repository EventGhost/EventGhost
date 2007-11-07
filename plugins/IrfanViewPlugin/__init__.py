version="0.1.0" 

# Plugins/IrfanView/__init__.py
#
# Copyright (C)  2007 Pako  <lubos.ruckl@quick.cz>
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


import eg

eg.RegisterPlugin(
    name = "IrfanView",
    author = "Pako",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control <a href="http://www.irfanview.com/">'
        'IrfanView</a>. \n\n<P>'
        '<BR><B>Full variant:</B> Contains whole list (99) of Hotkeys.'
        '<BR><B>Light variant:</B> Selection only some one (23) Hotkeys.'
        '<BR>To choice full or light variant you must replace'
        ' the file IrfanViewSet.py in folder EventGhost\plugins\IrfanView.'
    ),
    createMacrosOnAdd = True,    
    icon = (
        "R0lGODlhEAAQAPcAAAQCBISChIQCBMTCxPwCBPz+/AAAAAAAAHoDFR0AAAAAAAAAAAAEFQ"
        "AAABUAAAAAAA0CDQAAAAAAAAAAAAAADQIAAAAAAAAAAAAABAEADwAAEAAABygArukABBIA"
        "hQAAA+kAF+UAAIEAAHwAAAABAQAAAAEAAAAAAFYaGQAAAAAAAAAAADAAEegAABIAAAAAAH"
        "MA0QAAOQAAJQAAW1AVhOkAABIAAAAAABgViO4AFpAAKHwAW3ANFQUAAJEAAHwAAP8NG/8A"
        "AP8AAP8AAG0ElQUPOZEQJXwHW4WuCOcEP4GFOHwDAAAXpgAAExUAEgAAAFgB+AMAPgAAOA"
        "AAAPAZ274AGhgAJQAAW8gRDC4A9xsAEgAAAAABIAAAIAAARgAAAH4HhAAAAAAAAMAAAAAI"
        "pgAAEwAAEgAAAP8JhP8AAP8AAP8AAP8BAP8AAP8AAP8CAAABGwAAAAAAHwAAAAAwBADqAA"
        "ASAAAAAADQ4gA8BBUlAABbAGDwYOk/nhI4gAAAfNIbQOYAXIEAGHwAAMgfAC4AABsAAAAA"
        "AErwB+PqAIESAHwAAKBGAHfQAFAmAABbAMjwAC4/UAE4GAAAAGsFAAAAAAAAAAAAAJxrAO"
        "hZABIAAAAAAAB4AADqAAASAAAAAAiFAPwrABKDAAB8ABgAaO4AnpAAgHwAfHAA/wUA/5EA"
        "/3wA//8AYP8Anv8AgP8AfG0pKgW3AJGSAHx8AEpAKvRcAIAYAHwAAAA0WABk8RWDEgB8AA"
        "D//wD//wD//wD//8gAAC4AABsAAAAAAABcpAHq6wASEgAAAAA09gBkOACDTAB8AFcIhPT8"
        "64ASEnwAAIgYd+ruEBKQTwB8AMgAuC636xuSEgB8AKD/NAD/ZAD/gwD/fB9AWgBc7AAYEg"
        "AAABE01ABk/wCD/wB8fwSgMADr7AASEgAAAAPnQABkXACDGAB8AACINABkZACDgwB8fAAB"
        "QAAAXAAAGAAAAAQxawAAWQAAAAAAAAMBAAAAAAAAAAAAAAAajQAA4gAARwAAACH5BAEAAA"
        "UALAAAAAAQABAABwhqAAsIFDiAYICBAxIOLEDgIIGHBQtElCiwocSHEhUKDNAQQICCFiNO"
        "FBAAAMSGGhcyfMiSQMGJCFuyVFng4EqZDz9+xMnzZM+cAyx+lMhRJkyKII3SfBkUY9CiFB"
        "diHMjx5cKmNq/CxEozIAA7"
    ),
)


class Text:
    filemask = "i_view32.exe|i_view32.exe|All-Files (*.*)|*.*"
    label = "Path to i_view32.exe:"
    title = "Written by Pako on base MonsterMagnet's and Bitmonster's plugins"
    version = "Version: "
    text1 = "Couldn't find IrfanView window !"
    grpName1 = "File"
    grpName2 = "Edit"
    grpName3 = "Picture"
    grpName4 = "Settings"
    grpName5 = "View"
    grpName6 = "Other"
    grpDescription1 = "Adds File menu to control IrfanView"
    grpDescription2 = "Adds Edit menu to control IrfanView"
    grpDescription3 = "Adds Picture menu to control IrfanView"
    grpDescription4 = "Adds Settings menu to control IrfanView"
    grpDescription5 = "Adds View menu to control IrfanView"
    grpDescription6 = "Adds other actions to control IrfanView"
    class Run:
        text2="Couldn't find file i_view32.exe !"
        
import wx
import os
import _winreg
import win32api
from IrfanViewSet import Actions

# Now we can start to define the plugin by subclassing eg.PluginClass
class IrfanView(eg.PluginClass):
    text=Text
    IrfanViewPath = None
    
    def __init__(self):
        self.AddAction(Run)
        self.AddAction(Exit)
        IrfanViewPath = ""
        
        i=0
        for grpTuple in Actions[1]:
            if Actions[0]=="Full":
                i+=1
                group=eval (
                    "self.AddGroup(self.text.grpName"+str(i)\
                    +", self.text.grpDescription"+str(i)+")"
                )
            # And now begins the tricky part. We will loop through
            # every tuple in our list to get the needed values.
            for tmpClassName, tmpName, tmpDescription, tmpHotKey in grpTuple:
                # Then we will create a subclass of eg.ActionClass on every
                # iteration and assign the values to the class-variables.
                class tmpActionClass(eg.ActionClass):
                    name = tmpName
                    description = tmpDescription
                    # Every action needs a workhorse.
                    def __call__(self):
                        handle = self.plugin.FindIrfanView()
                        if len(handle) != 0:
                            eg.plugins.Window.SendKeys(tmpHotKey, False)
                        else:
                            self.PrintError(self.plugin.text.text1)
                        return

                # We also have to change the classname of the action to a unique
                # value, otherwise we would overwrite our newly created action
                # on the next iteration.
                tmpActionClass.__name__ = tmpClassName
                # Finally we cann add the new ActionClass to our plugin
                if Actions[0]=="Full":
                    group.AddAction(tmpActionClass)
                else:
                    self.AddAction(tmpActionClass)
        del i
        
        
    def __start__(self, IrfanViewPath=None):
        self.IrfanViewPath = IrfanViewPath
        self.FindIrfanView=eg.plugins.Window.FindWindow.Compile(
            u'i_view32.exe', None, u'IrfanView', None, None, 1, False, 1.0, 0
        )                 


    def Configure(self, IrfanViewPath=None):
        if IrfanViewPath is None:
            IrfanViewPath = self.GetIrfanViewPath()
            if IrfanViewPath is None:
                IrfanViewPath = os.path.join(
                    eg.PROGRAMFILES, 
                    "IrfanView", 
                    "i_view32.exe"
                )
        dialog = eg.ConfigurationDialog(self)
        TitleText = wx.StaticText(
            dialog, -1, self.text.title, style=wx.ALIGN_LEFT
        )
        VersionText = wx.StaticText(
            dialog, -1, self.text.version+version\
            +"  -  "+Actions[0], style=wx.ALIGN_LEFT
        )
        filepathCtrl = eg.FileBrowseButton(
            dialog, 
            size=(320,-1),
            initialValue=IrfanViewPath, 
            startDirectory=eg.PROGRAMFILES,
            fileMask = self.text.filemask,
            buttonText=eg.text.General.browse
        )
        dialog.sizer.Add(TitleText, 0, wx.EXPAND)
        dialog.sizer.Add((5, 5))
        dialog.sizer.Add(VersionText, 0, wx.EXPAND)
        dialog.sizer.Add((5, 20))
        dialog.AddLabel(self.text.label)
        dialog.AddCtrl(filepathCtrl)
        
        if dialog.AffirmedShowModal():
            return (filepathCtrl.GetValue(), )

    def GetIrfanViewPath(self):
        """
        Get the path of IrfanView's install-dir through querying the 
        Windows registry.        
        """

        try:
            iv_reg = _winreg.OpenKey(
                _winreg.HKEY_CLASSES_ROOT,
                "\\Applications\\i_view32.exe\\shell\\open\\command"
            )
            IrfanViewPath =_winreg.QueryValue(iv_reg, None)
            _winreg.CloseKey(iv_reg)
            IrfanViewPath=IrfanViewPath[:-5]
            IrfanViewPath=IrfanViewPath[1:-1]
        except WindowsError:
            IrfanViewPath = None
        return IrfanViewPath


class Run(eg.ActionClass):
    name = "Run"
    description = "Run IrfanView with its default settings."
    
    def __call__(self):
        try:
            head, tail = os.path.split(self.plugin.IrfanViewPath)
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


class Exit(eg.ActionClass):
    name = "Exit"
    description = "Exit."
    def __call__(self):
        handle = self.plugin.FindIrfanView()
        if len(handle) != 0:
            eg.plugins.Window.Close()
        else:
            self.PrintError(self.plugin.text.text1)
        return
         

# -*- coding: utf-8 -*-

version="0.0.1"

# plugins/SplashLite/__init__.py
#
# Copyright (C)  2010 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

eg.RegisterPlugin(
    name = "Splash Lite",
    author = "Pako",
    version = version,
    kind = "program",
    guid = "{95217A88-AB62-4193-90D7-791E78C28232}",
    description = """<rst>
Adds actions to control the `Splash Lite`_ - next generation player.

Play all your High Definition MPEG-2 and AVC/H.264 camcorder clips and movies,
incredibly fast, smooth and without problems.
You don't need any additional codecs.
Download, install, watch.
It takes about one second to start application and High Definition video playback !

`Splash Lite`_ is for home use free !

.. _Splash Lite: http://www.mirillis.com/splash.html
""",
    createMacrosOnAdd = True,
    #url = "http://www.eventghost.org/forum/viewtopic.php?t=XXXX",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4XiDAAADAFBMVEX+/v6zs7OEhIRy"
        "cnKTk5Oampujo6OLjIxbW1vLy8vDw8Pc3Nxra2tjY2NTU1NCQkI7OzvZ3uTW2uHT09Os"
        "rKx1dngyMjO1vMl0hKJsgbHR1t5LS0uTna1debui8vuCvPKxucZ8fHyttcJld5xmn+6p"
        "//+w//+O1vmOkZa7u7vFy9WAjaJQetmH5v6g/f+W+/9naGjf4uhcc6VbpvKH9P/O0deK"
        "lahJcMlj1/529P926v9kgMEqKiqapLRDXposg/NX2v9n5P9cgNS4yNUjIyOGjJhYa4s1"
        "g+skuf9Xi+JDREs4OkVFSVdBW7M1n/wnwf8ZuP53eXxNUFtQXY5Che01yf9mxft6g5hl"
        "ZWhPUmEkq/0ZxP881fxY5P9ccJcYGBo2OD6anah0doFmanoxg9MKpv4Ht/9Ka7MOERsm"
        "KjiVmKdrb4FYWmUuMD0MEikJJz0JVpxt+P9EdtoBAgQiJCssMkkbI0YbIjoXGigLmvwW"
        "p/5J4P88QlgrM1IPQHcX1vgVmf01O1UB/f4D6P1TVFomLlEVGzgJWaEWleYh+/1Na6o1"
        "Zsq5wMxfoc9dgr0THEMLFDkDCSQHiO2mw9Q/QUgDCBgGWIg/Za4CCzYHx/8Xh/clK0cM"
        "GUIOk+hTZ5zN0tsOdLRCbcgMVn4a6PspXtamrLgzNT0bYeUSefUE1/0MefV2iKYPousC"
        "V+kfMHckM3smOZMEhfYBQcEFF3MkPq7d6PIDLVUBJYkCFGcDHIcOK6hAWs3P5/jO2emf"
        "oKEEYrwQInxledSMnejW3PWu3vWCnrIFL2cfXs2Zo8u32u96xOQHP2sJPX0nlt96jamM"
        "v94TfboXgsYZcMUUUJIVQ3kXSYMVWaENeOFMdaTT2N95stpM2fEp1/U/ZYp+p81Cyukh"
        "h9hEY4arsbrCxMhhkbwxqeAPve9Ia5FrdYWjpqq2trhvfZBbaHlscn1+gYiSlZkAAAAA"
        "AAAAAAAAAAD///////////////////////////////////////////////8L6ENIAAAA"
        "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"
    ),
)

from win32gui import MessageBox
from time import sleep
from win32api import ShellExecute
from eg.WinApi.Dynamic import SendMessage
from os import path

WM_CLOSE = 16


FindSplash = eg.WindowMatcher(
    u'SplashLite.exe',
    None,
    u'DX_DISPLAY0',
    None,
    None,
    None,
    True,
    0.0,
    0
)
#===============================================================================

class MyDirBrowseButton(eg.DirBrowseButton):

    def GetTextCtrl(self):          #  now I can make build-in textCtrl non-editable !!!
        return self.textControl     #


class Text:
    label1 = "Path to SplashLite.exe:"
    text1 = "Couldn't find Splash Lite window !"
    text2 = "Couldn't find file %s !"
    browseTitle = "Selected folder:"
    toolTipFolder = "Press button and browse to select folder ..."
    boxTitle = "Message from EventGhost:"
    boxMessage1 = 'Folder "%s" is incorrect.\nMissing file %s !'
#===============================================================================

class SplashLite(eg.PluginBase):

    text=Text
    SplashPath = None

    def Execute(self, exe, path, param = None):
        try:
            ShellExecute(
                0,
                None,
                exe,
                param,
                path,
                1
            )
        except:
            self.PrintError(self.text.text2 % exe)


    def __init__(self):
        text=Text
        self.AddActionsFromList(ACTIONS)


    def __start__(self, SplashPath = None):
        self.SplashPath = SplashPath


    def Configure(self, SplashPath = None):
        panel = eg.ConfigPanel(self)
        labelText = wx.StaticText(panel, -1, self.text.label1)
        filepathCtrl = MyDirBrowseButton(
            panel,
            size=(410,-1),
            toolTip = self.text.toolTipFolder,
            dialogTitle = self.text.browseTitle,
            buttonText = eg.text.General.browse
        )
        filepathCtrl.GetTextCtrl().SetEditable(False)
        if SplashPath is None:
            SplashPath = eg.folderPath.ProgramFiles+'\\Splash Lite'
            filepathCtrl.SetValue("")
        else:
            filepathCtrl.SetValue(SplashPath)
        filepathCtrl.startDirectory = SplashPath
        sizerAdd = panel.sizer.Add
        sizerAdd(labelText, 0, wx.TOP,15)
        sizerAdd(filepathCtrl,0,wx.TOP,3)


        def OnPathChange(event = None):
            fPath = filepathCtrl.GetValue()
            flag = path.exists(fPath + "\\SplashLite.exe")
            panel.dialog.buttonRow.okButton.Enable(flag)
            panel.isDirty = True
            panel.dialog.buttonRow.applyButton.Enable(flag)
            if event and not flag:
                MessageBox(
                    panel.GetHandle(),
                    self.text.boxMessage1 % (fPath,'SplashLite.exe'),
                    self.text.boxTitle,
                        0
                    )
            if fPath != "":
                filepathCtrl.startDirectory = fPath
        filepathCtrl.Bind(wx.EVT_TEXT,OnPathChange)
        OnPathChange()

        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue(),)
#===============================================================================

class Run(eg.ActionBase):

    def __call__(self):
        self.plugin.Execute('SplashLite.exe',self.plugin.SplashPath)
#===============================================================================

class Exit(eg.ActionClass):
    def __call__(self):
        hwnds = FindSplash()
        if len(hwnds) != 0:
            SendMessage(hwnds[0], WM_CLOSE, 0, 0)
        else:
            self.PrintError(self.plugin.text.text1)
#===============================================================================

class HotKeyAction(eg.ActionBase):

    def __call__(self):
        hwnds = FindSplash()
        if len(hwnds) != 0:
            eg.SendKeys(hwnds[0], self.value, True)
        else:
            self.PrintError(self.plugin.text.text1)
#===============================================================================

class OpenFile(eg.ActionBase):

    class text:
        txtLabel = "File to be play:"


    def __call__(self,filePath = ""):
        hwnds = FindSplash()
        if len(hwnds) != 0:
            filePath = '"%s"' % eg.ParseString(filePath)
            self.plugin.Execute('SplashLite.exe',self.plugin.SplashPath, filePath)
        else:
            self.PrintError(self.plugin.text.text1)


    def Configure(self,filePath = ""):
        panel = eg.ConfigPanel(self)
        txtBoxLabel = wx.StaticText(panel, -1, self.text.txtLabel)
        filePathCtrl = wx.TextCtrl(panel,-1,filePath)
        panel.sizer.Add(txtBoxLabel,0,wx.TOP,15)
        panel.sizer.Add(filePathCtrl,0,wx.TOP|wx.EXPAND,5)
        while panel.Affirmed():
            panel.SetResult(
                filePathCtrl.GetValue(),)
#===============================================================================

ACTIONS = (
    (Run,"Run","Run","Run Splash Lite.", None),
    (Exit,"Exit","Exit","Exit Splash Lite.", None),
    (HotKeyAction,"PausePlay","Pause/Play","Pause/Play.",u'{Space}'),
    (HotKeyAction,"Stop","Stop","Stop.",'{S}'),
    (HotKeyAction,"Next","Next","Next.",u'{Down}'),
    (HotKeyAction,"Previous","Previous","Previous.",u'{Up}'),
    (HotKeyAction,"SeekLeft","Seek Left","Seek in track left.",u'{Left}'),
    (HotKeyAction,"SeekRight","Seek Right","Seek in track Right.",u'{Right}'),
    (HotKeyAction,"Fullscreen","Fullscreen","Fullscreen.",u'{Enter}'),
    (HotKeyAction,"Mute","Mute","Mute.",u'{M}'),
    (OpenFile,"OpenFile","Open File","Open File.",None),
)
#===============================================================================

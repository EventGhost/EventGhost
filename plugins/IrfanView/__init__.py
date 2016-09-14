# -*- coding: utf-8 -*-

version="0.2.5"

# plugins/IrfanView/__init__.py
#
# Copyright (C)  2007 Pako  <lubos.ruckl@quick.cz>
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.2.5 by Pako 2011-04-28 13:31 UTC+1
#     - Now can be file i_view32.ini also in RoamingAppData+"\\IrfanView\\"
#     - Added actions Scroll right and Scroll left

eg.RegisterPlugin(
    name = "IrfanView",
    author = "Pako",
    version = version,
    kind = "program",
    guid = "{9593B4E9-5089-4C1F-BCE5-4A0B07F63DEE}",
    description = (
        'Adds actions to control <a href="http://www.irfanview.com/">'
        'IrfanView</a>.'
    ),
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=579",
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
    text1 = "Couldn't find IrfanView window !"
    grpName1 = "File"
    grpName2 = "Edit"
    grpName3 = "Picture"
    grpName4 = "Settings"
    grpName5 = "View"
    grpName6 = "Other"
    grpDescription1 = "Adds File menu to control IrfanView."
    grpDescription2 = "Adds Edit menu to control IrfanView."
    grpDescription3 = "Adds Picture menu to control IrfanView."
    grpDescription4 = "Adds Settings menu to control IrfanView."
    grpDescription5 = "Adds View menu to control IrfanView."
    grpDescription6 = "Adds other actions to control IrfanView."
    err ="Couldn't find file i_view32.exe !"

    class RunDefault:
        text2="Couldn't find file i_view32.exe !"



import wx
import os
from ConfigParser import SafeConfigParser
#from shutil import copyfile
import _winreg
import win32api
import locale
from eg.WinApi.Utils import CloseHwnd
myEncoding = locale.getdefaultlocale()[1]

Actions =((#Tuple 0 - most important actions
    ("OpenDialog","Show open dialog","Show open dialog.",u'{O}'),
    ("ShowNextPgOrFile","Show next page OR file","Show next page in a multipage image OR load next file in directory.",u'{Ctrl+PgDown}'),
    ("ShowPrevPgOrFile","Show previous page OR file","Show previous page in a multipage image OR load previous file in directory.",u'{Ctrl+PgUp}'),
    ("ScrollRight","Scroll right","Scroll image right OR next image in directory.",u'{Right}'),
    ("ScrollLeft","Scroll left","Scroll image left OR previous image in directory.",u'{Left}'),
    ("LoadFirstFile","First file in directory","Load first file in the directory.",u'{Ctrl+Home}'),
    ("LoadLastFile","Last file in directory","Load last file in the directory.",u'{Ctrl+End}'),
    ("CloseActualWindow","Close actual window","Close actual window (main window, slideshow, full screen,thumbnails or a dialog).",u'{Esc}'),
    ("ToggleStatusBar","Show/hide status bar","Show/hide status bar.",u'{Alt+Shift+S}'),
    ("ToggleToolbar","Show/hide toolbar","Show/hide toolbar.",u'{Alt+Shift+T}'),
    ("ToggleMenuBar","Show/hide menu bar","Show/hide menu bar.",u'{Alt+Shift+M}'),
    ("ToggleCaption","Show/hide caption","Show/hide caption.",u'{Alt+Shift+C}'),
    ("ToggleFit","Fit to desktop/Fit to image","Switch (toggle) between 'Fit images to desktop' and 'Fit window to image'.",u'{F}'),
    ("ZoomIn","Zoom In","Zoom In.",u'{Add}'),
    ("ZoomOut","Zoom Out","Zoom Out.",u'{Subtract}'),
    ("OriginalSize","Original size","Original size (no zoom).",u'{Ctrl+H}'),
    ("FullScreen","Full Screen","Full Screen.",u'{Enter}'),
    ("FullScreenMode1","Full screen mode 1:1","Full screen mode: Show images/movies with the original size (1:1).",u'{1}'),
    ("FullScreenMode2","Large fit to full screen","Full screen mode: Fit to screen only large images.",u'{2}'),
    ("FullScreenMode3","All fit to full screen","Full screen mode: Fit to screen all images/movies.",u'{3}'),
    ("FullScreenMode4","All stretch to full screen","Full screen mode: Stretch all images/movies to screen.",u'{4}'),
    ("StartDirSlideshow","Start directory slideshow","Start slideshow with current directory files.",u'{Ctrl+W}'),
    ("ToggleAutSlideshow1","Start/stop automatic slideshow","Start/stop automatic viewing (slideshow in window).",u'{Shift+A}'),
    ("ToggleAutSlideshow2","Pause/Resume automatic slideshow","Pause an automatic slideshow. Press this key again to resume the slideshow.",u'{Pause}'),
    ("MinimizeWindow","Minimize IrfanView window","Minimize IrfanView window - Boss key ;-).",u'{M}'),
),(#Tuple 1 - File menu
    #("OpenDialog","Show Open dialog","Show Open dialog.",u'{O}'),
    ("ReopenFile","Reopen file","Reopen file.",u'{Shift+R}'),
    ("OpenInExternal","Open in external","Open in external viewer/editor.",u'{Shift+E}'),
    ("Thumbnails","Thumbnails","Thumbnails.",u'{T}'),
    ("SlideshowDialog","Show Slideshow dialog","Show Slideshow dialog.",u'{W}'),
    ("BatchConversionRename","Batch Conversion/Rename","Batch Conversion/Rename.",u'{B}'),
    ("RenameFile","Rename file","Rename file.",u'{F2}'),
    ("MoveFile","Move file","Move file.",u'{F7}'),
    ("CopyFile","Copy file","Copy file.",u'{F8}'),
    ("DeleteFile","Delete file","Delete file.",u'{Del}'),
    ("SaveDialog","Show Save dialog","Show Save dialog.",u'{Ctrl+S}'),
    ("SaveAs",'Show "Save as" dialog','Show "Save as" dialog.',u'{S}'),
    ("PrintDialog","Show Print dialog","Show Print dialog.",u'{Ctrl+P}'),
    ("DirectPrint","Direct print","Print image, hide print dialog (direct print).",u'{Ctrl+Alt+P}'),
    ("AcquireBatchScanning","Acquire/Batch Scanning","Acquire/Batch Scanning.",u'{Ctrl+Shift+A}'),
    #("CloseActualWindow","Close actual window","Close actual window (main window, slideshow, full screen, thumbnails or a dialog).",u'{Esc}'),
    ("SearchFiles","Search files","Search files.",u'{Ctrl+F}'),
),(#Tuple 2 - Edit menu
    ("EditUndo","Edit - Undo","Edit - Undo.",u'{Ctrl+Z}'),
    ("CreateSelection","Create custom selection","Create custom selection.",u'{Shift+C}'),
    ("InsertText","Insert text into selection","Edit - Insert text into selection.",u'{Ctrl+T}'),
    ("CutSelectionRectangle","Cut selection rectangle","Cut selection rectangle.",u'{Ctrl+X}'),
    ("CropSelectionRectangle","Crop selection rectangle","Crop selection rectangle.",u'{Ctrl+Y}'),
    ("CopyToClipboard","Copy image to clipboard","Copy image to clipboard.",u'{Ctrl+C}'),
#    ("PasteFromClipboard","Paste image from clipboard","Paste image from clipboard.",u'{Ins}'),
    ("PasteFromClipboard","Paste from clipboard","Paste image from clipboard.",u'{Ctrl+V}'),
    ("EditDelete","Delete (Clear display) ","Delete - clear display.",u'{D}'),
),(#Tuple 3 - Picture menu
    ("ShowInformation","Show image information","Show image information.",u'{I}'),
    ("RotateLeft","Rotate left","Rotate left.",u'{L}'),
    ("RotateRight","Rotate right","Rotate right.",u'{R}'),
    ("RotateAngle","User/Fine rotation","Rotate by angle.",u'{Ctrl+U}'),
    ("VerticalFlip","Vertical flip","Vertical flip.",u'{V}'),
    ("HorizontalFlip","Horizontal flip","Horizontal flip.",u'{H}'),
    ("ResampleDialog","Show Resample dialog","Show Resample dialog.",u'{Ctrl+R}'),
    ("EnhanceColors","Enhance colors","Enhance colors.",u'{Shift+G}'),
    ("AutoColorCorrection","Auto color correction","Auto color correction.",u'{Shift+U}'),
    ("Sharpen","Sharpen","Sharpen.",u'{Shift+S}'),
    ("RedEyeReduction","Red eye reduction","Red eye reduction.",u'{Shift+Y}'),
    ("EffectsSetup","Effects setup","Effects setup.",u'{Ctrl+E}'),
    ("AdobeFiltersDialog","Adobe 8BF filters dialog","Adobe 8BF filters dialog.",u'{Ctrl+K}'),
    ("FilterFactoryDialog","Filter Factory dialog","Filter Factory dialog.",u'{K}'),
    ("RotationLeft","Lossless JPG rotation Left","Lossless JPG rotation - to left.",u'{Ctrl+Shift+L}'),
    ("RotationRight","Lossless JPG rotation right","Lossless JPG rotation - to right.",u'{Ctrl+Shift+R}'),
),(#Tuple 4 - Settings menu
    ("PropertiesDialog","Show Properties dialog","Show Properties dialog.",u'{P}'),
    ("StopAnimation","Stop animation","Stop GIF or ANI animation.",u'{G}'),
    ("ShowCommentDialog","Show Comment dialog JPGs","Show Comment dialog for JPGs.",u'{Ctrl+Shift+M}'),
    ("JpgLosslessOperations","JPG lossless operations","JPG lossless operations.",u'{Shift+J}'),
    ("CaptureDialog","Show Capture dialog","Show Capture dialog.",u'{C}'),
    #("MinimizeWindow","Minimize IrfanView window","Minimize IrfanView window - Boss key ;-).",u'{M}'),
    ("WallpaperCentered","Wallpaper centered","Set as wallpaper - centered.",u'{Ctrl+Shift+C}'),
    ("WallpaperTiled","Wallpaper tiled","Set as wallpaper - tiled.",u'{Ctrl+Shift+T}'),
    ("WallpaperStretched","Wallpaper stretched","Set as wallpaper - stretched.",u'{Ctrl+Shift+S}'),
    ("PreviousWallpaper","Previous wallpaper","Set as wallpaper - previous wallpaper.",u'{Ctrl+Shift+P}'),
),(#Tuple 5 - View menu
    #("ToggleStatusBar","Show/hide status bar","Show/hide status bar.",u'{Alt+Shift+S}'),
    #("ToggleToolbar","Show/hide toolbar","Show/hide toolbar.",u'{Alt+Shift+T}'),
    #("ToggleMenuBar","Show/hide menu bar","Show/hide menu bar.",u'{Alt+Shift+M}'),
    #("ToggleCaption","Show/hide caption","Show/hide caption.",u'{Alt+Shift+C}'),
    #("ToggleFit","Fit to desktop/Fit to image","Switch (toggle) between 'Fit images to desktop' and 'Fit window to image'.",u'{F}'),
    #("FullScreen","Full Screen","Full Screen.",u'{Enter}'),
    #("FullScreenMode1","Full screen mode 1:1","Full screen mode: Show images/movies with the original size (1:1).",u'{1}'),
    #("FullScreenMode2","Large fit to full screen","Full screen mode: Fit to screen: large images only.",u'{2}'),
    #("FullScreenMode3","All fit to full screen","Full screen mode: Fit to screen: all images/movies.",u'{3}'),
    #("FullScreenMode4","All stretch to full screen","Full screen mode: Stretch all images/movies to screen.",u'{4}'),
    ("LoadNextFile","Next file in directory","Load next file in directory.",u'{Space}'),
    ("LoadPrevFile","Previous file in directory","Load previous file in directory.",u'{Backspace}'),
    #("LoadFirstFile","Load first file","Load first file in the directory.",u'{Ctrl+Home}'),
    #("LoadLastFile","Load last file","Load last file in the directory.",u'{Ctrl+End}'),
    ("OpenRandomImage","Open random image","Open random image from the directory.",u'{Ctrl+M}'),
    ("Refresh","Refresh","Refresh (display and directory list).",u'{F5}'),
    #("ToggleAutSlideshow1","Start/stop automatic slideshow","Start/stop automatic viewing (slideshow in window).",u'{Shift+A}'),
    #("ZoomIn","Zoom In","Zoom In.",u'{Add}'),
    #("ZoomOut","Zoom Out","Zoom Out.",u'{Subtract}'),
    ("ToggleLockZoom","Lock/unlock zoom","Lock/unlock zoom (also in full screen mode).",u'{Shift+L}'),
    #("OriginalSize","Original size","Original size (no zoom).",u'{Ctrl+H}'),
    ("ShowInHexViewer","Show in HEX viewer","Show image in HEX viewer.",u'{F3}'),
    ("EditMultipageTif","Edit multipage TIF","Edit multipage TIF.",u'{Ctrl+Q}'),
    #("ShowNextPgOrFile","Show next page OR file","Show next page in a multipage image OR load next file in directory.",u'{Ctrl+PgDown}'),
    #("ShowPrevPgOrFile","Show previous page OR file","Show previous page in a multipage image OR load previous file in directory.",u'{Ctrl+PgUp}'),
    ("ScrollImageUp","Scroll image up","Scroll image up.",u'{Up}'),
    ("ScrollImageDown","Scroll image down","Scroll image down.",u'{Down}'),
    ("ScrollRightOrNext","Scroll right OR next image","Scroll image right OR next image in directory.",u'{Right}'),
    ("ScrollLeftOrPrevious","Scroll left OR previous","Scroll image left OR previous image in directory.",u'{Left}'),
    ("ScrollUpOrPrevious","Scroll up OR previous file","Load previous file in directory OR scroll image up.",u'{PgUp}'),
    ("ScrollDownOrNext","Scroll down OR next file","Load next file in directory OR scroll image down.",u'{PgDown}'),
    ("ScrollToBeginOrFirstFile","Scroll to begin OR load first file","Scroll to begin (horizontal scroll) OR load first file in directory.",u'{Home}'),
    ("ScrollToEndOrLastFile","Scroll to end OR load last file","Scroll to end (horizontal scroll) OR load last file in directory.",u'{End}'),
),(#Tuple 6 - other actions
    #("ToggleAutSlideshow2","Pause/Resume automatic slideshow","Pause an automatic slideshow. Press this key again to resume the slideshow.",u'{Pause}'),
    ("AppendToSlideshow","Append to current slideshow","Append current file to current slideshow.",u'{F4}'),
    ("ToggleSlideshow","Fullscreen/Slideshow text display","Toggle fullscreen/slideshow text display.",u'{N}'),
    #("StartDirSlideshow","Start directory slideshow","Start slideshow with current directory files.",u'{Ctrl+W}'),
    ("ShowExifDialog","Show EXIF dialog","Show EXIF dialog for JPGs with available EXIF data.",u'{E}'),
    ("ControlSwitchThumb","Control switch in thumbnail window","Control switch in the thumbnail window.",u'{Ctrl+Tab}'),
    ("SwitchMainThumbnail","Switch main/thumbnail window","Switch between main and thumbnail window (if visible).",u'{Tab}'),
    ("SelectAllThumb","Select all thumbnails","Select all thumbnails (thumbnail window).",u'{Ctrl+A}'),
    ("OpenBrowseDialog",'Show "Browse-Subfolders" dialog.','Show "Browse-Subfolders" dialog.',u'{Ctrl+B}'),
    ("ShowIptcDialog","Show IPTC dialog","Show IPTC dialog for JPGs.",u'{Ctrl+I}'),
    ("SendByMail","Send image by email","Send image by email.",u'{Shift+M}'),
    ("CopyFilename","Copy filename to clipboard","Copy current filename to clipboard.",u'{Shift+P}'),
    ("JumpIntoToolbar","Jump into toolbar edit field","Jump into the toolbar edit field.",u'{Shift+T}'),
    ("Help","Help","Help.",u'{F1}'),
    ("AboutIrfanView",'Show "About IrfanView" dialog','Show "About IrfanView" dialog.',u'{A}'),
))

FindIrfanView = eg.WindowMatcher(
    u'i_view32.exe', None, u'IrfanView', None, None, 1, False, 0.0, 0
)

class IrfanView(eg.PluginClass):
    text=Text
    IrfanViewPath = None

    def OpenHelpPage(self,html_page):
        try:
            head, tail = os.path.split(self.IrfanViewPath)
            return win32api.ShellExecute(
                0,
                None,
                "hh.exe",
                ('mk:@MSITStore:'+head+'\i_view32.chm::/'\
                +html_page).encode(myEncoding),
                os.environ['SYSTEMROOT'],
                1
            )
        except:
            self.PrintError(self.text.err)

    def __init__(self):
        self.AddAction(RunDefault)
        self.AddAction(RunCommandLine)
        self.AddAction(RunSlideshow)
        self.AddAction(RunWithOptions)
        self.AddAction(Exit)
        IrfanViewPath = ""

        i=0
        for grpTuple in Actions:
            if i>0:
                group=eval (
                    "self.AddGroup(self.text.grpName"+str(i)\
                    +", self.text.grpDescription"+str(i)+")"
                )
            for tmpClassName, tmpName, tmpDescription, tmpHotKey in grpTuple:
                class tmpActionClass(eg.ActionClass):
                    name = tmpName
                    description = tmpDescription
                    hotKey = tmpHotKey
                    def __call__(self):
                        hwnds = FindIrfanView()
                        if len(hwnds) != 0:
                            eg.SendKeys(hwnds[0], self.hotKey, False)
                        else:
                            self.PrintError(self.plugin.text.text1)
                        return
                tmpActionClass.__name__ = tmpClassName
                if i>0:
                    group.AddAction(tmpActionClass)
                else:
                    self.AddAction(tmpActionClass)
            i+=1

    def __start__(self, IrfanViewPath=None):
        self.IrfanViewPath = IrfanViewPath

    def Configure(self, IrfanViewPath=None):
        if IrfanViewPath is None:
            IrfanViewPath = self.GetIrfanViewPath()
            if IrfanViewPath is None:
                IrfanViewPath = os.path.join(
                    eg.folderPath.ProgramFiles,
                    "IrfanView",
                    "i_view32.exe"
                )
        panel = eg.ConfigPanel(self)
        filepathCtrl = eg.FileBrowseButton(
            panel,
            size=(320,-1),
            initialValue=IrfanViewPath,
            startDirectory=eg.folderPath.ProgramFiles,
            fileMask = self.text.filemask,
            buttonText=eg.text.General.browse
        )
        panel.sizer.Add((5, 20))
        panel.AddLabel(self.text.label)
        panel.AddCtrl(filepathCtrl)

        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue())

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


class RunDefault(eg.ActionClass):
    name = "Run default"
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
            self.PrintError(self.text.text2)

class RunCommandLine(eg.ActionClass):
    name = "Run with command line"
    description = "Run IrfanView with command line options."
    class text:
        err ="Couldn't find file i_view32.exe !"
        cmdline="Enter command line options:"
        label="Label for this action:"
        help = "Help"
    def __call__(self,label,cmdline):
        try:
            head, tail = os.path.split(self.plugin.IrfanViewPath)
            return win32api.ShellExecute(
                0,
                None,
                tail,
                cmdline.encode(myEncoding),
                head,
                1
            )
        except:
            self.PrintError(self.text.err)

    def GetLabel(self,label,cmdline):
        return "Run command line "+label

    def Configure(self,label="",cmdline=""):
        panel = eg.ConfigPanel(self)
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        cmdlineLbl=wx.StaticText(panel, -1, self.text.cmdline)
        cmdlineCtrl=wx.TextCtrl(panel,-1,cmdline)
        cmdlineCtrl.SetMinSize((400,20))
        hlpbtnCtrl = wx.Button(panel, -1, self.text.help)
        def onBtnClick(event):
            self.plugin.OpenHelpPage('hlp_command_line.htm')
            event.Skip()
        hlpbtnCtrl.Bind(wx.EVT_BUTTON, onBtnClick, hlpbtnCtrl)
        labelLbl=wx.StaticText(panel, -1, self.text.label)
        labelCtrl=wx.TextCtrl(panel,-1,label)
        mainSizer.Add(cmdlineLbl,0,wx.TOP,20)
        mainSizer.Add(cmdlineCtrl,0,wx.EXPAND)
        mainSizer.Add(hlpbtnCtrl,0,wx.ALIGN_RIGHT|wx.TOP,8)
        mainSizer.Add(labelLbl,0,wx.ALIGN_RIGHT|wx.TOP,50)
        mainSizer.Add(labelCtrl,0,wx.ALIGN_RIGHT)
        panel.sizer.Add(mainSizer)
        while panel.Affirmed():
            panel.SetResult(labelCtrl.GetValue(),cmdlineCtrl.GetValue())


class RunSlideshow(eg.ActionClass):
    name = "Run slideshow"
    description = "Run IrfanView and start slideshow."
    defaults = {
        "label_": "",
        "width_": 800.0,
        "high_": 600.0,
        "delay_": 5.0,
        "filepath_": eg.folderPath.Pictures,
        "dirpath_": eg.folderPath.Pictures,
        "mode_": 1,
        "source_": 0,
        "fit_": 1,
        "progress_": 0,
        "loop_": False,
        "noRepeat_": False,
        "suppress_": True,
        "displText_": True,
        "soundLoop_": True,
        "resample_": True,
        "hideCursor_": True,
        "alpha_": True,
        "close_": True,
        "mon_": 1,
        "mask_": u"$D$F $X",
    }

    class text:
        err ="Couldn't find file i_view32.exe !"
        runslideshow = "Run slideshow "
        radioboxmode = "Mode of slideshow"
        modeFull = "Full screen"
        modeWin = "Centered window"
        radioboxsource = "Source of slideshow"
        folder = "Folder"
        txtFile = "Text file"
        radioboxfit = "Fit mode"
        mode1_1 = "Original size"
        onlyBig = "Fit only big"
        fitAll = "Fit all"
        scratchAll = "Scratch all"
        radioboxprogress = "Progress of pictures"
        autoDelay = "Automatic after DELAY seconds"
        autoKeyb = "Automatic after mouse/keyb input"
        randomDelay = "Random after DELAY seconds"
        randomKeyb = "Random after mouse/keyb input"
        windowSize = "Window size [pixels]"
        width = "Width:"
        high = "Height:"
        delay = "Delay [s]:"
        label = "Label for this slideshow:"
        loop = "Loop slideshow"
        noRepeat = "No file repeat"
        suppress = "Suppress errors during playing"
        displtext = "Show text (filename ...)"
        soundLoop = "Loop MP3 files (background music)"
        resample = 'Use "Resample" function (slower)'
        hideCursor = "Hide mouse cursor"
        alpha = "Use Alpha blending between images"
        close = "Close IrfanView after the last file"
        filepath = "Path to text file:"
        filemask = (
            "Text files (*.txt)|*.txt|List files (*.lst)|*.lst"
            "|All-Files (*.*)|*.*"
        )
        dirpath = "Path to folder:"
        toolTipFile = 'Type filename or click browse to choose file'
        browseTitle = "Selected folder:"
        toolTipFolder = "Type directory name or browse to select"
        monitor = "Monitor:"
        lineOpt="Command line option:"
        help = "Help"
        mask = 'Mask for "Show text":'

    def __call__(self, kwargs):
        options = self.defaults.copy()
        options.update(kwargs)
        head, tail = os.path.split(self.plugin.IrfanViewPath)
        cp = SafeConfigParser()
        cp.optionxform = str #Case sensitive !
        cp.read(head+"\\i_view32.ini")
        if cp.has_option('Others','INI_Folder'):
            INI_Folder = cp.get('Others','INI_Folder',True)
            if INI_Folder == '%APPDATA%\\IrfanView':
                INI_Folder = eg.folderPath.RoamingAppData+"\\IrfanView\\"
            cp.read(INI_Folder+"\\i_view32.ini")
        sec="Slideshow"
        if not cp.has_section(sec):
            cp.add_section(sec)
        cp.set(sec, "WindowW", str(int(options["width_"])))
        cp.set(sec, "WindowH", str(int(options["high_"])))
        cp.set(sec, "AutoDelay", str(options["delay_"]))
        cp.set(sec, "RandomDelay", str(options["delay_"]))
        cp.set(sec, "PlayInWindow", str(options["mode_"]))
        cp.set(sec, "Advancement", str(options["progress_"]+1))
        cp.set(sec, "Loop", str(int(options["loop_"])))
        cp.set(sec, "NoSameImageAgain", str(int(options["noRepeat_"])))
        cp.set(sec, "SuppressErrors", str(int(options["suppress_"])))
        cp.set(sec, "ShowFilename", str(int(options["displText_"])))
        cp.set(sec, "LoopAudio", str(int(options["soundLoop_"])))
        cp.set(sec, "HideCursor", str(int(options["hideCursor_"])))
        cp.set(sec,"StopAndClose",str(int(options["close_"])))
        if len(options["mask_"])>0:
            cp.set(sec, "Text", options["mask_"])
        sec="Viewing"
        if not cp.has_section(sec):
            cp.add_section(sec)
        cp.set(sec, "ShowFullScreen", str(options["fit_"]))
        cp.set(sec, "FSResample", str(int(options["resample_"])))
        cp.set(sec, "FSAlpha", str(int(options["alpha_"])))
        if cp.has_option('Others','INI_Folder'):
            cp.remove_option('Others','INI_Folder')
        fp = open(eg.folderPath.RoamingAppData+"\\EventGhost\\i_view32.ini",'wb')
        cp.write(fp)
        fp.close()
        params='/slideshow="'+(options["filepath_"] if options["source_"] \
            else options["dirpath_"])
        params+='" /ini="'+eg.folderPath.RoamingAppData+'\\EventGhost\\" /monitor='\
            +str(options["mon_"])
        try:
            return win32api.ShellExecute(
                0,
                None,
                tail,
                params.encode(myEncoding),
                head,
                1
            )
        except:
            self.PrintError(self.text.err)

    def GetLabel(self, kwargs):
        options = self.defaults.copy()
        options.update(kwargs)
        return self.text.runslideshow+":"+options["label_"]

    def Configure(self, kwargs={}):
        options = self.defaults.copy()
        options.update(kwargs)
        panel = eg.ConfigPanel(self)
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            self.text.radioboxmode,
            choices=[self.text.modeFull, self.text.modeWin],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(options["mode_"])
        radioBoxMode.SetMinSize((197,65))
        radioBoxSource = wx.RadioBox(
            panel,
            -1,
            self.text.radioboxsource,
            choices=[self.text.folder, self.text.txtFile],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxSource.SetSelection(options["source_"])
        radioBoxSource.SetMinSize((197,65))
        radioBoxFit = wx.RadioBox(
            panel,
            -1,
            self.text.radioboxfit,
            choices=[
                self.text.mode1_1,
                self.text.onlyBig,
                self.text.fitAll,
                self.text.scratchAll
            ],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxFit.SetSelection(options["fit_"])
        radioBoxFit.SetMinSize((197,100))
        radioBoxProgress = wx.RadioBox(
            panel,
            -1,
            self.text.radioboxprogress,
            choices=[
                self.text.autoDelay,
                self.text.autoKeyb,
                self.text.randomDelay,
                self.text.randomKeyb
            ],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxProgress.SetSelection(options["progress_"])
        widthLbl=wx.StaticText(panel, -1, self.text.width)
        widthCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            options["width_"],
            max=8000.0,
            integerWidth= 4,
            fractionWidth=0,
            increment=10
        )
        highLbl=wx.StaticText(panel, -1, self.text.high)
        highCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            options["high_"],
            max=8000.0,
            integerWidth= 4,
            fractionWidth=0,
            increment=10
        )
        delayLbl=wx.StaticText(panel, -1, self.text.delay)
        delayCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            options["delay_"],
            max=99999.0,
            integerWidth= 5,
            fractionWidth=1,
            increment=0.1
        )
        loopCtrl = wx.CheckBox(panel, -1, self.text.loop)
        loopCtrl.SetMinSize((205,15))
        loopCtrl.SetValue(options["loop_"])
        noRepeatCtrl = wx.CheckBox(panel, -1, self.text.noRepeat)
        noRepeatCtrl.SetValue(options["noRepeat_"])
        suppressCtrl = wx.CheckBox(panel, -1, self.text.suppress)
        suppressCtrl.SetValue(options["suppress_"])
        displTextCtrl = wx.CheckBox(panel, -1, self.text.displtext)
        displTextCtrl.SetValue(options["displText_"])
        soundLoopCtrl = wx.CheckBox(panel, -1, self.text.soundLoop)
        soundLoopCtrl.SetValue(options["soundLoop_"])
        resampleCtrl = wx.CheckBox(panel, -1, self.text.resample)
        resampleCtrl.SetValue(options["resample_"])
        hideCursorCtrl = wx.CheckBox(panel, -1, self.text.hideCursor)
        hideCursorCtrl.SetValue(options["hideCursor_"])
        alphaCtrl = wx.CheckBox(panel, -1, self.text.alpha)
        alphaCtrl.SetValue(options["alpha_"])
        closeCtrl = wx.CheckBox(panel, -1, self.text.close)
        closeCtrl.SetValue(options["close_"])
        #
        monLbl=wx.StaticText(panel, -1, self.text.monitor)
        monLbl.Enable(False)
        monCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            options["mon_"],
            max=99,
        )
        monCtrl.Enable(False)
        labelLbl=wx.StaticText(panel, -1, self.text.label)
        labelCtrl=wx.TextCtrl(panel,-1,options["label_"])
        #
        #lineOptLbl=wx.StaticText(dialog, -1, self.text.lineOpt)
        #lineOptCtrl=wx.TextCtrl(dialog,-1,arrayValue[21])
        #lineOptCtrl.SetMinSize((333,20))
        #hlpbtnCommandCtrl = wx.Button(dialog, -1, self.text.help)
        maskLbl=wx.StaticText(panel, -1, self.text.mask)
        maskCtrl=wx.TextCtrl(panel,-1,options["mask_"])
        hlpbtnPatternCtrl = wx.Button(panel, -1, self.text.help)

        #Sizers
        monSizer=wx.BoxSizer(wx.VERTICAL)
        monSizer.Add(monLbl,0,wx.TOP,5)
        monSizer.Add(monCtrl,0,wx.TOP,2)
        #
        dummySizer1 = wx.BoxSizer(wx.VERTICAL)
        dummySizer1.Add((1,1))
        #
        LblSizer=wx.BoxSizer(wx.VERTICAL)
        LblSizer.Add(labelLbl,0,wx.TOP|wx.RIGHT,5)
        LblSizer.Add(labelCtrl,0,wx.TOP,2)
        #
        monLblSizer = wx.BoxSizer(wx.HORIZONTAL)
        monLblSizer.Add(monSizer,0)
        monLblSizer.Add(dummySizer1,wx.EXPAND)
        monLblSizer.Add(LblSizer,0,wx.ALIGN_RIGHT)
        #
        #lineOptSizer = wx.FlexGridSizer(2,2,hgap=5,vgap=1)
        #lineOptSizer.Add(lineOptLbl,0)
        #lineOptSizer.Add((1,1))
        #lineOptSizer.Add(lineOptCtrl,0)
        #lineOptSizer.Add(hlpbtnCommandCtrl,0,wx.TOP,-2)
        #
        maskSizer=wx.FlexGridSizer(2,2,hgap=1,vgap=1)
        maskSizer.Add(maskLbl,0,wx.RIGHT|wx.ALIGN_BOTTOM)
        maskSizer.Add((1,1))
        maskSizer.Add(maskCtrl,0,wx.RIGHT|wx.TOP,1)
        maskSizer.Add(hlpbtnPatternCtrl,0,wx.TOP)
        #
        maskMonLblSizer=wx.GridSizer(1,2)
        maskMonLblSizer.Add(maskSizer,0,wx.TOP,5)
        maskMonLblSizer.Add(monLblSizer,0,wx.EXPAND)
        #
        delaySizer= wx.FlexGridSizer(2,1,vgap=1)
        delaySizer.Add(delayLbl, 0,wx.LEFT,30)
        delaySizer.Add(delayCtrl, 0,wx.LEFT,30)
        #
        windowSizer = wx.FlexGridSizer(rows=2, cols=2, hgap=30, vgap=2)
        windowSizer.Add(widthLbl, 0,wx.LEFT,10)
        windowSizer.Add(highLbl, 0)
        windowSizer.Add(widthCtrl, 0,wx.LEFT,10)
        windowSizer.Add(highCtrl, 0)
        box = wx.StaticBox(panel,-1,self.text.windowSize)
        boxSizer = wx.StaticBoxSizer(box,wx.HORIZONTAL)
        boxSizer.Add(windowSizer,0)
        #
        radioSizer = wx.FlexGridSizer(rows=3, cols=2, hgap=10, vgap=10)
        radioSizer.Add(radioBoxMode, 0)
        radioSizer.Add(radioBoxSource, 0,wx.EXPAND)
        radioSizer.Add(radioBoxFit, 0)
        radioSizer.Add(radioBoxProgress, 0,wx.EXPAND)
        radioSizer.Add(boxSizer,0,wx.EXPAND)
        radioSizer.Add(delaySizer,0,wx.TOP,17)
        #
        checkBoxSizer = wx.FlexGridSizer(rows=4, cols=2, hgap=8,vgap=6)
        checkBoxSizer.Add(loopCtrl, 0)
        checkBoxSizer.Add(noRepeatCtrl, 0)
        checkBoxSizer.Add(suppressCtrl, 0)
        checkBoxSizer.Add(displTextCtrl, 0)
        checkBoxSizer.Add(soundLoopCtrl, 0)
        checkBoxSizer.Add(resampleCtrl, 0)
        checkBoxSizer.Add(hideCursorCtrl, 0)
        checkBoxSizer.Add(alphaCtrl, 0)
        checkBoxSizer.Add((1,1))
        checkBoxSizer.Add(closeCtrl, 0)
        #
        dynSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(radioSizer, 0,wx.EXPAND)
        mainSizer.Add(checkBoxSizer,0,wx.TOP,10)
        mainSizer.Add(maskMonLblSizer,0,wx.EXPAND|wx.TOP,8)
        #mainSizer.Add(lineOptSizer,0,wx.TOP,8)
        mainSizer.Add(dynSizer,0)
        panel.sizer.Add(mainSizer)
        #
        def onSourceChange(event=None):
            dynSizer.Clear(True)
            if radioBoxSource.GetSelection():
                filepathLbl=wx.StaticText(panel, -1, self.text.filepath)
                filepathCtrl = eg.FileBrowseButton(
                    panel,
                    size=(370,-1),
                    initialValue=options["filepath_"],
                    startDirectory=eg.folderPath.ProgramFiles,
                    fileMask = self.text.filemask,
                    buttonText=eg.text.General.browse,
                    toolTip=self.text.toolTipFile
                )
                filepathCtrl.SetValue(options["filepath_"])
                dynSizer.Add(filepathLbl,0,wx.TOP,8)
                dynSizer.Add(filepathCtrl,0)
            else:
                dirpathLbl=wx.StaticText(panel, -1, self.text.dirpath)
                dirpathCtrl = eg.DirBrowseButton(
                    panel,
                    -1,
                    size=(370,-1),
                    startDirectory=options["dirpath_"],
                    labelText="",
                    buttonText=eg.text.General.browse,
                    dialogTitle=self.text.browseTitle,
                    toolTip=self.text.toolTipFolder
                )
                dirpathCtrl.SetValue(options["dirpath_"])
                dynSizer.Add(dirpathLbl,0,wx.TOP,8)
                dynSizer.Add(dirpathCtrl,0)
            mainSizer.Layout()
            if event:
                event.Skip()
        radioBoxSource.Bind(wx.EVT_RADIOBOX, onSourceChange)
        onSourceChange()

        #def onBtnCommandClick(event):
        #    self.plugin.OpenHelpPage('hlp_command_line.htm')
        #    event.Skip()
        #hlpbtnCommandCtrl.Bind(wx.EVT_BUTTON, onBtnCommandClick, hlpbtnCommandCtrl)

        def onProgressChange(event=None):
            noRepeatCtrl.Enable(radioBoxProgress.GetSelection()>1)
            delayCtrl.Enable((radioBoxProgress.GetSelection()+1)%2)
            delayLbl.Enable((radioBoxProgress.GetSelection()+1)%2)
            if event:
                event.Skip()

        radioBoxProgress.Bind(wx.EVT_RADIOBOX, onProgressChange)
        onProgressChange()

        def onModeChange(event=None):
            widthCtrl.Enable(radioBoxMode.GetSelection())
            highCtrl.Enable(radioBoxMode.GetSelection())
            widthLbl.Enable(radioBoxMode.GetSelection())
            highLbl.Enable(radioBoxMode.GetSelection())
            if event:
                event.Skip()

        radioBoxMode.Bind(wx.EVT_RADIOBOX, onModeChange)
        onModeChange()

        def onCloseChange(event=None):
            loopCtrl.Enable(not closeCtrl.GetValue())
            if event:
                event.Skip()

        closeCtrl.Bind(wx.EVT_CHECKBOX, onCloseChange)
        onCloseChange()

        def onBtnPatternClick(event):
            self.plugin.OpenHelpPage('hlp_text_patternoptions.htm')
            event.Skip()

        hlpbtnPatternCtrl.Bind(
            wx.EVT_BUTTON,
            onBtnPatternClick,
            hlpbtnPatternCtrl
        )

        def onShowTextChange(event=None):
            maskLbl.Enable(displTextCtrl.GetValue())
            maskCtrl.Enable(displTextCtrl.GetValue())
            hlpbtnPatternCtrl.Enable(displTextCtrl.GetValue())
            if event:
                event.Skip()

        displTextCtrl.Bind(wx.EVT_CHECKBOX, onShowTextChange)
        onShowTextChange()
        while panel.Affirmed():
            #kwargs = {}
            kwargs["label_"]=labelCtrl.GetValue()
            kwargs["width_"]=widthCtrl.GetValue()
            kwargs["high_"]=highCtrl.GetValue()
            kwargs["delay_"]=delayCtrl.GetValue()
            if radioBoxSource.GetSelection():
                kwargs["filepath_"]=\
                    dynSizer.GetChildren()[1].GetWindow().GetValue()
            else:
                kwargs["dirpath_"]=\
                    dynSizer.GetChildren()[1].GetWindow().GetValue()
            kwargs["mode_"]=radioBoxMode.GetSelection()
            kwargs["source_"]=radioBoxSource.GetSelection()
            kwargs["fit_"]=radioBoxFit.GetSelection()
            kwargs["progress_"]=radioBoxProgress.GetSelection()
            kwargs["loop_"]=loopCtrl.GetValue()
            kwargs["noRepeat_"]=noRepeatCtrl.GetValue()
            kwargs["suppress_"]=suppressCtrl.GetValue()
            kwargs["displText_"]=displTextCtrl.GetValue()
            kwargs["soundLoop_"]=soundLoopCtrl.GetValue()
            kwargs["resample_"]=resampleCtrl.GetValue()
            kwargs["hideCursor_"]=hideCursorCtrl.GetValue()
            kwargs["alpha_"]=alphaCtrl.GetValue()
            kwargs["close_"]=closeCtrl.GetValue()
            kwargs["mon_"]=monCtrl.GetValue()
            kwargs["mask_"]=maskCtrl.GetValue()
            #kwargs["lineOpt_"]=lineOptCtrl.GetValue()
            panel.SetResult(kwargs)


class RunWithOptions(eg.ActionClass):
    name = "Run with options"
    description = "Run IrfanView with options."
    defaults = {
        "label_": "",
        "filepath_": eg.folderPath.Pictures,
        "resample_": True,
        "alpha_": True,
        "hide_": True,
        "displ_": True,
        "resample2_": True,
        "center_": True,
        "caption_": True,
        "menuBar_": True,
        "toolBar_": True,
        "statusBar_": True,
        "fullOrWin_": 0,
        "winMode_": 2,
        "fullMode_": 1,
        "xCoord_": 50,
        "yCoord_": 50,
        "width_": 800,
        "high_": 600,
        "mon_": 1,
        "lineOpt_": "",
        "mask_": u"$D$F $X"
    }

    class text:
        err ="Couldn't find file i_view32.exe !"
        runwithoption = "Run with option "
        radioboxmode = "Starting mode"
        modeWin = "Window"
        modeFull = "Full screen"
        radioboxwinmode = "Window mode"
        winMode1 = "Fit window to image 1:1"
        winMode2 = "Fit images to window"
        winMode3 = "Fit only big images to window"
        winMode4 = "Fit images to desktop"
        winMode5 = "Fit only big images to desktop"
        winMode6 = "Do not fit anything"
        winMode7 = "Fit images to desktop width"
        winMode8 = "Fit images to desktop height"
        radiofullmode = "Full screen mode"
        mode1_1 = "Original size"
        onlyBig = "Fit only big"
        fitAll = "Fit all"
        scratchAll = "Scratch all"
        windowHide = "Hide Window elements (checked=hide)"
        caption = "Caption"
        menuBar = "Menu bar"
        toolBar = "Tool bar"
        statusLine = "Status bar"
        windowOption = "Window options"
        resample2 = "Resample"
        centerImage = "Center image in window"
        posAndSize = "Start position and size of window"
        xCoord = "X coordinate:"
        yCoord = "Y coordinate:"
        width = "Width:"
        high = "Height:"
        monitor = "Monitor:"
        label = "Label for this action:"
        displtext = "Show text (filename ...)"
        fsOptions = "Full screen options"
        resample = 'Use "Resample" function (slower)'
        hideCursor = "Hide mouse cursor"
        alpha = "Use Alpha blending between images"
        filepath = "Path to file:"
        filemask = (
            "JPG files (*.jpg)|*.jpg"
            "|BMP files (*.bmp)|*.bmp"
            "|PNG files (*.png)|*.png"
            "|All-Files (*.*)|*.*"
        )
        toolTipFile = 'Type filename or click browse to choose file'
        lineOpt="Another options enter like command line:"
        mask = 'Mask for "Show text":'
        help = "Help"

    def __call__(self, kwargs):
        options = self.defaults.copy()
        options.update(kwargs)
        head, tail = os.path.split(self.plugin.IrfanViewPath)
        cp = SafeConfigParser()
        cp.optionxform = str #Case sensitive !
        cp.read(head+"\\i_view32.ini")
        if cp.has_option('Others','INI_Folder'):
            INI_Folder = cp.get('Others','INI_Folder',True)
            if INI_Folder == '%APPDATA%\\IrfanView':
                INI_Folder = eg.folderPath.RoamingAppData+"\\IrfanView\\"
            cp.read(INI_Folder+"\\i_view32.ini")
        sec="WinPosition"
        if not cp.has_section(sec):
            cp.add_section(sec)
        cp.set(sec, "Width", str(options["width_"]))
        cp.set(sec, "Height", str(options["high_"]))
        fp = open(head+"\\i_view32.ini",'wb')
        cp.write(fp)
        fp.close()
        sec="Viewing"
        if not cp.has_section(sec):
            cp.add_section(sec)
        cp.set(sec, "FSResample", str(int(options["resample_"])))
        cp.set(sec, "FSAlpha", str(int(options["alpha_"])))
        cp.set(sec, "HideCursor", str(int(options["hide_"])))
        cp.set(sec, "ShowFullScreenName", str(int(options["displ_"])))
        cp.set(sec, "UseResample", str(int(options["resample2_"])))
        cp.set(sec, "Centered", str(int(options["center_"])))
        cp.set(sec, "FullScreen", str(options["fullOrWin_"]))
        cp.set(sec, "FitWindowOption", str(options["winMode_"]+1))
        cp.set(sec, "ShowFullScreen", str(options["fullMode_"]))
        if len(options["mask_"])>0:
            cp.set(sec, "FullText", options["mask_"])
        if cp.has_option('Others','INI_Folder'):
            cp.remove_option('Others','INI_Folder')
        fp = open(eg.folderPath.RoamingAppData+"\\EventGhost\\i_view32.ini",'wb')
        cp.write(fp)
        fp.close()
        params=options["filepath_"]+' /hide='+str(8*options["caption_"]\
            +4*options["menuBar_"]+2*options["statusBar_"]+options["toolBar_"])
        params+=' /ini="'+eg.folderPath.RoamingAppData+'\\EventGhost\\" /pos=('\
            +str(options["xCoord_"])+','+str(options["yCoord_"])+')'
        if len(options["lineOpt_"])>0:
            params+=' '+options["lineOpt_"]
        #params+=' /monitor='+str(options["mon_"])
        try:
            return win32api.ShellExecute(
                0,
                None,
                tail,
                params.encode(myEncoding),
                head,
                1
            )
        except:
            self.PrintError(self.text.err)

    def GetLabel(self, kwargs):
        options = self.defaults.copy()
        options.update(kwargs)
        return self.text.runwithoption+":"+options["label_"]

    def Configure(self, kwargs={}):
        options = self.defaults.copy()
        options.update(kwargs)
        panel = eg.ConfigPanel(self)
        radioBoxfullOrWin = wx.RadioBox(
            panel,
            -1,
            self.text.radioboxmode,
            choices=[self.text.modeWin, self.text.modeFull],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxfullOrWin.SetSelection(options["fullOrWin_"])
        radioBoxWinMode = wx.RadioBox(
            panel,
            -1,
            self.text.radioboxwinmode,
            choices=[
                self.text.winMode1,
                self.text.winMode2,
                self.text.winMode3,
                self.text.winMode4,
                self.text.winMode5,
                self.text.winMode6,
                self.text.winMode7,
                self.text.winMode8
            ],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxWinMode.SetSelection(options["winMode_"])
        radioBoxFullMode = wx.RadioBox(
            panel,
            -1,
            self.text.radiofullmode,
            choices=[
                self.text.mode1_1,
                self.text.onlyBig,
                self.text.fitAll,
                self.text.scratchAll
            ],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxFullMode.SetSelection(options["fullMode_"])
        resampleCtrl = wx.CheckBox(panel, -1, self.text.resample)
        resampleCtrl.SetValue(options["resample_"])
        alphaCtrl = wx.CheckBox(panel, -1, self.text.alpha)
        alphaCtrl.SetValue(options["alpha_"])
        hideCursorCtrl = wx.CheckBox(panel, -1, self.text.hideCursor)
        hideCursorCtrl.SetValue(options["hide_"])
        displTextCtrl = wx.CheckBox(panel, -1, self.text.displtext)
        displTextCtrl.SetValue(options["displ_"])
        captionCtrl = wx.CheckBox(panel, -1, self.text.caption)
        captionCtrl.SetValue(options["caption_"])
        menuBarCtrl = wx.CheckBox(panel, -1, self.text.menuBar)
        menuBarCtrl.SetValue(options["menuBar_"])
        toolBarCtrl = wx.CheckBox(panel, -1, self.text.toolBar)
        toolBarCtrl.SetValue(options["toolBar_"])
        statusLineCtrl = wx.CheckBox(panel, -1, self.text.statusLine)
        statusLineCtrl.SetValue(options["statusBar_"])
        resample2Ctrl = wx.CheckBox(panel, -1, self.text.resample2)
        resample2Ctrl.SetValue(options["resample2_"])
        centerImageCtrl = wx.CheckBox(panel, -1, self.text.centerImage)
        centerImageCtrl.SetValue(options["center_"])
        maskLbl=wx.StaticText(panel, -1, self.text.mask)
        maskCtrl=wx.TextCtrl(panel,-1,options["mask_"])
        hlpbtnPatternCtrl = wx.Button(panel, -1, self.text.help)
        labelLbl=wx.StaticText(panel, -1, self.text.label)
        labelCtrl=wx.TextCtrl(panel,-1,options["label_"])
        monLbl=wx.StaticText(panel, -1, self.text.monitor)
        monLbl.Enable(False)
        monCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            options["mon_"],
            max=99,
        )
        monCtrl.Enable(False)
        xCoordLbl=wx.StaticText(panel, -1, self.text.xCoord)
        xCoordCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            options["xCoord_"],
            max=8000,
        )
        yCoordLbl=wx.StaticText(panel, -1, self.text.yCoord)
        yCoordCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            options["yCoord_"],
            max=8000,
        )
        widthLbl=wx.StaticText(panel, -1, self.text.width)
        widthCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            options["width_"],
            max=8000,
        )
        highLbl=wx.StaticText(panel, -1, self.text.high)
        highCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            options["high_"],
            max=8000,
        )
        lineOptLbl=wx.StaticText(panel, -1, self.text.lineOpt)
        lineOptCtrl=wx.TextCtrl(panel,-1,options["lineOpt_"])
        lineOptCtrl.SetMinSize((333,20))
        hlpbtnCommandCtrl = wx.Button(panel, -1, self.text.help)
        filepathLbl=wx.StaticText(panel, -1, self.text.filepath)
        filepathCtrl = eg.FileBrowseButton(
            panel,
            size=(370,-1),
            initialValue=options["filepath_"],
            startDirectory=eg.folderPath.ProgramFiles,
            fileMask = self.text.filemask,
            buttonText=eg.text.General.browse,
            toolTip=self.text.toolTipFile
        )
        filepathCtrl.SetValue(options["filepath_"])
        #Sizers
        posAndSizeSizer = wx.FlexGridSizer(4,2,hgap=40,vgap=1)
        posAndSizeSizer.Add(xCoordLbl,0,wx.TOP,0)
        posAndSizeSizer.Add(yCoordLbl,0,wx.TOP,0)
        posAndSizeSizer.Add(xCoordCtrl,0,wx.TOP,0)
        posAndSizeSizer.Add(yCoordCtrl,0,wx.TOP,0)
        posAndSizeSizer.Add(widthLbl,0,wx.TOP,5)
        posAndSizeSizer.Add(highLbl,0,wx.TOP,5)
        posAndSizeSizer.Add(widthCtrl,0,wx.TOP,0)
        posAndSizeSizer.Add(highCtrl,0,wx.TOP,0)
        #
        box4 = wx.StaticBox(panel,-1,self.text.posAndSize)
        boxSizer4 = wx.StaticBoxSizer(box4,wx.HORIZONTAL)
        boxSizer4.Add((10,1),0)
        boxSizer4.Add(posAndSizeSizer,0,wx.EXPAND)
        #
        maskSizer=wx.FlexGridSizer(2,2,hgap=1,vgap=1)
        maskSizer.Add(maskLbl,0,wx.RIGHT|wx.ALIGN_BOTTOM)
        maskSizer.Add((1,1))
        maskSizer.Add(maskCtrl,0,wx.RIGHT|wx.TOP,2)
        maskSizer.Add(hlpbtnPatternCtrl,0,wx.TOP,1)
        #
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(radioBoxfullOrWin,0,wx.EXPAND)
        leftSizer.Add(radioBoxWinMode,0,wx.EXPAND|wx.TOP,9)
        leftSizer.Add(boxSizer4,0,wx.EXPAND|wx.TOP,9)
        leftSizer.Add(maskSizer,0,wx.EXPAND|wx.TOP,12)
        #
        box1 = wx.StaticBox(panel,-1,self.text.fsOptions)
        boxSizer1 = wx.StaticBoxSizer(box1,wx.VERTICAL)
        boxSizer1.Add(resampleCtrl, 0,wx.ALL,2)
        boxSizer1.Add(alphaCtrl, 0,wx.ALL,2)
        boxSizer1.Add(hideCursorCtrl, 0,wx.ALL,2)
        boxSizer1.Add(displTextCtrl, 0,wx.ALL,2)
        #
        box2 = wx.StaticBox(panel,-1,self.text.windowHide)
        boxSizer2 = wx.StaticBoxSizer(box2,wx.VERTICAL)
        boxSizer2.Add(captionCtrl, 0,wx.ALL,2)
        boxSizer2.Add(menuBarCtrl, 0,wx.ALL,2)
        boxSizer2.Add(toolBarCtrl, 0,wx.ALL,2)
        boxSizer2.Add(statusLineCtrl, 0,wx.ALL,2)
        #
        box3 = wx.StaticBox(panel,-1,self.text.windowOption)
        boxSizer3 = wx.StaticBoxSizer(box3,wx.VERTICAL)
        boxSizer3.Add(resample2Ctrl, 0,wx.ALL,2)
        boxSizer3.Add(centerImageCtrl, 0,wx.ALL,2)
        #
        monSizer=wx.BoxSizer(wx.VERTICAL)
        monSizer.Add(monLbl,0,wx.TOP,5)
        monSizer.Add(monCtrl,0,wx.TOP,2)
        dummySizer1 = wx.BoxSizer(wx.VERTICAL)
        dummySizer1.Add((1,1))
        LblSizer=wx.BoxSizer(wx.VERTICAL)
        LblSizer.Add(labelLbl,0,wx.TOP|wx.RIGHT,5)
        LblSizer.Add(labelCtrl,0,wx.TOP,2)
        monLblSizer = wx.BoxSizer(wx.HORIZONTAL)
        monLblSizer.Add(monSizer,0)
        monLblSizer.Add(dummySizer1,wx.EXPAND)
        monLblSizer.Add(LblSizer,0,wx.ALIGN_RIGHT)
        #
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(radioBoxFullMode,0,wx.EXPAND)
        rightSizer.Add(boxSizer1,0,wx.EXPAND|wx.TOP,7)
        rightSizer.Add(boxSizer3,0,wx.EXPAND|wx.TOP,7)
        rightSizer.Add(boxSizer2,0,wx.EXPAND|wx.TOP,7)
        rightSizer.Add(monLblSizer,0,wx.EXPAND|wx.TOP,7)
        #
        cmdlineSizer = wx.FlexGridSizer(4,2,hgap=5,vgap=1)
        cmdlineSizer.Add(lineOptLbl,0,wx.TOP,0)
        cmdlineSizer.Add((1,1))
        cmdlineSizer.Add(lineOptCtrl,0,wx.TOP,1)
        cmdlineSizer.Add(hlpbtnCommandCtrl,0,wx.TOP,-1)
        #
        bottomSizer = wx.BoxSizer(wx.VERTICAL)
        bottomSizer.Add(cmdlineSizer,0,wx.TOP,8)
        bottomSizer.Add(filepathLbl,0,wx.TOP,8)
        bottomSizer.Add(filepathCtrl,0,wx.TOP,1)
        #
        leftrightSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftrightSizer.Add(leftSizer,1)
        leftrightSizer.Add((5,1))
        leftrightSizer.Add(rightSizer,1)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(leftrightSizer,0)
        mainSizer.Add(bottomSizer,0)
        panel.sizer.Add(mainSizer)
        def onBtnPatternClick(event):
            self.plugin.OpenHelpPage('hlp_text_patternoptions.htm')
            event.Skip()
        hlpbtnPatternCtrl.Bind(
            wx.EVT_BUTTON,
            onBtnPatternClick,
            hlpbtnPatternCtrl
        )
        def onBtnCommandClick(event):
            self.plugin.OpenHelpPage('hlp_command_line.htm')
            event.Skip()
        hlpbtnCommandCtrl.Bind(
            wx.EVT_BUTTON,
            onBtnCommandClick,
            hlpbtnCommandCtrl
        )
        def onModeChange(event=None):
            widthCtrl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            highCtrl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            widthLbl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            highLbl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            xCoordCtrl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            yCoordCtrl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            xCoordLbl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            yCoordLbl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            if event:
                event.Skip()
        radioBoxWinMode.Bind(wx.EVT_RADIOBOX, onModeChange)
        onModeChange()
        def onShowTextChange(event=None):
            maskLbl.Enable(displTextCtrl.GetValue())
            maskCtrl.Enable(displTextCtrl.GetValue())
            hlpbtnPatternCtrl.Enable(displTextCtrl.GetValue())
            if event:
                event.Skip()
        displTextCtrl.Bind(wx.EVT_CHECKBOX, onShowTextChange)
        onShowTextChange()

        while panel.Affirmed():
            #kwargs = {}
            kwargs["label_"]=labelCtrl.GetValue()
            kwargs["filepath_"]=filepathCtrl.GetValue()
            kwargs["resample_"]=resampleCtrl.GetValue()
            kwargs["alpha_"]=alphaCtrl.GetValue()
            kwargs["hide_"]=hideCursorCtrl.GetValue()
            kwargs["displ_"]=displTextCtrl.GetValue()
            kwargs["resample2_"]=resample2Ctrl.GetValue()
            kwargs["center_"]=centerImageCtrl.GetValue()
            kwargs["caption_"]=captionCtrl.GetValue()
            kwargs["menuBar_"]=menuBarCtrl.GetValue()
            kwargs["toolBar_"]=toolBarCtrl.GetValue()
            kwargs["statusBar_"]=statusLineCtrl.GetValue()
            kwargs["fullOrWin_"]=radioBoxfullOrWin.GetSelection()
            kwargs["winMode_"]=radioBoxWinMode.GetSelection()
            kwargs["fullMode_"]=radioBoxFullMode.GetSelection()
            kwargs["xCoord_"]=xCoordCtrl.GetValue()
            kwargs["yCoord_"]=yCoordCtrl.GetValue()
            kwargs["width_"]=widthCtrl.GetValue()
            kwargs["high_"]=highCtrl.GetValue()
            kwargs["mon_"]=monCtrl.GetValue()
            kwargs["lineOpt_"]=lineOptCtrl.GetValue()
            kwargs["mask_"]=maskCtrl.GetValue()
            panel.SetResult(kwargs)




class Exit(eg.ActionClass):
    name = "Exit"
    description = "Exit."
    def __call__(self):
        hwnds = FindIrfanView()
        if len(hwnds) != 0:
            CloseHwnd(hwnds[0])
        else:
            self.PrintError(self.plugin.text.text1)
        return


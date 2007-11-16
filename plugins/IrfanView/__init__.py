version="0.2.1" 

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
# but widthOUT ANY WARRANTY; widthout even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along width EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import eg

eg.RegisterPlugin(
    name = "IrfanView",
    author = "Pako",
    version = version,
    kind = "program",
    description = (
        'Adds actions to control <a href="http://www.irfanview.com/">'
        'IrfanView</a>.'
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
    err ="Couldn't find file i_view32.exe !"

    class RunDefault:
        text2="Couldn't find file i_view32.exe !"

        
        
import wx
import os
from ConfigParser import SafeConfigParser
from shutil import copyfile
import _winreg
import win32api
import locale
myEncoding = locale.getdefaultlocale()[1]

Actions =((#Tuple 0 - most important actions
    ("OpenDialog","Show open dialog","Show open dialog.",u'{O}'),
    ("ShowNextPgOrFile","Show next page OR file","Show next page in a multipage image OR load next file in directory.",u'{Ctrl+PgDown}'),
    ("ShowPrevPgOrFile","Show previous page OR file","Show previous page in a multipage image OR load previous file in directory.",u'{Ctrl+PgUp}'),
    ("LoadFirstFile","Load first file","Load first file in the directory.",u'{Ctrl+Home}'),
    ("LoadLastFile","Load last file","Load last file in the directory.",u'{Ctrl+End}'),
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
    ("FullScreenMode2","Large fit to full screen","Full screen mode: Fit to screen: large images only.",u'{2}'),
    ("FullScreenMode3","All fit to full screen","Full screen mode: Fit to screen: all images/movies.",u'{3}'),
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
    ("AcquireBatchScanning","Acquire/Batch Scanning","Acquire/Batch Scanning",u'{Ctrl+Shift+A}'),
    #("CloseActualWindow","Close actual window","Close actual window (main window, slideshow, full screen, thumbnails or a dialog).",u'{Esc}'),
    ("SearchFiles","Search files","Search files.",u'{Ctrl+F}'),
),(#Tuple 2 - Edit menu
    ("EditUndo","Edit -> Undo","Edit -> Undo.",u'{Ctrl+Z}'),
    ("CreateSelection","Create custom selection","Edit -> Create custom selection.",u'{Shift+C}'),
    ("InsertText","Insert text into selection","Edit -> Insert text into selection.",u'{Ctrl+T}'),
    ("CutSelectionRectangle","Cut selection rectangle","Cut selection rectangle.",u'{Ctrl+X}'),
    ("CropSelectionRectangle","Crop selection rectangle","Crop selection rectangle.",u'{Ctrl+Y}'),
    ("CopyToClipboard","Copy image to clipboard","Copy image to clipboard.",u'{Ctrl+C}'),
#    ("PasteFromClipboard","Paste image from clipboard","Paste image from clipboard.",u'{Ins}'),
    ("PasteFromClipboard","Paste from clipboard","Paste image from clipboard.",u'{Ctrl+V}'),
    ("EditDelete","Edit -> Delete","Edit -> Delete.",u'{D}'),
),(#Tuple 3 - Picture menu
    ("ShowInformation","Show image information","Show image information.",u'{I}'),
    ("RotateLeft","Rotate left","Rotate left.",u'{L}'),
    ("RotateRight","Rotate right","Rotate right.",u'{R}'),
    ("RotateAngle","Rotate by angle","Rotate by angle.",u'{Ctrl+U}'),
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
    ("RotationLeft","Lossless JPG rot. Left","Lossless JPG rotation - to Left.",u'{Ctrl+Shift+L}'),
    ("RotationRight","Lossless JPG rot. Right","Lossless JPG rotation - to Right.",u'{Ctrl+Shift+R}'),
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
    ("LoadNextFile","Load next file","Load next file in directory.",u'{Space}'),
    ("LoadPrevFile","Load previous file","Load previous file in directory.",u'{Backspace}'),
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
    ("ControlSwitchThumb","Control switch in thumb. wind.","Control switch in the thumbnail window.",u'{Ctrl+Tab}'),
    ("SwitchMainThumbnail","Switch main/thumbnail window","Switch between main and thumbnail window (if visible).",u'{Tab}'),
    ("SelectAllThumb","Select all thumbnails","Select all thumbnails (thumbnail window).",u'{Ctrl+A}'),
    ("OpenBrowseDialog",'Show "Browse-Subfolders" dialog.','Show "Browse-Subfolders" dialog.',u'{Ctrl+B}'),
    ("ShowIptcDialog","Show IPTC dialog","Show IPTC dialog for JPGs.",u'{Ctrl+I}'),
    ("SendByMail","Send image by email","Send image by email.",u'{Shift+M}'),
    ("CopyFilename","Copy filename to clipboard.","Copy current filename to clipboard.",u'{Shift+P}'),
    ("JumpIntoToolbar","Jump into toolbar edit field","Jump into the toolbar edit field.",u'{Shift+T}'),
    ("Help","Help","Help.",u'{F1}'),
    ("AboutIrfanView",'Show "About IrfanView" dialog','Show "About IrfanView" dialog.',u'{A}'),
))


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
                ('mk:@MSITStore:'+head+'\i_view32.chm::/'+html_page).encode(myEncoding), 
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
                        handle = self.plugin.FindIrfanView()
                        if len(handle) != 0:
                            eg.plugins.Window.SendKeys(self.hotKey, False)
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
        filepathCtrl = eg.FileBrowseButton(
            dialog, 
            size=(320,-1),
            initialValue=IrfanViewPath, 
            startDirectory=eg.PROGRAMFILES,
            fileMask = self.text.filemask,
            buttonText=eg.text.General.browse
        )
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
        dialog = eg.ConfigurationDialog(self)
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        cmdlineLbl=wx.StaticText(dialog, -1, self.text.cmdline)
        cmdlineCtrl=wx.TextCtrl(dialog,-1,cmdline)
        cmdlineCtrl.SetMinSize((400,20))
        hlpbtnCtrl = wx.Button(dialog, -1, self.text.help)
        def onBtnClick(event=None):
            self.plugin.OpenHelpPage('hlp_command_line.htm') 
        hlpbtnCtrl.Bind(wx.EVT_BUTTON, onBtnClick, hlpbtnCtrl)            
        labelLbl=wx.StaticText(dialog, -1, self.text.label)
        labelCtrl=wx.TextCtrl(dialog,-1,label)
        mainSizer.Add(cmdlineLbl,0,wx.TOP,20)
        mainSizer.Add(cmdlineCtrl,0,wx.EXPAND)
        mainSizer.Add(hlpbtnCtrl,0,wx.ALIGN_RIGHT|wx.TOP,8)
        mainSizer.Add(labelLbl,0,wx.ALIGN_RIGHT|wx.TOP,50)
        mainSizer.Add(labelCtrl,0,wx.ALIGN_RIGHT)        
        dialog.sizer.Add(mainSizer)
        if dialog.AffirmedShowModal():
            return (labelCtrl.GetValue(),cmdlineCtrl.GetValue())


class RunSlideshow(eg.ActionClass):
    name = "Run slideshow"
    description = "Run IrfanView and start slideshow."
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
        filemask = "Text files (*.txt)|*.txt|List files (*.lst)|*.lst|All-Files (*.*)|*.*"
        dirpath = "Path to folder:"
        toolTipFile = 'Type filename or click browse to choose file'
        browseTitle = "Selected folder:"
        toolTipFolder = "Type directory name or browse to select"
        monitor = "Monitor:"
        lineOpt="Command line option:"
        help = "Help"
        mask = 'Mask for "Show text":'
    
    def __call__(self,arrayValue):
        head, tail = os.path.split(self.plugin.IrfanViewPath)            
        cp = SafeConfigParser()
        cp.optionxform = str #Case sensitive !
        cp.read(head+"\\i_view32.ini")        
        sec="Slideshow"
        if not cp.has_section(sec):
            cp.add_section(sec)
        cp.set(sec, "WindowW", str(int(arrayValue[1])))
        cp.set(sec, "WindowH", str(int(arrayValue[2])))
        cp.set(sec, "AutoDelay", str(arrayValue[3]))
        cp.set(sec, "RandomDelay", str(arrayValue[3]))
        cp.set(sec, "PlayInWindow", str(arrayValue[6]))
        cp.set(sec, "Advancement", str(arrayValue[9]+1))
        cp.set(sec, "Loop", str(int(arrayValue[10])))
        cp.set(sec, "NoSameImageAgain", str(int(arrayValue[11])))
        cp.set(sec, "SuppressErrors", str(int(arrayValue[12])))
        cp.set(sec, "ShowFilename", str(int(arrayValue[13])))
        cp.set(sec, "LoopAudio", str(int(arrayValue[14])))
        cp.set(sec, "HideCursor", str(int(arrayValue[16])))
        cp.set(sec,"StopAndClose",str(int(arrayValue[18])))
        if len(arrayValue[20])>0:
            cp.set(sec, "Text", arrayValue[20])
        sec="Viewing"
        if not cp.has_section(sec):
            cp.add_section(sec)
        cp.set(sec, "ShowFullScreen", str(arrayValue[8]))
        cp.set(sec, "FSResample", str(int(arrayValue[15])))
        cp.set(sec, "FSAlpha", str(int(arrayValue[17])))
        fp = open(eg.APPDATA+"\\EventGhost\\i_view32.ini",'wb') 
        cp.write(fp) 
        fp.close()
        params='/slideshow="'+(arrayValue[4] if arrayValue[7] else arrayValue[5])
        params+='" /ini="'+eg.APPDATA+'\\EventGhost\\" /monitor='+str(arrayValue[19])
        if len(arrayValue[21])>0:
            params+=' '+arrayValue[21]
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
            
    def GetLabel(self,arrayValue):
        return self.text.runslideshow+arrayValue[0]
    def Configure(
        self,
        arrayValue=[
            "",
            800.0,
            600.0,
            5.0,
            eg.APPDATA,
            eg.APPDATA,
            1,
            0,
            1,
            0,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            2,
            u"$D$F $X",
            "",
        ]
    ):
        dialog = eg.ConfigurationDialog(self)
        radioBoxMode = wx.RadioBox(
            dialog, 
            -1, 
            self.text.radioboxmode, 
            choices=[self.text.modeFull, self.text.modeWin], 
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(arrayValue[6])
        radioBoxMode.SetMinSize((197,65))
        radioBoxSource = wx.RadioBox(
            dialog, 
            -1, 
            self.text.radioboxsource, 
            choices=[self.text.folder, self.text.txtFile], 
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxSource.SetSelection(arrayValue[7])
        radioBoxSource.SetMinSize((197,65))
        radioBoxFit = wx.RadioBox(
            dialog, 
            -1, 
            self.text.radioboxfit, 
            choices=[self.text.mode1_1, self.text.onlyBig, self.text.fitAll, self.text.scratchAll], 
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxFit.SetSelection(arrayValue[8])
        radioBoxFit.SetMinSize((197,100))
        radioBoxProgress = wx.RadioBox(
            dialog, 
            -1, 
            self.text.radioboxprogress, 
            choices=[self.text.autoDelay, self.text.autoKeyb, self.text.randomDelay, self.text.randomKeyb], 
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxProgress.SetSelection(arrayValue[9])
        widthLbl=wx.StaticText(dialog, -1, self.text.width)
        widthCtrl = eg.SpinNumCtrl(
            dialog,
            -1,
            arrayValue[1],
            max=8000.0,
            integerWidth= 4,
            fractionWidth=0,
            increment=10
        )
        highLbl=wx.StaticText(dialog, -1, self.text.high)
        highCtrl = eg.SpinNumCtrl(
            dialog,
            -1,
            arrayValue[2],
            max=8000.0,
            integerWidth= 4,
            fractionWidth=0,
            increment=10
        )
        delayLbl=wx.StaticText(dialog, -1, self.text.delay)
        delayCtrl = eg.SpinNumCtrl(
            dialog,
            -1,
            arrayValue[3],
            max=99999.0,
            integerWidth= 5,
            fractionWidth=1,
            increment=0.1
        )
        loopCtrl = wx.CheckBox(dialog, -1, self.text.loop)
        loopCtrl.SetMinSize((205,15))
        loopCtrl.SetValue(arrayValue[10])
        noRepeatCtrl = wx.CheckBox(dialog, -1, self.text.noRepeat)
        noRepeatCtrl.SetValue(arrayValue[11])
        suppressCtrl = wx.CheckBox(dialog, -1, self.text.suppress)
        suppressCtrl.SetValue(arrayValue[12])
        displTextCtrl = wx.CheckBox(dialog, -1, self.text.displtext)
        displTextCtrl.SetValue(arrayValue[13])
        soundLoopCtrl = wx.CheckBox(dialog, -1, self.text.soundLoop)
        soundLoopCtrl.SetValue(arrayValue[14])
        resampleCtrl = wx.CheckBox(dialog, -1, self.text.resample)
        resampleCtrl.SetValue(arrayValue[15])
        hideCursorCtrl = wx.CheckBox(dialog, -1, self.text.hideCursor)
        hideCursorCtrl.SetValue(arrayValue[16])
        alphaCtrl = wx.CheckBox(dialog, -1, self.text.alpha)
        alphaCtrl.SetValue(arrayValue[17])
        closeCtrl = wx.CheckBox(dialog, -1, self.text.close)
        closeCtrl.SetValue(arrayValue[18])
        #
        monLbl=wx.StaticText(dialog, -1, self.text.monitor)
        monLbl.Enable(False)
        monCtrl = eg.SpinIntCtrl(
            dialog,
            -1,
            arrayValue[19],
            max=99,
        )
        monCtrl.Enable(False)
        labelLbl=wx.StaticText(dialog, -1, self.text.label)
        labelCtrl=wx.TextCtrl(dialog,-1,arrayValue[0])
        #
        #lineOptLbl=wx.StaticText(dialog, -1, self.text.lineOpt)
        #lineOptCtrl=wx.TextCtrl(dialog,-1,arrayValue[21])
        #lineOptCtrl.SetMinSize((333,20))
        #hlpbtnCommandCtrl = wx.Button(dialog, -1, self.text.help)
        maskLbl=wx.StaticText(dialog, -1, self.text.mask)
        maskCtrl=wx.TextCtrl(dialog,-1,arrayValue[20])
        hlpbtnPatternCtrl = wx.Button(dialog, -1, self.text.help)
        
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
        box = wx.StaticBox(dialog,-1,self.text.windowSize)
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
        dialog.sizer.Add(mainSizer)
        #
        def onSourceChange(event=None):
            dynSizer.Clear(True)
            if radioBoxSource.GetSelection():
                filepathLbl=wx.StaticText(dialog, -1, self.text.filepath)
                filepathCtrl = eg.FileBrowseButton(
                    dialog, 
                    size=(370,-1),
                    initialValue=arrayValue[4], 
                    startDirectory=eg.PROGRAMFILES,
                    fileMask = self.text.filemask,
                    buttonText=eg.text.General.browse,
                    toolTip=self.text.toolTipFile
                )
                filepathCtrl.SetValue(arrayValue[4])
                dynSizer.Add(filepathLbl,0,wx.TOP,8)
                dynSizer.Add(filepathCtrl,0)
            else:
                dirpathLbl=wx.StaticText(dialog, -1, self.text.dirpath)
                dirpathCtrl = eg.DirBrowseButton(
                    dialog, 
                    -1, 
                    size=(370,-1),
                    startDirectory=arrayValue[5],
                    labelText="",
                    buttonText=eg.text.General.browse,
                    dialogTitle=self.text.browseTitle,
                    toolTip=self.text.toolTipFolder
                )
                dirpathCtrl.SetValue(arrayValue[5])
                dynSizer.Add(dirpathLbl,0,wx.TOP,8)
                dynSizer.Add(dirpathCtrl,0)
            mainSizer.Layout()
        radioBoxSource.Bind(wx.EVT_RADIOBOX, onSourceChange)
        onSourceChange()

        #def onBtnCommandClick(event=None):
        #    self.plugin.OpenHelpPage('hlp_command_line.htm') 
        #hlpbtnCommandCtrl.Bind(wx.EVT_BUTTON, onBtnCommandClick, hlpbtnCommandCtrl)

        def onProgressChange(event=None):
            noRepeatCtrl.Enable(radioBoxProgress.GetSelection()>1)
            delayCtrl.Enable((radioBoxProgress.GetSelection()+1)%2)
            delayLbl.Enable((radioBoxProgress.GetSelection()+1)%2)
        radioBoxProgress.Bind(wx.EVT_RADIOBOX, onProgressChange)
        onProgressChange()

        def onModeChange(event=None):
            widthCtrl.Enable(radioBoxMode.GetSelection())
            highCtrl.Enable(radioBoxMode.GetSelection())
            widthLbl.Enable(radioBoxMode.GetSelection())
            highLbl.Enable(radioBoxMode.GetSelection())
        radioBoxMode.Bind(wx.EVT_RADIOBOX, onModeChange)
        onModeChange()

        def onBtnPatternClick(event=None):
            self.plugin.OpenHelpPage('hlp_text_patternoptions.htm')
        hlpbtnPatternCtrl.Bind(wx.EVT_BUTTON, onBtnPatternClick, hlpbtnPatternCtrl)
        
        def onShowTextChange(event=None):
            maskLbl.Enable(displTextCtrl.GetValue())
            maskCtrl.Enable(displTextCtrl.GetValue())
            hlpbtnPatternCtrl.Enable(displTextCtrl.GetValue())
        displTextCtrl.Bind(wx.EVT_CHECKBOX, onShowTextChange)
        onShowTextChange()
        if dialog.AffirmedShowModal():
            arrayValue[0]=labelCtrl.GetValue()
            arrayValue[1]=widthCtrl.GetValue()
            arrayValue[2]=highCtrl.GetValue()
            arrayValue[3]=delayCtrl.GetValue()
            if radioBoxSource.GetSelection():
                arrayValue[4]=dynSizer.GetChildren()[1].GetWindow().GetValue()
            else:
                arrayValue[5]=dynSizer.GetChildren()[1].GetWindow().GetValue()
            arrayValue[6]=radioBoxMode.GetSelection()
            arrayValue[7]=radioBoxSource.GetSelection()
            arrayValue[8]=radioBoxFit.GetSelection()
            arrayValue[9]=radioBoxProgress.GetSelection()
            arrayValue[10]=loopCtrl.GetValue()
            arrayValue[11]=noRepeatCtrl.GetValue()
            arrayValue[12]=suppressCtrl.GetValue()
            arrayValue[13]=displTextCtrl.GetValue()
            arrayValue[14]=soundLoopCtrl.GetValue()
            arrayValue[15]=resampleCtrl.GetValue()
            arrayValue[16]=hideCursorCtrl.GetValue()
            arrayValue[17]=alphaCtrl.GetValue()
            arrayValue[18]=closeCtrl.GetValue()
            arrayValue[19]=monCtrl.GetValue()
            arrayValue[20]=maskCtrl.GetValue()
            #arrayValue[21]=lineOptCtrl.GetValue()
            return (arrayValue,)


class RunWithOptions(eg.ActionClass):
    name = "Run with options"
    description = "Run IrfanView with options."
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
    
    def __call__(self,arrayValue):
        head, tail = os.path.split(self.plugin.IrfanViewPath)            
        cp = SafeConfigParser()
        cp.optionxform = str #Case sensitive !
        cp.read(head+"\\i_view32.ini")        
        sec="WinPosition"
        if not cp.has_section(sec):
            cp.add_section(sec)
        cp.set(sec, "Width", str(arrayValue[17]))
        cp.set(sec, "Height", str(arrayValue[18]))
        fp = open(head+"\\i_view32.ini",'wb') 
        cp.write(fp) 
        fp.close()
        sec="Viewing"
        if not cp.has_section(sec):
            cp.add_section(sec)
        cp.set(sec, "FSResample", str(int(arrayValue[2])))
        cp.set(sec, "FSAlpha", str(int(arrayValue[3])))
        cp.set(sec, "HideCursor", str(int(arrayValue[4])))
        cp.set(sec, "ShowFullScreenName", str(int(arrayValue[5])))
        cp.set(sec, "UseResample", str(int(arrayValue[6])))
        cp.set(sec, "Centered", str(int(arrayValue[7])))
        cp.set(sec, "FullScreen", str(arrayValue[12]))
        cp.set(sec, "FitWindowOption", str(arrayValue[13]+1))
        cp.set(sec, "ShowFullScreen", str(arrayValue[14]))
        if len(arrayValue[21])>0:
            cp.set(sec, "FullText", arrayValue[21])
        fp = open(eg.APPDATA+"\\EventGhost\\i_view32.ini",'wb') 
        cp.write(fp) 
        fp.close()
        params=arrayValue[1]+' /hide='+str(8*arrayValue[8]+4*arrayValue[9]+2*arrayValue[10]+arrayValue[11])
        params+=' /ini="'+eg.APPDATA+'\\EventGhost\\" /pos=('+str(arrayValue[15])+','+str(arrayValue[16])+')'
        if len(arrayValue[20])>0:
            params+=' '+arrayValue[20]
        #params+=' /monitor='+str(arrayValue[19])
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
            
    def GetLabel(self,arrayValue):
        return self.text.runwithoption+arrayValue[0]
    def Configure(
        self,
        arrayValue=[
            "",
            "",
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            0,
            2,
            1,
            50,
            50,
            800,
            600,
            1,
            "",
            u"$D$F $X"
        ]
    ):
        dialog = eg.ConfigurationDialog(self)
        radioBoxFullOrWin = wx.RadioBox(
            dialog, 
            -1, 
            self.text.radioboxmode, 
            choices=[self.text.modeWin, self.text.modeFull], 
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxFullOrWin.SetSelection(arrayValue[12])
        radioBoxWinMode = wx.RadioBox(
            dialog, 
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
        radioBoxWinMode.SetSelection(arrayValue[13])
        radioBoxFullMode = wx.RadioBox(
            dialog, 
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
        radioBoxFullMode.SetSelection(arrayValue[14])
        resampleCtrl = wx.CheckBox(dialog, -1, self.text.resample)
        resampleCtrl.SetValue(arrayValue[2])
        alphaCtrl = wx.CheckBox(dialog, -1, self.text.alpha)
        alphaCtrl.SetValue(arrayValue[3])
        hideCursorCtrl = wx.CheckBox(dialog, -1, self.text.hideCursor)
        hideCursorCtrl.SetValue(arrayValue[4])
        displTextCtrl = wx.CheckBox(dialog, -1, self.text.displtext)
        displTextCtrl.SetValue(arrayValue[5])
        captionCtrl = wx.CheckBox(dialog, -1, self.text.caption)
        captionCtrl.SetValue(arrayValue[8])
        menuBarCtrl = wx.CheckBox(dialog, -1, self.text.menuBar)
        menuBarCtrl.SetValue(arrayValue[9])
        toolBarCtrl = wx.CheckBox(dialog, -1, self.text.toolBar)
        toolBarCtrl.SetValue(arrayValue[10])
        statusLineCtrl = wx.CheckBox(dialog, -1, self.text.statusLine)
        statusLineCtrl.SetValue(arrayValue[11])
        resample2Ctrl = wx.CheckBox(dialog, -1, self.text.resample2)
        resample2Ctrl.SetValue(arrayValue[6])
        centerImageCtrl = wx.CheckBox(dialog, -1, self.text.centerImage)
        centerImageCtrl.SetValue(arrayValue[7])
        maskLbl=wx.StaticText(dialog, -1, self.text.mask)
        maskCtrl=wx.TextCtrl(dialog,-1,arrayValue[21])
        hlpbtnPatternCtrl = wx.Button(dialog, -1, self.text.help)
        labelLbl=wx.StaticText(dialog, -1, self.text.label)
        labelCtrl=wx.TextCtrl(dialog,-1,arrayValue[0])
        monLbl=wx.StaticText(dialog, -1, self.text.monitor)
        monLbl.Enable(False)
        monCtrl = eg.SpinIntCtrl(
            dialog,
            -1,
            arrayValue[19],
            max=99,
        )
        monCtrl.Enable(False)
        xCoordLbl=wx.StaticText(dialog, -1, self.text.xCoord)
        xCoordCtrl = eg.SpinIntCtrl(
            dialog,
            -1,
            arrayValue[15],
            max=8000,
        )
        yCoordLbl=wx.StaticText(dialog, -1, self.text.yCoord)
        yCoordCtrl = eg.SpinIntCtrl(
            dialog,
            -1,
            arrayValue[16],
            max=8000,
        )
        widthLbl=wx.StaticText(dialog, -1, self.text.width)
        widthCtrl = eg.SpinIntCtrl(
            dialog,
            -1,
            arrayValue[17],
            max=8000,
        )
        highLbl=wx.StaticText(dialog, -1, self.text.high)
        highCtrl = eg.SpinIntCtrl(
            dialog,
            -1,
            arrayValue[18],
            max=8000,
        )
        lineOptLbl=wx.StaticText(dialog, -1, self.text.lineOpt)
        lineOptCtrl=wx.TextCtrl(dialog,-1,arrayValue[20])
        lineOptCtrl.SetMinSize((333,20))
        hlpbtnCommandCtrl = wx.Button(dialog, -1, self.text.help)
        filepathLbl=wx.StaticText(dialog, -1, self.text.filepath)
        filepathCtrl = eg.FileBrowseButton(
            dialog, 
            size=(370,-1),
            initialValue=arrayValue[1], 
            startDirectory=eg.PROGRAMFILES,
            fileMask = self.text.filemask,
            buttonText=eg.text.General.browse,
            toolTip=self.text.toolTipFile
        )
        filepathCtrl.SetValue(arrayValue[1])
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
        box4 = wx.StaticBox(dialog,-1,self.text.posAndSize)
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
        leftSizer.Add(radioBoxFullOrWin,0,wx.EXPAND)
        leftSizer.Add(radioBoxWinMode,0,wx.EXPAND|wx.TOP,9)
        leftSizer.Add(boxSizer4,0,wx.EXPAND|wx.TOP,9)
        leftSizer.Add(maskSizer,0,wx.EXPAND|wx.TOP,12)
        #
        box1 = wx.StaticBox(dialog,-1,self.text.fsOptions)
        boxSizer1 = wx.StaticBoxSizer(box1,wx.VERTICAL)
        boxSizer1.Add(resampleCtrl, 0,wx.ALL,2)
        boxSizer1.Add(alphaCtrl, 0,wx.ALL,2)
        boxSizer1.Add(hideCursorCtrl, 0,wx.ALL,2)
        boxSizer1.Add(displTextCtrl, 0,wx.ALL,2)
        #
        box2 = wx.StaticBox(dialog,-1,self.text.windowHide)        
        boxSizer2 = wx.StaticBoxSizer(box2,wx.VERTICAL)
        boxSizer2.Add(captionCtrl, 0,wx.ALL,2)
        boxSizer2.Add(menuBarCtrl, 0,wx.ALL,2)
        boxSizer2.Add(toolBarCtrl, 0,wx.ALL,2)
        boxSizer2.Add(statusLineCtrl, 0,wx.ALL,2)
        #
        box3 = wx.StaticBox(dialog,-1,self.text.windowOption)
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
        #=#
        cmdlineSizer = wx.FlexGridSizer(4,2,hgap=5,vgap=1) #X
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
        dialog.sizer.Add(mainSizer)
        def onBtnPatternClick(event=None):
            self.plugin.OpenHelpPage('hlp_text_patternoptions.htm')
        hlpbtnPatternCtrl.Bind(wx.EVT_BUTTON, onBtnPatternClick, hlpbtnPatternCtrl)
        def onBtnCommandClick(event=None):
            self.plugin.OpenHelpPage('hlp_command_line.htm') 
        hlpbtnCommandCtrl.Bind(wx.EVT_BUTTON, onBtnCommandClick, hlpbtnCommandCtrl)
        def onModeChange(event=None):
            widthCtrl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            highCtrl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            widthLbl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            highLbl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            xCoordCtrl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            yCoordCtrl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            xCoordLbl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
            yCoordLbl.Enable(radioBoxWinMode.GetSelection() in [1,2,5])
        radioBoxWinMode.Bind(wx.EVT_RADIOBOX, onModeChange)
        onModeChange()
        def onShowTextChange(event=None):
            maskLbl.Enable(displTextCtrl.GetValue())
            maskCtrl.Enable(displTextCtrl.GetValue())
            hlpbtnPatternCtrl.Enable(displTextCtrl.GetValue())
        displTextCtrl.Bind(wx.EVT_CHECKBOX, onShowTextChange)
        onShowTextChange()
        
        if dialog.AffirmedShowModal():
            arrayValue[0]=labelCtrl.GetValue()
            arrayValue[1]=filepathCtrl.GetValue()
            arrayValue[2]=resampleCtrl.GetValue()
            arrayValue[3]=alphaCtrl.GetValue()
            arrayValue[4]=hideCursorCtrl.GetValue()
            arrayValue[5]=displTextCtrl.GetValue()
            arrayValue[6]=resample2Ctrl.GetValue()
            arrayValue[7]=centerImageCtrl.GetValue()
            arrayValue[8]=captionCtrl.GetValue()
            arrayValue[9]=menuBarCtrl.GetValue()
            arrayValue[10]=toolBarCtrl.GetValue()
            arrayValue[11]=statusLineCtrl.GetValue()
            arrayValue[12]=radioBoxFullOrWin.GetSelection()
            arrayValue[13]=radioBoxWinMode.GetSelection()
            arrayValue[14]=radioBoxFullMode.GetSelection()
            arrayValue[15]=xCoordCtrl.GetValue()
            arrayValue[16]=yCoordCtrl.GetValue()
            arrayValue[17]=widthCtrl.GetValue()
            arrayValue[18]=highCtrl.GetValue()
            arrayValue[19]=monCtrl.GetValue()
            arrayValue[20]=lineOptCtrl.GetValue()
            arrayValue[21]=maskCtrl.GetValue()
            return (arrayValue,)




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
         

# -*- coding: utf-8 -*-

version="0.0.8"

# plugins/LogRedirector/__init__.py
#
# Copyright (C)  2010 Pako  (lubos.ruckl@quick.cz)
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.8 by Pako 2013-09-03 10:40 GMT+1
#     - support url updated
# 0.0.7 by Pako 2013-01-20 10:02 GMT+1
#     - the new eg.Log API taken into consideration
# 0.0.6 by Pako 2011-10-03 07:25 GMT+1
#     - bugfix - "Only selected text file" option
# 0.0.5 by Pako 2011-05-17 15:13 GMT+1
#     - eg.scheduler used instead of the Threading
# 0.0.4 by Pako 2011-05-16 19:54 GMT+1
#     - some bugfixes
# 0.0.3 by Pako 2011-03-24 12:26 GMT+1
#     - bug fix when you just added this plugin
# 0.0.2 by Pako 2010-10-31 09:12 GMT+1
#     - added filtration option
# 0.0.1 by Pako 2010-10-24 17:57 GMT+1
#     - added check file size feature
# 0.0.0 by Pako 2010-10-20 14:56 GMT+1
#     - initial version
#===============================================================================

eg.RegisterPlugin(
    name = "Log redirector",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{E34BB200-A001-410B-B5F2-16B479AF2046}",
    description = u'''<rst>This plugin is designed to easily redirection of
EventGhost log to text file.''',
    createMacrosOnAdd = False,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=2852",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEUA////AAD/fHz/"
        "jIz/vb3/TU3/p6f/aGj/mpr/srL/x8f/2dn/0NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAABub2l0QgZzZVliYVRlZHIAAAJCVAdvdHR0QgUEb050ZmVUA2h4AnBkaVdL"
        "AmhpZUgCdGhhQwdvaXRCBQZvTm5iYVRlZHIAAQJCVAdvdHR0QgUEa090ZmUDALgCcG9p"
        "VwUCaHRlSAZ0aGdDBxlpdHAFBm5PbnRhVAhkck8CAnJUBwB0dHVCCW5hQ25sZWNmZUwB"
        "CANwb1RXBXhodGRIBktoZ2kHGQJ0cGEGbm9udEJjbmFUCGxyT2ICcmUFAABpZEVkRQhw"
        "bklMBHQCdGZvVAMFPgJ0ZGkA6QNpZUgCdGhhVAhkck8EAnJUBgBlbmFuUAZwZVNmZUwD"
        "DAICcG9pVwUDaHRIBgBoZ2kKAgJldmV0dU8GB3JvTnZDBWVyb2xsYwdjYWxhUBB0bmVr"
        "Y2F1b3IICGRPYmFyZWQAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAPAAAAAAEAAAEAAAB5utwAAAAAAAAAAAAA"
        "AAAAAAMAAAA3BI8AAAAAAAAAAAAAAAAAAAMAAQEAAQAAAAAAAAAAAABhFgh5urQAEHAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAJhFgh5veQAEBBGzxB5PdhxxNgAAAAAAAgAAGAAAAB5QBhgKuLGAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAIRJREFUeNql01kOgCAMBNCW"
        "VZD7n9cYY8PSOkb7V3xBOyARLp7L+fAMzvIIcESg28MADEFCICPAC7jaDQF6DbwB3N2W"
        "vzkEACQmA/QHDh6rIAYVENWofMKQwy5N1QH5NYYpSWXOEShbjCtN2qIDyjKrAeoyyPxS"
        "ySIbIMlCQ1es//++1wFodAMcT/AbEgAAAABJRU5ErkJggg=="
    ),
)
#===============================================================================

from os import path, fsync
from datetime import datetime as dt
from codecs import open as openFile
from winsound import PlaySound, SND_ASYNC
from win32gui import MessageBox
from Queue import Queue
if eg.Version.base >= "0.4.0":
    from eg.Classes.MainFrame.TreeCtrl import DropTarget as EventDropTarget
    IMAGES_DIR = eg.imagesDir 
else:
    from eg.Classes.MainFrame.TreeCtrl import EventDropTarget
    IMAGES_DIR = eg.IMAGES_DIR 
SYS_VSCROLL_X  = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
#===============================================================================

class Text:
    commitLabel = "File commit interval (seconds):"
    fileSize = "Current log file size:"
    logMode = "Logging mode"
    modes = (
        "Only native EventGhost log",
        "Native EventGhost log and selected text file",
        "Only selected text file",
    )
    boxTitle = 'Folder "%s" is incorrect'
    toolTipFile = "Press button and browse to select a logfile ..."
    browseFile = 'Select the logfile'
    label = "Log file:"
    size_1 = "Once the file reaches the size of"
    size_2 = "MiB, leave only the last"
    size_3 = "MiB"
    prefix="LogRedirector.LogFile"
    exceeded = "MaxSizeExceeded"
    truncated = "Truncated"
    toolTip = "Drag-and-drop an event from the log into the box."
    popup = (
        "Delete item",
        "Delete all items",
    )
    addItem = "Add item"
    filterMode = "To the log file write (only) the events:"
    filterModes = (
        "All",
        #"That includes the following strings",
        #"That excludes the following strings"
        "That starts with one of the following strings:",
        "That does not start with any of the following strings:"
    )
    mess = '''In the folder "%s"
is the "Log.txt" name reserved for system logfile of EventGhost.

Change the file name or folder !'''
#===============================================================================

class MyTextDropTarget(EventDropTarget):

    def __init__(self, object):
        EventDropTarget.__init__(self, object)
        self.object = object


    def OnDragOver(self, x, y, dragResult):
        return wx.DragMove


    def OnData(self, dummyX, dummyY, dragResult):
        if self.GetData() and self.customData.GetDataSize() > 0:
            txt = self.customData.GetData()
            evtList = self.object.GetEvtList()[0]
            flag = True
            for lst in evtList:
                if txt in lst:
                    flag = False
                    break
            if flag:
                self.object.InsertItem(txt)
            else:
                PlaySound('SystemExclamation', SND_ASYNC)


    def OnLeave(self):
        pass
#===============================================================================

newEVT_BUTTON_AFTER = wx.NewEventType()
EVT_BUTTON_AFTER = wx.PyEventBinder(newEVT_BUTTON_AFTER, 1)


class EventAfter(wx.PyCommandEvent):

    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.myVal = None


    def SetValue(self, val):
        self.myVal = val


    def GetValue(self):
        return self.myVal
#===============================================================================

class EventListCtrl(wx.ListCtrl):

    def __init__(self, parent, id, evtList, width, plugin):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | 
            wx.LC_NO_HEADER | wx.LC_SINGLE_SEL, size = (width, -1))
        self.parent = parent
        self.id = id
        self.evtList = evtList
        self.plugin = plugin
        self.sel = -1
        self.il = wx.ImageList(16, 16)
        self.il.Add(wx.BitmapFromImage(wx.Image(path.join(IMAGES_DIR, "event.png"), wx.BITMAP_TYPE_PNG)))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, '')
        self.SetColumnWidth(0, width - 5 - SYS_VSCROLL_X)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)
        self.SetToolTipString(self.plugin.text.toolTip)
        self.back = self.GetBackgroundColour()
        self.fore = self.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        self.SetItems(self.evtList)


    def SelRow(self, row):
        if row != self.sel:
            if self.sel in range(self.GetItemCount()):
                item = self.GetItem(self.sel)
                item.SetTextColour(self.fore)
                item.SetBackgroundColour(self.back)
                self.SetItem(item)
            self.sel = row
            self.SetItemState(row, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        if self.GetItemBackgroundColour(row) != self.selBack:
            item = self.GetItem(row)
            item.SetTextColour(self.selFore)
            item.SetBackgroundColour(self.selBack)
            self.SetItem(item)
            self.SetItemState(row, 0, wx.LIST_STATE_SELECTED)


    def InsertItem(self, txt):
        cnt = self.GetItemCount()
        self.InsertImageStringItem(cnt, txt, 0)
        self.evtList.append(txt)
        self.SelRow(cnt)
        self.EnsureVisible(cnt)


    def OnSelect(self, event):
        self.SelRow(event.GetIndex())
        evt = EventAfter(newEVT_BUTTON_AFTER, self.sel)
        evt.SetValue(self.GetItemText(self.sel))
        self.GetEventHandler().ProcessEvent(evt)
        event.Skip()


    def OnRightClick(self, event):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnDeleteButton, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnDeleteAllButton, id=self.popupID2)
        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, self.plugin.text.popup[0])
        menu.Append(self.popupID2, self.plugin.text.popup[1])
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()


    def OnDeleteButton(self, event=None):
        self.DeleteItem(self.sel)
        self.evtList.pop(self.sel)
        if self.sel > -1 and self.sel < self.GetItemCount():
            self.SetItemState(self.sel, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
            evtString = self.GetItemText(self.sel)
        else:
            self.sel = -1
            evtString = ""
        evt = EventAfter(newEVT_BUTTON_AFTER, self.sel)
        evt.SetValue(evtString)
        self.GetEventHandler().ProcessEvent(evt)        
        

    def OnDeleteAllButton(self, event=None):
        self.DeleteAllItems()
        self.evtList = []
        self.sel = -1
        evt = EventAfter(newEVT_BUTTON_AFTER, -1)
        evt.SetValue("")
        self.GetEventHandler().ProcessEvent(evt)


    def GetEvtList(self):
        return self.evtList, self.sel


    def SetItems(self, evtList):
        for i in range(len(evtList)):
            self.InsertImageStringItem(i, evtList[i], 0) 
 

    def ChangeItem(self, val):
        self.SetItemText(self.sel, val)
        return self.sel
#===============================================================================

class MyFileBrowseButton(eg.FileBrowseButton):

    def __init__(self,*args,**kwargs):
        if 'defaultFile' in kwargs:
            self.defaultFile = kwargs['defaultFile']
            del kwargs['defaultFile']
        else:
            self.defaultFile = ""
        eg.FileBrowseButton.__init__(self, *args, **kwargs)


    def GetValue(self):
        if self.textControl.GetValue():
            res = self.textControl.GetValue()
        else:
            res = "%s\\%s" % (self.startDirectory, self.defaultFile)
        return res


    def GetTextCtrl(self):          #  now I can make build-in textCtrl
        return self.textControl     #  non-editable !!!
#===============================================================================

class LogRedirector(eg.PluginBase):

    text = Text
    default = None
    ioFile = None
    task = None
    filterFlag = False


    def OpenFile(self, logfile):
        self.ioFile = openFile(logfile, encoding = 'utf-8', mode = 'a')
    

    def SetFlag(self, val):
        self.flag = val


    def WriteLine(self, line, icon, wRef, when, indent):
        wref = wRef.__repr__().split(" ") if wRef else ""
        if len(wref) == 1:
            wref = "EVENT: "
        elif len(wref) == 7:
            wref = wref[4][1:-5].upper()+": "
        if wref == "PLUGIN: ":
            wref = ""
        if self.check:
            if not self.fMode:
                self.q.put("%s  %s%s%s\r\n" % (str(dt.fromtimestamp(when))[:19],indent*3*" ",wref,line.strip()))
                if self.flag:
                    while not self.q.empty():
                        self.ioFile.write(self.q.get())
                return
            elif wref == "EVENT: ":
                if self.fMode == 1:
                    self.filterFlag = False
                    for evt in self.evtList:
                        if line.find(evt,0,1+len(evt)) == 0:
                            self.filterFlag = True
                            break
                elif self.fMode == 2:
                    self.filterFlag = True
                    for evt in self.evtList:
                        if line.find(evt,0,1+len(evt)) == 0:
                            self.filterFlag = False
                            break                    
                if not self.filterFlag:
                    return
            if not indent:
                self.filterFlag = True
            if not self.filterFlag:
                return
            self.q.put("%s  %s%s%s\r\n" % (str(dt.fromtimestamp(when))[:19],indent*3*" ",wref,line.strip()))
            if self.flag:
                while not self.q.empty():
                    self.ioFile.write(self.q.get())
        else:
            self.ioFile.write("%s  %s%s%s\r\n" % (str(dt.fromtimestamp(when))[:19],indent*3*" ",wref,line.strip()))


    def __start__(
        self,
        mode = 0,
        logfile = "",
        interval = 60,
        maxSize = 20,
        minSize = 10,
        check = False,
        evtList = [],
        fMode = 0
    ):
        self.interval = interval
        self.maxSize = maxSize
        self.minSize = minSize
        if check:
            self.q = Queue()
            self.flag = True
        self.check = check
        self.fMode = fMode
        self.evtList = evtList
        if mode == 0:
            eg.log.RemoveLogListener(self)
            self.task = None
            self.ioFile = None
        else:          
            self.OpenFile(logfile)
            self.task = eg.scheduler.AddTask(self.interval, self.CheckFileTask)
            eg.log.AddLogListener(self)
            eg.log.NativeLogOn(not bool(mode-1))


    def CheckFileTask(self):
        self.task = 0
        self.ioFile.flush()
        fsync(self.ioFile.fileno())
        if self.check:
            fn = self.ioFile.name
            sz = path.getsize(fn)
            if sz > self.maxSize*1048576:
                eg.TriggerEvent(self.text.exceeded, prefix=self.text.prefix, payload = sz)
                self.SetFlag(False)
                self.ioFile.close()
                tmpf = open(fn, 'rb+')
                tmpf.seek(-1048576*self.minSize,2)
                data = tmpf.read()
                pos = data.find("\r\n")
                tmpf.seek(0)
                tmpf.write(data[pos+2:])
                tmpf.truncate()
                tmpf.close()
                self.OpenFile(fn)
                eg.TriggerEvent(self.text.truncated, prefix=self.text.prefix, payload = path.getsize(fn))
                self.SetFlag(True)
        if self.task is not None:
            self.task = eg.scheduler.AddTask(self.interval, self.CheckFileTask)


    def __stop__(self):
        if self.task:
            eg.scheduler.CancelTask(self.task)
        self.task = None
        eg.log.NativeLogOn(True)
        eg.log.RemoveLogListener(self)
        if self.ioFile:
            if self.check:
                while not self.q.empty():
                    self.ioFile.write(self.q.get())
            self.ioFile.close()
            self.ioFile = None


    def Configure(
        self,
        mode = 0,
        logfile = "",
        interval = 60,
        maxSize = 20,
        minSize = 10,
        check = False,
        evtList = [],
        fMode = 0
):
        text = self.text
        panel = eg.ConfigPanel(self)
        self.logfile = logfile
        logFileCtrl = MyFileBrowseButton(
            panel,
            toolTip = text.toolTipFile,
            dialogTitle = text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.configDir,
            defaultFile = "EventGhost_Log.txt"
        )
        logFileCtrl.GetTextCtrl().SetEditable(False)
        logLabel = wx.StaticText(panel, -1, text.label)
        radioBox = wx.RadioBox(
            panel, 
            -1, 
            text.logMode, 
            choices = text.modes, 
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(mode)
        commitLabel = wx.StaticText(panel, -1, text.commitLabel)
        commitCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            interval,
            min=1,
            max=999,
        )
        fileSize_1 = wx.StaticText(panel, -1, text.fileSize)
        fileSizeCtrl = wx.TextCtrl(panel, -1, "",size=(30,-1))
        if self.logfile:
            fileSizeCtrl.ChangeValue(str((524288+path.getsize(self.logfile))/1048576))
        fileSize_2 = wx.StaticText(panel, -1, text.size_3)
        fileSize_1.Enable(False)
        fileSizeCtrl.Enable(False)
        fileSize_2.Enable(False)
        sizeCheck = wx.CheckBox(panel, -1, "")
        sizeCheck.SetValue(check)
        sizeLabel_1 = wx.StaticText(panel, -1, text.size_1)
        sizeCtrl_1 = eg.SpinIntCtrl(
            panel,
            -1,
            maxSize,
            min=2,
            max=999,
        )
        sizeLabel_2 = wx.StaticText(panel, -1, text.size_2)
        sizeCtrl_2 = eg.SpinIntCtrl(
            panel,
            -1,
            minSize,
            min=1,
            max=998,
        )
        sizeLabel_3 = wx.StaticText(panel, -1, text.size_3)
        filterLabel = wx.StaticText(panel, -1, text.filterMode)
        filterChoice = wx.Choice(panel, -1, choices = text.filterModes)
        filterChoice.SetSelection(fMode)
        w = filterChoice.GetSize()[0]
        eventsCtrl = EventListCtrl(panel, -1, evtList, w, self)
        dt = MyTextDropTarget(eventsCtrl)
        eventsCtrl.SetDropTarget(dt)
        editEventCtrl = wx.TextCtrl(panel, -1, "", size = ((w, -1)))
        editEventCtrl.Enable(False)
        delButton = wx.Button(panel, -1, text.popup[0])
        delButton.Enable(False)
        delAllButton = wx.Button(panel, -1, text.popup[1])
        delAllButton.Enable(len(evtList) > 0)
        addButton = wx.Button(panel, -1, text.addItem)
        commitSizer = wx.BoxSizer(wx.HORIZONTAL)
        commitSizer.Add(commitLabel, 0, wx.TOP, 3)
        commitSizer.Add(commitCtrl, 0, wx.LEFT, 8)
        commitSizer.Add((-1,-1), 1, wx.EXPAND)
        commitSizer.Add(fileSize_1, 0, wx.TOP, 3)
        commitSizer.Add(fileSizeCtrl, 0, wx.LEFT|wx.RIGHT, 4)
        commitSizer.Add(fileSize_2, 0, wx.TOP, 3)
        sizeSizer = wx.BoxSizer(wx.HORIZONTAL)
        sizeSizer.Add(sizeCheck, 0, wx.TOP|wx.RIGHT, 3)
        sizeSizer.Add(sizeLabel_1, 0, wx.TOP, 3)
        sizeSizer.Add(sizeCtrl_1, 0, wx.LEFT|wx.RIGHT, 5)
        sizeSizer.Add(sizeLabel_2, 0, wx.TOP, 3)
        sizeSizer.Add(sizeCtrl_2, 0, wx.LEFT|wx.RIGHT, 5)
        sizeSizer.Add(sizeLabel_3, 0, wx.TOP, 3)
        sizerAdd = panel.sizer.Add
        sizerAdd(radioBox, 0)
        sizerAdd(logLabel, 0, wx.TOP, 15)
        sizerAdd(logFileCtrl, 0, wx.TOP | wx.EXPAND, 2)
        sizerAdd(commitSizer, 0, wx.TOP | wx.EXPAND, 15)
        sizerAdd(sizeSizer, 0, wx.TOP | wx.EXPAND, 15)
        filterSizer = wx.GridBagSizer(vgap=1,hgap=20)
        filterSizer.AddGrowableRow(2)
        filterSizer.AddGrowableRow(4)
        filterSizer.AddGrowableRow(6)
        filterSizer.Add(filterLabel, (0, 0))
        filterSizer.Add(filterChoice, (1,0))
        filterSizer.Add(eventsCtrl, (2,0), (5, 1),flag = wx.TOP|wx.BOTTOM|wx.EXPAND)
        filterSizer.Add(editEventCtrl, (7,0))
        filterSizer.Add((-1, 14), (2,1))
        filterSizer.Add(delButton, (3,1),flag=wx.EXPAND)
        filterSizer.Add((-1, 12), (4,1))
        filterSizer.Add(delAllButton, (5,1))
        filterSizer.Add((-1, 14), (6,1))
        filterSizer.Add(addButton, (7,1),flag=wx.EXPAND)
        sizerAdd(filterSizer, 0, wx.EXPAND|wx.TOP,10)


        def onEditEvent(evt):
            str = evt.GetString()
            sel = eventsCtrl.ChangeItem(str)
            evtList[sel] = str
        editEventCtrl.Bind(wx.EVT_TEXT, onEditEvent)


        def onFocus(evt):
            str = evt.GetValue()
            editEventCtrl.ChangeValue(evt.GetValue())
            enb = evt.GetId() != -1
            editEventCtrl.Enable(enb)
            delButton.Enable(enb)
            delAllButton.Enable(eventsCtrl.GetItemCount() > 0)
            Validation()
        eventsCtrl.Bind(EVT_BUTTON_AFTER, onFocus)        


        def DummyHandle(evt):
            pass
        sizeCtrl_1.Bind(wx.EVT_TEXT, DummyHandle)
        sizeCtrl_2.Bind(wx.EVT_TEXT, DummyHandle)


        def Validation(event = None):
            fileYes = bool(radioBox.GetSelection())
            fltr = filterChoice.GetSelection()
            flg = True
            if fileYes and not self.logfile:
                flg = False
            if sizeCtrl_1.GetValue() <= sizeCtrl_2.GetValue():
                flg = False
            if fltr and not eventsCtrl.GetItemCount():
                flg = False
            panel.dialog.buttonRow.okButton.Enable(flg)
            panel.dialog.buttonRow.applyButton.Enable(flg)
        sizeCtrl_1.Bind(eg.EVT_VALUE_CHANGED, Validation)
        sizeCtrl_2.Bind(eg.EVT_VALUE_CHANGED, Validation)


        def onDeleteItem(evt):
            eventsCtrl.OnDeleteButton()
            Validation()
        delButton.Bind(wx.EVT_BUTTON, onDeleteItem)


        def onDeleteAllItem(evt):
            eventsCtrl.OnDeleteAllButton()
            Validation()
        delAllButton.Bind(wx.EVT_BUTTON, onDeleteAllItem)


        def onAddItem(evt):
            editEventCtrl.Enable(True)
            eventsCtrl.InsertItem("")
        addButton.Bind(wx.EVT_BUTTON, onAddItem)


        def onFilterChoice(event = None):
            filterOn = filterChoice.GetSelection()
            eventsCtrl.Enable(filterOn)
            addButton.Enable(filterOn)
            if filterOn:
                if not eventsCtrl.GetItemCount():
                    eventsCtrl.SetItems(evtList)
                sel = eventsCtrl.GetEvtList()[1]
                selected = sel > -1
                delButton.Enable(selected)
                editEventCtrl.Enable(selected)
                if selected:
                    eventsCtrl.SelRow(sel)
                    editEventCtrl.ChangeValue(evtList[sel])
                delAllButton.Enable(len(evtList) > 0) 
            else:
                delButton.Enable(False)
                editEventCtrl.Enable(False)
                delAllButton.Enable(False)
                eventsCtrl.DeleteAllItems()
                editEventCtrl.ChangeValue("")
            Validation()
        filterChoice.Bind(wx.EVT_CHOICE, onFilterChoice)


        def logFileChange(event):
            val = logFileCtrl.GetTextCtrl().GetValue()
            if val.lower() == u"%s\\log.txt" % unicode(eg.configDir).lower():
                PlaySound('SystemExclamation', SND_ASYNC)
                MessageBox(
                    panel.GetHandle(),
                    text.mess % unicode(eg.configDir),
                    "EventGhost - %s" % self.name,
                    48
                    )
                log_f = self.logfile if self.logfile else ""
                logFileCtrl.GetTextCtrl().SetValue(log_f)
                return
            self.logfile = val
            Validation()
        logFileCtrl.Bind(wx.EVT_TEXT, logFileChange)


        def onSizeCheck(event = None):
            val=sizeCheck.GetValue()
            sizeLabel_1.Enable(val)
            sizeCtrl_1.Enable(val)
            sizeLabel_2.Enable(val)
            sizeCtrl_2.Enable(val)
            sizeLabel_3.Enable(val)            
        sizeCheck.Bind(wx.EVT_CHECKBOX, onSizeCheck)
        onSizeCheck()


        def onRadioBox(event = None):
            val = bool(radioBox.GetSelection())
            if not val or self.logfile is None:
                logFileCtrl.GetTextCtrl().ChangeValue("")
            else:
                logFileCtrl.GetTextCtrl().ChangeValue(self.logfile)
            logLabel.Enable(val)
            logFileCtrl.Enable(val)
            commitLabel.Enable(val)
            commitCtrl.Enable(val)
            sizeCheck.Enable(val)
            filterLabel.Enable(val)
            filterChoice.Enable(val)
            if val:
                val=sizeCheck.GetValue()
            else:
                filterChoice.SetSelection(0)
            onFilterChoice()
            sizeCheck.SetValue(val)
            onSizeCheck()
        radioBox.Bind(wx.EVT_RADIOBOX, onRadioBox)
        onRadioBox()

        while panel.Affirmed():
            val = radioBox.GetSelection()
            panel.SetResult(
                val,
                logFileCtrl.GetTextCtrl().GetValue() if val else self.logfile,
                commitCtrl.GetValue(),
                sizeCtrl_1.GetValue(),
                sizeCtrl_2.GetValue(),                
                sizeCheck.GetValue(),
                eventsCtrl.GetEvtList()[0],
                filterChoice.GetSelection()
            )
#===============================================================================

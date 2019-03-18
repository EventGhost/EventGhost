version="0.0"

# Plugins/Battery/__init__.py
#
# Copyright (C)  2014 Pako  (lubos.ruckl@quick.cz)
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
# 0.0 by Pako 2014-09-12 16:55 UTC+1
#     - initial version

eg.RegisterPlugin(
    name = "Battery",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{B0FEAC8B-528C-40A4-8D73-867CDD57F19C}",
    canMultiLoad = False,
    createMacrosOnAdd = True,
    description = """ """,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6304",
    icon = (
        "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"
    )
)


from threading import enumerate as threads
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from ctypes import wintypes, Structure, POINTER, pointer, windll, WinError
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
ACV           = wx.ALIGN_CENTER_VERTICAL
ST            = [i for i in threads() if i.name=="SchedulerThread"][0]
#===============================================================================

class SYSTEM_POWER_STATUS(Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.c_ubyte),
        ('BatteryFlag', wintypes.c_ubyte),
        ('BatteryLifePercent', wintypes.c_ubyte),
        ('Reserved1', wintypes.c_ubyte),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
    ]
SYSTEM_POWER_STATUS_P = POINTER(SYSTEM_POWER_STATUS)
GetSystemPowerStatus = windll.kernel32.GetSystemPowerStatus
GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
GetSystemPowerStatus.restype = wintypes.BOOL
#===============================================================================

class Text:
    label1="List of alarm levels:"
    header1 = (
        "Enabled",
        "Name/Event suffix",
        "Percentage",
    )

    buttons1 = (
        "Add new",
        "Duplicate",
        "Edit",
        "Delete"
    )

    title1 = "Alarm level details"
    title4 = 'Alarm level "%s" details'
    profLbl1 = "List:"
    profLbl2 = "Name:"
    cancel = "Cancel"
    ok = "OK"
    #add = "Add"
    #delete = "Delete"
    period = "Polling period [s]:"
    prefix = "Event prefix:"
    levelSuffix = "AlarmLevel"
    ACstatus = ("Offline", "Online")
    version = "version"
#===============================================================================

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):

    def __init__(self, parent, header, rows):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL
        )
        self.rows = rows
        self.selRow = -1
        self.back = self.GetBackgroundColour()
        self.fore = self.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        self.wk = SYS_VSCROLL_X+self.GetWindowBorderSize()[0]
        self.collens = []
        hc = len(header)
        for i in range(hc):
            self.InsertColumn(i, header[i])
        for i in range(hc):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            w = self.GetColumnWidth(i)
            self.collens.append(w)
            self.wk += w
        self.InsertItem(0, "dummy")
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        hh = rect[1] #header height
        hi = rect[3] #item height
        self.DeleteAllItems()
        self.SetMinSize((self.wk, 5 + hh + rows * hi))
        self.SetSize((self.wk, 5 + hh + rows * hi))
        self.Layout()
        CheckListCtrlMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def SetWidth(self):
        newW = self.GetSize().width
        p = newW/float(self.wk)
        col = self.GetColumnCount()
        w = SYS_VSCROLL_X + self.GetWindowBorderSize()[0]+self.GetColumnWidth(0)
        for c in range(1, col-1):
            self.SetColumnWidth(c, p*self.collens[c])
            w += self.GetColumnWidth(c)
        self.SetColumnWidth(col-1, newW-w)


    def OnSize(self, event):
        wx.CallAfter(self.SetWidth)
        event.Skip()



    def OnItemSelected(self, evt):
        self.SelRow(evt.GetSelection())
        evt.Skip()


    # this is called by the base class when an item is checked/unchecked !!!!!!!
    def OnCheckItem(self, index, flag):
        evt = eg.ValueChangedEvent(self.GetId(), value = (index, flag))
        wx.PostEvent(self, evt)


    def SelRow(self, row):
        if row != self.selRow:
            if self.selRow in range(self.GetItemCount()):
                item = self.GetItem(self.selRow)
                item.SetTextColour(self.fore)
                item.SetBackgroundColour(self.back)
                self.SetItem(item)
            self.selRow = row
        if self.GetItemBackgroundColour(row) != self.selBack:
            item = self.GetItem(row)
            item.SetTextColour(self.selFore)
            item.SetBackgroundColour(self.selBack)
            self.SetItem(item)
            self.SetItemState(row, 0, wx.LIST_STATE_SELECTED)



    def DeleteRow(self, row = None):
        row = self.selRow if row is None else row
        if row > -1:
            self.DeleteItem(row)
            row = row if row < self.GetItemCount() else self.GetItemCount() - 1
            if row > -1:
                self.SelRow(row)
            else:
                self.selRow = -1
                evt = eg.ValueChangedEvent(self.GetId(), value="Empty")
                wx.PostEvent(self, evt)


    def AppendRow(self):
        ix = self.GetItemCount()
        self.InsertItem(ix, "")
        self.CheckItem(ix)
        self.EnsureVisible(ix)
        self.SelRow(ix)
        if ix == 0:
            evt = eg.ValueChangedEvent(self.GetId(), value="One")
            wx.PostEvent(self, evt)


    def SetRow(self, rowData, row = None):
        row = self.selRow if row is None else row
        if rowData[0]:
            self.CheckItem(row)
        elif self.IsChecked(row):
            self.ToggleItem(row)
        for i in range(1, len(rowData)):
            data = rowData[i] if i != 2 else str(rowData[i])
            self.SetItem(row, i, data)


    def GetSelectedItemIx(self):
        return self.selRow


    def GetRow(self, row = None):
        row = self.selRow if row is None else row
        rowData=[]
        rowData.append(self.IsChecked(row))
        for i in range(1, self.GetColumnCount()):
            data = self.GetItem(row, i).GetText()
            data = data if i != 2 else int(data)
            rowData.append(data)
        return rowData


    def GetData(self):
        data = []
        for row in range(self.GetItemCount()):
            rowData = self.GetRow(row)
            data.append(rowData)
        return data


    def SetData(self, data):
        if data:
            for row in range(len(data)):
                self.AppendRow()
                self.SetRow(data[row])
            self.SelRow(0)
            self.EnsureVisible(0)
#===============================================================================

class extDialog(wx.Frame):
    def __init__(
        self,
        parent,
        plugin,
        labels,
        data,
        grid,
        add = False,

    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL|wx.RESIZE_BORDER,
            name="BatteryExtDialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.labels = labels
        self.data = data
        self.grid = grid
        self.add = add



    def ShowExtDialog(self, title):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)
        text = self.plugin.text
        panel = wx.Panel(self)

        def wxst(label):
            return wx.StaticText(panel, -1, label)

        labels = self.labels
        data = self.data
        rows = len(labels)
        sizer = wx.FlexGridSizer(rows-1, 2, 5, 5)
        sizer.AddGrowableCol(1)
        for row in range(1, rows):
            sizer.Add(wxst(labels[row]), 0, ACV)
            if row == 1:
                ctrl = wx.TextCtrl(panel, -1, data[row])
            else:
                ctrl = eg.SpinIntCtrl(
                    panel,
                    -1,
                    data[row],
                    min=1,
                    max=100,
                )
            sizer.Add(ctrl,0,wx.EXPAND)

        line = wx.StaticLine(
            panel,
            -1,
            style = wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer,1,wx.ALL|wx.EXPAND,5)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        mainSizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        mainSizer.Add((1,6))
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)


        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)


        def onOk(evt):
            if self.add:
                self.grid.AppendRow()
            data=[self.data[0]]
            children = sizer.GetChildren()
            for child in range(1,len(children),2):
                ctrl=children[child].GetWindow()
                data.append(ctrl.GetValue())
            self.grid.SetRow(data)
            data = self.grid.GetData()
            data.sort(key = lambda level: int(level[2]))
            self.grid.DeleteAllItems()
            self.grid.SetData(data)
            self.Close()
        btn1.Bind(wx.EVT_BUTTON, onOk)


        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)

        mainSizer.Layout()
        w, h = self.GetSize()
        self.SetSize((max(w, 400), h))
        self.SetMinSize((max(w, 400), h))
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

#===============================================================================

    
class Battery(eg.PluginBase):
    text = Text

    def CancelTask(self):
        try:
            eg.scheduler.CancelTask(self.task)
        except:
            pass
        self.task = None


    def OnComputerSuspend(self, dummy):
        self.CancelTask()


    def OnComputerResume(self, dummy):
        self.CancelTask()
        self.levelFlags = dict([(level[0], False) for level in self.levels])
        self.task = eg.scheduler.AddTask(10.0, self.worker)


    def __init__(self):
        self.AddActionsFromList(ACTIONS)


    def __start__(
        self,
        levels = [],
        prefix = "Battery",
        period = 60,
    ):
        self.info.eventPrefix = prefix
        self.period = period
        levels.sort(key=lambda level: level[2],reverse=True)
        self.levels = [(item[2], item[1]) for item in levels if item[0]]
        percent = self.GetPercent()
        self.levelFlags = dict([(level[0], 
            not percent > level[0]) for level in self.levels])
        self.task = eg.scheduler.AddTask(0.1, self.worker)
        self.oldAcStatus = self.GetACpowerStatus()
        eg.Bind("System.PowerStatusChange", self.onPowerStatusChange)


    def __stop__(self):
        eg.Unbind("System.PowerStatusChange", self.onPowerStatusChange)
        self.CancelTask()


    def onPowerStatusChange(self, event):
        acStatus = self.GetACpowerStatus()
        if acStatus != self.oldAcStatus:
            if acStatus != 255:
                self.TriggerEvent("ACstatus.%s" % self.text.ACstatus[acStatus])
                self.oldAcStatus = acStatus


    def GetACpowerStatus(self):
        status = SYSTEM_POWER_STATUS()
        if not GetSystemPowerStatus(pointer(status)):
            raise WinError()
        return status.ACLineStatus   
    

    def GetPercent(self):
        try:
            status = SYSTEM_POWER_STATUS()
            if not GetSystemPowerStatus(pointer(status)):
                raise WinError()
            return status.BatteryLifePercent
        except:
            eg.PrintTraceback()


    def worker(self):
        heap = eg.scheduler.heap
        flag = False
        for task in heap:
            if task[1] == ST.LongTask:
                if task[2][0] == self.worker:
                    try:
                        eg.scheduler.CancelTask(task)
                        task = None
                    except:
                        pass
        self.task = eg.scheduler.AddTask(self.period, self.worker)
        percent = self.GetPercent()
        for level, suffix in self.levels:
            if percent <= level:
                if not self.levelFlags[level]:
                    self.TriggerEvent(
                        "%s.%s" % (self.text.levelSuffix, suffix), 
                        payload = percent
                    )
                    self.levelFlags[level] = True
            else:
                self.levelFlags[level] = False


    def Configure(
        self,
        levels = [],
        prefix = "Battery",
        period = 60,
    ):
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        label1 = wx.StaticText(panel, -1, self.text.label1)
        level_grid = CheckListCtrl(panel, self.text.header1, 3)
        self.level_grid = level_grid
        level_grid.SetData(levels)
        ttl = panel.dialog.GetTitle()
        panel.dialog.SetTitle(
            "%s - %s - %s %s" % ("Battery", ttl, self.text.version, version)
        )        

        def enableButtons1(enable):
            for b in range(1, len(self.text.buttons1)):
                wx.FindWindowById(bttns[b]).Enable(enable)


        def OnGridChange1(evt):
            value = evt.GetValue()
            if value == "Empty":
                enableButtons1(False)
            elif value == "One":
                enableButtons1(True)
            evt.Skip()
        level_grid.Bind(eg.EVT_VALUE_CHANGED, OnGridChange1)


        def edit1():
            dlg = extDialog(
                parent = panel,
                plugin = self,
                labels = self.text.header1,
                data=level_grid.GetRow(),
                grid=level_grid,
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowExtDialog,
                self.text.title1,
            )


        def OnActivated1(evt):
            edit1()
            evt.Skip()
        level_grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, OnActivated1)


        def onButton(evt):
            id = evt.GetId()
            if id == bttns[0]: #Add
                dlg = extDialog(
                    parent = panel,
                    plugin = self,
                    labels = self.text.header1,
                    data = [True,"",0],
                    grid = level_grid,
                    add = True,
                )
                dlg.Centre()
                wx.CallAfter(
                    dlg.ShowExtDialog,
                    self.text.title1,
                )
            elif id == bttns[1]: #Duplicate
                dlg = extDialog(
                    parent = panel,
                    plugin = self,
                    labels = self.text.header1,
                    data = level_grid.GetRow(),
                    grid = level_grid,
                    add = True
                )
                dlg.Centre()
                wx.CallAfter(
                    dlg.ShowExtDialog,
                    self.text.title1,
                )
            elif id == bttns[2]: # Edit
                edit1()
            elif id == bttns[3]: # Delete
                level_grid.DeleteRow()
            evt.Skip()

        panel.sizer.Add(label1, 0, wx.TOP|wx.LEFT, 5)
        panel.sizer.Add(level_grid, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        bttnSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        bttnSizer1.Add((5, -1))
        i = 0
        bttns = []
        for bttn in self.text.buttons1:
            id = wx.NewIdRef()
            bttns.append(id)
            b = wx.Button(panel, id, bttn)
            bttnSizer1.Add(b,1)
            if not len(levels) and i not in (0,):
                b.Enable(False)
            if i == 0:
                b.SetDefault()
            b.Bind(wx.EVT_BUTTON, onButton, id = id)
            bttnSizer1.Add((5, -1))
            i += 1
        panel.sizer.Add(bttnSizer1,0,wx.EXPAND)
        bottomSizer = wx.GridBagSizer(5, 5)
        panel.sizer.Add(bottomSizer,0,wx.ALL,5)
        prefLbl = wx.StaticText(panel, -1, self.text.prefix)
        prefCtrl = wx.TextCtrl(panel, -1, prefix)
        periLbl = wx.StaticText(panel, -1, self.text.period)
        periCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            period,
            min=30,
            max=600,
        )
        periCtrl.increment = 30
        periCtrl.numCtrl.SetEditable(False)


        def onPeriod(evt):
            val = evt.GetString()
            try:
                val = int(val)
            except:
                val = 0
                periCtrl.SetValue(0)
            evt.Skip()
        periCtrl.Bind(wx.EVT_TEXT, onPeriod)
        
        bottomSizer.Add(prefLbl,(0,0),flag=wx.ALIGN_CENTER_VERTICAL)
        bottomSizer.Add(prefCtrl,(0,1),flag=wx.EXPAND)
        bottomSizer.Add(periLbl,(1,0),flag=wx.ALIGN_CENTER_VERTICAL)
        bottomSizer.Add(periCtrl,(1,1),flag=wx.EXPAND)
        
        while panel.Affirmed():
            panel.SetResult(
                level_grid.GetData(),
                prefCtrl.GetValue(),
                periCtrl.GetValue()
            )
 
#===============================================================================

class GetACpowerStatus(eg.ActionBase):
 
    def __call__(self):
        return self.plugin.GetACpowerStatus()
#===============================================================================

class GetPercent(eg.ActionBase):
 
    def __call__(self):
        return self.plugin.GetPercent()
#===============================================================================

ACTIONS = (
    (
        GetPercent,
        "GetPercent",
        "Get battery percentage",
        "Returns remaining battery percentage.",
        None
    ),
    (
        GetACpowerStatus,
        "GetACpowerStatus",
        "Get AC power status",
        "Returns AC power status.",
        None
    ),
)

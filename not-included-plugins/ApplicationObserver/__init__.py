version="0.0.4"
# Plugins/ApplicationObserver/__init__.py
#
# Copyright (C)  2011 Pako  (lubos.ruckl@quick.cz)
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
# 0.0.4 by Pako 2011-06-19 08:10 GMT+1
#     - eg.scheduler used instead of the Threading
#     - Added an option to monitor a screensaver (*.scr)
# 0.0.3 by Pako 2010-10-18 18:39 GMT+1
#     - bugfix - when app is running before EventGhost start
# 0.0.2 by Pako 2010-09-24 07:27 GMT+1
#     - added url
# 0.0.1 by Pako 2010-09-23 19:02 GMT+1
#     - tooltip text fixed
# 0.0.0 by Pako 2010-09-23 18:42 GMT+1
#     - initial version

eg.RegisterPlugin(
    name = "Application Observer",
    author = "Pako",
    version = version,
    guid = "{EB732E73-B5BF-48E9-AD50-505548AAC6AA}",
    canMultiLoad = False,
    description = (
        "Generates events if selected application(s) is (are) launched or terminated."
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2792",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAADAFBMVEUAAADY2NjW1tbU"
        "1NTR0dHOzs7KysrHx8fDw8O/v7+7u7u3t7eysrKurq6pqanV1dXv7/Hf4ePf4OLf3+Le"
        "3+Le3uHd3uHc3eDc3N/b3N/b297s7O6jo6PS0tJNcqfY2dydnZ1pj8V1mcuSrtaatdqS"
        "sNmNrNeIqdeFqNfX19uWlpbJyclqkMZrkcd6ns6QrteRr9mJqdaCpdV+pNbW1tuQkJDE"
        "xMTc3uFqkcdskshtlMp4ndCIqNWMrNiEp9d9o9bU1dmKiopsk8lulctvl81ymM59otSA"
        "pdZ/pNbT09eEhIS6urpulsxwl81xmc9zm9F0ndN1ntTR0td+fn60tLTd3uDU1tp4eHjj"
        "4+TV1tfS09bX2NvBwcTMzdLLzNG6u73S0tXJyczW1thycnJdXV2CgoJ7e3tYWFirq6un"
        "p6dQUFBubm5hYWFeXl5aWlo1NTU+Pj5mZmbFxsg4ODgMDAyNjY2ysrPExcfBwci8vcTH"
        "yM2lpaZqamooKCioqKj7+/v39/f29vb19fWTk5McHBxnZ2d8fHx0dHRwcHBsbGxpaWkA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADinpTinpQAACQAAAAA"
        "AAAAAAAAAAABAAAAANAAABNBfbgAAAAAAADinpTinpQAACQAAAAAAAAAAAAAAAAgAAAA"
        "AQQAABNBfbgAAAAAAADiqqTiqqQAAIwAAAAAAAAAAAAAAAAAAAAAAADiplDiplAAAGgA"
        "AADiqtjiqtgAAFgAAAAAAAAAAAAAAACAAAAAAADipuzipBQAADQAAADinpTinpQAACQA"
        "AAAAAAAAAAAAAABAAAAAAaAAABNBfbgAAAAAAADiq0Diq0AABDQAAAAAAAAAAAAAAAAA"
        "AAAAAADiq2Tiq2QABBAAAADinpTinpQAACQAAAAAAAAABAAAAAAAAAAAADRM+c2wAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAANVJREFUeNpjYGBkYmZhZWPn"
        "4OTi5uHlY2Bg4BcQFBIWERUTl5CUkpYBCsgKycGBvAJQgFVYTlFJWUVVTV1DTlMLKKAt"
        "Kqejq6dvYGhkLGdiChQwM5ezsLSytrG1s5dzcAQKcErK6To5u7i6uXvIeXoBBbyl5Cyt"
        "fHz9/AMC5YKCgQIhoQhbwsKBArwRkVHRMbFx8QmJiUnJQIGU1OC01PSMzKzsnNy8fAYI"
        "KCgscggvZoCBktKy8orKquoamEBtXX1DY1NDfXMLTKS1Lby9o7MriwEbAACTCS12bX3A"
        "fQAAAABJRU5ErkJggg=="
    ),
)

from eg.cFunctions import GetProcessDict
from os.path import splitext
#===============================================================================

class Text:
    label_1 = "Observed applications (as notepad.exe or ssText3d.scr):"
    label_2 = "Refresh period (s):"
    launched = "Launched"
    terminated = "Terminated"
    prefix = "Application"
    addBtn = "Add application"
    delBtn = "Delete item"
    clrBtn = "Clear all"
    message = "Observed application(s):"
    toolTipList = """If some row is marked (selected),
the new item is inserted in its position.
Otherwise a new entry is inserted at the end of the list.
Row can be selected with the left mouse button
and unselected with the right mouse button."""
#===============================================================================

class ApplicationObserver(eg.PluginBase):
    text = Text
    task = None

    def __start__(self, apps, period):

        self.apps = apps
        self.period = period
        if apps:
            process = GetProcessDict()
            self.running = dict([(app, app in process.itervalues()) for app in apps])
            print "%s " % self.text.message,
            for app in apps[:-1]:
                print "%s, " % app,
            print apps[-1]
            self.task = eg.scheduler.AddTask(period, self.AppObserver)


    def __stop__(self):
        if self.task:
            eg.scheduler.CancelTask(self.task)
        self.task = None


    def AppObserver(self):
        self.task = 0
        process = GetProcessDict()
        for app in self.apps:
            if app in process.itervalues():
                if not self.running[app]:
                    eg.TriggerEvent(self.text.launched+"."+splitext(app)[0], prefix = self.text.prefix)
                    self.running[app] = True
            else:
                if self.running[app]:
                    eg.TriggerEvent(self.text.terminated+"."+splitext(app)[0], prefix = self.text.prefix)
                    self.running[app] = False
        if self.task is not None:
            self.task = eg.scheduler.AddTask(self.period, self.AppObserver)


    def Configure(self, apps = [], period = 0.5):
        panel = eg.ConfigPanel()
        label_1 = wx.StaticText(panel, -1, self.text.label_1)
        label_2 = wx.StaticText(panel, -1, self.text.label_2)
        addAppCtrl = wx.TextCtrl(panel, -1, "")
        periodCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            period,
            integerWidth = 5,
            fractionWidth = 1,
            allowNegative = False,
            min = 0.1,
            increment = 0.1,
        )
        appListCtrl = wx.ListBox(
            panel,
            -1,
            choices = apps,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        appListCtrl.SetToolTipString(self.text.toolTipList)
        addButton = wx.Button(panel, -1, self.text.addBtn)
        addButton.Enable(False)
        delButton = wx.Button(panel, -1, self.text.delBtn)
        clrButton = wx.Button(panel, -1, self.text.clrBtn)
        Sizer = wx.GridBagSizer(2, 10)
        Sizer.Add(label_2, (0, 0), flag=wx.TOP,border=3)
        Sizer.Add(periodCtrl, (0, 1))
        Sizer.Add(label_1, (1, 0), (1, 3), flag=wx.TOP,border=10)
        Sizer.Add(appListCtrl, (2, 0),(3, 3), flag = wx.EXPAND)
        Sizer.Add(delButton, (2, 3))
        Sizer.Add(clrButton, (3, 3), flag=wx.TOP,border=10)
        Sizer.Add((-1, 45), (4, 3))
        Sizer.Add(addAppCtrl, (5, 0), (1, 2), flag=wx.TOP|wx.EXPAND,border=10)
        Sizer.Add(addButton, (5, 2), flag=wx.TOP,border=10)
        panel.sizer.Add(Sizer, 1, wx.EXPAND)

        def EnableButtons():
            if appListCtrl.GetSelection() > -1:
                delButton.Enable(True)
            else:
                delButton.Enable(False)
            if appListCtrl.GetCount() == 0:
                clrButton.Enable(False)
            else:
                clrButton.Enable(True)

        EnableButtons()

        def OnAppListCtrl(event):
            EnableButtons()
            event.Skip()
        appListCtrl.Bind(wx.EVT_LISTBOX, OnAppListCtrl)


        def OnAppListCtrlRightClick(event):
            appListCtrl.SetSelection(-1)
            EnableButtons()
            event.Skip()
        appListCtrl.Bind(wx.EVT_RIGHT_DOWN, OnAppListCtrlRightClick)


        def OnAddAppCtrl(evt):
            val = evt.GetString()
            flag = False
            if len(val) > 4:
                flag = val[-4:].lower() in (".exe", ".scr")
            addButton.Enable(flag)
            if flag:
                addButton.SetFocus()
            evt.Skip()
        addAppCtrl.Bind(wx.EVT_TEXT, OnAddAppCtrl)


        def OnAddBtn(evt):
            pos = appListCtrl.GetSelection()
            if pos == -1:
                pos = appListCtrl.GetCount()
            app = addAppCtrl.GetValue()
            if app:
                if app not in appListCtrl.GetStrings():
                    appListCtrl.InsertItems((app,), pos)
                addAppCtrl.SetValue("")
            addAppCtrl.SetFocus()
            EnableButtons()
            evt.Skip()
        addButton.Bind(wx.EVT_BUTTON, OnAddBtn)


        def OnDelButton(event):
            sel = appListCtrl.GetSelection()
            if sel > -1:
                appListCtrl.Delete(sel)
                length = appListCtrl.GetCount()
                if length == sel:
                    sel -= 1
                if sel > -1:
                    appListCtrl.SetSelection(sel)
            EnableButtons()
            event.Skip()
        delButton.Bind(wx.EVT_BUTTON, OnDelButton)


        def OnClrButton(event):
            appListCtrl.Set([])
            EnableButtons()
            event.Skip()
        clrButton.Bind(wx.EVT_BUTTON, OnClrButton)

        while panel.Affirmed():
            panel.SetResult(
                appListCtrl.GetStrings(),
                periodCtrl.GetValue()
            )

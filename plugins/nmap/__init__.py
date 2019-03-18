version="1.0"

# Plugins/Nmap/__init__.py
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
# 1.0 by Pako 2014-09-15 16:08 UTC+1
#     - the device profiles introduced
#     - added option to disable/enable individual types of events
#     - added actions "Open/Close device/gr. info" and "Close all info dialogs"
#     - the info dialogs are automatically refreshed
# 0.7 by Pako 2014-08-03 07:55 UTC+1
#     - bugfix (main config dialog resize)
# 0.6 by Pako 2014-06-15 20:23 UTC+1
#     - added option to choose the length of the scanning period
#     - added an events Increased and Decreased
#             (when the number of group members is changed)
# 0.5 by Pako 2014-06-04 06:04 UTC+1
#     - bugfix (problem when filepath to nmap.exe contains a space character)
# 0.4 by Pako 2014-05-12 10:51 UTC+1
#     - update of action "Set IP address range"
# 0.3 by Pako 2014-05-06 17:24 UTC+1
#     - added action "Set IP address range"
# 0.2 by Pako 2014-05-05 19:09 UTC+1
#     - plugin config. dialog resize bugfix
#     - bugfix (function getAddresses)
# 0.1 by Pako 2014-05-03 09:01 UTC+1
#     - first public version
# 0.0 by Pako 2014-05-03 08:24 UTC+1
#     - initial version
#===============================================================================

eg.RegisterPlugin(
    name = "Nmap",
    author = "Pako",
    version = version,
    guid = "{62418772-B56D-436E-85CF-0E3292733D08}",
    canMultiLoad = False,
    createMacrosOnAdd = True,
    description = ur'''<rst>This plugin is intended to be used to monitor 
important devices on your local network. It will generate events if 
selected devices changes their statuses.
    

| This plugin is interfacing with Nmap_. Actually, it's Nmap_ frontend. 
| It follows that the installation of Nmap_ is a prerequisite for the
  functioning of this plugin. Nmap_ scans the network and the plugin
  handles the scanning results. Scanning is done periodically, by default
  every 30 seconds. 

| **WARNING!** 
| Scanning is performed on OSI layer two, so devices that are separated 
 using a router operating at layer 3 are not visible! 

| The **unique identifiers** for devices on the network does not use
| IP addresses. Instead **MAC addresses** are used. This is more reliable
 since it will overcome eventual changes of IP addresses, but it may add
 a little complication when setting up the plugin. To assist when adding
 a device, a dropdown list is presented. This list holds identified devices
 on the network with corresponding MAC addresses. The selection of the
 device can then be made directly from this list.   

**Notes on setting up and using the plugin:**

| **IP address range** 
| This box is necessary to set the range of IP addresses to be included in
 the scanning. 
 It is appropriate to set this as accurately as possible since this will
 then speed up the scanning process. There are several ways to set this up. 
 Refer therefore to the `documentation for Nmap`__. 
 Once you set the range, press **Apply**. This starts the scanning of devices
 listed under *Named devices* according to the related parameter settings.

| **The MAC addresses to be ignored** 
| Here you can enter the MAC addresses to be ignored by the plugin. The 
 address of the local computer (server) on which EventGhost is running, is
 ignored automatically.

| **Named devices**
| Here you simply add the devices you would like to monitor. You can also assign
 a customized profile to it if the Default is not fitting your need. 

| **Profiles**
| This feature allows you to define profiles that fits various types of DEVICE
 monitoring. Smartphones and routers might need a different profile than
 standard PC's.Power saving schemes on smartphones might require profiles
 with a more generous setting of the security factor and scanning period.
  
| **Security factor and Scanning period**
| Reliability of scanning is not 100%. The fault lies not on the side of Nmap_, 
 but on the part of some devices (especially smartphones), 
 which use various saving modes. Hence, the device is considered to be 
 disconnected at the moment when it is not found during several successive
 scans. This number can be adjusted using the *Security factor*.
 Suppose the scanning period is set to a default value of 30 seconds.
 Then this means, that at the default setting for Security factor of 8 is a
 disconnection detected after 8 * 30 seconds, i.e. after four minutes.

| **Device Groups**
| Your devices can in addition be organized into groups. The plugin will
  then generate events also based on the statuses of these groups
  (empty, incomplete, complete and increased/decreased).


__ http://nmap.org/book/man-target-specification.html
.. _Nmap:    http://nmap.org/
    ''',
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6136",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADZklEQVRYw+3WTWxUVRTA"
        "8d/rzLQz006prVCiQysfqUhQAyHKV+LGuGBhjBJMMCHGsFAXmrhyS+LCEIKBhYkbNcQl"
        "IcSFcWHEGF34HQlClSqfIXwMpS1MmXbaPhfv1BBIDCoJC3s399377jnnf84957zH3Jgb"
        "c+P/PpI0TZO7CdBytyMwBzAHMAeQ/0dNI3m+i/ISip1UFlAoM5GnMEX9PM0a9ZN8O5ym"
        "gzN3rBElydpuVr1EdS3LVlKaz3SRYkplismERpOrY5w+zrmvOfF+mh48+68BkuSZFlr7"
        "mP8qrdtYvIDlmB+BO48JrMQw6rEu4ChGxzjzMfZy9Uia7mvcNkCSbG6l62nKr7FhPeMt"
        "VEI5jGAmDE7FfgnzcA9+QRWncOkktY/I70rTPWN/C5AkW1roeYzKG1Q3Z7vL8BP6cQll"
        "tAbEBM7gKTRifQ5tMuAuXA255mEu7ubK/jTdN34LQJJsK5PbRN9bLFpCV55xXA7jRVwI"
        "gHOo4efYXxOel24orHtxJYwXcB+ODVPby+V30/SD2l8ASbK9SmU3qzZxuZx5/b3szh9B"
        "e6zd4NF7+AMPxfwKBtCLUWwMmBP4PXLnGjpm+OEIw9s5/WNux46z/fS/Q+E5Hi9kAk2s"
        "DuWd4cHpCO3Z2SRDDx6N860YCxlhsCPmKi4GQG/CtV7a1tF2NE//bgaezTwbxJKgL92U"
        "LuVQWA2gg5EHIunWYEMkYjPm9njfjicwhEOzOlbSsT9PYVPm1TC6Q3kuPILpWPdE+Hsi"
        "2Tbgizg3EADzQqYYkROys3MzongKk8h351hXptFOfZqxYnbyRCRYEkBtofRSzDksDogW"
        "bI1Q98gSty8qYALH4soORcVcm6R+gfrvpJ8mvFlhZCEeoDlA92o8SW9fpjwXpfhw3OFQ"
        "eDoeBs5jUYA1wvMH8V1EbCSq5voIE5/R+IrJoUxRZ+2WRhQdsJPOLXRt5f71lPMZSCWM"
        "j8ZzMaQaATQL/GuU3WGUBql/wtAuxmpp+vnUbbbiF1ooLST3IktfplDNolCM+r4S9zgd"
        "CdsRtd+BbzDaYPQAI29T/y1N903+h4/R9oVUdrJ0DSuqdBYp3fQlvT7DeIOTNY4fZuzD"
        "NN1z4I79lifJ60UKyyltpLIii0ghIJpTNC/SHGL0Swym6c7h29H7JwkjJsQ5KhX4AAAA"
        "AElFTkSuQmCC"
    ),
)

import _winreg
from subprocess import Popen, PIPE, STDOUT, SW_HIDE
from os import environ
from os.path import join
from time import time as ttime
from copy import deepcopy as cpy
from winsound import PlaySound, SND_ASYNC
from re import match
from threading import Thread, currentThread
from wx import ComboCtrl, ComboPopup
from eg.WinApi.Dynamic import BringWindowToTop


MAC_PATT = "^([0-9A-F]{2}[:]){5}([0-9A-F]{2})($| )"
ACV = wx.ALIGN_CENTER_VERTICAL
STYLE = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.STAY_ON_TOP
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
#===============================================================================

class Text:
    tooltip = "Right mouse button click closes this window"
    version = "version"
    label_0 = "Nmap install folder:"
    label_1 = "Event prefix:"
    label_2 = "Security factor:"
    label_3 = "Period of scanning [s]:"
    nmpFldr = "Choose the Nmap install folder ..."
    filter  = "Selector of events ..."
    evtFilter = [
        "Connected/Disconnected (for the unnamed devices)",
        "Away/Present (for device status)",
        "Empty/Incomplete/Complete (for group status)",
        "Increased/Decreased (for number of group members)",
        "DataAvailable/DataUnavailable",
        "Events run until after the first change \
(not immediately after plugin start)"
    ]
    profileLabels = (
        "Profile name",
        "Security factor",
        "Scanning period [s]"
    )
    prefix = "Nmap"
    dataAv = "DataAvailable "
    dataUn = "DataUnavailable "
    ignored = "The MAC addresses to be ignored:"
    toolTip = """Enter the MAC addresses that should be ignored.
This computer (on which EventGhost is running) is ignored automatically.
Use a comma as the separator.
Example: AA:BB:CC:DD:EE:FF, 00:11:22:33:44:55"""
    ipRng = "IP address range:"
    toolTipIp = """Enter the observed IP address range.
Example: 192.168.1.0/24 or 192.168.1.1-5,7,11,20-99"""
    title1 = "Named device"
    title2 = "Device group"
    title3 = "Nmap - Profile manager"
    btnProfMan = "Profile manager"
    named = "Named devices:"
    groups = "Device groups:"
    header1 = (
        "MAC address",
        "Nickname",
        "Profile"
    )
    infoLbl1 = (
        "Manufacturer",
        "Group(s)",
        "Status",
        "IP address(-es)"
    )
    header2 = (
        "Name",
        "Members"
    )
    buttons1 = (
        "Add new",
        "Edit",
        "Delete",
        "Show info",
    )
    refresh = "Refresh"
    cancel = "Cancel"
    ok = "OK"
    close = "Close"
    add = "Add new"
    delete = "Delete"
    more = "Apply and add more"
    status = ("Away", "Present")
    grState = ("Unknown", "Empty", "Incomplete", "Complete")
    unkn = "Unknown"
    auto = "Auto close after %i s"
    messBoxTit0 = "EventGhost - Nmap"
    messBoxTit1 = "Attention - empty value !"
    messBoxTit2 = "Attention duplicity !"
    messBoxTit3 = "Attention conflict !"
    messBoxTit4 = "Attention !"
    message1 = 'Group name can not be empty.'
    message2 = 'Group that has no members is unnecessary.'
    message3 = 'It is not possible to use the group name "%s",\n\
because the same name is already in the table.'
    message4 = 'Nickname can not be empty.'
    message5 = 'MAC addres can not be empty.'
    message6 = 'It is not possible to use the nickname "%s",\n\
because the same nickname is already in the table.'
    message7 = 'It is not possible to use the MAC address "%s",\n\
because the same MAC address is already in the table as "%s".'
    message8 = 'It is not possible to use the MAC address "%s",\n\
because this MAC address is on the ignore list.'
    message9 = 'It is not possible to use the MAC address "%s",\n\
because only the format as "09:1A:2B:3C:4D:5F" is accepted.'
    message10 = 'It is not possible to use the MAC address "%s",\n\
because this MAC address is on the list "Named devices".'
    message11 = 'It is not allowed to delete the profile \n\
"%s", because it is used.'
#===============================================================================

class CheckListComboBox(ComboCtrl):

    class CheckListBoxComboPopup(ComboPopup):

        def __init__(self, values, helpText):
            ComboPopup.__init__(self)
            self.values = values
            self.helpText = helpText

        def OnDclick(self, evt):
            self.Dismiss()
            self.SetHelpText()

        def Init(self):
            self.curitem = None

        def Create(self, parent):
            self.lb = wx.CheckListBox(parent, -1, (80, 50), wx.DefaultSize)
            # self.itemHeight = self.lb.GetItemHeight()
            self.SetValue(self.values)
            self.SetHelpText()
            self.lb.Bind(wx.EVT_MOTION, self.OnMotion)
            self.lb.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            self.lb.Bind(wx.EVT_LEFT_DCLICK, self.OnDclick)
            return True

        def SetHelpText(self, helpText = None):
            self.helpText = helpText if helpText is not None else self.helpText
            combo = self.GetComboCtrl()
            combo.SetText(self.helpText)
            combo.TextCtrl.SetEditable(False)

        def SetValue(self, values):
            self.lb.Set(values[0])
            for i in range(len(values[1])):
                self.lb.Check(i, int(values[1][i]))

        def GetValue(self):
            strngs = self.lb.GetStrings()
            return [strngs, [self.lb.IsChecked(i) for i in range(len(strngs))]]

        def GetControl(self):
            return self.lb

        def OnPopup(self):
            if self.curitem:
                self.lb.EnsureVisible(self.curitem)
                self.lb.SetSelection(self.curitem)

        # def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        #     return wx.Size(
        #         minWidth,
        #         min(self.itemHeight*(0.5+len(self.lb.GetStrings())), maxHeight)
        #     )

        def OnMotion(self, evt):
            item = self.lb.HitTest(evt.GetPosition())
            if item > -1:
                self.lb.SetSelection(item)
                self.curitem = item
            evt.Skip()

        def OnLeftDown(self, evt):
            item = self.lb.HitTest(evt.GetPosition())
            if item > -1:
                self.curitem = item
            evt.Skip()


    def __init__(self, parent, id=-1, values=[[],[]], **kwargs):
        if 'helpText' in kwargs:
            helpText = kwargs['helpText']
            del kwargs['helpText']
        else:
            helpText = ""
        ComboCtrl.__init__(self, parent, id, **kwargs)
        self.popup = self.CheckListBoxComboPopup(values, helpText)
        self.SetPopupControl(self.popup)
        self.popup.lb.Bind(wx.EVT_CHECKLISTBOX, self.onCheck)

    def onCheck(self, evt):
        wx.PostEvent(self, evt)
        evt.StopPropagation()

    def GetValue(self):
        return self.popup.GetValue()

    def SetValue(self, values):
        self.popup.SetValue(values)

    def SetHelpText(self, helpText = None):
        self.popup.SetHelpText(helpText)
#===============================================================================

class profileDialog(wx.Frame):
    def __init__(
        self,
        parent,
        plugin,
        data
    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = STYLE,
            name="NmapProfileDialog"
        )
        self.parent = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.labels = self.text.profileLabels
        self.data = data
        self.Centre()


    def ShowProfileDialog(self, title):
        self.parent.Enable(False)
        self.parent.dialog.buttonRow.cancelButton.Enable(False)
        self.parent.EnableButtons(False)
        self.SetTitle(title)
        text = self.plugin.text
        panel = wx.Panel(self)
        self.panel = panel

        def wxst(label):
            return wx.StaticText(panel, -1, label)

        labels = self.labels
        data = self.data
        gridSizer = wx.GridBagSizer(4, 5)
        gridSizer.Add(wxst(labels[0] + ":"), (0, 0), flag=ACV)
        profNameCtrl = wx.TextCtrl(panel, -1, data[0][0])
        profNameCtrl.Enable(False)
        gridSizer.Add(profNameCtrl, (0, 1), (1, 2), flag = wx.ALIGN_RIGHT)
        gridSizer.Add(wxst(labels[1] + ":"), (1, 0), (1, 2), ACV)
        factorCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            data[0][1],
            min = 1,
            max = 99,
        )
        gridSizer.Add(factorCtrl, (1,2), flag = wx.ALIGN_RIGHT)
        gridSizer.Add(wxst(labels[2] + ":"), (2, 0), (1, 2), ACV)
        periodCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            data[0][2],
            min = 10,
            max = 600,
        )
        periodCtrl.increment = 10
        periodCtrl.numCtrl.SetEditable(False)
        gridSizer.Add(periodCtrl, (2, 2), flag = wx.ALIGN_RIGHT)

        box = wx.StaticBox(panel, -1, "")
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        boxSizer.Add(gridSizer, 1, wx.EXPAND)
        sizerADE = wx.BoxSizer(wx.VERTICAL)
        sizerADE.Add(boxSizer, 1, wx.EXPAND)
        btn3 = wx.Button(panel, wx.ID_ADD)
        btn3.SetLabel(text.add)
        btn4 = wx.Button(panel, wx.ID_DELETE)
        btn4.SetLabel(text.delete)
        btn4.Enable(False)
        btnsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer2.Add(btn3)
        btnsizer2.Add((-1, -1), 1, wx.EXPAND)
        btnsizer2.Add(btn4)
        sizerADE.Add(btnsizer2, 0, wx.EXPAND|wx.TOP, 3)

        line = wx.StaticLine(
            panel,
            -1,
            style = wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer.Add((-1,-1), 1, wx.EXPAND)
        btnsizer.Add(btn1, 0, wx.RIGHT, 5)
        btnsizer.Add(btn2, 0, wx.RIGHT, 5)

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(sizerADE, 0, wx.RIGHT, 6)
        profile_grid = ListCtrl(panel, labels, data, 4, self)
        topSizer.Add(profile_grid, 0, wx.TOP, 7)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 5)
        mainSizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        mainSizer.Add((1, 6))
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        btn2.SetFocus()


        def onGridSelect(ix):
            flag = ix > 0
            btn4.Enable(flag)
            rowData = profile_grid.GetRow(ix)
            profNameCtrl.ChangeValue(rowData[0])
            factorCtrl.numCtrl.ChangeValue(rowData[1])
            periodCtrl.numCtrl.ChangeValue(rowData[2])
            profNameCtrl.Enable(flag)
        
        def onDelete(evt):
            rowData = profile_grid.GetRow()
            usedProf = tuple(
                set([itm[2] for itm in self.parent.named_grid.GetData()])
            )
            if rowData[0] in usedProf:
                MessageBox(
                    self.panel,
                    text.message11 % rowData[0],
                    text.messBoxTit4,
                    wx.ICON_EXCLAMATION,
                    plugin = self.plugin,
                    time = 20
                    )
                return
            profile_grid.DeleteRow()
            onGridSelect(profile_grid.selRow)
            btn1.Enable(True)
            evt.Skip()
        btn4.Bind(wx.EVT_BUTTON,onDelete)


        def onAdd(evt):
            btn3.Enable(False)
            profile_grid.AppendRow()
            profile_grid.SetRow(("","8","30"))
            onGridSelect(profile_grid.selRow)
            profNameCtrl.SetFocus()
            evt.Skip()
        btn3.Bind(wx.EVT_BUTTON,onAdd)

        def onProfName(evt):
            txt = evt.GetString()
            rowData = profile_grid.GetRow()
            rowData[0] = txt
            profile_grid.SetRow(rowData)
            names = [i[0] for i in profile_grid.GetData()]
            flag = txt != "" and names.count(txt) == 1
            btn3.Enable(flag)
            btn1.Enable(flag)
            evt.Skip()
        profNameCtrl.Bind(wx.EVT_TEXT,onProfName)

        def onFactor(evt):
            txt = evt.GetString().strip()
            rowData = profile_grid.GetRow()
            rowData[1] = txt
            profile_grid.SetRow(rowData)
            evt.Skip()
        factorCtrl.Bind(wx.EVT_TEXT, onFactor)

        def onPeriod(evt):
            txt = evt.GetString().strip()
            rowData = profile_grid.GetRow()
            rowData[2] = txt
            profile_grid.SetRow(rowData)
            evt.Skip()
        periodCtrl.Bind(wx.EVT_TEXT, onPeriod)

        def onGrid(evt):
            ix = evt.GetIndex()
            onGridSelect(ix)
            evt.Skip()
        profile_grid.Bind(wx.EVT_LIST_ITEM_SELECTED,onGrid)


        def onClose(evt):
            self.MakeModal(False)
            self.parent.Enable(True)
            self.parent.dialog.buttonRow.cancelButton.Enable(True)
            self.parent.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)


        def onOk(evt):
            self.parent.profiles = profile_grid.GetData()
            self.Close()
        btn1.Bind(wx.EVT_BUTTON, onOk)


        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)

        mainSizer.Layout()
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

#===============================================================================

class namedDialog(wx.Frame):
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
            style = STYLE | wx.RESIZE_BORDER,
            name="NmapNamedDialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.labels = labels
        self.data = data
        self.grid = grid
        self.add = add
        self.Centre()
        self.textId = wx.NewIdRef()


    def getNickname(self, txt):
        ix = txt.find("(")
        if ix > 16:
            iy = txt.rfind(")",ix,len(txt))
            if iy>ix:
                return txt[ix+1:iy]


    def ShowNamedDialog(self, title):
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
        sizer = wx.FlexGridSizer(rows, 2, 5, 5)
        sizer.AddGrowableCol(1)
        for row in range(rows):
            sizer.Add(wxst(labels[row] + ":"), 0, ACV)
            if row == 0:
                chcs = self.plugin.macs
                if chcs is not None:
                    chcs = chcs.iterkeys()
                    chcs = ["%s (%s)" % (i, self.plugin.ouis[i]) \
                        for i in chcs if i not in self.plugin.ignrd]
                else:
                    chcs = []
                ctrl = wx.ComboBox(panel, -1, choices=chcs,style=wx.CB_DROPDOWN)
                def onDevice(evt):
                    txtCtrl = wx.FindWindowById(self.textId)
                    nick = self.getNickname(evt.String)
                    if nick is not None:
                        txtCtrl.ChangeValue(nick)
                    evt.Skip()
                ctrl.Bind(wx.EVT_COMBOBOX, onDevice)
                flag = False
                if not self.add and chcs:
                    for mac in chcs:
                        if mac.startswith(data[row][:17]):
                            flag = True
                            break
                    if flag:
                        ctrl.SetStringSelection(mac)
                ctrl.SetValue(data[row] if not flag else mac)
                    
            elif row == 2:
                chcs = [i[0] for i in self.panel.profiles]
                ctrl = wx.ComboBox(panel, -1, choices=chcs,style=wx.CB_DROPDOWN)
                if not self.add:
                    ctrl.SetStringSelection(data[row])
                    
            else:
                ctrl = wx.TextCtrl(panel, self.textId, data[row])
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
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer.Add((-1,-1),1,wx.EXPAND)
        if self.add:
            btn0 = wx.Button(panel, wx.ID_APPLY)
            btn0.SetLabel(text.more)
            btnsizer.Add(btn0,0,wx.RIGHT,5)
        btnsizer.Add(btn1,0,wx.RIGHT,5)
        btnsizer.Add(btn2,0,wx.RIGHT,5)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer,1,wx.ALL|wx.EXPAND,5)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        mainSizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        mainSizer.Add((1,6))
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        btn2.SetFocus()


        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

        def onOk(evt):
            id = evt.GetId()
            data = ["","", 0]
            children = sizer.GetChildren()
            ctrls = []
            for i in range(len(self.labels)):
                ctrl = children[2 * i + 1].GetWindow()
                ctrls.append(ctrl)
                val = ctrl.GetValue()
                if i==1:
                    if val == "":
                        MessageBox(
                            self,
                            text.message4,
                            text.messBoxTit1,
                            wx.ICON_EXCLAMATION,
                            plugin = self.plugin,
                            time = 20
                            )
                        return
                    nicks = [j[1] for j in self.grid.GetData()]
                    if val in nicks:
                        ix = nicks.index(val)
                        if self.add or ix != self.grid.GetSelectedItemIx():
                            MessageBox(
                                self,
                                text.message6 % val,
                                text.messBoxTit2,
                                wx.ICON_EXCLAMATION,
                                plugin = self.plugin,
                                time = 20
                                )
                            return
                elif i==2:
                    val = ctrl.GetStringSelection()
                    val = val if val else ctrl.GetStrings()[0]
                else:
                    if val == "":
                        MessageBox(
                            self,
                            text.message5,
                            text.messBoxTit1,
                            wx.ICON_EXCLAMATION,
                            plugin = self.plugin,
                            time = 20
                            )
                        return
                    elif val.split(" ")[0] in self.plugin.ignrd:
                        MessageBox(
                            self,
                            text.message8 % val.split(" ")[0],
                            text.messBoxTit3,
                            wx.ICON_EXCLAMATION,
                            plugin = self.plugin,
                            time = 20
                            )
                        return
                    elif match(MAC_PATT, val) is None:
                        MessageBox(
                            self,
                            text.message9 % val.split(" ")[0],
                            text.messBoxTit4,
                            wx.ICON_EXCLAMATION,
                            plugin = self.plugin,
                            time = 20
                            )
                        return
                    rows = self.grid.GetData()
                    macs = [j[0] for j in rows]
                    if val in macs:
                        ix = macs.index(val)
                        if self.add or ix != self.grid.GetSelectedItemIx():
                            nick = [k[1] for k in rows][macs.index(val)]
                            MessageBox(
                                self,
                                text.message7 % (val.split(" ")[0], nick),
                                text.messBoxTit2,
                                wx.ICON_EXCLAMATION,
                                plugin = self.plugin,
                                time = 20
                                )
                            return
                data[i] = val
            if id == wx.ID_OK:
                self.Close()
            else:
                for i in range(len(self.labels)):
                    ctrls[i].SetValue("")
            if self.add:
                self.grid.AppendRow()
            self.grid.SetRow(data)
                
        if self.add:
            btn0.Bind(wx.EVT_BUTTON, onOk)
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

class groupDialog(wx.Frame):
    def __init__(
        self,
        parent,
        plugin,
        labels,
        data,
        grid,
        names,
        add=False,
    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = STYLE | wx.RESIZE_BORDER,
            name="NmapGroupDialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.labels = labels
        self.grid = grid
        self.iNamed = dict([(i[1], str(i[0].split(" ")[0])) \
            for i in names.GetData()])
        self.data = self.convData(data) if data else self.getInitChcs()
        self.add = add
        self.Centre()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

    def convData(self, data):
        chcs = list(self.iNamed.iterkeys())
        chcs.sort()
        vals=[]
        for item in chcs:
            vals.append(self.iNamed[item] in data[1])
        return [data[0],[chcs, vals]]
            
        chcs.sort()
        chcs = [chcs, len(chcs)*[False]]
        return data

    def getInitChcs(self):
        chcs = list(self.iNamed.iterkeys())
        chcs.sort()
        chcs = [chcs, len(chcs)*[False]]
        return ["", chcs]

    def ShowGroupDialog(self, title):
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
        sizer = wx.FlexGridSizer(rows, 2, 5, 5)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(1)
        for row in range(rows):
            sizer.Add(wxst(labels[row] + ":"), 0, ACV)
            if row == 0:
                ctrl = wx.TextCtrl(panel, -1, data[row])
            else:
                ctrl = myCheckListBox(
                    panel,
                    -1,
                    exChoices = data[row],
                )
            sizer.Add(ctrl,1,wx.EXPAND)
        line = wx.StaticLine(
            panel,
            -1,
            style = wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnsizer.Add((-1,-1),1,wx.EXPAND)
        if self.add:
            btn0 = wx.Button(panel, wx.ID_APPLY)
            btn0.SetLabel(text.more)
            btnsizer.Add(btn0,0,wx.RIGHT,5)
        btnsizer.Add(btn1,0,wx.RIGHT,5)
        btnsizer.Add(btn2,0,wx.RIGHT,5)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer,1,wx.ALL|wx.EXPAND,5)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        mainSizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        mainSizer.Add((1,6))
        panel.SetSizer(mainSizer)
        mainSizer.Layout()
        mainSizer.Fit(self)
        btn2.SetFocus()


        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

        def onOk(evt):
            id = evt.GetId()
            data = ["",[]]
            children = sizer.GetChildren()
            ctrls = []
            for i in range(len(self.labels)):
                ctrl = children[2 * i + 1].GetWindow()
                ctrls.append(ctrl)
                val = ctrl.GetValue()
                if i:
                    if val[1]==len(val[1])*[False]:
                        MessageBox(
                            self,
                            text.message2,
                            text.messBoxTit1,
                            wx.ICON_EXCLAMATION,
                            plugin = self.plugin,
                            time = 20
                            )
                        return  
                    tmp = []
                    for j in range(len(val[0])):
                        if val[1][j]:
                            tmp.append(self.iNamed[val[0][j]])
                    val = tmp
                else:
                    if val == "":
                        MessageBox(
                            self,
                            text.message1,
                            text.messBoxTit1,
                            wx.ICON_EXCLAMATION,
                            plugin = self.plugin,
                            time = 20
                            )
                        return  
                    titles = [j[0] for j in self.grid.GetData()]
                    if val in titles:
                        ix = titles.index(val)
                        if self.add or ix != self.grid.GetSelectedItemIx():
                            MessageBox(
                                self,
                                text.message3 % val,
                                text.messBoxTit2,
                                wx.ICON_EXCLAMATION,
                                plugin = self.plugin,
                                time = 20
                                )
                            return  
                data[i] = val
            if self.add:
                self.grid.AppendRow()
            self.grid.SetRow(data)
            if id == wx.ID_OK:
                self.Close()
            else:
                for i in range(len(self.labels)):
                    val = self.getInitChcs()[1] if i else ""
                    ctrls[i].SetValue(val)
        if self.add:
            btn0.Bind(wx.EVT_BUTTON, onOk)
        btn1.Bind(wx.EVT_BUTTON, onOk)


        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)

        size = self.GetSize()
        self.SetSize(size)
        self.SetMinSize(size)
        self.Raise()
        self.MakeModal(True)
        self.Show()
#===============================================================================

class infDialog(wx.Frame):
    def __init__(
        self,
        plugin,
        parent,
        row
    ):
        mc = row[0]
        mac = mc if not " " in mc else mc[:mc.find(" ")]
        if mac in plugin.infoDialogs.iterkeys() or mac not in plugin.named:
            return
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.STAY_ON_TOP | wx.BORDER_NONE,
            name="NmapInfoDialog",
        )
        self.SetBackgroundColour(wx.BLACK)
        self.SetForegroundColour(wx.Colour(255,255,0))
        self.parent = parent
        self.plugin = plugin
        self.text = plugin.text
        self.row = row
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        infoSizer = wx.GridBagSizer(8, 20)
        self.Bind(wx.EVT_RIGHT_UP, self.OnCloseCommand)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.SetToolTip(self.text.tooltip)

        self.infoSizer = infoSizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        self.RefreshData()
        mainSizer.Add(infoSizer,1,wx.ALL|wx.EXPAND,5)
        mainSizer.Fit(self)
        size = self.GetSize()
        self.SetMinSize(size)
        self.SetSize(size)
        self.Centre()
        if parent:
            self.MakeModal(True)
        plugin.infoDialogs[mac] = self
        self.Show(True)
        BringWindowToTop(self.GetHandle())



        def onClose(evt):
            self.MakeModal(False)
            if self.parent:
                self.parent.Enable(True)
                self.parent.dialog.buttonRow.cancelButton.Enable(True)
                self.parent.EnableButtons(True)
                self.GetParent().GetParent().Raise()
            self.Show(False)
            del self.plugin.infoDialogs[mac]
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

    def RefreshData(self):
        mc = self.row[0]
        nick = self.row[1]
        mac = mc if not " " in mc else mc[:mc.find(" ")]
        man = self.text.unkn if not " " in mc else mc[1+mc.find("("):-1]
        self.SetTitle(nick)
        data = [mac, nick, self.row[2], man]
        grps = []
        for gr, ms in self.plugin.groups.iteritems():
            if mac in ms:
                grps.append(gr)
        grps = ", ".join(grps)
        data.append(grps)
        self.flag = self.plugin.oldState[mac][0] if mac \
            in self.plugin.oldState.iterkeys()  else False
        data.append(self.text.status[int(self.flag)])
        ip = self.plugin.oldState[mac][3] if self.flag else ""
        data.append(ip if not isinstance(ip, list) else \
            str(ip)[1:-1].replace("'","").replace('"','').replace("u",""))
        text = self.text



        def StaticText(txt, bold, status = False):
            st = wx.StaticText(self, -1, txt, pos = ((0,-50)))
            font = st.GetFont()
            font.SetPointSize(1.4*font.GetPointSize())
            if bold:
                font.SetWeight(wx.FONTWEIGHT_BOLD )
            st.SetFont(font)
            if status:
                st.SetForegroundColour(wx.GREEN if self.flag else wx.RED)
            st.Bind(wx.EVT_RIGHT_UP, self.OnCloseCommand)
            st.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            st.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            st.Bind(wx.EVT_MOTION, self.OnMouseMove)
            st.SetToolTip(text.tooltip)
            return st

        infoSizer = self.infoSizer
        infoSizer.Clear(True)
        labels = list(text.header1)
        labels.extend(text.infoLbl1)
        for i in range(len(data)):
            infoSizer.Add(StaticText(labels[i]+":", True),(i,0))
            infoSizer.Add(StaticText(data[i],False, i==5),(i,1))
        infoSizer.Layout()


    def OnCloseCommand(self, evt):
        self.Close()
        

    def OnLeftDown(self, evt):
        self.CaptureMouse()
        x, y = self.ClientToScreen(evt.GetPosition())
        win = evt.GetEventObject()
        if isinstance(win, wx.StaticText):
            childX, childY = win.GetPosition()
            x += childX
            y += childY
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))


    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()


    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)
        evt.Skip()
#===============================================================================

class infGroupDialog(wx.Frame):
    def __init__(
        self,
        plugin,
        parent,
        row
    ):
        grp = row[0]
        if grp in plugin.infoDialogs.iterkeys() or grp not in plugin.groups:
            return
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style = wx.STAY_ON_TOP | wx.BORDER_NONE,
            name="NmapInfoGroupDialog",
        )
        self.SetBackgroundColour(wx.BLACK)
        self.SetForegroundColour(wx.Colour(255,255,0))
        self.parent = parent
        self.plugin = plugin
        self.text = plugin.text
        self.row = row
        self.delta = (0,0)
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.SetTitle(row[0])
        infoSizer = wx.GridBagSizer(8, 20)

        self.Bind(wx.EVT_RIGHT_UP, self.OnCloseCommand)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.SetToolTip(self.text.tooltip)
        self.infoSizer = infoSizer
        self.RefreshData()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        mainSizer.Add(infoSizer, 1, wx.EXPAND|wx.ALL, 5)

        mainSizer.Fit(self) 
        size = self.GetSize()
        self.SetMinSize(size)
        self.SetSize(size)
        self.Centre()
        if parent:
            self.MakeModal(True)
        plugin.groupInfoDialogs[grp] = self
        self.Show(True)
        BringWindowToTop(self.GetHandle())



        def onClose(evt):
            self.MakeModal(False)
            if self.parent:
                self.parent.Enable(True)
                self.parent.dialog.buttonRow.cancelButton.Enable(True)
                self.parent.EnableButtons(True)
                self.GetParent().GetParent().Raise()
            del self.plugin.groupInfoDialogs[grp]
            self.Show(False)
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

    def RefreshData(self):
        mmbrs = self.row[1]
        self.stats = [self.plugin.oldState[i][0] \
            if i in self.plugin.oldState.iterkeys() else False for i in mmbrs]
        if self.stats == len(self.stats)*[True]:
             self.state = 3
        elif self.stats == len(self.stats)*[False]:
            self.state = 1
        else:
            self.state = 2
        state = self.text.grState[self.state]
        data = [self.row[0], state]
        data.extend([self.plugin.named[i] for i in mmbrs])
        text = self.text
        infoSizer = self.infoSizer
        infoSizer.Clear(True)

        def StaticText(txt, bold, status = False, mmbrSt = None):
            st = wx.StaticText(self, -1, txt, pos = ((0,-50)))
            font = st.GetFont()
            font.SetPointSize(1.4*font.GetPointSize())
            if bold:
                font.SetWeight(wx.FONTWEIGHT_BOLD)
            st.SetFont(font)
            if status:
                st.SetForegroundColour(
                    (wx.WHITE,wx.RED, wx.GREEN,wx.BLUE)[self.state]
                )
            if mmbrSt is not None:
                st.SetForegroundColour((wx.RED, wx.GREEN)[int(mmbrSt)])
            st.Bind(wx.EVT_RIGHT_UP, self.OnCloseCommand)
            st.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            st.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            st.Bind(wx.EVT_MOTION, self.OnMouseMove)
            st.SetToolTip(text.tooltip)
            return st

        labels = list(text.header2)
        labels.insert(1, text.infoLbl1[2])
        lenDat = len(data)
        if lenDat > len(labels):
            labels.extend((lenDat-len(labels))*[""])
        for i in range(lenDat):
            label = labels[i]+":" if labels[i] else ""
            infoSizer.Add(StaticText(label, True),(i,0))
            mmbrSt = self.stats[i-2] if i > 1 else None
            infoSizer.Add(StaticText(data[i],False, i==1, mmbrSt),(i,1))
        infoSizer.Layout()


    def OnCloseCommand(self, evt):
        self.Close()
        

    def OnLeftDown(self, evt):
        self.CaptureMouse()
        x, y = self.ClientToScreen(evt.GetPosition())
        win = evt.GetEventObject()
        if isinstance(win, wx.StaticText):
            childX, childY = win.GetPosition()
            x += childX
            y += childY
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))


    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()


    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)
        evt.Skip()
#===============================================================================

class myCheckListBox(wx.CheckListBox):
    items = None
    def __init__(self, parent, id, exChoices):
        wx.CheckListBox.__init__(
            self,
            parent,
            id,
            wx.DefaultPosition,
            wx.DefaultSize,
            exChoices[0],
        )
        self.SetValue(exChoices)

    def SetValue(self, exChoices):
        self.items = exChoices[0]
        for i, val in enumerate(exChoices[1]):
            self.Check(i, val)
    
    def GetValue(self):
        values = []
        for i in range(len(self.items)):
            values.append(self.IsChecked(i))
        return [self.items, values]    
#===============================================================================

class ListCtrl(wx.ListCtrl):

    def __init__(self, parent, header, items, rows, plugin):
        wx.ListCtrl.__init__(
            self,
            parent,
            -1,
            style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.LC_SINGLE_SEL
        )
        self.plugin = plugin
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
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetData(items)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)


    def OnRightClick(self, event):
        if not hasattr(self, "popupIDs"):
            self.popupIDs = (wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef())
            self.Bind(wx.EVT_MENU, self.PostEvent, id=self.popupIDs[0])
            self.Bind(wx.EVT_MENU, self.PostEvent, id=self.popupIDs[1])
            self.Bind(wx.EVT_MENU, self.PostEvent, id=self.popupIDs[2])
            self.Bind(wx.EVT_MENU, self.PostEvent, id=self.popupIDs[3])
        menu = wx.Menu()
        menu.Append(self.popupIDs[0], self.plugin.text.buttons1[0])
        menu.Append(self.popupIDs[1], self.plugin.text.buttons1[1])
        menu.Append(self.popupIDs[2], self.plugin.text.buttons1[2])
        menu.Append(self.popupIDs[3], self.plugin.text.buttons1[3])
        self.PopupMenu(menu)
        menu.Destroy()
        event.Skip()


    def PostEvent(self, event):
        id = event.GetId()
        evt = eg.ValueChangedEvent(self.GetId(),value = self.popupIDs.index(id))
        wx.PostEvent(self, evt)
        event.Skip()


    def SetWidth(self):
        newW = self.GetSize().width
        p = newW/float(self.wk)
        col = self.GetColumnCount()
        w = SYS_VSCROLL_X + self.GetWindowBorderSize()[0]
        for c in range(col-1):
            self.SetColumnWidth(c, p*self.collens[c])
            w += self.GetColumnWidth(c)
        self.SetColumnWidth(col-1, newW-w)


    def OnSize(self, event):
        wx.CallAfter(self.SetWidth)
        event.Skip()


    def OnItemSelected(self, evt):
        self.SelRow(evt.GetSelection())
        evt.Skip()


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


    def DeleteRow(self):
        row = self.selRow
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
        self.EnsureVisible(ix)
        self.SelRow(ix)
        if ix == 0:
            evt = eg.ValueChangedEvent(self.GetId(), value="One")
            wx.PostEvent(self, evt)


    def SetRow(self, rowData):
        row = self.selRow
        for i in range(self.GetColumnCount()):
            self.SetItem(row, i, rowData[i])


    def GetSelectedItemIx(self):
        return self.selRow


    def GetRow(self, row = None):
        row = self.selRow if row is None else row
        rowData=[]
        for i in range(self.GetColumnCount()):
            rowData.append(self.GetItem(row, i).GetText())
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

class GroupListCtrl(ListCtrl):
    cliData = {}
    key = -1
    
    def GetKey(self):
        self.key += 1
        return self.key
        # you can not use row number as the key 
        # there would be a problem after deleting a row        

    def GetRow(self, r = None):
        r = self.selRow if r is None else r
        return [self.GetItem(r, 0).GetText(), self.cliData[self.GetItemData(r)]]


    def SetRow(self, rowData):
        row = self.selRow
        self.SetItem(row, 0, rowData[0])
        key = self.GetKey()
        self.SetItemData(row, key)
        self.cliData[key] = rowData[1]
        val = []
        named = dict([(str(i[0].split(" ")[0]),i[1]) \
            for i in self.plugin.named_grid.GetData()])          
        for item in rowData[1]:
            val.append(named[item])
        if len(val):
            val.sort()
        self.SetItem(row, 1, ", ".join(val))
#===============================================================================

class MessageBox(wx.Dialog):

    def __init__(
        self, parent, message, caption='', flags=0, time = 0, plugin = None
    ):
        PlaySound('SystemExclamation', SND_ASYNC)
        wx.Dialog.__init__(
            self, parent, style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP
        )
        self.SetTitle(plugin.text.messBoxTit0)
        self.SetIcon(plugin.info.icon.GetWxIcon())
        if flags:
            art = None
            if flags & wx.ICON_EXCLAMATION:
                art = wx.ART_WARNING            
            elif flags & wx.ICON_ERROR:
                art = wx.ART_ERROR
            elif flags & wx.ICON_QUESTION:
                art = wx.ART_QUESTION
            elif flags & wx.ICON_INFORMATION:
                art = wx.ART_INFORMATION
            if art is not None:
                bmp = wx.ArtProvider.GetBitmap(art, wx.ART_MESSAGE_BOX, (32,32))
                icon = wx.StaticBitmap(self, -1, bmp)
                icon2 = wx.StaticBitmap(self, -1, bmp)
            else:
                icon = (32,32)
                icon2 = (32,32)
        if caption:
            caption = wx.StaticText(self, -1, caption)
            caption.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        message = wx.StaticText(self, -1, message)
        line = wx.StaticLine(self, -1, size=(1,-1), style = wx.LI_HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add((10, 1)) 

        if time:
            self.cnt = time
            txt = plugin.text.auto % self.cnt
            info = wx.StaticText(self, -1, txt)
            info.Enable(False)
            bottomSizer.Add(info, 0, wx.TOP, 3)
            
            def UpdateInfoLabel(evt):
                self.cnt -= 1
                txt = plugin.text.auto % self.cnt
                info.SetLabel(txt)
                if not self.cnt:
                    self.Close()

            self.Bind(wx.EVT_TIMER, UpdateInfoLabel)
            self.timer = wx.Timer(self)
            self.timer.Start(1000)
        else:
            self.timer = None

        button = wx.Button(self, -1, plugin.text.ok)
        button.SetDefault()
        bottomSizer.Add((1,1),1,wx.EXPAND) 
        bottomSizer.Add(button, 0, wx.RIGHT, 10)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(icon,0,wx.LEFT|wx.RIGHT,10)
        topSizer.Add((1,1),1,wx.EXPAND)
        topSizer.Add(caption,0,wx.TOP,5)
        topSizer.Add((1,1),1,wx.EXPAND)
        topSizer.Add(icon2,0,wx.LEFT|wx.RIGHT,10)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM,10)
        mainSizer.Add(message, 0, wx.EXPAND|wx.LEFT|wx.RIGHT,10)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALL,5)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND|wx.BOTTOM,5)
        
        def OnButton(evt):
            self.Close()
            evt.Skip()
        button.Bind(wx.EVT_BUTTON, OnButton)


        def onClose(evt):
            if self.timer:
                self.timer.Stop()
                del self.timer
            self.MakeModal(False)
            self.GetParent().Raise()
            self.Destroy()

        self.Bind(wx.EVT_CLOSE, onClose)
        self.SetSizer(mainSizer)
        self.Fit()
        self.MakeModal(True)
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler


#===============================================================================

class Nmap(eg.PluginBase):
    text = Text
    task = None
    macs = None
    ips = None
    ouis = None
    counters = {}
    grState = {}
    panel = None
    thrd = None
    infoDialogs = {}
    groupInfoDialogs = {}

    def __init__(self):
        self.AddActionsFromList(ACTIONS)


    def OnComputerSuspend(self, dummy):
        self.__stop__()


    def OnComputerResume(self, dummy):
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        self.__start__(*args)


    def __start__(
        self,
        prefix = "",
        profiles = 8,
        ignored = "",
        ipRng = "",
        named = [],
        groups = [],
        nmp = "",
        evtFilter = len(Text.evtFilter) * [True],
        per = 30
    ):
        if isinstance(profiles, int):
            profiles = [["Default", str(profiles), str(per)]]
            named = [[item[0], item[1], 0] for item in named]
        self.profiles = profiles
        if isinstance(evtFilter, bool): #for backward compatibility
            evtFilter = [evtFilter]
            evtFilter.extend((len(self.text.evtFilter)-2)*[True])
            evtFilter.append(False)
        self.evtFilter = evtFilter
        self.info.eventPrefix = prefix if prefix != "" else self.text.prefix
        self.ignrd = ignored.replace(" ","").split(",")
        self.ipRng = ipRng
        self.devices = named
        self.oldState = {}
        self.infoDialogs = {}
        self.groupInfoDialogs = {}
        self.counters = {}
        self.dataFlag = True
        self.macs = None
        self.ips = None
        self.ouis = None
        self.groups = dict(groups)
        self.grState = {}
        if self.evtFilter[4]:
            self.TriggerEvent(self.text.dataUn)
        self.named, self.iNamed, self.nmdProf = self.getNamed(named)
        for gr in self.groups.iterkeys():
            self.grState[gr]=(
                0,
                [],
                True if self.evtFilter[5] else False
            ) # 0=Unknown,1=Empty,2=Incomplete,3=Complete
        nmp = nmp if nmp else self.GetNmapPath()
        self.myExe = '"%s"' % join(nmp, "nmap.exe")
        self.usedProf = list(set([itm[2] for itm in named]))
        if (not 0 in self.usedProf) and self.evtFilter[0]:
            self.usedProf.append(0)
        t = int(ttime())
        ct = 10 - t % 10
        t = t + ct
        self.workerFlag = False
        self.profCounters = len(self.profiles) * [1]
        self.task = eg.scheduler.AddTask(
            0.01, self.worker, t - 15
        )


    def CloseInfoDialogs(self):
        for dlg in list(self.infoDialogs.itervalues()):
            dlg.Close()
        for dlg in list(self.groupInfoDialogs.itervalues()):
            dlg.Close()

    def __stop__(self):
        if self.task:
            eg.scheduler.CancelTask(self.task)
        wx.CallAfter(self.CloseInfoDialogs)
        self.thrd = None
        self.task = None
        self.macs = None
        self.ips = None
        self.ouis = None
        self.counters = {}
        self.grState = {}
        self.workerFlag = False
        if self.panel:
            wx.CallAfter(self.panel.Enbl, False)


    def GetNmapPath(self):
        """
        Get the path of Nmap's installation directory through querying 
        the Windows registry.
        """
        try:
            args = [_winreg.HKEY_CURRENT_USER,            
                "Software\Nmap"]
            if "PROCESSOR_ARCHITEW6432" in environ:
                args.extend((0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY))
            nmp_reg = _winreg.OpenKey(*args)
            nmp =_winreg.QueryValue(nmp_reg, None)
            _winreg.CloseKey(nmp_reg)
        except WindowsError:
            nmp = None
        return nmp


    def getMac(self, item):
        return str(item if not " " in item else item[:item.find(" ")])


    def getNamed(self, lst):
        named={}
        nmdProf={}
        iNamed={}
        for itm in lst:
            val = self.getMac(itm[0])
            named[val] = itm[1]
            nmdProf[val] = itm[2]
            iNamed[itm[1]] = val
        return (named, iNamed, nmdProf)


    def popen(self, cmd):
        proc = Popen(
            cmd,
            stdout = PIPE,
            stderr = STDOUT,
            creationflags = SW_HIDE,
            shell = True
        )
        data = proc.communicate()[0]
        return (proc.returncode, data)

    
    def getAddresses(self, res):
        macs, ips, ouis = ({},{},{})
        skip = res.find("Nmap done:")
        if skip == -1:
            return (macs, ips, ouis)
        while skip > -1:    
            maci = res.find("MAC Address:",skip+21)
            if maci > -1:
                skip = res.find("Nmap scan report for ", maci) 
                break
            skip = res.rfind("Nmap scan report for ", 0, skip)
        if skip == -1:
            return (macs, ips, ouis)
        res=res[:skip]
        ix = 0
        ouie = 0
        while 1:
            ix=res.find("Nmap scan report for",ouie)
            if ix==-1:
                break
            le=res.find("\r",ix+21)
            ip=res[ix+21:le]
            maci=res.find("MAC Address:",ix+21)+13
            mace=res.find(" ",maci)
            mac=res[maci:mace]
            ouii=res.find("(", mace)+1
            ouie=res.find(")", ouii)
            oui=res[ouii:ouie]
            ips[ip] = mac
            ouis[mac]=oui
            if not mac in macs:
                macs[mac]=ip
            elif isinstance(macs[mac], list):
                macs[mac].append(ip)
            else:
                macs[mac] = [macs[mac], ip]
        return (macs, ips, ouis)

# Old states:
#============
# State A = present, counter OFF [present]
# State B = away,    counter OFF [away]
# State C = present, counter ON  [unknown]
# State D = away,    counter ON  [start]
#
# New (scanned) states:
#======================
# State E = present
# State F = away
#
#
# AE - do nothing
# BE - set state A,                      with event
# CE - set state A, counter turn OFF, without event
# DE - set state A, counter turn OFF, without event/with event (by settings)
#
# AF - set state C, counter turn ON, without event
# BF - do nothing
# CF - counter + 1, check counter a) no overflow, do nothing
#				                  b) overflow -> counter turn OFF, set state B, with event																
# DF - counter + 1, check counter a) no overflow, do nothing
#				                  b) overflow -> counter turn OFF, set state B, without event/with event (by settings)																

    def worker(self, oldT):
        # print "Nmap worker thread"
        activeProfs = []
        for i in range(len(self.profCounters)):
            self.profCounters[i] -= 1
            if not self.profCounters[i]:
                if i in self.usedProf:
                    activeProfs.append(i)
                self.profCounters[i] = int(self.profiles[i][2])/10
        if not activeProfs:
            if self.info.isStarted and self.task is not None:
                newT = oldT + 10 * (1 + int((ttime()-oldT)/10))
                self.task = eg.scheduler.AddTaskAbsolute(newT,self.worker,newT)
            return
        try:
            self.task = 0
            if not self.info.isStarted or self.workerFlag:
                return
            self.workerFlag = True
            res = self.popen('%s -sn -PE -PO -n %s' % (self.myExe, self.ipRng))
            data = res[1].decode(eg.systemEncoding, "ignore")
            # print "data =",data[-60:]
            macs, ips, ouis = self.getAddresses(data)
            macSet = list((set(macs) | set(self.named)) - set(self.ignrd))
            rawAdded = []
            rawRemoved = []
            for element in macSet:
                if not element in self.oldState.iterkeys():
                    self.oldState[element] = [False, 0, True, ""] #state 'start'
                oS_e = self.oldState[element]
                profile=self.nmdProf[element] if element in self.nmdProf else 0
                if profile in activeProfs:
                    factor = int(self.profiles[profile][1])
                    present = element in macs.iterkeys()

                    if present and oS_e[1] is not None:                #CE or DE
                        if element in self.named.iterkeys():
                            if not oS_e[0] and self.evtFilter[1] \
                                and not self.evtFilter[5]:
                                    self.TriggerEvent(
                                        "Present.%s" % self.named[element],
                                        (element, macs[element])
                                    )
                        elif self.evtFilter[0]:
                            rawAdded.append(element)
                        if not oS_e[0]:
                            oS_e[2] = False
                        oS_e = [True, None, oS_e[2], macs[element]]
                    elif present and oS_e[:2] == [False, None]:              #BE
                        if self.evtFilter[1]:
                            self.TriggerEvent(
                                "Present.%s" % self.named[element],
                                (element, macs[element])
                            )
                            oS_e = [True, None, False, oS_e[3]]
                    elif not present and oS_e[:2] == [True, None]:           #AF
                        oS_e[1] = 0 # counter start
                    elif not present and oS_e[1] is not None:          #CF or DF
                        oS_e[1] += 1
                        if oS_e[1] >= factor:
                            if element in self.named.iterkeys():
                                if oS_e[0] or self.evtFilter[1] \
                                    and not self.evtFilter[5]:
                                        self.TriggerEvent(
                                            "Away.%s" % self.named[element],
                                            element
                                        )
                            elif self.evtFilter[0]: 
                                rawRemoved.append(element)
                            if not oS_e[0]:
                                oS_e[2] = False
                            oS_e = [False, None, oS_e[2], oS_e[3]]
                self.oldState[element] = oS_e

            if rawAdded:
                self.TriggerEvent("Connected", rawAdded)
            if rawRemoved:
                self.TriggerEvent("Disconnected",rawRemoved)
        except:
            eg.PrintTraceback()

        grState = self.getGroupStates()
        for gr in self.groups:
            gS = grState[gr]
            if not self.grState[gr][2]: # Must be tested previous condition !
                if self.evtFilter[3]:
                    if len(gS[1]) > len(self.grState[gr][1]):
                        self.TriggerEvent(
                            "Increased.%s" % gr,
                            (gr, gS[1])
                        )
                    elif len(gS[1]) < len(self.grState[gr][1]):
                        self.TriggerEvent(
                            "Decreased.%s" % gr,
                            (gr, gS[1])
                        )
                if self.evtFilter[2]:
                    if gS[0] != self.grState[gr][0]:
                        self.TriggerEvent(
                            "%s.%s" % (self.text.grState[gS[0]],gr),
                            (gr, gS[0])
                        )
            if gS != self.grState[gr]:
                self.grState[gr] = gS


        if self.evtFilter[4] and self.dataFlag:
            self.dataFlag = False
            self.TriggerEvent(self.text.dataAv)
        if self.panel:
            self.panel.Enbl(True)

        self.macs = cpy(macs)
        self.ips = cpy(ips)
        self.ouis = cpy(ouis)
        wx.CallAfter(self.RefreshInfoDialogs)

        if self.info.isStarted and self.task is not None:
            newT = oldT + 10 * (1 + int((ttime()-oldT)/10))
            self.workerFlag = False
            self.task = eg.scheduler.AddTaskAbsolute(newT, self.worker, newT)


    def RefreshInfoDialogs(self):
        for dlg in list(self.infoDialogs.itervalues()):
            dlg.RefreshData()
        for dlg in list(self.groupInfoDialogs.itervalues()):
            dlg.RefreshData()


    def SetIpRangeTsk(self, trItem, args):
        eg.actionThread.Func(trItem.SetArguments)(args) # __stop__ / __start__        
        eg.document.SetIsDirty()
        eg.document.Save()


    def SetIpRange(self, ipr, save):
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        args[3] = ipr
        if save:
            if self.ipRng != ipr:
                ct = currentThread()
                if ct == eg.actionThread._ThreadWorker__thread:
                    trItem.SetArguments(args) #automatically __stop__/__start__      
                    eg.document.SetIsDirty()
                    eg.document.Save()
                else:
                    eg.scheduler.AddTask(0.01, self.SetIpRangeTsk, trItem, args)
        else:
            if self.ipRng != ipr:
                self.__stop__()
                self.__start__(*args)
                

    def getGroupStates(self):
        grState = {}
        for gr in self.groups:
            membs = self.groups[gr]
            st = []
            state = None
            start = False
            for member in membs:
                if not self.oldState[member][0] \
                    and self.oldState[member][1] is not None:
                        state = 0 # Start (unknown)
                        if self.grState[gr][2] and self.evtFilter[5]:
                            start = True
                        break
                elif self.oldState[member][0]:
                    st.append(member)
                if self.grState[gr][2] and self.evtFilter[5]:
                    start |= self.oldState[member][2]
            if state == 0:
                pass
            elif len(st) == len(membs):
                state = 3 #Complete
            elif len(st) > 0 and len(st) < len(membs):
                state = 2 #Incomplete
            elif len(st) == 0:
                state = 1 #Empty
            grState[gr] = (state, st, start)
        return grState


    def Configure(
        self,
        prefix = "",
        profiles = 8,
        ignored = "",
        ipRng = "",
        named = [],
        groups = [],
        nmp = "",
        evtFilter = len(Text.evtFilter) * [True],
        per = 30
    ):
        wx.CallAfter(self.CloseInfoDialogs)
        text = self.text               
        if isinstance(profiles, int):
            profiles = [["Default",str(profiles),str(per)]]
            named = [[item[0], item[1], 0] for item in named]
        if isinstance(evtFilter, bool): #for backward compatibility
            evtFilter = [evtFilter]
            evtFilter.extend((len(self.text.evtFilter)-2)*[True])
            evtFilter.append(False)
        evtFilter = [text.evtFilter, evtFilter]
        prefix = prefix if prefix != "" else text.prefix
        if not nmp:
            nmp = self.GetNmapPath()
            if nmp is None:
                nmp = join(
                    eg.folderPath.ProgramFiles, 
                    "Nmap",
                )
        panel = eg.ConfigPanel()
        panel.profiles = cpy(profiles)

        self.panel = panel
        ttl = panel.dialog.GetTitle()
        panel.dialog.SetTitle(
            "%s - %s - %s %s" % ("Nmap", ttl, text.version, version)
        )

        def onClose(evt):
            self.panel = None
            evt.Skip()
        panel.dialog.Bind(wx.EVT_CLOSE, onClose)
        panel.dialog.buttonRow.cancelButton.Bind(wx.EVT_BUTTON, onClose)
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, onClose)

        label_0 = wx.StaticText(panel, -1, text.label_0)
        label_1 = wx.StaticText(panel, -1, text.label_1)
        label_4 = wx.StaticText(panel, -1, text.ignored)
        label_3 = wx.StaticText(panel, -1, text.ipRng)
        label_5 = wx.StaticText(panel, -1, text.named)
        label_6 = wx.StaticText(panel, -1, text.groups)
        nmpCtrl= eg.DirBrowseButton(
            panel,
            -1,
            dialogTitle = text.nmpFldr,
            buttonText = eg.text.General.browse,
            startDirectory = eg.folderPath.ProgramFiles,
        )
        nmpCtrl.SetValue(nmp)
        prefixCtrl = wx.TextCtrl(panel, -1, prefix)
        profileBtn = wx.Button(panel.dialog, -1, text.btnProfMan)
        ignoredCtrl = wx.TextCtrl(panel, -1, ignored)
        ipRngCtrl = wx.TextCtrl(panel, -1, ipRng)
        label_3.SetToolTip(text.toolTipIp)
        ignoredCtrl.SetToolTip(text.toolTip)
        label_4.SetToolTip(text.toolTip)
        ipRngCtrl.SetToolTip(text.toolTipIp)
        eventFilter = CheckListComboBox(
            panel,
            -1,
            values = evtFilter,
            helpText = text.filter
        )
        nmd = [[i[0],i[1],profiles[i[2]][0]] for i in named]
        named_grid = ListCtrl(panel, text.header1, nmd, 5, self)
        self.named_grid = named_grid
        panel.named_grid = named_grid #used for profile dialog
        group_grid = GroupListCtrl(panel, text.header2, groups, 3, self)

        def add1(evt = None):
            dlg = namedDialog(
                parent = panel,
                plugin = self,
                labels = text.header1,
                data=["", "", ""],
                grid=named_grid,
                add=True,
            )
            wx.CallAfter(
                dlg.ShowNamedDialog,
                text.title1,
            )

        def add2(evt = None):
            dlg = groupDialog(
                parent = panel,
                plugin = self,
                labels = text.header2,
                data=None,
                grid = group_grid,
                names = named_grid,
                add = True,
            )
            wx.CallAfter(
                dlg.ShowGroupDialog,
                text.title2,
            )

        def edit1(evt = None):
            dlg = namedDialog(
                parent = panel,
                plugin = self,
                labels = text.header1,
                data=named_grid.GetRow(),
                grid=named_grid
            )
            wx.CallAfter(
                dlg.ShowNamedDialog,
                text.title1,
            )

        def edit2(evt = None):
            dlg = groupDialog(
                parent = panel,
                plugin = self,
                labels = text.header2,
                data = group_grid.GetRow(),
                grid = group_grid,
                names = named_grid,
            )
            wx.CallAfter(
                dlg.ShowGroupDialog,
                text.title2,
            )

        def delete1(evt = None):
            named_grid.DeleteRow()

        def delete2(evt = None):
            group_grid.DeleteRow()

        def info1(evt = None):
            self.dialog = infDialog(
                self,
                parent = panel,
                row = named_grid.GetRow()
            )

        def info2(evt = None):
            self.dialog = infGroupDialog(
                self,
                parent = panel,
                row = group_grid.GetRow()
            )

        def onButton(evt):
            ix = bttns.index(evt.GetId())
            (add1, edit1, delete1, info1, add2, edit2, delete2, info2)[ix]()
            evt.Skip()

        butlen = len(text.buttons1)
        bttns = []
        def createButtons(szr):
            for i, bttn in enumerate(text.buttons1):
                id = wx.NewIdRef()
                bttns.append(id)
                b = wx.Button(panel, id, bttn)
                szr.Add(b,1)
                if i == 0:
                    b.SetDefault()
                if i != butlen-1:
                    szr.Add((5, -1))
                b.Bind(wx.EVT_BUTTON, onButton, id = id)

        bttnSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        createButtons(bttnSizer1)
        bttnSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        createButtons(bttnSizer2)
       
        namedSizer=wx.BoxSizer(wx.VERTICAL)
        namedSizer.Add(label_5)
        namedSizer.Add(named_grid, 1, flag = wx.EXPAND)
        namedSizer.Add(bttnSizer1,0,wx.TOP|wx.EXPAND,5)        
        groupSizer=wx.BoxSizer(wx.VERTICAL)
        groupSizer.Add(label_6)
        groupSizer.Add(group_grid, 1, flag = wx.EXPAND)
        groupSizer.Add(bttnSizer2,0,wx.TOP|wx.EXPAND,5) 
        Sizer = wx.GridBagSizer(5, 10)
        Sizer.Add(label_0, (0, 0), flag = wx.TOP|ACV)
        Sizer.Add(nmpCtrl, (0, 1), flag = wx.EXPAND)
        Sizer.Add(label_1, (1, 0), flag = wx.TOP|ACV)
        Sizer.Add(prefixCtrl, (1, 1))
        Sizer.Add(label_3, (2, 0), flag = wx.TOP|ACV)
        Sizer.Add(ipRngCtrl, (2, 1), flag = wx.EXPAND)
        Sizer.Add(label_4, (3, 0), flag = wx.TOP|ACV)
        Sizer.Add(ignoredCtrl, (3, 1), flag = wx.EXPAND)
        Sizer.Add(eventFilter, (4, 0), (1, 2), flag = wx.EXPAND)
        Sizer.Add(namedSizer, (5, 0),(1,2), flag = wx.EXPAND|wx.TOP|ACV)
        Sizer.Add(groupSizer, (6, 0),(1,2), flag = wx.EXPAND|wx.TOP|ACV)
        Sizer.AddGrowableCol(1)
        Sizer.AddGrowableRow(5, namedSizer.GetSize()[1])
        Sizer.AddGrowableRow(6, groupSizer.GetSize()[1])
        panel.sizer.Add(Sizer, 1, wx.EXPAND | wx.ALL,10)

        def onProfileBtn(evt):
            dlg = profileDialog(
                parent = panel,
                plugin = self,
                data = cpy(panel.profiles),
            )
            wx.CallAfter(
                dlg.ShowProfileDialog,
                text.title3,
            )
            evt.Skip()
        profileBtn.Bind(wx.EVT_BUTTON, onProfileBtn)

        def onIgnored(evt):
            ignrd = evt.GetString().replace(" ","").split(",")
            named = dict([(str(i[0].split(" ")[0]),i[1],i[2]) \
                for i in self.named_grid.GetData()])
            flag = True
            for mc in ignrd:
                if len(mc) == 17:
                    if match(MAC_PATT, mc) is None:
                        MessageBox(
                            panel,
                            text.message9 % mc,
                            text.messBoxTit4,
                            wx.ICON_EXCLAMATION,
                            plugin = self,
                            time = 20
                            )
                        flag = False
                        break
                    if mc in named:
                        MessageBox(
                            panel,
                            text.message10 % mc,
                            text.messBoxTit3,
                            wx.ICON_EXCLAMATION,
                            plugin = self,
                            time = 20
                            )
                        flag = False
                        break
                else:
                    flag = False
            panel.EnableButtons(flag)
            evt.Skip()
        ignoredCtrl.Bind(wx.EVT_TEXT, onIgnored)

        def enableButtons1(enable):
            if self.macs is None:
                enable = False
            for b in range(1, len(text.buttons1)):
                wx.FindWindowById(bttns[b]).Enable(enable)


        def enableButtons2(enable):
            if self.macs is None:
                enable = False
            for b in range(1+len(text.buttons1),2*len(text.buttons1)):
                wx.FindWindowById(bttns[b]).Enable(enable)

        def Enbl(val):
            def enbl(val, ix):
                for b in range(ix, ix + 4):
                    wx.FindWindowById(bttns[b]).Enable(val)
            named_grid.Enable(val)
            group_grid.Enable(val)
            if not val:
                enbl(False, 0)
                enbl(False, 4)
            else:
                rows = named_grid.GetItemCount()
                if rows:
                    enbl(True, 0)
                else:
                    wx.FindWindowById(bttns[0]).Enable(True)
                rows = group_grid.GetItemCount()
                if rows:
                    enbl(True, 4)
                else:
                    wx.FindWindowById(bttns[4]).Enable(True)
        panel.Enbl = Enbl
        if self.macs is None:
            Enbl(False)

        def OnGridChange1(evt):
            value = evt.GetValue()
            if isinstance(value, int) and value in range(4):
                (add1,edit1,delete1,info1)[value]()
            elif value == "Empty":
                enableButtons1(False)
            elif value == "One":
                enableButtons1(True)
            evt.Skip()
        named_grid.Bind(eg.EVT_VALUE_CHANGED, OnGridChange1)


        def OnGridChange2(evt):
            value = evt.GetValue()
            if isinstance(value, int) and value in range(4):
                (add2, edit2, delete2, info2)[value]()
            elif value == "Empty":
                enableButtons2(False)
            elif value == "One":
                enableButtons2(True)
            evt.Skip()
        group_grid.Bind(eg.EVT_VALUE_CHANGED, OnGridChange2)

        panel.dialog.buttonRow.Add(profileBtn)


        while panel.Affirmed():
            pN = [n[0] for n in panel.profiles]
            named = [[i[0], i[1], pN.index(i[2])] for i in named_grid.GetData()]
            panel.SetResult(
                prefixCtrl.GetValue(),
                panel.profiles,
                ignoredCtrl.GetValue(),
                ipRngCtrl.GetValue(),
                named,
                group_grid.GetData(),
                nmpCtrl.GetValue(),
                eventFilter.GetValue()[1]
            )
#===============================================================================

class GetMacAddress(eg.ActionBase):
    
    class text:
        label = "IP address:"
        notPres = 'IP address "%s" not present'

    def __call__(self, ip = ""):
        ip = eg.ParseString(ip).replace(" ","")
        tmp = [(val[3], key) for key, val \
            in self.plugin.oldState.iteritems() if val[0]]
        tmp2 = {}
        for item in tmp:
            if isinstance(item[0], unicode):
                tmp2[item[0]] = item[1]
            elif isinstance(item[0], list):
                for i in item[0]:
                    tmp2[i] = item[1]
        if ip in self.plugin.ips:
            return self.plugin.ips[ip]
        elif ip in tmp2.iterkeys():
            return tmp2[ip]
        else:
            return self.text.notPres % ip
        

    def Configure(self, ip = ""):
        panel = eg.ConfigPanel(self)
        ipLbl = wx.StaticText(panel, -1, self.text.label)
        ipCtrl = wx.TextCtrl(panel, -1, ip)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(ipLbl,0,ACV)
        sizer.Add(ipCtrl,1,wx.EXPAND|wx.LEFT, 5)
        panel.sizer.Add(sizer,0,wx.EXPAND|wx.ALL,10)
        while panel.Affirmed():
            panel.SetResult(
                ipCtrl.GetValue(),
            )
#===============================================================================

class GetIpAddress(eg.ActionBase):
    
    class text:
        label = "MAC address:"
        notPres = 'MAC address "%s" not present'

    def __call__(self, mac = ""):
        mac = eg.ParseString(mac).upper()
        if mac in self.plugin.macs:
            return self.plugin.macs[mac]
        elif mac in self.plugin.oldState and self.plugin.oldState[mac][0]:
            return self.plugin.oldState[mac][3]
        else:
            return self.text.notPres % mac
        

    def Configure(self, mac = ""):
        panel = eg.ConfigPanel(self)
        macLbl = wx.StaticText(panel, -1, self.text.label)
        macCtrl = wx.TextCtrl(panel, -1, mac)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(macLbl,0,ACV)
        sizer.Add(macCtrl,1,wx.EXPAND|wx.LEFT, 5)
        panel.sizer.Add(sizer,0,wx.EXPAND|wx.ALL,10)
        while panel.Affirmed():
            panel.SetResult(
                macCtrl.GetValue(),
            )
#===============================================================================

class SetIpRange(eg.ActionBase):
    
    class text:
        label = "IP address range:"
        rbLabel = "Persistence of change"
        choices = (
            "Make the change only temporarily", 
            "Make the change persistent (and automatically save the document)"
        )
        labels = ("temporarily", "persistent")

    def __call__(self, ipr = "", save = 1):
        ipr = eg.ParseString(ipr)
        self.plugin.SetIpRange(ipr, save)


    def GetLabel(self, ipr, save):
        return "%s: %s (%s)" % (self.name, ipr, self.text.labels[save])


    def Configure(self, ipr = "", save = 1):
        panel = eg.ConfigPanel(self)
        text = self.text
        iprLbl = wx.StaticText(panel, -1, text.label)
        iprCtrl = wx.TextCtrl(panel, -1, ipr)
        saveCtrl = wx.RadioBox(
            panel, 
            -1, 
            text.rbLabel,
            choices = text.choices,
            style = wx.RA_SPECIFY_ROWS
        )
        saveCtrl.SetSelection(save)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(iprLbl, 0, ACV)
        hSizer.Add(iprCtrl, 1, wx.EXPAND|wx.LEFT, 5)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(hSizer, 0, wx.EXPAND)
        mainSizer.Add(saveCtrl, 0, wx.TOP|wx.EXPAND, 20)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND|wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(
                iprCtrl.GetValue(),
                saveCtrl.GetSelection()
            )
#===============================================================================

class GetDeviceState(eg.ActionBase):
    oldRb = None
    
    class text:
        chooseLbl = "Select device by:"
        devLbl = "Device:"
        chooses = ("Name", "MAC address", "IP address")
        res = "Result to return as:"
        kinds = ('Away / Present','0 / 1','False / True')

    def __call__(self, choose = 0, dev = "", res=0):
        if not self.plugin.macs:
            return None
        dev = eg.ParseString(dev)
        if choose == 0:
            dev = self.plugin.iNamed[dev] if dev in self.plugin.iNamed else ""
        elif choose == 2:
            dev = self.plugin.ips[dev] if dev in self.plugin.ips else ""
        b = self.plugin.oldState[dev][0] \
            if dev in self.plugin.oldState.iterkeys() else False
        i = int(b)
        if self.value:
            return [self.plugin.text.status[i], i, b][res]
        elif self.value is None and not self.plugin.panel:
            nmd = dict([(
                self.plugin.getMac(i[0]),
                [i[0],i[1],self.plugin.profiles[i[2]][0]]
            ) for i in self.plugin.devices])
            if dev in nmd:
                wx.CallAfter(
                    infDialog,
                    self.plugin,
                    None,
                    nmd[dev]
                )
        elif dev in self.plugin.infoDialogs.iterkeys():
                self.plugin.infoDialogs[dev].Close()


    def GetLabel(self, choose, dev, res):
        return "%s: %s" % (self.name, dev)


    def Configure(self, choose = 0, dev = "", res=0):
        text = self.text
        panel = eg.ConfigPanel(self)
        chooseSizer = wx.BoxSizer(wx.HORIZONTAL)
        chooseLbl=wx.StaticText(panel,-1,text.chooseLbl)
        devLbl=wx.StaticText(panel,-1,text.devLbl)
        rb0=panel.RadioButton(choose==0,text.chooses[0], style=wx.RB_GROUP)
        rb1=panel.RadioButton(choose==1,text.chooses[1])
        rb2=panel.RadioButton(choose==2,text.chooses[2])
        devCtrl = wx.ComboBox(panel, -1, choices = [],style=wx.CB_DROPDOWN)
        devCtrl.SetValue(dev)
        chooseSizer.Add(rb0)
        chooseSizer.Add(rb1, 0, wx.LEFT, 10)
        chooseSizer.Add(rb2, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(3, 2, 10, 20)
        topSizer.AddGrowableCol(1)
        topSizer.Add(chooseLbl)
        topSizer.Add(chooseSizer)
        topSizer.Add(devLbl,0,ACV)
        topSizer.Add(devCtrl, 0, wx.EXPAND)

        def onRadioBox(evt = None, choose = None):
            newVal = ""
            rb = (rb0, rb1, rb2).index(evt.GetEventObject()) if evt else choose
            macs = list(self.plugin.named.iterkeys())
            if rb == 1:
                chcs = macs
            elif rb == 2:
                ips = self.plugin.macs
                tmp = [ips[mac] for mac in macs if mac in ips]
                chcs = []
                for i in tmp:
                    if isinstance(i, list):
                        chcs.extend(i)
                    else:
                        chcs.append(i)                
            else:
                chcs = list(self.plugin.iNamed.iterkeys())
            if self.oldRb is not None:
                oldVal = devCtrl.GetValue()
                if self.oldRb == 1: #mac
                    if rb == 0:     #name
                        newVal = self.plugin.named[oldVal] if\
                            oldVal in self.plugin.named else ""
                    if rb == 2:     #ip
                        newVal = self.plugin.macs[oldVal] if\
                            oldVal in self.plugin.macs else ""
                        newVal = newVal[0] if\
                            isinstance(newVal, list) else newVal
                elif self.oldRb == 2: #ip
                    newVal = self.plugin.ips[oldVal] if\
                        oldVal in self.plugin.ips else ""         # ip->mac
                    if rb == 0: #name
                        newVal = self.plugin.named[newVal] if\
                            newVal in self.plugin.named else ""
                else: #name
                    newVal = self.plugin.iNamed[oldVal] if\
                        oldVal in self.plugin.iNamed else ""      # name->mac
                    if rb == 2: #ip
                        newVal = self.plugin.macs[newVal] if\
                            newVal in self.plugin.macs else ""
                        newVal = newVal[0] if\
                            isinstance(newVal, list) else newVal
            self.oldRb = rb
            devCtrl.Clear()
            devCtrl.AppendItems(chcs)
            devCtrl.SetValue(newVal)
            if evt:
                evt.Skip()
        onRadioBox(choose = choose)
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb2.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        devCtrl.SetValue(dev)

        if self.value:
            resSizer = wx.BoxSizer(wx.HORIZONTAL)
            rb3=panel.RadioButton(res==0, text.kinds[0], style=wx.RB_GROUP)
            rb4 = panel.RadioButton(res==1, text.kinds[1])
            rb5 = panel.RadioButton(res==2, text.kinds[2])
            resLbl=wx.StaticText(panel,-1,text.res)
            resSizer.Add(rb3)
            resSizer.Add(rb4, 0, wx.LEFT, 10)
            resSizer.Add(rb5, 0, wx.LEFT, 10)
            topSizer.Add(resLbl,0,ACV)
            topSizer.Add(resSizer)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 1, wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)

        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue()) + 2*int(rb2.GetValue()),
                devCtrl.GetValue(),
                int(rb4.GetValue())+2*int(rb5.GetValue()) if self.value else 0
            )
#===============================================================================

class GetGroupState(eg.ActionBase):
    
    class text:
        grpLbl = "Group:"
        res = "Result to return as:"
        kinds = ('Unknown / Empty / Icomplete / Complete', '0 / 1 / 2 / 3',)

    def __call__(self, grp = "", res=0):
        if not self.plugin.macs:
            return None
        grp = eg.ParseString(grp)
        if grp in self.plugin.groups:
            if self.value:
                if grp in self.plugin.grState:
                    i = self.plugin.grState[grp][0]
                    return [self.plugin.text.grState[i], i][res]
            elif self.value is None and not self.plugin.panel:
                wx.CallAfter(
                    infGroupDialog,
                    self.plugin,
                    None,
                    (grp, self.plugin.groups[grp])
                )
            elif grp in self.plugin.groupInfoDialogs.iterkeys():
                self.plugin.groupInfoDialogs[grp].Close()


    def GetLabel(self, grp, res):
        return "%s: %s" % (self.name, grp)


    def Configure(self, grp = "", res=0):
        text = self.text
        panel = eg.ConfigPanel(self)
        grpLbl=wx.StaticText(panel,-1,text.grpLbl)
        chcs = list(self.plugin.groups.iterkeys()) if self.plugin.groups else []
        grpCtrl = wx.ComboBox(panel, -1, choices = chcs,style=wx.CB_DROPDOWN)
        grpCtrl.SetValue(grp)
        topSizer = wx.FlexGridSizer(3, 2, 10, 20)
        topSizer.AddGrowableCol(1)
        topSizer.Add(grpLbl,0,ACV)
        topSizer.Add(grpCtrl, 0, wx.EXPAND)

        if self.value:
            resLbl=wx.StaticText(panel,-1,text.res)
            resSizer = wx.BoxSizer(wx.HORIZONTAL)
            rb0=panel.RadioButton(res==0, text.kinds[0], style=wx.RB_GROUP)
            rb1 = panel.RadioButton(res==1, text.kinds[1])
            resSizer.Add(rb0)
            resSizer.Add(rb1, 0, wx.LEFT, 10)
            topSizer.Add(resLbl,0,ACV)
            topSizer.Add(resSizer)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 1, wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)

        while panel.Affirmed():
            panel.SetResult(
                grpCtrl.GetValue(),
                int(rb1.GetValue()) if self.value else 0
            )
#===============================================================================

class GetDeviceList(eg.ActionBase):

    class text:
        stateLbl = "Device state:"
        state = ("Away", "Present", "All named")
        res = "Result to return as:"
        kinds = ('MAC addresses', 'Names', 'Dict. MAC: Name', 'Dict. Name: MAC')


    def __call__(self, state = 1, res = 0):
        sp = self.plugin
        if not sp.macs:
            return None
        if state == 1:
            macs = list(set(sp.named).intersection(set(sp.macs)))
        elif state == 0:
            macs = list(set(sp.named) - set(sp.macs))
        else:
            macs = sp.named.iterkeys()

        if res == 1:
            result = [sp.named[item] for item in macs]
        elif res == 2:
            result = dict([(item, sp.named[item]) for item in macs])
        elif res == 3:
            result = dict([(sp.named[item], item) for item in macs])
        else:
            result = macs
        return result


    def GetLabel(self, state, res):
        return "%s: %s" % (self.name, self.text.state[state])


    def Configure(self, state = 1, res = 0):
        text = self.text
        panel = eg.ConfigPanel(self)
        stateLbl=wx.StaticText(panel,-1,text.stateLbl)
        resLbl=wx.StaticText(panel,-1,text.res)
        stateSizer = wx.BoxSizer(wx.HORIZONTAL)
        resSizer = wx.BoxSizer(wx.HORIZONTAL)
        rb0=panel.RadioButton(state==0, text.state[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(state==1, text.state[1])
        rb2 = panel.RadioButton(state==2, text.state[2])
        rb3=panel.RadioButton(res==0, text.kinds[0], style=wx.RB_GROUP)
        rb4 = panel.RadioButton(res==1, text.kinds[1])
        rb5 = panel.RadioButton(res==2, text.kinds[2])
        rb6 = panel.RadioButton(res==3, text.kinds[3])
        stateSizer.Add(rb0)
        stateSizer.Add(rb1, 0, wx.LEFT, 10)
        stateSizer.Add(rb2, 0, wx.LEFT, 10)
        resSizer.Add(rb3)
        resSizer.Add(rb4, 0, wx.LEFT, 10)
        resSizer.Add(rb5, 0, wx.LEFT, 10)
        resSizer.Add(rb6, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(2, 2, 20, 30)
        topSizer.Add(stateLbl,0,ACV)
        topSizer.Add(stateSizer)
        topSizer.Add(resLbl,0,ACV)
        topSizer.Add(resSizer)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 1, wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)


        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue())+2*int(rb2.GetValue()),
                int(rb4.GetValue())+2*int(rb5.GetValue())+3*int(rb6.GetValue())
            )
#===============================================================================

class GetGroupList(eg.ActionBase):

    class text:
        stateLbl = "Group state:"
        res = "Result to return as:"
        kinds = ('Group names', 'Dictionary  Group name: Members')


    def __call__(self, state = 2, res = 0):
        sp = self.plugin
        if not sp.macs:
            return None
        tmp = list(self.plugin.grState.iteritems())
        rslt = [itm[0] for itm in tmp if itm[1][0] == state]
        if res:
            rslt = dict([(gr, self.plugin.groups[gr]) for gr in rslt])
        return rslt


    def GetLabel(self, state, res):
        return "%s: %s" % (self.name, self.plugin.text.grState[state])


    def Configure(self, state = 2, res = 0):
        state = state - 1
        text = self.text
        panel = eg.ConfigPanel(self)
        stateLbl=wx.StaticText(panel,-1,text.stateLbl)
        resLbl=wx.StaticText(panel,-1,text.res)
        stateSizer = wx.BoxSizer(wx.HORIZONTAL)
        resSizer = wx.BoxSizer(wx.HORIZONTAL)
        states = self.plugin.text.grState[1:]
        rb0 = panel.RadioButton(state==0, states[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(state==1, states[1])
        rb2 = panel.RadioButton(state==2, states[2])
        rb3 = panel.RadioButton(res==0, text.kinds[0], style=wx.RB_GROUP)
        rb4 = panel.RadioButton(res==1, text.kinds[1])
        stateSizer.Add(rb0)
        stateSizer.Add(rb1, 0, wx.LEFT, 10)
        stateSizer.Add(rb2, 0, wx.LEFT, 10)
        resSizer.Add(rb3)
        resSizer.Add(rb4, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(2, 2, 20, 30)
        topSizer.Add(stateLbl,0,ACV)
        topSizer.Add(stateSizer)
        topSizer.Add(resLbl,0,ACV)
        topSizer.Add(resSizer)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 1, wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)

        while panel.Affirmed():
            panel.SetResult(
                1 + int(rb1.GetValue())+2*int(rb2.GetValue()),
                int(rb4.GetValue())
            )
#===============================================================================

class CloseInfoDialogs(eg.ActionBase):

    def __call__(self):
        self.plugin.CloseInfoDialogs()
#===============================================================================

ACTIONS = (
    ( eg.ActionGroup, 'GetterActions', 'Getter actions', 'Getter actions',(
        (
            GetMacAddress,
            'GetMacAddress',
            'Get MAC address',
            "Returns MAC address assigned to the specified IP address.",
            None
        ),
        (
            GetIpAddress,
            'GetIpAddress',
            "Get IP address",
            "Returns IP address(-es) assigned to the specified MAC address.",
            None
        ),
        (
            GetDeviceState,
            'GetDeviceState',
            "Get device status",
            "Returns current status (away/present) of selected device.",
            True
        ),
        (
            GetGroupState,
            'GetGroupState',
            "Get group status",
            "Returns current status (empty/.../complete) of selected group.",
            True
        ),
        (
            GetDeviceList,
            'GetDeviceList',
            "Get device list",
            """Returns a list (or dictionary) of (named) devices \
                that are in the specified state.""",
            None
        ),
        (
            GetGroupList,
            'GetGroupList',
            "Get group list",
            """Returns a list (or dictionary) of groups \
                that are in the specified state.""",
            None
        ),
    )),
    ( eg.ActionGroup, 'InfoDialogs', 'Info dialogs', 'Info dialogs',(
        (
            GetDeviceState,
            'ShowDeviceInfo',
            'Open device info dialog',
            "Opens device info dialog.",
            None
        ),
        (
            GetDeviceState,
            'CloseDeviceInfo',
            'Close device info dialog',
            "Closes device info dialog.",
            False
        ),
        (
            GetGroupState,
            'ShowGroupInfo',
            "Open group info dialog",
            "Opens group info dialog.",
            None
        ),
        (
            GetGroupState,
            'CloseGroupInfo',
            "Close group info dialog",
            "Closes group info dialog.",
            False
        ),
        (
            CloseInfoDialogs,
            'CloseInfoDialogs',
            "Close all info dialogs",
            "Closes all info dialogs.",
            None
        ),
    )),
    (
        SetIpRange,
        'SetIpRange',
        'Set IP address range',
        "Sets IP address range.",
        None
    ),
)
#===============================================================================

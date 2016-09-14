# -*- coding: utf-8 -*-

version="0.1.7"

# Copyright (C)  2008-2011 Pako  (lubos.ruckl@quick.cz)
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
# 0.1.7  by Pako 2011-04-11 08:33 UTC+1
#        - added eg.ParseString for some inputs
# 0.1.6  by Pako 2010-04-15 15:27 GMT+1
#===============================================================================

eg.RegisterPlugin(
    name = "File Operations",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{50D933C5-F93B-4A8A-A6CE-95A40F906036}",
    createMacrosOnAdd = False,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAA"
        "ABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAINSURBVBgZBcG/r55z"
        "GAfg6/4+z3va01NHlYgzEfE7MdCIGISFgS4Gk8ViYyM2Mdlsko4GSf8Do0FLRCIkghhY"
        "JA3aVBtEz3nP89wf11VJvPDepdd390+8Nso5nESBQoq0pfvXm9fzWf19453LF85vASqJ"
        "lz748vInb517dIw6EyYBIIG49u+xi9/c9MdvR//99MPPZ7+4cP4IZhhTPbwzT2d+vGoa"
        "VRRp1rRliVvHq+cfvM3TD82+7mun0o/ceO7NT+/4/KOXjwZU1ekk0840bAZzMQ2mooqh"
        "0A72d5x/6sB9D5zYnff3PoYBoWBgFKPKqDKqjCpjKr//dcu9p489dra88cydps30KswA"
        "CfNEKanSaxhlntjJ8Mv12Paie+vZ+0+oeSwwQ0Iw1xAR1CiFNJkGO4wu3ZMY1AAzBI0q"
        "SgmCNJsJUEOtJSMaCTBDLyQ0CknAGOgyTyFFiLI2awMzdEcSQgSAAKVUmAeNkxvWJWCG"
        "tVlDmgYQ0GFtgg4pNtOwbBcwQy/Rife/2yrRRVI0qYCEBly8Z+P4qMEMy7JaVw72N568"
        "e+iwhrXoECQkfH91kY7jwwXMsBx1L93ZruqrK6uuiAIdSnTIKKPLPFcvay8ww/Hh+ufe"
        "znTXu49v95IMoQG3784gYXdTqvRmqn/Wpa/ADFX58MW3L71SVU9ETgEIQQQIOOzub+fh"
        "IvwPRDgeVjWDahIAAAAASUVORK5CYII="
    ),
    description = (
        "File Operations (reading, periodical reading and writing)."
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=1011"
)
#===============================================================================

import os
import time
import codecs
from threading import Thread, Event

def String2Hex(strng, length = '2'):
    tmp = []
    s2h = "%0" + length + "X "
    for c in strng:
        tmp.append( s2h % ord( c ) )
    return ''.join( tmp ).strip()
#===============================================================================

class ObservationThread(Thread):
    def __init__(
        self,
        stp,
    ):
        self.abort = False
        self.aborted = False
        self.lastCheck = 0
        self.threadFlag = Event()
        #self.firstRun = True

        self.inCoding = stp[0]
        self.fileName = eg.ParseString(stp[1])
        self.mode = stp[2]
        self.errDecMode = stp[3]
        self.inPage = stp[4]
        self.fromLine = stp[5]
        self.direction = stp[6]
        self.lines = stp[7]
        self.period = stp[8]
        self.evtName = eg.ParseString(stp[9])
        self.trigger = stp[10]
        self.oldData = None
        Thread.__init__(self, name = self.evtName.encode('unicode_escape')+'_Thread')

    def run(self):
        while 1:
            errorList = ('strict','ignore','replace')
            try:
                input = codecs.open(self.fileName,'r',self.inPage, errorList[self.errDecMode])
            except:
                raise
            else:
                if self.lines > 0:
                    data = input.readlines()
                    if self.direction == 0: #from beginning
                        data = data[self.fromLine-1:self.fromLine+self.lines-1]
                    else:              #from end
                        if self.fromLine-self.lines < 1:
                            data = data[-self.fromLine:]
                        else:
                            data = data[-self.fromLine:-(self.fromLine-self.lines)]
                    if self.mode == 2:      #one string
                        data = ''.join(data)
                    elif self.mode == 0:    #without CR/LF
                        tmp = []
                        for line in data:
                            tmp.append(line.rstrip())
                        data = tmp
                    if self.lines == 1:
                        if len(data) > 0: #empty file ?
                            data = data[0]
                        else:
                            data = ''
                else:                  #whole file
                    data = input.read()
                try:
                    input.close()
                except:
                    raise
                flag = True
                while True:
                    if self.trigger == 0:   #always
                        break
                    elif self.trigger == 1: #always if not empty
                        if self.mode == 2:
                            if data != '':
                                break
                        else:
                            if data != []:
                                break
                    elif self.trigger == 2: #only at change
                        if data != self.oldData:
                            break
                    else:                   #only at change and not empty
                        if data != self.oldData:
                            if self.mode == 2:
                                if data != '':
                                    break
                            else:
                                if data != []:
                                    break
                    flag = False
                    break
                if flag:
                    eg.TriggerEvent(self.evtName, payload = data, prefix = 'File')
                self.oldData = data

            if self.abort:
                break
            self.lastCheck = time.time()
            self.threadFlag.wait(self.period)
            self.threadFlag.clear()
        self.aborted = True


    def AbortObservation(self, close=False):
        self.abort = True
        self.threadFlag.set()
#===============================================================================

class FileOperations(eg.PluginClass):
    def __init__(self):
        self.AddAction(Read)
        self.AddAction(ReadPeriodically)
        self.AddAction(AbortPeriodicalRead)
        self.AddAction(AbortAllPeriodicalRead)
        self.AddAction(Write)
        self.observThreads = {}
        self.observData = []


    def StartObservation(
        self,
        stp,
    ):
        observName = eg.ParseString(stp[9])
        if observName in self.observThreads:
            ot = self.observThreads[observName]
            if ot.isAlive():
                ot.AbortObservation()
            del self.observThreads[observName]
        ot = ObservationThread(
            stp,
        )
        ot.start()
        self.observThreads[observName] = ot

    def AbortObservation(self, observName):
        if observName in self.observThreads:
            ot = self.observThreads[observName]
            ot.AbortObservation()

    def AbortAllObservations(self, close=False):
        thrds = list(enumerate(self.observThreads))
        thrds.reverse()
        for i, item in thrds:
            ot = self.observThreads[item]
            ot.AbortObservation(close)


    def Configure(self, *args):
        panel = eg.ConfigPanel(self, resizable=True)

        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.header),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        mySizer = wx.GridBagSizer(5, 5)

        observListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)

        for i, colLabel in enumerate(self.text.colLabels):
            observListCtrl.InsertColumn(i, colLabel)

        #setting cols width
        observListCtrl.InsertStringItem(0, 30*"X")
        observListCtrl.SetStringItem(0, 1, 16*"X")
        observListCtrl.SetStringItem(0, 2, 16*"X")

        size = 0
        for i in range(3):
            observListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            size += observListCtrl.GetColumnWidth(i)

        observListCtrl.SetMinSize((size, -1))

        mySizer.Add(observListCtrl, (0,0), (1, 4), flag = wx.EXPAND)

        #buttons
        abortButton = wx.Button(panel, -1, "Abort")
        mySizer.Add(abortButton, (1,0))

        abortAllButton = wx.Button(panel, -1, "Abort all")
        mySizer.Add(abortAllButton, (1,1), flag = wx.ALIGN_CENTER_HORIZONTAL)

        refreshButton = wx.Button(panel, -1, "Refresh")
        mySizer.Add(refreshButton, (1,3), flag = wx.ALIGN_RIGHT)

        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(2)

        def PopulateList (event=None):
            observListCtrl.DeleteAllItems()
            row = 0
            for i, item in enumerate(self.observThreads):
                t = self.observThreads[item]
                if t.isAlive():
                    observListCtrl.InsertStringItem(row, os.path.split(t.fileName)[1])
                    observListCtrl.SetStringItem(row, 1, t.evtName)
                    observListCtrl.SetStringItem(row, 2, str(t.period) + " sec")
                    row += 1
            ListSelection(wx.CommandEvent())

        def OnAbortButton(event):
            item = observListCtrl.GetFirstSelected()
            while item != -1:
                cell = observListCtrl.GetItem(item,1)
                evtName = cell.GetText()
                ot = self.observThreads[evtName]
                self.AbortObservation(evtName)
                while not ot.aborted:
                    pass
                item = observListCtrl.GetNextSelected(item)
            PopulateList()
            event.Skip()

        def OnAbortAllButton(event):
            self.AbortAllObservations()
            PopulateList()
            event.Skip()

        def ListSelection(event):
            flag = observListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            event.Skip()

        def OnSize(event):
            observListCtrl.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER)
            event.Skip()

        PopulateList()

        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        observListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        observListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)

        while panel.Affirmed():
            panel.SetResult(*args)

    #function to fill the action's Comboboxes
    def GetObservData(self):
        self.observData.sort(lambda a,b: cmp(a[1].lower(), b[1].lower()))
        return self.observData

    #function to collect data for action's Comboboxes
    def AddObservData(self, stp):
        item = (os.path.split(stp[1])[1],stp[9])
        if not item in self.observData:
            self.observData.append(item)

    class text:
        FilePath = "Read file:"
        browseFileDialogTitle = "Choose the file"
        txtMode = "Line(s) return like as a:"
        listNotIncluding = "List of line strings without CR/LF"
        listIncluding = "List of line strings including CR/LF"
        oneNotIncluding = "String without CR/LF"
        oneIncluding = "String including CR/LF"
        oneString = "One string (including CR/LF)"
        systemPage = "system code page (%s)"
        defaultIn = "unicode (UTF-8)"
        inputPage = "Input data coding:"
        txtDecErrMode = "Error handling during decoding:"
        strict = "Raise an exception"
        ignore = "Ignore (skip bad chars)"
        replace = "Replace bad chars"
        lineNum = "Start read at line number:"
        begin = "from the beginning"
        end = "from the end"
        readAhead = "Read"
        readBehind = "lines (0 = whole file)"
        intervalLabel = "Refresh interval (s):"
        evtNameLabel = "Observation and event name:"
        triggerLabel = "Event trigger:"
        triggerChoice = (
            "always",
            "always if not empty",
            "only at changes",
            "only at changes and if not empty"
        )
        header = "Currently active file observations:"
        colLabels = (
            "File",
            "Event name",
            "Interval")
#===============================================================================

class Read(eg.ActionClass):
    name = "Read text from file"
    description = "Reads text from selected file."

    def __call__(
        self,
        inCoding = 0,
        fileName = '',
        mode = 0,
        errDecMode = 0,
        inPage = "",
        fromLine = 1,
        direction = 0,
        lines = 1,
    ):
        fileName = eg.ParseString(fileName)
        errorList = ('strict', 'ignore', 'replace')
        try:
            input = codecs.open(fileName, 'r', inPage, errorList[errDecMode])
        except:
            raise
        else:
            data = input.readlines()
            if lines == 0:
                direction = 0
                lines = len(data)
                fromLine = 1
            if direction == 0: #from beginning
                data = data[fromLine-1:fromLine+lines-1]
            else:              #from end
                if fromLine-lines < 1:
                    data = data[-fromLine:]
                else:
                    data = data[-fromLine:-(fromLine-lines)]
            if mode == 2:      #one string
                data = ''.join(data)
            elif mode == 0:    #without CR/LF
                tmp = []
                for line in data:
                    tmp.append(line.rstrip())
                data = tmp
            if lines == 1:
                if len(data) > 0: #empty file ?
                    data = data[0]
                else:
                    data = ''
            try:
                input.close()
            except:
                raise
            return data

    def GetLabel(
        self,
        inCoding,
        fileName,
        mode,
        errDecMode,
        inPage,
        fromLine,
        direction,
        lines = 1,
    ):
        return '%s: %s' % (str(self.name), os.path.split(fileName)[1])

    def Configure(
        self,
        inCoding = 0,
        fileName = '',
        mode = 0,
        errDecMode = 0,
        inPage="",
        fromLine=1,
        direction = 0,
        lines = 1,
    ):
        from codecsList import codecsList
        panel = eg.ConfigPanel(self)
        text = self.plugin.text
        self.mode = mode
    #Controls
        inPageText = wx.StaticText(panel, -1, text.inputPage)
        labelMode = wx.StaticText(panel, -1, text.txtMode)
        labelDecErrMode = wx.StaticText(panel, -1, text.txtDecErrMode)
        fileText = wx.StaticText(panel, -1, text.FilePath)
        filepathCtrl = eg.FileBrowseButton(
            panel,
            -1,
            initialValue=fileName,
            labelText="",
            fileMask="*.*",
            buttonText=eg.text.General.browse,
            dialogTitle=text.browseFileDialogTitle
        )
        width = labelDecErrMode.GetTextExtent(text.txtDecErrMode)[0]
        choiceDecErrMode = wx.Choice(
            panel,
            -1,
            size = ((width,-1)),
            choices=(text.strict, text.ignore, text.replace)
        )
        choiceDecErrMode.SetSelection(errDecMode)
        choices = [text.systemPage % eg.systemEncoding, text.defaultIn]
        choices.extend(codecsList)
        inPageCtrl = wx.Choice(panel,-1,choices=choices)
        inPageCtrl.SetSelection(inCoding)
        lineNumLbl=wx.StaticText(panel, -1, text.lineNum)
        fromLineNumCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            fromLine,
            min = 1,
            max = 999,
        )
        rb0 = panel.RadioButton(not direction, text.begin, style=wx.RB_GROUP)
        rb1 = panel.RadioButton(direction, text.end)
        lblAhead = wx.StaticText(panel, -1, text.readAhead)
        lblBehind = wx.StaticText(panel, -1, text.readBehind)
        linesNumCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            lines,
            min = 0,
            max = 999,
        )
        w0 = inPageCtrl.GetTextExtent(text.listNotIncluding)[0]
        w1 = inPageCtrl.GetTextExtent(text.listIncluding)[0]
        w2 = inPageCtrl.GetTextExtent(text.oneNotIncluding)[0]
        w3 = inPageCtrl.GetTextExtent(text.oneIncluding)[0]
        w4 = inPageCtrl.GetTextExtent(text.oneString)[0]
        width = max(w0,w1,w2,w3,w4)+30
        choiceMode = wx.Choice(panel,-1,size=(width,-1))
    #Sizers
        topSizer = wx.FlexGridSizer(2,0,2,15)
        topSizer.AddGrowableCol(0,1)
        topSizer.AddGrowableCol(1,1)
        topSizer.Add(inPageText,0,wx.EXPAND)
        topSizer.Add(labelDecErrMode,0,wx.EXPAND)
        topSizer.Add(inPageCtrl,0,wx.EXPAND)
        topSizer.Add(choiceDecErrMode,0,wx.EXPAND)
        fromSizer = wx.BoxSizer(wx.HORIZONTAL)
        fromSizer.Add(lineNumLbl,0,wx.TOP,4)
        fromSizer.Add(fromLineNumCtrl,0,wx.LEFT,10)
        fromSizer.Add(rb0,0,wx.EXPAND|wx.LEFT,20)
        fromSizer.Add(rb1,0,wx.EXPAND|wx.LEFT,15)
        linesSizer = wx.BoxSizer(wx.HORIZONTAL)
        linesSizer.Add(lblAhead,0,wx.TOP,4)
        linesSizer.Add(linesNumCtrl,0,wx.LEFT|wx.RIGHT,8)
        linesSizer.Add(lblBehind,0,wx.TOP,4)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(fileText,0,wx.EXPAND)
        mainSizer.Add(filepathCtrl,0,wx.EXPAND)
        mainSizer.Add(topSizer,0,wx.TOP|wx.EXPAND,5)
        mainSizer.Add(linesSizer,0,wx.TOP|wx.EXPAND,11)
        mainSizer.Add(fromSizer,0,wx.TOP|wx.EXPAND,11)
        mainSizer.Add(labelMode,0,wx.TOP|wx.EXPAND,11)
        mainSizer.Add(choiceMode,0,wx.TOP,2)
        panel.sizer.Add(mainSizer,0,wx.EXPAND)

        def onLinesNumCtrl(event=None):
            flag = False
            if event:
                self.mode = choiceMode.GetSelection()
            if linesNumCtrl.GetValue() == 0:
                fromLineNumCtrl.SetValue(1)
                rb0.SetValue(True)
                rb1.SetValue(False)
                lineNumLbl.Enable(False)
                fromLineNumCtrl.Enable(False)
                rb0.Enable(False)
                rb1.Enable(False)
            else:
                lineNumLbl.Enable(True)
                fromLineNumCtrl.Enable(True)
                rb0.Enable(True)
                rb1.Enable(True)

            if linesNumCtrl.GetValue() == 1:
                choiceMode.Clear()
                choiceMode.AppendItems(strings=(text.oneNotIncluding,text.oneIncluding))
            else:
                if len(choiceMode.GetStrings()) != 3:
                    choiceMode.Clear()
                    choiceMode.AppendItems(
                        strings=(text.listNotIncluding,text.listIncluding,text.oneString)
                    )
                    if self.mode == 2:
                        flag = True
            if event:
                choiceMode.SetSelection(0)
                event.Skip()
                if flag:
                    self.mode = 0
            choiceMode.SetSelection(self.mode)
        linesNumCtrl.Bind(wx.EVT_SPIN, onLinesNumCtrl)
        onLinesNumCtrl()

        while panel.Affirmed():
            inCoding = inPageCtrl.GetSelection()
            pgTpl = (eg.systemEncoding, 'utf8')
            panel.SetResult(
                inCoding,
                filepathCtrl.GetValue(),
                choiceMode.GetSelection(),
                choiceDecErrMode.GetSelection(),
                inPageCtrl.GetStringSelection() if inCoding > 1 else pgTpl[inCoding],
                fromLineNumCtrl.GetValue(),
                rb1.GetValue(),
                linesNumCtrl.GetValue(),
            )
#===============================================================================

class AbortPeriodicalRead(eg.ActionClass):
    name = "Abort periodical reading"
    description = "Aborts periodical reading of text from selected file."

    def __call__(self, observName='', file = ''):
        observName = eg.ParseString(observName)
        self.plugin.AbortObservation(observName)

    def GetLabel(self, observName, file):
        return '%s: %s -> %s' % (str(self.name), file, observName)

    def Configure(self, observName='', file = ''):
        text=self.text
        panel = eg.ConfigPanel(self)
        choices = [item[1] for item in self.plugin.GetObservData()]
        fileLbl = wx.StaticText(panel, -1, '')
        fileLbl.Enable(False)
        nameLbl=wx.StaticText(panel, -1, text.nameObs)
        nameCtrl=wx.ComboBox(panel,-1,choices = choices)
        nameCtrl.SetStringSelection(observName)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(fileLbl,0)
        mainSizer.Add((1,20))
        mainSizer.Add(nameLbl,0)
        mainSizer.Add(nameCtrl,0,wx.EXPAND)
        panel.sizer.Add(mainSizer)
        panel.sizer.Layout()

        def onComboBox(event = None):
            choices = [item[1] for item in self.plugin.GetObservData()]
            evtName = nameCtrl.GetValue()
            if evtName in choices:
                indx = choices.index(evtName)
                fileName = self.plugin.GetObservData()[indx][0]
                lbl = text.fileLabel  % fileName
            else:
                lbl = ''
            fileLbl.SetLabel(lbl)
            if event:
                event.Skip()
        onComboBox()
        nameCtrl.Bind(wx.EVT_COMBOBOX,onComboBox)

        # re-assign the test button
        def OnTestButton(event):
            self.plugin.AbortObservation(nameCtrl.GetValue())
        panel.dialog.buttonRow.testButton.SetLabel(text.abortNow)
        panel.dialog.buttonRow.testButton.SetToolTipString(text.tip)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnTestButton)

        while panel.Affirmed():
            lbl = fileLbl.GetLabel()
            if lbl != '':
                fileName = lbl[2+lbl.rfind(':'):]
            else:
                fileName = ''
            panel.SetResult(
                nameCtrl.GetValue(),
                fileName
            )
    class text:
        nameObs = 'Observation and event name:'
        abortNow = 'Abort now !'
        tip = 'Abort observation now'
        fileLabel = 'File to read: %s'
#===============================================================================

class AbortAllPeriodicalRead(eg.ActionClass):
    name = "Abort all periodical reading"
    description = "Aborts all periodical reading of text from file."
    def __call__(self):
        self.plugin.AbortAllObservations()
#===============================================================================

class ReadPeriodically(eg.ActionClass):
    name = "Start periodical reading"
    description = ("Starts periodical reading of text from selected file. "
                   "Learning the line(s) return as payload of event.")

    def startObserv(self, stp):
        self.plugin.StartObservation(stp)

    def __call__(self, stp):
        self.startObserv(stp)

    def GetLabel(
        self,
        stp
    ):
        self.plugin.AddObservData(stp)
        return '%s: %s -> %s' % (str(self.name), os.path.split(stp[1])[1], stp[9])

    def Configure(
        self,
        stp = []
    ):
        if stp == []:
            inCoding = 0
            fileName = ''
            mode = 0
            errDecMode = 0
            inPage = ""
            fromLine = 1
            direction = 0
            lines = 1
#            period = 0.1
            period = 1
            evtName = ''
            trigger = 1
        else:
            inCoding = stp[0]
            fileName = stp[1]
            mode = stp[2]
            errDecMode = stp[3]
            inPage = stp[4]
            fromLine = stp[5]
            direction = stp[6]
            lines = stp[7]
            period = stp[8]
            evtName = stp[9]
            trigger = stp[10]

        from codecsList import codecsList
        panel = eg.ConfigPanel(self)
        text = self.plugin.text
        self.mode = mode
    #Controls
        inPageText = wx.StaticText(panel, -1, text.inputPage)
        labelMode = wx.StaticText(panel, -1, text.txtMode)
        labelDecErrMode = wx.StaticText(panel, -1, text.txtDecErrMode)
        fileText = wx.StaticText(panel, -1, text.FilePath)
        filepathCtrl = eg.FileBrowseButton(
            panel,
            -1,
            initialValue=fileName,
            labelText="",
            fileMask="*.*",
            buttonText=eg.text.General.browse,
            dialogTitle=text.browseFileDialogTitle
        )
        width = labelDecErrMode.GetTextExtent(text.txtDecErrMode)[0]
        choiceDecErrMode = wx.Choice(
            panel,
            -1,
            size = ((width,-1)),
            choices=(text.strict, text.ignore, text.replace)
        )
        choiceDecErrMode.SetSelection(errDecMode)
        choices = [text.systemPage % eg.systemEncoding, text.defaultIn]
        choices.extend(codecsList)
        inPageCtrl = wx.Choice(panel,-1,choices=choices)
        inPageCtrl.SetSelection(inCoding)
        lineNumLbl=wx.StaticText(panel, -1, text.lineNum)
        fromLineNumCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            fromLine,
            min = 1,
            max = 999,
        )
        rb0 = panel.RadioButton(not direction, text.begin, style=wx.RB_GROUP)
        rb1 = panel.RadioButton(direction, text.end)
        lblAhead = wx.StaticText(panel, -1, text.readAhead)
        lblBehind = wx.StaticText(panel, -1, text.readBehind)
        linesNumCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            lines,
            min = 0,
            max = 999,
        )
        periodNumCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            period,
            integerWidth = 5,
            fractionWidth = 1,
            allowNegative = False,
            min = 0.1,
            increment = 0.1,
        )
        intervalLbl = wx.StaticText(panel, -1, text.intervalLabel)
        w0 = inPageCtrl.GetTextExtent(text.listNotIncluding)[0]
        w1 = inPageCtrl.GetTextExtent(text.listIncluding)[0]
        w2 = inPageCtrl.GetTextExtent(text.oneNotIncluding)[0]
        w3 = inPageCtrl.GetTextExtent(text.oneIncluding)[0]
        w4 = inPageCtrl.GetTextExtent(text.oneString)[0]
        width = max(w0,w1,w2,w3,w4)+30
        choiceMode = wx.Choice(panel,-1,size=(width,-1))
        evtNameCtrl = wx.TextCtrl(panel,-1,evtName)
        evtNameLbl = wx.StaticText(panel, -1, text.evtNameLabel)
        triggerCtrl = wx.Choice(panel,-1, choices = text.triggerChoice)
        triggerCtrl.SetSelection(trigger)
        triggerLbl = wx.StaticText(panel, -1, text.triggerLabel)
    #Sizers
        topSizer = wx.FlexGridSizer(2,0,2,25)
        topSizer.AddGrowableCol(0,1)
        topSizer.AddGrowableCol(1,1)
        topSizer.Add(inPageText,0,wx.EXPAND)
        topSizer.Add(labelDecErrMode,0,wx.EXPAND)
        topSizer.Add(inPageCtrl,0,wx.EXPAND)
        topSizer.Add(choiceDecErrMode,0,wx.EXPAND)
        fromSizer = wx.BoxSizer(wx.HORIZONTAL)
        fromSizer.Add(lineNumLbl,0,wx.TOP,4)
        fromSizer.Add(fromLineNumCtrl,0,wx.LEFT,10)
        fromSizer.Add(rb0,0,wx.EXPAND|wx.LEFT,20)
        fromSizer.Add(rb1,0,wx.EXPAND|wx.LEFT,15)
        linesSizer = wx.BoxSizer(wx.HORIZONTAL)
        linesSizer.Add(lblAhead,0, flag = wx.TOP, border = 4)
        linesSizer.Add(linesNumCtrl,0,wx.LEFT|wx.RIGHT,8)
        linesSizer.Add(lblBehind,0, flag = wx.TOP, border = 4)
        periodSizer = wx.BoxSizer(wx.HORIZONTAL)
        periodSizer.Add(intervalLbl,0, wx.TOP|wx.RIGHT, 4)
        periodSizer.Add(periodNumCtrl,0, wx.RIGHT)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(fileText,0,wx.EXPAND)
        mainSizer.Add(filepathCtrl,0,wx.EXPAND)
        mainSizer.Add(topSizer,0,wx.TOP|wx.EXPAND,5)
        mainSizer.Add(linesSizer,0,wx.TOP|wx.EXPAND,11)
        mainSizer.Add(fromSizer,0,wx.TOP|wx.EXPAND,11)
        bottomSizer = wx.FlexGridSizer(4,0,2,25)
        bottomSizer.AddGrowableCol(0,1)
        bottomSizer.AddGrowableCol(1,1)
        bottomSizer.Add(labelMode,0,wx.EXPAND)
        bottomSizer.Add((1,1))
        bottomSizer.Add(choiceMode,0,wx.EXPAND)
        bottomSizer.Add(periodSizer,0,wx.EXPAND|wx.RIGHT,3)
        bottomSizer.Add(evtNameLbl,0,wx.TOP,8)
        bottomSizer.Add(triggerLbl,0,wx.TOP,8)
        bottomSizer.Add(evtNameCtrl,0,wx.EXPAND)
        bottomSizer.Add(triggerCtrl,0,wx.EXPAND)
        mainSizer.Add(bottomSizer,0,wx.TOP|wx.EXPAND,11)
        panel.sizer.Add(mainSizer,0,wx.EXPAND)

        def onLinesNumCtrl(event=None):
            flag = False
            if event:
                self.mode = choiceMode.GetSelection()
            if linesNumCtrl.GetValue() == 0:
                fromLineNumCtrl.SetValue(1)
                rb0.SetValue(True)
                rb1.SetValue(False)
                lineNumLbl.Enable(False)
                fromLineNumCtrl.Enable(False)
                rb0.Enable(False)
                rb1.Enable(False)
            else:
                lineNumLbl.Enable(True)
                fromLineNumCtrl.Enable(True)
                rb0.Enable(True)
                rb1.Enable(True)

            if linesNumCtrl.GetValue() == 1:
                choiceMode.Clear()
                choiceMode.AppendItems(strings=(text.oneNotIncluding,text.oneIncluding))
            else:
                if len(choiceMode.GetStrings()) != 3:
                    choiceMode.Clear()
                    choiceMode.AppendItems(
                        strings=(text.listNotIncluding,text.listIncluding,text.oneString)
                    )
                    if self.mode == 2:
                        flag = True
            if event:
                choiceMode.SetSelection(0)
                event.Skip()
                if flag:
                    self.mode = 0
            choiceMode.SetSelection(self.mode)
        linesNumCtrl.Bind(wx.EVT_SPIN, onLinesNumCtrl)
        onLinesNumCtrl()

        while panel.Affirmed():
            inCoding = inPageCtrl.GetSelection()
            pgTpl = (eg.systemEncoding, 'utf8')
            setup = [
                inCoding,
                filepathCtrl.GetValue(),
                choiceMode.GetSelection(),
                choiceDecErrMode.GetSelection(),
                inPageCtrl.GetStringSelection() if inCoding > 1 else pgTpl[inCoding],
                fromLineNumCtrl.GetValue(),
                rb1.GetValue(),
                linesNumCtrl.GetValue(),
                periodNumCtrl.GetValue(),
                evtNameCtrl.GetValue(),
                triggerCtrl.GetSelection()
            ]
            panel.SetResult(
                setup
            )
#===============================================================================

class Write(eg.ActionClass):
    name = "Write text to file"
    description = "Writes text to selected file."
    class text:
        TreeLabel = "Write %s to file: %s"
        FilePath = "Output file:"
        browseFileDialogTitle = "Choose the file"
        txtModeMulti = "Mode of write"
        overwrite = "File overwrite"
        append = "Append to file"
        newLine = "Append to file with new line"
        writeToLog = "Write to EventGhost log too"
        systemPage = "system code page (%s)"
        defaultOut = "unicode (UTF-8)"
        hexdump = "String write in the HexDump form"
        inString = "Input text:"
        logTimes = "Write Timestamp"
        outputPage = "Output data coding:"
        txtEncErrMode = "Error handling during encoding:"
        strict = "Raise an exception"
        ignore = "Ignore (skip bad chars)"
        replace = "Replace bad chars"
        internal = 'unicode internal'

    def __call__(
        self,
        outCoding,
        string = "",
        fileName = '',
        mode = 0,
        errEncMode = 0,
        log = False,
        times = False,
        hex = False,
        outPage = "",
    ):
        modeStr = 'w' if mode==0 else 'a'
        stamp = time.strftime('%y-%m-%d %H:%M:%S')+'  ' if times else ''
        cr = '\r\n' if mode == 2 else ''
        errorList = ('strict','ignore','replace')
        string = eg.ParseString(string)
        fileName = eg.ParseString(fileName)
        if hex:
            if outPage != 'unicode_internal':
                string = string.encode(outPage,errorList[errEncMode])
                string = String2Hex(string)
            else:
                string = String2Hex(string,'4')
            outPage = 'ascii'

        try:
            file = codecs.open(fileName, modeStr, outPage, errorList[errEncMode])
        except:
            raise
        try:
            file.write('%s%s%s' % (stamp, string, cr))
        except:
            raise
        try:
            file.close()
        except:
            raise
        if log:
            print string
        return string

    def GetLabel(
        self,
        outCoding,
        string,
        fileName,
        mode,
        errEncMode,
        log,
        times,
        hex,
        outPage,
    ):
        return self.text.TreeLabel % (string, fileName)

    def Configure(
        self,
        outCoding = 2,
        string = "{eg.result}",
        fileName = u'EG_WTTF.txt',
        mode = 2,
        errEncMode = 0,
        log = False,
        times = False,
        hex = False,
        outPage="",
    ):
        from codecsList import codecsList
        panel = eg.ConfigPanel(self)
        text = self.text
    #Controls
        stringText = wx.StaticText(panel, -1, text.inString)
        outPageText = wx.StaticText(panel, -1, text.outputPage)
        labelEncErrMode = wx.StaticText(panel, -1, text.txtEncErrMode)
        fileText = wx.StaticText(panel, -1, text.FilePath)
        filepathCtrl = eg.FileBrowseButton(
            panel,
            -1,
            initialValue=fileName,
            labelText="",
            fileMask="*.*",
            buttonText=eg.text.General.browse,
            dialogTitle=text.browseFileDialogTitle
        )
        width = labelEncErrMode.GetTextExtent(text.txtEncErrMode)[0]
        choiceEncErrMode = wx.Choice(
            panel,
            -1,
            size = ((width,-1)),
            choices=(text.strict, text.ignore, text.replace)
        )
        stringCtrl = wx.TextCtrl(panel, -1, string, style=wx.TE_NOHIDESEL)
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.txtModeMulti,
            choices=[text.overwrite, text.append, text.newLine],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBoxMode.SetSelection(mode)
        choiceEncErrMode.SetSelection(errEncMode)
        writeToLogCheckBox = wx.CheckBox(panel, -1, text.writeToLog)
        writeToLogCheckBox.SetValue(log)
        timesCheckBox = wx.CheckBox(panel, -1, text.logTimes)
        timesCheckBox.SetValue(times)
        hexCheckBox = wx.CheckBox(panel, -1, text.hexdump)
        hexCheckBox.SetValue(hex)
        choices = [text.internal, text.defaultOut, text.systemPage % eg.systemEncoding]
        choices.extend(codecsList)
        outPageCtrl = wx.Choice(panel,-1,choices=choices)
        outPageCtrl.SetSelection(outCoding)
    #Sizers
        topSizer = wx.FlexGridSizer(5,0,1,15)
        topSizer.AddGrowableCol(0,1)
        topSizer.AddGrowableCol(1,1)
        topSizer.Add(stringText,0,wx.EXPAND)
        topSizer.Add(fileText,0,wx.EXPAND)
        topSizer.Add(stringCtrl,0,wx.EXPAND)
        topSizer.Add(filepathCtrl,0,wx.EXPAND)
        topSizer.Add((1,7))
        topSizer.Add((1,7))
        topSizer.Add(outPageText,0,wx.EXPAND)
        topSizer.Add(labelEncErrMode,0,wx.EXPAND)
        topSizer.Add(outPageCtrl,0,wx.EXPAND)
        topSizer.Add(choiceEncErrMode,0,wx.EXPAND)
        chkBoxSizer = wx.BoxSizer(wx.VERTICAL)
        chkBoxSizer.Add(writeToLogCheckBox,0,wx.TOP|wx.LEFT,12)
        chkBoxSizer.Add(timesCheckBox,0,wx.TOP|wx.LEFT,12)
        chkBoxSizer.Add(hexCheckBox,0,wx.TOP|wx.LEFT,12)
        bottomSizer = wx.GridSizer(1,2,1,10)
        bottomSizer.Add(radioBoxMode,0,wx.TOP|wx.EXPAND,5)
        bottomSizer.Add(chkBoxSizer,1,wx.EXPAND)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer,0,wx.EXPAND)
        mainSizer.Add(bottomSizer,0,wx.TOP|wx.EXPAND,10)
        panel.sizer.Add(mainSizer,0,wx.EXPAND)

        while panel.Affirmed():
            outCoding = outPageCtrl.GetSelection()
            pgTpl = ('unicode_internal', 'utf8', eg.systemEncoding)
            panel.SetResult(
                outCoding,
                stringCtrl.GetValue(),
                filepathCtrl.GetValue(),
                radioBoxMode.GetSelection(),
                choiceEncErrMode.GetSelection(),
                writeToLogCheckBox.IsChecked(),
                timesCheckBox.IsChecked(),
                hexCheckBox.IsChecked(),
                outPageCtrl.GetStringSelection() if outCoding > 2 else pgTpl[outCoding],
            )
#===============================================================================

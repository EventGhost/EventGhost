#
# plugins/NetworkTraffic/__init__.py
#
# Copyright (C) 2008 Stefan Gollmer
#
# This file is part of EventGhost.
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
#
#
# $LastChangedDate: 2009-05-28 10:40:24 +0200 (Do, 28 Mai 2009) $
# $LastChangedRevision: 1025 $
# $LastChangedBy: Prinz $

import eg

eg.RegisterPlugin(
    name='Network Data Rate Monitor',
    guid='{210B39D5-074F-4B44-BEEC-E3C14A66456A}',
    author='Stefan Gollmer',
    version='1.00.' + '$LastChangedRevision: 1025 $'.split()[1],
    description=(
        'Plugin monitors the transfer rate '
        'of different interfaces of the network'

    ),
    url='http://www.eventghost.org/forum/viewtopic.php?f=9&t=1766',
    icon=(
        'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/'
        'AAAACXBIWXMAAAsSAAALEgHS3X78AAAAB3RJTUUH1gIQFgQb1MiCRwAAAVVJREFUOMud'
        'kjFLw2AQhp8vif0fUlPoIgVx6+AgopNI3fwBViiIoOAgFaugIDhUtP4BxWDs4CI4d3MR'
        'cSyIQ1tDbcHWtjFI4tAWG5pE8ca7997vnrtP4BOZvW0dSBAcZ0pAMTEzPUs4GvMsVkvP'
        '6HktGWRAOBpjIXVNKOSWWdYXN7lFAAINhBCEQgqxyTHAAQQAD/dFbLurUYJYT7P7TI2C'
        'VavwIiZodyyaH6ZLo/RZVTXiOYVhGOh5jcpbq5eRAXAc5wdBVSPMLR16GtxdbgJgN95d'
        'OxicACG6bPH4uIu1UHjE7sFqR/NDVxhaoixLvFYbtDufNFtu1tzxgdeAaZfBU7ECTvd1'
        'WRlxsa4sp1ydkiRxkstmlEFRrWT4nrRer3vmlf6mb883fK8AoF1d+Bqc6Xkt+cufT6e3'
        'dnb9DJJrq+uYpunZ2WcFfA0ol8v8N5Qgvr/EN8Lzfbs+L0goAAAAAElFTkSuQmCC'
    )
)


import wx
from threading import Event, Lock, Thread, Timer
from eg.WinApi.Dynamic import (Array, byref, BYTE, c_char, c_wchar, DWORD, sizeof, Structure, windll)


class Text:
    interface = 'Interface: '
    interfaces = 'Interfaces: '

    pollTime = 'Poll period [s]: '

    lowLimit = 'Lower limit [Byte/s]: '
    upperLimit = 'Upper limit [Byte/s]: '
    cycles = 'Cycles : '

    addInterface = 'Add'

    interfaceName = 'Interface'
    inAverage = 'Input average'
    outAverage = 'Output average'
    lowLimitTab = 'Lower limit'
    highLimitTab = 'Upper limit'
    cyclesTab = 'Cycles'

    clearInterface = 'Clear'



WCHAR = c_wchar


# BYTE  = c_byte


def WSTRING(size):
    class WS(Array):
        _type_ = WCHAR
        _length_ = size

        def __str__(self):
            return ''.join(self).split('\0')[0]

        def __repr__(self):
            return repr(str(self))

    return WS


def STRING(size):
    class S(Array):
        _type_ = c_char
        _length_ = size

        def __str__(self):
            return ''.join(self).split('\0')[0]

        def __repr__(self):
            return repr(str(self))

    return S


BUFFER_SIZE = 100
MAX_CYCLE = BUFFER_SIZE
MAX_LIMIT = 128000000
DEFAULT_LOW = 000000000
DEFAULT_HIGH = MAX_LIMIT
DEFAULT_CYCLE = 10

MAX_INTERFACE_NAME_LEN = 256
MAXLEN_PHYSADDR = 8
MAXLEN_IFDESCR = 256
NUM_INTERFACES_ADDON = 32

NO_ERROR = 0
ERROR_INSUFFICIENT_BUFFER = 122


class MIB_IFROW(Structure):
    _fields_ = [
        ('wszName', WSTRING(MAX_INTERFACE_NAME_LEN)),
        ('dwIndex', DWORD),
        ('dwType', DWORD),
        ('dwMtu', DWORD),
        ('dwSpeed', DWORD),
        ('dwPhysAddrLen', DWORD),
        ('bPhysAddr', BYTE * MAXLEN_PHYSADDR),
        ('dwAdminStatus', DWORD),
        ('dwOperStatus', DWORD),
        ('dwLastChange', DWORD),
        ('dwInOctets', DWORD),
        ('dwInUcastPkts', DWORD),
        ('dwInNUcastPkts', DWORD),
        ('dwInDiscards', DWORD),
        ('dwInErrors', DWORD),
        ('dwInUnknownProtos', DWORD),
        ('dwOutOctets', DWORD),
        ('dwOutUcastPkts', DWORD),
        ('dwOutNUcastPkts', DWORD),
        ('dwOutDiscards', DWORD),
        ('dwOutErrors', DWORD),
        ('dwOutQLen', DWORD),
        ('dwDescrLen', DWORD),
        ('bDescr', STRING(MAXLEN_IFDESCR))
    ]


class MIB_IFTABLE():

    def __init__(self, maxNumInterfaces=0):
        class MIB_IFTABLE_BASE(Structure):
            _fields_ = [
                ('dwNumEntries', DWORD),
                ('table', MIB_IFROW * maxNumInterfaces)
            ]

        self.c_instance = MIB_IFTABLE_BASE()
        self.c_instance.dwNumEntries = maxNumInterfaces

    def GetCInstance(self):
        return self.c_instance


class HandleInterfaces():

    def __init__(self):

        self.numInterfaces = 0

    def GetIfTable(self):

        count = 2

        while count > 0:

            rIfTable = MIB_IFTABLE(self.numInterfaces)

            ifTable = rIfTable.GetCInstance()
            dwSize = DWORD(sizeof(ifTable))

            ret = windll.iphlpapi.GetIfTable(byref(ifTable), byref(dwSize), 0)

            if ret == ERROR_INSUFFICIENT_BUFFER:

                self.numInterfaces = (dwSize.value - sizeof(dwSize)) / sizeof(MIB_IFROW)
                del rIfTable
                count -= 1
                continue

            elif ret != NO_ERROR:

                eg.PrintError('Unexpected error in NetworTraffic plugin. ErrorCode:' + str(ret))
                return MIB_IFTABLE(0).GetCInstance()

            else:
                # print "numInterfaces = ", self.numInterfaces
                return ifTable

        eg.PrintError('Cannot get the number of interfaces')
        return MIB_IFTABLE(0).GetCInstance()


class AverageParameters:

    def __init__(self, lowerLimit=0, upperLimit=999999999999, cycles=10):
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit
        self.cycles = cycles


class InterfaceInfo:
    class AverageLimitInfo:

        def __init__(self, averageParameters):
            self.averageParameters = averageParameters

            self.Reset()

        def Modify(self, averageParameters):
            self.averageParameters = averageParameters

        def Reset(self):
            self.lastValue = -1

            self.buffer = [0L] * BUFFER_SIZE
            self.bIdx = 0
            self.numEntries = 0

            self.lastOctetsSum = 0

            self.lastCycles = 0

            self.isLower = True

            self.average = 0

        def LowerLimit(self):
            return self.averageParameters.lowerLimit

        def UpperLimit(self):
            return self.averageParameters.upperLimit

        def Cycles(self):
            return self.averageParameters.cycles

    def __init__(self, descr, averageParameters):

        self.descr = descr
        self.lastCheckTime = -1

        self.isActive = False

        self.averageLimitInfos = [self.AverageLimitInfo(averageParameters),  # in
                                  self.AverageLimitInfo(averageParameters)  # out
                                  ]

    def Modify(self, averageParameters):

        self.averageLimitInfos[0].Modify(averageParameters)
        self.averageLimitInfos[1].Modify(averageParameters)

    def GetAverage(self):
        if self.isActive:
            return [info.average for info in self.averageLimitInfos]
        else:
            return None

    def GetParas(self):
        paras = self.averageLimitInfos[0].averageParameters
        return paras.lowerLimit, paras.upperLimit, paras.cycles

    def GetDescr(self):
        return self.descr

    def CalcAverage(self, values, payload, plugin, checkTime, enableEvents):

        # values[ 0 ]:  in
        # values[ 1 ]: out

        text = ['In', 'Out']

        if self.lastCheckTime != checkTime and self.lastCheckTime > 0:

            for info in self.averageLimitInfos:
                info.Reset()

        for ix, info in enumerate(self.averageLimitInfos):

            value = values[ix]

            if info.lastValue < 0:
                info.lastValue = value
                continue

            delta = value - info.lastValue

            if delta < 0:
                delta += 4294967296  # overflow

            info.lastValue = value

            buffer = info.buffer

            info.lastOctetsSum += delta

            while info.lastCycles != info.Cycles():
                i = -1
                if info.lastCycles < info.Cycles():
                    i = 1
                info.lastOctetsSum += i * buffer[(info.bIdx - info.lastCycles + 1 + BUFFER_SIZE) % BUFFER_SIZE]
                info.lastCycles += i

            c = info.Cycles()
            if info.numEntries < info.Cycles():
                c = info.numEntries + 1

            info.average = info.lastOctetsSum / c / int(checkTime)

            if enableEvents:

                if info.average > info.UpperLimit() and info.isLower:

                    plugin.TriggerEvent('HighAverageLimit' + text[ix], payload)
                    info.isLower = False


                elif info.average < info.LowerLimit() and not info.isLower:

                    plugin.TriggerEvent('LowAverageLimit' + text[ix], payload)
                    info.isLower = True

            info.numEntries += 1 - int(info.numEntries / BUFFER_SIZE)

            if info.numEntries > info.Cycles() - 1:
                info.lastOctetsSum -= buffer[(info.bIdx - info.Cycles() + BUFFER_SIZE) % BUFFER_SIZE]

            # print 'cycles = ', info.Cycles(), '   average = ', info.average, '   buffer = ', buffer

            # if ix == 0 :
            #   print "sum = ", info.lastOctetsSum, "   delta = ", delta, "   removed = ", buffer[ ( info.bIdx - info.Cycles() + BUFFER_SIZE ) % BUFFER_SIZE  ]

            buffer[info.bIdx] = delta
            info.bIdx = (info.bIdx + 1) % BUFFER_SIZE

        return True


class NetworkDataRateMonitorThread(Thread):

    def __init__(self, plugin, checkTime):

        Thread.__init__(self, name='NetworkDataRateMonitor')

        self.checkTime = checkTime
        self.plugin = plugin
        self.finish = False

        self.event = Event()

        self.lock = Lock()

        self.interfaceInfos = {}
        self.copied = None

        self.updateDisplay = None
        self.enableEvents = True

    @eg.LogItWithReturn
    def run(self):

        plugin = self.plugin

        iphlpapi = windll.iphlpapi

        while not self.finish:

            ifTable = plugin.interfaces.GetIfTable()

            self.lock.acquire()

            for desr, interfaceInfo in self.interfaceInfos.iteritems():
                interfaceInfo.isActive = False

            for ix in range(ifTable.dwNumEntries):

                ifRow = ifTable.table[ix]

                descr = str(ifRow.bDescr)
                # print 'Interface description = ', descr

                if descr in self.interfaceInfos:
                    # print 'Interface description = ', descr

                    # print 'ifRow.dwInOctets = ', ifRow.dwInOctets
                    # print 'ifRow.dwOutOctets = ', ifRow.dwOutOctets

                    interfaceInfo = self.interfaceInfos[descr]

                    interfaceInfo.isActive = True

                    values = [ifRow.dwInOctets, ifRow.dwOutOctets]
                    # print values

                    interfaceInfo.CalcAverage(values, descr, plugin, self.checkTime, self.enableEvents)

            self.lock.release()

            if self.updateDisplay is not None:
                self.updateDisplay()

            self.event.wait(self.checkTime)

        return True

    def Finish(self):
        self.finish = True
        self.event.set()

    def Update(self, checkTime, averageInfos):

        self.lock.acquire()

        if self.checkTime != checkTime:
            del self.interfaceInfos
            self.interfaceInfos = {}
            self.event.set()
            self.event.clear()

        self.checkTime = checkTime

        descritions = {}

        for descr, averageInfo in averageInfos.iteritems():

            descritions[descr] = True

            if descr in self.interfaceInfos:

                info = self.interfaceInfos[descr]

                info.Modify(averageInfo)

            else:

                self.interfaceInfos[descr] = InterfaceInfo(descr, averageInfo)

        toDelete = []

        for descr, info in self.interfaceInfos.iteritems():

            if descr not in averageInfos:
                toDelete.append(descr)

        for descr in toDelete:
            del self.interfaceInfos[descr]

        self.lock.release()

    def EnableEvents(self, flag=True):
        self.enableEvents = flag

    def SetUpdateDisplay(self, subRoutine):

        self.updateDisplay = subRoutine

    def GetInterfaceInfos(self, ):

        return self.interfaceInfos


class NetworkDataRateMonitor(eg.PluginClass):
    text = Text

    class ConfParameters():

        def __init__(self):
            pass

        def Import(self, inp=[]):
            out = {}
            for ix in range(0, len(inp), 4):
                paras = AverageParameters(
                    lowerLimit=inp[ix + 1],
                    upperLimit=inp[ix + 2],
                    cycles=inp[ix + 3]
                )
                out[inp[ix]] = paras
            return out

        def Export(self, interfacesParameters={}):
            out = []
            for key, paras in interfacesParameters.iteritems():
                out.append(key)
                out.append(paras.lowerLimit)
                out.append(paras.upperLimit)
                out.append(paras.cycles)
            return out

    def __init__(self):

        self.interfaces = HandleInterfaces()

        self.terminateTimer = None

        self.polltime = -1

        self.thread = NetworkDataRateMonitorThread(self, 1.0)
        self.thread.start()

    def __start__(self, confParameters=[], pollTime=2):

        interfacesParameters = self.ConfParameters().Import(confParameters)

        if self.terminateTimer is not None:
            self.terminateTimer.cancel()
            self.terminateTimer = None

        if self.thread is None:

            self.thread = NetworkDataRateMonitorThread(self, 1.0)
            self.thread.start()

        else:
            self.thread.EnableEvents(True)

        self.thread.Update(pollTime, interfacesParameters)

    @eg.LogItWithReturn
    def Finish(self):
        def Terminate():
            self.__close__()

        self.terminateTimer = Timer(1.0, Terminate)
        self.terminateTimer.start()
        self.thread.EnableEvents(False)

        return True

    def __stop__(self):
        self.Finish()

    def __close__(self):
        if self.thread is not None:
            self.thread.Finish()
            self.thread = None
        return True

    def Configure(self, confParameters=[], pollTime=2):

        self.actInterfacesParameters = self.ConfParameters().Import(confParameters)

        def onInterfaceChange(event):

            low = DEFAULT_LOW
            high = DEFAULT_HIGH
            cycles = DEFAULT_CYCLE

            descr = interfaceDescrCtrl.GetValue()
            if descr in self.actInterfacesParameters:
                paras = self.actInterfacesParameters[descr]
                low = paras.lowerLimit
                high = paras.upperLimit
                cycles = paras.cycles

            lowerLimitCtrl.SetValue(low)
            upperLimitCtrl.SetValue(high)
            cycleCtrl.SetValue(cycles)
            event.Skip()

        def onInterfaceAddButton(event):
            descr = interfaceDescrCtrl.GetValue()
            averageParameters = AverageParameters(
                lowerLimit=lowerLimitCtrl.GetValue(),
                upperLimit=upperLimitCtrl.GetValue(),
                cycles=cycleCtrl.GetValue()
            )

            self.actInterfacesParameters[descr] = averageParameters
            FillTable()
            event.Skip()

        def onTextChange(event):
            descr = interfaceDescrCtrl.GetValue()
            if descr in self.actInterfacesParameters:
                averageParameters = AverageParameters(
                    lowerLimit=lowerLimitCtrl.GetValue(),
                    upperLimit=upperLimitCtrl.GetValue(),
                    cycles=cycleCtrl.GetValue()
                )

                self.actInterfacesParameters[descr] = averageParameters
                UpdateLimits()
            event.Skip()

        def UpdateAverage():
            row = 0
            if self.thread is not None:
                for descr, paras in self.actInterfacesParameters.iteritems():
                    infos = self.thread.GetInterfaceInfos()
                    if descr in infos:
                        averages = infos[descr].GetAverage()
                        if averages is not None:
                            interfaceListCtrl.SetItem(row, 1, str(averages[0]))
                            interfaceListCtrl.SetItem(row, 2, str(averages[1]))
                        else:
                            interfaceListCtrl.SetItem(row, 1, 'unknown')
                            interfaceListCtrl.SetItem(row, 2, 'unknown')

                    row += 1

        def UpdateLimits():
            row = 0
            for descr, paras in self.actInterfacesParameters.iteritems():
                interfaceListCtrl.SetItem(row, 3, str(paras.lowerLimit))
                interfaceListCtrl.SetItem(row, 4, str(paras.upperLimit))
                interfaceListCtrl.SetItem(row, 5, str(paras.cycles))
                row += 1

        def FillTable():
            interfaceListCtrl.DeleteAllItems()
            clearButton.Enable(False)
            row = 0
            for descr, paras in self.actInterfacesParameters.iteritems():
                interfaceListCtrl.InsertItem(row, descr)
                if self.thread is not None:
                    infos = self.thread.GetInterfaceInfos()
                    if descr in infos:
                        averages = infos[descr].GetAverage()
                        if averages is not None:
                            interfaceListCtrl.SetItem(row, 1, str(averages[0]))
                            interfaceListCtrl.SetItem(row, 2, str(averages[1]))
                        else:
                            interfaceListCtrl.SetItem(row, 1, 'unknown')
                            interfaceListCtrl.SetItem(row, 2, 'unknown')
                interfaceListCtrl.SetItem(row, 3, str(paras.lowerLimit))
                interfaceListCtrl.SetItem(row, 4, str(paras.upperLimit))
                interfaceListCtrl.SetItem(row, 5, str(paras.cycles))
                row += 1

        def listSelection(event):
            selected = interfaceListCtrl.GetFirstSelected()
            enable = selected != -1
            clearButton.Enable(enable)
            if enable:
                descr = interfaceListCtrl.GetItemText(selected)
                interfaceDescrCtrl.SetValue(descr)
                BindText(False)
                onInterfaceChange(wx.CommandEvent())
                BindText(True)
            event.Skip()

        def onClearButton(event):
            item = interfaceListCtrl.GetFirstSelected()
            while item != -1:
                descr = interfaceListCtrl.GetItemText(item)
                del self.actInterfacesParameters[descr]
                item = interfaceListCtrl.GetNextSelected(item)
            FillTable()
            event.Skip()

        def BindText(enable):
            if enable:
                lowerLimitCtrl.Bind(wx.EVT_TEXT, onTextChange)
                upperLimitCtrl.Bind(wx.EVT_TEXT, onTextChange)
                cycleCtrl.Bind(wx.EVT_TEXT, onTextChange)
            else:
                lowerLimitCtrl.Unbind(wx.EVT_TEXT)
                upperLimitCtrl.Unbind(wx.EVT_TEXT)
                cycleCtrl.Unbind(wx.EVT_TEXT)

        self.allInterfaceNames = []

        ifTable = self.interfaces.GetIfTable()

        for ix in range(ifTable.dwNumEntries):
            ifRow = ifTable.table[ix]

            self.allInterfaceNames.append(str(ifRow.bDescr))

        for descr, paras in self.actInterfacesParameters.iteritems():

            if descr not in self.allInterfaceNames:
                self.allInterfaceNames.append(descr)

        self.allInterfaceNames.sort()

        text = self.text

        panel = eg.ConfigPanel(self, resizable=True)

        pollTimeCtrl = panel.SpinIntCtrl(pollTime, min=1, max=60)

        interfaceDescrCtrl = wx.ComboBox(
            panel,
            -1,
            value=self.allInterfaceNames[0],
            choices=self.allInterfaceNames,
            size=(350, -1),
            style=wx.CB_READONLY
        )
        interfaceDescrCtrl.Bind(wx.EVT_COMBOBOX, onInterfaceChange)

        lowerLimitCtrl = panel.SpinIntCtrl(DEFAULT_LOW, min=0, max=MAX_LIMIT)
        upperLimitCtrl = panel.SpinIntCtrl(DEFAULT_HIGH, min=0, max=MAX_LIMIT)
        cycleCtrl = panel.SpinIntCtrl(DEFAULT_CYCLE, min=1, max=MAX_CYCLE)

        BindText(True)

        addInterfaceButton = wx.Button(panel, -1, text.addInterface)
        addInterfaceButton.Bind(wx.EVT_BUTTON, onInterfaceAddButton)

        interfaceListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)

        interfaceListCtrl.InsertColumn(0, text.interfaceName)
        interfaceListCtrl.InsertColumn(1, text.inAverage)
        interfaceListCtrl.InsertColumn(2, text.outAverage)
        interfaceListCtrl.InsertColumn(3, text.lowLimitTab)
        interfaceListCtrl.InsertColumn(4, text.highLimitTab)
        interfaceListCtrl.InsertColumn(5, text.cyclesTab)

        columnLengthMin = (200, 70, 70, 70, 70, 40)

        size = 0
        for c in range(len(columnLengthMin)):
            interfaceListCtrl.SetColumnWidth(c, wx.LIST_AUTOSIZE_USEHEADER)
            csize = interfaceListCtrl.GetColumnWidth(c)
            if csize < columnLengthMin[c]:
                csize = columnLengthMin[c]
            interfaceListCtrl.SetColumnWidth(c, csize)
            size += csize

        interfaceListCtrl.SetMinSize((size, -1))

        interfaceListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, listSelection)
        interfaceListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, listSelection)

        clearButton = wx.Button(panel, -1, text.clearInterface)
        clearButton.Bind(wx.EVT_BUTTON, onClearButton)

        gridSizer = wx.GridBagSizer(3, 3)

        rowCount = 0
        gridSizer.Add(
            wx.StaticText(panel, -1, text.pollTime),
            (rowCount, 0),
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
        )
        gridSizer.Add(pollTimeCtrl, (rowCount, 1), flag=wx.ALIGN_LEFT)

        rowCount += 1

        gridSizer.Add(wx.Size(5, 10), (rowCount, 0))

        rowCount += 1

        gridSizer.Add(
            wx.StaticText(panel, -1, text.interface),
            (rowCount, 0),
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
        )
        gridSizer.Add(interfaceDescrCtrl, (rowCount, 1), flag=wx.ALIGN_RIGHT)

        gridSizer.Add(addInterfaceButton, (rowCount, 3), flag=wx.EXPAND)

        rowCount += 1

        gridSizer.Add(wx.Size(5, 3), (rowCount, 0))

        rowCount += 1
        gridSizer.Add(
            wx.StaticText(panel, -1, text.lowLimit),
            (rowCount, 0),
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
        )
        gridSizer.Add(lowerLimitCtrl, (rowCount, 1), flag=wx.ALIGN_LEFT)

        rowCount += 1

        gridSizer.Add(
            wx.StaticText(panel, -1, text.upperLimit),
            (rowCount, 0),
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
        )
        gridSizer.Add(upperLimitCtrl, (rowCount, 1), flag=wx.ALIGN_LEFT)

        rowCount += 1

        gridSizer.Add(
            wx.StaticText(panel, -1, text.cycles),
            (rowCount, 0),
            flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
        )
        gridSizer.Add(cycleCtrl, (rowCount, 1), flag=wx.ALIGN_LEFT)

        panel.sizer.Add(gridSizer)

        # Interface table

        panel.sizer.Add(wx.Size(5, 10))

        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.interfaces),
            flag=wx.ALIGN_CENTER_VERTICAL
        )
        panel.sizer.Add(wx.Size(5, 5))

        tableSizer = wx.GridBagSizer(5, 5)
        tableSizer.AddGrowableRow(0)
        tableSizer.AddGrowableCol(0)

        rowCount = 0
        tableRows = 6
        tableSizer.Add(interfaceListCtrl, (0, 0), (tableRows, 4), flag=wx.EXPAND)
        rowCount += tableRows

        tableSizer.Add(clearButton, (rowCount, 1), flag=wx.LEFT)
        clearButton.Enable(False)

        panel.sizer.Add(tableSizer, flag=wx.EXPAND)

        FillTable()
        onInterfaceChange(wx.CommandEvent())

        if self.thread is not None:
            self.thread.SetUpdateDisplay(UpdateAverage)

        confirmed = False

        while panel.Affirmed():
            pollTime = pollTimeCtrl.GetValue()

            panel.SetResult(self.ConfParameters().Export(self.actInterfacesParameters), pollTime)

        if self.thread is not None:
            self.thread.SetUpdateDisplay(None)

#
# plugins/KMK_5I8O/__init__.py
#
# Copyright (C) 2009
# Walter Kraembring
#
##############################################################################
# Revision history:
#
# 2010-03-23  Uses eg.PersistentData to save persistent data instead of pickle
# 2009-12-19  0.4.0 compatible GUID added
# 2009-12-05  Version 1.1.0 Release
# 2009-12-01  Version 1.0.2 (beta_2)
# 2009-11-30  Version 1.0.1 (beta_2)
# 2009-11-10  Version 1.0.0 (beta_1)
# 2009-11-08  The first stumbling version (alpha)
##############################################################################

import eg

eg.RegisterPlugin(
    name="KMK_5I8O",
    guid='{B41545BD-9F6F-493C-8247-487F80F1B3D9}',
    author="Walter Kraembring",
    version="1.1.2",
    canMultiLoad=True,
    kind="external",
    url="http://www.kmk.com.hk/ProductShop/USB5I8O.htm",
    description=(
        '<p>Plugin to control the KMK USB 5I8O Board</p>'
        '\n\n<p><a href="http://www.kmk.com.hk/ProductShop/USB5I8O.htm">'
        'Product details...</a></p>'
        '<center><img src="USB5I8O.PNG" /></center>'
    ),
)

import win32com.client
import time, random
import pythoncom
import wx
from threading import Event, Thread


class Text:
    txt_BoardSerial = "Board Serial Number "
    txt_ThreadWaitTime = "Thread wait time (x.y s)"

    txt_DigitalIn_1 = "Digital In_1 Value for event (0,1, Both)"
    txt_DigitalIn_2 = "Digital In_2 Value for event (0,1, Both)"
    txt_DigitalIn_3 = "Digital In_3 Value for event (0,1, Both)"
    txt_DigitalIn_4 = "Digital In_4 Value for event (0,1, Both)"
    txt_DigitalIn_5 = "Digital In_5 Value for event (0,1, Both)"
    txt_DI = " DI:"
    txt_State = " State:"

    txt_Initiated = "KMK USB 5I8O is initiated"
    txt_OCX_CannotBeFound_T = (
        "KMKUSB5I8OOCX.KMKUSB cannot be found by the thread"
    )
    txt_OCX_Found_T = "OCX is found by the thread"
    txt_ReadingData = "Reading KMK_5I8O configuration data from file..."
    txt_WritingData = "Writing KMK_5I8O configuration data to file..."
    txt_IsStopped = " is stopped"
    txt_IsDeleted = " is deleted"
    txt_Polling = "The polling thread has stopped"
    txt_InitOut = "Init of outputs to last known state: "
    txt_OutSent = "Outputs sent to board: "
    txt_OutSet = "Output set to: "
    txt_boardError = "The board is not responding: "
    txt_boardOK = "The board is responding: "

    class SetDigitalOut:
        name = "Set Digital Output ON"
        description = "Turns on a digital output on the KMK USB 5I8O"
        txt_ConfSetDO = "Digital Output (1-8)"

    class ClearDigitalOut:
        name = "Set Digital Output OFF"
        description = "Turns off a digital output on the KMK USB 5I8O"
        txt_ConfClrDO = "Digital Output (1-8)"


class OutputStateData(eg.PersistentData):
    do_state_memory = {}


class KMK5I8O(eg.PluginClass):
    text = Text

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        board_serial="",
        tw=0.1,
        el_1='',
        el_2='',
        el_3='',
        el_4='',
        el_5='',
        di_event_trigger=[0] * 5,
        di_event_memory=[0] * 5
    ):
        panel = eg.ConfigPanel(self)

        # Create a combo for board serials
        board_serialCtrl = wx.ComboBox(parent=panel, pos=(10, 10))
        list = [
            'KMSJAD6H',
            'KMSJAA5A',
            'KMSHF43V'
        ]

        if board_serial != "":
            if list.count(board_serial) == 0:
                list.append(board_serial)

        board_serialCtrl.AppendItems(items=list)

        if list.count(board_serial) == 0:
            board_serialCtrl.Select(n=0)
        else:
            board_serialCtrl.SetSelection(int(list.index(board_serial)))

        board_serialCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, self.text.txt_BoardSerial)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(board_serialCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        thread_wait = panel.SpinNumCtrl(
            tw,
            fractionWidth=1,
            integerWidth=2,
            min=0.1,
            max=5.0
        )

        staticBox = wx.StaticBox(panel, -1, self.text.txt_ThreadWaitTime)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(thread_wait, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Digital event trigger levels
        di_1_levelCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '0',
            '1',
            'Both'
        ]
        di_1_levelCtrl.AppendItems(items=list)
        if list.count(el_1) == 0:
            di_1_levelCtrl.Select(n=2)
        else:
            di_1_levelCtrl.SetSelection(int(list.index(el_1)))
        di_1_levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, self.text.txt_DigitalIn_1)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(di_1_levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        di_2_levelCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '0',
            '1',
            'Both'
        ]
        di_2_levelCtrl.AppendItems(items=list)
        if list.count(el_2) == 0:
            di_2_levelCtrl.Select(n=2)
        else:
            di_2_levelCtrl.SetSelection(int(list.index(el_2)))
        di_2_levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, self.text.txt_DigitalIn_1)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(di_2_levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        di_3_levelCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '0',
            '1',
            'Both'
        ]
        di_3_levelCtrl.AppendItems(items=list)
        if list.count(el_3) == 0:
            di_3_levelCtrl.Select(n=2)
        else:
            di_3_levelCtrl.SetSelection(int(list.index(el_3)))
        di_3_levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, self.text.txt_DigitalIn_1)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(di_3_levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        di_4_levelCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '0',
            '1',
            'Both'
        ]
        di_4_levelCtrl.AppendItems(items=list)
        if list.count(el_4) == 0:
            di_4_levelCtrl.Select(n=2)
        else:
            di_4_levelCtrl.SetSelection(int(list.index(el_4)))
        di_4_levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, self.text.txt_DigitalIn_1)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(di_4_levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        di_5_levelCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '0',
            '1',
            'Both'
        ]
        di_5_levelCtrl.AppendItems(items=list)
        if list.count(el_5) == 0:
            di_5_levelCtrl.Select(n=2)
        else:
            di_5_levelCtrl.SetSelection(int(list.index(el_5)))
        di_5_levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, self.text.txt_DigitalIn_1)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(di_5_levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            board_serial = board_serialCtrl.GetValue()
            tw = thread_wait.GetValue()
            el_1 = di_1_levelCtrl.GetStringSelection()
            del di_event_trigger[0]
            di_event_trigger.insert(0, el_1)
            el_2 = di_2_levelCtrl.GetStringSelection()
            del di_event_trigger[1]
            di_event_trigger.insert(1, el_2)
            el_3 = di_3_levelCtrl.GetStringSelection()
            del di_event_trigger[2]
            di_event_trigger.insert(2, el_3)
            el_4 = di_4_levelCtrl.GetStringSelection()
            del di_event_trigger[3]
            di_event_trigger.insert(3, el_4)
            el_5 = di_5_levelCtrl.GetStringSelection()
            del di_event_trigger[4]
            di_event_trigger.insert(4, el_5)

            panel.SetResult(
                board_serial,
                tw,
                el_1,
                el_2,
                el_3,
                el_4,
                el_5,
                di_event_trigger,
                di_event_memory
            )

    def __init__(self):
        self.b_nbr = ''
        self.stopThreadEvent = Event()
        self.AddAction(SetDigitalOut)
        self.AddAction(ClearDigitalOut)

    def __start__(
        self,
        board_serial,
        tw,
        el_1,
        el_2,
        el_3,
        el_4,
        el_5,
        di_event_trigger,
        di_event_memory
    ):
        self.di_event_trigger = di_event_trigger
        self.di_event_memory = di_event_memory
        self.kmkSum_trigger = 0
        self.kmkSum = 0
        self.do_state_memory = [0] * 8
        self.b_nbr = board_serial
        self.thread_wait = tw

        # Get persistent output status data if it exists
        if str(self.b_nbr) in OutputStateData.do_state_memory:
            self.do_state_memory = OutputStateData.do_state_memory[str(self.b_nbr)]

        self.kmkSum = (
            self.do_state_memory[0]
            + self.do_state_memory[1]
            + self.do_state_memory[2]
            + self.do_state_memory[3]
            + self.do_state_memory[4]
            + self.do_state_memory[5]
            + self.do_state_memory[6]
            + self.do_state_memory[7]
        )

        self.thread = Thread(
            target=self.ThreadWorker,
            args=(self.stopThreadEvent,)
        )
        self.thread.start()

    def __stop__(self):
        # Make current output status data persistent
        OutputStateData.do_state_memory[str(self.b_nbr)] = self.do_state_memory
        print (
            self.text.txt_BoardSerial + str(self.b_nbr) +
            self.text.txt_IsStopped
        )
        time.sleep(1.0)
        self.stopThreadEvent.set()

    def __close__(self):
        print (
            self.text.txt_BoardSerial + str(self.b_nbr) +
            self.text.txt_IsDeleted
        )
        time.sleep(1.0)
        self.stopThreadEvent.set()

    def attachOCX(self, flag):
        # Attach interface to the OCX
        self.AxkmkusbT = None
        try:
            self.AxkmkusbT = win32com.client.Dispatch(
                "KMKUSB5I8OOCX.KMKUSB"
            )
        except:
            raise eg.Exception(
                self.b_nbr,
                self.text.txt_OCX_CannotBeFound_T
            )
        if self.AxkmkusbT != None and flag:
            print self.b_nbr, self.text.txt_OCX_Found_T

    def inputMem(self, ret, i):
        if (
            ret == self.di_event_trigger[i]
            or self.di_event_trigger[i] == "Both"
        ):
            if self.di_event_memory[i] != ret:
                self.TriggerEvent(
                    self.b_nbr +
                    ":" +
                    self.text.txt_DI + str(i + 1) +
                    self.text.txt_State + str(ret)
                )
                del self.di_event_memory[i]
                self.di_event_memory.insert(i, ret)

        if self.di_event_memory[i] != ret:
            del self.di_event_memory[i]
            self.di_event_memory.insert(i, ret)

    def ThreadWorker(self, stopThreadEvent):
        pythoncom.CoInitialize()
        self.cntr = 0
        self.inputs = ""
        random.jumpahead(137)

        # Attach interface to the OCX
        self.attachOCX(True)

        # Address the board...
        self.AxkmkusbT.device = self.b_nbr
        print self.b_nbr, self.text.txt_Initiated

        # Open the port
        self.AxkmkusbT.port_open_close = 1
        time.sleep(2.0 + random.random())

        # Set outputs to last known states
        if self.kmkSum != self.kmkSum_trigger:
            self.AxkmkusbT.out = str(self.kmkSum)
            print self.b_nbr, self.text.txt_InitOut, self.kmkSum
            self.kmkSum_trigger = self.kmkSum

        time.sleep(2.0)

        while not stopThreadEvent.isSet():
            for i in range(0, 2):
                self.inputs = str(self.AxkmkusbT.binary)
                if self.inputs != "":
                    break
                else:
                    time.sleep(2.0)

            if self.inputs != "":
                inputList = []

                for i in range(0, len(self.inputs)):
                    inputList.insert(i, self.inputs[i])

                for i in range(0, len(self.inputs)):
                    ret = str(inputList[i])
                    self.inputMem(ret, i)

            else:
                # The board is not responding
                if self.cntr == 9:
                    self.cntr = 0

                if self.cntr == 0:
                    self.TriggerEvent(
                        self.text.txt_boardError +
                        str(self.b_nbr)
                    )

                self.cntr += 1
                self.attachOCX(False)
                self.AxkmkusbT.device = self.b_nbr
                self.AxkmkusbT.port_open_close = 1
                time.sleep(2.0 + random.random())

                for i in range(0, 5):
                    self.inputs = str(self.AxkmkusbT.binary)
                    if self.inputs != "":
                        break
                    else:
                        time.sleep(2.0)

                if self.inputs != "":
                    self.TriggerEvent(
                        self.text.txt_boardOK +
                        str(self.b_nbr)
                    )
                    self.cntr = 0
                    time.sleep(2.0)
                    self.AxkmkusbT.out = str(self.kmkSum_trigger)
                    print self.b_nbr, self.text.txt_InitOut, self.kmkSum

            if self.kmkSum != self.kmkSum_trigger:
                self.AxkmkusbT.out = str(self.kmkSum_trigger)
                print self.b_nbr, self.text.txt_OutSent, self.kmkSum_trigger
                self.kmkSum = self.kmkSum_trigger

            # Test to see what gets sent.
            #            print self.b_nbr, self.di_event_trigger
            #            print self.b_nbr, self.di_event_memory
            #            print self.b_nbr, self.inputs
            #            print self.b_nbr, self.do_state_memory
            #            print self.b_nbr, self.text.txt_OutSet, str(self.kmkSum)

            stopThreadEvent.wait(self.thread_wait)

        self.AxkmkusbT.port_open_close = 0
        pythoncom.CoUninitialize()
        print self.b_nbr, self.text.txt_Polling


class SetDigitalOut(eg.ActionClass):
    iconFile = "digital-out-on"

    def __call__(self, do):

        if self.plugin.do_state_memory[do - 1] == 0:
            del self.plugin.do_state_memory[do - 1]
            self.plugin.do_state_memory.insert(do - 1, 2 ** (do - 1))
            self.plugin.kmkSum_trigger = (
                self.plugin.do_state_memory[0]
                + self.plugin.do_state_memory[1]
                + self.plugin.do_state_memory[2]
                + self.plugin.do_state_memory[3]
                + self.plugin.do_state_memory[4]
                + self.plugin.do_state_memory[5]
                + self.plugin.do_state_memory[6]
                + self.plugin.do_state_memory[7]
            )

    # Digital outputs on the board, 8 in total
    def Configure(self, do=1):
        panel = eg.ConfigPanel(self)
        digitalOut_ctrl = panel.SpinIntCtrl(do, 1, 8)
        digitalOut_ctrl.SetInitialSize((40, -1))
        panel.AddLine(self.text.txt_ConfSetDO, digitalOut_ctrl)
        while panel.Affirmed():
            do = digitalOut_ctrl.GetValue()
            panel.SetResult(
                do
            )


class ClearDigitalOut(eg.ActionClass):
    iconFile = "digital-out-off"

    def __call__(self, do):

        if self.plugin.do_state_memory[do - 1] == 2 ** (do - 1):
            del self.plugin.do_state_memory[do - 1]
            self.plugin.do_state_memory.insert(do - 1, 0)
            self.plugin.kmkSum_trigger = (
                self.plugin.do_state_memory[0]
                + self.plugin.do_state_memory[1]
                + self.plugin.do_state_memory[2]
                + self.plugin.do_state_memory[3]
                + self.plugin.do_state_memory[4]
                + self.plugin.do_state_memory[5]
                + self.plugin.do_state_memory[6]
                + self.plugin.do_state_memory[7]
            )

    # Digital outputs on the board, 8 in total
    def Configure(self, do=1):
        panel = eg.ConfigPanel(self)
        digitalOut_ctrl = panel.SpinIntCtrl(do, 1, 8)
        digitalOut_ctrl.SetInitialSize((40, -1))
        panel.AddLine(self.text.txt_ConfClrDO, digitalOut_ctrl)
        while panel.Affirmed():
            do = digitalOut_ctrl.GetValue()
            panel.SetResult(
                do
            )

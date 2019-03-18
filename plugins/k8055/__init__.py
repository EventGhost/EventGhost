#
# plugins/k8055/__init__.py
#
# Copyright (C) 2008
# Walter Kraembring
#
##############################################################################
# Revision history:
#
# 2010-02-12  On request I have added a function that allows you to get an
#             event on every counter count. Selectable per counter
# 2010-01-03  Changed back, now only analogue input values are in the payload
#             Introduced filter for analogue inputs to reduce sensitivity 
# 2010-01-02  Values read from inputs and counters are now in the payload of
#             the event
# 2009-12-19  0.4.0 compatible GUID added
# 2008-04-14  Modified design
# 2008-03-18  Modified thread ending
# 2008-03-09  Some further modifications and clean-up
# 2008-03-05  Now with support for multiple boards (0-3)
# 2008-03-01  The first stumbling version
##############################################################################

eg.RegisterPlugin(
    name = "K8055",
    guid = '{46C132A0-ECA3-48EF-BB00-2E76E4C5B032}',
    author = "Walter Kraembring",
    version = "0.1.8",
    canMultiLoad = True,
    kind = "external",
    url = "http://www.velleman.be/ot/en/product/view/?id=351346",
    description = (
        '<p>Plugin to control Welleman K8055 VM110 USB Experiment Interface Board</p>'
        '\n\n<p><a href="http://www.velleman.be/ot/en/product/view/?id=351346">Product details...</a></p>'
        '<center><img src="k8055.png" /></center>'
    ),
)

from ctypes import windll
from threading import Event, Thread



class Text:

    txt_BoardNumber = "K8055 Board Number"
    txt_ThreadWaitTime = "Thread wait time (x.y s)"
    
    txt_DigitalIn_1 = "Digital In_1 Value for event (0-1)"
    txt_DigitalIn_2 = "Digital In_2 Value for event (0-1)"
    txt_DigitalIn_3 = "Digital In_3 Value for event (0-1)"
    txt_DigitalIn_4 = "Digital In_4 Value for event (0-1)"
    txt_DigitalIn_5 = "Digital In_5 Value for event (0-1)"
    
    txt_AnalogIn_1 = "Analog In_1 Value for event (0-254)"
    txt_AnalogIn_2 = "Analog In_2 Value for event (0-254)"
    
    txt_Counter_1 = "Counter 1 Threshold (0-254)"
    txt_Counter_2 = "Counter 2 Threshold (0-254)"
    txt_Counter_1_event = "    Create event for every count"
    txt_Counter_2_event = "    Create event for every count"
    
    txt_Initiated = "K8055 is initiated"
    txt_dllNotFound = "K8055 dll not found"
    txt_dllLoaded = "K8055 dll is loaded"
    
    txt_BoardNbr = "K8055 Board nbr: "
    txt_CannotBeFound = " cannot be found"
    txt_IsFound = " is found and started"
    txt_IsStopped = " is stopped"
    txt_IsDeleted = " is deleted"
    txt_Polling = "The polling thread has stopped"

    txt_Counter = " Counter:"
    txt_AI = " AI:"
    txt_Value = " Value:"
    txt_Count = " Count:"
    txt_DI = " DI:"
    txt_State = " State:"
    
    class SetDigitalChannel:
        name = "Set Digital Channel ON"
        description = "Turns on a digital channel on K8055"
        txt_ConfSetDO = "Digital Output Channel (1-8)"
        
    class ClearDigitalChannel:
        name = "Set Digital Channel OFF"
        description = "Turns off a digital channel on K8055"
        txt_ConfClrDO = "Digital Output Channel (1-8)"
        
    class SetAnalogChannel:
        name = "Set Analog Channel ON"
        description = "Sets a value on an analog channel on K8055"
        txt_ConfSetAO = "Analog Output Channel (1-2)"
        txt_ConfSetVa = "Analog value (0-254)"
        
    class ClearAnalogChannel:
        name = "Set Analog Channel OFF"
        description = "Turns off an analog channel on K8055"
        txt_ConfCLrAO = "Analog Output Channel (1-2)"
        
    class ReadDigitalChannel:
        name = "Read Digital Channel"
        description = "A digital input channel on K8055"
        txt_ConfRdDI = "Digital Input Channel (1-5)"
        
    class ReadAnalogChannel:
        name = "Read Analog Channel"
        description = "An analog input channel on K8055"
        txt_ConfRdAI = "Analog Input Channel (1-2)"
        
    class Counter:
        name = "Counter"
        description = "Holds a counter in K8055"
        txt_ConfCntr = "Counter (1-2)"
        txt_ConfDbns = "Counter debounce (0, 2, 10, 1000 ms)"
        
    class Info:
        name = "Information"
        description = "Shows version information of the K8055-dll"
    


class k8055(eg.PluginClass):
    text = Text

    def Configure(
        self,
        board = 0,
        tw = 0.5,
        el_1 = 1,
        el_2 = 1,
        el_3 = 1,
        el_4 = 1,
        el_5 = 1,
        av_1 = 128,
        av_2 = 128,
        ct_1 = 5,
        ct_2 = 5,
        counter_threshold = [5]*2,
        ai_event_trigger = [128]*2,
        di_event_trigger = [0]*5,
        di_event_memory = [0]*5,
        ai_event_memory = [0]*2,
        counter_events = [False]*2,
        counter_old = [0]*2,
        ct_1_cb = False,
        ct_2_cb = False
     ):

        panel = eg.ConfigPanel(self)
        boardCtrl = panel.SpinIntCtrl(board, 0, 3)
        boardCtrl.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_BoardNumber, boardCtrl)

        thread_wait = panel.SpinNumCtrl(
            tw,
            decimalChar = '.',                 # by default, use '.' for decimal point
            groupChar = ',',                   # by default, use ',' for grouping
            fractionWidth = 2,
            integerWidth = 2,
            increment = 0.01,
            min = 0.01,
            max = 5.0
        )

        thread_wait.SetInitialSize((60,-1))
        panel.AddLine(self.text.txt_ThreadWaitTime , thread_wait)

        #Digital event trigger levels
        di_1_level = panel.SpinIntCtrl(el_1, 0, 1)
        di_1_level.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_DigitalIn_1, di_1_level)
        
        di_2_level = panel.SpinIntCtrl(el_2, 0, 1)
        di_2_level.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_DigitalIn_2, di_2_level)
        
        di_3_level = panel.SpinIntCtrl(el_3, 0, 1)
        di_3_level.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_DigitalIn_3, di_3_level)
        
        di_4_level = panel.SpinIntCtrl(el_4, 0, 1)
        di_4_level.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_DigitalIn_4, di_4_level)
        
        di_5_level = panel.SpinIntCtrl(el_5, 0, 1)
        di_5_level.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_DigitalIn_5, di_5_level)

        #Analog event trigger levels
        ai_1_level = panel.SpinIntCtrl(av_1, 0, 254)
        ai_1_level.SetInitialSize((50,-1))
        panel.AddLine(self.text.txt_AnalogIn_1,ai_1_level)

        ai_2_level = panel.SpinIntCtrl(av_2, 0, 254)
        ai_2_level.SetInitialSize((50,-1))
        panel.AddLine(self.text.txt_AnalogIn_2,ai_2_level)
 
        #Counter thresholds
        ct_1_level = panel.SpinIntCtrl(ct_1, 0, 254)
        ct_1_level.SetInitialSize((50,-1))
        panel.AddLine(self.text.txt_Counter_1, ct_1_level)
        ct_1_count = wx.CheckBox(panel, -1, self.text.txt_Counter_1_event)
        ct_1_count.SetValue(ct_1_cb)
        panel.AddLine(ct_1_count)

        ct_2_level = panel.SpinIntCtrl(ct_2, 0, 254)
        ct_2_level.SetInitialSize((50,-1))
        panel.AddLine(self.text.txt_Counter_2, ct_2_level)
        ct_2_count = wx.CheckBox(panel, -1, self.text.txt_Counter_2_event)
        ct_2_count.SetValue(ct_2_cb)
        panel.AddLine(ct_2_count)

        while panel.Affirmed():
            board = boardCtrl.GetValue()
            tw = thread_wait.GetValue()

            el_1 = di_1_level.GetValue()
            del di_event_trigger[0]
            di_event_trigger.insert(0, el_1)
            el_2 = di_2_level.GetValue()
            del di_event_trigger[1]
            di_event_trigger.insert(1, el_2)
            el_3 = di_3_level.GetValue()
            del di_event_trigger[2]
            di_event_trigger.insert(2, el_3)
            el_4 = di_4_level.GetValue()
            del di_event_trigger[3]
            di_event_trigger.insert(3, el_4)
            el_5 = di_5_level.GetValue()
            del di_event_trigger[4]
            di_event_trigger.insert(4, el_5)

            av_1 = ai_1_level.GetValue()
            del ai_event_trigger[0]
            ai_event_trigger.insert(0, av_1)
            av_2 = ai_2_level.GetValue()
            del ai_event_trigger[1]
            ai_event_trigger.insert(1, av_2)

            ct_1 = ct_1_level.GetValue()
            del counter_threshold[0]
            counter_threshold.insert(0, ct_1)
            ct_2 = ct_2_level.GetValue()
            del counter_threshold[1]
            counter_threshold.insert(1, ct_2)

            ct_1_cb = ct_1_count.GetValue()
            del counter_events[0]
            counter_events.insert(0, ct_1_cb)
            ct_2_cb = ct_2_count.GetValue()
            del counter_events[1]
            counter_events.insert(1, ct_2_cb)

            panel.SetResult(
                board,
                tw,
                el_1,
                el_2,
                el_3,
                el_4,
                el_5,
                av_1,
                av_2,
                ct_1,
                ct_2,
                counter_threshold,
                ai_event_trigger,
                di_event_trigger,
                di_event_memory,
                ai_event_memory,
                counter_events,
                counter_old,
                ct_1_cb,
                ct_2_cb
            )


    def __init__(self):
        self.AddAction(SetDigitalChannel)
        self.AddAction(ClearDigitalChannel)
        self.AddAction(SetAnalogChannel)
        self.AddAction(ClearAnalogChannel)
        self.AddAction(ReadDigitalChannel)
        self.AddAction(ReadAnalogChannel)
        self.AddAction(Counter)
        self.AddAction(Info)
        print self.text.txt_Initiated
   
        
    def __start__(
        self,
        detect_board,
        tw,
        el_1,
        el_2,
        el_3,
        el_4,
        el_5,
        av_1,
        av_2,
        ct_1,
        ct_2,
        counter_threshold,
        ai_event_trigger,
        di_event_trigger,
        di_event_memory,
        ai_event_memory,
        counter_events,
        counter_old,
        ct_1_cb,
        ct_2_cb
    ):
                
        self.counter_threshold = counter_threshold
        self.counter_events = counter_events
        self.counter_old = counter_old
        self.ai_event_trigger = ai_event_trigger
        self.di_event_trigger = di_event_trigger
        self.di_event_memory = di_event_memory
        self.ai_event_memory = ai_event_memory
        self.b_nbr = detect_board
        self.thread_wait = tw
        self.found_board = -1
        
        #Load the dll
        self.dll = None
        try:
            self.dll = windll.LoadLibrary("K8055D_C.dll")
        except: 
            raise eg.Exception(self.text.txt_dllNotFound)
        if self.dll != None:
            print self.text.txt_dllLoaded
        
        #Try to find the board...
        self.found_board = self.dll.OpenDevice(self.b_nbr)
        if self.found_board == -1:
            raise eg.Exception(
                self.text.txt_BoardNbr+str(self.b_nbr)+
                self.text.txt_CannotBeFound
            )
        else:
            print (
                self.text.txt_BoardNbr+str(self.b_nbr)+
                self.text.txt_IsFound
            )
            self.dll.SetCurrentDevice(self.b_nbr)
            self.dll.ClearAllDigital()
            self.dll.ClearAllAnalog()
            self.stopThreadEvent = Event()
            thread = Thread(
                target=self.ThreadWorker,
                args=(self.stopThreadEvent,)
            )
            thread.start()
   
        
    def __stop__(self):
        if self.found_board != -1:
            self.stopThreadEvent.set()
            self.dll.SetCurrentDevice(self.b_nbr)
            self.dll.CloseDevice()
            print (
                self.text.txt_BoardNbr+str(self.b_nbr)+
                self.text.txt_IsStopped
            )    
    

    def __close__(self):
        if self.found_board != -1:
            self.stopThreadEvent.set()
            self.dll.SetCurrentDevice(self.b_nbr)
            self.dll.CloseDevice()
            print (
                self.text.txt_BoardNbr+str(self.b_nbr)+
                self.text.txt_IsDeleted
            )
        

    def ReadCounter(self, b, nbr, counter_limit, counter_event, counter_old):
            self.dll.SetCurrentDevice(b)
            ret = self.dll.ReadCounter(nbr)
            if counter_event and ret != counter_old:
                self.TriggerEvent(
                    self.text.txt_Counter+str(nbr)+
                    self.text.txt_Count+str(ret)
                )
                del self.counter_old[nbr-1]
                self.counter_old.insert(nbr-1, ret)
            if ret>counter_limit and ret < 255:
                self.TriggerEvent(
                    self.text.txt_Counter+str(nbr)+
                    self.text.txt_Value+str(ret)
                )
                self.dll.ResetCounter(nbr)


    def ReadAnalogIn(self, b, nbr, trig_level):
            self.dll.SetCurrentDevice(b)
            ret = self.dll.ReadAnalogChannel(nbr)
            if ret>trig_level:
                for i in range (0, 2):
                    if nbr == i+1:
                        if(
                        	self.ai_event_memory[i] != ret
                        	and(
                        		ret > self.ai_event_memory[i]+1
	                        	or ret < self.ai_event_memory[i]-1
	                        )
                        ):
                            self.TriggerEvent(
                                self.text.txt_AI+str(nbr)+
                                self.text.txt_Value, str(ret)
                            )
                            del self.ai_event_memory[i]
                            self.ai_event_memory.insert(i, ret)
   
                
    def ReadDigitalIn(self, b, nbr, trig_level):
            self.dll.SetCurrentDevice(b)
            ret = self.dll.ReadDigitalChannel(nbr)
            for i in range (0, 5):
                if nbr == i+1:
                    if ret != trig_level:
                        if self.di_event_memory[i] != ret:
                            self.TriggerEvent(
                                self.text.txt_DI+str(nbr)+
                                self.text.txt_State+str(ret)
                            )
                            del self.di_event_memory[i]
                            self.di_event_memory.insert(i, ret)
                    if self.di_event_memory[i] != ret:
                        self.TriggerEvent(
                            self.text.txt_DI+str(nbr)+
                            self.text.txt_State+str(ret)
                        )
                        del self.di_event_memory[i]
                        self.di_event_memory.insert(i, ret)


    def ThreadWorker(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            b = self.b_nbr
            for j in range(0, 2):
                self.ReadCounter(
                    b,
                    j+1,
                    self.counter_threshold[j],
                    self.counter_events[j],
                    self.counter_old[j]
                )
            for j in range(0, 2):
                self.ReadAnalogIn(b, j+1, self.ai_event_trigger[j])
            for j in range(0, 5):
                self.ReadDigitalIn(b, j+1, self.di_event_trigger[j])
                    
#            print b, self.counter_threshold
#            print b, self.counter_old
#            print b, self.ai_event_trigger
#            print b, self.di_event_trigger
#            print b, self.di_event_memory
#            print b, self.ai_event_memory

            stopThreadEvent.wait(self.thread_wait)
        print self.text.txt_Polling



class SetDigitalChannel(eg.ActionClass):
    iconFile = "digital-out-on"

    def __call__(self, b, do):
        self.plugin.dll.SetCurrentDevice(b)
        ret = self.plugin.dll.SetDigitalChannel(do)
        return ret


    #Digital outputs on the board, 8 in total
    def Configure(self, b = 0, do = 1):
        panel = eg.ConfigPanel(self)
        board_n = self.plugin.b_nbr
        digitalOut_ctrl = panel.SpinIntCtrl(do, 1, 8)
        digitalOut_ctrl.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_ConfSetDO, digitalOut_ctrl)
        while panel.Affirmed():
            b = board_n
            do = digitalOut_ctrl.GetValue()
            panel.SetResult(
                b,
                do
            )



class ClearDigitalChannel(eg.ActionClass):
    iconFile = "digital-out-off"

    def __call__(self, b, do):
        self.plugin.dll.SetCurrentDevice(b)
        ret = self.plugin.dll.ClearDigitalChannel(do)
        return ret


    #Digital outputs on the board, 8 in total
    def Configure(self, b = 0, do = 1):
        panel = eg.ConfigPanel(self)
        board_n = self.plugin.b_nbr
        digitalOut_ctrl = panel.SpinIntCtrl(do, 1, 8)
        digitalOut_ctrl.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_ConfClrDO, digitalOut_ctrl)
        while panel.Affirmed():
            b = board_n
            do = digitalOut_ctrl.GetValue()
            panel.SetResult(
                b,
                do
            )



class SetAnalogChannel(eg.ActionClass):
    iconFile = "analog-out-on"

    def __call__(self, b, ao, av):
        self.plugin.dll.SetCurrentDevice(b)
        ret = self.plugin.dll.OutputAnalogChannel(ao, av)
        return ret


    #Analog outputs on the board, 2 in total
    def Configure(self, b = 0, ao = 1, av = 254):
        panel = eg.ConfigPanel(self)
        board_n = self.plugin.b_nbr
        analogOut_ctrl = panel.SpinIntCtrl(ao, 1, 2)
        analogOut_ctrl.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_ConfSetAO, analogOut_ctrl)
        analogOut_value = panel.SpinIntCtrl(av, 0, 254)
        analogOut_value.SetInitialSize((50,-1))
        panel.AddLine(self.text.txt_ConfSetVa, analogOut_value)
        while panel.Affirmed():
            b = board_n
            ao = analogOut_ctrl.GetValue()
            av = analogOut_value.GetValue()
            panel.SetResult(
                b,
                ao,
                av
            )



class ClearAnalogChannel(eg.ActionClass):
    iconFile = "analog-out-off"

    def __call__(self, b, ao):
        self.plugin.dll.SetCurrentDevice(b)
        ret = self.plugin.dll.ClearAnalogChannel(ao)
        return ret


    #Analog outputs on the board, 2 in total
    def Configure(self, b = 0, ao = 1):
        panel = eg.ConfigPanel(self)
        board_n = self.plugin.b_nbr
        analogOut_ctrl = panel.SpinIntCtrl(ao, 1, 2)
        analogOut_ctrl.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_ConfCLrAO, analogOut_ctrl)
        while panel.Affirmed():
            b = board_n
            ao = analogOut_ctrl.GetValue()
            panel.SetResult(
                b,
                ao
            )



class ReadDigitalChannel(eg.ActionClass):
    iconFile = "digital-in"

    def __call__(self, b, di):
        self.plugin.dll.SetCurrentDevice(b)
        ret = self.plugin.dll.ReadDigitalChannel(di)
        print ret
        return ret


    #Digital inputs on the board, 5 in total
    def Configure(self, b = 0, di = 1):
        panel = eg.ConfigPanel(self)
        board_n = self.plugin.b_nbr
        digitalIn_ctrl = panel.SpinIntCtrl(di, 1, 5)
        digitalIn_ctrl.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_ConfRdDI, digitalIn_ctrl)
        while panel.Affirmed():
            b = board_n
            di = digitalIn_ctrl.GetValue()
            panel.SetResult(
                b,
                di
            )



class ReadAnalogChannel(eg.ActionClass):
    iconFile = "analog-in"

    def __call__(self, b, ai):
        self.plugin.dll.SetCurrentDevice(b)
        ret = self.plugin.dll.ReadAnalogChannel(ai)
        print ret
        return ret


    #Analog inputs on the board, 2 in total
    def Configure(self, b = 0, ai = 1):
        panel = eg.ConfigPanel(self)
        board_n = self.plugin.b_nbr
        analogIn_ctrl = panel.SpinIntCtrl(ai, 1, 2)
        analogIn_ctrl.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_ConfRdAI, analogIn_ctrl)
        while panel.Affirmed():
            b = board_n
            ai = analogIn_ctrl.GetValue()
            panel.SetResult(
                b,
                ai
            )



class Counter(eg.ActionClass):
    iconFile = "counter"

    def __call__(self, b, ct, cdb):
        self.plugin.dll.SetCurrentDevice(b)
        ret = self.plugin.dll.ReadCounter(ct)
        print ret
        return ret


    #Counters on the board, 2 in total
    def Configure(self, b = 0, ct = 1, cdb = 2):
        panel = eg.ConfigPanel(self)
        board_n = self.plugin.b_nbr
        counter_ctrl = panel.SpinIntCtrl(ct, 1, 2)
        counter_ctrl.SetInitialSize((40,-1))
        panel.AddLine(self.text.txt_ConfCntr, counter_ctrl)
        ctr_debounce = panel.Choice(cdb, choices=['0', '2', '10', '1000'])
        panel.AddLine(self.text.txt_ConfDbns, ctr_debounce)
        while panel.Affirmed():
            b = board_n
            ct = counter_ctrl.GetValue()
            cdb = ctr_debounce.GetValue()
            panel.SetResult(
                b,
                ct,
                cdb
            )
            self.plugin.dll.SetCounterDebounceTime(ct, cdb)

        
        
class Info(eg.ActionClass):
    iconFile = "info"

    def __call__(self):
        self.plugin.dll.Version()

        
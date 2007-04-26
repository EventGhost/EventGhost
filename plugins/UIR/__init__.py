import eg

class PluginInfo(eg.PluginInfo):
    name = "UIR / Irman"
    author = "Bitmonster"
    version = "1.0.0"
    kind = "remote"
    description = (
        'Hardware plugin for the <a href="http://fly.cc.fer.hr/~mozgic/UIR/">'
        'Universal Infrared Receiver V1 (UIR)</a> '
        'and the <a href="http://www.evation.com/irman/index.html">Irman</a> '
        'device.'
    )


import wx
import time
import threading
import win32event


class UIR(eg.RawReceiverPlugin):
    canMultiLoad = True
    
    @eg.LogIt
    def __start__(self, port):
        self.port = port
        self.stopEvent = win32event.CreateEvent(None, 1, 0, None)
        self.receiveThread = threading.Thread(target=self.ReceiveThread)
        self.receiveThread.start()    
    
    
    @eg.LogIt
    def __stop__(self):
        if self.receiveThread:
            win32event.SetEvent(self.stopEvent)
            self.receiveThread.join(1.0)
            self.receiveThread = None
    
    
    @eg.LogItWithReturn
    def ReceiveThread(self):
        from win32event import (
            ResetEvent, 
            MsgWaitForMultipleObjects, 
            QS_ALLINPUT, 
            WAIT_OBJECT_0, 
            WAIT_TIMEOUT,
        )
        from win32file import ReadFile, AllocateReadBuffer, GetOverlappedResult
        from win32api import GetLastError

        self.buffer = ""
        self.lastReceivedTime = time.clock()
        try:
            serialPort = eg.SerialPort(self.port, baudrate=9600)
        except:
            self.PrintError("Can't open COM port.")
            return
        try:
            serialPort.timeout = 1.0
            serialPort.setRTS()
            serialPort.setDTR()
            time.sleep(0.05)
            serialPort.flushInput()
            serialPort.write("I")
            time.sleep(0.05)
            serialPort.write("R")
            if serialPort.read(2) != "OK":
                self.PrintError("Got no OK from device.")
                #return
            overlapped = serialPort._overlappedRead
            hComPort = serialPort.hComPort
            hEvent = overlapped.hEvent
            winEvents = (hEvent, self.stopEvent)
            n = 1
            waitingOnRead = False
            buf = AllocateReadBuffer(n)
            while True:
                if not waitingOnRead:
                    ResetEvent(hEvent)
                    hr, _ = ReadFile(hComPort, buf, overlapped)
                    if hr == 997:
                        waitingOnRead = True
                    elif hr == 0:
                        pass
                    else:
                        self.PrintError("error")
                        return
    
                rc = MsgWaitForMultipleObjects(winEvents, 0, 1000, QS_ALLINPUT)
                if rc == WAIT_OBJECT_0:
                    n = GetOverlappedResult(hComPort, overlapped, 1)
                    if n:
                        self.HandleChar(str(buf))
                    waitingOnRead = False
                elif rc == WAIT_OBJECT_0+1:
                    return
                elif rc == WAIT_TIMEOUT:
                    pass
                else:
                    self.PrintError("unknown message")
        finally:
            serialPort.close()
                        
                        
    def HandleChar(self, data):
        now = time.clock()
        if self.lastReceivedTime + 1.0 < now:
            self.buffer = ""
        self.lastReceivedTime = now
        self.buffer += "%X" % ord(data)
        if len(self.buffer) >= 12:
            self.TriggerEvent(self.buffer)
            self.buffer = ""
            
        
    def Configure(self, port=0):
        dialog = eg.ConfigurationDialog(self)
        portCtrl = eg.SerialPortChoice(dialog, value=port)
        dialog.sizer.Add(wx.StaticText(dialog, -1, 'COM Port:'))
        dialog.sizer.Add(portCtrl)
        
        if dialog.AffirmedShowModal():
            return (
                portCtrl.GetValue(),
            )
                    
        
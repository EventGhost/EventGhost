# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2019 obermann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import eg


eg.RegisterPlugin(
    name = "REALmagic Remote",
    author = "obermann",
    version = "4.1.0",
    kind = "remote",
    canMultiLoad = False,
    guid = "{664E1E2C-3D12-4EB0-BE48-4BF858460A8F}",
    description = (
        "Plugin for REALmagic remote control. "
        "Works directly with COM port."
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAWUlEQVQ4T2NkoBAw4tL/n4EBiFAB"
        "UDGGeqwGpKWlYWiGGTVr1iwUPdgM+A80gCEqKoph2bJlcCfA+EQbgMtr9DMA5mR0etQFyxhGSBiA"
        "EiGuvEBcZiIlhwMA+TZdEbVMElwAAAAASUVORK5CYII="
    ),
)


import threading
import time


CODES = {
    0x8D : "POWER"      ,
    0x8E : "DVD"        ,
    0x91 : "LEFT"       ,
    0x8F : "UP"         ,
    0xBE : "RIGHT"      ,
    0x93 : "DOWN"       ,
    0x92 : "SELECT"     ,
    0x94 : "MENU"       ,
    0x95 : "TITLE"      ,
    0x96 : "OSD"        ,
    0x97 : "LANGUAGE"   ,
    0x98 : "ANGLE"      ,
    0x99 : "SUBTITLE"   ,
    0x9A : "PLAYPAUSE"  ,
    0x9B : "STOP"       ,
    0x9C : "SLOW"       ,
    0x9D : "EJECT"      ,
    0x9E : "REWIND"     ,
    0x9F : "FASTFORWARD",
    0xA0 : "PREVIOUS"   ,
    0xA1 : "NEXT"       ,
    0xA2 : "VOLUME_UP"  ,
    0xA6 : "VOLUME_DOWN",
    0xAB : "MUTE"       ,
    0x25 : "LR"         ,
    0xA3 : "1"          ,
    0xA4 : "2"          ,
    0xAC : "3"          ,
    0xA7 : "4"          ,
    0xA8 : "5"          ,
    0x41 : "6"          ,
    0x0D : "7"          ,
    0x11 : "8"          ,
    0xA9 : "9"          ,
    0x19 : "0"          ,
    0x15 : "VGATV"      ,
    0x21 : "ENT"
}
# Accelerator
COMMANDS = [ CODES.get(i, "BLIP") for i in range(0x100) ]


class Timer(threading.Thread):

    def __init__(self, function):
        self.function = function
        self.lastTime = 0.0
        super(Timer, self).__init__(name="REALmagic_Timer")

    def endure(self):
        self.lastTime = time.clock()

    def run(self):
        # Phase-locked loop
        pause = 0.12
        while pause > 0.04: # 0.0 would do, but must be sure
            time.sleep(pause)
            # Next is the simplification/optimization of
            # pause = (lastTime - prevLastTime) - (clock() - lastTime) + 0.02 # Tolerate by +0.02s
            # so increase from 0.12 to 0.15 would mean 0.05s waiting for a late endure()
            pause = 0.12 - (time.clock() - self.lastTime)
        #print "EndLastEvent"
        self.function()


class REALmagic(eg.PluginClass):

    def __start__(self, port=0):
        self.timer = Timer(self.EndLastEvent)
        self.serialThread = eg.SerialThread()
        # According Sigma Designs REALmagic Xcard User's Guide
        self.serialThread.Open(port, baudrate=1200, mode='8N1')
        self.serialThread.SetRts(flag=True)
        self.serialThread.SetReadEventCallback(self.HandleReceive)
        self.serialThread.Start()

    def __stop__(self):
        self.serialThread.Close()
        if self.timer.isAlive():
            self.timer.join()

    def HandleReceive(self, serial):
        # On very short (unsure/accidental) click: code = 83xxxx
        # On firm click: code = 83xxxx83xxxx
        # (where all xx are the same)
        # While keep pressing: code = 83xxxx
        # with interval of ~0.09-0.11s
        # NOTE! If IR receiver misses initial click signal from remote
        # (e.g. press starts behind an obsticale),
        # it produces key press codes of the previous known click.
        #print "REALmagic go"
        if len(serial.buffer) == 6:
            self.TriggerEnduringEvent(COMMANDS[ord(serial.buffer[1])])
            self.timer = Timer(self.EndLastEvent)
            self.timer.start()
        else:
            self.timer.endure()
        serial.buffer = ""

    def Configure(self, port=0):
        panel = eg.ConfigPanel()
        portCtrl = panel.SerialPortChoice(port)
        panel.AddCtrl(portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())

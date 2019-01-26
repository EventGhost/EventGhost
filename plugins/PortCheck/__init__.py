# -*- coding: utf-8 -*-
#
# plugins/PortCheck/__init__.py
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


import eg


eg.RegisterPlugin(
    name="PortCheck",
    author="bengalih",
    version="0.2.2",
    kind="other",
    guid="{D32066FB-83FA-42D2-AC0D-4C356807268C}",
    description=(
        "This plugin checks TCP port status (open/closed) on a host.  "
        "Events can be generated for port status."
    ),
    createMacrosOnAdd=True,
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=7423",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0RVh0"
        "U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAKeSURBVDjLpZPrS5NRHMf9O/Zse2yCBDKi"
        "EEFCqL0KEok9mg3FvCxL09290jZj2EyLMnJexkgpLbPUanPObOrU5taUMnHZo4SYe9OFasPoYt/O"
        "sxczSXxRB75wOJzP53eucQDi/id/DRT6DiXkTR/U53hS2cwn+8PSx+Kw1JXESp1J+gz73oRdBfne"
        "NEbmSQnpPDLcDFrQv9wdTddiC0pdxyDpo0OSXprZUUCqMlnjyZGrc0Y4Vwdge3UNprmqaLi+Y7Uf"
        "TTPVOGATRFJsAmabINeTKspyJ69zMDexNlCOSn8pNDNnoCOpIKnxnYX9zT1cnKqE2MJfF1/ni2IC"
        "mTvZoBrLjlbmYA5UeU9BMV0ExVQh1FNFcK8NweBVwkEkeb1HkHiFb4gJMh+L2a5gC6zBZlT6SqB8"
        "KidgAZSTJJ4CjL91gWuhyBraXzTBNteE+AY+GxMctSduPFi5jbqABlpvMVnJIBY/zkM1UYSxteEo"
        "/HPzB9qfX4JhogT9wS4IjdRGTCC5T28MLPfA6Fehzq/F52+fotCHr+9isGW2AWpXDvTu0xgIdkJY"
        "+6egl2ZvzDejY+EydJNymH01iHz/EoU3f23C8uwCyp3Z0BBBa6AeHV4z6Gpqawtpt4QG+WA67Ct3"
        "UTMhh9p9EvXTFVh6v4D22UaUDR2HwnECOmcu7K97kGE9DLqK2jrEFKtAtI9cjdmjwUP2DqpG86Ed"
        "yYVqWAalgwsH5+DRUjeMwyUQqnnrtJoSbXtISc18Jr6Ripjc5XAQSVvADP1oMc6NyNFGtmAnsN5Z"
        "DEEZL0JgZsenvKeRz9AmKiTtlKDDb0bfSyv65q2weE1Ib02DUMEL0SqK2fUz0ef5CbSB0tO1FCvU"
        "8sJCFS9MKrIkerqM2v0z/Ut+A2fQrOU2UvurAAAAAElFTkSuQmCC"
    ),
)

# changelog:
#   0.2.2   code cleanup


import socket
from threading import Event, Lock, Thread


prefix = "PortCheck"


class PortCheckPlugin(eg.PluginBase):
    def __init__(self):
        self.hosts = {}
        self.AddAction(OneCheck)
        self.AddAction(AddHost)
        self.AddAction(RemoveHost)
        self.AddAction(RemoveAllHosts)
        self.AddAction(GetHostsStatus)

    def __start__(self):
        print "PortCheck is started."
        for host in self.hosts:
            print "Starting thread " + self.hosts[host].name
            self.hosts[host].StartThread()

    def __stop__(self):
        print "PortCheck is stopped."
        for host in self.hosts:
            print "Stopping thread " + self.hosts[host].name
            self.hosts[host].StopThread()
        for host in self.hosts:
            print "Joining thread " + self.hosts[host].name
            self.hosts[host].portcheckThread.join()

    def __close__(self):
        print "PortCheck is closed."
        while len(self.hosts) > 0:
            for host in self.hosts:
                print "Removing " + self.hosts[host].name
                self.RemoveHost(host)
                break

    def RemoveHost(self, host=""):
        hostToDel = self.hosts.get(host, None)
        if hostToDel:
            if hostToDel.GetThreadState() == "Thread is running":
                hostToDel.StopThread()
                hostToDel.portcheckThread.join()
            elif hostToDel.GetThreadState() == "Thread is finishing his job":
                hostToDel.portcheckThread.join()
            elif hostToDel.GetThreadState() == "Problem !":
                print "Problem !!!"
            else:
                print "--- " + hostToDel.GetThreadState()
            del self.hosts[host]
            del hostToDel
        else:
            print "PortCheck Plugin: " + host + " isn't in managed list. Check syntax."
        if len(self.hosts) == 0:
            print "PortCheck Plugin: Managed list of hosts is empty."

    def AddHost(self, host):
        print "PortCheck Plugin: Adding host " + host.name + " to managed list."
        hostToDel = self.hosts.get(host.name, None)
        if hostToDel:
            print "PortCheck Plugin: " + host.name + " already exists in managed list. It will be replaced."
            self.RemoveHost(host.name)
        self.hosts[host.name] = host
        self.hosts[host.name].StartThread()


class OneCheck(eg.ActionBase):
    name = "Quick Host Check"
    description = "Check host port once. The port state is returned in eg.result. Optionally, you can generate an event."

    def __call__(self, hostName, displayName, portNumber, timeoutNumber, sendEvent, eventPortOpen, eventPortClosed):
        global prefix

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeoutNumber)

        print hostName
        try:
            result = sock.connect_ex((hostName, portNumber))
            sock.close()
            if result == 0:
                hostStatus = "port open"
            else:
                hostStatus = "port closed"
        except:
            hostStatus = "hostname unresolved"
            print "Error: can't resolve " + hostName

        if eventPortOpen == "":
            if displayName == "":
                eventPortOpen = hostName + "_PORT_OPEN"
            else:
                eventPortOpen = displayName + "_PORT_OPEN"
        if eventPortClosed == "":
            if displayName == "":
                eventPortClosed = hostName + "_PORT_CLOSED"
            else:
                eventPortClosed = displayName + "_PORT_CLOSED"
        if sendEvent:
            if hostStatus == "port open":
                eg.TriggerEvent(prefix=prefix, suffix=eventPortOpen)
            else:
                eg.TriggerEvent(prefix=prefix, suffix=eventPortClosed)
        return hostStatus

    def Configure(self, hostName="", displayName="", portNumber=80, timeoutNumber=3, sendEvent=False, eventPortOpen="",
                  eventPortClosed=""):
        panel = eg.ConfigPanel()
        displayNameEdit = panel.TextCtrl(displayName)
        hostNameEdit = panel.TextCtrl(hostName)
        portNumberEdit = panel.SpinIntCtrl(portNumber, min=0, max=65535)
        timeoutNumberEdit = panel.SpinIntCtrl(timeoutNumber, min=1, max=60)
        sendEventEdit = panel.CheckBox(sendEvent)
        eventPortOpenEdit = panel.TextCtrl(eventPortOpen)
        eventPortClosedEdit = panel.TextCtrl(eventPortClosed)
        panel.AddLine("Display Name (optional): ", displayNameEdit)
        panel.AddLine("Hostname or IP Address (required): ", hostNameEdit)
        panel.AddLine("Port Number to test (0-65535): ", portNumberEdit)
        panel.AddLine("Timeout (1-60s): ", timeoutNumberEdit)
        panel.AddLine()
        panel.AddLine(
            "If below is enabled, will generate an event corresponding to the host response.  eg.results will always return 'port open/closed':")
        panel.AddLine("Generate an event?", sendEventEdit)
        panel.AddLine("Event to fire on port open (optional. Default: [Display Name]_PORT_OPEN): ", eventPortOpenEdit)
        panel.AddLine("Event to fire on port closed (optional. Default: [Display Name]_PORT_CLOSED):",
                      eventPortClosedEdit)
        while panel.Affirmed():
            panel.SetResult(
                hostNameEdit.GetValue(),
                displayNameEdit.GetValue(),
                portNumberEdit.GetValue(),
                timeoutNumberEdit.GetValue(),
                sendEventEdit.GetValue(),
                eventPortOpenEdit.GetValue(),
                eventPortClosedEdit.GetValue()
            )


class AddHost(eg.ActionBase):
    name = "Add Managed Host"
    description = "Adds a host/port pair to a list of watched hosts.  Each host/port pair is run in a different thread."

    def __call__(self, hostName, displayName, portNumber, timeoutNumber, checkintervalNumber, eventPortOpen,
                 eventPortClosed, delayEventPortOpen, repeatTriggerEventOpen, delayEventPortClosed,
                 repeatTriggerEventClosed, printDebugMessages):
        instName = hostName + ":" + str(portNumber)
        host = Host(instName, hostName, displayName, portNumber, timeoutNumber, checkintervalNumber, eventPortOpen,
                    eventPortClosed, delayEventPortOpen, repeatTriggerEventOpen, delayEventPortClosed,
                    repeatTriggerEventClosed, printDebugMessages)
        self.plugin.AddHost(host)

    def Configure(self, hostName="", displayName="", portNumber=80, timeoutNumber=3, checkintervalNumber=5,
                  eventPortOpen="", eventPortClosed="", delayEventPortOpen=1, repeatTriggerEventOpen=0,
                  delayEventPortClosed=1, repeatTriggerEventClosed=0, printDebugMessages=0):
        panel = eg.ConfigPanel()
        displayNameEdit = panel.TextCtrl(displayName)
        hostNameEdit = panel.TextCtrl(hostName)
        portNumberEdit = panel.SpinIntCtrl(portNumber, min=0, max=65535)
        timeoutNumberEdit = panel.SpinIntCtrl(timeoutNumber, min=1, max=60)
        checkintervalNumberEdit = panel.SpinIntCtrl(checkintervalNumber, min=1, max=86400)
        eventPortOpenEdit = panel.TextCtrl(eventPortOpen)
        eventPortClosedEdit = panel.TextCtrl(eventPortClosed)
        delayEventPortOpenEdit = panel.SpinIntCtrl(delayEventPortOpen, min=1, max=99999)
        repeatTriggerEventOpenEdit = panel.SpinIntCtrl(repeatTriggerEventOpen, min=0, max=99999)
        delayEventPortClosedEdit = panel.SpinIntCtrl(delayEventPortClosed, min=1, max=99999)
        repeatTriggerEventClosedEdit = panel.SpinIntCtrl(repeatTriggerEventClosed, min=0, max=99999)
        printDebugMessagesEdit = panel.CheckBox(printDebugMessages)

        panel.AddLine("Display Name (optional): ", displayNameEdit)
        panel.AddLine("Hostname or IP Address (required): ", hostNameEdit)
        panel.AddLine("Port Number to test (0-65535): ", portNumberEdit)
        panel.AddLine("Timeout (1-60s): ", timeoutNumberEdit)
        panel.AddLine("Check Interval (1-86400s): ", checkintervalNumberEdit)
        panel.AddLine()
        panel.AddLine("Event Settings:")
        panel.AddLine("Event to fire on port open (optional. Default: [Display Name]_PORT_OPEN): ", eventPortOpenEdit)
        panel.AddLine("Event to fire on port closed (optional. Default: [Display Name]_PORT_CLOSED):",
                      eventPortClosedEdit)
        panel.AddLine()
        panel.AddLine("Number of contiguous successful port checks before firing the port open event: ",
                      delayEventPortOpenEdit)
        panel.AddLine("Repeat port open events after contiguous number of occurrences (0=no repeat):",
                      repeatTriggerEventOpenEdit)
        panel.AddLine("Number of contiguous unsuccessful port checks before firing the port closed event: ",
                      delayEventPortClosedEdit)
        panel.AddLine("Repeat port closed events after contiguous number of occurrences (0=no repeat):",
                      repeatTriggerEventClosedEdit)
        panel.AddLine("Print debug messages: ", printDebugMessagesEdit)

        while panel.Affirmed():
            panel.SetResult(
                hostNameEdit.GetValue(),
                displayNameEdit.GetValue(),
                portNumberEdit.GetValue(),
                timeoutNumberEdit.GetValue(),
                checkintervalNumberEdit.GetValue(),
                eventPortOpenEdit.GetValue(),
                eventPortClosedEdit.GetValue(),
                delayEventPortOpenEdit.GetValue(),
                repeatTriggerEventOpenEdit.GetValue(),
                delayEventPortClosedEdit.GetValue(),
                repeatTriggerEventClosedEdit.GetValue(),
                printDebugMessagesEdit.GetValue(),
            )


class RemoveHost(eg.ActionBase):
    name = "Remove Managed Host"
    description = "Removes a host/port pair from list of managed hosts.  The associated thread will be stopped."

    def __call__(self, instName):
        self.plugin.RemoveHost(instName)

    def Configure(self, instName=""):
        panel = eg.ConfigPanel()
        instNameEdit = panel.TextCtrl(instName)
        panel.AddLine("Enter the hostname:port pair to remove from managed hosts:")
        panel.AddLine("Hostname:port (e.g: 10.10.10.100:80): ", instNameEdit)
        while panel.Affirmed():
            panel.SetResult(
                instNameEdit.GetValue())


class RemoveAllHosts(eg.ActionBase):
    name = "Remove All Managed Hosts"
    description = "Clears the managed hosts list.  All threads will be stopped."

    def __call__(self):
        res = {}
        for hostName in self.plugin.hosts:
            res[hostName] = hostName
        for hostName in res:
            self.plugin.RemoveHost(hostName)


class GetHostsStatus(eg.ActionBase):
    name = "Get Managed Hosts Status"
    description = "Returns eg.result containing the status of all managed hosts."
    description += "This can be used to output host status to other events/script."

    def __call__(self, displayNameShow, hostNameShow, portNumberShow, closedPortsShow, openPortsShow, returnDict,
                 printDebugMessages):
        res = {}
        returnString = ""
        if not self.plugin.hosts and printDebugMessages:
            print "No managed hosts"
            return
        for hostName in self.plugin.hosts:
            host = self.plugin.hosts[hostName]
            if (host.GetStatus() == "port open" and openPortsShow == 1) or (
                host.GetStatus() == "port closed" and closedPortsShow == 1):
                res[hostName] = ""
                if displayNameShow == 1:
                    res[hostName] += host.displayName + ","
                if hostNameShow == 1:
                    res[hostName] += host.hostName + ","
                if portNumberShow == 1:
                    res[hostName] += str(host.portNumber) + ","
                res[hostName] = res[hostName][:-1]  # trim trailing comma
        if returnDict == 1:
            if printDebugMessages:
                print res
            return res
        else:
            for hostName in res:
                returnString = returnString + res[hostName] + "\n"
            returnString = returnString[:-1]  # trim trailing line return
            if printDebugMessages:
                print returnString
            return returnString

    def Configure(self, displayNameShow=1, hostNameShow=1, portNumberShow=1, closedPortsShow=1, openPortsShow=0,
                  returnDict=0, printDebugMessages=0):
        panel = eg.ConfigPanel()
        displayNameEdit = panel.CheckBox(displayNameShow)
        hostNameEdit = panel.CheckBox(hostNameShow)
        portNumberEdit = panel.CheckBox(portNumberShow)
        closedPortsEdit = panel.CheckBox(closedPortsShow)
        openPortsEdit = panel.CheckBox(openPortsShow)
        returnDictEdit = panel.CheckBox(returnDict)
        printDebugMessagesEdit = panel.CheckBox(printDebugMessages)
        panel.AddLine("Select the items to return in a status query\n")
        panel.AddLine("Closed port status: ", closedPortsEdit, "Open ports status: ", openPortsEdit, "\n")
        panel.AddLine("Display names: ", displayNameEdit)
        panel.AddLine("Host names: ", hostNameEdit)
        panel.AddLine("Port numbers: ", portNumberEdit)
        panel.AddLine("Return result as dictionary: ", returnDictEdit)
        panel.AddLine("Print debug messages: ", printDebugMessagesEdit)
        while panel.Affirmed():
            panel.SetResult(
                displayNameEdit.GetValue(),
                hostNameEdit.GetValue(),
                portNumberEdit.GetValue(),
                closedPortsEdit.GetValue(),
                openPortsEdit.GetValue(),
                returnDictEdit.GetValue(),
                printDebugMessagesEdit.GetValue()
            )


class Host:
    def __init__(self, instName, hostName, displayName, portNumber, timeoutNumber, checkintervalNumber, eventPortOpen,
                 eventPortClosed, delayEventPortOpen, repeatTriggerEventOpen, delayEventPortClosed,
                 repeatTriggerEventClosed, printDebugMessages):
        self.name = instName
        self.hostName = hostName
        self.displayName = displayName
        self.portNumber = portNumber
        self.timeoutNumber = timeoutNumber
        self.checkintervalNumber = checkintervalNumber
        self.repeatTriggerEventOpen = repeatTriggerEventOpen
        self.repeatTriggerEventClosed = repeatTriggerEventClosed
        self.printDebugMessages = printDebugMessages
        self.status = "unknown"
        self.lastPortCheckResult = "unknown"
        global prefix

        if eventPortOpen == "":
            if displayName == "":
                self.eventPortOpen = self.name + "_PORT_OPEN"
            else:
                self.eventPortOpen = displayName + "_PORT_OPEN"
        else:
            self.eventPortOpen = eventPortOpen

        if eventPortClosed == "":
            if displayName == "":
                self.eventPortClosed = self.name + "_PORT_CLOSED"
            else:
                self.eventPortClosed = displayName + "_PORT_CLOSED"
        else:
            self.eventPortClosed = eventPortClosed

        self.delayEventPortOpen = delayEventPortOpen
        self.delayEventPortClosed = delayEventPortClosed

        self.portcheckThread = None
        self.stopPortCheckThreadEvent = Event()
        self.lock = Lock()

    def PortCheckThread(self, stopPortCheckThreadEvent):
        print "PortCheck Plugin: Thread " + self.name + "  is starting.  Socket Timeout=" + str(
            self.timeoutNumber) + "s Check Interval=" + str(self.checkintervalNumber) + "s"

        eventsPortOpen = 0
        eventsPortClosed = 0
        repeatCounterOpen = 0
        repeatCounterClosed = 0

        while not stopPortCheckThreadEvent.isSet():
            if self.printDebugMessages:
                print "Thread " + self.name + " is running.  Last status: " + self.lastPortCheckResult + ". repeatCounterOpen=" + str(
                    repeatCounterOpen) + "/" + str(self.repeatTriggerEvent) + " repeatCounterClosed=" + str(
                    repeatCounterClosed) + "/" + str(self.repeatTriggerEvent)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeoutNumber)
            result = sock.connect_ex((self.hostName, self.portNumber))
            sock.close()

            if result == 0:
                eventsPortOpen += 1
                eventsPortClosed = 0
                repeatCounterClosed = 0
                self.lock.acquire()
                try:
                    self.lastPortCheckResult = "port open"
                    if eventsPortOpen >= self.delayEventPortOpen:
                        if self.status != "port open":
                            self.status = "port open"
                            eg.TriggerEvent(prefix=prefix, suffix=self.eventPortOpen)
                            repeatCounterOpen = 0
                        if self.repeatTriggerEventOpen > 0 and repeatCounterOpen == self.repeatTriggerEventOpen:
                            eg.TriggerEvent(prefix=prefix, suffix=self.eventPortOpen)
                            repeatCounterOpen = 0

                finally:
                    self.lock.release()
                    repeatCounterOpen += 1
            else:
                eventsPortOpen = 0
                eventsPortClosed += 1
                repeatCounterOpen = 0
                self.lock.acquire()
                try:
                    self.lastPortCheckResult = "port closed"
                    if eventsPortClosed >= self.delayEventPortClosed:
                        if self.status != "port closed":
                            self.status = "port closed"
                            eg.TriggerEvent(prefix=prefix, suffix=self.eventPortClosed)
                            repeatCounterClosed = 0
                        if self.repeatTriggerEventClosed > 0 and repeatCounterClosed == self.repeatTriggerEventClosed:
                            eg.TriggerEvent(prefix=prefix, suffix=self.eventPortClosed)
                            repeatCounterClosed = 0
                finally:
                    self.lock.release()
                    repeatCounterClosed += 1

            stopPortCheckThreadEvent.wait(self.checkintervalNumber)

        print "PortCheck Plugin: Thread " + self.name + " is ending."
        self.stopPortCheckThreadEvent.clear()

    def GetStatus(self):
        self.lock.acquire()
        try:
            status = self.status
        finally:
            self.lock.release()
        return status

    def GetLastPortCheckResult(self):
        self.lock.acquire()
        try:
            res = self.lastPortCheckResult
        finally:
            self.lock.release()
        return res

    def GetThreadState(self):
        if self.portcheckThread.isAlive() and not self.stopPortCheckThreadEvent.isSet():
            return "Thread is running"
        elif self.portcheckThread.isAlive() and self.stopPortCheckThreadEvent.isSet():
            return "Thread is finishing his job"
        elif (not self.portcheckThread.isAlive()) and (not self.stopPortCheckThreadEvent.isSet()):
            return "Thread is ready to be started"
        else:
            return "Problem !"

    def StopThread(self):
        self.stopPortCheckThreadEvent.set()

    def StartThread(self):
        if self.stopPortCheckThreadEvent.isSet():
            self.stopPortCheckThreadEvent.clear()
        self.portcheckThread = Thread(target=self.PortCheckThread, args=(self.stopPortCheckThreadEvent,))
        self.portcheckThread.start()

    def Print(self):
        print self.name
        print self.displayName
        print self.status
        print self.eventPortOpen
        print self.eventPortClosed

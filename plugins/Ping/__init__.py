# -*- coding: utf-8 -*-
#
# plugins/Ping/__init__.py
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

import eg

eg.RegisterPlugin(
  name = "Ping",
  author = (
    "miljbee",
    "Sem;colon",
  ),
  version = "0.0.3",
  guid = "{59C111B9-EF9E-48DA-A57D-6231BC9AB2FD}",
  kind = "other",
  description = "This plugin generates events when an host become available or unavailable on your LAN. It uses the ping commands of windows. Please, have a look at the readme file !"
)

import os
import subprocess
from threading import Event, Thread, Lock
prefix="Ping"

class PingPlugin(eg.PluginBase):
    def __init__(self):
        self.hosts = {}
        self.AddAction(OnePing)
        self.AddAction(AddHost)
        self.AddAction(RemoveHost)
        self.AddAction(GetHostsStatus)

    def __start__(self, pingString):
        self.pingString=str(pingString)
        print "Ping is started with parameter: " + pingString
        for host in self.hosts:
            print "Starting thread " + self.hosts[host].name
            self.hosts[host].StartThread()


    def __stop__(self):
        print "Ping is stopped."
        for host in self.hosts:
            print "Stopping thread " + self.hosts[host].name
            self.hosts[host].StopThread()
        for host in self.hosts:
            print "Joining thread " + self.hosts[host].name
            self.hosts[host].pingThread.join()


    def __close__(self):
        print "Ping is closed."
        while len(self.hosts)>0:
            for host in self.hosts:
                print "Removing " + self.hosts[host].name
                self.RemoveHost(host)
                break


    def Configure(self, pingString="=32"):
        helpString = "This plugin launch ping commands to know if hosts are alive or dead.\n"
        helpString = helpString + "Ping commands are the same you would use in the command line interpreter. ping 192.168.0.1 -w 500 as an exemple.\n"
        helpString = helpString + "Unfortunately, the output of the ping command is not the same depending on the version of windows and its localization.\n"
        helpString = helpString + "Thus, you should provide here a string, that may be found in the output of the ping command when a host respond to the request.\n"
        helpString = helpString + "This string will be compared against the output of the ping command. If it's found, the host is considered to be alive.\n"
        helpString = helpString + "If it's not found, then the host is considered to be dead.\n"
        helpString = helpString + "You should test some ping commands in your command prompt to determine which string best fits with your os !\n"

        panel = eg.ConfigPanel(self)
        helpLabel=panel.StaticText(helpString)
        pingStringEdit=panel.TextCtrl(pingString)
        panel.AddLine(helpLabel)
        panel.AddLine("String to match : ",pingStringEdit)

        while panel.Affirmed():
            panel.SetResult(pingStringEdit.GetValue())

    def RemoveHost(self, host=""):
        hostToDel=self.hosts.get(host,None)
        if hostToDel:
            #print "--- " + hostToDel.GetThreadState()
            if hostToDel.GetThreadState()=="Thread is running":
                hostToDel.StopThread()
                hostToDel.pingThread.join()
            elif hostToDel.GetThreadState()=="Thread is finishing his job":
                hostToDel.pingThread.join()
            elif hostToDel.GetThreadState()=="Problem !":
                print "Oups !"
            else:
                print "--- " + hostToDel.GetThreadState()
            del self.hosts[host]
            del hostToDel
        else:
            print "Ping Plugin : /!\\ " + host + " isn't in my list !"
        if len(self.hosts)==0:
            print "Ping Plugin : the list of watched hosts is now empty !"

    def AddHost(self, host):
        print "Ping Plugin : Adding host " + host.name + " to the list of managed hosts."
        hostToDel=self.hosts.get(host.name,None)
        if hostToDel:
            print "Ping Plugin : /!\\ Host already exists, it will be replaced"
            self.RemoveHost(host.name)
        self.hosts[host.name]=host
        self.hosts[host.name].StartThread()

class OnePing(eg.ActionBase):
    name = "One Ping Now"
    description = "Send one only ping command to the specified host. The state of the hosts is returned in eg.result. Optionnaly, you can generate an event."

    def __call__(self, hostName,hostFriendlyName,pingDelay,sendEvent,eventAlive,eventDead):
        global prefix
        pingCmd = os.popen("ping " + hostName + " -w " + str(pingDelay) + " -n 1","r")
        if pingCmd.read().find(self.plugin.pingString)>-1:
            hostStatus="alive"
        else:
            hostStatus="dead"
        if eventAlive=="":
            if hostFriendlyName=="":
                eventAlive=hostName + "_IS_ALIVE"
            else:
                eventAlive=hostFriendlyName + "_IS_ALIVE"
        if eventDead=="":
            if hostFriendlyName=="":
                eventDead=hostName + "_IS_DEAD"
            else:
                eventDead=hostFriendlyName + "_IS_DEAD"
        if sendEvent:
            if hostStatus=="alive":
                eg.TriggerEvent(prefix=prefix,suffix=eventAlive)
            else:
                eg.TriggerEvent(prefix=prefix,suffix=eventDead)
        return (hostStatus=="alive")

    def Configure(self,hostName="",hostFriendlyName="",pingDelay=200,sendEvent=False,eventAlive="",eventDead=""):
        panel = eg.ConfigPanel()
        hostNameEdit=panel.TextCtrl(hostName)
        hostFriendlyNameEdit=panel.TextCtrl(hostFriendlyName)
        pingDelayEdit=panel.SpinIntCtrl(pingDelay, max=5000)
        sendEventEdit=panel.CheckBox(sendEvent)
        eventAliveEdit=panel.TextCtrl(eventAlive)
        eventDeadEdit=panel.TextCtrl(eventDead)
        panel.AddLine("Host name: ",hostNameEdit)
        panel.AddLine("Host friendly name: ",hostFriendlyNameEdit)
        panel.AddLine("Time to wait for the host response to the ping (milliseconds): ",pingDelayEdit)
        panel.AddLine()
        panel.AddLine("Generate an event ",sendEventEdit)
        panel.AddLine("if checked will generate an event corresponding to the host response, otherwise, eg.result will be set to true/false")
        panel.AddLine()
        panel.AddLine("Event string to fire if the host responds: ",eventAliveEdit)
        panel.AddLine("Event string to fire if the host doesn't responds:",eventDeadEdit)
        while panel.Affirmed():
            panel.SetResult(
                hostNameEdit.GetValue(),
                hostFriendlyNameEdit.GetValue(),
                pingDelayEdit.GetValue(),
                sendEventEdit.GetValue(),
                eventAliveEdit.GetValue(),
                eventDeadEdit.GetValue()
                )


class AddHost(eg.ActionBase):
    name = "Add Host"
    description = "Adds a host to the list of watched host. Once done, you'll get an event when the state of the host changes."

    def __call__(self,hostName,hostFriendlyName,pingDelay,eventAlive,eventDead,delayEventAlive,delayEventDead):
        host = Host(hostName,hostFriendlyName,pingDelay,eventAlive,eventDead,delayEventAlive,delayEventDead,self.plugin.pingString)
        self.plugin.AddHost(host)

    def Configure(self,hostName="",hostFriendlyName="",pingDelay=200,eventAlive="",eventDead="",delayEventAlive=1,delayEventDead=1):
        panel = eg.ConfigPanel()
        hostNameEdit=panel.TextCtrl(hostName)
        hostFriendlyNameEdit=panel.TextCtrl(hostFriendlyName)
        pingDelayEdit=panel.SpinIntCtrl(pingDelay, max=5000)
        eventAliveEdit=panel.TextCtrl(eventAlive)
        eventDeadEdit=panel.TextCtrl(eventDead)
        delayEventAliveEdit=panel.SpinIntCtrl(delayEventAlive, min=1)
        delayEventDeadEdit=panel.SpinIntCtrl(delayEventDead, min=1)


        panel.AddLine("Host Name: ",hostNameEdit)
        panel.AddLine("Host Friendly Name: ",hostFriendlyNameEdit)
        panel.AddLine("Ping delay (ms): ",pingDelayEdit)
        panel.AddLine("Name of the event to fire when host become alive: ",eventAliveEdit)
        panel.AddLine("Name of the event to fire when host become dead: ",eventDeadEdit)
        panel.AddLine("The next two settings will delay the events. As an exemple, if you set the first one to 5,\nyou will get the alive event only when five successive ping commands will be successfull")
        panel.AddLine("Number of successive successfull ping to fire the alive event: ",delayEventAliveEdit)
        panel.AddLine("Number of successive unsuccessfull ping to fire the dead event: ",delayEventDeadEdit)
        while panel.Affirmed():
            panel.SetResult(
                hostNameEdit.GetValue(),
                hostFriendlyNameEdit.GetValue(),
                pingDelayEdit.GetValue(),
                eventAliveEdit.GetValue(),
                eventDeadEdit.GetValue(),
                delayEventAliveEdit.GetValue(),
                delayEventDeadEdit.GetValue(),
            )

class RemoveHost(eg.ActionBase):
    name="Remove Host"
    description="Removes a host from the list of watched hosts. Once done, you won't receive any more event from this host."
    def __call__(self,hostName):
        self.plugin.RemoveHost(hostName)

    def Configure(self,hostName=""):
        panel = eg.ConfigPanel()
        hostNameEdit=panel.TextCtrl(hostName)
        panel.AddLine("Enter the name of the host you wish to remove, not the friendly name !")
        panel.AddLine("Host name: ",hostNameEdit)
        while panel.Affirmed():
            panel.SetResult(
                hostNameEdit.GetValue())

class GetHostsStatus(eg.ActionBase):
    name="Get Hosts Status"
    description="Set eg.result with a python dict containing the config and status of all watched hosts. The key of the dict is the host name.\n"
    description+="Each dict entry is a string where values are separated by a coma.\n the values are :\n"
    description+="hostName,hostFriendlyName,pingDelay,eventAlive,eventDead,delayEventAlive,delayEventDead, status,lastPingResult.\n"
    description+="Here is an exemple of a python script you could run jus after this action :\n"
    description+="hosts=eg.result\n"
    description+="for host in hosts:\n"
    description+="    print host + \" : \" + hosts[host]\n"
    description+="    hostData=hosts[host].split(\",\")\n"
    description+="    for idx in range(0,len(hostData)):\n"
    description+="        print hostData[idx]\n"
    def __call__(self):
        res={}
        for hostName in self.plugin.hosts:
            host=self.plugin.hosts[hostName]
            res[hostName]=""
            res[hostName]+=host.name + ","
            res[hostName]+=host.friendlyName + ","
            res[hostName]+=str(host.pingDelay) + ","
            res[hostName]+=host.eventAlive + ","
            res[hostName]+=host.eventDead + ","
            res[hostName]+=str(host.delayEventAlive) + ","
            res[hostName]+=str(host.delayEventDead) + ","
            res[hostName]+=host.GetStatus() + ","
            res[hostName]+=host.GetLastPingResult()
        return res


class Host:
    def __init__(self,name,friendlyName,pingDelay,eventAlive,eventDead,delayEventAlive,delayEventDead,pingString):
        self.pingDelay = pingDelay
        self.name = name
        self.friendlyName = friendlyName
        self.status = "unknown"
        self.lastPingResult = "unknown"
        global prefix

        if eventAlive=="":
            if friendlyName=="":
                self.eventAlive=name+"_IS_ALIVE"
            else:
                self.eventAlive=friendlyName+"_IS_ALIVE"
        else:
            self.eventAlive = eventAlive

        if eventDead=="":
            if friendlyName=="":
                self.eventDead=name+"_IS_DEAD"
            else:
                self.eventDead=friendlyName+"_IS_DEAD"
        else:
            self.eventDead = eventDead

        self.delayEventAlive=delayEventAlive
        self.delayEventDead=delayEventDead
        self.pingString = str(pingString)

        self.pingThread = None
        self.stopPingThreadEvent = Event()
        self.lock = Lock()

    def PingThread(self,stopPingThreadEvent):
        print "Ping Plugin : Thread " + self.name + " is starting ! "
        eventsAlive=0
        eventsDead=0
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        pingCmd = subprocess.Popen(["ping",self.name,"-4","-t","-w",str(self.pingDelay)], stdout=subprocess.PIPE, stderr=None,startupinfo=startupinfo)
        pingCmd.wShowWindow = 0
        while not stopPingThreadEvent.isSet():
            output = pingCmd.stdout.readline()
            #print output
            if output.find(self.pingString)>-1:
            #print "	Thread " + self.name + " is pinging !"
                eventsAlive+=1
                eventsDead=0
                self.lock.acquire()
                try:
                    self.lastPingResult="alive"
                    if eventsAlive>=self.delayEventAlive:
                        if self.status!="alive":
                            self.status="alive"
                            eg.TriggerEvent(prefix=prefix,suffix=self.eventAlive)
                finally:
                    self.lock.release()
            else:
                eventsAlive=0
                eventsDead+=1
                self.lock.acquire()
                try:
                    self.lastPingResult="dead"
                    if eventsDead>=self.delayEventDead:
                        if self.status!="dead":
                            self.status="dead"
                            eg.TriggerEvent(prefix=prefix,suffix=self.eventDead)
                finally:
                    self.lock.release()
        print "Ping Plugin : Thread " + self.name + " is ending ! "
        pingCmd.terminate()
        self.stopPingThreadEvent.clear()
        #print "Thread " + self.name + " has finished his job !"

    def GetStatus(self):
        self.lock.acquire()
        try:
            status =self.status
        finally:
            self.lock.release()
        return status

    def GetLastPingResult(self):
        self.lock.acquire()
        try:
            res=self.lastPingResult
        finally:
            self.lock.release()
        return res


    def GetThreadState(self):
        if self.pingThread.isAlive() and not self.stopPingThreadEvent.isSet():
            return "Thread is running"
        elif self.pingThread.isAlive() and self.stopPingThreadEvent.isSet():
            return "Thread is finishing his job"
        elif (not self.pingThread.isAlive()) and (not self.stopPingThreadEvent.isSet()):
            return "Thread is ready to be started"
        else:
            return "Problem !"

    def StopThread(self):
        self.stopPingThreadEvent.set()

    def StartThread(self):
        if self.stopPingThreadEvent.isSet():
            #print "/!\\ Problem : stopPingThreadEvent Is Set ..."
            self.stopPingThreadEvent.clear()
        self.pingThread = Thread(target=self.PingThread,args=(self.stopPingThreadEvent,))
        self.pingThread.start()

    def Print(self):
        print self.name
        print self.friendlyName
        print self.status
        print self.eventAlive
        print self.eventDead


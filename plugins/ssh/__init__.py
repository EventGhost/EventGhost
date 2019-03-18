# -*- coding: utf-8 -*-
#
# plugins/SSH/__init__.py
#
# This file is a plugin for EventGhost.

import paramiko
from time import sleep
from threading import Event, Thread
import socket
import re

eg.RegisterPlugin(
    name = "SSH",
    author = "Sem;colon",
    version = "1.79",
    kind = "other",
    canMultiLoad = False,
    description = 'A simple SSH client',
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6021",
    guid = '{19E6BDAD-5765-41A5-96B7-69656C1E64D5}',
)

class SSH(eg.PluginClass):
    hosts={}
    instances=[]
    comms=["Log","Event","Don't show"]
    
    def __init__(self):
        self.AddAction(AddHost, "AddHost", "Add Host", "Creates a new SSH connection.")
        self.AddAction(RemoveHost, "RemoveHost", "Remove Host", "Closes an existing SSH connection.")
        self.AddAction(RunCommand, "RunCommand", "Send Command", 'Sends a command through the SSH Connection.<br><br>This function creates an event "Data" if the execution of the command is done.<br><br>Only one command can be executed at the same time on one host. If a command is running, the new command will be enqueued.')
        self.AddAction(SendText, "SendText", "Send Text", "Sends some text through the SSH Connection.<br><br>This function should only be used if the executed command waits for input.")
        		
    def __start__(self):
        for i in range(0,len(self.instances)):
            if self.hosts[self.instances[i]].stopThreadEvent.isSet():
                self.hosts[self.instances[i]].startThread()
        
    def __stop__(self):
        for i in range(0,len(self.instances)):
            self.hosts[self.instances[i]].stopThreadEvent.set()
            self.hosts[self.instances[i]].Disconnect()
            
    def __close__(self):
        for i in range(0,len(self.instances)):
            self.hosts[self.instances[i]].stopThreadEvent.set()
            self.hosts[self.instances[i]].Disconnect()
            
    def removeHost(self, host):
        inst=self.instances.index(host)
        self.hosts[host].stopThreadEvent.set()
        self.hosts[host].Disconnect()
        del self.hosts[host]
        del self.instances[inst]
        return True
        

class Controller():
    
    def __init__(self, ip, port, user, pw, host, comm, autoDisconnect, plugin):
        self.plugin=plugin
        self.plugin.instances.append(host)
        self.plugin.hosts[host]=self
        self.lastCommands=[]
        self.commandQ=[]
        self.addCommand=False
        self.onlyIfChanged=False
        self.responseList={}
        self.commandIsProcessed=False
        self.commandIsInitiated=False
        self.startLine=""
        self.cache=""
        self.ip=ip
        self.port=port
        self.user=user
        self.pw=pw
        self.host=host
        self.comm=comm
        self.autoDisconnect=autoDisconnect
        self.connected=False
        self.checkcounter=0
        self.startThread()
        
    def startThread(self):
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.Receive,
            args=(self.stopThreadEvent, )
        )
        thread.start()
    
    def isAlive(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((host,port))
            sock.close()
            return True
        except:
            return False
    
    def Connect(self, ip, port, user, pw, host):
        if self.connected==False and self.isAlive(ip, port):
            print 'SSH: Host "'+host+'" found on the network, trying to connect to '+ip+':'+str(port)+'...'
            try:
                self.client = paramiko.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client.connect(ip, port=port, username=user, password=pw)
                self.channel = self.client.invoke_shell()
                self.commandIsProcessed=True
                self.connected=True
                self.plugin.TriggerEvent("Connected."+host)
                return True
            except Exception as e:
                self.plugin.TriggerEvent("ConnectionError."+host)
                eg.PrintError(str(e))
                return False
    
    def Disconnect(self):
        if self.connected:
            self.connected=False
            self.channel.shutdown(2)
            self.client.close()
            self.lastCommands=[]
            self.startLine=""
            i=len(self.commandQ)-1
            while i>=0:
                if self.commandQ[i][4]==False:
                    self.commandQ.pop(i)
                i-=1
            self.plugin.TriggerEvent("Disconnected."+self.host)
            self.commandIsProcessed=False
            self.cache=""
            self.commandIsInitiated=False
        
    def Receive(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            if self.connected:
                if self.channel.recv_ready():
                    self.checkcounter=0
                    if self.commandIsProcessed:
                        tempData1=self.channel.recv(2048)
                        data=re.sub("\\x1b\[\d.*?m","",(self.cache+tempData1)).split("\r\n")
                        tempData=re.sub("\\x1b\[\d.*?m","",tempData1.replace("\n",""))
                        tempData=tempData.split("\r")
                        y=len(tempData)-1
                        while y>=0:
                            if len(tempData[y].replace(" ",""))==0:
                                tempData.pop(y)
                            y-=1
                        if self.comm == "Log":
                            for i in tempData:
                                print "SSH: "+self.host+": "+i
                        elif self.comm == "Event":
                            for i in tempData:
                                self.plugin.TriggerEvent("New_line."+self.host,i)
                        if self.startLine=="":
                            for i in data:
                                i=i.strip()
                                if len(i)>0 and i[0]!="#" and (i[-1]=="$" or i[-1]=="#" or i[-1]==">"):
                                    end=i.find(":")
                                    if  end!=-1:
                                        userend=i.find("@")
                                        if userend!=-1:
                                            self.startLine=i[userend:end+1]
                                        else:
                                            self.startLine=i[:end+1]
                                        self.ReceiveOK()
                        else:
                            self.cache+=tempData1
                            if data[-1].find(self.startLine)!=-1:
                                i=len(data)-1
                                while i>=0:
                                    if data[i] in self.lastCommands:
                                        data.pop(i)
                                    if data[i].find("\r")!=-1:
                                        temparr=data[i].split("\r")
                                        y=1
                                        while y < len(temparr):
                                            if temparr[y-1]==temparr[y]:
                                                temparr.pop(y)
                                            elif y>1 and temparr[y-1]=="" and len(temparr[y-2].replace(" ",""))!=0:
                                                temparr.pop(y-1)
                                                temparr.pop(y-2)
                                                y-=1
                                            else:
                                                y+=1
                                        y=len(temparr)-2
                                        while y >= 0:
                                            if len(temparr[y+1].replace(" ",""))==0:
                                                if len(temparr[y])==len(temparr[y+1]) or len(temparr[y])==0:
                                                    temparr.pop(y+1)
                                                    temparr.pop(y)
                                            y-=1
                                        data[i]="".join(temparr)
                                    i-=1
                                if self.onlyIfChanged==False or self.responseList[self.lastCommands[0]]!=data:
                                    self.responseList[self.lastCommands[0]]=data
                                    tempString="Data."+self.host
                                    if self.addCommand:
                                        tempString+="."+self.lastCommands[0]
                                    if self.addSuffix!="":
                                        tempString+="."+self.addSuffix
                                    self.plugin.TriggerEvent(tempString,data)
                                self.ReceiveOK()
                    else:
                        tempData=re.sub("\\x1b\[\d.*?m","",self.channel.recv(2048).replace("\n","")).split("\r")
                        while len(tempData)>0 and tempData[-1]=="":
                            tempData.pop(-1)
                        while len(tempData)>0 and tempData[0]=="":
                            tempData.pop(0)
                        self.plugin.TriggerEvent("UnknownData."+self.host,tempData)
                        self.cache=""      
                elif self.autoDisconnect:
                    self.checkcounter+=1
                    if self.checkcounter>=80:
                        self.checkcounter=0
                        if self.isAlive(self.ip, self.port)==False:
                            print "SSH: Host "+self.host+" is not responding, will disconnect!"
                            self.Disconnect()
                            sleep(3)
            else:
                self.Connect(self.ip, self.port, self.user, self.pw, self.host)
                sleep(3)
            stopThreadEvent.wait(0.1)
    
    def ReceiveOK(self):
        self.cache=""
        if len(self.commandQ)>0:
            self.SendCommand(False)
        else:
            self.commandIsProcessed=False
          
    def SendCommand(self, newEvent):
        command, host, addCommand, onlyIfChanged, keepInQ, addSuffix=self.commandQ[0]
        if self.connected and self.channel.send_ready:
            try:
                self.lastCommands=[command]
                self.addCommand=addCommand
                self.addSuffix=addSuffix
                self.onlyIfChanged=onlyIfChanged
                if command not in self.responseList:
                    self.responseList[command]=[""]
                self.commandQ.pop(0)
                self.commandIsProcessed=True
                self.channel.sendall(command+chr(13))
                return True
            except:
                if keepInQ==False:
                    self.commandQ.pop(0)
                    self.plugin.TriggerEvent("Cannot_send_command."+host,command)
                if self.isAlive(self.ip, self.port)==False:
                    self.Disconnect()
                self.commandIsProcessed=False
                return False
        else:
            if keepInQ==False:
                self.commandQ.pop(0)
                self.plugin.TriggerEvent("Cannot_send_command."+host,command)
            self.commandIsProcessed=False
            return False
    
            
class AddHost(eg.ActionBase):

    class Text:
        tcpBox = "Connection Settings"
        ip = "Hostname/IP:"
        port = "Port:"
        user = "Username:"
        pw = "Password:"
        egBox = "EventGhost Settings"
        host = "Alias in EventGhost (unique!):"
        comm = "Communication behavior:"
        replace = "Replace host if it already exists."
        autoDisconnect = "Automatically disconnect if host becomes inactive."
    
    def __call__(self, ip, port, user, pw, host, comm, replace=False, autoDisconnect=True):
        if host in self.plugin.instances:
            print 'SSH: Host "'+host+'" already exists!'
            if replace:
                print 'SSH: Host "'+host+'" will be replaced...'
                self.plugin.removeHost(host)
            else:
                return False
        Controller(ip, port, user, pw, host, comm, autoDisconnect, self.plugin)
        return True

    def Configure(self, ip="", port=22, user="", pw="", host="", comm="Log", replace=True, autoDisconnect=True):
        text = self.Text
        panel = eg.ConfigPanel()
        wx_ip = panel.TextCtrl(ip)
        wx_port = panel.SpinIntCtrl(port, min=0, max=65535)
        wx_user = panel.TextCtrl(user)
        wx_pw = panel.TextCtrl(pw)
        wx_host = panel.TextCtrl(host)
        wx_comm = wx.Choice(panel, -1, choices=self.plugin.comms)
        wx_comm.SetSelection(self.plugin.comms.index(comm))
        wx_replace = wx.CheckBox(panel, -1, text.replace)
        wx_replace.SetValue(replace)
        wx_autoDisconnect = wx.CheckBox(panel, -1, text.autoDisconnect)
        wx_autoDisconnect.SetValue(autoDisconnect)

        st_ip = panel.StaticText(text.ip)
        st_port = panel.StaticText(text.port)
        st_user = panel.StaticText(text.user)
        st_pw = panel.StaticText(text.pw)
        st_host = panel.StaticText(text.host)
        st_comm = panel.StaticText(text.comm)
        st_replace = panel.StaticText("")
        st_autoDisconnect = panel.StaticText("")
        eg.EqualizeWidths((st_ip, st_port, st_user, st_pw, st_host, st_comm, st_replace, st_autoDisconnect))

        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (st_ip, wx_ip),
            (st_port, wx_port),
            (st_user, wx_user),
            (st_pw, wx_pw),
            (st_autoDisconnect, wx_autoDisconnect),
        )
        egBox = panel.BoxedGroup(
            text.egBox,
            (st_host,wx_host),
            (st_replace,wx_replace),
            (st_comm,wx_comm),
        )

        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(egBox, 1, wx.EXPAND)

        while panel.Affirmed():
            host2 = wx_host.GetValue()
            if host2 == "":
                host2 = "_"
            panel.SetResult(
                wx_ip.GetValue(),
                wx_port.GetValue(),
                wx_user.GetValue(),
                wx_pw.GetValue(),
                host2,
                wx_comm.GetStringSelection(),
                wx_replace.GetValue(),
                wx_autoDisconnect.GetValue(),
            )

        
class RemoveHost(eg.ActionBase):
    
    class text:
        hostName="Host:"
    
    def __call__(self, host):
        if host in self.plugin.instances:
            return self.plugin.removeHost(host)
        else:
            print 'SSH: Host "'+host+'" does not exist!'
            return False

    def Configure(self, host=""):
        panel = eg.ConfigPanel()
        text = self.text
        st_host = panel.StaticText(text.hostName)
        wx_host = wx.Choice(panel, -1, choices=self.plugin.instances)
        if host in self.plugin.instances:
            wx_host.SetSelection(self.plugin.instances.index(host))

        panel.AddLine(st_host,wx_host)

        while panel.Affirmed():
            panel.SetResult(wx_host.GetStringSelection())
            
            
class RunCommand(eg.ActionBase):
    
    class text:
        command = "Command to send:"
        hostName = "Host:"
        addCommand = 'Add executed command as additional suffix to the "Data" event.'
        onlyIfChanged = 'Triggers the "Data" event only if the result is different from the last time this command was executed.'
        keep = 'Do not discard this command if host is not connected.'
        suffix = 'Additional Suffix:'
    
    def __call__(self, command, host, addCommand=False, onlyIfChanged=False, keep=False, addSuffix=""):
        if host in self.plugin.instances:
            thisHost=self.plugin.hosts[host]
            thisHost.commandQ.append([command,host,addCommand,onlyIfChanged,keep,addSuffix])
            if thisHost.commandIsProcessed or thisHost.commandIsInitiated:
                return True
            else:
                thisHost.commandIsInitiated=True
                val=thisHost.SendCommand(True)
                thisHost.commandIsInitiated=False
                return val
        else:
            print 'SSH: Host "'+host+'" does not exist!'
            return False

    def Configure(self, Command="", host="", addCommand=False, onlyIfChanged=False, keep=False, addSuffix=""):
        panel = eg.ConfigPanel()
        text = self.text
        st_command = panel.StaticText(text.command)
        wx_command = panel.TextCtrl(Command, size=(400, -1))
        st_host = panel.StaticText(text.hostName)
        wx_host = wx.Choice(panel, -1, choices=self.plugin.instances)
        wx_addCommand = wx.CheckBox(panel, -1, text.addCommand)
        wx_addCommand.SetValue(addCommand)
        wx_onlyIfChanged = wx.CheckBox(panel, -1, text.onlyIfChanged)
        wx_onlyIfChanged.SetValue(onlyIfChanged)
        wx_keep = wx.CheckBox(panel, -1, text.keep)
        wx_keep.SetValue(keep)
        st_addSuffix = panel.StaticText(text.suffix)
        wx_addSuffix = panel.TextCtrl(addSuffix)
        if host in self.plugin.instances:
            wx_host.SetSelection(self.plugin.instances.index(host))
        eg.EqualizeWidths((st_host, st_command, st_addSuffix))
        
        panel.AddLine(st_host,wx_host)
        panel.AddLine(st_command,wx_command)
        panel.AddLine(wx_addCommand)
        panel.AddLine(wx_onlyIfChanged)
        panel.AddLine(wx_keep)
        panel.AddLine(st_addSuffix,wx_addSuffix)

        while panel.Affirmed():
            panel.SetResult(wx_command.GetValue(),wx_host.GetStringSelection(),wx_addCommand.GetValue(),wx_onlyIfChanged.GetValue(),wx_keep.GetValue(),wx_addSuffix.GetValue())
            
            
class SendText(eg.ActionBase):
    
    class text:
        command = "Text to send:"
        hostName = "Host:"
        addReturn = "Add a return at the end of the text."
    
    def __call__(self, command, host, addReturn=True):
        if host in self.plugin.instances:
            thisHost=self.plugin.hosts[host]
            if thisHost.connected and thisHost.channel.send_ready and thisHost.commandIsProcessed:
                try:
                    thisHost.lastCommands.append(command)
                    if addReturn:
                        thisHost.channel.send(command+chr(13))
                    else:
                        thisHost.channel.send(command)
                    return True
                except:
                    self.plugin.TriggerEvent("Cannot_send_text."+host,command)
                    return False
            else:
                self.plugin.TriggerEvent("Cannot_send_text."+host,command)
                return False
        else:
            print 'SSH: Host "'+host+'" does not exist!'
            return False

    def Configure(self, Command="", host="", addReturn=True):
        panel = eg.ConfigPanel()
        text = self.text
        st_command = panel.StaticText(text.command)
        wx_command = panel.TextCtrl(Command)
        st_host = panel.StaticText(text.hostName)
        wx_host = wx.Choice(panel, -1, choices=self.plugin.instances)
        wx_addReturn = wx.CheckBox(panel, -1, text.addReturn)
        wx_addReturn.SetValue(addReturn)
        if host in self.plugin.instances:
            wx_host.SetSelection(self.plugin.instances.index(host))
        eg.EqualizeWidths((st_host, st_command))

        panel.AddLine(st_host,wx_host)
        panel.AddLine(st_command,wx_command)
        panel.AddLine(wx_addReturn)

        while panel.Affirmed():
            panel.SetResult(wx_command.GetValue(),wx_host.GetStringSelection(),wx_addReturn.GetValue())
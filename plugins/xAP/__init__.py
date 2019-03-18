# -*- coding: utf-8 -*-
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

eg.RegisterPlugin(
    name = "xAP",
    author = "K",
    version = "1.5.5.b",
    canMultiLoad = False,
    kind = "external",
    guid = "{26649308-3137-4C33-A5D2-6F50DAE36A65}",
    description = "Send and receive xAP messages.",
    url = "",
)
    
import sys
import socket
import wx
import threading
from copy import deepcopy as dc
from eg.WinApi.Utils import GetMonitorDimensions
from wx.lib.mixins.listctrl import CheckListCtrlMixin

class PRINT:
    def __init__(self, plugin):
        self.plugin = plugin
     
    def Log(self, direct, logStr, event):
        res = direct+'     '+logStr
        if event is False: print res
        elif event[0] is None: res = None
        elif event in self.plugin.dbgEvt: print res
        return res

    def Notice(self, noticeString):
        eg.PrintNotice(noticeString)

    def Error(self, errorString):
        eg.PrintError(errorString)
        return []


class Text:
    HubModeOff = [u'', u'Server Mode: xAP Server Not Running']
    HubModeHub = [u'xAP-Hub', u'Server Mode: xAP Hub Mode Running: ']
    HubModeApp = [u'xAP-App', u'Server Mode: xAP Application Mode Running: ']
    HubModeClt = [[u'', u', Client Mode: Off'], [u':xAP-Client', u', Client Mode: On']]
    DefaultUID = [["FF", "5AC0", "00"], ["FF.", "5BC0D811", ":0000"]]
    class Config:
        VerBox  = "Version"
        VenBox  = "Vendor Name"
        VerBox  = "xAP Version"
        HbtBox  = "Heart Beat Interval"
        UIDBox  = "Unique Identifier"
        CltBox  = "Client Mode"
        PayBox  = "Payload Data"
        IPAText = "Listening Address: "
        HstText = "Host Information as Prefix: "
        CltText = "xAP Client Mode: "
        VenText = "Vendor Name: "
        VerText = "xAP Version: "
        HbtText = "Interval: "
        IgDbBtn = "Ignore/Debug Events"
        PayText = "Include Payload: "
        DesText = {
                    'ClientMode': ("Client Mode is for triggering an event with payload that was sent specifically\n"
                                    "to the computer running this plugin and no other events will be triggered except\n"
                                    "the ones that have been targeted for this computer.\n"),
                    'Vendor':     ("You can enter up to an 8 character vendor name if you want. or leave it as is\n"
                                    "the mode that the plugin is runing in will be appended as will the host name\n"
                                    "of this computer\n"),
                    'Version':    ("Set to 1.2 if you don't know what version of xAP your devices use. If they use 1.3\n"
                                    "they will be able to talk to EG because of backwards compatability. 1.2 uses a\n"
                                    "identifier (electronic serial number) formatted like FF5AC000 and 1.3 is like\n"
                                    "FF.5AC0E811:0000. Not enough room to explain about it.\n"),
                    'Payload':    ("Selecting this will pass the data received as a python dictionary in the paload. I\n"
                                    "have also written the data to eg.result as well so it can be accessed even if the\n"
                                    "payload is turned off that way you will still be able to access the informtion that\n"
                                    "is incoming without cluttering up the EventGhost Log window\n")}
    class Server:
        SockErr = "xAP: Failed to open socket: "
        HUStart = "xAP: UDP has Started: "
        HUClose = "xAP: UDP has Shutdown"
        HUError = "xAP: Server start error: "
        HBStart = "xAP: HeartBeat has Started"
        HBClose = "xAP: HeartBeat has Shutdown"
        PortLbl = "Port: "
        Restart = "Restarting xAP Server: an external hub was started or shutdown"
    class DataProcess:
        MalData  = "Malformed Data: "
        MalExpt  = "Malformed Data: Exception: "
        PortLbl = "Port: "
        ForwdLs = "New lease: "
        TermnLs = "Terminating lease: "
        RenewLs = "Renewing lease: "
        TmOutLs = "Lease timed out: "
        LngthLs = "Lease Length: "
        ScndsLs = " seconds"
        DataLbl = "Data: "
        UIDLabl = "UID: "
        PreLabl = "Prefix: "
        SufLabl = "Suffix: "
        PayLabl = "Payload: "
        NoData1 = u'**NODATA**'
    class IgnDbgFrame:
        DbgIgnFrm = 'xAP Debug Events/Ignore Events'
        DbgIgnCol = [u'Source', u'Class', u'Type', u'Target']
        NoDataSrt = [u'**NODATA**']
        NoDataLng = [u'********NODATA********']
        NoDataSml = [NoDataSrt*len(DbgIgnCol)]
        NoDataLrg = [NoDataLng*len(DbgIgnCol)]
        DbgIgnLbl = {
                        'Dbg': ["Debug xAP Events", "Select All", "Unselect All"],
                        'Ign': ["Ignore xAP Events", "Select All", "Unselect All"],
                        'Pnl': ["Refresh Tables", "OK", "Cancel"],
                        }
    class sendxAP:
        name = "Send xAP message"
        description = "Sends an xAP message"
        SrcLbl  = "xAP Message Source: " 
        TypLbl  = "xAP Message Type: "
        ClsLbl  = "xAP Message Class: "
        TgtLbl  = "xAP Message Target: "
        MsgLbl  = "xAP Message: "

class File:
    import shutil
    import os

    fileInfo = ['\\xAP.', 'List', '.txt']
    
    def __init__(self, plugin):
        path = self.os.path
        self.filePath = path.join(path.expanduser('~'),'Documents')+'\\EventGhost-xAP'
        try: self.os.mkdir(self.filePath)
        except OSError as exception:
            if exception.errno != 17:
                self.filePath = None

    def Load(self, fInfo):
        Print = eg.PrintError
        path = self.os.path
        
        try: fileName = self.filePath+fInfo.format(*self.fileInfo)
        except: return []
        else:
            try:
                with open(fileName, 'r') as f: return f.readlines()
            except:
                try:
                    file(fileName, 'w').close()
                    return []
                except IOError as err:
                    return Print('xAP File Load Error: '+str(err))


    def Save(self, fInfo, writeString):
        try: fInfo[0] = self.filePath+fInfo[0].format(*self.fileInfo)
        except: return
        if writeString and self.Backup(fInfo[0]):
            with open(*fInfo) as f: f.write(writeString)

    def Backup(self, fName):
        Print = eg.PrintError
        path = self.os.path
        copyfile = self.shutil.copyfile
        fPath = self.filePath

        if path.exists(fName):
            j = 4
            fNP = fName.split('.')
            fNP = ['.'.join(fNP[:len(fNP)-1]+["Backup"+str(j-i)]+fNP[len(fNP)-1:]) for i in range(1, 4)]
            try:
                for i, name in enumerate(fNP):
                    if path.exists(name) and i != 0:
                        copyfile(name, fNP[i-1])
                copyfile(fName, fNP[len(fNP)-1])
                return True
            except IOError as exception:
                return Print('xAP File Backup Error: '+str(exception))
        else:
            try:
                file(fName, 'w').close()
                return True
            except IOError as exception:
                return Print('xAP File Create Error: '+str(exception))

class List:

    def __init__(self, plugin):
        self.File = File(plugin)
        self.plugin = plugin

    def Load(self, fInfo):
        res = self.File.Load(fInfo)
        if res:
            lineNum = 0
            for i, line in enumerate(res):
                if line == '*'*50+'\n': lineNum = i+4
            res = res[lineNum:]
            fileLen = len(res)
            for i in range(fileLen):
                items = res.pop(0).strip()
                if not items: continue
                items = items.split(' '*5)
                itemLen = len(items)
                res += [[]]
                for i in range(itemLen):
                    item = items.pop(0).strip()
                    if item: res[len(res)-1] += [item]
        return dc(res)

    def Save(self, saveInfo, saveList):
        saveList = dc(saveList)
        writeString = ''
        if saveList and saveList != self.Load(saveInfo[0]):
            minSpace = 5
            saveList.insert(0, ['Source', 'Class', 'Type', 'Target'])
            maxLen = [minSpace*2]*len(saveList[0])
            for line in saveList:
                maxLen = [max(maxLen[i], len(item)) for i, item in enumerate(line)]
            saveList.insert(1, ['-'*(i+minSpace) for i in maxLen])
            writeString = '\n'+('*'*50)+'\n\n'
            for items in saveList:
                for i, item in enumerate(items):
                    writeString += item+' '*((maxLen[i]-len(item))+minSpace) \
                                    if item != '-'*(maxLen[i]+minSpace) else item
                writeString += '\n'
            writeString += '\n'
        self.File.Save(saveInfo, writeString)

class Server:

    text = Text

    def __init__(self, plugin):
        self.plugin = plugin
        self.HBSock = False
        self.HBEvent = threading.Event()
        self.UDPEvent = threading.Event()
        self.leaseData = []
        Print = PRINT(self.plugin)
        self.PN = Print.Notice
        self.PE = Print.Error
        self.Log = Print.Log
        self.port = 0
        self.hubmode = self.text.HubModeOff
        
    def Start(self, *args):
        try:
            self.UDPSock = None
            threading.Thread(target=self.RunListener, args=args).start()
            return True
        except:
            self.PE(self.text.ServerStartErr+str(sys.exc_info()))
            return False

    def RunListener(self, port, sendaddr, vendor, client, pretype, heartbeat, paydata):
        text = self.text
        txt = self.text.Server
        plg = self.plugin
        self.client = client
        hubname = ''
        recvaddr = sendaddr
        client = self.text.HubModeClt[client]
        clientname = ''

        while self.UDPEvent.isSet(): pass

        try:
            UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDPSock.settimeout(1)
            hubmode = dc(text.HubModeHub)
            notice = dc(txt.HUStart)
        except:
            UDPSock = False
            hubmode = dc(text.HubModeOff)
            notice = dc(txt.SockErr)+str(sys.exc_info())

        while notice == txt.HUStart:
            try:
                UDPSock.bind((recvaddr, port))
                notice += hubmode[1]+txt.PortLbl+str(port)
            except:
                if port == 3639:
                    hubmode = dc(text.HubModeApp)
                    port = 50000
                    recvaddr = '127.0.0.1'
                elif port < 51000:
                    port += 1
                else:
                    hubmode = dc(text.HubModeOff)
                    notice = dc(txt.HUError)
                    UDPSock = False
            else:
                self.port    = port
                hubname      = vendor+'.'+hubmode[0]+'.'+socket.gethostname() if hubmode[0] else ''
                clientname   = hubname+client[0] if client[0] else ''
                notice += client[1]
                hubmode[1] = notice

        plg.hubname    = dc(hubname)
        self.hubmode   = dc(hubmode)
        self.hubname   = dc(hubname)
        self.sendIP    = sendaddr
        self.recvIP    = recvaddr
        self.hostname  = socket.gethostname()
        self.heartbeat = heartbeat
        plg.clientname = dc(clientname)
        self.PN(notice)
        if self.hubmode[0]:
            threading.Thread(target=self.RunHeartBeat).start()

        self.UDPSock = UDPSock
        while self.hubmode[0]:
            try: data, inaddr = UDPSock.recvfrom(1500)
            except socket.timeout: continue
            if not self.UDPEvent.isSet():
                args = [data, inaddr[0], recvaddr, sendaddr, pretype, hubname, clientname, paydata]
                threading.Thread(target=self.IncomingData, args=args).start()
            else:
                self.HBEvent.set()
                while self.HBSock: pass
                UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.hubmode = dc(self.text.HubModeOff)

        self.PN(txt.HUClose)

        try: UDPSock.close()
        except: pass
        try: self.appModeTimer.cancel()
        except: pass
        while self.leaseData:
            try: self.leaseData.pop(0).cancel()
            except: pass

        self.UDPEvent.clear()
        self.UDPSock = False

    def GetServerState(self):
        return self.hubmode

    def RestartHub(self, *args):
        self.PN(self.text.Server.Restart)
        self.Stop()
        self.Start(*args)

    def RunHeartBeat(self):
        plg = self.plugin
        text = self.text.Server

        if not self.UDPEvent.isSet():
            self.HBSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.HBSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
            self.PN(text.HBStart)
            msg = plg.Message(u'xap-hbeat', u'xap-hbeat.alive', self.hubname, interval=self.heartbeat, port=str(self.port))

            while not self.HBEvent.isSet():
                self.Send(msg)
                self.HBEvent.wait(60)

        self.PN(text.HBClose)

        try: self.HBSock.close()
        except: pass

        self.HBEvent.clear()
        self.HBSock = False

    def Send(self, msg, address=None):
        address = (msg, address) if address else (msg, (self.sendIP, 3639))
        if self.HBSock: self.HBSock.sendto(*address)

    def IncomingData(self, data, inaddr, recvaddr, sendaddr, pretype, hubname, clientname, paydata):
        if not data: return
        plg = self.plugin
        text = self.text.DataProcess
        payload = {}

        splitData = data.split("\n")
        for i, line in enumerate(splitData):
            try:
                if line == "{":
                    payload['Type'] = splitData[i-1]
                elif "=" in list(line):
                    line = line.split("=")
                    key = line.pop(0)
                    key = key.upper() if key in ['uid', 'Uid', 'UID', 'v', 'pid', 'Pid', 'PID'] else key.title()
                    line = line[0] if len(line) == 1 else '='.join(line)
                    if key == 'UID': line = line.upper()
                    payload[key] = line
            except:
                self.Log('>', text.MalData+data, False)
                self.Log('>', text.MalExpt+str(sys.exc_info()), False)

        UID = dc(payload['UID'])
        Type = dc(payload['Type'])
        Class = dc(payload['Class'])
        Source = dc(payload['Source'])

        try: Target = dc(payload['Target'])
        except: Target = text.NoData1

        newEvent = dc(plg.CheckEvent([dc(Source), dc(Class), dc(Type), dc(Target)]))
        self.Log(">", text.DataLbl+data, newEvent)
        
        if Type == 'xap-hbeat':
            try: Interval = dc(payload['Interval'])
            except: Interval = '60'

            try: Port = dc(payload['Port'])
            except: Port = None

            args = [3639, sendaddr, plg.vendor, self.client, pretype, self.heartbeat, paydata]
            if recvaddr == inaddr:
                if self.hubmode[0] == 'xAP-Hub' and Source != hubname:
                    lease = text.TermnLs if payload['Class'].find('alive') == -1 else text.RenewLs
                    try:
                        idx = self.leaseData.index([UID, Port])
                        newLease = self.leaseData.pop(idx)
                        self.leaseData.pop(idx).cancel()
                    except:
                        if payload['Class'].find('alive') > -1:
                            newLease = [UID, Port]
                            lease = text.ForwdLs

                    lease += text.UIDLabl+UID+", "+text.PortLbl+Port

                    if Port != '3639':
                        if lease.find(text.TermnLs) == -1:
                            lease += ", "+text.LngthLs+str(int(Interval)*2)+text.ScndsLs
                            tmr = threading.Timer(int(Interval)*2, self.RemoveHost, args=[newLease])
                            self.leaseData += [newLease, tmr]
                            tmr.start()
                        if newEvent not in plg.ignEvt:
                            self.PN(lease)

                    self.leaseData = [[False, False], False] \
                            if not self.leaseData else self.leaseData[2:] \
                            if self.leaseData[0][0] is False else self.leaseData
                
                    if Port == '3639' and Source.find('ersp.SlimServer.') > -1:
                        self.PN('xAP: You have to change the xAP plugin installed in the Logitech Media Server to "External Hub"')
                        return
                    elif Port == '3639':            
                        self.RestartHub(*args)

                elif self.hubmode[0] != 'xAP-Hub' and Source == hubname:
                    try: self.appModeTimer.cancel()
                    except: pass
                    self.appModeTimer = threading.Timer(int(Interval)*2, self.RestartHub, args=args)
                    self.appModeTimer.start()

        if self.hubmode[0] == 'xAP-Hub':
            for host in self.leaseData:
                try: self.Send(data, ("127.0.0.1", int(host[1])))
                except: pass

        presuf = [Source]
        presuf += ['xAP'+Class[3:].title() if Type == 'xap-hbeat' else Class]
        prefix = presuf[0] if pretype else presuf[1]
        suffix = presuf[1] if pretype else presuf[0]

        self.Log(">", text.PreLabl+prefix, newEvent)
        self.Log(">", text.SufLabl+suffix, newEvent)
        self.Log(">", text.PayLabl+str(payload), newEvent)

        if newEvent not in plg.ignEvt:
            eg.result = dc(payload)
            eg.event.payload = dc(payload)
            if paydata:
                eg.TriggerEvent(prefix=prefix, suffix=suffix, payload=dc(payload))
            else:
                eg.TriggerEvent(prefix=prefix, suffix=suffix)

        t = Target.split(':')
        if t[0] == hubname:
            if clientname:
                if 'Prefix' not in payload or payload['Prefix'] == 'None':
                    return self.PN('xAP Client Mode, There is no "Prefix=" in xAP Message, For: '+Target+', From: '+Source)
                kwargs = dict(prefix=dc(payload['Prefix']))
                if 'Suffix' in payload and payload['Suffix'] != 'None':
                    kwargs['suffix'] = dc(payload['Suffix'])
                if clientname.split(':')[1] != t[1]:
                    if 'suffix' in kwargs:
                        kwargs['suffix'] += '.'+t[1]
                    else:
                        kwargs['suffix'] = t[1]
                if 'Payload' in payload and payload['Payload'] != 'None':
                    try:
                        if payload['Payload'][:4] == "{eg.":
                            kwargs['payload'] = dc(eval(payload['Payload'][1:-1]))
                        else:
                            kwargs['payload'] = dc(eval(payload['Payload']))
                    except: pass
                eg.TriggerEvent(**kwargs)
            else:
                self.PN("ClientMode is not currently enabled, there are incoming events, For: "+Target+", From: "+Source)

    def RemoveHost(self, lease):
        text = self.text.DataProcess
        if lease in self.leaseData:
            idx = self.leaseData.index(lease)
            self.leaseData.pop(idx)
            self.leaseData.pop(idx)
            self.Log(text.TmOutLs+text.UIDLabl+lease[0]+", "+text.PortLbl+lease[1], False)

    def Stop(self):
        if self.port:
            self.UDPEvent.set()
            msg = self.plugin.Message(u'xap-hbeat', u'xap-hbeat.stopped', self.hubname, interval=self.heartbeat, port=str(self.port))
            if self.sendIP != self.recvIP: self.Send(msg, (self.recvIP, self.port))
            self.Send(msg, (self.sendIP, 3639))

class xAP(eg.PluginBase):

    text = Text

    def __init__(self):
        self.port = 3639
        self.AddAction(sendxAP)
        
        Print = PRINT(self)
        self.PN = Print.Notice
        self.PE = Print.Error
        self.Log = Print.Log

        self.Server = Server(self)
        load = List(self).Load

        self.eventList = load('{0}Event{1}{2}')
        self.dbgEvt = load('{0}Debug{1}{2}')
        self.ignEvt = load('{0}Ignore{1}{2}')

        self.hubname = ''
        self.clientname = ''
        self.vendor = ''
        self.hostname = ''
        self.heartbeat = ''
        self.hubUID = ''

    def __start__(
                self,
                hostname="",
                pretype=True,
                UID=["5AC0", "5BC0D811"],
                vendor="EvntGhst",
                version=0,
                heartbeat="60",
                client=True,
                paydata=False
                ):

        self.UID = UID
        self.version = '1.3' if version else '1.2'
        self.vendor = vendor
        self.hostname = hostname
        self.heartbeat = heartbeat
        self.hubUID = ''.join(self.GenUID(version, UID))

        if hostname in self.GetAddresses():
            self.Server.Start(self.port, hostname, vendor, client,  pretype, heartbeat, paydata)

        while self.Server.UDPSock is None: pass

        File(self).Save(
                ['{0}ConfigSettings{2}', 'w'],
                '\n'.join([line for line in self.GenConfig()])
                )

    def __stop__(self):
        self.Server.Stop()
        save = List(self).Save
        for params in self.GenLists(): save(*params)

    def __close__(self):
        self.Server.Stop()
        save = List(self).Save
        for params in self.GenLists():
            save(*params)

    def GenLists(self):
        for fName, fList in [['Event', self.eventList], ['Debug', self.dbgEvt], ['Ignore', self.ignEvt]]:
            yield (['{0}'+fName+'{1}{2}', 'a'], fList)

    def GenConfig(self):
        return [
                "UID v1.2: "+self.UID[0],
                "UID v1.3: "+self.UID[1],
                "Listning On: "+self.hostname,
                "Heart Beat: "+self.heartbeat,
                "Version: "+self.version,
                "Vendor Name: "+self.vendor,
                "Hub Name: "+self.hubname,
                "Client Name: "+self.clientname
                ]

    def GenUID(self, v, UID):
        if v is None:
            v = 0 if len(UID) == 4 else 1
            UID = ['',UID] if v else [UID,'']
        B = 'FF.' if v else 'FF'
        N = UID[v] 
        E = ':000' if v else '0'
        return [B, N, E]
            
    def DbgIgnEvent(self, dItems, iItems):
        if dItems is not None: self.dbgEvt = dc(dItems)
        if iItems is not None: self.ignEvt = dc(iItems)
        return dc(self.eventList)

    def GetAddresses(self):
        addresses = socket.gethostbyname_ex(socket.gethostname())[2]
        addresses.sort(key=lambda a: [int(b) for b in a.split('.', 4)])
        return addresses

    def CheckEvent(self, event):
        if not self.eventList or event not in self.eventList:
            self.eventList += [event]
        return event

    def Message(self, header, cls, source, target=None, interval=None, port=None, typ=None, msg=None):

        uid = dc(self.hubUID)
        uid += '1' if ':' in list(source) else '0'
        ver = '13' if ':' in list(uid) else '12'

        Msg = header+"\n"
        Msg += "{\n"
        Msg += "V="+ver+"\n"
        Msg += "Hop=1\n"
        Msg += "UID="+uid+"\n"
        Msg += "Class="+cls+"\n"
        Msg += "Source="+source+"\n"
        Msg += "Target="+target+"\n" if target else ""
        Msg += "Interval="+interval+"\n" if interval else ""
        Msg += "Port="+port+"\n" if port else ""
        Msg += "}\n"
        Msg += typ+"\n" if typ else ""
        Msg += "{\n" if typ else ""
        Msg += msg+"\n" if msg else ""
        Msg += "}\n" if typ else ""

        Source = source
        Class = cls
        Type = typ if typ else header
        Target = target if target else self.text.DataProcess.NoData1
        newEvent = self.CheckEvent([Source, Class, Type, Target])
        self.Log('<', Msg, newEvent)

        return Msg

    def Configure(
                self,
                hostname="",
                pretype=True,
                UID=["5AC0", "5BC0D811"],
                vendor="EvntGhst",
                version=0,
                heartbeat="60",
                client=True,
                paydata=False
                ):

        text = self.text.Config
        panel = eg.ConfigPanel(self)
        buttonRow = panel.dialog.buttonRow

        def bind(typ, instance, handler, *args, **kwargs):
            instance.Bind(typ, lambda event: handler(event, *args, **kwargs), instance)

        colSizer = wx.BoxSizer(wx.HORIZONTAL)

        uidSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        col1Sizer = wx.BoxSizer(wx.VERTICAL)
        col2Sizer = wx.BoxSizer(wx.VERTICAL)

        addrs = self.GetAddresses()
        try: addr = addrs.index(hostname)
        except ValueError: addr = 0
 
        st1 = panel.StaticText(self.Server.GetServerState()[1])
        st2 = wx.StaticLine(panel, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        st3 = panel.StaticText(text.DesText['ClientMode'])
        st4 = panel.CheckBox(client)
        st5 = panel.Choice(addr, addrs)
        st6 = panel.CheckBox(pretype)
        st7 = panel.TextCtrl(' ', style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        st8 = panel.TextCtrl(' ', style=wx.TE_RICH2)
        st9 = panel.TextCtrl(' ', style=wx.TE_READONLY)
        st10 = panel.StaticText(text.DesText['Vendor'])
        st11 = panel.TextCtrl(vendor)
        st12 = panel.StaticText(text.DesText['Version'])
        st13 = panel.Choice(version, ['1.2', '1.3'])
        st14 = panel.SpinIntCtrl(int(heartbeat))
        st15 = panel.StaticText(text.DesText['Payload'])
        st16 = panel.CheckBox(paydata)
        st17 = wx.Button(panel, -1, text.IgDbBtn)

        def getPanelResults():
            return [addrs[st5.GetValue()], st6.GetValue(), UID, st11.GetValue(),
                        st13.GetValue(), str(st14.GetValue()), st4.GetValue(), st16.GetValue()]

        def addBoldRedText(ctrl, txt):
            font = st10.GetFont()
            font.SetWeight(wx.BOLD)
            ctrl.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 0, 0), font=font))
            ctrl.AppendText(txt)
            font.SetWeight(wx.NORMAL)
            ctrl.SetDefaultStyle(wx.TextAttr(wx.Colour(0, 0, 0), font=font))
        
        def checkHex():
            hex_digits = list("0123456789ABCDEF")
            update = st8.GetValue().upper()
            saved = update
            st8.ChangeValue("")
            for char in update:
                if char not in hex_digits:
                    addBoldRedText(st8, char)
                    saved = False
                else:
                    st8.AppendText(char)
            return st13.GetValue(), saved

        def loadUID(ver):
            ID = self.GenUID(ver, UID)
            ID[2] += '0'
            st8.SetMaxLength(len(ID[1]))
            st7.ChangeValue(ID[0])
            st7.SetBackgroundColour((170, 170, 170))
            st8.ChangeValue(ID[1])
            st9.SetBackgroundColour((170, 170, 170))
            st9.ChangeValue(ID[2])

        def onChoice(evt):
            v, update = checkHex()
            if update and len(update) == len(UID[not v]):
                UID[not v] = update
                loadUID(v)
            elif update:
                st8.ChangeValue("")
                addBoldRedText(st8, update)
                st13.SetSelection(not v)
            elif not update:
                st13.SetSelection(not v)
            evt.Skip()

        def onIgnDbg(evt):
            if not self.Server: self.__start__(*getPanelResults())
            dlg = DbgIgnFrame(parent=panel, plugin=self)
            dlg.Centre()
            wx.CallAfter(dlg.showDialog, bind)
            evt.Skip()

        def onUID(evt, func=None):
            v, update = checkHex()
            if update and len(update) == len(UID[v]):
                UID[v] = update
                if func: func(evt)
                else: evt.Skip()
            elif update and func:
                st8.ChangeValue("")
                addBoldRedText(st8, update)
        
        def onUpdateUID(evt, func=None):
            wx.CallAfter(onUID, evt, func)

        loadUID(version)

        uidSizer.Add(st7, 0, wx.ALIGN_RIGHT)
        uidSizer.Add(st8, 0, wx.ALIGN_CENTER)
        uidSizer.Add(st9, 0, wx.ALIGN_LEFT)

        btnSizer.Add(st17, 0, wx.ALIGN_CENTER)

        col1Sizer.Add(panel.BoxedGroup('', (text.IPAText, st5), (text.HstText, st6)), 0, wx.EXPAND|wx.ALL, 5)
        col1Sizer.Add(panel.BoxedGroup(text.CltBox, st3, (text.CltText, st4)), 0, wx.EXPAND|wx.ALL, 5)
        col1Sizer.Add(panel.BoxedGroup(text.UIDBox, uidSizer), 0, wx.EXPAND|wx.ALL, 5)
        col1Sizer.Add(panel.BoxedGroup(text.HbtBox, (text.HbtText, st14)), 0, wx.EXPAND|wx.ALL, 5)
        col1Sizer.Add(panel.BoxedGroup('', btnSizer), 0, wx.EXPAND|wx.ALL, 5)

        col2Sizer.Add(panel.BoxedGroup(text.VenBox, st10, (text.VenText, st11)), 0, wx.EXPAND|wx.ALL, 5)
        col2Sizer.Add(panel.BoxedGroup(text.VerBox, st12, (text.VerText, st13)), 0, wx.EXPAND|wx.ALL, 5)
        col2Sizer.Add(panel.BoxedGroup(text.PayBox, st15, (text.PayText, st16)), 0, wx.EXPAND|wx.ALL, 5)

        colSizer.Add(col1Sizer, 0, wx.ALIGN_LEFT)
        colSizer.Add(col2Sizer, 0, wx.ALIGN_RIGHT)

        panel.sizer.Add(st1, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.LEFT|wx.BOTTOM|wx.TOP, 5)
        panel.sizer.Add(st2, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.LEFT|wx.BOTTOM, 5)
        panel.sizer.Add(colSizer, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 5)

        st8.Bind(wx.EVT_CHAR, onUpdateUID)
        st13.Bind(wx.EVT_CHOICE, onChoice)
        st17.Bind(wx.EVT_BUTTON, onIgnDbg)

        bind(wx.EVT_BUTTON, buttonRow.applyButton, onUpdateUID, func=buttonRow.OnApply)
        bind(wx.EVT_BUTTON, buttonRow.okButton, onUpdateUID, func=buttonRow.OnOK)

        while panel.Affirmed():
            st1.SetLabel(self.Server.GetServerState()[1])
            panel.SetResult(*getPanelResults())

class sendxAP(eg.ActionClass):

    text = Text

    def __call__(self, source, typ, cls, target, msg):

        if self.plugin.Server.UDPSock:
            msg = self.plugin.Message('xap-header', cls, source, target=target, typ=typ, msg=msg)
            self.plugin.Server.Send(msg)
        
    def Configure(self, source="", typ="", cls="", target="", msg=""):

        text = self.text.sendxAP
        panel = eg.ConfigPanel(self)
        plg = self.plugin
        sourceLst = [plg.hubname, plg.clientname]
        try: source = sourceLst.index(source)
        except: source = 0

        st1 = panel.Choice(source, sourceLst)
        st2 = panel.TextCtrl(typ, size=(300, 20))
        st3 = panel.TextCtrl(cls, size=(300, 20))
        st4 = panel.TextCtrl(target, size=(300, 20))
        st5 = panel.TextCtrl(msg, style=wx.TE_MULTILINE, size=(300, 200))

        box1 = panel.BoxedGroup(text.SrcLbl, st1)
        box2 = panel.BoxedGroup(text.TypLbl, st2)
        box3 = panel.BoxedGroup(text.ClsLbl, st3)
        box4 = panel.BoxedGroup(text.TgtLbl, st4)
        box5 = panel.BoxedGroup(text.MsgLbl, st5)

        panel.sizer.AddMany([(box1, 0, wx.EXPAND), (box2, 0, wx.EXPAND), (box3, 0, wx.EXPAND), (box4, 0, wx.EXPAND), (box5, 0, wx.EXPAND)])
        while panel.Affirmed(): panel.SetResult(sourceLst[st1.GetValue()], st2.GetValue(), st3.GetValue(), st4.GetValue(), st5.GetValue())


class Table(wx.ListCtrl, CheckListCtrlMixin):

    text = Text

    def __init__(self, panel, parent, style):

        text = self.text.IgnDbgFrame
        header = dc(text.DbgIgnCol)
        nC = len(header)

        wx.ListCtrl.__init__(self, parent, -1, style=style)
        CheckListCtrlMixin.__init__(self)

        while header:
            self.InsertColumn(nC-len(header), header.pop(0), format=wx.LIST_FORMAT_LEFT)

        def build(testTable, lines):
            cW = []
            self.insertItems(dc(testTable))
            for i in range(nC):
                self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
                cW += [self.GetColumnWidth(i)]
            tW = wx.SYS_VSCROLL_X+self.GetWindowBorderSize()[0]+sum(cW)
            rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
            rect = 2+rect[1]+lines*rect[3]
            self.DeleteAllItems()
            return cW, tW, rect

        monW = 0
        monH = 0
        for mon in GetMonitorDimensions():
            monW = min(monW, mon[2])
            monH = min(monH, mon[3])

        cW, tW, rect = build(text.NoDataLrg, 10)
        rect = min(monH, rect*2+400)
        tW = min(monW, tW*2+150)

        if monH == rect or monW == tW:
            line = 5 if monH == rect else 10
            tmpText = text.NoDataSml if monW == tW else text.NoDataLrg
            cW, tW, rect = build(tmpText, line)

        parent.panelMin = (tW+75, rect+175)
        self.SetMinSize((tW, rect))
        self.cW = cW
        self.tW = tW
        self.nC = nC
        self.panel = panel

        self.OnCheckItem = panel.onCheck
        self.Bind(wx.EVT_SIZE, self.onSize)

    def insertItems(self, newTable, checked=False):
        oldTable = self.getItems(checkcol=True)
        newTable = dc(newTable)
        oldTable = dc(oldTable)
        self.DeleteAllItems()
        newTable = [item+[checked] for item in newTable \
                        if not oldTable \
                            or (item+[checked] not in oldTable \
                                and item+[not checked] not in oldTable)]
        newTable += oldTable
        newTable.sort()

        for items in newTable:
            pos = False
            check = items.pop(len(items)-1)
            for j, item in enumerate(items):
                if pos is False: pos = self.InsertItem(j, item)
                else: self.SetItem(pos, j, item)
            self.CheckItem(pos, check)

    def checkItems(self, evt, check):
        num = self.GetItemCount()
        for row in range(num):
            self.CheckItem(row, check)
        evt.Skip()
        #wx.CallAfter(self.panel.onRfsh)

    def getItems(self, checkcol=False):
        data = []
        num = self.GetItemCount()
        for row in range(num):
            if checkcol or self.IsChecked(row):
                data += [[dc(self.GetItem(row, i).GetText()) for i in range(self.nC)]]
            if checkcol:
                data[row] += [dc(self.IsChecked(row))]
        return data

    def onSize(self, evt):
        for i in range(self.nC):
            self.SetColumnWidth(i, (self.GetSize().width - self.tW)/self.nC + self.cW[i])
        evt.Skip()

class DbgIgnFrame(wx.Frame):

    text = Text

    def __init__(self, parent, plugin):

        title = self.text.IgnDbgFrame.DbgIgnFrm
        style = wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL| wx.RESIZE_BORDER
        wx.Frame.__init__(self, parent, -1, style=style, name=title)

        parent.Enable(False)
        parent.dialog.buttonRow.cancelButton.Enable(False)
        parent.EnableButtons(False)
        self.plugin = plugin
        self.parent = parent
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.panelMin = (100, 100)
        self.SetTitle(title)

    def showDialog(self, bind):
        text = self.text.IgnDbgFrame
        plg = self.plugin
        panel = wx.Panel(self, -1)
        self.savedDbg = dc(plg.dbgEvt)
        self.savedIgn = dc(plg.ignEvt)
        self.update = plg.DbgIgnEvent
        
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        tableSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(panelSizer)

        lbls = dc(text.DbgIgnLbl)
        rfsh = wx.Button(panel, -1, lbls['Pnl'][0])
        ok = wx.Button(panel, wx.ID_OK, lbls['Pnl'][1])
        cncl = wx.Button(panel, wx.ID_CANCEL, lbls['Pnl'][2])

        self.updateItems = True
        tblSizer, self.dbgTable, self.dbgInsert, self.dbgGet, dbgAddAll, dbgDelAll = self.tblSizer(panel, bind, *lbls['Dbg'])
        tableSizer.Add(tblSizer, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 10)
        tblSizer, self.ignTable, self.ignInsert, self.ignGet, ignAddAll, ignDelAll = self.tblSizer(panel, bind, *lbls['Ign'])
        tableSizer.Add(tblSizer, 0, wx.EXPAND|wx.ALIGN_RIGHT|wx.ALL, 10)
        self.dbgInsert(dc(self.savedDbg), checked=True)
        self.ignInsert(dc(self.savedIgn), checked=True)
        self.updateItems = False

        panelBtnSizer.Add(rfsh)
        panelBtnSizer.Add(ok)
        panelBtnSizer.Add(cncl)
        panelSizer.Add(tableSizer, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 10)
        panelSizer.Add(panelBtnSizer, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 10)

        panelSizer.Add((1,6))
        panelSizer.Fit(self)
        self.SetMinSize(self.panelMin)
        self.SetSize((-1, -1))
        panelSizer.Layout()
        self.Raise()
        self.MakeModal(True)
        self.Centre()

        wx.CallAfter(self.Show, True)
        wx.CallAfter(self.onRfsh)

        rfsh.Bind(wx.EVT_BUTTON, self.onRfsh)
        ok.Bind(wx.EVT_BUTTON, self.onOK)
        cncl.Bind(wx.EVT_BUTTON, self.onCncl)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

    def tblSizer(self, panel, bind, tableLbl, btn1Lbl, btn2Lbl):
        tmpBoxLbl = wx.StaticBox(panel, -1, tableLbl)
        tmpBox = wx.StaticBoxSizer(tmpBoxLbl, wx.VERTICAL)
        tmpBtnSizer = wx.BoxSizer(wx.HORIZONTAL)

        line = wx.StaticLine(panel, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        btn1Lbl = wx.Button(panel, -1, btn1Lbl)
        btn2Lbl = wx.Button(panel, -1, btn2Lbl)
        style = wx.LC_REPORT|wx.VSCROLL|wx.HSCROLL|wx.LC_HRULES|wx.LC_VRULES|wx.SUNKEN_BORDER
        table = Table(self, panel, style)

        tmpBtnSizer.Add(btn1Lbl, 0, wx.EXPAND|wx.ALIGN_CENTER)
        tmpBtnSizer.Add(btn2Lbl, 0, wx.EXPAND|wx.ALIGN_CENTER)
        tmpBox.Add(table, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 10)
        tmpBox.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER)
        tmpBox.Add(tmpBtnSizer, 0, wx.EXPAND|wx.ALIGN_RIGHT|wx.ALL, 10)

        bind(wx.EVT_BUTTON, btn1Lbl, table.checkItems, check=True)
        bind(wx.EVT_BUTTON, btn2Lbl, table.checkItems, check=False)

        return tmpBox, table, table.insertItems, table.getItems, btn1Lbl, btn2Lbl

    def onCheck(self, index, check):
        self.update(self.dbgGet(), self.ignGet())

    def onRfsh(self, *args):
        if len(args) == 2 and self.updateItems: return
        self.updateItems = True
        nItems = dc(self.update(self.dbgGet(), self.ignGet()))
        self.dbgInsert(nItems)
        self.ignInsert(nItems)
        self.updateItems = False
        try: args[0].Skip()
        except: pass

    def onOK(self, evt):
        self.savedDbg = self.dbgGet()
        self.savedIgn = self.ignGet()
        wx.CallAfter(self.onClose)

    def onCncl(self, evt):
        wx.CallAfter(self.onClose)

    def onClose(self, evt=None):
        self.update(dc(self.savedDbg), dc(self.savedIgn))
        self.MakeModal(False)
        self.parent.Enable(True)
        self.parent.dialog.buttonRow.cancelButton.Enable(True)
        self.parent.EnableButtons(True)
        self.GetParent().GetParent().Raise()
        wx.CallAfter(self.Destroy)

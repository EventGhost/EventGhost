# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2014-2020 Chase Whitten <shocktherapysb10@gmail.com>
#
# No Code here on out within this file may be used accept with EventGhost.
# Permission by myself (Chase Whitten) must be granted by me to use this code
# or part of this code in any other program.
#
######################################## Register ############################################
eg.RegisterPlugin(
    name = "Sonos",
    guid='{8733E10E-C2C8-43B7-B1A6-B9CBFEFA195F}',
    author = "Chase Whitten (Techoguy)",
    version = "0.9.2 beta",
    kind = "program",
    canMultiLoad = False,
    description = "This plugin allows you to control your SONOS zone players. This works with grouped zones or stereo pairs. This plugin will search your network for Zone Players during startup, and if any SONOS ZP is added or removed from the network the plugin will automatically update itself. Each ZP is unique based on the MAC address. This means even if the name of a ZP is changed it won't affect your actions. If you have to replace a ZP, then all actions that use that ZP will have to be updated. Many more comands will be added soon.",
    createMacrosOnAdd = True
    #createMacrosOnAdd = False    
)
###################################### Import ###############################################
import eg
from xml.dom.minidom import parse, parseString
import httplib, urllib
import wx.lib
#from socket import *
import time
import asyncore, socket
from xml.dom.minidom import parse, parseString
import os
import linecache # for PrintException()
import sys # for PrintException()
if os.name != "nt":
    import fcntl
    import struct
#for debugging and knowing which functions called another
import inspect

###################################### Globals ############################################### 
globalZPList = {} #dict to store ZP objects.
globalServiceList = {} #dict to store service/subscription objects
globalDebug = 0
globalRestartScheduler = None

############# Manually add IP address below ##############
# this plugin is designed to support PCs with only one active network card
# So to guarantee the right IP address is selected when you have multiple network cards
# enter it below.
# Note that this PC should have a static address if an address is entered below. 
# To allow dynamic ip address in which the plugin gets the IP address automatically, 
# leave it blank ("")
localip = ""
##########################################################

'''Known models:
S1    = Sonos PLAY:1
S3    = Sonos PLAY:3
S5    = Sonos PLAY:5
S9    = Sonos PLAYBAR
Sub   = Sonos SUB
ZP120 = Sonos CONNECT:AMP
ZP90  = Sonos CONNECT
'''

#list of ZPs that support Line In
LINEINMODELS = [
'ZP90', 'ZP120', 'S5'
]

#list of ZPs that support TV inputs 
TVINMODELS = [
'S9'
]

#weather conditions
CONDITIONCODES = {
'0':'tornado',
'1':'tropical storm',
'2':'hurricane',
'3':'severe thunderstorms',
'4':'thunderstorms',
'5':'mixed rain and snow',
'6':'mixed rain and sleet',
'7':'mixed snow and sleet',
'8':'freezing drizzle',
'9':'drizzle',
'10':'freezing rain',
'11':'showers',
'12':'showers',
'13':'snow flurries',
'14':'light snow showers',
'15':'blowing snow',
'16':'snow',
'17':'hail',
'18':'sleet',
'19':'dust',
'20':'foggy',
'21':'haze',
'22':'smoky',
'23':'blustery',
'24':'windy',
'25':'cold',
'26':'cloudy',
'27':'mostly cloudy at night',
'28':'mostly cloudy during the day',
'29':'partly cloudy at night',
'30':'partly cloudy during the day',
'31':'clear at night',
'32':'sunny',
'33':'fair at night',
'34':'fair day',
'35':'mixed rain and hail',
'36':'hot',
'37':'isolated thunderstorms',
'38':'scattered thunderstorms',
'39':'scattered thunderstorms',
'40':'scattered showers',
'41':'heavy snow',
'42':'scattered snow showers',
'43':'heavy snow',
'44':'partly cloudy',
'45':'thundershowers',
'46':'snow showers',
'47':'isolated thundershowers',
'3200':'not available'
}
###################################### Functions #############################################

### example of calling the speech plugin: eg.plugins.Speech.TextToSpeech(u'Microsoft Hazel Desktop - English (Great Britain)', 1, u'Today is a beutiful day. the temperature is 87 degrees outside at {TIME} ', 0, 100)

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    #filename = f.f_code.co_filename
    #linecache.checkcache(filename)
    #line = linecache.getline(filename, lineno, f.f_globals)
    #print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    print 'EXCEPTION AT LINE: %s = %s' % (lineno, exc_obj)
    trigger = 'EXCEPTION AT LINE: '+str(lineno)+" = "+str(exc_obj)
    eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
    

    
def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                            ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


def HtmlSplit(data=""):
    header = {}
    header['body'] = ""
    headerstring = data.split("\r\n\r\n")[0]
    try:
        header['body'] = data.split("\r\n\r\n")[1]
    except:
        pass
    headerlist = headerstring.split("\r\n")
    try:
        header['status-type'] = headerlist[0].split(" ",2)[0]
        header['status-code'] = headerlist[0].split(" ",2)[1]
        header['status'] = headerlist[0].split(" ",2)[2]
        headerlist = headerlist[1:]
    except:
        header['status-type'] = "Unknown"
        header['status-code'] = "NA"
        header['status'] = "Response Error, Status Code not found (HtmlSplit)"
        trigger = "Response Error, Status Code not found (HtmlSplit)"
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
    for s in headerlist:
        variable = s.split(":",1)[0]
        try:
            value = s.split(":",1)[1].strip() #remove white space, there is usually a space after :
        except:
            value = ""
        header[variable] = value
    return header  
  
class AsyncRequesting(asyncore.dispatcher):    
    
    def __init__(self, HOSTzp, PORTzp, data, callback):
        self.HOSTzp = HOSTzp
        self.PORTzp = PORTzp
        self.data = data
        self.contentLength = 0
        self.connectionClose = ''
        self.callback = callback
        self.portused = 0
        self.buffer = ""
        self.start_connection()
    
    def RestartSonosAsyncore(self):
        if globalDebug >= 2:
            print "====== Restarting Asyncore Now ====================="
        eg.RestartAsyncore()
        
    def start_connection(self):
        global globalRestartScheduler
        self.connectionMade = "NO"
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        # it appears that if you call eg.RestartAsyncore() to close together, it causes all 
        # kinds of problems with the asyncore and sockets. To fix this, eg.RestartAsyncore() is
        # only called once 0.1 seconds has passed without any other new sockets created. 
        try: 
            self.renewCallBack = eg.scheduler.CancelTask(globalRestartScheduler)
        except:
            pass
        globalRestartScheduler = eg.scheduler.AddTask(.3, self.RestartSonosAsyncore)
        #eg.RestartAsyncore()
        try:
            self.connect((self.HOSTzp, self.PORTzp))
            self.portused = self.getsockname()[1]
        except socket.error, e:
            print "Connection to %s on port %s failed: %s" % (self.HOSTzp, self.PORTzp, e)
            trigger = "Connection to "+str(self.HOSTzp)+" on port "+str(self.PORTzp)+" failed: "+str(e)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
        self.buffer = self.data
        
    def handle_connect(self):
        if globalDebug >= 2:
            print "%s handle_connect" % self.portused
        self.connectionMade = "CONNECTED"
        pass

    def handle_close(self):
        if globalDebug >= 2:
            print str(self.portused) + " -- CLOSED handle_close, State: %s" % self.connectionMade
        if self.connectionMade == "CONNECTED": #connection made but then closed, so retry.
            self.close() #close current socket, 
            #if globalDebug >= 1:
            print "%s socket closed before reading, RETRYING connection" % self.portused
            self.start_connection() #retry sending.
        elif self.connectionMade == "READ":
            if globalDebug >= 1:
                print "%s -- handle_close state:, %s" % (self.portused,self.connectionMade)
            self.close()
        else: #everything else and "NO"
            if globalDebug >= 1:
                print "No response from %s:%s" % (self.HOSTzp, self.PORTzp)
            self.close()
            data = "No Response from %s:%s" % (self.HOSTzp, self.PORTzp)
            response = {'body':"",'ERROR':data}
            self.callback(response)

    def chunk_decode(self, data):
        tempString = "".join(data.split('\r\n')[1::2])
        tempString = tempString.replace("\n","")
        try:
            tempString = tempString.replace("\t","        ")
        except:
            pass
        return tempString
        
    def handle_read(self):
        if globalDebug >= 2:
            print "%s handle_read" % self.portused
        self.connectionMade = "READ"
        data = self.recv(1024)
        if globalDebug >= 2:
            print "%s-Data:\r\n%s------End Of Data------" % (self.portused, data)        
        try:
            self.response #if it doesn't exist, it's the first read
            if data != '':
                self.response['body'] = self.response['body'] + data
                #if self.contentLength <= len(self.response['body']):
                #    if self.connectionClose == 'close':
                #        if globalDebug >= 1:
                #            print "%s length met 2+ socket closing" % self.portused
                #        self.close()
                #    self.callback(self.response)
                if self.transferEncoding == "":    
                    if self.contentLength <= len(self.response['body']):
                        if self.connectionClose == 'close':
                            if globalDebug >= 2:
                                print "%s length met 2+ socket closing" % self.portused
                            self.close()
                        self.callback(self.response)
                else:#handle chunk encoding
                    if self.response['body'][-4:]=="\r\n\r\n":
                        if self.connectionClose == 'close':
                            if globalDebug >= 2:
                                print "%s chunk 2+ socket closing" % self.portused
                            self.close()
                        self.response['body'] = self.chunk_decode(self.response['body'])
                        self.callback(self.response)
            else: # data empty before content length reached
               print "%s Response ERROR: Connection closed before reaching content length or end" % self.portused
               print "%s Current-Length:%s  SB: %s \n%s" % (self.portused,len(self.response['body']), self.contentLength, self.response)
               self.callback(self.response)
        except AttributeError: #if first read
            self.response = HtmlSplit(data)
            if data != '':
                '''need to look for Transfer-Encoding: chunked first, and 
                create a new function that will read all data and decode it'''
                try:
                    self.transferEncoding = self.response['Transfer-Encoding']
                except:
                    self.transferEncoding = ""
                try:
                    self.contentLength = int(self.response['CONTENT-LENGTH'])
                except:
                    self.contentLength = 0
                try:
                    self.connectionClose = self.response['Connection']
                except:
                    self.connectionClose = ''
                if self.transferEncoding == "":    
                    if self.contentLength <= len(self.response['body']):
                        if self.connectionClose == 'close':
                            if globalDebug >= 2:
                                print "%s length met 1 socket closing" % self.portused
                            self.close()
                        self.callback(self.response)
                else:#handle chunk encoding
                    if self.response['body'][-4:]=="\r\n\r\n":
                        if self.connectionClose == 'close':
                            if globalDebug >= 2:
                                print "%s chunk 1 socket closing" % self.portused
                            self.close()
                        self.response['body'] = self.chunk_decode(self.response['body'])    
                        self.callback(self.response)
            else:
                if globalDebug >= 1:
                    print "%s ---- Response empty ----- " % self.portused
                self.callback(self.response)
                '''might need to have "except" here to handle all other exceptions for the sockets errors. '''
               
    def writable(self):
        try:
            if globalDebug >= 99:
                print "%s writable len:%s" % (self.portused,len(self.buffer))
            #this is actually called sometimes before the next lines of self.connect((self.HOSTzp, self.PORTzp))
            # which means portused and buffer might not be assigned yet. 
            return (len(self.buffer) > 0)
        except:
            print "%s writable no buffer" % self.portused
            return False

    def handle_write(self):
        if globalDebug >= 2:
            print "%s handle_write" % self.portused
        try:
            sent = self.send(self.buffer)
        except:
            sent = self.send(self.buffer.encode("utf-8"))
        '''might need another try/except here to handle the send if not available right now'''
        self.buffer = self.buffer[sent:]

    def handle_expt(self):
        errorText = "handle_expt : %s:%s" % (self.HOSTzp, self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
        try:
            self.close()
        except:
            pass
        trigger = "ERROR, handle_expt: "+str(self.HOSTzp)+":"+str(self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
        raise Exception("ERROR, handle_expt: %s:%s" % (self.HOSTzp, self.PORTzp))

    def handle_error(self):
        errorText = "handle_error : %s:%s" % (self.HOSTzp, self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
        try:
            self.close()
        except:
            pass
        PrintException()
        trigger = "ERROR, handle_error: "+str(self.HOSTzp)+":"+str(self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
        raise Exception("ERROR, handle_error: %s:%s" % (self.HOSTzp, self.PORTzp))
        

    def handle_connect_expt(self,expt):
        errorText = "connection error: %s \r\n..... %s:%s" % (expt,self.HOSTzp, self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
        try:
            self.close()
        except:
            pass
        trigger = "ERROR, handle_connect_expt: "+str(self.HOSTzp)+":"+str(self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
        raise Exception("ERROR, handle_connect_expt: %s:%s" % (self.HOSTzp, self.PORTzp))


class Service():

    def __init__(self, zp, url, EventCallBack, eventport):
        self.zp = zp
        self.url = url
        self.EventCallBack = EventCallBack
        self.eventport = eventport
        self.subsTimeout = 3600
        self.Subscribe()

    def ServiceErrorHandler(self, data):
        if "ERROR" in data.keys():
            if data['ERROR'].find("No Response") >= 0:
                self.UnsubResponse(data)
                del globalZPList[self.zp.uuid] #delete zp from list
                #trigger eg event....
                if globalDebug >= 1:
                    print "\n\ndeleted ZP from List: %s" % self.zp.uuid
                trigger = "%s.%s" % ("DELETED", self.zp.uuid)
                eg.TriggerEvent(trigger, prefix='SONOS', payload=self.zp.ip)
                trigger = "%s-%s" % (self.zp.ip, self.zp.uuid)
                eg.TriggerEvent("ZonePlayerDeleted", prefix='SONOS', payload=trigger)
                if globalDebug >= 1:
                    print "\n\n"
                if self.url.find("ZoneGroupTopology")>0: #if true, subscribe to a different ZP.
                    try:
                        uuid = globalZPList.keys()[0] #select random ZP to get grouptopology from
                        tempservice = Service(globalZPList[uuid], "/ZoneGroupTopology/Event",               ZoneGroupTopologyEvent)             
                    except:#if there are no more ZPs, through error
                        trigger = "ERROR: Can't connect to SONOS Zone Players"
                        eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
                        raise Exception(trigger)
            else: #unhandled error
                trigger = data['ERROR']
                eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
                raise Exception(data['ERROR'])
        return data 
    
    def RenewResponse(self, data):
        #might not need. 
        #store timeout 
        #schedule, renew function call
        #remember to store this so it can be cancelled later. 
        if globalDebug >= 1:
            print "renew Response received..."
        pass
    
    def Renew(self):
        if globalDebug >= 1:
            print "sending renew request...."
        port = 1400
        data = "SUBSCRIBE " + self.url + " HTTP/1.1\r\nSID: " + self.SID + "\r\nTIMEOUT: Second-"+str(self.subsTimeout)+"\r\nHOST: "+self.zp.ip+":"+str(port)+"\r\nContent-Length: 0\r\n\r\n"
        #self.renrequest = AsyncRequesting(self.zp.ip, port, data, self.RenewResponse)
        self.subrequest = AsyncRequesting(self.zp.ip, port, data, self.SubResponse)
        #restart loop to include the new socket object
        # this is needed because this is created after the first call to RestartAsyncore
        #eg.RestartAsyncore() #removed
        if globalDebug >= 1:
            print "%s requesting renew: %s - %s" % (self.subrequest.portused, globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
        #eg.RestartAsyncore() 
    
    def UnsubResponse(self, data):
        # Unsubscribe response
        # check to make sure 200 OK is recieved 
        # trigger eg event....
        #HTTP/1.1 200 OK
        #Server: Linux UPnP/1.0 Sonos/24.0-71060 (ZP120)
        #Connection: close
        global globalServiceList
        global globalZPList
        if globalDebug >= 2:
            print "%s Unsubscribed response %s - %s" % (self.unsubrequest.portused, globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
        del globalServiceList[self.SID]
        globalZPList[self.zp.uuid].services[self.url.split("/")[-2]] = ""
        if globalDebug >= 2:
            print "UnsubResponse Data: %s" % data
        try:
            self.unsubrequest.close()
        except Exception, e:
            print " Service Unsubscribe Response Error: %s" % e
            trigger = "Service Unsubscribe Response Error: "+str(e)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
            PrintException()
        
    def Unsubscribe(self):
        #cancel the scheduled task for the renew
        #send cancel request
        if globalDebug >= 2:
            print "sending unsubscribe request to %s" % (self.zp.ip)
        try:
            eg.scheduler.CancelTask(self.renewCallBack) # cancel renew callback
        except Exception, e:
            if globalDebug >= 2:
                print "can't Cancel Task renewCallBack in Unsubscribed %s" % str(e)
            pass
        try:
            self.renrequest.close()
        except Exception, e:
            pass
        try:
            self.subrequest.close()
        except Exception, e:
            pass
        try:
            self.unsubrequest.close()
        except Exception, e:
            pass
        port = 1400
        data = "UNSUBSCRIBE " + self.url + " HTTP/1.1\r\nUSER-AGENT: Linux UPnP/1.0 Sonos/24.0-69180m (WDCR:Microsoft Windows NT 6.2.9200.0)\r\nHOST: "+self.zp.ip+":"+str(port)+"\r\nSID: " + self.SID + "\r\n\r\n"
        if globalDebug >= 2:
            print "sending unsubscribe request: %s - %s" % (globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
        self.unsubrequest = AsyncRequesting(self.zp.ip, port, data, self.UnsubResponse)      
    
    def SubResponse(self, data):
        global globalServiceList
        global globalZPList
        #print "subscribe response: %s - %s" % (globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
        try:
            response = self.ServiceErrorHandler(data)
            try:
                eg.scheduler.CancelTask(self.renewCallBack)#restart if needed.
            except:
                pass
            self.subsTimeout = int(response['TIMEOUT'].split("-")[1]) #ex: TIMEOUT: Seconds-3200
            if globalDebug >= 2:
                print response['SID']
            self.SID = response['SID']
            globalServiceList[self.SID] = self # store service object in global dict
            # store SID info in ZP object
            globalZPList[self.zp.uuid].services[self.url.split("/")[-2]] = self.SID  
            if globalZPList[self.zp.uuid].name == "":
                globalZPList[self.zp.uuid].name = self.zp.ip
            if globalDebug >= 2:
                print "Subscribed to %s on %s" % (self.url.split("/")[-2],globalZPList[self.zp.uuid].name)
            if globalDebug >= 2:
                print "%s subscribed response %s - %s" % (self.subrequest.portused, globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
            self.renewCallBack = eg.scheduler.AddTask(self.subsTimeout/2, self.Renew)
        except Exception, e:
            print " Service Subscribe Response Error: %s" % e
            trigger = "Service Subscribe Response Error:  "+str(e)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
            PrintException()
        
    def Subscribe(self):
        global globalZPList
        port = 1400
        data = "SUBSCRIBE " + self.url + " HTTP/1.1\r\nNT: upnp:event\r\nTIMEOUT: Second-"+str(self.subsTimeout)+"\r\nHOST: "+self.zp.ip+":"+str(port)+"\r\nCALLBACK: <http://" + localip + ":" + str(self.eventport) + "/events>\r\nContent-Length: 0\r\n\r\n"
        self.subrequest = AsyncRequesting(self.zp.ip, port, data, self.SubResponse)
        if globalZPList[self.zp.uuid].name == "":
            globalZPList[self.zp.uuid].name = self.zp.ip
        if globalDebug >= 2:
            print "%s sending subscribe request: %s - %s" % (self.subrequest.portused, globalZPList[self.zp.uuid].name, self.url.split("/")[-2])
    
    def Event(self, data):
        #define how the event response is handled, unique for each service
        self.EventCallBack(self.zp.uuid, data)


def RenderingControlEvent(uuid, data):
    global globalZPList
    try:
        #print "AVTransportEvent received from %s" % globalZPList[uuid].name
        xml = parseString(data)
        xmlLastChange = xml.getElementsByTagName('LastChange')[0].firstChild.nodeValue
        xml = parseString(xmlLastChange.encode('utf-8'))    
        if globalDebug >= 2:
            print xml.toxml()
        try: 
            globalZPList[uuid].volume
        except:
            globalZPList[uuid].volume = "-"
        #try:
        if True:
            #loop through all volume nodes to find Master node
            for volume in xml.getElementsByTagName('Volume'):
                if volume.attributes['channel'].value=="Master": #if master channel, save current volume
                    vol = volume.attributes['val'].value
                    if globalZPList[uuid].volume != vol: #if volume has changed, trigger event and save.
                        trigger = "%s.%s" % (uuid, "Volume")
                        vol = "vol-%s %s" % (vol, globalZPList[uuid].name)
                        eg.TriggerEvent(trigger, prefix='SONOS', payload=vol)
                        globalZPList[uuid].volume = volume.attributes['val'].value
        #except:
        #    pass
        try: 
            globalZPList[uuid].mute
        except:
            globalZPList[uuid].mute = "-"
        try:
            #loop through all mute nodes to find Master node
            for mute in xml.getElementsByTagName('Mute'):
                if mute.attributes['channel'].value=="Master": #if master channel, save current mute
                    vol = mute.attributes['val'].value
                    if globalZPList[uuid].mute != vol: #if mute has changed, trigger event and save.
                        trigger = "%s.%s" % (uuid, "Mute")
                        vol = "mute-%s %s" % (vol, globalZPList[uuid].name)
                        eg.TriggerEvent(trigger, prefix='SONOS', payload=vol)
                        globalZPList[uuid].mute = mute.attributes['val'].value
        except:
            pass
        try:
            globalZPList[uuid].outputFixed = xml.getElementsByTagName('OutputFixed').attributes['val'].value
        except:
            pass
        try:
            globalZPList[uuid].headphoneConnected = xml.getElementsByTagName('HeadphoneConnected').attributes['val'].value
        except:
            pass
    except Exception, e:
        print "RenderingControlEvent XML error: %s" % e
        trigger = "RenderingControlEvent XML error: "+str(e)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
        

        
def UpdateTransportStates(uuid, transportstate):
    #updated all Zone Players within a group.
    for key in globalZPList:
        if not globalZPList[key].invisible:
            if globalZPList[key].coordinator == uuid:
                globalZPList[key].TransportState(transportstate)        
        
'''
Need to clean this up and have it match the getmediainfo and getpositioninfo
need to create event for when stream source changes
need to create event when track/metadata is updated
  
'''        
def AVTransportEvent(uuid, data):
    global globalZPList
    try:
        #print "AVTransportEvent received from %s" % globalZPList[uuid].name
        xml = parseString(data)
        xmlLastChange = xml.getElementsByTagName('LastChange')[0].firstChild.nodeValue
        xml = parseString(xmlLastChange.encode('utf-8'))    
        if globalDebug >= 2:
            print xml.toxml()
        try:
            transportstate = xml.getElementsByTagName("TransportState")[0].attributes['val'].value
            #check to see if avTransportURI exists, if it doesn't update transportstate (only occurs when first starting)
            if globalDebug >= 1:
                print "%s Received ZP Transport State: %s" % (globalZPList[uuid].name,transportstate)
        except:
            pass
            
        try:
            globalZPList[uuid].avTransportURI
        except:
            globalZPList[uuid].avTransportURI = ""
            try: #sleeptimer triggers this event with no transportstate info
                UpdateTransportStates(uuid, transportstate)
            except:
                pass
            
        try:
            newAVTransportURI = xml.getElementsByTagName("AVTransportURI")[0].attributes['val'].value   
            globalZPList[uuid].avTransportURI = newAVTransportURI
        except Exception, e: 
            #if AVTransportURI is present, this means the stream is updating so transportstate 'STOPPED' should be ignored.
            try:
                UpdateTransportStates(uuid, transportstate)
            except:
                pass
        try:
            globalZPList[uuid].currentPlayMode = xml.getElementsByTagName("CurrentPlayMode")[0].attributes['val'].value
            if globalDebug >= 1:
                print "%s currentPlayMode: %s" % (globalZPList[uuid].name, globalZPList[uuid].currentPlayMode)
        except: 
            pass
        try:
            globalZPList[uuid].playbackStorageMedium = xml.getElementsByTagName("PlaybackStorageMedium")[0].attributes['val'].value
            if globalDebug >= 1:
                print "%s playbackStorageMedium: %s" % (globalZPList[uuid].name, globalZPList[uuid].playbackStorageMedium)
        except: 
            pass
        
        #AVTransportURIMetaData (streaming station info)
        try:
            avtransportURIMetaData = xml.getElementsByTagName("AVTransportURIMetaData")[0].attributes['val'].value
            if avtransportURIMetaData == "":
                if globalDebug >= 1:
                    print "%s avtransportURIMetaData: <empty>" % globalZPList[uuid].name
            else:
                tempxml = parseString(avtransportURIMetaData)
                #print tempxml.toxml()
                title = tempxml.getElementsByTagName("dc:title")[0].firstChild.nodeValue 
                if globalDebug >= 1:
                    print "%s Stream Title: %s" % (globalZPList[uuid].name, title)
        except Exception, e:
            if globalDebug >= 2:
                print "failed %s" % str(e)
            
        #CurrentTrackMetaData information (sub xml)
        try:
            currenttrackmetadata = xml.getElementsByTagName("CurrentTrackMetaData")[0].attributes['val'].value
            tempxml = parseString(currenttrackmetadata.encode('utf-8'))
            tempxml = parseString(currenttrackmetadata.encode('utf-8'))
            #print tempxml.toxml()
            albumartlink = tempxml.getElementsByTagName("upnp:albumArtURI")[0].firstChild.nodeValue 
            #print "http://" + globalZPList[uuid].ip + ":1400" + albumartlink
            #to get high resolution pics: 
            #http://www.albumartexchange.com/covers.php?sort=7&q=Scary+Monsters+and+Nice&fltr=2&bgc=&page=&sng=1
            #this returns: html, which has a <a href="/gallery/images/public/..." taht has the picture. 
            #if it can't find anything it response with "There are no images to display."  
        except Exception, e:
            if globalDebug >= 2:
                print "failed %s" % str(e)
            pass
        try:
            title = tempxml.getElementsByTagName("dc:title")[0].firstChild.nodeValue
            if globalDebug >= 1:
                print "Track: " + title
        except:
            pass
        try:
            artist = tempxml.getElementsByTagName("dc:creator")[0].firstChild.nodeValue
            if globalDebug >= 1:
                print "Artist: " + artist
        except:
            pass
        try:
            album = tempxml.getElementsByTagName("upnp:album")[0].firstChild.nodeValue
            if globalDebug >= 1:
                print "Album: " + album
            #high resolution artwork search based on alum name:
            album = album.replace(" ","+")
            #print "http://www.albumartexchange.com/covers.php?sort=7&q=" + album + "&fltr=2&bgc=&page=&sng=1"
        except:
            pass
    except Exception, e:
        print "AVTransportEvent XML error: %s" % e
        trigger = "AVTransportEvent XML error: "+str(e)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
        
'''
need to add an event when group topology changes
how to handle name/ip changes vs actual grouping changes?

need to look at zonegrouptopology for ZPs that are added and removed.
currently the plugin knows when they are removed when the event renewal times out due
to no response from the removed ZP. Adding a new ZP should work below but it seems when
a ZP is disconnected this isn't happening. As example, ZP was removed, commands
said that the device had been rmoved as expected but when it was re-added the device
was not re-added. 
Also, if a device can be seen to be removed from grouptopology then it'll work faster. 
The problem here to look out ofr is that during group changes sometimes the 
grouptopology doesn't have all the ZPs listed. 
'''        
def ZoneGroupTopologyEvent(uuid, data):
    global globalZPList
    try:
        #print data
        xml = parseString(data)
        #find ZoneGroupState, ignore any other event
        #if "ZoneGroupState" in xml.childNodes
        try:
            xmlstring = xml.getElementsByTagName('ZoneGroupState')[0].firstChild.nodeValue
        except:
            if globalDebug >= 1:
                print "ZoneGroupTopologyEvent: Property is not ZoneGroupState, ignoring..."
            return
        #print xmlstring
        xml = parseString(xmlstring.encode('utf-8'))
        grouplist = xml.getElementsByTagName('ZoneGroup')
        #print grouplist
        #loop through group info and update zpList
        zpInfo = {} #temp.
        subscribeList = []
        unsubscribeList = []
        for zg in grouplist:
            #print zg.attributes['Coordinator'].value
            coordinator = zg.attributes['Coordinator'].value
            #to find ZPs that are in the Satellites configurations with PlayBar:
            try:
                zplist = zg.getElementsByTagName('Satellite')
                for zp in zplist:
                    attrlist = dict(zp.attributes.items())
                    uuid = attrlist['UUID']
                    #add ZP to dict if new
                    ip = attrlist['Location'].split("/")[2].split(":")[0]
                    xmllocation = attrlist['Location']
                    if uuid not in globalZPList:
                        globalZPList[uuid] = ZonePlayer(uuid, ip, xmllocation)
                    #globalZPList[uuid].uuid = uuid
                    globalZPList[uuid].ip = ip
                    globalZPList[uuid].name = attrlist['ZoneName']
                    globalZPList[uuid].isZoneBridge = '0'        
                    globalZPList[uuid].coordinator = coordinator
                    globalZPList[uuid].invisible = 1
                    if globalDebug >= 1:
                        print '{0: <27}'.format(uuid) + '{0: <17}'.format(ip) + attrlist['ZoneName']
            except:
                pass
            zplist = zg.getElementsByTagName('ZoneGroupMember')
            for zp in zplist:
                attrlist = dict(zp.attributes.items())
                uuid = attrlist['UUID']
                #add ZP to dict if new
                ip = attrlist['Location'].split("/")[2].split(":")[0]
                xmllocation = attrlist['Location']
                if uuid not in globalZPList:
                    globalZPList[uuid] = ZonePlayer(uuid, ip, xmllocation)
                #globalZPList[uuid].uuid = uuid
                globalZPList[uuid].ip = ip
                globalZPList[uuid].name = attrlist['ZoneName']
                try:
                    globalZPList[uuid].isZoneBridge = attrlist['IsZoneBridge'] 
                except:
                    globalZPList[uuid].isZoneBridge = '0' 
                #check to see if the coordinator is changing,
                #if coordinator changing, update transportstate for ZP to state. 
                if globalZPList[uuid].coordinator != coordinator:
                    if globalDebug >= 1:
                            print "%s coordinator changed to %s" % (globalZPList[uuid].name,globalZPList[coordinator].name)
                    if coordinator == uuid:
                        globalZPList[uuid].TransportState("PAUSED_PLAYBACK")
                    elif globalZPList[coordinator].transportState == "Playing":
                        globalZPList[uuid].TransportState("PLAYING")
                    else:
                        globalZPList[uuid].TransportState("PAUSED_PLAYBACK")
                    
                globalZPList[uuid].coordinator = coordinator
                #subscribe to AVTransport (all that are coordinators)
                if coordinator == uuid: #if true, ZP is coordinator 
                    stringflagco = " :coordinator -%s-" % globalZPList[uuid].services["AVTransport"]
                    if globalZPList[uuid].services["AVTransport"] == "": # no SID
                        if globalDebug >= 2:
                            print "    Subscribing to %s" % globalZPList[uuid].name
                        subscribeList.append(uuid)
                    else:
                        pass
                        if globalDebug >= 2:
                            print "    AVTransport already subscribed to %s" % globalZPList[uuid].name
                else:
                    stringflagco = " -%s-" % globalZPList[uuid].services["AVTransport"]
                    if not globalZPList[uuid].services["AVTransport"] == "": #SID present
                        unsubscribeList.append(uuid)
                        if globalDebug >= 2:
                            print "    Unsubscribing to %s" % globalZPList[uuid].name
                        #globalServiceList[globalZPList[uuid].services["AVTransport"]].Unsubscribe()
                    else:
                        if globalDebug >= 2:
                            print "    AVTransport already unsubscribed to %s" % globalZPList[uuid].name
                if "Invisible" in attrlist:
                    globalZPList[uuid].invisible = 1
                    if globalDebug >= 1:
                        print '{0: <27}'.format(uuid) + '{0: <17}'.format(ip) + attrlist['ZoneName'] + " (Invisible)" + stringflagco
                else:
                    globalZPList[uuid].invisible = 0
                    if globalDebug >= 1:
                        print '{0: <27}'.format(uuid) + '{0: <17}'.format(ip) + attrlist['ZoneName'] + stringflagco
        for zp in subscribeList:
            if not globalZPList[zp].isZoneBridge == '1':
                if globalDebug >= 1:
                    print "Subscribing to AVTransportEvent on %s" % globalZPList[zp].name
                #globalZPList[zp].services["AVTransport"] = "testing"
                tempservice = Service(globalZPList[zp], "/MediaRenderer/AVTransport/Event", AVTransportEvent, serverPort)
        for zp in unsubscribeList:
            if globalDebug >= 1:
                print "Unsubscribing to AVTransportEvent on%s" % globalZPList[zp].name
            #globalZPList[zp].services["AVTransport"] = ""
            globalServiceList[globalZPList[zp].services["AVTransport"]].Unsubscribe()
        #subscribe to RenderingControl (Volume) only if it's not invisible 
        for zp, zpobject in globalZPList.iteritems():
            if zpobject.invisible:
                #if subscribed, unsubscribe
                if not zpobject.services["RenderingControl"] == "":
                    globalServiceList[zpobject.services["RenderingControl"]].Unsubscribe()
            else:#if unsubscriebed, subscribe
                if zpobject.services["RenderingControl"] == "":
                    tempservice = Service(globalZPList[zp], "/MediaRenderer/RenderingControl/Event", RenderingControlEvent, serverPort)
    except Exception, e:
        print "ZoneGroupTopologyEvent XML error: %s" % e
        trigger = "ZoneGroupTopologyEvent XML error: "+str(e)+"\n\n"+data
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
        if globalDebug >= 1:
            print "----- ZoneGroupTopology Data Response -------\n%s\n\n" % data


class EventChannel(asyncore.dispatcher):
    contentlength = 0
    eventdata = ""
    def handle_write(self):
        pass
    
    def handle_close(self):
        pass
        
    def handle_read(self):
        if globalDebug >= 2:
            print "--- Event Handle_Read ---"
        data = self.recv(8192)
        try:
            if self.contentlength == 0:
                self.eventdata = HtmlSplit(data)
                self.contentlength = int(self.eventdata['CONTENT-LENGTH'])
                if self.eventdata['NT'] != 'upnp:event': #check to make sure it's an event
                    trigger = "ERROR, expected to receive event"
                    eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
                    raise Exception("ERROR, expected to receive event")
            else:
                self.eventdata['body'] = self.eventdata['body'] + data
            
            if self.contentlength <= len(self.eventdata['body']):
                self.send('HTTP/1.1 200 OK\r\nContent-Length: 0')
                self.close()
                if globalDebug >= 2:
                    print self.eventdata['body']
                SID = self.eventdata['SID']
                if SID in globalServiceList:
                    servicename = globalServiceList[SID].url.split("/")[-2]
                    zpevent = globalZPList[globalServiceList[SID].zp.uuid].name
                    if globalDebug >= 1:
                        print "--- EVENT Received --- %s from %s" % (servicename, zpevent)
                    globalServiceList[SID].Event(self.eventdata['body'])
                self.contentlength = 0
                self.eventdata = ""
        except Exception, e:
            self.close()
            errorText = "event receive error: %s - %s" % (Exception, e)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
            print errorText
            #self.send('HTTP/1.1 500 Internal Server ERROR\r\nContent-Length: 0')
            
    def handle_expt(self):
        errorText = "EventChannel handle_expt : %s:%s" % (self.HOSTzp, self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
        try:
            self.close()
        except:
            pass
        raise Exception("ERROR, EventChannel handle_expt: %s:%s" % (self.HOSTzp, self.PORTzp))

    def handle_error(self):
        errorText = "EventChannel handle_error : %s:%s" % (self.HOSTzp, self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
        try:
            self.close()
        except:
            pass
        PrintException()
        raise Exception("ERROR, EventChannel handle_error: %s:%s" % (self.HOSTzp, self.PORTzp))

    def handle_connect_expt(self,expt):
        errorText = "EventChannel connection error: %s \r\n..... %s:%s" % (expt,self.HOSTzp, self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
        try:
            self.close()
        except:
            pass
        raise Exception("ERROR, EventChannel handle_connect_expt: %s:%s" % (self.HOSTzp, self.PORTzp))

class EventServer(asyncore.dispatcher):

    def __init__(self, port=0):#leaving the port assigned to 0 will allow the OS to pick an available port. 
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        ''' other plugins place the RestartAsyncore here but it doesn't help me '''
        #eg.RestartAsyncore() #this used instead of asyncore.loop for EG.
        self.bind(("", self.port))
        self.port = self.getsockname()[1] #gets assigned port number
        self.listen(5)
        print "SONOS Event Server listening on port", self.port

    def handle_accept(self):
        channel, addr = self.accept()
        if globalDebug >= 2:
            print " connected to channel: " + str(channel)
        if globalDebug >= 2:
            print " connected to addr: " + str(addr)
        EventChannel(channel)

    def handle_expt(self):
        errorText = "EventServer handle_expt : %s:%s" % (self.HOSTzp, self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
        try:
            self.close()
        except:
            pass
        raise Exception("ERROR, EventServer handle_expt: %s:%s" % (self.HOSTzp, self.PORTzp))

    def handle_error(self):
        errorText = "ERROR, EventServer handle_error : %s:%s" % (self.HOSTzp, self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
        try:
            self.close()
        except:
            pass
        PrintException()
        raise Exception("ERROR, EventServer handle_error: %s:%s" % (self.HOSTzp, self.PORTzp))

    def handle_connect_expt(self,expt):
        errorText = "EventServer connection error: %s \r\n..... %s:%s" % (expt,self.HOSTzp, self.PORTzp)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
        try:
            self.close()
        except:
            pass
        raise Exception("ERROR, EventServer handle_connect_expt: %s:%s" % (self.HOSTzp, self.PORTzp))

        
class ZonePlayer():
    household = ""
    COMMANDPORT = 1400
    def __init__(self, uuid, ip, xmllocation):
        if globalDebug >= 2:
            print "New ZonePlayer Added: %s : %s" % (uuid, ip)
        self.uuid = uuid
        self.ip = ip
        self.invisible = 1 #added to fix playbar topology xml issue
        self.xmllocation = xmllocation
        self.name = uuid
        self.coordinator = uuid
        self.transportState = ""
        self.model = "unknown"
        self.swversion = "unknown" 
        self.hwversion = "unknown"
        self.favPlayList = {}
        self.sendCmdState = "ready" #STATES: ready, busy
        self.storeMediaInfo = {'mediaRestore':False, 'volRestore':False}
        #services:
        services = {
                    'ZoneGroupTopology':"", #only one ZP 
                    'ContentDirectory':"", #none right now, otherwise all ZPs (bridge?)
                    'AVTransport':"", #Play etc. only the coordinators
                    'AlarmClock':"", #only one ZP
                    'RenderingControl':"" #vol etc. All ZPs except if invisible (sub, or stereo pair)
                    }
        self.services = services
        prename = "%s-%s" % (ip, uuid)
        eg.TriggerEvent("ZonePlayerAdded", prefix='SONOS', payload=prename)
        trigger = "%s.%s" % ("ADDED", uuid)
        eg.TriggerEvent(trigger, prefix='SONOS', payload=ip)
        eg.scheduler.AddTask(2, self.GetDeviceXML)
        #self.GetDeviceXML()

    
    def GetDeviceXMLResponse(self, response):
        try:
            if response['status'] == "OK":
                if globalDebug >= 2:
                    print "%s Device XML: \r\n%s" % (self.name, response['body'])
                body = response['body']
                xml = parseString(body)
                #example: <modelNumber>S5</modelNumber>
                #example: <modelDescription>Sonos PLAY:5</modelDescription>
                #example: <modelName>Sonos PLAY:5</modelName>
                self.model = xml.getElementsByTagName('modelNumber')[0].firstChild.nodeValue
                self.modelName = xml.getElementsByTagName('modelName')[0].firstChild.nodeValue
                self.name = xml.getElementsByTagName('roomName')[0].firstChild.nodeValue
                self.swversion = xml.getElementsByTagName('softwareVersion')[0].firstChild.nodeValue
                self.hwversion = xml.getElementsByTagName('hardwareVersion')[0].firstChild.nodeValue
                if globalDebug >= 1:
                    print "%s--%s--%s is a %s" % (self.name,self.uuid,self.ip,self.modelName)
                if globalDebug >= 1:
                    print "      %s--HW Version:  %s" % (self.name,self.hwversion)
                    print "      %s--SW Version:  %s" % (self.name,self.swversion)
                    print "      %s--SONOS Model: %s" % (self.name,self.model)
            else:
                print "**Response Device XML Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
                if globalDebug >= 1:
                    print "%s Device XML Request Error: \r\n%s" % (self.name, response['body'])
        except:
            print "**Response Device XML Request Error from %s" % (self.name)
            print response
            errorText = "**Response Device XML Request Error from %s\n\n%s" % (self.name,response)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
        
        
    def GetDeviceXML(self):
        #self.xmllocation
        if globalDebug >= 1:
            print "Requesting Device XML for %s..." % self.uuid
        port = 1400
        location = self.xmllocation[self.xmllocation.find('/',8):]
        data = "GET " + location + " HTTP/1.1\r\nHOST: " + self.ip + ":"+str(port)+"\r\nConnection: close\r\nACCEPT: */*\r\nUSER-AGENT: Linux UPnP/1.0 Sonos/26.1-76020 (WDCR:Microsoft Windows NT 6.2.9200.0)\r\n\r\n"
        self.deviceXMLRequest = AsyncRequesting(self.ip, port, data, self.GetDeviceXMLResponse)

            
    def TransportState(self, transportstate):
        # Transport States from SONOS ZP (transportstate/self.zpTransportState): 
        #    STOPPED, PAUSED_PLAYBACK, TRANSITIONING, PLAYING
        # Transport States for EG and Triggering Events (globalZPList[uuid].transportstate):
        #    Stopped, Playing
        # should only be called when AVTransportURI is present (updated) in AVTransport Event
        trigger = ""
        if globalDebug >= 1:
            print "%s Pre Transport State: %s" % (self.name,self.transportState)
        self.zpTransportState = transportstate
        if self.transportState == "":
            if transportstate == "TRANSITIONING":
                self.transportState = "Playing"
                trigger = "%s.%s" % (self.uuid, self.transportState)
            if transportstate == "PAUSED_PLAYBACK":
                self.transportState = "Stopped"
                trigger = "%s.%s" % (self.uuid, self.transportState)
            if transportstate == "STOPPED":
                self.transportState = "Stopped"
                trigger = "%s.%s" % (self.uuid, self.transportState)
            if transportstate == "PLAYING":
                self.transportState = "Playing"
                trigger = "%s.%s" % (self.uuid, self.transportState)
        elif self.transportState == "Playing":
            if transportstate == "PAUSED_PLAYBACK":
                self.transportState = "Stopped"
                trigger = "%s.%s" % (self.uuid, self.transportState)
            if transportstate == "STOPPED":
                self.transportState = "Stopped"
                trigger = "%s.%s" % (self.uuid, self.transportState)
        elif self.transportState == "Stopped":
            if transportstate == "PLAYING":
                self.transportState = "Playing"
                trigger = "%s.%s" % (self.uuid, self.transportState)
            if transportstate == "TRANSITIONING":
                self.transportState = "Playing"
                trigger = "%s.%s" % (self.uuid, self.transportState)
        if trigger != "":
            eg.TriggerEvent(trigger, prefix='SONOS', payload=self.name)
        if globalDebug >= 1:
            print "%s Transport State: %s" % (self.name,self.transportState)
    
    #------------- Standard functions for commands -----------------------
    def CommandPacketForm(self, path, hostport, xml, service, command):
        datalist = [
            'POST %s HTTP/1.1\r\n' % path,
            'Accept-Encoding: gzip\r\n',
            'CONNECTION: close\r\n',
            'HOST: %s\r\n' % hostport,
            'CONTENT-TYPE: text/xml; charset="utf-8"\r\n',
            'CONTENT-LENGTH: %s\r\n' % len(xml),
            'SOAPACTION: "urn:schemas-upnp-org:service:%s:1#%s"\r\n' % (service, command),
            '\r\n',
            xml.decode('utf-8'),#encode added
            '\r\n',
            '\r\n'
        ]
        return "".join(datalist)
    
    def XMLDataForm(self, service, command, variables={} ):
        try:
            xmldoc = '''<?xml version="1.0" encoding="utf-8"?>
            <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
                <s:Body>
                </s:Body>
            </s:Envelope>'''
            xml = parseString(xmldoc)
            body = xml.getElementsByTagName('s:Body')[0]
            cmdnode = xml.createElement("u:"+command)
            urn = "urn:schemas-upnp-org:service:%s:1" % service
            cmdnode.setAttribute("xmlns:u",urn) 
            for var, value in variables.iteritems():
                if globalDebug >= 1:
                    print "Command Variables " + var + ":" + value
                newnode = xml.createElement(var)
                newnode.appendChild(xml.createTextNode(value))
                cmdnode.appendChild(newnode)
            body.appendChild(cmdnode)
            xmlstr = xml.toxml(encoding="utf-8")
            xmlstr = xmlstr.replace("\r","").replace("\n","").replace("    ","") #compress
            return xmlstr
        except Exception, e:
            print "XMLDataForm Error %s" % (e) 
            errorText = "XMLDataForm Error %s" % (e)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
    
    def SendCommandWait(self):
        while True:
         time.sleep(0.1)#small delay to allow socket to be created and wait between reads
         try:
             #check to see if socket is still alive, if it's not break. This is to avoid hanging in the loop. 
             noread = self.socketSendCmd.getsockname()
         except:
             if globalDebug >= 1:
                 print "SendCommandWait complete - %s" % (self.name)
             self.sendCmdState = "ready"
             break
    
    #---------- generic command send (can use to send commands for something that is not hard coded.        
    def SendCommand(self, service, command, device = '', variables={'InstanceID':'0'}, responseCallBack = 'StandardCmdRes'):
        self.sendCmdState = "busy"
        try:
            callBackFunction = getattr(self, responseCallBack)
        except:
            if globalDebug >= 1:
                print "SendCommand responseCallBack function not found, setting to StandardCmdRes"
            callBackFunction = getattr(self, 'StandardCmdRes')
            
        try:
            command = command[0].upper() + command[1:] #make sure first character is capitalized
            if globalDebug >= 1:
                print "Sending %s to %s" % (command, self.name)
            if device == "":
                path = "/%s/Control" % (service)
            else:
                path = "/%s/%s/Control" % (device, service)
            hostport = self.ip + ":" + str(self.COMMANDPORT)
            xml = self.XMLDataForm(service, command, variables)
            data = self.CommandPacketForm(path, hostport, xml, service, command)
            if globalDebug >= 2:
                print data
            self.socketSendCmd = AsyncRequesting(self.ip, self.COMMANDPORT, data, callBackFunction)
            #eg.RestartAsyncore() removed
            if globalDebug >= 1:
                print "%s Sending %s to %s" % (self.socketSendCmd.portused, command, self.name)
        except Exception, e:
            print "ERROR Handled: Sending %s to %s Failed - %s" % ( command, self.name, e)
            self.sendCmdState = "ready"
            errorText = "ERROR Handled: Sending %s to %s Failed - %s" % ( command, self.name, e)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
            
        
    def SendCommandPrint(service, command, device = '', variables={'InstanceID':'0'}):
        self.SendCommand(service, command, device, variables, 'StandardCmdResPrint')
    
    #------------- Device Property Commands -------------------------------------------------

    def SendSetZoneName(self, name):
        variables = {'DesiredZoneName':name, 'DesiredIcon':'', 'DesiredConfiguration':''}
        self.SendCommand( "DeviceProperties", "SetZoneAttributes", "", variables)
        
    #------------- AVTransport Commands -------------------------------------------------
        
    def SendBecomeCoordinatorOfStandaloneGroup(self):
        self.SendCommand('AVTransport', 'BecomeCoordinatorOfStandaloneGroup', 'MediaRenderer')
        
    def SendPlay(self):
        self.SendCommand( "AVTransport", "Play", "MediaRenderer", variables={'InstanceID':'0', 'Speed':'1'})
    
    def SendPause(self):
        self.SendCommand( "AVTransport", "Pause", "MediaRenderer")
        
    def SendStop(self):
        self.SendCommand( "AVTransport", "Stop", "MediaRenderer")
        
    def SendNext(self):
        self.SendCommand( "AVTransport", "Next", "MediaRenderer")
    
    def SendPrevious(self):
        self.SendCommand( "AVTransport", "Previous", "MediaRenderer")
        
    def SendSeek(self, unit, target):
        variables = {'InstanceID':'0', 'Unit':unit, 'Target':target}
        self.SendCommand( "AVTransport", "Seek", "MediaRenderer", variables)
    
    def SendGetPositionInfo(self, callback=None):
        variables = {'InstanceID':'0'}
        self.GetPositionInfoCallback = callback
        self.SendCommand( "AVTransport",  "GetPositionInfo", "MediaRenderer", variables, 'ResponseGetPositionInfo')
    
    def StorePositionInfo(self, callback=None):
        self.storePositionInfo = {}
        self.StorePositionInfoCallback = callback
        self.SendGetPositionInfo(self.StorePositionInfoResponse)

    def SendGetMediaInfo(self, callback=None):
        variables = {'InstanceID':'0'}
        self.GetMediaInfoCallback = callback
        self.SendCommand( "AVTransport", "GetMediaInfo", "MediaRenderer", variables, 'ResponseGetMediaInfo')
    
    def StoreMediaInfo(self, callback=None):
        self.StoreMediaInfoCallback = callback
        self.SendGetMediaInfo(self.StoreMediaInfoResponse)
    
    def SendSetAVTransportURI(self, uri, urimetadata=''):
        variables = {'InstanceID':'0', 
                     'CurrentURI':uri, 
                     'CurrentURIMetaData':urimetadata
                    }
        self.SendCommand( "AVTransport", "SetAVTransportURI", "MediaRenderer", variables)
        
    def SendAddURIToQueue(self, uri, urimetadata):
        variables = {'InstanceID':'0', 
                     'EnqueuedURI':uri, 
                     'EnqueuedURIMetaData':urimetadata,
                     'DesiredFirstTrackNumberEnqueued':'0',
                     'EnqueueAsNext':'0'
                    }
        self.SendCommand( "AVTransport", "AddURIToQueue", "MediaRenderer", variables)
    
    def SendSetPlayMode(self, playmode):
        variables = {'InstanceID':'0', 'NewPlayMode':playmode}
        self.SendCommand( "AVTransport", "SetPlayMode", "MediaRenderer", variables)
    
    def SendSetCrossfadeMode(self, crossfade):
        if crossfade == "ON":
            crossfade = '1'
        else:
            crossfade = '0'
        variables = {'InstanceID':'0', 'CrossfadeMode':crossfade}
        self.SendCommand( "AVTransport", "SetCrossfadeMode", "MediaRenderer", variables)
    
    def SendRemoveAllTracksFromQueue(self):
        variables = {'InstanceID':'0'}
        self.SendCommand( "AVTransport", "RemoveAllTracksFromQueue", "MediaRenderer", variables)
        
    def SendConfigureSleepTimer(self, timer): #timer in minutes
        if int(timer) == 0:
            time = ""
        else:
            hour = int(timer)//60
            minutes = int(timer)%60
            time = '%s:%s:00' % (str(hour).zfill(2), str(minutes).zfill(2))
        variables = {'InstanceID':'0', 'NewSleepTimerDuration':time}
        self.SendCommand( "AVTransport", "ConfigureSleepTimer", "MediaRenderer", variables)
    
    #------------- Rendering Commands -------------------------------------------------    
    #NOTE: sending volume commands should not be sent to invisible ZPs. 
    def SendRelVolume(self, incvol):
        variables = {'InstanceID':'0', 'Channel':'Master', 'Adjustment':incvol}
        self.SendCommand( "RenderingControl", "SetRelativeVolume", "MediaRenderer", variables)

    def SendSetVolume(self, setvol):
        variables = {'InstanceID':'0', 'Channel':'Master', 'DesiredVolume':setvol}
        self.SendCommand( "RenderingControl", "SetVolume", "MediaRenderer", variables)

    def SendMuteOn(self):
        variables = {'InstanceID':'0', 'Channel':'Master', 'DesiredMute':'1'}
        self.SendCommand( "RenderingControl", "SetMute", "MediaRenderer", variables)
    
    def SendMuteOff(self):
        variables = {'InstanceID':'0', 'Channel':'Master', 'DesiredMute':'0'}
        self.SendCommand( "RenderingControl", "SetMute", "MediaRenderer", variables)
        
    #------------- Group Rendering Commands -------------------------------------------------
    #NOTE: these commands should only be sent to the coordinator of the groups
    def SendGroupRelVolume(self, incvol):
        variables = {'InstanceID':'0', 'Adjustment':incvol}
        self.SendCommand( "GroupRenderingControl", "SetRelativeGroupVolume", "MediaRenderer", variables)

    def SendSetGroupVolume(self, setvol):
        variables = {'InstanceID':'0', 'DesiredVolume':setvol}
        self.SendCommand( "GroupRenderingControl", "SetGroupVolume", "MediaRenderer", variables)
    
    def SendGroupMuteOff(self):
        variables = {'InstanceID':'0', 'DesiredMute':'0'}
        self.SendCommand( "GroupRenderingControl", "SetGroupMute", "MediaRenderer", variables)
        
    def SendGroupMuteOn(self):
        variables = {'InstanceID':'0', 'DesiredMute':'1'}
        self.SendCommand( "GroupRenderingControl", "SetGroupMute", "MediaRenderer", variables)
        
    #------------- Media Server Commands ------------------------------------------------- 
    def SendGetFavPlayList(self, callback=None):    
        variables = {
                     'ObjectID':'FV:2',
                     'BrowseFlag':'BrowseDirectChildren',
                     'Filter':'dc:title,res,dc:creator,upnp:artist,upnp:album,upnp:albumArtURI',
                     'StartingIndex':'0',
                     'RequestedCount':'100',
                     'SortCriteria':''
                    }
        self.GetFavPlayListCallback = callback
        self.SendCommand( "ContentDirectory", "Browse", "MediaServer", variables, 'ResponseGetFavPlayList')
    
    #------------- Response Callback Functions  ------------------------------------------   
    def StandardCmdResPrint(self, response):
        self.sendCmdState = "ready"
        try:
            if response['status'] == "OK":
                print "%s Standard Response: \r\n%s" % (self.name, response['body'])
                pass
            else:

                print "**Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
                if globalDebug >= 1:
                    print "Response Data: %s" % (self.name, response['body'])
        except:
            print "**Response HTML Error from %s" % (self.name)
            errorText = "**Response HTML Error from %s" % (self.name)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
    
    def StandardCmdRes(self, response):
        self.sendCmdState = "ready"
        try:
            if response['status'] == "OK":
                if globalDebug >= 1:
                    print "%s Standard Response: \r\n%s" % (self.name, response['body'])
                pass
            else:
                print "**Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
                if globalDebug >= 1:
                    print "Response Data: %s" % (self.name, response['body'])
        except:
            print "**Response HTML Error from %s" % (self.name)
            print response
            errorText = "**Response HTML Error from %s\n\n%s" % (self.name,response)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
            
    def ResponseGetPositionInfo(self, response):
        self.sendCmdState = "ready"
        try:
            if response['status'] == "OK":
                if globalDebug >= 1:
                    print "%s GetPositionInfo Response: \r\n%s" % (self.name, response['body'])
                xmlstr = response['body']
                xml = parseString(xmlstr.encode('utf-8'))
                #current track playing info. 
                try:
                    self.trackNum = xml.getElementsByTagName('Track')[0].childNodes[0].nodeValue
                except:
                    self.trackNum = ""
                try:    
                    self.trackDuration = xml.getElementsByTagName('TrackDuration')[0].childNodes[0].nodeValue
                except:
                    self.trackDuration = ""
                try:     
                    self.trackURI = xml.getElementsByTagName('TrackURI')[0].childNodes[0].nodeValue
                except:
                    self.trackURI = ""
                try:     
                    self.trackMetaData = xml.getElementsByTagName('TrackMetaData')[0].childNodes[0].nodeValue
                except:
                    self.trackMetaData = ""
                try:     
                    self.relTime = xml.getElementsByTagName('RelTime')[0].childNodes[0].nodeValue
                except:
                    self.relTime = ""
                if globalDebug >= 1:
                    print "Track Number: %s" % self.trackNum
                    print "Track Duration: %s" % self.trackDuration
                    print "Track URI: %s" % self.trackURI
                    print "Track MetaData: %s" % self.trackMetaData
                    print "Track RelTime: %s" % self.relTime
                #call callback function if present 
                try: 
                    self.GetPositionInfoCallback() 
                    self.GetPositionInfoCallback = None
                except: 
                    pass
            else:
                print "**Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
                if globalDebug >= 1:
                    print "Response Data: %s" % (self.name, response['body'])
        except:
            print "**Response HTML Error from %s" % (self.name) 
            errorText = "**Response HTML Error from %s" % (self.name)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
     
    def ResponseGetMediaInfo(self, response):
        self.sendCmdState = "ready"
        try:
            if response['status'] == "OK":
                if globalDebug >= 1:
                    print "%s GetMediaInfo Response %s" % (self.name, response['body'])
                xmlstr = response['body']
                xml = parseString(xmlstr.encode('utf-8'))
                try:
                    self.nrTracks = xml.getElementsByTagName('NrTracks')[0].childNodes[0].nodeValue
                except:
                    self.nrTracks = 0
                try:
                    self.currentURI = xml.getElementsByTagName('CurrentURI')[0].childNodes[0].nodeValue
                except:
                    self.currentURI = ""
                try:
                    self.currentURIMetaData = xml.getElementsByTagName('CurrentURIMetaData')[0].childNodes[0].nodeValue
                except:
                    self.currentURIMetaData = ""
                self.isPlayList = ( self.currentURI.find("x-rincon-queue:") == 0 )
                if globalDebug >= 1:
                    print "Number of Tracks: %s" % self.nrTracks
                    print "Current URI: %s" % self.currentURI
                    print "Current URI MetaData: %s" % self.currentURIMetaData
                    print "Is this a Play List: %s" % self.isPlayList
                #call callback function if present 
                try: 
                    self.GetMediaInfoCallback() 
                    self.GetMediaInfoCallback = None
                except: 
                    pass 
            else:
                print "Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
                if globalDebug >= 1:
                    print "Response Data: %s" % (self.name, response['body'])
        except Exception, e:
            print "**Response HTML Error from %s: %s" % (self.name, e)
            errorText = "**Response HTML Error from %s: %s" % (self.name,e)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
    
    def StorePositionInfoResponse(self):
        self.sendCmdState = "ready"
        self.storePositionInfo['trackNum'] = self.trackNum
        self.storePositionInfo['trackDuration'] = self.trackDuration
        self.storePositionInfo['trackURI'] = self.trackURI
        self.storePositionInfo['trackMetaData'] = self.trackMetaData
        self.storePositionInfo['relTime'] = self.relTime
        #call callback function if present 
        try: 
            self.StorePositionInfoCallback() 
            self.StorePositionInfoCallback = None
        except: 
            pass
            
    def StoreMediaInfoResponse(self):
        self.sendCmdState = "ready"
        self.storeMediaInfo['nrTracks'] = self.nrTracks
        self.storeMediaInfo['currentURI'] = self.currentURI
        self.storeMediaInfo['currentURIMetaData'] = self.currentURIMetaData
        self.storeMediaInfo['isPlayList'] = self.isPlayList
        self.storeMediaInfo['transportstate'] = self.transportState
        #call callback function if present 
        try: 
            self.StoreMediaInfoCallback() 
            self.StoreMediaInfoCallback = None
        except: 
            pass
    
    def ResponseGetFavPlayList(self, response):
        self.sendCmdState = "ready"
        try:
            if response['status'] == "OK":
                if globalDebug >= 1:
                    print "%s GetFavPlayList Response \n%s" % (self.name, response['body'])
                xmlstr = response['body']
                xml = parseString(xmlstr)
                xmlplayliststring = xml.getElementsByTagName('Result')[0].firstChild.nodeValue
                xml = parseString(xmlplayliststring.encode('utf-8'))
                #print xml.toxml()
                self.favPlayList={} #clear dict
                for item in xml.getElementsByTagName('item'):
                    tempdescription = item.getElementsByTagName('r:description')[0].firstChild.nodeValue.replace(" Station","")
                    temptitle = item.getElementsByTagName('dc:title')[0].firstChild.nodeValue
                    tempuri = item.getElementsByTagName('res')[0].firstChild.nodeValue
                    subxmlstr = item.getElementsByTagName('r:resMD')[0].firstChild.nodeValue
                    subxml = parseString(subxmlstr.encode('utf-8'))
                    tempurimetadata = subxml.getElementsByTagName('DIDL-Lite')[0].toxml()
                    tempupnpclass = subxml.getElementsByTagName('upnp:class')[0].firstChild.nodeValue
                    if tempupnpclass.find("playlistContainer") > 0: #is this a streaming station or a playlist
                        tempisplaylist = True
                    else:
                        tempisplaylist = False
                    self.favPlayList[temptitle]={} #clear/create dict
                    self.favPlayList[temptitle]['description'] = tempdescription
                    self.favPlayList[temptitle]['uri'] = tempuri
                    self.favPlayList[temptitle]['urimetadata'] = tempurimetadata
                    self.favPlayList[temptitle]['upnpclass'] = tempupnpclass
                    self.favPlayList[temptitle]['isplaylist'] = tempisplaylist
                
                #call callback function if present 
                try: 
                    self.GetFavPlayListCallback() 
                    self.GetFavPlayListCallback = None
                except: 
                    print "Error No GetFavPlayListCallback executed..."
                    errorText = "Error No GetFavPlayListCallback executed..."
                    eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
            else:
                print "**Response HTML Error from %s: %s %s" % (self.name, response['status-code'],response['status'])
                if globalDebug >= 1:
                    print "Response Data: %s" % (self.name, response['body'])
        except Exception, e:
            print "**Response HTML Error from %s %s response:\n%s" % (self.name, e, response) 
            errorText = "**Response HTML Error from %s %s response:\n%s" % (self.name, e, response) 
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)            
            
            
def searchforsonos(broadcastip='239.255.255.250'):
    try:
        zpList = {} #need to make zp class now. 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1.5)#very important if useing while loop to receive all responses,if this is removed, loop occurs
        s.bind((localip, 0)) #port changed to 0 to allow OS to pick available port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        data = 'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 3\r\nST: urn:schemas-upnp-org:device:ZonePlayer:1\r\n\r\n'
        #need to send use broadcast address 239.255.255.250 and 255.255.255.255 due to some routers
        s.sendto(data, (broadcastip, 1900))
        print "Searching for SONOS ZonePlayers on network..."
        while True:#look until timeout # this is to capture all responses
            data, srv_sock = s.recvfrom(65565)              
            if not data: break
            if data.find("ST: urn:schemas-upnp-org:device:ZonePlayer:1") > 0: #verify it's SONOS
                srv_addr = srv_sock[0]
                html = HtmlSplit(data)
                uuid = html["USN"].split("::")[0].split(":")[1]
                household = html["X-RINCON-HOUSEHOLD"]
                location = html["LOCATION"]
                zpList[uuid] = ZonePlayer(uuid, srv_addr, location)
                zpList[uuid].household = household
                #print "USN: %s IP: %s" % (zpList[uuid].uuid, zpList[uuid].ip)
                #print "Household HHID: %s" % zpList[uuid].household
                #print "XML info: %s" % location
                #print data
    except Exception, e:
        if str(e) == "timed out":
            print "MSEARCH socket closed"
        else:
            print "ERROR %s" % e
            errorText = "MSEARCH Socket ERROR %s" % e
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText) 
        s.close
    return zpList 

    
def connerror(status, reason):
    if not int(status) == 200:
        print "ERROR: " + str(status) + " - " + reason  
        errorText = "Connection ERROR: " + str(status) + " - " + reason
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText) 

        
def httpRequest(host, port, path, type, headers, data=""):
    print "host: %s" % host
    print "path: %s" % path
    print "port: %s" % port
    print "type: %s" % type
    print "headers: %s" % headers
    print "data: %s" % data
    conn = httplib.HTTPConnection(host,port)
    conn.request(type, path, data, headers)
    res = conn.getresponse() #res.read() #res.getheader(name) #res.getheaders() list #
    connerror(res.status, res.reason)
    conn.close
    return res  


################################################################################################  
###################################### Plugin Base #############################################
################################################################################################
class Sonos(eg.PluginBase):

    def __init__(self):
        print "initializing SONOS plugin..."
        self.server = None
        self.AddActionsFromList(ACTIONS)
    
    def __start__(self, debugLvL=0):
        print "SONOS plugin starting..."
        global globalZPList
        global globalServiceList
        global localip
        global serverPort
        global globalDebug 
        globalDebug = debugLvL
        if localip == "":
            localip = get_lan_ip()
        if globalDebug >= 1:
            print "Network IP Address: %s" % localip        
        globalServiceList = {}
        try:
            globalZPList = searchforsonos('239.255.255.250')
            if not globalZPList:  #if nothing found, try one more time using different port. 
                globalZPList = searchforsonos('255.255.255.255')
            if not globalZPList: # if still no ZPs found, stop plugin. 
                errorText = "ERROR, no ZPs found on network during M-SEARCH"
                eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
                print "**** No Zone Players were found on your network, SONOS plugin shutting down ****"
                print " 1) check to make sure your local ip is correct when the plugin first starts"
                print " 2) verify EG is allowed in your firewall settings"
                print " 3) if you have multiple active network ports, open the _init_.py file and enter your IP address"
            else:
                self.server = EventServer() #start listening for events as long as plugin is active (creates a listening socket)
                serverPort = self.server.port
                uuid = globalZPList.keys()[0] #select random ZP to get grouptopology from 
                #send request using asyncore
                tempservice = Service(globalZPList[uuid], "/ZoneGroupTopology/Event", ZoneGroupTopologyEvent, serverPort)   
                #asyncore.loop(5)
                eg.RestartAsyncore() #this used instead of asyncore.loop for EG.
        except Exception,e: 
            print "error while executing..."
            print str(e)
            PrintException()
            errorText = "error while executing..."
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=errorText)
            print "calling closesockets due to exception..."
            self.closesockets()
            
    def __stop__(self):
        print "SONOS plugin stopping..."
        self.closesockets()
        
    def __close__(self):
        print "SONOS plugin closing..."
        #self.closesockets()

    def closesockets(self):
        #print group topology state one last time. 
        print "\r\nSONOS Plugin SHUTTING DOWN..."
        if globalDebug >= 1:
            print 'caller name:', inspect.stack()[1][3]

        for uuid in globalZPList:
            if globalZPList[uuid].coordinator == uuid:
                coordinator = "Coordinator"
            else:
                coordinator = ""
            if globalDebug >= 1:
                print uuid + " = " + globalZPList[uuid].name + " : " + coordinator + " SID:" + globalZPList[uuid].services['AVTransport']
        try:
            if globalDebug >= 1:
                print "unsubscribing to all services..." 
            #replace with loop that cycles through globalServiceList
            for k, service in globalServiceList.iteritems():
                #print "SID Exists..."
                service.Unsubscribe()
        except AttributeError,e:
            if globalDebug >= 1:
                print "nothing to unsubscribe from : %s" % str(e)
            pass
        if self.server:
            self.server.close()
        print "SONOS Event Server has been Shut down, the end."        
    
    def Configure(self, debugLvL=0):
        panel = eg.ConfigPanel()
        mySizer = wx.GridBagSizer(6, 2)
        mySizer.AddGrowableRow(4)
        mySizer.AddGrowableCol(0)
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        text1 = '''
                0 - Debug Off, only screen print when errors occur
                1 - Print general comments within functions
                2 - Print Asyncore Socket messages and everything else
                '''
        TextZPSelect = wx.StaticText(panel, -1, "Select Debug Level...")
        TextSelect = wx.StaticText(panel, -1, text1)
        TextNote = wx.StaticText(panel, -1, "")
        try:
            DropDown = wx.SpinCtrl(panel, -1, str(debugLvL), (0,0), (100,20))
            DropDown.SetRange(0,2)
        except:
            DropDown = wx.SpinCtrl(panel, -1, '0', (0,0), (100,20))
            DropDown.SetRange(0,2)
        
        mySizer.Add(TextZPSelect, (0,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(DropDown, (1,0), (1,2), flag = (wx.ALIGN_CENTER | wx.ALIGN_RIGHT))
        mySizer.Add(TextSelect, (3,0), flag = wx.EXPAND)
        mySizer.Add(TextNote, (4,0), (1,2), flag = wx.EXPAND)
        while panel.Affirmed():
            Final = DropDown.GetValue()
            panel.SetResult(
                Final
            )

########################################## Window Panels ########################################
class WindowUUIDText():
    def __init__(self, value = '', title="Select a Zone Player from the list below...", text1="", text2=""):
                
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(5, 1)
        mySizer.AddGrowableRow(4)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        TextPMSelect = wx.StaticText(panel, -1, text1)
        TextPMNote = wx.StaticText(panel, -1, text2)
        #============ text box ==============
        CustomBox =  wx.TextCtrl(panel, -1, value)
        #============ end text box ==============
        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(TextPMSelect, (1,0), flag = wx.EXPAND)
        mySizer.Add(CustomBox, (2,0), flag = wx.EXPAND)
        mySizer.Add(TextPMNote, (3,0), flag = (wx.ALIGN_BOTTOM | wx.ALIGN_LEFT))
        while panel.Affirmed():
            panel.SetResult(
                CustomBox.GetValue()                
            )

class WindowUUIDSelectText():
    def __init__(self, uuid="", value = '', title="Select a Zone Player from the list below...", text1="", text2=""):
                
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(6, 1)
        mySizer.AddGrowableRow(5)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        TextPMSelect = wx.StaticText(panel, -1, text1)
        TextPMNote = wx.StaticText(panel, -1, text2)
        #============ dropdown ==============
        ChoiceList = []
        if globalZPList:
            for k, v in globalZPList.iteritems():
                if v.invisible == 0:
                    ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                    #ChoiceList.append(k)
            if ChoiceList: 
                ChoiceList.sort()
            else:
                ChoiceList.append("-no Zone Players found...-")
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(globalZPList[uuid].name + "-" + uuid + "-" + globalZPList[uuid].ip)
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        #============ end dropdown ==============
        
        #============ text box ==============
        CustomBox =  wx.TextCtrl(panel, -1, value)
        #============ end text box ==============
        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextPMSelect, (2,0), flag = wx.EXPAND)
        mySizer.Add(CustomBox, (3,0), flag = wx.EXPAND)
        mySizer.Add(TextPMNote, (4,0), flag = (wx.ALIGN_BOTTOM | wx.ALIGN_LEFT))
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            panel.SetResult(
                FinalChoice.split("-")[-2], #save only the uuid from the list.
                CustomBox.GetValue()                
            )
            
class WindowUUIDSelecttwo():   
    def __init__(self, uuid="", uuid2 = '', title="Select a Zone Player and item from the list below...", text1="", text2="", models=[]):
                
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(6, 1)
        mySizer.AddGrowableRow(5)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        TextPMSelect = wx.StaticText(panel, -1, text1)
        TextPMNote = wx.StaticText(panel, -1, text2)
        #============ dropdown ==============
        ChoiceList = []
        if globalZPList:
            for k, v in globalZPList.iteritems():
                if v.invisible == 0:
                    ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                    #ChoiceList.append(k)
            if ChoiceList: 
                ChoiceList.sort()
            else:
                ChoiceList.append("-no Zone Players found...-")
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(globalZPList[uuid].name + "-" + uuid + "-" + globalZPList[uuid].ip)
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        #============ end dropdown ==============
        #============ dropdown ==============
        ChoiceList = []
        if globalZPList:
            for k, v in globalZPList.iteritems():
                if v.invisible == 0:
                    if v.model in models or not models:
                        ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                        #ChoiceList.append(k)
            if ChoiceList: 
                ChoiceList.sort()
            else:
                ChoiceList.append("-no Zone Players found...-")
            PMDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(globalZPList[uuid2].name + "-" + uuid2 + "-" + globalZPList[uuid2].ip)
            #p = ChoiceList.index(uuid2)
            PMDropDown.SetSelection(p)
        except: #ValueError:
            PMDropDown.SetSelection(0)
        #============ end dropdown ==============
        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextPMSelect, (2,0), flag = wx.EXPAND)
        mySizer.Add(PMDropDown, (3,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextPMNote, (4,0), flag = wx.EXPAND)
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            FinalPM = PMDropDown.GetStringSelection()
            panel.SetResult(
                FinalChoice.split("-")[-2], #save only the uuid from the list.
                FinalPM.split("-")[-2] #save only the uuid from the list.
            )

         
class WindowUUIDSelectList():
    def __init__(self, uuid="", item = '', title="Select a Zone Player and item from the list below...", list=[], text1="", text2=""):
                
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(6, 1)
        mySizer.AddGrowableRow(5)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        TextPMSelect = wx.StaticText(panel, -1, text1)
        TextPMNote = wx.StaticText(panel, -1, text2)
        #============ dropdown ==============
        ChoiceList = []
        if globalZPList:
            for k, v in globalZPList.iteritems():
                if v.invisible == 0:
                    ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                    #ChoiceList.append(k)
            if ChoiceList: 
                ChoiceList.sort()
            else:
                ChoiceList.append("-no Zone Players found...-")
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs, search network again"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(globalZPList[uuid].name + "-" + uuid + "-" + globalZPList[uuid].ip)
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        #============ end dropdown ==============
        
        #============ dropdown ==============
        ChoiceList = list
        PMDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(item)
            PMDropDown.SetSelection(p)
        except: #ValueError:
            PMDropDown.SetSelection(0)
        #============ end dropdown ==============
        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextPMSelect, (2,0), flag = wx.EXPAND)
        mySizer.Add(PMDropDown, (3,0), flag = (wx.ALIGN_TOP | wx.ALIGN_LEFT))
        mySizer.Add(TextPMNote, (4,0), flag = (wx.ALIGN_BOTTOM | wx.ALIGN_LEFT))
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            FinalPM = PMDropDown.GetStringSelection()
            panel.SetResult(
                FinalChoice.split("-")[-2], #save only the uuid from the list.
                FinalPM                
            )


class WindowUUIDSelectRange():
    def __init__(self, uuid="", value=0, title="Select a Zone Player and Value from the list below...", range="0:100", text1="", text2=""):
                
        try:
            rangeMin = int(range.split(":")[0])
            rangeMax = int(range.split(":")[1])
        except:
            print "Range for Window set incorrectly sb: 'min:max' "
            rangeMin = 0
            rangeMax = 10
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(6, 2)
        mySizer.AddGrowableRow(4)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        TextVolSelect = wx.StaticText(panel, -1, text1)
        TextVolNote = wx.StaticText(panel, -1, text2)
        ChoiceList = []
        if globalZPList:
            for k, v in globalZPList.iteritems():
                try:
                    if v.invisible == 0:
                        ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                except:
                    print "Plugin has not received Group Topology info yet."
            if ChoiceList: 
                ChoiceList.sort()
            else:
                ChoiceList.append("-no Zone Players found...-")
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs found on network, please add a ZP and restart plugin"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(globalZPList[uuid].name + "-" + uuid + "-" + globalZPList[uuid].ip)
            #p = ChoiceList.index(uuid)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        try:
            VolDropDown = wx.SpinCtrl(panel, -1, value, (0,0), (100,20))
            VolDropDown.SetRange(rangeMin,rangeMax)
        except:
            VolDropDown = wx.SpinCtrl(panel, -1, '3', (0,0), (100,20))
            VolDropDown.SetRange(rangeMin,rangeMax)
        
        mySizer.Add(TextZPSelect, (0,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), (1,2), flag = (wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextVolSelect, (3,0), flag = wx.EXPAND)
        mySizer.Add(TextVolNote, (4,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(VolDropDown, (3,1), flag = (wx.ALIGN_CENTER | wx.ALIGN_RIGHT))
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            FinalVol = VolDropDown.GetValue()
            panel.SetResult(
                FinalChoice.split("-")[-2], #save only the uuid from the list.
                str(FinalVol) 
            )

class WindowUUIDMultiSelect():
    def __init__(self, checkList=[], title="Select Zone Players from the list below..."):
        panel = eg.ConfigPanel()
        zpCount = 0
        selectedList = []
        ChoiceList = []
        #count all ZPs that are not hidden.
        if globalZPList:
            for k, v in globalZPList.iteritems():
                try:
                    if v.invisible == 0:
                        ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                except:
                    print "Plugin has not received Group Topology info yet."
            if ChoiceList: 
                ChoiceList.sort()
            else:
                ChoiceList.append("-no Zone Players found...-")
            zpCount = len(ChoiceList)
        else:
            print "!! - No SONOS ZPs found on network, please add a ZP and restart plugin"
            return
            
        mySizer = wx.GridBagSizer(zpCount+1, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        
        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        zpCount = 0
        ZPCheckBox = []
        for k in ChoiceList:
            ZPCheckBox.append( wx.CheckBox(panel, -1, label=k) )
            if k.split("-")[-2] in checkList:
                ZPCheckBox[zpCount].SetValue(True)
            else:
                ZPCheckBox[zpCount].SetValue(False)
            mySizer.Add(ZPCheckBox[zpCount], (zpCount+2,0), flag = wx.ALIGN_LEFT)
            zpCount = zpCount + 1
            
        while panel.Affirmed():
            for box in ZPCheckBox:
                if box.GetValue():
                    if box.GetLabel().split("-")[-2] not in selectedList: #only appended if not already added, need for testing command in config window
                        selectedList.append(box.GetLabel().split("-")[-2]) #save only the uuid from the label and only the ZPs checked.
                else:
                    try:
                        selectedList.remove(box.GetLabel().split("-")[-2]) #removes from list if added, this is needed when testing command in config window
                    except:
                        pass
            panel.SetResult(
                selectedList
            )


class WindowUUIDSelect():
    def __init__(self, uuid="", title="Select a Zone Player from the list below...", models=[]):
        panel = eg.ConfigPanel()
        
        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        
        ChoiceList = []
        if globalZPList:
            for k, v in globalZPList.iteritems():
                try:
                    if v.invisible == 0:
                        if v.model in models or not models:
                            ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                except:
                    print "Plugin has not received Group Topology info yet."
            if ChoiceList: 
                ChoiceList.sort()
            else:
                ChoiceList.append("-no Zone Players found...-")
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs found on network, please add a ZP and restart plugin"
            return
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            
            p = ChoiceList.index(globalZPList[uuid].name + "-" + uuid + "-" + globalZPList[uuid].ip)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            panel.SetResult(
                FinalChoice.split("-")[-2] #save only the uuid from the list.
            )         
        
################################################ Actions ########################################

class SetZoneName(eg.ActionBase):
    name = "Change name of selected ZP"
    description = "changes the name of the ZP "

    def __call__(self, uuid="", name=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        if name == "":
            print "Please enter a name for the ZP."
            return
        globalZPList[uuid].SendSetZoneName(name)     

    def Configure(self, uuid="", name=""):
        title = "Select a ZP to change the name of:"
        text1 = 'Enter the name of the ZP:'
        text2 = ''
        winSelectGUI = WindowUUIDSelectText(uuid, name, title, text1, text2)
        
        
class Play(eg.ActionBase):
    name = "Send SONOS PLay"
    description = "sends the play command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendPlay()
    
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)       
            
            
class Pause(eg.ActionBase):
    name = "Send SONOS Pause"
    description = "sends the pause command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendPause()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)

class PauseAll(eg.ActionBase):
    name = "Send SONOS Pause All Players"
    description = "sends the pause command to all ZPs or the coordinator of the group the ZP is in."

    def __call__(self):
        pass
        for uuid, zpObj in globalZPList.iteritems():
            if uuid == zpObj.coordinator:
                globalZPList[uuid].SendPause()       
        
class Stop(eg.ActionBase):
    name = "Send SONOS Stop (NOTE: in most cases Paused should be used instead of Stop)"
    description = "sends the stop command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendStop()
       
    def Configure(self, uuid=""):
        text1 = '''Select a Zone Player from the list below...\n(NOTE: in most cases Paused should be used instead of Stop)'''
        winSelectGUI = WindowUUIDSelect(uuid, text1) 

class Next(eg.ActionBase):
    name = "Send SONOS Next"
    description = "sends the next command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendNext()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)        

class Previous(eg.ActionBase):
    name = "Send SONOS Previous"
    description = "sends the previous command to the ZP or the coordinator of the group the ZP is in."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendPrevious()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)         
 
class VolumeAdjust(eg.ActionBase):
    name = "Send SONOS VolumeAdjust"
    description = "sends command to adjust the volume by a relative amount. "

    def __call__(self, uuid="", incvol="3"):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        globalZPList[uuid].SendRelVolume(incvol)
        #NOTE: sending volume commands should not be sent to 
        # invisible ZPs. When selecting a ZP from the dropdown
        # invisible ZPz are not listed. So this should not be a problem
        if globalDebug >= 1:
            print "adjusted volume by " + str(incvol) + " in " + globalZPList[uuid].name
        
       
    def Configure(self, uuid="", incvol="3"):
        title = "Select a Zone Player and Step Value from the list below..."
        range1 = "-10:10"
        text1 = '''Select incremental percentage to adjust volume\nrelative to current value.\nVol. Up def.= 3\nVol. Dwn def.= -3'''
        text2 = '''- Select positive number to adjust volume up\n - Select negative to adjust volume down.\n'''
        winSelectGUI = WindowUUIDSelectRange(uuid, incvol, title, range1, text1, text2)

class VolumeSet(eg.ActionBase):
    name = "Send SONOS VolumeSet"
    description = "sends command to set volume to specific value. "

    def __call__(self, uuid="", setvol="20"):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        globalZPList[uuid].SendSetVolume(setvol)
        #NOTE: sending volume commands should not be sent to 
        # invisible ZPs. When selecting a ZP from the dropdown
        # invisible ZPz are not listed. So this should not be a problem
        if globalDebug >= 1:
            print "set volume to "+ str(setvol) + " in " + globalZPList[uuid].name
        
       
    def Configure(self, uuid="", setvol="20"):
        title = "Select a Zone Player and Volume level from the list below..."
        range1 = "0:100"
        text1 = '''Select Volume level (0-100%)'''
        text2 = ''''''
        winSelectGUI = WindowUUIDSelectRange(uuid, setvol, title, range1, text1, text2)

class MuteOn(eg.ActionBase):
    name = "Send SONOS Mute On"
    description = "sends command to activate Mute."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        globalZPList[uuid].SendMuteOn()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)

class MuteOff(eg.ActionBase):
    name = "Send SONOS Mute Off"
    description = "sends command to disable Mute."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        globalZPList[uuid].SendMuteOff()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)

        
class MuteAllOn(eg.ActionBase):
    name = "Mute All Players"
    description = "sends the MuteAll command to a ZP that mutes all players."

    def __call__(self):
        for uuid, zpObj in globalZPList.iteritems():
            #if uuid == zpObj.coordinator:
            #    globalZPList[uuid].SendGroupMuteOn()
            if zpObj.invisible == 0:
                globalZPList[uuid].SendMuteOn()
 
class MuteAllOff(eg.ActionBase):
    name = "UnMute All Players"
    description = "sends the UnMute command to a ZP."

    def __call__(self):
        for uuid, zpObj in globalZPList.iteritems():
            #if uuid == zpObj.coordinator:
            #    globalZPList[uuid].SendGroupMuteOff() 
            if zpObj.invisible == 0:
                globalZPList[uuid].SendMuteOff()

class GroupVolumeAdjust(eg.ActionBase):
    name = "Send SONOS GroupVolumeAdjust"
    description = "sends command to adjust the group volume by a relative amount. "

    def __call__(self, uuid="", incvol="3"):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendGroupRelVolume(incvol)
        #NOTE: sending volume commands should not be sent to 
        # invisible ZPs. When selecting a ZP from the dropdown
        # invisible ZPz are not listed. So this should not be a problem
        if globalDebug >= 1:
            print "adjusted group volume by " + str(incvol) + " in " + globalZPList[uuid].name
        
       
    def Configure(self, uuid="", incvol="3"):
        title = "Select a Zone Player and Group Volume Step Value from the list below..."
        range1 = "-10:10"
        text1 = '''Select incremental percentage to adjust group volume\nrelative to current value.\nVol. Up def.= 3\nVol. Dwn def.= -3'''
        text2 = '''- Select positive number to adjust volume up\n - Select negative to adjust volume down.\n'''
        winSelectGUI = WindowUUIDSelectRange(uuid, incvol, title, range1, text1, text2)
        
        
class GroupVolumeSet(eg.ActionBase):
    name = "Send SONOS GroupVolumeSet"
    description = "sends command to set group volume to specific value. "

    def __call__(self, uuid="", setvol="20"):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendSetGroupVolume(setvol)
        #NOTE: sending volume commands should not be sent to 
        # invisible ZPs. When selecting a ZP from the dropdown
        # invisible ZPz are not listed. So this should not be a problem
        if globalDebug >= 1:
            print "set group volume to "+ str(setvol) + " in " + globalZPList[uuid].name
               
    def Configure(self, uuid="", setvol="20"):
        title = "Select a Zone Player and Specific Group Volume level from the list below..."
        range1 = "0:100"
        text1 = '''Select Volume level (0-100%)'''
        text2 = ''''''
        winSelectGUI = WindowUUIDSelectRange(uuid, setvol, title, range1, text1, text2)

class GroupMuteOn(eg.ActionBase):
    name = "Send SONOS Group Mute On"
    description = "sends command to activate Mute for the group."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendGroupMuteOn()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)

class GroupMuteOff(eg.ActionBase):
    name = "Send SONOS Group Mute Off"
    description = "sends command to disable Mute for the group."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendGroupMuteOff()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)

                
class SetPlayMode(eg.ActionBase):
    name = "Send SONOS PlayMode, like shuffle and repeat"
    description = "sends command to set play mode. "

    def __call__(self, uuid="", playmode="NORMAL"):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendSetPlayMode(playmode)
        #NOTE: sending volume commands should not be sent to 
        # invisible ZPs. When selecting a ZP from the dropdown
        # invisible ZPz are not listed. So this should not be a problem
        if globalDebug >= 1:
            print "set playmode to "+ playmode + " in " + globalZPList[uuid].name
        
       
    def Configure(self, uuid="", playmode="NORMAL"):
        title = "Select a Zone Player and Play Mode from the list below..."
        list1 = ["NORMAL", "REPEAT_ALL", "SHUFFLE_NOREPEAT", "SHUFFLE"]
        text1 = '''Select Play Mode.'''
        text2 = '''NOTE: Streaming stations like Pandora don't support PlayMode.\n\tFor this reason if this is sent while listening\n\tto streaming station, it will return a 500 error.'''
        winSelectGUI = WindowUUIDSelectList(uuid, playmode, title, list1, text1, text2)

        
class SetCrossfade(eg.ActionBase):
    name = "Send SONOS Crossfade mode"
    description = "sends command to set crossfade. "

    def __call__(self, uuid="", crossfade="OFF"):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendSetCrossfadeMode(crossfade)
        if globalDebug >= 1:
            print "set crossfade to "+ crossfade + " in " + globalZPList[uuid].name
        
    def Configure(self, uuid="", crossfade="OFF"):
        title = "Select a Zone Player and Crossfade Mode from the list below..."
        list1 = ["OFF", "ON"]
        text1 = '''Select Crossfade mode.'''
        text2 = ''''''
        winSelectGUI = WindowUUIDSelectList(uuid, crossfade, title, list1, text1, text2)
        
class SetSleepTimer(eg.ActionBase):
    name = "Set Sleep Timer"
    description = "sends command to set configure sleep timer. "

    def __call__(self, uuid="", timer="30"):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendConfigureSleepTimer(timer)
        if globalDebug >= 1:
            print "set Sleept timer to "+ str(timer) + " in " + globalZPList[uuid].name
                    
    def Configure(self, uuid="", timer="30"):
        title = "Select a Zone Player and Sleep Timer Value."
        range1 = "0:1200"
        text1 = '''Select Sleep time in minutes.'''
        text2 = '''Set time to 0 if you want to cancel or turn off the current sleep timer'''
        winSelectGUI = WindowUUIDSelectRange(uuid, timer, title, range1, text1, text2)
        
        

class GroupZPs(eg.ActionBase):
    name = "Group Zone Players"
    description = "Will group all Zone Players selected into a single group"

    def __call__(self, coordinator="", selectedList=[]):
        if coordinator == "":
            if len(selectedList) < 2:
                print "Please select at least two or more ZPs to group."
                return
        else:
            if coordinator in selectedList:
                if len(selectedList) == 1:
                    print "Please select at least two or more ZPs to group."
                    return
            if len(selectedList) == 0:
                print "Please select at least two or more ZPs to group."
                return
        #x-rincon:RINCON_000E58A4D8E001400
        
        '''
        inclusive mode only when the coordinator is left blank.
        selecting a coordinator will make an exclusive group, none will be inclusive. 
        inclusion means Zps already part of group will stay part of the group even if not selected
        exclusion means only ZPs selected will be part of the group
        '''
        #command = 'BecomeCoordinatorOfStandaloneGroup'
        #service = 'AVTransport'
        #device = 'MediaRenderer'
        #globalZPList[uuid].SendCommand(service, command, device)
        
        if coordinator == "":
        #find largest group with the selectedList (playing groups have highest priority)
            groups = {}
            groupCordinator = ""
            groupCnt = 0
            for uuid in selectedList:
                groups[globalZPList[uuid].coordinator] = 0
            for cord, cnt in groups.iteritems():
                if globalDebug >= 1:
                    print "    %s" % globalZPList[cord].name
                for uuid, zpObj in globalZPList.iteritems():
                    if cord == zpObj.coordinator and not zpObj.invisible:
                        if globalDebug >= 1:
                            print "        %s" % zpObj.name
                        groups[cord] = groups[cord]+1
                
                #any group that is playing will have 1000 added to it. Then it just finds the largest number
                #this allows it to priorities the groups that are playing first. 
                if globalZPList[cord].transportState == "Playing":#top priority to groups that have music playing
                    groups[cord] = groups[cord]+1000
                if not globalZPList[cord].avTransportURI == "": #priority to groups that have music queued
                    groups[cord] = groups[cord]+100
                if groups[cord]>groupCnt:
                    groupCnt = groups[cord]
                    groupCoordinator = cord
                if globalDebug >= 1:
                    print "    %s" % groups[cord]
            if globalDebug >= 1:
                print "Biggest Group: %s" % globalZPList[groupCoordinator].name
        else:
            groupCoordinator = coordinator
            #if coordinator is not currently coordinator, remove it from the group it's a part of. 
            if coordinator != globalZPList[coordinator].coordinator:
                if globalDebug >= 1:
                    print "- Coordinator is not coordinator -"
                globalZPList[coordinator].SendBecomeCoordinatorOfStandaloneGroup()
                globalZPList[coordinator].SendCommandWait()
            #remove ZPs that are part of the group but not in the selected list
            #only needs to run if coordinator is currently coordinator of a group.
            else:
                if globalDebug >= 1:
                    print "- Coordinator is coordinator -"
                for uuid, zpObj in globalZPList.iteritems():
                    if coordinator == globalZPList[uuid].coordinator and not globalZPList[uuid].invisible:
                        if not uuid in selectedList and not uuid == coordinator:
                            globalZPList[coordinator].SendBecomeCoordinatorOfStandaloneGroup()
                for uuid, zpObj in globalZPList.iteritems():
                    if coordinator == globalZPList[uuid].coordinator and not globalZPList[uuid].invisible:
                        if not uuid in selectedList and not uuid == coordinator:
                            globalZPList[uuid].SendCommandWait()
        #add all ZPs that are part of the group
        trackuri = "x-rincon:" + groupCoordinator
        if globalDebug >= 1:
            print selectedList
        for uuid in selectedList:
            if not uuid == groupCoordinator: #make sure uuid is not the coordinator 
                globalZPList[uuid].SendSetAVTransportURI(trackuri)
        for uuid in selectedList:
            if not uuid == groupCoordinator: #make sure uuid is not the coordinator 
                globalZPList[uuid].SendCommandWait()
        if globalDebug >= 1:
                print "created group..."
                     
    def Configure(self, coordinator="", selectedList=[]):
        panel = eg.ConfigPanel()
        title = '''Select Coordinator of group: 
        Use the drop down to select the ZP that 
        should be the coordinator (the one that will control the music)
        Leave this blank if you want the plugin to automatically select the 
        coordinator based on current group state and music transport state. When 
        left blank the plugin will select a ZP with the largest group and playing 
        music to be the coordinator so the playing music will continue playing 
        when the group is made. 
        Selecting a coordinator will also create an exclusive group. Only ZPs 
        selected will be in the group. If the same group is already present but
        a different ZP is the coordinator, the music will stop due to the fact that
        the coordinator will be changed within the group.
        Leaving the coordinator blank creates an inclusive group. If Zps are part
        of the group already but not selected, they will remain part of the group.
        
        PlayBars: if you want to play the TV input in other rooms, the PlayBar must
        be the coordinator. 
        '''
        zpCount = 0
        ChoiceList = [""]
        #count all ZPs that are not hidden.
        if globalZPList:
            for k, v in globalZPList.iteritems():
                try:
                    if v.invisible == 0:
                        ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                except:
                    print "Plugin has not received Group Topology info yet."
            ChoiceList.sort()
            zpCount = len(ChoiceList)
            ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
        else:
            print "!! - No SONOS ZPs found on network, please add a ZP and restart plugin"
            return           
        p = 0
        try:
            p = ChoiceList.index(globalZPList[coordinator].name + "-" + coordinator + "-" + globalZPList[coordinator].ip)
            ZPDropDown.SetSelection(p)
        except: #ValueError:
            ZPDropDown.SetSelection(0)
            
        mySizer = wx.GridBagSizer(zpCount+3, 2)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        TextZPSelect = wx.StaticText(panel, -1, title)
        mySizer.Add(TextZPSelect, (0,0),(1,3), flag = wx.EXPAND)
        mySizer.Add(ZPDropDown, (1,0),(1,3), flag = (wx.ALIGN_TOP | wx.EXPAND))
        zpHeader = wx.StaticText(panel, -1, "\nSelect all Zone Players that will be included in the group:")
        mySizer.Add(zpHeader, (2,0), flag = wx.EXPAND)
        line = wx.StaticLine(panel, -1,style=wx.LI_HORIZONTAL)
        mySizer.Add(line, (3,0), (1,3), flag = wx.EXPAND)
        zpCount = 0
        ZPCheckBox = []
        for k in ChoiceList[1:]:
            ZPCheckBox.append( wx.CheckBox(panel, -1, label=k) )
            uuid = k.split("-")[-2]
            if uuid in selectedList:
                ZPCheckBox[zpCount].SetValue(True)
            else:
                ZPCheckBox[zpCount].SetValue(False)
            mySizer.Add(ZPCheckBox[zpCount], (zpCount+4,0), flag = wx.ALIGN_LEFT)
            zpCount = zpCount + 1
            
        selectedList = []
        while panel.Affirmed():
            FinalChoice = ZPDropDown.GetStringSelection()
            try:
                coordinator = FinalChoice.split("-")[-2] #save only the uuid from the list.
            except:
                coordinator = ""
            for box in ZPCheckBox:
                uuid = box.GetLabel().split("-")[-2]
                try:
                    selectedList.remove(uuid)
                except:
                    pass
                if box.GetValue():
                    selectedList.append(uuid)
                else:
                    try:
                        selectedList.remove(uuid)
                    except:
                        pass
            panel.SetResult(
                coordinator,
                selectedList
            ) 
            

    
class UnGroup(eg.ActionBase):
    name = "Remove select ZP from current group"
    description = "sends command to activate Mute."

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        #if uuid != globalZPList[uuid].coordinator:
        globalZPList[uuid].SendBecomeCoordinatorOfStandaloneGroup()
       
    def Configure(self, uuid=""):
        winSelectGUI = WindowUUIDSelect(uuid)
 
# need to create command that will take strings to send "SendCommand"
# SendCommand(service, command, device, variables) variables will have to be formatted correcctly. 
# for Device, put a text string that explains the choices

class NotificationStart(eg.ActionBase):
    name = "StoreStateForNotification"
    description = "stores current state to be recalled later"

    def __call__(self, selectedList={}):
        if len(selectedList) == 0:
            print "Please select at least one ZP to store state."
            return
        #try:
            #eg.scheduler.CancelTask(globalRestartScheduler)
        zpList = []
        print "ZP selected: %s" % selectedList
        #first Store Media Info
        for uuid, volDict in selectedList.iteritems():
            if uuid not in globalZPList:
                print "!!! zone player %s no longer in globalZPList (not found on network) !!!" % uuid
            else:
                globalZPList[uuid].storeMediaInfo['volRestore'] = True
                globalZPList[uuid].storeMediaInfo['volume'] = globalZPList[uuid].volume
                globalZPList[uuid].storeMediaInfo['mute'] = globalZPList[uuid].mute
                coordinator = globalZPList[uuid].coordinator
                if coordinator not in globalZPList:
                    print "!!! zone player %s no longer in globalZPList (not found on network) !!!" % uuid
                elif coordinator not in zpList: #make sure to only send it to the ZP once
                    globalZPList[coordinator].storeMediaInfo['mediaRestore'] = True
                    #if transitioning wait to be completed. 
                    while globalZPList[coordinator].zpTransportState == "TRANSITIONING":
                        time.sleep(0.25)
                    globalZPList[coordinator].StoreMediaInfo()
                    zpList.append(coordinator)
                    #handle all ZPs selected first then check positioninfo, this
                    #saves a lot of time when handling many ZPs at once. 
        #loop through each ZP in zpList to see if Position needs to be stored
        for coordinator in zpList:        
            globalZPList[coordinator].SendCommandWait() #make sure previous command is complete
            if globalZPList[coordinator].storeMediaInfo['isPlayList']:
                globalZPList[coordinator].StorePositionInfo() 
        #loop through each ZP to Stop playing before volume adjustments
        for coordinator in zpList:        
            globalZPList[coordinator].SendCommandWait() #make sure previous command is complete
            globalZPList[coordinator].SendStop() 
        #loop through each ZP to set volume (if option selected)
        for uuid, volDict in selectedList.iteritems():
            if uuid not in globalZPList:
                print "!!! zone player %s no longer in globalZPList (not found on network) !!!" % uuid
            elif volDict['vol'] > 0: #if volume set to 0 then use ZP current volume
                globalZPList[uuid].SendCommandWait()
                globalZPList[uuid].SendSetVolume( str(volDict['vol']) )
        #loop through each ZP to un-mute (if option selected)
        for uuid, volDict in selectedList.iteritems():
            if uuid not in globalZPList:
                print "!!! zone player %s no longer in globalZPList (not found on network) !!!" % uuid
            elif volDict['mute']: #if volume set to 0 then use ZP current volume
                globalZPList[uuid].SendCommandWait()
                globalZPList[uuid].SendMuteOff()
          
    def Configure(self, selectedList={}):
        panel = eg.ConfigPanel()
        title = '''Select Zone Players that you want the Notifications to be sent to.
        
        Volume: Set the volume level for the notification to played at.
                     If set to 0 then the ZP's current volume will be used.
        
        un-Mute: check if you want to make sure the ZP is un-muted during the notificaiton
                      If this is unchecked, notifications will not be heard in rooms that are muted. 
        '''
        zpCount = 0
        ChoiceList = []
        #count all ZPs that are not hidden.
        if globalZPList:
            for k, v in globalZPList.iteritems():
                try:
                    if v.invisible == 0:
                        ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                except:
                    print "Plugin has not received Group Topology info yet."
            if ChoiceList: 
                ChoiceList.sort()
            else:
                ChoiceList.append("-no Zone Players found...-")
            zpCount = len(ChoiceList)
        else:
            print "!! - No SONOS ZPs found on network, please add a ZP and restart plugin"
            return
            
        mySizer = wx.GridBagSizer(zpCount+3, 2)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)
        
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        title = title + "\n"
        TextZPSelect = wx.StaticText(panel, -1, title)
        mySizer.Add(TextZPSelect, (0,0),(1,3), flag = wx.EXPAND)
        zpHeader = wx.StaticText(panel, -1, "Zone Players")
        mySizer.Add(zpHeader, (1,0), flag = wx.EXPAND)
        volHeader = wx.StaticText(panel, -1, "Volume")
        mySizer.Add(volHeader, (1,1), flag = wx.ALIGN_CENTER)
        mutHeader = wx.StaticText(panel, -1, "un-Mute")
        mySizer.Add(mutHeader, (1,2), flag = wx.ALIGN_CENTER)
        line = wx.StaticLine(panel, -1,style=wx.LI_HORIZONTAL)
        mySizer.Add(line, (2,0), (1,3), flag = wx.EXPAND)
        zpCount = 0
        ZPCheckBox = []
        volRange = []
        muteCB = []
        for k in ChoiceList:
            ZPCheckBox.append( wx.CheckBox(panel, -1, label=k) )
            muteCB.append( wx.CheckBox(panel, -1) )
            volRange.append( wx.SpinCtrl(panel, -1, size=(60,20) ))
            volRange[zpCount].SetRange(0,100)
            uuid = k.split("-")[-2]
            if uuid in selectedList:
                ZPCheckBox[zpCount].SetValue(True)
                try:
                    volRange[zpCount].SetValue(selectedList[uuid]['vol'])
                except Exception, e:
                    print "vol faile %s" % e
                    volRange[zpCount].SetValue( 0 )
                try:
                    muteCB[zpCount].SetValue(selectedList[uuid]['mute'])
                except:
                    print "mute fail %s" % e
                    muteCB[zpCount].SetValue(False)
            else:
                ZPCheckBox[zpCount].SetValue(False)
                volRange[zpCount].SetValue( 0 )
                muteCB[zpCount].SetValue(False)
            mySizer.Add(volRange[zpCount], (zpCount+3,1), flag = wx.ALIGN_CENTER)
            mySizer.Add(muteCB[zpCount], (zpCount+3,2), flag = wx.ALIGN_CENTER)
            mySizer.Add(ZPCheckBox[zpCount], (zpCount+3,0), flag = wx.ALIGN_LEFT)
            zpCount = zpCount + 1
            
        while panel.Affirmed():
            for (box, vol, mute) in zip(ZPCheckBox, volRange, muteCB):
                if box.GetValue():
                    uuid = box.GetLabel().split("-")[-2]
                    selectedList[uuid] = {}
                    selectedList[uuid]['vol']= vol.GetValue()
                    selectedList[uuid]['mute'] = mute.GetValue() #save only the uuid from the label and only the ZPs checked.
                else:
                    try: #if part of dict, remove ZP
                        del selectedList[box.GetLabel().split("-")[-2]]
                    except:
                        pass
            panel.SetResult(
                selectedList
            )

        
class NotificationRestore(eg.ActionBase):        
    name = "Restore Track State"
    description = "execute this action after StoreCurrentTrackState to restore track state"

    def __call__(self, restoreDelay=10):
        global globalRestoreTask
        if globalDebug >= 1:
            print "Restoring music in %s seconds" % restoreDelay
        globalRestoreTask = eg.scheduler.AddTask(restoreDelay, self.RestoreTrackStateNow)
        
    def RestoreTrackStateNow(self):
        if globalDebug >= 1:
            print "Restoring music now"
        #restore URI
        for uuid, zpObj in globalZPList.iteritems(): 
            #try:
            if zpObj.storeMediaInfo['mediaRestore']:
                uri = zpObj.storeMediaInfo['currentURI']
                uriMetaData = zpObj.storeMediaInfo['currentURIMetaData']
                zpObj.SendSetAVTransportURI(uri, uriMetaData)
        #restore volume and mute state
        for uuid, zpObj in globalZPList.iteritems(): 
            #try:
            if zpObj.storeMediaInfo['volRestore']:
                zpObj.SendCommandWait()
                zpObj.SendSetVolume( zpObj.storeMediaInfo['volume']) 
                zpObj.SendCommandWait()
                if zpObj.storeMediaInfo['mute'] == '1':
                    zpObj.SendMuteOn()
                else:
                    zpObj.SendMuteOff()
                globalZPList[uuid].storeMediaInfo['volRestore'] = False
        #restore seek point and play state
        for uuid, zpObj in globalZPList.iteritems(): 
            #try:
            if zpObj.storeMediaInfo['mediaRestore']:
                zpObj.SendCommandWait()
                if zpObj.storeMediaInfo['isPlayList']:
                    zpObj.SendSeek( "TRACK_NR", zpObj.storePositionInfo['trackNum'])
                    zpObj.SendCommandWait()
                    zpObj.SendSeek( "REL_TIME", zpObj.storePositionInfo['relTime'])
                    zpObj.SendCommandWait()
                if zpObj.storeMediaInfo['transportstate'] == "Playing": 
                    zpObj.SendPlay()
                globalZPList[uuid].storeMediaInfo['mediaRestore'] = False
            #except:
            #    print "Run StoreCurrentTrackState before running this action" 
    
    def Configure(self, restoreDelay=10):
        panel = eg.ConfigPanel()
        mySizer = wx.GridBagSizer(3, 2)
        mySizer.AddGrowableRow(3)
        mySizer.AddGrowableCol(0)
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        text1 = '''select the time it takes for your notification to play in seconds. \nYour SONOS system will be restored after this time has passed.'''
        TextZPSelect = wx.StaticText(panel, -1, "Enter restore time delay")
        TextSelect = wx.StaticText(panel, -1, text1)
        try:
            DropDown = wx.SpinCtrl(panel, -1, str(restoreDelay), (0,0), (100,20))
            DropDown.SetRange(1,300)
        except:
            DropDown = wx.SpinCtrl(panel, -1, '1', (0,0), (100,20))
            DropDown.SetRange(1,300)
        
        mySizer.Add(TextZPSelect, (0,0), (1,2), flag = wx.EXPAND)
        mySizer.Add(DropDown, (2,0), (1,2), flag = (wx.ALIGN_CENTER | wx.ALIGN_RIGHT))
        mySizer.Add(TextSelect, (1,0), flag = wx.EXPAND)
        while panel.Affirmed():
            Final = DropDown.GetValue()
            panel.SetResult(
                Final
            )     
     
class NotificationLineIn(eg.ActionBase):
    name = "Set SONOS player to the Line-In of the selected Zone Player"
    description = "Sets player or group to Line In "

    def __call__(self, linein=""):
        trackuri = "x-rincon-stream:" + linein
        for uuid, zpObj in globalZPList.iteritems():
            if uuid not in globalZPList:
                print "!!! zone player no longer in globalZPList (not found on network) !!!"
            elif zpObj.storeMediaInfo['mediaRestore']:
                coordinator = globalZPList[uuid].coordinator
                globalZPList[coordinator].SendSetAVTransportURI(trackuri)
        #send play to all
        for uuid, zpObj in globalZPList.iteritems():    
            if zpObj.storeMediaInfo['mediaRestore']:
                coordinator = globalZPList[uuid].coordinator
                globalZPList[coordinator].SendCommandWait()
                globalZPList[coordinator].SendPlay()
                if globalDebug >= 1:
                    print "set TrackURI to "+ trackuri + " in " + globalZPList[uuid].name
          
    def Configure(self, linein=""):
        title = '''Select a Zone Player with a Line In\nNOTE: Make sure to select a ZP that has a Line In and something is plugged into it.'''
        winSelectGUI = WindowUUIDSelect(linein, title)

        
def SendNotificationTrackURI(trackuri):
        #make sure track is formatted correctly
        #x-rincon-mp3radio is to stream MP3 from the web
        #x-file-cifs is to stream a local file
        trackuri = trackuri.replace(" ", "%20").replace("\\","/")
        if trackuri[0:2] == "//": #local network file vs http://
            trackuri = "x-file-cifs:" + trackuri
        elif trackuri[0:5] == "http:":
            trackuri = "x-rincon-mp3radio:" + trackuri[5:]
        #set all URI first
        for uuid, zpObj in globalZPList.iteritems():
            if uuid not in globalZPList:
                print "!!! zone player no longer in globalZPList (not found on network) !!!"
            elif zpObj.storeMediaInfo['mediaRestore']:
                coordinator = globalZPList[uuid].coordinator
                globalZPList[coordinator].SendSetAVTransportURI(trackuri)
        #send play to all
        for uuid, zpObj in globalZPList.iteritems():    
            if zpObj.storeMediaInfo['mediaRestore']:
                coordinator = globalZPList[uuid].coordinator
                globalZPList[coordinator].SendCommandWait()
                globalZPList[coordinator].SendPlay()
                globalZPList[coordinator].SendCommandWait()
                if globalDebug >= 1:
                    print "set TrackURI to "+ trackuri + " in " + globalZPList[uuid].name   
        

class NotificationTrackURI(eg.ActionBase):
    name = "Send SONOS TrackURI with specified Track Link and then send Play"
    description = "Sets current track to track listed "

    def __call__(self, trackuri=""):
        SendNotificationTrackURI(trackuri)     

    def Configure(self, trackuri=""):
        title = "Enter the track address that should play as the notification"
        text1 = '''URI can be a local file or from the cloud.\n\nPlace Track URI here:'''
        text2 = '''NOTE: track must be accessible by SONOS and in the proper format to play'''
        winSelectGUI = WindowUUIDText(trackuri, title, text1, text2)

 
class NotificationGoogleTTS(eg.ActionBase):
    name = "Google TTS Notifications"
    description = "Use Google's TTS API to play notificaitons over SONOS"

    def __call__(self, tts="", language="en"):
        if len(tts)>99:
            text = tts[0:99]
        else:
            text = tts
        trackuri = "http://translate.google.com/translate_tts?ie=UTF-8&q=%s&tl=%s&total=1&idx=0&textlen=%s&prev=input" % (text, language, len(text))
        SendNotificationTrackURI(trackuri)
              
    def Configure(self, tts="", language="en"):
        title = "Enter the text you want SONOS to say"
        text2 = '''Enter the language to speak the text in.'''
        text1 = '''NOTE: Google restricts this to a max of 100 characters.\nThe amount of times the service can be used per day is also restricted\n'''
        panel = eg.ConfigPanel()
        mySizer = wx.GridBagSizer(5, 1)
        mySizer.AddGrowableRow(3)
        mySizer.AddGrowableCol(0)
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        TextZPSelect = wx.StaticText(panel, -1, title)
        Text1Select = wx.StaticText(panel, -1, text1)
        Text2Select = wx.StaticText(panel, -1, text2)
        ttsBox =  wx.TextCtrl(panel, -1, tts)
        lnBox =  wx.TextCtrl(panel, -1, language)
        
        mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
        mySizer.Add(ttsBox, (1,0), flag = wx.EXPAND)
        mySizer.Add(Text1Select, (2,0), flag = wx.EXPAND)
        mySizer.Add(Text2Select, (3,0), flag = wx.EXPAND)
        mySizer.Add(lnBox, (4,0), flag = wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                ttsBox.GetValue(),
                lnBox.GetValue()
            ) 
        
          
        
class PlayLineIn(eg.ActionBase):
    name = "Set SONOS player to the Line-In of the selected Zone Player"
    description = "Sets player or group to Line In "

    def __call__(self, uuid="", linein=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        trackuri = "x-rincon-stream:" + linein
        globalZPList[coordinator].SendSetAVTransportURI(trackuri)
        globalZPList[coordinator].SendPlay()
        if globalDebug >= 1:
            print "set TrackURI to "+ trackuri + " in " + globalZPList[uuid].name
          
    def Configure(self, uuid="", linein=""):
        title = "Select a Zone Player..."
        text1 = '''Select a Zone Player with a Line In\n only models with Line-in are listed'''
        text2 = '''NOTE: SONOS will accept this command all the time, \nbut if nothing is plugged into it, SONOS will clear the \n currently playing track '''
        winSelectGUI = WindowUUIDSelecttwo(uuid, linein, title, text1, text2, LINEINMODELS)

                
class PlayTVonPlayBar(eg.ActionBase):
    #has to be sent to play bar regardless if it's grouped or not. 
    name = "Set SONOS PlayBar to the TV source"
    description = "Sets PlayBar to TV source"

    def __call__(self, uuid=""):
        if uuid == "":
            print "Please select a PlayBar to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        trackuri = "x-sonos-htastream:" + uuid + ":spdif"
        globalZPList[uuid].SendSetAVTransportURI(trackuri)
        globalZPList[uuid].SendPlay()
        if globalDebug >= 1:
            print "set TrackURI to "+ trackuri + " in " + globalZPList[uuid].name
          
    def Configure(self, uuid=""):
        title = '''Select a PlayBar,\nOnly PlayBars are listed'''
        winSelectGUI = WindowUUIDSelect(uuid, title, TVINMODELS)  
        
        

class PlayTrackURI(eg.ActionBase):
    name = "Send SONOS TrackURI with specified Track Link and then send Play"
    description = "Sets current track to track listed "

    def __call__(self, uuid="", trackuri=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        #make sure track is formatted correctly
        #x-rincon-mp3radio is to stream MP3 from the web
        #x-file-cifs is to stream a local file
        trackuri = trackuri.replace(" ", "%20").replace("\\","/")
        if trackuri[0:2] == "//": #local network file vs http://
            trackuri = "x-file-cifs:" + trackuri
        elif trackuri[0:5] == "http:":
            trackuri = "x-rincon-mp3radio:" + trackuri[5:]
        coordinator = globalZPList[uuid].coordinator
        globalZPList[coordinator].SendSetAVTransportURI(trackuri)
        globalZPList[coordinator].SendCommandWait()
        globalZPList[coordinator].SendPlay()
        if globalDebug >= 1:
            print "set TrackURI to "+ trackuri + " in " + globalZPList[uuid].name
          
    def Configure(self, uuid="", trackuri=""):
        title = "Select a Zone Player..."
        text1 = '''Place Track URI here:\n'''
        text2 = '''NOTE: track must be accessible by SONOS and in the proper format to play'''
        winSelectGUI = WindowUUIDSelectText(uuid, trackuri, title, text1, text2)
       
class StartPlayList(eg.ActionBase):
    name = "Start a playlist from the SONOS Favorites list"
    description = "sends command to start playlist. "

    def __call__(self, uuid="", track="", dscr="", uri="", urimetadata="", upnpclass="", isplaylist=""):
        if uuid == "":
            print "Please select a ZP to send command to."
            return
        if uuid not in globalZPList:
            print "!!! zone player no longer in globalZPList (not found on network) !!!"
            return
        coordinator = globalZPList[uuid].coordinator
        if isplaylist:
            globalZPList[coordinator].SendRemoveAllTracksFromQueue()
            globalZPList[coordinator].SendCommandWait()#wait for previous command to complete
            globalZPList[coordinator].SendAddURIToQueue(uri, urimetadata)
            globalZPList[coordinator].SendSetAVTransportURI("x-rincon-queue:"+coordinator+"#0", "")
            if globalDebug >= 1:
                print "Starting Playlist "+ track + " in " + globalZPList[uuid].name
        else:
            globalZPList[coordinator].SendSetAVTransportURI(uri, urimetadata)
            if globalDebug >= 1:
                print "Starting Station " + track + " in " + globalZPList[uuid].name
        globalZPList[coordinator].SendCommandWait()#wait for previous command to complete
        globalZPList[coordinator].SendPlay()
       
    def ResponseReceived(self):
        if globalDebug >= 1:
            print "getFavPlayList Socket ResponseReceived callback Success"
        self.favPlayListReceived = True
        
    def Configure(self, uuid="", track="", dscr="", uri="", urimetadata="", upnpclass="", isplaylist=""):
        try:
            panel = eg.ConfigPanel()
            #get SONOS Favorites...(make sure not to select a bridge by ignoring invisible zps)
            if globalDebug >= 1:
                print "looking for ZP that is not invisible..."
            self.favPlayListReceived = False
            for k, v in globalZPList.iteritems():
                    if v.invisible == 0: #find the first non invisible ZP
                        tempuuid = k
                        break
            if globalDebug >= 0:
                print "Getting Favorites List from %s at %s" % (globalZPList[tempuuid].name,globalZPList[tempuuid].ip)
            globalZPList[tempuuid].SendGetFavPlayList(self.ResponseReceived)
            if globalDebug >= 1:
                print "Waiting for SendGetFavPlayList response..."
            globalZPList[tempuuid].SendCommandWait()#wait for previous command to complete
            try: 
                presets = globalZPList[tempuuid].favPlayList
            except:
                print "ERROR getting favPlayLists..."
                return
            
            mySizer = wx.GridBagSizer(5, 1)
            mySizer.AddGrowableRow(4)
            mySizer.AddGrowableCol(0)
            
            panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
            
            TextZPSelect = wx.StaticText(panel, -1, "Select a Zone Player from the list below...")
            TextPLSelect = wx.StaticText(panel, -1, "Select a Playlist or Station from your SONOS Favorites list...")
            TextPLNote = wx.StaticText(panel, -1, '''Make sure to add any station you want to select to the SONOS favorites list before opening this dialogue.\nAlso note when the action is triggered, if it's a playlist it will replace the current queue''')
            #============ dropdown ==============
            ChoiceList = []
            if globalZPList:
                for k, v in globalZPList.iteritems():
                    if v.invisible == 0:
                        ChoiceList.append(v.name + "-" + k + "-" + v.ip)
                        #ChoiceList.append(k)
                if ChoiceList: 
                    ChoiceList.sort()
                else:
                    ChoiceList.append("-no Zone Players found...-")
                ZPDropDown =  wx.Choice(panel, -1, choices=ChoiceList)
            else:
                print "!! - No SONOS ZPs, search network again"
                return
            #Identify the device and set dropdown to correct position
            p = 0
            try:
                p = ChoiceList.index(globalZPList[uuid].name + "-" + uuid + "-" + globalZPList[uuid].ip)
                ZPDropDown.SetSelection(p)
            except: #ValueError:
                ZPDropDown.SetSelection(0)
            #============ end dropdown ==============
            
            #============ dropdown ==============
            ChoiceList = []
            for k, v in presets.iteritems():
                ChoiceList.append(v['description'] + ": " + k)
            PLDropDown =  wx.Choice(panel, -1, choices=ChoiceList) # (0,0), (60,20)
            #Identify the device and set dropdown to correct position
            p = 0
            try:
                p = ChoiceList.index(dscr + ": " + track)
                PLDropDown.SetSelection(p)
            except: #ValueError:
                PLDropDown.SetSelection(0)
            #============ end dropdown ==============
            mySizer.Add(TextZPSelect, (0,0), flag = wx.EXPAND)
            mySizer.Add(ZPDropDown, (1,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
            mySizer.Add(TextPLSelect, (2,0), flag = wx.EXPAND)
            mySizer.Add(TextPLNote, (3,0), flag = wx.EXPAND)
            mySizer.Add(PLDropDown, (4,0), flag = (wx.ALIGN_TOP | wx.EXPAND))
            while panel.Affirmed():
                FinalChoice = ZPDropDown.GetStringSelection()
                FinalPL = PLDropDown.GetStringSelection().split(": ")[1]
                panel.SetResult(
                    FinalChoice.split("-")[-2], #save only the uuid from the list.
                    FinalPL,
                    presets[FinalPL]['description'],
                    presets[FinalPL]['uri'],
                    presets[FinalPL]['urimetadata'],
                    presets[FinalPL]['upnpclass'],
                    presets[FinalPL]['isplaylist']                
                ) 
        except Exception, e:
            trigger = "ERROR StartPlayList: something went wrong "+str(e)
            eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
            print trigger

#class TestCmd(eg.ActionBase):
#    name = "Send SONOS TestCmd"
#    description = "sends command to test."
#
#    def __call__(self, uuid=""):
#        if uuid == "":
#            print "Please select a ZP to send command to."
#            return
#        if uuid not in globalZPList:
#            print "!!! zone player no longer in globalZPList (not found on network) !!!"
#            return
#        globalZPList[uuid].SendGetFavPlayList(self.ResponseReceived)
#    
#    def ResponseReceived():
#        print "TestCmd Response Received" 
#        
#    def Configure(self, uuid=""):
#        winSelectGUI = WindowUUIDSelect(uuid)            
# 
#===========================================================================================
#===================  Weather ==============================================================
#===========================================================================================
def GetWOEID(searchText):
    url = "query.yahooapis.com"
    searchText = searchText.replace(",","")
    paramQ = 'select * from geo.places where text="%s"' % searchText
    params = urllib.urlencode({'q':paramQ, 'format':'xml'})
    path = "/v1/public/yql?%s" % params
    headers = {"Content-Type": "text/xml; charset=UTF-8"}
    woeidDict = {}
    try:
        woeidXML = httpRequest(url, 80, path, "GET", headers, "").read()
        if globalDebug >= 2:
            print "woeidXML:\n%s" % woeidXML
        xml = parseString(woeidXML)
        woeidList = xml.getElementsByTagName('woeid')
        local2List = xml.getElementsByTagName('locality2')
        local1List = xml.getElementsByTagName('locality1')
        admin3List = xml.getElementsByTagName('admin3')
        admin2List = xml.getElementsByTagName('admin2')
        admin1List = xml.getElementsByTagName('admin1')
        countryList = xml.getElementsByTagName('country')
        for index, woeidElement in enumerate(woeidList):
            woeid = woeidElement.firstChild.nodeValue
            woeidDict[woeid]= []
            try:
                woeidDict[woeid].append(local2List[index].firstChild.nodeValue)
            except:
                pass
            try:
                woeidDict[woeid].append(local1List[index].firstChild.nodeValue)
            except:
                pass
            try:
                woeidDict[woeid].append(admin3List[index].firstChild.nodeValue)
            except:
                pass
            try:
                woeidDict[woeid].append(admin2List[index].firstChild.nodeValue)
            except:
                pass
            try:
                woeidDict[woeid].append(admin1List[index].firstChild.nodeValue)
            except:
                pass
            try:
                woeidDict[woeid].append(countryList[index].firstChild.nodeValue)
            except:
                pass
    except Except, e:
        trigger = "Get WOEID XML Error: "+str(e)
        eg.TriggerEvent("ERROR", prefix='SONOS', payload=trigger)
        if globalDebug >= 1:
            print trigger
    return woeidDict

def GetWeatherForcast(woeid, units):
    print "requesting weather from yahoo for WOEID: " + woeid
    url = "weather.yahooapis.com"
    params = urllib.urlencode({'w':woeid, 'u':units})
    path = "/forecastrss?%s" % params
    headers = {"Content-Type": "text/xml; charset=UTF-8"}
    woeidXML = httpRequest(url, 80, path, "GET", headers, "").read()
    xml = parseString(woeidXML)
    forecast = {} #temp,text, todayshigh, todayslow, todaystext
    forecast['temp'] = xml.getElementsByTagName('yweather:condition')[0].getAttribute('temp')
    forecast['code'] = xml.getElementsByTagName('yweather:condition')[0].getAttribute('code')
    try:
        forecast['text'] = CONDITIONCODES[forecast['code']]
    except:
        forecast['text'] = xml.getElementsByTagName('yweather:condition')[0].getAttribute('text')
    forecast['todayshigh'] = xml.getElementsByTagName('yweather:forecast')[0].getAttribute('high')
    forecast['todayslow'] = xml.getElementsByTagName('yweather:forecast')[0].getAttribute('low')
    forecast['todayscode'] = xml.getElementsByTagName('yweather:forecast')[0].getAttribute('code')
    try:
        forecast['todaystext'] = CONDITIONCODES[forecast['todayscode']]
    except:
        forecast['todaystext'] = xml.getElementsByTagName('yweather:forecast')[0].getAttribute('text')
    return forecast

    
class LocSearchDialog(wx.Dialog):
    
    def __init__(self, parent, id, title, varwoeid, searchText):
        self.woeid = varwoeid
        self.location = ''
        searchAgain = False
        woeidDict = GetWOEID(searchText)
        ChoiceList = []
        woeidList = []
        for woeid, list in woeidDict.iteritems():
            woeidList.append(woeid)
            ChoiceList.append(', '.join(list))
        wx.Dialog.__init__(self, parent, id, title) #size=(250, 146)
        panel = wx.Panel(self, -1)
        #panel.SetBackgroundColour("white")
        vbox = wx.BoxSizer(wx.VERTICAL)
        if len(ChoiceList) == 0:
            ChoiceList.append("No locations found, please try again")
            searchAgain = True
        radioBox =  wx.RadioBox(panel, -1, "select your location", choices=ChoiceList, style=wx.RA_SPECIFY_COLS, majorDimension=1)
        try: 
            key = woeidList.index(self.woeid)
            radioBox.SetSelection(key)
        except:
            radioBox.SetSelection(0)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        if not searchAgain:
            selectButton = wx.Button(self, -1, 'Select', size=(70, 30))
        cancelButton = wx.Button(self, -1, 'Cancel', size=(70, 30))
        if not searchAgain:
            hbox.Add(selectButton, 1)
        hbox.Add(cancelButton, 1, wx.LEFT, 5)
        
        vbox.AddSpacer(15)
        vbox.Add(panel, 0, wx.ALIGN_CENTER, 5 )
        vbox.AddSpacer(15)
        vbox.Add(hbox, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        
        self.SetAutoLayout(True)
        self.SetSizerAndFit(vbox)
        self.Layout()

        def CancelButton(event):
            self.Destroy()
        
        def OKButton(event):
            if globalDebug >= 1:
                print "%s" % woeidList
                print "WOEID: %s Location: %s" % (woeidList[radioBox.GetSelection()],ChoiceList[radioBox.GetSelection()])
            self.woeid = woeidList[radioBox.GetSelection()]
            self.location = ChoiceList[radioBox.GetSelection()]
            self.Destroy()
        
        cancelButton.Bind(wx.EVT_BUTTON, CancelButton)
        if not searchAgain:
            selectButton.Bind(wx.EVT_BUTTON, OKButton)
        
class NotificationWeather(eg.ActionBase):
    name = "Get Weather"
    description = "Get the current weather and forecast for the day based on location entered."
    classwoeid = ""
    searchText = ""
    
    def WoeidResponse(self, data):
        print data
    
    def __call__(self, woeid="", location="", units="f"):
        self.classwoeid = woeid
        if woeid == "":
            print "Search for your location and select it from the list and try again"
            return
        if globalDebug >= 1:
            print "WOEID: %s" % self.classwoeid
            print "location: %s units: %s" % (location,units)
        weather = GetWeatherForcast(woeid, units)
        current = "The current weather is %s degrees and %s" % (weather['temp'], weather['text'])
        forecast = "Todays high will be %s degrees and %s" % (weather['todayshigh'], weather['todaystext'])
        print current
        print forecast
        print "total length: %s" % len(current+forecast)
        #trackuri = "http://translate.google.com/translate_tts?ie=UTF-8&q=%s&tl=%s&total=1&idx=0&textlen=%s&prev=input" % (current, 'en', len(current))
        #SendNotificationTrackURI(trackuri)
        #time.sleep(5)
        trackuri = "http://translate.google.com/translate_tts?ie=UTF-8&q=%s&tl=%s&total=1&idx=0&textlen=%s&prev=input" % (forecast, 'en', len(forecast))
        SendNotificationTrackURI(trackuri)
        
        info = "temp:%s, units:%s, condition:%s" % (weather['temp'], units, weather['text'])
        eg.TriggerEvent("CurrentConditions", prefix='WEATHER', payload=info)
        info = "high:%s, low:%s, units:%s, condition:%s" % (weather['todayshigh'], 
                                                            weather['todayslow'],
                                                            units, 
                                                            weather['todaystext']
                                                            )
        eg.TriggerEvent("DayForecast", prefix='WEATHER', payload=info)
        eg.TriggerEvent("Today", prefix='WEATHER', payload=weather)
        
    def OnSearchButton(self, event):
        self.selectLocation = LocSearchDialog(None, -1, 'Select your location...', self.classwoeid, self.locationBox.GetValue())
        self.selectLocation.ShowModal()
        self.classwoeid = self.selectLocation.woeid
        self.searchText = self.selectLocation.location
        if self.searchText != '':
            self.locationBox.SetValue(self.searchText)
        #PopulateDeviceList(wx.CommandEvent())
    
    def Configure(self, woeid="", location="", units="f"):
        self.classwoeid = woeid
        title = "***BETA*** This action is still under development and will change\nGet and announce the current weather\n"
        text1 = '''Enter town, state, country, address, zipcode, or landmark'''
        text2 = '''NOTE: uses Yahoo location API''' #and will select first location found \n Press test to verify your location is correct.
        text3 = '''Select Units: Fahrenheit or Celsius'''
        panel = eg.ConfigPanel()
        mySizer = wx.GridBagSizer(5, 3)
        mySizer.AddGrowableRow(3)
        mySizer.AddGrowableCol(0)
        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)
        TextZPSelect = wx.StaticText(panel, -1, title)
        Text1Select = wx.StaticText(panel, -1, text1)
        Text2Select = wx.StaticText(panel, -1, text2)
        Text3Select = wx.StaticText(panel, -1, text3)
        self.locationBox =  wx.TextCtrl(panel, -1, location)
        searchButton = wx.Button(panel, -1, "Search")
        ChoiceList = ['f','c']
        unitsBox =  wx.Choice(panel, -1, choices=ChoiceList)
        #Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(units)
            unitsBox.SetSelection(p)
        except: #ValueError:
            unitsBox.SetSelection(0) 
        mySizer.Add(TextZPSelect, (0,0),(1,3), flag = wx.EXPAND)
        mySizer.Add(self.locationBox, (2,0),(1,3), flag = wx.EXPAND)
        mySizer.Add(Text1Select, (1,0),(1,3), flag = wx.EXPAND)
        mySizer.Add(Text2Select, (3,0),(1,1), flag = wx.EXPAND)
        mySizer.Add(searchButton, (3,2),(1,1), flag = wx.ALIGN_RIGHT)
        mySizer.Add(unitsBox, (4,2), flag = wx.ALIGN_CENTER)
        mySizer.Add(Text3Select, (4,1), flag = wx.ALIGN_LEFT)
        
        searchButton.Bind(wx.EVT_BUTTON, self.OnSearchButton)
        while panel.Affirmed():
            panel.SetResult(
                self.classwoeid,
                self.locationBox.GetValue(),
                unitsBox.GetStringSelection()
            )
#===================================================================================
#====================  Weather End =================================================
#===================================================================================
 
ACTIONS = (
    #(SearchForSonosZPs,"SearchForSonosZPs","SearchForSonosZPs","SearchForSonosZPs.", None),
    (SetZoneName,"SetZoneName","SetZoneName","Change ZP Name.", None),
    (Play,"Play","Play","Send Play to ZonePlayer.", None),
    (Pause,"Pause","Pause","Send Pause to ZonePlayer.", None),
    (PauseAll,"PauseAll","PauseAll","Send PauseAll to ZonePlayers.", None),
    (Stop,"Stop","Stop","Send Stop to ZonePlayer.", None),
    (Next,"Next","Next","Send Next to ZonePlayer.", None),
    (Previous,"Previous","Previous","Send Previous to ZonePlayer.", None),
    (VolumeAdjust,"VolumeAdjust","VolumeAdjust","VolumeAdjust Sonos.", None),
    (VolumeSet,"VolumeSet","VolumeSet","VolumeSet Sonos.", None),
    (MuteOn,"MuteOn","MuteOn","MuteOn Sonos.", None),
    (MuteOff,"MuteOff","MuteOff","MuteOff Sonos.", None),
    (GroupVolumeAdjust,"GroupVolumeAdjust","GroupVolumeAdjust","GroupVolumeAdjust Sonos.", None),
    (GroupVolumeSet,"GroupVolumeSet","GroupVolumeSet","GroupVolumeSet Sonos.", None),
    (GroupMuteOn,"GroupMuteOn","GroupMuteOn","GroupMuteOn Sonos.", None),
    (GroupMuteOff,"GroupMuteOff","GroupMuteOff","GroupMuteOff Sonos.", None),
    (MuteAllOn,"MuteAllOn","MuteAllOn","MuteAll On Sonos.", None),
    (MuteAllOff,"MuteAllOff","MuteAllOff","Mute All Off Sonos.", None),
    (StartPlayList, "StartPlayList","StartPlayList","Start Playlist", None),
    (SetPlayMode, "SetPlayMode", "SetPlayMode", "Set Play Mode", None),
    (SetCrossfade, "SetCrossfade", "SetCrossfade", "Set Crossfade Mode", None),
    (SetSleepTimer, "SetSleepTimer", "SetSleepTimer", "Set Sleep Timer Value", None),
    (PlayTrackURI, "PlayTrackURI", "PlayTrackURI", "Start playing specified track URI", None),
    (PlayLineIn, "PlayLineIn", "PlayLineIn", "Select and Play Line-In", None),
    (PlayTVonPlayBar, "PlayTVonPlayBar", "PlayTVonPlayBar", "Select TV input from PlayBar", None),
    (GroupZPs,"GroupZPs","GroupZPs","Group Selected Zone Players.", None),
    (UnGroup,"UnGroup","UnGroup","Send UnGroup to ZonePlayer.", None),
    (NotificationStart, "NotificationStart", "NotificationStart", "Execute before notifications, stores State of ZPs", None),
    (NotificationRestore, "NotificationRestore", "NotificationRestore", "Restore State after Notifications", None),
    (NotificationLineIn, "NotificationLineIn", "NotificationLineIn", "Play notification through Line-In of a ZP", None),
    (NotificationTrackURI, "NotificationTrackURI", "NotificationTrackURI", "Play notification from a location", None),
    (NotificationWeather, "NotificationWeather", "NotificationWeather", "Play notification announcing the weather", None),
    (NotificationGoogleTTS, "NotificationGoogleTTS", "NotificationGoogleTTS", "Play notification using Google TTS API", None)
    #(TestCmd, "TestCmd", "TestCmd", "TestCmd", None)
    #(WhatstheWeather, "WhatstheWeather", "WhatstheWeather", "Play current weather forecast over SONOS", None)
)

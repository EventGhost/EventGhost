import xml.dom.minidom
from xml.dom.minidom import parseString
import httplib
from httplib import responses
from httplib import HTTPSConnection
from httplib import HTTPConnection
from urllib import urlencode
from urllib2 import base64
import threading
import hashlib
import binascii
import time
from threading import Event
import wx
from hashlib import md5



eg.RegisterPlugin(
    name = "Dlink-DIR655 Router Status",
    version = "0.1.4",
    author = "Torbjorn Westerlund",
    guid = "{A4F0DEFE-4E0B-47F3-A565-AD72C7A4E270}",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAKBmlUWHRYTUw6Y29tLmFkb2JlLnht"
        "cAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQi"
        "Pz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1Q"
        "IENvcmUgNS4wLWMwNjAgNjEuMTM0Nzc3LCAyMDEwLzAyLzEyLTE3OjMyOjAwICAgICAgICAiPgog"
        "PHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50"
        "YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wUmln"
        "aHRzPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvcmlnaHRzLyIKICAgIHhtbG5zOmRjPSJo"
        "dHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgIHhtbG5zOklwdGM0eG1wQ29yZT0i"
        "aHR0cDovL2lwdGMub3JnL3N0ZC9JcHRjNHhtcENvcmUvMS4wL3htbG5zLyIKICAgIHhtbG5zOnBs"
        "dXNfMV89Imh0dHA6Ly9ucy51c2VwbHVzLm9yZy9sZGYveG1wLzEuMC8iCiAgICB4bWxuczp4bXA9"
        "Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25z"
        "LmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUu"
        "Y29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgIHhtcFJpZ2h0czpNYXJrZWQ9IlRy"
        "dWUiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMTEtMDEtMjVUMTM6NTU6MDcrMDE6MDAiCiAgIHht"
        "cE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6RDE3RTA1NTY4MjI4RTAxMTk4OUNDMEExQUQwMkI1QzIi"
        "CiAgIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6RDE3RTA1NTY4MjI4RTAxMTk4OUNDMEExQUQw"
        "MkI1QzIiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDpEMTdFMDU1NjgyMjhF"
        "MDExOTg5Q0MwQTFBRDAyQjVDMiI+CiAgIDx4bXBSaWdodHM6VXNhZ2VUZXJtcz4KICAgIDxyZGY6"
        "QWx0PgogICAgIDxyZGY6bGkgeG1sOmxhbmc9IngtZGVmYXVsdCI+Q3JlYXRpdmUgQ29tbW9ucyBB"
        "dHRyaWJ1dGlvbi1Ob25Db21tZXJjaWFsIGxpY2Vuc2U8L3JkZjpsaT4KICAgIDwvcmRmOkFsdD4K"
        "ICAgPC94bXBSaWdodHM6VXNhZ2VUZXJtcz4KICAgPGRjOmNyZWF0b3I+CiAgICA8cmRmOlNlcT4K"
        "ICAgICA8cmRmOmxpPkdlbnRsZWZhY2UgY3VzdG9tIHRvb2xiYXIgaWNvbnMgZGVzaWduPC9yZGY6"
        "bGk+CiAgICA8L3JkZjpTZXE+CiAgIDwvZGM6Y3JlYXRvcj4KICAgPGRjOmRlc2NyaXB0aW9uPgog"
        "ICAgPHJkZjpBbHQ+CiAgICAgPHJkZjpsaSB4bWw6bGFuZz0ieC1kZWZhdWx0Ij5XaXJlZnJhbWUg"
        "bW9ubyB0b29sYmFyIGljb25zPC9yZGY6bGk+CiAgICA8L3JkZjpBbHQ+CiAgIDwvZGM6ZGVzY3Jp"
        "cHRpb24+CiAgIDxkYzpzdWJqZWN0PgogICAgPHJkZjpCYWc+CiAgICAgPHJkZjpsaT5jdXN0b20g"
        "aWNvbiBkZXNpZ248L3JkZjpsaT4KICAgICA8cmRmOmxpPnRvb2xiYXIgaWNvbnM8L3JkZjpsaT4K"
        "ICAgICA8cmRmOmxpPmN1c3RvbSBpY29uczwvcmRmOmxpPgogICAgIDxyZGY6bGk+aW50ZXJmYWNl"
        "IGRlc2lnbjwvcmRmOmxpPgogICAgIDxyZGY6bGk+dWkgZGVzaWduPC9yZGY6bGk+CiAgICAgPHJk"
        "ZjpsaT5ndWkgZGVzaWduPC9yZGY6bGk+CiAgICAgPHJkZjpsaT50YXNrYmFyIGljb25zPC9yZGY6"
        "bGk+CiAgICA8L3JkZjpCYWc+CiAgIDwvZGM6c3ViamVjdD4KICAgPGRjOnJpZ2h0cz4KICAgIDxy"
        "ZGY6QWx0PgogICAgIDxyZGY6bGkgeG1sOmxhbmc9IngtZGVmYXVsdCI+Q3JlYXRpdmUgQ29tbW9u"
        "cyBBdHRyaWJ1dGlvbi1Ob25Db21tZXJjaWFsIGxpY2Vuc2U8L3JkZjpsaT4KICAgIDwvcmRmOkFs"
        "dD4KICAgPC9kYzpyaWdodHM+CiAgIDxJcHRjNHhtcENvcmU6Q3JlYXRvckNvbnRhY3RJbmZvCiAg"
        "ICBJcHRjNHhtcENvcmU6Q2lVcmxXb3JrPSJodHRwOi8vd3d3LmdlbnRsZWZhY2UuY29tIi8+CiAg"
        "IDxwbHVzXzFfOkltYWdlQ3JlYXRvcj4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAg"
        "cGx1c18xXzpJbWFnZUNyZWF0b3JOYW1lPSJnZW50bGVmYWNlLmNvbSIvPgogICAgPC9yZGY6U2Vx"
        "PgogICA8L3BsdXNfMV86SW1hZ2VDcmVhdG9yPgogICA8cGx1c18xXzpDb3B5cmlnaHRPd25lcj4K"
        "ICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgcGx1c18xXzpDb3B5cmlnaHRPd25lck5h"
        "bWU9ImdlbnRsZWZhY2UuY29tIi8+CiAgICA8L3JkZjpTZXE+CiAgIDwvcGx1c18xXzpDb3B5cmln"
        "aHRPd25lcj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAg"
        "ICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6"
        "RDE3RTA1NTY4MjI4RTAxMTk4OUNDMEExQUQwMkI1QzIiCiAgICAgIHN0RXZ0OndoZW49IjIwMTEt"
        "MDEtMjVUMTM6NTU6MDcrMDE6MDAiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii9tZXRhZGF0YSIvPgog"
        "ICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8"
        "L3JkZjpSREY+CjwveDp4bXBtZXRhPgo8P3hwYWNrZXQgZW5kPSJyIj8+kDdMIgAAABl0RVh0U29m"
        "dHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAADUSURBVHjarFDBDYMwEONKX0hIDMAjv3xpJugI"
        "bJAROmJhg3aCsAEMAAlnlaD0UREokY6Di23sS5IzjlLKcIkdeAEO3i94TNMkxnGsYwWABWcV4EHD"
        "Ax0rwNgHOKGDF1clpay2yMDg7+CEDloudB1hXy/YNnTQLMM6Jj+wXw6MMQMPOmutKMvyZwzcAQMs"
        "c7pVwC9yK0Zgv/GzUOC9FcPbBzY561Ce5z0RFUfIzrmBsixzLHDjD4g894pckYnJHztEaFjQPTpC"
        "mqY99+LgCoa/lzgLMADoWadHl0geHwAAAABJRU5ErkJggg=="
    ),
    description = (
        "Get notifications about router status."
    ),
    canMultiLoad = True,
)



class Text:
    settingsBox = "Dlink-DIR655 Router Status - Settings"

class Settings:
    password=""
    routerAddress="192.168.0.1"
    useHTTPS=0
    eventFireSensitivity = 15
    stableSignalSeconds = 10
    updateRate = 2.0
    userAgent = "EventGhost"
    eventPrefix = "dir655"
    errorRetryDelay = 5
    gracePeriodSeconds = 5

class Status:
    newFirmware = 0


status = Status
settings = Settings

class Dir655Status(eg.PluginBase):
    text = Text

    def __init__(self):
        password = ""

    def __start__(self, password, routerAddress, useHTTPS, eventFireSensitivity, stableSignalSeconds , updateRate , gracePeriod ):
        settings.password				= password
        settings.routerAddress        	= routerAddress
        settings.useHTTPS             	= useHTTPS
        settings.eventFireSensitivity 	= eventFireSensitivity
        settings.stableSignalSeconds  	= stableSignalSeconds
        settings.updateRate           	= updateRate
        settings.gracePeriodSeconds     = gracePeriod
        self.stopThreadEvent = Event()
        t = RouterCommunicationThread( self.stopThreadEvent )
        t.start()


    def __stop__(self):
        self.stopThreadEvent.set()

    def Configure(self, password="", routerAddress="192.168.0.1", useHTTPS=0, eventFireSensitivity = 15, stableSignalSeconds = 10 , updateRate = 2.0 , disconnectGracePeriod = 5):
        text = self.text
        panel = eg.ConfigPanel()

        passwordCtrl                = panel.TextCtrl(password , style=wx.TE_PASSWORD)
        routerAddressCtrl           = panel.TextCtrl( routerAddress )
        useHTTPS                    = panel.CheckBox( useHTTPS )
        eventFireSensitivityCtrl    = panel.SpinIntCtrl( eventFireSensitivity , min=1, max=100 )
        stableSignalSecondsCtrl     = panel.SpinIntCtrl( stableSignalSeconds , min=1, max=600 )
        updateRateCtrl              = panel.SpinIntCtrl( updateRate , min=0.5 , max=600 )
        disconnectGracePeriodCtrl   = panel.SpinIntCtrl( disconnectGracePeriod , min=1 , max=600 )

        ctrlTexts = [ 'Password' , 'Router Address' , "Use HTTPS" , "Event fire sensitivity" , "Stable signal (sec)" , "Update rate (sec)" , "Disconnect grace period (sec)" ]
        staticTexts = []

        for txt in ctrlTexts:
            newStaticText = panel.StaticText( txt )
            staticTexts.append( newStaticText )

        eg.EqualizeWidths( staticTexts )


        settingsBox = panel.BoxedGroup(
            text.settingsBox,
            (staticTexts[0], passwordCtrl),
            (staticTexts[1], routerAddressCtrl),
            (staticTexts[2], useHTTPS),
            (staticTexts[3], eventFireSensitivityCtrl),
            (staticTexts[4], stableSignalSecondsCtrl),
            (staticTexts[5], updateRateCtrl),
            (staticTexts[6], disconnectGracePeriodCtrl),
        )

        panel.sizer.Add(settingsBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                passwordCtrl.GetValue(),
                routerAddressCtrl.GetValue(),
                useHTTPS.GetValue(),
                eventFireSensitivityCtrl.GetValue(),
                stableSignalSecondsCtrl.GetValue(),
                updateRateCtrl.GetValue(),
                disconnectGracePeriodCtrl.GetValue()
            )

        settings.password		     	= passwordCtrl.GetValue()
        settings.routerAddress	     	= routerAddressCtrl.GetValue()
        settings.useHTTPS		     	= useHTTPS.GetValue()
        settings.eventFireSensitivity   = eventFireSensitivityCtrl.GetValue()
        settings.stableSignalSeconds	= stableSignalSecondsCtrl.GetValue()
        settings.updateRate 			= updateRateCtrl.GetValue()
        settings.gracePeriodSeconds 	= disconnectGracePeriodCtrl.GetValue()

connections = {}

class WifiConnection:
    wifiSid = 'none'
    macAddress = 'none'
    ipAddress = 'none'
    wifiType = 'none'
    wifiRate = 0.0
    wifiQuality = 0
    wifiChannel = 0
    markedForRemoval = 0
    lastReportedQuality = 0
    isStable = 0
    gracePeriodCounter = 0

    stableCounter = 0

    def __init__(self, wifiSid, macAddress , ipAddress , wifiType , wifiRate , wifiQuality ,wifiChannel ):
        #print "Connected to {4} : {0} (ip:{1}) Rate:{2} Quality:{3} Channel:{5}".format( macAddress , ipAddress , wifiRate , wifiQuality , wifiSid , wifiChannel )
        payload = { "quality" : wifiQuality , "ssid" : wifiSid, "ip" : ipAddress , "type" : wifiType, "rate" : wifiRate, "channel" : wifiChannel }
        eg.TriggerEvent( "Wifi.Connected." + macAddress , payload , settings.eventPrefix )
        self.macAddress     = macAddress
        self.wifiSid		= wifiSid
        self.ipAddress   	= ipAddress
        self.wifiType    	= wifiType
        self.wifiRate    	= wifiRate
        self.wifiQuality 	= wifiQuality
        self.wifiChannel 	= wifiChannel


    def Update(self, wifiSid, ipAddress , wifiType , wifiRate , wifiQuality ,wifiChannel ):

        #print "Settings - Update rate : {0} Stable seconds: {1} Sensitivity: {2} ".format( settings.updateRate , settings.stableSignalSeconds , settings.eventFireSensitivity )
        self.gracePeriodCounter = 0
        self.markedForRemoval = 0
        if ( self.wifiSid != wifiSid ):
            self.wifiSid = wifiSid
        if ( self.ipAddress != ipAddress ):
            self.ipAddress = ipAddress
        if ( self.wifiType != wifiType ):
            #print "Wifi type went from {0} to {1}".format( self.wifiType , wifiType )
            self.wifiType = wifiType
        if ( self.wifiRate != wifiRate ):
            #print "Wifi rate went from {0} to {1}".format( self.wifiRate , wifiRate )
            self.wifiRate = wifiRate
        if ( self.wifiQuality != wifiQuality ):
            difference = abs( wifiQuality - self.lastReportedQuality )
            if difference >= settings.eventFireSensitivity:
                #print "{2} Wifi Quality went from {4}({0}) to {1} changed : {3}".format( self.wifiQuality , wifiQuality , self.macAddress , wifiQuality - self.lastReportedQuality , self.lastReportedQuality )
                payload = { "quality" : wifiQuality , "last_reported_quality" : self.lastReportedQuality , "change" : wifiQuality - self.lastReportedQuality }
                eg.TriggerEvent( "Wifi.Quality.Change." + self.macAddress , payload , settings.eventPrefix )
                self.lastReportedQuality = wifiQuality
                self.stableCounter = 0
                self.isStable = 0
            else:
                self.stableCounter += 1
                if self.isStable == 0 and self.stableCounter*settings.updateRate >= settings.stableSignalSeconds:
                    #print "{0} Wifi Quality stable at ~{1}".format( self.macAddress , wifiQuality )
                    payload = { "quality" : wifiQuality }
                    eg.TriggerEvent( "Wifi.Quality.Stable." + self.macAddress , payload , settings.eventPrefix )
                    self.isStable = 1
            self.wifiQuality = wifiQuality
        if ( self.wifiChannel != wifiChannel ):
            print "Wifi channel went from {0} to {1}".format( self.wifiChannel , wifiChannel )
            self.wifiChannel = wifiChannel

    def MarkForRemoval(self):
        self.gracePeriodCounter = self.gracePeriodCounter + 1
        if self.gracePeriodCounter * settings.updateRate >= settings.gracePeriodSeconds:
            self.markedForRemoval = 1

    def IsMarkedForRemoval(self):
        return self.markedForRemoval;

    def NotifyDisconnect(self):
        payload = { "quality" : self.wifiQuality , "ssid" : self.wifiSid, "ip" : self.ipAddress , "type" : self.wifiType, "rate" : self.wifiRate, "channel" : self.wifiChannel }
        eg.TriggerEvent( "Wifi.Disconnected." + self.macAddress , payload , settings.eventPrefix )

class RouterCommunicationThread(threading.Thread):

    def __init__(self,*args):
        self._target = self.Initialize
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

    def parse_new_wifi_assoc(self, response):
        dom = parseString(response)
        if ( dom.firstChild.nodeName != "env:Envelope" ):
            result = self.Login()
            if not result:
                print "Could not login to router."
            return 0
        bodyElement = dom.getElementsByTagName('env:Body')
        nodes = bodyElement[0].childNodes

        # This firmware does not supply the channel nor the SSID
        wifi_channel = 0
        wifi_ssid = 'Unknown'
        currentMacAddress = 'none'
        for node in nodes:
            if node.nodeName == 'mac':  currentMacAddress   = node.firstChild.nodeValue.replace(':' , '' )
            if node.nodeName == 'rate': wifi_rate           = node.firstChild.nodeValue.replace('M','')
            if node.nodeName == 'type': wifi_type           = node.firstChild.nodeValue
            if node.nodeName == 'ip':   wifi_ip_address     = node.firstChild.nodeValue
            if node.nodeName == 'rsi':
                wifi_quality = node.firstChild.nodeValue
                if currentMacAddress != 'none':
                    if not connections.has_key( currentMacAddress ):
                        connections[ currentMacAddress ] = WifiConnection(
                            wifi_ssid,
                            currentMacAddress,
                            wifi_ip_address ,
                            wifi_type ,
                            float( wifi_rate ),
                            int( wifi_quality),
                            int( wifi_channel) )
                    else:
                        connections[ currentMacAddress ].Update(
                            wifi_ssid,
                            wifi_ip_address ,
                            wifi_type ,
                            float( wifi_rate ),
                            int( wifi_quality),
                            int( wifi_channel) )
                    currentMacAddress = 'none'

    def parse_old_wifi_assoc(self, response):
        dom = parseString(response)
        if ( dom.firstChild.nodeName != "wifi_assoc" ):
            #print "Connection timed out to router. Trying to logon again..."
            result = self.Login()
            if not result:
                print "Could not login to router."
            return 0

        macElements = dom.getElementsByTagName('assoc')

        for node in macElements:
            try:
                wifi_macAddress = node.getElementsByTagName('mac')[0].firstChild.nodeValue
                wifi_ssid       = node.getElementsByTagName('ssid')[0].firstChild.nodeValue
                wifi_channel    = node.getElementsByTagName('channel')[0].firstChild.nodeValue
                wifi_rate       = node.getElementsByTagName('rate')[0].firstChild.nodeValue
                wifi_quality    = node.getElementsByTagName('quality')[0].firstChild.nodeValue
                wifi_type       = node.getElementsByTagName('type')[0].firstChild.nodeValue
                wifi_ip_address = node.getElementsByTagName('ip_address')[0].firstChild.nodeValue
                if not connections.has_key( wifi_macAddress ):
                    connections[ wifi_macAddress ] = WifiConnection(
                        wifi_ssid,
                        wifi_macAddress,
                        wifi_ip_address ,
                        wifi_type ,
                        float( wifi_rate ),
                        int( wifi_quality),
                        int( wifi_channel) )
                else:
                    connections[ wifi_macAddress ].Update(
                        wifi_ssid,
                        wifi_ip_address ,
                        wifi_type ,
                        float( wifi_rate ),
                        int( wifi_quality),
                        int( wifi_channel) )
            except Exception, e:
                print "Could not parse WiFi associations element : %s" % e

    def handle_wifi_assoc_reponse(self, response):
        #print "parse:%s" % response
        result = 1
        if status.newFirmware:
            result = self.parse_new_wifi_assoc( response )
        else:
            result = self.parse_old_wifi_assoc( response )

        for conkey in connections.keys():
            if connections[conkey].IsMarkedForRemoval():
                connections[conkey].NotifyDisconnect()
                del connections[conkey]
            else:
                connections[conkey].MarkForRemoval()

        return result

    def parse_login_reponse(self, response):
            #print "parse:%s" % response
            dom = parseString(response)
            codeElement = dom.getElementsByTagName('login')
            for node in codeElement:
                #print node.firstChild.nodeValue
                if node.firstChild.nodeValue == 'error' :
                    return 0
                else:
                    return 1
            return 0

    def SendRequest( self, method, path, args=None , credentials=None ):
            try:
                headers = {
                    'User-Agent': settings.userAgent
                }
                if credentials!= None:
                    headers['Authorization'] = 'Basic %s' % base64.encodestring('%s:%s' % (credentials['username'], credentials['password'])).replace('\n', '')
                if method == "POST":
                    headers['Content-type'] = "application/x-www-form-urlencoded"

                #print headers
                if settings.useHTTPS:
                    http_handler = HTTPSConnection(settings.routerAddress)
                else:
                    http_handler = HTTPConnection(settings.routerAddress)
                if args == None:
                    http_handler.request(method, path, None, headers)
                else:
                    http_handler.request(method, path, urlencode(args), headers)
                resp = http_handler.getresponse()

                #print resp.read()

                return resp;

            except Exception, e:
                eg.PrintError( "DIR-655: Could not send request : {0}".format( e ) )
                return None

    def EnterThreadLoop(self , stopThreadEvent ):
        status.newFirmware = 0
        while not stopThreadEvent.isSet():
            if not status.newFirmware:
                resp = self.SendRequest( "GET" , "/wifi_assoc.xml" )
                if resp.status == httplib.NOT_FOUND:
                    status.newFirmware = 1
            if status.newFirmware:
                resp = self.SendRequest( "GET" , "/device.xml=wireless_list" )
                if resp.status == httplib.NOT_FOUND:
                    eg.PrintError("DIR-655 - Could not get wifi status. Firmware not supported." )
                    return
            if ( self.handle_wifi_assoc_reponse( resp.read() ) ):
                time.sleep(settings.updateRate);
            else:
                time.sleep(settings.errorRetryDelay);

    def Initialize(self, stopThreadEvent ):
        result = self.Login()
        if not result:
            if settings.useHTTPS:
                settings.useHTTPS = 0
                result = self.Login()
                if result:
                    print "WARNING: Failed to login using HTTPS (using HTTP instead). You have to configure the router manually to allow HTTPS connections."
                else:
                    eg.PrintError("DIR-655: Could not login to router. Please re-configure and try again." )
        if result:
            self.EnterThreadLoop( stopThreadEvent )

    def Login(self):
        # Ok, first we have to get the salt, which is sent in the html-response of the root-page
        resp = self.SendRequest( "GET" , "/" )
        if not resp == None:
            responseStr = resp.read()
        else:
            return 0

        salt = ""
        saltDefStr = "var salt = ";
        saltStartIndex = responseStr.find(saltDefStr )
        if saltStartIndex != -1:
            salt = responseStr[saltStartIndex + len(saltDefStr) :saltStartIndex + len(saltDefStr) + 10]
            salt = salt.replace( '"' , '' );

        if salt=="":
            print "Could not find salt in response. Login not possible."
            return 0

        pwd = settings.password;

        # Dlink uses some stupid padding for some reason
        pwdLeftoverPadding = 16 - len(pwd)
        if pwdLeftoverPadding > 0:
            pwd += unichr(1)* pwdLeftoverPadding;

        input = salt + pwd;

        inputLeftoverPadding = 63 - len(input)

        if inputLeftoverPadding > 0:
            input += unichr(1)* inputLeftoverPadding;

        input += unichr(1); # Admin padding :) ... capital U should be added if we want to login as "user"

        m = hashlib.md5()
        m.update( input )
        logonParam = salt + binascii.hexlify( m.digest() )

        #print salt
        #print logonParam

        resp = self.SendRequest( "GET" , "/post_login.xml?hash=" + logonParam )

        try:
            result = self.parse_login_reponse(resp.read())
        except Exception, e:
            print e
            response = 0

        return result

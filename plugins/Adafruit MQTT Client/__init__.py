# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright (C) 2016 Walter Kraembring <krambriw>.
#
###############################################################################
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
#
##############################################################################
#
# Acknowledgement: All credits to:
# Mr Tony DiCola <tony@tonydicola.com> for the Adafruit IO Python Client Library 
# The Eclipse Foundation project for the Eclipse Paho MQTT Python Client library
##############################################################################
# Revision history:
#
# 2016-04-05  Changed looping method
# 2016-03-30  Rewamped again!!!
# 2016-03-22  Rewamped!
# 2016-03-21  Reconnection routines introduced & improved
# 2016-03-16  Avoiding the plugin to hang if Adafruit refuses connection
# 2016-03-08  Adafruit stabilized communication, added events when connected and
#             disconnected
# 2016-03-02  Endless story, trying to improve connection handling. Adafruit
#             made a configuration change to stabilize connections 
# 2016-02-29  Further improved connection error handling
# 2016-02-23  Introduced heart beats to keep connection alive
#             Improved connection error handling
# 2016-02-22  Found a better and simpler way to publish messages
# 2016-02-21  Adafruit-IO MQTT client plugin, first version
##############################################################################


eg.RegisterPlugin(
    name = "Adafruit MQTT Client",
    author = "krambriw",
    version = "0.1.3",
    kind = "other",
    canMultiLoad = True,
    url = "http://www.eventghost.org/forum",
    description = "Connects to Adafruit-IO via MQTT",
    guid = "{2B94CD19-9472-4ACC-8178-7BEA8C10FE03}",
    help = """
        <center><img src="Adafruit.png" /></center>
    """
)

import eg
import time
import os
from threading import Event, Thread

# Import Adafruit IO MQTT client.
from .Adafruit_IO import MQTTClient



class Text:
    adafruitUser = "Adafruit-IO user name: "
    adafruitIOkey = "Adafruit-IO key: "
    adafruitFeedId = "Adafruit-IO feed ID: "
    repeat = "Show repeated events: "
    comms_up = "Communication with Adafruit-IO started..."
    comms_dwn = "Communication with Adafruit-IO stopped..."
    plugin_init = "Please wait, Adafruit-IO MQTT client is starting up..."
    plugin_dwn = "Adafruit-IO MQTT client plugin stopped..."
    plugin_restart = "Please wait, Adafruit-IO MQTT client is restarting..."
    publish_failed = "Failed to publish: "
    connect_failed = "Not connected to Adafruit-IO..."
    connect_failed_waiting = "Not yet connected to Adafruit-IO...please wait"
    diconnect_event = "Event received: client.on_disconnect"

     

class publishMQTTtxt:
    name = "Publish a MQTT message"
    description = ("A MQTT message")
    actionName =  "MQTT publisher name: "
    topicName =   "Feed/Topic: "
    messageName = "Message: "



class Adafruit_IO_MQTT(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddAction(publishMQTT)


    def monitoring(self, mainThreadEvent, client):
        mainThreadEvent.wait(10.0) #Initial wait
        while not mainThreadEvent.isSet(): # Main Loop
            client.loop()
            if client.is_connected():
                mainThreadEvent.wait(0.1)
            else:
                eg.PrintError (self.text.connect_failed_waiting)
                if not mainThreadEvent.isSet():
                    self.reStart()
                mainThreadEvent.wait(5.0)


    def reStart(self):
        print self.text.plugin_restart
        self.__stop__()
        for i in range(0, 200):
            time.sleep(0.05)
        self.__start__(
            self.adafruitUser,
            self.adafruitIOkey,
            self.adafruitFeedId,
            self.repeat
        )


    def __start__(
        self,
        adafruitUser='adafruit io username',
        adafruitIOkey='adafruit io key',
        adafruitFeedId='feed id',
        repeat=False
    ):
        self.adafruitUser = adafruitUser
        self.adafruitIOkey = adafruitIOkey
        self.adafruitFeedId = adafruitFeedId
        self.repeat = repeat
        self.oldEvent = ''
        self.prefix = 'Adafruit_IO'
        self.started = False
        self.client = None
        self.message = []
        self.connectionCntr = 0


        def goInit():
            print self.text.plugin_init         
            # Create an MQTT client instance.
            self.client = None
            self.client = MQTTClient(
                adafruitUser, 
                adafruitIOkey, 
                service_host='io.adafruit.com', 
                service_port=1883
            )
            # Setup the callback functions defined above.
            self.client.on_connect    = connected
            self.client.on_disconnect = disconnected
            self.client.on_message    = message
            # Connect to the Adafruit IO server.
            self.client.connect()
            self.mainThreadEvent = Event()
            self.started = True
            mainThread = Thread(target=self.monitoring, args=(self.mainThreadEvent, self.client,))
            mainThread.start()


        def connected(client):
            if client.is_connected() and self.started:
                self.connectionCntr += 1
                #Start subscribing.
                client.subscribe(adafruitFeedId)
                #print self.text.comms_up
                eg.TriggerEvent(
                    self.text.comms_up,
                    payload = None,
                    prefix=self.prefix
                )
            if not client.is_connected():
                eg.PrintError (self.text.connect_failed)           

   
        def disconnected(client):
            if not client.is_connected() and self.started:
                if self.connectionCntr > 0:
                    self.connectionCntr -= 1
                self.started = False
                LogToFile(self.text.diconnect_event)
                #print self.text.comms_dwn
                eg.TriggerEvent(
                    self.text.comms_dwn,
                    payload = None,
                    prefix=self.prefix
                )


        def message(client, feed_id, payload):
            msg = str(feed_id)
            pl = str(payload)
            if (self.oldEvent <> msg+pl or self.repeat):
                eg.TriggerEvent(
                    msg,
                    payload = pl,
                    prefix=self.prefix
                )
                self.oldEvent = msg+pl
            if pl == 'disconnect':
                try:
                    self.client.disconnect()
                except:
                    pass

            
        def LogToFile(s):
            s = s.decode('utf-8')
            timeStamp = str(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            logStr = timeStamp+"\t"+s+"<br\n>"
            fileHandle = None
            progData = eg.configDir + '\plugins\Adafruit MQTT Client'
            if (
                not os.path.exists(progData)
                and not os.path.isdir(progData)
            ):
                os.makedirs(progData)
            fileHandle = open (
                progData+'/'+
                self.name+'.htm', 'a'
            )
            fileHandle.write ( logStr.encode('utf-8') )
            fileHandle.close ()


        goInit()


    def publishEvent(self, message):
        if message <> [] and self.started:
            try:
                self.client.publish(message[0], message[1])
            except:
                eg.PrintError (self.text.publish_failed+str(message))
            self.message = []

            
    def __stop__(self):
        self.mainThreadEvent.set()
        self.started = False
        self.connectionCntr = 0
        try:
            self.client.disconnect()
        except:
            pass
        print self.text.plugin_dwn
        

    def __close__(self):
        self.started = False
        self.connectionCntr = 0
        try:
            self.client.disconnect()
        except:
            pass


    def Configure(
        self,
        adafruitUser='adafruit io username',
        adafruitIOkey='adafruit io key',
        adafruitFeedId='feed id',
        repeat=False,
        *args
    ):
        text = self.text
        panel = eg.ConfigPanel(self, resizable=True)
        
        UserCtrl = wx.TextCtrl(panel, -1, adafruitUser)
        UserCtrl.SetInitialSize((250,-1))

        IOkeyCtrl = wx.TextCtrl(panel, -1, adafruitIOkey)
        IOkeyCtrl.SetInitialSize((250,-1))

        FeedIdCtrl = wx.TextCtrl(panel, -1, adafruitFeedId)
        FeedIdCtrl.SetInitialSize((250,-1))
  
        repeatCtrl = wx.CheckBox(panel, -1, "")
        repeatCtrl.SetValue(repeat)
  
        panel.AddLine(text.adafruitUser, UserCtrl)
        panel.AddLine(text.adafruitIOkey, IOkeyCtrl)
        panel.AddLine(text.adafruitFeedId, FeedIdCtrl)
        panel.AddLine(text.repeat, repeatCtrl)

        while panel.Affirmed():
            panel.SetResult(
                UserCtrl.GetValue(),
                IOkeyCtrl.GetValue(),
                FeedIdCtrl.GetValue(),
                repeatCtrl.GetValue(),
                *args
            )



class publishMQTT(eg.ActionClass):
    text = publishMQTTtxt
    
    def __call__(
        self,
        name,
        topic,
        message
    ):
        self.message = str(
            (eg.ParseString(message) if message else '').encode("utf-8")
        )
        self.plugin.publishEvent([str(topic), self.message])
        
             
    def Configure(
        self,
        name="Give this MQTT message a name",
        topic="eventghost",
        message=u"{eg.event.string}{eg.event.payload}"
    ):
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)
        mySizer_3 = wx.GridBagSizer(10, 10)

        #name
        nameCtrl = wx.TextCtrl(panel, -1, name)
        nameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.actionName), (0,0))
        mySizer_1.Add(nameCtrl, (1,0))

        #topic
        topicCtrl = wx.TextCtrl(panel, -1, topic)
        topicCtrl.SetInitialSize((250,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.topicName), (1,0))
        mySizer_2.Add(topicCtrl, (2,0))

        #message
        messageCtrl = wx.TextCtrl(panel, -1, message)
        messageCtrl.SetInitialSize((250,-1))
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.messageName), (1,0))
        mySizer_3.Add(messageCtrl, (2,0))


        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            name = nameCtrl.GetValue()
            topic = topicCtrl.GetValue()
            message = messageCtrl.GetValue()
            panel.SetResult(
                name,
                topic,
                message
            )




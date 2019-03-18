#!/usr/bin/python
#   Title: samsungremote.py
#   Author: D. Redkin. Code based on work of Asif Iqbal 
#   Date: 20OCT2012
#   Info: To send remote control commands to the Samsung tv over LAN
#   TODO:
 
import socket
import base64
import time, datetime
import wininet_tools

class SamsungTVSender:
    """ Can send commnds to Samsung TVs over LAN """
    #What the iPhone app reports
    appstring = "iphone..iapp.samsung"
    #What gets reported when it asks for permission
    remotename = ""
    tvip = "samsungtv."
    myip = ""
    mymac = ""
    sock = None
    def __init__(self, remotename):
        self.remotename = remotename
        
    def __del__(self):
        self.disconnect()

    def disconnect(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None
        
    def connect(self, tvip, tvmodel):
        self.tvip = tvip
        self.tvmodel = tvmodel
        (self.myip, self.mymac) = wininet_tools.getMyIPAndMAC(tvip)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "sending connecting to ", self.tvip
        self.sock.connect((self.tvip, 55000))

    # First configure the connection
    def initConn(self):
        if self.sock is None :
            raise Exception("Call connect first")
        ipencoded = base64.b64encode(self.myip)
        macencoded = base64.b64encode(self.mymac)
        messagepart1 = chr(0x64) + chr(0x00) + chr(len(ipencoded)) \
        + chr(0x00) + ipencoded + chr(len(macencoded)) + chr(0x00) \
        + macencoded + chr(len(base64.b64encode(self.remotename))) + chr(0x00) \
        + base64.b64encode(self.remotename)
         
        part1 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring \
        + chr(len(messagepart1)) + chr(0x00) + messagepart1
        self.sock.send(part1)
     
        messagepart2 = chr(0xc8) + chr(0x00)
        part2 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) + self.appstring \
        + chr(len(messagepart2)) + chr(0x00) + messagepart2
        self.sock.send(part2)

    # Function to send keys
    def sendKey(self, skey):
        if self.sock is None :
            raise Exception("Call connect first")
        self.initConn()

        messagepart3 = chr(0x00) + chr(0x00) + chr(0x00) \
        + chr(len(base64.b64encode(skey))) + chr(0x00) + base64.b64encode(skey);
        part3 = chr(0x00) + chr(len(self.appstring)) + chr(0x00) \
        + self.appstring + chr(len(messagepart3)) + chr(0x00) + messagepart3
        self.sock.send(part3);
       
#S = SamsungTVSender("Python Remote")
#S.connect("192.168.1.96","LE46C650")
#S.sendKey("KEY_TOOLS")
#S.disconnect
#
# plugins/DovadoUMR/__init__.py
#
# Copyright (C) 2010
# Michael Lindborg
#
##############################################################################
# Revision history:
#
#
# 2010-01-06  The first alpha version
# 2010-02-20  First published version (Limited error handling, SMS Delete action not yet implemented)
################################################################################################################################################################
#
#
# EventGhost Plugin for the Dovado UMR 3G Router, with Tellstick and SMS functions. 
#
# The plugin implements the functions in the Dovado UMR API, providing
# Tellstick ON/OFF control and SMS send/receive capabilities to EventGhost
#
# The API must be activated in the router setup: SYSTEM->REMOTE MANAGEMENT->DOVADO API
# Don't forget to reboot the router after activation
#
# $LastChangedDate: 2010-02-03 $
# $LastChangedRevision: 1 $
# $LastChangedBy: mickelin $
#
# telnet code based on TelnetController.py by Corey Goldberg (C) 2005
# pdu conversion code borrowed from pdu.py by Costin Stroie (C) 2006 
#
# Basic code structure and inspiration from the Zoomplayer plugin by Lars-Peter Voss (C) 2005 
# and the NetHomeServer plugin by Walter Kraembring (C) 2009
#
# Thanks to all!
#
#############################################################################

__description__ = (
    'Adds actions to control the Dovado UMR 3G Router '
    '<a href="http://www.dovado.com/">Dovado UMR</a>.'
)

__help__ = """\
<b>Notice:</b><br>
To make it work, you have to enable the API in the Dovado UMR setup.

<i>SYSTEM->REMOTE MANAGEMENT->DOVADO API</i>

Don't forget to reboot the router after enabling the API

"""

import eg

eg.RegisterPlugin(
    name="Dovado UMR",
    guid='{424AFF67-B71A-40A0-AC21-BFBB389C8DEE}',
    author="mickelin",
    version="0.1." + "$LastChangedRevision: 001 $".split()[1],
    kind="external",
    canMultiLoad=False,
    createMacrosOnAdd=False,
    description=__description__,
    help=__help__,
)

import os
import sys
import telnetlib
import time
import wx

from threading import Event, Thread

# ===================================================================
# Functions and class for PDU <-> text conversion, copied from pdu.py
# ===================================================================

# Hex to dec conversion array
hex2dec = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
           'D': 13, 'E': 14, 'F': 15}

# GSM to ISO8859-1 conversion array
gsm_to_latin = {'0': 64, '1': 163, '2': 36, '3': 165, '4': 232, '5': 233, '6': 249, '7': 236, '8': 242, '9': 199,
                '11': 216, '12': 248,
                '14': 197, '15': 229, '16': 0, '17': 95,
                '18': 0, '19': 0, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0, '25': 0, '26': 0, '27': 0,
                '28': 198, '29': 230, '30': 223, '31': 201,
                '36': 164,
                '64': 161,
                '91': 196, '92': 214, '93': 209, '94': 220, '95': 167, '96': 191,
                '123': 228, '124': 246, '125': 241, '126': 252, '127': 224}


def hex2int(n):
    """
    Convert a hex number to decimal
    """
    c1 = n[0]
    c2 = n[1]

    c3 = (hex2dec[c1] * 16) + (hex2dec[c2])
    return int("%s" % c3)


def int2hex(n):
    """
    Convert a decimal number to hexadecimal
    """
    hex = ""
    q = n
    while q > 0:
        r = q % 16
        if r == 10:
            hex = 'A' + hex
        elif r == 11:
            hex = 'B' + hex
        elif r == 12:
            hex = 'C' + hex
        elif r == 13:
            hex = 'D' + hex
        elif r == 14:
            hex = 'E' + hex
        elif r == 15:
            hex = 'F' + hex
        else:
            hex = str(r) + hex
        q = int(q / 16)

    if len(hex) % 2 == 1: hex = '0' + hex
    return hex


def byteSwap(byte):
    """
    Swap the first and second digit position inside a hex byte
    """
    return "%c%c" % (byte[1], byte[0])


def parseTimeStamp(time):
    """
    Convert the time from PDU format to some common format
    """

    y = byteSwap(time[0:2])
    m = byteSwap(time[2:4])
    d = byteSwap(time[4:6])

    hour = byteSwap(time[6:8])
    min = byteSwap(time[8:10])
    sec = byteSwap(time[10:12])

    if int(y) < 70:
        y = "20" + y

    return "%s.%s.%s %s:%s" % (y, m, d, hour, min)


def decodeText7Bit(src):
    """
    Decode the 7-bits coded text to one byte per character
    """

    bits = ''

    i = 0
    l = len(src) - 1

    # First, get the bit stream, concatenating all binary represented chars
    while i < l:
        bits += char2bits(src[i:i + 2])
        i += 2

    # Now decode those pseudo-8bit octets
    char_nr = 0
    i = 1

    tmp_out = ''
    acumul = ''
    decoded = ''
    while char_nr <= len(bits):
        byte = bits[char_nr + i:char_nr + 8]
        tmp_out += byte + "+" + acumul + " "
        byte += acumul
        c = chr(bits2int(byte))

        decoded += c

        acumul = bits[char_nr:char_nr + i]

        i += 1
        char_nr += 8

        if i == 8:
            i = 1
            char_nr
            decoded += chr(bits2int(acumul))
            acumul = ''
            tmp_out += "\n"

    return gsm2latin(decoded)


def decodeText8Bit(src):
    """
    Decode the 8-bits coded text to one byte per character
    """
    chars = ''
    i = 0
    while i < len(src):
        chars += chr(src[i:i + 2])
        i += 2
    return chars


def decodeText16Bit(src):
    """
    Decode the 16-bits coded text to one byte per character
    """
    chars = u''
    i = 0
    while i < len(src):
        h1 = src[i:i + 2]
        h2 = src[i + 2:i + 4]
        c1 = hex2int(h1)
        c2 = hex2int(h2)

        unicodeIntChar = (256 * c1) + c2
        unicodeChar = chr(unicodeIntChar)

        chars += unicodeChar
        i += 4
    return chars


def encodeText7Bit(src):
    """
    Encode ASCII text to 7-bit encoding
    """
    result = []
    count = 0
    last = 0
    for c in src:
        this = ord(c) << (8 - count)
        if count:
            result.append('%02X' % ((last >> 8) | (this & 0xFF)))
        count = (count + 1) % 8
        last = this
    result.append('%02x' % (last >> 8))
    return ''.join(result)


def char2bits(char):
    """
    Convert a character to binary.
    """

    inputChar = hex2int(char)
    mask = 1
    output = ''
    bitNo = 1

    while bitNo <= 8:
        if inputChar & mask > 0:
            output = '1' + output
        else:
            output = '0' + output
        mask = mask << 1
        bitNo += 1

    return output


def bits2int(bits):
    """
    Convert a binary string to a decimal integer
    """

    mask = 1
    i = 0
    end = len(bits) - 1

    result = 0
    while i <= end:
        if bits[end - i] == "1":
            result += mask
        mask = mask << 1
        i += 1

    return result


def gsm2latin(gsm):
    """
    Convert a GSM encoded string to latin1 (where available).
    TODO: implement the extension table introduced by char 27.
    """

    i = 0
    latin = ''
    while i < len(gsm) - 1:
        if str(ord(gsm[i])) in gsm_to_latin:
            latin += chr(gsm_to_latin[str(ord(gsm[i]))])
        else:
            latin += gsm[i]
        i += 1

    return latin


class PDU:
    """
    The PDU class implements basic encoding and decoding functions related
    to the GSM PDU format.
    """

    def __init__(self):
        """
        Class initialisation routines
        """

    def decodeSMS(self, sms):
        """
        Return the SMS and extra SMS data decoded from the PDU format
        """
        self.SMS = {}

        smsc_len = hex2int(sms[0:2])
        type_of_address = hex2int(sms[2:4])

        # Read the SMS center number
        smsc_number = ''
        i = 4
        while i / 2 <= smsc_len:
            smsc_number += sms[i + 1]
            if i / 2 != smsc_len:
                smsc_number += sms[i]
            i += 2
        self.SMS['smsc'] = smsc_number

        # Decode the sms sender information
        pdu_flags = hex2int(sms[i:i + 2])

        # Message type indicator. Bits no 1 and 0 are both set to 0 to indicate that this PDU is an SMS-DELIVER.
        if pdu_flags & 1 == 0 and pdu_flags & 2 == 0:
            self.SMS['fMTI'] = True
        else:
            self.SMS['fMTI'] = False

        # More messages to send. This bit is set to 0 if there are more messages to send.
        if pdu_flags & 4 != 0:
            self.SMS['fMMS'] = True
        else:
            self.SMS['fMMS'] = False

        # Status report indication. This bit is set to 1 if a status report is going to be returned to the SME.
        if pdu_flags & 32 != 0:
            self.SMS['fSRI'] = True
        else:
            self.SMS['fSRI'] = False

        # User data header indicator. This bit is set to 1 if the User Data field starts with a header.
        if pdu_flags & 64 != 0:
            self.SMS['fUDHI'] = True
        else:
            self.SMS['fUDHI'] = False

        # Reply path. Parameter indicating that reply path exists.
        if pdu_flags & 128 != 0:
            self.SMS['fRP'] = True
        else:
            self.SMS['fRP'] = False

        # Decode the sender number
        i += 2
        sender_len = hex2int(sms[i:i + 2])
        i += 2
        sender_type = sms[i:i + 2]
        i += 2
        if sender_len % 2 == 1:
            # with a trailing F
            sender_number = sms[i:i + sender_len + 1]
            i += sender_len + 1
        else:
            sender_number = sms[i:i + sender_len]
            i += sender_len

        tmp_sender = ''
        s = 0
        e = len(sender_number) - 1

        while s < e:
            tmp_sender += sender_number[s + 1]
            tmp_sender += sender_number[s]
            s += 2

        if sender_len % 2 == 1:
            # need to cut of 'F'
            tmp_sender = tmp_sender[0:-1]

        self.SMS['sender'] = tmp_sender

        # Loading DATA CODING SCHEME and FLAGS
        protocol_id = sms[i:i + 2]
        i += 2
        dcs_mode = sms[i:i + 2]
        i += 2

        dcs_bits = hex2int(dcs_mode)
        if dcs_bits & 128 == 1 and dcs_bits & 64 == 1 and dcs_bits & 32 == 1 and dcs_bits & 16 == 1:
            # Data coding/message class
            special_coding = True
        else:
            special_coding = False

        if (dcs_bits & 8 == 0 and dcs_bits & 4 == 0) or special_coding == True:
            self.SMS['coding'] = 7
        elif dcs_bits & 8 > 0 and dcs_bits & 4 == 0:
            self.SMS['coding'] = 16
        elif dcs_bits & 8 == 0 and dcs_bits & 4 > 0:
            self.SMS['coding'] = 8
        else:
            self.SMS['coding'] = 0

        # Get the sending timestamp
        self.SMS['time'] = parseTimeStamp(sms[i:i + 14])

        # Finally, get the message
        i += 14
        self.SMS['length'] = hex2int(sms[i:i + 2])

        if self.SMS['length'] > 0:
            i += 2
            message_enc = sms[i:i + (self.SMS['length'] * 2) - 1]

        if self.SMS['coding'] == 7:
            self.SMS['message'] = decodeText7Bit(message_enc)
        # print message_enc
        # print self.SMS['message']
        # print len(self.SMS['message'])
        elif self.SMS['coding'] == 8:
            self.SMS['message'] = decodeText8Bit(message_enc)
        else:
            self.SMS['message'] = decodeText16Bit(message_enc)

        return self.SMS

    def encodeSMS(self, dest_number, text):
        """
        Return the SMS encoded to PDU format, based on a template
        and on supplied data.
        """

        # Start from a template
        result = "001100"

        # Add the length of the phone number and the number format
        result += int2hex(len(dest_number)) + '91'

        # Add the phone number
        tmp_number = dest_number
        if len(tmp_number) % 2 == 1: tmp_number += 'F'
        i = 0
        while i < len(tmp_number):
            result = result + byteSwap(tmp_number[i:i + 2])
            i += 2

        # Add the protocol id and DCS
        result += '0000'

        # Add the validity period (4 days)
        result += 'AA'

        # Added the message length and the message
        result += int2hex(len(text))
        result += encodeText7Bit(text)

        return result


# ===================================================================
# UMR Plugin code
# ===================================================================

def ProcessInbox(self):
    commandStr = "sms recv"
    response = self.__SendCommand__(commandStr)
    # Check for empty inbox
    if str(response) == " >>":
        self.TriggerEvent("Inbox empty")
    else:
        msgarray = response[1:]
        messages = msgarray.splitlines()
        messages.pop()
        i = len(messages)
        for message in messages:
            tmp = message.split(":")
            num = tmp[0]
            p = tmp[1]
            pdu = PDU()
            pdu.decodeSMS(p)
            payload = (pdu.SMS['sender'] + "|" + pdu.SMS['message'])
            self.TriggerEvent("New SMS ", payload)
            if self.logSMS == True:
                io = 'In'
                LogToFile(payload, io)
            if self.deleteSMS == True:
                commandStr = "sms del " + num
                response = self.__SendCommand__(commandStr)
    return


def LogToFile(s, io):
    timeStamp = str(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    )
    fileDate = str(
        time.strftime("%Y%m%d", time.localtime())
    )
    logStr = timeStamp + " " + io + " " + s + "<br\n>"
    majorVersion, minorVersion = sys.getwindowsversion()[0:2]
    if majorVersion > 5:
        progData = os.environ['ALLUSERSPROFILE']
        if (
            not os.path.exists(progData + "/EventGhost/Log")
            and not os.path.isdir(progData + "/EventGhost/Log")
        ):
            os.makedirs(progData + "/EventGhost/Log")
        fileHandle = open(
            progData + '/EventGhost/Log/' + fileDate + ' Dovado UMR SMS Log.html', 'a'
        )
        fileHandle.write(logStr)
        fileHandle.close()

    else:
        if not os.path.exists('Log') and not os.path.isdir('Log'):
            os.mkdir('Log')
        fileHandle = open('Log/' + fileDate + ' Dovado UMR SMS Log.html', 'a')
        fileHandle.write(logStr)
        fileHandle.close()
    return


class Text:
    tcpBox = "TCP/IP Settings"
    hostLabel = "Host:"
    portLabel = "Port:"
    userLabel = "User:"
    passwordLabel = "Password:"
    smsBox = "SMS settings"
    delete = "Delete processed SMS messages"
    log = "Log incoming/outgoing SMS messages"
    SMSpoll = "SMS polling interval"

    class Add:
        alias = "Device Name:"
        protocol = "Protocol:"
        house = "House Code:"
        channel = "Channel:"

    class Del:
        alias = "Device Name:"

    class OnOff:
        alias = "Device Name:"
        onoff = "on/off:"

    class SMS:
        number = "Phone Number:"
        message = "Message Text:"


class UMRSession:
    """
    Handles a Dovado UMR Telnet session.
    """

    def __init__(self, host_name, port, user_name, password):
        """Initialise telnet session parameters    
        """

        self.host_name = host_name
        self.port = port
        self.user_name = user_name
        self.password = password
        self.prompt = ">>"
        self.tn = None

    def login(self):
        """Connect to a remote host and login.
        """

        # Add error handling

        # print "Login"
        self.tn = telnetlib.Telnet(self.host_name, self.port)
        reply = self.tn.read_until(self.prompt)
        # print "Reply 1: " + reply
        sendStr = ("user " + self.user_name).encode('ascii')
        # print "Sending text: "+ sendStr
        self.tn.write(sendStr + "\n")
        reply = self.tn.read_until(self.prompt)
        # print "Reply 2: " + reply
        sendStr = ("pass " + self.password).encode('ascii')
        # print "Sending text:" + sendStr
        self.tn.write(sendStr + "\n")
        reply = self.tn.read_until(self.prompt)
        # print "Reply 3: "+ reply        

    def RunCommand(self, command):
        """Run a command on the remote host UMR
        """
        self.tn.write(command + '\n')
        reply = self.tn.read_until(self.prompt)
        return reply

    def logout(self):
        """Close the connection to the remote host.            
        """
        self.tn.write("exit\n")
        reply = self.tn.read_until("lost.")
        self.tn.close()
        return None


# Prototype of an action

class ActionBase(eg.ActionClass):

    def SendCommand(self, command):
        """Start a UMR session,login, send a command and logout 
        """
        umr = UMRSession(self.plugin.host, self.plugin.port, self.plugin.user, self.plugin.password)
        umr.login()
        reply = umr.RunCommand(command)
        umr.logout()
        return reply


class umrListAlias(ActionBase):
    # Retrieve a list of RF devices defined in the UMR, called Aliases
    name = "List Aliases"
    description = "Retrieve a list of aliases defined in the UMR"

    def __call__(self):
        commandStr = "ts aliases"
        reply = self.SendCommand(commandStr)
        print reply
        return


class umrAddAlias(ActionBase):
    # Add a new device/alias
    name = "Add Alias"
    description = "Add a new device/Alias"

    text = Text.Add

    def __call__(self, alias, protocol, house, channel):
        self.alias = alias
        self.protocol = protocol
        self.house = str(house)
        self.channel = str(channel)
        commandStr = ("ts add " + alias + " " + protocol + " " + house + " " + channel).encode('ascii')
        return self.SendCommand(commandStr)

    def Configure(
        self,
        alias=(
            "Name of the device"
        ),
        protocol=" ",
        house=" ",
        channel=" "
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)
        mySizer_3 = wx.GridBagSizer(10, 10)
        mySizer_4 = wx.GridBagSizer(10, 10)

        # alias
        aliasCtrl = wx.TextCtrl(panel, -1, alias)
        aliasCtrl.SetInitialSize((250, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.alias), (0, 0))
        mySizer_1.Add(aliasCtrl, (1, 0))

        # protocol
        protocolCtrl = wx.Choice(panel, -1,
                                 choices=("NEXA", "WAVEMAN", "SARTANO", "IKEA", "RISINGSUN", "ARCTECH", "BRATECK"))
        protocolCtrl.SetInitialSize((250, -1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.protocol), (0, 0))
        mySizer_2.Add(protocolCtrl, (1, 0))

        # house code
        houseCtrl = wx.Choice(panel, -1,
                              choices=("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"))
        houseCtrl.SetInitialSize((250, -1))
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.house), (0, 0))
        mySizer_3.Add(houseCtrl, (1, 0))

        # channel
        channelCtrl = wx.Choice(panel, -1, choices=(
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"))
        channelCtrl.SetInitialSize((250, -1))
        mySizer_4.Add(wx.StaticText(panel, -1, self.text.channel), (0, 0))
        mySizer_4.Add(channelCtrl, (1, 0))

        panel.sizer.Add(mySizer_1, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_4, 0, flag=wx.EXPAND)

        while panel.Affirmed():
            alias = aliasCtrl.GetValue()
            protocol = protocolCtrl.GetStringSelection()
            house = houseCtrl.GetStringSelection()
            channel = channelCtrl.GetStringSelection()
            panel.SetResult(
                alias,
                protocol,
                house,
                channel
            )


class umrAliasOnOff(ActionBase):
    # Turn on or off the named device
    name = "Alias On/Off"
    description = "Turn named Alias On or Off"

    text = Text.OnOff

    def __call__(self, alias, onoff):
        self.alias = alias
        commandStr = ("ts turn " + self.alias + " " + onoff).encode('ascii')
        return self.SendCommand(commandStr)

    def Configure(
        self,
        alias=(
            "Name of the device"
        ),
        onoff=" "
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)

        # alias
        aliasCtrl = wx.TextCtrl(panel, -1, alias)
        aliasCtrl.SetInitialSize((250, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.alias), (0, 0))
        mySizer_1.Add(aliasCtrl, (1, 0))

        # onoff
        onoffCtrl = wx.Choice(panel, -1, choices=("on", "off"))
        onoffCtrl.SetInitialSize((250, -1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.onoff), (0, 0))
        mySizer_2.Add(onoffCtrl, (1, 0))

        panel.sizer.Add(mySizer_1, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag=wx.EXPAND)

        while panel.Affirmed():
            alias = aliasCtrl.GetValue()
            onoff = onoffCtrl.GetStringSelection()
            panel.SetResult(
                alias,
                onoff
            )


class umrDelAlias(ActionBase):
    # Delete the named device
    name = "Delete Alias"
    description = "Delete named Alias"

    text = Text.Del

    def __call__(self, alias):
        self.alias = alias
        commandStr = ("ts remove " + self.alias).encode('ascii')
        return self.SendCommand(commandStr)

    def Configure(
        self,
        alias=(
            "Name of the device"
        )
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)

        # alias
        aliasCtrl = wx.TextCtrl(panel, -1, alias)
        aliasCtrl.SetInitialSize((250, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.alias), (0, 0))
        mySizer_1.Add(aliasCtrl, (1, 0))

        panel.sizer.Add(mySizer_1, 0, flag=wx.EXPAND)

        while panel.Affirmed():
            alias = aliasCtrl.GetValue()
            panel.SetResult(
                alias
            )


class umrSmsCheck(ActionBase):
    # List number of messages in inbox
    name = "Check SMS inbox"
    description = "Check SMS inbox: unread/total"

    def __call__(self):
        commandStr = "sms list"
        p = self.SendCommand(commandStr)
        s = p.split("/")
        unread = s[0]
        t = s[1]
        total = t.split('\n')
        return unread


class umrSmsRecv(ActionBase):
    # Retrieve all the messages in the inbox
    name = "Receive all SMS"
    description = "Receive all messages in the inbox"

    def __call__(self):
        commandStr = "sms recv"
        response = self.SendCommand(commandStr)
        # Check for empty inbox
        if str(response) == ' >>':
            self.plugin.TriggerEvent("Inbox empty")
        else:
            # Remove leading space
            msgarray = response[1:]
            messages = msgarray.splitlines()
            # remove prompt at the end
            messages.pop()
            # loop through the messages and separate message number from PDU
            for message in messages:
                tmp = message.split(":")
                num = tmp[0]
                p = tmp[1]
                pdu = PDU()
                pdu.decodeSMS(p)
                payload = (pdu.SMS['sender'] + "|" + pdu.SMS['message'])
                self.plugin.TriggerEvent("New SMS ", payload)
                if self.plugin.logSMS == True:
                    io = 'In'
                    LogToFile(payload, io)
                if self.plugin.deleteSMS == True:
                    commandStr = "sms del " + num
                    response = self.SendCommand(commandStr)
        return


class umrSmsSend(ActionBase):
    # Send a SMS message
    name = "Send SMS"
    description = "Send SMS"

    text = Text.SMS

    def __call__(self, number, message):
        commandStr = "sms send "
        self.number = number
        self.message = message
        pdu = PDU()
        sms = pdu.encodeSMS(self.number, self.message)
        command = (commandStr + sms).encode('ascii')
        umr = UMRSession(self.plugin.host, self.plugin.port, self.plugin.user, self.plugin.password)
        umr.login()
        umr.RunCommand(command)
        umr.logout()
        if self.plugin.logSMS == True:
            io = 'Out'
            payload = (self.number + "|" + self.message)
            LogToFile(payload, io)
        return None

    def Configure(
        self,
        number="Country Code, no prefix (e.g. 467nnnnnnnn)",
        message=(
            "Message"
        )
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)

        # number
        numberCtrl = wx.TextCtrl(panel, -1, number)
        numberCtrl.SetInitialSize((250, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.number), (0, 0))
        mySizer_1.Add(numberCtrl, (1, 0))

        # message
        messageCtrl = wx.TextCtrl(panel, -1, message, style=wx.TE_MULTILINE)
        messageCtrl.SetInitialSize((400, -1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.message), (1, 0))
        mySizer_2.Add(messageCtrl, (2, 0))

        panel.sizer.Add(mySizer_1, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag=wx.EXPAND)

        while panel.Affirmed():
            number = numberCtrl.GetValue()
            message = messageCtrl.GetValue()
            panel.SetResult(
                number,
                message
            )


class umrSmsDel(ActionBase):
    # Delete a specific SMS from inbox (not yet implemented)
    name = "Delete SMS"
    description = "Delete SMS from Inbox"

    def __call__(self, sms):
        self.sms = sms
        commandStr = ("sms del " + self.sms).encode('ascii')
        return self.SendCommand(commandStr)


class Dovado_UMR(eg.PluginClass):
    text = Text

    def __init__(self):
        print "Initialising Dovado UMR Plugin"
        self.host = "192.168.0.1"
        self.port = 6435
        self.user = "admin"
        self.password = "password"
        self.deleteSMS = False
        self.logSMS = False
        self.isSessionRunning = False

        self.AddAction(umrAliasOnOff)
        self.AddAction(umrAddAlias)
        self.AddAction(umrDelAlias)
        self.AddAction(umrListAlias)
        self.AddAction(umrSmsCheck)
        self.AddAction(umrSmsRecv)
        self.AddAction(umrSmsSend)

    #        self.AddAction(umrSmsDel)

    def __start__(
        self,
        host="192.168.0.1",
        port=6435,
        user="admin",
        password="password",
        deleteSMS=False,
        logSMS=False,
        pollSMS=90
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.deleteSMS = deleteSMS
        self.logSMS = logSMS
        self.pollSMS = pollSMS

        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.PollSMSInbox,
            args=(self.stopThreadEvent,)
        )
        thread.start()

    def __stop__(self):
        self.stopThreadEvent.set()
        if self.isSessionRunning:
            self.session.close()

    def __SendCommand__(self, command):
        """Start a UMR session,login, send a command and logout 
        """
        umr = UMRSession(self.host, self.port, self.user, self.password)
        umr.login()
        reply = umr.RunCommand(command)
        umr.logout()
        return reply

    def PollSMSInbox(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            commandStr = "sms list"
            reply = self.__SendCommand__(commandStr)
            tmp = reply.split("/")
            unread = tmp[0]
            t = tmp[1]
            total = t.split('\n')
            if int(unread) > 0:
                ProcessInbox(self)
            else:
                self.TriggerEvent("No new SMS")
            stopThreadEvent.wait(self.pollSMS)

    def Configure(
        self,
        host="192.168.0.1",
        port=6435,
        user="admin",
        password="password",
        deleteSMS=False,
        logSMS=False,
        pollSMS=600
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        userCtrl = panel.TextCtrl(user)
        passwordCtrl = panel.TextCtrl(password)
        deleteCtrl = panel.CheckBox(deleteSMS, text.delete)
        logCtrl = panel.CheckBox(logSMS, text.log)
        SMSpollCtrl = panel.SpinIntCtrl(pollSMS, min=10, max=3000)

        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (text.hostLabel, hostCtrl),
            (text.portLabel, portCtrl),
            (text.userLabel, userCtrl),
            (text.passwordLabel, passwordCtrl),
        )
        eg.EqualizeWidths(tcpBox.GetColumnItems(0))
        smsBox = panel.BoxedGroup(
            text.smsBox,
            deleteCtrl,
            logCtrl,
            text.SMSpoll,
            SMSpollCtrl,
        )
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(smsBox, 0, wx.TOP | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                userCtrl.GetValue(),
                passwordCtrl.GetValue(),
                deleteCtrl.GetValue(),
                logCtrl.GetValue(),
                SMSpollCtrl.GetValue(),
            )

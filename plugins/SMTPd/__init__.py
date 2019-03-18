eg.RegisterPlugin(
    name = "SMTPd",
    guid='{A6E9B04D-2B6A-4936-90C9-CE7E33271B4A}',
    author = "Techoguy and luma",
    version = "0.0.1",
    kind = "other",
    description = "Setup an SMTP daemon and trigger events when messages arrive.",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACx"
        "jwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAu"
        "NvyMY98AAAErSURBVDhP1ZK9SgNBFEbnhVLbm0qwzFPoA1hYKhIQGy0EOxuxUJCAIIQQTBBEDFio"
        "KPgDbkDCRmSFRLMkuXI+mHXWINiJC2czezPfmbm74/7+mls/t5WdG+M3pLR6OsHscjOjuLBvhdKG"
        "ubWDyPqDkSX9oQ2G41/B3PgtlcSxOoXNw8geOh8a38fjjOglFQRYiDnlvSe7bSfalVrAWmklOUkY"
        "9GGeCW/VX1XLCS7baU5CwIf5nzDtEq5evX8JuDHh+nkkdk+6WoUAdR+mVcKNu1RkAt6oF7Qee1Y5"
        "iyXxOwHG1GBCML14LAEtVC+6kiBjm9v1jmAcLpATTM0fqV/CSMIv8J1QQlsScBiwUeDte5D+BPMR"
        "6RwgYBdAO56ZpZoIT5+HenYS//vl3CeOUlJ5FnYb6QAAAABJRU5ErkJggg=="
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=7833"
)

# TO DO:
# - There is no error handling when looking for the subject
# - Can add much more function to store the attachments and pull the body text. 

import eg
import smtpd
from email.parser import Parser

# set the default event prefix value here
smtpdPrefix = 'SMTPd'

class Text:
    port = "SMTP TCP Port:"
    ip = "SMTP listener address:"
    eventPrefix = "Event Prefix:"
    tcpBox = "SMTP Server Settings"
    eventGenerationBox = "Event generation" 

class CustomSMTPServer(smtpd.SMTPServer):
    global smtpdPrefix
    def process_message(self, peer, mailfrom, rcpttos, data):
        print 'SMTPd: Receiving message from:', peer
        #print 'SMTPd: Message addressed from:', mailfrom
        #print 'SMTPd: Message addressed to  :', rcpttos
        #print 'SMTPd: Message length        :', len(data)
        headers = Parser().parsestr(data)
        #print 'SMTPd: Subject               :%s' % headers['subject']
        #print 'SMTPd: Message               :\n', data
        for recemail in rcpttos:
            eg.TriggerEvent(recemail, prefix=smtpdPrefix, payload=headers['subject'])

class SMTPdaemon(eg.PluginBase):
    text = Text
    global smtpdPrefix
	
    def __start__(self, port, ip, prefix):
        global smtpdPrefix
        self.port = port
        self.ip = ip
        smtpdPrefix = prefix
        print 'Starting SMTPd Server at %s:%s' % (self.ip, self.port)
        self.server = CustomSMTPServer((self.ip, self.port), None)
        eg.RestartAsyncore()

    def __stop__(self):
        if self.server:
            self.server.close()
            print 'Stopping SMTPd Server at %s:%s' % (self.ip, self.port)
        self.server = None
        
    def __close__(self):
        if self.server:
            self.server.close()
        self.server = None

    def Configure(self, port=25, ip="127.0.0.1", prefix=smtpdPrefix):
        text = self.text
        panel = eg.ConfigPanel()
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        ipCtrl = panel.TextCtrl(ip)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        st1 = panel.StaticText(text.port)
        st2 = panel.StaticText(text.ip)
        st3 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st2, st3))
        box1 = panel.BoxedGroup(text.tcpBox, (st1, portCtrl),(st2, ipCtrl))
        box2 = panel.BoxedGroup(text.eventGenerationBox, (st3, eventPrefixCtrl))
        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND|wx.TOP, 10),
        ])
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                ipCtrl.GetValue(),
                eventPrefixCtrl.GetValue()
            )

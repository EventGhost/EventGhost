# -*- coding: utf-8 -*-
version = "0.0.1"

# plugins/Gmail/__init__.py
#
# Copyright (C) 2017  Pako <lubos.ruckl@gmail.com>
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.0 by Pako 2017-11-19 13:09 GMT+1
#     - first public version
#===============================================================================
#ToDo:
#1) Confirmation of delivery.
#   -> Add "message ['Disposition-notification-to'] = Sender address"
#   This indicates that the plugin must know the address of the sender !
#===============================================================================

eg.RegisterPlugin(
    name = "Gmail",
    author = "Pako",
    version = version,
    kind = "program",
    guid = "{31990FB1-302D-46C0-9862-C17F80B3945F}",
    createMacrosOnAdd = True,
    canMultiLoad = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEUA///xQzbxmJPT"
        "LirxNyjy8vLxOivwLx3y+vry9fXxLBjQDwUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAABg1ghg1ggAM8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADRxNocAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAHtJREFUeNrtzVsWgCAIBFAm"
        "HO2x//2WgUfNbAXxUeJcQeSvuwAss2y5wgyu7+xtAZjmELV/eMbB7lXUBd6eQzWfdBQl"
        "NgBaH0scrWcFTO0QOye2gD4kibjNdx2gz/VtHAHXmq98A2VN7QdgayLngBuw8Qv09YMG"
        "7N/gOAGbDwjAXkJZSAAAAABJRU5ErkJggg=="
    ),
    description = ur'''<rst>
Sending emails (including attachments).

This plugin has only one use and one action:
it sends emails using the Google Gmail account.
The plugin uses OAuth_ authorization, so you do not need to save 
the credentials in open form anywhere !


**ATTENTION!**
This plugin requires the user to have an account on `Google Developers`_ !!!

| **Installation:**
| ==========
| **A) Getting the client_secret.json file (it may be common to multiple Gmail plugins)**
| A.1) Use this_ wizard to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials
| A.2) On the Add credentials to your project page, click the Cancel button
| A.3) At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button
| A.4) Select the Credentials tab, click the Create credentials button and select OAuth client ID
| A.5) Select the application type Other, enter the name "Gmail API Quickstart", and click the Create button
| A.6) Click OK to dismiss the resulting dialog
| A.7) Click the file_download (Download JSON) button to the right of the client ID
| A.8) Move this file to your "Credentials Folder" and rename it *client_secret.json*
| A.9) If you want to have multiple instances of the Gmail plugin for multiple Gmail accounts, copy the *client_secret.json* file to all "Credentials Folders"

| **B) Gmail plugin settings**
| B.1) Add the Gmail plugin to EventGhost
| B.2) In the main configuration dialog, set the path to the "Credentials Folder"
| B.3) Prefix setting is optional. This is especially important if you have multiple instances of the Gmail plugin for multiple Gmail accounts
| B.4) Press the OK button to close the configuration dialog
| B.5) If the *client_secret.json* file is in the "Credentials Folder", your default internet browser opens
| B.6) Choose the appropriate Gmail account and allow email to be sent using the Gmail plugin

Plugin version: %s

.. _OAuth:                https://en.wikipedia.org/wiki/OAuth
.. _this:                 https://console.developers.google.com/start/api?id=gmail
.. _`Google Developers`:  https://developers.google.com/
''' % version,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=9941",
)
import socket
if not hasattr(socket, 'errno'):
    import errno
    socket.errno = errno
from os import makedirs
from re import match
from base64 import urlsafe_b64encode
from mimetypes import guess_type
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 
from io import BytesIO 
from threading import Thread
from os.path import join, isfile, split, abspath, exists, basename
from json import loads
mod_pth = abspath(split(__file__)[0])
from sys import path as syspath
syspath.append(mod_pth + "\\lib")
import httplib2
import oauth2client
import oauth2client.file
from oauth2client import client, tools
from googleapiclient import errors, discovery

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_known_args()[0]
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
APPLICATION_NAME = 'Gmail API Python Send Email' 
ACV = wx.ALIGN_CENTER_VERTICAL
#===============================================================================

class Text:
    prefix     = "Event prefix:"
    folder     = 'Credentials Folder:'
    toolTipDir = 'Type name or click button to choose folder'
    browseDir  = 'Choose a folder'
    nofile     = u'%s: The "client_secret.json" file not found in the "%s" folder'
    noaddr     = u'%s: The "%s" address is not valid.'
    error      = u'%s: Email sending failed: %s'
    crdfld     = u'%s: Getting credentials failed: %s'
#===============================================================================

def as_bytes(self, unixfrom = False):
    """Return the entire formatted message as bytes.
        Optional `unixfrom' when True, means include the Unix From_ envelope
        header.
    """
    from email.generator import Generator
    fp = BytesIO()
    g = Generator(fp)
    g.flatten(self, unixfrom = unixfrom)
    return fp.getvalue()

MIMEMultipart.as_bytes = as_bytes
#===============================================================================

def validateEmailAddr(emailAddr):
    if len(emailAddr) > 5:
        if match(
            r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$",
            emailAddr
        ) != None:
            return True
    return False
#===============================================================================

class Gmail(eg.PluginClass):
    text = Text

    def __init__(self):
        self.AddActionsFromList(ACTIONS)


    def __start__(
        self,
        prefix = "",
        folder = None
    ):
        prefix = prefix if prefix else self.name
        self.info.eventPrefix = prefix
        if folder:
            if not exists(folder):
                makedirs(folder)
            self.client_secret_file = join(folder, "client_secret.json")
            if not isfile(self.client_secret_file):
                self.PrintError(self.text.nofile % (self.name, folder))
                return
            self.credential_path = join(folder, 'gmail-python-quickstart.json')
            if not isfile(self.credential_path):
                _ = self.get_credentials()


    def get_credentials(self):
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Returns:
            Credentials, the obtained credential.
        """
        store = oauth2client.file.Storage(self.credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_known_args()[0]
            flow = client.flow_from_clientsecrets(self.client_secret_file, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)
        return credentials
     

    def send_email(
        self,
        subject,
        to,
        cc,
        bcc,
        txt,
        attch,
        suffix
    ):
        if not validateEmailAddr(to):
            eg.PrintError(self.text.noaddr % (self.name, to))
            return
        if cc:
            cc_ = cc.split(",")
            cc = []
            for item in cc_:
                if validateEmailAddr(item.strip()):
                    cc.append(item)
            cc = ",".join(cc)
        if bcc:
            bcc_ = bcc.split(",")
            bcc = []
            for item in bcc_:
                if validateEmailAddr(item.strip()):
                    bcc.append(item)
            bcc = ",".join(bcc)
        try:
            credentials = self.get_credentials()
        except Exception, e:
            self.PrintError(self.text.crdfld % (self.name, e.message.decode(eg.systemEncoding)))
            return
        http = httplib2.Http()
        http = credentials.authorize(http)
        try:
            service = discovery.build('gmail', 'v1', http = http)
        except:
            eg.PrintTraceback()
            return
        message = MIMEMultipart()
        message['To'] = to
        #message['Disposition-notification-to'] = "me.me@gmail.com" # my address !
        if len(cc) > 4:
            message['Cc'] = cc
        if len(bcc) > 4:
            message['Bcc'] = bcc
        message['Subject'] = subject
        message.attach(MIMEText(txt.encode("utf-8"), 'plain', 'utf-8'))
        if isfile(attch):
            mmtp, encoding = guess_type(attch)
            if mmtp is None or encoding is not None:
                mmtp = 'application/octet-stream' 
            main_type, sub_type = mmtp.split('/', 1)
            if main_type == 'text':
                temp = open(attch)
                attachment = MIMEText(temp.read(), _subtype=sub_type)
                temp.close()
            elif main_type == 'image':
                temp = open(attch, 'rb')
                attachment = MIMEImage(temp.read(), _subtype=sub_type)
                temp.close()
            elif main_type == 'audio':
                temp = open(attch, 'rb')
                attachment = MIMEAudio(temp.read(), _subtype=sub_type)
                temp.close()            
            elif main_type == 'application' and sub_type == 'pdf':   
                temp = open(attch, 'rb')
                attachment = MIMEApplication(temp.read(), _subtype=sub_type)
                temp.close()
            else:                              
                attachment = MIMEBase(main_type, sub_type)
                temp = open(attch, 'rb')
                attachment.set_payload(temp.read())
                temp.close()
            filename = basename(attch)
            attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename = filename.encode('utf-8')
            )
            message.attach(attachment)
        body = {'raw': urlsafe_b64encode(message.as_bytes())}
        try:
            result = (service.users().messages().send(userId="me", body = body).execute())
            if suffix:
                self.TriggerEvent("Success.%s" % suffix, payload = (
                    subject,
                    to,
                    cc,
                    bcc,
                    txt,
                    attch,
                    suffix,
                    result['id']
                ))
        except errors.HttpError as error:
            errmsg = loads(error.content)['error']['message'].decode(eg.systemEncoding)
            if suffix:
                self.TriggerEvent("Failed.%s" % suffix, payload = (
                    subject,
                    to,
                    cc,
                    bcc,
                    txt,
                    attch,
                    suffix,
                    errmsg
                ))
            else:
                self.PrintError(self.text.error % (self.name, errmsg))
        except Exception, e:
            if hasattr(e, 'message') and len(e.message) > 0:
                errmsg = e.message.decode(eg.systemEncoding)
            elif hasattr(e, 'args') and len(e.args) > 1:
                errmsg = e.args[1].decode(eg.systemEncoding)
            elif hasattr(e, 'errno'):
                errmsg = str(e.errno)
            else:
                errmsg = "???"
            if suffix:
                self.TriggerEvent("Failed.%s" % suffix, payload = (
                    subject,
                    to,
                    cc,
                    bcc,
                    txt,
                    attch,
                    suffix,
                    errmsg
                ))
            else:
                self.PrintError(self.text.error % (self.name, errmsg))         


    def Configure(
        self,
        prefix = "",
        folder = ""
    ):
        panel = eg.ConfigPanel(self)
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        prefix = self.name if prefix == "" else prefix
        text = self.text
        prefixLabel = wx.StaticText(panel, -1, text.prefix)
        prefixCtrl = wx.TextCtrl(panel, -1, prefix)
        filepathLabel = wx.StaticText(panel, -1, text.folder)
        folder = folder if folder else join(eg.folderPath.Profile, ".credentials")
        filepathCtrl = eg.DirBrowseButton(
            panel,
            -1,
            toolTip = text.toolTipDir,
            dialogTitle = text.browseDir,
            buttonText = eg.text.General.browse,
            startDirectory = folder,
        )
        filepathCtrl.SetValue(folder)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(prefixLabel)
        topSizer.Add(prefixCtrl, 0, wx.TOP|wx.EXPAND, 2)
        topSizer.Add(filepathLabel, 0, wx.TOP|wx.EXPAND, 20)
        topSizer.Add(filepathCtrl, 0, wx.TOP|wx.EXPAND, 2)
        panel.sizer.Add(topSizer, 0, wx.EXPAND|wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                prefixCtrl.GetValue(),
                filepathCtrl.GetValue()
           )
#===============================================================================

class SendEmail(eg.ActionBase):

    def __call__(
        self,
        sbjct = '',
        To = '',
        Cc = '',
        Hidden = '',
        Txt = '',
        attch = '',
        suffix = ''
    ):
        sbjct = eg.ParseString(sbjct)
        To = eg.ParseString(To)
        Cc = eg.ParseString(Cc)
        Hidden = eg.ParseString(Hidden)
        Txt = eg.ParseString(Txt)
        attch = eg.ParseString(attch)
        suffix = eg.ParseString(suffix)
        smt = Thread(
            target=self.plugin.send_email,
            args=(
                sbjct,
                To,
                Cc,
                Hidden,
                Txt,
                attch,
                suffix
            )
        )
        smt.start()


    def Configure(
        self,
        sbjct = '',
        To = '',
        Cc = '',
        Hidden = '',
        Txt = '',
        attch = '',
        suffix = ''
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        panel.GetParent().GetParent().SetIcon(self.plugin.info.icon.GetWxIcon())
        subjectLbl=wx.StaticText(panel, -1, text.subjectLabel)
        subjectCtrl=wx.TextCtrl(panel,-1,sbjct)
        subjectLbl.SetToolTip(text.tip0)
        subjectCtrl.SetToolTip(text.tip0)
        toLbl=wx.StaticText(panel, -1, text.toLabel)
        toCtrl=wx.TextCtrl(panel,-1,To)
        toLbl.SetToolTip(text.tip1)
        toCtrl.SetToolTip(text.tip1)
        ccLbl=wx.StaticText(panel, -1, text.ccLabel)
        ccCtrl=wx.TextCtrl(panel,-1,Cc)
        ccLbl.SetToolTip(text.tip2)
        ccCtrl.SetToolTip(text.tip2)
        hdLbl=wx.StaticText(panel, -1, text.hdLabel)
        hdCtrl=wx.TextCtrl(panel,-1,Hidden)
        hdLbl.SetToolTip(text.tip3)
        hdCtrl.SetToolTip(text.tip3)

        textLbl=wx.StaticText(panel, -1, text.outText)
        outTextCtrl=wx.TextCtrl(
            panel,-1,'',size=(-1, 60),
            style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.HSCROLL|wx.TE_AUTO_URL|wx.TE_RICH2
        )
        outTextCtrl.SetValue(Txt)
        textLbl.SetToolTip(text.tip4)
        outTextCtrl.SetToolTip(text.tip4)        
        attchLbl=wx.StaticText(panel, -1, text.attch)
        attchCtrl = eg.FileBrowseButton(
            panel,
            -1,
            toolTip = text.tip5,
            dialogTitle = text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = eg.folderPath.Documents,
            initialValue = attch,
            fileMask = text.fileMask
        )
        attchLbl.SetToolTip(text.tip5)
        sfLbl=wx.StaticText(panel, -1, text.sfLabel)
        sfCtrl=wx.TextCtrl(panel, -1, suffix)
        sfLbl.SetToolTip(text.tip6)
        sfCtrl.SetToolTip(text.tip6)

        topSizer = wx.GridBagSizer(5, 5)
        topSizer.Add(subjectLbl,(0, 0),flag = wx.ALIGN_RIGHT|ACV)
        topSizer.Add(subjectCtrl, (0, 1), flag = wx.EXPAND)    

        topSizer.Add(toLbl,(1, 0),flag = wx.ALIGN_RIGHT|ACV)
        topSizer.Add(toCtrl, (1, 1), flag = wx.EXPAND)
        topSizer.Add(ccLbl,(2, 0),flag = wx.ALIGN_RIGHT|ACV)
        topSizer.Add(ccCtrl, (2, 1), flag = wx.EXPAND)
        topSizer.Add(hdLbl,(3, 0),flag = wx.ALIGN_RIGHT|ACV)
        topSizer.Add(hdCtrl, (3, 1), flag = wx.EXPAND)
        topSizer.Add(textLbl,(4, 0), flag = wx.ALIGN_RIGHT)
        topSizer.Add(outTextCtrl, (4, 1), flag = wx.EXPAND)
        topSizer.Add(attchLbl,(5, 0), flag = wx.ALIGN_RIGHT|ACV)
        topSizer.Add(attchCtrl, (5, 1), flag = wx.EXPAND)
        topSizer.Add(sfLbl,(6, 0), flag = wx.ALIGN_RIGHT|ACV)
        topSizer.Add(sfCtrl, (6, 1), flag = wx.EXPAND)
        topSizer.AddGrowableCol(1)
        topSizer.AddGrowableRow(4)
        panel.sizer.Add(topSizer,1,wx.EXPAND|wx.LEFT|wx.RIGHT,16)

        # re-assign the test button
        def OnTestButton(event):
            smt = Thread(
                target=self.plugin.send_email,
                args = (
                    subjectCtrl.GetValue(),
                    toCtrl.GetValue(),
                    ccCtrl.GetValue(),
                    hdCtrl.GetValue(),
                    outTextCtrl.GetValue(),
                    attchCtrl.GetValue(),
                    sfCtrl.GetValue()
                )
            )
            smt.start()
        panel.dialog.buttonRow.testButton.SetLabel(text.sendNow)
        panel.dialog.buttonRow.testButton.SetToolTip(text.tip7)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnTestButton)
        
        def validation(event=None):
            flag = True
            to_ = toCtrl.GetValue()
            if to_:
                if to_[0]=="{" and to_[-1]=="}":
                    pass
                elif not validateEmailAddr(to_):
                    flag = False
            else:
                flag = False
            cc_ = ccCtrl.GetValue()
            if cc_:
                if cc_[0]=="{" and cc_[-1]=="}":
                    pass
                else:
                    cc_ = cc_.split(",")
                    for item in cc_:
                        if not validateEmailAddr(item.strip()):
                            flag = False
                            break
            hd_ = hdCtrl.GetValue()
            if hd_:
                if hd_[0]=="{" and hd_[-1]=="}":
                    pass
                else:
                    hd_ = hd_.split(",")
                    for item in hd_:
                        if not validateEmailAddr(item):
                            flag = False
                            break
            if outTextCtrl.GetValue()=='':
                flag = False
            if subjectCtrl.GetValue()=='':
                flag = False
            panel.dialog.buttonRow.applyButton.Enable(flag)
            panel.dialog.buttonRow.okButton.Enable(flag)
    
        outTextCtrl.Bind(wx.EVT_TEXT, validation)
        subjectCtrl.Bind(wx.EVT_TEXT, validation)
        toCtrl.Bind(wx.EVT_TEXT, validation)
        ccCtrl.Bind(wx.EVT_TEXT, validation)
        hdCtrl.Bind(wx.EVT_TEXT, validation)
        validation()
        panel.sizer.Layout()
        
        while panel.Affirmed():
            panel.SetResult(
                subjectCtrl.GetValue(),
                toCtrl.GetValue(),
                ccCtrl.GetValue(),
                hdCtrl.GetValue(),
                outTextCtrl.GetValue(),
                attchCtrl.GetValue(),
                sfCtrl.GetValue()
            )
            
    class text:
        toLabel = 'To:'
        ccLabel = 'Copy:'
        hdLabel = 'Hidden copy:'
        sfLabel = 'Event suffix:'
        subjectLabel = 'Subject:'
        outText = "Text:"
        attch = "Attachment:"
        tip0 = """E-mail subject (required).
Here can be an expression as {eg.event.payload} too !"""
        tip1 = """Recipient's Address (required).
Here can be an expression as {eg.event.payload} too !"""
        tip2 = """One or more addresses of other recipients (optional).
If the addresses are more, then they are separated by a comma.
Here can be an expression as {eg.event.payload} too !"""
        tip3 = """One or more addresses of hidden recipients (optional).
If the addresses are more, then they are separated by a comma.
Here can be an expression as {eg.event.payload} too !"""
        tip4 = """The actual text (the body) of e-mail (required).
Here can be an expression as {eg.event.payload} too !"""
        tip5 = """The path to the file to be sent as an attachment (optional).
Type filename or click button to choose file.
Here can be an expression as {eg.event.payload} too !"""
        tip6 = """An event can be triggered when the email is sent.
If the field remains blank, no event will be triggered.
Here can be an expression as {eg.event.payload} too !"""
        tip7 = 'Send your e-mail now !'
        sendNow = 'Send now !'
        browseFile = 'Choose a file'
        fileMask = (
            "All files (*.*)|*.*"
        )
#===============================================================================

ACTIONS = (    
    (SendEmail,
        "SendEmail",
        "Send Email",
        "Sends Email.",
        None
    ),
)
#===============================================================================

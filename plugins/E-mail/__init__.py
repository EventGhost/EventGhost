# -*- coding: utf-8 -*-

version = "0.1.8"

# This file is part of EventGhost.
# Copyright (C) 2008-2013 Pako <lubos.ruckl@quick.cz>
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.1.8 by Pako 2013-03-25 08:42 UTC+1
#     - added wx.ComboBox for event suffix (action "Start observation")
#===============================================================================
#Structure of setup/account (one record):
#-----------------------------------------
#        labelCtrl             0
#        choiceType            1
#        userNameCtrl          2
#        mailAddressCtrl       3
#        replAddressCtrl       4
#        incServerCtrl         5
#        incPortCtrl           6
#        userLoginCtrl         7
#        outServerCtrl         8
#        choiceSecureCtrl      9
#        useSecureCtrl        10
#        userPasswordCtrl     11

#SMTP servers structure  (one record):
#-------------------------------------
#[0] = servName
#[1] = servAddress
#[2] = port
#[3] = secConnect
#[4] = secAutent
#[5] = userName
#[6] = userPassw

#texts structure (one record):  [txtName, txt]

#groups structure (one record): [groupName, [list of addresses]]

#tempData structure (one record):
#--------------------------------
#[0] observName
#[1] last count
#[2] array of messages: [id, subject, from, account,numAbs,numAccount], [], ...
#[3] Work thread
#[4] Notification Frame
#Empty record:['', 0, [], None, None]

# Configs (Start observation) structure (one record):
#----------------------------------------------------
#[0]=observName = string
#[1]=interval - integer
#[2]=[accounts] - list
#[3]=event name - string
#[4]=mode - integer (0-2)
#[5]=filter[[integer,integer,string],[],[],[],[],[],...]
#[6]=show notif window - boolean
#[7]=trigger event - boolean
#[8]=attach payload - integer (0, 1)
#[9]=Background Colour
#[10]=Foreground Colour
#[11]=trigger event2 - boolean
#[12]=event name2 - string
#[13]=attach payload2 - integer (0, 1, 2, 3)
#[14]=delete event - boolean
#===============================================================================

eg.RegisterPlugin(
    name = "E-mail",
    author = "Pako",
    version = version,
    kind = "other",
    guid = "{8BEB93CE-242E-46B5-A17A-D9737D362E1E}",
    createMacrosOnAdd = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEX////KysqhoaGA"
        "gIA+Pj4AAABVVVWfn5+2traPj48pKSkVFRUQEBALCwsGBgYNDQ0kJCRxcXG7u7ucnJwf"
        "Hx8aGhpkZGTS0tLc3NxhYWEXFxeDg4OkpKTAwMCwsLCZmZkiIiIICAgsLCyXl5fX19dX"
        "V1cDAwMzMzN9fX3CwsJmZmaSkpJDQ0O9vb1cXFw7OzvMzMzHx8eFhYWzs7NpaWkSEhKU"
        "lJQdHR1KSkpsbGxQUFBAQEDZ2dlNTU1fX194eHhubm57e3snJyempqZaWlpzc3NSUlKp"
        "qak2Njbe3t4xMTHFxcWurq7Pz8+NjY2rq6u4uLgAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAQADJwHjJwHgAAQQAAADJxqDJxqAAAFgAAAAAAAAAAAAAAAAAAAAAAADJ"
        "zKjJzEAAADQAAADJ/QzJ/QwAACQAAAAAAAAAAAAAAAAAAAAAAGgAABNBmXQAAAAAAADJ"
        "xwjJxwgAAIwAAAAAAAAAAAAAAAAAEAAAAADJydDJxpAAAGgAAADJxzzJxzwAAFgAAAAA"
        "AAAAAAAAAAAAAIAAAADJx8jJx8gAADQAAADJv/zJv/wAACQAAAAAAAAAACAAAAAAAAAA"
        "BeQAABNBmXQAAAAAAABhZgRhZgQAJvgAAAAAAAAAAAAAAAAAAAAIAABhZgRhZgQAJtQA"
        "AADJv/zJv/wAACQAAAAAAAAAAAAIAAAAAAAAADQAABNBmXQAAAAAAABhZgRhZgQAJpAA"
        "AAAAAAAAAAAAAAAAAAABAABhZgRhZgQAJmwAAADJyEDJyEAAAFgAAAAAAgAAAAAAAAAA"
        "AAAAAADJxfTJxYwAADQAAADJ/QzJ/QwAACQAAAAAAAAAAAAAAAAAAAAAAGjfdT5zAAAA"
        "AXRSTlMAQObYZgAAAAlwSFlzAAALEgAACxIB0t1+/AAAAf9JREFUeNqFU+ta2kAQXZRJ"
        "Yi4bIgQsNF2WyGIBK9bGFIsiarUqvbz/0/RsEiGg/Tp/dmfmfHPOzM4ytrbKzm6ViAzT"
        "Ym/Znu04rsc59x2nFuxvp+sNl0rmhc1WOX3wro2o3XlvRVH0QQRdItmL1/nDviIaHH1c"
        "BaxhSNQevbgtA/nxJutxTVIoCucTkTrJKSdCnLJKLOqm8Ii6kyz42VHUq+jbWXACKjHQ"
        "MtkXn/N+BmgQJef60nGKHqSUHmMDUqnmHaGBrzo/5SSTEOaRIg5mzMRAPCVydIEdCLcz"
        "pRfkacDkGzIzFqHA5QHC6D3NZQc5gF0RuWdsBOImvCgBkG0AhgDU2RwjDuDFbg4sAebE"
        "Vcq6nNMcnq0kXW8CjkiiXTRFC3h4oKxSCbBASv4PQCuK2msKaOA3bFGI3MXsh5uAgMjf"
        "Y6MkT9wCeJcDvpfaNJmFOdzDm2Gi1fz1rgvAPQARm2HCtQeNl4p+POqJ3EAcANYTRq0L"
        "+qQu9E43SCoHb5UvZztMOPla3bMucYzLslG8tl2VntSby9NsC6eu4uNszTooSpfxfv9l"
        "uY1M08xG7fz6LIQ4xBHHQptZrH4cQtXVT/ZvOw+xQ+PlOvC4jTZtjsW8+/Ub/yZa1uOm"
        "sV2j1Wx75a/nvKb5M2242d/l0nfc3ptSLNOAFnqa1x9OV8G/O1M0GpLUB68AAAAASUVO"
        "RK5CYII="
    ),
    description = (
        "Adds E-mail actions."
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1168",
)
from wx.lib.intctrl import IntCtrl as intCtrl
from threading import Thread, Event
from threading import enumerate as threnum
import time
import re
from copy import deepcopy as cpy
from eg.WinApi.Dynamic import BringWindowToTop, CreateEvent, SetEvent
import _winreg, os, win32api
import poplib, imaplib, smtplib
from email.header import decode_header
from email.Header import Header
from email.MIMEText import MIMEText
from email.Utils import parseaddr, formataddr,formatdate
import email.Parser as parser
myParser = parser.Parser()
#===============================================================================

def SendCfg(
    self,
    panel,
    sbjct,
    From,
    To,
    Copy,
    Txt,
    Append,
    toName,
    text,
    plugin
    ):
    self.plugin = plugin
    subjectLbl=wx.StaticText(panel, -1, text.subjectLabel)
    subjectCtrl=wx.TextCtrl(panel,-1,sbjct)
    fromLbl=wx.StaticText(panel, -1, text.fromLabel)
    choices = ["%s <%s> - %s" % (item[2],item[3],item[0]) for item in self.plugin.configs]
    fromCtrl=wx.Choice(panel,-1,choices = choices)
    fromCtrl.SetStringSelection(From)
    toLbl=wx.StaticText(panel, -1, text.toLabel)
    toNameCtrl=wx.TextCtrl(panel,-1,toName)
    toCtrl=wx.TextCtrl(panel,-1,To)
    copyLbl=wx.StaticText(panel, -1, text.copyLabel)
    choices = ['']
    choices.extend([item[0] for item in self.plugin.groups])
    copyCtrl=wx.Choice(panel,-1,choices = choices)
    copyCtrl.SetStringSelection(Copy)
    textLbl=wx.StaticText(panel, -1, text.outText)
    outTextCtrl=wx.TextCtrl(
        panel,-1,'',size=(-1, 60),
        style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.HSCROLL|wx.TE_AUTO_URL|wx.TE_RICH2
    )
    outTextCtrl.SetValue(Txt)
    textsLbl=wx.StaticText(panel, -1, text.outTexts)
    choices = ['']
    choices.extend([item[0] for item in self.plugin.texts])
    textsCtrl=wx.ComboBox(panel, -1, choices = choices, size = (200,-1))
    textsCtrl.SetValue(Append)
    toNameCtrl.SetToolTipString(text.tip1+'.\n'+text.tip)
    toCtrl.SetToolTipString(text.tip2+'.\n'+text.tip)
    outTextCtrl.SetToolTipString(text.tip)
    subjectCtrl.SetToolTipString(text.tip)
    textsCtrl.SetToolTipString(text.tip)

    topSizer = wx.GridBagSizer(5, 5)
    topSizer.Add(subjectLbl,(0, 0),flag = wx.ALIGN_RIGHT)
    topSizer.Add(subjectCtrl, (0, 1), (1, 2), flag = wx.EXPAND)
    topSizer.Add(fromLbl,(1, 0),flag = wx.ALIGN_RIGHT)
    topSizer.Add(fromCtrl, (1, 1), (1, 2), flag = wx.EXPAND)
    topSizer.Add(toLbl,(2, 0),flag = wx.ALIGN_RIGHT)
    topSizer.Add(toNameCtrl, (2, 1), flag = wx.EXPAND)
    topSizer.Add(toCtrl, (2, 2), flag = wx.EXPAND)
    topSizer.Add(copyLbl,(3, 0),flag = wx.ALIGN_RIGHT)
    topSizer.Add(copyCtrl, (3, 1), (1, 2), flag = wx.EXPAND)
    topSizer.Add(textLbl,(4, 0), flag = wx.ALIGN_RIGHT)
    topSizer.Add(outTextCtrl, (4, 1), (1, 2), flag = wx.EXPAND)
    topSizer.Add(textsLbl,(5, 0),flag = wx.ALIGN_RIGHT)
    topSizer.Add(textsCtrl, (5, 1), (1, 2), flag = wx.EXPAND)
    topSizer.AddGrowableCol(1)
    topSizer.AddGrowableCol(2)
    topSizer.AddGrowableRow(4)

    return (subjectCtrl,
        fromCtrl,
        toCtrl,
        copyCtrl,
        outTextCtrl,
        textsCtrl,
        toNameCtrl,
        topSizer
    )

#===============================================================================

def validateEmailAddr(emailAddr):
    if len(emailAddr) > 5:
        if re.match(
            r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$",
            emailAddr
        ) != None:
            return True
    return False


def DecodeSection(section, coding=None):
    if coding:
        List = (coding, 'utf-8', 'iso-8859-1', 'us-ascii')
    else:
        List = ('utf-8', 'iso-8859-1', 'us-ascii')
    for charset in List:
        try:
            section = section.decode(charset,'strict')
#        except UnicodeError:
        except:
            pass
        else:
            return section.strip(' "')

    for charset in List:
        try:
            section = section.decode(charset,'replace')
#        except UnicodeError:
        except:
            pass
        else:
            return section.strip(' "')
    return u''


def ParseItem(item):
    x = decode_header(item)[0]
    if x[1]:
        return DecodeSection(x[0],x[1])
    else:
        return x[0]


def ParseAddress(item):
    parseAddr = parseaddr(item)
    if parseAddr[0] == '':
        return parseAddr[1]
    decAddr = decode_header(parseAddr[0])[0]
    if not decAddr[1]:
        return parseAddr[0]
    else:
        return DecodeSection(decAddr[0], decAddr[1])
#===============================================================================

def GetParts(msg, ext = False):
    from email.Iterators import typed_subpart_iterator
    partCounter=0
    bodyText=[]
    def get_charset(part, default="ascii"):
        """Get the part charset"""
        if part.get_content_charset():
            return part.get_content_charset()
        if part.get_charset():
            return part.get_charset()
        return default

    def get_body(message):
        """Get the body of the email message"""
#ToDo : option choice for html part viewing
        if message.is_multipart():
            #get the text (plain or html) version only
            text_parts = [part
#                          for part in typed_subpart_iterator(message,
#                                                             'text',
#                                                             'plain')]
                          for part in typed_subpart_iterator(message, 'text')]
            body = []
            for part in text_parts:
                charset = get_charset(part, get_charset(message))
                try:
                    body.append(unicode(part.get_payload(decode=True),
                                    charset,
                                    "replace"))
                except:
                    body.append(unicode(part.get_payload(decode=True),
                                    'us-ascii',
                                    "replace"))
            return u"\n".join(body).strip()+u"\n"

        else: # if it is not multipart, the payload will be a string
              # representing the message body
            try:
                body = unicode(message.get_payload(decode=True),
                               get_charset(message),
                               "replace")
            except:
                body = unicode(message.get_payload(decode=True),
                               'us-ascii',
                               "replace")
            return body.strip()+u"\n"

    if not ext:
        return [ParseItem(msg['Subject']),msg['From'], get_body(msg)]
    else:
        return [
            ParseItem(msg['Subject']),
            msg['From'],
            get_body(msg),
            None,
            None,
            msg['References'],
            msg['Reply-To'],
            msg['Message-ID'],
            msg['X-Original-To'] if msg.has_key('X-Original-To') else parseaddr(msg['To'])[1],
        ]
#===============================================================================

def RunEmailClient(text):
    """Get the path of default email client through querying the
        Windows registry. """
    try:
        em_reg = _winreg.OpenKey(
            _winreg.HKEY_CLASSES_ROOT,
            "\\mailto\\shell\\open\\command"
        )
        EmPath = _winreg.EnumValue(em_reg,0)[1]
        _winreg.CloseKey(em_reg)
        EmPath = EmPath.split('"')[1]
    except:
        eg.PrintError(text.error9)
    else:
        head, tail = os.path.split(EmPath)
        win32api.ShellExecute(
            0,
            None,
            tail,
            None,
            head,
            1
        )
#===============================================================================

def Move(lst,index,direction):
    tmpList = lst[:]
    max = len(lst)-1
    #Last to first position, other down
    if index == max and direction == 1:
        tmpList[1:] = lst[:-1]
        tmpList[0] = lst[max]
        index2 = 0
    #First to last position, other up
    elif index == 0 and direction == -1:
        tmpList[:-1] = lst[1:]
        tmpList[max] = lst[0]
        index2 = max
    else:
        index2 = index+direction
        tmpList[index] = lst[index2]
        tmpList[index2] = lst[index]
    return index2,tmpList
#===============================================================================

class MessageFrame(wx.MiniFrame):
    def __init__(self, parent, message):
        self.message = message
        self.setup = parent.setup
        wx.MiniFrame.__init__(
            self,
            None,
            -1,
            '',
            size=(-1, -1),
            style=wx.CAPTION|wx.RESIZE_BORDER
        )
        self.parent = parent
        self.plugin = parent.plugin
        self.SetBackgroundColour(wx.NullColour)
        self.id = self.plugin.tempData[self.message[3]][2][int(self.message[4][0])-1][0]

    def ShowMessageFrame(
        self, position, size
    ):

        text = self.plugin.text
        self.setTitle()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        centralSizer = wx.GridBagSizer(10, 10)
        centralSizer.AddGrowableRow(0)
        centralSizer.AddGrowableCol(1)
        centralSizer.AddGrowableCol(3)
        centralSizer.AddGrowableCol(5)
        self.messageCtrl = wx.TextCtrl(
            self,
            -1,
            '', #wx.TE_AUTO_URL not works
            style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_AUTO_URL|wx.TE_RICH2
        )
        self.messageCtrl.SetValue(self.message[2]) #wx.TE_AUTO_URL activation
        #Buttons
        sizes = []
        sizes.append(self.GetTextExtent(text.delete)[0])
        sizes.append(self.GetTextExtent(text.client)[0])
        sizes.append(self.GetTextExtent(text.reply)[0])
        sizes.append(self.GetTextExtent(text.close)[0])
        w=max(sizes)+12
        self.deleteButton = wx.Button(self, -1, text.delete, size=((w,-1)))
        self.clientButton = wx.Button(self, -1, text.client, size=((w,-1)))
        self.replyButton = wx.Button(self, -1, text.reply, size=((w,-1)))
        self.closeButton = wx.Button(self, -1, text.close, size=((w,-1)))
        centralSizer.Add(self.messageCtrl, (0,0),(1,7), flag = wx.EXPAND)
        centralSizer.Add(self.deleteButton,(1,0), flag = wx.ALIGN_LEFT|wx.BOTTOM,border = 10)
        centralSizer.Add(self.clientButton,(1,2), flag = wx.ALIGN_CENTER_HORIZONTAL)
        centralSizer.Add(self.replyButton,(1,4), flag = wx.ALIGN_CENTER_HORIZONTAL)
        centralSizer.Add(self.closeButton,(1,6), flag = wx.RIGHT)
        mainSizer.Add(centralSizer, 1,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,10)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.Layout()

        def onURLclick(event):
            if event.MouseEvent.LeftDown():
                url = event.GetEventObject().GetValue()[event.GetURLStart(): event.GetURLEnd()]
                wx.LaunchDefaultBrowser(url)
            else:
                event.Skip()
        self.messageCtrl.Bind(wx.EVT_TEXT_URL,onURLclick)

        def OnCloseWindow(event):
            self.parent.messFramSize = self.GetSize()
            self.parent.messFramPosition = self.GetPosition()
            self.Destroy()
            event.Skip()
        self.Bind(wx.EVT_CLOSE, OnCloseWindow)

        def onCloseButton(evt):
            self.Close(True)
        self.closeButton.Bind(wx.EVT_BUTTON, onCloseButton)

        def onClientButton(evt):
            RunEmailClient(text)
        self.clientButton.Bind(wx.EVT_BUTTON, onClientButton)

        def onReplyButton(evt):
            addressList = [item[3] for item in self.plugin.configs]
            if self.message[8] in addressList:
                indx = addressList.index(self.message[8])
            else:
                indx = 0
            From = ["%s <%s> - %s" % (item[2],item[3],item[0]) for item in self.plugin.configs][indx]
            sbjct = u"Re: "+self.message[0]
            replAddr = parseaddr(self.message[6])
            fromAddr = parseaddr(self.message[1])
            if replAddr[1] != '':
                To = replAddr[1]
            else:
                To = fromAddr[1]
            if replAddr[0] != '':
                toName = ParseAddress(self.message[6])
            elif fromAddr[0] != '':
                toName = ParseAddress(self.message[1])
            else:
                toName = ''
            #if self.message[5] is None:
            body = self.message[2].split('\n')
            sender = ParseAddress(self.message[1])
            reBody = [text.wrote % sender]
            reBody.append('')
            for line in body:
                reBody.append('> '+line)
            reBody = u'\n'.join(reBody)

            myDlg = SendMailDlg(parent = self)
            myDlg.ShowSendMailDlg(
                sbjct=sbjct,
                From = From,
                To = To,
                Txt = reBody,
                toName = toName,
                text = SendEmail.text,
                plugin = self.plugin,
                references = self.message[5],
                messageID = self.message[7],
            )
        self.replyButton.Bind(wx.EVT_BUTTON, onReplyButton)

        def onDeleteButton(evt):
            wx.CallAfter(self.parent.deleteEmails,self.message[3], self.message[4], True)
            self.messageCtrl.ChangeValue('')
            self.parent.Refresh()
            time.sleep(1)
            self.Close(True)
        self.deleteButton.Bind(wx.EVT_BUTTON, onDeleteButton)

        self.SetMinSize(self.GetSize())
        self.SetSize(size)
        self.SetPosition(position)
        self.Show(True)

    def getEmailNum(self):
        return self.message[4][0]

    def setTitle(self):
        title = ('%s-%s | %s: %s' % (
            self.setup[0],
            self.message[4][0],
            ParseAddress(self.message[1]),
            self.message[0]
        ))
        if len(title) > 68:
            title = title[:65]+'...'
        self.SetTitle(title)

    def Unblock(self, unblock):
        if unblock:
            data = self.plugin.tempData[self.message[3]][2]
            try:
                ix = [item[0] for item in data].index(self.id)
                self.message[4][0] = data[ix][4]
                self.setTitle()
            except:
                self.Close(True)
            colour = self.GetForegroundColour()
        else:
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        self.messageCtrl.SetForegroundColour(colour)
        self.deleteButton.Enable(unblock)
        self.clientButton.Enable(unblock)
        self.closeButton.Enable(unblock)
        self.Refresh()
        self.Enable(unblock)
#===============================================================================

class DetailsFrame(wx.MiniFrame):
    messageFrame = None
    messFramSize = (-1, -1)
    messFramPosition = (-1, -1)

    def __init__(self, parent):
        self.parent = parent
        self.plugin = parent.plugin
        self.passINC = self.plugin.passINC
        self.setup = parent.setup
        wx.MiniFrame.__init__(
            self,
            None,
            -1,
            size=(-1, -1),
            style=wx.CAPTION|wx.RESIZE_BORDER
        )
        self.SetBackgroundColour(wx.NullColour)
        self.menuFlagS = False
        self.menuFlagD = False
        self.delFlag = False


    def ShowDetailsFrame(
        self,
        position,
        size
    ):
        self.text = self.plugin.text
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        centralSizer = wx.GridBagSizer(10, 10)
        centralSizer.AddGrowableRow(0)
        centralSizer.AddGrowableCol(1)
        centralSizer.AddGrowableCol(3)
        centralSizer.AddGrowableCol(5)
        centralSizer.AddGrowableCol(7)
        self.messagesListCtrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)
        for i, labelsDetails in enumerate(self.text.labelsDetails):
            self.messagesListCtrl.InsertColumn(
                i,
                labelsDetails,
            )
        centralSizer.Add(self.messagesListCtrl, (0,0),(1,9), flag = wx.EXPAND)

        #Buttons
        sizes = []
        sizes.append(self.GetTextExtent(self.text.show)[0])
        sizes.append(self.GetTextExtent(self.text.delete)[0])
        sizes.append(self.GetTextExtent(self.text.refresh)[0])
        sizes.append(self.GetTextExtent(self.text.client)[0])
        sizes.append(self.GetTextExtent(self.text.close)[0])
        w=max(sizes)+12
        self.showButton = wx.Button(self, -1, self.text.show,size=((w,-1)))
        self.deleteButton = wx.Button(self, -1, self.text.delete,size=((w,-1)))
        self.refreshButton = wx.Button(self, -1, self.text.refresh,size=((w,-1)))
        self.clientButton = wx.Button(self, -1, self.text.client,size=((w,-1)))
        self.closeButton = wx.Button(self, -1, self.text.close,size=((w,-1)))
        centralSizer.Add(self.showButton,(1,0), flag = wx.ALIGN_LEFT|wx.BOTTOM,border = 10)
        centralSizer.Add(self.deleteButton,(1,2), flag = wx.ALIGN_CENTER_HORIZONTAL)
        centralSizer.Add(self.refreshButton,(1,4), flag = wx.ALIGN_CENTER_HORIZONTAL)
        centralSizer.Add(self.clientButton,(1,6), flag = wx.ALIGN_CENTER_HORIZONTAL)
        centralSizer.Add(self.closeButton,(1,8), flag = wx.ALIGN_RIGHT)
        self.messagesListCtrl.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        self.messagesListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.ListSelection)
        self.messagesListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.ListSelection)

        def OnSize(event):
            self.messagesListCtrl.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER)
            event.Skip()

        self.Refresh()
        self.Bind(wx.EVT_SIZE, OnSize)
        mainSizer.Add(centralSizer, 1,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,10)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        sizes = (40,75,200,200)
        for i in range(4):
            self.messagesListCtrl.SetColumnWidth(i, sizes[i])
        mainSizer.Layout()

        def OnCloseWindow(event):
            self.parent.detFramePosition = self.GetPosition()
            self.parent.detFrameSize = self.GetSize()
            if self.messageFrame:
                self.messageFrame.Close()
            self.Destroy()
            event.Skip()

        self.Bind(wx.EVT_CLOSE, OnCloseWindow)
        self.closeButton.Bind(wx.EVT_BUTTON, self.onCloseButton)
        self.deleteButton.Bind(wx.EVT_BUTTON, self.onDeleteButton)
        self.clientButton.Bind(wx.EVT_BUTTON, self.onClientButton)
        self.showButton.Bind(wx.EVT_BUTTON, self.onShowButton)
        self.refreshButton.Bind(wx.EVT_BUTTON, self.onRefresh)
        self.messagesListCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onShowButton) #Doubleclick
        self.SetMinSize((565,160))
        self.SetSize(size)
        self.SetPosition(position)
        self.Show(True)

    def onRefresh(self,evt):
        self.Unblock(False)
        indx = [i[0] for i in self.plugin.tempData].index(self.setup[0])
        wt = self.plugin.tempData[indx][3]
        wt.operate(True)
        evt.Skip()

    def onShowButton(self, evt):
        item = self.messagesListCtrl.GetFirstSelected()
        nbr = self.messagesListCtrl.GetItemText(item)
        sel=[nbr]
        indx = [i[0] for i in self.plugin.tempData].index(self.setup[0])
        message = self.RealizeAction(indx, sel, 1) # 1 ~ mode 'show'
        if message:
            if self.messageFrame:
                self.messageFrame.Close()
            self.messageFrame = MessageFrame(
                parent = self,
                message = message,
            )
            wx.CallAfter(
                self.messageFrame.ShowMessageFrame,
                position = self.messFramPosition,
                size = self.messFramSize,
            )
        evt.Skip()

    def onCloseButton(self, evt):
        self.Close(True)

    def deleteEmails(self, indx, sel, close = False):
        self.delFlag = True
        if close:
            self.messageFrame.Close()
        else:
            if self.messageFrame:
                num = self.messageFrame.getEmailNum()
                rec = self.plugin.tempData[indx][2][int(num)-1]
                if num in sel or rec[0] == rec[2]:
                    self.messageFrame.Close()
                else:
                    self.messageFrame.Enable(False)
        self.Unblock(False)
        wt = self.plugin.tempData[indx][3]
        wt.DeleteAction((indx, sel, 0,self))

    def onDeleteButton(self, evt):
        item = self.messagesListCtrl.GetFirstSelected()
        sel = []
        while item != -1:
            nbr = self.messagesListCtrl.GetItemText(item)
            sel.append(nbr)
            item = self.messagesListCtrl.GetNextSelected(item)
        indx = [i[0] for i in self.plugin.tempData].index(self.setup[0])
        self.deleteEmails(indx, sel)
        evt.Skip()

    def onClientButton(self, evt):
        RunEmailClient(self.text)

    def ListSelection(self, event=None):
        if self.messageFrame:
            self.messageFrame.Raise()
        self.menuFlagS = self.messagesListCtrl.GetSelectedItemCount() == 1
        self.showButton.Enable(self.menuFlagS)
        self.menuFlagD = self.messagesListCtrl.GetFirstSelected() != -1
        self.deleteButton.Enable(self.menuFlagD)
        if event:
            event.Skip()

    def Disappear(self):
        if self.delFlag:
            self.Show(False)
        else:
            self.Close()

    def resDelFlag(self):
        self.delFlag = False

    def isCloseReq(self):
        return self.delFlag and not self.IsShown()

    def Refresh(self, event=None):
        observName = self.setup[0]
        indx = [item[0] for item in self.plugin.tempData].index(observName)
        self.messagesListCtrl.DeleteAllItems()
        row = 0
        for item in self.plugin.tempData[indx][2]:
            self.messagesListCtrl.InsertStringItem(row, item[4])
            self.messagesListCtrl.SetStringItem(row, 1,item[3])
            self.messagesListCtrl.SetStringItem(row, 2, item[1])
            self.messagesListCtrl.SetStringItem(row, 3, item[2])
            row += 1
        self.SetTitle(self.plugin.text.detTitle % (self.setup[0],str(row)))
        label = self.parent.GetNum()
        if label != row:
            self.parent.SetNum(row)
        self.Unblock(True)
        self.ListSelection()

    def Unblock(self, unblock):
        if unblock:
            colour = self.GetForegroundColour()
        else:
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        self.messagesListCtrl.SetTextColour(colour)
        self.deleteButton.Enable(unblock)
        self.refreshButton.Enable(unblock)
        self.clientButton.Enable(unblock)
        self.closeButton.Enable(unblock)
        self.showButton.Enable(unblock)
        self.messagesListCtrl.Refresh()
        self.Enable(unblock)
        if self.messageFrame:
            self.messageFrame.Unblock(unblock)

    def OnRightClick(self, event):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.onShowButton, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.onDeleteButton, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.onRefresh, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.onClientButton, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.onCloseButton, id=self.popupID5)
        # make a menu
        menu = wx.Menu()
        # add some items
        if self.menuFlagS:
            menu.Append(self.popupID1, self.text.popup[0])
        if self.menuFlagD:
            menu.Append(self.popupID2, self.text.popup[1])
        menu.Append(self.popupID3, self.text.popup[2])
        menu.Append(self.popupID4, self.text.popup[3])
        menu.Append(self.popupID5, self.text.popup[4])
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def RealizeAction(self, indx, sel, mode):
        obsData = self.plugin.tempData[indx][2]
        observName = self.plugin.tempData[indx][0]
        resultMessage = None
        oldAccount = ''
        m = len(sel)-1
        item = sel[m]
        ix = [i[4] for i in obsData].index(item)
        iac = [cfg[0] for cfg in self.plugin.configs].index(obsData[ix][3])
        account =  self.plugin.configs[iac]
        while m > -1:
            while oldAccount == account:
                id = obsData[ix][5]
                if account[1] == 0: #POP3
                    lst = mailbox.list()[1]
                    cnt = len(lst)
                    if cnt >= int(id):
                        MAXLINES=100 #ToDo :  MAXLINES choice
                        if mode == 0:
                            MAXLINES = 0 #Delete -> not need read
                        resp, txt, octets = mailbox.top(id, MAXLINES)
                        if resp != '+OK':
                            resp, txt, octets = mailbox.retr(id)
                        txt = "\n".join(txt)
                        msg=myParser.parsestr(txt)
                        if msg.has_key('Message-Id'):
                            messId =  msg['Message-Id']
                        else:
                            messId = ParseAddress(msg['From'])
                        if messId == obsData[ix][0]:
                            if mode == 1:
                                resultMessage = GetParts(msg, True)
                                resultMessage[3] = indx
                                resultMessage[4] = sel
                            else: #mode = 0 ~ delete
                                mailbox.dele(id)

                else:               #IMAP
                    typ, txt = mailbox.select('INBOX') #Folder selection
                    if txt[0]:
                        if mode == 1:
                            typ, txt = mailbox.fetch(id, '(RFC822)')
                            mailbox.store(id, "-FLAGS", '(\Seen)') #Reset UNSEEN flag
                        else:
                            typ, txt = mailbox.fetch(id, '(RFC822.HEADER)')
                        txt = txt[0][1]
                        msg = myParser.parsestr(txt)
                        if msg.has_key('Message-Id'):
                            messId =  msg['Message-Id']
                        else:
                            messId = ParseAddress(msg['From'])
                        if messId == obsData[ix][0]:
                            if mode == 1:
                                resultMessage = GetParts(msg, True)
                                resultMessage[3] = indx
                                resultMessage[4] = sel
                            else: #mode = 0 ~ delete
                                mailbox.store(id, "+FLAGS", '(\Deleted)')
                m -= 1
                if m == -1:
                    break
                else:
                    item = sel[m]
                    ix = [i[4] for i in obsData].index(item)
                    iac = [cfg[0] for cfg in self.plugin.configs].index(obsData[ix][3])
                    account =  self.plugin.configs[iac]

            if oldAccount != '':
                if account[1] == 0: #POP
                    mailbox.quit()
                else:               #IMAP
                    mailbox.expunge()
                    mailbox.logout()
            if m == -1:
                break
            Error = True
            while Error:
                oldAccount = account
                SERVER = account[5]
                PORT = account[6]
                USER = account[7]
                PASSWORD = self.passINC.data[account[0]]
                USE_SSL = account[9] == 3
                Error = False
                if account[1] == 0: #POP
                    try:
                        if USE_SSL:
                            mailbox = poplib.POP3_SSL(SERVER, PORT)
                        else:
                            mailbox = poplib.POP3(SERVER, PORT)
                    except:
                        eg.PrintError(self.text.error0+' '+self.text.error1 % (SERVER,PORT))
                        Error = True
                    else:
                        #mailbox.set_debuglevel(5)
                        try:
                            mailbox.user(USER)
                            mailbox.pass_(PASSWORD)
                        except poplib.error_proto, errmsg:
                            eg.PrintError(self.text.error0+' '+str(errmsg))
                            Error = True
                            mailbox.quit()

                else:               #IMAP
                    try:
                        if USE_SSL:
                            mailbox = imaplib.IMAP4_SSL(SERVER, PORT)
                        else:
                            mailbox = imaplib.IMAP4(SERVER, PORT)
                    except:
                        eg.PrintError(self.text.error2+' '+self.text.error3 % (SERVER,PORT))
                        Error = True
                    else:
                        try:
                            mailbox.login(USER, PASSWORD)
                        except:
                            eg.PrintError(self.text.error2+' '+self.text.error4 % (USER, SERVER, PORT))
                            Error = True
                            mailbox.logout()
                if Error:
                    while oldAccount == account:
                        m -= 1
                        if m == -1:
                            Error = False
                            break
                        else:
                            item = sel[m]
                            ix = [i[4] for i in obsData].index(item)
                            iac = [cfg[0] for cfg in self.plugin.configs].index(obsData[ix][3])
                            account =  self.plugin.configs[iac]

        return resultMessage
#===============================================================================

class NotifFrame(wx.MiniFrame):
    detailsFrame = None
    detFramePosition = (-1,-1)
    detFrameSize = (-1,-1)

    def __init__(self, parent):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            '',
            size = (120, 60),
            style = wx.STAY_ON_TOP|wx.CAPTION
        )

    def ShowNotifFrame(
        self,
        plugin,
        stp,
        event=None
    ):
        self.plugin = plugin
        self.setup = stp
        self.SetTitle('  '+self.setup[0])
        self.SetBackgroundColour(self.setup[9])
        self.SetForegroundColour(self.setup[10])
        text = self.plugin.text
        tip = text.tip0
        self.label = wx.StaticText(self, -1, '')
        label2 = wx.StaticText(self,-1,text.notifLabel)
        font = self.label.GetFont()
        font.SetPointSize(20)
        self.label.SetFont(font)
        w = self.label.GetTextExtent(' 888 ')[0]
        self.label.SetPosition((0,1))
        label2.SetPosition((w,4))
        self.label.SetToolTipString(tip)
        label2.SetToolTipString(tip)
        self.Refresh()

        def OnCloseWindow(event):
            if self.detailsFrame:
                self.detailsFrame.Disappear()
            self.Destroy()
            event.Skip()
        self.Bind(wx.EVT_CLOSE, OnCloseWindow)

        def OnDoubleClick(evt):
            if evt.ControlDown(): #with CTRL
                RunEmailClient(text)
            else:                 #without CTRL
                if self.detailsFrame:
                    BringWindowToTop(self.detailsFrame.GetHandle())
                else:
                    self.detailsFrame = DetailsFrame(parent = self)
                    wx.CallAfter(
                        self.detailsFrame.ShowDetailsFrame,
                        position = self.detFramePosition,
                        size = self.detFrameSize
                    )

        self.Bind(wx.EVT_LEFT_DCLICK, OnDoubleClick)
        self.label.Bind(wx.EVT_LEFT_DCLICK, OnDoubleClick)
        label2.Bind(wx.EVT_LEFT_DCLICK, OnDoubleClick)

        def OnRightClick(evt):
            if self.detailsFrame:
                self.detailsFrame.Disappear()
            self.Show(False)
        self.Bind(wx.EVT_RIGHT_UP, OnRightClick)
        self.label.Bind(wx.EVT_RIGHT_UP, OnRightClick)
        label2.Bind(wx.EVT_RIGHT_UP, OnRightClick)
        BringWindowToTop(self.GetHandle())
        wx.Yield()
        SetEvent(event)

    def Disappear(self, close=False):
        if self.detailsFrame:
            self.detailsFrame.Disappear()
        if not close:
            self.Show(False)
        else:
            self.Close()

    def GetNum(self):
        return int(self.label.GetLabel())

    def SetNum(
        self,
        label="",
    ):
        lbl = str(label)
        if label<10:
            lbl = "  %s  " % lbl
        elif label<100:
            lbl = "  %s " % lbl
        else:
            lbl = " %s " % lbl
        self.label.SetLabel(lbl)
        if self.detailsFrame:
            wx.CallAfter(self.detailsFrame.Refresh)
#===============================================================================

class outServerDialog(wx.MiniFrame):
    oldSel = 0
    def __init__(self, parent, plugin):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION,
            name="Servers dialog"
        )
        self.panel = parent
        self.passSMTP = {}
        for i,item in list(enumerate(self.panel.passSMTP)):
            self.passSMTP[item]=self.panel.passSMTP[item]
        self.plugin = plugin
        self.servers = cpy(self.panel.servers)
        self.cfgs = cpy(self.panel.cfgs)
        self.val = self.panel.outServerCtrl.GetStringSelection()
        self.SetBackgroundColour(wx.NullColour)
#===============================================================================

    def ShowOutServDlg(self):
        def boxEnable(enable):
            labelCtrl.Enable(enable)
            labelLbl.Enable(enable)
            outServerLbl.Enable(enable)
            outServerCtrl.Enable(enable)
            outPortLbl.Enable(enable)
            outPortCtrl.Enable(enable)
            choiceSecureLbl.Enable(enable)
            choiceSecureCtrl.Enable(enable)
            useSecureCtrl.Enable(enable)

        def setValue(item):
            labelCtrl.ChangeValue (item[0])
            outServerCtrl.SetValue(item[1])
            outPortCtrl.SetValue(item[2])
            choiceSecureCtrl.SetSelection(item[3])
            useSecureCtrl.SetValue(item[4])
            userCtrl.SetValue(item[5])
            if item[0] != '' and item[0] in self.passSMTP:
                passwCtrl.ChangeValue(self.passSMTP[item[0]])
            else:
                passwCtrl.ChangeValue('')

        def validation():
            flag = True
            label = labelCtrl.GetValue()
            if label == "":
                flag = False
            else:
                if [n[0] for n in self.servers].count(label)!=1:
                    flag = False
            if outServerCtrl.GetValue() == '':
                flag = False
            if outPortCtrl.GetValue() < 0:
                flag = False
            if useSecureCtrl.GetValue():
                if userCtrl.GetValue() == '' or passwCtrl.GetValue() == '':
                    flag = False
            btn1.Enable(flag)
            btnApp.Enable(flag)

        text = self.plugin.text
        self.SetTitle(text.outServerTitle)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.SetMinSize((450, 308))
        leftSizer = wx.FlexGridSizer(4,2,2,8)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        previewLbl=wx.StaticText(self, -1, text.serversList)
        listBoxCtrl=wx.ListBox(
            self,-1,
            size=wx.Size(120,106),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        labelLbl=wx.StaticText(self, -1, text.servLabel)
        labelCtrl=wx.TextCtrl(self,-1,'')
        box = wx.StaticBox(self,-1,text.servParam)
        rightSizer = wx.StaticBoxSizer(box,wx.VERTICAL)
        #Box content
        outServerLbl=wx.StaticText(self, -1, text.outServer)
        outServerCtrl=wx.TextCtrl(self,-1,'')
        outPortLbl=wx.StaticText(self, -1, text.incPort)
        outPortCtrl=intCtrl(self,-1,25,size=(50,-1))
        choiceSecureLbl =wx.StaticText(self, -1, text.secureConnectLabel)
        choiceSecureCtrl = wx.Choice(
            self,
            -1,
            choices=(text.secureConnectChoice2),
        )
        choiceSecureCtrl.SetMaxSize((194,-1))
        useSecureCtrl = wx.CheckBox(self, label = text.useName)
        userLbl=wx.StaticText(self, -1, text.userLogin)
        userCtrl=wx.TextCtrl(self,-1,'')
        userCtrl.SetMaxSize((194,-1))
        passwLbl=wx.StaticText(self, -1, text.userPassword)
        passwCtrl=wx.TextCtrl(self,-1,'',style = wx.TE_PASSWORD)
        passwCtrl.SetMaxSize((194,-1))
        serverSizer = wx.BoxSizer(wx.HORIZONTAL)
        serverSizerL = wx.BoxSizer(wx.VERTICAL)
        serverSizerR = wx.BoxSizer(wx.VERTICAL)
        serverSizer.Add(serverSizerL,1,wx.EXPAND)
        serverSizer.Add(serverSizerR,0,wx.EXPAND|wx.LEFT,5)
        serverSizerL.Add(outServerLbl,0,wx.EXPAND)
        serverSizerL.Add(outServerCtrl,0,wx.EXPAND)
        serverSizerR.Add(outPortLbl,0,wx.EXPAND|wx.LEFT,3)
        serverSizerR.Add(outPortCtrl,0,wx.EXPAND)
        rightSizer.Add(choiceSecureLbl,0,wx.TOP,5)
        rightSizer.Add(choiceSecureCtrl,0,wx.EXPAND|wx.TOP,3)
        rightSizer.Add(serverSizer,0,wx.EXPAND|wx.TOP,10)
        rightSizer.Add(useSecureCtrl,0,wx.TOP,16)
        rightSizer.Add(userLbl,0,wx.TOP,5)
        rightSizer.Add(userCtrl,0,wx.EXPAND|wx.TOP|wx.BOTTOM,3)
        rightSizer.Add(passwLbl,0,wx.TOP,5)
        rightSizer.Add(passwCtrl,0,wx.EXPAND|wx.TOP|wx.BOTTOM,3)
        rightSizer.Add((1,3))
        leftSizer.Add(previewLbl,0,wx.TOP,5)
        leftSizer.Add((1,1))
        leftSizer.Add(listBoxCtrl,0,wx.TOP,5)
        leftSizer.Add(topMiddleSizer,0,wx.TOP,5)
        leftSizer.Add(labelLbl,0,wx.TOP,3)
        leftSizer.Add((1,1))
        leftSizer.Add(labelCtrl,0,wx.EXPAND)
        leftSizer.Add((1,1))
        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(self, -1, bmp)
        btnUP.Enable(False)
        topMiddleSizer.Add(btnUP)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(self, -1, bmp)
        btnDOWN.Enable(False)
        topMiddleSizer.Add(btnDOWN,0,wx.TOP,3)
        #Buttons 'Delete' and 'Insert new'
        w1 = self.GetTextExtent(text.delete)[0]
        w2 = self.GetTextExtent(text.insert)[0]
        if w1 > w2:
            btnDEL=wx.Button(self,-1,text.delete)
            btnApp=wx.Button(self,-1,text.insert,size=btnDEL.GetSize())
        else:
            btnApp=wx.Button(self,-1,text.insert)
            btnDEL=wx.Button(self,-1,text.delete,size=btnApp.GetSize())
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer,0,wx.LEFT,10)
        mainSizer.Add(rightSizer,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,14)
        sizer.Add(mainSizer,0,wx.TOP,10)
        line = wx.StaticLine(self, -1, size=(20,-1),pos = (200,0), style=wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.Enable(False)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add((1,12))
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
#===============================================================================

        def onClose(evt):
            self.MakeModal(False)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON,onCancel)

        def onOK(evt):
            self.panel.servers = self.servers
            self.panel.cfgs = self.cfgs
            self.panel.passSMTP = self.passSMTP
            self.panel.outServerCtrl.Clear()
            self.panel.outServerCtrl.AppendItems(strings=[n[0] for n in self.servers])
            self.panel.outServerCtrl.SetStringSelection(self.val)
            self.panel.validation()
            self.Close()
        btn1.Bind(wx.EVT_BUTTON,onOK)

        def OnLabelAndPassword(evt):
            if self.servers <> []:
                srvrs = [item[8] for item in self.cfgs]
                oldLbl = listBoxCtrl.GetStringSelection()
                sel = self.oldSel
                label = labelCtrl.GetValue().strip()
                val = passwCtrl.GetValue()
                if val != '':
                    self.passSMTP[label] = val
                self.servers[sel][0]=label
                if listBoxCtrl.GetStrings().count(oldLbl)==1:
                    if oldLbl in srvrs:
                        if self.val == oldLbl:
                            self.val = label
                        for item in self.cfgs:
                            if item[8] == oldLbl:
                                item[8] = label
                listBoxCtrl.Set([n[0] for n in self.servers])
                listBoxCtrl.SetSelection(sel)
                validation()
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnLabelAndPassword)
        passwCtrl.Bind(wx.EVT_TEXT, OnLabelAndPassword)

        def onServerName(event):
            if self.servers<>[]:
                val = outServerCtrl.GetValue().strip()
                sel = self.oldSel
                self.servers[sel][1] = val
                validation()
            event.Skip()
        outServerCtrl.Bind(wx.EVT_TEXT, onServerName)

        def onPort(event):
            if self.servers<>[]:
                val = outPortCtrl.GetValue()
                sel = self.oldSel
                self.servers[sel][2] = val
                validation()
            event.Skip()
        outPortCtrl.Bind(wx.EVT_TEXT, onPort)

        def onSSL(event):
            if self.servers<>[]:
                ports=(25,587,587,465)
                val = choiceSecureCtrl.GetSelection()
                port = ports[val]
                outPortCtrl.SetValue(port)
                sel = self.oldSel
                self.servers[sel][2] = port
                self.servers[sel][3] = val
                validation()
            event.Skip()
        choiceSecureCtrl.Bind(wx.EVT_CHOICE, onSSL)

        def onCheckbox(event=None):
            val = useSecureCtrl.GetValue()
            sel = self.oldSel
            self.servers[sel][4] = val
            userCtrl.Enable(val)
            userLbl.Enable(val)
            passwCtrl.Enable(val)
            passwLbl.Enable(val)
            if not val:
                userCtrl.SetValue('')
                passwCtrl.SetValue('')
            validation()
            if event:
                event.Skip()
        useSecureCtrl.Bind(wx.EVT_CHECKBOX,onCheckbox)

        def onUser(event):
            if self.servers<>[]:
                val = userCtrl.GetValue().strip()
                sel = self.oldSel
                self.servers[sel][5] = val
                validation()
            event.Skip()
        userCtrl.Bind(wx.EVT_TEXT, onUser)

        def onClick(evt):
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            if label.strip() <> "":
                if [n[0] for n in self.servers].count(label) == 1:
                    self.oldSel=sel
                    item = self.servers[sel]
                    setValue(item)
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            val = self.servers[sel][4]
            userCtrl.Enable(val)
            userLbl.Enable(val)
            passwCtrl.Enable(val)
            passwLbl.Enable(val)
            validation()
            evt.Skip()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)

        def onButtonUp(evt):
            newSel,self.servers=Move(self.servers,listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set([n[0] for n in self.servers])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)

        def onButtonDown(evt):
            newSel,self.servers=Move(self.servers,listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set([n[0] for n in self.servers])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)

        def onButtonDelete(evt):
            srvrs = [item[8] for item in self.cfgs]
            val = listBoxCtrl.GetStringSelection()
            if val in srvrs:
                answer = wx.MessageBox(
                    text.deleteServer % val,
                    eg.APP_NAME,
                    wx.NO_DEFAULT|wx.OK|wx.ICON_EXCLAMATION
                )
                return
            sel = listBoxCtrl.GetSelection()
            lngth = len(self.servers)
            if lngth == 2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            if lngth == 1:
                self.servers=[]
                listBoxCtrl.Set([])
                item = ['','',25,0,False,'']
                setValue(item)
                boxEnable(False)
                btn1.Enable(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                userCtrl.Enable(False)
                userLbl.Enable(False)
                passwCtrl.Enable(False)
                passwLbl.Enable(False)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            tmp = self.servers.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set([n[0] for n in self.servers])
            listBoxCtrl.SetSelection(sel)
            item = self.servers[sel]
            setValue(item)
            onCheckbox()
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)

        def OnButtonAppend(evt):
            if len(self.servers)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            boxEnable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            item = ['','',25,0,False,'']
            self.servers.insert(sel,item)
            listBoxCtrl.Set([n[0] for n in self.servers])
            listBoxCtrl.SetSelection(sel)
            setValue(item)
            labelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            onCheckbox()
            evt.Skip()

        if len(self.servers) > 0:
            listBoxCtrl.Set([n[0] for n in self.servers])
            listBoxCtrl.SetSelection(0)
            setValue(self.servers[0])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
            onCheckbox()
        else:
            boxEnable(False)
            btn1.Enable(False)
            btnApp.Enable(True)
            userCtrl.Enable(False)
            userLbl.Enable(False)
            passwCtrl.Enable(False)
            passwLbl.Enable(False)

        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)
        sizer.Layout()
        self.MakeModal(True)
        self.SetFocus()
        self.Show()
#===============================================================================

class outTextsDialog(wx.MiniFrame):
    oldSel = 0
    def __init__(self, parent, plugin):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION,
            name="Texts dialog"
        )
        self.SetBackgroundColour(wx.NullColour)
        self.panel = parent
        self.plugin = plugin
        self.texts = cpy(self.panel.txts)
#===============================================================================

    def ShowOutTxtsDlg(self):
        text = self.plugin.text
        self.SetTitle(text.textsTitle)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.SetMinSize((450, 300))
        leftSizer = wx.FlexGridSizer(4,2,2,8)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        previewLbl=wx.StaticText(self, -1, text.textsList)
        listBoxCtrl=wx.ListBox(
            self,-1,
            size=wx.Size(120,106),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        labelLbl=wx.StaticText(self, -1, text.txtLabel)
        labelCtrl=wx.TextCtrl(self,-1,'')
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        outTextLbl=wx.StaticText(self, -1, text.outText)
        outTextCtrl=wx.TextCtrl(
            self,-1,'',size=(210, 232),
            style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER
        )
        rightSizer.Add(outTextLbl,0,wx.EXPAND)
        rightSizer.Add(outTextCtrl,0,wx.EXPAND)
        leftSizer.Add(previewLbl,0,wx.TOP,5)
        leftSizer.Add((1,1))
        leftSizer.Add(listBoxCtrl,0,wx.TOP,5)
        leftSizer.Add(topMiddleSizer,0,wx.TOP,5)
        leftSizer.Add(labelLbl,0,wx.TOP,3)
        leftSizer.Add((1,1))
        leftSizer.Add(labelCtrl,0,wx.EXPAND)
        leftSizer.Add((1,1))
        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(self, -1, bmp)
        btnUP.Enable(False)
        topMiddleSizer.Add(btnUP)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(self, -1, bmp)
        btnDOWN.Enable(False)
        topMiddleSizer.Add(btnDOWN,0,wx.TOP,3)
        #Buttons 'Delete' and 'Insert new'
        w1 = self.GetTextExtent(text.delete)[0]
        w2 = self.GetTextExtent(text.insert)[0]
        if w1 > w2:
            btnDEL=wx.Button(self,-1,text.delete)
            btnApp=wx.Button(self,-1,text.insert,size=btnDEL.GetSize())
        else:
            btnApp=wx.Button(self,-1,text.insert)
            btnDEL=wx.Button(self,-1,text.delete,size=btnApp.GetSize())
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer,0,wx.LEFT,10)
        mainSizer.Add(rightSizer,0,wx.EXPAND|wx.LEFT|wx.RIGHT,14)
        sizer.Add(mainSizer,0,wx.TOP,10)
        line = wx.StaticLine(self, -1, size=(20,-1),pos = (200,0), style=wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.Enable(False)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add((1,5))
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)

        def boxEnable(enable):
            labelCtrl.Enable(enable)
            outTextCtrl.Enable(enable)
            labelLbl.Enable(enable)
            outTextLbl.Enable(enable)

        def setValue(item):
            labelCtrl.ChangeValue (item[0])
            outTextCtrl.ChangeValue(item[1])

        if len(self.texts) > 0:
            listBoxCtrl.Set([n[0] for n in self.texts])
            listBoxCtrl.SetSelection(0)
            setValue(self.texts[0])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            boxEnable(False)
            btn1.Enable(False)

        sizer.Layout()
        self.MakeModal(True)
        self.SetFocus()
        self.Show()
#===============================================================================

        def onClose(evt):
            self.MakeModal(False)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON,onCancel)

        def onOK(evt):
            self.panel.txts = self.texts
            self.Close()
        btn1.Bind(wx.EVT_BUTTON,onOK)

        def validation():
            flag = True
            label = labelCtrl.GetValue()
            if label == "":
                flag = False
            else:
                if [n[0] for n in self.texts].count(label)!=1:
                    flag = False
            if outTextCtrl.GetValue().strip() == '':
                flag = False
            btn1.Enable(flag)
            btnApp.Enable(flag)

        def OnTxtChange(evt):
            if self.texts<>[]:
                sel = self.oldSel
                label = labelCtrl.GetValue().strip()
                self.texts[sel][0]=label
                listBoxCtrl.Set([n[0] for n in self.texts])
                listBoxCtrl.SetSelection(sel)
                validation()
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTxtChange)

        def ontextName(event):
            if self.texts<>[]:
                val = outTextCtrl.GetValue().strip()
                sel = self.oldSel
                self.texts[sel][1] = val
                validation()
            event.Skip()
        outTextCtrl.Bind(wx.EVT_TEXT, ontextName)

        def onClick(evt):
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            if label.strip()<>"":
                if [n[0] for n in self.texts].count(label)==1:
                    self.oldSel=sel
                    item = self.texts[sel]
                    setValue(item)
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)

        def onButtonUp(evt):
            newSel,self.texts=Move(self.texts,listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set([n[0] for n in self.texts])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)

        def onButtonDown(evt):
            newSel,self.texts=Move(self.texts,listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set([n[0] for n in self.texts])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)

        def onButtonDelete(evt):
            lngth=len(self.texts)
            if lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.texts=[]
                listBoxCtrl.Set([])
                item = ['','']
                setValue(item)
                boxEnable(False)
                btn1.Enable(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            tmp = self.texts.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set([n[0] for n in self.texts])
            listBoxCtrl.SetSelection(sel)
            item = self.texts[sel]
            setValue(item)
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)

        def OnButtonAppend(evt):
            if len(self.texts)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            boxEnable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            item = ['','']
            self.texts.insert(sel,item)
            listBoxCtrl.Set([n[0] for n in self.texts])
            listBoxCtrl.SetSelection(sel)
            setValue(item)
            labelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)
#===============================================================================

class groupsDialog(wx.MiniFrame):
    oldSel = 0
    oldSel2 = 0
    def __init__(self, parent, plugin):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            style=wx.CAPTION,
            name="Groups dialog"
        )
        self.SetBackgroundColour(wx.NullColour)
        self.panel = parent
        self.plugin = plugin
        self.groups = cpy(self.panel.grps)
#===============================================================================

    def ShowGroupsDlg(self):
        text = self.plugin.text
        self.SetTitle(text.groupsTitle)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.SetMinSize((450, 307))
        leftSizer = wx.FlexGridSizer(4,2,2,8)
        rightSizer = wx.FlexGridSizer(4,2,2,8)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        topMiddleSizer2=wx.BoxSizer(wx.VERTICAL)
        previewLbl=wx.StaticText(self, -1, text.groupsList)
        listBoxCtrl=wx.ListBox(
            self,-1,
            size=wx.Size(100,146),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        labelLbl=wx.StaticText(self, -1, text.groupLabel)
        labelCtrl=wx.TextCtrl(self,-1,'')
        leftSizer.Add(previewLbl,0,wx.TOP,5)
        leftSizer.Add((1,1))
        leftSizer.Add(listBoxCtrl,0,wx.TOP,1)
        leftSizer.Add(topMiddleSizer,0,wx.TOP,1)
        leftSizer.Add(labelLbl,0,wx.TOP,3)
        leftSizer.Add((1,1))
        leftSizer.Add(labelCtrl,0,wx.EXPAND)
        leftSizer.Add((1,1))

        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(self, -1, bmp)
        btnUP.Enable(False)
        topMiddleSizer.Add(btnUP)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(self, -1, bmp)
        btnDOWN.Enable(False)
        topMiddleSizer.Add(btnDOWN,0,wx.TOP,3)
        #Buttons 'Delete' and 'Insert new'
        w1 = self.GetTextExtent(text.delete)[0]
        w2 = self.GetTextExtent(text.insert)[0]
        w = max(w1,w2)+24
        btnApp=wx.Button(self,-1,text.insert,size = (w,-1))
        btnDEL=wx.Button(self,-1,text.delete,size = (w,-1))
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        addressesLbl=wx.StaticText(self, -1, text.outAddress)
        listBoxCtrl2=wx.ListBox(
            self,-1,
            size=wx.Size(140,146),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        labelLbl2=wx.StaticText(self, -1, text.addressLabel)
        labelCtrl2=wx.TextCtrl(self,-1,'')
        rightSizer.Add(addressesLbl,0,wx.TOP,5)
        rightSizer.Add((1,1))
        rightSizer.Add(listBoxCtrl2,0,wx.TOP,1)
        rightSizer.Add(topMiddleSizer2,0,wx.TOP,1)
        rightSizer.Add(labelLbl2,0,wx.TOP,3)
        rightSizer.Add((1,1))
        rightSizer.Add(labelCtrl2,0,wx.EXPAND)
        rightSizer.Add((1,1))

        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP2 = wx.BitmapButton(self, -1, bmp)
        btnUP2.Enable(False)
        topMiddleSizer2.Add(btnUP2)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN2 = wx.BitmapButton(self, -1, bmp)
        btnDOWN2.Enable(False)
        topMiddleSizer2.Add(btnDOWN2,0,wx.TOP,3)
        #Buttons 'Delete' and 'Insert new'
        btnApp2=wx.Button(self,-1,text.insert,size = (w,-1))
        btnDEL2=wx.Button(self,-1,text.delete,size = (w,-1))
        btnDEL2.Enable(False)
        topMiddleSizer2.Add(btnDEL2,0,wx.TOP,5)
        topMiddleSizer2.Add(btnApp2,0,wx.TOP,5)
        mainSizer = wx.GridBagSizer(0, 0)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(leftSizer,(0,0),flag = wx.ALIGN_LEFT)
        mainSizer.Add(rightSizer,(0,2),flag = wx.ALIGN_RIGHT)
        sizer.Add(mainSizer,0,wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND,20)
        line = wx.StaticLine(self, -1, size=(20,-1),pos = (200,0), style=wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn1.Enable(False)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add((1,36))
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)

        def boxDisable():
            addressesLbl.Enable(False)
            listBoxCtrl2.Enable(False)
            labelLbl2.Enable(False)
            labelCtrl2.Enable(False)
            btnUP2.Enable(False)
            btnDOWN2.Enable(False)
            btnApp2.Enable(False)
            btnDEL2.Enable(False)

        def setValue(item):
            labelCtrl.ChangeValue (item[0])
            listBoxCtrl2.Set(item[1])
            if len(item[1]) == 0:
                btnDEL2.Enable(False)
                btnUP2.Enable(False)
                btnDOWN2.Enable(False)
            else:
                listBoxCtrl2.SetSelection(0)
                labelCtrl2.ChangeValue(item[1][0])
                btnDEL2.Enable(True)
                flag = len(item[1]) > 1
                btnUP2.Enable(flag)
                btnDOWN2.Enable(flag)

        if len(self.groups) > 0:
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(0)
            setValue(self.groups[0])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            labelLbl.Enable(False)
            labelCtrl.Enable(False)
            btn1.Enable(False)
            boxDisable()

        sizer.Layout()
        self.MakeModal(True)
        self.SetFocus()
        self.Show()
#===============================================================================

        def onClose(evt):
            self.MakeModal(False)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON,onCancel)

        def onOK(evt):
            self.panel.grps = self.groups
            self.Close()
        btn1.Bind(wx.EVT_BUTTON,onOK)

        def validation():
            while True:
                flag = True
                flag2 = True
                label = labelCtrl.GetValue()
                if label == '':
                    flag2 = False
                if len(self.groups) > 0:
                    strings = listBoxCtrl.GetStrings()
                    for lbl in strings:
                        if lbl == '':
                            flag = False
                            break
                if strings.count(label) != 1:
                    flag = False
                    break
                sel = self.oldSel
                address = labelCtrl2.GetValue()
                if len(self.groups[sel][1]) > 0:
                    if address == '':
                        flag2 = False
                        break
                    strings = listBoxCtrl2.GetStrings()
                    for addrss in strings:
                        if not validateEmailAddr(addrss):
                            flag2 = False
                            break
                    if strings.count(address) != 1:
                        flag2 = False
                        break
                else:
                    flag = False
                break
            btnApp2.Enable(flag2)
            btn1.Enable(flag and flag2)
            btnApp.Enable(flag and flag2)

        def OnTxtChange(evt):
            if self.groups<>[]:
                sel = self.oldSel
                label = labelCtrl.GetValue().strip()
                self.groups[sel][0]=label
                listBoxCtrl.Set([n[0] for n in self.groups])
                listBoxCtrl.SetSelection(sel)
                validation()
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnTxtChange)

        def onClick(evt):
            sel = listBoxCtrl.GetSelection()
            if self.oldSel != sel:
                flag = True
                for address in self.groups[self.oldSel][1]:
                    if not validateEmailAddr(address):
                        flag = False
                        break
                label = labelCtrl.GetValue()
                if label.strip()<>"":
                    if [n[0] for n in self.groups].count(label)>1:
                        flag = False
                if flag:
                    self.oldSel=sel
                    item = self.groups[sel]
                    setValue(item)
                listBoxCtrl.SetSelection(self.oldSel)
                listBoxCtrl.SetFocus()
            #evt.Skip()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onClick)

        def onButtonUp(evt):
            newSel,self.groups=Move(self.groups,listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)

        def onButtonDown(evt):
            newSel,self.groups=Move(self.groups,listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)

        def onButtonDelete(evt):
            lngth=len(self.groups)
            if lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                self.groups=[]
                listBoxCtrl.Set([])
                item = ['', []]
                setValue(item)
                labelCtrl2.ChangeValue('')
                labelLbl.Enable(False)
                labelCtrl.Enable(False)
                boxDisable()
                btnApp2.Enable(False)
                btn1.Enable(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            tmp = self.groups.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(sel)
            item = self.groups[sel]
            setValue(item)
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)

        def OnButtonAppend(evt):
            if len(self.groups)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            labelLbl.Enable(True)
            labelCtrl.Enable(True)
            boxDisable()
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            item = ['', []]
            self.groups.insert(sel,item)
            listBoxCtrl.Set([n[0] for n in self.groups])
            listBoxCtrl.SetSelection(sel)
            labelCtrl2.ChangeValue('')
            setValue(item)
            labelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)

        def OnLabelChange(evt):
            sel = self.oldSel
            if self.groups[sel][1]<>[]:
                sel2 = self.oldSel2
                label = labelCtrl2.GetValue().strip()
                self.groups[sel][1][sel2]=label
                listBoxCtrl2.Set(self.groups[sel][1])
                listBoxCtrl2.SetSelection(sel2)
                validation()
            evt.Skip()
        labelCtrl2.Bind(wx.EVT_TEXT, OnLabelChange)

        def onClick2(evt):
            sel2 = listBoxCtrl2.GetSelection()
            if self.oldSel2 != sel2:
                item = listBoxCtrl2.GetStrings()[self.oldSel2]
                if validateEmailAddr(item):
                    label = listBoxCtrl2.GetStringSelection()
                    labelCtrl2.ChangeValue(label)
                    self.oldSel2=sel2
                listBoxCtrl2.SetSelection(self.oldSel2)
                listBoxCtrl2.SetFocus()
                evt.Skip()
        listBoxCtrl2.Bind(wx.EVT_LISTBOX, onClick2)

        def onButtonUp2(evt):
            sel = self.oldSel
            newSel,self.groups[sel][1]=Move(self.groups[sel][1],listBoxCtrl2.GetSelection(),-1)
            listBoxCtrl2.Set(self.groups[sel][1])
            listBoxCtrl2.SetSelection(newSel)
            self.oldSel2 = newSel
            evt.Skip()
        btnUP2.Bind(wx.EVT_BUTTON, onButtonUp2)

        def onButtonDown2(evt):
            sel = self.oldSel
            newSel,self.groups[sel][1]=Move(self.groups[sel][1],listBoxCtrl2.GetSelection(),1)
            listBoxCtrl2.Set(self.groups[sel][1])
            listBoxCtrl2.SetSelection(newSel)
            self.oldSel2 = newSel
            evt.Skip()
        btnDOWN2.Bind(wx.EVT_BUTTON, onButtonDown2)

        def onButtonDelete2(evt):
            sel = self.oldSel
            sel2 = listBoxCtrl2.GetSelection()
            lngth=len(self.groups[sel][1])
            if lngth==2:
                btnUP2.Enable(False)
                btnDOWN2.Enable(False)
            if lngth == 1:
                labelCtrl2.ChangeValue('')
                self.groups[sel][1] = []
                listBoxCtrl2.Set([])
                listBoxCtrl2.SetStringSelection('')
                btn1.Enable(False)
                btnDEL2.Enable(False)
                btnApp2.Enable(True)
                evt.Skip()
                return
            elif sel2 == lngth - 1:
                sel2 = 0
            self.oldSel2 = sel2
            tmp = self.groups[sel][1].pop(listBoxCtrl2.GetSelection())
            listBoxCtrl2.Set(self.groups[sel][1])
            listBoxCtrl2.SetSelection(sel2)
            item = self.groups[sel][1][sel2]
            labelCtrl2.ChangeValue(item)
            validation()
            evt.Skip()
        btnDEL2.Bind(wx.EVT_BUTTON, onButtonDelete2)

        def OnButtonAppend2(evt):
            if len(self.groups[self.oldSel][1]) == 1:
                btnUP2.Enable(True)
                btnDOWN2.Enable(True)
            labelLbl2.Enable(True)
            labelCtrl2.Enable(True)
            addressesLbl.Enable(True)
            listBoxCtrl2.Enable(True)
            sel = listBoxCtrl2.GetSelection() + 1
            self.oldSel2=sel
            self.groups[self.oldSel][1].insert(sel,'')
            listBoxCtrl2.Set(self.groups[self.oldSel][1])
            listBoxCtrl2.SetSelection(sel)
            labelCtrl2.SetValue('')
            labelCtrl2.SetFocus()
            btnApp2.Enable(False)
            btnDEL2.Enable(True)
            evt.Skip()
        btnApp2.Bind(wx.EVT_BUTTON, OnButtonAppend2)
#===============================================================================

class observViewerDialog(wx.MiniFrame):
    def __init__(self, parent, plugin, observThreads):
        wx.MiniFrame.__init__(
        self, parent, -1,
        style=wx.CAPTION|wx.RESIZE_BORDER, name="Observations viewer/manager"
    )
        self.SetBackgroundColour(wx.NullColour)
        self.observThreads = observThreads
        self.plugin = plugin

    def ShowObservViewerDialog(self):
        text = self.plugin.text
        self.SetTitle(text.viewerTitle)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(
            wx.StaticText(self, -1, text.listhead),
            0,wx.TOP|wx.LEFT|wx.RIGHT,10
        )

        centralSizer = wx.GridBagSizer(10, 10)
        centralSizer.AddGrowableRow(0)
        centralSizer.AddGrowableCol(3)
        observListCtrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)
        for i, colLabel in enumerate(text.colLabels):
            observListCtrl.InsertColumn(
                i,
                colLabel,
                wx.LIST_FORMAT_RIGHT if (i==1 or i==2) else wx.LIST_FORMAT_LEFT
            )
        observListCtrl.InsertStringItem(0, text.colLabels[0])
        observListCtrl.SetStringItem(0, 2, time.strftime("%c"))
        size = 0
        for i in range(5):
            observListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            size += observListCtrl.GetColumnWidth(i)
        observListCtrl.SetMinSize((size, -1))
        centralSizer.Add(observListCtrl, (0,0),(1,5), flag = wx.EXPAND)
        #buttons
        abortButton = wx.Button(self, -1, text.buttons[0])
        abortAllButton = wx.Button(self, -1, text.buttons[1])
        refreshButton = wx.Button(self, -1, text.buttons[2])
        closeButton = wx.Button(self, -1, text.buttons[3])
        centralSizer.Add(abortButton,(1,0), flag = wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM, border = 10)
        centralSizer.Add(abortAllButton,(1,1), flag = wx.ALIGN_CENTER_HORIZONTAL)
        centralSizer.Add(refreshButton,(1,2), flag = wx.ALIGN_LEFT)
        centralSizer.Add(closeButton,(1,4), flag = wx.ALIGN_RIGHT)

        def FillListCtrl (event=None):
            observListCtrl.DeleteAllItems()
            row = 0
            for i, item in enumerate(self.observThreads):
                ot = self.observThreads[item]
                if ot.isAlive() and not ot.isAborted():
                    observListCtrl.InsertStringItem(row, ot.observName)
                    observListCtrl.SetStringItem(row, 1, str(ot.setup[1]))
                    timestamp = time.strftime("%c",  time.localtime(ot.lastCheck)) if ot.lastCheck!=0 else ''
                    observListCtrl.SetStringItem(row, 2, timestamp)
                    observListCtrl.SetStringItem(row, 3, ot.setup[3])
                    observListCtrl.SetStringItem(row, 4, ot.setup[12])
                    row += 1
            ListSelection()

        def OnAbortButton(event):
            item = observListCtrl.GetFirstSelected()
            while item != -1:
                name = observListCtrl.GetItemText(item)
                ot = self.observThreads[name]
                if ot.isAlive():
                    ot.AbortObservation()
                    time.sleep(0.25)
                item = observListCtrl.GetNextSelected(item)
            FillListCtrl()
            event.Skip()

        def OnAbortAllButton(event):
            thrds = list(enumerate(self.observThreads))
            thrds.reverse()
            for i, name in thrds:
                ot = self.observThreads[name]
                ot.AbortObservation()
                time.sleep(0.25)
                FillListCtrl()
                self.Update()
            event.Skip()

        def OnCloseButton(event):
            self.Destroy()
            event.Skip()

        def ListSelection(event=None):
            flag = observListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            if event:
                event.Skip()

        def OnSize(event):
            observListCtrl.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER)
            event.Skip()

        FillListCtrl()
        self.SetMinSize((size+52,178))
        self.SetSize((size+52,178))
        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, FillListCtrl)
        closeButton.Bind(wx.EVT_BUTTON, OnCloseButton)
        observListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        observListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        self.Bind(wx.EVT_SIZE, OnSize)
        mainSizer.Add(centralSizer, 1,wx.EXPAND|wx.LEFT|wx.RIGHT,10)
        self.SetSizer(mainSizer)
        mainSizer.Layout()
        self.Show()
#===============================================================================

class SendMailThread(Thread):
    def __init__(
        self,
        plugin,
        sbjct,
        From,
        To,
        Copy,
        Txt,
        Append,
        toName,
        references,
        messageID
    ):
        Thread.__init__(self, name="SendMailThread" )
        self.plugin=plugin
        self.passSMTP = self.plugin.passSMTP
        self.sbjct = sbjct
        self.From = From
        self.To = To
        self.Copy = Copy
        self.Txt = Txt
        self.Append = Append
        self.toName = toName
        self.references = references
        self.messageID = messageID

    def run(self):
        sbjct = self.sbjct
        sbjct = eg.ParseString(sbjct)
        From = self.From
        To = self.To
        To = eg.ParseString(To)
        Copy = self.Copy
        Txt = self.Txt
        Txt = eg.ParseString(Txt)
        text = self.plugin.text
        Append = self.Append
        Append = eg.ParseString(Append)
        toName = self.toName
        toName = eg.ParseString(toName)
        choices = [item[0] for item in self.plugin.texts]
        if Append in choices:
            indx = choices.index(Append)
            Append = self.plugin.texts[indx][1]
        else:
            Append = None
        From = From.split(' - ')[-1]
        indx = [item[0] for item in self.plugin.configs].index(From)
        account = self.plugin.configs[indx]
        try:
            indx = [item[0] for item in self.plugin.servers].index(account[8])
        except:
            eg.PrintError(text.error5 % (account[8], self.plugin.servers[0][0]))
            indx = 0
        server = self.plugin.servers[indx]
        choices = [item[0] for item in self.plugin.groups]
        if Copy in choices:
            indx = choices.index(Copy)
            Copy = self.plugin.groups[indx][1]
        else:
            Copy = None
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        header_charset = 'UTF-8'
        body = Txt
        if Append is not None:
            body += '\n----====###====----\n'+Append
        for body_charset in 'US-ASCII', 'UTF-8':
            try:
                body.encode(body_charset)
            except UnicodeError:
                pass
            else:
                break
        sender_name = str(Header(unicode(account[2]), header_charset))
        recipient_name = str(Header(unicode(toName), header_charset))
        msg = MIMEText(body.encode(body_charset), 'plain', body_charset)
        msg['From'] = formataddr((sender_name, account[3]))
        msg['To'] = formataddr((recipient_name, To))
        if Copy is not None:
            msg['Cc'] = ','.join(Copy)
        msg['Subject'] = Header(unicode(sbjct), header_charset)
        msg["User-agent"]= "EventGhost %s" % eg.Version.string
        if account[4] != '':
            msg["Reply-to"]= formataddr((sender_name,account[4]))
        #msg["Date"] = formatdate() #return: Wed, 03 Dec 2008 12:17:35 -0000
        msg["Date"] = formatdate(None, True) #return: Wed, 03 Dec 2008 13:17:35 +0100
        if self.messageID is not None:
            msg['In-Reply-To'] = self.messageID
            if self.references is None:
                msg['References'] = self.messageID+u'\r\n'
            else:
                msg['References'] = self.references+self.messageID+u'\r\n'
        case = server[3] #secure connection ?
        try:
            if case < 3:
                smtp = smtplib.SMTP(server[1],server[2])
            else:
                smtp = smtplib.SMTP_SSL(server[1],server[2])
        except:
            eg.PrintError(text.error6+' '+text.error7 % (server[1],server[2]))
        else:
            try:
                if server[4]: #secure authentication
                    #smtp.debuglevel = 5
                    capa = smtp.ehlo()
                    if case == 1 and not 'STARTTLS' in capa[-1].upper():
                        case = 0
                    if case == 0 or case == 3:
                        smtp.esmtp_features["auth"] = "LOGIN PLAIN"
                    else:
                        smtp.starttls()
                        smtp.ehlo()
                    password = self.passSMTP.data[server[0]]
                    smtp.login(server[5], password)
                if Copy is None:
                    smtp.sendmail(account[3], To, msg.as_string())
                else:
                    rcpnt = [To]
                    rcpnt.extend(Copy)
                    smtp.sendmail(account[3], rcpnt, msg.as_string())
            except:
                eg.PrintError(text.error6+' '+text.error8)
            else:
                From = formataddr((account[2], account[3]))
                eg.TriggerEvent('Sent', payload = '%s: %s' % (From, sbjct), prefix = 'E-mail')
            smtp.quit()
#===============================================================================

class deleteEmail(Thread):
    def __init__(
        self,
        indx,
        sel,
        mode,
        parent
    ):
        self.indx = indx
        self.sel = sel
        self.mode = mode
        self.parent = parent
        Thread.__init__(self, name = 'DeleteEmail')

    def run(self):
        self.parent.RealizeAction(self.indx, self.sel, self.mode)
#===============================================================================

class WorkThread(Thread):
    def __init__(
        self,
        plugin,
        setup,
        notifFrame,
    ):
        self.setup = setup
        Thread.__init__(self, name = self.setup[0].encode('unicode_escape')+'_W-Thread')
        self.plugin = plugin
        self.passINC = self.plugin.passINC
        self.configs = self.plugin.configs
        self.notifFrame = notifFrame
        self.runFlag = False
        self.abort = False
        self.refresh=False
        self.threadFlag = Event()
        self.delArgs = None
        self.text = self.plugin.text
        print self.text.observStarts % self.setup[0]

    def isRunning(self):
        return self.runFlag

    def DeleteAction(self, args):
        self.delArgs = args
        if not self.runFlag:
            self.threadFlag.set()

    def operate(self, refresh = False):
        self.refresh = refresh or self.refresh
        if not self.runFlag:
            self.threadFlag.set()

    def AbortObservation(self, close = False):
        self.abort = True
        self.close = close
        self.threadFlag.set()

    def run(self):
        while 1:
            if self.abort:
                break
            self.runFlag = True
            if self.delArgs is not None:
                self.delArgs[3].RealizeAction(self.delArgs[0], self.delArgs[1], self.delArgs[2])
                if self.delArgs[3].isCloseReq():
                    self.delArgs[3].Close()
                else:
                    self.delArgs[3].resDelFlag()
                self.delArgs = None
                val, shift = self.CheckEmails()
                if self.setup[6]: #Show notification Window
                    self.notifFrame.SetNum(val)
                    if val>0:
                        if not self.notifFrame.IsShown():
                            self.notifFrame.Show(True)
                    else:
                        self.notifFrame.Disappear()
            else:
                val, shift = self.CheckEmails()
                if self.setup[6]: #Show notification Window
                    if val == 0:
                        self.notifFrame.Disappear()
                    elif shift or self.refresh:
                        self.notifFrame.SetNum(val)
                        if not self.notifFrame.IsShown():
                            self.notifFrame.Show(True)
                if self.refresh:
                    self.refresh = False
                else:
                    if self.setup[7]: #Trigger event
                        if val > 0 and shift:
                            if self.setup[8]:
                                eg.TriggerEvent(self.setup[3], payload = str(val), prefix = 'E-mail')
                            else:
                                eg.TriggerEvent(self.setup[3], prefix = 'E-mail')
            self.runFlag = False
            if self.abort:
                break
            if self.delArgs is None:
                self.threadFlag.clear()
                self.threadFlag.wait()
        self.notifFrame.Disappear(self.close)
        self.observName = self.setup[0]
        indx = [item[0] for item in self.plugin.tempData].index(self.observName)
        self.plugin.tempData[indx][1:]=[0,[],None,self.notifFrame]

    def CreateOneRecord(self, data, account, nbr, id):
        msg=myParser.parsestr(data)
        if msg.has_key('Message-Id'):
            messId =  msg['Message-Id']
        else:
            messId = ParseAddress(msg['From'])
        tmpRec=[messId]                           #0
        tmpRec.append(ParseItem(msg['Subject']))  #1
        tmpRec.append(ParseAddress(msg['From']))  #2
        tmpRec.append(account)                    #3
        tmpRec.append(str(nbr))                   #4
        tmpRec.append(id)                         #5
        return tmpRec

    def CheckEmails(self):
        accList=[n[0] for n in self.configs]
        accounts = []
        observName = self.setup[0]
        loop=0
        while 1:
            try:
                loop+=1
                indx = [item[0] for item in self.plugin.tempData].index(observName)
                break
            except:
                pass
        for i in range(len(accList)):
            for item in self.setup[2]:
                if item == accList[i]:
                    accounts.append(i)
        nbr = 0
        if len(self.plugin.tempData[indx][2])>0:
            idList = [item[0] for item in self.plugin.tempData[indx][2]]
        else:
            idList = []
        count = 0
        tmpData =[]
        if self.setup[4] == 0: #non-filter mode
            for i in accounts:
                account =  self.configs[i]
                SERVER = account[5]
                PORT = account[6]
                USER = account[7]
                PASSWORD = self.passINC.data[account[0]]
                USE_SSL = account[9] == 3
                if account[1] == 0: #POP
                    try:
                        if USE_SSL:
                            mailbox = poplib.POP3_SSL(SERVER,PORT)
                        else:
                            mailbox = poplib.POP3(SERVER,PORT)
                    except:
                        eg.PrintError(self.text.error0+' '+self.text.error1 % (SERVER,PORT))
                    else:
                        #mailbox.set_debuglevel(5)
                        try:
                            mailbox.user(USER)
                            mailbox.pass_(PASSWORD)
                            #capa = mailbox._longcmd('CAPA')[1]
                            #if 'STLS' in capa:
                            #    print 'STLS'
                            #    #mailbox._shortcmd('STLS')
                            lst = mailbox.list()[1]
                            cnt = len(lst)
                            if cnt > 0:
                                count += cnt
                                MAXLINES = 0
                            for msg in lst:
                                id = msg.split(' ')[0]
                                resp, data, octets = mailbox.top(id, MAXLINES)
                                if resp != '+OK':
                                    resp, data, octets = mailbox.retr(id)
                                data = "\n".join(data)
                                nbr += 1
                                oneRec =  self.CreateOneRecord(data, account[0], nbr, id)
                                tmpData.append(oneRec)
                        except poplib.error_proto, errmsg:
                            eg.PrintError(self.text.error0+' '+str(errmsg))
                        mailbox.quit()
                else:               #IMAP
                    try:
                        if USE_SSL:
                            mailbox = imaplib.IMAP4_SSL(SERVER, PORT)
                        else:
                            mailbox = imaplib.IMAP4(SERVER, PORT)
                    except:
                        eg.PrintError(self.text.error2+' '+self.text.error3 % (SERVER,PORT))
                    else:
                        try:
                            mailbox.login(USER, PASSWORD)
                        except:
                            eg.PrintError(self.text.error2+' '+self.text.error4 % (USER, SERVER, PORT))
                        else:
                            typ, data = mailbox.select('INBOX') #Folder selection
                            typ, data = mailbox.search(None, 'UNSEEN')
                            if data[0]:
                                lst = data[0].split()
                                count += len(lst)
                                for num in lst:
                                    typ, data = mailbox.fetch(num, '(RFC822.HEADER)')
                                    mailbox.store(num, "-FLAGS", '(\Seen)') #Reset UNSEEN flag
                                    data = data[0][1]
                                    nbr += 1
                                    oneRec =  self.CreateOneRecord(data, account[0], nbr, num)
                                    tmpData.append(oneRec)
                        mailbox.logout()

#-------------------------
        else: #filter mode
            def processEmail(mailbox, data, idList, account, count, id, tmpData):
                conds = ["%s.find(%s)>-1",
                    "not %s.find(%s)>-1",
                    "%s==%s",
                    "not %s==%s",
                    "%s.startswith(%s)",
                    "%s.endswith(%s)"]
                msg = myParser.parsestr(data)
                parts = GetParts(msg)
                flag = False
                if self.setup[4] == 1: #filter AND mode
                    i = 0
                    while i < 6:
                        what, cond, strng = self.setup[5][i]
                        if what > 0 and not eval(conds[cond] % (('parts[what-1]'), 'strng')):
                            break
                        i += 1
                    if i == 6:
                        flag = True
                else:                  #filter OR mode
                    i = 0
                    while i < 6:
                        what, cond, strng = self.setup[5][i]
                        if what > 0 and eval(conds[cond] % (('parts[what-1]'), 'strng')):
                            flag = True
                            break
                        i += 1
                if flag:
                    if msg.has_key('Message-Id'):
                        messId =  msg['Message-Id']
                    else:
                        messId = parts[1]
                    if self.setup[11]: #trigger event for each email ?
                        if not messId in idList:
                            itms = self.plugin.text.field_1[1:]
                            suff = self.setup[12]
                            if suff in itms:
                                suff = itms.index(suff)
                                suff = u"%s.%s" % (self.setup[12],parts[suff])
                            if self.setup[13] > 0:
                                eg.TriggerEvent(suff, payload = parts[self.setup[13]-1], prefix = 'E-mail')
                            else:
                                eg.TriggerEvent(suff, prefix = 'E-mail')
                        if self.setup[14]: #~ delete
                            if account[1] == 0: #POP
                                resp = mailbox.dele(id)
                                #if resp[:3]=='+OK':
                                #    print "deleted !!!"
                                #    notDeleted = False
                            else:
                                resp = mailbox.store(id, "+FLAGS", '(\Deleted)')
                                #if resp[0] =='OK':
                                #    resp = mailbox.expunge()
                                #    if resp[0] =='OK':
                                #        print "deleted !!!"
                    count += 1
                    #show notification window?
                    if not self.setup[14]:
                        tmpRec = [messId]           #0 ID
                        tmpRec.append(parts[0])     #1 Subject
                        tmpRec.append(parts[1])     #2 From
                        tmpRec.append(account[0])   #3
                        tmpRec.append(str(count))   #4
                        tmpRec.append(id)           #5
                        tmpData.append(tmpRec)
                return (count, tmpData)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            for i in accounts:
                account =  self.configs[i]
                SERVER = account[5]
                PORT = account[6]
                USER = account[7]
                PASSWORD = self.passINC.data[account[0]]
                USE_SSL = account[9] == 3
                if account[1] == 0: #POP
                    try:
                        if USE_SSL:
                            mailbox = poplib.POP3_SSL(SERVER, PORT)
                        else:
                            mailbox = poplib.POP3(SERVER, PORT)
                    except:
                        eg.PrintError(self.text.error0+' '+self.text.error1 % (SERVER,PORT))
                    else:
                        try:
                            mailbox.user(USER)
                            mailbox.pass_(PASSWORD)
                            lst = mailbox.list()[1]
                            cnt = len(lst)
                            if cnt > 0:
                                for msg in lst:
                                    id = msg.split(' ')[0]
                                    resp, data, octets = mailbox.retr(id)
                                    data = "\n".join(data)
                                    count, tmpData = processEmail(mailbox, data,idList, account, count, id, tmpData)
                        except poplib.error_proto, errmsg:
                            eg.PrintError(self.text.error0+' '+str(errmsg))
                        mailbox.quit()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                else:               #IMAP
                    try:
                        if USE_SSL:
                            mailbox = imaplib.IMAP4_SSL(SERVER, PORT)
                        else:
                            mailbox = imaplib.IMAP4(SERVER, PORT)
                    except:
                        eg.PrintError(self.text.error2+' '+self.text.error3 % (SERVER,PORT))
                    else:
                        try:
                            mailbox.login(USER, PASSWORD)
                        except:
                            eg.PrintError(self.text.error2+' '+self.text.error4 % (USER, SERVER, PORT))
                        else:
                            typ, data = mailbox.select('INBOX') #Folder selection
                            typ, data = mailbox.search(None, 'UNSEEN')
                            if data[0]:
                                lst = data[0].split()
                                for id in lst:
                                    typ, data = mailbox.fetch(id, '(RFC822)')
                                    mailbox.store(id, "-FLAGS", '(\Seen)') #Reset UNSEEN flag
                                    data = data[0][1]
                                    count, tmpData = processEmail(mailbox, data,idList, account, count, id, tmpData)
                        resp = mailbox.expunge()
                        mailbox.logout()
        countOld = self.plugin.tempData[indx][1]
        shift = count != countOld
        countOld = count
        self.plugin.tempData[indx][2] = tmpData
        self.plugin.tempData[indx][1] = count
        return count, shift
#===============================================================================

class ObservationThread(Thread):
    def __init__(
        self,
        setup,
        plugin,
        notifFrame,
    ):
        self.setup = setup
        Thread.__init__(self, name=self.setup[0].encode('unicode_escape')+'_O-Thread')
        self.plugin = plugin
        self.notifFrame = notifFrame
        self.observName = setup[0]
        self.abort = False
        self.lastCheck = 0
        self.threadFlag = Event()
        self.firstRun = True

    def isAborted(self):
        return self.abort

    def run(self):
        while 1:
            if self.firstRun:
                self.firstRun = False
                while True:
                    try:
                        if self.plugin.tempData[indx][3] is not None:
                            wt = self.plugin.tempData[indx][3]
                            if wt.isAlive():
                                #print "WAITING"
                                wt.AbortObservation()
                                self.threadFlag.wait(1)
                                self.threadFlag.clear()
                    except:
                        self.plugin.observThreads[self.setup[0]] = self #update dictionary
                        indx = [item[0] for item in self.plugin.tempData].index(self.observName)
                        self.wt = WorkThread(plugin = self.plugin, setup = self.setup, notifFrame = self.notifFrame)
                        self.plugin.tempData[indx][3] = self.wt
                        self.wt.start()
                        break
            else:
                if self.abort:
                    break
                self.lastCheck = time.time()
                self.wt.operate()
                self.threadFlag.wait(60*self.setup[1])
                self.threadFlag.clear()

    def AbortObservation(self, close=False):
        self.wt.AbortObservation(close)
        self.abort = True
        self.threadFlag.set()
#===============================================================================

class AbortAllObservations(eg.ActionClass):
    def __call__(self):
        self.plugin.AbortAllObservations()
#===============================================================================

class AbortObservation(eg.ActionClass):
    def __call__(self, observName=''):
        self.plugin.AbortObservation(observName)

    def Configure(self, observName=''):
        text=self.text
        panel = eg.ConfigPanel(self)
        nameLbl=wx.StaticText(panel, -1, text.nameObs)
        nameCtrl=wx.TextCtrl(panel,-1,observName)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(nameLbl,0)
        mainSizer.Add(nameCtrl,0,wx.EXPAND)
        panel.sizer.Add(mainSizer)
        panel.sizer.Layout()

        # re-assign the test button
        def OnTestButton(event):
            self.plugin.AbortObservation(nameCtrl.GetValue())
        panel.dialog.buttonRow.testButton.SetLabel(text.abortNow)
        panel.dialog.buttonRow.testButton.SetToolTipString(text.tip)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnTestButton)

        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
            )

    class text:
        nameObs = 'Observation name:'
        abortNow = 'Abort now !'
        tip = 'Abort observation now'
#===============================================================================

class StartObservation(eg.ActionClass):

    def startObserv(self, stp):
        observName = stp[0]
        data = [item[0] for item in self.plugin.tempData]
        if observName in data:
            indx = data.index(observName)
            self.notifFrame = self.plugin.tempData[indx][4]
        else:
            self.notifFrame = NotifFrame(None)
        self.event = CreateEvent(None, 0, 0, None)
        wx.CallAfter(self.notifFrame.ShowNotifFrame,
            plugin = self.plugin,
            stp = stp,
            event = self.event
        )
        eg.actionThread.WaitOnEvent(self.event)
        self.plugin.StartObservation(stp, self.notifFrame)

    def __call__(self, stp):
        #stp
        accounts=[]
        accList = [item[0] for item in self.plugin.configs]
        for i in range(len(accList)):
            for item in stp[2]:
                if item == accList[i]:
                    accounts.append(i)
        if len(accounts) > 0:
            self.startObserv(stp)
        else:
            eg.PrintError(self.text.warning % stp[2])

    def GetLabel(self, stp):
        res1 = stp[0]
        return res1

    def Configure(self, stp = []):

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.flag2=True
        def validation():
            if self.flag2:
                return
            while 1:
                flag = False
                if nameCtrl.GetValue()  == "":
                    break
                lng = len(accountCtrl.GetStrings())
                if lng == 0:
                    break
                indx = 0
                while indx < lng:
                    if accountCtrl.IsChecked(indx):
                        break
                    indx += 1
                if indx == lng: # No one checkbox is checked ?
                    break

                if not eventCtrl.GetValue() and not event2Ctrl.GetValue() and not messageCtrl.GetValue():
                    break

                if eventCtrl.GetValue():
                    if evtNameCtrl.GetValue() == '':
                        break

                if event2Ctrl.GetValue():
                    if evtName2Ctrl.GetValue() == '':
                        break

                if not rb0.GetValue():
                    indx = 0
                    sum = 0
                    while indx < 6:
                        wnd0 = wx.FindWindowById(indx+100)
                        if wnd0.GetSelection() > 0:
                            wnd1 = wx.FindWindowById(indx+200)
                            wnd2 = wx.FindWindowById(indx+300)
                            if wnd1.GetSelection() == -1:
                                break
                            if wnd2.GetValue() == '':
                                break
                        else:
                            sum += 1
                        indx += 1
                    if indx < 6 or sum == 6:
                        break
                #All is OK !
                flag = True
                break
            panel.dialog.buttonRow.applyButton.Enable(flag)
            panel.dialog.buttonRow.okButton.Enable(flag)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        def onFilter(evt):
            if self.flag2:
                return
            id = evt.GetId()
            if id < 200:
                ctrl_1=wx.FindWindowById(id)
                indx=ctrl_1.GetSelection()
                flag = indx > 0
                ctrl_2=wx.FindWindowById(id+100)
                ctrl_3=wx.FindWindowById(id+200)
                ctrl_2.Enable(flag)
                ctrl_3.Enable(flag)
                if not flag:
                    ctrl_2.SetSelection(-1)
                    ctrl_3.ChangeValue('')
                choicLen = len(ctrl_2.GetStrings())
                if choicLen == 2 and indx !=3:
                    ctrl_2.Clear()
                    ctrl_2.AppendItems(strings = text.field_2)
                elif choicLen == 6 and indx == 3:
                    ctrl_2.Clear()
                    ctrl_2.AppendItems(strings = text.field_2[:2])
            evt.Skip()
            validation()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if stp == []:
            self.stp = [
                '',2,[],'',0,
                [[-1,-1,''],[-1,-1,''],[-1,-1,''],[-1,-1,''],[-1,-1,''],[-1,-1,'']],
                False, True, 0, (255,255,255), (0,0,0), False,'',0, False
            ]
        else:
            self.stp = cpy(stp)

        text=self.text
        panel = eg.ConfigPanel(self)
        nameLbl=wx.StaticText(panel, -1, text.nameObs)
        nameCtrl=wx.TextCtrl(panel,-1,self.stp[0])
        intervalLbl_1=wx.StaticText(panel, -1, text.interval_1)
        intervalCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            value = self.stp[1],
            min=1,
            max=999,
        )
        intervalLbl_2=wx.StaticText(panel, -1, text.interval_2)
        accountLbl=wx.StaticText(panel, -1, text.accounts)
        choices=[n[0] for n in self.plugin.configs]
        accountCtrl = wx.CheckListBox(
            panel,
            -1,
            choices = choices,
            size=((-1,80)),
        )
        checked = self.stp[2]
        for i in range(len(choices)):
            while 1:
                for x in checked:
                    if x == choices[i]:
                        accountCtrl.Check(i,True)
                        break
                break

        rb0 = panel.RadioButton(self.stp[4]==0,text.radio_buttons[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(self.stp[4]==1,text.radio_buttons[1])
        rb2 = panel.RadioButton(self.stp[4]==2,text.radio_buttons[2])
        messageCtrl = wx.CheckBox(panel, label = text.message)
        messageCtrl.SetValue(self.stp[6])
        messageCtrl.Enable(not self.stp[14])
        messageCtrl.SetToolTipString(text.tip0)
        eventCtrl = wx.CheckBox(panel, label = text.totalEvent)
        eventCtrl.SetToolTipString(text.tip4)
        event2Ctrl = wx.CheckBox(panel, label = text.emailEvent)
        event2Ctrl.SetToolTipString(text.tip3)
        event2Ctrl.SetValue(self.stp[11])
        eventCtrl.SetValue(self.stp[7])
        eventCtrl.Enable(not self.stp[14])
        event2Ctrl.Enable(False)
        evtNameLbl=wx.StaticText(panel, -1, text.evtName)
        evtNameCtrl=wx.TextCtrl(panel,-1,self.stp[3])
        #evtName2Ctrl=wx.TextCtrl(panel,-1,self.stp[12])
        evtName2Ctrl = wx.ComboBox(
            panel,
            -1,
            choices = self.plugin.text.field_1[1:],
            style = wx.CB_DROPDOWN
        )
        evtName2Ctrl.SetValue(self.stp[12])
        payloadLbl=wx.StaticText(panel, -1, text.payload)
        payloadCtrl = wx.Choice(panel, -1, choices =text.totalPayload)
        payload2Ctrl = wx.Choice(panel, -1, choices=self.plugin.text.field_1)
        payloadCtrl.SetSelection(self.stp[8])
        payload2Ctrl.SetSelection(self.stp[13])
        deleteCtrl = wx.CheckBox(panel, label = text.delete)
        deleteCtrl.SetValue(self.stp[14])
        deleteCtrl.SetToolTipString(text.tip1)
        filterSizer = wx.FlexGridSizer(4,3,0,0)
        for n in range(6):
            fieldCtrl_1 = wx.Choice(panel,id=100+n,choices=self.plugin.text.field_1)
            fieldCtrl_1.Bind(wx.EVT_CHOICE,onFilter)
            indx0 = self.stp[5][n][0]
            fieldCtrl_1.SetSelection(indx0)
            if indx0 == -1:
                fieldCtrl_1.Enable(False)
            fieldCtrl_2 = wx.Choice(panel,id=200+n,choices=text.field_2)
            fieldCtrl_2.Bind(wx.EVT_CHOICE,onFilter)
            indx1 = self.stp[5][n][1]
            fieldCtrl_2.SetSelection(indx1)
            fieldCtrl_3 = wx.TextCtrl(panel,300+n,self.stp[5][n][2])
            fieldCtrl_3.Bind(wx.EVT_TEXT,onFilter)
            filterSizer.Add(fieldCtrl_1)
            filterSizer.Add(fieldCtrl_2)
            filterSizer.Add(fieldCtrl_3)
            if indx0 < 1:
                fieldCtrl_2.Enable(False)
                fieldCtrl_3.Enable(False)
        horizSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(rb0,0,wx.TOP,0)
        rightSizer.Add(rb1,0,wx.TOP,2)
        rightSizer.Add(rb2,0,wx.TOP,2)
        rightSizer.Add(filterSizer,0,wx.EXPAND|wx.TOP,7)
        intervalSizer = wx.BoxSizer(wx.HORIZONTAL)
        horizSizer.Add(leftSizer,0,wx.EXPAND,wx.TOP,0)
        horizSizer.Add(rightSizer,0,wx.LEFT|wx.EXPAND,16)
        leftSizer.Add(nameLbl,0,wx.TOP,0)
        leftSizer.Add(nameCtrl,0,wx.EXPAND)
        intervalSizer.Add(intervalLbl_1,0,wx.TOP,4)
        intervalSizer.Add(intervalCtrl,0,wx.LEFT|wx.RIGHT,4)
        intervalSizer.Add(intervalLbl_2,0,wx.TOP,4)
        leftSizer.Add(intervalSizer,0,wx.EXPAND|wx.TOP,15)
        leftSizer.Add(accountLbl,0,wx.TOP,11) #13
        leftSizer.Add(accountCtrl,0,wx.EXPAND)
        panel.sizer.Add(horizSizer)
        bottomSizer = wx.GridBagSizer(2,10)
        bottomSizer.Add(evtNameLbl,(0,1),wx.DefaultSpan)
        bottomSizer.Add(payloadLbl,(0,2),wx.DefaultSpan)
        bottomSizer.Add(event2Ctrl,(1,0),wx.DefaultSpan,wx.TOP,4)
        bottomSizer.Add(evtName2Ctrl,(1,1),wx.DefaultSpan,wx.EXPAND)
        bottomSizer.Add(payload2Ctrl,(1,2),wx.DefaultSpan,wx.EXPAND)
        bottomSizer.Add(deleteCtrl,(1,3),wx.DefaultSpan,wx.TOP|wx.ALIGN_RIGHT,4)
        bottomSizer.Add(eventCtrl,(2,0),wx.DefaultSpan,wx.TOP,10)
        bottomSizer.Add(evtNameCtrl,(2,1),wx.DefaultSpan,wx.TOP|wx.EXPAND,6)
        bottomSizer.Add(payloadCtrl,(2,2),wx.DefaultSpan,wx.TOP|wx.EXPAND,6)
        bottomSizer.Add(messageCtrl,(3,0),wx.DefaultSpan,wx.TOP,16)
        labelBck = wx.StaticText(panel, -1, text.backCol)
        labelFore = wx.StaticText(panel, -1, text.forCol)
        backgroundColourButton = wx.ColourPickerCtrl(panel)
        backgroundColourButton.SetColour(self.stp[9])
        foregroundColourButton = wx.ColourPickerCtrl(panel)
        foregroundColourButton.SetColour(self.stp[10])
        colourSizer = wx.GridBagSizer(3,3)
        colourSizer.AddGrowableCol(2)
        colourSizer.Add(labelBck,(0,0),wx.DefaultSpan,wx.TOP,4)
        colourSizer.Add(backgroundColourButton,(0,1))
        colourSizer.Add(labelFore,(0,3),wx.DefaultSpan,wx.TOP,4)
        colourSizer.Add(foregroundColourButton,(0,4))
        bottomSizer.Add(colourSizer,(3,1),(1,3),wx.TOP|wx.EXPAND,12)
        panel.sizer.Add(bottomSizer,0,wx.EXPAND|wx.TOP,12)
        panel.sizer.Layout()
        self.flag2=False

        def OnBackgroundColourButton(event):
            self.stp[9] = event.GetColour()
        backgroundColourButton.Bind(wx.EVT_COLOURPICKER_CHANGED, OnBackgroundColourButton)

        def OnForegroundColourButton(event):
            self.stp[10] = event.GetColour()
        foregroundColourButton.Bind(wx.EVT_COLOURPICKER_CHANGED, OnForegroundColourButton)

        def EnableEventCtrl():
            flag = deleteCtrl.GetValue()
            eventCtrl.Enable(not flag)
            if flag:
                eventCtrl.SetValue(False)
                evtNameCtrl.Enable(False)
                payloadCtrl.Enable(False)
                evtNameCtrl.ChangeValue('')
                payloadCtrl.SetSelection(0)

        def EnableEvent2Ctrl():
            if rb0.GetValue():
                event2Ctrl.SetValue(False)
                event2Ctrl.Enable(False)
            else:
                event2Ctrl.Enable(True)
            onEvent2Ctrl()
            EnableEventCtrl()

        def onRadioBtns(evt=None):
            if self.flag2:
                return
            if rb0.GetValue():
                mode = 0
                for indx in range(6):
                    ctrl_1=wx.FindWindowById(indx+100)
                    ctrl_2=wx.FindWindowById(indx+200)
                    ctrl_3=wx.FindWindowById(indx+300)
                    ctrl_1.Enable(False)
                    ctrl_2.Enable(False)
                    ctrl_3.Enable(False)
                    ctrl_1.SetSelection(-1)
                    ctrl_2.SetSelection(-1)
                    ctrl_3.ChangeValue('')
            else:
                for indx in range(6):
                    ctrl_1=wx.FindWindowById(indx+100)
                    if not ctrl_1.IsEnabled():
                        ctrl_1.SetSelection(0)
                        ctrl_1.Enable(True)
                if rb1.GetValue():
                    mode = 1
                else:
                    mode = 2
            self.stp[4] = mode
            if evt:
                evt.Skip()
            EnableEvent2Ctrl()
            validation()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBtns)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBtns)
        rb2.Bind(wx.EVT_RADIOBUTTON, onRadioBtns)

        def onEvent2Ctrl(evt = None):
            flag = event2Ctrl.GetValue()
            evtName2Ctrl.Enable(flag)
            payload2Ctrl.Enable(flag)
            deleteCtrl.Enable(flag)
            if not flag:
                payload2Ctrl.SetSelection(0)
                deleteCtrl.SetValue(False)
                #evtName2Ctrl.ChangeValue('')
                evtName2Ctrl.SetValue('')
                self.stp[12] = ''
            self.stp[11] = flag
            if evt:
                evt.Skip()
            validation()
        event2Ctrl.Bind(wx.EVT_CHECKBOX, onEvent2Ctrl)

        def onDeleteCtrl(evt = None):
            flag = deleteCtrl.GetValue()
            messageCtrl.Enable(not flag)
            if flag:
                messageCtrl.SetValue(False)
            onMessageCtrl()
            EnableEventCtrl()
            evt.Skip()
            validation()
        deleteCtrl.Bind(wx.EVT_CHECKBOX, onDeleteCtrl)

        def onEventCtrl(evt = None):
            flag = eventCtrl.GetValue()
            evtNameCtrl.Enable(flag)
            payloadCtrl.Enable(flag)
            if not flag:
                #evtNameCtrl.ChangeValue('')
                evtNameCtrl.SetValue('')
                self.stp[3] = ''
            if evt:
                evt.Skip()
            validation()
        eventCtrl.Bind(wx.EVT_CHECKBOX, onEventCtrl)

        def onNameCtrl(evt):
            self.stp[0] = nameCtrl.GetValue()
            evt.Skip()
            validation()
        nameCtrl.Bind(wx.EVT_TEXT, onNameCtrl)

        def onEvtNameCtrl(evt):
            evt.Skip()
            validation()
        evtNameCtrl.Bind(wx.EVT_TEXT, onEvtNameCtrl)

        def onEvtName2Ctrl(evt):
            evt.Skip()
            validation()
        evtName2Ctrl.Bind(wx.EVT_TEXT, onEvtName2Ctrl)
        evtName2Ctrl.Bind(wx.EVT_COMBOBOX, onEvtName2Ctrl)

        def onMessageCtrl(evt=None):
            self.stp[6] = messageCtrl.GetValue()
            flag = self.stp[6]

            labelBck.Enable(flag)
            labelFore.Enable(flag)
            backgroundColourButton.Enable(flag)
            foregroundColourButton.Enable(flag)
            if evt:
                evt.Skip()
            validation()
        onMessageCtrl()
        messageCtrl.Bind(wx.EVT_CHECKBOX, onMessageCtrl)

        def onCheckListBox(evt):
            index = evt.GetSelection()
            evt.Skip()
            validation()
            accountCtrl.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
        accountCtrl.Bind(wx.EVT_CHECKLISTBOX, onCheckListBox)

        def UpdateConfig():
            choices = accountCtrl.GetStrings()
            tmpList=[]
            for indx in range(len(choices)):
                if accountCtrl.IsChecked(indx):
                    tmpList.append(choices[indx])
            self.stp[2] = tmpList[:]
            tmpList=[]
            for indx in range(6):
                ctrl_0 = wx.FindWindowById(indx+100)
                indx0 = ctrl_0.GetSelection()
                ctrl_1 = wx.FindWindowById(indx+200)
                indx1 = ctrl_1.GetSelection()
                val2=wx.FindWindowById(indx+300).GetValue()
                tmpList.append((indx0, indx1, val2))
            self.stp[5] = tmpList[:]
            self.stp[1] = intervalCtrl.GetValue()
            self.stp[3] = evtNameCtrl.GetValue()
            self.stp[7] = eventCtrl.GetValue()
            self.stp[8] = payloadCtrl.GetSelection()
            self.stp[12] = evtName2Ctrl.GetValue()
            self.stp[13] = payload2Ctrl.GetSelection()
            self.stp[14] = deleteCtrl.GetValue()

        # re-assign the test button
        def OnTestButton(event):
            UpdateConfig()
            self.startObserv(self.stp)
        panel.dialog.buttonRow.testButton.SetLabel(text.startNow)
        panel.dialog.buttonRow.testButton.SetToolTipString(text.tip2)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnTestButton)
        EnableEvent2Ctrl()

        while panel.Affirmed():
            UpdateConfig()
            panel.SetResult(
                self.stp,
            )

    class text:
        nameObs = 'Observation name:'
        accounts = 'Accounts to observation:'
        interval_1 = 'Interval:'
        interval_2 = 'minutes'
        field_2 = (
            'contains',
            "doesn't contain ",
            'is',
            "isn't",
            'starts with',
            'ends with',
        )
        radio_buttons = (
            'Global observation without filtering',
            'Message match all of the following rules',
            'Message match any of the following rules',
        )
        message = 'Show notification window'
        #colour = "Colours ..."
        totalEvent = 'Trigger total event'
        evtName = 'Event name:'
        tip0 = 'Show notification window with count of waiting e-mails'
        tip1 = 'After event triggering delete e-mail on server'
        tip2 = 'Start observation now'
        tip3 = 'Trigger event for each e-mail'
        tip4 = 'Trigger event in any change in the number of waiting messages'
        emailEvent = "E-mail event"
        totalEvent = 'Total event'
        payload = "Payload:"
        totalPayload = ("None", "Count")
        delete = "Delete"
        startNow = 'Start now !'
        backCol = 'Background colour:'
        forCol = 'Foreground colour:'
        warning = 'Was found no one account, corresponding to the list %s !'
#===============================================================================

class SendEmail(eg.ActionClass):
    def __call__(
        self,
        sbjct = '',
        From = '',
        To = '',
        Copy = '',
        Txt = '',
        Append = '',
        toName = '',
        references = None,
        messageID = None
    ):
        smt=SendMailThread(
            self.plugin,
            sbjct,
            From,
            To,
            Copy,
            Txt,
            Append,
            toName,
            references,
            messageID
        )
        smt.start()

    def Configure(
        self,
        sbjct = '',
        From = '',
        To = '',
        Copy = '',
        Txt = '',
        Append = '',
        toName = ''
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        subjectCtrl,fromCtrl,toCtrl,copyCtrl,outTextCtrl,textsCtrl,toNameCtrl, topSizer = SendCfg(
            self,
            panel,
            sbjct,
            From,
            To,
            Copy,
            Txt,
            Append,
            toName,
            self.text,
            self.plugin
        )
        panel.sizer.Add(topSizer,1,wx.EXPAND|wx.LEFT|wx.RIGHT,16)
        text = self.text
        # re-assign the test button
        def OnTestButton(event):
            t = SendMailThread(
                self.plugin,
                subjectCtrl.GetValue(),
                fromCtrl.GetStringSelection(),
                toCtrl.GetValue(),
                copyCtrl.GetStringSelection(),
                outTextCtrl.GetValue(),
                textsCtrl.GetValue(),
                toNameCtrl.GetValue(),
                None,
                None
            )
            t.start()
        panel.dialog.buttonRow.testButton.SetLabel(text.sendNow)
        panel.dialog.buttonRow.testButton.SetToolTipString(text.tip3)
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, OnTestButton)

        def validation(event=None):
            flag = True
            if not validateEmailAddr(toCtrl.GetValue()):
                flag = False
            if subjectCtrl.GetValue()=='':
                flag = False
            panel.dialog.buttonRow.applyButton.Enable(flag)
            panel.dialog.buttonRow.okButton.Enable(flag)

        subjectCtrl.Bind(wx.EVT_TEXT, validation)
        toCtrl.Bind(wx.EVT_TEXT, validation)
        validation()
        panel.sizer.Layout()

        while panel.Affirmed():
            panel.SetResult(
                subjectCtrl.GetValue(),
                fromCtrl.GetStringSelection(),
                toCtrl.GetValue(),
                copyCtrl.GetStringSelection(),
                outTextCtrl.GetValue(),
                textsCtrl.GetValue(),
                toNameCtrl.GetValue()
            )

    class text:
        fromLabel = 'From:'
        toLabel = 'To:'
        copyLabel = 'Copy:'
        subjectLabel = 'Subject:'
        outText = "Text:"
        outTexts = "Append:"
        tip = 'Here can be expression as {eg.event.payload} too !'
        tip1 = "Recipient's Name (not obligatory)"
        tip2 = "Recipient's Address (obligatory)"
        tip3 = 'Send your e-mail now !'
        sendNow = 'Send now !'
        replyTitle = 'Reply'
#===============================================================================

class SendMailDlg(wx.MiniFrame):
    def __init__(self, parent):
        wx.MiniFrame.__init__(
            self,
            parent,
            -1,
            '',
            size = (360, 270),
            style = wx.CAPTION|wx.RESIZE_BORDER,
            name  = 'Send Email'
        )
        self.SetBackgroundColour(wx.NullColour)

    def ShowSendMailDlg(
        self,
        sbjct = '',
        From = '',
        To = '',
        Copy = '',
        Txt = '',
        Append = '',
        toName = '',
        text = SendEmail.text,
        plugin = None,
        references = None,
        messageID = None
    ):
        self.SetTitle(3*' '+text.replyTitle)
        panel = self
        subjectCtrl,fromCtrl,toCtrl,copyCtrl,outTextCtrl,textsCtrl,toNameCtrl,topSizer = SendCfg(
            self,
            panel,
            sbjct,
            From,
            To,
            Copy,
            Txt,
            Append,
            toName,
            text,
            plugin
        )
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        sizer.Add((1,10))
        sizer.Add(topSizer,1,wx.EXPAND|wx.LEFT|wx.RIGHT,16)
        line = wx.StaticLine(self, -1, size=(20,-1),pos = (200,0), style=wx.LI_HORIZONTAL)
        btn1 = wx.Button(self, wx.ID_OK)
        btn1.SetLabel(text.sendNow)
        btn1.Enable(False)
        btn1.SetDefault()
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btn2.SetLabel(plugin.text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        sizer.Add((1,5))
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 12)
        sizer.Add((1,5))

        def onSomeChange(evt):
            flag = True
            if not validateEmailAddr(toCtrl.GetValue()):
                flag = False
            if subjectCtrl.GetValue()=='':
                flag = False
            if outTextCtrl.GetValue()=='':
                flag = False
            btn1.Enable(flag)

        toCtrl.Bind(wx.EVT_TEXT,onSomeChange)
        outTextCtrl.Bind(wx.EVT_TEXT,onSomeChange)
        subjectCtrl.Bind(wx.EVT_TEXT,onSomeChange)

        def onClose(evt):
            self.MakeModal(False)
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON,onCancel)

        def onSend(evt):
            t = SendMailThread(
                self.plugin,
                subjectCtrl.GetValue(),
                fromCtrl.GetStringSelection(),
                toCtrl.GetValue(),
                copyCtrl.GetStringSelection(),
                outTextCtrl.GetValue(),
                textsCtrl.GetValue(),
                toNameCtrl.GetValue(),
                references,
                messageID
            )
            t.start()
            self.Close()

        btn1.Bind(wx.EVT_BUTTON,onSend)
        sizer.Layout()
        sizer.Fit(self)
        size = self.GetSize()
        self.SetMinSize(size)
        self.MakeModal(True)
        self.Centre()
        self.Show()
        self.SetFocus()
        self.Raise()
#===============================================================================

ACTIONS = (
    (StartObservation, 'StartObservation', 'Start observation', 'Start observation.', None),
    (AbortObservation, 'AbortObservation', 'Abort observation', 'Abort observation.', None),
    (AbortAllObservations, 'AbortAllObservations', 'Abort all observations', 'Abort all observations.', None),
    (SendEmail, 'SendEmail', 'Send e-mail', 'Send e-mail.', None),
)
#===============================================================================

class E_mail(eg.PluginClass):
    configs = []
    servers = []
    texts = []
    groups = []

    def __init__(
        self,
    ):
        self.AddActionsFromList(ACTIONS)
        self.observThreads = {}

    def __stop__(self):
        self.AbortAllObservations(close = True)

    def __close__(self):
        self.AbortAllObservations(close = True)

    def __start__(
        self,
        configs=[],
        servers=[],
        texts = [],
        groups = [],
        passINC = eg.Bunch(data={}),
        passSMTP = eg.Bunch(data={})
    ):
        self.observThreads = {}
        self.tempData = []
        self.passINC = passINC
        self.passSMTP = passSMTP
        self.servers=servers
        self.configs=configs
        del passINC
        del passSMTP
        self.texts = texts
        self.groups = groups

    def StartObservation(
        self,
        setup,
        notifFrame,
    ):
        observName = setup[0]
        if observName in self.observThreads:
            ot = self.observThreads[observName]
            if ot.isAlive():
                ot.AbortObservation()
        if not observName in [item[0] for item in self.tempData]:
            self.tempData.append([observName, 0, [], None, notifFrame]) #update temporary data store
        ot = ObservationThread(
            setup,
            self,
            notifFrame
        )
        ot.start()

    def AbortObservation(self, observName):
        if observName in self.observThreads:
            ot = self.observThreads[observName]
            ot.AbortObservation()

    def AbortAllObservations(self, close=False):
        thrds = list(enumerate(self.observThreads))
        thrds.reverse()
        for i, item in thrds:
            ot = self.observThreads[item]
            ot.AbortObservation(close)

    def Configure(
        self,
        configs=[],
        servers=[],
        texts = [],
        groups = [],
        passINC = eg.Bunch(data={}),
        passSMTP = eg.Bunch(data={})
    ):
        panel = eg.ConfigPanel(self)
        panel.cfgs = cpy(configs)
        panel.servers = cpy(servers)
        panel.txts = cpy(texts)
        panel.grps = cpy(groups)
        del configs
        del servers
        del texts
        del groups
        panel.passINC = {}
        panel.passSMTP = {}
        for i,item in list(enumerate(passINC.data)):
            panel.passINC[item]=passINC.data[item]
        for i,item in list(enumerate(passSMTP.data)):
            panel.passSMTP[item]=passSMTP.data[item]
        text = self.text
        panel.dialog.buttonRow.okButton.SetToolTipString(text.warning)

        def boxEnable(enable):
            choiceType.Enable(enable) #
            labelCtrl.Enable(enable)
            labelLbl.Enable(enable)
            userNameLbl.Enable(enable)
            userNameCtrl.Enable(enable)
            mailAddressLbl.Enable(enable)
            mailAddressCtrl.Enable(enable)
            replAddressLbl.Enable(enable)
            replAddressCtrl.Enable(enable)
            incServerLbl.Enable(enable)
            incServerCtrl.Enable(enable)
            incPortLbl.Enable(enable)
            incPortCtrl.Enable(enable)
            userLoginLbl.Enable(enable)
            userLoginCtrl.Enable(enable)
            userPasswordLbl.Enable(enable)
            userPasswordCtrl.Enable(enable)
            outServerLbl.Enable(enable)
            panel.outServerCtrl.Enable(enable)
            choiceSecureLbl.Enable(enable)
            choiceSecureCtrl.Enable(enable)
            useSecureCtrl.Enable(enable)
            outServerBtn.Enable(enable)

        def setValue(item):
            labelCtrl.ChangeValue(item[0])
            choiceType.SetSelection(item[1])
            userNameCtrl.SetValue(item[2])
            mailAddressCtrl.SetValue(item[3])
            replAddressCtrl.SetValue(item[4])
            incServerCtrl.SetValue(item[5])
            incPortCtrl.SetValue(item[6])
            userLoginCtrl.SetValue(item[7])
            panel.outServerCtrl.SetStringSelection(item[8])
            choiceSecureCtrl.SetSelection(item[9])
            useSecureCtrl.SetValue(item[10])
            if item[0] != '' and item[0] in panel.passINC:
                userPasswordCtrl.ChangeValue(panel.passINC[item[0]])
            else:
                userPasswordCtrl.ChangeValue('')

        def validation():
            flag = True
            label = labelCtrl.GetValue()
            if label == "":
                flag = False
            else:
                if [n[0] for n in panel.cfgs].count(label)!=1:
                    flag = False
            if not validateEmailAddr(mailAddressCtrl.GetValue()):
                flag = False
            replAddr = replAddressCtrl.GetValue()
            if replAddr != '' and not validateEmailAddr(replAddr):
                flag = False
            if incServerCtrl.GetValue() == '':
                flag = False
            if incPortCtrl.GetValue() < 0:
                flag = False
            if userLoginCtrl.GetValue() == '':
                flag = False
            if userPasswordCtrl.GetValue() == '':
                flag = False
            if panel.outServerCtrl.GetSelection() == -1:
                flag = False
            panel.dialog.buttonRow.applyButton.Enable(flag)
            panel.dialog.buttonRow.okButton.Enable(flag)
            btnApp.Enable(flag)

        panel.validation = validation
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        topLeftSizer = wx.FlexGridSizer(5,2,2,8)
        leftSizer.Add(topLeftSizer,0,wx.EXPAND)
        topMiddleSizer=wx.BoxSizer(wx.VERTICAL)
        previewLbl=wx.StaticText(panel, -1, text.accountsList)
        listBoxCtrl=wx.ListBox(
            panel,-1,
            size=wx.Size(120,106),
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB
        )
        labelLbl=wx.StaticText(panel, -1, text.label)
        labelCtrl=wx.TextCtrl(panel,-1,'')
        choiceType = wx.RadioBox(
            panel,
            -1,
            text.accType,
            choices=(text.eBoxCase),
            style=wx.RA_SPECIFY_ROWS
        )
        #Box content
        userNameLbl=wx.StaticText(panel, -1, text.userName)
        userNameCtrl=wx.TextCtrl(panel,-1,'')
        userNameCtrl.SetMaxSize((194,-1))
        mailAddressLbl=wx.StaticText(panel, -1, text.mailAddress)
        mailAddressCtrl=wx.TextCtrl(panel,-1,'')
        replAddressLbl=wx.StaticText(panel, -1, text.replAddress)
        replAddressCtrl=wx.TextCtrl(panel,-1,'')
        incServerLbl=wx.StaticText(panel, -1, text.incServer)
        incServerCtrl=wx.TextCtrl(panel,-1,'')
        incPortLbl=wx.StaticText(panel, -1, text.incPort)
        incPortCtrl=intCtrl(panel,-1,0,size=(50,-1))
        userLoginLbl=wx.StaticText(panel, -1, text.userLogin)
        userLoginCtrl=wx.TextCtrl(panel,-1,'')
        userPasswordLbl=wx.StaticText(panel, -1, text.userPassword)
        userPasswordCtrl=wx.TextCtrl(panel,-1,'',style = wx.TE_PASSWORD)
        outServerLbl=wx.StaticText(panel, -1, text.outServer)
        panel.outServerCtrl=wx.Choice(
            panel,
            -1,
            choices = [n[0] for n in panel.servers],
        )
        outServerBtn = wx.Button(panel,-1,'...',size=(50,-1))
        viewerBtn = wx.Button(panel,-1,text.viewerTitle)
        panel.txtsBtn = wx.Button(panel,-1,text.textsTitle)
        panel.grpsBtn = wx.Button(panel,-1,text.groupsTitle)
        choiceSecureLbl =wx.StaticText(panel, -1, text.secureConnectLabel)
        choiceSecureCtrl = wx.Choice(
            panel,
            -1,
            choices=(text.secureConnectChoice1),
        )
        choiceSecureCtrl.SetMaxSize((194,-1))
        useSecureCtrl = wx.CheckBox(panel, label = text.useSecure)
        serverSizer = wx.BoxSizer(wx.HORIZONTAL)
        serverSizerL = wx.BoxSizer(wx.VERTICAL)
        serverSizerL.Add(incServerLbl,0,wx.EXPAND)
        serverSizerL.Add(incServerCtrl,0,wx.EXPAND)
        serverSizerR = wx.BoxSizer(wx.VERTICAL)
        serverSizerR.Add(incPortLbl,0,wx.EXPAND|wx.LEFT,3)
        serverSizerR.Add(incPortCtrl,0,wx.EXPAND)
        serverSizer.Add(serverSizerL,1,wx.EXPAND)
        serverSizer.Add(serverSizerR,0,wx.EXPAND|wx.LEFT,5)
        outServSizer = wx.BoxSizer(wx.HORIZONTAL)
        outServSizerL = wx.BoxSizer(wx.VERTICAL)
        outServSizerL.Add(outServerLbl,0,wx.EXPAND|wx.TOP,3)
        outServSizerL.Add(panel.outServerCtrl,0,wx.EXPAND)
        outServSizerR = wx.BoxSizer(wx.VERTICAL)
        outServSizerR.Add(outServerBtn,0,wx.EXPAND|wx.TOP,15)
        outServSizer.Add(outServSizerL,1,wx.EXPAND)
        outServSizer.Add(outServSizerR,0,wx.EXPAND|wx.LEFT,5)
        box = wx.StaticBox(panel,-1,text.param)
        rightSizer = wx.StaticBoxSizer(box,wx.VERTICAL)
        rightSizer.Add(userNameLbl,0,wx.TOP,3)
        rightSizer.Add(userNameCtrl,0,wx.EXPAND)
        rightSizer.Add(userLoginLbl,0,wx.TOP,3)
        rightSizer.Add(userLoginCtrl,0,wx.EXPAND)
        rightSizer.Add(userPasswordLbl,0,wx.TOP,3)
        rightSizer.Add(userPasswordCtrl,0,wx.EXPAND)
        rightSizer.Add(mailAddressLbl,0,wx.TOP,3)
        rightSizer.Add(mailAddressCtrl,0,wx.EXPAND)
        rightSizer.Add(replAddressLbl,0,wx.TOP,3)
        rightSizer.Add(replAddressCtrl,0,wx.EXPAND)
        rightSizer.Add(useSecureCtrl,0,wx.TOP,5)
        rightSizer.Add(choiceSecureLbl,0,wx.TOP,3)
        rightSizer.Add(choiceSecureCtrl,0,wx.EXPAND)
        rightSizer.Add(serverSizer,0,wx.EXPAND|wx.TOP,3)
        rightSizer.Add(outServSizer,0,wx.EXPAND|wx.TOP,3)
        topLeftSizer.Add(previewLbl,0,wx.TOP,5)
        topLeftSizer.Add((1,1))
        topLeftSizer.Add(listBoxCtrl,0,wx.TOP,5)
        topLeftSizer.Add(topMiddleSizer,0,wx.TOP,5)
        topLeftSizer.Add(labelLbl,0,wx.TOP,3)
        topLeftSizer.Add((1,1))
        topLeftSizer.Add(labelCtrl,0,wx.EXPAND)
        topLeftSizer.Add((1,1))
        topLeftSizer.Add(choiceType,0,wx.EXPAND|wx.TOP,1)
        topLeftSizer.Add((1,1))
        leftSizer.Add(viewerBtn,0,wx.EXPAND|wx.TOP,10)
        leftSizer.Add(panel.txtsBtn,0,wx.EXPAND|wx.TOP,10)
        leftSizer.Add(panel.grpsBtn,0,wx.EXPAND|wx.TOP,10)
        #Button UP
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_OTHER, (16, 16))
        btnUP = wx.BitmapButton(panel, -1, bmp)
        btnUP.Enable(False)
        topMiddleSizer.Add(btnUP)
        #Button DOWN
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_OTHER, (16, 16))
        btnDOWN = wx.BitmapButton(panel, -1, bmp)
        btnDOWN.Enable(False)
        topMiddleSizer.Add(btnDOWN,0,wx.TOP,3)
        #Buttons 'Delete' and 'Insert new'
        w1 = panel.GetTextExtent(text.delete)[0]
        w2 = panel.GetTextExtent(text.insert)[0]
        if w1 > w2:
            btnDEL=wx.Button(panel,-1,text.delete)
            btnApp=wx.Button(panel,-1,text.insert,size=btnDEL.GetSize())
        else:
            btnApp=wx.Button(panel,-1,text.insert)
            btnDEL=wx.Button(panel,-1,text.delete,size=btnApp.GetSize())
        btnDEL.Enable(False)
        topMiddleSizer.Add(btnDEL,0,wx.TOP,5)
        topMiddleSizer.Add(btnApp,0,wx.TOP,5)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer)
        mainSizer.Add(rightSizer,0,wx.LEFT|wx.EXPAND,14)
        panel.sizer.Add(mainSizer)
        if len(panel.cfgs) > 0:
            listBoxCtrl.Set([n[0] for n in panel.cfgs])
            listBoxCtrl.SetSelection(0)
            setValue(panel.cfgs[0])
            self.oldSel=0
            btnUP.Enable(True)
            btnDOWN.Enable(True)
            btnDEL.Enable(True)
        else:
            boxEnable(False)
            panel.dialog.buttonRow.applyButton.Enable(False)
            panel.dialog.buttonRow.okButton.Enable(False)
        panel.sizer.Layout()

        def OnLabelAndPassword(evt):
            if panel.cfgs<>[]:
                sel = self.oldSel
                label = labelCtrl.GetValue().strip()
                val = userPasswordCtrl.GetValue().strip()
                panel.cfgs[sel][0]=label
                listBoxCtrl.Set([n[0] for n in panel.cfgs])
                listBoxCtrl.SetSelection(sel)
                if val != '':
                    panel.passINC[label]=val
                validation()
            evt.Skip()
        labelCtrl.Bind(wx.EVT_TEXT, OnLabelAndPassword)
        userPasswordCtrl.Bind(wx.EVT_TEXT, OnLabelAndPassword)

        def setPort():
            ports=((110,-1,-1,995),(143,-1,-1,993))
            secure = choiceSecureCtrl.GetSelection()
            type = choiceType.GetSelection()
            port = ports[type][secure]
            if port>-1:
                incPortCtrl.SetValue(port)

        def onChoiceType(evt):
            type = choiceType.GetSelection()
            sel = self.oldSel
            panel.cfgs[sel][1] = type
            setPort()
            validation()
            evt.Skip()
        choiceType.Bind(wx.EVT_RADIOBOX, onChoiceType)

        def onUserName(evt):
            if panel.cfgs<>[]:
                val = userNameCtrl.GetValue().strip()
                sel = self.oldSel
                panel.cfgs[sel][2] = val
            #    validation()         #optional
            evt.Skip()
        userNameCtrl.Bind(wx.EVT_TEXT, onUserName)

        def onMailAddress(evt):
            if panel.cfgs<>[]:
                val = mailAddressCtrl.GetValue().strip()
                sel = self.oldSel
                panel.cfgs[sel][3] = val
                validation()
            evt.Skip()
        mailAddressCtrl.Bind(wx.EVT_TEXT, onMailAddress)

        def onReplAddress(evt):
            if panel.cfgs<>[]:
                val = replAddressCtrl.GetValue().strip()
                sel = self.oldSel
                panel.cfgs[sel][4] = val
                validation()
            evt.Skip()
        replAddressCtrl.Bind(wx.EVT_TEXT, onReplAddress)

        def onIncServer(evt):
            if panel.cfgs<>[]:
                val = incServerCtrl.GetValue().strip()
                sel = self.oldSel
                panel.cfgs[sel][5] = val
                validation()
            evt.Skip()
        incServerCtrl.Bind(wx.EVT_TEXT, onIncServer)

        def onIncPort(evt):
            if panel.cfgs<>[]:
                val = incPortCtrl.GetValue()
                sel = self.oldSel
                panel.cfgs[sel][6] = val
                validation()
            evt.Skip()
        incPortCtrl.Bind(wx.EVT_TEXT, onIncPort)

        def onUserLogin(evt):
            if panel.cfgs<>[]:
                val = userLoginCtrl.GetValue().strip()
                sel = self.oldSel
                panel.cfgs[sel][7] = val
                validation()
            evt.Skip()
        userLoginCtrl.Bind(wx.EVT_TEXT, onUserLogin)

        def onOutServer(evt):
            if panel.cfgs<>[]:
                val = panel.outServerCtrl.GetStringSelection()
                sel = self.oldSel
                panel.cfgs[sel][8] = val
                validation()
            evt.Skip()
        panel.outServerCtrl.Bind(wx.EVT_CHOICE, onOutServer)

        def onChoiceSecure(evt):
            if panel.cfgs<>[]:
                val = choiceSecureCtrl.GetSelection()
                sel = self.oldSel
                panel.cfgs[sel][9] = val
    #            validation()
            setPort()
            evt.Skip()
        choiceSecureCtrl.Bind(wx.EVT_CHOICE, onChoiceSecure)

        def onUseSecure(evt):
            if panel.cfgs<>[]:
                val = useSecureCtrl.GetValue()
                sel = self.oldSel
                panel.cfgs[sel][10] = val
    #            validation()
            evt.Skip()
        useSecureCtrl.Bind(wx.EVT_CHECKBOX, onUseSecure)

        def onServButton(evt):
            dlg = outServerDialog(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowOutServDlg)
            evt.Skip()
        outServerBtn.Bind(wx.EVT_BUTTON, onServButton)

        def onTxtsButton(evt):
            dlg = outTextsDialog(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowOutTxtsDlg)
            evt.Skip()
        panel.txtsBtn.Bind(wx.EVT_BUTTON, onTxtsButton)

        def onGrpsButton(evt):
            dlg = groupsDialog(
                parent = panel,
                plugin = self,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowGroupsDlg)
            evt.Skip()
        panel.grpsBtn.Bind(wx.EVT_BUTTON, onGrpsButton)

        def onViewerButton(evt):
            dlg = observViewerDialog(
                parent = panel,
                plugin = self,
                observThreads=self.observThreads
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowObservViewerDialog)
            text.viewerTitle,
            evt.Skip()
        viewerBtn.Bind(wx.EVT_BUTTON, onViewerButton)

        def onListClick(evt):
            sel = listBoxCtrl.GetSelection()
            label = labelCtrl.GetValue()
            if label.strip()<>"":
                if [n[0] for n in panel.cfgs].count(label)==1:
                    self.oldSel=sel
                    item = panel.cfgs[sel]
                    setValue(item)
            listBoxCtrl.SetSelection(self.oldSel)
            listBoxCtrl.SetFocus()
            evt.Skip()
        listBoxCtrl.Bind(wx.EVT_LISTBOX, onListClick)

        def onButtonUp(evt):
            newSel,panel.cfgs=Move(panel.cfgs,listBoxCtrl.GetSelection(),-1)
            listBoxCtrl.Set([n[0] for n in panel.cfgs])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnUP.Bind(wx.EVT_BUTTON, onButtonUp)

        def onButtonDown(evt):
            newSel,panel.cfgs=Move(panel.cfgs,listBoxCtrl.GetSelection(),1)
            listBoxCtrl.Set([n[0] for n in panel.cfgs])
            listBoxCtrl.SetSelection(newSel)
            self.oldSel = newSel
            evt.Skip()
        btnDOWN.Bind(wx.EVT_BUTTON, onButtonDown)

        def onButtonDelete(evt):
            lngth=len(panel.cfgs)
            if lngth==2:
                btnUP.Enable(False)
                btnDOWN.Enable(False)
            sel = listBoxCtrl.GetSelection()
            if lngth == 1:
                panel.cfgs=[]
                listBoxCtrl.Set([])
                item = ['', 0, '', '', '', '', 0, '', '', 0, False]
                setValue(item)
                boxEnable(False)
                panel.dialog.buttonRow.applyButton.Enable(False)
                panel.dialog.buttonRow.okButton.Enable(False)
                btnDEL.Enable(False)
                btnApp.Enable(True)
                evt.Skip()
                return
            elif sel == lngth - 1:
                sel = 0
            self.oldSel = sel
            tmp = panel.cfgs.pop(listBoxCtrl.GetSelection())
            listBoxCtrl.Set([n[0] for n in panel.cfgs])
            listBoxCtrl.SetSelection(sel)
            item = panel.cfgs[sel]
            setValue(item)
            evt.Skip()
        btnDEL.Bind(wx.EVT_BUTTON, onButtonDelete)

        def OnButtonAppend(evt):
            if len(panel.cfgs)==1:
                btnUP.Enable(True)
                btnDOWN.Enable(True)
            boxEnable(True)
            labelCtrl.Enable(True)
            sel = listBoxCtrl.GetSelection() + 1
            self.oldSel=sel
            item = ['', 0, '', '', '', '', 0, '', '', 0, False]
            panel.cfgs.insert(sel,item)
            listBoxCtrl.Set([n[0] for n in panel.cfgs])
            listBoxCtrl.SetSelection(sel)
            setValue(item)
            setPort()
            choiceSecureCtrl.SetSelection(0)
            panel.outServerCtrl.Clear()
            panel.outServerCtrl.AppendItems(strings=[n[0] for n in panel.servers])
            panel.outServerCtrl.SetSelection(0)
            labelCtrl.SetFocus()
            btnApp.Enable(False)
            btnDEL.Enable(True)
            evt.Skip()
        btnApp.Bind(wx.EVT_BUTTON, OnButtonAppend)

        while panel.Affirmed():
            passINC.data=panel.passINC
            passSMTP.data=panel.passSMTP
            panel.SetResult(
                panel.cfgs,
                panel.servers,
                panel.txts,
                panel.grps,
                passINC,
                passSMTP
            )

    class text:
        label = 'Account name:'
        servLabel = 'Server name:'
        accountsList = 'List of accounts:'
        serversList = 'List of servers:'
        delete = 'Delete'
        insert = 'Add new'
        param = "Account parameters"
        servParam = "Server parameters"
        assignError = 'Account "%s" not exists!'
        eBoxCase = (
            'POP3',
            'IMAP',
        )
        accType = 'Account type'
        userName = 'User name (optional):'
        #user = 'User name:'
        mailAddress = 'E-mail address:'
        replAddress = 'Address for reply (optional):'
        incServer = 'Incoming server:'
        incPort = 'Port'
        userLogin = 'User login:'
        userPassword = 'User password:'
        outServerTitle = 'Outgoing Servers (SMTP) Settings'
        viewerTitle = 'Observations viewer/manager'
        secureConnectLabel = 'Use secure connection:'
        useName = 'Use name and password'
        secureConnectChoice1 = (
            'No',
#            'TLS, if available',
#            'TLS',
            '>>> TLS is not yet supported <<<',
            '>>> TLS is not yet supported <<<',
            'SSL',
        )
        secureConnectChoice2 = (
            'No',
            'TLS, if available',
            'TLS',
            'SSL',
        )
        useSecure = 'Use secure authentication'
        outServer = 'Outgoing SMTP server:'
        colLabels = (
            'Observation Name',
            'Interval',
            'Last check',
            'Total Event',
            'Message Event',
        )
        labelsDetails = (
            'Nr.',
            'Account',
            'Subject',
            'From',
        )

        listhead = "Currently active observation:"
        show = "Show"
        delete = "Delete"
        refresh = "Refresh"
        client = "E-mail client"
        reply = "Reply"
        close = "Close"
        textsTitle = 'Templates for outgoing e-mails'
        textsList = "List of texts:"
        txtLabel = "Text name:"
        outText = "Text:"
        groupsTitle = 'Recipient groups for outgoing e-mails'
        groupsList = "List of groups:"
        groupLabel = "Group name:"
        addressLabel = "E-mail address:"
        outAddress = "List of e-mail addresses:"
        deleteServer = ('Server "%s" is used in your configuration.\n'
            'You cannot remove it.')
        detTitle = 'Observation "%s" : %s new E-mails'
        popup = ("Show",
                "Delete",
                "Refresh",
                "E-mail client",
                "Close"
        )
        error0 = 'POP3 Protocol Error:'
        error1 = 'Cannot connect to POP server "%s:%i"'
        error2 = 'IMAP Protocol Error:'
        error3 = 'Cannot connect to IMAP server "%s:%i"'
        error4 = 'Cannot log in to account "%s" on server "%s:%i"'
        error5 = 'Cannot found server "%s", try use default server "%s".'
        error6 = 'SMTP Protocol Error:'
        error7 = 'Cannot connect to SMTP server "%s:%i"'
        error8 = 'Your message may not have been sent!'
        error9 = 'Cannot open default e-mail client !'
        tip0 = (
            "Right-click to hide the window\n"
            "Double-click to open/refresh details\n"
            "CTRL+Double-click to open default e-mail client"
        )
        notifLabel = 'waiting\ne-mail(s)'
        cancel = 'Cancel'
        ok = 'OK'
        buttons = (
            "Abort",
            "Abort all",
            "Refresh",
            "Close",
        )
        observStarts = 'Observation "%s" starts'
        warning = 'When any change in the configuration, will all running observations stopped!'
        wrote = '%s wrote:'
        field_1 = (
            'None',
            'Subject',
            'From',
            'Body',
        )
#===============================================================================

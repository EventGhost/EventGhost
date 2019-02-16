# -*- coding: utf-8 -*-
version = "0.3.0"

# plugins/PushBullet/__init__.py
#
# Copyright (C) 2014-2015  Pako <lubos.ruckl@gmail.com>
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
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# The BSD 3-Clause License (applies to parts of the code obtained from gcm.py)
# Copyright (c) <YEAR>, <OWNER>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.3.0 by topix
#   - code cleanup and splitted
# 0.2.21  by K 2017-10-04 12:14 GMT-7
#     - added - support for EventGhost 0.5
# 0.2.20  by Pako 2017-09-14 12:14 GMT+1 (+ another 1 due to DST)
#     - bugfix - pycurl workaround
# 0.2.19  by Pako 2017-06-26 14:40 GMT+1 (+ another 1 due to DST)
#     - bugfix (TypeError: run_forever() got an unexpected keyword argument 'http_proxy_auth')
# 0.2.18  by Pako 2017-04-20 12:29 GMT+1 (+ another 1 due to DST)
#     - bugfix (push file failed)
# 0.2.17  by Pako 2017-04-16 11:25 GMT+1 (+ another 1 due to DST)
#     - bugfix (incoming push type 'link' & 'url' parameter is missing)
# 0.2.16.1  by Pako 2016-07-03 07:04 GMT+1
#     - TEST VERSION - added html proxy support
# 0.2.16  by Pako 2016-06-05 06:39 GMT+1
#     - removed address and list pushes which have been deprecated for forever
# 0.2.15  by Pako 2016-02-07 19:04 GMT+1
#     - bugfix (sometime 'sender_email' parameter is missing)
# 0.2.14  by Pako 2015-12-24 20:38 GMT+1
#     - bugfix
# 0.2.13  by Pako 2015-12-12 20:39 GMT+1
#     - bugfixes
# 0.2.12  by Pako 2015-11-51 12:09 GMT+1
#     - 'sms_changed' handler added
#     - bugfixes
# 0.2.11  by Pako 2015-10-08 12:27 GMT+1
#     - icon (in mirrored notification) is now correctly displayed
# 0.2.10  by Pako 2015-10-04 11:00 GMT+1
#     - now can be dismissed also a push (not only mirror)
# 0.2.9  by Pako 2015-10-03 13:07 GMT+1
#     - plugin now reacts to push of type 'dismissal'.
#     - added action "Dismiss"
#     - when you close a mirrored notification (using right click),
#       push of type 'dismissal' is sent
# 0.2.8  by Pako 2015-09-24 12:43 GMT+1
#     - added opt. "Use the complete original push as last part of the payload"
# 0.2.7  by Pako 2015-09-15 12:36 GMT+1
#     - added "End to end encryption" support
#     - uses the first word out of the body as the event suffix (optionaly)
#     - added response to ping message
# 0.2.6  by Pako 2015-03-27 14:53 GMT+1
#     - photo of the sender is clipped into the shape of a circle
# 0.2.5  by Pako 2015-02-13 20:35 GMT+1
#     - bugfix - upload of non-ascii named file
# 0.2.4  by Pako 2015-01-28 20:35 GMT+1
#     - added action "Send bulk SMS to list from file"
# 0.2.3  by Pako 2015-01-25 13:06 GMT+1
#     - bugfix - missing getNmNr() function
# 0.2.2  by Pako 2015-01-23 09:06 GMT+1
#     - added action "Push to a single"
# 0.2.1  by Pako 2015-01-20 09:09 GMT+1
#     - bugfix (actions "Push reply" and "Push to everything" - GUI problem)
# 0.2.0  by Pako 2015-01-11 18:38 GMT+1
#     - code adapted to use the pycurl library instead of requests library
#     - (this was necessary because of changes pushbullet server certificate)
# 0.1.10  by Pako 2015-01-01 14:21 GMT+1
#     - added recipients groups (push and SMS)
#     - added WebSocketOpened and WebSocketClosed events
# 0.1.9  by Pako 2014-12-15 16:12 GMT+1
#     - bugfix (action "Send SMS to multiple recipients")
# 0.1.8  by Pako 2014-12-08 18:08 GMT+1
#     - added action "Send SMS to multiple recipients"
# 0.1.7  by Pako 2014-11-07 06:00 GMT+1
#     - bugfix
# 0.1.6  by Pako 2014-11-06 20:43 GMT+1
#     - bugfix
#     - multiload of plugin enabled
#     - added action "Send SMS"
# 0.1.5  by Pako 2014-10-22 12:43 GMT+1
#     - added option to push an image, obtained as clipboard content
# 0.1.4  by Pako 2014-10-03 19:38 GMT+1
#     - bugfixes
#     - better synchronization with the time of server
# 0.1.3  by Pako 2014-10-02 20:09 GMT+1
#     - quick bugfix
# 0.1.2  by Pako 2014-10-01 19:24 GMT+1
#     - added action "Push reply"
#     - added support of channels
# 0.1.1  by Pako 2014-09-29 09:58 GMT+1
#     - added action "Push screenshot"
# 0.1.0  by Pako 2014-08-30 08:40 GMT+1
#     - "websocket-client (websocket)" library used instead of "Tornado" library
#     - Reply dialog improved
# 0.0.25 by Pako 2014-08-22 10:48 GMT+1
#     - bugfix
# 0.0.24 by Pako 2014-08-21 20:00 GMT+1
#     - push type 'clip' is now supported
# 0.0.23 by Pako 2014-08-10 09:12 GMT+1
#     - event payload contains "push dictionary" always
#                                             (if it is a mirrored notification)
# 0.0.22 by Pako 2014-08-02 17:19 GMT+1
#     - bugfix (action "Set popups")
#     - fixed bug - when decoding escape sequences (mirrored notifications)
#     - fixed bug - when 'body' parameter is missing in push (type 'note')
# 0.0.21 by Pako 2014-07-11 12:44 GMT+1
#     - checkbox "Disable popping up of mirrored notification" changed to
#                "Enable popping up of mirrored notification"
#     - added action "Set popups" (enables, disables or toggles popups)
#     - added action "Get states of popups"
#     - action Push - added "smart" button "Apply, push and close"
#     - an image of the sender (on "Quick-Reply" dialogue) is now better
#     - reply buttons are now accompanied by an icon
# 0.0.20 by Pako 2014-06-25 13:39 GMT+1
#     - better text wrapping of mirrored notification
#     - the ability to copy text from an incoming message in the Reply dialogue
#     - disabling / enabling of mirroring for each application works again
# 0.0.19 by Pako 2014-06-22 12:21 GMT+1
#     - first version for release r1669 and later (no need to install libraries)
#     - mirror notifications are customizable now (colour, monitor, alignment)
#     - introduced a new event "ReplyAllowingMirror"
#     - added an action "Send reply to mirror"
#     - if there is a possibility to send a reply,
#                        then on the mirror notification is a new button "Reply"
# 0.0.18 by Pako 2014-05-30 18:45 GMT+1
#     - bugfix (when the 'title' parameter is missing in the received "Mirror")
# 0.0.17 by Pako 2014-05-30 11:53 GMT+1
#     - http://www.eventghost.net/forum/viewtopic.php?f=9&t=5709&p=31230#p31226
# 0.0.16 by Pako 2014-05-27 12:57 GMT+1
#     - bugfix (when friend is not "active")
# 0.0.15 by Pako 2014-05-25 12:51 GMT+1
#     - "Mirror" as kind of Push now exists only in action "Push to everything"
# 0.0.14 by Pako 2014-05-25 10:01 GMT+1
#     - incoming "Mirror" is processed differently (enforced by the new API)
# 0.0.13 by Pako 2014-05-21 06:17 GMT+1
#     - forced change of url, used to test connectivity
# 0.0.12 by Pako 2014-05-19 10:55 GMT+1
#     - added option to delete pushes, sent using this plugin
# 0.0.11 by Pako 2014-05-19 07:55 GMT+1
#     - pyPushBullet module from Azelphur no longer needed
#     - fixed issue with sending pushes to friends
# 0.0.10 by Pako 2014-05-17 10:58 GMT+1
#     - changes induced by introducing a new API
#     - added action "Delete push"
# 0.0.9 by Pako 2014-05-01 14:24 GMT+1
#     - added new action "Push to everything"
#     - optional message for push types "Link"
#                                            and "File/Picture" is now supported
# 0.0.8 by Pako 2014-04-18 17:04 GMT+1
#     - a pushed file can be defined using a variables now
# 0.0.7 by Pako 2014-04-15 16:43 GMT+1
#     - popping up of mirrored notification can now be disabled
# 0.0.6 by Pako 2014-04-13 09:20 GMT+1
#     - bugfix
#     - icons size 96x96 (if possible) are now using also when sending mirrors
# 0.0.5 by Pako 2014-04-11 11:25 GMT+1
#     - new SSL certificate for tornado lib 3.2 is valid
#     - icon with size 96x96 is now supported (mirroring)
# 0.0.4 by Pako 2014-03-26 10:04 GMT+1
#     - automatic opening of pictures is now optional feature
#     - added actions "Open file" and "Jump according to file extension"
#     - with the api_key is treated as with a password for more security
# 0.0.3 by Pako 2014-03-14 12:35 GMT+1
#     - 'not_user' excluded from friends
# 0.0.2 by Pako 2014-02-26 16:02 GMT+1
#     - added support for push to "All of my devices" (Tasker integration)
# 0.0.1 by Pako 2014-02-21 08:04 GMT+1
#     - websocket.py is no longer needed
#     - support url inserted
# 0.0.0 by Pako 2014-02-07 20:00 GMT+1
#     - first public version
# ===============================================================================

import eg

eg.RegisterPlugin(
    name="PushBullet",
    author="Pako",
    version=version,
    kind="other",
    guid="{C92AD47A-B959-44D5-A849-9FCCCAAC9572}",
    createMacrosOnAdd=True,
    canMultiLoad=True,
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACyUlEQVRYw+1XPUxUQRD+"
        "Zt/eu4M7ThQSiBgVvWgM2Jmo0YKCxIaChPgvFhTaohV2WkmnMTaaUBj0REiMhkQLCyuJ"
        "BitpTMSQIBoi4AXuwb2/3bEgHMcdx1+QZ8Ekr5ndN/vt983OzgLbFrARAOzuPFMfO1Td"
        "As76G7TWXcNnu58uOKpet9bFfdEkiCILPmYuFtfTWg8p3x8cufh8fEUA+x4075XlJUkj"
        "ap7KG+OZ6fTp8baXAwCQ6Gv9KAzjOOVOKA4AABiApRyvWzt+D0rkwMiFpMqfJMI1O2JG"
        "1CxfDpwkHM5OJErQ+tktE6a8LqPhJ0R0eX/yfKQAwEoRhCAjX651a0xkkCFqDWk8kiHz"
        "YaL3SmzNADY32ShCQrRqwrU9Ly6Fc5jNGvK/f5DxpkF0i+3J5i1nYFESUVFaVt1e2nY0"
        "FAgAAERMJypPHjx3oO8qiaAKkLkz3gTomAiwAh6zrYlEYAAArhIqVBsgAxQLl8SPSJ6v"
        "p1y0mK699K4/GaWQgTHAANhTHFwOKK112rEDA+D/yaRdy/0qA9n8jA1/OjNBrH/IVYXa"
        "RNHZU/AmZ6FmMiApPpMph6X2NUgQSBRePnrWzTYQrDSTNDa0tvYUVGoOKu2CXX++ZUpl"
        "+s2auCWd75MwoibkrtKlP7kKM9N2FoD724KMR5YFWrBZBuApaMeHshYXzXIREp9So1N9"
        "dud7ltAMlXag57ylQbReCshy4VoOaA19CYMBVaS0EKYcTt23k188AJA5FBdpWXOzh+eD"
        "b9xcNvRd9sSrBcdWngIbpvFMSOPxZMcHZ20A9BJaNrp1xYxRhOk2s9v78+Y7O3dQkqQ0"
        "a6SguVDKdGY4R45vACrXdfAEWdrX3fBUD5eVDPxqf6uWVbnqTmO9KUMtWLxsGliKrrGO"
        "N9mHScW9xrpSO9QExZFVrhiQgMdSDLEUg2M3+se333//tf0FeVUoa3993xsAAAAASUVO"
        "RK5CYII="
    ),
    description=ur'''<rst>
Sends/receives notifications (and links, pictures and files) 
to/from your Android device or browser (Chrome, Firefox) via PushBullet_.

Google account and PushBullet account (free) are required to use PushBullet_.

| Plugin uses libraries websocket-client_ and pyCurl_.
| Plugin also incorporates the majority of code from the file pbkdf2.py_
  and **gcm.py**.
| The file **gcm.py** is part of a project iphone-dataprotection_, 
  which is protected by a license `The BSD 3-Clause License`_.

Plugin version: %s

.. _PushBullet:                 https://www.pushbullet.com/
.. _websocket-client:           https://pypi.python.org/pypi/websocket-client
.. _pyCurl:                     http://pycurl.sourceforge.net/
.. _pbkdf2.py:                  https://www.dlitz.net/software/python-pbkdf2/
.. _iphone-dataprotection:      https://code.google.com/p/iphone-dataprotection/
.. _`The BSD 3-Clause License`: http://opensource.org/licenses/BSD-3-Clause
''' % version,
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=5709",
)


import logging
import os
import pycurl
from base64 import b64encode
from copy import deepcopy
from cStringIO import StringIO
from datetime import datetime
from json import dumps, loads
from locale import strcoll
from mimetypes import guess_type as mimetype
from shutil import copy as sh_copy, copyfileobj
from socket import gethostname
from os.path import abspath, basename, dirname, isdir, isfile, join
from tempfile import mktemp
from threading import currentThread, Thread
from time import time as ttime
from urllib import urlencode

import certifi
import wx.adv
from Crypto.Hash import SHA256

from .actions import (
    DeletePush,
    Dismiss,
    EnableDisablePopups,
    GetPopups,
    JumpIf,
    OpenFile,
    Push,
    PushScreenshot,
    SendReply,
    SendSMS,
    SendSMS2list,
    SendSMSgroup,
    SendSMSmulti,
)
from .texts import Text
from .utils import (
    gcm_decrypt,
    gcm_encrypt,
    get_icon,
    get_key_fingerprint,
    HMAC,
    PBKDF2,
    SEP
)
from .websocketclient import WebSocketClient
from .widgets import (
    CheckListComboBox,
    EnableDialog,
    MirrorNote,
    ProxyDialog,
    PushGroupDialog,
    SmsGroupDialog,
)


logging.basicConfig()

API = 'https://api.pushbullet.com/v2/'
API3 = 'https://api.pushbullet.com/v3/'
DEFAULT_WAIT = 35.0

BODY = {
    'type': 'stream',
    'manufacturer': 'EventGhost',
    'model': 'plugin by Pako',
    'icon': 'system',
    'app_version': int(version.replace(".", "")),
    'key_fingerprint': None
}

ACTIONS = (
    (
        Push,
        "Push",
        "Push",
        "Pushes to one (or more) of the device (or friend).",
        False
    ),
    (
        Push,
        "PushToGroup",
        "Push to group",
        "Pushes to recipient group.",
        "Gr"
    ),
    (
        Push,
        "PushToEverything",
        "Push to everything",
        "Pushes to all of your devices.",
        "Everything"
    ),
    (
        Push,
        "PushReply",
        "Push reply",
        "Pushes a reply to the device from which the original push was sent.",
        "Reply"
    ),
    (
        Push,
        "PushSingle",
        "Push to a single",
        "Pushes to just one recipient (specified by iden, email, nickname or channel tag).",
        "Single"
    ),
    (
        PushScreenshot,
        "PushScreenshot",
        "Grab and push image",
        "Pushes screenshot (or clipboard content) to one (or more) of the device (or friend).",
        False
    ),
    (
        PushScreenshot,
        "PushScreenshotToEverything",
        "Grab and push image to everything",
        "Pushes screenshot (or clipboard content) to all of your devices.",
        True
    ),
    (
        DeletePush,
        "DeletePush",
        "Delete push",
        "Deletes push.",
        None
    ),
    (
        OpenFile,
        'OpenFile',
        "Open file",
        "Opens (downloaded) file in the associated application.",
        None
    ),
    (
        JumpIf,
        'JumpIf',
        "Jump according to file extension",
        "Jumps if the file is/is not one of the listed extension.",
        None
    ),
    (
        SendSMS,
        'SendSMS',
        "Send SMS",
        "Sends SMS.",
        None
    ),
    (
        SendSMS2list,
        'SendSMS2list',
        "Send bulk SMS to list from file",
        "Sends bulk SMS to list, imported from specified file.",
        None
    ),
    (
        SendSMSmulti,
        'SendSMSmulti',
        "Send SMS to multiple recipients",
        "Sends SMS to multiple recipients.",
        None
    ),
    (
        SendSMSgroup,
        'SendSMSgroup',
        "Send SMS to recipient group",
        "Sends SMS to recipient group.",
        None
    ),
    (
        SendReply,
        'SendReply',
        "Send reply to mirror",
        "Sends a reply to application, whose notification was mirrored.",
        None
    ),
    (
        Dismiss,
        'Dismiss',
        "Dismiss the notification or push",
        "Dismisses the notification or push.",
        None
    ),
    (
        EnableDisablePopups,
        'EnableDisablePopups',
        "Set popups",
        "Enables, disables or toggles popups.",
        None
    ),
    (
        GetPopups,
        'GetPopups',
        "Get states of popups",
        "Gets states of popups (enabled or disabled).",
        None
    )
)


class PushBullet(eg.PluginClass):
    api_key = None
    auto_open = True
    auto_update = False
    channels = []
    conn_flag = False
    ct = None
    debug = 1
    devices = []
    disabled = []
    email = None
    enab_mirr = False
    flag1 = False
    flag2 = False
    flag_dev = True
    friends = []
    iden = None
    key = None
    last_message = 0
    modified_after = 0
    msg_wait = DEFAULT_WAIT
    notification_ids = {}
    pb = None
    sms_trds = {}
    source_user_iden = None
    targets = []
    text = Text
    updt_dvcs = None
    watchdog = None
    ws_c = None

    def __init__(self):
        super(PushBullet, self).__init__()
        self.AddActionsFromList(ACTIONS)

    def __start__(
        self,
        nickname=None,
        api_key="",
        iden="",
        prefix="PushBullet",
        mode=0,
        fldr="",
        debug=3,
        hide=15,
        p_hide=15,
        disabled=None,
        hide_btn=False,
        wavs="",
        auto_open=True,
        dummy="",
        enab_mirr=True,
        clr=(255, 255, 255),
        alignment=0,
        dspl=0,
        offset=(0, 0),
        filtered=None,
        push_groups=None,
        sms_groups=None,
        password="",
        first_word=True,
        compl_push=False,
        proxy=None
    ):
        if proxy is None:
            proxy = ["", 0, "", ""]
        if sms_groups is None:
            sms_groups = []
        if push_groups is None:
            push_groups = []
        if filtered is None:
            filtered = []
        if disabled is None:
            disabled = []
        self.proxy = proxy
        self.source_user_iden = None
        self.notification_ids = {}
        self.push_groups = push_groups
        self.sms_groups = sms_groups
        if filtered and isinstance(filtered[0], list):  # backward compatibility
            tmp = []
            for i, item in enumerate(filtered[0]):
                if filtered[1][i]:
                    tmp.append(item)
            filtered = tmp
        self.filtered = filtered

        if self.auto_update:
            self.auto_update = False
            return
        if isinstance(api_key, eg.Password):
            api_key = api_key.Get()
        self.api_key = api_key
        self.pssd = password
        self.key = None
        self.info.eventPrefix = prefix
        self.nickname = nickname
        self.iden = iden
        self.prefix = prefix
        self.mode = mode
        self.fldr = fldr if isdir(fldr) else eg.folderPath.TemporaryFiles
        self.debug = debug
        self.hide = hide
        self.p_hide = p_hide

        self.disabled = []
        for item in disabled:  # backward compatibility
            self.disabled.append(item if len(item) == 2 else item[1:])
        self.hideBtn = hide_btn
        self.wavs = wavs
        self.auto_open = auto_open
        self.firstWord = first_word
        self.complPush = compl_push
        self.enabMirr = enab_mirr
        self.clr = clr
        self.alignment = alignment
        self.dspl = dspl
        self.offset = offset
        self.conn_flag = False
        self.sms_trds = {}
        self.updt_dvcs = eg.scheduler.AddTask(2.0, self.update_devices)

    def connectivity(self):
        # header = StringIO()
        body = StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.CAINFO, certifi.where())
        # curl.setopt(pycurl.HEADERFUNCTION, header.write)
        curl.setopt(pycurl.WRITEFUNCTION, body.write)
        curl.setopt(pycurl.URL, 'http://www.google.com')
        curl.setopt(pycurl.CONNECTTIMEOUT, 1)
        if self.proxy[0]:
            curl.setopt(pycurl.PROXY, str(self.proxy[0]))
            curl.setopt(pycurl.PROXYPORT, self.proxy[1])
            if self.proxy[2]:
                curl.setopt(
                    pycurl.PROXYUSERPWD,
                    "%s:%s" % (str(self.proxy[2]), str(self.proxy[3].Get()))
                )
        try:
            curl.perform()
            status_code = curl.getinfo(pycurl.RESPONSE_CODE)
            curl.close()
        except:
            eg.PrintTraceback()
            status_code = None
        return status_code in (200, 302)

    def stop_watchdog(self):
        if self.watchdog:
            try:
                eg.scheduler.CancelTask(self.watchdog)
            except ValueError:
                pass

    def stop_updt_dvcs(self):
        fcs = [i[2][0] for i in eg.scheduler.__dict__['heap'] if isinstance(i[2], tuple)]
        if self.update_devices in fcs:
            try:
                eg.scheduler.CancelTask(self.updt_dvcs)
            except ValueError:
                pass

    def OnComputerResume(self, dummy):
        self.updt_dvcs = eg.scheduler.AddTask(5.0, self.update_devices)
        self.watchdog = eg.scheduler.AddTask(15.0, self.watcher)

    def OnComputerSuspend(self, dummy):
        self.stop_watchdog()
        self.stop_updt_dvcs()
        if self.ws_c:
            self.ws_c.close()
        self.ws_c = None
        self.ct = None
        self.devices = []
        self.friends = []
        self.channels = []
        self.targets = []

    def __stop__(self):
        if self.auto_update:
            return
        self.stop_watchdog()
        self.stop_updt_dvcs()
        if self.ws_c:
            self.ws_c.close()
        self.ws_c = None
        self.ct = None
        self.watchdog = None
        self.devices = []
        self.friends = []
        self.channels = []
        self.targets = []
        self.sms_trds = {}
        self.email = None

    def log(self, message, level):
        if self.debug >= level:
            print "%s: %s" % (self.name, message)

    @staticmethod
    def parse_argument(arg):
        try:
            arg = eg.ParseString(arg)
        except (ValueError, TypeError):
            pass
        try:
            arg = eval(arg)
        except (ValueError, TypeError):
            pass
        return arg

    def watcher(self):
        if not self.info.isStarted:
            return
        if self.api_key and (ttime() - self.last_message) > self.msg_wait:
            if self.connectivity():
                self.conn_flag = True
                self.TriggerEvent("InternetConnection.Restored")
                self.log(self.text.reconnect, 2)
                self.msg_wait = min(600000, self.msg_wait * 2)
                self.refresh_web_socket()
            elif self.conn_flag:
                self.log(self.text.waiting, 1)
                self.conn_flag = False
                self.TriggerEvent("InternetConnection.Broken")
        elif not self.conn_flag:
            if self.connectivity():
                self.conn_flag = True
                self.TriggerEvent("InternetConnection.Restored")
        self.stop_watchdog()
        self.watchdog = eg.scheduler.AddTask(5.0, self.watcher)

    def on_open(self, _):
        self.TriggerEvent(self.text.wsOpenedEvt)
        res, flag = self.request("GET", API + 'pushes?limit=1&modified_after=0.0')
        if not flag or not isinstance(res, dict) or 'pushes' not in res:
            self.log(self.text.fRetrTmstmp, 1)
            return
        pushes = res['pushes']
        for push in pushes:
            try:
                self.modified_after = max(self.modified_after, push['modified'])
                self.log(self.text.mdfdUpd % self.modified_after, 4)
            except ValueError:
                self.log(self.text.fRetrTmstmp, 1)

    def establish_subscriber(self):
        if self.ws_c:
            return
        self.flag1 = False
        url = 'wss://stream.pushbullet.com/websocket/' + self.api_key
        self.ws_c = WebSocketClient(url, self)
        self.ct = Thread(target=self.ws_c.start)
        self.ct.start()
        self.last_message = ttime()
        self.stop_watchdog()
        self.watchdog = eg.scheduler.AddTask(0.01, self.watcher)
        self.log(self.text.addLstnr, 4)

    def refresh_web_socket(self):
        self.msg_wait = DEFAULT_WAIT
        if self.ws_c:
            self.ws_c.close()
        self.ws_c = None
        self.establish_subscriber()

    def request_threads(self, iden):
        res, flag = self.request(
            "POST",
            API3 + 'get-permanent',
            data={'key': iden + '_threads'}
        )

        self.log(self.text.thrReqRes % repr(res), 4)
        if not flag or not isinstance(res, dict) or 'data' not in res:
            self.log(self.text.fLoadThrds, 1)
            return []
        data = res['data']
        if 'encrypted' in data and data['encrypted']:
            if self.key:
                decrypted = gcm_decrypt(self.key, data[u'ciphertext'])
                try:
                    data = loads(decrypted)
                    if not isinstance(data, dict):
                        self.log(self.text.e2eMssg2, 2)
                        return []
                except ValueError:
                    self.log(self.text.e2eMssg3, 2)
                    return []
            else:
                eg.PrintNotice(self.text.noKey)
                return []
        self.log(self.text.thrdsRcvd % self.get_device(iden), 4)
        return data['threads'] if 'threads' in data else []

    def on_message(self, _, m):
        if not self.info.isStarted:
            if self.ws_c:
                self.ws_c.close()
        if not self.targets:
            if self.flag1:
                self.flag2 = True
            else:
                self.updt_dvcs = eg.scheduler.AddTask(5.00, self.update_devices)
            return
        if m is None:
            return
        try:
            m = loads(m)
            self.log(self.text.wsMssg % repr(m), 5)
            self.last_message = ttime()
            self.msg_wait = DEFAULT_WAIT
        except ValueError:
            eg.PrintTraceback()
            self.refresh_web_socket()
            return
        if m['type'] == 'nop':
            pass
        elif m['type'] == 'alert':
            if m.target_device_iden != self.iden:
                return
            # noinspection PyArgumentList
            self.TriggerEvent(
                'Alert',
                m['title'] or "Empty",
                payload=m['body']
            )
        elif m['type'] == 'push':
            push = m['push']
            if 'encrypted' in push and push['encrypted']:
                if self.key:
                    decrypted = gcm_decrypt(self.key, push['ciphertext'])
                    if decrypted is None:
                        self.log(self.text.e2eMssg1, 2)
                        return
                    try:
                        push = loads(decrypted)
                        self.log(self.text.dcrptdMssg % repr(push), 5)
                        if not isinstance(push, dict):
                            self.log(self.text.e2eMssg2, 2)
                            return
                    except ValueError:
                        self.log(self.text.e2eMssg3, 2)
                        return
                else:
                    eg.PrintNotice(self.text.noKey)
                    return
            if push['type'] == 'mirror':
                try:
                    self.process_mirror(push)
                except ValueError:
                    eg.PrintTraceback()
            elif push['type'] == 'clip':
                dev = push['device_iden'] if 'device_iden' in push else None
                dev = push['source_device_iden'] \
                    if 'source_device_iden' in push else dev
                if dev not in self.filtered:
                    try:
                        self.process_push(push)
                    except ValueError:
                        eg.PrintTraceback()
            elif push['type'] == 'dismissal':
                notification_id = push['notification_id']
                if notification_id in self.notification_ids:
                    win = self.notification_ids[notification_id]
                    win.Close()
            elif push['type'] == 'messaging_extension_reply':
                pass
            elif push['type'] == 'mute':
                pass
            elif push['type'] == 'unmute':
                pass
            elif push['type'] == 'pong':
                pass
            elif push['type'] == 'ping':
                pong = {
                    'type': 'pong',
                    "device_iden": self.iden,
                }
                res, flag = self.request(
                    "POST",
                    API + 'ephemerals',
                    data={"type": "push", "push": pong}
                )
                self.log(self.text.rspnsr % repr(res), 4)
                if not flag:
                    self.log(self.text.fPong, 1)
                    return
                self.log(self.text.pong, 3)
            elif push['type'] == 'sms_changed':
                src_id = push[u'source_device_iden']
                trds = self.request_threads(src_id)
                for trd in trds:
                    cid = trd[u'id']
                    if 'latest' not in trd:
                        continue
                    if trd[u'latest']['direction'] != 'incoming':
                        continue
                    if cid in self.sms_trds[src_id]:
                        if (
                            trd['latest']['timestamp'] <= self.sms_trds[src_id][cid][0]
                            and trd['latest']['id'] <= self.sms_trds[src_id][cid][1]
                        ):
                            continue
                    self.sms_trds[src_id][cid] = [  # timestamp and id update
                        trd['latest']['timestamp'],
                        trd['latest']['id']
                    ]
                    dev = self.get_device(src_id)
                    rec = {}
                    try:
                        trd_recs = trd['recipients']
                        if len(trd_recs) == 1:
                            suffix = "ReplyAllowingMirror"
                            rec = trd_recs[0]
                            name = rec['name']
                            icon = self.urlretrieve(rec['image_url']) if 'image_url' in rec else None
                        else:
                            suffix = "Mirror"
                            icon = None
                            name = ", ".join([i['name'] for i in trd_recs])
                        self.TriggerEvent(
                            "%s.%s" % (
                                suffix,
                                name.replace(" ", "").replace(".", ":")
                            ),
                            payload=[
                                trd['latest']['body'],
                                dev,
                                icon,
                                trd if self.complPush else trd['latest']
                            ]
                        )
                        if self.enabMirr:
                            push_dict = deepcopy(trd['latest'])
                            push_dict['dev'] = dev
                            push_dict['recip'] = rec['number'] if len(trd_recs) == 1 else "MULTI"
                            notification_id = 0
                            push_dict['notification_id'] = notification_id
                            push_dict['conversation_iden'] = cid
                            if notification_id in self.notification_ids:
                                win = self.notification_ids[notification_id]
                                win.Close()
                            body = trd['latest']['body']
                            wx.CallAfter(
                                MirrorNote,
                                None,
                                self,
                                dev,
                                name,
                                body if body else " ",
                                icon,
                                "sms",
                                self.get_sound('mirror'),
                                push_dict
                            )
                    except ValueError:
                        eg.PrintTraceback()
            else:
                eg.PrintNotice(Text.unknStream % push['type'])
        elif m['type'] == 'tickle' and m['subtype'] == 'push':
            self.request_pushes()
        elif m['type'] == 'tickle' and m['subtype'] == 'device':
            self.devices = []
            fcs = [i[2][0] for i in eg.scheduler.__dict__['heap'] if isinstance(i[2], tuple)]
            if self.update_devices not in fcs:
                if self.flag1:
                    self.flag2 = True
                else:
                    self.updt_dvcs = eg.scheduler.AddTask(5.0, self.update_devices)
        elif m['type'] == 'tickle' and m['subtype'] == 'contact':
            self.friends = []
            fcs = [i[2][0] for i in eg.scheduler.__dict__['heap'] if isinstance(i[2], tuple)]
            if self.update_devices not in fcs:
                if self.flag1:
                    self.flag2 = True
                else:
                    self.updt_dvcs = eg.scheduler.AddTask(5.0, self.update_devices)
        elif m['type'] == 'tickle' and m['subtype'] == 'channel':
            self.channels = []
            fcs = [i[2][0] for i in eg.scheduler.__dict__['heap'] if isinstance(i[2], tuple)]
            if self.update_devices not in fcs:
                if self.flag1:
                    self.flag2 = True
                else:
                    self.updt_dvcs = eg.scheduler.AddTask(5.0, self.update_devices)

    def do_trigger_event(self, part1, part2, part3, part4, part5, dev, ts):
        if self.mode:
            self.TriggerEvent(
                part1,
                payload=[part2, part3, part4, part5, dev, ts]
            )
        else:
            self.TriggerEvent(
                "%s.%s" % (part1, part2.title().replace(" ", "").replace(".", ":")),
                payload=[part3, part4, part5, dev, ts]
            )

    def urlretrieve(self, remote, flpth=None):
        headers = {}

        def header_function(header_line):
            if ':' not in header_line:
                return
            name, value = header_line.split(':', 1)
            name = name.strip()
            value = value.strip()
            name = name.lower()
            headers[name] = value

        buff = StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.URL, remote)
        curl.setopt(pycurl.HTTPHEADER, ['Accept: */*', 'User-Agent: EventGhost'])
        curl.setopt(pycurl.WRITEDATA, buff)
        curl.setopt(pycurl.HEADERFUNCTION, header_function)
        if self.proxy[0]:
            curl.setopt(pycurl.PROXY, str(self.proxy[0]))
            curl.setopt(pycurl.PROXYPORT, self.proxy[1])
            if self.proxy[2]:
                curl.setopt(
                    pycurl.PROXYUSERPWD,
                    "%s:%s" % (str(self.proxy[2]), str(self.proxy[3].Get()))
                )
        curl.perform()
        status_code = curl.getinfo(pycurl.RESPONSE_CODE)
        curl.close()
        if status_code == 200:
            if flpth is not None:
                ct = headers['content-type']
                fo = open(flpth, 'wb')
                buff.seek(0)
                # noinspection PyTypeChecker
                copyfileobj(buff, fo)
                fo.close()
                self.TriggerEvent("FileDownloaded", payload=flpth)
                if self.auto_open and ct.split(r"/")[0] == u'image':
                    eg.plugins.System.DisplayImage(
                        flpth, 3, 1, True, False, 0, True, 4,
                        self.p_hide,
                        0, 5, 5, 640, 480, (51, 51, 51), False, True, True, u''
                    )
            else:
                return b64encode(buff.getvalue())
        else:
            self.log(self.text.dwnldFailed % (flpth, status_code), 1)

    def get_sound(self, tp):
        if self.wavs:
            if isfile(join(self.wavs, "%s.wav" % tp)):
                return join(self.wavs, "%s.wav" % tp)

    def delete_push(self, iden):
        res, flag = self.request("DELETE", API + 'pushes/%s' % iden)
        if flag:
            self.log(self.text.pushDelted, 4)
        else:
            self.log(self.text.pushDelFld % res, 2)

    def send_reply(self, push, msg):
        if 'type' in push and push['type'] == 'sms':
            return self.send_sms(push['dev'], push['recip'], msg)
        push['type'] = 'messaging_extension_reply'
        push['target_device_iden'] = push['source_device_iden']
        push['message'] = msg
        package_name = push['package_name']
        if 'source_device_iden' in push:
            del push['source_device_iden']
        if 'dismissible' in push:
            del push['dismissible']
        if 'notification_id' in push:
            del push['notification_id']
        if 'notification_tag' in push:
            del push['notification_tag']
        push = push if self.key is None else \
            {
                'encrypted': True,
                'ciphertext': gcm_encrypt(self.key, dumps(push))
            }
        body = {'type': 'push', 'push': push}
        res, flag = self.request("POST", API + 'ephemerals', data=body)
        if flag:
            self.log(self.text.forwRep % package_name, 4)
        else:
            self.log(self.text.forwRepFld % package_name, 2)

    def sms_dismiss(self):
        dismissal = {
            'type': 'dismissal',
            'source_user_iden': self.source_user_iden,
            'package_name': 'sms',
            'notification_id': 0
        }
        body = {
            'type': 'push',
            'push': dismissal,
            'targets': ['stream', 'android']
        }
        res, flag = self.request("POST", API + 'ephemerals', data=body)
        if flag:
            self.log(self.text.dismissSms, 4)
        else:
            self.log(self.text.dismissSmsFld, 2)

    def dismiss(self, oldpush):
        if isinstance(oldpush, dict):
            if 'notification_id' not in oldpush:
                self.log(self.text.notIdMissing, 2)
                return
            notification_id = oldpush['notification_id']
            push = {
                'notification_id': notification_id,
                'notification_tag': None if 'notification_tag' not in oldpush else oldpush['notification_tag'],
                'type': u'dismissal',
                'source_user_iden': self.source_user_iden,
                'package_name': oldpush['package_name']
            }
            push = push if self.key is None else \
                {
                    'encrypted': True,
                    'ciphertext': gcm_encrypt(self.key, dumps(push))
                }
            body = {
                'type': 'push',
                'push': push,
                'targets': [u'stream', u'android', u'ios']
            }
            res, flag = self.request("POST", API + 'ephemerals', data=body)
            if flag:
                self.log(self.text.dismissNote % notification_id, 4)
            else:
                self.log(self.text.dismissNoteFld % notification_id, 2)
        else:
            body = {"dismissed": True}
            res, flag = self.request("POST", API + 'pushes/%s' % oldpush, data=body)
            if flag:
                self.log(self.text.dismissPush % oldpush, 4)
            else:
                self.log(self.text.dismissPushFld % oldpush, 2)

    def process_mirror(self, push):
        body = push[u'body'] if 'body' in push and push['body'] else ""
        title = push['title'] if 'title' in push and push['title'] else ""
        dev = self.get_device(push['source_device_iden']) \
            if 'source_device_iden' in push else "Unknown"
        push_dict = {
            'package_name': push['package_name'] if 'package_name' in push else None,
            'source_user_iden': push['source_user_iden'] if 'source_user_iden' in push else None,
            'source_device_iden': push['source_device_iden'] if 'source_device_iden' in push else None,
            'dismissible': push['dismissible'] if 'dismissible' in push else None,
            'notification_id': push['notification_id'] if 'notification_id' in push else None,
            'notification_tag': push['notification_tag'] if 'notification_tag' in push else None
        }
        try:
            if "conversation_iden" in push:
                push_dict["conversation_iden"] = push['conversation_iden']
                suffix = "ReplyAllowingMirror"
            else:
                suffix = "Mirror"
            self.TriggerEvent(
                "%s.%s" % (
                    suffix,
                    title.title().replace(" ", "").replace(".", ":") if title else suffix,
                ),
                payload=[
                    body,
                    dev,
                    push[u'icon'],
                    push if self.complPush else push_dict
                ]
            )
            if self.enabMirr:
                title = title if title else body
                notification_id = push_dict['notification_id']
                if notification_id in self.notification_ids:
                    win = self.notification_ids[notification_id]
                    win.Close()
                wx.CallAfter(
                    MirrorNote,
                    None,
                    self,
                    dev,
                    title,
                    body if body and body != title else "",
                    push[u'icon'],
                    push['application_name'] if 'application_name'
                    in push and push['application_name'] else "",
                    self.get_sound(push['type']),
                    push_dict
                )
        except ValueError:
            eg.PrintTraceback()

    def process_push(self, push):
        dev = None
        if (
            ('active' in push and not push['active'])
            or 'dismissed' in push and push['dismissed']
        ):
            return
        if (
            'target_device_iden' in push
            and push['target_device_iden'] != self.iden
        ):
            return
        friend = False
        if 'receiver_email' in push:
            if push['receiver_email'] != self.email:
                return
            elif 'sender_email' in push and push['sender_email'] != self.email:
                friend = True
                dev = self.get_device(push['sender_email'])
        if not friend:
            dev = self.get_device(push['source_device_iden']) \
                if 'source_device_iden' in push else push['sender_name']
        if 'modified' in push:
            ts = push['modified']
            if ts > self.modified_after:
                self.modified_after = ts
                self.log(self.text.mdfdUpd % self.modified_after, 4)
        else:
            ts = ttime()
        ts = str(datetime.fromtimestamp(ts))[:19]
        wav = self.get_sound(push['type'])
        if wav:
            sound = wx.adv.Sound(wav)
            if sound.IsOk():
                sound.Play(wx.adv.SOUND_ASYNC)
        body = push[u'body'] if ('body' in push and push['body']) else ""
        part1 = push['type'].capitalize()
        part2 = push['title'] if ('title' in push and push['title']) else part1
        if self.firstWord and part1 == "Note" and part2 == 'Note':
            tmp_body = body.strip(' \t\n\r').replace("\n", " ")
            part2 = tmp_body.split(" ")[0].replace(",", "") if tmp_body else part1
        part3 = None
        part4 = None
        part5 = push[u'iden'] if 'iden' in push else None
        if push['type'] == u'link':
            if 'url' in push:
                part3 = push[u'url']
                part4 = body
            else:
                part3 = body
        elif push['type'] == u'note':
            part3 = body
        elif push['type'] == 'clip':
            part3 = body
            part2 = dev if dev else part2
        if push['type'] in (u'link', u'note', u'clip'):
            self.do_trigger_event(part1, part2, part3, part4, part5, dev, ts)
        elif push['type'] == u'file':
            image = push[u'file_type'].split(r"/")[0] == u'image'
            self.TriggerEvent(
                "Image" if image else "File",
                payload=[
                    push[u'file_name'],
                    push[u'file_type'],
                    push[u'file_url'],
                    body,
                    dev,
                    ts
                ]
            )
            flpth = join(self.fldr, push[u'file_name'])
            self.urlretrieve(push[u'file_url'], flpth=flpth)

    def disable_mirroring(self, pushDict, app):
        push = {
            'type': 'mute',
            'source_user_iden': pushDict['source_user_iden'],
            "source_device_iden": self.iden,
            'package_name': pushDict['package_name']
        }
        push = push if self.key is None else \
            {
                'encrypted': True,
                'ciphertext': gcm_encrypt(self.key, dumps(push))
            }
        res, flag = self.request(
            "POST",
            API + 'ephemerals',
            data={"type": "push", "push": push}
        )
        self.log(self.text.rspnsr % repr(res), 4)
        if not flag:
            self.log(self.text.fTriggMute % app, 1)
            return
        self.log(self.text.triggMute % app, 3)
        self.update_config(disabled=(
            {'source_user_iden': pushDict['source_user_iden'],
             'package_name': pushDict['package_name']},
            app
        ))

    def enable_mirroring(self, push, app):
        push['type'] = 'unmute'
        push['source_device_iden'] = self.iden
        push = push if self.key is None else \
            {
                'encrypted': True,
                'ciphertext': gcm_encrypt(self.key, dumps(push))
            }
        res, flag = self.request(
            "POST",
            API + 'ephemerals',
            data={"type": "push", "push": push}
        )
        self.log(self.text.rspnsr % repr(res), 4)
        if not flag:
            self.log(self.text.fTriggUnmute % app, 1)
            return
        self.log(self.text.triggUnmute % app, 3)

    def enable_mirroring_many(self, lst):
        for item in lst:
            self.enable_mirroring(*item)
        self.update_config(enabled=lst)

    @staticmethod
    def enable_disable_popups_tsk(trItem, args):
        eg.actionThread.Func(trItem.SetArguments)(args)  # __stop__ / __start__
        eg.document.SetIsDirty()
        eg.document.Save()

    def enable_disable_popups(self, pic, mirr, save):
        if not self.info.isStarted:
            return
        if pic == 2 and mirr == 2:
            return
        if (2 > pic == self.auto_open) or pic == 3:
            self.auto_open = not self.auto_open
        if (2 > mirr == self.enabMirr) or mirr == 3:
            self.enab_mirr = not self.enab_mirr
        if save:
            flag = False
            tr_item = self.info.treeItem
            args = list(tr_item.GetArguments())
            if args[12] != self.auto_open:
                flag = True
                args[12] = self.auto_open
            if args[14] != self.enabMirr:
                flag = True
                args[14] = self.enabMirr
            if flag:
                self.auto_update = True
                ct = currentThread()
                # noinspection PyProtectedMember
                if ct == eg.actionThread._ThreadWorker__thread:
                    tr_item.SetArguments(args)  # automatically __stop__/__start__
                    eg.document.SetIsDirty()
                    eg.document.Save()
                else:
                    eg.scheduler.AddTask(
                        0.01,
                        self.enable_disable_popups_tsk,
                        tr_item,
                        args
                    )

    def get_device(self, iden):
        tmp = [t[1] for t in self.targets]
        if iden in tmp:
            return [t[0] for t in self.targets][tmp.index(iden)]
        else:
            return iden

    def get_targets(self, nick):
        tmp = [list(item) for item in self.targets if item[0] == nick]
        for item in tmp:
            item.append(True)
        return tmp

    def get_single(self, pbid):
        if pbid in [itm[1] for itm in self.targets]:
            return [itm for itm in self.targets if itm[1] == pbid]
        if pbid in [itm[0] for itm in self.targets]:
            return [itm for itm in self.targets if itm[0] == pbid]
        elif pbid in [itm['tag'] for itm in self.channels if itm['active']]:
            return [
                [itm['name'], itm['tag'], 'channel'] for
                itm in self.channels if itm['active'] and itm['tag'] == pbid]

    def request_pushes(self):
        self.log(self.text.gettPshs % self.modified_after, 4)
        res, flag = self.request(
            "GET", API + 'pushes?modified_after=%.7f&active=true' % self.modified_after
        )
        self.log(self.text.rspnsr % repr(res), 4)
        if not flag or not isinstance(res, dict) or 'pushes' not in res:
            self.log(self.text.fLoadPshs, 1)
            return
        pushes = res['pushes']
        for push in pushes:
            try:
                self.process_push(push)
            except ValueError:
                eg.PrintTraceback()

    def upload_file(self, filepath):

        def guess_type(file_path):
            return mimetype(file_path)[0] or 'application/octet-stream'

        base_name = basename(filepath)
        params = {
            "file_name": base_name.encode("utf-8"),
            "file_type": guess_type(base_name)
        }
        resp, flag = self.request(
            "GET",
            API + "upload-request",
            params=params
        )
        if flag:
            if not isfile(filepath.encode("utf-8")):
                tmpfile = mktemp(".tmp", prefix='_eg_')
                sh_copy(filepath, tmpfile)
            else:
                tmpfile = None
            local_file = tmpfile if tmpfile is not None else filepath
            data = [("file", (pycurl.FORM_FILE, local_file.encode("utf-8")))]
            c = pycurl.Curl()
            c.setopt(pycurl.CAINFO, certifi.where())
            c.setopt(pycurl.URL, resp["upload_url"])
            c.setopt(pycurl.POST, 1)
            c.setopt(pycurl.HTTPPOST, data)
            if self.proxy[0]:
                c.setopt(pycurl.PROXY, str(self.proxy[0]))
                c.setopt(pycurl.PROXYPORT, self.proxy[1])
                if self.proxy[2]:
                    c.setopt(
                        pycurl.PROXYUSERPWD,
                        "%s:%s" % (str(self.proxy[2]), str(self.proxy[3].Get()))
                    )
            c.perform()
            response_code = c.getinfo(pycurl.RESPONSE_CODE)
            c.close()
            if tmpfile is not None:
                os.remove(tmpfile)
            if response_code == 204:
                return resp["file_name"], resp["file_type"], resp["file_url"]

    def request(self, method, url, **kwargs):
        hdrs = [
            "X-User-Agent:EventGhost",
            "Authorization:Basic " + b64encode(self.api_key + ":"),
            'Accept:application/json',
            "Content-type:application/json",
        ] if 'headers' not in kwargs else kwargs['headers']

        curl = pycurl.Curl()
        curl.setopt(pycurl.CAINFO, certifi.where())
        if 'params' in kwargs:
            url = url + '?' + urlencode(kwargs['params'])
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.HTTPHEADER, hdrs)
        if method == "POST":
            post_data = kwargs['data'] if 'data' in kwargs else {}
            postfields = dumps(post_data)
            curl.setopt(pycurl.POST, 1)
            curl.setopt(pycurl.POSTFIELDS, postfields)
        elif method == 'DELETE':  # rv = self.app.delete('/subscription?uuid=%s&service=%s' % (self.uuid, public))
            curl.setopt(pycurl.CUSTOMREQUEST, "DELETE")
        buf = StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        if self.proxy[0]:
            curl.setopt(pycurl.PROXY, str(self.proxy[0]))
            curl.setopt(pycurl.PROXYPORT, self.proxy[1])
            if self.proxy[2]:
                curl.setopt(
                    pycurl.PROXYUSERPWD,
                    "%s:%s" % (str(self.proxy[2]), str(self.proxy[3].Get()))
                )
        curl.perform()
        status_code = curl.getinfo(pycurl.RESPONSE_CODE)
        curl.close()
        resp = buf.getvalue()
        if status_code == 200:
            if method == "DELETE":
                return resp, True
            else:
                return loads(resp), True
        else:
            eg.PrintError(self.text.reqErr % str(resp))
            return status_code, False

    def update_config(self, iden=None, disabled=None, enabled=None):
        tr_item = self.info.treeItem
        args = list(tr_item.GetArguments())
        if iden:
            args[2] = iden
            self.log(self.text.idenSaved % iden, 2)
            self.iden = args[2]
        elif disabled and disabled not in args[9]:
            args[9].append(disabled)
            self.log(self.text.dsbldUpdated, 2)
            self.disabled = deepcopy(args[9])
        elif enabled:
            for item in enabled:
                del item[0]['type']
                del item[0]['source_device_iden']
                if item in args[9]:
                    args[9].remove(item)
            self.log(self.text.dsbldUpdated, 2)
            self.disabled = deepcopy(args[9])
        self.auto_update = True
        eg.actionThread.Func(tr_item.SetArguments)(args)
        eg.document.SetIsDirty()
        eg.document.Save()

    def get_account(self):
        account, flag = self.request("GET", API + 'users/me')
        if flag and isinstance(account, dict) and "email" in account:
            self.email = account["email"]
            self.source_user_iden = account["iden"]
            self.log(self.text.emlObtained, 4)
        else:
            self.log(self.text.accReqFailed, 1)

    def get_sm_sdevices(self):
        sms_devs = {}
        for dev in self.devices:
            if 'has_sms' in dev and dev['has_sms'] and dev['active']:
                sms_devs[dev['nickname']] = dev['iden']
        return sms_devs

    def get_phonebook(self, dev):
        sms_devs = self.get_sm_sdevices()
        if dev in list(sms_devs.iterkeys()):
            ph_book, flag = self.request(
                'GET',
                API + 'permanents/phonebook_' + sms_devs[dev])
            if flag:
                if 'encrypted' in ph_book and ph_book['encrypted']:
                    if self.key:
                        decrypted = gcm_decrypt(self.key, ph_book['ciphertext'])
                        try:
                            ph_book = loads(decrypted)
                            if not isinstance(ph_book, dict):
                                self.log(self.text.e2eMssg2, 2)
                                return []
                        except ValueError:
                            self.log(self.text.e2eMssg3, 2)
                            return []
                    else:
                        eg.PrintNotice(self.text.noKey)
                        return []
                self.log(self.text.bookRcvd % dev, 4)
                phbook = ph_book['phonebook']
                choices = []
                for item in phbook:
                    choices.append(item['name'] + SEP + item['phone'])
                # noinspection PyTypeChecker
                choices.sort(cmp=strcoll)
                return choices
            else:
                self.log(self.text.bookReqFailed % dev, 2)
        return []

    def send_sms(self, dev, recip, msg):
        sms_devs = self.get_sm_sdevices()
        if dev in list(sms_devs.iterkeys()):
            iden = sms_devs[dev]
            recip = recip.strip() if SEP not in recip else \
                recip.split(SEP)[1].strip()
            push = {
                "type": "messaging_extension_reply",
                "package_name": "com.pushbullet.android",
                "source_user_iden": self.source_user_iden,
                "target_device_iden": iden,
                "source_device_iden": self.iden,
                "conversation_iden": recip,
                "message": msg,
            }
            push = push if self.key is None else \
                {
                    'encrypted': True,
                    'ciphertext': gcm_encrypt(self.key, dumps(push))
                }
            res, flag = self.request(
                "POST",
                API + 'ephemerals',
                data={"type": "push", "push": push}
            )

            if flag:
                self.log(self.text.smsSent % dev, 4)
            else:
                self.log(self.text.smsSentF % dev, 2)

    def send_sm_smulti(self, recips, msg, dev=None):
        if dev is not None:
            for recip in recips:
                self.send_sms(dev, recip, msg)
        else:
            for recip in recips:
                self.send_sms(recip[0], recip[2], msg)

    def update_devices(self):
        if self.flag1:
            return
        fcs = [i[2][0] for i in eg.scheduler.__dict__['heap'] if isinstance(i[2], tuple)]
        if self.update_devices in fcs:
            try:
                eg.scheduler.CancelTask(self.updt_dvcs)
                return
            except ValueError:
                pass
        if not self.info.isStarted:
            return
        if not self.connectivity():
            self.stop_watchdog()
            self.watchdog = eg.scheduler.AddTask(5.0, self.watcher)
            return
        if not self.api_key:
            self.log(self.text.noApi, 1)
            return
        if not self.nickname:
            self.log(self.text.noNick, 1)
            return
        self.flag1 = True
        self.flag2 = False

        if not self.email:
            self.get_account()

        pssd = self.pssd.Get() if isinstance(self.pssd, eg.Password) else None
        if self.key is None and pssd and self.source_user_iden:
            self.key = PBKDF2(
                pssd,
                self.source_user_iden,
                30000,
                digestmodule=SHA256,
                macmodule=HMAC
            ).read(32)

        if not self.devices:
            devices, flag = self.request("GET", API + "devices?active=true")
            if flag and isinstance(devices, dict) and "devices" in devices:
                self.devices = devices["devices"]
                self.log(self.text.devRcvd % repr(self.devices), 3)

                self.flag_dev = True

                for dev in self.devices:
                    if not dev['active']:  # ignore deleted device
                        continue
                    if 'nickname' not in dev or not dev['nickname']:
                        nick = dev['manufacturer'].capitalize() + ' ' + dev['model']
                        dev['nickname'] = nick
                nicknames = dict(
                    [
                        (dev['nickname'], dev) for dev
                        in self.devices if dev['active']
                    ]
                )
                key_fingerprint = get_key_fingerprint(self.key)
                BODY['key_fingerprint'] = key_fingerprint
                if self.nickname in nicknames.iterkeys():
                    dev = nicknames[self.nickname]
                    if dev['manufacturer'] == u'EventGhost':
                        if self.iden != dev['iden']:
                            self.iden = dev['iden']
                            self.update_config(iden=self.iden)
                    else:
                        eg.PrintNotice(self.text.nicknameUsed % self.nickname)
                        if self.flag2:
                            self.updt_dvcs = eg.scheduler.AddTask(5.0, self.update_devices)
                            self.flag2 = False
                        self.flag1 = False
                        return
                    if self.key:
                        if 'key_fingerprint' not in dev or key_fingerprint != dev['key_fingerprint']:
                            self.request("POST", API + 'devices/%s' % self.iden, data=BODY)
                else:
                    BODY['nickname'] = self.nickname
                    me, flag = self.request("POST", API + 'devices', data=BODY)
                    self.log(self.text.pcMssng, 2)
                    if flag and isinstance(me, dict) and me:
                        self.log(self.text.devCrtd % repr(me), 3)
                        self.iden = me['iden']
                        self.update_config(iden=self.iden)
                        if self.flag2:
                            self.updt_dvcs = eg.scheduler.AddTask(5.0, self.update_devices)
                            self.flag2 = False
                        self.flag1 = False
                        return
                    else:
                        self.log(self.text.crDevFld, 1)
                        self.flag1 = False
                        if self.flag2:
                            self.updt_dvcs = eg.scheduler.AddTask(5.0, self.update_devices)
                            self.flag2 = False
                        return
            else:
                self.log(self.text.devReqFailed, 1)
                self.flag1 = False
                self.updt_dvcs = eg.scheduler.AddTask(5.0, self.update_devices)
                self.flag2 = False
                return
        if not self.friends:
            friends, flag = self.request("GET", API + "contacts?active=true")
            if flag and isinstance(friends, dict) and "contacts" in friends:
                self.friends = friends["contacts"]
                self.log(self.text.frndsRcvd % repr(self.friends), 3)
        if not self.channels:
            channels, flag = self.request("GET", API + "channels")
            if flag and isinstance(channels, dict) and "channels" in channels:
                self.channels = channels["channels"]
                self.log(self.text.chnnlsRcvd % repr(self.channels), 3)
        self.targets = []
        for dev in self.devices:
            if not dev['active']:
                continue
            droid = 'android' if 'android_version' in dev \
                                 and dev['android_version'] is not None else 'pc'
            self.targets.append((dev['nickname'], dev['iden'], droid))
            if 'has_sms' in dev and dev['has_sms']:
                trds = self.request_threads(dev['iden'])
                if trds:
                    self.sms_trds[dev['iden']] = dict(
                        [
                            (
                                i[u'id'],
                                [
                                    i[u'latest'][u'timestamp'],
                                    i[u'latest'][u'id']
                                ]
                            ) for i in trds if 'latest' in i and i[u'latest'][u'direction'] == u'incoming'
                        ]
                    )

        for fr in self.friends:
            if not fr['active'] or fr['status'] == 'not_user':
                continue
            name = fr['name'] if 'name' in fr and fr['name'] else fr['email']
            self.targets.append((name, fr['email'], 'user'))
        for ch in self.channels:
            if not ch['active']:
                continue
            name = ch['name']
            self.targets.append((name, ch['tag'], 'channel'))
        self.log(self.text.trgtsDrvd % repr(self.targets), 3)
        self.establish_subscriber()
        self.flag1 = False
        if self.flag2:
            self.updt_dvcs = eg.scheduler.AddTask(5.0, self.update_devices)
            self.flag2 = False

    def push(self, kind, trgts, data, suff=None):
        if not self.ws_c:
            eg.actionThread.Call(eg.PrintNotice, self.text.waiting2)
            return
        kinds = [i.lower() for i in self.text.kinds]
        payload = {'type': kinds[kind]}
        results = []
        ok = True
        if kind == 2:  # file
            payload['body'] = data[0] if data[0] else None
            fl = data[1]
            file_info = self.upload_file(fl)
            if not file_info:
                eg.actionThread.Call(
                    self.log,
                    self.text.uplFld % basename(fl),
                    1
                )
                return
            eg.actionThread.Call(
                self.log,
                self.text.uplSucc % basename(fl),
                4
            )
            payload["file_name"] = file_info[0]
            payload["file_type"] = file_info[1]
            payload["file_url"] = file_info[2]
            for trgt in trgts:
                if not trgt[3]:
                    continue
                dev = trgt[0]
                # check, if trgt is valid ?
                tmp = {'nickname': dev}
                if trgt[2] == 'user':
                    iden = 'email'
                    tmp['type'] = 'friend'
                    if 'device_iden' in payload:
                        del payload['device_iden']
                    if 'channel_tag' in payload:
                        del payload['channel_tag']
                elif trgt[2] == 'channel':
                    iden = 'channel_tag'
                    tmp['type'] = 'channel'
                    if 'device_iden' in payload:
                        del payload['device_iden']
                    if 'email' in payload:
                        del payload['email']
                else:
                    iden = 'device_iden'
                    tmp['type'] = 'device'
                    if 'channel_tag' in payload:
                        del payload['channel_tag']
                    if 'email' in payload:
                        del payload['email']
                tmp[iden] = trgt[1]
                payload[iden] = trgt[1]
                res, flag = self.request("POST", API + "pushes", data=payload)
                if flag:
                    tmp['push_iden'] = res['iden']
                else:
                    ok = False
                tmp['ok'] = flag
                results.append(tmp)
            level = 4 if ok else 1
            eg.actionThread.Call(
                self.log,
                self.text.pushRslt % repr(results),
                level
            )
            if suff:
                self.TriggerEvent("PushSent.%s" % suff, payload=results)
            return

        else:  # if kind in (0, 1, 3):
            payload['title'] = data[0]
        if kind in (0, 3):
            payload['body'] = data[1]
        elif kind == 1:
            payload['url'] = data[1]
            payload['body'] = data[2] if data[2] else None
        payload[u'source_device_iden'] = self.iden
        for trgt in trgts:
            if not trgt[3]:
                continue
            dev = trgt[0]
            tmp = {'nickname': dev}
            if trgt[2] == 'user':
                iden = 'email'
                tmp['type'] = 'friend'
                if 'device_iden' in payload:
                    del payload['device_iden']
                if 'channel_tag' in payload:
                    del payload['channel_tag']
            elif trgt[2] == 'channel':
                iden = 'channel_tag'
                tmp['type'] = 'channel'
                if 'device_iden' in payload:
                    del payload['device_iden']
                if 'email' in payload:
                    del payload['email']
            else:
                iden = 'device_iden'
                tmp['type'] = 'device'
                if 'email' in payload:
                    del payload['email']
                if 'channel_tag' in payload:
                    del payload['channel_tag']
            tmp[iden] = trgt[1]
            payload[iden] = trgt[1]
            # check, if trgt is valid ?
            if kind != 3:
                res, flag = self.request("POST", API + "pushes", data=payload)
            else:  # mirror
                payload['icon'] = get_icon(self.text.err, data[2])
                payload[u'application_name'] = eg.event.prefix if \
                    eg.event else 'EventGhost'

                payload = payload if self.key is None else \
                    {
                        'encrypted': True,
                        'ciphertext': gcm_encrypt(self.key, dumps(payload))
                    }

                res, flag = self.request(
                    "POST",
                    API + "ephemerals",
                    data={
                        "type": "push",
                        "push": payload,
                        'targets': ['stream', 'android']
                    }
                )
            if flag:
                if 'iden' in res:
                    tmp['push_iden'] = res['iden']
            else:
                ok = False
            tmp['ok'] = flag
            results.append(tmp)
        level = 4 if ok else 1
        eg.actionThread.Call(self.log, self.text.pushRslt % repr(results), level)
        if suff:
            self.TriggerEvent("PushSent.%s" % suff, payload=results)
        return

    def get_active_devices(self):
        act_devs = {}
        for device in self.devices:
            if device['active']:
                act_devs[device['iden']] = device['nickname']
        return act_devs

    def Configure(
        self,
        nickname=None,
        api_key="",
        iden="",
        prefix="PushBullet",
        mode=0,
        fldr="",
        debug=3,
        hide=15,
        p_hide=15,
        disabled=None,
        hide_btn=False,
        wavs="",
        auto_open=True,
        dummy="",
        enab_mirr=True,
        clr=(255, 255, 255),
        alignment=0,
        dspl=0,
        offset=(0, 0),
        filtered=None,
        push_groups=None,
        sms_groups=None,
        password="",
        first_word=True,
        compl_push=False,
        proxy=None
    ):
        if proxy is None:
            proxy = ["", 0, "", ""]
        if sms_groups is None:
            sms_groups = []
        if push_groups is None:
            push_groups = []
        if filtered is None:
            filtered = []
        if disabled is None:
            disabled = []
        self.disabled = []
        for item in disabled:  # backward compatibility
            self.disabled.append(item if len(item) == 2 else item[1:])

        if nickname is None:
            nickname = "EG-%s" % gethostname()
        if not isinstance(api_key, eg.Password):
            api_key = eg.Password(None)
            api_key.Set("")  # api_key.Set(apiKey)
        else:
            api_key = api_key
        if not isinstance(password, eg.Password):
            passw = eg.Password(None)
            passw.Set(password)
        else:
            passw = password
        if not isinstance(proxy[3], eg.Password):
            p = eg.Password(None)
            p.Set("")
            proxy[3] = p
        text = self.text
        panel = eg.ConfigPanel(self)
        panel.push_groups = deepcopy(push_groups)
        panel.sms_groups = deepcopy(sms_groups)
        panel.proxy = deepcopy(proxy)
        if not fldr:
            fldr = eg.folderPath.TemporaryFiles
        n_label = wx.StaticText(panel, -1, text.nLabel)
        nick_ctrl = wx.TextCtrl(panel, -1, nickname)
        api_label = wx.StaticText(panel, -1, text.apiLabel)
        passw_label = wx.StaticText(panel, -1, text.password)
        api_ctrl = wx.TextCtrl(panel, -1, api_key.Get(), style=wx.TE_PASSWORD)
        passw_ctrl = wx.TextCtrl(panel, -1, passw.Get(), style=wx.TE_PASSWORD)
        prefix_label = wx.StaticText(panel, -1, text.prefix)
        prefix_ctrl = panel.TextCtrl(prefix)
        mode_label = wx.StaticText(panel, -1, text.mode)
        rb0 = panel.RadioButton(mode == 0, self.text.modes[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(mode == 1, self.text.modes[1])
        fldr_label = wx.StaticText(panel, -1, text.folder)
        fldr_ctrl = panel.DirBrowseButton(fldr)
        wav_label = wx.StaticText(panel, -1, text.wavs)
        wav_ctrl = eg.DirBrowseButton(
            panel,
            -1,
            toolTip=self.text.toolWav,
            dialogTitle=self.text.wavFldr,
            buttonText=eg.text.General.browse,
            startDirectory=join(
                abspath(dirname(__file__.decode('mbcs'))),
                "sounds"
            ),
        )
        wav_ctrl.SetValue(wavs)
        debug_label = wx.StaticText(panel, -1, text.debug)
        debug_label2 = wx.StaticText(panel, -1, text.debug2)
        debug_ctrl = eg.SpinIntCtrl(
            panel,
            -1,
            debug,
            min=1,
            max=5
        )
        button = wx.Button(panel, -1, self.text.reenab)
        hide_btn_ctrl = wx.CheckBox(panel, 0, self.text.hideBtn)
        hide_btn_ctrl.SetValue(hide_btn)
        hide_label = wx.StaticText(panel, -1, text.timeout)
        hide_label2 = wx.StaticText(panel, -1, text.timeout2)
        hide_ctrl = eg.SpinIntCtrl(
            panel,
            -1,
            hide,
            min=0,
            max=999
        )
        auto_open_ctrl = panel.CheckBox(auto_open, self.text.autoOpen)
        first_word_ctrl = panel.CheckBox(first_word, self.text.firstWord)
        compl_push_ctrl = panel.CheckBox(compl_push, self.text.complPush)
        enab_mirr_ctrl = panel.CheckBox(enab_mirr, self.text.enabMirr)
        p_hide_label = wx.StaticText(panel, -1, text.pTimeout)
        p_hide_label2 = wx.StaticText(panel, -1, text.timeout2)
        p_hide_ctrl = eg.SpinIntCtrl(
            panel,
            -1,
            p_hide,
            min=0,
            max=999
        )
        clip_filter_ctrl = CheckListComboBox(
            panel,
            -1,
            values=[[], [], []],
            helpText=text.clipFilter
        )
        if self.devices:
            act_devs = self.get_active_devices()
            items = list(self.get_active_devices().iterkeys())
            values = [
                [act_devs[item] for item in items],
                [item in filtered for item in items],
                act_devs
            ]

            def sort_lst(lst):
                tmp = zip(lst[0], lst[1], lst[2])
                tmp.sort()
                return [
                    [itm[0] for itm in tmp],
                    [itm[1] for itm in tmp],
                    [itm[2] for itm in tmp]
                ]

            clip_filter_ctrl.SetValue(sort_lst(values))
        else:
            clip_filter_ctrl.Enable(False)
        clip_filter_ctrl.SetToolTip(text.filterToolTip)
        clr_label = wx.StaticText(panel, -1, text.bcgColour)
        alg_label = wx.StaticText(panel, -1, text.alignment)
        dsp_label = wx.StaticText(panel, -1, text.display)
        x_of_label = wx.StaticText(panel, -1, text.xOffset)
        y_of_label = wx.StaticText(panel, -1, text.yOffset)

        clr_ctrl = panel.ColourSelectButton(clr)
        alg_ctrl = panel.Choice(
            alignment, choices=text.alignmentChoices
        )
        dsp_ctrl = eg.DisplayChoice(panel, dspl)
        x_of_ctrl = panel.SpinIntCtrl(offset[0], -32000, 32000)
        y_of_ctrl = panel.SpinIntCtrl(offset[1], -32000, 32000)

        p_hide_sizer = wx.BoxSizer(wx.HORIZONTAL)
        p_hide_sizer.Add(p_hide_ctrl, 0, wx.RIGHT, 5)
        p_hide_sizer.Add(p_hide_label2, 0, flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer = wx.GridBagSizer(10, 10)

        grid_sizer.Add(n_label, (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(nick_ctrl, (0, 1), flag=wx.EXPAND)
        grid_sizer.Add(api_label, (1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(api_ctrl, (1, 1), flag=wx.EXPAND)
        grid_sizer.Add(passw_label, (2, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(passw_ctrl, (2, 1), flag=wx.EXPAND)
        grid_sizer.Add(prefix_label, (3, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(prefix_ctrl, (3, 1), flag=wx.EXPAND)
        grid_sizer.AddGrowableCol(1)

        mode_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mode_sizer.Add(rb0)
        mode_sizer.Add(rb1, 0, wx.LEFT, 10)
        grid_sizer.Add(mode_label, (4, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(mode_sizer, (4, 1), flag=wx.EXPAND)
        grid_sizer.Add(fldr_label, (5, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(fldr_ctrl, (5, 1), flag=wx.EXPAND)
        debug_sizer = wx.BoxSizer(wx.HORIZONTAL)
        debug_sizer.Add(debug_ctrl, 0, wx.RIGHT, 5)
        debug_sizer.Add(debug_label2, 0, flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(debug_label, (6, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(debug_sizer, (6, 1))
        grid_sizer.Add(first_word_ctrl, (7, 0), (1, 2))
        grid_sizer.Add(auto_open_ctrl, (8, 0), (1, 2))
        grid_sizer.Add(p_hide_label, (9, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(p_hide_sizer, (9, 1))
        grid_sizer.Add(clip_filter_ctrl, (10, 0), (1, 2), flag=wx.EXPAND)
        grid_sizer.Add(wav_label, (11, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(wav_ctrl, (11, 1), flag=wx.EXPAND)

        m_sizer = wx.GridBagSizer(10, 5)
        m_sizer.Add(enab_mirr_ctrl, (0, 0), (1, 3))
        m_sizer.Add(clr_label, (1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(clr_ctrl, (1, 1), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(alg_label, (2, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(alg_ctrl, (2, 1), (1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(dsp_label, (3, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(dsp_ctrl, (3, 1), (1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(x_of_label, (4, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(x_of_ctrl, (4, 1), (1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(y_of_label, (5, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(y_of_ctrl, (5, 1), (1, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(hide_label, (6, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(hide_ctrl, (6, 1))
        m_sizer.Add(hide_label2, (6, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(hide_btn_ctrl, (7, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(compl_push_ctrl, (8, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        m_sizer.Add(button, (9, 0))
        m_sizer.AddGrowableCol(2)

        static_box = wx.StaticBox(panel, -1, label=text.mirroring)
        static_box_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
        static_box_sizer.Add(m_sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(grid_sizer, 0, wx.RIGHT | wx.EXPAND, 10)
        main_sizer.Add(static_box_sizer, 0, wx.EXPAND)
        panel.sizer.Add(main_sizer, 0, wx.EXPAND | wx.ALL, 10)

        def enable_hide_picture(enable):
            p_hide_label.Enable(enable)
            p_hide_ctrl.Enable(enable)
            p_hide_label2.Enable(enable)

        enable_hide_picture(auto_open)

        def on_auto_open(evt):
            enable_hide_picture(evt.Checked())
            evt.Skip()

        auto_open_ctrl.Bind(wx.EVT_CHECKBOX, on_auto_open)

        def disable_mirr_pop_up(disable):
            hide_label.Enable(disable)
            hide_ctrl.Enable(disable)
            hide_label2.Enable(disable)
            hide_btn_ctrl.Enable(disable)
            compl_push_ctrl.Enable(disable)
            button.Enable(disable)
            clr_label.Enable(disable)
            alg_label.Enable(disable)
            dsp_label.Enable(disable)
            x_of_label.Enable(disable)
            y_of_label.Enable(disable)
            clr_ctrl.Enable(disable)
            alg_ctrl.Enable(disable)
            dsp_ctrl.Enable(disable)
            x_of_ctrl.Enable(disable)
            y_of_ctrl.Enable(disable)

        disable_mirr_pop_up(enab_mirr)

        def on_dis_mirr(evt):
            disable_mirr_pop_up(evt.Checked())
            evt.Skip()

        enab_mirr_ctrl.Bind(wx.EVT_CHECKBOX, on_dis_mirr)

        def on_button(evt):
            dlg = EnableDialog(
                parent=panel,
                plugin=self,
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.show_enab_dialog,
            )
            evt.Skip()

        button.Bind(wx.EVT_BUTTON, on_button)

        push_group_btn = wx.Button(panel.dialog, -1, text.pushGroupsTitle)

        def on_push_group_btn(evt):
            dlg = PushGroupDialog(
                parent=panel,
                plugin=self,
            )
            wx.CallAfter(
                dlg.show_push_groups_dlg,
            )
            evt.Skip()

        push_group_btn.Bind(wx.EVT_BUTTON, on_push_group_btn)
        panel.dialog.buttonRow.Add(push_group_btn)

        sms_group_btn = wx.Button(panel.dialog, -1, text.smsGroupsTitle)

        def on_sms_group_btn(evt):
            dlg = SmsGroupDialog(
                parent=panel,
                plugin=self,
            )
            wx.CallAfter(
                dlg.show_sms_groups_dlg,
            )
            evt.Skip()

        sms_group_btn.Bind(wx.EVT_BUTTON, on_sms_group_btn)
        panel.dialog.buttonRow.Add(sms_group_btn)

        proxy_btn = wx.Button(panel.dialog, -1, text.proxyTitle)

        def on_proxy_btn(evt):
            dlg = ProxyDialog(
                parent=panel,
                plugin=self,
                labels=text.headers,
                data=panel.proxy,
            )
            wx.CallAfter(
                dlg.show_proxy_dlg, text.proxyTitle
            )
            evt.Skip()

        proxy_btn.Bind(wx.EVT_BUTTON, on_proxy_btn)
        panel.dialog.buttonRow.Add(proxy_btn)

        while panel.Affirmed():
            values = clip_filter_ctrl.GetValue()
            act_devs = self.get_active_devices()
            idens = []
            for iden in act_devs:
                if iden in values[2]:
                    ix = values[2].index(iden)
                    if values[1][ix]:
                        idens.append(iden)
            old_key = api_key.Get()
            new_key = api_ctrl.GetValue()
            if old_key != new_key:
                api_key.Set(new_key)
                dummy = str(ttime())
            old_passw = passw.Get()
            new_passw = passw_ctrl.GetValue()
            if old_passw != new_passw:
                passw.Set(new_passw)
                dummy = str(ttime())
            if proxy[3].Get() != panel.proxy[3].Get():
                dummy = str(ttime())
            panel.SetResult(
                nick_ctrl.GetValue(),
                api_key,
                self.iden,
                prefix_ctrl.GetValue(),
                int(rb1.GetValue()),
                fldr_ctrl.GetValue(),
                debug_ctrl.GetValue(),
                hide_ctrl.GetValue(),
                p_hide_ctrl.GetValue(),
                self.disabled,
                hide_btn_ctrl.GetValue(),
                wav_ctrl.GetValue(),
                auto_open_ctrl.GetValue(),
                dummy,
                enab_mirr_ctrl.GetValue(),
                clr_ctrl.GetValue(),
                alg_ctrl.GetValue(),
                dsp_ctrl.GetValue(),
                (x_of_ctrl.GetValue(), y_of_ctrl.GetValue()),
                idens,
                panel.push_groups,
                panel.sms_groups,
                passw,
                first_word_ctrl.GetValue(),
                compl_push_ctrl.GetValue(),
                panel.proxy
            )

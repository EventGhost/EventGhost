# -*- coding: utf-8 -*-

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
# 0.2.1 (2019-01-20) by topix
#       - outgoing server was not saved for an account in plugin config
# 0.2.0 (2018-10-21) by topix
#     - code cleanup
#     - code changes for wxPython 4.0 (some UI redesigning)
#     - compatibility with EG 0.4 and 0.5 (wxPython 3 and wxPython 4)
# 0.1.9  (2018-02-03) by topix
#     - some changes for EG0.5 because wxPython 3.0 handles some sizer
#       related things differently.
# 0.1.8 by Pako 2013-03-25 08:42 UTC+1
#     - added wx.ComboBox for event suffix (action "Start observation")
# ===============================================================================
# Structure of setup/account (one record):
# -----------------------------------------
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

# SMTP servers structure  (one record):
# -------------------------------------
# [0] = servName
# [1] = servAddress
# [2] = port
# [3] = secConnect
# [4] = secAutent
# [5] = userName
# [6] = userPassw

# texts structure (one record):  [txtName, txt]

# groups structure (one record): [groupName, [list of addresses]]

# temp_data structure (one record):
# --------------------------------
# [0] observ_name
# [1] last count
# [2] array of messages: [id, subject, from, account,numAbs,numAccount], [], ...
# [3] Work thread
# [4] Notification Frame
# Empty record:['', 0, [], None, None]

# Configs (Start observation) structure (one record):
# ----------------------------------------------------
# [0]=observ_name = string
# [1]=interval - integer
# [2]=[accounts] - list
# [3]=event name - string
# [4]=mode - integer (0-2)
# [5]=filter[[integer,integer,string],[],[],[],[],[],...]
# [6]=show notif window - boolean
# [7]=trigger event - boolean
# [8]=attach payload - integer (0, 1)
# [9]=Background Colour
# [10]=Foreground Colour
# [11]=trigger event2 - boolean
# [12]=event name2 - string
# [13]=attach payload2 - integer (0, 1, 2, 3)
# [14]=delete event - boolean
# ===============================================================================

import eg

__version__ = "0.2.1"

eg.RegisterPlugin(
    name="E-mail",
    author="Pako",
    version=__version__,
    kind="other",
    guid="{8BEB93CE-242E-46B5-A17A-D9737D362E1E}",
    createMacrosOnAdd=True,
    icon=(
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
    description=(
        "Trigger events on incoming mail (global or filtered) and an action for sending eMails."
    ),
    url="http://www.eventghost.org/forum/viewtopic.php?f=9&t=1168",
)


from copy import deepcopy

import wx
from wx.lib.intctrl import IntCtrl as intCtrl

from .actions import AbortAllObservations, AbortObservation, SendEmail, StartObservation
from .dialogs import GroupsDialog, ObservViewerDialog, OutServerDialog, SignaturesDialog
from .threads import ObservationThread
from .utils import move_item, validate_email_addr


ACTIONS = (
    (StartObservation, 'StartObservation', 'Start observation', 'Start observation.', None),
    (AbortObservation, 'AbortObservation', 'Abort observation', 'Abort observation.', None),
    (AbortAllObservations, 'AbortAllObservations', 'Abort all observations', 'Abort all observations.', None),
    (SendEmail, 'SendEmail', 'Send e-mail', 'Send e-mail.', None),
)


# noinspection PyClassHasNoInit
class Text(eg.TranslatableStrings):
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
    # user = 'User name:'
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
    refresh = "Refresh"
    client = "E-mail client"
    reply = "Reply"
    close = "Close"
    textsTitle = 'Signatures for outgoing e-mails'
    textsList = "Signatures:"
    txtLabel = "Text name:"
    outText = "Text:"
    groupsTitle = 'Recipient groups for outgoing e-mails'
    groupsList = "List of groups:"
    groupLabel = "Group name:"
    addressLabel = "E-mail address:"
    outAddress = "List of e-mail addresses:"
    deleteServer = ('Server "%s" is used in your configuration.\n'
                    'You cannot remove it.')
    details_title = 'Observation'
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


class EMail(eg.PluginClass):
    text = Text

    def __init__(self):
        super(EMail, self).__init__()
        self.AddActionsFromList(ACTIONS)
        self.configs = []
        self.servers = []
        self.texts = []
        self.groups = []
        self.observ_threads = {}

    def __stop__(self):
        self.abort_all_observations(close=True)

    def __close__(self):
        self.abort_all_observations(close=True)

    def __start__(self, configs=None, servers=None, texts=None, groups=None, pass_inc=None, pass_smtp=None):
        if groups is None:
            groups = []
        if texts is None:
            texts = []
        if servers is None:
            servers = []
        if configs is None:
            configs = []
        if pass_inc is None:
            pass_inc = eg.Bunch(data={})
        if pass_smtp is None:
            pass_smtp = eg.Bunch(data={})
        self.observ_threads = {}
        self.temp_data = []
        self.pass_inc = pass_inc
        self.pass_smtp = pass_smtp
        self.servers = servers
        self.configs = configs
        self.texts = texts
        self.groups = groups

    def Configure(self, configs=None, servers=None, texts=None, groups=None, pass_inc=None, pass_smtp=None):
        if groups is None:
            groups = []
        if texts is None:
            texts = []
        if servers is None:
            servers = []
        if configs is None:
            configs = []
        if pass_inc is None:
            pass_inc = eg.Bunch(data={})
        if pass_smtp is None:
            pass_smtp = eg.Bunch(data={})
        panel = eg.ConfigPanel(self)
        PluginConfig(self, panel, configs, servers, texts, groups, pass_inc, pass_smtp)

    def start_observation(self, setup, notif_frame):
        observ_name = setup[0]
        if observ_name in self.observ_threads:
            ot = self.observ_threads[observ_name]
            if ot.isAlive():
                ot.abort_observation()
        if observ_name not in [item[0] for item in self.temp_data]:
            self.temp_data.append([observ_name, 0, [], None, notif_frame])  # update temporary data store
        ot = ObservationThread(
            setup,
            self,
            notif_frame
        )
        ot.start()

    def abort_observation(self, observ_name):
        if observ_name in self.observ_threads:
            ot = self.observ_threads[observ_name]
            ot.abort_observation()

    def abort_all_observations(self, close=False):
        thrds = list(enumerate(self.observ_threads))
        thrds.reverse()
        for i, item in thrds:
            ot = self.observ_threads[item]
            ot.abort_observation(close)


class PluginConfig:
    def __init__(self, plugin, panel, configs, servers, texts, groups, pass_inc, pass_smtp):
        self.plugin = plugin
        self.panel = panel
        self.cfgs = deepcopy(configs)
        self.servers = deepcopy(servers)
        self.texts = deepcopy(texts)
        self.grps = deepcopy(groups)
        self.pass_inc = {}
        self.pass_smtp = {}
        for i, item in list(enumerate(pass_inc.data)):
            self.pass_inc[item] = pass_inc.data[item]
        for i, item in list(enumerate(pass_smtp.data)):
            self.pass_smtp[item] = pass_smtp.data[item]
        self.text = text = Text
        self.old_sel = -1
        panel.dialog.buttonRow.okButton.SetToolTip(wx.ToolTip(text.warning))

        self.create_widgets()
        self.create_sizers()
        self.bindings()

        if self.cfgs:
            self.list_box_ctrl.Set([n[0] for n in self.cfgs])
            self.list_box_ctrl.SetSelection(0)
            self.set_value(self.cfgs[0])
            self.old_sel = 0
            self.btn_up.Enable()
            self.btn_down.Enable()
            self.btn_del.Enable()
        else:
            self.box_enable(False)
            panel.dialog.buttonRow.applyButton.Disable()
            panel.dialog.buttonRow.okButton.Disable()

        while panel.Affirmed():
            pass_inc.data = self.pass_inc
            pass_smtp.data = self.pass_smtp
            panel.SetResult(
                self.cfgs,
                self.servers,
                self.texts,
                self.grps,
                pass_inc,
                pass_smtp
            )

    # noinspection PyAttributeOutsideInit
    def create_widgets(self):
        panel = self.panel
        text = self.text
        self.preview_lbl = wx.StaticText(panel, wx.ID_ANY, text.accountsList)
        # self.label_lbl = wx.StaticText(panel, wx.ID_ANY, text.label)
        self.user_name_lbl = wx.StaticText(panel, wx.ID_ANY, text.userName)
        self.mail_address_lbl = wx.StaticText(panel, wx.ID_ANY, text.mailAddress)
        self.repl_address_lbl = wx.StaticText(panel, wx.ID_ANY, text.replAddress)
        self.inc_server_lbl = wx.StaticText(panel, wx.ID_ANY, text.incServer)
        self.inc_port_lbl = wx.StaticText(panel, wx.ID_ANY, text.incPort)
        self.user_login_lbl = wx.StaticText(panel, wx.ID_ANY, text.userLogin)
        self.user_password_lbl = wx.StaticText(panel, wx.ID_ANY, text.userPassword)
        self.out_server_lbl = wx.StaticText(panel, wx.ID_ANY, text.outServer)
        self.choice_secure_lbl = wx.StaticText(panel, wx.ID_ANY, text.secureConnectLabel)

        self.user_name_ctrl = wx.TextCtrl(panel)
        self.mail_address_ctrl = wx.TextCtrl(panel)
        self.repl_address_ctrl = wx.TextCtrl(panel)
        self.inc_server_ctrl = wx.TextCtrl(panel)
        self.inc_port_ctrl = intCtrl(panel, wx.ID_ANY, 0)
        self.user_login_ctrl = wx.TextCtrl(panel)
        self.user_password_ctrl = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        self.label_ctrl = wx.TextCtrl(panel)
        self.list_box_ctrl = wx.ListBox(panel, style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.choice_type = wx.RadioBox(
            panel,
            label=text.accType,
            choices=text.eBoxCase,
        )
        self.out_server_ctrl = wx.Choice(panel, choices=[n[0] for n in self.servers])
        self.out_server_btn = wx.Button(panel, wx.ID_ANY, u'...')
        self.viewer_btn = wx.Button(panel, wx.ID_ANY, text.viewerTitle)
        self.txts_btn = wx.Button(panel, wx.ID_ANY, text.textsTitle)
        self.grps_btn = wx.Button(panel, wx.ID_ANY, text.groupsTitle)
        self.choice_secure_ctrl = wx.Choice(
            panel,
            wx.ID_ANY,
            choices=text.secureConnectChoice1,
        )
        self.use_secure_ctrl = wx.CheckBox(panel, label=text.useSecure)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, (16, 16))
        self.btn_up = wx.BitmapButton(panel, wx.ID_ANY, bmp)
        self.btn_up.Enable(False)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, (16, 16))
        self.btn_down = wx.BitmapButton(panel, wx.ID_ANY, bmp)
        self.btn_down.Enable(False)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16, 16))
        self.btn_del = wx.BitmapButton(panel, wx.ID_ANY, bmp)
        self.btn_del.Enable(False)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16))
        self.btn_app = wx.BitmapButton(panel, wx.ID_ANY, bmp)

    def create_sizers(self):
        top_middle_sizer = wx.BoxSizer(wx.VERTICAL)
        top_middle_sizer.Add(self.btn_up)
        top_middle_sizer.Add(self.btn_down, 0, wx.TOP, 3)
        top_middle_sizer.Add(self.btn_del, 0, wx.TOP, 5)
        top_middle_sizer.Add(self.btn_app, 0, wx.TOP, 5)

        top_left_sizer = wx.GridBagSizer(hgap=5, vgap=10)
        top_left_sizer.Add(self.preview_lbl, pos=(0, 0), flag=wx.EXPAND)
        top_left_sizer.Add(self.list_box_ctrl, pos=(1, 0), span=(4, 1), flag=wx.EXPAND)
        top_left_sizer.Add(self.label_ctrl, pos=(5, 0), span=(1, 2), flag=wx.EXPAND)
        top_left_sizer.Add(self.choice_type, pos=(6, 0))
        top_left_sizer.Add(self.btn_up, pos=(1, 1), flag=wx.ALIGN_BOTTOM)
        top_left_sizer.Add(self.btn_down, pos=(2, 1))
        top_left_sizer.Add(self.btn_del, pos=(3, 1))
        top_left_sizer.Add(self.btn_app, pos=(4, 1))
        top_left_sizer.AddGrowableCol(0, 1)
        top_left_sizer.AddGrowableRow(1, 1)
        top_left_sizer.SetFlexibleDirection(wx.BOTH)

        server_sizer_l = wx.BoxSizer(wx.VERTICAL)
        server_sizer_l.Add(self.inc_server_lbl, 0, wx.EXPAND)
        server_sizer_l.Add(self.inc_server_ctrl, 0, wx.EXPAND)

        server_sizer_r = wx.BoxSizer(wx.VERTICAL)
        server_sizer_r.Add(self.inc_port_lbl, 0, wx.LEFT, 3)
        server_sizer_r.Add(self.inc_port_ctrl, 0)

        server_sizer = wx.BoxSizer(wx.HORIZONTAL)
        server_sizer.Add(server_sizer_l, 1, wx.EXPAND)
        server_sizer.Add(server_sizer_r, 0, wx.LEFT, 5)

        out_serv_sizer = wx.BoxSizer(wx.HORIZONTAL)
        out_serv_sizer.Add(self.out_server_ctrl, 1, wx.EXPAND)
        out_serv_sizer.Add(self.out_server_btn, 0, wx.EXPAND)

        box = wx.StaticBox(self.panel, wx.ID_ANY, self.text.param)
        right_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        right_sizer.Add(self.user_name_lbl, 0, wx.TOP, 3)
        right_sizer.Add(self.user_name_ctrl, 0, wx.EXPAND)
        right_sizer.Add(self.user_login_lbl, 0, wx.TOP, 3)
        right_sizer.Add(self.user_login_ctrl, 0, wx.EXPAND)
        right_sizer.Add(self.user_password_lbl, 0, wx.TOP, 3)
        right_sizer.Add(self.user_password_ctrl, 0, wx.EXPAND)
        right_sizer.Add(self.mail_address_lbl, 0, wx.TOP, 3)
        right_sizer.Add(self.mail_address_ctrl, 0, wx.EXPAND)
        right_sizer.Add(self.repl_address_lbl, 0, wx.TOP, 3)
        right_sizer.Add(self.repl_address_ctrl, 0, wx.EXPAND)
        right_sizer.Add(self.use_secure_ctrl, 0, wx.TOP, 5)
        right_sizer.Add(self.choice_secure_lbl, 0, wx.TOP, 3)
        right_sizer.Add(self.choice_secure_ctrl, 0, wx.EXPAND)
        right_sizer.Add(server_sizer, 0, wx.EXPAND | wx.TOP, 3)
        right_sizer.Add(self.out_server_lbl, 0, wx.TOP, 3)
        right_sizer.Add(out_serv_sizer, 0, wx.EXPAND | wx.TOP, 3)

        box2 = wx.StaticBox(self.panel)
        mgr_sizer = wx.StaticBoxSizer(box2, wx.VERTICAL)
        mgr_sizer.Add(self.viewer_btn, 0, wx.EXPAND)
        mgr_sizer.Add(self.txts_btn, 0, wx.EXPAND | wx.TOP, 10)
        mgr_sizer.Add(self.grps_btn, 0, wx.EXPAND | wx.TOP, 10)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(top_left_sizer, 1, wx.EXPAND)
        left_sizer.Add(mgr_sizer, 0, wx.EXPAND | wx.TOP, 10)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(left_sizer, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(right_sizer, 1, wx.TOP | wx.BOTTOM | wx.RIGHT, 10)
        self.panel.sizer.Add(main_sizer, 1, wx.EXPAND)
        wx.CallAfter(self.panel.Layout)
        wx.CallAfter(self.panel.Refresh)

    def bindings(self):
        self.label_ctrl.Bind(wx.EVT_TEXT, self.on_label_and_password)
        self.user_password_ctrl.Bind(wx.EVT_TEXT, self.on_label_and_password)
        self.choice_type.Bind(wx.EVT_RADIOBOX, self.on_choice_type)
        self.user_name_ctrl.Bind(wx.EVT_TEXT, self.on_user_name)
        self.mail_address_ctrl.Bind(wx.EVT_TEXT, self.on_mail_address)
        self.repl_address_ctrl.Bind(wx.EVT_TEXT, self.on_repl_address)
        self.inc_server_ctrl.Bind(wx.EVT_TEXT, self.on_inc_server)
        self.inc_port_ctrl.Bind(wx.EVT_TEXT, self.on_inc_port)
        self.user_login_ctrl.Bind(wx.EVT_TEXT, self.on_user_login)
        self.out_server_ctrl.Bind(wx.EVT_CHOICE, self.on_out_server)
        self.choice_secure_ctrl.Bind(wx.EVT_CHOICE, self.on_choice_secure)
        self.use_secure_ctrl.Bind(wx.EVT_CHECKBOX, self.on_use_secure)
        self.out_server_btn.Bind(wx.EVT_BUTTON, self.on_serv_button)
        self.txts_btn.Bind(wx.EVT_BUTTON, self.on_txts_button)
        self.grps_btn.Bind(wx.EVT_BUTTON, self.on_grps_button)
        self.viewer_btn.Bind(wx.EVT_BUTTON, self.on_viewer_button)
        self.list_box_ctrl.Bind(wx.EVT_LISTBOX, self.on_list_click)
        self.btn_up.Bind(wx.EVT_BUTTON, self.on_button_up)
        self.btn_down.Bind(wx.EVT_BUTTON, self.on_button_down)
        self.btn_del.Bind(wx.EVT_BUTTON, self.on_button_delete)
        self.btn_app.Bind(wx.EVT_BUTTON, self.on_button_append)

    def box_enable(self, enable):
        self.choice_type.Enable(enable)
        self.label_ctrl.Enable(enable)
        # self.label_lbl.Enable(enable)
        self.user_name_lbl.Enable(enable)
        self.user_name_ctrl.Enable(enable)
        self.mail_address_lbl.Enable(enable)
        self.mail_address_ctrl.Enable(enable)
        self.repl_address_lbl.Enable(enable)
        self.repl_address_ctrl.Enable(enable)
        self.inc_server_lbl.Enable(enable)
        self.inc_server_ctrl.Enable(enable)
        self.inc_port_lbl.Enable(enable)
        self.inc_port_ctrl.Enable(enable)
        self.user_login_lbl.Enable(enable)
        self.user_login_ctrl.Enable(enable)
        self.user_password_lbl.Enable(enable)
        self.user_password_ctrl.Enable(enable)
        self.out_server_lbl.Enable(enable)
        self.out_server_ctrl.Enable(enable)
        self.out_server_btn.Enable(enable)
        self.choice_secure_lbl.Enable(enable)
        self.choice_secure_ctrl.Enable(enable)
        self.use_secure_ctrl.Enable(enable)

    def set_value(self, item):
        self.label_ctrl.ChangeValue(item[0])
        self.choice_type.SetSelection(item[1])
        self.user_name_ctrl.SetValue(item[2])
        self.mail_address_ctrl.SetValue(item[3])
        self.repl_address_ctrl.SetValue(item[4])
        self.inc_server_ctrl.SetValue(item[5])
        self.inc_port_ctrl.SetValue(item[6])
        self.user_login_ctrl.SetValue(item[7])
        self.out_server_ctrl.SetStringSelection(item[8])
        self.choice_secure_ctrl.SetSelection(item[9])
        self.use_secure_ctrl.SetValue(item[10])
        if item[0] in self.pass_inc and item[0] != u'':
            self.user_password_ctrl.ChangeValue(self.pass_inc[item[0]])
        else:
            self.user_password_ctrl.ChangeValue(u'')

    def validation(self):
        flag = True
        label = self.label_ctrl.GetValue()
        if label == u'':
            flag = False
        else:
            if [n[0] for n in self.cfgs].count(label) != 1:
                flag = False
        if not validate_email_addr(self.mail_address_ctrl.GetValue()):
            flag = False
        repl_addr = self.repl_address_ctrl.GetValue()
        if repl_addr != '' and not validate_email_addr(repl_addr):
            flag = False
        if self.inc_server_ctrl.GetValue() == u'':
            flag = False
        if self.inc_port_ctrl.GetValue() < 0:
            flag = False
        if self.user_login_ctrl.GetValue() == u'':
            flag = False
        if self.user_password_ctrl.GetValue() == u'':
            flag = False
        if self.out_server_ctrl.GetSelection() == -1:
            flag = False
        self.panel.dialog.buttonRow.applyButton.Enable(flag)
        self.panel.dialog.buttonRow.okButton.Enable(flag)
        self.btn_app.Enable(flag)

    def on_label_and_password(self, evt):
        if self.cfgs:
            sel = self.old_sel
            label = self.label_ctrl.GetValue().strip()
            val = self.user_password_ctrl.GetValue().strip()
            self.cfgs[sel][0] = label
            self.list_box_ctrl.Set([n[0] for n in self.cfgs])
            self.list_box_ctrl.SetSelection(sel)
            if val != u'':
                self.pass_inc[label] = val
            self.validation()
        evt.Skip()

    def set_port(self):
        ports = ((110, -1, -1, 995), (143, -1, -1, 993))
        secure = self.choice_secure_ctrl.GetSelection()
        typ = self.choice_type.GetSelection()
        port = ports[typ][secure]
        if port > -1:
            self.inc_port_ctrl.SetValue(port)

    def on_choice_type(self, evt):
        typ = self.choice_type.GetSelection()
        sel = self.old_sel
        self.cfgs[sel][1] = typ
        self.set_port()
        self.validation()
        evt.Skip()

    def on_user_name(self, evt):
        if self.cfgs:
            val = self.user_name_ctrl.GetValue().strip()
            sel = self.old_sel
            self.cfgs[sel][2] = val
        evt.Skip()

    def on_mail_address(self, evt):
        if self.cfgs:
            val = self.mail_address_ctrl.GetValue().strip()
            sel = self.old_sel
            self.cfgs[sel][3] = val
            self.validation()
        evt.Skip()

    def on_repl_address(self, evt):
        if self.cfgs:
            val = self.repl_address_ctrl.GetValue().strip()
            sel = self.old_sel
            self.cfgs[sel][4] = val
            self.validation()
        evt.Skip()

    def on_inc_server(self, evt):
        if self.cfgs:
            val = self.inc_server_ctrl.GetValue().strip()
            sel = self.old_sel
            self.cfgs[sel][5] = val
            self.validation()
        evt.Skip()

    def on_inc_port(self, evt):
        if self.cfgs:
            val = self.inc_port_ctrl.GetValue()
            sel = self.old_sel
            self.cfgs[sel][6] = val
            self.validation()
        evt.Skip()

    def on_user_login(self, evt):
        if self.cfgs:
            val = self.user_login_ctrl.GetValue().strip()
            sel = self.old_sel
            self.cfgs[sel][7] = val
            self.validation()
        evt.Skip()

    def on_out_server(self, evt):
        if self.cfgs:
            val = self.out_server_ctrl.GetStringSelection()
            sel = self.old_sel
            self.cfgs[sel][8] = val
            self.validation()
        evt.Skip()

    def on_choice_secure(self, evt):
        if self.cfgs:
            val = self.choice_secure_ctrl.GetSelection()
            sel = self.old_sel
            self.cfgs[sel][9] = val
            self.set_port()
        evt.Skip()

    def on_use_secure(self, evt):
        if self.cfgs:
            val = self.use_secure_ctrl.GetValue()
            sel = self.old_sel
            self.cfgs[sel][10] = val
        evt.Skip()

    def on_serv_button(self, evt):
        evt.Skip()
        dlg = OutServerDialog(
            parent=self.panel,
            plugin=self.plugin,
            servers=self.servers,
            pass_smtp=self.pass_smtp,
            cfgs=self.cfgs,
            val=self.out_server_ctrl.GetStringSelection()
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.servers = dlg.get_servers()
            self.pass_smtp = dlg.get_pass_smtp()
            choices = [n[0] for n in self.servers]
            self.out_server_ctrl.SetItems(choices)
            self.out_server_ctrl.SetStringSelection(dlg.get_string_for_selection())
        dlg.Destroy()

    def on_txts_button(self, evt):
        evt.Skip()
        dlg = SignaturesDialog(
            parent=self.panel,
            plugin=self.plugin,
            signatures=self.texts
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.texts = dlg.get_texts()
        dlg.Destroy()

    def on_grps_button(self, evt):
        evt.Skip()
        dlg = GroupsDialog(
            parent=self.panel,
            plugin=self.plugin,
            grps=self.grps
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.grps = dlg.get_groups()
        dlg.Destroy()

    def on_viewer_button(self, evt):
        evt.Skip()
        dlg = ObservViewerDialog(
            parent=self.panel,
            plugin=self.plugin,
        )
        wx.CallAfter(dlg.show_observ_viewer_dialog)

    def on_list_click(self, evt):
        evt.Skip()
        sel = self.list_box_ctrl.GetSelection()
        label = self.label_ctrl.GetValue()
        if label.strip() != "":
            if [n[0] for n in self.cfgs].count(label) == 1:
                self.old_sel = sel
                item = self.cfgs[sel]
                self.set_value(item)
        self.list_box_ctrl.SetSelection(self.old_sel)
        self.list_box_ctrl.SetFocus()

    def on_button_up(self, evt):
        evt.Skip()
        new_sel, self.cfgs = move_item(self.cfgs, self.list_box_ctrl.GetSelection(), -1)
        self.list_box_ctrl.Set([n[0] for n in self.cfgs])
        self.list_box_ctrl.SetSelection(new_sel)
        self.old_sel = new_sel

    def on_button_down(self, evt):
        evt.Skip()
        new_sel, self.cfgs = move_item(self.cfgs, self.list_box_ctrl.GetSelection(), 1)
        self.list_box_ctrl.Set([n[0] for n in self.cfgs])
        self.list_box_ctrl.SetSelection(new_sel)
        self.old_sel = new_sel

    def on_button_delete(self, evt):
        evt.Skip()
        lngth = len(self.cfgs)
        if lngth == 2:
            self.btn_up.Enable(False)
            self.btn_down.Enable(False)
        sel = self.list_box_ctrl.GetSelection()
        if lngth == 1:
            self.cfgs = []
            self.list_box_ctrl.Set([])
            item = [u'', 0, u'', u'', u'', u'', 0, u'', u'', 0, False]
            self.set_value(item)
            self.box_enable(False)
            self.panel.dialog.buttonRow.applyButton.Enable(False)
            self.panel.dialog.buttonRow.okButton.Enable(False)
            self.btn_del.Enable(False)
            self.btn_app.Enable(True)
            return
        elif sel == lngth - 1:
            sel = 0
        self.old_sel = sel
        self.cfgs.pop(self.list_box_ctrl.GetSelection())
        self.list_box_ctrl.Set([n[0] for n in self.cfgs])
        self.list_box_ctrl.SetSelection(sel)
        item = self.cfgs[sel]
        self.set_value(item)

    def on_button_append(self, evt):
        evt.Skip()
        if len(self.cfgs) == 1:
            self.btn_up.Enable(True)
            self.btn_down.Enable(True)
        self.box_enable(True)
        self.label_ctrl.Enable(True)
        sel = self.list_box_ctrl.GetSelection() + 1
        self.old_sel = sel
        item = [u'', 0, u'', u'', u'', u'', 0, u'', u'', 0, False]
        self.cfgs.insert(sel, item)
        self.list_box_ctrl.Set([n[0] for n in self.cfgs])
        self.list_box_ctrl.SetSelection(sel)
        self.set_value(item)
        self.set_port()
        self.choice_secure_ctrl.SetSelection(0)
        self.out_server_ctrl.Clear()
        self.out_server_ctrl.AppendItems([n[0] for n in self.servers])
        self.out_server_ctrl.SetSelection(0)
        self.label_ctrl.SetFocus()
        self.btn_app.Enable(False)
        self.btn_del.Enable(True)

# coding=utf8

from copy import deepcopy

import wx

import eg
from eg.WinApi.Dynamic import CreateEvent
from .dialogs import ComposeMsg, NotifFrame
from .dialogs.send_mail_dlg import SendMailText
from .threads import SendMailThread
from .utils import validate_email_addr


class AbortAllObservations(eg.ActionClass):
    def __call__(self):
        self.plugin.abort_all_observations()


# noinspection PyPep8Naming
class AbortObservation(eg.ActionClass):
    def __call__(self, observ_name=''):
        self.plugin.abort_observation(observ_name)

    def Configure(self, observ_name=''):
        text = self.text
        panel = eg.ConfigPanel(self)
        name_lbl = wx.StaticText(panel, -1, text.nameObs)
        name_ctrl = wx.TextCtrl(panel, -1, observ_name)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(name_lbl, 0)
        main_sizer.Add(name_ctrl, 0, wx.EXPAND)
        panel.sizer.Add(main_sizer)
        panel.sizer.Layout()

        # re-assign the test button
        def on_test_button(evt):
            evt.Skip()
            self.plugin.abort_observation(name_ctrl.GetValue())

        panel.dialog.buttonRow.testButton.SetLabel(text.abortNow)
        panel.dialog.buttonRow.testButton.SetToolTip(wx.ToolTip(text.tip))
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, on_test_button)

        while panel.Affirmed():
            panel.SetResult(
                name_ctrl.GetValue(),
            )

    # noinspection PyClassHasNoInit,PyPep8Naming
    class text:
        nameObs = 'Observation name:'
        abortNow = 'Abort now !'
        tip = 'Abort observation now'


# noinspection PyPep8Naming,PyAttributeOutsideInit
class StartObservation(eg.ActionClass):

    def startObserv(self, stp):
        observ_name = stp[0]
        data = [item[0] for item in self.plugin.temp_data]
        if observ_name in data:
            indx = data.index(observ_name)
            self.notifFrame = self.plugin.temp_data[indx][4]
        else:
            self.notifFrame = NotifFrame(None, self.plugin)
        self.event = CreateEvent(None, 0, 0, None)
        wx.CallAfter(
            self.notifFrame.show_notif_frame,
            stp=stp,
            event=self.event
        )
        eg.actionThread.WaitOnEvent(self.event)
        self.plugin.start_observation(stp, self.notifFrame)

    def __call__(self, stp):
        accounts = []
        acc_list = [item[0] for item in self.plugin.configs]
        for i in range(len(acc_list)):
            for item in stp[2]:
                if item == acc_list[i]:
                    accounts.append(i)
        if len(accounts) > 0:
            self.startObserv(stp)
        else:
            eg.PrintError(self.text.warning % stp[2])

    def GetLabel(self, stp):
        res1 = stp[0]
        return res1

    def Configure(self, stp=None):
        if not stp:
            self.stp = [
                '', 2, [], '', 0,
                [[-1, -1, ''], [-1, -1, ''], [-1, -1, ''], [-1, -1, ''], [-1, -1, ''], [-1, -1, '']],
                False, True, 0, (255, 255, 255), (0, 0, 0), False, '', 0, False
            ]
        else:
            self.stp = deepcopy(stp)
        self.max_filters = 6
        self.filter_ctrls = []

        self.create_widgets()
        self.create_sizers()
        self.bindings()
        self.onMessageCtrl()
        self.EnableEvent2Ctrl()

        while self.panel.Affirmed():
            self.UpdateConfig()
            self.panel.SetResult(
                self.stp,
            )

    def validation(self, evt=None):
        if evt:
            evt.Skip()
        flag = True

        if self.name_ctrl.GetValue() == "":
            flag = False

        if int(wx.__version__.split('.', 1)[0]) < 4:
            chk = True
            for idx in range(self.account_ctrl.GetCount()):
                if self.account_ctrl.IsChecked(idx):
                    chk = False
                    break
            if chk:
                flag = False
        else:
            if len(self.account_ctrl.GetCheckedItems()) == 0:
                flag = False

        if (
            not self.event_ctrl.GetValue()
            and not self.event2_ctrl.GetValue()
            and not self.message_ctrl.GetValue()
        ):
            flag = False

        if self.event_ctrl.GetValue():
            if self.evt_name_ctrl.GetValue() == '':
                flag = False

        if self.event2_ctrl.GetValue():
            if self.evt_name2_ctrl.GetValue() == '':
                flag = False

        if not self.rb0.GetValue():
            for row in range(self.max_filters):
                wnd0 = self.filter_ctrls[row][0]
                if wnd0.GetSelection() > 0:
                    wnd1 = self.filter_ctrls[row][1]
                    wnd2 = self.filter_ctrls[row][2]
                    if wnd1.GetSelection() == -1:
                        flag = False
                        break
                    if wnd2.GetValue() == '':
                        flag = False
                        break

        self.panel.dialog.buttonRow.applyButton.Enable(flag)
        self.panel.dialog.buttonRow.okButton.Enable(flag)

    def on_filter(self, evt):
        obj = evt.GetEventObject()
        row = int(obj.GetName())
        ctrl_1 = self.filter_ctrls[row][0]
        ctrl_2 = self.filter_ctrls[row][1]
        ctrl_3 = self.filter_ctrls[row][2]

        indx = ctrl_1.GetSelection()
        flag = indx > 0
        ctrl_2.Enable(flag)
        ctrl_3.Enable(flag)
        if not flag:
            ctrl_2.SetSelection(-1)
            ctrl_3.ChangeValue(u'')
        choic_len = len(ctrl_2.GetStrings())
        if choic_len == 2 and indx != 3:
            ctrl_2.Clear()
            ctrl_2.AppendItems(items=self.text.field_2)
        elif choic_len == 6 and indx == 3:
            ctrl_2.Clear()
            ctrl_2.AppendItems(items=self.text.field_2[:2])
        self.validation()

    def create_widgets(self):
        text = self.text
        self.panel = panel = eg.ConfigPanel(self)
        self.name_lbl = wx.StaticText(panel, label=text.nameObs)
        self.name_ctrl = wx.TextCtrl(panel, value=self.stp[0])
        self.interval_lbl_1 = wx.StaticText(panel, label=text.interval_1)
        self.interval_ctrl = eg.SpinIntCtrl(panel, value=self.stp[1], min=1, max=999)
        self.interval_lbl_2 = wx.StaticText(panel, label=text.interval_2)
        self.account_lbl = wx.StaticText(panel, -1, text.accounts)
        choices = [row[0] for row in self.plugin.configs]
        self.account_ctrl = wx.CheckListBox(panel, choices=choices)
        checked = self.stp[2]
        self.account_ctrl.SetCheckedStrings(checked)

        self.rb0 = panel.RadioButton(self.stp[4] == 0, text.radio_buttons[0], style=wx.RB_GROUP)
        self.rb1 = panel.RadioButton(self.stp[4] == 1, text.radio_buttons[1])
        self.rb2 = panel.RadioButton(self.stp[4] == 2, text.radio_buttons[2])
        self.message_ctrl = wx.CheckBox(panel, label=text.message)
        self.message_ctrl.SetValue(self.stp[6])
        self.message_ctrl.Enable(not self.stp[14])
        self.message_ctrl.SetToolTip(wx.ToolTip(text.tip0))
        self.event_ctrl = wx.CheckBox(panel, label=text.totalEvent)
        self.event_ctrl.SetToolTip(wx.ToolTip(text.tip4))
        self.event2_ctrl = wx.CheckBox(panel, label=text.emailEvent)
        self.event2_ctrl.SetToolTip(wx.ToolTip(text.tip3))
        self.event2_ctrl.SetValue(self.stp[11])
        self.event_ctrl.SetValue(self.stp[7])
        self.event_ctrl.Enable(not self.stp[14])
        self.event2_ctrl.Disable()
        self.evt_name_lbl = wx.StaticText(panel, label=text.evtName)
        self.evt_name_ctrl = wx.TextCtrl(panel, value=self.stp[3])
        self.evt_name2_ctrl = wx.ComboBox(
            parent=panel,
            choices=self.plugin.text.field_1[1:],
            style=wx.CB_DROPDOWN
        )
        self.evt_name2_ctrl.SetValue(self.stp[12])
        self.payload_lbl = wx.StaticText(panel, -1, text.payload)
        self.payload_ctrl = wx.Choice(panel, choices=text.totalPayload)
        self.payload2_ctrl = wx.Choice(panel, choices=self.plugin.text.field_1)
        self.payload_ctrl.SetSelection(self.stp[8])
        self.payload2_ctrl.SetSelection(self.stp[13])
        self.delete_ctrl = wx.CheckBox(panel, label=text.delete)
        self.delete_ctrl.SetValue(self.stp[14])
        self.delete_ctrl.SetToolTip(wx.ToolTip(text.tip1))

        for row in range(self.max_filters):
            indx0 = self.stp[5][row][0]

            field_ctrl_1 = wx.Choice(panel, choices=self.plugin.text.field_1, name=str(row))
            field_ctrl_1.Bind(wx.EVT_CHOICE, self.on_filter)
            field_ctrl_1.SetSelection(indx0)

            field_ctrl_2 = wx.Choice(panel, choices=text.field_2, name=str(row))
            field_ctrl_2.Bind(wx.EVT_CHOICE, self.validation)
            field_ctrl_2.SetSelection(self.stp[5][row][1])

            field_ctrl_3 = wx.TextCtrl(panel, value=self.stp[5][row][2], name=str(row))
            field_ctrl_3.Bind(wx.EVT_TEXT, self.validation)

            if indx0 == -1:
                field_ctrl_1.Disable()
            if indx0 < 1:
                field_ctrl_2.Disable()
                field_ctrl_3.Disable()

            self.filter_ctrls.append(
                [
                    field_ctrl_1,
                    field_ctrl_2,
                    field_ctrl_3
                ]
            )

        self.label_bck = wx.StaticText(panel, label=text.backCol)
        self.label_fore = wx.StaticText(panel, label=text.forCol)
        self.background_colour_button = wx.ColourPickerCtrl(panel)
        self.background_colour_button.SetColour(self.stp[9])
        self.foreground_colour_button = wx.ColourPickerCtrl(panel)
        self.foreground_colour_button.SetColour(self.stp[10])

        panel.dialog.buttonRow.testButton.SetLabel(text.startNow)
        panel.dialog.buttonRow.testButton.SetToolTip(wx.ToolTip(text.tip2))

    def create_sizers(self):
        interval_sizer = wx.BoxSizer(wx.HORIZONTAL)
        interval_sizer.Add(self.interval_lbl_1, 0, wx.TOP, 4)
        interval_sizer.Add(self.interval_ctrl, 0, wx.LEFT | wx.RIGHT, 4)
        interval_sizer.Add(self.interval_lbl_2, 0, wx.TOP, 4)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(self.name_lbl)
        left_sizer.Add(self.name_ctrl, 0, wx.EXPAND)
        left_sizer.Add(interval_sizer, 0, wx.EXPAND | wx.TOP, 15)
        left_sizer.Add(self.account_lbl, 0, wx.TOP, 15)
        left_sizer.Add(self.account_ctrl, 1, wx.EXPAND)

        filter_sizer = wx.FlexGridSizer(rows=self.max_filters, cols=3, vgap=0, hgap=0)
        for row in range(self.max_filters):
            filter_sizer.Add(self.filter_ctrls[row][0], 0, wx.EXPAND)
            filter_sizer.Add(self.filter_ctrls[row][1], 0, wx.EXPAND)
            filter_sizer.Add(self.filter_ctrls[row][2], 0, wx.EXPAND)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(self.rb0, 0, wx.TOP, 0)
        right_sizer.Add(self.rb1, 0, wx.TOP, 2)
        right_sizer.Add(self.rb2, 0, wx.TOP, 2)
        right_sizer.Add(filter_sizer, 0, wx.EXPAND | wx.TOP, 7)

        horiz_sizer = wx.BoxSizer(wx.HORIZONTAL)
        horiz_sizer.Add(left_sizer, 0, wx.EXPAND, wx.TOP, 0)
        horiz_sizer.Add(right_sizer, 0, wx.LEFT | wx.EXPAND, 16)

        event_sizer = wx.GridBagSizer(2, 10)
        event_sizer.Add(self.evt_name_lbl, (0, 1))
        event_sizer.Add(self.payload_lbl, (0, 2))
        event_sizer.Add(self.event2_ctrl, (1, 0), flag=wx.TOP, border=4)
        event_sizer.Add(self.evt_name2_ctrl, (1, 1), flag=wx.EXPAND)
        event_sizer.Add(self.payload2_ctrl, (1, 2), flag=wx.EXPAND)
        event_sizer.Add(self.delete_ctrl, (1, 3), flag=wx.TOP, border=4)
        event_sizer.Add(self.event_ctrl, (2, 0), flag=wx.TOP, border=10)
        event_sizer.Add(self.evt_name_ctrl, (2, 1), flag=wx.TOP | wx.EXPAND, border=6)
        event_sizer.Add(self.payload_ctrl, (2, 2), flag=wx.TOP | wx.EXPAND, border=6)

        notify_sizer = wx.BoxSizer(wx.HORIZONTAL)
        notify_sizer.Add(self.message_ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)
        notify_sizer.Add(self.label_bck, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        notify_sizer.Add(self.background_colour_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)
        notify_sizer.Add(self.label_fore, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        notify_sizer.Add(self.foreground_colour_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

        self.panel.sizer.Add(horiz_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.panel.sizer.Add(event_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.panel.sizer.Add(notify_sizer, 0, wx.ALL, 5)
        self.panel.sizer.Layout()

    def bindings(self):
        self.background_colour_button.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnBackgroundColourButton)
        self.foreground_colour_button.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnForegroundColourButton)
        self.rb0.Bind(wx.EVT_RADIOBUTTON, self.onRadioBtns)
        self.rb1.Bind(wx.EVT_RADIOBUTTON, self.onRadioBtns)
        self.rb2.Bind(wx.EVT_RADIOBUTTON, self.onRadioBtns)
        self.event2_ctrl.Bind(wx.EVT_CHECKBOX, self.onEvent2Ctrl)
        self.delete_ctrl.Bind(wx.EVT_CHECKBOX, self.onDeleteCtrl)
        self.event_ctrl.Bind(wx.EVT_CHECKBOX, self.onEventCtrl)
        self.name_ctrl.Bind(wx.EVT_TEXT, self.onNameCtrl)
        self.evt_name_ctrl.Bind(wx.EVT_TEXT, self.validation)
        self.evt_name2_ctrl.Bind(wx.EVT_TEXT, self.validation)
        self.evt_name2_ctrl.Bind(wx.EVT_COMBOBOX, self.validation)
        self.message_ctrl.Bind(wx.EVT_CHECKBOX, self.onMessageCtrl)
        self.account_ctrl.Bind(wx.EVT_CHECKLISTBOX, self.onCheckListBox)
        self.panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, self.on_start_observer_button)

    def OnBackgroundColourButton(self, event):
        self.stp[9] = event.GetColour()

    def OnForegroundColourButton(self, event):
        self.stp[10] = event.GetColour()

    def EnableEventCtrl(self):
        flag = self.delete_ctrl.GetValue()
        self.event_ctrl.Enable(not flag)
        if flag:
            self.event_ctrl.SetValue(False)
            self.evt_name_ctrl.Enable(False)
            self.payload_ctrl.Enable(False)
            self.evt_name_ctrl.ChangeValue('')
            self.payload_ctrl.SetSelection(0)

    def EnableEvent2Ctrl(self):
        if self.rb0.GetValue():
            self.event2_ctrl.SetValue(False)
            self.event2_ctrl.Enable(False)
        else:
            self.event2_ctrl.Enable(True)
            self.onEvent2Ctrl()
        self.EnableEventCtrl()

    def onRadioBtns(self, evt=None):
        if evt:
            evt.Skip()
        if self.rb0.GetValue():
            mode = 0
            for row in range(self.max_filters):
                ctrl_1 = self.filter_ctrls[row][0]
                ctrl_2 = self.filter_ctrls[row][1]
                ctrl_3 = self.filter_ctrls[row][2]
                ctrl_1.Enable(False)
                ctrl_2.Enable(False)
                ctrl_3.Enable(False)
                ctrl_1.SetSelection(-1)
                ctrl_2.SetSelection(-1)
                ctrl_3.ChangeValue('')
        else:
            for row in range(self.max_filters):
                ctrl_1 = self.filter_ctrls[row][0]
                if not ctrl_1.IsEnabled():
                    ctrl_1.SetSelection(0)
                    ctrl_1.Enable(True)
            if self.rb1.GetValue():
                mode = 1
            else:
                mode = 2
        self.stp[4] = mode
        self.EnableEvent2Ctrl()
        self.validation()

    def onEvent2Ctrl(self, evt=None):
        if evt:
            evt.Skip()
        flag = self.event2_ctrl.GetValue()
        self.evt_name2_ctrl.Enable(flag)
        self.payload2_ctrl.Enable(flag)
        self.delete_ctrl.Enable(flag)
        if not flag:
            self.payload2_ctrl.SetSelection(0)
            self.delete_ctrl.SetValue(False)
            self.stp[12] = ''
        self.stp[11] = flag
        self.validation()

    def onDeleteCtrl(self, evt=None):
        if evt:
            evt.Skip()
        flag = self.delete_ctrl.GetValue()
        self.message_ctrl.Enable(not flag)
        if flag:
            self.message_ctrl.SetValue(False)
        self.onMessageCtrl()
        self.EnableEventCtrl()
        self.validation()

    def onEventCtrl(self, evt=None):
        if evt:
            evt.Skip()
        flag = self.event_ctrl.GetValue()
        self.evt_name_ctrl.Enable(flag)
        self.payload_ctrl.Enable(flag)
        if not flag:
            self.stp[3] = ''
        self.validation()

    def onNameCtrl(self, evt):
        evt.Skip()
        self.stp[0] = self.name_ctrl.GetValue()
        self.validation()

    def onMessageCtrl(self, evt=None):
        if evt:
            evt.Skip()
        self.stp[6] = self.message_ctrl.GetValue()
        flag = self.stp[6]

        self.label_bck.Enable(flag)
        self.label_fore.Enable(flag)
        self.background_colour_button.Enable(flag)
        self.foreground_colour_button.Enable(flag)
        self.validation()

    def onCheckListBox(self, evt):
        index = evt.GetSelection()
        self.validation()
        # so that (un)checking also selects (moves the highlight)
        self.account_ctrl.SetSelection(index)

    def UpdateConfig(self):
        choics = self.account_ctrl.GetStrings()
        tmp_list = []
        for row in range(len(choics)):
            if self.account_ctrl.IsChecked(row):
                tmp_list.append(choics[row])
        self.stp[2] = tmp_list[:]
        tmp_list = []
        for row in range(self.max_filters):
            ctrl_0 = self.filter_ctrls[row][0]
            indx_0 = ctrl_0.GetSelection()
            ctrl_1 = self.filter_ctrls[row][1]
            indx_1 = ctrl_1.GetSelection()
            val2 = self.filter_ctrls[row][2].GetValue()
            tmp_list.append((indx_0, indx_1, val2))
        self.stp[5] = tmp_list[:]
        self.stp[1] = self.interval_ctrl.GetValue()
        self.stp[3] = self.evt_name_ctrl.GetValue()
        self.stp[7] = self.event_ctrl.GetValue()
        self.stp[8] = self.payload_ctrl.GetSelection()
        self.stp[12] = self.evt_name2_ctrl.GetValue()
        self.stp[13] = self.payload2_ctrl.GetSelection()
        self.stp[14] = self.delete_ctrl.GetValue()

    def on_start_observer_button(self, evt):
        evt.Skip()
        self.UpdateConfig()
        self.startObserv(self.stp)

    # noinspection PyClassHasNoInit,PyPep8Naming
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
        totalEvent = 'Trigger total event'
        evtName = 'Event name:'
        tip0 = 'Show notification window with count of waiting e-mails'
        tip1 = 'After event triggering delete e-mail on server'
        tip2 = 'Start observation now'
        tip3 = 'Trigger event for each e-mail'
        tip4 = 'Trigger event in any change in the number of waiting messages'
        emailEvent = "E-mail event"
        payload = 'Payload:'
        totalPayload = ("None", "Count")
        # noinspection SqlNoDataSourceInspection
        delete = 'Delete from server after event'
        startNow = 'Start now !'
        backCol = 'Background colour:'
        forCol = 'Foreground colour:'
        warning = 'Was found no one account, corresponding to the list %s !'


# noinspection PyPep8Naming
class SendEmail(eg.ActionClass, ComposeMsg):
    text = SendMailText

    def __call__(
        self,
        subject=u'',
        from_adr=u'',
        to_adr=u'',
        cc_adr=u'',
        body=u'',
        templates=u'',
        to_name=u'',
        references=None,
        message_id=None
    ):
        smt = SendMailThread(
            self.plugin,
            subject,
            from_adr,
            to_adr,
            cc_adr,
            body,
            templates,
            to_name,
            references,
            message_id
        )
        smt.start()

    def Configure(
        self,
        subject=u'',
        from_adr=u'',
        to_adr=u'',
        cc_adr=u'',
        body=u'',
        templates=u'',
        to_name=u''
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        top_sizer = self.send_cfg(
            panel, subject, from_adr, to_adr, cc_adr,
            body, templates, to_name, self.text, self.plugin
        )
        panel.sizer.Add(top_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 16)
        text = self.text

        # re-assign the test button
        def on_test_button(evt):
            evt.Skip()
            t = SendMailThread(
                self.plugin,
                self.subject_ctrl.GetValue(),
                self.from_ctrl.GetStringSelection(),
                self.to_ctrl.GetValue(),
                self.cc_ctrl.GetStringSelection(),
                self.body_ctrl.GetValue(),
                self.templates_ctrl.GetValue(),
                self.to_name_ctrl.GetValue(),
                None,
                None
            )
            t.start()

        panel.dialog.buttonRow.testButton.SetLabel(text.sendNow)
        panel.dialog.buttonRow.testButton.SetToolTip(wx.ToolTip(text.tip3))
        panel.dialog.buttonRow.testButton.Bind(wx.EVT_BUTTON, on_test_button)

        def validation(evt=None):
            if evt:
                evt.Skip()
            flag = True
            if not validate_email_addr(self.to_ctrl.GetValue()):
                flag = False
            if self.subject_ctrl.GetValue() == '':
                flag = False
            panel.dialog.buttonRow.applyButton.Enable(flag)
            panel.dialog.buttonRow.okButton.Enable(flag)

        self.subject_ctrl.Bind(wx.EVT_TEXT, validation)
        self.to_ctrl.Bind(wx.EVT_TEXT, validation)
        validation()
        panel.sizer.Layout()

        while panel.Affirmed():
            panel.SetResult(
                self.subject_ctrl.GetValue(),
                self.from_ctrl.GetStringSelection(),
                self.to_ctrl.GetValue(),
                self.cc_ctrl.GetStringSelection(),
                self.body_ctrl.GetValue(),
                self.templates_ctrl.GetValue(),
                self.to_name_ctrl.GetValue()
            )

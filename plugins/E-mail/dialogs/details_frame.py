# coding=utf8

import imaplib
import poplib

import wx

import eg
from .message_frame import MessageFrame
from ..utils import get_parts, my_parser, parse_address, run_email_client


class DetailsFrame(wx.MiniFrame):
    message_frame = None
    mess_fram_size = (-1, -1)
    mess_fram_position = (-1, -1)

    def __init__(self, parent):
        self.text = parent.plugin.text
        self.parent = parent
        self.plugin = parent.plugin
        self.pass_inc = self.plugin.pass_inc
        self.setup = parent.setup
        wx.MiniFrame.__init__(
            self,
            parent=parent,
            id=wx.ID_ANY,
            title=self.text.details_title,
            style=wx.CAPTION | wx.RESIZE_BORDER,
            name="Details Frame"
        )
        # self.SetBackgroundColour(wx.NullColour)
        self.menu_flag_s = False
        self.menu_flag_d = False
        self.del_flag = False
        self.show_button = wx.Button(self, wx.ID_ANY, self.text.show)
        self.delete_button = wx.Button(self, wx.ID_ANY, self.text.delete)
        self.refresh_button = wx.Button(self, wx.ID_ANY, self.text.refresh)
        self.client_button = wx.Button(self, wx.ID_ANY, self.text.client)
        self.close_button = wx.Button(self, wx.ID_ANY, self.text.close)
        self.messages_list_ctrl = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)
        for i, labels_details in enumerate(self.text.labelsDetails):
            self.messages_list_ctrl.InsertColumn(
                i,
                labels_details,
            )
        self.messages_list_ctrl.SetColumnWidth(0, 40)
        self.messages_list_ctrl.SetColumnWidth(1, 75)
        self.messages_list_ctrl.SetColumnWidth(2, 200)
        self.messages_list_ctrl.SetColumnWidth(3, 200)

        central_sizer = wx.GridBagSizer(10, 10)
        central_sizer.Add(self.messages_list_ctrl, (0, 0), (1, 9), flag=wx.EXPAND)
        central_sizer.Add(self.show_button, (1, 0), flag=wx.ALIGN_LEFT | wx.BOTTOM, border=10)
        central_sizer.Add(self.delete_button, (1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL)
        central_sizer.Add(self.refresh_button, (1, 4), flag=wx.ALIGN_CENTER_HORIZONTAL)
        central_sizer.Add(self.client_button, (1, 6), flag=wx.ALIGN_CENTER_HORIZONTAL)
        central_sizer.Add(self.close_button, (1, 8), flag=wx.ALIGN_RIGHT)
        central_sizer.AddGrowableRow(0)
        central_sizer.AddGrowableCol(1)
        central_sizer.AddGrowableCol(3)
        central_sizer.AddGrowableCol(5)
        central_sizer.AddGrowableCol(7)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(central_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        main_sizer.Fit(self)
        main_sizer.Layout()
        self.SetSizerAndFit(main_sizer)

        self.popupID1 = wx.NewIdRef()
        self.popupID2 = wx.NewIdRef()
        self.popupID3 = wx.NewIdRef()
        self.popupID4 = wx.NewIdRef()
        self.popupID5 = wx.NewIdRef()
            
        self.Bind(wx.EVT_MENU, self.on_show_button, id=self.popupID1)
        self.Bind(wx.EVT_MENU, self.on_delete_button, id=self.popupID2)
        self.Bind(wx.EVT_MENU, self.on_refresh, id=self.popupID3)
        self.Bind(wx.EVT_MENU, self.on_client_button, id=self.popupID4)
        self.Bind(wx.EVT_MENU, self.on_close_button, id=self.popupID5)
        self.messages_list_ctrl.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.on_right_click)
        self.messages_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_selection)
        self.messages_list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.list_selection)
        self.messages_list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_show_button)  # Doubleclick
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        self.close_button.Bind(wx.EVT_BUTTON, self.on_close_button)
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete_button)
        self.client_button.Bind(wx.EVT_BUTTON, self.on_client_button)
        self.show_button.Bind(wx.EVT_BUTTON, self.on_show_button)
        self.refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)

    def on_size(self, event):
        self.messages_list_ctrl.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER)
        event.Skip()

    def on_close_window(self, event):
        self.parent.detFramePosition = self.GetPosition()
        self.parent.detFrameSize = self.GetSize()
        if self.message_frame:
            self.message_frame.Close()
        self.Destroy()
        event.Skip()

    def show_details_frame(self, position, size):
        self.Refresh()
        self.SetMinSize((565, 160))
        self.SetSize(size)
        self.SetPosition(position)
        self.Show(True)

    def on_refresh(self, evt):
        self.unblock(False)
        indx = [i[0] for i in self.plugin.temp_data].index(self.setup[0])
        wt = self.plugin.temp_data[indx][3]
        wt.operate(True)
        evt.Skip()

    def on_show_button(self, evt):
        item = self.messages_list_ctrl.GetFirstSelected()
        if item == -1:
            return
        nbr = self.messages_list_ctrl.GetItemText(item)
        sel = [nbr]
        indexes = [i[0] for i in self.plugin.temp_data]
        indx = indexes.index(self.setup[0])
        message = self.realize_action(indx, sel, 1)  # 1 ~ mode 'show'
        if message:
            if self.message_frame:
                self.message_frame.Close()
            self.message_frame = MessageFrame(
                parent=self,
                message=message,
            )
            wx.CallAfter(
                self.message_frame.show_message_frame,
                position=self.mess_fram_position,
                size=self.mess_fram_size,
            )

    # noinspection PyUnusedLocal
    def on_close_button(self, evt):
        self.Close(True)

    def delete_emails(self, indx, sel, close=False):
        self.del_flag = True
        if close:
            self.message_frame.Close()
        else:
            if self.message_frame:
                num = self.message_frame.get_email_num()
                rec = self.plugin.temp_data[indx][2][int(num) - 1]
                if num in sel or rec[0] == rec[2]:
                    self.message_frame.Close()
                else:
                    self.message_frame.Enable(False)
        self.unblock(False)
        wt = self.plugin.temp_data[indx][3]
        wt.delete_action((indx, sel, 0, self))

    def on_delete_button(self, evt):
        item = self.messages_list_ctrl.GetFirstSelected()
        sel = []
        while item != -1:
            nbr = self.messages_list_ctrl.GetItemText(item)
            sel.append(nbr)
            item = self.messages_list_ctrl.GetNextSelected(item)
        indx = [i[0] for i in self.plugin.temp_data].index(self.setup[0])
        self.delete_emails(indx, sel)
        evt.Skip()

    @staticmethod
    def on_client_button(evt):
        evt.Skip()
        run_email_client()

    def list_selection(self, event=None):
        if self.message_frame:
            self.message_frame.Raise()
        self.menu_flag_s = self.messages_list_ctrl.GetSelectedItemCount() == 1
        self.show_button.Enable(self.menu_flag_s)
        self.menu_flag_d = self.messages_list_ctrl.GetFirstSelected() != -1
        self.delete_button.Enable(self.menu_flag_d)
        if event:
            event.Skip()

    def disappear(self):
        if self.del_flag:
            self.Show(False)
        else:
            self.Close()

    def res_del_flag(self):
        self.del_flag = False

    def is_close_req(self):
        return self.del_flag and not self.IsShown()

    def refresh_list(self, evt=None):
        if evt:
            evt.Skip()
        observ_name = self.setup[0]
        indx = [item[0] for item in self.plugin.temp_data].index(observ_name)
        self.messages_list_ctrl.DeleteAllItems()
        if int(wx.__version__.split('.', 1)[0]) < 4:
            for row, item in enumerate(self.plugin.temp_data[indx][2]):
                self.messages_list_ctrl.InsertStringItem(row, item[4])
                self.messages_list_ctrl.SetStringItem(row, 1, item[3])
                self.messages_list_ctrl.SetStringItem(row, 2, item[1])
                self.messages_list_ctrl.SetStringItem(row, 3, item[2])
        else:
            for row, item in enumerate(self.plugin.temp_data[indx][2]):
                self.messages_list_ctrl.InsertItem(row, item[4])
                self.messages_list_ctrl.SetItem(row, 1, item[3])
                self.messages_list_ctrl.SetItem(row, 2, item[1])
                self.messages_list_ctrl.SetItem(row, 3, item[2])
        self.SetTitle(self.plugin.text.detTitle % (self.setup[0], str(row)))
        label = self.parent.get_number()
        if label != row:
            self.parent.set_number(row)
        self.unblock(True)
        self.list_selection()

    def unblock(self, unblock):
        if unblock:
            colour = self.GetForegroundColour()
        else:
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        self.messages_list_ctrl.SetTextColour(colour)
        self.delete_button.Enable(unblock)
        self.refresh_button.Enable(unblock)
        self.client_button.Enable(unblock)
        self.close_button.Enable(unblock)
        self.show_button.Enable(unblock)
        self.messages_list_ctrl.Refresh()
        self.Enable(unblock)
        if self.message_frame:
            self.message_frame.unblock(unblock)

    # noinspection PyUnusedLocal
    def on_right_click(self, event):
        # make a menu
        menu = wx.Menu()
        # add some items
        if self.menu_flag_s:
            menu.Append(self.popupID1, self.text.popup[0])
        if self.menu_flag_d:
            menu.Append(self.popupID2, self.text.popup[1])
        menu.Append(self.popupID3, self.text.popup[2])
        menu.Append(self.popupID4, self.text.popup[3])
        menu.Append(self.popupID5, self.text.popup[4])
        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def realize_action(self, indx, sel, mode):
        if not sel:
            return
        global mailbox
        obs_data = self.plugin.temp_data[indx][2]
        # observ_name = self.plugin.temp_data[indx][0]
        result_message = None
        old_account = u''
        m = len(sel) - 1
        item = sel[m]
        ix = [i[4] for i in obs_data].index(item)
        iac = [cfg[0] for cfg in self.plugin.configs].index(obs_data[ix][3])
        account = self.plugin.configs[iac]
        while m > -1:
            while old_account == account:
                acc_id = obs_data[ix][5]
                if account[1] == 0:  # POP3
                    lst = mailbox.list()[1]
                    cnt = len(lst)
                    if cnt >= int(acc_id):
                        maxlines = 100  # ToDo :  MAXLINES choice
                        if mode == 0:
                            maxlines = 0  # Delete -> not need read
                        resp, txt, octets = mailbox.top(acc_id, maxlines)
                        if resp != '+OK':
                            resp, txt, octets = mailbox.retr(acc_id)
                        txt = "\n".join(txt)
                        msg = my_parser.parsestr(txt)
                        if 'Message-Id' in msg:
                            mess_id = msg['Message-Id']
                        else:
                            mess_id = parse_address(msg['From'])
                        if mess_id == obs_data[ix][0]:
                            if mode == 1:
                                result_message = get_parts(msg, True)
                                result_message[3] = indx
                                result_message[4] = sel
                            else:  # mode = 0 ~ delete
                                mailbox.dele(acc_id)

                else:  # IMAP
                    typ, txt = mailbox.select('INBOX')  # Folder selection
                    if txt[0]:
                        if mode == 1:
                            typ, txt = mailbox.fetch(acc_id, '(RFC822)')
                            mailbox.store(acc_id, "-FLAGS", '(\Seen)')  # Reset UNSEEN flag
                        else:
                            typ, txt = mailbox.fetch(acc_id, '(RFC822.HEADER)')
                        txt = txt[0][1]
                        msg = my_parser.parsestr(txt)
                        if 'Message-Id' in msg:
                            mess_id = msg['Message-Id']
                        else:
                            mess_id = parse_address(msg['From'])
                        if mess_id == obs_data[ix][0]:
                            if mode == 1:
                                result_message = get_parts(msg, True)
                                result_message[3] = indx
                                result_message[4] = sel
                            else:  # mode = 0 ~ delete
                                mailbox.store(acc_id, "+FLAGS", '(\Deleted)')
                m -= 1
                if m == -1:
                    break
                else:
                    item = sel[m]
                    ix = [i[4] for i in obs_data].index(item)
                    iac = [cfg[0] for cfg in self.plugin.configs].index(obs_data[ix][3])
                    account = self.plugin.configs[iac]

            if old_account != '':
                if account[1] == 0:  # POP
                    mailbox.quit()
                else:  # IMAP
                    mailbox.expunge()
                    mailbox.logout()
            if m == -1:
                break
            error = True
            while error:
                old_account = account
                server = account[5]
                port = account[6]
                user = account[7]
                password = self.pass_inc.data[account[0]]
                use_ssl = account[9] == 3
                error = False
                if account[1] == 0:  # POP
                    try:
                        if use_ssl:
                            mailbox = poplib.POP3_SSL(server, port)
                        else:
                            mailbox = poplib.POP3(server, port)
                    except IOError:
                        eg.PrintError(self.text.error0 + ' ' + self.text.error1 % (server, port))
                        error = True
                    else:
                        # mailbox.set_debuglevel(5)
                        try:
                            mailbox.user(user)
                            mailbox.pass_(password)
                        except poplib.error_proto, errmsg:
                            eg.PrintError(self.text.error0 + ' ' + str(errmsg))
                            error = True
                            mailbox.quit()

                else:  # IMAP
                    try:
                        if use_ssl:
                            mailbox = imaplib.IMAP4_SSL(server, port)
                        else:
                            mailbox = imaplib.IMAP4(server, port)
                    except IOError:
                        eg.PrintError(self.text.error2 + ' ' + self.text.error3 % (server, port))
                        error = True
                    else:
                        try:
                            mailbox.login(user, password)
                        except IOError:
                            eg.PrintError(self.text.error2 + ' ' + self.text.error4 % (user, server, port))
                            error = True
                            mailbox.logout()
                if error:
                    while old_account == account:
                        m -= 1
                        if m == -1:
                            error = False
                            break
                        else:
                            item = sel[m]
                            ix = [i[4] for i in obs_data].index(item)
                            iac = [cfg[0] for cfg in self.plugin.configs].index(obs_data[ix][3])
                            account = self.plugin.configs[iac]

        return result_message

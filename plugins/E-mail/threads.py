# coding=utf8

import imaplib
import poplib
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate
from threading import Thread, Event

import eg
from .utils import get_parts, my_parser, parse_address, parse_item


class SendMailThread(Thread):
    def __init__(
        self, plugin, subject, from_adr, to_adr, cc_adr,
        body, signature, to_name, references, message_id
    ):
        Thread.__init__(self, name="SendMailThread")
        self.plugin = plugin
        self.pass_smtp = self.plugin.pass_smtp
        self.subject = subject
        self.from_adr = from_adr
        self.to_adr = to_adr
        self.cc_adr = cc_adr
        self.body = body
        self.signature = signature
        self.to_name = to_name
        self.references = references
        self.message_id = message_id

    def run(self):
        subject = eg.ParseString(self.subject)
        from_adr = self.from_adr
        to_adr = eg.ParseString(self.to_adr)
        cc_adr = self.cc_adr
        body = eg.ParseString(self.body)
        text = self.plugin.text
        signature = eg.ParseString(self.signature)
        to_name = eg.ParseString(self.to_name)
        choices = [item[0] for item in self.plugin.texts]
        if signature in choices:
            indx = choices.index(signature)
            signature = self.plugin.texts[indx][1]
        else:
            signature = None
        from_adr = from_adr.split(' - ')[-1]
        indx = [item[0] for item in self.plugin.configs].index(from_adr)
        account = self.plugin.configs[indx]
        try:
            indx = [item[0] for item in self.plugin.servers].index(account[8])
        except (IndexError, ValueError):
            eg.PrintError(text.error5 % (account[8], self.plugin.servers[0][0]))
            indx = 0
        server = self.plugin.servers[indx]
        choices = [item[0] for item in self.plugin.groups]
        if cc_adr in choices:
            indx = choices.index(cc_adr)
            cc_adr = self.plugin.groups[indx][1]
        else:
            cc_adr = None

        header_charset = 'UTF-8'
        if signature is not None:
            body += '\n' if body[-1] != '\n' else ''
            body += signature
        for body_charset in 'US-ASCII', 'UTF-8':
            try:
                body.encode(body_charset)
            except UnicodeError:
                pass
            else:
                break
        sender_name = str(Header(unicode(account[2]), header_charset))
        recipient_name = str(Header(unicode(to_name), header_charset))
        msg = MIMEText(body.encode(body_charset), 'plain', body_charset)
        msg['From'] = formataddr((sender_name, account[3]))
        msg['To'] = formataddr((recipient_name, to_adr))
        if cc_adr is not None:
            msg['Cc'] = ','.join(cc_adr)
        msg['Subject'] = Header(unicode(subject), header_charset)
        msg["User-agent"] = "EventGhost %s" % eg.Version.string
        if account[4] != '':
            msg["Reply-to"] = formataddr((sender_name, account[4]))
        msg["Date"] = formatdate(None, True)  # return: Wed, 03 Dec 2008 13:17:35 +0100
        if self.message_id is not None:
            msg['In-Reply-To'] = self.message_id
            if self.references is None:
                msg['References'] = self.message_id + u'\r\n'
            else:
                msg['References'] = self.references + self.message_id + u'\r\n'
        case = server[3]  # secure connection ?
        try:
            if case < 3:
                smtp = smtplib.SMTP(server[1], server[2])
            else:
                smtp = smtplib.SMTP_SSL(server[1], server[2])
        except IOError:
            eg.PrintError(text.error6 + ' ' + text.error7 % (server[1], server[2]))
        else:
            try:
                if server[4]:  # secure authentication
                    # smtp.debuglevel = 5
                    capa = smtp.ehlo()
                    if case == 1 and 'STARTTLS' not in capa[-1].upper():
                        case = 0
                    if case == 0 or case == 3:
                        smtp.esmtp_features["auth"] = "LOGIN PLAIN"
                    else:
                        smtp.starttls()
                        smtp.ehlo()
                    password = self.pass_smtp.data[server[0]]
                    smtp.login(server[5], password)
                if cc_adr is None:
                    smtp.sendmail(account[3], to_adr, msg.as_string())
                else:
                    rcpnt = [to_adr]
                    rcpnt.extend(cc_adr)
                    smtp.sendmail(account[3], rcpnt, msg.as_string())
            except IOError:
                eg.PrintError(text.error6 + ' ' + text.error8)
            else:
                from_adr = formataddr((account[2], account[3]))
                eg.TriggerEvent('Sent', payload='%s: %s' % (from_adr, subject), prefix='E-mail')
            smtp.quit()


class DeleteEmail(Thread):
    def __init__(self, indx, sel, mode, parent):
        self.indx = indx
        self.sel = sel
        self.mode = mode
        self.parent = parent
        Thread.__init__(self, name='DeleteEmail')

    @eg.LogIt
    def run(self):
        self.parent.realize_action(self.indx, self.sel, self.mode)


class WorkThread(Thread):
    def __init__(self, plugin, setup, notify_frame):
        self.setup = setup
        Thread.__init__(self, name=self.setup[0].encode('unicode_escape') + '_W-Thread')
        self.plugin = plugin
        self.pass_inc = self.plugin.pass_inc
        self.configs = self.plugin.configs
        self.notify_frame = notify_frame
        self.run_flag = False
        self.abort = False
        self.refresh = False
        self.thread_flag = Event()
        self.del_args = None
        self.text = self.plugin.text
        self.close = False
        eg.Print(self.text.observStarts % self.setup[0])

    def is_running(self):
        return self.run_flag

    def delete_action(self, args):
        self.del_args = args
        if not self.run_flag:
            self.thread_flag.set()

    def operate(self, refresh=False):
        self.refresh = refresh or self.refresh
        if not self.run_flag:
            self.thread_flag.set()

    @eg.LogIt
    def abort_observation(self, close=False):
        self.abort = True
        self.close = close
        self.thread_flag.set()

    @eg.LogIt
    def run(self):
        while True:
            if self.abort:
                break
            self.run_flag = True
            if self.del_args is not None:
                self.del_args[3].realize_action(self.del_args[0], self.del_args[1], self.del_args[2])
                if self.del_args[3].is_close_req():
                    self.del_args[3].Close()
                else:
                    self.del_args[3].res_del_flag()
                self.del_args = None
                val, shift = self.check_emails()
                if self.setup[6]:  # Show notification Window
                    self.notify_frame.set_number(val)
                    if val > 0:
                        if not self.notify_frame.IsShown():
                            self.notify_frame.Show(True)
                    else:
                        self.notify_frame.disappear()
            else:
                val, shift = self.check_emails()
                if self.setup[6]:  # Show notification Window
                    if val == 0:
                        self.notify_frame.disappear()
                    elif shift or self.refresh:
                        self.notify_frame.set_number(val)
                        if not self.notify_frame.IsShown():
                            self.notify_frame.Show(True)
                if self.refresh:
                    self.refresh = False
                else:
                    if self.setup[7]:  # Trigger event
                        if val > 0 and shift:
                            if self.setup[8]:
                                eg.TriggerEvent(self.setup[3], payload=str(val), prefix='E-mail')
                            else:
                                eg.TriggerEvent(self.setup[3], prefix='E-mail')
            self.run_flag = False
            if self.abort:
                break
            if self.del_args is None:
                self.thread_flag.clear()
                self.thread_flag.wait()
        self.notify_frame.disappear(self.close)
        indx = [item[0] for item in self.plugin.temp_data].index(self.setup[0])
        self.plugin.temp_data[indx][1:] = [0, [], None, self.notify_frame]

    @staticmethod
    def create_one_record(data, account, nbr, rec_id):
        msg = my_parser.parsestr(data)
        if 'Message-Id' in msg:
            mess_id = msg['Message-Id']
        else:
            mess_id = parse_address(msg['From'])
        tmp_rec = [
            mess_id,  # 0
            parse_item(msg['Subject']),  # 1
            parse_address(msg['From']),  # 2
            account,  # 3
            str(nbr),  # 4
            rec_id,  # 5
        ]
        return tmp_rec

    @eg.LogIt
    def check_emails(self):
        acc_list = [n[0] for n in self.configs]
        accounts = []
        observ_name = self.setup[0]
        loop = 0
        count = 0
        while True:
            try:
                loop += 1
                indx = [item[0] for item in self.plugin.temp_data].index(observ_name)
                break
            except IndexError:
                pass
        for i in range(len(acc_list)):
            for item in self.setup[2]:
                if item == acc_list[i]:
                    accounts.append(i)
        nbr = 0
        if len(self.plugin.temp_data[indx][2]) > 0:
            id_list = [item[0] for item in self.plugin.temp_data[indx][2]]
        else:
            id_list = []
        count = 0
        tmp_data = []
        if self.setup[4] == 0:  # non-filter mode
            for i in accounts:
                account = self.configs[i]
                server = account[5]
                port = account[6]
                user = account[7]
                password = self.pass_inc.data[account[0]]
                use_ssl = account[9] == 3
                if account[1] == 0:  # POP
                    try:
                        if use_ssl:
                            mailbox = poplib.POP3_SSL(server, port)
                        else:
                            mailbox = poplib.POP3(server, port)
                    except IOError:
                        eg.PrintError(self.text.error0 + ' ' + self.text.error1 % (server, port))
                    else:
                        # mailbox.set_debuglevel(5)
                        try:
                            mailbox.user(user)
                            mailbox.pass_(password)
                            # capa = mailbox._longcmd('CAPA')[1]
                            # if 'STLS' in capa:
                            #    print 'STLS'
                            #    #mailbox._shortcmd('STLS')
                            lst = mailbox.list()[1]
                            cnt = len(lst)
                            if cnt > 0:
                                count += cnt
                            maxlines = 0
                            for msg in lst:
                                msg_id = msg.split(' ')[0]
                                resp, data, octets = mailbox.top(msg_id, maxlines)
                                if resp != '+OK':
                                    resp, data, octets = mailbox.retr(msg_id)
                                data = "\n".join(data)
                                nbr += 1
                                one_rec = self.create_one_record(data, account[0], nbr, msg_id)
                                tmp_data.append(one_rec)
                        except poplib.error_proto, errmsg:
                            eg.PrintError(self.text.error0 + ' ' + str(errmsg))
                        mailbox.quit()

                else:  # IMAP
                    try:
                        if use_ssl:
                            mailbox = imaplib.IMAP4_SSL(server, port)
                        else:
                            mailbox = imaplib.IMAP4(server, port)
                    except IOError:
                        eg.PrintError(self.text.error2 + ' ' + self.text.error3 % (server, port))
                    else:
                        try:
                            mailbox.login(user, password)
                        except IOError:
                            eg.PrintError(self.text.error2 + ' ' + self.text.error4 % (user, server, port))
                        else:
                            mailbox.select('INBOX')  # Folder selection
                            typ, data = mailbox.search(None, 'UNSEEN')
                            if data[0]:
                                lst = data[0].split()
                                count += len(lst)
                                for num in lst:
                                    typ, data = mailbox.fetch(num, '(RFC822.HEADER)')
                                    mailbox.store(num, "-FLAGS", '(\Seen)')  # Reset UNSEEN flag
                                    data = data[0][1]
                                    nbr += 1
                                    one_rec = self.create_one_record(data, account[0], nbr, num)
                                    tmp_data.append(one_rec)
                        mailbox.logout()

        else:  # filter mode
            def process_email(mbox, pe_data, pe_id_list, pe_account, pe_count, pe_id, pe_tmp_data):
                conds = [
                    "%s.find(%s)>-1",
                    "not %s.find(%s)>-1",
                    "%s==%s",
                    "not %s==%s",
                    "%s.startswith(%s)",
                    "%s.endswith(%s)"
                ]
                pe_msg = my_parser.parsestr(pe_data)
                parts = get_parts(pe_msg)
                flag = False
                if self.setup[4] == 1:  # filter AND mode
                    j = 0
                    while j < 6:
                        what, cond, strng = self.setup[5][j]
                        if what > 0 and not eval(conds[cond] % ('parts[what-1]', 'strng')):
                            break
                        j += 1
                    if j == 6:
                        flag = True
                else:  # filter OR mode
                    j = 0
                    while j < 6:
                        what, cond, strng = self.setup[5][j]
                        if what > 0 and eval(conds[cond] % ('parts[what-1]', 'strng')):
                            flag = True
                            break
                        j += 1
                if flag:
                    if 'Message-Id' in pe_msg:
                        mess_id = pe_msg['Message-Id']
                    else:
                        mess_id = parts[1]
                    if self.setup[11]:  # trigger event for each email ?
                        if mess_id not in pe_id_list:
                            itms = self.plugin.text.field_1[1:]
                            suff = self.setup[12]
                            if suff in itms:
                                suff = itms.index(suff)
                                suff = u"%s.%s" % (self.setup[12], parts[suff])
                            if self.setup[13] > 0:
                                eg.TriggerEvent(suff, payload=parts[self.setup[13] - 1], prefix='E-mail')
                            else:
                                eg.TriggerEvent(suff, prefix='E-mail')
                        if self.setup[14]:  # ~ delete
                            if pe_account[1] == 0:  # POP
                                mbox.dele(pe_id)
                                # if resp[:3]=='+OK':
                                #    print "deleted !!!"
                                #    notDeleted = False
                            else:
                                mbox.store(pe_id, "+FLAGS", '(\Deleted)')
                                # if resp[0] =='OK':
                                #    resp = mailbox.expunge()
                                #    if resp[0] =='OK':
                                #        print "deleted !!!"
                    pe_count += 1
                    # show notification window?
                    if not self.setup[14]:
                        tmp_rec = [
                            mess_id,  # 0 ID
                            parts[0],  # 1 Subject
                            parts[1],  # 2 From
                            pe_account[0],  # 3
                            str(pe_count),  # 4
                            pe_id,  # 5
                        ]
                        pe_tmp_data.append(tmp_rec)
                return pe_count, pe_tmp_data

            for i in accounts:
                account = self.configs[i]
                server = account[5]
                port = account[6]
                user = account[7]
                password = self.pass_inc.data[account[0]]
                use_ssl = account[9] == 3
                if account[1] == 0:  # POP
                    try:
                        if use_ssl:
                            mailbox = poplib.POP3_SSL(server, port)
                        else:
                            mailbox = poplib.POP3(server, port)
                    except IOError:
                        eg.PrintError(self.text.error0 + ' ' + self.text.error1 % (server, port))
                    else:
                        try:
                            mailbox.user(user)
                            mailbox.pass_(password)
                            lst = mailbox.list()[1]
                            cnt = len(lst)
                            if cnt > 0:
                                count = 0
                                for msg in lst:
                                    msg_id = msg.split(' ')[0]
                                    resp, data, octets = mailbox.retr(msg_id)
                                    data = "\n".join(data)
                                    count, tmp_data = process_email(
                                        mailbox, data, id_list, account, count, msg_id, tmp_data
                                    )
                        except poplib.error_proto, errmsg:
                            eg.PrintError(self.text.error0 + ' ' + str(errmsg))
                        mailbox.quit()

                else:  # IMAP
                    try:
                        if use_ssl:
                            mailbox = imaplib.IMAP4_SSL(server, port)
                        else:
                            mailbox = imaplib.IMAP4(server, port)
                    except IOError:
                        eg.PrintError(self.text.error2 + ' ' + self.text.error3 % (server, port))
                    else:
                        try:
                            mailbox.login(user, password)
                        except IOError:
                            eg.PrintError(self.text.error2 + ' ' + self.text.error4 % (user, server, port))
                        else:
                            mailbox.select('INBOX')  # Folder selection
                            typ, data = mailbox.search(None, 'UNSEEN')
                            if data[0]:
                                lst = data[0].split()
                                count = 0
                                for msg_id in lst:
                                    typ, data = mailbox.fetch(msg_id, '(RFC822)')
                                    mailbox.store(msg_id, "-FLAGS", '(\Seen)')  # Reset UNSEEN flag
                                    data = data[0][1]
                                    count, tmp_data = process_email(
                                        mailbox, data, id_list, account, count, msg_id, tmp_data
                                    )
                        mailbox.expunge()
                        mailbox.logout()
        count_old = self.plugin.temp_data[indx][1]
        shift = count != count_old
        count_old = count
        self.plugin.temp_data[indx][2] = tmp_data
        self.plugin.temp_data[indx][1] = count
        return count, shift


class ObservationThread(Thread):
    def __init__(self, setup, plugin, notify_frame, ):
        self.setup = setup
        Thread.__init__(self, name=self.setup[0].encode('unicode_escape') + '_O-Thread')
        self.plugin = plugin
        self.notify_frame = notify_frame
        self.observ_name = setup[0]
        self.abort = False
        self.last_check = 0
        self.thread_flag = Event()
        self.first_run = True
        self.wt = None

    def is_aborted(self):
        return self.abort

    @eg.LogIt
    def run(self):
        indx = 0
        if self.first_run:
            self.first_run = False
            while True:
                try:
                    if self.plugin.temp_data[indx][3] is not None:
                        wt = self.plugin.temp_data[indx][3]
                        if wt.isAlive():
                            wt.abort_observation()
                            self.thread_flag.wait(1)
                            self.thread_flag.clear()
                    else:
                        self.plugin.observ_threads[self.setup[0]] = self  # update dictionary
                        indx = [item[0] for item in self.plugin.temp_data].index(self.observ_name)
                        self.wt = WorkThread(plugin=self.plugin, setup=self.setup, notify_frame=self.notify_frame)
                        self.plugin.temp_data[indx][3] = self.wt
                        self.wt.start()
                        break
                except IOError:
                    self.plugin.observ_threads[self.setup[0]] = self  # update dictionary
                    indx = [item[0] for item in self.plugin.temp_data].index(self.observ_name)
                    print "create wt"
                    self.wt = WorkThread(plugin=self.plugin, setup=self.setup, notify_frame=self.notify_frame)
                    self.plugin.temp_data[indx][3] = self.wt
                    self.wt.start()
                    break
        while True:
            if self.abort:
                break
            self.last_check = time.time()
            self.wt.operate()
            self.thread_flag.wait(60 * self.setup[1])
            self.thread_flag.clear()

    @eg.LogIt
    def abort_observation(self, close=False):
        self.wt.abort_observation(close)
        self.abort = True
        self.thread_flag.set()

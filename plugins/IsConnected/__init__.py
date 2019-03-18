# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright Â© 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import eg


eg.RegisterPlugin(
    name=u'Is Connected',
    author=u'K',
    version=u'0.2b',
    description=u'Monitors a devices network connection',
    kind=u'other',
    canMultiLoad=False,
    createMacrosOnAdd=True,
    guid=u'{4E64F965-8378-48A3-A7AA-12ABBB0B0664}',
)

import threading # NOQA
import struct # NOQA
import ctypes # NOQA
import socket # NOQA
import time # NOQA
import string # NOQA
import re # NOQA
import random # NOQA
import select # NOQA
import wx # NOQA

HEADER_STRUCT_FORMAT = '>HHHHHH'
HEADER_STRUCT_SIZE = struct.calcsize(HEADER_STRUCT_FORMAT)


def _encode_name(name, type, scope=None):
    if name == '*':
        name = name + '\0' * 15
    elif len(name) > 15:
        name = name[:15] + chr(type)
    else:
        name = string.ljust(name, 15) + chr(type)

    def _do_first_level_encoding(m):
        l = ord(m.group(0))
        return string.uppercase[l >> 4] + string.uppercase[l & 0x0f]

    encoded_name = (
        chr(len(name) * 2) + re.sub('.', _do_first_level_encoding, name)
    )
    if scope:
        encoded_scope = ''
        for k in string.split(scope, '.'):
            encoded_scope = encoded_scope + chr(len(k)) + k
        return encoded_name + encoded_scope + '\0'
    else:
        return encoded_name + '\0'


def _prepare_netbios_query(trn_id, name, is_broadcast=True):
    header = struct.pack(
        HEADER_STRUCT_FORMAT,
        trn_id,
        (is_broadcast and 0x0110) or 0x0100,
        1,
        0,
        0,
        0
    )
    payload = _encode_name(name, 0x20) + '\x00\x20\x00\x01'

    return header + payload


def _poll_for_netbios_packet(sock, wait_trn_id, timeout):
    end_time = time.time() + timeout
    while True:
        try:
            _timeout = end_time - time.time()
            if _timeout <= 0:
                return None

            ready, _, _ = select.select([sock.fileno()], [], [], _timeout)
            if not ready:
                return None

            data, _ = sock.recvfrom(0xFFFF)
            if len(data) == 0:
                return None

            trn_id, ret = _decode_packet(data)

            if trn_id == wait_trn_id:
                if ret:
                    return ret

        except select.error, ex:
            if isinstance(ex, tuple):
                if ex[0] != errno.EINTR and ex[0] != errno.EAGAIN:
                    raise ex
            else:
                raise ex


def _decode_packet(data):
    if len(data) < HEADER_STRUCT_SIZE:
        raise Exception

    answer = struct.unpack(
        HEADER_STRUCT_FORMAT,
        data[:HEADER_STRUCT_SIZE]
    )
    trn_id, code = answer[:2]

    is_response = bool((code >> 15) & 0x01)
    opcode = (code >> 11) & 0x0F

    if opcode == 0x0000 and is_response:
        name_len = ord(data[HEADER_STRUCT_SIZE])
        offset = HEADER_STRUCT_SIZE + 2 + name_len + 8

        record_count = (struct.unpack('>H', data[offset:offset + 2])[0]) / 6

        offset += 4  # Constant 4 for the Data Length and Flags field
        ret = []
        for i in range(0, record_count):
            ret.append(
                '%d.%d.%d.%d' % struct.unpack('4B', (data[offset:offset + 4]))
            )
            offset += 6
        return trn_id, ret
    else:
        return trn_id, None


def _netbios_to_ip(netbios_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', 29567))
    trn_id = random.randint(1, 0xFFFF)
    data = _prepare_netbios_query(trn_id, netbios_name)
    sock.sendto(data, ('<broadcast>', 29567))

    return _poll_for_netbios_packet(sock, trn_id, 10)


def _validate_ip(ip):
    if len(ip.split('.')) == 4 and ip.replace('.', '').isdigit():
        return ip
    else:
        res = _get_ip_from_host(ip)
        if not res:
            return _netbios_to_ip(ip)
        else:
            return res


def _get_ip_from_host(hostname):
    try:
        res = socket.gethostbyname(socket.getfqdn(hostname))
    except:
        res = None

    return res


def _get_mac_address(ip_address):
    send_arp = ctypes.windll.Iphlpapi.SendARP
    inetaddr = ctypes.windll.wsock32.inet_addr(ip_address)

    hw_address = ctypes.c_buffer(6)
    addlen = ctypes.c_ulong(ctypes.sizeof(hw_address))

    send_arp(inetaddr, 0, ctypes.byref(hw_address), ctypes.byref(addlen))

    res = []

    for val in struct.unpack('BBBBBB', hw_address):
        if val > 15:
            replace_str = '0x'
        else:
            replace_str = 'x'

        res.append(hex(val).replace(replace_str, '').upper())

    return ':'.join(res)


class Thread(object):
    def __init__(self, plugin, client_name, host, interval, timeout):

        self._interval_event = threading.Event()
        self._timeout_event = threading.Event()
        self.plugin = plugin
        self.client_name = client_name
        self.interval = interval
        self.timeout = timeout
        self.host = host
        self.connected = None
        self._new_connection = False
        self._thread = None
        self._lock = threading.Lock()

    def start(self):
        while self._interval_event.isSet():
            pass

        if self._thread is None:
            self._thread = threading.Thread(
                name=__name__ + '.' + self.client_name,
                target=self.run
            )
            self._thread.start()

    def trigger_event(self, connected):
        change = self.connected != connected
        self.connected = connected
        suffix = self.client_name + '.'

        if change and connected:
                suffix += 'Connected'
        elif change:
            suffix += 'Disconnected'
        else:
            return

        self.plugin.TriggerEvent(suffix)

    def run(self):
        notice_ip = _validate_ip(self.host)

        if notice_ip and notice_ip != self.host:
            eg.Print(
                'Is Connected: '
                'Monitoring Started: '
                'Name: %s, '
                'Host Name: %s '
                'IP Address: %s '
                'MAC Address: %s' %
                (
                    self.client_name,
                    self.host,
                    notice_ip,
                    _get_mac_address(notice_ip)
                )
            )
        elif notice_ip == self.host:
            eg.Print(
                'Is Connected: '
                'Monitoring Started: '
                'Name: %s, '
                'IP Address: %s '
                'MAC Address: %s' %
                (self.client_name, notice_ip, _get_mac_address(notice_ip))
            )

        else:
            eg.Print(
                'Is Connected: '
                'Monitoring Started: '
                'Name: %s, '
                'Host Name: %s' %
                (self.client_name, self.host)
            )

        while not self._interval_event.isSet():
            ip = _validate_ip(self.host)

            def send_arp():
                self._lock.acquire()
                new_connection = False
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)

                while not self._timeout_event.isSet():
                    try:
                        sock.connect((ip, 56421))
                    except socket.timeout:
                        self._timeout_event.set()
                    except socket.error as err:
                        if err[0] == 10060:
                            new_connection = False
                        elif err[0] == 10061:
                            new_connection = True
                            self._timeout_event.set()
                        elif err[0] == 10022:
                            pass
                        else:
                            raise
                    else:
                        new_connection = True
                        self._timeout_event.set()
                    finally:
                        try:
                            sock.close()
                        except socket.error:
                            pass
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(self.timeout)

                self._lock.release()
                self.trigger_event(new_connection)

            t = threading.Thread(target=send_arp)
            t.start()

            self._timeout_event.wait(self.timeout)
            self._timeout_event.set()

            try:
                t.join(1)
            except:
                pass

            self._lock.acquire()
            self._lock.release()
            self._interval_event.wait(self.interval)
            self._timeout_event.clear()

        self._thread = None
        self._timeout_event.clear()
        self._interval_event.clear()

        eg.Print(
            'Is Connected: '
            'Monitoring Stopped: '
            'Name: %s' %
            self.client_name
        )

    def stop(self):
        if self._thread is not None:
            self._interval_event.set()
            self._timeout_event.set()
            self._thread.join(3)


class Config(eg.PersistentData):
    clients = []


class Text:
    # add variables with string that you want to be able to have translated
    # using the language editor in here

    class AddDevice:
        name = 'Add Device'
        description = 'Action Add Device'
        name_lbl = 'Client Name:'
        host_lbl = 'Host Name/IP Address:'
        interval_lbl = 'Time between checking (seconds):'
        timeout_lbl = 'How long to check (seconds):'
        modify_lbl = 'Modify existing client:'

    class RemoveDevice:
        name = 'Remove Device'
        description = 'Action Remove Device'
        name_lbl = 'Client Name:'


    class StartMonitoring:
        name = 'Start Monitoring'
        description = 'Action Start Monitoring'
        name_lbl = 'Client Name:'


    class StopMonitoring:
        name = 'Stop Monitoring'
        description = 'Action Stop Monitoring'
        name_lbl = 'Client Name:'


class IsConnected(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddAction(AddDevice)
        self.AddAction(RemoveDevice)
        self.AddAction(StartMonitoring)
        self.AddAction(StopMonitoring)
        self.threads = []

    def __start__(self):

        for client in Config.clients:
            t = Thread(self, *client)
            self.threads += [t]
            t.start()

    def __close__(self):
        pass

    def __stop__(self):
        for t in self.threads[:]:
            t.stop()

        del self.threads[:]

    def OnDelete(self):
        try:
            del Config
        except UnboundLocalError:
            pass


class AddDevice(eg.ActionBase):

    def __call__(
        self,
        name,
        host,
        interval,
        timeout,
        modify=False
    ):
        for client in Config.clients:
            if client[0] == name:
                if modify:
                    Config.clients.remove(client)
                    for t in self.plugin.threads:
                        if t.client_name == name:
                            t.stop()
                            self.plugin.threads.remove(t)
                else:
                    eg.PrintNotice(
                        'Is Connected: '
                        'A client with the name %s already exists.' %
                        name
                    )
                    return

        Config.clients += [(name, host, interval, timeout)]

        t = Thread(self.plugin, name, host, interval, timeout)
        self.plugin.threads += [t]
        t.start()

    def GetLabel(
        self,
        name='',
        host='',
        interval=5,
        timeout=0.25,
        modify=False
    ):
        name = 'Client Name: ' + name

        if host:
            ip = _validate_ip(host)
            if ip == host:
                host = 'IP: ' + host
            elif ip is not None:
                host = 'Host: ' + host
            else:
                host = 'Host: Invalid Host/IP'
        else:
            host = 'Host: '

        interval = 'Interval: %d' % interval
        timeout = 'Timeout: %0.2f' % timeout

        return self.name + ': %s %s %s %s' % (name, host, interval, timeout)

    def Configure(
        self,
        name='',
        host='',
        interval=5,
        timeout=0.25,
        modify=False
    ):
        text = self.text
        panel = eg.ConfigPanel()

        name_st = panel.StaticText(text.name_lbl)
        host_st = panel.StaticText(text.host_lbl)
        interval_st = panel.StaticText(text.interval_lbl)
        timeout_st = panel.StaticText(text.timeout_lbl)
        modify_st = panel.StaticText(text.modify_lbl)

        name_ctrl = panel.TextCtrl(name)
        host_ctrl = panel.TextCtrl(host)
        interval_ctrl = panel.SpinIntCtrl(interval, min=0, max=99)
        timeout_ctrl = panel.SpinNumCtrl(
            timeout,
            min=0.0,
            max=100.0,
            increment=0.05
        )

        modify_ctrl = wx.CheckBox(panel, -1, '')
        modify_ctrl.SetValue(modify)

        eg.EqualizeWidths(
            (name_st, host_st, interval_st, timeout_st, modify_st)
        )
        eg.EqualizeWidths(
            (name_ctrl, host_ctrl, interval_ctrl, timeout_ctrl)
        )

        def on_text(evt):

            def check():
                clients = list(client[0] for client in Config.clients)
                value = name_ctrl.GetValue()
                modify_ctrl.Enable(value in clients)

            if evt is not None:
                evt.Skip()
            wx.CallAfter(check)

        name_ctrl.Bind(wx.EVT_CHAR, on_text)

        on_text(None)

        def add(st, ctrl):
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(st, 0, wx.EXPAND | wx.ALL, 5)
            sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 5)
            panel.sizer.Add(sizer, 0, wx.EXPAND)

        add(name_st, name_ctrl)
        add(host_st, host_ctrl)
        add(interval_st, interval_ctrl)
        add(timeout_st, timeout_ctrl)
        add(modify_st, modify_ctrl)

        while panel.Affirmed():
            panel.SetResult(
                name_ctrl.GetValue(),
                host_ctrl.GetValue(),
                interval_ctrl.GetValue(),
                timeout_ctrl.GetValue(),
                modify_ctrl.GetValue()
            )


class ActionBase(eg.ActionBase):

    def __call__(self, name):
        raise NotImplementedError

    def Configure(self, name=''):
        text = self.text
        panel = eg.ConfigPanel()

        choices = sorted(list(t.client_name for t in self.plugin.threads))

        if name in choices:
            selected = choices.index(name)
        else:
            selected = 0

        name_st = panel.StaticText(text.name_lbl)
        name_ctrl = panel.Choice(value=selected, choices=choices)

        name_sizer = wx.BoxSizer(wx.HORIZONTAL)

        name_sizer.Add(name_st, 0, wx.EXPAND | wx.ALL, 5)
        name_sizer.Add(name_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(name_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(name_ctrl.GetStringSelection())


class RemoveDevice(ActionBase):

    def __call__(self, name):
        for client in Config.clients:
            if client[0] == name:
                Config.clients.remove(client)
                for t in self.plugin.threads:
                    if t.client_name == name:
                        t.stop()
                        self.plugin.threads.remove(t)


class StartMonitoring(ActionBase):

    def __call__(self, name):
        for t in self.plugin.threads:
            if t.client_name == name:
                t.start()


class StopMonitoring(ActionBase):

    def __call__(self, name):
        for t in self.plugin.threads:
            if t.client_name == name:
                t.stop()

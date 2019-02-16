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
    name='Shutdown Notifier',
    author='K',
    version='0.1b',
    description=(
        'Generates events if the system is shutting down.\n'
        '\n'
        'This plugin will generate one of the following events.\n'
        '\n'
        'ShutdownNotifier.SystemShutdown\n'
        'ShutdownNotifier.EventGhostShutdown\n'
        'ShutdownNotifier.LogOff\n'
        'ShutdownNotifier.EventGhostForcedClose\n'
        '\n'
        'If Windows calls for EG to shutdown there is an action that you '
        'can place an action that gets run by the shutdown event that will '
        'interrupt the system shutdown. You will also be able to do the '
        'same thing for not allowing the currently signed on user to logoff.'
    ),
    kind=u'other',
    canMultiLoad=False,
    createMacrosOnAdd=True,
    guid='{838EC869-AF28-4A5A-8DD5-6CC88E2C362A}',
)

import wx # NOQA
import ctypes # NOQA
from ctypes.wintypes import BOOL # NOQA
import threading # NOQA

user32 = ctypes.windll.User32
kernel32 = ctypes.windll.Kernel32

WM_QUERYENDSESSION = 0x00000011
WM_ENDSESSION = 0x00000016

ENDSESSION_SHUTDOWN = 0x00000000
ENDSESSION_CLOSEAPP = 0x00000001
ENDSESSION_LOGOFF = 0x80000000
ENDSESSION_CRITICAL = 0x40000000

MAX_STR_BLOCKREASON = 256


# BOOL ShutdownBlockReasonCreate(
#   HWND    hWnd,
#   LPCWSTR pwszReason
# );
ShutdownBlockReasonCreate = user32.ShutdownBlockReasonCreate
ShutdownBlockReasonCreate.restype = BOOL

# BOOL ShutdownBlockReasonDestroy(
#   HWND hWnd
# );
ShutdownBlockReasonDestroy = user32.ShutdownBlockReasonDestroy
ShutdownBlockReasonDestroy.restype = BOOL

# BOOL SetProcessShutdownParameters(
#   DWORD dwLevel,
#   DWORD dwFlags
# );

SetProcessShutdownParameters = kernel32.SetProcessShutdownParameters
SetProcessShutdownParameters.restype = BOOL


class Text(eg.TranslatableStrings):

    reason_default = 'EventGhost has stopped the system from shutting down'
    shutdown_block_error = (
        'This action can only be placed in a macro with the '
        'ShutdownNotifier.SystemShutdown event.'
    )
    logoff_block_error = (
        'This action can only be placed in a macro with the '
        'ShutdownNotifier.LogOff event.'
    )

    event_error = (
        'There is something that is holding up the '
        'shutdown process. You have a maximum of 3 seconds to '
        'process all actions.'
    )

    block_shutdown_clear_error = (
        'You need to run the "Clear Shutdown Block" action before running '
        'another "Block Shutdown" action'
    )

    class BlockShutdown:
        name = 'Block Shutdown'
        description = (
            'Blocks the system from shutting down.\n\n'
            'This action can only be placed in a macro that contains the \n\n'
            'ShutdownNotifier.SystemShutdown\n\n'
            'event. In this action you will be giving the availability to '
            'provide a message or reason for blocking the shutdown.'
        )
        reason_lbl = 'Block reason:'
        message_timeout_lbl = 'Clear message in '
        message_timeout_sfx = 'seconds'

    class BlockLogoff:
        name = 'Block Logoff'
        description = (
            'Blocks the currently logged in user from being able to logoff.'
        )
        block_logoff_msg = (
            'This action will block the logged in user from logging off.'
        )


class ShutdownNotifier(eg.PluginBase):
    text = Text

    def __init__(self):
        self._block_logoff = False
        self._block_shutdown = None
        self._block_timeout = None
        self._process_event = threading.Event()
        self._stop_event = threading.Event()

        self.AddAction(BlockShutdown)
        self.AddAction(BlockLogoff)

        self.shutdown_triggered = False
        self.should_veto = False

    def __start__(self):
        self.info.eventPrefix = 'ShutdownNotifier'
        self._block_logoff = False
        self._block_shutdown = None
        self._block_timeout = None
        self._process_event.clear()
        self._stop_event.clear()
        wx.CallAfter(self.register_notification)

    @eg.LogIt
    def register_notification(self):
        '''
        This method MUST be called form the main thread.
        Windows can get a little bit out of sorts and strange errors can occur
        if this method is not called form the main thread

        example to call from main thread
        wx.CallAfter(plugin_instance.register_notification)
        '''

        SetProcessShutdownParameters(0x280, 0)
        eg.app.Unbind(
            wx.EVT_QUERY_END_SESSION,
            handler=eg.app.OnQueryEndSessionVista
        )
        eg.app.Unbind(
            wx.EVT_END_SESSION,
            handler=eg.app.OnEndSession
        )
        eg.app.Bind(
            wx.EVT_QUERY_END_SESSION,
            self.OnQueryEndSession
        )
        eg.app.Bind(wx.EVT_END_SESSION, self.OnEndSession)

    def __stop__(self):
        wx.CallAfter(self.unregister_notification)

    @eg.LogIt
    def unregister_notification(self):
        '''
        This method MUST be called form the main thread.
        Windows can get a little bit out of sorts and strange errors can occur
        if this method is not called form the main thread

        example to call from main thread
        wx.CallAfter(plugin_instance.unregister_notification)
        '''


        eg.app.Unbind(
            wx.EVT_QUERY_END_SESSION,
            handler=self.OnQueryEndSession
        )

        eg.app.Unbind(
            wx.EVT_END_SESSION,
            handler=self.OnEndSession
        )

        eg.app.Bind(
            wx.EVT_QUERY_END_SESSION,
            eg.app.OnQueryEndSessionVista
        )
        eg.app.Bind(
            wx.EVT_END_SESSION,
            eg.app.OnEndSession
        )

        SetProcessShutdownParameters(0x0100, 0)

    def up_func(self):
        self._process_event.set()

    def block_shutdown(self, reason, timeout):
        self._block_shutdown = reason
        self._block_timeout = timeout
        self._process_event.set()

    def block_logoff(self):
        self._block_logoff = True
        self._process_event.set()

    def clear_block_shutdown(self):
        ShutdownBlockReasonDestroy(eg.messageReceiver.hwnd)
        self._block_shutdown = None
        self._block_timeout = None

    def message_timer(self, timeout):
        event = threading.Event()
        event.wait(timeout)
        wx.CallAfter(self.clear_block_shutdown)

    @eg.LogIt
    def OnQueryEndSession(self, event):
        if self.should_veto:
            self.should_veto = False
            event.Veto()
            return

        if self.shutdown_triggered:
            return

        if event.GetLoggingOff():
            self.shutdown_triggered = True

            self._process_event.clear()

            evt = self.TriggerEvent('LogOff')
            evt.AddUpFunc(self.up_func)

            self._process_event.wait(3.0)
            if not self._process_event.isSet():
                eg.PrintError(Text.event_error)

            else:
                block_logoff = self._block_logoff
                self._block_logoff = False

                if block_logoff:
                    self.shutdown_triggered = True
                    self.should_veto = True
                    event.Veto(True)
                else:
                    self.should_veto = False
                    eg.app.OnQueryEndSessionVista(event)
        else:
            self._process_event.clear()
            evt = self.TriggerEvent('SystemShutdown')
            evt.AddUpFunc(self.up_func)

            self._process_event.wait(3.0)

            if not self._process_event.isSet():
                eg.PrintError(Text.event_error)

            elif self._block_shutdown is not None:
                self.shutdown_triggered = True
                event.Veto(True)
                self.should_veto = True
                ShutdownBlockReasonCreate(
                    eg.messageReceiver.hwnd,
                    self._block_shutdown
                )

                threading.Thread(
                    target=self.message_timer,
                    args=(self._block_timeout,)
                ).start()
            else:
                self.should_veto = False
            eg.app.OnQueryEndSessionVista(event)

    def OnEndSession(self, event):
        eg.app.OnEndSession(event)


class BlockShutdown(eg.ActionBase):

    def __call__(self, reason='', message_timeout=5.0):
        if (
            eg.event.prefix == 'ShutdownNotifier' and
            eg.event.suffix == 'SystemShutdown'
        ):
            self.plugin.block_shutdown(reason, message_timeout)
        else:
            eg.PrintNotice(Text.shutdown_block_error)

    def Configure(
        self,
        reason=Text.reason_default,
        message_timeout=30.0
    ):
        text = self.text
        panel = eg.ConfigPanel()

        st = panel.StaticText(text.reason_lbl)
        ctrl = panel.TextCtrl(reason)
        timeout_st = panel.StaticText(text.message_timeout_lbl)
        timeout_suffix = panel.StaticText(text.message_timeout_sfx)
        timeout_ctrl = panel.SpinNumCtrl(
            value=message_timeout,
            min=0.0,
            increment=0.1
        )

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(st, 0, wx.EXPAND | wx.ALL, 5)
        sizer1.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(timeout_st, 0, wx.EXPAND | wx.ALL, 5)
        sizer2.Add(timeout_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        sizer2.Add(timeout_suffix, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(sizer1)
        panel.sizer.Add(sizer2)

        wx.CallAfter(panel.EnableButtons)

        while panel.Affirmed():
            panel.SetResult(ctrl.GetValue(), timeout_ctrl.GetValue())


class BlockLogoff(eg.ActionBase):

    # this code gets executed when the action gets run
    def __call__(self):

        if (
            eg.event.prefix == 'ShutdownNotifier' and
            eg.event.suffix == 'LogOff'
        ):
            self.plugin.block_logoff()
        else:
            eg.PrintNotice(Text.logoff_block_error)

    def Configure(self):
        text = self.text
        panel = eg.ConfigPanel()

        st = panel.StaticText(text.block_logoff_msg)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(st, 0, wx.EXPAND | wx.ALL, 5)
        sizer.AddStretchSpacer(1)

        panel.sizer.AddStretchSpacer(1)
        panel.sizer.Add(sizer)
        panel.sizer.AddStretchSpacer(1)

        wx.CallAfter(panel.EnableButtons)

        while panel.Affirmed():
            panel.SetResult()

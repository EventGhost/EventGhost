# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

from ..Utils import UpdateStartupShortcut
import os
import win32com.client

IID_ITask = "{148BD524-A2AB-11CE-B11F-00AA00530503}"

TASK_VALIDATE_ONLY = 0x1
TASK_CREATE = 0x2
TASK_UPDATE = 0x4
TASK_CREATE_OR_UPDATE = 0x6
TASK_DISABLE = 0x8
TASK_DONT_ADD_PRINCIPAL_ACE = 0x10
TASK_IGNORE_REGISTRATION_TRIGGERS = 0x20

TASK_ACTION_EXEC = 0x0
TASK_ACTION_COM_HANDLER = 0x5
TASK_ACTION_SEND_EMAIL = 0x6
TASK_ACTION_SHOW_MESSAGE = 0x7

TASK_RUN_NO_FLAGS = 0x0
TASK_RUN_AS_SELF = 0x1
TASK_RUN_IGNORE_CONSTRAINTS = 0x2
TASK_RUN_USE_SESSION_ID = 0x4
TASK_RUN_USER_SID = 0x8

TASK_LOGON_NONE = 0x0
TASK_LOGON_PASSWORD = 0x1
TASK_LOGON_S4U = 0x2
TASK_LOGON_INTERACTIVE_TOKEN = 0x3
TASK_LOGON_GROUP = 0x4
TASK_LOGON_SERVICE_ACCOUNT = 0x5
TASK_LOGON_INTERACTIVE_TOKEN_OR_PASSWORD = 0x6

TASK_TRIGGER_EVENT = 0x0
TASK_TRIGGER_TIME = 0x1
TASK_TRIGGER_DAILY = 0x2
TASK_TRIGGER_WEEKLY = 0x3
TASK_TRIGGER_MONTHLY = 0x4
TASK_TRIGGER_MONTHLYDOW = 0x5
TASK_TRIGGER_IDLE = 0x6
TASK_TRIGGER_REGISTRATION = 0x7
TASK_TRIGGER_BOOT = 0x8
TASK_TRIGGER_LOGON = 0x9
TASK_TRIGGER_SESSION_STATE_CHANGE = 0xB


class RegisterTask:
    def __init__(self):
        UpdateStartupShortcut(False)
        self.scheduler = win32com.client.Dispatch("Schedule.Service")
        self.scheduler.Connect(None, None, None, None)
        self.root = self.scheduler.GetFolder('\\')

    def IsEnabled(self):
        import eg
        from eg.WinApi import User
        username = User.NameSamCompatible().replace('\\', '-')

        try:
            task = self.root.GetTask("EventGhost Login " + username)
        except:
            return False

        executable = os.path.join(eg.mainDir, 'eventghost.exe')

        return (
            task.Enabled and
            task.Definition.Actions[0].Path == executable
        )

    def Enable(self, flag):
        import eg
        import wx
        from eg.WinApi import User

        user_name = User.NameSamCompatible()
        username = user_name.replace('\\', '-')

        class Dialog(eg.MessageDialog):

            def __init__(self):
                eg.MessageDialog.__init__(
                    self,
                    eg.document.frame,
                    "Please enter the password for user " + User.Name(),
                    "Enter User Password"
                )
                sizer = self.GetSizer()
                password_ctrl = wx.TextCtrl(self, -1, '', style=wx.TE_PASSWORD)
                sizer.Insert(1, password_ctrl, 1, wx.EXPAND | wx.ALL, 10)
                self.GetValue = password_ctrl.GetValue
                self.SetSizerAndFit(sizer)
                password_ctrl.SetFocus()

        dialog = Dialog()
        try:
            if dialog.ShowModal() == wx.ID_OK:
                password = dialog.GetValue()
            else:
                return
        finally:
            dialog.Destroy()

        boot_task = self.scheduler.NewTask(0)
        boot_trigger = boot_task.Triggers.Create(TASK_TRIGGER_BOOT)
        boot_trigger.Enabled = True
        boot_action = boot_task.Actions.Create(TASK_ACTION_EXEC)
        boot_action.ID = "EventGhost Boot"
        boot_action.Path = os.path.join(eg.mainDir, 'eventghost.exe')
        boot_action.WorkingDirectory = eg.mainDir
        boot_action.Arguments = '-event OnInitAfterBoot'
        boot_task.RegistrationInfo.Author = "EventGhost"
        boot_task.RegistrationInfo.Description = "EventGhost Boot"
        boot_task.Settings.Enabled = flag
        boot_task.Settings.Hidden = False
        boot_task.Settings.DisallowStartIfOnBatteries = False
        boot_task.Settings.StopIfGoingOnBatteries = False
        boot_task.Settings.ExecutionTimeLimit = ''

        login_task = self.scheduler.NewTask(0)
        login_trigger = login_task.Triggers.Create(TASK_TRIGGER_LOGON)
        login_trigger.Enabled = True
        login_trigger.UserId = user_name
        login_action = login_task.Actions.Create(TASK_ACTION_EXEC)
        login_action.ID = "EventGhost Login " + username
        login_action.Path = os.path.join(eg.mainDir, 'eventghost.exe')
        login_action.WorkingDirectory = eg.mainDir
        login_action.Arguments = ''
        login_task.RegistrationInfo.Author = "EventGhost"
        login_task.RegistrationInfo.Description = (
            "EventGhost Login " + username
        )
        login_task.Settings.Enabled = flag
        login_task.Settings.Hidden = False
        login_task.Settings.DisallowStartIfOnBatteries = False
        login_task.Settings.StopIfGoingOnBatteries = False
        login_task.Settings.ExecutionTimeLimit = ''

        class MessageFrame(wx.Frame):
            def __init__(self):
                wx.Frame.__init__(
                    self,
                    None,
                    title='EventGhost: Updating Scheduler',
                    style=wx.CAPTION | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR
                )
                ctrl = wx.StaticText(
                    self,
                    -1,
                    'Adding/Updating Task Scheduler Items. Please Wait....'
                )
                v_sizer = wx.BoxSizer(wx.VERTICAL)
                h_sizer = wx.BoxSizer(wx.HORIZONTAL)
                h_sizer.AddStretchSpacer()
                h_sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL, 20)
                h_sizer.AddStretchSpacer()
                v_sizer.AddStretchSpacer()
                v_sizer.Add(h_sizer, 0, wx.EXPAND)
                v_sizer.AddStretchSpacer()
                self.SetSizerAndFit(v_sizer)
                self.Show()

        dialog = MessageFrame()

        def run():
            self.root.RegisterTaskDefinition(
                "EventGhost Boot",
                boot_task,
                TASK_CREATE_OR_UPDATE,
                user_name,
                password,
                TASK_LOGON_PASSWORD
            )
            self.root.RegisterTaskDefinition(
                "EventGhost Login " + username,
                login_task,
                TASK_CREATE_OR_UPDATE,
                user_name,
                password,
                TASK_LOGON_PASSWORD
            )

            dialog.Destroy()
        wx.CallLater(100, run)

    def Delete(self):
        try:
            tasks = self.root.GetTasks(0)
            for task in tasks:
                if task.Name.startswith('EventGhost'):
                    self.root.DeleteTask(task.Name, 0)
        except:
            pass


RegisterTask = RegisterTask()

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


import eg
import os
import win32com.client

IID_ITask = "{148BD524-A2AB-11CE-B11F-00AA00530503}"

TASK_CREATE = 2
TASK_CREATE_OR_UPDATE = 6
TASK_ACTION_EXEC = 0

TASK_RUN_NO_FLAGS = 0
TASK_RUN_AS_SELF = 1
TASK_RUN_IGNORE_CONSTRAINTS = 2
TASK_RUN_USE_SESSION_ID = 4
TASK_RUN_USER_SID = 8

TASK_LOGON_NONE = 0
TASK_LOGON_PASSWORD = 1
TASK_LOGON_S4U = 2
TASK_LOGON_INTERACTIVE_TOKEN = 3
TASK_LOGON_GROUP = 4
TASK_LOGON_SERVICE_ACCOUNT = 5
TASK_LOGON_INTERACTIVE_TOKEN_OR_PASSWORD = 6

TASK_TRIGGER_EVENT = 0
TASK_TRIGGER_TIME = 1
TASK_TRIGGER_DAILY = 2
TASK_TRIGGER_WEEKLY = 3
TASK_TRIGGER_MONTHLY = 4
TASK_TRIGGER_MONTHLYDOW = 5
TASK_TRIGGER_IDLE = 6
TASK_TRIGGER_REGISTRATION = 7
TASK_TRIGGER_BOOT = 8
TASK_TRIGGER_LOGON = 9
TASK_TRIGGER_SESSION_STATE_CHANGE = 11


class RegisterTask:
    def __init__(self):
        print 'starting task register'
        self.scheduler = win32com.client.Dispatch("Schedule.Service")
        self.scheduler.Connect(None, None, None, None)
        self.root = self.scheduler.GetFolder("\\")

    def IsEnabled(self):
        tasks = self.root.GetTasks(0)

        for task in tasks:
            print task.Name
            if task.Name == 'EventGhost':
                return task.Enabled
        return False

    def Enable(self, flag):
        task = self.scheduler.NewTask(0)
        trigger = task.Triggers.Create(TASK_TRIGGER_BOOT)
        trigger.Enabled = True
        action = task.Actions.Create(TASK_ACTION_EXEC)
        action.ID = "EventGhost"
        action.Path = os.path.join(eg.mainDir, 'eventghost.exe')
        action.WorkingDirectory = eg.mainDir
        action.Arguments = '-event OnInitAfterBoot'
        task.RegistrationInfo.Author = "EventGhost"
        task.RegistrationInfo.Description = "EventGhost Startup"
        task.Settings.Enabled = flag
        task.Settings.Hidden = False

        self.root.RegisterTaskDefinition(
            "EventGhost",
            task,
            TASK_CREATE_OR_UPDATE,
            "",
            "",
            TASK_LOGON_NONE
        )
        # task = self.root.GetTask("EventGhost")
        # task.Enabled = flag




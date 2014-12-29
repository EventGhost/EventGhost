# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

import eg
import wx
from os.path import basename
from threading import Thread
from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW, PIPE, Popen
from os import devnull


def popen(cmd, si):
    return Popen(
        'cmd /C %s' % cmd,
        stdout = PIPE,
        stderr = open(devnull),
        startupinfo = si,
        shell = False
    )


class Command(eg.ActionBase):
    name = "Windows Command"
    description = "Executes a single Windows Command Line statement."
    iconFile = "icons/Execute"
    class text:
        label = "Windows Command: %s"
        Command = "Command Line:"
        waitCheckbox = "Wait until command is terminated before proceeding"
        eventCheckbox = "Trigger event when command is terminated"
        eventSuffix = "WindowsCommand"
        disableParsing = "Disable parsing of string"
        additionalSuffix = "Additional Suffix:"
        payload = "The result to use as payload"


    def __call__(
        self,
        command = '',
        waitForCompletion = True,
        triggerEvent = False,
        additionalSuffix = "",
        disableParsingCommand = True,
        disableParsingAdditionalSuffix = True,
        payload = False,
    ):
        prefix = self.plugin.info.eventPrefix
        suffix = self.text.eventSuffix
        if additionalSuffix != "":
            suffix = "%s.%s" % (suffix, additionalSuffix)
        if not disableParsingCommand:
            command = eg.ParseString(command)
        if not disableParsingAdditionalSuffix:
            additionalSuffix = eg.ParseString(additionalSuffix)
        si = STARTUPINFO()
        si.dwFlags |= STARTF_USESHOWWINDOW
        if waitForCompletion:
            proc = popen("chcp", si) #DOS console codepage
            data = proc.communicate()[0]
            if not proc.returncode:
                cp = "cp" + data.split()[-1].replace(".","")
                proc = popen(command, si)
                data = proc.communicate()[0]
                if not proc.returncode:
                    data = data.decode(cp)
                    if triggerEvent:
                        if payload:
                            eg.TriggerEvent(
                                suffix,
                                prefix = prefix,
                                payload = data.rstrip()
                            )
                        else:
                            eg.TriggerEvent(suffix, prefix = prefix)
                    return data.rstrip()
        elif triggerEvent:
            te = self.TriggerEvent(command, si, suffix, prefix, payload)
            te.start()
        else:
            proc = popen(command, si)


    class TriggerEvent(Thread):

        def __init__(self, cmd, si, suffix, prefix, pld):
            Thread.__init__(self)
            self.cmd = cmd
            self.si = si
            self.suffix = suffix
            self.prefix = prefix
            self.pld = pld

        def run(self):
            proc = popen("chcp", self.si) #DOS console codepage
            data = proc.communicate()[0]
            if not proc.returncode:
                cp = "cp" + data.split()[-1].replace(".","")
                proc = popen(self.cmd, self.si)
                data = proc.communicate()[0]
                if not proc.returncode:
                    data = data.decode(cp)
                    if self.pld:
                        eg.TriggerEvent(
                            self.suffix,
                            prefix = self.prefix,
                            payload = data.rstrip()
                        )
                    else:
                        eg.TriggerEvent(self.suffix, prefix = self.prefix)


    def GetLabel(self, command = '', *dummyArgs):
        return self.text.label % basename(command)


    def Configure(
        self,
        command = '',
        waitForCompletion = True,
        triggerEvent = False,
        additionalSuffix = "",
        disableParsingCommand = True,
        disableParsingAdditionalSuffix = False,
        payload = False,
    ):
        panel = eg.ConfigPanel()
        text = self.text
        commandCtrl = panel.TextCtrl(command)
        disableParsingCommandBox = panel.CheckBox(
            bool(disableParsingCommand),
            text.disableParsing
        )
        waitCheckBox = panel.CheckBox(
            bool(waitForCompletion),
            text.waitCheckbox
        )
        eventCheckBox = panel.CheckBox(
            bool(triggerEvent),
            text.eventCheckbox
        )
        pldCheckBox = panel.CheckBox(
            bool(payload),
            text.payload
        )
        additionalSuffixCtrl = panel.TextCtrl(additionalSuffix)
        disableParsingAdditionalSuffixBox = panel.CheckBox(
            bool(disableParsingAdditionalSuffix),
            text.disableParsing
        )

        SText = panel.StaticText
        lowerSizer2 = wx.GridBagSizer(2, 0)
        lowerSizer2.AddGrowableCol(1)
        lowerSizer2.AddGrowableCol(3)
        stTxt = SText(text.additionalSuffix)
        lowerSizer2.AddMany([
            ((eventCheckBox), (0, 0), (1, 1), wx.ALIGN_BOTTOM),
            ((1, 1), (0, 1), (1, 1), wx.EXPAND),
            (pldCheckBox, (0, 2), (1, 1)),
            (stTxt, (1, 2), (1, 1), wx.ALIGN_BOTTOM),
            (additionalSuffixCtrl, (2, 2)),
            (disableParsingAdditionalSuffixBox, (3, 2)),
            ((1, 1), (0, 3), (1, 1), wx.EXPAND),
        ])
        
        def onEventCheckBox(evt = None):
            enable = eventCheckBox.GetValue()
            stTxt.Enable(enable)
            additionalSuffixCtrl.Enable(enable)
            disableParsingAdditionalSuffixBox.Enable(enable)
            disableParsingAdditionalSuffixBox.SetValue(enable)
            pldCheckBox.Enable(enable)
            if not enable:
                additionalSuffixCtrl.ChangeValue("")
            if evt:
                pldCheckBox.SetValue(False)
                evt.Skip()
        eventCheckBox.Bind(wx.EVT_CHECKBOX, onEventCheckBox)
        onEventCheckBox()
        
        panel.sizer.AddMany([
            (SText(text.Command)),
            ((1, 2)),
            (commandCtrl, 0, wx.EXPAND),
            ((1, 2)),
            (disableParsingCommandBox),
            ((10, 15)),
            (waitCheckBox),
            ((10, 8)),
            (lowerSizer2, 0, wx.EXPAND),
        ])

        while panel.Affirmed():
            panel.SetResult(
                commandCtrl.GetValue(),
                waitCheckBox.GetValue(),
                eventCheckBox.GetValue(),
                additionalSuffixCtrl.GetValue(),
                disableParsingCommandBox.GetValue(),
                disableParsingAdditionalSuffixBox.GetValue(),
                pldCheckBox.GetValue()
            )


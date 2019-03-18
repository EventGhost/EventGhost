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
import wx
from types import ClassType


class RemoteUserInput(eg.ActionBase):

    def __call__(self):
        self.plugin.EnterNumber(self.value)


class ToggleInput(eg.ActionBase):

    def __call__(self):
        self.plugin.userInput = not self.plugin.userInput


class SendCommand(eg.ActionBase):

    def __call__(self, *args):
        user, comm = self.value

        inputSets = self.GetInputSets(user)
        if inputSets:
            if args and len(args) == len(inputSets):
                sendCommand = []
                for i, arg in enumerate(args):
                    if arg.isdigit() and len(arg) == inputSets[i]:
                        sendCommand.extend(list(arg))

                user = list(user)
                for i, char in enumerate(user):
                    if char == '*':
                        try:
                            user[i] = sendCommand.pop(0)
                        except IndexError:
                            break

                user = ''.join(user)
                if '*' not in user:
                    return self.plugin.sendCommand(user)

            values = self.UserInput(inputSets, panel=None)
            self.__call__(*values)
        else:
            self.plugin.sendCommand(comm)

    def Configure(self, *args):
        user = self.value[0]

        if '*' in user or args:
            panel = eg.ConfigPanel()

            if args:
                GetResults = self.UserInput(args, panel=panel)
            else:
                inputSets = self.GetInputSets(user)
                GetResults = self.UserInput(inputSets, panel=panel)

            while panel.Affirmed():
                panel.SetResult(*GetResults())

        else:
            eg.ActionBase.Configure(self)

    def GetInputSets(self, user):
        inputSets = []
        for char in user:
            if char == '*':
                if not inputSets:
                    inputSets.append(0)
                inputSets[len(inputSets) - 1] += 1
            elif inputSets and inputSets[len(inputSets) - 1]:
                inputSets.append(0)
        return inputSets

    def UserInput(self, inputLengths, panel=None):
        inputLengths = list(inputLengths)
        if panel is None:
            parent = wx.Dialog(None)
        else:
            parent = panel

        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        vSizer1 = wx.BoxSizer(wx.VERTICAL)
        vSizer2 = wx.BoxSizer(wx.VERTICAL)

        if panel is None:
            buttonRow = eg.ButtonRow(parent, (wx.ID_OK, wx.ID_CANCEL))
        else:
            buttonRow = panel.dialog.buttonRow

        widgets = ()

        def ButtonEnable(flag):
            if panel is not None:
                buttonRow.testButton.Enable(flag)
                buttonRow.applyButton.Enable(flag)
            buttonRow.okButton.Enable(flag)

        def MoveCursor(inputLength):
            import win32api
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('{RIGHT}' * inputLength)

        def Fields(inputLength):

            if isinstance(inputLength, int):
                ctrl = wx.TextCtrl(parent, -1, '')
                ButtonEnable(False)
            else:
                user = self.value[0]
                inputSets = self.GetInputSets(user)

                label = inputLength
                idx = inputLengths.index(inputLength)
                inputLengths[idx] = len(inputLength)
                inputLength = inputLengths[idx]

                if label.isdigit() and len(label) == inputSets[idx]:
                    ctrl = wx.TextCtrl(parent, -1, label)
                    ButtonEnable(True)
                else:
                    return Fields(inputSets[idx])

            MoveCursor(inputLength)

            vSizer1.Add(ctrl, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            def OnText(evt):
                value = ctrl.GetValue().strip()
                if len(value) > inputLength:
                    value = value[len(value) - inputLength:]
                    ctrl.SetValue(value)
                    MoveCursor(inputLength)
                try:
                    tmp = int(value)
                except ValueError:
                    value = list(value)
                    newValue = ''
                    for char in value:
                        if not char.isdigit():
                            char = ''
                        newValue += char
                    if newValue != value:
                        ctrl.SetValue(newValue)
                        MoveCursor(inputLength)
                enable = None
                for i, widget in enumerate(widgets):
                    def GetEnable():
                        return (
                            len(widget.GetValue().strip()) == inputLengths[i]
                        )
                    if enable is None:
                        enable = GetEnable()
                    else:
                        enable = enable and GetEnable()

                buttonRow.okButton.Enable(enable)
                if panel is not None:
                    buttonRow.testButton.Enable(enable)
                    buttonRow.applyButton.Enable(enable)

                evt.Skip()
            ctrl.Bind(wx.EVT_TEXT, OnText)

            return ctrl

        vSizer1.AddStretchSpacer()

        for inputLen in inputLengths:
            widgets += (Fields(inputLen),)

        vSizer1.AddStretchSpacer()

        hSizer.AddStretchSpacer()
        hSizer.Add(vSizer1, wx.EXPAND)
        hSizer.AddStretchSpacer()
        vSizer2.Add(hSizer, wx.EXPAND | wx.ALL, 10)

        parent.SetSizer(vSizer2)

        def GetResults():
            res = []
            for widget in widgets:
                res.append(widget.GetValue().strip())
            return res

        if panel is None:
            vSizer2.Add(buttonRow.sizer)

            def OnCancel(evt):
                parent.EndModal(wx.ID_CANCEL)

            def OnOk(evt):
                parent.EndModal(wx.ID_OK)

            buttonRow.OkButton.Bind(wx.EVT_BUTTON, OnOk)
            buttonRow.CancelButton.Bind(wx.EVT_BUTTON, OnCancel)
            parent.Bind(wx.EVT_CLOSE, OnCancel)

            answer = parent.ShowModal()
            userInput = GetResults()
            parent.Destroy()
            if answer == wx.ID_OK:
                res = userInput
            else:
                res = None
        else:
            res = GetResults
        return res


ACTIONS = (
    (eg.ActionGroup, 'gpMaster', 'Master', 'Master', (
        (eg.ActionGroup, 'gpPower', 'Power', 'Power', (
            (SendCommand, 'fnPWON', 'Master Power On', 'Master Power On', ['PWON', 'PWON']),
            (SendCommand, 'fnPWSTANDBY', 'Master Power Standby', 'Master Power Standby', ['PWSTANDBY', 'PWSTANDBY']),
            (SendCommand, 'fnPWSTATUS', 'Master Power Status', 'Master Power Status', ['PW?', 'PW?']),
        )),
    )),
    (eg.ActionGroup, 'gpMainZone', 'Main Zone', 'Main Zone', (
        (eg.ActionGroup, 'gpVolume', 'Volume', 'Volume', (
            (SendCommand, 'fnMVUP', 'Main Zone Volume Up', 'Main Zone Volume Up', ['MVUP', 'MVUP']),
            (SendCommand, 'fnMVDOWN', 'Main Zone Volume Down', 'Main Zone Volume Down', ['MVDOWN', 'MVDOWN']),
            (SendCommand, 'fnMVINPUT', 'Main Zone Volume Input', 'Main Zone Volume Input', ['MV**', 'MV**']),
            (SendCommand, 'fnMVSTATUS', 'Main Zone Volume Status', 'Main Zone Volume Status', ['MV?', 'MV?']),
        )),
        (eg.ActionGroup, 'gpChannelVolume', 'Channel Volume', 'Channel Volume', (
            (eg.ActionGroup, 'gpFrontLeft', 'Front Left', 'Front Left', (
                (SendCommand, 'fnCVFL_UP', 'Main Zone Channel Volume Front Left Up', 'Main Zone Channel Volume Front Left Up', ['CVFL UP', 'CVFL UP']),
                (SendCommand, 'fnCVFL_DOWN', 'Main Zone Channel Volume Front Left Down', 'Main Zone Channel Volume Front Left Down', ['CVFL DOWN', 'CVFL DOWN']),
                (SendCommand, 'fnCVFL_INPUT', 'Main Zone Channel Volume Front Left Input', 'Main Zone Channel Volume Front Left Input', ['CVFL **', 'CVFL 50']),
            )),
            (eg.ActionGroup, 'gpFrontRight', 'Front Right', 'Front Right', (
                (SendCommand, 'fnCVFR_UP', 'Main Zone Channel Volume Front Right Up', 'Main Zone Channel Volume Front Right Up', ['CVFR UP', 'CVFR UP']),
                (SendCommand, 'fnCVFR_DOWN', 'Main Zone Channel Volume Front Right Down', 'Main Zone Channel Volume Front Right Down', ['CVFR DOWN', 'CVFR DOWN']),
                (SendCommand, 'fnCVFR_INPUT', 'Main Zone Channel Volume Front Right Input', 'Main Zone Channel Volume Front Right Input', ['CVFR **', 'CVFR 50']),
            )),
            (eg.ActionGroup, 'gpCenter', 'Center', 'Center', (
                (SendCommand, 'fnCVC_UP', 'Main Zone Channel Volume Center Up', 'Main Zone Channel Volume Center Up', ['CVC UP', 'CVC UP']),
                (SendCommand, 'fnCVC_DOWN', 'Main Zone Channel Volume Center Down', 'Main Zone Channel Volume Center Down', ['CVC DOWN', 'CVC DOWN']),
                (SendCommand, 'fnCVC_INPUT', 'Main Zone Channel Volume Center Input', 'Main Zone Channel Volume Center Input', ['CVC **', 'CVC 50']),
            )),
            (eg.ActionGroup, 'gpSurroundLeft', 'Surround Left', 'Surround Left', (
                (SendCommand, 'fnCVSL_UP', 'Main Zone Channel Volume Surround Left Up', 'Main Zone Channel Volume Surround Left Up', ['CVSL UP', 'CVSL UP']),
                (SendCommand, 'fnCVSL_DOWN', 'Main Zone Channel Volume Surround Left Down', 'Main Zone Channel Volume Surround Left Down', ['CVSL DOWN', 'CVSL DOWN']),
                (SendCommand, 'fnCVSL_INPUT', 'Main Zone Channel Volume Surround Left Input', 'Main Zone Channel Volume Surround Left Input', ['CVSL **', 'CVSL 50']),
            )),
            (eg.ActionGroup, 'gpSurroundRight', 'Surround Right', 'Surround Right', (
                (SendCommand, 'fnCVSR_UP', 'Main Zone Channel Volume Surround Right Up', 'Main Zone Channel Volume Surround Right Up', ['CVSR UP', 'CVSR UP']),
                (SendCommand, 'fnCVSR_DOWN', 'Main Zone Channel Volume Surround Right Down', 'Main Zone Channel Volume Surround Right Down', ['CVSR DOWN', 'CVSR DOWN']),
                (SendCommand, 'fnCVSR_INPUT', 'Main Zone Channel Volume Surround Right Input', 'Main Zone Channel Volume Surround Right Input', ['CVSR **', 'CVSR 50']),
            )),
            (eg.ActionGroup, 'gpSurroundBackLeft', 'Surround Back Left', 'Surround Back Left', (
                (SendCommand, 'fnCVSBL_UP', 'Main Zone Channel Volume Surround Back Left Up', 'Main Zone Channel Volume Surround Back Left Up', ['CVSBL UP', 'CVSBL UP']),
                (SendCommand, 'fnCVSBL_DOWN', 'Main Zone Channel Volume Surround Back Left Down', 'Main Zone Channel Volume Surround Back Left Down', ['CVSBL DOWN', 'CVSBL DOWN']),
                (SendCommand, 'fnCVSBL_INPUT', 'Main Zone Channel Volume Surround Back Left Input', 'Main Zone Channel Volume Surround Back Left Input', ['CVSBL **', 'CVSBL 50']),
            )),
            (eg.ActionGroup, 'gpSurroundBackRight', 'Surround Back Right', 'Surround Back Right', (
                (SendCommand, 'fnCVSBR_UP', 'Main Zone Channel Volume Surround Back Right Up', 'Main Zone Channel Volume Surround Back Right Up', ['CVSBR UP', 'CVSBR UP']),
                (SendCommand, 'fnCVSBR_DOWN', 'Main Zone Channel Volume Surround Back Right Down', 'Main Zone Channel Volume Surround Back Right Down', ['CVSBR DOWN', 'CVSBR DOWN']),
                (SendCommand, 'fnCVSBR_INPUT', 'Main Zone Channel Volume Surround Back Right Input', 'Main Zone Channel Volume Surround Back Right Input', ['CVSBR **', 'CVSBR 50']),
            )),
            (eg.ActionGroup, 'gpSurroundBack', 'Surround Back', 'Surround Back', (
                (SendCommand, 'fnCVSB_UP', 'Main Zone Channel Volume Surround Back Up', 'Main Zone Channel Volume Surround Back Up', ['CVSB UP', 'CVSB UP']),
                (SendCommand, 'fnCVSB_DOWN', 'Main Zone Channel Volume Surround Back Down', 'Main Zone Channel Volume Surround Back Down', ['CVSB DOWN', 'CVSB DOWN']),
                (SendCommand, 'fnCVSB_INPUT', 'Main Zone Channel Volume Surround Back Input', 'Main Zone Channel Volume Surround Back Input', ['CVSB **', 'CVSB 50']),
            )),
            (eg.ActionGroup, 'gpSubwoofer', 'Subwoofer', 'Subwoofer', (
                (SendCommand, 'fnCVSW_UP', 'Main Zone Channel Volume Subwoofer Up', 'Main Zone Channel Volume Subwoofer Up', ['CVSW UP', 'CVSW UP']),
                (SendCommand, 'fnCVSW_DOWN', 'Main Zone Channel Volume Subwoofer Down', 'Main Zone Channel Volume Subwoofer Down', ['CVSW DOWN', 'CVSW DOWN']),
                (SendCommand, 'fnCVSW_INPUT', 'Main Zone Channel Volume Subwoofer Input', 'Main Zone Channel Volume Subwoofer Input', ['CVSW **', 'CVSW 50']),
            )),
            (eg.ActionGroup, 'gpSubwoofer2', 'Subwoofer 2', 'Subwoofer 2', (
                (SendCommand, 'fnCVSW2_UP', 'Main Zone Channel Volume Subwoofer 2 Up', 'Main Zone Channel Volume Subwoofer 2 Up', ['CVSW2 UP', 'CVSW2 UP']),
                (SendCommand, 'fnCVSW2_DOWN', 'Main Zone Channel Volume Subwoofer 2 Down', 'Main Zone Channel Volume Subwoofer 2 Down', ['CVSW2 DOWN', 'CVSW2 DOWN']),
                (SendCommand, 'fnCVSW2_INPUT', 'Main Zone Channel Volume Subwoofer 2 Input', 'Main Zone Channel Volume Subwoofer 2 Input', ['CVSW2 **', 'CVSW2 50']),
            )),
            (eg.ActionGroup, 'gpLeftFrontHeight', 'Left Front Height', 'Left Front Height', (
                (SendCommand, 'fnCVFHL_UP', 'Main Zone Channel Volume Left Front Height Up', 'Main Zone Channel Volume Left Front Height Up', ['CVFHL UP', 'CVFHL UP']),
                (SendCommand, 'fnCVFHL_DOWN', 'Main Zone Channel Volume Left Front Height Down', 'Main Zone Channel Volume Left Front Height Down', ['CVFHL DOWN', 'CVFHL DOWN']),
                (SendCommand, 'fnCVFHL_INPUT', 'Main Zone Channel Volume Left Front Height Input', 'Main Zone Channel Volume Left Front Height Input', ['CVFHL **', 'CVFHL 50']),
            )),
            (eg.ActionGroup, 'gpRightFrontHeight', 'Right Front Height', 'Right Front Height', (
                (SendCommand, 'fnCVFHR_UP', 'Main Zone Channel Volume Right Front Height Up', 'Main Zone Channel Volume Right Front Height Up', ['CVFHR UP', 'CVFHR UP']),
                (SendCommand, 'fnCVFHR_DOWN', 'Main Zone Channel Volume Right Front Height Down', 'Main Zone Channel Volume Right Front Height Down', ['CVFHR DOWN', 'CVFHR DOWN']),
                (SendCommand, 'fnCVFHR_INPUT', 'Main Zone Channel Volume Right Front Height Input', 'Main Zone Channel Volume Right Front Height Input', ['CVFHR **', 'CVFHR 50']),
            )),
            (eg.ActionGroup, 'gpLeftRearHeight', 'Left Rear Height', 'Left Rear Height', (
                (SendCommand, 'fnCVRHL_UP', 'Main Zone Channel Volume Left Rear Height Up', 'Main Zone Channel Volume Left Rear Height Up', ['CVRHL UP', 'CVRHL UP']),
                (SendCommand, 'fnCVRHL_DOWN', 'Main Zone Channel Volume Left Rear Height Down', 'Main Zone Channel Volume Left Rear Height Down', ['CVRHL DOWN', 'CVRHL DOWN']),
                (SendCommand, 'fnCVRHL_INPUT', 'Main Zone Channel Volume Left Rear Height Input', 'Main Zone Channel Volume Left Rear Height Input', ['CVRHL **', 'CVRHL 50']),
            )),
            (eg.ActionGroup, 'gpRightRearHeight', 'Right Rear Height', 'Right Rear Height', (
                (SendCommand, 'fnCVRHR_UP', 'Main Zone Channel Volume Right Rear Height Up', 'Main Zone Channel Volume Right Rear Height Up', ['CVRHR UP', 'CVRHR UP']),
                (SendCommand, 'fnCVRHR_DOWN', 'Main Zone Channel Volume Right Rear Height Down', 'Main Zone Channel Volume Right Rear Height Down', ['CVRHR DOWN', 'CVRHR DOWN']),
                (SendCommand, 'fnCVRHR_INPUT', 'Main Zone Channel Volume Right Rear Height Input', 'Main Zone Channel Volume Right Rear Height Input', ['CVRHR **', 'CVRHR 50']),
            )),
            (eg.ActionGroup, 'gpLeftFrontTop', 'Left Front Top', 'Left Front Top', (
                (SendCommand, 'fnCVTFL_UP', 'Main Zone Channel Volume Left Front Top Up', 'Main Zone Channel Volume Left Front Top Up', ['CVTFL UP', 'CVTFL UP']),
                (SendCommand, 'fnCVTFL_DOWN', 'Main Zone Channel Volume Left Front Top Down', 'Main Zone Channel Volume Left Front Top Down', ['CVTFL DOWN', 'CVTFL DOWN']),
                (SendCommand, 'fnCVTFL_INPUT', 'Main Zone Channel Volume Left Front Top Input', 'Main Zone Channel Volume Left Front Top Input', ['CVTFL **', 'CVTFL 50']),
            )),
            (eg.ActionGroup, 'gpRightFrontTop', 'Right Front Top', 'Right Front Top', (
                (SendCommand, 'fnCVTFR_UP', 'Main Zone Channel Volume Right Front Top Up', 'Main Zone Channel Volume Right Front Top Up', ['CVTFR UP', 'CVTFR UP']),
                (SendCommand, 'fnCVTFR_DOWN', 'Main Zone Channel Volume Right Front Top Down', 'Main Zone Channel Volume Right Front Top Down', ['CVTFR DOWN', 'CVTFR DOWN']),
                (SendCommand, 'fnCVTFR_INPUT', 'Main Zone Channel Volume Right Front Top Input', 'Main Zone Channel Volume Right Front Top Input', ['CVTFR **', 'CVTFR 50']),
            )),
            (eg.ActionGroup, 'gpLeftRearTop', 'Left Rear Top', 'Left Rear Top', (
                (SendCommand, 'fnCVTRL_UP', 'Main Zone Channel Volume Left Rear Top Up', 'Main Zone Channel Volume Left Rear Top Up', ['CVTRL UP', 'CVTRL UP']),
                (SendCommand, 'fnCVTRL_DOWN', 'Main Zone Channel Volume Left Rear Top Down', 'Main Zone Channel Volume Left Rear Top Down', ['CVTRL DOWN', 'CVTRL DOWN']),
                (SendCommand, 'fnCVTRL_INPUT', 'Main Zone Channel Volume Left Rear Top Input', 'Main Zone Channel Volume Left Rear Top Input', ['CVTRL **', 'CVTRL 50']),
            )),
            (eg.ActionGroup, 'gpRightRearTop', 'Right Rear Top', 'Right Rear Top', (
                (SendCommand, 'fnCVTRR_UP', 'Main Zone Channel Volume Right Rear Top Up', 'Main Zone Channel Volume Right Rear Top Up', ['CVTRR UP', 'CVTRR UP']),
                (SendCommand, 'fnCVTRR_DOWN', 'Main Zone Channel Volume Right Rear Top Down', 'Main Zone Channel Volume Right Rear Top Down', ['CVTRR DOWN', 'CVTRR DOWN']),
                (SendCommand, 'fnCVTRR_INPUT', 'Main Zone Channel Volume Right Rear Top Input', 'Main Zone Channel Volume Right Rear Top Input', ['CVTRR **', 'CVTRR 50']),
            )),
            (eg.ActionGroup, 'gpLeftFrontDolby', 'Left Front Dolby', 'Left Front Dolby', (
                (SendCommand, 'fnCVFDL_UP', 'Main Zone Channel Volume Left Front Dolby Up', 'Main Zone Channel Volume Left Front Dolby Up', ['CVFDL UP', 'CVFDL UP']),
                (SendCommand, 'fnCVFDL_DOWN', 'Main Zone Channel Volume Left Front Dolby Down', 'Main Zone Channel Volume Left Front Dolby Down', ['CVFDL DOWN', 'CVFDL DOWN']),
                (SendCommand, 'fnCVFDL_INPUT', 'Main Zone Channel Volume Left Front Dolby Input', 'Main Zone Channel Volume Left Front Dolby Input', ['CVFDL **', 'CVFDL 50']),
            )),
            (eg.ActionGroup, 'gpRightFrontDolby', 'Right Front Dolby', 'Right Front Dolby', (
                (SendCommand, 'fnCVFDR_UP', 'Main Zone Channel Volume Right Front Dolby Up', 'Main Zone Channel Volume Right Front Dolby Up', ['CVFDR UP', 'CVFDR UP']),
                (SendCommand, 'fnCVFDR_DOWN', 'Main Zone Channel Volume Right Front Dolby Down', 'Main Zone Channel Volume Right Front Dolby Down', ['CVFDR DOWN', 'CVFDR DOWN']),
                (SendCommand, 'fnCVFDR_INPUT', 'Main Zone Channel Volume Right Front Dolby Input', 'Main Zone Channel Volume Right Front Dolby Input', ['CVFDR **', 'CVFDR 50']),
            )),
            (eg.ActionGroup, 'gpSurroundLeftDolby', 'Surround Left Dolby', 'Surround Left Dolby', (
                (SendCommand, 'fnCVSDL_UP', 'Main Zone Channel Volume Surround Left Dolby Up', 'Main Zone Channel Volume Surround Left Dolby Up', ['CVSDL UP', 'CVSDL UP']),
                (SendCommand, 'fnCVSDL_DOWN', 'Main Zone Channel Volume Surround Left Dolby Down', 'Main Zone Channel Volume Surround Left Dolby Down', ['CVSDL DOWN', 'CVSDL DOWN']),
                (SendCommand, 'fnCVSDL_INPUT', 'Main Zone Channel Volume Surround Left Dolby Input', 'Main Zone Channel Volume Surround Left Dolby Input', ['CVSDL **', 'CVSDL 50']),
            )),
            (eg.ActionGroup, 'gpSurroundRightDolby', 'Surround Right Dolby', 'Surround Right Dolby', (
                (SendCommand, 'fnCVSDR_UP', 'Main Zone Channel Volume Surround Right Dolby Up', 'Main Zone Channel Volume Surround Right Dolby Up', ['CVSDR UP', 'CVSDR UP']),
                (SendCommand, 'fnCVSDR_DOWN', 'Main Zone Channel Volume Surround Right Dolby Down', 'Main Zone Channel Volume Surround Right Dolby Down', ['CVSDR DOWN', 'CVSDR DOWN']),
                (SendCommand, 'fnCVSDR_INPUT', 'Main Zone Channel Volume Surround Right Dolby Input', 'Main Zone Channel Volume Surround Right Dolby Input', ['CVSDR **', 'CVSDR 50']),
            )),
            (eg.ActionGroup, 'gpSurroundBackLeftDolby', 'Surround Back Left Dolby', 'Surround Back Left Dolby', (
                (SendCommand, 'fnCVBDL_UP', 'Main Zone Channel Volume Surround Back Left Dolby Up', 'Main Zone Channel Volume Surround Back Left Dolby Up', ['CVBDL UP', 'CVBDL UP']),
                (SendCommand, 'fnCVBDL_DOWN', 'Main Zone Channel Volume Surround Back Left Dolby Down', 'Main Zone Channel Volume Surround Back Left Dolby Down', ['CVBDL DOWN', 'CVBDL DOWN']),
                (SendCommand, 'fnCVBDL_INPUT', 'Main Zone Channel Volume Surround Back Left Dolby Input', 'Main Zone Channel Volume Surround Back Left Dolby Input', ['CVBDL **', 'CVBDL 50']),
            )),
            (eg.ActionGroup, 'gpSurroundBackRightDolby', 'Surround Back Right Dolby', 'Surround Back Right Dolby', (
                (SendCommand, 'fnCVBDR_UP', 'Main Zone Channel Volume Surround Back Right Dolby Up', 'Main Zone Channel Volume Surround Back Right Dolby Up', ['CVBDR UP', 'CVBDR UP']),
                (SendCommand, 'fnCVBDR_DOWN', 'Main Zone Channel Volume Surround Back Right Dolby Down', 'Main Zone Channel Volume Surround Back Right Dolby Down', ['CVBDR DOWN', 'CVBDR DOWN']),
                (SendCommand, 'fnCVBDR_INPUT', 'Main Zone Channel Volume Surround Back Right Dolby Input', 'Main Zone Channel Volume Surround Back Right Dolby Input', ['CVBDR **', 'CVBDR 50']),
            )),
            (eg.ActionGroup, 'gpLeftFrontWide', 'Left Front Wide', 'Left Front Wide', (
                (SendCommand, 'fnCVFWL_UP', 'Main Zone Channel Volume Left Front Wide Up', 'Main Zone Channel Volume Left Front Wide Up', ['CVFWL UP', 'CVFWL UP']),
                (SendCommand, 'fnCVFWL_DOWN', 'Main Zone Channel Volume Left Front Wide Down', 'Main Zone Channel Volume Left Front Wide Down', ['CVFWL DOWN', 'CVFWL DOWN']),
                (SendCommand, 'fnCVFWL_INPUT', 'Main Zone Channel Volume Left Front Wide Input', 'Main Zone Channel Volume Left Front Wide Input', ['CVFWL **', 'CVFWL 50']),
            )),
            (eg.ActionGroup, 'gpRightFrontWide', 'Right Front Wide', 'Right Front Wide', (
                (SendCommand, 'fnCVFWR_UP', 'Main Zone Channel Volume Right Front Wide Up', 'Main Zone Channel Volume Right Front Wide Up', ['CVFWR UP', 'CVFWR UP']),
                (SendCommand, 'fnCVFWR_DOWN', 'Main Zone Channel Volume Right Front Wide Down', 'Main Zone Channel Volume Right Front Wide Down', ['CVFWR DOWN', 'CVFWR DOWN']),
                (SendCommand, 'fnCVFWR_INPUT', 'Main Zone Channel Volume Right Front Wide Input', 'Main Zone Channel Volume Right Front Wide Input', ['CVFWR **', 'CVFWR 50']),
            )),
            (eg.ActionGroup, 'gpLeftFrontMiddle', 'Left Front Middle', 'Left Front Middle', (
                (SendCommand, 'fnCVTML_UP', 'Main Zone Channel Volume Left Front Middle Up', 'Main Zone Channel Volume Left Front Middle Up', ['CVTML UP', 'CVTML UP']),
                (SendCommand, 'fnCVTML_DOWN', 'Main Zone Channel Volume Left Front Middle Down', 'Main Zone Channel Volume Left Front Middle Down', ['CVTML DOWN', 'CVTML DOWN']),
                (SendCommand, 'fnCVTML_INPUT', 'Main Zone Channel Volume Left Front Middle Input', 'Main Zone Channel Volume Left Front Middle Input', ['CVTML **', 'CVTML 50']),
            )),
            (eg.ActionGroup, 'gpRightFrontMiddle', 'Right Front Middle', 'Right Front Middle', (
                (SendCommand, 'fnCVTMR_UP', 'Main Zone Channel Volume Right Front Middle Up', 'Main Zone Channel Volume Right Front Middle Up', ['CVTMR UP', 'CVTMR UP']),
                (SendCommand, 'fnCVTMR_DOWN', 'Main Zone Channel Volume Right Front Middle Down', 'Main Zone Channel Volume Right Front Middle Down', ['CVTMR DOWN', 'CVTMR DOWN']),
                (SendCommand, 'fnCVTMR_INPUT', 'Main Zone Channel Volume Right Front Middle Input', 'Main Zone Channel Volume Right Front Middle Input', ['CVTMR **', 'CVTMR 50']),
            )),
            (eg.ActionGroup, 'gpSurroundLeftHeightAuro-3D', 'Surround Left Height Auro-3D ', 'Surround Left Height Auro-3D ', (
                (SendCommand, 'fnCVSHL_UP', 'Main Zone Channel Volume Surround Left Height Auro-3D  Up', 'Main Zone Channel Volume Surround Left Height Auro-3D  Up', ['CVSHL UP', 'CVSHL UP']),
                (SendCommand, 'fnCVSHL_DOWN', 'Main Zone Channel Volume Surround Left Height Auro-3D  Down', 'Main Zone Channel Volume Surround Left Height Auro-3D  Down', ['CVSHL DOWN', 'CVSHL DOWN']),
                (SendCommand, 'fnCVSHL_INPUT', 'Main Zone Channel Volume Surround Left Height Auro-3D  Input', 'Main Zone Channel Volume Surround Left Height Auro-3D  Input', ['CVSHL **', 'CVSHL **']),
            )),
            (eg.ActionGroup, 'gpSurroundRightHeightAuro-3D', 'Surround Right Height Auro-3D ', 'Surround Right Height Auro-3D ', (
                (SendCommand, 'fnCVSHR_UP', 'Main Zone Channel Volume Surround Right Height Auro-3D  Up', 'Main Zone Channel Volume Surround Right Height Auro-3D  Up', ['CVSHR UP', 'CVSHR UP']),
                (SendCommand, 'fnCVSHR_DOWN', 'Main Zone Channel Volume Surround Right Height Auro-3D  Down', 'Main Zone Channel Volume Surround Right Height Auro-3D  Down', ['CVSHR DOWN', 'CVSHR DOWN']),
                (SendCommand, 'fnCVSHR_INPUT', 'Main Zone Channel Volume Surround Right Height Auro-3D  Input', 'Main Zone Channel Volume Surround Right Height Auro-3D  Input', ['CVSHR **', 'CVSHR **']),
            )),
            (eg.ActionGroup, 'gpSurroundTopAuro-3D', 'Surround Top Auro-3D ', 'Surround Top Auro-3D ', (
                (SendCommand, 'fnCVTS_UP', 'Main Zone Channel Volume Surround Top Auro-3D  Up', 'Main Zone Channel Volume Surround Top Auro-3D  Up', ['CVTS UP', 'CVTS UP']),
                (SendCommand, 'fnCVTS_DOWN', 'Main Zone Channel Volume Surround Top Auro-3D  Down', 'Main Zone Channel Volume Surround Top Auro-3D  Down', ['CVTS DOWN', 'CVTS DOWN']),
                (SendCommand, 'fnCVTS_INPUT', 'Main Zone Channel Volume Surround Top Auro-3D  Input', 'Main Zone Channel Volume Surround Top Auro-3D  Input', ['CVTS **', 'CVTS **']),
            )),
            (SendCommand, 'fnCVZRL', 'Main Zone Channel Volume Reset', 'Main Zone Channel Volume Reset', ['CVZRL', 'CVZRL']),
            (SendCommand, 'fnCVSTATUS', 'Main Zone Channel Volume Status', 'Main Zone Channel Volume Status', ['CV?', 'CV?']),
        )),
        (eg.ActionGroup, 'gpMute', 'Mute', 'Mute', (
            (SendCommand, 'fnMUON', 'Main Zone Mute On', 'Main Zone Mute On', ['MUON', 'MUON']),
            (SendCommand, 'fnMUOFF', 'Main Zone Mute Off', 'Main Zone Mute Off', ['MUOFF', 'MUOFF']),
            (SendCommand, 'fnMUSTATUS', 'Main Zone Mute Status', 'Main Zone Mute Status', ['MU?', 'MU?']),
        )),
        (eg.ActionGroup, 'gpSource', 'Source', 'Source', (
            (SendCommand, 'fnSIPHONO', 'Main Zone Source Phono', 'Main Zone Source Phono', ['SIPHONO', 'SIPHONO']),
            (SendCommand, 'fnSICD', 'Main Zone Source CD', 'Main Zone Source CD', ['SICD', 'SICD']),
            (SendCommand, 'fnSITUNER', 'Main Zone Source Tuner', 'Main Zone Source Tuner', ['SITUNER', 'SITUNER']),
            (SendCommand, 'fnSIDVD', 'Main Zone Source DVD', 'Main Zone Source DVD', ['SIDVD', 'SIDVD']),
            (SendCommand, 'fnSIBD', 'Main Zone Source BluRay', 'Main Zone Source BluRay', ['SIBD', 'SIBD']),
            (SendCommand, 'fnSITV', 'Main Zone Source TV', 'Main Zone Source TV', ['SITV', 'SITV']),
            (SendCommand, 'fnSISAT/CBL', 'Main Zone Source Sat/Cable', 'Main Zone Source Sat/Cable', ['SISAT/CBL', 'SISAT/CBL']),
            (SendCommand, 'fnSIMPLAY', 'Main Zone Source Media Player', 'Main Zone Source Media Player', ['SIMPLAY', 'SIMPLAY']),
            (SendCommand, 'fnSIGAME', 'Main Zone Source Game', 'Main Zone Source Game', ['SIGAME', 'SIGAME']),
            (SendCommand, 'fnSIHDRADIO', 'Main Zone Source HD Radio', 'Main Zone Source HD Radio', ['SIHDRADIO', 'SIHDRADIO']),
            (SendCommand, 'fnSINET', 'Main Zone Source Net', 'Main Zone Source Net', ['SINET', 'SINET']),
            (SendCommand, 'fnSIPANDORA', 'Main Zone Source Pandora', 'Main Zone Source Pandora', ['SIPANDORA', 'SIPANDORA']),
            (SendCommand, 'fnSISIRIUSXM', 'Main Zone Source Sirius/XM', 'Main Zone Source Sirius/XM', ['SISIRIUSXM', 'SISIRIUSXM']),
            (SendCommand, 'fnSIIRADIO', 'Main Zone Source Internet Radio', 'Main Zone Source Internet Radio', ['SIIRADIO', 'SIIRADIO']),
            (SendCommand, 'fnSISERVER', 'Main Zone Source Server', 'Main Zone Source Server', ['SISERVER', 'SISERVER']),
            (SendCommand, 'fnSIFAVORITES', 'Main Zone Source Favorites', 'Main Zone Source Favorites', ['SIFAVORITES', 'SIFAVORITES']),
            (SendCommand, 'fnSIAUX1', 'Main Zone Source Aux 1', 'Main Zone Source Aux 1', ['SIAUX1', 'SIAUX1']),
            (SendCommand, 'fnSIAUX2', 'Main Zone Source Aux 2', 'Main Zone Source Aux 2', ['SIAUX2', 'SIAUX2']),
            (SendCommand, 'fnSIAUX3', 'Main Zone Source Aux 3', 'Main Zone Source Aux 3', ['SIAUX3', 'SIAUX3']),
            (SendCommand, 'fnSIAUX4', 'Main Zone Source Aux 4', 'Main Zone Source Aux 4', ['SIAUX4', 'SIAUX4']),
            (SendCommand, 'fnSIAUX5', 'Main Zone Source Aux 5', 'Main Zone Source Aux 5', ['SIAUX5', 'SIAUX5']),
            (SendCommand, 'fnSIAUX6', 'Main Zone Source Aux 6', 'Main Zone Source Aux 6', ['SIAUX6', 'SIAUX6']),
            (SendCommand, 'fnSIAUX7', 'Main Zone Source Aux 7', 'Main Zone Source Aux 7', ['SIAUX7', 'SIAUX7']),
            (SendCommand, 'fnSIBT', 'Main Zone Source Blue Teeth', 'Main Zone Source Blue Teeth', ['SIBT', 'SIBT']),
            (SendCommand, 'fnSIUSB/IPOD', 'Main Zone Source USB/IPOD', 'Main Zone Source USB/IPOD', ['SIUSB/IPOD', 'SIUSB/IPOD']),
            (SendCommand, 'fnSIUSB', 'Main Zone Source USB + Playback', 'Main Zone Source USB + Playback', ['SIUSB', 'SIUSB']),
            (SendCommand, 'fnSIIPD', 'Main Zone Source IPOD + Playback', 'Main Zone Source IPOD + Playback', ['SIIPD', 'SIIPD']),
            (SendCommand, 'fnSIIRP', 'Main Zone Source Internet Radio + Playback Recent', 'Main Zone Source Internet Radio + Playback Recent', ['SIIRP', 'SIIRP']),
            (SendCommand, 'fnSIFVP', 'Main Zone Source Internet Radio + Playback Favorites', 'Main Zone Source Internet Radio + Playback Favorites', ['SIFVP', 'SIFVP']),
            (SendCommand, 'fnSISTATUS', 'Main Zone Source Status', 'Main Zone Source Status', ['SI?', 'SI?']),
        )),
        (eg.ActionGroup, 'gpPower', 'Power', 'Power', (
            (SendCommand, 'fnZMON', 'Main Zone Power On', 'Main Zone Power On', ['ZMON', 'ZMON']),
            (SendCommand, 'fnZMOFF', 'Main Zone Power Off', 'Main Zone Power Off', ['ZMOFF', 'ZMOFF']),
            (SendCommand, 'fnZMSTATUS', 'Main Zone Power Status', 'Main Zone Power Status', ['ZM?', 'ZM?']),
        )),
        (eg.ActionGroup, 'gpAudioInput', 'Audio Input', 'Audio Input', (
            (SendCommand, 'fnSDAUTO', 'Main Zone Audio Input Auto', 'Main Zone Audio Input Auto', ['SDAUTO', 'SDAUTO']),
            (SendCommand, 'fnSDHDMI', 'Main Zone Audio Input Audio HDMI', 'Main Zone Audio Input Audio HDMI', ['SDHDMI', 'SDHDMI']),
            (SendCommand, 'fnSDDIGITAL', 'Main Zone Audio Input Optical/Coaxial', 'Main Zone Audio Input Optical/Coaxial', ['SDDIGITAL', 'SDDIGITAL']),
            (SendCommand, 'fnSDANALOG', 'Main Zone Audio Input Analog', 'Main Zone Audio Input Analog', ['SDANALOG', 'SDANALOG']),
            (SendCommand, 'fnSD7.1IN', 'Main Zone Audio Input 7.1 In', 'Main Zone Audio Input 7.1 In', ['SD7.1IN', 'SD7.1IN']),
            (SendCommand, 'fnSDNO', 'Main Zone Audio Input No', 'Main Zone Audio Input No', ['SDNO', 'SDNO']),
            (SendCommand, 'fnSDSTATUS', 'Main Zone Audio Input Status', 'Main Zone Audio Input Status', ['SD?', 'SD?']),
        )),
        (eg.ActionGroup, 'gpDigitalAudioInputMode', 'Digital Audio Input Mode', 'Digital Audio Input Mode', (
            (SendCommand, 'fnDCAUTO', 'Main Zone Digital Audio Input Mode Auto', 'Main Zone Digital Audio Input Mode Auto', ['DCAUTO', 'DCAUTO']),
            (SendCommand, 'fnDCPCM', 'Main Zone Digital Audio Input Mode PCM', 'Main Zone Digital Audio Input Mode PCM', ['DCPCM', 'DCPCM']),
            (SendCommand, 'fnDCDTS', 'Main Zone Digital Audio Input Mode DTS', 'Main Zone Digital Audio Input Mode DTS', ['DCDTS', 'DCDTS']),
            (SendCommand, 'fnDCSTATUS', 'Main Zone Digital Audio Input Mode Status', 'Main Zone Digital Audio Input Mode Status', ['DC?', 'DC?']),
        )),
        (eg.ActionGroup, 'gpVideoSelect', 'Video Select', 'Video Select', (
            (SendCommand, 'fnSVDVD', 'Main Zone Video Select DVD', 'Main Zone Video Select DVD', ['SVDVD', 'SVDVD']),
            (SendCommand, 'fnSVBD', 'Main Zone Video Select BluRay', 'Main Zone Video Select BluRay', ['SVBD', 'SVBD']),
            (SendCommand, 'fnSVTV', 'Main Zone Video Select TV', 'Main Zone Video Select TV', ['SVTV', 'SVTV']),
            (SendCommand, 'fnSVSAT/CBL', 'Main Zone Video Select Sat/Cable', 'Main Zone Video Select Sat/Cable', ['SVSAT/CBL', 'SVSAT/CBL']),
            (SendCommand, 'fnSVMPLAY', 'Main Zone Video Select Media Player', 'Main Zone Video Select Media Player', ['SVMPLAY', 'SVMPLAY']),
            (SendCommand, 'fnSVGAME', 'Main Zone Video Select Game', 'Main Zone Video Select Game', ['SVGAME', 'SVGAME']),
            (SendCommand, 'fnSVAUX1', 'Main Zone Video Select Aux 1', 'Main Zone Video Select Aux 1', ['SVAUX1', 'SVAUX1']),
            (SendCommand, 'fnSVAUX2', 'Main Zone Video Select Aux 2', 'Main Zone Video Select Aux 2', ['SVAUX2', 'SVAUX2']),
            (SendCommand, 'fnSVAUX3', 'Main Zone Video Select Aux 3', 'Main Zone Video Select Aux 3', ['SVAUX3', 'SVAUX3']),
            (SendCommand, 'fnSVAUX4', 'Main Zone Video Select Aux 4', 'Main Zone Video Select Aux 4', ['SVAUX4', 'SVAUX4']),
            (SendCommand, 'fnSVAUX5', 'Main Zone Video Select Aux 5', 'Main Zone Video Select Aux 5', ['SVAUX5', 'SVAUX5']),
            (SendCommand, 'fnSVAUX6', 'Main Zone Video Select Aux 6', 'Main Zone Video Select Aux 6', ['SVAUX6', 'SVAUX6']),
            (SendCommand, 'fnSVAUX7', 'Main Zone Video Select Aux 7', 'Main Zone Video Select Aux 7', ['SVAUX7', 'SVAUX7']),
            (SendCommand, 'fnSVCD', 'Main Zone Video Select CD', 'Main Zone Video Select CD', ['SVCD', 'SVCD']),
            (SendCommand, 'fnSVON', 'Main Zone Video Select On', 'Main Zone Video Select On', ['SVON', 'SVON']),
            (SendCommand, 'fnSVOFF', 'Main Zone Video Select Off', 'Main Zone Video Select Off', ['SVOFF', 'SVOFF']),
            (SendCommand, 'fnSVSTATUS', 'Main Zone Video Select Status', 'Main Zone Video Select Status', ['SV?', 'SV?']),
        )),
        (eg.ActionGroup, 'gpSleepTimer', 'Sleep Timer', 'Sleep Timer', (
            (SendCommand, 'fnSLPOFF', 'Main Zone Sleep Timer Off', 'Main Zone Sleep Timer Off', ['SLPOFF', 'SLPOFF']),
            (SendCommand, 'fnSLPINPUT', 'Main Zone Sleep Timer Input', 'Main Zone Sleep Timer Input', ['SLP***', 'SLP120']),
            (SendCommand, 'fnSLPSTATUS', 'Main Zone Sleep Timer Status', 'Main Zone Sleep Timer Status', ['SLP?', 'SLP?']),
        )),
        (eg.ActionGroup, 'gpAutoStandby', 'Auto Standby', 'Auto Standby', (
            (SendCommand, 'fnSTBY15M', 'Main Zone Auto Standby 15 Minutes', 'Main Zone Auto Standby 15 Minutes', ['STBY15M', 'STBY15M']),
            (SendCommand, 'fnSTBY30M', 'Main Zone Auto Standby 30 Minutes', 'Main Zone Auto Standby 30 Minutes', ['STBY30M', 'STBY30M']),
            (SendCommand, 'fnSTBY60M', 'Main Zone Auto Standby 60 Minutes', 'Main Zone Auto Standby 60 Minutes', ['STBY60M', 'STBY60M']),
            (SendCommand, 'fnSTBYOFF', 'Main Zone Auto Standby Off', 'Main Zone Auto Standby Off', ['STBYOFF', 'STBYOFF']),
            (SendCommand, 'fnSTBYSTATUS', 'Main Zone Auto Standby Status', 'Main Zone Auto Standby Status', ['STBY?', 'STBY?']),
        )),
        (eg.ActionGroup, 'gpEcoMode', 'Eco Mode', 'Eco Mode', (
            (SendCommand, 'fnECOON', 'Main Zone Eco Mode On', 'Main Zone Eco Mode On', ['ECOON', 'ECOON']),
            (SendCommand, 'fnECOAUTO', 'Main Zone Eco Mode Auto', 'Main Zone Eco Mode Auto', ['ECOAUTO', 'ECOAUTO']),
            (SendCommand, 'fnECOOFF', 'Main Zone Eco Mode Off', 'Main Zone Eco Mode Off', ['ECOOFF', 'ECOOFF']),
            (SendCommand, 'fnECOSTATUS', 'Main Zone Eco Mode Status', 'Main Zone Eco Mode Status', ['ECO?', 'ECO?']),
        )),
        (eg.ActionGroup, 'gpSurroundMode', 'Surround Mode', 'Surround Mode', (
            (SendCommand, 'fnMSMOVIE', 'Main Zone Surround Mode Movie', 'Main Zone Surround Mode Movie', ['MSMOVIE', 'MSMOVIE']),
            (SendCommand, 'fnMSMUSIC', 'Main Zone Surround Mode Music', 'Main Zone Surround Mode Music', ['MSMUSIC', 'MSMUSIC']),
            (SendCommand, 'fnMSGAME', 'Main Zone Surround Mode Game', 'Main Zone Surround Mode Game', ['MSGAME', 'MSGAME']),
            (SendCommand, 'fnMSDIRECT', 'Main Zone Surround Mode Direct', 'Main Zone Surround Mode Direct', ['MSDIRECT', 'MSDIRECT']),
            (SendCommand, 'fnMSPURE_DIRECT', 'Main Zone Surround Mode Pure Direct', 'Main Zone Surround Mode Pure Direct', ['MSPURE DIRECT', 'MSPURE DIRECT']),
            (SendCommand, 'fnMSSTEREO', 'Main Zone Surround Mode Stereo', 'Main Zone Surround Mode Stereo', ['MSSTEREO', 'MSSTEREO']),
            (SendCommand, 'fnMSAUTO', 'Main Zone Surround Mode Auto', 'Main Zone Surround Mode Auto', ['MSAUTO', 'MSAUTO']),
            (SendCommand, 'fnMSDOLBY_DIGITAL', 'Main Zone Surround Mode Dolby Digital', 'Main Zone Surround Mode Dolby Digital', ['MSDOLBY DIGITAL', 'MSDOLBY DIGITAL']),
            (SendCommand, 'fnMSDTS_SURROUND', 'Main Zone Surround Mode DTS', 'Main Zone Surround Mode DTS', ['MSDTS SURROUND', 'MSDTS SURROUND']),
            (SendCommand, 'fnMSAURO3D', 'Main Zone Surround Mode Auro 3D', 'Main Zone Surround Mode Auro 3D', ['MSAURO3D', 'MSAURO3D']),
            (SendCommand, 'fnMSAURO2DSURR', 'Main Zone Surround Mode Auro 2D', 'Main Zone Surround Mode Auro 2D', ['MSAURO2DSURR', 'MSAURO2DSURR']),
            (SendCommand, 'fnMSMCH_STEREO', 'Main Zone Surround Mode Multi Channel Stereo', 'Main Zone Surround Mode Multi Channel Stereo', ['MSMCH STEREO', 'MSMCH STEREO']),
            (SendCommand, 'fnMSWIDE_SCREEN', 'Main Zone Surround Mode Wide Screen', 'Main Zone Surround Mode Wide Screen', ['MSWIDE SCREEN', 'MSWIDE SCREEN']),
            (SendCommand, 'fnMSSUPER_STADIUM', 'Main Zone Surround Mode Super Stadium', 'Main Zone Surround Mode Super Stadium', ['MSSUPER STADIUM', 'MSSUPER STADIUM']),
            (SendCommand, 'fnMSROCK_ARENA', 'Main Zone Surround Mode Rock Arena', 'Main Zone Surround Mode Rock Arena', ['MSROCK ARENA', 'MSROCK ARENA']),
            (SendCommand, 'fnMSJAZZ_CLUB', 'Main Zone Surround Mode Jazz Club', 'Main Zone Surround Mode Jazz Club', ['MSJAZZ CLUB', 'MSJAZZ CLUB']),
            (SendCommand, 'fnMSCLASSIC_CONCERT', 'Main Zone Surround Mode Classic Concert', 'Main Zone Surround Mode Classic Concert', ['MSCLASSIC CONCERT', 'MSCLASSIC CONCERT']),
            (SendCommand, 'fnMSMONO_MOVIE', 'Main Zone Surround Mode Mono Movie', 'Main Zone Surround Mode Mono Movie', ['MSMONO MOVIE', 'MSMONO MOVIE']),
            (SendCommand, 'fnMSMATRIX', 'Main Zone Surround Mode Matrix', 'Main Zone Surround Mode Matrix', ['MSMATRIX', 'MSMATRIX']),
            (SendCommand, 'fnMSVIDEO_GAME', 'Main Zone Surround Mode Video Game', 'Main Zone Surround Mode Video Game', ['MSVIDEO GAME', 'MSVIDEO GAME']),
            (SendCommand, 'fnMSVIRTUAL', 'Main Zone Surround Mode Virtual', 'Main Zone Surround Mode Virtual', ['MSVIRTUAL', 'MSVIRTUAL']),
            (SendCommand, 'fnMSLEFT', 'Main Zone Surround Mode Left', 'Main Zone Surround Mode Left', ['MSLEFT', 'MSLEFT']),
            (SendCommand, 'fnMSRIGHT', 'Main Zone Surround Mode Right', 'Main Zone Surround Mode Right', ['MSRIGHT', 'MSRIGHT']),
            (SendCommand, 'fnMSSTATUS', 'Main Zone Surround Mode Status', 'Main Zone Surround Mode Status', ['MS?', 'MS?']),
            (eg.ActionGroup, 'gpQuickSelect', 'Quick Select', 'Quick Select', (
                (SendCommand, 'fnMSQUICK1', 'Main Zone Surround Mode Quick Select 1', 'Main Zone Surround Mode Quick Select 1', ['MSQUICK1', 'MSQUICK1']),
                (SendCommand, 'fnMSQUICK2', 'Main Zone Surround Mode Quick Select 2', 'Main Zone Surround Mode Quick Select 2', ['MSQUICK2', 'MSQUICK2']),
                (SendCommand, 'fnMSQUICK3', 'Main Zone Surround Mode Quick Select 3', 'Main Zone Surround Mode Quick Select 3', ['MSQUICK3', 'MSQUICK3']),
                (SendCommand, 'fnMSQUICK4', 'Main Zone Surround Mode Quick Select 4', 'Main Zone Surround Mode Quick Select 4', ['MSQUICK4', 'MSQUICK4']),
                (SendCommand, 'fnMSQUICK5', 'Main Zone Surround Mode Quick Select 5', 'Main Zone Surround Mode Quick Select 5', ['MSQUICK5', 'MSQUICK5']),
                (SendCommand, 'fnMSQUICK_STATUS', 'Main Zone Surround Mode Quick Select Quick Status', 'Main Zone Surround Mode Quick Select Quick Status', ['MSQUICK ?', 'MSQUICK ?']),
            )),
            (eg.ActionGroup, 'gpQuickMemorySelect', 'Quick Memory Select', 'Quick Memory Select', (
                (SendCommand, 'fnMSQUICK1_MEMORYSTATUS', 'Main Zone Surround Mode Quick Memory Select 1', 'Main Zone Surround Mode Quick Memory Select 1', ['MSQUICK1 MEMORY?', 'MSQUICK1 MEMORY']),
                (SendCommand, 'fnMSQUICK2_MEMORY', 'Main Zone Surround Mode Quick Memory Select 2', 'Main Zone Surround Mode Quick Memory Select 2', ['MSQUICK2 MEMORY', 'MSQUICK2 MEMORY']),
                (SendCommand, 'fnMSQUICK3_MEMORY', 'Main Zone Surround Mode Quick Memory Select 3', 'Main Zone Surround Mode Quick Memory Select 3', ['MSQUICK3 MEMORY', 'MSQUICK3 MEMORY']),
                (SendCommand, 'fnMSQUCIK4_MEMORY', 'Main Zone Surround Mode Quick Memory Select 4', 'Main Zone Surround Mode Quick Memory Select 4', ['MSQUCIK4 MEMORY', 'MSQUICK4 MEMORY']),
                (SendCommand, 'fnMSQUICK5_MEMORY', 'Main Zone Surround Mode Quick Memory Select 5', 'Main Zone Surround Mode Quick Memory Select 5', ['MSQUICK5 MEMORY', 'MSQUICK5 MEMORY']),
                (SendCommand, 'fnMSQUICK_STATUS', 'Main Zone Surround Mode Quick Memory Select Quick Status', 'Main Zone Surround Mode Quick Memory Select Quick Status', ['MSQUICK ?', 'MSQUICK ?']),
            )),
        )),
        (eg.ActionGroup, 'gpVideoSettings', 'Video Settings', 'Video Settings', (
            (eg.ActionGroup, 'gpAspectRatio', 'Aspect Ratio', 'Aspect Ratio', (
                (SendCommand, 'fnVSASPNRM', 'Main Zone Video Settings Aspect Ratio 4:3', 'Main Zone Video Settings Aspect Ratio 4:3', ['VSASPNRM', 'VSASPNRM']),
                (SendCommand, 'fnVSASPFUL', 'Main Zone Video Settings Aspect Ratio 16:9', 'Main Zone Video Settings Aspect Ratio 16:9', ['VSASPFUL', 'VSASPFUL']),
                (SendCommand, 'fnVSASP_STATUS', 'Main Zone Video Settings Aspect Ratio Status', 'Main Zone Video Settings Aspect Ratio Status', ['VSASP ?', 'VSASP ?']),
            )),
            (eg.ActionGroup, 'gpHDMIMonitor', 'HDMI Monitor', 'HDMI Monitor', (
                (SendCommand, 'fnVSMONIAUTO', 'Main Zone Video Settings HDMI Monitor Auto', 'Main Zone Video Settings HDMI Monitor Auto', ['VSMONIAUTO', 'VSMONIAUTO']),
                (SendCommand, 'fnVSMONI1', 'Main Zone Video Settings HDMI Monitor Out 1', 'Main Zone Video Settings HDMI Monitor Out 1', ['VSMONI1', 'VSMONI1']),
                (SendCommand, 'fnVSMONI2', 'Main Zone Video Settings HDMI Monitor Out 2', 'Main Zone Video Settings HDMI Monitor Out 2', ['VSMONI2', 'VSMONI2']),
                (SendCommand, 'fnVSMONI_STATUS', 'Main Zone Video Settings HDMI Monitor Status', 'Main Zone Video Settings HDMI Monitor Status', ['VSMONI ?', 'VSMONI ?']),
            )),
            (eg.ActionGroup, 'gpResolution', 'Resolution', 'Resolution', (
                (SendCommand, 'fnVSSC48P', 'Main Zone Video Settings Resolution 480p/576p', 'Main Zone Video Settings Resolution 480p/576p', ['VSSC48P', 'VSSC48P']),
                (SendCommand, 'fnVSSC10I', 'Main Zone Video Settings Resolution 1080i', 'Main Zone Video Settings Resolution 1080i', ['VSSC10I', 'VSSC10I']),
                (SendCommand, 'fnVSSC72P', 'Main Zone Video Settings Resolution 720p', 'Main Zone Video Settings Resolution 720p', ['VSSC72P', 'VSSC72P']),
                (SendCommand, 'fnVSSC10P', 'Main Zone Video Settings Resolution 1080p', 'Main Zone Video Settings Resolution 1080p', ['VSSC10P', 'VSSC10P']),
                (SendCommand, 'fnVSSC10P24', 'Main Zone Video Settings Resolution 1080p:24Hz', 'Main Zone Video Settings Resolution 1080p:24Hz', ['VSSC10P24', 'VSSC10P24']),
                (SendCommand, 'fnVSSC4K', 'Main Zone Video Settings Resolution 4K', 'Main Zone Video Settings Resolution 4K', ['VSSC4K', 'VSSC4K']),
                (SendCommand, 'fnVSSC4KF', 'Main Zone Video Settings Resolution 4K(60/50) ', 'Main Zone Video Settings Resolution 4K(60/50) ', ['VSSC4KF', 'VSSC4KF']),
                (SendCommand, 'fnVSSCAUTO', 'Main Zone Video Settings Resolution Auto', 'Main Zone Video Settings Resolution Auto', ['VSSCAUTO', 'VSSCAUTO']),
                (SendCommand, 'fnVSSC_STATUS', 'Main Zone Video Settings Resolution Status', 'Main Zone Video Settings Resolution Status', ['VSSC ?', 'VSSC ?']),
            )),
            (eg.ActionGroup, 'gpHDMIResolution', 'HDMI Resolution', 'HDMI Resolution', (
                (SendCommand, 'fnVSSCH48P', 'Main Zone Video Settings HDMI Resolution 480p/576p', 'Main Zone Video Settings HDMI Resolution 480p/576p', ['VSSCH48P', 'VSSCH48P']),
                (SendCommand, 'fnVSSCH10I', 'Main Zone Video Settings HDMI Resolution 1080i', 'Main Zone Video Settings HDMI Resolution 1080i', ['VSSCH10I', 'VSSCH10I']),
                (SendCommand, 'fnVSSCH72P', 'Main Zone Video Settings HDMI Resolution 720p', 'Main Zone Video Settings HDMI Resolution 720p', ['VSSCH72P', 'VSSCH72P']),
                (SendCommand, 'fnVSSCH10P', 'Main Zone Video Settings HDMI Resolution 1080p', 'Main Zone Video Settings HDMI Resolution 1080p', ['VSSCH10P', 'VSSCH10P']),
                (SendCommand, 'fnVSSCH10P24', 'Main Zone Video Settings HDMI Resolution 1080p:24Hz', 'Main Zone Video Settings HDMI Resolution 1080p:24Hz', ['VSSCH10P24', 'VSSCH10P24']),
                (SendCommand, 'fnVSSCH4K', 'Main Zone Video Settings HDMI Resolution 4K', 'Main Zone Video Settings HDMI Resolution 4K', ['VSSCH4K', 'VSSCH4K']),
                (SendCommand, 'fnVSSCH4KF', 'Main Zone Video Settings HDMI Resolution 4K(60/50) ', 'Main Zone Video Settings HDMI Resolution 4K(60/50) ', ['VSSCH4KF', 'VSSCH4KF']),
                (SendCommand, 'fnVSSCHAUTO', 'Main Zone Video Settings HDMI Resolution Auto', 'Main Zone Video Settings HDMI Resolution Auto', ['VSSCHAUTO', 'VSSCHAUTO']),
                (SendCommand, 'fnVSSCH_STATUS', 'Main Zone Video Settings HDMI Resolution Status', 'Main Zone Video Settings HDMI Resolution Status', ['VSSCH ?', 'VSSCH ?']),
            )),
            (eg.ActionGroup, 'gpHDMIAudioOutput', 'HDMI Audio Output', 'HDMI Audio Output', (
                (SendCommand, 'fnVSAUDIO_AMP', 'Main Zone Video Settings HDMI Audio Output Amp', 'Main Zone Video Settings HDMI Audio Output Amp', ['VSAUDIO AMP', 'VSAUDIO AMP']),
                (SendCommand, 'fnVSAUDIO_TV', 'Main Zone Video Settings HDMI Audio Output TV', 'Main Zone Video Settings HDMI Audio Output TV', ['VSAUDIO TV', 'VSAUDIO TV']),
                (SendCommand, 'fnVSAUDIO_STATUS', 'Main Zone Video Settings HDMI Audio Output Status', 'Main Zone Video Settings HDMI Audio Output Status', ['VSAUDIO ?', 'VSAUDIO ?']),
            )),
            (eg.ActionGroup, 'gpVideoProcessing', 'Video Processing', 'Video Processing', (
                (SendCommand, 'fnVSVPMAUTO', 'Main Zone Video Settings Video Processing Auto', 'Main Zone Video Settings Video Processing Auto', ['VSVPMAUTO', 'VSVPMAUTO']),
                (SendCommand, 'fnVSVPMGAME', 'Main Zone Video Settings Video Processing Game', 'Main Zone Video Settings Video Processing Game', ['VSVPMGAME', 'VSVPMGAME']),
                (SendCommand, 'fnVSVPMMOVI', 'Main Zone Video Settings Video Processing Movie', 'Main Zone Video Settings Video Processing Movie', ['VSVPMMOVI', 'VSVPMMOVI']),
                (SendCommand, 'fnVSVPMBYP', 'Main Zone Video Settings Video Processing Bypass', 'Main Zone Video Settings Video Processing Bypass', ['VSVPMBYP', 'VSVPMBYP']),
                (SendCommand, 'fnVSVPM_STATUS', 'Main Zone Video Settings Video Processing Status', 'Main Zone Video Settings Video Processing Status', ['VSVPM ?', 'VSVPM ?']),
            )),
            (eg.ActionGroup, 'gpVerticalStretch', 'Vertical Stretch', 'Vertical Stretch', (
                (SendCommand, 'fnVSVST_ON', 'Main Zone Video Settings Vertical Stretch On', 'Main Zone Video Settings Vertical Stretch On', ['VSVST ON', 'VSVST ON']),
                (SendCommand, 'fnVSVST_OFF', 'Main Zone Video Settings Vertical Stretch Off', 'Main Zone Video Settings Vertical Stretch Off', ['VSVST OFF', 'VSVST OFF']),
                (SendCommand, 'fnVSVST_STATUS', 'Main Zone Video Settings Vertical Stretch Status', 'Main Zone Video Settings Vertical Stretch Status', ['VSVST ?', 'VSVST ?']),
            )),
        )),
        (eg.ActionGroup, 'gpOtherSettings', 'Other Settings', 'Other Settings', (
            (eg.ActionGroup, 'gpTone', 'Tone', 'Tone', (
                (SendCommand, 'fnPSTONE_CTRL_ON', 'Main Zone Other Settings Tone On', 'Main Zone Other Settings Tone On', ['PSTONE CTRL ON', 'PSTONE CTRL ON']),
                (SendCommand, 'fnPSTONE_CTRL_OFF', 'Main Zone Other Settings Tone Off', 'Main Zone Other Settings Tone Off', ['PSTONE CTRL OFF', 'PSTONE CTRL OFF']),
                (SendCommand, 'fnPSTONE_CTRL_STATUS', 'Main Zone Other Settings Tone Status', 'Main Zone Other Settings Tone Status', ['PSTONE CTRL ?', 'PSTONE CTRL ?']),
            )),
            (eg.ActionGroup, 'gpBass', 'Bass', 'Bass', (
                (SendCommand, 'fnPSBAS_UP', 'Main Zone Other Settings Bass Up', 'Main Zone Other Settings Bass Up', ['PSBAS UP', 'PSBAS UP']),
                (SendCommand, 'fnPSBAS_DOWN', 'Main Zone Other Settings Bass Down', 'Main Zone Other Settings Bass Down', ['PSBAS DOWN', 'PSBAS DOWN']),
                (SendCommand, 'fnPSBAS_INPUT', 'Main Zone Other Settings Bass Input', 'Main Zone Other Settings Bass Input', ['PSBAS **', 'PSBAS 50']),
                (SendCommand, 'fnPSBAS_STATUS', 'Main Zone Other Settings Bass Status', 'Main Zone Other Settings Bass Status', ['PSBAS ?', 'PSBAS ?']),
            )),
            (eg.ActionGroup, 'gpTreble', 'Treble', 'Treble', (
                (SendCommand, 'fnPSTRE_UP', 'Main Zone Other Settings Treble Up', 'Main Zone Other Settings Treble Up', ['PSTRE UP', 'PSTRE UP']),
                (SendCommand, 'fnPSTRE_DOWN', 'Main Zone Other Settings Treble Down', 'Main Zone Other Settings Treble Down', ['PSTRE DOWN', 'PSTRE DOWN']),
                (SendCommand, 'fnPSTRE_INPUT', 'Main Zone Other Settings Treble Input', 'Main Zone Other Settings Treble Input', ['PSTRE **', 'PSTRE 50']),
                (SendCommand, 'fnPSTRE_STATUS', 'Main Zone Other Settings Treble Status', 'Main Zone Other Settings Treble Status', ['PSTRE ?', 'PSTRE ?']),
            )),
            (eg.ActionGroup, 'gpDialogLevel', 'Dialog Level', 'Dialog Level', (
                (SendCommand, 'fnPSDIL_ON', 'Main Zone Other Settings Dialog Level On', 'Main Zone Other Settings Dialog Level On', ['PSDIL ON', 'PSDIL ON']),
                (SendCommand, 'fnPSDIL_OFF', 'Main Zone Other Settings Dialog Level Off', 'Main Zone Other Settings Dialog Level Off', ['PSDIL OFF', 'PSDIL OFF']),
                (SendCommand, 'fnPSDIL_UP', 'Main Zone Other Settings Dialog Level Up', 'Main Zone Other Settings Dialog Level Up', ['PSDIL UP', 'PSDIL UP']),
                (SendCommand, 'fnPSDIL_DOWN', 'Main Zone Other Settings Dialog Level Down', 'Main Zone Other Settings Dialog Level Down', ['PSDIL DOWN', 'PSDIL DOWN']),
                (SendCommand, 'fnPSDIL_INPUT', 'Main Zone Other Settings Dialog Level Input', 'Main Zone Other Settings Dialog Level Input', ['PSDIL **', 'PSDIL 50']),
                (SendCommand, 'fnPSDIL_STATUS', 'Main Zone Other Settings Dialog Level Status', 'Main Zone Other Settings Dialog Level Status', ['PSDIL ?', 'PSDIL ?']),
            )),
            (eg.ActionGroup, 'gpSubwooferLevel', 'Subwoofer Level', 'Subwoofer Level', (
                (SendCommand, 'fnPSSWL_ON', 'Main Zone Other Settings Subwoofer Level On', 'Main Zone Other Settings Subwoofer Level On', ['PSSWL ON', 'PSSWL ON']),
                (SendCommand, 'fnPSSWL_OFF', 'Main Zone Other Settings Subwoofer Level Off', 'Main Zone Other Settings Subwoofer Level Off', ['PSSWL OFF', 'PSSWL OFF']),
                (SendCommand, 'fnPSSWL_UP', 'Main Zone Other Settings Subwoofer Level Up', 'Main Zone Other Settings Subwoofer Level Up', ['PSSWL UP', 'PSSWL UP']),
                (SendCommand, 'fnPSSWL_DOWN', 'Main Zone Other Settings Subwoofer Level Down', 'Main Zone Other Settings Subwoofer Level Down', ['PSSWL DOWN', 'PSSWL DOWN']),
                (SendCommand, 'fnPSSWL_INPUT', 'Main Zone Other Settings Subwoofer Level Input', 'Main Zone Other Settings Subwoofer Level Input', ['PSSWL **', 'PSSWL 50']),
                (SendCommand, 'fnPSSWL_STATUS', 'Main Zone Other Settings Subwoofer Level Status', 'Main Zone Other Settings Subwoofer Level Status', ['PSSWL ?', 'PSSWL ?']),
            )),
            (eg.ActionGroup, 'gpSubwoofer2Level', 'Subwoofer 2 Level', 'Subwoofer 2 Level', (
                (SendCommand, 'fnPSSWL2_UP', 'Main Zone Other Settings Subwoofer 2 Level Up', 'Main Zone Other Settings Subwoofer 2 Level Up', ['PSSWL2 UP', 'PSSWL2 UP']),
                (SendCommand, 'fnPSSWL2_DOWN', 'Main Zone Other Settings Subwoofer 2 Level Down', 'Main Zone Other Settings Subwoofer 2 Level Down', ['PSSWL2 DOWN', 'PSSWL2 DOWN']),
                (SendCommand, 'fnPSSWL2_INPUT', 'Main Zone Other Settings Subwoofer 2 Level Input', 'Main Zone Other Settings Subwoofer 2 Level Input', ['PSSWL2 **', 'PSSWL2 50']),
                (SendCommand, 'fnPSSWL_STATUS', 'Main Zone Other Settings Subwoofer 2 Level Status', 'Main Zone Other Settings Subwoofer 2 Level Status', ['PSSWL ?', 'PSSWL ?']),
            )),
            (eg.ActionGroup, 'gpCinemaEQ', 'Cinema EQ', 'Cinema EQ', (
                (SendCommand, 'fnPSCINEMA_EQ.ON', 'Main Zone Other Settings Cinema EQ On', 'Main Zone Other Settings Cinema EQ On', ['PSCINEMA EQ.ON', 'PSCINEMA EQ.ON']),
                (SendCommand, 'fnPSCINEMA_EQ.OFF', 'Main Zone Other Settings Cinema EQ Off', 'Main Zone Other Settings Cinema EQ Off', ['PSCINEMA EQ.OFF', 'PSCINEMA EQ.OFF']),
                (SendCommand, 'fnPSCINEMA_EQ._STATUS', 'Main Zone Other Settings Cinema EQ Status', 'Main Zone Other Settings Cinema EQ Status', ['PSCINEMA EQ. ?', 'PSCINEMA EQ. ?']),
            )),
            (eg.ActionGroup, 'gpLoudnessManagement', 'Loudness Management', 'Loudness Management', (
                (SendCommand, 'fnPSPSLOM_ON', 'Main Zone Other Settings Loudness Management On', 'Main Zone Other Settings Loudness Management On', ['PSPSLOM ON', 'PSLOM ON']),
                (SendCommand, 'fnPSPSLOM_OFF', 'Main Zone Other Settings Loudness Management Off', 'Main Zone Other Settings Loudness Management Off', ['PSPSLOM OFF', 'PSLOM OFF']),
                (SendCommand, 'fnPSPSLOM_STATUS', 'Main Zone Other Settings Loudness Management Status', 'Main Zone Other Settings Loudness Management Status', ['PSPSLOM ?', 'PSLOM ?']),
            )),
            (eg.ActionGroup, 'gpSP', 'SP', 'SP', (
                (SendCommand, 'fnPSSP:FL', 'Main Zone Other Settings SP Floor', 'Main Zone Other Settings SP Floor', ['PSSP:FL', 'PSSP:FL']),
                (SendCommand, 'fnPSSP:HF', 'Main Zone Other Settings SP Height & Floor', 'Main Zone Other Settings SP Height & Floor', ['PSSP:HF', 'PSSP:HF']),
                (SendCommand, 'fnPSSP:FR', 'Main Zone Other Settings SP Front', 'Main Zone Other Settings SP Front', ['PSSP:FR', 'PSSP:FR']),
                (SendCommand, 'fnPSSP:_STATUS', 'Main Zone Other Settings SP Status', 'Main Zone Other Settings SP Status', ['PSSP: ?', 'PSSP: ?']),
            )),
            (eg.ActionGroup, 'gpMultiEQ', 'Multi EQ', 'Multi EQ', (
                (SendCommand, 'fnPSMULTEQ:AUDYSSEY', 'Main Zone Other Settings Multi EQ Audyssey', 'Main Zone Other Settings Multi EQ Audyssey', ['PSMULTEQ:AUDYSSEY', 'PSMULTEQ:AUDYSSEY']),
                (SendCommand, 'fnPSMULTEQ:BYP.LR', 'Main Zone Other Settings Multi EQ Bypass', 'Main Zone Other Settings Multi EQ Bypass', ['PSMULTEQ:BYP.LR', 'PSMULTEQ:BYP.LR']),
                (SendCommand, 'fnPSMULTEQ:FLAT', 'Main Zone Other Settings Multi EQ Flat', 'Main Zone Other Settings Multi EQ Flat', ['PSMULTEQ:FLAT', 'PSMULTEQ:FLAT']),
                (SendCommand, 'fnPSMULTEQ:OFF', 'Main Zone Other Settings Multi EQ Off', 'Main Zone Other Settings Multi EQ Off', ['PSMULTEQ:OFF', 'PSMULTEQ:OFF']),
                (SendCommand, 'fnPSMULTEQ_STATUS', 'Main Zone Other Settings Multi EQ Status', 'Main Zone Other Settings Multi EQ Status', ['PSMULTEQ ?', 'PSMULTEQ: ?']),
            )),
            (eg.ActionGroup, 'gpDynamicEQ', 'Dynamic EQ', 'Dynamic EQ', (
                (SendCommand, 'fnPSDYNEQ_ON', 'Main Zone Other Settings Dynamic EQ On', 'Main Zone Other Settings Dynamic EQ On', ['PSDYNEQ ON', 'PSDYNEQ ON']),
                (SendCommand, 'fnPSDYNEQ_OFF', 'Main Zone Other Settings Dynamic EQ Off', 'Main Zone Other Settings Dynamic EQ Off', ['PSDYNEQ OFF', 'PSDYNEQ OFF']),
                (SendCommand, 'fnPSDYNEQ_STATUS', 'Main Zone Other Settings Dynamic EQ Status', 'Main Zone Other Settings Dynamic EQ Status', ['PSDYNEQ ?', 'PSDYNEQ ?']),
            )),
            (eg.ActionGroup, 'gpReferenceLevelOffset', 'Reference Level Offset', 'Reference Level Offset', (
                (SendCommand, 'fnPSREFLEV_0', 'Main Zone Other Settings Reference Level Offset 0dB', 'Main Zone Other Settings Reference Level Offset 0dB', ['PSREFLEV 0', 'PSREFLEV 0']),
                (SendCommand, 'fnPSREFLEV_5', 'Main Zone Other Settings Reference Level Offset 5dB', 'Main Zone Other Settings Reference Level Offset 5dB', ['PSREFLEV 5', 'PSREFLEV 5']),
                (SendCommand, 'fnPSREFLEV_10', 'Main Zone Other Settings Reference Level Offset 10dB', 'Main Zone Other Settings Reference Level Offset 10dB', ['PSREFLEV 10', 'PSREFLEV 10']),
                (SendCommand, 'fnPSREFLEV_15', 'Main Zone Other Settings Reference Level Offset 15dB', 'Main Zone Other Settings Reference Level Offset 15dB', ['PSREFLEV 15', 'PSREFLEV 15']),
                (SendCommand, 'fnPSREFREV_STATUS', 'Main Zone Other Settings Reference Level Offset Status', 'Main Zone Other Settings Reference Level Offset Status', ['PSREFREV ?', 'PSREFLEV ?']),
            )),
            (eg.ActionGroup, 'gpDynamicVolume', 'Dynamic Volume', 'Dynamic Volume', (
                (SendCommand, 'fnPSDYNVOL_HEV', 'Main Zone Other Settings Dynamic Volume Heavy', 'Main Zone Other Settings Dynamic Volume Heavy', ['PSDYNVOL HEV', 'PSDYNVOL HEV']),
                (SendCommand, 'fnPSDYNVOL_MED', 'Main Zone Other Settings Dynamic Volume Medium', 'Main Zone Other Settings Dynamic Volume Medium', ['PSDYNVOL MED', 'PSDYNVOL MED']),
                (SendCommand, 'fnPSDYNVOL_LIT', 'Main Zone Other Settings Dynamic Volume Light', 'Main Zone Other Settings Dynamic Volume Light', ['PSDYNVOL LIT', 'PSDYNVOL LIT']),
                (SendCommand, 'fnPSDYNVOL_OFF', 'Main Zone Other Settings Dynamic Volume Off', 'Main Zone Other Settings Dynamic Volume Off', ['PSDYNVOL OFF', 'PSDYNVOL OFF']),
                (SendCommand, 'fnPSDYNVOL_STATUS', 'Main Zone Other Settings Dynamic Volume Status', 'Main Zone Other Settings Dynamic Volume Status', ['PSDYNVOL ?', 'PSDYNVOL ?']),
            )),
            (eg.ActionGroup, 'gpAudysseyLFC', 'Audyssey LFC', 'Audyssey LFC', (
                (SendCommand, 'fnPSLFC_ON', 'Main Zone Other Settings Audyssey LFC On', 'Main Zone Other Settings Audyssey LFC On', ['PSLFC ON', 'PSLFC ON']),
                (SendCommand, 'fnPSLFC_OFF', 'Main Zone Other Settings Audyssey LFC Off', 'Main Zone Other Settings Audyssey LFC Off', ['PSLFC OFF', 'PSLFC OFF']),
                (SendCommand, 'fnPSLFC_STATUS', 'Main Zone Other Settings Audyssey LFC Status', 'Main Zone Other Settings Audyssey LFC Status', ['PSLFC ?', 'PSLFC ?']),
            )),
            (eg.ActionGroup, 'gpContainment', 'Containment', 'Containment', (
                (SendCommand, 'fnPSCNTAMT_UP', 'Main Zone Other Settings Containment Up', 'Main Zone Other Settings Containment Up', ['PSCNTAMT UP', 'PSCNTAMT UP']),
                (SendCommand, 'fnPSCNTAMT_DOWN', 'Main Zone Other Settings Containment Down', 'Main Zone Other Settings Containment Down', ['PSCNTAMT DOWN', 'PSCNTAMT DOWN']),
                (SendCommand, 'fnPSCNTAMT_INPUT', 'Main Zone Other Settings Containment Input', 'Main Zone Other Settings Containment Input', ['PSCNTAMT **', 'PSCNTAMT 01']),
                (SendCommand, 'fnPSCNTAMT_STATUS', 'Main Zone Other Settings Containment Status', 'Main Zone Other Settings Containment Status', ['PSCNTAMT ?', 'PSCNTAMT ?']),
            )),
            (eg.ActionGroup, 'gpAudysseyDSX', 'Audyssey DSX', 'Audyssey DSX', (
                (SendCommand, 'fnPSDSX_ONHW', 'Main Zone Other Settings Audyssey DSX Height and Wide', 'Main Zone Other Settings Audyssey DSX Height and Wide', ['PSDSX ONHW', 'PSDSX ONHW']),
                (SendCommand, 'fnPSDSX_ONH', 'Main Zone Other Settings Audyssey DSX Height', 'Main Zone Other Settings Audyssey DSX Height', ['PSDSX ONH', 'PSDSX ONH']),
                (SendCommand, 'fnPSDSX_ONW', 'Main Zone Other Settings Audyssey DSX Wide', 'Main Zone Other Settings Audyssey DSX Wide', ['PSDSX ONW', 'PSDSX ONW']),
                (SendCommand, 'fnPSDSX_OFF', 'Main Zone Other Settings Audyssey DSX Off', 'Main Zone Other Settings Audyssey DSX Off', ['PSDSX OFF', 'PSDSX OFF']),
                (SendCommand, 'fnPSDSX_STATUS', 'Main Zone Other Settings Audyssey DSX Status', 'Main Zone Other Settings Audyssey DSX Status', ['PSDSX ?', 'PSDSX ?']),
            )),
            (eg.ActionGroup, 'gpStageWidth', 'Stage Width', 'Stage Width', (
                (SendCommand, 'fnPSSTW_UP', 'Main Zone Other Settings Stage Width Up', 'Main Zone Other Settings Stage Width Up', ['PSSTW UP', 'PSSTW UP']),
                (SendCommand, 'fnPSSTW_DOWN', 'Main Zone Other Settings Stage Width Down', 'Main Zone Other Settings Stage Width Down', ['PSSTW DOWN', 'PSSTW DOWN']),
                (SendCommand, 'fnPSSTW_INPUT', 'Main Zone Other Settings Stage Width Input', 'Main Zone Other Settings Stage Width Input', ['PSSTW **', 'PSSTW 50']),
                (SendCommand, 'fnPSSTW_STATUS', 'Main Zone Other Settings Stage Width Status', 'Main Zone Other Settings Stage Width Status', ['PSSTW ?', 'PSSTW ?']),
            )),
            (eg.ActionGroup, 'gpStageHeight', 'Stage Height', 'Stage Height', (
                (SendCommand, 'fnPSSTH_UP', 'Main Zone Other Settings Stage Height Up', 'Main Zone Other Settings Stage Height Up', ['PSSTH UP', 'PSSTH UP']),
                (SendCommand, 'fnPSSTH_DOWN', 'Main Zone Other Settings Stage Height Down', 'Main Zone Other Settings Stage Height Down', ['PSSTH DOWN', 'PSSTH DOWN']),
                (SendCommand, 'fnPSSTH_INPUT', 'Main Zone Other Settings Stage Height Input', 'Main Zone Other Settings Stage Height Input', ['PSSTH **', 'PSSTH 50']),
                (SendCommand, 'fnPSSTH_STATUS', 'Main Zone Other Settings Stage Height Status', 'Main Zone Other Settings Stage Height Status', ['PSSTH ?', 'PSSTH ?']),
            )),
            (eg.ActionGroup, 'gpGraphicEQ', 'Graphic EQ', 'Graphic EQ', (
                (SendCommand, 'fnPSGEQ_ON', 'Main Zone Other Settings Graphic EQ On', 'Main Zone Other Settings Graphic EQ On', ['PSGEQ ON', 'PSGEQ ON']),
                (SendCommand, 'fnPSGEQ_OFF', 'Main Zone Other Settings Graphic EQ Off', 'Main Zone Other Settings Graphic EQ Off', ['PSGEQ OFF', 'PSGEQ OFF']),
                (SendCommand, 'fnPSGEQ_STATUS', 'Main Zone Other Settings Graphic EQ Status', 'Main Zone Other Settings Graphic EQ Status', ['PSGEQ ?', 'PSGEQ ?']),
            )),
            (eg.ActionGroup, 'gpHeadphoneEQ', 'Headphone EQ', 'Headphone EQ', (
                (SendCommand, 'fnPSHEQ_ON', 'Main Zone Other Settings Headphone EQ On', 'Main Zone Other Settings Headphone EQ On', ['PSHEQ ON', 'PSHEQ ON']),
                (SendCommand, 'fnPSHEQ_OFF', 'Main Zone Other Settings Headphone EQ Off', 'Main Zone Other Settings Headphone EQ Off', ['PSHEQ OFF', 'PSHEQ OFF']),
                (SendCommand, 'fnPSHEQ_STATUS', 'Main Zone Other Settings Headphone EQ Status', 'Main Zone Other Settings Headphone EQ Status', ['PSHEQ ?', 'PSHEQ ?']),
            )),
            (eg.ActionGroup, 'gpDynamicCompression', 'Dynamic Compression', 'Dynamic Compression', (
                (SendCommand, 'fnPSDRC_AUTO', 'Main Zone Other Settings Dynamic Compression Auto', 'Main Zone Other Settings Dynamic Compression Auto', ['PSDRC AUTO', 'PSDRC AUTO']),
                (SendCommand, 'fnPSDRC_LOW', 'Main Zone Other Settings Dynamic Compression Low', 'Main Zone Other Settings Dynamic Compression Low', ['PSDRC LOW ', 'PSDRC LOW']),
                (SendCommand, 'fnPSDRC_MID', 'Main Zone Other Settings Dynamic Compression Mid', 'Main Zone Other Settings Dynamic Compression Mid', ['PSDRC MID', 'PSDRC MID']),
                (SendCommand, 'fnPSDRC_HI', 'Main Zone Other Settings Dynamic Compression Hi', 'Main Zone Other Settings Dynamic Compression Hi', ['PSDRC HI', 'PSDRC HI']),
                (SendCommand, 'fnPSDRC_OFF', 'Main Zone Other Settings Dynamic Compression Off', 'Main Zone Other Settings Dynamic Compression Off', ['PSDRC OFF', 'PSDRC OFF']),
                (SendCommand, 'fnPSDRC_STATUS', 'Main Zone Other Settings Dynamic Compression Status', 'Main Zone Other Settings Dynamic Compression Status', ['PSDRC ?', 'PSDRC ?']),
            )),
            (eg.ActionGroup, 'gpDialogControl', 'Dialog Control', 'Dialog Control', (
                (SendCommand, 'fnPSDIC_UP', 'Main Zone Other Settings Dialog Control Up', 'Main Zone Other Settings Dialog Control Up', ['PSDIC UP', 'PSDIC UP']),
                (SendCommand, 'fnPSDIC_DOWN', 'Main Zone Other Settings Dialog Control Down', 'Main Zone Other Settings Dialog Control Down', ['PSDIC DOWN', 'PSDIC DOWN']),
                (SendCommand, 'fnPSDIC_INPUT', 'Main Zone Other Settings Dialog Control Input', 'Main Zone Other Settings Dialog Control Input', ['PSDIC **', 'PSDIC 03']),
                (SendCommand, 'fnPSDIC_STATUS', 'Main Zone Other Settings Dialog Control Status', 'Main Zone Other Settings Dialog Control Status', ['PSDIC ?', 'PSDIC ?']),
            )),
            (eg.ActionGroup, 'gpBassSync', 'Bass Sync', 'Bass Sync', (
                (SendCommand, 'fnPSBSC_UP', 'Main Zone Other Settings Bass Sync Up', 'Main Zone Other Settings Bass Sync Up', ['PSBSC UP', 'PSBSC UP']),
                (SendCommand, 'fnPSBSC_DOWN', 'Main Zone Other Settings Bass Sync Down', 'Main Zone Other Settings Bass Sync Down', ['PSBSC DOWN', 'PSBSC DOWN']),
                (SendCommand, 'fnPSBSC_INPUT', 'Main Zone Other Settings Bass Sync Input', 'Main Zone Other Settings Bass Sync Input', ['PSBSC **', 'PSBSC 10']),
                (SendCommand, 'fnPSBSC_STATUS', 'Main Zone Other Settings Bass Sync Status', 'Main Zone Other Settings Bass Sync Status', ['PSBSC ?', 'PSBSC ?']),
            )),
            (eg.ActionGroup, 'gpDialogEnhancer', 'Dialog Enhancer', 'Dialog Enhancer', (
                (SendCommand, 'fnPSDEH_OFF', 'Main Zone Other Settings Dialog Enhancer Off', 'Main Zone Other Settings Dialog Enhancer Off', ['PSDEH OFF', 'PSDEH OFF']),
                (SendCommand, 'fnPSDEH_LOW', 'Main Zone Other Settings Dialog Enhancer Low', 'Main Zone Other Settings Dialog Enhancer Low', ['PSDEH LOW', 'PSDEH LOW']),
                (SendCommand, 'fnPSDEH_MED', 'Main Zone Other Settings Dialog Enhancer Medium', 'Main Zone Other Settings Dialog Enhancer Medium', ['PSDEH MED', 'PSDEH MED']),
                (SendCommand, 'fnPSDEH_HIGH', 'Main Zone Other Settings Dialog Enhancer Hight', 'Main Zone Other Settings Dialog Enhancer Hight', ['PSDEH HIGH', 'PSDEH HIGH']),
                (SendCommand, 'fnPSDEH_STATUS', 'Main Zone Other Settings Dialog Enhancer Status', 'Main Zone Other Settings Dialog Enhancer Status', ['PSDEH ?', 'PSDEH ?']),
            )),
            (eg.ActionGroup, 'gpLFE', 'LFE', 'LFE', (
                (SendCommand, 'fnPSLFE_UP', 'Main Zone Other Settings LFE Up', 'Main Zone Other Settings LFE Up', ['PSLFE UP', 'PSLEE UP']),
                (SendCommand, 'fnPSLFE_DOWN', 'Main Zone Other Settings LFE Down', 'Main Zone Other Settings LFE Down', ['PSLFE DOWN', 'PSLFE DOWN']),
                (SendCommand, 'fnPSLFE_INPUT', 'Main Zone Other Settings LFE Input', 'Main Zone Other Settings LFE Input', ['PSLFE **', 'PSLFE 10']),
                (SendCommand, 'fnPSLFE_STATUS', 'Main Zone Other Settings LFE Status', 'Main Zone Other Settings LFE Status', ['PSLFE ?', 'PSLFE ?']),
            )),
            (eg.ActionGroup, 'gpLFELevel', 'LFE Level', 'LFE Level', (
                (SendCommand, 'fnPSLFL_00', 'Main Zone Other Settings LFE Level 00', 'Main Zone Other Settings LFE Level 00', ['PSLFL 00', 'PSLFL 00']),
                (SendCommand, 'fnPSLFL_05', 'Main Zone Other Settings LFE Level 05', 'Main Zone Other Settings LFE Level 05', ['PSLFL 05', 'PSLFL 05']),
                (SendCommand, 'fnPSLFL_10', 'Main Zone Other Settings LFE Level 10', 'Main Zone Other Settings LFE Level 10', ['PSLFL 10', 'PSLFL 10']),
                (SendCommand, 'fnPSLFL_15', 'Main Zone Other Settings LFE Level 15', 'Main Zone Other Settings LFE Level 15', ['PSLFL 15', 'PSLFL 15']),
                (SendCommand, 'fnPSLFL_STATUS', 'Main Zone Other Settings LFE Level Status', 'Main Zone Other Settings LFE Level Status', ['PSLFL ?', 'PSLFL ?']),
            )),
            (eg.ActionGroup, 'gpEffectLevel', 'Effect Level', 'Effect Level', (
                (SendCommand, 'fnPSEFF_ON', 'Main Zone Other Settings Effect Level On', 'Main Zone Other Settings Effect Level On', ['PSEFF ON', 'PSEFF ON']),
                (SendCommand, 'fnPSEFF_OFF', 'Main Zone Other Settings Effect Level Off', 'Main Zone Other Settings Effect Level Off', ['PSEFF OFF', 'PSEFF OFF']),
                (SendCommand, 'fnPSEFF_UP', 'Main Zone Other Settings Effect Level Up', 'Main Zone Other Settings Effect Level Up', ['PSEFF UP', 'PSEFF UP']),
                (SendCommand, 'fnPSEFF_DOWN', 'Main Zone Other Settings Effect Level Down', 'Main Zone Other Settings Effect Level Down', ['PSEFF DOWN', 'PSEFF DOWN']),
                (SendCommand, 'fnPSEFF_INPUT', 'Main Zone Other Settings Effect Level Input', 'Main Zone Other Settings Effect Level Input', ['PSEFF **', 'PSEFF 10']),
                (SendCommand, 'fnPSEFF_STATUS', 'Main Zone Other Settings Effect Level Status', 'Main Zone Other Settings Effect Level Status', ['PSEFF ?', 'PSEFF ?']),
            )),
            (eg.ActionGroup, 'gpDelay', 'Delay', 'Delay', (
                (SendCommand, 'fnPSDEL_UP', 'Main Zone Other Settings Delay Up', 'Main Zone Other Settings Delay Up', ['PSDEL UP', 'PSDEL UP']),
                (SendCommand, 'fnPSDEL_DOWN', 'Main Zone Other Settings Delay Down', 'Main Zone Other Settings Delay Down', ['PSDEL DOWN', 'PSDEL DOWN']),
                (SendCommand, 'fnPSDEL_INPUT', 'Main Zone Other Settings Delay Input', 'Main Zone Other Settings Delay Input', ['PSDEL ***', 'PSDEL 000']),
                (SendCommand, 'fnPSDEL_STATUS', 'Main Zone Other Settings Delay Status', 'Main Zone Other Settings Delay Status', ['PSDEL ?', 'PSDEL ?']),
            )),
            (eg.ActionGroup, 'gpCenterSpread', 'Center Spread', 'Center Spread', (
                (SendCommand, 'fnPSCES_ON', 'Main Zone Other Settings Center Spread On', 'Main Zone Other Settings Center Spread On', ['PSCES ON', 'PSCES ON']),
                (SendCommand, 'fnPSCES_OFF', 'Main Zone Other Settings Center Spread Off', 'Main Zone Other Settings Center Spread Off', ['PSCES OFF', 'PSCES OFF']),
                (SendCommand, 'fnPSCES_STATUS', 'Main Zone Other Settings Center Spread Status', 'Main Zone Other Settings Center Spread Status', ['PSCES ?', 'PSCES ?']),
            )),
            (eg.ActionGroup, 'gpNeutral:X', 'Neutral:X', 'Neutral:X', (
                (SendCommand, 'fnPSNEURAL_ON', 'Main Zone Other Settings Neutral:X On', 'Main Zone Other Settings Neutral:X On', ['PSNEURAL ON', 'PSNEURAL ON']),
                (SendCommand, 'fnPSNEURAL_OFF', 'Main Zone Other Settings Neutral:X Off', 'Main Zone Other Settings Neutral:X Off', ['PSNEURAL OFF', 'PSNEURAL OFF']),
                (SendCommand, 'fnPSNEURAL_STATUS', 'Main Zone Other Settings Neutral:X Status', 'Main Zone Other Settings Neutral:X Status', ['PSNEURAL ?', 'PSNEURAL ?']),
            )),
            (eg.ActionGroup, 'gpSobwoofer', 'Sobwoofer', 'Sobwoofer', (
                (SendCommand, 'fnPSSWR_ON', 'Main Zone Other Settings Sobwoofer On', 'Main Zone Other Settings Sobwoofer On', ['PSSWR ON', 'PSSWR ON']),
                (SendCommand, 'fnPSSWR_OFF', 'Main Zone Other Settings Sobwoofer Off', 'Main Zone Other Settings Sobwoofer Off', ['PSSWR OFF', 'PSSWR OFF']),
                (SendCommand, 'fnPSSWR_STATUS', 'Main Zone Other Settings Sobwoofer Status', 'Main Zone Other Settings Sobwoofer Status', ['PSSWR ? ', 'PSSWR ?']),
            )),
            (eg.ActionGroup, 'gpRoomSize', 'Room Size', 'Room Size', (
                (SendCommand, 'fnPSRSZ_S', 'Main Zone Other Settings Room Size Small', 'Main Zone Other Settings Room Size Small', ['PSRSZ S', 'PSRSZ S']),
                (SendCommand, 'fnPSRSZ_MS', 'Main Zone Other Settings Room Size Medium Small', 'Main Zone Other Settings Room Size Medium Small', ['PSRSZ MS', 'PSRSZ MS']),
                (SendCommand, 'fnPSRSZ_M', 'Main Zone Other Settings Room Size Medium', 'Main Zone Other Settings Room Size Medium', ['PSRSZ M', 'PSRSZ M']),
                (SendCommand, 'fnPSRSZ_ML', 'Main Zone Other Settings Room Size Medium Large', 'Main Zone Other Settings Room Size Medium Large', ['PSRSZ ML', 'PSRSZ ML']),
                (SendCommand, 'fnPSRSZ_L', 'Main Zone Other Settings Room Size Large', 'Main Zone Other Settings Room Size Large', ['PSRSZ L', 'PSRSZ L']),
                (SendCommand, 'fnPSRSZ_STATUS', 'Main Zone Other Settings Room Size Status', 'Main Zone Other Settings Room Size Status', ['PSRSZ ?', 'PSRSZ ?']),
            )),
            (eg.ActionGroup, 'gpAudioDelay', 'Audio Delay', 'Audio Delay', (
                (SendCommand, 'fnPSDELAY_UP', 'Main Zone Other Settings Audio Delay Up', 'Main Zone Other Settings Audio Delay Up', ['PSDELAY UP', 'PSDELAY UP']),
                (SendCommand, 'fnPSDELAY_DOWN', 'Main Zone Other Settings Audio Delay Down', 'Main Zone Other Settings Audio Delay Down', ['PSDELAY DOWN', 'PSDELAY DOWN']),
                (SendCommand, 'fnPSDELAY_INPUT', 'Main Zone Other Settings Audio Delay Input', 'Main Zone Other Settings Audio Delay Input', ['PSDELAY ***', 'PSDELAY 200']),
                (SendCommand, 'fnPSDELAYSTATUS', 'Main Zone Other Settings Audio Delay Status', 'Main Zone Other Settings Audio Delay Status', ['PSDELAY?', 'PSDELAY ?']),
            )),
            (eg.ActionGroup, 'gpAudioRestorer', 'Audio Restorer', 'Audio Restorer', (
                (SendCommand, 'fnPSRSTR_OFF', 'Main Zone Other Settings Audio Restorer Off', 'Main Zone Other Settings Audio Restorer Off', ['PSRSTR OFF', 'PSRSTR OFF']),
                (SendCommand, 'fnPSRSTR_LOW', 'Main Zone Other Settings Audio Restorer Low', 'Main Zone Other Settings Audio Restorer Low', ['PSRSTR LOW', 'PSRSTR LOW']),
                (SendCommand, 'fnPSRSTR_MED', 'Main Zone Other Settings Audio Restorer Medium', 'Main Zone Other Settings Audio Restorer Medium', ['PSRSTR MED', 'PSRSTR MED']),
                (SendCommand, 'fnPSRSTR_HI', 'Main Zone Other Settings Audio Restorer High', 'Main Zone Other Settings Audio Restorer High', ['PSRSTR HI', 'PSRSTR HI']),
                (SendCommand, 'fnPSRSTR_STATUS', 'Main Zone Other Settings Audio Restorer Status', 'Main Zone Other Settings Audio Restorer Status', ['PSRSTR ?', 'PSRSTR ?']),
            )),
            (eg.ActionGroup, 'gpFrontSpeaker', 'Front Speaker', 'Front Speaker', (
                (SendCommand, 'fnPSFRONT_SPA', 'Main Zone Other Settings Front Speaker A', 'Main Zone Other Settings Front Speaker A', ['PSFRONT SPA', 'PSFRONT SPA']),
                (SendCommand, 'fnPSFRONT_SPB', 'Main Zone Other Settings Front Speaker B', 'Main Zone Other Settings Front Speaker B', ['PSFRONT SPB', 'PSFRONT SPB']),
                (SendCommand, 'fnPSFRONT_AB', 'Main Zone Other Settings Front Speaker A + B', 'Main Zone Other Settings Front Speaker A + B', ['PSFRONT A+B', 'PSFRONT A+B']),
                (SendCommand, 'fnPSFRONTSTATUS', 'Main Zone Other Settings Front Speaker Status', 'Main Zone Other Settings Front Speaker Status', ['PSFRONT?', 'PSFRONT?']),
            )),
            (eg.ActionGroup, 'gpAuroMatic3DPreset', 'Auro Matic 3D Preset', 'Auro Matic 3D Preset', (
                (SendCommand, 'fnPSAUROPR_SMA', 'Main Zone Other Settings Auro Matic 3D Preset Small', 'Main Zone Other Settings Auro Matic 3D Preset Small', ['PSAUROPR SMA', 'PSAUROPR SMA']),
                (SendCommand, 'fnPSAUROPR_MED', 'Main Zone Other Settings Auro Matic 3D Preset Medium', 'Main Zone Other Settings Auro Matic 3D Preset Medium', ['PSAUROPR MED', 'PSAUROPR MED']),
                (SendCommand, 'fnPSAUROPR_LAR', 'Main Zone Other Settings Auro Matic 3D Preset Large', 'Main Zone Other Settings Auro Matic 3D Preset Large', ['PSAUROPR LAR', 'PSAUROPR LAR']),
                (SendCommand, 'fnPSAUROPR_SPE', 'Main Zone Other Settings Auro Matic 3D Preset Special', 'Main Zone Other Settings Auro Matic 3D Preset Special', ['PSAUROPR SPE', 'PSAUROPR SPE']),
                (SendCommand, 'fnPSAUROPR_STATUS', 'Main Zone Other Settings Auro Matic 3D Preset Status', 'Main Zone Other Settings Auro Matic 3D Preset Status', ['PSAUROPR ?', 'PSAUROPR ?']),
            )),
            (eg.ActionGroup, 'gpAuroMaticStrength', 'Auro Matic Strength', 'Auro Matic Strength', (
                (SendCommand, 'fnPSAUROST_UP', 'Main Zone Other Settings Auro Matic Strength Up', 'Main Zone Other Settings Auro Matic Strength Up', ['PSAUROST UP', 'PSAUROST UP']),
                (SendCommand, 'fnPSAUROST_DOWN', 'Main Zone Other Settings Auro Matic Strength Down', 'Main Zone Other Settings Auro Matic Strength Down', ['PSAUROST DOWN', 'PSAUROST DOWN']),
                (SendCommand, 'fnPSAUROST_INPUT', 'Main Zone Other Settings Auro Matic Strength Input', 'Main Zone Other Settings Auro Matic Strength Input', ['PSAUROST **', 'PSAUROST **']),
                (SendCommand, 'fnPSAUROST_STATUS', 'Main Zone Other Settings Auro Matic Strength Status', 'Main Zone Other Settings Auro Matic Strength Status', ['PSAUROST ?', 'PSAUROST ?']),
            )),
        )),
        (eg.ActionGroup, 'gpPictureSettings', 'Picture Settings', 'Picture Settings', (
            (eg.ActionGroup, 'gpMode', 'Mode', 'Mode', (
                (SendCommand, 'fnPVOFF', 'Main Zone Picture Settings Mode Off', 'Main Zone Picture Settings Mode Off', ['PVOFF', 'PVOFF']),
                (SendCommand, 'fnPVSTD', 'Main Zone Picture Settings Mode Standard', 'Main Zone Picture Settings Mode Standard', ['PVSTD', 'PVSTD']),
                (SendCommand, 'fnPVMOV', 'Main Zone Picture Settings Mode Movie', 'Main Zone Picture Settings Mode Movie', ['PVMOV', 'PVMOV']),
                (SendCommand, 'fnPVVVD', 'Main Zone Picture Settings Mode Vivid', 'Main Zone Picture Settings Mode Vivid', ['PVVVD', 'PVVVD']),
                (SendCommand, 'fnPVSTM', 'Main Zone Picture Settings Mode Stream', 'Main Zone Picture Settings Mode Stream', ['PVSTM', 'PVSTM']),
                (SendCommand, 'fnPVCTM', 'Main Zone Picture Settings Mode Cinema', 'Main Zone Picture Settings Mode Cinema', ['PVCTM', 'PVCTM']),
                (SendCommand, 'fnPVDAY', 'Main Zone Picture Settings Mode Day', 'Main Zone Picture Settings Mode Day', ['PVDAY', 'PVDAY']),
                (SendCommand, 'fnPVNGT', 'Main Zone Picture Settings Mode Night', 'Main Zone Picture Settings Mode Night', ['PVNGT', 'PVNGT']),
                (SendCommand, 'fnPVSTATUS', 'Main Zone Picture Settings Mode Status', 'Main Zone Picture Settings Mode Status', ['PV?', 'PV?']),
            )),
            (eg.ActionGroup, 'gpContrast', 'Contrast', 'Contrast', (
                (SendCommand, 'fnPVCN_UP', 'Main Zone Picture Settings Contrast Up', 'Main Zone Picture Settings Contrast Up', ['PVCN UP', 'PVCN UP']),
                (SendCommand, 'fnPVCN_DOWN', 'Main Zone Picture Settings Contrast Down', 'Main Zone Picture Settings Contrast Down', ['PVCN DOWN', 'PVCN DOWN']),
                (SendCommand, 'fnPVCN_INPUT', 'Main Zone Picture Settings Contrast Input', 'Main Zone Picture Settings Contrast Input', ['PVCN ***', 'PVCN 050']),
                (SendCommand, 'fnPVCN_STATUS', 'Main Zone Picture Settings Contrast Status', 'Main Zone Picture Settings Contrast Status', ['PVCN ?', 'PVCN ?']),
            )),
            (eg.ActionGroup, 'gpBrightness', 'Brightness', 'Brightness', (
                (SendCommand, 'fnPVBR_UP', 'Main Zone Picture Settings Brightness Up', 'Main Zone Picture Settings Brightness Up', ['PVBR UP', 'PVBR UP']),
                (SendCommand, 'fnPVBR_DOWN', 'Main Zone Picture Settings Brightness Down', 'Main Zone Picture Settings Brightness Down', ['PVBR DOWN', 'PVBR DOWN']),
                (SendCommand, 'fnPVBR_INPUT', 'Main Zone Picture Settings Brightness Input', 'Main Zone Picture Settings Brightness Input', ['PVBR ***', 'PVBR 050']),
                (SendCommand, 'fnPVBR_STATUS', 'Main Zone Picture Settings Brightness Status', 'Main Zone Picture Settings Brightness Status', ['PVBR ?', 'PVBR ?']),
            )),
            (eg.ActionGroup, 'gpChromaLevel', 'Chroma Level', 'Chroma Level', (
                (SendCommand, 'fnPVST_UP', 'Main Zone Picture Settings Chroma Level Up', 'Main Zone Picture Settings Chroma Level Up', ['PVST UP', 'PVST UP']),
                (SendCommand, 'fnPVST_DOWN', 'Main Zone Picture Settings Chroma Level Down', 'Main Zone Picture Settings Chroma Level Down', ['PVST DOWN', 'PVST DOWN']),
                (SendCommand, 'fnPVST_INPUT', 'Main Zone Picture Settings Chroma Level Input', 'Main Zone Picture Settings Chroma Level Input', ['PVST ***', 'PVST 050']),
                (SendCommand, 'fnPVST_STATUS', 'Main Zone Picture Settings Chroma Level Status', 'Main Zone Picture Settings Chroma Level Status', ['PVST ?', 'PVST ?']),
            )),
            (eg.ActionGroup, 'gpDynamicNoiseReduction', 'Dynamic Noise Reduction', 'Dynamic Noise Reduction', (
                (SendCommand, 'fnPVDNR_OFF', 'Main Zone Picture Settings Dynamic Noise Reduction Off', 'Main Zone Picture Settings Dynamic Noise Reduction Off', ['PVDNR OFF', 'PVDNR OFF']),
                (SendCommand, 'fnPVDNR_LOW', 'Main Zone Picture Settings Dynamic Noise Reduction Low', 'Main Zone Picture Settings Dynamic Noise Reduction Low', ['PVDNR LOW', 'PVDNR LOW']),
                (SendCommand, 'fnPVDNR_MID', 'Main Zone Picture Settings Dynamic Noise Reduction Middle', 'Main Zone Picture Settings Dynamic Noise Reduction Middle', ['PVDNR MID', 'PVDNR MID']),
                (SendCommand, 'fnPVDNR_HI', 'Main Zone Picture Settings Dynamic Noise Reduction High', 'Main Zone Picture Settings Dynamic Noise Reduction High', ['PVDNR HI', 'PVDNR HI']),
                (SendCommand, 'fnPVDNR_STATUS', 'Main Zone Picture Settings Dynamic Noise Reduction Status', 'Main Zone Picture Settings Dynamic Noise Reduction Status', ['PVDNR ?', 'PVDNR ?']),
            )),
            (eg.ActionGroup, 'gpEnhancer', 'Enhancer', 'Enhancer', (
                (SendCommand, 'fnPVENH_UP', 'Main Zone Picture Settings Enhancer Up', 'Main Zone Picture Settings Enhancer Up', ['PVENH UP', 'PVENH UP']),
                (SendCommand, 'fnPVENH_DOWN', 'Main Zone Picture Settings Enhancer Down', 'Main Zone Picture Settings Enhancer Down', ['PVENH DOWN', 'PVENH DOWN']),
                (SendCommand, 'fnPVENH_INPUT', 'Main Zone Picture Settings Enhancer Input', 'Main Zone Picture Settings Enhancer Input', ['PVENH ***', 'PVENH 12']),
                (SendCommand, 'fnPVENH_STATUS', 'Main Zone Picture Settings Enhancer Status', 'Main Zone Picture Settings Enhancer Status', ['PVENH ?', 'PVENH ?']),
            )),
        )),
    )),
    (eg.ActionGroup, 'gpZone2', 'Zone 2', 'Zone 2', (
        (eg.ActionGroup, 'gpInput', 'Input', 'Input', (
            (SendCommand, 'fnZ2SOURCE', 'Zone 2 Input Main Zone', 'Zone 2 Input Main Zone', ['Z2SOURCE', 'Z2SOURCE']),
            (SendCommand, 'fnZ2PHONO', 'Zone 2 Input Phono', 'Zone 2 Input Phono', ['Z2PHONO', 'Z2PHONO']),
            (SendCommand, 'fnZ2CD', 'Zone 2 Input CD', 'Zone 2 Input CD', ['Z2CD', 'Z2CD']),
            (SendCommand, 'fnZ2TUNER', 'Zone 2 Input Tuner', 'Zone 2 Input Tuner', ['Z2TUNER', 'Z2TUNER']),
            (SendCommand, 'fnZ2DVD', 'Zone 2 Input DVD', 'Zone 2 Input DVD', ['Z2DVD', 'Z2DVD']),
            (SendCommand, 'fnZ2BD', 'Zone 2 Input BluRay', 'Zone 2 Input BluRay', ['Z2BD', 'Z2BD']),
            (SendCommand, 'fnZ2TV', 'Zone 2 Input TV', 'Zone 2 Input TV', ['Z2TV', 'Z2TV']),
            (SendCommand, 'fnZ2SAT/CBL', 'Zone 2 Input Sat/Cable', 'Zone 2 Input Sat/Cable', ['Z2SAT/CBL', 'Z2SAT/CBL']),
            (SendCommand, 'fnZ2MPLAY', 'Zone 2 Input Media Player', 'Zone 2 Input Media Player', ['Z2MPLAY', 'Z2MPLAY']),
            (SendCommand, 'fnZ2GAME', 'Zone 2 Input Game', 'Zone 2 Input Game', ['Z2GAME', 'Z2GAME']),
            (SendCommand, 'fnZ2HDRADIO', 'Zone 2 Input HD Radio', 'Zone 2 Input HD Radio', ['Z2HDRADIO', 'Z2HDRADIO']),
            (SendCommand, 'fnZ2NET', 'Zone 2 Input Net', 'Zone 2 Input Net', ['Z2NET', 'Z2NET']),
            (SendCommand, 'fnZ2PANDORA', 'Zone 2 Input Pandora', 'Zone 2 Input Pandora', ['Z2PANDORA', 'Z2PANDORA']),
            (SendCommand, 'fnZ2SIRIUSXM', 'Zone 2 Input Sirius/XM', 'Zone 2 Input Sirius/XM', ['Z2SIRIUSXM', 'Z2SIRIUSXM']),
            (SendCommand, 'fnZ2IRADIO', 'Zone 2 Input Internet Radio', 'Zone 2 Input Internet Radio', ['Z2IRADIO', 'Z2IRADIO']),
            (SendCommand, 'fnZ2SERVER', 'Zone 2 Input Server', 'Zone 2 Input Server', ['Z2SERVER', 'Z2SERVER']),
            (SendCommand, 'fnZ2FAVORITES', 'Zone 2 Input Favorites', 'Zone 2 Input Favorites', ['Z2FAVORITES', 'Z2FAVORITES']),
            (SendCommand, 'fnZ2AUX1', 'Zone 2 Input Aux 1', 'Zone 2 Input Aux 1', ['Z2AUX1', 'Z2AUX1']),
            (SendCommand, 'fnZ2AUX2', 'Zone 2 Input Aux 2', 'Zone 2 Input Aux 2', ['Z2AUX2', 'Z2AUX2']),
            (SendCommand, 'fnZ2AUX3', 'Zone 2 Input Aux 3', 'Zone 2 Input Aux 3', ['Z2AUX3', 'Z2AUX3']),
            (SendCommand, 'fnZ2AUX4', 'Zone 2 Input Aux 4', 'Zone 2 Input Aux 4', ['Z2AUX4', 'Z2AUX4']),
            (SendCommand, 'fnZ2AUX5', 'Zone 2 Input Aux 5', 'Zone 2 Input Aux 5', ['Z2AUX5', 'Z2AUX5']),
            (SendCommand, 'fnZ2AUX6', 'Zone 2 Input Aux 6', 'Zone 2 Input Aux 6', ['Z2AUX6', 'Z2AUX6']),
            (SendCommand, 'fnZ2AUX7', 'Zone 2 Input Aux 7', 'Zone 2 Input Aux 7', ['Z2AUX7', 'Z2AUX7']),
            (SendCommand, 'fnZ2BT', 'Zone 2 Input Blue Teeth', 'Zone 2 Input Blue Teeth', ['Z2BT', 'Z2BT']),
            (SendCommand, 'fnZ2USB/IPOD', 'Zone 2 Input USB/IPOD', 'Zone 2 Input USB/IPOD', ['Z2USB/IPOD', 'Z2USB/IPOD']),
            (SendCommand, 'fnZ2USB', 'Zone 2 Input USB + Playback', 'Zone 2 Input USB + Playback', ['Z2USB', 'Z2USB']),
            (SendCommand, 'fnZ2IPD', 'Zone 2 Input IPOD + Playback', 'Zone 2 Input IPOD + Playback', ['Z2IPD', 'Z2IPD']),
            (SendCommand, 'fnZ2IRP', 'Zone 2 Input Internet Radio + Recent Playback', 'Zone 2 Input Internet Radio + Recent Playback', ['Z2IRP', 'Z2IRP']),
            (SendCommand, 'fnZ2FVP', 'Zone 2 Input Internet Radio + Favorites Playback', 'Zone 2 Input Internet Radio + Favorites Playback', ['Z2FVP', 'Z2FVP']),
            (eg.ActionGroup, 'gpQuickSelect', 'Quick Select', 'Quick Select', (
                (SendCommand, 'fnZ2QUICK1', 'Zone 2 Input Quick Select 1', 'Zone 2 Input Quick Select 1', ['Z2QUICK1', 'Z2QUICK1']),
                (SendCommand, 'fnZ2QUICK2', 'Zone 2 Input Quick Select 2', 'Zone 2 Input Quick Select 2', ['Z2QUICK2', 'Z2QUICK2']),
                (SendCommand, 'fnZ2QUICK3', 'Zone 2 Input Quick Select 3', 'Zone 2 Input Quick Select 3', ['Z2QUICK3', 'Z2QUICK3']),
                (SendCommand, 'fnZ2QUICK4', 'Zone 2 Input Quick Select 4', 'Zone 2 Input Quick Select 4', ['Z2QUICK4', 'Z2QUICK4']),
                (SendCommand, 'fnZ2QUICK5', 'Zone 2 Input Quick Select 5', 'Zone 2 Input Quick Select 5', ['Z2QUICK5', 'Z2QUICK5']),
                (SendCommand, 'fnZ2QUICK_STATUS', 'Zone 2 Input Quick Select Status', 'Zone 2 Input Quick Select Status', ['Z2QUICK ?', 'Z2QUICK ?']),
            )),
            (eg.ActionGroup, 'gpQuickMemorySelect', 'Quick Memory Select', 'Quick Memory Select', (
                (SendCommand, 'fnZ2QUICK1_MEMORYSTATUS', 'Zone 2 Input Quick Memory Select 1', 'Zone 2 Input Quick Memory Select 1', ['Z2QUICK1 MEMORY?', 'Z2QUICK1 MEMORY']),
                (SendCommand, 'fnZ2QUICK2_MEMORY', 'Zone 2 Input Quick Memory Select 2', 'Zone 2 Input Quick Memory Select 2', ['Z2QUICK2 MEMORY', 'Z2QUICK2 MEMORY']),
                (SendCommand, 'fnZ2QUICK3_MEMORY', 'Zone 2 Input Quick Memory Select 3', 'Zone 2 Input Quick Memory Select 3', ['Z2QUICK3 MEMORY', 'Z2QUICK3 MEMORY']),
                (SendCommand, 'fnZ2QUCIK4_MEMORY', 'Zone 2 Input Quick Memory Select 4', 'Zone 2 Input Quick Memory Select 4', ['Z2QUCIK4 MEMORY', 'Z2QUICK4 MEMORY']),
                (SendCommand, 'fnZ2QUICK5_MEMORY', 'Zone 2 Input Quick Memory Select 5', 'Zone 2 Input Quick Memory Select 5', ['Z2QUICK5 MEMORY', 'Z2QUICK5 MEMORY']),
                (SendCommand, 'fnZ2QUICK_STATUS', 'Zone 2 Input Quick Memory Select Status', 'Zone 2 Input Quick Memory Select Status', ['Z2QUICK ?', 'Z2QUICK ?']),
            )),
        )),
        (eg.ActionGroup, 'gpVolume', 'Volume', 'Volume', (
            (SendCommand, 'fnZ2UP', 'Zone 2 Volume Up', 'Zone 2 Volume Up', ['Z2UP', 'Z2UP']),
            (SendCommand, 'fnZ2DOWN', 'Zone 2 Volume Down', 'Zone 2 Volume Down', ['Z2DOWN', 'Z2DOWN']),
            (SendCommand, 'fnZ2INPUT', 'Zone 2 Volume Input', 'Zone 2 Volume Input', ['Z2**', 'Z280']),
        )),
        (eg.ActionGroup, 'gpPower', 'Power', 'Power', (
            (SendCommand, 'fnZ2ON', 'Zone 2 Power On', 'Zone 2 Power On', ['Z2ON', 'Z2ON']),
            (SendCommand, 'fnZ2OFF', 'Zone 2 Power Off', 'Zone 2 Power Off', ['Z2OFF', 'Z2OFF']),
            (SendCommand, 'fnZ2STATUS', 'Zone 2 Power Status', 'Zone 2 Power Status', ['Z2?', 'Z2?']),
        )),
        (eg.ActionGroup, 'gpMute', 'Mute', 'Mute', (
            (SendCommand, 'fnZ2MUON', 'Zone 2 Mute On', 'Zone 2 Mute On', ['Z2MUON', 'Z2MUON']),
            (SendCommand, 'fnZ2MUOFF', 'Zone 2 Mute Off', 'Zone 2 Mute Off', ['Z2MUOFF', 'Z2MUOFF']),
            (SendCommand, 'fnZ2MUSTATUS', 'Zone 2 Mute Status', 'Zone 2 Mute Status', ['Z2MU?', 'Z2MU?']),
        )),
        (eg.ActionGroup, 'gpSoundMode', 'Sound Mode', 'Sound Mode', (
            (SendCommand, 'fnZ2CSST', 'Zone 2 Sound Mode Stereo', 'Zone 2 Sound Mode Stereo', ['Z2CSST', 'Z2CSST']),
            (SendCommand, 'fnZ2CSMONO', 'Zone 2 Sound Mode Mono', 'Zone 2 Sound Mode Mono', ['Z2CSMONO', 'Z2CSMONO']),
            (SendCommand, 'fnZ2CSSTATUS', 'Zone 2 Sound Mode Status', 'Zone 2 Sound Mode Status', ['Z2CS?', 'Z2CS?']),
        )),
        (eg.ActionGroup, 'gpChannelVolume', 'Channel Volume', 'Channel Volume', (
            (eg.ActionGroup, 'gpFrontLeft', 'Front Left', 'Front Left', (
                (SendCommand, 'fnZ2CVFL_UP', 'Zone 2 Channel Volume Front Left Up', 'Zone 2 Channel Volume Front Left Up', ['Z2CVFL UP', 'Z2CVFL UP']),
                (SendCommand, 'fnZ2CVFL_DOWN', 'Zone 2 Channel Volume Front Left Down', 'Zone 2 Channel Volume Front Left Down', ['Z2CVFL DOWN', 'Z2CVFL DOWN']),
                (SendCommand, 'fnZ2CVFL_INPUT', 'Zone 2 Channel Volume Front Left Input', 'Zone 2 Channel Volume Front Left Input', ['Z2CVFL **', 'Z2CVFL 50']),
            )),
            (eg.ActionGroup, 'gpFrontRight', 'Front Right', 'Front Right', (
                (SendCommand, 'fnZ2CVFR_UP', 'Zone 2 Channel Volume Front Right Up', 'Zone 2 Channel Volume Front Right Up', ['Z2CVFR UP', 'Z2CVFR UP']),
                (SendCommand, 'fnZ2CVFR_DOWN', 'Zone 2 Channel Volume Front Right Down', 'Zone 2 Channel Volume Front Right Down', ['Z2CVFR DOWN', 'Z2CVFR DOWN']),
                (SendCommand, 'fnZ2CVFR_INPUT', 'Zone 2 Channel Volume Front Right Input', 'Zone 2 Channel Volume Front Right Input', ['Z2CVFR **', 'Z2CVFR 50']),
            )),
            (SendCommand, 'fnZ2CVSTATUS', 'Zone 2 Channel Volume Status', 'Zone 2 Channel Volume Status', ['Z2CV?', 'Z2CV?']),
        )),
        (eg.ActionGroup, 'gpHighPassFilter', 'High Pass Filter', 'High Pass Filter', (
            (SendCommand, 'fnZ2HPFON', 'Zone 2 High Pass Filter On', 'Zone 2 High Pass Filter On', ['Z2HPFON', 'Z2HPFON']),
            (SendCommand, 'fnZ2HPFOFF', 'Zone 2 High Pass Filter Off', 'Zone 2 High Pass Filter Off', ['Z2HPFOFF', 'Z2HPFOFF']),
            (SendCommand, 'fnZ2HPFSTATUS', 'Zone 2 High Pass Filter Status', 'Zone 2 High Pass Filter Status', ['Z2HPF?', 'Z2HPF?']),
        )),
        (eg.ActionGroup, 'gpTone', 'Tone', 'Tone', (
            (eg.ActionGroup, 'gpBass', 'Bass', 'Bass', (
                (SendCommand, 'fnZ2PSBAS_UP', 'Zone 2 Tone Bass Up', 'Zone 2 Tone Bass Up', ['Z2PSBAS UP', 'Z2PSBAS UP']),
                (SendCommand, 'fnZ2PSBAS_DOWN', 'Zone 2 Tone Bass Down', 'Zone 2 Tone Bass Down', ['Z2PSBAS DOWN', 'Z2PSBAS DOWN']),
                (SendCommand, 'fnZ2PSBAS_INPUT', 'Zone 2 Tone Bass Input', 'Zone 2 Tone Bass Input', ['Z2PSBAS **', 'Z2PSBAS 50']),
                (SendCommand, 'fnZ2PSBAS_STATUS', 'Zone 2 Tone Bass Status', 'Zone 2 Tone Bass Status', ['Z2PSBAS ?', 'Z2PSBAS ?']),
            )),
            (eg.ActionGroup, 'gpTreble', 'Treble', 'Treble', (
                (SendCommand, 'fnZ2PSTRE_UP', 'Zone 2 Tone Treble Up', 'Zone 2 Tone Treble Up', ['Z2PSTRE UP', 'Z2PSTRE UP']),
                (SendCommand, 'fnZ2PSTRE_DOWN', 'Zone 2 Tone Treble Down', 'Zone 2 Tone Treble Down', ['Z2PSTRE DOWN', 'Z2PSTRE DOWN']),
                (SendCommand, 'fnZ2PSTRE_INPUT', 'Zone 2 Tone Treble Input', 'Zone 2 Tone Treble Input', ['Z2PSTRE **', 'Z2PSTRE 50']),
                (SendCommand, 'fnZ2PSTRE_STATUS', 'Zone 2 Tone Treble Status', 'Zone 2 Tone Treble Status', ['Z2PSTRE ?', 'Z2PSTRE ?']),
            )),
        )),
        (eg.ActionGroup, 'gpHDMIAudioMode', 'HDMI Audio Mode', 'HDMI Audio Mode', (
            (SendCommand, 'fnZ2HADTHR', 'Zone 2 HDMI Audio Mode Pass Thru', 'Zone 2 HDMI Audio Mode Pass Thru', ['Z2HADTHR', 'Z2HDA THR']),
            (SendCommand, 'fnZ2HADPCM', 'Zone 2 HDMI Audio Mode PCM', 'Zone 2 HDMI Audio Mode PCM', ['Z2HADPCM', 'Z2HDA PCM']),
            (SendCommand, 'fnZ2HADSTATUS', 'Zone 2 HDMI Audio Mode Status', 'Zone 2 HDMI Audio Mode Status', ['Z2HAD?', 'Z2HDA?']),
        )),
        (eg.ActionGroup, 'gpSleepTimer', 'Sleep Timer', 'Sleep Timer', (
            (SendCommand, 'fnZ2SLPOFF', 'Zone 2 Sleep Timer Off', 'Zone 2 Sleep Timer Off', ['Z2SLPOFF', 'Z2SLPOFF']),
            (SendCommand, 'fnZ2SLPINPUT', 'Zone 2 Sleep Timer Input', 'Zone 2 Sleep Timer Input', ['Z2SLP***', 'Z2SLP120']),
            (SendCommand, 'fnZ2SLPSTATUS', 'Zone 2 Sleep Timer Status', 'Zone 2 Sleep Timer Status', ['Z2SLP?', 'Z2SLP?']),
        )),
        (eg.ActionGroup, 'gpAutoStandby', 'Auto Standby', 'Auto Standby', (
            (SendCommand, 'fnZ2STBY2H', 'Zone 2 Auto Standby 2 Hours', 'Zone 2 Auto Standby 2 Hours', ['Z2STBY2H', 'Z2STBY2H']),
            (SendCommand, 'fnZ2STBY4H', 'Zone 2 Auto Standby 4 Hours', 'Zone 2 Auto Standby 4 Hours', ['Z2STBY4H', 'Z2STBY4H']),
            (SendCommand, 'fnZ2STBY8H', 'Zone 2 Auto Standby 8 Hours', 'Zone 2 Auto Standby 8 Hours', ['Z2STBY8H', 'Z2STBY8H']),
            (SendCommand, 'fnZ2STBYOFF', 'Zone 2 Auto Standby Off', 'Zone 2 Auto Standby Off', ['Z2STBYOFF', 'Z2STBYOFF']),
            (SendCommand, 'fnZ2STBYSTATUS', 'Zone 2 Auto Standby Status', 'Zone 2 Auto Standby Status', ['Z2STBY?', 'Z2STBY?']),
        )),
    )),
    (eg.ActionGroup, 'gpZone3', 'Zone 3', 'Zone 3', (
        (eg.ActionGroup, 'gpInput', 'Input', 'Input', (
            (SendCommand, 'fnZ3SOURCE', 'Zone 3 Input Main Zone', 'Zone 3 Input Main Zone', ['Z3SOURCE', 'Z3SOURCE']),
            (SendCommand, 'fnZ3PHONO', 'Zone 3 Input Phono', 'Zone 3 Input Phono', ['Z3PHONO', 'Z3PHONO']),
            (SendCommand, 'fnZ3CD', 'Zone 3 Input CD', 'Zone 3 Input CD', ['Z3CD', 'Z3CD']),
            (SendCommand, 'fnZ3TUNER', 'Zone 3 Input Tuner', 'Zone 3 Input Tuner', ['Z3TUNER', 'Z3TUNER']),
            (SendCommand, 'fnZ3DVD', 'Zone 3 Input DVD', 'Zone 3 Input DVD', ['Z3DVD', 'Z3DVD']),
            (SendCommand, 'fnZ3BD', 'Zone 3 Input BluRay', 'Zone 3 Input BluRay', ['Z3BD', 'Z3BD']),
            (SendCommand, 'fnZ3TV', 'Zone 3 Input TV', 'Zone 3 Input TV', ['Z3TV', 'Z3TV']),
            (SendCommand, 'fnZ3SAT/CBL', 'Zone 3 Input Sat/Cable', 'Zone 3 Input Sat/Cable', ['Z3SAT/CBL', 'Z3SAT/CBL']),
            (SendCommand, 'fnZ3MPLAY', 'Zone 3 Input Media Player', 'Zone 3 Input Media Player', ['Z3MPLAY', 'Z3MPLAY']),
            (SendCommand, 'fnZ3GAME', 'Zone 3 Input Game', 'Zone 3 Input Game', ['Z3GAME', 'Z3GAME']),
            (SendCommand, 'fnZ3HDRADIO', 'Zone 3 Input HD Radio', 'Zone 3 Input HD Radio', ['Z3HDRADIO', 'Z3HDRADIO']),
            (SendCommand, 'fnZ3NET', 'Zone 3 Input Net', 'Zone 3 Input Net', ['Z3NET', 'Z3NET']),
            (SendCommand, 'fnZ3PANDORA', 'Zone 3 Input Pandora', 'Zone 3 Input Pandora', ['Z3PANDORA', 'Z3PANDORA']),
            (SendCommand, 'fnZ3SIRIUSXM', 'Zone 3 Input Sirius/XM', 'Zone 3 Input Sirius/XM', ['Z3SIRIUSXM', 'Z3SIRIUSXM']),
            (SendCommand, 'fnZ3IRADIO', 'Zone 3 Input Internet Radio', 'Zone 3 Input Internet Radio', ['Z3IRADIO', 'Z3IRADIO']),
            (SendCommand, 'fnZ3SERVER', 'Zone 3 Input Server', 'Zone 3 Input Server', ['Z3SERVER', 'Z3SERVER']),
            (SendCommand, 'fnZ3FAVORITES', 'Zone 3 Input Favorites', 'Zone 3 Input Favorites', ['Z3FAVORITES', 'Z3FAVORITES']),
            (SendCommand, 'fnZ3AUX1', 'Zone 3 Input Aux 1', 'Zone 3 Input Aux 1', ['Z3AUX1', 'Z3AUX1']),
            (SendCommand, 'fnZ3AUX2', 'Zone 3 Input Aux 2', 'Zone 3 Input Aux 2', ['Z3AUX2', 'Z3AUX2']),
            (SendCommand, 'fnZ3AUX3', 'Zone 3 Input Aux 3', 'Zone 3 Input Aux 3', ['Z3AUX3', 'Z3AUX3']),
            (SendCommand, 'fnZ3AUX4', 'Zone 3 Input Aux 4', 'Zone 3 Input Aux 4', ['Z3AUX4', 'Z3AUX4']),
            (SendCommand, 'fnZ3AUX5', 'Zone 3 Input Aux 5', 'Zone 3 Input Aux 5', ['Z3AUX5', 'Z3AUX5']),
            (SendCommand, 'fnZ3AUX6', 'Zone 3 Input Aux 6', 'Zone 3 Input Aux 6', ['Z3AUX6', 'Z3AUX6']),
            (SendCommand, 'fnZ3AUX7', 'Zone 3 Input Aux 7', 'Zone 3 Input Aux 7', ['Z3AUX7', 'Z3AUX7']),
            (SendCommand, 'fnZ3BT', 'Zone 3 Input Blue Teeth', 'Zone 3 Input Blue Teeth', ['Z3BT', 'Z3BT']),
            (SendCommand, 'fnZ3USB/IPOD', 'Zone 3 Input USB/IPOD', 'Zone 3 Input USB/IPOD', ['Z3USB/IPOD', 'Z3USB/IPOD']),
            (SendCommand, 'fnZ3USB', 'Zone 3 Input USB + Playback', 'Zone 3 Input USB + Playback', ['Z3USB', 'Z3USB']),
            (SendCommand, 'fnZ3IPD', 'Zone 3 Input IPOD + Playback', 'Zone 3 Input IPOD + Playback', ['Z3IPD', 'Z3IPD']),
            (SendCommand, 'fnZ3IRP', 'Zone 3 Input Internet Radio + Recent Playback', 'Zone 3 Input Internet Radio + Recent Playback', ['Z3IRP', 'Z3IRP']),
            (SendCommand, 'fnZ3FVP', 'Zone 3 Input Internet Radio + Favorites Playback', 'Zone 3 Input Internet Radio + Favorites Playback', ['Z3FVP', 'Z3FVP']),
            (eg.ActionGroup, 'gpQuickSelect', 'Quick Select', 'Quick Select', (
                (SendCommand, 'fnZ3QUICK1', 'Zone 3 Input Quick Select 1', 'Zone 3 Input Quick Select 1', ['Z3QUICK1', 'Z3QUICK1']),
                (SendCommand, 'fnZ3QUICK2', 'Zone 3 Input Quick Select 2', 'Zone 3 Input Quick Select 2', ['Z3QUICK2', 'Z3QUICK2']),
                (SendCommand, 'fnZ3QUICK3', 'Zone 3 Input Quick Select 3', 'Zone 3 Input Quick Select 3', ['Z3QUICK3', 'Z3QUICK3']),
                (SendCommand, 'fnZ3QUICK4', 'Zone 3 Input Quick Select 4', 'Zone 3 Input Quick Select 4', ['Z3QUICK4', 'Z3QUICK4']),
                (SendCommand, 'fnZ3QUICK5', 'Zone 3 Input Quick Select 5', 'Zone 3 Input Quick Select 5', ['Z3QUICK5', 'Z3QUICK5']),
                (SendCommand, 'fnZ3QUICK_STATUS', 'Zone 3 Input Quick Select Status', 'Zone 3 Input Quick Select Status', ['Z3QUICK ?', 'Z3QUICK ?']),
            )),
            (eg.ActionGroup, 'gpQuickMemorySelect', 'Quick Memory Select', 'Quick Memory Select', (
                (SendCommand, 'fnZ3QUICK1_MEMORYSTATUS', 'Zone 3 Input Quick Memory Select 1', 'Zone 3 Input Quick Memory Select 1', ['Z3QUICK1 MEMORY?', 'Z3QUICK1 MEMORY']),
                (SendCommand, 'fnZ3QUICK2_MEMORY', 'Zone 3 Input Quick Memory Select 2', 'Zone 3 Input Quick Memory Select 2', ['Z3QUICK2 MEMORY', 'Z3QUICK2 MEMORY']),
                (SendCommand, 'fnZ3QUICK3_MEMORY', 'Zone 3 Input Quick Memory Select 3', 'Zone 3 Input Quick Memory Select 3', ['Z3QUICK3 MEMORY', 'Z3QUICK3 MEMORY']),
                (SendCommand, 'fnZ3QUCIK4_MEMORY', 'Zone 3 Input Quick Memory Select 4', 'Zone 3 Input Quick Memory Select 4', ['Z3QUCIK4 MEMORY', 'Z3QUICK4 MEMORY']),
                (SendCommand, 'fnZ3QUICK5_MEMORY', 'Zone 3 Input Quick Memory Select 5', 'Zone 3 Input Quick Memory Select 5', ['Z3QUICK5 MEMORY', 'Z3QUICK5 MEMORY']),
                (SendCommand, 'fnZ3QUICK_STATUS', 'Zone 3 Input Quick Memory Select Status', 'Zone 3 Input Quick Memory Select Status', ['Z3QUICK ?', 'Z3QUICK ?']),
            )),
        )),
        (eg.ActionGroup, 'gpVolume', 'Volume', 'Volume', (
            (SendCommand, 'fnZ3UP', 'Zone 3 Volume Up', 'Zone 3 Volume Up', ['Z3UP', 'Z3UP']),
            (SendCommand, 'fnZ3DOWN', 'Zone 3 Volume Down', 'Zone 3 Volume Down', ['Z3DOWN', 'Z3DOWN']),
            (SendCommand, 'fnZ3INPUT', 'Zone 3 Volume Input', 'Zone 3 Volume Input', ['Z3**', 'Z380']),
        )),
        (eg.ActionGroup, 'gpPower', 'Power', 'Power', (
            (SendCommand, 'fnZ3ON', 'Zone 3 Power On', 'Zone 3 Power On', ['Z3ON', 'Z3ON']),
            (SendCommand, 'fnZ3OFF', 'Zone 3 Power Off', 'Zone 3 Power Off', ['Z3OFF', 'Z3OFF']),
            (SendCommand, 'fnZ3STATUS', 'Zone 3 Power Status', 'Zone 3 Power Status', ['Z3?', 'Z3?']),
        )),
        (eg.ActionGroup, 'gpMute', 'Mute', 'Mute', (
            (SendCommand, 'fnZ3MUON', 'Zone 3 Mute On', 'Zone 3 Mute On', ['Z3MUON', 'Z3MUON']),
            (SendCommand, 'fnZ3MUOFF', 'Zone 3 Mute Off', 'Zone 3 Mute Off', ['Z3MUOFF', 'Z3MUOFF']),
            (SendCommand, 'fnZ3MUSTATUS', 'Zone 3 Mute Status', 'Zone 3 Mute Status', ['Z3MU?', 'Z3MU?']),
        )),
        (eg.ActionGroup, 'gpSoundMode', 'Sound Mode', 'Sound Mode', (
            (SendCommand, 'fnZ3CSST', 'Zone 3 Sound Mode Stereo', 'Zone 3 Sound Mode Stereo', ['Z3CSST', 'Z3CSST']),
            (SendCommand, 'fnZ3CSMONO', 'Zone 3 Sound Mode Mono', 'Zone 3 Sound Mode Mono', ['Z3CSMONO', 'Z3CSMONO']),
            (SendCommand, 'fnZ3CSSTATUS', 'Zone 3 Sound Mode Status', 'Zone 3 Sound Mode Status', ['Z3CS?', 'Z3CS?']),
        )),
        (eg.ActionGroup, 'gpChannelVolume', 'Channel Volume', 'Channel Volume', (
            (eg.ActionGroup, 'gpFrontLeft', 'Front Left', 'Front Left', (
                (SendCommand, 'fnZ3CVFL_UP', 'Zone 3 Channel Volume Front Left Up', 'Zone 3 Channel Volume Front Left Up', ['Z3CVFL UP', 'Z3CVFL UP']),
                (SendCommand, 'fnZ3CVFL_DOWN', 'Zone 3 Channel Volume Front Left Down', 'Zone 3 Channel Volume Front Left Down', ['Z3CVFL DOWN', 'Z3CVFL DOWN']),
                (SendCommand, 'fnZ3CVFL_INPUT', 'Zone 3 Channel Volume Front Left Input', 'Zone 3 Channel Volume Front Left Input', ['Z3CVFL **', 'Z3CVFL 50']),
            )),
            (eg.ActionGroup, 'gpFrontRight', 'Front Right', 'Front Right', (
                (SendCommand, 'fnZ3CVFR_UP', 'Zone 3 Channel Volume Front Right Up', 'Zone 3 Channel Volume Front Right Up', ['Z3CVFR UP', 'Z3CVFR UP']),
                (SendCommand, 'fnZ3CVFR_DOWN', 'Zone 3 Channel Volume Front Right Down', 'Zone 3 Channel Volume Front Right Down', ['Z3CVFR DOWN', 'Z3CVFR DOWN']),
                (SendCommand, 'fnZ3CVFR_INPUT', 'Zone 3 Channel Volume Front Right Input', 'Zone 3 Channel Volume Front Right Input', ['Z3CVFR **', 'Z3CVFR 50']),
            )),
            (SendCommand, 'fnZ3CVSTATUS', 'Zone 3 Channel Volume Status', 'Zone 3 Channel Volume Status', ['Z3CV?', 'Z3CV?']),
        )),
        (eg.ActionGroup, 'gpHighPassFilter', 'High Pass Filter', 'High Pass Filter', (
            (SendCommand, 'fnZ3HPFON', 'Zone 3 High Pass Filter On', 'Zone 3 High Pass Filter On', ['Z3HPFON', 'Z3HPFON']),
            (SendCommand, 'fnZ3HPFOFF', 'Zone 3 High Pass Filter Off', 'Zone 3 High Pass Filter Off', ['Z3HPFOFF', 'Z3HPFOFF']),
            (SendCommand, 'fnZ3HPFSTATUS', 'Zone 3 High Pass Filter Status', 'Zone 3 High Pass Filter Status', ['Z3HPF?', 'Z3HPF?']),
        )),
        (eg.ActionGroup, 'gpTone', 'Tone', 'Tone', (
            (eg.ActionGroup, 'gpBass', 'Bass', 'Bass', (
                (SendCommand, 'fnZ3PSBAS_UP', 'Zone 3 Tone Bass Up', 'Zone 3 Tone Bass Up', ['Z3PSBAS UP', 'Z3PSBAS UP']),
                (SendCommand, 'fnZ3PSBAS_DOWN', 'Zone 3 Tone Bass Down', 'Zone 3 Tone Bass Down', ['Z3PSBAS DOWN', 'Z3PSBAS DOWN']),
                (SendCommand, 'fnZ3PSBAS_INPUT', 'Zone 3 Tone Bass Input', 'Zone 3 Tone Bass Input', ['Z3PSBAS **', 'Z3PSBAS 50']),
                (SendCommand, 'fnZ3PSBAS_STATUS', 'Zone 3 Tone Bass Status', 'Zone 3 Tone Bass Status', ['Z3PSBAS ?', 'Z3PSBAS ?']),
            )),
            (eg.ActionGroup, 'gpTreble', 'Treble', 'Treble', (
                (SendCommand, 'fnZ3PSTRE_UP', 'Zone 3 Tone Treble Up', 'Zone 3 Tone Treble Up', ['Z3PSTRE UP', 'Z3PSTRE UP']),
                (SendCommand, 'fnZ3PSTRE_DOWN', 'Zone 3 Tone Treble Down', 'Zone 3 Tone Treble Down', ['Z3PSTRE DOWN', 'Z3PSTRE DOWN']),
                (SendCommand, 'fnZ3PSTRE_INPUT', 'Zone 3 Tone Treble Input', 'Zone 3 Tone Treble Input', ['Z3PSTRE **', 'Z3PSTRE 50']),
                (SendCommand, 'fnZ3PSTRE_STATUS', 'Zone 3 Tone Treble Status', 'Zone 3 Tone Treble Status', ['Z3PSTRE ?', 'Z3PSTRE ?']),
            )),
        )),
        (eg.ActionGroup, 'gpSleepTimer', 'Sleep Timer', 'Sleep Timer', (
            (SendCommand, 'fnZ3SLPOFF', 'Zone 3 Sleep Timer Off', 'Zone 3 Sleep Timer Off', ['Z3SLPOFF', 'Z3SLPOFF']),
            (SendCommand, 'fnZ3SLPINPUT', 'Zone 3 Sleep Timer Input', 'Zone 3 Sleep Timer Input', ['Z3SLP***', 'Z3SLP120']),
            (SendCommand, 'fnZ3SLPSTATUS', 'Zone 3 Sleep Timer Status', 'Zone 3 Sleep Timer Status', ['Z3SLP?', 'Z3SLP?']),
        )),
        (eg.ActionGroup, 'gpAutoStandby', 'Auto Standby', 'Auto Standby', (
            (SendCommand, 'fnZ3STBY2H', 'Zone 3 Auto Standby 2 Hours', 'Zone 3 Auto Standby 2 Hours', ['Z3STBY2H', 'Z3STBY2H']),
            (SendCommand, 'fnZ3STBY4H', 'Zone 3 Auto Standby 4 Hours', 'Zone 3 Auto Standby 4 Hours', ['Z3STBY4H', 'Z3STBY4H']),
            (SendCommand, 'fnZ3STBY8H', 'Zone 3 Auto Standby 8 Hours', 'Zone 3 Auto Standby 8 Hours', ['Z3STBY8H', 'Z3STBY8H']),
            (SendCommand, 'fnZ3STBYOFF', 'Zone 3 Auto Standby Off', 'Zone 3 Auto Standby Off', ['Z3STBYOFF', 'Z3STBYOFF']),
            (SendCommand, 'fnZ3STBYSTATUS', 'Zone 3 Auto Standby Status', 'Zone 3 Auto Standby Status', ['Z3STBY?', 'Z3STBY?']),
        )),
    )),
    (eg.ActionGroup, 'gpTuner', 'Tuner', 'Tuner', (
        (eg.ActionGroup, 'gpFrequancy', 'Frequancy', 'Frequancy', (
            (SendCommand, 'fnTFANUP', 'Tuner Frequancy Up', 'Tuner Frequancy Up', ['TFANUP', 'TFANUP']),
            (SendCommand, 'fnTFANDOWN', 'Tuner Frequancy Down', 'Tuner Frequancy Down', ['TFANDOWN', 'TFANDOWN']),
            (SendCommand, 'fnTFANINPUT', 'Tuner Frequancy Input', 'Tuner Frequancy Input', ['TFAN******', 'TFAN105000']),
            (SendCommand, 'fnTFANSTATUS', 'Tuner Frequancy Status', 'Tuner Frequancy Status', ['TFAN?', 'TFAN?']),
            (SendCommand, 'fnTFANNAMESTATUS', 'Tuner Frequancy RDS Info', 'Tuner Frequancy RDS Info', ['TFANNAME?', 'TFANNAME?']),
        )),
        (eg.ActionGroup, 'gpPreset', 'Preset', 'Preset', (
            (SendCommand, 'fnTPANUP', 'Tuner Preset Up', 'Tuner Preset Up', ['TPANUP', 'TPANUP']),
            (SendCommand, 'fnTPANDOWN', 'Tuner Preset Down', 'Tuner Preset Down', ['TPANDOWN', 'TPANDOWN']),
            (SendCommand, 'fnTPANINPUT', 'Tuner Preset Input', 'Tuner Preset Input', ['TPAN**', 'TPAN01']),
            (SendCommand, 'fnTPANSTATUS', 'Tuner Preset Return TP Status', 'Tuner Preset Return TP Status', ['TPAN?', 'TPAN?']),
            (eg.ActionGroup, 'gpMemory', 'Memory', 'Memory', (
                (SendCommand, 'fnTPANMEM', 'Tuner Preset Memory Down', 'Tuner Preset Memory Down', ['TPANMEM', 'TPANMEM']),
                (SendCommand, 'fnTPANMEMINPUT', 'Tuner Preset Memory Input', 'Tuner Preset Memory Input', ['TPANMEM**', 'TPANMEM01']),
            )),
        )),
        (eg.ActionGroup, 'gpBand', 'Band', 'Band', (
            (SendCommand, 'fnTMANAM', 'Tuner Band AM', 'Tuner Band AM', ['TMANAM', 'TMANAM']),
            (SendCommand, 'fnTMANFM', 'Tuner Band FM', 'Tuner Band FM', ['TMANFM', 'TMANFM']),
            (SendCommand, 'fnTMANSTATUS', 'Tuner Band Status', 'Tuner Band Status', ['TMAN?', 'TMAN?']),
            (eg.ActionGroup, 'gpScanMode', 'Scan Mode', 'Scan Mode', (
                (SendCommand, 'fnTMANAUTO', 'Tuner Band Scan Mode Auto', 'Tuner Band Scan Mode Auto', ['TMANAUTO', 'TMANAUTO']),
                (SendCommand, 'fnTMANMANUAL', 'Tuner Band Scan Mode Manual', 'Tuner Band Scan Mode Manual', ['TMANMANUAL', 'TMANMANUAL']),
            )),
        )),
    )),
    (eg.ActionGroup, 'gpHDRadio', 'HD Radio', 'HD Radio', (
        (eg.ActionGroup, 'gpFrequancy', 'Frequancy', 'Frequancy', (
            (SendCommand, 'fnTFHDUP', 'HD Radio Frequancy Up', 'HD Radio Frequancy Up', ['TFHDUP', 'TFHDUP']),
            (SendCommand, 'fnTFHDDOWN', 'HD Radio Frequancy Down', 'HD Radio Frequancy Down', ['TFHDDOWN', 'TFHDDOWN']),
            (SendCommand, 'fnTFHDINPUT', 'HD Radio Frequancy Input', 'HD Radio Frequancy Input', ['TFHD******', 'TFHD105000']),
            (SendCommand, 'fnTFHDSTATUS', 'HD Radio Frequancy Return TFHD Status', 'HD Radio Frequancy Return TFHD Status', ['TFHD?', 'TFHD?']),
            (eg.ActionGroup, 'gpMultiCast', 'Multi Cast', 'Multi Cast', (
                (SendCommand, 'fnTFHDMCINPUT', 'HD Radio Frequancy Multi Cast Input', 'HD Radio Frequancy Multi Cast Input', ['TFHDMC*', 'TFHDMC2']),
                (SendCommand, 'fnTFHDMCINPUT', 'HD Radio Frequancy Multi Cast Frequancy Input', 'HD Radio Frequancy Multi Cast Frequancy Input', ['TFHD******MC*', 'TFHD008750MC5']),
            )),
        )),
        (eg.ActionGroup, 'gpPreset', 'Preset', 'Preset', (
            (SendCommand, 'fnTPHDUP', 'HD Radio Preset Up', 'HD Radio Preset Up', ['TPHDUP', 'TPHDUP']),
            (SendCommand, 'fnTPHDDOWN', 'HD Radio Preset Down', 'HD Radio Preset Down', ['TPHDDOWN', 'TPHDDOWN']),
            (SendCommand, 'fnTPHDINPUT', 'HD Radio Preset Input', 'HD Radio Preset Input', ['TPHD**', 'TPHD01']),
            (SendCommand, 'fnTPHDSTATUS', 'HD Radio Preset Status', 'HD Radio Preset Status', ['TPHD?', 'TPHD?']),
            (eg.ActionGroup, 'gpMemory', 'Memory', 'Memory', (
                (SendCommand, 'fnTPHDMEM', 'HD Radio Preset Memory Down', 'HD Radio Preset Memory Down', ['TPHDMEM', 'TPHDMEM']),
                (SendCommand, 'fnTPHDMEMINPUT', 'HD Radio Preset Memory Input', 'HD Radio Preset Memory Input', ['TPHDMEM**', 'TPHDMEM01']),
            )),
        )),
        (eg.ActionGroup, 'gpBand', 'Band', 'Band', (
            (SendCommand, 'fnTMHDAM', 'HD Radio Band AM', 'HD Radio Band AM', ['TMHDAM', 'TMHDAM']),
            (SendCommand, 'fnTMHDFM', 'HD Radio Band FM', 'HD Radio Band FM', ['TMHDFM', 'TMHDFM']),
            (SendCommand, 'fnTMHDSTATUS', 'HD Radio Band Status', 'HD Radio Band Status', ['TMHD?', 'TMHD?']),
            (eg.ActionGroup, 'gpScanMode', 'Scan Mode', 'Scan Mode', (
                (SendCommand, 'fnTMHDAUTOHD', 'HD Radio Band Scan Mode HD Auto', 'HD Radio Band Scan Mode HD Auto', ['TMHDAUTOHD', 'TMHDAUTOHD']),
                (SendCommand, 'fnTMHDAUTO', 'HD Radio Band Scan Mode Digital Auto', 'HD Radio Band Scan Mode Digital Auto', ['TMHDAUTO', 'TMHDAUTO']),
                (SendCommand, 'fnTMHDMANUAL', 'HD Radio Band Scan Mode Digital Manual', 'HD Radio Band Scan Mode Digital Manual', ['TMHDMANUAL', 'TMHDMANUAL']),
                (SendCommand, 'fnTMHDANAAUTO', 'HD Radio Band Scan Mode Analog Auto', 'HD Radio Band Scan Mode Analog Auto', ['TMHDANAAUTO', 'TMHDANAAUTO']),
                (SendCommand, 'fnTMHDANAMANU', 'HD Radio Band Scan Mode Analog Manual', 'HD Radio Band Scan Mode Analog Manual', ['TMHDANAMANU', 'TMHDANAMANU']),
            )),
        )),
        (SendCommand, 'fnTHDSTATUS', 'HD Radio Status', 'HD Radio Status', ['THD?', 'HD?']),
    )),
    (eg.ActionGroup, 'gpNetAudio', 'Net Audio', 'Net Audio', (
        (SendCommand, 'fnNS90', 'Net Audio Cursor Up', 'Net Audio Cursor Up', ['NS90', 'NS90']),
        (SendCommand, 'fnNS91', 'Net Audio Cursor Down', 'Net Audio Cursor Down', ['NS91', 'NS91']),
        (SendCommand, 'fnNS92', 'Net Audio Cursor Left', 'Net Audio Cursor Left', ['NS92', 'NS92']),
        (SendCommand, 'fnNS93', 'Net Audio Cursor Right', 'Net Audio Cursor Right', ['NS93', 'NS93']),
        (SendCommand, 'fnNS94', 'Net Audio Enter', 'Net Audio Enter', ['NS94', 'NS94']),
        (SendCommand, 'fnNS9A', 'Net Audio Play', 'Net Audio Play', ['NS9A', 'NS9A']),
        (SendCommand, 'fnNS9B', 'Net Audio Pause', 'Net Audio Pause', ['NS9B', 'NS9B']),
        (SendCommand, 'fnNS9C', 'Net Audio Stop', 'Net Audio Stop', ['NS9C', 'NS9C']),
        (SendCommand, 'fnNS9D', 'Net Audio Skip Forward', 'Net Audio Skip Forward', ['NS9D', 'NS9D']),
        (SendCommand, 'fnNS9E', 'Net Audio Skip Back', 'Net Audio Skip Back', ['NS9E', 'NS9E']),
        (SendCommand, 'fnNS9F', 'Net Audio Fast Forward', 'Net Audio Fast Forward', ['NS9F', 'NS9F']),
        (SendCommand, 'fnNS9G', 'Net Audio Rewind', 'Net Audio Rewind', ['NS9G', 'NS9G']),
        (SendCommand, 'fnNS9H', 'Net Audio Repeat', 'Net Audio Repeat', ['NS9H', 'NS9H']),
        (SendCommand, 'fnNS9I', 'Net Audio Repeat All', 'Net Audio Repeat All', ['NS9I', 'NS9I']),
        (SendCommand, 'fnNS9J', 'Net Audio Repeat Off', 'Net Audio Repeat Off', ['NS9J', 'NS9J']),
        (SendCommand, 'fnNS9K', 'Net Audio Random On', 'Net Audio Random On', ['NS9K', 'NS9K']),
        (SendCommand, 'fnNS9M', 'Net Audio Random Off', 'Net Audio Random Off', ['NS9M', 'NS9M']),
        (SendCommand, 'fnNS9W', 'Net Audio iPod Mode/On Screen Mode', 'Net Audio iPod Mode/On Screen Mode', ['NS9W', 'NS9W']),
        (SendCommand, 'fnNS9X', 'Net Audio Next Page', 'Net Audio Next Page', ['NS9X', 'NS9X']),
        (SendCommand, 'fnNS9Y', 'Net Audio Previous Page', 'Net Audio Previous Page', ['NS9Y', 'NS9Y']),
        (SendCommand, 'fnNS9Z', 'Net Audio Stop FF/REW', 'Net Audio Stop FF/REW', ['NS9Z', 'NS9Z']),
        (SendCommand, 'fnNSRPT', 'Net Audio Repeat On/Off', 'Net Audio Repeat On/Off', ['NSRPT', 'NSRPT']),
        (SendCommand, 'fnNSRND', 'Net Audio Random On/Off', 'Net Audio Random On/Off', ['NSRND', 'NSRND']),
        (SendCommand, 'fnNSBINPUT', 'Net Audio Preset Input', 'Net Audio Preset Input', ['NSB**', 'NSB00']),
        (SendCommand, 'fnNSCINPUT', 'Net Audio Preset Memory Input', 'Net Audio Preset Memory Input', ['NSC**', 'NSC00']),
        (SendCommand, 'fnNSH', 'Net Audio Preset Name Status', 'Net Audio Preset Name Status', ['NSH', 'NSH']),
    )),
    (eg.ActionGroup, 'gpSystem', 'System', 'System', (
        (eg.ActionGroup, 'gpDirectionPad', 'Direction Pad', 'Direction Pad', (
            (SendCommand, 'fnMNCUP', 'System Direction Pad Cursor Up', 'System Direction Pad Cursor Up', ['MNCUP', 'MNCUP']),
            (SendCommand, 'fnMNCDN', 'System Direction Pad Cursor Down', 'System Direction Pad Cursor Down', ['MNCDN', 'MNCDN']),
            (SendCommand, 'fnMNCLT', 'System Direction Pad Cursor Left', 'System Direction Pad Cursor Left', ['MNCLT', 'MNCLT']),
            (SendCommand, 'fnMNCRT', 'System Direction Pad Cursor Right', 'System Direction Pad Cursor Right', ['MNCRT', 'MNCRT']),
            (SendCommand, 'fnMNENT', 'System Direction Pad Enter', 'System Direction Pad Enter', ['MNENT', 'MNENT']),
            (SendCommand, 'fnMNRTN', 'System Direction Pad Return', 'System Direction Pad Return', ['MNRTN', 'MNRTN']),
            (SendCommand, 'fnMNOPT', 'System Direction Pad Option', 'System Direction Pad Option', ['MNOPT', 'MNOPT']),
            (SendCommand, 'fnMNINF', 'System Direction Pad Info', 'System Direction Pad Info', ['MNINF', 'MNINF']),
            (SendCommand, 'fnMNCHL', 'System Direction Pad Channel Adjust Menu', 'System Direction Pad Channel Adjust Menu', ['MNCHL', 'MNCHL']),
            (SendCommand, 'fnMNMEN_ON', 'System Direction Pad Setup Menu On', 'System Direction Pad Setup Menu On', ['MNMEN ON', 'MNMEN ON']),
            (SendCommand, 'fnMNMEN_OFF', 'System Direction Pad Setup Menu Off', 'System Direction Pad Setup Menu Off', ['MNMEN OFF', 'MNMEN OFF']),
            (SendCommand, 'fnMNMENSTATUS', 'System Direction Pad Setup Menu Status', 'System Direction Pad Setup Menu Status', ['MNMEN?', 'MNMEN?']),
        )),
        (eg.ActionGroup, 'gpAllZoneStereo', 'All Zone Stereo', 'All Zone Stereo', (
            (SendCommand, 'fnMNZST_ON', 'System All Zone Stereo On', 'System All Zone Stereo On', ['MNZST ON', 'MNZST ON']),
            (SendCommand, 'fnMNZST_OFF', 'System All Zone Stereo Off', 'System All Zone Stereo Off', ['MNZST OFF', 'MNZST OFF']),
            (SendCommand, 'fnMNZSTSTATUS<CR>', 'System All Zone Stereo Status', 'System All Zone Stereo Status', ['MNZST?<CR>', 'MNZST?']),
        )),
        (eg.ActionGroup, 'gpLocks', 'Locks', 'Locks', (
            (eg.ActionGroup, 'gpRemote', 'Remote', 'Remote', (
                (SendCommand, 'fnSYREMOTE_LOCK_ON', 'System Locks Remote On', 'System Locks Remote On', ['SYREMOTE LOCK ON', 'SYREMOTE LOCK ON']),
                (SendCommand, 'fnSYREMOTE_LOCK_OFF', 'System Locks Remote Off', 'System Locks Remote Off', ['SYREMOTE LOCK OFF', 'SYREMOTE LOCK OFF']),
            )),
            (eg.ActionGroup, 'gpPanelButtons', 'Panel Buttons', 'Panel Buttons', (
                (SendCommand, 'fnSYPANEL_LOCK_ON', 'System Locks Panel Buttons Everything But Master Volume', 'System Locks Panel Buttons Everything But Master Volume', ['SYPANEL LOCK ON', 'SYPANEL LOCK ON']),
                (SendCommand, 'fnSYPANELV_LOCK_ON', 'System Locks Panel Buttons On', 'System Locks Panel Buttons On', ['SYPANEL+V LOCK ON', 'SYPANEL+V LOCK ON']),
                (SendCommand, 'fnSYPANEL_LOCK_OFF', 'System Locks Panel Buttons Off', 'System Locks Panel Buttons Off', ['SYPANEL LOCK OFF', 'SYPANEL LOCK OFF']),
            )),
        )),
        (eg.ActionGroup, 'gpTrigger', 'Trigger', 'Trigger', (
            (eg.ActionGroup, 'gp1', '1', '1', (
                (SendCommand, 'fnTR1_ON', 'System Trigger 1 On', 'System Trigger 1 On', ['TR1 ON', 'TR1 ON']),
                (SendCommand, 'fnTR1_OFF', 'System Trigger 1 Off', 'System Trigger 1 Off', ['TR1 OFF', 'TR1 OFF']),
            )),
            (eg.ActionGroup, 'gp2', '2', '2', (
                (SendCommand, 'fnTR2_ON', 'System Trigger 2 On', 'System Trigger 2 On', ['TR2 ON', 'TR2 ON']),
                (SendCommand, 'fnTR2_OFF', 'System Trigger 2 Off', 'System Trigger 2 Off', ['TR2 OFF', 'TR2 OFF']),
            )),
            (SendCommand, 'fnTRSTATUS', 'System Trigger Status', 'System Trigger Status', ['TR?', 'TR?']),
        )),
        (eg.ActionGroup, 'gpUpgradeId', 'Upgrade Id', 'Upgrade Id', (
            (SendCommand, 'fnUGIDN', 'System Upgrade Id Display Number', 'System Upgrade Id Display Number', ['UGIDN', 'UGIDN']),
        )),
        (eg.ActionGroup, 'gpRemoteMaintance', 'Remote Maintance', 'Remote Maintance', (
            (SendCommand, 'fnRNSTA', 'System Remote Maintance Start', 'System Remote Maintance Start', ['RNSTA', 'RM STA']),
            (SendCommand, 'fnRNEND', 'System Remote Maintance End', 'System Remote Maintance End', ['RNEND', 'RM END']),
            (SendCommand, 'fnRNSTATUS', 'System Remote Maintance Status', 'System Remote Maintance Status', ['RN?', 'RM ?']),
        )),
        (eg.ActionGroup, 'gpFrontPanelLightLevel', 'Front Panel Light Level', 'Front Panel Light Level', (
            (SendCommand, 'fnDIM_BRI', 'System Front Panel Light Level Bright', 'System Front Panel Light Level Bright', ['DIM BRI', 'DIM BRI']),
            (SendCommand, 'fnDIM_DIM', 'System Front Panel Light Level Dim', 'System Front Panel Light Level Dim', ['DIM DIM', 'DIM DIM']),
            (SendCommand, 'fnDIM_DAR', 'System Front Panel Light Level Dark', 'System Front Panel Light Level Dark', ['DIM DAR', 'DIM DAR']),
            (SendCommand, 'fnDIM_OFF', 'System Front Panel Light Level Off', 'System Front Panel Light Level Off', ['DIM OFF', 'DIM OFF']),
            (SendCommand, 'fnDIM_SEL', 'System Front Panel Light Level Toggle', 'System Front Panel Light Level Toggle', ['DIM SEL', 'DIM SEL']),
            (SendCommand, 'fnDIM_STATUS', 'System Front Panel Light Level Status', 'System Front Panel Light Level Status', ['DIM ?', 'DIM ?']),
        )),
    )),
    (eg.ActionGroup, 'gpRemoteUserInput', 'Remote Control User Input', 'Remote Control User Input', (
        (RemoteUserInput, 'fnUSER_INPUT_1', 'User Input 1', 'User Input 1', '1'),
        (RemoteUserInput, 'fnUSER_INPUT_2', 'User Input 2', 'User Input 2', '2'),
        (RemoteUserInput, 'fnUSER_INPUT_3', 'User Input 3', 'User Input 3', '3'),
        (RemoteUserInput, 'fnUSER_INPUT_4', 'User Input 4', 'User Input 4', '4'),
        (RemoteUserInput, 'fnUSER_INPUT_5', 'User Input 5', 'User Input 5', '5'),
        (RemoteUserInput, 'fnUSER_INPUT_6', 'User Input 6', 'User Input 6', '6'),
        (RemoteUserInput, 'fnUSER_INPUT_7', 'User Input 7', 'User Input 7', '7'),
        (RemoteUserInput, 'fnUSER_INPUT_8', 'User Input 8', 'User Input 8', '8'),
        (RemoteUserInput, 'fnUSER_INPUT_9', 'User Input 9', 'User Input 9', '9'),
        (RemoteUserInput, 'fnUSER_INPUT_0', 'User Input 0', 'User Input 0', '0'),
        (ToggleInput, 'fnUSER_INPUT_TOGGLE', 'User Input Toggle On/Off', 'User Input Toggle On/Off', None)
    ))
)


def CreateActions(plugin):
    plugin.AddActionsFromList(ACTIONS)

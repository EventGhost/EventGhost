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

import wx

# Local imports
import eg

class ControlProviderMixin:
    def BoxedGroup(self, *args, **kwargs):
        return eg.BoxedGroup(self, *args, **kwargs)

    def Button(self, label="", *args, **kwargs):
        return wx.Button(self, -1, label, *args, **kwargs)

    def CheckBox(self, value=0, label="", *args, **kwargs):
        checkBox = wx.CheckBox(self, -1, label, *args, **kwargs)
        checkBox.SetValue(bool(value))
        return checkBox

    def Choice(self, value, choices, *args, **kwargs):
        return eg.Choice(self, value, choices, *args, **kwargs)

    def ColourSelectButton(self, value=(255, 255, 255), *args, **kwargs):
        return eg.ColourSelectButton(self, value, *args, **kwargs)

    def ComboBox(
        self,
        value,
        choices,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        *args,
        **kwargs
    ):
        return wx.ComboBox(
            self, -1, value, pos, size, choices, *args, **kwargs
        )

    def DirBrowseButton(self, value, *args, **kwargs):
        dirpathCtrl = eg.DirBrowseButton(
            self,
            size=(320, -1),
            startDirectory=value,
            labelText="",
            buttonText=eg.text.General.browse
        )
        dirpathCtrl.SetValue(value)
        return dirpathCtrl

    def DisplayChoice(self, value=0, *args, **kwargs):
        return eg.DisplayChoice(self, value, *args, **kwargs)

    def FileBrowseButton(self, value, **kwargs):
        filepathCtrl = eg.FileBrowseButton(
            self,
            size=(320, -1),
            initialValue=value,
            labelText="",
            buttonText=eg.text.General.browse,
            **kwargs
        )
        return filepathCtrl

    def FontSelectButton(self, value=None, *args, **kwargs):
        fontCtrl = eg.FontSelectButton(self)
        fontCtrl.SetValue(value)
        return fontCtrl

    def MacroSelectButton(self, *args, **kwargs):
        return eg.MacroSelectButton(self, *args, **kwargs)

    def MonitorsCtrl(self, *args, **kwargs):
        return eg.MonitorsCtrl(self, -1, *args, **kwargs)

    def PasswordCtrl(self, *args, **kwargs):
        return eg.PasswordCtrl(self, -1, *args, **kwargs)

    def RadioBox(self, value, choices, *args, **kwargs):
        kwargs["choices"] = choices
        radioBox = eg.RadioBox(self, *args, **kwargs)
        radioBox.SetValue(value)
        return radioBox

    def RadioButton(self, value, label="", *args, **kwargs):
        ctrl = wx.RadioButton(self, -1, label, *args, **kwargs)
        ctrl.SetValue(value)
        return ctrl

    def SerialPortChoice(self, value=0, *args, **kwargs):
        kwargs['value'] = value
        return eg.SerialPortChoice(self, *args, **kwargs)

    def SmartSpinIntCtrl(self, value=0, *args, **kwargs):
        return eg.SmartSpinIntCtrl(self, -1, value, *args, **kwargs)

    def SmartSpinNumCtrl(self, value=0, *args, **kwargs):
        return eg.SmartSpinNumCtrl(self, -1, value, *args, **kwargs)

    def SpinIntCtrl(self, value=0, *args, **kwargs):
        return eg.SpinIntCtrl(self, -1, value, *args, **kwargs)

    def SpinNumCtrl(self, value=0, *args, **kwargs):
        return eg.SpinNumCtrl(self, -1, value, *args, **kwargs)

    def StaticText(self, label, *args, **kwargs):
        """
        Returns a wx.StaticText control.
        """
        return wx.StaticText(self, -1, label, *args, **kwargs)

    def TextCtrl(
        self,
        value="",
        pos=wx.DefaultPosition,
        size=(150, -1),
        style=0,
        validator=wx.DefaultValidator,
        name=wx.TextCtrlNameStr
    ):
        """
        Returns a wx.TextCtrl control.
        """
        return wx.TextCtrl(self, -1, value, pos, size, style, validator, name)

    def VStaticBoxSizer(self, label, *items):
        staticBox = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer.AddMany(items)
        return sizer

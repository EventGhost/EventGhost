# This file is part of EventGhost.
# Copyright (C) 2007 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate: 2007-11-14 04:19:28 +0100 (Mi, 14 Nov 2007) $
# $LastChangedRevision: 263 $
# $LastChangedBy: bitmonster $


class ControlProviderMixin:
    
    def StaticText(self, label, *args, **kwargs):
        return wx.StaticText(self, -1, label, *args, **kwargs)
        
    
    def SpinIntCtrl(self, value=0, *args, **kwargs):
        return eg.SpinIntCtrl(self, -1, value, *args, **kwargs)
    
    
    def SpinNumCtrl(self, value=0, *args, **kwargs):
        return eg.SpinNumCtrl(self, -1, value, *args, **kwargs)
    
    
    def TextCtrl(self, value="", *args, **kwargs):
        return wx.TextCtrl(self, -1, value, *args, **kwargs)
    
    
    def Choice(self, value=0, *args, **kwargs):
        return eg.Choice(self, value, *args, **kwargs)
    
    
    def DisplayChoice(self, value=0, *args, **kwargs):
        return eg.DisplayChoice(self, value, *args, **kwargs)
    
    
    def ColourSelectButton(self, value=(255, 255, 255), *args, **kwargs):
        return eg.ColourSelectButton(self, value, *args, **kwargs)
    
    
    def FontSelectButton(self, value=None, *args, **kwargs):
        fontCtrl = eg.FontSelectButton(self)
        fontCtrl.SetValue(value)
        return fontCtrl
    
    
    def CheckBox(self, value=0, label="", *args, **kwargs):
        checkBox = wx.CheckBox(self, -1, label, *args, **kwargs)
        checkBox.SetValue(bool(value))
        return checkBox
    
    
    def RadioBox(self, value=0, label="", *args, **kwargs):
        radioBox = eg.RadioBox(self, -1, label, *args, **kwargs)
        radioBox.SetValue(value)
        return radioBox
    
    
    def Button(self, label="", *args, **kwargs):
        return wx.Button(self, -1, label, *args, **kwargs)
    
    
    def RadioButton(self, value, label="", *args, **kwargs):
        ctrl = wx.RadioButton(self, -1, label, *args, **kwargs)
        ctrl.SetValue(value)
        return ctrl
        
    
    def DirBrowseButton(self, value, *args, **kwargs):
        dirpathCtrl = eg.DirBrowseButton(
            self,
            size=(320,-1),
            startDirectory=value, 
            labelText="",
            buttonText=eg.text.General.browse
        )
        dirpathCtrl.SetValue(value)
        return dirpathCtrl
    
    
    def FileBrowseButton(self, value, *args, **kwargs):
        filepathCtrl = eg.FileBrowseButton(
            self,
            size=(320,-1),
            initialValue=value, 
            labelText="",
            buttonText=eg.text.General.browse,
            **kwargs
        )
        return filepathCtrl
    
    
    def SerialPortChoice(self, value=0, *args, **kwargs):
        kwargs['value'] = value
        return eg.SerialPortChoice(self, *args, **kwargs)
    
    
    def MacroSelectButton(self, *args, **kwargs):
        return eg.MacroSelectButton(self, *args, **kwargs)
    


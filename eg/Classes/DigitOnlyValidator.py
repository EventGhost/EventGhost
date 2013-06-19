# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import wx
import string


class DigitOnlyValidator(wx.PyValidator):
    
    def __init__(self, choices=None):
        wx.PyValidator.__init__(self)
        self.choices = choices
        self.Bind(wx.EVT_CHAR, self.OnChar)


    def Clone(self):
        return DigitOnlyValidator(self.choices)


    def TransferToWindow(self):
        return True


    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        
        if self.choices is not None:
            try:
                i = self.choices.index(val)
                return True
            except:
                pass
        
        for x in val:
            if x not in string.digits:
                return False

        return True


    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.digits:
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling event.Skip eats the event before it
        # gets to the text control
        return


        
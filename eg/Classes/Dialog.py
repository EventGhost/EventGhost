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


class Dialog(wx.Dialog, eg.ControlProviderMixin):
    __isModal = False
    __grparent = None
    __result = None
    
    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        if self.GetParent() == eg.document.frame:
            eg.document.frame.AddDialog(self)
        
#    @eg.LogIt
#    def Destroy(self):
#        if self.GetParent() == eg.document.frame:
#            eg.document.frame.RemoveDialog(self)
#        wx.Dialog.Destroy(self)

    
    @classmethod
    @eg.LogItWithReturn
    def GetModalResult(cls, *args, **kwargs):
        self = cls.__new__(cls)
        self.__nextResult = None
        self.__gr = eg.Greenlet(self.Process)
        self.__isModal = True
        self.Affirmed = self.AffirmedShowModal
        self.__gr.switch(*args, **kwargs)
        self.Bind(wx.EVT_CLOSE, self.OnCancel)
        eg.Utils.EnsureVisible(self)
        self.ShowModal()
        self.Destroy()
        return self.__result


    @classmethod
    def Create(cls, *args, **kwargs):
        self = cls.__new__(cls)
        self.__nextResult = None
        self.__gr = eg.Greenlet(self.Process)
        self.__gr.switch(*args, **kwargs)
        return self
    
    
    def FinishSetup(self):
        self.__grparent = self.__gr.parent
        if not self.__isModal:
            self.__grparent.switch(self)
    
    
    def Process(self, *args, **kwargs):
        raise NotImplemented
    
    
    def GetResult(self):
        if self.__gr.dead:
            raise Exception("called get result on dead dialog")
        result = self.__gr.switch()
        if self.__gr.dead:
            self.Destroy()
        return result
        
        
    @eg.LogIt
    def SetResult(self, *args, **kwargs):
        if self.__isModal:
            self.__result = (args, kwargs)
            self.EndModal(wx.ID_CANCEL)
            return
        self.__grparent.switch(args, kwargs)
    
    
    @eg.LogItWithReturn
    def AffirmedShowModal(self):
        if self.__result is not None:
            return False
        result = self.__gr.parent.switch()
        if result == wx.ID_CANCEL:
            return False
        return result

        
    @eg.LogItWithReturn
    def Affirmed(self):
        if self.__nextResult == wx.ID_CANCEL:
            return False
        self.Bind(wx.EVT_CLOSE, self.OnCancel)
        eg.Utils.EnsureVisible(self)
        self.Show(True)
        if self.__grparent is None:
            self.FinishSetup()
        result = eg.mainGreenlet.switch()
        if result == wx.ID_CANCEL:
            return False
        elif result == wx.ID_OK:
            self.__nextResult = wx.ID_CANCEL
            return wx.ID_OK
        return result
        
    
    @eg.LogItWithReturn
    def OnOK(self, event=None):
        self.__gr.switch(wx.ID_OK)
        
        
    @eg.LogItWithReturn
    def OnCancel(self, event=None):
        self.__gr.switch(wx.ID_CANCEL)
        if self.__isModal and self.__gr.dead:
            self.EndModal(wx.ID_CANCEL)
        
        
    @eg.LogItWithReturn
    def OnApply(self, event=None):
        self.__gr.switch(wx.ID_APPLY)
        
        
    

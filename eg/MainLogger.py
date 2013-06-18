import sys
from time import time, strftime, localtime
from types import UnicodeType

import wx
import wx.lib.mixins.listctrl as listmix

import eg

EVENT_ICON_INDEX = eg.EventItem.iconIndex



class Logger:
    
    def __init__(self, document):
        self.document = document
    
    
    def CreateCtrl(self, parent):
        self.ctrl = LoggerCtrl(parent)
        
    

import collections

class LoggerCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """Implemention of a ListCtrl with a circular buffer."""
    
    def __init__(
        self, 
        parent, 
        id=-1, 
        pos=wx.DefaultPosition, 
        size=wx.DefaultSize
    ):
        self.buffer = u""
        self.maxlength = 2000
        self.data = collections.deque()
        wx.ListCtrl.__init__(
            self, 
            parent, 
            id, 
            pos, 
            size,
            style=(
                wx.LC_REPORT
                |wx.LC_VIRTUAL
                |wx.NO_FULL_REPAINT_ON_RESIZE
                |wx.HSCROLL
                |wx.CLIP_CHILDREN
            )
        )
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.SetImageList(eg.imageList, wx.IMAGE_LIST_SMALL)

        sysColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        r = sysColour.Red()
        g = sysColour.Green()
        b = sysColour.Blue()
        sum = r + g + (b / 2)
        if sum > 382:
            r = max(r - 15, 0)
            g = max(g - 15, 0)
        else:
            r = min(r + 30, 255)
            g = min(g + 30, 255)
            b = min(b + 30, 255)
        sysTextColour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour((r, g, b))
        self.attr1.SetTextColour(sysTextColour)

        self.attr2 = wx.ListItemAttr()
        self.attr2.SetBackgroundColour(sysColour)
        self.attr2.SetTextColour(sysTextColour)
        
        text = self.text = eg.text.MainFrame.Logger
        #self.InsertColumn(0, "")
        self.InsertColumn(0, text.timeHeader)
        self.InsertColumn(1, text.descriptionHeader)
        self.SetItemCount(len(self.data))
        #self.SetColumnWidth(0, 20)
        self.ScrollList(0, len(self.data) * 20)
        self.oldWidth,_ = self.GetClientSizeTuple()
        
        # logger popup menu
        menu = eg.Menu(self, "EditMenu", eg.text.MainFrame.Menu)
        menu.AddItem("Copy")
        menu.AddSeparator()
        menu.AddItem("ClearAll")
        self.contextMenu = menu
        
        Bind = self.Bind
        Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightUp)
        Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnBeginColumnDrag)
        Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnStartDrag)
        Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelected)
        
        class print_class:
            def write(self2, data):
                wx.CallAfter(self.__OnWrite, data, 0)
        
        class print_err_class:
            def write(self2, data):
                wx.CallAfter(self.__OnWrite, data, 1)
        
        if not eg._debug:
            sys.stdout = print_class()
            sys.stderr = print_err_class()
        
        self.logTimes = True
        self.__inSelection = False
        self.__OnWrite(text.welcomeText + "\n", 0)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        
    def OnSelected(self, event):
        eg.whoami()
        #self.Unbind(wx.EVT_LIST_ITEM_SELECTED)
        #wx.CallAfter(self.OnSelected2,  event.GetIndex())
        event.Skip()
        
        
    def OnSelected2(self, index):
        eg.whoami()
        origIndex = index
        eg.notice(index)
        flags = wx.LIST_STATE_SELECTED | wx.LIST_STATE_FOCUSED
        if self.GetItemData(index)[0] == 1:
            while self.GetItemData(index-1)[0] == 1:
                index -= 1
            while self.GetItemData(index)[0] == 1:
                state = self.GetItemState(index, flags)
                if state != flags:
                    self.SetItemState(index, flags, flags)
                index += 1
        wx.CallAfter(self.Bind, wx.EVT_LIST_ITEM_SELECTED, self.OnSelected)
        
        
    def SetTimeLogging(self, flag):
        self.Freeze()
        self.logTimes = flag
        if flag:
            self.InsertColumn(0, self.text.timeHeader)
            self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        else:
            self.DeleteColumn(0)
        self.resizeLastColumn(0)
        self.Refresh()
        self.Thaw()
        
        
    def OnStartDrag(self, event):
        idx = event.GetIndex()
        itemData = self.GetItemData(idx)
        if itemData[0] != EVENT_ICON_INDEX:
            return
        text = str(itemData[2])
        # create our own data format and use it in a
        # custom data object
        customData = wx.CustomDataObject(wx.CustomDataFormat("DragItem"))
        customData.SetData(text)

        # And finally, create the drop source and begin the drag
        # and drop opperation
        dropSource = wx.DropSource(self)
        dropSource.SetData(customData)
        result = dropSource.DoDragDrop(wx.Drag_AllowMove)
        if result == wx.DragMove:
            self.Refresh()
            
            
    def CanCut(self):
        return False
    
    
    def CanCopy(self):
        return self.GetSelectedItemCount() > 0
    
    
    def CanPaste(self):
        return False
    
    
    def OnCmdCopy(self, event):
        self.Copy()
        
    
    def Copy(self, event=None):
        text = ""
        lines = 1
        firstItem = item = self.GetNextItem(
            -1, 
            wx.LIST_NEXT_ALL, 
            wx.LIST_STATE_SELECTED
        )
        if item != -1:
            text = self.GetItemLineText(item)
            item = self.GetNextItem(
                item, 
                wx.LIST_NEXT_ALL, 
                wx.LIST_STATE_SELECTED
            )
            while item != -1:
                lines += 1
                text += "\r\n" + self.GetItemLineText(item)
                item = self.GetNextItem(
                    item, 
                    wx.LIST_NEXT_ALL, 
                    wx.LIST_STATE_SELECTED
                )
        if text != "" and wx.TheClipboard.Open():
            textDataObject = wx.TextDataObject(text)
            dataObjectComposite = wx.DataObjectComposite()
            dataObjectComposite.Add(textDataObject)
            if lines == 1:
                iconIndex, _, eventstring, _ = self.GetItemData(firstItem)
                if iconIndex == EVENT_ICON_INDEX:
                    customDataObject = wx.CustomDataObject("DragEventItem")
                    customDataObject.SetData(str(eventstring))
                    dataObjectComposite.Add(customDataObject)
            
            wx.TheClipboard.SetData(dataObjectComposite)
            wx.TheClipboard.Close()
            wx.TheClipboard.Flush()
            eg.app.clipboardEvent.Fire()
            
            
    def OnCmdClearAll(self, event):
        self.SetItemCount(0)
        self.DeleteAllItems()
        self.ScrollList(0, 1000000)
        self.Refresh()
    
    
    def OnBeginColumnDrag(self, event):
        if event.GetColumn() == 0:
            event.Veto()
        else:
            event.Skip()
            
            
    def OnRightUp(self, event):
        self.PopupMenu(self.contextMenu)


    def OnMouseMotion(self, event):
        item, flags = self.HitTest(event.GetPosition())
        if flags & wx.LIST_HITTEST_ONITEM:
            self.tooltip.SetTip(self.OnGetItemText(item, 0))
        
        
    def OnDoubleClick(self, event):
        item, flags = self.HitTest(event.GetPosition())
        if flags & wx.LIST_HITTEST_ONITEM:
            iconIndex, _, wref, _ = self.GetItemData(item)
            if iconIndex != EVENT_ICON_INDEX and wref is not None:
                obj = wref()
                if obj is not None:
                    obj.Select()
        
        
    def GetItemData(self, item):
        return self.data[item]
        
    
    def OnGetItemText(self, item, column):
        if self.logTimes:
            if column == 0:
                return strftime("%X", localtime(self.GetItemData(item)[3]))
            elif column == 1:
                return self.GetItemData(item)[1]
            else:
                return "unknown column" + str(column)
        else:
            if column == 0:
                return self.GetItemData(item)[1]
            else:
                return "unknown column" + str(column)
    
    
    def GetItemLineText(self, item):
        data = self.GetItemData(item)
        if self.logTimes:
            return strftime("%X", localtime(data[3])) + " " + data[1]
        else:
            return data[1]
        
        
    def OnGetItemAttr(self, item):
        if item % 2 == 0:
            return self.attr1
        else:
            return self.attr2


    def OnGetItemImage(self, item):
        return self.GetItemData(item)[0]
    
    
    def OnGetItemColumnImage(self, item, column):
        if column == 0:
            return self.GetItemData(item)[0]
        else:
            return -1


    def __append(self, text, icon, wRef):
        data = self.data
        data.append((icon, text, wRef, time()))
        self.SetItemCount(len(data))
        self.ScrollList(0, 1000000)
        if len(data) >= self.maxlength:
            data.popleft()
            self.DeleteItem(0)
           
        
    def __OnWrite(self, text, icon, wRef=None):
        buffer = self.buffer + text
        n = buffer.find("\n")
        while n != -1:
            self.__append(buffer[:n], icon, wRef)
            buffer = buffer[n+1:]
            n = buffer.find("\n")
        self.buffer = buffer
            

    def DoPrint(self, text, icon=0, wRef=None):
        wx.CallAfter(self.__OnWrite, text + "\n", icon, wRef)
        
        
    def LogEvent(self, event):
        """Store and display an EventGhostEvent in the logger."""
        payload = event.payload
        eventstring = event.string
        if payload is not None:
            if type(payload) == UnicodeType:
                mesg = eventstring + ' u"' + payload + '"'
            else:
                mesg = eventstring + ' ' + repr(payload)
        else:
            mesg = eventstring
        self.__append(mesg, EVENT_ICON_INDEX, eventstring)
        
        

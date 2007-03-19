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

import eg

class PluginInfo(eg.PluginInfo):
    name = "EventGhost"
    author = ""
    version = ""
    description = \
        "Here you find actions that mainly control the core "\
        "functionality of EventGhost."    
    kind = "core"
    
    
import sys
import time
import traceback
import threading
import locale

import wx

from eg import ContainerItem, FolderItem, MacroItem, RootItem, AutostartItem


class EventGhost(eg.PluginClass):
    """
    Plugin: EventGhost
    
    Here you find actions that mainly control the core functionality of 
    EventGhost.
    """
    pass
        


class PythonCommand(eg.ActionWithStringParameter):
    name = "Python Command"
    description = "Executes a parameter as a single Python statement."
    iconFile = 'icons/PythonCommand'
    class text:
        parameterDescription = "Python statement:"

    def __call__(self, pythonstring):
        try:
            try:
                result = eval(pythonstring, {}, eg.globals.__dict__)
                return result
            except SyntaxError:
                eg.globals.result = None
                exec pythonstring in {}, eg.globals.__dict__
                return eg.globals.result
        finally:
            pass
#        except:
#            eg.PrintError(eg.text.Error.InAction % pythonstring)
#            errorlines = traceback.format_exc().splitlines()
#            for i in range(4, len(errorlines)):
#                eg.PrintError(errorlines[i])
#            return
        
        
    def GetLabel(self, pythonstring=""):
        return pythonstring
        
        
        
#-----------------------------------------------------------------------------
# Action: EventGhost.PythonScript
#-----------------------------------------------------------------------------
from PythonScript import PythonScript
    
    
    
class Comment(eg.ActionClass):
    name = "Comment"
    description = \
        "Just a do-nothing action that can be used to comment your "\
        "configuration."
    iconFile = 'icons/Comment'

    def __call__(self):
        pass
        
        
        
#-----------------------------------------------------------------------------
# Action: EventGhost.NewJumpIf
#-----------------------------------------------------------------------------
from NewJumpIf import NewJumpIf



#-----------------------------------------------------------------------------
# Action: EventGhost.EnableItem
#-----------------------------------------------------------------------------
class EnableItem(eg.ActionClass):
    name = "Enable an item"
    description = "Enable an item in the tree."  
    iconFile = 'icons/EnableItem'
    class text:
        label = "Enable: %s"
        text1 = "Please select the item which should be enabled:"

    def __call__(self, link):
        if link:
            obj = link.target
            if obj:
                obj.Enable()
    
    
    def GetLabel(self, link):
        obj = link.target
        if obj:
            return self.text.label % obj.GetLabel()
        return self.text.label % ''
        
        
    def filterFunc(self, obj):
        return True
    
    
    def IsSelectableItem(self, item):
        return not isinstance(item, AutostartItem)


    def Configure(self, link=None):
        dialog = eg.ConfigurationDialog(self, resizeable=True)
        sizer = dialog.sizer
        okButton = dialog.buttonRow.okButton
        staticText = wx.StaticText(dialog, -1, self.text.text1)
        sizer.Add(staticText, 0, wx.BOTTOM, 5)
        self.foundId = None
        if link is not None:
            searchItem = link.target
        else:
            searchItem = None
            link = eg.TreeLink(eg.currentConfigureItem)
            
        tree = eg.TreeItemBrowseCtrl(
            dialog, 
            self.filterFunc, 
            #searchFunc, 
            selectItem=searchItem
        )
        
        if not searchItem:
            okButton.Enable(False)
            
        def selectionFunc(event):
            id = event.GetItem()
            if id.IsOk():
                item = tree.GetPyData(id)
                if self.IsSelectableItem(item):
                    okButton.Enable(True)
                else:
                    okButton.Enable(False)
            event.Skip()
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, selectionFunc)
        #tree.SetMinSize((-1,300))
        tree.SetFocus()
        sizer.Add(tree, 1, wx.EXPAND)

        if dialog.AffirmedShowModal():
            id = tree.GetSelection()
            if id.IsOk():
                obj = tree.GetPyData(id)
                link.SetTarget(obj)
            return (link,)
       
    
    
#-----------------------------------------------------------------------------
# Action: EventGhost.DisableItem
#-----------------------------------------------------------------------------
class DisableItem(EnableItem):
    name = "Disable an item"
    description = "Disable an item"
    iconFile = 'icons/DisableItem'
    class text:
        label = "Disable: %s"
        text1 = "Please select the item which should be disabled:"
        

    def __call__(self, link):
        if link:
            obj = link.target
            if obj:
                obj.Enable(False)



class EnableExclusive(EnableItem):
    name = "Exclusive enable a folder/macro"
    description = (
        "This will enable a specified folder or macro in your "
        "configuration, but also disable all other folders and "
        "macros that are siblings on the same level in this "
        "sub-branch of the tree."
    )
    iconFile = "icons/EnableExclusive"
    class text:
        label = "Enable exclusive: %s"
        text1 = "Please select the folder/macro which should be enabled:"
        
    
    def __call__(self, link):
        if not link:
            return
        item = link.target
        if not item:
            return
        def DoIt():
            item.Enable(True)
            for child in item.parent.childs:
                if child is not item:
                    child.Enable(False)
        eg.actionThread.Call(DoIt)
                
                
    def filterFunc(self, obj):
        return obj.__class__.__bases__[0] in (FolderItem, MacroItem)
    
    
    def IsSelectableItem(self, item):
        return item.__class__.__bases__[0] is not RootItem
    
    
    
class Wait(eg.ActionClass):
    name = "Wait some time"
    description = "Wait some time"        
    iconFile = "icons/Wait"
    class text:
        label = "Wait: %s sec"
        wait = "Wait"
        seconds = "seconds"

    def __call__(self, waitTime):
        eg.actionThread.Wait(waitTime)


    def GetLabel(self, waitTime=0):
        return self.text.label % str(waitTime)


    def Configure(self, waitTime=0.0):
        dialog = eg.ConfigurationDialog(self)
        mySizer = wx.BoxSizer(wx.HORIZONTAL)
        staticText = wx.StaticText(dialog, -1, self.text.wait)
        mySizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        waitTimeCtrl = eg.SpinNumCtrl(
            dialog, 
            -1,
            waitTime,
            integerWidth=3
        )
        mySizer.Add(waitTimeCtrl, 0, wx.EXPAND)
        staticText = wx.StaticText(dialog, -1, self.text.seconds)
        mySizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        dialog.sizer.Add(mySizer, 0, wx.EXPAND)
        
        yield dialog
        yield (waitTimeCtrl.GetValue(),)
        


class StopProcessing(eg.ActionClass):
    name = "Stop processing this event"
    description = "Stop processing this event"
    iconFile = 'icons/StopProcessing'

    def __call__(self):
        eg.event.skipEvent = True



class JumpIfLongPress(eg.ActionClass):
    name = "Jump if long press"
    description = \
        "Jumps to another macro, if the button on the remote is "\
        "held down longer than the configured time."
    iconFile = "icons/LongPress"
    class text:
        label = "If button is held down %s sec, go to: %s"
        text1 = "If button is held down for longer than"
        text2 = "seconds,"
        text3 = "jump to:"
        text4 = "Select the long press macro..."
        text5 = \
            "Please select the macro, which should be triggered "\
            "if the event is a long event."
        
    
    def __call__(self, interval, link):
        eg.event.shouldEnd.wait(interval)
        if not eg.event.shouldEnd.isSet():
            next = link.target
            next_id = next.parent.GetChildIndex(next)
            eg.SetProgramCounter((next, next_id))
                
                
    def GetLabel(self, interval, link):
        return self.text.label % (interval, link.target.name)


    def Configure(self, interval=2.0, link=None):
        dialog = eg.ConfigurationDialog(self)
        text = self.text
        if link is None:
            link = eg.TreeLink(eg.currentConfigureItem)
        
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        textCtrl = wx.StaticText(dialog, -1, text.text1)
        sizer1.Add(textCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        intervalCtrl = eg.SpinNumCtrl(dialog)
        intervalCtrl.SetValue(interval)
        sizer1.Add(intervalCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        textCtrl = wx.StaticText(dialog, -1, text.text2)
        sizer1.Add(textCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        dialog.sizer.Add(sizer1)
        
        mySizer = wx.FlexGridSizer(2,3,5,5)
        mySizer.AddGrowableCol(1, 1)
        
        textCtrl = wx.StaticText(dialog, -1, text.text3)
        mySizer.Add(textCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        button = eg.BrowseMacroButton(  
            dialog,
            eg.text.General.choose,
            text.text4,
            text.text5,
            link.target
        )
        mySizer.Add(button, 1, wx.EXPAND)
                    
        dialog.sizer.Add(mySizer, 1, wx.EXPAND|wx.TOP, 5)
        
        yield dialog
        link.SetTarget(button.GetValue())
        yield (
            intervalCtrl.GetValue(), 
            link
        )



class AutoRepeat(eg.ActionClass):
    name = "Autorepeat current macro"
    description = \
        "Makes the macro where this command is added to an "\
        "autorepeating macro."
    iconFile = "icons/AutoRepeat"
    class text:
        seconds = "seconds"
        text1 = "Start first repetition after"
        text2 = "with one repetition every"
        text3 = "Increase repetition the next"
        text4 = "to one repetition every"
        

    def __call__(
        self, 
        firstDelay=0.6, 
        startDelay=0.3,
        endDelay=0.01, 
        sweepTime=3.0
    ):
        event = eg.event
        if not event.shouldEnd.isSet():
            x = time.clock() - event.time
            if x < firstDelay * 0.90:
                res = firstDelay
            else:
                x = x + firstDelay
                s = startDelay - endDelay
                d = (s / sweepTime) * (sweepTime - x)
                if d < 0:
                    d = 0
                res = d + endDelay
            event.shouldEnd.wait(res)
            #wait_event.wait(res)
            if not event.shouldEnd.isSet():
                eg.SetProgramCounter((eg.currentItem.parent.childs[0], 0))
            
            
    def Configure(
        self, 
        firstDelay=0.6, 
        startDelay=0.3,
        endDelay=0.01, 
        sweepTime=3.0
    ):
        dialog = eg.ConfigurationDialog(self)
        text = self.text

        st1 = wx.StaticText(dialog, -1, text.text1)
        firstDelayCtrl = eg.SpinNumCtrl(dialog)
        firstDelayCtrl.SetValue(firstDelay)
        st2 = wx.StaticText(dialog, -1, text.seconds)
        
        st3 = wx.StaticText(dialog, -1, text.text2)
        startDelayCtrl = eg.SpinNumCtrl(dialog)
        startDelayCtrl.SetValue(startDelay)
        st4 = wx.StaticText(dialog, -1, text.seconds)
        
        st5 = wx.StaticText(dialog, -1, text.text3)
        sweepTimeCtrl = eg.SpinNumCtrl(dialog)
        sweepTimeCtrl.SetValue(sweepTime)
        st6 = wx.StaticText(dialog, -1, text.seconds)
        
        st7 = wx.StaticText(dialog, -1, text.text4)
        endDelayCtrl = eg.SpinNumCtrl(dialog)
        endDelayCtrl.SetValue(endDelay)
        st8 = wx.StaticText(dialog, -1, text.seconds)
        
        sizer = wx.FlexGridSizer(4,3,5,5)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)
        sizer.AddGrowableCol(0, 1)
        Add = sizer.Add
        Add(st1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        Add(firstDelayCtrl, 1, wx.EXPAND)
        Add(st2, 0, wx.ALIGN_CENTER_VERTICAL)
        Add(st3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        Add(startDelayCtrl, 1, wx.EXPAND)
        Add(st4, 0, wx.ALIGN_CENTER_VERTICAL)
        Add((5, 5))
        Add((5, 5))
        Add((5, 5))
        Add(st5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        Add(sweepTimeCtrl, 1, wx.EXPAND)
        Add(st6, 0, wx.ALIGN_CENTER_VERTICAL)
        Add(st7, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        Add(endDelayCtrl, 1, wx.EXPAND)
        Add(st8, 0, wx.ALIGN_CENTER_VERTICAL)
        
        dialog.sizer.Add(sizer)#, 0, wx.EXPAND)
        
        yield dialog
        yield (
            firstDelayCtrl.GetValue(),
            startDelayCtrl.GetValue(),
            endDelayCtrl.GetValue(),
            sweepTimeCtrl.GetValue()
        )



class TriggerEvent(eg.ActionClass):
    name = "Trigger Event"
    description = \
        "Causes an event to be generated (optionally after some "\
        "time)."
    iconFile = "icons/Plugin"
    class text:
        labelWithTime = 'Trigger event "%s" after %.2f seconds'
        labelWithoutTime = 'Trigger event "%s"'
        text1 = "Event string to fire:"
        text2 = "Delay the firing of the event:"
        text3 = "seconds. (0 = fire immediately)"
        
    
    def __call__(self, eventString, waitTime=0):
        eventString = eg.ParseString(eventString)
        if not waitTime:
            eg.TriggerEvent(eventString)
        else:
            t = threading.Timer(waitTime, eg.TriggerEvent, (eventString,))
            t.start()


    def GetLabel(self, eventString="", waitTime=0):
        if waitTime:
            return self.text.labelWithTime % (eventString, waitTime)
        else:
            return self.text.labelWithoutTime % eventString
        
    
    def Configure(self, eventString="", waitTime=0):
        dialog = eg.ConfigurationDialog(self)
        sizer = dialog.sizer
        text = self.text
        
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        staticText = wx.StaticText(dialog, -1, text.text1)
        sizer1.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL, 5)
        
        eventStringCtrl = wx.TextCtrl(dialog, -1, eventString, size=(250, -1))
        sizer1.Add(eventStringCtrl, 0, wx.LEFT, 5)
        sizer.Add(sizer1, 0, wx.EXPAND)
        
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        staticText = wx.StaticText(dialog, -1, text.text2)
        sizer2.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL)
        waitTimeCtrl = eg.SpinNumCtrl(dialog, -1, waitTime, integerWidth=5)
        sizer2.Add(waitTimeCtrl, 0, wx.ALL, 5)
        staticText = wx.StaticText(dialog, -1, text.text3)
        sizer2.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(sizer2, 0, wx.EXPAND)
        
        yield dialog
        yield (
            eventStringCtrl.GetValue(),
            waitTimeCtrl.GetValue(),
        )
    
    

class FlushEvents(eg.ActionClass):
    name = "Flush Events"
    description = \
        "The \"Flush Events\" flushes all events which are "\
        "currently in the processing queue. It is useful in case a "\
        "macro has just some lengthy processing, and events have "\
        "queued up during that processing which should not be "\
        "processed.\n\n<p>"\
        "<b>Example:</b> You have a lengthy \"start system\" macro "\
        "which takes about 90 seconds to process. The end user will "\
        "not see anything until the projector lights up, which "\
        "takes 60s. It is very likely that he presses the remote "\
        "button which starts the macro for several times in a row, "\
        "causing all of the lengthy processing to start over and "\
        "over again. If you place a \"Flush Events\" command at the "\
        "end of your macro, all the excessive remote key presses "\
        "will be discarded."
    iconFile = "icons/Plugin"
    
    def __call__(self):
        eg.eventThread.FlushAllEvents()
        eg.actionThread.FlushAllEvents()



#-----------------------------------------------------------------------------
# Action: EventGhost.Jump
#-----------------------------------------------------------------------------
class Jump(eg.ActionClass, eg.HiddenAction):
    name = "Jump"
    description = \
        "Jumps unconditionally to another macro and optionally "\
        "returns from there."        
    iconFile = 'icons/LongPress'
    class text:
        label1 = "Jump to %s"
        label2 = "Jump to %s and return"
        text2 = "Jump to:"
        text3 = "Return after execution"
        mesg1 = "Select the macro..."
        mesg2 = "Please select the macro that should be executed:"

    
    def __call__(self, link, gosub=False):
        if gosub:
            eg.programReturnStack.append(eg.programCounter)
        next = link.target
        next_id = next.parent.GetChildIndex(next)
        eg.SetProgramCounter((next, next_id))


    def GetLabel(self, link, gosub=False):
        if gosub:
            return self.text.label2 % link.target.name
        else:
            return self.text.label1 % link.target.name
        
        
    def Configure(self, link=None, gosub=False):
        dialog = eg.ConfigurationDialog(self)
        if link is None:
            link = eg.TreeLink(dialog.actionItem)
        text = self.text
        label2 = wx.StaticText(dialog, -1, text.text2)
        button = eg.BrowseMacroButton(  
            dialog,
            eg.text.General.choose,
            text.mesg1,
            text.mesg2,
            link.target
        )
        gosubCB = wx.CheckBox(dialog, -1, text.text3)
        gosubCB.SetValue(gosub)
        sizer = wx.FlexGridSizer(2, 2, 5, 5)
        sizer.AddGrowableCol(1, 1)
        sizer.AddGrowableRow(1, 1)
        sizer.Add(label2, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(button, 1, wx.EXPAND)
        sizer.Add((0, 0))
        sizer.Add(gosubCB, 0, wx.EXPAND)
        dialog.sizer.Add(sizer, 1, wx.EXPAND)
        
        if dialog.AffirmedShowModal():
            link.SetTarget(button.GetValue())
            return (
                link, 
                gosubCB.GetValue()
            )
    
    
    
#-----------------------------------------------------------------------------
# Action: EventGhost.JumpIf
#-----------------------------------------------------------------------------
class JumpIf(eg.ActionClass, eg.HiddenAction):
    name = "Jump if"
    description = \
        "Jumps to another macro, if the specified python-evaluation "\
        "returns true."        
    iconFile = 'icons/LongPress'
    class text:
        label1 = "If %s goto %s"
        label2 = "If %s gosub %s"
        text1 = "If:"
        text2 = "Go to:"
        text3 = "Return after execution"
        mesg1 = "Select the macro..."
        mesg2 = \
            "Please select the macro that should be executed, if the "\
            "condition is true."

    
    def __call__(self, evalstr, link, gosub=False):
        try:
            result = eval(evalstr, {}, eg.globals.__dict__)
        except:
            result = False
            eg.PrintError("Error in evaluating Python expression")
        if result:
            if gosub:
                eg.programReturnStack.append(eg.programCounter)
            next = link.target
            next_id = next.parent.GetChildIndex(next)
            eg.SetProgramCounter((next, next_id))
        
        
    def GetLabel(self, evalstr, link, gosub=False):
        if gosub:
            return self.text.label2 % (evalstr, link.target.name)
        else:
            return self.text.label1 % (evalstr, link.target.name)


    def Configure(
        self, 
        evalStr='', 
        link=None, 
        gosub=False
    ):
        dialog = eg.ConfigurationDialog(self)
        if link is None:
            link = eg.TreeLink(dialog.actionItem)
        text = self.text
        label1 = wx.StaticText(dialog, -1, text.text1)
        evalCtrl = wx.TextCtrl(dialog, -1, evalStr)
        label2 = wx.StaticText(dialog, -1, text.text2)
        button = eg.BrowseMacroButton(  
            dialog,
            eg.text.General.choose,
            text.mesg1,
            text.mesg2,
            link.target
        )
        gosubCB = wx.CheckBox(dialog, -1, text.text3)
        gosubCB.SetValue(gosub)
        sizer = wx.FlexGridSizer(2,2,5,5)
        sizer.AddGrowableCol(1, 1)
        sizer.AddGrowableRow(1, 1)
        sizer.Add(label1, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(evalCtrl, 1, wx.EXPAND)
        sizer.Add(label2, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(button, 1, wx.EXPAND)
        sizer.Add((0,0))
        sizer.Add(gosubCB, 0, wx.EXPAND)
        dialog.sizer.Add(sizer, 1, wx.EXPAND)
        
        if dialog.AffirmedShowModal():
            link.SetTarget(button.GetValue())
            return (
                evalCtrl.GetValue(), 
                link, 
                gosubCB.GetValue()
            )



#-----------------------------------------------------------------------------
# Action: EventGhost.StopIf
#-----------------------------------------------------------------------------
class StopIf(eg.ActionWithStringParameter, eg.HiddenAction):
    name = "Stop if"
    description = \
        "Stops executing the current macro, if the specified "\
        "Python-evaluation returns true."
    iconFile = 'icons/StopProcessing'
    class text:
        label = "Stop if %s"
        parameterDescription = "Python condition:"
        
    
    def __call__(self, evalstr):
        try:
            result = eval(evalstr, {}, eg.globals.__dict__)
        except:
            result = False
            eg.PrintTraceback()
        if result:
            eg.SetProgramCounter(None)
        return eg.globals.result
        
        
    def GetLabel(self, evalstr):
        return self.text.label % evalstr


#-----------------------------------------------------------------------------
# Action: EventGhost.ShowOSD
#-----------------------------------------------------------------------------
import ShowOSD


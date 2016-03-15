# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

eg.RegisterPlugin(
    name = "EventGhost",
    author = "Bitmonster",
    description = (
        "Here you find actions that mainly control the core functionality of"
        "EventGhost."
    ),
    kind = "core",
    version = "1.0.7",
    guid = "{9D499A2C-72B6-40B0-8C8C-995831B10BB4}",
)

import wx
import sys
import time
import traceback
from threading import Event, Thread
from eg import ContainerItem, FolderItem, MacroItem, RootItem, AutostartItem

from PythonScript import PythonScript
from ShowOSD import ShowOSD
from NewJumpIf import NewJumpIf
from JumpIfElse import JumpIfElse
from win32gui import FindWindow, MessageBox
from eg.WinApi.Utils import BringHwndToFront
from winsound import PlaySound, SND_ASYNC
from os.path import join
from eg.WinApi.Dynamic import CreateEvent, SetEvent

from win32con import (
    # constants:
    MB_TOPMOST, MB_ABORTRETRYIGNORE, MB_ICONERROR, MB_ICONINFORMATION,
    MB_ICONQUESTION, MB_ICONWARNING, MB_NOFOCUS, MB_OK, MB_OKCANCEL,
    MB_RETRYCANCEL, MB_SYSTEMMODAL, MB_YESNO, MB_YESNOCANCEL
)
ACV   = wx.ALIGN_CENTER_VERTICAL



class EventGhost(eg.PluginBase):
    """
    Plugin: EventGhost

    Here you find actions that mainly control the core functionality of
    EventGhost.
    """
    def __init__(self):
        self.AddAction(PythonCommand)
        self.AddAction(PythonScript)
        self.AddAction(Comment)
        self.AddAction(EnableItem)
        self.AddAction(DisableItem)
        self.AddAction(GetItemState)
        self.AddAction(EnableExclusive)
        self.AddAction(Wait)
        self.AddAction(StopProcessing)
        self.AddAction(OpenConfig)
        self.AddAction(NewJumpIf)
        self.AddAction(JumpIfElse)
        self.AddAction(JumpIfLongPress)
        self.AddAction(JumpIfDoubleEvent)
        self.AddAction(AutoRepeat)
        self.AddAction(TriggerEvent)
        self.AddAction(FlushEvents)
        self.AddAction(ShowOSD)
        self.AddAction(ShowMessageBox)
        self.AddAction(DumpResult)


class PythonCommand(eg.ActionWithStringParameter):
    name = "Python Command"
    description = "Executes a single Python statement."
    iconFile = 'icons/PythonCommand'
    class text:
        parameterDescription = "Python statement:"

    def __call__(self, pythonstring=""):
        try:
            try:
                result = eval(pythonstring, {}, eg.globals.__dict__)
                return result
            except SyntaxError:
                exec(pythonstring, {}, eg.globals.__dict__)
                return eg.result
        except:
            eg.PrintTraceback(
                eg.text.Error.InAction % pythonstring,
                skip=1,
                source=eg.currentItem
            )


    def GetLabel(self, pythonstring=""):
        return pythonstring



class Comment(eg.ActionBase):
    name = "Comment"
    description = \
        "Just a do-nothing action that can be used to comment your "\
        "configuration."
    iconFile = 'icons/Comment'

    def __call__(self):
        pass



class EnableItem(eg.ActionBase):
    name = "Enable an item"
    description = "Enable an item in the tree."
    iconFile = 'icons/EnableItem'
    class text:
        label = "Enable: %s"
        text1 = "Please select the item which should be enabled:"
        cantSelect = (
            "The selected item type can't change its enable state.\n\n"
            "Please select another item."
        )

    def __call__(self, link):
        if link:
            node = link.target
            if node:
                node.SetEnable(True)
                return node


    def GetLabel(self, link):
        obj = link.target
        if obj:
            return self.text.label % obj.GetLabel()
        return self.text.label % ''


    def FilterFunc(self, dummyObj):
        return True


    def IsSelectableItem(self, item):
        return item.isDeactivatable


    def Configure(self, link=None):
        panel = eg.ConfigPanel(resizable=True)
        if link is not None:
            searchItem = link.target
        else:
            searchItem = None
        link = eg.TreeLink(panel.dialog.treeItem)

        tree = eg.TreeItemBrowseCtrl(
            panel,
            self.FilterFunc,
            #searchFunc,
            selectItem=searchItem
        )
        tree.SetFocus()
        panel.sizer.Add(panel.StaticText(self.text.text1), 0, wx.BOTTOM, 5)
        panel.sizer.Add(tree, 1, wx.EXPAND)
        while panel.Affirmed():
            treeItem = tree.GetSelection()
            if treeItem.IsOk():
                obj = tree.GetPyData(treeItem)
                if self.IsSelectableItem(obj):
                    link.SetTarget(obj)
                    panel.SetResult(link)
                    continue
            eg.MessageBox(self.text.cantSelect, parent=panel)



class DisableItem(EnableItem):
    name = "Disable an item"
    description = "Disable an item"
    iconFile = 'icons/DisableItem'
    class text:
        label = "Disable: %s"
        text1 = "Please select the item which should be disabled:"
        cantSelect = (
            "The selected item type can't change its enable state.\n\n"
            "Please select another item."
        )


    def __call__(self, link):
        if link:
            node = link.target
            if node and node.isDeactivatable:
                node.SetEnable(False)
                return node



class GetItemState(EnableItem):
    name = "Get item enable state"
    description = "Gets item enable state (True when enabled)"
    iconFile = 'icons/DisableItem'
    class text:
        label = "Item: %s"
        text1 = "Please select the item whose enable state should be detected:"
        cantSelect = (
            "The enable state of selected item can't be detected.\n\n"
            "Please select another item."
        )


    def __call__(self, link):
        if link:
            node = link.target
            if node and node.isDeactivatable:
                return node.isEnabled


class EnableExclusive(EnableItem):
    name = "Exclusive enable a folder/macro"
    description = """
        This will enable a specified folder or macro in your configuration,
        but also disable all other folders and macros that are siblings on the
        same level in this sub-branch of the tree.
    """
    iconFile = "icons/EnableExclusive"
    class text:
        label = "Enable exclusive: %s"
        text1 = "Please select the folder/macro which should be enabled:"
        cantSelect = (
            "The selected item type can't change its enable state.\n\n"
            "Please select another item."
        )


    def __call__(self, link):
        if not link:
            return
        node = link.target
        if not node:
            return
        def DoIt():
            node.SetEnable(True)
            for child in node.parent.childs:
                if child is not node and child.isDeactivatable:
                    child.SetEnable(False)
        eg.actionThread.Call(DoIt)


    def FilterFunc(self, item):
        return isinstance(item, (FolderItem, MacroItem))


    def IsSelectableItem(self, item):
        return item.isDeactivatable




class Wait(eg.ActionBase):
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
        panel = eg.ConfigPanel()
        waitTimeCtrl = panel.SpinNumCtrl(waitTime, integerWidth=3)
        panel.AddLine(self.text.wait, waitTimeCtrl, self.text.seconds)
        while panel.Affirmed():
            panel.SetResult(waitTimeCtrl.GetValue())



class StopProcessing(eg.ActionBase):
    name = "Stop processing this event"
    description = """
        After this action, EventGhost will no further search for matching
        macros of the currently processed event.
    """
    iconFile = 'icons/StopProcessing'

    def __call__(self):
        eg.event.skipEvent = True


def BringDialogToFront(name):
    hwnd = 0
    i = 0
    while hwnd == 0 and i < 10000:
        hwnd = FindWindow("#32770", name)
        i += 1
    if hwnd:
        BringHwndToFront(hwnd)



class OpenConfig(eg.ActionBase):
    name = "Open configuration dialogue"
    description = """
        Opens selected configuration dialogue.
    """
    iconFile = "icons/Dialog"
    class text:
        text0 = "Action or plugin: "
        text1 = "Select action or plugin..."
        text2 = \
            "Please select the action or plugin, whose configuration dialogue "\
            "should be opened."


    def __call__(self, link):
        wx.CallAfter(eg.document.OnCmdConfigure, link.target)
        wx.CallAfter(
            BringDialogToFront,
            eg.text.General.settingsActionCaption
        )


    def GetLabel(self, link):
        label = link.target.GetLabel() if link else ""
        return "%s: %s" % (self.name, label)


    def Configure(self, link=None):
        panel = eg.ConfigPanel()
        text = self.text
        actionCtrl = eg.ActionSelectButton(
            panel,
            eg.text.General.choose,
            text.text1,
            text.text2,
            link
        )
        mySizer = wx.FlexGridSizer(2, 2, 5, 5)
        mySizer.AddGrowableCol(1)
        mySizer.Add(panel.StaticText(text.text0), 0, wx.ALIGN_CENTER_VERTICAL)
        mySizer.Add(actionCtrl, 1, wx.EXPAND)
        panel.sizer.Add(mySizer, 1, wx.EXPAND|wx.ALL, 5)

        while panel.Affirmed():
            panel.SetResult(actionCtrl.GetValue())


class JumpIfLongPress(eg.ActionBase):
    name = "Jump if long press"
    description = """
        Jumps to another macro, if the button on the remote is held down longer
        than the configured time.
    """
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
            nextItem = link.target
            nextIndex = nextItem.parent.GetChildIndex(nextItem)
            eg.programCounter = (nextItem, nextIndex)


    def GetLabel(self, interval, link):
        return self.text.label % (interval, link.target.name)


    def Configure(self, interval=2.0, link=None):
        panel = eg.ConfigPanel()
        text = self.text
        intervalCtrl = panel.SpinNumCtrl(interval)
        macroCtrl = eg.MacroSelectButton(
            panel,
            eg.text.General.choose,
            text.text4,
            text.text5,
            link
        )

        sizer1 = eg.HBoxSizer(
            (panel.StaticText(text.text1), 0, wx.ALIGN_CENTER_VERTICAL),
            (intervalCtrl, 0, wx.LEFT|wx.RIGHT, 5),
            (panel.StaticText(text.text2), 0, wx.ALIGN_CENTER_VERTICAL),
        )
        mySizer = wx.FlexGridSizer(2, 3, 5, 5)
        mySizer.AddGrowableCol(1, 1)
        mySizer.Add(panel.StaticText(text.text3), 0, wx.ALIGN_CENTER_VERTICAL)
        mySizer.Add(macroCtrl, 1, wx.EXPAND)

        panel.sizer.AddMany(((sizer1), (mySizer, 1, wx.EXPAND|wx.TOP, 5)))
        while panel.Affirmed():
            panel.SetResult(intervalCtrl.GetValue(), macroCtrl.GetValue())



class JumpIfDoubleEvent(eg.ActionBase):
    name = "Jump if double event"
    description = (
        "Jumps to another macro, if the same event that has triggered this "
        "macro, happens twice in a given time."
    )
    iconFile = "icons/LongPress"
    class text:
        label = "If event arrives twice, go to: %s"
        text1 = "If event arrives twice within"
        text2 = "seconds,"
        text3 = "jump to:"
        text4 = (
            "Select the macro that should be executed if the event happens "
            "twice..."
        )
        text5 = (
            "Please select the macro, which should be triggered "
            "if the event is a double click."
        )

    def __call__(self, interval, link):
        firstEvent = eg.event
        # wait for the first event to release
        firstEvent.shouldEnd.wait(10.0)

        waitEvent = Event()
        waitEvent.wasSameEvent = False
        def EventFilter(event):
            if event.string == firstEvent.string:
                waitEvent.wasSameEvent = True
                waitEvent.secondEvent = event
                waitEvent.set()
                return True
            else:
                waitEvent.set()

        eg.eventThread.AddFilter(firstEvent.source, EventFilter)
        waitEvent.wait(interval)
        eg.eventThread.RemoveFilter(firstEvent.source, EventFilter)
        if waitEvent.isSet() and waitEvent.wasSameEvent:
            nextItem = link.target
            nextIndex = nextItem.parent.GetChildIndex(nextItem)
            eg.programCounter = (nextItem, nextIndex)
            eg.event = waitEvent.secondEvent


    def GetLabel(self, interval, link):
        return self.text.label % (link.target.name)


    def Configure(self, interval=0.5, link=None):
        panel = eg.ConfigPanel()
        text = self.text
        intervalCtrl = panel.SpinNumCtrl(interval)
        macroCtrl = eg.MacroSelectButton(
            panel,
            eg.text.General.choose,
            text.text4,
            text.text5,
            link
        )

        sizer1 = eg.HBoxSizer(
            (panel.StaticText(text.text1), 0, wx.ALIGN_CENTER_VERTICAL),
            (intervalCtrl, 0, wx.LEFT|wx.RIGHT, 5),
            (panel.StaticText(text.text2), 0, wx.ALIGN_CENTER_VERTICAL),
        )
        mySizer = wx.FlexGridSizer(2, 3, 5, 5)
        mySizer.AddGrowableCol(1, 1)
        mySizer.Add(panel.StaticText(text.text3), 0, wx.ALIGN_CENTER_VERTICAL)
        mySizer.Add(macroCtrl, 1, wx.EXPAND)

        panel.sizer.AddMany(((sizer1), (mySizer, 1, wx.EXPAND|wx.TOP, 5)))
        while panel.Affirmed():
            panel.SetResult(intervalCtrl.GetValue(), macroCtrl.GetValue())



class AutoRepeat(eg.ActionBase):
    name = "Autorepeat current macro"
    description = (
        "Makes the macro where this command is added to an autorepeating "
        "macro."
    )
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
        if event.shouldEnd.isSet():
            return
        elapsed = time.clock() - event.time
        if elapsed < firstDelay * 0.90:
            delay = firstDelay
        elif sweepTime > 0.0:
            sweepDelay = (
                (startDelay - endDelay)
                * (sweepTime - (elapsed + firstDelay))
                / sweepTime
            )
            if sweepDelay < 0:
                sweepDelay = 0
            delay = sweepDelay + endDelay
        else:
            delay = endDelay
        event.shouldEnd.wait(delay)
        if not event.shouldEnd.isSet():
            eg.programCounter = (eg.currentItem.parent.childs[0], 0)


    def Configure(
        self,
        firstDelay=0.6,
        startDelay=0.3,
        endDelay=0.01,
        sweepTime=3.0
    ):
        text = self.text
        panel = eg.ConfigPanel()
        firstDelayCtrl = panel.SpinNumCtrl(firstDelay)
        startDelayCtrl = panel.SpinNumCtrl(startDelay)
        sweepTimeCtrl = panel.SpinNumCtrl(sweepTime)
        endDelayCtrl = panel.SpinNumCtrl(endDelay)

        panel.SetColumnFlags(0, wx.ALIGN_RIGHT)
        panel.AddLine(text.text1, firstDelayCtrl, text.seconds)
        panel.AddLine(text.text2, startDelayCtrl, text.seconds)
        panel.AddLine()
        panel.AddLine(text.text3, sweepTimeCtrl, text.seconds)
        panel.AddLine(text.text4, endDelayCtrl, text.seconds)

        while panel.Affirmed():
            panel.SetResult(
                firstDelayCtrl.GetValue(),
                startDelayCtrl.GetValue(),
                endDelayCtrl.GetValue(),
                sweepTimeCtrl.GetValue()
            )



class TriggerEvent(eg.ActionBase):
    name = "Trigger Event"
    description = \
        "Causes an event to be generated (optionally after some time)."
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
            eg.scheduler.AddShortTask(waitTime, eg.TriggerEvent, eventString)


    def GetLabel(self, eventString="", waitTime=0):
        if waitTime:
            return self.text.labelWithTime % (eventString, waitTime)
        else:
            return self.text.labelWithoutTime % eventString


    def Configure(self, eventString="", waitTime=0):
        panel = eg.ConfigPanel()
        text = self.text

        eventStringCtrl = panel.TextCtrl(eventString, size=(250, -1))
        waitTimeCtrl = panel.SpinNumCtrl(waitTime, integerWidth=5)

        sizer1 = eg.HBoxSizer(
            (panel.StaticText(text.text1), 0, wx.ALIGN_CENTER_VERTICAL, 5),
            (eventStringCtrl, 0, wx.LEFT, 5),
        )
        sizer2 = eg.HBoxSizer(
            (panel.StaticText(text.text2), 0, wx.ALIGN_CENTER_VERTICAL),
            (waitTimeCtrl, 0, wx.ALL, 5),
            (panel.StaticText(text.text3), 0, wx.ALIGN_CENTER_VERTICAL),
        )
        panel.sizer.AddMany(((sizer1, 0, wx.EXPAND), (sizer2, 0, wx.EXPAND)))
        while panel.Affirmed():
            panel.SetResult(
                eventStringCtrl.GetValue(),
                waitTimeCtrl.GetValue(),
            )



class FlushEvents(eg.ActionBase):
    name = "Clear Pending Events"
    description = """<rst>
        The "Clear Pending Events" clears all unprocessed events which are
        currently in the processing queue.

        It is useful in case a macro has just some lengthy processing, and
        events have queued up during that processing which should not be
        processed.

        **Example:** You have a lengthy "start system" macro which takes about
        90 seconds to process. The end user will not see anything until the
        projector lights up, which takes 60s. It is very likely that he presses
        the remote button which starts the macro for several times in a row,
        causing all of the lengthy processing to start over and over again. If
        you place a "Clear Pending Events" command at the end of your macro,
        all the excessive remote key presses will be discarded.
    """
    iconFile = "icons/Plugin"

    def __call__(self):
        eg.eventThread.ClearPendingEvents()
        eg.actionThread.ClearPendingEvents()


class DumpResult(eg.ActionBase):
    name = "Dump Result to Log"
    description = "Outputs the most recent eg.result to your EventGhost log. Useful for debugging."

    def __call__(self):
        result = eg.result
        print str(result)
        return result




#===============================================================================

class MessageBoxDialog(wx.Dialog):

    ARTS = (
        None,
        wx.ART_INFORMATION,
        wx.ART_QUESTION,
        wx.ART_WARNING,
        wx.ART_ERROR
    )
    SOUNDS = (
        'SystemExclamation',
        'SystemAsterisk',
        'SystemQuestion',
        'SystemExclamation',
        'SystemHand'
    )
    BUTTONS = (
        (wx.ID_OK,),
        (wx.ID_OK, wx.ID_CANCEL),
        (wx.ID_RETRY, wx.ID_CANCEL),
        (wx.ID_ABORT, wx.ID_RETRY, wx.ID_IGNORE),
        (wx.ID_YES, wx.ID_NO),
        (wx.ID_YES, wx.ID_NO, wx.ID_CANCEL),
    )
    LABELS = {
        wx.ID_OK:"ok",
        wx.ID_CANCEL:"cancel",
        wx.ID_RETRY:"retry",
        wx.ID_ABORT:"abort",
        wx.ID_IGNORE:"ignore",
        wx.ID_YES:"yes",
        wx.ID_NO:"no",
    }

    def __init__(
        self,
        parent,
        title = "",
        message = "",
        alias = "",
        payload = None,
        flags = 0,
        time = 0,
        action = None,
        event = None
    ):
        self.alias = alias
        self.payload = payload
        self.action = action
        self.event = event
        self.title = title if title else eg.APP_NAME
        optionFlags, iconFlag, buttonFlags = action.getFlags(flags)
        dialogStyle = wx.DEFAULT_DIALOG_STYLE & (~wx.CLOSE_BOX)
        if optionFlags & 2:
            dialogStyle |= wx.STAY_ON_TOP
        wx.Dialog.__init__(self, parent, -1, "", wx.DefaultPosition, style=dialogStyle)
        self.SetTitle(title)
        icon = wx.EmptyIcon()
        icon.LoadFile(join(eg.imagesDir, "icon32x32.png"), wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        art = self.ARTS[iconFlag]
        if art is not None:
            bmp = wx.ArtProvider.GetBitmap(art, wx.ART_MESSAGE_BOX, (32,32))
            icon = wx.StaticBitmap(self, -1, bmp)
        else:
            icon = (32,32)
        if optionFlags & 4:
            PlaySound(self.SOUNDS[iconFlag], SND_ASYNC)
        message = wx.StaticText(self, -1, message)
        font = message.GetFont()
        font.SetPointSize(10)
        message.SetFont(font)
        message.Wrap(416)
        line = wx.StaticLine(self, -1, size=(1,-1), style = wx.LI_HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add((10, 1))

        if time:
            self.cnt = time
            txt = action.text.autoClose % self.cnt
            info = wx.StaticText(self, -1, txt)
            info.Enable(False)
            bottomSizer.Add(info, 0, wx.TOP, 3)

            def UpdateInfoLabel(evt):
                self.cnt -= 1
                txt = action.text.autoClose % self.cnt
                info.SetLabel(txt)
                if not self.cnt:
                    self.SetReturnCode(wx.ID_CANCEL)
                    self.Close()

            self.Bind(wx.EVT_TIMER, UpdateInfoLabel)
            self.timer = wx.Timer(self)
            self.timer.Start(1000)
        else:
            self.timer = None

        bottomSizer.Add((5,1), 1, wx.EXPAND)
        buttons = self.BUTTONS[buttonFlags]
        for bttn in buttons:
            b = wx.Button(self, bttn, action.text.__dict__[self.LABELS[bttn]])
            b.SetFont(font)
            bottomSizer.Add(b, 0, wx.LEFT, 5)
        bottomSizer.Add((10, 1))
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add((1,1),0,wx.LEFT|wx.RIGHT,5)
        topSizer.Add(icon,0,wx.LEFT|wx.RIGHT|wx.TOP,10)
        topSizer.Add(message,0,wx.TOP|wx.BOTTOM,10)
        topSizer.Add((1,1),0,wx.EXPAND|wx.RIGHT,35)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)
        mainSizer.Add(line, 0, wx.EXPAND|wx.ALL,5)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND|wx.BOTTOM, 5)
        self.SetSizer(mainSizer)
        self.Fit()
        self.Bind(wx.EVT_CLOSE, self.onClose)

        def OnButton(evt):
            self.SetReturnCode(evt.GetId())
            self.Close()
            evt.Skip()
        wx.EVT_BUTTON(self, -1, OnButton)

    def onClose(self, evt):
        retCode = self.GetReturnCode()
        if retCode not in self.LABELS:
            return
        if self.timer:
            self.timer.Stop()
            del self.timer
        ix = 1 + self.action.RES_IDS.index(retCode) if retCode in self.action.RES_IDS else 1
        result = self.action.RESULTS[ix]
        self.alias = self.alias if self.alias else self.title
        if self.payload:
            eg.TriggerEvent("%s.%s" % (self.alias, result), self.payload, "MessageBox")
        else:
            eg.TriggerEvent("%s.%s" % (self.alias, result), prefix = "MessageBox")
        if self.event is not None:
            self.action.retCode = result
            SetEvent(self.event)
        self.Destroy()
#===============================================================================

class ShowMessageBox(eg.ActionBase):
    retCode = None
    RESULTS = (0, "OK", "CANCEL", "ABORT", "RETRY", "IGNORE", "YES", "NO")
    RES_IDS = (
        wx.ID_OK,
        wx.ID_CANCEL,
        wx.ID_ABORT,
        wx.ID_RETRY,
        wx.ID_IGNORE,
        wx.ID_YES,
        wx.ID_NO,
        )
    name = "Show Message Box"
    iconFile = "icons/Dialog"

    class text:
        main = "General settings:"
        buttons = "Buttons:"
        icon = "Icon:"
        options = "Advanced settings:"
        alias = "Alias:"
        payload = "Payload:"
        title = "Title:"
        body = "Message:"
        wait = "Wait for the Message Box to close"
        radioBoxButtons = [
            "OK",
            "OK, Cancel",
            "Retry, Cancel",
            "Abort, Retry, Ignore",
            "Yes, No",
            "Yes, No, Cancel"
        ]
        radioBoxIcon = [
            "No icon",
            "Information",
            "Question",
            "Warning",
            "Error"
        ]
        radioBoxOptions = [
            "Default",
            "Always on top",
            "No focus",
            "System modal"
        ]
        mbType = "Message Box type"
        mbTypes = (
            "System (Windows)",
            "Tweaked (EventGhost)"
        )
        autoClose0 = "Auto-close timer [s]:"
        autoClose1 = "(0 = feature disabled)"
        yes = "Yes"
        no = "No"
        cancel = "Cancel"
        ok = "OK"
        ignore = "Ignore"
        retry = "Retry"
        abort = "Abort"
        autoClose = "Auto close after %i s"
        aot = "Always on top"
        modal = "Modal"
        play = "Play a system sound"

        #MB_TOPMOST=262144, MB_ABORTRETRYIGNORE=2, MB_ICONERROR=16,
        #MB_ICONINFORMATION=64, MB_ICONQUESTION=32, MB_ICONWARNING=48, MB_NOFOCUS=32768, MB_OK=0,
        #MB_OKCANCEL=1, MB_RETRYCANCEL=5, MB_SYSTEMMODAL=4096, MB_YESNO=4, MB_YESNOCANCEL=3

    def getFlags(self, options, twk = True):
        if twk:
            optionid = (options - options % 4096)/4096
        else:
            optionid=0
            if options & MB_TOPMOST:
                optionid=1
            elif options & MB_NOFOCUS:
                optionid=2
            elif options & MB_SYSTEMMODAL:
                optionid=3
        iconid=0
        if options & MB_ICONINFORMATION:
            iconid=1
        elif options & MB_ICONWARNING == MB_ICONWARNING:
            iconid=3
        elif options & MB_ICONQUESTION:
            iconid=2
        elif options & MB_ICONERROR:
            iconid=4
        buttonid=0
        if options & MB_RETRYCANCEL == MB_RETRYCANCEL:
            buttonid=2
        elif options & MB_YESNOCANCEL == MB_YESNOCANCEL:
            buttonid=5
        elif options & MB_YESNO:
            buttonid=4
        elif options & MB_ABORTRETRYIGNORE:
            buttonid=3
        elif options & MB_OKCANCEL:
            buttonid=1
        return (optionid,iconid,buttonid)


    def showMessageBox(self,title,body,alias,payload,options):
            if not alias:
                alias=title
            result = MessageBox(0, body, title, options)

            if result > 0 and result < 8:
                result = self.RESULTS[result]
            else:
                result=str(result)
            if payload:
                eg.TriggerEvent("%s.%s" % (alias,result), payload, "MessageBox")
            else:
                eg.TriggerEvent("%s.%s" % (alias,result), prefix = "MessageBox")
            return result


    def showTweakedBox(self, parent, title, message, alias, payload, flags, time, event):
        optionid, iconid, buttonid = self.getFlags(flags)
        mssgbx = MessageBoxDialog(parent, title, message, alias, payload, flags, time, self, event)
        if optionid & 1:
            mssgbx.ShowModal()
        else:
            mssgbx.Show()


    def __call__(
        self,
        title = "",
        body = "",
        alias = "",
        payload = "",
        blocking = False,
        options = 0,
        mbType = 0,
        autoClose = 0
    ):
        title = eg.ParseString(title)
        body = eg.ParseString(body)
        alias = eg.ParseString(alias)
        payload = eg.ParseString(payload)
        if not isinstance(autoClose, int):
            try:
                autoClose = int(eg.ParseString(autoClose))
            except:
                autoClose = 0
        if mbType:
            event = CreateEvent(None, 0, 0, None) if blocking else None
            wx.CallAfter(self.showTweakedBox,None, title, body, alias, payload, options, autoClose, event)
            if blocking:
                #print "Waiting ..."
                eg.actionThread.WaitOnEvent(event, 999999999999)
                return self.retCode
        else:
            if blocking:
                return self.showMessageBox(title, body, alias, payload, options)
            else:
                Thread(
                    target = self.showMessageBox,
                    args = (title, body, alias, payload, options)
                ).start()
                return None


    def Configure(
        self,
        title = "",
        body = "",
        alias = "",
        payload = "",
        blocking = False,
        options = 0,
        mbType = 0,
        autoClose = 0
    ):
        ids = (wx.NewId(), wx.NewId(), wx.NewId())

        def getOptions(mbt):
            result = buttonsArr[buttonsCtrl.GetSelection()]
            result += iconArr[iconCtrl.GetSelection()]
            if not mbt:
                result += optionsArr[wx.FindWindowById(ids[0]).GetSelection()]
            else:
                tmp = wx.FindWindowById(ids[0]).GetValue()   + \
                    2 * wx.FindWindowById(ids[1]).GetValue() + \
                    4 * wx.FindWindowById(ids[2]).GetValue()
                result += 4096 * tmp
            return result

        buttonsArr = [0,MB_OKCANCEL,MB_RETRYCANCEL,MB_ABORTRETRYIGNORE,MB_YESNO,MB_YESNOCANCEL]
        iconArr = [0,MB_ICONINFORMATION,MB_ICONQUESTION,MB_ICONWARNING,MB_ICONERROR]
        optionsArr = [0,MB_TOPMOST,MB_NOFOCUS,MB_SYSTEMMODAL]
        optionid, iconid, buttonid = self.getFlags(options, mbType)
        panel = eg.ConfigPanel()
        text = self.text
        waitCtrl = wx.CheckBox(panel, -1, text.wait)
        waitCtrl.SetValue(blocking)
        aliasCtrl = panel.TextCtrl(alias)
        st1 = panel.StaticText(text.alias)
        titleCtrl = panel.TextCtrl(title)
        st2 = panel.StaticText(text.title)
        bodyCtrl = panel.TextCtrl(body, style = wx.TE_MULTILINE)
        st3 = panel.StaticText(text.body)
        payloadCtrl = panel.TextCtrl(payload)
        st4 = panel.StaticText(text.payload)
        statSizer = wx.FlexGridSizer(4, 2, 5, 5)
        statSizer.AddGrowableCol(1)
        statSizer.AddGrowableRow(1)
        statSizer.Add(st2, 0, ACV)
        statSizer.Add(titleCtrl,0,wx.EXPAND)
        statSizer.Add(st3, 0, ACV)
        statSizer.Add(bodyCtrl,1,wx.EXPAND)
        statSizer.Add(st1, 0, ACV)
        statSizer.Add(aliasCtrl,0,wx.EXPAND)
        statSizer.Add(st4, 0, ACV)
        statSizer.Add(payloadCtrl,0,wx.EXPAND)
        statBox = wx.StaticBox(panel, -1, self.text.main)
        box0 = wx.StaticBoxSizer(statBox, wx.HORIZONTAL)
        box0.Add(statSizer,1,wx.EXPAND)
        buttonsCtrl = wx.RadioBox(
            panel,
            label=text.buttons,
            choices=text.radioBoxButtons,
            style=wx.RA_SPECIFY_ROWS
        )
        buttonsCtrl.SetSelection(buttonid)
        iconCtrl = wx.RadioBox(
            panel,
            label=text.icon,
            choices=text.radioBoxIcon,
            style=wx.RA_SPECIFY_ROWS
        )
        iconCtrl.SetSelection(iconid)
        mbTypeCtrl = wx.RadioBox(
            panel,
            label=text.mbType,
            choices=text.mbTypes,
            style=wx.RA_SPECIFY_COLS
        )
        mbTypeCtrl.SetSelection(mbType)

        autoCloseLbl0 = wx.StaticText(panel, -1, text.autoClose0)
        autoCloseLbl1 = wx.StaticText(panel, -1, text.autoClose1)
        autoCloseCtrl = eg.SmartSpinIntCtrl(
                        panel,
                        -1,
                        autoClose,
                        min = 0,
                        max = 999
                    )
        autoCloseSizer = wx.BoxSizer(wx.HORIZONTAL)
        autoCloseSizer.Add(autoCloseLbl0, 0, ACV)
        autoCloseSizer.Add(autoCloseCtrl, 0, wx.LEFT|wx.RIGHT,5)
        autoCloseSizer.Add(autoCloseLbl1, 0, ACV)
        optionSizer = wx.BoxSizer(wx.HORIZONTAL)

        def onRadioBox(evt):
            val = evt.GetSelection() != 1
            waitCtrl.Enable(val)
            if not val:
                waitCtrl.SetValue(False)
            evt.Skip()

        def onCheckBox(evt):
            ctrl1 = wx.FindWindowById(ids[1])
            val = evt.IsChecked()
            ctrl1.Enable(not val)
            if val:
                ctrl1.SetValue(True)
            evt.Skip()

        def fillOptSizer(twk, init = False):
            val = optionid if init else (0, 7)[twk]
            autoCloseLbl0.Enable(twk)
            autoCloseLbl1.Enable(twk)
            autoCloseCtrl.Enable(twk)
            waitCtrl.Enable(twk)
            optionSizer.Clear(True)
            if twk:
                stBox = wx.StaticBox(panel, -1, text.options)
                box1 = wx.StaticBoxSizer(stBox, wx.VERTICAL)
                optionSizer.Add(box1,1,wx.EXPAND)
                ctrl0 = wx.CheckBox(panel, ids[0], text.modal)
                ctrl0.SetValue(val & 1)
                wx.EVT_CHECKBOX(ctrl0, ids[0], onCheckBox)
                ctrl1 = wx.CheckBox(panel, ids[1], text.aot)
                ctrl1.SetValue(val & 2)
                ctrl2 = wx.CheckBox(panel, ids[2], text.play)
                ctrl2.SetValue(val & 4)
                box1.Add(ctrl0, 0, wx.TOP, 5)
                box1.Add(ctrl1, 0, wx.TOP, 5)
                box1.Add(ctrl2, 0, wx.TOP, 5)
                if ctrl0.GetValue():
                    ctrl1.Enable(False)
                    ctrl1.SetValue(True)
                else:
                    ctrl1.Enable(True)
            else:
                autoCloseCtrl.SetValue(0)
                optionCtrl = wx.RadioBox(
                    panel,
                    ids[0],
                    label=text.options,
                    choices=text.radioBoxOptions,
                    style=wx.RA_SPECIFY_ROWS
                )
                wx.EVT_RADIOBOX(optionCtrl, ids[0], onRadioBox)
                optionCtrl.SetSelection(val)
                if val == 1:
                    waitCtrl.Enable(False)
                    waitCtrl.SetValue(False)
                else:
                    waitCtrl.Enable(True)
                optionSizer.Add(optionCtrl,0,wx.EXPAND)
            panel.sizer.Layout()
        fillOptSizer(mbType, True)

        def onMbType(event):
            wx.CallAfter(fillOptSizer, bool(event.GetSelection()))
            event.Skip()
        mbTypeCtrl.Bind(wx.EVT_RADIOBOX, onMbType)

        mainSizer = wx.FlexGridSizer(2, 2, 5, 5)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add(box0,0,wx.EXPAND)
        mainSizer.Add(optionSizer,0,wx.EXPAND)
        mainSizer.Add(buttonsCtrl,0,wx.EXPAND)
        mainSizer.Add(iconCtrl,0,wx.EXPAND)
        panel.sizer.Add(mbTypeCtrl,0,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.EXPAND|wx.TOP,5)
        panel.sizer.Add(waitCtrl,0,wx.TOP,5)
        panel.sizer.Add(autoCloseSizer,0,wx.TOP,5)
        while panel.Affirmed():
            mbt = mbTypeCtrl.GetSelection()
            panel.SetResult(
                titleCtrl.GetValue(),
                bodyCtrl.GetValue(),
                aliasCtrl.GetValue(),
                payloadCtrl.GetValue(),
                waitCtrl.GetValue(),
                getOptions(mbt),
                mbt,
                autoCloseCtrl.GetValue(),
            )


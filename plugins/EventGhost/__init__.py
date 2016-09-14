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

import time
import wx
from threading import Event
from win32gui import FindWindow

# Local imports
import eg
from eg import FolderItem, MacroItem
from eg.WinApi.Utils import BringHwndToFront
from eg.WinApi.Dynamic import GetForegroundWindow
from JumpIfElse import JumpIfElse
from NewJumpIf import NewJumpIf
from PythonScript import PythonScript
from ShowMessageBox import ShowMessageBox
from ShowOSD import ShowOSD

eg.RegisterPlugin(
    name = "EventGhost",
    author = "Bitmonster",
    description = (
        "Actions to control events, macro flow, and the configuration tree."
    ),
    kind = "core",
    version = "1.0.7",
    guid = "{9D499A2C-72B6-40B0-8C8C-995831B10BB4}",
)

class EventGhost(eg.PluginBase):
    def __init__(self):
        self.AddAction(PythonCommand)
        self.AddAction(PythonScript)
        self.AddAction(AutoRepeat)
        self.AddAction(FlushEvents)
        self.AddAction(Comment)
        self.AddAction(DisableItem)
        self.AddAction(DumpResult)
        self.AddAction(EnableItem)
        self.AddAction(EnableExclusive)
        self.AddAction(GetItemState)
        self.AddAction(NewJumpIf)
        self.AddAction(JumpIfElse)
        self.AddAction(JumpIfDoubleEvent)
        self.AddAction(JumpIfLongPress)
        self.AddAction(OpenConfig)
        self.AddAction(OpenEventGhost)
        self.AddAction(ShowMessageBox)
        self.AddAction(ShowOSD)
        self.AddAction(StopProcessing)
        self.AddAction(TriggerEvent)
        self.AddAction(Wait)


class EnableItem(eg.ActionBase):
    name = "Enable Item"
    description = "Enables an item in the tree."
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

    def FilterFunc(self, dummyObj):
        return True

    def GetLabel(self, link):
        obj = link.target
        if obj:
            return self.text.label % obj.GetLabel()
        return self.text.label % ''

    def IsSelectableItem(self, item):
        return item.isDeactivatable


class AutoRepeat(eg.ActionBase):
    name = "Auto-Repeat Macro"
    description = "Makes the current macro auto-repeat."
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
                (startDelay - endDelay) *
                (sweepTime - (elapsed + firstDelay)) /
                sweepTime
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


class Comment(eg.ActionBase):
    name = "Comment"
    description = (
        "Does nothing at all. Useful for commenting your configuration."
    )
    iconFile = 'icons/Comment'

    def __call__(self):
        pass


class DisableItem(EnableItem):
    name = "Disable Item"
    description = "Disables an item in the tree."
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


class DumpResult(eg.ActionBase):
    name = "Dump Result to Log"
    description = (
        "Outputs the most recent `eg.result` to your EventGhost log. Useful "
        "for debugging."
    )

    def __call__(self):
        result = eg.result
        print str(result)
        return result


class EnableExclusive(EnableItem):
    name = "Enable Item Exclusively"
    description = (
        "Enables a specified folder or macro in your configuration, but "
        "also disables all other folders and macros that are siblings on "
        "the same level in that branch of the tree."
    )
    iconFile = "icons/EnableExclusive"

    class text:
        label = "Enable Exclusively: %s"
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


class FlushEvents(eg.ActionBase):
    name = "Clear Pending Events"
    description = """<rst>
        Clears all unprocessed events that are currently in the processing
        queue.

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


class GetItemState(EnableItem):
    name = "Get Item State"
    description = "Gets an item's enable state (True when enabled)."
    iconFile = 'icons/DisableItem'

    class text:
        label = "Get State: %s"
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


class JumpIfDoubleEvent(eg.ActionBase):
    name = "Jump If Duplicate Event"
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
            (intervalCtrl, 0, wx.LEFT | wx.RIGHT, 5),
            (panel.StaticText(text.text2), 0, wx.ALIGN_CENTER_VERTICAL),
        )
        mySizer = wx.FlexGridSizer(2, 3, 5, 5)
        mySizer.AddGrowableCol(1, 1)
        mySizer.Add(panel.StaticText(text.text3), 0, wx.ALIGN_CENTER_VERTICAL)
        mySizer.Add(macroCtrl, 1, wx.EXPAND)

        panel.sizer.AddMany(((sizer1), (mySizer, 1, wx.EXPAND | wx.TOP, 5)))
        while panel.Affirmed():
            panel.SetResult(intervalCtrl.GetValue(), macroCtrl.GetValue())

    def GetLabel(self, interval, link):
        return self.text.label % (link.target.name)


class JumpIfLongPress(eg.ActionBase):
    name = "Jump If Long Press"
    description = (
        "Jumps to another macro, if the button on the remote is held down "
        "longer than the configured time."
    )
    iconFile = "icons/LongPress"

    class text:
        label = "If button held for %s sec(s), go to: %s"
        text1 = "If button held for longer than"
        text2 = "seconds,"
        text3 = "jump to:"
        text4 = "Select the long press macro..."
        text5 = (
            "Please select the macro, which should be triggered "
            "if the event is a long event."
        )

    def __call__(self, interval, link):
        eg.event.shouldEnd.wait(interval)
        if not eg.event.shouldEnd.isSet():
            nextItem = link.target
            nextIndex = nextItem.parent.GetChildIndex(nextItem)
            eg.programCounter = (nextItem, nextIndex)

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
            (intervalCtrl, 0, wx.LEFT | wx.RIGHT, 5),
            (panel.StaticText(text.text2), 0, wx.ALIGN_CENTER_VERTICAL),
        )
        mySizer = wx.FlexGridSizer(2, 3, 5, 5)
        mySizer.AddGrowableCol(1, 1)
        mySizer.Add(panel.StaticText(text.text3), 0, wx.ALIGN_CENTER_VERTICAL)
        mySizer.Add(macroCtrl, 1, wx.EXPAND)

        panel.sizer.AddMany(((sizer1), (mySizer, 1, wx.EXPAND | wx.TOP, 5)))
        while panel.Affirmed():
            panel.SetResult(intervalCtrl.GetValue(), macroCtrl.GetValue())

    def GetLabel(self, interval, link):
        return self.text.label % (interval, link.target.name)


class OpenConfig(eg.ActionBase):
    name = "Open Configuration"
    description = "Opens the specified configuration dialog."
    iconFile = "icons/Dialog"

    class text:
        text0 = "Action or plugin: "
        text1 = "Select action or plugin..."
        text2 = (
            "Please select the action or plugin, whose configuration dialogue "
            "should be opened."
        )

    def __call__(self, link):
        wx.CallAfter(eg.document.OnCmdConfigure, link.target)
        wx.CallAfter(
            self.BringDialogToFront,
            eg.text.General.settingsActionCaption
        )

    @staticmethod
    def BringDialogToFront(name):
        hwnd = 0
        i = 0
        while hwnd == 0 and i < 10000:
            hwnd = FindWindow("#32770", name)
            i += 1
        if hwnd:
            BringHwndToFront(hwnd)

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
        panel.sizer.Add(mySizer, 1, wx.EXPAND | wx.ALL, 5)

        while panel.Affirmed():
            panel.SetResult(actionCtrl.GetValue())

    def GetLabel(self, link):
        label = link.target.GetLabel() if link else ""
        return "%s: %s" % (self.name, label)


class OpenEventGhost(eg.ActionBase):
    class text:
        name = "Open EventGhost"
        description = (
            "Opens, closes, or toggles EventGhost's main window. "
            "Particularly helpful when system tray icon is hidden."
        )
        label = (
            "Open EventGhost",
            "Close EventGhost",
            "Toggle EventGhost",
        )

    def __call__(self, action = 0):
        if action == 0:
            show = True
        elif action == 1:
            show = False
        elif action == 2:
            if eg.document.frame:
                if eg.document.frame.GetHandle() == GetForegroundWindow():
                    show = False
                else:
                    show = True
            else:
                show = True
        else:
            return False
        func = (eg.document.ShowFrame if show else eg.document.HideFrame)
        wx.CallAfter(func)

    def Configure(self, action = 0):
        panel = eg.ConfigPanel()
        choice = panel.RadioBox(action, self.text.label)
        panel.sizer.Add(choice, 0, wx.ALL, 10)
        while panel.Affirmed():
            panel.SetResult(choice.GetValue())

    def GetLabel(self, action = 0):
        return self.text.label[action]


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


class StopProcessing(eg.ActionBase):
    name = "Stop Processing Event"
    description = (
        "Stops EventGhost from searching for further macros matching the "
        "current event."
    )
    iconFile = 'icons/StopProcessing'

    def __call__(self):
        eg.event.skipEvent = True


class TriggerEvent(eg.ActionBase):
    name = "Trigger Event"
    description = (
        "Triggers an event with an optional delay."
    )
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

    def GetLabel(self, eventString="", waitTime=0):
        if waitTime:
            return self.text.labelWithTime % (eventString, waitTime)
        else:
            return self.text.labelWithoutTime % eventString


class Wait(eg.ActionBase):
    name = "Wait"
    description = "Pauses execution for the specified number of seconds."
    iconFile = "icons/Wait"

    class text:
        label = "Wait: %s sec(s)"
        wait = "Wait"
        seconds = "seconds"

    def __call__(self, waitTime):
        eg.actionThread.Wait(waitTime)

    def Configure(self, waitTime=0.0):
        panel = eg.ConfigPanel()
        waitTimeCtrl = panel.SpinNumCtrl(waitTime, integerWidth=3)
        panel.AddLine(self.text.wait, waitTimeCtrl, self.text.seconds)
        while panel.Affirmed():
            panel.SetResult(waitTimeCtrl.GetValue())

    def GetLabel(self, waitTime=0):
        return self.text.label % str(waitTime)

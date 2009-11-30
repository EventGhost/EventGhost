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

eg.RegisterPlugin(
    name = "EventGhost",
    author = "Bitmonster",
    description = (
        "Here you find actions that mainly control the core functionality of"
        "EventGhost."
    ),
    kind = "core",
    version = "1.0.0",
    guid = "{9D499A2C-72B6-40B0-8C8C-995831B10BB4}",
)

import wx
import sys
import time
import traceback
from threading import Event
from eg import ContainerItem, FolderItem, MacroItem, RootItem, AutostartItem

from PythonScript import PythonScript
from ShowOSD import ShowOSD
from NewJumpIf import NewJumpIf


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
        self.AddAction(EnableExclusive)
        self.AddAction(Wait)
        self.AddAction(StopProcessing)
        self.AddAction(NewJumpIf)
        self.AddAction(JumpIfLongPress)
        self.AddAction(JumpIfDoubleEvent)
        self.AddAction(AutoRepeat)
        self.AddAction(TriggerEvent)
        self.AddAction(FlushEvents)
        self.AddAction(ShowOSD)



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
                node.isEnabled = True
                node.Refresh()
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
        link = eg.TreeLink(eg.currentConfigureItem)

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
                node.isEnabled = False
                node.Refresh()



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
            node.isEnabled = True
            node.Refresh()
            for child in node.parent.childs:
                if child is not node and child.isDeactivatable:
                    child.isEnabled = False
                    child.Refresh()
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
            eg.scheduler.AddTask(waitTime, eg.TriggerEvent, eventString)


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


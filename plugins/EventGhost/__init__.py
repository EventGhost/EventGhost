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
                obj = tree.GetItemData(treeItem)
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


DESCRIPTION = """<md>Triggers an event with options.  

* ***Event String***
  ______
  Events are separated by "."'s, the purpose for this is to group them
together. As an example if you wanted to group events together by a
device type this can be done by using the following example.

        Remote.StopButton  

  So you would be able to group all of the various buttons to a remote.
Plugins use this same grouping mechanism for generating events. You also
have the ability to go one step further and group a group.

        Remote.Volume.Up  
        Remote.Volume.Down  
        Remote.Volume.Mute

  The purpose for this is when you add an event to an action you can
target specific groups by using the * so if you wanted to target all of
the events that take place for Remote.Volume you would add an event to
the macro like this.  

        Remote.Volume.*  

  This will run that macro for any event that begins with Remote.Volume.

  All events have to have at the very least a group and an item. So if
you do not specify a group and only an item the group of Main will be
added automatically. So if you specify an event of VolumeUp the actual
event that will be triggered will be.

        Main.VolumeUp
        
There is also a check box to enable or disable the Main prefix. 
You will only be able to disable the Main if there is more then single group

  You also have the ability to set the event string using a python 
expression (see below).
<br><br>
* ***Wait Time***
  ______

  The amount of time to wait before triggering the event. this has a
resolution of hundredths of a second.
<br><br>
* ***Event Payload***
  ______

  When an event occurs you are able to attach a data packet to the
event. This data packet can be any kind of a python object.

  Most common ones are:
  * integers 3
  * floats 0.00
  * lists []
  * tuples ()
  * dictionaries {}
  * unicode strings u''
  * and strings ""

  When there is an attached payload you will see the payload in the log.
  
  You also have the ability just like the Event String to attach a
python expression (see below).
<br><br>
* ***Add to Queue***
  ______
  If the wait time is set to 0.00 this option will appear. Adding the
event to the queue means that the event will get triggered after the
event that caused this action has processed all of it's macros and also
after processing any events that have come in while the event that
triggered this action was running.

  If unchecked the event will get triggered right away Not being added 
to the queue and not waiting until the event that started this action 
has finished processing.
<br><br>
* ***Restore eg.event***
  ______
  If add to queue has not been checked this option will appear. This
relates more to the scripting portions of EventGhost. What this done is
each and every time an event gets triggered there are 2 variables that
get set into place. Those 2 variables are eg.event and eg.eventString.
When you trigger an event while the current event is running those 2
variables will get changed to the new event. Upon completion of the new
event if you would like to change those variables back to the event that
ran this action then check this box.
<br><br>
* ***Using a Python Expression***
  ______
  You can use a python expression in several ways. The expression 
**MUST** be wrapped in curly braces {}. This is the identifier that
tells EventGhost that it needs to do some work.

  You can pass global variables which are stored in eg.globals by
wrapping the variable name in the curly braces.

        {eg.globals.some_variable}

  If you want to transfer the results of another action you can do this
as well.

        {eg.plugins.SomePlugin.SomeAction()}
  
  ***Or maybe you want to do something a little more complex.***
  
  A different value passed based on if a global is True or False.

        {"TV.On" if eg.globals.tv_power else "TV.Off"}

  Or checking a global for a specific value and passing True or False.

        {eg.plugins.SomePlugin.SomeAction() == 100}

  When using a python expression in a payload the curly braces are the
same thing that is used in a dictionary but our crafty programmers have
accounted for this so don't worry.

  These expressions get run when the TriggerAction gets run. So if you
have a programmed wait time (see below) the data may be different at the
start of the wait time then at the end.
  
"""
class TriggerEvent(eg.ActionBase):
    __doc__ = DESCRIPTION
    name = "Trigger Event"
    description = DESCRIPTION
    iconFile = "icons/Plugin"

    class text:
        text1 = "Event string to fire:"
        text2 = "Delay the firing of the event:"
        text3 = "seconds. (0 = fire immediately)"
        text4 = "Add event to event queue:"
        text5 = "Return eg.event to original event:"
        text6 = "Event Payload:"
        text7 = 'Remove "Main" prefix:'

    def __call__(
        self,
        eventString,
        waitTime=0,
        payload=None,
        queueEvent=True,
        restoreEvent=False,
        removeMain=False
    ):

        def parse(value):
            if value is None:
                return None
            parsed_value = eg.ParseString(value)
            if value == parsed_value:
                try:
                    value = eval(value)
                except (SyntaxError, NameError):
                    pass
            else:
                value = parsed_value
            return value

        eventString = parse(eventString)
        payload = parse(payload)

        split_event = eventString.split('.', 1)
        if len(split_event) == 1:
            split_event.insert(0, 'Main')

        if not removeMain and split_event[0] != 'Main':
            split_event.insert(0, 'Main')
            split_event = [split_event[0], '.'.join(split_event[1:])]

        kwargs = dict(
            prefix=split_event[0],
            suffix=split_event[1],
            payload=payload
        )

        if not waitTime:
            if queueEvent:
                eg.TriggerEvent(**kwargs)
            else:
                event = eg.EventGhostEvent(**kwargs)
                if restoreEvent:
                    old_event_string = eg.eventString
                    old_event = eg.event
                    event.Execute()
                    eg.event = old_event
                    eg.eventString = old_event_string
                else:
                    event.Execute()
        else:
            eg.scheduler.AddShortTask(waitTime, eg.TriggerEvent, **kwargs)

    def Configure(
        self,
        eventString="",
        waitTime=0,
        payload=None,
        queueEvent=False,
        restoreEvent=False,
        removeMain=False
    ):
        panel = eg.ConfigPanel()
        text = self.text

        if payload is None:
            payload = ''

        eventStringCtrl = panel.TextCtrl(eventString)
        waitTimeCtrl = panel.SpinNumCtrl(waitTime, integerWidth=5)
        payloadCtrl = panel.TextCtrl(payload)
        queueEventCtrl = wx.CheckBox(panel, -1, '')
        restoreEventCtrl = wx.CheckBox(panel, -1, '')
        removeMainCtrl = wx.CheckBox(panel, -1, '')

        queueEventCtrl.SetValue(queueEvent)
        restoreEventCtrl.SetValue(restoreEvent)
        removeMainCtrl.SetValue(removeMain)
        queueEventCtrl.Enable(not waitTime)
        restoreEventCtrl.Enable(not waitTime and not queueEvent)
        removeMainCtrl.Enable('.' in eventString)

        if not eventString:
            removeMainCtrl.Disable()

        def on_char(evt):
            if '.' in eventStringCtrl.GetValue():
                removeMainCtrl.Enable()
            else:
                removeMainCtrl.Disable()

            evt.Skip()

        eventStringCtrl.Bind(wx.EVT_TEXT, on_char)

        def on_spin(evt):
            def check_spin():
                value = bool(waitTimeCtrl.GetValue())
                queueEventCtrl.Enable(not value)
                restoreEventCtrl.Enable(
                    not value or (not value and not queueEventCtrl.GetValue())
                )
            wx.CallLater(20, check_spin)
            evt.Skip()

        def on_check(evt):
            restoreEventCtrl.Enable(not queueEventCtrl.GetValue())
            evt.Skip()

        def HBoxSizer(lbl, ctrl, suf=None, prop=0):
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            style = wx.EXPAND | wx.ALL | wx.ALIGN_BOTTOM

            lbl = panel.StaticText(lbl)
            lbl_sizer = wx.BoxSizer(wx.VERTICAL)
            lbl_sizer.AddStretchSpacer(prop=1)
            lbl_sizer.Add(lbl)

            sizer.Add(lbl_sizer, 0, style, 5)
            sizer.Add(ctrl, prop, style, 5)

            if suf is not None:
                suf = panel.StaticText(suf)
                suf_sizer = wx.BoxSizer(wx.VERTICAL)
                suf_sizer.AddStretchSpacer(prop=1)
                suf_sizer.Add(suf)
                sizer.Add(suf_sizer, 0, style, 5)
            panel.sizer.Add(sizer, 0, wx.EXPAND)

            return lbl

        waitTimeCtrl.Bind(wx.EVT_SPIN, on_spin)
        waitTimeCtrl.Bind(wx.EVT_CHAR_HOOK, on_spin)
        queueEventCtrl.Bind(wx.EVT_CHECKBOX, on_check)

        eg.EqualizeWidths((
            HBoxSizer(text.text1, eventStringCtrl, prop=1),
            HBoxSizer(text.text7, removeMainCtrl),
            HBoxSizer(text.text6, payloadCtrl, prop=1),
            HBoxSizer(text.text2, waitTimeCtrl, suf=text.text3),
            HBoxSizer(text.text4, queueEventCtrl),
            HBoxSizer(text.text5, restoreEventCtrl),

        ))

        while panel.Affirmed():
            panel.SetResult(
                eventStringCtrl.GetValue(),
                waitTimeCtrl.GetValue(),
                payloadCtrl.GetValue() if payloadCtrl.GetValue() else None,
                queueEventCtrl.IsEnabled() and queueEventCtrl.GetValue(),
                restoreEventCtrl.IsEnabled() and restoreEventCtrl.GetValue(),
                removeMainCtrl.IsEnabled() and removeMainCtrl.GetValue(),
            )

    def GetLabel(
        self,
        eventString="",
        waitTime=0,
        payload=None,
        queueEvent=False,
        restoreEvent=False
    ):

        label = (
            '%s: Event: %s, Payload: %s, Wait: ' %
            (self.name, eventString, payload)
        )

        if waitTime:
            label += '%.2f seconds' % waitTime
        elif queueEvent:
            label += 'Queued'
        else:
            label += 'Immediate, Restore eg.event: %s' % restoreEvent
        return label


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

# -*- coding: utf-8 -*-

# Contains LGPL code of PyHooked: https://github.com/ethanhs/pyhooked

import eg

eg.RegisterPlugin(
    name = "WindowWatcher",
    author = "David Perry <d.perry@utoronto.ca>",
    version = "0.0.1",
    kind = "other",
    description = "Detect when the active window changes. Also detect new windows.",
    url = "https://github.com/Boolean263/EventGhost-WindowWatcher",
    guid = "{051a79aa-80f7-4150-bead-538537d17dd5}",
)

import wx
import win32gui
from eg.WinApi.Utils import GetWindowProcessName
from eg.WinApi import GetWindowText, GetClassName

from threading import Event, Thread

class PrettyBunch(eg.Utils.Bunch):
    """
    Tweak to EG's Bunch object to make it print pretty
    when it's used as an event payload.
    I may eventually propose this as an improvement to EG core.
    """
    def __str__(self):
        """
        EG doesn't use this when it shows the event payload.
        Perhaps it should?
        """
        return self.__dict__.__str__()
    def __repr__(self):
        """
        EG uses this to show the event's payload.
        This is where I make the object pretty, but it technically breaks
        the Python rule of the representation being valid Python code that
        you can re-evaluate to get the object back.
        """
        return ", ".join(k+"="+repr(v) for k, v in self.__dict__.items())

class WindowWatcher(eg.PluginBase):
    """
    Watches for changes in the active window, by periodically seeing which
    one is active. Also detects newly opened/closed windows by keeping a list
    of what windows are open.
    """

    # Internal state
    stopThreadEvent = None
    lastWindow = None
    allWindows = set()

    # Configurable options
    showFocus = True
    showBlur = False
    showOpen = False
    showClose = False
    setAsFound = False
    interval = 1.0

    # showClose has been removed from the configurable options for now,
    # because we (obviously) can't get window properties from a window
    # that is no longer there. A future version may allow this by tracking
    # the properties of windows it sees open, so it can provide those to
    # Close events.

    def Configure(self, interval=1.0, setAsFound=False, showFocus=True, showBlur=False, showOpen=False):
        """Display the configuration dialog for this plugin."""

        panel = eg.ConfigPanel()
        pollCtrl = panel.SpinNumCtrl(interval, min=0.1, max=60)
        foundCtrl = panel.CheckBox(setAsFound, "Set target window as Found")
        focusCtrl = panel.CheckBox(showFocus, "On Window Activate")
        blurCtrl = panel.CheckBox(showBlur, "On Window Deactivate")
        openCtrl = panel.CheckBox(showOpen, "On Window Open")
        #closeCtrl = panel.CheckBox(showClose, "On Window Close")

        sizer = wx.GridBagSizer(5, 5)
        expand = wx.EXPAND
        sizer.AddMany([
            (panel.StaticText("Poll for changes:"), (0, 0), (1, 1)),
            (pollCtrl, (0, 1), (1, 1)),
            (panel.StaticText("seconds"), (0, 2), (1, 1)),
            (panel.StaticText("Trigger Events:"), (1, 0), (1, 2)),
            (focusCtrl, (2, 1), (1, 1)),
            (blurCtrl, (3, 1), (1, 1)),
            (openCtrl, (4, 1), (1, 1)),
            #(closeCtrl, (5, 1), (1, 1)),
            (panel.StaticText(""), (6, 0), (1, 2)),
            (foundCtrl, (7, 0), (1, 2)),
            (panel.StaticText("This option makes the target window the subject of\nfuture Window actions in your macro."), (8, 1), (1, 2)),
        ])
        panel.sizer.Add(sizer, 1, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                pollCtrl.GetValue() or 1.0,
                foundCtrl.GetValue(),
                focusCtrl.GetValue(),
                blurCtrl.GetValue(),
                openCtrl.GetValue(),
                #closeCtrl.GetValue(),
            )

    def __init__(self):
        #print "WindowWatcher inited"
        pass

    def __start__(self, interval=1.0, setAsFound=False, showFocus=True, showBlur=False, showOpen=False):
        self.interval = interval
        self.setAsFound = setAsFound
        self.showFocus = showFocus
        self.showBlur = showBlur
        self.showOpen = showOpen
        #self.showClose = showClose

        if self.showOpen or self.showClose:
            self.allWindows = self.GetAllWindows()
        self.stopThreadEvent = Event()
        thread = Thread(
                target = self.ThreadLoop,
                args = (self.stopThreadEvent, )
        )
        thread.start()

    def __stop__(self):
        self.stopThreadEvent.set()

    def __close__(self):
        #print "WindowWatcher closed"
        pass

    def GetAllWindows(self):
        """Get a list of all currently open windows. Return it as a set."""
        s = set()
        def cb(hwnd, args):
            s.add(hwnd)
            return True

        win32gui.EnumWindows(cb, None)
        return s


    def WindowEvent(self, eventType, window_id):
        """Trigger an EventGhost event for the given window ID."""
        if not window_id:
            return

        payload = PrettyBunch(
            id=window_id,
            process=GetWindowProcessName(window_id).upper(),
            title=GetWindowText(window_id),
            window_class=GetClassName(window_id),
            is_visible=win32gui.IsWindowVisible(window_id),
            is_enabled=win32gui.IsWindowEnabled(window_id),
        )

        self.TriggerEvent("{}.{}".format(eventType, payload.process),
            payload=payload)

        if self.setAsFound:
            eg.lastFoundWindows[:] = [window_id]

    def ThreadLoop(self, stopThreadEvent):
        """Main thread loop. Polls current and open windows every interval."""

        while not stopThreadEvent.isSet():
            if self.showFocus or self.showBlur:
                # Figure out if the current window has changed
                thisWindow = win32gui.GetForegroundWindow()
                if thisWindow != self.lastWindow:
                    if self.showBlur:
                        self.WindowEvent("Deactivate", self.lastWindow)
                    if self.showFocus:
                        self.WindowEvent("Activate", thisWindow)
                    self.lastWindow = thisWindow

            if self.showOpen or self.showClose:
                # Figure out if windows have been opened or closed
                wins = self.GetAllWindows()

                if self.showOpen:
                    for w in wins - self.allWindows:
                        self.WindowEvent("Open", w)
                if self.showClose:
                    for w in self.allWindows - wins:
                        self.WindowEvent("Close", w)

                self.allWindows = wins

            # Sleep
            stopThreadEvent.wait(self.interval)
        #print("Stopped")


#
# Editor modelines  -  https://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# coding: utf-8
# End:
#
# vi: set shiftwidth=4 tabstop=4 expandtab fileencoding=utf-8:
# :indentSize=4:tabSize=4:noTabs=true:coding=utf-8:
#

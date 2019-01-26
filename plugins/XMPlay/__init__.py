# -*- coding: utf-8 -*-
#

import eg

eg.RegisterPlugin(
    name="XMPlay",
    author="obermann",
    version="1.0.1",
    kind="program",
    guid="{E7DB64B9-6C0D-4F38-A4CA-9FE2868AEA49}",
    description=(
        "Adds actions to control the XMPlay audio player."
        "As of XMPlay 3.8.3 this plugin should consistently control singular"
        "of the multiple running XMPlay instances (usually the first one)."
        "This plugin version is a compatible rework of the original by Pako."
    ),
    createMacrosOnAdd=True,
    url="https://github.com/obermann/XMPlay",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABQElEQVR4nGNgQAXRM88x"
        "4AWMDAwMySW9h3asuH3lNLKGpelGDAwMMkqaNm6hEBFuHv65PcWM+M1emm4ko6Spa+rA"
        "LyjKwMCwYkYTE0QpLpdEzzz35N51BgaGj+9fQ52UXNL77PEdBgYGKVkVBgYGOBvC2L5y"
        "Olyzqo7p7SunGTzDM////////3+IKISNLJhc0ouiBpmPqRPCRWYz/VB1lJJVYWSE+h7O"
        "QGN7RWQxMDB4hmcycdze/+zxHWSD0fwNEUH2DMLdcDZcHcS1cGWe4ZlMEKsZGRmlZFWS"
        "S3ohbIgbkkt64a5NLun1isiSklVhZGBgiMioO7JrNSS8ccUgHDBBKF1TB4iT8Ktemm4E"
        "1QCJeRklTUgSwqoUIsXCwMDAzcP/9ctHfkFRXVMHBliyQ0uFqjqmxjaeK2Y04bEfu38A"
        "SgS6R4+k12sAAAAASUVORK5CYII="
    ),
)

from os import path
from subprocess import Popen
from time import sleep
import threading
import _winreg
from dde_client_eg import (
    DDEClient, DDEError,
    XTYP_REGISTER,
    XTYP_UNREGISTER,
    XTYP_DISCONNECT,
    XTYP_ERROR,
    ST_CONNECTED,
)
from memory_reader import MemoryReader
from actions_xmp_open import *
import actions_xmp_winamp
import actions_xmp_dde
import actions_xmp_catalog

NOTHING = object()


class Run(eg.ActionBase):

    def __call__(self):
        if self.plugin.is_xmp_off(thorough=True, log=False):
            # best way to initiate is on DDE server registration callback
            if self.plugin.dde_client is None:
                self.plugin.dde_start()
            Popen(self.plugin.xmp_exe_path + "\\xmplay.exe")


class GetTitle(eg.ActionBase):

    def __call__(self):
        if self.plugin.is_xmp_off(): return
        return eg.WinApi.GetWindowText(self.plugin.xmp_window)


class ObservationThread(threading.Thread):

    def __init__(self, plugin):
        # initiate with plugin is a hack, being careful
        self.plugin = plugin
        self.oldData = ""
        self.threadFlag = threading.Event()
        super(ObservationThread, self).__init__(
            name=self.plugin.suffix.encode("unicode_escape") + "_Thread")

    def run(self):
        while not self.threadFlag.isSet():
            data = eg.WinApi.GetWindowText(self.plugin.xmp_window)
            if data and data != self.oldData and data != "XMPlay":
                self.oldData = data
                self.plugin.TriggerEvent(self.plugin.suffix, payload=data)
            self.threadFlag.wait(self.plugin.period)

    def terminate(self):
        """Stop the thread and wait for it to end."""
        if self.isAlive():
            self.threadFlag.set()
            super(ObservationThread, self).join()
            self.plugin = None


class Text:
    error1 = "Cannot connect to XMPlay."
    error2 = "XMPlay is not running."
    label1 = "XMPlay Installation Folder:"
    toolTipFolder = "Press button and browse to select folder..."
    browseTitle = "Selected folder:"
    events = "Trigger events with suffix"
    label2 = "when changing tracks"
    intervalLabel = "Refresh Period of Titlebar Reading:"
    suffix = "Track_Changed"
    from_eg_result = "Use EventGhost Result"


class XMPlay(eg.PluginBase):
    text = Text

    def __init__(self):

        self.AddActionsFromList((
            (Run, "Run", "Run", "Run XMPlay if it is not running already.", None),
            (actions_xmp_dde.Execute, "Close", "Close", "Close XMPlay. Command No. 10", 10),
            (actions_xmp_dde.Execute, "ClosePositionSaved", "Close with Position Saved",
             "Close with position saved. Command No. 11", 11),
            (actions_xmp_dde.ExecuteEx, "PlayPause", "Toggle Play", "Toggle Play/Pause. Command No. 80", 80),
            (actions_xmp_dde.Execute, "Stop", "Stop", "Stop playing current track. Command No. 81", 81),
            (actions_xmp_dde.Execute, "FastForward", "Fast Forward", "Skip forward. Command No. 82", 82),
            (actions_xmp_dde.Execute, "FastRewind", "Fast Rewind", "Skip back. Command No. 83", 83),
            (actions_xmp_dde.Execute, "Replay", "Replay", "Play current track again. Command No. 84", 84),
            (actions_xmp_dde.Execute, "Repeat", "Repeat", "Toggle looping. Command No. 9", 9),
            (
            actions_xmp_dde.Execute, "NextTrack", "Next Track", "Jump forward to the next track. Command No. 128", 128),
            (actions_xmp_dde.Execute, "PreviousTrack", "Previous Track",
             "Jump forward to the previous track. Command No. 129", 129),
            (
            actions_xmp_dde.Execute, "RandomTrack", "Random Track", "Jump forward to the random track. Command No. 130",
            130),
            (actions_xmp_dde.Execute, "Shuffle", "Shuffle", "Toggle random play order. Command No. 313", 313),
            (actions_xmp_dde.Execute, "BookmarkSet", "Bookmark Set", "Set the bookmark. Command No. 640", 640),
            (actions_xmp_dde.Execute, "BookmarkResume", "Bookmark Resume", "Resume from the bookmark. Command No. 130",
             130),
            (actions_xmp_dde.Execute, "VolumeUp", "Volume Up", "Volume up. Command No. 512", 512),
            (actions_xmp_dde.Execute, "VolumeDown", "Volume Down", "Volume down. Command No. 513", 513),
        ))

        scripting = self.AddGroup(
            "Scripting",
            "Scripting actions to interrogate XMPlay."
        )
        scripting.AddActionsFromList(actions_xmp_dde.actions)
        scripting.AddAction(GetTitle, "GetTitle", "Get Title",
                            "Get the title of currently playing track from the XMPlay main window title. "
                            "It is somewhat faster analog of \"Store General Info\" + \"Select from General\".")
        scripting.AddAction(Add, "Add", "Add",
                            "Add file, folder or URL to the playlist. "
                            "XMPlay will treat files coming in quickly after each other as a single batch, so it can auto-sort them.")
        scripting.AddAction(Open, "Open", "Open",
                            "Open file, folder or URL. "
                            "XMPlay will treat files coming in quickly after each other as a single batch, so it can auto-sort them.")
        scripting.AddAction(OpenFileFolder, "Open_file_folder",
                            "Open/Add file(s) or folder", "Open or add file(s), playlist(s) or folder(s)")
        # As of XMPlay 3.8.3 URLs are openned in the same way as files
        # scripting.AddAction(Open,"OpenUrl","Open URL (Internet radio)","Open URL (Internet radio)")

        self.AddGroup(
            "IPC Scripting",
            ("Scripting actions for the set of XMPlay commands that are compatible with Winamp API.")
        ).AddActionsFromList(actions_xmp_winamp.actions)

        self.AddGroup(
            "Catalog",
            ("Full official verbatim list of possible DDE actions to control XMPlay (except open). "
             "A scripting action DDECommand may be used instead of any of them.")
        ).AddActionsFromList(actions_xmp_catalog.actions)

    def __start__(self, path, suffix="", period=1.0):
        self.xmp_exe_path = path
        self.period = period
        self.suffix = suffix
        # no action without xmp_on!
        self.xmp_on = False
        self.lock = threading.Lock()
        self.observation = None
        self.dde_client = None

    def __stop__(self):
        self.xmp_on = False
        if self.observation:
            self.observation.terminate()
            self.observation = None
        self.xmp_memory_reader = None
        if self.dde_client:
            self.dde_client.shutdown()
            self.dde_client = None

    def dde_start(self):
        self.dde_client = DDEClient(callback=self.dde_callback)
        sleep(1)

    def dde_get_conversation(self, topic=NOTHING):
        """DDE shortcut."""
        # for XMPlay DDE execute topic is meaningless,
        # but it may save a conversation for DDE requests
        if topic is NOTHING: topic = "info0"  # this is most useful universal one
        return self.dde_client[("XMPlay", topic)]

    def dde_try(self, log=True):
        if self.lock.acquire(False):
            try:
                if self.xmp_on:
                    return True
                if self.observation:
                    self.observation.terminate()
                    self.observation = None
                # here globaly useful vars declared because
                # no one using them without xmp_on
                self.xmp_pid = 0
                self.xmp_window = None
                self.xmp_memory_reader = None
                # info_general made threadsafe with self.lock (unused feature for now)
                self.info_general = None
                self.info_message = None
                try:
                    conversation_info = self.dde_get_conversation().info()
                    if not conversation_info.wStatus & ST_CONNECTED:
                        raise Exception("DDE connection with XMPlay not confirmed.")
                    self.xmp_pid = eg.WinApi.GetWindowThreadProcessId(conversation_info.hwndPartner)[1]
                    if not self.xmp_pid:
                        raise Exception("Cannot find XMPlay DDE window 0x%.8X process." % conversation_info.hwndPartner)
                    for hwnd in eg.WinApi.GetTopLevelWindowList(False):
                        if (eg.WinApi.GetWindowThreadProcessId(hwnd)[1] == self.xmp_pid and
                            eg.WinApi.GetClassName(hwnd) == "XMPLAY-MAIN"):
                            self.xmp_window = hwnd
                            break
                    if not self.xmp_window:
                        raise Exception("Cannot find XMPlay process %i main window." % self.xmp_pid)
                    self.xmp_memory_reader = MemoryReader(self.xmp_pid)
                    self.xmp_on = True
                    self.TriggerEvent("Connected", payload=self.xmp_window)
                    if self.suffix:
                        self.observation = ObservationThread(self)
                        self.observation.start()
                    # print "XMP pid: %i" % self.xmp_pid
                    # print "XMP hwnd: " + hex(self.xmp_window)
                    # print conversation_info.__dict__
                except Exception as e:
                    if log: eg.PrintTraceback(self.text.error1)
                    # if log: eg.PrintError(e.__class__.__name__, str(e), self.text.error1)
                    return False
                return True
            finally:
                self.lock.release()
        else:
            with self.lock:
                return self.xmp_on

    def dde_callback(self, type, str1, **kwargs):
        """This is the core method of this plugin."""
        if str1.upper() != "XMPLAY": return
        if not self.xmp_on and type == XTYP_REGISTER:
            sleep(1)
            self.dde_try()
        elif self.xmp_on and type in (XTYP_UNREGISTER, XTYP_DISCONNECT, XTYP_ERROR):
            self.xmp_on = False
            if self.observation:
                self.observation.terminate()
                self.observation = None
            self.xmp_memory_reader = None
            # To call for DDEClient shutdown() in its own callback is NOT right.
            # That produces zombie DDEML windows.
            # So DDE once started will serve till plugin's stop (disable).
            self.TriggerEvent("Disconnected")
        # print kwargs

    def is_xmp_off(self, thorough=False, log=True):
        """
        Pattern for every action check:
        if self.plugin.is_xmp_off(): return

        """
        # fast check
        if self.xmp_on:
            retval = False
        # medium check
        # do no threading without dde_client !!!
        elif self.dde_client is None and eg.WinApi.Dynamic.FindWindow("XMPLAY-MAIN", None):
            # creating daemon on action
            self.dde_start()
            # log all errors, because window & no DDE is exception
            retval = not self.dde_try(log=True)
            log = False
            # flush malinformed events from the meantime
            eg.eventThread.ClearPendingEvents()
            eg.actionThread.ClearPendingEvents()
        # thorough check
        elif thorough and self.dde_client is not None:
            retval = not self.dde_try(False)
        else:
            retval = True

        if log and retval:
            eg.PrintNotice(self.text.error2)
        return retval

    def find_xmp_exe_path(self):
        """
        Get the path of XMPlay's installation directory through querying
        the Windows registry.
        """
        value = ""
        try:
            with _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                                 "Software\\Classes\\XMPlay\\shell\\Open\\command") as xmp:
                value = path.dirname(_winreg.EnumValue(xmp, 0)[1].strip('"'))
        except:
            pass
        return value

    def Configure(self, path=None, suffix="", period=1.0):
        if not path:
            path = self.find_xmp_exe_path()
        panel = eg.ConfigPanel(self)
        label1Text = wx.StaticText(panel, -1, self.text.label1)
        xmpPathCtrl = eg.DirBrowseButton(
            panel,
            size=(410, -1),
            startDirectory=path,
            toolTip=self.text.toolTipFolder,
            dialogTitle=self.text.browseTitle,
            buttonText=eg.text.General.browse
        )
        xmpPathCtrl.SetValue(path)
        val = suffix != ""
        evtCheckBox = wx.CheckBox(panel, -1, self.text.events)
        evtCheckBox.SetValue(val)
        label2Text = wx.StaticText(panel, -1, self.text.label2)
        suffixCtrl = wx.TextCtrl(panel, -1, suffix, size=(100, -1))
        suffixCtrl.Enable(val)
        print period
        periodNumCtrl = eg.SpinNumCtrl(
            parent=panel,
            value=period,
            integerWidth=5,
            fractionWidth=1,
            allowNegative=False,
            increment=0.1,
        )
        periodNumCtrl.numCtrl.SetMin(min=0.1)
        periodNumCtrl.Enable(val)
        intervalLbl = wx.StaticText(panel, -1, self.text.intervalLabel)
        intervalLbl.Enable(val)
        suffixSizer = wx.BoxSizer(wx.HORIZONTAL)
        suffixSizer.Add(evtCheckBox, 0, wx.TOP, 2)
        suffixSizer.Add(suffixCtrl, 0, wx.LEFT | wx.RIGHT, 5)
        suffixSizer.Add(label2Text, 0, wx.TOP, 2)
        periodSizer = wx.BoxSizer(wx.HORIZONTAL)
        periodSizer.Add(intervalLbl, 0, wx.TOP, 2)
        periodSizer.Add(periodNumCtrl, 0, wx.LEFT, 5)
        panelAdd = panel.sizer.Add
        panelAdd(label1Text, 0, wx.TOP, 15)
        panelAdd(xmpPathCtrl, 0, wx.EXPAND | wx.TOP, 2)
        panelAdd(suffixSizer, 0, wx.TOP, 20)
        panelAdd(periodSizer, 0, wx.TOP, 20)

        def OnCheckBox(evt):
            val = evt.IsChecked()
            suffixCtrl.Enable(val)
            intervalLbl.Enable(val)
            periodNumCtrl.Enable(val)
            suffixCtrl.ChangeValue("" if not val else self.text.suffix)

        evtCheckBox.Bind(wx.EVT_CHECKBOX, OnCheckBox)

        while panel.Affirmed():
            panel.SetResult(
                xmpPathCtrl.GetValue(),
                suffixCtrl.GetValue(),
                periodNumCtrl.GetValue()
            )

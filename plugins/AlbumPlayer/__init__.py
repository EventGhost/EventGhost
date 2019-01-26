# -*- coding: utf-8 -*-

#  1.1  added 'Bring To Front' action
#  1.0  initial version


import eg


eg.RegisterPlugin(
    name="AlbumPlayer",
    author="topix",
    version="1.0.1",
    kind="program",
    guid="{D944DEFC-C7BD-4E1E-AF7F-430B42315EF0}",
    createMacrosOnAdd=True,
    description='Adds actions to control '
                '<br><a href="http://www.albumplayer.com/">'
                'AlbumPlayer</a>.',
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=6838",
)


import ctypes
import win32gui
from sys import maxint

import wx

import xmltodict
from eg.WinApi.Dynamic import (
    COPYDATASTRUCT, PCOPYDATASTRUCT,
    WM_COPYDATA, WM_USER,
)


AP_REMOTE_CONTROL = WM_USER + 10  # remote control the AlbumPlayer
AP_SUBSCRIBE_FOR_INFO = WM_USER + 11  # subscribe to AlbumPlayer notifications
AP_NEW_COVER_AVAILABLE = WM_USER + 12  # notify a new cover is available
AP_NEW_RATING = WM_USER + 13  # notify new rating
AP_ADJUST_VOLUME = WM_USER + 14  # adjust volume

AP_RC_PLAY_PAUSE = 1
AP_RC_STOP = 2
AP_RC_NEXT_TRACK = 3
AP_RC_PREV_TRACK = 4
AP_RC_PLAY = 5
AP_RC_PAUSE = 6
AP_RC_INC_SPEED = 7  # Increase Play Speed Factor
AP_RC_DEC_SPEED = 8  # Decrease Play Speed Factor
AP_RC_SEEK = 9  # lparam = position in ms
AP_RC_SET_VOLUME = 10  # lparam 0 - 100
AP_RC_CHANGE_VOLUME = 11  # lparam = Steps on a volume scale of 0 to 100 (step max -100 to 100)
AP_RC_TOGGLE_MUTE = 12
AP_RC_BAN_TRACK = 13
AP_RC_RC_KEYS = 14  # lparam =
#       15 = Info
#       18 = Next Page
#       19 = Prev Page
#       30 = Up
#       31 = Down
#       32 = Left
#       33 = Right
#       34 = Ok/Enter
#       35 = Back
#       91 = Red Key
#       92 = Green Key
#       93 = Yellow Key
#       94 = Blue Key
AP_RC_REQ_STATE = 15  # Request Player state, lparam =
#   0 = Play State      (Notifies status with wparam 1)
#   1 = Track Progress  (Notifies sttus with wparam 6)
#   2 = Volume          (Notifies status with wparam 12)
AP_BRING_TO_FRONT = 100
AP_RC_EXIT = 101

AP_NOTIFY_NEW_TRACK = 0  # new track notification, ap_info.txt is written
AP_NOTIFY_NEW_PLAY_STATE = 1  # new play state
AP_NOTIFY_CLOSING = 2  # albumplayer will be closed
AP_NOTIFY_COVER_ACCEPTED = 3  # new cover is accepted
AP_NOTIFY_TRACK_UPDATE = 4  # track update notification, ap_info.txt is written, same track
AP_NOTIFY_NEW_PROGRESS = 5  # new track progress (lParam = progress in seconds)
AP_NOTIFY_PROGRESS_UPDATE = 6  # new track progress (lParam = progress in seconds)
AP_NOTIFY_PLAYLIST_CHANGED = 10
AP_NOTIFY_VOLUME_CHANGED = 12  # lparam = volume percentage (0-100)
AP_NOTIFY_SETTINGS_CHANGED = 20

AP_PLAY_STATES = [
    'Stopped',
    'Playing',
    'Paused'
]

AP_SETTING_TYPES = [
    'PreferencesChanged',
    'NewSkinApllied',
    'PartyModeChanged'
]


# noinspection PyPep8Naming
class AlbumPlayer(eg.PluginBase):
    # noinspection PyPep8Naming,PyClassHasNoInit
    class text:
        enableNotifications = 'Enable Notifications'

    def __init__(self):
        super(AlbumPlayer, self).__init__()
        self.apHwnd = None
        self.isEnabled = False
        self.verbose = False  # print the received dict
        # add actions to control AlbumPlayer
        self.AddActionsFromList(ACTIONS, RemoteControl)

    def __start__(self, notifications):
        self.notifyMe = notifications
        self.FindWindow()
        if not self.apHwnd:
            self.PrintError('AlbumPlayer is not running.')
            self.TriggerEvent('NotRunning')
            return False
        self.msg_rcvr = eg.MessageReceiver("AP_plugin_")
        msg = self.msg_rcvr.AddWmUserHandler(self.SimpleMessageHandler)
        self.msg_rcvr.AddHandler(WM_COPYDATA, self.XmlMessageHandler)
        if not self.isEnabled:
            self.msg_rcvr.Start()
        # we want to receive notifications from AlbumPlayer
        win32gui.SendMessage(self.apHwnd, AP_SUBSCRIBE_FOR_INFO,
                             self.msg_rcvr.hwnd, msg)
        win32gui.SendMessage(self.apHwnd, AP_SUBSCRIBE_FOR_INFO,
                             self.msg_rcvr.hwnd, WM_COPYDATA)
        self.TriggerEvent('Connected')
        self.isEnabled = True
        return True

    def __stop__(self):
        if self.apHwnd:
            self.msg_rcvr.RemoveWmUserHandler(self.SimpleMessageHandler)
            self.msg_rcvr.RemoveHandler(WM_COPYDATA, self.XmlMessageHandler)
        if hasattr(self, 'msg_rcvr'):
            # noinspection PyProtectedMember
            if self.msg_rcvr._ThreadWorker__thread.is_alive():
                wx.CallAfter(self.msg_rcvr.Stop)
            self.msg_rcvr = None
            del self.msg_rcvr
        self.TriggerEvent('Disconnected')
        self.isEnabled = False
        return

    def __close__(self):
        pass

    def Configure(self, notifications=True):
        panel = eg.ConfigPanel()

        notify = wx.CheckBox(panel, wx.ID_ANY, self.text.enableNotifications)
        notify.SetValue(notifications)

        panel.sizer.AddStretchSpacer()
        panel.sizer.Add(notify, 0, wx.ALIGN_CENTRE)
        panel.sizer.AddStretchSpacer()

        # panel.dialog.buttonRow.applyButton.Enable(False)
        while panel.Affirmed():
            panel.SetResult(notify.GetValue())

    def FindWindow(self):
        # Find the AlbumPlayer window
        self.apHwnd = win32gui.FindWindow('TfrmPlayer', 'AlbumPlayer')

    # noinspection PyUnusedLocal
    def SimpleMessageHandler(self, hwnd, mesg, wParam, lParam):
        if wParam == AP_NOTIFY_CLOSING:
            self.__stop__()
            self.apHwnd = None
            self.TriggerEvent("Closing")

        if not self.notifyMe or not self.isEnabled:
            return True

        if wParam == AP_NOTIFY_NEW_PROGRESS:
            return True
            # self.TriggerEvent("Progress", payload=lParam)
        elif wParam == AP_NOTIFY_PROGRESS_UPDATE:
            return True
            # self.TriggerEvent("ProgressUpdate", payload=lParam)
        elif wParam == AP_NOTIFY_COVER_ACCEPTED:
            self.TriggerEvent("CoverAccepted")
        elif wParam == AP_NOTIFY_NEW_PLAY_STATE:
            self.TriggerEvent(AP_PLAY_STATES[lParam])
        elif wParam == AP_NOTIFY_NEW_TRACK:
            self.TriggerEvent("NewTrack", payload=lParam)
        elif wParam == AP_NOTIFY_TRACK_UPDATE:
            self.TriggerEvent("TrackUpdate")
        elif wParam == AP_NOTIFY_PLAYLIST_CHANGED:
            self.TriggerEvent("PlaylistChanged")
        elif wParam == AP_NOTIFY_VOLUME_CHANGED:
            self.TriggerEvent("VolumeChanged", payload=lParam)
        elif wParam == AP_NOTIFY_SETTINGS_CHANGED:
            self.TriggerEvent(AP_SETTING_TYPES[lParam])
        else:
            print u'unknown simple message. (wParam=%s, lParam=%s)' % (repr(wParam), repr(lParam))
        return True

    def PrintDict(self, theDict):
        for key, value in theDict.iteritems():
            if isinstance(value, dict):
                self.PrintDict(value)
            else:
                print key, ':', value

    # noinspection PyPep8Naming,PyUnusedLocal
    def XmlMessageHandler(self, hwnd, mesg, wParam, lParam):
        cpy_data = ctypes.cast(lParam, PCOPYDATASTRUCT)
        msg = xmltodict.parse(ctypes.string_at(cpy_data.contents.lpData))
        if 'AlbumPlayerReply' in msg:
            if not msg['AlbumPlayerReply']:
                return True
            cmd = msg['AlbumPlayerReply'].pop('@id')
            self.TriggerEvent(cmd, payload=msg['AlbumPlayerReply'])
            if self.verbose:
                self.PrintDict(msg['AlbumPlayerReply'])
        else:
            self.PrintError(u'Unknown xml message: %s' % repr(msg))
        return True

    def SendCopydata(self, xml_msg):
        if not self.apHwnd:
            return None
        cpy_data = ctypes.create_string_buffer(xml_msg)
        cds = COPYDATASTRUCT()
        cds.cbData = ctypes.sizeof(cpy_data)
        cds.lpData = ctypes.cast(ctypes.pointer(cpy_data), ctypes.c_void_p)
        return win32gui.SendMessage(self.apHwnd, WM_COPYDATA, self.msg_rcvr.hwnd, cds)


class ConnectAP(eg.ActionBase):
    """ Connect to AlbumPlayer """

    def __call__(self):
        if self.plugin.apHwnd:
            return True
        return self.plugin.__start__(self.plugin.notifyMe)


# noinspection PyUnresolvedReferences
class RemoteControl(eg.ActionBase):
    """ Send a Window Message to AlbumPlayer. """

    def __call__(self):
        if not self.plugin.apHwnd:
            print "no apHwnd"
            return None
        print "VALUE:", self.value
        return win32gui.SendMessage(
            self.plugin.apHwnd,
            AP_REMOTE_CONTROL,
            self.value,
            0
        )


# noinspection PyUnresolvedReferences
class RemoteControlKey(eg.ActionBase):
    """ Send a Window Message to AlbumPlayer. """

    def __call__(self):
        if not self.plugin.apHwnd:
            return None
        return win32gui.SendMessage(
            self.plugin.apHwnd,
            AP_REMOTE_CONTROL,
            AP_RC_RC_KEYS,
            self.value
        )


# noinspection PyUnresolvedReferences
class SetVolume(eg.ActionBase):
    """ Set the Volume on a scale of 0 to 100. """

    # noinspection PyPep8Naming,PyClassHasNoInit
    class text:
        lblVolume = 'Set the volume on a scale of 0 to 100.'

    def __call__(self, volume):
        if not self.plugin.apHwnd:
            return None
        return win32gui.SendMessage(
            self.plugin.apHwnd,
            AP_REMOTE_CONTROL,
            self.value,
            volume
        )

    def Configure(self, volume=50):
        panel = eg.ConfigPanel()

        label = wx.StaticText(panel, wx.ID_ANY, self.text.lblVolume)
        spin = wx.SpinCtrl(
            panel,
            wx.ID_ANY,
            style=wx.SP_ARROW_KEYS | wx.ALIGN_RIGHT | wx.SP_WRAP,
            min=0,
            max=100,
            initial=volume
        )

        panel.sizer.AddStretchSpacer()
        panel.sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        panel.sizer.Add(spin, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        panel.sizer.AddStretchSpacer()

        while panel.Affirmed():
            panel.SetResult(spin.GetValue())


# noinspection PyUnresolvedReferences
class ChangeVolume(eg.ActionBase):
    """ Increase/Decrease the volume. """

    # noinspection PyPep8Naming,PyClassHasNoInit
    class text:
        lblVolume = 'Set the steps to increase or decrease the volume (step max -100 to 100):'

    def __call__(self, volume):
        if not self.plugin.apHwnd:
            return None
        return win32gui.SendMessage(
            self.plugin.apHwnd,
            AP_REMOTE_CONTROL,
            self.value,
            volume
        )

    def Configure(self, volume=50):
        panel = eg.ConfigPanel()

        label = wx.StaticText(panel, wx.ID_ANY, self.text.lblVolume)
        spin = wx.SpinCtrl(
            panel,
            wx.ID_ANY,
            style=wx.SP_ARROW_KEYS | wx.ALIGN_RIGHT | wx.SP_WRAP,
            min=-100,
            max=100,
            initial=volume
        )

        panel.sizer.AddStretchSpacer()
        panel.sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        panel.sizer.Add(spin, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        panel.sizer.AddStretchSpacer()

        while panel.Affirmed():
            panel.SetResult(spin.GetValue())


# noinspection PyUnresolvedReferences
class Seek(eg.ActionBase):
    """ Seek to position (in ms). """

    # noinspection PyPep8Naming,PyClassHasNoInit
    class text:
        lblVolume = 'Seek to position (in ms):'

    def __call__(self, position):
        if not self.plugin.apHwnd:
            return None
        return win32gui.SendMessage(
            self.plugin.apHwnd,
            AP_REMOTE_CONTROL,
            self.value,
            position
        )

    def Configure(self, position=0):
        panel = eg.ConfigPanel()

        label = wx.StaticText(panel, wx.ID_ANY, self.text.lblVolume)
        spin = wx.SpinCtrl(
            panel,
            wx.ID_ANY,
            style=wx.SP_ARROW_KEYS | wx.ALIGN_RIGHT | wx.SP_WRAP,
            min=0,
            max=maxint,
            initial=position
        )

        panel.sizer.AddStretchSpacer()
        panel.sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        panel.sizer.Add(spin, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        panel.sizer.AddStretchSpacer()

        while panel.Affirmed():
            panel.SetResult(spin.GetValue())


# noinspection PyUnresolvedReferences
class SendSimpleXmlCommand(eg.ActionBase):
    """
    Send a AlbumPlayerCommand which is only build of the id
    and don't need any further parameters.
    """

    def __call__(self):
        xml_msg = r'<?xml version="1.0" encoding="utf-8"?>' \
                 r'<AlbumPlayerCommand id="%s"/>' % self.value
        return self.plugin.SendCopydata(xml_msg)


ACTIONS = (
    (ConnectAP, 'Connect', 'Connect to AlbumPlayer', 'Connect to AlbumPlayer if it wasn\'t running at plugin start.',
     None),
    (RemoteControl, 'CloseAP', 'Quit AlbumPlayer', None, AP_RC_EXIT),
    (RemoteControl, 'BringToFront', 'Bring To Front', None, AP_BRING_TO_FRONT),
    (RemoteControl, 'PlayPause', 'Play/Pause', None, AP_RC_PLAY_PAUSE),
    (RemoteControl, 'Play', 'Play', None, AP_RC_PLAY),
    (RemoteControl, 'Pause', 'Pause', None, AP_RC_PAUSE),
    (RemoteControl, 'Stop', 'Stop', None, AP_RC_STOP),
    (RemoteControl, 'NextTrack', 'Next Track', None, AP_RC_NEXT_TRACK),
    (RemoteControl, 'PreviousTrack', 'Previous Track', None, AP_RC_PREV_TRACK),
    (RemoteControl, 'IncSpeed', 'Increase Play Speed', None, AP_RC_INC_SPEED),
    (RemoteControl, 'DecSpeed', 'Decrease Play Speed', None, AP_RC_DEC_SPEED),
    (RemoteControl, 'ToggleMute', 'Toggle mute', None, AP_RC_TOGGLE_MUTE),
    (SetVolume, 'SetVolume', 'Set Volume', None, AP_RC_SET_VOLUME),
    (ChangeVolume, 'ChangeVolume', 'Increase/Decrease Volume', None, AP_RC_CHANGE_VOLUME),
    (Seek, 'Seek', 'Seek to position', None, AP_RC_SEEK),
    (RemoteControl, 'BanTrack', 'Ban track', None, AP_RC_BAN_TRACK),

    (eg.ActionGroup, 'AlbumPlayerRequests', 'Request info from AlbumPlayer', None, (
        (SendSimpleXmlCommand, "GetWindowState", "Get window state", "Get window State", 'GetWindowState'),
        (SendSimpleXmlCommand, "GetNowPlayingInfo", "GetNowPlayingInfo", "GetNowPlayingInfo", 'GetNowPlayingInfo'),
        (SendSimpleXmlCommand, "GetPlayMode", "GetPlayMode", "GetPlayMode", 'GetPlayMode'),
        (SendSimpleXmlCommand, "GetPlayState", "GetPlayState", "GetPlayState", 'GetPlayState'),
        (SendSimpleXmlCommand, "GetPlaylistNameList", "GetPlaylistNameList", "GetPlaylistNameList",
         'GetPlaylistNameList'),
        (SendSimpleXmlCommand, "ClearPlaylist", "ClearPlaylist", "ClearPlaylist", 'ClearPlaylist'),
        (SendSimpleXmlCommand, "GetCollectionTypeList", "GetCollectionTypeList", "GetCollectionTypeList",
         'GetCollectionTypeList'),
        (SendSimpleXmlCommand, "GetCollectionType", "GetCollectionType", "GetCollectionType", 'GetCollectionType'),
        (SendSimpleXmlCommand, "GetPage", "GetPage", "GetPage", 'GetPage'),
        (SendSimpleXmlCommand, "GetSelectedAlbum", "GetSelectedAlbum", "GetSelectedAlbum", 'GetSelectedAlbum'),
        (SendSimpleXmlCommand, "GetPartyModeSettings", "GetPartyModeSettings", "GetPartyModeSettings",
         'GetPartyModeSettings'),
        (SendSimpleXmlCommand, "GetCredits", "GetCredits", "GetCredits", 'GetCredits'),
    )),
    (eg.ActionGroup, 'RemoteControlKeys', 'Remote Control Keys', None, (
        (RemoteControlKey, "KeyInfo", "Info", "Info", 15),
        (RemoteControlKey, "KeyNextPage", "Next Page", "Next Page", 18),
        (RemoteControlKey, "KeyPrevPage", "Previous Page", "Previous Page", 19),
        (RemoteControlKey, "KeyUp", "Up", "Up", 30),
        (RemoteControlKey, "KeyDown", "Down", "Down", 31),
        (RemoteControlKey, "KeyLeft", "Left", "Left", 32),
        (RemoteControlKey, "KeyRight", "Right", "Right", 33),
        (RemoteControlKey, "KeyOkEnter", "Ok/Enter", "Ok/Enter", 34),
        (RemoteControlKey, "KeyBack", "Back", "Back", 35),
        (RemoteControlKey, "KeyRed", "Red", "Red", 91),
        (RemoteControlKey, "KeyGreen", "Green", "Green", 92),
        (RemoteControlKey, "KeyYellow", "Yellow", "Yellow", 93),
        (RemoteControlKey, "KeyBlue", "Blue", "Blue", 94),
    )),
)

eg.RegisterPlugin(
    name = "SageTV",
    author = "Bitmonster",
    version = "1.2.1093",
    kind = "program",
    guid = "{654FC50A-3052-42F7-AE26-84A752FFDCA6}",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=795",
    description = (
        'Adds actions to control the <a href="http://www.sagetv.com/">'
        'SageTV Media Center</a>.'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAB3RJTUUH1wMXEAcEHYti"
        "bwAAABd0RVh0U29mdHdhcmUAR0xEUE5HIHZlciAzLjRxhaThAAAACHRwTkdHTEQzAAAA"
        "AEqAKR8AAAAEZ0FNQQAAsY8L/GEFAAACx0lEQVR4nH2TbUhTYRTH9+Z0u3POu93t7u5F"
        "J5ovEWVvJlEaWhIRiSaCZmpSfSor8oNCX4QikqCQzPpQERqUsC8hmh/UQNEoN5thapRa"
        "JoLMFywni/x37iWlNDvwg/vA+f/POc95rky2QcQ4o7YSFUQlsWejvHVhjGSNsdGue07B"
        "9t3MGsFFsqDvYExU9DOXw2n7r1inZdQOwfbczluREBuHspJSnD19BlsSkyBwZlAnPYaI"
        "CP2GBiajsZCqIWXHTni9XqzE8NAwMtLTYbfwsHDcpQ0NBIulyUqVnjQ0Ym10trfDaRVA"
        "HXb8U6zVaFOibLYpm9mCfo93ncHczAziXDGg8QICz//dRTijc9B841aTGbnHsvGguw6P"
        "3tXh/ewAxr8FcevlEKqb+1BefgFRggCXwwGLiStYNaDDDbH1k4UnsLS4hJ7JTpS2HMfl"
        "xlwUV12H62oz6rtHpE7u1NZCzHVYhUEdw2hkKqVKTYc30XYHXvX2rrbc5+9DfdVR1KRt"
        "h9v7EcEfQSwsLGBsbAx7U1Ol9bIGwz6ZQqGw2Hj+i7iqiYkJSbz82+TrzXMYLEhE0D+F"
        "ab8fIyMj8Hg8OJyVBT2jQ0S4Pl8ml8s5wcIP2OmGX7S2SsJAIIDFn8v43FAD38UjGB0d"
        "Rf9bH7q6uuB2u7E5IREGvR5qtfqgeAUaNsLwWLz9A/vT4PP5MD8/h+mZWbS5n+J+dSVe"
        "01Y6OjokcW5OjlSdDD7J5DLpZSqUCkU2jTFpZk1Iik/AqZISFBcVYVNcPDgzj0OZmcjP"
        "y8P25GSEMwyMhkiEqtVXSKtcWYRdpVJVmFjjB45lpQoilLhsYtmgKGLCNJKYnvIsie+G"
        "qEKSqbBixUB0SiLKaK46nVbbQjSrQ0Juk/E1TZimidFq20JDQx+S5jzlbVMqlZq1j1FO"
        "iDOJv24WkUHsJnYR6UQmkUI4/mz9FwoIacGNmDGLAAAAAElFTkSuQmCC"
    ),
)

# Plugin implements the description from here:
# http://www.sage.tv/2_papers/SageTVWindowsMessages.txt

# changelog:
# 1.2 by bitmonster
#     - changed code to use new AddActionsFromList
#     - uses new eg.WinApi calls for SendMessage
# 1.1 by eruji
#     - added actions from 90 to 104
# 1.0 by bitmonster
#     - initial version



ACTIONS = (
    ("Left", "Left", None, 2),
    ("Right", "Right", None, 3),
    ("Up", "Up", None, 4),
    ("Down", "Down", None, 5),
    ("Pause", "Pause", None, 6),
    ("Play", "Play", None, 7),
    ("SkipFwdPageRight", "Skip Fwd/Page Right", None, 8),
    ("SkipBkwdPageLeft", "Skip Bkwd/Page Left", None, 9),
    ("TimeScroll", "Time Scroll", None, 10),
    ("ChannelUpPageUp", "Channel Up/Page Up", None, 11),
    ("ChannelDownPageDown", "Channel Down/Page Down", None, 12),
    ("VolumeUp", "Volume Up", None, 13),
    ("VolumeDown", "Volume Down", None, 14),
    ("Tv", "TV", None, 15),
    ("PlayFaster", "Play Faster", None, 16),
    ("PlaySlower", "Play Slower", None, 17),
    ("Guide", "Guide", None, 18),
    ("Power", "Power", None, 19),
    ("Select", "Select", None, 20),
    ("Watched", "Watched", None, 21),
    ("Favorite", "Favorite", None, 22),
    ("DontLike", "Don't Like", None, 23),
    ("Info", "Info", None, 24),
    ("Record", "Record", None, 25),
    ("Mute", "Mute", None, 26),
    ("FullScreen", "Full Screen", None, 27),
    ("Home", "Home", None, 28),
    ("Options", "Options", None, 29),
    ("Num0", "Num 0", None, 30),
    ("Num1", "Num 1", None, 31),
    ("Num2", "Num 2", None, 32),
    ("Num3", "Num 3", None, 33),
    ("Num4", "Num 4", None, 34),
    ("Num5", "Num 5", None, 35),
    ("Num6", "Num 6", None, 36),
    ("Num7", "Num 7", None, 37),
    ("Num8", "Num 8", None, 38),
    ("Num9", "Num 9", None, 39),
    ("Search", "Search", None, 40),
    ("Setup", "Setup", None, 41),
    ("Library", "Library", None, 42),
    ("PowerOn", "Power On", None, 43),
    ("PowerOff", "Power Off", None, 44),
    ("MuteOn", "Mute On", None, 45),
    ("MuteOff", "Mute Off", None, 46),
    ("AspectRatioFill", "Aspect Ratio Fill", None, 47),
    ("AspectRatio4x3", "Aspect Ratio 4x3", None, 48),
    ("AspectRatio16x9", "Aspect Ratio 16x9", None, 49),
    ("AspectRatioSource", "Aspect Ratio Source", None, 50),
    ("RightVolumeUp", "Right/Volume Up", None, 51),
    ("LeftVolumeDown", "Left/Volume Down", None, 52),
    ("UpChannelUp", "Up/Channel Up", None, 53),
    ("DownChannelDown", "Down/Channel Down", None, 54),
    ("PageUp", "Page Up", None, 55),
    ("PageDown", "Page Down", None, 56),
    ("PageRight", "Page Right", None, 57),
    ("PageLeft", "Page Left", None, 58),
    ("PlayPause", "Play/Pause", None, 59),
    ("PreviousChannel", "Previous Channel", None, 60),
    ("SkipFwd2", "Skip Fwd #2", None, 61),
    ("SkipBkwd2", "Skip Bkwd #2", None, 62),
    ("LiveTv", "Live TV", None, 63),
    ("DvdReversePlay", "DVD Reverse Play", None, 64),
    ("DvdNextChapter", "DVD Next Chapter", None, 65),
    ("DvdPrevChapter", "DVD Prev Chapter", None, 66),
    ("DvdMenu", "DVD Menu", None, 67),
    ("DvdTitleMenu", "DVD Title Menu", None, 68),
    ("DvdReturn", "DVD Return", None, 69),
    ("DvdSubtitleChange", "DVD Subtitle Change", None, 70),
    ("DvdSubtitleToggle", "DVD Subtitle Toggle", None, 71),
    ("DvdAudioChange", "DVD Audio Change", None, 72),
    ("DvdAngleChange", "DVD Angle Change", None, 73),
    ("Dvd", "DVD", None, 74),
    ("Back", "Back", None, 75),
    ("Forward", "Forward", None, 76),
    ("Customize", "Customize", None, 77),
    ("Custom1", "Custom1", None, 78),
    ("Custom2", "Custom2", None, 79),
    ("Custom3", "Custom3", None, 80),
    ("Custom4", "Custom4", None, 81),
    ("Custom5", "Custom5", None, 82),
    ("Delete", "Delete", None, 83),
    ("MusicJukebox", "Music Jukebox", None, 84),
    ("RecordingSchedule", "Recording Schedule", None, 85),
    ("SageTvRecordings", "SageTV Recordings", None, 86),
    ("PictureLibrary", "Picture Library", None, 87),
    ("VideoLibrary", "Video Library", None, 88),
    ("Stop", "Stop", None, 89),
    ("Eject", "Eject", None, 90),
    ("StopEject", "Stop/Eject", None, 91),
    ("Input", "Input", None, 92),
    ("SmoothFF", "Smooth FF", None, 93),
    ("SmoothRew", "Smooth Rew", None, 94),
    ("AspectRatioToggle", "Aspect Ratio Toggle", None, 96),
    ("FullScreenOn", "Full Screen On", None, 97),
    ("FullScreenOff", "Full Screen Off", None, 98),
    ("RightSkipFwd", "Right Skip Fwd", None, 99),
    ("LeftSkipBkwd", "Left Skip Bkwd", None, 100),
    ("UpVolUp", "Left Vol Up", None, 101),
    ("DownVolDown", "Down Vol Down", None, 102),
    ("Online", "Online", None, 103),
    ("VideoOutput", "Video Output", None, 104),
)


from eg.WinApi import SendMessageTimeout, FindWindow


class ActionPrototype(eg.ActionClass):

    def __call__(self):
        """
        Find SageTV's message window and send it a message with
        SendMessageTimeout.
        """
        try:
            hwnd = FindWindow(self.plugin.targetClass, "SageWin")
            # WM_USER + 234 = 1258
            return SendMessageTimeout(hwnd, 1258, self.value, self.value)
        except:
            raise self.Exceptions.ProgramNotRunning



class SageTV(eg.PluginClass):

    def __init__(self):
        self.targetClass = "SageApp"
        self.AddActionsFromList(ACTIONS, ActionPrototype)


    def __start__(self, useClient=False):
        if useClient:
            self.targetClass = "SageClientApp"
        else:
            self.targetClass = "SageApp"


    def Configure(self, useClient=False):
        panel = eg.ConfigPanel(self)
        useClientCtrl = wx.RadioBox(
            panel,
            label = "Target:",
            choices=["SageTV.exe", "SageTVClient.exe"],
            style=wx.RA_SPECIFY_ROWS
        )
        useClientCtrl.SetSelection(useClient)
        panel.sizer.Add(useClientCtrl, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(useClientCtrl.GetSelection())




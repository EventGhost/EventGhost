eg.RegisterPlugin(
    name = "SageTV",
    author = "Bitmonster",
    version = "1.2." + "$LastChangedRevision$".split()[1],
    kind = "program",
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
    ("Left", "Left", 2),
    ("Right", "Right", 3),
    ("Up", "Up", 4),
    ("Down", "Down", 5),
    ("Pause", "Pause", 6),
    ("Play", "Play", 7),
    ("SkipFwdPageRight", "Skip Fwd/Page Right", 8),
    ("SkipBkwdPageLeft", "Skip Bkwd/Page Left", 9),
    ("TimeScroll", "Time Scroll", 10),
    ("ChannelUpPageUp", "Channel Up/Page Up", 11),
    ("ChannelDownPageDown", "Channel Down/Page Down", 12),
    ("VolumeUp", "Volume Up", 13),
    ("VolumeDown", "Volume Down", 14),
    ("Tv", "TV", 15),
    ("PlayFaster", "Play Faster", 16),
    ("PlaySlower", "Play Slower", 17),
    ("Guide", "Guide", 18),
    ("Power", "Power", 19),
    ("Select", "Select", 20),
    ("Watched", "Watched", 21),
    ("Favorite", "Favorite", 22),
    ("DontLike", "Don't Like", 23),
    ("Info", "Info", 24),
    ("Record", "Record", 25),
    ("Mute", "Mute", 26),
    ("FullScreen", "Full Screen", 27),
    ("Home", "Home", 28),
    ("Options", "Options", 29),
    ("Num0", "Num 0", 30),
    ("Num1", "Num 1", 31),
    ("Num2", "Num 2", 32),
    ("Num3", "Num 3", 33),
    ("Num4", "Num 4", 34),
    ("Num5", "Num 5", 35),
    ("Num6", "Num 6", 36),
    ("Num7", "Num 7", 37),
    ("Num8", "Num 8", 38),
    ("Num9", "Num 9", 39),
    ("Search", "Search", 40),
    ("Setup", "Setup", 41),
    ("Library", "Library", 42),
    ("PowerOn", "Power On", 43),
    ("PowerOff", "Power Off", 44),
    ("MuteOn", "Mute On", 45),
    ("MuteOff", "Mute Off", 46),
    ("AspectRatioFill", "Aspect Ratio Fill", 47),
    ("AspectRatio4x3", "Aspect Ratio 4x3", 48),
    ("AspectRatio16x9", "Aspect Ratio 16x9", 49),
    ("AspectRatioSource", "Aspect Ratio Source", 50),
    ("RightVolumeUp", "Right/Volume Up", 51),
    ("LeftVolumeDown", "Left/Volume Down", 52),
    ("UpChannelUp", "Up/Channel Up", 53),
    ("DownChannelDown", "Down/Channel Down", 54),
    ("PageUp", "Page Up", 55),
    ("PageDown", "Page Down", 56),
    ("PageRight", "Page Right", 57),
    ("PageLeft", "Page Left", 58),
    ("PlayPause", "Play/Pause", 59),
    ("PreviousChannel", "Previous Channel", 60),
    ("SkipFwd2", "Skip Fwd #2", 61),
    ("SkipBkwd2", "Skip Bkwd #2", 62),
    ("LiveTv", "Live TV", 63),
    ("DvdReversePlay", "DVD Reverse Play", 64),
    ("DvdNextChapter", "DVD Next Chapter", 65),
    ("DvdPrevChapter", "DVD Prev Chapter", 66),
    ("DvdMenu", "DVD Menu", 67),
    ("DvdTitleMenu", "DVD Title Menu", 68),
    ("DvdReturn", "DVD Return", 69),
    ("DvdSubtitleChange", "DVD Subtitle Change", 70),
    ("DvdSubtitleToggle", "DVD Subtitle Toggle", 71),
    ("DvdAudioChange", "DVD Audio Change", 72),
    ("DvdAngleChange", "DVD Angle Change", 73),
    ("Dvd", "DVD", 74),
    ("Back", "Back", 75),
    ("Forward", "Forward", 76),
    ("Customize", "Customize", 77),
    ("Custom1", "Custom1", 78),
    ("Custom2", "Custom2", 79),
    ("Custom3", "Custom3", 80),
    ("Custom4", "Custom4", 81),
    ("Custom5", "Custom5", 82),
    ("Delete", "Delete", 83),
    ("MusicJukebox", "Music Jukebox", 84),
    ("RecordingSchedule", "Recording Schedule", 85),
    ("SageTvRecordings", "SageTV Recordings", 86),
    ("PictureLibrary", "Picture Library", 87),
    ("VideoLibrary", "Video Library", 88),
    ("Stop", "Stop", 89),
    ("Eject", "Eject", 90),
    ("StopEject", "Stop/Eject", 91),
    ("Input", "Input", 92),
    ("SmoothFF", "Smooth FF", 93),
    ("SmoothRew", "Smooth Rew", 94),
    ("AspectRatioToggle", "Aspect Ratio Toggle", 96),
    ("FullScreenOn", "Full Screen On", 97),
    ("FullScreenOff", "Full Screen Off", 98),
    ("RightSkipFwd", "Right Skip Fwd", 99),
    ("LeftSkipBkwd", "Left Skip Bkwd", 100),
    ("UpVolUp", "Left Vol Up", 101),
    ("DownVolDown", "Down Vol Down", 102),
    ("Online", "Online", 103),
    ("VideoOutput", "Video Output", 104),
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




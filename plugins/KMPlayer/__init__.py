import eg

eg.RegisterPlugin(
    name="KMPlayer",
    guid='{D28B1EC9-0099-49B8-825B-433F54E0C236}',
    author="Milbrot",
    version="1.0." + "$LastChangedRevision: 348 $".split()[1],
    kind="program",
    createMacrosOnAdd=True,
    description=(
        "Adds actions to control KMPlayer - Powered by Pandora TV.\n\n"
        "<p><a href=\"http://www.kmplayer.com/forums/forums.php/\">KMPlayer's Forums</a></p>"
    ),
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACt0lEQVR42qWTW0gUURzG"
        "v5nddS1L89JYSeWqCVmusg9RrqT5oOQlRboZJEomQmvuZigUmK5UVEJWkpGigaDdsA1N"
        "SS0fArOb+GBK+GBR1LaG66q567o709kzkxj05oEz/xnmfL/5n+87wwRE7hawgsF4ACWN"
        "ryBfmIZSzpApwFvGQM4CP75M4HVfDxx2O3x8/RAcGgH/TWGAlzdmnQLajHki4HTTAGQO"
        "GwUoZICSiMeHBtHffp9+JUabiKi4BCh8/OHggYVFAS6lH+pPxomAotv9YBesIoCIJz+P"
        "40VrE1iZDMk5eQgOi4CbCBfdREymgwB4b3806vaJgJQTVdi6Qw2ljAXLO/H8bg3mZ2zQ"
        "Zh2BKloDnojdxKlFUp0eiIuHmwDu6RJFgEoVC3XaUWyM2I7vI+8x3P0IwaptSMgpAHWY"
        "XFyeDqTqlAAtxRIg/uAZmC4eQnmHBVcyOGiS8jH0shnGHgv1oCKZQ0W3Bcb9HH0uaTeD"
        "XxWANn2CCMg434rmXBV9mXTcCJv5Kz70NvwTV3kngadz0D+1oDaTQ1GXE48NfwHVHWg+"
        "HEQXJh67AMfMFAY7b6GsQ+zgKunKQITXM8UOCh6aAdKB6awEiC19gr7CDUir7MSzynTs"
        "StXhbVcd9CYRUJvFQdduQV02h9y2n5gjUdi9AvGuSvIgJKcOI/V6qAsvwTr6BtbhXuwx"
        "3ITSZy0F0BRInSMuusmNm2Sq8OUwdlkCKMJTMTU6AE1pA36bJ/Cx8Rwis4sRFK0VU+Bp"
        "EBTCSET5coB1Wo7wzFMIVO+lmY0/uIb5yW+I0d343+lfBpA8WK3JQ0h8FsCydInLPke2"
        "ZEBAVBy2pOQv6ZaGB+C3HmPVWhGws6wLrtlfYFgZGIaha13zNnwy3cHm+ANYFxpFNALd"
        "hiCQSoyQrwnESE2aCFjJ7/wHPxcgEF4vrrkAAAAASUVORK5CYII="
    ),
)

import _winreg
from eg.WinApi import FindWindow, SendMessageTimeout
from win32con import SMTO_ABORTIFHUNG, SMTO_NORMAL
from win32api import ShellExecute


class KMPlayer(eg.PluginClass):

    def __init__(self):
        self.AddActionsFromList(ACTIONS)

    def __start__(self):
        try:
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\\KMPlayer\\KMP2.0\\OptionArea")
            self.myKMPlayerPath, dummy = _winreg.QueryValueEx(key, "InstallPath")
        except WindowsError:
            self.PrintError("KMPlayer installation path not found!")
            self.myTheatrePath = ""


gWindowMatcher = eg.WindowMatcher("KMPlayer.exe")


class GetAction(eg.ActionClass):

    def __call__(self):
        try:
            hwnd = gWindowMatcher()[0]
            result = SendMessageTimeout(hwnd, 2242, self.value, 0)
            if (result == 0):
                self.plugin.TriggerEvent("PlayMode Normal")
            elif (result == 1):
                self.plugin.TriggerEvent("PlayMode DVD")
            elif (result == 2):
                self.plugin.TriggerEvent("PlayMode WDM")
            elif (result == 3):
                self.plugin.TriggerEvent("PlayMode Audio")
            elif (result == 4):
                self.plugin.TriggerEvent("PlayMode Video")
            return result
        except:
            raise self.Exceptions.ProgramNotRunning


class MsgAction(eg.ActionClass):

    def __call__(self):
        try:
            hwnd = gWindowMatcher()[0]
            return SendMessageTimeout(hwnd, 2242, self.value, 0, SMTO_ABORTIFHUNG | SMTO_NORMAL, 3000)
        except:
            raise self.Exceptions.ProgramNotRunning


class ExeAction(eg.ActionClass):
    def __call__(self):
        try:
            return ShellExecute(0, None, self.plugin.myKMPlayerPath, self.value, None, 0)
        except:
            raise self.Exceptions.ProgramNotFound


ACTIONS = (
    (eg.ActionGroup, 'Open', 'Open', None, (
        (MsgAction, 'File', 'File', None, 0x19),
        (MsgAction, 'URL', 'URL', None, 0x1A),
        (MsgAction, 'Folder', 'Folder', None, 0x1B),
        (MsgAction, 'TVOut', 'TVOut', None, 0x101B),
        (MsgAction, 'IEMedia', 'IEMedia', None, 0x1C),
        (MsgAction, 'Recent', 'Recent', None, 0x1D),
        (MsgAction, 'ReTry', 'ReTry', None, 0x1E),
        (MsgAction, 'WDM', 'WDM', None, 0x1F),
        (MsgAction, 'BaseWDM', 'BaseWDM', None, 0x101F),
        (MsgAction, 'DVDDevice', 'DVDDevice', None, 0x20),
        (MsgAction, 'DVDFile', 'DVDFile', None, 0x21),
        (MsgAction, 'VCD', 'VCD', None, 0x22),
        (MsgAction, 'URL', 'URL', None, 0x16E),
        (MsgAction, 'Menu', 'Menu', None, 0x6),
    )),
    (eg.ActionGroup, 'DVD', 'DVD', None, (
        (MsgAction, 'SubpictureMenu', 'SubpictureMenu', None, 0x30),
        (MsgAction, 'AudioMenu', 'AudioMenu', None, 0x31),
        (MsgAction, 'AngleMenu', 'AngleMenu', None, 0x32),
        (MsgAction, 'MoveMenu', 'MoveMenu', None, 0x33),
        (MsgAction, 'PrevChapter', 'PrevChapter', None, 0x34),
        (MsgAction, 'NextChapter', 'NextChapter', None, 0x35),
        (MsgAction, 'RootMenu', 'RootMenu', None, 0x36),
        (MsgAction, 'TitleMenu', 'TitleMenu', None, 0x37),
        (MsgAction, 'SubpictureMenu', 'SubpictureMenu', None, 0x38),
        (MsgAction, 'AudioMenu', 'AudioMenu', None, 0x39),
        (MsgAction, 'AngleMenu', 'AngleMenu', None, 0x3A),
        (MsgAction, 'ChapterMenu', 'ChapterMenu', None, 0x3B),
        (MsgAction, 'RestoreMenu', 'RestoreMenu', None, 0x3C),
        (MsgAction, 'ClosedCaption', 'ClosedCaption', None, 0x3D),
        (MsgAction, '1XBackward', '1XBackward', None, 0x3E),
        (MsgAction, '2XBackward', '2XBackward', None, 0x3F),
        (MsgAction, '4XBackward', '4XBackward', None, 0x40),
        (MsgAction, '8XBackward', '8XBackward', None, 0x41),
        (MsgAction, '1XForeward', '1XForeward', None, 0x42),
        (MsgAction, '2XForeward', '2XForeward', None, 0x43),
        (MsgAction, '4XForeward', '4XForeward', None, 0x44),
        (MsgAction, '8XForeward', '8XForeward', None, 0x45),
        (MsgAction, 'RelativeButton', 'RelativeButton', None, 0x210000),
        (MsgAction, 'ActivateButton', 'ActivateButton', None, 0x210001),
        (MsgAction, 'GetSelectedButton', 'GetSelectedButton', None, 0x210002),
        (MsgAction, 'Menu', 'Menu', None, 0xA),
    )),
    (eg.ActionGroup, 'Winamp', 'Winamp', None, (
        (MsgAction, 'PluginSetup', 'PluginSetup', None, 0x46),
        (MsgAction, 'PluginInfo', 'PluginInfo', None, 0x47),
        (MsgAction, 'FileInfo', 'FileInfo', None, 0x48),
        (MsgAction, 'MediaLib', 'MediaLib', None, 0x29F),
        (MsgAction, 'Menu', 'Menu', None, 0xB),
    )),
    (eg.ActionGroup, 'Screen', 'Screen', None, (
        (MsgAction, 'KeepBaseRatio', 'KeepBaseRatio', None, 0x49),
        (MsgAction, 'Keep43Ratio', 'Keep43Ratio', None, 0x4A),
        (MsgAction, 'Keep169Ratio', 'Keep169Ratio', None, 0x4B),
        (MsgAction, 'Keep235Ratio', 'Keep235Ratio', None, 0x124B),
        (MsgAction, 'KeepCurRatio', 'KeepCurRatio', None, 0x4C),
        (MsgAction, 'CycleRatio', 'CycleRatio', None, 0x304C),
        (MsgAction, 'MinSize', 'MinSize', None, 0x704D),
        (MsgAction, 'VisOn', 'VisOn', None, 0x704E),
        (MsgAction, 'VisOff', 'VisOff', None, 0x704F),
        (MsgAction, 'HalfSize', 'HalfSize', None, 0x4D),
        (MsgAction, 'NormalSize', 'NormalSize', None, 0x4F),
        (MsgAction, 'DoubleSize', 'DoubleSize', None, 0x2046),
        (MsgAction, 'MaxSize', 'MaxSize', None, 0x2047),
        (MsgAction, 'RestoreSize', 'RestoreSize', None, 0x3047),
        (MsgAction, 'FullSize', 'FullSize', None, 0x2048),
        (MsgAction, 'DesktopView', 'DesktopView', None, 0x2166),
        (MsgAction, 'WideSize', 'WideSize', None, 0x2266),
        (MsgAction, 'TopLeft', 'TopLeft', None, 0x2049),
        (MsgAction, 'TopCenter', 'TopCenter', None, 0x204A),
        (MsgAction, 'TopRight', 'TopRight', None, 0x204B),
        (MsgAction, 'MiddleLeft', 'MiddleLeft', None, 0x204C),
        (MsgAction, 'MiddleCenter', 'MiddleCenter', None, 0x204D),
        (MsgAction, 'MiddleRight', 'MiddleRight', None, 0x204E),
        (MsgAction, 'BottomLeft', 'BottomLeft', None, 0x204F),
        (MsgAction, 'BottomCenter', 'BottomCenter', None, 0x50),
        (MsgAction, 'BottomRight', 'BottomRight', None, 0x51),
        (MsgAction, 'AllwaysOnTop', 'AllwaysOnTop', None, 0x52),
        (MsgAction, 'PlayingOnTop', 'PlayingOnTop', None, 0x53),
        (MsgAction, 'ScreenSave', 'ScreenSave', None, 0x54),
        (MsgAction, 'HideMouse', 'HideMouse', None, 0x55),
        (MsgAction, 'Menu', 'Menu', None, 0xC),
    )),
    (eg.ActionGroup, 'AdvScreen', 'AdvScreen', None, (
        (MsgAction, 'Restore', 'Restore', None, 0x56),
        (MsgAction, 'ZoomIn', 'ZoomIn', None, 0x57),
        (MsgAction, 'ZoomOut', 'ZoomOut', None, 0x58),
        (MsgAction, 'ZoomInHori', 'ZoomInHori', None, 0x59),
        (MsgAction, 'ZoomOutHori', 'ZoomOutHori', None, 0x5A),
        (MsgAction, 'ZoomInVert', 'ZoomInVert', None, 0x5B),
        (MsgAction, 'ZoomOutVert', 'ZoomOutVert', None, 0x5C),
        (MsgAction, 'MoveLeft', 'MoveLeft', None, 0x5D),
        (MsgAction, 'MoveRight', 'MoveRight', None, 0x5E),
        (MsgAction, 'MoveUp', 'MoveUp', None, 0x5F),
        (MsgAction, 'MoveDown', 'MoveDown', None, 0x60),
        (MsgAction, 'Offset', 'Offset', None, 0x61),
        (MsgAction, 'Menu', 'Menu', None, 0xD),
    )),
    (eg.ActionGroup, 'Play', 'Play', None, (
        (MsgAction, 'PlayPause', 'PlayPause', None, 0x7061),
        (MsgAction, 'PausePlay', 'PausePlay', None, 0x7062),
        (MsgAction, 'Play', 'Play', None, 0x62),
        (MsgAction, 'Stop', 'Stop', None, 0x63),
        (MsgAction, 'Frame', 'Frame', None, 0x64),
        (MsgAction, 'PrevFile', 'PrevFile', None, 0x65),
        (MsgAction, 'NextFile', 'NextFile', None, 0x66),
        (MsgAction, 'Backward1', 'Backward1', None, 0x67),
        (MsgAction, 'Forward1', 'Forward1', None, 0x68),
        (MsgAction, 'Backward2', 'Backward2', None, 0x69),
        (MsgAction, 'Forward2', 'Forward2', None, 0x6A),
        (MsgAction, 'Backward3', 'Backward3', None, 0x6B),
        (MsgAction, 'Forward3', 'Forward3', None, 0x6C),
        (MsgAction, 'Backward4', 'Backward4', None, 0x6D),
        (MsgAction, 'Forward4', 'Forward4', None, 0x6E),
        (MsgAction, 'PrevCap', 'PrevCap', None, 0x6F),
        (MsgAction, 'NextCap', 'NextCap', None, 0x70),
        (MsgAction, 'StartPos', 'StartPos', None, 0x71),
        (MsgAction, 'MidPos', 'MidPos', None, 0x72),
        (MsgAction, 'LastPos', 'LastPos', None, 0x73),
        (MsgAction, 'SlowerSpeed', 'SlowerSpeed', None, 0x74),
        (MsgAction, 'NormalSpeed', 'NormalSpeed', None, 0x75),
        (MsgAction, 'FasterSpeed', 'FasterSpeed', None, 0x76),
        (MsgAction, 'SlowerPitch', 'SlowerPitch', None, 0x77),
        (MsgAction, 'NormalPitch', 'NormalPitch', None, 0x78),
        (MsgAction, 'FasterPitch', 'FasterPitch', None, 0x79),
        (MsgAction, 'RepeatMenu', 'RepeatMenu', None, 0x7A),
        (MsgAction, 'RepeatSet', 'RepeatSet', None, 0x307A),
        (MsgAction, 'RepeatStart', 'RepeatStart', None, 0x307B),
        (MsgAction, 'RepeatEnd', 'RepeatEnd', None, 0x307C),
        (MsgAction, 'RepeatUse', 'RepeatUse', None, 0x307D),
        (MsgAction, 'ModeMenu', 'ModeMenu', None, 0x7B),
        (MsgAction, 'ModeDirDown', 'ModeDirDown', None, 0x307E),
        (MsgAction, 'ModeDirUp', 'ModeDirUp', None, 0x307F),
        (MsgAction, 'ModeDirRandom', 'ModeDirRandom', None, 0x3080),
        (MsgAction, 'ModeDirRepeat', 'ModeDirRepeat', None, 0x3081),
        (MsgAction, 'ModeAlbumNext', 'ModeAlbumNext', None, 0x3082),
        (MsgAction, 'ModeAlbumRepeat', 'ModeAlbumRepeat', None, 0x3083),
        (MsgAction, 'ModeAlbumNone', 'ModeAlbumNone', None, 0x3084),
        (MsgAction, 'ModeAlbumExit', 'ModeAlbumExit', None, 0x3085),
        (MsgAction, 'ModeAlbumPowerOff', 'ModeAlbumPowerOff', None, 0x3086),
        (MsgAction, 'ModeAlbumFileClose', 'ModeAlbumFileClose', None, 0x3087),
        (MsgAction, 'MoveMenu', 'MoveMenu', None, 0x3088),
        (MsgAction, 'SkipStart', 'SkipStart', None, 0x3089),
        (MsgAction, 'SkipIntro', 'SkipIntro', None, 0x308C),
        (MsgAction, 'SkipEnd', 'SkipEnd', None, 0x309A),
        (MsgAction, 'SkipSetting', 'SkipSetting', None, 0x309B),
        (MsgAction, 'SaveFilePos', 'SaveFilePos', None, 0x309C),
        (MsgAction, 'UseAVIKeyFrame', 'UseAVIKeyFrame', None, 0x309D),
        (MsgAction, 'InfoView', 'InfoView', None, 0x16B),
        (MsgAction, 'Menu', 'Menu', None, 0xE),
    )),
    (eg.ActionGroup, 'Caption', 'Caption', None, (
        (MsgAction, 'FileOpen', 'FileOpen', None, 0x7C),
        (MsgAction, 'Visible', 'Visible', None, 0x7D),
        (MsgAction, 'SyncInput', 'SyncInput', None, 0x7E),
        (MsgAction, 'SyncPrev', 'SyncPrev', None, 0x7F),
        (MsgAction, 'SyncNext', 'SyncNext', None, 0x80),
        (MsgAction, 'Overlay', 'Overlay', None, 0x81),
        (MsgAction, 'Image', 'Image', None, 0x82),
        (MsgAction, 'AlignMenu', 'AlignMenu', None, 0x83),
        (MsgAction, 'AlignLeft', 'AlignLeft', None, 0x84),
        (MsgAction, 'AlignCenter', 'AlignCenter', None, 0x85),
        (MsgAction, 'AlignRight', 'AlignRight', None, 0x86),
        (MsgAction, 'AlignTop', 'AlignTop', None, 0x2084),
        (MsgAction, 'AlignMiddle', 'AlignMiddle', None, 0x2085),
        (MsgAction, 'AlignBottom', 'AlignBottom', None, 0x2086),
        (MsgAction, 'LanguageMenu', 'LanguageMenu', None, 0x87),
        (MsgAction, 'MarginMenu', 'MarginMenu', None, 0x88),
        (MsgAction, 'Margin0', 'Margin0', None, 0x89),
        (MsgAction, 'Margin5', 'Margin5', None, 0x8A),
        (MsgAction, 'Margin10', 'Margin10', None, 0x8B),
        (MsgAction, 'Margin15', 'Margin15', None, 0x8C),
        (MsgAction, 'Margin20', 'Margin20', None, 0x8D),
        (MsgAction, 'Margin25', 'Margin25', None, 0x8E),
        (MsgAction, 'Margin30', 'Margin30', None, 0x8F),
        (MsgAction, 'Larger', 'Larger', None, 0x90),
        (MsgAction, 'Smaller', 'Smaller', None, 0x91),
        (MsgAction, 'Normal', 'Normal', None, 0x92),
        (MsgAction, 'Bold', 'Bold', None, 0x93),
        (MsgAction, 'Itialic', 'Itialic', None, 0x94),
        (MsgAction, 'Alpha', 'Alpha', None, 0x95),
        (MsgAction, 'Underline', 'Underline', None, 0x96),
        (MsgAction, 'Fade', 'Fade', None, 0x97),
        (MsgAction, 'Shadow', 'Shadow', None, 0x98),
        (MsgAction, 'Outline', 'Outline', None, 0x99),
        (MsgAction, 'Vert', 'Vert', None, 0x9A),
        (MsgAction, 'Antialias', 'Antialias', None, 0x9B),
        (MsgAction, 'HTML', 'HTML', None, 0x9C),
        (MsgAction, 'MoveDown', 'MoveDown', None, 0x9D),
        (MsgAction, 'MoveUp', 'MoveUp', None, 0x9E),
        (MsgAction, 'IncMargin', 'IncMargin', None, 0x9F),
        (MsgAction, 'DecMargin', 'DecMargin', None, 0x1100),
        (MsgAction, 'Menu', 'Menu', None, 0xF),
    )),
    (eg.ActionGroup, 'Video', 'Video', None, (
        (MsgAction, 'DecBaseBright', 'DecBaseBright', None, 0x1101),
        (MsgAction, 'IncBaseBright', 'IncBaseBright', None, 0x1102),
        (MsgAction, 'MotionBlur', 'MotionBlur', None, 0x1103),
        (MsgAction, 'LPFilter', 'LPFilter', None, 0x1104),
        (MsgAction, 'SharpenFilter', 'SharpenFilter', None, 0x1105),
        (MsgAction, 'MediaBlock', 'MediaBlock', None, 0x1106),
        (MsgAction, 'MediaCross', 'MediaCross', None, 0x1107),
        (MsgAction, 'MeanYFilter', 'MeanYFilter', None, 0x1108),
        (MsgAction, 'MeanUVFilter', 'MeanUVFilter', None, 0x1109),
        (MsgAction, 'GreyScale', 'GreyScale', None, 0x110A),
        (MsgAction, 'AutoLevel', 'AutoLevel', None, 0x110B),
        (MsgAction, 'Mirror', 'Mirror', None, 0x110C),
        (MsgAction, 'InInverse', 'InInverse', None, 0x110D),
        (MsgAction, 'OutInverse', 'OutInverse', None, 0x110E),
        (MsgAction, 'SpecialFilterMenu', 'SpecialFilterMenu', None, 0x210F),
        (MsgAction, 'HPFilter', 'HPFilter', None, 0x2110),
        (MsgAction, 'Laplace', 'Laplace', None, 0x2101),
        (MsgAction, 'EdgeDetect', 'EdgeDetect', None, 0x2102),
        (MsgAction, 'EdgeEnhance', 'EdgeEnhance', None, 0x2103),
        (MsgAction, 'ColorEmboss', 'ColorEmboss', None, 0x2104),
        (MsgAction, 'ColorInverse', 'ColorInverse', None, 0x2105),
        (MsgAction, 'Histogram', 'Histogram', None, 0x2106),
        (MsgAction, 'IgnoreSetting', 'IgnoreSetting', None, 0x2107),
        (MsgAction, 'UsePlugin', 'UsePlugin', None, 0x2108),
        (MsgAction, 'Menu', 'Menu', None, 0x10),
    )),
    (eg.ActionGroup, 'AdvVideo', 'AdvVideo', None, (
        (MsgAction, 'LowUseOverSample', 'LowUseOverSample', None, 0x3109),
        (MsgAction, 'AllUseOverSample', 'AllUseOverSample', None, 0x310A),
        (MsgAction, 'NoUseOverSample', 'NoUseOverSample', None, 0x310B),
        (MsgAction, 'DeInterlace', 'DeInterlace', None, 0x310C),
        (MsgAction, 'PostProcess', 'PostProcess', None, 0x310D),
        (MsgAction, 'PicProperty', 'PicProperty', None, 0x310E),
        (MsgAction, 'Sharpen', 'Sharpen', None, 0x310F),
        (MsgAction, 'Blur', 'Blur', None, 0x3110),
        (MsgAction, 'GDeNoise', 'GDeNoise', None, 0x3111),
        (MsgAction, 'LevelControl', 'LevelControl', None, 0x3112),
        (MsgAction, 'FastestMode', 'FastestMode', None, 0x3113),
        (MsgAction, 'FastPreset', 'FastPreset', None, 0x3114),
        (MsgAction, 'HQPreset', 'HQPreset', None, 0x3115),
        (MsgAction, 'BasePreset', 'BasePreset', None, 0x3116),
        (MsgAction, 'HardwareMenu', 'HardwareMenu', None, 0x3117),
        (MsgAction, 'SoftwareMenu', 'SoftwareMenu', None, 0x3118),
        (MsgAction, 'HWIncBright', 'HWIncBright', None, 0x3119),
        (MsgAction, 'HWBaseBright', 'HWBaseBright', None, 0x311A),
        (MsgAction, 'HWDecBright', 'HWDecBright', None, 0x311B),
        (MsgAction, 'HWIncSaturat', 'HWIncSaturat', None, 0x311C),
        (MsgAction, 'HWBaseSaturat', 'HWBaseSaturat', None, 0x311D),
        (MsgAction, 'HWDecSaturat', 'HWDecSaturat', None, 0x311E),
        (MsgAction, 'HWIncContrast', 'HWIncContrast', None, 0x311F),
        (MsgAction, 'HWBaseContrast', 'HWBaseContrast', None, 0x3120),
        (MsgAction, 'HWDecContrast', 'HWDecContrast', None, 0x3121),
        (MsgAction, 'SWIncBright', 'SWIncBright', None, 0x3122),
        (MsgAction, 'SWBaseBright', 'SWBaseBright', None, 0x3123),
        (MsgAction, 'SWDecBright', 'SWDecBright', None, 0x3124),
        (MsgAction, 'SWIncSaturat', 'SWIncSaturat', None, 0x3125),
        (MsgAction, 'SWBaseSaturat', 'SWBaseSaturat', None, 0x3126),
        (MsgAction, 'SWDecSaturat', 'SWDecSaturat', None, 0x3127),
        (MsgAction, 'SWIncContrast', 'SWIncContrast', None, 0x3128),
        (MsgAction, 'SWBaseContrast', 'SWBaseContrast', None, 0x3129),
        (MsgAction, 'SWDecContrast', 'SWDecContrast', None, 0x312A),
        (MsgAction, 'Menu', 'Menu', None, 0x11),
    )),
    (eg.ActionGroup, 'Audio', 'Audio', None, (
        (MsgAction, 'IncVolume', 'IncVolume', None, 0x12C),
        (MsgAction, 'DecVolume', 'DecVolume', None, 0x12D),
        (MsgAction, 'MuteVolume', 'MuteVolume', None, 0x12E),
        (MsgAction, 'DecAmp', 'DecAmp', None, 0x12F),
        (MsgAction, 'IncAmp', 'IncAmp', None, 0x130),
        (MsgAction, 'UseEqulizer', 'UseEqulizer', None, 0x131),
        (MsgAction, 'EqulizerPresetMenu', 'EqulizerPresetMenu', None, 0x132),
        (MsgAction, 'EqulizerFreqDomain', 'EqulizerFreqDomain', None, 0x2132),
        (MsgAction, 'EqulizerTimeDomain', 'EqulizerTimeDomain', None, 0x2133),
        (MsgAction, 'EqulizerDirectX', 'EqulizerDirectX', None, 0x2134),
        (MsgAction, 'RemoveLeftCh', 'RemoveLeftCh', None, 0x133),
        (MsgAction, 'RemoveRightCh', 'RemoveRightCh', None, 0x134),
        (MsgAction, 'SwapCh', 'SwapCh', None, 0x135),
        (MsgAction, 'MergeCh', 'MergeCh', None, 0x136),
        (MsgAction, 'VioceRemove', 'VioceRemove', None, 0x137),
        (MsgAction, 'ViocePass', 'ViocePass', None, 0x138),
        (MsgAction, 'UseDynamicAmp', 'UseDynamicAmp', None, 0x2138),
        (MsgAction, 'UseAutoGain', 'UseAutoGain', None, 0x3310),
        (MsgAction, 'UseEcho', 'UseEcho', None, 0x2139),
        (MsgAction, 'SlowerEcho', 'SlowerEcho', None, 0x139),
        (MsgAction, 'FasterEcho', 'FasterEcho', None, 0x13A),
        (MsgAction, 'UseBandPass', 'UseBandPass', None, 0x223A),
        (MsgAction, 'UseTrueBass', 'UseTrueBass', None, 0x223B),
        (MsgAction, 'UseTrebleEhn', 'UseTrebleEhn', None, 0x223C),
        (MsgAction, 'UseTempo', 'UseTempo', None, 0x23A),
        (MsgAction, 'SlowerPitch', 'SlowerPitch', None, 0x14B),
        (MsgAction, 'FasterPitch', 'FasterPitch', None, 0x14C),
        (MsgAction, 'Use3DEffect', 'Use3DEffect', None, 0x14D),
        (MsgAction, 'Dec3DEffect', 'Dec3DEffect', None, 0x14E),
        (MsgAction, 'Inc3DEffect', 'Inc3DEffect', None, 0x14F),
        (MsgAction, 'IgnoreSetting', 'IgnoreSetting', None, 0x150),
        (MsgAction, 'UsePlugin', 'UsePlugin', None, 0x151),
        (MsgAction, 'Menu', 'Menu', None, 0x12),
    )),
    (eg.ActionGroup, 'Capture', 'Capture', None, (
        (MsgAction, 'AVIMovie', 'AVIMovie', None, 0x152),
        (MsgAction, 'AVIAuto', 'AVIAuto', None, 0x153),
        (MsgAction, 'CurScrFile', 'CurScrFile', None, 0x154),
        (MsgAction, 'CurScrTime', 'CurScrTime', None, 0x155),
        (MsgAction, 'CurScrClipBoard', 'CurScrClipBoard', None, 0x156),
        (MsgAction, 'SampleGrabber', 'SampleGrabber', None, 0x157),
        (MsgAction, 'DesktopCenter', 'DesktopCenter', None, 0x158),
        (MsgAction, 'DesktopTile', 'DesktopTile', None, 0x159),
        (MsgAction, 'DesktopStretch', 'DesktopStretch', None, 0x15A),
        (MsgAction, 'SelectFolder', 'SelectFolder', None, 0x15B),
        (MsgAction, 'OpenFolder', 'OpenFolder', None, 0x15C),
        (MsgAction, 'ClipToAVI', 'ClipToAVI', None, 0x24A),
        (MsgAction, 'Menu', 'Menu', None, 0x13),
    )),
    (eg.ActionGroup, 'Visual', 'Visual', None, (
        (MsgAction, 'WaveForm', 'WaveForm', None, 0x15D),
        (MsgAction, 'Freq', 'Freq', None, 0x15E),
        (MsgAction, 'WaveFreq', 'WaveFreq', None, 0x15F),
        (MsgAction, 'WinMediaVis', 'WinMediaVis', None, 0x160),
        (MsgAction, 'Simple', 'Simple', None, 0x161),
        (MsgAction, 'Black', 'Black', None, 0x162),
        (MsgAction, 'PrevVis', 'PrevVis', None, 0x163),
        (MsgAction, 'NextVis', 'NextVis', None, 0x164),
        (MsgAction, 'Menu', 'Menu', None, 0x14),
    )),
    (eg.ActionGroup, 'Skin', 'Skin', None, (
        (MsgAction, 'NormalControlSkin', 'NormalControlSkin', None, 0x16F),
        (MsgAction, 'AutoHideControlSkin', 'AutoHideControlSkin', None, 0x172),
        (MsgAction, 'OSCControlSkin', 'OSCControlSkin', None, 0x170),
        (MsgAction, 'BothControlSkin', 'BothControlSkin', None, 0x171),
        (MsgAction, 'Change', 'Change', None, 0x1171),
        (MsgAction, 'Menu', 'Menu', None, 0x18),
    )),
    (eg.ActionGroup, 'PlayList', 'PlayList', None, (
        (MsgAction, 'PopupMenu', 'PopupMenu', None, 0x190),
        (MsgAction, 'AddFileCmd', 'AddFileCmd', None, 0x191),
        (MsgAction, 'AddFolderCmd', 'AddFolderCmd', None, 0x192),
        (MsgAction, 'ClearAllCmd', 'ClearAllCmd', None, 0x193),
        (MsgAction, 'View', 'View', None, 0x168),
    )),
    (eg.ActionGroup, 'WDM', 'WDM', None, (
        (MsgAction, 'Channel0', 'Channel0', None, 0x294),
        (MsgAction, 'Channel1', 'Channel1', None, 0x295),
        (MsgAction, 'Channel2', 'Channel2', None, 0x296),
        (MsgAction, 'Channel3', 'Channel3', None, 0x297),
        (MsgAction, 'Channel4', 'Channel4', None, 0x298),
        (MsgAction, 'Channel5', 'Channel5', None, 0x299),
        (MsgAction, 'Channel6', 'Channel6', None, 0x29A),
        (MsgAction, 'Channel7', 'Channel7', None, 0x29B),
        (MsgAction, 'Channel8', 'Channel9', None, 0x29C),
        (MsgAction, 'Channel9', 'Channel9', None, 0x29D),
        (MsgAction, 'ChannelSet', 'ChannelSet', None, 0x29E),
        (MsgAction, 'TunerMag', 'TunerMag', None, 0x25),
        (MsgAction, 'ChannelMag', 'ChannelMag', None, 0x26),
        (MsgAction, 'FirstChannel', 'FirstChannel', None, 0x27),
        (MsgAction, 'PrevChannel', 'PrevChannel', None, 0x28),
        (MsgAction, 'NextChannel', 'NextChannel', None, 0x29),
        (MsgAction, 'LastChannel', 'LastChannel', None, 0x2A),
        (MsgAction, 'RegPrevChannel', 'RegPrevChannel', None, 0x2B),
        (MsgAction, 'RegNextChannel', 'RegNextChannel', None, 0x2C),
        (MsgAction, 'InputChannel', 'InputChannel', None, 0x2D),
        (MsgAction, 'AntennaInput', 'AntennaInput', None, 0x2E),
        (MsgAction, 'CableInput', 'CableInput', None, 0x2F),
        (MsgAction, 'Menu', 'Menu', None, 0x9),
    )),
    (eg.ActionGroup, 'Album', 'Album', None, (
        (MsgAction, 'PrevOpen', 'PrevOpen', None, 0x23),
        (MsgAction, 'NextOpen', 'NextOpen', None, 0x24),
        (MsgAction, 'Menu', 'Menu', None, 0x7),
    )),
    (eg.ActionGroup, 'Bookmark', 'Bookmark', None, (
        (MsgAction, 'Add', 'Add', None, 0x165),
        (MsgAction, 'Menu', 'Menu', None, 0x16),
    )),
    (eg.ActionGroup, 'ColorTheme', 'ColorTheme', None, (
        (MsgAction, 'Cycle', 'Cycle', None, 0x237),
        (MsgAction, 'Random', 'Random', None, 0x236),
        (MsgAction, 'Menu', 'Menu', None, 0x235),
    )),
    (eg.ActionGroup, 'Others', 'Others', None, (
        (ExeAction, 'Start', 'Start', None, None),
        (MsgAction, 'MainMenu', 'MainMenu', None, 0x1),
        (MsgAction, 'SystemMenu', 'SystemMenu', None, 0x2),
        (MsgAction, 'Min', 'Min', None, 0x3),
        (MsgAction, 'Max', 'Max', None, 0x4),
        (MsgAction, 'Exit', 'Exit', None, 0x5),
        (MsgAction, 'Close', 'Close', None, 0x8),
        (MsgAction, 'ConfigureView', 'ConfigureView', None, 0x167),
        (MsgAction, 'ControlBoxView', 'ControlBoxView', None, 0x169),
        (MsgAction, 'AdvMenuView', 'AdvMenuView', None, 0x16A),
        (MsgAction, 'HelpView', 'HelpView', None, 0x16C),
        (MsgAction, 'AboutView', 'AboutView', None, 0x16D),
        (MsgAction, 'ViewFileInfo', 'ViewFileInfo', None, 0x230),
        (MsgAction, 'SearchAnyFile', 'SearchAnyFile', None, 0x231),
        (MsgAction, 'FilterMenu', 'FilterMenu', None, 0x15),
        (MsgAction, 'EnvRestoreMenu', 'EnvRestoreMenu', None, 0x17),
        (GetAction, 'GetPlayMode', 'GetPlayMode', None, 0x220000),
        (GetAction, 'GetIsPopupMenu', 'GetIsPopupMenu', None, 0x220001),
    )),
)

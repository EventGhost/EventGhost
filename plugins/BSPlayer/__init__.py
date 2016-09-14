# -*- coding: utf-8 -*-
#
# plugins/BSlayer/__init__.py
#
# This file is a plugin for EventGhost.
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

eg.RegisterPlugin(
    name = "BSPlayer",
    author = "CHeitkamp",
    version = "1.0.1488",
    kind = "program",
    guid = "{AEBC185B-0F4D-4E3E-8C4E-7574C21C6BA2}",
    createMacrosOnAdd = True,
    description = (
        "Adds support functions to control BSPlayer."
    ),
    url = "http://www.eventghost.org/forum/",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAAZi"
        "S0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9oCBhEoHQNl"
        "kmEAAANISURBVDjLbZNPaCNlAMXf980kk++bTrJJJt0/tUnIdls1C7a49OBKD1pNYTUg"
        "7a0s4kXqoXgQSqke9KCHsrgXLdZAizepBIp/Liv4p4t2TaFaV3ezrIpp0rXZmG0zk8kk"
        "M5MZT8qy9cE7PPjxTu8RPKBMJiONj48/n0qlnlIUJU4IsTVNKxaLxU/X1tau7ezsePfz"
        "5P6Qy+UuKIry/p+6lfi1y2D7GOC5kO0WzjHbG4r3fV0oFF6en5///UhBPp+fqTX0974i"
        "J4RYPIF0tAe268F0XNTbNn7aP0B/o4JsjNYMw8hMT0//CAACAKyuro4ZHfvjzwMD4pNn"
        "BxFmEnTbRcNycWi5MBwPAb+EO/5juH3PkM8flzPJZPKjjY2NNs1ms5Qxdumqv08cGUhA"
        "7wJ3Oy6Kuo0v9pr4pKThs70mfrjXhu5R/ML7cK3eSU5OTr4GAMLs7OyI55Pe3FbTJAIL"
        "9bYDrXGAW3/rEBwLrmOj2hVx0m2BOhZaREQVAYySw2Q0Gl2iiUTi/B2mEs45no1QPCY0"
        "IZkavsymcXkkjKvPncGUsI/8eAqvnuZgcHFLjKDV7vQPDw/Hqd/vP94UOSwqAoTg4uOD"
        "SEUUXP6+iJrpoFytgYo+gBAU2xSGX4bnZzAgkkgkcoISQgxFBA5dAV0QeJ6Hu6YNVQ6g"
        "oplQQ0HchILXN0vInuJ4IUYRkHyQRQLP8wxqWdb1h6wDND0Kw+ni7Y0b6JUlvDiSwhNx"
        "FZwFcBoGLp4JQ+3haHY9DIgWmEC0arVaEkul0neMsb8eCR+efKfKYYkyes0mrnxTAQCY"
        "pAtTHcK7u004uxrqPb2Ywh9gjF0pFAqa0Gg0rImJCXqqU3/mZjgFNyCjw4Lo8BA6PASX"
        "KaASQ4eHYPMgHvY0XLBLZigYfGVmZmZXKJfL3tjY2M/Uap8d9plDezwGW5QgCvSIH3Xq"
        "mGoVu2Gl541cLpff3t52/5vy+vp6TNf1S2KATZd7B4XfpBgOBAYBHmKOjrS5j36z1ggG"
        "g29tbm5+MDc3Zx450+LiIh8dHX26Uqm8BOCcz+eLUkq7APY459+qqvrhysrK9eXlZft/"
        "3/ivFhYWAul0+piiKDIAt16v61tbW42lpSX7QfYf0q5gOg4gH2UAAAAASUVORK5CYII="
    ),
)


# changelog:
# 1.0 by CHeitkamp
#     - initial version

from eg.WinApi import FindWindow, SendMessageTimeout, WM_USER



# Based bsp.h
WM_BSP_CMD = WM_USER+2


BSP_ExitFScreen = 0
BSP_VolUp = 1
BSP_VolDown = 2
BSP_DeDynUp = 3
BSP_DeDynPreUp = 4
BSP_DeDynDown = 5
BSP_DeDynPreDown = 6
BSP_Preferences = 7
BSP_FrmCapture = 8
BSP_Frm2 = 9
BSP_FS_Switch = 10
BSP_SubsEnDi = 11
BSP_Skins = 12
BSP_AStrmVolCyc = 13
BSP_Rew = 14
BSP_Forw = 15
BSP_SubCorInc = 16
BSP_SubCorDec = 17
BSP_SubCorIncS = 18
BSP_SubCorDecS = 19
BSP_Play = 20
BSP_Pause = 21
BSP_Stop = 22
BSP_ViewChp = 23
BSP_VBlankSwitch = 24
BSP_Prev = 25
BSP_PrevCh = 26
BSP_PrevCD = 27
BSP_Next = 28
BSP_NextCh = 29
BSP_NextCD = 30
BSP_ATop = 31
BSP_OvrTop = 32
BSP_AspCyc = 33
BSP_PlayList = 34
BSP_Mute = 35
BSP_JumpToTime = 36
BSP_Zoom50 = 37
BSP_Zoom100 = 38
BSP_Zoom200 = 39
BSP_AspOrg = 40
BSP_Asp169 = 41
BSP_Asp43 = 42
BSP_FSSW640 = 43
BSP_FSSW800 = 44
BSP_VInf = 45
BSP_PanIn = 46
BSP_PanOut = 47
BSP_ZoomIn = 48
BSP_ZoomOut = 49
BSP_MoveLeft = 50
BSP_MoveRight = 51
BSP_MoveUp = 52
BSP_MoveDown = 53
BSP_FRSizeLeft = 54
BSP_FRSizeRight = 55
BSP_FRSizeUp = 56
BSP_FRSizeDown = 57
BSP_ResetMov = 58
BSP_HideCtrl = 59
BSP_EQ = 60
BSP_OpenAud = 61
BSP_OpenSub = 62
BSP_OpenMov = 63
BSP_PanScan = 64
BSP_CusPanScan = 65
BSP_DeskMode = 66
BSP_AddBk = 67
BSP_EditBK = 68
BSP_SkinRefr = 69
BSP_About = 70
BSP_CycleAS = 71
BSP_CycleSub = 72
BSP_IncPBRate = 73
BSP_DecPBRate = 74
BSP_IncPP = 75
BSP_DecPP = 76
BSP_Exit = 77
BSP_CloseM = 78
BSP_JumpF = 79
BSP_JumpB = 80
BSP_ChBordEx = 81
BSP_CycleVid = 82
BSP_IncFnt = 83
BSP_DecFnt = 84
BSP_IncBri = 85
BSP_DecBri = 86
BSP_MovSubUp = 87
BSP_MovSubDown = 88
BSP_SHTime = 89
BSP_IncBriHW = 90
BSP_DecBriHW = 91
BSP_IncConHW = 92
BSP_DecConHW = 93
BSP_IncHueHW = 94
BSP_DecHueHW = 95
BSP_IncSatHW = 96
BSP_DecSatHW = 97
BSP_ShowHWClr = 98
BSP_IncMovWin = 99
BSP_DecMovWin = 100
BSP_IncPBRate1 = 101
BSP_DecPBRate1 = 102
BSP_SWRepeat = 103
BSP_SWDispFmt = 104
BSP_FastForw = 105
BSP_FastRew = 106
BSP_BossBtn = 107
BSP_MediaLib = 108
BSP_OpenURL = 109
BSP_Minimize = 110
BSP_ShowMenu = 111
BSP_LoadSwSub = 112
BSP_CycleSubR = 113
BSP_SubNextFnt = 114
BSP_SubPrevFnt = 115
BSP_AspCycR = 116
BSP_DVDTitle = 117
BSP_DVDChapter = 118
BSP_DVDSub = 119
BSP_DVDLang = 120
BSP_Res8 = 121
BSP_Res9 = 122

BSP_ML_VIDEO = 6500
BSP_ML_DVD = 6501
BSP_ML_AUDIO = 6502
BSP_ML_RADIO = 6503

BSP_GETVERSION = 0x10000
BSP_GetMovLen = 0x10100
BSP_GetMovPos = 0x10101
BSP_GetStatus = 0x10102
BSP_Seek = 0x10103
BSP_SetVol = 0x10104
BSP_GetVol = 0x10105
BSP_SetSkin = 0x10106
BSP_GetSkin = 0x10107
BSP_OpenFile = 0x10108
BSP_LoadSub = 0x10109
BSP_LoadAudio = 0x1010A
BSP_GetFileName = 0x1010B
BSP_LoadPlaylist = 0x1010C
BSP_LoadPlaylistInt = 0x1010D



ACTIONS = (
    ( eg.ActionGroup, 'GroupMainControls', 'Main controls', None, (
        ( 'Play', 'Play', None, BSP_Play ),
        ( 'Pause', 'Pause', None, BSP_Pause ),
        ( 'Stop', 'Stop', None, BSP_Stop ),
        ( 'VolumeUp', 'Volume Up', None, BSP_VolUp ),
        ( 'VolumeDown', 'Volume Down', None, BSP_VolDown ),
        ( 'VolumeMute', 'Volume Mute', None, BSP_Mute ),
        ( 'BossKey', 'Boss Key', None, BSP_BossBtn ),
        ( 'Next', 'Next', None, BSP_Next ),
        ( 'Previous', 'Previous', None, BSP_Prev ),
        ( 'Exit', 'Quit Application', None, BSP_Exit ),
    ) ),
)


class ActionPrototype(eg.ActionClass):

    def __call__(self):
        try:
            hWnd = FindWindow( "BSPlayer" )
            return SendMessageTimeout(hWnd, WM_BSP_CMD, self.value, 0)
        except:
            raise self.Exceptions.ProgramNotRunning


class BSPlayer(eg.PluginClass):

    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)

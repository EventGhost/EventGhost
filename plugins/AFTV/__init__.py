# -*- coding: utf-8 -*-
import eg

eg.RegisterPlugin(
    name="Amazon FireTV",
    guid='{56E98168-ED7D-4379-B434-7026F1C14140}',
    author="Eric Fetty",
    version="0.0.1",
    kind="other",
    description="Issues controller commands to a FireTV using ADB.")

import subprocess

global adbPath
global aftvString


class AFTVPlugin(eg.PluginBase):
    def __init__(self):
        self.AddAction(HOME)
        self.AddAction(BACK)
        self.AddAction(UP)
        self.AddAction(DOWN)
        self.AddAction(LEFT)
        self.AddAction(RIGHT)
        self.AddAction(SELECT)
        self.AddAction(MENU)
        self.AddAction(POWER)
        self.AddAction(CheckStatus)

    def __start__(self, aftvString, adbPath):
        self.adbPath = str(adbPath)
        self.aftvString = str(aftvString)
        subprocess.Popen([adbPath, 'connect', aftvString], shell=True, creationflags=subprocess.SW_HIDE)

    def __stop__(self):
        subprocess.Popen([self.adbPath, 'disconnect', self.aftvString], shell=True, creationflags=subprocess.SW_HIDE)

    def Configure(self, aftvString="", adbPath=""):
        panel = eg.ConfigPanel()
        aftvStringEdit = panel.TextCtrl(aftvString)
        # adbPathEdit=panel.TextCtrl(adbPath)
        adbPathEdit = MyFileBrowseButton(
            panel,
            buttonText=eg.text.General.browse,
            fileMask='*.exe')
        panel.AddLine("Amazon FireTV IP : ", aftvStringEdit)
        panel.AddLine("ADB Executable Location : ", adbPathEdit)
        while panel.Affirmed():
            panel.SetResult(aftvStringEdit.GetValue(), adbPathEdit.GetValue())


class MENU(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath, 'shell', 'input', 'keyevent', '1'], shell=True,
                         creationflags=subprocess.SW_HIDE)


class HOME(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath, 'shell', 'input', 'keyevent', '3'], shell=True,
                         creationflags=subprocess.SW_HIDE)


class BACK(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath, 'shell', 'input', 'keyevent', '4'], shell=True,
                         creationflags=subprocess.SW_HIDE)


class UP(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath, 'shell', 'input', 'keyevent', '19'], shell=True,
                         creationflags=subprocess.SW_HIDE)


class DOWN(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath, 'shell', 'input', 'keyevent', '20'], shell=True,
                         creationflags=subprocess.SW_HIDE)


class LEFT(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath, 'shell', 'input', 'keyevent', '21'], shell=True,
                         creationflags=subprocess.SW_HIDE)


class RIGHT(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath, 'shell', 'input', 'keyevent', '22'], shell=True,
                         creationflags=subprocess.SW_HIDE)


class SELECT(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath, 'shell', 'input', 'keyevent', '23'], shell=True,
                         creationflags=subprocess.SW_HIDE)


class POWER(eg.ActionBase):
    def __call__(self):
        subprocess.Popen([self.plugin.adbPath, 'shell', 'input', 'keyevent', '26'], shell=True,
                         creationflags=subprocess.SW_HIDE)


class CheckStatus(eg.ActionBase):
    def __call__(self):
        proc = subprocess.Popen([self.plugin.adbPath, 'shell', 'dumpsys', 'power', '|', 'grep', 'mScreenOn'],
                                shell=True, stdout=subprocess.PIPE, creationflags=subprocess.SW_HIDE)
        status = proc.stdout.readline().strip()
        # eg.TriggerEvent("Status",prefix="AFTV",payload=status)
        if "true" in status:
            eg.TriggerEvent("PowerOn", prefix="AFTV")
        else:
            eg.TriggerEvent("PowerOff", prefix="AFTV")


class MyFileBrowseButton(eg.FileBrowseButton):
    def GetTextCtrl(self):
        return self.textControl

# 4 --> "KEYCODE_BACK"
# 5 --> "KEYCODE_CALL"
# 6 --> "KEYCODE_ENDCALL"
# 7 --> "KEYCODE_0"
# 8 --> "KEYCODE_1"
# 9 --> "KEYCODE_2"
# 10 --> "KEYCODE_3"
# 11 --> "KEYCODE_4"
# 12 --> "KEYCODE_5"
# 13 --> "KEYCODE_6"
# 14 --> "KEYCODE_7"
# 15 --> "KEYCODE_8"
# 16 --> "KEYCODE_9"
# 17 --> "KEYCODE_STAR"
# 18 --> "KEYCODE_POUND"
# 19 --> "KEYCODE_DPAD_UP"
# 20 --> "KEYCODE_DPAD_DOWN"
# 21 --> "KEYCODE_DPAD_LEFT"
# 22 --> "KEYCODE_DPAD_RIGHT"
# 23 --> "KEYCODE_DPAD_CENTER"
# 24 --> "KEYCODE_VOLUME_UP"
# 25 --> "KEYCODE_VOLUME_DOWN"
# 26 --> "KEYCODE_POWER"
# 27 --> "KEYCODE_CAMERA"
# 28 --> "KEYCODE_CLEAR"
# 29 --> "KEYCODE_A"
# 30 --> "KEYCODE_B"
# 31 --> "KEYCODE_C"
# 32 --> "KEYCODE_D"
# 33 --> "KEYCODE_E"
# 34 --> "KEYCODE_F"
# 35 --> "KEYCODE_G"
# 36 --> "KEYCODE_H"
# 37 --> "KEYCODE_I"
# 38 --> "KEYCODE_J"
# 39 --> "KEYCODE_K"
# 40 --> "KEYCODE_L"
# 41 --> "KEYCODE_M"
# 42 --> "KEYCODE_N"
# 43 --> "KEYCODE_O"
# 44 --> "KEYCODE_P"
# 45 --> "KEYCODE_Q"
# 46 --> "KEYCODE_R"
# 47 --> "KEYCODE_S"
# 48 --> "KEYCODE_T"
# 49 --> "KEYCODE_U"
# 50 --> "KEYCODE_V"
# 51 --> "KEYCODE_W"
# 52 --> "KEYCODE_X"
# 53 --> "KEYCODE_Y"
# 54 --> "KEYCODE_Z"
# 55 --> "KEYCODE_COMMA"
# 56 --> "KEYCODE_PERIOD"
# 57 --> "KEYCODE_ALT_LEFT"
# 58 --> "KEYCODE_ALT_RIGHT"
# 59 --> "KEYCODE_SHIFT_LEFT"
# 60 --> "KEYCODE_SHIFT_RIGHT"
# 61 --> "KEYCODE_TAB"
# 62 --> "KEYCODE_SPACE"
# 63 --> "KEYCODE_SYM"
# 64 --> "KEYCODE_EXPLORER"
# 65 --> "KEYCODE_ENVELOPE"
# 66 --> "KEYCODE_ENTER"
# 67 --> "KEYCODE_DEL"
# 68 --> "KEYCODE_GRAVE"
# 69 --> "KEYCODE_MINUS"
# 70 --> "KEYCODE_EQUALS"
# 71 --> "KEYCODE_LEFT_BRACKET"
# 72 --> "KEYCODE_RIGHT_BRACKET"
# 73 --> "KEYCODE_BACKSLASH"
# 74 --> "KEYCODE_SEMICOLON"
# 75 --> "KEYCODE_APOSTROPHE"
# 76 --> "KEYCODE_SLASH"
# 77 --> "KEYCODE_AT"
# 78 --> "KEYCODE_NUM"
# 79 --> "KEYCODE_HEADSETHOOK"
# 80 --> "KEYCODE_FOCUS"
# 81 --> "KEYCODE_PLUS"
# 82 --> "KEYCODE_MENU"
# 83 --> "KEYCODE_NOTIFICATION"
# 84 --> "KEYCODE_SEARCH"
# 85 --> "TAG_LAST_KEYCODE"

# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright Â© 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

# If you set this be sure to turn down the polling speed to 3 seconds first.
# Otherwise it will flood the log.
_DEBUG = False
_DEBUG_FILTER = [2, 3, 4]

import eg # NOQA


eg.RegisterPlugin(
    name=u'XBox Controllers',
    author=u'K',
    version=u'1.9b',
    description=(
        u'This is an upgraded version of the XInput plugin by TheRetroPirate.'
        u'\n'
        u'\n'
        u'This version allows for these different controller types:<br><br>'
        u'GamePad<br>'
        u'Steering Wheel<br>'
        u'Flight Stick<br>'
        u'Guitar<br>'
        u'Bass Guitar<br>'
        u'Drums<br>'
        u'Dance Pad<br>'
        u'Arcade Stick<br>'
        u'Arcade Pad<br>'
        u'<br>'
        u'The plugin is also able to determine if the controller has '
        u'batteries and will generate battery events when the battery level '
        u'goes down or up. There is also an action to set the Force Feedback '
        u'(vibration) if the controller supports it.<br>'
        u'<br>'
        u'The plugin will automatically load the xinput 1.4 dll if your '
        u'Windows version is 8 or above. otherwise it will load the included '
        u'xinput 1.3 dll<br>'
    ),
    kind=u'remote',
    canMultiLoad=False,
    createMacrosOnAdd=True,
    guid=u'{72D8C9EA-FF9A-4884-8430-FE51D05B2E5C}'
)

import os # NOQA
import shutil # NOQA
import math # NOQA
import ctypes # NOQA
import time # NOQA
import threading # NOQA
import wx # NOQA
from math import hypot, atan2, degrees, sqrt # NOQA
from eg.WinApi.Dynamic import SetCursorPos, mouse_event # NOQA
from ctypes.wintypes import DWORD, WORD, BYTE, SHORT, WCHAR, POINTER # NOQA
from eg.WinApi.Utils import GetMonitorDimensions # NOQA

MOUSEEVENT_LEFTDOWN = 0x0002
MOUSEEVENT_LEFTUP = 0x0004
MOUSEEVENT_RIGHTDOWN = 0x0008
MOUSEEVENT_RIGHTUP = 0x0010
MOUSEEVENT_MIDDLEDOWN = 0x0020
MOUSEEVENT_MIDDLEUP = 0x0040
MOUSEEVENT_VWHEEL = 0x0800
MOUSEEVENT_HWHEEL = 0x01000

ERROR_SUCCESS = 0
ERROR_DEVICE_NOT_CONNECTED = 0x48F

XINPUT_CAPS_VOICE_SUPPORTED = 0x0004
XINPUT_CAPS_FFB_SUPPORTED = 0x0001
XINPUT_CAPS_WIRELESS = 0x0002
XINPUT_CAPS_NO_NAVIGATION = 0x0010


XINPUT_GAMEPAD_DPAD_UP = 0x0001
XINPUT_GAMEPAD_DPAD_DOWN = 0x0002
XINPUT_GAMEPAD_DPAD_LEFT = 0x0004
XINPUT_GAMEPAD_DPAD_RIGHT = 0x0008
XINPUT_GAMEPAD_START = 0x0010
XINPUT_GAMEPAD_BACK = 0x0020
XINPUT_GAMEPAD_LEFT_THUMB = 0x0040
XINPUT_GAMEPAD_RIGHT_THUMB = 0x0080
XINPUT_GAMEPAD_LEFT_SHOULDER = 0x0100
XINPUT_GAMEPAD_RIGHT_SHOULDER = 0x0200
XINPUT_GAMEPAD_A = 0x1000
XINPUT_GAMEPAD_B = 0x2000
XINPUT_GAMEPAD_X = 0x4000
XINPUT_GAMEPAD_Y = 0x8000

# output flags
XINPUT_FLAG_GAMEPAD = 0x00000001

# Wireless, connected devices with known battery types
# Battery devices
BATTERY_DEVTYPE_GAMEPAD = 0x00
BATTERY_DEVTYPE_HEADSET = 0x01

# Battery types
BATTERY_TYPE_DISCONNECTED = 0x00    # This device is not connected
BATTERY_TYPE_WIRED = 0x01    # Wired device, no battery
BATTERY_TYPE_ALKALINE = 0x02    # Alkaline battery source
BATTERY_TYPE_NIMH = 0x03    # Nickel Metal Hydride battery source
BATTERY_TYPE_UNKNOWN = 0xFF    # Cannot determine the battery type

# Battery level
BATTERY_LEVEL_EMPTY = 0x00
BATTERY_LEVEL_LOW = 0x01
BATTERY_LEVEL_MEDIUM = 0x02
BATTERY_LEVEL_FULL = 0x03


BATTERY_LEVELS = {
    BATTERY_LEVEL_EMPTY: 'BatteryLevel.Empty',
    BATTERY_LEVEL_LOW: 'BatteryLevel.Low',
    BATTERY_LEVEL_MEDIUM: 'BatteryLevel.Medium',
    BATTERY_LEVEL_FULL: 'BatteryLevel.Full'
}

BATTERY_TYPES = {
    BATTERY_TYPE_DISCONNECTED: 'Disconnected',
    BATTERY_TYPE_WIRED: 'Wired',
    BATTERY_TYPE_ALKALINE: 'Alkaline',
    BATTERY_TYPE_NIMH: 'Nickle Metal Hydride',
    BATTERY_TYPE_UNKNOWN: 'Unknown'
}


# User index definitions
XUSER_MAX_COUNT = 4
XUSER_INDEX_ANY = 0x000000FF

# Standard buttons
VK_PAD_A = 0x5800
VK_PAD_B = 0x5801
VK_PAD_X = 0x5802
VK_PAD_Y = 0x5803
VK_PAD_START = 0x5814
VK_PAD_BACK = 0x5815
VK_PAD_GUIDE_BUTTON = 0x0400

# Shoulder buttons
VK_PAD_RSHOULDER = 0x5804
VK_PAD_LSHOULDER = 0x5805

# Triggers
VK_PAD_LTRIGGER = 0x5806
VK_PAD_RTRIGGER = 0x5807

# Direction pad
VK_PAD_DPAD_UP = 0x5810
VK_PAD_DPAD_DOWN = 0x5811
VK_PAD_DPAD_LEFT = 0x5812
VK_PAD_DPAD_RIGHT = 0x5813

# Left analog
VK_PAD_LTHUMB_UP = 0x5820
VK_PAD_LTHUMB_DOWN = 0x5821
VK_PAD_LTHUMB_RIGHT = 0x5822
VK_PAD_LTHUMB_LEFT = 0x5823
VK_PAD_LTHUMB_UPLEFT = 0x5824
VK_PAD_LTHUMB_UPRIGHT = 0x5825
VK_PAD_LTHUMB_DOWNRIGHT = 0x5826
VK_PAD_LTHUMB_DOWNLEFT = 0x5827
VK_PAD_LTHUMB_PRESS = 0x5816

# Right analog
VK_PAD_RTHUMB_UP = 0x5830
VK_PAD_RTHUMB_DOWN = 0x5831
VK_PAD_RTHUMB_RIGHT = 0x5832
VK_PAD_RTHUMB_LEFT = 0x5833
VK_PAD_RTHUMB_UPLEFT = 0x5834
VK_PAD_RTHUMB_UPRIGHT = 0x5835
VK_PAD_RTHUMB_DOWNRIGHT = 0x5836
VK_PAD_RTHUMB_DOWNLEFT = 0x5837
VK_PAD_RTHUMB_PRESS = 0x5817

# Button press states
XINPUT_KEYSTROKE_KEYDOWN = 0x0001
XINPUT_KEYSTROKE_KEYUP = 0x0002
XINPUT_KEYSTROKE_REPEAT = 0x0004

# Analog trims
XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE = 7849
XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE = 8689
XINPUT_GAMEPAD_TRIGGER_THRESHOLD = 30

XINPUT_DEVTYPE_GAMEPAD = 0x01

# Controller types
XINPUT_DEVSUBTYPE_UNKNOWN = 0x00
XINPUT_DEVSUBTYPE_GAMEPAD = 0x01 # (Subtype 1)
XINPUT_DEVSUBTYPE_WHEEL = 0x02 # (Subtype 2)
XINPUT_DEVSUBTYPE_ARCADE_STICK = 0x03 # (Subtype 3)
XINPUT_DEVSUBTYPE_FLIGHT_STICK = 0x04 # (Subtype 4)
XINPUT_DEVSUBTYPE_DANCE_PAD = 0x05 # (Subtype 5)
XINPUT_DEVSUBTYPE_GUITAR = 0x06 # (Subtype 6)
XINPUT_DEVSUBTYPE_GUITAR_ALTERNATE = 0x07 # (Subtype 7)
XINPUT_DEVSUBTYPE_DRUM_KIT = 0x08 # (Subtype 8)
XINPUT_DEVSUBTYPE_GUITAR_BASS = 0xB # (Subtype 11)
XINPUT_DEVSUBTYPE_ARCADE_PAD = 0x13 # (Subtype 19)

LEFT_ANALOG = (
    VK_PAD_LTHUMB_UP,
    VK_PAD_LTHUMB_DOWN,
    VK_PAD_LTHUMB_LEFT,
    VK_PAD_LTHUMB_RIGHT,
    VK_PAD_LTHUMB_UPLEFT,
    VK_PAD_LTHUMB_UPRIGHT,
    VK_PAD_LTHUMB_DOWNLEFT,
    VK_PAD_LTHUMB_DOWNRIGHT
)
RIGHT_ANALOG = (
    VK_PAD_RTHUMB_UP,
    VK_PAD_RTHUMB_DOWN,
    VK_PAD_RTHUMB_LEFT,
    VK_PAD_RTHUMB_RIGHT,
    VK_PAD_RTHUMB_UPLEFT,
    VK_PAD_RTHUMB_UPRIGHT,
    VK_PAD_RTHUMB_DOWNLEFT,
    VK_PAD_RTHUMB_DOWNRIGHT
)


CONTROLLER_MAPPINGS = {
    XINPUT_DEVSUBTYPE_GAMEPAD: {
        VK_PAD_DPAD_UP         : 'D-Pad.Up',
        VK_PAD_DPAD_DOWN       : 'D-Pad.Down',
        VK_PAD_DPAD_LEFT       : 'D-Pad.Left',
        VK_PAD_DPAD_RIGHT      : 'D-Pad.Right',
        VK_PAD_A               : 'A',
        VK_PAD_B               : 'B',
        VK_PAD_X               : 'X',
        VK_PAD_Y               : 'Y',
        VK_PAD_START           : 'Start',
        VK_PAD_BACK            : 'Back',
        VK_PAD_LSHOULDER       : 'Shoulder.Left',
        VK_PAD_RSHOULDER       : 'Shoulder.Right',
        VK_PAD_LTRIGGER        : 'Trigger.Left',
        VK_PAD_RTRIGGER        : 'Trigger.Right',
        VK_PAD_LTHUMB_UP       : 'LeftStick.Up',
        VK_PAD_LTHUMB_DOWN     : 'LeftStick.Down',
        VK_PAD_LTHUMB_LEFT     : 'LeftStick.Left',
        VK_PAD_LTHUMB_RIGHT    : 'LeftStick.Right',
        VK_PAD_LTHUMB_UPLEFT   : 'LeftStick.UpLeft',
        VK_PAD_LTHUMB_UPRIGHT  : 'LeftStick.UpRight',
        VK_PAD_LTHUMB_DOWNLEFT : 'LeftStick.DownLeft',
        VK_PAD_LTHUMB_DOWNRIGHT: 'LeftStick.DownRight',
        VK_PAD_LTHUMB_PRESS    : 'LeftStick.Push',
        VK_PAD_RTHUMB_UP       : 'RightStick.Up',
        VK_PAD_RTHUMB_DOWN     : 'RightStick.Down',
        VK_PAD_RTHUMB_LEFT     : 'RightStick.Left',
        VK_PAD_RTHUMB_RIGHT    : 'RightStick.Right',
        VK_PAD_RTHUMB_UPLEFT   : 'RightStick.UpLeft',
        VK_PAD_RTHUMB_UPRIGHT  : 'RightStick.UpRight',
        VK_PAD_RTHUMB_DOWNLEFT : 'RightStick.DownLeft',
        VK_PAD_RTHUMB_DOWNRIGHT: 'RightStick.DownRight',
        VK_PAD_RTHUMB_PRESS    : 'RightStick.Push',
        VK_PAD_GUIDE_BUTTON    : 'Guide'
    },
    XINPUT_DEVSUBTYPE_WHEEL: {
        VK_PAD_DPAD_UP         : 'HatSwitch.Up',
        VK_PAD_DPAD_DOWN       : 'HatSwitch.Down',
        VK_PAD_DPAD_LEFT       : 'HatSwitch.Left',
        VK_PAD_DPAD_RIGHT      : 'HatSwitch.Right',
        VK_PAD_A               : 'A',
        VK_PAD_B               : 'B',
        VK_PAD_X               : 'X',
        VK_PAD_Y               : 'Y',
        VK_PAD_START           : 'START',
        VK_PAD_BACK            : 'BACK',
        VK_PAD_LSHOULDER       : 'LSHOULDER',
        VK_PAD_RSHOULDER       : 'RSHOULDER',
        VK_PAD_LTRIGGER        : 'LTRIGGER',
        VK_PAD_RTRIGGER        : 'RTRIGGER',
        VK_PAD_LTHUMB_UP       : 'LTHUMB_UP',
        VK_PAD_LTHUMB_DOWN     : 'LTHUMB_DOWN',
        VK_PAD_LTHUMB_LEFT     : 'Wheel.Left',
        VK_PAD_LTHUMB_RIGHT    : 'Wheel.Right',
        VK_PAD_LTHUMB_UPLEFT   : 'LTHUMB_UPLEFT',
        VK_PAD_LTHUMB_UPRIGHT  : 'LTHUMB_UPRIGHT',
        VK_PAD_LTHUMB_DOWNLEFT : 'LTHUMB_DOWNLEFT',
        VK_PAD_LTHUMB_DOWNRIGHT: 'LTHUMB_DOWNRIGHT',
        VK_PAD_LTHUMB_PRESS    : 'LTHUMB_PRESS',
        VK_PAD_RTHUMB_UP       : 'RTHUMB_UP',
        VK_PAD_RTHUMB_DOWN     : 'RTHUMB_DOWN',
        VK_PAD_RTHUMB_LEFT     : 'RTHUMB_LEFT',
        VK_PAD_RTHUMB_RIGHT    : 'RTHUMB_RIGHT',
        VK_PAD_RTHUMB_UPLEFT   : 'RTHUMB_UPLEFT',
        VK_PAD_RTHUMB_UPRIGHT  : 'RTHUMB_UPRIGHT',
        VK_PAD_RTHUMB_DOWNLEFT : 'RTHUMB_DOWNLEFT',
        VK_PAD_RTHUMB_DOWNRIGHT: 'RTHUMB_DOWNRIGHT',
        VK_PAD_RTHUMB_PRESS    : 'RTHUMB_PRESS',
        VK_PAD_GUIDE_BUTTON    : 'Guide'
    },
    XINPUT_DEVSUBTYPE_FLIGHT_STICK: {
        VK_PAD_DPAD_UP         : 'DPAD_UP',
        VK_PAD_DPAD_DOWN       : 'DPAD_DOWN',
        VK_PAD_DPAD_LEFT       : 'DPAD_LEFT',
        VK_PAD_DPAD_RIGHT      : 'DPAD_RIGHT',
        VK_PAD_A               : 'Weapon.Primary',
        VK_PAD_B               : 'Weapon.Secondary',
        VK_PAD_X               : 'X',
        VK_PAD_Y               : 'Y',
        VK_PAD_START           : 'START',
        VK_PAD_BACK            : 'BACK',
        VK_PAD_LSHOULDER       : 'LSHOULDER',
        VK_PAD_RSHOULDER       : 'RSHOULDER',
        VK_PAD_LTRIGGER        : 'Throttle.Up',
        VK_PAD_RTRIGGER        : 'Throttle.Down',
        VK_PAD_LTHUMB_UP       : 'Pitch.Down',
        VK_PAD_LTHUMB_DOWN     : 'Pitch.Up',
        VK_PAD_LTHUMB_LEFT     : 'Roll.Left',
        VK_PAD_LTHUMB_RIGHT    : 'Roll.Right',
        VK_PAD_LTHUMB_UPLEFT   : 'PitchDown.RollLeft',
        VK_PAD_LTHUMB_UPRIGHT  : 'PitchDown.RollRight',
        VK_PAD_LTHUMB_DOWNLEFT : 'PitchUp.RollLeft',
        VK_PAD_LTHUMB_DOWNRIGHT: 'PitchUp.RollRight',
        VK_PAD_LTHUMB_PRESS    : 'LTHUMB_PRESS',
        VK_PAD_RTHUMB_UP       : 'POVHat.Up',
        VK_PAD_RTHUMB_DOWN     : 'POVHat.Down',
        VK_PAD_RTHUMB_LEFT     : 'POVHat.Left',
        VK_PAD_RTHUMB_RIGHT    : 'POVHat.Right',
        VK_PAD_RTHUMB_UPLEFT   : 'RTHUMB_UPLEFT',
        VK_PAD_RTHUMB_UPRIGHT  : 'RTHUMB_UPRIGHT',
        VK_PAD_RTHUMB_DOWNLEFT : 'RTHUMB_DOWNLEFT',
        VK_PAD_RTHUMB_DOWNRIGHT: 'RTHUMB_DOWNRIGHT',
        VK_PAD_RTHUMB_PRESS    : 'RTHUMB_PRESS',
        VK_PAD_GUIDE_BUTTON    : 'Guide'
    },
    XINPUT_DEVSUBTYPE_GUITAR: {
        VK_PAD_DPAD_UP         : 'Strum.Up',
        VK_PAD_DPAD_DOWN       : 'Strum.Down',
        VK_PAD_DPAD_LEFT       : 'D-Pad.Left',
        VK_PAD_DPAD_RIGHT      : 'D-Pad.Right',
        VK_PAD_A               : 'Fret.Green',
        VK_PAD_B               : 'Fret.Red',
        VK_PAD_X               : 'Fret.Blue',
        VK_PAD_Y               : 'Fret.Yellow',
        VK_PAD_START           : 'Start',
        VK_PAD_BACK            : 'Back',
        VK_PAD_LSHOULDER       : 'Fret.Orange',
        VK_PAD_RSHOULDER       : 'FretModifier.2',
        VK_PAD_LTRIGGER        : 'PickupSelector',
        VK_PAD_RTRIGGER        : 'FretModifier.1',
        VK_PAD_LTHUMB_UP       : 'Pitch.Down',
        VK_PAD_LTHUMB_DOWN     : 'Pitch.Up',
        VK_PAD_LTHUMB_LEFT     : 'Roll.Left',
        VK_PAD_LTHUMB_RIGHT    : 'Roll.Right',
        VK_PAD_LTHUMB_UPLEFT   : 'LTHUMB_UPLEFT',
        VK_PAD_LTHUMB_UPRIGHT  : 'LTHUMB_UPRIGHT',
        VK_PAD_LTHUMB_DOWNLEFT : 'LTHUMB_DOWNLEFT',
        VK_PAD_LTHUMB_DOWNRIGHT: 'LTHUMB_DOWNRIGHT',
        VK_PAD_LTHUMB_PRESS    : 'FretModifier.3',
        VK_PAD_RTHUMB_UP       : 'Orientation.Up',
        VK_PAD_RTHUMB_DOWN     : 'Orientation.Down',
        VK_PAD_RTHUMB_LEFT     : 'WhammyBar.Left',
        VK_PAD_RTHUMB_RIGHT    : 'WhammyBar.Right',
        VK_PAD_RTHUMB_UPLEFT   : 'RTHUMB_UPLEFT',
        VK_PAD_RTHUMB_UPRIGHT  : 'RTHUMB_UPRIGHT',
        VK_PAD_RTHUMB_DOWNLEFT : 'RTHUMB_DOWNLEFT',
        VK_PAD_RTHUMB_DOWNRIGHT: 'RTHUMB_DOWNRIGHT',
        VK_PAD_RTHUMB_PRESS    : 'RTHUMB_PRESS',
        VK_PAD_GUIDE_BUTTON    : 'Guide'
    },
    XINPUT_DEVSUBTYPE_DRUM_KIT: {
        VK_PAD_DPAD_UP         : 'D-Pad.Up',
        VK_PAD_DPAD_DOWN       : 'D-Pad.Down',
        VK_PAD_DPAD_LEFT       : 'D-Pad.Left',
        VK_PAD_DPAD_RIGHT      : 'D-Pad.Right',
        VK_PAD_A               : 'Tom.Floor',
        VK_PAD_B               : 'Drum.Snare',
        VK_PAD_X               : 'Tom.Low',
        VK_PAD_Y               : 'Tom.High',
        VK_PAD_START           : 'Start',
        VK_PAD_BACK            : 'Back',
        VK_PAD_LSHOULDER       : 'Drum.Bass',
        VK_PAD_RSHOULDER       : 'RSHOULDER',
        VK_PAD_LTRIGGER        : 'LTRIGGER',
        VK_PAD_RTRIGGER        : 'RTRIGGER',
        VK_PAD_LTHUMB_UP       : 'LTHUMB_UP',
        VK_PAD_LTHUMB_DOWN     : 'LTHUMB_DOWN',
        VK_PAD_LTHUMB_LEFT     : 'LTHUMB_LEFT',
        VK_PAD_LTHUMB_RIGHT    : 'LTHUMB_RIGHT',
        VK_PAD_LTHUMB_UPLEFT   : 'LTHUMB_UPLEFT',
        VK_PAD_LTHUMB_UPRIGHT  : 'LTHUMB_UPRIGHT',
        VK_PAD_LTHUMB_DOWNLEFT : 'LTHUMB_DOWNLEFT',
        VK_PAD_LTHUMB_DOWNRIGHT: 'LTHUMB_DOWNRIGHT',
        VK_PAD_LTHUMB_PRESS    : 'LTHUMB_PRESS',
        VK_PAD_RTHUMB_UP       : 'RTHUMB_UP',
        VK_PAD_RTHUMB_DOWN     : 'RTHUMB_DOWN',
        VK_PAD_RTHUMB_LEFT     : 'RTHUMB_LEFT',
        VK_PAD_RTHUMB_RIGHT    : 'RTHUMB_RIGHT',
        VK_PAD_RTHUMB_UPLEFT   : 'RTHUMB_UPLEFT',
        VK_PAD_RTHUMB_UPRIGHT  : 'RTHUMB_UPRIGHT',
        VK_PAD_RTHUMB_DOWNLEFT : 'RTHUMB_DOWNLEFT',
        VK_PAD_RTHUMB_DOWNRIGHT: 'RTHUMB_DOWNRIGHT',
        VK_PAD_RTHUMB_PRESS    : 'RTHUMB_PRESS',
        VK_PAD_GUIDE_BUTTON    : 'Guide'
    },
    XINPUT_DEVSUBTYPE_DANCE_PAD: {
        VK_PAD_DPAD_UP         : 'D-Pad.Up',
        VK_PAD_DPAD_DOWN       : 'D-Pad.Down',
        VK_PAD_DPAD_LEFT       : 'D-Pad.Left',
        VK_PAD_DPAD_RIGHT      : 'D-Pad.Right',
        VK_PAD_A               : 'A',
        VK_PAD_B               : 'B',
        VK_PAD_X               : 'X',
        VK_PAD_Y               : 'Y',
        VK_PAD_START           : 'Start',
        VK_PAD_BACK            : 'Back',
        VK_PAD_LSHOULDER       : 'LSHOULDER',
        VK_PAD_RSHOULDER       : 'RSHOULDER',
        VK_PAD_LTRIGGER        : 'LTRIGGER',
        VK_PAD_RTRIGGER        : 'RTRIGGER',
        VK_PAD_LTHUMB_UP       : 'LTHUMB_UP',
        VK_PAD_LTHUMB_DOWN     : 'LTHUMB_DOWN',
        VK_PAD_LTHUMB_LEFT     : 'LTHUMB_LEFT',
        VK_PAD_LTHUMB_RIGHT    : 'LTHUMB_RIGHT',
        VK_PAD_LTHUMB_UPLEFT   : 'LTHUMB_UPLEFT',
        VK_PAD_LTHUMB_UPRIGHT  : 'LTHUMB_UPRIGHT',
        VK_PAD_LTHUMB_DOWNLEFT : 'LTHUMB_DOWNLEFT',
        VK_PAD_LTHUMB_DOWNRIGHT: 'LTHUMB_DOWNRIGHT',
        VK_PAD_LTHUMB_PRESS    : 'LTHUMB_PRESS',
        VK_PAD_RTHUMB_UP       : 'RTHUMB_UP',
        VK_PAD_RTHUMB_DOWN     : 'RTHUMB_DOWN',
        VK_PAD_RTHUMB_LEFT     : 'RTHUMB_LEFT',
        VK_PAD_RTHUMB_RIGHT    : 'RTHUMB_RIGHT',
        VK_PAD_RTHUMB_UPLEFT   : 'RTHUMB_UPLEFT',
        VK_PAD_RTHUMB_UPRIGHT  : 'RTHUMB_UPRIGHT',
        VK_PAD_RTHUMB_DOWNLEFT : 'RTHUMB_DOWNLEFT',
        VK_PAD_RTHUMB_DOWNRIGHT: 'RTHUMB_DOWNRIGHT',
        VK_PAD_RTHUMB_PRESS    : 'RTHUMB_PRESS',
        VK_PAD_GUIDE_BUTTON    : 'Guide'
    },
    XINPUT_DEVSUBTYPE_ARCADE_STICK: {
        VK_PAD_DPAD_UP         : 'D-Pad.Up',
        VK_PAD_DPAD_DOWN       : 'D-Pad.Down',
        VK_PAD_DPAD_LEFT       : 'D-Pad.Left',
        VK_PAD_DPAD_RIGHT      : 'D-Pad.Right',
        VK_PAD_A               : 'A',
        VK_PAD_B               : 'B',
        VK_PAD_X               : 'X',
        VK_PAD_Y               : 'Y',
        VK_PAD_START           : 'Start',
        VK_PAD_BACK            : 'Back',
        VK_PAD_LSHOULDER       : 'LSHOULDER',
        VK_PAD_RSHOULDER       : 'RSHOULDER',
        VK_PAD_LTRIGGER        : 'Trigger.Left',
        VK_PAD_RTRIGGER        : 'Trigger.Right',
        VK_PAD_LTHUMB_UP       : 'LTHUMB_UP',
        VK_PAD_LTHUMB_DOWN     : 'LTHUMB_DOWN',
        VK_PAD_LTHUMB_LEFT     : 'LTHUMB_LEFT',
        VK_PAD_LTHUMB_RIGHT    : 'LTHUMB_RIGHT',
        VK_PAD_LTHUMB_UPLEFT   : 'LTHUMB_UPLEFT',
        VK_PAD_LTHUMB_UPRIGHT  : 'LTHUMB_UPRIGHT',
        VK_PAD_LTHUMB_DOWNLEFT : 'LTHUMB_DOWNLEFT',
        VK_PAD_LTHUMB_DOWNRIGHT: 'LTHUMB_DOWNRIGHT',
        VK_PAD_LTHUMB_PRESS    : 'LTHUMB_PRESS',
        VK_PAD_RTHUMB_UP       : 'RTHUMB_UP',
        VK_PAD_RTHUMB_DOWN     : 'RTHUMB_DOWN',
        VK_PAD_RTHUMB_LEFT     : 'RTHUMB_LEFT',
        VK_PAD_RTHUMB_RIGHT    : 'RTHUMB_RIGHT',
        VK_PAD_RTHUMB_UPLEFT   : 'RTHUMB_UPLEFT',
        VK_PAD_RTHUMB_UPRIGHT  : 'RTHUMB_UPRIGHT',
        VK_PAD_RTHUMB_DOWNLEFT : 'RTHUMB_DOWNLEFT',
        VK_PAD_RTHUMB_DOWNRIGHT: 'RTHUMB_DOWNRIGHT',
        VK_PAD_RTHUMB_PRESS    : 'RTHUMB_PRESS',
        VK_PAD_GUIDE_BUTTON    : 'Guide'
    },
    XINPUT_DEVSUBTYPE_ARCADE_PAD: {
        VK_PAD_DPAD_UP         : 'D-Pad.Up',
        VK_PAD_DPAD_DOWN       : 'D-Pad.Down',
        VK_PAD_DPAD_LEFT       : 'D-Pad.Left',
        VK_PAD_DPAD_RIGHT      : 'D-Pad.Right',
        VK_PAD_A               : 'A',
        VK_PAD_B               : 'B',
        VK_PAD_X               : 'X',
        VK_PAD_Y               : 'Y',
        VK_PAD_START           : 'Start',
        VK_PAD_BACK            : 'Back',
        VK_PAD_LSHOULDER       : 'Shoulder.Left',
        VK_PAD_RSHOULDER       : 'Shoulder.Right',
        VK_PAD_LTRIGGER        : 'Trigger.Left',
        VK_PAD_RTRIGGER        : 'Trigger.Right',
        VK_PAD_LTHUMB_UP       : 'LTHUMB_UP',
        VK_PAD_LTHUMB_DOWN     : 'LTHUMB_DOWN',
        VK_PAD_LTHUMB_LEFT     : 'LTHUMB_LEFT',
        VK_PAD_LTHUMB_RIGHT    : 'LTHUMB_RIGHT',
        VK_PAD_LTHUMB_UPLEFT   : 'LTHUMB_UPLEFT',
        VK_PAD_LTHUMB_UPRIGHT  : 'LTHUMB_UPRIGHT',
        VK_PAD_LTHUMB_DOWNLEFT : 'LTHUMB_DOWNLEFT',
        VK_PAD_LTHUMB_DOWNRIGHT: 'LTHUMB_DOWNRIGHT',
        VK_PAD_LTHUMB_PRESS    : 'LTHUMB_PRESS',
        VK_PAD_RTHUMB_UP       : 'RTHUMB_UP',
        VK_PAD_RTHUMB_DOWN     : 'RTHUMB_DOWN',
        VK_PAD_RTHUMB_LEFT     : 'RTHUMB_LEFT',
        VK_PAD_RTHUMB_RIGHT    : 'RTHUMB_RIGHT',
        VK_PAD_RTHUMB_UPLEFT   : 'RTHUMB_UPLEFT',
        VK_PAD_RTHUMB_UPRIGHT  : 'RTHUMB_UPRIGHT',
        VK_PAD_RTHUMB_DOWNLEFT : 'RTHUMB_DOWNLEFT',
        VK_PAD_RTHUMB_DOWNRIGHT: 'RTHUMB_DOWNRIGHT',
        VK_PAD_RTHUMB_PRESS    : 'RTHUMB_PRESS',
        VK_PAD_GUIDE_BUTTON    : 'Guide'
    },
}

CONTROLLER_MAPPINGS[XINPUT_DEVSUBTYPE_UNKNOWN] = (
    CONTROLLER_MAPPINGS[XINPUT_DEVSUBTYPE_GAMEPAD]
)
CONTROLLER_MAPPINGS[XINPUT_DEVSUBTYPE_GUITAR_BASS] = (
    CONTROLLER_MAPPINGS[XINPUT_DEVSUBTYPE_GUITAR]
)
CONTROLLER_MAPPINGS[XINPUT_DEVSUBTYPE_GUITAR_ALTERNATE] = (
    CONTROLLER_MAPPINGS[XINPUT_DEVSUBTYPE_GUITAR]
)


if eg.WindowsVersion >= '8':
    XInputDLL = ctypes.windll.LoadLibrary("xinput1_4")
    XINPUT_14 = True
    XINPUT_13_PLUGIN = False
else:
    XINPUT_14 = False
    try:
        XInputDLL = ctypes.windll.LoadLibrary("xinput1_3")
        XINPUT_13_PLUGIN = False
    except:
        dll_path = os.path.join(__path__[0], "xinput1_3.dll")
        XInputDLL = ctypes.cdll.LoadLibrary(dll_path)
        XINPUT_13_PLUGIN = True


class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ('wButtons', WORD),
        ('bLeftTrigger', BYTE),
        ('bRightTrigger', BYTE),
        ('sThumbLX', SHORT),
        ('sThumbLY', SHORT),
        ('sThumbRX', SHORT),
        ('sThumbRY', SHORT),
    ]


class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ('dwPacketNumber', DWORD),
        ('Gamepad', XINPUT_GAMEPAD)
    ]


class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [
        ('wLeftMotorSpeed', WORD),
        ('wRightMotorSpeed', WORD)
    ]


class XINPUT_CAPABILITIES(ctypes.Structure):
    _fields_ = [
        ('Type', BYTE),
        ('SubType', BYTE),
        ('Flags', BYTE),
        ('Gamepad', XINPUT_GAMEPAD),
        ('Vibration', XINPUT_VIBRATION),
    ]


class XINPUT_BATTERY_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('BatteryType', BYTE),
        ('BatteryLevel', BYTE)
    ]


class XINPUT_KEYSTROKE(ctypes.Structure):
    _fields_ = [
        ('VirtualKey', WORD),
        ('Unicode', WCHAR),
        ('Flags', WORD),
        ('UserIndex', BYTE),
        ('HidCode', BYTE)
    ]


XInputPowerOffControllerAPI = XInputDLL[103]
XInputPowerOffControllerAPI.restype = DWORD
XInputPowerOffControllerAPI.argtypes = [
    DWORD
]


XInputSetStateAPI = XInputDLL.XInputSetState
XInputSetStateAPI.restype = DWORD
XInputSetStateAPI.argtypes = [
    DWORD,
    POINTER(XINPUT_VIBRATION)
]


XInputGetStateAPI = XInputDLL[100]
XInputGetStateAPI.restype = DWORD
XInputGetStateAPI.argtypes = [
    DWORD,
    POINTER(XINPUT_STATE)
]

XInputGetCapabilitiesAPI = XInputDLL.XInputGetCapabilities
XInputGetCapabilitiesAPI.restype = DWORD
XInputGetCapabilitiesAPI.argtypes = [
    DWORD,
    DWORD,
    POINTER(XINPUT_CAPABILITIES)
]

XInputGetBatteryInformationAPI = XInputDLL.XInputGetBatteryInformation
XInputGetBatteryInformationAPI.restype = DWORD
XInputGetBatteryInformationAPI.argtypes = [
    DWORD,
    BYTE,
    POINTER(XINPUT_BATTERY_INFORMATION)
]

XInputGetKeystrokeAPI = XInputDLL.XInputGetKeystroke
XInputGetKeystrokeAPI.restype = DWORD
XInputGetKeystrokeAPI.argtypes = [
    DWORD,
    DWORD,
    POINTER(XINPUT_KEYSTROKE)
]


def XInputPowerOffController(dwUserIndex):
    return XInputPowerOffControllerAPI(DWORD(dwUserIndex))


def XInputGetState(dwUserIndex, pState):
    return XInputGetStateAPI(
        DWORD(dwUserIndex),
        ctypes.byref(pState)
    )


def XInputSetState(dwUserIndex, pVibration):
    XInputSetStateAPI(
        DWORD(dwUserIndex),
        ctypes.byref(pVibration)
    )


def XInputGetCapabilities(dwUserIndex, pCapabilities):
    return XInputGetCapabilitiesAPI(
        DWORD(dwUserIndex),
        DWORD(XINPUT_FLAG_GAMEPAD),
        ctypes.byref(pCapabilities)
    )


def XInputGetBatteryInformation(dwUserIndex, pBatteryInformation):
    return XInputGetBatteryInformationAPI(
        DWORD(dwUserIndex),
        BYTE(BATTERY_DEVTYPE_GAMEPAD),
        ctypes.byref(pBatteryInformation)
    )


def XInputGetKeystroke(dwUserIndex, pKeystroke):
    return XInputGetKeystrokeAPI(
        DWORD(dwUserIndex),
        DWORD(0),
        ctypes.byref(pKeystroke)
    )


def _get_mouse_absolute(x, y):
    new_min_x = 0
    new_max_x = 0
    new_min_y = 0
    new_max_y = 0
    for monitor in GetMonitorDimensions():
        pos_x, pos_y, size_x, size_y = monitor
        new_min_x = min(pos_x, new_min_x)
        new_max_x = max(pos_x + size_x, new_max_x)
        new_min_y = min(pos_y, new_min_y)
        new_max_y = max(pos_y + size_y, new_max_y)

    def re_range(old_min, old_max, new_min, new_max, value):
        old_range = old_max - old_min
        new_range = new_max - new_min

        return (
            (((value - old_min) * new_range) / old_range) +
            new_min
        )

    if x > 0:
        sq_x = sqrt(re_range(-32767.0, 32767.0, 2.0, 1.0, float(x)))
    else:
        sq_x = sqrt(re_range(-32767.0, 32767.0, 2.0, 1.0, float(-x)))
    if y > 0:
        sq_y = sqrt(re_range(-32767.0, 32767.0, 2.0, 1.0, float(y)))
    else:
        sq_y = sqrt(re_range(-32767.0, 32767.0, 2.0, 1.0, float(-y)))

    new_min_x *= sq_x
    new_max_x *= sq_x
    new_min_y *= sq_y
    new_max_y *= sq_y

    new_x = int(re_range(-32767.0, 32767.0, new_min_x, new_max_x, float(x)))
    new_y = int(re_range(-32767.0, 32767.0, new_min_y, new_max_y, float(y)))

    return new_x, new_y


class DEBUG:

    def __init__(self, cls_name, _id):
        self._cls_name = cls_name
        self._id = _id + 1
        self()

    def __call__(self, *args):
        self._print('', self._cls_name, 'ID', self._id, *args)

    def IN(self, *args):
        self._print('--->', self._cls_name, 'ID', self._id, *args)

    def OUT(self, *args):
        self._print('<---', self._cls_name, 'ID', self._id, *args)

    def _print(self, direction, cls_name, *args):
        if _DEBUG and self._id not in _DEBUG_FILTER:
            debug = (
                ' {0} {1}: ' +
                ': '.join(list('{%d}' % (i + 2,) for i in range(len(args))))
            )
            eg.PrintDebugNotice(debug.format(direction, cls_name, *args))


class Controller(object):

    def __init__(self, plugin, _id):
        self._debug = DEBUG(self.__class__.__name__, _id)

        self.plugin = plugin
        self._poll_rate = 0.3
        self._mouse_pointer = None
        self._mouse_left_click = False
        self._mouse_right_click = False
        self._mouse_middle_click = False
        self._id = max(min(_id, 3), 0) # 0..3
        self._name = 'Controller' + str(self._id + 1)
        self._events = None
        self._bat_level = None
        self._connected = False
        self._keycodes = []
        self.thread = None
        self._calibrated = 50
        self._mouse_absolute = False
        self._mouse_movement = False
        self._mouse_queue = (
            eg.plugins.Mouse.plugin.thread.receiveQueue
        )
        self._packet = 0
        self._timer = None
        self._idle = 0

        self._debug(
            'XINPUT_TYPE',
            '',
            'XINPUT_14',
            XINPUT_14,
            'XINPUT_13_PLUGIN',
            XINPUT_13_PLUGIN
        )

    def enable_mouse(self, analog_stick, absolute):
        self._mouse_absolute = absolute
        self._mouse_pointer = analog_stick

    def disable_mouse(self):
        self._mouse_pointer = None

    def is_connected(self):
        return self._connected

    def _is_connected(self):
        xinput_state = XINPUT_STATE()
        res = XInputGetState(self._id, xinput_state)
        connected = res == ERROR_SUCCESS

        self._debug.OUT('Controller Connection', self._connected)
        self._debug.IN('Connected', connected, 'RES', hex(res))

        if self._connected and not connected:
            self.plugin.TriggerEvent(
                suffix=self._name + '.Disconnected'
            )
            self._debug('Disconnected', '...')
            self.reset()

        elif connected and not self._connected:
            self.plugin.TriggerEvent(
                suffix=self._name + '.Connected'
            )
            self._debug('Connected', '...')

            xinput_capabilities = XINPUT_CAPABILITIES()
            XInputGetCapabilities(self._id, xinput_capabilities)

            self._events = CONTROLLER_MAPPINGS[xinput_capabilities.SubType]

        self._connected = connected
        return connected

    def reset(self):
        if self._events is not None:
            self._debug('Resetting', '...')
            self._events = None
            self._bat_level = None
            self._connected = False
            self._keycodes = []
            self._poll_rate = 0.3
            self._packet = 0
            self._idle = 0
            self._calibrated = 50
            self._mouse_left_click = False
            self._mouse_right_click = False
            self._mouse_middle_click = False
            if self._mouse_movement:
                self._mouse_movement = False
                if self._mouse_absolute:
                    SetCursorPos(*_get_mouse_absolute(0, 0))
                else:
                    self._mouse_queue.put((-2,))

            try:
                self._timer.stop()
            except:
                pass

            self._timer = None

    def getID(self):
        return self._id

    def set_ffb(self, left=0, right=0):

        if left:
            wLeftMotorSpeed = (
                int((left * int(65535 * 0.88)) / 100) +
                (65535 - int(65535 * 0.88))
            )
        else:
            wLeftMotorSpeed = 0
        if right:
            wRightMotorSpeed = (
                int((right * int(65535 * 0.88)) / 100) +
                (65535 - int(65535 * 0.88))
            )
        else:
            wRightMotorSpeed = 0

        self._debug.OUT(
            'Set FFB',
            '',
            'Left',
            left,
            'Right',
            right,
            'wLeftMotorSpeed',
            wLeftMotorSpeed,
            'wRightMotorSpeed',
            wRightMotorSpeed
        )

        xinput_vibration = XINPUT_VIBRATION(wLeftMotorSpeed, wRightMotorSpeed)
        XInputSetState(self._id, xinput_vibration)

    def _create_suffix(self):
        self._keycodes.sort()
        suf = list(
            self._events[c] for c in self._keycodes
        )
        return '.'.join([self._name] + suf)

    def _read_analogs(self):
        xinput_state = XINPUT_STATE()
        XInputGetState(self._id, xinput_state)
        xinput_gamepad = xinput_state.Gamepad

        sThumbL = (
            xinput_gamepad.sThumbLX,
            xinput_gamepad.sThumbLY
        )
        sThumbR = (
            xinput_gamepad.sThumbRX,
            xinput_gamepad.sThumbRY
        )

        bLeftTrigger = xinput_gamepad.bLeftTrigger
        bRightTrigger = xinput_gamepad.bRightTrigger

        payload = dict()
        for keycode in sorted(self._keycodes):

            if keycode in (VK_PAD_LTRIGGER, VK_PAD_RTRIGGER):

                if keycode == VK_PAD_LTRIGGER:
                    key = 'left_trigger_analog'
                    value = bLeftTrigger
                else:
                    key = 'right_trigger_analog'
                    value = bRightTrigger

                if value > XINPUT_GAMEPAD_TRIGGER_THRESHOLD:
                    value -= float(XINPUT_GAMEPAD_TRIGGER_THRESHOLD)
                    value /= float(0xFF - XINPUT_GAMEPAD_TRIGGER_THRESHOLD)
                else:
                    value = 0.0

            elif keycode in LEFT_ANALOG + RIGHT_ANALOG:
                if keycode in LEFT_ANALOG:
                    key = 'left_analog'
                    value = sThumbL
                    #deadzone = XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE
                else:
                    key = 'right_analog'
                    value = sThumbR
                    #deadzone = XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE

                #x = float(value[0])
                #y = float(value[1])
                #magnitude = math.sqrt(x * x + y * y)
                #if magnitude < deadzone:
                #    value = (0, 0)
                    # normalized_x = x / magnitude
                    # normalized_y = y / magnitude
                    # magnitude = min(magnitude, 32767)
                    # magnitude = magnitude - deadzone
                    # normalized_magnitude = magnitude / (32767 - deadzone)
                    # normalized_x *= normalized_magnitude
                    # normalized_y *= normalized_magnitude
                    # value = (normalized_x, normalized_y)
                # else:

            else:
                continue

            payload[key] = value

        if payload:
            items = ['unfactored', '']
            items += ['L_Thumb', sThumbL, 'R_Thumb', sThumbR]
            items += ['L_Trigger', bLeftTrigger, 'R_Trigger', bRightTrigger]
            items += ['factored', '']
            for item in payload.items():
                items += list(item)

            self._debug.IN('ANALOG', '', *items)
            return payload

    def _trigger_event(self, suffix, prefix=None):
        if suffix == 'Repeat':
            try:
                self._timer.stop()
            except:
                pass
            self._timer = None

        payload = self._read_analogs()
        if self._mouse_pointer:
            if 'left' in self._mouse_pointer:
                thumb_press = VK_PAD_LTHUMB_PRESS
                middle_click = VK_PAD_RTHUMB_PRESS
            else:
                thumb_press = VK_PAD_RTHUMB_PRESS
                middle_click = VK_PAD_LTHUMB_PRESS

            if payload and self._mouse_pointer in payload:
                self._mouse_movement = True
                x, y = payload[self._mouse_pointer]

                if thumb_press in self._keycodes:
                    x = x / 8191
                    y = y / 8191
                    if x:
                        mouse_event(MOUSEEVENT_HWHEEL, 0, 0, x * 120, 0)
                    if y:
                        mouse_event(MOUSEEVENT_VWHEEL, 0, 0, y * 120, 0)

                elif self._mouse_absolute:
                    SetCursorPos(*_get_mouse_absolute(x, y))

                else:
                    if x == 0 and y == 0:
                        self._mouse_queue.put((-2,))
                    else:
                        speed = hypot(x, y) / 8000
                        angle = degrees(atan2(float(x), float(y)))
                        self._mouse_queue.put((angle, 3, speed, 5, 0))
                return

            elif self._mouse_movement:
                self._mouse_movement = False
                if self._mouse_absolute:
                    SetCursorPos(*_get_mouse_absolute(0, 0))
                else:
                    self._mouse_queue.put((-2,))
                return

            left_clicked = VK_PAD_LTRIGGER in self._keycodes

            if left_clicked and not self._mouse_left_click:
                self._mouse_left_click = True
                mouse_event(MOUSEEVENT_LEFTDOWN, 0, 0, 0, 0)
                return

            elif not left_clicked and self._mouse_left_click:
                self._mouse_left_click = False
                mouse_event(MOUSEEVENT_LEFTUP, 0, 0, 0, 0)
                return

            right_clicked = VK_PAD_RTRIGGER in self._keycodes

            if right_clicked and not self._mouse_right_click:
                self._mouse_right_click = True
                mouse_event(MOUSEEVENT_RIGHTDOWN, 0, 0, 0, 0)
                return

            elif not right_clicked and self._mouse_right_click:
                self._mouse_right_click = False
                mouse_event(MOUSEEVENT_RIGHTUP, 0, 0, 0, 0)
                return

            middle_clicked = middle_click in self._keycodes
            if middle_clicked and not self._mouse_middle_click:
                self._mouse_middle_click = True
                mouse_event(MOUSEEVENT_MIDDLEDOWN, 0, 0, 0, 0)
                return

            elif not middle_clicked and self._mouse_middle_click:
                self._mouse_middle_click = False
                mouse_event(MOUSEEVENT_MIDDLEUP, 0, 0, 0, 0)
                return

        if prefix is None:
            if self._keycodes:
                self.plugin.TriggerEvent(
                    suffix=self._create_suffix() + '.' + suffix,
                    payload=payload
                )
        else:
            self.plugin.TriggerEvent(
                suffix=self._name + '.' + prefix + '.' + suffix,
            )

    def update(self, event):
        while not event.isSet():
            if self._is_connected():
                xinput_state = XINPUT_STATE()
                xinput_keystroke = XINPUT_KEYSTROKE()

                state = (
                    XInputGetState(self._id, xinput_state) ==
                    ERROR_SUCCESS
                )
                keypress = (
                    XInputGetKeystroke(self._id, xinput_keystroke) ==
                    ERROR_SUCCESS
                )

                if state and keypress:
                    packet = xinput_state.dwPacketNumber
                    packet_loss = (packet - self._packet) - 1
                    self._packet = packet

                    if packet_loss:
                        self._calibrated -= 1
                    elif self._calibrated < 101:
                        self._calibrated += 1

                    if self._calibrated < 99:
                        self._poll_rate -= self._poll_rate / 2

                    elif self._calibrated == 99:
                        self._poll_rate += self._poll_rate / 2

                    elif self._calibrated == 100:
                        self._calibrated += 1

                elif not self._keycodes and state and self._poll_rate < 0.3:
                    self._idle += self._poll_rate

                    if self._idle / self._poll_rate == 20:
                        self._poll_rate += self._poll_rate
                        self._idle = 0

                if self._poll_rate < 0.05:
                    self._poll_rate = 0.05

                elif self._poll_rate > 0.3:
                    self._poll_rate = 0.3

                if state:
                    wButtons = xinput_state.Gamepad.wButtons
                    guide = wButtons | VK_PAD_GUIDE_BUTTON == wButtons
                    if guide and VK_PAD_GUIDE_BUTTON not in self._keycodes:
                        try:
                            self._timer.stop()
                        except:
                            pass
                        self._timer = None

                        self._keycodes += [VK_PAD_GUIDE_BUTTON]
                        self._trigger_event('Pressed')

                    elif not guide and VK_PAD_GUIDE_BUTTON in self._keycodes:
                        try:
                            self._timer.stop()
                        except:
                            pass
                        self._timer = None

                        self._keycodes.remove(VK_PAD_GUIDE_BUTTON)
                        self._trigger_event(
                            'Released',
                            self._events[VK_PAD_GUIDE_BUTTON]
                        )
                        self._trigger_event('Pressed')

                if keypress:
                    keycode = xinput_keystroke.VirtualKey
                    flags = xinput_keystroke.Flags

                    try:
                        self._timer.stop()
                    except:
                        pass
                    self._timer = None

                    if keycode in self._events:
                        if flags == XINPUT_KEYSTROKE_KEYDOWN:
                            self._debug.IN('KEYSTROKE_KEYDOWN', hex(keycode))

                            if keycode not in self._keycodes:
                                self._keycodes += [keycode]
                                self._trigger_event('Pressed')

                        elif flags == XINPUT_KEYSTROKE_KEYUP:
                            self._debug.IN('KEYSTROKE_KEYUP', hex(keycode))
                            if keycode in self._keycodes:
                                self._keycodes.remove(keycode)
                                self._trigger_event(
                                    'Released',
                                    self._events[keycode]
                                )
                                self._trigger_event('Pressed')

                        elif flags == XINPUT_KEYSTROKE_REPEAT:
                            self._debug.IN('KEYSTROKE_REPEAT', hex(keycode))
                        else:
                            self._debug.IN('KEYSTROKE_UNKNOWN', hex(keycode))
                    else:
                        self._debug('KEYCODE_NOT_FOUND', hex(keycode))

                xinput_battery_information = XINPUT_BATTERY_INFORMATION()
                update = XInputGetBatteryInformation(
                    self._id,
                    xinput_battery_information
                )

                if update == ERROR_SUCCESS:
                    bat_type = xinput_battery_information.BatteryType
                    bat_level = xinput_battery_information.BatteryLevel
                    if (
                        bat_type in BATTERY_TYPES and
                        bat_level in BATTERY_LEVELS and
                        bat_level != self._bat_level
                    ):
                        self._debug.IN(
                            'BATTERY_INFORMATION',
                            '',
                            'BatteryType',
                            BATTERY_TYPES[bat_type],
                            'BatteryType Code',
                            hex(bat_type),
                            'BatteryLevel',
                            BATTERY_LEVELS[bat_level],
                            'BatteryLevel Code',
                            hex(bat_level)
                        )

                        self._bat_level = bat_level

                        self.plugin.TriggerEvent(
                            suffix=(
                                self._name + '.' + BATTERY_LEVELS[bat_level]
                            ),
                            payload=BATTERY_TYPES[bat_type]
                        )

                if self._timer is None:
                    self._timer = threading.Timer(
                        self._poll_rate * 2,
                        self._trigger_event,
                        ('Repeat',)
                        )

                    self._timer.start()
            event.wait(self._poll_rate)
        self.reset()


class XBoxControllers(eg.PluginBase):
    def __init__(self):
        self.AddAction(SetFFB)
        self.AddAction(PowerOff)
        self.AddAction(EnableMouse)
        self.AddAction(DisableMouse)

        self.controllers = []
        self.event = threading.Event()

    def __start__(self):

        while self.event.isSet():
            pass

        for i in range(4):
            controller = Controller(self, i)
            thread = threading.Thread(
                name=__name__ + '.Controller' + str(i + 1),
                target=controller.update,
                args=(self.event,)
            )

            controller.thread = thread
            self.controllers += [controller]
            thread.start()

    def __stop__(self):
        self.event.set()
        for controller in self.controllers:
            try:
                controller.thread.join(3.0)
            except:
                pass
        del self.controllers[:]
        self.event.clear()


class SetFFB(eg.ActionBase):
    name = 'Set Force Feedback'
    description = 'Set a controllers vibration (if supported).'

    def __call__(self, controller_id, l_motor=0, r_motor=0):
        controller = self.plugin.controllers[controller_id - 1]

        if not controller.is_connected():
            eg.PrintNotice(
                'Controller %d is not connected.' % controller_id
            )
            return False

        controller.set_ffb(l_motor, r_motor)
        return True

    def GetLabel(self, controller_id=1, l_motor=0, r_motor=0):
        label = '%s: ' % self.name
        label += 'Controller %d: ' % controller_id
        label += 'Left Vibration Speed: %d ' % l_motor
        label += 'Right Vibration Speed: %d' % r_motor

        return label

    def Configure(self, controller_id=1, l_motor=0, r_motor=0):
        panel = eg.ConfigPanel()
        choices = list('Controller %d' % (i + 1,) for i in range(4))
        status_ctrl = panel.StaticText('')
        controller_st = panel.StaticText('Controller:')
        controller_ctrl = panel.Choice(
            value=controller_id - 1,
            choices=choices
        )

        left_motor_st = panel.StaticText('Left Vibration Speed:')
        left_motor_ctrl = panel.SpinIntCtrl(l_motor, min=0, max=100)
        right_motor_st = panel.StaticText('Right Vibration Speed:')
        right_motor_ctrl = panel.SpinIntCtrl(r_motor, min=0, max=100)

        status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        controller_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_sizer = wx.BoxSizer(wx.HORIZONTAL)

        status_sizer.AddStretchSpacer()
        status_sizer.Add(status_ctrl, 0, wx.EXPAND)
        status_sizer.AddStretchSpacer()

        controller_sizer.Add(controller_st, 0, wx.EXPAND | wx.ALL, 5)
        controller_sizer.Add(controller_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        left_sizer.Add(left_motor_st, 0, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(left_motor_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        right_sizer.Add(right_motor_st, 0, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(right_motor_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(status_sizer, 0, wx.EXPAND)
        panel.sizer.Add(controller_sizer, 0, wx.EXPAND)
        panel.sizer.Add(left_sizer, 0, wx.EXPAND)
        panel.sizer.Add(right_sizer, 0, wx.EXPAND)

        eg.EqualizeWidths((controller_st, left_motor_st, right_motor_st))
        eg.EqualizeWidths((controller_ctrl, left_motor_ctrl, right_motor_ctrl))

        event = threading.Event()

        def poll():
            while not event.isSet():
                selection = controller_ctrl.GetValue()
                controller = self.plugin.controllers[selection]
                old_label = status_ctrl.GetLabel()

                if not controller.is_connected():
                    new_label = (
                        'Controller %d is not connected.' % (selection + 1,)
                    )
                else:
                    new_label = (
                        'To stop the vibrations you have to make another\n'
                        'action with 0\'s for the speeds'
                    )

                if new_label != old_label:
                    status_ctrl.SetLabel(new_label)
                    panel.Layout()
                    panel.Refresh()

                event.wait(0.1)

        thread = threading.Thread(
            name=__name__ + '.' + self.__class__.__name__,
            target=poll
        )
        thread.start()

        while panel.Affirmed():
            panel.SetResult(
                controller_ctrl.GetValue() + 1,
                left_motor_ctrl.GetValue(),
                right_motor_ctrl.GetValue()
            )

        event.set()
        thread.join(1.0)


class EnableMouse(eg.ActionBase):
    name = 'Enable Mouse Control'
    description = 'Enable controlling the mouse from the controller.'

    def __call__(
        self,
        controller_id=1,
        analog_stick='right_analog',
        absolute=False
    ):
        for controller in self.plugin.controllers:
            controller.disable_mouse()

        controller = self.plugin.controllers[controller_id - 1]
        controller.enable_mouse(analog_stick, absolute)

    def GetLabel(
        self,
        controller_id=1,
        analog_stick='right_analog',
        absolute=False
    ):
        return (
            '%s: Controller %d Joystick: %s Absolute: %s' %
            (self.name, controller_id, analog_stick, str(absolute))
        )

    def Configure(
        self,
        controller_id=1,
        analog_stick='right_analog',
        absolute=False
    ):
        panel = eg.ConfigPanel()

        choices = list('Controller %d' % (i + 1,) for i in range(4))
        controller_st = panel.StaticText('Controller:')
        controller_ctrl = panel.Choice(
            value=controller_id - 1,
            choices=choices
        )

        choices = ['left_analog', 'right_analog']
        joystick_st = panel.StaticText('Joystick:')
        joystick_ctrl = panel.Choice(
            value=choices.index(analog_stick),
            choices=choices
        )

        absolute_st = panel.StaticText('Use Absolute Positioning:')
        absolute_ctrl = wx.CheckBox(panel, -1, '')

        absolute_ctrl.SetValue(absolute)

        controller_sizer = wx.BoxSizer(wx.HORIZONTAL)
        controller_sizer.Add(controller_st, 0, wx.EXPAND | wx.ALL, 5)
        controller_sizer.Add(controller_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        joystick_sizer = wx.BoxSizer(wx.HORIZONTAL)
        joystick_sizer.Add(joystick_st, 0, wx.EXPAND | wx.ALL, 5)
        joystick_sizer.Add(joystick_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        absolute_sizer = wx.BoxSizer(wx.HORIZONTAL)
        absolute_sizer.Add(absolute_st, 0, wx.EXPAND | wx.ALL, 5)
        absolute_sizer.Add(absolute_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        panel.sizer.Add(controller_sizer, 0, wx.EXPAND)
        panel.sizer.Add(joystick_sizer, 0, wx.EXPAND)
        panel.sizer.Add(absolute_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                controller_ctrl.GetValue() + 1,
                joystick_ctrl.GetStringSelection(),
                absolute_ctrl.GetValue()
            )


class DisableMouse(eg.ActionBase):
    name = 'Disable Mouse Control'
    description = 'Stops a controller from controlling the mouse.'

    def __call__(self):
        for controller in self.plugin.controllers:
            controller.disable_mouse()


class PowerOff(eg.ActionBase):
    name = 'Turn Off Controller'
    description = 'Powers off a non bluetooth controller.'

    def __call__(self, controller_id=1):
        return XInputPowerOffController(controller_id - 1)

    def GetLabel(self, controller_id=1):
        return '%s: Controller %d' % (self.name, controller_id)

    def Configure(self, controller_id=1):
        panel = eg.ConfigPanel()

        choices = list('Controller %d' % (i + 1,) for i in range(4))
        controller_st = panel.StaticText('Controller:')
        controller_ctrl = panel.Choice(
            value=controller_id - 1,
            choices=choices
        )

        controller_sizer = wx.BoxSizer(wx.HORIZONTAL)
        controller_sizer.Add(controller_st, 0, wx.EXPAND | wx.ALL, 5)
        controller_sizer.Add(controller_ctrl, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(controller_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(controller_ctrl.GetValue() + 1)

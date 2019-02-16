# -*- coding: utf-8 -*-
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

import eg

ICON = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QArABNAAA01td7
AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QQHDwonssmjmQAAAIx0RVh0Q29tbWVudABNZW
51LXNpemVkIGljb24KPT09PT09PT09PQoKKGMpIDIwMDMgSmFrdWIgJ2ppbW1hYycgU3RlaW5lciwg
Cmh0dHA6Ly9qaW1tYWMubXVzaWNoYWxsLmN6CgpjcmVhdGVkIHdpdGggdGhlIEdJTVAsCmh0dHA6Ly
93d3cuZ2ltcC5vcmdnisdHAAACIUlEQVQ4y5WSy2tTQRTGf5Pc5CbW0qSxNvXRh6C4SbAU/4KCexGK
iIKoIFgIwYWtD7TdiC5ECgqCSBZd1boTRNCFuyJUsxNEFCoVNTW3afTmdW/muLhpmkKy6IEDw/DNN7
/55ig61MezhP+q3TNhKV8CfOsqsmBQvzo+Xyi16lSnw3V83/oO7Y0b4RCiNY5dZu37urWhegZPzOft
Ta2vnYFGpWNDsbivK4zr92MVa9iuj4Ej/b3A/Vatr8MLUoFdYfymiREMEAwa/F61iA7GicjGmVahkU
pPzgB3WjfLVganVMHK2XRHuyjm/+HWHNyqQ0WZ0VT6sjSksyqVnpS5h4+2Xf/r5T2qy3NYuSL5tRKi
YN/wHqKxLuqHL3Dw1G1s2+bGrSkMAK01hUJhC+v4OXJvHtM/1MfIaA+GGaD48w+5VYcD5y9iWRZBM7
iVgWjxWrxWgRAD15dY1Kf5uvSFz+8+8ao0zv6b71GBECICjUd4BKLRIiDifawAhokb6mXkwSorKyvk
376GgInWGsAzaRKIYL24xo/pYdYXpxpEGrfutiQjSF0jutENA6OZ/PICUitRWl6g++RdAI4lR3n67E
lzXRfdRG/mtRliaGyCyofnhMYm0FqjREgkkiQSSUQUSomH3zDYRmCaJkevZIBM26mybW9yy+UyAJVK
ZTtBNpvFdV12UkqpLYNIJNJEAqhWqwDUarWOBo7jeEbtRnkHNfsfqMAAn2HmrMwAAAAASUVORK5CYI
I="""

eg.RegisterPlugin(
    name="Joystick",
    author="K",
    version="2.0.0",
    kind="remote",
    guid="{615F3B89-FB7E-4FD9-B7D5-9F07FEF0BED9}",
    description=(
        "Use joysticks and game pads as input devices for EventGhost."
    ),
    icon=ICON,
)

import ctypes # NOQA
from copy import deepcopy # NOQA
import threading # NOQA
from ctypes.wintypes import UINT # NOQA
import joystickapi_h # NOQA

UINT_PTR = ctypes.c_uint32


class Joystick(eg.PluginBase):

    def __init__(self):
        super(Joystick, self).__init__()
        self._event = threading.Event()
        self._thread = None
        self.last_joy_states = {}

    def __start__(self):
        while self._event.isSet():
            pass

        self._thread = threading.Thread(target=self.loop)
        self._thread.daemon = True
        self._thread.start()

    def get_joy_data(self, joy_id):
        joy_caps = joystickapi_h.JOYCAPS()
        res = joystickapi_h.joyGetDevCaps(
            UINT_PTR(joy_id),
            ctypes.byref(joy_caps),
            ctypes.sizeof(joystickapi_h.JOYCAPS)
        )

        if res != joystickapi_h.MMSYSERR_NODRIVER:
            joy_info = joystickapi_h.JOYINFOEX()
            joy_info.dwSize = ctypes.sizeof(joystickapi_h.JOYINFOEX)

            joystickapi_h.joyGetPosEx(
                UINT_PTR(joy_id),
                ctypes.byref(joy_info)
            )

            if joystickapi_h.JOY_RETURNBUTTONS & joy_info.dwFlags:
                buttons = ['Released'] * joy_caps.wNumButtons
                for i in range(1, joy_caps.wNumButtons):
                    button = getattr(joystickapi_h, 'JOY_BUTTON' + str(i))
                    if joy_info.dwButtons & button:
                        buttons[i - 1] = 'Pressed'
            else:
                buttons = []

            if joystickapi_h.JOY_RETURNX & joy_info.dwFlags:
                first_axis_x = joy_info.dwXpos
            else:
                first_axis_x = None

            first_axis_x = dict(
                axis='x',
                position=first_axis_x,
                max=joy_caps.wXmax,
                min=joy_caps.wXmin

            )

            if joystickapi_h.JOY_RETURNY & joy_info.dwFlags:
                second_axis_y = joy_info.dwYpos
            else:
                second_axis_y = None

            second_axis_y = dict(
                axis='y',
                position=second_axis_y,
                max=joy_caps.wYmax,
                min=joy_caps.wYmin

            )

            res = dict(
                id=joy_id,
                name=joy_caps.szPname,
                num_axis=joy_caps.wNumAxes,
                buttons=buttons,
                first_axis=first_axis_x,
                second_axis=second_axis_y
            )

            if joystickapi_h.JOYCAPS_HASZ & joy_caps.wCaps:
                if joystickapi_h.JOY_RETURNZ & joy_info.dwFlags:
                    third_axis_z = joy_info.dwZpos
                else:
                    third_axis_z = None

                res['third_axis'] = dict(
                    axis='z',
                    position=third_axis_z,
                    max=joy_caps.wZmax,
                    min=joy_caps.wZmin
                )

            if joystickapi_h.JOYCAPS_HASR & joy_caps.wCaps:
                if joystickapi_h.JOY_RETURNR & joy_info.dwFlags:
                    fourth_axis_r = joy_info.dwRpos
                else:
                    fourth_axis_r = None

                res['fourth_axis'] = dict(
                    axis='r',
                    position=fourth_axis_r,
                    max=joy_caps.wRmax,
                    min=joy_caps.wRmin
                )

            if joystickapi_h.JOYCAPS_HASU & joy_caps.wCaps:
                if joystickapi_h.JOY_RETURNU & joy_info.dwFlags:
                    fifth_axis_u = joy_info.dwUpos
                else:
                    fifth_axis_u = None

                res['fifth_axis'] = dict(
                    axis='u',
                    position=fifth_axis_u,
                    max=joy_caps.wUmax,
                    min=joy_caps.wUmin
                )

            if joystickapi_h.JOYCAPS_HASV & joy_caps.wCaps:
                if joystickapi_h.JOY_RETURNV & joy_info.dwFlags:
                    sixth_axis_v = joy_info.dwVpos
                else:
                    sixth_axis_v = None

                res['sixth_axis'] = dict(
                    axis='v',
                    position=sixth_axis_v,
                    max=joy_caps.wVmax,
                    min=joy_caps.wVmin

                )

            if joystickapi_h.JOYCAPS_HASPOV & joy_caps.wCaps:

                if joystickapi_h.JOY_RETURNPOV & joy_info.dwFlags:
                    degrees = joy_info.dwPOV
                    if degrees != -1:
                        degrees /= 100.0
                else:
                    degrees = None

                res['pov'] = dict(degrees=degrees)

            return res

    def loop(self):
        for joy_id in range(joystickapi_h.joyGetNumDevs()):
            joy_data = self.get_joy_data(joy_id)
            if joy_data is not None:
                self.last_joy_states[(joy_data['id'], joy_data['name'])] = (
                    joy_data
                )

        while not self._event.isSet():
            new_data = {}
            for joy_id in range(joystickapi_h.joyGetNumDevs()):
                joy_data = self.get_joy_data(joy_id)
                if joy_data is not None:
                    new_data[(joy_data['id'], joy_data['name'])] = joy_data

            for key in sorted(new_data.keys()):
                new_value = new_data[key]

                if key not in self.last_joy_states:
                    self.TriggerEvent('Device.Added', deepcopy(new_value))
                else:
                    old_value = self.last_joy_states.pop(key)
                    if new_value != old_value:
                        def iter_dicts(old, new, event=''):
                            for k in new.keys():
                                if old[k] != new[k]:
                                    if isinstance(old[k], dict):
                                        evt = k.replace('_', '').title()
                                        evt = evt.replace(' ', '')
                                        if event:
                                            iter_dicts(
                                                old[k],
                                                new[k],
                                                event + '.' + evt
                                            )
                                        else:
                                            iter_dicts(
                                                old[k],
                                                new[k],
                                                evt
                                            )
                                    elif isinstance(old[k], list):
                                        for num, o_state in enumerate(old[k]):
                                            n_state = new[k][num]
                                            if o_state != n_state:
                                                evt = (
                                                    new_value['name'] +
                                                    '-' +
                                                    str(new_value['id']) +
                                                    '.' +
                                                    'Button' +
                                                    str(num) +
                                                    '.' +
                                                    n_state
                                                )
                                                self.TriggerEvent(
                                                    evt,
                                                    deepcopy(new_value)
                                                )
                                    else:
                                        evt = k.replace('_', '').title()
                                        evt = evt.replace(' ', '')
                                        if event:
                                            evt = event + '.' + evt
                                        evt = (
                                            new_value['name'] +
                                            '-' +
                                            str(new_value['id']) +
                                            '.' +
                                            evt
                                        )

                                        self.TriggerEvent(
                                            evt,
                                            deepcopy(new_value)
                                        )

                        iter_dicts(old_value, new_value)

            for key in sorted(self.last_joy_states.keys()):
                self.TriggerEvent(
                    'Device.Removed',
                    deepcopy(self.last_joy_states[key])
                )

            self.last_joy_states.clear()
            self.last_joy_states = deepcopy(new_data)
            self._event.wait(0.15)

        self.last_joy_states.clear()
        self._thread = None
        self._event.clear()

    def __stop__(self):
        if self._thread is not None:
            self._event.set()
            self._thread.join(3.0)

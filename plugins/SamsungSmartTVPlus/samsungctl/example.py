# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2018 EventGhost Project <http://eventghost.net/>
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

import time
import logging
import sys
logging.disable(logging.DEBUG)
logging.disable(logging.WARNING)
logging.disable(logging.INFO)


if sys.version_info[0] >= 3:
    raw_input = input

answer = raw_input(
    'This example is going to change some of the settings on your TV. '
    'It should change them back to what they were before hand. \n'
    'But seeing how how this is still in a test phase. It could stop running '
    'and not change your settings back to where they were.\n\n'
    'Would you like to continue? y/n'
)

if not answer.lower().startswith('y'):
    sys.exit(0)


from . import remote

for tv in remote.discover(5):
    break
else:
    raise RuntimeError('TV not found')

tv.open()
volume = tv.volume

print('volume:', volume)
time.sleep(2)
tv.volume = 10
print('volume:', tv.volume)
time.sleep(2)
tv.volume = volume

mute = tv.mute

print('mute:', mute)
time.sleep(2)
tv.mute = not mute
print('mute:', tv.mute)
time.sleep(2)

tv.mute = mute

source = tv.source
print('source name:', source.name, 'source label:', source.label)
time.sleep(4)

for src in tv.source_list:
    if not src.is_active and src.is_connected:
        src.activate()
        break

time.sleep(4)
source.activate()

time.sleep(4)
for src in tv.source_list:
    if src.is_editable and src.is_connected:
        src.activate()
        break
else:
    src = None

if src is not None:
    time.sleep(4)

    label = src.label
    print('source label:', label)
    time.sleep(2)
    src.label = 'SAMSUNGCTL'
    time.sleep(4)

    if src == source:
        for new_src in tv.source_list:
            if not new_src.is_active and new_src.is_connected:
                new_src.activate()

                break
        else:
            pass

    else:
        source.activate()

    print('source_label:', src.label)
    time.sleep(4)
    src.activate()
    time.sleep(4)
    src.label = label

source.activate()
time.sleep(4)
brightness = tv.brightness
contrast = tv.contrast
color_temperature = tv.color_temperature
sharpness = tv.sharpness

print('brightness:', brightness)
print('contrast:', contrast)
print('color temperature:', color_temperature)
print('sharpness:', sharpness)

tv.brightness = 10
print('brightness:', tv.brightness)
time.sleep(4)
tv.brightness = brightness
time.sleep(4)
tv.contrast = 10
print('contrast:', tv.contrast)
time.sleep(4)
tv.contrast = contrast
time.sleep(4)
tv.color_temperature = 2
print('color temperature:', tv.color_temperature)
time.sleep(4)
tv.color_temperature = color_temperature
time.sleep(4)
tv.sharpness = 40
print('sharpness:', tv.sharpness)
time.sleep(4)
tv.sharpness = sharpness
time.sleep(4)

print('brightness:', tv.brightness)
print('contrast:', tv.contrast)
print('color temperature:', tv.color_temperature)
print('sharpness:', tv.sharpness)


print('channel_list:', )
for channel in tv.channel_list['supported_channels']:
    print('   ', channel)

print('year:', tv.year)
print('model:', tv.model)
print('region:', tv.region)
print('dtv support:', tv.dtv_support)
print('pvr_support:', tv.pvr_support)
print('tuner count:', tv.tuner_count)
print('panel technology:', tv.panel_technology)
print('panel type:', tv.panel_type)
print('panel size:', tv.size)
print('watching information:', tv.watching_information)
print('position info:', tv.position_info)
print('channel:', tv.channel)
print('channel:', tv.channel)
print('operating system:', tv.operating_system)
print('frame tv support:', tv.frame_tv_support)
print('game pad support:', tv.game_pad_support)
print('voice support:', tv.voice_support)
print('firmware version:', tv.firmware_version)
print('network type:', tv.network_type)
print('resolution:', tv.resolution)
print('wifi mac:', tv.wifi_mac)


print(
    'This is a list of all available methods, arguments,\n'
    'argument data types, default values, minimum/maximum\n'
    'values, choices, return values, and return data types.\n'
)

print('\n')
time.sleep(3)
print(tv)

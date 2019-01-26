# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

from __core_audio.enum import EChannelMapping
from __core_audio.constant import (
    KSAUDIO_SPEAKER_DIRECTOUT,
    KSAUDIO_SPEAKER_MONO,
    KSAUDIO_SPEAKER_1POINT1,
    KSAUDIO_SPEAKER_STEREO,
    KSAUDIO_SPEAKER_2POINT1,
    KSAUDIO_SPEAKER_3POINT0,
    KSAUDIO_SPEAKER_3POINT1,
    KSAUDIO_SPEAKER_QUAD,
    KSAUDIO_SPEAKER_SURROUND,
    KSAUDIO_SPEAKER_5POINT0,
    KSAUDIO_SPEAKER_5POINT1,
    KSAUDIO_SPEAKER_7POINT0,
    KSAUDIO_SPEAKER_7POINT1,
    KSAUDIO_SPEAKER_5POINT1_SURROUND,
    KSAUDIO_SPEAKER_7POINT1_SURROUND,
)

KSAUDIO_SPEAKER = {
    KSAUDIO_SPEAKER_DIRECTOUT: dict(
        front_left=False,
        front_right=False,
        center=False,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=False,
        string='Direct'
    ),
    KSAUDIO_SPEAKER_MONO: dict(
        front_left=False,
        front_right=False,
        center=True,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=False,
        string='Mono'
    ),
    KSAUDIO_SPEAKER_1POINT1: dict(
        front_left=False,
        front_right=False,
        center=True,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=True,
        string='Mono with subwoofer'
    ),
    KSAUDIO_SPEAKER_STEREO: dict(
        front_left=True,
        front_right=True,
        center=False,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=False,
        string='Stereo'
    ),
    KSAUDIO_SPEAKER_2POINT1: dict(
        front_left=True,
        front_right=True,
        center=False,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=True,
        string='Stereo with subwoofer'
    ),
    KSAUDIO_SPEAKER_3POINT0: dict(
        front_left=True,
        front_right=True,
        center=True,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=False,
        string='3.0'
    ),
    KSAUDIO_SPEAKER_3POINT1: dict(
        front_left=True,
        front_right=True,
        center=True,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=True,
        string='3.1'
    ),
    KSAUDIO_SPEAKER_QUAD: dict(
        front_left=True,
        front_right=True,
        center=False,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=True,
        back_right=True,
        back_center=False,
        subwoofer=False,
        string='Quad'
    ),
    KSAUDIO_SPEAKER_SURROUND: dict(
        front_left=True,
        front_right=True,
        center=True,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=False,
        back_right=False,
        back_center=True,
        subwoofer=False,
        string='Surround'
    ),
    KSAUDIO_SPEAKER_5POINT0: dict(
        front_left=True,
        front_right=True,
        center=True,
        high_left=False,
        high_right=False,
        side_left=True,
        side_right=True,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=False,
        string='5.0'
    ),
    KSAUDIO_SPEAKER_5POINT1: dict(
        front_left=True,
        front_right=True,
        center=True,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=True,
        back_right=True,
        back_center=False,
        subwoofer=True,
        string='5.1'
    ),
    KSAUDIO_SPEAKER_7POINT0: dict(
        front_left=True,
        front_right=True,
        center=True,
        high_left=False,
        high_right=False,
        side_left=True,
        side_right=True,
        back_left=True,
        back_right=True,
        back_center=False,
        subwoofer=False,
        string='7.0'
    ),
    KSAUDIO_SPEAKER_7POINT1: dict(
        front_left=True,
        front_right=True,
        center=True,
        high_left=True,
        high_right=True,
        side_left=False,
        side_right=False,
        back_left=True,
        back_right=True,
        back_center=False,
        subwoofer=True,
        string='7.1'
    ),
    KSAUDIO_SPEAKER_5POINT1_SURROUND: dict(
        front_left=True,
        front_right=True,
        center=True,
        high_left=False,
        high_right=False,
        side_left=True,
        side_right=True,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=True,
        string='5.1 Surround'
    ),
    KSAUDIO_SPEAKER_7POINT1_SURROUND: dict(
        front_left=True,
        front_right=True,
        center=True,
        high_left=False,
        high_right=False,
        side_left=True,
        side_right=True,
        back_left=True,
        back_right=True,
        back_center=False,
        subwoofer=True,
        string='7.1 Surround'
    )
}

CHANNEL_MAPPING = {
    EChannelMapping.ePcxChanMap_FL_FR: (
        KSAUDIO_SPEAKER[KSAUDIO_SPEAKER_STEREO]
    ),
    EChannelMapping.ePcxChanMap_FC_LFE: (
        KSAUDIO_SPEAKER[KSAUDIO_SPEAKER_1POINT1]
    ),
    EChannelMapping.ePcxChanMap_FLC_FRC: (
        KSAUDIO_SPEAKER[KSAUDIO_SPEAKER_3POINT0]
    ),
    EChannelMapping.ePcxChanMap_BL_BR: dict(
        front_left=False,
        front_right=False,
        center=False,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=True,
        back_right=True,
        back_center=False,
        subwoofer=False,
        string='Back left & right'
    ),

    EChannelMapping.ePcxChanMap_SL_SR: dict(
        front_left=False,
        front_right=False,
        center=False,
        high_left=False,
        high_right=False,
        side_left=True,
        side_right=True,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=False,
        string='Side left & right'
    ),
    EChannelMapping.ePcxChanMap_Unknown: dict(
        front_left=False,
        front_right=False,
        center=False,
        high_left=False,
        high_right=False,
        side_left=False,
        side_right=False,
        back_left=False,
        back_right=False,
        back_center=False,
        subwoofer=False,
        string='Unknown'
    ),
}


class AudioSpeakers(object):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value is None:
            return 'None'
        return KSAUDIO_SPEAKER[self.value]['string']

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if self.value is None:
            raise AttributeError

        if item in KSAUDIO_SPEAKER[self.value]:
            return KSAUDIO_SPEAKER[self.value][item]

        raise AttributeError

# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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

import os
import pyIRDecoder
from pyIRDecoder import high_precision_timers

# Local imports
import eg

DEBUG = eg.debugLevel


class IrDecoder(object):
    def __init__(self, plugin, sampleTime=0, config_path=None):

        if config_path is None:
            config_path = os.path.join(eg.configDir, 'ir_decoders', plugin.info.name + '.xml')

        config = pyIRDecoder.Config(config_path)
        self._decoder = pyIRDecoder.IRDecoder(config)
        self._config = config

        self._last_code = None
        self.last_code = None
        self.plugin = plugin
        self.sampleTime = sampleTime
        self.lastDecoder = None
        self.event = None
        self.mapTable = {}
        self._stream_registered = False
        self.timer = high_precision_timers.TimerUS()

    @property
    def config(self):
        return self._config

    def __iter__(self):
        return iter(self._decoder)

    @property
    def decoders(self):
        return iter(self._decoder)

    def Close(self):
        self._decoder.close()

    def DecodeStream(self, data, frequency):
        if not self._stream_registered:
            self._stream_registered = True
            self._decoder.bind_callback(self._stream_callback)

        self._decoder.stream_decode(data, frequency)

    def _stream_callback(self, code):
        if code.decoder != self._decoder.Universal:
            code.save()

        if self._last_code is None or self._last_code != code:
            self.timer.reset()
            self.event = self.plugin.TriggerEnduringEvent(str(code), code)
            self._last_code = code
            self.last_code = code
            code.bind_released_callback(self.OnTimeout)

    def Decode(self, data, length=-1, frequency=0):
        if length < 3 and length != -1:
            return

        if length == -1:
            code = self._decoder.decode(data, frequency)
        else:
            code = self._decoder.decode(data[:length], frequency)

        if code is None:
            return

        if self._last_code is None or self._last_code != code:
            self.event = self.plugin.TriggerEnduringEvent(str(code), code)
            self._last_code = code
            self.last_code = code
            code.bind_released_callback(self.OnTimeout)

    def OnTimeout(self, code):
        if self._last_code is not None and self._last_code == code:
            self.event.SetShouldEnd()
            self._last_code = None

        code.unbind_released_callback(self.OnTimeout)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return getattr(self._decoder, item)


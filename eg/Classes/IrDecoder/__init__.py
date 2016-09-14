# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

import os
from collections import deque
from glob import glob

# Local imports
import eg
from eg.Classes.IrDecoder.Universal import IrProtocolBase, Universal

DECODERS_DIR = os.path.dirname(__file__.decode('mbcs'))
DEBUG = eg.debugLevel

# Exceptions
class DecodeError(Exception):  # Raised if code doesn't match expectation.
    pass

class IrDecoder(object):
    def __init__(self, plugin, sampleTime):
        self.plugin = plugin
        self.sampleTime = sampleTime
        self.lastDecoder = None
        self.event = None
        self.decoders = deque()
        self.mapTable = {}
        for decoderCls in DECODERS:
            decoder = decoderCls(self)
            if decoderCls == Universal:
                self.universalDecoder = decoder
                continue
            self.decoders.append(decoder)
        self.timer = eg.ResettableTimer(self.OnTimeout)

    def Close(self):
        self.timer.Stop()

    def Decode(self, data, length=-1):
        if length < 3:
            return

        #print dataLen, repr(data)
        if isinstance(data, str):
            data = [int(ord(x) * self.sampleTime) for x in data[:length]]
        else:
            data = [int(x * self.sampleTime) for x in data[:length]]
        #data.append(10000)

        uniCode = None
        if self.lastDecoder == self.universalDecoder:
            uniCode = self.universalDecoder.Decode(data)
            if self.universalDecoder.lastCode == uniCode:
                self.timer.Reset(self.universalDecoder.timeout)
                return uniCode

        #print data
        decoders = self.decoders
        code = None
        for i, decoder in enumerate(decoders):
            try:
                code = decoder.Decode(data)
            except (IndexError, DecodeError), exc:
                if DEBUG:
                    print decoder.__class__.__name__ + ": " + str(exc)
                continue
            except Exception, exc:
                print decoder
                raise exc

            if code is None:
                continue
            if i != 0:
                del decoders[i]
                decoders.appendleft(decoder)
            break
        if code is None:
            decoder = self.universalDecoder
            if uniCode is None:
                code = decoder.Decode(data)
            else:
                code = uniCode

        self.lastDecoder = decoder
        timeout = decoder.timeout
        if code in self.mapTable:
            code, timeout2, self.repeatCode = self.mapTable[code]
            if timeout2 is not None:
                timeout = timeout2
        if code != decoder.lastCode:
            self.event = self.plugin.TriggerEnduringEvent(code)
        decoder.lastCode = code
        self.timer.Reset(timeout)

    def OnTimeout(self):
        self.lastDecoder.lastCode = None
        self.event.SetShouldEnd()
#        if DEBUG:
#            print "timeout"


class ManchesterBase(IrProtocolBase):
    pos = 0
    data = None
    bitState = 0
    bufferLen = 0
    halfBitTime = None

    def __init__(self, controller, halfBitTime):
        IrProtocolBase.__init__(self, controller)
        self.halfBitTime = halfBitTime

    def Decode(self, data):
        raise NotImplementedError

    def GetBit(self):
        raise NotImplementedError

    def GetBitsLsbFirst(self, numBits=8):
        """
        Returns numBits count manchester bits with LSB last order.
        """
        data = 0
        mask = 1
        for dummyCounter in range(numBits):
            data |= mask * self.GetBit()
            mask <<= 1
        return data

    def GetBitsLsbLast(self, numBits=8):
        """
        Returns numBits count manchester bits with LSB last order.
        """
        data = 0
        for dummyCounter in range(numBits):
            data <<= 1
            data |= self.GetBit()
        return data

    def GetSample(self):
        if self.bufferLen == 0:
            if self.pos >= len(self.data):
                raise DecodeError("not enough timings")
            self.bufferLen = (
                (self.data[self.pos] + 2 * self.halfBitTime / 3) / self.halfBitTime
            )
            if self.bufferLen == 0:
                raise DecodeError("duration too short")
            self.pos += 1
            self.bitState = self.pos % 2
        self.bufferLen -= 1
        return self.bitState

    def SetData(self, data, pos=0):
        self.data = data
        self.pos = pos
        self.bufferLen = 0
        self.bitState = 0


class ManchesterCoding1(ManchesterBase):
    """
    Manchester coding with falling edge for logic one.
    """
    def Decode(self, data):
        raise NotImplementedError

    def GetBit(self):
        sample = self.GetSample() * 2 + self.GetSample()
        if sample == 1:  # binary 01
            return 0
        elif sample == 2:  # binary 10
            return 1
        else:
            raise DecodeError("wrong bit transition")


class ManchesterCoding2(ManchesterBase):
    """
    Manchester coding with raising edge for logic one.
    """
    def Decode(self, data):
        raise NotImplementedError

    def GetBit(self):
        sample = self.GetSample() * 2 + self.GetSample()
        if sample == 1:  # binary 01
            return 1
        elif sample == 2:  # binary 10
            return 0
        else:
            raise DecodeError("wrong bit transition")


def GetBitString(value, numdigits=8):
    digits = []
    for dummyCounter in range(numdigits):
        if value & 1:
            digits.append("1")
        else:
            digits.append("0")
        value >>= 1
    return "".join(reversed(digits))

def GetDecoders():
    decoders = []
    for path in glob(os.path.join(DECODERS_DIR, "*.py")):
        name = os.path.basename(path)
        moduleName = os.path.splitext(name)[0]
        if moduleName.startswith("_"):
            continue
        module = __import__(moduleName, globals())
        decoders.append(getattr(module, moduleName))
    return decoders

DECODERS = GetDecoders()

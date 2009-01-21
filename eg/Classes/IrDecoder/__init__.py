# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

from collections import deque



class DecodeError(Exception):
    """ Raised if the code doesn't match the expectation. """
    
    
from Rc5 import Rc5Decoder
from Rc6 import Rc6Decoder
from Sharp import SharpDecoder
from Sony import SonyDecoder
from Nec import NecDecoder
from Recs80 import Recs80Decoder



class IrDecoder:
    
    def __init__(self, sampleTime):
        self.sampleTime = sampleTime * 1000000
        self.suppressRc5ToggleBit = True
        self.decoders = deque([
            Rc5Decoder().Decode,
            Rc6Decoder().Decode,
            SharpDecoder().Decode,
            SonyDecoder().Decode,
            NecDecoder().Decode,
            Recs80Decoder().Decode,
        ])
        

    def Decode(self, data, dataLen):
        if dataLen < 3:
            return None
        
        data2 = [x * self.sampleTime for x in data[:dataLen]]
        data2.append(10000)

        decoders = self.decoders
        for i, decoder in enumerate(decoders):
            try:
                code = decoder(data2)
            except DecodeError, exc:
                #print decoder.im_self.__class__.__name__, exc
                continue
            if code is None:
                continue
            if i != 0:
                del decoders[i]
                decoders.appendleft(decoder)
            return code
            
        minHigh = 10000
        minLow = 10000
        maxHigh = 0
        maxLow = 0
        for i in xrange(2, dataLen):
            value = data[i]
            if i % 2:
                if value > maxLow:
                    maxLow = value
                if value < minLow:
                    minLow = value
            else:
                if value > maxHigh:
                    maxHigh = value
                if value < minHigh:
                    minHigh = value
                    
        levelHigh = (minHigh + maxHigh) / 2
        levelLow = (minLow + maxLow) / 2
        if (maxHigh - minHigh) < 5:
            levelHigh += 4
        if (maxLow - minLow) < 5:
            levelLow += 4
            
        code = 3L
        for i in xrange(0, dataLen):
            value = data[i]
            code = code << 1
            if i % 2:
                if value > levelLow:
                    code |= 1
            else:
                if value > levelHigh:
                    code |= 1
                    
#        # shift in b'10', so we have an identifiable beginning
#        code = 3L
#        
#        last_mark_time = 0
#        last_space_time = 0
#        tolerance = 2
#        
#        for i in xrange(0, dataLen):
#            # get the raw timing
#            value = data[i]
#            # make room for next bit
#            code = code << 1
#            if i % 2:
#                if (
#                    (value >= last_space_time + tolerance) 
#                    or (value <= last_space_time - tolerance)
#                ):
#                    code |= 1
#                last_space_time = value
#            else:
#                if (
#                    (value >= last_mark_time + tolerance) 
#                    or (value <= last_mark_time - tolerance)
#                ):
#                    code |= 1
#                last_mark_time = value

        return "U%X" % code


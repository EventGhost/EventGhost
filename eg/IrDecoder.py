# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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



def ShiftInBits(data, start, end, threshold):
    buffer = 0
    for i in xrange(start, end + 1, 2):
        buffer <<= 1
        if data[i] >= threshold:
            buffer |= 1
    return buffer
            
            
def ShiftInBitsReverse(data, start, end, threshold):
    buffer = 0
    for i in xrange(end - 1, start - 1, -2):
        buffer <<= 1
        if data[i] >= threshold:
            buffer |= 1
    return buffer
            
            
def Rc5Decode(data, start, end, threshold):
    state = 0
    buffer = 1L
    length = 0
    for i in xrange(start, end):
        value = data[i]
        if state == 0: # Mid1
            if value < threshold:
                state = 1
            else:
                state = 2
                buffer <<= 1
                length += 1
        elif state == 1: # Start1
            if value < threshold:
                state = 0
                buffer <<= 1
                buffer |= 1
                length += 1
            else:
                return None
        elif state == 2: # Mid0
            if value < threshold:
                state = 3
            else:
                state = 0
                buffer <<= 1
                buffer |= 1
                length += 1
        else: # Start0
            if value < threshold:
                state = 2
                buffer <<= 1
                length += 1
            else:
                return None
    return buffer
                
            
            
class IrDecoder:
    def __init__(self, sampleTime, quality=0.25):
        self.sampleTime = sampleTime
        
        SHARP_TIME = 0.000320  # 320 micro-seconds
        self.SHARP_PULSE_MIN   = self.MakeMinTime(SHARP_TIME)
        self.SHARP_PULSE_MAX   = self.MakeMaxTime(SHARP_TIME)
        self.SHARP_SPACE0_MIN  = self.MakeMinTime(2 * SHARP_TIME)
        self.SHARP_SPACE0_MAX  = self.MakeMaxTime(2 * SHARP_TIME)
        self.SHARP_SPACE1_MIN  = self.MakeMinTime(5 * SHARP_TIME)
        self.SHARP_SPACE1_MAX  = self.MakeMaxTime(5 * SHARP_TIME)
        self.SHARP_THRESHOLD   = self.MakeTime(3.5 * SHARP_TIME)
        
        SIRC_TIME = 0.600e-3   # 600 micro-seconds
        self.SIRC_PREPULSE_MIN = self.MakeMinTime(4 * SIRC_TIME)
        self.SIRC_PREPULSE_MAX = self.MakeMaxTime(4 * SIRC_TIME)
        self.SIRC_SPACE_MIN    = self.MakeMinTime(SIRC_TIME)
        self.SIRC_SPACE_MAX    = self.MakeMaxTime(SIRC_TIME)
        self.SIRC_PULSE0_MIN   = self.MakeMinTime(SIRC_TIME)
        self.SIRC_PULSE0_MAX   = self.MakeMaxTime(SIRC_TIME)
        self.SIRC_PULSE1_MIN   = self.MakeMinTime(2 * SIRC_TIME)
        self.SIRC_PULSE1_MAX   = self.MakeMaxTime(2 * SIRC_TIME)
        self.SIRC_THRESHOLD    = self.MakeTime(1.5 * SIRC_TIME)

        RC5_TIME = 0.889e-3    # 889 micro-seconds
        self.RC5_PULSE_MIN	   = self.MakeMinTime(RC5_TIME)
        self.RC5_PULSE_MAX	   = self.MakeMaxTime(RC5_TIME * 2.0)
        self.RC5_SPACE_MIN	   = self.MakeMinTime(RC5_TIME)
        self.RC5_SPACE_MAX	   = self.MakeMaxTime(RC5_TIME * 2.0)
        self.RC5_THRESHOLD	   = self.MakeTime(RC5_TIME * 1.50)
        self.suppressRc5ToggleBit = True


    def MakeMinTime(self, tvalue):
        return int(round(((tvalue / self.sampleTime) * 0.66) - 2))


    def MakeMaxTime(self, tvalue):
        return int(round(((tvalue / self.sampleTime) * 1.33) + 2))


    def MakeTime(self, tvalue):
        return int(round((tvalue / self.sampleTime)))
    
    
    def Decode(self, data, dataLen):
        if dataLen < 3:
            return None
        min_high = 10000
        min_low = 10000
        max_high = 0
        max_low = 0
        for i in xrange(2, dataLen):
            value = data[i]
            if i % 2:
                if value > max_low:
                    max_low = value
                if value < min_low:
                    min_low = value
            else:
                if value > max_high:
                    max_high = value
                if value < min_high:
                    min_high = value
                    
        prePulse = data[0]
        preSpace = data[1]
        
        #print min_high, max_high, min_low, max_low
        if (
            dataLen == 31 and
            prePulse >= self.SHARP_PULSE_MIN and 
            prePulse <= self.SHARP_PULSE_MAX and 
            preSpace >= self.SHARP_SPACE0_MIN and 
            preSpace <= self.SHARP_SPACE1_MAX and 
            min_high >= self.SHARP_PULSE_MIN and 
            max_high <= self.SHARP_PULSE_MAX and 
            min_low >= self.SHARP_SPACE0_MIN and 
            max_low <= self.SHARP_SPACE1_MAX
            ):
                code = ShiftInBits(data, 1, 30, self.SHARP_THRESHOLD)
                if (code & 256):
                    code ^= 0x03ff
                return "Sharp_%0.4X" % code
            
        if (
            prePulse >= self.SIRC_PREPULSE_MIN and 
            prePulse <= self.SIRC_PREPULSE_MAX and 
            (
                (dataLen == 25) or 
                (dataLen == 31) or 
                (dataLen == 41)
            ) and 
            min_high >= self.SIRC_PULSE0_MIN and 
            max_high <= self.SIRC_PULSE1_MAX and 
            min_low >= self.SIRC_SPACE_MIN and 
            max_low <= self.SIRC_SPACE_MAX and 
            preSpace >= self.SIRC_SPACE_MIN and 
            preSpace <= self.SIRC_SPACE_MAX
        ):
            code = ShiftInBitsReverse(data, 2, dataLen, self.SIRC_THRESHOLD)
            return "SIRC%d_%0.4X" % (dataLen / 2, code)
            
        if (
            prePulse >= self.RC5_PULSE_MIN and 
            prePulse <= self.RC5_PULSE_MAX and 
            preSpace >= self.RC5_SPACE_MIN and 
            preSpace <= self.RC5_SPACE_MAX and 
            min_high >= self.RC5_PULSE_MIN and 
            max_high <= self.RC5_PULSE_MAX and 
            min_low >= self.RC5_SPACE_MIN and 
            max_low <= self.RC5_SPACE_MAX
        ):
            code = Rc5Decode(data, 0, dataLen, self.RC5_THRESHOLD)
            if code is not None:
                if self.suppressRc5ToggleBit:
                    code &= 0xF7FF
                return "RC5_%0.4X" % code

        level_high = (min_high + max_high) / 2
        level_low = (min_low + max_low) / 2
        if (max_high - min_high) < 5:
            level_high += 4
        if (max_low - min_low) < 5:
            level_low += 4
            
        code = 3L
        for i in xrange(0, dataLen):
            value = data[i]
            code = code << 1
            if i % 2:
                if value > level_low:
                    code |= 1
            else:
                if value > level_high:
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

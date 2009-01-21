# This file is part of EventGhost.
# Copyright (C) 2009 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2008-12-29 19:13:21 +0100 (Mo, 29 Dez 2008) $
# $LastChangedRevision: 649 $
# $LastChangedBy: bitmonster $

from eg.Classes.IrDecoder import DecodeError


RC5STATE_MID0 = 0
RC5STATE_MID1 = 1
RC5STATE_START0 = 2
RC5STATE_START1 = 3

RC5EVENT_SHORT_SPACE = 0
RC5EVENT_LONG_SPACE = 1
RC5EVENT_SHORT_PULSE = 2
RC5EVENT_LONG_PULSE = 3

RC5STATE_MID0 = 'RC5STATE_MID0'
RC5STATE_MID1 = 'RC5STATE_MID1'
RC5STATE_START0 = 'RC5STATE_START0'
RC5STATE_START1 = 'RC5STATE_START1'

RC5EVENT_SHORT_SPACE = 'RC5_SHORT_SPACE'
RC5EVENT_LONG_SPACE = 'RC5_LONG_SPACE'
RC5EVENT_SHORT_PULSE = 'RC5_SHORT_PULSE'
RC5EVENT_LONG_PULSE = 'RC5_LONG_PULSE'


class Rc5Decoder(object):
    
    @staticmethod
    def Decode(data):
        buf = 1
        length = 0
        pos = 0
        
        state = RC5STATE_MID1
        while length < 13:
            oldState = state
            duration = data[pos]
            pos += 1
            isPulse = pos % 2
            if duration < 600:
                raise DecodeError("duration to short")
            if duration > 2000:
                raise DecodeError("duration to long")
                
            if isPulse:
                if duration < 1200:
                    event = RC5EVENT_SHORT_PULSE
                else:
                    event = RC5EVENT_LONG_PULSE
            else:
                if duration < 1200:
                    event = RC5EVENT_SHORT_SPACE
                else:
                    event = RC5EVENT_LONG_SPACE
                
            #print event,
            if state == RC5STATE_MID0:
                if event == RC5EVENT_SHORT_SPACE:
                    state = RC5STATE_START0
                elif event == RC5EVENT_LONG_SPACE:
                    buf <<= 1
                    buf |= 1
                    length += 1
                    state = RC5STATE_MID1
            elif state == RC5STATE_MID1:
                if event == RC5EVENT_SHORT_PULSE:
                    state = RC5STATE_START1
                elif event == RC5EVENT_LONG_PULSE:
                    buf <<= 1
                    length += 1
                    state = RC5STATE_MID0
            elif state == RC5STATE_START0:
                if event == RC5EVENT_SHORT_PULSE:
                    buf <<= 1
                    length += 1
                    state = RC5STATE_MID0
            elif state == RC5STATE_START1:
                if event == RC5EVENT_SHORT_SPACE:
                    buf <<= 1
                    buf |= 1
                    length += 1
                    state = RC5STATE_MID1
            #print state
            if oldState == state:
                raise DecodeError("missing state transition")
        return "RC5_%04X" % buf
            

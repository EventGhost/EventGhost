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

class IrProtocolBase(object):
    lastCode = None
    timeout = 150

    def __init__(self, controller):
        self.controller = controller

    def Decode(self, data):
        raise NotImplementedError


class Universal(IrProtocolBase):
    """
    IR decoder for unknown protocols.
    """
    def __init__(self, controller):
        IrProtocolBase.__init__(self, controller)
        self.diffTime = controller.sampleTime * 3

#    def Decode(self, data):
#        print len(data), data
#        sampleTime = self.controller.sampleTime
#        pulses = [x for x in data[2::2]]
#        pauses = [x for x in data[3::2]]
#        pulseMax = max(pulses)
#        pulseMin = min(pulses)
#        pauseMax = max(pauses)
#        pauseMin = min(pauses)
#        pulseLimit = (pulseMin + pulseMax) / 2
#        pauseLimit = (pauseMin + pauseMax) / 2
#        if (pulseMax - pulseMin) < 2 * sampleTime:
#            pulseLimit += 4 * sampleTime
#        if (pauseMax - pauseMin) < 2 * sampleTime:
#            pauseLimit += 4 * sampleTime
#
#        code = 1L
#        for i, value in enumerate(data):
#            code <<= 1
#            if i % 2:
#                if value > pauseLimit:
#                    code |= 1
#            else:
#                if value > pulseLimit:
#                    code |= 1
#        return "U%X" % code

    def Decode(self, data):
        #print data
        lastPause = 0
        lastPulse = 0
        code = 0
        mask = 1
        for i, x in enumerate(data):
            if i % 2:
                diff = max(self.diffTime, lastPause * 0.2)
                if -diff < x - lastPause < diff:
                    code |= mask
                lastPause = x
            else:
                diff = max(self.diffTime, lastPulse * 0.2)
                if -diff < x - lastPulse < diff:
                    code |= mask
                lastPulse = x
            mask <<= 1
        code |= mask
        return "Unknown.%X" % code

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
# $LastChangedDate: 2009-01-25 12:34:22 +0100 (So, 25 Jan 2009) $
# $LastChangedRevision: 800 $
# $LastChangedBy: bitmonster $

import eg

class IrDecoderPlugin(eg.PluginBase):

    def __init__(self, sampleTime):
        eg.PluginBase.__init__(self)
        self.irDecoder = eg.IrDecoder(self, sampleTime)


    def Map(self, what, to, timeout=None, repeatCode=None):
        self.irDecoder.mapTable[what] = (to, timeout, repeatCode)


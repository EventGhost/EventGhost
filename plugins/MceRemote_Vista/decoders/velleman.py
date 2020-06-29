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

from . import protocol_base


class Velleman(protocol_base.IRPNotation):
    """
    IR decoder for the Velleman protocol.
    """
    irp = '{38k,1,msb}<700,-5060|700,-7590>(1:1,T:1,D:3,F:6,1,-55m)+'
    variables = ['D', 'F', 'T']

    def encode(self, device, function, toggle):

        def get_bit(value, bit_num):
            if value & (1 << bit_num) != 0:
                return [self.mark_1, self.space_1]
            else:
                return [self.mark_0, self.space_0]

        encoded_bit1 = [get_bit(1, i) for i in range(1)]
        encoded_function = [get_bit(function, i) for i in range(2, -1, -1)]
        encoded_device = [get_bit(device, i) for i in range(5, -1, -1)]
        encoded_toggle = [get_bit(toggle, i) for i in range(1)]

        packet = encoded_bit1
        packet += encoded_toggle
        packet += encoded_device
        packet += encoded_function
        packet += zip(self.footer_mark, self.footer_space)
        packet = list(item for sublist in packet for item in sublist)

        return Velleman.decode(packet, self.frequency)


Velleman = Velleman()

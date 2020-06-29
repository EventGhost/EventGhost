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


class Sunfire(protocol_base.IRPNotation):
    """
    IR decoder for the Sunfire protocol.
    """
    irp = '{38k,560,msb}<1,-1|3,-1>(16,-8,D:4,F:8,~D:4,~F:8,-32)+'
    variables = ['D', 'F']

    def encode(self, device, function):

        def get_bit(value, bit_num):
            if value & (1 << bit_num) != 0:
                return [self.mark_1, self.space_1]
            else:
                return [self.mark_0, self.space_0]

        encoded_device = []
        encoded_function = []
        device_checksum = []
        function_checksum = []

        for i in range(8):
            encoded_function.insert(0, get_bit(function, i))

            if encoded_function[0][0] == self.mark_1:
                function_checksum.insert(0, [self.mark_0, self.space_0])
            else:
                function_checksum.insert(0, [self.mark_1, self.space_1])

            if i < 4:
                encoded_device.insert(0, get_bit(device, i))

                if encoded_device[0][0] == self.mark_1:
                    device_checksum.insert(0, [self.mark_0, self.space_0])
                else:
                    device_checksum.insert(0, [self.mark_1, self.space_1])

        packet = [[self.header_mark, self.header_space]]
        packet += encoded_device
        packet += encoded_function
        packet += device_checksum
        packet += function_checksum
        packet = list(item for sublist in packet for item in sublist)
        packet[-1] += self.footer_space[0]

        return Sunfire.decode(packet, self.frequency)


Sunfire = Sunfire()

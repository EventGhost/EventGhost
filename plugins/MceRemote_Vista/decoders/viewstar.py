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


class Viewstar(protocol_base.IRPNotation):
    """
    IR decoder for the Viewstar protocol.
    """
    irp = '{50.5k,337}<1,-8|1,-5>(F:5,1,-17)+'
    variables = ['F']

    def encode(self, function):

        def get_bit(value, bit_num):
            if value & (1 << bit_num) != 0:
                return [self.mark_1, self.space_1]
            else:
                return [self.mark_0, self.space_0]

        encoded_function = [get_bit(function, i) for i in range(5)]

        packet = encoded_function
        packet += zip(self.footer_mark, self.footer_space)
        packet = list(item for sublist in packet for item in sublist)

        return Viewstar.decode(packet, self.frequency)


Viewstar = Viewstar()

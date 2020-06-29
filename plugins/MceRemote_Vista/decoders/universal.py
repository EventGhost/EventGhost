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
from . import utils


class Universal(protocol_base.IrProtocolBase):
    """
    IR decoder for unknown protocols.
    """

    def decode(self, data, frequency):

        norm_data = utils.clean_code(data[:], self.tolerance)

        for item in norm_data[:]:
            if norm_data.count(item) == 1:
                norm_data.remove(item)

        if norm_data[0] < 0:
            norm_data = norm_data[1:]

        if norm_data[-1] < 0:
            norm_data = norm_data[:-1]

        diff_time = 3

        # print data
        last_pause = 0
        last_pulse = 0
        code = 0
        mask = 1
        for i, x in enumerate(norm_data):
            if i % 2:
                diff = max(diff_time, last_pause * 0.2)
                if -diff < x - last_pause < diff:
                    code |= mask
                last_pause = x
            else:
                diff = max(diff_time, last_pulse * 0.2)
                if -diff < x - last_pulse < diff:
                    code |= mask

                last_pulse = x
            mask <<= 1
        code |= mask

        params = {'CODE': code, 'frequency': frequency}

        code = protocol_base.IRCode(self, data, norm_data, params)

        print code

        return code

    def _test_decode(self):
        rlc = [[
            9024, -4512, 564, -1692, 564, -564, 564, -1692, 564, -564, 564, -564, 564, -564,
            564, -564, 564, -1692, 564, -564, 564, -564, 564, -564, 564, -564, 564, -1692,
            564, -1692, 564, -564, 564, -564, 564, -1692, 564, -1692, 564, -1692, 564, -564,
            564, -564, 564, -1692, 564, -1692, 564, -564, 564, -564, 564, -564, 564, -1692,
            564, -564, 564, -1692, 564, -564, 564, -564, 564, -1692, 564, -43992,
        ]]

        params = [dict(code=0x3755F777DDDFD7F54)]

        protocol_base.IrProtocolBase._test_decode(self, rlc, params)


Universal = Universal()

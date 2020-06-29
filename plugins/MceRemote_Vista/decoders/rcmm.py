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

# Local imports
from . import DecodeError
from . import macros
from . import code_wrapper
from . import protocol_base

HEADER_MARK = 417
HEADER_SPACE = -278

MARK = 167
LOGICAL_0_SPACE = -278
LOGICAL_1_SPACE = -444
LOGICAL_2_SPACE = -611
LOGICAL_3_SPACE = -778


MODE_MAPPING = {
    0: "OEM",
    1: "Mouse",
    2: "Keyboard",
    3: "Gamepad",
}

SPACE_TO_BIT_MAPPING = {
    LOGICAL_0_SPACE: [0, 0],
    LOGICAL_1_SPACE: [0, 1],
    LOGICAL_2_SPACE: [1, 0],
    LOGICAL_3_SPACE: [1, 1]
}


class RCMM(protocol_base.IrProtocolBase):

    def decode(self, data, frequency):
        # in this protocol each burst pair represents 2 bits
        # so a 12 bit code is going to have 6 burst pairs and
        # a 24 bit code will have 12 burst pairs
        # excluding the header and footer

        try:
            code = self._normalize_rlc(data)
        except ValueError:
            raise DecodeError('Invalid code')

        mode = SPACE_TO_BIT_MAPPING[code.get_burst_pair(1)[-1]]

        if sum(mode) != 0 and code.bits == 6:
            # 12 bit code   |   mode   |   address   |    data   |
            #                  2 bits      2 bits        8 bits

            # mode bits | mode
            # 0 0         24 bit code
            # 0 1         Mouse
            # 1 0         Keyboard
            # 1 1         Gamepad

            address = SPACE_TO_BIT_MAPPING[code.get_burst_pair(2)[-1]]
            command = SPACE_TO_BIT_MAPPING[code.get_burst_pair(3)[-1]]

            for i in range(4, 7):
                command += SPACE_TO_BIT_MAPPING[code.get_burst_pair(1)[-1]]

            decoded_address = 0
            decoded_command = 0

            for bit_num, value in enumerate(address):
                decoded_address = self._set_bit(decoded_address, bit_num, value)

            for bit_num, value in enumerate(command):
                decoded_command = self._set_bit(decoded_command, bit_num, value)

            command = '%02X.%08X' % (decoded_address, decoded_command)

            params = {
                'D': decoded_address,
                'F': decoded_command,
            }

        # extended protocol
        elif code.bits == 12:
            # 24 bit code   |   mode    |         data           |
            #                  4 bits            20 bits
            # mode bits | mode
            # 0 0 0 0     OEM
            # 0 0 0 1     Mouse
            # 0 0 1 0     Keyboard
            # 0 0 1 1     Gamepad

            mode += SPACE_TO_BIT_MAPPING[code.get_burst_pair(2)[-1]]

            # oem version of the protocol
            if sum(mode) == 0:
                # 24 bit OEM code   |   mode    | customer id |   data    |
                #                      6 bits       6 bits       12 bits
                # mode bits   | mode
                # 0 0 0 0 1 1    OEM

                # The mode will always be 0 0 0 0 1 1

                mode += SPACE_TO_BIT_MAPPING[code.get_burst_pair(3)[-1]]
                if sum(mode) != 2:
                    raise DecodeError('Invalid mode')

                # next 6 bits are the manufacturer.
                mfg = SPACE_TO_BIT_MAPPING[code.get_burst_pair(4)[-1]]
                mfg += SPACE_TO_BIT_MAPPING[code.get_burst_pair(5)[-1]]
                mfg += SPACE_TO_BIT_MAPPING[code.get_burst_pair(6)[-1]]

                # then the final 12 bits are the command or data
                command = SPACE_TO_BIT_MAPPING[code.get_burst_pair(7)[-1]]
                for i in range(8, 13):
                    command += SPACE_TO_BIT_MAPPING[code.get_burst_pair(i)[-1]]

                decoded_command = 0
                decoded_manufacturer = 0

                for bit_num, value in enumerate(command):
                    decoded_command = self._set_bit(decoded_command, bit_num, value)

                for bit_num, value in enumerate(mfg):
                    decoded_manufacturer = self._set_bit(decoded_manufacturer, bit_num, value)

                params = {
                    'D': decoded_manufacturer,
                    'F': decoded_command,
                }

            else:
                command = SPACE_TO_BIT_MAPPING[code.get_burst_pair(3)[-1]]

                for i in range(4, 13):
                    command += SPACE_TO_BIT_MAPPING[code.get_burst_pair(3)[-1]]

                decoded_command = 0

                for bit_num, value in enumerate(command):
                    decoded_command = self._set_bit(decoded_command, bit_num, value)

                params = {
                    'F': decoded_command,
                }

        else:
            raise DecodeError('Invalid code')

        decoded_mode = 0
        for bit_num, value in enumerate(mode):
            decoded_mode = self._set_bit(decoded_mode, bit_num, value)

        params['M'] = decoded_mode

        return protocol_base.IRCode(self.__class__.__name__, frequency, data, code, params)

    def _normalize_rlc(self, code):
        code = code_wrapper.CodeWrapper(code[:])

        if self._match(code.header_mark, HEADER_MARK):
            code.header_mark = HEADER_MARK
        else:
            raise ValueError('Invalid header mark')

        if self._match(code.header_space, HEADER_SPACE):
            code.header_space = HEADER_SPACE
        else:
            raise ValueError('Invalid header space')

        if code.footer_space >= LOGICAL_3_SPACE:
            raise ValueError('invalid closing space')

        for i in range(code.bits):
            pair = code.get_burst_pair(i)

            if self._match_pair(MARK, LOGICAL_3_SPACE, *pair):
                code.set_burst_pair(i, MARK, LOGICAL_3_SPACE)
            elif self._match_pair(MARK, LOGICAL_2_SPACE, *pair):
                code.set_burst_pair(i, MARK, LOGICAL_2_SPACE)
            elif self._match_pair(MARK, LOGICAL_1_SPACE, *pair):
                code.set_burst_pair(i, MARK, LOGICAL_1_SPACE)
            elif self._match_pair(MARK, LOGICAL_0_SPACE, *pair):
                code.set_burst_pair(i, MARK, LOGICAL_0_SPACE)
            elif self._match(pair[0], MARK) and pair[1] < LOGICAL_3_SPACE:
                code = code[:(i * 2) + 2]
                code.footer_mark = MARK
                break
            else:
                raise ValueError('Invalid burst pair')

        return code


RCMM = RCMM()

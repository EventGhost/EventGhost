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
from . import protocol_base
from . import DecodeError
from . import code_wrapper


TIMING = 444

#
# class Replay(protocol_base.ManchesterCoding1):
#     """
#     IR decoder for the Replay protocol.
#     """
#     _half_bit_time = TIMING
#
#     # {36k,444,msb}<-1,1|1,-1>(6,-2,1:1,6:3,<-2,2|2,-2>(T:1),D:8,S:8,F:8,-100m)*
#
#     header_mark = TIMING * 6
#     header_space = -TIMING * 2
#     footer_space = -100000
#
#     frequency = 36000
#
#     def _normalize_rlc(self, code):
#         code = code_wrapper.CodeWrapper(code[:])
#
#         if self._match(code.header_mark, self.header_mark):
#             code.header_mark = self.header_mark
#         else:
#             raise ValueError('invalid header mark')
#
#         if self._match(code.header_space, self.header_space):
#             code.header_space = self.header_space
#         elif self._match(code.header_space, self.header_space - TIMING):
#             code.header_space = self.header_space - TIMING
#         else:
#             raise ValueError('invalid header space')
#
#         for i, item in code[2:-1]:
#             for j in range(1, 4):
#                 if self._match(item, TIMING * j):
#                     code[i + 2] = TIMING * j
#                     break
#                 elif self._match(item, -TIMING * j):
#                     code[i + 2] = -TIMING * j
#                     break
#             else:
#                 raise ValueError('invalid half bit')
#
#         if self._match(code.footer_space, self.footer_space):
#             code.footer_space = self.footer_space
#         elif self._match(code.footer_space, self.footer_space + (-TIMING * 2)):
#             code.footer_space = self.footer_space + (-TIMING * 2)
#         else:
#             raise ValueError('invalid footer space')
#
#         return code
#
#     def decode(self, data, frequency):
#         if not self._match(frequency, self.frequency):
#             raise DecodeError('Invalid Frequency')
#
#         try:
#             code = self._normalize_rlc(data)
#         except ValueError:
#             raise DecodeError('Invalid code')
#
#         code_data = list(abs(item) for item in code)
#         self._set_data(code_data, 2)
#
#         # Get the start bit
#         if self._get_bit() != 1:
#             raise DecodeError("missing start bit")
#
#         mode = self._get_bits_lsb_last(3)
#
#         if mode != 6:
#             raise DecodeError('Invalid Mode')
#
#         self._get_trailer_bit()
#         toggle_bit = self._get_bits_lsb_last(1)
#
#         device = self._get_bits_lsb_last(8)
#         sub = self._get_bits_lsb_last(8)
#         function = self._get_bits_lsb_last(8)
#
#         params = {
#             'D': device,
#             'S': sub,
#             'F': function,
#             'T': toggle_bit
#         }
#         return protocol_base.IRCode(self.__class__.__name__, self.frequency, data, code, params)
#
#     def _get_trailer_bit(self):
#         sample = (
#             self._get_sample() * 8 +
#             self._get_sample() * 4 +
#             self._get_sample() * 2 +
#             self._get_sample()
#         )
#         if sample == 3:  # binary 0011
#             return 0
#         elif sample == 12:  # binary 1100
#             return 1
#         else:
#             raise DecodeError("wrong trailer bit transition")
#
#
# Replay = Replay()

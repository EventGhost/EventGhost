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

from collections import deque

from .config import Config


class IRException(Exception):
    pass


class DecodeError(IRException):
    pass


class RepeatTimeoutExpired(IRException):
    pass


class RepeatLeadIn(IRException):
    pass


class RepeatLeadOut(IRException):
    pass


from .ad_notham import AdNotham  # NOQA
from .aiwa import Aiwa  # NOQA
from .akai import Akai  # NOQA
from .akord import Akord  # NOQA
from .amino import Amino  # NOQA
from .amino56 import Amino56  # NOQA
from .anthem import Anthem  # NOQA
from .apple import Apple  # NOQA
from .archer import Archer  # NOQA
from .arctech import Arctech  # NOQA
from .arctech38 import Arctech38  # NOQA
from .audiovox import Audiovox  # NOQA
from .barco import Barco  # NOQA
from .blaupunkt import Blaupunkt  # NOQA
from .bose import Bose  # NOQA
from .bryston import Bryston  # NOQA
from .canalsat import CanalSat  # NOQA
from .canalsatld import CanalSatLD  # NOQA
from .denon import Denon  # NOQA
from .denon1 import Denon1  # NOQA
from .denon2 import Denon2  # NOQA
from .denon_k import DenonK  # NOQA
from .dgtec import Dgtec  # NOQA
from .digivision import Digivision  # NOQA
from .dishnetwork import DishNetwork  # NOQA
from .dishplayer import DishPlayer  # NOQA
from .dyson import Dyson  # NOQA
from .dyson2 import Dyson2  # NOQA
from .elan import Elan  # NOQA
from .elunevision import Elunevision  # NOQA
from .emerson import Emerson  # NOQA
from .entone import Entone  # NOQA
from .epson import Epson  # NOQA
from .f12 import F12  # NOQA
from .f120 import F120  # NOQA
from .f121 import F121  # NOQA
from .f32 import F32  # NOQA
from .fujitsu import Fujitsu  # NOQA
from .fujitsu128 import Fujitsu128  # NOQA
from .fujitsu56 import Fujitsu56  # NOQA
from .gi4dtv import GI4DTV  # NOQA
from .gicable import GICable  # NOQA
from .girg import GIRG  # NOQA
from .grundig16 import Grundig16  # NOQA
from .grundig1630 import Grundig1630  # NOQA
from .guangzhou import GuangZhou  # NOQA
from .gwts import GwtS  # NOQA
from .gxb import GXB  # NOQA
from .humax4phase import Humax4Phase  # NOQA
from .intervideorc201 import InterVideoRC201  # NOQA
from .iodatan import IODATAn  # NOQA
from .jerrold import Jerrold  # NOQA
from .jvc import JVC  # NOQA
from .jvc48 import JVC48  # NOQA
from .jvc56 import JVC56  # NOQA
from .kaseikyo import Kaseikyo  # NOQA
from .kaseikyo56 import Kaseikyo56  # NOQA
from .kathrein import Kathrein  # NOQA
from .konka import Konka  # NOQA
from .logitech import Logitech  # NOQA
from .lumagen import Lumagen  # NOQA
from .lutron import Lutron  # NOQA
from .matsui import Matsui  # NOQA
from .mce import MCE  # NOQA
from .mcir2kbd import MCIR2kbd  # NOQA
from .mcir2mouse import MCIR2mouse  # NOQA
from .metz19 import Metz19  # NOQA
from .mitsubishi import Mitsubishi  # NOQA
from .mitsubishik import MitsubishiK  # NOQA
from .motorola import Motorola  # NOQA
from .nec import NEC  # NOQA
from .nec48 import NEC48  # NOQA
from .necf16 import NECf16  # NOQA
from .necrnc import NECrnc  # NOQA
from .necx import NECx  # NOQA
from .necxf16 import NECxf16  # NOQA
from .nokia import Nokia  # NOQA
from .nokia12 import Nokia12  # NOQA
from .nokia32 import Nokia32  # NOQA
from .novapace import NovaPace  # NOQA
from .nrc16 import NRC16  # NOQA
from .nrc1632 import NRC1632  # NOQA
from .nrc17 import NRC17  # NOQA
from .ortek import Ortek  # NOQA
from .ortekmce import OrtekMCE  # NOQA
from .pacemss import PaceMSS  # NOQA
from .panasonic import Panasonic  # NOQA
from .panasonic2 import Panasonic2  # NOQA
from .panasonicold import PanasonicOld  # NOQA
from .pctv import PCTV  # NOQA
from .pid0001 import PID0001  # NOQA
from .pid0003 import PID0003  # NOQA
from .pid0004 import PID0004  # NOQA
from .pid0083 import pid0083  # NOQA
from .pioneer import Pioneer  # NOQA
from .proton import Proton  # NOQA
from .proton40 import Proton40  # NOQA
from .rc5 import RC5  # NOQA
from .rc57f import RC57F  # NOQA
from .rc57f57 import RC57F57  # NOQA
from .rc5x import RC5x  # NOQA
from .rc6 import RC6  # NOQA
from .rc6620 import RC6620  # NOQA
from .rc6624 import RC6624  # NOQA
from .rc6632 import RC6632  # NOQA
from .rc6m16 import RC6M16  # NOQA
from .rc6m28 import RC6M28  # NOQA
from .rc6m32 import RC6M32  # NOQA
from .rc6m56 import RC6M56  # NOQA
from .rca import RCA  # NOQA
from .rca38 import RCA38  # NOQA
from .rca38old import RCA38Old  # NOQA
from .rcaold import RCAOld  # NOQA
from .rcmm import RCMM  # NOQA
from .recs800045 import RECS800045  # NOQA
from .recs800068 import RECS800068  # NOQA
from .recs800090 import RECS800090  # NOQA
# replay
from .revox import Revox  # NOQA
from .roku import Roku  # NOQA
from .rs200 import Rs200  # NOQA
from .rti_relay import RTIRelay  # NOQA
from .sampo import Sampo  # NOQA
from .samsung20 import Samsung20  # NOQA
from .samsung36 import Samsung36  # NOQA
from .samsungsmtg import SamsungSMTG  # NOQA
from .scatl6 import ScAtl6  # NOQA
from .sejin138 import Sejin138  # NOQA
from .sejin156 import Sejin156  # NOQA
from .sharp import Sharp  # NOQA
from .sharp1 import Sharp1  # NOQA
from .sharp2 import Sharp2  # NOQA
from .sharpdvd import SharpDVD  # NOQA
from .sim2 import SIM2  # NOQA
from .sky import Sky  # NOQA
from .sky_hd import SkyHD  # NOQA
from .sky_plus import SkyPlus  # NOQA
from .somfy import Somfy  # NOQA
from .sony12 import Sony12  # NOQA
from .sony15 import Sony15  # NOQA
from .sony20 import Sony20  # NOQA
from .sony8 import Sony8  # NOQA
# sonydsp
from .streamzap import StreamZap  # NOQA
from .streamzap57 import StreamZap57  # NOQA
# sunfire
# tdc38
# tdc56
from .teack import TeacK  # NOQA
from .thomson import Thomson  # NOQA
from .thomson7 import Thomson7  # NOQA
from .tivo import Tivo  # NOQA
from .universal import Universal  # NOQA
# velleman
# viewstar
# whynter
# x10
# x10n
# x10_18
# x10_8
from .xbox_360 import XBox360  # NOQA
from .xbox_one import XBoxOne  # NOQA
# zaptor36
# zaptor56


DECODERS = [
    AdNotham,
    Aiwa,
    Akai,
    Akord,
    Amino,
    Amino56,
    Anthem,
    Apple,
    Archer,
    Arctech,
    Arctech38,
    Audiovox,
    Barco,
    Blaupunkt,
    Bose,
    Bryston,
    CanalSat,
    CanalSatLD,
    Denon,
    Denon1,
    Denon2,
    DenonK,
    Dgtec,
    Digivision,
    DishNetwork,
    DishPlayer,
    Dyson,
    Dyson2,
    Elan,
    Elunevision,
    Emerson,
    Entone,
    Epson,
    F12,
    F120,
    F121,
    F32,
    Fujitsu,
    Fujitsu128,
    Fujitsu56,
    GI4DTV,
    GICable,
    GIRG,
    Grundig16,
    Grundig1630,
    GuangZhou,
    GwtS,
    GXB,
    Humax4Phase,
    InterVideoRC201,
    IODATAn,
    Jerrold,
    JVC,
    JVC48,
    JVC56,
    Kaseikyo,
    Kaseikyo56,
    Kathrein,
    Konka,
    Logitech,
    Lumagen,
    Lutron,
    Matsui,
    MCE,
    MCIR2kbd,
    MCIR2mouse,
    Metz19,
    Mitsubishi,
    MitsubishiK,
    Motorola,
    NEC,
    NEC48,
    NECf16,
    NECrnc,
    Nokia,
    Nokia12,
    Nokia32,
    NovaPace,
    NRC16,
    NRC1632,
    NRC17,
    Ortek,
    OrtekMCE,
    PaceMSS,
    Panasonic,
    Panasonic2,
    PanasonicOld,
    PCTV,
    PID0001,
    PID0003,
    PID0004,
    pid0083,
    Pioneer,
    Proton,
    Proton40,
    RC5,
    RC57F,
    RC57F57,
    RC5x,
    RC6,
    RC6620,
    RC6624,
    RC6M16,
    RC6M28,
    RC6M32,
    RC6M56,
    RCA,
    RCA38,
    RCA38Old,
    RCAOld,
    # RCMM,
    RECS800045,
    RECS800068,
    RECS800090,
    Revox,
    Roku,
    Rs200,
    RTIRelay,
    Sampo,
    Samsung20,
    Samsung36,
    SamsungSMTG,
    ScAtl6,
    Sejin138,
    Sejin156,
    Sharp,
    Sharp1,
    Sharp2,
    SharpDVD,
    SIM2,
    Sky,
    SkyHD,
    SkyPlus,
    Somfy,
    Sony12,
    Sony15,
    Sony20,
    Sony8,
    StreamZap,
    StreamZap57,
    TeacK,
    Thomson,
    Thomson7,
    Tivo,
    XBox360,
    RC6632,
    XBoxOne,
    NECx,
    NECxf16,

]
#


class IrDecoder(object):
    def __init__(self):
        self.decoders = deque(DECODERS[:])
        self.universal_decoder = Universal

    def set_tolerance(self, name, tolerance):
        for decoder in self.decoders:
            if decoder.__class__.__name__ == name:
                decoder.tolerance = tolerance
                break

    def decode(self, data, frequency=0):
        if isinstance(data, tuple):
            data = list(data)

        if not isinstance(data, list):
            data = [int(ord(x)) for x in data]
        else:
            data = [int(x) for x in data]

        if len(data) < 3:
            return

        decoders = self.decoders

        for i, decoder in enumerate(decoders):
            try:
                code = decoder.decode(data, frequency)
            except DecodeError:
                print decoder.__class__.__name__
                continue

            if i != 0:
                decoders.remove(decoder)
                decoders.appendleft(decoder)
            break

        else:
            decoder = self.universal_decoder
            code = decoder.decode(data, frequency)

        return code

    @property
    def decoder_order(self):
        names = list(decoder.__class__.__name__ for decoder in self.decoders)
        return names

    @decoder_order.setter
    def decoder_order(self, value):
        decoders = list(decoder for decoder in self.decoders)
        self.decoders.clear()
        for name in value:
            for decoder in decoders[:]:
                if decoder.__class__.__name__ == name:
                    self.decoders.append(decoder)
                    decoders.remove(decoder)

        for decoder in decoders:
            self.decoders.append(decoder)


IrDecoder = IrDecoder()


from . import xbox_one

import time

for function in xbox_one.XBOX_ONE_COMMANDS.keys():
    rlc = XBoxOne.encode(function)[0]
    # code = XBox360.decode(rlc[:], XBox360.frequency)
    start = time.time()
    c = IrDecoder.decode(rlc, XBoxOne.frequency)

    stop = time.time()
    print c, (stop - start) * 1000

#
# import os
# import sys
#
# path = os.path.dirname(__file__)
#
# from . import protocol_base
#
# decoders = []
# output = []
# for f in os.listdir(path):
#     if f in ('__init__.py', 'code_wrapper.py', 'protocol_base.py', 'test_decoders') or not f.endswith('py'):
#         continue
#
#     mod_name = f.rsplit('.', 1)[0]
#
#     try:
#         __import__('decoders.' + mod_name)
#     except AttributeError:
#         print '# ' + mod_name
#         continue
#
#     mod = sys.modules['decoders.' + mod_name]
#
#     for key, value in mod.__dict__.items():
#         if key.startswith('_'):
#             continue
#
#         try:
#             if isinstance(value, protocol_base.IrProtocolBase):
#                 decoders += [value]
#                 print 'from .' + mod_name + ' import ' + key + '  # NOQA'
#                 output += [key]
#                 break
#         except TypeError:
#             continue
#     else:
#         print '#', mod_name
#
# print
# print
# for item in output:
#     print '   ', item + ','
#
# count = 0
#
# output = []
# import time
#
# start = time.time()
# for value in decoders:
#     try:
#         value._test_decode()
#         count += 1
#         output += [value.__class__.__name__]
#
#     except NotImplementedError:
#         continue
#
# stop = time.time()
#
# # 1037.99986839
# print (stop - start) * 1000
#
# for item in output:
#     print item
#
# print count

#
# print
# print
# for item in output:
#     print '[*]' + item


#
#
# def GetBitString(value, numdigits=8):
#     digits = []
#     for dummyCounter in range(numdigits):
#         if value & 1:
#             digits.append("1")
#         else:
#             digits.append("0")
#         value >>= 1
#     return "".join(reversed(digits))

#
# def GetDecoders():
#     decoders = []
#     for path in glob(os.path.join(DECODERS_DIR, "*.py")):
#         name = os.path.basename(path)
#         moduleName = os.path.splitext(name)[0]
#         if moduleName.startswith("_"):
#             continue
#         module = __import__(moduleName, globals())
#         decoders.append(getattr(module, moduleName))
#     return decoders
#
# DECODERS = GetDecoders()

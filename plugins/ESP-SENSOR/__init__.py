# -*- coding: utf-8 -*-
version = "0.0.1"

# plugins/ESP-SENSOR/__init__.py
#
# Copyright (C) 2018  Pako <lubos.ruckl@gmail.com>
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.1 by Pako 2018-06-24 07:06 GMT+1
#     - first public version
# ===========================================================================

eg.RegisterPlugin(
    name="ESP-SENSOR",
    author="Pako",
    version=version,
    kind="external",
    guid="{636C5CAF-9462-4D72-B4AA-E4BE4D2E4345}",
    createMacrosOnAdd=True,
    canMultiLoad=True,
    icon=(
        "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"
        "AAAASUVORK5CYII="
    ),
    description=ur'''<rst>
Plugin for ESP-SENSOR control.

ESP-SENSOR is a device that measures temperature and humidity and controls one relay.

Plugin allows you to set any number of significant levels.
If any of the levels are exceeded (and / or the value drops below), the corresponding event is triggered.
A change of relay state will trigger an event in EventGhost too.

The project assumes the use of ESP-12F_ board with FW "ESP-SENSOR".

.. image:: ESP-12F_1.png
.. image:: ESP-12F_2.png

Plugin uses libraries beebotte_, websocket-client_ and ObjectListView_.

Plugin version: %s

.. _ESP-12F:           https://en.wikipedia.org/wiki/ESP8266
.. _ObjectListView:    http://objectlistview.sourceforge.net/cs/index.html
.. _websocket-client:  https://pypi.python.org/pypi/websocket-client
.. _beebotte:          https://github.com/beebotte/bbt_python
''' % version,
    # url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=XXXX",
)

from time import time as ttime
from threading import Thread
from base64 import b64encode
from copy import deepcopy as cpy
from json import loads, dumps
from random import randrange
from winsound import PlaySound, SND_ASYNC
from eg.WinApi.Dynamic import CreateEvent, SetEvent
from os.path import split, abspath

mod_pth = abspath(split(__file__)[0])
from sys import path as syspath

syspath.append(mod_pth + "\\lib")
from websocket_0440SE import WebSocketApp
from beebotte_050SE import *
# from ObjectListView_12SE import ObjectListView, ColumnDefn
from ObjectListView import ObjectListView, ColumnDefn
from eg.WinApi.Dynamic import BringWindowToTop
from cStringIO import StringIO
from base64 import b64encode, b64decode
from PIL import Image
from wx.lib.statbmp import GenStaticBitmap
from wx.lib.buttons import GenButton

import paho.mqtt.client as mqtt

# from locale import setlocale, strcoll, LC_ALL
# import logging
# logging.basicConfig()
# setlocale(LC_ALL, "")

ACV = wx.ALIGN_CENTER_VERTICAL
DEFAULT_WAIT = 35.0
RELSTATES = ("OFF", "ON")
MQTT_HOST = "mqtt.beebotte.com"
MQTT_PORT = 1883
SLEEP_TIME = 60
WATCHDOG_TIME = 35.0
SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)

BULB_ON = (
    "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"
    "RU5ErkJggg=="
)

BULB_OFF = (
    "iVBORw0KGgoAAAANSUhEUgAAADsAAABgCAYAAACjbAqHAAAACXBIWXMAAAsTAAALEwEA"
    "mpwYAAAAB3RJTUUH4gUfCyYiTSn1sQAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3"
    "aXRoIEdJTVBkLmUHAAAgAElEQVR4nOW86ZNsx3Un9juZeZe6tfXer/st2InlgSDBFSSH"
    "lCiNhhyPJ2LEGciOiZDpLyOOx1I4/Bcg8F0R+jYOQg7bIzoUYcF2SJRoKcbSaEANl5EI"
    "EMADHkC8/XW/13t1Vd26Wy7n+EN1NRoLSaziB5+I21V9696q/OXvnJMnT568wP+PhD7s"
    "HxAR+uVf/mUN3Gm63US1Wofq8BA6y7pc9SzPNQ0DCA899JB/8sknBYB8WG35EMA+ob76"
    "1UF0aK/P1XVY83VzxrGcAssaNPoQigGJiYgFYglUQbAPLVsG6nYc6c1oTu3e0e0WTz/9"
    "dPggW/ZBgaXHH388urHrV8pJ/ggTfcza5q65fm9t7dTK3B3nzrTX11aS1ZWVpNfJoiRJ"
    "FClC01ieFGXY2z+wt25v25sbW/nW9u72YDi8DpGX4zh6YbXbv/yFLzyUP/nkk/y+G/l+"
    "7//617+evHB5/35v3ZdMHH2hnbUfuv++u7uPPvKAe+SjD7bPrK1l/V4nNcYoIlKkCASA"
    "iAIIAQIwM3wIGOcTv729W7108Sf59//2udGzP37p9qQoX4kj/YNev/2Dr37xE3vvB/R7"
    "Bvtbv/Vb0d8+f/0hhvq1pJX+o6yV3XvPPXe0v/T5T2ef/Pj5aGlxgbRWIBAEQkQkxz9I"
    "BCI4RVQDEBHEgTlmZjX9X2Q8mTTPP//y3nf+/X84+N73nzsE+JLW9N0zi/N//Vd/9ccD"
    "vAfbfi9g1Re/8uur42HzlaQV/3rWbj/c7XSyB+672/zDL38h/ci9d0ZaKQERFJEQkdVa"
    "NUopB2EIFIGEFCmvCE5ESASKhQ2zJN6H9vScgIXD9s7u8P/6kz+/+qff+cuR8xwpjeci"
    "lfzFw/fO/fDpp5+276bh+t1c/MQTT5ixyx4VUd/odrv/7eLC0j3z/TmzurzEv/blLyT3"
    "3HUugoADi0BQa037xqgDRRgDUgIoaXoUEKlE2IpIA6CGSAVw4QLD+xD7wOJ9oDRN07VT"
    "K3p7Z/fg8HBUBR/O+uA/sXtQth/8yIMbN29erj5wsF//+hPpM3/3d/84a3V+u9/v/+rC"
    "wkLW63ZDt9fxZ8+s4eMffTDVWouIsAgHRci1pj1FKAA0IvJzDrYiqCFc+8DsvY9DEITA"
    "iOIoKwrbaZxPlNbWe6edD+cnNpxau/Pe3b1bVw8+MLCPP/5vOq/d/MnXOp3u/7C4uPTw"
    "fL9PvW7Xdzod384y187Sg9Prq5kxmpSiA62wR8CYIEUQbjiwE5Game1PO0IIlpktICUE"
    "eWND1wcfMQt758Lt7X1nXUg67fZ8u9PpxXGcBQ731LVbXlm/c39/6/oOfo4d/1ywjz/+"
    "bzpXtzf+q16v/6+Xl5bu7PU63O12fKfT9q1WWntffW94sP3vT60sTVpZ+67AolwIsXWh"
    "ZZ1PbePbHNgCMnwnYI/eo27civPBcGDe2t1vbm3t1gTFUaQpiqIkSZJOK027IjhbFfXC"
    "8ul79v/73/rN288888xPBWx+NtD/sXVj9+qvz/Xn/9XCwsLZbqftO+2Oz7I0xEnM7O3z"
    "44Nbfw3m8sLFn8w7Vq+dXV8u0jTRDDYkqjSaKhFpnAtOKfVTf4v59RGlanzaNEGs8+5g"
    "MLS3tnZqpTRnWYuM0aK1Fq20aKUMoLqAfH40Hof/889/UInIizPP/46Z/eY3vxn95fd/"
    "+NW5/txvLy8t3NHtdkK32/HtLAutVhIU+NWqOPy+iWNJklhpEyW7e1sXivHgx8ao3SSO"
    "BsxCdeO6jXWJiExEuAgh2Lc7mNl6761zzo7yenF/MF7e2tmr9/YHtXVOlFJQSgmRglEK"
    "SmlRiqCUUlFkehCsc+Du//y//eFrt29eOnzHYJ944gn1f//pdx/t9vq/vbS49HC32+Fe"
    "p+PaWRbSNGVj9BASrrc63bVef/Gj7JsbTXG46ZpqMBgMqlvb25NRwefGE/vIpHJ3l7U/"
    "VTdWSXA3vXe5tbax1tbW2qppmqqqqklRFKODg4O9zc3NWxub2zuDw3HUWN8XBhEUaDqU"
    "QWklpPQUPE3PEwjamAyEuxpn6489+OkLly9faN6M6+3UmP7mRxfXWt3ef72wsPBop5Nx"
    "p9N2WdYKSZJyHEeste6qJPmMUkqzb17yzWRXKeWjKE3a/cW74lb3ASD+RD6pkryorCIV"
    "ODQviz18USnltdYgIvLeSwiBm6YJzrlgrWXvPdq95VbaWWwpUkRawEIAC0gBJICKIaCY"
    "BYDINCphYQDSCSH889uH+5eeeOKJbz/55JP+Z4L9nd/5nfjF17Z/ZX6h+yvdTke3s8xn"
    "rRnQmI1RUIqIoA0RgUhLFKUaCDK/cu5LSdr5AhGl0w6f2igLDybjwQVXj4Y/zWxCmMb8"
    "xhgAnJPwliKzIlCpJoYQgQUAE5QoxBEJBAxhsDCYGcxCLLLOzP/i23/xd68AeBUnPPQb"
    "1PiJJ55Q3//RlYd6c/1/tbCwcG+73eZ21vZpmro4jimKNET4FgETpaOOgDdsPXnO1uON"
    "Vm9xLessfoVIKmZ/hYO/BOGbIrLHrn7W18PXAEgURdBaHx+ilCJAZv+rOE67vbV/pKP4"
    "PlKqQwTQ9A8UQEQE4Oh/RaAjVRYQiQgAKEAWrHODh+771EtXr77o3pbZixf3srgVf7nX"
    "7T+cJIlVkJvOlzc7FDlFvCBCXVtNvm+SdMWYiOpy9NeT4dZLRCRKVPCu+r6rx68EWxyK"
    "qKCUiDFJxOys1lq0fr1vRUSl7YW7lU7W62r8crCTAQAk7eVHTJw8BFAXAggJRBiKACgl"
    "DECRgHgaZccxBEhEKRLvffAhEHO3W9XNr+0N9n8A4Eczdo9//YknnlAvXL7ywFxv4b+Z"
    "n587F7x9drC3+eexdj/54uc+heWF7vbt2xs/asrRZtaZu7upJv95Mty6qLXmKIrAocnF"
    "V5vCLieiQAQxxgggYcoGpsxNvSrS3spn4rT/X+ooud9otcve7iet3mqSzf0XRHpxaiJT"
    "50M0DeKFCJAp07PPFBGdPr2ariwtxuM89845MDMRkFnb7Dxw7+vsHjN7cTxOEtP6VK/f"
    "uzuOovGoGL0SGRl96Uv/4PTdd995h9Zaut22f/7Fl1lF8WJTDn+gteapjQFRFAkAb4yB"
    "Uuot49xJVnXcW0+S7mdJUSaCRqXtX9MmOkWkDGmzAsBDAJlSC4YChEHCBEVgEQgDWms6"
    "tbKSra8tp4qUbmzDdV03PrBw4HbZ6X5+eDD8KwCvAJBZC2h1YX290+n+xsL84n2k+PJk"
    "uPejRx99JPncY599qJ2128aYqN/vz03y8cb+weFtW012jVGeiBBFEZRSEkURZiwCgFJK"
    "jDE48r4gIqTZ3Om43f+iNtHdwv5VRcqTNsvaRKdJqzVSBFIkIBIChIiEQEJEopRiEDER"
    "WGvF66srrTPrK1mrleooMqrXbeuiqvw4n3hmIRHW4/zwyj/5ypcvPfvss2wA4PHHH1db"
    "g+a+dCm7K06Ms3W5Ecem+sSjH3twvt9fOop8ZGdn59r169f3mrp2SpHMwMyAnYyQTjIZ"
    "RWnK7CqKojjO+p9WOn4IJEN4XFaR/hRBOwAQaABHoRQLQFN2+UhPBAIlDA6KosioXq+t"
    "0jShKDIgRYgjoz9yzx3J9s5+7ayTLMt6Wat9/uLNw2cA7B2p8XJLxwcPtNvZfBRFLlgZ"
    "f/Thh7t3nrvzLmNMSykldV3vX758+VJZlvZIZRHH8bG6ztR3Bn4mSdKdi7L+Y64ZPc/O"
    "DUBkFfEmiGIXileVh1VR68sgyqaA1NSdaECYX59wH/0SsyJlGD54DIfjfGGul8SRNkoZ"
    "MDOdOb0W33F2TRdF4XxIdKfXuWvv9t4agH0DACN7MA/BnbGJjLP1FdfUt8+ff2C102kv"
    "aa00EfFgMLj26quv7h0x+AZGZ+9PngOAKO2tRGnnQWPic8zZJfGHWxTq5wTxvjbxnVHS"
    "XtRRa10rYwQyZZeFQDLFpjSEGVO9EjAIRFN7hQaGw7EfHI7j+X4nNUYrgSYC9F3nTqfX"
    "b9yqrHXSTjsLB2Zn7Zd+6ZcuGgBqNKrWFSipbX1rMip+lLXM8NyZ049EkWlprZX3frSx"
    "sXHjyC5l2sMsxhicdEgn1dgYgyRtr2tjlkmTT5JkSUJ8w8TxsjHJUmDZikyypI05C6gA"
    "TLVXCHSkv2AIQHrqqBgg8FSlZ+cI2DsYDNdPLXXn55L+1END1tZXk7VTy6ooS5+20hYp"
    "sxbrs4n6oz/6I3LOrtd1w4f7+68W5fjg3Nn11vz83JrWOtZaJ03TDK5du3YwY3XGZhzH"
    "cgLo8Wez874+vAh2L2qiXBFJu7PymTjtfk5Hyf1xkj4apa3PKK0Tpckrrb3SymulnVba"
    "kSanlXJKHb0aTF+JvFLkFZEnrX1d1eXhaDw0kUFkjDJGU7uV6lMrS1FktIsiE0WxWdK6"
    "ycx3vvOdKHheJkWcT8b7i722W1la7MRxkimlFBHpqqoOyrK0M2DGGBRFYZg5pGnKb2er"
    "R+dqgd+TUL+go+ScVvFHZDrcnYxZ3xC/Qk81mEQTIMdTPxENaAEgZJ0jY4wIM6AUDgbD"
    "Q+9Or6dpkmnWYrTB0tKcieOo8d4f1qXVnKBjbpVlEpgXEm2C1uSUNqHdbRsiQESciPii"
    "KA6IiE8wiJ2dnW5d1yunT5/bOX361ODtANd1rYyotD2/8BAptTYN4+Fwclp7IjFqXT3c"
    "29sdL87N7ZgoWSQd3amUUp6dksBU15XZ2trs9Lq9aml5tWIQBEBRlHlVN0WnnXWYmZQi"
    "zPd7ITF6q6rK3AcbiTc9o9DTgmFKWgWlEFQk3EpamogCMzfMzE3TlEqp43BPKSWnTp0a"
    "X7p0aW17+9bZg4PdxeXl5UG73a5CCMo5l3jm9UlerNZVhfse+Oh6t9eP0jTzxuiglK6U"
    "1g0R+hyEnHOqmIzNpZ+87G9tXjvs9XpVp9M7mF9aXUnibN2z18F7BREJzGFufrEgUqw1"
    "g0XAIqEoyuHqyuIq+ek0sNVKKIro5sHBfkFEWgJlpg/Wt4m0JhWUUkGJYgZCCKEBEI4Y"
    "PbbLoyBB5ufn7alTp64ppSLnXG9nZ2eVmY1SiuM4lbvuvf+hO+6aXyqLSRWYsb+7tTke"
    "H46jJF3QSreCc4iihOM0WQApENAYra7+8q98ZV+E1zxL1+goKGMmURRxFMW+qSsVAiNt"
    "pRYQ8FEgSszIJ8VYWAKmw7EorX2apeysbZipTcypGXtr1DRQYaMMK6XYNVUVQigAxFpr"
    "xHEczbyw1vrYbpeXl+v9/X05f/789aP5qTLGcJZ1u+25pXuVMnlZFjjc3/vPp08vvwB/"
    "h6YoOeuaxhLpeQCIkmQ9itLewd72wdqptWx+aeVjROhO7VRImMeQafxYV1Xc6/a81ool"
    "MEErEDOEFFvrJ957KwCIEEjg2mnLAACRKGGOFZnYC8GDiAkiURRJUdS1975g5sp7X6Vp"
    "2krTVM2Azrxuv993ALC3txdHUcStVsunaRqAMEEIrymRrSxLL06KwdW9rS2kaWST2Bwm"
    "kbnW6fb2251sK42jC01T7ZdVfnFhaTlSpFoKaEjIEWlPUJ4Ivi5L0Uq5NE0sEXmllCPA"
    "g6iydXXBu/oFERmB5UgjJaRpamjqJ6A0gtFR40lUA6A1dRMBw+GwKut61FFKiAhxHLfm"
    "5uaSvb298uRQAwBLS0vNcDhM1tfX65mDSpKsq5TSUFQaaHXX3Q+dz0cDE6dzExEZUiw5"
    "ka/YuT0vEo8Oh52sne4EXzVGR30XXG10ek5pcwbQYCbYuqYsa+csYU8p6gdIYG+HdVMf"
    "DPZuXz29tnAHEQ4A6TJLFFimy0pEAlFBSCozR4thgw6OwQYAg8FhNR4Od9M4Ns65Yjwe"
    "bzdNE94M9EiVbZ7n0XA4jBYXF0O3u3g2aXXu19r0ZrFev5fANU08KcvFuV6vxULXxdtd"
    "pcRfuXLFAPr6XXedq1xdVKz1jmgdx1H7tCLloIGinBgi+FYrHRfF8KVgHWttFhy7Kh8e"
    "7AIIURQZABaKDgmSMItunNOkiUHi4iQqDdFh0EYXHGTBQwjQqJwNGxsbG5PJZG9nZ2d/"
    "e3t7QkT85unbTK273a5rvKz2F9bm4ig+pYxuAxTULKWpgPmF+XA4GMSAdNK0dz6EsDUZ"
    "DQatTv/UHefunjdGORFhJoqJEQkhJsALgKoqdJZlTWRMlrX793pdDlWcnE5Eoqaxf+tG"
    "g2G32+0ys4dIEOGC2YfJpBgqIJCimhilueeee5pXbwz3WeRODtAhBKVY6JVXXtlVSoU4"
    "jmUGchYOzrIO3nskSSL3fOTB3vBwfA+LzJkoClBwYIAUXr8nSaCNpoPhwJg0u0MIp4Oo"
    "ycrqmk47mTk53gbnSx/sDVKqrJvqlFLa9XtzDYMRU7wcGb0oLMraZhBsVcZxTO12e56Z"
    "6xBCYJYmhFDlk8lEBBwZPUo72dAAYKNp2zlmZjEhBO2EyVqWNFXH4+qb2Zy9EpFptbrr"
    "Iqo3GY+p0+14BYDM0T2KjmOI5cXF8Nyrryx70kbEo5+00vP3f+QQLJ5PBhqRjqGjnq2b"
    "zdHhMO10ul0oeAUg8DQPJWDvfH07hNAsLCxkSZIsMHPNzMF76+q6LoaDw1IpsCY6XExD"
    "oZ588kkxLb3HLD54iTh4HUJQzNMkj1JKvPczNo9t1rnjPBaMJjU3368A9t65oJVyCvDT"
    "g/3sPROFOgQ9321PWmmrdgQCi8fxtfA4uj7W0XxR5O3B/s5r7XZrUxMcmLxWcKSUs85u"
    "5sPBLRGROI61tXZ0NPzU3odmeDgc7ezt1wACFA3m5+cbA0DWOov7l0dbQ+td2zmOghcd"
    "gldAHE4yq5QSZoZSClpPE9Vxq9U2kUkJyrVaCY0OD6m9fuqoJxRenwgpIDgNrUKv15no"
    "soqHk6KllHq916ZXHWu0a+zZxcWF16pmcqmVdoIms8DQ4upirxgfXA8hNEopbGxsjPM8"
    "/49nz5493ZubO6OUWtzZ3R9Vk8oHx9JKkp1vfvOb3gDA/PxncrPz7evO8aMu+MRaGzU+"
    "qISZjPeI4xgA4L3HLIKaNS5N2ylNc5p+bnHJ725tpY1znEQx42i2NhUBiESAEJvINsZB"
    "wDE0eQ1GOLZZgtJAVZaKlMLp03cuN2VRuLq6rVrdxFbloC6LXWZ2Ms2dklJK9vb2iq2t"
    "rcsh4Fa711vZ2LhlHAeworwTx7tEJAoAnnrqGz5L4kshBK6qkBW1TawNhlnRLCc3Y1dr"
    "Ld77Y/t1vqklcKkEzijliMgN9neV0sopDacxnZrpWRAg4jVpCyInIl4DDlDH12hM7xkO"
    "h5RlWR0ZZVrt7JwxSaus8muO3bjd7axnWbePN4m1TMN8El565ZXh9Y3btfWBCLJ35sz8"
    "aKY1ACBz671NIdltrMts49LaVbGzVnvvjxXxJKMz0FWeH9q63FJKWSi4lZWVgj17dt5r"
    "pRymauqUghPAiYgnBUeAFyEPwJFSVik4KDgo5SprQwjsFxYXS4FygKY0ay21WulSp90+"
    "pXXUCggWmBZgeA8wMzEzOee0q51hG7R1Lhhlbi8sLLiTYBGXZR7p6GLTuKiomnZRu2RS"
    "11HtvbKWacam9/4NDkprLUUx3qubal8BLo6NhSa3d7CrmL0H5OggpxQci3iAPZE4EHtA"
    "PM0+BzlA/P7ejo4iZTXgCOxB7Jk5GG1igUhTFVtlno9f59TDWiZrra69086xabxTCtgz"
    "8+bWrMLmGOzTTz8dltezl4Rwu26aTlXWWVXWibNWzzyzc+4tw5D3Ht57W+bD201Z7Ung"
    "cnFxcVzXNTOLB8FpgiMhDyYPcADgReCFEYjIE5Enmb76YIPzPpxaWS0Y4hXIEciD2IuI"
    "rYvq9uHh/rb3npmneccQAjEzVc7qpvBR7WxUOy+UJDc+e++9k1l73zDbbnl/mET65aZx"
    "v1pMbKfdaqq6rpskTb1pDLdaU6CzYMI5hyiKICJSVVXDzLfjOI50kujh4HBeQlBnz95R"
    "aa1MlKguFARCnpRyAtEi4pVWTglkNs7ube+1okhbaOVUAJgdCQBFSooyHw2H+4MQAnvv"
    "jwiY2mpprbY2mLKp47ryRph35022cbJu6g1L4U8//XS489T6S0T6Zt00nUlRtcfjKm3q"
    "2jAzeT8FetJ2Z717JMFaW1d5XiSJ2b527cphnh/ulmW+VRXlrbop91mCVQJHJE7Ajlk8"
    "E3swe9c0oWmasLqyNkFgz2APpR0z+6ooh6PRYM85F076D+aGvPeqaWpTVFVc2yYum4oh"
    "dO2hh9byk/jesu5/330rozSLfmytk2JSd4u6ysqqics3qfNJ0DP7PVJpAMDi4qIjIt7Y"
    "2EistVJVeV7k+diL2MDBhwAvIlMHRdoxsb+1tam1VtZEkQXgBMEFdh7gqq4nQ2utP6rI"
    "OdawJgQqrdVVZeOiqJOqsoaIbt19pn/jzdVwb1l5f+aZZ+Rr//Sro83d0bxz4Ywxyhuj"
    "XBIbn0RxUCpiY+g44z8LMk4mzGcTfQD47nNXHrx4Y3zmyq3DuVFRt+umXji7ujao6kpt"
    "D0bdfOj0C6/eXL3wk83Vm5vb3Y+ev2c7UsYDgYNjgYBtY12ej/MQgoiIUkpRXdeoa6/q"
    "sjb5ZJKMx2VrMilbRVU1kaEX/+gP/2D/zdjetszghz/8YXjg/CeaqmnugKClSTmTxC6K"
    "TEgiwyIKxkyjqdnKnMg0E3iyE3706v65SxujzymtfbAc7RyMl7YHwzPjURNtbA+WN7YH"
    "Z8ZDGxW1i0Z52d7azc+10tb++nJn7EQYDGa24hyHoqjqKEriTifLrLVc17VMaqvzoohH"
    "kyod5Xk7L8qYhS7fvd5/9dlnn31LRetPq5aRe053Ni5cqi5UVfMPJmnczYZlnSSRi+M4"
    "9A0YiI4vZmZhZkRR9Ib3SiGcPjX38pc/ddcL7STx49JFl27vrIRA87201b5zffHqA+dO"
    "H2RJ7POmNH/1vVcfZrD1XlwIlgDAhoAQrI1jRTqOUts0YTwe+6pyqq5rk5dlXOZFWlRN"
    "4hoZzrfjy0899ZR7O1A/tTToqaeecv/sN3/zhc2bozuKsjqVx3GZ5UldR7WLlQ5aN5Ik"
    "iczAGWPgnDtm1jmH06udgQ1iEq19mhqfpsafXr3vBlG0k7aTND7h6CaVxIvz3e31hfZB"
    "CNYffYdUZWmLonBERIa5KYrCOQdUzqmqKqMqr5O8tmldWBIjV4xpfmq1208vTALwsbvv"
    "PsxM9LytvRRl1R1Nyiwvi9jaRjchkPceJ2c/Wmtxzh2fOzXXK7JEV3uHVXqyq7UWEcA1"
    "TfBNE3xZ2rB7kJssMflCv5XXde2rqnLj8biaTCa1iISqqkKe59VkMuHKH7Gal3Fe1q2y"
    "qBLP4dbKncuXf1ZB9s+scHvmmWfka//sq6NbW4fzLoQzkdZOGe2iSHttkhDpqbM6Ylam"
    "RRxThzW1XxIw8bCs0/lW0hCxOOcgIiwhCMDC7LmqGtrZH6fz3SRvJbqx1oaytN7a2nvv"
    "wcwQEXLOTcfUySQ6HE3SUV5mo7xsF2Xl4m7y3J/9wf+y+7Pw/ExmAeD3fu/36n6r9ePA"
    "YZhXVbcsqqysytjaRjtXqtkQdJLR2fADAGvLWcHMtLl/2J6dt9aKtdYVReHKsvRXb+/H"
    "RVGGXlvnZVm6pmlcVeVhpjlHpQPSNEyVc6qoa1NUZTwp61ZdlREpXP2Nr/zSBn5O7eLP"
    "BQtAHnvsgc040heqqk7zouyO8jIbFZO4qpwKR+o8AzIDLCKvdwAR7x0UHe89ee+RV5Ue"
    "DgvVNA1PJg1v7QxTUlJXVRXqumZrrcw6cCZN01DDDVVVZcZlGY+LulVMyjR4Och6vVe/"
    "8Y1vvK1TOik/s3ZxJk8++aT/l//yv3vx2tbtc0VZnUompmxlSV1HsUuSNBABUfT6fHfm"
    "tGYSKwlXdkerNzZ21vKqXmjEzRGEs6i112slhyZOZL6/kp8EN5PXOxFoJrXO83FU5U1S"
    "F02rqi0ZUq999qFzB3/xDnC843rjr33tn9iNWwOqrbtHkyGtlI0T46I09fFRUHPkiY9t"
    "d+aZ//KHr31qbzC5n4MIG59SJAxFohXZxnI0HBan86LCPWcWdqfA3MxOj2wVKG2hi6qJ"
    "RpMqHY3LTl5M2i7426tzK8/923/7u28p3XtfYJ955hn54q//43y0O15klpU4iWystUuS"
    "yCsojmMzXUM5clDANLC4vnnYv7J58PD9dyz+4NOPnLl4YCfR6mJ3I2npUadjxl9+5L4L"
    "Ve2q7f3RneurcxtGTbMyM8fkvacQHFXW6lFRxvmozIpi0plMGmgVP////On/uvVOMbwT"
    "mz2Wb/3u75adVvKyD8HWdZPVtU2apjYhMJ3UwJM23HivYqMm996xuAMQB/amn5g8i03h"
    "fIiIAq+utAciIPi3OjhmLU3DZJtG+8pFdW2TqnaxCG2u9E/dwLvYGPGuwBKRnL/v1A0N"
    "3GjqJi1sk9aVi6xtNHMghzeuwB/ZrhCRY2bx3iFwQBxFVgE+IBzZtwiAwFqEmeXkd0zn"
    "qoGsZV3XVWwbl9Te+yRWV59++vfqd9P+dwUWAHq9XhN3Wq/VjkPTuLSubWyZdQhMeBt/"
    "qJQ6CptFputQJMxKFMCzNKIBmAT85vtnBDvnVdN4U9kQVbaOCLR1z9n+Jt7ldpd3DfbJ"
    "J5/ktS42wWGvblxaWZs0jTcO7qio5ajS++hQSonSCEorUVoLkYhSLEwkTHKCRQpaqzfc"
    "CwDMgTxEWWuNbXxcWwd42XjqqafeFavvCSwA/PjHP67Zuq26tpG1PrZNY7ybZirfOpgF"
    "KFBIpmXuQmSOi06IzNECGbFMazDfIkExee+Vs8HUzkauqqtqtLuH97CJ6T2BvXjxIhf1"
    "YNva2jW1jS0HA+9VUIGmjTcyO0gpUUqHk9kNwECp6EQua3qNUlpO3msMwEFR03jjnDVV"
    "WcRlNRlcv35x8l7AvqOg4m2ER7ubY21ak9o2LWedqb1XnaBo9oWvL5VEovRURYNoAU0d"
    "ULcv9ikAAAlSSURBVKREDJForcVEESsFRvT6fSFMO05xIO+9qp0zZVXpusiHe3t7Pzda"
    "ejt5T8wCkOFw2NiiLOuqiUMQDQ+lOJAxRk6yqJSIBgWl9LHqTjc2TIsvjTGilRYFHTTr"
    "t7DFzCSsKHhvmrKRYjQYY7qM/PcHNs9z3zTDwtnGWBuiMnjjnFNN07zpOw2UNmHqdBKZ"
    "bUNRKhZSr29JiTQFnbyxdNc5KOecsmxNUVRxVRU8HucV3lBQ9M7lvaoxALhinJfF3CQq"
    "6yqdJryaKEnSADhozTKd9gUiYgkhUAiBwK9n7wHA+2nNriiwdaIamnaWc6LKsjBFXcd1"
    "ZeOqqlt1XdTW5jXe4+7p9wPWV1VVNGWpy6Js58Wk0hrIy6KXJFqJ+CRY3x1O6lWx9tTF"
    "ixdOewkJV/WZW9fKj3phU7NEL770wl2eGWLt8uXXXkuzJDpUUVx6D+8DfFkUUVGU2XiS"
    "d6uiGFVV1fwiwIaqyou6LqUqioeKoc5cOV7RSp3SCn0CZURIfEDsgkQHhxUEonwQVagG"
    "PC33kUFZsoA4WKGDg7IeQCwEFQN5YOz5wLfLshk0RVFVVfETAO9qG+kHBZadc6MQmqiq"
    "8n9RlGbe+0hH082Hx5uOWAg+AM3R0qWDQE21GQECC6UZQPCAJYmBo306PN1h6XwIZVlY"
    "FvcffJP/yS8KrADIh/vbt2xj1Wg4NEvLy1hcXEBqkuMy+dhopCqC0dMbUq0RaY0oiqBN"
    "BH10HZRBEhtMF+MFZVHi+o0buLmxoYvJ2BB4bzKZbAFvF5R++GABwHnvq7o4FAWH9dV5"
    "rC72kLYyhMAIgaeAjMHwcIg8z6GURhQnSNNkNtFHq9XCvfeexfLKCrJWijiOMBoNUU4O"
    "cfHCPvLxofR7/UMA79k5fRBgAQQGNDg4RJqxvNDB8tISlJ6OQEnSQtM0+OGtq7h1/Qrq"
    "uoHzAcwCpRXSJMYnP/lJfPFzv4Hz588jTROwCG7evIlrl15GEinkwjgabd7XMyze6zg7"
    "E691vK+UuRaCl3E+Rp7nCMFDEcFojSSO0Gln6HQyKDC8a9DUBcpijHIyQlnk2Nm6hWtX"
    "L6NpamitYbRGp51hfX0dS0tLiKJo1tT39fSF98ssF0VxMD8/dxOgjzd1E43HOSaTAiFM"
    "E+fGRGi32zh//jyctdjc3IS1FkQKSZqg0+liZXkFZVFgMsnR7/cAACEw0jRFp9OGMRFE"
    "JGBK7y9MjeO5ud6DRPikUioSEYxGI9ze2kKWZUjTBNZaAITllRU89vnPY293B84FRHGE"
    "leVVnD13Disrq5hfmEeSJNjd2cXh8BAvv/wyvvef/ga3bt0SpWijrutLAN7xZv4PAyyY"
    "ASJWImo6XDBDICCabpAgpUCK4KzFwf4+trZ3MJkUSNMWHnzwPB7+6CNI0wSNbTAejVBV"
    "FfYP9nHlymW89tprGBwcAKQmRVGM8B7DxA8KrB2Pxy/PzfX+1nu/XtWVCd4jiRP0ez1k"
    "WYZur492u43DwQAvXXgRV6/dwDjPsbi4hI9//ONwzqLf76PT7cJai8mkgHMOnXYHrawF"
    "E0VUVdX9cRx/CsDfAMjxC4igAECladpnlkUiqLpusLu3jyRJEEJAv98DixwtaQIrq6tI"
    "khQmirGyuop+v49iUqDdbqOuCZOiQD4eY3A4gLUWSZIiSRJ47yvvfY7p5olfmM1GSWLu"
    "B/BJpZRqtVL0e130+330ul10O1102h1kWYaFhUUkaYqD/QNUdY3AjIPBACyMVpZNq+am"
    "22fAzEiSBM5ZHK0OXN7fH/wYQPF+Gvt+wXrn3I0oil4B8BlmJh8CnLMoyxJE0xV6Ywx2"
    "tnfw4osXcOXqVQwGh2ARPPbYY3jssccAAYRlev0RaG0MILO0bFjp9Xp37e/vp+8H8Psd"
    "Z0NZNjtE+gYze+8DRAQmipBlGdrtDGmaQhsz9dK3b6EoJogig6WlRbSzDAcHB6jrGuZo"
    "x7QPAXVdIXiPKIpgjKGmac4AuBfTAvD3PNa+bzXu9XoPAPwJZo68c5hMCoxHY3TbbURR"
    "hKwdoJTCuTvOQWmNYlIgSVOcOnUKH3/0E7j3vvvQ7XWhiKC1QZKkIFKo63qq7iFIu51d"
    "C0FexpTVX5jNkkgwzCqmo8a2WimyLEMUx5juZp/uZE7iBFmrhcFggO2dXUyKAp957HPo"
    "9/qo6xrFZIKiKDAaj3DlyhW88uor2NjYQF1VSFut8Wg03MX7mAR8EGCbPC9+NDfX+0si"
    "9ZvaqChNE3Q6bbRa6bFqMjNu3rqBZ3/0LDY2N5FPSqytreETn/gk7rn7HrQ7Uy1oZRnS"
    "Vguj0QjtdhvGaAhAdV0/0G63P11V1Q8ATH5uqz4ksAHABiB/0m63z/f7/U932h0VRebY"
    "6Rw9PwJJnGBlZQVzc/NIswzz8wsI3mN3dwcLfhFlVSHPxxgeHmJz8xacc+h1+6gWGl9V"
    "1aa19QHevG/v7xksAJTDYf7DNE3/J2NMHQJ/oa6tMaaCCwEsQGM9lFJYO3MGVVVjUpS4"
    "vbWNK9eu4/kXL6B1xGaejzGZFJgcqbT3fthqtf7fyWT8x7u7Bz8EMHo/Df2gHlinACzF"
    "cfyFdrv9rzudzpd7vW7UztpI0hTMDGvtcclACFOvrZTCbA/ubG5rrZ06p6q6XZblH4/H"
    "4//de/8KgDHeZ7j4rp709TNEAJQhhB1m3tVaL2mt79TGKGMMiOgY6AwsgGOwSZIcBxN1"
    "XUtRFFfzPP/D4XD4LWZ+GVM7fd/PY/ygwM6kDiHseu+34zheTNP0nNZaRVFEs6ccENEx"
    "k1EUIY5jxHF8VCTtZTKZvDIajf5gNBr9HwAuYZqd+EDkg7DZkyIADq213xsOh3LXnefC"
    "ww+f/9U0bUXGREeVtIq01pQkqbTbbUnTlI8A03PPPff8t7/97W8Nh8PvALiJ95Fcezv5"
    "oMECR4DLsvzexuZt+dznPkuPfvzj/3Bubj7q9fvo9frU7fbQ6/ep0+lCa62JSF544YUX"
    "v/vd7/67jY2NPwOwgffped9OPmg1PinNaDTa297Z3lpeWuqDVN9ax9baYK0NRTFxg4NB"
    "fevWrcmFCxde/P3f//1/961vfevPAGziQwAKfPgPhiUAvV6v95HTp0/fnyTJQpIkWauV"
    "xN6zP3r41WQ8Hl+/du3aRQA7+JCAzhrz9yERgPjoVR0dgulQ4jG1TYsP8Qm4APD/AbRn"
    "hnLxkLZkAAAAAElFTkSuQmCC"
)


# ===========================================================================

class Text:
    label1 = "Significant temperature levels:"
    header1 = (
        "Enabled",
        "Name/Event suffix",
        u"Temperature [\u00B0C]",
        "Up",
        "Down"
    )
    title1 = "Temperature level details"
    noLevel1 = "No temperature level is defined"

    label2 = "Significant humidity levels:"
    header2 = (
        "Enabled",
        "Name/Event suffix",
        u"Relative humidity [%]",
        "Up",
        "Down"
    )
    title2 = "Humidity level details"
    noLevel2 = "No humidity level is defined"

    buttons = (
        "Add new",
        "Duplicate",
        "Edit",
        "Delete"
    )

    cancel = "Cancel"
    ok = "OK"
    version = "version"
    debug = "Logging level:"
    debug2 = "(the higher the number, the more message writes ...)"
    prefix = "Event prefix/sensor name:"
    host = "Host address:"
    port = "TCP/IP port:"
    password = "Password:"
    channel = "Channel:"
    cmdrsrc = "Command resource:"
    msgrsrc = "Message resource:"
    apikey = "API key:"
    secretkey = "Secret key:"
    token = "Channel token:"
    cancel = "Cancel"
    ok = "OK"
    headers = (
        "Host:",
        "Port:",
        "Username:",
        "Password:",
    )
    proxyInfo = """If the proxy server does not require authentication, 
leave the Username and Password entries blank."""
    proxyTitle = "Proxy settings"
    reconnect = "Haven't seen a nop lately, reconnecting"
    connected = "Connected"
    disconnected = "Disconnected"
    wsOpenedEvt = "WebSocketOpened"
    wsClosedEvt = "WebSocketClosed"
    wsError = u"%s: WebSocket error: %s"
    wsMssg = "WebSocket message: %s"
    unknmsg = '%s: Unknown message: %s'
    mode = 'Connection method:'
    mode0 = 'Locale LAN (websocket)'
    mode1 = 'Beebotte (MQTT)'
    messBoxTit0 = "EventGhost - ESP-SENSOR"
    auto = "Auto close after %i s"
    conftitle = (
        "dummy",
        "Name conflict",
        "Conflict of values",
        "Conflict of values and names"
    )
    message1 = 'It is not possible to use the event name "%s",\n\
because the same name is already in the table.'
    message2 = 'It is not possible to use the value "%s",\n\
because the same value is already in the table.'
    tooltip = "Right mouse button click closes this window"
    addLstnr = 'Adding websocket listener'
    dashboard = '%s - dashboard'
    relState = "RelayState"
    relON = "Turn relay ON"
    relOFF = "Turn relay OFF"


# ===========================================================================

class StaticBitmap(GenStaticBitmap):
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        if self._bitmap:
            dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
            dc.Clear()
            dc.DrawBitmap(self._bitmap, 0, 0, True)
        # ===========================================================================


class FlatButton(GenButton):

    def __init__(
        self,
        parent=None,
        id=-1,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        idleBmp=None,
        activeBmp=None,
        label=None,
        radius=5,
        idleTextClr="#FFFFFF",
        activeTextClr="#FFFFFF",
        idleBackClr="#27ae60",
        activeBackClr="#2ecc71",
        font=None,
        bmpIndent=None,
        lblIndent=None
    ):
        GenButton.__init__(self, parent, id, "", pos, size, 0)
        self.font = font
        self.radius = radius
        self.idleTextClr = idleTextClr
        self.activeTextClr = activeTextClr
        self.idleBackClr = idleBackClr
        self.activeBackClr = activeBackClr
        self.idleBmp = idleBmp
        self.activeBmp = activeBmp if activeBmp else idleBmp
        self.label = label
        self.bmpIndent = bmpIndent
        self.lblIndent = lblIndent
        self.state = False
        self.mouse = False
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeave)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.onMouseUp)

    def setButton(self, idlbckclr, idltxtclr, ackbckclr, acktxtclr, txt):
        self.idleBackClr = idlbckclr
        self.idleTextClr = idltxtclr
        self.activeBackClr = ackbckclr
        self.activeTextClr = acktxtclr
        self.label = txt
        self.Refresh(False)

    def onPaint(self, evt):
        if self.state:
            backClr = self.activeBackClr
            textClr = self.activeTextClr
            bmp = self.activeBmp
        else:
            backClr = self.idleBackClr
            textClr = self.idleTextClr
            bmp = self.idleBmp
        width, height = self.GetSize()
        if bmp:
            if exists(bmp):
                try:
                    wxBmp = wx.Image(bmp, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                    bw, bh = wxBmp.GetWidth(), wxBmp.GetHeight()
                except:
                    wxBmp = None
            else:
                try:
                    pil = Image.open(StringIO(b64decode(bmp)))
                    hasAlpha = (pil.mode in ('RGBA', 'LA') \
                                or (pil.mode == 'P' and 'transparency' in pil.info))
                    image = wx.EmptyImage(*pil.size)
                    rgbPil = pil.convert('RGB')
                    if hasAlpha:
                        image.SetData(rgbPil.tostring())
                        image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
                    else:
                        new_image = rgbPil
                        data = new_image.tostring()
                        image.SetData(data)
                    wxBmp = image.ConvertToBitmap()
                    bw, bh = wxBmp.GetWidth(), wxBmp.GetHeight()
                except:
                    wxBmp = None
            if self.bmpIndent is None:
                tmpy = (bh + 2 * self.radius - height) / 2
                self.bmpIndent = self.radius - sqrt(self.radius ** 2 - tmpy ** 2) \
                    if (tmpy > 0 and self.radius > tmpy) else 0
                self.bmpIndent = max(5, self.bmpIndent)
                if not self.label:
                    self.bmpIndent = (width - bw) / 2
        else:
            wxBmp = None

        if self.label:
            if self.font is None:
                self.font = wx.Font(
                    12,
                    wx.FONTFAMILY_SWISS,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD,
                    False,
                    u'Arial'
                )
            self.SetFont(self.font)
            tw, th = self.GetTextExtent(self.label)
            if self.lblIndent is None:
                if wxBmp:
                    self.lblIndent = (width - tw - bw - self.bmpIndent) / 2
                else:
                    self.lblIndent = (width - tw) / 2
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()
        path = gc.CreatePath()
        path.AddRoundedRectangle(0, 0, width, height, self.radius)
        path.CloseSubpath()
        gc.SetBrush(wx.Brush(backClr))
        gc.FillPath(path)
        dc.SetTextForeground(textClr)
        if wxBmp:
            dc.DrawBitmap(wxBmp, self.bmpIndent, (height - bh) / 2)
        if self.label:
            dc.SetFont(self.font)
            lblPos = self.lblIndent if not wxBmp \
                else bw + self.bmpIndent + self.lblIndent
            dc.DrawText(self.label, lblPos, (height - th) / 2)

    def onMouseDown(self, evt):
        if self.mouse:
            self.state = False
        self.Refresh()
        evt.Skip()

    def onMouseUp(self, evt):
        if self.mouse:
            self.state = True
        self.Refresh()
        evt.Skip()

    def onEnter(self, evt):
        self.mouse = True
        self.state = True
        self.Refresh()
        evt.Skip()

    def onLeave(self, evt):
        self.mouse = False
        self.state = False
        self.Refresh()
        evt.Skip()


# ===========================================================================

class dashBoard(wx.Frame):
    delta = (0, 0)
    state = 0
    ctrlIds = (None, None)

    def __init__(
        self,
        plugin
    ):
        wx.Frame.__init__(
            self,
            None,  # parent
            -1,  # id
            style=wx.STAY_ON_TOP | wx.BORDER_SIMPLE,
            name="EspSensorDashBoard",
        )
        self.SetBackgroundColour(wx.Colour(238, 238, 238))
        self.SetForegroundColour(wx.Colour(128, 0, 0))
        self.plugin = plugin
        self.delta = (0, 0)

    def ShowDashBoard(self, data):

        text = self.plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.SetTitle(text.dashboard % data[0])
        infoSizer = wx.GridBagSizer(0, 16)
        self.Bind(wx.EVT_RIGHT_UP, self.OnCloseCommand)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.SetToolTip(text.tooltip)
        self.infoSizer = infoSizer

        def StaticText(txt, bold, coeff):
            st = wx.StaticText(self, -1, txt)
            font = st.GetFont()
            font.SetPointSize(coeff * font.GetPointSize())
            if bold:
                font.SetWeight(wx.FONTWEIGHT_BOLD)
            st.SetFont(font)
            st.Bind(wx.EVT_RIGHT_UP, self.OnCloseCommand)
            st.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            st.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            st.Bind(wx.EVT_MOTION, self.OnMouseMove)
            st.SetToolTip(text.tooltip)
            return st

        labels = (data[0], text.header1[2], text.header2[2])

        for i, label in enumerate(labels):
            params = ((2, True, 2), (1, False, 1.4), (1, False, 1.4))
            prms = params[i]
            infoSizer.Add(StaticText(label, prms[1], prms[2]), (i, 0), (1, prms[0]), flag=ACV)
            if i == 0:
                continue
            val = data[i]
            brdr = 15 if (val < "10.0" and val >= "0.0") else 5
            infoSizer.Add(StaticText(val, True, 2), (i, 1), flag=wx.RIGHT, border=brdr)
        sbuf = StringIO(b64decode(BULB_ON))
        wximg = wx.Image(sbuf)
        img = wx.Bitmap(wximg)
        self.ctrlIds = (wx.NewIdRef(), wx.NewIdRef())
        bmp = StaticBitmap(
            self,
            self.ctrlIds[0],
            img,
            size=(59, 96),
        )
        bmp.Bind(wx.EVT_RIGHT_UP, self.OnCloseCommand)
        bmp.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        bmp.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        bmp.Bind(wx.EVT_MOTION, self.OnMouseMove)
        bmp.SetToolTip(text.tooltip)
        infoSizer.Add(bmp, (0, 2), (4, 1), flag=wx.RIGHT | wx.TOP | wx.BOTTOM, border=5)

        btn = FlatButton(
            self,
            self.ctrlIds[1],
            size=(200, 28),
            radius=5,
            bmpIndent=5
        )
        self.SetState(self.plugin.state)

        def onBtn(event):
            if self.plugin.mode:
                data = self.plugin.SendMessage(
                    "setstate",
                    not self.state
                )
            else:
                data = self.plugin.SendCommand(
                    "setstate",
                    not self.state
                )
            event.Skip()

        btn.Bind(wx.EVT_BUTTON, onBtn)

        infoSizer.Add(btn, (3, 0), (1, 2), flag=wx.TOP | wx.EXPAND, border=5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        mainSizer.Add(infoSizer, 1, wx.EXPAND | wx.ALL, 5)
        size = mainSizer.Fit(self)
        sz = (size[0], size[1])
        self.SetMinSize(sz)
        self.SetSize(sz)
        if self.plugin.pos is None:
            self.Centre()
        else:
            self.SetPosition(self.plugin.pos)
        self.Show(True)
        BringWindowToTop(self.GetHandle())

    def onClose(self, evt):
        self.plugin.pos = self.GetPosition()
        self.plugin.dashboard = None
        self.Show(False)
        self.Destroy()

    def Update(self, tmprtr, hmdt):
        ctrls = []
        sizer = self.infoSizer
        children = sizer.GetChildren()
        for child in range(2, len(children), 2):
            ctrl = children[child].GetWindow()
            ctrls.append(ctrl)
        ctrls[0].SetLabel(tmprtr)
        ctrls[1].SetLabel(hmdt)

    def GetState(self):
        return self.state

    def SetState(self, state):
        txt = self.plugin.text
        params = (
            ("#27ae60", "#ffffff", "#2ecc71", "#ffffff", txt.relON),
            ("#bf263c", "#ffffff", "#d8334a", "#ffffff", txt.relOFF)
        )
        self.state = state
        sbuf = StringIO(b64decode((BULB_OFF, BULB_ON)[state]))
        wximg = wx.Image(sbuf)
        img = wx.Bitmap(wximg)
        bmp = wx.FindWindowById(self.ctrlIds[0])
        bmp.SetBitmap(img)
        btn = wx.FindWindowById(self.ctrlIds[1])
        btn.setButton(*params[state])

    def OnCloseCommand(self, evt):
        self.Close()

    def OnLeftDown(self, evt):
        self.CaptureMouse()
        x, y = self.ClientToScreen(evt.GetPosition())
        win = evt.GetEventObject()
        if isinstance(win, (
            wx._controls.StaticText,
            eg.CorePluginModule.__dict__['ESP-SENSOR'].StaticBitmap
        )):
            childX, childY = win.GetPosition()
            x += childX
            y += childY
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))

    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)
        evt.Skip()


# ===============================================================================

class MessageBox(wx.Dialog):

    def __init__(
        self, parent, message, caption='', flags=0, time=0, plugin=None
    ):
        PlaySound('SystemExclamation', SND_ASYNC)
        wx.Dialog.__init__(
            self, parent, style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP
        )
        self.SetTitle(plugin.text.messBoxTit0)
        self.SetIcon(plugin.info.icon.GetWxIcon())
        if flags:
            art = None
            if flags & wx.ICON_EXCLAMATION:
                art = wx.ART_WARNING
            elif flags & wx.ICON_ERROR:
                art = wx.ART_ERROR
            elif flags & wx.ICON_QUESTION:
                art = wx.ART_QUESTION
            elif flags & wx.ICON_INFORMATION:
                art = wx.ART_INFORMATION
            if art is not None:
                bmp = wx.ArtProvider.GetBitmap(art, wx.ART_MESSAGE_BOX, (32, 32))
                icon = wx.StaticBitmap(self, -1, bmp)
                icon2 = wx.StaticBitmap(self, -1, bmp)
            else:
                icon = (32, 32)
                icon2 = (32, 32)
        if caption:
            caption = wx.StaticText(self, -1, caption)
            caption.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        message = wx.StaticText(self, -1, message)
        line = wx.StaticLine(self, -1, size=(1, -1), style=wx.LI_HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add((10, 1))

        if time:
            self.cnt = time
            txt = plugin.text.auto % self.cnt
            info = wx.StaticText(self, -1, txt)
            info.Enable(False)
            bottomSizer.Add(info, 0, wx.TOP, 3)

            def UpdateInfoLabel(evt):
                self.cnt -= 1
                txt = plugin.text.auto % self.cnt
                info.SetLabel(txt)
                if not self.cnt:
                    self.Close()

            self.Bind(wx.EVT_TIMER, UpdateInfoLabel)
            self.timer = wx.Timer(self)
            self.timer.Start(1000)
        else:
            self.timer = None

        button = wx.Button(self, -1, plugin.text.ok)
        button.SetDefault()
        bottomSizer.Add((1, 1), 1, wx.EXPAND)
        bottomSizer.Add(button, 0, wx.RIGHT, 10)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(icon, 0, wx.LEFT | wx.RIGHT, 10)
        topSizer.Add((1, 1), 1, wx.EXPAND)
        topSizer.Add(caption, 0, wx.TOP, 5)
        topSizer.Add((1, 1), 1, wx.EXPAND)
        topSizer.Add(icon2, 0, wx.LEFT | wx.RIGHT, 10)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        mainSizer.Add(message, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        mainSizer.Add(line, 0, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND | wx.BOTTOM, 5)

        def OnButton(evt):
            self.Close()
            evt.Skip()

        button.Bind(wx.EVT_BUTTON, OnButton)

        def onClose(evt):
            if self.timer:
                self.timer.Stop()
                del self.timer
            self.MakeModal(False)
            self.GetParent().Raise()
            self.Destroy()

        self.Bind(wx.EVT_CLOSE, onClose)
        self.SetSizer(mainSizer)
        self.Fit()
        self.MakeModal(True)
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler


# ===============================================================================

class extDialog(wx.Frame):
    def __init__(
        self,
        parent,
        plugin,
        coldefs,
        grid,
        ix,
        rowdata=None,

    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.RESIZE_BORDER,
            name="EspSensorExtDialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.coldefs = coldefs
        self.rowdata = rowdata
        self.grid = grid
        self.ix = ix

    def ShowExtDialog(self, title):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)
        text = self.plugin.text
        panel = wx.Panel(self)

        def wxst(label):
            return wx.StaticText(panel, -1, label)

        labels = [it[0] for it in self.coldefs]
        rowdata = self.rowdata if self.rowdata is not None else self.grid.GetRow(self.ix)
        dgrows = len(labels)
        sizer = wx.FlexGridSizer(dgrows, 2, 5, 5)
        sizer.AddGrowableCol(1)
        for dgrow in range(0, dgrows):
            kind = self.coldefs[dgrow][2]
            sizer.Add(wxst(labels[dgrow]), 0, ACV)
            if kind == 1:
                ctrl = wx.TextCtrl(panel, -1, rowdata[dgrow])
            elif kind == 2:
                ctrl = eg.SpinIntCtrl(
                    panel,
                    -1,
                    rowdata[dgrow],
                    min=self.coldefs[dgrow][4][0],
                    max=self.coldefs[dgrow][4][0],
                )

            elif kind == 3:
                params = self.coldefs[dgrow][4]
                ctrl = eg.SpinNumCtrl(
                    panel,
                    -1,
                    rowdata[dgrow],
                    integerWidth=params[0],
                    fractionWidth=params[1],
                    allowNegative=params[2],
                    min=params[3],
                    max=params[4],
                    increment=params[5],
                )
            else:
                ctrl = wx.CheckBox(panel, -1, " ")
                ctrl.SetValue(rowdata[dgrow])
            sizer.Add(ctrl, 0, wx.EXPAND)

        line = wx.StaticLine(
            panel,
            -1,
            style=wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        mainSizer.Add(btnsizer, 0, wx.EXPAND | wx.RIGHT, 10)
        mainSizer.Add((1, 6))
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()

        self.Bind(wx.EVT_CLOSE, onClose)

        def onOk(evt):
            oldLevels = self.grid.GetData()
            data = []
            children = sizer.GetChildren()
            for child in range(1, len(children), 2):
                ctrl = children[child].GetWindow()
                data.append(ctrl.GetValue())
            flag = 0
            valuConfl = False
            for i, item in enumerate(oldLevels):
                if i == self.ix:
                    continue
                if item[1] == data[1]:
                    flag += 1
                    break
            for i, item in enumerate(oldLevels):
                if i == self.ix:
                    continue
                if item[2] == data[2]:
                    flag += 2
                    break
            if flag:
                mssg = ""
                mssg += self.plugin.text.message1 % data[1] if flag & 1 else ""
                mssg += "\n" if flag == 3 else ""
                mssg += self.plugin.text.message2 % data[2] if flag & 2 else ""
                MessageBox(
                    panel,
                    mssg,
                    self.plugin.text.conftitle[flag],
                    wx.ICON_EXCLAMATION,
                    plugin=self.plugin,
                    time=20
                )
            else:
                if self.ix == -1:
                    self.grid.AppendRow(data)
                else:
                    self.grid.SetRow(data)
                self.grid.RefreshTable()
                self.Close()

        btn1.Bind(wx.EVT_BUTTON, onOk)

        def onCancel(evt):
            self.Close()

        btn2.Bind(wx.EVT_BUTTON, onCancel)

        mainSizer.Layout()
        w, h = self.GetSize()
        self.SetSize((max(w, 400), h))
        self.SetMinSize((max(w, 400), h))
        self.Raise()
        self.MakeModal(True)
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler


# ===========================================================================

class Level(object):
    attrs = ('enab', 'name', 'val', 'up', 'down')
    nonum = (True, True, False, True, True)

    def __init__(self, enab=True, name="", val=0.0, up=False, down=False):
        args = locals()
        for i, item in enumerate(self.attrs):
            setattr(self, item, args[item] if self.nonum[i] else str(args[item]))

    def update(self, data):
        for i, item in enumerate(self.attrs):
            setattr(self, item, data[i] if self.nonum[i] else str(data[i]))
        # ===========================================================================


class ObjectListCtrl(ObjectListView):

    def __init__(self, parent, coldefs, rows, objmodel):
        ObjectListView.__init__(
            self,
            parent,
            -1,
            style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL
        )
        self.coldefs = coldefs
        self.rows = rows
        self.objmodel = objmodel
        self.selRow = -1
        self.wk = SYS_VSCROLL_X + self.GetWindowBorderSize()[0]
        self.wkc = SYS_VSCROLL_X + self.GetWindowBorderSize()[0]
        self.colwidths = [0]
        hc = 1 + len(coldefs)

        self.SetTable()

        for i, cd in enumerate(self.coldefs):
            self.SetColumnWidth(i + 1, wx.LIST_AUTOSIZE_USEHEADER)
            w = self.GetColumnWidth(i + 1)
            self.colwidths.append(w)
            self.wk += w
            if cd[3]:
                self.wkc += w
                self.columns[i + 1].SetFixedWidth(w)
        self.AddObject(objmodel())
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        hh = rect[1]  # header height
        hi = rect[3]  # item height
        self.DeleteAllItems()
        self.SetMinSize((self.wk, 5 + hh + rows * hi))
        self.SetSize((self.wk, 5 + hh + rows * hi))
        self.Layout()
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

    def OnItemSelected(self, evt):
        self.SelRow(evt.GetIndex())
        evt.Skip()

    def OnSize(self, event):
        wx.CallAfter(self.SetWidth)
        event.Skip()

    # Important !!!
    # Otherwise, the indexes do not match after sorting by one of the columns
    def OnColClick(self, evt):
        wx.CallAfter(self.RefreshTable)
        evt.Skip()

    def SetTable(self):
        getters = self.objmodel.attrs
        self.AddColumnDefn(ColumnDefn(fixedWidth=0))
        for i, it in enumerate(self.coldefs):
            if it[2]:
                cldf = ColumnDefn(it[0], it[1], valueGetter=getters[i])
            else:
                cldf = ColumnDefn(it[0], it[1], checkStateGetter=getters[i])
            self.AddColumnDefn(cldf)
        self.RepopulateList()

    def SetWidth(self):
        newW = self.GetSize().width
        p = (newW - self.wkc) / float(self.wk - self.wkc)
        col = self.GetColumnCount()
        w = SYS_VSCROLL_X + self.GetWindowBorderSize()[0]
        for c in range(1, col - 1):
            if not self.coldefs[c - 1][3]:
                self.SetColumnWidth(c, p * self.colwidths[c])
            w += self.GetColumnWidth(c)
        self.SetColumnWidth(col - 1, newW - w)

    def SelRow(self, row):
        self.selRow = row
        obj = self.GetObjects()[row]
        self.SelectObject(obj, deselectOthers=True, ensureVisible=True)
        self.SetFocus()

    def DeleteRow(self, row=None):
        row = self.selRow if row is None else row
        if row > -1:
            obj = self.GetObjects()[row]
            self.RemoveObject(obj)
            self.RefreshTable()
            row = row if row < self.GetItemCount() else self.GetItemCount() - 1
            if row > -1:
                self.SelRow(row)
            else:
                self.selRow = -1
                evt = eg.ValueChangedEvent(self.GetId(), value="Empty")
                wx.PostEvent(self, evt)

    def AppendRow(self, data):
        self.AddObject(self.objmodel(*data))
        ix = self.GetItemCount()
        if ix == 1:
            evt = eg.ValueChangedEvent(self.GetId(), value="One")
            wx.PostEvent(self, evt)

    def SetRow(self, rowData, row=None):
        row = self.selRow if row is None else row
        obj = self.GetObjects()[row]
        obj.update(rowData)
        self.RefreshTable()

    def RefreshTable(self):
        self.RepopulateList()
        self.SetWidth()

    def GetSelectedItemIx(self):
        return self.selRow

    def GetRow(self, row=None):
        row = self.selRow if row is None else row
        rowData = []
        for i in range(1, self.GetColumnCount()):
            kind = self.coldefs[i - 1][2]
            if kind > 0:
                data = self.GetItem(row, i).GetText() if row > -1 else ""
                if kind == 2:
                    data = 0 if data == "" else int(data)
                elif kind == 3:
                    data = 0.0 if data == "" else float(data)
            else:
                if row > -1:
                    col = self.columns[i]
                    obj = self.GetObjects()[row]
                    data = col.GetCheckState(obj)
                else:
                    data = False
            rowData.append(data)
        return rowData

    def GetData(self):
        data = []
        for row in range(self.GetItemCount()):
            rowData = self.GetRow(row)
            data.append(rowData)
        return data

    def SetData(self, data):
        if data:
            for row in data:
                self.AppendRow(row)
            self.SelRow(0)
            self.EnsureVisible(0)


# ===========================================================================

class WebSocketClient(WebSocketApp):
    def __init__(self, url, plugin):
        WebSocketApp.__init__(
            self,
            url,
            on_open=plugin.on_open,
            on_message=plugin.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.plugin = plugin

    def on_error(self, _, error):
        eg.PrintError(self.plugin.text.wsError % (self.plugin.info.eventPrefix, error))
        self.plugin.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(5.0, self.plugin.watcher)

    def on_close(self, _):
        if self.plugin.connFlag:
            self.plugin.TriggerEvent(self.plugin.text.wsClosedEvt)
            self.plugin.connFlag = False

    def start(self):
        auth = None
        if self.plugin.proxy[0] != "":
            host = str(self.plugin.proxy[0])
            port = self.plugin.proxy[1]
            if self.plugin.proxy[2] != "":
                auth = (
                    str(self.plugin.proxy[2]),
                    str(self.plugin.proxy[3].Get())
                )
        else:
            host = None
            port = None
        self.run_forever(
            http_proxy_host=host,
            http_proxy_port=port,
            http_proxy_auth=auth
        )
    # ===========================================================================


class ESP_SENSOR(eg.PluginClass):
    client = None
    wsC = None
    text = Text
    prefix = None
    connFlag = False
    msgWait = 0
    lastMessage = 0
    watchdog = None
    debug = 5
    proxy = ("",)
    queryData = {}
    tmprtr = "0.0"
    hmdt = "0.0"
    state = 0
    lastTevent = None
    lastHevent = None
    dashboard = None
    pos = None

    def __init__(self):
        self.AddActionsFromList(ACTIONS)

    def GetToken(self):
        flag = True
        while flag:
            token = format(randrange(16777216), '06x')
            flag = token in self.queryData
        event = CreateEvent(None, 0, 0, None)
        self.queryData[token] = event
        return token

    def SendCommand(self, cmd, value):
        token = self.GetToken()
        evt = self.queryData[token]
        msg = {"command": cmd, "token": token}
        if value is not None:
            msg["state"] = value
        msg = dumps(msg)
        try:
            self.wsC.send(msg)
            eg.actionThread.WaitOnEvent(evt)
            data = self.queryData[token]
            del self.queryData[token]
        except:
            del self.queryData[token]
            data = {}
        return data

    def normalizeURL(self, url, port):
        if not url.startswith("ws://"):
            if url.startswith("http://"):
                url = url.replace("http://", "ws://")
            else:
                url = "ws://" + url
        if not url.endswith("/ws") and not url.endswith("/ws/"):
            if url.endswith("/"):
                url += "ws"
            else:
                url += "/ws"
        elif url.endswith("/ws/"):
            url = url[:-1]
        return url.replace("/ws", ":%i/ws" % port)

    def SendMessage(self, cmd, message):
        token = self.GetToken()
        evt = self.queryData[token]
        msg = {"command": cmd, "token": token}
        if message is not None:
            msg["value"] = message
        try:
            self.resource.publish(msg)
            eg.actionThread.WaitOnEvent(evt)
            data = self.queryData[token]
            del self.queryData[token]
            return data
        except:
            del self.queryData[token]
            eg.PrintTraceback()
            return {}

    def stopClient(self):
        if self.client is not None:
            try:
                self.client.unsubscribe(str("%s/%s" % (self.channel, self.msgrsrc)))
            except:
                pass
            try:
                self.client.disconnect()
            except:
                pass
        self.client = None
        del self.client
        self.connFlag = False

    def startClient(self):
        self.stopClient()

        # Will be called upon reception of CONNACK response from the server.
        def on_connect(client, data, rc):
            client.subscribe(str("%s/%s" % (self.channel, self.msgrsrc)), 1)
            if self.connFlag:
                self.TriggerEvent(self.text.disconnected)
                self.connFlag = False
            self.resource.publish({'command': 'getinitstate'})

        def on_message(client, data, msg):
            pld = loads(msg.payload)
            if isinstance(pld, dict) and "data" in pld:
                if isinstance(pld["data"], dict) and 'message' in pld["data"]:
                    m = pld["data"]
                    mssg = m['message']
                    self.Log('message: %s' % m['message'], 5)
                    self.lastMessage = ttime()
                    if 'state' in m:
                        self.state = m['state']
                    if self.dashboard is not None:
                        self.dashboard.SetState(self.state)
                    if "token" in m:
                        token = m['token']
                        event = self.queryData[token]
                        del m["token"]
                        self.queryData[token] = m
                        SetEvent(event)
                        # return
                    if mssg in ('nop', 'state', 'initstate'):
                        tmprtr = str(m['temperature'])
                        hmdt = str(m['humidity'])
                        self.checkLevels(tmprtr, hmdt)
                        if self.dashboard:
                            self.dashboard.Update(tmprtr, hmdt)
                        if mssg == 'initstate':
                            self.connFlag = True
                            self.TriggerEvent(
                                self.text.connected,
                                payload=self.state
                            )
                    elif mssg == "change":
                        if m['change']:
                            self.TriggerEvent(
                                "%s.%s" % (self.text.relState, RELSTATES[self.state]),
                                payload=self.state
                            )
                    elif mssg == 'button':
                        self.TriggerEvent("Button")
                    elif mssg == 'connected':
                        if self.connFlag:
                            self.TriggerEvent(self.text.disconnected)
                        self.connFlag = False
                        self.resource.publish({'command': 'getinitstate'})
                    else:
                        eg.PrintNotice(self.text.unknmsg % (self.info.eventPrefix, repr(m)))
                else:
                    eg.PrintNotice(self.text.unknmsg % (self.info.eventPrefix, repr(pld["data"])))
            else:
                eg.PrintNotice(self.text.unknmsg % (self.info.eventPrefix, repr(pld)))

        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.username_pw_set("token:%s" % self.TOKEN)
        try:
            self.client.connect(MQTT_HOST, MQTT_PORT, SLEEP_TIME)
        except  Exception, exc:
            eg.PrintError("%s: %s" % (self.info.eventPrefix, exc.args[1]))
        self.client.loop_start()

    def __start__(
        self,
        prefix=None,
        debug=3,
        mode=0,
        host="ws://",
        port=80,
        password="",
        channel="",
        cmdrsrc="",
        msgrsrc="",
        bbt_tkn="",
        bbt_api="",
        bbt_secret="",
        dummy="",
        proxy=["", 0, "", ""],
        tempLevels=[],
        humiLevels=[],
    ):
        prefix = self.name if prefix is None else prefix
        self.info.eventPrefix = prefix
        self.prefix = prefix
        self.debug = debug
        self.proxy = proxy
        self.connFlag = False
        self.msgWait = DEFAULT_WAIT
        self.lastMessage = ttime()
        self.queryData = {}
        self.debug = debug
        self.mode = mode
        self.tempLevels = tempLevels
        self.humiLevels = humiLevels
        self.pos = None
        if mode:
            self.channel = channel
            self.msgrsrc = msgrsrc
            if not isinstance(bbt_tkn, eg.Password):
                tkn = eg.Password(None)
                tkn.Set(bbt_tkn)
            else:
                tkn = bbt_tkn
            self.TOKEN = tkn.Get()

            if not isinstance(bbt_api, eg.Password):
                api = eg.Password(None)
                api.Set(bbt_api)
            else:
                api = bbt_api
            API_KEY = api.Get()

            if not isinstance(bbt_secret, eg.Password):
                secret = eg.Password(None)
                secret.Set(bbt_secret)
            else:
                secret = bbt_secret
            SECRET_KEY = secret.Get()
            bbt = BBT(API_KEY, SECRET_KEY)
            self.resource = Resource(bbt, self.channel, cmdrsrc)
            self.stopWatchdog()
            self.watchdog = eg.scheduler.AddTask(WATCHDOG_TIME, self.watcher)
            self.startClient()
        else:
            _ = eg.scheduler.AddTask(1.0, self.establishSubscriber)
            self.url = self.normalizeURL(host, port)
            self.port = port
            if not isinstance(password, eg.Password):
                passw = eg.Password(None)
                passw.Set(password)
            else:
                passw = password
            self.password = b64encode(passw.Get())

    def stopWatchdog(self):
        if self.watchdog:
            try:
                eg.scheduler.CancelTask(self.watchdog)
            except:
                pass
        self.watchdog = None

    def OnComputerResume(self, dummy):
        self.watchdog = eg.scheduler.AddTask(15.0, self.watcher)

    def OnComputerSuspend(self, dummy):
        self.stopWatchdog()
        self.stopClient()
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.ct = None
        if self.dashboard:
            try:
                self.dashboard.Close()
            except:
                pass

    def __stop__(self):
        self.stopWatchdog()
        self.stopClient()
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.ct = None
        if self.dashboard:
            try:
                self.dashboard.Close()
            except:
                pass

    def Log(self, message, level):
        if self.debug >= level:
            print "%s: %s" % (self.info.eventPrefix, message)

    def watcher(self):
        if not self.info.isStarted:
            return
        if (ttime() - self.lastMessage) > self.msgWait:
            if self.connFlag:
                self.TriggerEvent(self.text.disconnected)
            self.Log(self.text.reconnect, 2)
            self.lastMessage = ttime()
            if self.mode:  # MQTT
                self.startClient()
            else:
                self.refreshWebSocket()
        self.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(5.0, self.watcher)

    def on_open(self, _):
        self.connFlag = True
        self.TriggerEvent(self.text.wsOpenedEvt)

    def establishSubscriber(self):
        if self.wsC:
            return
        self.wsC = WebSocketClient(self.url, self)
        self.ct = Thread(target=self.wsC.start)
        self.ct.start()
        self.lastMessage = ttime()
        self.stopWatchdog()
        self.watchdog = eg.scheduler.AddTask(0.01, self.watcher)
        self.Log(self.text.addLstnr, 4)

    def refreshWebSocket(self):
        self.msgWait = DEFAULT_WAIT
        if self.wsC:
            self.wsC.close()
        self.wsC = None
        self.establishSubscriber()
        self.connFlag = False

    def checkLevels(self, tmprtr, hmdt):
        if self.tmprtr != "0.0" or self.hmdt != "0.0":
            for item in self.tempLevels:
                val = str(item[2])
                if item[0] and item[3] and self.tmprtr <= val and tmprtr > val:
                    if self.lastTevent != (val, 1):
                        self.TriggerEvent("TemperatureUp.%s" % item[1], payload=(val, tmprtr))
                        self.lastTevent = (val, 1)
                elif item[0] and item[4] and self.tmprtr >= val and tmprtr < val:
                    if self.lastTevent != (val, 0):
                        self.TriggerEvent("TemperatureDown.%s" % item[1], payload=(val, tmprtr))
                        self.lastTevent = (val, 0)
            for item in self.humiLevels:
                val = str(item[2])
                if item[0] and item[3] and self.hmdt <= val and hmdt > val:
                    if self.lastHevent != (val, 1):
                        self.TriggerEvent("HumidityUp.%s" % item[1], payload=(val, hmdt))
                        self.lastHevent = (val, 1)
                elif item[0] and item[4] and self.hmdt >= val and hmdt < val:
                    if self.lastHevent != (val, 0):
                        self.TriggerEvent("HumidityDown.%s" % item[1], payload=(val, hmdt))
                        self.lastHevent = (val, 0)
        self.tmprtr = tmprtr
        self.hmdt = hmdt

    def OpenDashboard(self):
        if self.dashboard is None:
            self.dashboard = dashBoard(self)
            wx.CallAfter(
                self.dashboard.ShowDashBoard,
                (self.prefix, self.tmprtr, self.hmdt),
            )
        else:
            BringWindowToTop(self.dashboard.GetHandle())

    def CloseDashBoard(self):
        if self.dashboard is not None:
            try:
                self.dashboard.Close()
            except:
                pass

    def on_message(self, _, m):
        if not self.info.isStarted:
            if self.wsC:
                self.wsC.close()
        if m is None:
            return
        try:
            m = loads(m)
            if 'command' in m and m['command'] == 'configfile':
                del m['apwd']
                del m['pswd']
            self.Log(self.text.wsMssg % repr(m), 5)
            self.lastMessage = ttime()
            self.msgWait = DEFAULT_WAIT
        except:
            eg.PrintTraceback()
            self.refreshWebSocket()
            return
        if 'state' in m:
            self.state = m['state']
        if "token" in m:
            token = m['token']
            event = self.queryData[token]
            del m["token"]
            self.queryData[token] = m
            SetEvent(event)
            # return  # ToDo: make it optional
        if 'command' in m:
            cmd = m['command']
            if cmd in ('nop', 'state'):
                tmprtr = str(m['temperature'])
                hmdt = str(m['humidity'])
                self.checkLevels(tmprtr, hmdt)
                if self.dashboard:
                    self.dashboard.Update(tmprtr, hmdt)
            elif cmd == 'password':
                self.wsC.send("{'command':'password','password':'%s'}" % self.password)
            elif cmd == 'authorized':
                self.wsC.send("{'command':'getstate'}")
                self.TriggerEvent(self.text.connected)
            elif cmd == 'configfile':
                pass
            elif cmd == 'button':
                self.TriggerEvent("Button")
            elif cmd == 'change':
                if m['change']:
                    self.TriggerEvent(
                        "%s.%s" % (self.text.relState, RELSTATES[self.state]),
                        payload=self.state
                    )
            if self.dashboard is not None:
                self.dashboard.SetState(self.state)

        else:
            eg.PrintNotice(unknmsg % (self.info.eventPrefix, repr(m)))

    def Configure(
        self,
        prefix=None,
        debug=3,
        mode=0,
        host="ws://",
        port=80,
        password="",
        channel="",
        cmdrsrc="",
        msgrsrc="",
        bbt_tkn="",
        bbt_api="",
        bbt_secret="",
        dummy="",
        proxy=None,
        tempLevels=None,
        humiLevels=None,
    ):
        if humiLevels is None:
            humiLevels = []
        if tempLevels is None:
            tempLevels = []
        if proxy is None:
            proxy = ["", 0, "", ""]
        prefix = self.name if prefix is None else prefix
        if not isinstance(proxy[3], eg.Password):
            p = eg.Password(None)
            p.Set("")
            proxy[3] = p
        if not isinstance(bbt_tkn, eg.Password):
            tkn = eg.Password(None)
            tkn.Set("")
            bbt_tkn = tkn
        tkn = bbt_tkn
        if not isinstance(bbt_api, eg.Password):
            api = eg.Password(None)
            api.Set("")
            bbt_api = api
        api = bbt_api
        if not isinstance(bbt_secret, eg.Password):
            secret = eg.Password(None)
            secret.Set("")
            bbt_secret = secret
        secret = bbt_secret
        text = self.text
        panel = eg.ConfigPanel(self)
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        panel.proxy = cpy(proxy)

        if not isinstance(password, eg.Password):
            passw = eg.Password(None)
            passw.Set(password)
        else:
            passw = password
        debugLabel2 = wx.StaticText(panel, -1, text.debug2)
        debugCtrl = eg.SpinIntCtrl(
            panel,
            -1,
            debug,
            min=1,
            max=5
        )
        debugSizer = wx.BoxSizer(wx.HORIZONTAL)
        debugSizer.Add(debugCtrl, 0, wx.RIGHT, 5)
        debugSizer.Add(debugLabel2, 0, flag=ACV)
        prefixCtrl = panel.TextCtrl(prefix)

        rb0 = panel.RadioButton(mode == 0, self.text.mode0, style=wx.RB_GROUP)
        rb1 = panel.RadioButton(mode == 1, self.text.mode1)
        modeSizer = wx.BoxSizer(wx.HORIZONTAL)
        modeSizer.Add(rb0)
        modeSizer.Add(rb1, 0, wx.LEFT, 10)
        labels = (
            panel.StaticText(text.prefix),
            panel.StaticText(text.debug),
            panel.StaticText(text.mode)
        )
        eg.EqualizeWidths(labels)
        topSizer = wx.FlexGridSizer(3, 2, 10, 5)
        topSizer.Add(labels[0], 0, ACV | wx.LEFT, 10)
        topSizer.Add(prefixCtrl, 0, wx.EXPAND | wx.LEFT, 5)
        topSizer.Add(labels[1], 0, ACV | wx.LEFT, 10)
        topSizer.Add(debugSizer, 0, wx.EXPAND | wx.LEFT, 5)
        topSizer.Add(labels[2], 0, ACV | wx.LEFT, 10)
        topSizer.Add(modeSizer, 0, wx.EXPAND | wx.LEFT, 5)

        sizer = wx.FlexGridSizer(10, 2, 8, 5)
        sizer.AddGrowableCol(1)
        labels0 = (
            panel.StaticText(text.host),
            panel.StaticText(text.port),
            panel.StaticText(text.password)
        )
        labels1 = (
            panel.StaticText(text.channel),
            panel.StaticText(text.cmdrsrc),
            panel.StaticText(text.msgrsrc),
            panel.StaticText(text.apikey),
            panel.StaticText(text.secretkey),
            panel.StaticText(text.token)
        )
        ctrls0 = (
            panel.TextCtrl(host),
            panel.SpinIntCtrl(port, min=1, max=65535),
            wx.TextCtrl(panel, -1, passw.Get(), style=wx.TE_PASSWORD)
        )
        ctrls1 = (
            wx.TextCtrl(panel, -1, channel),
            wx.TextCtrl(panel, -1, cmdrsrc),
            wx.TextCtrl(panel, -1, msgrsrc),
            wx.TextCtrl(panel, -1, bbt_api.Get(), style=wx.TE_PASSWORD),
            wx.TextCtrl(panel, -1, bbt_secret.Get(), style=wx.TE_PASSWORD),
            wx.TextCtrl(panel, -1, bbt_tkn.Get(), style=wx.TE_PASSWORD)
        )
        sizer.Add((-1, 1))
        sizer.Add((-1, 1))
        for i in range(len(labels0)):
            sizer.Add(labels0[i], 0, ACV)
            sizer.Add(ctrls0[i], 0, wx.EXPAND)
        for i in range(len(labels1)):
            sizer.Add(labels1[i], 0, ACV)
            sizer.Add(ctrls1[i], 0, wx.EXPAND)

        staticBox = wx.StaticBox(panel, label="")
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)

        ttl = panel.dialog.GetTitle()
        panel.dialog.SetTitle(
            "%s - %s - %s %s" % (self.name, ttl, self.text.version, version)
        )

        #        #Temperature handling
        label1 = wx.StaticText(panel, -1, self.text.label1)
        coldefs1 = (
            (self.text.header1[0], "left", 0, True),
            (self.text.header1[1], "left", 1, False),
            (self.text.header1[2], "left", 3, False, (3, 1, True, -39.5, 125.0, 0.5)),
            (self.text.header1[3], "left", 0, True),
            (self.text.header1[4], "left", 0, True),
        )
        temp_table = ObjectListCtrl(panel, coldefs1, 3, Level)
        temp_table.SetEmptyListMsg(self.text.noLevel1)
        temp_table.SetEmptyListMsgFont(wx.Font(22, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
        temp_table.SortBy(3, ascending=False)
        self.temp_table = temp_table
        temp_table.SetData(tempLevels)

        def enableButtons1(enable):
            for b in range(1, len(self.text.buttons)):
                wx.FindWindowById(bttns1[b]).Enable(enable)

        def OnGridChange1(evt):
            value = evt.GetValue()
            if value == "Empty":
                enableButtons1(False)
            elif value == "One":
                enableButtons1(True)
            evt.Skip()

        temp_table.Bind(eg.EVT_VALUE_CHANGED, OnGridChange1)

        def edit1():
            dlg = extDialog(
                parent=panel,
                plugin=self,
                coldefs=coldefs1,
                grid=temp_table,
                ix=temp_table.GetSelectedItemIx(),
                rowdata=temp_table.GetRow()
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowExtDialog,
                self.text.title1,
            )

        def OnActivated1(evt):
            edit1()
            evt.Skip()

        temp_table.Bind(wx.EVT_LIST_ITEM_ACTIVATED, OnActivated1)

        def onButton1(evt):
            id = evt.GetId()
            if id == bttns1[0]:  # Add
                dlg = extDialog(
                    parent=panel,
                    plugin=self,
                    coldefs=coldefs1,
                    grid=temp_table,
                    ix=-1,
                    rowdata=None,
                )
                dlg.Centre()
                wx.CallAfter(
                    dlg.ShowExtDialog,
                    self.text.title1,
                )
            elif id == bttns1[1]:  # Duplicate
                dlg = extDialog(
                    parent=panel,
                    plugin=self,
                    coldefs=coldefs1,
                    grid=temp_table,
                    ix=-1,
                    rowdata=temp_table.GetRow()
                )
                dlg.Centre()
                wx.CallAfter(
                    dlg.ShowExtDialog,
                    self.text.title1,
                )
            elif id == bttns1[2]:  # Edit
                edit1()
            elif id == bttns1[3]:  # Delete
                temp_table.DeleteRow()
            evt.Skip()

        bttnSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        bttnSizer1.Add((5, -1))
        i = 0
        bttns1 = []
        for bttn in self.text.buttons:
            id = wx.NewIdRef()
            bttns1.append(id)
            b = wx.Button(panel, id, bttn)
            bttnSizer1.Add(b, 1)
            if not len(tempLevels) and i not in (0,):
                b.Enable(False)
            if i == 0:
                b.SetDefault()
            b.Bind(wx.EVT_BUTTON, onButton1, id=id)
            bttnSizer1.Add((5, -1))
            i += 1

        #        #Humidity handling
        label2 = wx.StaticText(panel, -1, self.text.label2)
        coldefs2 = (
            (self.text.header2[0], "left", 0, True),
            (self.text.header2[1], "left", 1, False),
            (self.text.header2[2], "left", 3, False, (3, 1, True, 0.0, 100.0, 0.5)),
            (self.text.header2[3], "left", 0, True),
            (self.text.header2[4], "left", 0, True),
        )
        humi_table = ObjectListCtrl(panel, coldefs2, 3, Level)
        humi_table.SetEmptyListMsg(self.text.noLevel2)
        humi_table.SetEmptyListMsgFont(wx.Font(22, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
        humi_table.SortBy(3, ascending=False)

        self.humi_table = humi_table
        humi_table.SetData(humiLevels)

        def enableButtons2(enable):
            for b in range(1, len(self.text.buttons)):
                wx.FindWindowById(bttns2[b]).Enable(enable)

        def OnGridChange2(evt):
            value = evt.GetValue()
            if value == "Empty":
                enableButtons2(False)
            elif value == "One":
                enableButtons2(True)
            evt.Skip()

        humi_table.Bind(eg.EVT_VALUE_CHANGED, OnGridChange2)

        def edit2():
            dlg = extDialog(
                parent=panel,
                plugin=self,
                coldefs=coldefs2,
                grid=humi_table,
                ix=humi_table.GetSelectedItemIx(),
                rowdata=humi_table.GetRow()
            )
            dlg.Centre()
            wx.CallAfter(
                dlg.ShowExtDialog,
                self.text.title2,
            )

        def OnActivated2(evt):
            edit2()
            evt.Skip()

        humi_table.Bind(wx.EVT_LIST_ITEM_ACTIVATED, OnActivated2)

        def onButton2(evt):
            id = evt.GetId()
            if id == bttns2[0]:  # Add
                dlg = extDialog(
                    parent=panel,
                    plugin=self,
                    coldefs=coldefs2,
                    grid=humi_table,
                    ix=-1,
                    rowdata=None,
                )
                dlg.Centre()
                wx.CallAfter(
                    dlg.ShowExtDialog,
                    self.text.title2,
                )
            elif id == bttns2[1]:  # Duplicate
                dlg = extDialog(
                    parent=panel,
                    plugin=self,
                    coldefs=coldefs2,
                    grid=humi_table,
                    ix=-1,
                    rowdata=humi_table.GetRow()
                )
                dlg.Centre()
                wx.CallAfter(
                    dlg.ShowExtDialog,
                    self.text.title2,
                )
            elif id == bttns2[2]:  # Edit
                edit2()
            elif id == bttns2[3]:  # Delete
                humi_table.DeleteRow()
            evt.Skip()

        bttnSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        bttnSizer2.Add((5, -1))
        i = 0
        bttns2 = []
        for bttn in self.text.buttons:
            id = wx.NewIdRef()
            bttns2.append(id)
            b = wx.Button(panel, id, bttn)
            bttnSizer2.Add(b, 1)
            if not len(humiLevels) and i not in (0,):
                b.Enable(False)
            if i == 0:
                b.SetDefault()
            b.Bind(wx.EVT_BUTTON, onButton2, id=id)
            bttnSizer2.Add((5, -1))
            i += 1
        #
        panel.sizer.Add(topSizer, 0, wx.EXPAND | wx.TOP, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        panel.sizer.Add(label1, 0, wx.TOP | wx.LEFT, 5)
        panel.sizer.Add(temp_table, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)
        panel.sizer.Add(bttnSizer1, 0, wx.EXPAND)

        panel.sizer.Add(label2, 0, wx.TOP | wx.LEFT, 5)
        panel.sizer.Add(humi_table, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)
        panel.sizer.Add(bttnSizer2, 0, wx.EXPAND)

        proxyBtn = wx.Button(panel.dialog, -1, text.proxyTitle)

        def onProxyBtn(evt):
            dlg = ProxyDialog(
                parent=panel,
                plugin=self,
                labels=text.headers,
                data=panel.proxy,
            )
            wx.CallAfter(
                dlg.ShowProxyDlg, text.proxyTitle
            )
            evt.Skip()

        proxyBtn.Bind(wx.EVT_BUTTON, onProxyBtn)
        panel.dialog.buttonRow.Add(proxyBtn)

        # ONLY FOR DIALOG FITTING
        for item in labels0:  #
            item.Show(False)  #
        for item in ctrls0:  #
            item.Show(False)  #

        # ONLY FOR DIALOG FITTING

        def redrawDialog(evt):
            md = 0 if rb0.GetValue() else 1
            for item in labels1:
                item.Show(md)
            for item in ctrls1:
                item.Show(md)
            md = not md
            for item in labels0:
                item.Show(md)
            for item in ctrls0:
                item.Show(md)
            panel.sizer.Layout()
            evt.Skip()

        rb0.Bind(wx.EVT_RADIOBUTTON, redrawDialog)
        rb1.Bind(wx.EVT_RADIOBUTTON, redrawDialog)
        panel.dialog.Bind(wx.EVT_SHOW, redrawDialog)

        while panel.Affirmed():
            oldPassw = passw.Get()
            newPassw = ctrls0[2].GetValue()
            if oldPassw != newPassw:
                passw.Set(newPassw)
                dummy = str(ttime())
            if proxy[3].Get() != panel.proxy[3].Get():
                dummy = str(ttime())
            oldTkn = tkn.Get()
            newTkn = ctrls1[5].GetValue()
            if oldTkn != newTkn:
                tkn.Set(newTkn)
                dummy = str(ttime())
            oldApi = api.Get()
            newApi = ctrls1[3].GetValue()
            if oldApi != newApi:
                api.Set(newApi)
                dummy = str(ttime())
            oldSecret = secret.Get()
            newSecret = ctrls1[4].GetValue()
            if oldSecret != newSecret:
                secret.Set(newSecret)
                dummy = str(ttime())
            if proxy[3].Get() != panel.proxy[3].Get():
                dummy = str(ttime())
            panel.SetResult(
                prefixCtrl.GetValue(),
                debugCtrl.GetValue(),
                int(rb1.GetValue()),
                ctrls0[0].GetValue(),
                ctrls0[1].GetValue(),
                passw,
                ctrls1[0].GetValue(),
                ctrls1[1].GetValue(),
                ctrls1[2].GetValue(),
                tkn,
                api,
                secret,
                dummy,
                panel.proxy,
                temp_table.GetData(),
                humi_table.GetData()
            )


# ===============================================================================

class ProxyDialog(wx.Frame):
    def __init__(
        self,
        parent,
        plugin,
        labels,
        data,
    ):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.RESIZE_BORDER,
            name="ProxyDialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.labels = labels
        self.data = data

    def ShowProxyDlg(self, title):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)
        text = self.plugin.text
        panel = wx.Panel(self)

        def wxst(label):
            return wx.StaticText(panel, -1, label)

        labels = self.labels
        data = self.data
        rows = len(labels)
        sizer = wx.GridBagSizer(5, 5)
        for row in range(rows):
            sizer.Add(wxst(labels[row]), (row, 0), flag=ACV)
            if row not in (1, 3):
                txtCtrl = wx.TextCtrl(panel, -1, data[row])
            elif row == 1:
                txtCtrl = eg.SpinIntCtrl(
                    panel,
                    -1,
                    data[row],
                    min=0,
                    max=65535
                )
            elif row == 3:
                self.password = eg.Password(data[row])
                txtCtrl = wx.TextCtrl(
                    panel,
                    -1,
                    self.password.Get(),
                    style=wx.TE_PASSWORD
                )
            sizer.Add(txtCtrl, (row, 1), flag=wx.EXPAND)
        info = wxst(text.proxyInfo)
        info.Enable(False)
        sizer.Add(info, (rows, 0), (1, 2), flag=ACV)
        sizer.AddGrowableCol(1)

        line = wx.StaticLine(
            panel,
            -1,
            style=wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)
        mainSizer.Add(btnsizer, 0, wx.EXPAND | wx.RIGHT, 10)
        mainSizer.Add((1, 6))
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()

        self.Bind(wx.EVT_CLOSE, onClose)

        def onOk(evt):
            data = []
            children = sizer.GetChildren()
            for child in range(1, len(children), 2):
                ctrl = children[child].GetWindow()
                if child != 7:
                    data.append(ctrl.GetValue())
                else:
                    self.password.Set(ctrl.GetValue())
                    data.append(self.password)
            self.GetParent().proxy = data
            self.Close()

        btn1.Bind(wx.EVT_BUTTON, onOk)

        def onCancel(evt):
            self.Close()

        btn2.Bind(wx.EVT_BUTTON, onCancel)

        mainSizer.Layout()
        w, h = self.GetSize()
        self.SetSize((max(w, 300), h))
        self.SetMinSize((max(w, 300), h))
        self.Raise()
        self.MakeModal(True)
        self.Centre()
        self.Show()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

# ===============================================================================

class pinCommand(eg.ActionBase):
    class text:
        val = "State:"

    def __call__(self, val=0):
        if self.plugin.mode:
            data = self.plugin.SendMessage(
                self.value,
                val if self.value == "setstate" else None
            )
            if data is not None:
                if isinstance(data, dict) and "state" in data:
                    return RELSTATES[data['state']]
        else:
            data = self.plugin.SendCommand(
                self.value,
                val if self.value == "setstate" else None
            )
            if data is not None:
                if isinstance(data, dict) and "state" in data:
                    return RELSTATES[data['state']]

    def GetLabel(self, val=0):
        if self.value == "setstate":
            return "%s: %s" % (self.name, RELSTATES[val])
        else:
            return "%s" % self.name

    def Configure(self, val=0):
        text = self.text
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.plugin.info.icon.GetWxIcon())
        if self.value == "setstate":
            valLabel = wx.StaticText(panel, -1, text.val)
            valCtrl = wx.Choice(panel, -1, choices=RELSTATES)
            valCtrl.SetSelection(val)

        sizer = wx.FlexGridSizer(2 if self.value == "setstate" else 1, 2, 10, 10)

        if self.value == "setstate":
            sizer.Add(valLabel, 0, ACV)
            sizer.Add(valCtrl)
        panel.sizer.Add(sizer, 0, wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(
                valCtrl.GetSelection() if self.value == "setstate" else None,
            )


# ===============================================================================

# class sendPing(eg.ActionBase):
#
#    def __call__(self):
#        if self.plugin.mode:
#            pass
#        else:
#            self.plugin.SendCommand("ping", None)
#        #msg = {"command":"ping"}
#        #try:
#        #    self.plugin.wsC.send(msg)
#        #except:
#        #    eg.PrintTraceback()
# ===============================================================================

class getValue(eg.ActionBase):

    def __call__(self):
        val = self.plugin.hmdt if self.value else self.plugin.tmprtr
        return float(val)


# ===============================================================================

class openDashBoard(eg.ActionBase):

    def __call__(self):
        self.plugin.OpenDashboard()


# ===============================================================================

class closeDashBoard(eg.ActionBase):

    def __call__(self):
        self.plugin.CloseDashBoard()


# ===============================================================================

ACTIONS = (
    (pinCommand,
     "GetState",
     "Get state",
     "Get state.",
     "getstate"
     ),
    (pinCommand,
     "ToggleState",
     "Toggle state",
     "Toggles state.",
     "toggle"
     ),
    (pinCommand,
     "SetState",
     "Set state",
     "Set state",
     "setstate"
     ),
    # (sendPing,
    #    "SendPing",
    #    "Send ping",
    #    "Sends ping",
    #    None
    # ),
    (getValue,
     "GetTemp",
     "Get temperature",
     "Gets temperature.",
     0
     ),
    (getValue,
     "GetHumi",
     "Get humidity",
     "Gets humidity.",
     1
     ),
    (openDashBoard,
     "openDashBoard",
     "Open dashboard",
     "Opens dashboard.",
     None
     ),
    (closeDashBoard,
     "closeDashBoard",
     "Close dashboard",
     "Closes dashboard.",
     None
     ),
)
# ===============================================================================

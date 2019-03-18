# -*- coding: utf-8 -*-
version="0.0"

# Plugins/ICS_Relay/__init__.py
#
# Copyright (C)  2015 Pako  (lubos.ruckl@quick.cz)
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
# 0.0 by Pako 2015-05-26 11:03 UTC+1
#     - initial version
#===============================================================================

eg.RegisterPlugin(
    name = "ICS_Relay",
    author = "Pako",
    guid = "{C475375B-85C1-4959-AC78-DEEBB1FC79CE}",
    version = version,
    kind = "external",
    createMacrosOnAdd = True,
    canMultiLoad = True,
    description =  ur"""<rst>
Plugin to control cheap `ICstation USB Relay Board`__ series **ICSE01XA**.

| **Warning Notice**:
| Particularly for users of Windows 8 !
| Do not install the latest drivers from the website Prolific !
| It does not work !
| It is necessary to use older drivers that support ("fake") chip PL-2303HX.

| **There are three types of boards:**
| ICSE012A - 4 channels
| ICSE013A - 2 channels
| ICSE014A - 8 channels

| It is possible to buy these boards preferably also through the eBay 
 (free shipping may be).

| **Notice:**
| These boards are actually very cheap, but you must reckon with some drawbacks 
 as well:

1. After powering up (connection to USB port) all relays are switched ON.
2. There is absolutely no feedback. We can not read the status of each channel. 
   Plugin has to maintain a "picture" of the state in its memory.
3. There is no command to reset boards.
4. The type of board can be read only once during the initialization 
   (after powering up). Then it is impossible to read anything.
5. The boards have no serial number. 
   Operating system can not distinguish between the two "identical" boards
   (actually it can be completely different device that uses a Prolific chip).
   *The operating system assigns a port number based on the USB port.*

__ http://www.icstation.com/relay-module-c-208_209_251.html
""",

    icon = (
        "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"
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6955"
)
#===============================================================================

import eg
import wx
from time import sleep
from _winreg import OpenKey, QueryValueEx, EnumValue, HKEY_LOCAL_MACHINE
from re import search
from wx.lib.statbmp import GenStaticBitmap
from base64 import b64decode
from StringIO import StringIO
#===============================================================================
 
myEVT_STATUS_BITMAP_CHANGED = wx.NewEventType()
EVT_STATUS_BITMAP_CHANGED = wx.PyEventBinder(myEVT_STATUS_BITMAP_CHANGED, 1)
 
myEVT_BITMAP_MOUSE_IN = wx.NewEventType()
EVT_BITMAP_MOUSE_IN = wx.PyEventBinder(myEVT_BITMAP_MOUSE_IN, 1)
 
myEVT_BITMAP_MOUSE_OUT = wx.NewEventType()
EVT_BITMAP_MOUSE_OUT = wx.PyEventBinder(myEVT_BITMAP_MOUSE_OUT, 1)

BOARDS = {
    '\xAB':('ICSE012A', '4'),
    '\xAD':('ICSE013A', '2'),
    '\xAC':('ICSE014A', '8'),
    '':('', '')
}

RED = (
        "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"
        "d0I7eTmtdjrm9NbZwVnsfNj5FxemS5pLi8ujecbz+PMa54256rlyXOtdpW4Mt0S3vW5S"
        "d113jnuD+wMPfQ+eR5PHhKepZ6rnQc9nXtZeIq8Or9dsZ/ZK9ilvxNvPu8R70IfiE+VT"
        "7XPfV8832bfVd8rP3m+F3yl/tH+Q/zb/GwFaAdyA5oCpQMfAlYF9QaSgBUHVQQ+CzYJF"
        "wT0hcEhgyPaQu/MN5wvnd4WC0IDQ7aH3wozDloV9H44JDwuvCX8YYRNRENG/gLpgyYKW"
        "Ba8ivSLLIu9EmURJonqjFaMTopujX8d4x5THSGOtYlfGXorTiBPEdcdj46Pjm+KnF/os"
        "3LlwPME+oTjh+iLjRXmLLizWWJy++PgSxSWcJUcS0YkxiS2J7zmhnAbO9NKApbVLp7hs"
        "7i7uE54Hbwdvku/KL+dPJLkmlSc9SnZN3p48meKeUpHyVMAWVAuep/qn1qW+TgtN25/2"
        "KT0mvT0Dl5GYcVRIEaYJ+zK1M/Myh7PMs4qzpMucl+1cNiUKEjVlQ9mLsrvFNNnP1IDE"
        "RLJeMprjllOT8yY3OvdInnKeMG9gudnyTcsn8n3zv16BWsFd0VugW7C2YHSl58r6VdCq"
        "pat6V+uvLlo9vsZvzYG1hLVpa38otC4sL3y5LmZdT5FW0ZqisfV+61uLFYpFxTc2uGyo"
        "24jaKNg4uGnupqpNH0t4JRdLrUsrSt9v5m6++JXNV5VffdqStGWwzKFsz1bMVuHW69vc"
        "tx0oVy7PLx/bHrK9cwdjR8mOlzuX7LxQYVdRt4uwS7JLWhlc2V1lULW16n11SvVIjVdN"
        "e61m7aba17t5u6/s8djTVqdVV1r3bq9g7816v/rOBqOGin2YfTn7HjZGN/Z/zfq6uUmj"
        "qbTpw37hfumBiAN9zY7NzS2aLWWtcKukdfJgwsHL33h/093GbKtvp7eXHgKHJIcef5v4"
        "7fXDQYd7j7COtH1n+F1tB7WjpBPqXN451ZXSJe2O6x4+Gni0t8elp+N7y+/3H9M9VnNc"
        "5XjZCcKJohOfTuafnD6Vderp6eTTY71Leu+ciT1zrS+8b/Bs0Nnz53zPnen37D953vX8"
        "sQvOF45eZF3suuRwqXPAfqDjB/sfOgYdBjuHHIe6Lztd7hmeN3ziivuV01e9r567FnDt"
        "0sj8keHrUddv3ki4Ib3Ju/noVvqt57dzbs/cWXMXfbfkntK9ivua9xt+NP2xXeogPT7q"
        "PTrwYMGDO2PcsSc/Zf/0frzoIflhxYTORPMj20fHJn0nLz9e+Hj8SdaTmafFPyv/XPvM"
        "5Nl3v3j8MjAVOzX+XPT806+bX6i/2P/S7mXvdNj0/VcZr2Zel7xRf3PgLett/7uYdxMz"
        "ue+x7ys/mH7o+Rj08e6njE+ffgP3hPP74FSqLwAAACBjSFJNAAB6JgAAgIQAAPoAAACA"
        "6AAAdTAAAOpgAAA6mAAAF3CculE8AAAEFklEQVRIx7WWy4scVRSHv3vr0V3dM5ln5kWM"
        "j8REDZpERFA3AV0pJAgmJIK4UBDX+QvMUnGRZVARBSFkEIIIIuJC0E0QokRMIgSjSZxx"
        "Mo/MdHdNd9W957jo6p5uYxINWFBUXW7x/c75nXPvLfifL3OnD96FZGaG8WB4aCyJwmFx"
        "kuf1fKmV1Rd/mWP5LZC7Evh4konRrTP7qqNjzyajI08ESWkyisJYVMU1szRrNC6lSyvf"
        "Nuauf5VfXPn+EGT/VsCc3j22b3zb9jc3TY0/V0qCEZuvo1mKZk3UWIgTNK6Sa+jTtfVL"
        "q1eunVw+f/79I39w5bYCpyBIdk8cntr9yNGBwXCvWZ3H31hEWykqgiqoglfQIMSUB7Fj"
        "M7RMpbW2sHJq6dwPbx++yk+9zKB38OqeqZcmHr7/2GDc2iXXLiKrS2iegyqqIAoixdN7"
        "XJqSLS1gfB6G1cFHw6Gx8efXFs5+mrJyk8Dsjupj0w89cGxTvL5X5n8FlxcRK3SiVhBV"
        "RBQR8NIeu3oDyVJjk8rOYGQsP3B58btZcAAW4AREY1umD5dl7SlZ+B1EUNXibsOlgHuv"
        "+ALuRfG+/Z6t1fArC1GAO2QfHHqmE7gFGN1W3VE2rRfC5kpAD7gPLm24CIXIBtyJdkWy"
        "2uq9tlLafxxKACFAKbaP06xvy7IMa9ulV+j6rtqOVqQtJAret+vhtS3kRGk5Jctqxtjo"
        "6YlJpvmTy+EpCKy4XcZJxVntgpXOvZGNdIQKASfgvJJ7yERxHrwIgc23RJXyPdC8HDYn"
        "KQ9YJkGNdL0u/JaNzvFa2FOI+OLdSY9o8b06SQxMAoRlwahKJGoxmP4oZSNq3wsv5nyn"
        "NtIfGIo1Sgxgr5Twgql7NTcDRHGibSt6irnRQT3CnRZu+5obIzUAe/QqTfH85j3e9wD6"
        "YRtZ9Al1suwpPoC1pma8v9ppU3Viz+aEy7eCOVGc9s91wJ3ItdP3QUgYBBdCoStAupr+"
        "mIk9Kza+jSV05zZs0T44xhBFURZgvzw4z2JX4JVF5pyzJ50p3RAb3jKLvxdTtH/njCtV"
        "oiA8Y9cbXxRLqS0AsLq8/FnuzCzRgJcw7mbRa0lv8fvgxhJvGqIURnOmmb53ZJ4LN212"
        "p2usv0jjEtXqlC0lO8UG1uU5rtgeeiPvZQdxifLwCJGx16nXjjda6x9+Xif/x+16ts71"
        "/aZxzpYr5SCpbjeVgbLaAKFYQO0qYsOQMEkoDQ0TVwc1Erlo1lbe8en6idfmSe94ZH4w"
        "xebB4aEDJqm+TFze48NgWBUjIoUjFsRnJsvnSNOvtVb/JLzW+uYQ+P906H80zda4lOzV"
        "OH5SbXCfscEwaG6cW1CX/2yarTONljv3+hK1u/6r6BylbCahRNyoIVmF7I25fitudf0F"
        "D3c2SgRcEsYAAAAASUVORK5CYII="
    )

GREEN = (
        "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"
        "d0I7eTmtdjrm9NbZwVnsfNj5FxemS5pLi8ujecbz+PMa54256rlyXOtdpW4Mt0S3vW5S"
        "d113jnuD+wMPfQ+eR5PHhKepZ6rnQc9nXtZeIq8Or9dsZ/ZK9ilvxNvPu8R70IfiE+VT"
        "7XPfV8832bfVd8rP3m+F3yl/tH+Q/zb/GwFaAdyA5oCpQMfAlYF9QaSgBUHVQQ+CzYJF"
        "wT0hcEhgyPaQu/MN5wvnd4WC0IDQ7aH3wozDloV9H44JDwuvCX8YYRNRENG/gLpgyYKW"
        "Ba8ivSLLIu9EmURJonqjFaMTopujX8d4x5THSGOtYlfGXorTiBPEdcdj46Pjm+KnF/os"
        "3LlwPME+oTjh+iLjRXmLLizWWJy++PgSxSWcJUcS0YkxiS2J7zmhnAbO9NKApbVLp7hs"
        "7i7uE54Hbwdvku/KL+dPJLkmlSc9SnZN3p48meKeUpHyVMAWVAuep/qn1qW+TgtN25/2"
        "KT0mvT0Dl5GYcVRIEaYJ+zK1M/Myh7PMs4qzpMucl+1cNiUKEjVlQ9mLsrvFNNnP1IDE"
        "RLJeMprjllOT8yY3OvdInnKeMG9gudnyTcsn8n3zv16BWsFd0VugW7C2YHSl58r6VdCq"
        "pat6V+uvLlo9vsZvzYG1hLVpa38otC4sL3y5LmZdT5FW0ZqisfV+61uLFYpFxTc2uGyo"
        "24jaKNg4uGnupqpNH0t4JRdLrUsrSt9v5m6++JXNV5VffdqStGWwzKFsz1bMVuHW69vc"
        "tx0oVy7PLx/bHrK9cwdjR8mOlzuX7LxQYVdRt4uwS7JLWhlc2V1lULW16n11SvVIjVdN"
        "e61m7aba17t5u6/s8djTVqdVV1r3bq9g7816v/rOBqOGin2YfTn7HjZGN/Z/zfq6uUmj"
        "qbTpw37hfumBiAN9zY7NzS2aLWWtcKukdfJgwsHL33h/093GbKtvp7eXHgKHJIcef5v4"
        "7fXDQYd7j7COtH1n+F1tB7WjpBPqXN451ZXSJe2O6x4+Gni0t8elp+N7y+/3H9M9VnNc"
        "5XjZCcKJohOfTuafnD6Vderp6eTTY71Leu+ciT1zrS+8b/Bs0Nnz53zPnen37D953vX8"
        "sQvOF45eZF3suuRwqXPAfqDjB/sfOgYdBjuHHIe6Lztd7hmeN3ziivuV01e9r567FnDt"
        "0sj8keHrUddv3ki4Ib3Ju/noVvqt57dzbs/cWXMXfbfkntK9ivua9xt+NP2xXeogPT7q"
        "PTrwYMGDO2PcsSc/Zf/0frzoIflhxYTORPMj20fHJn0nLz9e+Hj8SdaTmafFPyv/XPvM"
        "5Nl3v3j8MjAVOzX+XPT806+bX6i/2P/S7mXvdNj0/VcZr2Zel7xRf3PgLett/7uYdxMz"
        "ue+x7ys/mH7o+Rj08e6njE+ffgP3hPP74FSqLwAAACBjSFJNAAB6JgAAgIQAAPoAAACA"
        "6AAAdTAAAOpgAAA6mAAAF3CculE8AAAER0lEQVRIx7WWy4sdRRTGf1XdfR9z52YmufPI"
        "BDVRBwWDeaiIMQsDuhCFBCSGRJAsFMR1/gKzVATFVVAXCkLIKIobEXEREx9EJZFITMRg"
        "zCROnMzDmbm3597uqnNcdN/HGDUasKDoKqr6+75zztdVDf9zM9fb8MDLlKN1DFWDgVq5"
        "HA4mImkrTWdbrfrM0R+Z4wXkhgi2vc3I+jXrdgxVag8PllffVw6Ko4UoLKioLLskrieN"
        "87Px/PErjaufXEjnvzmzh+TfEpgnPqjtGB8af35s1dAjq4rBamuX8RrjtAlqsZQxWqGZ"
        "hn4uXj4/uXD58Lm5H944to/JfyY4QrC7PLJ389q7Doz0h1u9uULTz5BqjKggCqLgPaAh"
        "oanSZ9cRt/palxfnj5yaPfXil3v5vhcy6J3s3r9298aRWw8OV1sbYzlHU2bxmqIoXkEk"
        "614gFU/TxSwk0xiThuWweveqsDZUeGz65OR7zF9D8OhEZdPmsdsODq9a3hrLzwgpqqCq"
        "eEA8eAUvmndwHpwoDdfASWyKtu/O/qCWFnfNfH5pAgdgAe49RLShNra3UlrcFstFFEFV"
        "Ec2Uew9OMjDnldST92zsPNSTJRp+OgoCt6dmB7a3hVuAoTWVOyql1uM2nA+UDFiUDriX"
        "XLnXjMgrqdcsAg+py4gWkyWWk4X1RVvcOf4qRYAQoFS093jqty8mCYHNKm/ygoq0iTJw"
        "L0oqPVHlRKlTWi0lSZaMmOjB2ghjP8GFkCMExrqNaqSv6TLlKGj+RBVtu0foiQJSB4lT"
        "0hSSRHEOvBcI0psqUelmaF4INzUpRf2Mgpq2QyRXKr5n7ruF9blq78lBNSfP9qtKWQyj"
        "AOHqEkZUIhELxmSAf3qhF9B7zYDbc9HOvszGioDFUACwrUm8iql7bzoA7eI5rziXh+7I"
        "xrmDstzn4L1kAgbSwMgSgP3qAM1U+CX1eN/7gusl6hYzI+vucx31iuTHnrFmCeMvtV2k"
        "3tmTSRrOEaTD7ZR006ArgDoiOrUByY0AENiQIOSsC7nU+Q6W4vi7VmJPqhQ6KXHXpIRu"
        "unrqIdIFNxjCKEoI7MfHn2SmQ3DsaaZiZw8nrvi7SvjXKXHa89HlLpPMye1WLlQIo/CE"
        "2MZHmGzJthenFuY+bKZmAvq9kUI3Cr+yFl3lXXCDpb8wQFSMppyJX/9sH2dXHBUAX+9n"
        "9tfmb6/Eib4f2KqPTBUR002J9BSzR3YhKDJQrhEVoqtNrb+2WG++S09gK47rixNcHdnZ"
        "OB3avlIhqIwXTX/JaND1uIIhILAhpbBMtThIuVBVE8m52My/NOuXD516hvi6V+aWNxke"
        "rQ7sKpvKUyGlLdYHg6oYn/vQGIvgE2/SqRbxp7HW3zkWto6yB/+fLv3tb3FLVChvjbRw"
        "v9VgAyYYVDRV46a9pmdS0zrhG+70F8+ydMN/Fe2r9CEot6BQbCD1hOTb51am4u/aH2Fc"
        "PuX8b+9RAAAAAElFTkSuQmCC"
    )

GRAY = (
        "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"
        "d0I7eTmtdjrm9NbZwVnsfNj5FxemS5pLi8ujecbz+PMa54256rlyXOtdpW4Mt0S3vW5S"
        "d113jnuD+wMPfQ+eR5PHhKepZ6rnQc9nXtZeIq8Or9dsZ/ZK9ilvxNvPu8R70IfiE+VT"
        "7XPfV8832bfVd8rP3m+F3yl/tH+Q/zb/GwFaAdyA5oCpQMfAlYF9QaSgBUHVQQ+CzYJF"
        "wT0hcEhgyPaQu/MN5wvnd4WC0IDQ7aH3wozDloV9H44JDwuvCX8YYRNRENG/gLpgyYKW"
        "Ba8ivSLLIu9EmURJonqjFaMTopujX8d4x5THSGOtYlfGXorTiBPEdcdj46Pjm+KnF/os"
        "3LlwPME+oTjh+iLjRXmLLizWWJy++PgSxSWcJUcS0YkxiS2J7zmhnAbO9NKApbVLp7hs"
        "7i7uE54Hbwdvku/KL+dPJLkmlSc9SnZN3p48meKeUpHyVMAWVAuep/qn1qW+TgtN25/2"
        "KT0mvT0Dl5GYcVRIEaYJ+zK1M/Myh7PMs4qzpMucl+1cNiUKEjVlQ9mLsrvFNNnP1IDE"
        "RLJeMprjllOT8yY3OvdInnKeMG9gudnyTcsn8n3zv16BWsFd0VugW7C2YHSl58r6VdCq"
        "pat6V+uvLlo9vsZvzYG1hLVpa38otC4sL3y5LmZdT5FW0ZqisfV+61uLFYpFxTc2uGyo"
        "24jaKNg4uGnupqpNH0t4JRdLrUsrSt9v5m6++JXNV5VffdqStGWwzKFsz1bMVuHW69vc"
        "tx0oVy7PLx/bHrK9cwdjR8mOlzuX7LxQYVdRt4uwS7JLWhlc2V1lULW16n11SvVIjVdN"
        "e61m7aba17t5u6/s8djTVqdVV1r3bq9g7816v/rOBqOGin2YfTn7HjZGN/Z/zfq6uUmj"
        "qbTpw37hfumBiAN9zY7NzS2aLWWtcKukdfJgwsHL33h/093GbKtvp7eXHgKHJIcef5v4"
        "7fXDQYd7j7COtH1n+F1tB7WjpBPqXN451ZXSJe2O6x4+Gni0t8elp+N7y+/3H9M9VnNc"
        "5XjZCcKJohOfTuafnD6Vderp6eTTY71Leu+ciT1zrS+8b/Bs0Nnz53zPnen37D953vX8"
        "sQvOF45eZF3suuRwqXPAfqDjB/sfOgYdBjuHHIe6Lztd7hmeN3ziivuV01e9r567FnDt"
        "0sj8keHrUddv3ki4Ib3Ju/noVvqt57dzbs/cWXMXfbfkntK9ivua9xt+NP2xXeogPT7q"
        "PTrwYMGDO2PcsSc/Zf/0frzoIflhxYTORPMj20fHJn0nLz9e+Hj8SdaTmafFPyv/XPvM"
        "5Nl3v3j8MjAVOzX+XPT806+bX6i/2P/S7mXvdNj0/VcZr2Zel7xRf3PgLett/7uYdxMz"
        "ue+x7ys/mH7o+Rj08e6njE+ffgP3hPP74FSqLwAAACBjSFJNAAB6JgAAgIQAAPoAAACA"
        "6AAAdTAAAOpgAAA6mAAAF3CculE8AAAD6UlEQVRIx7VWTWgkRRh9VV2d6Z5JmMyMmzCJ"
        "SUxCRCKIKyKolyV6ExQEl0UyJKchSyAHPeTg2UA8SXROGjAQYTGCIAEj4kHwFIRFFFkD"
        "E9YoJDG7k9/u6fr3sNtNJ05244INRX/VdL339Xtf1dfA/3yRh70wPz/v9/T0POZ5Xqm9"
        "vb1TKSU553eDILizvr7eqNVq5pEIFhcXu/r6+q6USqVX8vn8867rdvu+36a1NpzzMAiC"
        "+sHBwY97e3vfHR4e/jQxMSEuSkBWV1evDA4OXu/u7n41l8sVKKXQWkNrfe8Fcm+ZEELv"
        "7+/Xd3Z2bmxubn5aqVT+fCBBrVZzhoaGro2Ojr5bLBYvW2sRRVECbq2FMQZKKQCA4zjw"
        "PA9RFPHd3d0vNjY2PqhUKr+eS7C2tvbWyMjI+6VSaUQIAa01jDGw1sJamxAZY5JYa41M"
        "JgNrrWk0Giv1ev29SqVSjzFpHKysrDwzPDw8UygURprN5oXAlVKQUuLw8BBBEFDP897s"
        "7++vLi8v+6cIFhYW3IGBgWu+77/IOQeABDwGUkrBGAMpZTJPjyAIEEWRSym9ms1mXz5F"
        "UC6Xn8xms685juPEGcbg6YyllIkHaaI4DoIAzWZzgDH2+tzcXAYAGAD4vv+cMWY4CAIw"
        "xgAgMTQeSqmEMAaNY6UUhBBoNpvgnBNCyEu9vb1lALdZrVZzKKVPA8gKIcA5T8CttQlZ"
        "2tR05kIISCkRRRGEEFBKgTH2OGOsD8Bt5rquxxjrBkDScsR6t3qW1j6ex8T35fWttd0A"
        "wDo6Oogxxj1ranw/T5IYOC1far9QxlgbANCtrS1tjDlpVRlnwWIJzn5FOiljDAghkhBy"
        "DAB0dnY20lr/IaXUDwJPm9mqguJiuH+UHFNK/4qryEopbwohGoyxS2clapVpWpJ0WQMA"
        "YwxtbW23YgIKAEdHRz9zzm+mTZRStjS0lTwxOCEEmUxGOI7z7djY2J2EYHJycptzfkNK"
        "eZA2MpYkHi3MTMABIJvNwnXddULIN+Vy2Z46i7a3t7/mnK9QSrUx5hRoq5JM7xNCCHK5"
        "HDzP27bWfjI+Pn7rX4ddtVq922g0PgzD8CvGmGaMJcdDGjRtJgC4rot8Pg/P8/aUUh/t"
        "7+9/CcCe23CWlpaeKhQK7zDGriql8mEYJrs0BqeUwnVdZDIZMMas4zi/c84/DsPws2q1"
        "Gjy0ZdZqtUtdXV1vMMbedhznWa11p7WWpDuatVYA2NZafy+l/Pzo6OiH6elp/Z+a/uLi"
        "Yr/neZcBvADgCUppJwAJ4G9jzG/W2vWTk5Nfpqamjh/5ryJupcVi0ddat0VRZMIwFDMz"
        "M+FF1v4DEL/v6F7gYJsAAAAASUVORK5CYII="
    )
#===============================================================================
 
class StatusBitmapEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self._state = -1
 
    def GetState(self):
        return self._state
#===============================================================================

class StatusBitmap(GenStaticBitmap):
    def __init__(self, *args, **kwds):
        if 'stateValues' in kwds:
            self.stateValues = kwds['stateValues']
            del kwds['stateValues']
        else:
            self.stateValues = []
        if 'tooltips' in kwds:
            self.tooltips = kwds['tooltips']
            del kwds['tooltips']
        else:
            self.tooltips = []
        if 'state' in kwds:
            self.currState = kwds['state']
            del kwds['state']
        else:
            self.currState = -1
        GenStaticBitmap.__init__(self, *args, bitmap=wx.NullBitmap, **kwds)
        self.SetState(self.currState)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseIn, self)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseOut, self)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp, self)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp, self)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        if self._bitmap:
            dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
            dc.Clear()
            dc.DrawBitmap(self._bitmap, 0, 0, True)
    
 
    def OnMouseIn(self, event):
        self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        evt = StatusBitmapEvent(myEVT_BITMAP_MOUSE_IN, self.GetId())
        evt._state = self.currState
        self.GetEventHandler().ProcessEvent(evt)
 

    def OnMouseOut(self, event):
        self.SetCursor(wx.Cursor(wx.CURSOR_DEFAULT))
        evt = StatusBitmapEvent(myEVT_BITMAP_MOUSE_OUT, self.GetId())
        evt._state = self.currState
        self.GetEventHandler().ProcessEvent(evt)
 

    def OnLeftUp(self, event):
        self.currState += 1
        if self.currState >= len(self.stateValues):
            self.currState = 0
        self.SetState(self.currState)
        self.SetToolTip(self.tooltips[self.currState]) 
        evt = StatusBitmapEvent(myEVT_STATUS_BITMAP_CHANGED, self.GetId())
        evt._state = self.currState
        self.GetEventHandler().ProcessEvent(evt)
 

    def OnRightUp(self, event):
        self.currState -= 1
        if self.currState < 0:
            self.currState = len(self.stateValues) - 1
        self.SetState(self.currState)
        self.SetToolTip(self.tooltips[self.currState])
        evt = StatusBitmapEvent(myEVT_STATUS_BITMAP_CHANGED, self.GetId())
        evt._state = self.currState
        self.GetEventHandler().ProcessEvent(evt)
 

    def SetTooltips(self, tips):
        self.tooltips = tips
 

    def GetValue(self):
        return self.currState
 

    def SetStateBitmaps(self, vals):
        self.stateValues = vals
 

    def SetState(self, state):
        if state > - 1 and state < len(self.stateValues):
            self.SetBitmap(self.stateValues[state])
            self.SetToolTip(self.tooltips[state])
            self.Update()
            self.currState = state 
#===============================================================================

class Text:
    board = "Port and board"
    port = "Serial port:"
    cc = "Number of channels:"
    bType = "Board type:"
    initState = "Required initial state"
    newState = "New state"
    channel = "Channel:"
    state = "State:"
    states = ("OFF", "ON", "No change")
    prefix = "Name and event prefix:"
    idProblem = "The problem with identifying ..."
    message = """Either it is not a relay board, or the board does not work or
initialization was performed earlier.\n 
Please disconnect the board and after a while connect it again 
(keep the dialogue open).\n\nAs soon as in EventGhost log 
"System.DeviceAttached" event occurs, repeat port selection !!!"""
    info1 = "%s: Port COM%i not found ..."
    info2 = """%s: No Ser2pl or Ser2pl64 service found to control
Prolific USB-serial COM ports.
Is the Prolific driver installed?"""
    info3 = "%s: Connection of port COM%i failed"
    info4 = "%s: The port COM%i is not Prolific USB-serial COM port !!!"
    connect = "Connected"
    disconnect = "Disconnected"
#===============================================================================

class ICS_Relay(eg.RawReceiverPlugin):
    text = Text
    curState = None
    initState = None
    coms = []
    flag = True
    bType = ''

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddActionsFromList(ACTIONS)
        self.serialThread = None


    def __start__(
        self,
        port = 0,
        bType = '',
        initState = [0,0,0,0,0,0,0,0],
        prefix = "ICS_Relay"
    ):
        coms = self.enumerate_ports()
        self.coms = coms
        self.port = port
        self.bType = bType
        self.info.eventPrefix = prefix
        self.curState = initState[:]
        self.initState = initState[:]
        eg.Bind("System.DeviceAttached", self.InitBoard)
        eg.Bind("System.DeviceRemoved", self.DeleteBoard)
        if self.port in self.coms:
            self.ConnectPort()
            #bType = self.SelectBoard() # init or not ?
        else:
            eg.PrintNotice(self.text.info1 % (prefix, self.port + 1))


    def __stop__(self):
        eg.Unbind("System.DeviceAttached", self.InitBoard)
        eg.Unbind("System.DeviceRemoved", self.DeleteBoard)
        if self.serialThread is not None:
            self.serialThread.Flush()
            self.serialThread.Stop()
            self.serialThread.Close()
            self.serialThread = None

  
    #def get_squids(self):
    #    '''Return unique serial numbers in Prolific registry'''
    #    squids = self.squids
    #    try:
    #      i = 0
    #      while 1:
    #        name, string, type = EnumValue(self.prolific_path, i)
    #        if type == 1: # 1 is for 'REG_SZ', 'A null-terminated string'
    #          sn = search('(?<=[\][0-9]&)\w+',string)
    #          if str(sn.group(0)) not in squids:
    #            squids.append(str(sn.group(0)))
    #        i += 1
    #    except WindowsError:
    #      pass
  

    def enumerate_ports(self):
        SER2PL32 = 'SYSTEM\\CurrentControlSet\\Services\\Ser2pl\\Enum'
        SER2PL64 = 'SYSTEM\\CurrentControlSet\\Services\\Ser2pl64\\Enum'
        
        try:
            # 32-bit Prolific driver
            self.arch = 32
            self.prolific_path = OpenKey(HKEY_LOCAL_MACHINE, SER2PL32)
        except WindowsError:
            try:
                # 64-bit
                self.arch = 64
                self.prolific_path = OpenKey(HKEY_LOCAL_MACHINE, SER2PL64)
            except WindowsError:
                eg.PrintNotice(self.text.info2 % self.info.eventPrefix)
                return []
        ports, type = QueryValueEx(self.prolific_path, 'Count')
        if ports is 0:
            return []
        coms = [0] * ports
        ENUM = 'SYSTEM\\CurrentControlSet\\Enum\\'
        try:
            i = 0
            j = 0
            while 1:
                name, string, type = EnumValue(self.prolific_path, i)
                if type == 1: # 1 is for 'REG_SZ', 'A null-terminated string'
                    sn = search('(?<=[\][0-9]&)\w+',string)
                    offset = 0
                    try:
                        serint = ENUM + string + '\\Device Parameters'
                        serial_path = OpenKey(HKEY_LOCAL_MACHINE,serint)
                        port, type = QueryValueEx(serial_path, 'PortName')
                        coms[j] = int(str(port)[3:]) - 1
                        j += 1
                    except WindowsError:
                        pass
                i += 1
        except WindowsError:
            pass
        return coms


    def ConnectPort(self):
        if self.serialThread is not None:
            try:
                self.serialThread.Flush()
                self.serialThread.Stop()
                self.serialThread.Close()
            except:
                pass
            self.serialThread = None
        try:
            self.serialThread = eg.SerialThread()
            self.serialThread.Open(self.port, 9600, "8N1")
            self.serialThread.SetRts()
            self.serialThread.Start()
            self.TriggerEvent(self.text.connect)
        except:
            self.serialThread = None
            eg.PrintError(
                self.text.info3 % (self.info.eventPrefix, self.port)
            )
            return


    def ConvertState(self, state):
        bits = 255
        j = 1
        for i in range(8):
            if state[i]:
                bits -= j
            j *= 2
        return bits


    def SelectBoard(self):
        self.serialThread.Write("P")
        sleep(0.05)
        bType = self.serialThread.Read(1, 1.0)
        self.serialThread.Write("Q")
        sleep(0.05)
        self.serialThread.Write("\x00")
        sleep(0.01)
        self.curState = 8*[0] if self.curState is None else self.curState
        bits = self.ConvertState(self.curState)
        self.serialThread.Write(chr(bits))
        return bType


    def DeleteBoard(self, event):
        if self.flag:
            coms = self.enumerate_ports()
            diff = set(self.coms) - set(coms)
            self.coms = coms
            if not self.port in diff:
                return
            self.TriggerEvent(self.text.disconnect)
            if self.serialThread is not None:
                try:
                    self.serialThread.Flush()
                    self.serialThread.Stop()
                    self.serialThread.Close()
                except:
                    pass
                self.serialThread = None


    def InitBoard(self, event):
        if self.flag:
            coms = self.enumerate_ports()
            diff = set(coms) - set(self.coms)
            self.coms = coms
            if not self.port in diff:
                return
            if event.payload[0].startswith(u'\\\\?\\USB#VID_067B&PID_2303#'):            
                self.ConnectPort()
                bType = self.SelectBoard()
            else:
                eg.PrintNotice(
                    self.text.info4 % (self.info.eventPrefix, self.port)
                )


    def parseArgument(self, arg):
        if not arg:
            return 0
        if isinstance(arg, int):
            return arg
        else:
            return eg.ParseString(arg)


    def SetChannel(self, ch, state):
        self.curState[ch-1] = state
        bits = self.ConvertState(self.curState)
        self.serialThread.Write(chr(bits))
        cNum = BOARDS[self.bType][1]
        cNum = int(cNum) if cNum != "" else 0
        return self.curState[:cNum]


    def SetAllChannels(self, state):
        self.curState = state[:]
        bits = self.ConvertState(self.curState)
        self.serialThread.Write(chr(bits))
        cNum = BOARDS[self.bType][1]
        cNum = int(cNum) if cNum != "" else 0
        return self.curState[:cNum]


    def Configure(
        self,
        port = 0,
        bType ='',
        initState = [0,0,0,0,0,0,0,0],
        prefix = "ICS_Relay"
    ):
        self.flag = False
        text = self.text
        panel = eg.ConfigPanel()
        panel.SetBackgroundColour(wx.WHITE)
        coms = self.enumerate_ports()
        global tmp_bType
        tmp_bType = bType
        tmp_initState = initState[:]
        choices = ["COM%i" % (com + 1) for com in coms]
        choices.sort()
        portCtrl = wx.Choice(
            panel,
            -1,
            choices = choices
        )
        portCtrl.SetStringSelection("COM%i" % (port + 1))
        bTypeCtrl = wx.StaticText(panel, -1, BOARDS[bType][0])
        ccCtrl = wx.StaticText(panel, -1, BOARDS[bType][1])
        prefixCtrl = wx.TextCtrl(panel, -1, prefix)
        panel.SetColumnFlags(1, wx.EXPAND)
        staticBox = wx.StaticBox(panel, -1, text.board)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)        
        portSizer = wx.FlexGridSizer(4, 2, 10, 9)
        staticBoxSizer.Add(portSizer,1,wx.EXPAND)
        lbl0 = wx.StaticText(panel,-1, text.prefix)
        lbl1 = wx.StaticText(panel,-1, text.port)
        lbl2 = wx.StaticText(panel,-1, text.bType)
        lbl3 = wx.StaticText(panel,-1, text.cc)
        portSizer.Add(lbl0,0,wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,30)
        portSizer.Add(prefixCtrl)
        portSizer.Add(lbl1,0,wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,30)
        portSizer.Add(portCtrl)
        portSizer.Add(lbl2,0,wx.RIGHT,30)
        portSizer.Add(bTypeCtrl)
        portSizer.Add(lbl3,0,wx.RIGHT,30)
        portSizer.Add(ccCtrl)
        staticBox2 = wx.StaticBox(panel, -1, text.initState)
        staticBoxSizer2 = wx.StaticBoxSizer(staticBox2, wx.VERTICAL)        
        stateSizer = wx.FlexGridSizer(2, 9, 4, 9)
        staticBoxSizer2.Add(stateSizer,1,wx.EXPAND)
        panel.sizer.Add(staticBoxSizer,0,wx.EXPAND)
        panel.sizer.Add(staticBoxSizer2,0,wx.EXPAND|wx.TOP,10)
        stateSizer.Add(wx.StaticText(panel,-1, text.channel))

        def onPort(evt):
            strng = evt.GetString()
            self.port = int(strng[3:]) - 1
            self.ConnectPort()
            global tmp_bType
            tmp_bType = self.SelectBoard()
            bTypeCtrl.SetLabel(BOARDS[tmp_bType][0])
            ccCtrl.SetLabel(BOARDS[tmp_bType][1])
            panel.sizer.Layout()
            if tmp_bType == "":
                eg.MessageBox(text.message, text.idProblem, parent = panel)
            SetDynSizer(tmp_initState, tmp_bType)
            evt.Skip()

        portCtrl.Bind(wx.EVT_CHOICE, onPort)
        buttons = (
            wx.NewIdRef(),wx.NewIdRef(),wx.NewIdRef(),wx.NewIdRef(),
            wx.NewIdRef(),wx.NewIdRef(),wx.NewIdRef(),wx.NewIdRef()
        )
        images = [None, None]
        sbuf = StringIO(b64decode(RED))
        wximg = wx.Image(sbuf)
        images[0] = wx.Bitmap(wximg)        
        sbuf = StringIO(b64decode(GREEN))
        wximg = wx.Image(sbuf)
        images[1] = wx.Bitmap(wximg)        

        def OnStatusChange(evt):
            panel.SetIsDirty()
            evt.Skip()
        

        def SetDynSizer(state, bType):
            cNum = BOARDS[bType][1]
            cNum = int(cNum) if cNum != "" else 0
            stateSizer.Clear(True)
            lbl4 = wx.StaticText(panel,-1, text.channel)
            lbl5 = wx.StaticText(panel,-1, text.state)
            stateSizer.Add(lbl4, 0, wx.TOP, 8)
            for i in range(8):
                if i < cNum:
                    stateSizer.Add(
                        wx.StaticText(panel, -1, str(i + 1)),
                        0,
                        wx.ALIGN_CENTER|wx.TOP,
                        8
                    )
                else:
                    stateSizer.Add((24,24))
            stateSizer.Add(lbl5,0,wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,30)
            eg.EqualizeWidths([lbl0, lbl1, lbl2, lbl3, lbl4, lbl5])
            for i in range(8):
                if i < cNum:
                    ctrl = StatusBitmap(
                        panel,
                        buttons[i], 
                        stateValues = images,
                        tooltips = text.states[:2],
                        state = state[i]
                    )
                    stateSizer.Add(ctrl,0,wx.ALIGN_CENTER)
                    ctrl.Bind(EVT_STATUS_BITMAP_CHANGED, OnStatusChange) 
                else:
                    stateSizer.Add((24,24))
            panel.sizer.Layout()
        SetDynSizer(tmp_initState, tmp_bType)


        def OnDestroy(evt):
            if evt.Window == panel: # it may even be MessageBox !
                self.flag = True
            evt.Skip()
        panel.Bind(wx.EVT_WINDOW_DESTROY, OnDestroy)

        while panel.Affirmed():
            port = portCtrl.GetStringSelection()
            port = int(port[3:]) - 1 if port != "" else 0
            cNum = BOARDS[tmp_bType][1]
            cNum = int(cNum) if cNum != "" else 0
            tmp_initState = 8 * [0]
            for i in range(cNum):
                ctrl = wx.FindWindowById(buttons[i])
                tmp_initState[i] = ctrl.GetValue()
            panel.SetResult(
                port,
                tmp_bType,
                tmp_initState,
                prefixCtrl.GetValue()
            )
#===============================================================================

class SetChannel(eg.ActionBase):

    class text:
        channel = "Channel:"

    def __call__(self, ch=1):
        ch = self.plugin.parseArgument(ch)
        return self.plugin.SetChannel(ch, self.value)


    def Configure(self, ch=1):
        text = self.text
        panel = eg.ConfigPanel(self) 
        label = wx.StaticText(panel, -1, self.text.channel)
        maxch = BOARDS[self.plugin.bType][1]
        maxch = int(maxch) if maxch != "" else 0
        limit = maxch if maxch else 1
        ctrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            ch,
            min = 1,
            max = limit
        ) 
        label.Enable(maxch > 0)
        ctrl.Enable(maxch > 0)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(ctrl)
        panel.sizer.Add(sizer,0,wx.ALL,10)

        while panel.Affirmed():
            panel.SetResult(ctrl.GetValue(),)
#===============================================================================

class SetChannelTemp(eg.ActionBase):

    class text:
        channel = "Channel:"
        time = "Time [s]:"
        suffix = "Event suffix:"

    def __call__(self, ch=1,tm=0,suffix="TimeElapsed"):
        ch = self.plugin.parseArgument(ch)
        tm = self.plugin.parseArgument(tm)
        suffix = eg.ParseString(suffix)
        eg.scheduler.AddShortTask(tm,self.TimeElapsed,ch,suffix)
        return self.plugin.SetChannel(ch, self.value)


    def GetLabel(self, ch, tm, suffix):
        return "%s: %s, %s, %s" % (self.name, ch, tm, suffix)


    def TimeElapsed(self, ch, suffix):
        res = self.plugin.SetChannel(ch, (1,0)[self.value])
        self.plugin.TriggerEvent(suffix, payload = res)
        

    def Configure(self, ch=1,tm=0,suffix="TimeElapsed"):
        text = self.text
        panel = eg.ConfigPanel(self) 
        maxch = BOARDS[self.plugin.bType][1]
        maxch = int(maxch) if maxch != "" else 0
        chLabel = wx.StaticText(panel, -1, self.text.channel)
        limit = maxch if maxch else 1
        chCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            ch,
            min = 1,
            max = limit
        ) 
        chLabel.Enable(maxch > 0)
        chCtrl.Enable(maxch > 0)
        tmLabel = wx.StaticText(panel, -1, self.text.time)
        tmCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            tm,
            min = 1,
            max = 999999
        ) 
        suffLabel = wx.StaticText(panel, -1, self.text.suffix)
        suffCtrl = wx.TextCtrl(panel, -1, suffix)
        if not maxch:
            chLabel.Enable(False)
            chCtrl.Enable(False)
        sizer = wx.FlexGridSizer(3, 2, 10, 9)
        sizer.AddGrowableCol(1)
        sizer.Add(chLabel, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(chCtrl)
        sizer.Add(tmLabel, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(tmCtrl)
        sizer.Add(suffLabel, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(suffCtrl, 1, wx.EXPAND)
        panel.sizer.Add(sizer, 1, wx.ALL|wx.EXPAND, 10)

        while panel.Affirmed():
            panel.SetResult(
                chCtrl.GetValue(),
                tmCtrl.GetValue(),
                suffCtrl.GetValue()
            )
#===============================================================================

class SetAllChannels(eg.ActionBase):

    def __call__(self):
        return self.plugin.SetAllChannels(8 * [self.value])
#===============================================================================

class SetInitialState(eg.ActionBase):

    def __call__(self):
        return self.plugin.SetAllChannels(self.plugin.initState)
#===============================================================================

class GetCurrentState(eg.ActionBase):

    def __call__(self):
        cNum = BOARDS[self.plugin.bType][1]
        cNum = int(cNum) if cNum != "" else 0
        return self.plugin.curState[:cNum]
#===============================================================================

class SetNewState(eg.ActionBase):

    def __call__(self, newState = 8 * [0]):
        tmp_newState = newState[:]
        for i in range(8):
            if tmp_newState[i] == 2:
                tmp_newState[i] = self.plugin.curState[i]
        return self.plugin.SetAllChannels(tmp_newState)


    def GetLabel(self, newState):
        trItem = self.plugin.info.treeItem
        bType = list(trItem.GetArguments())[1]
        cNum = BOARDS[bType][1]
        cNum = int(cNum) if cNum != "" else 0
        return "%s: %s" % (self.name, repr(newState[:cNum]))


    def Configure(self, newState = 8 * [0]):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        panel.SetBackgroundColour(wx.WHITE)
        tmp_newState = newState[:]
        staticBox2 = wx.StaticBox(panel, -1, text.newState)
        staticBoxSizer2 = wx.StaticBoxSizer(staticBox2, wx.VERTICAL)        
        stateSizer = wx.FlexGridSizer(2, 9, 4, 10)
        staticBoxSizer2.Add(stateSizer,1,wx.EXPAND)
        panel.sizer.Add(staticBoxSizer2,0,wx.EXPAND|wx.TOP,10)
        stateSizer.Add(wx.StaticText(panel,-1, text.channel))
        buttons = (
            wx.NewIdRef(),wx.NewIdRef(),wx.NewIdRef(),wx.NewIdRef(),
            wx.NewIdRef(),wx.NewIdRef(),wx.NewIdRef(),wx.NewIdRef()
        )
        images = [None, None, None]
        sbuf = StringIO(b64decode(RED))
        wximg = wx.Image(sbuf)
        images[0] = wx.Bitmap(wximg)        
        sbuf = StringIO(b64decode(GREEN))
        wximg = wx.Image(sbuf)
        images[1] = wx.Bitmap(wximg)        
        sbuf = StringIO(b64decode(GRAY))
        wximg = wx.Image(sbuf)
        images[2] = wx.Bitmap(wximg)

        def OnStatusChange(evt):
            panel.SetIsDirty()
            evt.Skip()        

        def SetDynSizer(state, bType):
            cNum = BOARDS[bType][1]
            cNum = int(cNum) if cNum != "" else 0
            stateSizer.Clear(True)
            lbl1 = wx.StaticText(panel,-1, text.channel)
            lbl2 = wx.StaticText(panel,-1, text.state)
            stateSizer.Add(lbl1,0,wx.TOP,8)
            for i in range(8):
                if i < cNum:
                    stateSizer.Add(
                        wx.StaticText(panel,-1, str(i+1)),
                        0,
                        wx.ALIGN_CENTER|wx.TOP,
                        8
                    )
                else:
                    stateSizer.Add((24,24))
            stateSizer.Add(lbl2, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 50)
            for i in range(8):
                if i < cNum:
                    ctrl = StatusBitmap(
                        panel,
                        buttons[i], 
                        stateValues = images,
                        tooltips = text.states,
                        state = state[i]
                    )
                    ctrl.Bind(EVT_STATUS_BITMAP_CHANGED, OnStatusChange)
                    stateSizer.Add(ctrl,0,wx.ALIGN_CENTER)
                else:
                    stateSizer.Add((24,24))
            panel.sizer.Layout()
        SetDynSizer(tmp_newState, self.plugin.bType)

        while panel.Affirmed():
            cNum = BOARDS[self.plugin.bType][1]
            cNum = int(cNum) if cNum != "" else 0
            tmp_newState = 8 * [0]
            for i in range(cNum):
                ctrl = wx.FindWindowById(buttons[i])
                tmp_newState[i] = ctrl.GetValue()
            panel.SetResult(
                tmp_newState,
            )
#===============================================================================

ACTIONS = (
    (
        SetChannel,
        "TurnOn",
        "Turn relay ON",
        "Turns relay ON.",
        1
    ),
    (
        SetChannel,
        "TurnOff",
        "Turn relay OFF",
        "Turns relay OFF.",
        0
    ),
    (
        SetChannelTemp,
        "TurnOnTemp",
        "Turn relay ON for some time",
        "Turns relay ON for some time.",
        1
    ),
    (
        SetChannelTemp,
        "TurnOffTemp",
        "Turn relay OFF for some time",
        "Turns relay OFF for some time.",
        0
    ),
    (
        SetAllChannels,
        "TurnAllOn",
        "Turn all relays ON",
        "Turns all relays ON.",
        1
    ),
    (
        SetAllChannels,
        "TurnAllOff",
        "Turn all relays OFF",
        "Turns all relays OFF.",
        0
    ),
    (
        SetInitialState,
        "SetInitial",
        "Set initial state",
        "Sets initial state.",
        None
    ),
    (
        GetCurrentState,
        "GetCurState",
        "Get current state",
        "Gets current state.",
        None
    ),
    (
        SetNewState,
        "SetNewState",
        "Set a new state",
        "Sets a new state.",
        None
    )
)
#===============================================================================

# -*- coding: utf-8 -*-
version = "0.0"

# Plugins/HID_Relay/__init__.py
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
# 0.0 by Pako 2015-09-20 08:20 UTC+1
#     - initial version
# ===============================================================================

eg.RegisterPlugin(
    name="HID_Relay",
    author="Pako",
    guid="{83E5DD2C-C99A-4279-B72B-907A7707F401}",
    version=version,
    kind="external",
    createMacrosOnAdd=True,
    canMultiLoad=True,
    description='''<rst>
Plugin to control USB relay "For Smart Home" (eBay phrase).

.. image:: picture.png

Some of the information comes from the site `Driver-less USB relays 
(HID interface)`__.

| This series of relay boards, it is far superior to the ICS series.
| The great advantage is that it uses the HID technology, 
| so no need to install any driver in windows system.
| Compared to ICS series, we can even read the current status of each channel.

| Unfortunately, even these devices are not quite perfect.
| They have one major flaw:
| **Windows (XP, 7, 8, 10) fails to recognize these devices on some PCs** 
| **(complains that device descriptors cannot be read).**
| *Possible workaround:*
| When connected thru a USB hub, these devices are properly detected.
| *I have experienced that in some cases, this workaround is not working.*

Plugin version: %s

__ http://vusb.wikidot.com/project:driver-less-usb-relays-hid-interface
''' % version,
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAC/VBMVEXN4sfd5dO64sKr"
        "6suW7tOA897//wBKwsFMwb/U4su56ciI8dk3Tk7Z48+06clCmZkzMzPV4syi7M4zOTnj"
        "6No8b2+L8dhIwcE3TU3Q4sjc5dKE89zO4si+4cKk683k6Nvf5tVCl5dIwMBGtLQ+f38z"
        "NzdM29tFsbGy07Y0Pz9Dn59K0dFL1dVFq6tAiopEp6dK0NA9dXUzNjY7a2tHuLg1QUE0"
        "PDxFra1Ajo4/gYFJyclIvLw2TEw1Q0NN4OBIv788dHRBk5NClpY/g4NBkpI7ZWU3U1Mz"
        "NDRM3d1L0NBJzMw3UVE9e3s7aWlAkJBAi4tJx8c3T082R0c6Y2NN3985W1s4VFRM2Ng0"
        "PT08c3NCmJgzNTVEpqZEo6NL1tY0OjpAjIxCm5s4XFxHvb0+hIQ5X180Pj4/iIg5Xl5G"
        "s7NDnp4+fX1Hubk1RkY1RUU7ampDoqJL2dk4Wlo4WVlBj49JyMhCmpo2SkpL1NRL19dE"
        "qKg9cXE7bGwzODg6XV1M3t45ZGQ0Ozs7cHBGsLBN3NxJxMQ6YmJL0dE/hoZL09NEoaE4"
        "V1dM19c2SEg1REQ4WFhAiYlAhYU6ZmY6Z2dKycm33r93m4k8REI+REGAloTK3sPR0dGU"
        "lJRqampTU1M+Pj4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADkXbWhAAAAAXRS"
        "TlMAQObYZgAAAPBJREFUOMuVk7EKAjEMhnsiGc+Ag8MJItzkLvgA4iRuDo5OLj6Ab+Ci"
        "k4P4tl6b3iVpWsHAcbn83zVtkzjHVgPApHvAZQ2CIdK7IHc6zsibZ3UPYO8LuZI6Ti3R"
        "R5YBGJaAVJebJNLq/wJg9BKwQRYUAHS/4XOnANiSFzPw6X4AOgW05FVDjVYJEH8ZFwBe"
        "MgO0dOGXBDiJ43V2jJlGTmWMwBVEvUShD5LkgspWwFuiCwDumHSDt9p0g82gibUGmgDM"
        "c+VWPceBp8/xMD3p1B54jUVubLydjc5zF2yfHT4fe3GKJj+9PVC7glVvxI8OfQErYSLs"
        "Ayx1rAAAAABJRU5ErkJggg=="
    ),
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=7426"
)
# ===============================================================================

from base64 import b64decode
from os.path import abspath, split
from StringIO import StringIO
from sys import path as syspath

import wx
from wx.lib.statbmp import GenStaticBitmap

import eg

mod_pth = abspath(split(__file__)[0])
syspath.append(mod_pth + "\\pywinusb")
import pywinusb.hid as hid

# ===============================================================================

myEVT_STATUS_BITMAP_CHANGED = wx.NewEventType()
EVT_STATUS_BITMAP_CHANGED = wx.PyEventBinder(myEVT_STATUS_BITMAP_CHANGED, 1)

myEVT_BITMAP_MOUSE_IN = wx.NewEventType()
EVT_BITMAP_MOUSE_IN = wx.PyEventBinder(myEVT_BITMAP_MOUSE_IN, 1)

myEVT_BITMAP_MOUSE_OUT = wx.NewEventType()
EVT_BITMAP_MOUSE_OUT = wx.PyEventBinder(myEVT_BITMAP_MOUSE_OUT, 1)

RED = (
    "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"
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

SET_ON = 0xFF
SET_ALL_ON = 0xFE
SET_OFF = 0xFD
SET_ALL_OFF = 0xFC


# ===============================================================================

class StatusBitmapEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self._state = -1

    def GetState(self):
        return self._state


# ===============================================================================

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
        # ===============================================================================


class Text:
    board = "Board"
    ser_id = "Serial id:"
    cNum = "Board type:"
    initState = "Required initial state"
    newState = "New state"
    channel = "Channel:"
    state = "State:"
    states = ("OFF", "ON", "No change")
    prefix = "Name and event prefix:"
    message = 'Unexpected board type "%s".\nUnable to get the number of channels.'
    header = "%s: Warning"
    failed = "%s: Relay settings failed."
    connect = "Connected"
    disconnect = "Disconnected"


# ===============================================================================

def get_serial(res):
    res = "".join([chr(i) for i in res][1:6])
    return res


# ===============================================================================
class HID_Relay(eg.RawReceiverPlugin):
    text = Text
    initState = None
    ser_ids = {}
    flag = True
    cNum = 0
    opened = False

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddActionsFromList(ACTIONS)
        self.serialThread = None

    def __start__(
        self,
        ser_id="",
        cNum=0,
        initState=[0, 0, 0, 0, 0, 0, 0, 0],
        prefix="HID_Relay"
    ):
        ser_ids = self.Enumerate_rels()
        self.ser_ids = ser_ids
        self.ser_id = ser_id
        self.cNum = cNum
        self.initState = initState[:]
        self.info.eventPrefix = prefix

        if self.ser_id in self.ser_ids:
            rel = self.ser_ids[self.ser_id]
            try:
                if not rel.is_opened():
                    rel.open()
                self.opened = True
                self.SetAllChannels(self.initState)
            except:
                # raise
                eg.PrintError(self.text.failed % self.info.eventPrefix)
                self.opened = True
        eg.Bind("System.DeviceAttached", self.InitBoard)
        eg.Bind("System.DeviceRemoved", self.DeleteBoard)

    def __stop__(self):
        eg.Unbind("System.DeviceAttached", self.InitBoard)
        eg.Unbind("System.DeviceRemoved", self.DeleteBoard)
        if self.ser_id in self.ser_ids:
            rel = self.ser_ids[self.ser_id]
            if rel and rel.is_opened():
                rel.close()

    def get_state(self, rel):
        dev = self.ser_ids[self.ser_id]
        if not dev.is_opened():
            dev.open()
        rep = dev.find_feature_reports()[0]
        state = rep.get()[-1]
        mask = 1 << (rel - 1)
        return (state & mask) / mask

    def get_state_all(self):
        state = []
        for i in range(self.cNum):
            state.append(self.get_state(i + 1))
        return state

    def Enumerate_rels(self):
        rels = hid.HidDeviceFilter(vendor_id=0x16c0, product_id=0x05df).get_devices()
        ser_ids = {}
        for rel in rels:
            if not rel.is_opened():
                rel.open()
            rep = rel.find_feature_reports()[0]
            if rep:
                res = rep.get()
                ser = get_serial(res)
                ser_ids[ser] = rel
            rel.close()
        return ser_ids

    def DeleteBoard(self, event):
        if self.flag:
            if event.payload[0].startswith(u'\\\\?\\HID#VID_16C0&PID_05DF#'):
                ser_ids = self.Enumerate_rels()
                diff = set(self.ser_ids.iterkeys()) - set(ser_ids.iterkeys())
                self.ser_ids = ser_ids
                if self.ser_id in tuple(diff):
                    self.TriggerEvent(self.text.disconnect)

    def InitBoard(self, event):
        if self.flag:
            if event.payload[0].startswith(u'\\\\?\\HID#VID_16C0&PID_05DF#'):
                ser_ids = self.Enumerate_rels()
                diff = set(ser_ids.iterkeys()) - set(self.ser_ids.iterkeys())
                self.ser_ids = ser_ids
                if not self.ser_id in tuple(diff):
                    return
                self.TriggerEvent(self.text.connect)
                rel = self.ser_ids[self.ser_id]
                if not rel.is_opened():
                    rel.open()
                self.opened = True
                self.SetAllChannels(self.initState)

    def parseArgument(self, arg):
        if not arg:
            return 0
        if isinstance(arg, int):
            return arg
        else:
            return eg.ParseString(arg)

    def SetChannel(self, rel, val):
        dev = self.ser_ids[self.ser_id]
        if not dev.is_opened():
            dev.open()
        rep = dev.find_feature_reports()[0]
        res = rep.send([0, (SET_OFF, SET_ON)[val], rel, 0, 0, 0, 0, 0, 0])
        if res:
            return self.get_state(rel)

    def set_all(self, val):
        rel = self.ser_ids[self.ser_id]
        if not rel.is_opened():
            rel.open()
        rep = rel.find_feature_reports()[0]
        return rep.send([0, (SET_ALL_OFF, SET_ALL_ON)[val], 0, 0, 0, 0, 0, 0, 0])

    def SetAllChannels(self, state):
        cNum = self.cNum
        if state[:self.cNum] == [0] * cNum:
            self.set_all(0)
        elif state[:self.cNum] == [1] * cNum:
            self.set_all(1)
        else:
            for i, val in enumerate(state[:self.cNum]):
                if val != 2:
                    self.SetChannel(i + 1, val)
        return self.get_state_all()

    def Configure(
        self,
        ser_id="",
        cNum=0,
        initState=[0, 0, 0, 0, 0, 0, 0, 0],
        prefix="HID_Relay"
    ):
        self.flag = False
        text = self.text
        panel = eg.ConfigPanel()
        panel.SetBackgroundColour(wx.WHITE)
        ser_ids = self.Enumerate_rels()
        self.ser_ids = ser_ids
        global tmp_cNum
        tmp_cNum = cNum
        tmp_initState = initState[:]
        choices = list(ser_ids.iterkeys())
        choices.sort()
        ser_idCtrl = wx.Choice(
            panel,
            -1,
            choices=choices
        )
        pname = ser_ids[ser_id].product_name if ser_id in choices else ""
        ser_idCtrl.SetStringSelection(ser_id)
        cNumCtrl = wx.StaticText(panel, -1, pname)
        prefixCtrl = wx.TextCtrl(panel, -1, prefix)
        panel.SetColumnFlags(1, wx.EXPAND)
        staticBox = wx.StaticBox(panel, -1, text.board)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        ser_idSizer = wx.FlexGridSizer(3, 2, 10, 9)
        staticBoxSizer.Add(ser_idSizer, 1, wx.EXPAND)
        lbl0 = wx.StaticText(panel, -1, text.prefix)
        lbl1 = wx.StaticText(panel, -1, text.ser_id)
        lbl2 = wx.StaticText(panel, -1, text.cNum)
        ser_idSizer.Add(lbl0, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 30)
        ser_idSizer.Add(prefixCtrl)
        ser_idSizer.Add(lbl1, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 30)
        ser_idSizer.Add(ser_idCtrl)
        ser_idSizer.Add(lbl2, 0, wx.RIGHT, 30)
        ser_idSizer.Add(cNumCtrl)
        staticBox2 = wx.StaticBox(panel, -1, text.initState)
        staticBoxSizer2 = wx.StaticBoxSizer(staticBox2, wx.VERTICAL)
        stateSizer = wx.FlexGridSizer(2, 9, 4, 9)
        staticBoxSizer2.Add(stateSizer, 1, wx.EXPAND)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        panel.sizer.Add(staticBoxSizer2, 0, wx.EXPAND | wx.TOP, 10)
        stateSizer.Add(wx.StaticText(panel, -1, text.channel))

        def onser_id(evt):
            old_id = self.ser_id if hasattr(self, "ser_id") else None
            self.ser_id = str(evt.GetString())
            if old_id != self.ser_id:
                if old_id in self.ser_ids:
                    old_rel = self.ser_ids[old_id]
                    if old_rel.is_opened():
                        old_rel.close()
            rel = self.ser_ids[self.ser_id]
            if not rel.is_opened():
                rel.open()
            global tmp_cNum
            tmp_cNum = 0
            pname = rel.product_name
            try:
                tmp_cNum = int(pname[-1])
                cNumCtrl.SetLabel(pname)
                panel.sizer.Layout()
            except:
                eg.MessageBox(
                    text.message % pname,
                    self.text.header % self.info.eventPrefix,
                    parent=panel
                )
            SetDynSizer(tmp_initState, tmp_cNum)
            evt.Skip()

        ser_idCtrl.Bind(wx.EVT_CHOICE, onser_id)
        buttons = (
            wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef(),
            wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef()
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

        def SetDynSizer(state, cNum):
            stateSizer.Clear(True)
            lbl4 = wx.StaticText(panel, -1, text.channel)
            lbl5 = wx.StaticText(panel, -1, text.state)
            stateSizer.Add(lbl4, 0, wx.TOP, 8)
            for i in range(8):
                if i < cNum:
                    stateSizer.Add(
                        wx.StaticText(panel, -1, str(i + 1)),
                        0,
                        wx.ALIGN_CENTER | wx.TOP,
                        8
                    )
                else:
                    stateSizer.Add((24, 24))
            stateSizer.Add(lbl5, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 30)
            eg.EqualizeWidths([lbl0, lbl1, lbl2, lbl4, lbl5])
            for i in range(8):
                if i < cNum:
                    ctrl = StatusBitmap(
                        panel,
                        buttons[i],
                        stateValues=images,
                        tooltips=text.states,
                        state=state[i]
                    )
                    stateSizer.Add(ctrl, 0, wx.ALIGN_CENTER)
                    ctrl.Bind(EVT_STATUS_BITMAP_CHANGED, OnStatusChange)
                else:
                    stateSizer.Add((24, 24))
            panel.sizer.Layout()

        SetDynSizer(tmp_initState, tmp_cNum)

        def OnDestroy(evt):
            if evt.Window == panel:  # it may even be MessageBox !
                self.flag = True
            evt.Skip()

        panel.Bind(wx.EVT_WINDOW_DESTROY, OnDestroy)

        while panel.Affirmed():
            ser_id = ser_idCtrl.GetStringSelection()
            tmp_initState = 8 * [0]
            for i in range(tmp_cNum):
                ctrl = wx.FindWindowById(buttons[i])
                tmp_initState[i] = ctrl.GetValue()
            panel.SetResult(
                ser_id,
                tmp_cNum,
                tmp_initState,
                prefixCtrl.GetValue()
            )


# ===============================================================================

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
        maxch = self.plugin.cNum
        limit = maxch if maxch else 1
        ctrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            ch,
            min=1,
            max=limit
        )
        label.Enable(maxch > 0)
        ctrl.Enable(maxch > 0)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(ctrl)
        panel.sizer.Add(sizer, 0, wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(ctrl.GetValue(), )


# ===============================================================================

class SetChannelTemp(eg.ActionBase):
    class text:
        channel = "Channel:"
        time = "Time [s]:"
        suffix = "Event suffix:"

    def __call__(self, ch=1, tm=0, suffix="TimeElapsed"):
        ch = self.plugin.parseArgument(ch)
        tm = self.plugin.parseArgument(tm)
        suffix = eg.ParseString(suffix)
        eg.scheduler.AddShortTask(tm, self.TimeElapsed, ch, suffix)
        return self.plugin.SetChannel(ch, self.value)

    def GetLabel(self, ch, tm, suffix):
        return "%s: %s, %s, %s" % (self.name, ch, tm, suffix)

    def TimeElapsed(self, ch, suffix):
        res = self.plugin.SetChannel(ch, (1, 0)[self.value])
        self.plugin.TriggerEvent(suffix, payload=res)

    def Configure(self, ch=1, tm=0, suffix="TimeElapsed"):
        text = self.text
        panel = eg.ConfigPanel(self)
        maxch = self.plugin.cNum
        chLabel = wx.StaticText(panel, -1, self.text.channel)
        limit = maxch if maxch else 1
        chCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            ch,
            min=1,
            max=limit
        )
        chLabel.Enable(maxch > 0)
        chCtrl.Enable(maxch > 0)
        tmLabel = wx.StaticText(panel, -1, self.text.time)
        tmCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            tm,
            min=1,
            max=999999
        )
        suffLabel = wx.StaticText(panel, -1, self.text.suffix)
        suffCtrl = wx.TextCtrl(panel, -1, suffix)
        if not maxch:
            chLabel.Enable(False)
            chCtrl.Enable(False)
        sizer = wx.FlexGridSizer(3, 2, 10, 9)
        sizer.AddGrowableCol(1)
        sizer.Add(chLabel, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(chCtrl)
        sizer.Add(tmLabel, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(tmCtrl)
        sizer.Add(suffLabel, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(suffCtrl, 1, wx.EXPAND)
        panel.sizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 10)

        while panel.Affirmed():
            panel.SetResult(
                chCtrl.GetValue(),
                tmCtrl.GetValue(),
                suffCtrl.GetValue()
            )


# ===============================================================================

class SetAllChannels(eg.ActionBase):

    def __call__(self):
        return self.plugin.SetAllChannels(8 * [self.value])


# ===============================================================================

class SetInitialState(eg.ActionBase):

    def __call__(self):
        return self.plugin.SetAllChannels(self.plugin.initState)


# ===============================================================================

class GetCurrentStateAll(eg.ActionBase):

    def __call__(self):
        return self.plugin.get_state_all()


# ===============================================================================

class GetCurrentStateOne(eg.ActionBase):
    class text:
        channel = "Channel:"

    def __call__(self, ch=1):
        state = self.plugin.get_state_all()
        return state[ch - 1]

    def Configure(self, ch=1):
        text = self.text
        panel = eg.ConfigPanel(self)
        label = wx.StaticText(panel, -1, self.text.channel)
        maxch = self.plugin.cNum
        limit = maxch if maxch else 1
        ctrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            ch,
            min=1,
            max=limit
        )
        label.Enable(maxch > 0)
        ctrl.Enable(maxch > 0)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
        sizer.Add(ctrl)
        panel.sizer.Add(sizer, 0, wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(ctrl.GetValue(), )


# ===============================================================================

class SetNewState(eg.ActionBase):

    def __call__(self, newState=8 * [0]):
        return self.plugin.SetAllChannels(newState)

    def GetLabel(self, newState):
        trItem = self.plugin.info.treeItem
        cNum = list(trItem.GetArguments())[1]
        return "%s: %s" % (self.name, repr(newState[:cNum]))

    def Configure(self, newState=8 * [0]):
        text = self.plugin.text
        panel = eg.ConfigPanel()
        panel.SetBackgroundColour(wx.WHITE)
        tmp_newState = newState[:]
        staticBox2 = wx.StaticBox(panel, -1, text.newState)
        staticBoxSizer2 = wx.StaticBoxSizer(staticBox2, wx.VERTICAL)
        stateSizer = wx.FlexGridSizer(2, 9, 4, 10)
        staticBoxSizer2.Add(stateSizer, 1, wx.EXPAND)
        panel.sizer.Add(staticBoxSizer2, 0, wx.EXPAND | wx.TOP, 10)
        stateSizer.Add(wx.StaticText(panel, -1, text.channel))
        buttons = (
            wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef(),
            wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef(), wx.NewIdRef()
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

        def SetDynSizer(state, cNum):
            stateSizer.Clear(True)
            lbl1 = wx.StaticText(panel, -1, text.channel)
            lbl2 = wx.StaticText(panel, -1, text.state)
            stateSizer.Add(lbl1, 0, wx.TOP, 8)
            for i in range(8):
                if i < cNum:
                    stateSizer.Add(
                        wx.StaticText(panel, -1, str(i + 1)),
                        0,
                        wx.ALIGN_CENTER | wx.TOP,
                        8
                    )
                else:
                    stateSizer.Add((24, 24))
            stateSizer.Add(lbl2, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 50)
            for i in range(8):
                if i < cNum:
                    ctrl = StatusBitmap(
                        panel,
                        buttons[i],
                        stateValues=images,
                        tooltips=text.states,
                        state=state[i]
                    )
                    ctrl.Bind(EVT_STATUS_BITMAP_CHANGED, OnStatusChange)
                    stateSizer.Add(ctrl, 0, wx.ALIGN_CENTER)
                else:
                    stateSizer.Add((24, 24))
            panel.sizer.Layout()

        SetDynSizer(tmp_newState, self.plugin.cNum)

        while panel.Affirmed():
            cNum = self.plugin.cNum
            tmp_newState = 8 * [0]
            for i in range(cNum):
                ctrl = wx.FindWindowById(buttons[i])
                tmp_newState[i] = ctrl.GetValue()
            panel.SetResult(
                tmp_newState,
            )


# ===============================================================================

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
        GetCurrentStateAll,
        "GetCurrentStateAll",
        "Get current state (all channels)",
        "Gets current state (all channels).",
        None
    ),
    (
        GetCurrentStateOne,
        "GetCurrentStateOne",
        "Get current state (one channel)",
        "Gets current state (one channel).",
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
# ===============================================================================

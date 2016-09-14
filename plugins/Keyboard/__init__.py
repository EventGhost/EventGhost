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

"""<rst>
This plugin generates events on keypresses (hotkeys).

**Notice:** If such a keyboard event is assigned to a macro, the plugin will
block the key, so Windows or another application will not see it anymore. This
is needed to permit remapping of keys as otherwise the old key would reach the
target in conjunction of another action you might want to do and this is
mostly not what you intend.

But this blocking only happens, if a macro would actually execute in
succession of the event. So if the macro or any of its parents is disabled,
the keypress will pass through.
"""

import wx

# Local imports
import eg
from eg import HasActiveHandler
from eg.cFunctions import SetKeyboardCallback

eg.RegisterPlugin(
    name = "Keyboard",
    author = (
        "Bitmonster",
        "blackwind",
    ),
    version = "1.1.1",
    kind = "remote",
    guid = "{59CBD10F-C1D8-4ADB-999B-9B76BA360F1F}",
    description = __doc__,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeT"
        "AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QQIDBMjdIFglwAAADV0RVh0Q29t"
        "bWVudAAoYykgMjAwNCBKYWt1YiBTdGVpbmVyCgpDcmVhdGVkIHdpdGggVGhlIEdJTVCQ"
        "2YtvAAABfklEQVQ4y6WSv0sCYRjHP2+IGlI0GOeN4WQJQnd/gENbRHtTji2NIkhTROLa"
        "EATh0hpE0OTmKNzgQUpDFEhdmosNVw3d2yB3+HYXRX3h5Xnf7/v8fh7BL1CrHywASSAN"
        "uMAAeK2Uq56IUFwFtoAH4BG4AZ6BJ+AF+KiUq55vE/sS7Ai4Ag6Bh0q5+vZTdqJWP1gD"
        "mj/oWYARwe/EgObG+qZMpxcFgBACKSVCKNUZ/t80ThsnxzEATcuIfr//bXjbtslmlxQu"
        "lZpTe2DbtqKgaRqDwUDhEokG7+8lEokGsKs6KBQKOI6Drus4jkMmk0FKGbxvb+/IZkt4"
        "nsR93WZ+kgAzvoNpY13XGY/HigSIx5Mkk7Pc390TGuO0cZQE6PV6of4EDjqdDgDD4TBS"
        "AuRyOSzLYnllOeCCEkzTxHVdTNNUDkA+n8d13ck8DYPudTecQavVUuQ02u32ZJssK7qE"
        "0WhEsVhESomUEiB09zwvWDKf9x3sX1ye7/E3nPFffAJVOqjtMbQazAAAAABJRU5ErkJg"
        "gg=="
    ),
)

class Text:
    label = "Universal modifiers"


class Keyboard(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddEvents()

    def __start__(self, universalMods = False, *dummyArgs):
        SetKeyboardCallback(self.KeyboardCallback, int(universalMods))

    def __stop__(self):
        SetKeyboardCallback(None, 0)

    def Configure(self, universalMods = True):
        panel = eg.ConfigPanel()
        universalModsCtrl = panel.CheckBox(universalMods, self.text.label)
        panel.sizer.Add(universalModsCtrl, 0, wx.ALL, 20)
        while panel.Affirmed():
            panel.SetResult(universalModsCtrl.GetValue())

    def KeyboardCallback(self, codes, num, lastNum):
        if codes == "":
            self.EndLastEvent()
        else:
            if num >= lastNum:
                self.TriggerEnduringEvent(codes)
            else:
                self.EndLastEvent()
            return HasActiveHandler("Keyboard." + codes)

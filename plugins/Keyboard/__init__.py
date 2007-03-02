#
# plugins/Keyboard/__init__.py
#
# Copyright (C) 2005 Lars-Peter Voss
#
# This file is part of EventGhost.
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import eg

class PluginInfo(eg.PluginInfo):
    name = "Keyboard"
    author = "Bitmonster"
    version = "0.0.1"
    kind = "remote"
    description = "This plugin generates events on keypresses (hotkeys)."
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
    )


from eg import HasActiveHandler
from eg.cFunctions import SetKeyboardCallback


LLKHF_EXTENDED = 0x01
LLKHF_INJECTED = 0x10
LLKHF_ALTDOWN = 0x20
LLKHF_UP = 0x80
    
    
    
class Keyboard(eg.PluginClass):
    
    def __start__(self, *args):
        SetKeyboardCallback(self.KeyboardCallback)
        
        
    def __stop__(self):
        SetKeyboardCallback(None)
        
        
    def KeyboardCallback(self, codes):
        if codes == "":
            self.EndLastEvent()
        else:
            shouldBlock = HasActiveHandler("Keyboard." + codes)
            self.TriggerEnduringEvent(codes)
            return shouldBlock
                
                    
        
        

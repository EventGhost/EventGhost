# This file is part of EventGhost.
# Copyright (C) 2010 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2010-12-07 14:07:00 +0100 (Tu, 07 Dec 2010) $
# $LastChangedRevision: r1481 $
# $LastChangedBy: Pako $

import eg

class TimeCtrl_Duration(eg.TimeCtrl):

    '''Ignore key "C", "c" and "!" (set time to "Now")'''

    def _TimeCtrl__OnSetToNow(self, evt):
        return False


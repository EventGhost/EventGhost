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
# $LastChangedDate: 2011-02-12 09:14:30 +0100 (Su, 12 Feb 2011) $
# $LastChangedRevision: r1486 $
# $LastChangedBy: Pako $

import eg

class TimeCtrl_Duration(eg.TimeCtrl):

    '''Ignore key "C", "c" and "!" (set time to "Now")'''

    def _TimeCtrl__OnSetToNow(self, evt):
        return False


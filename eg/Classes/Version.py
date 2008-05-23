# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2008-04-03 18:53:37 +0200 (Do, 03 Apr 2008) $
# $LastChangedRevision: 374 $
# $LastChangedBy: bitmonster $


class Version:
    major = 0
    minor = 3
    micro = 6
    releaselevel = 'beta'
    buildNum = 1427
    buildTime = 1211553715.95
    svnRevision = int('$LastChangedRevision: 412 $'.split()[1])
    string = "%s.%s.%s.%s" % (major, minor, micro, buildNum)

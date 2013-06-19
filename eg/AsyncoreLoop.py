# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2007-08-03 16:50:53 +0200 (Fri, 03 Aug 2007) $
# $LastChangedRevision: 205 $
# $LastChangedBy: bitmonster $

"""
Create an asyncore main loop for all asyncore dependant code.
"""
import asyncore
import socket
import thread
import atexit

dispatcher = asyncore.dispatcher()
dispatcher.create_socket(socket.AF_INET, socket.SOCK_STREAM)
thread.start_new_thread(asyncore.loop, ())
atexit.register(dispatcher.close)


def RestartAsyncore():
    """ Informs the asyncore loop of a new socket to handle. """
    global dispatcher
    
    oldDispatcher = dispatcher
    dispatcher = asyncore.dispatcher()
    dispatcher.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    oldDispatcher.close()
    

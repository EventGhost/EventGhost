# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import socket
import locale
from hashlib import md5
import wx

ENCODING = locale.getdefaultlocale()[1]


def NetworkSend(host, port, password, eventString, payload=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(2.0)
    try:
        try:
            sock.connect((host, port))
        except Exception, e:
            if e[0] == 10061:
                app = wx.PySimpleApp()
                win = wx.MessageBox(
                    '%s.\n\nMaybe the destination computer has not installed\nthe plugin "Network event receiver" ?' % e[1],
                    caption = "EventGhost - warning",
                    style=wx.ICON_EXCLAMATION|wx.OK,
                    parent = None
                )
            sock.close()
            return False
        sock.settimeout(1.0)
        # First wake up the server, for security reasons it does not
        # respond by it self it needs this string, why this odd word ?
        # well if someone is scanning ports "connect" would be very
        # obvious this one you'd never guess :-)
        sock.sendall("quintessence\n\r")

        # The server now returns a cookie, the protocol works like the
        # APOP protocol. The server gives you a cookie you add :<password>
        # calculate the md5 digest out of this and send it back
        # if the digests match you are in.
        # We do this so that none can listen in on our password exchange
        # much safer then plain text.
        cookie = sock.recv(128)

        # Trim all enters and whitespaces off
        cookie = cookie.strip()

        # Combine the token <cookie>:<password>
        token = cookie + ":" + password

        # Calculate the digest
        digest = md5(token).hexdigest()

        # add the enters
        digest = digest + "\n"

        # Send it to the server
        sock.sendall(digest)

        # Get the answer
        answer = sock.recv(512)

        # If the password was correct and you are allowed to connect
        # to the server, you'll get "accept"
        if (answer.strip() != "accept"):
            raise Exception("Server didn't send 'accept'")

        # now just pipe those commands to the server
        if (payload is not None) and (len(payload) > 0):
            for pld in payload:
                sock.sendall("payload " + pld.encode(ENCODING) + "\n")

        # send the eventstring
        sock.sendall(eventString.encode(ENCODING) + "\n")

        # tell the server that we are done nicely.
        sock.sendall("close\n")
    finally:
        sock.close()

    return True


def Main(argv):
    host, port = argv[0].split(":")
    password = argv[1]
    eventstring = argv[2]
    payloads = argv[3:]
    NetworkSend(host, int(port), password, eventstring, payloads)


if __name__ == '__main__':
    import sys
    Main(sys.argv[1:])


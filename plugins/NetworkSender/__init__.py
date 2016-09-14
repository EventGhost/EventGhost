# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
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

import eg

eg.RegisterPlugin(
    name = "Network Event Sender",
    version = "1.0",
    author = "Bitmonster",
    guid = "{B4F0DAFE-2E0B-47F3-A155-ED72C7A4E270}",
    description = (
        "Sends events to an Network Event Receiver plugin through TCP/IP."
    ),
    canMultiLoad = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/"
        "AAAACXBIWXMAAAsSAAALEgHS3X78AAAAB3RJTUUH1gIQFgQOuRVmrAAAAVRJREFUOMud"
        "kjFLw2AQhp+kMQ7+jJpCF+ni1lFEwUXq5g+wgiCCgoNUrG5Oltb2DygGYwUXwbmbg+Li"
        "IhSHhobaora2MZTGoQb5aBLFd/u4u/fuufskApQ92DWAFOEqKSHB1OzMHJoW8w1aloVR"
        "1tNhBmhajPnlQ9/Yzdk2AKEGkiQBkExOAS4wfFcqDwwGg6FBGGv++IiF5DiOZPHcnKDb"
        "+6T9YQs5iscajSd8p2jUqhhlnZfXYfeIMgaA67o/CNF4gsW1C1RVJHKcPlfFJQCaZt23"
        "geKxqqpCYnpSYL2/feIbleuTrZErjCwxEpGpNzp0ew7tjshaKOb8BsgIBnePdXAlz05g"
        "XV1ZEyplWaZQzGUVL8lx+qhv7yM78NRqtYJ30KhVucynAq8AoJ+fBhqUjLKe/uXPZzI7"
        "e/tBBumN9U1s2/at9FiBQANM0+S/UsL4/qIvHUp+5VOP+PAAAAAASUVORK5CYII="
    ),
)

import wx
import socket
from hashlib import md5


class Text:
    host = "Host:"
    port = "Port:"
    password = "Password:"
    tcpBox = "TCP/IP Settings"
    securityBox = "Security"
    class Map:
        parameterDescription = "Event name to send:"



class NetworkSender(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddAction(Map)


    def __start__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password


    def Configure(self, host="127.0.0.1", port=1024, password=""):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        passwordCtrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)

        st1 = panel.StaticText(text.host)
        st2 = panel.StaticText(text.port)
        st3 = panel.StaticText(text.password)
        eg.EqualizeWidths((st1, st2, st3))
        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (st1, hostCtrl),
            (st2, portCtrl),
        )
        securityBox = panel.BoxedGroup(
            text.securityBox,
            (st3, passwordCtrl),
        )

        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(securityBox, 0, wx.TOP|wx.EXPAND, 10)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                passwordCtrl.GetValue()
            )


    def Send(self, eventString, payload=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket = sock
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(2.0)
        try:
            sock.connect((self.host, self.port))
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
            # We do this so that no one can listen in on our password exchange
            # much safer then plain text.

            cookie = sock.recv(128)

            # Trim all enters and whitespaces off
            cookie = cookie.strip()

            # Combine the token <cookie>:<password>
            token = cookie + ":" + self.password

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
                sock.close()
                return False

            # now just pipe those commands to the server
            if (payload is not None) and (len(payload) > 0):
                for pld in payload:
                    sock.sendall(
                        "payload %s\n" % pld.encode(eg.systemEncoding)
                    )

            sock.sendall("payload withoutRelease\n")
            sock.sendall(eventString.encode(eg.systemEncoding) + "\n")

            return sock

        except:
            if eg.debugLevel:
                eg.PrintTraceback()
            sock.close()
            self.PrintError("NetworkSender failed")
            return None


    def MapUp(self, sock):
        # tell the server that we are done nicely.
        sock.sendall("close\n")
        sock.close()



class Map(eg.ActionWithStringParameter):

    def __call__(self, mesg):
        res = self.plugin.Send(eg.ParseString(mesg))
        if res:
            eg.event.AddUpFunc(self.plugin.MapUp, res)
        return res


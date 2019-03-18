"""
PySqueezeCenter: Python Wrapper for Logitech SqueezeCenter CLI
(Telnet) Interface

Copyright (C) 2010 JingleManSweep <jinglemansweep [at] gmail [dot] com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import telnetlib
import urllib

from player import Player


class Server(object):
    """
    SqueezeCenter Server
    """

    def __init__(self, hostname="localhost",
                 port=9090,
                 username="",
                 password=""):

        """
        Constructor
        """
        self.debug = False
        self.logger = None
        self.telnet = None
        self.logged_in = False
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.version = ""
        self.player_count = 0
        self.players = []

    def connect(self, update=True):
        """
        Connect
        """
        self.telnet_connect()
        self.login()
        self.get_players(update=update)

    def telnet_connect(self):
        """
        Telnet Connect
        """
        self.telnet = telnetlib.Telnet(self.hostname, self.port)

    def login(self):
        """
        Login
        """
        result = self.request("login %s %s" % (self.username, self.password))
        print result
        self.logged_in = (result == "******")

    def request(self, command_string, preserve_encoding=False):
        """
        Request
        """
        # self.logger.debug("Telnet: %s" % (command_string))
        self.telnet.write(command_string + "\n")
        response = self.telnet.read_until("\n")[:-1]
        if not preserve_encoding:
            response = urllib.unquote(response)
        start = command_string.split(" ")[0]
        if start in ["songinfo", "trackstat"]:
            result = response[len(command_string) + 1:]
        else:
            result = response[len(command_string) - 1:]
        result = result.strip()
        return result

    def get_players(self, update=True):
        """
        Get Players
        """
        self.players = []
        player_count = self.get_player_count()
        for i in range(player_count):
            player = Player(server=self, index=i - 1, update=update)
            self.players.append(player)
        return self.players

    def get_player(self, ref=None):
        """
        Get Player
        """
        ref = str(ref).lower()
        if ref:
            for player in self.players:
                player_name = str(player.name).lower()
                player_ref = str(player.ref).lower()
                if ref == player_ref or ref in player_name:
                    return player

    def get_version(self):
        """
        Get Version
        """
        self.version = self.request("version ?")
        return self.version

    def get_player_count(self):
        """
        Get Number Of Players
        """
        self.player_count = self.request("player count ?")
        print self.player_count
        return int(self.player_count)

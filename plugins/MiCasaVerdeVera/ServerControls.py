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
# This plugin is an HTTP client and Server that sends and receives MiCasaVerde UI5 and UI7 states.
# This plugin is based on the Vera plugins by Rick Naething, well kinda sorta, 

import urllib2
import threading

class SERVER(threading.Thread):

    def __init__ (self, plugin, STATIC):
        self.EVENT = threading.Event()
        self.LOADTIME = '0'
        self.DATAVERSION = '0'
        self.LUUPSTATE = -3
        self.UPSPEED = plugin.upspeed
        self.URLS = STATIC.URLS
        self.RAMPWAIT = 0
        self.RAMPEVENT = threading.Event()

        self.plugin = plugin
        super(SERVER, self).__init__()

    def send(self, **kwargs):
        try: URL = self.URL
        except: return eg.PrintError('Vera HTTP Server: Stopped')
        for key in kwargs.keys():
            kwargs[key] = str(kwargs[key])

        try: URL += kwargs.pop('server')
        except:
            if self.LUUPSTATE == -2:
                return eg.PrintError('Vera HTTP Server: Stopped, Not Connected')
            keys = sorted(kwargs.keys())
            URL += ''.join([''.join(item) for item in zip(self.URLS[keys[-1:][0]], [str(kwargs[key]) for key in keys])])
            if len(keys) < len(self.URLS[keys[-1:][0]]):
                URL += self.URLS[keys[-1:][0]][-1:][0]
                
        try: reply = urllib2.urlopen(URL)
        except Exception as err: print [str(err)]
        else: return reply.read()

    def run(self):
        self.URL = self.plugin.URL
        while self.EVENT.isSet(): pass
        self.RAMPEVENT.set()
        self.RAMPWAIT = 0

        eg.PrintNotice('Vera HTTP Server: Started')

        while not self.EVENT.isSet():
            self.UPSPEED = self.plugin.upspeed
            data = self.send(server='sdata&loadtime='+self.LOADTIME+'&dataversion='+self.DATAVERSION+'&output_format=xml')
            if data: self.LUUPSTATE, self.LOADTIME, self.DATAVERSION = self.plugin.VDL.Update(data)
            else: self.UPSPEED = 15
            self.RAMPEVENT.wait(self.RAMPWAIT)
            self.EVENT.wait(self.UPSPEED)
        eg.PrintNotice('Vera HTTP Server: Stopped')

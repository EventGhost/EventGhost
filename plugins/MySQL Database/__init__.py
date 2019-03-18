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

# 1.1.0, 2019-03-12 by topix
#   - added port selection to configuration
#   - change textfield to password-ctrl for password option


"""<rst>

**MySQL Plugin**

This plugin allows you to manage a connection and queries to a MySQL database.

This plugin requires the `MySQL Library <http://www.eventghost.net/forum/viewtopic.php?f=2&t=4005&p=22929&hilit=mysql&sid=7ee838d8dc602864924007a2801c9379#p22929>`_ to be installed into the Eventghost lib26\site-packages folder.



*Option/Setup*

Enter the MySQL Database Host address, username, password, and database name.

"""

import eg

eg.RegisterPlugin(
    name='MySQL Database',
    guid='{9998F604-C700-4F67-8CF6-A23FBA51BC2C}',
    description=__doc__,
    author='rdgerken',
    version='1.1.0',
    kind='other',
    canMultiLoad=True,
    createMacrosOnAdd=True,
    icon=(
        "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"
        "OmXsINoAAAAASUVORK5CYII="
    )
)

import MySQLdb
import threading
from types import ClassType


class Text:
    tcpBox = 'MySQL Settings'
    hostLabel = 'Host:'
    port_label = 'Port:'
    databaseLabel = 'Database:'
    userLabel = 'Username:'
    passLabel = 'Password:'


class NvAction(eg.ActionBase):
    def __call__(self):
        self.plugin.DoNoReturnCommand(self.command)


class ParAction(eg.ActionWithStringParameter):
    def __call__(self, value):
        self.plugin.DoNoReturnCommand(eg.ParseString(value))


class MySQL(eg.PluginBase):
    text = Text

    def __init__(self):
        self.host = '192.168.32.18'
        self.port = 3306
        self.database = 'RA2'
        self.dbuser = 'eg'
        self.dbpass = 'eg'
        self.isSessionRunning = False
        self.waitStr = None
        self.waitFlag = threading.Event()
        self.session = None
        self.debug = False

        group = self.AddGroup('No Return Commands')
        className = 'NoReturnExecute'
        clsAttributes = dict(name='No Return Execute', parameterDescription='SQL Statement')
        cls = ClassType(className, (ParAction,), clsAttributes)
        group.AddAction(cls)

        # self.AddEvents()

    def __start__(
        self,
        host='192.168.32.18',
        database='RA2',
        dbuser='eg',
        dbpass='eg',
        debug=False,
        port=3306,
    ):
        self.host = host
        self.port = port
        self.database = database
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.debug = debug

        if not self.isSessionRunning:
            self.session = MySQLdb.connect(
                host=self.host,
                port=port,
                user=self.dbuser,
                passwd=unicode(self.dbpass),
                db=self.database
            )
            self.isSessionRunning = True
            self.TriggerEvent('Connected')
            if self.debug:
                print 'MySQL> MySQL Connection to {}:{}@{} is Active'.format(
                    self.database,
                    self.port,
                    self.host
                )

    def __stop__(self):
        if self.isSessionRunning:
            self.session.close()
            self.TriggerEvent('Disconnected')
            if self.debug:
                print 'MySQL> MySQL Connection Closed'

    @eg.LogIt
    def DoNoReturnCommand(self, cmdstr):
        self.waitFlag.clear()
        self.waitStr = cmdstr
        if not self.isSessionRunning:
            self.session = MySQLdb.connect(self.host, self.dbuser, self.dbpass, self.database)
            self.isSessionRunning = True
            self.TriggerEvent('Connected')
            if self.debug:
                print 'MySQL> DoNoReturnCommand Connection to ' + self.database + '@' + self.host + ' is Active'
        try:
            if self.debug:
                print 'MySQL> Trying: ' + cmdstr
            cursor = self.session.cursor()
            cursor.execute(cmdstr)
            self.session.autocommit(True)
            cursor.close()
        except:
            print 'MySQL> Command Failed: ' + cmdstr
        self.waitFlag.wait(2.0)
        self.waitStr = None
        self.waitFlag.set()

    def Configure(
        self,
        host='192.168.32.18',
        database='RA2',
        dbuser='eg',
        dbpass='eg',
        debug=False,
        port=3306,
    ):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)
        databaseCtrl = panel.TextCtrl(database)
        userCtrl = panel.TextCtrl(dbuser)
        passCtrl = panel.PasswordCtrl(dbpass)
        debugCtrl = panel.CheckBox(debug, '')
        port_ctrl = panel.SmartSpinIntCtrl(value=port, min=1, max=65535)

        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (text.hostLabel, hostCtrl, text.port_label, port_ctrl),
            (text.databaseLabel, databaseCtrl),
            (text.userLabel, userCtrl),
            (text.passLabel, passCtrl),
            ('Debug', debugCtrl),
        )
        eg.EqualizeWidths(tcpBox.GetColumnItems(0))
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                databaseCtrl.GetValue(),
                userCtrl.GetValue(),
                passCtrl.GetValue(),
                debugCtrl.GetValue(),
                port_ctrl.GetValue()
            )

# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

"""
Parses the command line arguments of the program.
"""

import ctypes
import locale
import os
import sys
import threading
from os.path import abspath, dirname, join

import PythonPaths
import LoopbackSocket

ENCODING = locale.getdefaultlocale()[1]
locale.setlocale(locale.LC_ALL, '')
argvIter = (val.decode(ENCODING) for val in sys.argv)
scriptPath = argvIter.next()

mainDir = PythonPaths.mainDir

# determine the commandline parameters
import __main__  # NOQA


class args:
    allowMultiLoad = False
    configDir = None
    debugLevel = 0
    hideOnStartup = False
    install = False
    # splitext(basename(scriptPath))[0].lower() == "eventghost"
    isMain = hasattr(__main__, "isMain")
    pluginFile = None
    startupEvent = None
    startupFile = None
    translate = False
    restart = False


def restart():
    if send_message('eg.document.IsDirty') is True:
        answer = ctypes.windll.user32.MessageBoxA(
            0,
            'EventGhost cannot restart.             \n\n'
            'Configuration contains unsaved changes.\n'
            'Do you want to save before continuing? \n',
            "EventGhost Restart Error",
            3 | 40000
        )

        if answer == 2:
            sys.exit(0)
        elif answer == 7:
            send_message('eg.document.SetIsDirty', False)
        elif answer == 6:
            import wx

            answer = send_message('eg.document.Save')
            if answer == wx.ID_CANCEL:
                sys.exit(0)

    if send_message('eg.app.Exit') in (None, False):
        ctypes.windll.user32.MessageBoxA(
            0,
            'EventGhost cannot restart.             \n\n'
            'Unknown Error.                         \n',
            "EventGhost Restart Error",
            0 | 40000
        )
        sys.exit(1)

    return True


def send_message(msg, msg_args=()):

    res = LoopbackSocket.send_message('%s, %s' % (msg, str(msg_args)))

    try:
        return eval(res)
    except:
        return res


if args.isMain:
    for arg in argvIter:
        arg = arg.lower()

        if arg in ('-e', '-event'):
            eventstring = argvIter.next()
            payloads = list()
            for payload in argvIter:
                if payload.startswith('-'):
                    arg = payload
                    break
                payloads.append(payload)

            if len(payloads) == 0:
                payloads = None
            args.startupEvent = (str(eventstring), payloads)

        if arg.startswith('-debug'):
            args.debugLevel = 1
            if len(arg) > 6:
                args.debugLevel = int(arg[6:])
        elif arg in ("-n", "-netsend"):
            from Classes.NetworkSend import Main
            Main(list(argvIter))
            sys.exit(0)
        elif arg in ('-h', '-hide'):
            args.hideOnStartup = True
        elif arg == '-install':
            import compileall
            compileall.compile_dir(mainDir)
            args.install = True
        elif arg == '-uninstall':
            for root, dirs, files in os.walk(mainDir):
                for name in files:
                    if name.lower().endswith((".pyc", ".pyo")):
                        os.remove(join(root, name))
            sys.exit(0)
        elif arg in ('-m', '-multiload'):
            args.allowMultiLoad = True
        elif arg in ('-f', '-file'):
            args.startupFile = abspath(argvIter.next())
        elif arg in ('-p', '-plugin'):
            args.pluginFile = abspath(argvIter.next())
            # args.isMain = False
        elif arg == '-configdir':
            args.configDir = argvIter.next()
        elif arg == '-translate':
            args.translate = True
        elif arg == "-restart":
            args.restart = True
        else:
            path = abspath(arg)
            ext = os.path.splitext(path)[1].lower()
            if ext == ".egplugin":
                args.pluginFile = path
            elif ext in (".egtree", ".xml"):
                args.startupFile = path
    if (
        not args.allowMultiLoad and
        not args.translate and
        args.isMain # and
        # not args.pluginFile
    ):

        no_count = 0

        for command, params in (
            ('eg.document.Open', args.startupFile),
            ('eg.TriggerEvent', args.startupEvent),
            ('eg.PluginInstall.Import', args.pluginFile),
            ('eg.document.HideFrame', args.hideOnStartup)
        ):
            if params:
                if isinstance(params, bool):
                    if not send_message(command):
                        break
                else:
                    if not send_message(command, params):
                        break
            else:
                no_count += 1
        else:
            if no_count == 4:
                is_eg_running = LoopbackSocket.is_eg_running()
                retry_count = 0
                retry_event = threading.Event()

                while is_eg_running is None:
                    retry_count += 1
                    if retry_count == 5:
                        sys.stderr._displayMessage = False
                        sys.stderr.write('New Instance: check failure\n')
                        sys.exit(2348)

                    retry_event.wait(retry_count / 10.0)
                    is_eg_running = LoopbackSocket.is_eg_running()

                if is_eg_running:
                    send_message('eg.document.ShowFrame')
                    sys.exit(0)
            else:
                sys.exit(0)

        appMutex = ctypes.windll.kernel32.CreateMutexA(
            None,
            0,
            "Global\\EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B"
        )

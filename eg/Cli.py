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
import pywintypes
import sys
import wx
import argparse
from os.path import abspath, dirname, join

ENCODING = locale.getdefaultlocale()[1]
locale.setlocale(locale.LC_ALL, '')

# get program directory
mainDir = abspath(join(dirname(__file__.decode('mbcs')), ".."))

# determine the commandline parameters
import __main__  # NOQA

isMain = hasattr(__main__, "isMain")


class StdOut(object):

    def __init__(self):
        self.app = None
        self.dialog = None
        self.textCtrl = None

    def write(self, data):
        if self.app is None:
            self.app = wx.App()
            self.app.MainLoop()
            self.dialog = wx.Dialog(None)
            self.textCtrl = wx.StaticText(self.dialog, -1, data)
            self.dialog.Fit()
            self.dialog.ShowModal()

            def OnClose(evt):
                self.dialog.EndModal(wx.ID_CANCEL)
                self.app.ExitMainLoop()
                wx.WakeUpMainThread()
                sys.exit(1)

            self.dialog.Bind(wx.EVT_CLOSE, OnClose)
        else:
            text = self.textCtrl.GetLabel()
            text += '\n'
            text += data
            self.textCtrl.SetLabel(text)
            self.dialog.Fit()

    def flush(self):
        pass

    def isatty(self):
        return True


def Decoder(val):
    return val.decode(ENCODING)


def DefaultValue(val):
    val = Decoder(val)

    if val == 'True':
        return True
    elif val == 'False':
        return False
    else:
        print (
            '\n\n%s is not a valid argument.\n'
            'True or False is only accepted\n\n' %
            val
        )


def AbsPath(val):
    return abspath(Decoder(val))


def get_args():
    parser = argparse.ArgumentParser(
        description='EventGhost Automation Software'
    )

    parser.add_argument(
        dest='loadFile',
        help=(
            'Specify a save file (.egtree)'
            ' or a plugin file (.egplugin) to load.'
        ),
        type=AbsPath,
        default=None,
        nargs='?'
    )

    parser.add_argument(
        '-d',
        '-debug',
        '--debug',
        dest='debugLevel',
        help='Debugging',
        type=int,
        required=False,
        default=0,
        nargs='?',
        const=1
    )
    parser.add_argument(
        '-n',
        '-netsend',
        '--netsend',
        dest='netSend',
        help='Send data to another computer.',
        type=Decoder,
        required=False,
        default=None,
        nargs='*'
    )
    parser.add_argument(
        '-mg',
        '-minimizegui',
        '--minimizegui',
        dest='hideOnStartup',
        help='Start EventGhost minimized.',
        type=DefaultValue,
        required=False,
        default=False,
        nargs='?',
        const=True
    )
    parser.add_argument(
        '-i',
        '-install',
        '--install',
        dest='install',
        help='Compile all EventGhost files.',
        type=DefaultValue,
        required=False,
        default=False,
        nargs='?',
        const=True
    )
    parser.add_argument(
        '-u',
        '-uninstall',
        '--uninstall',
        dest='uninstall',
        help='Remove all .pyc (python compiled) files.',
        type=DefaultValue,
        required=False,
        default=False,
        nargs='?',
        const=True
    )
    parser.add_argument(
        '-m',
        '-multiload',
        '--multiload',
        dest='allowMultiLoad',
        help='Open multiple instances of EventGhost.',
        type=DefaultValue,
        required=False,
        default=False,
        nargs='?',
        const=True
    )
    parser.add_argument(
        '-e',
        '-event',
        '--event',
        dest='startupEvent',
        help='Send an event.',
        type=Decoder,
        required=False,
        default=None,
        nargs='*'
    )
    parser.add_argument(
        '-f',
        '-file',
        '--file',
        dest='startupFile',
        help='Specify which .egtree (save file) to load.',
        type=AbsPath,
        required=False,
        default=None,
        nargs='?',
        const=True
    )
    parser.add_argument(
        '-p',
        '-plugin',
        '--plugin',
        dest='pluginFile',
        help='Install Plugin',
        type=AbsPath,
        required=False,
        default=None,
        nargs='?',
        const=True
    )
    parser.add_argument(
        '-c',
        '-configdir',
        '--configdir',
        dest='configDir',
        help='Specify what config file to use.',
        type=Decoder,
        required=False,
        default=None,
        nargs='?',
        const=True
    )
    parser.add_argument(
        '-t',
        '-translate',
        '--translate',
        dest='translate',
        help='Open Translation Editor.',
        type=DefaultValue,
        required=False,
        default=False,
        nargs='?',
        const=True
    )
    parser.add_argument(
        '-r',
        '-restart',
        '--restart',
        dest='restart',
        help='Restart EventGhost.',
        type=DefaultValue,
        required=False,
        default=False,
        nargs='?',
        const=True
    )

    return parser.parse_args()


if isMain:
    old_stdout = sys.stdout
    sys.stdout = StdOut()

    args = get_args()
    setattr(args, 'isMain', isMain)
    err = ''

    if args.startupFile is True:
        err += '\nWhen using -f, -file, or --file\n'
        err += 'you must specify file path and file name.\n\n'

    if args.pluginFile is True:
        err += '\nWhen using -p, -plugin, or --plugin\n'
        err += 'you must specify file path and file name.\n\n'

    if args.configDir is True:
        err += '\nWhen using -c, -configdir, or --configdir\n'
        err += 'you must specify file path and file name.\n\n'

    if args.startupEvent is not None and not args.startupEvent:
        err += '\nWhen using -e, -event, or --event\n'
        err += 'you must specify the event and payload (if any).\n\n'

    if args.netSend is not None and not args.netSend:
        err += '\nWhen using -n, -netsend, or --netsend\n'
        err += 'you must specify the data to be sent.\n\n'

    if args.loadFile:
        path = args.saveFile
        ext = os.path.splitext(path)[1].lower()
        if ext == ".egplugin":
            args.pluginFile = path
        elif ext in (".egtree", ".xml"):
            if args.startupFile:
                err += '\nYou cannot use the switches -f, -file, or --file\n'
                err += 'when specifying the file to load after the executable.'
                err += '\n\n'

            else:
                args.startupFile = path

    if err:
        print err

    sys.stdout = old_stdout

    if args.netSend:
        from Classes.NetworkSend import Main
        Main(args.netSend)
        sys.exit(0)

    if args.install:
        import compileall
        compileall.compile_dir(mainDir)

    if args.uninstall:
        for root, dirs, files in os.walk(mainDir):
            for name in files:
                if name.lower().endswith((".pyc", ".pyo")):
                    os.remove(join(root, name))
        sys.exit(0)

    if args.startupEvent:
        eventstring = args.startupEvent[0]
        payload = args.startupEvent[1:]
        if len(payload) == 0:
            payload = None
        args.startupEvent = (eventstring, payloads)

    if args.restart:
        import time

        while True:
            appMutex = ctypes.windll.kernel32.CreateMutexA(
                None,
                0,
                "Global\\EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B"
            )
            err = ctypes.GetLastError()
            if appMutex:
                ctypes.windll.kernel32.CloseHandle(appMutex)
            if err == 0:
                break
            time.sleep(0.1)

    if not args.allowMultiLoad and not args.translate and isMain:
        # check if another instance of the program is running
        appMutex = ctypes.windll.kernel32.CreateMutexA(
            None,
            0,
            "Global\\EventGhost:7EB106DC-468D-4345-9CFE-B0021039114B"
        )
        if ctypes.GetLastError() != 0:
            # another instance of EventGhost is running
            from win32com.client import Dispatch
            try:
                e = Dispatch("{7EB106DC-468D-4345-9CFE-B0021039114B}")
                if args.startupFile is not None:
                    e.OpenFile(args.startupFile)
                if args.startupEvent is not None:
                    e.TriggerEvent(args.startupEvent[0], args.startupEvent[1])
                if args.pluginFile:
                    e.InstallPlugin(args.pluginFile)

                e.BringToFront()
            except pywintypes.com_error as err:
                if err[0] in (-2147024156, -2147467259):
                    msg = (
                        "Unable to run elevated and unelevated simultaneously."
                    )
                elif err[2]:
                    msg = "%s:\n\n%s" % (str(err[2][1]), str(err[2][2]))
                else:
                    msg = "Failed to launch for unknown reasons: %s" % err
                ctypes.windll.user32.MessageBoxA(0, msg, "EventGhost", 48)
            finally:
                ctypes.windll.kernel32.ExitProcess(0)

else:
    class args:
        allowMultiLoad = False
        configDir = None
        debugLevel = 0
        hideOnStartup = False
        install = False
        isMain = isMain
        pluginFile = None
        startupEvent = None
        startupFile = None
        translate = False


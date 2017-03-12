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


HELP = '''
Usage:
    eventghost [.egtree/.egplugin file]
               [-?,   --help] [-h, --hide] [-i, --install] [-u, --uninstall]
               [-m, --multiload] [-t, --translate] [-r, --restart]
               [-n,   --netsend [data]] [-d, --debug [modules]]
               [-e,   --event [event] [payload]] [-c, --configdir [config path]]
               [-p,   --pluginfile [.egplugin file]] [-f, --file [.egtree file]]


    .egtree/.egplugin file
        will load a save file or install a plugin
        eventghost C:\SomeDirectory\SomeFile.(egtree/egplugin)

    -?,   --help              Show this help message and exit.
    -h,   --hide             Start EventGhost minimized.
    -i,    --install           Compile all EventGhost files.
    -u,   --uninstall      Remove all .pyc (python compiled) files.
    -m, --multiload     Open multiple instances of EventGhost.
    -t,    --translate      Open Translation Editor.
    -r,    --restart          Restart EventGhost.
    -n,   --netsend       Send data to another computer.
                                     --netsend "Some data to be sent"

    -d,   --debug          Enable debugging. Optionally you can specify
                                     module names to enable verbose debugging.
                                     If the module supports verbose debugging.

                                     enable verbose debugging globally.
                                     --debug eg

                                     enable debugging for all core plugins.
                                     --debug eg.CorePluginModule

                                     enable debugging for a specific core
                                     plugin.
                                     --debug eg.CorePluginModule.EventGhost

                                     enable debugging for a specific module in
                                     a core plugin.
                                     --debug eg.CorePluginModule.Window.SendKeys

                                     You can also specify more then one module
                                     to set to verbose debugging just put a
                                     space between them. Because this feature
                                     uses a "Bottom Up" means to set the
                                     verbose debugging doing the following is
                                     pointless.
                                     --debug eg.CorePluginModule eg

                                     This is because eg is the bottom most
                                     module and everything on top of it also
                                     has verbose debugging set.

    -e,    --event            Trigger an event.
                                     --event Some.Triggered.Event PayloadData

    -c,   --configdir      Specify what config file to use.
                                     --configdir C:\SomeDirectory

    -p,   --pluginfile     Install a plugin (.egplugin).
                                     --pluginfile C:\SomeDir\PluginFile.egplugin

    -f,   --file           Specify which .egtree (save file) to load.
                                     --file C:\SomeDir\SaveFile.egtree

    ** Now don't forget if you want an optional argument that has spaces in it
    to be treated as a single statement, you will need to wrap the statement in
    "double quotes"

'''

class StdOut(object):

    def __init__(self):
        self.app = None
        self.dialog = None
        self.textCtrl = None

    def ShowModal(self):
        self.dialog.ShowModal()

    def write(self, data):
        if self.app is None:
            self.app = wx.App()
            self.app.MainLoop()
            self.dialog = wx.Dialog(
                None,
                size=(475, 600),
                title='Command Line Help',
                style=(
                    wx.CAPTION |
                    wx.RESIZE_BORDER |
                    wx.CLOSE_BOX
                )
            )
            panel = wx.Panel(self.dialog)
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.textCtrl = wx.TextCtrl(
                panel,
                -1,
                data,
                style=wx.TE_MULTILINE | wx.TE_READONLY
            )

            sizer.Add(self.textCtrl, 1, wx.EXPAND | wx.ALL, 10)
            panel.SetSizer(sizer)

            def OnClose(evt):
                self.dialog.EndModal(wx.ID_CANCEL)
                self.app.ExitMainLoop()
                wx.WakeUpMainThread()

            self.dialog.Bind(wx.EVT_CLOSE, OnClose)
        else:
            text = self.textCtrl.GetLabel()
            text += '\n'
            text += data
            self.textCtrl.SetLabel(text)
            self.dialog.Refresh()

    def flush(self):
        pass

    def isatty(self):
        return True

stdout = StdOut()


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
        stdout.ShowModal()
        sys.exit(1)


def AbsPath(val):
    return abspath(Decoder(val))


def get_args():
    parser = argparse.ArgumentParser(
        description='EventGhost Automation Software',
        add_help=False,
        prefix_chars='-/'
    )

    parser.add_argument(
        '-?',
        '-help',
        '--help',
        '/?',
        dest='help',
        type=Decoder,
        required=False,
        default=False,
        nargs='?',
        const=True
    )

    parser.add_argument(
        dest='saveFile',
        type=AbsPath,
        default=None,
        nargs='?',

    )

    parser.add_argument(
        '-d',
        '-debug',
        '--debug',
        '/d',
        dest='debugLevel',
        type=Decoder,
        required=False,
        default=False,
        nargs='*',

    )
    parser.add_argument(
        '-n',
        '-netsend',
        '--netsend',
        '/n',
        dest='netSend',
        type=Decoder,
        required=False,
        default=None,
        nargs='*'
    )
    parser.add_argument(
        '-h',
        '-hide',
        '--hide',
        '/h',
        dest='hideOnStartup',
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
        '/i',
        dest='install',
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
        '/u',
        dest='uninstall',
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
        '/m',
        dest='allowMultiLoad',
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
        '/e',
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
        '/f',
        dest='startupFile',
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
        '/p',
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
        '/c',
        dest='configDir',
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
        '/t',
        dest='translate',
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
        '/r',
        dest='restart',
        type=DefaultValue,
        required=False,
        default=False,
        nargs='?',
        const=True
    )

    return parser.parse_args()


if isMain:
    old_stdout = sys.stdout
    sys.stdout = stdout

    try:
        args = get_args()
    except:
        print HELP
        stdout.ShowModal()
        sys.exit(1)

    if args.help:
        print HELP
        stdout.ShowModal()
        sys.exit(1)

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

    if args.saveFile:
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
        print err + '\n\n' + HELP
        stdout.ShowModal()
        sys.exit(1)

    sys.stdout = old_stdout

    if args.debugLevel is False:
        args.debugLevel = 0
        setattr(args, 'debugVerbose', ())
    else:
        setattr(args, 'debugVerbose', tuple(args.debugLevel))
        args.debugLevel = 1

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
        debugVerbose = ()
        hideOnStartup = False
        install = False
        isMain = isMain
        pluginFile = None
        startupEvent = None
        startupFile = None
        translate = False


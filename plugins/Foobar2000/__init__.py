# Plugins/Foobar2000/__init__.py
#
# Copyright (C) 2006 MonsterMagnet
#
# This file is a plugin for EventGhost.
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


# Every EventGhost plugin should start with the import of 'eg' and the 
# definition of an eg.PluginInfo subclass.


eg.RegisterPlugin(
    name = "Foobar2000",
    author = "MonsterMagnet",
    version = "1.1." + "$LastChangedRevision$".split()[1],
    kind = "program",
    description = (
        'Adds actions to control the <a href="http://www.foobar2000.org/">'
        'Foobar2000</a> audio player.'
    ),
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=695",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC0UlEQVR42m1TO0hjURA9"
        "1/8nH+OPJdoYRIWgLgZhwUJsLFZUkG0iYiGCgnZpJKRQUDfEVhAsDWIRFSzURtlO0YiC"
        "pFAskxiiFnn5+Es0OzPw3GYHLu8+7sy5Z86ZqwDYaP2uq6v7YaYoKChAPp+XxXuOz89P"
        "KKVkfXx8IJlMZh8fH4N05FKUFBgZGfk1MDCA8vJySSoqKpK9pmkCRLh4f3/H29ub/L+8"
        "vODg4AC7u7v7qr6+Pup2u621tbXIZrOS2NzcjI6ODuzt7SGXy2FwcBCRSASXl5coKSlB"
        "cXExnp6e4PV6Y8pqtWrj4+OmsrIyocogTqcT7e3t2NzcRCqVwvT0NMLhMNbX14VBYWEh"
        "Xl9f+TypqqurE/39/WYG4GJihMXFRVRUVEgx91xVVSXgCwsLuLm5AecywPHxsaYqKysT"
        "nZ2dAsAFExMTcuP/Ymdnh2nDYDCIHtfX15qifhKNjY1m7qu0tBRzc3NoaGhAb2/vVyHr"
        "EAgEYLFYMD8/L/0zI9JFYxcSNTU1ZlbeZrOhp6cHPp8PJCyWlpZE1MnJSfj9fqyuruLo"
        "6AgnJyfiFgH9A2AGJpNJKE5NTSEejyMYDIp4ZDPsdju2t7cxNjaG+/t7YfAFQENkZvqZ"
        "TAazs7MYGhrC8vIyPB6PeL6xsSGM2FYWkmeEBadh0hRRT5CVZladFWfkra0tdHd3IxQK"
        "iQOkEU5PT0F2i43cLrsQi8U0RTcnWlpaeIpFMD5oa2vDysoKDg8PQS6JLjMzM4hGoyI0"
        "989s7+7uNGU0GjWHw2HiSdTfAdMeHh7G6OioJK6trYkeTF0Peg88mUlFlsW6urq+NTU1"
        "CTXdNr7J5XLh9vZWWuI50YMveXh4wMXFRVzR/35ra+vPvr4+cUF/dQxC7iCdTouVPL5c"
        "yPH8/Izz83OcnZ39YQA7LS89nu9UaGQ7GUBnwm3prXGw0BSZq6urEH09fwEfgnAhbyFf"
        "mQAAAABJRU5ErkJggg=="
    ),
)

# changelog:
# 1.1 by bitmonster
#     - changed code to use new AddActionsFromList method
# 1.0 by MonsterMagnet
#     - initial version


# Now import some other modules that are needed for the special purpose of
# this plugin.
import os
import _winreg
from win32api import ShellExecute


# This plugin will create its actions dynamically from a list of data.
#
# Here we define a list of tuples, where every tuple contains the following
# information:
#   1. The name of the eg.ActionClass we want to create later.
#   2. A value for the 'name' member.
#   3. A value for the 'description' member.
#   4. A value that is needed by the action to do the actual work. This time
#      it is the parameter that will be used for a command line that calls
#      Foobar2000.

ACTIONS = (
    (
        "Play",
        "Play", 
        "Simulate a press on the play button.", 
        "/play"
    ), 
    (
        "Pause",
        "Pause", 
        "Simulate a press on the pause button.", 
        "/pause"
    ), 
    (
        "Stop",
        "Stop", 
        "Simulate a press on the stop button.", 
        "/stop"
    ), 
    (
        "PreviousTrack",
        "Previous Track", 
        "Simulate a press on the previous track button.", 
        "/prev"
    ), 
    (
        "NextTrack", 
        "Next Track", 
        "Simulate a press on the next track button.", 
        "/next"
    ), 
    (
        "Random", 
        "Random", 
        "Simulate a press on the random button.", 
        "/rand"
    ), 
    (
        "Exit", 
        "Exit", 
        "Quits foobar.", 
        "/exit"
    ), 
    (
        "PlayPause", 
        "Toggle Play/Pause", 
        "Simulate a press on the PlayPause button.", 
        "/playpause"
    ), 
    (
        "Show", 
        "Show", 
        "Shows foobar.", 
        "/show"
    ), 
    (
        "Hide", 
        "Hide", 
        "Hides foobar.", 
        "/hide"
    ), 
    (
        "Run", 
        "Run", 
        "Run foobar with its default settings.", 
        None
    ),
    (
        "SeekAhead1s", 
        "Seek ahead by 1 second", 
        "Seek ahead by 1 second.", 
        '/command:"Seek ahead by 1 second"'
    ),
    (
        "VolumeUp", 
        "Volume Up", 
        "Turn Volume Up.", 
        '/command:"Volume up"'
    ),
    (
        "VolumeDown", 
        "Volume Down", 
        "Turn Volume Down.", 
        '/command:"Volume down"'
    ),
    (
        "VolumeMute", 
        "Volume Mute", 
        "Turn Volume Mute.", 
        '/command:"Volume mute"'
    ),
    (
        "SeekAhead1s", 
        "Seek ahead by 1 seconds", 
        "Seek ahead by 1 seconds.", 
        '/command:"Seek ahead by 1 seconds"'
    ),
    (
        "SeekAhead5s", 
        "Seek ahead by 5 seconds", 
        "Seek ahead by 5 seconds.", 
        '/command:"Seek ahead by 5 seconds"'
    ),
    (
        "SeekAhead10s", 
        "Seek ahead by 10 seconds", 
        "Seek ahead by 10 seconds.", 
        '/command:"Seek ahead by 10 seconds"'
    ),
    (
        "SeekAhead30s", 
        "Seek ahead by 30 seconds", 
        "Seek ahead by 30 seconds.", 
        '/command:"Seek ahead by 30 seconds"'
    ),
    (
        "SeekAhead1m", 
        "Seek ahead by 1 minute", 
        "Seek ahead by 1 minute.", 
        '/command:"Seek ahead by 1 minute"'
    ),
    (
        "SeekAhead2m", 
        "Seek ahead by 2 minute", 
        "Seek ahead by 2 minute.", 
        '/command:"Seek ahead by 2 minute"'
    ),
    (
        "SeekAhead5m", 
        "Seek ahead by 5 minute", 
        "Seek ahead by 5 minute.", 
        '/command:"Seek ahead by 5 minute"'
    ),
    (
        "SeekAhead10m", 
        "Seek ahead by 10 minute", 
        "Seek ahead by 10 minute.", 
        '/command:"Seek ahead by 10 minute"'
    ),
    (
        "SeekBack1s", 
        "Seek back by 1 seconds", 
        "Seek back by 1 seconds.", 
        '/command:"Seek back by 1 seconds"'
    ),
    (
        "SeekBack5s", 
        "Seek back by 5 seconds", 
        "Seek back by 5 seconds.", 
        '/command:"Seek back by 5 seconds"'
    ),
    (
        "SeekBack10s", 
        "Seek back by 10 seconds", 
        "Seek back by 10 seconds.", 
        '/command:"Seek back by 10 seconds"'
    ),
    (
        "SeekBack30s", 
        "Seek back by 30 seconds", 
        "Seek back by 30 seconds.", 
        '/command:"Seek back by 30 seconds"'
    ),
    (
        "SeekBack1m", 
        "Seek back by 1 minute", 
        "Seek back by 1 minute.", 
        '/command:"Seek back by 1 minute"'
    ),
    (
        "SeekBack2m", 
        "Seek back by 2 minute", 
        "Seek back by 2 minute.", 
        '/command:"Seek back by 2 minute"'
    ),
    (
        "SeekBack5m", 
        "Seek back by 5 minute", 
        "Seek back by 5 minute.", 
        '/command:"Seek back by 5 minute"'
    ),
    (
        "SeekBack10m", 
        "Seek back by 10 minute", 
        "Seek back by 10 minute.", 
        '/command:"Seek back by 10 minute"'
    ),
)


class ActionPrototype(eg.ActionClass):

    # Every action needs a workhorse.
    def __call__(self):
        # This one is quite simple. It just calls ShellExecute.
        try:
            head, tail = os.path.split(self.plugin.foobar2000Path)
            return ShellExecute(0, None, tail, self.value, head, 1)
        except:
            # Some error-checking is always fine.
            raise self.Exceptions.ProgramNotFound


# Now we can start to define the plugin by sub-classing eg.PluginClass
class Foobar2000(eg.PluginClass):
    
    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)


    def __start__(self, foobar2000Path=None):
        if foobar2000Path is None:
            foobar2000Path = self.GetFoobar2000Path()
        if not os.path.exists(foobar2000Path):
            raise self.Exceptions.ProgramNotFound
        self.foobar2000Path = foobar2000Path
        
        
    def Configure(self, foobar2000Path=None):
        if foobar2000Path is None:
            foobar2000Path = self.GetFoobar2000Path()
            if foobar2000Path is None:
                foobar2000Path = os.path.join(
                    eg.folderPath.ProgramFiles, 
                    "foobar2000", 
                    "foobar2000.exe"
                )
        panel = eg.ConfigPanel(self)
        filepathCtrl = eg.FileBrowseButton(
            panel, 
            size=(320,-1),
            initialValue=foobar2000Path, 
            startDirectory=eg.folderPath.ProgramFiles,
            labelText="",
            fileMask = "Foobar2000 executable|foobar2000.exe|All-Files (*.*)|*.*",
            buttonText=eg.text.General.browse,
        )
        panel.AddLabel("Path to foobar2000 executable:")
        panel.AddCtrl(filepathCtrl)
        
        while panel.Affirmed():
            panel.SetResult(filepathCtrl.GetValue())
        
        
    def GetFoobar2000Path(self):
        """
        Get the path of Foobar2000's installation directory through querying 
        the Windows registry.
        
        Only works for older version of foobar2000.
        """
        try:
            fb = _winreg.OpenKey(
                _winreg.HKEY_CURRENT_USER,
                "Software\\foobar2000"
            )
            foobar2000Path, dummy =_winreg.QueryValueEx(fb, "InstallDir")
            _winreg.CloseKey(fb)
            foobar2000Path = os.path.join(foobar2000Path, "foobar2000.exe")
        except WindowsError:
            foobar2000Path = None
        return foobar2000Path
        

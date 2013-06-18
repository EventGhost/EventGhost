
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
import eg

class PluginInfo(eg.PluginInfo):
    name = "Foobar2000"
    author = "MonsterMagnet"
    version = "1.0.0"
    kind = "program"
    description = (
        'Adds support functions to control Foobar2000.'
        '\n\n<p><a href="http://www.foobar2000.org/">Foobar2000 Homepage</a>'
    )
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
    )


# Since we also have to do some GUI stuff, we also need 'wx'
import wx

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
#      it is the parameter that will be used for a commandline that calls
#      Foobar2000.

fnList = (
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
)


# Now we can start to define the plugin by subclassing eg.PluginClass
class Foobar2000(eg.PluginClass):
    foobar2000Path = None
    
    def __init__(self):
        foobar2000Path = ""
        # And now begins the tricky part. We will loop through every tuple in
        # our list to get the needed values.
        for tmpClassName, tmpName, tmpDescription, tmpParameter in fnList:
            # Then we will create a subclass of eg.ActionClass on every
            # iteration and assign the values to the class-variables.
            class tmpActionClass(eg.ActionClass):
                name = tmpName
                description = tmpDescription
                parameter = tmpParameter
                
                # Every action needs a workhorse.
                def __call__(self):
                    # This one is quite simple. It just calls ShellExecute.
                    try:
                        head, tail = os.path.split(self.plugin.foobar2000Path)
                        return ShellExecute(
                            0, 
                            None, 
                            tail,
                            self.parameter, 
                            head, 
                            1
                        )
                    except:
                        # Some error-checking is always fine.
                        self.PrintError("Foobar2000 not found!")
            
            # We also have to change the classname of the action to a unique
            # value, otherwise we would overwrite our newly created action
            # on the next iteration.
            tmpActionClass.__name__ = tmpClassName
            
        # EventGhost will monitor the creation of every new subclass of 
        # eg.ActionClass, so everything that is finally needed is to call
        # self.AddAllActions() to instantiate all defined actions. 
        self.AddAllActions()


    def __start__(self, foobar2000Path=None):
        if foobar2000Path is None:
            foobar2000Path = self.GetFoobar2000Path()
        self.foobar2000Path = foobar2000Path
        
        
    def Configure(self, foobar2000Path=None):
        if foobar2000Path is None:
            foobar2000Path = self.GetFoobar2000Path()
            if foobar2000Path is None:
                foobar2000Path = os.path.join(
                    eg.PROGRAMFILES, 
                    "foobar2000", 
                    "foobar2000.exe"
                )
        dialog = eg.ConfigurationDialog(self)
        filepathCtrl = eg.FileBrowseButton(
            dialog, 
            size=(320,-1),
            initialValue=foobar2000Path, 
            startDirectory=eg.PROGRAMFILES,
            labelText="",
            fileMask = "Foobar2000 executable|foobar2000.exe|All-Files (*.*)|*.*",
            buttonText=eg.text.General.browse
        )
        dialog.AddLabel("Path to foobar2000 executable:")
        dialog.AddCtrl(filepathCtrl)
        
        if dialog.AffirmedShowModal():
            return (filepathCtrl.GetValue(), )
        
        
    def GetFoobar2000Path(self):
        """
        Get the path of Foobar2000's install-dir through querying the 
        Windows registry.
        
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
        

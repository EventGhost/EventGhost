# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org> 
#                    and Matthew Jacob Edwards
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
# Winamp AlbumList Plugin for Eventghost
# only importent funktions included for this essential Album User Plugin
#

# expose some information about the plugin through an eg.PluginInfo subclass

import eg

eg.RegisterPlugin(
    name="Winamp AlbumList",
    guid='{714CC227-631A-4703-B551-BAA4DC454F3D}',
    author="Bjoern Buettner",
    version="1.0.0",
    kind="program",
    createMacrosOnAdd=True,
    description=(
        'Adds actions to control <a href="http://albumlist.sourceforge.net/">Album List for Winamp</a>.'
    ),
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACDElEQVR42pWTT0gUcRTH"
        "P7OQemvKQ7pSbkQgHWLm0k2cgxpUsLOBFUS4UmCBZEuHLsHugBAeLPca4U4RmILsinno"
        "j+SCYLTETiUsRsFuBOpSMoE2SGzbONg6q6vR7/J+vx/v832/937vCeyygsFgcd3qui7s"
        "5CPsBttgYmOvukSCxxtF//ucGdhR4C9cLBZVx0kQEusiyxnd0HrPSuPDM0Qm8kJFga1w"
        "NpsleidES8NL1I6rkBzj8tAXYyhVkLcJuGHTNNEfRPmR1ghfOwo1p2B2hO7HefP+m8Jh"
        "290sE3DDtuXdZIjwuVXE2gNwpAuexdCeVxMZ+5xw10Rww+l0Wn14t4vOEx+Q5CY7ah0U"
        "bJc1D+Z3Ae1ehs7oOLIsl0QEd2RNs597+iPkFsH6DScvwNfX9nkZMnNMr/yCtkcoilIq"
        "7HaBphFY+Qmt3TY4D1Mz4PXAnjUGJ/Io4VkkSdoU2JpCIHCG+HAP0twU5D/BoSrMhW9o"
        "SZGWKwOoqlqCnRTcRTSMFLF+P1L6KeyznKh60iJXf5HeW2FEUSyDy37B690fm7zdHpSs"
        "t3Cwiuz8IlGjEX/PgJOzu6Hcre1sfHU1kXj0fFiyUlBcRRtdYm9bHzdCNzd7vgJcEuho"
        "rn01er1eMYwFQk/MaV/zJaVSK1caKuei/Vh1XG7wKP0vLM0+Dv5jmCpOo2/DZv93nP8A"
        "opkfXpsJ2wUAAAAASUVORK5CYII="
    ),
)

# Now we import some other things we will need later
from eg.WinApi import (
    SendMessageTimeout,
    FindWindow,
)

WM_USER = 1024
WM_AL_IPC = WM_USER


# Next we define a prototype of an action, with some helper methods

class ActionBase(eg.ActionClass):

    def SendCommand(self, mesg, wParam, lParam=0):
        """
        Find Winamp's message window and send it a message with 
        SendMessageTimeout.
        """
        try:
            halbumlist = FindWindow('Winamp AL')
            return SendMessageTimeout(halbumlist, mesg, wParam, lParam)
        except:
            raise self.Exceptions.ProgramNotRunning


# And now we define the actual plugin:

class WinampAlbumlist(eg.PluginClass):
    class text:
        infoGroupName = "Information retrieval"
        infoGroupDescription = (
            "Here you find actions that query different aspects of Winamp."
            "They can for example be used to display these informations on a "
            "small LCD/VFD."
        )

    def __init__(self):
        self.AddAction(PlayPrevAlbum)
        self.AddAction(PlayNextAlbum)
        self.AddAction(PlayRandomAlbum)
        self.AddAction(PlayPrevAlbumArtist)
        self.AddAction(PlayNextAlbumArtist)

    # Here we define our first action. Actions are always subclasses of


# ActionBase.

AL_PLAYPREVALBUM = 114
AL_PLAYNEXTALBUM = 115
AL_PLAYALLALBUMS = 116
AL_PLAYRANDOMALBUM = 102
AL_PLAYPREVALBUMARTIST = 120
AK_PLAYNEXTALBUMARTIST = 121


class PlayPrevAlbum(ActionBase):
    # If we don't define a 'name' member, EventGhost creates one with the
    # class-name as content.
    description = "Simulate a press on the play button."

    def __call__(self):
        return self.SendCommand(WM_AL_IPC, AL_PLAYPREVALBUM)


class PlayNextAlbum(ActionBase):
    # If we don't define a 'name' member, EventGhost creates one with the
    # class-name as content.
    description = "Simulate a press on the play button."

    def __call__(self):
        return self.SendCommand(WM_AL_IPC, AL_PLAYNEXTALBUM)


class PlayRandomAlbum(ActionBase):
    description = "Simulate a press on the pause button."

    def __call__(self):
        return self.SendCommand(WM_AL_IPC, AL_PLAYRANDOMALBUM)


class PlayPrevAlbumArtist(ActionBase):
    description = "Simulate a press on the pause button."

    def __call__(self):
        return self.SendCommand(WM_AL_IPC, AL_PLAYPREVALBUMARTIST)


class PlayNextAlbumArtist(ActionBase):
    description = "Simulate a press on the pause button."

    def __call__(self):
        return self.SendCommand(WM_AL_IPC, AK_PLAYNEXTALBUMARTIST)

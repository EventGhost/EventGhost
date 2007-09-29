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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

from eg.WinAPI.cTypes import (
    byref, sizeof, addressof, pointer,
    HMIXER, 
    MIXERCONTROL, 
    MIXERLINECONTROLS, 
    MIXERLINE, 
    MIXERCONTROL, 
    MIXERCONTROLDETAILS, 
    MIXERCONTROLDETAILS_UNSIGNED, 
    mixerOpen, 
    mixerGetControlDetails, 
    mixerGetLineInfo, 
    mixerGetLineControls,
    mixerSetControlDetails, 
    MIXERLINE_COMPONENTTYPE_DST_SPEAKERS,
    MIXERCONTROL_CONTROLTYPE_MUTE,
    MIXERCONTROL_CONTROLTYPE_VOLUME,
    MIXER_GETLINEINFOF_COMPONENTTYPE,
    MIXER_GETLINECONTROLSF_ONEBYTYPE,
    MMSYSERR_NOERROR,
)
    
    
class SoundMixerException(Exception):
    pass


def GetMixerControl(componentType, ctrlType):
    '''
    Obtains an appropriate pointer and info for the volume control
    This function attempts to obtain a mixer control. Raises 
    SoundMixerException if not successful.
    '''
    hmixer = HMIXER()

    # Obtain the hmixer struct
    rc = mixerOpen(byref(hmixer), 0, 0, 0, 0)
    if rc != MMSYSERR_NOERROR:
        raise SoundMixerException()

    mixerLineControls = MIXERLINECONTROLS()
    mixerLineControls.cbStruct = sizeof(MIXERLINECONTROLS)
    mixerLine = MIXERLINE()
    mixerLine.cbStruct = sizeof(MIXERLINE)
    mixerControl = MIXERCONTROL()
    mixerControl.cbStruct = sizeof(MIXERCONTROL)

    mixerLine.dwComponentType = componentType

    # Obtain a line corresponding to the component type
    rc = mixerGetLineInfo(
        hmixer, 
        byref(mixerLine), 
        MIXER_GETLINEINFOF_COMPONENTTYPE
    )
    if rc != MMSYSERR_NOERROR:
        raise SoundMixerException()

    mixerLineControls.dwLineID = mixerLine.dwLineID
    mixerLineControls.dwControlType = ctrlType
    mixerLineControls.cControls = 1
    mixerLineControls.cbmxctrl = sizeof(mixerControl)
    mixerLineControls.pamxctrl = pointer(mixerControl)

    # Get the control
    rc = mixerGetLineControls(
        hmixer, 
        byref(mixerLineControls), 
        MIXER_GETLINECONTROLSF_ONEBYTYPE
    )
    if MMSYSERR_NOERROR != rc:
        raise SoundMixerException()
    return hmixer, mixerControl


def GetControlValue(hmixer, mixerControl):
    valueDetails = MIXERCONTROLDETAILS_UNSIGNED()

    mixerControlDetails = MIXERCONTROLDETAILS()
    mixerControlDetails.cbStruct = sizeof(MIXERCONTROLDETAILS)
    mixerControlDetails.item = 0
    mixerControlDetails.dwControlID = mixerControl.dwControlID
    mixerControlDetails.cbDetails = sizeof(valueDetails)
    mixerControlDetails.paDetails = addressof(valueDetails)
    mixerControlDetails.cChannels = 1

    # Get the control value
    rc = mixerGetControlDetails(hmixer, byref(mixerControlDetails), 0)
    if rc != MMSYSERR_NOERROR:
        raise SoundMixerException()
    return valueDetails.dwValue


def SetControlValue(hmixer, mixerControl, value):
    ''' 
    Sets the volumne from the pointer of the object passed through

    ' [Note: original source taken from MSDN 
    http://support.microsoft.com/default.aspx?scid=KB;EN-US;Q178456&]

    This function sets the value for a volume control. Returns True if 
    successful
    '''

    valueDetails = MIXERCONTROLDETAILS_UNSIGNED()
    valueDetails.dwValue = value
    mixerControlDetails = MIXERCONTROLDETAILS()
    mixerControlDetails.cbStruct = sizeof(MIXERCONTROLDETAILS)
    mixerControlDetails.item = 0
    mixerControlDetails.dwControlID = mixerControl.dwControlID
    mixerControlDetails.cbDetails = sizeof(valueDetails)
    mixerControlDetails.paDetails = addressof(valueDetails)
    mixerControlDetails.cChannels = 1

    # Set the control value
    rc = mixerSetControlDetails(hmixer, byref(mixerControlDetails), 0)
    if rc != MMSYSERR_NOERROR:
        raise SoundMixerException()


def GetMute():
    # Obtain the volumne control object
    hmixer, mixerControl = GetMixerControl(
        MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
        MIXERCONTROL_CONTROLTYPE_MUTE
    )

    # Then get the volume
    return GetControlValue(hmixer, mixerControl)    


def SetMute(mute=True):
    # Obtain the volumne control object
    hmixer, mixerControl = GetMixerControl(
        MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
        MIXERCONTROL_CONTROLTYPE_MUTE
    )

    # Then set the volume
    return SetControlValue(hmixer, mixerControl, int(mute))


def ToggleMute():
    flag = not GetMute()
    SetMute(flag)
    return flag


def GetMasterVolume():
    # Obtain the volumne control object
    hmixer, mixerControl = GetMixerControl(
        MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
        MIXERCONTROL_CONTROLTYPE_VOLUME
    )

    # Then get the volume
    value = GetControlValue(hmixer, mixerControl)
    
    max = mixerControl.Bounds.lMaximum
    min = mixerControl.Bounds.lMinimum
    value = 100.0 * (value - min) / (max - min)
    return value
    
    
def SetMasterVolume(value):
    # Obtain the volumne control object
    hmixer, volCtrl = GetMixerControl(
        MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
        MIXERCONTROL_CONTROLTYPE_VOLUME
    )

    max = volCtrl.Bounds.lMaximum
    min = volCtrl.Bounds.lMinimum
    newValue = int((value / 100.0) * (max - min)) + min
    if newValue < min:
        newValue = min
    elif newValue > max:
        newValue = max
    SetControlValue(hmixer, volCtrl, newValue)
    
    
def ChangeMasterVolumeBy(value):
    # Obtain the volumne control object
    hmixer, mixerControl = GetMixerControl(
        MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
        MIXERCONTROL_CONTROLTYPE_VOLUME
    )

    # Then get the volume
    oldVolume = GetControlValue(hmixer, mixerControl)
    
    max = mixerControl.Bounds.lMaximum
    min = mixerControl.Bounds.lMinimum
    newVolume = int(round((max - min) * value / 100.0)) + oldVolume
    if newVolume < min:
        newVolume = min
    elif newVolume > max:
        newVolume = max
    SetControlValue(hmixer, mixerControl, newVolume)
    

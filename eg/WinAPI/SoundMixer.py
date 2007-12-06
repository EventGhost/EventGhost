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

from ctypes.dynamic import (
    byref, sizeof, addressof, pointer,
    HMIXER, 
    MIXERCAPS,
    MIXERCONTROL, 
    MIXERLINECONTROLS, 
    MIXERLINE, 
    MIXERCONTROL, 
    MIXERLINECONTROLS,
    MIXERCONTROLDETAILS, 
    MIXERCONTROLDETAILS_UNSIGNED, 
    mixerOpen, 
    mixerGetNumDevs,
    mixerGetDevCaps,
    mixerGetControlDetails, 
    mixerGetLineInfo, 
    mixerGetLineControls,
    mixerSetControlDetails, 
    MIXERLINE_COMPONENTTYPE_DST_SPEAKERS,
    MIXERCONTROL_CONTROLTYPE_MUTE,
    MIXERCONTROL_CONTROLTYPE_VOLUME,
    MIXER_GETLINEINFOF_COMPONENTTYPE,
    MIXER_GETLINECONTROLSF_ONEBYTYPE,
    MIXER_GETLINECONTROLSF_ALL,
    MIXER_GETLINEINFOF_DESTINATION,
    MIXER_GETLINEINFOF_SOURCE,
    MMSYSERR_NOERROR,
)
    
    
class SoundMixerException(Exception):
    pass


def GetMixerControl(componentType, ctrlType, deviceId=0):
    '''
    Obtains an appropriate pointer and info for the volume control
    This function attempts to obtain a mixer control. Raises 
    SoundMixerException if not successful.
    '''
    hmixer = HMIXER()

    # Obtain the hmixer struct
    rc = mixerOpen(byref(hmixer), deviceId, 0, 0, 0)
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


def GetMute(deviceId=0):
    # Obtain the volumne control object
    hmixer, mixerControl = GetMixerControl(
        MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
        MIXERCONTROL_CONTROLTYPE_MUTE,
        deviceId
    )

    # Then get the volume
    return GetControlValue(hmixer, mixerControl)    


def SetMute(mute=True, deviceId=0):
    # Obtain the volumne control object
    hmixer, mixerControl = GetMixerControl(
        MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
        MIXERCONTROL_CONTROLTYPE_MUTE,
        deviceId
    )

    # Then set the volume
    return SetControlValue(hmixer, mixerControl, int(mute))


def ToggleMute(deviceId=0):
    flag = not GetMute(deviceId)
    SetMute(flag, deviceId)
    return flag


def GetMasterVolume(deviceId=0):
    # Obtain the volumne control object
    hmixer, mixerControl = GetMixerControl(
        MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
        MIXERCONTROL_CONTROLTYPE_VOLUME,
        deviceId
    )

    # Then get the volume
    value = GetControlValue(hmixer, mixerControl)
    
    max = mixerControl.Bounds.lMaximum
    min = mixerControl.Bounds.lMinimum
    value = 100.0 * (value - min) / (max - min)
    return value
    
    
def SetMasterVolume(value, deviceId=0):
    # Obtain the volumne control object
    hmixer, volCtrl = GetMixerControl(
        MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
        MIXERCONTROL_CONTROLTYPE_VOLUME,
        deviceId
    )

    max = volCtrl.Bounds.lMaximum
    min = volCtrl.Bounds.lMinimum
    newValue = int((value / 100.0) * (max - min)) + min
    if newValue < min:
        newValue = min
    elif newValue > max:
        newValue = max
    SetControlValue(hmixer, volCtrl, newValue)
    
    
def ChangeMasterVolumeBy(value, deviceId=0):
    # Obtain the volumne control object
    hmixer, mixerControl = GetMixerControl(
        MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
        MIXERCONTROL_CONTROLTYPE_VOLUME,
        deviceId
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
    
    
def GetMixerDevices():
    """ Returns a list of all mixer device names available on the system."""
    mixcaps = MIXERCAPS()
    result = []
    # get the number of Mixer devices in this computer
    for i in range(mixerGetNumDevs()):
        # get info about the device
        if mixerGetDevCaps(i, byref(mixcaps), sizeof(MIXERCAPS)):
            continue
        # store the name of the device
        result.append(mixcaps.szPname)
    return result
    
    
def GetDeviceLines(deviceId=0):
    mixercaps = MIXERCAPS()
    mixerline = MIXERLINE()
    hmixer = HMIXER()

    # Obtain the hmixer struct
    rc = mixerOpen(byref(hmixer), deviceId, 0, 0, 0)
    if rc != MMSYSERR_NOERROR:
        raise SoundMixerException()

    if mixerGetDevCaps(hmixer, byref(mixercaps), sizeof(MIXERCAPS)):
        raise SoundMixerException()
    
    for i in range(mixercaps.cDestinations):
        mixerline.cbStruct = sizeof(MIXERLINE)
        mixerline.dwDestination = i
        if mixerGetLineInfo(hmixer, byref(mixerline), MIXER_GETLINEINFOF_DESTINATION):
            continue
        print "Destination:", i, mixerline.szName.decode("mbcs")
        for name in GetControls(hmixer, mixerline):
            print "        Control:", name
        for n in range(mixerline.cConnections):
            mixerline.cbStruct = sizeof(MIXERLINE)
            mixerline.dwDestination = i
            mixerline.dwSource = n
            if mixerGetLineInfo(hmixer, byref(mixerline), MIXER_GETLINEINFOF_SOURCE):
                continue
            print "    Source:", n, mixerline.szName.decode("mbcs")
            for name in GetControls(hmixer, mixerline):
                print "            Control:", name
            
            
from ctypes.dynamic import (
    MIXERCONTROL_CT_CLASS_MASK,
    
    MIXERCONTROL_CT_CLASS_FADER,
    MIXERCONTROL_CONTROLTYPE_VOLUME,
    MIXERCONTROL_CONTROLTYPE_BASS,
    MIXERCONTROL_CONTROLTYPE_TREBLE,
    MIXERCONTROL_CONTROLTYPE_EQUALIZER,
    MIXERCONTROL_CONTROLTYPE_FADER,
    MIXERCONTROL_CT_CLASS_LIST,
    MIXERCONTROL_CONTROLTYPE_SINGLESELECT,
    MIXERCONTROL_CONTROLTYPE_MULTIPLESELECT,
    MIXERCONTROL_CONTROLTYPE_MUX,
    MIXERCONTROL_CONTROLTYPE_MIXER,
    MIXERCONTROL_CT_CLASS_METER,
    MIXERCONTROL_CONTROLTYPE_BOOLEANMETER,
    MIXERCONTROL_CONTROLTYPE_PEAKMETER,
    MIXERCONTROL_CONTROLTYPE_SIGNEDMETER,
    MIXERCONTROL_CONTROLTYPE_UNSIGNEDMETER,
    MIXERCONTROL_CT_CLASS_NUMBER,
    MIXERCONTROL_CONTROLTYPE_SIGNED,
    MIXERCONTROL_CONTROLTYPE_UNSIGNED,
    MIXERCONTROL_CONTROLTYPE_PERCENT,
    MIXERCONTROL_CONTROLTYPE_DECIBELS,
    MIXERCONTROL_CT_CLASS_SLIDER,
    MIXERCONTROL_CONTROLTYPE_SLIDER,
    MIXERCONTROL_CONTROLTYPE_PAN,
    MIXERCONTROL_CONTROLTYPE_QSOUNDPAN,
    MIXERCONTROL_CT_CLASS_SWITCH,
    MIXERCONTROL_CONTROLTYPE_BOOLEAN,
    MIXERCONTROL_CONTROLTYPE_BUTTON,
    MIXERCONTROL_CONTROLTYPE_LOUDNESS,
    MIXERCONTROL_CONTROLTYPE_MONO,
    MIXERCONTROL_CONTROLTYPE_MUTE,
    MIXERCONTROL_CONTROLTYPE_ONOFF,
    MIXERCONTROL_CONTROLTYPE_STEREOENH,
    MIXERCONTROL_CT_CLASS_TIME,
    MIXERCONTROL_CONTROLTYPE_MICROTIME,
    MIXERCONTROL_CONTROLTYPE_MILLITIME,
    MIXERCONTROL_CT_CLASS_CUSTOM,
    
    MIXERCONTROL_CONTROLF_DISABLED,
    MIXERCONTROL_CONTROLF_MULTIPLE,
    MIXERCONTROL_CONTROLF_UNIFORM,
)

            
MIXER_CONTROL_CLASSES = {
    MIXERCONTROL_CT_CLASS_FADER: {
        "name": "Fader",
        "types": {
            MIXERCONTROL_CONTROLTYPE_VOLUME: "Volume",
            MIXERCONTROL_CONTROLTYPE_BASS: "Bass",
            MIXERCONTROL_CONTROLTYPE_TREBLE: "Treble",
            MIXERCONTROL_CONTROLTYPE_EQUALIZER: "Equalizer",
            MIXERCONTROL_CONTROLTYPE_FADER: "Generic Fader",
        }
    },
    MIXERCONTROL_CT_CLASS_LIST: {
        "name": "List",
        "types": {
            MIXERCONTROL_CONTROLTYPE_SINGLESELECT: "Single Select",
            MIXERCONTROL_CONTROLTYPE_MULTIPLESELECT: "Multiple Select",
            MIXERCONTROL_CONTROLTYPE_MUX: "Mux",
            MIXERCONTROL_CONTROLTYPE_MIXER: "Mixer",
        }
    },
    MIXERCONTROL_CT_CLASS_METER: {
        "name": "Meter",
        "types": {
            MIXERCONTROL_CONTROLTYPE_BOOLEANMETER: "Boolean Meter",
            MIXERCONTROL_CONTROLTYPE_PEAKMETER: "Peak Meter",
            MIXERCONTROL_CONTROLTYPE_SIGNEDMETER: "Signed Meter",
            MIXERCONTROL_CONTROLTYPE_UNSIGNEDMETER: "Unsigned Meter",
        }
    },
    MIXERCONTROL_CT_CLASS_NUMBER: {
        "name": "Numeric",
        "types": {
            MIXERCONTROL_CONTROLTYPE_SIGNED: "Signed",
            MIXERCONTROL_CONTROLTYPE_UNSIGNED: "Unsigned",
            MIXERCONTROL_CONTROLTYPE_PERCENT: "Percent",
            MIXERCONTROL_CONTROLTYPE_DECIBELS: "Decibels",
        }
    },
    MIXERCONTROL_CT_CLASS_SLIDER: {
        "name": "Slider",
        "types": {
            MIXERCONTROL_CONTROLTYPE_SLIDER: "Slider",
            MIXERCONTROL_CONTROLTYPE_PAN: "Pan",
            MIXERCONTROL_CONTROLTYPE_QSOUNDPAN: "Qsound Pan",
        }
    },
    MIXERCONTROL_CT_CLASS_SWITCH: {
        "name": "Switch",
        "types": {
            MIXERCONTROL_CONTROLTYPE_BOOLEAN: "Boolean",
            MIXERCONTROL_CONTROLTYPE_BUTTON: "Button",
            MIXERCONTROL_CONTROLTYPE_LOUDNESS: "Loudness",
            MIXERCONTROL_CONTROLTYPE_MONO: "Mono",
            MIXERCONTROL_CONTROLTYPE_MUTE: "Mute",
            MIXERCONTROL_CONTROLTYPE_ONOFF: "OnOff",
            MIXERCONTROL_CONTROLTYPE_STEREOENH: "Stereo Enhance"
        }
    },
    MIXERCONTROL_CT_CLASS_TIME: {
        "name": "Time",
        "types": {
            MIXERCONTROL_CONTROLTYPE_MICROTIME: "Microseconds",
            MIXERCONTROL_CONTROLTYPE_MILLITIME: "Milliseconds",
        }
    },
    MIXERCONTROL_CT_CLASS_CUSTOM: {
        "name": "CUSTOM",
        "types": {
        }
    },
}

def GetControls(hmixer, mixerline):
    numCtrls = mixerline.cControls
    if numCtrls == 0:
        return []
    mixerControlArray = (MIXERCONTROL * numCtrls)()
    mixerLineControls = MIXERLINECONTROLS()
    mixerLineControls.cbStruct = sizeof(MIXERLINECONTROLS)
    mixerLineControls.cControls = numCtrls
    mixerLineControls.dwLineID = mixerline.dwLineID
    mixerLineControls.pamxctrl = pointer(mixerControlArray[0])
    mixerLineControls.cbmxctrl = sizeof(MIXERCONTROL)
    mixerGetLineControls(hmixer, byref(mixerLineControls), MIXER_GETLINECONTROLSF_ALL)
    result = []
    for i in range(numCtrls):
        mixerControl = mixerControlArray[i]
        dwControlType = mixerControl.dwControlType
        controlClass = MIXER_CONTROL_CLASSES[dwControlType & MIXERCONTROL_CT_CLASS_MASK]
        controlClassTypeName = controlClass["types"][dwControlType]
        flagNames = []
        fdwControl =  mixerControl.fdwControl
        if fdwControl & MIXERCONTROL_CONTROLF_DISABLED:
            flagNames.append("Disabled")
        if fdwControl & MIXERCONTROL_CONTROLF_MULTIPLE:
            flagNames.append("Multiple(%i)" % mixerControl.cMultipleItems)
        if fdwControl & MIXERCONTROL_CONTROLF_UNIFORM:
            flagNames.append("Uniform")
        result.append(
            (
                mixerControl.szName.decode("mbcs"), 
                controlClass["name"], 
                controlClassTypeName,
                ", ".join(flagNames)
            )
        )
    return result
    

def GetControlDetails():
    pass
    
#print GetDeviceLines()


        
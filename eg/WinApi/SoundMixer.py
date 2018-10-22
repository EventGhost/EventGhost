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

# Local imports
from Dynamic.Mmsystem import (
    addressof,
    byref,
    HMIXER,
    MIXER_GETLINECONTROLSF_ALL,
    MIXER_GETLINECONTROLSF_ONEBYTYPE,
    MIXER_GETLINEINFOF_COMPONENTTYPE,
    MIXER_GETLINEINFOF_DESTINATION,
    MIXER_GETLINEINFOF_SOURCE,
    MIXERCAPS,
    MIXERCONTROL,
    MIXERCONTROL_CONTROLF_DISABLED,
    MIXERCONTROL_CONTROLF_MULTIPLE,
    MIXERCONTROL_CONTROLF_UNIFORM,
    MIXERCONTROL_CONTROLTYPE_BASS,
    MIXERCONTROL_CONTROLTYPE_BOOLEAN,
    MIXERCONTROL_CONTROLTYPE_BOOLEANMETER,
    MIXERCONTROL_CONTROLTYPE_BUTTON,
    MIXERCONTROL_CONTROLTYPE_DECIBELS,
    MIXERCONTROL_CONTROLTYPE_EQUALIZER,
    MIXERCONTROL_CONTROLTYPE_FADER,
    MIXERCONTROL_CONTROLTYPE_LOUDNESS,
    MIXERCONTROL_CONTROLTYPE_MICROTIME,
    MIXERCONTROL_CONTROLTYPE_MILLITIME,
    MIXERCONTROL_CONTROLTYPE_MIXER,
    MIXERCONTROL_CONTROLTYPE_MONO,
    MIXERCONTROL_CONTROLTYPE_MULTIPLESELECT,
    MIXERCONTROL_CONTROLTYPE_MUTE,
    MIXERCONTROL_CONTROLTYPE_MUX,
    MIXERCONTROL_CONTROLTYPE_ONOFF,
    MIXERCONTROL_CONTROLTYPE_PAN,
    MIXERCONTROL_CONTROLTYPE_PEAKMETER,
    MIXERCONTROL_CONTROLTYPE_PERCENT,
    MIXERCONTROL_CONTROLTYPE_QSOUNDPAN,
    MIXERCONTROL_CONTROLTYPE_SIGNED,
    MIXERCONTROL_CONTROLTYPE_SIGNEDMETER,
    MIXERCONTROL_CONTROLTYPE_SINGLESELECT,
    MIXERCONTROL_CONTROLTYPE_SLIDER,
    MIXERCONTROL_CONTROLTYPE_STEREOENH,
    MIXERCONTROL_CONTROLTYPE_TREBLE,
    MIXERCONTROL_CONTROLTYPE_UNSIGNED,
    MIXERCONTROL_CONTROLTYPE_UNSIGNEDMETER,
    MIXERCONTROL_CONTROLTYPE_VOLUME,
    MIXERCONTROL_CT_CLASS_CUSTOM,
    MIXERCONTROL_CT_CLASS_FADER,
    MIXERCONTROL_CT_CLASS_LIST,
    MIXERCONTROL_CT_CLASS_MASK,
    MIXERCONTROL_CT_CLASS_METER,
    MIXERCONTROL_CT_CLASS_NUMBER,
    MIXERCONTROL_CT_CLASS_SLIDER,
    MIXERCONTROL_CT_CLASS_SWITCH,
    MIXERCONTROL_CT_CLASS_TIME,
    MIXERCONTROLDETAILS,
    MIXERCONTROLDETAILS_UNSIGNED,
    mixerGetControlDetails,
    mixerGetDevCaps,
    mixerGetLineControls,
    mixerGetLineInfo,
    mixerGetNumDevs,
    MIXERLINE,
    MIXERLINE_COMPONENTTYPE_DST_SPEAKERS,
    MIXERLINECONTROLS,
    mixerOpen,
    mixerSetControlDetails,
    MMSYSERR_NOERROR,
    pointer,
    sizeof,
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

# Exceptions
class SoundMixerException(Exception):
    pass

def ChangeMasterVolumeBy(value, deviceId=0):

    if eg.WindowsVersion >= 'Vista':
        minimum = 0
        maximum = 100.0

    else:
        hmixer, mixerControl = GetMixerControl(
            MIXERLINE_COMPONENTTYPE_DST_SPEAKERS,
            MIXERCONTROL_CONTROLTYPE_VOLUME,
            deviceId
        )

        minimum = mixerControl.Bounds.lMinimum
        maximum = mixerControl.Bounds.lMaximum

    oldVolume = GetMasterVolume(deviceId)
    newVolume = int(round((maximum - minimum) * value / 100.0)) + oldVolume

    if newVolume < minimum:
        newVolume = minimum
    elif newVolume > maximum:
        newVolume = maximum

    return SetMasterVolume(newVolume, deviceId)

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
    mixerGetLineControls(
        hmixer, byref(mixerLineControls), MIXER_GETLINECONTROLSF_ALL
    )
    result = []
    for i in range(numCtrls):
        mixerControl = mixerControlArray[i]
        dwControlType = mixerControl.dwControlType
        controlClass = MIXER_CONTROL_CLASSES[
            dwControlType & MIXERCONTROL_CT_CLASS_MASK
        ]
        controlClassTypeName = controlClass["types"][dwControlType]
        flagNames = []
        fdwControl = mixerControl.fdwControl
        if fdwControl & MIXERCONTROL_CONTROLF_DISABLED:
            flagNames.append("Disabled")
        if fdwControl & MIXERCONTROL_CONTROLF_MULTIPLE:
            flagNames.append("Multiple(%i)" % mixerControl.cMultipleItems)
        if fdwControl & MIXERCONTROL_CONTROLF_UNIFORM:
            flagNames.append("Uniform")
        result.append(
            (
                mixerControl.szName,
                controlClass["name"],
                controlClassTypeName,
                ", ".join(flagNames)
            )
        )
    return result

def GetControlDetails():
    pass

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

def GetDeviceId(deviceId, strVal=False):
    if strVal and deviceId == "Primary Sound Driver":
        deviceId = 0
    if isinstance(deviceId, int):
        if strVal:
            devices = GetMixerDevices()

            if -1 < deviceId < len(devices) - 1:
                return devices[deviceId]
            else:
                # return devices[0]
                raise SoundMixerException()
        else:
            return deviceId
    else:
        deviceId = deviceId[:31]
        devices = GetMixerDevices(True)
        if deviceId in devices:
            if strVal:
                return deviceId
            else:
                return devices.index(deviceId) - 1
        else:
            #return 0
            raise SoundMixerException()

def GetDeviceLines(deviceId=0):
    deviceId = GetDeviceId(deviceId)
    mixercaps = MIXERCAPS()
    mixerline = MIXERLINE()
    hmixer = HMIXER()

    # Obtain the hmixer struct
    rc = mixerOpen(byref(hmixer), deviceId, 0, 0, 0)
    if rc != MMSYSERR_NOERROR:
        raise SoundMixerException()

    if mixerGetDevCaps(deviceId, byref(mixercaps), sizeof(MIXERCAPS)):
        raise SoundMixerException()

    for destinationNum in range(mixercaps.cDestinations):
        mixerline.cbStruct = sizeof(MIXERLINE)
        mixerline.dwDestination = destinationNum
        if mixerGetLineInfo(
            hmixer, byref(mixerline), MIXER_GETLINEINFOF_DESTINATION
        ):
            continue
        print "Destination:", destinationNum, mixerline.szName
        for name in GetControls(hmixer, mixerline):
            print "        Control:", name
        for sourceNum in range(mixerline.cConnections):
            mixerline.cbStruct = sizeof(MIXERLINE)
            mixerline.dwDestination = destinationNum
            mixerline.dwSource = sourceNum
            if mixerGetLineInfo(
                hmixer, byref(mixerline), MIXER_GETLINEINFOF_SOURCE
            ):
                continue
            print "    Source:", sourceNum, mixerline.szName
            for name in GetControls(hmixer, mixerline):
                print "            Control:", name

def GetMasterVolume(deviceId=0):
    import eg

    if eg.WindowsVersion >= 'Vista':
        deviceId = GetDeviceId(deviceId, True)

        import VistaVolEvents

        value = VistaVolEvents.GetMasterVolume(deviceId) * 100.0

    else:
        deviceId = GetDeviceId(deviceId)
        # Obtain the volumne control object
        hmixer, mixerControl = GetMixerControl(
            MIXERLINE_COMPONENTTYPE_DST_SPEAKERS,
            MIXERCONTROL_CONTROLTYPE_VOLUME,
            deviceId
        )

        # Then get the volume
        value = GetControlValue(hmixer, mixerControl)

        maximum = mixerControl.Bounds.lMaximum
        minimum = mixerControl.Bounds.lMinimum
        value = 100.0 * (value - minimum) / (maximum - minimum)

    return value

def GetMixerControl(componentType, ctrlType, deviceId=0):
    """
    Obtains an appropriate pointer and info for the volume control
    This function attempts to obtain a mixer control. Raises
    SoundMixerException if not successful.
    """
    deviceId = GetDeviceId(deviceId)
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

def GetMixerDevices(useList=False):
    """
    Returns a list of all mixer device names available on the system.
    """
    mixcaps = MIXERCAPS()
    result = []
    # get the number of Mixer devices in this computer
    result.append("Primary Sound Driver")
    for i in range(mixerGetNumDevs()):
        # get info about the device
        if mixerGetDevCaps(i, byref(mixcaps), sizeof(MIXERCAPS)):
            continue
        # store the name of the device
        result.append(mixcaps.szPname)
    return result if useList else dict((i - 1, result[i]) for i in range(len(result)))

def GetMute(deviceId=0):
    import eg

    if eg.WindowsVersion >= 'Vista':
        deviceId = GetDeviceId(deviceId, True)

        import VistaVolEvents

        return VistaVolEvents.GetMute(deviceId)

    else:
        deviceId = GetDeviceId(deviceId)
        # Obtain the volumne control object
        hmixer, mixerControl = GetMixerControl(
            MIXERLINE_COMPONENTTYPE_DST_SPEAKERS,
            MIXERCONTROL_CONTROLTYPE_MUTE,
            deviceId
        )

        # Then get the volume
        return GetControlValue(hmixer, mixerControl)

def SetControlValue(hmixer, mixerControl, value):
    """
    Sets the volumne from the pointer of the object passed through

    ' [Note: original source taken from MSDN
    http://support.microsoft.com/default.aspx?scid=KB;EN-US;Q178456&]

    This function sets the value for a volume control. Returns True if
    successful
    """
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

def SetMasterVolume(value, deviceId=0):
    import eg

    if eg.WindowsVersion >= 'Vista':
        deviceId = GetDeviceId(deviceId, True)

        import VistaVolEvents

        value = float(value) / 100.0
        if value > 1.0:
            newValue = 1.0
        elif value < 0.0:
            newValue = 0.0
        else:
            newValue = value

        VistaVolEvents.SetMasterVolume(newValue, deviceId)
        # eg.Utils.time.sleep(0.5)

    else:
        deviceId = GetDeviceId(deviceId)
        # Obtain the volumne control object
        hmixer, volCtrl = GetMixerControl(
            MIXERLINE_COMPONENTTYPE_DST_SPEAKERS,
            MIXERCONTROL_CONTROLTYPE_VOLUME,
            deviceId
        )

        maximum = volCtrl.Bounds.lMaximum
        minimum = volCtrl.Bounds.lMinimum
        newValue = int((value / 100.0) * (maximum - minimum)) + minimum
        if newValue < minimum:
            newValue = minimum
        elif newValue > maximum:
            newValue = maximum
        SetControlValue(hmixer, volCtrl, newValue)

    try:
        return GetMasterVolume(deviceId)
    except:
        return newValue


def SetMute(mute=True, deviceId=0):
    import eg

    if eg.WindowsVersion >= 'Vista':
        deviceId = GetDeviceId(deviceId, True)

        import VistaVolEvents

        VistaVolEvents.SetMute(int(mute), deviceId)

    else:
        deviceId = GetDeviceId(deviceId)
        # Obtain the volumne control object
        deviceId = GetDeviceId(deviceId)
        hmixer, mixerControl = GetMixerControl(
            MIXERLINE_COMPONENTTYPE_DST_SPEAKERS,
            MIXERCONTROL_CONTROLTYPE_MUTE,
            deviceId
        )

        # Then set the volume
        SetControlValue(hmixer, mixerControl, int(mute))

    return GetMute(deviceId)

def ToggleMute(deviceId=0):
    flag = not GetMute(deviceId)
    SetMute(flag, deviceId)
    return flag

if __name__ == '__main__':
    print GetDeviceLines()

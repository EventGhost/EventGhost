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

import wx

# Local imports
from eg.WinApi.Dynamic.Mmsystem import (
    byref,
    c_void_p,
    cast,
    HMIXER,
    MIXER_GETCONTROLDETAILSF_LISTTEXT,
    MIXER_GETCONTROLDETAILSF_VALUE,
    MIXER_GETLINECONTROLSF_ALL,
    MIXER_GETLINECONTROLSF_ONEBYID,
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
    MIXERCONTROL_CONTROLTYPE_CUSTOM,
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
    MIXERCONTROLDETAILS_BOOLEAN,
    MIXERCONTROLDETAILS_LISTTEXT,
    MIXERCONTROLDETAILS_SIGNED,
    MIXERCONTROLDETAILS_UNSIGNED,
    mixerGetControlDetails,
    mixerGetDevCaps,
    mixerGetLineControls,
    mixerGetLineInfo,
    MIXERLINE,
    MIXERLINECONTROLS,
    mixerOpen,
    MMSYSERR_NOERROR,
    pointer,
    sizeof,
)
from eg.WinApi.SoundMixer import SoundMixerException

MCD_UNSIGNED = MIXERCONTROLDETAILS_UNSIGNED
MCD_SIGNED = MIXERCONTROLDETAILS_SIGNED
MCD_BOOLEAN = MIXERCONTROLDETAILS_BOOLEAN

MIXERCONTROLDETAILS_NAMES = {
    MCD_UNSIGNED: "Unsigned",
    MCD_SIGNED: "Signed",
    MCD_BOOLEAN: "Boolean",
}

CONTROLTYPES = {
    #MIXERCONTROL_CT_CLASS_FADER
    MIXERCONTROL_CONTROLTYPE_VOLUME: ("Volume", MCD_UNSIGNED),
    MIXERCONTROL_CONTROLTYPE_BASS: ("Bass", MCD_UNSIGNED),
    MIXERCONTROL_CONTROLTYPE_TREBLE: ("Treble", MCD_UNSIGNED),
    MIXERCONTROL_CONTROLTYPE_EQUALIZER: ("Equalizer", MCD_UNSIGNED),
    MIXERCONTROL_CONTROLTYPE_FADER: ("Generic Fader", MCD_UNSIGNED),

    #MIXERCONTROL_CT_CLASS_LIST
    MIXERCONTROL_CONTROLTYPE_SINGLESELECT: ("Single Select", MCD_BOOLEAN),
    MIXERCONTROL_CONTROLTYPE_MULTIPLESELECT: ("Multiple Select", MCD_BOOLEAN),
    MIXERCONTROL_CONTROLTYPE_MUX: ("Mux", MCD_BOOLEAN),
    MIXERCONTROL_CONTROLTYPE_MIXER: ("Mixer", MCD_BOOLEAN),

    #MIXERCONTROL_CT_CLASS_METER
    MIXERCONTROL_CONTROLTYPE_BOOLEANMETER: ("Boolean Meter", MCD_BOOLEAN),
    MIXERCONTROL_CONTROLTYPE_PEAKMETER: ("Peak Meter", MCD_SIGNED),
    MIXERCONTROL_CONTROLTYPE_SIGNEDMETER: ("Signed Meter", MCD_SIGNED),
    MIXERCONTROL_CONTROLTYPE_UNSIGNEDMETER: ("Unsigned Meter", MCD_UNSIGNED),

    #MIXERCONTROL_CT_CLASS_NUMBER
    MIXERCONTROL_CONTROLTYPE_SIGNED: ("Signed", MCD_SIGNED),
    MIXERCONTROL_CONTROLTYPE_UNSIGNED: ("Unsigned", MCD_UNSIGNED),
    MIXERCONTROL_CONTROLTYPE_PERCENT: ("Percent", MCD_UNSIGNED),
    MIXERCONTROL_CONTROLTYPE_DECIBELS: ("Decibels", MCD_SIGNED),

    #MIXERCONTROL_CT_CLASS_SLIDER
    MIXERCONTROL_CONTROLTYPE_SLIDER: ("Slider", MCD_SIGNED),
    MIXERCONTROL_CONTROLTYPE_PAN: ("Pan", MCD_SIGNED),
    MIXERCONTROL_CONTROLTYPE_QSOUNDPAN: ("Qsound Pan", MCD_SIGNED),

    #MIXERCONTROL_CT_CLASS_SWITCH
    MIXERCONTROL_CONTROLTYPE_BOOLEAN: ("Boolean", MCD_BOOLEAN),
    MIXERCONTROL_CONTROLTYPE_BUTTON: ("Button", MCD_BOOLEAN),
    MIXERCONTROL_CONTROLTYPE_LOUDNESS: ("Loudness", MCD_BOOLEAN),
    MIXERCONTROL_CONTROLTYPE_MONO: ("Mono", MCD_BOOLEAN),
    MIXERCONTROL_CONTROLTYPE_MUTE: ("Mute", MCD_BOOLEAN),
    MIXERCONTROL_CONTROLTYPE_ONOFF: ("OnOff", MCD_BOOLEAN),
    MIXERCONTROL_CONTROLTYPE_STEREOENH: ("Stereo Enhance", MCD_BOOLEAN),

    #MIXERCONTROL_CT_CLASS_TIME
    MIXERCONTROL_CONTROLTYPE_MICROTIME: "Microseconds",
    MIXERCONTROL_CONTROLTYPE_MILLITIME: "Milliseconds",
}

MIXER_CONTROL_CLASSES = {
    MIXERCONTROL_CT_CLASS_FADER: {
        "name": "Fader",
        "types": {
            MIXERCONTROL_CONTROLTYPE_VOLUME: "Volume",
            MIXERCONTROL_CONTROLTYPE_BASS: "Bass",
            MIXERCONTROL_CONTROLTYPE_TREBLE: "Treble",
            MIXERCONTROL_CONTROLTYPE_EQUALIZER: "Equalizer",
            MIXERCONTROL_CONTROLTYPE_FADER: "Generic Fader",
        },
        "valueType": MCD_UNSIGNED,
    },
    MIXERCONTROL_CT_CLASS_LIST: {
        "name": "List",
        "types": {
            MIXERCONTROL_CONTROLTYPE_SINGLESELECT: "Single Select",
            MIXERCONTROL_CONTROLTYPE_MULTIPLESELECT: "Multiple Select",
            MIXERCONTROL_CONTROLTYPE_MUX: "Mux",
            MIXERCONTROL_CONTROLTYPE_MIXER: "Mixer",
        },
        "valueType": MCD_BOOLEAN,
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
        "name": "Custom",
        "types": {
        }
    },
}

class SoundMixerTree(wx.TreeCtrl):
    def __init__(self, parent, panel, *args, **kwargs):
        self.deviceId = 0
        self.panel = panel
        wx.TreeCtrl.__init__(self, parent, *args, **kwargs)
        self.FillTree()
        self.ExpandAll()
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)

    def AddControls(self, parentItem, mixerline):
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
            self.mixerHandle,
            byref(mixerLineControls),
            MIXER_GETLINECONTROLSF_ALL
        )
        for i in range(numCtrls):
            mixerControl = mixerControlArray[i]
            ctrlItem = self.AppendItem(
                parentItem,
                mixerControl.szName
            )
            self.SetPyData(ctrlItem, mixerControl.dwControlID)

    def FillTree(self):
        root = self.AddRoot("Sound Card")
        mixercaps = MIXERCAPS()
        mixerline = MIXERLINE()
        self.mixerHandle = mixerHandle = HMIXER()

        # Obtain the hmixer struct
        rc = mixerOpen(byref(mixerHandle), self.deviceId, 0, 0, 0)
        if rc != MMSYSERR_NOERROR:
            raise SoundMixerException()

        if mixerGetDevCaps(mixerHandle, byref(mixercaps), sizeof(MIXERCAPS)):
            raise SoundMixerException()

        for i in range(mixercaps.cDestinations):
            mixerline.cbStruct = sizeof(MIXERLINE)
            mixerline.dwDestination = i
            if mixerGetLineInfo(
                mixerHandle, byref(mixerline), MIXER_GETLINEINFOF_DESTINATION
            ):
                continue
            destItem = self.AppendItem(
                root, mixerline.szName + ": %i" % mixerline.cChannels
            )
            self.AddControls(destItem, mixerline)
            for n in range(mixerline.cConnections):
                mixerline.cbStruct = sizeof(MIXERLINE)
                mixerline.dwDestination = i
                mixerline.dwSource = n
                if mixerGetLineInfo(
                    mixerHandle, byref(mixerline), MIXER_GETLINEINFOF_SOURCE
                ):
                    continue
                sourceItem = self.AppendItem(
                    destItem,
                    mixerline.szName + ": %i" % mixerline.cChannels
                )
                self.AddControls(sourceItem, mixerline)

    def OnSelectionChanged(self, event):
        dwControlID = self.GetPyData(event.GetItem())
        panel = self.panel
        panel.DestroyChildren()
        sizer = wx.BoxSizer(wx.VERTICAL)

        idCtrl = wx.StaticText(panel, -1, "ID: " + str(dwControlID))
        sizer.Add(idCtrl)
        if dwControlID is None:
            panel.SetSizerAndFit(sizer)
            return

        mixerControl = MIXERCONTROL()
        mixerLineControls = MIXERLINECONTROLS()
        mixerLineControls.cbStruct = sizeof(MIXERLINECONTROLS)
        mixerLineControls.cControls = 1
        mixerLineControls.dwControlID = dwControlID
        mixerLineControls.pamxctrl = pointer(mixerControl)
        mixerLineControls.cbmxctrl = sizeof(MIXERCONTROL)
        err = mixerGetLineControls(
            self.mixerHandle,
            byref(mixerLineControls),
            MIXER_GETLINECONTROLSF_ONEBYID
        )
        if err:
            print "error", err
            return

        idCtrl = wx.StaticText(panel, -1, "Name: " + mixerControl.szName)
        sizer.Add(idCtrl)

        idCtrl = wx.StaticText(
            panel, -1, "Short Name: " + mixerControl.szShortName
        )
        sizer.Add(idCtrl)

        dwControlType = mixerControl.dwControlType

        controlClass = MIXER_CONTROL_CLASSES[
            dwControlType & MIXERCONTROL_CT_CLASS_MASK
        ]
        idCtrl = wx.StaticText(
            panel, -1, "Classification: " + controlClass["name"]
        )
        sizer.Add(idCtrl)

        controlClassTypeName = controlClass["types"][dwControlType]
        idCtrl = wx.StaticText(panel, -1, "Type: " + controlClassTypeName)
        sizer.Add(idCtrl)

        fdwControl = mixerControl.fdwControl
        cMultipleItems = 0
        numMultipleItems = 1
        flagNames = []
        if fdwControl & MIXERCONTROL_CONTROLF_DISABLED:
            flagNames.append("Disabled")
        if fdwControl & MIXERCONTROL_CONTROLF_MULTIPLE:
            flagNames.append("Multiple(%i)" % mixerControl.cMultipleItems)
            numMultipleItems = mixerControl.cMultipleItems
            cMultipleItems = mixerControl.cMultipleItems
        if fdwControl & MIXERCONTROL_CONTROLF_UNIFORM:
            flagNames.append("Uniform")
        idCtrl = wx.StaticText(panel, -1, "Flags: " + ", ".join(flagNames))
        sizer.Add(idCtrl)

        valueType = CONTROLTYPES[dwControlType][1]
        valueTypeName = MIXERCONTROLDETAILS_NAMES[valueType]
        idCtrl = wx.StaticText(panel, -1, "Value Type: " + valueTypeName)
        sizer.Add(idCtrl)

        if dwControlType == MIXERCONTROL_CONTROLTYPE_CUSTOM:
            cChannels = 0
        elif fdwControl & MIXERCONTROL_CONTROLF_UNIFORM:
            cChannels = 1
        else:
            # TODO: Get the number of channels
            cChannels = 2
        details = (valueType * (cChannels * numMultipleItems))()
        mixerControlDetails = MIXERCONTROLDETAILS()
        mixerControlDetails.cbStruct = sizeof(MIXERCONTROLDETAILS)
        mixerControlDetails.dwControlID = dwControlID
        mixerControlDetails.cChannels = cChannels
        mixerControlDetails.cMultipleItems = cMultipleItems
        mixerControlDetails.cbDetails = sizeof(details)
        mixerControlDetails.paDetails = cast(pointer(details), c_void_p)
        valueType()
        mixerGetControlDetails(
            self.mixerHandle,
            byref(mixerControlDetails),
            MIXER_GETCONTROLDETAILSF_VALUE
        )
        values = []
        for i in range(cChannels * numMultipleItems):
            if valueType == MCD_BOOLEAN:
                values.append(details[i].fValue)
            elif valueType == MCD_SIGNED:
                values.append(details[i].lValue)
            elif valueType == MCD_UNSIGNED:
                values.append(details[i].dwValue)

        idCtrl = wx.StaticText(panel, -1, "Value: %r" % values)
        sizer.Add(idCtrl)

        if (
            dwControlType & MIXERCONTROL_CT_CLASS_MASK ==
            MIXERCONTROL_CT_CLASS_LIST
        ):
            labels = (
                MIXERCONTROLDETAILS_LISTTEXT * (cChannels * numMultipleItems)
            )()
            mixerControlDetails.cbDetails = sizeof(
                MIXERCONTROLDETAILS_LISTTEXT
            )
            mixerControlDetails.paDetails = cast(pointer(labels), c_void_p)
            mixerGetControlDetails(
                self.mixerHandle,
                byref(mixerControlDetails),
                MIXER_GETCONTROLDETAILSF_LISTTEXT
            )
            for i in range(cChannels * numMultipleItems):
                print labels[i].szName
        panel.SetSizerAndFit(sizer)

eg.RegisterPlugin(
    name = "Sound Mixer Ex",
    author = "Dexter",
    version = "1.1.1204",
    description = (
        "This plugin allows you to set virtually any control available on "
        "your soundcard.\n\n<p>"
        "Doesn't work under Windows Vista currently.</p>"
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=748",
    kind = "other",
    guid = "{B619678F-0C6F-425E-9240-3ADA82360DD2}",
)

# changelog
# 1.1.x bitmonster
#     - removed mbcs decoding everywhere, because eg.WinApi.Dynamic now uses the
#       unicode versions of all functions as default.
#     - root node of tree now starts expanded.


from eg.WinApi.Dynamic.Mmsystem import (
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
    #MIXER_GETLINECONTROLSF_ONEBYID,
    MIXER_GETLINECONTROLSF_ALL,
    MIXER_GETLINEINFOF_DESTINATION,
    MIXER_GETLINEINFOF_SOURCE,
    MMSYSERR_NOERROR,

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



class SoundMixerWin32():

    #def __init__(self):
        # Nothing to do here yet

    def GetMixer(self, deviceId):
        hmixer = HMIXER()
        rc = mixerOpen(byref(hmixer), deviceId, 0, 0, 0)
        if rc != MMSYSERR_NOERROR:
            raise SoundMixerException()
        return hmixer


    def GetControl(self, mixer, controlId):
        mixerControl = MIXERCONTROL()
        mixerControl.cbStruct = sizeof(MIXERCONTROL)
        mixerLineControls = MIXERLINECONTROLS()
        mixerLineControls.cbStruct = sizeof(MIXERLINECONTROLS)

        mixerLineControls.dwControlID = controlId
        mixerLineControls.cControls = 1
        mixerLineControls.cbmxctrl = sizeof(mixerControl)
        mixerLineControls.pamxctrl = pointer(mixerControl)

        rc = mixerGetLineControls(mixer, byref(mixerLineControls), 1) #MIXER_GETLINECONTROLSF_ONEBYID
        if MMSYSERR_NOERROR != rc:
            raise SoundMixerException()
        return mixerControl


    def GetControlValue(self, mixer, controlId):
        valueDetails = MIXERCONTROLDETAILS_UNSIGNED()

        mixerControlDetails = MIXERCONTROLDETAILS()
        mixerControlDetails.cbStruct = sizeof(MIXERCONTROLDETAILS)
        mixerControlDetails.item = 0
        mixerControlDetails.dwControlID = controlId
        mixerControlDetails.cbDetails = sizeof(valueDetails)
        mixerControlDetails.paDetails = addressof(valueDetails)
        mixerControlDetails.cChannels = 1

        rc = mixerGetControlDetails(mixer, byref(mixerControlDetails), 0)
        if rc != MMSYSERR_NOERROR:
            raise SoundMixerException()
        return valueDetails.dwValue


    def SetControlValue(self, mixer, controlId, value):
        valueDetails = MIXERCONTROLDETAILS_UNSIGNED()
        valueDetails.dwValue = value

        mixerControlDetails = MIXERCONTROLDETAILS()
        mixerControlDetails.cbStruct = sizeof(MIXERCONTROLDETAILS)
        mixerControlDetails.item = 0
        mixerControlDetails.dwControlID = controlId
        mixerControlDetails.cbDetails = sizeof(valueDetails)
        mixerControlDetails.paDetails = addressof(valueDetails)
        mixerControlDetails.cChannels = 1

        rc = mixerSetControlDetails(mixer, byref(mixerControlDetails), 0)
        if rc != MMSYSERR_NOERROR:
            raise SoundMixerException()


    def GetSwitchValue(self, deviceId, controlId):
        mixer = self.GetMixer(deviceId)
        value = self.GetControlValue(mixer, controlId)
        if value != 0:
            return True
        else:
            return False


    def SetSwitchValue(self, deviceId, controlId, value):
        mixer = self.GetMixer(deviceId)
        if value:
            value = 1
        else:
            value = 0
        self.SetControlValue(mixer, controlId, value)


    def GetFaderValue(self, deviceId, controlId):
        mixer = self.GetMixer(deviceId)
        control = self.GetControl(mixer, controlId)
        value = self.GetControlValue(mixer, controlId)
        max = control.Bounds.lMaximum
        min = control.Bounds.lMinimum
        value = 100.0 * (value - min) / (max - min)
        return value


    def SetFaderValue(self, deviceId, controlId, value):
        mixer = self.GetMixer(deviceId)
        control = self.GetControl(mixer, controlId)
        max = control.Bounds.lMaximum
        min = control.Bounds.lMinimum
        value = int((value / 100.0) * (max - min)) + min
        if value < min:
            value = min
        elif value > max:
            value = max
        self.SetControlValue(mixer, controlId, value)


    def GetMixerDevices(self):
        mixcaps = MIXERCAPS()
        result = []
        for i in range(mixerGetNumDevs()):
            if mixerGetDevCaps(i, byref(mixcaps), sizeof(MIXERCAPS)):
                continue
            result.append((i, mixcaps.szPname))
        return result


    def GetDeviceLines(self, deviceId=0):
        mixercaps = MIXERCAPS()
        mixerline = MIXERLINE()
        result = []

        hmixer = self.GetMixer(deviceId)
        if mixerGetDevCaps(hmixer, byref(mixercaps), sizeof(MIXERCAPS)):
            raise SoundMixerException()

        for i in range(mixercaps.cDestinations):
            mixerline.cbStruct = sizeof(MIXERLINE)
            mixerline.dwDestination = i
            if mixerGetLineInfo(hmixer, byref(mixerline), MIXER_GETLINEINFOF_DESTINATION):
                continue

            destination = mixerline.szName

            for control in self.GetControls(hmixer, mixerline):
                result.append((control[0], destination, None, control[1], control[2], control[3]))

            for n in range(mixerline.cConnections):
                mixerline.cbStruct = sizeof(MIXERLINE)
                mixerline.dwDestination = i
                mixerline.dwSource = n
                if mixerGetLineInfo(hmixer, byref(mixerline), MIXER_GETLINEINFOF_SOURCE):
                    continue
                source = mixerline.szName

                for control in self.GetControls(hmixer, mixerline):
                    result.append((control[0], destination, source, control[1], control[2], control[3]))

        return result


    def GetControls(self, hmixer, mixerline):
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
                    mixerControl.dwControlID,
                    mixerControl.szName,
                    controlClass["name"],
                    controlClassTypeName,
                    ", ".join(flagNames)
                )
            )

        return result



class SoundMixerEx(eg.PluginClass):

    def __init__(self):
        self.mixer = SoundMixerWin32()
        self.mixers = None
        self.controls = None
        self.AddAction(SetSoundSwitch)
        self.AddAction(SetSoundFader)


    def GetMixers(self):
        if self.mixers is None:
            self.mixers = self.mixer.GetMixerDevices()
        return self.mixers


    def GetControls(self):
        if self.controls is None:
            self.controls = []
            mixers = self.GetMixers()
            for mixerId, mixerName in mixers:
                controls = self.mixer.GetDeviceLines(mixerId)
                for controlId, dst, src, name, cclass, type in controls:
                    self.controls.append((mixerId, controlId, mixerName, dst, src, name, cclass, type))
        return self.controls


    def GetTree(self, panel, classVisible, mixerSelect, controlSelect):
        mixerLast = ""
        mixerItem = None
        dstLast = ""
        dstItem = None
        srcLast = ""
        srcItem = None

        # Multiple mixers?
        if len(self.GetMixers()) > 1:
            multipleMixers = True
        else:
            multipleMixers = False

        # Create tree control
        treeCtrl = wx.TreeCtrl(panel, -1, wx.Point(0, 0), wx.Size(350, 150))
        rootItem = treeCtrl.AddRoot("Available sound cards")

        # Loop over ALL controls in ALL mixers
        controls = self.GetControls()
        for mixerid, controlid, mixer, dst, src, name, cclass, type in controls:
            if not cclass in classVisible:
                continue

            if mixer != mixerLast:
                mixerItem = treeCtrl.AppendItem(rootItem, mixer)
                mixerLast = mixer

            if dst != dstLast:
                dstItem = treeCtrl.AppendItem(mixerItem, dst)
                dstLast = dst

            if src is not None:
                if src != srcLast:
                    srcItem = treeCtrl.AppendItem(dstItem, src)
                    srcLast = src
                item = treeCtrl.AppendItem(srcItem, "%s (%s)" % (name, type))
                name = "%s - %s - %s" % (dst, src, name)
            else:
                item = treeCtrl.AppendItem(dstItem, "%s (%s)" % (name, type))
                name = "%s - %s" % (dst, name)

            if multipleMixers:
                name = "'%s' on '%s'" % (name, mixer)
            else:
                name = "'%s'" % (name)

            treeCtrl.SetPyData(item, (mixerid, controlid, name))

            if mixerid == mixerSelect and controlid == controlSelect:
                    treeCtrl.SelectItem(item)

        treeCtrl.Expand(rootItem)
        #Return tree
        return treeCtrl



class SetSoundSwitch(eg.ActionClass):
    name = "Change sound switch"
    description = "Changes a selectable sound switch control"

    def __call__(self, deviceId=-1, controlId=-1, name="", value=0):
        if deviceId == -1 or controlId == -1:
            self.printError("No device/control selected")
        else:
            if value == 0:
                value = False
            elif value == 1:
                value = True
            else:
                value = not self.plugin.mixer.GetSwitchValue(deviceId, controlId)
            self.plugin.mixer.SetSwitchValue(deviceId, controlId, value)
        return value


    def GetLabel(self, deviceId=-1, controlId=-1, name="", value=0):
        if deviceId == -1 or controlId == -1:
            return "No device/control selected"
        if value == 1:
            return "Sets %s to on" % (name)
        elif value == 0:
            return "Sets %s to off" % (name)
        else:
            return "Toggles %s" % (name)


    def Configure(self, deviceId=-1, controlId=-1, name="", value=0):
        panel = eg.ConfigPanel(self)

        treeTxt = wx.StaticText(panel, -1, "Available controls:")
        treeCtrl = self.plugin.GetTree(panel, ("Switch"), deviceId, controlId)
        actionTxt = wx.StaticText(panel, -1, "Action:")
        actionCtrl = panel.Choice(value, choices=("Set off", "Set on", "Toggle"))

        panel.sizer.Add(treeTxt)
        panel.sizer.Add(treeCtrl, 1, wx.EXPAND)
        panel.sizer.Add((5,5))
        panel.sizer.Add(actionTxt)
        panel.sizer.Add(actionCtrl)

        while panel.Affirmed():
            data = treeCtrl.GetPyData(treeCtrl.GetSelection())
            if data is not None:
                (deviceId, controlId, name) = data
                value = actionCtrl.GetValue()
            panel.SetResult(deviceId, controlId, name, value)



class SetSoundFader(eg.ActionClass):
    name = "Change sound fader/slider"
    description = "Changes a selectable sound fader/slider control"

    def __call__(self, deviceId=-1, controlId=-1, name="", value=0, relative=1):
        if deviceId == -1 or controlId == -1:
            self.printError("No device/control selected")
        else:
            if relative == 1:
                value += self.plugin.mixer.GetFaderValue(deviceId, controlId)
            self.plugin.mixer.SetFaderValue(deviceId, controlId, value)
        return value


    def GetLabel(self, deviceId=-1, controlId=-1, name="", value=0, relative=1):
        if deviceId == -1 or controlId == -1:
            return "No device/control selected"
        if relative == 1:
            if value > 0:
                return "Increases %s with %d%%" % (name, value)
            else:
                return "Decreases %s with %d%%" % (name, value)
        else:
            return "Sets %s to %d%%" % (name, value)


    def Configure(self, deviceId=-1, controlId=-1, name="", value=0, relative=1):
        panel = eg.ConfigPanel(self)

        treeTxt = wx.StaticText(panel, -1, "Available controls:")
        treeCtrl = self.plugin.GetTree(panel, ("Fader", "Slider"), deviceId, controlId)
        actionTxt = wx.StaticText(panel, -1, "Update:")
        actionCtrl = panel.Choice(relative, choices=("Absolute", "Relative"))
        valueTxt = wx.StaticText(panel, -1, "Value:")
        valueCtrl = panel.SpinNumCtrl(value, increment=5, min=-100, max=100)

        panel.sizer.Add(treeTxt)
        panel.sizer.Add(treeCtrl, 1, wx.EXPAND)
        panel.sizer.Add((5,5))
        panel.sizer.Add(actionTxt)
        panel.sizer.Add(actionCtrl)
        panel.sizer.Add((5,5))
        panel.sizer.Add(valueTxt)
        panel.sizer.Add(valueCtrl)

        while panel.Affirmed():
            data = treeCtrl.GetPyData(treeCtrl.GetSelection())
            if data is not None:
                (deviceId, controlId, name) = data
                relative = actionCtrl.GetValue()
                value = valueCtrl.GetValue()
            panel.SetResult(deviceId, controlId, name, value, relative)



# -*- coding: utf-8 -*-
#
# plugins/AudioEndpoint/__init__.py
# 
# This file is a plugin for EventGhost.

import eg

eg.RegisterPlugin(
    name = "AudioEndpoint",
    guid = "{31DE576B-5938-4C0B-A0E2-64F9ADF02BF8}",
    author = "Sem;colon",
    version = "2.3.3",
    kind = "other",
    canMultiLoad = False,
    description = "This plugin can set the default audio render device and generates events when an audio endpoint changes!",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6213",
)

import AudioEndpointControl
from fnmatch import fnmatch

class MMNotificationClient(object):
    
    def __init__(self, plugin):
        self.plugin = plugin

    def OnDeviceStateChanged(self, AudioDevice, NewState):
        NewState=str(NewState).upper()
        self.plugin.TriggerEvent("State."+NewState+"."+AudioDevice.getName(),[AudioDevice.getId()])
        if NewState == "ACTIVE" or NewState == "NOTPRESENT":
            self.plugin.ReInitAudioDevices()
    
    def OnDeviceRemoved(self, AudioDevice):
        self.plugin.TriggerEvent("DeviceRemoved."+AudioDevice.getName(),[AudioDevice.getId()])
        if AudioDevice in self.plugin.registeredAudioDevices:
            AudioDevice.UnregisterCallback()
            self.plugin.registeredAudioDevices.remove(AudioDevice)
        self.plugin.ReInitAudioDevices()

    def OnDeviceAdded(self, AudioDevice):
        self.plugin.TriggerEvent("DeviceAdded."+AudioDevice.getName(),[AudioDevice.getId()])
        self.plugin.ReInitAudioDevices()
    
    def OnDefaultDeviceChanged(self, flow, role, AudioDevice):
        self.plugin.TriggerEvent("Default."+str(flow)+"."+str(role)+"."+AudioDevice.getName(),[AudioDevice.getId()])
            
    #def OnPropertyValueChanged(self, AudioDevice, key):
    #    if self.plugin.advancedEndpointEvents:
    #        property=u"{%8.08x-%4.04x-%4.04x-%2.02x%2.02x-%2.02x%2.02x%2.02x%2.02x%2.02x%2.02x}" % (key.fmtid.Data1, key.fmtid.Data2, key.fmtid.Data3,	2**8+key.fmtid.Data4[0], 2**8+key.fmtid.Data4[1],	2**8+key.fmtid.Data4[2], 2**8+key.fmtid.Data4[3],	2**8+key.fmtid.Data4[4], 2**8+key.fmtid.Data4[5],	2**8+key.fmtid.Data4[6], 2**8+key.fmtid.Data4[7])
    #        self.plugin.TriggerEvent("Property."+AudioDevice.getName(),[AudioDevice.getId(),property,int(key.pid)])
    
    
class AudioEndpointVolumeCallback(object):
    
    def __init__(self, plugin):
        self.plugin = plugin
    
    def OnNotify(self, Notify, AudioDevice):
        if self.plugin.AudioDeviceData[AudioDevice.getId()]["volume"] != Notify.MasterVolume:
            self.plugin.AudioDeviceData[AudioDevice.getId()]["volume"] = Notify.MasterVolume
            self.plugin.TriggerEvent("Volume."+AudioDevice.getName(), [AudioDevice.getId(), str(round(Notify.MasterVolume*100,2))])
        if self.plugin.AudioDeviceData[AudioDevice.getId()]["mute"] != Notify.Muted:  
            self.plugin.AudioDeviceData[AudioDevice.getId()]["mute"] = Notify.Muted
            if Notify.Muted:
                self.plugin.TriggerEvent("Mute."+AudioDevice.getName(), [AudioDevice.getId(), Notify.Muted])
            else:
                self.plugin.TriggerEvent("UnMute."+AudioDevice.getName(), [AudioDevice.getId(), Notify.Muted])

        
class AudioEndpoint(eg.PluginBase):
  
    class Text:
        eventBox = "Trigger events:"
        volumeEvents = "Volume or mute changes on an audio endpoint"
        endpointEvents = "Audio endpoint state changes"
        advancedEndpointEvents = "Advanced audio endpoint state changes (property changes)"
        flows = ["Render", "Capture"]
        returnedDevice = 'Returned device from the an "Get Audio Device" action'
    
    
    def __init__(self):
        self.AddAction(SetRender, "SetRender", "Set Default Audio Render", "Sets the default audio render device.(by id)", hidden=True)#only for backwards compatibillity
        self.AddAction(GetRender, "GetRender", "Get Default Audio Render", "Returns the ID of the current Default Audio Render", hidden=True)#only for backwards compatibillity
        self.AddAction(SetDefaultDevice, "SetDefaultDevice", "Set Default Audio Device", "Sets the default audio device.(by id)")
        self.AddAction(GetDefaultDevice, "GetDefaultDevice", "Get Default Audio Device", "Returns the ID and the name of the current Default Audio Device")
        self.AddAction(GetDeviceByName, "GetDeviceByName", "Get Audio Device By Name", "Returns the ID and the name of the first device with the specified name")
        self.AddAction(NextRender, "NextRender", "Next Default Audio Render", "Selects the next available Default Audio Render", hidden=True)#only for backwards compatibillity
        self.AddAction(PreviousRender, "PreviousRender", "Previous Default Audio Render", "Selects previous available Default Audio Render", hidden=True)#only for backwards compatibillity
        self.AddAction(NextDefaultDevice, "NextDefaultDevice", "Next Default Audio Device", "Selects the next available Default Audio Device")
        self.AddAction(PreviousDefaultDevice, "PreviousDefaultDevice", "Previous Default Audio Device", "Selects previous available Default Audio Device")
        self.AddAction(GetMute, "GetMute", "Get Mute", "Returns True if a specific audio endpoint is muted, and False if not")
        self.AddAction(SetMute, "SetMute", "Set Mute", "Set mute for a specific audio endpoint (ON, OFF or TOGGLE)")
        self.AddAction(GetVolume, "GetVolume", "Get Volume", "Returns the current volume of a specific audio endpoint")
        self.AddAction(SetVolume, "SetVolume", "Set Volume", "Set the volume for a specific audio endpoint. Can be absolute or relative")
        self.registeredAudioDevices = []
        self.AudioDeviceData = {}

        
    def __start__(self, volumeEvents=True, endpointEvents=True, advancedEndpointEvents=False):
        self.volumeEvents=volumeEvents
        self.endpointEvents=endpointEvents
        #self.advancedEndpointEvents=advancedEndpointEvents
        self.AudioDevices = AudioEndpointControl.AudioEndpoints()
        if endpointEvents:
            self.AudioDevices.RegisterCallback(MMNotificationClient(self))
        if self.ReInitAudioDevices():
            print "Audio Endpoint plugin started."
            for flow in [0,1]:
                for role in [0,1,2]:
                    try:
                        device=self.AudioDevices.GetDefault(role,flow)
                        flow2=AudioEndpointControl.EDataFlow[flow]
                        role2=AudioEndpointControl.ERole[role]
                        self.TriggerEvent("Default."+flow2+"."+role2+"."+device.getName(),[device.getId()])
                    except:
                        pass
                        

    def __stop__(self):
        for AudioDevice in self.registeredAudioDevices:
            AudioDevice.UnregisterCallback()
        self.registeredAudioDevices = []
        if self.endpointEvents:
            self.AudioDevices.UnregisterCallback()
        self.AudioDevices=None
        print "Audio Endpoint plugin stopped."

        
    def __close__(self):
        print "Audio Endpoint plugin closed."

        
    def ReInitAudioDevices(self):
        self.AudioDeviceIDs = [[],[]]
        self.AudioDeviceNames = [[],[]]
        self.allAudioDeviceIDs = []
        self.allAudioDeviceNames= []
        for flow in [0,1]: #Render,Capture
            for AudioDevice in self.AudioDevices.__iter__(flow):
                if self.volumeEvents and AudioDevice not in self.registeredAudioDevices:
                    AudioDevice.RegisterCallback(AudioEndpointVolumeCallback(self))
                    self.registeredAudioDevices.append(AudioDevice)
                self.AudioDeviceIDs[flow].append(AudioDevice.getId())
                self.allAudioDeviceIDs.append(AudioDevice.getId())
                self.AudioDeviceNames[flow].append(AudioDevice.getName())
                self.allAudioDeviceNames.append(self.Text.flows[flow]+": "+AudioDevice.getName())
                if AudioDevice.getId() not in self.AudioDeviceData:
                    self.AudioDeviceData[AudioDevice.getId()] = {"volume":None,"mute":None}
                if self.AudioDeviceData[AudioDevice.getId()]["volume"] != AudioDevice.volume.Get():
                    self.AudioDeviceData[AudioDevice.getId()]["volume"] = AudioDevice.volume.Get()
                    #self.TriggerEvent("Volume."+AudioDevice.getName(),[AudioDevice.getId(),str(round(AudioDevice.volume.Get()*100,2))])
                if self.AudioDeviceData[AudioDevice.getId()]["mute"] != (AudioDevice.GetMute() == 1):  
                    self.AudioDeviceData[AudioDevice.getId()]["mute"] = AudioDevice.GetMute() == 1
                    #if AudioDevice.GetMute() == 1:
                    #    self.TriggerEvent("Mute."+AudioDevice.getName(),[AudioDevice.getId(),AudioDevice.GetMute() == 1])
                    #else:
                    #    self.TriggerEvent("UnMute."+AudioDevice.getName(),[AudioDevice.getId(),AudioDevice.GetMute() == 1])
        self.allAudioDeviceIDs.append("returnedDevice")
        self.allAudioDeviceNames.append(self.Text.returnedDevice)
        return True
            
            
    def Configure(self, volumeEvents=True, endpointEvents=True, advancedEndpointEvents=False):
        text = self.Text
        panel = eg.ConfigPanel()
        wx_volumeEvents = wx.CheckBox(panel, -1, text.volumeEvents)
        wx_volumeEvents.SetValue(volumeEvents)
        wx_endpointEvents = wx.CheckBox(panel, -1, text.endpointEvents)
        wx_endpointEvents.SetValue(endpointEvents)
        #wx_advancedEndpointEvents = wx.CheckBox(panel, -1, text.advancedEndpointEvents)
        #wx_advancedEndpointEvents.SetValue(advancedEndpointEvents)
        eventBox = panel.BoxedGroup(
            text.eventBox,
            ("",wx_volumeEvents),
            ("",wx_endpointEvents),
            #("",wx_advancedEndpointEvents),
        )

        panel.sizer.Add(eventBox, 0, wx.EXPAND)
        
        while panel.Affirmed():
            panel.SetResult(
                wx_volumeEvents.GetValue(),
                wx_endpointEvents.GetValue(),
                #wx_advancedEndpointEvents.GetValue(),
            )
    
            
class SetRender(eg.ActionBase):#only for backward compatibillity
    
    class Text:
        role = "Role:"
        setTo = "Set default to:"
    
    def __call__(self,target,role=0):
        try:
            self.plugin.AudioDevices.SetDefault(self.plugin.AudioDevices(target),role)
            return True
        except:
            eg.PrintError("AudioEndpoint SetRender: Device not found! "+str(target))
            return False
    
    def GetLabel(self, target="",role=0):
        try:
            target = self.plugin.AudioDevices(target).getName()
        except:
            target = "???"
        return target
        
    def Configure(self,target="",role=0):
        roles=["Console","Multimedia","Communications"]
        panel = eg.ConfigPanel(self)
        
        wx_role = wx.Choice(panel, -1, choices=roles)
        wx_role.SetSelection(role)
        st_role = panel.StaticText(self.Text.role)
        
        if target in self.plugin.AudioDeviceIDs[0]:
            target = self.plugin.AudioDeviceIDs[0].index(target)
        else:
            target = 0
        wx_setTo = wx.Choice(panel, -1, choices=self.plugin.AudioDeviceNames[0])
        wx_setTo.SetSelection(target)
        st_setTo = panel.StaticText(self.Text.setTo)
        
        panel.AddLine(st_role,wx_role)
        panel.AddLine(st_setTo,wx_setTo)

        while panel.Affirmed():
            panel.SetResult(self.plugin.AudioDeviceIDs[0][wx_setTo.GetCurrentSelection()],wx_role.GetCurrentSelection())    
    

class GetRender(eg.ActionBase):#only for backward compatibillity
    
    def __call__(self):
        return self.plugin.AudioDevices.GetDefault(0,0).getId() 

        
class SetDefaultDevice(eg.ActionBase):
    
    class Text:
        role = "Role:"
        setTo = "Set default to:"
    
    def __call__(self,deviceId,role=0):
        try:
            if deviceId=="returnedDevice":
                deviceId = eg.result["id"]
            self.plugin.AudioDevices.SetDefault(self.plugin.AudioDevices(deviceId),role)
            return True
        except:
            eg.PrintError("AudioEndpoint SetCapture: Device not found! "+str(deviceId))
            return False
    
    def GetLabel(self, deviceId,role=0):
        target = "to the returned device"
        if deviceId!="returnedDevice":
            try:
                target = "to " + self.plugin.AudioDevices(deviceId).getName()
            except:
                target = "???"
        return self.name + " " + target

    def Configure(self,target="",role=0):
        roles=["Console","Multimedia","Communications"]
        panel = eg.ConfigPanel(self)
        
        wx_role = wx.Choice(panel, -1, choices=roles)
        wx_role.SetSelection(role)
        st_role = panel.StaticText(self.Text.role)
        
        if target in self.plugin.allAudioDeviceIDs:
            target = self.plugin.allAudioDeviceIDs.index(target)
        else:
            target = 0
        wx_setTo = wx.Choice(panel, -1, choices=self.plugin.allAudioDeviceNames)
        wx_setTo.SetSelection(target)
        st_setTo = panel.StaticText(self.Text.setTo)
        
        panel.AddLine(st_role,wx_role)
        panel.AddLine(st_setTo,wx_setTo)

        while panel.Affirmed():
            panel.SetResult(self.plugin.allAudioDeviceIDs[wx_setTo.GetCurrentSelection()],wx_role.GetCurrentSelection())    

    
    
class GetDefaultDevice(eg.ActionBase):
    
    class Text:
        flow = "Flow:"
        role = "Role:"
    
    def __call__(self,role=0,flow=0):
        try:
            device = self.plugin.AudioDevices.GetDefault(role,flow)
            return {"id":device.getId(),"name":device.getName()}
        except:
            eg.PrintError("AudioEndpoint GetDefaultDevice: Default device not found!")
            return False
        
    def Configure(self,role=0,flow=0):
        flows=["Render","Capture"]
        roles=["Console","Multimedia","Communications"]
        panel = eg.ConfigPanel(self)
        
        wx_role = wx.Choice(panel, -1, choices=roles)
        wx_role.SetSelection(role)
        st_role = panel.StaticText(self.Text.role)
        
        wx_flow = wx.Choice(panel, -1, choices=flows)
        wx_flow.SetSelection(flow)
        st_flow = panel.StaticText(self.Text.flow)
        
        panel.AddLine(st_role,wx_role)
        panel.AddLine(st_flow,wx_flow)

        while panel.Affirmed():
            panel.SetResult(wx_role.GetCurrentSelection(),wx_flow.GetCurrentSelection())    
        

class GetDeviceByName(eg.ActionBase):
    
    class Text:
        target = "Device Name:"
        parsing = "disable parsing"
    
    def __call__(self,target1,parseNoTarget=True):
        result = None
        if not parseNoTarget:
            target1=eg.ParseString(unicode(target1))
        for target in self.plugin.allAudioDeviceNames:
            if fnmatch(target,target1):
                targetIndex = self.plugin.allAudioDeviceNames.index(target)
                id = self.plugin.allAudioDeviceIDs[targetIndex]
                device = self.plugin.AudioDevices(id)
                result = {"id":device.getId(),"name":device.getName()}
                break
        return result

    def Configure(self,target="",parseNoTarget=True):
        panel = eg.ConfigPanel(self)
        wx_parseNoTarget = wx.CheckBox(panel, -1, self.Text.parsing)
        wx_parseNoTarget.SetValue(parseNoTarget)
        wx_target = panel.TextCtrl(unicode(target), size=(400,-1))
        st_target = panel.StaticText(self.Text.target)
        
        panel.AddLine(st_target,wx_target,wx_parseNoTarget)

        while panel.Affirmed():
            panel.SetResult(wx_target.GetValue(),wx_parseNoTarget.GetValue())  
        
        
class NextRender(eg.ActionBase):#only for backward compatibillity
    
    class Text:
        role = "Role:"
    
    def __call__(self,role=0):
        oldIndex = self.plugin.AudioDeviceIDs[0].index(self.plugin.AudioDevices.GetDefault(role,0).getId())
        i=oldIndex+1
        while i!=oldIndex:
            if i<len(self.plugin.AudioDeviceIDs[0]):
                target = self.plugin.AudioDeviceIDs[0][i]
                self.plugin.AudioDevices.SetDefault(self.plugin.AudioDevices(target),role)
                return True
            if i>=len(self.plugin.AudioDeviceIDs[0]):
                i=0
            else:
                i+=1
        eg.PrintError("AudioEndpoint NextRender: No (other) selectable Render!")
        return False

    def Configure(self,role=0):
        while panel.Affirmed():
            panel.SetResult(role)    
    
    
class PreviousRender(eg.ActionBase):#only for backward compatibillity
        
    class Text:
        role = "Role:"
    
    def __call__(self,role=0):
        oldIndex = self.plugin.AudioDeviceIDs[0].index(self.plugin.AudioDevices.GetDefault(role,0).getId())
        i=oldIndex-1
        while i!=oldIndex:
            if i>=0:
                target = self.plugin.AudioDeviceIDs[0][i]
                self.plugin.AudioDevices.SetDefault(self.plugin.AudioDevices(target),role)
                return True
            if i<=0:
                i=len(self.plugin.AudioDeviceIDs[0])-1
            else:
                i-=1
        eg.PrintError("AudioEndpoint PreviousRender: No (other) selectable Render!")
        return False

    def Configure(self,role=0):
        while panel.Affirmed():
            panel.SetResult(role)

            
class NextDefaultDevice(eg.ActionBase):
    
    class Text:
        flow = "Flow:"
        role = "Role:"
    
    def __call__(self,role=0,flow=0):
        oldIndex = self.plugin.AudioDeviceIDs[flow].index(self.plugin.AudioDevices.GetDefault(role,flow).getId())
        i=oldIndex+1
        while i!=oldIndex:
            if i<len(self.plugin.AudioDeviceIDs[flow]):
                target = self.plugin.AudioDeviceIDs[flow][i]
                self.plugin.AudioDevices.SetDefault(self.plugin.AudioDevices(target),role)
                return True
            if i>=len(self.plugin.AudioDeviceIDs[flow]):
                i=0
            else:
                i+=1
        eg.PrintError("AudioEndpoint NextDefaultDevice: No (other) selectable device!")
        return False

    def Configure(self,role=0,flow=0):
        flows=["Render","Capture"]
        roles=["Console","Multimedia","Communications"]
        panel = eg.ConfigPanel(self)
        
        wx_role = wx.Choice(panel, -1, choices=roles)
        wx_role.SetSelection(role)
        st_role = panel.StaticText(self.Text.role)
        
        wx_flow = wx.Choice(panel, -1, choices=flows)
        wx_flow.SetSelection(flow)
        st_flow = panel.StaticText(self.Text.flow)
        
        panel.AddLine(st_role,wx_role)
        panel.AddLine(st_flow,wx_flow)

        while panel.Affirmed():
            panel.SetResult(wx_role.GetCurrentSelection(),wx_flow.GetCurrentSelection())    
    
    
class PreviousDefaultDevice(eg.ActionBase):
        
    class Text:
        flow = "Flow:"
        role = "Role:"
    
    def __call__(self,role=0,flow=0):
        oldIndex = self.plugin.AudioDeviceIDs[flow].index(self.plugin.AudioDevices.GetDefault(role,flow).getId())
        i=oldIndex-1
        while i!=oldIndex:
            if i>=0:
                target = self.plugin.AudioDeviceIDs[flow][i]
                self.plugin.AudioDevices.SetDefault(self.plugin.AudioDevices(target),role)
                return True
            if i<=0:
                i=len(self.plugin.AudioDeviceIDs[flow])-1
            else:
                i-=1
        eg.PrintError("AudioEndpoint PreviousDefaultDevice: No (other) selectable device!")
        return False

    def Configure(self,role=0,flow=0):
        flows=["Render","Capture"]
        roles=["Console","Multimedia","Communications"]
        panel = eg.ConfigPanel(self)
        
        wx_role = wx.Choice(panel, -1, choices=roles)
        wx_role.SetSelection(role)
        st_role = panel.StaticText(self.Text.role)
        
        wx_flow = wx.Choice(panel, -1, choices=flows)
        wx_flow.SetSelection(flow)
        st_flow = panel.StaticText(self.Text.flow)
        
        panel.AddLine(st_role,wx_role)
        panel.AddLine(st_flow,wx_flow)

        while panel.Affirmed():
            panel.SetResult(wx_role.GetCurrentSelection(),wx_flow.GetCurrentSelection())
			
            
class GetMute(eg.ActionBase):
    
    class Text:
        device="Device:"
        
    def __call__(self, deviceId):
        try:
            if deviceId=="returnedDevice":
                deviceId = eg.result["id"]
            targetDevice = self.plugin.AudioDevices(deviceId)
        except:
            eg.PrintError("AudioEndpoint GetMute: Device not found! "+str(deviceId))
            return None
        return targetDevice.GetMute() == 1
    
    def GetLabel(self, deviceId):
        target = "for the returned device"
        if deviceId!="returnedDevice":
            try:
                target = "for " + self.plugin.AudioDevices(deviceId).getName()
            except:
                target = "???"
        return self.name + " " + target

    def Configure(self, deviceId=""):
        panel = eg.ConfigPanel(self)
        
        if deviceId in self.plugin.allAudioDeviceIDs:
            target = self.plugin.allAudioDeviceIDs.index(deviceId)
        else:
            target = 0
        wx_device = wx.Choice(panel, -1, choices=self.plugin.allAudioDeviceNames)
        wx_device.SetSelection(target)
        st_device = panel.StaticText(self.Text.device)
        
        panel.AddLine(st_device,wx_device)

        while panel.Affirmed():
            panel.SetResult(self.plugin.allAudioDeviceIDs[wx_device.GetCurrentSelection()])
                    
                    
class SetMute(eg.ActionBase):
    
    class Text:
        device = "Device:"
        state  = "State:"
    
    def __call__(self, deviceId, targetState):
        try:
            if deviceId=="returnedDevice":
                deviceId = eg.result["id"]
            targetDevice = self.plugin.AudioDevices(deviceId)
        except:
            eg.PrintError("AudioEndpoint SetMute: Device not found! "+str(deviceId))
            return False
        if targetState==1:
            targetDevice.SetMute(True)
        elif targetState==0:
            targetDevice.SetMute(False)
        else:
            targetDevice.SetMute(targetDevice.GetMute() == 0)
        return True
    
    def GetLabel(self, deviceId, targetState=0):
        states=["OFF","ON","TOGGLE"]
        target = states[targetState] + " on the returned device"
        if deviceId!="returnedDevice":
            try:
                target = states[targetState] + " on " + self.plugin.AudioDevices(deviceId).getName()
            except:
                target = "???"
        return self.name + " " + target
        
    def Configure(self, deviceId="", targetState=0):
        states=["OFF","ON","TOGGLE"]
        panel = eg.ConfigPanel(self)
        
        wx_state = wx.Choice(panel, -1, choices=states)
        wx_state.SetSelection(targetState)
        st_state = panel.StaticText(self.Text.state)
        
        if deviceId in self.plugin.allAudioDeviceIDs:
            target = self.plugin.allAudioDeviceIDs.index(deviceId)
        else:
            target = 0
        wx_device = wx.Choice(panel, -1, choices=self.plugin.allAudioDeviceNames)
        wx_device.SetSelection(target)
        st_device = panel.StaticText(self.Text.device)
        
        panel.AddLine(st_device,wx_device)
        panel.AddLine(st_state,wx_state)

        while panel.Affirmed():
            panel.SetResult(self.plugin.allAudioDeviceIDs[wx_device.GetCurrentSelection()],wx_state.GetCurrentSelection())
            
            
class GetVolume(eg.ActionBase):
    
    class Text:
        device="Device:"
        
    def __call__(self, deviceId):
        try:
            if deviceId=="returnedDevice":
                deviceId = eg.result["id"]
            targetDevice = self.plugin.AudioDevices(deviceId)
        except:
            eg.PrintError("AudioEndpoint GetVolume: Device not found! "+str(deviceId))
            return None
        return round(targetDevice.volume.Get()*100,2)
        
    def GetLabel(self, deviceId):
        target = "for the returned device"
        if deviceId!="returnedDevice":
            try:
                target = "for " + self.plugin.AudioDevices(deviceId).getName()
            except:
                target = "???"
        return self.name + " " + target
        
    def Configure(self, deviceId=""):
        panel = eg.ConfigPanel(self)
        
        if deviceId in self.plugin.allAudioDeviceIDs:
            target = self.plugin.allAudioDeviceIDs.index(deviceId)
        else:
            target = 0
        wx_device = wx.Choice(panel, -1, choices=self.plugin.allAudioDeviceNames)
        wx_device.SetSelection(target)
        st_device = panel.StaticText(self.Text.device)
        
        panel.AddLine(st_device,wx_device)

        while panel.Affirmed():
            panel.SetResult(self.plugin.allAudioDeviceIDs[wx_device.GetCurrentSelection()])
                    
                    
class SetVolume(eg.ActionBase):
    
    class Text:
        device = "Device:"
        relative = "Relative"
        level = "Level:"
    
    def __call__(self, deviceId, level, relative=False):
        try:
            if deviceId=="returnedDevice":
                deviceId = eg.result["id"]
            targetDevice = self.plugin.AudioDevices(deviceId)
        except:
            eg.PrintError("AudioEndpoint SetVolume: Device not found! "+str(deviceId))
            return False
        targetVolume=0.0
        if relative:
            targetVolume=round(targetDevice.volume.Get()*100,2)+level
        else:
            targetVolume=level
        if targetVolume>100:
            targetVolume=100.0
        elif targetVolume<0:
            targetVolume=0.0
        targetDevice.volume.Set(targetVolume/100)
        return True
        
    def GetLabel(self, deviceId, level, relative=False):
        if relative:
            target = "Relative by " + str(level) + " on "
        else:
            target = "to " + str(level) + " on "
        if deviceId=="returnedDevice":
            target += "the returned device"
        else:
            try:
                target += self.plugin.AudioDevices(deviceId).getName()
            except:
                target = "???"
        return self.name + " " + target
        
    def Configure(self, deviceId="", level=0.0, relative=False):
        panel = eg.ConfigPanel(self)
        
        if deviceId in self.plugin.allAudioDeviceIDs:
            target = self.plugin.allAudioDeviceIDs.index(deviceId)
        else:
            target = 0
        wx_device = wx.Choice(panel, -1, choices=self.plugin.allAudioDeviceNames)
        wx_device.SetSelection(target)
        st_device = panel.StaticText(self.Text.device)
        
        wx_level = eg.SpinNumCtrl(panel, -1, level, min=-100.0, max=100.0)
        st_level = panel.StaticText(self.Text.level)
        
        wx_relative = wx.CheckBox(panel, -1, self.Text.relative)
        wx_relative.SetValue(relative)
        st_relative = panel.StaticText("")
        
        panel.AddLine(st_device,wx_device)
        panel.AddLine(st_level,wx_level)
        panel.AddLine(st_relative,wx_relative)

        while panel.Affirmed():
            panel.SetResult(self.plugin.allAudioDeviceIDs[wx_device.GetCurrentSelection()],wx_level.GetValue(),wx_relative.GetValue())
            
# Python Imports
import wx.lib.agw.floatspin as FS
from datetime import datetime
import re
import time
from threading import Thread

# Local Imports
import globals
from yamaha import *
from helpers import *

class SmartVolumeFinished(eg.ActionBase):
    def __call__(self):
        self.plugin.smart_vol_up_start = None
        self.plugin.smart_vol_down_start = None

class SmartVolumeUp(eg.ActionBase):
    def __call__(self, zone, step1, step2, wait):
        izone = convert_zone_to_int(self.plugin, zone)
        if self.plugin.smart_vol_up_start is None:
            self.plugin.smart_vol_up_start = datetime.now()
        diff = datetime.now() - self.plugin.smart_vol_up_start
        if diff.seconds < float(wait):
            #print "Volume Up:", step1
            increase_volume(self.plugin, izone, step1)
        else:
            #print "Volume Up:", step2
            increase_volume(self.plugin, izone, step2)

    def Configure(self, zone='Active Zone', step1=0.5, step2=2.0, wait=2.0):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Increase Amount (Step 1): ", pos=(10, 60))
        fs_step1 = FS.FloatSpin(panel, -1, pos=(170, 57), min_val=0.5, max_val=10,
            increment=0.5, value=float(step1), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="dB", pos=(270, 60))
        fs_step1.SetFormat("%f")
        fs_step1.SetDigits(1)

        wx.StaticText(panel, label="Time between Step 1 to Step 2: ", pos=(10, 100))
        fs_wait = FS.FloatSpin(panel, -1, pos=(170, 97), min_val=0.5, max_val=999,
            increment=0.1, value=float(wait), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="Seconds", pos=(270, 100))
        fs_wait.SetFormat("%f")
        fs_wait.SetDigits(1)

        wx.StaticText(panel, label="Increase Amount (Step 2): ", pos=(10, 140))
        fs_step2 = FS.FloatSpin(panel, -1, pos=(170, 137), min_val=0.5, max_val=10,
            increment=0.5, value=float(step2), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="dB", pos=(270, 140))

        fs_step2.SetFormat("%f")
        fs_step2.SetDigits(1)

        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], fs_step1.GetValue(), fs_step2.GetValue(), fs_wait.GetValue())

class SmartVolumeDown(eg.ActionBase):
    def __call__(self, zone, step1, step2, wait):
        izone = convert_zone_to_int(self.plugin, zone)
        if self.plugin.smart_vol_down_start is None:
            self.plugin.smart_vol_down_start = datetime.now()
        diff = datetime.now() - self.plugin.smart_vol_down_start
        if diff.seconds < float(wait):
            decrease_volume(self.plugin, izone, step1)
        else:
            decrease_volume(self.plugin, izone, step2)

    def Configure(self, zone='Active Zone', step1=0.5, step2=2.0, wait=2.0):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Decrease Amount (Step 1): ", pos=(10, 60))
        fs_step1 = FS.FloatSpin(panel, -1, pos=(170, 57), min_val=0.5, max_val=10,
            increment=0.5, value=float(step1), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="dB", pos=(270, 60))
        fs_step1.SetFormat("%f")
        fs_step1.SetDigits(1)

        wx.StaticText(panel, label="Time between Step 1 to Step 2: ", pos=(10, 100))
        fs_wait = FS.FloatSpin(panel, -1, pos=(170, 97), min_val=0.5, max_val=999,
            increment=0.1, value=float(wait), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="Seconds", pos=(270, 100))
        fs_wait.SetFormat("%f")
        fs_wait.SetDigits(1)

        wx.StaticText(panel, label="Decrease Amount (Step 2): ", pos=(10, 140))
        fs_step2 = FS.FloatSpin(panel, -1, pos=(170, 137), min_val=0.5, max_val=10,
            increment=0.5, value=float(step2), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="dB", pos=(270, 140))
        fs_step2.SetFormat("%f")
        fs_step2.SetDigits(1)

        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], fs_step1.GetValue(), fs_step2.GetValue(), fs_wait.GetValue())

class IncreaseVolume(eg.ActionBase):
    def __call__(self, zone, step):
        increase_volume(self.plugin, convert_zone_to_int(self.plugin, zone), float(step))

    def Configure(self, zone='Active Zone', step=0.5):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Increase Amount (Step): ", pos=(10, 60))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=0.5, max_val=10,
            increment=0.5, value=float(step), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], floatspin.GetValue())

class DecreaseVolume(eg.ActionBase):
    def __call__(self, zone, step):
        decrease_volume(self.plugin, convert_zone_to_int(self.plugin, zone), float(step))

    def Configure(self, zone='Active Zone', step=0.5):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Decrease Amount (Step): ", pos=(10, 60))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=0.5, max_val=10,
                                 increment=0.5, value=float(step), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], floatspin.GetValue())

class SetVolume(eg.ActionBase):
    def __call__(self, zone, vol):
        set_volume(self.plugin, convert_zone_to_int(self.plugin, zone), float(vol))

    def Configure(self, zone='Active Zone', vol=-50.0):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Exact Volume (dB): ", pos=(10, 60))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=-100.0, max_val=50.0,
            increment=0.5, value=float(vol), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], floatspin.GetValue())
            
class SetMaxVolume(eg.ActionBase):
    def __call__(self, zone, vol):
        set_max_volume(self.plugin, convert_zone_to_int(self.plugin, zone), float(vol))

    def Configure(self, zone='Active Zone', vol=16.5):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Max Volume (dB): ", pos=(10, 60))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=-30.0, max_val=16.5,
            increment=0.5, value=float(vol), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], floatspin.GetValue())
            
class SetInitVolume(eg.ActionBase):
    def __call__(self, zone, vol, mode):
        set_init_volume(self.plugin, convert_zone_to_int(self.plugin, zone), float(vol), mode)

    def Configure(self, zone='Active Zone', vol=-50.0, mode="Off"):
        panel = eg.ConfigPanel()
        modes = ["Off", "On"]
        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)
        wx.StaticText(panel, label="Mode: ", pos=(10, 60))
        choice_mode = wx.Choice(panel, -1, (10, 80), choices=modes)
        choice_mode.SetStringSelection(mode)
        wx.StaticText(panel, label="Exact Volume (dB): ", pos=(10, 110))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 130), min_val=-100.0, max_val=50.0,
            increment=0.5, value=float(vol), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], floatspin.GetValue(), modes[choice_mode.GetCurrentSelection()])

class SetBass(eg.ActionBase):
    def __call__(self, zone, val):
        set_bass(self.plugin, convert_zone_to_int(self.plugin, zone), float(val))

    def Configure(self, zone='Active Zone', val=0.0):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Exact Value (dB): ", pos=(10, 60))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=-6.0, max_val=6.0,
            increment=0.5, value=float(val), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], floatspin.GetValue())
            
class SetTreble(eg.ActionBase):
    def __call__(self, zone, val):
        set_treble(self.plugin, convert_zone_to_int(self.plugin, zone), float(val))

    def Configure(self, zone='Active Zone', val=0.0):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Exact Value (dB): ", pos=(10, 60))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=-6.0, max_val=6.0,
            increment=0.5, value=float(val), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], floatspin.GetValue())
            
class SetPattern1(eg.ActionBase):
    def __call__(self, levels):
        set_pattern1(self.plugin, levels)

    def Configure(self, levels=None):
        panel = eg.ConfigPanel()
        if levels == None:
            levels = get_system_pattern_1(self.plugin) #gets levels from receiver
        adjpos = (10, 10)
        floatspin = []
        for speaker in levels:
            wx.StaticText(panel, label=speaker[0] + " Exact Value (dB): ", pos=adjpos)
            adjpos = (10, adjpos[1] + 20)
            floatspin.append(FS.FloatSpin(panel, -1, pos=adjpos, min_val=-10.0, max_val=10.0,
                increment=0.5, value=float(speaker[1]), agwStyle=FS.FS_LEFT))
            floatspin[-1].SetFormat("%f")
            floatspin[-1].SetDigits(1)
            adjpos = (10, adjpos[1] + 30)
        while panel.Affirmed():
            for i in range(0,len(floatspin)):
                levels[i] = [levels[i][0], floatspin[i].GetValue()]
            panel.SetResult(levels)
            
class SetActiveZone(eg.ActionBase):
    def __call__(self, zone):
        set_active_zone(self.plugin, convert_zone_to_int(self.plugin, zone))

    def Configure(self, zone='Main Zone'):
        panel = eg.ConfigPanel()
        zones = get_available_zones(self.plugin, False, self.plugin.AVAILABLE_ZONES) # Don't include active zone!
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()])

class SetScene(eg.ActionBase):
    def __call__(self, scene):
        set_scene(self.plugin, int(scene))

    def Configure(self, scene=1):
        panel = eg.ConfigPanel()

        wx.StaticText(panel, label="Scene Number: ", pos=(10, 10))
        spin = wx.SpinCtrl(panel, -1, "", (10, 30), (80, -1))
        spin.SetRange(1,12)
        spin.SetValue(int(scene))
        while panel.Affirmed():
            panel.SetResult(spin.GetValue())

class SetSourceInput(eg.ActionBase):
    def __call__(self, zone, source):
        izone = convert_zone_to_int(self.plugin, zone)
        if source =="Tuner":        #special case.  I don't know why
            source = "TUNER"
        change_source(self.plugin, source, izone)

    def Configure(self, zone="Active Zone", source="HDMI1"):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)
        inputs = self.plugin.AVAILABLE_SOURCES
        wx.StaticText(panel, label="Source Input: ", pos=(10, 60))
        choice_input = wx.Choice(panel, -1, (10, 80), choices=inputs)
        if source in inputs:
            choice_input.SetStringSelection(source)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], inputs[choice_input.GetCurrentSelection()])

class SetPowerStatus(eg.ActionBase):
    def __call__(self, zone, status):
        izone = convert_zone_to_int(self.plugin, zone)
        if status == 'Toggle On/Standby':
            toggle_on_standby(self.plugin, izone)
        elif status == 'On':
            power_on(self.plugin, izone)
        elif status == 'Standby':
            power_standby(self.plugin, izone)

    def Configure(self, zone="Active Zone", status="Toggle On/Standby"):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        statuses = [ 'Toggle On/Standby', 'On', 'Standby' ]
        wx.StaticText(panel, label="Power Status: ", pos=(10, 60))
        choice = wx.Choice(panel, -1, (10, 80), choices=statuses)
        if status in statuses:
            choice.SetStringSelection(status)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], statuses[choice.GetCurrentSelection()])

class SetSleepStatus(eg.ActionBase):
    def __call__(self, zone, status):
        izone = convert_zone_to_int(self.plugin, zone)
        set_sleep(self.plugin, status, izone)

    def Configure(self, zone="Active Zone", status="Off"):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        statuses = [ 'Off', '30 min', '60 min', '90 min', '120 min', 'Last' ]
        wx.StaticText(panel, label="Sleep Status: ", pos=(10, 60))
        choice = wx.Choice(panel, -1, (10, 80), choices=statuses)
        if status in statuses:
            choice.SetStringSelection(status)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], statuses[choice.GetCurrentSelection()])
            
class SetSurroundMode(eg.ActionBase):
    def __call__(self, mode):
        if mode == 'Toggle Straight/Surround Decode':
            toggle_straight_decode(self.plugin)
        elif mode == 'Straight':
            straight(self.plugin)
        elif mode == 'Surround Decode':
            surround_decode(self.plugin)

    def Configure(self, mode='Toggle Straight/Surround Decode'):
        panel = eg.ConfigPanel()

        modes = [ 'Toggle Straight/Surround Decode', 'Straight', 'Surround Decode' ]
        wx.StaticText(panel, label="Surround Mode: ", pos=(10, 10))
        choice = wx.Choice(panel, -1, (10, 30), choices=modes)
        if mode in modes:
            choice.SetStringSelection(mode)
        while panel.Affirmed():
            panel.SetResult(modes[choice.GetCurrentSelection()])

class Set7ChannelMode(eg.ActionBase): # McB 1/11/2014 - Turn 7-channel mode on and off
    def __call__(self, mode):
        if mode == 'On':
            channel7_on(self.plugin)
        elif mode == 'Off':
            channel7_off(self.plugin)

    def Configure(self, mode='On'):
        panel = eg.ConfigPanel()

        modes = [ 'On', 'Off' ]
        wx.StaticText(panel, label="7-Channel Mode: ", pos=(10, 10))
        choice = wx.Choice(panel, -1, (10, 30), choices=modes)
        if mode in modes:
            choice.SetStringSelection(mode)
        while panel.Affirmed():
            panel.SetResult(modes[choice.GetCurrentSelection()])

class CursorAction(eg.ActionBase):
    def __call__(self, action, zone):
        code = None
        izone = convert_zone_to_int(self.plugin, zone, convert_active=True)
        if izone in [0,1]:
            code = globals.CURSOR_CODES[1][action]
        if izone == 2:
            # Not all of the actions are supported for zone 2
            code = globals.CURSOR_CODES[2].get(action, None)

        if code is not None:
            send_code(self.plugin, code)
        else:
            # It is possible the user's active zone is not yet supported
            eg.PrintError("Zone {0} is not yet supported for this action".format(izone if izone > -1 else chr(-1 * izone)))

    def Configure(self, action="Up", zone="Active Zone"):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, globals.ALL_ZONES_PLUS_ACTIVE, limit=2)
        actions = globals.CURSOR_CODES[1].keys()

        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Cursor Action: ", pos=(10, 60))
        choice_action = wx.Choice(panel, -1, (10, 80), choices=actions)
        if action in actions:
            choice_action.SetStringSelection(action)

        while panel.Affirmed():
            panel.SetResult(actions[choice_action.GetCurrentSelection()], zones[choice_zone.GetCurrentSelection()])

class OperationAction(eg.ActionBase):
    def __call__(self, action, zone):
        code = None
        izone = convert_zone_to_int(self.plugin, zone, convert_active=True)
        if izone in [0,1]:
            code = globals.OPERATION_CODES[1][action]
        if izone == 2:
            code = globals.OPERATION_CODES[2][action]

        if code is not None:
            send_code(self.plugin, code)
        else:
            # It is possible the user's active zone is not yet supported
            eg.PrintError("Zone {0} is not yet supported for this action".format(izone if izone > -1 else chr(-1 * izone)))

    def Configure(self, action="Play", zone="Active Zone"):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, globals.ALL_ZONES_PLUS_ACTIVE, limit=2)
        actions = globals.OPERATION_CODES[1].keys()

        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Operation: ", pos=(10, 60))
        choice_action = wx.Choice(panel, -1, (10, 80), choices=actions)
        if action in actions:
            choice_action.SetStringSelection(action)

        while panel.Affirmed():
            panel.SetResult(actions[choice_action.GetCurrentSelection()], zones[choice_zone.GetCurrentSelection()])

class NumCharAction(eg.ActionBase):
    def __call__(self, action, zone):
        code = None
        izone = convert_zone_to_int(self.plugin, zone, convert_active=True)
        if izone in [0,1]:
            code = globals.NUMCHAR_CODES[1][action]
        if izone == 2:
            code = globals.NUMCHAR_CODES[2][action]

        if code is not None:
            send_code(self.plugin, code)
        else:
            # It is possible the user's active zone is not yet supported
            eg.PrintError("Zone {0} is not yet supported for this action".format(izone if izone > -1 else chr(-1 * izone)))

    def Configure(self, action="1", zone="Main Zone"):
        panel = eg.ConfigPanel()

        zones = get_available_zones(self.plugin, True, globals.ALL_ZONES_PLUS_ACTIVE, limit=2)
        actions = sorted(globals.NUMCHAR_CODES[1].keys(), key=lambda k: int(k) if len(k) == 1 else 10 + len(k))

        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Action: ", pos=(10, 60))
        choice_action = wx.Choice(panel, -1, (10, 80), choices=actions)
        if action in actions:
            choice_action.SetStringSelection(action)

        while panel.Affirmed():
            panel.SetResult(actions[choice_action.GetCurrentSelection()], zones[choice_zone.GetCurrentSelection()])

class GetInfo(eg.ActionBase):
    def __call__(self, object, cat):
        if object == "Active Speakers":
            return get_system_pattern_1(self.plugin, object)
        if object == "PreOut Levels":
            return get_system_pattern_1(self.plugin, object)
        zone = None
        #zone specific objects
        if object == "Input Selection":
            object = "Input_Sel"
        if object == "Scene":
            return "not complete"
        if object == "Sound Program":
            object = "Sound_Program"
        if cat == "Main Zone":
            zone = 1
        if cat.startswith("Zone"):
            zone = convert_zone_to_int(self.plugin, cat)
        if object == "Volume Level":
            val, unit = get_status_strings(self.plugin, ["Val", "Unit"], zone)
            return "{0} {1}".format(float(val) / 10.0, unit)
        if object == "Treble":
            val = get_sound_video_string(self.plugin, "Val", zone, "Treble")
            return "{0} ".format(float(val) / 10.0) + "dB"
        if object == "Bass":
            val = get_sound_video_string(self.plugin, "Val", zone, "Bass")
            return "{0} ".format(float(val) / 10.0) + "dB"
        if object == "Init Volume Mode":
            return get_volume_string(self.plugin, "Mode", zone, "Init_Lvl")
        if object == "Init Volume Level":
            val = get_volume_string(self.plugin, "Val", zone, "Init_Lvl")
            return "{0} ".format(float(val) / 10.0) + "dB"
        if object == "Max Volume Level":
            val = get_volume_string(self.plugin, "Val", zone, "Max_Lvl")
            return "{0} ".format(float(val) / 10.0) + "dB"
        if zone is not None:
            return get_status_string(self.plugin, object,zone)

        #all the rest are zone agnostic
        #object, input, location to get_device_string
        section = "List_Info"
        if object in ["Menu Layer", "Menu Name", "Current Line", "Max Line"] \
                or object in ['Line {0}'.format(i) for i in range(9)]:
            object = object.replace(' ', '_')
        else:
            section = "Play_Info"
        if object == "FM Mode":
            object = "FM_Mode"
        elif object == "Frequency":
            try:
                val, unit, band, exp = get_device_strings(self.plugin, ["Val", "Unit", "Band", "Exp"], cat, section)
                if int(exp) == 0:
                    real_val = int(val)
                else:
                    real_val = float(val) / pow(10, int(exp))
                return "{0} {1}".format(real_val, unit)
            except:
                eg.PrintError("Input not active or unavailable with your model.")
                return None
        elif object == "Audio Mode":
            object = "Current"
        elif object == "Antenna Strength":
            object = "Antenna_Lvl"
        elif object == "Channel Number":
            object = "Ch_Number"
        elif object == "Channel Name":
            object = "Ch_Name"
        elif object == "Playback Info":
            object = "Playback_Info"
        elif object == "Repeat Mode":
            object = "Repeat"
        elif object == "Connect Information":
            object = "Connect_Info"

        try:
            return get_device_string(self.plugin, object, cat, section)
        except:
            eg.PrintError("Input not active or unavailable with your model.")


    def Configure(self, object="Power", cat="Main Zone"):
        panel = eg.ConfigPanel()

        self.cats = ["System"] + self.plugin.AVAILABLE_ZONES + self.plugin.AVAILABLE_INFO_SOURCES

        wx.StaticText(panel, label="Category: ", pos=(10, 10))
        self.choice_cat = wx.Choice(panel, -1, (10, 30), choices=self.cats)
        if cat in self.cats:
            self.choice_cat.SetStringSelection(cat)
        self.choice_cat.Bind(wx.EVT_CHOICE, self.CategoryChanged)

        self.objects = [ 'Power', 'Sleep', 'Volume Level', 'Mute', 'Input Selection', 'Scene', 'Straight', 'Enhancer', 'Sound Program']
        wx.StaticText(panel, label="Object: ", pos=(10, 60))
        self.choice_object = wx.Choice(panel, -1, (10, 80), choices=self.objects)
        self.CategoryChanged()
        if object in self.objects:
            self.choice_object.SetStringSelection(object)
            
        while panel.Affirmed():
            panel.SetResult(self.objects[self.choice_object.GetCurrentSelection()], self.cats[self.choice_cat.GetCurrentSelection()])

    def CategoryChanged(self, event=None):
        cat = self.cats[self.choice_cat.GetCurrentSelection()]
        if cat == "System":
            self.objects = globals.SYSTEM_OBJECTS
        elif cat == "Main Zone":
            self.objects = globals.MAIN_ZONE_OBJECTS
        elif cat.startswith("Zone"):
            self.objects = globals.ZONE_OBJECTS
        elif cat == "Tuner" or cat == "TUNER":
            self.objects = [ 'Band', 'Frequency', 'FM Mode']
        elif cat == "HD Radio":
            self.objects = [ 'Band', 'Frequency', 'Audio Mode']
        elif cat == "SIRIUS" or cat == "SiriusXM" or cat == "Spotify":
            self.objects = globals.SIRIUS_OBJECTS
        elif cat == "iPod":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        elif cat == "Bluetooth":
            self.objects = [ 'Connect Information']
        elif cat == "Rhapsody":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        elif cat == "SIRIUSInternetRadio":
            self.objects = globals.SIRIUS_IR_OBJECTS
        elif cat == "Pandora":
            self.objects = globals.PANDORA_OBJECTS
        elif cat == "PC" or "SERVER":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        elif cat == "NET RADIO" or cat == "NET_RADIO":
            self.objects = globals.NET_RADIO_OBJECTS
        elif cat == "Napster":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        elif cat == "USB":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        elif cat == "iPod (USB)" or cat == "iPod_USB" or cat == "Airplay":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        else:
            eg.PrintError("Unknown Category!")
        self.choice_object.Clear()
        self.choice_object.AppendItems(self.objects)
        self.choice_object.SetSelection(0) 

class GetAvailability(eg.ActionBase):
    def __call__(self, **kwargs):
        setup_availability(self.plugin, **kwargs)
        return list(self.plugin.AVAILABLE_SOURCES)

class AutoDetectIP(eg.ActionBase):
    def __call__(self):
        ip = auto_detect_ip_threaded(self.plugin)
        if ip is not None:
            setup_availability(self.plugin)
        return ip

class VerifyStaticIP(eg.ActionBase):
    def __call__(self):
        if self.plugin.ip_auto_detect:
            eg.PrintError('Static IP is not enabled!')
            return False
        else:
            ip = setup_ip(self.plugin)
            if ip is not None:
                setup_availability(self.plugin)
            return ip is not None

class NextInput(eg.ActionBase):
    def __call__(self, zone, inputs):
        print inputs
        izone = convert_zone_to_int(self.plugin, zone, convert_active=True)
        src = get_source_name(self.plugin, izone)
        index = inputs.index(src) if src in inputs else -1
        self._next_input(izone, index, inputs)

    def _next_input(self, izone, cur_index, inputs):
        next_index = 0
        if cur_index != -1:
            if cur_index < len(inputs) - 1:
                next_index = cur_index + 1
            else:
                next_index = 0
        else:
            # Current source not in the user's list. Change to the first item?
            next_index = 0
            print "Warning: Current source was not in the list of sources. Changing to first source in list."
        print "Switching input to", inputs[next_index]
        change_source(self.plugin, inputs[next_index], izone)

        t = Thread(target=self._verify_input, args=[izone, next_index, inputs])
        t.start()

    def _verify_input(self, izone, index, inputs, wait=0.3):
        time.sleep(wait)
        src = get_source_name(self.plugin, izone)
        if src != inputs[index]:
            eg.PrintError("Source input did not change! Your receiver may not have this input.")
            print "Skipping to next input."
            self._next_input(izone, index, inputs)

    def Configure(self, zone='Active Zone', inputs=['HDMI1']):
        panel = eg.ConfigPanel()
        #reset "TUNER" to "Tuner"
        newinputs = []
        for source in inputs:
            if source == "TUNER":
                source = "Tuner"
            newinputs.append(source)
        inputs = newinputs

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (45, 7), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        y = 45
        x_start = 10
        x = x_start
        num_per_row = 5
        x_padding = 80
        y_padding = 20

        sources = self.plugin.AVAILABLE_SOURCES
        self.cbs = []
        for i in range(len(sources)):
            if i > 0 and i % num_per_row == 0:
                x = x_start
                y += y_padding
            cb = wx.CheckBox(panel, -1, sources[i], (x, y))
            cb.SetValue(sources[i] in inputs)
            self.cbs.append(cb)
            x += x_padding

        # Futile attempt at setting a scrollbar, not working
        # panel.SetScrollbar(wx.VERTICAL, 0, 95, 100)

        while panel.Affirmed():
            res = []
            for i in range(len(self.cbs)):
                if self.cbs[i].GetValue():
                    if sources[i] == "Tuner":
                        res.append("TUNER")
                    else:
                        res.append(sources[i])
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], res)

class PreviousInput(eg.ActionBase):
    def __call__(self, zone, inputs):
        izone = convert_zone_to_int(self.plugin, zone, convert_active=True)
        src = get_source_name(self.plugin, izone)
        index = inputs.index(src) if src in inputs else -1
        self._prev_input(izone, index, inputs)

    def _prev_input(self, izone, cur_index, inputs):
        prev_index = 0
        if cur_index != -1:
            if cur_index > 0:
                prev_index = cur_index - 1
            else:
                prev_index = len(inputs) - 1
        else:
            # Current source not in the user's list. Change to the first item?
            prev_index = 0
            print "Warning: Current source was not in the list of sources. Changing to first source in list."
        print "Switching input to", inputs[prev_index]
        change_source(self.plugin, inputs[prev_index], izone)

        t = Thread(target=self._verify_input, args=[izone, prev_index, inputs])
        t.start()

    def _verify_input(self, izone, index, inputs, wait=0.3):
        time.sleep(wait)
        src = get_source_name(self.plugin, izone)
        if src != inputs[index]:
            eg.PrintError("Source input did not change! Your receiver may not have this input.")
            print "Skipping to previous input."
            self._prev_input(izone, index, inputs)

    def Configure(self, zone='Active Zone', inputs=['HDMI1']):
        panel = eg.ConfigPanel()
        #reset "TUNER" to "Tuner"
        newinputs = []
        for source in inputs:
            if source == "TUNER":
                source = "Tuner"
            newinputs.append(source)
        inputs = newinputs

        zones = get_available_zones(self.plugin, True, self.plugin.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (45, 7), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        y = 45
        x_start = 10
        x = x_start
        num_per_row = 5
        x_padding = 80
        y_padding = 20

        sources = self.plugin.AVAILABLE_SOURCES
        self.cbs = []
        for i in range(len(sources)):
            if i > 0 and i % num_per_row == 0:
                x = x_start
                y += y_padding
            cb = wx.CheckBox(panel, -1, sources[i], (x, y))
            cb.SetValue(sources[i] in inputs)
            self.cbs.append(cb)
            x += x_padding

        # Futile attempt at setting a scrollbar, not working
        # panel.SetScrollbar(wx.VERTICAL, 0, 95, 100)

        while panel.Affirmed():
            res = []
            for i in range(len(self.cbs)):
                if self.cbs[i].GetValue():
                    if sources[i] == "Tuner":
                        res.append("TUNER")
                    else:
                        res.append(sources[i])
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], res)

class InputVolumeTrim(eg.ActionBase):
    def __call__(self, sources):
        #sources = get_system_io_vol_trim(self.plugin)
        #print sources
        #sources = [['TUNER', '0'], ['HDMI_1', '0'], ['HDMI_2', '0'], ['HDMI_3', '0'], ['HDMI_4', '0'], ['HDMI_5', '0'], ['AV_1', '0'], ['AV_2', '0'], ['AV_3', '0'], ['AV_4', '0'], ['AV_5', '0'], ['AV_6', '0'], ['V_AUX', '0'], ['AUDIO_1', '0'], ['AUDIO_2', '0'], ['Rhapsody', '0'], ['SiriusXM', '0'], ['Spotify', '0'], ['Pandora', u'0'], ['SERVER', u'0'], ['NET_RADIO', '0'], ['USB', '0'], ['AirPlay', '0']]
        set_system_io_vol_trim(self.plugin, sources)
        
    def Configure(self, sources=None):
        panel = eg.ConfigPanel()
        if sources == None:
            sources = get_system_io_vol_trim(self.plugin)
            
        y = 10
        x_start = 10
        x = x_start
        num_per_row = 3
        x_padding = 110
        y_padding = 45

        self.fss = []
        for i in range(len(sources)):
            print sources[i][0]
            if i > 0 and i % num_per_row == 0:
                x = x_start
                y += y_padding
            wx.StaticText(panel, label=sources[i][0], pos=(x, y))
            fs = FS.FloatSpin(panel, -1, min_val=-6.0, max_val=6.0, increment=0.5, pos=(x, y+15), value=float(sources[i][1]/10), agwStyle=FS.FS_LEFT)
            fs.SetFormat("%f")
            fs.SetDigits(1)
            self.fss.append(fs)
            x += x_padding
            
        while panel.Affirmed():
            res = []
            for i in range(len(self.fss)):
                res.append([sources[i][0], int(self.fss[i].GetValue()*10)])
            panel.SetResult(res)
class ToggleMute(eg.ActionBase):
    def __call__(self):
        toggle_mute(self.plugin)
            
class ToggleEnhancer(eg.ActionBase):
    def __call__(self):
        toggle_enhancer(self.plugin)
        
class NextRadioPreset(eg.ActionBase):
    def __call__(self):
        next_radio_preset(self.plugin)
    
class PreviousRadioPreset(eg.ActionBase):
    def __call__(self):
        prev_radio_preset(self.plugin)
    
class ToggleRadioAMFM(eg.ActionBase):
    def __call__(self):
        toggle_radio_amfm(self.plugin)
            
class RadioAutoFreqUp(eg.ActionBase):
    def __call__(self):
        radio_freq(self.plugin, 'Auto Up')
    
class RadioAutoFreqDown(eg.ActionBase):
    def __call__(self):
        radio_freq(self.plugin, 'Auto Down')
    
class RadioFreqUp(eg.ActionBase):
    def __call__(self):
        radio_freq(self.plugin, 'Up')
        
class RadioFreqDown(eg.ActionBase):
    def __call__(self):
        radio_freq(self.plugin, 'Down')
        

class RadioSetExact(eg.ActionBase):
    def __call__(self, freq, band):
        set_radio_freq(self.plugin, freq, band)
        
    def Configure(self, freq="87.5", band="FM"):
        panel = eg.ConfigPanel()
        self.freq = freq
        self.bands = ['AM', 'FM']
        wx.StaticText(panel, label="Band: ", pos=(10, 10))
        self.choice_band = wx.Choice(panel, -1, (10, 30), choices=self.bands)
        if band in self.bands:
            self.choice_band.SetStringSelection(band)
        self.choice_band.Bind(wx.EVT_CHOICE, self.BandChanged)

        wx.StaticText(panel, label="Frequency: ", pos=(10, 60))
        self.floatspin = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=87.5, max_val=107.9,
            increment=0.2, value=float(freq), agwStyle=FS.FS_LEFT)
        self.floatspin.SetFormat("%f")
        self.floatspin.SetDigits(1)
        
        #self.objects = [ 'Power', 'Sleep', 'Volume Level', 'Mute', 'Input Selection', 'Scene', 'Straight', 'Enhancer', 'Sound Program']
        #wx.StaticText(panel, label="Object: ", pos=(10, 60))
        #self.choice_object = wx.Choice(panel, -1, (10, 80), choices=self.objects)
        self.BandChanged()
        #if object in self.objects:
        #    self.choice_object.SetStringSelection(object)
            
        while panel.Affirmed():
            panel.SetResult(self.floatspin.GetValue(), self.bands[self.choice_band.GetCurrentSelection()])

    def BandChanged(self, event=None):
        band = self.bands[self.choice_band.GetCurrentSelection()]
        if band == "FM":
            self.floatspin.SetRange(min_val=87.5, max_val=107.9)
            if 87.5 <= float(self.freq) and float(self.freq) <= 107.9:
                self.floatspin.SetValue(float(self.freq))
            else:
                self.floatspin.SetValue(float(87.5))
            self.floatspin.SetIncrement(0.2)
        else:
            self.floatspin.SetRange(min_val=530, max_val=1710)
            if 530 <= float(self.freq) and float(self.freq) <= 1710:
                self.floatspin.SetValue(float(self.freq))
            else:
                self.floatspin.SetValue(float(530))
            self.floatspin.SetIncrement(10)
        
class SetFeatureVideoOut(eg.ActionBase):

    def __call__(self, Feature, Source):
        feature_video_out(self.plugin, Feature, Source)
        
    def Configure(self, Feature="Tuner", Source="Off"):
        panel = eg.ConfigPanel()
        self.Source = Source
        if Feature == "TUNER":
            Feature = "Tuner"

        wx.StaticText(panel, label="Feature Input: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (95, 7), choices=self.plugin.AVAILABLE_INFO_SOURCES)
        if Feature in self.plugin.AVAILABLE_INFO_SOURCES:
            choice_zone.SetStringSelection(Feature)

        y = 45
        x_start = 10
        x = x_start
        num_per_row = 5
        x_padding = 80
        y_padding = 20

        sources = ['Off'] + self.plugin.AVAILABLE_INPUT_SOURCES
        self.cbs = []
        for i in range(len(sources)):
            if i > 0 and i % num_per_row == 0:
                x = x_start
                y += y_padding
            cb = wx.CheckBox(panel, -1, sources[i], (x, y))
            if Source == sources[i]:
                cb.SetValue(True)
            else:
                cb.SetValue(False)
            cb.Bind(wx.EVT_CHECKBOX, lambda evt, temp=i: self.SourceChanged(evt, temp))
            self.cbs.append(cb)
            x += x_padding

        while panel.Affirmed():
            for i in range(len(self.cbs)):
                if self.cbs[i].GetValue():
                    res = sources[i]
            if self.plugin.AVAILABLE_INFO_SOURCES[choice_zone.GetCurrentSelection()] == "Tuner":
                xx = "TUNER"
            else:
                xx = self.plugin.AVAILABLE_INFO_SOURCES[choice_zone.GetCurrentSelection()]
            panel.SetResult(xx, res)
            
    def SourceChanged(self, event, item):
        sources = ['Off'] + self.plugin.AVAILABLE_INPUT_SOURCES
        self.Source = sources[item]
        for i in range(len(sources)):
            if i == item:
                self.cbs[i].SetValue(True)
            else:
                self.cbs[i].SetValue(False)

class SetDisplayDimmer(eg.ActionBase):

    def __call__(self, level):
        levels = ['100%','75%','50%','25%','10%']
        lev = levels.index(level)
        DisplayDimmer(self.plugin, int(lev)*-1)

    def Configure(self, level='100%'):
        panel = eg.ConfigPanel()

        levels = ['100%','75%','50%','25%','10%']
        wx.StaticText(panel, label="Brightness: ", pos=(10, 10))
        choice_level = wx.Choice(panel, -1, (10, 50), choices=levels)
        if level in levels:
            choice_level.SetStringSelection(level)
        while panel.Affirmed():
            panel.SetResult(levels[choice_level.GetCurrentSelection()])
            
class SetAudioIn(eg.ActionBase):

    def __call__(self, Audio, Source):
        source_audio_in(self.plugin, Audio, Source)
        
    def Configure(self, Audio="HDMI1", Source="HDMI_1"):
        panel = eg.ConfigPanel()
        self.Source = Source[:-2] + Source[-1:]
        print self.Source
        self.VidChoices = []
        PosChoices = ['HDMI1', 'HDMI2', 'HDMI3', 'HDMI4', 'HDMI5', 'HDMI6', 'HDMI7', 'HDMI8', 'HDMI9', 'AV1', 'AV2']
        for x in PosChoices:
            if x in self.plugin.AVAILABLE_SOURCES:
                self.VidChoices.append(x)
        wx.StaticText(panel, label="Video Input: ", pos=(10, 10))
        self.choice_video = wx.Choice(panel, -1, (95, 7), choices=self.VidChoices)
        if self.Source in self.VidChoices:
            self.choice_video.SetStringSelection(self.Source)
        self.choice_video.Bind(wx.EVT_CHOICE, self.VidChanged)
        
        PosSources = ['AV1', 'AV2', 'AV3', 'AV4', 'AV5', 'AV6', 'AV7', 'AV8', 'AV9', 'AUDIO1', 'AUDIO2']
        self.AudChoices = [self.Source]
        for x in PosSources:
            if x in self.plugin.AVAILABLE_SOURCES:
                self.AudChoices.append(x)
        wx.StaticText(panel, label="Audio Input: ", pos=(10, 40))
        self.choice_audio = wx.Choice(panel, -1, (95, 37), choices=self.AudChoices)
        if Audio in self.AudChoices:
            self.choice_audio.SetStringSelection(Audio)
         
        while panel.Affirmed():
            vid = self.VidChoices[self.choice_video.GetCurrentSelection()]
            vid = vid[:-1] + "_" + vid[-1:]
            panel.SetResult(self.AudChoices[self.choice_audio.GetCurrentSelection()], vid)
            
    def VidChanged(self, event):
        self.AudChoices[0] = self.VidChoices[self.choice_video.GetCurrentSelection()]
        self.choice_audio.Clear()
        self.choice_audio.AppendItems(self.AudChoices)
        self.choice_audio.SetSelection(0)
        
class SetWallPaper(eg.ActionBase):
    def __call__(self, Pic):
        wallpaper(self.plugin, Pic)
        
    def Configure(self, Pic="Picture 1"):
        panel = eg.ConfigPanel()
        PicChoices = ['Picture 1', 'Picture 2', 'Picture 3', 'Gray']
        wx.StaticText(panel, label="Background Image: ", pos=(10, 10))
        choice_pic = wx.Choice(panel, -1, (10, 30), choices=PicChoices)
        if Pic in PicChoices:
            choice_pic.SetStringSelection(Pic)
        
        while panel.Affirmed():
            panel.SetResult(PicChoices[choice_pic.GetCurrentSelection()])
            
class SendAnyCommand(eg.ActionBase):
    def __call__(self, value, action):
        if action == "Put":
            send_any(self.plugin, value, action)
        else:
            result = send_any(self.plugin, value, action)
            print result
            return result
        
    def Configure(self, value="", action="Put"):
        panel = eg.ConfigPanel()
        wx.StaticText(panel, label="Command: ", pos=(10, 10))
        CommandCtrl = wx.TextCtrl(panel, pos=(10, 30), size=(420,-1))
        wx.StaticText(panel, label="Ex: <Main_Zone><Basic_Status><Volume><Lvl><Val>***</Val></Lvl>", pos=(10, 70))
        wx.StaticText(panel, label="    <Exp>1</Exp><Unit>dB</Unit></Lvl></Volume></Basic_Status></Main_Zone>", pos=(10, 90))
        CommandCtrl.SetValue(value)
        Choices = ['Put', 'Get']
        ChoiceCtrl = wx.Choice(panel, -1, (10, 110), choices=Choices)
        ChoiceCtrl.SetStringSelection(action)
        wx.StaticText(panel, label="***If Get is selected make sure GetParam is in place of value", pos=(10, 150))
        
        while panel.Affirmed():
            panel.SetResult(CommandCtrl.GetValue(),Choices[ChoiceCtrl.GetCurrentSelection()])

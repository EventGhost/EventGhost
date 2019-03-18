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
# This plugin is an HTTP client and Server that sends and receives MiCasaVerde UI5 and UI7 states.
# This plugin is based on the Vera plugins by Rick Naething, well kinda sorta,

def HVACMinMax(unit):
    if unit == 'C': return [int((50-32)*5.0/9.0), int((90-32)*5.0/9.0)]
    else: return [50, 90]

class Text:
    class Vera:
        DeviceBox      = 'Device'
        DeviceText     = 'Device: '
        PluginBox      = 'Plugin Config Settings'
        VeraBox        = 'Vera IP and Port Settings'
        PrefixBox      = 'Event Prefix / Generation Settings'   
        UpdateBox      = 'Vera Update Speed Settings'
        WattsFPBox     = 'Watts File Settings'
        MonitorBox     = 'Monitor Default Settings'
        MonitorSubBox  = 'Monitor '
        PrefixText     = 'Event Prefix: '
        VeraBox        = 'Vera IP and Port Settings'
        VeraIPText     = 'IP: '
        VeraPortText   = 'Port: '
        MinEvtText     = 'Reduce Events: '
        EvtPayText     = 'Generate Payload Data: '
        UpSpeedText    = 'Seconds: '
        WattsFPText    = 'Watts File: '
        WidthText      = 'Width: '
        HeightText     = 'Height: '
        FPMText        = 'Frames Per Minute: '
        CameraMonBox   = 'Monitor / Refresh Settings '
        ColorText      = 'Color: '
        FontText       = 'Font: '
        DataButton     = 'All Vera Data'
        AddOnButton    = 'Add On\'s'


    class DimmerStatus:
        name           = 'Level of a Dimmer'
        description    = 'Get the Current Level of a Dimmer Switch'
        DimmStBox      = 'Get Dimmer Level'

    class RampDimmer:
        name           = 'Ramp Dimmable Light'
        description    = 'Control the Speed and Brightness as a Dimmer Turns on or Off'
        RampDmBox      = 'Ramp Dimmer Up or Down'
        StrtText       = 'Start Percent: '
        StopText       = 'Stop Percent: '
        IncrText       = 'Brightness Steps: '
        SpedText       = 'Speed: '
        CurrBox        = "Current Level"
        CurrText       = "Current Level: "
        UseCurrText    = "Use Level as Start"

    class Scene:
        name           = 'Run Scene'
        description    = 'Runs a Vera Scene'
        ScenesBox      = 'Run A Scene'
        ScenesText     = 'Scene: '

    class Dimmer:
        name           = 'Set Light Level'
        description    = 'Set the Dim Level of a Dimmable Switch'
        DimmerBox      = 'Set the Dim Level of a Dimmable Switch'
        DimmerText     = 'Level: '
        Choice         = [str(i)+'%' for i in range(101)]

    class Switch:
        name           = 'Switch Power'
        description    = 'Turn a Light or Binary Switch ON or OFF'
        SwitchBox      = 'Turn a Light or Binary Switch On or Off'
        SwitchText     = 'ON or OFF: '
        Choice         = ["Off","On"]

    class Toggle:
        name           = 'Toggle Power'
        description    = 'Toggle a Light or Binary Switch to Opposite of Current State'
        ToggleBox      = 'Toggle a Light or Binary Switch'

    class HVAC:
        
        name           = 'HVAC Controls'
        description    = 'Control Heating and Cooling'
        HVACText       = 'HVAC Control'
        FanModBox      = 'HVAC Fan Mode'
        FanModText     = 'Fan Mode: '
        FanChoice      = ["Auto","PeriodicOn","ContinuousOn","FollowSchedule"]
        OppModBox      = 'HVAC Opperating Mode'
        OppModText     = 'Opperating Mode: '
        OppChoice      = ["Off","CoolOn","HeatOn","AutoChangeOver"]
        HStTmpBox      = 'HVAC Heat Set Temperature'
        HStTmpText     = 'Set Teperature: '
        SetTmpChoiceF   = [str(i)+'\xb0' for i in range(*HVACMinMax('F'))]
        SetTmpChoiceC   = [str(i)+'\xb0' for i in range(*HVACMinMax('C'))]
        CStTmpBox      = 'HVAC Cool Set Temperature'
        CStTmpText     = 'Set Teperature: '
        CurrTempText   = 'Current Temp: '
        CurrOppMText   = 'Current Opperating Mode: '
        CurrOppSText   = 'Current Opperating State: '
        CurrFanMText   = 'Current Fan Mode: '
        CurrFanSText   = 'Current Fan State: '
        CurrCoolText   = 'Current Cool Set Temp: '
        CurrHeatText   = 'Current Heat Set Temp: '
        RealTimeText   = 'Make Settings Real Time: '
        
    class Alarm:
        name           = 'Alarm Control'
        description    = 'Arm or Disarm your Security System'
        AlarmsBox      = 'Arm or Disarm Alarm'
        AlarmsText     = 'Arm or Disarm: '
        Choice         = ["DISARM","ARM"]

    class DoorLock:
        name           = 'Door Lock Control'
        description    = 'Lock or Unlock Your Doors'
        LockText       = "Door: "
        Choice         = ["Unlocked", "Locked"]
        LockBox        = "Door Locks"

    class DisplayMenu:
        name                = 'Menu System'
        description         = 'Display On Screen Menu System'
        OtherBox            = 'Other Settings'
        menuTimeText        = 'Menu TimeOut: '
        FadeInText          = 'Fade in Steps: '
        FadeOutText         = 'Fade Out Steps: '
        MonitorText         = 'Display Monitor: '
        FontBox             = 'Font Settings'
        FontText            = 'Font: '
        FontColorText       = 'Font Color: '
        SelectFontColorText = 'Selected Font Color: '
        BackBox             = 'Background Settings'
        BackColortext       = 'Background Color: '
        TransparencyText    = 'Background Transparency: '
        BorderBox           = "Border Settings"
        BorderWidthText     = 'Border Width: '
        BorderColorText     = 'Border Color: '
        DimensionBox        = 'Menu Dimensions'
        DimensionDesc       = 'Sizes are based on a percentage of the screen size'
        WidthText           = 'Menu Width: '
        HeightText          = 'Menu Height: '
        BorderTransText     = 'Border Transparency: '
        BorderCornerText    = 'Border Corner Radius: '
        WindowTransText     = 'Window Transparency'

class STATIC:
    URLS = {
        'dimmer'      : ['action&DeviceNum=', '&serviceId=urn:upnp-org:serviceId:Dimming1&action=SetLoadLevelTarget&newLoadlevelTarget='],
        'switch'      : ['action&DeviceNum=', '&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue='],
        'toggle'      : ['action&DeviceNum=', '&serviceId=urn:micasaverde-com:serviceId:HaDevice1&action=ToggleState'],
        'scene'       : ['action&serviceId=urn:micasaverde-com:serviceId:HomeAutomationGateway1&action=RunScene&SceneNum='],
        'hvacFanMode' : ['action&DeviceNum=', '&serviceId=urn:upnp-org:serviceId:HVAC_FanOperatingMode1&action=SetMode&NewMode='],
        'hvacOppMode' : ['action&DeviceNum=', '&serviceId=urn:upnp-org:serviceId:HVAC_UserOperatingMode1&action=SetModeTarget&NewModeTarget='],
        'hvacSetTempC': ['action&DeviceNum=', '&serviceId=urn:upnp-org:serviceId:TemperatureSetpoint1_Cool&action=SetCurrentSetpoint&NewCurrentSetpoint='], 
        'hvacSetTempH': ['action&DeviceNum=', '&serviceId=urn:upnp-org:serviceId:TemperatureSetpoint1_Heat&action=SetCurrentSetpoint&NewCurrentSetpoint='],
        'alarm'       : ['action&output_format=xml&Category=4&serviceId=urn:micasaverde-com:serviceId:SecuritySensor1&action=SetArmed&newArmedValue='],
        'doorLock'    : ['variableset&DeviceNum=', '&serviceId=urn:micasaverde-com:serviceId:DoorLock1&Variable=Status&Value='],
        'videoCamera' : ['request_image&Device_Num=', 'res='],
        'userData'    : ['user_data&output_format=xml'],
        'summarydata' : ['sdata&loadtime=', '&dataversion=', '&output_format=xml'],
        'deviceData'  : ['status&output_format=xml'], #**** Alerts
        'deviceStatus': ['status&output_format=xml&DeviceNum='],
        'webData'     : ['invoke'],                                                                                    
        'liveEnergy'  : ['live_energy_usage'],
        'createRoom'  : ['room&action=create&name='],
        'renameRoom'  : ['room&action=rename&name='],
        'deleteRoom'  : ['room&action=delete&room='],
        'allLights'   : ['action&output_format=xml&Category=999&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=']
    }
    CATEGORIES = {
        '-5': 'Scene',
        '-4': 'Category',
        '-3': 'Room',
        '-2': 'Hub',
        '-1': 'System',
        '0' : 'Plugin',
        '1' : 'Interface',
        '2' : 'Dimmable-Switch',
        '3' : 'Switch',
        '4' : 'Sensor',
        '5' : 'Thermostat',
        '6' : 'Camera',
        '7' : 'Door-Lock',
        '8' : 'Window-Covering',
        '9' : 'Remote',
        '10': 'IR-Transmitter',
        '11': 'Generic-I/O',
        '12': 'Generic-Sensor',
        '13': 'Serial-Port',
        '14': 'Scene-Controller',
        '15': 'Audio/Video',
        '16': 'Humidity-Sensor',
        '17': 'Temperature-Sensor',
        '18': 'Light-Sensor',
        '19': 'Z-Wave-Interface',
        '20': 'Insteon-Interface',
        '21': 'Power-Meter',
        '22': 'Alarm-Panel',
        '23': 'Alarm-Partition',
        '24': 'Siren',
        '25': 'Weather',
        '26': 'Philips-Controller',
        '27': 'Plugin'
    }
    ALLOWEDEVENTS = {
        '-5': { 'name'         : ['Name'],
                'room'         : ['Room'],
                'active'       : [['All Devices Off', 'Device On']]},
        '-4': { 'name'         : ['Name']},
        '-3': { 'name'         : ['Name'],
                'section'      : ['Section']},
        '-2': { 'name'         : ['Name']},
        '-1': { 'version'      : ['Version'],
                'temperature'  : ['Temperature'],
                'zwave_heal'   : ['Z Wave Heal'],
                'ir'           : ['IR'],
                'model'        : ['Model'],
                'serial_number': ['Serial Number']},
        '0':  { 'name'         : ['Name'],
                'room'         : ['Room'],
                'uv'           : ['UV Index'],
                'dew'          : ['Dew Point'],
                'feels'        : ['Heat Index'],
                'solar'        : ['Solar Index'],
                'pressure'     : ['Pressure'],
                'humidity'     : ['Humidity'],
                'windgust'     : ['Wind Gust'],
                'condition'    : ['Current Condition'],
                'windchill'    : ['Wind Chill'],
                'windspeed'    : ['Wind Speed'],
                'temperature'  : ['Temperature'],
                'windcondition': ['Wind Condition'],
                'winddirection': ['Wind Direction']},
        '1':  {},
        '2':  { 'name'         : ['Name'],
                'room'         : ['Room'],
                'level'        : ['Level'],
                'status'       : [['Off', 'On']],
                'watts'        : ['Watts Used']},
        '3':  { 'name'         : ['Name'],
                'room'         : ['Room'],
                'status'       : [['Off', 'On']],
                'watts'        : ['Watts Used']},
        '4':  { 'name'         : ['Name'],
                'room'         : ['Room'],
                'armed'        : [['Disarmed', 'Armed']],
                'humidity'     : ['Humidity'],
                'temperature'  : ['Temperature'],
                'armedtripped' : ['Sensor Fault'],
                'batterylevel' : ['Sensor Battery Level']},
        '5':  { 'name'         : ['Name'],
                'room'         : ['Room'],
                'fan'          : ['Fan'],
                'mode'         : ['Mode'],
                'fanmode'      : ['Fan Mode'],
                'humidity'     : ['Humidity'],
                'coolsp'       : ['Cool SetPoint'],
                'cool'         : ['Cool SetPoint'],
                'hvacstate'    : ['HVAC State'],
                'heatsp'       : ['Heat SetPoint'],
                'heat'         : ['Heat SetPoint'],
                #'setpoint'     : ['SetPoint'],
                'temperature'  : ['Temperature']},
        '6':  { 'name'         : ['Name'],
                'room'         : ['Room']},
        '7':  { 'name'         : ['Name'],
                'room'         : ['Room'],
                'locked'       : [['Unlocked', 'Locked']]},
        '8':  { 'name'         : ['Name'],
                'room'         : ['Room']},
        '9':  { 'name'         : ['Name'],
                'room'         : ['Room']},
        '10': { 'name'         : ['Name'],
                'room'         : ['Room']},
        '11': { 'name'         : ['Name'],
                'room'         : ['Room']},
        '12': { 'name'         : ['Name'],
                'room'         : ['Room'],
                'armed'        : [['Disarmed', 'Armed']],
                'humidity'     : ['Humidity'],
                'temperature'  : ['Temperature'],
                'armedtripped' : ['Sensor Fault'],
                'batterylevel' : ['Sensor Battery Level']},
        '13': { 'name'         : ['Name'],
                'room'         : ['Room']},
        '14': { 'name'         : ['Name'],
                'room'         : ['Room'],
                'active'       : [['All Devices Off', 'Device On']]},
        '15': { 'name'         : ['Name'],
                'room'         : ['Room']},
        '16': { 'name'         : ['Name'],
                'room'         : ['Room'],
                'humidity'     : ['Humidity']},
        '17': { 'name'         : ['Name'],
                'room'         : ['Room'],
                'temperature'  : ['Temperature']},
        '18': { 'name'         : ['Name'],
                'room'         : ['Room']},
        '19': { 'name'         : ['Name'],
                'room'         : ['Room']},
        '20': { 'name'         : ['Name'],
                'room'         : ['Room']},
        '21': { 'name'         : ['Name'],
                'room'         : ['Room'],
                'watts'        : ['Watts Used']},
        '22': { 'name'         : ['Name'],
                'room'         : ['Room'],
                'armed'        : [['Disarmed', 'Armed']]},
        '23': { 'name'         : ['Name'],
                'room'         : ['Room']},
        '24': { 'name'         : ['Name'],
                'room'         : ['Room']},
        '25': { 'name'         : ['Name'],
                'room'         : ['Room'],
                'uv'           : ['UV Index'],
                'dew'          : ['Dew Point'],
                'feels'        : ['Heat Index'],
                'solar'        : ['Solar Index'],
                'pressure'     : ['Pressure'],
                'humidity'     : ['Humidity'],
                'windgust'     : ['Wind Gust'],
                'condition'    : ['Current Condition'],
                'windchill'    : ['Wind Chill'],
                'windspeed'    : ['Wind Speed'],
                'temperature'  : ['Temperature'],
                'windcondition': ['Wind Condition'],
                'winddirection': ['Wind Direction']},
        '26': { 'name'         : ['Name'],
                'room'         : ['Room']},
        '27': { 'name'         : ['Name'],
                'room'         : ['Room']}

    }

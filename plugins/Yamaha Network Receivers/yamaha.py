# Python Imports
from xml.dom import minidom
from threading import Thread, Timer
import time

# Local Imports
import globals
from helpers import *
from yamaha_xml import *

def send_any(self, value, action):
    if action == "Put":
        put_xml(self, value)
    else:
        #now find param
        #to do this, parse value (originally passed)
        param = value.split("GetParam")
        param = param[0].split("<")
        param = param[-1]
        param = param[0:-1]
        values = value.split("<" + param + ">")
        values2 = values[1].split("</" + param + ">")
        value = values[0] + "GetParam" + values2[1]
        xml = get_xml(self, value)
        xmldoc = minidom.parseString(xml)

        return xmldoc.getElementsByTagName(param)[0].firstChild.data


def increase_volume(self, zone=-1, inc=0.5):
    change_volume(self, zone, inc)

def decrease_volume(self, zone=-1, dec=0.5):
    change_volume(self, zone, -1 * dec)

def change_volume(self, zone=-1, diff=0.0):
    if abs(diff) == 0.5 or int(abs(diff)) in [1, 2, 5]:
        # Faster volume method which uses the built in methods
        param1 = 'Up' if diff > 0 else 'Down'
        param2 = ' {0} dB'.format(int(abs(diff))) if abs(diff) != 0.5 else ''
        zone_put_xml(self, zone, '<Volume><Lvl><Val>{0}{1}</Val><Exp></Exp><Unit></Unit></Lvl></Volume>'.format(param1, param2))
        # Sleep for a little amount of time to ensure we do not get "stuck" sending too many calls in short succession
        time.sleep(0.03)
    else:
        # Slower method that relies on get_volume() first
        set_volume(self, zone, (get_volume(self) / 10.0) + diff)

def get_volume(self):
    return get_status_int(self, 'Val')

def set_volume(self, zone=-1, value=-25.0):
    zone_put_xml(self, zone, '<Volume><Lvl><Val>{0}</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume>'.format(int(value * 10.0)))
    
def set_max_volume(self, zone=-1, value=16.5):
    zone_put_xml(self, zone, '<Volume><Max_Lvl><Val>{0}</Val><Exp>1</Exp><Unit>dB</Unit></Max_Lvl></Volume>'.format(int(value * 10.0)))
    
def set_init_volume(self, zone=-1, value=-50.0, mode="Off"):
    zone_put_xml(self, zone, '<Volume><Init_Lvl><Mode>{1}</Mode><Lvl><Val>{0}</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Init_Lvl></Volume>'.format(int(value * 10.0), mode))
    
def set_pattern1(self, levels):
    for speaker in levels:
        put_xml(self, '<System><Speaker_Preout><Pattern_1><Lvl><{0}><Val>{1}</Val><Exp>1</Exp><Unit>dB</Unit></{0}></Lvl></Pattern_1></Speaker_Preout></System>'.format(speaker[0], int(speaker[1]*10)))
    
def set_bass(self, zone=-1, value=-0.0):
    zone_put_xml(self, zone, '<Sound_Video><Tone><Bass><Val>{0}</Val><Exp>1</Exp><Unit>dB</Unit></Bass></Tone></Sound_Video>'.format(int(value * 10.0)))
    
def set_treble(self, zone=-1, value=-0.0):
    zone_put_xml(self, zone, '<Sound_Video><Tone><Treble><Val>{0}</Val><Exp>1</Exp><Unit>dB</Unit></Treble></Tone></Sound_Video>'.format(int(value * 10.0)))

def mute_on(self, zone=-1):
    zone_put_xml(self, zone, '<Volume><Mute>On</Mute></Volume>')

def mute_off(self, zone=-1):
    zone_put_xml(self, zone, '<Volume><Mute>Off</Mute></Volume>')

def get_mute(self, zone=-1):
    return get_status_param_is_on(self, 'Mute', zone)

def power_on(self, zone=-1):
    zone_put_xml(self, zone, '<Power_Control><Power>On</Power></Power_Control>')

def power_off(self, zone=-1):
    zone_put_xml(self, zone, '<Power_Control><Power>Off</Power></Power_Control>')

def power_standby(self, zone=-1):
    zone_put_xml(self, zone, '<Power_Control><Power>Standby</Power></Power_Control>')

def toggle_on_standby(self, zone=-1):
    zone_put_xml(self, zone, '<Power_Control><Power>On/Standby</Power></Power_Control>')

def toggle_mute(self, zone=-1):
    if get_mute(self, zone):
        mute_off(self, zone)
    else:
        mute_on(self, zone)

def change_source(self, source, zone=-1):
    #first look to see if the source has been renamed
    for s in self.AVAILABLE_SOURCES_RENAME:
        if source == s[1]:
            source = s[0]
    zone_put_xml(self, zone, '<Input><Input_Sel>{0}</Input_Sel></Input>'.format(source))

def feature_video_out(self, feature, source):
    #first look to see if the source has been renamed
    for s in self.AVAILABLE_SOURCES_RENAME:
        if source == s[1]:
            source = s[0]
    #first look to see if the source has been renamed
    for s in self.AVAILABLE_SOURCES_RENAME:
        if feature == s[1]:
            feature = s[0]
    put_xml(self, '<System><Input_Output><Assign><Video_Out><{0}>{1}</{0}></Video_Out></Assign></Input_Output></System>'.format(feature, source))
    
def source_audio_in(self, audio, video):
    #first look to see if the source has been renamed
    for s in self.AVAILABLE_SOURCES_RENAME:
        if audio == s[1]:
            audio = s[0]
    #first look to see if the source has been renamed
    for s in self.AVAILABLE_SOURCES_RENAME:
        if video == s[1]:
            video = s[0]
    put_xml(self, '<System><Input_Output><Assign><Audio_In><{0}>{1}</{0}></Audio_In></Assign></Input_Output></System>'.format(video, audio))
    
def wallpaper(self, pic):
    put_xml(self, '<System><Misc><Display><Wall_Paper>{0}</Wall_Paper></Display></Misc></System>'.format(pic))
    
def DisplayDimmer(self, level):
    put_xml(self, '<System><Misc><Display><FL><Dimmer>{0}</Dimmer></FL></Display></Misc></System>'.format(level))

def straight(self, zone=-1):
    zone_put_xml(self, zone, '<Surround><Program_Sel><Current><Straight>On</Straight><Sound_Program>Straight</Sound_Program></Current></Program_Sel></Surround>')

def surround_decode(self, zone=-1):
    zone_put_xml(self, zone, '<Surround><Program_Sel><Current><Straight>Off</Straight><Sound_Program>Surround Decoder</Sound_Program></Current></Program_Sel></Surround>')

def toggle_straight_decode(self, zone=-1):
    if get_straight(self, zone):
        surround_decode(self, zone)
    else:
        straight(self, zone)

def get_straight(self, zone=-1):
    return get_status_param_is_on(self, 'Straight', zone)

def channel7_on(self, zone=-1): # McB 1/11/2014 - Turn 7-channel mode on and off
    zone_put_xml(self, zone, '<Surround><Program_Sel><Current><Sound_Program>7ch Stereo</Sound_Program></Current></Program_Sel></Surround>')

def channel7_off(self, zone=-1):
    zone_put_xml(self, zone, '<Surround><Program_Sel><Current><Sound_Program>Standard</Sound_Program></Current></Program_Sel></Surround>')

def set_enhancer(self, arg, zone=-1):
    zone_put_xml(self, zone, '<Surround><Program_Sel><Current><Enhancer>{0}</Enhancer></Current></Program_Sel></Surround>'.format(arg))

def get_enhancer(self, zone=-1):
    return get_status_param_is_on(self, 'Enhancer', zone)

def toggle_enhancer(self):
    if get_enhancer(self):
        set_enhancer(self, "Off")
    else:
        set_enhancer(self, "On")

def set_sleep(self, arg, zone=-1):
    zone_put_xml(self, zone, '<Power_Control><Sleep>{0}</Sleep></Power_Control>'.format(arg))

def set_radio_preset(self, preset):
    put_xml(self, '<Tuner><Play_Control><Preset><Preset_Sel>{0}</Preset_Sel></Preset></Play_Control></Tuner>'.format(preset))

def get_radio_band(self):
    return get_tuner_string(self, 'Band')

def toggle_radio_amfm(self):
    if get_radio_band(self) == 'FM':
        set_radio_band(self, 'AM')
    else:
        set_radio_band(self, 'FM')

def set_radio_band(self, band):
    put_xml(self, '<Tuner><Play_Control><Tuning><Band>{0}</Band></Tuning></Play_Control></Tuner>'.format(band))

def next_radio_preset(self):
    put_xml(self, '<Tuner><Play_Control><Preset><Preset_Sel>Up', close_xml=True)

def prev_radio_preset(self):
    put_xml(self, '<Tuner><Play_Control><Preset><Preset_Sel>Down', close_xml=True)

def modify_radio_preset(self, diff, turn_on, wrap):
    """
    Deprecated
    """
    oldpreset = get_tuner_int(self, 'Preset_Sel')
    preset = oldpreset + diff
    set_radio_preset(self, preset)
    if turn_on:
        is_on = is_radio_on(self)
        if not is_on:
            change_source('TUNER')
    if wrap and (not turn_on or is_on):
        count = get_radio_preset_count(self)
        if diff > 0 and preset > count:
            preset = 1
            set_radio_preset(self, preset)
        elif diff < 0 and preset < 1:
            preset = count
            set_radio_preset(self, preset)

def get_radio_preset_count(**kwargs):
    """
    Currently broken
    """
    xml = get_tuner_presets(self, **kwargs)
    if kwargs.get('print_xml', False):
        print xml
    xmldoc = minidom.parseString(xml)
    count = 0
    done = False
    while not done and count <= 40:
        num = "Number_{0}".format(count + 1)
        value = xmldoc.getElementsByTagName(num)[0].getElementsByTagName('Status')[0].firstChild.data
        if value == 'Exist':
            count += 1
        else:
            done = True
    return count

def is_radio_on(self):
    return get_status_string(self, 'Input_Sel') == "TUNER"

def radio_freq(self, updown):
    if get_radio_band(self) == 'FM':
        val = '<FM><Val>{0}</Val></FM>'.format(updown)
    else:
        val = '<AM><Val>{0}</Val></AM>'.format(updown)
    put_xml(self, '<Tuner><Play_Control><Tuning><Freq>{0}</Freq></Tuning></Play_Control></Tuner>'.format(val))

def set_radio_freq(self, freq, band):
    if band == 'FM':
        put_xml(self, '<Tuner><Play_Control><Tuning><Freq><FM><Val>{0}</Val></FM></Freq></Tuning></Play_Control></Tuner>'.format(int(freq*100)))
    else:
        put_xml(self, '<Tuner><Play_Control><Tuning><Freq><AM><Val>{0}</Val></AM></Freq></Tuning></Play_Control></Tuner>'.format(int(freq)))

def set_scene(self, scene_num, zone=-1):
    zone_put_xml(self, zone, '<Scene><Scene_Sel>Scene {0}</Scene_Sel></Scene>'.format(scene_num))

def send_code(self, code):
    put_xml(self, '<System><Misc><Remote_Signal><Receive><Code>{0}</Code></Receive></Remote_Signal></Misc></System>'.format(code))

def set_active_zone(self, zone):
    self.active_zone = zone
    print "Active Zone: Zone", zone if zone > -1 else chr(-1 * zone)

def get_source_name(self, zone=-1):
    return get_status_string(self, "Input_Sel", zone)

def get_system_config(self, **kwargs):
    xml = get_config(self, **kwargs)
    xmldoc = minidom.parseString(xml)
    return xmldoc
    
def get_system_io_vol_trim(self):
    sources = []
    xml = get_xml(self, '<System><Input_Output><Volume_Trim>GetParam</Volume_Trim></Input_Output></System>')
    print xml
    print type(xml)
    if not xml:
        return []
    xmldoc = minidom.parseString(xml)
    for item in xmldoc.getElementsByTagName('Val'):
        sources.append([item.parentNode.tagName, item.firstChild.data])
    return sources
    
def set_system_io_vol_trim(self, sources):
    for source in sources:
        put_xml(self, '<System><Input_Output><Volume_Trim><{0}><Val>{1}</Val><Exp>1</Exp><Unit>dB</Unit></{0}></Volume_Trim></Input_Output></System>'.format(source[0], source[1]))
    
def get_main_zone_inputs(self):
    xml = get_xml(self, '<Main_Zone><Input><Input_Sel_Item>GetParam</Input_Sel_Item></Input></Main_Zone>')
    xmldoc = minidom.parseString(xml)
    return xmldoc
    
def get_availability_dict(self, items_to_check):
    xml = get_config(self)
    xmldoc = minidom.parseString(xml)
    res = {}
    for item in items_to_check:
        try:
            value = xmldoc.getElementsByTagName(item)[0].firstChild.data
        except:
            value = None
        res[item] = value
    return res

# Python Imports
from xml.dom import minidom
import httplib

# Local Imports
import globals
from helpers import *

def do_xml(self, xml, **kwargs):
    """
    Base function to send/receive xml using either GET or POST

    Optional Parameters:
    timeout, ip, port, return_result, print_error, close_xml, print_xml, retry_count, print_response
    """
    timeout = float(kwargs.get('timeout', self.default_timeout))
    ip = kwargs.get('ip', self.ip_address)
    port = kwargs.get('port', self.port)
    return_result = kwargs.get('return_result', False)
    print_error = kwargs.get('print_error', True)
    close_xml = kwargs.get('close_xml', False)
    print_xml = kwargs.get('print_xml', False)
    retry_count = kwargs.get('retry_count', 0)  #used for retry errors
    print_response = kwargs.get('print_response', False)  #used for returning raw xml response

    if close_xml:
        xml = close_xml_tags(xml)
    if print_xml:
        print xml

    conn = httplib.HTTPConnection('{0}:{1}'.format(ip, port), timeout=float(timeout))
    headers = { "Content-type": "text/xml" }
    try:
        conn.request("POST", "/YamahaRemoteControl/ctrl", "", headers)
        conn.send(xml)
        if return_result:
            response = conn.getresponse()
            rval = response.read()
            if print_response:
                print rval
            conn.close()
            return rval
        else:
            response = conn.getresponse()
            rval = response.read()
            conn.close()
            if rval != "":
                if str(rval[25]) == "0":
                    return True
                else:
                    print "Command did not go to Yamaha Receiver, error code " + str(rval[25])
            else:
                print "Command did not go to Yamaha Receiver, error NOT possible to set on this model."
    except socket.error:
        if print_error:
            #eg.PrintError("Unable to communicate with Yamaha Receiver. Will try again for 10 times.")
            kwargs['retry_count'] = retry_count + 1
            if retry_count < 10:
                kwargs['close_xml'] = False #could have potential for further errors if not done.
                return do_xml(self, xml, **kwargs)
            else:
                eg.PrintError("Need to check communication with Yamaha Receiver.")
                return None
        else:
            raise

def send_xml(self, xml, **kwargs):
    """
    Communicate with the receiver, but do not wait or return the results
    """
    if not 'return_result' in kwargs:
        kwargs['return_result'] = False
    do_xml(self, xml, **kwargs)

def put_xml(self, xml, **kwargs):
    send_xml(self, '<YAMAHA_AV cmd="PUT">{0}</YAMAHA_AV>'.format(xml), **kwargs)

def zone_put_xml(self, zone, xml, **kwargs):
    if zone == -1:
        zone = self.active_zone
    if zone < 2:
        put_xml(self, '<Main_Zone>{0}</Main_Zone>'.format(xml), **kwargs)
    elif zone < -1:
        put_xml(self, '<Zone_{1}>{0}</Zone_{1}>'.format(xml, chr(-1 * zone)), **kwargs)
    else:
        put_xml(self, '<Zone_{1}>{0}</Zone_{1}>'.format(xml, zone), **kwargs)

def receive_xml(self, xml, **kwargs):
    kwargs['return_result'] = True
    return do_xml(self, xml, **kwargs)

def get_xml(self, xml, **kwargs):
    return receive_xml(self, '<YAMAHA_AV cmd="GET">{0}</YAMAHA_AV>'.format(xml), **kwargs)

def zone_get_xml(self, zone, xml, **kwargs):
    if zone == -1:
        zone = self.active_zone
    if zone < 2:
        return get_xml(self, '<Main_Zone>{0}</Main_Zone>'.format(xml), **kwargs)
    elif zone < -1:
        return get_xml(self, '<Zone_{1}>{0}</Zone_{1}>'.format(xml, chr(-1 * zone)), **kwargs)
    else:
        return get_xml(self, '<Zone_{1}>{0}</Zone_{1}>'.format(xml, zone), **kwargs)

def get_sound_video(self, zone=-1, **kwargs):
    return zone_get_xml(self, zone, '<Sound_Video>GetParam</Sound_Video>', **kwargs)
        
def get_basic_status(self, zone=-1, **kwargs):
    return zone_get_xml(self, zone, '<Basic_Status>GetParam</Basic_Status>', **kwargs)

def get_tuner_status(self, **kwargs):
    return get_xml(self, '<Tuner><Play_Info>GetParam</Play_Info></Tuner>', **kwargs)

def get_device_status(self, input, section, **kwargs):
    return get_xml(self, '<{0}><{1}>GetParam</{1}></{0}>'.format(input, section), **kwargs)

def get_tuner_presets(self, **kwargs):
    return get_xml(self, '<Tuner><Play_Control><Preset><Data>GetParam</Data></Preset></Play_Control></Tuner>', **kwargs)

def get_config(self, **kwargs):
    return get_xml(self, '<System><Config>GetParam</Config></System>', **kwargs)

def get_sound_video_string(self, param, zone=-1, elem=None, **kwargs):
    if elem == "Treble":
        xml = zone_get_xml(self, zone, '<Sound_Video><Tone><Treble>GetParam</Treble></Tone></Sound_Video>', **kwargs)
    elif elem == "Bass":
        xml = zone_get_xml(self, zone, '<Sound_Video><Tone><Bass>GetParam</Bass></Tone></Sound_Video>', **kwargs)
    else:
        xml = get_sound_video(self, zone, **kwargs)
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value
    
def get_volume_string(self, param, zone=-1, elem=None, **kwargs):
    xml = zone_get_xml(self, zone, '<Volume><{0}>GetParam</{0}></Volume>'.format(elem), **kwargs)
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value
    
def get_status_string(self, param, zone=-1, **kwargs):
    xml = get_basic_status(self, zone, **kwargs)
    if kwargs.get('print_xml', False):
        print xml
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value

def get_status_strings(self, params, zone=-1, **kwargs):
    """
    Return multiple values as to to not query the receiver over the network more than once
    """
    xml = get_basic_status(self, zone, **kwargs)
    if kwargs.get('print_xml', False):
        print xml
    xmldoc = minidom.parseString(xml)
    values = []
    for param in params:
        values.append(xmldoc.getElementsByTagName(param)[0].firstChild.data)
    return tuple(values)

def get_status_param_is_on(self, param, zone=-1, **kwargs):
    return get_status_string(self, param, zone, **kwargs) == "On"

def get_status_int(self, param, zone=-1, **kwargs):
    return int(get_status_string(self, param, zone, **kwargs))

def get_config_string(self, param, **kwargs):
    #print "in get config string"
    #print self.FOUND_IP
    #print "value in self.active_zone " + str(self.active_zone)
    xml = get_config(self, **kwargs)
    if kwargs.get('print_xml', False):
        print xml
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value
"""
def get_config_param_is_on(param, **kwargs):
    return get_config_string(param, **kwargs) == "On"

def get_config_int(param, **kwargs):
    return int(get_config_string(param, **kwargs))
"""
def get_tuner_string(self, param, **kwargs):
    xml = get_tuner_status(self, **kwargs)
    if kwargs.get('print_xml', False):
        print xml
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value
"""
def get_tuner_param_is_on(param, **kwargs):
    return get_tuner_string(param, **kwargs) == "On"

def get_tuner_int(param, **kwargs):
    return int(get_tuner_string(param, **kwargs))
"""    
def get_device_string(self, param, input, section, **kwargs):
    xml = get_device_status(self, input, section, **kwargs)
    if kwargs.get('print_xml', False):
        print xml
    xmldoc = minidom.parseString(xml)
    if param[:4] == "Line":
        value = xmldoc.getElementsByTagName('Txt')[int(param[5])-1].firstChild.data
    else:
        value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value

def get_device_strings(self, params, input, section, **kwargs):
    """
    Return multiple values as to to not query the receiver over the network more than once
    """
    xml = get_device_status(self, input, section, **kwargs)
    if kwargs.get('print_xml', False):
        print xml
    xmldoc = minidom.parseString(xml)
    values = []
    for param in params:
        if param.startswith("Line"):
            values.append(xmldoc.getElementsByTagName('Txt')[int(param[5])-1].firstChild.data)
        else:
            values.append(xmldoc.getElementsByTagName(param)[0].firstChild.data)
    return tuple(values)

def get_system_pattern_1(self, param=None, **kwargs):
    types = ['Front', 'Center', 'Sur', 'Sur_Back', 'Subwoofer']
    speakers = []
    levels = []
    for type in types:
        xml = get_xml(self, '<System><Speaker_Preout><Pattern_1><Config><{0}>GetParam</{0}></Config></Pattern_1></Speaker_Preout></System>'.format(type), **kwargs)
        if not xml:
            continue
        xmldoc = minidom.parseString(xml)
        value = xmldoc.getElementsByTagName("Type")[0].firstChild.data
        if value != "None":
            if value == "Use":
                speakers.append("Subwoofer_1")
                try:
                    if xmldoc.getElementsByTagName("Type")[1].firstChild.data == "Use":
                        speakers.append("Subwoofer_2")
                except:
                    pass
            elif value[-2:] == "x2":
                speakers.append("Sur_Back_R")
                speakers.append("Sur_Back_L")
            if type == "Sur":
                speakers.append("Sur_R")
                speakers.append("Sur_L")
            if type == "Front":
                speakers.append("Front_R")
                speakers.append("Front_L")
            if type == "Center":
                speakers.append("Center")
    if param == "Active Speakers":
        return speakers
    #This is then also done only if levels are requested
    else:
        for speaker in speakers:
            xml = get_xml(self, '<System><Speaker_Preout><Pattern_1><Lvl>GetParam</Lvl></Pattern_1></Speaker_Preout></System>', **kwargs)
            xmldoc = minidom.parseString(xml)
            levels.append([speaker, float(xmldoc.getElementsByTagName(speaker)[0].firstChild.firstChild.data) /10])
        return levels

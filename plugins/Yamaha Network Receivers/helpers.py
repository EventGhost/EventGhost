# Python Imports
import traceback
from threading import Thread
from datetime import datetime
import socket
from collections import *

# Local Imports
import globals
import yamaha

def setup_ip(self):
    """
    If auto detect ip is enabled, this function will attempt to configure the ip
    address, otherwise if static ip is enabled, this function will
    verify whether a yamaha receiver can be found at the given static ip.
    """
    if self.ip_auto_detect:
        print "Searching for Yamaha Recievers ({0})...".format(self.auto_detect_model)
        ip = auto_detect_ip_threaded(self)
        if ip is not None:
            self.ip_address = ip
            return ip
    else:
        try:
            model = yamaha.get_config_string(self, 'Model_Name', timeout=self.auto_detect_timeout, ip=self.ip_address, print_error=False)
            print "Found Yamaha Receiver: {0} [{1}]".format(self.ip_address, model)
            return self.ip_address
        except:
            eg.PrintError("Yamaha Receiver Not Found [{0}]!".format(self.ip_address))
    return None

def get_lan_ip():
    """
    Attempts to open a socket connection to Google's DNS
    servers in order to determine the local IP address
    of this computer. Eg, 192.168.1.100
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.100"

def get_network_prefix():
    """
    Returns the network prefix, which is the local IP address
    without the last segment, Eg: 192.168.1.100 -> 192.168.1
    """
    lan_ip = get_lan_ip()
    return lan_ip[:lan_ip.rfind('.')]

def auto_detect_ip_threaded(self):
    """
    Blasts the network with requests, attempting to find any and all yamaha receivers
    on the local network. First it detects the user's local ip address, eg 192.168.1.100.
    Then, it converts that to the network prefix, eg 192.168.1, and then sends a request
    to every ip on that subnet, eg 192.168.1.1 -> 192.168.1.254. It does each request on
    a separate thread in order to avoid waiting for the timeout for every 254 requests
    one by one.
    """
    self.FOUND_IP = None
    threads = []

    # Get network prefix (eg 192.168.1)
    net_prefix = get_network_prefix()
    ip_range = create_ip_range(net_prefix + '.1', net_prefix + '.254')

    for ip in ip_range:
        t = Thread(target=try_connect, kwargs={'self':self, 'ip':ip})
        t.daemon = True
        threads.append(t)
        t.start()
    for t in threads:
        if self.FOUND_IP is not None:
            break
        else:
            t.join()
    if self.FOUND_IP is not None:
        print "Found Yamaha Receiver IP: {0} [{1}]".format(self.FOUND_IP, self.MODEL)
    else:
        eg.PrintError("Yamaha Receiver Was Not Found!")
    return self.FOUND_IP

def try_connect(self, ip):
    """
    Used with the auto-detect-ip functions, determines if a yamaha receiver is
    waiting at the other end of the given ip address.
    """
    #print "value in self.active_zone " + str(self.active_zone)
    #print "try connect " + ip
    try:
        model = yamaha.get_config_string(self,'Model_Name', timeout=self.auto_detect_timeout, ip=ip, print_error=False)
        print '{0}: {1}'.format(ip, model)
        if self.auto_detect_model in ["ANY", "", None] or model.upper() == self.auto_detect_model.upper():
            self.FOUND_IP = ip
            self.MODEL = model
    except:
        pass

def create_ip_range(range_start, range_end):
    """
    Given a start ip, eg 192.168.1.1, and an end ip, eg 192.168.1.254,
    generate a list of all of the ips within that range, including
    the start and end ips.
    """
    ip_range = []
    start = int(range_start[range_start.rfind('.')+1:])
    end = int(range_end[range_end.rfind('.')+1:])
    for i in range(start, end+1):
        ip = range_start[:range_start.rfind('.')+1] + str(i)
        ip_range.append(ip)
    return ip_range

def convert_zone_to_int(self, zone, convert_active=False):
    """
    Convert a zone name into the integer value that it represents:
    Examples:
    Active Zone: -1
    Main Zone: 0
    Zone 2: 2
    Zone A: -65 (this is the negative version of the integer that represents this letter: 'A' -> 65, thus -65)
    """
    if zone == 'Main Zone' or zone == 'Main_Zone' or zone == 'MZ':
        return 0
    elif 'active' in zone.lower():
        # -1 means active zone
        if convert_active:
            return self.active_zone
        else:
            return -1
    else:
        z = zone.replace('Zone_', '').replace('Zone', '').replace('Z', '').strip()
        if z in [ 'A', 'B', 'C', 'D' ]:
            return -1 * ord(z)
        return int(z)

def open_to_close_tag(tag):
    """
    Given an opening xml tag, return the matching close tag
    eg. '<YAMAHA_AV cmd="PUT"> becomes </YAMAHA_AV>
    """
    index = tag.find(' ')
    if index == -1:
        index = len(tag) - 1
    return '</' + tag[1:index] + '>'

def close_xml_tags(xml):
    """
    Automagically takes an input xml string and returns that string
    with all of the xml tags properly closed. It can even handle when
    the open tag is in the middle of the string and not the end.
    """
    output = []
    stack = []
    xml_chars = deque(list(xml))
    c = None

    while len(xml_chars) > 0:
        while len(xml_chars) > 0 and c != '<':
            c = xml_chars.popleft()
            if c != '<':
                output.append(c)
        if c == '<':
            temp = [ '<' ]
            c = xml_chars.popleft()
            end_tag = c == '/'
            while c != '>':
                temp.append(c)
                c = xml_chars.popleft()
            temp.append('>')
            tag = ''.join(temp)
            if end_tag:
                other_tag = stack.pop()
                other_close_tag = open_to_close_tag(other_tag)
                while other_close_tag != tag:
                    output.append(other_close_tag)
                    other_tag = stack.pop()
                    other_close_tag = open_to_close_tag(other_tag)
            elif not tag.endswith('/>'):
                # Only add to stack if not self-closing
                stack.append(tag)
            output.append(tag)

    while len(stack) > 0:
        tag = stack.pop()
        output.append(open_to_close_tag(tag))

    return ''.join(output)

def setup_availability(self, **kwargs):
    """
    Query the receiver to see which zones and inputs it supports.
    Should be called after a successful ip check.
    """
    xmldoc = yamaha.get_system_config(self, **kwargs)
        
    zones = []
    inputs = []
    
    for node in xmldoc.getElementsByTagName("Feature_Existence"): #just in case there are multiple "Feature" sections
        x = 0
        stop = False
        while stop==False:
            try:
                if node.childNodes[x].firstChild.data != "0":
                    if node.childNodes[x].tagName != "Main_Zone" and node.childNodes[x].tagName[:4] != "Zone":
                        inputs.append(str(node.childNodes[x].tagName))
                    else:
                        zones.append(str(node.childNodes[x].tagName))
            except:
                stop=True
            x = x + 1

    self.AVAILABLE_FEATURE_SOURCES = list(inputs)
    self.AVAILABLE_INFO_SOURCES = list(inputs)
       
    #models from RX-V use this
    x = 0
    for node in xmldoc.getElementsByTagName("Input"):
        stop = False
        while stop==False:
            try:
                self.AVAILABLE_SOURCES_RENAME.append([str(node.childNodes[x].tagName), str(node.childNodes[x].firstChild.data)])
                self.AVAILABLE_INPUT_SOURCES.append(str(node.childNodes[x].firstChild.data))
                inputs.append(str(node.childNodes[x].firstChild.data))
            except:
                stop=True
            x = x + 1

    #models from N-Line use this
    if x == 0: #this means the other lookup resulted in nothing
        MainInputxmldoc = yamaha.get_main_zone_inputs(self)
        x = 0
        for node in MainInputxmldoc.getElementsByTagName("Input_Sel_Item"):
            stop = False
            while stop==False:
                try:
                    self.AVAILABLE_SOURCES_RENAME.append([str(node.childNodes[x].tagName), str(node.childNodes[x].firstChild.data)])
                    self.AVAILABLE_INPUT_SOURCES.append(str(node.childNodes[x].firstChild.firstChild.data))
                    inputs.append(str(node.childNodes[x].firstChild.firstChild.data))
                except:
                    stop=True
                x = x + 1
            
    self.AVAILABLE_ZONES = [ zone.replace('_', ' ') for zone in zones ]
    self.AVAILABLE_SOURCES = [ input.replace('_', ' ') for input in inputs ]
    #self.AVAILABLE_SOURCES = list(set(self.AVAILABLE_SOURCES))
    tempList =[]
    for source in self.AVAILABLE_SOURCES_RENAME:
        tempList.append([source[0].replace('_',''),source[1].replace('_','')])
    self.AVAILABLE_SOURCES_RENAME = list(tempList)

def get_available_zones(self, include_active, fallback_zones, limit=None):
    """
    Returns the zones that are marked as available based on availability, and
    optionally includes an active zone. If zone availability info is not present,
    this will return fallback_zones. Optionally a limit can be imposed to only show
    a certain amount of zones if the code does not support the extra zones yet.
    """
    if len(self.AVAILABLE_ZONES) > 0:
        if limit is not None and limit < len(self.AVAILABLE_ZONES):
            # For example, limit to only 2 zones
            zones = [ self.AVAILABLE_ZONES[i] for i in range(limit) ]
        else:
            # Must use list() to create a copy
            zones = list(self.AVAILABLE_ZONES)
        if include_active:
            return ['Active Zone'] + zones
        else:
            return zones
    else:
        return fallback_zones

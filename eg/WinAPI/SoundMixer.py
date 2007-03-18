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

#from tools import *
import wx
#from ctypes_tools import *
from ctypes import *
from ctypes.wintypes import *
UINT = c_uint

WCHAR = wchar_t = c_ushort

def WSTRING(size):
    class WS(Array):
        _type_ = wchar_t
        _length_ = size
 
        def __str__(self):
            s = ""
            for c in self:
                if c == 0:
                    break
                s += chr(c)
            return s#return "".join(self)#.split("\0")[0]

        def __repr__(self):
            return repr(str(self))
 
    return WS

_Winmm = windll.Winmm


MMRESULT = UINT
MIXERR_BASE           = 1024
MMSYSERR_NOERROR      = 0
#****************************************************************************
#
#			    Mixer Support
#
#****************************************************************************

HMIXEROBJ = HANDLE
LPHMIXEROBJ = POINTER(HMIXEROBJ)
HMIXER = HANDLE
LPHMIXER = POINTER(HMIXER)

MIXER_SHORT_NAME_CHARS  = 16
MIXER_LONG_NAME_CHARS   = 64

#
#  MMRESULT error return values specific to the mixer API 
#
#
MIXERR_INVALLINE           = (MIXERR_BASE + 0)
MIXERR_INVALCONTROL        = (MIXERR_BASE + 1)
MIXERR_INVALVALUE          = (MIXERR_BASE + 2)
MIXERR_LASTERROR           = (MIXERR_BASE + 2)

MIXER_OBJECTF_HANDLE   = 0x80000000L
MIXER_OBJECTF_MIXER    = 0x00000000L
MIXER_OBJECTF_HMIXER   = (MIXER_OBJECTF_HANDLE|MIXER_OBJECTF_MIXER)
MIXER_OBJECTF_WAVEOUT  = 0x10000000L
MIXER_OBJECTF_HWAVEOUT = (MIXER_OBJECTF_HANDLE|MIXER_OBJECTF_WAVEOUT)
MIXER_OBJECTF_WAVEIN   = 0x20000000L
MIXER_OBJECTF_HWAVEIN  = (MIXER_OBJECTF_HANDLE|MIXER_OBJECTF_WAVEIN)
MIXER_OBJECTF_MIDIOUT  = 0x30000000L
MIXER_OBJECTF_HMIDIOUT = (MIXER_OBJECTF_HANDLE|MIXER_OBJECTF_MIDIOUT)
MIXER_OBJECTF_MIDIIN   = 0x40000000L
MIXER_OBJECTF_HMIDIIN  = (MIXER_OBJECTF_HANDLE|MIXER_OBJECTF_MIDIIN)
MIXER_OBJECTF_AUX      = 0x50000000L

mixerGetNumDevs = _Winmm.mixerGetNumDevs
mixerGetNumDevs.argTypes = []
mixerGetNumDevs.restype  = UINT

class MIXERCAPS(Structure):
    _fields_ = [
        ("wMid", WORD),             # manufacturer id
        ("wPid", WORD),             # product id
        ("vDriverVersion", UINT),   # version of the driver
        ("szPname", WSTRING(32)),   # product name
        ("fdwSupport", DWORD),      # misc. support bits
        ("cDestinations", DWORD)    # count of destinations
        ]
    
LPMIXERCAPS = POINTER(MIXERCAPS)

mixerGetDevCaps = _Winmm.mixerGetDevCapsW
mixerGetDevCaps.argTypes = [UINT, LPMIXERCAPS, UINT]
mixerGetDevCaps.restype  = MMRESULT

mixerOpen = _Winmm.mixerOpen
mixerOpen.argTypes = [LPHMIXER, UINT, DWORD, DWORD, DWORD]
mixerOpen.restype  = MMRESULT

mixerClose = _Winmm.mixerClose
mixerClose.argTypes = [HMIXER]
mixerClose.restype  = MMRESULT

mixerMessage = _Winmm.mixerMessage
mixerMessage.argTypes = [HMIXER, UINT, DWORD, DWORD]
mixerMessage.restype  = DWORD

class MIXERLINE(Structure):
    class _TARGET(Structure):
        _fields_ = [
            ("dwType", DWORD),          # MIXERLINE_TARGETTYPE_xxxx
            ("dwDeviceID", DWORD),      # target device ID of device type
            ("wMid", WORD),             # of target device
            ("wPid", WORD),             #      "
            ("vDriverVersion", UINT),   #      "
            ("szPname", WSTRING(32)),   #      "
        ]
    
    _fields_ = [
        ("cbStruct", DWORD),        # size of MIXERLINE structure
        ("dwDestination", DWORD),   # zero based destination index
        ("dwSource", DWORD),        # zero based source index (if source)
        ("dwLineID", DWORD),        # unique line id for mixer device
        ("fdwLine", DWORD),         # state/information about line
        ("dwUser", DWORD),          # driver specific information
        ("dwComponentType", DWORD), # component type line connects to
        ("cChannels", DWORD),       # number of channels line supports
        ("cConnections", DWORD),    # number of connections [possible]
        ("cControls", DWORD),       # number of controls at this line
        ("szShortName", WSTRING(MIXER_SHORT_NAME_CHARS)),
        ("szPname", WSTRING(MIXER_LONG_NAME_CHARS)),
        ("Target", _TARGET),
        ]
    
LPMIXERLINE = POINTER(MIXERLINE)
#
#  MIXERLINE.fdwLine
#
#
MIXERLINE_LINEF_ACTIVE             = 0x00000001
MIXERLINE_LINEF_DISCONNECTED       = 0x00008000
MIXERLINE_LINEF_SOURCE             = 0x80000000

#
#  MIXERLINE.dwComponentType 
#
#  component types for destinations and sources 
#
#
MIXERLINE_COMPONENTTYPE_DST_FIRST      = 0x00000000
MIXERLINE_COMPONENTTYPE_DST_UNDEFINED  = (MIXERLINE_COMPONENTTYPE_DST_FIRST + 0)
MIXERLINE_COMPONENTTYPE_DST_DIGITAL    = (MIXERLINE_COMPONENTTYPE_DST_FIRST + 1)
MIXERLINE_COMPONENTTYPE_DST_LINE       = (MIXERLINE_COMPONENTTYPE_DST_FIRST + 2)
MIXERLINE_COMPONENTTYPE_DST_MONITOR    = (MIXERLINE_COMPONENTTYPE_DST_FIRST + 3)
MIXERLINE_COMPONENTTYPE_DST_SPEAKERS   = (MIXERLINE_COMPONENTTYPE_DST_FIRST + 4)
MIXERLINE_COMPONENTTYPE_DST_HEADPHONES = (MIXERLINE_COMPONENTTYPE_DST_FIRST + 5)
MIXERLINE_COMPONENTTYPE_DST_TELEPHONE  = (MIXERLINE_COMPONENTTYPE_DST_FIRST + 6)
MIXERLINE_COMPONENTTYPE_DST_WAVEIN     = (MIXERLINE_COMPONENTTYPE_DST_FIRST + 7)
MIXERLINE_COMPONENTTYPE_DST_VOICEIN    = (MIXERLINE_COMPONENTTYPE_DST_FIRST + 8)
MIXERLINE_COMPONENTTYPE_DST_LAST       = (MIXERLINE_COMPONENTTYPE_DST_FIRST + 8)

MIXERLINE_COMPONENTTYPE_SRC_FIRST      = 0x00001000
MIXERLINE_COMPONENTTYPE_SRC_UNDEFINED  = (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 0)
MIXERLINE_COMPONENTTYPE_SRC_DIGITAL    = (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 1)
MIXERLINE_COMPONENTTYPE_SRC_LINE       = (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 2)
MIXERLINE_COMPONENTTYPE_SRC_MICROPHONE = (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 3)
MIXERLINE_COMPONENTTYPE_SRC_SYNTHESIZER= (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 4)
MIXERLINE_COMPONENTTYPE_SRC_COMPACTDISC= (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 5)
MIXERLINE_COMPONENTTYPE_SRC_TELEPHONE  = (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 6)
MIXERLINE_COMPONENTTYPE_SRC_PCSPEAKER  = (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 7)
MIXERLINE_COMPONENTTYPE_SRC_WAVEOUT    = (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 8)
MIXERLINE_COMPONENTTYPE_SRC_AUXILIARY  = (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 9)
MIXERLINE_COMPONENTTYPE_SRC_ANALOG     = (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 10)
MIXERLINE_COMPONENTTYPE_SRC_LAST       = (MIXERLINE_COMPONENTTYPE_SRC_FIRST + 10)

#
#  MIXERLINE.Target.dwType 
#
#
MIXERLINE_TARGETTYPE_UNDEFINED     = 0
MIXERLINE_TARGETTYPE_WAVEOUT       = 1
MIXERLINE_TARGETTYPE_WAVEIN        = 2
MIXERLINE_TARGETTYPE_MIDIOUT       = 3
MIXERLINE_TARGETTYPE_MIDIIN        = 4
MIXERLINE_TARGETTYPE_AUX           = 5

mixerGetLineInfo = _Winmm.mixerGetLineInfoW
mixerGetLineInfo.argTypes = [HMIXEROBJ, LPMIXERLINE, DWORD]
mixerGetLineInfo.restype  = MMRESULT

MIXER_GETLINEINFOF_DESTINATION     = 0x00000000
MIXER_GETLINEINFOF_SOURCE          = 0x00000001
MIXER_GETLINEINFOF_LINEID          = 0x00000002
MIXER_GETLINEINFOF_COMPONENTTYPE   = 0x00000003
MIXER_GETLINEINFOF_TARGETTYPE      = 0x00000004

MIXER_GETLINEINFOF_QUERYMASK       = 0x0000000F

mixerGetID = _Winmm.mixerGetID
mixerGetID.argTypes = [HMIXEROBJ, POINTER(UINT), DWORD]
mixerGetID.restype  = MMRESULT

#
#  MIXERCONTROL 
#
#
class MIXERCONTROL(Structure):
    class _BOUNDS(Union):
        class _BOUNDS_LONG(Structure):
            _fields_ = [
                ("lMinimum", LONG),         # signed minimum for this control
                ("lMaximum", LONG),         # signed maximum for this control
            ]

        class _BOUNDS_DWORD(Structure):
            _fields_ = [
                ("dwMinimum", DWORD),       # unsigned minimum for this control
                ("dwMaximum", DWORD),       # unsigned maximum for this control
            ]
            
        _fields_ = [
            ("lBounds", _BOUNDS_LONG), 
            ("dwBounds", _BOUNDS_DWORD),
            ("dwReserved", DWORD * 6),  
        ]
        
    class _METRICS(Union):
        _fields_ = [
            ("cSteps", DWORD),          # of steps between min & max
            ("cbCustomData", DWORD),    # size in bytes of custom data
            ("dwReserved", DWORD * 6),  # !!! needed? we have cbStruct....
        ]
        
    _fields_ = [
        ("cbStruct", DWORD),        # size in bytes of MIXERCONTROL
        ("dwControlID", DWORD),     # unique control id for mixer device
        ("dwControlType", DWORD),   # MIXERCONTROL_CONTROLTYPE_xxx
        ("fdwControl", DWORD),      # MIXERCONTROL_CONTROLF_xxx
        ("cMultipleItems", DWORD),  # if MIXERCONTROL_CONTROLF_MULTIPLE set
        ("szShortName", WSTRING(MIXER_SHORT_NAME_CHARS)),
        ("szPname", WSTRING(MIXER_LONG_NAME_CHARS)),
        ("Bounds", _BOUNDS),
        ("Metrics", _METRICS),
    ]
        
#
#  MIXERCONTROL.fdwControl
#
#
MIXERCONTROL_CONTROLF_UNIFORM  = 0x00000001
MIXERCONTROL_CONTROLF_MULTIPLE = 0x00000002
MIXERCONTROL_CONTROLF_DISABLED = 0x80000000

#
#  MIXERCONTROL_CONTROLTYPE_xxx building block defines
#
#
MIXERCONTROL_CT_CLASS_MASK         = 0xF0000000
MIXERCONTROL_CT_CLASS_CUSTOM       = 0x00000000
MIXERCONTROL_CT_CLASS_METER        = 0x10000000
MIXERCONTROL_CT_CLASS_SWITCH       = 0x20000000
MIXERCONTROL_CT_CLASS_NUMBER       = 0x30000000
MIXERCONTROL_CT_CLASS_SLIDER       = 0x40000000
MIXERCONTROL_CT_CLASS_FADER        = 0x50000000
MIXERCONTROL_CT_CLASS_TIME         = 0x60000000
MIXERCONTROL_CT_CLASS_LIST         = 0x70000000

MIXERCONTROL_CT_SUBCLASS_MASK      = 0x0F000000

MIXERCONTROL_CT_SC_SWITCH_BOOLEAN  = 0x00000000
MIXERCONTROL_CT_SC_SWITCH_BUTTON   = 0x01000000

MIXERCONTROL_CT_SC_METER_POLLED    = 0x00000000

MIXERCONTROL_CT_SC_TIME_MICROSECS  = 0x00000000
MIXERCONTROL_CT_SC_TIME_MILLISECS  = 0x01000000

MIXERCONTROL_CT_SC_LIST_SINGLE     = 0x00000000
MIXERCONTROL_CT_SC_LIST_MULTIPLE   = 0x01000000

MIXERCONTROL_CT_UNITS_MASK         = 0x00FF0000
MIXERCONTROL_CT_UNITS_CUSTOM       = 0x00000000
MIXERCONTROL_CT_UNITS_BOOLEAN      = 0x00010000
MIXERCONTROL_CT_UNITS_SIGNED       = 0x00020000
MIXERCONTROL_CT_UNITS_UNSIGNED     = 0x00030000
MIXERCONTROL_CT_UNITS_DECIBELS     = 0x00040000 # in 10ths 
MIXERCONTROL_CT_UNITS_PERCENT      = 0x00050000 # in 10ths

#
#  Commonly used control types for specifying MIXERCONTROL.dwControlType 
#

MIXERCONTROL_CONTROLTYPE_CUSTOM        = (MIXERCONTROL_CT_CLASS_CUSTOM | MIXERCONTROL_CT_UNITS_CUSTOM)
MIXERCONTROL_CONTROLTYPE_BOOLEANMETER  = (MIXERCONTROL_CT_CLASS_METER | MIXERCONTROL_CT_SC_METER_POLLED | MIXERCONTROL_CT_UNITS_BOOLEAN)
MIXERCONTROL_CONTROLTYPE_SIGNEDMETER   = (MIXERCONTROL_CT_CLASS_METER | MIXERCONTROL_CT_SC_METER_POLLED | MIXERCONTROL_CT_UNITS_SIGNED)
MIXERCONTROL_CONTROLTYPE_PEAKMETER     = (MIXERCONTROL_CONTROLTYPE_SIGNEDMETER + 1)
MIXERCONTROL_CONTROLTYPE_UNSIGNEDMETER = (MIXERCONTROL_CT_CLASS_METER | MIXERCONTROL_CT_SC_METER_POLLED | MIXERCONTROL_CT_UNITS_UNSIGNED)
MIXERCONTROL_CONTROLTYPE_BOOLEAN       = (MIXERCONTROL_CT_CLASS_SWITCH | MIXERCONTROL_CT_SC_SWITCH_BOOLEAN | MIXERCONTROL_CT_UNITS_BOOLEAN)
MIXERCONTROL_CONTROLTYPE_ONOFF         = (MIXERCONTROL_CONTROLTYPE_BOOLEAN + 1)
MIXERCONTROL_CONTROLTYPE_MUTE          = (MIXERCONTROL_CONTROLTYPE_BOOLEAN + 2)
MIXERCONTROL_CONTROLTYPE_MONO          = (MIXERCONTROL_CONTROLTYPE_BOOLEAN + 3)
MIXERCONTROL_CONTROLTYPE_LOUDNESS      = (MIXERCONTROL_CONTROLTYPE_BOOLEAN + 4)
MIXERCONTROL_CONTROLTYPE_STEREOENH     = (MIXERCONTROL_CONTROLTYPE_BOOLEAN + 5)
MIXERCONTROL_CONTROLTYPE_BUTTON        = (MIXERCONTROL_CT_CLASS_SWITCH | MIXERCONTROL_CT_SC_SWITCH_BUTTON | MIXERCONTROL_CT_UNITS_BOOLEAN)
MIXERCONTROL_CONTROLTYPE_DECIBELS      = (MIXERCONTROL_CT_CLASS_NUMBER | MIXERCONTROL_CT_UNITS_DECIBELS)
MIXERCONTROL_CONTROLTYPE_SIGNED        = (MIXERCONTROL_CT_CLASS_NUMBER | MIXERCONTROL_CT_UNITS_SIGNED)
MIXERCONTROL_CONTROLTYPE_UNSIGNED      = (MIXERCONTROL_CT_CLASS_NUMBER | MIXERCONTROL_CT_UNITS_UNSIGNED)
MIXERCONTROL_CONTROLTYPE_PERCENT       = (MIXERCONTROL_CT_CLASS_NUMBER | MIXERCONTROL_CT_UNITS_PERCENT)
MIXERCONTROL_CONTROLTYPE_SLIDER        = (MIXERCONTROL_CT_CLASS_SLIDER | MIXERCONTROL_CT_UNITS_SIGNED)
MIXERCONTROL_CONTROLTYPE_PAN           = (MIXERCONTROL_CONTROLTYPE_SLIDER + 1)
MIXERCONTROL_CONTROLTYPE_QSOUNDPAN     = (MIXERCONTROL_CONTROLTYPE_SLIDER + 2)
MIXERCONTROL_CONTROLTYPE_FADER         = (MIXERCONTROL_CT_CLASS_FADER | MIXERCONTROL_CT_UNITS_UNSIGNED)
MIXERCONTROL_CONTROLTYPE_VOLUME        = (MIXERCONTROL_CONTROLTYPE_FADER + 1)
MIXERCONTROL_CONTROLTYPE_BASS          = (MIXERCONTROL_CONTROLTYPE_FADER + 2)
MIXERCONTROL_CONTROLTYPE_TREBLE        = (MIXERCONTROL_CONTROLTYPE_FADER + 3)
MIXERCONTROL_CONTROLTYPE_EQUALIZER     = (MIXERCONTROL_CONTROLTYPE_FADER + 4)
MIXERCONTROL_CONTROLTYPE_SINGLESELECT  = (MIXERCONTROL_CT_CLASS_LIST | MIXERCONTROL_CT_SC_LIST_SINGLE | MIXERCONTROL_CT_UNITS_BOOLEAN)
MIXERCONTROL_CONTROLTYPE_MUX           = (MIXERCONTROL_CONTROLTYPE_SINGLESELECT + 1)
MIXERCONTROL_CONTROLTYPE_MULTIPLESELECT= (MIXERCONTROL_CT_CLASS_LIST | MIXERCONTROL_CT_SC_LIST_MULTIPLE | MIXERCONTROL_CT_UNITS_BOOLEAN)
MIXERCONTROL_CONTROLTYPE_MIXER         = (MIXERCONTROL_CONTROLTYPE_MULTIPLESELECT + 1)
MIXERCONTROL_CONTROLTYPE_MICROTIME     = (MIXERCONTROL_CT_CLASS_TIME | MIXERCONTROL_CT_SC_TIME_MICROSECS | MIXERCONTROL_CT_UNITS_UNSIGNED)
MIXERCONTROL_CONTROLTYPE_MILLITIME     = (MIXERCONTROL_CT_CLASS_TIME | MIXERCONTROL_CT_SC_TIME_MILLISECS | MIXERCONTROL_CT_UNITS_UNSIGNED)

#
#  MIXERLINECONTROLS
#
class MIXERLINECONTROLS(Structure):
    class _UNION(Union):
        _fields_ = [
            ("ID", DWORD),              # MIXER_GETLINECONTROLSF_ONEBYID
            ("Type", DWORD),            # MIXER_GETLINECONTROLSF_ONEBYTYPE
        ]
    
    _fields_ = [
        ("cbStruct", DWORD),        # size in bytes of MIXERLINECONTROLS
        ("dwLineID", DWORD),        # line id (from MIXERLINE.dwLineID)
        ("dwControl", _UNION),
        ("cControls", DWORD),       # count of controls pmxctrl points to
        ("cbmxctrl", DWORD),        # size in bytes of _one_ MIXERCONTROL
        ("pamxctrl", POINTER(MIXERCONTROL)), # pointer to first MIXERCONTROL array
    ]
LPMIXERLINECONTROLS = POINTER(MIXERLINECONTROLS)

mixerGetLineControls = _Winmm.mixerGetLineControlsW
mixerGetLineControls.argTypes = [HMIXEROBJ, LPMIXERLINECONTROLS, DWORD]
mixerGetLineControls.restype  = MMRESULT

MIXER_GETLINECONTROLSF_ALL         = 0x00000000
MIXER_GETLINECONTROLSF_ONEBYID     = 0x00000001
MIXER_GETLINECONTROLSF_ONEBYTYPE   = 0x00000002

MIXER_GETCONTROLDETAILSF_QUERYMASK = 0x0000000F


class MIXERCONTROLDETAILS(Structure):
    class _UNION(Union):
        _fields_ = [
            ("hwndOwner", HWND),        # for MIXER_SETCONTROLDETAILSF_CUSTOM 
            ("cMultipleItems", DWORD),  # if _MULTIPLE, the number of items per channel
            ]
        
    _fields_ = [
        ("cbStruct", DWORD),        # size in bytes of MIXERCONTROLDETAILS
        ("dwControlID", DWORD),     # control id to get/set details on 
        ("cChannels", DWORD),       # number of channels in paDetails array
        ("Union", _UNION),
        ("cbDetails", DWORD),       # size of _one_ details_XX struct
        ("paDetails", c_void_p),    # pointer to array of details_XX structs
        ]
LPMIXERCONTROLDETAILS = POINTER(MIXERCONTROLDETAILS)

#
#  MIXER_GETCONTROLDETAILSF_LISTTEXT 
#
#
class MIXERCONTROLDETAILS_LISTTEXT(Structure):
    _fields_ = [
        ("dwParam1", DWORD),
        ("dwParam2", DWORD),
        ("szName", WSTRING(MIXER_LONG_NAME_CHARS)),
        ]

#
#  MIXER_GETCONTROLDETAILSF_VALUE 
#
class MIXERCONTROLDETAILS_BOOLEAN(Structure):
    _fields_ = [
        ("fValue", LONG),
        ]
    
class MIXERCONTROLDETAILS_SIGNED(Structure):
    _fields_ = [
        ("lValue", LONG),
        ]
    
class MIXERCONTROLDETAILS_UNSIGNED(Structure):
    _fields_ = [
        ("dwValue", DWORD),
        ]

mixerGetControlDetails = _Winmm.mixerGetControlDetailsW
mixerGetControlDetails.argTypes = [HMIXEROBJ, LPMIXERLINECONTROLS, DWORD]
mixerGetControlDetails.restype  = MMRESULT

MIXER_GETCONTROLDETAILSF_VALUE     = 0x00000000
MIXER_GETCONTROLDETAILSF_LISTTEXT  = 0x00000001

MIXER_GETCONTROLDETAILSF_QUERYMASK = 0x0000000F

mixerSetControlDetails = _Winmm.mixerSetControlDetails
mixerSetControlDetails.argTypes = [HMIXEROBJ, LPMIXERLINECONTROLS, DWORD]
mixerSetControlDetails.restype  = MMRESULT

MIXER_SETCONTROLDETAILSF_VALUE     = 0x00000000
MIXER_SETCONTROLDETAILSF_CUSTOM    = 0x00000001

MIXER_SETCONTROLDETAILSF_QUERYMASK = 0x0000000F



#-----------------------------------
#  Windows Multimedia Functions
#-----------------------------------



CONTROL_TYPES = [
    "VOLUME", "BASS", "TREBLE", "EQUALIZER", "FADER", 
    "BOOLEAN", "BUTTON", "LOUDNESS", "MONO", "MUTE", "ONOFF", "STEREOENH", 
    "SINGLESELECT", "MULTIPLESELECT", "MUX", "MIXER", 
    "BOOLEANMETER", "PEAKMETER", "SIGNEDMETER", "UNSIGNEDMETER", 
    "SIGNED", "UNSIGNED", "PERCENT", "DECIBELS", 
    "SLIDER", "PAN", "QSOUNDPAN", 
    "MICROTIME", "MILLITIME"
    ]

CONTROL_TYPES_DICT = {}
for i in CONTROL_TYPES:
    value = locals()["MIXERCONTROL_CONTROLTYPE_" + i]
    CONTROL_TYPES_DICT[value] = "MIXERCONTROL_CONTROLTYPE_" + i
    
def GetControlInfo(devId, controlId):
    mixerHandle = HMIXER()
    mixerControlArray = MIXERCONTROL()
    mixerLineControls = MIXERLINECONTROLS()
    
    err = mixerOpen(byref(mixerHandle), devId, 0, 0, MIXER_OBJECTF_MIXER)

    mixerLineControls.cbStruct = sizeof(MIXERLINECONTROLS)
    mixerLineControls.cControls = 1
    mixerLineControls.dwControl.ID = controlId
    mixerLineControls.pamxctrl = pointer(mixerControlArray)
    mixerLineControls.cbmxctrl = sizeof(MIXERCONTROL)
    err = mixerGetLineControls(mixerHandle, byref(mixerLineControls), MIXER_GETLINECONTROLSF_ONEBYID)
    mixerClose(mixerHandle)
    str = ""
    str += "dwControlType: %d\n" % mixerControlArray.dwControlType
    str += "fdwControl: %d\n" % mixerControlArray.fdwControl
    str += "cMultipleItems: %d\n" % mixerControlArray.cMultipleItems
    if MIXERCONTROL_CONTROLF_UNIFORM == mixerControlArray.fdwControl:
        str += "MIXERCONTROL_CONTROLF_UNIFORM\n"
    str += CONTROL_TYPES_DICT[mixerControlArray.dwControlType] + "\n"

    return str

def GetControlValue(devId, controlId):
    mixerHandle = HMIXER()
    value = MIXERCONTROLDETAILS_BOOLEAN()
    mixerControlDetails = MIXERCONTROLDETAILS()
    mixerControlDetails.cbStruct = sizeof(MIXERCONTROLDETAILS)
    mixerControlDetails.dwControlID = controlId
    mixerControlDetails.cChannels = 1
    mixerControlDetails.cMultipleItems = 0
    mixerControlDetails.paDetails = addressof(value)
    mixerControlDetails.cbDetails = sizeof(value)
    err = mixerOpen(byref(mixerHandle), devId, 0, 0, MIXER_OBJECTF_MIXER)
    err = mixerGetControlDetails(mixerHandle, byref(mixerControlDetails), MIXER_GETCONTROLDETAILSF_VALUE)
    mixerClose(mixerHandle)



class VolumeDialog(wx.Dialog):
    def __init__(self, data=None):

                    
        wx.Dialog.__init__(self, None, -1, "Volume", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
       
        style = wx.TR_HAS_BUTTONS# | wx.TR_HIDE_ROOT | wx.TR_MULTIPLE #  wx.TR_NO_LINES | | wx.TR_FULL_ROW_HIGHLIGHT# |wx.TR_HAS_BUTTONS 
        style = wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.TR_FULL_ROW_HIGHLIGHT
        self.tree = tree = wx.TreeCtrl(self, -1, size=(250,200), style=style)
        tree.SetMinSize((250,200))
        self.root = root = tree.AddRoot("Functions")
        #traverse(tree, root, gTreeData, "")
        #tree.Expand(root)
        self.Traverse()
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)

        panel = wx.Panel(self, -1, size=(250,-1))
        panel.SetMinSize((250,-1))
        self.funcText = wx.TextCtrl(panel, -1, size=(200,-1), style=wx.TE_READONLY)
        self.funcText.SetMinSize((200,-1))
        self.funcText.SetBackgroundColour(self.GetBackgroundColour())
        
        self.docText = wx.TextCtrl(panel, -1, size=(200,200), style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.docText.SetBackgroundColour(self.GetBackgroundColour())
            
        okButton = wx.Button(self, wx.ID_OK, lang.ok)
        okButton.SetDefault()
        #okButton.Bind(wx.EVT_BUTTON, self.OnOK)

        cancelButton = wx.Button(self, wx.ID_CANCEL, lang.cancel)
        #cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        
        stdbtnsizer = wx.StdDialogButtonSizer()
        stdbtnsizer.AddButton(okButton)
        stdbtnsizer.AddButton(cancelButton)
        stdbtnsizer.Realize()
        btnrowSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnrowSizer.Add((5,5), 1)
        btnrowSizer.Add(stdbtnsizer, 0, wx.TOP|wx.BOTTOM, 6)
        btnrowSizer.Add((2,2), 0)

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.funcText, 0, wx.EXPAND)
        panelSizer.Add(self.docText, 1, wx.EXPAND)
        panel.SetSizer(panelSizer)
        panel.SetAutoLayout(True)
        panelSizer.Fit(panel)
        
        middleSizer = wx.BoxSizer(wx.HORIZONTAL)
        middleSizer.Add(tree, 0, wx.EXPAND)
        middleSizer.Add(panel, 1, wx.EXPAND)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(middleSizer, 1, wx.EXPAND)
        mainSizer.Add(btnrowSizer, 0, wx.EXPAND)
        
        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)
        mainSizer.Fit(self)
        minSize = self.GetSize()
        self.SetMinSize(minSize)
        self.Show()

    def OnSelectionChanged(self, event):
        item = event.GetItem()
        tree = self.tree
        data = tree.GetPyData(item)
        if data is None:
            self.funcText.SetValue("")
            self.docText.SetValue("")
            return
        self.funcText.SetValue("(%d, %d)" % (data[0], data[1]))
        str = GetControlInfo(data[0], data[1])
        self.docText.SetValue(str)
    
    def OnOK(self, event):
        event.Skip()

    def Traverse(self):
        def appendControls(hMixer, devID, mixerline, item):
            if mixerline.cControls > 0:
                mixerControlArray = (MIXERCONTROL * mixerline.cControls)()
                mixerLineControls = MIXERLINECONTROLS()
                mixerLineControls.cbStruct = sizeof(MIXERLINECONTROLS)
                mixerLineControls.cControls = mixerline.cControls
                mixerLineControls.dwLineID = mixerline.dwLineID
                mixerLineControls.pamxctrl = pointer(mixerControlArray[0])
                mixerLineControls.cbmxctrl = sizeof(MIXERCONTROL)

                err = mixerGetLineControls(hMixer, byref(mixerLineControls), MIXER_GETLINECONTROLSF_ALL)
                for i in range(mixerline.cControls):
                    tmp = self.tree.AppendItem(item, str(mixerControlArray[i].szPname))
                    self.tree.SetPyData(tmp, (devID, mixerControlArray[i].dwControlID))

            
        hMixer = HMIXER()
        mixcaps = MIXERCAPS()
        mixcaps.cbStruct = sizeof(MIXERCAPS)
        mixerline = MIXERLINE()
        mixerline.cbStruct = sizeof(MIXERLINE)
        
        # Get the number of Mixer devices in this computer
        iNumDevs = mixerGetNumDevs()
        
        # Go through all of those devices
        for uMxId in range(iNumDevs):
            err = mixerGetDevCaps(uMxId, byref(mixcaps), sizeof(MIXERCAPS))
            if err:
                continue
            result = mixerOpen(byref(hMixer), uMxId, 0, 0, MIXER_OBJECTF_MIXER)
            devitem = self.tree.AppendItem(self.root, str(mixcaps.szPname))
            
            for j in range(mixcaps.cDestinations):
                mixerline.cbStruct = sizeof(MIXERLINE)
                mixerline.dwDestination = j
                err = mixerGetLineInfo(hMixer, byref(mixerline), MIXER_GETLINEINFOF_DESTINATION)
                destitem = self.tree.AppendItem(devitem, str(mixerline.szPname) + " " + str(mixerline.cChannels))
                item = self.tree.AppendItem(destitem, "Mastercontrols")
                appendControls(hMixer, uMxId, mixerline, item)
                for k in range(mixerline.cConnections):
                    mixerline.cbStruct = sizeof(MIXERLINE)
                    mixerline.dwDestination = j
                    mixerline.dwSource = k
                    err = mixerGetLineInfo(hMixer, byref(mixerline), MIXER_GETLINEINFOF_SOURCE)
                    item = self.tree.AppendItem(destitem, str(mixerline.szPname) + " " + str(mixerline.cChannels))
                    appendControls(hMixer, uMxId, mixerline, item)

            mixerClose(hMixer)

            
##if __name__ == "__main__":
##    print
##    print
##    print
##    result = MMRESULT()
##    hMixer = HMIXER()
##    mixcaps = MIXERCAPS()
##    mixcaps.cbStruct = sizeof(MIXERCAPS)
##    mixerline = MIXERLINE()
##    mixerline.cbStruct = sizeof(MIXERLINE)
##
##    # Get the number of Mixer devices in this computer
##    iNumDevs = mixerGetNumDevs()
##
##    controlList = {}
##
##    # Go through all of those devices, displaying their IDs/names
##    for uMxId in range(iNumDevs):
##        err = mixerGetDevCaps(uMxId, byref(mixcaps), sizeof(MIXERCAPS))
##        if not err:
##            result = mixerOpen(byref(hMixer), uMxId, 0, 0, MIXER_OBJECTF_MIXER)
##            print "Device ID #%d: %s " % (uMxId, mixcaps.szPname)
##            for j in range(mixcaps.cDestinations):
##                mixerline.cbStruct = sizeof(MIXERLINE)
##                mixerline.dwDestination = j
##                err = mixerGetLineInfo(hMixer, byref(mixerline), MIXER_GETLINEINFOF_DESTINATION)
##                print "  Destination #%d = %s" % (j, mixerline.szPname)
##
##                if mixerline.cControls > 0:
##                    mixerControlArray = (MIXERCONTROL * mixerline.cControls)()
##                    mixerLineControls = MIXERLINECONTROLS()
##                    mixerLineControls.cbStruct = sizeof(MIXERLINECONTROLS)
##                    mixerLineControls.cControls = mixerline.cControls
##                    mixerLineControls.dwLineID = mixerline.dwLineID
##                    mixerLineControls.pamxctrl = pointer(mixerControlArray[0])
##                    mixerLineControls.cbmxctrl = sizeof(MIXERCONTROL)
##
##                    err = mixerGetLineControls(hMixer, byref(mixerLineControls), MIXER_GETLINECONTROLSF_ALL)
##                    for l in range(mixerline.cControls):
##                        print "      Control #%d = %s %d" % (l, mixerControlArray[l].szPname, mixerControlArray[l].dwControlID)
##                        controlList[mixerControlArray[l].dwControlID] = 1
##                for k in range(mixerline.cConnections):
##                    mixerline.cbStruct = sizeof(MIXERLINE)
##                    mixerline.dwDestination = j
##                    mixerline.dwSource = k
##                    err = mixerGetLineInfo(hMixer, byref(mixerline), MIXER_GETLINEINFOF_SOURCE)
##                    print "    Source #%d = %s" % (k, mixerline.szPname)
##                    if mixerline.cControls > 0:
##                        mixerControlArray = (MIXERCONTROL * mixerline.cControls)()
##                        mixerLineControls = MIXERLINECONTROLS()
##
##                        mixerLineControls.cbStruct = sizeof(MIXERLINECONTROLS)
##                        mixerLineControls.cControls = mixerline.cControls
##                        mixerLineControls.dwLineID = mixerline.dwLineID
##                        mixerLineControls.pamxctrl = pointer(mixerControlArray[0])
##                        mixerLineControls.cbmxctrl = sizeof(MIXERCONTROL)
##
##                        err = mixerGetLineControls(hMixer, byref(mixerLineControls), MIXER_GETLINECONTROLSF_ALL)
##                        for l in range(mixerline.cControls):
##                            print "      Control #%d = %s %d" % (l, mixerControlArray[l].szPname, mixerControlArray[l].dwControlID)
##                            controlList[mixerControlArray[l].dwControlID] = 1
##                    
##            mixerClose(hMixer)
##
##    print        
##    GetControlInfo(0, 5)
##    GetControlInfo(0, 6)
##    for controlId in controlList.keys():
##        print
##        GetControlInfo(0, controlId)




def SetVolume(Level):
    # Sets the volume to a specific percentage as passed through
    hmixer = HMIXER()

    # Obtain the hmixer struct
    err = mixerOpen(byref(hmixer), 0, 0, 0, 0)
    if err != 0:
        return False

    # Obtain the volumne control object
    volCtrl = GetVolumeControl(hmixer, MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
                    MIXERCONTROL_CONTROLTYPE_VOLUME)
    if volCtrl is None:
        return False
    
    # Then determine the value of the new volume
    lngVolSetting = int(volCtrl.Bounds.lBounds.lMaximum * (Level / 100.0))
    if lngVolSetting > volCtrl.Bounds.lBounds.lMaximum:
        lngVolSetting = volCtrl.Bounds.lBounds.lMaximum
        
    # Then set the volume
    return SetVolumeControl(hmixer, volCtrl, lngVolSetting)


def SetMute(mute=True):
    # This routine sets the volume setting of the current unit depending on the value passed through
    hmixer = HMIXER()
    volCtrl = MIXERCONTROL()

    # Obtain the hmixer struct
    err = mixerOpen(byref(hmixer), 0, 0, 0, 0)
    if err != 0:
        return False

    # Obtain the volumne control object
    volCtrl = GetVolumeControl(hmixer, MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
                                MIXERCONTROL_CONTROLTYPE_MUTE)
    if volCtrl is None:
        return False

    # Then set the volume
    return SetVolumeControl(hmixer, volCtrl, int(mute))

def ClearMute():
    SetMute(False)

def ToggleMute():
    flag = not GetMute()
    SetMute(flag)
    return flag

def GetVolumeControl(hmixer, componentType, ctrlType):
    '''Obtains an appropriate pointer and info for the volume control
       This function attempts to obtain a mixer control. Returns True if successful.'''
    mxlc = MIXERLINECONTROLS()
    mxl = MIXERLINE()
    mxc = MIXERCONTROL()

    mxl.cbStruct = sizeof(mxl)
    mxl.dwComponentType = componentType

    # Obtain a line corresponding to the component type
    rc = mixerGetLineInfo(hmixer, byref(mxl), MIXER_GETLINEINFOF_COMPONENTTYPE)

    if (MMSYSERR_NOERROR == rc):
        mxlc.cbStruct = sizeof(mxlc)
        mxlc.dwLineID = mxl.dwLineID
        mxlc.dwControl.Type = ctrlType
        mxlc.cControls = 1
        mxlc.cbmxctrl = sizeof(mxc)

        # Allocate a buffer for the control
        mxlc.pamxctrl = pointer(mxc)
        mxc.cbStruct = sizeof(mxc)

        # Get the control
        rc = mixerGetLineControls(hmixer, byref(mxlc), MIXER_GETLINECONTROLSF_ONEBYTYPE)

        if (MMSYSERR_NOERROR == rc):
            return mxc

    return None


def GetVolumeValue(hmixer, mxc):
    mxcd = MIXERCONTROLDETAILS()
    vol = MIXERCONTROLDETAILS_UNSIGNED()

    mxcd.item = 0
    mxcd.dwControlID = mxc.dwControlID
    mxcd.cbStruct = sizeof(mxcd)
    mxcd.cbDetails = sizeof(vol)

    #' Allocate a buffer for the control value buffer
    mxcd.paDetails = addressof(vol)
    mxcd.cChannels = 1
    #vol.dwValue = volume

    #' Get the control value
    err = mixerGetControlDetails(hmixer, byref(mxcd), 0)

    if err != MMSYSERR_NOERROR:
        return None
    return vol.dwValue


def GetMute():
    hmixer = HMIXER()
    volCtrl = MIXERCONTROL()

    # Obtain the hmixer struct
    err = mixerOpen(byref(hmixer), 0, 0, 0, 0)
    if err != 0:
        return False

    # Obtain the volumne control object
    volCtrl = GetVolumeControl(hmixer, MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
                                MIXERCONTROL_CONTROLTYPE_MUTE)
    if volCtrl is None:
        return False

    # Then set the volume
    return GetVolumeValue(hmixer, volCtrl)    

    
def SetVolumeControl(hmixer, mxc, volume):
    ''' Sets the volumne from the pointer of the object passed through

    ' [Note: original source taken from MSDN http://support.microsoft.com/default.aspx?scid=KB;EN-US;Q178456&]

    'This function sets the value for a volume control. Returns True if successful'''

    mxcd = MIXERCONTROLDETAILS()
    vol = MIXERCONTROLDETAILS_UNSIGNED()

    mxcd.item = 0
    mxcd.dwControlID = mxc.dwControlID
    mxcd.cbStruct = sizeof(mxcd)
    mxcd.cbDetails = sizeof(vol)

    #' Allocate a buffer for the control value buffer
    mxcd.paDetails = addressof(vol)
    mxcd.cChannels = 1
    vol.dwValue = volume

    #' Set the control value
    err = mixerSetControlDetails(hmixer, byref(mxcd), 0)

    return (err == MMSYSERR_NOERROR)


def GetMasterVolume():
    hmixer = HMIXER()
    volCtrl = MIXERCONTROL()

    # Obtain the hmixer struct
    err = mixerOpen(byref(hmixer), 0, 0, 0, 0)
    if err != 0:
        return None

    # Obtain the volumne control object
    volCtrl = GetVolumeControl(hmixer, MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
                                MIXERCONTROL_CONTROLTYPE_VOLUME)
    if volCtrl is None:
        return None

    # Then get the volume
    vol = GetVolumeValue(hmixer, volCtrl)
    
    max = volCtrl.Bounds.lBounds.lMaximum
    min = volCtrl.Bounds.lBounds.lMinimum
    vol = 100.0 * (vol - min) / (max - min)
    return vol
    
    
def SetMasterVolume(value):
    hmixer = HMIXER()
    volCtrl = MIXERCONTROL()

    # Obtain the hmixer struct
    err = mixerOpen(byref(hmixer), 0, 0, 0, 0)
    if err != 0:
        return None

    # Obtain the volumne control object
    volCtrl = GetVolumeControl(hmixer, MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
                                MIXERCONTROL_CONTROLTYPE_VOLUME)
    if volCtrl is None:
        return None

    max = volCtrl.Bounds.lBounds.lMaximum
    min = volCtrl.Bounds.lBounds.lMinimum
    volint = int((value / 100.0) * (max - min)) + min
    if volint < min:
        volint = min
    elif volint > max:
        volint = max
    SetVolumeControl(hmixer, volCtrl, volint)
    
    
def ChangeMasterVolumeBy(value):
    hmixer = HMIXER()
    volCtrl = MIXERCONTROL()

    # Obtain the hmixer struct
    err = mixerOpen(byref(hmixer), 0, 0, 0, 0)
    if err != 0:
        return None

    # Obtain the volumne control object
    volCtrl = GetVolumeControl(hmixer, MIXERLINE_COMPONENTTYPE_DST_SPEAKERS, 
                                MIXERCONTROL_CONTROLTYPE_VOLUME)
    if volCtrl is None:
        return None

    # Then get the volume
    old_volume = GetVolumeValue(hmixer, volCtrl)
    
    max = volCtrl.Bounds.lBounds.lMaximum
    min = volCtrl.Bounds.lBounds.lMinimum
    new_volume = int(round((max - min) * value / 100.0)) + old_volume
    if new_volume < min:
        new_volume = min
    elif new_volume > max:
        new_volume = max
    SetVolumeControl(hmixer, volCtrl, new_volume)
    return
    

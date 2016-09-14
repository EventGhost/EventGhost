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

#pylint: disable-msg=C0103,C0301,C0302

# This file gets automatically extended by ctypeslib.dynamic_module, so don't
# edit it yourself.

import sys

# Local imports
from eg.WinApi.Dynamic import *

_Winmm = WinDLL("Winmm")
if __name__ == "__main__":
    try:
        ctypeslib = __import__("ctypeslib.dynamic_module")
    except ImportError:
        print "ctypeslib is not installed!"
    else:
        try:
            ctypeslib.dynamic_module.include(
                "#define UNICODE\n"
                "#define _WIN32_WINNT 0x500\n"
                "#define WIN32_LEAN_AND_MEAN\n"
                "#define NO_STRICT\n"
                "#include <windows.h>\n"
                "#include <Mmsystem.h>\n"
            )
        except WindowsError:
            print "GCC_XML most likely not installed"

#-----------------------------------------------------------------------------#
# everything after the following line is automatically created
#-----------------------------------------------------------------------------#
MIXERCONTROL_CT_CLASS_MASK = 4026531840L  # Variable c_ulong '-268435456ul'
MIXERCONTROL_CT_CLASS_FADER = 1342177280  # Variable c_long '1342177280l'
MIXERCONTROL_CONTROLTYPE_VOLUME = 1342373889  # Variable c_long '1342373889l'
MIXERCONTROL_CONTROLTYPE_BASS = 1342373890  # Variable c_long '1342373890l'
MIXERCONTROL_CONTROLTYPE_TREBLE = 1342373891  # Variable c_long '1342373891l'
MIXERCONTROL_CONTROLTYPE_EQUALIZER = 1342373892  # Variable c_long '1342373892l'
MIXERCONTROL_CONTROLTYPE_FADER = 1342373888  # Variable c_long '1342373888l'
MIXERCONTROL_CT_CLASS_LIST = 1879048192  # Variable c_long '1879048192l'
MIXERCONTROL_CONTROLTYPE_SINGLESELECT = 1879113728  # Variable c_long '1879113728l'
MIXERCONTROL_CONTROLTYPE_MULTIPLESELECT = 1895890944  # Variable c_long '1895890944l'
MIXERCONTROL_CONTROLTYPE_MUX = 1879113729  # Variable c_long '1879113729l'
MIXERCONTROL_CONTROLTYPE_MIXER = 1895890945  # Variable c_long '1895890945l'
MIXERCONTROL_CT_CLASS_METER = 268435456  # Variable c_long '268435456l'
MIXERCONTROL_CONTROLTYPE_BOOLEANMETER = 268500992  # Variable c_long '268500992l'
MIXERCONTROL_CONTROLTYPE_PEAKMETER = 268566529  # Variable c_long '268566529l'
MIXERCONTROL_CONTROLTYPE_SIGNEDMETER = 268566528  # Variable c_long '268566528l'
MIXERCONTROL_CONTROLTYPE_UNSIGNEDMETER = 268632064  # Variable c_long '268632064l'
MIXERCONTROL_CT_CLASS_NUMBER = 805306368  # Variable c_long '805306368l'
MIXERCONTROL_CONTROLTYPE_SIGNED = 805437440  # Variable c_long '805437440l'
MIXERCONTROL_CONTROLTYPE_UNSIGNED = 805502976  # Variable c_long '805502976l'
MIXERCONTROL_CONTROLTYPE_PERCENT = 805634048  # Variable c_long '805634048l'
MIXERCONTROL_CONTROLTYPE_DECIBELS = 805568512  # Variable c_long '805568512l'
MIXERCONTROL_CT_CLASS_SLIDER = 1073741824  # Variable c_long '1073741824l'
MIXERCONTROL_CONTROLTYPE_SLIDER = 1073872896  # Variable c_long '1073872896l'
MIXERCONTROL_CONTROLTYPE_PAN = 1073872897  # Variable c_long '1073872897l'
MIXERCONTROL_CONTROLTYPE_QSOUNDPAN = 1073872898  # Variable c_long '1073872898l'
MIXERCONTROL_CT_CLASS_SWITCH = 536870912  # Variable c_long '536870912l'
MIXERCONTROL_CONTROLTYPE_BOOLEAN = 536936448  # Variable c_long '536936448l'
MIXERCONTROL_CONTROLTYPE_BUTTON = 553713664  # Variable c_long '553713664l'
MIXERCONTROL_CONTROLTYPE_LOUDNESS = 536936452  # Variable c_long '536936452l'
MIXERCONTROL_CONTROLTYPE_MONO = 536936451  # Variable c_long '536936451l'
MIXERCONTROL_CONTROLTYPE_MUTE = 536936450  # Variable c_long '536936450l'
MIXERCONTROL_CONTROLTYPE_ONOFF = 536936449  # Variable c_long '536936449l'
MIXERCONTROL_CONTROLTYPE_STEREOENH = 536936453  # Variable c_long '536936453l'
MIXERCONTROL_CT_CLASS_TIME = 1610612736  # Variable c_long '1610612736l'
MIXERCONTROL_CONTROLTYPE_MICROTIME = 1610809344  # Variable c_long '1610809344l'
MIXERCONTROL_CONTROLTYPE_MILLITIME = 1627586560  # Variable c_long '1627586560l'
MIXERCONTROL_CT_CLASS_CUSTOM = 0  # Variable c_long '0l'
MIXERCONTROL_CONTROLTYPE_CUSTOM = 0  # Variable c_long '0l'
class tMIXERCONTROLDETAILS_UNSIGNED(Structure):
    pass
MIXERCONTROLDETAILS_UNSIGNED = tMIXERCONTROLDETAILS_UNSIGNED
tMIXERCONTROLDETAILS_UNSIGNED._pack_ = 1
tMIXERCONTROLDETAILS_UNSIGNED._fields_ = [
    ('dwValue', DWORD),
]
class tMIXERCONTROLDETAILS_SIGNED(Structure):
    pass
MIXERCONTROLDETAILS_SIGNED = tMIXERCONTROLDETAILS_SIGNED
tMIXERCONTROLDETAILS_SIGNED._pack_ = 1
tMIXERCONTROLDETAILS_SIGNED._fields_ = [
    ('lValue', LONG),
]
class tMIXERCONTROLDETAILS_BOOLEAN(Structure):
    pass
MIXERCONTROLDETAILS_BOOLEAN = tMIXERCONTROLDETAILS_BOOLEAN
tMIXERCONTROLDETAILS_BOOLEAN._pack_ = 1
tMIXERCONTROLDETAILS_BOOLEAN._fields_ = [
    ('fValue', LONG),
]
class tagMIXERCONTROLDETAILS_LISTTEXTW(Structure):
    pass
MIXERCONTROLDETAILS_LISTTEXTW = tagMIXERCONTROLDETAILS_LISTTEXTW
MIXERCONTROLDETAILS_LISTTEXT = MIXERCONTROLDETAILS_LISTTEXTW
tagMIXERCONTROLDETAILS_LISTTEXTW._pack_ = 1
tagMIXERCONTROLDETAILS_LISTTEXTW._fields_ = [
    ('dwParam1', DWORD),
    ('dwParam2', DWORD),
    ('szName', WCHAR * 64),
]
MIXERCONTROL_CONTROLF_DISABLED = 2147483648L  # Variable c_ulong '-2147483648ul'
MIXERCONTROL_CONTROLF_MULTIPLE = 2  # Variable c_long '2l'
MIXERCONTROL_CONTROLF_UNIFORM = 1  # Variable c_long '1l'
MMSYSERR_NOERROR = 0  # Variable c_int '0'
class tagMIXERCAPSW(Structure):
    pass
MIXERCAPSW = tagMIXERCAPSW
MIXERCAPS = MIXERCAPSW
MMVERSION = UINT
tagMIXERCAPSW._pack_ = 1
tagMIXERCAPSW._fields_ = [
    ('wMid', WORD),
    ('wPid', WORD),
    ('vDriverVersion', MMVERSION),
    ('szPname', WCHAR * 32),
    ('fdwSupport', DWORD),
    ('cDestinations', DWORD),
]
class tagMIXERLINEW(Structure):
    pass
MIXERLINEW = tagMIXERLINEW
MIXERLINE = MIXERLINEW
class N13tagMIXERLINEW5DOLLAR_112E(Structure):
    pass
N13tagMIXERLINEW5DOLLAR_112E._pack_ = 1
N13tagMIXERLINEW5DOLLAR_112E._fields_ = [
    ('dwType', DWORD),
    ('dwDeviceID', DWORD),
    ('wMid', WORD),
    ('wPid', WORD),
    ('vDriverVersion', MMVERSION),
    ('szPname', WCHAR * 32),
]
tagMIXERLINEW._pack_ = 1
tagMIXERLINEW._fields_ = [
    ('cbStruct', DWORD),
    ('dwDestination', DWORD),
    ('dwSource', DWORD),
    ('dwLineID', DWORD),
    ('fdwLine', DWORD),
    ('dwUser', DWORD_PTR),
    ('dwComponentType', DWORD),
    ('cChannels', DWORD),
    ('cConnections', DWORD),
    ('cControls', DWORD),
    ('szShortName', WCHAR * 16),
    ('szName', WCHAR * 64),
    ('Target', N13tagMIXERLINEW5DOLLAR_112E),
]
class tagMIXERCONTROLW(Structure):
    pass
MIXERCONTROLW = tagMIXERCONTROLW
MIXERCONTROL = MIXERCONTROLW
class N16tagMIXERCONTROLW5DOLLAR_117E(Union):
    pass
class N16tagMIXERCONTROLW5DOLLAR_1175DOLLAR_118E(Structure):
    pass
N16tagMIXERCONTROLW5DOLLAR_1175DOLLAR_118E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_1175DOLLAR_118E._fields_ = [
    ('lMinimum', LONG),
    ('lMaximum', LONG),
]
class N16tagMIXERCONTROLW5DOLLAR_1175DOLLAR_119E(Structure):
    pass
N16tagMIXERCONTROLW5DOLLAR_1175DOLLAR_119E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_1175DOLLAR_119E._fields_ = [
    ('dwMinimum', DWORD),
    ('dwMaximum', DWORD),
]
N16tagMIXERCONTROLW5DOLLAR_117E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_117E._anonymous_ = ['_0', '_1']
N16tagMIXERCONTROLW5DOLLAR_117E._fields_ = [
    ('_0', N16tagMIXERCONTROLW5DOLLAR_1175DOLLAR_118E),
    ('_1', N16tagMIXERCONTROLW5DOLLAR_1175DOLLAR_119E),
    ('dwReserved', DWORD * 6),
]
class N16tagMIXERCONTROLW5DOLLAR_120E(Union):
    pass
N16tagMIXERCONTROLW5DOLLAR_120E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_120E._fields_ = [
    ('cSteps', DWORD),
    ('cbCustomData', DWORD),
    ('dwReserved', DWORD * 6),
]
tagMIXERCONTROLW._pack_ = 1
tagMIXERCONTROLW._fields_ = [
    ('cbStruct', DWORD),
    ('dwControlID', DWORD),
    ('dwControlType', DWORD),
    ('fdwControl', DWORD),
    ('cMultipleItems', DWORD),
    ('szShortName', WCHAR * 16),
    ('szName', WCHAR * 64),
    ('Bounds', N16tagMIXERCONTROLW5DOLLAR_117E),
    ('Metrics', N16tagMIXERCONTROLW5DOLLAR_120E),
]
class tagMIXERLINECONTROLSW(Structure):
    pass
MIXERLINECONTROLSW = tagMIXERLINECONTROLSW
MIXERLINECONTROLS = MIXERLINECONTROLSW
class N21tagMIXERLINECONTROLSW5DOLLAR_122E(Union):
    pass
N21tagMIXERLINECONTROLSW5DOLLAR_122E._pack_ = 1
N21tagMIXERLINECONTROLSW5DOLLAR_122E._fields_ = [
    ('dwControlID', DWORD),
    ('dwControlType', DWORD),
]
LPMIXERCONTROLW = POINTER(tagMIXERCONTROLW)
tagMIXERLINECONTROLSW._pack_ = 1
tagMIXERLINECONTROLSW._anonymous_ = ['_0']
tagMIXERLINECONTROLSW._fields_ = [
    ('cbStruct', DWORD),
    ('dwLineID', DWORD),
    ('_0', N21tagMIXERLINECONTROLSW5DOLLAR_122E),
    ('cControls', DWORD),
    ('cbmxctrl', DWORD),
    ('pamxctrl', LPMIXERCONTROLW),
]
class tMIXERCONTROLDETAILS(Structure):
    pass
MIXERCONTROLDETAILS = tMIXERCONTROLDETAILS
class N20tMIXERCONTROLDETAILS5DOLLAR_123E(Union):
    pass
N20tMIXERCONTROLDETAILS5DOLLAR_123E._pack_ = 1
N20tMIXERCONTROLDETAILS5DOLLAR_123E._fields_ = [
    ('hwndOwner', HWND),
    ('cMultipleItems', DWORD),
]
tMIXERCONTROLDETAILS._pack_ = 1
tMIXERCONTROLDETAILS._anonymous_ = ['_0']
tMIXERCONTROLDETAILS._fields_ = [
    ('cbStruct', DWORD),
    ('dwControlID', DWORD),
    ('cChannels', DWORD),
    ('_0', N20tMIXERCONTROLDETAILS5DOLLAR_123E),
    ('cbDetails', DWORD),
    ('paDetails', LPVOID),
]
HMIXER = HANDLE
MMRESULT = UINT
LPHMIXER = POINTER(HMIXER)
mixerOpen = _Winmm.mixerOpen
mixerOpen.restype = MMRESULT
mixerOpen.argtypes = [LPHMIXER, UINT, DWORD_PTR, DWORD_PTR, DWORD]
LPMIXERCAPSW = POINTER(tagMIXERCAPSW)
mixerGetDevCapsW = _Winmm.mixerGetDevCapsW
mixerGetDevCapsW.restype = MMRESULT
mixerGetDevCapsW.argtypes = [UINT_PTR, LPMIXERCAPSW, UINT]
mixerGetDevCaps = mixerGetDevCapsW  # alias
HMIXEROBJ = HANDLE
LPMIXERLINEW = POINTER(tagMIXERLINEW)
mixerGetLineInfoW = _Winmm.mixerGetLineInfoW
mixerGetLineInfoW.restype = MMRESULT
mixerGetLineInfoW.argtypes = [HMIXEROBJ, LPMIXERLINEW, DWORD]
mixerGetLineInfo = mixerGetLineInfoW  # alias
LPMIXERLINECONTROLSW = POINTER(tagMIXERLINECONTROLSW)
mixerGetLineControlsW = _Winmm.mixerGetLineControlsW
mixerGetLineControlsW.restype = MMRESULT
mixerGetLineControlsW.argtypes = [HMIXEROBJ, LPMIXERLINECONTROLSW, DWORD]
mixerGetLineControls = mixerGetLineControlsW  # alias
LPMIXERCONTROLDETAILS = POINTER(tMIXERCONTROLDETAILS)
mixerGetControlDetailsW = _Winmm.mixerGetControlDetailsW
mixerGetControlDetailsW.restype = MMRESULT
mixerGetControlDetailsW.argtypes = [HMIXEROBJ, LPMIXERCONTROLDETAILS, DWORD]
mixerGetControlDetails = mixerGetControlDetailsW  # alias
MIXER_GETLINEINFOF_DESTINATION = 0  # Variable c_long '0l'
MIXER_GETLINEINFOF_SOURCE = 1  # Variable c_long '1l'
MIXER_GETLINECONTROLSF_ALL = 0  # Variable c_long '0l'
MIXER_GETLINECONTROLSF_ONEBYID = 1  # Variable c_long '1l'
MIXER_GETCONTROLDETAILSF_VALUE = 0  # Variable c_long '0l'
MIXER_GETCONTROLDETAILSF_LISTTEXT = 1  # Variable c_long '1l'
mixerGetNumDevs = _Winmm.mixerGetNumDevs
mixerGetNumDevs.restype = UINT
mixerGetNumDevs.argtypes = []
mixerSetControlDetails = _Winmm.mixerSetControlDetails
mixerSetControlDetails.restype = MMRESULT
mixerSetControlDetails.argtypes = [HMIXEROBJ, LPMIXERCONTROLDETAILS, DWORD]
MIXERLINE_COMPONENTTYPE_DST_SPEAKERS = 4  # Variable c_long '4l'
MIXER_GETLINEINFOF_COMPONENTTYPE = 3  # Variable c_long '3l'
MIXER_GETLINECONTROLSF_ONEBYTYPE = 2  # Variable c_long '2l'

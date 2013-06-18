# Created by makepy.py version 0.4.91
# By python version 2.4.1 (#65, Mar 30 2005, 09:33:37) [MSC v.1310 32 bit (Intel)]
# From type library '{001000AF-1DEF-0001-10B6-DC5BA692C858}'
# On Wed Apr 27 17:33:46 2005
"""X10 Controls"""
makepy_version = '0.4.91'
python_version = 0x20401f0

import win32com.client.CLSIDToClass, pythoncom
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing and pythoncom.Empty
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{001000AF-1DEF-0001-10B6-DC5BA692C858}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

class constants:
    KEY_DOWN                      =0x1        # from enum tagEKeyState
    KEY_DURATION                  =0x3        # from enum tagEKeyState
    KEY_GETQUEUE                  =0x4        # from enum tagEKeyState
    KEY_SINGLE                    =0x0        # from enum tagEKeyState
    KEY_UP                        =0x2        # from enum tagEKeyState
    X10COMM_ALL_LIGHTS_OFF        =0x45       # from enum tagEX10Comm
    X10COMM_ALL_LIGHTS_ON         =0x44       # from enum tagEX10Comm
    X10COMM_ALL_OFF               =0x46       # from enum tagEX10Comm
    X10COMM_BRIGHT                =0x42       # from enum tagEX10Comm
    X10COMM_DIM                   =0x43       # from enum tagEX10Comm
    X10COMM_DIRECT                =0x49       # from enum tagEX10Comm
    X10COMM_EVENT                 =0x48       # from enum tagEX10Comm
    X10COMM_EXTENDED              =0x47       # from enum tagEX10Comm
    X10COMM_OFF                   =0x41       # from enum tagEX10Comm
    X10COMM_ON                    =0x40       # from enum tagEX10Comm
    X10CMD_0                      =0x14       # from enum tagEX10Command
    X10CMD_1                      =0x2c       # from enum tagEX10Command
    X10CMD_1_OFF                  =0x32       # from enum tagEX10Command
    X10CMD_1_ON                   =0x31       # from enum tagEX10Command
    X10CMD_2                      =0x2f       # from enum tagEX10Command
    X10CMD_2_OFF                  =0x34       # from enum tagEX10Command
    X10CMD_2_ON                   =0x33       # from enum tagEX10Command
    X10CMD_3                      =0x2a       # from enum tagEX10Command
    X10CMD_3_OFF                  =0x35       # from enum tagEX10Command
    X10CMD_3_ON                   =0x2d       # from enum tagEX10Command
    X10CMD_4                      =0x16       # from enum tagEX10Command
    X10CMD_4_OFF                  =0x37       # from enum tagEX10Command
    X10CMD_4_ON                   =0x36       # from enum tagEX10Command
    X10CMD_5                      =0x1b       # from enum tagEX10Command
    X10CMD_6                      =0x19       # from enum tagEX10Command
    X10CMD_7                      =0x17       # from enum tagEX10Command
    X10CMD_8                      =0x1a       # from enum tagEX10Command
    X10CMD_9                      =0x15       # from enum tagEX10Command
    X10CMD_AB                     =0x12       # from enum tagEX10Command
    X10CMD_ALL_LIGHTS_OFF         =0x45       # from enum tagEX10Command
    X10CMD_ALL_LIGHTS_ON          =0x44       # from enum tagEX10Command
    X10CMD_ALL_LTS_ON             =0x1f       # from enum tagEX10Command
    X10CMD_ALL_OFF                =0x46       # from enum tagEX10Command
    X10CMD_AUD_AUX_E              =0x24       # from enum tagEX10Command
    X10CMD_AUTOFOCUS              =0x8b       # from enum tagEX10Command
    X10CMD_BOOKMARK               =0x61       # from enum tagEX10Command
    X10CMD_BOOKSYMBOL             =0x53       # from enum tagEX10Command
    X10CMD_BRIGHT                 =0x42       # from enum tagEX10Command
    X10CMD_BUTTON_A               =0x4a       # from enum tagEX10Command
    X10CMD_BUTTON_B               =0x4b       # from enum tagEX10Command
    X10CMD_BUTTON_C               =0x4c       # from enum tagEX10Command
    X10CMD_BUTTON_D               =0x4d       # from enum tagEX10Command
    X10CMD_BUTTON_E               =0x4e       # from enum tagEX10Command
    X10CMD_BUTTON_F               =0x4f       # from enum tagEX10Command
    X10CMD_CAB_AUX_B              =0x22       # from enum tagEX10Command
    X10CMD_CAMCENTER              =0x72       # from enum tagEX10Command
    X10CMD_CAMCLEARALLPOSITIONS   =0x74       # from enum tagEX10Command
    X10CMD_CAMENTERSWEEPTESTMODE  =0x75       # from enum tagEX10Command
    X10CMD_CAMGOPOSITION1         =0x6a       # from enum tagEX10Command
    X10CMD_CAMGOPOSITION2         =0x6c       # from enum tagEX10Command
    X10CMD_CAMGOPOSITION3         =0x6e       # from enum tagEX10Command
    X10CMD_CAMGOPOSITION4         =0x70       # from enum tagEX10Command
    X10CMD_CAMSETPOSITION1        =0x6b       # from enum tagEX10Command
    X10CMD_CAMSETPOSITION2        =0x6d       # from enum tagEX10Command
    X10CMD_CAMSETPOSITION3        =0x6f       # from enum tagEX10Command
    X10CMD_CAMSETPOSITION4        =0x71       # from enum tagEX10Command
    X10CMD_CAMSWEEP               =0x73       # from enum tagEX10Command
    X10CMD_CHECK                  =0x63       # from enum tagEX10Command
    X10CMD_CH_DN                  =0x30       # from enum tagEX10Command
    X10CMD_CH_UP                  =0x29       # from enum tagEX10Command
    X10CMD_DIM                    =0x43       # from enum tagEX10Command
    X10CMD_DIRPADDOWN             =0x5c       # from enum tagEX10Command
    X10CMD_DIRPADLEFT             =0x5b       # from enum tagEX10Command
    X10CMD_DIRPADLEFTDOWN         =0x5f       # from enum tagEX10Command
    X10CMD_DIRPADLEFTUP           =0x60       # from enum tagEX10Command
    X10CMD_DIRPADRIGHT            =0x59       # from enum tagEX10Command
    X10CMD_DIRPADRIGHTDOWN        =0x5e       # from enum tagEX10Command
    X10CMD_DIRPADRIGHTUP          =0x5d       # from enum tagEX10Command
    X10CMD_DIRPADUP               =0x5a       # from enum tagEX10Command
    X10CMD_DISPLAY                =0x10       # from enum tagEX10Command
    X10CMD_DN                     =0xc        # from enum tagEX10Command
    X10CMD_DVDMODE                =0x51       # from enum tagEX10Command
    X10CMD_DVD_AUX_D              =0x20       # from enum tagEX10Command
    X10CMD_ENTER                  =0xf        # from enum tagEX10Command
    X10CMD_EVENT                  =0x48       # from enum tagEX10Command
    X10CMD_EXIT                   =0x18       # from enum tagEX10Command
    X10CMD_EXTENDED               =0x47       # from enum tagEX10Command
    X10CMD_FF                     =0x4        # from enum tagEX10Command
    X10CMD_FILLEDHAND             =0x76       # from enum tagEX10Command
    X10CMD_FOCUSDOWN              =0x84       # from enum tagEX10Command
    X10CMD_FOCUSUP                =0x83       # from enum tagEX10Command
    X10CMD_GOPOSITION5            =0x79       # from enum tagEX10Command
    X10CMD_GOPOSITION6            =0x7b       # from enum tagEX10Command
    X10CMD_GOPOSITION7            =0x7d       # from enum tagEX10Command
    X10CMD_GOPOSITION8            =0x7f       # from enum tagEX10Command
    X10CMD_GOPOSITION9            =0x81       # from enum tagEX10Command
    X10CMD_HANDSYMBOL             =0x54       # from enum tagEX10Command
    X10CMD_INPUT                  =0x89       # from enum tagEX10Command
    X10CMD_IRISDOWN               =0x86       # from enum tagEX10Command
    X10CMD_IRISUP                 =0x85       # from enum tagEX10Command
    X10CMD_IR_ALL_OFF             =0x26       # from enum tagEX10Command
    X10CMD_LEFT                   =0xd        # from enum tagEX10Command
    X10CMD_LEFTMOUSEDOUBLECLICK   =0x64       # from enum tagEX10Command
    X10CMD_LEFTMOUSEDOWN          =0x55       # from enum tagEX10Command
    X10CMD_LEFTMOUSEUP            =0x56       # from enum tagEX10Command
    X10CMD_MENU                   =0x9        # from enum tagEX10Command
    X10CMD_MUTE                   =0x28       # from enum tagEX10Command
    X10CMD_NONE                   =0x0        # from enum tagEX10Command
    X10CMD_OFF                    =0x41       # from enum tagEX10Command
    X10CMD_OKAY                   =0x11       # from enum tagEX10Command
    X10CMD_ON                     =0x40       # from enum tagEX10Command
    X10CMD_PANDOWN                =0x69       # from enum tagEX10Command
    X10CMD_PANLEFT                =0x66       # from enum tagEX10Command
    X10CMD_PANRIGHT               =0x67       # from enum tagEX10Command
    X10CMD_PANUP                  =0x68       # from enum tagEX10Command
    X10CMD_PAUSE                  =0x0        # from enum tagEX10Command
    X10CMD_PC                     =0x49       # from enum tagEX10Command
    X10CMD_PLAY                   =0x6        # from enum tagEX10Command
    X10CMD_POWER                  =0x1e       # from enum tagEX10Command
    X10CMD_PTZOFF                 =0x88       # from enum tagEX10Command
    X10CMD_PTZON                  =0x87       # from enum tagEX10Command
    X10CMD_RECALL                 =0x2e       # from enum tagEX10Command
    X10CMD_RECORD                 =0x1        # from enum tagEX10Command
    X10CMD_RELEASE                =0x3f       # from enum tagEX10Command
    X10CMD_RESIZE                 =0x62       # from enum tagEX10Command
    X10CMD_RETURN                 =0xe        # from enum tagEX10Command
    X10CMD_REWIND                 =0x2        # from enum tagEX10Command
    X10CMD_RFRECEIVERINIT         =0xfe       # from enum tagEX10Command
    X10CMD_RIGHT                  =0xb        # from enum tagEX10Command
    X10CMD_RIGHTMOUSEDOUBLECLICK  =0x65       # from enum tagEX10Command
    X10CMD_RIGHTMOUSEDOWN         =0x57       # from enum tagEX10Command
    X10CMD_RIGHTMOUSEUP           =0x58       # from enum tagEX10Command
    X10CMD_SAT_AUX_C              =0x21       # from enum tagEX10Command
    X10CMD_SETPOSITION5           =0x7a       # from enum tagEX10Command
    X10CMD_SETPOSITION6           =0x7c       # from enum tagEX10Command
    X10CMD_SETPOSITION7           =0x7e       # from enum tagEX10Command
    X10CMD_SETPOSITION8           =0x80       # from enum tagEX10Command
    X10CMD_SETPOSITION9           =0x82       # from enum tagEX10Command
    X10CMD_SETUP                  =0x2b       # from enum tagEX10Command
    X10CMD_SKIP_DN                =0xa        # from enum tagEX10Command
    X10CMD_SKIP_UP                =0x3        # from enum tagEX10Command
    X10CMD_STOP                   =0x5        # from enum tagEX10Command
    X10CMD_SUBTITLE               =0x7        # from enum tagEX10Command
    X10CMD_TITLE                  =0x8        # from enum tagEX10Command
    X10CMD_TV                     =0x1d       # from enum tagEX10Command
    X10CMD_TVMODE                 =0x50       # from enum tagEX10Command
    X10CMD_UP                     =0x13       # from enum tagEX10Command
    X10CMD_VALUE56                =0x38       # from enum tagEX10Command
    X10CMD_VALUE57                =0x39       # from enum tagEX10Command
    X10CMD_VALUE58                =0x3a       # from enum tagEX10Command
    X10CMD_VALUE59                =0x3b       # from enum tagEX10Command
    X10CMD_VALUE60                =0x3c       # from enum tagEX10Command
    X10CMD_VALUE61                =0x3d       # from enum tagEX10Command
    X10CMD_VALUE62                =0x3e       # from enum tagEX10Command
    X10CMD_VCR_AUX_A              =0x1c       # from enum tagEX10Command
    X10CMD_VOL_DN                 =0x25       # from enum tagEX10Command
    X10CMD_VOL_UP                 =0x23       # from enum tagEX10Command
    X10CMD_WEBMODE                =0x52       # from enum tagEX10Command
    X10CMD_X10CMD_AUX_F           =0x27       # from enum tagEX10Command
    X10CMD_ZOOM                   =0x8a       # from enum tagEX10Command
    X10CMD_ZOOMIN                 =0x77       # from enum tagEX10Command
    X10CMD_ZOOMOUT                =0x78       # from enum tagEX10Command
    X10STATE_ACTIVE               =0x2        # from enum tagEX10CommandState
    X10STATE_DISABLED             =0x0        # from enum tagEX10CommandState
    X10STATE_EXECUTING            =0x4        # from enum tagEX10CommandState
    X10STATE_FAILURE              =0x6        # from enum tagEX10CommandState
    X10STATE_NONE                 =0x1        # from enum tagEX10CommandState
    X10STATE_QUEUED               =0x3        # from enum tagEX10CommandState
    X10STATE_SUCCESS              =0x5        # from enum tagEX10CommandState
    X10EVENT_ABSTIME              =0x2        # from enum tagEX10EventType
    X10EVENT_NONE                 =0x0        # from enum tagEX10EventType
    X10EVENT_ONCOMPLETION         =0x5        # from enum tagEX10EventType
    X10EVENT_ONEVENT              =0x4        # from enum tagEX10EventType
    X10EVENT_ONFAILURE            =0x6        # from enum tagEX10EventType
    X10EVENT_RELTIME              =0x1        # from enum tagEX10EventType
    X10EVENT_REPEATING            =0x3        # from enum tagEX10EventType
    X10EVENT_SCRIPTED             =0x7        # from enum tagEX10EventType
    X10KEY_OFF                    =0x2        # from enum tagEX10Key
    X10KEY_ON                     =0x1        # from enum tagEX10Key
    X10KEY_REPEAT                 =0x3        # from enum tagEX10Key
    X10SCOPE_COMMAND              =0x5        # from enum tagEX10Scope
    X10SCOPE_CONNECTION           =0x2        # from enum tagEX10Scope
    X10SCOPE_DEVICE               =0x4        # from enum tagEX10Scope
    X10SCOPE_DEVICETYPE           =0x3        # from enum tagEX10Scope
    X10SCOPE_LOCAL                =0x1        # from enum tagEX10Scope
    X10SCOPE_SKIN                 =0x0        # from enum tagEX10Scope

from win32com.client import DispatchBaseClass
class IX10Control(DispatchBaseClass):
    """IX10Control Interface"""
    CLSID = IID('{001000AF-3DEF-0001-10B6-DC5BA692C858}')
    coclass_clsid = IID('{001000AF-2DEF-0001-10B6-DC5BA692C858}')

    def Close(self):
        return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), (),)

    def Command(self, varCommand=defaultNamedNotOptArg, varParam=defaultNamedNotOptArg):
        return self._ApplyTypes_(2, 1, (12, 0), ((12, 1), (12, 1)), 'Command', None,varCommand, varParam)

    def Hide(self):
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), (),)

    def Show(self, fIsHideOnCloseSet=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((11, 1),),fIsHideOnCloseSet)

    _prop_map_get_ = {
        "Control": (1, 2, (12, 0), (), "Control", None),
        # Method 'Interface' returns object of type 'IX10Interface'
        "Interface": (0, 2, (9, 0), (), "Interface", '{001000AF-3DEF-0003-10B6-DC5BA692C858}'),
    }
    _prop_map_put_ = {
    }
    # Default property for this class is 'Interface'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (9, 0), (), "Interface", '{001000AF-3DEF-0003-10B6-DC5BA692C858}'))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IX10Interface(DispatchBaseClass):
    """IX10Interface Interface"""
    CLSID = IID('{001000AF-3DEF-0003-10B6-DC5BA692C858}')
    coclass_clsid = IID('{001000AF-2DEF-0002-10B6-DC5BA692C858}')

    def Breakpoints(self, ppBreakpoints=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), ((16393, 0),),ppBreakpoints)

    def CancelAllCommands(self):
        return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

    def CheckCommand(self):
        return self._oleobj_.InvokeTypes(25, LCID, 1, (24, 0), (),)

    # Result is of type IX10Control
    def CreateControl(self, varControl=defaultNamedNotOptArg, varSkin=defaultNamedNotOptArg):
        ret = self._oleobj_.InvokeTypes(30, LCID, 1, (9, 0), ((12, 1), (12, 1)),varControl, varSkin)
        if ret is not None:
            ret = Dispatch(ret, 'CreateControl', '{001000AF-3DEF-0001-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def GetAdaptersPresent(self, lAdapterType=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(34, LCID, 1, (3, 0), ((3, 0),),lAdapterType)

    def GetNextCommand(self):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (24, 0), (),)

    # Result is of type IXRecvCommand
    def LastRecv(self, lHistoryIndex=0):
        """Received command history"""
        ret = self._oleobj_.InvokeTypes(26, LCID, 1, (9, 0), ((3, 49),),lHistoryIndex)
        if ret is not None:
            ret = Dispatch(ret, 'LastRecv', '{001000AF-3DEF-0018-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    # Result is of type IXSendCommand
    def LastSend(self, lHistoryIndex=0):
        """Send command history"""
        ret = self._oleobj_.InvokeTypes(27, LCID, 1, (9, 0), ((3, 49),),lHistoryIndex)
        if ret is not None:
            ret = Dispatch(ret, 'LastSend', '{001000AF-3DEF-0014-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def QueueDepth(self):
        return self._oleobj_.InvokeTypes(8, LCID, 1, (3, 0), (),)

    def QueueDepthWithCommand(self, vCommand=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(9, LCID, 1, (3, 0), ((12, 1),),vCommand)

    def ResumeCommands(self):
        return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), (),)

    def Send(self, vCommand=defaultNamedNotOptArg, vScope=defaultNamedNotOptArg, vAddress='', vDuration=0, vWait=0):
        """Send a command"""
        return self._ApplyTypes_(4, 1, (12, 32), ((12, 1), (12, 1), (12, 49), (12, 49), (12, 49)), 'Send', None,vCommand, vScope, vAddress, vDuration, vWait)

    def SendKeyDown(self, vCommand=defaultNamedNotOptArg, vScope=defaultNamedNotOptArg, vAddress=''):
        """Send a single key press"""
        return self._ApplyTypes_(5, 1, (12, 32), ((12, 1), (12, 1), (12, 49)), 'SendKeyDown', None,vCommand, vScope, vAddress)

    def SendKeyUp(self, vCommand=defaultNamedNotOptArg, vScope=defaultNamedNotOptArg, vAddress=''):
        """Send a single key release"""
        return self._ApplyTypes_(6, 1, (12, 32), ((12, 1), (12, 1), (12, 49)), 'SendKeyUp', None,vCommand, vScope, vAddress)

    def SendPriority(self, vCommand=defaultNamedNotOptArg, vScope=defaultNamedNotOptArg, vAddress='', vDuration=0):
        """Immediately send this command"""
        return self._ApplyTypes_(3, 1, (12, 32), ((12, 1), (12, 1), (12, 49), (12, 49)), 'SendPriority', None,vCommand, vScope, vAddress, vDuration)

    def SingleCommandInto(self):
        return self._oleobj_.InvokeTypes(23, LCID, 1, (24, 0), (),)

    def SingleCommandOver(self):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (24, 0), (),)

    def StartRecord(self):
        """Start/Resume macro recording"""
        return self._oleobj_.InvokeTypes(11, LCID, 1, (24, 0), (),)

    # Result is of type IXCommand
    def StopRecord(self, vCommand=defaultNamedNotOptArg):
        """Stop/pause macro recording"""
        ret = self._oleobj_.InvokeTypes(12, LCID, 1, (9, 0), ((12, 1),),vCommand)
        if ret is not None:
            ret = Dispatch(ret, 'StopRecord', '{001000AF-3DEF-0019-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def SuspendCommands(self):
        """Suspend Commands"""
        return self._oleobj_.InvokeTypes(19, LCID, 1, (24, 0), (),)

    def Update(self):
        return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), (),)

    _prop_map_get_ = {
        # Method 'Commands' returns object of type 'IXCommands'
        "Commands": (15, 2, (9, 0), (), "Commands", '{001000AF-3DEF-001A-10B6-DC5BA692C858}'),
        "Connection": (1, 2, (12, 0), (), "Connection", None),
        # Method 'ConnectionTypes' returns object of type 'IXConnectionTypes'
        "ConnectionTypes": (18, 2, (9, 0), (), "ConnectionTypes", '{001000AF-3DEF-000A-10B6-DC5BA692C858}'),
        # Method 'Connections' returns object of type 'IXConnections'
        "Connections": (13, 2, (9, 0), (), "Connections", '{001000AF-3DEF-0009-10B6-DC5BA692C858}'),
        "Device": (2, 2, (12, 0), (), "Device", None),
        # Method 'DeviceTypes' returns object of type 'IXDeviceTypes'
        "DeviceTypes": (17, 2, (9, 0), (), "DeviceTypes", '{001000AF-3DEF-0012-10B6-DC5BA692C858}'),
        # Method 'Devices' returns object of type 'IXDevices'
        "Devices": (14, 2, (9, 0), (), "Devices", '{001000AF-3DEF-0010-10B6-DC5BA692C858}'),
        "HouseCodeEventMask": (32, 2, (3, 0), (), "HouseCodeEventMask", None),
        # Method 'Objects' returns object of type 'IXObjects'
        "Objects": (16, 2, (9, 0), (), "Objects", '{001000AF-3DEF-001C-10B6-DC5BA692C858}'),
        "RecvHistoryLength": (28, 2, (3, 0), (), "RecvHistoryLength", None),
        "SendHistoryLength": (29, 2, (3, 0), (), "SendHistoryLength", None),
        "UnitCodeEventMask": (33, 2, (3, 0), (), "UnitCodeEventMask", None),
        "Version": (31, 2, (12, 0), (), "Version", None),
    }
    _prop_map_put_ = {
        "Connection": ((1, LCID, 4, 0),()),
        "Device": ((2, LCID, 4, 0),()),
        "HouseCodeEventMask": ((32, LCID, 4, 0),()),
        "RecvHistoryLength": ((28, LCID, 4, 0),()),
        "SendHistoryLength": ((29, LCID, 4, 0),()),
        "UnitCodeEventMask": ((33, LCID, 4, 0),()),
    }

class IXCollection(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0005-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Add(self, vObject=defaultNamedNotOptArg):
        """Add an item"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((12, 1),),vObject)

    def Insert(self, Index=defaultNamedNotOptArg, vObject=defaultNamedNotOptArg):
        """Insert an item"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 1), (12, 1)),Index, vObject)

    def Remove(self, Index=defaultNamedNotOptArg):
        """Index an item"""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 1),),Index)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IXCommand(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0019-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Address": (6, 2, (12, 0), (), "Address", None),
        "Comment": (2, 2, (12, 0), (), "Comment", None),
        # Method 'Connection' returns object of type 'IXConnection'
        "Connection": (5, 2, (9, 0), (), "Connection", '{001000AF-3DEF-0008-10B6-DC5BA692C858}'),
        "Enabled": (3, 2, (3, 0), (), "Enabled", None),
        # Method 'Events' returns object of type 'IXEvents'
        "Events": (4, 2, (9, 0), (), "Events", '{001000AF-3DEF-0017-10B6-DC5BA692C858}'),
        "ID": (11, 2, (8, 0), (), "ID", None),
        "Label": (1, 2, (12, 0), (), "Label", None),
        "Name": (0, 2, (12, 0), (), "Name", None),
        # Method 'Owner' returns object of type 'IXCommand'
        "Owner": (9, 2, (9, 0), (), "Owner", '{001000AF-3DEF-0019-10B6-DC5BA692C858}'),
        "Scope": (8, 2, (3, 0), (), "Scope", None),
        "ScopeName": (7, 2, (12, 0), (), "ScopeName", None),
        # Method 'Values' returns object of type 'IXProperties'
        "Values": (10, 2, (9, 0), (), "Values", '{001000AF-3DEF-0007-10B6-DC5BA692C858}'),
    }
    _prop_map_put_ = {
        "Address": ((6, LCID, 4, 0),()),
        "Comment": ((2, LCID, 4, 0),()),
        "Connection": ((5, LCID, 4, 0),()),
        "Enabled": ((3, LCID, 4, 0),()),
        "Events": ((4, LCID, 4, 0),()),
        "Label": ((1, LCID, 4, 0),()),
        "Name": ((0, LCID, 4, 0),()),
        "Owner": ((9, LCID, 4, 0),()),
        "Scope": ((8, LCID, 4, 0),()),
        "ScopeName": ((7, LCID, 4, 0),()),
        "Values": ((10, LCID, 4, 0),()),
    }
    # Default property for this class is 'Name'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Name", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXCommands(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-001A-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Add(self, vObject=defaultNamedNotOptArg):
        """Add an item"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((12, 1),),vObject)

    def FilterItem(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(6, 1, (12, 0), ((12, 1),), 'FilterItem', None,Index)

    def GetFilterItemCount(self):
        return self._oleobj_.InvokeTypes(7, LCID, 1, (3, 0), (),)

    def Insert(self, Index=defaultNamedNotOptArg, vObject=defaultNamedNotOptArg):
        """Insert an item"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 1), (12, 1)),Index, vObject)

    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), 'Item', None,Index)

    # Result is of type IXCommand
    def New(self):
        ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
        if ret is not None:
            ret = Dispatch(ret, 'New', '{001000AF-3DEF-0019-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def Remove(self, Index=defaultNamedNotOptArg):
        """Index an item"""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 1),),Index)

    def SetFilter(self, eScope=defaultNamedNotOptArg, pszScope=defaultNamedNotOptArg, fIsVisibleOnly=defaultNamedNotOptArg, fIsEnabledOnly=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(8, LCID, 1, (24, 0), ((3, 1), (8, 1), (11, 1), (11, 1)),eScope, pszScope, fIsVisibleOnly, fIsEnabledOnly)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    # Default method for this class is 'Item'
    def __call__(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), '__call__', None,Index)

    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IXConnection(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0008-10B6-DC5BA692C858}')
    coclass_clsid = None

    def CancelAllCommands(self):
        return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

    def Connect(self):
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (),)

    def ConnectStatus(self):
        # Result is a Unicode object - return as-is for this version of Python
        return self._oleobj_.InvokeTypes(5, LCID, 1, (8, 0), (),)

    def ConnectTime(self):
        return self._oleobj_.InvokeTypes(6, LCID, 1, (5, 0), (),)

    def Disconnect(self):
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), (),)

    def Extended(self):
        return self._ApplyTypes_(8, 1, (12, 0), (), 'Extended', None,)

    def IsConnected(self):
        return self._oleobj_.InvokeTypes(7, LCID, 1, (3, 0), (),)

    def QueueDepth(self):
        return self._oleobj_.InvokeTypes(9, LCID, 1, (3, 0), (),)

    def Send(self, varCommand=defaultNamedNotOptArg, varAddress='', varDuration=0, varWait=0):
        """Send a command"""
        return self._ApplyTypes_(12, 1, (12, 32), ((12, 1), (12, 49), (12, 49), (12, 49)), 'Send', None,varCommand, varAddress, varDuration, varWait)

    def SendKeyDown(self, varCommand=defaultNamedNotOptArg, varAddress=''):
        """Send a single key press"""
        return self._ApplyTypes_(13, 1, (12, 32), ((12, 1), (12, 49)), 'SendKeyDown', None,varCommand, varAddress)

    def SendKeyUp(self, varCommand=defaultNamedNotOptArg, varAddress=''):
        """Send a single key release"""
        return self._ApplyTypes_(14, 1, (12, 32), ((12, 1), (12, 49)), 'SendKeyUp', None,varCommand, varAddress)

    def SendPriority(self, varCommand=defaultNamedNotOptArg, varAddress='', varDuration=0):
        """Immediately send this command"""
        return self._ApplyTypes_(11, 1, (12, 32), ((12, 0), (12, 49), (12, 49)), 'SendPriority', None,varCommand, varAddress, varDuration)

    _prop_map_get_ = {
        "Comment": (2, 2, (12, 0), (), "Comment", None),
        "Name": (0, 2, (12, 0), (), "Name", None),
        # Method 'Values' returns object of type 'IXProperties'
        "Values": (1, 2, (9, 0), (), "Values", '{001000AF-3DEF-0007-10B6-DC5BA692C858}'),
    }
    _prop_map_put_ = {
        "Comment": ((2, LCID, 4, 0),()),
        "Name": ((0, LCID, 4, 0),()),
        "Values": ((1, LCID, 4, 0),()),
    }
    # Default property for this class is 'Name'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Name", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXConnectionType(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-000B-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Name": (0, 2, (12, 0), (), "Name", None),
    }
    _prop_map_put_ = {
        "Name": ((0, LCID, 4, 0),()),
    }
    # Default property for this class is 'Name'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Name", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXConnectionTypeLocalRecv(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-000D-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Name": (0, 2, (12, 0), (), "Name", None),
    }
    _prop_map_put_ = {
        "Name": ((0, LCID, 4, 0),()),
    }
    # Default property for this class is 'Name'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Name", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXConnectionTypeLocalSend(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-000C-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Name": (0, 2, (12, 0), (), "Name", None),
    }
    _prop_map_put_ = {
        "Name": ((0, LCID, 4, 0),()),
    }
    # Default property for this class is 'Name'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Name", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXConnectionTypeNetClient(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-000E-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Name": (0, 2, (12, 0), (), "Name", None),
    }
    _prop_map_put_ = {
        "Name": ((0, LCID, 4, 0),()),
    }
    # Default property for this class is 'Name'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Name", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXConnectionTypeNetServer(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-000F-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Name": (0, 2, (12, 0), (), "Name", None),
    }
    _prop_map_put_ = {
        "Name": ((0, LCID, 4, 0),()),
    }
    # Default property for this class is 'Name'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Name", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXConnectionTypes(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-000A-10B6-DC5BA692C858}')
    coclass_clsid = None

    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, Index=defaultNamedNotOptArg):
        """Return an item"""
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), 'Item', None,Index)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    # Default method for this class is 'Item'
    def __call__(self, Index=defaultNamedNotOptArg):
        """Return an item"""
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), '__call__', None,Index)

    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IXConnections(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0009-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Add(self, vObject=defaultNamedNotOptArg):
        """Add an item"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((12, 1),),vObject)

    def Insert(self, Index=defaultNamedNotOptArg, vObject=defaultNamedNotOptArg):
        """Insert an item"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 1), (12, 1)),Index, vObject)

    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), 'Item', None,Index)

    # Result is of type IXConnection
    def New(self):
        ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
        if ret is not None:
            ret = Dispatch(ret, 'New', '{001000AF-3DEF-0008-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def Remove(self, Index=defaultNamedNotOptArg):
        """Index an item"""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 1),),Index)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    # Default method for this class is 'Item'
    def __call__(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), '__call__', None,Index)

    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IXDevice(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0011-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Send(self, vCommand=defaultNamedNotOptArg, vAddress='', vDuration=0, vWait=0):
        """Send a command"""
        return self._ApplyTypes_(11, 1, (12, 32), ((12, 1), (12, 49), (12, 49), (12, 49)), 'Send', None,vCommand, vAddress, vDuration, vWait)

    def SendEvent(self, varCommandState=defaultNamedNotOptArg, varEvent=''):
        """Sets a command event (default is to stop)"""
        return self._ApplyTypes_(14, 1, (12, 32), ((12, 1), (12, 49)), 'SendEvent', None,varCommandState, varEvent)

    def SendKeyDown(self, vCommand=defaultNamedNotOptArg, vAddress=''):
        """Send a single key press"""
        return self._ApplyTypes_(12, 1, (12, 32), ((12, 1), (12, 49)), 'SendKeyDown', None,vCommand, vAddress)

    def SendKeyUp(self, vCommand=defaultNamedNotOptArg, vAddress=''):
        """Send a single key release"""
        return self._ApplyTypes_(13, 1, (12, 32), ((12, 1), (12, 49)), 'SendKeyUp', None,vCommand, vAddress)

    def SendPriority(self, vCommand=defaultNamedNotOptArg, vAddress='', vDuration=0):
        """Immediately send this command"""
        return self._ApplyTypes_(10, 1, (12, 32), ((12, 0), (12, 49), (12, 49)), 'SendPriority', None,vCommand, vAddress, vDuration)

    _prop_map_get_ = {
        "Comment": (3, 2, (12, 0), (), "Comment", None),
        "Connection": (7, 2, (12, 0), (), "Connection", None),
        # Method 'DeviceContainer' returns object of type 'IXDevice'
        "DeviceContainer": (9, 2, (9, 0), (), "DeviceContainer", '{001000AF-3DEF-0011-10B6-DC5BA692C858}'),
        "DeviceType": (8, 2, (12, 0), (), "DeviceType", None),
        "Enabled": (4, 2, (11, 0), (), "Enabled", None),
        "ID": (2, 2, (8, 0), (), "ID", None),
        "IsVisible": (5, 2, (11, 0), (), "IsVisible", None),
        "Label": (1, 2, (12, 0), (), "Label", None),
        "Name": (0, 2, (12, 0), (), "Name", None),
        # Method 'Values' returns object of type 'IXProperties'
        "Values": (6, 2, (9, 0), (), "Values", '{001000AF-3DEF-0007-10B6-DC5BA692C858}'),
    }
    _prop_map_put_ = {
        "Comment": ((3, LCID, 4, 0),()),
        "Connection": ((7, LCID, 4, 0),()),
        "DeviceContainer": ((9, LCID, 4, 0),()),
        "DeviceType": ((8, LCID, 4, 0),()),
        "Enabled": ((4, LCID, 4, 0),()),
        "IsVisible": ((5, LCID, 4, 0),()),
        "Label": ((1, LCID, 4, 0),()),
        "Name": ((0, LCID, 4, 0),()),
        "Values": ((6, LCID, 4, 0),()),
    }
    # Default property for this class is 'Name'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Name", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXDeviceType(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0013-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "IsVisibleByDefault": (2, 2, (11, 0), (), "IsVisibleByDefault", None),
        "Name": (0, 2, (12, 0), (), "Name", None),
        "Parent": (1, 2, (12, 0), (), "Parent", None),
    }
    _prop_map_put_ = {
        "Name": ((0, LCID, 4, 0),()),
        "Parent": ((1, LCID, 4, 0),()),
    }
    # Default property for this class is 'Name'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Name", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXDeviceTypeDefault(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0200-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "IsVisibleByDefault": (2, 2, (11, 0), (), "IsVisibleByDefault", None),
        "Name": (0, 2, (12, 0), (), "Name", None),
        "Parent": (1, 2, (12, 0), (), "Parent", None),
    }
    _prop_map_put_ = {
        "Name": ((0, LCID, 4, 0),()),
        "Parent": ((1, LCID, 4, 0),()),
    }
    # Default property for this class is 'Name'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Name", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXDeviceTypes(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0012-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Add(self, vObject=defaultNamedNotOptArg):
        """Add an item"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((12, 1),),vObject)

    def Insert(self, Index=defaultNamedNotOptArg, vObject=defaultNamedNotOptArg):
        """Insert an item"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 1), (12, 1)),Index, vObject)

    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), 'Item', None,Index)

    def New(self, bszType=defaultNamedNotOptArg):
        ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), ((8, 1),),bszType)
        if ret is not None:
            ret = Dispatch(ret, 'New', None, UnicodeToString=0)
        return ret

    def Remove(self, Index=defaultNamedNotOptArg):
        """Index an item"""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 1),),Index)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    # Default method for this class is 'Item'
    def __call__(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), '__call__', None,Index)

    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IXDevices(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0010-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Add(self, vObject=defaultNamedNotOptArg):
        """Add an item"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((12, 1),),vObject)

    def Insert(self, Index=defaultNamedNotOptArg, vObject=defaultNamedNotOptArg):
        """Insert an item"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 1), (12, 1)),Index, vObject)

    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), 'Item', None,Index)

    # Result is of type IXDevice
    def New(self):
        ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
        if ret is not None:
            ret = Dispatch(ret, 'New', '{001000AF-3DEF-0011-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def Remove(self, Index=defaultNamedNotOptArg):
        """Index an item"""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 1),),Index)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    # Default method for this class is 'Item'
    def __call__(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), '__call__', None,Index)

    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IXEvent(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0016-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        # Method 'Commands' returns object of type 'IXSendCommands'
        "Commands": (2, 2, (9, 0), (), "Commands", '{001000AF-3DEF-0015-10B6-DC5BA692C858}'),
        "EventType": (0, 2, (3, 0), (), "EventType", None),
        # Method 'Values' returns object of type 'IXProperties'
        "Values": (1, 2, (9, 0), (), "Values", '{001000AF-3DEF-0007-10B6-DC5BA692C858}'),
    }
    _prop_map_put_ = {
        "Commands": ((2, LCID, 4, 0),()),
        "EventType": ((0, LCID, 4, 0),()),
        "Values": ((1, LCID, 4, 0),()),
    }
    # Default property for this class is 'EventType'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (3, 0), (), "EventType", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXEvents(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0017-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Add(self, vObject=defaultNamedNotOptArg):
        """Add an item"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((12, 1),),vObject)

    def Insert(self, Index=defaultNamedNotOptArg, vObject=defaultNamedNotOptArg):
        """Insert an item"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 1), (12, 1)),Index, vObject)

    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), 'Item', None,Index)

    # Result is of type IXEvent
    def New(self):
        ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
        if ret is not None:
            ret = Dispatch(ret, 'New', '{001000AF-3DEF-0016-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def Remove(self, Index=defaultNamedNotOptArg):
        """Index an item"""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 1),),Index)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    # Default method for this class is 'Item'
    def __call__(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), '__call__', None,Index)

    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IXGroup(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0022-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

class IXGroups(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0023-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Add(self, vObject=defaultNamedNotOptArg):
        """Add an item"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((12, 1),),vObject)

    def Insert(self, Index=defaultNamedNotOptArg, vObject=defaultNamedNotOptArg):
        """Insert an item"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 1), (12, 1)),Index, vObject)

    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), 'Item', None,Index)

    # Result is of type IXObject
    def New(self):
        ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
        if ret is not None:
            ret = Dispatch(ret, 'New', '{001000AF-3DEF-001B-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def Remove(self, Index=defaultNamedNotOptArg):
        """Index an item"""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 1),),Index)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    # Default method for this class is 'Item'
    def __call__(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), '__call__', None,Index)

    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IXObject(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-001B-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Cancel(self):
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (),)

    def SendKeyUp(self):
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (),)

    # Result is of type IXEvent
    def State(self, Index=defaultNamedNotOptArg):
        ret = self._oleobj_.InvokeTypes(1, LCID, 1, (9, 0), ((12, 1),),Index)
        if ret is not None:
            ret = Dispatch(ret, 'State', '{001000AF-3DEF-0016-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    _prop_map_get_ = {
        # Method 'Command' returns object of type 'IXCommand'
        "Command": (0, 2, (9, 0), (), "Command", '{001000AF-3DEF-0019-10B6-DC5BA692C858}'),
    }
    _prop_map_put_ = {
        "Command": ((0, LCID, 4, 0),()),
    }
    # Default property for this class is 'Command'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (9, 0), (), "Command", '{001000AF-3DEF-0019-10B6-DC5BA692C858}'))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXObjects(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-001C-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Add(self, vObject=defaultNamedNotOptArg):
        """Add an item"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((12, 1),),vObject)

    def Insert(self, Index=defaultNamedNotOptArg, vObject=defaultNamedNotOptArg):
        """Insert an item"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 1), (12, 1)),Index, vObject)

    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), 'Item', None,Index)

    # Result is of type IXObject
    def New(self):
        ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
        if ret is not None:
            ret = Dispatch(ret, 'New', '{001000AF-3DEF-001B-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def Remove(self, Index=defaultNamedNotOptArg):
        """Index an item"""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 1),),Index)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    # Default method for this class is 'Item'
    def __call__(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), '__call__', None,Index)

    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IXProperties(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Add(self, vObject=defaultNamedNotOptArg):
        """Add an item"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((12, 1),),vObject)

    def Insert(self, Index=defaultNamedNotOptArg, vObject=defaultNamedNotOptArg):
        """Insert an item"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 1), (12, 1)),Index, vObject)

    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, Index=defaultNamedNotOptArg):
        """Return an item"""
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), 'Item', None,Index)

    # Result is of type IXProperty
    def New(self):
        ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
        if ret is not None:
            ret = Dispatch(ret, 'New', '{001000AF-3DEF-0006-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def Remove(self, Index=defaultNamedNotOptArg):
        """Index an item"""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 1),),Index)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    # Default method for this class is 'Item'
    def __call__(self, Index=defaultNamedNotOptArg):
        """Return an item"""
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), '__call__', None,Index)

    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IXProperty(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0006-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Name": (1, 2, (12, 0), (), "Name", None),
        "Value": (0, 2, (12, 0), (), "Value", None),
    }
    _prop_map_put_ = {
        "Name": ((1, LCID, 4, 0),()),
        "Value": ((0, LCID, 4, 0),()),
    }
    # Default property for this class is 'Value'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Value", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXRecvCommand(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0018-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Address": (3, 2, (12, 0), (), "Address", None),
        "Command": (0, 2, (12, 0), (), "Command", None),
        "CommandCode": (5, 2, (3, 0), (), "CommandCode", None),
        "CommandID": (1, 2, (3, 0), (), "CommandID", None),
        "CommandType": (4, 2, (3, 0), (), "CommandType", None),
        # Method 'Connection' returns object of type 'IXConnection'
        "Connection": (2, 2, (9, 0), (), "Connection", '{001000AF-3DEF-0008-10B6-DC5BA692C858}'),
        "KeyState": (8, 2, (3, 0), (), "KeyState", None),
        "Sequence": (7, 2, (3, 0), (), "Sequence", None),
        "TimestampHigh": (10, 2, (3, 0), (), "TimestampHigh", None),
        "TimestampLow": (9, 2, (3, 0), (), "TimestampLow", None),
        # Method 'Values' returns object of type 'IXProperties'
        "Values": (6, 2, (9, 0), (), "Values", '{001000AF-3DEF-0007-10B6-DC5BA692C858}'),
    }
    _prop_map_put_ = {
        "Address": ((3, LCID, 4, 0),()),
        "Command": ((0, LCID, 4, 0),()),
        "CommandCode": ((5, LCID, 4, 0),()),
        "CommandID": ((1, LCID, 4, 0),()),
        "CommandType": ((4, LCID, 4, 0),()),
        "Connection": ((2, LCID, 4, 0),()),
        "KeyState": ((8, LCID, 4, 0),()),
        "Sequence": ((7, LCID, 4, 0),()),
        "TimestampHigh": ((10, LCID, 4, 0),()),
        "TimestampLow": ((9, LCID, 4, 0),()),
        "Values": ((6, LCID, 4, 0),()),
    }
    # Default property for this class is 'Command'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Command", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXSendCommand(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0014-10B6-DC5BA692C858}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Address": (2, 2, (12, 0), (), "Address", None),
        "Command": (0, 2, (12, 0), (), "Command", None),
        # Method 'Connection' returns object of type 'IXConnection'
        "Connection": (1, 2, (9, 0), (), "Connection", '{001000AF-3DEF-0008-10B6-DC5BA692C858}'),
        "Duration": (4, 2, (3, 0), (), "Duration", None),
        "State": (6, 2, (3, 0), (), "State", None),
        # Method 'Values' returns object of type 'IXProperties'
        "Values": (5, 2, (9, 0), (), "Values", '{001000AF-3DEF-0007-10B6-DC5BA692C858}'),
        "Wait": (3, 2, (3, 0), (), "Wait", None),
    }
    _prop_map_put_ = {
        "Address": ((2, LCID, 4, 0),()),
        "Command": ((0, LCID, 4, 0),()),
        "Connection": ((1, LCID, 4, 0),()),
        "Duration": ((4, LCID, 4, 0),()),
        "Values": ((5, LCID, 4, 0),()),
        "Wait": ((3, LCID, 4, 0),()),
    }
    # Default property for this class is 'Command'
    def __call__(self):
        return self._ApplyTypes_(*(0, 2, (12, 0), (), "Command", None))
    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))

class IXSendCommands(DispatchBaseClass):
    CLSID = IID('{001000AF-3DEF-0015-10B6-DC5BA692C858}')
    coclass_clsid = None

    def Add(self, vObject=defaultNamedNotOptArg):
        """Add an item"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((12, 1),),vObject)

    def Insert(self, Index=defaultNamedNotOptArg, vObject=defaultNamedNotOptArg):
        """Insert an item"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((12, 1), (12, 1)),Index, vObject)

    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), 'Item', None,Index)

    # Result is of type IXSendCommand
    def New(self):
        ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
        if ret is not None:
            ret = Dispatch(ret, 'New', '{001000AF-3DEF-0014-10B6-DC5BA692C858}', UnicodeToString=0)
        return ret

    def Remove(self, Index=defaultNamedNotOptArg):
        """Index an item"""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((12, 1),),Index)

    _prop_map_get_ = {
        "Count": (1, 2, (3, 0), (), "Count", None),
    }
    _prop_map_put_ = {
    }
    # Default method for this class is 'Item'
    def __call__(self, Index=defaultNamedNotOptArg):
        return self._ApplyTypes_(0, 2, (12, 0), ((12, 1),), '__call__', None,Index)

    # str(ob) and int(ob) will use __call__
    def __unicode__(self, *args):
        try:
            return unicode(self.__call__(*args))
        except pythoncom.com_error:
            return repr(self)
    def __str__(self, *args):
        return str(self.__unicode__(*args))
    def __int__(self, *args):
        return int(self.__call__(*args))
    def __iter__(self):
        "Return a Python iterator for this object"
        ob = self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),())
        return win32com.client.util.Iterator(ob)
    def _NewEnum(self):
        "Create an enumerator from this object"
        return win32com.client.util.WrapEnum(self._oleobj_.InvokeTypes(-4,LCID,1,(13, 10),()),None)
    def __getitem__(self, index):
        "Allow this class to be accessed as a collection"
        if not self.__dict__.has_key('_enum_'):
            self.__dict__['_enum_'] = self._NewEnum()
        return self._enum_.__getitem__(index)
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "Count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class _DIX10ControlEvents:
    """_DIX10ControlEvents Interface"""
    CLSID = CLSID_Sink = IID('{001000AF-3DEF-0002-10B6-DC5BA692C858}')
    coclass_clsid = IID('{001000AF-2DEF-0001-10B6-DC5BA692C858}')
    _public_methods_ = [] # For COM Server support
    _dispid_to_func_ = {
                0 : "OnX10Command",
        }

    def __init__(self, oobj = None):
        if oobj is None:
            self._olecp = None
        else:
            import win32com.server.util
            from win32com.server.policy import EventHandlerPolicy
            cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
            cp=cpc.FindConnectionPoint(self.CLSID_Sink)
            cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
            self._olecp,self._olecp_cookie = cp,cookie
    def __del__(self):
        try:
            self.close()
        except pythoncom.com_error:
            pass
    def close(self):
        if self._olecp is not None:
            cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
            cp.Unadvise(cookie)
    def _query_interface_(self, iid):
        import win32com.server.util
        if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

    # Event Handlers
    # If you create handlers, they should have the following prototypes:
#	def OnX10Command(self, bszCommand=defaultNamedNotOptArg, eCommand=defaultNamedNotOptArg, lAddress=defaultNamedNotOptArg, EKeyState=defaultNamedNotOptArg, lSequence=defaultNamedNotOptArg, eCommandType=defaultNamedNotOptArg, varTimestamp=defaultNamedNotOptArg):
#		"""method X10Command - Called when commands have been received"""


class _DIX10InterfaceEvents:
    """_DIX10InterfaceEvents Interface"""
    CLSID = CLSID_Sink = IID('{001000AF-3DEF-0024-10B6-DC5BA692C858}')
    coclass_clsid = IID('{001000AF-2DEF-0002-10B6-DC5BA692C858}')
    _public_methods_ = [] # For COM Server support
    _dispid_to_func_ = {
                0 : "OnX10Command",
                1 : "OnX10HelpEvent",
        }

    def __init__(self, oobj = None):
        if oobj is None:
            self._olecp = None
        else:
            import win32com.server.util
            from win32com.server.policy import EventHandlerPolicy
            cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
            cp=cpc.FindConnectionPoint(self.CLSID_Sink)
            cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
            self._olecp,self._olecp_cookie = cp,cookie
    def __del__(self):
        try:
            self.close()
        except pythoncom.com_error:
            pass
    def close(self):
        if self._olecp is not None:
            cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
            cp.Unadvise(cookie)
    def _query_interface_(self, iid):
        import win32com.server.util
        if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

    # Event Handlers
    # If you create handlers, they should have the following prototypes:
#	def OnX10Command(self, bszCommand=defaultNamedNotOptArg, eCommand=defaultNamedNotOptArg, lAddress=defaultNamedNotOptArg, EKeyState=defaultNamedNotOptArg, lSequence=defaultNamedNotOptArg, eCommandType=defaultNamedNotOptArg, varTimestamp=defaultNamedNotOptArg):
#		"""method X10Command - Called when commands have been received"""
#	def OnX10HelpEvent(self, hwndDialog=defaultNamedNotOptArg, lHelpID=defaultNamedNotOptArg):
#		"""method X10HelpEvent - Called when a help button has been pressed"""


from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'X10net.X10Control.1'
class X10Control(CoClassBaseClass): # A CoClass
    # X10 Control Class
    CLSID = IID('{001000AF-2DEF-0001-10B6-DC5BA692C858}')
    coclass_sources = [
        _DIX10ControlEvents,
    ]
    default_source = _DIX10ControlEvents
    coclass_interfaces = [
        IX10Control,
    ]
    default_interface = IX10Control

# This CoClass is known by the name 'X10net.X10Interface.1'
class X10Interface(CoClassBaseClass): # A CoClass
    # X10 Interface Class
    CLSID = IID('{001000AF-2DEF-0002-10B6-DC5BA692C858}')
    coclass_sources = [
        _DIX10InterfaceEvents,
    ]
    default_source = _DIX10InterfaceEvents
    coclass_interfaces = [
        IX10Interface,
    ]
    default_interface = IX10Interface

IX10Control_vtables_dispatch_ = 1
IX10Control_vtables_ = [
    (('Interface', 'ppInterface'), 0, (0, (), [(16393, 10, None, "IID('{001000AF-3DEF-0003-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Control', 'pvarControl'), 1, (1, (), [(16396, 10, None, None)], 1, 2, 4, 0, 32, (3, 0, None, None), 0)),
    (('Command', 'varCommand', 'varParam', 'pvarRet'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None), (16396, 10, None, None)], 1, 1, 4, 0, 36, (3, 0, None, None), 0)),
    (('Show', 'fIsHideOnCloseSet'), 3, (3, (), [(11, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Hide',), 4, (4, (), [], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
    (('Close',), 5, (5, (), [], 1, 1, 4, 0, 48, (3, 0, None, None), 0)),
]

IX10DirectInterface_vtables_dispatch_ = 0
IX10DirectInterface_vtables_ = [
    (('Send', 'bszTarget', 'lHouseCode', 'lUnitCode', 'eCommand'), 0, (0, (), [(8, 1, None, None), (3, 1, None, None), (3, 1, None, None), (3, 1, None, None)], 1, 1, 4, 0, 12, (3, 0, None, None), 0)),
    (('SendKey', 'bszTarget', 'lHouseCode', 'lUnitCode', 'eCommand', 'EKeyState', 'lDuration', 'plmsQueue', 'plmsCommand', 'plIdentifier'), 1, (1, (), [(8, 1, None, None), (3, 1, None, None), (3, 1, None, None), (3, 1, None, None), (3, 1, None, None), (3, 1, None, None), (16387, 2, None, None), (16387, 2, None, None), (16387, 10, None, None)], 1, 1, 4, 0, 16, (3, 0, None, None), 0)),
    (('ReleaseKey', 'plIdentifier'), 2, (2, (), [(16387, 3, None, None)], 1, 1, 4, 0, 20, (3, 0, None, None), 0)),
    (('GetQueueDepth', 'bszTarget', 'plmsQueue'), 3, (3, (), [(8, 1, None, None), (16387, 2, None, None)], 1, 1, 4, 0, 24, (3, 0, None, None), 0)),
    (('RegisterWindow', 'hwnd', 'uMsg'), 4, (4, (), [(3, 1, None, None), (3, 1, None, None)], 1, 1, 4, 0, 28, (3, 0, None, None), 0)),
    (('DialogControl', 'hwnd', 'lDialog', 'lCommand', 'plRet'), 5, (5, (), [(3, 1, None, None), (3, 1, None, None), (3, 1, None, None), (16387, 2, None, None)], 1, 1, 4, 0, 32, (3, 0, None, None), 0)),
]

IX10Interface_vtables_dispatch_ = 1
IX10Interface_vtables_ = [
    (('Connection', 'vConnection'), 1, (1, (), [(12, 1, None, None)], 1, 4, 4, 0, 28, (3, 0, None, None), 0)),
    (('Connection', 'vConnection'), 1, (1, (), [(16396, 10, None, None)], 1, 2, 4, 0, 32, (3, 0, None, None), 0)),
    (('Device', 'vDevice'), 2, (2, (), [(12, 1, None, None)], 1, 4, 4, 0, 36, (3, 0, None, None), 0)),
    (('Device', 'vDevice'), 2, (2, (), [(16396, 10, None, None)], 1, 2, 4, 0, 40, (3, 0, None, None), 0)),
    (('SendPriority', 'vCommand', 'vScope', 'vAddress', 'vDuration', 'pvCommandState'), 3, (3, (), [(12, 1, None, None), (12, 1, None, None), (12, 49, "''", None), (12, 49, '0', None), (16396, 10, None, None)], 1, 1, 4, 0, 44, (3, 32, None, None), 0)),
    (('Send', 'vCommand', 'vScope', 'vAddress', 'vDuration', 'vWait', 'pvCommandState'), 4, (4, (), [(12, 1, None, None), (12, 1, None, None), (12, 49, "''", None), (12, 49, '0', None), (12, 49, '0', None), (16396, 10, None, None)], 1, 1, 4, 0, 48, (3, 32, None, None), 0)),
    (('SendKeyDown', 'vCommand', 'vScope', 'vAddress', 'pvCommandState'), 5, (5, (), [(12, 1, None, None), (12, 1, None, None), (12, 49, "''", None), (16396, 10, None, None)], 1, 1, 4, 0, 52, (3, 32, None, None), 0)),
    (('SendKeyUp', 'vCommand', 'vScope', 'vAddress', 'pvCommandState'), 6, (6, (), [(12, 1, None, None), (12, 1, None, None), (12, 49, "''", None), (16396, 10, None, None)], 1, 1, 4, 0, 56, (3, 32, None, None), 0)),
    (('Update',), 7, (7, (), [], 1, 1, 4, 0, 60, (3, 0, None, None), 0)),
    (('QueueDepth', 'plmsQueue'), 8, (8, (), [(16387, 10, None, None)], 1, 1, 4, 0, 64, (3, 0, None, None), 0)),
    (('QueueDepthWithCommand', 'vCommand', 'plmsQueue'), 9, (9, (), [(12, 1, None, None), (16387, 10, None, None)], 1, 1, 4, 0, 68, (3, 0, None, None), 0)),
    (('CancelAllCommands',), 10, (10, (), [], 1, 1, 4, 0, 72, (3, 0, None, None), 0)),
    (('StartRecord',), 11, (11, (), [], 1, 1, 4, 0, 76, (3, 0, None, None), 0)),
    (('StopRecord', 'vCommand', 'ppCommand'), 12, (12, (), [(12, 1, None, None), (16393, 10, None, "IID('{001000AF-3DEF-0019-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 80, (3, 0, None, None), 0)),
    (('Connections', 'ppConnections'), 13, (13, (), [(16393, 10, None, "IID('{001000AF-3DEF-0009-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 84, (3, 0, None, None), 0)),
    (('Devices', 'ppDevices'), 14, (14, (), [(16393, 10, None, "IID('{001000AF-3DEF-0010-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 88, (3, 0, None, None), 0)),
    (('Commands', 'ppCommands'), 15, (15, (), [(16393, 10, None, "IID('{001000AF-3DEF-001A-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 92, (3, 0, None, None), 0)),
    (('Objects', 'ppObjects'), 16, (16, (), [(16393, 10, None, "IID('{001000AF-3DEF-001C-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 96, (3, 0, None, None), 0)),
    (('DeviceTypes', 'ppDeviceTypes'), 17, (17, (), [(16393, 10, None, "IID('{001000AF-3DEF-0012-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 100, (3, 0, None, None), 0)),
    (('ConnectionTypes', 'ppConnectionTypes'), 18, (18, (), [(16393, 10, None, "IID('{001000AF-3DEF-000A-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 104, (3, 0, None, None), 0)),
    (('SuspendCommands',), 19, (19, (), [], 1, 1, 4, 0, 108, (3, 0, None, None), 0)),
    (('Breakpoints', 'ppBreakpoints'), 20, (20, (), [(16393, 0, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 112, (3, 0, None, None), 0)),
    (('ResumeCommands',), 21, (21, (), [], 1, 1, 4, 0, 116, (3, 0, None, None), 0)),
    (('SingleCommandOver',), 22, (22, (), [], 1, 1, 4, 0, 120, (3, 0, None, None), 0)),
    (('SingleCommandInto',), 23, (23, (), [], 1, 1, 4, 0, 124, (3, 0, None, None), 0)),
    (('GetNextCommand',), 24, (24, (), [], 1, 1, 4, 0, 128, (3, 0, None, None), 0)),
    (('CheckCommand',), 25, (25, (), [], 1, 1, 4, 0, 132, (3, 0, None, None), 0)),
    (('LastRecv', 'lHistoryIndex', 'ppCommand'), 26, (26, (), [(3, 49, '0', None), (16393, 10, None, "IID('{001000AF-3DEF-0018-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 136, (3, 0, None, None), 0)),
    (('LastSend', 'lHistoryIndex', 'ppCommand'), 27, (27, (), [(3, 49, '0', None), (16393, 10, None, "IID('{001000AF-3DEF-0014-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 140, (3, 0, None, None), 0)),
    (('RecvHistoryLength', 'plHistory'), 28, (28, (), [(3, 1, None, None)], 1, 4, 4, 0, 144, (3, 0, None, None), 0)),
    (('RecvHistoryLength', 'plHistory'), 28, (28, (), [(16387, 10, None, None)], 1, 2, 4, 0, 148, (3, 0, None, None), 0)),
    (('SendHistoryLength', 'plHistory'), 29, (29, (), [(3, 1, None, None)], 1, 4, 4, 0, 152, (3, 0, None, None), 0)),
    (('SendHistoryLength', 'plHistory'), 29, (29, (), [(16387, 10, None, None)], 1, 2, 4, 0, 156, (3, 0, None, None), 0)),
    (('CreateControl', 'varControl', 'varSkin', 'ppControl'), 30, (30, (), [(12, 1, None, None), (12, 1, None, None), (16393, 10, None, "IID('{001000AF-3DEF-0001-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 160, (3, 0, None, None), 0)),
    (('Version', 'vVersion'), 31, (31, (), [(16396, 10, None, None)], 1, 2, 4, 0, 164, (3, 0, None, None), 0)),
    (('HouseCodeEventMask', 'plHouseCodeEventMask'), 32, (32, (), [(3, 1, None, None)], 1, 4, 4, 0, 168, (3, 0, None, None), 0)),
    (('HouseCodeEventMask', 'plHouseCodeEventMask'), 32, (32, (), [(16387, 10, None, None)], 1, 2, 4, 0, 172, (3, 0, None, None), 0)),
    (('UnitCodeEventMask', 'plUnitCodeEventMask'), 33, (33, (), [(3, 1, None, None)], 1, 4, 4, 0, 176, (3, 0, None, None), 0)),
    (('UnitCodeEventMask', 'plUnitCodeEventMask'), 33, (33, (), [(16387, 10, None, None)], 1, 2, 4, 0, 180, (3, 0, None, None), 0)),
    (('GetAdaptersPresent', 'lAdapterType', 'plAdaptersPresent'), 34, (34, (), [(3, 0, None, None), (16387, 10, None, None)], 1, 1, 4, 0, 184, (3, 0, None, None), 0)),
]

IXCollection_vtables_dispatch_ = 1
IXCollection_vtables_ = [
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 32, (3, 0, None, None), 1)),
    (('Insert', 'Index', 'vObject'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None)], 1, 1, 4, 0, 36, (3, 0, None, None), 0)),
    (('Remove', 'Index'), 3, (3, (), [(12, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Add', 'vObject'), 4, (4, (), [(12, 1, None, None)], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
]

IXCommand_vtables_dispatch_ = 1
IXCommand_vtables_ = [
    (('Name', 'vName'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Name', 'vName'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
    (('Label', 'vLabel'), 1, (1, (), [(16396, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Label', 'vLabel'), 1, (1, (), [(12, 1, None, None)], 1, 4, 4, 0, 40, (3, 0, None, None), 0)),
    (('Comment', 'vComment'), 2, (2, (), [(16396, 10, None, None)], 1, 2, 4, 0, 44, (3, 0, None, None), 0)),
    (('Comment', 'vComment'), 2, (2, (), [(12, 1, None, None)], 1, 4, 4, 0, 48, (3, 0, None, None), 0)),
    (('Enabled', 'bEnabled'), 3, (3, (), [(16387, 10, None, None)], 1, 2, 4, 0, 52, (3, 0, None, None), 0)),
    (('Enabled', 'bEnabled'), 3, (3, (), [(3, 1, None, None)], 1, 4, 4, 0, 56, (3, 0, None, None), 0)),
    (('Events', 'ppEvents'), 4, (4, (), [(16393, 10, None, "IID('{001000AF-3DEF-0017-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 60, (3, 0, None, None), 0)),
    (('Events', 'ppEvents'), 4, (4, (), [(9, 1, None, "IID('{001000AF-3DEF-0017-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 64, (3, 0, None, None), 0)),
    (('Connection', 'ppConnection'), 5, (5, (), [(16393, 10, None, "IID('{001000AF-3DEF-0008-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 68, (3, 0, None, None), 0)),
    (('Connection', 'ppConnection'), 5, (5, (), [(9, 1, None, "IID('{001000AF-3DEF-0008-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 72, (3, 0, None, None), 0)),
    (('Address', 'pvAddress'), 6, (6, (), [(16396, 10, None, None)], 1, 2, 4, 0, 76, (3, 0, None, None), 0)),
    (('Address', 'pvAddress'), 6, (6, (), [(12, 1, None, None)], 1, 4, 4, 0, 80, (3, 0, None, None), 0)),
    (('ScopeName', 'pvScopeName'), 7, (7, (), [(16396, 10, None, None)], 1, 2, 4, 0, 84, (3, 0, None, None), 0)),
    (('ScopeName', 'pvScopeName'), 7, (7, (), [(12, 1, None, None)], 1, 4, 4, 0, 88, (3, 0, None, None), 0)),
    (('Scope', 'eScope'), 8, (8, (), [(16387, 10, None, None)], 1, 2, 4, 0, 92, (3, 0, None, None), 0)),
    (('Scope', 'eScope'), 8, (8, (), [(3, 1, None, None)], 1, 4, 4, 0, 96, (3, 0, None, None), 0)),
    (('Owner', 'ppOwner'), 9, (9, (), [(16393, 10, None, "IID('{001000AF-3DEF-0019-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 100, (3, 0, None, None), 0)),
    (('Owner', 'ppOwner'), 9, (9, (), [(9, 1, None, "IID('{001000AF-3DEF-0019-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 104, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 10, (10, (), [(16393, 10, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 108, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 10, (10, (), [(9, 1, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 112, (3, 0, None, None), 0)),
    (('ID', 'ppszID'), 11, (11, (), [(16392, 10, None, None)], 1, 2, 4, 0, 116, (3, 0, None, None), 0)),
]

IXCommands_vtables_dispatch_ = 1
IXCommands_vtables_ = [
    (('Item', 'Index', 'pvarObject'), 0, (0, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 32, (3, 0, None, None), 1)),
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Insert', 'Index', 'vObject'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Remove', 'Index'), 3, (3, (), [(12, 1, None, None)], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
    (('Add', 'vObject'), 4, (4, (), [(12, 1, None, None)], 1, 1, 4, 0, 48, (3, 0, None, None), 0)),
    (('New', 'ppObject'), 5, (5, (), [(16393, 10, None, "IID('{001000AF-3DEF-0019-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 52, (3, 0, None, None), 0)),
    (('FilterItem', 'Index', 'pvarObject'), 6, (6, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 1, 4, 0, 56, (3, 0, None, None), 0)),
    (('GetFilterItemCount', 'plCount'), 7, (7, (), [(16387, 10, None, None)], 1, 1, 4, 0, 60, (3, 0, None, None), 0)),
    (('SetFilter', 'eScope', 'pszScope', 'fIsVisibleOnly', 'fIsEnabledOnly'), 8, (8, (), [(3, 1, None, None), (8, 1, None, None), (11, 1, None, None), (11, 1, None, None)], 1, 1, 4, 0, 64, (3, 0, None, None), 0)),
]

IXConnection_vtables_dispatch_ = 1
IXConnection_vtables_ = [
    (('Name', 'varName'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Name', 'varName'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 1, (1, (), [(16393, 10, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 1, (1, (), [(9, 1, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 40, (3, 0, None, None), 0)),
    (('Comment', 'varComment'), 2, (2, (), [(16396, 10, None, None)], 1, 2, 4, 0, 44, (3, 0, None, None), 0)),
    (('Comment', 'varComment'), 2, (2, (), [(12, 1, None, None)], 1, 4, 4, 0, 48, (3, 0, None, None), 0)),
    (('Connect',), 3, (3, (), [], 1, 1, 4, 0, 52, (3, 0, None, None), 0)),
    (('Disconnect',), 4, (4, (), [], 1, 1, 4, 0, 56, (3, 0, None, None), 0)),
    (('ConnectStatus', 'pbszConnectStatus'), 5, (5, (), [(16392, 10, None, None)], 1, 1, 4, 0, 60, (3, 0, None, None), 0)),
    (('ConnectTime', 'pmsConnected'), 6, (6, (), [(16389, 10, None, None)], 1, 1, 4, 0, 64, (3, 0, None, None), 0)),
    (('IsConnected', 'bConnected'), 7, (7, (), [(16387, 10, None, None)], 1, 1, 4, 0, 68, (3, 0, None, None), 0)),
    (('Extended', 'pvarObject'), 8, (8, (), [(16396, 10, None, None)], 1, 1, 4, 0, 72, (3, 0, None, None), 0)),
    (('QueueDepth', 'plmsQueue'), 9, (9, (), [(16387, 10, None, None)], 1, 1, 4, 0, 76, (3, 0, None, None), 0)),
    (('CancelAllCommands',), 10, (10, (), [], 1, 1, 4, 0, 80, (3, 0, None, None), 0)),
    (('SendPriority', 'varCommand', 'varAddress', 'varDuration', 'pvarCommandState'), 11, (11, (), [(12, 0, None, None), (12, 49, "''", None), (12, 49, '0', None), (16396, 10, None, None)], 1, 1, 4, 0, 84, (3, 32, None, None), 0)),
    (('Send', 'varCommand', 'varAddress', 'varDuration', 'varWait', 'pvarCommandState'), 12, (12, (), [(12, 1, None, None), (12, 49, "''", None), (12, 49, '0', None), (12, 49, '0', None), (16396, 10, None, None)], 1, 1, 4, 0, 88, (3, 32, None, None), 0)),
    (('SendKeyDown', 'varCommand', 'varAddress', 'pvarCommandState'), 13, (13, (), [(12, 1, None, None), (12, 49, "''", None), (16396, 10, None, None)], 1, 1, 4, 0, 92, (3, 32, None, None), 0)),
    (('SendKeyUp', 'varCommand', 'varAddress', 'pvarCommandState'), 14, (14, (), [(12, 1, None, None), (12, 49, "''", None), (16396, 10, None, None)], 1, 1, 4, 0, 96, (3, 32, None, None), 0)),
]

IXConnectionType_vtables_dispatch_ = 1
IXConnectionType_vtables_ = [
    (('Name', 'vName'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Name', 'vName'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
]

IXConnectionTypeLocalRecv_vtables_dispatch_ = 1
IXConnectionTypeLocalRecv_vtables_ = [
    (('Name', 'vName'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Name', 'vName'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
]

IXConnectionTypeLocalSend_vtables_dispatch_ = 1
IXConnectionTypeLocalSend_vtables_ = [
    (('Name', 'vName'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Name', 'vName'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
]

IXConnectionTypeNetClient_vtables_dispatch_ = 1
IXConnectionTypeNetClient_vtables_ = [
    (('Name', 'vName'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Name', 'vName'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
]

IXConnectionTypeNetServer_vtables_dispatch_ = 1
IXConnectionTypeNetServer_vtables_ = [
    (('Name', 'vName'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Name', 'vName'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
]

IXConnectionTypes_vtables_dispatch_ = 1
IXConnectionTypes_vtables_ = [
    (('Item', 'Index', 'pvarObject'), 0, (0, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 32, (3, 0, None, None), 1)),
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
]

IXConnections_vtables_dispatch_ = 1
IXConnections_vtables_ = [
    (('Item', 'Index', 'pvarObject'), 0, (0, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 32, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 36, (3, 0, None, None), 1)),
    (('Insert', 'Index', 'vObject'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Remove', 'Index'), 3, (3, (), [(12, 1, None, None)], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
    (('Add', 'vObject'), 4, (4, (), [(12, 1, None, None)], 1, 1, 4, 0, 48, (3, 0, None, None), 0)),
    (('New', 'ppObject'), 5, (5, (), [(16393, 10, None, "IID('{001000AF-3DEF-0008-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 52, (3, 0, None, None), 0)),
]

IXDevice_vtables_dispatch_ = 1
IXDevice_vtables_ = [
    (('Name', 'vName'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Name', 'vName'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
    (('Label', 'vLabel'), 1, (1, (), [(16396, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Label', 'vLabel'), 1, (1, (), [(12, 1, None, None)], 1, 4, 4, 0, 40, (3, 0, None, None), 0)),
    (('ID', 'ppszID'), 2, (2, (), [(16392, 10, None, None)], 1, 2, 4, 0, 44, (3, 0, None, None), 0)),
    (('Comment', 'vComment'), 3, (3, (), [(16396, 10, None, None)], 1, 2, 4, 0, 48, (3, 0, None, None), 0)),
    (('Comment', 'vComment'), 3, (3, (), [(12, 1, None, None)], 1, 4, 4, 0, 52, (3, 0, None, None), 0)),
    (('Enabled', 'bEnabled'), 4, (4, (), [(16395, 10, None, None)], 1, 2, 4, 0, 56, (3, 0, None, None), 0)),
    (('Enabled', 'bEnabled'), 4, (4, (), [(11, 1, None, None)], 1, 4, 4, 0, 60, (3, 0, None, None), 0)),
    (('IsVisible', 'pbVisible'), 5, (5, (), [(16395, 10, None, None)], 1, 2, 4, 0, 64, (3, 0, None, None), 0)),
    (('IsVisible', 'pbVisible'), 5, (5, (), [(11, 1, None, None)], 1, 4, 4, 0, 68, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 6, (6, (), [(16393, 10, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 72, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 6, (6, (), [(9, 1, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 76, (3, 0, None, None), 0)),
    (('Connection', 'pvarConnection'), 7, (7, (), [(16396, 10, None, None)], 1, 2, 4, 0, 80, (3, 0, None, None), 0)),
    (('Connection', 'pvarConnection'), 7, (7, (), [(12, 1, None, None)], 1, 4, 4, 0, 84, (3, 0, None, None), 0)),
    (('DeviceType', 'pvarDeviceType'), 8, (8, (), [(16396, 10, None, None)], 1, 2, 4, 0, 88, (3, 0, None, None), 0)),
    (('DeviceType', 'pvarDeviceType'), 8, (8, (), [(12, 1, None, None)], 1, 4, 4, 0, 92, (3, 0, None, None), 0)),
    (('DeviceContainer', 'ppDeviceContainer'), 9, (9, (), [(16393, 10, None, "IID('{001000AF-3DEF-0011-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 96, (3, 0, None, None), 0)),
    (('DeviceContainer', 'ppDeviceContainer'), 9, (9, (), [(9, 1, None, "IID('{001000AF-3DEF-0011-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 100, (3, 0, None, None), 0)),
    (('SendPriority', 'vCommand', 'vAddress', 'vDuration', 'pvCommandState'), 10, (10, (), [(12, 0, None, None), (12, 49, "''", None), (12, 49, '0', None), (16396, 10, None, None)], 1, 1, 4, 0, 104, (3, 32, None, None), 0)),
    (('Send', 'vCommand', 'vAddress', 'vDuration', 'vWait', 'pvCommandState'), 11, (11, (), [(12, 1, None, None), (12, 49, "''", None), (12, 49, '0', None), (12, 49, '0', None), (16396, 10, None, None)], 1, 1, 4, 0, 108, (3, 32, None, None), 0)),
    (('SendKeyDown', 'vCommand', 'vAddress', 'pvCommandState'), 12, (12, (), [(12, 1, None, None), (12, 49, "''", None), (16396, 10, None, None)], 1, 1, 4, 0, 112, (3, 32, None, None), 0)),
    (('SendKeyUp', 'vCommand', 'vAddress', 'pvCommandState'), 13, (13, (), [(12, 1, None, None), (12, 49, "''", None), (16396, 10, None, None)], 1, 1, 4, 0, 116, (3, 32, None, None), 0)),
    (('SendEvent', 'varCommandState', 'varEvent', 'pvarCommandState'), 14, (14, (), [(12, 1, None, None), (12, 49, "''", None), (16396, 10, None, None)], 1, 1, 4, 0, 120, (3, 32, None, None), 0)),
]

IXDeviceType_vtables_dispatch_ = 1
IXDeviceType_vtables_ = [
    (('Name', 'vName'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Name', 'vName'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
    (('Parent', 'vParent'), 1, (1, (), [(16396, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Parent', 'vParent'), 1, (1, (), [(12, 1, None, None)], 1, 4, 4, 0, 40, (3, 0, None, None), 0)),
    (('IsVisibleByDefault', 'pbVisible'), 2, (2, (), [(16395, 10, None, None)], 1, 2, 4, 0, 44, (3, 0, None, None), 0)),
]

IXDeviceTypeDefault_vtables_dispatch_ = 1
IXDeviceTypeDefault_vtables_ = [
    (('Name', 'vName'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Name', 'vName'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
    (('Parent', 'vParent'), 1, (1, (), [(16396, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Parent', 'vParent'), 1, (1, (), [(12, 1, None, None)], 1, 4, 4, 0, 40, (3, 0, None, None), 0)),
    (('IsVisibleByDefault', 'pbVisible'), 2, (2, (), [(16395, 10, None, None)], 1, 2, 4, 0, 44, (3, 0, None, None), 0)),
]

IXDeviceTypes_vtables_dispatch_ = 1
IXDeviceTypes_vtables_ = [
    (('Item', 'Index', 'pvarObject'), 0, (0, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 32, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 36, (3, 0, None, None), 1)),
    (('Insert', 'Index', 'vObject'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Remove', 'Index'), 3, (3, (), [(12, 1, None, None)], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
    (('Add', 'vObject'), 4, (4, (), [(12, 1, None, None)], 1, 1, 4, 0, 48, (3, 0, None, None), 0)),
    (('New', 'bszType', 'ppObject'), 5, (5, (), [(8, 1, None, None), (16393, 10, None, None)], 1, 1, 4, 0, 52, (3, 0, None, None), 0)),
]

IXDevices_vtables_dispatch_ = 1
IXDevices_vtables_ = [
    (('Item', 'Index', 'pvarObject'), 0, (0, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 32, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 36, (3, 0, None, None), 1)),
    (('Insert', 'Index', 'vObject'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Remove', 'Index'), 3, (3, (), [(12, 1, None, None)], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
    (('Add', 'vObject'), 4, (4, (), [(12, 1, None, None)], 1, 1, 4, 0, 48, (3, 0, None, None), 0)),
    (('New', 'ppObject'), 5, (5, (), [(16393, 10, None, "IID('{001000AF-3DEF-0011-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 52, (3, 0, None, None), 0)),
]

IXEvent_vtables_dispatch_ = 1
IXEvent_vtables_ = [
    (('EventType', 'peType'), 0, (0, (), [(16387, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('EventType', 'peType'), 0, (0, (), [(3, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 1, (1, (), [(16393, 10, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 1, (1, (), [(9, 1, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 40, (3, 0, None, None), 0)),
    (('Commands', 'ppValues'), 2, (2, (), [(16393, 10, None, "IID('{001000AF-3DEF-0015-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 44, (3, 0, None, None), 0)),
    (('Commands', 'ppValues'), 2, (2, (), [(9, 1, None, "IID('{001000AF-3DEF-0015-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 48, (3, 0, None, None), 0)),
]

IXEvents_vtables_dispatch_ = 1
IXEvents_vtables_ = [
    (('Item', 'Index', 'pvarObject'), 0, (0, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 32, (3, 0, None, None), 1)),
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Insert', 'Index', 'vObject'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Remove', 'Index'), 3, (3, (), [(12, 1, None, None)], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
    (('Add', 'vObject'), 4, (4, (), [(12, 1, None, None)], 1, 1, 4, 0, 48, (3, 0, None, None), 0)),
    (('New', 'ppObject'), 5, (5, (), [(16393, 10, None, "IID('{001000AF-3DEF-0016-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 52, (3, 0, None, None), 0)),
]

IXGroup_vtables_dispatch_ = 1
IXGroup_vtables_ = [
]

IXGroups_vtables_dispatch_ = 1
IXGroups_vtables_ = [
    (('Item', 'Index', 'pvarObject'), 0, (0, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 32, (3, 0, None, None), 1)),
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Insert', 'Index', 'vObject'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Remove', 'Index'), 3, (3, (), [(12, 1, None, None)], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
    (('Add', 'vObject'), 4, (4, (), [(12, 1, None, None)], 1, 1, 4, 0, 48, (3, 0, None, None), 0)),
    (('New', 'ppObject'), 5, (5, (), [(16393, 10, None, "IID('{001000AF-3DEF-001B-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 52, (3, 0, None, None), 0)),
]

IXObject_vtables_dispatch_ = 1
IXObject_vtables_ = [
    (('Command', 'ppCommand'), 0, (0, (), [(16393, 10, None, "IID('{001000AF-3DEF-0019-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Command', 'ppCommand'), 0, (0, (), [(9, 1, None, "IID('{001000AF-3DEF-0019-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
    (('State', 'Index', 'ppObject'), 1, (1, (), [(12, 1, None, None), (16393, 10, None, "IID('{001000AF-3DEF-0016-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 36, (3, 0, None, None), 0)),
    (('Cancel',), 2, (2, (), [], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('SendKeyUp',), 3, (3, (), [], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
]

IXObjects_vtables_dispatch_ = 1
IXObjects_vtables_ = [
    (('Item', 'Index', 'pvarObject'), 0, (0, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 32, (3, 0, None, None), 1)),
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Insert', 'Index', 'vObject'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Remove', 'Index'), 3, (3, (), [(12, 1, None, None)], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
    (('Add', 'vObject'), 4, (4, (), [(12, 1, None, None)], 1, 1, 4, 0, 48, (3, 0, None, None), 0)),
    (('New', 'ppObject'), 5, (5, (), [(16393, 10, None, "IID('{001000AF-3DEF-001B-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 52, (3, 0, None, None), 0)),
]

IXProperties_vtables_dispatch_ = 1
IXProperties_vtables_ = [
    (('Item', 'Index', 'pvarObject'), 0, (0, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 32, (3, 0, None, None), 1)),
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Insert', 'Index', 'vObject'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Remove', 'Index'), 3, (3, (), [(12, 1, None, None)], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
    (('Add', 'vObject'), 4, (4, (), [(12, 1, None, None)], 1, 1, 4, 0, 48, (3, 0, None, None), 0)),
    (('New', 'ppObject'), 5, (5, (), [(16393, 10, None, "IID('{001000AF-3DEF-0006-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 52, (3, 0, None, None), 0)),
]

IXProperty_vtables_dispatch_ = 1
IXProperty_vtables_ = [
    (('Value', 'vValue'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Value', 'vValue'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
    (('Name', 'vName'), 1, (1, (), [(16396, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Name', 'vName'), 1, (1, (), [(12, 1, None, None)], 1, 4, 4, 0, 40, (3, 0, None, None), 0)),
]

IXRecvCommand_vtables_dispatch_ = 1
IXRecvCommand_vtables_ = [
    (('Command', 'vCommand'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Command', 'vCommand'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
    (('CommandID', 'plCommand'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('CommandID', 'plCommand'), 1, (1, (), [(3, 1, None, None)], 1, 4, 4, 0, 40, (3, 0, None, None), 0)),
    (('Connection', 'ppConnection'), 2, (2, (), [(16393, 10, None, "IID('{001000AF-3DEF-0008-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 44, (3, 0, None, None), 0)),
    (('Connection', 'ppConnection'), 2, (2, (), [(9, 1, None, "IID('{001000AF-3DEF-0008-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 48, (3, 0, None, None), 0)),
    (('Address', 'pvAddress'), 3, (3, (), [(16396, 10, None, None)], 1, 2, 4, 0, 52, (3, 0, None, None), 0)),
    (('Address', 'pvAddress'), 3, (3, (), [(12, 1, None, None)], 1, 4, 4, 0, 56, (3, 0, None, None), 0)),
    (('CommandType', 'peCommandType'), 4, (4, (), [(16387, 10, None, None)], 1, 2, 4, 0, 60, (3, 0, None, None), 0)),
    (('CommandType', 'peCommandType'), 4, (4, (), [(3, 1, None, None)], 1, 4, 4, 0, 64, (3, 0, None, None), 0)),
    (('CommandCode', 'peCommandCode'), 5, (5, (), [(16387, 10, None, None)], 1, 2, 4, 0, 68, (3, 0, None, None), 0)),
    (('CommandCode', 'peCommandCode'), 5, (5, (), [(3, 1, None, None)], 1, 4, 4, 0, 72, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 6, (6, (), [(16393, 10, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 76, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 6, (6, (), [(9, 1, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 80, (3, 0, None, None), 0)),
    (('Sequence', 'plSequence'), 7, (7, (), [(16387, 10, None, None)], 1, 2, 4, 0, 84, (3, 0, None, None), 0)),
    (('Sequence', 'plSequence'), 7, (7, (), [(3, 1, None, None)], 1, 4, 4, 0, 88, (3, 0, None, None), 0)),
    (('KeyState', 'peKeyState'), 8, (8, (), [(16387, 10, None, None)], 1, 2, 4, 0, 92, (3, 0, None, None), 0)),
    (('KeyState', 'peKeyState'), 8, (8, (), [(3, 1, None, None)], 1, 4, 4, 0, 96, (3, 0, None, None), 0)),
    (('TimestampLow', 'plTimestampLow'), 9, (9, (), [(16387, 10, None, None)], 1, 2, 4, 0, 100, (3, 0, None, None), 0)),
    (('TimestampLow', 'plTimestampLow'), 9, (9, (), [(3, 1, None, None)], 1, 4, 4, 0, 104, (3, 0, None, None), 0)),
    (('TimestampHigh', 'plTimestampHigh'), 10, (10, (), [(16387, 10, None, None)], 1, 2, 4, 0, 108, (3, 0, None, None), 0)),
    (('TimestampHigh', 'plTimestampHigh'), 10, (10, (), [(3, 1, None, None)], 1, 4, 4, 0, 112, (3, 0, None, None), 0)),
]

IXSendCommand_vtables_dispatch_ = 1
IXSendCommand_vtables_ = [
    (('Command', 'vCommand'), 0, (0, (), [(16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('Command', 'vCommand'), 0, (0, (), [(12, 1, None, None)], 1, 4, 4, 0, 32, (3, 0, None, None), 0)),
    (('Connection', 'ppConnection'), 1, (1, (), [(16393, 10, None, "IID('{001000AF-3DEF-0008-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Connection', 'ppConnection'), 1, (1, (), [(9, 1, None, "IID('{001000AF-3DEF-0008-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 40, (3, 0, None, None), 0)),
    (('Address', 'pvAddress'), 2, (2, (), [(16396, 10, None, None)], 1, 2, 4, 0, 44, (3, 0, None, None), 0)),
    (('Address', 'pvAddress'), 2, (2, (), [(12, 1, None, None)], 1, 4, 4, 0, 48, (3, 0, None, None), 0)),
    (('Wait', 'plWait'), 3, (3, (), [(16387, 10, None, None)], 1, 2, 4, 0, 52, (3, 0, None, None), 0)),
    (('Wait', 'plWait'), 3, (3, (), [(3, 1, None, None)], 1, 4, 4, 0, 56, (3, 0, None, None), 0)),
    (('Duration', 'plDuration'), 4, (4, (), [(16387, 10, None, None)], 1, 2, 4, 0, 60, (3, 0, None, None), 0)),
    (('Duration', 'plDuration'), 4, (4, (), [(3, 1, None, None)], 1, 4, 4, 0, 64, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 5, (5, (), [(16393, 10, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 2, 4, 0, 68, (3, 0, None, None), 0)),
    (('Values', 'ppValues'), 5, (5, (), [(9, 1, None, "IID('{001000AF-3DEF-0007-10B6-DC5BA692C858}')")], 1, 4, 4, 0, 72, (3, 0, None, None), 0)),
    (('State', 'peState'), 6, (6, (), [(16387, 10, None, None)], 1, 2, 4, 0, 76, (3, 0, None, None), 0)),
]

IXSendCommands_vtables_dispatch_ = 1
IXSendCommands_vtables_ = [
    (('Item', 'Index', 'pvarObject'), 0, (0, (), [(12, 1, None, None), (16396, 10, None, None)], 1, 2, 4, 0, 28, (3, 0, None, None), 0)),
    (('_NewEnum', 'ppObject'), -4, (-4, (), [(16397, 10, None, None)], 1, 1, 4, 0, 32, (3, 0, None, None), 1)),
    (('Count', 'c'), 1, (1, (), [(16387, 10, None, None)], 1, 2, 4, 0, 36, (3, 0, None, None), 0)),
    (('Insert', 'Index', 'vObject'), 2, (2, (), [(12, 1, None, None), (12, 1, None, None)], 1, 1, 4, 0, 40, (3, 0, None, None), 0)),
    (('Remove', 'Index'), 3, (3, (), [(12, 1, None, None)], 1, 1, 4, 0, 44, (3, 0, None, None), 0)),
    (('Add', 'vObject'), 4, (4, (), [(12, 1, None, None)], 1, 1, 4, 0, 48, (3, 0, None, None), 0)),
    (('New', 'ppObject'), 5, (5, (), [(16393, 10, None, "IID('{001000AF-3DEF-0014-10B6-DC5BA692C858}')")], 1, 1, 4, 0, 52, (3, 0, None, None), 0)),
]

_IX10InterfaceEvents_vtables_dispatch_ = 0
_IX10InterfaceEvents_vtables_ = [
    (('X10Command', 'bszCommand', 'eCommand', 'lAddress', 'EKeyState', 'lSequence', 'eCommandType', 'varTimestamp'), 0, (0, (), [(8, 0, None, None), (3, 0, None, None), (3, 0, None, None), (3, 0, None, None), (3, 0, None, None), (3, 0, None, None), (12, 0, None, None)], 1, 1, 4, 0, 12, (3, 0, None, None), 0)),
    (('X10HelpEvent', 'hwndDialog', 'lHelpID'), 1, (1, (), [(3, 0, None, None), (3, 0, None, None)], 1, 1, 4, 0, 16, (3, 0, None, None), 0)),
]

RecordMap = {
}

CLSIDToClassMap = {
    '{001000AF-3DEF-000D-10B6-DC5BA692C858}' : IXConnectionTypeLocalRecv,
    '{001000AF-3DEF-000F-10B6-DC5BA692C858}' : IXConnectionTypeNetServer,
    '{001000AF-3DEF-0016-10B6-DC5BA692C858}' : IXEvent,
    '{001000AF-3DEF-0011-10B6-DC5BA692C858}' : IXDevice,
    '{001000AF-3DEF-0013-10B6-DC5BA692C858}' : IXDeviceType,
    '{001000AF-2DEF-0001-10B6-DC5BA692C858}' : X10Control,
    '{001000AF-3DEF-001A-10B6-DC5BA692C858}' : IXCommands,
    '{001000AF-3DEF-001B-10B6-DC5BA692C858}' : IXObject,
    '{001000AF-3DEF-0017-10B6-DC5BA692C858}' : IXEvents,
    '{001000AF-2DEF-0002-10B6-DC5BA692C858}' : X10Interface,
    '{001000AF-3DEF-0019-10B6-DC5BA692C858}' : IXCommand,
    '{001000AF-3DEF-0200-10B6-DC5BA692C858}' : IXDeviceTypeDefault,
    '{001000AF-3DEF-0002-10B6-DC5BA692C858}' : _DIX10ControlEvents,
    '{001000AF-3DEF-0023-10B6-DC5BA692C858}' : IXGroups,
    '{001000AF-3DEF-0006-10B6-DC5BA692C858}' : IXProperty,
    '{001000AF-3DEF-0008-10B6-DC5BA692C858}' : IXConnection,
    '{001000AF-3DEF-000A-10B6-DC5BA692C858}' : IXConnectionTypes,
    '{001000AF-3DEF-0015-10B6-DC5BA692C858}' : IXSendCommands,
    '{001000AF-3DEF-000C-10B6-DC5BA692C858}' : IXConnectionTypeLocalSend,
    '{001000AF-3DEF-000E-10B6-DC5BA692C858}' : IXConnectionTypeNetClient,
    '{001000AF-3DEF-0010-10B6-DC5BA692C858}' : IXDevices,
    '{001000AF-3DEF-0012-10B6-DC5BA692C858}' : IXDeviceTypes,
    '{001000AF-3DEF-0009-10B6-DC5BA692C858}' : IXConnections,
    '{001000AF-3DEF-0014-10B6-DC5BA692C858}' : IXSendCommand,
    '{001000AF-3DEF-0018-10B6-DC5BA692C858}' : IXRecvCommand,
    '{001000AF-3DEF-001C-10B6-DC5BA692C858}' : IXObjects,
    '{001000AF-3DEF-0001-10B6-DC5BA692C858}' : IX10Control,
    '{001000AF-3DEF-0022-10B6-DC5BA692C858}' : IXGroup,
    '{001000AF-3DEF-0003-10B6-DC5BA692C858}' : IX10Interface,
    '{001000AF-3DEF-0024-10B6-DC5BA692C858}' : _DIX10InterfaceEvents,
    '{001000AF-3DEF-0005-10B6-DC5BA692C858}' : IXCollection,
    '{001000AF-3DEF-000B-10B6-DC5BA692C858}' : IXConnectionType,
    '{001000AF-3DEF-0007-10B6-DC5BA692C858}' : IXProperties,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
    '{001000AF-3DEF-000D-10B6-DC5BA692C858}' : 'IXConnectionTypeLocalRecv',
    '{001000AF-3DEF-000F-10B6-DC5BA692C858}' : 'IXConnectionTypeNetServer',
    '{001000AF-3DEF-0016-10B6-DC5BA692C858}' : 'IXEvent',
    '{001000AF-3DEF-0011-10B6-DC5BA692C858}' : 'IXDevice',
    '{001000AF-3DEF-0013-10B6-DC5BA692C858}' : 'IXDeviceType',
    '{001000AF-3DEF-001A-10B6-DC5BA692C858}' : 'IXCommands',
    '{001000AF-3DEF-001B-10B6-DC5BA692C858}' : 'IXObject',
    '{001000AF-3DEF-0017-10B6-DC5BA692C858}' : 'IXEvents',
    '{001000AF-3DEF-0019-10B6-DC5BA692C858}' : 'IXCommand',
    '{001000AF-3DEF-001D-10B6-DC5BA692C858}' : 'IX10DirectInterface',
    '{001000AF-3DEF-0200-10B6-DC5BA692C858}' : 'IXDeviceTypeDefault',
    '{001000AF-3DEF-0023-10B6-DC5BA692C858}' : 'IXGroups',
    '{001000AF-3DEF-0004-10B6-DC5BA692C858}' : '_IX10InterfaceEvents',
    '{001000AF-3DEF-0006-10B6-DC5BA692C858}' : 'IXProperty',
    '{001000AF-3DEF-0008-10B6-DC5BA692C858}' : 'IXConnection',
    '{001000AF-3DEF-000A-10B6-DC5BA692C858}' : 'IXConnectionTypes',
    '{001000AF-3DEF-0015-10B6-DC5BA692C858}' : 'IXSendCommands',
    '{001000AF-3DEF-000C-10B6-DC5BA692C858}' : 'IXConnectionTypeLocalSend',
    '{001000AF-3DEF-000E-10B6-DC5BA692C858}' : 'IXConnectionTypeNetClient',
    '{001000AF-3DEF-0010-10B6-DC5BA692C858}' : 'IXDevices',
    '{001000AF-3DEF-0012-10B6-DC5BA692C858}' : 'IXDeviceTypes',
    '{001000AF-3DEF-0009-10B6-DC5BA692C858}' : 'IXConnections',
    '{001000AF-3DEF-0014-10B6-DC5BA692C858}' : 'IXSendCommand',
    '{001000AF-3DEF-0018-10B6-DC5BA692C858}' : 'IXRecvCommand',
    '{001000AF-3DEF-001C-10B6-DC5BA692C858}' : 'IXObjects',
    '{001000AF-3DEF-0001-10B6-DC5BA692C858}' : 'IX10Control',
    '{001000AF-3DEF-0022-10B6-DC5BA692C858}' : 'IXGroup',
    '{001000AF-3DEF-0003-10B6-DC5BA692C858}' : 'IX10Interface',
    '{001000AF-3DEF-0005-10B6-DC5BA692C858}' : 'IXCollection',
    '{001000AF-3DEF-000B-10B6-DC5BA692C858}' : 'IXConnectionType',
    '{001000AF-3DEF-0007-10B6-DC5BA692C858}' : 'IXProperties',
}


NamesToIIDMap = {
    'IXCommand' : '{001000AF-3DEF-0019-10B6-DC5BA692C858}',
    'IX10Control' : '{001000AF-3DEF-0001-10B6-DC5BA692C858}',
    'IXConnectionTypeNetClient' : '{001000AF-3DEF-000E-10B6-DC5BA692C858}',
    'IXDevices' : '{001000AF-3DEF-0010-10B6-DC5BA692C858}',
    'IXConnectionTypeNetServer' : '{001000AF-3DEF-000F-10B6-DC5BA692C858}',
    'IXDeviceTypes' : '{001000AF-3DEF-0012-10B6-DC5BA692C858}',
    'IXConnectionTypeLocalSend' : '{001000AF-3DEF-000C-10B6-DC5BA692C858}',
    'IX10Interface' : '{001000AF-3DEF-0003-10B6-DC5BA692C858}',
    'IXProperty' : '{001000AF-3DEF-0006-10B6-DC5BA692C858}',
    '_IX10InterfaceEvents' : '{001000AF-3DEF-0004-10B6-DC5BA692C858}',
    'IXConnectionTypes' : '{001000AF-3DEF-000A-10B6-DC5BA692C858}',
    'IXConnectionTypeLocalRecv' : '{001000AF-3DEF-000D-10B6-DC5BA692C858}',
    'IXSendCommands' : '{001000AF-3DEF-0015-10B6-DC5BA692C858}',
    'IXEvents' : '{001000AF-3DEF-0017-10B6-DC5BA692C858}',
    'IXObjects' : '{001000AF-3DEF-001C-10B6-DC5BA692C858}',
    'IXConnectionType' : '{001000AF-3DEF-000B-10B6-DC5BA692C858}',
    'IXDevice' : '{001000AF-3DEF-0011-10B6-DC5BA692C858}',
    'IXEvent' : '{001000AF-3DEF-0016-10B6-DC5BA692C858}',
    'IXRecvCommand' : '{001000AF-3DEF-0018-10B6-DC5BA692C858}',
    'IXSendCommand' : '{001000AF-3DEF-0014-10B6-DC5BA692C858}',
    'IXConnection' : '{001000AF-3DEF-0008-10B6-DC5BA692C858}',
    '_DIX10ControlEvents' : '{001000AF-3DEF-0002-10B6-DC5BA692C858}',
    'IXCollection' : '{001000AF-3DEF-0005-10B6-DC5BA692C858}',
    'IXCommands' : '{001000AF-3DEF-001A-10B6-DC5BA692C858}',
    'IXDeviceTypeDefault' : '{001000AF-3DEF-0200-10B6-DC5BA692C858}',
    'IXDeviceType' : '{001000AF-3DEF-0013-10B6-DC5BA692C858}',
    'IXGroups' : '{001000AF-3DEF-0023-10B6-DC5BA692C858}',
    'IXGroup' : '{001000AF-3DEF-0022-10B6-DC5BA692C858}',
    'IX10DirectInterface' : '{001000AF-3DEF-001D-10B6-DC5BA692C858}',
    '_DIX10InterfaceEvents' : '{001000AF-3DEF-0024-10B6-DC5BA692C858}',
    'IXObject' : '{001000AF-3DEF-001B-10B6-DC5BA692C858}',
    'IXConnections' : '{001000AF-3DEF-0009-10B6-DC5BA692C858}',
    'IXProperties' : '{001000AF-3DEF-0007-10B6-DC5BA692C858}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)


# -*- coding: mbcs -*-
# Created by makepy.py version 0.4.95
# By python version 2.5 (r25:51908, Sep 19 2006, 09:52:17) [MSC v.1310 32 bit (Intel)]
# From type library 'Yards.exe'
# On Thu Sep 21 21:29:20 2006
"""Yards Bibliothek"""
makepy_version = '0.4.95'
python_version = 0x20500f0

import win32com.client.CLSIDToClass, pythoncom
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{8F8DC6FC-9A0A-43AE-B91C-7B8041DCBE61}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

class constants:
    gaoClear                      =0x2        # from enum GraphicAreaOp
    gaoClearOutline               =0x4        # from enum GraphicAreaOp
    gaoFill                       =0x1        # from enum GraphicAreaOp
    gaoInvert                     =0x0        # from enum GraphicAreaOp
    gaoOutline                    =0x3        # from enum GraphicAreaOp
    fnt10x14euro                  =0x4        # from enum GraphicFont
    fnt10x14katanka               =0x2        # from enum GraphicFont
    fnt5x7euro                    =0x3        # from enum GraphicFont
    fnt5x7katanka                 =0x1        # from enum GraphicFont
    fntMini                       =0x0        # from enum GraphicFont
    fntOnePixelSpace              =0x5        # from enum GraphicFont
    fntTwoPixelSpace              =0x6        # from enum GraphicFont
    porPowerOnKey0                =0x64       # from enum PowerOnReasons
    porPowerOnRemote              =0x3        # from enum PowerOnReasons
    porPowerOnReturn              =0x1        # from enum PowerOnReasons
    porPowerOnTimer               =0x2        # from enum PowerOnReasons
    porPowerOnTimer2              =0x4        # from enum PowerOnReasons
    porUnknown                    =0x0        # from enum PowerOnReasons

from win32com.client import DispatchBaseClass
class IYard(DispatchBaseClass):
    """Dispatch-Schnittstelle für Yard-Objekt"""
    CLSID = IID('{9F3FCB18-1F4B-41B9-BF8F-FB37675A2B81}')
    coclass_clsid = IID('{9AFE3574-1FAF-437F-A8C5-270ED1C84B2E}')

    def GetBootReason(self):
        """Liefert den Grund für den Neustart des Systems, sofern die Hardware ihn ausgelöst hat."""
        return self._oleobj_.InvokeTypes(7, LCID, 1, (3, 0), (),)

    def GetFirmwareVersion(self):
        """Liefert die Versionnummer der aktuellen Firmware (als Zahl zwischen 0 ... 255)"""
        return self._oleobj_.InvokeTypes(14, LCID, 1, (3, 0), (),)

    # Result is of type IYardLcd
    def GetLcd(self, nr=defaultNamedNotOptArg):
        ret = self._oleobj_.InvokeTypes(16, LCID, 1, (9, 0), ((3, 1),),nr
            )
        if ret is not None:
            ret = Dispatch(ret, 'GetLcd', '{7D2C1259-E55F-4D9D-96FC-04514A55BEE5}', UnicodeToString=0)
        return ret

    # Result is of type IYardRemotes
    def GetRemotes(self):
        """Liste der Fernbedienungen"""
        ret = self._oleobj_.InvokeTypes(13, LCID, 1, (9, 0), (),)
        if ret is not None:
            ret = Dispatch(ret, 'GetRemotes', '{7A218892-C4F2-40C8-8AC8-3C4B94A022D3}', UnicodeToString=0)
        return ret

    def GetTime(self):
        """Liefert die aktuelle Zeit der Hardware Uhr (genauigkeit beachten!)"""
        return self._oleobj_.InvokeTypes(4, LCID, 1, (7, 0), (),)

    def GetWakeupTime(self):
        """Liefert die aktuelle in der Hardware eingestellt Weckzeit."""
        return self._oleobj_.InvokeTypes(3, LCID, 1, (7, 0), (),)

    def ReadUserPort(self, portNr=defaultNamedNotOptArg):
        """Liefert den Status des freien Ports vom Pic."""
        return self._oleobj_.InvokeTypes(8, LCID, 1, (11, 0), ((3, 1),),portNr
            )

    def Read_I2C(self, adresse=defaultNamedNotOptArg, numReadBytes=defaultNamedNotOptArg, firstWriteBytesArray=defaultNamedNotOptArg):
        """Daten vom I2C Bus lesen, und ggf. vorher ein paar Bytes auf den I2C Bus schreiben."""
        return self._ApplyTypes_(11, 1, (12, 0), ((2, 1), (2, 1), (12, 1)), 'Read_I2C', None,adresse
            , numReadBytes, firstWriteBytesArray)

    def RegisterNotifier(self, notifier=defaultNamedNotOptArg):
        """Meldet einen neuen IR-Event Callback an."""
        return self._oleobj_.InvokeTypes(9, LCID, 1, (3, 0), ((13, 1),),notifier
            )

    def SendIrCode(self, protocolName=defaultNamedNotOptArg, codeSeq=defaultNamedNotOptArg, NumRepeats=defaultNamedNotOptArg):
        """Sendet einen IR-Code auf Basis eines im Server definierten Protokolls"""
        return self._oleobj_.InvokeTypes(2, LCID, 1, (11, 0), ((8, 1), (8, 1), (3, 1)),protocolName
            , codeSeq, NumRepeats)

    def SendRemoteKey(self, RemoteName=defaultNamedNotOptArg, KeyName=defaultNamedNotOptArg, NumRepeats=defaultNamedNotOptArg):
        """Sendet eine Taste einer im Server definierten Fernbedienung"""
        return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), ((8, 1), (8, 1), (3, 1)),RemoteName
            , KeyName, NumRepeats)

    def SetSecondWakeupTime(self, DateTimeValue=defaultNamedNotOptArg):
        """Stellt die 2. Hardware Weckzeit ein."""
        return self._oleobj_.InvokeTypes(15, LCID, 1, (11, 0), ((7, 1),),DateTimeValue
            )

    def SetTime(self, DateTimeValue=defaultNamedNotOptArg):
        """Stellt die Uhr der Hardware."""
        return self._oleobj_.InvokeTypes(6, LCID, 1, (24, 0), ((7, 1),),DateTimeValue
            )

    def SetWakeupTime(self, DateTimeValue=defaultNamedNotOptArg):
        """Stellt die Hardware Weckzeit ein."""
        return self._oleobj_.InvokeTypes(5, LCID, 1, (11, 0), ((7, 1),),DateTimeValue
            )

    def UnRegisterNotifier(self, handle=defaultNamedNotOptArg):
        """Meldet einen IR-Event Callback ab."""
        return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), ((3, 1),),handle
            )

    def Write_I2C(self, adresse=defaultNamedNotOptArg, daten=defaultNamedNotOptArg):
        """Nur Daten auf den I2C Bus schreiben."""
        return self._oleobj_.InvokeTypes(12, LCID, 1, (11, 0), ((2, 1), (12, 1)),adresse
            , daten)

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

class IYardGraphicLcd(DispatchBaseClass):
    """Noritake VFD"""
    CLSID = IID('{C93DB1A6-8FCC-4FD4-961D-9AF742869668}')
    coclass_clsid = IID('{48F91A1C-2833-4567-8691-EF5A45A69EFF}')

    def AreaOp(self, left=defaultNamedNotOptArg, top=defaultNamedNotOptArg, right=defaultNamedNotOptArg, bottom=defaultNamedNotOptArg
            , operation=defaultNamedNotOptArg):
        """Flaechenoperation (Fill,Clear,Rect,Invert..)"""
        return self._oleobj_.InvokeTypes(12, LCID, 1, (11, 0), ((3, 1), (3, 1), (3, 1), (3, 1), (3, 1)),left
            , top, right, bottom, operation)

    def BeginUpdate(self):
        return self._oleobj_.InvokeTypes(10, LCID, 1, (24, 0), (),)

    def ClrScr(self):
        return self._oleobj_.InvokeTypes(4, LCID, 1, (11, 0), (),)

    def DefineChar(self, chrnr=defaultNamedNotOptArg, permanent=defaultNamedNotOptArg, data=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(7, LCID, 1, (11, 0), ((16, 1), (11, 1), (12, 1)),chrnr
            , permanent, data)

    def DrawPixels(self, left=defaultNamedNotOptArg, top=defaultNamedNotOptArg, right=defaultNamedNotOptArg, bottom=defaultNamedNotOptArg
            , pixeldata=defaultNamedNotOptArg):
        """kopiert die Pixeldaten zeilenweise - auf das Display"""
        return self._oleobj_.InvokeTypes(14, LCID, 1, (11, 0), ((3, 1), (3, 1), (3, 1), (3, 1), (12, 1)),left
            , top, right, bottom, pixeldata)

    def EndUpdate(self):
        return self._oleobj_.InvokeTypes(19, LCID, 1, (24, 0), (),)

    def FillChar(self, count=defaultNamedNotOptArg, Value=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), ((16, 1), (16, 1)),count
            , Value)

    def GetGraphicSize(self, width=defaultNamedNotOptArg, height=defaultNamedNotOptArg):
        return self._ApplyTypes_(18, 1, (11, 0), ((16387, 3), (16387, 3)), 'GetGraphicSize', None,width
            , height)

    def GetSize(self, rows=defaultNamedNotOptArg, cols=defaultNamedNotOptArg):
        return self._ApplyTypes_(9, 1, (11, 0), ((16387, 3), (16387, 3)), 'GetSize', None,rows
            , cols)

    def GotoXY(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), ((16, 1), (16, 1)),x
            , y)

    def GraphicText(self, text=defaultNamedNotOptArg):
        """GraphicText an aktuelle Graphiccursorposition ausgeben"""
        return self._oleobj_.InvokeTypes(15, LCID, 1, (11, 0), ((8, 1),),text
            )

    def GraphicTextAt(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, text=defaultNamedNotOptArg):
        """GraphicText an bestimmter CursorPosition ausgeben"""
        return self._oleobj_.InvokeTypes(16, LCID, 1, (11, 0), ((3, 1), (3, 1), (8, 1)),x
            , y, text)

    def LoadBitmap(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, filename=defaultNamedNotOptArg):
        """laedt eine SW-Bitmap auf eine bestimmte Position des Displays"""
        return self._oleobj_.InvokeTypes(13, LCID, 1, (11, 0), ((3, 1), (3, 1), (8, 1)),x
            , y, filename)

    def MoveGraphicCursor(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
        """positioniert den Grafikcursor für Textausgabe"""
        return self._oleobj_.InvokeTypes(17, LCID, 1, (11, 0), ((3, 1), (3, 1)),x
            , y)

    def Print(self, str=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(2, LCID, 1, (11, 0), ((8, 1),),str
            )

    def PrintAt(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, str=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(3, LCID, 1, (11, 0), ((16, 1), (16, 1), (8, 1)),x
            , y, str)

    def PutChar(self, ch=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(8, LCID, 1, (11, 0), ((17, 1),),ch
            )

    def SelectFont(self, fnt=defaultNamedNotOptArg):
        """Font für Graphictextausgabe festlegen"""
        return self._oleobj_.InvokeTypes(11, LCID, 1, (11, 0), ((3, 1),),fnt
            )

    def SetBacklight(self, Value=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(5, LCID, 1, (11, 0), ((16, 1),),Value
            )

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

class IYardLcd(DispatchBaseClass):
    """LCD Display"""
    CLSID = IID('{7D2C1259-E55F-4D9D-96FC-04514A55BEE5}')
    coclass_clsid = IID('{AF9E7532-C9B1-4F75-9232-A64211BB403F}')

    def ClrScr(self):
        return self._oleobj_.InvokeTypes(4, LCID, 1, (11, 0), (),)

    def DefineChar(self, chrnr=defaultNamedNotOptArg, permanent=defaultNamedNotOptArg, data=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(7, LCID, 1, (11, 0), ((16, 1), (11, 1), (12, 1)),chrnr
            , permanent, data)

    def FillChar(self, count=defaultNamedNotOptArg, Value=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), ((16, 1), (16, 1)),count
            , Value)

    def GetSize(self, rows=defaultNamedNotOptArg, cols=defaultNamedNotOptArg):
        return self._ApplyTypes_(9, 1, (11, 0), ((16387, 3), (16387, 3)), 'GetSize', None,rows
            , cols)

    def GotoXY(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), ((16, 1), (16, 1)),x
            , y)

    def Print(self, str=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(2, LCID, 1, (11, 0), ((8, 1),),str
            )

    def PrintAt(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, str=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(3, LCID, 1, (11, 0), ((16, 1), (16, 1), (8, 1)),x
            , y, str)

    def PutChar(self, ch=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(8, LCID, 1, (11, 0), ((17, 1),),ch
            )

    def SetBacklight(self, Value=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(5, LCID, 1, (11, 0), ((16, 1),),Value
            )

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

class IYardNotification2:
    CLSID = CLSID_Sink = IID('{C0E81602-A672-4CA0-B245-851456CD126D}')
    coclass_clsid = IID('{9AFE3574-1FAF-437F-A8C5-270ED1C84B2E}')
    _public_methods_ = [] # For COM Server support
    _dispid_to_func_ = {
                1 : "OngetName",
                3 : "OnReceivedKey",
                2 : "OnShutdown",
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
#	def OngetName(self, result=pythoncom.Missing):
#	def OnReceivedKey(self, key=defaultNamedNotOptArg):
#	def OnShutdown(self):


class IYardRemote(DispatchBaseClass):
    CLSID = IID('{42F9F112-DA9B-44E9-A586-9F1ECDB3E27B}')
    coclass_clsid = IID('{B0711A1F-C3A8-4C58-BCC9-793AE0232073}')

    # Result is of type IYardRemoteKey
    def FindKey(self, KeyName=defaultNamedNotOptArg):
        """Taste suchen"""
        ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), ((8, 1),),KeyName
            )
        if ret is not None:
            ret = Dispatch(ret, 'FindKey', '{C10A342B-6A65-49C4-87B0-68720BBC0741}', UnicodeToString=0)
        return ret

    # Result is of type IYardRemoteKey
    # The method Keys is actually a property, but must be used as a method to correctly pass the arguments
    def Keys(self, index=defaultNamedNotOptArg):
        """Tasten"""
        ret = self._oleobj_.InvokeTypes(4, LCID, 2, (9, 0), ((3, 1),),index
            )
        if ret is not None:
            ret = Dispatch(ret, 'Keys', '{C10A342B-6A65-49C4-87B0-68720BBC0741}', UnicodeToString=0)
        return ret

    _prop_map_get_ = {
        "Name": (1, 2, (8, 0), (), "Name", None),
        "count": (3, 2, (3, 0), (), "count", None),
    }
    _prop_map_put_ = {
    }
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(3, 2, (3, 0), (), "count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

class IYardRemoteKey(DispatchBaseClass):
    CLSID = IID('{C10A342B-6A65-49C4-87B0-68720BBC0741}')
    coclass_clsid = IID('{D0354179-B63D-4B64-827F-C6FFAA38D77C}')

    _prop_map_get_ = {
        "Code": (4, 2, (8, 0), (), "Code", None),
        "Name": (2, 2, (8, 0), (), "Name", None),
        "Protocol": (5, 2, (8, 0), (), "Protocol", None),
    }
    _prop_map_put_ = {
    }

class IYardRemotes(DispatchBaseClass):
    """Liste der Fernbedienungen"""
    CLSID = IID('{7A218892-C4F2-40C8-8AC8-3C4B94A022D3}')
    coclass_clsid = IID('{9F79C001-3887-4C6C-B456-A145C9523C2E}')

    # Result is of type IYardRemote
    def FindRemote(self, RemoteName=defaultNamedNotOptArg):
        """Fernbedienung suchen"""
        ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), ((8, 1),),RemoteName
            )
        if ret is not None:
            ret = Dispatch(ret, 'FindRemote', '{42F9F112-DA9B-44E9-A586-9F1ECDB3E27B}', UnicodeToString=0)
        return ret

    # Result is of type IYardRemote
    # The method Item is actually a property, but must be used as a method to correctly pass the arguments
    def Item(self, index=defaultNamedNotOptArg):
        """Fernbedienung"""
        ret = self._oleobj_.InvokeTypes(2, LCID, 2, (9, 0), ((3, 1),),index
            )
        if ret is not None:
            ret = Dispatch(ret, 'Item', '{42F9F112-DA9B-44E9-A586-9F1ECDB3E27B}', UnicodeToString=0)
        return ret

    _prop_map_get_ = {
        "count": (1, 2, (3, 0), (), "count", None),
    }
    _prop_map_put_ = {
    }
    #This class has Item property/method which may take args - allow indexed access
    def __getitem__(self, item):
        return self._get_good_object_(self._oleobj_.Invoke(*(2, LCID, 2, 1, item)), "Item")
    #This class has Count() property - allow len(ob) to provide this
    def __len__(self):
        return self._ApplyTypes_(*(1, 2, (3, 0), (), "count", None))
    #This class has a __len__ - this is needed so 'if object:' always returns TRUE.
    def __nonzero__(self):
        return True

from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'Yards.Yard'
class Yard(CoClassBaseClass): # A CoClass
    # Yard Objekt
    CLSID = IID('{9AFE3574-1FAF-437F-A8C5-270ED1C84B2E}')
    coclass_sources = [
        IYardNotification2,
    ]
    default_source = IYardNotification2
    coclass_interfaces = [
        IYard,
    ]
    default_interface = IYard

class YardGraphicLcd(CoClassBaseClass): # A CoClass
    CLSID = IID('{48F91A1C-2833-4567-8691-EF5A45A69EFF}')
    coclass_sources = [
    ]
    coclass_interfaces = [
        IYardGraphicLcd,
    ]
    default_interface = IYardGraphicLcd

class YardLcd(CoClassBaseClass): # A CoClass
    CLSID = IID('{AF9E7532-C9B1-4F75-9232-A64211BB403F}')
    coclass_sources = [
    ]
    coclass_interfaces = [
        IYardLcd,
    ]
    default_interface = IYardLcd

class YardRemote(CoClassBaseClass): # A CoClass
    CLSID = IID('{B0711A1F-C3A8-4C58-BCC9-793AE0232073}')
    coclass_sources = [
    ]
    coclass_interfaces = [
        IYardRemote,
    ]
    default_interface = IYardRemote

class YardRemoteKey(CoClassBaseClass): # A CoClass
    CLSID = IID('{D0354179-B63D-4B64-827F-C6FFAA38D77C}')
    coclass_sources = [
    ]
    coclass_interfaces = [
        IYardRemoteKey,
    ]
    default_interface = IYardRemoteKey

class YardRemotes(CoClassBaseClass): # A CoClass
    CLSID = IID('{9F79C001-3887-4C6C-B456-A145C9523C2E}')
    coclass_sources = [
    ]
    coclass_interfaces = [
        IYardRemotes,
    ]
    default_interface = IYardRemotes

IYard_vtables_dispatch_ = 1
IYard_vtables_ = [
    (( 'SendRemoteKey' , 'RemoteName' , 'KeyName' , 'NumRepeats' , 'result' , 
            ), 1, (1, (), [ (8, 1, None, None) , (8, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 28 , (3, 0, None, None) , 0 , )),
    (( 'SendIrCode' , 'protocolName' , 'codeSeq' , 'NumRepeats' , 'result' , 
            ), 2, (2, (), [ (8, 1, None, None) , (8, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
    (( 'GetWakeupTime' , 'result' , ), 3, (3, (), [ (16391, 10, None, None) , ], 1 , 1 , 4 , 0 , 36 , (3, 0, None, None) , 0 , )),
    (( 'GetTime' , 'result' , ), 4, (4, (), [ (16391, 10, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
    (( 'SetWakeupTime' , 'DateTimeValue' , 'result' , ), 5, (5, (), [ (7, 1, None, None) , 
            (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 44 , (3, 0, None, None) , 0 , )),
    (( 'SetTime' , 'DateTimeValue' , ), 6, (6, (), [ (7, 1, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
    (( 'GetBootReason' , 'result' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 52 , (3, 0, None, None) , 0 , )),
    (( 'ReadUserPort' , 'portNr' , 'result' , ), 8, (8, (), [ (3, 1, None, None) , 
            (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
    (( 'RegisterNotifier' , 'notifier' , 'result' , ), 9, (9, (), [ (13, 1, None, "IID('{4DA51DCB-76CA-4FB0-8837-04CC9FF39E31}')") , 
            (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 60 , (3, 0, None, None) , 0 , )),
    (( 'UnRegisterNotifier' , 'handle' , ), 10, (10, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
    (( 'Read_I2C' , 'adresse' , 'numReadBytes' , 'firstWriteBytesArray' , 'result' , 
            ), 11, (11, (), [ (2, 1, None, None) , (2, 1, None, None) , (12, 1, None, None) , (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 68 , (3, 0, None, None) , 0 , )),
    (( 'Write_I2C' , 'adresse' , 'daten' , 'result' , ), 12, (12, (), [ 
            (2, 1, None, None) , (12, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
    (( 'GetRemotes' , 'result' , ), 13, (13, (), [ (16393, 10, None, "IID('{7A218892-C4F2-40C8-8AC8-3C4B94A022D3}')") , ], 1 , 1 , 4 , 0 , 76 , (3, 0, None, None) , 0 , )),
    (( 'GetFirmwareVersion' , 'result' , ), 14, (14, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
    (( 'GetLcd' , 'nr' , 'result' , ), 16, (16, (), [ (3, 1, None, None) , 
            (16393, 10, None, "IID('{7D2C1259-E55F-4D9D-96FC-04514A55BEE5}')") , ], 1 , 1 , 4 , 0 , 84 , (3, 0, None, None) , 0 , )),
    (( 'SetSecondWakeupTime' , 'DateTimeValue' , 'result' , ), 15, (15, (), [ (7, 1, None, None) , 
            (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
]

IYardGraphicLcd_vtables_dispatch_ = 1
IYardGraphicLcd_vtables_ = [
    (( 'MoveGraphicCursor' , 'x' , 'y' , 'result' , ), 17, (17, (), [ 
            (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
    (( 'SelectFont' , 'fnt' , 'result' , ), 11, (11, (), [ (3, 1, None, None) , 
            (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 68 , (3, 0, None, None) , 0 , )),
    (( 'AreaOp' , 'left' , 'top' , 'right' , 'bottom' , 
            'operation' , 'result' , ), 12, (12, (), [ (3, 1, None, None) , (3, 1, None, None) , 
            (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
    (( 'LoadBitmap' , 'x' , 'y' , 'filename' , 'result' , 
            ), 13, (13, (), [ (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 76 , (3, 0, None, None) , 0 , )),
    (( 'DrawPixels' , 'left' , 'top' , 'right' , 'bottom' , 
            'pixeldata' , 'result' , ), 14, (14, (), [ (3, 1, None, None) , (3, 1, None, None) , 
            (3, 1, None, None) , (3, 1, None, None) , (12, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
    (( 'GraphicText' , 'text' , 'result' , ), 15, (15, (), [ (8, 1, None, None) , 
            (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 84 , (3, 0, None, None) , 0 , )),
    (( 'GraphicTextAt' , 'x' , 'y' , 'text' , 'result' , 
            ), 16, (16, (), [ (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
    (( 'GetGraphicSize' , 'width' , 'height' , 'result' , ), 18, (18, (), [ 
            (16387, 3, None, None) , (16387, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 92 , (3, 0, None, None) , 0 , )),
    (( 'BeginUpdate' , ), 10, (10, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
    (( 'EndUpdate' , ), 19, (19, (), [ ], 1 , 1 , 4 , 0 , 100 , (3, 0, None, None) , 0 , )),
]

IYardLcd_vtables_dispatch_ = 1
IYardLcd_vtables_ = [
    (( 'GotoXY' , 'x' , 'y' , 'result' , ), 1, (1, (), [ 
            (16, 1, None, None) , (16, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 28 , (3, 0, None, None) , 0 , )),
    (( 'Print' , 'str' , 'result' , ), 2, (2, (), [ (8, 1, None, None) , 
            (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
    (( 'PrintAt' , 'x' , 'y' , 'str' , 'result' , 
            ), 3, (3, (), [ (16, 1, None, None) , (16, 1, None, None) , (8, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 36 , (3, 0, None, None) , 0 , )),
    (( 'ClrScr' , 'result' , ), 4, (4, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
    (( 'SetBacklight' , 'Value' , 'result' , ), 5, (5, (), [ (16, 1, None, None) , 
            (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 44 , (3, 0, None, None) , 0 , )),
    (( 'FillChar' , 'count' , 'Value' , 'result' , ), 6, (6, (), [ 
            (16, 1, None, None) , (16, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
    (( 'DefineChar' , 'chrnr' , 'permanent' , 'data' , 'result' , 
            ), 7, (7, (), [ (16, 1, None, None) , (11, 1, None, None) , (12, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 52 , (3, 0, None, None) , 0 , )),
    (( 'PutChar' , 'ch' , 'result' , ), 8, (8, (), [ (17, 1, None, None) , 
            (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
    (( 'GetSize' , 'rows' , 'cols' , 'result' , ), 9, (9, (), [ 
            (16387, 3, None, None) , (16387, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 60 , (3, 0, None, None) , 0 , )),
]

IYardNotification_vtables_dispatch_ = 0
IYardNotification_vtables_ = [
    (( 'Shutdown' , ), 2, (2, (), [ ], 1 , 1 , 4 , 0 , 12 , (24, 0, None, None) , 0 , )),
    (( 'ReceivedKey' , 'key' , ), 3, (3, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 16 , (24, 0, None, None) , 0 , )),
    (( 'getName' , 'tmp' , ), 4, (4, (), [ (16392, 3, None, None) , ], 1 , 1 , 4 , 0 , 20 , (24, 0, None, None) , 0 , )),
]

IYardRemote_vtables_dispatch_ = 1
IYardRemote_vtables_ = [
    (( 'Name' , 'Value' , ), 1, (1, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 28 , (3, 0, None, None) , 0 , )),
    (( 'count' , 'Value' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
    (( 'Keys' , 'index' , 'Value' , ), 4, (4, (), [ (3, 1, None, None) , 
            (16393, 10, None, "IID('{C10A342B-6A65-49C4-87B0-68720BBC0741}')") , ], 1 , 2 , 4 , 0 , 36 , (3, 0, None, None) , 0 , )),
    (( 'FindKey' , 'KeyName' , 'result' , ), 5, (5, (), [ (8, 1, None, None) , 
            (16393, 10, None, "IID('{C10A342B-6A65-49C4-87B0-68720BBC0741}')") , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
]

IYardRemoteKey_vtables_dispatch_ = 1
IYardRemoteKey_vtables_ = [
    (( 'Name' , 'Value' , ), 2, (2, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 28 , (3, 0, None, None) , 0 , )),
    (( 'Code' , 'Value' , ), 4, (4, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
    (( 'Protocol' , 'Value' , ), 5, (5, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 36 , (3, 0, None, None) , 0 , )),
]

IYardRemotes_vtables_dispatch_ = 1
IYardRemotes_vtables_ = [
    (( 'count' , 'Value' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 28 , (3, 0, None, None) , 0 , )),
    (( 'Item' , 'index' , 'Value' , ), 2, (2, (), [ (3, 1, None, None) , 
            (16393, 10, None, "IID('{42F9F112-DA9B-44E9-A586-9F1ECDB3E27B}')") , ], 1 , 2 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
    (( 'FindRemote' , 'RemoteName' , 'result' , ), 3, (3, (), [ (8, 1, None, None) , 
            (16393, 10, None, "IID('{42F9F112-DA9B-44E9-A586-9F1ECDB3E27B}')") , ], 1 , 1 , 4 , 0 , 36 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
    '{C0E81602-A672-4CA0-B245-851456CD126D}' : IYardNotification2,
    '{7A218892-C4F2-40C8-8AC8-3C4B94A022D3}' : IYardRemotes,
    '{B0711A1F-C3A8-4C58-BCC9-793AE0232073}' : YardRemote,
    '{9F79C001-3887-4C6C-B456-A145C9523C2E}' : YardRemotes,
    '{AF9E7532-C9B1-4F75-9232-A64211BB403F}' : YardLcd,
    '{9F3FCB18-1F4B-41B9-BF8F-FB37675A2B81}' : IYard,
    '{C93DB1A6-8FCC-4FD4-961D-9AF742869668}' : IYardGraphicLcd,
    '{C10A342B-6A65-49C4-87B0-68720BBC0741}' : IYardRemoteKey,
    '{D0354179-B63D-4B64-827F-C6FFAA38D77C}' : YardRemoteKey,
    '{7D2C1259-E55F-4D9D-96FC-04514A55BEE5}' : IYardLcd,
    '{48F91A1C-2833-4567-8691-EF5A45A69EFF}' : YardGraphicLcd,
    '{9AFE3574-1FAF-437F-A8C5-270ED1C84B2E}' : Yard,
    '{42F9F112-DA9B-44E9-A586-9F1ECDB3E27B}' : IYardRemote,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
    '{7A218892-C4F2-40C8-8AC8-3C4B94A022D3}' : 'IYardRemotes',
    '{9F3FCB18-1F4B-41B9-BF8F-FB37675A2B81}' : 'IYard',
    '{C93DB1A6-8FCC-4FD4-961D-9AF742869668}' : 'IYardGraphicLcd',
    '{C10A342B-6A65-49C4-87B0-68720BBC0741}' : 'IYardRemoteKey',
    '{7D2C1259-E55F-4D9D-96FC-04514A55BEE5}' : 'IYardLcd',
    '{4DA51DCB-76CA-4FB0-8837-04CC9FF39E31}' : 'IYardNotification',
    '{42F9F112-DA9B-44E9-A586-9F1ECDB3E27B}' : 'IYardRemote',
}


NamesToIIDMap = {
    'IYardRemotes' : '{7A218892-C4F2-40C8-8AC8-3C4B94A022D3}',
    'IYardGraphicLcd' : '{C93DB1A6-8FCC-4FD4-961D-9AF742869668}',
    'IYardRemote' : '{42F9F112-DA9B-44E9-A586-9F1ECDB3E27B}',
    'IYard' : '{9F3FCB18-1F4B-41B9-BF8F-FB37675A2B81}',
    'IYardLcd' : '{7D2C1259-E55F-4D9D-96FC-04514A55BEE5}',
    'IYardNotification2' : '{C0E81602-A672-4CA0-B245-851456CD126D}',
    'IYardRemoteKey' : '{C10A342B-6A65-49C4-87B0-68720BBC0741}',
    'IYardNotification' : '{4DA51DCB-76CA-4FB0-8837-04CC9FF39E31}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)


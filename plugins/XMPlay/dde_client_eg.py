# -*- coding: utf-8 -*-
#
# DDE Management Library (DDEML) client module
#
# Notes:
# This code has been adapted from David Naylor's dde-client code from
# ActiveState's Python recipes (Revision 1) modified by Indranil Sinharoy
# Copyright:
# (c) David Naylor
# Licence:
# New BSD license
# Website:
# http://code.activestate.com/recipes/577654-dde-client/
#

# DDEML will attempt to convert the command string based on the target build of the DDE server, 
# which it knows based on whether you called the ANSI or Unicode version of DdeInitialize().
# The scenario where it does fail though is sending a CF_TEXT format command string 
# from a Unicode build DDE client to an ANSI build DDE server.
# MUST default to CF_UNICODETEXT.
# http://chrisoldwood.blogspot.com/2013/11/dde-xtypexecute-command-corruption.html
#


from ctypes import c_int, c_double, c_char_p, c_wchar_p, c_void_p, c_ulong, c_char, c_byte
from ctypes import windll, byref, create_string_buffer, create_unicode_buffer, Structure, sizeof
from ctypes import POINTER, WINFUNCTYPE
from ctypes.wintypes import BOOL, HWND, MSG, DWORD, BYTE, INT, LPCWSTR, UINT, ULONG, LPCSTR, LPSTR, LPWSTR, WPARAM
import UserDict


# DECLARE_HANDLE(name) typedef void *name;
HCONV     = c_void_p  # = DECLARE_HANDLE(HCONV)
HDDEDATA  = c_void_p  # = DECLARE_HANDLE(HDDEDATA)
HSZ       = c_void_p  # = DECLARE_HANDLE(HSZ)
LPBYTE    = POINTER(BYTE) #LPSTR
LPDWORD   = POINTER(DWORD)
ULONG_PTR = WPARAM #c_ulong
DWORD_PTR = ULONG_PTR
HCONVLIST = c_void_p  # = DECLARE_HANDLE(HCONVLIST)
PCONVINFO = c_void_p
PCONVCONTEXT = c_void_p

# DDEML errors
DMLERR_NO_ERROR            = 0x0000  # No error
DMLERR_ADVACKTIMEOUT       = 0x4000  # request for synchronous advise transaction timed out
DMLERR_BUSY                = 0x4001
DMLERR_DATAACKTIMEOUT      = 0x4002  # request for synchronous data transaction timed out
DMLERR_DLL_NOT_INITIALIZED = 0x4003  # DDEML functions called without iniatializing
DMLERR_DLL_USAGE           = 0x4004
DMLERR_EXECACKTIMEOUT      = 0x4005  # request for synchronous execute transaction timed out
DMLERR_INVALIDPARAMETER    = 0x4006
DMLERR_LOW_MEMORY          = 0x4007
DMLERR_MEMORY_ERROR        = 0x4008
DMLERR_NOTPROCESSED        = 0x4009
DMLERR_NO_CONV_ESTABLISHED = 0x400a  # client's attempt to establish a conversation has failed (can happen during DdeConnect)
DMLERR_POKEACKTIMEOUT      = 0x400b  # A request for a synchronous poke transaction has timed out.
DMLERR_POSTMSG_FAILED      = 0x400c  # An internal call to the PostMessage function has failed.
DMLERR_REENTRANCY          = 0x400d
DMLERR_SERVER_DIED         = 0x400e
DMLERR_SYS_ERROR           = 0x400f
DMLERR_UNADVACKTIMEOUT     = 0x4010
DMLERR_UNFOUND_QUEUE_ID    = 0x4011

# Predefined Clipboard Formats
CF_TEXT         =  1
CF_BITMAP       =  2
CF_METAFILEPICT =  3
CF_SYLK         =  4
CF_DIF          =  5
CF_TIFF         =  6
CF_OEMTEXT      =  7
CF_DIB          =  8
CF_PALETTE      =  9
CF_PENDATA      = 10
CF_RIFF         = 11
CF_WAVE         = 12
CF_UNICODETEXT  = 13
CF_ENHMETAFILE  = 14
CF_HDROP        = 15
CF_LOCALE       = 16
CF_DIBV5        = 17
CF_MAX          = 18

# DDE conversation states
XST_NULL           = 0  # quiescent states
XST_INCOMPLETE     = 1
XST_CONNECTED      = 2
XST_INIT1          = 3  # mid-initiation states
XST_INIT2          = 4
XST_REQSENT        = 5  # active conversation states
XST_DATARCVD       = 6
XST_POKESENT       = 7
XST_POKEACKRCVD    = 8
XST_EXECSENT       = 9
XST_EXECACKRCVD    = 10
XST_ADVSENT        = 11
XST_UNADVSENT      = 12
XST_ADVACKRCVD     = 13
XST_UNADVACKRCVD   = 14
XST_ADVDATASENT    = 15
XST_ADVDATAACKRCVD = 16

# DDE conversation status bits
ST_CONNECTED  = 0x0001
ST_ADVISE     = 0x0002
ST_ISLOCAL    = 0x0004
ST_BLOCKED    = 0x0008
ST_CLIENT     = 0x0010
ST_TERMINATED = 0x0020
ST_INLIST     = 0x0040
ST_BLOCKNEXT  = 0x0080
ST_ISSELF     = 0x0100 

# DDE constants for wStatus field
DDE_FACK          = 0x8000
DDE_FBUSY         = 0x4000
DDE_FDEFERUPD     = 0x4000
DDE_FACKREQ       = 0x8000
DDE_FRELEASE      = 0x2000
DDE_FREQUESTED    = 0x1000
DDE_FAPPSTATUS    = 0x00FF
DDE_FNOTPROCESSED = 0x0000

DDE_FACKRESERVED  = (~(DDE_FACK | DDE_FBUSY | DDE_FAPPSTATUS))
DDE_FADVRESERVED  = (~(DDE_FACKREQ | DDE_FDEFERUPD))
DDE_FDATRESERVED  = (~(DDE_FACKREQ | DDE_FRELEASE | DDE_FREQUESTED))
DDE_FPOKRESERVED  = (~(DDE_FRELEASE))

# DDEML Transaction class flags
XTYPF_NOBLOCK        = 0x0002
XTYPF_NODATA         = 0x0004
XTYPF_ACKREQ         = 0x0008

XCLASS_MASK          = 0xFC00
XCLASS_BOOL          = 0x1000
XCLASS_DATA          = 0x2000
XCLASS_FLAGS         = 0x4000
XCLASS_NOTIFICATION  = 0x8000

XTYP_ERROR           = (0x0000 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)
XTYP_ADVDATA         = (0x0010 | XCLASS_FLAGS)
XTYP_ADVREQ          = (0x0020 | XCLASS_DATA | XTYPF_NOBLOCK)
XTYP_ADVSTART        = (0x0030 | XCLASS_BOOL)
XTYP_ADVSTOP         = (0x0040 | XCLASS_NOTIFICATION)
XTYP_EXECUTE         = (0x0050 | XCLASS_FLAGS)
XTYP_CONNECT         = (0x0060 | XCLASS_BOOL | XTYPF_NOBLOCK)
XTYP_CONNECT_CONFIRM = (0x0070 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)
XTYP_XACT_COMPLETE   = (0x0080 | XCLASS_NOTIFICATION )
XTYP_POKE            = (0x0090 | XCLASS_FLAGS)
XTYP_REGISTER        = (0x00A0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK )
XTYP_REQUEST         = (0x00B0 | XCLASS_DATA )
XTYP_DISCONNECT      = (0x00C0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK )
XTYP_UNREGISTER      = (0x00D0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK )
XTYP_WILDCONNECT     = (0x00E0 | XCLASS_DATA | XTYPF_NOBLOCK)
XTYP_MONITOR         = (0x00F0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)

XTYP_MASK            = 0x00F0
XTYP_SHIFT           = 4

# DDE Timeout constants
TIMEOUT_ASYNC        = 0xFFFFFFFF

# DDE Transaction ID constants
QID_SYNC             = 0xFFFFFFFF

# DDE Initialization flags (afCmd)

# Callback filter flags for use with standard apps.
CBF_FAIL_SELFCONNECTIONS     = 0x00001000
CBF_FAIL_CONNECTIONS         = 0x00002000
CBF_FAIL_ADVISES             = 0x00004000
CBF_FAIL_EXECUTES            = 0x00008000
CBF_FAIL_POKES               = 0x00010000
CBF_FAIL_REQUESTS            = 0x00020000
CBF_FAIL_ALLSVRXACTIONS      = 0x0003f000
CBF_SKIP_CONNECT_CONFIRMS    = 0x00040000
CBF_SKIP_REGISTRATIONS       = 0x00080000
CBF_SKIP_UNREGISTRATIONS     = 0x00100000
CBF_SKIP_DISCONNECTS         = 0x00200000
CBF_SKIP_ALLNOTIFICATIONS    = 0x003c0000

# Application command flags
APPCMD_CLIENTONLY            = 0x00000010
APPCMD_FILTERINITS           = 0x00000020
APPCMD_MASK                  = 0x00000FF0

# Application classification flags
APPCLASS_STANDARD            = 0x00000000
APPCLASS_MASK                = 0x0000000F
APPCLASS_MONITOR             = 0x00000001

# Callback filter flags for use with MONITOR apps - 0 implies no monitor callbacks.
MF_HSZ_INFO                  = 0x01000000
MF_SENDMSGS                  = 0x02000000
MF_POSTMSGS                  = 0x04000000
MF_CALLBACKS                 = 0x08000000
MF_ERRORS                    = 0x10000000
MF_LINKS                     = 0x20000000
MF_CONV                      = 0x40000000
MF_MASK                      = 0xFF000000

# Code page for rendering string.
CP_WINANSI      = 1004    # default codepage for windows & old DDE convs.
CP_WINUNICODE   = 1200

# Declaration
DDECALLBACK = WINFUNCTYPE(HDDEDATA, UINT, UINT, HCONV, HSZ, HSZ, HDDEDATA, ULONG_PTR, ULONG_PTR)


class SECURITY_QUALITY_OF_SERVICE(Structure):
    _fields_ = [
        ("Length",              c_ulong),
        ("ImpersonationLevel",  c_ulong),
        ("ContextTrackingMode", c_byte ),
        ("EffectiveOnly",       c_byte )
    ]

class CONVCONTEXT(Structure):
    _fields_ = [
        ("cb",         UINT                       ),
        ("wFlags",     UINT                       ),
        ("wCountryID", UINT                       ),
        ("iCodePage",  c_int                      ),
        ("dwLangID",   DWORD                      ),
        ("dwSecurity", DWORD                      ),
        ("qos",        SECURITY_QUALITY_OF_SERVICE)
    ]

class CONVINFO(Structure):
    _fields_ = [
        ("cb",            DWORD      ),
        ("hUser",         DWORD_PTR  ),
        ("hConvPartner",  HCONV      ),
        ("hszSvcPartner", HSZ        ),
        ("hszServiceReq", HSZ        ),
        ("hszTopic",      HSZ        ),
        ("hszItem",       HSZ        ),
        ("wFmt",          UINT       ),
        ("wType",         UINT       ),
        ("wStatus",       UINT       ),
        ("wConvst",       UINT       ),
        ("wLastError",    UINT       ),
        ("hConvList",     HCONVLIST  ),
        ("ConvCtxt",      CONVCONTEXT),
        ("hwnd",          HWND       ),
        ("hwndPartner",   HWND       )
    ]

    
    
def get_winfunc(funcname, restype=None, argtypes=()):
    """Retrieve a function from a library/DLL, and set the data types."""
    func = getattr(windll.user32, funcname)
    func.argtypes = argtypes
    func.restype = restype
    return func
    
    
class DDE(object):
    """Object containing all the DDEML functions"""
    #AccessData         = get_winfunc("DdeAccessData",          LPBYTE,   (HDDEDATA, LPDWORD))
    ClientTransaction  = get_winfunc("DdeClientTransaction",   HDDEDATA, (LPBYTE, DWORD, HCONV, HSZ, UINT, UINT, DWORD, LPDWORD))
    Connect            = get_winfunc("DdeConnect",             HCONV,    (DWORD, HSZ, HSZ, PCONVCONTEXT))
    #CreateDataHandle   = get_winfunc("DdeCreateDataHandle",    HDDEDATA, (DWORD, LPBYTE, DWORD, DWORD, HSZ, UINT, UINT))
    CreateStringHandle = get_winfunc("DdeCreateStringHandleW", HSZ,      (DWORD, LPCWSTR, UINT))  # Unicode version
    #CreateStringHandle = get_winfunc("DdeCreateStringHandleA", HSZ,      (DWORD, LPCSTR, UINT))  # ANSI version
    Disconnect         = get_winfunc("DdeDisconnect",          BOOL,     (HCONV,))
    GetLastError       = get_winfunc("DdeGetLastError",        UINT,     (DWORD,))
    Initialize         = get_winfunc("DdeInitializeW",         UINT,     (LPDWORD, DDECALLBACK, DWORD, DWORD)) # Unicode version of DDE initialize
    #Initialize         = get_winfunc("DdeInitializeA",         UINT,     (LPDWORD, DDECALLBACK, DWORD, DWORD)) # ANSI version of DDE initialize
    FreeDataHandle     = get_winfunc("DdeFreeDataHandle",      BOOL,     (HDDEDATA,))
    FreeStringHandle   = get_winfunc("DdeFreeStringHandle",    BOOL,     (DWORD, HSZ))
    QueryString        = get_winfunc("DdeQueryStringW",        DWORD,    (DWORD, HSZ, LPWSTR, DWORD, c_int)) # Unicode version of QueryString
    #QueryString        = get_winfunc("DdeQueryStringA",        DWORD,    (DWORD, HSZ, LPSTR, DWORD, c_int)) # ANSI version of QueryString
    #UnaccessData       = get_winfunc("DdeUnaccessData",        BOOL,     (HDDEDATA,))
    Uninitialize       = get_winfunc("DdeUninitialize",        BOOL,     (DWORD,))
    AbandonTransaction = get_winfunc("DdeAbandonTransaction",  BOOL,     (DWORD, HCONV, DWORD))
    GetData            = get_winfunc("DdeGetData",             DWORD,    (HDDEDATA, LPBYTE, DWORD, DWORD))
    QueryConvInfo      = get_winfunc("DdeQueryConvInfo",       UINT,     (HCONV, DWORD, PCONVINFO))
    
    
    @classmethod
    def get_data(cls, hDdeData):
        """
        Gets raw DDE data.
        If text expected it may need to be interpreted with decode().
        """
        if not hDdeData:
            return None
        i = cls.GetData(hDdeData, None, 0, 0)
        if i:
            array = bytearray(i)
            pDst = (c_byte * i).from_buffer(array)
            cls.GetData(hDdeData, pDst, i, 0)
            return array
            # pDst = (c_byte * i)()
            # cls.GetData(hDdeData, pDst, i, 0)
            # return cast(pDst, ctypes.c_char_p).value
            # return bytearray(pDst)
        else:
            return None
    
    
    @classmethod
    def query_string(cls, idInst, hsz):
            if not hsz:
                return ""
            i = cls.QueryString(idInst, hsz, None, 0, CP_WINUNICODE)
            if i:
                i += 1
                buffer = create_unicode_buffer(i)
                cls.QueryString(idInst, hsz, buffer, i, CP_WINUNICODE)
                return buffer.value
            else:
                return ""

                
            
NOTHING = object()
class DDEError(OSError):
    """Exception raise when a DDE error occures."""
    def __init__(self, msg, conv=None, app=None, num=NOTHING):
        self.winerror = 0
        if num == NOTHING and app is not None:
            num = DDE.GetLastError(app)
        elif num == NOTHING and conv is not None:
            num = DDE.GetLastError(conv._idInst)
        if num != NOTHING:
            self.winerror = num
            msg = hex(num) + " " + msg
            # + " " + FormatError(num) windows have no strings about DDE
        if conv is not None:
            msg += " (service=%s, topic=%s)" % (conv.service, conv.topic)
        super(DDEError, self).__init__(msg.encode("utf-8"))

            
            
class DDEClient(UserDict.DictMixin):
    """The DDEClient class.

    Use this class to create and manage DDE conversations with service/topic.
    DDEClient is caching DDE conversations, each idetified by case insensitive service/topic.
    Therefore DDEClient has features of a dictionary:
    
    dde_client = DDEClient()
    # is empty dict
    bool(dde_client)
    > False
    dde_client[("Service","Topic")].execute("This")
    bool(dde_client)
    > True
    print "There are %i ready conversations." % len(dde_client)
    # this always will disconnect irrespective of any other references:
    del dde_client[("service","topic")]
    #or dde_client.clear()
    #or instead - finalize:
    dde_client.shutdown()
    
    There is no need to shutdown() DDEClient on DDE connection errors!
    
    callback -- any function with **kwargs that returns None if not DDE specific.
        Generally in it you want to check what type==XTYP_* you were waiting for bringing what: str1,2,data...
        For details look at the source of DDEClient._callback() for intel dict.
        For the asynchronous DDE conversations you are interested in XTYP_ADVDATA and XTYP_XACT_COMPLETE,
        later brings id you've got returned from calling request(), etc.
        
        Search DDE documentation on MS website by:
        Desktop technologies > Desktop App UI > Data Exchange > /or maybe/ Interprocess communications >
        Dynamic Data Exchange Management Library >
        DDEML Reference >
        DDEML Transactions > XTYP_XACT_COMPLETE /and/ DDEML Functions > DdeCallback
        
        DDE client deals with at most 6 XTYPs:
        XTYP_ERROR        
        XTYP_REGISTER     
        XTYP_DISCONNECT   
        XTYP_UNREGISTER   
        XTYP_ADVDATA      
        XTYP_XACT_COMPLETE
    
    flags -- default and highly recommended is APPCMD_CLIENTONLY.
        Add CBF_SKIP_ALLNOTIFICATIONS to cut in half the number of XTYPs for callback.
    """

    def __init__(self, callback=None, flags=APPCMD_CLIENTONLY):
        """Create an instance of DDE application."""
        self._idInst = DWORD(0) # application instance identifier. byref(DWORD(self._idInst))
        self._callback = DDECALLBACK(self._callback)
        self._conversations = dict()
        self.callback = callback
        
        # Initialize and register application with DDEML
        # The DdeInitializeA vs. DdeInitializeW version called determines the type of 
        # the window procedures used to control DDE conversations (ANSI or Unicode).
        res = DDE.Initialize(byref(self._idInst), self._callback, flags, 0)
        if res != DMLERR_NO_ERROR:
            raise DDEError("Unable to register with DDEML.", num=res)

            
    def shutdown(self):
        """Destroy DDE instance with any active connections and free all DDEML resources."""
        if self._idInst:
            self._conversations = None
            # DdeUninitialize terminates any conversations currently open for the application. 
            DDE.Uninitialize(self._idInst)
            self._idInst = None
            self._callback = None
            self.callback = None
    
    
    def __del__(self):
        self.shutdown()
            
            
    def __getitem__(self, key):
        """
        Establish or get established DDE conversation 
        with specific service and topic names provided as in a tuple.
        Do not forget to mark string unicode when name has non ASCII chars.
        """
        K = tuple(["" if s is None else unicode(s).upper() for s in key])
        try:
            return self._conversations[K]
        except(KeyError):
            conversation = DDEConversation(self._idInst, key)
            self._conversations[K] = conversation
            return conversation

            
    def __delitem__(self, key):
        """
        End DDE conversation if found any 
        with specific service and topic names provided as in a tuple.
        Do not forget to mark string unicode when name has non ASCII chars.
        """
        K = tuple(["" if s is None else unicode(s).upper() for s in key])
        try:
            self._conversations[K].__del__()
            del self._conversations[K]
        except(KeyError):
            pass
            
            
    def keys(self):
        return self._conversations.keys() if self._conversations else ()
        
        
    def __str__(self):
        retval = [self.__class__.__name__, "with established conversations:"]
        if self._conversations: 
            for v in self._conversations.values():
                retval.append("(service=%s, topic=%s)" % (v.service, v.topic))
        return " ".join(retval).encode("utf-8")
        
        
    def abandon_transaction(self):
        """Abandon all asynchronous transactions."""
        return DDE.AbandonTransaction(self._idInst, 0, 0)
        
        
    def _callback(self, wType, uFmt, hConv, hsz1, hsz2, hDdeData, dwData1, dwData2):
        """DdeCallback callback function for processing Dynamic Data Exchange (DDE)
        transactions sent by DDEML in response to DDE events.
        
        XTYP_ERROR           = (0x0000 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)
        XTYP_REGISTER        = (0x00A0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK )
        XTYP_DISCONNECT      = (0x00C0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK )
        XTYP_UNREGISTER      = (0x00D0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK )
       
        Client only types:
        XTYP_ADVDATA         = (0x0010 | XCLASS_FLAGS)
        XTYP_XACT_COMPLETE   = (0x0080 | XCLASS_NOTIFICATION )
        
        Server only types, blocked by APPCMD_CLIENTONLY or CBF_FAIL_ALLSVRXACTIONS:
        ?XTYP_ADVREQ          = (0x0020 | XCLASS_DATA | XTYPF_NOBLOCK)
        XTYP_ADVSTART        = (0x0030 | XCLASS_BOOL)
        XTYP_ADVSTOP         = (0x0040 | XCLASS_NOTIFICATION)
        XTYP_EXECUTE         = (0x0050 | XCLASS_FLAGS)
        XTYP_CONNECT         = (0x0060 | XCLASS_BOOL | XTYPF_NOBLOCK)
        ?XTYP_CONNECT_CONFIRM = (0x0070 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)
        XTYP_POKE            = (0x0090 | XCLASS_FLAGS)
        XTYP_REQUEST         = (0x00B0 | XCLASS_DATA )
        XTYP_WILDCONNECT     = (0x00E0 | XCLASS_DATA | XTYPF_NOBLOCK)
        
        Monitor only type:
        XTYP_MONITOR         = (0x00F0 | XCLASS_NOTIFICATION | XTYPF_NOBLOCK)
        
        https://msdn.microsoft.com/en-us/library/windows/desktop/ms648742(v=vs.85).aspx

        Parameters
        ----------
        wType    : transaction type (UINT)
        uFmt     : clipboard data format (UINT)
        hConv    : handle to conversation (HCONV)
        hsz1     : handle to string (HSZ)
        hsz2     : handle to string (HSZ)
        hDDedata : handle to global memory object (HDDEDATA)
        dwData1  : transaction-specific data (DWORD)
        dwData2  : transaction-specific data (DWORD)

        Returns
        -------
        ret      : specific to the type of transaction (wType)
        """
        
        # kwargs for pythonic callback
        intel = dict([
            ("type", wType), 
            ("str1", ""), 
            ("str2", ""), 
            ("format", uFmt), 
            ("data", None), 
            ])
                
        if wType == XTYP_ERROR:
            # Only one meaning - DMLERR_LOW_MEMORY 
            # Memory is low; advise, poke, or execute data may be lost, or the system may fail.
            # Panic only if it is us:
            if hConv:
                for name, conversation in self._conversations.items():
                    if conversation._hConv == hConv:
                        if self.callback:
                            intel["str1"] = conversation.service
                            intel["str2"] = conversation.topic
                        del self._conversations[name]
                        del conversation
                        break
        elif wType == XTYP_DISCONNECT:
            for name, conversation in self._conversations.items():
                if conversation._hConv == hConv:
                    if self.callback:
                        intel["str1"] = conversation.service
                        intel["str2"] = conversation.topic
                    del self._conversations[name]
                    del conversation
                    break
        elif wType in (XTYP_ADVDATA, XTYP_XACT_COMPLETE):  
            # hsz1 = topic; hsz2 = item; hDdeData = data
            if self.callback:
                intel["str1"] = DDE.query_string(self._idInst, hsz1)
                intel["str2"] = DDE.query_string(self._idInst, hsz2)
                if wType == XTYP_XACT_COMPLETE:
                    intel["id"] = dwData1 # unique transaction identifier
                # hDdeData == NULL if advise for XTYP_ADVDATA was with XTYPF_NODATA flag
                # hDdeData == NULL if XTYP_XACT_COMPLETE unsuccessful
                # hDdeData == TRUE if XTYP_XACT_COMPLETE successful but involved no data
                # (data may be received only on advise and request transactions)
                if wType == XTYP_XACT_COMPLETE and hDdeData in (None, 1):
                    intel["data"] = bool(hDdeData)
                elif hDdeData:
                    intel["data"] = DDE.get_data(hDdeData)
                    # An application must not free hDdeData obtained during callback.
        # elif wType in (XTYP_REGISTER, XTYP_UNREGISTER):
            # # hsz1 = handle to the base service name being registered.
            # # hsz2 = handle to the instance-specific service name being registered.
            # if self.callback:
                # intel["str1"] = DDE.query_string(self._idInst, hsz1)
                # intel["str2"] = DDE.query_string(self._idInst, hsz2)
        else:
            # presume that unused DDE parameters always return 0
            if self.callback:
                intel["str1"] = DDE.query_string(self._idInst, hsz1)
                intel["str2"] = DDE.query_string(self._idInst, hsz2)
                
        if self.callback:
            response = self.callback(**intel)
            if response:
                return response
        # return whatever to please DDEML
        xclass = wType & XCLASS_MASK
        # if xclass == XCLASS_BOOL: return False
        # if xclass == XCLASS_DATA: return None
        # if xclass == XCLASS_FLAGS: return DDE_FACK
        # if xclass == XCLASS_NOTIFICATION: return None
        return DDE_FACK if xclass == XCLASS_FLAGS else None
            
            
class DDEConversation(object):
    """The DDEConversation class.

    DDEConversation is used internally in DDEClient class as cached item
    and provides for initiating DDE client transactions.
    Here and by DDE specification service/topic/item names are case insensitive!
    If service or topic name is empty, servers are free to ignore such a wildcard.
    """
    def __init__(self, idInst, key):
        """Create a connection to a service/topic."""
        self._hConv = None
        self._idInst = idInst #weakref.ref(idInst)
        self.service = None
        self.topic = None
        if len(key) >= 1:
            self.service = key[0]
        if len(key) >= 2:
            self.topic = key[1]
        
        hszServName = DDE.CreateStringHandle(self._idInst, self.service, CP_WINUNICODE) if self.service else None
        hszTopic = DDE.CreateStringHandle(self._idInst, self.topic, CP_WINUNICODE) if self.topic else None
        self._hConv = DDE.Connect(self._idInst, hszServName, hszTopic, None)
        if hszTopic: DDE.FreeStringHandle(self._idInst, hszTopic)
        if hszServName: DDE.FreeStringHandle(self._idInst, hszServName)
        if not self._hConv:
            raise DDEError("Unable to establish a conversation with server.", self)

            
    def __del__(self):
        """Conversation ends with disconnect."""
        if self._hConv:
            DDE.Disconnect(self._hConv)
            self._hConv = None
            
            
    def info(self, idTransaction=QID_SYNC):
        ConvInfo = CONVINFO()
        ConvInfo.cb = sizeof(CONVINFO) # maybe windows needs to know the struct version
        if not DDE.QueryConvInfo(self._hConv, idTransaction, byref(ConvInfo)):
            raise DDEError("Unable to get conversation information.", self)
            
        ConvInfo.SvcPartner = DDE.query_string(self._idInst, ConvInfo.hszSvcPartner)
        ConvInfo.ServiceReq = DDE.query_string(self._idInst, ConvInfo.hszServiceReq)
        ConvInfo.Topic = DDE.query_string(self._idInst, ConvInfo.hszTopic)
        ConvInfo.Item = DDE.query_string(self._idInst, ConvInfo.hszItem)
        return ConvInfo

        
    def advise(self, item, stop=False, format=CF_UNICODETEXT, flags=0):
        """
        Request updates when DDE data changes.
        flags choice: XTYPF_NODATA, XTYPF_ACKREQ
        Returns unique transaction identifier.
        """
        hszItem = DDE.CreateStringHandle(self._idInst, item, CP_WINUNICODE)
        pdwResult = DWORD(0)
        hDdeData = DDE.ClientTransaction(None, 0, self._hConv, hszItem, format, (XTYP_ADVSTOP if stop else XTYP_ADVSTART)|flags, TIMEOUT_ASYNC, byref(pdwResult))
        DDE.FreeStringHandle(self._idInst, hszItem)
        if not hDdeData:
            raise DDEError("Unable to %s advise for item=%s." % ("stop" if stop else "start", item), self)
        DDE.FreeDataHandle(hDdeData)
        return pdwResult

        
    def execute(self, data, timeout=5000):
        """Execute a DDE item. Returns unique transaction identifier if made asynchronous."""
        if isinstance(data, basestring):
            data = bytearray(data, "utf-16le")
            if data[-2:] != b'\x00\x00':
                data.extend([0,0])
        cbData = len(data)
        #pData = (c_byte * cbData)(*data)
        pData = (c_byte * cbData).from_buffer(data)
        pdwResult = DWORD(0)
        hDdeData = DDE.ClientTransaction(pData, cbData, self._hConv, None, 0, XTYP_EXECUTE, timeout, byref(pdwResult))
        if not hDdeData:
            raise DDEError("Unable to execute.", self)
        DDE.FreeDataHandle(hDdeData)
        return pdwResult

        
    def request(self, item, timeout=5000, format=CF_UNICODETEXT):
        """Request data from DDE service. Returns unique transaction identifier if made asynchronous."""
        hszItem = DDE.CreateStringHandle(self._idInst, item, CP_WINUNICODE)
        pdwResult = DWORD(0)
        hDdeData = DDE.ClientTransaction(None, 0, self._hConv, hszItem, format, XTYP_REQUEST, timeout, byref(pdwResult))
        DDE.FreeStringHandle(self._idInst, hszItem)
        if not hDdeData:
            raise DDEError("Unable to request item=%s." % item, self)
        data = pdwResult if timeout == TIMEOUT_ASYNC else DDE.get_data(hDdeData)
        DDE.FreeDataHandle(hDdeData)
        return data
    
    
    def poke(self, item, data, timeout=5000, format=CF_UNICODETEXT):
        """Poke (unsolicited) data to DDE server. Returns unique transaction identifier if made asynchronous."""
        hszItem = DDE.CreateStringHandle(self._idInst, item, CP_WINUNICODE)
        # if data is not an array - convert
        if isinstance(data, basestring):
            data = bytearray(data, "utf-16le")
            if data[-2:] != b'\x00\x00':
                data.extend([0,0])
        cbData = len(data)
        #pData = (c_byte * cbData)(*data)
        pData = (c_byte * cbData).from_buffer(data)
        pdwResult = DWORD(0)
        #hData = DDE.CreateDataHandle(self._idInst, pData, cbData, 0, hszItem, format, 0)
        #hDdeData = DDE.ClientTransaction(hData, -1, self._hConv, hszItem, format, XTYP_POKE, timeout, byref(pdwResult))
        hDdeData = DDE.ClientTransaction(pData, cbData, self._hConv, hszItem, format, XTYP_POKE, timeout, byref(pdwResult))
        #DDE.FreeDataHandle(dData)
        DDE.FreeStringHandle(self._idInst, hszItem)
        if not hDdeData:
            raise DDEError("Unable to poke to item=%s." % item, self)
        DDE.FreeDataHandle(hDdeData)
        return pdwResult

        
    def abandon_transaction(self, id=0):
        """Abandon asynchronous transaction. Without id will abandon all pending transactions in the conversation."""
        return DDE.AbandonTransaction(self._idInst, self._hConv, DWORD(id))
    
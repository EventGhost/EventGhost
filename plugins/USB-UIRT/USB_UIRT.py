# 
# To isolate developers from the hardware details and firmware mobility of the
# USB-UIRT, I have developed a driver .dll which presents an easy-to-use API
# to the developer. The API supports reception, transmission, and learning.
# So, all the developer needs to concentrate on is playing back codes passed
# to them during learning. The API also supports Pronto format codes which
# taps into a rather vast database at RemoteCentral.com.
# 
# The API documentation follows:
# 
# ---
# 
# UUIRTDRV_API HUUHANDLE PASCAL UUIRTOpen(void);
# 
# Opens communication with the USB-UIRT. On success, returns a handle to be
# used in subsequent calls to USB-UIRT functions. On failure, returns
# INVALID_HANDLE_VALUE. A call to UUIRTOpen should occur prior to any other
# driver function calls (with the exception of UUIRTGetDrvInfo below).
# 
# 
# UUIRTDRV_API BOOL PASCAL UUIRTClose(HUUHANDLE hHandle);
# 
# Terminates communication with the USB-UIRT. Should be called prior to
# terminating host program.
# 
# 
# UUIRTDRV_API BOOL PASCAL UUIRTGetDrvInfo(unsigned int *puDrvVersion);
# 
# Retrieves information about the *driver* (not the hardware itself). This is
# intended to allow version control on the .DLL driver and accomodate future
# changes and enhancements to the API. Returns TRUE on success, as well as a
# driver version number in *puDrvVersion. NOTE: This call may be called prior
# to a call to UUIRTOpen.
# 
# 
# UUIRTDRV_API BOOL PASCAL UUIRTGetUUIRTInfo(HUUHANDLE hHandle, PUUINFO
# *puuInfo);
# 
# Retrieves information about the UUIRT hardware. On success, returns TRUE and
# fills in the structure PUUINFO, defined as follows:
# 
# typedef struct
# {
# unsigned int fwVersion; // version of firmware residing on the USB-UIRT.
# unsigned int protVersion; // protocol version supported by the USB-UIRT
# firmware.
# unsigned char fwDateDay; // firmware revision date
# unsigned char fwDateMonth; //
# unsigned char fwDateYear; //
# } UUINFO, *PUUINFO;
# 
# 
# UUIRTDRV_API BOOL PASCAL UUIRTGetUUIRTConfig(HUUHANDLE hHandle, PUINT32
# puConfig);
# 
# Retrieves the current feature configuration bits from the USB-UIRT's
# nonvolatile configuration memory. These various configuration bits control
# how the USB-UIRT behaves. Most are reserved for future implementation and
# shout be read and written as Zero. Using this API call is optional and is
# only needed to support changing USB-UIRT's internal 'preferences'. Bits
# defined in uConfig are as follows:
# 
# #define UUIRTDRV_CFG_LEDRX 0x01 // Indicator LED on USB-UIRT blinks when
# remote signals are received
# 
# #define UUIRTDRV_CFG_LEDTX 0x02 // Indicator LED on USB-UIRT lights during
# IR transmission.
# 
# #define UUIRTDRV_CFG_LEGACYRX 0x04 // Generate 'legacy' UIRT-compatible
# codes on receive
# 
# #define RESERVED0 0x08
# 
# #define RESERVED1 0x10
# 
# ...
# 
# UUIRTDRV_API BOOL PASCAL UUIRTSetUUIRTConfig(HUUHANDLE hHandle, UINT32
# uConfig);
# 
# Configures the current feature configuration bits for the USB-UIRT's
# nonvolatile configuration memory. These various configuration bits control
# how the USB-UIRT behaves. See definition of uConfig in UUIRGetUUIRTConfig
# above
# 
# 
# UUIRTDRV_API BOOL PASCAL UUIRTTransmitIR(HUUHANDLE hHandle, char *IRCode,
# int codeFormat, int repeatCount, int inactivityWaitTime, HANDLE hEvent, void
# *reserved0, void *reserved1);
# 
# Transmits an IR code via the USB-UIRT hardware. The IR code is a
# null-terminated *string*. codeFormat is a format specifier which identifies
# the format of the IRCode code. Currently, supported formats are
# Compressed_UIRT (STRUCT), RAW, and Pronto-RAW. RepeatCount indicates how
# many iterations of the code should be sent (in the case of a 2-piece code,
# the first stream is sent once followed by the second stream sent repeatCount
# times). InactivityWaitTime is the time in milliseconds since the last
# received IR activity to wait before sending an IR code -- normally pass 0
# for this parameter. hEvent is an optional event handle which is obtained by
# a call to CreateEvent. If hEvent is NULL, the call to UUIRTTransmitIR will
# block and not return until the IR code has been fully transmitted to the
# air. If hEvent is not NULL, it must be a valid Windows event hande. In this
# case, UUIRTTransmitIR will return immediately and when the IR stream has
# completed transmission this event will be signalled by the driver. The last
# parameters, labelled 'reservedx' are for future expansion and should be
# NULL.
# 
# 
# UUIRTDRV_API BOOL PASCAL UUIRTLearnIR(HUUHANDLE hHandle, int codeFormat,
# char *IRCode, PLEARNCALLBACKPROC progressProc, void *userData, BOOL *pAbort,
# unsigned int param1, void *reserved0, void *reserved1);
# 
# Instructs the USB-UIRT and the API to learn an IR code. The IR code learned
# will be a complete IR stream suitable for subsequent transmission via
# UUIRTTransmitIR. Consequently, the same formats supported by Transmit are
# also available for learn. It is recommended to use either RAW or Pronto-RAW
# codeFormat to offer the best compatibility; compressed-UIRT format is often
# too limiting, although it does produce the smallest codes. IRCode will be
# filled with the learned IR code upon return -- it is the responsibility of
# the caller to allocate space for this string -- suggested string size is at
# least 2048 bytes. ProgressProc is a caller-supplied callback function which
# will be called periodically during the learn process and may be used to
# update user dialogs, etc. Information passed to the callback are learn
# progress %, signal quality, and carrier frequency. The parameter userData
# will be passed by the USB-UIRT driver to any calls of progressProc. The
# pAbort parameter should pass the pointer to a Boolean variable which should
# be initialized to FALSE (0) prior to the call. Setting this variable TRUE
# during the learn process will cause the UUIRTLearnIR process to abort and
# the function to return. Since the UUIRTLearnIR function will block for the
# duration of the learn process, one could set the *pAbort to TRUE either
# within the callback function or from another thread. Param1 is currently
# used only when the codeFormat includes the UUIRTDRV_IRFMT_LEARN_FORCEFREQ
# flag (not normally needed) -- in which case param1 should indicate the
# forced carrier frequency. The last parameters, labelled 'reservedx' are for
# future expansion and should be NULL.
# 
# 
# UUIRTDRV_API BOOL PASCAL UUIRTSetReceiveCallback(HUUHANDLE hHandle,
# PUUCALLBACKPROC receiveProc, void *userData);
# 
# Registers a receive callback function which the driver will call when an IR
# code is received from the air. receiveProc should contain the address of a
# PUUCALLBACKPROC function defined as:
# 
# typedef void (WINAPI *PUUCALLBACKPROC) (char *IREventStr, void *userData);
# 
# When the USB-UIRT receives a code from the air, it will call the callback
# function with a null-terminated, twelve-character (like IRMAN) ir code in
# IREventStr. The driver will also pass the parameter userData, which is a
# general-purpose 32-bit value supplied by the caller to
# UUIRTSetReceiveCallback. This parameter is useful for carrying context
# information, etc. Note that the types of codes which are passed to
# IREventStr are *not* the same as the type of codes passed back from a
# UUIRTLearnIR call (the codes from a UUIRTLearnIR are much larger and contain
# all the necessary data to reproduce a code, whereas the codes passed to
# IREventStr are simpler representations of IR codes only long enough to be
# unique).

from ctypes import *
from win32api import GetLastError
from win32file import INVALID_HANDLE_VALUE
import datetime
import thread
import threading

UINT32 = c_uint

class UUINFO(Structure):
    _fields_ = (
        ('fwVersion',   c_uint),
        ('protVersion', c_uint),
        ('fwDateDay',   c_ubyte),
        ('fwDateMonth', c_ubyte),
        ('fwDateYear',  c_ubyte),
    )
PUUINFO = POINTER(UUINFO)

UUIRTDRV_ERR_NO_DEVICE = 0x20000001
UUIRTDRV_ERR_NO_RESP = 0x20000002
UUIRTDRV_ERR_NO_DLL = 0x20000003
UUIRTDRV_ERR_VERSION = 0x20000004

UUIRTDRV_CFG_LEDRX = 0x0001
UUIRTDRV_CFG_LEDTX = 0x0002
UUIRTDRV_CFG_LEGACYRX = 0x0004

UUIRTDRV_IRFMT_UUIRT = 0x0000
UUIRTDRV_IRFMT_PRONTO = 0x0010

UUIRTDRV_IRFMT_LEARN_FORCERAW = 0x0100
UUIRTDRV_IRFMT_LEARN_FORCESTRUC	= 0x0200
UUIRTDRV_IRFMT_LEARN_FORCEFREQ = 0x0400
UUIRTDRV_IRFMT_LEARN_FREQDETECT	= 0x0800

UUCALLBACKPROC = WINFUNCTYPE(c_int, c_char_p, c_void_p)
LEARNCALLBACKPROC = WINFUNCTYPE(c_int, c_uint, c_uint, c_ulong, c_void_p)


class UUIRTError(Exception):
    pass



class USB_UIRT:
    
    def __init__(self):
        self.learnThread = None
        self.learnThreadAbortEvent = threading.Event()
        self.learnThreadAbortEvent.set()
        self.bAbortLearn = c_int(0)
        self.codeFormat = UUIRTDRV_IRFMT_PRONTO
        try:
            dll = WinDLL('uuirtdrv')
        except:
            raise UUIRTError(
                "Unable to load uuirtdrv.dll!\n"
                "Please make sure driver is installed!"
            )
        puDrvVersion = c_uint(0)
        if not dll.UUIRTGetDrvInfo(byref(puDrvVersion)):
            raise UUIRTError("Unable to retrieve uuirtdrv version!")
        if puDrvVersion.value != 0x0100:
            raise UUIRTError("Invalid uuirtdrv version!")

        hDrvHandle = dll.UUIRTOpen()
        if hDrvHandle == INVALID_HANDLE_VALUE:
            err = GetLastError()
            if err == UUIRTDRV_ERR_NO_DLL:
                raise UUIRTError("Unable to find USB-UIRT Driver. Please "\
                    "make sure driver is Installed!")
            elif err == UUIRTDRV_ERR_NO_DEVICE:
                raise UUIRTError("Unable to connect to USB-UIRT device! Please ensure device is connected to the computer!")
            elif err == UUIRTDRV_ERR_NO_RESP:
                raise UUIRTError("Unable to communicate with USB-UIRT device! Please check connections and try again. If you still have problems, try unplugging and reconnecting your USB-UIRT. If problem persists, contact Technical Support!")
            else:
                raise UUIRTError("Unable to initialize USB-UIRT (unknown error)!")
        self.hDrvHandle = hDrvHandle

        puuInfo = UUINFO()
        if not dll.UUIRTGetUUIRTInfo(hDrvHandle, byref(puuInfo)):
            raise UUIRTError("Error calling UUIRTGetUUIRTInfo")
        self.firmwareVersion = str(puuInfo.fwVersion >> 8) + '.' + str(puuInfo.fwVersion & 0xFF)
        self.protocolVersion = str(puuInfo.protVersion >> 8) + '.' + str(puuInfo.protVersion & 0xFF)
        self.firmwareDate = datetime.date(
            puuInfo.fwDateYear+2000,
            puuInfo.fwDateMonth, 
            puuInfo.fwDateDay
        )
        self.dll = dll


    def GetConfig(self):
        puConfig = UINT32()
        if not self.dll.UUIRTGetUUIRTConfig(self.hDrvHandle, byref(puConfig)):
            raise UUIRTError("Error calling UUIRTGetUUIRTConfig")
        return (
            bool(puConfig.value & UUIRTDRV_CFG_LEDRX),
            bool(puConfig.value & UUIRTDRV_CFG_LEDTX),
            bool(puConfig.value & UUIRTDRV_CFG_LEGACYRX)
        )


    def SetConfig(self, ledRX, ledTX, legacyRX, repeatStopCodes=False):
        value = 0
        if ledRX:
            value |= UUIRTDRV_CFG_LEDRX
        if ledTX:
            value |= UUIRTDRV_CFG_LEDTX
        if legacyRX:
            value |= UUIRTDRV_CFG_LEGACYRX
        if repeatStopCodes:
            value |= 16
        if not self.dll.UUIRTSetUUIRTConfig(self.hDrvHandle, UINT32(value)):
            raise UUIRTError("Error calling UUIRTSetUUIRTConfig")
        
        
    def _receiveCallback(self, IREventStr, userdata):
        self.receiveCallback(IREventStr)
        return 0
        
        
    def SetReceiveCallback(self, receiveCallback):
        """
        Registers a receive callback function which the driver will call when 
        an IR code is received from the air.
        When the USB-UIRT receives a code from the air, it will call the 
        callback function with a twelve-character (like IRMAN) ir code in
        the first parameter. 
        Note that the types of codes which are passed to the callback
        are *not* the same as the type of codes passed back from a
        LearnIR call (the codes from a LearnIR are much larger and contain
        all the necessary data to reproduce a code, whereas the codes passed to
        the callback are simpler representations of IR codes only long enough 
        to be unique).
        """
        self.receiveCallback = receiveCallback
        self.receiveProc = UUCALLBACKPROC(self._receiveCallback)
        if not self.dll.UUIRTSetReceiveCallback(self.hDrvHandle, self.receiveProc, 0):
            raise UUIRTError("Error calling UUIRTSetReceiveCallback")
        
        
    def Close(self):
        """
        Terminates communication with the USB-UIRT. Should be called prior to
        terminating host program.
        """
        if not self.dll.UUIRTClose(self.hDrvHandle):
            raise UUIRTError("Error calling UUIRTClose")
        
        
    def SetRawMode(self, flag=True):
        if flag:
            self.codeFormat = UUIRTDRV_IRFMT_LEARN_FORCERAW
        else:
            self.codeFormat = UUIRTDRV_IRFMT_PRONTO
        
        
    def LearnThread(self, progressFunc):
        IRLearnCallback = LEARNCALLBACKPROC(progressFunc)
        learnBuffer = create_string_buffer('\000' * 2048)
        self.dll.UUIRTLearnIR(  
            self.hDrvHandle,            # hHandle
            self.codeFormat,            # codeFormat
            learnBuffer,                # IRCode buffer
            IRLearnCallback,            # progressProc
            0x5a5a5a5a,                 # userData
            byref(self.bAbortLearn),    # *pAbort
            0,                          # param1
            0,                          # reserved0
            0                           # reserved1
        )
        if self.bAbortLearn.value != 1 and self.succesFunc:
            self.succesFunc(learnBuffer.value)
        self.learnThreadAbortEvent.set()
        
        
    def StartLearnIR(self, progressFunc=None, succesFunc=None):
        self.succesFunc = succesFunc
        self.bAbortLearn.value = False
        self.learnThreadAbortEvent.clear()
        self.learnThread = thread.start_new_thread(
            self.LearnThread, 
            (progressFunc,)
        )
        
        
    def AbortLearnThread(self):
        self.bAbortLearn.value = True
        
        
    def AbortLearnThreadWait(self):
        self.bAbortLearn.value = True
        self.learnThreadAbortEvent.wait(10)
        
        
    def AcceptBurst(self):
        self.bAbortLearn.value = -1
        
        
    def TransmitIR(self, code, repeatCount=1, inactivityWaitTime=0):
        if len(code) > 5:
            start = 0
            if code[0] == "Z":
                start = 2
            if code[start+3] == "R":
                codeFormat = UUIRTDRV_IRFMT_UUIRT
            elif code[start+4] == " ":
                codeFormat = UUIRTDRV_IRFMT_PRONTO
            else:
                codeFormat = UUIRTDRV_IRFMT_LEARN_FORCESTRUC
        else:
            repeatCount = 0
            codeFormat = UUIRTDRV_IRFMT_PRONTO
            code = ""
        if not self.dll.UUIRTTransmitIR(
            self.hDrvHandle,    # hHandle
            c_char_p(code),     # IRCode
            codeFormat,         # codeFormat
            repeatCount,        # repeatCount
            inactivityWaitTime, # inactivityWaitTime
            0,                  # hEvent
            0,                  # reserved1
            0                   # reserved2
        ):
            raise UUIRTError("Error calling UUIRTTransmitIR")
        


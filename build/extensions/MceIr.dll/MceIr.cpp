// MceIr.cpp : Defines the entry point for the DLL application.
//

#include "stdafx.h"
#include <winioctl.h>
#include "MceIrDrv.h"
#include "MceIr.h"
#include "IrDec.h"

#if _DEBUG
#define Trace TraceOut
#define Debug TraceOut
#define DebugIoControl TraceOut
#else
#define Trace
#define Debug
#define DebugIoControl
#endif

#define BULK_INPUT_PIPE   "Pipe01"
#define BULK_OUTPUT_PIPE  "Pipe00"

#define IRBUS_PIPE        "Pipe01"

#define PRONTO_PROTO_RC5  0x5000
#define PRONTO_PROTO_RC5X 0x5001
#define PRONTO_PROTO_RC6  0x6000
#define PRONTO_PROTO_RC6A 0x6001

#define BIT_SET(a, b)     (a) |= (1 << (b))
#define BIT_TEST(a, b)    ((a) & (1 << (b)))

#define EVENT_READ        (WAIT_OBJECT_0)
#define EVENT_WRITE       (WAIT_OBJECT_0 + 1)
#define EVENT_RECORD      (WAIT_OBJECT_0 + 2)
#define EVENT_PLAY        (WAIT_OBJECT_0 + 3)
#define EVENT_TERMINATE   (WAIT_OBJECT_0 + 4)

typedef struct {
    /// Last packet in block?
    int DataEnd;
    /// Number of bytes in block.
    int ByteCount;
    /// Carrier frequency of IR received.
    int CarrierFrequency;
} ReceiveParams, *ReceiveParamsPtr;

typedef struct {
    /// Index of the receiver to use.
    int Receiver;
    /// Receive timeout, in milliseconds.
    int Timeout;
} StartReceiveParams, *StartReceiveParamsPtr;

typedef struct {
    /// Device protocol version.
    int ProtocolVersion;
    /// Number of transmit ports – 0-32.
    int TransmitPorts;
    /// Number of receive ports – 0-32. For beanbag, this is two (one for learning, one for normal receiving).
    int ReceivePorts;
    /// Bitmask identifying which receivers are learning receivers – low bit is the first receiver, second-low bit is the second receiver, etc ...
    int LearningMask;
    /// Device flags.
    int DetailsFlags;
} MCEDeviceCapabilities, *MCEDeviceCapabilitiesPtr;

typedef enum
{
    /// Start receiving IR.
    IoCtrl_StartReceive  = 0x0F608028,
    /// Stop receiving IR.
    IoCtrl_StopReceive   = 0x0F60802C,
    /// Get IR device details.
    IoCtrl_GetDetails    = 0x0F604004,
    /// Get IR blasters
    IoCtrl_GetBlasters   = 0x0F604008,
    /// Receive IR.
    IoCtrl_Receive       = 0x0F604022,
    /// Transmit IR.
    IoCtrl_Transmit      = 0x0F608015,
}  IoCtrl;

// Global variables
HINSTANCE hInstance;
DWORD     KbdFirstRepeat  = 750;
DWORD     KbdNextRepeats  = 150;
HWND      hWndRegistered  = NULL;
DWORD     Blaster         = BLASTER_BOTH;
DWORD     BlasterSpeed    = SPEED_NONE;
DWORD     BlasterType     = TYPE_MICROSOFT;

//Local functions
static void         MceIrOpenPipes          ();
static BOOL         MceIrGetDeviceFileName  (LPGUID  pGuid, char *outNameBuf);
static HANDLE       MceIrOpenUsbDevice      (LPGUID  pGuid, char *outNameBuf);
static DWORD WINAPI MceIrXpThreadProc       (LPVOID lpParameter);
static DWORD WINAPI MceIrVistaThreadProc    (LPVOID lpParameter);
static BOOL         MceIrReadFile           (HANDLE hPlay, PUCHAR *pBuffer, PULONG Read);

//Local variables
static HANDLE hTraceMutex   = INVALID_HANDLE_VALUE;
static HANDLE hThread       = INVALID_HANDLE_VALUE;
static HANDLE hThreadEvent  = INVALID_HANDLE_VALUE;
static HANDLE hReadPipe     = INVALID_HANDLE_VALUE;
static HANDLE hWritePipe    = INVALID_HANDLE_VALUE;
static HANDLE hRecord       = INVALID_HANDLE_VALUE;
static HANDLE hPlay         = INVALID_HANDLE_VALUE;

static HANDLE hRecordEvent  = INVALID_HANDLE_VALUE;
static HANDLE hRecordDone   = INVALID_HANDLE_VALUE;
static HANDLE hPlayEvent    = INVALID_HANDLE_VALUE;
static HANDLE hPlayDone     = INVALID_HANDLE_VALUE;
static DWORD  RecordTimeout;

static BOOL   IsPlaying     = FALSE;

static BOOL   probablyVista = FALSE;
static BOOL   VistaThreadStop;
static int    PacketTimeout = 100;
static int   _numTxPorts;
static int   _txPortMask;
static int   _learnPortMask;
static int   _receivePort;
static int   _learnPort;

BOOL APIENTRY DllMain(HINSTANCE hModule, DWORD  Reason, LPVOID lpReserved)
{
    switch (Reason)
    {
    case DLL_PROCESS_ATTACH:
        hTraceMutex = CreateMutex(NULL, FALSE, NULL);
        hInstance = hModule;
        hThreadEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
        hRecordEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
        hRecordDone = CreateEvent(NULL, FALSE, FALSE, NULL);
        hPlayEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
        hPlayDone = CreateEvent(NULL, FALSE, FALSE, NULL);
        MceIrResume();
        break;

    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
        break;

    case DLL_PROCESS_DETACH:
        MceIrSuspend();

        CloseHandle(hThreadEvent);
        CloseHandle(hRecordEvent);
        CloseHandle(hRecordDone);
        CloseHandle(hPlayEvent);
        CloseHandle(hPlayDone);

        if (hTraceMutex != INVALID_HANDLE_VALUE)
        {
            CloseHandle(hTraceMutex);
            hTraceMutex = INVALID_HANDLE_VALUE;
        }
        break;
    }

    return TRUE;
}

static int FirstHighBit(int mask)
{
    for (int i = 0; i < 32; i++)
        if ((mask & (1 << i)) != 0)
            return i;

    return -1;
}
static int FirstLowBit(int mask)
{
    for (int i = 0; i < 32; i++)
        if ((mask & (1 << i)) == 0)
            return i;

    return -1;
}

bool IoControl(IoCtrl ioControlCode, int *inBuffer, int inBufferSize, int *outBuffer, int outBufferSize, LPDWORD bytesReturned)
{
    OVERLAPPED overlapped;
    BOOL deviceIoControl;
    int ret;

    DebugIoControl("IoControl ENTER\n");
    if (hReadPipe == INVALID_HANDLE_VALUE)
        return false;

    DebugIoControl("IoControl: hReadPipe is valid\n");

    memset(&overlapped, 0, sizeof(overlapped));
    overlapped.hEvent = CreateEvent(NULL, // No security attribute
                                      TRUE, // Manual reset
                                      FALSE, // Initial state = nonsignaled
                                      NULL); // No name
    if (!overlapped.hEvent)
        return false;
    DebugIoControl("IoControl: Event created successfully\n");


    // Send a control code directly to my device driver
    deviceIoControl = DeviceIoControl(hReadPipe,
                                      ioControlCode,
                                      inBuffer,
                                      inBufferSize, 
                                      outBuffer, 
                                      outBufferSize, 
                                      bytesReturned, 
                                      (LPOVERLAPPED)&overlapped);
    DebugIoControl("IoControl: after calling DeviceIoControl(), returned=%d\n", deviceIoControl);
    if (deviceIoControl == FALSE)
    {
        DebugIoControl("IoControl: deviceIoControl == FALSE\n");
        if  (GetLastError() != ERROR_IO_PENDING)
        {
            DebugIoControl("IoControl: GetLastError() != ERROR_IO_PENDING\n");
            CancelIo(hReadPipe);
            CloseHandle(overlapped.hEvent);
            return false;
        }
        // Wait for event
        DebugIoControl("IoControl: about to wait for the event...\n");
        if (WaitForSingleObject(overlapped.hEvent, INFINITE) == WAIT_FAILED)
        {
            DebugIoControl("IoControl: WaitForSingleObject failed\n");
            CancelIo(hReadPipe);
            CloseHandle(overlapped.hEvent);
            return false;
        }
        ret = GetOverlappedResult(hReadPipe, (LPOVERLAPPED)&overlapped, bytesReturned, false);
        if (ret = 0)
            DebugIoControl("IoControl: GetOverlappedResult FAILED: error=0x%x\n", GetLastError());
        DebugIoControl("IoControl: bytesReturned=%d\n", *bytesReturned);
    }
    DebugIoControl("IoControl EXIT\n");
    CloseHandle(overlapped.hEvent);
    return true;
}

static void VistaStartReceive(int receivePort, int timeout)
{
    int bytesRead;
    StartReceiveParams parms;

    parms.Receiver = receivePort;
    parms.Timeout = timeout;
    if (!IoControl(IoCtrl_StartReceive, (int *)&parms, sizeof(parms), NULL, 0, (LPDWORD)&bytesRead))
    {
        Trace("VistaStartReceive(port=%d, timeout=%d) failed\n", receivePort, timeout);
    }
}

static void VistaStopReceive(void)
{
    int bytesRead;
    if (!IoControl(IoCtrl_StopReceive, NULL, 0, NULL, 0, (LPDWORD)&bytesRead))
    {
        Trace("IoCtrl_StopReceive() failed\n");
    }
}

bool VistaGetDeviceCapabilities(void)
{
    int bytesReturned;
    MCEDeviceCapabilities parms;

    Trace("VistaGetDeviceCapabilities() ENTER\n");

    if (!IoControl(IoCtrl_GetDetails, NULL, 0, (int *)&parms, sizeof(parms), (LPDWORD)&bytesReturned))
    {
        Trace("VistaGetDeviceCapabilities(),  IoControl failed\n");
        return false;
    }

    if (bytesReturned < sizeof(parms))
    {
        Trace("VistaGetDeviceCapabilities(), IoControl returned not enough bytes\n");
        return false;
    }

    _numTxPorts = parms.TransmitPorts;
    //_numRxPorts = parms.ReceivePorts;
    _learnPortMask = parms.LearningMask;

    int receivePort = FirstLowBit(_learnPortMask);
    if (receivePort != -1)
        _receivePort = receivePort;

    int learnPort = FirstHighBit(_learnPortMask);
    if (learnPort != -1)
        _learnPort = learnPort;
    else
        _learnPort = _receivePort;

    //DeviceCapabilityFlags flags = (DeviceCapabilityFlags)*parms.DetailsFlags;
    //_legacyDevice = (int)(flags & DeviceCapabilityFlags.Legacy) != 0;
    //_canFlashLed = (int)(flags & DeviceCapabilityFlags.FlashLed) != 0;

    Trace("Device Capabilities:\n");
    Trace("NumTxPorts: %d\n", _numTxPorts);
    Trace("NumRxPorts: %d\n", parms.ReceivePorts);
    Trace("LearnPortMask: 0x%x\n", _learnPortMask);
    Trace("ReceivePort: %d\n", _receivePort);
    Trace("LearnPort: %d\n", _learnPort);
    Trace("DetailsFlags: 0x%x\n", parms.DetailsFlags);
    return true;
}

BOOL WINAPI MceIrSuspend()
{
    Trace("MceIrSuspend\n");

    if (probablyVista)
    {
        VistaStopReceive();
        VistaThreadStop = true;
    }
    else
    {
        if (hThread != INVALID_HANDLE_VALUE)
        {
            SetEvent(hThreadEvent);

            if (WaitForSingleObject(hThread, 1000L) != WAIT_OBJECT_0)
            {
                TerminateThread(hThread, 0); //Be zen...
            }

            CloseHandle(hThread);
            hThread = INVALID_HANDLE_VALUE;
        }

        ResetEvent(hThreadEvent);
    }

    return TRUE;
}

BOOL WINAPI MceIrResume()
{
    DWORD ThreadId;

    Trace("MceIrResume\n");

    if (hThread == INVALID_HANDLE_VALUE)
    {
        MceIrOpenPipes();
        if (probablyVista)
        {
            VistaGetDeviceCapabilities();
            VistaStartReceive(_receivePort, PacketTimeout);
            hThread = CreateThread(NULL, 0, MceIrVistaThreadProc, NULL, 0, &ThreadId);
        }
        else
        {
            hThread = CreateThread(NULL, 0, MceIrXpThreadProc, NULL, 0, &ThreadId);
        }
        SetThreadPriority(hThread, THREAD_PRIORITY_NORMAL);
    }

    return TRUE;
}

BOOL WINAPI MceIrRegisterEvents(HWND hWnd)
{
    BOOL Result = FALSE;

    Trace("MceIrRegisterEvents %08X\n", hWnd);

    if ((hWnd == INVALID_HANDLE_VALUE) || !IsWindow(hWnd))
    {
        Trace("Invalid window handle\n");
    }
    else if (hWndRegistered)
    {
        Trace("Already registered !\n");
    }
    else
    {
        hWndRegistered = hWnd;
        Result = TRUE;
    }

    return Result;
}

BOOL WINAPI MceIrUnregisterEvents()
{
    BOOL Result = FALSE;

    Trace("MceIrUnregisterEvents\n");

    if (!hWndRegistered)
    {
        Trace("Nothing registered yet\n");
    }
    else
    {
        hWndRegistered = NULL;
        Result = TRUE;
    }

    return Result;
}

BOOL WINAPI MceIrSetRepeatTimes(DWORD FirstRepeat, DWORD NextRepeats)
{
    Trace("MceIrSetRepeatTimes\n");

    KbdFirstRepeat = FirstRepeat;
    KbdNextRepeats = NextRepeats;

    return TRUE;
}

BOOL WINAPI MceIrPlaybackFromFile(HANDLE hFile)
{
    BOOL Result = FALSE;

    Trace("MceIrPlaybackFromFile\n");

    if (hFile == INVALID_HANDLE_VALUE)
    {
        Trace("Invalid file handle\n");
    }
    else if (hWritePipe == INVALID_HANDLE_VALUE)
    {
        Trace("Device unavailable\n");
    }
    else if (IsPlaying)
    {
        Trace("Already playing\n");
    }
    else
    {
        hPlay = hFile;
        ResetEvent(hPlayDone);
        SetEvent(hPlayEvent);

        if (WaitForSingleObject(hPlayDone, 10000L) != WAIT_OBJECT_0)
        {
            Trace("Error during play\n");
        }
        else
        {
            Result = TRUE;
            // Sleep(250); // Added 250 ms sleep to allow time for IR to blast
            Debug("Played successfully !\n");
        }
    }

    return Result;
}

BOOL WINAPI MceIrRecordToFile(HANDLE hFile, DWORD Timeout)
{
    BOOL Result = FALSE;

    // Learn init ...
    // UCHAR[4] packet1 = new UCHAR[] { 0x9F, 0x0C, 0x0F, 0xA0 };
    // UCHAR[3] packet2 = new UCHAR[] { 0x9F, 0x14, 0x01 };
    // DWORD BytesWritten;
    // OVERLAPPED OvlWrite;
    // OvlWrite.hEvent = hWriteEvent;
    // OvlWrite.Offset = 0;
    // OvlWrite.OffsetHigh = 0;
    // WriteFile(hWritePipe, packet1, 4, &BytesWritten, &OvlWrite)
    // WriteFile(hWritePipe, packet2, 3, &BytesWritten, &OvlWrite)

    Trace("MceIrRecordToFile\n");

    if (hFile == INVALID_HANDLE_VALUE)
    {
        Trace("Invalid file handle\n");
    }
    else if (hReadPipe == INVALID_HANDLE_VALUE)
    {
        Trace("Device unavailable\n");
    }
    else if (hRecord != INVALID_HANDLE_VALUE)
    {
        Trace("Already recording\n");
    }
    else
    {
        RecordTimeout = Timeout;
        hRecord = hFile;
        ResetEvent(hRecordDone);
        SetEvent(hRecordEvent);

        if (WaitForSingleObject(hRecordDone, 30000L + Timeout) != WAIT_OBJECT_0)
        {
            Trace("Error during record\n");
        }
        else
        {
            Result = TRUE;

            Debug("Recorded successfully !\n");
        }

        hRecord = INVALID_HANDLE_VALUE;
    }

    return Result;
}

BOOL WINAPI MceIrCheckFile(HANDLE hFile)
{
    BOOL Result = FALSE;
    PUCHAR poutBuf = NULL;
    DWORD BytesFile;

    Trace("MceIrCheckFile\n");

    if (hFile == INVALID_HANDLE_VALUE)
    {
        Trace("Invalid file handle\n");
    }
    else
    {
        Result = MceIrReadFile(hFile, &poutBuf, &BytesFile);

        if (poutBuf)
            HeapFree(GetProcessHeap(), 0, poutBuf);
    }

    return Result;
}

BOOL WINAPI MceIrSelectBlaster(DWORD Port)
{
    BOOL Result = FALSE;

    Trace("MceIrSelectBlaster\n");

    switch(Port)
    {
    case BLASTER_1:
    case BLASTER_2:
    case BLASTER_BOTH:
        Blaster = Port;
        Result = TRUE;
        break;
    }

    return Result;
}

BOOL WINAPI MceIrSetBlasterSpeed(DWORD Speed)
{
    BOOL Result = FALSE;

    Trace("MceIrSetBlasterSpeed\n");

    switch (Speed)
    {
    case SPEED_FAST:
    case SPEED_MEDIUM:
    case SPEED_SLOW:
    case SPEED_NONE:
        BlasterSpeed = Speed;
        Result = TRUE;
        break;
    }

    return Result;
}

BOOL WINAPI MceIrSetBlasterType(DWORD Type)
{
    BOOL Result = FALSE;

    Trace("MceIrSetBlasterType\n");

    switch (Type)
    {
    case TYPE_MICROSOFT:
    case TYPE_SMK:
        BlasterType = Type;
        Result = TRUE;
        break;
    }

    return Result;
}


static DWORD WINAPI MceIrXpThreadProc(LPVOID lpParameter)
{
    HANDLE hReadEvent = INVALID_HANDLE_VALUE;
    HANDLE hWriteEvent = INVALID_HANDLE_VALUE;
    HANDLE hEvents[5];
    UCHAR pinBuf[256], *poutBuf = NULL;
    DWORD BytesRead, BytesWritten, Retcode;
    DWORD IdleTimeout = 0, RecTimeout = 0, PlayDelay = 0;
    OVERLAPPED OvlRead, OvlWrite;
    BOOL IsReading = FALSE, IsWriting = FALSE;
    BOOL Running = TRUE;
    UCHAR *pByte, BufPos = 0;

    hReadEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
    hWriteEvent = CreateEvent(NULL, FALSE, FALSE, NULL);

    hEvents[0] = hReadEvent;
    hEvents[1] = hWriteEvent;
    hEvents[2] = hRecordEvent;
    hEvents[3] = hPlayEvent;
    hEvents[4] = hThreadEvent;

    memset(&OvlRead, 0, sizeof(OvlRead));
    OvlRead.hEvent = hReadEvent;

    while (Running)
    {
        while(hReadPipe == INVALID_HANDLE_VALUE)
        {
            MceIrOpenPipes();
            if (hReadPipe != INVALID_HANDLE_VALUE)
            {
                IsReading = FALSE;
                IsWriting = FALSE;
            }

            if (WaitForSingleObject(hThreadEvent, 1000L) == WAIT_OBJECT_0)
            {
                Running = FALSE;
                break;
            }
        }
        if (Running == FALSE)
            break;

        Retcode = WAIT_FAILED;

        if (!IsReading)
        {
#if 0
{
    int i;
    for (i = BufPos; i < 32; i++) {
        pinBuf[i] = 0;
    }
}
Debug("Calling ReadFile()... BufPos=%d, BytesRead=%d\n", BufPos);
#endif
    if (ReadFile(hReadPipe, pinBuf + BufPos, sizeof(pinBuf), &BytesRead, &OvlRead))
            {
#if 0
{
    char tmp[512];
    int i;
    Debug("%s\n", "ReadFile!!!!!!!!!!!!!!!!!!!!!!!!!!");
    tmp[0] = '\0';
    for (i = 0; i < BytesRead; i++) {
        sprintf(tmp + strlen(tmp), "%02x ", pinBuf + BufPos + i);
    }
    Debug("%s\n", tmp);
}
#endif
                Retcode = EVENT_READ;
                BytesRead += BufPos;
            }
            else if (GetLastError() != ERROR_IO_PENDING)
            {
                Trace("Read error %d !\n", GetLastError());
                CancelIo(hReadPipe);
                CancelIo(hWritePipe);
                CloseHandle(hReadPipe);
                CloseHandle(hWritePipe);
                hReadPipe = INVALID_HANDLE_VALUE;
                hWritePipe = INVALID_HANDLE_VALUE;
                continue;
            }
            else
            {
                IsReading = TRUE;
            }
        }

        if (IsPlaying && !IsWriting && (PlayDelay < GetTickCount()))
        {
            DWORD BytesFile;
            IsWriting = FALSE;
            if (!MceIrReadFile(hPlay, &poutBuf, &BytesFile))
            {
                IsPlaying = FALSE;
                BytesFile = 0;
                Trace("Error %d reading file\n", GetLastError());
            }

            OvlWrite.hEvent = hWriteEvent;
            OvlWrite.Offset = 0;
            OvlWrite.OffsetHigh = 0;

            if ((BytesFile == 0) || (WriteFile(hWritePipe, poutBuf, BytesFile, &BytesWritten, &OvlWrite)))
            {
                Retcode = EVENT_WRITE;
            }
            else if (GetLastError() != ERROR_IO_PENDING)
            {
                Trace("Write error %d !\n", GetLastError());
                IsWriting = TRUE;
                Retcode = WAIT_TIMEOUT;
            }
            else
            {
                IsWriting = TRUE;
            }
        }

        if ((IsReading || IsWriting) && (Retcode == WAIT_FAILED))
        {
            switch(Retcode = WaitForMultipleObjects(5, hEvents, FALSE, 100L))
            {
            case EVENT_READ:
                GetOverlappedResult(hReadPipe, &OvlRead, &BytesRead, FALSE);
                BytesRead += BufPos;
                break;

            case EVENT_WRITE:
                GetOverlappedResult(hWritePipe, &OvlWrite, &BytesWritten, FALSE);
                break;
            }
        }

        if ((RecTimeout) && (hRecord != INVALID_HANDLE_VALUE))
        {
            if (GetTickCount() > RecTimeout)
            {
                Trace("Record timed out !\n");
                hRecord = INVALID_HANDLE_VALUE;
                SetEvent(hRecordDone);
            }
        }

        switch(Retcode)
        {
        case WAIT_TIMEOUT:
            MceIrDecode(NULL, 0);
            PlayDelay = 0;
            if (IdleTimeout > 100L)
            {
                IdleTimeout -= 100L;
            }
            else if (IdleTimeout)
            {
                Debug("WAIT KEY !\n");
                IdleTimeout = 0L;
                RecTimeout = GetTickCount() + RecordTimeout;
            }
            break;

        case EVENT_READ:
            Debug("READ! %d bytes\n", BytesRead);
            IsReading = FALSE;
            pByte = pinBuf;
            BufPos = (UCHAR)BytesRead;

            while (BufPos)
            {
                //IR data packet begins with 0x8X where X is data length
                if (*pByte >= 0x81 && *pByte <= 0x9E)
                {
                    UCHAR Length = *pByte & 0x7F;
                    if (Length > BufPos - 1)
                    {
                        BytesRead -= BufPos;
                        break;
                    }
                    MceIrDecode(pByte + 1, Length);
                    BufPos -= Length + 1;
                    pByte += Length + 1;
                }
                else
                {
                    MceIrDecode(NULL, 0);
                    BufPos--;
                    pByte++;
                }
            }

            if (IdleTimeout)
            {
                IdleTimeout = 1000L;
                if (BufPos)
                    memcpy(pinBuf, pinBuf + 0x10 - BufPos, BufPos);
                break;
            }

            if (RecTimeout && (hRecord != INVALID_HANDLE_VALUE))
            {
                pByte = pinBuf;
                while (BytesRead)
                {
                    static UCHAR Remains = 0;
                    //Check packet header
                    if (!(*pByte & 0x80))
                    {
                        Trace("Invalid packet received !\n");
                        hRecord = INVALID_HANDLE_VALUE;
                        SetEvent(hRecordDone);
                        break;
                    }
                    //End of IR data
                    if (*pByte & 0x10)
                    {
                        Trace("Record successfull !\n");
                        hRecord = INVALID_HANDLE_VALUE;
                        SetEvent(hRecordDone);
                        break;
                    }
                    /*
                    for (i = 1 ; i <= (*pByte & 0x0F) ; i++)
                    {
                    if (pByte[i] & 0x80)
                    {
                    if (pByte[i] > 0x81)
                    {
                    pByte[i] -= 1;
                    Remains += 1;
                    }
                    }
                    else if (Remains)
                    {
                    if (pByte[i] > Remains)
                    {
                    pByte[i] += Remains;
                    Remains = 0;
                    }
                    else if (pByte[i] > 1)
                    {
                    Remains -= pByte[i] - 1;
                    pByte[i] = 1;
                    }
                    }
                    }
                    */
                    WriteFile(hRecord, pByte + 1, *pByte & 0x0F, &BytesWritten, NULL);
                    BytesRead -= (*pByte & 0x0F) + 1;
                    pByte += (*pByte & 0x0F) + 1;
                }
            }
            if (BufPos)
            {
                memcpy(pinBuf, pinBuf + 0x10 - BufPos, BufPos);
            }
            break;

        case EVENT_RECORD:
            Debug("WAIT IDLE!\n");
            IdleTimeout = 1000L;
            RecTimeout = 0L;
            break;

        case EVENT_PLAY:
            Debug("PLAY !\n");
            IsPlaying = TRUE;
            if (PlayDelay == 0)
                PlayDelay = GetTickCount() + 300L;
            break;

        case EVENT_WRITE:
            Debug("WRITE !\n");
            IsPlaying = FALSE;
            IsWriting = FALSE;
            SetEvent(hPlayDone);
            if (poutBuf)
                HeapFree(GetProcessHeap(), 0, poutBuf);
            poutBuf = NULL;
            break;

        case EVENT_TERMINATE:
            Running = FALSE;
            break;
        }
    }

    // perform some cleanup
    if (IsReading)
    {
        CancelIo(hReadPipe);
    }

    if (IsWriting)
    {
        CancelIo(hWritePipe);
    }

    if (hReadEvent  != INVALID_HANDLE_VALUE)
        CloseHandle(hReadEvent);

    if (hWriteEvent != INVALID_HANDLE_VALUE) 
        CloseHandle(hWriteEvent);

    if (hReadPipe   != INVALID_HANDLE_VALUE) 
        CloseHandle(hReadPipe);

    if ((hWritePipe  != INVALID_HANDLE_VALUE) && (hWritePipe  != hReadPipe)) 
        CloseHandle(hWritePipe);

    return 0;
}

static DWORD WINAPI MceIrVistaThreadProc(LPVOID lpParameter)
{
    int DeviceBufferSize = 100;
    int bytesRead;
    int *receiveParamsPtr;
    int receiveParamsSize;
    int ret;

    receiveParamsSize = sizeof(ReceiveParams) + DeviceBufferSize + 8;
    receiveParamsPtr = (int *)calloc(1, receiveParamsSize);
    ((ReceiveParamsPtr)receiveParamsPtr)->ByteCount = DeviceBufferSize;

    VistaThreadStop = false;

    DebugIoControl("***************** MceIrVistaThreadProc() starting LOOP\n");
    while (!VistaThreadStop)
    {
        DebugIoControl("***************** MceIrVistaThreadProc() Before IoControl\n");
        ret = IoControl(IoCtrl_Receive, NULL, 0, receiveParamsPtr, receiveParamsSize, (LPDWORD)&bytesRead);
        if (!ret)
            break;
        DebugIoControl("***************** MceIrVistaThreadProc() After IoControl, bytesRead=%d\n", bytesRead);
        if (bytesRead > sizeof(ReceiveParams))
        {
            MceIrDecodeVista((DWORD *)((PUCHAR)receiveParamsPtr + sizeof(ReceiveParams)),
                                       (bytesRead - sizeof(ReceiveParams)) / 4);
        }
        else
        {
            DebugIoControl("***************** MceIrVistaThreadProc() TRYING RECOVERY...\n");
            if (!VistaGetDeviceCapabilities())
                DebugIoControl("***************** MceIrVistaThreadProc() FAILED, Somthing must be broken!!!!!!!!!!!!!\n");
            DebugIoControl("***************** MceIrVistaThreadProc() RESTARTING RECEIVING\n");
            VistaStopReceive();
            VistaStartReceive(_receivePort, PacketTimeout);
            if (!VistaGetDeviceCapabilities())
            {
                DebugIoControl("***************** MceIrVistaThreadProc() FAILED, STILL broken!!!!!!!!!!!!!\n");
                DebugIoControl("***************** MceIrVistaThreadProc() TRYING TO REOPEN DEVICE...\n");
                VistaStopReceive();
                CancelIo(hReadPipe);
                CloseHandle(hReadPipe);
                MceIrOpenPipes();
                VistaGetDeviceCapabilities();
                VistaStartReceive(_receivePort, PacketTimeout);
                if (!VistaGetDeviceCapabilities())
                {
                    DebugIoControl("***************** MceIrVistaThreadProc() FAILED, STILL STILL broken, exitting...!!!!!!!!!!!!!\n");
                    break;
                }
                else
                {
                    DebugIoControl("***************** MceIrVistaThreadProc() FIXED (should be)!!!!!!!!!!!!!\n");
                }
            }
            // Sleep(PacketTimeout / 10);
        }
    }
    DebugIoControl("***************** MceIrVistaThreadProc() exitting LOOPn");

    // perform some cleanup
    free(receiveParamsPtr);
    VistaStopReceive();
    if (hReadPipe != INVALID_HANDLE_VALUE) {
        CancelIo(hReadPipe);
        CloseHandle(hReadPipe);
    }
    return 0;
}

static BOOL MceIrGetDeviceFileName(LPGUID pGuid, char *outNameBuf)
{
    HANDLE hDev = MceIrOpenUsbDevice(pGuid, outNameBuf);
    if (hDev != INVALID_HANDLE_VALUE)
    {
        CloseHandle(hDev);
        return TRUE;
    }

    return FALSE;
}

static void MceIrOpenPipes()
{
    char DeviceName[MAX_PATH] = "";
    char PipeName[MAX_PATH] = "";

    if (MceIrGetDeviceFileName((LPGUID)&GUID_CLASS_USB_BULK, DeviceName))
    {
        wsprintf(PipeName, "%s\\%s", DeviceName, BULK_INPUT_PIPE);

        hReadPipe = CreateFile(PipeName,
            GENERIC_READ,
            0,
            NULL,
            OPEN_EXISTING,
            FILE_FLAG_OVERLAPPED,
            NULL);

        if (hReadPipe == INVALID_HANDLE_VALUE)
        {
            Trace("Failed to open (%s) = %d\n", PipeName, GetLastError());
            return;
        }

        wsprintf(PipeName, "%s\\%s", DeviceName, BULK_OUTPUT_PIPE);

        hWritePipe = CreateFile(PipeName,
            GENERIC_WRITE,
            0,
            NULL,
            OPEN_EXISTING,
            FILE_FLAG_OVERLAPPED,
            NULL);

        if (hWritePipe == INVALID_HANDLE_VALUE)
        {
            CloseHandle(hReadPipe);
            hReadPipe = INVALID_HANDLE_VALUE;
            Trace("Failed to open (%s) = %d\n", DeviceName, GetLastError());
        }
    }
    else if (MceIrGetDeviceFileName((LPGUID)&GUID_CLASS_IRBUS, DeviceName))
    {
        wsprintf(PipeName, "%s\\%s", DeviceName, IRBUS_PIPE);

        hReadPipe = CreateFile(PipeName,
            GENERIC_READ | GENERIC_WRITE,
            0,
            NULL,
            OPEN_EXISTING,
            FILE_FLAG_OVERLAPPED,
            NULL);

        if (hReadPipe == INVALID_HANDLE_VALUE)
        {
            /* try again for Vista */
            hReadPipe = CreateFile(DeviceName,
                GENERIC_READ | GENERIC_WRITE,
                0,
                NULL,
                OPEN_EXISTING,
                FILE_FLAG_OVERLAPPED,
                NULL);

            if (hReadPipe == INVALID_HANDLE_VALUE)
            {
                Trace("Failed to open (%s) = %d\n", PipeName, GetLastError());
                return;
            }
            probablyVista = TRUE;
        }

        hWritePipe = hReadPipe;
    }
}

static HANDLE MceIrOpenOneDevice(IN HDEVINFO HardwareDeviceInfo, IN PSP_DEVICE_INTERFACE_DATA DeviceInterfaceData, IN char *devName)
{
    PSP_DEVICE_INTERFACE_DETAIL_DATA     functionClassDeviceData = NULL;
    ULONG                                predictedLength = 0;
    ULONG                                requiredLength = 0;
    HANDLE                               hOut = INVALID_HANDLE_VALUE;

    //
    // allocate a function class device data structure to receive the
    // goods about this particular device.
    //
    SetupDiGetDeviceInterfaceDetail (
        HardwareDeviceInfo,
        DeviceInterfaceData,
        NULL, // probing so no output buffer yet
        0, // probing so output buffer length of zero
        &requiredLength,
        NULL); // not interested in the specific dev-node


    predictedLength = requiredLength;

    functionClassDeviceData = (PSP_DEVICE_INTERFACE_DETAIL_DATA) malloc (256);
    memset(functionClassDeviceData, 0, 256);
    functionClassDeviceData->cbSize = (sizeof(DWORD) == 8) ? 8 : 5;

    //
    // Retrieve the information from Plug and Play.
    //
    if (! SetupDiGetDeviceInterfaceDetail(
        HardwareDeviceInfo,
        DeviceInterfaceData,
        functionClassDeviceData,
        requiredLength,
        NULL,
        NULL))
    {
        free(functionClassDeviceData);
        return INVALID_HANDLE_VALUE;
    }

    // strcpy(devName, functionClassDeviceData->DevicePath); // Deprecated
    strcpy_s(devName, MAX_PATH, functionClassDeviceData->DevicePath);
    Debug("Attempting to open %s\n", devName);

    hOut = CreateFile(
        functionClassDeviceData->DevicePath,
        GENERIC_READ | GENERIC_WRITE,
        0,
        NULL, // no SECURITY_ATTRIBUTES structure
        OPEN_EXISTING, // No special create flags
        0, // No special attributes
        NULL); // No template file

    if (INVALID_HANDLE_VALUE == hOut)
    {
        Trace("FAILED to open %s\n", devName);
    }

    free(functionClassDeviceData);

    return hOut;
}

static HANDLE MceIrOpenUsbDevice(LPGUID  pGuid, char *outNameBuf)
{
    HANDLE            hOut = INVALID_HANDLE_VALUE;
    HDEVINFO          hardwareDeviceInfo;
    SP_DEVINFO_DATA   deviceInfoData;
    ULONG             i;

    // Open a handle to the plug and play dev node.
    // SetupDiGetClassDevs() returns a device information set that contains info on all
    // installed devices of a specified class.
    hardwareDeviceInfo = SetupDiGetClassDevs(
        pGuid,
        NULL, // Define no enumerator (global)
        NULL, // Define no
        (DIGCF_PRESENT | // Only Devices present
        DIGCF_DEVICEINTERFACE)); // Function class devices.

    if (hardwareDeviceInfo == INVALID_HANDLE_VALUE)
        return INVALID_HANDLE_VALUE;

    for (i = 0; ; i++)
    {
        memset(&deviceInfoData, 0, sizeof(deviceInfoData));
        deviceInfoData.cbSize = sizeof(deviceInfoData);
        if (SetupDiEnumDeviceInfo (hardwareDeviceInfo, i, &deviceInfoData))
        {
            // SetupDiEnumDeviceInterfaces() returns information about device interfaces
            // exposed by one or more devices. Each call returns information about one interface;
            // the routine can be called repeatedly to get information about several interfaces
            // exposed by one or more devices.
            SP_DEVICE_INTERFACE_DATA   deviceInterfaceData;
            memset(&deviceInterfaceData, 0, sizeof(deviceInterfaceData));
            deviceInterfaceData.cbSize = sizeof(deviceInterfaceData);
            SetupDiEnumDeviceInterfaces (
                hardwareDeviceInfo,
                &deviceInfoData,
                pGuid,
                0,
                &deviceInterfaceData);
            hOut = MceIrOpenOneDevice(hardwareDeviceInfo, &deviceInterfaceData, outNameBuf);
            if (hOut != INVALID_HANDLE_VALUE)
                break;
        }
        else
        {
            if (ERROR_NO_MORE_ITEMS == GetLastError())
                break;
        }
    }

    // SetupDiDestroyDeviceInfoList() destroys a device information set
    // and frees all associated memory.

    SetupDiDestroyDeviceInfoList(hardwareDeviceInfo);

    return hOut;
}

static BOOL MceIrImportProntoRC5(PUCHAR pData, ULONG Length, PUCHAR *pBuf, PULONG pReadCount)
{
    USHORT Proto, Clock, Seq1, Seq2;
    USHORT System, Command;
    USHORT RC5 = 0;
    PUCHAR pBuffer = NULL;
    //  PUCHAR pData2 = NULL;
    BOOL LastIsPulse = TRUE;
    int i;

    //Read 15 bytes of header
    if (Length < 20)
        return FALSE;
    if (sscanf_s((PCHAR)pData, "%04x %04x %04x %04x", &Proto, &Clock, &Seq1, &Seq2) != 4) 
        return FALSE;
    if (Proto != PRONTO_PROTO_RC5)
        return FALSE;
    if (Seq1 + Seq2 != 1)
        return FALSE;

    pData += 20;
    if (sscanf_s((PCHAR)pData, "%04x %04x", &System, &Command) != 2)
        return FALSE;
    if (System > 31)
        return FALSE;
    if (Command > 127)
        return FALSE;

    BIT_SET(RC5, 13); //SS1
    if (Command < 64)
        BIT_SET(RC5, 12); //SS2
    BIT_SET(RC5, 11); //Toggle

    RC5 |= (System << 6) | Command;

    Trace("PLAY_RC5_KEYCODE code:%04X !!!\n", RC5);

    pBuffer = *pBuf = (PUCHAR) HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, 1000);
    if (!pBuffer)
        return FALSE;

    *pBuffer = 0x92;
    for (i = 13 ; i-- ; )
    {
        if (BIT_TEST(RC5, i))
        {
            if (LastIsPulse)
                pBuffer++;

            *pBuffer += 0x12;
            pBuffer++;
            *pBuffer = 0x92;
            LastIsPulse = TRUE;
        }
        else
        {
            if (!LastIsPulse)
                pBuffer++;

            *pBuffer |= 0x80;
            *pBuffer += 0x12;
            pBuffer++;
            *pBuffer = 0x12;
            LastIsPulse = FALSE;
        }
    }
    pBuffer++;

    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;
    *pBuffer++ = 0x7F;

    memcpy(pBuffer, *pBuf, pBuffer - *pBuf);
    pBuffer += pBuffer - *pBuf;
    memcpy(pBuffer, *pBuf, pBuffer - *pBuf);
    pBuffer += pBuffer - *pBuf;

    *pReadCount = (ULONG) (pBuffer - *pBuf);

    return TRUE;
}

static BOOL MceIrImportProntoRC5X(PUCHAR pData, ULONG Length, PUCHAR *pBuf, PULONG pReadCount)
{
    BOOL Result = FALSE;
    USHORT Proto, Clock, Seq1, Seq2;
    USHORT System, Command, Data;
    ULONG RC5 = 0;
    PUCHAR pBuffer = NULL;
    //  PUCHAR pData2 = NULL;
    BOOL LastIsPulse = TRUE;
    int i;

    do
    {
        //Read 15 bytes of header
        if (Length < 20)
            break;
        if (sscanf_s((PCHAR)pData, "%04x %04x %04x %04x", &Proto, &Clock, &Seq1, &Seq2) != 4) 
            break;
        if (Proto != PRONTO_PROTO_RC5X) 
            break;
        if (Seq1 + Seq2 != 2) 
            break;

        pData += 20;
        if (sscanf_s((PCHAR)pData, "%04x %04x %04x", &System, &Command, &Data) != 3) 
            break;
        if (System > 31) 
            break;
        if (Command > 127) 
            break;
        if (Data > 63) 
            break;

        BIT_SET(RC5, 19); //SS1
        if (Command < 64)
            BIT_SET(RC5, 18); //SS2
        BIT_SET(RC5, 17); //Toggle

        RC5 |= (System << 12) | (Command << 6) | Data;

        Trace("PLAY_RC5X_KEYCODE code:%08X !!!\n", RC5);

        pBuffer = *pBuf = (PUCHAR) HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, 1000);
        if (!pBuffer)
            break;

        *pBuffer = 0x92;
        for (i = 19 ; i-- ; )
        {
            if (i == 11)
            {
                if (LastIsPulse) 
                    pBuffer++;
                *pBuffer += 0x48;
                LastIsPulse = FALSE;
            }
            if (BIT_TEST(RC5, i))
            {
                if (LastIsPulse) 
                    pBuffer++;
                *pBuffer += 0x12;
                pBuffer++;
                *pBuffer = 0x92;
                LastIsPulse = TRUE;
            }
            else
            {
                if (!LastIsPulse) 
                    pBuffer++;
                *pBuffer |= 0x80;
                *pBuffer += 0x12;
                pBuffer++;
                *pBuffer = 0x12;
                LastIsPulse = FALSE;
            }
        }
        pBuffer++;

        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;

        memcpy(pBuffer, *pBuf, pBuffer - *pBuf);
        pBuffer += pBuffer - *pBuf;
        memcpy(pBuffer, *pBuf, pBuffer - *pBuf);
        pBuffer += pBuffer - *pBuf;

        *pReadCount = (ULONG) (pBuffer - *pBuf);

        Result = TRUE;

    } while (FALSE);

    return Result;
}

static BOOL MceIrImportProntoRC6(PUCHAR pData, ULONG Length, PUCHAR *pBuf, PULONG pReadCount)
{
    BOOL Result = FALSE;
    USHORT Proto, Clock, Seq1, Seq2;
    USHORT System, Command;
    ULONG RC6 = 0;
    PUCHAR pBuffer = NULL;
    //  PUCHAR pData2 = NULL;
    BOOL LastIsPulse = TRUE;
    int i;

    do
    {
        //Read 15 bytes of header
        if (Length < 20) break;
        if (sscanf_s((PCHAR)pData, "%04x %04x %04x %04x", &Proto, &Clock, &Seq1, &Seq2) != 4) break;
        if (Proto != PRONTO_PROTO_RC6) break;
        if (Seq1 + Seq2 != 1) break;

        pData += 20;
        if (sscanf_s((PCHAR)pData, "%04x %04x", &System, &Command) != 2) break;
        if (System > 255) break;
        if (Command > 255) break;

        RC6 = (System << 8) | Command;

        Trace("PLAY_RC6_KEYCODE code:%08X !!!\n", RC6);

        pBuffer = *pBuf = (PUCHAR) HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, 1000);
        if (!pBuffer) break;

        //RC6 header
        *pBuffer++ = 0xB6;
        *pBuffer++ = 0x12;
        *pBuffer++ = 0x89;
        *pBuffer++ = 0x12;
        *pBuffer++ = 0x89;
        *pBuffer++ = 0x09;
        *pBuffer++ = 0x89;
        *pBuffer++ = 0x09;
        *pBuffer++ = 0x89;
        *pBuffer++ = 0x12;
        *pBuffer   = 0x92;

        for (i = 16 ; i-- ; )
        {
            if (BIT_TEST(RC6, i))
            {
                if (!LastIsPulse) pBuffer++;
                *pBuffer |= 0x80;
                *pBuffer += 0x09;
                pBuffer++;
                *pBuffer = 0x09;
                LastIsPulse = FALSE;
            }
            else
            {
                if (LastIsPulse) pBuffer++;
                *pBuffer += 0x09;
                pBuffer++;
                *pBuffer = 0x89;
                LastIsPulse = TRUE;
            }
        }
        pBuffer++;

        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;

        memcpy(pBuffer, *pBuf, pBuffer - *pBuf);
        pBuffer += pBuffer - *pBuf;
        memcpy(pBuffer, *pBuf, pBuffer - *pBuf);
        pBuffer += pBuffer - *pBuf;

        *pReadCount = (ULONG) (pBuffer - *pBuf);

        Result = TRUE;

    } while (FALSE);

    return Result;
}

static BOOL MceIrImportProntoRC6A(PUCHAR pData, ULONG Length, PUCHAR *pBuf, PULONG pReadCount)
{
    BOOL Result = FALSE;
    USHORT Proto, Clock, Seq1, Seq2;
    USHORT Customer, System, Command;
    ULONG RC6 = 0;
    PUCHAR pBuffer = NULL;
    //  PUCHAR pData2 = NULL;
    BOOL LastIsPulse = TRUE;
    BYTE BitCount;
    int i;

    do
    {
        //Read 15 bytes of header
        if (Length < 20) break;
        if (sscanf_s((PCHAR)pData, "%04x %04x %04x %04x", &Proto, &Clock, &Seq1, &Seq2) != 4) break;
        if (Proto != PRONTO_PROTO_RC6A) break;
        if (Seq1 + Seq2 != 2) break;

        pData += 20;
        if (sscanf_s((PCHAR)pData, "%04x %04x %04x", &Customer, &System, &Command) != 3) break;
        if (System > 255) break;
        if (Command > 255) break;
        if ((Customer > 127) && (Customer < 32768)) break;

        RC6 = (Customer << 16) | (System << 8) | Command;

        Trace("PLAY_RC6A_KEYCODE code:%08X !!!\n", RC6);

        pBuffer = *pBuf = (PUCHAR) HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, 1000);
        if (!pBuffer) break;

        //RC6A header
        *pBuffer++ = 0xBF;
        *pBuffer++ = 0x12;
        *pBuffer++ = 0x89;
        *pBuffer++ = 0x09;
        *pBuffer++ = 0x89;
        *pBuffer++ = 0x09;
        *pBuffer++ = 0x89;
        *pBuffer++ = 0x12;
        *pBuffer++ = 0x89;
        *pBuffer++ = 0x12;
        *pBuffer   = 0x92;

        BitCount = (Customer >= 32768) ? 16 : 8;

        for (i = (Customer >= 32768) ? 32 : 24 ; i-- ; )
        {
            if (BIT_TEST(RC6, i))
            {
                if (!LastIsPulse) pBuffer++;
                *pBuffer |= 0x80;
                *pBuffer += 0x09;
                pBuffer++;
                *pBuffer = 0x09;
                LastIsPulse = FALSE;
            }
            else
            {
                if (LastIsPulse) pBuffer++;
                *pBuffer += 0x09;
                pBuffer++;
                *pBuffer = 0x89;
                LastIsPulse = TRUE;
            }
        }
        pBuffer++;

        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;
        *pBuffer++ = 0x7F;

        memcpy(pBuffer, *pBuf, pBuffer - *pBuf);
        pBuffer += pBuffer - *pBuf;
        memcpy(pBuffer, *pBuf, pBuffer - *pBuf);
        pBuffer += pBuffer - *pBuf;

        *pReadCount = (ULONG) (pBuffer - *pBuf);

        Result = TRUE;

    } while (FALSE);

    return Result;
}

static BOOL MceIrImportProntoLearned(PUCHAR pData, ULONG Length, PUCHAR *pBuf, PULONG pReadCount)
{
    PCHAR pHeader;
    double Carrier;
    ULONG Sequence, Seq;
    USHORT Clock, Seq1, Seq2;
    PUCHAR pBuffer = NULL;
    PUCHAR pData2 = NULL;
    PUCHAR pPronto;
    USHORT Remaining = 0;
    BYTE RepeatCount = 0;
    BOOL NextIsPulse = TRUE;
    BOOL Result = FALSE;

    do
    {
        //Read 15 bytes of header
        if (Length < 20) break;
        pHeader = (PCHAR)pData + 5;

        if (sscanf_s(pHeader, " %04x %04x %04x", &Clock, &Seq1, &Seq2) != 3) break;
        if (Clock == 0) break;

        pBuffer = pData2 = (PUCHAR) HeapAlloc(GetProcessHeap(), 0, (Length << 4));
        if (!pBuffer) break;

        Carrier = Clock * .241246;
        Sequence = Seq = (Seq1 ? Seq1 : Seq2) * 2;
        NextIsPulse = TRUE;
        Remaining = 0;
        RepeatCount = 0;

        *pReadCount = 0;
        pPronto = pData + 15;

        for(;;)
        {
            if (Remaining)
            {
                if (Remaining < 128)
                {
                    *pBuffer++ = (UCHAR)Remaining | (NextIsPulse ? 0x00 : 0x80);
                    (*pReadCount)++;
                    Remaining = 0;
                }
                else
                {
                    *pBuffer++ = 0x7F | (NextIsPulse ? 0x00 : 0x80);
                    (*pReadCount)++;
                    Remaining -= 0x7F;
                }
            }
            if (!Remaining)
            {
                if ((pPronto >= pData + Length) || (Seq == 0))
                {
                    if (RepeatCount >= 3)
                    {
                        Result = TRUE;
                        break;
                    }
                    pPronto = pData + 15;
                    RepeatCount++;
                    NextIsPulse = TRUE;
                    Seq = Sequence;
                    continue;
                }
                pPronto += 5;
                if (pPronto > pData + Length) break;
                if (sscanf_s((PCHAR)pPronto, " %04x", &Remaining) != 1)  break;
                Seq--;
                Remaining = (USHORT)(((Remaining * Carrier) + 25) / 50);
                NextIsPulse = !NextIsPulse;
            }
        }
        if (!Result)
        {
            if (pData2) HeapFree(GetProcessHeap(), 0, pData2);
            pData2 = NULL;
            break;
        }
        HeapFree(GetProcessHeap(), 0, pData);
        *pBuf = pData2;

    } while (FALSE);

    return Result;
}

static BOOL MceIrReadFile(HANDLE hPlay, PUCHAR *pBuf, PULONG pReadCount)
{
    //  BOOL IsPronto = FALSE;
    PUCHAR pData = NULL;
    PUCHAR pBuffer = NULL;
    ULONG Length;
    BOOL Result = FALSE;
    DWORD Counter;
    UCHAR BytesToCopy;
    PUCHAR pSource, pDest;

    do
    {
        SetFilePointer(hPlay, 0, NULL, FILE_BEGIN);

        Length = GetFileSize(hPlay, NULL);

        if (Length == 0xFFFFFFFF) 
            break;

        pData = (PUCHAR) HeapAlloc(GetProcessHeap(), 0, Length + 1);

        if (!pData) 
            break;

        //Read full file
        if (!ReadFile(hPlay, pData, Length, pReadCount, NULL) ||
            (*pReadCount != Length))
        {
            Trace( "Read failed with error %d\n", GetLastError());
            break;
        }
        pData[Length] = 0;

        if (Length >= 5)
        {
            if ((strncmp((PCHAR)pData, "0000 ", 5) == 0) ||
                (strncmp((PCHAR)pData, "0100 ", 5) == 0))
            {
                Result = MceIrImportProntoLearned(pData, Length, &pData, &Length);
                if (!Result) 
                    break;
            }
            else if (strncmp((PCHAR)pData, "5000 ", 5) == 0)
            {
                Result = MceIrImportProntoRC5(pData, Length, &pData, &Length);
                if (!Result) 
                    break;
            }
            else if (strncmp((PCHAR)pData, "5001 ", 5) == 0)
            {
                Result = MceIrImportProntoRC5X(pData, Length, &pData, &Length);
                if (!Result) 
                    break;
            }
            else if (strncmp((PCHAR)pData, "6000 ", 5) == 0)
            {
                Result = MceIrImportProntoRC6(pData, Length, &pData, &Length);
                if (!Result) 
                    break;
            }
            else if (strncmp((PCHAR)pData, "6001 ", 5) == 0)
            {
                Result = MceIrImportProntoRC6A(pData, Length, &pData, &Length);
                if (!Result) 
                    break;
            }
            else if (!(*pData & 0x80)) 
                break;
        }

        if (BlasterSpeed == SPEED_NONE)
        {
            pDest = pBuffer = (PUCHAR) HeapAlloc(GetProcessHeap(), 0, (Length * 6 / 4) + 5);
            pSource = pData;
        }
        else
        {
            pDest = pBuffer = (PUCHAR) HeapAlloc(GetProcessHeap(), 0, (Length * 6 / 4) + 9);
            pSource = pData;

            // Set Blaster Speed
            *pDest++ = 0x9F;
            *pDest++ = 0x06;
            *pDest++ = 0x01;

            switch(BlasterSpeed)
            {
            case SPEED_FAST:    *pDest++ = 0x44;  break;
            case SPEED_SLOW:    *pDest++ = 0x50;  break;
            default:            *pDest++ = 0x4A;  break;  // Medium
            }
        }

        // Set Blaster Port
        *pDest++ = 0x9F;
        *pDest++ = 0x08;

        switch(BlasterType)
        {
        case TYPE_SMK:
            {
                switch(Blaster)
                {
                case BLASTER_1: *pDest++ = 0x01;  break;
                case BLASTER_2: *pDest++ = 0x02;  break;
                default:        *pDest++ = 0x00;  break;  // Both
                }
                break;
            }

        default:  // Microsoft
            {
                switch(Blaster)
                {
                case BLASTER_1: *pDest++ = 0x04;  break;
                case BLASTER_2: *pDest++ = 0x02;  break;
                default:        *pDest++ = 0x06;  break;  // Both
                }
                break;
            }
        }

        for (Counter = 0 ; Counter < Length ; Counter += 4)
        {
            BytesToCopy = (UCHAR)(Length - Counter < 4 ? Length - Counter : 4);
            *pDest++ = 0x80 + BytesToCopy;
            memcpy(pDest, pSource, BytesToCopy);
            pDest += BytesToCopy;
            pSource += BytesToCopy;
        }
        *pDest++ = 0x80;
        *pReadCount = (ULONG) (pDest - pBuffer);
        Result = TRUE;

    } while (FALSE);

    if (pData)
        HeapFree(GetProcessHeap(), 0, pData);

    *pBuf = pBuffer;

    return Result;
}

void TraceOut(LPSTR szFormat, ...)
{
    CHAR szTempOutput[500];
    WaitForSingleObject(hTraceMutex, INFINITE);
    va_list args;
    va_start(args, szFormat);
    //_vsnprintf(szTempOutput, sizeof(szTempOutput), szFormat, args);
    _vsnprintf_s(szTempOutput, sizeof(szTempOutput), szFormat, args);
    szTempOutput[sizeof(szTempOutput)-2] = '\n';
    szTempOutput[sizeof(szTempOutput)-1] = 0;
    va_end(args);
    OutputDebugString(szTempOutput);
    ReleaseMutex(hTraceMutex);
}

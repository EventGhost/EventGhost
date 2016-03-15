#include <windows.h>
#include <deque>
#include <tchar.h>
#include <strsafe.h>
#include <aclapi.h>
#include <stdio.h>
#include "MceIrMessages.h"
#include <stdio.h>
#include <malloc.h>
#include <setupapi.h>
#include <winioctl.h>
#include "MceIrDrv.h"
#include <strsafe.h>

#define WIN32_LEAN_AND_MEAN
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "setupapi.lib")
// MceIr.cpp : Defines the entry point for the DLL application.
//

void TraceOut(LPTSTR szFormat, ...);
void EventTraceOut(LPTSTR szFormat, ...);
void EventTraceError(LPTSTR szFormat, ...);
#if _DEBUG
#define EventTrace EventTraceOut
#define Trace TraceOut
#define Debug TraceOut
#define DebugIoControl TraceOut
#else
#define EventTrace //EventTraceOut
#define Trace //EventTraceOut
#define Debug //EventTraceOut
#define DebugIoControl //EventTraceOut
#endif

#define IRBUS_PIPE        _T("Pipe01")

#define BIT_SET(a, b)     (a) |= (1 << (b))
#define BIT_TEST(a, b)    ((a) & (1 << (b)))

#ifdef _WIN64
  typedef __int64 PtrSize;
#else
  typedef int __w64 PtrSize; // Add __w64 keyword
#endif

typedef struct {
    /// Last packet in block?
    PtrSize DataEnd;
    /// Number of bytes in block.
    PtrSize ByteCount;
    /// Carrier frequency of IR received.
    PtrSize CarrierFrequency;
} ReceiveParams, *ReceiveParamsPtr;

typedef struct {
    /// Index of the receiver to use.
    PtrSize Receiver;
    /// Receive timeout, in milliseconds.
    PtrSize Timeout;
} StartReceiveParams, *StartReceiveParamsPtr;

typedef struct {
    /// Device protocol version.
    PtrSize ProtocolVersion;
    /// Number of transmit ports – 0-32.
    PtrSize TransmitPorts;
    /// Number of receive ports – 0-32. For beanbag, this is two (one for learning, one for normal receiving).
    PtrSize ReceivePorts;
    /// Bitmask identifying which receivers are learning receivers – low bit is the first receiver, second-low bit is the second receiver, etc ...
    PtrSize LearningMask;
    /// Device flags.
    PtrSize DetailsFlags;
} MCEDeviceCapabilities, *MCEDeviceCapabilitiesPtr;

typedef struct 
{
  /// Blaster bit-mask.
  PtrSize Blasters;
} AvailableBlasters;

typedef struct 
{
  /// Next chunk offset.
  PtrSize OffsetToNextChunk;
  /// Repeat count.
  PtrSize RepeatCount;
  /// Number of bytes.
  PtrSize ByteCount;
} TransmitChunk;

typedef struct 
{
  /// Bitmask containing ports to transmit on.
  PtrSize TransmitPortMask;
  /// Carrier period.
  PtrSize CarrierPeriod;
  /// Transmit Flags.
  PtrSize Flags;
  /// Pulse Size.  If Pulse Mode Flag set.
  PtrSize PulseSize;
} TransmitParams;

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
    /// Reset IR.
    IoCtrl_Reset         = 0x0F608010,
}  IoCtrl;

class ReceiveChunk
{
public:
	PUCHAR data;
	DWORD len;	
	ReceiveChunk(PUCHAR inptr, DWORD inlen)
	{
		data = new unsigned char[inlen];
		memcpy(data,inptr,inlen);
		len = inlen;
	}
	~ReceiveChunk()
	{
		delete [] data;
	}
private:
	ReceiveChunk();
	ReceiveChunk(const ReceiveChunk &);
	ReceiveChunk& ReceiveChunk::operator=(const ReceiveChunk &);
};

std::deque<ReceiveChunk *> ReceivedData;
CRITICAL_SECTION CriticalSection_Deque;

//Local functions
static bool         MceIrOpenPipes          ();
static BOOL         MceIrGetDeviceFileName  (LPGUID  pGuid, TCHAR *outNameBuf);
static HANDLE       MceIrOpenUsbDevice      (LPGUID  pGuid, TCHAR *outNameBuf);
static void VistaStartReceive(int receivePort, int timeout);
static bool VistaStopReceive(void);
static DWORD WINAPI MceIrVistaThreadProc    (LPVOID lpParameter);
static DWORD WINAPI OutputConnectionsThreadProc (LPVOID lpParameter);
//Local variables
static HANDLE hTraceMutex   = INVALID_HANDLE_VALUE;
static HANDLE hThread       = INVALID_HANDLE_VALUE;
static HANDLE hOutThread    = INVALID_HANDLE_VALUE;
static HANDLE hReadPipe     = INVALID_HANDLE_VALUE;
static HANDLE hOutPipe      = INVALID_HANDLE_VALUE;
static HANDLE hStopEvent    = INVALID_HANDLE_VALUE;
static HANDLE hModeChangeEvent = INVALID_HANDLE_VALUE;
static HANDLE hDataReady    = INVALID_HANDLE_VALUE;
static char pDataFromOutpipe[2048];
static const int DeviceBufferSize = 100;
static int nData;
static BOOL isPipeConnected = false, isDeviceConnected = false;
static MCEDeviceCapabilities deviceCapabilities;

static BOOL   IsPlaying     = FALSE;

static BOOL   probablyVista = FALSE;
static BOOL   keepRunning;
static BOOL   newConnection;
static BOOL   modeChanged;
static int   portToUse;
static BOOL   OutputThreadStop;
static int    PacketTimeout = 100;
static int   _numTxPorts;
static int   _txPortMask;
static int   _learnPortMask;
static int   _receivePort;
static int   _learnPort;

static int count = 0;
#define SVCNAME TEXT("AlternateMceIrService")

SERVICE_STATUS          gSvcStatus; 
SERVICE_STATUS_HANDLE   gSvcStatusHandle; 
HANDLE                  ghSvcStopEvent = NULL;

TCHAR szCommand[10];
SC_HANDLE schSCManager;
SC_HANDLE schService;

VOID SvcInstall(void);
VOID WINAPI SvcCtrlHandler( DWORD ); 
VOID WINAPI SvcMain( DWORD, LPTSTR * ); 

VOID ReportSvcStatus( DWORD, DWORD, DWORD );
VOID SvcInit( DWORD, LPTSTR * ); 
VOID SvcReportErrorEvent( LPTSTR, BOOL includeLastError = true);
VOID SvcReportInfoEvent( LPTSTR );

VOID __stdcall DisplayUsage(void);

VOID __stdcall DoStartSvc(void);
VOID __stdcall DoUpdateSvcDacl(void);
VOID __stdcall DoStopSvc(void);

BOOL __stdcall StopDependentServices(void);
VOID __stdcall DoQuerySvc(void);
VOID __stdcall DoUpdateSvcDesc(void);
VOID __stdcall DoDisableSvc(void);
VOID __stdcall DoEnableSvc(void);
VOID __stdcall DoDeleteSvc(void);

void __cdecl _tmain(int argc, TCHAR *argv[]) 
{ 
    // Look for command-line parameter like "install". 
    // Otherwise, the service is probably being started by the SCM.

	if (argc > 1)
	{
		StringCchCopy(szCommand, 10, argv[1]);

		if (lstrcmpi( szCommand, TEXT("install")) == 0 )
			SvcInstall();
		else if (lstrcmpi( szCommand, TEXT("query")) == 0 )
			DoQuerySvc();
		else if (lstrcmpi( szCommand, TEXT("describe")) == 0 )
			DoUpdateSvcDesc();
		else if (lstrcmpi( szCommand, TEXT("disable")) == 0 )
			DoDisableSvc();
		else if (lstrcmpi( szCommand, TEXT("enable")) == 0 )
			DoEnableSvc();
		else if (lstrcmpi( szCommand, TEXT("delete")) == 0 )
			DoDeleteSvc();
		else if (lstrcmpi( szCommand, TEXT("start")) == 0 )
			DoStartSvc();
		else if (lstrcmpi( szCommand, TEXT("dacl")) == 0 )
			DoUpdateSvcDacl();
		else if (lstrcmpi( szCommand, TEXT("stop")) == 0 )
			DoStopSvc();
		else 
		{
			_tprintf(TEXT("Unknown command (%s)\n\n"), szCommand);
			DisplayUsage();
		}
	}

    // TO_DO: Add any additional services for the process to this table.
    SERVICE_TABLE_ENTRY DispatchTable[] = 
    { 
        { SVCNAME, (LPSERVICE_MAIN_FUNCTION) SvcMain }, 
        { NULL, NULL } 
    }; 
 
    // This call returns when the service has stopped. 
    // The process should simply terminate when the call returns.

    if (!StartServiceCtrlDispatcher( DispatchTable )) 
    { 
        SvcReportErrorEvent(TEXT("StartServiceCtrlDispatcher")); 
    } 
} 

VOID SvcInstall()
{
    TCHAR szPath[MAX_PATH];

    if( !GetModuleFileName( NULL, szPath, MAX_PATH ) )
    {
        printf("Cannot install service (%d)\n", GetLastError());
        return;
    }

    // Get a handle to the SCM database. 
 
    schSCManager = OpenSCManager( 
        NULL,                    // local computer
        NULL,                    // ServicesActive database 
        SC_MANAGER_ALL_ACCESS);  // full access rights 
 
    if (NULL == schSCManager) 
    {
        printf("OpenSCManager failed (%d)\n", GetLastError());
        return;
    }

    // Create the service

    schService = CreateService( 
        schSCManager,              // SCM database 
        SVCNAME,                   // name of service 
        SVCNAME,                   // service name to display 
        SERVICE_ALL_ACCESS,        // desired access 
        SERVICE_WIN32_OWN_PROCESS, // service type 
        SERVICE_AUTO_START,        // start type 
        SERVICE_ERROR_NORMAL,      // error control type 
        szPath,                    // path to service's binary 
        NULL,                      // no load ordering group 
        NULL,                      // no tag identifier 
        NULL,                      // no dependencies 
        NULL,                      // LocalSystem account 
        NULL);                     // no password 
 
    if (schService == NULL) 
    {
        printf("CreateService failed (%d)\n", GetLastError()); 
        CloseServiceHandle(schSCManager);
        return;
    }
    else printf("Service installed successfully\n"); 

    CloseServiceHandle(schService); 
    CloseServiceHandle(schSCManager);
}


VOID WINAPI SvcMain( DWORD dwArgc, LPTSTR *lpszArgv )
{
    // Register the handler function for the service
    gSvcStatusHandle = RegisterServiceCtrlHandler( 
        SVCNAME, 
        SvcCtrlHandler);

    if( !gSvcStatusHandle )
    { 
        SvcReportErrorEvent(TEXT("RegisterServiceCtrlHandler")); 
        return; 
    } 

    // These SERVICE_STATUS members remain as set here

    gSvcStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS; 
    gSvcStatus.dwServiceSpecificExitCode = 0;    

    // Report initial status to the SCM

    ReportSvcStatus( SERVICE_START_PENDING, NO_ERROR, 3000 );

    // Perform service-specific initialization and work.

    SvcInit( dwArgc, lpszArgv );
}


VOID SvcInit( DWORD dwArgc, LPTSTR *lpszArgv)
{
    // TO_DO: Declare and set any required variables.
    //   Be sure to periodically call ReportSvcStatus() with 
    //   SERVICE_START_PENDING. If initialization fails, call
    //   ReportSvcStatus with SERVICE_STOPPED.
	hTraceMutex = CreateMutex(NULL, false, NULL);
	hStopEvent = CreateEvent(NULL, false, false, NULL);
	hModeChangeEvent = CreateEvent(NULL, true, false, NULL);
	hDataReady    = CreateEvent(NULL, false, false, NULL);

	//Create worker threads.
	//One for attaching to IR Receiver
    DWORD ThreadId;
    hThread = CreateThread(NULL, 0, MceIrVistaThreadProc, NULL, 0, &ThreadId);
	SetThreadPriority(hThread, THREAD_PRIORITY_NORMAL);
	//Second for handling non-privileged output namedpipe
    hOutThread = CreateThread(NULL, 0, OutputConnectionsThreadProc, NULL, 0, &ThreadId);
    SetThreadPriority(hOutThread, THREAD_PRIORITY_NORMAL);

    // Create an event. The control handler function, SvcCtrlHandler,
    // signals this event when it receives the stop control code.

    ghSvcStopEvent = CreateEvent(
                         NULL,    // default security attributes
                         TRUE,    // manual reset event
                         FALSE,   // not signaled
                         NULL);   // no name

    if ( ghSvcStopEvent == NULL)
    {
        ReportSvcStatus( SERVICE_STOPPED, NO_ERROR, 0 );
        return;
    }

	// Initialize the critical section one time only.
    if (!InitializeCriticalSectionAndSpinCount(&CriticalSection_Deque, 
        0x80000400) )
	{
		ReportSvcStatus( SERVICE_STOPPED, NO_ERROR, 0 );
        return;
	}

    // Report running status when initialization is complete.

    ReportSvcStatus( SERVICE_RUNNING, NO_ERROR, 0 );

    // TO_DO: Perform work until service stops.

    while(1)
    {
        // Check whether to stop the service.

        WaitForSingleObject(ghSvcStopEvent, INFINITE);
		SetEvent(hStopEvent);

		keepRunning = false;

		if (hTraceMutex != INVALID_HANDLE_VALUE)
		{
			CloseHandle(hTraceMutex);
			hTraceMutex = INVALID_HANDLE_VALUE;
		}
		CloseHandle(hStopEvent);
		CloseHandle(hModeChangeEvent);
		CloseHandle(hDataReady);
		// Release resources used by the critical section object.
		DeleteCriticalSection(&CriticalSection_Deque);
        ReportSvcStatus( SERVICE_STOPPED, NO_ERROR, 0 );
        return;
    }
}

VOID ReportSvcStatus( DWORD dwCurrentState,
                      DWORD dwWin32ExitCode,
                      DWORD dwWaitHint)
{
    static DWORD dwCheckPoint = 1;

    // Fill in the SERVICE_STATUS structure.

    gSvcStatus.dwCurrentState = dwCurrentState;
    gSvcStatus.dwWin32ExitCode = dwWin32ExitCode;
    gSvcStatus.dwWaitHint = dwWaitHint;

    if (dwCurrentState == SERVICE_START_PENDING)
        gSvcStatus.dwControlsAccepted = 0;
    else gSvcStatus.dwControlsAccepted = SERVICE_ACCEPT_STOP;

    if ( (dwCurrentState == SERVICE_RUNNING) ||
           (dwCurrentState == SERVICE_STOPPED) )
        gSvcStatus.dwCheckPoint = 0;
    else gSvcStatus.dwCheckPoint = dwCheckPoint++;

    // Report the status of the service to the SCM.
    SetServiceStatus( gSvcStatusHandle, &gSvcStatus );
}

VOID WINAPI SvcCtrlHandler( DWORD dwCtrl )
{
   // Handle the requested control code. 

   switch(dwCtrl) 
   {  
      case SERVICE_CONTROL_STOP: 
         ReportSvcStatus(SERVICE_STOP_PENDING, NO_ERROR, 0);

         // Signal the service to stop.

         SetEvent(ghSvcStopEvent);
         
         return;
 
      case SERVICE_CONTROL_INTERROGATE: 
         // Fall through to send current status.
         break; 
 
      default: 
         break;
   } 

   ReportSvcStatus(gSvcStatus.dwCurrentState, NO_ERROR, 0);
}

VOID SvcReportErrorEvent(LPTSTR szFunction, BOOL includeLastError) 
{ 
    LPVOID lpMsgBuf;
    DWORD dw = GetLastError(); 

    HANDLE hEventSource;
    LPCTSTR lpszStrings[2];
    TCHAR Buffer[180];

    hEventSource = RegisterEventSource(NULL, SVCNAME);

    if( NULL != hEventSource )
    {
		if (includeLastError)
		{
			FormatMessage(
				FORMAT_MESSAGE_ALLOCATE_BUFFER | 
				FORMAT_MESSAGE_FROM_SYSTEM |
				FORMAT_MESSAGE_IGNORE_INSERTS,
				NULL,
				dw,
				MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
				(LPTSTR) &lpMsgBuf,
				0, NULL );

			StringCchPrintf(Buffer, 180, TEXT("%s failed with (%d) %s"), szFunction, dw, lpMsgBuf);

			lpszStrings[0] = SVCNAME;
			lpszStrings[1] = Buffer;

			ReportEvent(hEventSource,        // event log handle
						EVENTLOG_ERROR_TYPE, // event type
						0,                   // event category
						SVC_ERROR,           // event identifier
						NULL,                // no security identifier
						2,                   // size of lpszStrings array
						0,                   // no binary data
						lpszStrings,         // array of strings
						NULL);               // no binary data

			DeregisterEventSource(hEventSource);
			LocalFree(lpMsgBuf);
		}
		else
		{
			StringCchPrintf(Buffer, 180, TEXT("Error: %s"), szFunction);

			lpszStrings[0] = SVCNAME;
			lpszStrings[1] = Buffer;

			ReportEvent(hEventSource,        // event log handle
						EVENTLOG_ERROR_TYPE, // event type
						0,                   // event category
						SVC_ERROR,           // event identifier
						NULL,                // no security identifier
						2,                   // size of lpszStrings array
						0,                   // no binary data
						lpszStrings,         // array of strings
						NULL);               // no binary data

			DeregisterEventSource(hEventSource);
		}
    }
}

VOID SvcReportInfoEvent(LPTSTR szFunction) 
{ 
    HANDLE hEventSource;
    LPCTSTR lpszStrings[2];
    TCHAR Buffer[80];

    hEventSource = RegisterEventSource(NULL, SVCNAME);

    if( NULL != hEventSource )
    {
		StringCchPrintf(Buffer, 80, TEXT("%s"), szFunction);

        lpszStrings[0] = SVCNAME;
        lpszStrings[1] = Buffer;

        ReportEvent(hEventSource,        // event log handle
					EVENTLOG_INFORMATION_TYPE, // event type
                    0,                   // event category
                    SVC_INFO,            // event identifier
                    NULL,                // no security identifier
                    2,                   // size of lpszStrings array
                    0,                   // no binary data
                    lpszStrings,         // array of strings
                    NULL);               // no binary data

        DeregisterEventSource(hEventSource);
    }
}

VOID __stdcall DoStartSvc()
{
    SERVICE_STATUS_PROCESS ssStatus; 
    DWORD dwOldCheckPoint; 
    DWORD dwStartTickCount;
    DWORD dwWaitTime;
    DWORD dwBytesNeeded;

    // Get a handle to the SCM database. 
 
    schSCManager = OpenSCManager( 
        NULL,                    // local computer
        NULL,                    // servicesActive database 
        SC_MANAGER_ALL_ACCESS);  // full access rights 
 
    if (NULL == schSCManager) 
    {
        printf("OpenSCManager failed (%d)\n", GetLastError());
        return;
    }

    // Get a handle to the service.

    schService = OpenService( 
        schSCManager,         // SCM database 
        SVCNAME,            // name of service 
        SERVICE_ALL_ACCESS);  // full access 
 
    if (schService == NULL)
    { 
        printf("OpenService failed (%d)\n", GetLastError()); 
        CloseServiceHandle(schSCManager);
        return;
    }    

    // Check the status in case the service is not stopped. 

    if (!QueryServiceStatusEx( 
            schService,                     // handle to service 
            SC_STATUS_PROCESS_INFO,         // information level
            (LPBYTE) &ssStatus,             // address of structure
            sizeof(SERVICE_STATUS_PROCESS), // size of structure
            &dwBytesNeeded ) )              // size needed if buffer is too small
    {
        printf("QueryServiceStatusEx failed (%d)\n", GetLastError());
        CloseServiceHandle(schService); 
        CloseServiceHandle(schSCManager);
        return; 
    }

    // Check if the service is already running. It would be possible 
    // to stop the service here, but for simplicity this example just returns. 

    if(ssStatus.dwCurrentState != SERVICE_STOPPED && ssStatus.dwCurrentState != SERVICE_STOP_PENDING)
    {
        printf("Cannot start the service because it is already running\n");
        CloseServiceHandle(schService); 
        CloseServiceHandle(schSCManager);
        return; 
    }

    // Save the tick count and initial checkpoint.

    dwStartTickCount = GetTickCount();
    dwOldCheckPoint = ssStatus.dwCheckPoint;

    // Wait for the service to stop before attempting to start it.

    while (ssStatus.dwCurrentState == SERVICE_STOP_PENDING)
    {
        // Do not wait longer than the wait hint. A good interval is 
        // one-tenth of the wait hint but not less than 1 second  
        // and not more than 10 seconds. 
 
        dwWaitTime = ssStatus.dwWaitHint / 10;

        if( dwWaitTime < 1000 )
            dwWaitTime = 1000;
        else if ( dwWaitTime > 10000 )
            dwWaitTime = 10000;

        Sleep( dwWaitTime );

        // Check the status until the service is no longer stop pending. 
 
        if (!QueryServiceStatusEx( 
                schService,                     // handle to service 
                SC_STATUS_PROCESS_INFO,         // information level
                (LPBYTE) &ssStatus,             // address of structure
                sizeof(SERVICE_STATUS_PROCESS), // size of structure
                &dwBytesNeeded ) )              // size needed if buffer is too small
        {
            printf("QueryServiceStatusEx failed (%d)\n", GetLastError());
            CloseServiceHandle(schService); 
            CloseServiceHandle(schSCManager);
            return; 
        }

        if ( ssStatus.dwCheckPoint > dwOldCheckPoint )
        {
            // Continue to wait and check.

            dwStartTickCount = GetTickCount();
            dwOldCheckPoint = ssStatus.dwCheckPoint;
        }
        else
        {
            if(GetTickCount()-dwStartTickCount > ssStatus.dwWaitHint)
            {
                printf("Timeout waiting for service to stop\n");
                CloseServiceHandle(schService); 
                CloseServiceHandle(schSCManager);
                return; 
            }
        }
    }

    // Attempt to start the service.

    if (!StartService(
            schService,  // handle to service 
            0,           // number of arguments 
            NULL) )      // no arguments 
    {
        printf("StartService failed (%d)\n", GetLastError());
        CloseServiceHandle(schService); 
        CloseServiceHandle(schSCManager);
        return; 
    }
    else printf("Service start pending...\n"); 

    // Check the status until the service is no longer start pending. 
 
    if (!QueryServiceStatusEx( 
            schService,                     // handle to service 
            SC_STATUS_PROCESS_INFO,         // info level
            (LPBYTE) &ssStatus,             // address of structure
            sizeof(SERVICE_STATUS_PROCESS), // size of structure
            &dwBytesNeeded ) )              // if buffer too small
    {
        printf("QueryServiceStatusEx failed (%d)\n", GetLastError());
        CloseServiceHandle(schService); 
        CloseServiceHandle(schSCManager);
        return; 
    }
 
    // Save the tick count and initial checkpoint.

    dwStartTickCount = GetTickCount();
    dwOldCheckPoint = ssStatus.dwCheckPoint;

    while (ssStatus.dwCurrentState == SERVICE_START_PENDING) 
    { 
        // Do not wait longer than the wait hint. A good interval is 
        // one-tenth the wait hint, but no less than 1 second and no 
        // more than 10 seconds. 
 
        dwWaitTime = ssStatus.dwWaitHint / 10;

        if( dwWaitTime < 1000 )
            dwWaitTime = 1000;
        else if ( dwWaitTime > 10000 )
            dwWaitTime = 10000;

        Sleep( dwWaitTime );

        // Check the status again. 
 
        if (!QueryServiceStatusEx( 
            schService,             // handle to service 
            SC_STATUS_PROCESS_INFO, // info level
            (LPBYTE) &ssStatus,             // address of structure
            sizeof(SERVICE_STATUS_PROCESS), // size of structure
            &dwBytesNeeded ) )              // if buffer too small
        {
            printf("QueryServiceStatusEx failed (%d)\n", GetLastError());
            break; 
        }
 
        if ( ssStatus.dwCheckPoint > dwOldCheckPoint )
        {
            // Continue to wait and check.

            dwStartTickCount = GetTickCount();
            dwOldCheckPoint = ssStatus.dwCheckPoint;
        }
        else
        {
            if(GetTickCount()-dwStartTickCount > ssStatus.dwWaitHint)
            {
                // No progress made within the wait hint.
                break;
            }
        }
    } 

    // Determine whether the service is running.

    if (ssStatus.dwCurrentState == SERVICE_RUNNING) 
    {
        printf("Service started successfully.\n"); 
    }
    else 
    { 
        printf("Service not started. \n");
        printf("  Current State: %d\n", ssStatus.dwCurrentState); 
        printf("  Exit Code: %d\n", ssStatus.dwWin32ExitCode); 
        printf("  Check Point: %d\n", ssStatus.dwCheckPoint); 
        printf("  Wait Hint: %d\n", ssStatus.dwWaitHint); 
    } 

    CloseServiceHandle(schService); 
    CloseServiceHandle(schSCManager);
}


VOID __stdcall DoUpdateSvcDacl()
{
    EXPLICIT_ACCESS      ea;
    SECURITY_DESCRIPTOR  sd;
    PSECURITY_DESCRIPTOR psd            = NULL;
    PACL                 pacl           = NULL;
    PACL                 pNewAcl        = NULL;
    BOOL                 bDaclPresent   = FALSE;
    BOOL                 bDaclDefaulted = FALSE;
    DWORD                dwError        = 0;
    DWORD                dwSize         = 0;
    DWORD                dwBytesNeeded  = 0;

    // Get a handle to the SCM database. 
 
    schSCManager = OpenSCManager( 
        NULL,                    // local computer
        NULL,                    // ServicesActive database 
        SC_MANAGER_ALL_ACCESS);  // full access rights 
 
    if (NULL == schSCManager) 
    {
        printf("OpenSCManager failed (%d)\n", GetLastError());
        return;
    }

    // Get a handle to the service

    schService = OpenService( 
        schSCManager,              // SCManager database 
        SVCNAME,                 // name of service 
        READ_CONTROL | WRITE_DAC); // access
 
    if (schService == NULL)
    { 
        printf("OpenService failed (%d)\n", GetLastError()); 
        CloseServiceHandle(schSCManager);
        return;
    }    

    // Get the current security descriptor.

    if (!QueryServiceObjectSecurity(schService,
        DACL_SECURITY_INFORMATION, 
        &psd,           // using NULL does not work on all versions
        0, 
        &dwBytesNeeded))
    {
        if (GetLastError() == ERROR_INSUFFICIENT_BUFFER)
        {
            dwSize = dwBytesNeeded;
            psd = (PSECURITY_DESCRIPTOR)HeapAlloc(GetProcessHeap(),
                    HEAP_ZERO_MEMORY, dwSize);
            if (psd == NULL)
            {
                // Note: HeapAlloc does not support GetLastError.
                printf("HeapAlloc failed\n");
                goto dacl_cleanup;
            }
  
            if (!QueryServiceObjectSecurity(schService,
                DACL_SECURITY_INFORMATION, psd, dwSize, &dwBytesNeeded))
            {
                printf("QueryServiceObjectSecurity failed (%d)\n", GetLastError());
                goto dacl_cleanup;
            }
        }
        else 
        {
            printf("QueryServiceObjectSecurity failed (%d)\n", GetLastError());
            goto dacl_cleanup;
        }
    }

    // Get the DACL.

    if (!GetSecurityDescriptorDacl(psd, &bDaclPresent, &pacl,
                                   &bDaclDefaulted))
    {
        printf("GetSecurityDescriptorDacl failed(%d)\n", GetLastError());
        goto dacl_cleanup;
    }

    // Build the ACE.

    BuildExplicitAccessWithName(&ea, TEXT("GUEST"),
        SERVICE_START | SERVICE_STOP | READ_CONTROL | DELETE,
        SET_ACCESS, NO_INHERITANCE);

    dwError = SetEntriesInAcl(1, &ea, pacl, &pNewAcl);
    if (dwError != ERROR_SUCCESS)
    {
        printf("SetEntriesInAcl failed(%d)\n", dwError);
        goto dacl_cleanup;
    }

    // Initialize a new security descriptor.

    if (!InitializeSecurityDescriptor(&sd, 
        SECURITY_DESCRIPTOR_REVISION))
    {
        printf("InitializeSecurityDescriptor failed(%d)\n", GetLastError());
        goto dacl_cleanup;
    }

    // Set the new DACL in the security descriptor.

    if (!SetSecurityDescriptorDacl(&sd, TRUE, pNewAcl, FALSE))
    {
        printf("SetSecurityDescriptorDacl failed(%d)\n", GetLastError());
        goto dacl_cleanup;
    }

    // Set the new DACL for the service object.

    if (!SetServiceObjectSecurity(schService, 
        DACL_SECURITY_INFORMATION, &sd))
    {
        printf("SetServiceObjectSecurity failed(%d)\n", GetLastError());
        goto dacl_cleanup;
    }
    else printf("Service DACL updated successfully\n");

dacl_cleanup:
    CloseServiceHandle(schSCManager);
    CloseServiceHandle(schService);

    if(NULL != pNewAcl)
        LocalFree((HLOCAL)pNewAcl);
    if(NULL != psd)
        HeapFree(GetProcessHeap(), 0, (LPVOID)psd);
}


VOID __stdcall DoStopSvc()
{
    SERVICE_STATUS_PROCESS ssp;
    DWORD dwStartTime = GetTickCount();
    DWORD dwBytesNeeded;
    DWORD dwTimeout = 30000; // 30-second time-out
    DWORD dwWaitTime;

    // Get a handle to the SCM database. 
 
    schSCManager = OpenSCManager( 
        NULL,                    // local computer
        NULL,                    // ServicesActive database 
        SC_MANAGER_ALL_ACCESS);  // full access rights 
 
    if (NULL == schSCManager) 
    {
        printf("OpenSCManager failed (%d)\n", GetLastError());
        return;
    }

    // Get a handle to the service.

    schService = OpenService( 
        schSCManager,         // SCM database 
        SVCNAME,            // name of service 
        SERVICE_STOP | 
        SERVICE_QUERY_STATUS | 
        SERVICE_ENUMERATE_DEPENDENTS);  
 
    if (schService == NULL)
    { 
        printf("OpenService failed (%d)\n", GetLastError()); 
        CloseServiceHandle(schSCManager);
        return;
    }    

    // Make sure the service is not already stopped.

    if ( !QueryServiceStatusEx( 
            schService, 
            SC_STATUS_PROCESS_INFO,
            (LPBYTE)&ssp, 
            sizeof(SERVICE_STATUS_PROCESS),
            &dwBytesNeeded ) )
    {
        printf("QueryServiceStatusEx failed (%d)\n", GetLastError()); 
        goto stop_cleanup;
    }

    if ( ssp.dwCurrentState == SERVICE_STOPPED )
    {
        printf("Service is already stopped.\n");
        goto stop_cleanup;
    }

    // If a stop is pending, wait for it.

    while ( ssp.dwCurrentState == SERVICE_STOP_PENDING ) 
    {
        printf("Service stop pending...\n");

        // Do not wait longer than the wait hint. A good interval is 
        // one-tenth of the wait hint but not less than 1 second  
        // and not more than 10 seconds. 
 
        dwWaitTime = ssp.dwWaitHint / 10;

        if( dwWaitTime < 1000 )
            dwWaitTime = 1000;
        else if ( dwWaitTime > 10000 )
            dwWaitTime = 10000;

        Sleep( dwWaitTime );

        if ( !QueryServiceStatusEx( 
                 schService, 
                 SC_STATUS_PROCESS_INFO,
                 (LPBYTE)&ssp, 
                 sizeof(SERVICE_STATUS_PROCESS),
                 &dwBytesNeeded ) )
        {
            printf("QueryServiceStatusEx failed (%d)\n", GetLastError()); 
            goto stop_cleanup;
        }

        if ( ssp.dwCurrentState == SERVICE_STOPPED )
        {
            printf("Service stopped successfully.\n");
            goto stop_cleanup;
        }

        if ( GetTickCount() - dwStartTime > dwTimeout )
        {
            printf("Service stop timed out.\n");
            goto stop_cleanup;
        }
    }

    // If the service is running, dependencies must be stopped first.

    StopDependentServices();

    // Send a stop code to the service.

    if ( !ControlService( 
            schService, 
            SERVICE_CONTROL_STOP, 
            (LPSERVICE_STATUS) &ssp ) )
    {
        printf( "ControlService failed (%d)\n", GetLastError() );
        goto stop_cleanup;
    }

    // Wait for the service to stop.

    while ( ssp.dwCurrentState != SERVICE_STOPPED ) 
    {
        Sleep( ssp.dwWaitHint );
        if ( !QueryServiceStatusEx( 
                schService, 
                SC_STATUS_PROCESS_INFO,
                (LPBYTE)&ssp, 
                sizeof(SERVICE_STATUS_PROCESS),
                &dwBytesNeeded ) )
        {
            printf( "QueryServiceStatusEx failed (%d)\n", GetLastError() );
            goto stop_cleanup;
        }

        if ( ssp.dwCurrentState == SERVICE_STOPPED )
            break;

        if ( GetTickCount() - dwStartTime > dwTimeout )
        {
            printf( "Wait timed out\n" );
            goto stop_cleanup;
        }
    }
    printf("Service stopped successfully\n");

stop_cleanup:
    CloseServiceHandle(schService); 
    CloseServiceHandle(schSCManager);
}

BOOL __stdcall StopDependentServices()
{
    DWORD i;
    DWORD dwBytesNeeded;
    DWORD dwCount;

    LPENUM_SERVICE_STATUS   lpDependencies = NULL;
    ENUM_SERVICE_STATUS     ess;
    SC_HANDLE               hDepService;
    SERVICE_STATUS_PROCESS  ssp;

    DWORD dwStartTime = GetTickCount();
    DWORD dwTimeout = 30000; // 30-second time-out

    // Pass a zero-length buffer to get the required buffer size.
    if ( EnumDependentServices( schService, SERVICE_ACTIVE, 
         lpDependencies, 0, &dwBytesNeeded, &dwCount ) ) 
    {
         // If the Enum call succeeds, then there are no dependent
         // services, so do nothing.
         return TRUE;
    } 
    else 
    {
        if ( GetLastError() != ERROR_MORE_DATA )
            return FALSE; // Unexpected error

        // Allocate a buffer for the dependencies.
        lpDependencies = (LPENUM_SERVICE_STATUS) HeapAlloc( 
            GetProcessHeap(), HEAP_ZERO_MEMORY, dwBytesNeeded );
  
        if ( !lpDependencies )
            return FALSE;

        __try {
            // Enumerate the dependencies.
            if ( !EnumDependentServices( schService, SERVICE_ACTIVE, 
                lpDependencies, dwBytesNeeded, &dwBytesNeeded,
                &dwCount ) )
            return FALSE;

            for ( i = 0; i < dwCount; i++ ) 
            {
                ess = *(lpDependencies + i);
                // Open the service.
                hDepService = OpenService( schSCManager, 
                   ess.lpServiceName, 
                   SERVICE_STOP | SERVICE_QUERY_STATUS );

                if ( !hDepService )
                   return FALSE;

                __try {
                    // Send a stop code.
                    if ( !ControlService( hDepService, 
                            SERVICE_CONTROL_STOP,
                            (LPSERVICE_STATUS) &ssp ) )
                    return FALSE;

                    // Wait for the service to stop.
                    while ( ssp.dwCurrentState != SERVICE_STOPPED ) 
                    {
                        Sleep( ssp.dwWaitHint );
                        if ( !QueryServiceStatusEx( 
                                hDepService, 
                                SC_STATUS_PROCESS_INFO,
                                (LPBYTE)&ssp, 
                                sizeof(SERVICE_STATUS_PROCESS),
                                &dwBytesNeeded ) )
                        return FALSE;

                        if ( ssp.dwCurrentState == SERVICE_STOPPED )
                            break;

                        if ( GetTickCount() - dwStartTime > dwTimeout )
                            return FALSE;
                    }
                } 
                __finally 
                {
                    // Always release the service handle.
                    CloseServiceHandle( hDepService );
                }
            }
        } 
        __finally 
        {
            // Always free the enumeration buffer.
            HeapFree( GetProcessHeap(), 0, lpDependencies );
        }
    } 
    return TRUE;
}

VOID __stdcall DoQuerySvc()
{
    LPQUERY_SERVICE_CONFIG lpsc; 
    LPSERVICE_DESCRIPTION lpsd;
    DWORD dwBytesNeeded, cbBufSize, dwError; 

    // Get a handle to the SCM database. 
 
    schSCManager = OpenSCManager( 
        NULL,                    // local computer
        NULL,                    // ServicesActive database 
        SC_MANAGER_ALL_ACCESS);  // full access rights 
 
    if (NULL == schSCManager) 
    {
        printf("OpenSCManager failed (%d)\n", GetLastError());
        return;
    }

    // Get a handle to the service.

    schService = OpenService( 
        schSCManager,          // SCM database 
        SVCNAME,             // name of service 
        SERVICE_QUERY_CONFIG); // need query config access 
 
    if (schService == NULL)
    { 
        printf("OpenService failed (%d)\n", GetLastError()); 
        CloseServiceHandle(schSCManager);
        return;
    }

    // Get the configuration information.
 
    if( !QueryServiceConfig( 
        schService, 
        NULL, 
        0, 
        &dwBytesNeeded))
    {
        dwError = GetLastError();
        if( ERROR_INSUFFICIENT_BUFFER == dwError )
        {
            cbBufSize = dwBytesNeeded;
            lpsc = (LPQUERY_SERVICE_CONFIG) LocalAlloc(LMEM_FIXED, cbBufSize);
        }
        else
        {
            printf("QueryServiceConfig failed (%d)", dwError);
            goto cleanup; 
        }
    }
  
    if( !QueryServiceConfig( 
        schService, 
        lpsc, 
        cbBufSize, 
        &dwBytesNeeded) ) 
    {
        printf("QueryServiceConfig failed (%d)", GetLastError());
        goto cleanup;
    }

    if( !QueryServiceConfig2( 
        schService, 
        SERVICE_CONFIG_DESCRIPTION,
        NULL, 
        0, 
        &dwBytesNeeded))
    {
        dwError = GetLastError();
        if( ERROR_INSUFFICIENT_BUFFER == dwError )
        {
            cbBufSize = dwBytesNeeded;
            lpsd = (LPSERVICE_DESCRIPTION) LocalAlloc(LMEM_FIXED, cbBufSize);
        }
        else
        {
            printf("QueryServiceConfig2 failed (%d)", dwError);
            goto cleanup; 
        }
    }
 
    if (! QueryServiceConfig2( 
        schService, 
        SERVICE_CONFIG_DESCRIPTION,
        (LPBYTE) lpsd, 
        cbBufSize, 
        &dwBytesNeeded) ) 
    {
        printf("QueryServiceConfig2 failed (%d)", GetLastError());
        goto cleanup;
    }
 
    // Print the configuration information.
 
    _tprintf(TEXT("%s configuration: \n"), SVCNAME);
    _tprintf(TEXT("  Type: 0x%x\n"), lpsc->dwServiceType);
    _tprintf(TEXT("  Start Type: 0x%x\n"), lpsc->dwStartType);
    _tprintf(TEXT("  Error Control: 0x%x\n"), lpsc->dwErrorControl);
    _tprintf(TEXT("  Binary path: %s\n"), lpsc->lpBinaryPathName);
    _tprintf(TEXT("  Account: %s\n"), lpsc->lpServiceStartName);

    if (lpsd->lpDescription != NULL && lstrcmp(lpsd->lpDescription, TEXT("")) != 0)
        _tprintf(TEXT("  Description: %s\n"), lpsd->lpDescription);
    if (lpsc->lpLoadOrderGroup != NULL && lstrcmp(lpsc->lpLoadOrderGroup, TEXT("")) != 0)
        _tprintf(TEXT("  Load order group: %s\n"), lpsc->lpLoadOrderGroup);
    if (lpsc->dwTagId != 0)
        _tprintf(TEXT("  Tag ID: %d\n"), lpsc->dwTagId);
    if (lpsc->lpDependencies != NULL && lstrcmp(lpsc->lpDependencies, TEXT("")) != 0)
        _tprintf(TEXT("  Dependencies: %s\n"), lpsc->lpDependencies);
 
    LocalFree(lpsc); 
    LocalFree(lpsd);

cleanup:
    CloseServiceHandle(schService); 
    CloseServiceHandle(schSCManager);
}

VOID __stdcall DoDisableSvc()
{
    // Get a handle to the SCM database.  
    schSCManager = OpenSCManager( 
        NULL,                    // local computer
        NULL,                    // ServicesActive database 
        SC_MANAGER_ALL_ACCESS);  // full access rights 
 
    if (NULL == schSCManager) 
    {
        printf("OpenSCManager failed (%d)\n", GetLastError());
        return;
    }

    // Get a handle to the service.

    schService = OpenService( 
        schSCManager,            // SCM database 
        SVCNAME,               // name of service 
        SERVICE_CHANGE_CONFIG);  // need change config access 
 
    if (schService == NULL)
    { 
        printf("OpenService failed (%d)\n", GetLastError()); 
        CloseServiceHandle(schSCManager);
        return;
    }    

    // Change the service start type.

    if (! ChangeServiceConfig( 
        schService,        // handle of service 
        SERVICE_NO_CHANGE, // service type: no change 
        SERVICE_DISABLED,  // service start type 
        SERVICE_NO_CHANGE, // error control: no change 
        NULL,              // binary path: no change 
        NULL,              // load order group: no change 
        NULL,              // tag ID: no change 
        NULL,              // dependencies: no change 
        NULL,              // account name: no change 
        NULL,              // password: no change 
        NULL) )            // display name: no change
    {
        printf("ChangeServiceConfig failed (%d)\n", GetLastError()); 
    }
    else printf("Service disabled successfully.\n"); 

    CloseServiceHandle(schService); 
    CloseServiceHandle(schSCManager);
}

VOID __stdcall DoEnableSvc()
{
    // Get a handle to the SCM database.  
    schSCManager = OpenSCManager( 
        NULL,                    // local computer
        NULL,                    // ServicesActive database 
        SC_MANAGER_ALL_ACCESS);  // full access rights 
 
    if (NULL == schSCManager) 
    {
        printf("OpenSCManager failed (%d)\n", GetLastError());
        return;
    }

    // Get a handle to the service.

    schService = OpenService( 
        schSCManager,            // SCM database 
        SVCNAME,               // name of service 
        SERVICE_CHANGE_CONFIG);  // need change config access 
 
    if (schService == NULL)
    { 
        printf("OpenService failed (%d)\n", GetLastError()); 
        CloseServiceHandle(schSCManager);
        return;
    }    

    // Change the service start type.

    if (! ChangeServiceConfig( 
        schService,            // handle of service 
        SERVICE_NO_CHANGE,     // service type: no change 
        SERVICE_DEMAND_START,  // service start type 
        SERVICE_NO_CHANGE,     // error control: no change 
        NULL,                  // binary path: no change 
        NULL,                  // load order group: no change 
        NULL,                  // tag ID: no change 
        NULL,                  // dependencies: no change 
        NULL,                  // account name: no change 
        NULL,                  // password: no change 
        NULL) )                // display name: no change
    {
        printf("ChangeServiceConfig failed (%d)\n", GetLastError()); 
    }
    else printf("Service enabled successfully.\n"); 

    CloseServiceHandle(schService); 
    CloseServiceHandle(schSCManager);
}


VOID __stdcall DoUpdateSvcDesc()
{
    SERVICE_DESCRIPTION sd;
    LPTSTR szDesc = TEXT("This is a test description");

    // Get a handle to the SCM database. 
 
    schSCManager = OpenSCManager( 
        NULL,                    // local computer
        NULL,                    // ServicesActive database 
        SC_MANAGER_ALL_ACCESS);  // full access rights 
 
    if (NULL == schSCManager) 
    {
        printf("OpenSCManager failed (%d)\n", GetLastError());
        return;
    }

    // Get a handle to the service.

    schService = OpenService( 
        schSCManager,            // SCM database 
        SVCNAME,               // name of service 
        SERVICE_CHANGE_CONFIG);  // need change config access 
 
    if (schService == NULL)
    { 
        printf("OpenService failed (%d)\n", GetLastError()); 
        CloseServiceHandle(schSCManager);
        return;
    }    

    // Change the service description.

    sd.lpDescription = szDesc;

    if( !ChangeServiceConfig2(
        schService,                 // handle to service
        SERVICE_CONFIG_DESCRIPTION, // change: description
        &sd) )                      // new description
    {
        printf("ChangeServiceConfig2 failed\n");
    }
    else printf("Service description updated successfully.\n");

    CloseServiceHandle(schService); 
    CloseServiceHandle(schSCManager);
}

VOID __stdcall DoDeleteSvc()
{
    // Get a handle to the SCM database.  
    schSCManager = OpenSCManager( 
        NULL,                    // local computer
        NULL,                    // ServicesActive database 
        SC_MANAGER_ALL_ACCESS);  // full access rights 
 
    if (NULL == schSCManager) 
    {
        printf("OpenSCManager failed (%d)\n", GetLastError());
        return;
    }

    // Get a handle to the service.

    schService = OpenService( 
        schSCManager,       // SCM database 
        SVCNAME,          // name of service 
        DELETE);            // need delete access 
 
    if (schService == NULL)
    { 
        printf("OpenService failed (%d)\n", GetLastError()); 
        CloseServiceHandle(schSCManager);
        return;
    }

    // Delete the service.
 
    if (! DeleteService(schService) ) 
    {
        printf("DeleteService failed (%d)\n", GetLastError()); 
    }
    else printf("Service deleted successfully\n"); 
 
    CloseServiceHandle(schService); 
    CloseServiceHandle(schSCManager);
}
VOID __stdcall DisplayUsage()
{
    printf("Description:\n");
    printf("\tCommand-line tool to install/delete/modify %s.\n\n",SVCNAME);
    printf("Usage:\n");
    printf("\tsvcconfig [command]\n\n");
    printf("\t[command]\n");
	printf("\tinstall\tdelete\n");
	printf("\tenable\tdisable\n");
	printf("\tstart\tstop\tquery\n");
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

bool IoControl(IoCtrl ioControlCode, void *inBuffer, int inBufferSize, void *outBuffer, int outBufferSize, LPDWORD bytesReturned)
{
    OVERLAPPED overlapped;
    BOOL deviceIoControl;
    int ret;

    DebugIoControl(_T("IoControl ENTER"));
    if (hReadPipe == INVALID_HANDLE_VALUE)
        return false;

    DebugIoControl(_T("IoControl: hReadPipe is valid"));

    memset(&overlapped, 0, sizeof(overlapped));

	DWORD dw;
	HANDLE handleArray[2];
	handleArray[0] = overlapped.hEvent = CreateEvent(NULL, false, false, NULL);
    if (!overlapped.hEvent)
        return false;	
	handleArray[1] = hModeChangeEvent;
    DebugIoControl(_T("IoControl: Event created successfully"));

	EventTrace(_T("InSize = %d, OutSize = %d"),inBufferSize,outBufferSize);
    // Send a control code directly to my device driver
    deviceIoControl = DeviceIoControl(hReadPipe,
                                      ioControlCode,
                                      inBuffer,
                                      inBufferSize, 
                                      outBuffer, 
                                      outBufferSize, 
                                      bytesReturned, 
                                      (LPOVERLAPPED)&overlapped);
    //DebugIoControl(_T("IoControl: after calling DeviceIoControl(), returned=%d, GetLast = %d"), deviceIoControl, GetLastError());
    if (deviceIoControl == FALSE)
    {
        if  (GetLastError() != ERROR_IO_PENDING)
        {
            DebugIoControl(_T("IoControl: GetLastError() != ERROR_IO_PENDING"));
            CancelIo(hReadPipe);
            CloseHandle(overlapped.hEvent);
            return false;
        }
        // Wait for event
        DebugIoControl(_T("IoControl: about to wait for the event..."));
		DWORD nWait = 1;
		if (ioControlCode == IoCtrl_Receive)
			nWait = 2; 
			//Only receive should be slow.  We should ignore hModeChangeEvent unless
			//this is a receive command
		dw = WaitForMultipleObjects(nWait, handleArray, FALSE, INFINITE);
		switch (dw)
		{
		case WAIT_OBJECT_0:
			ret = GetOverlappedResult(hReadPipe, (LPOVERLAPPED)&overlapped, bytesReturned, false);
			if (ret == 0)
				DebugIoControl(_T("IoControl: GetOverlappedResult FAILED: error=0x%x"), GetLastError());
			DebugIoControl(_T("IoControl: bytesReturned=%d"), *bytesReturned);
			break;

		case WAIT_OBJECT_0 + 1:
			DebugIoControl(_T("IoControl: WaitForSingleObject stopped for mode change"));
			CancelIo(hReadPipe);
			break;

		case WAIT_FAILED:
            DebugIoControl(_T("IoControl: WaitForSingleObject failed"));
			CancelIo(hReadPipe);
			break;
        }
    }
    DebugIoControl(_T("IoControl EXIT"));
    CloseHandle(overlapped.hEvent);
    return dw == WAIT_OBJECT_0;
}

static void VistaStartReceive(int receivePort, int timeout)
{
    int bytesRead;
    StartReceiveParams parms;

    parms.Receiver = receivePort;
    parms.Timeout = timeout;
	Trace(_T("VistaStartReceive() ENTER"));
    if (!IoControl(IoCtrl_StartReceive, (void *)&parms, sizeof(parms), NULL, 0, (LPDWORD)&bytesRead))
    {
        Trace(_T("VistaStartReceive(port=%d, timeout=%d) failed"), receivePort, timeout);
    }
}

static bool VistaStopReceive(void)
{
    int bytesRead;
	Trace(_T("VistaStopReceive() ENTER"));
    if (!IoControl(IoCtrl_StopReceive, NULL, 0, NULL, 0, (LPDWORD)&bytesRead))
    {
        Trace(_T("IoCtrl_StopReceive() failed"));
		return false;
    }
	return true;
}

bool VistaGetDeviceCapabilities(void)
{
    int bytesReturned;
    //MCEDeviceCapabilities parms; //switched to a global deviceCapabilities parameter

    Trace(_T("VistaGetDeviceCapabilities() ENTER"));

    if (!IoControl(IoCtrl_GetDetails, NULL, 0, (void *)&deviceCapabilities, sizeof(MCEDeviceCapabilities), (LPDWORD)&bytesReturned))
    {
        Trace(_T("VistaGetDeviceCapabilities(),  IoControl failed"));
        return false;
    }

    if (bytesReturned < sizeof(deviceCapabilities))
    {
        Trace(_T("VistaGetDeviceCapabilities(), IoControl returned not enough bytes"));
        return false;
    }

    _numTxPorts = static_cast<int>(deviceCapabilities.TransmitPorts);
    //_numRxPorts = parms.ReceivePorts;
    _learnPortMask = static_cast<int>(deviceCapabilities.LearningMask);

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

    Trace(_T("Device Capabilities:"));
    Trace(_T("NumTxPorts: %d"), _numTxPorts);
    Trace(_T("NumRxPorts: %d"), deviceCapabilities.ReceivePorts);
    Trace(_T("LearnPortMask: 0x%x"), _learnPortMask);
    Trace(_T("ReceivePort: %d"), _receivePort);
    Trace(_T("LearnPort: %d"), _learnPort);
    Trace(_T("DetailsFlags: 0x%x"), deviceCapabilities.DetailsFlags);
    return true;
}

static void TransmitIR(char *data, int dataLen)
{
	//Make this easy for the driver, make the caller of TransmitIR get the setup
	//First four parameters (4 or 8 bytes per parameters, depending on OS) are input settings:
	//  portmask, carrierperiod, flags, pulsesize
	//Next three parameters are the "chunk" parameters:
	//  offset, repeatcount, bytecount
	//Rest of the data is the specific pulse data.
	DWORD bytesReturned;
	EventTraceOut(_T("In TransmitIR"));
	int chunkLen = dataLen - sizeof(TransmitParams);
	if (chunkLen < sizeof(TransmitChunk) || chunkLen > 1024)
	{
		EventTraceError(_T("Invalid blaster input (datasize = %d)"),chunkLen);
		return;
	}
	AvailableBlasters ab;
	IoControl(IoCtrl_GetBlasters, NULL, 0, &ab, sizeof(AvailableBlasters),(LPDWORD)&bytesReturned);
	EventTraceOut(_T("Blasters result (got %d): %Id"),bytesReturned,ab.Blasters);
	//Debug(_T("Blasters result (got %d): %Id"),bytesReturned,ab.Blasters);
	((TransmitParams*)data)->TransmitPortMask = ab.Blasters;
	IoControl(IoCtrl_Transmit, data, sizeof(TransmitParams), data+sizeof(TransmitParams), chunkLen, (LPDWORD)&bytesReturned);
	EventTraceOut(_T("After transmit (got %d)"),bytesReturned);
	//Debug(_T("After transmit (got %d)"),bytesReturned);

	// Force a delay between blasts (hopefully solves back-to-back blast errors) ...
	//Sleep(PacketTimeout);
}

static UCHAR TestTransmit()
{
	EventTraceOut(_T("In TestTransmit"));
	DWORD bytesReturned;
	DWORD Command[] = {0, 1, 272, 2650, -900, 400, -500, 400, -500, 400, -950, 400, -950, 1300, -950, 400, -500, 400, -500, 400, -500, 400, -500, 400, -500, 400, -500, 400, -500, 400, -500, 400, -500, 400, -500, 850, -500, 400, -500, 400, -500, 400, -950, 400, -500, 400, -500, 400, -500, 400, -500, 850, -950, 400, -500, 400, -500, 400, -500, 400, -500, 400, -500, 400, -500, 400, -500, 400, -500, 850, -69700};
	TransmitParams Params = {0,27,0,0};
	AvailableBlasters ab;
	IoControl(IoCtrl_GetBlasters, NULL, 0, &ab, sizeof(AvailableBlasters),(LPDWORD)&bytesReturned);
	EventTraceOut(_T("Blasters result (got %d): %Id"),bytesReturned,ab.Blasters);
	Params.TransmitPortMask = ab.Blasters;
	IoControl(IoCtrl_Transmit, &Params, sizeof(TransmitParams), &Command, sizeof(Command), (LPDWORD)&bytesReturned);
	EventTraceOut(_T("After test transmit (got %d)"),bytesReturned);
	return 0;
}
static DWORD WINAPI MceIrVistaThreadProc(LPVOID lpParameter)
{
    DWORD bytesRead;
    ReceiveParams *receiveParamsPtr;
    int receiveParamsSize = sizeof(ReceiveParams) + DeviceBufferSize + 8;
    receiveParamsPtr = (ReceiveParams *)calloc(1, receiveParamsSize);
    receiveParamsPtr->ByteCount = DeviceBufferSize;
    int ret;
	keepRunning = true;
	bool doneOnce = false, validPort = false;
	DWORD maxChunkLen = 100+sizeof(ReceiveParams);

	DebugIoControl(_T("Device Thread, starting IR device I/O thread"));
	while (keepRunning) //Outer Connect/HandleData 
	{
		while (keepRunning && !MceIrOpenPipes()) //Inner Connect loop
		{
			DebugIoControl(_T("Device Thread, in connect loop"));
			Sleep(1000);
			if (!doneOnce)
			{
				doneOnce = true;  //Only post this message once
				SvcReportInfoEvent(_T("Device Thread, no device present, will keep trying to connect"));
			}
		}
		if (keepRunning && newConnection)
		{
			DebugIoControl(_T("Device Thread, connected to IR device"));
		}
		if (keepRunning) //Inner HandleData loop
		{
			if (VistaGetDeviceCapabilities())
			{
				validPort = true;
				isDeviceConnected = true;
				if (newConnection)
				{
					portToUse = _receivePort;
					if (doneOnce) //Report that we eventually connected
					{
						SvcReportInfoEvent(_T("Device Thread, able to connect to IR device"));
					}
					doneOnce = false; //If we lose the connection, we should report it again above
					newConnection = false;
					modeChanged = true;
				}
			}
			if (!validPort)
				break;
			DebugIoControl(_T("Device Thread, before StartReceive"));
			VistaStartReceive(portToUse, PacketTimeout);
			DebugIoControl(_T("Device Thread, after StartReceive"));
			if (modeChanged) //we just changed modes, so set to false
			{
				if (portToUse == _receivePort)
					DebugIoControl(_T("Device Thread, mode set to normal receive port"));
				else
					DebugIoControl(_T("Device Thread, mode set to learn receive port"));
				modeChanged = false;
				ResetEvent(hModeChangeEvent);
			}
			while (keepRunning && !modeChanged)
			{
				DebugIoControl(_T("Device Thread, before IoControl"));
				ret = IoControl(IoCtrl_Receive, NULL, 0, receiveParamsPtr, receiveParamsSize, (LPDWORD)&bytesRead);
				if (!ret || bytesRead <= sizeof(ReceiveParams))
				{
					DebugIoControl(_T("Device Thread, problem talking to device, breaking out of I/O loop"));
					break;
				}
				EventTrace(_T("Device Thread, able to decode"));

				if (isPipeConnected)
				{
					PUCHAR ptr = (PUCHAR)receiveParamsPtr;	
					ReceiveChunk* pChunk;
					EnterCriticalSection(&CriticalSection_Deque);					
					while (bytesRead > maxChunkLen)
					{
						pChunk = new ReceiveChunk(ptr,maxChunkLen);
						bytesRead -= maxChunkLen;
						ptr += maxChunkLen;
						ReceivedData.push_back(pChunk);
					}
					pChunk = new ReceiveChunk(ptr,bytesRead);
					ReceivedData.push_back(pChunk);
					SetEvent(hDataReady);
					LeaveCriticalSection(&CriticalSection_Deque);
				}
			}
			// perform some cleanup
			DebugIoControl(_T("Device Thread, before StopReceive"));
			int i = 0;
			for (; i < 10; i++)
			{
				if (VistaStopReceive())
					break;
				Sleep(10);
			}
			DebugIoControl(_T("Device Thread, after StopReceive (tried %d times)"),i);
			if (hReadPipe != INVALID_HANDLE_VALUE) {
				//IoControl(IoCtrl_Reset, NULL, 0, NULL, 0, (LPDWORD)&bytesRead);
				if (!keepRunning || !modeChanged) //Keep handle open if we are only doing a modeChange
				{
					isDeviceConnected = false;
					CloseHandle(hReadPipe);
					hReadPipe = INVALID_HANDLE_VALUE;
				}
			}
			DebugIoControl(_T("Device Thread, end of Handle Data loop"));
		}
	}
	free(receiveParamsPtr);
	DebugIoControl(_T("Device Thread, closing thread"));
	return 0;
}
static VOID WINAPI CloseNamedPipe()
{
	isPipeConnected = false;
	EventTrace(_T("Disconnecting named pipe"));
	FlushFileBuffers(hOutPipe);
	DisconnectNamedPipe(hOutPipe);
	CloseHandle(hOutPipe);
	EnterCriticalSection(&CriticalSection_Deque);
	while (ReceivedData.size() > 0)
	{
		delete ReceivedData.front();
		ReceivedData.pop_front();
	}
	LeaveCriticalSection(&CriticalSection_Deque);
}
static DWORD WINAPI OutputConnectionsThreadProc(LPVOID lpParameter)
{
    BOOL ConnectionThreadStop = false;
	PSID pEveryoneSID = NULL;
	PSECURITY_DESCRIPTOR pSD = NULL;
	SID_IDENTIFIER_AUTHORITY SIDAuthWorld = SECURITY_WORLD_SID_AUTHORITY;
	SECURITY_ATTRIBUTES sa;
	// Create a well-known SID for the Everyone group.
    if(!AllocateAndInitializeSid(&SIDAuthWorld, 1,
                     SECURITY_WORLD_RID,
                     0, 0, 0, 0, 0, 0, 0,
                     &pEveryoneSID))
    {
        printf("AllocateAndInitializeSid Error %u\n", GetLastError());
        goto Cleanup;
    }
	pSD = (PSECURITY_DESCRIPTOR) LocalAlloc(LPTR, SECURITY_DESCRIPTOR_MIN_LENGTH); 
    if (NULL == pSD) 
    { 
        printf("LocalAlloc Error %u\n", GetLastError());
        goto Cleanup; 
    } 
 
    if (!InitializeSecurityDescriptor(pSD,
            SECURITY_DESCRIPTOR_REVISION)) 
    {  
        printf("InitializeSecurityDescriptor Error %u\n",
                                GetLastError());
        goto Cleanup; 
    } 
 
    // Add the ACL to the security descriptor. 
    if (!SetSecurityDescriptorDacl(pSD, 
            TRUE,     // bDaclPresent flag   
            NULL, 
            FALSE))   // not a default DACL 
    {  
        printf("SetSecurityDescriptorDacl Error %u\n",
                GetLastError());
        goto Cleanup; 
    } 

    // Initialize a security attributes structure.
    sa.nLength = sizeof (SECURITY_ATTRIBUTES);
    sa.lpSecurityDescriptor = pSD;
    sa.bInheritHandle = FALSE;

	OVERLAPPED connectOvlap, writeOvlap, readOvlap, replyOvlap;
	HANDLE      handleArray[4];
	while (!ConnectionThreadStop)
	{
		EventTrace(_T("Creating named pipe"));
		hOutPipe = CreateNamedPipe(_T("\\\\.\\pipe\\MceIr"),
			PIPE_ACCESS_DUPLEX | FILE_FLAG_OVERLAPPED, PIPE_WAIT, 1,
			256,256,1000,&sa);
		if (hOutPipe == INVALID_HANDLE_VALUE) {
			SvcReportErrorEvent(_T("Failed CreateNamedPipe (%s)"));
			return 0;
		}

		memset(&connectOvlap, 0, sizeof(connectOvlap));		
		handleArray[0] = connectOvlap.hEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
		handleArray[1] = hStopEvent;
		ConnectNamedPipe(hOutPipe, &connectOvlap);

		DebugIoControl(_T("***************** OutputConnectionsThreadProc() before wait"));
		EventTrace(_T("Waiting for connection..."));
		DWORD dw = WaitForMultipleObjects(2, handleArray, FALSE, INFINITE);
		switch (dw - WAIT_OBJECT_0)
		{
		case 0:
			break;

		case 1:
			ConnectionThreadStop = true;
			break;
		}
		isPipeConnected = TRUE;
		DebugIoControl(_T("***************** OutputConnectionsThreadProc() after wait, Stop = %d"),ConnectionThreadStop);
		DebugIoControl(_T("***************** OutputConnectionsThreadProc() starting LOOP?"));

		memset(&writeOvlap, 0, sizeof(writeOvlap));	
		memset(&replyOvlap, 0, sizeof(replyOvlap));
		replyOvlap.hEvent = CreateEvent(NULL,FALSE,FALSE,NULL);
		memset(&readOvlap, 0, sizeof(readOvlap));
		handleArray[2] = writeOvlap.hEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
		handleArray[3] = readOvlap.hEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
		handleArray[0] = hDataReady;
		ReadFile(hOutPipe, pDataFromOutpipe, 2048, NULL, &readOvlap);
		ReceiveChunk* pData;
		while (!ConnectionThreadStop && isPipeConnected)
		{		
			EventTrace(_T("Waiting for data or close"));
			DWORD dw = WaitForMultipleObjects(4, handleArray, FALSE, INFINITE);
			switch (dw - WAIT_OBJECT_0)
			{
			case 0:
				DWORD nSent;
				EventTrace(_T("Data available event"));
				EnterCriticalSection(&CriticalSection_Deque);
				pData = ReceivedData.front();
				ReceivedData.pop_front();
				LeaveCriticalSection(&CriticalSection_Deque);
				if (!WriteFile(hOutPipe, pData->data, pData->len, &nSent, &writeOvlap) 
					       && (ERROR_IO_PENDING != GetLastError()))
				{
					CloseNamedPipe();
				}
				break;

			case 1:
				EventTrace(_T("stop event"));
				ConnectionThreadStop = true;
				break;

			case 2:
				EventTrace(_T("write finished event"));
				delete pData;
				EnterCriticalSection(&CriticalSection_Deque);
				if (ReceivedData.size() > 0)
					SetEvent(hDataReady);
				LeaveCriticalSection(&CriticalSection_Deque);	
				break;

			case 3:
				ULONG_PTR nGot = readOvlap.InternalHigh;
				Debug(_T("Data read from namedpipe (got %Id)"),nGot);
				if (nGot == 1) //message, not ir code
				{
					char ch = *pDataFromOutpipe;
					switch (tolower(ch))
					{
					case 'q': //Quit signal
						SvcReportInfoEvent(_T("Quit signal received from namedpipe"));
						CloseNamedPipe();
						break;
					case 'l': //switch to learn mode
						if (isDeviceConnected && portToUse != _learnPort)
						{
							portToUse = _learnPort;
							modeChanged = true;
							SetEvent(hModeChangeEvent);
						}
						break;
					case 'n': //switch to normal mode
						if (isDeviceConnected && portToUse != _receivePort)
						{
							portToUse = _receivePort;
							modeChanged = true;
							SetEvent(hModeChangeEvent);
						}
						break;
					case 'b': //Get Blaster info
						char reply[sizeof(MCEDeviceCapabilities)+sizeof(AvailableBlasters)+1];
						memset(&reply, 0, sizeof(reply));
						reply[0] = 'b';
						if (isDeviceConnected)
						{
							//SvcReportInfoEvent(_T("Blaster Info request received from namedpipe"));
							AvailableBlasters ab;
							DWORD bytesReturned;
							IoControl(IoCtrl_GetBlasters, NULL, 0, &ab, sizeof(AvailableBlasters),(LPDWORD)&bytesReturned);
							Debug(_T("Blasters result (got %d): %Id"),bytesReturned,ab.Blasters);
							memcpy(reply+1,&deviceCapabilities,sizeof(MCEDeviceCapabilities));
							memcpy(reply+1+sizeof(MCEDeviceCapabilities),&ab.Blasters,sizeof(AvailableBlasters));
						}
						if (!WriteFile(hOutPipe, reply, sizeof(MCEDeviceCapabilities)+sizeof(AvailableBlasters)+1, &nSent, &replyOvlap) 
								   && (ERROR_IO_PENDING != GetLastError()))
						{
							Debug(_T("Blasters write failed"));
							CloseNamedPipe();
						}
						WaitForSingleObject(replyOvlap.hEvent, INFINITE);
						break;
					case 't': //Test blaster
						char test_reply[1+sizeof(ULONG_PTR)];
						UCHAR ret;
						memset(&test_reply, 0, sizeof(test_reply));
						test_reply[0] = 't';
						if (isDeviceConnected)
						{
							ret = TestTransmit();
							memcpy(test_reply+1,&ret,1);
						}
						if (!WriteFile(hOutPipe, test_reply, 1+sizeof(ULONG_PTR), &nSent, &replyOvlap) 
								   && (ERROR_IO_PENDING != GetLastError()))
						{
							Debug(_T("Blaster test write failed"));
							CloseNamedPipe();
						}
						WaitForSingleObject(replyOvlap.hEvent, INFINITE);
						Debug(_T("Blaster test result (%c)"),test_reply[1]);
						break;
					default:
						break;
					}
				}
				else
				{
					if (isDeviceConnected)
					{
						int* pInt = reinterpret_cast<int *>(pDataFromOutpipe);
						Debug(_T("read finished event, got %Id, data[0] = %d, data[last] = %d"),nGot,*pInt,*(pInt+nGot/4-1));
						TransmitIR(pDataFromOutpipe,static_cast<int>(nGot));	
					}
				}
				ReadFile(hOutPipe, pDataFromOutpipe, 2048, NULL, &readOvlap);
				break;
			}
		}
		EventTrace(_T("End Loop"));
		DebugIoControl(_T("***************** OutputConnectionsThreadProc() exitting LOOPn"));
	}

    // perform some cleanup
    CloseHandle(hOutPipe);
	CloseHandle(writeOvlap.hEvent);
	CloseHandle(readOvlap.hEvent);
	CloseHandle(replyOvlap.hEvent);
	CloseHandle(connectOvlap.hEvent);

Cleanup:

    if (pEveryoneSID) 
        FreeSid(pEveryoneSID);
    if (pSD) 
        LocalFree(pSD);
	return 0;
}
static BOOL MceIrGetDeviceFileName(LPGUID pGuid, TCHAR *outNameBuf)
{
    HANDLE hDev = MceIrOpenUsbDevice(pGuid, outNameBuf);
    if (hDev != INVALID_HANDLE_VALUE)
    {
		Trace(_T("OpenUsb = TRUE"));
        CloseHandle(hDev);
        return TRUE;
    }

	Trace(_T("OpenUsb = FALSE"));
    return FALSE;
}

static bool MceIrOpenPipes()
{
	if (hReadPipe != INVALID_HANDLE_VALUE)
		return true;

    TCHAR DeviceName[MAX_PATH] = _T("");

	if (MceIrGetDeviceFileName((LPGUID)&GUID_CLASS_IRBUS, DeviceName))
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
            Trace(_T("Failed to open (%s) = %d"), DeviceName, GetLastError());
            return false;
        }
    }
	else
		return false;
	newConnection = true;
	return true;
}

static HANDLE MceIrOpenOneDevice(IN HDEVINFO HardwareDeviceInfo, IN PSP_DEVICE_INTERFACE_DATA DeviceInterfaceData, IN TCHAR *devName)
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


    predictedLength = requiredLength+16;

    functionClassDeviceData = (PSP_DEVICE_INTERFACE_DETAIL_DATA) malloc (predictedLength);
    memset(functionClassDeviceData, 0, predictedLength);
    //functionClassDeviceData->cbSize = sizeof(PSP_DEVICE_INTERFACE_DETAIL_DATA);
	functionClassDeviceData->cbSize = sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA);

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
		SvcReportErrorEvent(_T("FAILED to open MCE IR Device (error at MceIrOpenOneDevice->SetupDiGetDeviceInterfaceDetail)"));
        return INVALID_HANDLE_VALUE;
    }

    // strcpy(devName, functionClassDeviceData->DevicePath); // Deprecated
    _tcscpy_s(devName, MAX_PATH, functionClassDeviceData->DevicePath);
    Debug(_T("Attempting to open %s"), devName);

	//HERE'S THE PROBLEM
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
        SvcReportErrorEvent(_T("FAILED to open MCE IR Device (error at MceIrOpenOneDevice->CreateFile)"));
    }
	EventTrace(_T("SUCCEEDED in opening MCE IR Device"));
    free(functionClassDeviceData);

    return hOut;
}

static HANDLE MceIrOpenUsbDevice(LPGUID  pGuid, TCHAR *outNameBuf)
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
	{
		SvcReportErrorEvent(_T("FAILED to open MCE IR Device (error at MceIrOpenUsbDevice->SetupDiGetClassDevs)"));
        return INVALID_HANDLE_VALUE;
	}

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
			{
                break;
			}
        }
        else
        {
            if (ERROR_NO_MORE_ITEMS == GetLastError())
			{
				SvcReportErrorEvent(_T("FAILED to open MCE IR Device (searched all devices in MceIrOpenUsbDevice)"));
                break;
			}
        }
    }

    // SetupDiDestroyDeviceInfoList() destroys a device information set
    // and frees all associated memory.

    SetupDiDestroyDeviceInfoList(hardwareDeviceInfo);

    return hOut;
}
void TraceOut(LPTSTR szFormat, ...)
{
	if (!szFormat) 
	{
		return;
	}
	TCHAR szTempOutput[500];
    WaitForSingleObject(hTraceMutex, INFINITE);
    va_list args;
    va_start(args, szFormat);
    _vsntprintf_s(szTempOutput, sizeof(szTempOutput), sizeof(szTempOutput)-1, szFormat, args);
    va_end(args);
    OutputDebugString(szTempOutput);
	_tprintf(_T("%s\n"),szTempOutput);
    ReleaseMutex(hTraceMutex);
}
void EventTraceOut(LPTSTR szFormat, ...)
{
	if (!szFormat) 
	{
		return;
	}
    TCHAR szTempOutput[500];
    WaitForSingleObject(hTraceMutex, INFINITE);
    va_list args;
    va_start(args, szFormat);
    _vsntprintf_s(szTempOutput, sizeof(szTempOutput), sizeof(szTempOutput)-1, szFormat, args);
    va_end(args);
	SvcReportInfoEvent(szTempOutput);
    ReleaseMutex(hTraceMutex);
}
void EventTraceError(LPTSTR szFormat, ...)
{
	if (!szFormat) 
	{
		return;
	}
    TCHAR szTempOutput[500];
    WaitForSingleObject(hTraceMutex, INFINITE);
    va_list args;
    va_start(args, szFormat);
    _vsntprintf_s(szTempOutput, sizeof(szTempOutput), sizeof(szTempOutput)-1, szFormat, args);
    va_end(args);
	SvcReportErrorEvent(szTempOutput,false);
    ReleaseMutex(hTraceMutex);
}
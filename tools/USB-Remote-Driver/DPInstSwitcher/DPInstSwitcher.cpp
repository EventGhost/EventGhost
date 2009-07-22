// DPInstSwitcher.cpp : Defines the entry point for the application.
//

#include "stdafx.h"
#include "DPInstSwitcher.h"
#include <stdio.h>
#include <windows.h>
#include <tchar.h>
#include <strsafe.h>

static BOOL IsWow64( void );
static void PrintLastError( const WCHAR* apiname );

#define MAX_LOADSTRING 100



int APIENTRY _tWinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPTSTR    lpCmdLine,
                     int       nCmdShow)
{
    STARTUPINFO         StartupInfo;
    PROCESS_INFORMATION ProcessInformation;

    WCHAR * X86 = TEXT("DPInst_x86.exe /f /lm");
    WCHAR * X64 = TEXT("DPInst_amd64.exe /f /lm");

    WCHAR * AppName = NULL;
    WCHAR * command = NULL;

    if (IsWow64()) 
    {
        AppName = X64;
        wprintf( L"We are on a 64 bit OS.\n" );
    }
    else
    {
        AppName = X86;
        wprintf( L"We are on a 32 bit OS.\n" );
    }

    command = (WCHAR*)HeapAlloc( GetProcessHeap(), 0, (wcslen(AppName)+1)*sizeof(WCHAR) );
    if( command == NULL )
    {
        wprintf( L"Out of memory.\n" );
        return 0;
    }
    
    StringCchCopy( command, wcslen(AppName)+1, AppName );

    ZeroMemory( &ProcessInformation, sizeof( ProcessInformation ) );
    ZeroMemory( &StartupInfo, sizeof( StartupInfo ) );
    StartupInfo.cb = sizeof( STARTUPINFO );    
	StartupInfo.dwFlags = STARTF_FORCEOFFFEEDBACK;
	if( CreateProcess( 
                NULL, 
                command, 
                NULL, 
                NULL, 
                FALSE, 
                0, 
                NULL, 
                NULL, 
                &StartupInfo, 
                &ProcessInformation ) ) 
    {
        wprintf( L"CreateProcess succeeded\n" );
    }
    else
    {
        PrintLastError( L"CreateProcess()" );        
    }

    if( ProcessInformation.hProcess )
    {
        AllowSetForegroundWindow(ProcessInformation.dwProcessId);
		DWORD Ret = WaitForSingleObject( ProcessInformation.hProcess, INFINITE ); 

        if( WAIT_OBJECT_0 == Ret )
            wprintf(L"Process finished.\n" );
        else
            PrintLastError( L"WaitForSingleObject");

        DWORD ExitCode;

        if( GetExitCodeProcess( ProcessInformation.hProcess, &ExitCode ) )
            wprintf( L"Process exit code = 0x%X\n", ExitCode );
        else
            PrintLastError( L"GetExitCodeProcess()" );            

        GetExitCodeThread( ProcessInformation.hThread, &ExitCode );
        wprintf( L"Thread exit code = 0x%X\n", ExitCode );
        
        CloseHandle( ProcessInformation.hProcess );
        CloseHandle( ProcessInformation.hThread );
    }
    else
    {
        wprintf( L"No process created\n");
    }

    if( command ) 
        HeapFree( GetProcessHeap(), 0, command );
    
    return 0;
}
	 
 
typedef UINT (WINAPI* GETSYSTEMWOW64DIRECTORY)(LPTSTR, UINT);

BOOL
IsWow64(void)
{

    GETSYSTEMWOW64DIRECTORY getSystemWow64Directory;
    HMODULE hKernel32;
    TCHAR Wow64Directory[MAX_PATH];

    hKernel32 = GetModuleHandle(TEXT("kernel32.dll"));
    if (hKernel32 == NULL) {
        //
        // This shouldn't happen, but if we can't get 
        // kernel32's module handle then assume we are 
        //on x86.  We won't ever install 32-bit drivers
        // on 64-bit machines, we just want to catch it 
        // up front to give users a better error message.
        //
        return FALSE;
    }

    getSystemWow64Directory = (GETSYSTEMWOW64DIRECTORY)
        GetProcAddress(hKernel32, "GetSystemWow64DirectoryW");

    if (getSystemWow64Directory == NULL) {
        //
        // This most likely means we are running 
        // on Windows 2000, which didn't have this API 
        // and didn't have a 64-bit counterpart.
        //
        return FALSE;
    }

    if (getSystemWow64Directory(Wow64Directory, sizeof(Wow64Directory)/sizeof(TCHAR)) == 0)
	{
        return FALSE;
    }
    
    //
    // GetSystemWow64Directory succeeded 
    // so we are on a 64-bit OS.
    //
    return TRUE;
}
	 
 
void
PrintLastError( const WCHAR* apiname )
{
    DWORD error = GetLastError();
    LPVOID lpvMessageBuffer;
    if( FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
                  NULL, error, 
                  MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), //The user default language
                  (LPTSTR)&lpvMessageBuffer, 0, NULL) )
    {
        _tprintf( TEXT("ERROR: %s: 0x%X: %s\n"), apiname, error, lpvMessageBuffer );
        LocalFree(lpvMessageBuffer);
    }
}	 

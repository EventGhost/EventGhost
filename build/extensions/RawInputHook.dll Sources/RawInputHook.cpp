// hook.cpp : Defines the entry point for the DLL application.
//

#include "stdafx.h"
#include <stdio.h>
#include <stdlib.h>
//#include <Psapi.h>
#include "RawInputHook.h"

#pragma message("library is linking with \"Psapi.lib\"")
//#pragma comment(lib, "Psapi.lib")

//
// struct for hook events
//
typedef struct
{
    int     nCode;
    DWORD   dwHookType;
    WPARAM  wParam;
    LPARAM  lParam;
} HEVENT;

#pragma data_seg(".shared")
HHOOK     gHook = NULL;
HWND      gHwnd = NULL;
HINSTANCE gInst = NULL;
#pragma data_seg()
#pragma comment(linker, "/SECTION:.shared,RWS")

#define DBG OutputDebugString

//
// DLL main function
//
BOOL WINAPI DllMain(HINSTANCE hInst, ULONG uReason, LPVOID lpReserved)
{
    switch(uReason)
    {
        case DLL_PROCESS_ATTACH:
            DBG("HOOK: DLL_PROCESS_ATTACH");
            gInst = hInst;
            DisableThreadLibraryCalls(hInst);
            break;
        case DLL_PROCESS_DETACH:
            // on detaching the DLL, close the MMF
            DBG("HOOK: DLL_PROCESS_DETACH");
            break;
    }    
   
    return TRUE;
}


//
// callback function for hooks
//
LRESULT CALLBACK KeyboardProc(INT nCode, WPARAM wParam, LPARAM lParam)
{   
	DBG("HOOK: HookProc");
    if (nCode != HC_ACTION)
		return CallNextHookEx(gHook, nCode, wParam, lParam);

    COPYDATASTRUCT cds;
	HEVENT data;

    data.lParam = lParam;
    data.wParam = wParam;
    data.nCode = nCode;
    data.dwHookType = WH_KEYBOARD;

	cds.dwData = 0;
	cds.cbData = sizeof(data);
	cds.lpData = &data;

	// ask the controlling program if the hook should be passed
    BOOL bRes = SendMessage(gHwnd, WM_COPYDATA, 0, (LPARAM)(VOID*)&cds);  

    if(!bRes) 
        // pass hook to next handler
        return CallNextHookEx(gHook, nCode, wParam, lParam);
    else 
        // just return
        return(bRes);
}


//
// hook setup function
//
BOOL Start(HWND hWnd)
{
    // remember the windows and hook handle for further instances
    gHwnd = hWnd;
    gHook = SetWindowsHookEx(WH_KEYBOARD, KeyboardProc, gInst, 0);
    return (gHook != NULL);
}


//
// hook remove function
//
BOOL Stop()
{
    // if the hook is defined
    if(gHook)
    {
        // reset data
        gHwnd = NULL;
        BOOL bRes = UnhookWindowsHookEx(gHook);
        gHook = NULL;
        return (bRes);
    }
    return(true);
}

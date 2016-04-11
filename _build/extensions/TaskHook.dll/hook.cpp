// hook.cpp : Defines the entry point for the DLL application.
//

#include "stdafx.h"
#include "hook.h"

#pragma data_seg(".shared")
static HWND g_egMessageHwnd = 0;
static HHOOK cbtHookHandle = NULL;
static HHOOK shellHookHandle = NULL;
static HINSTANCE hinstDLL; 
#pragma data_seg()
#pragma comment(linker, "/SECTION:.shared,RWS")


LRESULT CALLBACK CbtHook(int nCode, WPARAM wParam, LPARAM lParam) 
{
	switch (nCode)
	{
		case HCBT_SETFOCUS:
			PostMessage(g_egMessageHwnd, WM_APP+1, wParam, lParam);
			break;
		//case HCBT_CREATEWND:
		//	PostMessage(g_egMessageHwnd, WM_APP+2, wParam, lParam);
		//	break;
		//case HCBT_DESTROYWND:
		//	PostMessage(g_egMessageHwnd, WM_APP+3, wParam, lParam);
		//	break;
	}
	return CallNextHookEx(cbtHookHandle, nCode, wParam, lParam);
}


LRESULT CALLBACK ShellHook(int nCode, WPARAM wParam, LPARAM lParam) 
{
	switch (nCode)
	{
		case HSHELL_WINDOWCREATED:
			PostMessage(g_egMessageHwnd, WM_APP+2, wParam, lParam);
			break;
		case HSHELL_WINDOWDESTROYED:
			PostMessage(g_egMessageHwnd, WM_APP+3, wParam, lParam);
			break;
	}
	return CallNextHookEx(shellHookHandle, nCode, wParam, lParam);
}


void StartHook()
{
	g_egMessageHwnd = FindWindow("HiddenMessageReceiver", "EventGhost Message Receiver");
	cbtHookHandle = SetWindowsHookEx(WH_CBT, CbtHook, hinstDLL, 0);
	shellHookHandle = SetWindowsHookEx(WH_SHELL, ShellHook, hinstDLL, 0);
}


void StopHook()
{
	UnhookWindowsHookEx(cbtHookHandle);
	cbtHookHandle = NULL;
	UnhookWindowsHookEx(shellHookHandle);
	shellHookHandle = NULL;
}


BOOL APIENTRY DllMain( HINSTANCE hinst,
                       DWORD  ul_reason_for_call, 
                       LPVOID lpReserved
					 )
{
	switch (ul_reason_for_call)
	{
		case DLL_PROCESS_ATTACH:
			hinstDLL = hinst;
			DisableThreadLibraryCalls(hinst);
			break;
		case DLL_PROCESS_DETACH:
			break;
	}
    return TRUE;
}


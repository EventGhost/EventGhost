#include "Python.h"
#define _WIN32_WINNT 0x501
#include "windows.h"
#include "utils.h"
#include "keyhook.h"
#include "mousehook.h"

volatile DWORD gLastTickCount;
volatile BOOL gIsInIdle = FALSE;
DWORD gWaitThreadId = 0;
static DWORD gHookThreadId = 0;
static HANDLE gHookThreadHandle;
static HANDLE gWaitThreadHandle;
static HANDLE waitEvent;
DWORD gIdleTimeout = 60000;

PyObject* gPyIdleCallback;
PyObject* gPyUnIdleCallback;


DWORD WINAPI 
HookThreadProc(HANDLE startupEvent)
{
    MSG msg;
    BOOL bRet; 
	HINSTANCE hMod;

	CoInitialize(NULL);
	khData.lock = CreateMutex(NULL, FALSE, NULL);
	if(0==SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL))
		ErrorExit("SetThreadPriority");
	hMod = LoadLibrary("cFunctions.pyd");
	SetKeyboardHook(hMod);
	SetMouseHook(hMod);
    PeekMessage(&msg, NULL, WM_USER, WM_USER, PM_NOREMOVE);
	SetEvent(startupEvent);
	DBG("HookThread: started");
	while( (bRet = GetMessage( &msg, NULL, 0, 0 )) != 0)
    { 
        if (bRet == -1)
        {
			DBG("HookThreadProc: GetMessage: error");
			// handle the error and possibly exit
        }
        else
        {
			if(msg.message == WM_USER + 1)
			{
				DBG("HookThread: WM_USER+1\n");
				//break;
			}
			TranslateMessage(&msg); 
            DispatchMessage(&msg); 
        }
    } 
	UnsetKeyboardHook();
	UnsetMouseHook();
	CloseHandle(khData.lock);
	CoUninitialize();
	DBG("HookThread: stopped");
	return(0);
}


DWORD WINAPI 
WaitThreadProc(HANDLE startupEvent)
{
	DWORD res;
	PyGILState_STATE gil;
	HANDLE pHandles[] = { waitEvent }; 
	MSG msg;
	BOOL isKeyDown = FALSE;
	DWORD timeout;

	CoInitialize(NULL);
	gLastTickCount = GetTickCount();

	if(0==SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL))
		ErrorExit("WaitThread SetThreadPriority");
				
	PeekMessage(&msg, NULL, WM_USER, WM_USER, PM_NOREMOVE);
	SetEvent(startupEvent);
	DBG("WaitThread: started");
	while(1)
	{
		while (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) 
		{
			//DispatchMessage(&msg);
            switch(msg.message)
			{
				case WM_USER+1: // awake thread
					DBG("WaitThread: WM_USER+1: awake)");
					if(gIsInIdle)
					{
						DBG("    calling gPyUnIdleCallback");
						gil = PyGILState_Ensure();
						PyObject_CallObject(gPyUnIdleCallback, NULL);
						PyGILState_Release(gil);
						gIsInIdle = FALSE;
					}
					continue;
				case WM_USER+2: // key down
					DBG("WaitThread: WM_USER+2: key down");
					isKeyDown = TRUE;
					continue;
				case WM_USER+3: // key up
					DBG("WaitThread: WM_USER+3: key up");
					isKeyDown = FALSE;
					continue;
				case WM_QUIT:
					DBG("WaitThread: WM_QUIT");
					goto out;
				default:
					DBG("WaitThread: got mesg");
					TranslateMessage(&msg);
					DispatchMessage(&msg); 
			}
		}
		if (isKeyDown)
		{
			timeout = 100;
		}else if (gIsInIdle)
		{
			timeout = INFINITE;
		}
		else
		{
			timeout = gIdleTimeout - (GetTickCount() - gLastTickCount);
		}
		DBG("timeout: %d", timeout);
		res = MsgWaitForMultipleObjects(
			1, 
			pHandles, 
			FALSE, 
			timeout,
			QS_ALLEVENTS);

		switch (res)
		{
			case WAIT_OBJECT_0: 
				DBG("WaitThread: WAIT_OBJECT_0");
				continue;
			case WAIT_OBJECT_0+1: 
				DBG("WaitThread: WAIT_OBJECT_0+1");
				continue;
			case WAIT_TIMEOUT: 
				DBG("WaitThread: WAIT_TIMEOUT");
				if (isKeyDown)
				{
					isKeyDown = CheckKeyState();
				}
				if(!gIsInIdle && ((GetTickCount() - gLastTickCount) >= gIdleTimeout))
				{
					DBG("    calling PyIdleCallback");
					gil = PyGILState_Ensure();
					PyObject_CallObject(gPyIdleCallback, NULL);
					PyGILState_Release(gil);
					gIsInIdle = TRUE;
				}
				continue;
			default:
				DBG("WaitThread: ***unknow result!***\n");
				continue;
		}
		//res = WaitForSingleObject(waitEvent, INFINITE);

	}
out:
	DBG("WaitThread: stopped");
	CoUninitialize();
	return(0);
}


void AwakeWaitThread(void)
{
	gLastTickCount = GetTickCount();
	if (gIsInIdle)
		PostThreadMessage(gWaitThreadId, WM_USER+1, 0, 0);
}


PyObject *
SetIdleTime(PyObject *self, PyObject *args)
{

	if (!PyArg_ParseTuple(args, "l", &gIdleTimeout))
        return NULL;
	PostThreadMessage(gWaitThreadId, WM_USER+1, 0, 0);
	Py_RETURN_NONE;
}


PyObject *
ResetIdleTimer(PyObject *self, PyObject *args)
{
	PostThreadMessage(gWaitThreadId, WM_USER+1, 0, 0);
	Py_RETURN_NONE;
}


PyObject *
StartHooks(PyObject *self, PyObject *args)
// def StartHooks(idleCallback, unidleCallback) => None
{
	HANDLE startupEvent;

	if (!PyArg_ParseTuple(args, "OO", &gPyIdleCallback, &gPyUnIdleCallback))
	{
		PyErr_Print();
		return NULL;
	}
	Py_INCREF(gPyIdleCallback);
	Py_INCREF(gPyUnIdleCallback);
	PyEval_InitThreads();

	DBG("RegisterKeyhook");
	waitEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
	startupEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
	gWaitThreadHandle = CreateThread(
		NULL,			// default security
		0,				// default stack size
		WaitThreadProc, // name of the thread function
		startupEvent,   // the thread parameters
		0,				// default startup flags
		&gWaitThreadId);
	switch(WaitForSingleObject(startupEvent, 3000))
	{
		case WAIT_TIMEOUT:
			RAISE_SYSTEMERR("WAIT_TIMEOUT for WaitThread");
		case WAIT_OBJECT_0:
			break;
	}
	ResetEvent(startupEvent);
	if(PostThreadMessage(gWaitThreadId, WM_USER+1, 0, 0) == 0)
		RAISE_SYSTEMERR("PostThreadMessage WaitThread");

	gHookThreadHandle = CreateThread(
		NULL,			// default security
		0,				// default stack size
		HookThreadProc, // name of the thread function
		startupEvent,	// the thread parameters
		0,				// default startup flags
		&gHookThreadId);
	switch(WaitForSingleObject(startupEvent, 3000))
	{
		case WAIT_TIMEOUT:
			RAISE_SYSTEMERR("WAIT_TIMEOUT for HookThread");
		case WAIT_OBJECT_0:
			break;
	}
	CloseHandle(startupEvent);

	Py_RETURN_NONE;
}


PyObject *
StopHooks(PyObject *self, PyObject *args)
// def StopHooks() => None
{
	DBG("StopHooks");

	if (gHookThreadId != 0)
	{
		if(PostThreadMessage(gHookThreadId, WM_QUIT, 0, 0) == 0)
			RAISE_SYSTEMERR("PostThreadMessage HookThread");
		if(WaitForSingleObject(gHookThreadHandle, 3000) != WAIT_OBJECT_0)
			RAISE_SYSTEMERR("WaitForSingleObject HookThread");
		gHookThreadId = 0;
	}

	if (gWaitThreadId != 0)
	{
		if(PostThreadMessage(gWaitThreadId, WM_QUIT, 0, 0) == 0)
			RAISE_SYSTEMERR("PostThreadMessage WaitThread");
		if(WaitForSingleObject(gWaitThreadHandle, 3000) != WAIT_OBJECT_0)
			RAISE_SYSTEMERR("WaitForSingleObject WaitThread");
		gWaitThreadId = 0;
	}
	Py_RETURN_NONE;
}

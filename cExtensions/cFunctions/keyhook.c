#include "Python.h"
#define _WIN32_WINNT 0x501
#include "windows.h"
#include "utils.h"


PyObject* g_KeyboardCallback;
PyObject* g_MouseCallback = NULL;
PyObject* idle_func;
PyObject* unidle_func;
HANDLE waitThread;
static HANDLE waitEvent;
static HANDLE startupEvent;
static HINSTANCE hMod;

static DWORD  g_HookThreadId = 0;
static DWORD g_WaitThreadId = 0;
HHOOK oldKeyHook = NULL;
HHOOK oldMouseHook = NULL;
BYTE key_state[256];
DWORD g_idleTime = 60000;
BYTE currentKeys[16];
int numCurrentKeys = 0;
BOOL gIsAltGrDown = FALSE;
volatile BOOL isInIdle = FALSE;
volatile DWORD lastTickCount;

#define ALTGR_CODE 10


const char* orderedStringCodes[256] = {"AltGr", "Shift", "LShift", "RShift", 
    "Ctrl", "LCtrl", "RCtrl", "Alt", "LAlt", "RAlt", "LWin", "RWin", "Apps", 
    "LButton", "RButton", "MButton", "XButton1", "XButton2", "CapsLock", 
    "NumLock", "ScrollLock", "Cancel", "Backspace", "Tabulator", "Clear", 
    "Pause", "Kana", "Junja", "Final", "Hanja", "Escape", "Convert", 
    "NonConvert", "Accept", "ModeChange", "Space", "PageUp", "PageDown", 
    "End", "Home", "Left", "Up", "Right", "Down", "Select", "Print", 
    "Execute", "PrintScreen", "Insert", "Delete", "Help", "A", "B", "C", "D", 
    "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", 
    "T", "U", "V", "W", "X", "Y", "Z", "Sleep", "0", "1", "2", "3", "4", "5", 
    "6", "7", "8", "9", "Numpad0", "Numpad1", "Numpad2", "Numpad3", "Numpad4", 
    "Numpad5", "Numpad6", "Numpad7", "Numpad8", "Numpad9", "Multiply", "Add", 
    "Separator", "Subtract", "Decimal", "Divide", "F1", "F2", "F3", "F4", 
    "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14", "F15", 
    "F16", "F17", "F18", "F19", "F20", "F21", "F22", "F23", "F24", 
    "BrowserBack", "BrowserForward", "BrowserRefresh", "BrowserStop", 
    "BrowserSearch", "BrowserFavorites", "BrowserHome", "VolumeMute", 
    "VolumeDown", "VolumeUp", "MediaNextTrack", "MediaPrevTrack", "MediaStop", 
    "MediaPlayPause", "LaunchMail", "LaunchMediaSelect", "LaunchApp1", 
    "LaunchApp2", "OemPlus", "OemComma", "OemMinus", "OemPeriod", "Oem1", 
    "Oem2", "Oem3", "Oem4", "Oem5", "Oem6", "Oem7", "Oem8", "Oem92", "Oem93", 
    "Oem94", "Oem95", "Oem96", "OemE1", "Oem102", "OemE3", "OemE4", 
    "ProcessKey", "OemE6", "Packet", "OemE9", "OemEA", "OemEB", "OemEC", 
    "OemED", "OemEE", "OemEF", "OemF0", "OemF1", "OemF2", "OemF3", "OemF4", 
    "OemF5", "Attn", "CrSel", "ExSel", "EraseEof", "Play", "Zoom", "Noname", 
    "PA1", "OemClear", "U00", "U07", "U0B", "U0E", "U0F", "U16", "U1A", "U3A", 
    "U3B", "U3C", "U3D", "U3E", "U3F", "U40", "U5E", "U88", "U89", "U8A", 
    "U8B", "U8C", "U8D", "U8E", "U8F", "U97", "U98", "U99", "U9A", "U9B", 
    "U9C", "U9D", "U9E", "U9F", "UB8", "UB9", "UC1", "UC2", "UC3", "UC4", 
    "UC5", "UC6", "UC7", "UC8", "UC9", "UCA", "UCB", "UCC", "UCD", "UCE", 
    "UCF", "UD0", "UD1", "UD2", "UD3", "UD4", "UD5", "UD6", "UD7", "UD8", 
    "UD9", "UDA", "UE0", "UE8", "UFF", "Return", };

BYTE vk2ordering[256] = {192, 13, 14, 21, 15, 16, 17, 193, 22, 23, 0, 194, 24, 
    255, 195, 196, 1, 4, 7, 25, 18, 26, 197, 27, 28, 29, 198, 30, 31, 32, 33, 
    34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 78, 
    79, 80, 81, 82, 83, 84, 85, 86, 87, 199, 200, 201, 202, 203, 204, 205, 51, 
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 
    70, 71, 72, 73, 74, 75, 76, 10, 11, 12, 206, 77, 88, 89, 90, 91, 92, 93, 
    94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 
    110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 
    125, 126, 127, 207, 208, 209, 210, 211, 212, 213, 214, 19, 20, 158, 159, 
    160, 161, 162, 215, 216, 217, 218, 219, 220, 221, 222, 223, 2, 3, 5, 6, 8, 
    9, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 
    142, 143, 144, 145, 224, 225, 150, 146, 147, 148, 149, 151, 152, 226, 227, 
    228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 
    243, 244, 245, 246, 247, 248, 249, 250, 251, 153, 154, 155, 156, 157, 252, 
    163, 164, 165, 166, 167, 168, 169, 253, 170, 171, 172, 173, 174, 175, 176, 
    177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 
    254, };


#define MAX_RES_STRING_CHARS 256


const char g_szClassName[] = "HIDReceiver";

int ProcessInputCommand(HRAWINPUT hRawInput)
{
	UINT dwSize;
	RAWINPUT *ri;
	UINT pos;

	GetRawInputData(hRawInput, RID_INPUT, NULL, &dwSize, sizeof(RAWINPUTHEADER));
	ri = malloc(dwSize);
	GetRawInputData(hRawInput, RID_INPUT, ri, &dwSize, sizeof(RAWINPUTHEADER));
	if (ri->header.dwType == RIM_TYPEKEYBOARD)
	{
		pos = vk2ordering[ri->data.keyboard.VKey];

		print("got keyboard %s, %d", orderedStringCodes[pos], ri->data.keyboard.Message);
	}
	free(ri);
	return 1;
}
	

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    switch(msg)
    {
		case WM_INPUT:
			ProcessInputCommand((HRAWINPUT) lParam);
			break;
		case WM_CLOSE:
            DestroyWindow(hwnd);
			return (0);
        case WM_DESTROY:
            PostQuitMessage(0);
			return (0);
    }
    return DefWindowProc(hwnd, msg, wParam, lParam);
}


int CreateMessageWindow(HINSTANCE hInstance)
{
    WNDCLASSEX wc;
    HWND hwnd;
	RAWINPUTDEVICE rid;

    //Step 1: Registering the Window Class
    wc.cbSize        = sizeof(WNDCLASSEX);
    wc.style         = 0;
    wc.lpfnWndProc   = WndProc;
    wc.cbClsExtra    = 0;
    wc.cbWndExtra    = 0;
    wc.hInstance     = hInstance;
    wc.hIcon         = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wc.lpszMenuName  = NULL;
    wc.lpszClassName = g_szClassName;
    wc.hIconSm       = LoadIcon(NULL, IDI_APPLICATION);

    if(!RegisterClassEx(&wc))
    {
        MessageBox(NULL, "Window Registration Failed!", "Error!",
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    // Step 2: Creating the Window
    hwnd = CreateWindowEx(
        WS_EX_CLIENTEDGE,
        g_szClassName,
        "The title of my window",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 240, 120,
        NULL, NULL, hInstance, NULL);

    if(hwnd == NULL)
    {
        MessageBox(NULL, "Window Creation Failed!", "Error!",
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    //ShowWindow(hwnd, SW_SHOW);
    //UpdateWindow(hwnd);

    rid.usUsagePage = 0x01;      // adds HID keyboard with no legacy message
    rid.usUsage = 0x06;
    rid.dwFlags = RIDEV_INPUTSINK;
	rid.hwndTarget = hwnd;
	if(RegisterRawInputDevices(&rid, 1, sizeof(RAWINPUTDEVICE)) == FALSE)
	{
        MessageBox(NULL, "RegisterRawInputDevices Failed!", "Error!",
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
	}
	return TRUE;
}


LRESULT CALLBACK KeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) 
{
	PKBDLLHOOKSTRUCT kbd;
	static DWORD last_vkCode = -1;
	static DWORD last_scanCode = -1;
	static DWORD last_flags = -1;
	//void *kbd2;
	DWORD flags;
	BOOL isAltDown;
	BOOL isUpKey;
	DWORD vkCode;
	int i, j, pos;
	BYTE orderedCode;
	//BYTE *currentKeys2;
	PyObject *arglist, *pyRes;
	PyGILState_STATE gil;
	static BOOL blocked = FALSE;
	static BYTE blockedWinKey = 0;
	static BOOL ignoreNextWinKey = FALSE;
	char resString[MAX_RES_STRING_CHARS];
	char *destPtr;
	const char *srcPtr;

	
	if(nCode != HC_ACTION)
	{
		goto out;
	}

	lastTickCount = GetTickCount();
	if (isInIdle)
		PostThreadMessage(g_WaitThreadId, WM_USER+1, 0, 0);

	if(g_KeyboardCallback == NULL)
		goto out;
	
	//DEBUG("KeyboardProc");
	kbd = (PKBDLLHOOKSTRUCT)lParam;
	flags = kbd->flags;
	isAltDown = flags & LLKHF_ALTDOWN;
	isUpKey = flags & LLKHF_UP;
	vkCode = kbd->vkCode;

	//print("%i %i", vkCode, isUpKey);
	if (ignoreNextWinKey)
	{
		//print("pre-ignored");
		ignoreNextWinKey = FALSE;
		goto out;
	}

	// if this message is a just repeating, only awake WaitThread
	if ((last_vkCode == kbd->vkCode) 
		&& (last_flags == kbd->flags) 
		&& (last_scanCode == kbd->scanCode))
	{
		if (blocked)
			return 42;
		if (blockedWinKey)
			return 42;
		goto out;
	}

	blocked = FALSE;
	last_vkCode = kbd->vkCode;
	last_flags = kbd->flags;
	last_scanCode = kbd->scanCode;



	// get the "ordered" code
	orderedCode = vk2ordering[vkCode];
	if (isUpKey)
	{
		// remove the key
		for (i=0; i < numCurrentKeys; i++)
		{
			if (currentKeys[i] == orderedCode)
			{
				numCurrentKeys--;
				for (j=i; j < numCurrentKeys; j++)
				{
					currentKeys[j] = currentKeys[j+1];
				}
				break;
			}
		}
		currentKeys[numCurrentKeys] = 0;
	} else
	{
		// insert the key
		pos = numCurrentKeys;
		for (i=0; i < numCurrentKeys; i++)
		{
			if (currentKeys[i] == orderedCode)
			{
				// They key is already in. This should never happen, but it happens
				goto out;
			} 
			else if (currentKeys[i] > orderedCode)
			{
				pos = i;
				break;
			}
		}
		for (j=numCurrentKeys; j > pos; j--)
		{
			currentKeys[j] = currentKeys[j-1];
		}
		currentKeys[pos] = orderedCode;
		numCurrentKeys++;
		currentKeys[numCurrentKeys] = 0;
	}

	destPtr = resString;
	j = 0;
	for (i=0; i < numCurrentKeys; i++)
	{
		srcPtr = orderedStringCodes[currentKeys[i]];
		while (*srcPtr)
		{
			*destPtr = *srcPtr;
			destPtr++;
			srcPtr++;
			j++;
			if (j >= MAX_RES_STRING_CHARS)
				goto out;
		}
		if (i < numCurrentKeys - 1)
		{
			*destPtr = '+';
			destPtr++;
			j++;
			if (j >= MAX_RES_STRING_CHARS)
				goto out;
		}
	}
	*destPtr = 0x00;

	gil = PyGILState_Ensure();
	arglist = Py_BuildValue("(s)", resString);

	pyRes = PyObject_CallObject(g_KeyboardCallback, arglist);
	if(pyRes == NULL)
	{
		PyErr_Print();
	}else{
		if (Py_True == pyRes)
		{
			Py_XDECREF(pyRes);
			Py_DECREF(arglist);
			PyGILState_Release(gil);
			blocked = TRUE;
			blockedWinKey = 0;
			return 42;
		}
		Py_XDECREF(pyRes);
	}

	Py_DECREF(arglist);
	PyGILState_Release(gil);

	if (blockedWinKey)
	{
		ignoreNextWinKey = TRUE;
		keybd_event(blockedWinKey, 0, 0, NULL);
	}
	blockedWinKey = 0;
	if ((vkCode == 91) || (vkCode == 92))
	{
		if (!isUpKey)
		{
			blockedWinKey = vkCode;
			return 42;
		}
	}

out:
	return CallNextHookEx(oldKeyHook, nCode, wParam, lParam);
}


LRESULT CALLBACK MouseHookProc(int nCode, WPARAM wParam, LPARAM lParam) 
{
	PyObject *arglist, *pyRes;
	PyGILState_STATE gil;
	PMSLLHOOKSTRUCT mhs;
	char *resString;
	static BOOL mouseState[3] = {FALSE, FALSE, FALSE};
	
	lastTickCount = GetTickCount();
	if (isInIdle)
		PostThreadMessage(g_WaitThreadId, WM_USER+1, 0, 0);
	if (nCode == HC_ACTION)
	{	
		mhs = (PMSLLHOOKSTRUCT) lParam;
		resString = NULL;
		switch(wParam)
		{
			//case WM_LBUTTONDOWN:
			//	DEBUG("WM_LBUTTONDOWN");
			//	break;
			//case WM_LBUTTONUP:
			//	DEBUG("WM_LBUTTONUP");
			//	break;
			//case WM_MOUSEMOVE:
			//	DEBUG("WM_MOUSEMOVE");
			//	break;
			//case WM_MOUSEWHEEL:
			//	DEBUG("WM_MOUSEWHEEL");
			//	break;
			//case WM_RBUTTONDOWN:
			//	DEBUG("WM_RBUTTONDOWN");
			//	break;
			//case WM_RBUTTONUP:
			//	DEBUG("WM_RBUTTONUP");
			//	break;
			case WM_MBUTTONDOWN:
				//DEBUG("WM_MBUTTONDOWN");
				mouseState[1] = TRUE;
				resString = "MiddleButtonDown";
				break;
			case WM_MBUTTONUP:
				//DEBUG("WM_MBUTTONUP");
				mouseState[1] = FALSE;
				resString = "MiddleButtonUp";
				break;
			//case WM_XBUTTONDOWN:
			//	DEBUG("WM_XBUTTONDOWN");
			//	break;
			//case WM_XBUTTONUP:
			//	DEBUG("WM_XBUTTONUP");
			//	break;
			//case WM_XBUTTONDBLCLK:
			//	DEBUG("WM_XBUTTONDBLCLK");
			//	break;
			//default:
			//	DEBUG("unknown mouse message");
		}
		if (resString && g_MouseCallback)
		{
			gil = PyGILState_Ensure();
			arglist = Py_BuildValue("(s)", resString);

			pyRes = PyObject_CallObject(g_MouseCallback, arglist);
			if(pyRes == NULL)
			{
				PyErr_Print();
			}else{
				if (Py_True == pyRes)
				{
					Py_XDECREF(pyRes);
					Py_DECREF(arglist);
					PyGILState_Release(gil);
					//blocked = TRUE;
					return 42;
				}
				Py_XDECREF(pyRes);
			}

			Py_DECREF(arglist);
			PyGILState_Release(gil);
		}
		//print("%i: x:%i, y:%i", mhs->time, mhs->pt.x, mhs->pt.y);
	}
	return CallNextHookEx(oldMouseHook, nCode, wParam, lParam);
}



DWORD WINAPI 
HookThread(LPVOID lpParameter)
{
    MSG msg;
    BOOL bRet; 

	CoInitialize(NULL);
	if(0==SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL))
		ErrorExit("SetThreadPriority");;
	hMod = LoadLibrary("cFunctions.pyd");
	oldKeyHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardProc, (HINSTANCE) hMod, 0);//
	oldMouseHook = SetWindowsHookEx(WH_MOUSE_LL, MouseHookProc, (HINSTANCE) hMod, 0);//
	if(oldKeyHook == NULL)
	{
		ErrorExit("SetWindowsHookEx");
	}
	//CreateMessageWindow((HINSTANCE) hMod);
    PeekMessage(&msg, NULL, WM_USER, WM_USER, PM_NOREMOVE);
	SetEvent(startupEvent);
	DEBUG("HookThread started");
	while( (bRet = GetMessage( &msg, NULL, 0, 0 )) != 0)
    { 
        if (bRet == -1)
        {
            print("error\n");
			// handle the error and possibly exit
        }
        else
        {
            //print("msg");
			if(msg.message == WM_USER + 1)
			{
				print("HookThread WM_USER\n");
				//break;
			}
			TranslateMessage(&msg); 
            DispatchMessage(&msg); 
			//print("DispatchMessage\n");
        }
    } 
	UnhookWindowsHookEx(oldKeyHook);
	UnhookWindowsHookEx(oldMouseHook);
	CoUninitialize();
    SetEvent(startupEvent);
	DEBUG("HookThread stopped");
	return(0);
}


DWORD WINAPI 
WaitThread(LPVOID lpParameter)
{
	DWORD res;
	PyGILState_STATE gil;
	HANDLE pHandles[] = { waitEvent }; 
	MSG msg;

	CoInitialize(NULL);
	lastTickCount = GetTickCount();

	if(0==SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL))
		ErrorExit("WaitThread SetThreadPriority");
				
	PeekMessage(&msg, NULL, WM_USER, WM_USER, PM_NOREMOVE);
	SetEvent(startupEvent);
	DEBUG("WaitThread started");
	while(1)
	{
		while (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) 
		{
			//DispatchMessage(&msg);
            if(msg.message == WM_USER+1)
			{
				DEBUG("WM_USER+1");
				if(isInIdle)
				{
					gil = PyGILState_Ensure();
					PyObject_CallObject(unidle_func, NULL);
					PyGILState_Release(gil);
					isInIdle = FALSE;
				}
				continue;
			}
			else if(msg.message == WM_QUIT)
				goto out;
			else
			{
				print("got WaitThread mesg");
				TranslateMessage(&msg);
				DispatchMessage(&msg); 
			}
		}
		
		res = MsgWaitForMultipleObjects(
			1, 
			pHandles, 
			FALSE, 
			g_idleTime - (GetTickCount() - lastTickCount),
			QS_ALLEVENTS);

		switch (res)
		{
			case WAIT_OBJECT_0: 
				//print("WAIT_OBJECT_0");
				continue;
			case WAIT_OBJECT_0+1: 
				//print("WAIT_OBJECT_0+1");
				continue;
			case WAIT_TIMEOUT: 
				if(!isInIdle && ((GetTickCount() - lastTickCount) >= g_idleTime))
				{
					gil = PyGILState_Ensure();
					PyObject_CallObject(idle_func, NULL);
					PyGILState_Release(gil);
					isInIdle = TRUE;
				}
				continue;
			default:
				print("unknow result\n");
				continue;
		}
		//res = WaitForSingleObject(waitEvent, INFINITE);

	}
out:
    SetEvent(startupEvent);
	DEBUG("WaitThread stopped");
	CoUninitialize();
	return(0);
}

PyObject *
SetKeyboardCallback(PyObject *self, PyObject *args)
{
	PyObject* newCallback;
	PyObject* oldCallback;

	if (!PyArg_ParseTuple(args, "O", &newCallback))
	{
		PyErr_Print();
		return NULL;
	}
	oldCallback = g_KeyboardCallback;
	if (oldCallback == NULL)
		oldCallback = Py_None;
	Py_XDECREF(g_KeyboardCallback);
	Py_XINCREF(newCallback);
	if (newCallback == Py_None)
	{
		g_KeyboardCallback = NULL;
	}else
	{
		g_KeyboardCallback = newCallback;
	}
	Py_RETURN_NONE;
	//return Py_BuildValue("(O)", oldCallback);
}


PyObject *
SetMouseCallback(PyObject *self, PyObject *args)
{
	PyObject* callback;

	if (!PyArg_ParseTuple(args, "O", &callback))
	{
		PyErr_Print();
		return NULL;
	}
	Py_XDECREF(g_MouseCallback);
	if (callback == Py_None)
	{
		callback = NULL;
	}
	Py_XINCREF(callback);
	g_MouseCallback = callback;
	Py_RETURN_NONE;
}



PyObject *
RegisterKeyhook(PyObject *self, PyObject *args)
{
	HANDLE handle;

	if (!PyArg_ParseTuple(args, "OO", &idle_func, &unidle_func))
	{
		PyErr_Print();
		return NULL;
	}
	Py_INCREF(idle_func);
	Py_INCREF(unidle_func);
	PyEval_InitThreads();

	memset(key_state, 0, 256);
	key_state[VK_NUMLOCK] = (GetKeyState(VK_NUMLOCK)&0x0001) ? 0x01 : 0x00;
	key_state[VK_CAPITAL] = (GetKeyState(VK_CAPITAL)&0x0001) ? 0x01 : 0x00;
	key_state[VK_SCROLL] = (GetKeyState(VK_SCROLL)&0x0001) ? 0x01 : 0x00;

	DEBUG("RegisterKeyhook");
	waitEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
	startupEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
	handle = CreateThread(NULL, 0, WaitThread, NULL, 0, &g_WaitThreadId);
	switch(WaitForSingleObject(startupEvent, 3000))
	{
		case WAIT_TIMEOUT:
			PyErr_SetString(
				PyExc_SystemError, 
				"WAIT_TIMEOUT for WaitThread");
			return NULL;
		case WAIT_OBJECT_0:
			break;
	}
	ResetEvent(startupEvent);
	if(PostThreadMessage(g_WaitThreadId, WM_USER+1, 0, 0) == 0)
		RAISE_SYSTEMERR("PostThreadMessage WaitThread");

	handle = CreateThread(NULL, 0, HookThread, NULL, 0, &g_HookThreadId);
	switch(WaitForSingleObject(startupEvent, 3000))
	{
		case WAIT_TIMEOUT:
			PyErr_SetString(
				PyExc_SystemError, 
				"WAIT_TIMEOUT for HookThread");
			return NULL;
		case WAIT_OBJECT_0:
			break;
	}
	ResetEvent(startupEvent);

	Py_RETURN_NONE;
}


PyObject *
SetIdleTime(PyObject *self, PyObject *args)
{

	if (!PyArg_ParseTuple(args, "l", &g_idleTime))
        return NULL;
	if(PostThreadMessage(g_WaitThreadId, WM_USER+1, 0, 0) == 0)
		RAISE_SYSTEMERR("PostThreadMessage WaitThread");
	Py_RETURN_NONE;
}


PyObject *
ResetIdleTimer(PyObject *self, PyObject *args)
{
	if(PostThreadMessage(g_WaitThreadId, WM_USER+1, 0, 0) == 0)
		RAISE_SYSTEMERR("PostThreadMessage WaitThread");
	Py_RETURN_NONE;
}


PyObject *
UnregisterKeyhook(PyObject *self, PyObject *args)
{
	//DEBUG("UnregisterKeyhook");

	if (g_HookThreadId != 0)
	{
		if(PostThreadMessage(g_HookThreadId, WM_QUIT, 0, 0) == 0)
			RAISE_SYSTEMERR("PostThreadMessage HookThread");
		if(WaitForSingleObject(startupEvent, 3000) != WAIT_OBJECT_0)
			RAISE_SYSTEMERR("WaitForSingleObject HookThread");
		ResetEvent(startupEvent);
		g_HookThreadId = 0;
	}

	if (g_WaitThreadId != 0)
	{
		if(PostThreadMessage(g_WaitThreadId, WM_QUIT, 0, 0) == 0)
			RAISE_SYSTEMERR("PostThreadMessage WaitThread");
		if(WaitForSingleObject(startupEvent, 3000) != WAIT_OBJECT_0)
			RAISE_SYSTEMERR("WaitForSingleObject WaitThread");
		ResetEvent(startupEvent);
		g_WaitThreadId = 0;
	}
	CloseHandle(startupEvent);
	Py_RETURN_NONE;
}


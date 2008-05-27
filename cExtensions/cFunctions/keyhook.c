#include "Python.h"
#define _WIN32_WINNT 0x501
#include "windows.h"
#include "utils.h"
#include "hooks.h"


#define ALTGR_CODE 10

const char* ORDERED_KEY_NAMES[256] = {"AltGr", "Shift", "LShift", "RShift", 
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

const BYTE ORDERED_VK_CODES[256] = {192, 13, 14, 21, 15, 16, 17, 193, 22, 23, 0, 194, 24, 
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


PyObject* gPyKeyboardCallback;
HHOOK gOldKeyHook = NULL;
int   gNumCurrentKeys;
BYTE  gCurrentKeys[16];
BYTE  gKeyStateData[256];
DWORD gLastVkCode;
DWORD gLastScanCode;
DWORD gLastFlags;
BOOL  gBlocked;
BYTE  gBlockedWinKey;
BOOL  gIgnoreNextWinKey;


void 
ResetKeyboardHook(void)
{
	gNumCurrentKeys = 0;
	memset(gCurrentKeys, 0, 16);
	memset(gKeyStateData, 0, 256);
	gKeyStateData[VK_NUMLOCK] = (GetKeyState(VK_NUMLOCK)&0x0001) ? 0x01 : 0x00;
	gKeyStateData[VK_CAPITAL] = (GetKeyState(VK_CAPITAL)&0x0001) ? 0x01 : 0x00;
	gKeyStateData[VK_SCROLL] = (GetKeyState(VK_SCROLL)&0x0001) ? 0x01 : 0x00;
	gLastVkCode = -1;
	gLastScanCode = -1;
	gLastFlags = -1;
	gBlocked = FALSE;
	gBlockedWinKey = 0;
	gIgnoreNextWinKey = FALSE;
}


BOOL 
InsertKey(BYTE key)
{
	int i, pos;

	pos = gNumCurrentKeys;
	for (i=0; i < gNumCurrentKeys; i++)
	{
		if (gCurrentKeys[i] == key)
		{
			// They key is already in. This should never happen, but it happens
			return FALSE;
		} 
		else if (gCurrentKeys[i] > key)
		{
			pos = i;
			break;
		}
	}
	for (i=gNumCurrentKeys; i > pos; i--)
	{
		gCurrentKeys[i] = gCurrentKeys[i-1];
	}
	gCurrentKeys[pos] = key;
	gNumCurrentKeys++;
	gCurrentKeys[gNumCurrentKeys] = 0;
	return TRUE;
}


void 
RemoveKey(BYTE key)
{
	int i, j;

	for (i=0; i < gNumCurrentKeys; i++)
	{
		if (gCurrentKeys[i] == key)
		{
			gNumCurrentKeys--;
			for (j=i; j < gNumCurrentKeys; j++)
			{
				gCurrentKeys[j] = gCurrentKeys[j+1];
			}
			break;
		}
	}
	gCurrentKeys[gNumCurrentKeys] = 0;
}


BOOL
BuildKeyString(char *buffer)
{
	int i, j;
	char *destPtr;
	const char *srcPtr;

	destPtr = buffer;
	j = 0;
	for (i=0; i < gNumCurrentKeys; i++)
	{
		srcPtr = ORDERED_KEY_NAMES[gCurrentKeys[i]];
		while (*srcPtr)
		{
			*destPtr = *srcPtr;
			destPtr++;
			srcPtr++;
			j++;
			if (j >= MAX_RES_STRING_CHARS)
			{
				return FALSE;
			}
		}
		if (i < gNumCurrentKeys - 1)
		{
			*destPtr = '+';
			destPtr++;
			j++;
			if (j >= MAX_RES_STRING_CHARS)
			{
				return FALSE;
			}
		}
	}
	*destPtr = 0x00;
	return TRUE;
}


BOOL
CallPyCallback(char *keyString)
{
	PyObject *arglist, *pyRes;
	PyGILState_STATE gil;
	BOOL res = FALSE;

	gil = PyGILState_Ensure();
	arglist = Py_BuildValue("(s)", keyString);
	pyRes = PyObject_CallObject(gPyKeyboardCallback, arglist);
	if(pyRes == NULL)
	{
		PyErr_Print();
	}else{
		res = (pyRes == Py_True);
		Py_XDECREF(pyRes);
	}
	Py_DECREF(arglist);
	PyGILState_Release(gil);
	return res;
}


LRESULT CALLBACK 
KeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) 
{
	PKBDLLHOOKSTRUCT kbd;
	BOOL isAltDown;
	BOOL isUpKey;
	BYTE vkCode;
	//PyObject *arglist, *pyRes;
	//PyGILState_STATE gil;
	char keyString[MAX_RES_STRING_CHARS];

	
	if(nCode != HC_ACTION)
	{
		goto callNextHook;
	}

	AwakeWaitThread();

	if(gPyKeyboardCallback == NULL)
	{
		goto callNextHook;
	}
	
	//DEBUG("KeyboardProc");
	kbd = (PKBDLLHOOKSTRUCT)lParam;
	isAltDown = kbd->flags & LLKHF_ALTDOWN;
	isUpKey = kbd->flags & LLKHF_UP;
	vkCode = (BYTE) kbd->vkCode;

	//print("%i %i", vkCode, isUpKey);
	if (gIgnoreNextWinKey)
	{
		//print("pre-ignored");
		gIgnoreNextWinKey = FALSE;
		goto callNextHook;
	}

	// if this message is a just repeating, only awake WaitThread
	if ((gLastVkCode == kbd->vkCode) 
		&& (gLastFlags == kbd->flags) 
		&& (gLastScanCode == kbd->scanCode))
	{
		if (gBlocked || gBlockedWinKey)
		{
			goto blockThisKey;
		} else {
			goto callNextHook;
		}
	}

	gBlocked = FALSE;
	gLastVkCode = kbd->vkCode;
	gLastFlags = kbd->flags;
	gLastScanCode = kbd->scanCode;

	// insert or remove the "ordered" code
	if (isUpKey)
	{
		RemoveKey(ORDERED_VK_CODES[vkCode]);
	} else
	{
		if (!InsertKey(ORDERED_VK_CODES[vkCode]))
		{
			goto callNextHook;
		}
	}

	if (!BuildKeyString(keyString))
	{
		goto callNextHook;
	}

	if (CallPyCallback(keyString))
	{
		gBlocked = TRUE;
		gBlockedWinKey = 0;
		goto blockThisKey;
	}
	if (gBlockedWinKey)
	{
		gIgnoreNextWinKey = TRUE;
		keybd_event(gBlockedWinKey, 0, 0, 0);
	}
	gBlockedWinKey = 0;

	if ((vkCode == 91) || (vkCode == 92))
	{
		if (!isUpKey)
		{
			gBlockedWinKey = vkCode;
			goto blockThisKey;
		}
	}

callNextHook:
	return CallNextHookEx(gOldKeyHook, nCode, wParam, lParam);
blockThisKey:
	return 42;
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
	oldCallback = gPyKeyboardCallback;
	if (oldCallback == NULL)
		oldCallback = Py_None;
	Py_XDECREF(gPyKeyboardCallback);
	Py_XINCREF(newCallback);
	if (newCallback == Py_None)
	{
		gPyKeyboardCallback = NULL;
	}else
	{
		gPyKeyboardCallback = newCallback;
	}
	Py_RETURN_NONE;
	//return Py_BuildValue("(O)", oldCallback);
}



void
SetKeyboardHook(HINSTANCE hMod)
{
	ResetKeyboardHook();
	gOldKeyHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardProc, (HINSTANCE) hMod, 0);
	if(gOldKeyHook == NULL)
	{
		ErrorExit("SetWindowsHookEx");
	}
}


void 
UnsetKeyboardHook(void)
{
	UnhookWindowsHookEx(gOldKeyHook);
}
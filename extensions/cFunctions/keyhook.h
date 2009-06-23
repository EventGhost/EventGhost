#include "Python.h"
#define _WIN32_WINNT 0x501
#include "windows.h"

extern PyObject *
SetKeyboardCallback(PyObject *self, PyObject *args);

extern void 
SetKeyboardHook(HINSTANCE hMod);

extern void 
UnsetKeyboardHook(void);

extern BOOL CheckKeyState(void);

typedef struct{
	BYTE numPressedKeys;
	DWORD lastVkCode;
	DWORD lastScanCode;
	DWORD lastFlags;
	BOOL lastWasBlocked;
	BOOL ignoreNextWinKey;
	BYTE blockedWinKey;
	BYTE pressedKeys[16];
	HANDLE lock;
}KEYHOOK_DATA;

extern KEYHOOK_DATA khData;

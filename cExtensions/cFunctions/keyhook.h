#include "Python.h"
#define _WIN32_WINNT 0x501
#include "windows.h"

extern PyObject *
SetKeyboardCallback(PyObject *self, PyObject *args);

extern void 
SetKeyboardHook(HINSTANCE hMod);

extern void 
UnsetKeyboardHook(void);


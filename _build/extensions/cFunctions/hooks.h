#include "Python.h"
#define _WIN32_WINNT 0x501
#include "windows.h"


extern void AwakeWaitThread(void);

extern PyObject *
ResetIdleTimer(PyObject *self, PyObject *args);

extern PyObject *
SetIdleTime(PyObject *self, PyObject *args);

extern PyObject *
StartHooks(PyObject *self, PyObject *args);

extern PyObject *
StopHooks(PyObject *self, PyObject *args);

extern DWORD gWaitThreadId;

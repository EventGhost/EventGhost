#include "Python.h"


#include "registry_funcs.h"
#include "hooks.h"
#include "keyhook.h"
#include "mousehook.h"
#include "win_funcs.h"


static PyMethodDef example_methods[] = {
	{"RegEnumKeysAndValues", RegEnumKeysAndValues, 1, ""},
	{"StartHooks", StartHooks, 1, ""},
	{"StopHooks", StopHooks, 1, ""},
	{"ResetIdleTimer", ResetIdleTimer, 1, ""},
	{"SetIdleTime", SetIdleTime, 1, ""},
	{"SetKeyboardCallback", SetKeyboardCallback, 1, ""},
	{"SetMouseCallback", SetMouseCallback, 1, ""},
	{"GetTopLevelWindowList", GetTopLevelWindowList, 1, ""},
	{"GetWindowChildsList", GetWindowChildsList, 1, ""},
	{"GetProcessName", GetProcessName, 1, ""},
	{"GetProcessDict", GetProcessDict, 1, ""},
	{"GetWindowText", PyWin_GetWindowText, 1, ""},
	{"GetClassName", PyWin_GetClassName, 1, ""},
	{NULL, NULL}
};


PyMODINIT_FUNC
initcFunctions(void)
{
	Py_InitModule("cFunctions", example_methods);
}

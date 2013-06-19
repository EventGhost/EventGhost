#include "Python.h"


#include "registry_funcs.h"
#include "keyhook.h"


static PyMethodDef example_methods[] = {
	{"RegEnumKeysAndValues", RegEnumKeysAndValues, 1, ""},
	{"RegisterKeyhook", RegisterKeyhook, 1, ""},
	{"UnregisterKeyhook", UnregisterKeyhook, 1, ""},
	{"ResetIdleTimer", ResetIdleTimer, 1, ""},
	{"SetIdleTime", SetIdleTime, 1, ""},
	{"SetKeyboardCallback", SetKeyboardCallback, 1, ""},
	{"SetMouseCallback", SetMouseCallback, 1, ""},
	{NULL, NULL}
};


PyMODINIT_FUNC
initcFunctions(void)
{
	Py_InitModule("cFunctions", example_methods);
}

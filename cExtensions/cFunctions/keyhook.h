#include "Python.h"


extern PyObject *
RegisterKeyhook(PyObject *self, PyObject *args);

extern PyObject *
UnregisterKeyhook(PyObject *self, PyObject *args);

extern PyObject *
ResetIdleTimer(PyObject *self, PyObject *args);

extern PyObject *
SetIdleTime(PyObject *self, PyObject *args);

extern PyObject *
SetKeyboardCallback(PyObject *self, PyObject *args);

extern PyObject *
SetMouseCallback(PyObject *self, PyObject *args);
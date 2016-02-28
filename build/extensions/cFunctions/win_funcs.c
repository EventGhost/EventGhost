#define UNICODE
#include "Python.h"
#define _WIN32_WINNT 0x501
#include <windows.h>
#include <stdio.h>
#include <tchar.h>
#include <tlhelp32.h>

BOOL CALLBACK 
EnumAllWindowsProc(HWND hwnd, LPARAM lParam)
{
	PyObject *item;
	item = PyLong_FromVoidPtr(hwnd);
	PyList_Append((PyObject *) lParam, item);
	Py_DECREF(item); 
	return TRUE;
}

BOOL CALLBACK
EnumVisibleWindowsProc(HWND hwnd, LPARAM lParam)
{
	if (IsWindowVisible(hwnd))
	{	
		PyObject *item;

		item = PyLong_FromVoidPtr(hwnd);
		PyList_Append((PyObject *) lParam, item);
		Py_DECREF(item); 
	}
	return TRUE;
}


PyObject *
GetTopLevelWindowList(PyObject *self, PyObject *args)
{ 
	PyObject *pyWindowList;
	BOOL invisible=TRUE;

	if (!PyArg_ParseTuple(args, "|B", &invisible))
		return NULL;
	pyWindowList = PyList_New(0);
	if (invisible)
		EnumWindows((WNDENUMPROC) EnumAllWindowsProc, (LPARAM) pyWindowList);
	else
		EnumWindows((WNDENUMPROC) EnumVisibleWindowsProc, (LPARAM) pyWindowList);
	return Py_BuildValue("O", pyWindowList);
}


PyObject *
GetWindowChildsList(PyObject *self, PyObject *args)
{ 
	PyObject *pyWindowList;
	BOOL invisible=TRUE;
	HWND hWndParent;

	if (!PyArg_ParseTuple(args, "l|B", &hWndParent, &invisible))
		return NULL;
	pyWindowList = PyList_New(0);
	if (invisible)
		EnumChildWindows(hWndParent, (WNDENUMPROC) EnumAllWindowsProc, (LPARAM) pyWindowList);
	else
		EnumChildWindows(hWndParent, (WNDENUMPROC) EnumVisibleWindowsProc, (LPARAM) pyWindowList);
	return Py_BuildValue("O", pyWindowList);
}


PyObject *
PyWin_GetWindowText(PyObject *self, PyObject *args)
{
    HWND hwnd;
    int len;
	TCHAR buffer[512];

	if (!PyArg_ParseTuple(args, "l", &hwnd))
		return NULL;
    Py_BEGIN_ALLOW_THREADS
    len = GetWindowText(hwnd, buffer, sizeof(buffer)/sizeof(TCHAR));
    Py_END_ALLOW_THREADS
	return PyUnicode_FromWideChar(buffer, len);
}


PyObject *
PyWin_GetClassName(PyObject *self, PyObject *args)
{
    HWND hwnd;
    int len;
	TCHAR buffer[512];

	if (!PyArg_ParseTuple(args, "l", &hwnd))
		return NULL;
    Py_BEGIN_ALLOW_THREADS
	len = GetClassName(hwnd, buffer, 512);
    Py_END_ALLOW_THREADS
	return PyUnicode_FromWideChar(buffer, len);
}



PyObject *
GetProcessName(PyObject *self, PyObject *args)
{
	HANDLE hProcessSnap;
	PROCESSENTRY32 pe32;
	DWORD pid;

	if (!PyArg_ParseTuple(args, "k", &pid))
		return NULL;

	// Take a snapshot of all processes in the system.
	hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	if(hProcessSnap == INVALID_HANDLE_VALUE)
	{
		PyErr_SetFromWindowsErrWithFilename(0, "CreateToolhelp32Snapshot");
		return NULL;
	}

	// Set the size of the structure before using it.
	pe32.dwSize = sizeof(PROCESSENTRY32);

	// Retrieve information about the first process,
	// and exit if unsuccessful
	if(!Process32First(hProcessSnap, &pe32))
	{
		CloseHandle(hProcessSnap);          // clean the snapshot object
		PyErr_SetFromWindowsErrWithFilename(0, "Process32First");
		return NULL;
	}

	// Now walk the snapshot of processes
	do
	{
		if(pe32.th32ProcessID == pid)
		{
			CloseHandle(hProcessSnap);
			return PyUnicode_FromWideChar(pe32.szExeFile, wcslen(pe32.szExeFile));
		}
	}while(Process32Next(hProcessSnap, &pe32));

	CloseHandle(hProcessSnap);
	return Py_BuildValue("s", "<not found>");
}


PyObject *
GetProcessDict(PyObject *self, PyObject *args)
{
	HANDLE hProcessSnap;
	PROCESSENTRY32 pe32;
	PyObject *pyDict, *pyPid, *pyName;

	if (!PyArg_ParseTuple(args, "")) 
		return NULL;

	// Take a snapshot of all processes in the system.
	hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	if(hProcessSnap == INVALID_HANDLE_VALUE)
	{
		PyErr_SetFromWindowsErrWithFilename(0, "CreateToolhelp32Snapshot");
		return NULL;
	}

	// Set the size of the structure before using it.
	pe32.dwSize = sizeof(PROCESSENTRY32);

	// Retrieve information about the first process,
	// and exit if unsuccessful
	if(!Process32First(hProcessSnap, &pe32))
	{
		CloseHandle(hProcessSnap);          // clean the snapshot object
		PyErr_SetFromWindowsErrWithFilename(0, "Process32First");
		return NULL;
	}

	// create a dictionary for the results
	pyDict = PyDict_New();

	// Now walk the snapshot of processes
	do
	{
		pyPid = PyInt_FromLong(pe32.th32ProcessID);
		pyName = PyUnicode_FromWideChar(pe32.szExeFile, wcslen(pe32.szExeFile));
		PyDict_SetItem(pyDict, pyPid, pyName);
		Py_DECREF(pyPid);
		Py_DECREF(pyName);
	}while(Process32Next(hProcessSnap, &pe32));

	CloseHandle(hProcessSnap);
	return pyDict;
}

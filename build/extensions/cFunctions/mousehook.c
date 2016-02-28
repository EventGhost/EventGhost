#include "Python.h"
#define _WIN32_WINNT 0x501
#include "windows.h"
#include "utils.h"
#include "hooks.h"

PyObject* gPyMouseCallback = NULL;
HHOOK oldMouseHook = NULL;


LRESULT CALLBACK MouseHookProc(int nCode, WPARAM wParam, LPARAM lParam) 
{
	PyObject *arglist, *pyRes;
	PyGILState_STATE gil;
	PMSLLHOOKSTRUCT mhs;
	static BOOL mouseState[5] = {FALSE, FALSE, FALSE, FALSE, FALSE};
	char *mesg = NULL;
	int buttonNum = 0;
	int param = 0;
	
	AwakeWaitThread();
	if (nCode == HC_ACTION)
	{	
		mhs = (PMSLLHOOKSTRUCT) lParam;
		switch(wParam)
		{
			//case WM_LBUTTONDOWN:
			//	DBG("WM_LBUTTONDOWN");
			//	mouseState[0] = TRUE;
			//	mesg = "LeftButton";
			//	buttonNum = 0;
			//	param = 1;
			//	break;
			//case WM_LBUTTONUP:
			//	DBG("WM_LBUTTONUP");
			//	mouseState[0] = FALSE;
			//	mesg = "LeftButton";
			//	buttonNum = 0;
			//	param = 0;
			//	break;
			//case WM_MOUSEMOVE:
			//	DBG("WM_MOUSEMOVE");
			//	break;
			//case WM_MOUSEWHEEL:
			//	DBG("WM_MOUSEWHEEL");
			//	break;
			case WM_MBUTTONDOWN:
				DBG("WM_MBUTTONDOWN");
				mouseState[1] = TRUE;
				mesg = "MiddleButton";
				buttonNum = 1;
				param = 1;
				break;
			case WM_MBUTTONUP:
				DBG("WM_MBUTTONUP");
				mouseState[1] = FALSE;
				mesg = "MiddleButton";
				buttonNum = 1;
				param = 0;
				break;
			//case WM_RBUTTONDOWN:
			//	DBG("WM_RBUTTONDOWN");
			//	mouseState[2] = TRUE;
			//	mesg = "RightButton";
			//	buttonNum = 2;
			//	param = 1;
			//	break;
			//case WM_RBUTTONUP:
			//	DBG("WM_RBUTTONUP");
			//	mouseState[2] = FALSE;
			//	mesg = "RightButton";
			//	buttonNum = 2;
			//	param = 0;
			//	break;
			case WM_XBUTTONDOWN:
				DBG("WM_XBUTTONDOWN");
				if (HIWORD(mhs->mouseData) == XBUTTON1)
				{
					mouseState[3] = TRUE;
					mesg = "XButton1";
					buttonNum = 3;
				}else{
					mouseState[4] = TRUE;
					mesg = "XButton2";
					buttonNum = 4;
				}
				param = 1;
				break;
			case WM_XBUTTONUP:
				DBG("WM_XBUTTONUP");
				if (HIWORD(mhs->mouseData) == XBUTTON1)
				{
					mouseState[3] = FALSE;
					mesg = "XButton1";
					buttonNum = 3;
				}else{
					mouseState[4] = FALSE;
					mesg = "XButton2";
					buttonNum = 4;
				}
				param = 0;
				break;
			//case WM_XBUTTONDBLCLK:
			//	DBG("WM_XBUTTONDBLCLK");
			//	break;
			//default:
			//	DBG("unknown mouse message");
		}
		if (mesg && gPyMouseCallback)
		{
			gil = PyGILState_Ensure();
			arglist = Py_BuildValue("(sii)", mesg, buttonNum, param);

			pyRes = PyObject_CallObject(gPyMouseCallback, arglist);
			if(pyRes == NULL)
			{
				PyErr_Print();
			}else{
				if (Py_True == pyRes)
				{
					Py_XDECREF(pyRes);
					Py_DECREF(arglist);
					PyGILState_Release(gil);
					//gkhd.blocked = TRUE;
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


PyObject *
SetMouseCallback(PyObject *self, PyObject *args)
{
	PyObject* callback;

	if (!PyArg_ParseTuple(args, "O", &callback))
	{
		PyErr_Print();
		return NULL;
	}
	Py_XDECREF(gPyMouseCallback);
	if (callback == Py_None)
	{
		callback = NULL;
	}
	Py_XINCREF(callback);
	gPyMouseCallback = callback;
	Py_RETURN_NONE;
}


void SetMouseHook(HINSTANCE hMod)
{
	oldMouseHook = SetWindowsHookEx(WH_MOUSE_LL, MouseHookProc, (HINSTANCE) hMod, 0);
}

void UnsetMouseHook(void)
{
	UnhookWindowsHookEx(oldMouseHook);
}
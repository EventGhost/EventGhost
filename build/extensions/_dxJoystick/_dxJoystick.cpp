#include "Python.h"

#define STRICT
#define DIRECTINPUT_VERSION 0x0800
#include <dinput.h>

#define SAFE_DELETE(p)  { if(p) { delete (p);     (p)=NULL; } }
#define SAFE_RELEASE(p) { if(p) { (p)->Release(); (p)=NULL; } }
#define MAXJOYSTICKS 8
#define POSTRIP 500
#define NEGTRIP -500
#define MESSLEN 15

enum EVENTTYPE {
	EVT_DIRECTION,
	EVT_BTN_RELEASED,
	EVT_BTN_PUSHED,
	EVT_X_AXIS,
	EVT_Y_AXIS,
	EVT_Z_AXIS,
};

enum EVENT_DIRECTION{
	MIDDLE,
	UP,
	RIGHT,
	DOWN,
	LEFT
};

enum MY_ERROR_CODES{
	OK,
	ERR_NO_JOYSTICK_CONNECTED,
	ERR_CANNOT_CREATE_POLLINGTHREAD,
};

// *** globals ***
DWORD PollingTimeout = 5;	// default to poll a new joypad every ~5 ms
LPDIRECTINPUT8       g_pDI = NULL;
LPDIRECTINPUTDEVICE8 g_pJoystick[MAXJOYSTICKS] = {NULL};
DIJOYSTATE2 oldjoyst[MAXJOYSTICKS]; 
int g_joyno = 0;     
HINSTANCE hInstance;
HANDLE DeathEvent=NULL;
HANDLE PollingThreadHandle=NULL;
static PyObject *gCallback = NULL;

BOOL CALLBACK EnumObjectsCallback( const DIDEVICEOBJECTINSTANCE* pdidoi, VOID* pContext );
BOOL CALLBACK EnumJoysticksCallback( const DIDEVICEINSTANCE* pdidInstance, VOID* pContext );
bool WalkandSend(const DIJOYSTATE2 *newjoy, const DIJOYSTATE2 *oldjoy, int joynumber);
HRESULT InitDirectInput();
HRESULT UpdateInputState();
VOID FreeDirectInput();

//misc calls to return data from here
HINSTANCE GetDllHandle()
{
	return GetModuleHandle(NULL);
}

void TriggerEvent(int joynumber, EVENTTYPE etype, int value)
{
    PyObject *arglist;
    PyObject *result;

	if (gCallback != NULL)
	{
		/* Time to call the callback */
		arglist = Py_BuildValue("(iii)", joynumber, etype, value);
		PyGILState_STATE gstate;
		gstate = PyGILState_Ensure();
		result = PyEval_CallObject(gCallback, arglist);
		Py_DECREF(arglist);
		Py_DECREF(result);
		PyGILState_Release(gstate);
	}
}

//-----------------------------------------------------------------------------
// Name: PollingThread()
// output: return value/code
// Desc: Thread function that polls a new joystick every ?5ms.
// It also reports thru girder how many joysticks it found
//-----------------------------------------------------------------------------
DWORD WINAPI PollingThread( LPVOID lpParameter )
{
	// space for message
	char cString[256] = {0};
	
	//report no. of joysticks found and wait a sec to read it.
	Sleep(400);
	//sprintf(cString, "Found %d JoyPads", (g_joyno));
	//TriggerEvent(cString);
	//Sleep(2000);

	// main polling loop
	while (WaitForSingleObject(DeathEvent, PollingTimeout) == WAIT_TIMEOUT)
	{
        if( FAILED(UpdateInputState()) ){
            sprintf(cString, "Error Updating Joypad");
			//TriggerEvent(cString);
        }
	}

	// exit thread
	return 0;
}

//-----------------------------------------------------------------------------
// Name: Open_Port()
// output: none
// Desc: Sets up and creates thread after initializing directx and enumerating 
// joysticks
//-----------------------------------------------------------------------------
HRESULT Open_Port()
{
	DWORD dwThreadId;
	HRESULT err;

	// set up exit condition semaphore
	DeathEvent = CreateEvent(NULL, TRUE, TRUE, NULL);
	ResetEvent(DeathEvent);

	err = InitDirectInput();
	if (err) return err;

	// start polling thread
	PollingThreadHandle = CreateThread(NULL,0,&PollingThread,hInstance,0,&dwThreadId);
	if (PollingThreadHandle == NULL)
	{
		return ERR_CANNOT_CREATE_POLLINGTHREAD;
	}
	return OK;
}

//-----------------------------------------------------------------------------
// Name: Close_Port()
// output: none
// Desc: kills thread then frees directx objects
//-----------------------------------------------------------------------------
void Close_Port()
{
	
	if (PollingThreadHandle != NULL)
	{
		// signal thread to complete
		SetEvent(DeathEvent);
		// wait for thread to complete
		WaitForSingleObject(PollingThreadHandle, 40000);
		// free resources
		CloseHandle(DeathEvent);
		DeathEvent = NULL;
		CloseHandle(PollingThreadHandle);
		PollingThreadHandle = NULL;
	}
    FreeDirectInput();    
}

//-----------------------------------------------------------------------------
// Name: InitDirectInput()
// output: none
// Desc: very similar to microsoft directinput reference code.  I added multiple
// joystick enumeration, tho.
//-----------------------------------------------------------------------------
HRESULT InitDirectInput()
{
    HRESULT hr;

    // Register with the DirectInput subsystem and get a pointer
    // to a IDirectInput interface we can use.
    // Create a DInput object
    if( FAILED( hr = DirectInput8Create( GetDllHandle(), DIRECTINPUT_VERSION, 
                                         IID_IDirectInput8, (VOID**)&g_pDI, NULL ) ) )	
	{
        return hr;
	}

    // Enumerate all joysticks in the system. this proggy only can use MAXJOYSTICKS.
	if( FAILED( hr = g_pDI->EnumDevices( DI8DEVCLASS_GAMECTRL, 
										 EnumJoysticksCallback,
										 NULL, DIEDFL_ATTACHEDONLY ) ) )
		return hr;

    // Make sure we got at least one joystick
    if( NULL == g_pJoystick[0] )
    {
        //MessageBox( NULL, TEXT("Joystick not found. plugin will not work"),  
        //            TEXT("Joypad plugin"), 
        //            MB_ICONERROR | MB_OK );
        return DIERR_UNPLUGGED;
    }

    // Set the data format to "simple joystick" - a predefined data format 
    //
    // A data format specifies which controls on a device we are interested in,
    // and how they should be reported. This tells DInput that we will be
    // passing a DIJOYSTATE2 structure to IDirectInputDevice::GetDeviceState().
	// We need to repeat this setup and enumeration for each joystick.
	for (int c = 0; (c < MAXJOYSTICKS) && (g_pJoystick[c] != NULL); c++) {
		if( FAILED( hr = g_pJoystick[c]->SetDataFormat( &c_dfDIJoystick2 ) ) )
			return hr;

		// Set the cooperative level to let DInput know how this device should
		// interact with the system and with other DInput applications.
		//if( FAILED( hr = g_pJoystick->SetCooperativeLevel( hDlg, DISCL_NONEXCLUSIVE | 
		//                                                         DISCL_BACKGROUND  ) ) )
		if( FAILED( hr = g_pJoystick[c]->SetCooperativeLevel( NULL, DISCL_NONEXCLUSIVE | 
																 DISCL_BACKGROUND  ) ) )
			return hr;

		// Enumerate the joystick objects. The callback function enabled user
		// interface elements for objects that are found, and sets the min/max
		// values property for discovered axes.
		// The callback is run once for each axis object for each joystick.
		// c is passed so that the callback knows which joystick to setup
		if( FAILED( hr = g_pJoystick[c]->EnumObjects( EnumObjectsCallback, 
		                                            (VOID*)(&c), DIDFT_AXIS ) ) )
		    return hr;
	}

    return S_OK;
}

//-----------------------------------------------------------------------------
// Name: EnumJoysticksCallback()
// Desc: Called once for each enumerated joystick. If we find one, create a
//       device interface on it so we can play with it.
//-----------------------------------------------------------------------------
BOOL CALLBACK EnumJoysticksCallback( const DIDEVICEINSTANCE* pdidInstance,
                                     VOID* pContext )
{
    HRESULT hr;
    // Obtain an interface to the enumerated joystick.
    hr = g_pDI->CreateDevice( pdidInstance->guidInstance, &g_pJoystick[g_joyno], NULL );

    // If it failed, then we can't use this joystick. (Maybe the user unplugged
    // it while we were in the middle of enumerating it.)
    if( FAILED(hr) ) 
        return DIENUM_CONTINUE;

 	//increment the found joysticks and tell windows to keep looking.
	g_joyno++;
    return DIENUM_CONTINUE;
}

//-----------------------------------------------------------------------------
// Name: EnumObjectsCallback()
// input: pdidoi = pointer to the object being enumerated(like an axis or button)
//        pContext = pointer to the joystick number
// output: bool used to tell the Windows caller to go on or stop.
// Desc: Callback function for enumerating objects on a joystick. 
// This function enables user interface elements for objects
// that are found to exist, and scales axes min/max values.  It only looks for
// Axis objects right now.
//-----------------------------------------------------------------------------
BOOL CALLBACK EnumObjectsCallback( const DIDEVICEOBJECTINSTANCE* pdidoi,
                                   VOID* pContext )
{
	int enumjoynumber = *(int *)pContext;
    // For axes that are returned, set the DIPROP_RANGE property for the
    // enumerated axis in order to scale min/max values.
    if( pdidoi->dwType & DIDFT_AXIS )
    {
        DIPROPRANGE diprg; 
        diprg.diph.dwSize       = sizeof(DIPROPRANGE); 
        diprg.diph.dwHeaderSize = sizeof(DIPROPHEADER); 
        diprg.diph.dwHow        = DIPH_BYID; 
        diprg.diph.dwObj        = pdidoi->dwType; // Specify the enumerated axis
        diprg.lMin              = -1000; 
        diprg.lMax              = +1000; 
    
        // Set the range for the axis
        if( FAILED( g_pJoystick[enumjoynumber]->SetProperty( DIPROP_RANGE, &diprg.diph ) ) ) 
            return DIENUM_STOP;
    }
    return DIENUM_CONTINUE;
}

//-----------------------------------------------------------------------------
// Name: UpdateInputState()
// Desc: Get the input device's state.  Only send girder a new event if the state
// has changed from its previous value.  This will cut down on unecessary traffic
// between the app and dll.  
// This function uses a round robin approach.  It sends events to girder for each
// item that has changed on a particular controller.  The next time the thread 
// calls it, it will look at the next lowest joystick. All controllers get equal 
// time this way.
//-----------------------------------------------------------------------------
HRESULT UpdateInputState()
{
    HRESULT     hr;
    //TCHAR       strText[512]; // Device state text
    DIJOYSTATE2 js;      // current DInput joystick state 
    //TCHAR*      str;
	static int joynum = g_joyno - 1;
	int jtest = joynum;

    if( NULL == g_pJoystick[joynum] ) 
        return S_OK;

    // Poll the device to read the current state
    hr = g_pJoystick[joynum]->Poll(); 
    if( FAILED(hr) )  
    {
        // DInput is telling us that the input stream has been
        // interrupted. We aren't tracking any state between polls, so
        // we don't have any special reset that needs to be done. We
        // just re-acquire and try again.
        hr = g_pJoystick[joynum]->Acquire();
        while( hr == DIERR_INPUTLOST ) 
            hr = g_pJoystick[joynum]->Acquire();

        // hr may be DIERR_OTHERAPPHASPRIO or other errors.  This
        // may occur when the app is minimized or in the process of 
        // switching, so just try again later 
        return S_OK; 
    }

    // Get the input's device state
    if( FAILED( hr = g_pJoystick[joynum]->GetDeviceState( sizeof(DIJOYSTATE2), &js ) ) )
        return hr; // The device should have been acquired during the Poll()

	//walk thru all of the controls on a joystick and send girder a message for 
	//each that has changed.
	WalkandSend(&js, &oldjoyst[joynum], joynum);

    //decrement to the next lowest joystick for next poll
	oldjoyst[joynum] = js;
	if (--joynum < 0)
		joynum = g_joyno - 1;

	return S_OK;
}

//-----------------------------------------------------------------------------
// Name: WalkandSend()
// input: newjoy = pointer to the current joypad control values
//        oldjoy = pointer to the last read joypad control values
///	      joynumber = joystick number being polled
// output: bool that is not used.
// Desc: This function walks thru each item/control on a joystick and sends 
// girder a message string for each item/control that has changed from the last
// time it was polled.  This should cut down on girder/dll traffic.  This is 
// where a person would add new joystick functions to check and send.  Only two
// axis and all buttons are dealt with now. 
//-----------------------------------------------------------------------------
bool WalkandSend(const DIJOYSTATE2 *newjoy, const DIJOYSTATE2 *oldjoy, int joynumber)
{
	char cText[MESSLEN] = {0};
	int len = 0;
	// x-axis position **********************************
	//move to middle
	if ( (newjoy->lX > NEGTRIP) && (newjoy->lX < POSTRIP) ) {
		if ( (oldjoy->lX < NEGTRIP) || (oldjoy->lX > POSTRIP) ) {
            //len = sprintf(cText, "J%d:XC", joynumber);
			//assert (len < MESSLEN - 1);
			TriggerEvent(joynumber, EVT_X_AXIS, 0);
		}
	}
	//move left		
	if (newjoy->lX < NEGTRIP) {
		if (oldjoy->lX > NEGTRIP) {
            //len = sprintf(cText, "J%d:XL", joynumber);
			//assert (len < MESSLEN - 1);
			TriggerEvent(joynumber, EVT_X_AXIS, -1);
		}
	}
	//move right
	if (newjoy->lX > POSTRIP) {
		if (oldjoy->lX < POSTRIP) {
            //len = sprintf(cText, "J%d:XR", joynumber);
			//assert (len < MESSLEN - 1);
			TriggerEvent(joynumber, EVT_X_AXIS, 1);
		}
	}
	// y-axis position **********************************
	//move to middle
	if ( (newjoy->lY > NEGTRIP) && (newjoy->lY < POSTRIP) ) {
		if ( (oldjoy->lY < NEGTRIP) || (oldjoy->lY > POSTRIP) ) {
            //len = sprintf(cText, "J%d:YC", joynumber);
			//assert (len < MESSLEN - 1);
			TriggerEvent(joynumber, EVT_Y_AXIS, 0);
		}
	}
	//move up		
	if (newjoy->lY < NEGTRIP) {
		if (oldjoy->lY > NEGTRIP) {
            //len = sprintf(cText, "J%d:YU", joynumber);
			//assert (len < MESSLEN - 1);
			TriggerEvent(joynumber, EVT_Y_AXIS, -1);
		}
	}
	//move down
	if (newjoy->lY > POSTRIP) {
		if (oldjoy->lY < POSTRIP) {
            //len = sprintf(cText, "J%d:YD", joynumber);
			//assert (len < MESSLEN - 1);
			TriggerEvent(joynumber, EVT_Y_AXIS, 1);
		}
	}
	/*
	if (newjoy->rglSlider[0] != oldjoy->rglSlider[0]) {
		len = sprintf(cText, "J%d:Z:%d", joynumber, newjoy->rglSlider[0]);
			assert (len < MESSLEN - 1);
			//TriggerEvent(cText);
	}
	*/
    /*others that can be implemented  
    LONG    lZ;                     // z-axis position   
    DWORD   rgdwPOV[4];             // POV directions    
	*/
	//all buttons***************************************
    for( int i = 0; i < 128; i++ )
    {
        if ( (newjoy->rgbButtons[i] & 0x80) != (oldjoy->rgbButtons[i] & 0x80) ) {
			if (newjoy->rgbButtons[i] & 0x80) {
				len = sprintf(cText, "J%d:B%dON", joynumber, i);
				assert (len < MESSLEN - 1);
				TriggerEvent(joynumber, EVT_BTN_PUSHED, i);
			}
			else {
				len = sprintf(cText, "J%d:B%dOFF", joynumber, i);
				assert (len < MESSLEN - 1);
				TriggerEvent(joynumber, EVT_BTN_RELEASED, i);
			}
		}
	}
	return true;
}


//-----------------------------------------------------------------------------
// Name: FreeDirectInput()
// Desc: free directinput objects.
//-----------------------------------------------------------------------------
VOID FreeDirectInput()
{
    // Unacquire the device one last time just in case 
    // the app tried to exit while the device is still acquired.
	for (int c = 0; (c < MAXJOYSTICKS) && (g_pJoystick[c] != NULL); c++) {
		if( g_pJoystick[c] ) 
			g_pJoystick[c]->Unacquire();
    
		// Release any DirectInput objects.
		SAFE_RELEASE( g_pJoystick[c] );
	}
    SAFE_RELEASE( g_pDI );
	g_joyno = 0;
}

//static PyObject *
//ex_foo(PyObject *self, PyObject *args)
//{
//	PyEval_InitThreads();
//	Open_Port();
//	Py_INCREF(Py_None);
//	return Py_None;
//}

static PyObject *
RegisterEventFunc(PyObject *self, PyObject *args)
{
	PyObject *callback;
    PyObject *result = NULL;

    if (PyArg_ParseTuple(args, "O:set_callback", &callback))
	{
		if (callback == Py_None)
		{
			Py_XDECREF(gCallback);  /* Dispose of previous callback */
			gCallback = NULL;
			Close_Port();
			Py_RETURN_NONE;
		}
		if ((callback != Py_None) && (!PyCallable_Check(callback)) )
		{
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        if(gCallback == NULL)
		{
			PyEval_InitThreads();
			Open_Port();
		}
		Py_XINCREF(callback);  /* Add a reference to new callback */
        Py_XDECREF(gCallback); /* Dispose of previous callback */
        gCallback = callback;  /* Remember new callback */
        /* Boilerplate to return "None" */
        Py_INCREF(Py_None);
        result = Py_None;
    }
    return result;
}

static PyMethodDef _dxJoystick_methods[] = {
//	{"foo", ex_foo, 1, "foo() doc string"},
	{"RegisterEventFunc", RegisterEventFunc, 1, ""},
	{NULL, NULL}
};


PyMODINIT_FUNC
init_dxJoystick(void)
{
	Py_InitModule("_dxJoystick", _dxJoystick_methods);
}


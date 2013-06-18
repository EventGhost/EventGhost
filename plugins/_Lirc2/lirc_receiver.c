#include "Python.h"
#define _WIN32_WINNT 0x500
#include "windows.h"
#include "utils.h"

#define DEBUG_WINERR(msg) print(msg, GetLastError())

#define BUF_LEN 1024

typedef struct {
	int portNum;
	HANDLE transferThreadHandle;
	HANDLE irThreadHandle;
	HANDLE quitIrThreadEvent;
	HANDLE hasQuitIrThreadEvent;
	HANDLE quitTransferThreadEvent;
	HANDLE hasQuitTransferThreadEvent;

	HANDLE dataReadyEvent;
	PyObject *dataCallback;
	unsigned long buffer[BUF_LEN];
	int bufferStart;
	int bufferEnd;
}config_struct, *config_ptr;



DWORD WINAPI 
IrThread(config_ptr cfg)
{
	HANDLE hPort;
	OVERLAPPED ov;
	DCB dcb;
	DWORD status;
	DWORD dwEvtMask = EV_RLSD;
	DWORD event;
	HANDLE events[2];
	DWORD counter = 0;
	BOOL state;
	BOOL lastState;
	__int64 counterFrequency;
	__int64 performanceCount;
	__int64 lastPerformanceCount;
	unsigned long deltaT;
	int res;
	char portName[8] = "COM";
	unsigned long *buffer;
	int diff;
	int bufferEnd = 0;
	DWORD timeout = INFINITE;
	HANDLE dataReadyEvent = cfg->dataReadyEvent;

	DEBUG("Starting ThreadProc");
	
	if(!SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL))
		DEBUG_WINERR("SetThreadPriority");
	
	buffer = cfg->buffer;

	QueryPerformanceFrequency((LARGE_INTEGER *)&counterFrequency);
	
	itoa(cfg->portNum+1, &portName[3], 10);

	hPort = CreateFile(
		portName, 
		GENERIC_READ | GENERIC_WRITE,
		0,		// exclusive access 
		NULL,	// default security attributes 
		OPEN_EXISTING, 
		FILE_FLAG_OVERLAPPED, 
		NULL);
	if(hPort == INVALID_HANDLE_VALUE)
	{
		DEBUG_WINERR("CreateFile");
		goto out1;
	}

	if(!GetCommState(hPort, &dcb))
	{
		goto out2;
	}

	dcb.fDtrControl=DTR_CONTROL_DISABLE; // set the transmit LED to off initially.
	dcb.fRtsControl=RTS_CONTROL_ENABLE;
	dcb.BaudRate = 115200;					

	if(!SetCommState(hPort, &dcb))
	{
		DEBUG_WINERR("SetCommState1");
		goto out2;
	}

	if((ov.hEvent = CreateEvent(NULL, TRUE, FALSE, NULL)) == NULL)
	{
		DEBUG_WINERR("CreateEvent");
		goto out2;
	}
	events[0] = ov.hEvent;
	events[1] = cfg->quitIrThreadEvent;

	GetCommModemStatus(hPort, &status);
	state = (status & MS_RLSD_ON) ? TRUE : FALSE;
	lastState = !state;

	QueryPerformanceCounter((LARGE_INTEGER *) &lastPerformanceCount);

	/* We want to be notified of changes */
	if(SetCommMask(hPort, dwEvtMask)==0)	
	{
		DEBUG_WINERR("SetCommMask");
	}

	for(;;)
	{
		/* Reset the event */
		ResetEvent(ov.hEvent);
		/* Start waiting for the event */
		if(WaitCommEvent(hPort, &event, &ov) == 0 && GetLastError() != ERROR_IO_PENDING)
		{
			DEBUG_WINERR("WaitCommEvent error: %d");
		}

		/* Wait for the event to get triggered */	
		res = WaitForMultipleObjects(2, events, FALSE, INFINITE);

		QueryPerformanceCounter((LARGE_INTEGER *) &performanceCount);

		switch(res)
		{
			case WAIT_FAILED:
				DEBUG("Wait failed.");
				continue;
			
			case WAIT_OBJECT_0:
				state = !state;
				break;

			case WAIT_OBJECT_0+1:
				//DEBUG("IRThread terminating");
				goto out3;
			
			default:
				DEBUG("Wrong object in WaitForMultipleObjects");
				continue;
		}	
		deltaT = ((performanceCount - lastPerformanceCount) * 1000000) / counterFrequency;

		bufferEnd = cfg->bufferEnd;
		diff = cfg->bufferStart - bufferEnd;
		if(diff < 0) 
			diff += BUF_LEN;
		if(diff != 1)
		{
			buffer[bufferEnd++] = deltaT;
			if(bufferEnd >= BUF_LEN) 
				bufferEnd = 0;
			cfg->bufferEnd = bufferEnd;
			SetEvent(dataReadyEvent);
		}
		else
		{
			DEBUG("buffer full");
		}
		lastPerformanceCount = performanceCount;
	}

out3:
	CloseHandle(ov.hEvent);
out2:
	CloseHandle(hPort);
out1:
	hPort = NULL;
	SetEvent(cfg->hasQuitIrThreadEvent);
	return 0;
}


DWORD WINAPI 
TransferThread(config_ptr cfg)
{
	HANDLE events[2] = {cfg->dataReadyEvent, cfg->quitTransferThreadEvent};
	unsigned long deltaT;
	int counter = 0;
	unsigned long *buffer = cfg->buffer;
	int bufferStart = 0;
	PyGILState_STATE gil;
	PyObject *arglist, *pyRes;

	if(!SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL))
		DEBUG_WINERR("SetThreadPriority");

	for(;;)
	{
		switch(WaitForMultipleObjects(2, events, FALSE, INFINITE))
		{
			case WAIT_FAILED:
				DEBUG("Wait failed.");
				continue;
			
			case WAIT_OBJECT_0:
				break;

			case WAIT_OBJECT_0+1:
				//DEBUG("WaitThread terminating");
				SetEvent(cfg->hasQuitTransferThreadEvent);
				return 0;
			
			default:
				DEBUG("Wrong object in WaitForMultipleObjects");
				continue;
		}
		while(cfg->bufferEnd != bufferStart)
		{
			deltaT = buffer[bufferStart++];
			if(bufferStart >= BUF_LEN) 
				bufferStart = 0;
			cfg->bufferStart = bufferStart;

			gil = PyGILState_Ensure();
			arglist = Py_BuildValue("(k)", deltaT);
			pyRes = PyObject_CallObject(cfg->dataCallback, arglist);
			if(pyRes == NULL)
			{
				PyErr_Print();
			}			
			Py_XDECREF(pyRes);
			Py_DECREF(arglist);

			PyGILState_Release(gil);
			counter++;
		}
	}
	SetEvent(cfg->hasQuitTransferThreadEvent);
	return 0;
}


PyObject *
StartLircReceiver(PyObject *self, PyObject *args)
{
	HANDLE handle;
	config_ptr cfgPtr;

	cfgPtr = malloc(sizeof(config_struct));

	if (!PyArg_ParseTuple(args, "Oi", &cfgPtr->dataCallback, &cfgPtr->portNum))
	{
		PyErr_Print();
		return NULL;
	}
	Py_INCREF(cfgPtr->dataCallback);
	cfgPtr->quitIrThreadEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
	cfgPtr->hasQuitIrThreadEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
	cfgPtr->quitTransferThreadEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
	cfgPtr->hasQuitTransferThreadEvent = CreateEvent(NULL, TRUE, FALSE, NULL);

	cfgPtr->dataReadyEvent = CreateEvent(NULL, FALSE, FALSE, NULL);

	DEBUG("StartLircReceiver");

	cfgPtr->irThreadHandle = CreateThread(NULL, 0, IrThread, cfgPtr, 0, NULL);
	cfgPtr->transferThreadHandle  = CreateThread(NULL, 0, TransferThread, cfgPtr, 0, NULL);

	return Py_BuildValue("k", cfgPtr);
}


PyObject *
StopLircReceiver(PyObject *self, PyObject *args)
{
	config_ptr cfgPtr;

	if (!PyArg_ParseTuple(args, "k", &cfgPtr))
	{
		PyErr_Print();
		return NULL;
	}
	SetEvent(cfgPtr->quitIrThreadEvent);
	if(WaitForSingleObject(cfgPtr->hasQuitIrThreadEvent, 3000) != WAIT_OBJECT_0)
		RAISE_SYSTEMERR("WaitForSingleObject IrThread");

	SetEvent(cfgPtr->quitTransferThreadEvent);
	if(WaitForSingleObject(cfgPtr->hasQuitTransferThreadEvent, 3000) != WAIT_OBJECT_0)
		RAISE_SYSTEMERR("WaitForSingleObject TransferThread");

	CloseHandle(cfgPtr->quitIrThreadEvent);
	CloseHandle(cfgPtr->hasQuitIrThreadEvent);
	CloseHandle(cfgPtr->quitTransferThreadEvent);
	CloseHandle(cfgPtr->hasQuitTransferThreadEvent);
	CloseHandle(cfgPtr->dataReadyEvent);
	CloseHandle(cfgPtr->irThreadHandle);
	CloseHandle(cfgPtr->transferThreadHandle);
	free(cfgPtr);
	Py_DECREF(cfgPtr->dataCallback);
	Py_RETURN_NONE;
}

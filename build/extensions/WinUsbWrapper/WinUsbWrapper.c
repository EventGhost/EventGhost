#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include "strsafe.h"
#include <objbase.h>

#pragma warning(disable:4200)  //
#pragma warning(disable:4201)  // nameless struct/union
#pragma warning(disable:4214)  // bit field types other than int

#include <setupapi.h>
#include <basetyps.h>
#include "usbdi.h"
#include <winusb.h>

#pragma warning(default:4200)
#pragma warning(default:4201)
#pragma warning(default:4214)

#define WHILE(a) \
while(__pragma(warning(disable:4127)) a __pragma(warning(disable:4127)))

#if defined(BUILT_IN_DDK)
#define scanf_s scanf
#endif

// Global variable for the instance (i.e. module) handle
static HINSTANCE hInstance = NULL;

typedef struct _ThreadParams {
	PWCHAR devicePath;
	HANDLE startEvent;
	HANDLE endEvent;
	HANDLE thread;
	HWND notifyWnd;
	UINT msg;
	UINT chunkSize;
	BOOL suppressRepeat;
	UINT error;
} ThreadParams, *PThreadParams;


BOOL WINAPI DllMain(HINSTANCE hModule, DWORD dwReason, LPVOID lpvReserved)
{
	switch(dwReason)
	{
	case DLL_PROCESS_ATTACH:
		DisableThreadLibraryCalls(hModule);
		hInstance = hModule;
		break;
	case DLL_PROCESS_DETACH:
		break;
	default:
	    break;
	}
	return TRUE;
}


ULONG Reader(PThreadParams params)
{
	BOOL bResult = FALSE;
	HANDLE deviceHandle = NULL;
	WINUSB_INTERFACE_HANDLE usbHandle = NULL;	
	USB_INTERFACE_DESCRIPTOR ifaceDescriptor;
	WINUSB_PIPE_INFORMATION pipeInfo;
	UCHAR inPipeId = 0;
	ULONG length = 0;
	UCHAR* buffer = NULL;
	UCHAR* oldBuffer = NULL;
	UCHAR* tmpBuffer;
	OVERLAPPED overlapped;
	HANDLE handles[2];
	int i;

	params->error = 1;
	deviceHandle = CreateFile(
		params->devicePath, 
		GENERIC_WRITE | GENERIC_READ, 
		FILE_SHARE_WRITE | FILE_SHARE_READ, 
		NULL, 
		OPEN_EXISTING, 
		FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED, NULL
	);

    if (deviceHandle == INVALID_HANDLE_VALUE)
	{
		printf("Failed to open the device, error - %d", GetLastError());
		goto exit;
	}

	bResult = WinUsb_Initialize(deviceHandle, &usbHandle);
	if (!bResult) 
		goto exit;

	bResult = WinUsb_QueryInterfaceSettings(usbHandle, 0, &ifaceDescriptor);
	if (!bResult) 
		goto exit;

//	printf("Num Endpoints: %i\r\n", ifaceDescriptor.bNumEndpoints);
	for (i=0; i<ifaceDescriptor.bNumEndpoints; i++)
	{			
		bResult = WinUsb_QueryPipe(usbHandle, 0, (UCHAR) i, &pipeInfo);
		if (!bResult) 
			goto exit;
//		printf("Pipe Type: %i (%s)\r\n", pipeInfo.PipeType, USB_ENDPOINT_DIRECTION_OUT(pipeInfo.PipeId)?"out":"in");
		if (USB_ENDPOINT_DIRECTION_IN(pipeInfo.PipeId)) 
			inPipeId = pipeInfo.PipeId;
	}

	if (inPipeId==0) 
		goto exit;

	memset(&overlapped, sizeof(OVERLAPPED), 0);
	overlapped.hEvent = CreateEvent(NULL, TRUE, FALSE, NULL);

	handles[0] = overlapped.hEvent;
	handles[1] = params->endEvent;
	buffer = (UCHAR*) HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, sizeof(params->chunkSize));
	oldBuffer = (UCHAR*) HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, sizeof(params->chunkSize));

	params->error = 0;
	SetEvent(params->startEvent);
	while (TRUE)
	{
		WinUsb_ReadPipe(usbHandle, inPipeId, buffer, params->chunkSize, &length, &overlapped);
		if (WaitForMultipleObjects(2, handles, FALSE, INFINITE)!=WAIT_OBJECT_0) goto exit;
		if (!params->suppressRepeat || memcmp(buffer, oldBuffer, params->chunkSize))
			SendMessage(params->notifyWnd, params->msg, length, (LPARAM) buffer);
		tmpBuffer = oldBuffer;
		oldBuffer = buffer;
		buffer = tmpBuffer;
		ResetEvent(overlapped.hEvent);
	}

exit:
	if (usbHandle) WinUsb_Free(usbHandle);
	if (deviceHandle) CloseHandle(deviceHandle);
	if (overlapped.hEvent) CloseHandle(overlapped.hEvent);
	if (buffer) HeapFree(GetProcessHeap(), 0, buffer);
	if (oldBuffer) HeapFree(GetProcessHeap(), 0, oldBuffer);
//	printf("Reader stopped");
	SetEvent(params->startEvent);
	return 1;
}


PThreadParams Start(HWND notifyWnd, UINT msg, WCHAR* devicePath, UINT chunkSize, BOOL suppressRepeat)
{
	PThreadParams threadParams;
	
	threadParams = (PThreadParams) HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, sizeof(ThreadParams));
	if (!threadParams)
	{
		printf("Start.HeapAlloc failed!");
		return NULL;
	}
	threadParams->devicePath = devicePath;
	threadParams->startEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
	if (!threadParams->startEvent)
	{
		printf("Start.CreateEvent1 failed");
		goto error_exit;
	}
	threadParams->endEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
	if (!threadParams->endEvent)
	{
		printf("Start.CreateEvent2 failed");
		goto error_exit;
	}
	threadParams->notifyWnd = notifyWnd;
	threadParams->msg = msg;
	threadParams->chunkSize = chunkSize;
	threadParams->suppressRepeat = suppressRepeat;
	threadParams->thread = CreateThread(NULL, 0, Reader, threadParams, 0, NULL);
	if (!threadParams->thread)
	{
		printf("Start.CreateThread failed");
		goto error_exit;
	}
	if (WaitForSingleObject(threadParams->startEvent, 2000) != WAIT_OBJECT_0)
	{
		printf("Error waiting for thread start\r\n");
		return NULL;
	}
	if (threadParams->error)
		return NULL;
	return threadParams;

error_exit:
	HeapFree(GetProcessHeap(), 0, threadParams);
	return NULL;
}


void Stop(PThreadParams threadParams)
{
	if (!threadParams)
		return;
	if (threadParams->endEvent) 
		SetEvent(threadParams->endEvent);
	if (threadParams->thread)
	{
		if (WaitForSingleObject(threadParams->thread, 1000)!=WAIT_OBJECT_0)
			printf("Error waiting for thread\r\n");
		CloseHandle(threadParams->thread);
	}
	if (threadParams->endEvent) 
		CloseHandle(threadParams->endEvent);
	HeapFree(GetProcessHeap(), 0, threadParams);
}


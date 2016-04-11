// dllmain.cpp : Defines the entry point for the DLL application.
#include "stdafx.h"
#include <stdlib.h>
#include <stdio.h>
#include <windows.h>
#include <commctrl.h>
#include <mmdeviceapi.h>
#include <endpointvolume.h>
#include <string.h>
#include <Functiondiscoverykeys_devpkey.h>
#include "Python.h"

#define EXIT_ON_ERROR(hr)  \
              if (FAILED(hr)) { goto Exit; }

#define SAFE_RELEASE(punk)  \
              if ((punk) != NULL)  \
                { (punk)->Release(); (punk) = NULL; }

HWND g_hDlg = NULL;
static PyObject *VolumeHandler = NULL;
static PyObject *MuteHandler = NULL;
static IMMDevice *defaultDevice = NULL;
static IMMDevice *selectedDevice = NULL;
static IMMDeviceCollection *deviceList = NULL;
static IMMDeviceEnumerator *deviceEnumerator = NULL;
static IAudioEndpointVolume *defaultVolume = NULL;
static IAudioEndpointVolume *selectedVolume = NULL;
static int lastMute = FALSE;
static float lastVolume = 0;

int Volume_Event(void* args) {
  PyObject *pres;
  PyObject *arguments = (PyObject*)args;
  pres = PyEval_CallObject(VolumeHandler, arguments);
  Py_XDECREF(arguments);
  Py_DECREF(pres);
  return 0;
}

int Mute_Event(void* args) {
  PyObject *pres;
  PyObject *arguments = (PyObject*)args;
  pres = PyEval_CallObject(MuteHandler, arguments);
  Py_XDECREF(arguments);
  Py_DECREF(pres);
  return 0;
}

class CAudioEndpointVolumeCallback : public IAudioEndpointVolumeCallback {
  LONG _cRef;

public:
  CAudioEndpointVolumeCallback() :
    _cRef(1) {
  }

  ~CAudioEndpointVolumeCallback() {
  }

  // IUnknown methods -- AddRef, Release, and QueryInterface

  ULONG STDMETHODCALLTYPE AddRef() {
    return InterlockedIncrement(&_cRef);
  }

  ULONG STDMETHODCALLTYPE Release() {
    ULONG ulRef = InterlockedDecrement(&_cRef);
    if (0 == ulRef) {
      delete this;
    }
    return ulRef;

  }

  HRESULT STDMETHODCALLTYPE QueryInterface(REFIID riid, VOID **ppvInterface) {
    if (IID_IUnknown == riid) {
      AddRef();
      *ppvInterface = (IUnknown*)this;
    } else if (__uuidof(IAudioEndpointVolumeCallback) == riid) {
      AddRef();
      *ppvInterface = (IAudioEndpointVolumeCallback*)this;
    } else {
      *ppvInterface = NULL;
      return E_NOINTERFACE;
    }
    return S_OK;
  }

  // Callback method for endpoint-volume-change notifications.

  HRESULT STDMETHODCALLTYPE OnNotify(PAUDIO_VOLUME_NOTIFICATION_DATA pNotify) {
    HRESULT skipCOM;
    if (pNotify == NULL) {
      return E_INVALIDARG;
    }
    skipCOM = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
    HRESULT hr;
    int iMute;
    float fVolume;
    PyObject *args;

    hr = defaultVolume->GetMasterVolumeLevelScalar(&fVolume);
    EXIT_ON_ERROR(hr);
    hr = defaultVolume->GetMute(&iMute);
    EXIT_ON_ERROR(hr);

    if (iMute != lastMute) {
      PyGILState_STATE state = PyGILState_Ensure();
      char str[7] = "";
      sprintf_s(str, "%3.2f", fVolume * 100);
      args = Py_BuildValue("(is)", iMute, str);
      Mute_Event(args);
      Py_XDECREF(args);
      PyGILState_Release(state);
      lastMute = iMute;
      lastVolume = fVolume;
    } else {
      if (fabs(lastVolume - fVolume) >= 0.000099) {
        PyGILState_STATE state = PyGILState_Ensure();
        char str[7] = "";
        sprintf_s(str, "%3.2f", fVolume * 100);
        args = Py_BuildValue("(is)", iMute, str);
        Volume_Event(args);
        Py_XDECREF(args);
        PyGILState_Release(state);
        lastVolume = fVolume;
      }
    }
  Exit:
    if (skipCOM == S_OK) {
      CoUninitialize();
    }
    return S_OK;
  }
};

static CAudioEndpointVolumeCallback EPVolEvents;

class CMMNotificationClient : public IMMNotificationClient {
  LONG _cRef;
  IMMDeviceEnumerator *_pEnumerator;

public:
  CMMNotificationClient() :
    _cRef(1),
    _pEnumerator(NULL) {
  }

  ~CMMNotificationClient() {
    SAFE_RELEASE(_pEnumerator)
  }

  // IUnknown methods -- AddRef, Release, and QueryInterface

  ULONG STDMETHODCALLTYPE AddRef() {
    return InterlockedIncrement(&_cRef);
  }

  ULONG STDMETHODCALLTYPE Release() {
    ULONG ulRef = InterlockedDecrement(&_cRef);
    if (0 == ulRef) {
      delete this;
    }
    return ulRef;
  }

  HRESULT STDMETHODCALLTYPE QueryInterface(
    REFIID riid, VOID **ppvInterface) {
    if (IID_IUnknown == riid) {
      AddRef();
      *ppvInterface = (IUnknown*)this;
    } else if (__uuidof(IMMNotificationClient) == riid) {
      AddRef();
      *ppvInterface = (IMMNotificationClient*)this;
    } else {
      *ppvInterface = NULL;
      return E_NOINTERFACE;
    }
    return S_OK;
  }

  // Callback methods for device-event notifications.

  HRESULT STDMETHODCALLTYPE OnDefaultDeviceChanged(
    EDataFlow flow, ERole role,
    LPCWSTR pwstrDeviceId) {
    HRESULT hr, skipCOM;
    int iMute;
    float fVolume;
    PyObject *args;

    if (defaultVolume == NULL) return S_OK;

    if (flow == eRender && role == eConsole) {
      skipCOM = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
      hr = defaultVolume->UnregisterControlChangeNotify((IAudioEndpointVolumeCallback*)&EPVolEvents);
      hr = deviceEnumerator->GetDefaultAudioEndpoint(eRender, eConsole, &defaultDevice);
      EXIT_ON_ERROR(hr);
      hr = defaultDevice->Activate(__uuidof(IAudioEndpointVolume), CLSCTX_INPROC_SERVER, NULL, (LPVOID *)&defaultVolume);
      EXIT_ON_ERROR(hr);
      hr = defaultVolume->RegisterControlChangeNotify((IAudioEndpointVolumeCallback*)&EPVolEvents);
      EXIT_ON_ERROR(hr);

      hr = defaultVolume->GetMute(&iMute);
      EXIT_ON_ERROR(hr);
      hr = defaultVolume->GetMasterVolumeLevelScalar(&fVolume);
      EXIT_ON_ERROR(hr);

      if (iMute != lastMute) {
        PyGILState_STATE state = PyGILState_Ensure();
        char str[7] = "";
        sprintf_s(str, "%3.2f", fVolume * 100);
        args = Py_BuildValue("(is)", iMute, str);
        Mute_Event(args);
        Py_XDECREF(args);
        PyGILState_Release(state);
        lastMute = iMute;
        lastVolume = fVolume;
      } else {
        if (fabs(lastVolume - fVolume) >= 0.000099) {
          PyGILState_STATE state = PyGILState_Ensure();
          char str[7] = "";
          sprintf_s(str, "%3.2f", fVolume * 100);
          args = Py_BuildValue("(is)", iMute, str);
          Volume_Event(args);
          Py_XDECREF(args);
          PyGILState_Release(state);
          lastVolume = fVolume;
        }
      }
    Exit:
      if (skipCOM == S_OK) {
        CoUninitialize();
      }
    }
    return S_OK;
  }

  HRESULT STDMETHODCALLTYPE OnDeviceAdded(LPCWSTR pwstrDeviceId) {
    return S_OK;
  };

  HRESULT STDMETHODCALLTYPE OnDeviceRemoved(LPCWSTR pwstrDeviceId) {
    return S_OK;
  }

  HRESULT STDMETHODCALLTYPE OnDeviceStateChanged(
    LPCWSTR pwstrDeviceId,
    DWORD dwNewState) {
    return S_OK;
  }

  HRESULT STDMETHODCALLTYPE OnPropertyValueChanged(
    LPCWSTR pwstrDeviceId,
    const PROPERTYKEY key) {
    return S_OK;
  }
};

static CMMNotificationClient EPDevEvents;

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
  switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
      break;
    case DLL_THREAD_ATTACH:
      break;
    case DLL_THREAD_DETACH:
      break;
    case DLL_PROCESS_DETACH:
      if (defaultVolume != NULL) defaultVolume->UnregisterControlChangeNotify((IAudioEndpointVolumeCallback*)&EPVolEvents);
      if (deviceEnumerator != NULL) deviceEnumerator->UnregisterEndpointNotificationCallback((IMMNotificationClient*)&EPDevEvents);
      SAFE_RELEASE(defaultVolume);
      SAFE_RELEASE(defaultDevice);
      SAFE_RELEASE(deviceEnumerator);
      break;
  }
  return TRUE;
}

void SelectDevice(char *deviceId) {
  HRESULT hr;
  UINT count = 0;

  deviceList = NULL;
  selectedDevice = NULL;
  selectedVolume = NULL;

  hr = deviceEnumerator->EnumAudioEndpoints(eAll, DEVICE_STATE_ACTIVE, &deviceList);
  hr = deviceList->GetCount(&count);

  for (int i = 0; i < (int)count; i++) {
    hr = deviceList->Item(i, &selectedDevice);
    IPropertyStore *pProps = NULL;
    hr = selectedDevice->OpenPropertyStore(STGM_READ, &pProps);
    PROPVARIANT varName;
    PropVariantInit(&varName);
    hr = pProps->GetValue(PKEY_Device_FriendlyName, &varName);
    char buffer[256];
    wcstombs(buffer, varName.pwszVal, 256);
    if (strncmp(buffer, deviceId, sizeof(deviceId)) == 0) {
      hr = selectedDevice->Activate(__uuidof(IAudioEndpointVolume), CLSCTX_INPROC_SERVER, NULL, (LPVOID *)&selectedVolume);
      break;
    }
  }
}

static PyObject *Get_MasterVolume(PyObject *self, PyObject *args) {
  HRESULT hr;
  char *deviceId;
  float fVolume;
  PyArg_Parse(args, "s", &deviceId);
  SelectDevice(deviceId);
  if (selectedVolume == NULL) return Py_None;

  hr = selectedVolume->GetMasterVolumeLevelScalar(&fVolume);
  return Py_BuildValue("f", (float)fVolume);
}

static PyObject *Set_MasterVolume(PyObject *self, PyObject *args) {
  HRESULT hr;
  char *deviceId;
  float fVolume = 0;
  PyArg_ParseTuple(args, "fs", &fVolume, &deviceId);
  SelectDevice(deviceId);
  if (selectedVolume == NULL) return Py_None;

  hr = selectedVolume->SetMasterVolumeLevelScalar((float)(fVolume), NULL);
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *Get_Mute(PyObject *self, PyObject *args) {
  HRESULT hr;
  char *deviceId;
  int iMute;
  PyArg_Parse(args, "s", &deviceId);
  SelectDevice(deviceId);
  if (selectedVolume == NULL) return Py_None;

  hr = selectedVolume->GetMute(&iMute);
  return Py_BuildValue("i", iMute);
}

static PyObject *Set_Mute(PyObject *self, PyObject *args) {
  HRESULT hr;
  char *deviceId;
  int iMute = 0;
  PyArg_ParseTuple(args, "is", &iMute, &deviceId);
  SelectDevice(deviceId);
  if (selectedVolume == NULL) return Py_None;

  hr = selectedVolume->SetMute(iMute, NULL);
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *Register_Volume_Handler(PyObject *self, PyObject *args) {
  Py_XDECREF(VolumeHandler);
  PyArg_Parse(args, "O", &VolumeHandler);
  Py_INCREF(VolumeHandler);
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *Register_Mute_Handler(PyObject *self, PyObject *args) {
  Py_XDECREF(MuteHandler);
  PyArg_Parse(args, "O", &MuteHandler);
  Py_INCREF(MuteHandler);
  Py_INCREF(Py_None);
  return Py_None;
}

static struct PyMethodDef VistaVolEvents_methods[] = {
    {"RegisterVolumeHandler", Register_Volume_Handler},
    {"RegisterMuteHandler",   Register_Mute_Handler},
    {"GetMute",               Get_Mute},
    {"SetMute",               Set_Mute},
    {"GetMasterVolume",       Get_MasterVolume},
    {"SetMasterVolume",       Set_MasterVolume},
    {NULL, NULL}
};

void initVistaVolEvents() {
  HRESULT hr, skipCOM;
  int iMute;
  float fVolume;
  skipCOM = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
  (void)Py_InitModule("VistaVolEvents", VistaVolEvents_methods);
  hr = CoCreateInstance(__uuidof(MMDeviceEnumerator), NULL, CLSCTX_INPROC_SERVER, __uuidof(IMMDeviceEnumerator), (LPVOID *)&deviceEnumerator);
  EXIT_ON_ERROR(hr);
  hr = deviceEnumerator->RegisterEndpointNotificationCallback((IMMNotificationClient*)&EPDevEvents);
  EXIT_ON_ERROR(hr);

  hr = deviceEnumerator->GetDefaultAudioEndpoint(eRender, eConsole, &defaultDevice);
  EXIT_ON_ERROR(hr);
  hr = defaultDevice->Activate(__uuidof(IAudioEndpointVolume), CLSCTX_INPROC_SERVER, NULL, (LPVOID *)&defaultVolume);
  EXIT_ON_ERROR(hr);
  hr = defaultVolume->RegisterControlChangeNotify((IAudioEndpointVolumeCallback*)&EPVolEvents);
  EXIT_ON_ERROR(hr);
  hr = defaultVolume->GetMute(&iMute);
  if (!FAILED(hr)) {
    lastMute = iMute;
  }
  hr = defaultVolume->GetMasterVolumeLevelScalar(&fVolume);
  if (!FAILED(hr)) {
    lastVolume = fVolume;
  }
Exit:
  if (skipCOM == S_OK) {
    CoUninitialize();
  }
}

// VistaVolume.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdio.h>
#include <windows.h>
#include <mmdeviceapi.h>
#include <endpointvolume.h>

IAudioEndpointVolume * GetEndpointVolume() {
  HRESULT hr;
  IMMDeviceEnumerator *deviceEnumerator = NULL;
  hr = CoCreateInstance(__uuidof(MMDeviceEnumerator), NULL, CLSCTX_INPROC_SERVER, __uuidof(IMMDeviceEnumerator), (LPVOID *)&deviceEnumerator);
  IMMDevice *defaultDevice = NULL;

  hr = deviceEnumerator->GetDefaultAudioEndpoint(eRender, eConsole, &defaultDevice);
  deviceEnumerator->Release();
  deviceEnumerator = NULL;

  IAudioEndpointVolume *endpointVolume = NULL;
  hr = defaultDevice->Activate(__uuidof(IAudioEndpointVolume), CLSCTX_INPROC_SERVER, NULL, (LPVOID *)&endpointVolume);
  defaultDevice->Release();
  defaultDevice = NULL;
  return endpointVolume;
}

float GetMasterVolume() {
  HRESULT hr;
  CoInitialize(NULL);
  IAudioEndpointVolume *endpointVolume = GetEndpointVolume();
  float currentVolume = 0;
  hr = endpointVolume->GetMasterVolumeLevelScalar(&currentVolume);
  endpointVolume->Release();
  CoUninitialize();
  return currentVolume;
}

bool SetMasterVolume(float level) {
  HRESULT hr;
  CoInitialize(NULL);
  IAudioEndpointVolume *endpointVolume = GetEndpointVolume();
  hr = endpointVolume->SetMasterVolumeLevelScalar((float)(level), NULL);
  endpointVolume->Release();
  CoUninitialize();
  return 0;
}

bool GetMute() {
  HRESULT hr;
  CoInitialize(NULL);
  IAudioEndpointVolume *endpointVolume = GetEndpointVolume();
  BOOL currentMute = false;
  hr = endpointVolume->GetMute(&currentMute);
  endpointVolume->Release();
  CoUninitialize();
  return (bool)currentMute;
}

bool SetMute(bool mute) {
  HRESULT hr;
  CoInitialize(NULL);
  IAudioEndpointVolume *endpointVolume = GetEndpointVolume();
  hr = endpointVolume->SetMute((bool)(mute), NULL);
  endpointVolume->Release();
  CoUninitialize();
  return 0;
}

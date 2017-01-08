# -*- coding: utf-8 -*-

from ctypes import HRESULT as _HRESULT
from ctypes.wintypes import (
    DWORD as _DWORD,
    LPCWSTR as _PCWSTR,
)

from comtypes import (
    COMMETHOD as _COMMETHOD,
    GUID as _GUID,
    IUnknown as _IUnknown,
    STDMETHOD as _STDMETHOD,
)

CLSID_CPolicyConfigVistaClient = _GUID(
    '{294935CE-F637-4E7C-A41B-AB255460B862}')
IID_IPolicyConfigVista = _GUID('{568b9108-44bf-40b4-9006-86afe5b5a620}')


class IPolicyConfigVista(_IUnknown):
    _iid_ = IID_IPolicyConfigVista
    _methods_ = (
        _STDMETHOD(_HRESULT, 'GetMixFormat', []),
        _STDMETHOD(_HRESULT, 'GetDeviceFormat', []),
        _STDMETHOD(_HRESULT, 'SetDeviceFormat', []),
        _STDMETHOD(_HRESULT, 'GetProcessingPeriod', []),
        _STDMETHOD(_HRESULT, 'SetProcessingPeriod', []),
        _STDMETHOD(_HRESULT, 'GetShareMode', []),
        _STDMETHOD(_HRESULT, 'SetShareMode', []),
        _STDMETHOD(_HRESULT, 'GetPropertyValue', []),
        _STDMETHOD(_HRESULT, 'SetPropertyValue', []),
        _COMMETHOD(
            [], _HRESULT,
            'SetDefaultEndpoint',
            (['in'], _PCWSTR, 'wszDeviceId'),
            (['in'], _DWORD, 'eRole')
        ),
        _STDMETHOD(_HRESULT, 'SetEndpointVisibility', [])
    )

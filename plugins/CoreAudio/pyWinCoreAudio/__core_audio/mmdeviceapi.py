# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import ctypes
import comtypes
from comtypes import CoClass
from propertystore import PROPERTYKEY, PIPropertyStore, PPROPVARIANT
from enum import (
    ERole,
    EDataFlow,
    PEDataFlow
)

from iid import (
    IID_IMMDevice,
    IID_IMMDeviceCollection,
    IID_IMMDeviceEnumerator,
    IID_IMMNotificationClient,
    IID_IMMEndpoint,
    IID_IMMDeviceActivator,
    CLSID_MMDeviceEnumerator,
    IID_MMDeviceAPILib,
    IID_IActivateAudioInterfaceAsyncOperation,
    IID_IActivateAudioInterfaceCompletionHandler
)
from ctypes.wintypes import (
    UINT,
    LPARAM,
    DWORD,
    LPWSTR,
    LPCWSTR,
    LPVOID
)


COMMETHOD = comtypes.COMMETHOD
GUID = comtypes.GUID
CLSCTX_INPROC_SERVER = comtypes.CLSCTX_INPROC_SERVER
HRESULT = ctypes.HRESULT
POINTER = ctypes.POINTER
REFIID = POINTER(GUID)
LPDWORD = POINTER(DWORD)
UINT_PTR = POINTER(UINT)
LPHRESULT = POINTER(HRESULT)
PIUnknown = POINTER(comtypes.IUnknown)


class IMMNotificationClient(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IMMNotificationClient
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'OnDeviceStateChanged',
            (['in'], LPCWSTR, 'pwstrDeviceId'),
            (['in'], DWORD, 'dwNewState'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnDeviceAdded',
            (['in'], LPCWSTR, 'pwstrDeviceId')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnDeviceRemoved',
            (['in'], LPCWSTR, 'pwstrDeviceId')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnDefaultDeviceChanged',
            (['in'], EDataFlow, 'flow'),
            (['in'], ERole, 'role'),
            (['in'], LPCWSTR, 'pwstrDefaultDeviceId')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnPropertyValueChanged',
            (['in'], LPCWSTR, 'pwstrDeviceId'),
            (['in'], PROPERTYKEY, 'key')
        )
    )


PIMMNotificationClient = POINTER(IMMNotificationClient)


class IActivateAudioInterfaceAsyncOperation(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IActivateAudioInterfaceAsyncOperation
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetActivateResult',
            (['out'], LPHRESULT, 'activateResult'),
            (['out'], POINTER(PIUnknown), 'activatedInterface'),
        ),
    )


PIActivateAudioInterfaceAsyncOperation = POINTER(
    IActivateAudioInterfaceAsyncOperation
)


class IActivateAudioInterfaceCompletionHandler(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IActivateAudioInterfaceCompletionHandler
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'ActivateCompleted',
            (
                ['in'],
                PIActivateAudioInterfaceAsyncOperation,
                'activateOperation'
            ),
        ),
    )


PIActivateAudioInterfaceCompletionHandler = POINTER(
    IActivateAudioInterfaceCompletionHandler
)


class IMMEndpoint(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IMMEndpoint
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetDataFlow',
            (['out'], PEDataFlow, 'pDataFlow')
        ),
    )


PIMMEndpoint = POINTER(IMMEndpoint)


class IMMDevice(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IMMDevice
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'Activate',
            (['in'], REFIID, 'iid'),
            (['in'], DWORD, 'dwClsCtx'),
            (['in'], PPROPVARIANT, 'pActivationParams', None),
            (['out'], POINTER(LPVOID), 'ppInterface')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OpenPropertyStore',
            (['in'], DWORD, 'stgmAccess'),
            (['out'], POINTER(PIPropertyStore), 'ppProperties'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetId',
            (['out'], POINTER(LPWSTR), 'ppstrId')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetState',
            (['out'], LPDWORD, 'pdwState')
        )
    )


PIMMDevice = POINTER(IMMDevice)


class IMMDeviceActivator(comtypes.IUnknown):
    _iid_ = IID_IMMDeviceActivator
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'Activate',
            (['in'], REFIID, 'iid'),
            (['in'], PIMMDevice, 'pDevice'),
            (['in'], PPROPVARIANT, 'pActivationParams'),
            (['out'], POINTER(LPVOID), 'ppInterface'),
        ),
    )


PIMMDeviceActivator = POINTER(IMMDeviceActivator)


class IMMDeviceCollection(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IMMDeviceCollection
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetCount',
            (['out'], UINT_PTR, 'pcDevices')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Item',
            (['in'], UINT, 'nDevice'),
            (['out'], POINTER(PIMMDevice), 'ppDevice')
        )
    )


PIMMDeviceCollection = ctypes.POINTER(IMMDeviceCollection)


class IMMDeviceEnumerator(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IMMDeviceEnumerator
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'EnumAudioEndpoints',
            (['in'], DWORD, 'dataFlow'),
            (['in'], DWORD, 'dwStateMask'),
            (['out'], POINTER(PIMMDeviceCollection), 'ppDevices')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetDefaultAudioEndpoint',
            (['in'], DWORD, 'dataFlow'),
            (['in'], DWORD, 'role'),
            (['out'], POINTER(PIMMDevice), 'ppDevices')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetDevice',
            (['in'], LPCWSTR, 'pwstrId'),
            (['out'], POINTER(PIMMDevice), 'ppDevices')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'RegisterEndpointNotificationCallback',
            (['in'], PIMMNotificationClient, 'pClient'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'UnregisterEndpointNotificationCallback',
            (['in'], PIMMNotificationClient, 'pClient'),
        )
    )

    @classmethod
    def get_default(cls, dataFlow, role):
        enumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator, cls, CLSCTX_INPROC_SERVER)
        return enumerator.GetDefaultAudioEndpoint(dataFlow, role)


class MMDeviceAPILib(object):
    name = u'MMDeviceAPILib'
    _reg_typelib_ = (IID_MMDeviceAPILib, 1, 0)


class MMDeviceEnumerator(CoClass):
    _reg_clsid_ = CLSID_MMDeviceEnumerator
    _idlflags_ = []
    _reg_typelib_ = (IID_MMDeviceAPILib, 1, 0)
    _com_interfaces_ = [IMMDeviceEnumerator]


class AudioExtensionParams(ctypes.Structure):
    _fields_ = [
        ('AddPageParam', LPARAM),
        ('pEndpoint', PIMMDevice),
        ('pEndpoint', PIMMDevice),
        ('pPnpInterface', PIMMDevice),
        ('pPnpDevnode', PIMMDevice)
    ]

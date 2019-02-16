# -*- coding: utf-8 -*-
# TODO: Missing module docstring (missing-docstring)

from __future__ import print_function, unicode_literals, absolute_import

from ctypes import (
    POINTER as _POINTER,
    HRESULT as _HRESULT,
    c_float as _c_float,
    Structure
)
from ctypes.wintypes import (
    BOOL as _BOOL,
    DWORD as _DWORD,
    UINT as _UINT,
)
from comtypes import (
    GUID as _GUID,
    IUnknown as _IUnknown,
    COMMETHOD as _COMMETHOD,
)


class AUDIO_VOLUME_NOTIFICATION_DATA(Structure):
    # TODO: Missing class docstring (missing-docstring)
    pass


AUDIO_VOLUME_NOTIFICATION_DATA._fields_ = [
    ('guidEventContext', _GUID),
    ('bMuted', _BOOL),
    ('fMasterVolume', _c_float),
    ('nChannels', _UINT),
    ('afChannelVolumes', (_c_float * 1)),
]
PAUDIO_VOLUME_NOTIFICATION_DATA = _POINTER(AUDIO_VOLUME_NOTIFICATION_DATA)

IID_IAudioEndpointVolumeCallback = _GUID(
    '{657804FA-D6AD-4496-8A60-352752AF4F89}'
)


class IAudioEndpointVolumeCallback(_IUnknown):
    # TODO: Missing class docstring (missing-docstring)
    _iid_ = IID_IAudioEndpointVolumeCallback
    _methods_ = [
        _COMMETHOD(
            [],
            _HRESULT,
            'OnNotify',
            (['in'], PAUDIO_VOLUME_NOTIFICATION_DATA, 'pNotify')
        ),
    ]


IID_IAudioEndpointVolume = _GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')


class IAudioEndpointVolume(_IUnknown):
    # TODO: Missing class docstring (missing-docstring)
    _iid_ = _GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
    _methods_ = [
        _COMMETHOD(
            [], _HRESULT, 'RegisterControlChangeNotify',
            (['in'], _POINTER(IAudioEndpointVolumeCallback), 'pNotify')
        ),
        _COMMETHOD(
            [], _HRESULT, 'UnregisterControlChangeNotify',
            (['in'], _POINTER(IAudioEndpointVolumeCallback), 'pNotify')
        ),
        _COMMETHOD(
            [], _HRESULT, 'GetChannelCount',
            (['out', 'retval'], _POINTER(_UINT), 'pnChannelCount'),
        ),
        _COMMETHOD(
            [], _HRESULT, 'SetMasterVolumeLevel',
            (['in'], _c_float, 'fLevelDB'),
            (['in'], _POINTER(_GUID), 'pguidEventContext')
        ),
        _COMMETHOD(
            [], _HRESULT, 'SetMasterVolumeLevelScalar',
            (['in'], _c_float, 'fLevelDB'),
            (['in'], _POINTER(_GUID), 'pguidEventContext')
        ),
        _COMMETHOD(
            [], _HRESULT, 'GetMasterVolumeLevel',
            (['out', 'retval'], _POINTER(_c_float), 'pfLevelDB')
        ),
        _COMMETHOD(
            [], _HRESULT, 'GetMasterVolumeLevelScalar',
            (['out', 'retval'], _POINTER(_c_float), 'pfLevelDB')
        ),
        _COMMETHOD(
            [], _HRESULT, 'SetChannelVolumeLevel',
            (['in'], _UINT, 'nChannel'),
            (['in'], _c_float, 'fLevelDB'),
            (['in'], _POINTER(_GUID), 'pguidEventContext')
        ),
        _COMMETHOD(
            [], _HRESULT, 'SetChannelVolumeLevelScalar',
            (['in'], _UINT, 'nChannel'),
            (['in'], _c_float, 'fLevelDB'),
            (['in'], _POINTER(_GUID), 'pguidEventContext')
        ),
        _COMMETHOD(
            [], _HRESULT, 'GetChannelVolumeLevel',
            (['in'], _UINT, 'nChannel'),
            (['out', 'retval'], _POINTER(_c_float), 'pfLevelDB')
        ),
        _COMMETHOD(
            [], _HRESULT, 'GetChannelVolumeLevelScalar',
            (['in'], _UINT, 'nChannel'),
            (['out', 'retval'], _POINTER(_c_float), 'pfLevelDB')
        ),
        _COMMETHOD(
            [], _HRESULT, 'SetMute',
            (['in'], _BOOL, 'bMute'),
            (['in'], _POINTER(_GUID), 'pguidEventContext')
        ),
        _COMMETHOD(
            [], _HRESULT, 'GetMute',
            (['out', 'retval'], _POINTER(_BOOL), 'pbMute')
        ),
        _COMMETHOD(
            [], _HRESULT, 'GetVolumeStepInfo',
            (['out', 'retval'], _POINTER(_UINT), 'pnStep'),
            (['out', 'retval'], _POINTER(_UINT), 'pnStepCount'),
        ),
        _COMMETHOD(
            [], _HRESULT, 'VolumeStepUp',
            (['in'], _POINTER(_GUID), 'pguidEventContext')
        ),
        _COMMETHOD(
            [], _HRESULT, 'VolumeStepDown',
            (['in'], _POINTER(_GUID), 'pguidEventContext')
        ),
        _COMMETHOD(
            [], _HRESULT, 'QueryHardwareSupport',
            (['out', 'retval'], _POINTER(_DWORD), 'pdwHardwareSupportMask')
        ),
        _COMMETHOD(
            [], _HRESULT, 'GetVolumeRange',
            (['out', 'retval'], _POINTER(_c_float), 'pfLevelMinDB'),
            (['out', 'retval'], _POINTER(_c_float), 'pfLevelMaxDB'),
            (['out', 'retval'], _POINTER(_c_float), 'pfVolumeIncrementDB')
        ),
    ]

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
from enum import PAudioSessionState
from audioclient import PISimpleAudioVolume
from iid import (
    IID_IAudioSessionEvents,
    IID_IAudioSessionControl,
    IID_IAudioSessionControl2,
    IID_IAudioSessionManager,
    IID_IAudioSessionManager2,
    IID_IAudioSessionNotification,
    IID_IAudioVolumeDuckNotification,
    IID_IAudioSessionEnumerator,
)
from ctypes.wintypes import (
    FLOAT,
    INT,
    DWORD,
    BOOL,
    LPWSTR,
    LPCWSTR,
    WCHAR,
)


COMMETHOD = comtypes.COMMETHOD
GUID = comtypes.GUID
UINT32 = ctypes.c_uint32
HRESULT = ctypes.HRESULT
POINTER = ctypes.POINTER
LPWCHAR = POINTER(WCHAR)
LPCGUID = POINTER(comtypes.GUID)
LPDWORD = POINTER(DWORD)
LPINT = POINTER(INT)


class IAudioSessionEvents(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioSessionEvents
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'OnDisplayNameChanged',
            (['in'], LPCWSTR, 'NewDisplayName'),
            (['in'], LPCGUID, 'EventContext'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnIconPathChanged',
            (['in'], LPWCHAR, 'NewIconPath'),
            (['in'], LPCGUID, 'EventContext'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnSimpleVolumeChanged',
            (['in'], FLOAT, 'NewVolume'),
            (['in'], BOOL, 'NewMute'),
            (['in'], LPCGUID, 'EventContext'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnChannelVolumeChanged',
            (['in'], DWORD, 'ChannelCount'),
            (['in'], (FLOAT * 8), 'NewChannelVolumeArray'),
            (['in'], DWORD, 'ChangedChannel'),
            (['in'], LPCGUID, 'EventContext'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnGroupingParamChanged',
            (['in'], LPCGUID, 'NewGroupingParam'),
            (['in'], LPCGUID, 'EventContext'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnStateChanged',
            (['in'], DWORD, 'DisconnectReason'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnSessionDisconnected',
            (['in'], DWORD, 'DisconnectReason'),
        )
    )


PIAudioSessionEvents = POINTER(IAudioSessionEvents)


class IAudioSessionControl(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioSessionControl
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetState',
            (['out'], PAudioSessionState, 'pRetVal')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetDisplayName',
            (['out'], POINTER(LPWSTR), 'pRetVal')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetDisplayName',
            (['in'], LPCWSTR, 'Value'),
            (['in', 'unique'], LPCGUID, 'EventContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetIconPath',
            (['out'], POINTER(LPCWSTR), 'pRetVal')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetIconPath',
            (['in'], LPCWSTR, 'Value'),
            (['in'], LPCGUID, 'EventContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetGroupingParam',
            (['out'], POINTER(GUID), 'pRetVal')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetGroupingParam',
            (['in'], LPCGUID, 'Override'),
            (['in'], LPCGUID, 'EventContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'RegisterAudioSessionNotification',
            (['in'], PIAudioSessionEvents, 'NewNotifications')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'UnregisterAudioSessionNotification',
            (['in'], PIAudioSessionEvents, 'NewNotifications')
        )
    )


PIAudioSessionControl = POINTER(IAudioSessionControl)


class IAudioSessionNotification(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioSessionNotification
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'OnSessionCreated',
            (['in'], PIAudioSessionControl, 'NewSession')
        ),
    )


PIAudioSessionNotification = POINTER(IAudioSessionNotification)


class IAudioSessionEnumerator(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioSessionEnumerator
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetCount',
            (['out'], LPINT, 'SessionCount')
        ),

        COMMETHOD(
            [],
            HRESULT,
            'GetSession',
            (['in'], INT, 'SessionCount'),
            (['out'], POINTER(PIAudioSessionControl), 'Session')
        )
    )


PIAudioSessionEnumerator = POINTER(IAudioSessionEnumerator)


class IAudioSessionControl2(IAudioSessionControl):
    _case_insensitive_ = True
    _iid_ = IID_IAudioSessionControl2
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetSessionIdentifier',
            (['out'], POINTER(LPCWSTR), 'pRetVal')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetSessionInstanceIdentifier',
            (['out'], POINTER(LPCWSTR), 'pRetVal')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetProcessId',
            (['out'], POINTER(DWORD), 'pRetVal')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'IsSystemSoundsSession'
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetDuckingPreferences',
            (['in'], BOOL, 'optOut')
        )
    )


PIAudioSessionControl2 = POINTER(IAudioSessionControl2)


class IAudioSessionManager(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioSessionManager
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetAudioSessionControl',
            (['in'], LPCGUID, 'AudioSessionGuid'),
            (['in'], DWORD, 'StreamFlags'),
            (
                ['out'],
                POINTER(PIAudioSessionControl),
                'SessionControl'
            )
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetSimpleAudioVolume',
            (['in'], LPCGUID, 'AudioSessionGuid'),
            (['in'], DWORD, 'CrossProcessSession'),
            (['out'], POINTER(PISimpleAudioVolume), 'AudioVolume')
        )

    )


PIAudioSessionManager = POINTER(IAudioSessionManager)


class IAudioVolumeDuckNotification(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioVolumeDuckNotification
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'OnVolumeDuckNotification',
            (['in'], LPCWSTR, 'sessionID'),
            (['in'], UINT32, 'countCommunicationSessions'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'OnVolumeUnduckNotification',
            (['in'], LPCWSTR, 'sessionID')
        )
    )


PIAudioVolumeDuckNotification = POINTER(IAudioVolumeDuckNotification)


class IAudioSessionManager2(IAudioSessionManager):
    _case_insensitive_ = True
    _iid_ = IID_IAudioSessionManager2
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetSessionEnumerator',
            (
                ['out', 'retval'],
                POINTER(PIAudioSessionEnumerator),
                'SessionList'
            )
        ),
        comtypes.STDMETHOD(
            HRESULT,
            'RegisterSessionNotification',
            (
                PIAudioSessionNotification,
            )
        ),
        comtypes.STDMETHOD(
            HRESULT,
            'UnregisterSessionNotification',
            (
                PIAudioSessionNotification,
            )
        ),
        COMMETHOD(
            [],
            HRESULT,
            'RegisterDuckNotification',
            (['in'], LPCWSTR, 'SessionID'),
            (['in'], PIAudioVolumeDuckNotification, 'duckNotification')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'UnregisterDuckNotification',
            (['in'], PIAudioVolumeDuckNotification, 'duckNotification')
        )
    )


PIAudioSessionManager2 = POINTER(IAudioSessionManager2)

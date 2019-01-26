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

import comtypes
import ctypes
from comtypes.automation import VARTYPE
from enum import (
    PConnectorType,
    PDataFlow,
    KSJACK_SINK_CONNECTIONTYPE,
    PPartType,
)
from ctypes.wintypes import (
    FLOAT,
    UINT,
    LONG,
    ULONG,
    DWORD,
    BOOL,
    WORD,
    COLORREF,
    LPWSTR,
    WCHAR,
    LPVOID
)
from iid import (
    IID_IAudioAutoGainControl,
    IID_IAudioBass,
    IID_IAudioMidrange,
    IID_IAudioTreble,
    IID_IAudioChannelConfig,
    IID_IAudioInputSelector,
    IID_IAudioOutputSelector,
    IID_IAudioLoudness,
    IID_IAudioMute,
    IID_IAudioPeakMeter,
    IID_IAudioVolumeLevel,
    IID_IConnector,
    IID_IControlInterface,
    IID_IDeviceSpecificProperty,
    IID_IDeviceTopology,
    IID_IKsFormatSupport,
    IID_IKsJackDescription,
    IID_IKsJackDescription2,
    IID_IKsJackSinkInformation,
    IID_IPartsList,
    IID_IPart,
    IID_IPerChannelDbLevel,
    IID_ISubunit,
    IID_IControlChangeNotify,
    CLSID_DeviceTopology,
    IID_DevTopologyLib,
)

COMMETHOD = comtypes.COMMETHOD
GUID = comtypes.GUID
UCHAR = ctypes.c_ubyte
HRESULT = ctypes.HRESULT
POINTER = ctypes.POINTER
LPCGUID = REFIID = POINTER(GUID)
LPFLOAT = POINTER(FLOAT)
LPDWORD = POINTER(DWORD)
LPUINT = POINTER(UINT)
LPBOOL = POINTER(BOOL)
LPVARTYPE = POINTER(VARTYPE)
LPLONG = POINTER(LONG)


class KSDATAFORMAT(ctypes.Structure):
    _fields_ = [
        ('FormatSize', ULONG),
        ('Flags', ULONG),
        ('SampleSize', ULONG),
        ('Reserved', ULONG),
        ('MajorFormat', GUID),
        ('SubFormat', GUID),
        ('Specifier', GUID)
    ]


PKSDATAFORMAT = POINTER(KSDATAFORMAT)


class KSJACK_DESCRIPTION(ctypes.Structure):
    _fields_ = [
        ('ChannelMapping', DWORD),
        ('Color', COLORREF),
        ('ConnectionType', DWORD),
        ('GeoLocation', DWORD),
        ('GenLocation', DWORD),
        ('PortConnection', DWORD),
        ('IsConnected', BOOL)
    ]


PKSJACK_DESCRIPTION = POINTER(KSJACK_DESCRIPTION)


class LUID(ctypes.Structure):
    _fields_ = [
        ('LowPart', DWORD),
        ('HighPart', LONG)
    ]


PLUID = POINTER(LUID)


class tagKSJACK_SINK_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('ConnType', KSJACK_SINK_CONNECTIONTYPE),
        ('ManufacturerId', WORD),
        ('ProductId', WORD),
        ('AudioLatency', WORD),
        ('HDCPCapable', BOOL),
        ('AICapable', BOOL),
        ('SinkDescriptionLength', UCHAR),
        ('SinkDescription', (WCHAR * 32)),
        ('PortId', LUID),
    ]


KSJACK_SINK_INFORMATION = tagKSJACK_SINK_INFORMATION
PKSJACK_SINK_INFORMATION = POINTER(KSJACK_SINK_INFORMATION)


class tagKSJACK_DESCRIPTION2(ctypes.Structure):
    _fields_ = [
        ('DeviceStateInfo', DWORD),
        ('JackCapabilities', DWORD)
    ]


KSJACK_DESCRIPTION2 = tagKSJACK_DESCRIPTION2
PKSJACK_DESCRIPTION2 = POINTER(KSJACK_DESCRIPTION2)


class IAudioAutoGainControl(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioAutoGainControl
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetEnabled',
            (['out'], LPBOOL, 'pbEnabled')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetEnabled',
            (['in'], BOOL, 'bEnable'),
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        )
    )


PIAudioAutoGainControl = POINTER(IAudioAutoGainControl)


class IPerChannelDbLevel(comtypes.IUnknown):
    _iid_ = IID_IPerChannelDbLevel
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelCount',
            (['out'], LPUINT, 'pcChannels')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetLevelRange',
            (['in'], UINT, 'nChannel'),
            (['out'], LPFLOAT, 'pfMinLevelDB'),
            (['out'], LPFLOAT, 'pfMaxLevelDB'),
            (['out'], LPFLOAT, 'pfStepping')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetLevel',
            (['in'], UINT, 'nChannel'),
            (['out'], LPFLOAT, 'pfLevelDB')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetLevel',
            (['in'], UINT, 'nChannel'),
            (['in'], FLOAT, 'fLevelDB'),
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetLevelUniform',
            (['in'], FLOAT, 'fLevelDB'),
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetLevelAllChannels',
            (['in'], FLOAT, 'aLevelsDB'),
            (['in'], ULONG, 'cChannels'),
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        )
    )


PIPerChannelDbLevel = POINTER(IPerChannelDbLevel)


class IAudioBass(IPerChannelDbLevel):
    _iid_ = IID_IAudioBass


PIAudioBass = POINTER(IAudioBass)


class IAudioMidrange(IPerChannelDbLevel):
    _iid_ = IID_IAudioMidrange


PIAudioMidrange = POINTER(IAudioMidrange)


class IAudioTreble(IPerChannelDbLevel):
    _iid_ = IID_IAudioTreble


PIAudioTreble = POINTER(IAudioTreble)


class IAudioVolumeLevel(IPerChannelDbLevel):
    _iid_ = IID_IAudioVolumeLevel


PIAudioVolumeLevel = POINTER(IAudioVolumeLevel)


class IAudioChannelConfig(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioChannelConfig
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetChannelConfig',
            (['in'], DWORD, 'dwConfig'),
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelConfig',
            (['out'], LPDWORD, 'pdwConfig')
        )
    )


PIAudioChannelConfig = POINTER(IAudioChannelConfig)


class IAudioInputSelector(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioInputSelector
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetSelection',
            (['out'], LPUINT, 'pnIdSelected')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetSelection',
            (['in'], UINT, 'nIdSelect'),
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        )
    )


PIAudioInputSelector = POINTER(IAudioInputSelector)


class IAudioLoudness(comtypes.IUnknown):
    _iid_ = IID_IAudioLoudness
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetEnabled',
            (['out'], LPBOOL, 'pbEnabled')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetEnabled',
            (['in'], BOOL, 'bEnabled'),
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        )
    )


PIAudioLoudness = POINTER(IAudioLoudness)


class IAudioMute(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioMute
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetMute',
            (['out'], LPBOOL, 'pbMuted')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetMute',
            (['in'], BOOL, 'bMuted'),
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        )
    )


PIAudioMute = POINTER(IAudioMute)


class IAudioOutputSelector(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioOutputSelector
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetSelection',
            (['out'], LPUINT, 'pnIdSelected')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetSelection',
            (['in'], UINT, 'nIdSelect'),
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        )
    )


PIAudioOutputSelector = POINTER(IAudioOutputSelector)


class IAudioPeakMeter(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IAudioPeakMeter
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetChannelCount',
            (['out'], LPUINT, 'pcChannels')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetLevel',
            (['in'], UINT, 'nChannel'),
            (['out'], LPFLOAT, 'pfLevel')
        )
    )


PIAudioPeakMeter = POINTER(IAudioPeakMeter)


class IConnector(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IConnector


PIConnector = POINTER(IConnector)


IConnector._methods_ = (
    COMMETHOD(
        [],
        HRESULT,
        'GetType',
        (['out'], PConnectorType, 'pType')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetDataFlow',
        (['out'], PDataFlow, 'pFlow')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'ConnectTo',
        (['in'], PIConnector, 'pConnectTo')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Disconnect'
    ),
    COMMETHOD(
        [],
        HRESULT,
        'IsConnected',
        (['out'], LPBOOL, 'pbConnected')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetConnectedTo',
        (['out'], POINTER(PIConnector), 'ppConTo')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetConnectorIdConnectedTo',
        (['out'], POINTER(LPWSTR), 'ppwstrConnectorId')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetDeviceIdConnectedTo',
        (['out'], POINTER(LPWSTR), 'ppwstrDeviceId')
    )
)


class IControlInterface(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IControlInterface
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetName',
            (['out'], POINTER(LPWSTR), 'ppwstrName')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetIID',
            (['out'], LPCGUID, 'pIID')
        )
    )


PIControlInterface = POINTER(IControlInterface)


class IDeviceSpecificProperty(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IDeviceSpecificProperty
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetDataType',
            (['out'], LPVARTYPE, 'pVType')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetValue',
            (['out'], LPVOID, 'pvValue'),
            (['in', 'out'], LPDWORD, 'pcbValue')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetValue',
            (['in'], LPVOID, 'pvValue'),
            (['in'], DWORD, 'cbValue'),
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Get4BRange',
            (['out'], LPLONG, 'plMin'),
            (['out'], LPLONG, 'plMax'),
            (['out'], LPLONG, 'plStepping')
        )
    )


PIDeviceSpecificProperty = POINTER(IDeviceSpecificProperty)


class ISubunit(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_ISubunit


PISubunit = POINTER(ISubunit)


class IPartsList(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IPartsList


PIPartsList = POINTER(IPartsList)


class IPart(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IPart


PIPart = POINTER(IPart)


class IDeviceTopology(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IDeviceTopology
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetConnectorCount',
            (['out'], LPUINT, 'pCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetConnector',
            (['in'], UINT, 'nIndex'),
            (['out'], POINTER(PIConnector), 'ppConnector')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetSubunitCount',
            (['out'], LPUINT, 'pCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetSubunit',
            (['in'], UINT, 'nIndex'),
            (['out'], POINTER(PISubunit), 'ppSubunit')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetPartById',
            (['in'], UINT, 'nId'),
            (['out'], POINTER(PIPart), 'ppPart')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetDeviceId',
            (['out'], POINTER(LPWSTR), 'ppwstrDeviceId')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetSignalPath',
            (['in'], PIPart, 'pIPartFrom'),
            (['in'], PIPart, 'pIPartTo'),
            (['in'], BOOL, 'bRejectMixedPaths'),
            (['out'], POINTER(PIPartsList), 'ppParts')
        ),
    )


PIDeviceTopology = POINTER(IDeviceTopology)


class IKsFormatSupport(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IKsFormatSupport
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'IsFormatSupported',
            (['in'], PKSDATAFORMAT, 'pKsFormat'),
            (['in'], DWORD, 'cbFormat'),
            (['out'], LPBOOL, 'pbSupported')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetDevicePreferredFormat',
            (['out'], POINTER(PKSDATAFORMAT), 'ppKsFormat')
        )
    )


PIKsFormatSupport = POINTER(IKsFormatSupport)


class IKsJackDescription(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IKsJackDescription
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetJackCount',
            (['out'], LPUINT, 'pcJacks')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetJackDescription',
            (['in'], UINT, 'nJack'),
            (['out'], PKSJACK_DESCRIPTION, 'pDescription')
        )
    )


PIKsJackDescription = POINTER(IKsJackDescription)


class IKsJackDescription2(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IKsJackDescription2
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetJackCount',
            (['out'], LPUINT, 'pcJacks')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetJackDescription2',
            (['in'], UINT, 'nJack'),
            (['out'], PKSJACK_DESCRIPTION2, 'pDescription2')
        ),
    )


PIKsJackDescription2 = POINTER(IKsJackDescription2)


class IKsJackSinkInformation(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IKsJackSinkInformation
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetJackSinkInformation',
            (['out'], PKSJACK_SINK_INFORMATION, 'pJackSinkInformation')
        ),
    )


PIKsJackSinkInformation = POINTER(IKsJackSinkInformation)


class IControlChangeNotify(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IControlChangeNotify
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'OnNotify',
            (['in'], DWORD, 'dwSenderProcessId')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetIID',
            (['in', 'unique'], LPCGUID, 'pguidEventContext')
        )
    )


PIControlChangeNotify = POINTER(IControlChangeNotify)


IPartsList._methods_ = (
    COMMETHOD(
        [],
        HRESULT,
        'GetCount',
        (['out'], LPUINT, 'pCount')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetPart',
        (['in'], UINT, 'nIndex'),
        (['out'], POINTER(PIPart), 'ppPart')
    )
)


IPart._methods_ = (
    COMMETHOD(
        [],
        HRESULT,
        'GetName',
        (['out'], POINTER(LPWSTR), 'ppwstrName')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetLocalId',
        (['out'], LPUINT, 'pnId')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetGlobalId',
        (['out'], POINTER(LPWSTR), 'ppwstrGlobalId')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetPartType',
        (['out'], PPartType, 'pPartType')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetSubType',
        (['out'], LPCGUID, 'pSubType')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetControlInterfaceCount',
        (['out'], LPUINT, 'pCount')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetControlInterface',
        (['in'], UINT, 'nIndex'),
        (['out'], POINTER(PIControlInterface), 'ppInterfaceDesc')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'EnumPartsIncoming',
        (['out'], POINTER(PIPartsList), 'ppParts')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'EnumPartsOutgoing',
        (['out'], POINTER(PIPartsList), 'ppParts')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetTopologyObject',
        (['out'], POINTER(PIDeviceTopology), 'ppTopology')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Activate',
        (['in'], DWORD, 'dwClsContext'),
        (['in'], REFIID, 'refiid'),
        (['out'], POINTER(LPVOID), 'ppvObject'),
    ),
    COMMETHOD(
        [],
        HRESULT,
        'RegisterControlChangeCallback',
        (['in'], REFIID, 'refiid'),
        (['in'], PIControlChangeNotify, 'pNotify'),
    ),
    COMMETHOD(
        [],
        HRESULT,
        'RegisterControlChangeCallback',
        (['in'], PIControlChangeNotify, 'pNotify'),
    )
)


class DevTopologyLib(object):
    name = u'DevTopologyLib'
    _reg_typelib_ = (IID_DevTopologyLib, 1, 0)

    IPartsList = IPartsList
    IAudioVolumeLevel = IAudioVolumeLevel
    IAudioLoudness = IAudioLoudness
    # IAudioSpeakerMap = IAudioSpeakerMap
    IAudioInputSelector = IAudioInputSelector
    IAudioMute = IAudioMute
    IAudioBass = IAudioBass
    IAudioMidrange = IAudioMidrange
    IAudioTreble = IAudioTreble
    IAudioAutoGainControl = IAudioAutoGainControl
    IAudioOutputSelector = IAudioOutputSelector
    IAudioPeakMeter = IAudioPeakMeter
    IDeviceSpecificProperty = IDeviceSpecificProperty
    IKsFormatSupport = IKsFormatSupport


class DeviceTopology(comtypes.CoClass):
    _reg_clsid_ = CLSID_DeviceTopology
    _idlflags_ = []
    _reg_typelib_ = (IID_DevTopologyLib, 1, 0)

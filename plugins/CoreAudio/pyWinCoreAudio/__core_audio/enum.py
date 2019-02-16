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

from ctypes import POINTER, c_int as enum


class AUDCLNT_SHAREMODE(enum):
    AUDCLNT_SHAREMODE_SHARED = 1
    AUDCLNT_SHAREMODE_EXCLUSIVE = 2


PAUDCLNT_SHAREMODE = POINTER(AUDCLNT_SHAREMODE)


class AUDIO_STREAM_CATEGORY(enum):
    AudioCategory_Other = 0
    AudioCategory_ForegroundOnlyMedia = 1
    AudioCategory_BackgroundCapableMedia = 2
    AudioCategory_Communications = 3
    AudioCategory_Alerts = 4
    AudioCategory_SoundEffects = 5
    AudioCategory_GameEffects = 6
    AudioCategory_GameMedia = 7
    AudioCategory_GameChat = 8
    AudioCategory_Speech = 9
    AudioCategory_Movie = 10
    AudioCategory_Media = 11


PAUDIO_STREAM_CATEGORY = POINTER(AUDIO_STREAM_CATEGORY)


class STGM(enum):
    STGM_READ = 0x00000000


PSTGM = POINTER(STGM)


class AUDCLNT_BUFFERFLAGS(enum):
    AUDCLNT_BUFFERFLAGS_DATA_DISCONTINUITY = 0x1
    AUDCLNT_BUFFERFLAGS_SILENT = 0x2
    AUDCLNT_BUFFERFLAGS_TIMESTAMP_ERROR = 0x4


PAUDCLNT_BUFFERFLAGS = POINTER(AUDCLNT_BUFFERFLAGS)


class AUDCLNT_STREAMOPTIONS(enum):
    AUDCLNT_STREAMOPTIONS_NONE = 0
    AUDCLNT_STREAMOPTIONS_RAW = 0x1
    AUDCLNT_STREAMOPTIONS_MATCH_FORMAT = 0x2


PAUDCLNT_STREAMOPTIONS = POINTER(AUDCLNT_STREAMOPTIONS)


class ERole(enum):
    eConsole = 0
    eMultimedia = 1
    eCommunications = 2
    ERole_enum_count = 3


class EDataFlow(enum):
    eRender = 0
    eCapture = 1
    eAll = 2
    EDataFlow_enum_count = 3


PEDataFlow = POINTER(EDataFlow)


class DataFlow(enum):
    In = 0
    Out = 1


PDataFlow = POINTER(DataFlow)


class PartType(enum):
    Connector = 0
    Subunit = 1


PPartType = POINTER(PartType)


class ConnectorType(enum):
    Unknown_Connector = 0,
    Physical_Internal = 1
    Physical_External = 2
    Software_IO = 3
    Software_Fixed = 4
    Network = 5


PConnectorType = POINTER(ConnectorType)


class EndpointFormFactor(enum):
    RemoteNetworkDevice = 0
    Speakers = 1
    LineLevel = 2
    Headphones = 3
    Microphone = 4
    Headset = 5
    Handset = 6
    UnknownDigitalPassthrough = 7
    SPDIF = 8
    DigitalAudioDisplayDevice = 9
    UnknownFormFactor = 10
    EndpointFormFactor_enum_count = 11


PEndpointFormFactor = POINTER(EndpointFormFactor)


class AudioSessionState(enum):
    AudioSessionStateInactive = 0
    AudioSessionStateActive = 1
    AudioSessionStateExpired = 2


PAudioSessionState = POINTER(AudioSessionState)


class EndpointConnectorType(enum):
    eHostProcessConnector = 0,
    eOffloadConnector = 1,
    eLoopbackConnector = 2,
    eKeywordDetectorConnector = 3,
    eConnectorCount = 4


PEndpointConnectorType = POINTER(EndpointConnectorType)

class DeviceShareMode(enum):
    DeviceShared = 0
    DeviceExclusive = 1


PDeviceShareMode = POINTER(DeviceShareMode)


class AudioDeviceState(enum):
    Active = 0x1
    Disabled = 0x2
    NotPresent = 0x4
    Unplugged = 0x8


PAudioDeviceState = POINTER(AudioDeviceState)


class EChannelMapping(enum):
    ePcxChanMap_FL_FR = 0,
    ePcxChanMap_FC_LFE = 1
    ePcxChanMap_BL_BR = 2
    ePcxChanMap_FLC_FRC = 3
    ePcxChanMap_SL_SR = 4
    ePcxChanMap_Unknown = 5


PEChannelMapping = POINTER(EChannelMapping)


class EPcxConnectionType(enum):
    eConnTypeUnknown = 0
    eConnType3Point5mm = 1
    eConnTypeEighth = 1
    eConnTypeQuarter = 2
    eConnTypeAtapiInternal = 3
    eConnTypeRCA = 4
    eConnTypeOptical = 5
    eConnTypeOtherDigital = 6
    eConnTypeOtherAnalog = 7
    eConnTypeMultichannelAnalogDIN = 8
    eConnTypeXlrProfessional = 9
    eConnTypeRJ11Modem = 10
    eConnTypeCombination = 11


PEPcxConnectionType = POINTER(EPcxConnectionType)


class EPcxGeoLocation(enum):
    eGeoLocRear = 1
    eGeoLocFront = 2
    eGeoLocLeft = 3
    eGeoLocRight = 4
    eGeoLocTop = 5
    eGeoLocBottom = 6
    eGeoLocRearPanel = 7
    eGeoLocRearOPanel = 7
    eGeoLocRiser = 8
    eGeoLocInsideMobileLid = 9
    eGeoLocDrivebay = 10
    eGeoLocHDMI = 11
    eGeoLocOutsideMobileLid = 12
    eGeoLocATAPI = 13
    eGeoLocNotApplicable = 14
    eGeoLocReserved6 = 15


PEPcxGeoLocation = POINTER(EPcxGeoLocation)


class EPcxGenLocation(enum):
    eGenLocPrimaryBox = 0
    eGenLocInternal = 1
    eGenLocSeparate = 2
    eGenLocOther = 3


PEPcxGenLocation = POINTER(EPcxGenLocation)


class EPxcPortConnection(enum):
    ePortConnJack = 0
    ePortConnIntegratedDevice = 1
    ePortConnBothIntegratedAndJack = 2
    ePortConnUnknown = 3


PEPxcPortConnection = POINTER(EPxcPortConnection)


class DisconnectReason(enum):
    DisconnectReasonDeviceRemoval = 0
    DisconnectReasonServerShutdown = 1
    DisconnectReasonFormatChanged = 2
    DisconnectReasonSessionLogoff = 3
    DisconnectReasonSessionDisconnected = 4
    DisconnectReasonExclusiveModeOverride = 5


PDisconnectReason = POINTER(DisconnectReason)


class AE_POSITION_FLAGS(enum):
    POSITION_INVALID = 0
    POSITION_DISCONTINUOUS = 1
    POSITION_CONTINUOUS = 2
    POSITION_QPC_ERROR = 4


PAE_POSITION_FLAGS = POINTER(AE_POSITION_FLAGS)


class APO_BUFFER_FLAGS(enum):
    BUFFER_INVALID = 0
    BUFFER_VALID = 1
    BUFFER_SILENT = 2


PAPO_BUFFER_FLAGS = POINTER(APO_BUFFER_FLAGS)


class AUDIO_CURVE_TYPE(enum):
    AUDIO_CURVE_TYPE_NONE = 0
    AUDIO_CURVE_TYPE_WINDOWS_FADE = 1


PAUDIO_CURVE_TYPE = POINTER(AUDIO_CURVE_TYPE)


class AudioSessionDisconnectReason(enum):
    DisconnectReasonDeviceRemoval = 0
    DisconnectReasonServerShutdown = 1
    DisconnectReasonFormatChanged = 2
    DisconnectReasonSessionLogoff = 3
    DisconnectReasonSessionDisconnected = 4
    DisconnectReasonExclusiveModeOverride = 5


PAudioSessionDisconnectReason = POINTER(AudioSessionDisconnectReason)


class KSJACK_SINK_CONNECTIONTYPE(enum):
    KSJACK_SINK_CONNECTIONTYPE_HDMI = 0
    KSJACK_SINK_CONNECTIONTYPE_DISPLAYPORT = 1


PKSJACK_SINK_CONNECTIONTYPE = POINTER(KSJACK_SINK_CONNECTIONTYPE)


class KSRESET(enum):
    KSRESET_BEGIN = 0
    KSRESET_END = 1


PKSRESET = POINTER(KSRESET)


class KSSTATE(enum):
    KSSTATE_STOP = 0
    KSSTATE_ACQUIRE = 1
    KSSTATE_PAUSE = 2
    KSSTATE_RUN = 3


PKSSTATE = POINTER(KSSTATE)


class APO_CONNECTION_BUFFER_TYPE(enum):
    APO_CONNECTION_BUFFER_TYPE_ALLOCATED = 0
    APO_CONNECTION_BUFFER_TYPE_EXTERNAL = 1
    APO_CONNECTION_BUFFER_TYPE_DEPENDANT = 2


PAPO_CONNECTION_BUFFER_TYPE = POINTER(APO_CONNECTION_BUFFER_TYPE)


class APO_FLAG(enum):
    APO_FLAG_NONE = 0x00000000
    APO_FLAG_INPLACE = 0x00000001
    APO_FLAG_SAMPLESPERFRAME_MUST_MATCH = 0x00000002
    APO_FLAG_FRAMESPERSECOND_MUST_MATCH = 0x00000004
    APO_FLAG_BITSPERSAMPLE_MUST_MATCH = 0x00000008
    APO_FLAG_MIXER = 0x00000010
    APO_FLAG_DEFAULT = (
        APO_FLAG_SAMPLESPERFRAME_MUST_MATCH |
        APO_FLAG_FRAMESPERSECOND_MUST_MATCH |
        APO_FLAG_BITSPERSAMPLE_MUST_MATCH
    )


PAPO_FLAG = POINTER(APO_FLAG)


class AUDIO_FLOW_TYPE(enum):
    AUDIO_FLOW_PULL = 0
    AUDIO_FLOW_PUSH = 1


PAUDIO_FLOW_TYPE = POINTER(AUDIO_FLOW_TYPE)


class EAudioConstriction(enum):
    eAudioConstrictionOff = 0
    eAudioConstriction48_16 = 1
    eAudioConstriction44_16 = 2
    eAudioConstriction14_14 = 3
    eAudioConstrictionMute = 4


PEAudioConstriction = POINTER(EAudioConstriction)


class SpatialAudioMetadataWriterOverflowMode(enum):
    SpatialAudioMetadataWriterOverflow_Fail = 0
    SpatialAudioMetadataWriterOverflow_MergeWithNew = 1
    SpatialAudioMetadataWriterOverflow_MergeWithLast = 2


PSpatialAudioMetadataWriterOverflowMode = POINTER(
    SpatialAudioMetadataWriterOverflowMode
)


class SpatialAudioMetadataCopyMode(enum):
    SpatialAudioMetadataCopy_Overwrite = 0
    SpatialAudioMetadataCopy_Append = 1
    SpatialAudioMetadataCopy_AppendMergeWithLast = 2
    SpatialAudioMetadataCopy_AppendMergeWithFirst = 3


PSpatialAudioMetadataCopyMode = POINTER(
    SpatialAudioMetadataCopyMode
)


class AudioObjectType(enum):
    AudioObjectType_None = 0
    AudioObjectType_Dynamic = 1 << 0
    AudioObjectType_FrontLeft = 1 << 1
    AudioObjectType_FrontRight = 1 << 2
    AudioObjectType_FrontCenter = 1 << 3
    AudioObjectType_LowFrequency = 1 << 4
    AudioObjectType_SideLeft = 1 << 5
    AudioObjectType_SideRight = 1 << 6
    AudioObjectType_BackLeft = 1 << 7
    AudioObjectType_BackRight = 1 << 8
    AudioObjectType_TopFrontLeft = 1 << 9
    AudioObjectType_TopFrontRight = 1 << 10
    AudioObjectType_TopBackLeft = 1 << 11
    AudioObjectType_TopBackRight = 1 << 12
    AudioObjectType_BottomFrontLeft = 1 << 13
    AudioObjectType_BottomFrontRight = 1 << 14
    AudioObjectType_BottomBackLeft = 1 << 15
    AudioObjectType_BottomBackRight = 1 << 16
    AudioObjectType_BackCenter = 1 << 17


PAudioObjectType = POINTER(AudioObjectType)


class SpatialAudioHrtfDirectivityType(enum):
    SpatialAudioHrtfDirectivity_OmniDirectional = 0
    SpatialAudioHrtfDirectivity_Cardioid = 1
    SpatialAudioHrtfDirectivity_Cone = 2


PSpatialAudioHrtfDirectivityType = POINTER(SpatialAudioHrtfDirectivityType)


class SpatialAudioHrtfEnvironmentType(enum):
    SpatialAudioHrtfEnvironment_Small = 0
    SpatialAudioHrtfEnvironment_Medium = 1
    SpatialAudioHrtfEnvironment_Large = 2
    SpatialAudioHrtfEnvironment_Outdoors = 3
    SpatialAudioHrtfEnvironment_Average = 4


PSpatialAudioHrtfEnvironmentType = POINTER(SpatialAudioHrtfEnvironmentType)


class SpatialAudioHrtfDistanceDecayType(enum):
    SpatialAudioHrtfDistanceDecay_NaturalDecay = 0
    SpatialAudioHrtfDistanceDecay_CustomDecay = 1


PSpatialAudioHrtfDistanceDecayType = POINTER(SpatialAudioHrtfDistanceDecayType)


class KSPROPERTY_AUDIO(enum):

    KSPROPERTY_AUDIO_LATENCY = 1
    KSPROPERTY_AUDIO_COPY_PROTECTION = 2
    KSPROPERTY_AUDIO_CHANNEL_CONFIG = 3
    KSPROPERTY_AUDIO_VOLUMELEVEL = 4
    KSPROPERTY_AUDIO_POSITION = 5
    KSPROPERTY_AUDIO_DYNAMIC_RANGE = 6
    KSPROPERTY_AUDIO_QUALITY = 7
    KSPROPERTY_AUDIO_SAMPLING_RATE = 8
    KSPROPERTY_AUDIO_DYNAMIC_SAMPLING_RATE = 9
    KSPROPERTY_AUDIO_MIX_LEVEL_TABLE = 10
    KSPROPERTY_AUDIO_MIX_LEVEL_CAPS = 11
    KSPROPERTY_AUDIO_MUX_SOURCE = 12
    KSPROPERTY_AUDIO_MUTE = 13
    KSPROPERTY_AUDIO_BASS = 14
    KSPROPERTY_AUDIO_MID = 15
    KSPROPERTY_AUDIO_TREBLE = 16
    KSPROPERTY_AUDIO_BASS_BOOST = 17
    KSPROPERTY_AUDIO_EQ_LEVEL = 18
    KSPROPERTY_AUDIO_NUM_EQ_BANDS = 19
    KSPROPERTY_AUDIO_EQ_BANDS = 20
    KSPROPERTY_AUDIO_AGC = 21
    KSPROPERTY_AUDIO_DELAY = 22
    KSPROPERTY_AUDIO_LOUDNESS = 23
    KSPROPERTY_AUDIO_WIDE_MODE = 24
    KSPROPERTY_AUDIO_WIDENESS = 25
    KSPROPERTY_AUDIO_REVERB_LEVEL = 26
    KSPROPERTY_AUDIO_CHORUS_LEVEL = 27
    KSPROPERTY_AUDIO_DEV_SPECIFIC = 28
    KSPROPERTY_AUDIO_DEMUX_DEST = 29
    KSPROPERTY_AUDIO_STEREO_ENHANCE = 30
    KSPROPERTY_AUDIO_MANUFACTURE_GUID = 32
    KSPROPERTY_AUDIO_PRODUCT_GUID = 32
    KSPROPERTY_AUDIO_CPU_RESOURCES = 33
    KSPROPERTY_AUDIO_STEREO_SPEAKER_GEOMETRY = 34
    KSPROPERTY_AUDIO_SURROUND_ENCODE = 35
    KSPROPERTY_AUDIO_3D_INTERFACE = 36
    KSPROPERTY_AUDIO_PEAKMETER = 37
    KSPROPERTY_AUDIO_ALGORITHM_INSTANCE = 38
    KSPROPERTY_AUDIO_FILTER_STATE = 39
    KSPROPERTY_AUDIO_PREFERRED_STATUS = 40
    KSPROPERTY_AUDIO_PEQ_MAX_BANDS = 41
    KSPROPERTY_AUDIO_PEQ_NUM_BANDS = 42
    KSPROPERTY_AUDIO_PEQ_BAND_CENTER_FREQ = 43
    KSPROPERTY_AUDIO_PEQ_BAND_Q_FACTOR = 44
    KSPROPERTY_AUDIO_PEQ_BAND_LEVEL = 45
    KSPROPERTY_AUDIO_CHORUS_MODULATION_RATE = 46
    KSPROPERTY_AUDIO_CHORUS_MODULATION_DEPTH = 47
    KSPROPERTY_AUDIO_REVERB_TIME = 48
    KSPROPERTY_AUDIO_REVERB_DELAY_FEEDBACK = 49
    KSPROPERTY_AUDIO_POSITIONEX = 50
    KSPROPERTY_AUDIO_MIC_ARRAY_GEOMETRY = 51
    KSPROPERTY_AUDIO_PRESENTATION_POSITION = 52
    KSPROPERTY_AUDIO_WAVERT_CURRENT_WRITE_POSITION = 53
    KSPROPERTY_AUDIO_LINEAR_BUFFER_POSITION = 54
    KSPROPERTY_AUDIO_PEAKMETER2 = 55
    KSPROPERTY_AUDIO_WAVERT_CURRENT_WRITE_LASTBUFFER_POSITION = 56
    KSPROPERTY_AUDIO_VOLUMELIMIT_ENGAGED = 57
    KSPROPERTY_AUDIO_MIC_SENSITIVITY = 58
    KSPROPERTY_AUDIO_MIC_SNR = 59



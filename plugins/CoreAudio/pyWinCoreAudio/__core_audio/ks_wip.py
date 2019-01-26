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
from comtypes import GUID, POINTER
from ctypes.wintypes import ULONG, BOOL

LONGLONG = ctypes.c_longlong


class KSPROPERTY_GENERAL(enum):
    KSPROPERTY_GENERAL_COMPONENTID = 0


class KSMETHOD_STREAMIO(enum):
    KSMETHOD_STREAMIO_READ = 0
    KSMETHOD_STREAMIO_WRITE = 1


class KSPROPERTY_MEDIASEEKING(enum):
    KSPROPERTY_MEDIASEEKING_CAPABILITIES = 0
    KSPROPERTY_MEDIASEEKING_FORMATS = 1
    KSPROPERTY_MEDIASEEKING_TIMEFORMAT = 2
    KSPROPERTY_MEDIASEEKING_POSITION = 3
    KSPROPERTY_MEDIASEEKING_STOPPOSITION = 4
    KSPROPERTY_MEDIASEEKING_POSITIONS = 5
    KSPROPERTY_MEDIASEEKING_DURATION = 6
    KSPROPERTY_MEDIASEEKING_AVAILABLE = 7
    KSPROPERTY_MEDIASEEKING_PREROLL = 8
    KSPROPERTY_MEDIASEEKING_CONVERTTIMEFORMAT = 9


class KS_SEEKING_FLAGS(enum):
    KS_SEEKING_NoPositioning = 0
    KS_SEEKING_AbsolutePositioning = 1
    KS_SEEKING_RelativePositioning = 2
    KS_SEEKING_IncrementalPositioning = 3
    KS_SEEKING_PositioningBitsMask = 0x3
    KS_SEEKING_SeekToKeyFrame = 4
    KS_SEEKING_ReturnTime = 0x8


class KS_SEEKING_CAPABILITIES(enum):
    KS_SEEKING_CanSeekAbsolute = 0x1
    KS_SEEKING_CanSeekForwards = 0x2
    KS_SEEKING_CanSeekBackwards = 0x4
    KS_SEEKING_CanGetCurrentPos = 0x8
    KS_SEEKING_CanGetStopPos = 0x10
    KS_SEEKING_CanGetDuration = 0x20
    KS_SEEKING_CanPlayBackwards = 0x40


class KSIDENTIFIER_STRUCT(ctypes.Union):
    _fields_ = [
        ('Set', GUID),
        ('Id', ULONG),
        ('Flags', ULONG)
    ]


class KSIDENTIFIER_UNION(ctypes.Union):
    _anonymous_ = 'KSIDENTIFIER_STRUCT'
    _fields_ = [
        ('KSIDENTIFIER_STRUCT', KSIDENTIFIER_STRUCT)
    ]


class KSIDENTIFIER(ctypes.Structure):
    _anonymous_ = 'KSIDENTIFIER_UNION'
    _fields_ = [
        ('KSIDENTIFIER_UNION', KSIDENTIFIER_UNION),
        ('Alignment', LONGLONG)
    ]


PKSIDENTIFIER = POINTER(KSIDENTIFIER)


class KSMETHOD(KSIDENTIFIER):
    pass


PKSMETHOD = POINTER(KSMETHOD)


class KSEVENT(KSIDENTIFIER):
    pass


PKSEVENT = POINTER(KSEVENT)


class KSPROPERTY(KSIDENTIFIER):
    pass


PKSPROPERTY = POINTER(KSPROPERTY)


class  KSP_NODE(ctypes.Structure):
    _fields_ = [
        ('Property', KSPROPERTY),
        ('NodeId', ULONG),
        ('Reserved', ULONG),
    ]


PKSP_NODE = POINTER(KSP_NODE)


class KSM_NODE(ctypes.Structure):
    _fields_ = [
        ('Method', KSMETHOD),
        ('NodeId', ULONG),
        ('Reserved', ULONG),
    ]


PKSM_NODE = POINTER(KSM_NODE)


class KSE_NODE(ctypes.Structure):
    _fields_ = [
        ('Event', KSEVENT),
        ('NodeId', ULONG),
        ('Reserved', ULONG),
    ]


PKSE_NODE = POINTER(KSE_NODE)


class KSMULTIPLE_ITEM(ctypes.Structure):
    _fields_ = [
        ('Size', ULONG),
        ('Count', ULONG),
    ]


PKSMULTIPLE_ITEM = POINTER(KSMULTIPLE_ITEM)


class KSPROPERTY_DESCRIPTION(ctypes.Structure):
    _fields_ = [
        ('AccessFlags', ULONG),
        ('DescriptionSize', ULONG),
        ('PropTypeSet', KSIDENTIFIER),
        ('MembersListCount', ULONG),
        ('Reserved', ULONG),
    ]


PKSPROPERTY_DESCRIPTION = POINTER(KSPROPERTY_DESCRIPTION)


class KSPROPERTY_MEMBERSHEADER(ctypes.Structure):
    _fields_ = [
        ('MembersFlags', ULONG),
        ('MembersSize', ULONG),
        ('MembersCount', KSIDENTIFIER),
        ('Flags', ULONG),
    ]


PKSPROPERTY_MEMBERSHEADER = POINTER(KSPROPERTY_MEMBERSHEADER)


class KSPROPERTY_BOUNDS_LONG_STRUCT1(ctypes.Structure):
    _fields_ = [
        ('SignedMinimum', LONG),
        ('SignedMaximum', LONG)
    ]


class KSPROPERTY_BOUNDS_LONG_STRUCT2(ctypes.Structure):
    _fields_ = [
        ('UnsignedMinimum', ULONG),
        ('UnsignedMaximum', ULONG),
    ]


class KSPROPERTY_BOUNDS_LONG(ctypes.Union):
    _anonymous_ = [
        'KSPROPERTY_BOUNDS_LONG_STRUCT1',
        'KSPROPERTY_BOUNDS_LONG_STRUCT2'
    ]
    _fields_ = [
        ('KSPROPERTY_BOUNDS_LONG_STRUCT1', KSPROPERTY_BOUNDS_LONG_STRUCT1),
        ('KSPROPERTY_BOUNDS_LONG_STRUCT2', KSPROPERTY_BOUNDS_LONG_STRUCT2)
    ]


PKSPROPERTY_BOUNDS_LONG = POINTER(KSPROPERTY_BOUNDS_LONG)


class KSPROPERTY_BOUNDS_LONGLONG_STRUCT1(ctypes.Structure):
    _fields_ = [
        ('SignedMinimum', LONGLONG),
        ('SignedMaximum', LONGLONG)
    ]


class KSPROPERTY_BOUNDS_LONGLONG_STRUCT2(ctypes.Structure):
    _fields_ = [
        ('UnsignedMinimum', DWORDLONG),
        ('UnsignedMaximum', DWORDLONG),
    ]


class KSPROPERTY_BOUNDS_LONGLONG(ctypes.Union):
    _anonymous_ = [
        'KSPROPERTY_BOUNDS_LONGLONG_STRUCT1',
        'KSPROPERTY_BOUNDS_LONGLONG_STRUCT2'
    ]
    _fields_ = [
        (
            'KSPROPERTY_BOUNDS_LONGLONG_STRUCT1',
            KSPROPERTY_BOUNDS_LONGLONG_STRUCT1),
        (
            'KSPROPERTY_BOUNDS_LONGLONG_STRUCT2',
            KSPROPERTY_BOUNDS_LONGLONG_STRUCT2
        ),
    ]


PKSPROPERTY_BOUNDS_LONGLONG = POINTER(KSPROPERTY_BOUNDS_LONGLONG)


class KSPROPERTY_STEPPING_LONG(ctypes.Structure):
    _fields_ = [
        ('SteppingDelta', ULONG),
        ('Reserved', ULONG),
        ('Bounds', KSPROPERTY_BOUNDS_LONG)
    ]


PKSPROPERTY_STEPPING_LONG = POINTER(KSPROPERTY_STEPPING_LONG)


class KSPROPERTY_STEPPING_LONGLONG(ctypes.Structure):
    _fields_ = [
        ('SteppingDelta', DWORDLONG),
        ('Bounds', KSPROPERTY_BOUNDS_LONGLONG)
    ]


PKSPROPERTY_STEPPING_LONGLONG = POINTER(KSPROPERTY_STEPPING_LONGLONG)


class KSEVENTDATA_UNION(ctypes.Union):

    class EventHandle(ctypes.Structure):
        _fields_ = [
            ('Event', HANDLE),
            ('Reserved', ULONG_PTR)
        ]


    class SemaphoreHandle(ctypes.Structure):
        _fields_ = [
            ('Semaphore', HANDLE),
            ('Reserved', ULONG),
            ('Adjustment', LONG)
        ]

    class Alignment(ctypes.Structure):
        _fields_ = [
            ('Unused', PVOID),
            ('Alignment', LONG_PTR)
        ]

    _fields_ = [
        ('EventHandle', EventHandle),
        ('SemaphoreHandle', SemaphoreHandle),
        ('Alignment', Alignment),

    ]


class KSEVENTDATA(ctypes.Structure):
    _anonymous_ = 'KSEVENTDATA_UNION'
    _fields_ = [
        ('NotificationType', ULONG),
        ('KSEVENTDATA_UNION', KSEVENTDATA_UNION)
    ]


PKSEVENTDATA = POINTER(KSEVENTDATA)


class KSQUERYBUFFER(ctypes.Structure):
    _fields_ = [
        ('Event', KSEVENT),
        ('EventData', PKSEVENTDATA),
        ('Reserved', PVOID)
    ]


PKSQUERYBUFFER = POINTER(KSQUERYBUFFER)


class KSRELATIVEEVENT_UNION(ctypes.Union):
    _fields_ = [
        ('ObjectHandle', HANDLE),
        ('ObjectPointer', PVOID)
    ]


class KSRELATIVEEVENT(ctypes.Structure):
    _anonymous_ = 'KSRELATIVEEVENT_UNION'
    _fields_ = [
        ('Size', ULONG),
        ('Flags', ULONG),
        ('KSRELATIVEEVENT_UNION', KSRELATIVEEVENT_UNION),
        ('Reserved', PVOID),
        ('Event', KSEVENT),
        ('EventData', KSEVENTDATA)
    ]


PKSRELATIVEEVENT = POINTER(KSRELATIVEEVENT)


class KSEVENT_TIME_MARK(ctypes.Structure):
    _fields_ = [
        ('EventData', KSEVENTDATA),
        ('MarkTime', LONGLONG)
    ]


PKSEVENT_TIME_MARK = POINTER(KSEVENT_TIME_MARK)


class KSEVENT_TIME_INTERVAL(ctypes.Structure):
    _fields_ = [
        ('EventData', KSEVENTDATA),
        ('TimeBase', LONGLONG),
        ('Interval', LONGLONG)
    ]


PKSEVENT_TIME_INTERVAL = POINTER(KSEVENT_TIME_INTERVAL)


class KSINTERVAL(ctypes.Structure):
    _fields_ = [
        ('TimeBase', LONGLONG),
        ('Interval', LONGLONG)
    ]


PKSINTERVAL = POINTER(KSINTERVAL)


class KSCOMPONENTID(ctypes.Structure):
    _fields_ = [
        ('Manufacturer', GUID),
        ('Product', GUID),
        ('Manufacturer', GUID),
        ('Product', GUID),
        ('Manufacturer', ULONG),
        ('Product', ULONG)
    ]


PKSCOMPONENTID = POINTER(KSCOMPONENTID)


class KSPROPERTY_POSITIONS(ctypes.Structure):
    _fields_ = [
        ('Current', LONGLONG),
        ('Stop', LONGLONG),
        ('CurrentFlags', KS_SEEKING_FLAGS),
        ('StopFlags', KS_SEEKING_FLAGS)
    ]


PKSPROPERTY_POSITIONS = POINTER(KSPROPERTY_POSITIONS)


class KSPROPERTY_MEDIAAVAILABLE(ctypes.Structure):
    _fields_ = [
        ('Earliest', LONGLONG),
        ('Latest', LONGLONG)
    ]


PKSPROPERTY_MEDIAAVAILABLE = POINTER(KSPROPERTY_MEDIAAVAILABLE)


class KSP_TIMEFORMAT(ctypes.Structure):
    _fields_ = [
        ('Property', KSPROPERTY),
        ('SourceFormat', GUID),
        ('TargetFormat', GUID),
        ('Time', LONGLONG)
    ]


PKSP_TIMEFORMAT = POINTER(KSP_TIMEFORMAT)


class KSTOPOLOGY_CONNECTION(ctypes.Structure):
    _fields_ = [
        ('FromNode', ULONG),
        ('FromNodePin', ULONG),
        ('ToNode', ULONG),
        ('ToNodePin', ULONG)
    ]


PKSTOPOLOGY_CONNECTION = POINTER(KSTOPOLOGY_CONNECTION)


class KSTOPOLOGY(ctypes.Structure):
    _fields_ = [
        ('CategoriesCount', ULONG),
        ('Categories', LPGUID),
        ('TopologyNodesCount', ULONG),
        ('TopologyNodes', LPGUID),
        ('TopologyConnectionsCount', ULONG),
        ('TopologyConnections', PKSTOPOLOGY_CONNECTION),
        ('TopologyNodesNames', LPGUID),
        ('Reserved', ULONG)
    ]
    _field_size_ = [
        'CategoriesCount',
        'TopologyNodesCount',
        'TopologyConnectionsCount',
        'TopologyConnections'
    ]


PKSTOPOLOGY = POINTER(KSTOPOLOGY)


class KSNODE_CREATE(ctypes.Structure):
    _fields_ = [
        ('CreateFlags', ULONG),
        ('Node', ULONG)
    ]


PKSNODE_CREATE = POINTER(KSNODE_CREATE)


class KSINTERFACE_STANDARD(enum):
    KSINTERFACE_STANDARD_STREAMING = 0
    KSINTERFACE_STANDARD_LOOPED_STREAMING = 0
    KSINTERFACE_STANDARD_CONTROL = 0


PKSINTERFACE_STANDARD = POINTER(KSINTERFACE_STANDARD)


class KSINTERFACE_FILEIO(enum):
    KSINTERFACE_FILEIO_STREAMING = 0


PKSINTERFACE_FILEIO = POINTER(KSINTERFACE_FILEIO)


class KSPROPERTY_PIN(enum):
    KSPROPERTY_PIN_CINSTANCES = 0
    KSPROPERTY_PIN_CTYPES = 1
    KSPROPERTY_PIN_DATAFLOW = 2
    KSPROPERTY_PIN_DATARANGES = 3
    KSPROPERTY_PIN_DATAINTERSECTION = 4
    KSPROPERTY_PIN_INTERFACES = 5
    KSPROPERTY_PIN_MEDIUMS = 6
    KSPROPERTY_PIN_COMMUNICATION = 7
    KSPROPERTY_PIN_GLOBALCINSTANCES = 8
    KSPROPERTY_PIN_NECESSARYINSTANCES = 9
    KSPROPERTY_PIN_PHYSICALCONNECTION = 10
    KSPROPERTY_PIN_CATEGORY = 11
    KSPROPERTY_PIN_NAME = 12
    KSPROPERTY_PIN_CONSTRAINEDDATARANGES = 13
    KSPROPERTY_PIN_PROPOSEDATAFORMAT = 14
    KSPROPERTY_PIN_PROPOSEDATAFORMAT2 = 15


PKSPROPERTY_PIN = POINTER(KSPROPERTY_PIN)


class KSPIN_DATAFLOW(enum):
    KSPIN_DATAFLOW_IN = 1
    KSPIN_DATAFLOW_OUT = 2


PKSPIN_DATAFLOW = POINTER(KSPIN_DATAFLOW)


class KSPIN_COMMUNICATION(enum):
    KSPIN_COMMUNICATION_NONE = 0
    KSPIN_COMMUNICATION_SINK = 1
    KSPIN_COMMUNICATION_SOURCE = 2
    KSPIN_COMMUNICATION_BOTH = 3
    KSPIN_COMMUNICATION_BRIDGE = 4


PKSPIN_COMMUNICATION = POINTER(KSPIN_COMMUNICATION)


class KSEVENT_PINCAPS_CHANGENOTIFICATIONS(enum):
    KSEVENT_PINCAPS_FORMATCHANGE = 0
    KSEVENT_PINCAPS_JACKINFOCHANGE = 1


PKSEVENT_PINCAPS_CHANGENOTIFICATIONS = POINTER(
    KSEVENT_PINCAPS_CHANGENOTIFICATIONS
)


class KSEVENT_VOLUMELIMIT(enum):
    KSEVENT_VOLUMELIMIT_CHANGED = 0


PKSEVENT_VOLUMELIMIT = POINTER(KSEVENT_VOLUMELIMIT)


class KSPROPERTY_QUALITY(enum):
    KSPROPERTY_QUALITY_REPORT = 0
    KSPROPERTY_QUALITY_ERROR = 1


PKSPROPERTY_QUALITY = POINTER(KSPROPERTY_QUALITY)


class KSPROPERTY_CONNECTION(enum):
    KSPROPERTY_CONNECTION_STATE = 0
    KSPROPERTY_CONNECTION_PRIORITY = 1
    KSPROPERTY_CONNECTION_DATAFORMAT = 2
    KSPROPERTY_CONNECTION_ALLOCATORFRAMING = 3
    KSPROPERTY_CONNECTION_PROPOSEDATAFORMAT = 4
    KSPROPERTY_CONNECTION_ACQUIREORDERING = 5
    KSPROPERTY_CONNECTION_ALLOCATORFRAMING_EX = 6
    KSPROPERTY_CONNECTION_STARTAT = 7


PKSPROPERTY_CONNECTION = POINTER(KSPROPERTY_CONNECTION)


class KSEVENT_STREAMALLOCATOR(enum):
    KSEVENT_STREAMALLOCATOR_INTERNAL_FREEFRAME = 0
    KSEVENT_STREAMALLOCATOR_FREEFRAME = 1


PKSEVENT_STREAMALLOCATOR = POINTER(KSEVENT_STREAMALLOCATOR)


class KSMETHOD_STREAMALLOCATOR(enum):
    KSMETHOD_STREAMALLOCATOR_ALLOC = 0
    KSMETHOD_STREAMALLOCATOR_FREE = 1


PKSMETHOD_STREAMALLOCATOR = POINTER(KSMETHOD_STREAMALLOCATOR)


class KSPIN_MDL_CACHING_EVENT(enum):
    KSPIN_MDL_CACHING_NOTIFY_CLEANUP = 0
    KSPIN_MDL_CACHING_NOTIFY_CLEANALL_WAIT = 1
    KSPIN_MDL_CACHING_NOTIFY_CLEANALL_NOWAIT = 2
    KSPIN_MDL_CACHING_NOTIFY_ADDSAMPLE = 3


PKSPIN_MDL_CACHING_EVENT = POINTER(KSPIN_MDL_CACHING_EVENT)


class KSPROPERTY_STREAMINTERFACE(enum):
    KSPROPERTY_STREAMINTERFACE_HEADERSIZE = 0


PKSPROPERTY_STREAMINTERFACE = POINTER(KSPROPERTY_STREAMINTERFACE)


class KSPROPERTY_STREAM(enum):
    KSPROPERTY_STREAM_ALLOCATOR = 0
    KSPROPERTY_STREAM_QUALITY = 1
    KSPROPERTY_STREAM_DEGRADATION = 2
    KSPROPERTY_STREAM_MASTERCLOCK = 3
    KSPROPERTY_STREAM_TIMEFORMAT = 4
    KSPROPERTY_STREAM_PRESENTATIONTIME = 5
    KSPROPERTY_STREAM_PRESENTATIONEXTENT = 6
    KSPROPERTY_STREAM_FRAMETIME = 7
    KSPROPERTY_STREAM_RATECAPABILITY = 8
    KSPROPERTY_STREAM_RATE = 9
    KSPROPERTY_STREAM_PIPE_ID = 10


PKSPROPERTY_STREAM = POINTER(KSPROPERTY_STREAM)


class KSPPROPERTY_ALLOCATOR_MDLCACHING(enum):
    KSPROPERTY_ALLOCATOR_CLEANUP_CACHEDMDLPAGES = 1


PKSPPROPERTY_ALLOCATOR_MDLCACHING = POINTER(KSPPROPERTY_ALLOCATOR_MDLCACHING)


class KSPROPERTY_CLOCK(enum):
    KSPROPERTY_CLOCK_TIME = 0
    KSPROPERTY_CLOCK_PHYSICALTIME = 1
    KSPROPERTY_CLOCK_CORRELATEDTIME = 2
    KSPROPERTY_CLOCK_CORRELATEDPHYSICALTIME = 3
    KSPROPERTY_CLOCK_RESOLUTION = 4
    KSPROPERTY_CLOCK_STATE = 5


PKSPROPERTY_CLOCK = POINTER(KSPROPERTY_CLOCK)


class KSEVENT_CLOCK_POSITION(enum):
    KSEVENT_CLOCK_INTERVAL_MARK = 0
    KSEVENT_CLOCK_POSITION_MARK = 1


PKSEVENT_CLOCK_POSITION = POINTER(KSEVENT_CLOCK_POSITION)


class KSEVENT_CONNECTION(enum):
    KSEVENT_CONNECTION_POSITIONUPDATE = 0
    KSEVENT_CONNECTION_DATADISCONTINUITY = 1
    KSEVENT_CONNECTION_TIMEDISCONTINUITY = 2
    KSEVENT_CONNECTION_PRIORITY = 3
    KSEVENT_CONNECTION_ENDOFSTREAM = 4


PKSEVENT_CONNECTION = POINTER(KSEVENT_CONNECTION)



class KSP_PIN_UNION(ctypes.Union):
    _fields_ = [
        ('Reserved', ULONG),
        ('Flags', ULONG)
    ]


class KSP_PIN(ctypes.Structure):
    _anonymous_ = 'KSP_PIN_UNION'
    _fields_ = [
        ('Property', KSPROPERTY),
        ('PinId', ULONG)
    ]


PKSP_PIN = POINTER(KSP_PIN)


class KSE_PIN(ctypes.Structure):
    _fields_ = [
        ('Event', KSEVENT),
        ('PinId', ULONG),
        ('Reserved', ULONG),
    ]


PKSE_PIN = POINTER(KSE_PIN)


class KSPIN_CINSTANCES(ctypes.Structure):
    _fields_ = [
        ('PossibleCount', ULONG),
        ('CurrentCount', ULONG),
    ]


PKSPIN_CINSTANCES = POINTER(KSPIN_CINSTANCES)


class KSDATAFORMAT_STRUCT(ctypes.Structure):
    _fields_ = [
        ('FormatSize', ULONG),
        ('Flags', ULONG),
        ('SampleSize', ULONG),
        ('Reserved', ULONG),
        ('MajorFormat', GUID),
        ('SubFormat', GUID),
        ('Specifier', GUID),
    ]


class KSDATAFORMAT(ctypes.Union):

    _anonymous_ = 'KSDATAFORMAT_STRUCT'
    _fields_ = [
        ('KSDATAFORMAT_STRUCT', KSDATAFORMAT_STRUCT),
        ('Alignment', LONGLONG),
    ]


PKSDATAFORMAT = POINTER(KSDATAFORMAT)
KSDATARANGE = KSDATAFORMAT
PKSDATARANGE = POINTER(KSDATARANGE)


class KSATTRIBUTE(ctypes.Structure):
    _fields_ = [
        ('Size', ULONG),
        ('Flags', ULONG),
        ('Attribute', GUID),
    ]


PKSATTRIBUTE = POINTER(KSATTRIBUTE)


class KSPIN_CONNECT(ctypes.Structure):
    _fields_ = [
        ('Interface', KSPIN_INTERFACE),
        ('Medium', KSPIN_MEDIUM),
        ('PinId', ULONG),
        ('PinToHandle', HANDLE),
        ('Priority', KSPRIORITY),
    ]


PKSPIN_CONNECT = POINTER(KSPIN_CONNECT)


class KSPIN_PHYSICALCONNECTION(ctypes.Structure):
    _fields_ = [
        ('Size', ULONG),
        ('Pin', ULONG),
        ('SymbolicLinkName', WCHAR),
    ]


PKSPIN_PHYSICALCONNECTION = POINTER(KSPIN_PHYSICALCONNECTION)


class KSALLOCATOR_FRAMING_UNION1(ctypes.Union):
    _fields_ = [
        ('OptionsFlags', ULONG),
        ('RequirementsFlags', ULONG)
    ]


class KSALLOCATOR_FRAMING_UNION2(ctypes.Union):
    _fields_ = [
        ('FileAlignment', ULONG),
        ('FramePitch', LONG),
    ]


class KSALLOCATOR_FRAMING(ctypes.Structure):
    _anonymous_ = [
        'KSALLOCATOR_FRAMING_UNION1',
        'KSALLOCATOR_FRAMING_UNION2'
    ]
    _fields_ = [
        ('KSALLOCATOR_FRAMING_UNION1', KSALLOCATOR_FRAMING_UNION1),
        ('PoolType', ULONG),
        ('Frames', ULONG),
        ('FrameSize', ULONG),
        ('KSALLOCATOR_FRAMING_UNION2', KSALLOCATOR_FRAMING_UNION2),
        ('Reserved', ULONG),
    ]


PKSALLOCATOR_FRAMING = POINTER(KSALLOCATOR_FRAMING)


class KS_FRAMING_RANGE(ctypes.Structure):
    _fields_ = [
        ('MinFrameSize', ULONG),
        ('MaxFrameSize', ULONG),
        ('Stepping', ULONG),
    ]


PKS_FRAMING_RANGE = POINTER(KS_FRAMING_RANGE)


class KS_FRAMING_RANGE_WEIGHTED(ctypes.Structure):
    _fields_ = [
        ('Range', KS_FRAMING_RANGE),
        ('InPlaceWeight', ULONG),
        ('NotInPlaceWeight', ULONG),
    ]


PKS_FRAMING_RANGE_WEIGHTED = POINTER(KS_FRAMING_RANGE_WEIGHTED)


class KS_COMPRESSION(ctypes.Structure):
    _fields_ = [
        ('RatioNumerator', ULONG),
        ('RatioDenominator', ULONG),
        ('RatioConstantMargin', ULONG),
    ]


PKS_COMPRESSION = POINTER(KS_COMPRESSION)


class KS_FRAMING_ITEM_UNION(ctypes.Union):
    _fields_ = [
        ('FileAlignment', ULONG),
        ('FramePitch', LONG),
    ]


class KS_FRAMING_ITEM(ctypes.Structure):
    _anonymous_ = 'KS_FRAMING_ITEM_UNION'
    _fields_ = [
        ('MemoryType', GUID),
        ('BusType', GUID),
        ('MemoryFlags', ULONG),
        ('BusFlags', ULONG),
        ('Flags', ULONG),
        ('Frames', ULONG),
        ('KS_FRAMING_ITEM_UNION', KS_FRAMING_ITEM_UNION),
        ('MemoryTypeWeight', ULONG),
        ('PhysicalRange', KS_FRAMING_RANGE),
        ('FramingRange', KS_FRAMING_RANGE_WEIGHTED),
    ]


PKS_FRAMING_ITEM = POINTER(KS_FRAMING_ITEM)



class KSALLOCATOR_FRAMING_EX(ctypes.Structure):
    _fields_ = [
        ('CountItems', ULONG),
        ('PinFlags', ULONG),
        ('OutputCompression', KS_COMPRESSION),
        ('PinWeight', ULONG),
        ('FramingItem', KS_FRAMING_ITEM),
    ]


PKSALLOCATOR_FRAMING_EX = POINTER(KSALLOCATOR_FRAMING_EX)


class KSSTREAMALLOCATOR_STATUS(ctypes.Structure):
    _fields_ = [
        ('Framing', KSALLOCATOR_FRAMING),
        ('AllocatedFrames', ULONG),
        ('Reserved', ULONG)
    ]


PKSSTREAMALLOCATOR_STATUS = POINTER(KSSTREAMALLOCATOR_STATUS)


class KSSTREAMALLOCATOR_STATUS_EX(ctypes.Structure):
    _fields_ = [
        ('AllocatedFrames', ULONG),
        ('Reserved', ULONG)
    ]


PKSSTREAMALLOCATOR_STATUS_EX = POINTER(KSSTREAMALLOCATOR_STATUS_EX)


class KSTIME(ctypes.Structure):
    _fields_ = [
        ('Time', LONGLONG),
        ('Numerator', ULONG),
        ('Denominator', ULONG)
    ]


PKSTIME = POINTER(KSTIME)


class KSSTREAM_HEADER(ctypes.Structure):
    _fields_ = [
        ('Size', ULONG),
        ('TypeSpecificFlags', ULONG),
        ('PresentationTime', KSTIME),
        ('Duration', LONGLONG),
        ('FrameExtent', ULONG),
        ('DataUsed', ULONG),
        ('Data', PVOID),
        ('OptionsFlags', ULONG)
    ]
    _field_size_bytes_ = ['FrameExtent']


PKSSTREAM_HEADER = POINTER(KSSTREAM_HEADER)


class KSSTREAM_METADATA_INFO(ctypes.Structure):
    _fields_ = [
        ('BufferSize', ULONG),
        ('UsedSize', ULONG),
        ('Data', PVOID),
        ('SystemVa', PVOID),
        ('Flags', ULONG),
        ('Reserved', ULONG)
    ]
    _field_size_bytes_ = ['BufferSize']


PKSSTREAM_METADATA_INFO = POINTER(KSSTREAM_METADATA_INFO)


class KSSTREAM_UVC_METADATATYPE_TIMESTAMP_STRUCT(ctypes.Structure):
    _fields_ = [
        ('Counter', USHORT, 11),
        ('Reserved', USHORT, 5)
    ]


class KSSTREAM_UVC_METADATATYPE_TIMESTAMP_UNION(ctypes.Union):
    _anonymous_ = 'KSSTREAM_UVC_METADATATYPE_TIMESTAMP_STRUCT'
    _fields_ = [
        (
            'KSSTREAM_UVC_METADATATYPE_TIMESTAMP_STRUCT',
            KSSTREAM_UVC_METADATATYPE_TIMESTAMP_STRUCT
        ),
        ('SCRToken', USHORT),
    ]


class KSSTREAM_UVC_METADATATYPE_TIMESTAMP(ctypes.Structure):
    _anonymous_ = 'KSSTREAM_UVC_METADATATYPE_TIMESTAMP_UNION'
    _fields_ = [
        ('PresentationTimeStamp', ULONG),
        ('SourceClockReference', ULONG),
        (
            'KSSTREAM_UVC_METADATATYPE_TIMESTAMP_UNION',
            KSSTREAM_UVC_METADATATYPE_TIMESTAMP_UNION
        ),
        ('Reserved0', USHORT),
        ('Reserved1', ULONG)
    ]


PKSSTREAM_UVC_METADATATYPE_TIMESTAMP = POINTER(
    KSSTREAM_UVC_METADATATYPE_TIMESTAMP
)


class KSSTREAM_UVC_METADATA(ctypes.Structure):
    _fields_ = [
        ('StartOfFrameTimestamp', KSSTREAM_UVC_METADATATYPE_TIMESTAMP),
        ('EndOfFrameTimestamp', KSSTREAM_UVC_METADATATYPE_TIMESTAMP)
    ]


PKSSTREAM_UVC_METADATA = POINTER(KSSTREAM_UVC_METADATA)


class KSPIN_MDL_CACHING_NOTIFICATION(ctypes.Structure):
    _fields_ = [
        ('Event', KSPIN_MDL_CACHING_EVENT),
        ('Buffer', PVOID)
    ]


PKSPIN_MDL_CACHING_NOTIFICATION = POINTER(KSPIN_MDL_CACHING_NOTIFICATION)


class KSPIN_MDL_CACHING_NOTIFICATION32(ctypes.Structure):
    _fields_ = [
        ('Event', KSPIN_MDL_CACHING_EVENT),
        ('Buffer', ULONG)
    ]


PKSPIN_MDL_CACHING_NOTIFICATION32 = POINTER(KSPIN_MDL_CACHING_NOTIFICATION32)


class KSQUALITY_MANAGER(ctypes.Structure):
    _fields_ = [
        ('QualityManager', HANDLE),
        ('Context', PVOID)
    ]


PKSQUALITY_MANAGER = POINTER(KSQUALITY_MANAGER)


class KSFRAMETIME(ctypes.Structure):
    _fields_ = [
        ('Duration', LONGLONG),
        ('FrameFlags', ULONG),
        ('Reserved', ULONG)
    ]


PKSFRAMETIME = POINTER(KSFRAMETIME)


class KSRATE(ctypes.Structure):
    _fields_ = [
        ('PresentationStart', LONGLONG),
        ('Duration', LONGLONG),
        ('Interface', KSPIN_INTERFACE),
        ('Rate', LONG),
        ('Flags', ULONG)
    ]


PKSRATE = POINTER(KSRATE)


class KSRATE_CAPABILITY(ctypes.Structure):
    _fields_ = [
        ('Property', KSPROPERTY),
        ('Rate', KSRATE)
    ]


PKSRATE_CAPABILITY = POINTER(KSRATE_CAPABILITY)


class KSCLOCK_CREATE(ctypes.Structure):
    _fields_ = [
        ('CreateFlags', LONGLONG)
    ]


PKSCLOCK_CREATE = POINTER(KSCLOCK_CREATE)


class KSCORRELATED_TIME(ctypes.Structure):
    _fields_ = [
        ('Time', LONGLONG),
        ('SystemTime', LONGLONG)
    ]


PKSCORRELATED_TIME = POINTER(KSCORRELATED_TIME)


class KSRESOLUTION(ctypes.Structure):
    _fields_ = [
        ('Granularity', LONGLONG),
        ('Error', LONGLONG)
    ]


PKSRESOLUTION = POINTER(KSRESOLUTION)





class KSMETHOD_ITEM_UNION(ctypes.Union):
    _fields_ = [
        ('MethodHandler', PFNKSHANDLER),
        ('MethodSupported', BOOL)
    ]


class KSMETHOD_ITEM(ctypes.Structure):
    _anonymous_ = 'KSMETHOD_ITEM_UNION'
    _fields_ = [
        ('MethodId', ULONG),
        ('KSMETHOD_ITEM_UNION', KSMETHOD_ITEM_UNION),
        ('MinMethod', ULONG),
        ('MinData', ULONG),
        ('SupportHandler', PFNKSHANDLER),
        ('Flags', ULONG),
    ]



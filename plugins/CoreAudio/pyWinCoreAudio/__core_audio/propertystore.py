import ctypes

from ctypes.wintypes import (
    LARGE_INTEGER,
    VARIANT_BOOL,
    FILETIME,
    ULARGE_INTEGER,
    ULONG,
    SHORT,
    USHORT,
    INT,
    FLOAT,
    DOUBLE,
    UINT
)
from comtypes.automation import (
    SCODE,
    IDispatch,
    VARIANT
)
from comtypes import (
    COMMETHOD,
    IUnknown,
    GUID,
    BSTR
)
from comtypes.typeinfo import (
    tagSAFEARRAYBOUND,
    tagTYPEDESC,
    tagARRAYDESC,
    IRecordInfo
)

STRING = ctypes.c_char_p
WSTRING = ctypes.c_wchar_p
LONGLONG = ctypes.c_longlong
UBYTE = ctypes.c_ubyte
ULONGLONG = ctypes.c_ulonglong
CHAR = ctypes.c_char
HRESULT = ctypes.HRESULT
POINTER = ctypes.POINTER


class tagCAUH(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(ULARGE_INTEGER)),
    ]


class _wireSAFEARR_DISPATCH(ctypes.Structure):
    _fields_ = [
        ('Size', ULONG),
        ('apDispatch', POINTER(POINTER(IDispatch))),
    ]


class tagCACY(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(LONGLONG)),
    ]


class tagSTATSTG(ctypes.Structure):
    pass


tagSTATSTG._fields_ = [
    ('pwcsName', WSTRING),
    ('type', ULONG),
    ('cbSize', ULARGE_INTEGER),
    ('mtime', FILETIME),
    ('ctime', FILETIME),
    ('atime', FILETIME),
    ('grfMode', ULONG),
    ('grfLocksSupported', ULONG),
    ('clsid', GUID),
    ('grfStateBits', ULONG),
    ('reserved', ULONG),
]


class __MIDL___MIDL_itf_mmdeviceapi_0003_0085_0001(ctypes.Union):
    pass


class tagCLIPDATA(ctypes.Structure):
    pass


class tagBSTRBLOB(ctypes.Structure):
    _fields_ = [
        ('cbSize', ULONG),
        ('pData', POINTER(UBYTE)),
    ]


class tagBLOB(ctypes.Structure):
    _fields_ = [
        ('cbSize', ULONG),
        ('pBlobData', POINTER(UBYTE)),
    ]


class ISequentialStream(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0C733A30-2A1C-11CE-ADE5-00AA0044773D}')
    _idlflags_ = []


class IStream(ISequentialStream):
    _case_insensitive_ = True
    _iid_ = GUID('{0000000C-0000-0000-C000-000000000046}')
    _idlflags_ = []


class IStorage(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0000000B-0000-0000-C000-000000000046}')
    _idlflags_ = []


class tagVersionedStream(ctypes.Structure):
    pass


class _wireSAFEARRAY(ctypes.Structure):
    pass


wirePSAFEARRAY = POINTER(POINTER(_wireSAFEARRAY))


class tagCAC(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', STRING),
    ]


class tagCAUB(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(UBYTE)),
    ]


class tagCAI(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(SHORT)),
    ]


class tagCAUI(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(USHORT)),
    ]


class tagCAL(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(INT)),
    ]


class tagCAUL(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(ULONG)),
    ]


class tagCAH(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(LARGE_INTEGER)),
    ]


class tagCAFLT(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(FLOAT)),
    ]


class tagCADBL(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(DOUBLE)),
    ]


class tagCABOOL(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(VARIANT_BOOL)),
    ]


class tagCASCODE(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(SCODE)),
    ]


class tagCADATE(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(DOUBLE)),
    ]


class tagCAFILETIME(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(FILETIME)),
    ]


class tagCACLSID(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(GUID)),
    ]


class tagCACLIPDATA(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(tagCLIPDATA)),
    ]


class tagCABSTR(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(BSTR)),
    ]


class tagCABSTRBLOB(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(tagBSTRBLOB)),
    ]


class tagCALPSTR(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(STRING)),
    ]


class tagCALPWSTR(ctypes.Structure):
    _fields_ = [
        ('cElems', ULONG),
        ('pElems', POINTER(WSTRING)),
    ]


class tagCAPROPVARIANT(ctypes.Structure):
    pass


class tag_inner_PROPVARIANT(ctypes.Structure):
    pass


tagCAPROPVARIANT._fields_ = [
    ('cElems', ULONG),
    ('pElems', POINTER(tag_inner_PROPVARIANT)),
]


class DECIMAL(ctypes.Structure):
    _fields_ = [
        ("wReserved", USHORT),
        ("scale", UBYTE),
        ("sign", UBYTE),
        ("Hi32", ULONG),
        ("Lo64", ULONGLONG)
    ]


__MIDL___MIDL_itf_mmdeviceapi_0003_0085_0001._fields_ = [
    ('cVal', CHAR),
    ('bVal', UBYTE),
    ('iVal', SHORT),
    ('uiVal', USHORT),
    ('lVal', INT),
    ('ulVal', ULONG),
    ('intVal', INT),
    ('uintVal', UINT),
    ('hVal', LARGE_INTEGER),
    ('uhVal', ULARGE_INTEGER),
    ('fltVal', FLOAT),
    ('dblVal', DOUBLE),
    ('boolVal', VARIANT_BOOL),
    ('bool', VARIANT_BOOL),
    ('scode', SCODE),
    ('cyVal', LONGLONG),
    ('date', DOUBLE),
    ('filetime', FILETIME),
    ('puuid', POINTER(GUID)),
    ('pClipData', POINTER(tagCLIPDATA)),
    ('bstrVal', BSTR),
    ('bstrblobVal', tagBSTRBLOB),
    ('blob', tagBLOB),
    ('pszVal', STRING),
    ('pwszVal', WSTRING),
    ('punkVal', POINTER(IUnknown)),
    ('pdispVal', POINTER(IDispatch)),
    ('pStream', POINTER(IStream)),
    ('pStorage', POINTER(IStorage)),
    ('pVersionedStream', POINTER(tagVersionedStream)),
    ('parray', wirePSAFEARRAY),
    ('cac', tagCAC),
    ('caub', tagCAUB),
    ('cai', tagCAI),
    ('caui', tagCAUI),
    ('cal', tagCAL),
    ('caul', tagCAUL),
    ('cah', tagCAH),
    ('cauh', tagCAUH),
    ('caflt', tagCAFLT),
    ('cadbl', tagCADBL),
    ('cabool', tagCABOOL),
    ('cascode', tagCASCODE),
    ('cacy', tagCACY),
    ('cadate', tagCADATE),
    ('cafiletime', tagCAFILETIME),
    ('cauuid', tagCACLSID),
    ('caclipdata', tagCACLIPDATA),
    ('cabstr', tagCABSTR),
    ('cabstrblob', tagCABSTRBLOB),
    ('calpstr', tagCALPSTR),
    ('calpwstr', tagCALPWSTR),
    ('capropvar', tagCAPROPVARIANT),
    ('pcVal', STRING),
    ('pbVal', POINTER(UBYTE)),
    ('piVal', POINTER(SHORT)),
    ('puiVal', POINTER(USHORT)),
    ('plVal', POINTER(INT)),
    ('pulVal', POINTER(ULONG)),
    ('pintVal', POINTER(INT)),
    ('puintVal', POINTER(UINT)),
    ('pfltVal', POINTER(FLOAT)),
    ('pdblVal', POINTER(DOUBLE)),
    ('pboolVal', POINTER(VARIANT_BOOL)),
    ('pdecVal', POINTER(DECIMAL)),
    ('pscode', POINTER(SCODE)),
    ('pcyVal', POINTER(LONGLONG)),
    ('pdate', POINTER(DOUBLE)),
    ('pbstrVal', POINTER(BSTR)),
    ('ppunkVal', POINTER(POINTER(IUnknown))),
    ('ppdispVal', POINTER(POINTER(IDispatch))),
    ('pparray', POINTER(wirePSAFEARRAY)),
    ('pvarVal', POINTER(tag_inner_PROPVARIANT)),
]
ISequentialStream._methods_ = [
    COMMETHOD(
        [],
        HRESULT,
        'RemoteRead',
        (['out'], POINTER(UBYTE), 'pv'),
        (['in'], ULONG, 'cb'),
        (['out'], POINTER(ULONG), 'pcbRead')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'RemoteWrite',
        (['in'], POINTER(UBYTE), 'pv'),
        (['in'], ULONG, 'cb'),
        (['out'], POINTER(ULONG), 'pcbWritten')
    ),
]


IStream._methods_ = [
    COMMETHOD(
        [],
        HRESULT,
        'RemoteSeek',
        (['in'], LARGE_INTEGER, 'dlibMove'),
        (['in'], ULONG, 'dwOrigin'),
        (['out'], POINTER(ULARGE_INTEGER), 'plibNewPosition')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetSize',
        (['in'], ULARGE_INTEGER, 'libNewSize')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'RemoteCopyTo',
        (['in'], POINTER(IStream), 'pstm'),
        (['in'], ULARGE_INTEGER, 'cb'),
        (['out'], POINTER(ULARGE_INTEGER), 'pcbRead'),
        (['out'], POINTER(ULARGE_INTEGER), 'pcbWritten')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Commit',
        (['in'], ULONG, 'grfCommitFlags')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Revert'
    ),
    COMMETHOD(
        [],
        HRESULT,
        'LockRegion',
        (['in'], ULARGE_INTEGER, 'libOffset'),
        (['in'], ULARGE_INTEGER, 'cb'),
        (['in'], ULONG, 'dwLockType')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'UnlockRegion',
        (['in'], ULARGE_INTEGER, 'libOffset'),
        (['in'], ULARGE_INTEGER, 'cb'),
        (['in'], ULONG, 'dwLockType')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Stat',
        (['out'], POINTER(tagSTATSTG), 'pstatstg'),
        (['in'], ULONG, 'grfStatFlag')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Clone',
        (['out'], POINTER(POINTER(IStream)), 'ppstm')
    ),
]


class _FLAGGED_WORD_BLOB(ctypes.Structure):
    _fields_ = [
        ('fFlags', ULONG),
        ('clSize', ULONG),
        ('asData', POINTER(USHORT)),
    ]


class _IPropertyStore(IUnknown):
    _case_insensitive_ = True
    u'Simple Property Store Interface'
    _iid_ = GUID('{886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99}')
    _idlflags_ = []


class _tagpropertykey(ctypes.Structure):
    pass


_IPropertyStore._methods_ = [
    COMMETHOD(
        [],
        HRESULT,
        'GetCount',
        (['out'], POINTER(ULONG), 'cProps')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetAt',
        (['in'], ULONG, 'iProp'),
        (['out'], POINTER(_tagpropertykey), 'pkey')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'GetValue',
        (['in'], POINTER(_tagpropertykey), 'key'),
        (['out'], POINTER(tag_inner_PROPVARIANT), 'pv')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetValue',
        (['in'], POINTER(_tagpropertykey), 'key'),
        (['in'], POINTER(tag_inner_PROPVARIANT), 'propvar')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Commit'
    ),
]

tagVersionedStream._fields_ = [
    ('guidVersion', GUID),
    ('pStream', POINTER(IStream)),
]
_tagpropertykey._fields_ = [
    ('fmtid', GUID),
    ('pid', ULONG),
]


class __MIDL_IOleAutomationTypes_0005(ctypes.Union):
    pass


__MIDL_IOleAutomationTypes_0005._fields_ = [
    ('lptdesc', POINTER(tagTYPEDESC)),
    ('lpadesc', POINTER(tagARRAYDESC)),
    ('hreftype', ULONG),
]


class _BYTE_SIZEDARR(ctypes.Structure):
    _fields_ = [
        ('clSize', ULONG),
        ('pData', POINTER(UBYTE)),
    ]


tagCLIPDATA._fields_ = [
    ('cbSize', ULONG),
    ('ulClipFmt', INT),
    ('pClipData', POINTER(UBYTE)),
]


class _wireSAFEARR_UNKNOWN(ctypes.Structure):
    _fields_ = [
        ('Size', ULONG),
        ('apUnknown', POINTER(POINTER(IUnknown))),
    ]


class _wireSAFEARR_VARIANT(ctypes.Structure):
    pass


class _wireVARIANT(ctypes.Structure):
    pass


_wireSAFEARR_VARIANT._fields_ = [
    ('Size', ULONG),
    ('aVariant', POINTER(POINTER(_wireVARIANT))),
]


class __MIDL_IOleAutomationTypes_0006(ctypes.Union):
    pass


__MIDL_IOleAutomationTypes_0006._fields_ = [
    ('oInst', ULONG),
    ('lpvarValue', POINTER(VARIANT)),
]


class __MIDL_IOleAutomationTypes_0004(ctypes.Union):
    pass


class _wireBRECORD(ctypes.Structure):
    pass


__MIDL_IOleAutomationTypes_0004._fields_ = [
    ('llVal', LONGLONG),
    ('lVal', INT),
    ('bVal', UBYTE),
    ('iVal', SHORT),
    ('fltVal', FLOAT),
    ('dblVal', DOUBLE),
    ('boolVal', VARIANT_BOOL),
    ('scode', SCODE),
    ('cyVal', LONGLONG),
    ('date', DOUBLE),
    ('bstrVal', POINTER(_FLAGGED_WORD_BLOB)),
    ('punkVal', POINTER(IUnknown)),
    ('pdispVal', POINTER(IDispatch)),
    ('parray', POINTER(POINTER(_wireSAFEARRAY))),
    ('brecVal', POINTER(_wireBRECORD)),
    ('pbVal', POINTER(UBYTE)),
    ('piVal', POINTER(SHORT)),
    ('plVal', POINTER(INT)),
    ('pllVal', POINTER(LONGLONG)),
    ('pfltVal', POINTER(FLOAT)),
    ('pdblVal', POINTER(DOUBLE)),
    ('pboolVal', POINTER(VARIANT_BOOL)),
    ('pscode', POINTER(SCODE)),
    ('pcyVal', POINTER(LONGLONG)),
    ('pdate', POINTER(DOUBLE)),
    ('pbstrVal', POINTER(POINTER(_FLAGGED_WORD_BLOB))),
    ('ppunkVal', POINTER(POINTER(IUnknown))),
    ('ppdispVal', POINTER(POINTER(IDispatch))),
    ('pparray', POINTER(POINTER(POINTER(_wireSAFEARRAY)))),
    ('pvarVal', POINTER(POINTER(_wireVARIANT))),
    ('cVal', CHAR),
    ('uiVal', USHORT),
    ('ulVal', ULONG),
    ('ullVal', ULONGLONG),
    ('intVal', INT),
    ('uintVal', UINT),
    ('decVal', DECIMAL),
    ('pdecVal', POINTER(DECIMAL)),
    ('pcVal', STRING),
    ('puiVal', POINTER(USHORT)),
    ('pulVal', POINTER(ULONG)),
    ('pullVal', POINTER(ULONGLONG)),
    ('pintVal', POINTER(INT)),
    ('puintVal', POINTER(UINT)),
]
_wireVARIANT._fields_ = [
    ('clSize', ULONG),
    ('rpcReserved', ULONG),
    ('vt', USHORT),
    ('wReserved1', USHORT),
    ('wReserved2', USHORT),
    ('wReserved3', USHORT),
    ('DUMMYUNIONNAME', __MIDL_IOleAutomationTypes_0004),
]


class __MIDL_IOleAutomationTypes_0001(ctypes.Union):
    pass


class _wireSAFEARR_BSTR(ctypes.Structure):
    _fields_ = [
        ('Size', ULONG),
        ('aBstr', POINTER(POINTER(_FLAGGED_WORD_BLOB))),
    ]


class _wireSAFEARR_BRECORD(ctypes.Structure):
    _fields_ = [
        ('Size', ULONG),
        ('aRecord', POINTER(POINTER(_wireBRECORD))),
    ]


class _wireSAFEARR_HAVEIID(ctypes.Structure):
    _fields_ = [
        ('Size', ULONG),
        ('apUnknown', POINTER(POINTER(IUnknown))),
        ('iid', GUID),
    ]


class _SHORT_SIZEDARR(ctypes.Structure):
    _fields_ = [
        ('clSize', ULONG),
        ('pData', POINTER(USHORT)),
    ]


class _LONG_SIZEDARR(ctypes.Structure):
    _fields_ = [
        ('clSize', ULONG),
        ('pData', POINTER(ULONG)),
    ]


class _HYPER_SIZEDARR(ctypes.Structure):
    _fields_ = [
        ('clSize', ULONG),
        ('pData', POINTER(LONGLONG)),
    ]


__MIDL_IOleAutomationTypes_0001._fields_ = [
    ('BstrStr', _wireSAFEARR_BSTR),
    ('UnknownStr', _wireSAFEARR_UNKNOWN),
    ('DispatchStr', _wireSAFEARR_DISPATCH),
    ('VariantStr', _wireSAFEARR_VARIANT),
    ('RecordStr', _wireSAFEARR_BRECORD),
    ('HaveIidStr', _wireSAFEARR_HAVEIID),
    ('ByteStr', _BYTE_SIZEDARR),
    ('WordStr', _SHORT_SIZEDARR),
    ('LongStr', _LONG_SIZEDARR),
    ('HyperStr', _HYPER_SIZEDARR),
]


class tagRemSNB(ctypes.Structure):
    _fields_ = [
        ('ulCntStr', ULONG),
        ('ulCntChar', ULONG),
        ('rgString', POINTER(USHORT)),
    ]


class _wireSAFEARRAY_UNION(ctypes.Structure):
    pass


_wireSAFEARRAY_UNION._fields_ = [
    ('sfType', ULONG),
    ('u', __MIDL_IOleAutomationTypes_0001),
]
_wireSAFEARRAY._fields_ = [
    ('cDims', USHORT),
    ('fFeatures', USHORT),
    ('cbElements', ULONG),
    ('cLocks', ULONG),
    ('uArrayStructs', _wireSAFEARRAY_UNION),
    ('rgsabound', POINTER(tagSAFEARRAYBOUND)),
]
_wireBRECORD._fields_ = [
    ('fFlags', ULONG),
    ('clSize', ULONG),
    ('pRecInfo', POINTER(IRecordInfo)),
    ('pRecord', POINTER(UBYTE)),
]


class IEnumSTATSTG(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{0000000D-0000-0000-C000-000000000046}')
    _idlflags_ = []


IEnumSTATSTG._methods_ = [
    COMMETHOD(
        [],
        HRESULT,
        'RemoteNext',
        (['in'], ULONG, 'celt'),
        (['out'], POINTER(tagSTATSTG), 'rgelt'),
        (['out'], POINTER(ULONG), 'pceltFetched')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Skip',
        (['in'], ULONG, 'celt')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Reset'
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Clone',
        (['out'], POINTER(POINTER(IEnumSTATSTG)), 'ppenum')
    ),
]

tag_inner_PROPVARIANT._fields_ = [
    ('vt', USHORT),
    ('wReserved1', UBYTE),
    ('wReserved2', UBYTE),
    ('wReserved3', ULONG),
    (
        '__MIDL____MIDL_itf_mmdeviceapi_0003_00850001',
        __MIDL___MIDL_itf_mmdeviceapi_0003_0085_0001
    ),
]
wireSNB = POINTER(tagRemSNB)
IStorage._methods_ = [
    COMMETHOD(
        [],
        HRESULT,
        'CreateStream',
        (['in'], WSTRING, 'pwcsName'),
        (['in'], ULONG, 'grfMode'),
        (['in'], ULONG, 'reserved1'),
        (['in'], ULONG, 'reserved2'),
        (['out'], POINTER(POINTER(IStream)), 'ppstm')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'RemoteOpenStream',
        (['in'], WSTRING, 'pwcsName'),
        (['in'], ULONG, 'cbReserved1'),
        (['in'], POINTER(UBYTE), 'reserved1'),
        (['in'], ULONG, 'grfMode'),
        (['in'], ULONG, 'reserved2'),
        (['out'], POINTER(POINTER(IStream)), 'ppstm')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'CreateStorage',
        (['in'], WSTRING, 'pwcsName'),
        (['in'], ULONG, 'grfMode'),
        (['in'], ULONG, 'reserved1'),
        (['in'], ULONG, 'reserved2'),
        (['out'], POINTER(POINTER(IStorage)), 'ppstg')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'OpenStorage',
        (['in'], WSTRING, 'pwcsName'),
        (['in'], POINTER(IStorage), 'pstgPriority'),
        (['in'], ULONG, 'grfMode'),
        (['in'], wireSNB, 'snbExclude'),
        (['in'], ULONG, 'reserved'),
        (['out'], POINTER(POINTER(IStorage)), 'ppstg')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'RemoteCopyTo',
        (['in'], ULONG, 'ciidExclude'),
        (['in'], POINTER(GUID), 'rgiidExclude'),
        (['in'], wireSNB, 'snbExclude'),
        (['in'], POINTER(IStorage), 'pstgDest')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'MoveElementTo',
        (['in'], WSTRING, 'pwcsName'),
        (['in'], POINTER(IStorage), 'pstgDest'),
        (['in'], WSTRING, 'pwcsNewName'),
        (['in'], ULONG, 'grfFlags')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Commit',
        (['in'], ULONG, 'grfCommitFlags')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Revert'
    ),
    COMMETHOD(
        [],
        HRESULT,
        'RemoteEnumElements',
        (['in'], ULONG, 'reserved1'),
        (['in'], ULONG, 'cbReserved2'),
        (['in'], POINTER(UBYTE), 'reserved2'),
        (['in'], ULONG, 'reserved3'),
        (['out'], POINTER(POINTER(IEnumSTATSTG)), 'ppenum')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'DestroyElement',
        (['in'], WSTRING, 'pwcsName')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'RenameElement',
        (['in'], WSTRING, 'pwcsOldName'),
        (['in'], WSTRING, 'pwcsNewName')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetElementTimes',
        (['in'], WSTRING, 'pwcsName'),
        (['in'], POINTER(FILETIME), 'pctime'),
        (['in'], POINTER(FILETIME), 'patime'),
        (['in'], POINTER(FILETIME), 'pmtime')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetClass',
        (['in'], POINTER(GUID), 'clsid')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetStateBits',
        (['in'], ULONG, 'grfStateBits'),
        (['in'], ULONG, 'grfMask')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'Stat',
        (['out'], POINTER(tagSTATSTG), 'pstatstg'),
        (['in'], ULONG, 'grfStatFlag')
    ),
]


PROPVARIANT = tag_inner_PROPVARIANT
PPROPVARIANT = POINTER(PROPVARIANT)

PROPERTYKEY = _tagpropertykey
PPROPERTYKEY = POINTER(_tagpropertykey)


class IPropertyStore(_IPropertyStore):

    def GetValue(self, key):
        value = _IPropertyStore.GetValue(self, key)

        # Types for vt defined here:
        # https://msdn.microsoft.com/en-us/library/windows/
        # desktop/aa380072%28v=vs.85%29.aspx

        vt = value.vt
        vc = getattr(value, '__MIDL____MIDL_itf_mmdeviceapi_0003_00850001')

        if vt in (0, 1):
            return None
        if vt == 14:
            return vc.decVal
        if vt == 73:
            return vc.pVersionedStream
        if vt in (69, 67):
            return vc.pStorage
        if vt in (68, 66):
            return vc.pStream
        if vt == 9:
            return vc.pdispVal
        if vt == 13:
            return vc.punkVal
        if vt == 31:
            return vc.pwszVal
        if vt == 30:
            return vc.pszVal
        if vt in (70, 65):
            return vc.blob
        if vt == 0xfff:
            return vc.bstrblobVal
        if vt == 8:
            return vc.bstrVal
        if vt == 71:
            return vc.pclipdata
        if vt == 72:
            return vc.puuid
        if vt == 64:
            return vc.filetime
        if vt == 7:
            return vc.date
        if vt == 6:
            return vc.cyVal
        if vt == 10:
            return vc.scode
        if vt == 11:
            return vc.boolVal
        if vt == 5:
            return vc.dblVal
        if vt == 4:
            return vc.fltVal
        if vt == 21:
            return vc.uhVal
        if vt == 20:
            return vc.hVal
        if vt == 23:
            return vc.uintVal
        if vt == 22:
            return vc.intVal
        if vt == 19:
            return vc.ulVal
        if vt == 3:
            return vc.lVal
        if vt == 18:
            return vc.uiVal
        if vt == 2:
            return vc.iVal
        if vt == 17:
            return vc.bVal
        if vt == 16:
            return vc.cVal


PIPropertyStore = POINTER(IPropertyStore)

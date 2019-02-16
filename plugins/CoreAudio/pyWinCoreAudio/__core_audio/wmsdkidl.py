

import comtypes
import ctypes
from comtypes import GUID
from ctypes.wintypes import (
    BYTE,
    WORD,
    DWORD,
    WCHAR,

)

COMMETHOD = comtypes.COMMETHOD

VOID = ctypes.c_void_p
LONGLONG = ctypes.c_longlong
POINTER = ctypes.POINTER
Structure = ctypes.Structure
Union = ctypes.Union



def _convert_guid(*hex_guid):
    guid = []
    hex_four = ''
    hex_twelve = ''
    for h in hex_guid:
        h = hex(h)[2:].replace('L', '')

        if len(h) not in (8, 4, 2):
            h = '0' + h

        if len(h) == 2:
            if hex_four is not None and hex_four:
                h = hex_four + h
                hex_four = None
            elif hex_four is None:
                hex_twelve += h
                if len(hex_twelve) == 12:
                    h = hex_twelve
                else:
                    continue
            else:
                hex_four = h
                continue
        guid += [h.upper()]

    guid = '{' + '-'.join(guid) + '}'
    return guid


def EXTERN_GUID(*hex_guid):
    return GUID(_convert_guid(*hex_guid))


# ////////////////////////////////////////////////////////////////
# //
# // These are the special case attributes that give information
# // about the Windows Media file.
# //
g_dwWMSpecialAttributes = DWORD(20)
g_wszWMDuration = WCHAR("Duration")
g_wszWMBitrate = WCHAR("Bitrate")
g_wszWMSeekable = WCHAR("Seekable")
g_wszWMStridable = WCHAR("Stridable")
g_wszWMBroadcast = WCHAR("Broadcast")
g_wszWMProtected = WCHAR("Is_Protected")
g_wszWMTrusted = WCHAR("Is_Trusted")
g_wszWMSignature_Name = WCHAR("Signature_Name")
g_wszWMHasAudio = WCHAR("HasAudio")
g_wszWMHasImage = WCHAR("HasImage")
g_wszWMHasScript = WCHAR("HasScript")
g_wszWMHasVideo = WCHAR("HasVideo")
g_wszWMCurrentBitrate = WCHAR("CurrentBitrate")
g_wszWMOptimalBitrate = WCHAR("OptimalBitrate")
g_wszWMHasAttachedImages = WCHAR("HasAttachedImages")
g_wszWMSkipBackward = WCHAR("Can_Skip_Backward")
g_wszWMSkipForward = WCHAR("Can_Skip_Forward")
g_wszWMNumberOfFrames = WCHAR("NumberOfFrames")
g_wszWMFileSize = WCHAR("FileSize")
g_wszWMHasArbitraryDataStream = WCHAR("HasArbitraryDataStream")
g_wszWMHasFileTransferStream = WCHAR("HasFileTransferStream")
g_wszWMContainerFormat = WCHAR("WM/ContainerFormat")

# ////////////////////////////////////////////////////////////////
# //
# // The content description object supports 5 basic attributes.
# //
g_dwWMContentAttributes = DWORD(5)
g_wszWMTitle = WCHAR("Title")
g_wszWMTitleSort = WCHAR("TitleSort")
g_wszWMAuthor = WCHAR("Author")
g_wszWMAuthorSort = WCHAR("AuthorSort")
g_wszWMDescription = WCHAR("Description")
g_wszWMRating = WCHAR("Rating")
g_wszWMCopyright = WCHAR("Copyright")

# ////////////////////////////////////////////////////////////////
# //
# // These attributes are used to configure and query
# // DRM settings in the reader and writer.
# //
g_wszWMUse_DRM = WCHAR("Use_DRM")
g_wszWMDRM_Flags = WCHAR("DRM_Flags")
g_wszWMDRM_Level = WCHAR("DRM_Level")
g_wszWMUse_Advanced_DRM = WCHAR("Use_Advanced_DRM")
g_wszWMDRM_KeySeed = WCHAR("DRM_KeySeed")
g_wszWMDRM_KeyID = WCHAR("DRM_KeyID")
g_wszWMDRM_ContentID = WCHAR("DRM_ContentID")
g_wszWMDRM_SourceID = WCHAR("DRM_SourceID")
g_wszWMDRM_IndividualizedVersion = WCHAR("DRM_IndividualizedVersion")
g_wszWMDRM_LicenseAcqURL = WCHAR("DRM_LicenseAcqUR")
g_wszWMDRM_V1LicenseAcqURL = WCHAR("DRM_V1LicenseAcqUR")
g_wszWMDRM_HeaderSignPrivKey = WCHAR("DRM_HeaderSignPrivKey")
g_wszWMDRM_LASignaturePrivKey = WCHAR("DRM_LASignaturePrivKey")
g_wszWMDRM_LASignatureCert = WCHAR("DRM_LASignatureCert")
g_wszWMDRM_LASignatureLicSrvCert = WCHAR("DRM_LASignatureLicSrvCert")
g_wszWMDRM_LASignatureRootCert = WCHAR("DRM_LASignatureRootCert")

# ////////////////////////////////////////////////////////////////
# //
# // These are the additional attributes defined in the WM attribute
# // namespace that give information about the content.
# //
g_wszWMAlbumTitle = WCHAR("WM/AlbumTitle")
g_wszWMAlbumTitleSort = WCHAR("WM/AlbumTitleSort")
g_wszWMTrack = WCHAR("WM/Track")
g_wszWMPromotionURL = WCHAR("WM/PromotionUR")
g_wszWMAlbumCoverURL = WCHAR("WM/AlbumCoverUR")
g_wszWMGenre = WCHAR("WM/Genre")
g_wszWMYear = WCHAR("WM/Year")
g_wszWMGenreID = WCHAR("WM/GenreID")
g_wszWMMCDI = WCHAR("WM/MCDI")
g_wszWMComposer = WCHAR("WM/Composer")
g_wszWMComposerSort = WCHAR("WM/ComposerSort")
g_wszWMLyrics = WCHAR("WM/Lyrics")
g_wszWMTrackNumber = WCHAR("WM/TrackNumber")
g_wszWMToolName = WCHAR("WM/ToolName")
g_wszWMToolVersion = WCHAR("WM/ToolVersion")
g_wszWMIsVBR = WCHAR("IsVBR")
g_wszWMAlbumArtist = WCHAR("WM/AlbumArtist")
g_wszWMAlbumArtistSort = WCHAR("WM/AlbumArtistSort")

# ////////////////////////////////////////////////////////////////
# //
# // These optional attributes may be used to give information
# // about the branding of the content.
# //
g_wszWMBannerImageType = WCHAR("BannerImageType")
g_wszWMBannerImageData = WCHAR("BannerImageData")
g_wszWMBannerImageURL = WCHAR("BannerImageUR")
g_wszWMCopyrightURL = WCHAR("CopyrightUR")

# ////////////////////////////////////////////////////////////////
# //
# // Optional attributes, used to give information
# // about video stream properties.
# //
g_wszWMAspectRatioX = WCHAR("AspectRatioX")
g_wszWMAspectRatioY = WCHAR("AspectRatioY")

# ////////////////////////////////////////////////////////////////
# //
# // Optional attributes, used to give information
# // about the overall streaming properties of VBR files.
# // This attribute takes the format:
# //  WORD wReserved (must be 0)
# //  WM_LEAKY_BUCKET_PAIR pair1
# //  WM_LEAKY_BUCKET_PAIR pair2
# //  ...
# //
g_wszASFLeakyBucketPairs = WCHAR("ASFLeakyBucketPairs")

# ////////////////////////////////////////////////////////////////
# //
# // The NSC file supports the following attributes.
# //
g_dwWMNSCAttributes = DWORD(5)
g_wszWMNSCName = WCHAR("NSC_Name")
g_wszWMNSCAddress = WCHAR("NSC_Address")
g_wszWMNSCPhone = WCHAR("NSC_Phone")
g_wszWMNSCEmail = WCHAR("NSC_Email")
g_wszWMNSCDescription = WCHAR("NSC_Description")

# ////////////////////////////////////////////////////////////////
# //
# // Attributes introduced in V9
# //
g_wszWMWriter = WCHAR("WM/Writer")
g_wszWMConductor = WCHAR("WM/Conductor")
g_wszWMProducer = WCHAR("WM/Producer")
g_wszWMDirector = WCHAR("WM/Director")
g_wszWMContentGroupDescription = WCHAR("WM/ContentGroupDescription")
g_wszWMSubTitle = WCHAR("WM/SubTitle")
g_wszWMPartOfSet = WCHAR("WM/PartOfSet")
g_wszWMProtectionType = WCHAR("WM/ProtectionType")
g_wszWMVideoHeight = WCHAR("WM/VideoHeight")
g_wszWMVideoWidth = WCHAR("WM/VideoWidth")
g_wszWMVideoFrameRate = WCHAR("WM/VideoFrameRate")
g_wszWMMediaClassPrimaryID = WCHAR("WM/MediaClassPrimaryID")
g_wszWMMediaClassSecondaryID = WCHAR("WM/MediaClassSecondaryID")
g_wszWMPeriod = WCHAR("WM/Period")
g_wszWMCategory = WCHAR("WM/Category")
g_wszWMPicture = WCHAR("WM/Picture")
g_wszWMLyrics_Synchronised = WCHAR("WM/Lyrics_Synchronised")
g_wszWMOriginalLyricist = WCHAR("WM/OriginalLyricist")
g_wszWMOriginalArtist = WCHAR("WM/OriginalArtist")
g_wszWMOriginalAlbumTitle = WCHAR("WM/OriginalAlbumTitle")
g_wszWMOriginalReleaseYear = WCHAR("WM/OriginalReleaseYear")
g_wszWMOriginalFilename = WCHAR("WM/OriginalFilename")
g_wszWMPublisher = WCHAR("WM/Publisher")
g_wszWMEncodedBy = WCHAR("WM/EncodedBy")
g_wszWMEncodingSettings = WCHAR("WM/EncodingSettings")
g_wszWMEncodingTime = WCHAR("WM/EncodingTime")
g_wszWMAuthorURL = WCHAR("WM/AuthorUR")
g_wszWMUserWebURL = WCHAR("WM/UserWebUR")
g_wszWMAudioFileURL = WCHAR("WM/AudioFileUR")
g_wszWMAudioSourceURL = WCHAR("WM/AudioSourceUR")
g_wszWMLanguage = WCHAR("WM/Language")
g_wszWMParentalRating = WCHAR("WM/ParentalRating")
g_wszWMBeatsPerMinute = WCHAR("WM/BeatsPerMinute")
g_wszWMInitialKey = WCHAR("WM/InitialKey")
g_wszWMMood = WCHAR("WM/Mood")
g_wszWMText = WCHAR("WM/Text")
g_wszWMDVDID = WCHAR("WM/DVDID")
g_wszWMWMContentID = WCHAR("WM/WMContentID")
g_wszWMWMCollectionID = WCHAR("WM/WMCollectionID")
g_wszWMWMCollectionGroupID = WCHAR("WM/WMCollectionGroupID")
g_wszWMUniqueFileIdentifier = WCHAR("WM/UniqueFileIdentifier")
g_wszWMModifiedBy = WCHAR("WM/ModifiedBy")
g_wszWMRadioStationName = WCHAR("WM/RadioStationName")
g_wszWMRadioStationOwner = WCHAR("WM/RadioStationOwner")
g_wszWMPlaylistDelay = WCHAR("WM/PlaylistDelay")
g_wszWMCodec = WCHAR("WM/Codec")
g_wszWMDRM = WCHAR("WM/DRM")
g_wszWMISRC = WCHAR("WM/ISRC")
g_wszWMProvider = WCHAR("WM/Provider")
g_wszWMProviderRating = WCHAR("WM/ProviderRating")
g_wszWMProviderStyle = WCHAR("WM/ProviderStyle")
g_wszWMContentDistributor = WCHAR("WM/ContentDistributor")
g_wszWMSubscriptionContentID = WCHAR("WM/SubscriptionContentID")
g_wszWMWMADRCPeakReference = WCHAR("WM/WMADRCPeakReference")
g_wszWMWMADRCPeakTarget = WCHAR("WM/WMADRCPeakTarget")
g_wszWMWMADRCAverageReference = WCHAR("WM/WMADRCAverageReference")
g_wszWMWMADRCAverageTarget = WCHAR("WM/WMADRCAverageTarget")

# ////////////////////////////////////////////////////////////////
# //
# // Attributes introduced in V10
# //
g_wszWMStreamTypeInfo = WCHAR("WM/StreamTypeInfo")
g_wszWMPeakBitrate = WCHAR("WM/PeakBitrate")
g_wszWMASFPacketCount = WCHAR("WM/ASFPacketCount")
g_wszWMASFSecurityObjectsSize = WCHAR("WM/ASFSecurityObjectsSize")
g_wszWMSharedUserRating = WCHAR("WM/SharedUserRating")
g_wszWMSubTitleDescription = WCHAR("WM/SubTitleDescription")
g_wszWMMediaCredits = WCHAR("WM/MediaCredits")
g_wszWMParentalRatingReason = WCHAR("WM/ParentalRatingReason")
g_wszWMOriginalReleaseTime = WCHAR("WM/OriginalReleaseTime")
g_wszWMMediaStationCallSign = WCHAR("WM/MediaStationCallSign")
g_wszWMMediaStationName = WCHAR("WM/MediaStationName")
g_wszWMMediaNetworkAffiliation = WCHAR("WM/MediaNetworkAffiliation")
g_wszWMMediaOriginalChannel = WCHAR("WM/MediaOriginalChannel")
g_wszWMMediaOriginalBroadcastDateTime = WCHAR(
    "WM/MediaOriginalBroadcastDateTime"
)
g_wszWMMediaIsStereo = WCHAR("WM/MediaIsStereo")
g_wszWMVideoClosedCaptioning = WCHAR("WM/VideoClosedCaptioning")
g_wszWMMediaIsRepeat = WCHAR("WM/MediaIsRepeat")
g_wszWMMediaIsLive = WCHAR("WM/MediaIsLive")
g_wszWMMediaIsTape = WCHAR("WM/MediaIsTape")
g_wszWMMediaIsDelay = WCHAR("WM/MediaIsDelay")
g_wszWMMediaIsSubtitled = WCHAR("WM/MediaIsSubtitled")
g_wszWMMediaIsPremiere = WCHAR("WM/MediaIsPremiere")
g_wszWMMediaIsFinale = WCHAR("WM/MediaIsFinale")
g_wszWMMediaIsSAP = WCHAR("WM/MediaIsSAP")
g_wszWMProviderCopyright = WCHAR("WM/ProviderCopyright")

# ////////////////////////////////////////////////////////////////
# //
# // Attributes introduced in V11
# //
g_wszWMISAN = WCHAR("WM/ISAN")
g_wszWMADID = WCHAR("WM/ADID")
g_wszWMWMShadowFileSourceFileType = WCHAR("WM/WMShadowFileSourceFileType")
g_wszWMWMShadowFileSourceDRMType = WCHAR("WM/WMShadowFileSourceDRMType")
g_wszWMWMCPDistributor = WCHAR("WM/WMCPDistributor")
g_wszWMWMCPDistributorID = WCHAR("WM/WMCPDistributorID")
g_wszWMSeasonNumber = WCHAR("WM/SeasonNumber")
g_wszWMEpisodeNumber = WCHAR("WM/EpisodeNumber")

# ////////////////////////////////////////////////////////////////
# //
# // These are setting names for use in Get/SetOutputSetting
# //
g_wszEarlyDataDelivery = WCHAR("EarlyDataDelivery")
g_wszJustInTimeDecode = WCHAR("JustInTimeDecode")
g_wszSingleOutputBuffer = WCHAR("SingleOutputBuffer")
g_wszSoftwareScaling = WCHAR("SoftwareScaling")
g_wszDeliverOnReceive = WCHAR("DeliverOnReceive")
g_wszScrambledAudio = WCHAR("ScrambledAudio")
g_wszDedicatedDeliveryThread = WCHAR("DedicatedDeliveryThread")
g_wszEnableDiscreteOutput = WCHAR("EnableDiscreteOutput")
g_wszSpeakerConfig = WCHAR("SpeakerConfig")
g_wszDynamicRangeControl = WCHAR("DynamicRangeControl")
g_wszAllowInterlacedOutput = WCHAR("AllowInterlacedOutput")
g_wszVideoSampleDurations = WCHAR("VideoSampleDurations")
g_wszStreamLanguage = WCHAR("StreamLanguage")
g_wszEnableWMAProSPDIFOutput = WCHAR("EnableWMAProSPDIFOutput")

# ////////////////////////////////////////////////////////////////
# //
# // These are setting names for use in Get/SetInputSetting
# //
g_wszDeinterlaceMode = WCHAR("DeinterlaceMode")
g_wszInitialPatternForInverseTelecine = WCHAR(
    "InitialPatternForInverseTelecine"
)
g_wszJPEGCompressionQuality = WCHAR("JPEGCompressionQuality")
g_wszWatermarkCLSID = WCHAR("WatermarkCLSID")
g_wszWatermarkConfig = WCHAR("WatermarkConfig")
g_wszInterlacedCoding = WCHAR("InterlacedCoding")
g_wszFixedFrameRate = WCHAR("FixedFrameRate")

# ////////////////////////////////////////////////////////////////
# //
# // All known IWMPropertyVault property names
# //
# // g_wszOriginalSourceFormatTag is obsolete and has been
# // superceded by g_wszOriginalWaveFormat
g_wszOriginalSourceFormatTag = WCHAR("_SOURCEFORMATTAG")
g_wszOriginalWaveFormat = WCHAR("_ORIGINALWAVEFORMAT")
g_wszEDL = WCHAR("_ED")
g_wszComplexity = WCHAR("_COMPLEXITYEX")
g_wszDecoderComplexityRequested = WCHAR("_DECODERCOMPLEXITYPROFILE")

# ////////////////////////////////////////////////////////////////
# //
# // All known IWMIStreamProps property names
# //
g_wszReloadIndexOnSeek = WCHAR("ReloadIndexOnSeek")
g_wszStreamNumIndexObjects = WCHAR("StreamNumIndexObjects")
g_wszFailSeekOnError = WCHAR("FailSeekOnError")
g_wszPermitSeeksBeyondEndOfStream = WCHAR("PermitSeeksBeyondEndOfStream")
g_wszUsePacketAtSeekPoint = WCHAR("UsePacketAtSeekPoint")
g_wszSourceBufferTime = WCHAR("SourceBufferTime")
g_wszSourceMaxBytesAtOnce = WCHAR("SourceMaxBytesAtOnce")

# ////////////////////////////////////////////////////////////////
# //
# // VBR encoding settings
# //
g_wszVBREnabled = WCHAR("_VBRENABLED")
g_wszVBRQuality = WCHAR("_VBRQUALITY")
g_wszVBRBitrateMax = WCHAR("_RMAX")
g_wszVBRBufferWindowMax = WCHAR("_BMAX")

# ////////////////////////////////////////////////////////////////
# //
# // VBR Video settings
# //
g_wszVBRPeak = WCHAR("VBR Peak")
g_wszBufferAverage = WCHAR("Buffer Average")

# ////////////////////////////////////////////////////////////////
# //
# // Codec encoding complexity settings
# //
# // g_wszComplexity should be used to set desired encoding complexity on the
# // stream's IWMPropertyVault (see above for definition)
# // The below settings can be queried from IWMCodecInfo3::GetCodecProp()
# //
g_wszComplexityMax = WCHAR("_COMPLEXITYEXMAX")
g_wszComplexityOffline = WCHAR("_COMPLEXITYEXOFFLINE")
g_wszComplexityLive = WCHAR("_COMPLEXITYEXLIVE")
g_wszIsVBRSupported = WCHAR("_ISVBRSUPPORTED")

# ////////////////////////////////////////////////////////////////
# //
# // Codec enumeration settings
# //
# // g_wszVBREnabled can be used as a codec enumeration
# // setting (see above for definition)
g_wszNumPasses = WCHAR("_PASSESUSED")

# ////////////////////////////////////////////////////////////////
# //
# // These are WMA Voice V9 attribute names and values
# //
g_wszMusicSpeechClassMode = WCHAR("MusicSpeechClassMode")
g_wszMusicClassMode = WCHAR("MusicClassMode")
g_wszSpeechClassMode = WCHAR("SpeechClassMode")
g_wszMixedClassMode = WCHAR("MixedClassMode")

# ////////////////////////////////////////////////////////////////
# //
# // The WMA Voice V9 supports the following format property.
# //
g_wszSpeechCaps = WCHAR("SpeechFormatCap")

# ////////////////////////////////////////////////////////////////
# //
# // Multi-channel WMA properties
# //
g_wszPeakValue = WCHAR("PeakValue")
g_wszAverageLevel = WCHAR("AverageLevel")
g_wszFold6To2Channels3 = WCHAR("Fold6To2Channels3")
g_wszFoldToChannelsTemplate = WCHAR("Fold%luTo%luChannels%lu")

# ////////////////////////////////////////////////////////////////
# //
# // Complexity profile description strings
# //
g_wszDeviceConformanceTemplate = WCHAR("DeviceConformanceTemplate")

# ////////////////////////////////////////////////////////////////
# //
# // Frame interpolation on video decode
# //
g_wszEnableFrameInterpolation = WCHAR("EnableFrameInterpolation")

# ////////////////////////////////////////////////////////////////
# //
# // Needs previous sample for Delta frame on video decode
# //
g_wszNeedsPreviousSample = WCHAR("NeedsPreviousSample")

# ////////////////////////////////////////////////////////////////
# //
# // Corresponds to iTunes Compilation flag
# //
g_wszWMIsCompilation = WCHAR("WM/IsCompilation")


WM_START_CURRENTPOSITION = QWORD - 1
WM_BACKUP_OVERWRITE = DWORD(0x00000001)
WM_RESTORE_INDIVIDUALIZE = DWORD(0x00000002)
WAVE_FORMAT_DRM = 0x0009
LPCWSTR_WMSDK_TYPE_SAFE = LPCWSTR
WMT_VIDEOIMAGE_SAMPLE_INPUT_FRAME = 1 # sample has input frame
WMT_VIDEOIMAGE_SAMPLE_OUTPUT_FRAME = 2 # sample produces output frame
WMT_VIDEOIMAGE_SAMPLE_USES_CURRENT_INPUT_FRAME = 4
WMT_VIDEOIMAGE_SAMPLE_USES_PREVIOUS_INPUT_FRAME = 8
WMT_VIDEOIMAGE_SAMPLE_MOTION = 1 # acef used (includes resizing)
WMT_VIDEOIMAGE_SAMPLE_ROTATION = 2 # bd also used (not valid without acef)
WMT_VIDEOIMAGE_SAMPLE_BLENDING = 4 # BlendCoef1 used
WMT_VIDEOIMAGE_SAMPLE_ADV_BLENDING = 8 # BlendCoef2 also used (not valid without BlendCoef1)
WMT_VIDEOIMAGE_INTEGER_DENOMINATOR = 65536
WMT_VIDEOIMAGE_MAGIC_NUMBER = 0x1d4a45f2
WMT_VIDEOIMAGE_MAGIC_NUMBER_2 = 0x1d4a45f3
WMT_VIDEOIMAGE_TRANSITION_BOW_TIE = 11
WMT_VIDEOIMAGE_TRANSITION_CIRCLE = 12
WMT_VIDEOIMAGE_TRANSITION_CROSS_FADE = 13
WMT_VIDEOIMAGE_TRANSITION_DIAGONAL = 14
WMT_VIDEOIMAGE_TRANSITION_DIAMOND = 15
WMT_VIDEOIMAGE_TRANSITION_FADE_TO_COLOR = 16
WMT_VIDEOIMAGE_TRANSITION_FILLED_V = 17
WMT_VIDEOIMAGE_TRANSITION_FLIP = 18
WMT_VIDEOIMAGE_TRANSITION_INSET = 19
WMT_VIDEOIMAGE_TRANSITION_IRIS = 20
WMT_VIDEOIMAGE_TRANSITION_PAGE_ROLL = 21
WMT_VIDEOIMAGE_TRANSITION_RECTANGLE = 23
WMT_VIDEOIMAGE_TRANSITION_REVEAL = 24
WMT_VIDEOIMAGE_TRANSITION_SLIDE = 27
WMT_VIDEOIMAGE_TRANSITION_SPLIT = 29
WMT_VIDEOIMAGE_TRANSITION_STAR = 30
WMT_VIDEOIMAGE_TRANSITION_WHEEL = 31
WM_SampleExtension_ContentType_Size = 1
WM_SampleExtension_PixelAspectRatio_Size = 2
WM_SampleExtension_Timecode_Size = 14
WM_SampleExtension_SampleDuration_Size = 2
WM_SampleExtension_ChromaLocation_Size = 1
WM_SampleExtension_ColorSpaceInfo_Size = 3
WM_CT_REPEAT_FIRST_FIELD = 0x10
WM_CT_BOTTOM_FIELD_FIRST = 0x20
WM_CT_TOP_FIELD_FIRST = 0x40
WM_CT_INTERLACED = 0x80
WM_CL_INTERLACED420 = 0
WM_CL_PROGRESSIVE420 = 1
WM_MAX_VIDEO_STREAMS = 0x3f
WM_MAX_STREAMS = 0x3f


class __MIDL___MIDL_itf_wmsdkidl_0000_0000_0001(enum):
    WEBSTREAM_SAMPLE_TYPE_FILE = 0x1
    WEBSTREAM_SAMPLE_TYPE_RENDER = 0x2


class __MIDL___MIDL_itf_wmsdkidl_0000_0000_0002(enum):
    WM_SF_CLEANPOINT = 0x1
    WM_SF_DISCONTINUITY = 0x2
    WM_SF_DATALOSS = 0x4


class __MIDL___MIDL_itf_wmsdkidl_0000_0000_0003(enum):
    WM_SFEX_NOTASYNCPOINT = 0x2
    WM_SFEX_DATALOSS = 0x4


class WMT_STATUS(enum):
    WMT_ERROR = 0x0
    WMT_OPENED = 0x1
    WMT_BUFFERING_START = 0x2
    WMT_BUFFERING_STOP = 0x3
    WMT_EOF = 0x4
    WMT_END_OF_FILE = 0x4
    WMT_END_OF_SEGMENT = 0x5
    WMT_END_OF_STREAMING = 0x6
    WMT_LOCATING = 0x7
    WMT_CONNECTING = 0x8
    WMT_NO_RIGHTS = 0x9
    WMT_MISSING_CODEC = 0xA
    WMT_STARTED = 0xB
    WMT_STOPPED = 0xC
    WMT_CLOSED = 0xD
    WMT_STRIDING = 0xE
    WMT_TIMER = 0xF
    WMT_INDEX_PROGRESS = 0x10
    WMT_SAVEAS_START = 0x11
    WMT_SAVEAS_STOP = 0x12
    WMT_NEW_SOURCEFLAGS = 0x13
    WMT_NEW_METADATA = 0x14
    WMT_BACKUPRESTORE_BEGIN = 0x15
    WMT_SOURCE_SWITCH = 0x16
    WMT_ACQUIRE_LICENSE = 0x17
    WMT_INDIVIDUALIZE = 0x18
    WMT_NEEDS_INDIVIDUALIZATION = 0x19
    WMT_NO_RIGHTS_EX = 0x1A
    WMT_BACKUPRESTORE_END = 0x1B
    WMT_BACKUPRESTORE_CONNECTING = 0x1C
    WMT_BACKUPRESTORE_DISCONNECTING = 0x1D
    WMT_ERROR_WITHURL = 0x1E
    WMT_RESTRICTED_LICENSE = 0x1F
    WMT_CLIENT_CONNECT = 0x20
    WMT_CLIENT_DISCONNECT = 0x21
    WMT_NATIVE_OUTPUT_PROPS_CHANGED = 0x22
    WMT_RECONNECT_START = 0x23
    WMT_RECONNECT_END = 0x24
    WMT_CLIENT_CONNECT_EX = 0x25
    WMT_CLIENT_DISCONNECT_EX = 0x26
    WMT_SET_FEC_SPAN = 0x27
    WMT_PREROLL_READY = 0x28
    WMT_PREROLL_COMPLETE = 0x29
    WMT_CLIENT_PROPERTIES = 0x2A
    WMT_LICENSEURL_SIGNATURE_STATE = 0x2B
    WMT_INIT_PLAYLIST_BURN = 0x2C
    WMT_TRANSCRYPTOR_INIT = 0x2D
    WMT_TRANSCRYPTOR_SEEKED = 0x2E
    WMT_TRANSCRYPTOR_READ = 0x2F
    WMT_TRANSCRYPTOR_CLOSED = 0x30
    WMT_PROXIMITY_RESULT = 0x31
    WMT_PROXIMITY_COMPLETED = 0x32
    WMT_CONTENT_ENABLER = 0x33


class WMT_STREAM_SELECTION(enum):
    WMT_OFF = 0x0
    WMT_CLEANPOINT_ONLY = 0x1
    WMT_ON = 0x2


class WMT_IMAGE_TYPE(enum):
    WMT_IT_NONE = 0x0
    WMT_IT_BITMAP = 0x1
    WMT_IT_JPEG = 0x2
    WMT_IT_GIF = 0x3


class WMT_ATTR_DATATYPE(enum):
    WMT_TYPE_DWORD = 0x0
    WMT_TYPE_STRING = 0x1
    WMT_TYPE_BINARY = 0x2
    WMT_TYPE_BOOL = 0x3
    WMT_TYPE_QWORD = 0x4
    WMT_TYPE_WORD = 0x5
    WMT_TYPE_GUID = 0x6


class WMT_ATTR_IMAGETYPE(enum):
    WMT_IMAGETYPE_BITMAP = 0x1
    WMT_IMAGETYPE_JPEG = 0x2
    WMT_IMAGETYPE_GIF = 0x3


class WMT_VERSION(enum):
    WMT_VER_4_0 = 0x40000
    WMT_VER_7_0 = 0x70000
    WMT_VER_8_0 = 0x80000
    WMT_VER_9_0 = 0x90000


class tagWMT_STORAGE_FORMAT(enum):
    WMT_Storage_Format_MP3 = 0x0
    WMT_Storage_Format_V1 = 0x1


class tagWMT_DRMLA_TRUST(enum):
    WMT_DRMLA_UNTRUSTED = 0x0
    WMT_DRMLA_TRUSTED = 0x1
    WMT_DRMLA_TAMPERED = 0x2


class tagWMT_TRANSPORT_TYPE(enum):
    WMT_Transport_Type_Unreliable = 0x0
    WMT_Transport_Type_Reliable = 0x1


class WMT_NET_PROTOCOL(enum):
    WMT_PROTOCOL_HTTP = 0x0


class WMT_PLAY_MODE(enum):
    WMT_PLAY_MODE_AUTOSELECT = 0x0
    WMT_PLAY_MODE_LOCAL = 0x1
    WMT_PLAY_MODE_DOWNLOAD = 0x2
    WMT_PLAY_MODE_STREAMING = 0x3


class WMT_PROXY_SETTINGS(enum):
    WMT_PROXY_SETTING_NONE = 0x0
    WMT_PROXY_SETTING_MANUAL = 0x1
    WMT_PROXY_SETTING_AUTO = 0x2
    WMT_PROXY_SETTING_BROWSER = 0x3
    WMT_PROXY_SETTING_MAX = 0x4


class WMT_CODEC_INFO_TYPE(enum):
    WMT_CODECINFO_AUDIO = 0x0
    WMT_CODECINFO_VIDEO = 0x1
    WMT_CODECINFO_UNKNOWN = 0xFFFFFFFF


class __MIDL___MIDL_itf_wmsdkidl_0000_0000_0004(enum):
    WM_DM_NOTINTERLACED = 0x0
    WM_DM_DEINTERLACE_NORMAL = 0x1
    WM_DM_DEINTERLACE_HALFSIZE = 0x2
    WM_DM_DEINTERLACE_HALFSIZEDOUBLERATE = 0x3
    WM_DM_DEINTERLACE_INVERSETELECINE = 0x4
    WM_DM_DEINTERLACE_VERTICALHALFSIZEDOUBLERATE = 0x5


class __MIDL___MIDL_itf_wmsdkidl_0000_0000_0005(enum):
    WM_DM_IT_DISABLE_COHERENT_MODE = 0x0
    WM_DM_IT_FIRST_FRAME_IN_CLIP_IS_AA_TOP = 0x1
    WM_DM_IT_FIRST_FRAME_IN_CLIP_IS_BB_TOP = 0x2
    WM_DM_IT_FIRST_FRAME_IN_CLIP_IS_BC_TOP = 0x3
    WM_DM_IT_FIRST_FRAME_IN_CLIP_IS_CD_TOP = 0x4
    WM_DM_IT_FIRST_FRAME_IN_CLIP_IS_DD_TOP = 0x5
    WM_DM_IT_FIRST_FRAME_IN_CLIP_IS_AA_BOTTOM = 0x6
    WM_DM_IT_FIRST_FRAME_IN_CLIP_IS_BB_BOTTOM = 0x7
    WM_DM_IT_FIRST_FRAME_IN_CLIP_IS_BC_BOTTOM = 0x8
    WM_DM_IT_FIRST_FRAME_IN_CLIP_IS_CD_BOTTOM = 0x9
    WM_DM_IT_FIRST_FRAME_IN_CLIP_IS_DD_BOTTOM = 0xA


class tagWMT_OFFSET_FORMAT(enum):
    WMT_OFFSET_FORMAT_100NS = 0x0
    WMT_OFFSET_FORMAT_FRAME_NUMBERS = 0x1
    WMT_OFFSET_FORMAT_PLAYLIST_OFFSET = 0x2
    WMT_OFFSET_FORMAT_TIMECODE = 0x3
    WMT_OFFSET_FORMAT_100NS_APPROXIMATE = 0x4


class tagWMT_INDEXER_TYPE(enum):
    WMT_IT_PRESENTATION_TIME = 0x0
    WMT_IT_FRAME_NUMBERS = 0x1
    WMT_IT_TIMECODE = 0x2


class tagWMT_INDEX_TYPE(enum):
    WMT_IT_NEAREST_DATA_UNIT = 0x1
    WMT_IT_NEAREST_OBJECT = 0x2
    WMT_IT_NEAREST_CLEAN_POINT = 0x3


class tagWMT_FILESINK_MODE(enum):
    WMT_FM_SINGLE_BUFFERS = 0x1
    WMT_FM_FILESINK_DATA_UNITS = 0x2
    WMT_FM_FILESINK_UNBUFFERED = 0x4


class tagWMT_MUSICSPEECH_CLASS_MODE(enum):
    WMT_MS_CLASS_MUSIC = 0x0
    WMT_MS_CLASS_SPEECH = 0x1
    WMT_MS_CLASS_MIXED = 0x2


class tagWMT_WATERMARK_ENTRY_TYPE(enum):
    WMT_WMETYPE_AUDIO = 0x1
    WMT_WMETYPE_VIDEO = 0x2


class __MIDL___MIDL_itf_wmsdkidl_0000_0000_0006(enum):
    WM_PLAYBACK_DRC_HIGH = 0x0
    WM_PLAYBACK_DRC_MEDIUM = 0x1
    WM_PLAYBACK_DRC_LOW = 0x2


class __MIDL___MIDL_itf_wmsdkidl_0000_0000_0007(enum):
    WMT_TIMECODE_FRAMERATE_30 = 0x0
    WMT_TIMECODE_FRAMERATE_30DROP = 0x1
    WMT_TIMECODE_FRAMERATE_25 = 0x2
    WMT_TIMECODE_FRAMERATE_24 = 0x3


class WMT_CREDENTIAL_FLAGS(enum):
    WMT_CREDENTIAL_SAVE = 0x1
    WMT_CREDENTIAL_DONT_CACHE = 0x2
    WMT_CREDENTIAL_CLEAR_TEXT = 0x4
    WMT_CREDENTIAL_PROXY = 0x8
    WMT_CREDENTIAL_ENCRYPT = 0x10


class WM_AETYPE(enum):
    WM_AETYPE_INCLUDE = 0x69
    WM_AETYPE_EXCLUDE = 0x65


WMMEDIASUBTYPE_Base = EXTERN_GUID(
    0x00000000,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIATYPE_Video = EXTERN_GUID(
    0x73646976,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_RGB1 = EXTERN_GUID(
    0xE436EB78,
    0x524F,
    0x11CE,
    0x9F,
    0x53,
    0x00,
    0x20,
    0xAF,
    0x0B,
    0xA7,
    0x70
)
WMMEDIASUBTYPE_RGB4 = EXTERN_GUID(
    0xE436EB79,
    0x524F,
    0x11CE,
    0x9F,
    0x53,
    0x00,
    0x20,
    0xAF,
    0x0B,
    0xA7,
    0x70
)
WMMEDIASUBTYPE_RGB8 = EXTERN_GUID(
    0xE436EB7A,
    0x524F,
    0x11CE,
    0x9F,
    0x53,
    0x00,
    0x20,
    0xAF,
    0x0B,
    0xA7,
    0x70
)
WMMEDIASUBTYPE_RGB565 = EXTERN_GUID(
    0xE436EB7B,
    0x524F,
    0x11CE,
    0x9F,
    0x53,
    0x00,
    0x20,
    0xAF,
    0x0B,
    0xA7,
    0x70
)
WMMEDIASUBTYPE_RGB555 = EXTERN_GUID(
    0xE436EB7C,
    0x524F,
    0x11CE,
    0x9F,
    0x53,
    0x00,
    0x20,
    0xAF,
    0x0B,
    0xA7,
    0x70
)
WMMEDIASUBTYPE_RGB24 = EXTERN_GUID(
    0xE436EB7D,
    0x524F,
    0x11CE,
    0x9F,
    0x53,
    0x00,
    0x20,
    0xAF,
    0x0B,
    0xA7,
    0x70
)
WMMEDIASUBTYPE_RGB32 = EXTERN_GUID(
    0xE436EB7E,
    0x524F,
    0x11CE,
    0x9F,
    0x53,
    0x00,
    0x20,
    0xAF,
    0x0B,
    0xA7,
    0x70
)
WMMEDIASUBTYPE_I420 = EXTERN_GUID(
    0x30323449,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_IYUV = EXTERN_GUID(
    0x56555949,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_YV12 = EXTERN_GUID(
    0x32315659,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_YUY2 = EXTERN_GUID(
    0x32595559,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_P422 = EXTERN_GUID(
    0x32323450,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_UYVY = EXTERN_GUID(
    0x59565955,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_YVYU = EXTERN_GUID(
    0x55595659,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_YVU9 = EXTERN_GUID(
    0x39555659,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_VIDEOIMAGE = EXTERN_GUID(
    0x1D4A45F2,
    0xE5F6,
    0x4B44,
    0x83,
    0x88,
    0xF0,
    0xAE,
    0x5C,
    0x0E,
    0x0C,
    0x37
)
WMMEDIASUBTYPE_MP43 = EXTERN_GUID(
    0x3334504D,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_MP4S = EXTERN_GUID(
    0x5334504D,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_M4S2 = EXTERN_GUID(
    0x3253344D,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMV1 = EXTERN_GUID(
    0x31564D57,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMV2 = EXTERN_GUID(
    0x32564D57,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_MSS1 = EXTERN_GUID(
    0x3153534D,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_MPEG2_VIDEO = EXTERN_GUID(
    0xE06D8026,
    0xDB46,
    0x11CF,
    0xB4,
    0xD1,
    0x00,
    0x80,
    0x5F,
    0x6C,
    0xBB,
    0xEA
)
WMMEDIATYPE_Audio = EXTERN_GUID(
    0x73647561,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_PCM = EXTERN_GUID(
    0x00000001,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_DRM = EXTERN_GUID(
    0x00000009,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMAudioV9 = EXTERN_GUID(
    0x00000162,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMAudio_Lossless = EXTERN_GUID(
    0x00000163,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_MSS2 = EXTERN_GUID(
    0x3253534D,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMSP1 = EXTERN_GUID(
    0x0000000A,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMSP2 = EXTERN_GUID(
    0x0000000B,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMV3 = EXTERN_GUID(
    0x33564D57,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMVP = EXTERN_GUID(
    0x50564D57,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WVP2 = EXTERN_GUID(
    0x32505657,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMVA = EXTERN_GUID(
    0x41564D57,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WVC1 = EXTERN_GUID(
    0x31435657,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMAudioV8 = EXTERN_GUID(
    0x00000161,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMAudioV7 = EXTERN_GUID(
    0x00000161,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WMAudioV2 = EXTERN_GUID(
    0x00000161,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_ACELPnet = EXTERN_GUID(
    0x00000130,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_MP3 = EXTERN_GUID(
    0x00000055,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIASUBTYPE_WebStream = EXTERN_GUID(
    0x776257D4,
    0xC627,
    0x41CB,
    0x8F,
    0x81,
    0x7A,
    0xC7,
    0xFF,
    0x1C,
    0x40,
    0xCC
)
WMMEDIATYPE_Script = EXTERN_GUID(
    0x73636D64,
    0x0000,
    0x0010,
    0x80,
    0x00,
    0x00,
    0xAA,
    0x00,
    0x38,
    0x9B,
    0x71
)
WMMEDIATYPE_Image = EXTERN_GUID(
    0x34A50FD8,
    0x8AA5,
    0x4386,
    0x81,
    0xFE,
    0xA0,
    0xEF,
    0xE0,
    0x48,
    0x8E,
    0x31
)
WMMEDIATYPE_FileTransfer = EXTERN_GUID(
    0xD9E47579,
    0x930E,
    0x4427,
    0xAD,
    0xFC,
    0xAD,
    0x80,
    0xF2,
    0x90,
    0xE4,
    0x70
)
WMMEDIATYPE_Text = EXTERN_GUID(
    0x9BBA1EA7,
    0x5AB2,
    0x4829,
    0xBA,
    0x57,
    0x9,
    0x40,
    0x20,
    0x9B,
    0xCF,
    0x3E
)
WMFORMAT_VideoInfo = EXTERN_GUID(
    0x05589F80,
    0xC356,
    0x11CE,
    0xBF,
    0x01,
    0x00,
    0xAA,
    0x00,
    0x55,
    0x59,
    0x5A
)
WMFORMAT_MPEG2Video = EXTERN_GUID(
    0xE06D80E3,
    0xDB46,
    0x11CF,
    0xB4,
    0xD1,
    0x00,
    0x80,
    0x05F,
    0x6C,
    0xBB,
    0xEA
)
WMFORMAT_WaveFormatEx = EXTERN_GUID(
    0x05589F81,
    0xC356,
    0x11CE,
    0xBF,
    0x01,
    0x00,
    0xAA,
    0x00,
    0x55,
    0x59,
    0x5A
)
WMFORMAT_Script = EXTERN_GUID(
    0x5C8510F2,
    0xDEBE,
    0x4CA7,
    0xBB,
    0xA5,
    0xF0,
    0x7A,
    0x10,
    0x4F,
    0x8D,
    0xFF
)
WMFORMAT_WebStream = EXTERN_GUID(
    0xDA1E6B13,
    0x8359,
    0x4050,
    0xB3,
    0x98,
    0x38,
    0x8E,
    0x96,
    0x5B,
    0xF0,
    0x0C
)
WMSCRIPTTYPE_TwoStrings = EXTERN_GUID(
    0x82F38A70,
    0xC29F,
    0x11D1,
    0x97,
    0xAD,
    0x00,
    0xA0,
    0xC9,
    0x5E,
    0xA8,
    0x50
)
WM_SampleExtensionGUID_OutputCleanPoint = EXTERN_GUID(
    0xF72A3C6F,
    0x6EB4,
    0x4EBC,
    0xB1,
    0x92,
    0x9,
    0xAD,
    0x97,
    0x59,
    0xE8,
    0x28
)
WM_SampleExtensionGUID_Timecode = EXTERN_GUID(
    0x399595EC,
    0x8667,
    0x4E2D,
    0x8F,
    0xDB,
    0x98,
    0x81,
    0x4C,
    0xE7,
    0x6C,
    0x1E
)
WM_SampleExtensionGUID_ChromaLocation = EXTERN_GUID(
    0x4C5ACCA0,
    0x9276,
    0x4B2C,
    0x9E,
    0x4C,
    0xA0,
    0xED,
    0xEF,
    0xDD,
    0x21,
    0x7E
)
WM_SampleExtensionGUID_ColorSpaceInfo = EXTERN_GUID(
    0xF79ADA56,
    0x30EB,
    0x4F2B,
    0x9F,
    0x7A,
    0xF2,
    0x4B,
    0x13,
    0x9A,
    0x11,
    0x57
)
WM_SampleExtensionGUID_UserDataInfo = EXTERN_GUID(
    0x732BB4FA,
    0x78BE,
    0x4549,
    0x99,
    0xBD,
    0x2,
    0xDB,
    0x1A,
    0x55,
    0xB7,
    0xA8
)
WM_SampleExtensionGUID_FileName = EXTERN_GUID(
    0xE165EC0E,
    0x19ED,
    0x45D7,
    0xB4,
    0xA7,
    0x25,
    0xCB,
    0xD1,
    0xE2,
    0x8E,
    0x9B
)
WM_SampleExtensionGUID_ContentType = EXTERN_GUID(
    0xD590DC20,
    0x07BC,
    0x436C,
    0x9C,
    0xF7,
    0xF3,
    0xBB,
    0xFB,
    0xF1,
    0xA4,
    0xDC
)
WM_SampleExtensionGUID_PixelAspectRatio = EXTERN_GUID(
    0x1B1EE554,
    0xF9EA,
    0x4BC8,
    0x82,
    0x1A,
    0x37,
    0x6B,
    0x74,
    0xE4,
    0xC4,
    0xB8
)
WM_SampleExtensionGUID_SampleDuration = EXTERN_GUID(
    0xC6BD9450,
    0x867F,
    0x4907,
    0x83,
    0xA3,
    0xC7,
    0x79,
    0x21,
    0xB7,
    0x33,
    0xAD
)
WM_SampleExtensionGUID_SampleProtectionSalt = EXTERN_GUID(
    0x5403DEEE,
    0xB9EE,
    0x438F,
    0xAA,
    0x83,
    0x38,
    0x4,
    0x99,
    0x7E,
    0x56,
    0x9D
)
IID_IWMMediaProps = EXTERN_GUID(
    0x96406BCE,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMVideoMediaProps = EXTERN_GUID(
    0x96406BCF,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMWriter = EXTERN_GUID(
    0x96406BD4,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMInputMediaProps = EXTERN_GUID(
    0x96406BD5,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMReader = EXTERN_GUID(
    0x96406BD6,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMSyncReader = EXTERN_GUID(
    0x9397F121,
    0x7705,
    0x4DC9,
    0xB0,
    0x49,
    0x98,
    0xB6,
    0x98,
    0x18,
    0x84,
    0x14
)
IID_IWMSyncReader2 = EXTERN_GUID(
    0xFAED3D21,
    0x1B6B,
    0x4AF7,
    0x8C,
    0xB6,
    0x3E,
    0x18,
    0x9B,
    0xBC,
    0x18,
    0x7B
)
IID_IWMOutputMediaProps = EXTERN_GUID(
    0x96406BD7,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMStatusCallback = EXTERN_GUID(
    0x6D7CDC70,
    0x9888,
    0x11D3,
    0x8E,
    0xDC,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x09,
    0xCF
)
IID_IWMReaderCallback = EXTERN_GUID(
    0x96406BD8,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMCredentialCallback = EXTERN_GUID(
    0x342E0EB7,
    0xE651,
    0x450C,
    0x97,
    0x5B,
    0x2A,
    0xCE,
    0x2C,
    0x90,
    0xC4,
    0x8E
)
IID_IWMMetadataEditor = EXTERN_GUID(
    0x96406BD9,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMMetadataEditor2 = EXTERN_GUID(
    0x203CFFE3,
    0x2E18,
    0x4FDF,
    0xB5,
    0x9D,
    0x6E,
    0x71,
    0x53,
    0x05,
    0x34,
    0xCF
)
IID_IWMDRMEditor = EXTERN_GUID(
    0xFF130EBC,
    0xA6C3,
    0x42A6,
    0xB4,
    0x01,
    0xC3,
    0x38,
    0x2C,
    0x3E,
    0x08,
    0xB3
)
IID_IWMHeaderInfo = EXTERN_GUID(
    0x96406BDA,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMHeaderInfo2 = EXTERN_GUID(
    0x15CF9781,
    0x454E,
    0x482E,
    0xB3,
    0x93,
    0x85,
    0xFA,
    0xE4,
    0x87,
    0xA8,
    0x10
)
IID_IWMHeaderInfo3 = EXTERN_GUID(
    0x15CC68E3,
    0x27CC,
    0x4ECD,
    0xB2,
    0x22,
    0x3F,
    0x5D,
    0x02,
    0xD8,
    0x0B,
    0xD5
)
IID_IWMProfileManager = EXTERN_GUID(
    0xD16679F2,
    0x6CA0,
    0x472D,
    0x8D,
    0x31,
    0x2F,
    0x5D,
    0x55,
    0xAE,
    0xE1,
    0x55
)
IID_IWMProfileManager2 = EXTERN_GUID(
    0x7A924E51,
    0x73C1,
    0x494D,
    0x80,
    0x19,
    0x23,
    0xD3,
    0x7E,
    0xD9,
    0xB8,
    0x9A
)
IID_IWMProfileManagerLanguage = EXTERN_GUID(
    0xBA4DCC78,
    0x7EE0,
    0x4AB8,
    0xB2,
    0x7A,
    0xDB,
    0xCE,
    0x8B,
    0xC5,
    0x14,
    0x54
)
IID_IWMProfile = EXTERN_GUID(
    0x96406BDB,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMProfile2 = EXTERN_GUID(
    0x07E72D33,
    0xD94E,
    0x4BE7,
    0x88,
    0x43,
    0x60,
    0xAE,
    0x5F,
    0xF7,
    0xE5,
    0xF5
)
IID_IWMProfile3 = EXTERN_GUID(
    0x00EF96CC,
    0xA461,
    0x4546,
    0x8B,
    0xCD,
    0xC9,
    0xA2,
    0x8F,
    0x0E,
    0x06,
    0xF5
)
IID_IWMStreamConfig = EXTERN_GUID(
    0x96406BDC,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMStreamConfig2 = EXTERN_GUID(
    0x7688D8CB,
    0xFC0D,
    0x43BD,
    0x94,
    0x59,
    0x5A,
    0x8D,
    0xEC,
    0x20,
    0x0C,
    0xFA
)
IID_IWMStreamConfig3 = EXTERN_GUID(
    0xCB164104,
    0x3AA9,
    0x45A7,
    0x9A,
    0xC9,
    0x4D,
    0xAE,
    0xE1,
    0x31,
    0xD6,
    0xE1
)
IID_IWMStreamList = EXTERN_GUID(
    0x96406BDD,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMMutualExclusion = EXTERN_GUID(
    0x96406BDE,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMMutualExclusion2 = EXTERN_GUID(
    0x302B57D,
    0x89D1,
    0x4BA2,
    0x85,
    0xC9,
    0x16,
    0x6F,
    0x2C,
    0x53,
    0xEB,
    0x91
)
IID_IWMBandwidthSharing = EXTERN_GUID(
    0xAD694AF1,
    0xF8D9,
    0x42F8,
    0xBC,
    0x47,
    0x70,
    0x31,
    0x1B,
    0x0C,
    0x4F,
    0x9E
)
IID_IWMStreamPrioritization = EXTERN_GUID(
    0x8C1C6090,
    0xF9A8,
    0x4748,
    0x8E,
    0xC3,
    0xDD,
    0x11,
    0x08,
    0xBA,
    0x1E,
    0x77
)
IID_IWMWriterAdvanced = EXTERN_GUID(
    0x96406BE3,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMWriterAdvanced2 = EXTERN_GUID(
    0x962DC1EC,
    0xC046,
    0x4DB8,
    0x9C,
    0xC7,
    0x26,
    0xCE,
    0xAE,
    0x50,
    0x08,
    0x17
)
IID_IWMWriterAdvanced3 = EXTERN_GUID(
    0x2CD6492D,
    0x7C37,
    0x4E76,
    0x9D,
    0x3B,
    0x59,
    0x26,
    0x11,
    0x83,
    0xA2,
    0x2E
)
IID_IWMWriterPreprocess = EXTERN_GUID(
    0xFC54A285,
    0x38C4,
    0x45B5,
    0xAA,
    0x23,
    0x85,
    0xB9,
    0xF7,
    0xCB,
    0x42,
    0x4B
)
IID_IWMWriterSink = EXTERN_GUID(
    0x96406BE4,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMWriterFileSink = EXTERN_GUID(
    0x96406BE5,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMWriterFileSink2 = EXTERN_GUID(
    0x14282BA7,
    0x4AEF,
    0x4205,
    0x8C,
    0xE5,
    0xC2,
    0x29,
    0x03,
    0x5A,
    0x05,
    0xBC
)
IID_IWMWriterFileSink3 = EXTERN_GUID(
    0x3FEA4FEB,
    0x2945,
    0x47A7,
    0xA1,
    0xDD,
    0xC5,
    0x3A,
    0x8F,
    0xC4,
    0xC4,
    0x5C
)
IID_IWMWriterNetworkSink = EXTERN_GUID(
    0x96406BE7,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMClientConnections = EXTERN_GUID(
    0x73C66010,
    0xA299,
    0x41DF,
    0xB1,
    0xF0,
    0xCC,
    0xF0,
    0x3B,
    0x09,
    0xC1,
    0xC6
)
IID_IWMClientConnections2 = EXTERN_GUID(
    0x4091571E,
    0x4701,
    0x4593,
    0xBB,
    0x3D,
    0xD5,
    0xF5,
    0xF0,
    0xC7,
    0x42,
    0x46
)
IID_IWMReaderAdvanced = EXTERN_GUID(
    0x96406BEA,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMReaderAdvanced2 = EXTERN_GUID(
    0xAE14A945,
    0xB90C,
    0x4D0D,
    0x91,
    0x27,
    0x80,
    0xD6,
    0x65,
    0xF7,
    0xD7,
    0x3E
)
IID_IWMReaderAdvanced3 = EXTERN_GUID(
    0x5DC0674B,
    0xF04B,
    0x4A4E,
    0x9F,
    0x2A,
    0xB1,
    0xAF,
    0xDE,
    0x2C,
    0x81,
    0x00
)
IID_IWMReaderAdvanced4 = EXTERN_GUID(
    0x945A76A2,
    0x12AE,
    0x4D48,
    0xBD,
    0x3C,
    0xCD,
    0x1D,
    0x90,
    0x39,
    0x9B,
    0x85
)
IID_IWMReaderAdvanced5 = EXTERN_GUID(
    0x24C44DB0,
    0x55D1,
    0x49AE,
    0xA5,
    0xCC,
    0xF1,
    0x38,
    0x15,
    0xE3,
    0x63,
    0x63
)
IID_IWMReaderAdvanced6 = EXTERN_GUID(
    0x18A2E7F8,
    0x428F,
    0x4ACD,
    0x8A,
    0x00,
    0xE6,
    0x46,
    0x39,
    0xBC,
    0x93,
    0xDE
)
IID_IWMPlayerHook = EXTERN_GUID(
    0xE5B7CA9A,
    0x0F1C,
    0x4F66,
    0x90,
    0x02,
    0x74,
    0xEC,
    0x50,
    0xD8,
    0xB3,
    0x04
)
IID_IWMDRMReader = EXTERN_GUID(
    0xD2827540,
    0x3EE7,
    0x432C,
    0xB1,
    0x4C,
    0xDC,
    0x17,
    0xF0,
    0x85,
    0xD3,
    0xB3
)
IID_IWMDRMReader2 = EXTERN_GUID(
    0xBEFE7A75,
    0x9F1D,
    0x4075,
    0xB9,
    0xD9,
    0xA3,
    0xC3,
    0x7B,
    0xDA,
    0x49,
    0xA0
)
IID_IWMDRMReader3 = EXTERN_GUID(
    0xE08672DE,
    0xF1E7,
    0x4FF4,
    0xA0,
    0xA3,
    0xFC,
    0x4B,
    0x08,
    0xE4,
    0xCA,
    0xF8
)
IID_IWMReaderPlaylistBurn = EXTERN_GUID(
    0xF28C0300,
    0x9BAA,
    0x4477,
    0xA8,
    0x46,
    0x17,
    0x44,
    0xD9,
    0xCB,
    0xF5,
    0x33
)
IID_IWMReaderCallbackAdvanced = EXTERN_GUID(
    0x96406BEB,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMReaderNetworkConfig = EXTERN_GUID(
    0x96406BEC,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMReaderStreamClock = EXTERN_GUID(
    0x96406BED,
    0x2B2B,
    0x11D3,
    0xB3,
    0x6B,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x08,
    0xFF
)
IID_IWMIndexer = EXTERN_GUID(
    0x6D7CDC71,
    0x9888,
    0x11D3,
    0x8E,
    0xDC,
    0x00,
    0xC0,
    0x4F,
    0x61,
    0x09,
    0xCF
)
IID_IWMIndexer2 = EXTERN_GUID(
    0xB70F1E42,
    0x6255,
    0x4DF0,
    0xA6,
    0xB9,
    0x02,
    0xB2,
    0x12,
    0xD9,
    0xE2,
    0xBB
)
IID_IWMReaderAllocatorEx = EXTERN_GUID(
    0x9F762FA7,
    0xA22E,
    0x428D,
    0x93,
    0xC9,
    0xAC,
    0x82,
    0xF3,
    0xAA,
    0xFE,
    0x5A
)
IID_IWMReaderTypeNegotiation = EXTERN_GUID(
    0xFDBE5592,
    0x81A1,
    0x41EA,
    0x93,
    0xBD,
    0x73,
    0x5C,
    0xAD,
    0x1A,
    0xDC,
    0x5
)
IID_IWMLicenseBackup = EXTERN_GUID(
    0x05E5AC9F,
    0x3FB6,
    0x4508,
    0xBB,
    0x43,
    0xA4,
    0x06,
    0x7B,
    0xA1,
    0xEB,
    0xE8
)
IID_IWMLicenseRestore = EXTERN_GUID(
    0xC70B6334,
    0xA22E,
    0x4EFB,
    0xA2,
    0x45,
    0x15,
    0xE6,
    0x5A,
    0x00,
    0x4A,
    0x13
)
IID_IWMBackupRestoreProps = EXTERN_GUID(
    0x3C8E0DA6,
    0x996F,
    0x4FF3,
    0xA1,
    0xAF,
    0x48,
    0x38,
    0xF9,
    0x37,
    0x7E,
    0x2E
)
IID_IWMPacketSize = EXTERN_GUID(
    0xCDFB97AB,
    0x188F,
    0x40B3,
    0xB6,
    0x43,
    0x5B,
    0x79,
    0x03,
    0x97,
    0x5C,
    0x59
)
IID_IWMPacketSize2 = EXTERN_GUID(
    0x8BFC2B9E,
    0xB646,
    0x4233,
    0xA8,
    0x77,
    0x1C,
    0x6A,
    0x7,
    0x96,
    0x69,
    0xDC
)
IID_IWMRegisterCallback = EXTERN_GUID(
    0xCF4B1F99,
    0x4DE2,
    0x4E49,
    0xA3,
    0x63,
    0x25,
    0x27,
    0x40,
    0xD9,
    0x9B,
    0xC1
)
IID_IWMWriterPostView = EXTERN_GUID(
    0x81E20CE4,
    0x75EF,
    0x491A,
    0x80,
    0x04,
    0xFC,
    0x53,
    0xC4,
    0x5B,
    0xDC,
    0x3E
)
IID_IWMWriterPostViewCallback = EXTERN_GUID(
    0xD9D6549D,
    0xA193,
    0x4F24,
    0xB3,
    0x08,
    0x03,
    0x12,
    0x3D,
    0x9B,
    0x7F,
    0x8D
)
IID_IWMCodecInfo = EXTERN_GUID(
    0xA970F41E,
    0x34DE,
    0x4A98,
    0xB3,
    0xBA,
    0xE4,
    0xB3,
    0xCA,
    0x75,
    0x28,
    0xF0
)
IID_IWMCodecInfo2 = EXTERN_GUID(
    0xAA65E273,
    0xB686,
    0x4056,
    0x91,
    0xEC,
    0xDD,
    0x76,
    0x8D,
    0x4D,
    0xF7,
    0x10
)
IID_IWMCodecInfo3 = EXTERN_GUID(
    0x7E51F487,
    0x4D93,
    0x4F98,
    0x8A,
    0xB4,
    0x27,
    0xD0,
    0x56,
    0x5A,
    0xDC,
    0x51
)
IID_IWMPropertyVault = EXTERN_GUID(
    0x72995A79,
    0x5090,
    0x42A4,
    0x9C,
    0x8C,
    0xD9,
    0xD0,
    0xB6,
    0xD3,
    0x4B,
    0xE5
)
IID_IWMIStreamProps = EXTERN_GUID(
    0x6816DAD3,
    0x2B4B,
    0x4C8E,
    0x81,
    0x49,
    0x87,
    0x4C,
    0x34,
    0x83,
    0xA7,
    0x53
)
IID_IWMLanguageList = EXTERN_GUID(
    0xDF683F00,
    0x2D49,
    0x4D8E,
    0x92,
    0xB7,
    0xFB,
    0x19,
    0xF6,
    0xA0,
    0xDC,
    0x57
)
IID_IWMDRMWriter = EXTERN_GUID(
    0xD6EA5DD0,
    0x12A0,
    0x43F4,
    0x90,
    0xAB,
    0xA3,
    0xFD,
    0x45,
    0x1E,
    0x6A,
    0x07
)
IID_IWMDRMWriter2 = EXTERN_GUID(
    0x38EE7A94,
    0x40E2,
    0x4E10,
    0xAA,
    0x3F,
    0x33,
    0xFD,
    0x32,
    0x10,
    0xED,
    0x5B
)
IID_IWMDRMWriter3 = EXTERN_GUID(
    0xA7184082,
    0xA4AA,
    0x4DDE,
    0xAC,
    0x9C,
    0xE7,
    0x5D,
    0xBD,
    0x11,
    0x17,
    0xCE
)
IID_IWMWriterPushSink = EXTERN_GUID(
    0xDC10E6A5,
    0x072C,
    0x467D,
    0xBF,
    0x57,
    0x63,
    0x30,
    0xA9,
    0xDD,
    0xE1,
    0x2A
)
IID_IWMReaderNetworkConfig2 = EXTERN_GUID(
    0xD979A853,
    0x042B,
    0x4050,
    0x83,
    0x87,
    0xC9,
    0x39,
    0xDB,
    0x22,
    0x01,
    0x3F
)
IID_IWMWatermarkInfo = EXTERN_GUID(
    0x6F497062,
    0xF2E2,
    0x4624,
    0x8E,
    0xA7,
    0x9D,
    0xD4,
    0x0D,
    0x81,
    0xFC,
    0x8D
)
IID_IWMReaderAccelerator = EXTERN_GUID(
    0xBDDC4D08,
    0x944D,
    0x4D52,
    0xA6,
    0x12,
    0x46,
    0xC3,
    0xFD,
    0xA0,
    0x7D,
    0xD4
)
IID_IWMReaderTimecode = EXTERN_GUID(
    0xF369E2F0,
    0xE081,
    0x4FE6,
    0x84,
    0x50,
    0xB8,
    0x10,
    0xB2,
    0xF4,
    0x10,
    0xD1
)
IID_IWMImageInfo = EXTERN_GUID(
    0x9F0AA3B6,
    0x7267,
    0x4D89,
    0x88,
    0xF2,
    0xBA,
    0x91,
    0x5A,
    0xA5,
    0xC4,
    0xC6
)
IID_IWMAddressAccess = EXTERN_GUID(
    0xBB3C6389,
    0x1633,
    0x4E92,
    0xAF,
    0x14,
    0x9F,
    0x31,
    0x73,
    0xBA,
    0x39,
    0xD0
)
IID_IWMAddressAccess2 = EXTERN_GUID(
    0x65A83FC2,
    0x3E98,
    0x4D4D,
    0x81,
    0xB5,
    0x2A,
    0x74,
    0x28,
    0x86,
    0xB3,
    0x3D
)
IID_IWMDeviceRegistration = EXTERN_GUID(
    0xF6211F03,
    0x8D21,
    0x4E94,
    0x93,
    0xE6,
    0x85,
    0x10,
    0x80,
    0x5F,
    0x2D,
    0x99
)
IID_IWMRegisteredDevice = EXTERN_GUID(
    0xA4503BEC,
    0x5508,
    0x4148,
    0x97,
    0xAC,
    0xBF,
    0xA7,
    0x57,
    0x60,
    0xA7,
    0x0D
)
IID_IWMProximityDetection = EXTERN_GUID(
    0x6A9FD8EE,
    0xB651,
    0x4BF0,
    0xB8,
    0x49,
    0x7D,
    0x4E,
    0xCE,
    0x79,
    0xA2,
    0xB1
)
IID_IWMDRMMessageParser = EXTERN_GUID(
    0xA73A0072,
    0x25A0,
    0x4C99,
    0xB4,
    0xA5,
    0xED,
    0xE8,
    0x10,
    0x1A,
    0x6C,
    0x39
)
IID_IWMDRMTranscryptor = EXTERN_GUID(
    0x69059850,
    0x6E6F,
    0x4BB2,
    0x80,
    0x6F,
    0x71,
    0x86,
    0x3D,
    0xDF,
    0xC4,
    0x71
)
IID_IWMDRMTranscryptor2 = EXTERN_GUID(
    0xE0DA439F,
    0xD331,
    0x496A,
    0xBE,
    0xCE,
    0x18,
    0xE5,
    0xBA,
    0xC5,
    0xDD,
    0x23
)
IID_IWMDRMTranscryptionManager = EXTERN_GUID(
    0xB1A887B2,
    0xA4F0,
    0x407A,
    0xB0,
    0x2E,
    0xEF,
    0xBD,
    0x23,
    0xBB,
    0xEC,
    0xDF
)
IID_IWMLicenseRevocationAgent = EXTERN_GUID(
    0x6967F2C9,
    0x4E26,
    0x4B57,
    0x88,
    0x94,
    0x79,
    0x98,
    0x80,
    0xF7,
    0xAC,
    0x7B
)
CLSID_WMMUTEX_Language = EXTERN_GUID(
    0xD6E22A00,
    0x35DA,
    0x11D1,
    0x90,
    0x34,
    0x00,
    0xA0,
    0xC9,
    0x03,
    0x49,
    0xBE
)
CLSID_WMMUTEX_Bitrate = EXTERN_GUID(
    0xD6E22A01,
    0x35DA,
    0x11D1,
    0x90,
    0x34,
    0x00,
    0xA0,
    0xC9,
    0x03,
    0x49,
    0xBE
)
CLSID_WMMUTEX_Presentation = EXTERN_GUID(
    0xD6E22A02,
    0x35DA,
    0x11D1,
    0x90,
    0x34,
    0x00,
    0xA0,
    0xC9,
    0x03,
    0x49,
    0xBE
)
CLSID_WMMUTEX_Unknown = EXTERN_GUID(
    0xD6E22A03,
    0x35DA,
    0x11D1,
    0x90,
    0x34,
    0x00,
    0xA0,
    0xC9,
    0x03,
    0x49,
    0xBE
)
CLSID_WMBandwidthSharing_Exclusive = EXTERN_GUID(
    0xAF6060AA,
    0x5197,
    0x11D2,
    0xB6,
    0xAF,
    0x00,
    0xC0,
    0x4F,
    0xD9,
    0x08,
    0xE9
)
CLSID_WMBandwidthSharing_Partial = EXTERN_GUID(
    0xAF6060AB,
    0x5197,
    0x11D2,
    0xB6,
    0xAF,
    0x00,
    0xC0,
    0x4F,
    0xD9,
    0x08,
    0xE9
)
WMT_DMOCATEGORY_AUDIO_WATERMARK = EXTERN_GUID(
    0x65221C5A,
    0xFA75,
    0x4B39,
    0xB5,
    0x0C,
    0x06,
    0xC3,
    0x36,
    0xB6,
    0xA3,
    0xEF
)
WMT_DMOCATEGORY_VIDEO_WATERMARK = EXTERN_GUID(
    0x187CC922,
    0x8EFC,
    0x4404,
    0x9D,
    0xAF,
    0x63,
    0xF4,
    0x83,
    0x0D,
    0xF1,
    0xBC
)


class _WMStreamPrioritizationRecord(Structure):
    _fields_ = [
        ('wStreamNumber', WORD),
        ('fMandatory', BOOL),
    ]


WM_STREAM_PRIORITY_RECORD = _WMStreamPrioritizationRecord


class _WMWriterStatistics(Structure):
    _fields_ = [
        ('qwSampleCount', QWORD),
        ('qwByteCount', QWORD),
        ('qwDroppedSampleCount', QWORD),
        ('qwDroppedByteCount', QWORD),
        ('dwCurrentBitrate', DWORD),
        ('dwAverageBitrate', DWORD),
        ('dwExpectedBitrate', DWORD),
        ('dwCurrentSampleRate', DWORD),
        ('dwAverageSampleRate', DWORD),
        ('dwExpectedSampleRate', DWORD),
    ]


WM_WRITER_STATISTICS = _WMWriterStatistics


class _WMWriterStatisticsEx(Structure):
    _fields_ = [
        ('dwBitratePlusOverhead', DWORD),
        ('dwCurrentSampleDropRateInQueue', DWORD),
        ('dwCurrentSampleDropRateInCodec', DWORD),
        ('dwCurrentSampleDropRateInMultiplexer', DWORD),
        ('dwTotalSampleDropsInQueue', DWORD),
        ('dwTotalSampleDropsInCodec', DWORD),
        ('dwTotalSampleDropsInMultiplexer', DWORD),
    ]


WM_WRITER_STATISTICS_EX = _WMWriterStatisticsEx


class _WMReaderStatistics(Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('dwBandwidth', DWORD),
        ('cPacketsReceived', DWORD),
        ('cPacketsRecovered', DWORD),
        ('cPacketsLost', DWORD),
        ('wQuality', WORD),
    ]


WM_READER_STATISTICS = _WMReaderStatistics


class _WMReaderClientInfo(Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('wszLang', POINTER(WCHAR)),
        ('wszBrowserUserAgent', POINTER(WCHAR)),
        ('wszBrowserWebPage', POINTER(WCHAR)),
        ('qwReserved', QWORD),
        ('pReserved', POINTER(LPARAM)),
        ('wszHostExe', POINTER(WCHAR)),
        ('qwHostVersion', QWORD),
        ('wszPlayerUserAgent', POINTER(WCHAR)),
    ]


WM_READER_CLIENTINFO = _WMReaderClientInfo


class _WMClientProperties(Structure):
    _fields_ = [
        ('dwIPAddress', DWORD),
        ('dwPort', DWORD),
    ]


WM_CLIENT_PROPERTIES = _WMClientProperties


class _WMClientPropertiesEx(Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('pwszIPAddress', LPCWSTR),
        ('pwszPort', LPCWSTR),
        ('pwszDNSName', LPCWSTR),
    ]


WM_CLIENT_PROPERTIES_EX = _WMClientPropertiesEx


class _WMPortNumberRange(Structure):
    _fields_ = [
        ('wPortBegin', WORD),
        ('wPortEnd', WORD),
    ]


WM_PORT_NUMBER_RANGE = _WMPortNumberRange


class _WMT_BUFFER_SEGMENT(Structure):
    _fields_ = [
        ('pBuffer', POINTER(INSSBuffer)),
        ('cbOffset', DWORD),
        ('cbLength', DWORD),
    ]


WMT_BUFFER_SEGMENT = _WMT_BUFFER_SEGMENT


class _WMT_PAYLOAD_FRAGMENT(Structure):
    _fields_ = [
        ('dwPayloadIndex', DWORD),
        ('segmentData', WMT_BUFFER_SEGMENT),
    ]


WMT_PAYLOAD_FRAGMENT = _WMT_PAYLOAD_FRAGMENT


class _WMT_FILESINK_DATA_UNIT(Structure):
    _fields_ = [
        ('packetHeaderBuffer', WMT_BUFFER_SEGMENT),
        ('cPayloads', DWORD),
        ('pPayloadHeaderBuffers', POINTER(WMT_BUFFER_SEGMENT)),
        ('cPayloadDataFragments', DWORD),
        ('pPayloadDataFragments', POINTER(WMT_PAYLOAD_FRAGMENT)),
    ]


WMT_FILESINK_DATA_UNIT = _WMT_FILESINK_DATA_UNIT


class _WMT_WEBSTREAM_FORMAT(Structure):
    _fields_ = [
        ('cbSize', WORD),
        ('cbSampleHeaderFixedData', WORD),
        ('wVersion', WORD),
        ('wReserved', WORD),
    ]


WMT_WEBSTREAM_FORMAT = _WMT_WEBSTREAM_FORMAT


class _WMT_WEBSTREAM_SAMPLE_HEADER(Structure):
    _fields_ = [
        ('cbLength', WORD),
        ('wPart', WORD),
        ('cTotalParts', WORD),
        ('wSampleType', WORD),
        ('wszURL', WCHAR * 1),
    ]


WMT_WEBSTREAM_SAMPLE_HEADER = _WMT_WEBSTREAM_SAMPLE_HEADER


class _WMAddressAccessEntry(Structure):
    _fields_ = [
        ('dwIPAddress', DWORD),
        ('dwMask', DWORD),
    ]


WM_ADDRESS_ACCESSENTRY = _WMAddressAccessEntry


class _WMPicture(Structure):
    _fields_ = [
        ('pwszMIMEType', LPWSTR),
        ('bPictureType', BYTE),
        ('pwszDescription', LPWSTR),
        ('dwDataLen', DWORD),
        ('pbData', POINTER(BYTE)),
    ]


WM_PICTURE = _WMPicture


class _WMSynchronisedLyrics(Structure):
    _fields_ = [
        ('bTimeStampFormat', BYTE),
        ('bContentType', BYTE),
        ('pwszContentDescriptor', LPWSTR),
        ('dwLyricsLen', DWORD),
        ('pbLyrics', POINTER(BYTE)),
    ]


WM_SYNCHRONISED_LYRICS = _WMSynchronisedLyrics


class _WMUserWebURL(Structure):
    _fields_ = [
        ('pwszDescription', LPWSTR),
        ('pwszURL', LPWSTR),
    ]


WM_USER_WEB_URL = _WMUserWebURL


class _WMUserText(Structure):
    _fields_ = [
        ('pwszDescription', LPWSTR),
        ('pwszText', LPWSTR),
    ]


WM_USER_TEXT = _WMUserText


class _WMLeakyBucketPair(Structure):
    _fields_ = [
        ('dwBitrate', DWORD),
        ('msBufferWindow', DWORD),
    ]


WM_LEAKY_BUCKET_PAIR = _WMLeakyBucketPair


class _WMStreamTypeInfo(Structure):
    _fields_ = [
        ('guidMajorType', GUID),
        ('cbFormat', DWORD),
    ]


WM_STREAM_TYPE_INFO = _WMStreamTypeInfo


class _WM_LICENSE_STATE_DATA(Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('dwNumStates', DWORD),
        ('stateData', DRM_LICENSE_STATE_DATA * 1),
    ]


WM_LICENSE_STATE_DATA = _WM_LICENSE_STATE_DATA


class __WMT_WATERMARK_ENTRY(Structure):
    _fields_ = [
        ('wmetType', WMT_WATERMARK_ENTRY_TYPE),
        ('clsid', CLSID),
        ('cbDisplayName', UINT),
        ('pwszDisplayName', LPWSTR),
    ]


WMT_WATERMARK_ENTRY = __WMT_WATERMARK_ENTRY


class __WMT_VIDEOIMAGE_SAMPLE(Structure):
    _fields_ = [
        ('dwMagic', DWORD),
        ('cbStruct', ULONG),
        ('dwControlFlags', DWORD),
        ('dwInputFlagsCur', DWORD),
        ('lCurMotionXtoX', LONG),
        ('lCurMotionYtoX', LONG),
        ('lCurMotionXoffset', LONG),
        ('lCurMotionXtoY', LONG),
        ('lCurMotionYtoY', LONG),
        ('lCurMotionYoffset', LONG),
        ('lCurBlendCoef1', LONG),
        ('lCurBlendCoef2', LONG),
        ('dwInputFlagsPrev', DWORD),
        ('lPrevMotionXtoX', LONG),
        ('lPrevMotionYtoX', LONG),
        ('lPrevMotionXoffset', LONG),
        ('lPrevMotionXtoY', LONG),
        ('lPrevMotionYtoY', LONG),
        ('lPrevMotionYoffset', LONG),
        ('lPrevBlendCoef1', LONG),
        ('lPrevBlendCoef2', LONG),
    ]


WMT_VIDEOIMAGE_SAMPLE = __WMT_VIDEOIMAGE_SAMPLE


class __WMT_VIDEOIMAGE_SAMPLE2(Structure):
    _fields_ = [
        ('dwMagic', DWORD),
        ('dwStructSize', DWORD),
        ('dwControlFlags', DWORD),
        ('dwViewportWidth', DWORD),
        ('dwViewportHeight', DWORD),
        ('dwCurrImageWidth', DWORD),
        ('dwCurrImageHeight', DWORD),
        ('fCurrRegionX0', FLOAT),
        ('fCurrRegionY0', FLOAT),
        ('fCurrRegionWidth', FLOAT),
        ('fCurrRegionHeight', FLOAT),
        ('fCurrBlendCoef', FLOAT),
        ('dwPrevImageWidth', DWORD),
        ('dwPrevImageHeight', DWORD),
        ('fPrevRegionX0', FLOAT),
        ('fPrevRegionY0', FLOAT),
        ('fPrevRegionWidth', FLOAT),
        ('fPrevRegionHeight', FLOAT),
        ('fPrevBlendCoef', FLOAT),
        ('dwEffectType', DWORD),
        ('dwNumEffectParas', DWORD),
        ('fEffectPara0', FLOAT),
        ('fEffectPara1', FLOAT),
        ('fEffectPara2', FLOAT),
        ('fEffectPara3', FLOAT),
        ('fEffectPara4', FLOAT),
        ('bKeepPrevImage', BOOL),
    ]


WMT_VIDEOIMAGE_SAMPLE2 = __WMT_VIDEOIMAGE_SAMPLE2


class _WMMediaType(Structure):
    _fields_ = [
        ('majortype', GUID),
        ('subtype', GUID),
        ('bFixedSizeSamples', BOOL),
        ('bTemporalCompression', BOOL),
        ('lSampleSize', ULONG),
        ('formattype', GUID),
        ('pUnk', POINTER(IUnknown)),
        ('cbFormat', ULONG),
        ('pbFormat', POINTER(BYTE)),
    ]


WM_MEDIA_TYPE = _WMMediaType


class tagWMVIDEOINFOHEADER(Structure):
    _fields_ = [
        ('rcSource', RECT),
        ('rcTarget', RECT),
        ('dwBitRate', DWORD),
        ('dwBitErrorRate', DWORD),
        ('AvgTimePerFrame', LONGLONG),
        ('bmiHeader', BITMAPINFOHEADER),
    ]


WMVIDEOINFOHEADER = tagWMVIDEOINFOHEADER


class tagWMVIDEOINFOHEADER2(Structure):
    _fields_ = [
        ('rcSource', RECT),
        ('rcTarget', RECT),
        ('dwBitRate', DWORD),
        ('dwBitErrorRate', DWORD),
        ('AvgTimePerFrame', LONGLONG),
        ('dwInterlaceFlags', DWORD),
        ('dwCopyProtectFlags', DWORD),
        ('dwPictAspectRatioX', DWORD),
        ('dwPictAspectRatioY', DWORD),
        ('dwReserved1', DWORD),
        ('dwReserved2', DWORD),
        ('bmiHeader', BITMAPINFOHEADER),
    ]


WMVIDEOINFOHEADER2 = tagWMVIDEOINFOHEADER2


class tagWMMPEG2VIDEOINFO(Structure):
    _fields_ = [
        ('hdr', WMVIDEOINFOHEADER2),
        ('dwStartTimeCode', DWORD),
        ('cbSequenceHeader', DWORD),
        ('dwProfile', DWORD),
        ('dwLevel', DWORD),
        ('dwFlags', DWORD),
        ('dwSequenceHeader', DWORD * 1),
    ]


WMMPEG2VIDEOINFO = tagWMMPEG2VIDEOINFO


class tagWMSCRIPTFORMAT(Structure):
    _fields_ = [
        ('   scriptType', GUID),
    ]


WMSCRIPTFORMAT = tagWMSCRIPTFORMAT


class _WMT_COLORSPACEINFO_EXTENSION_DATA(Structure):
    _fields_ = [
        ('ucColorPrimaries', BYTE),
        ('ucColorTransferChar', BYTE),
        ('ucColorMatrixCoef', BYTE),
    ]


WMT_COLORSPACEINFO_EXTENSION_DATA = _WMT_COLORSPACEINFO_EXTENSION_DATA


class _WMT_TIMECODE_EXTENSION_DATA(Structure):
    _fields_ = [
        ('wRange', WORD),
        ('dwTimecode', DWORD),
        ('dwUserbits', DWORD),
        ('dwAmFlags', DWORD),
    ]


WMT_TIMECODE_EXTENSION_DATA = _WMT_TIMECODE_EXTENSION_DATA


class _DRM_VAL16(Structure):
    _fields_ = [
        ('val', BYTE * 16),
    ]


DRM_VAL16 = _DRM_VAL16


class IWMMediaProps(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IWMMediaProps
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetType',
            (['out'], POINTER(GUID), 'pguidType')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetMediaType',
            (['out'], POINTER(WM_MEDIA_TYPE), 'pType'),
            (['in', 'out'], POINTER(DWORD), 'pcbType'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetMediaType',
            (['in'], POINTER(WM_MEDIA_TYPE), 'pType'),
        )
    )


class IWMVideoMediaProps(IWMMediaProps):
    _case_insensitive_ = True
    _iid_ = IID_IWMVideoMediaProps
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetMaxKeyFrameSpacing',
            (['out'], POINTER(LONGLONG), 'pllTime')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetMaxKeyFrameSpacing',
            (['in'], LONGLONG, 'llTime'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetQuality',
            (['in'], POINTER(DWORD), 'pdwQuality'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetQuality',
            (['in'], DWORD, 'dwQuality'),
        )
    )


class IWMWriter(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IWMWriter
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetProfileByID',
            (['in'], REFGUID, 'guidProfile')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetProfile',
            (['in'], POINTER(IWMProfile), 'pProfile'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetOutputFilename',
            (['in'], POINTER(WCHAR), 'pwszFilename'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetInputCount',
            (['out'], POINTER(DWORD), 'pcInputs'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetInputProps',
            (['in'], DWORD, 'dwInputNum'),
            (['out'], POINTER(POINTER(IWMInputMediaProps)), 'ppInput'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetInputProps',
            (['in'], DWORD, 'dwInputNum'),
            (['in'], POINTER(IWMInputMediaProps), 'pInput'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetInputFormatCount',
            (['in'], DWORD, 'dwInputNumber'),
            (['out'], POINTER(DWORD), 'pcFormats'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetInputFormat',
            (['in'], DWORD, 'dwInputNumber'),
            (['in'], DWORD, 'dwFormatNumber'),
            (['out'], POINTER(IWMInputMediaProps), 'pProps'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'BeginWriting',
            (),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'EndWriting',
            (),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'AllocateSample',
            (['in'], DWORD, 'dwSampleSize'),
            (['out'], POINTER(POINTER(INSSBuffer)), 'ppSample'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'WriteSample',
            (['in'], DWORD, 'dwInputNum'),
            (['in'], QWORD, 'cnsSampleTime'),
            (['in'], DWORD, 'dwFlags'),
            (['in'], POINTER(INSSBuffer), 'pSample'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Flush',
            (),
        )

    )


class IWMDRMWriter(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IWMDRMWriter
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GenerateKeySeed',
            (['out'], POINTER(WCHAR), 'pwszKeySeed'),
            (['in', 'out'], POINTER(DWORD), 'pcwchLength')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GenerateKeyID',
            (['out'], POINTER(WCHAR), 'pwszKeyID'),
            (['in', 'out'], POINTER(DWORD), 'pcwchLength')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GenerateSigningKeyPair',
            (['out'], POINTER(WCHAR), 'pwszPrivKey'),
            (['in', 'out'], POINTER(DWORD), 'pcwchPrivKeyLength'),
            (['out'], POINTER(WCHAR), 'pwszPubKey'),
            (['in', 'out'], POINTER(DWORD), 'pcwchPubKeyLength')

        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetDRMAttribute',
            (['in'], WORD, 'wStreamNum'),
            (['in'], LPCWSTR, 'pszName'),
            (['in'], WMT_ATTR_DATATYPE, 'Type'),
            (['in'], POINTER(BYTE), 'pValue'),
            (['in'], WORD, 'cbLength'),
        )
    )


class IWMDRMWriter2(IWMDRMWriter):
    _case_insensitive_ = True
    _iid_ = IID_IWMDRMWriter2
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetWMDRMNetEncryption',
            (['in'], BOOL, 'fSamplesEncrypted'),
            (['in'], POINTER(BYTE), 'pbKeyID'),
            (['in'], DWORD, 'cbKeyID'),
        ),
    )


class IWMDRMWriter3(IWMDRMWriter2):
    _case_insensitive_ = True
    _iid_ = IID_IWMDRMWriter3
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetProtectStreamSamples',
            (['in'], POINTER(WMDRM_IMPORT_INIT_STRUCT), 'pImportInitStruct'),
        ),
    )


class IWMInputMediaProps(IWMMediaProps):
    _case_insensitive_ = True
    _iid_ = IID_IWMInputMediaProps
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetConnectionName',
            (['out'], POINTER(WCHAR), 'pwszName'),
            (['in', 'out'], POINTER(WORD), 'pcchName')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetGroupName',
            (['out'], POINTER(WCHAR), 'pwszName'),
            (['in', 'out'], POINTER(WORD), 'pcchName')
        )
    )


class IWMPropertyVault(ctypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IWMPropertyVault
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetPropertyCount',
            (['in'], POINTER(DWORD), 'pdwCount')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetPropertyByName',
            (['in'], LPCWSTR, 'pszName'),
            (['out'], POINTER(WMT_ATTR_DATATYPE), 'pType'),
            (['out'], POINTER(BYTE), 'pValue'),
            (['in', 'out'], POINTER(DWORD), 'pdwSize')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetProperty',
            (['in'], LPCWSTR, 'pszName'),
            (['in'], WMT_ATTR_DATATYPE, 'pType'),
            (['in'], POINTER(BYTE), 'pValue'),
            (['in'], DWORD, 'dwSize'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetPropertyByIndex',
            (['in'], DWORD, 'dwIndex'),
            (['out'], LPWSTR, 'pszName'),
            (['in', 'out'], POINTER(DWORD), 'pdwNameLen'),
            (['out'], POINTER(WMT_ATTR_DATATYPE), 'pType'),
            (['out'], POINTER(BYTE), 'pValue'),
            (['in', 'out'], POINTER(DWORD), 'pdwSize')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'CopyPropertiesFrom',
            (['in'], POINTER(IWMPropertyVault), 'pIWMPropertyVault')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Clear',
            (),
        )
    )


class IWMIStreamProps(ctypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IWMIStreamProps
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetProperty',
            (['in'], LPCWSTR, 'pszName'),
            (['out'], POINTER(WMT_ATTR_DATATYPE), 'pType'),
            (['out'], POINTER(BYTE), 'pValue'),
            (['in', 'out'], POINTER(DWORD), 'pdwSize')
        ),
    )


class IWMReader(ctypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IWMReader
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'Open',
            (['in'], POINTER(WCHAR), 'pwszURL'),
            (['in'], POINTER(IWMReaderCallback), 'pCallback'),
            (['in'], POINTER(VOID), 'pvContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Close',
            ()
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetOutputCount',
            (['out'], POINTER(DWORD), 'pcOutputs')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetOutputProps',
            (['in'], DWORD, 'dwOutputNum'),
            (['out'], POINTER(POINTER(IWMOutputMediaProps)), 'ppOutput')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetOutputProps',
            (['in'], DWORD, 'dwOutputNum'),
            (['in'], POINTER(IWMOutputMediaProps), 'pOutput')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetOutputFormatCount',
            (['in'], DWORD, 'dwOutputNumber'),
            (['out'], POINTER(DWORD), 'pcFormats')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetOutputFormat',
            (['in'], DWORD, 'dwOutputNumber'),
            (['in'], DWORD, 'dwFormatNumber'),
            (['out'], POINTER(POINTER(IWMOutputMediaProps)), 'ppProps')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Start',
            (['in'], QWORD, 'cnsStart'),
            (['in'], QWORD, 'cnsDuration'),
            (['in'], FLOAT, 'fRate'),
            (['in'], POINTER(VOID), 'pvContext')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Stop',
            ()
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Pause',
            ()
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Resume',
            ()
        )
    )


class IWMSyncReader2(IWMSyncReader):
    _case_insensitive_ = True
    _iid_ = IID_IWMSyncReader2
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'SetRangeByTimecode',
            (['in'], WORD, 'wStreamNum'),
            (['in'], POINTER(WMT_TIMECODE_EXTENSION_DATA), 'pStart'),
            (['in'], POINTER(WMT_TIMECODE_EXTENSION_DATA), 'pEnd')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetRangeByFrameEx',
            (['in'], WORD, 'wStreamNum'),
            (['in'], QWORD, 'qwFrameNumber'),
            (['in'], LONGLONG, 'cFramesToRead'),
            (['out'], POINTER(QWORD), 'pcnsStartTime')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetAllocateForOutput',
            (['in'], DWORD, 'dwOutputNum'),
            (['in'], POINTER(IWMReaderAllocatorEx), 'pAllocator'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetAllocateForOutput',
            (['in'], DWORD, 'dwOutputNum'),
            (['out'], POINTER(POINTER(IWMReaderAllocatorEx)), 'pAllocator'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetAllocateForStream',
            (['in'], WORD, 'wStreamNum'),
            (['in'], POINTER(IWMReaderAllocatorEx), 'pAllocator'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetAllocateForStream',
            (['in'], WORD, 'dwSreamNum'),
            (['out'], POINTER(POINTER(IWMReaderAllocatorEx)), 'pAllocator'),
        )
    )


class IWMOutputMediaProps(IWMMediaProps):
    _case_insensitive_ = True
    _iid_ = IID_IWMOutputMediaProps
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'GetStreamGroupName',
            (['out'], POINTER(WCHAR), 'pwszName'),
            (['in', 'out'], POINTER(WORD), 'pcchName')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetConnectionName',
            (['out'], POINTER(WCHAR), 'pwszName'),
            (['in', 'out'], POINTER(WORD), 'pcchName')
        )
    )


class IWMStatusCallback(ctypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IWMStatusCallback
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'OnStatus',
            (['in'], WMT_STATUS, 'Status'),
            (['in'], HRESULT, 'hr'),
            (['in'], WMT_ATTR_DATATYPE, 'dwType'),
            (['in'], POINTER(BYTE), 'pValue'),
            (['in'], POINTER(VOID), 'pvContext')
        ),
    )


class IWMReaderCallback(ctypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IWMReaderCallback
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'OnSample',
            (['in'], DWORD, 'dwOutputNum'),
            (['in'], QWORD, 'cnsSampleTime'),
            (['in'], QWORD, 'cnsSampleDuration'),
            (['in'], DWORD, 'dwFlags'),
            (['in'], POINTER(INSSBuffer), 'pSample'),
            (['in'], POINTER(VOID), 'pvContext')
        ),
    )


class IWMCredentialCallback(ctypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IWMCredentialCallback
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'AcquireCredentials',
            (['in'], POINTER(WCHAR), 'pwszRealm'),
            (['in'], POINTER(WCHAR), 'pwszSite'),
            (['out'], POINTER(WCHAR), 'pwszUser'),
            (['in'], DWORD, 'cchUser'),
            (['out'], POINTER(WCHAR), 'pwszPassword'),
            (['in'], DWORD, 'cchPassword'),
            (['in'], HRESULT, 'hrStatus'),
            (['out'], POINTER(DWORD), 'pdwFlags')
        ),
    )


class IWMMetadataEditor(ctypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IWMMetadataEditor
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'Open',
            (['in'], POINTER(WCHAR), 'pwszFilename')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Close',
            ()
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Flush',
            ()
        ),
    )


class IWMMetadataEditor2(IWMMetadataEditor):
    _case_insensitive_ = True
    _iid_ = IID_IWMMetadataEditor2
    _methods_ = (
        COMMETHOD(
            [],
            HRESULT,
            'OpenEx',
            (['in'], POINTER(WCHAR), 'pwszFilename'),
            (['in'], DWORD, 'dwDesiredAccess'),
            (['in'], DWORD, 'dwShareMode')
        ),
    )

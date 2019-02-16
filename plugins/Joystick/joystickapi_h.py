from win_constants_h import *
import ctypes
from comtypes import GUID
from ctypes.wintypes import POINTER, WORD, UINT, WCHAR, DWORD

VOID = ctypes.c_void_p
CHAR = ctypes.c_char

_JOYSTICKAPI_H_ = None
MMNOJOY = None


class tagJOYCAPSA(ctypes.Structure):
    pass


JOYCAPSA = tagJOYCAPSA
PJOYCAPSA = POINTER(tagJOYCAPSA)
NPJOYCAPSA = POINTER(tagJOYCAPSA)
LPJOYCAPSA = POINTER(tagJOYCAPSA)


class tagJOYCAPSW(ctypes.Structure):
    pass


JOYCAPSW = tagJOYCAPSW
PJOYCAPSW = POINTER(tagJOYCAPSW)
NPJOYCAPSW = POINTER(tagJOYCAPSW)
LPJOYCAPSW = POINTER(tagJOYCAPSW)


class tagJOYCAPS2A(ctypes.Structure):
    pass


JOYCAPS2A = tagJOYCAPS2A
PJOYCAPS2A = POINTER(tagJOYCAPS2A)
NPJOYCAPS2A = POINTER(tagJOYCAPS2A)
LPJOYCAPS2A = POINTER(tagJOYCAPS2A)


class tagJOYCAPS2W(ctypes.Structure):
    pass


JOYCAPS2W = tagJOYCAPS2W
PJOYCAPS2W = POINTER(tagJOYCAPS2W)
NPJOYCAPS2W = POINTER(tagJOYCAPS2W)
LPJOYCAPS2W = POINTER(tagJOYCAPS2W)


class joycaps_tag(ctypes.Structure):
    pass


JOYCAPS = joycaps_tag
PJOYCAPS = POINTER(joycaps_tag)
NPJOYCAPS = POINTER(joycaps_tag)
LPJOYCAPS = POINTER(joycaps_tag)


class joyinfo_tag(ctypes.Structure):
    pass


JOYINFO = joyinfo_tag
PJOYINFO = POINTER(joyinfo_tag)
NPJOYINFO = POINTER(joyinfo_tag)
LPJOYINFO = POINTER(joyinfo_tag)


class joyinfoex_tag(ctypes.Structure):
    pass


JOYINFOEX = joyinfoex_tag
PJOYINFOEX = POINTER(joyinfoex_tag)
NPJOYINFOEX = POINTER(joyinfoex_tag)
LPJOYINFOEX = POINTER(joyinfoex_tag)


# *****************************************************************************
# joystickapi.h -- ApiSet Contract for api-ms-win-mm-joystick-l1-1-0
# Copyright (c) Microsoft Corporation. All rights reserved.
# *****************************************************************************

if defined(_MSC_VER):
    pass
# END IF   _MSC_VER

if not defined(_JOYSTICKAPI_H_):
    _JOYSTICKAPI_H_ = VOID
    # from pyWinAPI.shared.apiset_h import * # NOQA
    # from pyWinAPI.shared.apisetcconv_h import * # NOQA
    #
    # # mm common definitions
    from mmsyscom_h import * # NOQA

    if defined(__cplusplus):
        pass
    # END IF

    winmm = ctypes.windll.WINMM

    if WINAPI_FAMILY_PARTITION(WINAPI_PARTITION_DESKTOP):
        if not defined(MMNOJOY):
            # *****************************************************************
            # Joystick support
            # *****************************************************************

            # joystick error return values
            JOYERR_NOERROR = 0 # no error
            JOYERR_PARMS = JOYERR_BASE + 5 # bad parameters
            JOYERR_NOCANDO = JOYERR_BASE + 6 # request not completed
            JOYERR_UNPLUGGED = JOYERR_BASE + 7 # joystick is unplugged

            # constants used with JOYINFO and JOYINFOEX structures and MM_JOY*
            # messages
            JOY_BUTTON1 = 0x0001
            JOY_BUTTON2 = 0x0002
            JOY_BUTTON3 = 0x0004
            JOY_BUTTON4 = 0x0008
            JOY_BUTTON1CHG = 0x0100
            JOY_BUTTON2CHG = 0x0200
            JOY_BUTTON3CHG = 0x0400
            JOY_BUTTON4CHG = 0x0800

            # constants used with JOYINFOEX
            JOY_BUTTON5 = 0x00000010
            JOY_BUTTON6 = 0x00000020
            JOY_BUTTON7 = 0x00000040
            JOY_BUTTON8 = 0x00000080
            JOY_BUTTON9 = 0x00000100
            JOY_BUTTON10 = 0x00000200
            JOY_BUTTON11 = 0x00000400
            JOY_BUTTON12 = 0x00000800
            JOY_BUTTON13 = 0x00001000
            JOY_BUTTON14 = 0x00002000
            JOY_BUTTON15 = 0x00004000
            JOY_BUTTON16 = 0x00008000
            JOY_BUTTON17 = 0x00010000
            JOY_BUTTON18 = 0x00020000
            JOY_BUTTON19 = 0x00040000
            JOY_BUTTON20 = 0x00080000
            JOY_BUTTON21 = 0x00100000
            JOY_BUTTON22 = 0x00200000
            JOY_BUTTON23 = 0x00400000
            JOY_BUTTON24 = 0x00800000
            JOY_BUTTON25 = 0x01000000
            JOY_BUTTON26 = 0x02000000
            JOY_BUTTON27 = 0x04000000
            JOY_BUTTON28 = 0x08000000
            JOY_BUTTON29 = 0x10000000
            JOY_BUTTON30 = 0x20000000
            JOY_BUTTON31 = 0x40000000
            JOY_BUTTON32 = 0x80000000

            # constants used with JOYINFOEX structure
            JOY_POVCENTERED = -1
            JOY_POVFORWARD = 0
            JOY_POVRIGHT = 9000
            JOY_POVBACKWARD = 18000
            JOY_POVLEFT = 27000
            JOY_RETURNX = 0x00000001
            JOY_RETURNY = 0x00000002
            JOY_RETURNZ = 0x00000004
            JOY_RETURNR = 0x00000008
            JOY_RETURNU = 0x00000010            # axis 5
            JOY_RETURNV = 0x00000020            # axis 6
            JOY_RETURNPOV = 0x00000040
            JOY_RETURNBUTTONS = 0x00000080
            JOY_RETURNRAWDATA = 0x00000100
            JOY_RETURNPOVCTS = 0x00000200
            JOY_RETURNCENTERED = 0x00000400
            JOY_USEDEADZONE = 0x00000800
            JOY_RETURNALL = (
                JOY_RETURNX |
                JOY_RETURNY |
                JOY_RETURNZ |
                JOY_RETURNR |
                JOY_RETURNU |
                JOY_RETURNV |
                JOY_RETURNPOV |
                JOY_RETURNBUTTONS
            )
            JOY_CAL_READALWAYS = 0x00010000
            JOY_CAL_READXYONLY = 0x00020000
            JOY_CAL_READ3 = 0x00040000
            JOY_CAL_READ4 = 0x00080000
            JOY_CAL_READXONLY = 0x00100000
            JOY_CAL_READYONLY = 0x00200000
            JOY_CAL_READ5 = 0x00400000
            JOY_CAL_READ6 = 0x00800000
            JOY_CAL_READZONLY = 0x01000000
            JOY_CAL_READRONLY = 0x02000000
            JOY_CAL_READUONLY = 0x04000000
            JOY_CAL_READVONLY = 0x08000000

            # joystick ID constants
            JOYSTICKID1 = 0
            JOYSTICKID2 = 1

            # joystick driver capabilities
            JOYCAPS_HASZ = 0x0001
            JOYCAPS_HASR = 0x0002
            JOYCAPS_HASU = 0x0004
            JOYCAPS_HASV = 0x0008
            JOYCAPS_HASPOV = 0x0010
            JOYCAPS_POV4DIR = 0x0020
            JOYCAPS_POVCTS = 0x0040

            # joystick device capabilities data structure

            if defined(_WIN32):
                # manufacturer ID
                _TEMP_tagJOYCAPSA = [
                    ('wMid', WORD),
                    # product ID
                    ('wPid', WORD),
                    # product name (NULL terminated string)
                    ('szPname', CHAR * MAXPNAMELEN),
                    # minimum x position value
                    ('wXmin', UINT),
                    # maximum x position value
                    ('wXmax', UINT),
                    # minimum y position value
                    ('wYmin', UINT),
                    # maximum y position value
                    ('wYmax', UINT),
                    # minimum z position value
                    ('wZmin', UINT),
                    # maximum z position value
                    ('wZmax', UINT),
                    # number of buttons
                    ('wNumButtons', UINT),
                    # minimum message period when captured
                    ('wPeriodMin', UINT),
                    # maximum message period when captured
                    ('wPeriodMax', UINT),
                ]
                if WINVER >= 0x0400:
                    _TEMP_tagJOYCAPSA += [
                        # minimum r position value
                        ('wRmin', UINT),
                        # maximum r position value
                        ('wRmax', UINT),
                        # minimum u (5th axis) position value
                        ('wUmin', UINT),
                        # maximum u (5th axis) position value
                        ('wUmax', UINT),
                        # minimum v (6th axis) position value
                        ('wVmin', UINT),
                        # maximum v (6th axis) position value
                        ('wVmax', UINT),
                        # joystick capabilites
                        ('wCaps', UINT),
                        # maximum number of axes supported
                        ('wMaxAxes', UINT),
                        # number of axes in use
                        ('wNumAxes', UINT),
                        # maximum number of buttons supported
                        ('wMaxButtons', UINT),
                        # registry key
                        ('szRegKey', CHAR * MAXPNAMELEN),
                        # OEM VxD in use
                        ('szOEMVxD', CHAR * MAX_JOYSTICKOEMVXDNAME),
                    ]
                # END IF

                tagJOYCAPSA._fields_ = _TEMP_tagJOYCAPSA

                # manufacturer ID
                _TEMP_tagJOYCAPSW = [
                    ('wMid', WORD),
                    # product ID
                    ('wPid', WORD),
                    # product name (NULL terminated string)
                    ('szPname', WCHAR * MAXPNAMELEN),
                    # minimum x position value
                    ('wXmin', UINT),
                    # maximum x position value
                    ('wXmax', UINT),
                    # minimum y position value
                    ('wYmin', UINT),
                    # maximum y position value
                    ('wYmax', UINT),
                    # minimum z position value
                    ('wZmin', UINT),
                    # maximum z position value
                    ('wZmax', UINT),
                    # number of buttons
                    ('wNumButtons', UINT),
                    # minimum message period when captured
                    ('wPeriodMin', UINT),
                    # maximum message period when captured
                    ('wPeriodMax', UINT),
                ]
                if WINVER >= 0x0400:
                    _TEMP_tagJOYCAPSW += [
                        # minimum r position value
                        ('wRmin', UINT),
                        # maximum r position value
                        ('wRmax', UINT),
                        # minimum u (5th axis) position value
                        ('wUmin', UINT),
                        # maximum u (5th axis) position value
                        ('wUmax', UINT),
                        # minimum v (6th axis) position value
                        ('wVmin', UINT),
                        # maximum v (6th axis) position value
                        ('wVmax', UINT),
                        # joystick capabilites
                        ('wCaps', UINT),
                        # maximum number of axes supported
                        ('wMaxAxes', UINT),
                        # number of axes in use
                        ('wNumAxes', UINT),
                        # maximum number of buttons supported
                        ('wMaxButtons', UINT),
                        # registry key
                        ('szRegKey', WCHAR * MAXPNAMELEN),
                        # OEM VxD in use
                        ('szOEMVxD', WCHAR * MAX_JOYSTICKOEMVXDNAME),
                    ]
                # END IF

                tagJOYCAPSW._fields_ = _TEMP_tagJOYCAPSW

                if defined(UNICODE):
                    JOYCAPS = JOYCAPSW
                    PJOYCAPS = PJOYCAPSW
                    NPJOYCAPS = NPJOYCAPSW
                    LPJOYCAPS = LPJOYCAPSW
                else:
                    JOYCAPS = JOYCAPSA
                    PJOYCAPS = PJOYCAPSA
                    NPJOYCAPS = NPJOYCAPSA
                    LPJOYCAPS = LPJOYCAPSA
                # END IF   UNICODE

                # manufacturer ID
                tagJOYCAPS2A._fields_ = [
                    ('wMid', WORD),
                    # product ID
                    ('wPid', WORD),
                    # product name (NULL terminated string)
                    ('szPname', CHAR * MAXPNAMELEN),
                    # minimum x position value
                    ('wXmin', UINT),
                    # maximum x position value
                    ('wXmax', UINT),
                    # minimum y position value
                    ('wYmin', UINT),
                    # maximum y position value
                    ('wYmax', UINT),
                    # minimum z position value
                    ('wZmin', UINT),
                    # maximum z position value
                    ('wZmax', UINT),
                    # number of buttons
                    ('wNumButtons', UINT),
                    # minimum message period when captured
                    ('wPeriodMin', UINT),
                    # maximum message period when captured
                    ('wPeriodMax', UINT),
                    # minimum r position value
                    ('wRmin', UINT),
                    # maximum r position value
                    ('wRmax', UINT),
                    # minimum u (5th axis) position value
                    ('wUmin', UINT),
                    # maximum u (5th axis) position value
                    ('wUmax', UINT),
                    # minimum v (6th axis) position value
                    ('wVmin', UINT),
                    # maximum v (6th axis) position value
                    ('wVmax', UINT),
                    # joystick capabilites
                    ('wCaps', UINT),
                    # maximum number of axes supported
                    ('wMaxAxes', UINT),
                    # number of axes in use
                    ('wNumAxes', UINT),
                    # maximum number of buttons supported
                    ('wMaxButtons', UINT),
                    # registry key
                    ('szRegKey', CHAR * MAXPNAMELEN),
                    # OEM VxD in use
                    ('szOEMVxD', CHAR * MAX_JOYSTICKOEMVXDNAME),
                    # for extensible MID mapping
                    ('ManufacturerGuid', GUID),
                    # for extensible PID mapping
                    ('ProductGuid', GUID),
                    # for name lookup in registry
                    ('NameGuid', GUID),
                ]

                # manufacturer ID
                tagJOYCAPS2W._fields_ = [
                    ('wMid', WORD),
                    # product ID
                    ('wPid', WORD),
                    # product name (NULL terminated string)
                    ('szPname', WCHAR * MAXPNAMELEN),
                    # minimum x position value
                    ('wXmin', UINT),
                    # maximum x position value
                    ('wXmax', UINT),
                    # minimum y position value
                    ('wYmin', UINT),
                    # maximum y position value
                    ('wYmax', UINT),
                    # minimum z position value
                    ('wZmin', UINT),
                    # maximum z position value
                    ('wZmax', UINT),
                    # number of buttons
                    ('wNumButtons', UINT),
                    # minimum message period when captured
                    ('wPeriodMin', UINT),
                    # maximum message period when captured
                    ('wPeriodMax', UINT),
                    # minimum r position value
                    ('wRmin', UINT),
                    # maximum r position value
                    ('wRmax', UINT),
                    # minimum u (5th axis) position value
                    ('wUmin', UINT),
                    # maximum u (5th axis) position value
                    ('wUmax', UINT),
                    # minimum v (6th axis) position value
                    ('wVmin', UINT),
                    # maximum v (6th axis) position value
                    ('wVmax', UINT),
                    # joystick capabilites
                    ('wCaps', UINT),
                    # maximum number of axes supported
                    ('wMaxAxes', UINT),
                    # number of axes in use
                    ('wNumAxes', UINT),
                    # maximum number of buttons supported
                    ('wMaxButtons', UINT),
                    # registry key
                    ('szRegKey', WCHAR * MAXPNAMELEN),
                    # OEM VxD in use
                    ('szOEMVxD', WCHAR * MAX_JOYSTICKOEMVXDNAME),
                    # for extensible MID mapping
                    ('ManufacturerGuid', GUID),
                    # for extensible PID mapping
                    ('ProductGuid', GUID),
                    # for name lookup in registry
                    ('NameGuid', GUID),
                ]

                if defined(UNICODE):
                    JOYCAPS2 = JOYCAPS2W
                    PJOYCAPS2 = PJOYCAPS2W
                    NPJOYCAPS2 = NPJOYCAPS2W
                    LPJOYCAPS2 = LPJOYCAPS2W
                else:
                    JOYCAPS2 = JOYCAPS2A
                    PJOYCAPS2 = PJOYCAPS2A
                    NPJOYCAPS2 = NPJOYCAPS2A
                    LPJOYCAPS2 = LPJOYCAPS2A
                # END IF   UNICODE

            else:
                # manufacturer ID
                _TEMP_joycaps_tag = [
                    ('wMid', WORD),
                    # product ID
                    ('wPid', WORD),
                    # product name (NULL terminated string)
                    ('szPname', CHAR * MAXPNAMELEN),
                    # minimum x position value
                    ('wXmin', UINT),
                    # maximum x position value
                    ('wXmax', UINT),
                    # minimum y position value
                    ('wYmin', UINT),
                    # maximum y position value
                    ('wYmax', UINT),
                    # minimum z position value
                    ('wZmin', UINT),
                    # maximum z position value
                    ('wZmax', UINT),
                    # number of buttons
                    ('wNumButtons', UINT),
                    # minimum message period when captured
                    ('wPeriodMin', UINT),
                    # maximum message period when captured
                    ('wPeriodMax', UINT),
                ]
                if WINVER >= 0x0400:
                    _TEMP_joycaps_tag += [
                        # minimum r position value
                        ('wRmin', UINT),
                        # maximum r position value
                        ('wRmax', UINT),
                        # minimum u (5th axis) position value
                        ('wUmin', UINT),
                        # maximum u (5th axis) position value
                        ('wUmax', UINT),
                        # minimum v (6th axis) position value
                        ('wVmin', UINT),
                        # maximum v (6th axis) position value
                        ('wVmax', UINT),
                        # joystick capabilites
                        ('wCaps', UINT),
                        # maximum number of axes supported
                        ('wMaxAxes', UINT),
                        # number of axes in use
                        ('wNumAxes', UINT),
                        # maximum number of buttons supported
                        ('wMaxButtons', UINT),
                        # registry key
                        ('szRegKey', CHAR * MAXPNAMELEN),
                        # OEM VxD in use
                        ('szOEMVxD', CHAR * MAX_JOYSTICKOEMVXDNAME),
                    ]
                # END IF

                joycaps_tag._fields_ = _TEMP_joycaps_tag
            # END IF

            # joystick information data structure
            # x position
            joyinfo_tag._fields_ = [
                ('wXpos', UINT),
                # y position
                ('wYpos', UINT),
                # z position
                ('wZpos', UINT),
                # button states
                ('wButtons', UINT),
            ]
            if WINVER >= 0x0400:
                # size of structure
                joyinfoex_tag._fields_ = [
                    ('dwSize', DWORD),
                    # flags to indicate what to return
                    ('dwFlags', DWORD),
                    # x position
                    ('dwXpos', DWORD),
                    # y position
                    ('dwYpos', DWORD),
                    # z position
                    ('dwZpos', DWORD),
                    # rudder/4th axis position
                    ('dwRpos', DWORD),
                    # 5th axis position
                    ('dwUpos', DWORD),
                    # 6th axis position
                    ('dwVpos', DWORD),
                    # button states
                    ('dwButtons', DWORD),
                    # current button number pressed
                    ('dwButtonNumber', DWORD),
                    # point of view state
                    ('dwPOV', DWORD),
                    # reserved for communication between winmm & driver
                    ('dwReserved1', DWORD),
                    # reserved for future expansion
                    ('dwReserved2', DWORD),
                ]
            # END IF

            # joystick function prototypes
            if WINVER >= 0x0400:
                # WINMMAPI
                # MMRESULT
                # WINAPI
                # joyGetPosEx(
                # _In_ UINT uJoyID,
                # _Out_ LPJOYINFOEX pji
                # );
                joyGetPosEx = winmm.joyGetPosEx
                joyGetPosEx.restype = MMRESULT

            # END IF  WINVER >= 0x0400

            # WINMMAPI
            # UINT
            # WINAPI
            # joyGetNumDevs(
            # void
            # );
            joyGetNumDevs = winmm.joyGetNumDevs
            joyGetNumDevs.restype = UINT

            if defined(_WIN32):
                # WINMMAPI
                # MMRESULT
                # WINAPI
                # joyGetDevCapsA(
                # _In_ UINT_PTR uJoyID,
                # _Out_writes_bytes_(cbjc) LPJOYCAPSA pjc,
                # _In_ UINT cbjc
                # );
                joyGetDevCapsA = winmm.joyGetDevCapsA
                joyGetDevCapsA.restype = MMRESULT

                # WINMMAPI
                # MMRESULT
                # WINAPI
                # joyGetDevCapsW(
                # _In_ UINT_PTR uJoyID,
                # _Out_writes_bytes_(cbjc) LPJOYCAPSW pjc,
                # _In_ UINT cbjc
                # );
                joyGetDevCapsW = winmm.joyGetDevCapsW
                joyGetDevCapsW.restype = MMRESULT

                if defined(UNICODE):
                    joyGetDevCaps = joyGetDevCapsW
                else:
                    joyGetDevCaps = joyGetDevCapsA
                # END IF   not UNICODE
            else:
                # MMRESULT WINAPI joyGetDevCaps(
                # UINT uJoyID,
                # LPJOYCAPS pjc,
                # UINT cbjc
                # );
                joyGetDevCaps = winmm.joyGetDevCaps
                joyGetDevCaps.restype = MMRESULT

            # END IF

            # WINMMAPI
            # MMRESULT
            # WINAPI
            # joyGetPos(
            # _In_ UINT uJoyID,
            # _Out_ LPJOYINFO pji
            # );
            joyGetPos = winmm.joyGetPos
            joyGetPos.restype = MMRESULT

            # WINMMAPI
            # MMRESULT
            # WINAPI
            # joyGetThreshold(
            # _In_ UINT uJoyID,
            # _Out_ LPUINT puThreshold
            # );
            joyGetThreshold = winmm.joyGetThreshold
            joyGetThreshold.restype = MMRESULT

            # WINMMAPI
            # MMRESULT
            # WINAPI
            # joyReleaseCapture(
            # _In_ UINT uJoyID
            # );
            joyReleaseCapture = winmm.joyReleaseCapture
            joyReleaseCapture.restype = MMRESULT

            # WINMMAPI
            # MMRESULT
            # WINAPI
            # joySetCapture(
            # _In_ HWND hwnd,
            # _In_ UINT uJoyID,
            # _In_ UINT uPeriod,
            # _In_ BOOL fChanged
            # );
            joySetCapture = winmm.joySetCapture
            joySetCapture.restype = MMRESULT
            
            # WINMMAPI
            # MMRESULT
            # WINAPI
            # joySetThreshold(
            # _In_ UINT uJoyID,
            # _In_ UINT uThreshold
            # );
            joySetThreshold = winmm.joySetThreshold
            joySetThreshold.restype = MMRESULT

            if WINVER >= 0x0400:
                # WINMMAPI
                # MMRESULT
                # WINAPI
                # joyConfigChanged(
                # _In_ DWORD dwFlags
                # );
                joyConfigChanged = winmm.joyConfigChanged
                joyConfigChanged.restype = MMRESULT
            # END IF
        # END IF  ifndef MMNOJOY
    # END IF   WINAPI_FAMILY_PARTITION(WINAPI_PARTITION_DESKTOP)

    if defined(__cplusplus):
        pass
    # END IF
# END IF   _JOYSTICKAPI_H_

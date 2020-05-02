# -*- coding: utf-8 -*-

import wx
import sys
import ctypes
import locale as _locale
from ctypes.wintypes import WORD, LCID, DWORD, INT, WCHAR, LPCWSTR, BOOL


PY3 = sys.version_info[0] >= 3

_Locale = wx.Locale
LC_ALL = _locale.LC_ALL
LANGID = WORD
LCTYPE = DWORD

LOCALE_NAME_MAX_LENGTH = 85
LOCALE_ALLOW_NEUTRAL_NAMES = 0x08000000
LOCALE_SENGLISHLANGUAGENAME = 0x00001001
LOCALE_SENGLISHCOUNTRYNAME = 0x00001002
LOCALE_IDEFAULTANSICODEPAGE = 0x00001004
LOCALE_SNATIVELANGUAGENAME = 0x00000004
LOCALE_SLOCALIZEDLANGUAGENAME = 0x0000006f
LOCALE_SNATIVECOUNTRYNAME = 0x00000008
LOCALE_SLOCALIZEDCOUNTRYNAME = 0x00000006

LCID_INSTALLED = 0x00000001
LCID_SUPPORTED = 0x00000002

_kernel32 = ctypes.windll.Kernel32

_IsValidLocale = _kernel32.IsValidLocale
_IsValidLocale.restype = BOOL

_SetThreadUILanguage = _kernel32.SetThreadUILanguage
_SetThreadUILanguage.restype = LANGID

_GetThreadUILanguage = _kernel32.GetThreadUILanguage
_GetThreadUILanguage.restype = LANGID

_GetLocaleInfoEx = _kernel32.GetLocaleInfoEx
_GetLocaleInfoEx.restype = INT

_LocaleNameToLCID = _kernel32.LocaleNameToLCID
_LocaleNameToLCID.restype = LCID

_LCIDToLocaleName = _kernel32.LCIDToLocaleName
_LCIDToLocaleName.restype = INT

_GetLocaleInfo = _kernel32.GetLocaleInfoW
_GetLocaleInfo.restype = INT

LOCALE_STHOUSAND = 0x0000000F
LOCALE_SMONDECIMALSEP = 0x00000016
LOCALE_SDECIMAL = 0x0000000E
LOCALE_SSHORTDATE = 0x0000001F
LOCALE_SLONGDATE = 0x00000020
LOCALE_STIMEFORMAT = 0x00001003


def GetLocaleInfo(
    lpLocaleName,
    index,
    cat=wx.LOCALE_CAT_DEFAULT
):
    if index == wx.LOCALE_THOUSANDS_SEP:
        LCType = LOCALE_STHOUSAND
    elif index == wx.LOCALE_DECIMAL_POINT:
        if cat == wx.LOCALE_CAT_MONEY:
            LCType = LOCALE_SMONDECIMALSEP
        else:
            LCType = LOCALE_SDECIMAL
    elif index == wx.LOCALE_SHORT_DATE_FMT:
        LCType = LOCALE_SSHORTDATE
    elif index == wx.LOCALE_LONG_DATE_FMT:
        LCType = LOCALE_SLONGDATE
    elif index == wx.LOCALE_TIME_FMT:
        LCType = LOCALE_STIMEFORMAT
    elif index == wx.LOCALE_DATE_TIME_FMT:
        date_fmt = GetLocaleInfo(lpLocaleName, wx.LOCALE_SHORT_DATE_FMT)
        if not date_fmt:
            return ''

        time_fmt = GetLocaleInfo(lpLocaleName, wx.LOCALE_TIME_FMT)
        if not time_fmt:
            return ''

        return date_fmt + ' ' + time_fmt
    else:
        raise RuntimeError('unknown wxLocaleInfo')

    value = GetLocaleInfoEx(lpLocaleName, LCType)

    if index == wx.LOCALE_TIME_FMT:
        hour_formats = [
            '',
            '%-I',
            '%I'
        ]
        hour_count = value.count('h')
        if not hour_count:
            hour_formats = [
                '',
                '%-H',
                '%H'
            ]
            hour_count = value.count('H')

        minute_count = value.count('m')
        second_count = value.count('s')
        suffix_count = value.count('t')

        minute_formats = [
            '',
            '%-M',
            '%M'
        ]
        second_formats = [
            '',
            '%-S',
            '%S'
        ]
        suffix_formats = [
            '',
            '%p',
            '%p'
        ]

        if hour_count > 0:
            hour_format = hour_formats[hour_count]
            value = value.replace('h' * hour_count, hour_format)
            value = value.replace('H' * hour_count, hour_format)

        if minute_count > 0:
            minute_format = minute_formats[minute_count]
            value = value.replace('m' * minute_count, minute_format)

        if second_count > 0:
            second_format = second_formats[second_count]
            value = value.replace('s' * second_count, second_format)

        if suffix_count > 0:
            suffix_format = suffix_formats[suffix_count]
            value = value.replace('t' * suffix_count, suffix_format)

    elif index in (wx.LOCALE_SHORT_DATE_FMT, wx.LOCALE_LONG_DATE_FMT):
        items = value.split(' ')
        for i, item in enumerate(items):
            month_count = item.count('M')
            day_count = item.count('d')
            year_count = item.count('y')

            month_formats = [
                '',
                '%-m',
                '%m',
                '%b',
                '%B'
            ]
            day_formats = [
                '',
                '%-d',
                '%d',
                '%a',
                '%A'
            ]
            year_formats = [
                '',
                '%y',
                '%y',
                '',
                '%Y',
                '%Y'
            ]

            if month_count > 0:
                month_format = month_formats[month_count]
                item = item.replace('M' * month_count, month_format)

            if day_count > 0:
                day_format = day_formats[day_count]
                item = item.replace('d' * day_count, day_format)

            if year_count > 0:
                year_format = year_formats[year_count]
                item = item.replace('y' * year_count, year_format)

            items[i] = item

        value = ' '.join(items)

    return value


def SetThreadUILanguage(lcid):
    if not isinstance(lcid, LCID):
        lcid = LCID(lcid)

    _SetThreadUILanguage(lcid)


def IsValidLocale(lcid):
    if not isinstance(lcid, LCID):
        lcid = LCID(lcid)

    if not _IsValidLocale(lcid, DWORD(LCID_SUPPORTED)):
        return False

    return bool(_IsValidLocale(lcid, DWORD(LCID_INSTALLED)))


def GetThreadUILanguage():
    lang_id = _GetThreadUILanguage()
    lcid = LCIDFROMLANGID(lang_id)
    return LCIDToLocaleName(lcid)


def LocaleNameToLCID(locale_name):
    if isinstance(locale_name, str):
        if PY3:
            pass
            # locale_name = locale_name.encode('utf-8')
        else:
            # noinspection PyUnresolvedReferences
            locale_name = unicode(locale_name)

    res = _LocaleNameToLCID(
        ctypes.create_string_buffer(locale_name),
        DWORD(0)
    )
    if res == 0:
        return None
    return res


def LCIDToLocaleName(lcid):
    if not isinstance(lcid, LCID):
        lcid = LCID(lcid)

    lpName = (ctypes.c_wchar * 0)()
    cchName = INT(0)
    dwFlags = DWORD(0)

    cchName = _LCIDToLocaleName(lcid, lpName, cchName, dwFlags)

    if not cchName:
        return

    lpName = (ctypes.c_wchar * cchName)()
    _LCIDToLocaleName(lcid, lpName, cchName, dwFlags)

    output = ''
    for i in range(cchName):
        char = lpName[i]
        if char in ('\x00', 0x0):
            break

        output += char

    return output


def GetLocaleInfoEx(lp_locale_name, lc_type):
    if not isinstance(lc_type, LCTYPE):
        lc_type = LCTYPE(lc_type)

    lp_lc_data = (ctypes.c_wchar * 0)()

    cch_data = _GetLocaleInfoEx(
        LPCWSTR(lp_locale_name),
        lc_type,
        lp_lc_data,
        0
    )
    if cch_data == 0:
        return ''

    lp_lc_data = (ctypes.c_wchar * cch_data)()
    res = _GetLocaleInfoEx(
        LPCWSTR(lp_locale_name),
        lc_type,
        lp_lc_data,
        cch_data
    )

    if res == 0:
        raise ctypes.WinError()

    output = ''
    for i in range(res):
        char = lp_lc_data[i]
        if char in ('\x00', 0x0):
            break

        output += char

    try:
        return int(output)
    except ValueError:
        return output


def LCIDFROMLANGID(lang_id):
    return LCID(lang_id)


def LANGIDFROMLCID(lcid):
    return LANGID(lcid.value)


def GetInfo(index, cat=wx.LOCALE_CAT_DEFAULT):
    locale = wx.GetLocale()

    def get_defaults():
        if index == wx.LOCALE_THOUSANDS_SEP:
            return ''
        if index == wx.LOCALE_DECIMAL_POINT:
            return '.'
        if index == wx.LOCALE_SHORT_DATE_FMT:
            return '%m/%d/%y'
        if index == wx.LOCALE_LONG_DATE_FMT:
            return '%A, %B %d, %Y'
        if index == wx.LOCALE_TIME_FMT:
            return '%H:%M:%S'
        if index == wx.LOCALE_DATE_TIME_FMT:
            return '%m/%d/%y %H:%M:%S'

        raise RuntimeError

    res = GetLocaleInfo(locale.CanonicalName.replace('_', '-'), index, cat)

    if not res and index in (
        wx.LOCALE_SHORT_DATE_FMT,
        wx.LOCALE_LONG_DATE_FMT,
        wx.LOCALE_TIME_FMT,
        wx.LOCALE_DATE_TIME_FMT
    ):
        return get_defaults()

    return res


def GetSystemLanguage():
    return GetThreadUILanguage().replace('-', '_')


wx.Locale.GetSystemLanguage = staticmethod(GetSystemLanguage)
wx.Locale.GetInfo = staticmethod(GetInfo)

# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2019 EventGhost Project <http://www.eventghost.net/>
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

import locale as _locale
import os
from functools import update_wrapper
from . import code_pages
from . import win_api


_original_getdefaultlocale = _locale.getdefaultlocale
_original_getlocale = _locale.getlocale
_original_setlocale = _locale.setlocale
_original_resetlocale = _locale.resetlocale


def getdefaultlocale(envvars=('LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE')):
    try:
        import _locale as _locale_

        code, encoding = _locale_._getdefaultlocale()

        if code and code[:2] == "0x":
            code = _locale.windows_locale.get(int(code, 0))

        if encoding.startswith('cp'):
            encoding = code_pages.CODE_PAGES.get(int(encoding[2:]), encoding)

        res = (code, encoding)

    except (ImportError, AttributeError):
        for variable in envvars:
            localename = os.environ.get(variable, None)
            if localename:
                if variable == 'LANGUAGE':
                    localename = localename.split(':')[0]
                break
        else:
            localename = 'C'

        res = _locale._parse_localename(localename)

    return res


def getlocale(category=_locale.LC_CTYPE):

    localename = _locale._setlocale(category)
    if category == _locale.LC_ALL and ';' in localename:
        raise TypeError('category LC_ALL is not supported')

    locale = _locale._parse_localename(localename)

    code_page = locale[1]

    if code_page.isdigit() and int(code_page) in code_pages.CODE_PAGES:
        code_page = code_pages.CODE_PAGES[int(code_page)]

    return locale[0], code_page


def try_locale(category, locale):
    try:
        return _locale._setlocale(category, locale)
    except _locale.Error:
        return False


def setlocale(category, locale=None):
    if locale and not isinstance(locale, (_locale._str, _locale._unicode)):
        locale = _locale.normalize(_locale._build_localename(locale))

    res = try_locale(category, locale)
    if res is False:
        if '.' in locale:
            locale, code_page = locale.split('.')
            code_page = '.' + code_page
        else:
            code_page = ''

        iso_code = locale.replace('_', '-')
        lang_name = win_api.GetLocaleInfoEx(
            iso_code,
            win_api.LOCALE_SENGLISHLANGUAGENAME
        )
        country_name = win_api.GetLocaleInfoEx(
            iso_code,
            win_api.LOCALE_SENGLISHCOUNTRYNAME
        )

        locale = lang_name + '_' + country_name + code_page

        res = try_locale(category, locale)

        if res is False:
            code_page = code_page.replace('cp', '').replace('windows-', '')
            locale = lang_name + '_' + country_name + code_page

            res = try_locale(category, locale)

    if res is False:
        raise

    return res


def resetlocale(category=_locale.LC_ALL):
    setlocale(category, _locale._build_localename(_locale.getdefaultlocale()))


_locale.setlocale = update_wrapper(setlocale, _locale.setlocale)
_locale.getlocale = update_wrapper(getlocale, _locale.getlocale)
_locale.getdefaultlocale = update_wrapper(getdefaultlocale, _locale.getdefaultlocale)
_locale.resetlocale = update_wrapper(resetlocale, _locale.resetlocale)

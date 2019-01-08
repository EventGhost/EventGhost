# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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
"""
This module handles all of the internationalism for EventGhost.
It will translate text to the language the language the user has selected
to display in EG.

This module supports

Countries 250
Languages 157
Country Language combinations 391

The wx module 172 country language combinations
Windows 7 w/o language packs 150 of 391 country language combinations
wxPython supports 128 of the 150 that Windows 7 w/o language packs supports

So the final number is 128 locale variations EG now supports.
"""
from __future__ import print_function
import wx
import os
import ctypes
import codecs
import types
import requests
import threading
from HTMLParser import HTMLParser
from ctypes.wintypes import LCID, DWORD, INT, WCHAR

if __name__ == '__main__':
    eg = None
    DecodeReST = None
    DecodeMarkdown = None

else:
    import eg
    from eg.Utils import DecodeReST, DecodeMarkdown


YANDEX_URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
YANDEX_API_KEY = (
    'trnsl.1.1.'
    '20181221T135822Z.'
    'fdd049052ddbbaf8.'
    'e96f9e106aee8f89cc2e5c75e9280eda01e41034'
)
ESCAPE_CODES = {
    '!': '%21',
    '#': '%23',
    '$': '%24',
    "'": '%27',
    '(': '%28',
    ')': '%29',
    '*': '%2A',
    '+': '%2B',
    ',': '%2C',
    '/': '%2F',
    ':': '%3A',
    ';': '%3B',
    '=': '%3D',
    '?': '%3F',
    '@': '%40',
    '[': '%5B',
    ']': '%5D',
    '\n': '%0A',
    ' ': '%20',
    '"': '%22',
    '.': '%2E',
    '<': '%3C',
    '>': '%3E',
    '\\': '%5C',
    '^': '%5E',
    '_': '%5F',
    '`': '%60',
    '{': '%7B',
    '|': '%7C',
    '}': '%7D',
    '~': '%7E'
}


LCID_TO_WX = {

    # Default custom sublanguage
    # sub: SUBLANG_CUSTOM_DEFAULT primary: LANG_NEUTRAL
    0x0C00: wx.LANGUAGE_DEFAULT,

    # no x-ref wx.LANGUAGE_ABKHAZIAN
    # no x-ref wx.LANGUAGE_AFAR

    # South Africa (ZA)
    # sub: SUBLANG_AFRIKAANS_SOUTH_AFRICA primary: LANG_AFRIKAANS
    0x0436: wx.LANGUAGE_AFRIKAANS,

    # Albania (AL)
    # sub: SUBLANG_ALBANIAN_ALBANIA primary: LANG_ALBANIAN
    0x041C: wx.LANGUAGE_ALBANIAN,

    # Ethiopia (ET)
    # sub: SUBLANG_AMHARIC_ETHIOPIA primary: LANG_AMHARIC
    0x045E: wx.LANGUAGE_AMHARIC,

    # Algeria (DZ)
    # sub: SUBLANG_ARABIC_ALGERIA primary: LANG_ARABIC
    0x1401: wx.LANGUAGE_ARABIC_ALGERIA,

    # Bahrain (BH)
    # sub: SUBLANG_ARABIC_BAHRAIN primary: LANG_ARABIC
    0x3C01: wx.LANGUAGE_ARABIC_BAHRAIN,

    # Egypt (EG)
    # sub: SUBLANG_ARABIC_EGYPT primary: LANG_ARABIC
    0x0C01: wx.LANGUAGE_ARABIC_EGYPT,

    # Iraq (IQ)
    # sub: SUBLANG_ARABIC_IRAQ primary: LANG_ARABIC
    0x0801: wx.LANGUAGE_ARABIC_IRAQ,

    # Jordan (JO)
    # sub: SUBLANG_ARABIC_JORDAN primary: LANG_ARABIC
    0x2C01: wx.LANGUAGE_ARABIC_JORDAN,

    # Kuwait (KW)
    # sub: SUBLANG_ARABIC_KUWAIT primary: LANG_ARABIC
    0x3401: wx.LANGUAGE_ARABIC_KUWAIT,

    # Lebanon (LB)
    # sub: SUBLANG_ARABIC_LEBANON primary: LANG_ARABIC
    0x3001: wx.LANGUAGE_ARABIC_LEBANON,

    # Libya (LY)
    # sub: SUBLANG_ARABIC_LIBYA primary: LANG_ARABIC
    0x1001: wx.LANGUAGE_ARABIC_LIBYA,

    # Morocco (MA)
    # sub: SUBLANG_ARABIC_MOROCCO primary: LANG_ARABIC
    0x1801: wx.LANGUAGE_ARABIC_MOROCCO,

    # Oman (OM)
    # sub: SUBLANG_ARABIC_OMAN primary: LANG_ARABIC
    0x2001: wx.LANGUAGE_ARABIC_OMAN,

    # Qatar (QA)
    # sub: SUBLANG_ARABIC_QATAR primary: LANG_ARABIC
    0x4001: wx.LANGUAGE_ARABIC_QATAR,

    # Saudi Arabia (SA)
    # sub: SUBLANG_ARABIC_SAUDI_ARABIA primary: LANG_ARABIC
    0x0401: wx.LANGUAGE_ARABIC_SAUDI_ARABIA,

    # no x-ref wx.LANGUAGE_ARABIC_SUDAN

    # Syria (SY)
    # sub: SUBLANG_ARABIC_SYRIA primary: LANG_ARABIC
    0x2801: wx.LANGUAGE_ARABIC_SYRIA,

    # Tunisia (TN)
    # sub: SUBLANG_ARABIC_TUNISIA primary: LANG_ARABIC
    0x1C01: wx.LANGUAGE_ARABIC_TUNISIA,

    # U.A.E. (AE)
    # sub: SUBLANG_ARABIC_UAE primary: LANG_ARABIC
    0x3801: wx.LANGUAGE_ARABIC_UAE,

    # Yemen (YE)
    # sub: SUBLANG_ARABIC_YEMEN primary: LANG_ARABIC
    0x2401: wx.LANGUAGE_ARABIC_YEMEN,

    # Armenia (AM)
    # sub: SUBLANG_ARMENIAN_ARMENIA primary: LANG_ARMENIAN
    0x042B: wx.LANGUAGE_ARMENIAN,

    # India (IN)
    # sub: SUBLANG_ASSAMESE_INDIA primary: LANG_ASSAMESE
    0x044D: wx.LANGUAGE_ASSAMESE,

    # no x-ref wx.LANGUAGE_ASTURIAN
    # no x-ref wx.LANGUAGE_AYMARA

    # Azerbaijan, Cyrillic (AZ)
    # sub: SUBLANG_AZERI_CYRILLIC primary: LANG_AZERI
    0x082C: wx.LANGUAGE_AZERI_CYRILLIC,

    # Azerbaijan, Latin (AZ)
    # sub: SUBLANG_AZERI_LATIN primary: LANG_AZERI
    0x042C: wx.LANGUAGE_AZERI_LATIN,

    # Russia (RU)
    # sub: SUBLANG_BASHKIR_RUSSIA primary: LANG_BASHKIR
    0x046D: wx.LANGUAGE_BASHKIR,

    # Basque (Basque)
    # sub: SUBLANG_BASQUE_BASQUE primary: LANG_BASQUE
    0x042D: wx.LANGUAGE_BASQUE,

    # Belarus (BY)
    # sub: SUBLANG_BELARUSIAN_BELARUS primary: LANG_BELARUSIAN
    0x0423: wx.LANGUAGE_BELARUSIAN,

    # no x-ref wx.LANGUAGE_BENGALI
    # no x-ref wx.LANGUAGE_BHUTANI
    # no x-ref wx.LANGUAGE_BIHARI
    # no x-ref wx.LANGUAGE_BISLAMA

    # Bosnia and Herzegovina, Cyrillic (BA)
    # sub:  primary: LANG_BOSNIAN_NEUTRAL
    # 0x781A: wx.LANGUAGE_BOSNIAN,

    # France (FR)
    # sub: SUBLANG_BRETON_FRANCE primary: LANG_BRETON
    0x047E: wx.LANGUAGE_BRETON,

    # Bulgaria (BG)
    # sub: SUBLANG_BULGARIAN_BULGARIA primary: LANG_BULGARIAN
    0x0402: wx.LANGUAGE_BULGARIAN,

    # no x-ref wx.LANGUAGE_BURMESE

    # Iraq (IQ)
    # sub: SUBLANG_CENTRAL_KURDISH_IRAQ primary: LANG_CENTRAL_KURDISH
    0x0492: wx.LANGUAGE_KURDISH,

    # no x-ref wx.LANGUAGE_CAMBODIAN

    # Spain (ES)
    # sub: SUBLANG_CATALAN_CATALAN primary: LANG_CATALAN
    0x0403: wx.LANGUAGE_CATALAN,

    # Hong Kong SAR, PRC (HK)
    # sub: SUBLANG_CHINESE_HONGKONG primary: LANG_CHINESE
    0x0C04: wx.LANGUAGE_CHINESE_HONGKONG,

    # Macao SAR (MO)
    # sub: SUBLANG_CHINESE_MACAU primary: LANG_CHINESE
    0x1404: wx.LANGUAGE_CHINESE_MACAU,

    # Singapore (SG)
    # sub: SUBLANG_CHINESE_SINGAPORE primary: LANG_CHINESE
    0x1004: wx.LANGUAGE_CHINESE_SINGAPORE,

    # Simplified (Hans)
    # sub: SUBLANG_CHINESE_SIMPLIFIED primary: LANG_CHINESE_SIMPLIFIED
    0x0004: wx.LANGUAGE_CHINESE_SIMPLIFIED,

    # no x-ref wx.LANGUAGE_CHINESE_TAIWAN

    # Traditional (Hant)
    # sub: SUBLANG_CHINESE_TRADITIONAL primary: LANG_CHINESE_TRADITIONAL
    0x7C04: wx.LANGUAGE_CHINESE_TRADITIONAL,

    # France (FR)
    # sub: SUBLANG_CORSICAN_FRANCE primary: LANG_CORSICAN
    0x0483: wx.LANGUAGE_CORSICAN,

    # Croatia (HR)
    # sub: SUBLANG_CROATIAN_CROATIA primary: LANG_CROATIAN
    0x041A: wx.LANGUAGE_CROATIAN,

    # Czech Republic (CZ)
    # sub: SUBLANG_CZECH_CZECH_REPUBLIC primary: LANG_CZECH
    0x0405: wx.LANGUAGE_CZECH,

    # Denmark (DK)
    # sub: SUBLANG_DANISH_DENMARK primary: LANG_DANISH
    0x0406: wx.LANGUAGE_DANISH,

    # Netherlands (NL)
    # sub: SUBLANG_DUTCH primary: LANG_DUTCH
    0x0413: wx.LANGUAGE_DUTCH,

    # Belgium (BE)
    # sub: SUBLANG_DUTCH_BELGIAN primary: LANG_DUTCH
    0x0813: wx.LANGUAGE_DUTCH_BELGIAN,

    # Australia (AU)
    # sub: SUBLANG_ENGLISH_AUS primary: LANG_ENGLISH
    0x0C09: wx.LANGUAGE_ENGLISH_AUSTRALIA,

    # Belize (BZ)
    # sub: SUBLANG_ENGLISH_BELIZE primary: LANG_ENGLISH
    0x2809: wx.LANGUAGE_ENGLISH_BELIZE,

    # no x-ref wx.LANGUAGE_ENGLISH_BOTSWANA

    # Canada (CA)
    # sub: SUBLANG_ENGLISH_CAN primary: LANG_ENGLISH
    0x1009: wx.LANGUAGE_ENGLISH_CANADA,

    # Caribbean (029)
    # sub: SUBLANG_ENGLISH_CARIBBEAN primary: LANG_ENGLISH
    0x2409: wx.LANGUAGE_ENGLISH_CARIBBEAN,

    # no x-ref wx.LANGUAGE_ENGLISH_DENMARK

    # Ireland (IE); see note 3
    # sub: SUBLANG_ENGLISH_EIRE primary: LANG_ENGLISH
    0x1809: wx.LANGUAGE_ENGLISH_EIRE,

    # Jamaica (JM)
    # sub: SUBLANG_ENGLISH_JAMAICA primary: LANG_ENGLISH
    0x2009: wx.LANGUAGE_ENGLISH_JAMAICA,

    # Malaysia (MY)
    # sub: SUBLANG_ENGLISH_MALAYSIA primary: LANG_ENGLISH
    0x4409: wx.LANGUAGE_MALAY,

    # New Zealand (NZ)
    # sub: SUBLANG_ENGLISH_NZ primary: LANG_ENGLISH
    0x1409: wx.LANGUAGE_ENGLISH_NEW_ZEALAND,

    # Philippines (PH)
    # sub: SUBLANG_ENGLISH_PHILIPPINES primary: LANG_ENGLISH
    0x3409: wx.LANGUAGE_ENGLISH_PHILIPPINES,

    # South Africa (ZA)
    # sub: SUBLANG_ENGLISH_SOUTH_AFRICA primary: LANG_ENGLISH
    0x1c09: wx.LANGUAGE_ENGLISH_SOUTH_AFRICA,

    # Trinidad and Tobago (TT)
    # sub: SUBLANG_ENGLISH_TRINIDAD primary: LANG_ENGLISH
    0x2C09: wx.LANGUAGE_ENGLISH_TRINIDAD,

    # United Kingdom (GB)
    # sub: SUBLANG_ENGLISH_UK primary: LANG_ENGLISH
    0x0809: wx.LANGUAGE_ENGLISH_UK,

    # United States (US)
    # sub: SUBLANG_ENGLISH_US primary: LANG_ENGLISH
    0x0409: wx.LANGUAGE_ENGLISH_US,

    # Zimbabwe (ZW)
    # sub: SUBLANG_ENGLISH_ZIMBABWE primary: LANG_ENGLISH
    0x3009: wx.LANGUAGE_ENGLISH_ZIMBABWE,

    # no x-ref wx.LANGUAGE_ESPERANTO

    # Estonia (EE)
    # sub: SUBLANG_ESTONIAN_ESTONIA primary: LANG_ESTONIAN
    0x0425: wx.LANGUAGE_ESTONIAN,

    # Faroe Islands (FO)
    # sub: SUBLANG_FAEROESE_FAROE_ISLANDS primary: LANG_FAEROESE
    0x0438: wx.LANGUAGE_FAEROESE,

    # no x-ref wx.LANGUAGE_FARSI
    # no x-ref wx.LANGUAGE_FIJI

    # Finland (FI)
    # sub: SUBLANG_FINNISH_FINLAND primary: LANG_FINNISH
    0x040B: wx.LANGUAGE_FINNISH,

    # Belgium (BE)
    # sub: SUBLANG_FRENCH_BELGIAN primary: LANG_FRENCH
    0x080c: wx.LANGUAGE_FRENCH_BELGIAN,

    # Canada (CA)
    # sub: SUBLANG_FRENCH_CANADIAN primary: LANG_FRENCH
    0x0C0C: wx.LANGUAGE_FRENCH_CANADIAN,

    # France (FR)
    # sub: SUBLANG_FRENCH primary: LANG_FRENCH
    0x040c: wx.LANGUAGE_FRENCH,

    # Luxembourg (LU)
    # sub: SUBLANG_FRENCH_LUXEMBOURG primary: LANG_FRENCH
    0x140C: wx.LANGUAGE_FRENCH_LUXEMBOURG,

    # Monaco (MC)
    # sub: SUBLANG_FRENCH_MONACO primary: LANG_FRENCH
    0x180C: wx.LANGUAGE_FRENCH_MONACO,

    # Switzerland (CH)
    # sub: SUBLANG_FRENCH_SWISS primary: LANG_FRENCH
    0x100C: wx.LANGUAGE_FRENCH_SWISS,

    # Netherlands (NL)
    # sub: SUBLANG_FRISIAN_NETHERLANDS primary: LANG_FRISIAN
    0x0462: wx.LANGUAGE_FRISIAN,

    # Spain (ES)
    # sub: SUBLANG_GALICIAN_GALICIAN primary: LANG_GALICIAN
    0x0456: wx.LANGUAGE_GALICIAN,

    # Georgia (GE)
    # sub: SUBLANG_GEORGIAN_GEORGIA primary: LANG_GEORGIAN
    0x0437: wx.LANGUAGE_GEORGIAN,

    # Austria (AT)
    # sub: SUBLANG_GERMAN_AUSTRIAN primary: LANG_GERMAN
    0x0C07: wx.LANGUAGE_GERMAN_AUSTRIAN,

    # Germany (DE)
    # sub: SUBLANG_GERMAN primary: LANG_GERMAN
    0x0407: wx.LANGUAGE_GERMAN,

    # no x-ref wx.LANGUAGE_GERMAN_BELGIUM

    # Liechtenstein (LI)
    # sub: SUBLANG_GERMAN_LIECHTENSTEIN primary: LANG_GERMAN
    0x1407: wx.LANGUAGE_GERMAN_LIECHTENSTEIN,

    # Luxembourg (LU)
    # sub: SUBLANG_GERMAN_LUXEMBOURG primary: LANG_GERMAN
    0x1007: wx.LANGUAGE_GERMAN_LUXEMBOURG,

    # Switzerland (CH)
    # sub: SUBLANG_GERMAN_SWISS primary: LANG_GERMAN
    0x0807: wx.LANGUAGE_GERMAN_SWISS,

    # Greece (GR)
    # sub: SUBLANG_GREEK_GREECE primary: LANG_GREEK
    0x0408: wx.LANGUAGE_GREEK,

    # Greenland (GL)
    # sub: SUBLANG_GREENLANDIC_GREENLAND primary: LANG_GREENLANDIC
    0x046F: wx.LANGUAGE_GREENLANDIC,

    # no x-ref wx.LANGUAGE_GUARANI

    # India (IN)
    # sub: SUBLANG_GUJARATI_INDIA primary: LANG_GUJARATI
    0x0447: wx.LANGUAGE_GUJARATI,

    # Nigeria (NG)
    # sub: SUBLANG_HAUSA_NIGERIA_LATIN primary: LANG_HAUSA
    0x0468: wx.LANGUAGE_HAUSA,

    # Israel (IL)
    # sub: SUBLANG_HEBREW_ISRAEL primary: LANG_HEBREW
    0x040D: wx.LANGUAGE_HEBREW,

    # India (IN)
    # sub: SUBLANG_HINDI_INDIA primary: LANG_HINDI
    0x0439: wx.LANGUAGE_HINDI,

    # Hungary (HU)
    # sub: SUBLANG_HUNGARIAN_HUNGARY primary: LANG_HUNGARIAN
    0x040E: wx.LANGUAGE_HUNGARIAN,

    # Iceland (IS)
    # sub: SUBLANG_ICELANDIC_ICELAND primary: LANG_ICELANDIC
    0x040F: wx.LANGUAGE_ICELANDIC,

    # Indonesia (ID)
    # sub: SUBLANG_INDONESIAN_INDONESIA primary: LANG_INDONESIAN
    0x0421: wx.LANGUAGE_INDONESIAN,

    # no x-ref wx.LANGUAGE_INTERLINGUA
    # no x-ref wx.LANGUAGE_INTERLINGUE

    # Canada (CA), Latin
    # sub: SUBLANG_INUKTITUT_CANADA_LATIN primary: LANG_INUKTITUT
    0x085D: wx.LANGUAGE_INUKTITUT,

    # no x-ref wx.LANGUAGE_INUPIAK

    # Ireland (IE)
    # sub: SUBLANG_IRISH_IRELAND primary: LANG_IRISH
    0x083C: wx.LANGUAGE_IRISH,

    # South Africa (ZA)
    # sub: SUBLANG_XHOSA_SOUTH_AFRICA primary: LANG_XHOSA
    0x0434: wx.LANGUAGE_XHOSA,

    # South Africa (ZA)
    # sub: SUBLANG_ZULU_SOUTH_AFRICA primary: LANG_ZULU
    0x0435: wx.LANGUAGE_ZULU,

    # Italy (IT)
    # sub: SUBLANG_ITALIAN primary: LANG_ITALIAN
    0x0410: wx.LANGUAGE_ITALIAN,

    # Switzerland (CH)
    # sub: SUBLANG_ITALIAN_SWISS primary: LANG_ITALIAN
    0x0810: wx.LANGUAGE_ITALIAN_SWISS,

    # Japan (JP)
    # sub: SUBLANG_JAPANESE_JAPAN primary: LANG_JAPANESE
    0x0411: wx.LANGUAGE_JAPANESE,

    # no x-ref wx.LANGUAGE_JAVANESE
    # no x-ref wx.LANGUAGE_KABYLE

    # India (IN)
    # sub: SUBLANG_KANNADA_INDIA primary: LANG_KANNADA
    0x044B: wx.LANGUAGE_KANNADA,

    # no x-ref wx.LANGUAGE_KASHMIRI

    # (reserved)
    # sub: SUBLANG_KASHMIRI_INDIA primary: LANG_KASHMIRI
    # ______: wx.LANGUAGE_KASHMIRI_INDIA,

    # Kazakhstan (KZ)
    # sub: SUBLANG_KAZAK_KAZAKHSTAN primary: LANG_KAZAK
    0x043F: wx.LANGUAGE_KAZAKH,

    # no x-ref wx.LANGUAGE_KERNEWEK

    # Rwanda (RW)
    # sub: SUBLANG_KINYARWANDA_RWANDA primary: LANG_KINYARWANDA
    0x0487: wx.LANGUAGE_KINYARWANDA,

    # no x-ref wx.LANGUAGE_KIRGHIZ
    # no x-ref wx.LANGUAGE_KIRUNDI

    # India (IN)
    # sub: SUBLANG_KONKANI_INDIA primary: LANG_KONKANI
    0x0457: wx.LANGUAGE_KONKANI,

    # Korea (KR)
    # sub: SUBLANG_KOREAN primary: LANG_KOREAN
    0x0412: wx.LANGUAGE_KOREAN,

    # no x-ref wx.LANGUAGE_LAOTHIAN

    # Latvia (LV)
    # sub: SUBLANG_LATVIAN_LATVIA primary: LANG_LATVIAN
    0x0426: wx.LANGUAGE_LATVIAN,

    # no x-ref wx.LANGUAGE_LINGALA

    # Lithuanian (LT); see note 5
    # sub: SUBLANG_LITHUANIAN_LITHUANIA primary: LANG_LITHUANIAN
    0x0427: wx.LANGUAGE_LITHUANIAN,

    # Macedonia (FYROM) (MK)
    # sub: SUBLANG_MACEDONIAN_MACEDONIA primary: LANG_MACEDONIAN
    0x042F: wx.LANGUAGE_MACEDONIAN,

    # Brunei Darassalam (BN)
    # sub: SUBLANG_MALAY_BRUNEI_DARUSSALAM primary: LANG_MALAY
    0x083E: wx.LANGUAGE_MALAY_BRUNEI_DARUSSALAM,

    # Malaysia (MY)
    # sub: SUBLANG_MALAY_MALAYSIA primary: LANG_MALAY
    0x043e: wx.LANGUAGE_MALAY_MALAYSIA,

    # no x-ref wx.LANGUAGE_MALAGASY

    # India (IN)
    # sub: SUBLANG_MALAYALAM_INDIA primary: LANG_MALAYALAM
    0x044C: wx.LANGUAGE_MALAYALAM,

    # Malta (MT)
    # sub: SUBLANG_MALTESE_MALTA primary: LANG_MALTESE
    0x043A: wx.LANGUAGE_MALTESE,

    # no x-ref wx.LANGUAGE_MANIPURI

    # New Zealand (NZ)
    # sub: SUBLANG_MAORI_NEW_ZEALAND primary: LANG_MAORI
    0x0481: wx.LANGUAGE_MAORI,

    # India (IN)
    # sub: SUBLANG_MARATHI_INDIA primary: LANG_MARATHI
    0x044E: wx.LANGUAGE_MARATHI,

    # no x-ref wx.LANGUAGE_MOLDAVIAN

    # Mongolia, Mong (MN)
    # sub: SUBLANG_MONGOLIAN_PRC primary: LANG_MONGOLIAN
    0x0850: wx.LANGUAGE_MONGOLIAN,

    # no x-ref wx.LANGUAGE_NAURU

    # Nepal (NP)
    # sub: SUBLANG_NEPALI_NEPAL primary: LANG_NEPALI
    0x0461: wx.LANGUAGE_NEPALI,

    # no x-ref wx.LANGUAGE_NEPALI_INDIA

    # Bokmål, Norway (NO)
    # sub: SUBLANG_NORWEGIAN_BOKMAL primary: LANG_NORWEGIAN
    0x0414: wx.LANGUAGE_NORWEGIAN_BOKMAL,

    # Nynorsk, Norway (NO)
    # sub: SUBLANG_NORWEGIAN_NYNORSK primary: LANG_NORWEGIAN
    0x0814: wx.LANGUAGE_NORWEGIAN_NYNORSK,

    # France (FR)
    # sub: SUBLANG_OCCITAN_FRANCE primary: LANG_OCCITAN
    0x0482: wx.LANGUAGE_OCCITAN,

    # India (IN)
    # sub: SUBLANG_ORIYA_INDIA primary: LANG_ORIYA
    0x0448: wx.LANGUAGE_ORIYA,

    # no x-ref wx.LANGUAGE_OROMO

    # Afghanistan (AF)
    # sub: SUBLANG_PASHTO_AFGHANISTAN primary: LANG_PASHTO
    0x0463: wx.LANGUAGE_PASHTO,

    # Poland (PL)
    # sub: SUBLANG_POLISH_POLAND primary: LANG_POLISH
    0x0415: wx.LANGUAGE_POLISH,

    # Brazil (BR)
    # sub: SUBLANG_PORTUGUESE_BRAZILIAN primary: LANG_PORTUGUESE
    0x0416: wx.LANGUAGE_PORTUGUESE_BRAZILIAN,

    # Portugal (PT); see note 7
    # sub: SUBLANG_PORTUGUESE primary: LANG_PORTUGUESE
    0x0816: wx.LANGUAGE_PORTUGUESE,

    # India, Gurmukhi script (IN)
    # sub: SUBLANG_PUNJABI_INDIA primary: LANG_PUNJABI
    0x0446: wx.LANGUAGE_PUNJABI,

    # Bolivia (BO)
    # sub: SUBLANG_QUECHUA_BOLIVIA primary: LANG_QUECHUA
    0x046B: wx.LANGUAGE_QUECHUA,

    # no x-ref wx.LANGUAGE_RHAETO_ROMANCE

    # Romania (RO)
    # sub: SUBLANG_ROMANIAN_ROMANIA primary: LANG_ROMANIAN
    0x0418: wx.LANGUAGE_ROMANIAN,

    # Russia (RU)
    # sub: SUBLANG_RUSSIAN_RUSSIA primary: LANG_RUSSIAN
    0x0419: wx.LANGUAGE_RUSSIAN,

    # no x-ref wx.LANGUAGE_RUSSIAN_UKRAINE

    # Inari, Finland (FI)
    # sub: SUBLANG_SAMI_INARI_FINLAND primary: LANG_SAMI
    0x243B: wx.LANGUAGE_SAMI,

    # no x-ref wx.LANGUAGE_SAMOAN
    # no x-ref wx.LANGUAGE_SANGHO

    # India (IN)
    # sub: SUBLANG_SANSKRIT_INDIA primary: LANG_SANSKRIT
    0x044F: wx.LANGUAGE_SANSKRIT,

    # no x-ref wx.LANGUAGE_SCOTS_GAELIC

    # Serbian (sr)
    # sub:  primary: LANG_SERBIAN
    0x1a:   wx.LANGUAGE_SERBIAN,

    # no x-ref wx.LANGUAGE_SERBO_CROATIAN

    # Serbia and Montenegro (former), Cyrillic (CS)
    # sub: SUBLANG_SERBIAN_CYRILLIC primary: LANG_SERBIAN
    0x0C1A: wx.LANGUAGE_SERBIAN_CYRILLIC,

    # Serbia and Montenegro (former), Latin (CS)
    # sub: SUBLANG_SERBIAN_LATIN primary: LANG_SERBIAN
    0x081A: wx.LANGUAGE_SERBIAN_LATIN,

    # no x-ref wx.LANGUAGE_SESOTHO
    # no x-ref wx.LANGUAGE_SETSWANA
    # no x-ref wx.LANGUAGE_SHONA

    # (reserved)
    # sub: primary: LANG_TSWANA
    0x59:   wx.LANGUAGE_SINDHI,

    # Sri Lanka (LK)
    # sub: SUBLANG_SINHALESE_SRI_LANKA primary: LANG_SINHALESE
    0x045B: wx.LANGUAGE_SINHALESE,

    # no x-ref wx.LANGUAGE_SISWATI

    # Slovakia (SK)
    # sub: SUBLANG_SLOVAK_SLOVAKIA primary: LANG_SLOVAK
    0x041B: wx.LANGUAGE_SLOVAK,

    # Slovenia (SI)
    # sub: SUBLANG_SLOVENIAN_SLOVENIA primary: LANG_SLOVENIAN
    0x0424: wx.LANGUAGE_SLOVENIAN,

    # no x-ref wx.LANGUAGE_SOMALI

    # Spain, Traditional Sort (ES)
    # sub: SUBLANG_SPANISH primary: LANG_SPANISH
    0x040A: wx.LANGUAGE_SPANISH,

    # Bolivia (BO)
    # sub: SUBLANG_SPANISH_BOLIVIA primary: LANG_SPANISH
    0x400A: wx.LANGUAGE_SPANISH_BOLIVIA,

    # Chile (CL)
    # sub: SUBLANG_SPANISH_CHILE primary: LANG_SPANISH
    0x340A: wx.LANGUAGE_SPANISH_CHILE,

    # Colombia (CO)
    # sub: SUBLANG_SPANISH_COLOMBIA primary: LANG_SPANISH
    0x240A: wx.LANGUAGE_SPANISH_COLOMBIA,

    # Costa Rica (CR)
    # sub: SUBLANG_SPANISH_COSTA_RICA primary: LANG_SPANISH
    0x140A: wx.LANGUAGE_SPANISH_COSTA_RICA,

    # Dominican Republic (DO)
    # sub: SUBLANG_SPANISH_DOMINICAN_REPUBLIC primary: LANG_SPANISH
    0x1C0A: wx.LANGUAGE_SPANISH_DOMINICAN_REPUBLIC,

    # Ecuador (EC)
    # sub: SUBLANG_SPANISH_ECUADOR primary: LANG_SPANISH
    0x300A: wx.LANGUAGE_SPANISH_ECUADOR,

    # El Salvador (SV)
    # sub: SUBLANG_SPANISH_EL_SALVADOR primary: LANG_SPANISH
    0x440A: wx.LANGUAGE_SPANISH_EL_SALVADOR,

    # Guatemala (GT)
    # sub: SUBLANG_SPANISH_GUATEMALA primary: LANG_SPANISH
    0x100A: wx.LANGUAGE_SPANISH_GUATEMALA,

    # Honduras (HN)
    # sub: SUBLANG_SPANISH_HONDURAS primary: LANG_SPANISH
    0x480A: wx.LANGUAGE_SPANISH_HONDURAS,

    # Mexico (MX)
    # sub: SUBLANG_SPANISH_MEXICAN primary: LANG_SPANISH
    0x080A: wx.LANGUAGE_SPANISH_MEXICAN,

    # Nicaragua (NI)
    # sub: SUBLANG_SPANISH_NICARAGUA primary: LANG_SPANISH
    0x4C0A: wx.LANGUAGE_SPANISH_NICARAGUA,

    # Panama (PA)
    # sub: SUBLANG_SPANISH_PANAMA primary: LANG_SPANISH
    0x180A: wx.LANGUAGE_SPANISH_PANAMA,

    # Paraguay (PY)
    # sub: SUBLANG_SPANISH_PARAGUAY primary: LANG_SPANISH
    0x3C0A: wx.LANGUAGE_SPANISH_PARAGUAY,

    # Peru (PE)
    # sub: SUBLANG_SPANISH_PERU primary: LANG_SPANISH
    0x280A: wx.LANGUAGE_SPANISH_PERU,

    # Puerto Rico (PR)
    # sub: SUBLANG_SPANISH_PUERTO_RICO primary: LANG_SPANISH
    0x500A: wx.LANGUAGE_SPANISH_PUERTO_RICO,

    # Spain, Modern Sort (ES)
    # sub: SUBLANG_SPANISH_MODERN primary: LANG_SPANISH
    0x0C0A: wx.LANGUAGE_SPANISH_MODERN,

    # Argentina (AR)
    # sub: SUBLANG_SPANISH_ARGENTINA primary: LANG_SPANISH
    0x2C0A: wx.LANGUAGE_SPANISH_ARGENTINA,

    # United States (US)
    # sub: SUBLANG_SPANISH_US primary: LANG_SPANISH
    0x540A: wx.LANGUAGE_SPANISH_US,

    # Uruguay (UY)
    # sub: SUBLANG_SPANISH_URUGUAY primary: LANG_SPANISH
    0x380A: wx.LANGUAGE_SPANISH_URUGUAY,

    # Venezuela (VE)
    # sub: SUBLANG_SPANISH_VENEZUELA primary: LANG_SPANISH
    0x200A: wx.LANGUAGE_SPANISH_VENEZUELA,

    # no x-ref wx.LANGUAGE_SUNDANESE

    # Kenya (KE)
    # sub: SUBLANG_SWAHILI primary: LANG_SWAHILI
    0x0441: wx.LANGUAGE_SWAHILI,

    # Finland (FI)
    # sub: SUBLANG_SWEDISH_FINLAND primary: LANG_SWEDISH
    0x081D: wx.LANGUAGE_SWEDISH_FINLAND,

    # Sweden (SE); see note 8
    # sub: SUBLANG_SWEDISH primary: LANG_SWEDISH
    0x041D: wx.LANGUAGE_SWEDISH,

    # no x-ref wx.LANGUAGE_TAGALOG

    # Tajikistan, Cyrillic (TJ)
    # sub: SUBLANG_TAJIK_TAJIKISTAN primary: LANG_TAJIK
    0x0428: wx.LANGUAGE_TAJIK,

    # India (IN)
    # sub: SUBLANG_TAMIL_INDIA primary: LANG_TAMIL
    0x0449: wx.LANGUAGE_TAMIL,

    # Russia (RU)
    # sub: SUBLANG_TATAR_RUSSIA primary: LANG_TATAR
    0x0444: wx.LANGUAGE_TATAR,

    # India (IN)
    # sub: SUBLANG_TELUGU_INDIA primary: LANG_TELUGU
    0x044A: wx.LANGUAGE_TELUGU,

    # Thailand (TH)
    # sub: SUBLANG_THAI_THAILAND primary: LANG_THAI
    0x041E: wx.LANGUAGE_THAI,

    # PRC (CN)
    # sub: SUBLANG_TIBETAN_PRC primary: LANG_TIBETAN
    0x0451: wx.LANGUAGE_TIBETAN,

    # Eritrea (ER)
    # sub: SUBLANG_TIGRINYA_ERITREA primary: LANG_TIGRINYA
    0x0873: wx.LANGUAGE_TIGRINYA,

    # no x-ref wx.LANGUAGE_TONGA
    # no x-ref wx.LANGUAGE_TSONGA

    # Turkey (TR)
    # sub: SUBLANG_TURKISH_TURKEY primary: LANG_TURKISH
    0x041F: wx.LANGUAGE_TURKISH,

    # Turkmenistan (TM)
    # sub: SUBLANG_TURKMEN_TURKMENISTAN primary: LANG_TURKMEN
    0x0442: wx.LANGUAGE_TURKMEN,

    # no x-ref wx.LANGUAGE_TWI

    # Ukraine (UA)
    # sub: SUBLANG_UKRAINIAN_UKRAINE primary: LANG_UKRAINIAN
    0x0422: wx.LANGUAGE_UKRAINIAN,

    # (reserved)
    # sub: SUBLANG_URDU_INDIA primary: LANG_URDU
    0x0820: wx.LANGUAGE_URDU_INDIA,

    # Urdu (ur)
    # sub: primary: LANG_URDU
    0x20:   wx.LANGUAGE_URDU,

    # Pakistan (PK)
    # sub: SUBLANG_URDU_PAKISTAN primary: LANG_URDU
    0x0420: wx.LANGUAGE_URDU_PAKISTAN,

    # PRC (CN)
    # sub: SUBLANG_UIGHUR_PRC primary: LANG_UIGHUR
    0x0480: wx.LANGUAGE_UIGHUR,

    # Uzbek (uz)
    # sub: primary: LANG_UZBEK
    0x43:   wx.LANGUAGE_UZBEK,

    # Uzbekistan, Cyrillic (UZ)
    # sub: SUBLANG_UZBEK_CYRILLIC primary: LANG_UZBEK
    0x0843: wx.LANGUAGE_UZBEK_CYRILLIC,

    # Uzbekistan, Latin (UZ)
    # sub: SUBLANG_UZBEK_LATIN primary: LANG_UZBEK
    0x0443: wx.LANGUAGE_UZBEK_LATIN,

    # Valencia (ES-Valencia)
    # sub: SUBLANG_VALENCIAN_VALENCIA primary: LANG_VALENCIAN
    0x0803: wx.LANGUAGE_VALENCIAN,

    # Vietnam (VN)
    # sub: SUBLANG_VIETNAMESE_VIETNAM primary: LANG_VIETNAMESE
    0x042A: wx.LANGUAGE_VIETNAMESE,

    # no x-ref wx.LANGUAGE_VOLAPUK

    # United Kingdom (GB)
    # sub: SUBLANG_WELSH_UNITED_KINGDOM primary: LANG_WELSH
    0x0452: wx.LANGUAGE_WELSH,

    # Senegal (SN)
    # sub: SUBLANG_WOLOF_SENEGAL primary: LANG_WOLOF
    0x0488: wx.LANGUAGE_WOLOF,

    # no x-ref wx.LANGUAGE_YIDDISH

    # Nigeria (NG)
    # sub: SUBLANG_YORUBA_NIGERIA primary: LANG_YORUBA
    0x046A: wx.LANGUAGE_YORUBA,

    # no x-ref wx.LANGUAGE_ZHUANG
}

kernel32 = ctypes.windll.Kernel32

# LCID LocaleNameToLCID(
#   LPCWSTR lpName,
#   DWORD   dwFlags
# );
_LocaleNameToLCID = kernel32.LocaleNameToLCID
_LocaleNameToLCID.restype = LCID

# int LCIDToLocaleName(
#   LCID   Locale,
#   LPWSTR lpName,
#   int    cchName,
#   DWORD  dwFlags
# );
_LCIDToLocaleName = kernel32.LCIDToLocaleName
_LCIDToLocaleName.restype = INT

# LANGID GetUserDefaultUILanguage();
GetUserDefaultUILanguage = kernel32.GetUserDefaultUILanguage


# int GetUserDefaultLocaleName(
#   LPWSTR lpLocaleName,
#   int    cchLocaleName
# );

GetUserDefaultLocaleName = kernel32.GetUserDefaultLocaleName
GetUserDefaultLocaleName.restype = INT

LOCALE_NAME_MAX_LENGTH = 85
LOCALE_ALLOW_NEUTRAL_NAMES = 0x08000000


def get_windows_user_language():
    lpLocaleName = (WCHAR * LOCALE_NAME_MAX_LENGTH)()
    cchLocaleName = INT(LOCALE_NAME_MAX_LENGTH)

    if not GetUserDefaultLocaleName(ctypes.byref(lpLocaleName), cchLocaleName):
        raise ctypes.WinError()

    lpLocaleName = lpLocaleName.value.replace('-', '_')

    for cntry in countries:
        for lng in cntry.wx_languages:
            if lng.iso_code == lpLocaleName:
                eg.PrintDebugNotice(
                    'default user language (1): ' + lpLocaleName
                )
                return lng

    lcid = GetUserDefaultUILanguage()

    for cntry in countries:
        for lng in cntry.wx_languages:
            if lng.lcid == lcid:
                eg.PrintDebugNotice(
                    'default user language (2): ' + lng.iso_code
                )
                return lng

    for cntry in countries:
        if cntry.code == 'US':
            eg.PrintDebugNotice(
                'default user language (3): ' + cntry.wx_languages[0].iso_code
            )
            return cntry.wx_languages[0]


def local_name_to_lcid(locale_name):
    res = _LocaleNameToLCID(unicode(locale_name), DWORD(0))
    if res == 0:
        return None
    return res


def escape(s):
    s = s.split('\n')
    res = []
    return_s = []

    for line in s:
        rep = []
        res += [rep]

        if line.strip():
            while 'http://' in line:
                beg, end = line.split('http://', 1)
                cut = end.find(' ')
                if cut == -1:
                    cut = end.find('\n')

                if cut == -1:
                    rep += ['http://' + end]
                else:
                    rep += ['http://' + end[:cut]]

                line = beg + 'http://' + end
                line = line.replace(rep[-1], '~@', 1)

            while '{' in s and '}' in line:
                beg, end = line.split('{', 1)
                save, end = end.split('}', 1)
                save = '{' + '}'
                line = beg + '~@' + end
                rep += [save]

            line = line.replace('&', '!@')
            line = line.replace('-', '*!')

            for pattern, replacement in ESCAPE_CODES.items():
                line = line.replace(pattern, replacement)

        return_s += [line]

    return return_s, res


def unescape(s, reps):
    return_s = []

    if not isinstance(s, list):
        s = [s]

    for line in s:
        rep = reps.pop(0)

        for replacement, pattern in ESCAPE_CODES.items():
            line = line.replace(pattern, replacement)

        line = line.replace('%25', '%')

        for item in rep:
            line = line.replace('~@', item, 1)

        line = line.replace('-', ' ')
        line = line.replace('*!', '-')
        line = line.replace('!@', '&')

        return_s += [line]

    return '\n'.join(return_s)


def list_to_string(lst, indent):
    res = ''
    indent_string = '    ' * indent

    for itm in lst:
        if isinstance(itm, str):
            itm = itm.decode("latin-1")
            res += indent_string + my_repr(itm) + ',\n'

        elif isinstance(itm, unicode):
            res += indent_string + my_repr(itm) + ',\n'

        elif isinstance(itm, (list, tuple)):
            if isinstance(itm, list):
                braces = ['[\n', '],\n', '[],\n']
            else:
                braces = ['(\n', '),\n', '(),\n']

            tmp = list_to_string(itm, indent + 1)
            if tmp != '':
                res += indent_string + braces[0]
                res += tmp
                res += indent_string + braces[1]
            else:
                res += indent_string + braces[2]

        else:
            res += indent_string + repr(itm) + ',\n'

    if res:
        res = indent_string + res

    return res


def my_repr(value):
    value = value.replace("\n", "\\n")
    if value.count("'") < value.count('"'):
        value = value.replace("'", "\\'")
        return "u'%s'" % value
    else:
        value = value.replace('"', '\\"')
        return 'u"%s"' % value


def parse_html(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
        HTMLParser.__init__(self)

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return self.fed


class TextToTranslate(object):
    """
    This is the container object for the actual text to be translated.
    This is where the text will get split on the newline character and
    processed so it is able to be sent in a URL. we have to excape the text we
    are going to send. We also have to process any RST, HTML and Markdown data
    to remove all of the tags used. the translation service also strips off
    any leading spaces. so we have to replace these as they might cause issues
    with any of the above 3 text styles.

    """

    count = 0
    processed = 0
    in_processing = 0

    def __init__(self, original):
        self.original = original
        self.escaped_lines = []
        self.leading_spaces = []
        self.marked_inprocessing = False

        # recording any leading spaces.

        for line in original.split('\n'):
            self.leading_spaces += [len(line) - len(line.lstrip())]

        # this is where the text type is discovered
        # RST, HTML, Markdown, or none of the above
        # we then escape the text to be translated.
        # there are patters that are generated during the escaping process.
        # these patterns include the marker and a text block. During the
        # escaping process there are things we do not want to translate,
        # like URL's so we replace the URL with a marker and that marker and
        # the URL are handed back to be stored. after the translation has
        # taken place we then use the marker as an identifier so we can
        # insert the text back in. We have to use a marker and not a position
        # because the translated text will not be the same size. and we do not
        # want to insert the text into the wrong location.

        if original.startswith('<md>'):
            html_lines = parse_html(DecodeMarkdown(original[4:]))
            for line in html_lines:
                escaped, patterns = escape(line)

                self.escaped_lines += [
                    dict(
                        escaped=escaped,
                        patterns=patterns,
                        original=line
                    )
                ]
        elif original.startswith('<rst>'):
            html_lines = parse_html(DecodeReST(original[5:]))

            for line in html_lines:
                escaped, patterns = escape(line)

                self.escaped_lines += [
                    dict(
                        escaped=escaped,
                        patterns=patterns,
                        original=line
                    )
                ]
        elif '</' in original:
            html_lines = parse_html(original)

            for line in html_lines:
                escaped, patterns = escape(line)

                self.escaped_lines += [
                    dict(
                        escaped=escaped,
                        patterns=patterns,
                        original=line
                    )
                ]
        else:
            escaped, patterns = escape(original)
            self.escaped_lines += [
                dict(
                    escaped=escaped,
                    patterns=patterns,
                    original=original
                )
            ]

        for line in self.escaped_lines:

            TextToTranslate.count += len(line['patterns'])

    def __len__(self):
        # this calculates the number fo text blocks being added to the url.
        # it is also used in determining the number of translated text blocks
        # that need to be handed back.
        return len(self.url_parameters.split('&text=')) - 1

    @property
    def url_parameters(self):
        # this is where we build the parameters that get added to the URL.
        # this is also used to determine the number of text blocks that need
        # to be passed back. Because we want to maximize the number of
        # characters being sent there are more then one of thses text objects
        # used in a single URL. So this property also gets used to determine
        # the number of text blocks.
        params = ''
        processing_count = 0

        for escaped in self.escaped_lines:
            for line in escaped['escaped']:
                if line.strip():
                    params += '&text=' + line
                processing_count += len(escaped['patterns'])

        if not self.marked_inprocessing:
            self.marked_inprocessing = True
            TextToTranslate.in_processing += processing_count

        return params

    def __str__(self):
        return self.original

    def __unicode__(self, translated_lines):
        # This is where the translated text blocks get handed back to. we then
        # process those text blocks unescaping and adding back in any text
        # that was removed. In order to keep the current text type correct
        # whether it is RST, HTML, Markdown we replace the original text block
        # with the translated text block. this keeps all the tags in proper
        # place. we then split the output on the new_line strip any leading
        # spaces. and add back in the leading spaces we recorded when this
        # class was constructed.

        count = 0
        output = self.original

        for escaped in self.escaped_lines:
            for line in escaped['escaped']:
                if not line.strip():
                    translated_lines.insert(count, u'')
                count += 1

        for escaped in self.escaped_lines:
            patterns = escaped['patterns']
            num_lines = len(patterns)

            translated_text = []
            for _ in range(num_lines):
                try:
                    translated_text += [translated_lines.pop(0)]
                except IndexError:
                    break

            translated_text = unescape(translated_text, patterns)

            if escaped['original'].strip():
                output = output.replace(escaped['original'], translated_text)

            TextToTranslate.processed += len(
                escaped['patterns']
            )

        output = '\n'.join(
            ' ' * self.leading_spaces[i] + line.lstrip()
            for i, line in enumerate(output.split('\n'))
        )

        if TextToTranslate.in_processing:
            TextToTranslate.in_processing = 0

        return unicode(output)


class TextContainer(object):
    """
    Container object that represents an entry in  eg.text.
    This is the worker for parsing and translating. It checks the data type
    (list, tuple, dict, str, unicode) and if needs be iterates over the data
    to grab any string/unicode objects. it keeps a close watch on what is
    supposed to go where and puts the translated text back where it belongs.

    Because of how the translation service works it does not like dealing
    with new lines, so we split the text to be translated on the new line and
    add it to the parameters that are passed to the translation service.
    The translation service is limited in size to what the maximum URL allowed
    whick is 10K or 10240 bytes. I have shortened this up to 10000 bytes
    for the total URL.
    """

    # TODO: allow for text items to contain greater then the max allowed.

    def __init__(self, language, container, key):
        self.language = language
        self.container = container
        self.key = key
        self.original = getattr(container, key)
        self.processed = False

        # this is the discovery section. this is where the data type is
        # discovered and iterated over if necessary.

        # the previous version of he language handling did not allow
        # translations for dictionaries. This does. it also allows for
        # nested lists, tuples, dictionaries and any combination of
        # the previous 3.
        #
        # we want to preserve the exact location where the text is that needs
        # to be translated is. so we create a duplicate of the structure
        # adding None in replacement of any objects that are not text

        def list_iter(val):
            new_val = []

            for i, item in enumerate(val):
                if isinstance(item, (list, tuple)):
                    new_val += [list_iter(item)]

                elif isinstance(item, (str, unicode)):
                    new_val += [TextToTranslate(item)]

                elif isinstance(item, dict):
                    new_val += [dict_iter(item)]

            if isinstance(val, tuple):
                new_val = tuple(new_val)

            return new_val

        def dict_iter(val):
            new_val = {}

            for k, v in val.items():
                if isinstance(v, (list, tuple)):
                    new_val[k] = list_iter(v)

                elif isinstance(v, (str, unicode)):
                    new_val[k] = TextToTranslate(v)

                elif isinstance(v, dict):
                    new_val[k] = dict_iter(v)

            return new_val

        if isinstance(self.original, (tuple, list)):
            self.waiting_translation = list_iter(self.original)

        elif isinstance(self.original, dict):
            self.waiting_translation = dict_iter(self.original)

        elif isinstance(self.original, (str, unicode)):
            self.waiting_translation = TextToTranslate(self.original)
        else:
            self.waiting_translation = None

    def __len__(self):
        if self.processed:
            return 0

        return len(self.url_parameters.split('&text=')) - 1

    @property
    def url_parameters(self):
        # this is where we build the url parameters. if necessary we
        # iterate over the data. once that is done the url parameters are
        # built. we add the parameters to the rest of the url and check the
        # size. if the size is over the maximum allowed will will then create
        # a unique request to handle this one specific object. and we will
        # return no parameters in this case.

        if self.processed:
            return ''

        def get_url_from_value(val):
            if val is None:
                return ''
            if isinstance(val, (list, tuple)):
                return list_url(val)

            elif isinstance(val, dict):
                return dict_url(val)

            elif isinstance(val, TextToTranslate):
                return val.url_parameters

            return ''

        def list_url(ll):
            params = ''
            for value in ll:
                params += get_url_from_value(value)
            return params

        def dict_url(d):
            params = ''
            for key in sorted(d.keys()):
                value = d[key]
                params += get_url_from_value(value)

            return params

        url_params = get_url_from_value(self.waiting_translation)

        if len(self.language.translation_url + url_params) >= 10000:
            translated_lines = []

            url_params = list(
                '&text=' + p for p in url_params.split('&text=')[1:]
            )
            url = ''

            while url_params:
                param = url_params.pop(0)
                if len(self.language.translation_url + url + param) < 10000:
                    url += param

                elif url:
                    translated_lines += self.language.get_translation(url)
                    url = param
                else:
                    raise RuntimeError(
                        'Translation text is to large: ' + self.key
                    )

            if url:
                translated_lines += self.language.get_translation(url)

            self(translated_lines)
            return ''

        return url_params

    def __call__(self, translated_lines):
        # this is where we will put together all of te translated text and
        # replace the old object with the new.
        def get_lines(val):
            if val is None:
                return

            if isinstance(val, (list, tuple)):
                return list_lines(val)

            elif isinstance(val, dict):
                return dict_lines(val)

            elif isinstance(val, TextToTranslate):
                lines = []
                for _ in range(len(val)):
                    try:
                        lines += [translated_lines.pop(0)]
                    except IndexError:
                        break

                return val.__unicode__(lines)

            return val

        def list_lines(ll):
            new_value = []

            for value in ll:
                new_value += [get_lines(value)]

            if isinstance(ll, tuple):
                new_value = tuple(new_value)

            return new_value

        def dict_lines(d):
            new_value = {}

            for key in sorted(d.keys()):
                value = d[key]
                new_value[key] = get_lines(value)

            return new_value

        setattr(self.container, self.key, get_lines(self.waiting_translation))
        self.processed = True

    def __str__(self):
        return str(getattr(self.container, self.key)).encode('utf-8')

    def __unicode__(self):
        return unicode(getattr(self.container, self.key))


class Language(object):
    ISO639_1 = None
    ISO639_2 = None
    ISO639_3 = None
    english_name = ''
    native_name = u''
    _lcid = None

    def __init__(self, country_name):
        self.country_name = country_name
        self.locale_names = []
        self._text_to_translate = []
        self._translation_lock = threading.Lock()

    @property
    def lcid(self):
        if self._lcid is None:
            for locale_name in self.locale_names:
                lcid = local_name_to_lcid(locale_name)
                if lcid is not None:
                    return lcid
        else:
            return self._lcid

    @property
    def wx_code(self):
        lcid = self.lcid
        if lcid in LCID_TO_WX:
            return LCID_TO_WX[lcid]

    @property
    def iso_code(self):
        if self.ISO639_1 is not None:
            return self.ISO639_1
        if self.ISO639_2 is not None:
            return self.ISO639_2
        if self.ISO639_3 is not None:
            return self.ISO639_3

    @property
    def translation_url(self):
        u = YANDEX_URL
        u += '?key=' + YANDEX_API_KEY
        u += '&lang=en-' + self.iso_code
        u += '&format=plain'
        return u

    def get_translation(self, params):
        url = self.translation_url + params

        eg.PrintDebugNotice(url.encode('utf-8'))

        response = requests.get(url, timeout=10)
        try:
            eg.PrintDebugNotice(
                str(response.content).encode('utf-8')
            )
        except UnicodeDecodeError:
            eg.PrintDebugNotice(
                str(response.content).decode('latin-1').encode('utf-8')
            )
        response = response.json()

        return response['text']

    def _build_translation_containers(self, cls):
        translation_containers = []

        for key, value in cls.__dict__.items():
            if key.startswith('_'):
                continue

            if type(value) in (types.ClassType, types.InstanceType):
                translation_containers += (
                    self._build_translation_containers(value)
                )

            else:
                translation_containers += [TextContainer(self, cls, key)]

        return translation_containers

    def _process_translation_containers(self, translation_containers):
        params = ''
        used_containers = []
        translation_lines = []

        while translation_containers:

            container = translation_containers.pop(0)
            container_params = container.url_parameters

            if not container_params:
                used_containers += [container]

            elif len(self.translation_url + params + container_params) < 9500:
                params += container_params
                used_containers += [container]

            elif params:
                translation_lines += self.get_translation(params)
                params = container_params
                used_containers += [container]

            else:
                raise RuntimeError

        if params:
            translation_lines += self.get_translation(params)

        for container in used_containers:
            lines = list(
                translation_lines.pop(0) for _ in range(len(container))
            )
            container(lines)

    def _build_plugin_language_file(self, plugin_text):
        with self._translation_lock:
            translation_containers = (
                self._build_translation_containers(plugin_text)
            )

            self._process_translation_containers(translation_containers)

            return self.assemble_file_data(plugin_text)

    def _build_language_file(self):
        with self._translation_lock:
            eg.PrintDebugNotice(
                'Building language file: ' + self.iso_code + '.lang'
            )

            path = os.path.join(eg.languagesDir, 'en.lang')
            namespace = {}
            eg.ExecFile(path, {}, namespace)
            text = types.ClassType('Text', (), namespace)

            eg.PrintDebugNotice(
                'Creating translation containers...'
            )

            translation_containers = (
                self._build_translation_containers(text)
            )

            eg.PrintDebugNotice(
                'Processing translation containers...'
            )

            self._process_translation_containers(translation_containers)

            eg.PrintDebugNotice(
                'Creating language file output...'
            )

            translation_output = self.assemble_file_data(text)

            return text, translation_output

    def assemble_file_data(self, node, indent=0):
        res = []
        append = res.append
        indent_string = '    ' * indent

        classes = []
        for key, value in node.__dict__.items():
            if key.startswith('_'):
                continue

            if type(value) in (types.ClassType, types.InstanceType):
                classes += [key]

            elif isinstance(value, list):
                tmp = list_to_string(value, indent + 1)
                if tmp != "":
                    append(indent_string + key + " = [\n")
                    append(tmp)
                    append(indent_string + "]\n")
                else:
                    append(indent_string + key + " = []\n")

            elif isinstance(value, tuple):
                tmp = list_to_string(value, indent + 1)
                if tmp != "":
                    append(indent_string + key + " = (\n")
                    append(tmp)
                    append(indent_string + ")\n")
                else:
                    append(indent_string + key + " = ()\n")
            elif isinstance(value, str):
                value = value.decode("latin-1")
                append(indent_string + my_repr(value) + ",\n")
            elif isinstance(value, unicode):
                append(indent_string + key + ' = %s\n' % my_repr(value))
            else:
                append(indent_string + key + ' = %s\n' % repr(value))

        for cls_name in classes:
            tmp = self.assemble_file_data(node.__dict__[cls_name], indent + 1)
            if tmp != "":
                append('\n')
                if not indent_string:
                    append('\n')

                append(indent_string + "class %s:\n" % cls_name)
                append(tmp)

        return "".join(res)

    @property
    def is_available(self):
        path = os.path.join(eg.languagesDir, self.iso_code + '.lang')
        if not os.path.exists(path):
            path = os.path.join(
                eg.folderPath.ProgramData,
                'EventGhost',
                'languages',
                self.iso_code + '.lang'
            )

        return os.path.exists(path)

    def is_plugin_description_available(self, plugin):
        path = os.path.join(
            eg.folderPath.ProgramData,
            'EventGhost',
            'languages',
            plugin.pluginName,
            self.iso_code + '_description.lang'
        )

        return os.path.exists(path)

    def is_plugin_available(self, plugin):
        path = os.path.join(
            eg.folderPath.ProgramData,
            'EventGhost',
            'languages',
            plugin.pluginName,
            self.iso_code + '.lang'
        )

        return os.path.exists(path)

    @staticmethod
    def _get_plugin_name(plugin):
        try:
            return str(
                os.path.basename(plugin.path)
            ).encode('utf-8')
        except UnicodeDecodeError:
            return str(
                os.path.basename(plugin.path)
            ).decode('latin-1').encode('utf-8')

    def load_plugin(self, plugin):
        plugin_name = self._get_plugin_name(plugin)

        eg.PrintDebugNotice(
            'Loading plugin language file: ' +
            plugin_name +
            '\\' +
            self.iso_code + '.lang'
        )

        path = os.path.join(
            eg.folderPath.ProgramData,
            'EventGhost',
            'languages',
            plugin_name
        )

        if not os.path.exists(path):
            os.makedirs(path)

        description_path = os.path.join(
            path,
            self.iso_code + '_description.lang'
        )

        # try to translate name and description

        if not os.path.exists(description_path):
            namespace = dict(
                name=plugin.name,
                description=plugin.description
            )

            translation = types.ClassType(plugin_name, (), namespace)

            if self.iso_code != 'en':
                translation_containers = (
                    self._build_translation_containers(translation)
                )

                self._process_translation_containers(translation_containers)

            output = "# -*- coding: UTF-8 -*-\n"
            output += self.assemble_file_data(translation)

            with codecs.open(description_path, "w", "utf_8") as f:
                f.write(output)

        path = os.path.join(path, self.iso_code + '.lang')
        if os.path.exists(path):
            namespace = {}
            eg.ExecFile(path, {}, namespace)
            translation = types.ClassType(plugin_name, (), namespace)
            self.load_plugin_description(plugin)
            return translation

        eg.PrintDebugNotice(
            'Plugin language file not found, creating new translation file: ' +
            plugin_name +
            '\\' +
            self.iso_code + '.lang'
        )

        translation = plugin.englishText

        output = "# -*- coding: UTF-8 -*-\n"

        if self.iso_code != 'en':
            output += self._build_plugin_language_file(translation)
        else:
            output += self.assemble_file_data(translation)

        with codecs.open(path, "w", "utf_8") as f:
            f.write(output)

        self.load_plugin_description(plugin)
        return translation

    def load_plugin_description(self, plugin):
        plugin_name = self._get_plugin_name(plugin)
        eg.PrintDebugNotice('Loading plugin description: ' + plugin_name)

        path = os.path.join(
            eg.folderPath.ProgramData,
            'EventGhost',
            'languages',
            plugin_name,
            self.iso_code + '_description.lang'
        )

        namespace = {}
        eg.ExecFile(path, {}, namespace)
        translation = types.ClassType(plugin_name, (), namespace)

        plugin.description = getattr(translation, 'description')
        plugin.name = getattr(translation, 'name')
        return plugin.description

    def build_plugin_descriptions(self):
        namespace = {}
        for info in eg.pluginManager.GetPluginInfoList():

            plugin_name = self._get_plugin_name(info)
            path = os.path.join(
                eg.folderPath.ProgramData,
                'EventGhost',
                'languages',
                plugin_name
            )

            if not os.path.exists(path):
                os.makedirs(path)

            path = os.path.join(path, self.iso_code + '_description.lang')

            if not os.path.exists(path):
                if isinstance(info.description, (str, unicode)):
                    description = info.description
                else:
                    description = str(info.description)

                if isinstance(info.name, (str, unicode)):
                    name = info.name
                else:
                    name = str(info.name)

                plugin_namespace = dict(
                    name=name,
                    description=description
                )

                namespace[plugin_name] = (
                    types.ClassType(plugin_name, (), plugin_namespace)
                )

        if namespace:
            with self._translation_lock:
                translation = types.ClassType('Descriptions', (), namespace)

                translation_containers = (
                    self._build_translation_containers(translation)
                )
                self._process_translation_containers(translation_containers)

            for plugin_name, value in translation.__dict__.items():
                if plugin_name.startswith('_'):
                    continue

                output = "# -*- coding: UTF-8 -*-\n"
                output += self.assemble_file_data(value)

                path = os.path.join(
                    eg.folderPath.ProgramData,
                    'EventGhost',
                    'languages',
                    plugin_name,
                    self.iso_code + '_description.lang'
                )

                with codecs.open(path, "w", "utf_8") as f:
                    f.write(output)

            TextToTranslate.count = 0
            TextToTranslate.in_processing = 0
            TextToTranslate.processed = 0

    def load_language_file(self):
        eg.PrintDebugNotice(
            'Loading language file: ' + self.iso_code + '.lang'
        )
        path = os.path.join(eg.languagesDir, self.iso_code + '.lang')
        if not os.path.exists(path):
            path = os.path.join(
                eg.folderPath.ProgramData,
                'EventGhost',
                'languages',
                self.iso_code + '.lang'
            )

        if os.path.exists(path):
            namespace = {}
            eg.ExecFile(path, {}, namespace)
            translation = types.ClassType('Text', (), namespace)
        else:
            translation, output = self._build_language_file()
            output = "# -*- coding: UTF-8 -*-\n" + output
            with codecs.open(path, "w", "utf_8") as f:
                f.write(output)

        setattr(translation, 'Plugin', types.ClassType('Plugin', (), {}))

        TextToTranslate.count = 0
        TextToTranslate.in_processing = 0
        TextToTranslate.processed = 0

        return translation

    def language_file(self, data):
        path, data = data

        if path is None:
            path = os.path.join(eg.languagesDir, self.iso_code + '.lang')
            if not os.path.exists(path):
                path = os.path.join(
                    eg.folderPath.ProgramData,
                    'EventGhost',
                    'languages',
                    self.iso_code + '.lang'
                )

        with codecs.open(path, "w", "utf_8") as f:
            f.write(data)

    language_file = property(fset=language_file)


countries = []


class CountryMeta(type):

    def __new__(mcs, name, bases, dct):
        country = type.__new__(mcs, name, bases, dct)
        instance = country()

        for i, item in enumerate(countries):
            if item.english_name > instance.english_name:
                countries.insert(i, instance)
                break
        else:
            countries.append(instance)

        return country


class WXLanguage(object):

    def __init__(self, country, language):
        self._country = country
        self._language = language
        self._language_file = None
        self._temp_language_file = None

    @property
    def flag(self):
        if self._country.flag:
            return eg.Icons.GetBitmap(
                os.path.join(eg.mainDir, self._country.flag)
            )
        else:
            return wx.EmptyBitmapRGBA(24, 24, 0, 0, 0, 0)

    @property
    def label(self):
        if self._language.country_name == self._language.native_name:
            return self._language.country_name

        return (
            self._language.country_name +
            u'  -  ' +
            self._language.native_name
        )

    def set(self):
        if self._language.wx_code:
            eg.config.language = self

    @property
    def iso_code(self):
        return self._language.iso_code + '_' + self._country.code

    def load_plugin(self, plugin):
        translation = self._language.load_plugin(plugin)
        setattr(
            self._language_file.Plugin,
            plugin.pluginCls.__name__,
            translation
        )
        return translation

    @property
    def lang_iso_code(self):
        return self._language.iso_code

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self._language.__dict__:
            return self.__language.__dict__[item]

        if (
            item in WXLanguage.__dict__ and
            'fget' in WXLanguage.__dict__[item].__dict__
        ):
            return WXLanguage.__dict__[item].fget(self)

        # if (
        #     item in Language.__dict__ and
        #     'fget' in Language.__dict__[item].__dict__
        # ):
        #     return Language.__dict__[item].fget(self._language)

        if hasattr(self._language, item):
            return getattr(self._language, item)

        if self._language_file is None:
            self.load()

        if item in self._language_file.__dict__:
            return self._language_file.__dict__[item]

        raise AttributeError(item)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        elif (
            key in WXLanguage.__dict__ and
            'fset' in WXLanguage.__dict__[key].__dict__
        ):
            WXLanguage.__dict__[key].fset(self, value)
        else:
            if self._language_file is None:
                if self._temp_language_file is None:
                    self._temp_language_file = eg.Bunch()

                import sys
                sys.stderr.write(key + ': ' + repr(value) + '\n')

                setattr(self._temp_language_file, key, value)
            else:
                setattr(self._language_file, key, value)

    @property
    def total_translation_count(self):
        return TextToTranslate.count

    @property
    def translations_processed(self):
        return TextToTranslate.processed

    @property
    def translations_in_processing(self):
        return TextToTranslate.in_processing

    def load(self):
        self._language_file = self._language.load_language_file()
        return self

    def save(self, data=None):

        if data is None:
            data = self._language_file

        plugins = data.__dict__.pop('Plugins')

        output = "# -*- coding: UTF-8 -*-\n"
        output += self._language.assemble_file_data(data)

        self._language.language_file = (None, output)
        data.__dict__['Plugins'] = plugins

        for plugin_name, plugin in plugins.__dict__.items():
            if plugin_name.startswith('_'):
                continue

            path = os.path.join(
                eg.folderPath.ProgramData,
                'EventGhost',
                'languages',
                plugin_name
            )

            if not os.path.exists(path):
                os.makedirs(path)

            path = os.path.join(path, self._language.iso_code + '.lang')

            output = "# -*- coding: UTF-8 -*-\n"
            output += self._language.assemble_file_data(plugin)

            with codecs.open(path, "w", "utf_8") as f:
                f.write(output)


class Country(object):
    __metaclass__ = CountryMeta

    code = ''
    english_name = ''
    flag = ''
    languages = []

    def __init__(self):
        for language in self.languages:
            language_codes = []
            if language.ISO639_1 is not None:
                language.locale_names.append(
                    language.ISO639_1 + '-' + self.code
                )
                language_codes += [language.ISO639_1]
            if language.ISO639_2 is not None:
                language.locale_names.append(
                    language.ISO639_2 + '-' + self.code
                )
                language_codes += [language.ISO639_1]
            if language.ISO639_3 is not None:
                language.locale_names.append(
                    language.ISO639_3 + '-' + self.code
                )
                language_codes += [language.ISO639_1]

            language.locale_names.extend(language_codes)


    @property
    def wx_languages(self):
        res = []

        for language in self.languages:
            code = language.wx_code
            if code is not None:
                res += [WXLanguage(self, language)]
        return res


class Afar(Language):
    ISO639_1 = 'aa'
    ISO639_2 = 'aar'
    english_name = 'Afar'
    native_name = u'Qafár af'


class Afrikaans(Language):
    ISO639_1 = 'af'
    ISO639_2 = 'afr'
    english_name = 'Afrikaans'
    native_name = u'Afrikaans'


class Amharic(Language):
    ISO639_1 = 'am'
    ISO639_2 = 'amh'
    english_name = 'Amharic'
    native_name = u'አማርኛ'


class Arabic(Language):
    ISO639_1 = 'ar'
    ISO639_2 = 'ara'
    english_name = 'Arabic'
    native_name = u'العربية'


class Asturian(Language):
    ISO639_2 = 'ast'
    english_name = 'Asturian'
    native_name = u'æˈstjʊəriən'


class Aymara(Language):
    ISO639_1 = 'ay'
    ISO639_2 = 'aym'
    english_name = 'Aymara'
    native_name = u'aymar aru'


class Azerbaijani(Language):
    ISO639_1 = 'az'
    ISO639_2 = 'aze'
    english_name = 'Azerbaijani'
    native_name = u'Azərbaycan'


class Belarusian(Language):
    ISO639_1 = 'be'
    ISO639_2 = 'bel'
    english_name = 'Belarusian'
    native_name = u'беларуская мова'


class Bulgarian(Language):
    ISO639_1 = 'bg'
    ISO639_2 = 'bul'
    english_name = 'Bulgarian'
    native_name = u'Български'


class Bislama(Language):
    ISO639_1 = 'bi'
    ISO639_2 = 'bis'
    english_name = 'Bislama'
    native_name = u'Bislama'


class Bengali(Language):
    ISO639_1 = 'bn'
    ISO639_2 = 'ben'
    english_name = 'Bengali'
    native_name = u'বাংলা'


class BosnianCyrillic(Language):
    ISO639_1 = 'bs'
    ISO639_2 = 'bos'
    english_name = 'Bosnian (Cyrillic)'
    native_name = u'беларуская мова'


class BosnianLatin(Language):
    ISO639_1 = 'bs'
    ISO639_2 = 'bos'
    english_name = 'Bosnian (Latin)'
    native_name = u'bosanski'


class Catalan(Language):
    ISO639_1 = 'ca'
    ISO639_2 = 'cat'
    english_name = 'Catalan'
    native_name = u'català'


class Chamorro(Language):
    ISO639_1 = 'ch'
    ISO639_2 = 'cha'
    english_name = 'Chamorro'
    native_language = u'Chamoru'


class SeychelloisCreole(Language):
    ISO639_2 = 'crs'
    english_name = 'Seychellois Creole'
    native_name = u'créole seychellois'


class Czech(Language):
    ISO639_1 = 'cs'
    ISO639_2 = 'cze'
    english_name = 'Czech'
    native_name = u'čeština'


class Welsh(Language):
    ISO639_1 = 'cy'
    ISO639_2 = 'wel'
    english_name = 'Welsh'
    native_name = u'Cymraeg'


class Yoruba(Language):
    ISO639_1 = 'yo'
    ISO639_2 = 'yor'
    english_name = 'Yoruba'
    native_name = u'ede Yorùbá'


class Danish(Language):
    ISO639_1 = 'da'
    ISO639_2 = 'dan'
    english_name = 'Danish'
    native_name = u'dansk'


class Dari(Language):
    ISO639_1 = 'fa'
    ISO639_2 = 'per'
    english_name = 'Dari'
    native_name = u'درى'


class German(Language):
    ISO639_1 = 'de'
    ISO639_2 = 'ger'
    english_name = 'German'
    native_name = u'Deutsch'


class Dhivehi(Language):
    ISO639_1 = 'dv'
    ISO639_2 = 'div'
    english_name = 'Dhivehi'
    native_name = u'ދިވެހި'


class Dzongkha(Language):
    ISO639_1 = 'dz'
    ISO639_2 = 'dzo'
    english_name = 'Dzongkha'
    native_name = u'རྫོང་ཁ་'


class Greek(Language):
    ISO639_1 = 'el'
    ISO639_2 = 'gre'
    english_name = 'Greek'
    native_name = u'Ελληνικά'


class Hausa(Language):
    ISO639_1 = 'ha'
    ISO639_2 = 'hau'
    english_name = 'Hausa'
    native_name = u'Hausa'


class Gujarati(Language):
    ISO639_1 = 'gu'
    ISO639_2 = 'guj'
    english_name = 'Gujarati'
    native_name = u'ગુજરાતી'


class English(Language):
    ISO639_1 = 'en'
    ISO639_2 = 'eng'
    english_name = 'English'
    native_name = u'English'


class Spanish(Language):
    ISO639_1 = 'es'
    ISO639_2 = 'spa'
    english_name = 'Spanish'
    native_name = u'Español'


class Estonian(Language):
    ISO639_1 = 'et'
    ISO639_2 = 'est'
    english_name = 'Estonian'
    native_name = u'eesti'


class Filipino(Language):
    ISO639_2 = 'fil'
    english_name = 'Filipino'
    native_name = u'Filipino'


class Basque(Language):
    ISO639_1 = 'eu'
    ISO639_2 = 'baq'
    english_name = 'Basque'
    native_name = u'euskara'


class Persian(Language):
    ISO639_1 = 'fa'
    ISO639_2 = 'fas'
    english_name = 'Persian'
    native_name = u'فارسی'


class Finnish(Language):
    ISO639_1 = 'fi'
    ISO639_2 = 'fin'
    english_name = 'Finnish'
    native_name = u'suomi'


class Faroese(Language):
    ISO639_1 = 'fo'
    ISO639_2 = 'fao'
    english_name = 'Faroese'


class French(Language):
    ISO639_1 = 'fr'
    ISO639_2 = 'fre'
    english_name = 'French'
    native_name = u'français'


class Irish(Language):
    ISO639_1 = 'ga'
    ISO639_2 = 'gle'
    english_name = 'Irish'
    native_name = u'Gaeilge'


class ScottishGaelic(Language):
    ISO639_1 = 'gd'
    ISO639_2 = 'gla'
    english_name = 'Scottish Gaelic'
    native_name = u'Gàidhlig'


class Galician(Language):
    ISO639_1 = 'gl'
    ISO639_2 = 'glg'
    english_name = 'Galician'
    native_name = u'galego'


class Guarani(Language):
    ISO639_1 = 'gn'
    ISO639_2 = 'grn'
    english_name = 'Guarani'
    native_name = u'avañeʼẽ'


class Hebrew(Language):
    ISO639_1 = 'he'
    ISO639_2 = 'heb'
    english_name = 'Hebrew'
    native_name = u'עברית'


class Hindi(Language):
    ISO639_1 = 'hi'
    ISO639_2 = 'hin'
    english_name = 'Hindi'
    native_name = u'हिंदी'


class HiriMotu(Language):
    ISO639_1 = 'ho'
    ISO639_2 = 'hmo'
    english_name = 'Hiri Motu'
    native_name = u'Hiri Motu'


class Croatian(Language):
    ISO639_1 = 'hr'
    ISO639_2 = 'hrv'
    english_name = 'Croatian'
    native_name = u'hrvatski'


class HaitianCreole(Language):
    ISO639_1 = 'ht'
    ISO639_2 = 'hat'
    english_name = 'Haitian Creole'
    native_name = u'Kreyòl Ayisyen'


class Hungarian(Language):
    ISO639_1 = 'hu'
    ISO639_2 = 'hun'
    english_name = 'Hungarian'
    native_name = u'magyar'


class Assamese(Language):
    ISO639_1 = 'as'
    ISO639_2 = 'asm'
    english_name = 'Assamese'
    native_name = u'অসমীয়া'


class Armenian(Language):
    ISO639_1 = 'hy'
    ISO639_2 = 'arm'
    english_name = 'Armenian'
    native_name = u'Հայերեն'


class Wolof(Language):
    ISO639_1 = 'wo'
    ISO639_2 = 'wol'
    english_name = 'Wolof'
    native_name = u'Wolof'


class Valencian(Language):
    ISO639_1 = 'ca'
    ISO639_2 = 'cat'
    english_name = 'Valencian'
    native_name = u'valencià'


class Uyghur(Language):
    ISO639_1 = 'ug'
    ISO639_2 = 'uig'
    english_name = 'Uyghur'
    native_name = u'ئۇيغۇرچە'


class Indonesian(Language):
    ISO639_1 = 'id'
    ISO639_2 = 'ind'
    english_name = 'Indonesian'
    natiive_name = u'Bahasa Indonesia'


class Icelandic(Language):
    ISO639_1 = 'is'
    ISO639_2 = 'ice'
    english_name = 'Icelandic'
    native_name = u'íslenska'


class Igbo(Language):
    ISO639_1 = 'ig'
    ISO639_2 = 'ibo'
    english_name = 'Igbo'
    native_name = u'Ndi Igbo'


class Italian(Language):
    ISO639_1 = 'it'
    ISO639_2 = 'ita'
    english_name = 'Italian'
    native_name = u'italiano'


class Japanese(Language):
    ISO639_1 = 'ja'
    ISO639_2 = 'jpn'
    english_name = 'Japanese'
    native_name = u'日本語‫'


class Kannada(Language):
    ISO639_1 = 'kn'
    ISO639_2 = 'kan'
    english_name = 'Kannada'
    native_name = u'ಕನ್ನಡ'


class Georgian(Language):
    ISO639_1 = 'ka'
    ISO639_2 = 'geo'
    english_name = 'Georgian'
    native_name = u'ქართული'


class KaraKalpak(Language):
    ISO639_2 = 'kaa'
    english_name = 'Karakalpak'
    native_name = u'قاراقالپاق تىلى'


class Kazakh(Language):
    ISO639_1 = 'kk'
    ISO639_2 = 'kaz'
    english_name = 'Kazakh'
    native_name = u'Қазақ'


class Cherokee(Language):
    ISO639_2 = 'chr'
    english_name = 'Cherokee'
    native_name = u'ᏣᎳᎩ ᎦᏬᏂᎯᏍᏗ'


class Kalaallisut(Language):
    ISO639_1 = 'kl'
    ISO639_2 = 'kal'
    english_name = 'Kalaallisut'
    native_name = u'Kalaallisut'


class Khmer(Language):
    ISO639_1 = 'km'
    ISO639_2 = 'khm'
    english_name = 'Khmer'
    native_name = u'ខ្មែរ'


class Korean(Language):
    ISO639_1 = 'ko'
    ISO639_2 = 'kor'
    english_name = 'Korean'
    native_name = u'한국어‫'


class Kurdish(Language):
    ISO639_1 = 'ku'
    ISO639_2 = 'kur'
    english_name = 'Kurdish'
    native_name = u'سۆرانی'


class Cornish(Language):
    ISO639_1 = 'kw'
    ISO639_2 = 'cor'
    english_name = 'Cornish'
    native_name = u'Kernewek'


class Kyrgyz(Language):
    ISO639_1 = 'ky'
    ISO639_2 = 'kir'
    english_name = 'Kyrgyz'
    native_name = u'Кыргыз'


class Luxembourgish(Language):
    ISO639_1 = 'lb'
    ISO639_2 = 'ltz'
    english_name = 'Luxembourgish'
    native_name = u'Lëtzebuergesch'


class Lao(Language):
    ISO639_1 = 'lo'
    ISO639_2 = 'lao'
    english_name = 'Lao'
    native_name = u'ພາສາລາວ'


class Lithuanian(Language):
    ISO639_1 = 'lt'
    ISO639_2 = 'lit'
    english_name = 'Lithuanian'
    native_name = u'lietuvių'


class Latvian(Language):
    ISO639_1 = 'lv'
    ISO639_2 = 'lav'
    english_name = 'Latvian'
    native_name = u'latviešu'


class Morisyen(Language):
    ISO639_2 = 'mfe'
    english_name = 'Morisyen'
    native_name = u'Kreol morisien'


class Malagasy(Language):
    ISO639_1 = 'mg'
    ISO639_2 = 'mlg'
    english_name = 'Malagasy'
    native_name = u'Malagasy'


class Marshallese(Language):
    ISO639_1 = 'mh'
    ISO639_2 = 'mah'
    english_name = 'Marshallese'
    native_name = u'kajin M̧ajeļ'


class Maori(Language):
    ISO639_1 = 'mi'
    ISO639_2 = 'mao'
    english_name = 'Maori'
    native_name = u'Te Reo Māori'


class Marathi(Language):
    ISO639_1 = 'mr'
    ISO639_2 = 'mar'
    english_name = 'Marathi'
    native_name = u'मराठी'


class Macedonian(Language):
    ISO639_1 = 'mk'
    ISO639_2 = 'mac'
    english_name = 'Macedonian'
    native_name = u'македонски јазик'


class Mongolian(Language):
    ISO639_1 = 'mn'
    ISO639_2 = 'mon'
    english_name = 'Mongolian'
    native_name = u'Монгол хэл'


class Malay(Language):
    ISO639_1 = 'ms'
    ISO639_2 = 'may'
    english_name = 'Malay'
    native_name = u'Bahasa Melayu'


class Malayalam(Language):
    ISO639_1 = 'ml'
    ISO639_2 = 'mal'
    english_name = 'Malayalam'
    native_name = u'മലയാളം'


class Maltese(Language):
    ISO639_1 = 'mt'
    ISO639_2 = 'mlt'
    english_name = 'Maltese'
    native_name = u'Malti'


class Burmese(Language):
    ISO639_1 = 'my'
    ISO639_2 = 'bur'
    english_name = 'Burmese'
    native_name = u'ဗမာစာ'


class Nauru(Language):
    ISO639_1 = 'na'
    ISO639_2 = 'nau'
    english_name = 'Nauru'
    native_name = u'ekakairũ naoero'


class NorwegianBokmal(Language):
    ISO639_1 = 'nb'
    ISO639_2 = 'nob'
    english_name = 'Norwegian (Bokmal)'
    native_name = u'norsk (bokmål)'


class NorthNdebele(Language):
    ISO639_1 = 'nd'
    ISO639_2 = 'nde'
    english_name = 'North Ndebele'
    native_name = u'saseNyakatho'


class Nepali(Language):
    ISO639_1 = 'ne'
    ISO639_2 = 'nep'
    english_name = 'Nepali'
    native_name = u'नेपाली'


class Niuean(Language):
    ISO639_2 = 'niu'
    english_name = 'Niuean'
    native_name = u'ko e vagahau Niuē'


class Dutch(Language):
    ISO639_1 = 'nl'
    ISO639_2 = 'dut'
    english_name = 'Dutch'
    native_name = u'Nederlands'


class NorwegianNynorsk(Language):
    ISO639_1 = 'nn'
    ISO639_2 = 'nno'
    english_name = 'Norwegian (Nynorsk)'
    native_name = u'norsk (nynorsk)'


class Norwegian(Language):
    ISO639_1 = 'no'
    ISO639_2 = 'nor'
    english_name = 'Norwegian'
    native_name = u'norsk'


class Nyanja(Language):
    ISO639_1 = 'ny'
    ISO639_2 = 'nya'
    english_name = 'Nyanja'
    native_name = u'chiCheŵa'


class Oriya(Language):
    ISO639_1 = 'or'
    ISO639_2 = 'ori'
    english_name = 'Oriya'
    native_name = u'ଓଡିଆ'


class Oromo(Language):
    ISO639_1 = 'om'
    ISO639_2 = 'orm'
    english_name = 'Oromo'
    native_name = u'Afaan Oromoo'


class Papiamento(Language):
    ISO639_2 = 'pap'
    english_name = 'Papiamento'
    native_name = u'papiamentu'


class Palauan(Language):
    ISO639_2 = 'pau'
    english_name = 'Palauan'
    native_name = u'tekoi ra Belau'


class PitcairnNorfolk(Language):
    ISO639_2 = 'pih'
    english_name = 'Pitcairn-Norfolk'
    native_name = u'Norfuk'


class Polish(Language):
    ISO639_1 = 'pl'
    ISO639_2 = 'pol'
    english_name = 'Polish'
    native_name = u'Polski'


class Pashto(Language):
    ISO639_1 = 'ps'
    ISO639_2 = 'pus'
    english_name = 'Pashto'
    native_name = u'پښتو'


class Portuguese(Language):
    ISO639_1 = 'pt'
    ISO639_2 = 'por'
    english_name = 'Portuguese'
    native_name = u'português'


class Punjabi(Language):
    ISO639_1 = 'pa'
    ISO639_2 = 'pan'
    english_name = 'Punjabi'
    native_name = u'ਪੰਜਾਬੀ'


class PunjabiArabic(Language):
    ISO639_1 = 'pa'
    ISO639_2 = 'pan'
    english_name = 'Punjabi (Arabic)'
    native_name = u'پنجابی'


class Quechua(Language):
    ISO639_1 = 'qu'
    ISO639_2 = 'que'
    english_name = 'Quechua'
    native_name = u'runasimi'


class Rarotongan(Language):
    ISO639_2 = 'rar'
    english_name = 'Rarotongan'
    native_name = u'Māori Kūki ’Āirani'


class Romansh(Language):
    ISO639_1 = 'rm'
    ISO639_2 = 'roh'
    english_name = 'Romansh'
    native_name = u'Rumantsch'


class Romanian(Language):
    ISO639_1 = 'ro'
    ISO639_2 = 'rum'
    english_name = 'Romanian'
    native_name = u'română'


class Russian(Language):
    ISO639_1 = 'ru'
    ISO639_2 = 'rus'
    english_name = 'Russian'
    native_name = u'Русский'


class Kiche(Language):
    ISO639_2 = 'quc'
    english_name = 'Kiche'
    native_name = u'Qatzijob\'al'


class Kinyarwanda(Language):
    ISO639_1 = 'rw'
    ISO639_2 = 'kin'
    english_name = 'Kinyarwanda'
    native_name = u'Kinyarwanda'


class NorthernSami(Language):
    ISO639_1 = 'se'
    ISO639_2 = 'sme'
    english_name = 'Northern Sami'
    native_name = u'davvisámegiella'


class Sango(Language):
    ISO639_1 = 'sg'
    ISO639_2 = 'sag'
    english_name = 'Sango'
    native_name = u'sängö'


class Sinhala(Language):
    ISO639_1 = 'si'
    ISO639_2 = 'sin'
    english_name = 'Sinhala'
    native_name = u'සිංහල'


class Slovak(Language):
    ISO639_1 = 'sk'
    ISO639_2 = 'slo'
    english_name = 'Slovak'
    native_name = u'slovenčina'


class Slovenian(Language):
    ISO639_1 = 'sl'
    ISO639_2 = 'slv'
    english_name = 'Slovenian'
    mative_name = u'slovenski'


class Samoan(Language):
    ISO639_1 = 'sm'
    ISO639_2 = 'smo'
    english_name = 'Samoan'
    native_name = u'gagana Sāmoa'


class Shona(Language):
    ISO639_1 = 'sn'
    ISO639_2 = 'sna'
    english_name = 'Shona'
    native_name = u'chiShona'


class Somali(Language):
    ISO639_1 = 'so'
    ISO639_2 = 'som'
    english_name = 'Somali'
    native_name = u'Soomaali'


class Albanian(Language):
    ISO639_1 = 'sq'
    ISO639_2 = 'alb'
    english_name = 'Albanian'
    native_name = u'shqip'


class SerbianCyrillic(Language):
    ISO639_1 = 'sr'
    ISO639_2 = 'srp'
    english_name = 'Serbian (Cyrillic)'
    native_name = u'српски'


class SerbianLatin(Language):
    ISO639_1 = 'sr'
    ISO639_2 = 'srp'
    english_name = 'Serbian (Latin)'
    native_name = u'srpski'


class SesothosaLeboa(Language):
    code = ''
    english_name = 'Sesotho sa Leboa'
    native_name = u'Sesotho sa Leboa'


class Swati(Language):
    ISO639_1 = 'ss'
    ISO639_2 = 'ssw'
    english_name = 'Swati'
    native_name = u'siSwati'


class SouthernSotho(Language):
    ISO639_1 = 'st'
    ISO639_2 = 'sot'
    english_name = 'Southern Sotho'
    native_name = u'Sesotho'


class Swedish(Language):
    ISO639_1 = 'sv'
    ISO639_2 = 'swe'
    english_name = 'Swedish'
    native_name = u'svenska'


class Konkani(Language):
    ISO639_2 = 'kok'
    english_name = 'Konkani'
    native_name = u'कोंकणी'


class Swahili(Language):
    ISO639_1 = 'sw'
    ISO639_2 = 'swa'
    english_name = 'Swahili'
    native_name = u'KiSwahili'


class Tamil(Language):
    ISO639_1 = 'ta'
    ISO639_2 = 'tam'
    english_name = 'Tamil'
    native_name = u'தமிழ்'


class Telugu(Language):
    ISO639_1 = 'te'
    ISO639_2 = 'tel'
    english_name = 'Telugu'
    native_name = u'తెలుగు'


class Tatar(Language):
    ISO639_1 = 'tt'
    ISO639_2 = 'tat'
    english_name = 'Tatar'
    native_name = u'Татар'


class Tetum(Language):
    ISO639_2 = 'tet'
    english_name = 'Tetum'
    native_name = u'Tetun'


class Tajik(Language):
    ISO639_1 = 'tg'
    ISO639_2 = 'tgk'
    english_name = 'Tajik'
    native_name = u'тоҷикӣ'


class Thai(Language):
    ISO639_1 = 'th'
    ISO639_2 = 'tha'
    english_name = 'Thai'
    native_name = u'ไทย'


class Tigrinya(Language):
    ISO639_1 = 'ti'
    ISO639_2 = 'tir'
    english_name = 'Tigrinya'
    native_name = u'ትግርኛ'


class Turkmen(Language):
    ISO639_1 = 'tk'
    ISO639_2 = 'tuk'
    english_name = 'Turkmen'
    native_name = u'Türkmençe'


class Tokelauan(Language):
    ISO639_2 = 'tkl'
    english_name = 'Tokelauan'
    native_name = u'Fakatokelau'


class Tagalog(Language):
    ISO639_1 = 'tl'
    ISO639_2 = 'tgl'
    english_name = 'Tagalog'
    native_name = u'ᜏᜒᜃᜅ᜔ ᜆᜄᜎᜓᜄ᜔'


class Setswana(Language):
    ISO639_1 = 'tn'
    ISO639_2 = 'tsn'
    english_name = 'Setswana'
    native_name = u'Setswana'


class Tobian(Language):
    ISO639_3 = 'tox'
    english_name = 'Tobian'
    native_name = u'ramarih Hatohobei'


class TokPisin(Language):
    ISO639_2 = 'tpi'
    english_name = 'Tok Pisin'
    native_name = u'Tok Pisin'


class Turkish(Language):
    ISO639_1 = 'tr'
    ISO639_2 = 'tur'
    english_name = 'Turkish'
    native_name = u'Türkçe'


class Ukrainian(Language):
    ISO639_1 = 'uk'
    ISO639_2 = 'ukr'
    english_name = 'Ukrainian'
    native_name = u'українська'


class Urdu(Language):
    ISO639_1 = 'ur'
    ISO639_2 = 'urd'
    english_name = 'Urdu'
    native_name = u'اردو'


class Uzbek(Language):
    ISO639_1 = 'uz'
    ISO639_2 = 'uzb'
    english_name = 'Uzbek'
    native_name = u'O\'zbekcha'


class Vietnamese(Language):
    ISO639_1 = 'vi'
    ISO639_2 = 'vie'
    english_name = 'Vietnamese'
    native_name = u'Tiếng Việt'


class Xhosa(Language):
    ISO639_1 = 'xh'
    ISO639_2 = 'xho'
    english_name = 'Xhosa'
    native_name = u'isiXhosa'


class StandardMoroccanTamazight(Language):
    ISO639_2 = 'zgh'
    english_name = 'Standard Moroccan Tamazight'
    native_name = u'Tamaziɣt'


class ChineseSimplified(Language):
    ISO639_1 = 'zh'
    ISO639_2 = 'chi'
    english_name = 'Chinese Simplified'
    native_name = u'中文(简体)'


class ChineseTraditional(Language):
    ISO639_1 = 'zh'
    ISO639_2 = 'zho'
    english_name = 'Chinese Traditional'
    native_name = u'中文(繁體)'


class Zulu(Language):
    ISO639_1 = 'zu'
    ISO639_2 = 'zul'
    english_name = 'Zulu'
    native_name = u'isiZulu'


class Alemannic(Language):
    ISO639_2 = 'gsw'
    english_name = 'Alemannic'
    native_name = u'Alemannisch'


class Bavarian(Language):
    ISO639_2 = 'bar'
    english_name = 'Bavarian'
    native_name = u'bairisch'


class UpperSorbian(Language):
    ISO639_2 = 'hsb'
    english_name = 'Upper Sorbian'
    native_name = u'hornjoserbšćina'


class LowerSorbian(Language):
    ISO639_2 = 'dsb'
    english_name = 'Lower Sorbian'
    native_name = u'dolnoserbšćina'


class NorthFrisian(Language):
    ISO639_2 = 'frr'
    english_name = 'North Frisian'
    native_name = u'Nuurdfresk'


class SaterlandFrisian(Language):
    ISO639_2 = 'stq'
    english_name = 'Saterland Frisian'
    native_name = u'Seeltersk'


class Romani(Language):
    ISO639_2 = 'rom'
    english_name = 'Romani'
    native_name = u'romani čhib'


class LowGerman(Language):
    ISO639_2 = 'nds'
    english_name = 'Low German'
    native_name = u'Nedderdüütsch'


class Andorra(Country):
    code = 'AD'
    english_name = 'Andorra'
    flag = 'images\\flags\\AD.png'
    languages = [
        Catalan(u'Andorra')
    ]


class UnitedArabEmirates(Country):
    code = 'AE'
    english_name = 'United Arab Emirates'
    flag = 'images\\flags\\AE.png'
    languages = [
        Arabic(u'الإمارات العربية المتحدة'),
        Azerbaijani(u'Birləşmiş Ərəb Əmirlikləri')
    ]


class Afghanistan(Country):
    code = 'AF'
    english_name = 'Afghanistan'
    flag = 'images\\flags\\AF.png'
    languages = [
        Persian(u'د افغانستان اسلامي دولتدولت اسلامی افغانستان'),
        Pashto(u'جمهوری اسلامی افغانستان')
    ]


class AntiguaandBarbuda(Country):
    code = 'AG'
    english_name = 'Antigua and Barbuda'
    flag = 'images\\flags\\AG.png'
    languages = [
        English(u'Antigua and Barbuda')
    ]


class Anguilla(Country):
    code = 'AI'
    english_name = 'Anguilla'
    flag = 'images\\flags\\AI.png'
    languages = [
        English(u'Anguilla')
    ]


class Albania(Country):
    code = 'AL'
    english_name = 'Albania'
    flag = 'images\\flags\\AL.png'
    languages = [
        Albanian(u'Shqipëria')
    ]


class Armenia(Country):
    code = 'AM'
    english_name = 'Armenia'
    flag = 'images\\flags\\AM.png'
    languages = [
        Armenian(u'Հայաստան')
    ]


class Angola(Country):
    code = 'AO'
    english_name = 'Angola'
    flag = 'images\\flags\\AO.png'
    languages = [
        Portuguese(u'Angola')
    ]


class Antarctica(Country):
    code = 'AQ'
    english_name = 'Antarctica'
    flag = 'images\\flags\\AQ.png'
    languages = [
        English(u'Antarctica'),
        Spanish(u'Antártico'),
        French(u'Antarctique'),
        Russian(u'Антарктике')
    ]


class Argentina(Country):
    code = 'AR'
    english_name = 'Argentina'
    flag = 'images\\flags\\AR.png'
    languages = [
        Spanish(u'Argentina')
    ]


class AmericanSamoa(Country):
    code = 'AS'
    english_name = 'American Samoa'
    flag = 'images\\flags\\AS.png'
    languages = [
        English(u'American Samoa'),
        Samoan(u'Amerika Samoa')
    ]


class Austria(Country):
    code = 'AT'
    english_name = 'Austria'
    flag = 'images\\flags\\AT.png'
    languages = [
        German(u'Österreich')
    ]


class Australia(Country):
    code = 'AU'
    english_name = 'Australia'
    flag = 'images\\flags\\AU.png'
    languages = [
        English(u'Australia')
    ]


class Aruba(Country):
    code = 'AW'
    english_name = 'Aruba'
    flag = 'images\\flags\\AW.png'
    languages = [
        Dutch(u'Aruba'),
        Papiamento(u'Aruba')
    ]


class AlandIslands(Country):
    code = 'AX'
    english_name = 'Aland Islands'
    flag = 'images\\flags\\AX.png'
    languages = [
        Swedish(u'Åland')
    ]


class Azerbaijan(Country):
    code = 'AZ'
    english_name = 'Azerbaijan'
    flag = 'images\\flags\\AZ.png'
    languages = [
        Azerbaijani(u'Azərbaycan')
    ]


class BosniaandHerzegovina(Country):
    code = 'BA'
    english_name = 'Bosnia and Herzegovina'
    flag = 'images\\flags\\BA.png'
    languages = [
        BosnianCyrillic(u'Bosna i Hercegovina'),
        Croatian(u'Bosna i Hercegovina'),
        SerbianCyrillic(u'Босна и Херцеговина')
    ]


class Barbados(Country):
    code = 'BB'
    english_name = 'Barbados'
    flag = 'images\\flags\\BB.png'
    languages = [
        English(u'Barbados')
    ]


class Bangladesh(Country):
    code = 'BD'
    english_name = 'Bangladesh'
    flag = 'images\\flags\\BD.png'
    languages = [
        Bengali(u'গণপ্রজাতন্ত্রী বাংলাদেশ')
    ]


class Belgium(Country):
    code = 'BE'
    english_name = 'Belgium'
    flag = 'images\\flags\\BE.png'
    languages = [
        German(u'Belgien'),
        French(u'Belgique'),
        Dutch(u'België')
    ]


class BurkinaFaso(Country):
    code = 'BF'
    english_name = 'Burkina Faso'
    flag = 'images\\flags\\BF.png'
    languages = [
        French(u'Burkina Faso')
    ]


class Bulgaria(Country):
    code = 'BG'
    english_name = 'Bulgaria'
    flag = 'images\\flags\\BG.png'
    languages = [
        Bulgarian(u'България')
    ]


class Bahrein(Country):
    code = 'BH'
    english_name = 'Bahrein'
    flag = 'images\\flags\\BH.png'
    languages = [
        Arabic(u'البحرين')
    ]


class Burundi(Country):
    code = 'BI'
    english_name = 'Burundi'
    flag = 'images\\flags\\BI.png'
    languages = [
        French(u'Burundi')
    ]


class Benin(Country):
    code = 'BJ'
    english_name = 'Benin'
    flag = 'images\\flags\\BJ.png'
    languages = [
        French(u'Bénin')
    ]


class SaintBarts(Country):
    code = 'BL'
    english_name = 'Saint-Barts'
    flag = 'images\\flags\\BL.png'
    languages = [
        French(u'Saint-Barthélemy')
    ]


class Bermuda(Country):
    code = 'BM'
    english_name = 'Bermuda'
    flag = 'images\\flags\\BM.png'
    languages = [
        English(u'Bermuda')
    ]


class BruneiDarussalam(Country):
    code = 'BN'
    english_name = 'Brunei Darussalam'
    flag = 'images\\flags\\BN.png'
    languages = [
        Malay(u'Brunei Darussalam')
    ]


class Bolivia(Country):
    code = 'BO'
    english_name = 'Bolivia'
    flag = 'images\\flags\\BO.png'
    languages = [
        Aymara(u'Wuliwya'),
        Spanish(u'Bolivia'),
        Guarani(u'Volívia'),
        Quechua(u'Bulibiya')
    ]


class CaribbeanNetherlands(Country):
    code = 'BQ'
    english_name = 'Caribbean Netherlands'
    flag = 'images\\flags\\BQ.png'
    languages = [
        Dutch(u'Caribisch Nederland')
    ]


class Brazil(Country):
    code = 'BR'
    english_name = 'Brazil'
    flag = 'images\\flags\\BR.png'
    languages = [
        Portuguese(u'Brasil')
    ]


class Bahamas(Country):
    code = 'BS'
    english_name = 'Bahamas'
    flag = 'images\\flags\\BS.png'
    languages = [
        English(u'Bahamas')
    ]


class Bhutan(Country):
    code = 'BT'
    english_name = 'Bhutan'
    flag = 'images\\flags\\BT.png'
    languages = [
        Dzongkha(u'འབྲུག་ཡུལ')
    ]


class BouvetIsland(Country):
    code = 'BV'
    english_name = 'Bouvet Island'
    flag = 'images\\flags\\BV.png'
    languages = [
        Norwegian(u'Bouvetøya')
    ]


class Botswana(Country):
    code = 'BW'
    english_name = 'Botswana'
    flag = 'images\\flags\\BW.png'
    languages = [
        English(u'Botswana'),
        Setswana(u'Botswana')
    ]


class Belarus(Country):
    code = 'BY'
    english_name = 'Belarus'
    flag = 'images\\flags\\BY.png'
    languages = [
        Belarusian(u'Беларусь'),
        Russian(u'Беларусь')
    ]


class Belize(Country):
    code = 'BZ'
    english_name = 'Belize'
    flag = 'images\\flags\\BZ.png'
    languages = [
        English(u'Belize')
    ]


class Canada(Country):
    code = 'CA'
    english_name = 'Canada'
    flag = 'images\\flags\\CA.png'
    languages = [
        English(u'Canada'),
        French(u'Canada')
    ]


class CocosIslands(Country):
    code = 'CC'
    english_name = 'Cocos (Keeling) Islands'
    flag = 'images\\flags\\CC.png'
    languages = [
        English(u'Cocos (Keeling) Islands')
    ]


class DemocraticRepublicoftheCongo(Country):
    code = 'CD'
    english_name = 'Democratic Republic of the Congo'
    flag = 'images\\flags\\CD.png'
    languages = [
        French(u'République Démocratique du Congo')
    ]


class CentralAfricanRepublic(Country):
    code = 'CF'
    english_name = 'Central African Republic'
    flag = 'images\\flags\\CF.png'
    languages = [
        French(u'République centrafricaine'),
        Sango(u'Ködörösêse tî Bêafrîka')
    ]


class RepublicoftheCongo(Country):
    code = 'CG'
    english_name = 'Republic of the Congo (Congo-Brazzaville)'
    flag = 'images\\flags\\CG.png'
    languages = [
        French(u'République du Congo')
    ]


class Switzerland(Country):
    code = 'CH'
    english_name = 'Switzerland'
    flag = 'images\\flags\\CH.png'
    languages = [
        German(u'Schweiz'),
        French(u'Suisse'),
        Italian(u'Svizzera'),
        Romansh(u'Svizra')
    ]


class IvoryCoast(Country):
    code = 'CI'
    english_name = 'Ivory Coast'
    flag = 'images\\flags\\CI.png'
    languages = [
        French(u'Côte d\'Ivoire')
    ]


class CookIslands(Country):
    code = 'CK'
    english_name = 'Cook Islands'
    flag = 'images\\flags\\CK.png'
    languages = [
        English(u'Cook Islands'),
        Rarotongan(u'Kūki ʻĀirani')
    ]


class Chile(Country):
    code = 'CL'
    english_name = 'Chile'
    flag = 'images\\flags\\CL.png'
    languages = [
        Spanish(u'Chile')
    ]


class Cameroon(Country):
    code = 'CM'
    english_name = 'Cameroon'
    flag = 'images\\flags\\CM.png'
    languages = [
        English(u'Cameroon'),
        French(u'Cameroun')
    ]


class China(Country):
    code = 'CN'
    english_name = 'China'
    flag = 'images\\flags\\CN.png'
    languages = [
        ChineseSimplified(u'中国')
    ]


class Colombia(Country):
    code = 'CO'
    english_name = 'Colombia'
    flag = 'images\\flags\\CO.png'
    languages = [
        Spanish(u'Colombia')
    ]


class CostaRica(Country):
    code = 'CR'
    english_name = 'Costa Rica'
    flag = 'images\\flags\\CR.png'
    languages = [
        Spanish(u'Costa Rica')
    ]


class Cuba(Country):
    code = 'CU'
    english_name = 'Cuba'
    flag = 'images\\flags\\CU.png'
    languages = [
        Spanish(u'Cuba')
    ]


class CaboVerde(Country):
    code = 'CV'
    english_name = 'Cabo Verde'
    flag = 'images\\flags\\CV.png'
    languages = [
        Portuguese(u'Cabo Verde')
    ]


class Curacao(Country):
    code = 'CW'
    english_name = 'Curacao'
    flag = 'images\\flags\\CW.png'
    languages = [
        English(u'Curacao'),
        Dutch(u'Curaçao')
    ]


class ChristmasIsland(Country):
    code = 'CX'
    english_name = 'Christmas Island'
    flag = 'images\\flags\\CX.png'
    languages = [
        English(u'Christmas Island')
    ]


class Cyprus(Country):
    code = 'CY'
    english_name = 'Cyprus'
    flag = 'images\\flags\\CY.png'
    languages = [
        Greek(u'Κύπρος'),
        Turkish(u'Kibris')
    ]


class CzechRepublic(Country):
    code = 'CZ'
    english_name = 'Czech Republic'
    flag = 'images\\flags\\CZ.png'
    languages = [
        Czech(u'Česká republika')
    ]


class Germany(Country):
    code = 'DE'
    english_name = 'Germany'
    flag = 'images\\flags\\DE.png'
    languages = [
        German(u'Deutschland'),
        Luxembourgish(u'Däitschland'),
        Alemannic(u'Deutschland'),
        Bavarian(u'Deitschland'),
        Danish(u'Tyskland'),
        UpperSorbian(u'Nىmska'),
        LowerSorbian(u'Nimce'),
        NorthFrisian(u'Tjüschlönj'),
        SaterlandFrisian(u'Dútslân'),
        Romani(u'Jermaniya'),
        LowGerman(u'Düütschland')
    ]


class Djibouti(Country):
    code = 'DJ'
    english_name = 'Djibouti'
    flag = 'images\\flags\\DJ.png'
    languages = [
        Afar(u'Gabuutih'),
        Arabic(u'جيبوتي'),
        French(u'Djibouti'),
        Somali(u'Jabuuti')
    ]


class Denmark(Country):
    code = 'DK'
    english_name = 'Denmark'
    flag = 'images\\flags\\DK.png'
    languages = [
        Danish(u'Danmark')
    ]


class Dominica(Country):
    code = 'DM'
    english_name = 'Dominica'
    flag = 'images\\flags\\DM.png'
    languages = [
        English(u'Dominica')
    ]


class DominicanRepublic(Country):
    code = 'DO'
    english_name = 'Dominican Republic'
    flag = 'images\\flags\\DO.png'
    languages = [
        Spanish(u'República Dominicana')
    ]


class Algeria(Country):
    code = 'DZ'
    english_name = 'Algeria'
    flag = 'images\\flags\\DZ.png'
    languages = [
        Arabic(u'الجزائر')
    ]


class Ecuador(Country):
    code = 'EC'
    english_name = 'Ecuador'
    flag = 'images\\flags\\EC.png'
    languages = [
        Spanish(u'Ecuador')
    ]


class Estonia(Country):
    code = 'EE'
    english_name = 'Estonia'
    flag = 'images\\flags\\EE.png'
    languages = [
        Estonian(u'Eesti')
    ]


class Egypt(Country):
    code = 'EG'
    english_name = 'Egypt'
    flag = 'images\\flags\\EG.png'
    languages = [
        Arabic(u'مصر')
    ]


class WesternSahara(Country):
    code = 'EH'
    english_name = 'Western Sahara'
    flag = 'images\\flags\\EH.png'
    languages = [
        Arabic(u'الصحراء الغربية'),
        Spanish(u'Sahara Occidental'),
        French(u'Sahara occidental')
    ]


class Eritrea(Country):
    code = 'ER'
    english_name = 'Eritrea'
    flag = 'images\\flags\\ER.png'
    languages = [
        Arabic(u'إرتريا'),
        English(u'Eritrea'),
        Tigrinya(u'ኤርትራ')
    ]


class Spain(Country):
    code = 'ES'
    english_name = 'Spain'
    flag = 'images\\flags\\ES.png'
    languages = [
        Asturian(u'España'),
        Catalan(u'Espanya'),
        Spanish(u'España'),
        Basque(u'Espainia'),
        Galician(u'España')
    ]


class Ethiopia(Country):
    code = 'ET'
    english_name = 'Ethiopia'
    flag = 'images\\flags\\ET.png'
    languages = [
        Amharic(u'ኢትዮጵያ'),
        Oromo(u'Itoophiyaa')
    ]


class Finland(Country):
    code = 'FI'
    english_name = 'Finland'
    flag = 'images\\flags\\FI.png'
    languages = [
        Finnish(u'Suomi'),
        NorthernSami(u'Suopma'),
        Swedish(u'Finland')
    ]


class Fiji(Country):
    code = 'FJ'
    english_name = 'Fiji'
    flag = 'images\\flags\\FJ.png'
    languages = [
        English(u'Fiji')
    ]


class FalklandIslands(Country):
    code = 'FK'
    english_name = 'Falkland Islands'
    flag = 'images\\flags\\FK.png'
    languages = [
        English(u'Falkland Islands')
    ]


class Micronesia(Country):
    code = 'FM'
    english_name = 'Micronesia (Federated States of)'
    flag = 'images\\flags\\FM.png'
    languages = [
        English(u'Micronesia')
    ]


class FaroeIslands(Country):
    code = 'FO'
    english_name = 'Faroe Islands'
    flag = 'images\\flags\\FO.png'
    languages = [
        Danish(u'Færøerne'),
        Faroese(u'Føroyar')
    ]


class France(Country):
    code = 'FR'
    english_name = 'France'
    flag = 'images\\flags\\FR.png'
    languages = [
        French(u'France')
    ]


class Gabon(Country):
    code = 'GA'
    english_name = 'Gabon'
    flag = 'images\\flags\\GA.png'
    languages = [
        French(u'Gabon')
    ]


class UnitedKingdom(Country):
    code = 'GB'
    english_name = 'United Kingdom'
    flag = 'images\\flags\\GB.png'
    languages = [
        Welsh(u'Y Deyrnas Unedig'),
        English(u'United Kingdom'),
        Irish(u'an Ríocht Aontaithe'),
        ScottishGaelic(u'An rioghachd aonaichte'),
        Cornish(u'Rywvaneth Unys')
    ]


class Grenada(Country):
    code = 'GD'
    english_name = 'Grenada'
    flag = 'images\\flags\\GD.png'
    languages = [
        English(u'Grenada')
    ]


class Georgia(Country):
    code = 'GE'
    english_name = 'Georgia'
    flag = 'images\\flags\\GE.png'
    languages = [
        Georgian(u'საქართველო')
    ]


class FrenchGuiana(Country):
    code = 'GF'
    english_name = 'French Guiana'
    flag = 'images\\flags\\GF.png'
    languages = [
        French(u'Guyane française')
    ]


class Guernsey(Country):
    code = 'GG'
    english_name = 'Guernsey'
    flag = 'images\\flags\\GG.png'
    languages = [
        English(u'Guernsey')
    ]


class Ghana(Country):
    code = 'GH'
    english_name = 'Ghana'
    flag = 'images\\flags\\GH.png'
    languages = [
        English(u'Ghana')
    ]


class Gibraltar(Country):
    code = 'GI'
    english_name = 'Gibraltar'
    flag = 'images\\flags\\GI.png'
    languages = [
        English(u'Gibraltar')
    ]


class Greenland(Country):
    code = 'GL'
    english_name = 'Greenland'
    flag = 'images\\flags\\GL.png'
    languages = [
        Danish(u'Grønland'),
        Kalaallisut(u'Kalaallit Nunaat')
    ]


class TheGambia(Country):
    code = 'GM'
    english_name = 'The Gambia'
    flag = 'images\\flags\\GM.png'
    languages = [
        English(u'The Gambia')
    ]


class Guinea(Country):
    code = 'GN'
    english_name = 'Guinea'
    flag = 'images\\flags\\GN.png'
    languages = [
        French(u'Guinée')
    ]


class Guadeloupe(Country):
    code = 'GP'
    english_name = 'Guadeloupe'
    flag = 'images\\flags\\GP.png'
    languages = [
        French(u'Guadeloupe')
    ]


class EquatorialGuinea(Country):
    code = 'GQ'
    english_name = 'Equatorial Guinea'
    flag = 'images\\flags\\GQ.png'
    languages = [
        Spanish(u'Guiena ecuatorial'),
        French(u'Guinée équatoriale'),
        Portuguese(u'Guiné Equatorial')
    ]


class Greece(Country):
    code = 'GR'
    english_name = 'Greece'
    flag = 'images\\flags\\GR.png'
    languages = [
        Greek(u'Ελλάδα')
    ]


class SouthGeorgiaandtheSouthSandwichIslands(Country):
    code = 'GS'
    english_name = 'South Georgia and the South Sandwich Islands'
    flag = 'images\\flags\\GS.png'
    languages = [
        English(u'South Georgia and the South Sandwich Islands')
    ]


class Guatemala(Country):
    code = 'GT'
    english_name = 'Guatemala'
    flag = 'images\\flags\\GT.png'
    languages = [
        Spanish(u'Guatemala')
    ]


class Guam(Country):
    code = 'GU'
    english_name = 'Guam'
    flag = 'images\\flags\\GU.png'
    languages = [
        Chamorro(u'Guåhån'),
        English(u'Guam')
    ]


class GuineaBissau(Country):
    code = 'GW'
    english_name = 'Guinea Bissau'
    flag = 'images\\flags\\GW.png'
    languages = [
        Portuguese(u'Guiné-Bissau')
    ]


class Guyana(Country):
    code = 'GY'
    english_name = 'Guyana'
    flag = 'images\\flags\\GY.png'
    languages = [
        English(u'Guyana')
    ]


class HongKong(Country):
    code = 'HK'
    english_name = 'Hong Kong (SAR of China)'
    flag = 'images\\flags\\HK.png'
    languages = [
        English(u'Hong Kong'),
        ChineseTraditional(u'香港')
    ]


class HeardIslandandMcDonaldIslands(Country):
    code = 'HM'
    english_name = 'Heard Island and McDonald Islands'
    flag = 'images\\flags\\HM.png'
    languages = [
        English(u'Heard Island and McDonald Islands')
    ]


class Honduras(Country):
    code = 'HN'
    english_name = 'Honduras'
    flag = 'images\\flags\\HN.png'
    languages = [
        Spanish(u'Honduras')
    ]


class Croatia(Country):
    code = 'HR'
    english_name = 'Croatia'
    flag = 'images\\flags\\HR.png'
    languages = [
        Croatian(u'Hrvatska')
    ]


class Haiti(Country):
    code = 'HT'
    english_name = 'Haiti'
    flag = 'images\\flags\\HT.png'
    languages = [
        French(u'Haïti'),
        HaitianCreole(u'Ayiti')
    ]


class Hungary(Country):
    code = 'HU'
    english_name = 'Hungary'
    flag = 'images\\flags\\HU.png'
    languages = [
        Hungarian(u'Magyarország')
    ]


class Indonesia(Country):
    code = 'ID'
    english_name = 'Indonesia'
    flag = 'images\\flags\\ID.png'
    languages = [
        Indonesian(u'Indonesia')
    ]


class Ireland(Country):
    code = 'IE'
    english_name = 'Ireland'
    flag = 'images\\flags\\IE.png'
    languages = [
        English(u'Ireland'),
        Irish(u'Éire')
    ]


class Israel(Country):
    code = 'IL'
    english_name = 'Israel'
    flag = 'images\\flags\\IL.png'
    languages = [
        Hebrew(u'ישראל')
    ]


class IsleofMan(Country):
    code = 'IM'
    english_name = 'Isle of Man'
    flag = 'images\\flags\\IM.png'
    languages = [
        English(u'Isle of Man')
    ]


class India(Country):
    code = 'IN'
    english_name = 'India'
    flag = 'images\\flags\\IN.png'
    languages = [
        English(u'India'),
        Hindi(u'भारत')
    ]


class BritishIndianOceanTerritory(Country):
    code = 'IO'
    english_name = 'British Indian Ocean Territory'
    flag = 'images\\flags\\IO.png'
    languages = [
        English(u'British Indian Ocean Territory')
    ]


class Iraq(Country):
    code = 'IQ'
    english_name = 'Iraq'
    flag = 'images\\flags\\IQ.png'
    languages = [
        Arabic(u'العراق'),
        Kurdish(u'Iraq')
    ]


class Iran(Country):
    code = 'IR'
    english_name = 'Iran'
    flag = 'images\\flags\\IR.png'
    languages = [
        Persian(u'ایران')
    ]


class Iceland(Country):
    code = 'IS'
    english_name = 'Iceland'
    flag = 'images\\flags\\IS.png'
    languages = [
        Icelandic(u'Ísland')
    ]


class Italia(Country):
    code = 'IT'
    english_name = 'Italia'
    flag = 'images\\flags\\IT.png'
    languages = [
        German(u'Italia'),
        French(u'Italia'),
        Italian(u'Italia')
    ]


class Jersey(Country):
    code = 'JE'
    english_name = 'Jersey'
    flag = 'images\\flags\\JE.png'
    languages = [
        English(u'Jersey')
    ]


class Jamaica(Country):
    code = 'JM'
    english_name = 'Jamaica'
    flag = 'images\\flags\\JM.png'
    languages = [
        English(u'Jamaica')
    ]


class Jordan(Country):
    code = 'JO'
    english_name = 'Jordan'
    flag = 'images\\flags\\JO.png'
    languages = [
        Arabic(u'الأُرْدُن')
    ]


class Japan(Country):
    code = 'JP'
    english_name = 'Japan'
    flag = 'images\\flags\\JP.png'
    languages = [
        Japanese(u'日本')
    ]


class Kenya(Country):
    code = 'KE'
    english_name = 'Kenya'
    flag = 'images\\flags\\KE.png'
    languages = [
        English(u'Kenya'),
        Swahili(u'Kenya')
    ]


class Kyrgyzstan(Country):
    code = 'KG'
    english_name = 'Kyrgyzstan'
    flag = 'images\\flags\\KG.png'
    languages = [
        Kyrgyz(u'Кыргызстан'),
        Russian(u'Киргизия')
    ]


class Cambodia(Country):
    code = 'KH'
    english_name = 'Cambodia'
    flag = 'images\\flags\\KH.png'
    languages = [
        Khmer(u'កម្ពុជា')
    ]


class Kiribati(Country):
    code = 'KI'
    english_name = 'Kiribati'
    flag = 'images\\flags\\KI.png'
    languages = [
        English(u'Kiribati')
    ]


class Comores(Country):
    code = 'KM'
    english_name = 'Comores'
    flag = 'images\\flags\\KM.png'
    languages = [
        Arabic(u'ﺍﻟﻘﻤﺮي'),
        French(u'Comores'),
        Swahili(u'Komori')
    ]


class SaintKittsandNevis(Country):
    code = 'KN'
    english_name = 'Saint Kitts and Nevis'
    flag = 'images\\flags\\KN.png'
    languages = [
        English(u'Saint Kitts and Nevis')
    ]


class NorthKorea(Country):
    code = 'KP'
    english_name = 'North Korea'
    flag = 'images\\flags\\KP.png'
    languages = [
        Korean(u'북조선')
    ]


class SouthKorea(Country):
    code = 'KR'
    english_name = 'South Korea'
    flag = 'images\\flags\\KR.png'
    languages = [
        English(u''),
        Korean(u'대한민국')
    ]


class Kuweit(Country):
    code = 'KW'
    english_name = 'Kuweit'
    flag = 'images\\flags\\KW.png'
    languages = [
        Arabic(u'الكويت')
    ]


class CaymanIslands(Country):
    code = 'KY'
    english_name = 'Cayman Islands'
    flag = 'images\\flags\\KY.png'
    languages = [
        English(u'Cayman Islands')
    ]


class Kazakhstan(Country):
    code = 'KZ'
    english_name = 'Kazakhstan'
    flag = 'images\\flags\\KZ.png'
    languages = [
        Kazakh(u'Қазақстан'),
        Russian(u'Казахстан')
    ]


class Laos(Country):
    code = 'LA'
    english_name = 'Laos'
    flag = 'images\\flags\\LA.png'
    languages = [
        Lao(u'ປະຊາຊົນລາວ')
    ]


class Lebanon(Country):
    code = 'LB'
    english_name = 'Lebanon'
    flag = 'images\\flags\\LB.png'
    languages = [
        Arabic(u'لبنان'),
        French(u'Liban')
    ]


class SaintLucia(Country):
    code = 'LC'
    english_name = 'Saint Lucia'
    flag = 'images\\flags\\LC.png'
    languages = [
        English(u'Saint Lucia')
    ]


class Liechtenstein(Country):
    code = 'LI'
    english_name = 'Liechtenstein'
    flag = 'images\\flags\\LI.png'
    languages = [
        German(u'Liechtenstein')
    ]


class SriLanka(Country):
    code = 'LK'
    english_name = 'Sri Lanka'
    flag = 'images\\flags\\LK.png'
    languages = [
        Sinhala(u'ශ්‍රී ලංකා'),
        Tamil(u'இலங்கை')
    ]


class Liberia(Country):
    code = 'LR'
    english_name = 'Liberia'
    flag = 'images\\flags\\LR.png'
    languages = [
        English(u'Liberia')
    ]


class Lesotho(Country):
    code = 'LS'
    english_name = 'Lesotho'
    flag = 'images\\flags\\LS.png'
    languages = [
        English(u'Lesotho'),
        SouthernSotho(u'Lesotho')
    ]


class Lithuania(Country):
    code = 'LT'
    english_name = 'Lithuania'
    flag = 'images\\flags\\LT.png'
    languages = [
        Lithuanian(u'Lietuva')
    ]


class Luxembourg(Country):
    code = 'LU'
    english_name = 'Luxembourg'
    flag = 'images\\flags\\LU.png'
    languages = [
        German(u'Luxemburg'),
        French(u'Luxembourg'),
        Luxembourgish(u'Lëtzebuerg')
    ]


class Latvia(Country):
    code = 'LV'
    english_name = 'Latvia'
    flag = 'images\\flags\\LV.png'
    languages = [
        Latvian(u'Latvija')
    ]


class Libya(Country):
    code = 'LY'
    english_name = 'Libya'
    flag = 'images\\flags\\LY.png'
    languages = [
        Arabic(u'ليبيا')
    ]


class Morocco(Country):
    code = 'MA'
    english_name = 'Morocco'
    flag = 'images\\flags\\MA.png'
    languages = [
        Arabic(u'المغرب'),
        French(u'Maroc'),
        StandardMoroccanTamazight(u'ⵍⵎⵖⵔⵉⴱ')
    ]


class Monaco(Country):
    code = 'MC'
    english_name = 'Monaco'
    flag = 'images\\flags\\MC.png'
    languages = [
        French(u'Monaco')
    ]


class Moldova(Country):
    code = 'MD'
    english_name = 'Moldova'
    flag = 'images\\flags\\MD.png'
    languages = [
        Romanian(u'Moldova'),
        Russian(u'Молдавия'),
        Ukrainian(u'Молдова')
    ]


class Montenegro(Country):
    code = 'ME'
    english_name = 'Montenegro'
    flag = 'images\\flags\\ME.png'
    languages = [
        BosnianCyrillic(u'Crna Gora'),
        Croatian(u'Crna Gora'),
        Albanian(u'Mali i Zi'),
        SerbianCyrillic(u'Црна Гора')
    ]


class SaintMartinFrench(Country):
    code = 'MF'
    english_name = 'Saint Martin (French part)'
    flag = 'images\\flags\\MF.png'
    languages = [
        French(u'Saint-Martin')
    ]


class Madagascar(Country):
    code = 'MG'
    english_name = 'Madagascar'
    flag = 'images\\flags\\MG.png'
    languages = [
        French(u'Madagascar'),
        Malagasy(u'Madagasikara')
    ]


class MarshallIslands(Country):
    code = 'MH'
    english_name = 'Marshall Islands'
    flag = 'images\\flags\\MH.png'
    languages = [
        English(u'Marshall Islands'),
        Marshallese(u'Aelōn̄ in M̧ajeļ')
    ]


class Macedonia(Country):
    code = 'MK'
    english_name = 'Macedonia (Former Yugoslav Republic of)'
    flag = 'images\\flags\\MK.png'
    languages = [
        Macedonian(u'Македонија')
    ]


class Mali(Country):
    code = 'ML'
    english_name = 'Mali'
    flag = 'images\\flags\\ML.png'
    languages = [
        French(u'Mali')
    ]


class Myanmar(Country):
    code = 'MM'
    english_name = 'Myanmar'
    flag = 'images\\flags\\MM.png'
    languages = [
        Burmese(u'မြန်မာပြည်')
    ]


class Mongolia(Country):
    code = 'MN'
    english_name = 'Mongolia'
    flag = 'images\\flags\\MN.png'
    languages = [
        Mongolian(u'Монгол Улс')
    ]


class Macao(Country):
    code = 'MO'
    english_name = 'Macao (SAR of China)'
    flag = 'images\\flags\\MO.png'
    languages = [
        Portuguese(u'Macau'),
        ChineseTraditional(u'澳門')
    ]


class NorthernMarianaIslands(Country):
    code = 'MP'
    english_name = 'Northern Mariana Islands'
    flag = 'images\\flags\\MP.png'
    languages = [
        Chamorro(u'Sankattan Siha Na Islas Mariånas'),
        English(u'Northern Mariana Islands')
    ]


class Martinique(Country):
    code = 'MQ'
    english_name = 'Martinique'
    flag = 'images\\flags\\MQ.png'
    languages = [
        French(u'Martinique')
    ]


class Mauritania(Country):
    code = 'MR'
    english_name = 'Mauritania'
    flag = 'images\\flags\\MR.png'
    languages = [
        Arabic(u'موريتانيا'),
        French(u'Mauritanie')
    ]


class Montserrat(Country):
    code = 'MS'
    english_name = 'Montserrat'
    flag = 'images\\flags\\MS.png'
    languages = [
        English(u'Montserrat')
    ]


class Malta(Country):
    code = 'MT'
    english_name = 'Malta'
    flag = 'images\\flags\\MT.png'
    languages = [
        English(u'Malta'),
        Maltese(u'Malta')
    ]


class Mauritius(Country):
    code = 'MU'
    english_name = 'Mauritius'
    flag = 'images\\flags\\MU.png'
    languages = [
        English(u'Mauritius'),
        French(u'Maurice'),
        Morisyen(u'Moris')
    ]


class Maldives(Country):
    code = 'MV'
    english_name = 'Maldives'
    flag = 'images\\flags\\MV.png'
    languages = [
        Dhivehi(u'ދިވެހިރާއްޖެ')
    ]


class Malawi(Country):
    code = 'MW'
    english_name = 'Malawi'
    flag = 'images\\flags\\MW.png'
    languages = [
        English(u'Malawi'),
        Nyanja(u'Malawi')
    ]


class Mexico(Country):
    code = 'MX'
    english_name = 'Mexico'
    flag = 'images\\flags\\MX.png'
    languages = [
        Spanish(u'México')
    ]


class Malaysia(Country):
    code = 'MY'
    english_name = 'Malaysia'
    flag = 'images\\flags\\MY.png'
    languages = [
        Malay(u'Malaysia')
    ]


class Mozambique(Country):
    code = 'MZ'
    english_name = 'Mozambique'
    flag = 'images\\flags\\MZ.png'
    languages = [
        Portuguese(u'Mozambique')
    ]


class Namibia(Country):
    code = 'NA'
    english_name = 'Namibia'
    flag = 'images\\flags\\NA.png'
    languages = [
        German(u'Namibia'),
        English(u'Namibia')
    ]


class NewCaledonia(Country):
    code = 'NC'
    english_name = 'New Caledonia'
    flag = 'images\\flags\\NC.png'
    languages = [
        French(u'Nouvelle-Calédonie')
    ]


class Niger(Country):
    code = 'NE'
    english_name = 'Niger'
    flag = 'images\\flags\\NE.png'
    languages = [
        French(u'Niger')
    ]


class NorfolkIsland(Country):
    code = 'NF'
    english_name = 'Norfolk Island'
    flag = 'images\\flags\\NF.png'
    languages = [
        English(u'Norfolk Island'),
        PitcairnNorfolk(u'Norfuk Ailen')
    ]


class Nigeria(Country):
    code = 'NG'
    english_name = 'Nigeria'
    flag = 'images\\flags\\NG.png'
    languages = [
        English(u'Nigeria')
    ]


class Nicaragua(Country):
    code = 'NI'
    english_name = 'Nicaragua'
    flag = 'images\\flags\\NI.png'
    languages = [
        Spanish(u'Nicaragua')
    ]


class TheNetherlands(Country):
    code = 'NL'
    english_name = 'The Netherlands'
    flag = 'images\\flags\\NL.png'
    languages = [
        Dutch(u'Nederland')
    ]


class Norway(Country):
    code = 'NO'
    english_name = 'Norway'
    flag = 'images\\flags\\NO.png'
    languages = [
        NorwegianBokmal(u'Norge'),
        NorwegianNynorsk(u'Noreg'),
        Norwegian(u'Norge'),
        NorthernSami(u'Norga')
    ]


class Nepal(Country):
    code = 'NP'
    english_name = 'Nepal'
    flag = 'images\\flags\\NP.png'
    languages = [
        Nepali(u'')
    ]


class CountryOfNauru(Country):
    code = 'NR'
    english_name = 'Nauru'
    flag = 'images\\flags\\NR.png'
    languages = [
        English(u'Nauru'),
        Nauru(u'')
    ]


class Niue(Country):
    code = 'NU'
    english_name = 'Niue'
    flag = 'images\\flags\\NU.png'
    languages = [
        English(u'Niue'),
        Niuean(u'')
    ]


class NewZealand(Country):
    code = 'NZ'
    english_name = 'New Zealand'
    flag = 'images\\flags\\NZ.png'
    languages = [
        English(u'New Zealand'),
        Maori(u'')
    ]


class Oman(Country):
    code = 'OM'
    english_name = 'Oman'
    flag = 'images\\flags\\OM.png'
    languages = [
        Arabic(u'سلطنة عُمان')
    ]


class Panama(Country):
    code = 'PA'
    english_name = 'Panama'
    flag = 'images\\flags\\PA.png'
    languages = [
        Spanish(u'Panama')
    ]


class Peru(Country):
    code = 'PE'
    english_name = 'Peru'
    flag = 'images\\flags\\PE.png'
    languages = [
        Spanish(u'Perú')
    ]


class FrenchPolynesia(Country):
    code = 'PF'
    english_name = 'French Polynesia'
    flag = 'images\\flags\\PF.png'
    languages = [
        French(u'Polynésie française')
    ]


class PapuaNewGuinea(Country):
    code = 'PG'
    english_name = 'Papua New Guinea'
    flag = 'images\\flags\\PG.png'
    languages = [
        English(u'Papua New Guinea'),
        HiriMotu(u''),
        TokPisin(u'')
    ]


class Philippines(Country):
    code = 'PH'
    english_name = 'Philippines'
    flag = 'images\\flags\\PH.png'
    languages = [
        English(u'Philippines'),
        Tagalog(u'')
    ]


class Pakistan(Country):
    code = 'PK'
    english_name = 'Pakistan'
    flag = 'images\\flags\\PK.png'
    languages = [
        English(u''),
        Urdu(u'پاکستان')
    ]


class Poland(Country):
    code = 'PL'
    english_name = 'Poland'
    flag = 'images\\flags\\PL.png'
    languages = [
        Polish(u'Polska')
    ]


class SaintPierreandMiquelon(Country):
    code = 'PM'
    english_name = 'Saint Pierre and Miquelon'
    flag = 'images\\flags\\PM.png'
    languages = [
        French(u'Saint-Pierre-et-Miquelon')
    ]


class Pitcairn(Country):
    code = 'PN'
    english_name = 'Pitcairn'
    flag = 'images\\flags\\PN.png'
    languages = [
        English(u'Pitcairn'),
        PitcairnNorfolk(u'Pitkern')
    ]


class PuertoRico(Country):
    code = 'PR'
    english_name = 'Puerto Rico'
    flag = 'images\\flags\\PR.png'
    languages = [
        English(u''),
        Spanish(u'Puerto Rico')
    ]


class PalestinianTerritory(Country):
    code = 'PS'
    english_name = 'Palestinian Territory'
    flag = 'images\\flags\\PS.png'
    languages = [
        Arabic(u'الأراضي الفلسطينية'),
        Hebrew(u'טריטוריה פלסטינית')
    ]


class Portugal(Country):
    code = 'PT'
    english_name = 'Portugal'
    flag = 'images\\flags\\PT.png'
    languages = [
        Portuguese(u'Portugal')
    ]


class Palau(Country):
    code = 'PW'
    english_name = 'Palau'
    flag = 'images\\flags\\PW.png'
    languages = [
        English(u'Palau'),
        Japanese(u'パラオ'),
        Palauan(u'Belau'),
        Tobian(u'Palau')
    ]


class Paraguay(Country):
    code = 'PY'
    english_name = 'Paraguay'
    flag = 'images\\flags\\PY.png'
    languages = [
        Spanish(u'Paraguay'),
        Guarani(u'Paraguái')
    ]


class Qatar(Country):
    code = 'QA'
    english_name = 'Qatar'
    flag = 'images\\flags\\QA.png'
    languages = [
        Arabic(u'قطر')
    ]


class Reunion(Country):
    code = 'RE'
    english_name = 'Reunion'
    flag = 'images\\flags\\RE.png'
    languages = [
        French(u'La Réunion')
    ]


class Romania(Country):
    code = 'RO'
    english_name = 'Romania'
    flag = 'images\\flags\\RO.png'
    languages = [
        Romanian(u'România')
    ]


class Serbia(Country):
    code = 'RS'
    english_name = 'Serbia'
    flag = 'images\\flags\\RS.png'
    languages = [
        SerbianCyrillic(u'Србија')
    ]


class Russia(Country):
    code = 'RU'
    english_name = 'Russia'
    flag = 'images\\flags\\RU.png'
    languages = [
        Russian(u'Россия')
    ]


class Rwanda(Country):
    code = 'RW'
    english_name = 'Rwanda'
    flag = 'images\\flags\\RW.png'
    languages = [
        English(u'Ikinyarwanda'),
        French(u'Rwanda'),
        Kinyarwanda(u'Rwanda')
    ]


class SaudiArabia(Country):
    code = 'SA'
    english_name = 'Saudi Arabia'
    flag = 'images\\flags\\SA.png'
    languages = [
        Arabic(u'السعودية')
    ]


class SolomonIslands(Country):
    code = 'SB'
    english_name = 'Solomon Islands'
    flag = 'images\\flags\\SB.png'
    languages = [
        English(u'Solomon Islands')
    ]


class Seychelles(Country):
    code = 'SC'
    english_name = 'Seychelles'
    flag = 'images\\flags\\SC.png'
    languages = [
        SeychelloisCreole(u'Sesel'),
        English(u'Seychelles'),
        French(u'Seychelles')
    ]


class Sudan(Country):
    code = 'SD'
    english_name = 'Sudan'
    flag = 'images\\flags\\SD.png'
    languages = [
        Arabic(u'السودان'),
        English(u'Sudan')
    ]


class Sweden(Country):
    code = 'SE'
    english_name = 'Sweden'
    flag = 'images\\flags\\SE.png'
    languages = [
        Swedish(u'Sverige')
    ]


class Singapore(Country):
    code = 'SG'
    english_name = 'Singapore'
    flag = 'images\\flags\\SG.png'
    languages = [
        English(u'Singapore'),
        Malay(u'Singapura'),
        Tamil(u'சிங்கப்பூர்'),
        ChineseSimplified(u'新加坡')
    ]


class SaintHelena(Country):
    code = 'SH'
    english_name = 'Saint Helena'
    flag = 'images\\flags\\SH.png'
    languages = [
        English(u'Saint Helena')
    ]


class Slovenia(Country):
    code = 'SI'
    english_name = 'Slovenia'
    flag = 'images\\flags\\SI.png'
    languages = [
        Slovenian(u'Slovenija')
    ]


class SvalbardandJanMayen(Country):
    code = 'SJ'
    english_name = 'Svalbard and Jan Mayen'
    flag = 'images\\flags\\SJ.png'
    languages = [
        Norwegian(u'Svalbard og Jan Mayen')
    ]


class Slovakia(Country):
    code = 'SK'
    english_name = 'Slovakia'
    flag = 'images\\flags\\SK.png'
    languages = [
        Slovak(u'Slovensko')
    ]


class SierraLeone(Country):
    code = 'SL'
    english_name = 'Sierra Leone'
    flag = 'images\\flags\\SL.png'
    languages = [
        English(u'Sierra Leone')
    ]


class SanMarino(Country):
    code = 'SM'
    english_name = 'San Marino'
    flag = 'images\\flags\\SM.png'
    languages = [
        Italian(u'San Marino')
    ]


class Senegal(Country):
    code = 'SN'
    english_name = 'Senegal'
    flag = 'images\\flags\\SN.png'
    languages = [
        French(u'Sénégal')
    ]


class Somalia(Country):
    code = 'SO'
    english_name = 'Somalia'
    flag = 'images\\flags\\SO.png'
    languages = [
        Arabic(u'الصومال'),
        Somali(u'Somalia')
    ]


class Suriname(Country):
    code = 'SR'
    english_name = 'Suriname'
    flag = 'images\\flags\\SR.png'
    languages = [
        Dutch(u'Suriname')
    ]


class SaoTomeandPrincipe(Country):
    code = 'ST'
    english_name = 'São Tomé and Príncipe'
    flag = 'images\\flags\\ST.png'
    languages = [
        Portuguese(u'São Tomé e Príncipe')
    ]


class SouthSudan(Country):
    code = 'SS'
    english_name = 'South Sudan'
    flag = 'images\\flags\\SS.png'
    languages = [
        English(u'South Sudan')
    ]


class ElSalvador(Country):
    code = 'SV'
    english_name = 'El Salvador'
    flag = 'images\\flags\\SV.png'
    languages = [
        Spanish(u'El Salvador')
    ]


class SaintMartinDutch(Country):
    code = 'SX'
    english_name = 'Saint Martin (Dutch part)'
    flag = 'images\\flags\\SX.png'
    languages = [
        English(u''),
        Dutch(u'Sint Maarten')
    ]


class Syria(Country):
    code = 'SY'
    english_name = 'Syria'
    flag = 'images\\flags\\SY.png'
    languages = [
        Arabic(u'سوريا'),
        Kurdish(u'Sūriyya')
    ]


class Swaziland(Country):
    code = 'SZ'
    english_name = 'Swaziland'
    flag = 'images\\flags\\SZ.png'
    languages = [
        English(u'Swaziland'),
        Swati(u'káNgwane')
    ]


class TurksandCaicosIslands(Country):
    code = 'TC'
    english_name = 'Turks and Caicos Islands'
    flag = 'images\\flags\\TC.png'
    languages = [
        English(u'Turks and Caicos Islands')
    ]


class Chad(Country):
    code = 'TD'
    english_name = 'Chad'
    flag = 'images\\flags\\TD.png'
    languages = [
        Arabic(u'تشاد'),
        French(u'Tchad')
    ]


class FrenchSouthernandAntarcticLands(Country):
    code = 'TF'
    english_name = 'French Southern and Antarctic Lands'
    flag = 'images\\flags\\TF.png'
    languages = [
        French(u'Terres australes et antarctiques françaises')
    ]


class Togo(Country):
    code = 'TG'
    english_name = 'Togo'
    flag = 'images\\flags\\TG.png'
    languages = [
        French(u'Togo')
    ]


class Thailand(Country):
    code = 'TH'
    english_name = 'Thailand'
    flag = 'images\\flags\\TH.png'
    languages = [
        Thai(u'ประเทศไทย')
    ]


class Tajikistan(Country):
    code = 'TJ'
    english_name = 'Tajikistan'
    flag = 'images\\flags\\TJ.png'
    languages = [
        Russian(u'Таджикистан'),
        Tajik(u'Тоҷикистон')
    ]


class Tokelau(Country):
    code = 'TK'
    english_name = 'Tokelau'
    flag = 'images\\flags\\TK.png'
    languages = [
        English(u'Tokelau'),
        Samoan(u'Tokelau'),
        Tokelauan(u'Fakatokelau')
    ]


class TimorLeste(Country):
    code = 'TL'
    english_name = 'Timor-Leste'
    flag = 'images\\flags\\TL.png'
    languages = [
        Portuguese(u'Timor-Leste'),
        Tetum(u'Timor Lorosa\'e')
    ]


class Turkmenistan(Country):
    code = 'TM'
    english_name = 'Turkmenistan'
    flag = 'images\\flags\\TM.png'
    languages = [
        Turkmen(u'Türkmenistan')
    ]


class Tunisia(Country):
    code = 'TN'
    english_name = 'Tunisia'
    flag = 'images\\flags\\TN.png'
    languages = [
        Arabic(u'تونس'),
        French(u'Tunisie')
    ]


class Tonga(Country):
    code = 'TO'
    english_name = 'Tonga'
    flag = 'images\\flags\\TO.png'
    languages = [
        English(u'Tonga')
    ]


class Turkey(Country):
    code = 'TR'
    english_name = 'Turkey'
    flag = 'images\\flags\\TR.png'
    languages = [
        Turkish(u'Türkiye')
    ]


class TrinidadandTobago(Country):
    code = 'TT'
    english_name = 'Trinidad and Tobago'
    flag = 'images\\flags\\TT.png'
    languages = [
        English(u'Trinidad and Tobago')
    ]


class Tuvalu(Country):
    code = 'TV'
    english_name = 'Tuvalu'
    flag = 'images\\flags\\TV.png'
    languages = [
        English(u'Tuvalu')
    ]


class Taiwan(Country):
    code = 'TW'
    english_name = 'Taiwan'
    flag = 'images\\flags\\TW.png'
    languages = [
        ChineseTraditional(u'台灣')
    ]


class Tanzania(Country):
    code = 'TZ'
    english_name = 'Tanzania'
    flag = 'images\\flags\\TZ.png'
    languages = [
        English(u'Tanzania'),
        Swahili(u'Tanzania')
    ]


class Ukraine(Country):
    code = 'UA'
    english_name = 'Ukraine'
    flag = 'images\\flags\\UA.png'
    languages = [
        Ukrainian(u'Україна')
    ]


class Uganda(Country):
    code = 'UG'
    english_name = 'Uganda'
    flag = 'images\\flags\\UG.png'
    languages = [
        English(u'Uganda'),
        Swahili(u'Uganda')
    ]


class UnitedStatesMinorOutlyingIslands(Country):
    code = 'UM'
    english_name = 'United States Minor Outlying Islands'
    flag = 'images\\flags\\UM.png'
    languages = [
        English(u'United States Minor Outlying Islands')
    ]


class UnitedStatesofAmerica(Country):
    code = 'US'
    english_name = 'United States of America'
    flag = 'images\\flags\\US.png'
    languages = [
        English(u'United States of America')
    ]


class Uruguay(Country):
    code = 'UY'
    english_name = 'Uruguay'
    flag = 'images\\flags\\UY.png'
    languages = [
        Spanish(u'Uruguay')
    ]


class Uzbekistan(Country):
    code = 'UZ'
    english_name = 'Uzbekistan'
    flag = 'images\\flags\\UZ.png'
    languages = [
        KaraKalpak(u'O\'zbekstan'),
        Uzbek(u'O\'zbekiston')
    ]


class CityoftheVatican(Country):
    code = 'VA'
    english_name = 'City of the Vatican'
    flag = 'images\\flags\\VA.png'
    languages = [
        Italian(u'Città del Vaticano')
    ]


class SaintVincentandtheGrenadines(Country):
    code = 'VC'
    english_name = 'Saint Vincent and the Grenadines'
    flag = 'images\\flags\\VC.png'
    languages = [
        English(u'Saint Vincent and the Grenadines')
    ]


class Venezuela(Country):
    code = 'VE'
    english_name = 'Venezuela'
    flag = 'images\\flags\\VE.png'
    languages = [
        Spanish(u'Venezuela')
    ]


class BritishVirginIslands(Country):
    code = 'VG'
    english_name = 'British Virgin Islands'
    flag = 'images\\flags\\VG.png'
    languages = [
        English(u'British Virgin Islands')
    ]


class UnitedStatesVirginIslands(Country):
    code = 'VI'
    english_name = 'United States Virgin Islands'
    flag = 'images\\flags\\VI.png'
    languages = [
        English(u'United States Virgin Islands')
    ]


class Vietnam(Country):
    code = 'VN'
    english_name = 'Vietnam'
    flag = 'images\\flags\\VN.png'
    languages = [
        Vietnamese(u'Việt Nam')
    ]


class Vanuatu(Country):
    code = 'VU'
    english_name = 'Vanuatu'
    flag = 'images\\flags\\VU.png'
    languages = [
        Bislama(u'Vanuatu'),
        English(u'Vanuatu'),
        French(u'Vanuatu')
    ]


class WallisandFutuna(Country):
    code = 'WF'
    english_name = 'Wallis and Futuna'
    flag = 'images\\flags\\WF.png'
    languages = [
        French(u'Wallis-et-Futuna')
    ]


class Samoa(Country):
    code = 'WS'
    english_name = 'Samoa'
    flag = 'images\\flags\\WS.png'
    languages = [
        English(u'Samoa'),
        Samoan(u'')
    ]


class Yemen(Country):
    code = 'YE'
    english_name = 'Yemen'
    flag = 'images\\flags\\YE.png'
    languages = [
        Arabic(u'اليَمَن')
    ]


class Mayotte(Country):
    code = 'YT'
    english_name = 'Mayotte'
    flag = 'images\\flags\\YT.png'
    languages = [
        French(u'Mayotte')
    ]


class SouthAfrica(Country):
    code = 'ZA'
    english_name = 'South Africa'
    flag = 'images\\flags\\ZA.png'
    languages = [
        Afrikaans(u'Suid-Afrika'),
        English(u'South Africa'),
        SouthernSotho(u'Afrika Borwa'),
        Setswana(u'Aferika Borwa'),
        Xhosa(u'Mzantsi Afrika'),
        Zulu(u'Iningizimu Afrika')
    ]


class Zambia(Country):
    code = 'ZM'
    english_name = 'Zambia'
    flag = 'images\\flags\\ZM.png'
    languages = [
        English(u'Zambia')
    ]


class Zimbabwe(Country):
    code = 'ZW'
    english_name = 'Zimbabwe'
    flag = 'images\\flags\\ZW.png'
    languages = [
        English(u'Zimbabwe'),
        NorthNdebele(u'Zimbabwe'),
        Shona(u'Zimbabwe')
    ]


if __name__ == '__main__':
    found_wx_codes = []
    found_lcid_codes = []

    for c in countries:
        print(c.english_name)
        print('    COUNTRY CODE:', c.code)
        for l in c.languages:
            l_lcid = l.lcid
            w_code = l.wx_code
            print('   ', l.english_name)
            print('   ', l.country_name)
            print('        LANGUAGE CODES:', l.locale_names)
            print('        LCID:          ', l_lcid)
            print('        WX CODE:       ', w_code)

            if l_lcid is not None and l_lcid not in found_lcid_codes:
                found_lcid_codes += [l_lcid]

            if w_code is not None and w_code not in found_wx_codes:
                found_wx_codes += [w_code]
    print('\n')
    print('FOUND LCID COUNT:', len(found_lcid_codes))
    print('FOUND WX COUNT:  ', len(found_wx_codes))
    print('WX CODE COUNT:   ', len(list(LCID_TO_WX.keys())))

    import sys

    mod = sys.modules[__name__]
    num_countries = 0
    num_languages = 0
    num_country_languages = 0

    for cls_val in mod.__dict__.values():
        try:
            if issubclass(cls_val, Country):
                num_countries += 1
                num_country_languages += len(cls_val.languages)
            elif issubclass(cls_val, Language):
                num_languages += 1
        except TypeError:
            pass

    print('NUMBER OF COUNTRIES:         ', num_countries)
    print('NUMBER OF LANGUAGES:         ', num_languages)
    print('NUMBER OF COUNTRY LANGUAGES: ', num_country_languages)

# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2018 EventGhost Project <http://eventghost.net/>
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

from __future__ import print_function

import wx
import ctypes
import os
import sys
import locale as _locale
from ctypes.wintypes import LCID, DWORD, INT, WCHAR, LPCWSTR


LANGUAGE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(sys.executable)),
    "languages"
)

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


CODE_PAGES = {
    # IBM EBCDIC US-Canada
    37: 'IBM037',
    # OEM United States
    437: 'IBM437',
    # IBM EBCDIC International
    500: 'IBM500',
    # Arabic (ASMO 708)
    708: 'ASMO-708',
    # Arabic (ASMO-449+, BCON V4)
    709: 'ASMO-708',
    # Arabic (Transparent ASMO);
    # Arabic (DOS)
    720: 'DOS-720',
    # OEM Greek (formerly 437G);
    # Greek (DOS)
    737: 'ibm737',
    # OEM Baltic;
    # Baltic (DOS)
    775: 'ibm775',
    # OEM Multilingual Latin 1;
    # Western European (DOS)
    850: 'ibm850',
    # OEM Latin 2;
    # Central European (DOS)
    852: 'ibm852',
    # OEM Cyrillic (primarily Russian)
    855: 'IBM855',
    # OEM Turkish;
    # Turkish (DOS)
    857: 'ibm857',
    # OEM Multilingual Latin 1 + Euro symbol
    858: 'IBM00858',
    # OEM Portuguese;
    # Portuguese (DOS)
    860: 'IBM860',
    # OEM Icelandic;
    # Icelandic (DOS)
    861: 'ibm861',
    # OEM Hebrew;
    # Hebrew (DOS)
    862: 'DOS-862',
    # OEM French Canadian;
    #  French Canadian (DOS)
    863: 'IBM863',
    # OEM Arabic;
    # Arabic (864)
    864: 'IBM864',
    # OEM Nordic;
    # Nordic (DOS)
    865: 'IBM865',
    # OEM Russian;
    # Cyrillic (DOS)
    866: 'cp866',
    # OEM Modern Greek;
    # Greek, Modern (DOS)
    869: 'ibm869',
    # IBM EBCDIC Multilingual/ROECE (Latin 2);
    # IBM EBCDIC Multilingual Latin 2
    870: 'IBM870',
    # ANSI/OEM Thai (ISO 8859-11);
    # Thai (Windows)
    874: 'windows-874',
    # IBM EBCDIC Greek Modern
    875: 'cp875',
    # ANSI/OEM Japanese;
    # Japanese (Shift-JIS)
    932: 'shift_jis',
    # ANSI/OEM Simplified Chinese (PRC, Singapore);
    # Chinese Simplified (GB2312)
    936: 'gb2312',
    # ANSI/OEM Korean (Unified Hangul Code)
    949: 'ks_c_5601-1987',
    # ANSI/OEM Traditional Chinese (Taiwan; Hong Kong SAR, PRC);
    # Chinese Traditional (Big5)
    950: 'big5',
    # IBM EBCDIC Turkish (Latin 5)
    1026: 'IBM1026',
    # IBM EBCDIC Latin 1/Open System
    1047: 'IBM01047',
    # IBM EBCDIC US-Canada (037 + Euro symbol);
    # IBM EBCDIC (US-Canada-Euro)
    1140: 'IBM01140',
    # IBM EBCDIC Germany (20273 + Euro symbol);
    # IBM EBCDIC (Germany-Euro)
    1141: 'IBM01141',
    # IBM EBCDIC Denmark-Norway (20277 + Euro symbol);
    # IBM EBCDIC (Denmark-Norway-Euro)
    1142: 'IBM01142',
    # IBM EBCDIC Finland-Sweden (20278 + Euro symbol);
    # IBM EBCDIC (Finland-Sweden-Euro)
    1143: 'IBM01143',
    # IBM EBCDIC Italy (20280 + Euro symbol);
    # IBM EBCDIC (Italy-Euro)
    1144: 'IBM01144',
    # IBM EBCDIC Latin America-Spain (20284 + Euro symbol);
    # IBM EBCDIC (Spain-Euro)
    1145: 'IBM01145',
    # IBM EBCDIC United Kingdom (20285 + Euro symbol);
    # IBM EBCDIC (UK-Euro)
    1146: 'IBM01146',
    # IBM EBCDIC France (20297 + Euro symbol);
    # IBM EBCDIC (France-Euro)
    1147: 'IBM01147',
    # IBM EBCDIC International (500 + Euro symbol);
    # IBM EBCDIC (International-Euro)
    1148: 'IBM01148',
    # IBM EBCDIC Icelandic (20871 + Euro symbol);
    # IBM EBCDIC (Icelandic-Euro)
    1149: 'IBM01149',
    # Unicode UTF-16, little endian byte order (BMP of ISO 10646);
    # available only to managed applications
    1200: 'utf-16',
    # Unicode UTF-16, big endian byte order;
    # available only to managed applications
    1201: 'unicodeFFFE',
    # ANSI Central European;
    # Central European (Windows)
    1250: 'windows-1250',
    # ANSI Cyrillic;
    # Cyrillic (Windows)
    1251: 'windows-1251',
    # ANSI Latin 1;
    # Western European (Windows)
    1252: 'windows-1252',
    # ANSI Greek;
    # Greek (Windows)
    1253: 'windows-1253',
    # ANSI Turkish;
    # Turkish (Windows)
    1254: 'windows-1254',
    # ANSI Hebrew;
    # Hebrew (Windows)
    1255: 'windows-1255',
    # ANSI Arabic;
    # Arabic (Windows)
    1256: 'windows-1256',
    # ANSI Baltic;
    # Baltic (Windows)
    1257: 'windows-1257',
    # ANSI/OEM Vietnamese;
    # Vietnamese (Windows)
    1258: 'windows-1258',
    # Korean (Johab)
    1361: 'Johab',
    # MAC Roman; Western European (Mac)
    10000: 'macintosh',
    # Japanese (Mac)
    10001: 'x-mac-japanese',
    # MAC Traditional Chinese (Big5);
    # Chinese Traditional (Mac)
    10002: 'x-mac-chinesetrad',
    # Korean (Mac)
    10003: 'x-mac-korean',
    # Arabic (Mac)
    10004: 'x-mac-arabic',
    # Hebrew (Mac)
    10005: 'x-mac-hebrew',
    # Greek (Mac)
    10006: 'x-mac-greek',
    # Cyrillic (Mac)
    10007: 'x-mac-cyrillic',
    # MAC Simplified Chinese (GB 2312);
    # Chinese Simplified (Mac)
    10008: 'x-mac-chinesesimp',
    # Romanian (Mac)
    10010: 'x-mac-romanian',
    # Ukrainian (Mac)
    10017: 'x-mac-ukrainian',
    # Thai (Mac)
    10021: 'x-mac-thai',
    # MAC Latin 2;
    # Central European (Mac)
    10029: 'x-mac-ce',
    # Icelandic (Mac)
    10079: 'x-mac-icelandic',
    # Turkish (Mac)
    10081: 'x-mac-turkish',
    # Croatian (Mac)
    10082: 'x-mac-croatian',
    # Unicode UTF-32, little endian byte order;
    # available only to managed applications
    12000: 'utf-32',
    # Unicode UTF-32, big endian byte order;
    # available only to managed applications
    12001: 'utf-32BE',
    # CNS Taiwan;
    # Chinese Traditional (CNS)
    20000: 'x-Chinese_CNS',
    # TCA Taiwan
    20001: 'x-cp20001',
    # Eten Taiwan;
    # Chinese Traditional (Eten)
    20002: 'x_Chinese-Eten',
    # IBM5550 Taiwan
    20003: 'x-cp20003',
    # TeleText Taiwan
    20004: 'x-cp20004',
    # Wang Taiwan
    20005: 'x-cp20005',
    # IA5 (IRV International Alphabet No. 5, 7-bit);
    # Western European (IA5)
    20105: 'x-IA5',
    # IA5 German (7-bit)
    20106: 'x-IA5-German',
    # IA5 Swedish (7-bit)
    20107: 'x-IA5-Swedish',
    # IA5 Norwegian (7-bit)
    20108: 'x-IA5-Norwegian',
    # US-ASCII (7-bit)
    20127: 'us-ascii',
    # T.61
    20261: 'x-cp20261',
    # ISO 6937 Non-Spacing Accent
    20269: 'x-cp20269',
    # IBM EBCDIC Germany
    20273: 'IBM273',
    # IBM EBCDIC Denmark-Norway
    20277: 'IBM277',
    # IBM EBCDIC Finland-Sweden
    20278: 'IBM278',
    # IBM EBCDIC Italy
    20280: 'IBM280',
    # IBM EBCDIC Latin America-Spain
    20284: 'IBM284',
    # IBM EBCDIC United Kingdom
    20285: 'IBM285',
    # IBM EBCDIC Japanese Katakana Extended
    20290: 'IBM290',
    # IBM EBCDIC France
    20297: 'IBM297',
    # IBM EBCDIC Arabic
    20420: 'IBM420',
    # IBM EBCDIC Greek
    20423: 'IBM423',
    # IBM EBCDIC Hebrew
    20424: 'IBM424',
    # IBM EBCDIC Korean Extended
    20833: 'x-EBCDIC-KoreanExtended',
    # IBM EBCDIC Thai
    20838: 'IBM-Thai',
    # Russian (KOI8-R);
    # Cyrillic (KOI8-R)
    20866: 'koi8-r',
    # IBM EBCDIC Icelandic
    20871: 'IBM871',
    # IBM EBCDIC Cyrillic Russian
    20880: 'IBM880',
    # IBM EBCDIC Turkish
    20905: 'IBM905',
    # IBM EBCDIC Latin 1/Open System (1047 + Euro symbol)
    20924: 'IBM00924',
    # Japanese (JIS 0208-1990 and 0212-1990)
    20932: 'EUC-JP',
    # Simplified Chinese (GB2312);
    # Chinese Simplified (GB2312-80)
    20936: 'x-cp20936',
    # Korean Wansung
    20949: 'x-cp20949',
    # IBM EBCDIC Cyrillic Serbian-Bulgarian
    21025: 'cp1025',
    # Ukrainian (KOI8-U);
    # Cyrillic (KOI8-U)
    21866: 'koi8-u',
    # ISO 8859-1 Latin 1;
    # Western European (ISO)
    28591: 'iso-8859-1',
    # ISO 8859-2 Central European;
    # Central European (ISO)
    28592: 'iso-8859-2',
    # ISO 8859-3 Latin 3
    28593: 'iso-8859-3',
    # ISO 8859-4 Baltic
    28594: 'iso-8859-4',
    # ISO 8859-5 Cyrillic
    28595: 'iso-8859-5',
    # ISO 8859-6 Arabic
    28596: 'iso-8859-6',
    # ISO 8859-7 Greek
    28597: 'iso-8859-7',
    # ISO 8859-8 Hebrew;
    # Hebrew (ISO-Visual)
    28598: 'iso-8859-8',
    # ISO 8859-9 Turkish
    28599: 'iso-8859-9',
    # ISO 8859-13 Estonian
    28603: 'iso-8859-13',
    # ISO 8859-15 Latin 9
    28605: 'iso-8859-15',
    # Europa 3
    29001: 'x-Europa',
    # ISO 8859-8 Hebrew;
    # Hebrew (ISO-Logical)
    38598: 'iso-8859-8-i',
    # ISO 2022 Japanese with no halfwidth Katakana;
    # Japanese (JIS)
    50220: 'iso-2022-jp',
    # ISO 2022 Japanese with halfwidth Katakana;
    # Japanese (JIS-Allow 1 byte Kana)
    50221: 'csISO2022JP',
    # ISO 2022 Japanese JIS X 0201-1989;
    # Japanese (JIS-Allow 1 byte Kana - SO/SI)
    50222: 'iso-2022-jp',
    # ISO 2022 Korean
    50225: 'iso-2022-kr',
    # ISO 2022 Simplified Chinese;
    # Chinese Simplified (ISO 2022)
    50227: 'x-cp50227',
    # EUC Japanese
    51932: 'euc-jp',
    # EUC Simplified Chinese;
    # Chinese Simplified (EUC)
    51936: 'EUC-CN',
    # EUC Korean
    51949: 'euc-kr',
    # HZ-GB2312 Simplified Chinese;
    # Chinese Simplified (HZ)
    52936: 'hz-gb-2312',
    # Windows XP and later:
    # GB18030 Simplified Chinese (4 byte);
    # Chinese Simplified (GB18030)
    54936: 'GB18030',
    # ISCII Devanagari
    57002: 'x-iscii-de',
    # ISCII Bangla
    57003: 'x-iscii-be',
    # ISCII Tamil
    57004: 'x-iscii-ta',
    # ISCII Telugu
    57005: 'x-iscii-te',
    # ISCII Assamese
    57006: 'x-iscii-as',
    # ISCII Odia
    57007: 'x-iscii-or',
    # ISCII Kannada
    57008: 'x-iscii-ka',
    # ISCII Malayalam
    57009: 'x-iscii-ma',
    # ISCII Gujarati
    57010: 'x-iscii-gu',
    # ISCII Punjabi
    57011: 'x-iscii-pa',
    # Unicode (UTF-7)
    65000: 'utf-7',
    # Unicode (UTF-8)
    65001: 'utf-8',
}

PY3 = sys.version_info[0] > 2

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# localized name of locale, eg "German (Germany)" in UI language
LOCALE_SLOCALIZEDDISPLAYNAME = 0x00000002

# Display name in native locale language, eg "Deutsch (Deutschland)
LOCALE_SNATIVEDISPLAYNAME = 0x00000073

# Language Display Name for a language, eg "German" in UI language
LOCALE_SLOCALIZEDLANGUAGENAME = 0x0000006f

# English name of language, eg "German"
LOCALE_SENGLISHLANGUAGENAME = 0x00001001

# native name of language, eg "Deutsch"
LOCALE_SNATIVELANGUAGENAME = 0x00000004

# localized name of country/region, eg "Germany" in UI language
LOCALE_SLOCALIZEDCOUNTRYNAME = 0x00000006

# English name of country/region, eg "Germany"
LOCALE_SENGLISHCOUNTRYNAME = 0x00001002

# native name of country/region, eg "Deutschland"
LOCALE_SNATIVECOUNTRYNAME = 0x00000008

# Additional LCTypes
# country/region dialing code, example: en-US and en-CA return 1.
LOCALE_IDIALINGCODE = 0x00000005

# list item separator, eg "," for "1,2,3,4"
LOCALE_SLIST = 0x0000000C

# 0 = metric, 1 = US measurement system
LOCALE_IMEASURE = 0x0000000D

# decimal separator, eg "." for 1,234.00
LOCALE_SDECIMAL = 0x0000000E

# thousand separator, eg "," for 1,234.00
LOCALE_STHOUSAND = 0x0000000F

# digit grouping, eg "3;0" for 1,000,000
LOCALE_SGROUPING = 0x00000010

# number of fractional digits eg 2 for 1.00
LOCALE_IDIGITS = 0x00000011

# leading zeros for decimal, 0 for .97, 1 for 0.97
LOCALE_ILZERO = 0x00000012

# negative number mode, 0-4, see documentation
# 0 	Left parenthesis, number, right parenthesis; for example, (1.1)
# 1 	Negative sign, number; for example, -1.1
# 2 	Negative sign, space, number; for example, - 1.1
# 3 	Number, negative sign; for example, 1.1-
# 4 	Number, space, negative sign; for example, 1.1 -
LOCALE_INEGNUMBER = 0x00001010

# native digits for 0-9, eg "0123456789"
LOCALE_SNATIVEDIGITS = 0x00000013

# local monetary symbol, eg "$"
LOCALE_SCURRENCY = 0x00000014

# intl monetary symbol, eg "USD"
LOCALE_SINTLSYMBOL = 0x00000015

# monetary decimal separator, eg "." for $1,234.00
LOCALE_SMONDECIMALSEP = 0x00000016

# monetary thousand separator, eg "," for $1,234.00
LOCALE_SMONTHOUSANDSEP = 0x00000017

# monetary grouping, eg "3;0" for $1,000,000.00
LOCALE_SMONGROUPING = 0x00000018

# local monetary digits, eg 2 for $1.00
LOCALE_ICURRDIGITS = 0x00000019

# positive currency mode, 0-3, see documentation
LOCALE_ICURRENCY = 0x0000001B

# negative currency mode, 0-15, see documentation
LOCALE_INEGCURR = 0x0000001C

# SHORT date format string, eg "MM/dd/yyyy"
LOCALE_SSHORTDATE = 0x0000001F

# LONG date format string, eg "dddd, MMMM dd, yyyy"
LOCALE_SLONGDATE = 0x00000020

# time format string, eg "HH:mm:ss"
LOCALE_STIMEFORMAT = 0x00001003

# AM designator, eg "AM"
LOCALE_SAM = 0x00000028

# PM designator, eg "PM"
LOCALE_SPM = 0x00000029

# type of calendar specifier, eg CAL_GREGORIAN
LOCALE_ICALENDARTYPE = 0x00001009

# additional calendar types specifier, eg CAL_GREGORIAN_US
LOCALE_IOPTIONALCALENDAR = 0x0000100B

# first day of week specifier, 0-6, 0=Monday, 6=Sunday
LOCALE_IFIRSTDAYOFWEEK = 0x0000100C

# first week of year specifier, 0-2, see documentation
LOCALE_IFIRSTWEEKOFYEAR = 0x0000100D

# LONG name for Monday
LOCALE_SDAYNAME1 = 0x0000002A

# LONG name for Tuesday
LOCALE_SDAYNAME2 = 0x0000002B

# LONG name for Wednesday
LOCALE_SDAYNAME3 = 0x0000002C

# LONG name for Thursday
LOCALE_SDAYNAME4 = 0x0000002D

# LONG name for Friday
LOCALE_SDAYNAME5 = 0x0000002E

# LONG name for Saturday
LOCALE_SDAYNAME6 = 0x0000002F

# LONG name for Sunday
LOCALE_SDAYNAME7 = 0x00000030

# abbreviated name for Monday
LOCALE_SABBREVDAYNAME1 = 0x00000031

# abbreviated name for Tuesday
LOCALE_SABBREVDAYNAME2 = 0x00000032

# abbreviated name for Wednesday
LOCALE_SABBREVDAYNAME3 = 0x00000033

# abbreviated name for Thursday
LOCALE_SABBREVDAYNAME4 = 0x00000034

# abbreviated name for Friday
LOCALE_SABBREVDAYNAME5 = 0x00000035

# abbreviated name for Saturday
LOCALE_SABBREVDAYNAME6 = 0x00000036

# abbreviated name for Sunday
LOCALE_SABBREVDAYNAME7 = 0x00000037

# Shortest day name for Monday
LOCALE_SSHORTESTDAYNAME1 = 0x00000060

# Shortest day name for Tuesday
LOCALE_SSHORTESTDAYNAME2 = 0x00000061

# Shortest day name for Wednesday
LOCALE_SSHORTESTDAYNAME3 = 0x00000062

# Shortest day name for Thursday
LOCALE_SSHORTESTDAYNAME4 = 0x00000063

# Shortest day name for Friday
LOCALE_SSHORTESTDAYNAME5 = 0x00000064

# Shortest day name for Saturday
LOCALE_SSHORTESTDAYNAME6 = 0x00000065

# Shortest day name for Sunday
LOCALE_SSHORTESTDAYNAME7 = 0x00000066

# LONG name for January
LOCALE_SMONTHNAME1 = 0x00000038

# LONG name for February
LOCALE_SMONTHNAME2 = 0x00000039

# LONG name for March
LOCALE_SMONTHNAME3 = 0x0000003A

# LONG name for April
LOCALE_SMONTHNAME4 = 0x0000003B

# LONG name for May
LOCALE_SMONTHNAME5 = 0x0000003C

# LONG name for June
LOCALE_SMONTHNAME6 = 0x0000003D

# LONG name for July
LOCALE_SMONTHNAME7 = 0x0000003E

# LONG name for August
LOCALE_SMONTHNAME8 = 0x0000003F

# LONG name for September
LOCALE_SMONTHNAME9 = 0x00000040

# LONG name for October
LOCALE_SMONTHNAME10 = 0x00000041

# LONG name for November
LOCALE_SMONTHNAME11 = 0x00000042

# LONG name for December
LOCALE_SMONTHNAME12 = 0x00000043

# LONG name for 13th month (if exists)
LOCALE_SMONTHNAME13 = 0x0000100E

# abbreviated name for January
LOCALE_SABBREVMONTHNAME1 = 0x00000044

# abbreviated name for February
LOCALE_SABBREVMONTHNAME2 = 0x00000045

# abbreviated name for March
LOCALE_SABBREVMONTHNAME3 = 0x00000046

# abbreviated name for April
LOCALE_SABBREVMONTHNAME4 = 0x00000047

# abbreviated name for May
LOCALE_SABBREVMONTHNAME5 = 0x00000048

# abbreviated name for June
LOCALE_SABBREVMONTHNAME6 = 0x00000049

# abbreviated name for July
LOCALE_SABBREVMONTHNAME7 = 0x0000004A

# abbreviated name for August
LOCALE_SABBREVMONTHNAME8 = 0x0000004B

# abbreviated name for September
LOCALE_SABBREVMONTHNAME9 = 0x0000004C

# abbreviated name for October
LOCALE_SABBREVMONTHNAME10 = 0x0000004D

# abbreviated name for November
LOCALE_SABBREVMONTHNAME11 = 0x0000004E

# abbreviated name for December
LOCALE_SABBREVMONTHNAME12 = 0x0000004F

# abbreviated name for 13th month (if exists)
LOCALE_SABBREVMONTHNAME13 = 0x0000100F

# positive sign, eg ""
LOCALE_SPOSITIVESIGN = 0x00000050

# negative sign, eg "-"
LOCALE_SNEGATIVESIGN = 0x00000051

# positive sign position (derived from INEGCURR)
LOCALE_IPOSSIGNPOSN = 0x00000052

# negative sign position (derived from INEGCURR)
LOCALE_INEGSIGNPOSN = 0x00000053

# mon sym precedes pos amt (derived from ICURRENCY)
LOCALE_IPOSSYMPRECEDES = 0x00000054

# mon sym sep by space from pos amt (derived from ICURRENCY)
LOCALE_IPOSSEPBYSPACE = 0x00000055

# mon sym precedes neg amt (derived from INEGCURR)
LOCALE_INEGSYMPRECEDES = 0x00000056

# mon sym sep by space from neg amt (derived from INEGCURR)
LOCALE_INEGSEPBYSPACE = 0x00000057

# english name of currency, eg "Euro"
LOCALE_SENGCURRNAME = 0x00001007

# native name of currency, eg "euro"
LOCALE_SNATIVECURRNAME = 0x00001008

# year month format string, eg "MM/yyyy"
LOCALE_SYEARMONTH = 0x00001006

# time duration format, eg "hh:mm:ss"
LOCALE_SDURATION = 0x0000005D

# Not a Number, eg "NaN"
LOCALE_SNAN = 0x00000069

# + Infinity, eg "infinity"
LOCALE_SPOSINFINITY = 0x0000006A

# - Infinity, eg "-infinity"
LOCALE_SNEGINFINITY = 0x0000006B

# Returns one of the following 4 reading layout values:
# 0 - Left to right (eg en-US)
# 1 - Right to left (eg arabic locales)
# 2 - Vertical top to bottom with columns to the
#     left and also left to right (ja-JP locales)
# 3 - Vertical top to bottom with columns proceeding to the right
LOCALE_IREADINGLAYOUT = 0x00000070

# Returns 0 for specific cultures, 1 for neutral cultures.
LOCALE_INEUTRAL = 0x00000071

# Returns 0-11 for the negative percent format
# 0 	Negative sign, number, space, percent; for example, -# %
# 1 	Negative sign, number, percent; for example, -#%
# 2 	Negative sign, percent, number; for example, -%#
# 3 	Percent, negative sign, number; for example, %-#
# 4 	Percent, number, negative sign; for example, %#-
# 5 	Number, negative sign, percent; for example, #-%
# 6 	Number, percent, negative sign; for example, #%-
# 7 	Negative sign, percent, space, number; for example, -% #
# 8 	Number, space, percent, negative sign; for example, # %-
# 9 	Percent, space, number, negative sign; for example, % #-
# 10 	Percent, space, negative sign, number; for example, % -#
# 11 	Number, negative sign, space, percent; for example, #- %
LOCALE_INEGATIVEPERCENT = 0x00000074

# Returns 0-3 for the positive percent format
# 0 	Number, space, percent; for example, # %
# 1 	Number, percent; for example, #%
# 2 	Percent, number; for example, %#
# 3 	Percent, space, number; for example, % #
LOCALE_IPOSITIVEPERCENT = 0x00000075

# Returns the percent symbol
LOCALE_SPERCENT = 0x00000076

# Returns the preferred month/day format
LOCALE_SMONTHDAY = 0x00000078

# Returns the preferred SHORT time format
# (ie: no seconds, just h:mm)
LOCALE_SSHORTTIME = 0x00000079

# Returns the permille (U + 2030) symbol
LOCALE_SPERMILLE = 0x00000077

LOCALE_IDEFAULTANSICODEPAGE = 0x00001004
LOCALE_IDEFAULTCODEPAGE = 0x0000000B
LOCALE_SNAME = 0x0000005C

kernel32 = ctypes.windll.Kernel32

# int GetLocaleInfoEx(
#   LPCWSTR lpLocaleName,
#   LCTYPE  LCType,
#   LPWSTR  lpLCData,
#   int     cchData
# );

LCTYPE = DWORD

_GetLocaleInfoEx = kernel32.GetLocaleInfoEx
# _GetLocaleInfoEx.argtypes = [LPCWSTR, LCTYPE, LPWSTR, INT]
_GetLocaleInfoEx.restype = INT


# noinspection PyCallingNonCallable,PyTypeChecker
def get_locale_info(lp_locale_name, lc_type):
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
        raise ctypes.WinError()

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
        output += lp_lc_data[i]

    return output


# LCID LocaleNameToLCID(
#   LPCWSTR lpName,
#   DWORD   dwFlags
# );
_LocaleNameToLCID = kernel32.LocaleNameToLCID
_LocaleNameToLCID.argtypes = [LPCWSTR, DWORD]
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
DEFAULT_USER_LANGUAGE = 'en-US'


# noinspection PyTypeChecker,PyCallingNonCallable
def get_windows_user_language():
    lp_locale_name = (WCHAR * LOCALE_NAME_MAX_LENGTH)()
    cch_locale_name = INT(LOCALE_NAME_MAX_LENGTH)

    if not GetUserDefaultLocaleName(
        ctypes.byref(lp_locale_name),
        cch_locale_name
    ):
        raise ctypes.WinError()

    lp_locale_name = lp_locale_name.value

    for locale in locales:
        for lang in locale.languages:
            if lang.iso_code == lp_locale_name:
                return lang

    lcid = GetUserDefaultUILanguage()

    for locale in locales:
        for lang in locale.languages:
            if lang.lcid == lcid:
                return lang

    default_language, default_locale = DEFAULT_USER_LANGUAGE.rsplit('-', 1)

    for locale in locales:
        if not locale == default_locale:
            continue
        for lang in locale.languages:
            if lang == default_language:
                return lang


def locale_name_to_lcid(locale_name):

    if isinstance(locale_name, str):
        if PY3:
            locale_name = locale_name.encode('utf-8')
        else:
            # noinspection PyUnresolvedReferences
            locale_name = unicode(locale_name)

    res = _LocaleNameToLCID(locale_name, DWORD(0))
    if res == 0:
        return None
    return res


# noinspection PyTypeChecker
def add_separator(num, sep, group_len):
    from textwrap import wrap

    def reverse_string(s):
        return ''.join(s[i] for i in range(len(s) - 1, -1, -1))

    # we need to reverse the number to add the separators. the group count
    # starts at index 0 of the string. so if wee have a number of 1234567
    # and a group length of 3 we do not want to end up with 123,456,7
    # this would be incorrect. so we need to make the count start from the end
    rev = reverse_string(str(num))

    # we use the stdlib wraptext.wrap to split the string into the group
    # lengths we need

    last_g_len = None
    groups = []

    for g_len in group_len:
        if last_g_len is None:
            last_g_len = g_len
        else:
            if not g_len:
                groups += wrap(rev, g_len)
                last_g_len = None
                break
            else:
                groups += wrap(rev, last_g_len)[0]
                last_g_len = g_len
                rev = rev.replace(''.join(groups[-1:]), 1)

    if last_g_len is not None:
        groups += wrap(rev, last_g_len)

    # we then add in the separator by joining the list of groups returned
    # from wraptext.wrap
    rev_output = sep.join(groups)

    # and finally we flip the string once again putting it back the way it was
    output = reverse_string(rev_output)
    return output


class NumberFormat(str):
    def __init__(
        self,
        template,
        group_sep,
        group_len,
        decimal_sep=None,
        precision=None
    ):
        self._decimal_sep = decimal_sep
        self._group_sep = group_sep
        self._group_len = group_len
        self._precision = precision

        str.__init__(self, template)

    def format(self, value):
        if isinstance(value, int):
            digits = add_separator(value, self._group_sep, self._group_len)
            return str.format(self, digits)
        elif isinstance(value, float):
            digits, decimal = str(value).split('.')
            if self._precision is not None:
                decimal = decimal[:self._precision]

            digits = add_separator(digits, self._group_sep, self._group_len)
            return str.format(self, digits + self._decimal_sep + decimal)

        raise ValueError('format value is not an int or a float')


class Language(object):
    ISO639_1 = None
    ISO639_2 = None
    ISO639_3 = None
    _lcid = None
    _lang_id = None
    _english_name = ''
    _native_name = u''

    def __init__(self, locale_name, lcid=None):
        self._locale_name = locale_name
        if lcid is not None:
            self._lcid = lcid
        self.locale = None
        self._iso_code = None

    # noinspection PyUnresolvedReferences
    def __eq__(self, other):
        if isinstance(other, Language):
            other_iso = other.iso_code
            self_iso = self.iso_code

            return (
                other_iso is not None and
                self_iso is not None and
                other_iso == self_iso
            )
        elif isinstance(other, int):
            return other == self.lcid

        else:
            if PY3:
                if isinstance(other, bytes):
                    other = other.decode('utf-8')

                if isinstance(other, str):
                    self_iso = self.iso_code

                    return (
                        self_iso is not None and (
                            other == self_iso or
                            self_iso.startswith(other)
                        )
                    )
            elif isinstance(other, (str, unicode)):
                self_iso = self.iso_code

                return (
                    self_iso is not None and (
                        other == self_iso or
                        self_iso.startswith(other)
                    )
                )

        return False

    @property
    def iso_code(self):
        if self._iso_code is None and self.ISO639_3 is not None:
            iso_code = self.ISO639_3 + '-' + self.locale.locale_iso_code
            if locale_name_to_lcid(iso_code) is not None:
                self._iso_code = iso_code

        if self._iso_code is None and self.ISO639_2 is not None:
            iso_code = self.ISO639_2 + '-' + self.locale.locale_iso_code
            if locale_name_to_lcid(iso_code) is not None:
                self._iso_code = iso_code

        if self._iso_code is None and self.ISO639_1 is not None:
            iso_code = self.ISO639_1 + '-' + self.locale.locale_iso_code
            if locale_name_to_lcid(iso_code) is not None:
                self._iso_code = iso_code

        return self._iso_code

    @property
    def lang_iso_code(self):
        iso_code = self.iso_code
        if iso_code is not None:
            if self.ISO639_3 is not None and self.ISO639_3 in iso_code:
                return self.ISO639_3
            if self.ISO639_2 is not None and self.ISO639_2 in iso_code:
                return self.ISO639_2
            if self.ISO639_1 is not None and self.ISO639_1 in iso_code:
                return self.ISO639_1

    @property
    def lcid(self):
        if self._lcid is None:
            lcid = locale_name_to_lcid(self.iso_code)
            self._lcid = lcid

        return self._lcid

    @property
    def wx_code(self):
        lcid = self.lcid
        if lcid is None:
            return

        if lcid in LCID_TO_WX:
            return LCID_TO_WX[lcid]

    def set_locale(self, code_page=False):

        def set_locale(c_page):
            try:
                return _locale.setlocale(_locale.LC_ALL, c_page)
            except (_locale.Error, TypeError):
                return False

        if code_page is False:
            return set_locale(
                '{0}_{1}.{2}'.format(
                    self.english_name,
                    self.english_locale_name,
                    self.default_ansi_codepage
                )
            )

        return set_locale(code_page)

    @property
    def ansi_code_page(self):
        code_page = self.default_ansi_codepage
        if code_page:
            code_page = int(code_page)
            if code_page in CODE_PAGES:
                return CODE_PAGES[code_page]

            return str(code_page)

    @property
    def code_page(self):
        code_page = self.default_codepage
        if code_page:
            code_page = int(code_page)
            if code_page in CODE_PAGES:
                return CODE_PAGES[code_page]

            return str(code_page)

    def set_wx_locale(self):
        if wx is not None:
            wx_code = self.wx_code
            if wx_code is None:
                return

            app = wx.GetApp()
            if app is None:
                return

            app.locale = wx.Locale(wx_code)

    def get_locale_info(self, flag):
        res = get_locale_info(self.iso_code, flag)

        if PY3:
            output = b''
            for char in list(res):
                if char == 0:
                    continue

                output += char
        else:
            output = ''

            for char in list(res):
                if char == '\x00':
                    continue

                output += char

        return output

    @property
    def label(self):
        return self.get_locale_info(LOCALE_SLOCALIZEDDISPLAYNAME)

    @property
    def english_label(self):
        return self._english_name + ' (' + self.locale.english_name + ')'

    @property
    def native_label(self):
        res = self.get_locale_info(LOCALE_SNATIVEDISPLAYNAME)
        if not res:
            res = self._native_name + u' (' + self._locale_name + u')'

        return res

    @property
    def name(self):
        return self.get_locale_info(LOCALE_SLOCALIZEDLANGUAGENAME)

    @property
    def english_name(self):
        res = self.get_locale_info(LOCALE_SENGLISHLANGUAGENAME)
        if not res:
            res = self._english_name

        return res

    @property
    def native_name(self):
        res = self.get_locale_info(LOCALE_SNATIVELANGUAGENAME)
        if not res:
            res = self._native_name

        return res

    @property
    def locale_name(self):
        return self.get_locale_info(LOCALE_SLOCALIZEDCOUNTRYNAME)

    @property
    def english_locale_name(self):
        res = self.get_locale_info(LOCALE_SENGLISHCOUNTRYNAME)
        if not res:
            res = self.locale.english_name

        return res

    @property
    def native_locale_name(self):
        res = self.get_locale_info(LOCALE_SNATIVECOUNTRYNAME)
        if not res:
            res = self._locale_name

        return res

    @property
    def international_phone_prefix(self):
        return self.get_locale_info(LOCALE_IDIALINGCODE)

    @property
    def list_separator(self):
        return self.get_locale_info(LOCALE_SLIST)

    @property
    def is_metric(self):
        res = self.get_locale_info(LOCALE_IMEASURE)

        if res == '1':
            return False
        return True

    @property
    def decimal_separator(self):
        return self.get_locale_info(LOCALE_SDECIMAL)

    @property
    def numeric_group_separator(self):
        return self.get_locale_info(LOCALE_STHOUSAND)

    @property
    def numeric_group_length(self):
        res = self.get_locale_info(LOCALE_SGROUPING)
        return list(int(itm) for itm in res.split(';'))

    @property
    def float_precision(self):
        return int(self.get_locale_info(LOCALE_IDIGITS))

    @property
    def float_leading_zeros(self):
        return int(self.get_locale_info(LOCALE_ILZERO))

    @property
    def numeric_neg_format(self):
        res = self.get_locale_info(LOCALE_INEGNUMBER)

        neg_formats = [
            '({{0}})',
            '{0}{{neg}}',
            '{{0}}{neg}'
            '{{0}} {neg}'
        ]

        neg_format = neg_formats[res]
        if '{neg}' in neg_format:
            neg_format = neg_format.format(neg=self.numeric_neg_symbol)

        return NumberFormat(
            neg_format,
            self.numeric_group_separator,
            self.numeric_group_length,
            decimal_sep=self.decimal_separator,
            precision=None
        )

    @property
    def native_digits(self):
        return self.get_locale_info(LOCALE_SNATIVEDIGITS)

    @property
    def currency_symbol(self):
        return self.get_locale_info(LOCALE_SCURRENCY)

    @property
    def currency_suffix(self):
        return self.get_locale_info(LOCALE_SINTLSYMBOL)

    @property
    def currency_decimal_separator(self):
        return self.get_locale_info(LOCALE_SMONDECIMALSEP)

    @property
    def currency_group_separator(self):
        return self.get_locale_info(LOCALE_SMONTHOUSANDSEP)

    @property
    def currency_group_length(self):
        res = self.get_locale_info(LOCALE_SMONGROUPING)
        return list(int(itm) for itm in res.split(';'))

    @property
    def currency_decimal_precision(self):
        return int(self.get_locale_info(LOCALE_ICURRDIGITS))

    @property
    def date_format_short(self):
        res = self.get_locale_info(LOCALE_SSHORTDATE)

        month_count = res.count('M')
        day_count = res.count('d')
        year_count = res.count('y')

        month_formats = [
            '',
            '%-m',
            '%m',
            '%b',
            '%B'
        ]
        day_formats = [
            '',
            '%-d'
            '%d'
            '%a'
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

        month_format = month_formats[month_count]
        day_format = day_formats[day_count]
        year_format = year_formats[year_count]

        res = res.replace('M' * month_count, month_format)
        res = res.replace('d' * day_count, day_format)
        res = res.replace('y' * year_count, year_format)
        return res

    @property
    def date_format_long(self):
        res = self.get_locale_info(LOCALE_SLONGDATE)

        month_count = res.count('M')
        day_count = res.count('d')
        year_count = res.count('y')

        month_formats = [
            '',
            '%-m',
            '%m',
            '%b',
            '%B'
        ]
        day_formats = [
            '',
            '%-d'
            '%d'
            '%a'
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

        month_format = month_formats[month_count]
        day_format = day_formats[day_count]
        year_format = year_formats[year_count]

        res = res.replace('M' * month_count, month_format)
        res = res.replace('d' * day_count, day_format)
        res = res.replace('y' * year_count, year_format)
        return res

    @property
    def time_format(self):
        res = self.get_locale_info(LOCALE_STIMEFORMAT)

        hour_count = res.count('h')
        if not hour_count:
            hour_count = res.count('H') * 3

        minute_count = res.count('m')
        second_count = res.count('s')
        suffix_count = res.count('t')

        hour_formats = [
            '',
            '%-I',
            '%I',
            '%-H',
            '',
            '',
            '%H'
        ]
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

        hour_format = hour_formats[hour_count]
        minute_format = minute_formats[minute_count]
        second_format = second_formats[second_count]
        suffix_format = suffix_formats[suffix_count]
        if hour_count < 3:
            res = res.replsce('h' * hour_count, hour_format)
        else:
            res = res.replsce('H' * int(hour_count / 3), hour_format)
        res = res.replsce('m' * minute_count, minute_format)
        res = res.replsce('s' * second_count, second_format)
        res = res.replsce('t' * suffix_count, suffix_format)

        return res

    @property
    def time_suffix_morning(self):
        return self.get_locale_info(LOCALE_SAM)

    @property
    def time_suffix_evening(self):
        return self.get_locale_info(LOCALE_SPM)

    @property
    def calendar_week_start_day(self):
        return int(self.get_locale_info(LOCALE_IFIRSTDAYOFWEEK))

    @property
    def calendar_first_wek_of_year(self):
        return int(self.get_locale_info(LOCALE_IFIRSTWEEKOFYEAR))

    def _get_week_day_long_name(self, day):
        day += self.calendar_week_start_day

        days = {
            1:  LOCALE_SDAYNAME1,
            3:  LOCALE_SDAYNAME2,
            5:  LOCALE_SDAYNAME3,
            7:  LOCALE_SDAYNAME4,
            9:  LOCALE_SDAYNAME5,
            11: LOCALE_SDAYNAME6,
            13: LOCALE_SDAYNAME7
        }

        return self.get_locale_info(days[day])

    @property
    def calendar_week_day_1_long_name(self):
        return self._get_week_day_long_name(1)

    @property
    def calendar_week_day_2_long_name(self):
        return self._get_week_day_long_name(2)

    @property
    def calendar_week_day_3_long_name(self):
        return self._get_week_day_long_name(3)

    @property
    def calendar_week_day_4_long_name(self):
        return self._get_week_day_long_name(4)

    @property
    def calendar_week_day_5_long_name(self):
        return self._get_week_day_long_name(5)

    @property
    def calendar_week_day_6_long_name(self):
        return self._get_week_day_long_name(6)

    @property
    def calendar_week_day_7_long_name(self):
        return self._get_week_day_long_name(7)

    def _get_week_day_short_name(self, day):
        day += self.calendar_week_start_day

        days = {
            1:  LOCALE_SABBREVDAYNAME1,
            3:  LOCALE_SABBREVDAYNAME2,
            5:  LOCALE_SABBREVDAYNAME3,
            7:  LOCALE_SABBREVDAYNAME4,
            9:  LOCALE_SABBREVDAYNAME5,
            11: LOCALE_SABBREVDAYNAME6,
            13: LOCALE_SABBREVDAYNAME7
        }

        return self.get_locale_info(days[day])

    @property
    def calendar_week_day_1_short_name(self):
        return self._get_week_day_short_name(1)

    @property
    def calendar_week_day_2_short_name(self):
        return self._get_week_day_short_name(2)

    @property
    def calendar_week_day_3_short_name(self):
        return self._get_week_day_short_name(3)

    @property
    def calendar_week_day_4_short_name(self):
        return self._get_week_day_short_name(4)

    @property
    def calendar_week_day_5_short_name(self):
        return self._get_week_day_short_name(5)

    @property
    def calendar_week_day_6_short_name(self):
        return self._get_week_day_short_name(6)

    @property
    def calendar_week_day_7_short_name(self):
        return self._get_week_day_short_name(7)

    def _get_week_day_shortest_name(self, day):
        day += self.calendar_week_start_day

        days = {
            1:  LOCALE_SSHORTESTDAYNAME1,
            3:  LOCALE_SSHORTESTDAYNAME2,
            5:  LOCALE_SSHORTESTDAYNAME3,
            7:  LOCALE_SSHORTESTDAYNAME4,
            9:  LOCALE_SSHORTESTDAYNAME5,
            11: LOCALE_SSHORTESTDAYNAME6,
            13: LOCALE_SSHORTESTDAYNAME7
        }

        return self.get_locale_info(days[day])

    @property
    def calendar_week_day_1_shortest_name(self):
        return self._get_week_day_shortest_name(1)

    @property
    def calendar_week_day_2_shortest_name(self):
        return self._get_week_day_shortest_name(2)

    @property
    def calendar_week_day_3_shortest_name(self):
        return self._get_week_day_shortest_name(3)

    @property
    def calendar_week_day_4_shortest_name(self):
        return self._get_week_day_shortest_name(4)

    @property
    def calendar_week_day_5_shortest_name(self):
        return self._get_week_day_shortest_name(5)

    @property
    def calendar_week_day_6_shortest_name(self):
        return self._get_week_day_shortest_name(6)

    @property
    def calendar_week_day_7_shortest_name(self):
        return self._get_week_day_shortest_name(7)

    @property
    def calendar_month_1_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME1)

    @property
    def calendar_month_2_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME2)

    @property
    def calendar_month_3_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME3)

    @property
    def calendar_month_4_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME4)

    @property
    def calendar_month_5_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME5)

    @property
    def calendar_month_6_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME6)

    @property
    def calendar_month_7_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME7)

    @property
    def calendar_month_8_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME8)

    @property
    def calendar_month_9_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME9)

    @property
    def calendar_month_10_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME10)

    @property
    def calendar_month_11_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME11)

    @property
    def calendar_month_12_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME12)

    @property
    def calendar_month_13_long_name(self):
        return self.get_locale_info(LOCALE_SMONTHNAME13)

    @property
    def calendar_month_1_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME1)

    @property
    def calendar_month_2_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME2)

    @property
    def calendar_month_3_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME3)

    @property
    def calendar_month_4_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME4)

    @property
    def calendar_month_5_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME5)

    @property
    def calendar_month_6_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME6)

    @property
    def calendar_month_7_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME7)

    @property
    def calendar_month_8_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME8)

    @property
    def calendar_month_9_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME9)

    @property
    def calendar_month_10_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME10)

    @property
    def calendar_month_11_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME11)

    @property
    def calendar_month_12_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME12)

    @property
    def calendar_month_13_short_name(self):
        return self.get_locale_info(LOCALE_SABBREVMONTHNAME13)

    @property
    def currency_pos_format(self):
        return self.get_locale_info(LOCALE_SMONTHDAY)

    @property
    def currency_neg_format(self):
        res = self.get_locale_info(LOCALE_SMONTHDAY)
        currency_formats = [
            '({0}{{0}})',
            '{1}{0}{{0}}',
            '{0}{1}{{0}}',
            '{0}{{0}}{1}',
            '({{0}}{0})',
            '{1}{{0}}{0}',
            '{{0}}{1}{0}',
            '{{0}}{0}{1}',
            '{1}{{0}} {0}',
            '{1}{0} {{0}}',
            '{{0}} {0}{1}',
            '{0} {{0}}{1}',
            '{0} {1}{{0}}',
            '{{0}}{1} {0}',
            '({0} {{0}})',
            '({{0}} {0})'
        ]

        currency_format = currency_formats[res]

        if '{1}' in currency_format:
            currency_format = currency_format.format(
                self.currency_symbol,
                self.numeric_neg_symbol
            )
        else:
            currency_format = currency_format.format(self.currency_symbol)

        return NumberFormat(
            currency_format,
            self.currency_decimal_separator,
            self.currency_group_separator,
            self.currency_group_length,
            self.currency_decimal_precision,
        )

    @property
    def numeric_pos_symbol(self):
        return self.get_locale_info(LOCALE_SPOSITIVESIGN)

    @property
    def numeric_neg_symbol(self):
        return self.get_locale_info(LOCALE_SNEGATIVESIGN)

    @property
    def currency_nglish_name(self):
        return self.get_locale_info(LOCALE_SENGCURRNAME)

    @property
    def currency_native_name(self):
        return self.get_locale_info(LOCALE_SNATIVECURRNAME)

    @property
    def time_duration_format(self):
        res = self.get_locale_info(LOCALE_SDURATION)

        hour_formats = [
            '',
            '%-I',
            '%I'
        ]
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
        hour_count = res.count('h')
        minute_count = res.count('m')
        second_count = res.count('s')

        hour_format = hour_formats[hour_count]
        minute_format = minute_formats[minute_count]
        second_format = second_formats[second_count]
        res = res.replsce('h' * hour_count, hour_format)
        res = res.replsce('m' * minute_count, minute_format)
        res = res.replsce('s' * second_count, second_format)

        if 'f' in res:
            res = res.rsplit('.', 1)[0]

        return res

    @property
    def numeric_nan(self):
        return self.get_locale_info(LOCALE_SNAN)

    @property
    def numeric_pos_infinity(self):
        return self.get_locale_info(LOCALE_SPOSINFINITY)

    @property
    def numeric_neg_infinity(self):
        return self.get_locale_info(LOCALE_SNEGINFINITY)

    @property
    def script_orientation(self):
        res = self.get_locale_info(LOCALE_IREADINGLAYOUT)

        if res == 0:
            return 'horizontal:left:right'
        elif res == 1:
            return 'horizontal:right:left'
        elif res == 2:
            return 'vertical:left:right'
        else:
            return 'vertical:right:left'

    @property
    def numeric_neg_percent_format(self):
        res = self.get_locale_info(LOCALE_INEGATIVEPERCENT)

        percent_formats = [
            u'{1}{{0}} {0}',
            u'{1}{{0}}{0}',
            u'{1}{0}{{0}}',
            u'{0}{1}{{0}}',
            u'{0}{{0}}{1}',
            u'{{0}}{1}{0}',
            u'{{0}}{0}{1}',
            u'{1}{0} {{0}}',
            u'{{0}} {0}{1}',
            u'{0} {{0}}{1}',
            u'{0} {1}{{0}}',
            u'{{0}}{1} {0}'
        ]
        percent_format = percent_formats[res]

        return percent_format.format(
            self.numeric_percent_symbol,
            self.numeric_neg_symbol
        )

    @property
    def numeric_pos_percent_format(self):
        res = self.get_locale_info(LOCALE_IPOSITIVEPERCENT)

        percent_formats = [
            u'{{0}} {0}',
            u'{{0}}{0}',
            u'{0}{{0}}',
            u'{0} {{0}}'
        ]
        percent_format = percent_formats[res]
        return percent_format.format(self.numeric_percent_symbol)

    @property
    def numeric_percent_symbol(self):
        return self.get_locale_info(LOCALE_SPERCENT)

    @property
    def date_preferred_format(self):
        res = self.get_locale_info(LOCALE_SMONTHDAY)

        month_count = res.count('M')
        day_count = res.count('d')
        year_count = res.count('y')

        month_formats = [
            '',
            '%-m',
            '%m',
            '%b',
            '%B'
        ]
        day_formats = [
            '',
            '%-d'
            '%d'
            '%a'
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

        month_format = month_formats[month_count]
        day_format = day_formats[day_count]
        year_format = year_formats[year_count]

        res = res.replace('M' * month_count, month_format)
        res = res.replace('d' * day_count, day_format)
        res = res.replace('y' * year_count, year_format)
        return res

    @property
    def time_short_format(self):
        res = self.get_locale_info(LOCALE_SSHORTTIME)
        res = res.replace('hh', '%h')
        res = res.replace('mm', '%m')
        return res

    @property
    def default_ansi_codepage(self):
        return self.get_locale_info(LOCALE_IDEFAULTANSICODEPAGE)

    @property
    def default_codepage(self):
        return self.get_locale_info(LOCALE_IDEFAULTCODEPAGE)


class Locales(object):
    def __init__(self):
        self._locales = []
        self.total_supported_countries = 0
        self.total_countries = 0
        self.total_supported_locales = 0
        self.total_locales = 0
        self._total_supported_languages = set()
        self._total_languages = set()

    @property
    def total_supported_languages(self):
        return len(self._total_supported_languages)

    @property
    def total_languages(self):
        return len(self._total_languages)

    def append(self, locale):
        for lcl in self:
            if lcl == locale:
                break
        else:
            self.total_countries += 1

            for lang in locale.languages[:]:
                self.total_locales += 1
                self._total_languages.add(lang.__class__)

                if lang.iso_code is None:
                    locale.languages.remove(lang)
                else:
                    self._total_supported_languages.add(lang.__class__)
                    self.total_supported_locales += 1

            if locale.languages:
                self.total_supported_countries += 1
                self._locales += [locale]

    def __iter__(self):
        for locale in self._locales:
            yield locale

    def __getitem__(self, item):
        for locale in self:
            if locale == item:
                return locale

        raise KeyError(item)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        for locale in self:
            if locale == item:
                return locale

        raise AttributeError(item)


locales = Locales()


class LocaleMeta(type):

    def __new__(mcs, name, bases, dct):
        locale = type.__new__(mcs, name, bases, dct)
        instance = locale()
        if instance.languages:
            locales.append(instance)
        return locale


class Locale(object):
    __metaclass__ = LocaleMeta

    _iso_code = ''
    _english_name = ''
    _flag = ''
    languages = []

    def __init__(self):
        for language in self.languages:
            language.locale = self

    def __iter__(self):
        for language in self.languages:
            yield language

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in Locale.__dict__:
            if hasattr(Locale.__dict__[item], 'fget'):
                return Locale.__dict__[item].fget(self)

        for language in self:
            if language == item:
                return language

        raise AttributeError(item)

    @property
    def english_name(self):
        return self._english_name

    def __getitem__(self, item):
        for language in self:
            if language == item:
                return language

        raise KeyError(item)

    # noinspection PyUnresolvedReferences
    def __eq__(self, other):
        if isinstance(other, Locale):
            return other.locale_iso_code == self.locale_iso_code

        if PY3:
            if isinstance(other, bytes):
                other = other.decode('utf-8')

            if isinstance(other, str):
                return other == self.locale_iso_code

        elif isinstance(other, (str, unicode)):
            return other == self.locale_iso_code

        return False

    @property
    def locale_iso_code(self):
        return self._iso_code

    @property
    def flag(self):
        if self._flag:
            return wx.Bitmap(
                os.path.abspath(
                    os.path.join(BASE_PATH, '..', 'images', self._flag)
                )
            )
        else:
            return wx.EmptyBitmapRGBA(24, 24, 0, 0, 0, 0)


class Afar(Language):
    ISO639_1 = 'aa'
    ISO639_2 = 'aar'
    _english_name = 'Afar'
    _native_name = u'Qafár af'
    _lang_id = 0x1000


class Afrikaans(Language):
    ISO639_1 = 'af'
    ISO639_2 = 'afr'
    _english_name = 'Afrikaans'
    _native_name = u'Afrikaans'
    _lang_id = 0x0036


class Aghem(Language):
    ISO639_2 = 'agq'
    _english_name = 'Aghem'
    _native_name = u'Aghem'
    _lang_id = 0x1000


class Akan(Language):
    ISO639_1 = 'ak'
    ISO639_2 = 'aka'
    _english_name = 'Akan'
    _native_name = u'Akan'
    _lang_id = 0x1000


class Albanian(Language):
    ISO639_1 = 'sq'
    ISO639_2 = 'alb'
    _english_name = 'Albanian'
    _native_name = u'Shqip'
    _lang_id = 0x001C


class SwissGerman(Language):
    ISO639_2 = 'gsw'
    _english_name = 'Swiss German'
    n_native_name = u'Schwiizerdütsch'
    _lang_id = 0x0084


class Amharic(Language):
    ISO639_1 = 'am'
    ISO639_2 = 'amh'
    _english_name = 'Amharic'
    _native_name = u'አማርኛ'
    _lang_id = 0x005E


class Arabic(Language):
    ISO639_1 = 'ar'
    ISO639_2 = 'ara'
    _english_name = 'Arabic'
    _native_name = u'العَرَبِيَّة'
    _lang_id = 0x0001


class Armenian(Language):
    ISO639_1 = 'hy'
    ISO639_2 = 'arm'
    ISO639_3 = 'hye'
    _english_name = 'Armenian'
    _native_name = u' Հայերէն'
    _lang_id = 0x002B


class Assamese(Language):
    ISO639_1 = 'as'
    ISO639_2 = 'asm'
    _english_name = 'Assamese'
    _native_name = u'অসমীয়া'
    _lang_id = 0x004D


class Asturian(Language):
    ISO639_2 = 'ast'
    _english_name = 'Asturian'
    _native_name = u'Asturianu'
    _lang_id = 0x1000


class Asu(Language):
    ISO639_2 = 'asa'
    _english_name = 'Asu'
    _native_name = u'Asu'
    _lang_id = 0x1000


class Aymara(Language):
    ISO639_1 = 'ay'
    ISO639_2 = 'aym'
    _english_name = 'Aymara'
    _native_name = u'Aymar aru'


class AzerbaijaniCyrillic(Language):
    ISO639_3 = 'az-Cyrl'
    _english_name = 'Azerbaijani'
    _native_name = u'Азәрбајҹан дили'
    _lang_id = 0x742C


class AzerbaijaniLatin(Language):
    ISO639_3 = 'az-Latn'
    _english_name = 'Azerbaijani'
    _native_name = u'Azərbaycan dili'
    _lang_id = 0x782C


class Azerbaijani(Language):
    ISO639_1 = 'az'
    ISO639_2 = 'aze'
    _english_name = 'Azerbaijani'
    _native_name = u'آذربایجان دیلی'
    _lang_id = 0x002C


class Bafia(Language):
    ISO639_2 = 'ksf'
    _english_name = 'Bafia'
    _native_name = u'Bafia'
    _lang_id = 0x1000


class Bamanankan(Language):
    ISO639_1 = 'bm'
    _english_name = 'Bamanankan'
    _native_name = u'Bamanankan'
    _lang_id = 0x1000


class BamanankanLatin(Language):
    ISO639_1 = 'bm'
    ISO639_3 = 'bm-Latn'
    _english_name = 'Bamanankan (Latin)'
    _native_name = u'Bamanankan (Latin)'
    _lang_id = 0x1000


class Basaa(Language):
    ISO639_2 = 'bas'
    _english_name = 'Basaa'
    _native_name = u'Basaa'
    _lang_id = 0x1000


class Bashkir(Language):
    ISO639_1 = 'ba'
    _english_name = 'Bashkir'
    _native_name = u' Башҡорт теле'
    _lang_id = 0x006D


class Basque(Language):
    ISO639_1 = 'eu'
    ISO639_2 = 'baq'
    _english_name = 'Basque'
    _native_name = u'euskara'
    _lang_id = 0x002D


class Bavarian(Language):
    ISO639_2 = 'bar'
    _english_name = 'Bavarian'
    _native_name = u'bairisch'


class Belarusian(Language):
    ISO639_1 = 'be'
    ISO639_2 = 'bel'
    _english_name = 'Belarusian'
    _native_name = u'Беларуская мова'
    _lang_id = 0x0023


class Bemba(Language):
    ISO639_2 = 'bem'
    _english_name = 'Bemba'
    _native_name = u'Chibemba'
    _lang_id = 0x1000


class Bena(Language):
    ISO639_2 = 'bez'
    _english_name = 'Bena'
    _native_name = u'Bena'
    _lang_id = 0x1000


class Blin(Language):
    ISO639_2 = 'byn'
    _english_name = 'Blin'
    _native_name = u'ብሊን'
    _lang_id = 0x1000


class Bodo(Language):
    ISO639_1 = 'brx'
    _english_name = 'Bodo'
    _native_name = u'Bodo'
    _lang_id = 0x1000


class Bosnian(Language):
    ISO639_1 = 'bs'
    ISO639_2 = 'bos'
    _english_name = 'Bosnian'
    _native_name = u'босански'
    _lang_id = 0x781A


class BosnianCyrillic(Language):
    ISO639_1 = 'bs'
    ISO639_2 = 'bos'
    ISO639_3 = 'bs-Cyrl'
    _english_name = 'Bosnian (Cyrillic)'
    _native_name = u'беларуская мова'
    _lang_id = 0x641A


class BosnianLatin(Language):
    ISO639_1 = 'bs'
    ISO639_2 = 'bos'
    ISO639_3 = 'bs-Latn'
    _english_name = 'Bosnian (Latin)'
    _native_name = u'bosanski'
    _lang_id = 0x681A


class Breton(Language):
    ISO639_1 = 'br'
    ISO639_2 = 'bre'
    _english_name = 'Breton'
    _native_name = u'Brezhoneg'
    _lang_id = 0x007E


class Bulgarian(Language):
    ISO639_1 = 'bg'
    ISO639_2 = 'bul'
    _english_name = 'Bulgarian'
    _native_name = u'български език'
    _lang_id = 0x0002


class Bislama(Language):
    ISO639_1 = 'bi'
    ISO639_2 = 'bis'
    _english_name = 'Bislama'
    _native_name = u'Bislama'


class Bengali(Language):
    ISO639_1 = 'bn'
    ISO639_2 = 'ben'
    _english_name = 'Bengali'
    _native_name = u'বাংলা'
    _lang_id = 0x0045


class Burmese(Language):
    ISO639_1 = 'my'
    ISO639_2 = 'bur'
    _english_name = 'Burmese'
    _native_name = u'မြန်မာစာ'
    _lang_id = 0x0055


class Catalan(Language):
    ISO639_1 = 'ca'
    ISO639_2 = 'cat'
    _english_name = 'Catalan'
    _native_name = u'català'
    _lang_id = 0x0003


class CentralAtlasTamazightLatin(Language):
    ISO639_3 = 'tzm-Latn-MA'
    _english_name = 'Central Atlas Tamazight (Latin)'
    _native_name = u'Central Atlas Tamazight (Latin)'
    _lang_id = 0x1000


class CentralKurdish(Language):
    ISO639_1 = 'ku'
    ISO639_2 = 'kur'
    _english_name = 'Central Kurdish'
    _native_name = u'Kurdî'
    _lang_id = 0x0092


class CentralKurdishArab(Language):
    ISO639_1 = 'ku'
    ISO639_2 = 'kur'
    ISO639_3 = 'ku-Arab'
    _english_name = 'Central Kurdish (Arab)'
    _native_name = u'کوردی (Arab)'
    _lang_id = 0x7c92


class Chamorro(Language):
    ISO639_1 = 'ch'
    ISO639_2 = 'cha'
    _english_name = 'Chamorro'
    native_language = u'Finu\' Chamoru'


class Chechen(Language):
    ISO639_1 = 'ce'
    ISO639_2 = 'che'
    _english_name = 'Chechen'
    _native_name = u'Нохчийн мотт'
    _lang_id = 0x1000


class Cherokee(Language):
    ISO639_2 = 'chr'
    _english_name = 'Cherokee'
    _native_name = u'ᏣᎳᎩ ᎦᏬᏂᎯᏍᏗ'
    _lang_id = 0x005C


class Chiga(Language):
    ISO639_2 = 'cgg'
    _english_name = 'Chiga'
    _native_name = u'Chiga'
    _lang_id = 0x1000


class ChineseSimplified(Language):
    ISO639_1 = 'zh'
    _english_name = 'Chinese (Simplified)'
    _native_name = u'中文'
    _lang_id = 0x7804


class ChineseSimplifiedHans(Language):
    ISO639_2 = 'chi'
    ISO639_3 = 'zh-Hans'
    _english_name = 'Chinese (Simplified)'
    _native_name = u'汉语'
    _lang_id = 0x0004


class ChineseTraditional(Language):
    ISO639_2 = 'zho'
    ISO639_3 = 'zh-Hant'
    _english_name = 'Chinese (Traditional)'
    _native_name = u'漢語'
    _lang_id = 0x7C04


class ChurchSlavic(Language):
    ISO639_1 = 'cu'
    ISO639_2 = 'chu'
    _english_name = 'Church Slavic'
    _native_name = u'Славе́нскїй ѧ҆зы́къ'
    _lang_id = 0x1000


class CongoSwahili(Language):
    ISO639_2 = 'swc'
    _english_name = 'Congo Swahili'
    _native_name = u'Congo Swahili'
    _lang_id = 0x1000


class Cornish(Language):
    ISO639_1 = 'kw'
    ISO639_2 = 'cor'
    _english_name = 'Cornish'
    _native_name = u'Kernowek'
    _lang_id = 0x1000


class Corsican(Language):
    ISO639_1 = 'co'
    ISO639_2 = 'cos'
    _english_name = 'Corsican'
    _native_name = u'Corsu'
    _lang_id = 0x0083


class CroatianLatin(Language):
    ISO639_1 = 'hr'
    ISO639_2 = 'hrv'
    _english_name = 'Croatian (Latin)'
    _native_name = u'hrvatski'
    _lang_id = 0x001A


class Croatian1(Language):
    ISO639_1 = 'bs'
    _english_name = 'Croatian (?)'
    _native_name = u'Croatian (?)'
    _lang_id = 0x001A


class Croatian2(Language):
    ISO639_1 = 'sr'
    _english_name = 'Croatian (?)'
    _native_name = u'Croatian (?)'
    _lang_id = 0x001A


class Czech(Language):
    ISO639_1 = 'cs'
    ISO639_2 = 'cze'
    _english_name = 'Czech'
    _native_name = u'čeština'
    _lang_id = 0x0005


class Danish(Language):
    ISO639_1 = 'da'
    ISO639_2 = 'dan'
    _english_name = 'Danish'
    _native_name = u'dansk'
    _lang_id = 0x0006


class Dari(Language):
    ISO639_1 = 'fa'
    ISO639_2 = 'per'
    _english_name = 'Dari'
    _native_name = u'درى'
    _lang_id = 0x008C


class Divehi(Language): # Dhivehi
    ISO639_1 = 'dv'
    ISO639_2 = 'div'
    _english_name = 'Divehi'
    _native_name = u'ދިވެހިބަސް'
    _lang_id = 0x0065


class Duala(Language):
    ISO639_2 = 'dua'
    _english_name = 'Duala'
    _native_name = u'Duala'
    _lang_id = 0x1000


class Dutch(Language):
    ISO639_1 = 'nl'
    ISO639_2 = 'dut'
    _english_name = 'Dutch'
    _native_name = u'Nederlands'
    _lang_id = 0x0013


class Dzongkha(Language):
    ISO639_1 = 'dz'
    ISO639_2 = 'dzo'
    _english_name = 'Dzongkha'
    _native_name = u'རྫོང་ཁ་'
    _lang_id = 0x1000


class Embu(Language):
    ISO639_2 = 'ebu'
    _english_name = 'Embu'
    _native_name = u'Embu'
    _lang_id = 0x1000


class English(Language):
    ISO639_1 = 'en'
    ISO639_2 = 'eng'
    _english_name = 'English'
    _native_name = u'English'
    _lang_id = 0x0009


class Esperanto(Language):
    ISO639_1 = 'eo'
    ISO639_2 = 'epo'
    _english_name = 'Esperanto'
    _native_name = u'Esperanto'
    _lang_id = 0x1000


class Estonian(Language):
    ISO639_1 = 'et'
    ISO639_2 = 'est'
    _english_name = 'Estonian'
    _native_name = u'eesti keel'
    _lang_id = 0x0025


class Ewe(Language):
    ISO639_1 = 'ee'
    ISO639_2 = 'ewe'
    _english_name = 'Ewe'
    _native_name = u'Èʋegbe'
    _lang_id = 0x1000


class Ewondo(Language):
    ISO639_2 = 'ewo'
    _english_name = 'Ewondo'
    _native_name = u'Ewondo'
    _lang_id = 0x1000


class Faroese(Language):
    ISO639_1 = 'fo'
    ISO639_2 = 'fao'
    _english_name = 'Faroese'
    _native_name = u'føroyskt'
    _lang_id = 0x0038


class Filipino(Language):
    ISO639_2 = 'fil'
    _english_name = 'Filipino'
    _native_name = u'Filipino'
    _lang_id = 0x0064


class Finnish(Language):
    ISO639_1 = 'fi'
    ISO639_2 = 'fin'
    _english_name = 'Finnish'
    _native_name = u'suomen kieli'
    _lang_id = 0x000B


class French(Language):
    ISO639_1 = 'fr'
    ISO639_2 = 'fre'
    _english_name = 'French'
    _native_name = u'français'
    _lang_id = 0x000C


class Frisian(Language):
    ISO639_1 = 'fy'
    ISO639_2 = 'fry'
    _english_name = 'Frisian'
    _native_name = u'Frysk'
    _lang_id = 0x0062


class Friulian(Language):
    ISO639_2 = 'fur'
    _english_name = 'Friulian'
    _native_name = u'Friulian'
    _lang_id = 0x1000


class Fulah(Language):
    ISO639_1 = 'ff'
    ISO639_2 = 'ful'
    _english_name = 'Fulah'
    _native_name = u'Fulfulde'
    _lang_id = 0x0067


class FulahLatin(Language):
    ISO639_3 = 'ff-Latn'
    _english_name = 'Fulah (Latin)'
    _native_name = u'Pular'
    _lang_id = 0x7C67


class Galician(Language):
    ISO639_1 = 'gl'
    ISO639_2 = 'glg'
    _english_name = 'Galician'
    _native_name = u'galego'
    _lang_id = 0x1000


class Ganda(Language):
    ISO639_1 = 'lg'
    ISO639_2 = 'lug'
    _english_name = 'Ganda'
    _native_name = u'Luganda'
    _lang_id = 0x1000


class Georgian(Language):
    ISO639_1 = 'ka'
    ISO639_2 = 'geo'
    _english_name = 'Georgian'
    _native_name = u'ქართული'
    _lang_id = 0x0037


class German(Language):
    ISO639_1 = 'de'
    ISO639_2 = 'ger'
    _english_name = 'German'
    _native_name = u'Deutsch'
    _lang_id = 0x0007


class Greek(Language):
    ISO639_1 = 'el'
    ISO639_2 = 'gre'
    _english_name = 'Greek'
    _native_name = u'Νέα Ελληνικά'
    _lang_id = 0x0008


class Guarani(Language):
    ISO639_1 = 'gn'
    ISO639_2 = 'grn'
    _english_name = 'Guarani'
    _native_name = u'Avañe\'ẽ'
    _lang_id = 0x0074


class Gujarati(Language):
    ISO639_1 = 'gu'
    ISO639_2 = 'guj'
    _english_name = 'Gujarati'
    _native_name = u'ગુજરાતી'


class Gusii(Language):
    ISO639_2 = 'guz'
    _english_name = 'Gusii'
    _native_name = u'Gusii'
    _lang_id = 0x1000


class HaitianCreole(Language):
    ISO639_1 = 'ht'
    ISO639_2 = 'hat'
    _english_name = 'Haitian Creole'
    _native_name = u'kreyòl ayisyen'


class Hausa(Language):
    ISO639_1 = 'ha'
    ISO639_2 = 'hau'
    _english_name = 'Hausa'
    _native_name = u'هَرْشَن'
    _lang_id = 0x0068


class HausaLatin(Language):
    ISO639_1 = 'ha'
    ISO639_2 = 'hau'
    ISO639_3 = 'ha-Latn'
    _english_name = 'Hausa (Latin)'
    _native_name = u'Harshen'
    _lang_id = 0x7C68


class Hawaiian(Language):
    ISO639_2 = 'haw'
    _english_name = 'Hawaiian'
    _native_name = u'ʻŌlelo Hawaiʻi'
    _lang_id = 0x0075


class Hebrew(Language):
    ISO639_1 = 'he'
    ISO639_2 = 'heb'
    _english_name = 'Hebrew'
    _native_name = u'עברית'
    _lang_id = 0x000D


class Hindi(Language):
    ISO639_1 = 'hi'
    ISO639_2 = 'hin'
    _english_name = 'Hindi'
    _native_name = u'हिन्दी'
    _lang_id = 0x0039


class HiriMotu(Language):
    ISO639_1 = 'ho'
    ISO639_2 = 'hmo'
    _english_name = 'Hiri Motu'
    _native_name = u'Hiri Motu'


class Hungarian(Language):
    ISO639_1 = 'hu'
    ISO639_2 = 'hun'
    _english_name = 'Hungarian'
    _native_name = u'magyar nyelv'
    _lang_id = 0x000E


class Icelandic(Language):
    ISO639_1 = 'is'
    ISO639_2 = 'ice'
    _english_name = 'Icelandic'
    _native_name = u'íslenska'
    _lang_id = 0x000F


class Igbo(Language):
    ISO639_1 = 'ig'
    ISO639_2 = 'ibo'
    _english_name = 'Igbo'
    _native_name = u'Asụsụ Igbo'
    _lang_id = 0x0070


class Indonesian(Language):
    ISO639_1 = 'id'
    ISO639_2 = 'ind'
    _english_name = 'Indonesian'
    natiive_name = u'bahasa Indonesia'
    _lang_id = 0x0021


class Interlingua(Language):
    ISO639_1 = 'ia'
    _english_name = 'Interlingua'
    _native_name = u'Interlingua'
    _lang_id = 0x1000


class Inuktitut(Language):
    ISO639_1 = 'iu'
    ISO639_2 = 'iku'
    _english_name = 'Inuktitut'
    _native_name = u'ᐃᓄᒃᑎᑐᑦ'
    _lang_id = 0x005D


class InuktitutLatin(Language):
    ISO639_3 = 'iu-Latn'
    _english_name = 'Inuktitut (Latin)'
    _native_name = u'Inuktitut (Latin)'
    _lang_id = 0x7C5D


class InuktitutSyllabics(Language):
    ISO639_3 = 'iu-Cans'
    _english_name = 'Inuktitut (Syllabics)'
    _native_name = u'Inuktitut (Syllabics)'
    _lang_id = 0x785D


class Irish(Language):
    ISO639_1 = 'ga'
    ISO639_2 = 'gle'
    _english_name = 'Irish'
    _native_name = u'Gaeilge'
    _lang_id = 0x003C


class Italian(Language):
    ISO639_1 = 'it'
    ISO639_2 = 'ita'
    _english_name = 'Italian'
    _native_name = u'italiano'
    _lang_id = 0x0010


class Japanese(Language):
    ISO639_1 = 'ja'
    ISO639_2 = 'jpn'
    _english_name = 'Japanese'
    _native_name = u'日本語'
    _lang_id = 0x0011


class Javanese(Language):
    ISO639_1 = 'jv'
    ISO639_2 = 'jav'
    _english_name = 'Javanese'
    _native_name = u'ꦧꦱꦗꦮ'
    _lang_id = 0x1000


class JavaneseLatin(Language):
    ISO639_3 = 'jv-Latn'
    _english_name = 'Javanese (Latin)'
    _native_name = u'Javanese (Latin)'
    _lang_id = 0x1000


class JolaFonyi(Language):
    ISO639_2 = 'dyo'
    _english_name = 'Jola-Fonyi'
    _native_name = u'Jola-Fonyi'
    _lang_id = 0x1000


class Kabuverdianu(Language):
    ISO639_2 = 'kea'
    _english_name = 'Kabuverdianu'
    _native_name = u'Kabuverdianu'
    _lang_id = 0x1000


class Kabyle(Language):
    ISO639_2 = 'kab'
    _english_name = 'Kabyle'
    _native_name = u'Tamaziɣt Taqbaylit'
    _lang_id = 0x1000


class Kako(Language):
    ISO639_2 = 'kkj'
    _english_name = 'Kako'
    _native_name = u'Kako'
    _lang_id = 0x1000


class Kalenjin(Language):
    ISO639_2 = 'kln'
    _english_name = 'Kalenjin'
    _native_name = u'Kalenjin'
    _lang_id = 0x1000


class Kamba(Language):
    ISO639_2 = 'kam'
    _english_name = 'Kamba'
    _native_name = u'Kamba'
    _lang_id = 0x1000


class Kannada(Language):
    ISO639_1 = 'kn'
    ISO639_2 = 'kan'
    _english_name = 'Kannada'
    _native_name = u'ಕನ್ನಡ'
    _lang_id = 0x004B


class Kashmiri(Language):
    ISO639_1 = 'ks'
    ISO639_2 = 'kas'
    _english_name = 'Kashmiri'
    _native_name = u'कॉशुर'
    _lang_id = 0x0060


class KashmiriArab(Language):
    ISO639_1 = 'ks'
    ISO639_2 = 'kas'
    ISO639_3 = 'ks-Arab'
    _english_name = 'Kashmiri (Arab)'
    _native_name = u'كأشُر'
    _lang_id = 0x0460


class Kazakh(Language):
    ISO639_1 = 'kk'
    ISO639_2 = 'kaz'
    _english_name = 'Kazakh'
    _native_name = u'қазақ тілі'
    _lang_id = 0x003F


class Khmer(Language):
    ISO639_1 = 'km'
    ISO639_2 = 'khm'
    _english_name = 'Khmer'
    _native_name = u'ភាសាខ្មែរ'
    _lang_id = 0x0053


class Kiche(Language):
    ISO639_2 = 'quc'
    ISO639_3 = 'quc-Latn'
    _english_name = 'K\'iche'
    _native_name = u'Qatzijob\'al'
    _lang_id = 0x0086


class Kikuyu(Language):
    ISO639_1 = 'ki'
    ISO639_2 = 'kik'
    _english_name = 'Kikuyu'
    _native_name = u'Gĩkũyũ'
    _lang_id = 0x1000


class Kinyarwanda(Language):
    ISO639_1 = 'rw'
    ISO639_2 = 'kin'
    _english_name = 'Kinyarwanda'
    _native_name = u'Kinyarwanda'
    _lang_id = 0x0087


class Konkani(Language):
    ISO639_2 = 'kok'
    _english_name = 'Konkani'
    _native_name = u'कोंकणी'
    _lang_id = 0x0057


class Kalaallisut(Language):
    ISO639_1 = 'kl'
    ISO639_2 = 'kal'
    _english_name = 'Kalaallisut'
    _native_name = u'Kalaallisut'
    _lang_id = 0x006F


class KaraKalpak(Language):
    ISO639_2 = 'kaa'
    _english_name = 'Karakalpak'
    _native_name = u'Қарақалпақ тили'


class Korean(Language):
    ISO639_1 = 'ko'
    ISO639_2 = 'kor'
    _english_name = 'Korean'
    _native_name = u'한국어'
    _lang_id = 0x0012


class KoyraChiini(Language):
    ISO639_2 = 'khq'
    _english_name = 'Koyra Chiini'
    _native_name = u'Koyra Chiini'
    _lang_id = 0x1000


class KoyraboroSenni(Language):
    ISO639_2 = 'ses'
    _english_name = 'Koyraboro Senni'
    _native_name = u'Koyraboro Senni'
    _lang_id = 0x1000


class Kurdish(Language):
    ISO639_1 = 'ku'
    ISO639_2 = 'kur'
    _english_name = 'Kurdish'
    _native_name = u'کوردی'


class Kwasio(Language):
    ISO639_2 = 'nmg'
    _english_name = 'Kwasio'
    _native_name = u'Kwasio'
    _lang_id = 0x1000


class Kyrgyz(Language):
    ISO639_1 = 'ky'
    ISO639_2 = 'kir'
    _english_name = 'Kyrgyz'
    _native_name = u'кыргыз тили'
    _lang_id = 0x0040


class Lakota(Language):
    ISO639_2 = 'lkt'
    _english_name = 'Lakota'
    _native_name = u'Lakota'
    _lang_id = 0x1000


class Langi(Language):
    ISO639_2 = 'lag'
    _english_name = 'Langi'
    _native_name = u'Langi'
    _lang_id = 0x1000


class Lao(Language):
    ISO639_1 = 'lo'
    ISO639_2 = 'lao'
    _english_name = 'Lao'
    _native_name = u'ພາສາລາວ'
    _lang_id = 0x0054


class Latvian(Language):
    ISO639_1 = 'lv'
    ISO639_2 = 'lav'
    _english_name = 'Latvian'
    _native_name = u'Latviešu valoda'
    _lang_id = 0x0026


class Lingala(Language):
    ISO639_1 = 'ln'
    ISO639_2 = 'lin'
    _english_name = 'Lingala'
    _native_name = u'Lingala'
    _lang_id = 0x1000


class Lithuanian(Language):
    ISO639_1 = 'lt'
    ISO639_2 = 'lit'
    _english_name = 'Lithuanian'
    _native_name = u'lietuvių kalba'
    _lang_id = 0x0027


class LowGerman(Language):
    ISO639_2 = 'nds'
    _english_name = 'Low German'
    _native_name = u'Plattdütsch'
    _lang_id = 0x1000


class LowerSorbian(Language):
    ISO639_2 = 'dsb'
    _english_name = 'Lower Sorbian'
    _native_name = u'Dolnoserbšćina'
    _lang_id = 0x7C2E


class LubaKatanga(Language):
    ISO639_1 = 'lu'
    ISO639_2 = 'lub'
    _english_name = 'Luba-Katanga'
    _native_name = u'Kiluba'
    _lang_id = 0x1000


class Luo(Language):
    ISO639_2 = 'luo'
    _english_name = 'Luo'
    _native_name = u'Dholuo'
    _lang_id = 0x1000


class Luxembourgish(Language):
    ISO639_1 = 'lb'
    ISO639_2 = 'ltz'
    _english_name = 'Luxembourgish'
    _native_name = u'Lëtzebuergesch'
    _lang_id = 0x006E


class Luyia(Language):
    ISO639_2 = 'luy'
    _english_name = 'Luyia'
    _native_name = u'Luyia'
    _lang_id = 0x1000


class Macedonian(Language):
    ISO639_1 = 'mk'
    ISO639_2 = 'mac'
    _english_name = 'Macedonian'
    _native_name = u'македонски јазик'
    _lang_id = 0x002F


class Machame(Language):
    ISO639_2 = 'jmc'
    _english_name = 'Machame'
    _native_name = u'Machame'
    _lang_id = 0x1000


class MakhuwaMeetto(Language):
    ISO639_2 = 'mgh'
    _english_name = 'Makhuwa-Meetto'
    _native_name = u'Makhuwa-Meetto'
    _lang_id = 0x1000


class Makonde(Language):
    ISO639_2 = 'kde'
    _english_name = 'Makonde'
    _native_name = u'Makonde'
    _lang_id = 0x1000


class Malagasy(Language):
    ISO639_1 = 'mg'
    ISO639_2 = 'mlg'
    _english_name = 'Malagasy'
    _native_name = u'Malagasy'
    _lang_id = 0x1000


class Malay(Language):
    ISO639_1 = 'ms'
    ISO639_2 = 'may'
    _english_name = 'Malay'
    _native_name = u'Bahasa Melayu'
    _lang_id = 0x003E


class Malayalam(Language):
    ISO639_1 = 'ml'
    ISO639_2 = 'mal'
    _english_name = 'Malayalam'
    _native_name = u'മലയാളം'
    _lang_id = 0x004C


class Maltese(Language):
    ISO639_1 = 'mt'
    ISO639_2 = 'mlt'
    _english_name = 'Maltese'
    _native_name = u'Malti'
    _lang_id = 0x003A


class Manx(Language):
    ISO639_1 = 'gv'
    _english_name = 'Manx'
    _native_name = u'Gaelg'
    _lang_id = 0x1000


class Maori(Language):
    ISO639_1 = 'mi'
    ISO639_2 = 'mao'
    _english_name = 'Maori'
    _native_name = u'Te Reo Māori'
    _lang_id = 0x0081


class Marathi(Language):
    ISO639_1 = 'mr'
    ISO639_2 = 'mar'
    _english_name = 'Marathi'
    _native_name = u'मराठी'
    _lang_id = 0x004E


class Mapudungun(Language):
    ISO639_2 = 'arn'
    _english_name = 'Mapudungun'
    _native_name = u'Mapudungun'
    _lang_id = 0x007A


class Masai(Language):
    ISO639_2 = 'mas'
    _english_name = 'Masai'
    _native_name = u'ɔl'
    _lang_id = 0x1000


class Mazanderani(Language):
    ISO639_2 = 'mzn'
    _english_name = 'Mazanderani'
    _native_name = u'Mazanderani'
    _lang_id = 0x1000


class Meru(Language):
    ISO639_1 = 'ml'
    ISO639_2 = 'mer'
    _english_name = 'Meru'
    _native_name = u'Meru'
    _lang_id = 0x1000


class Meta(Language):
    ISO639_2 = 'mgo'
    _english_name = 'Meta\''
    _native_name = u'Meta\''
    _lang_id = 0x1000


class Mohawk(Language):
    ISO639_2 = 'moh'
    _english_name = 'Mohawk'
    _native_name = u'Kanien’kéha'
    _lang_id = 0x007C


class Mongolian(Language):
    ISO639_1 = 'mn'
    ISO639_2 = 'mon'
    _english_name = 'Mongolian'
    _native_name = u'ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ'
    _lang_id = 0x0050


class MongolianCyrillic(Language):
    ISO639_1 = 'mn'
    ISO639_2 = 'mon'
    ISO639_3 = 'mn-Cryl'
    _english_name = 'Mongolian (Cyrillic)'
    _native_name = u'монгол хэл'
    _lang_id = 0x7850


class MongolianTraditional(Language):
    ISO639_1 = 'mn'
    ISO639_2 = 'mon'
    ISO639_3 = 'mn-Mong'
    _english_name = 'Mongolian (Traditional)'
    _native_name = u'ᠮᠣᠩᠭᠣᠯ ᠬᠡᠯᠡ'
    _lang_id = 0x7C50


class Morisyen(Language):
    ISO639_2 = 'mfe'
    _english_name = 'Morisyen'
    _native_name = u'Kreol morisien'
    _lang_id = 0x1000


class Marshallese(Language):
    ISO639_1 = 'mh'
    ISO639_2 = 'mah'
    _english_name = 'Marshallese'
    _native_name = u'Kajin M̧ajeļ'


class Mundang(Language):
    ISO639_2 = 'mua'
    _english_name = 'Mundang'
    _native_name = u'Mundang'
    _lang_id = 0x1000


class Nauru(Language):
    ISO639_1 = 'na'
    ISO639_2 = 'nau'
    _english_name = 'Nauru'
    _native_name = u'dorerin Naoero'


class Nko(Language):
    ISO639_2 = 'nqo'
    _english_name = 'N\'ko'
    _native_name = u'N\'ko'
    _lang_id = 0x1000


class Nama(Language):
    ISO639_2 = 'naq'
    _english_name = 'Nama'
    _native_name = u'Nama'
    _lang_id = 0x1000


class Nepali(Language):
    ISO639_1 = 'ne'
    ISO639_2 = 'nep'
    _english_name = 'Nepali'
    _native_name = u'नेपाली भाषा'
    _lang_id = 0x0061


class Ngiemboon(Language):
    ISO639_2 = 'nnh'
    _english_name = 'Ngiemboon'
    _native_name = u'Ngiemboon'
    _lang_id = 0x1000


class Ngomba(Language):
    ISO639_2 = 'jgo'
    _english_name = 'Ngomba'
    _native_name = u'Ngomba'
    _lang_id = 0x1000


class NorthernLuri(Language):
    ISO639_2 = 'irc'
    _english_name = 'Northern Luri'
    _native_name = u'Northern Luri'
    _lang_id = 0x1000


class NorthNdebele(Language):
    ISO639_1 = 'nd'
    ISO639_2 = 'nde'
    _english_name = 'North Ndebele'
    _native_name = u'saseNyakatho'
    _lang_id = 0x1000


class NorthFrisian(Language):
    ISO639_2 = 'frr'
    _english_name = 'North Frisian'
    _native_name = u'Frasch'


class Norwegian(Language):
    ISO639_1 = 'no'
    ISO639_2 = 'nor'
    _english_name = 'Norwegian'
    _native_name = u'norsk'
    _lang_id = 0x0014


class NorwegianNynorsk(Language):
    ISO639_1 = 'nn'
    ISO639_2 = 'nno'
    _english_name = 'Norwegian (Nynorsk)'
    _native_name = u'nynorsk'
    _lang_iid = 0x7814


class NorwegianBokmal(Language):
    ISO639_1 = 'nb'
    ISO639_2 = 'nob'
    _english_name = 'Norwegian (Bokmal)'
    _native_name = u'bokmål'
    _lang_id = 0x7C14


class Niuean(Language):
    ISO639_2 = 'niu'
    _english_name = 'Niuean'
    _native_name = u'ko e vagahau Niuē'


class Nuer(Language):
    ISO639_2 = 'nus'
    _english_name = 'Nuer'
    _native_name = u'Nuer'
    _lang_id = 0x1000


class Nyanja(Language):
    ISO639_1 = 'ny'
    ISO639_2 = 'nya'
    _english_name = 'Nyanja'
    _native_name = u'chiCheŵa'


class Nyankole(Language):
    ISO639_2 = 'nyn'
    _english_name = 'Nyankole'
    _native_name = u'Nyankole'
    _lang_id = 0x1000


class Occitan(Language):
    ISO639_1 = 'oc'
    ISO639_2 = 'oci'
    _english_name = 'Occitan'
    _native_name = u'lenga d\'òc'
    _lang_id = 0x0082


class Oriya(Language):
    ISO639_1 = 'or'
    ISO639_2 = 'ori'
    _english_name = 'Oriya'
    _native_name = u'ଓଡ଼ିଆ'
    _lang_id = 0x0048


class Oromo(Language):
    ISO639_1 = 'om'
    ISO639_2 = 'orm'
    _english_name = 'Oromo'
    _native_name = u'Afaan Oromoo'
    _lang_id = 0x0072


class Ossetian(Language):
    ISO639_1 = 'os'
    ISO639_2 = 'oss'
    _english_name = 'Ossetian'
    _native_name = u'Ирон æвзаг'
    _lang_id = 0x1000


class Papiamento(Language):
    ISO639_2 = 'pap'
    _english_name = 'Papiamento'
    _native_name = u'Papiamentu'


class Palauan(Language):
    ISO639_2 = 'pau'
    _english_name = 'Palauan'
    _native_name = u'a tekoi er a Belau'


class Pashto(Language):
    ISO639_1 = 'ps'
    ISO639_2 = 'pus'
    _english_name = 'Pashto'
    _native_name = u'پښتو'
    _lang_id = 0x0063


class Persian(Language):
    ISO639_1 = 'fa'
    ISO639_2 = 'fas'
    _english_name = 'Persian'
    _native_name = u'فارسی'
    _lang_id = 0x0029


class PitcairnNorfolk(Language):
    ISO639_2 = 'pih'
    _english_name = 'Pitcairn-Norfolk'
    _native_name = u'Norfuk'


class Polish(Language):
    ISO639_1 = 'pl'
    ISO639_2 = 'pol'
    _english_name = 'Polish'
    _native_name = u'Język polski'
    _lang_id = 0x0015


class Portuguese(Language):
    ISO639_1 = 'pt'
    ISO639_2 = 'por'
    _english_name = 'Portuguese'
    _native_name = u'português'
    _lang_id = 0x0016


class Prussian(Language):
    ISO639_3 = 'prg-001'
    _english_name = 'Prussian'
    _native_name = u'Prussian'
    _lang_id = 0x1000


class Punjabi(Language):
    ISO639_1 = 'pa'
    ISO639_2 = 'pan'
    _english_name = 'Punjabi'
    _native_name = u'ਪੰਜਾਬੀ'
    _lang_id = 0x0046


class PunjabiArabic(Language):
    ISO639_1 = 'pa'
    ISO639_2 = 'pan'
    _english_name = 'Punjabi (Arabic)'
    _native_name = u'پنجابی'
    _lang_id = 0x7C46


class Quechua(Language):
    ISO639_1 = 'qu'
    ISO639_2 = 'que'
    _english_name = 'Quechua'
    _native_name = u'Runa simi'
    lang_id = 0x006B


class Ripuarian(Language):
    ISO639_2 = 'ksh'
    _english_name = 'Ripuarian'
    _native_name = u'Ripuarian'
    lang_id = 0x1000


class Rarotongan(Language):
    ISO639_2 = 'rar'
    _english_name = 'Rarotongan'
    _native_name = u'Māori Kūki \'Āirani'


class Romani(Language):
    ISO639_2 = 'rom'
    _english_name = 'Romani'
    _native_name = u'romani čhib'


class Romanian(Language):
    ISO639_1 = 'ro'
    ISO639_2 = 'rum'
    _english_name = 'Romanian'
    _native_name = u'limba română'
    _lang_id = 0x0018


class Romansh(Language):
    ISO639_1 = 'rm'
    ISO639_2 = 'roh'
    _english_name = 'Romansh'
    _native_name = u'Rumàntsch'
    _lang_id = 0x0017


class Rombo(Language):
    ISO639_2 = 'rof'
    _english_name = 'Rombo'
    _native_name = u'Rombo'
    _lang_id = 0x1000


class Rundi(Language):
    ISO639_1 = 'rn'
    ISO639_2 = 'run'
    _english_name = 'Rundi'
    _native_name = u'Ikirundi'
    _lang_id = 0x1000


class Russian(Language):
    ISO639_1 = 'ru'
    ISO639_2 = 'rus'
    _english_name = 'Russian'
    _native_name = u'русский язык'
    _lang_id = 0x0019


class Rwa(Language):
    ISO639_2 = 'rwk'
    _english_name = 'Rwa'
    _native_name = u'Rwa'
    _lang_id = 0x1000


class Saho(Language):
    ISO639_2 = 'ssy'
    _english_name = 'Saho'
    _native_name = u'Saho'
    _lang_id = 0x1000


class Yakut(Language):
    ISO639_2 = 'sah'
    _english_name = 'Yakut'
    _native_name = u'Сахалыы'
    _lang_id = 0x0085


class Samburu(Language):
    ISO639_2 = 'saq'
    _english_name = 'Samburu'
    _native_name = u'Samburu'
    _lang_id = 0x1000


class SamiInari(Language):
    ISO639_2 = 'smn'
    _english_name = 'Inari Sami'
    _native_name = u'anarâškielâ'
    _lang_id = 0x703B


class SamiLule(Language):
    ISO639_2 = 'smj'
    _english_name = 'Lule Sami'
    _native_name = u'julevsámegiella'
    _lang_id = 0x7C3B


class SamiNorthern(Language):
    ISO639_1 = 'se'
    ISO639_2 = 'sme'
    _english_name = 'Northern Sami'
    _native_name = u'davvisámegiella'
    _lang_id = 0x003B


class SamiSkolt(Language):
    ISO639_2 = 'sms'
    _english_name = 'Skolt Sami'
    _native_name = u'sääʹmǩiõll'
    _lang_id = 0x743B


class SamiSouthern(Language):
    ISO639_2 = 'sma'
    _english_name = 'Southern Sami'
    _native_name = u'Åarjelsaemien gïele'
    _lang_id = 0x783B


class Samoan(Language):
    ISO639_1 = 'sm'
    ISO639_2 = 'smo'
    _english_name = 'Samoan'
    _native_name = u'Gagana faʻa Sāmoa'


class Sango(Language):
    ISO639_1 = 'sg'
    ISO639_2 = 'sag'
    _english_name = 'Sango'
    _native_name = u'yângâ tî sängö'
    _lang_id = 0x1000


class Sangu(Language):
    ISO639_2 = 'sbp'
    _english_name = 'Sangu'
    _native_name = u'Sangu'
    _lang_id = 0x1000


class Sanskrit(Language):
    ISO639_1 = 'sa'
    ISO639_2 = 'san'
    _english_name = 'Sanskrit'
    _native_name = u'संस्कृतम्'
    _lang_id = 0x004F


class SaterlandFrisian(Language):
    ISO639_2 = 'frs'
    _english_name = 'Saterland Frisian'
    _native_name = u'Seeltersk'


class ScottishGaelic(Language):
    ISO639_1 = 'gd'
    ISO639_2 = 'gla'
    _english_name = 'Scottish Gaelic'
    _native_name = u'Gàidhlig'
    _lang_id = 0x0091


class Sena(Language):
    ISO639_2 = 'seh'
    _english_name = 'Sena'
    _native_name = u'Sena'
    _lang_id = 0x1000


class Serbian(Language):
    ISO639_1 = 'sr'
    ISO639_2 = 'srp'
    _english_name = 'Serbian'
    _native_name = u'Serbian'
    _lang_id = 0x7C1A


class SerbianCyrillic(Language):
    ISO639_1 = 'sr'
    ISO639_2 = 'srp'
    ISO639_3 = 'sr-Cryl'
    _english_name = 'Serbian (Cyrillic)'
    _native_name = u'српски'
    _lang_id = 0x6C1A


class SerbianLatin(Language):
    ISO639_1 = 'sr'
    ISO639_2 = 'srp'
    ISO639_3 = 'sr-Latn'
    _english_name = 'Serbian (Latin)'
    _native_name = u'srpski'
    _lang_id = 0x701A


class Tswana(Language):
    ISO639_1 = 'tn'
    ISO639_2 = 'tsn'
    _english_name = 'Tswana'
    _native_name = u'Setswana'
    _lang_id = 0x0032


class SeychelloisCreole(Language):
    ISO639_2 = 'crs'
    _english_name = 'Seychellois Creole'
    _native_name = u'créole seychellois'


class Shambala(Language):
    ISO639_2 = 'ksb'
    _english_name = 'Shambala'
    _native_name = u'Shambala'
    _lang_id = 0x1000


class Shona(Language):
    ISO639_1 = 'sn'
    ISO639_2 = 'sna'
    _english_name = 'Shona'
    _native_name = u'chiShona'
    _lang_id = 0x1000


class Sindhi(Language):
    ISO639_1 = 'sd'
    _english_name = 'Sindhi'
    _native_name = u'सिन्धी'
    _lang_id = 0x0059


class SindhiArab(Language):
    ISO639_3 = 'sd-Arab'
    _english_name = 'Sindhi (Arab)'
    _native_name = u'سنڌي'
    _lang_id = 0x7C59


class Sinhala(Language):
    ISO639_1 = 'si'
    ISO639_2 = 'sin'
    _english_name = 'Sinhala'
    _native_name = u'සිංහල'
    _lang_id = 0x005B


class Slovak(Language):
    ISO639_1 = 'sk'
    ISO639_2 = 'slo'
    _english_name = 'Slovak'
    _native_name = u'slovenský jazyk'
    _lang_id = 0x001B


class Slovenian(Language):
    ISO639_1 = 'sl'
    ISO639_2 = 'slv'
    _english_name = 'Slovenian'
    _native_name = u'slovenščina'
    _lang_id = 0x0024


class Soga(Language):
    ISO639_2 = 'xog'
    _english_name = 'Soga'
    _native_name = u'Soga'
    _lang_id = 0x1000


class Somali(Language):
    ISO639_1 = 'so'
    ISO639_2 = 'som'
    _english_name = 'Somali'
    _native_name = u'af Soomaali'
    _lang_id = 0x0077


class Sotho(Language):
    ISO639_1 = 'st'
    ISO639_2 = 'sot'
    _english_name = 'Sotho'
    _native_name = u'Sesotho'
    _lang_id = 0x0030


class SothoNorthern(Language):
    ISO639_2 = 'nso'
    _english_name = 'Northern Sotho'
    _native_name = u'Sesotho sa Leboa'
    _lang_id = 0x006C


class SothoSouthern(Language):
    ISO639_1 = 'st'
    ISO639_2 = 'sot'
    _english_name = 'Southern Sotho'
    _native_name = u'Sesotho [southern]'
    _lang_id = 0x1000


class SouthNdebele(Language):
    ISO639_1 = 'nr'
    _english_name = 'South Ndebele'
    _native_name = u'isiNdebele seSewula'
    _lang_id = 0x1000


class Spanish(Language):
    ISO639_1 = 'es'
    ISO639_2 = 'spa'
    _english_name = 'Spanish'
    _native_name = u'Español'
    _lang_id = 0x000A


class StandardMoroccanTamazight(Language):
    ISO639_2 = 'zgh'
    _english_name = 'Standard Moroccan Tamazight'
    _native_name = u'ⵜⴰⵎⴰⵣⵉⵖⵜ ⵜⴰⵏⴰⵡⴰⵢⵜ'
    _lang_id = 0x1000


class Swati(Language):
    ISO639_1 = 'ss'
    ISO639_2 = 'ssw'
    _english_name = 'Swati'
    _native_name = u'siSwati'
    _lang_id = 0x1000


class Swedish(Language):
    ISO639_1 = 'sv'
    ISO639_2 = 'swe'
    _english_name = 'Swedish'
    _native_name = u'svenska'
    _lang_id = 0x001D


class Syriac(Language):
    ISO639_2 = 'syr'
    _english_name = 'Syriac'
    _native_name = u'ܠܫܢܐ ܣܘܪܝܝܐ'
    _lang_id = 0x005A


class Swahili(Language):
    ISO639_1 = 'sw'
    ISO639_2 = 'swa'
    _english_name = 'Swahili'
    _native_name = u'Kiswahili'
    _lang_id = 0x0041


class Tachelhit(Language):
    ISO639_2 = 'shi'
    _english_name = 'Tachelhit'
    _native_name = u'Tachelhit'
    _lang_id = 0x1000


class TachelhitLatin(Language):
    ISO639_3 = 'shi-Latn'
    _english_name = 'Tachelhit (Latin)'
    _native_name = u'Tachelhit (Latin)'
    _lang_id = 0x1000


class Tagalog(Language):
    ISO639_1 = 'tl'
    ISO639_2 = 'tgl'
    _english_name = 'Tagalog'
    _native_name = u'Wikang Tagalog'


class Taita(Language):
    ISO639_2 = 'dav'
    _english_name = 'Taita'
    _native_name = u'Taita'
    _lang_id = 0x1000


class Tajik(Language):
    ISO639_1 = 'tg'
    ISO639_2 = 'tgk'
    _english_name = 'Tajik'
    _native_name = u'tojikī'
    _lang_id = 0x0028


class TajikCyrillic(Language):
    ISO639_3 = 'tg-Cyrl'
    _english_name = 'Tajik (Cyrillic)'
    _native_name = u'тоҷикӣ'
    _lang_id = 0x7C28


class Tamazight(Language):
    ISO639_2 = 'tzm'
    _english_name = 'Tamazight'
    _native_name = u'Tamazight'
    _lang_id = 0x005F


class TamazightLatin(Language):
    ISO639_3 = 'tzm-Latn'
    _english_name = 'Tamazight (Latin)'
    _native_name = u'Tamazight'
    _lang_id = 0x7C5F


class Tamil(Language):
    ISO639_1 = 'ta'
    ISO639_2 = 'tam'
    _english_name = 'Tamil'
    _native_name = u'தமிழ்'
    _lang_id = 0x0049


class Tasawaq(Language):
    ISO639_2 = 'twq'
    _english_name = 'Tasawaq'
    _native_name = u'Tasawaq'
    _lang_id = 0x1000


class Tatar(Language):
    ISO639_1 = 'tt'
    ISO639_2 = 'tat'
    _english_name = 'Tatar'
    _native_name = u'татар теле'
    _lang_id = 0x0044


class Telugu(Language):
    ISO639_1 = 'te'
    ISO639_2 = 'tel'
    _english_name = 'Telugu'
    _native_name = u'తెలుగు'
    _lang_id = 0x004A


class Teso(Language):
    ISO639_2 = 'teo'
    _english_name = 'Teso'
    _native_name = u'Teso'
    _lang_id = 0x1000


class Tetum(Language):
    ISO639_2 = 'tet'
    _english_name = 'Tetum'
    _native_name = u'Lia-Tetun'


class Thai(Language):
    ISO639_1 = 'th'
    ISO639_2 = 'tha'
    _english_name = 'Thai'
    _native_name = u'ภาษาไทย'
    _lang_id = 0x001E


class Tibetan(Language):
    ISO639_1 = 'bo'
    _english_name = 'Tibetan'
    _native_name = u'ལྷ་སའི་སྐད་'
    _lang_id = 0x0051


class Tigre(Language):
    ISO639_2 = 'tig'
    _english_name = 'Tigre'
    _native_name = u'ትግራይት'
    _lang_id = 0x1000


class Tigrinya(Language):
    ISO639_1 = 'ti'
    ISO639_2 = 'tir'
    _english_name = 'Tigrinya'
    _native_name = u'ትግርኛ'
    _lang_id = 0x0073


class Tobian(Language):
    ISO639_3 = 'tox'
    _english_name = 'Tobian'
    _native_name = u'ramarih Hatohobei'


class Tokelauan(Language):
    ISO639_2 = 'tkl'
    _english_name = 'Tokelauan'
    _native_name = u'Fakatokelau'


class TokPisin(Language):
    ISO639_2 = 'tpi'
    _english_name = 'Tok Pisin'
    _native_name = u'Tok Pisin'


class Tongan(Language):
    ISO639_1 = 'to'
    _english_name = 'Tongan'
    _native_name = u'lea faka-Tonga'
    _lang_id = 0x1000


class Tsonga(Language):
    ISO639_1 = 'ts'
    ISO639_2 = 'tso'
    _english_name = 'Tsonga'
    _native_name = u'Xitsonga'
    _lang_id = 0x0031


class Turkish(Language):
    ISO639_1 = 'tr'
    ISO639_2 = 'tur'
    _english_name = 'Turkish'
    _native_name = u'Türkçe'
    _lang_id = 0x001F


class Turkmen(Language):
    ISO639_1 = 'tk'
    ISO639_2 = 'tuk'
    _english_name = 'Turkmen'
    _native_name = u'Türkmençe'
    _lang_id = 0x0042


class Ukrainian(Language):
    ISO639_1 = 'uk'
    ISO639_2 = 'ukr'
    _english_name = 'Ukrainian'
    _native_name = u'українська мова'
    _lang_id = 0x0022


class UpperSorbian(Language):
    ISO639_2 = 'hsb'
    _english_name = 'Upper Sorbian'
    _native_name = u'hornjoserbšćina'
    _lang_id = 0x002E


class Urdu(Language):
    ISO639_1 = 'ur'
    ISO639_2 = 'urd'
    _english_name = 'Urdu'
    _native_name = u'اُردُو'
    _lang_id = 0x0020


class Uyghur(Language):
    ISO639_1 = 'ug'
    ISO639_2 = 'uig'
    _english_name = 'Uyghur'
    _native_name = u'ئۇيغۇرچە'
    _lang_id = 0x0080


class UzbekArab(Language):
    ISO639_1 = 'uz'
    ISO639_2 = 'uzb'
    ISO639_3 = 'uzb-Arab'
    _english_name = 'Uzbek (Arab)'
    _native_name = u'ئوبېک تیلی'
    _lang_id = 0x1000


class UzbekCyrillic(Language):
    ISO639_1 = 'uz'
    ISO639_2 = 'uzb'
    ISO639_3 = 'uzb-Cyrl'
    _english_name = 'Uzbek (Cyrillic)'
    _native_name = u'ўзбекча'
    _lang_id = 0x7843


class UzbekLatin(Language):
    ISO639_1 = 'uz'
    ISO639_2 = 'uzb'
    ISO639_3 = 'uzb-Latn'
    _english_name = 'Uzbek (Latin)'
    _native_name = u'O\'zbekcha'
    _lang_id = 0x0043


class Vai(Language):
    ISO639_2 = 'vai'
    _english_name = 'Vai'
    _native_name = u'ꕙꔤ'
    _lang_id = 0x1000


class VaiLatin(Language):
    ISO639_3 = 'vai-Latn'
    _english_name = 'Vai (Latin)'
    _native_name = u'Vai (Latin)'
    _lang_id = 0x1000


class Valencian(Language):
    ISO639_1 = 'ca'
    _english_name = 'Valencian'
    _native_name = u'Valencian'
    _lang_id = 0x0803


class Venda(Language):
    ISO639_1 = 've'
    ISO639_2 = 'ven'
    _english_name = 'Venda'
    _native_name = u'Tshivenḓa'
    _lang_id = 0x0033


class Vietnamese(Language):
    ISO639_1 = 'vi'
    ISO639_2 = 'vie'
    _english_name = 'Vietnamese'
    _native_name = u'Tiếng Việt'
    _lang_id = 0x002A


class Volapuk(Language):
    ISO639_1 = 'vo'
    ISO639_2 = 'vol'
    _english_name = 'Volapuk'
    _native_name = u'Volapük'
    _lang_id = 0x1000


class Vunjo(Language):
    ISO639_2 = 'vun'
    _english_name = 'Vunjo'
    _native_name = u'Vunjo'
    _lang_id = 0x1000


class Walser(Language):
    ISO639_2 = 'wae'
    _english_name = 'Walser'
    _native_name = u'Walser'
    _lang_id = 0x1000


class Welsh(Language):
    ISO639_1 = 'cy'
    ISO639_2 = 'wel'
    _english_name = 'Welsh'
    _native_name = u'y Gymraeg'
    _lang_id = 0x0052


class Walamo(Language):
    ISO639_2 = 'wal'
    _english_name = 'Walamo'
    _native_name = u'Walamo'
    _lang_id = 0x1000


class Wolof(Language):
    ISO639_1 = 'wo'
    ISO639_2 = 'wol'
    _english_name = 'Wolof'
    _native_name = u'Wolof'
    _lang_id = 0x0088


class Xhosa(Language):
    ISO639_1 = 'xh'
    ISO639_2 = 'xho'
    _english_name = 'Xhosa'
    _native_name = u'isiXhosa'
    _lang_id = 0x0034


class Yangben(Language):
    ISO639_2 = 'yav'
    _english_name = 'Yangben'
    _native_name = u'Yangben'
    _lang_id = 0x1000


class SichuanYi(Language):
    ISO639_1 = 'ii'
    ISO639_2 = 'iii'
    _english_name = 'Sichuan Yi'
    _native_name = u'ꆈꌠꉙ'
    _lang_id = 0x0078


class Yoruba(Language):
    ISO639_1 = 'yo'
    ISO639_2 = 'yor'
    _english_name = 'Yoruba'
    _native_name = u'èdè Yorùbá'
    _lang_id = 0x006A


class Zarma(Language):
    ISO639_2 = 'dje'
    _english_name = 'Zarma'
    _native_name = u'Zarma'
    _lang_id = 0x1000


class Zulu(Language):
    ISO639_1 = 'zu'
    ISO639_2 = 'zul'
    _english_name = 'Zulu'
    _native_name = u'isiZulu'
    _lang_id = 0x0035


class Afghanistan(Locale):
    _iso_code = 'AF'
    _english_name = 'Afghanistan'
    _flag = 'flags\\AF.png'
    languages = [
        Persian(u'د افغانستان اسلامي دولتدولت اسلامی افغانستان', lcid=0x1000),
        Pashto(u'جمهوری اسلامی افغانستان', lcid=0x0463),
        Dari(u'افغانستان', lcid=0x048C),
        UzbekArab(u'', lcid=0x1000)
    ]


class AlandIslands(Locale):
    _iso_code = 'AX'
    _english_name = 'Aland Islands'
    _flag = 'flags\\AX.png'
    languages = [
        Swedish(u'Åland', lcid=0x1000)
    ]


class Albania(Locale):
    _iso_code = 'AL'
    _english_name = 'Albania'
    _flag = 'flags\\AL.png'
    languages = [
        Albanian(u'Shqipëria', lcid=0x041C)
    ]


class Algeria(Locale):
    _iso_code = 'DZ'
    _english_name = 'Algeria'
    _flag = 'flags\\DZ.png'
    languages = [
        Arabic(u'الجزائر', lcid=0x1401),
        French(u'', lcid=0x000C),
        Kabyle(u'', lcid=0x1000),
        TamazightLatin(u'', lcid=0x1000)
    ]


class AmericanSamoa(Locale):
    _iso_code = 'AS'
    _english_name = 'American Samoa'
    _flag = 'flags\\AS.png'
    languages = [
        English(u'American Samoa', lcid=0x1000),
        Samoan(u'Amerika Sāmoa', lcid=None)
    ]


class Andorra(Locale):
    _iso_code = 'AD'
    _english_name = 'Andorra'
    _flag = 'flags\\AD.png'
    languages = [
        Catalan(u'Andorra', lcid=0x1000)
    ]


class Angola(Locale):
    _iso_code = 'AO'
    _english_name = 'Angola'
    _flag = 'flags\\AO.png'
    languages = [
        Portuguese(u'Angola', lcid=0x1000),
        Lingala(u'Ngola', lcid=0x1000)
    ]


class Anguilla(Locale):
    _iso_code = 'AI'
    _english_name = 'Anguilla'
    _flag = 'flags\\AI.png'
    languages = [
        English(u'Anguilla', lcid=0x1000)
    ]


class Antarctica(Locale):
    _iso_code = 'AQ'
    _english_name = 'Antarctica'
    _flag = 'flags\\AQ.png'
    languages = [
        English(u'Antarctica', lcid=0x1000),
        Spanish(u'Antártico', lcid=None),
        French(u'Antarctique', lcid=None),
        Russian(u'Антарктике', lcid=None)
    ]


class AntiguaBarbuda(Locale):
    _iso_code = 'AG'
    _english_name = 'Antigua and Barbuda'
    _flag = 'flags\\AG.png'
    languages = [
        English(u'Antigua and Barbuda', lcid=0x1000)
    ]


class Argentina(Locale):
    _iso_code = 'AR'
    _english_name = 'Argentina'
    _flag = 'flags\\AR.png'
    languages = [
        Spanish(u'Argentina', lcid=0x2C0A)
    ]


class Armenia(Locale):
    _iso_code = 'AM'
    _english_name = 'Armenia'
    _flag = 'flags\\AM.png'
    languages = [
        Armenian(u'Հայաստան', lcid=0x042B)
    ]


class Aruba(Locale):
    _iso_code = 'AW'
    _english_name = 'Aruba'
    _flag = 'flags\\AW.png'
    languages = [
        Dutch(u'Aruba', lcid=0x1000),
        Papiamento(u'Aruba', lcid=None)
    ]


class Australia(Locale):
    _iso_code = 'AU'
    _english_name = 'Australia'
    _flag = 'flags\\AU.png'
    languages = [
        English(u'Australia', lcid=0x0C09)
    ]


class Austria(Locale):
    _iso_code = 'AT'
    _english_name = 'Austria'
    _flag = 'flags\\AT.png'
    languages = [
        German(u'Österreich', lcid=0x0C07),
        English(u'Austria', lcid=0x0009)
    ]


class Azerbaijan(Locale):
    _iso_code = 'AZ'
    _english_name = 'Azerbaijan'
    _flag = 'flags\\AZ.png'
    languages = [
        Azerbaijani(u'Azərbaycan', lcid=None),
        AzerbaijaniCyrillic(u'', lcid=0x082C),
        AzerbaijaniLatin(u'', lcid=0x042C)
    ]


class Bahamas(Locale):
    _iso_code = 'BS'
    _english_name = 'Bahamas'
    _flag = 'flags\\BS.png'
    languages = [
        English(u'The Bahamas', lcid=0x1000)
    ]


class Bahrein(Locale):
    _iso_code = 'BH'
    _english_name = 'Bahrein'
    _flag = 'flags\\BH.png'
    languages = [
        Arabic(u'البحرين', lcid=0x3C01)
    ]


class Bangladesh(Locale):
    _iso_code = 'BD'
    _english_name = 'Bangladesh'
    _flag = 'flags\\BD.png'
    languages = [
        Bengali(u'বাংলাদেশ', lcid=0x0845)
    ]


class Barbados(Locale):
    _iso_code = 'BB'
    _english_name = 'Barbados'
    _flag = 'flags\\BB.png'
    languages = [
        English(u'Barbados', lcid=0x1000)
    ]


class Belarus(Locale):
    _iso_code = 'BY'
    _english_name = 'Belarus'
    _flag = 'flags\\BY.png'
    languages = [
        Belarusian(u'Bielaruś', lcid=0x0423),
        Russian(u'Belarus', lcid=0x1000)
    ]


class Belgium(Locale):
    _iso_code = 'BE'
    _english_name = 'Belgium'
    _flag = 'flags\\BE.png'
    languages = [
        German(u'Belgien', lcid=0x1000),
        French(u'Belgique', lcid=0x080C),
        Dutch(u'België', lcid=0x0813),
        English(u'Belgium', lcid=0x0009)
    ]


class Belize(Locale):
    _iso_code = 'BZ'
    _english_name = 'Belize'
    _flag = 'flags\\BZ.png'
    languages = [
        English(u'Belize', lcid=0x2809),
        Spanish(u'', lcid=0x000A)
    ]


class Benin(Locale):
    _iso_code = 'BJ'
    _english_name = 'Benin'
    _flag = 'flags\\BJ.png'
    languages = [
        French(u'Bénin', lcid=0x1000),
        Yoruba(u'', lcid=0x006A)
    ]


class Bermuda(Locale):
    _iso_code = 'BM'
    _english_name = 'Bermuda'
    _flag = 'flags\\BM.png'
    languages = [
        English(u'Bermuda', lcid=0x1000)
    ]


class Bhutan(Locale):
    _iso_code = 'BT'
    _english_name = 'Bhutan'
    _flag = 'flags\\BT.png'
    languages = [
        Dzongkha(u'Druk Yul', lcid=None)
    ]


class Bolivia(Locale):
    _iso_code = 'BO'
    _english_name = 'Bolivia'
    _flag = 'flags\\BO.png'
    languages = [
        Aymara(u'Wuliwya', lcid=None),
        Spanish(u'Bolivia', lcid=0x400A),
        Guarani(u'Volívia', lcid=None),
        Quechua(u'Buliwya', lcid=None)
    ]


class BosniaHerzegovina(Locale):
    _iso_code = 'BA'
    _english_name = 'Bosnia and Herzegovina'
    _flag = 'flags\\BA.png'
    languages = [
        BosnianCyrillic(u'Босна и Херцеговина', lcid=0x201A),
        CroatianLatin(u'Bosna i Hercegovina', lcid=0x101A),
        SerbianCyrillic(u'Босна и Херцеговина', lcid=None),
        BosnianLatin(u'Bosna i Hercegovina', lcid=0x141A),
        SerbianLatin(u'Bosna i Hercegovina', lcid=0x181A)
    ]


class Botswana(Locale):
    _iso_code = 'BW'
    _english_name = 'Botswana'
    _flag = 'flags\\BW.png'
    languages = [
        English(u'Botswana', lcid=0x1000),
        Tswana(u'Botswana', lcid=None)
    ]


class BouvetIsland(Locale):
    _iso_code = 'BV'
    _english_name = 'Bouvet Island'
    _flag = 'flags\\BV.png'
    languages = [
        Norwegian(u'Bouvetøya', lcid=None)
    ]


class Brazil(Locale):
    _iso_code = 'BR'
    _english_name = 'Brazil'
    _flag = 'flags\\BR.png'
    languages = [
        Portuguese(u'Brasil', lcid=0x0416),
        Spanish(u'Brasil', lcid=0x000A)
    ]


class BritishIndianOceanTerritory(Locale):
    _iso_code = 'IO'
    _english_name = 'British Indian Ocean Territory'
    _flag = 'flags\\IO.png'
    languages = [
        English(u'British Indian Ocean Territory', lcid=0x1000)
    ]


class BritishVirginIslands(Locale):
    _iso_code = 'VG'
    _english_name = 'British Virgin Islands'
    _flag = 'flags\\VG.png'
    languages = [
        English(u'British Virgin Islands', lcid=0x1000)
    ]


class BruneiDarussalam(Locale):
    _iso_code = 'BN'
    _english_name = 'Brunei Darussalam'
    _flag = 'flags\\BN.png'
    languages = [
        Malay(u'Brunei', lcid=0x083E)
    ]


class Bulgaria(Locale):
    _iso_code = 'BG'
    _english_name = 'Bulgaria'
    _flag = 'flags\\BG.png'
    languages = [
        Bulgarian(u'Bulgariya', lcid=0x0402)
    ]


class BurkinaFaso(Locale):
    _iso_code = 'BF'
    _english_name = 'Burkina Faso'
    _flag = 'flags\\BF.png'
    languages = [
        French(u'Burkina Faso', lcid=None)
    ]


class Burundi(Locale):
    _iso_code = 'BI'
    _english_name = 'Burundi'
    _flag = 'flags\\BI.png'
    languages = [
        French(u'Burundi', lcid=None),
        English(u'Burundi', lcid=0x0009),
        Rundi(u'Uburundi', lcid=0x1000)
    ]


class CaboVerde(Locale):
    _iso_code = 'CV'
    _english_name = 'Cabo Verde'
    _flag = 'flags\\CV.png'
    languages = [
        Portuguese(u'Cabo Verde', lcid=None),
        Kabuverdianu(u'', lcid=0x1000)
    ]


class Cambodia(Locale):
    _iso_code = 'KH'
    _english_name = 'Cambodia'
    _flag = 'flags\\KH.png'
    languages = [
        Khmer(u'កម្ពុជា', lcid=0x0453)
    ]


class Cameroon(Locale):
    _iso_code = 'CM'
    _english_name = 'Cameroon'
    _flag = 'flags\\CM.png'
    languages = [
        English(u'Cameroon', lcid=0x1000),
        French(u'Cameroun', lcid=None),
        Aghem(u'', lcid=0x1000),
        Bafia(u'', lcid=0x1000),
        Basaa(u'', lcid=0x1000),
        Duala(u'', lcid=0x1000),
        Ewondo(u'', lcid=0x1000),
        Fulah(u'', lcid=0x0067),
        Kako(u'', lcid=0x1000),
        Kwasio(u'', lcid=0x1000),
        Meta(u'', lcid=0x1000),
        Mundang(u'', lcid=0x1000),
        Ngiemboon(u'', lcid=0x1000),
        Ngomba(u'', lcid=0x1000),
        Yangben(u'', lcid=0x1000)
    ]


class Canada(Locale):
    _iso_code = 'CA'
    _english_name = 'Canada'
    _flag = 'flags\\CA.png'
    languages = [
        English(u'Canada', lcid=0x1009),
        French(u'Canada', lcid=0x0C0C),
        InuktitutLatin(u'', lcid=0x085D),
        InuktitutSyllabics(u'', lcid=0x045D),
        Mohawk(u'', lcid=0x007C)
    ]


class Caribbean(Locale):
    _iso_code = '029'
    _english_name = 'Caribbean'
    _flag = None
    languages = [
        English(u'Caribbean', lcid=0x0009)
    ]


class CaribbeanNetherlands(Locale):
    _iso_code = 'BQ'
    _english_name = 'Caribbean Netherlands'
    _flag = 'flags\\BQ.png'
    languages = [
        Dutch(u'Caribisch Nederland', lcid=None)
    ]


class CaymanIslands(Locale):
    _iso_code = 'KY'
    _english_name = 'Cayman Islands'
    _flag = 'flags\\KY.png'
    languages = [
        English(u'Cayman Islands', lcid=0x1000)
    ]


class CentralAfricanRepublic(Locale):
    _iso_code = 'CF'
    _english_name = 'Central African Republic'
    _flag = 'flags\\CF.png'
    languages = [
        French(u'République Centrafricaine', lcid=None),
        Sango(u'Ködörösêse tî Bêafrîka', lcid=None),
        Lingala(u'', lcid=0x1000)
    ]


class Chad(Locale):
    _iso_code = 'TD'
    _english_name = 'Chad'
    _flag = 'flags\\TD.png'
    languages = [
        Arabic(u'تشاد', lcid=None),
        French(u'Tchad', lcid=None)
    ]


class Chile(Locale):
    _iso_code = 'CL'
    _english_name = 'Chile'
    _flag = 'flags\\CL.png'
    languages = [
        Spanish(u'Chile', lcid=0x340A),
        Mapudungun(u'', lcid=0x007A)
    ]


class China(Locale):
    _iso_code = 'CN'
    _english_name = 'China (People\'s Republic Of)'
    _flag = 'flags\\CN.png'
    languages = [
        ChineseSimplified(u'中国 (中华人民共和国)', lcid=0x0804),
        MongolianTraditional(u'', lcid=0x0850),
        Tibetan(u'', lcid=0x0051),
        Uyghur(u'', lcid=0x0080),
        SichuanYi(u'', lcid=0x0078)
    ]


class ChristmasIsland(Locale):
    _iso_code = 'CX'
    _english_name = 'Christmas Island'
    _flag = 'flags\\CX.png'
    languages = [
        English(u'Christmas Island', lcid=0x1000)
    ]


class CityoftheVatican(Locale):
    _iso_code = 'VA'
    _english_name = 'City of the Vatican'
    _flag = 'flags\\VA.png'
    languages = [
        Italian(u'Città del Vaticano', lcid=None)
    ]


class CocosIslands(Locale):
    _iso_code = 'CC'
    _english_name = 'Cocos (Keeling) Islands'
    _flag = 'flags\\CC.png'
    languages = [
        English(u'Cocos (Keeling) Islands', lcid=0x1000)
    ]


class Colombia(Locale):
    _iso_code = 'CO'
    _english_name = 'Colombia'
    _flag = 'flags\\CO.png'
    languages = [
        Spanish(u'Colombia', lcid=0x240A)
    ]


class Comores(Locale):
    _iso_code = 'KM'
    _english_name = 'Comores'
    _flag = 'flags\\KM.png'
    languages = [
        Arabic(u'جزر القمر', lcid=None),
        French(u'Comores', lcid=None),
        Swahili(u'Komori', lcid=None)
    ]


class CookIslands(Locale):
    _iso_code = 'CK'
    _english_name = 'Cook Islands'
    _flag = 'flags\\CK.png'
    languages = [
        English(u'Cook Islands', lcid=0x1000),
        Rarotongan(u'Kūki ʻĀirani', lcid=None)
    ]


class CostaRica(Locale):
    _iso_code = 'CR'
    _english_name = 'Costa Rica'
    _flag = 'flags\\CR.png'
    languages = [
        Spanish(u'Costa Rica', lcid=0x140A)
    ]


class CountryOfNauru(Locale):
    _iso_code = 'NR'
    _english_name = 'Nauru'
    _flag = 'flags\\NR.png'
    languages = [
        English(u'Nauru', lcid=0x1000),
        Nauru(u'', lcid=None)
    ]


class Croatia(Locale):
    _iso_code = 'HR'
    _english_name = 'Croatia'
    _flag = 'flags\\HR.png'
    languages = [
        CroatianLatin(u'Hrvatska', lcid=0x041A)
    ]


class Cuba(Locale):
    _iso_code = 'CU'
    _english_name = 'Cuba'
    _flag = 'flags\\CU.png'
    languages = [
        Spanish(u'Cuba', lcid=None)
    ]


class Curacao(Locale):
    _iso_code = 'CW'
    _english_name = 'Curacao'
    _flag = 'flags\\CW.png'
    languages = [
        English(u'Curacao', lcid=0x1000),
        Dutch(u'Curaçao', lcid=None)
    ]


class Cyprus(Locale):
    _iso_code = 'CY'
    _english_name = 'Cyprus'
    _flag = 'flags\\CY.png'
    languages = [
        Greek(u'Κύπρος', lcid=None),
        Turkish(u'Kıbrıs', lcid=None),
        English(u'Cyprus', lcid=0x0009)
    ]


class CzechRepublic(Locale):
    _iso_code = 'CZ'
    _english_name = 'Czech Republic'
    _flag = 'flags\\CZ.png'
    languages = [
        Czech(u'Česká republika Česko', lcid=0x0405)
    ]


class DemocraticRepublicCongo(Locale):
    _iso_code = 'CD'
    _english_name = 'Democratic Republic of the Congo'
    _flag = 'flags\\CD.png'
    languages = [
        French(u'République démocratique du Congo', lcid=None),
        CongoSwahili(u'Jamhuri ya Kidemokrasia ya Kongo', lcid=0x1000),
        Lingala(u'Republíki ya Kongó Demokratíki', lcid=0x1000),
        LubaKatanga(u'', lcid=0x1000)
    ]


class Denmark(Locale):
    _iso_code = 'DK'
    _english_name = 'Denmark'
    _flag = 'flags\\DK.png'
    languages = [
        Danish(u'Danmark', lcid=0x0406),
        English(u'Denmark', lcid=0x0009),
        Faroese(u'', lcid=0x0038)
    ]


class Djibouti(Locale):
    _iso_code = 'DJ'
    _english_name = 'Djibouti'
    _flag = 'flags\\DJ.png'
    languages = [
        Afar(u'Gabuutih', lcid=None),
        Arabic(u'جيبوتي', lcid=None),
        French(u'Djibouti', lcid=None),
        Somali(u'Jabuuti', lcid=None)
    ]


class Dominica(Locale):
    _iso_code = 'DM'
    _english_name = 'Dominica'
    _flag = 'flags\\DM.png'
    languages = [
        English(u'Dominica', lcid=0x1000)
    ]


class DominicanRepublic(Locale):
    _iso_code = 'DO'
    _english_name = 'Dominican Republic'
    _flag = 'flags\\DO.png'
    languages = [
        Spanish(u'República Dominicana', lcid=0x1C0A)
    ]


class Ecuador(Locale):
    _iso_code = 'EC'
    _english_name = 'Ecuador'
    _flag = 'flags\\EC.png'
    languages = [
        Spanish(u'Ecuador', lcid=0x300A),
        Quechua(u'', lcid=0x006B)
    ]


class Egypt(Locale):
    _iso_code = 'EG'
    _english_name = 'Egypt'
    _flag = 'flags\\EG.png'
    languages = [
        Arabic(u'مصر', lcid=0x0C01)
    ]


class ElSalvador(Locale):
    _iso_code = 'SV'
    _english_name = 'El Salvador'
    _flag = 'flags\\SV.png'
    languages = [
        Spanish(u'El Salvador', lcid=0x440A)
    ]


class EquatorialGuinea(Locale):
    _iso_code = 'GQ'
    _english_name = 'Equatorial Guinea'
    _flag = 'flags\\GQ.png'
    languages = [
        Spanish(u'Guiena ecuatorial', lcid=None),
        French(u'Guinée équatoriale', lcid=None),
        Portuguese(u'Guiné Equatorial', lcid=None)
    ]


class Eritrea(Locale):
    _iso_code = 'ER'
    _english_name = 'Eritrea'
    _flag = 'flags\\ER.png'
    languages = [
        Arabic(u'إرتريا', lcid=None),
        English(u'Eritrea', lcid=0x1000),
        Tigrinya(u'ኤርትራ', lcid=None),
        Afar(u'', lcid=0x1000),
        Blin(u'', lcid=0x1000),
        Saho(u'', lcid=0x1000),
        Tigre(u'', lcid=0x1000)
    ]


class Estonia(Locale):
    _iso_code = 'EE'
    _english_name = 'Estonia'
    _flag = 'flags\\EE.png'
    languages = [
        Estonian(u'eSwatini', lcid=0x0425)
    ]


class Ethiopia(Locale):
    _iso_code = 'ET'
    _english_name = 'Ethiopia'
    _flag = 'flags\\ET.png'
    languages = [
        Amharic(u'ኢትዮጵያ', lcid=0x045E),
        Oromo(u'Itoophiyaa', lcid=None),
        Afar(u'', lcid=0x1000),
        Somali(u'', lcid=0x0077),
        Tigrinya(u'', lcid=0x0073),
        Walamo(u'', lcid=0x1000)
    ]


class FalklandIslands(Locale):
    _iso_code = 'FK'
    _english_name = 'Falkland Islands'
    _flag = 'flags\\FK.png'
    languages = [
        English(u'Falkland Islands', lcid=0x1000)
    ]


class FaroeIslands(Locale):
    _iso_code = 'FO'
    _english_name = 'Faroe Islands'
    _flag = 'flags\\FO.png'
    languages = [
        Danish(u'Færøerne', lcid=None),
        Faroese(u'Føroyar', lcid=0x0438)
    ]


class Fiji(Locale):
    _iso_code = 'FJ'
    _english_name = 'Fiji'
    _flag = 'flags\\FJ.png'
    languages = [
        English(u'Fiji', lcid=0x1000)
    ]


class Finland(Locale):
    _iso_code = 'FI'
    _english_name = 'Finland'
    _flag = 'flags\\FI.png'
    languages = [
        Finnish(u'Suomi', lcid=0x040B),
        SamiNorthern(u'Suopma', lcid=0x0C3B),
        Swedish(u'Finland', lcid=0x081D),
        English(u'Finland', lcid=0x0009),
        SamiInari(u'', lcid=0x703B),
        SamiSkolt(u'', lcid=0x743B)
    ]


class France(Locale):
    _iso_code = 'FR'
    _english_name = 'France'
    _flag = 'flags\\FR.png'
    languages = [
        French(u'France', lcid=0x040C),
        SwissGerman(u'', lcid=0x0084),
        Breton(u'', lcid=0x007E),
        Catalan(u'', lcid=0x0003),
        Corsican(u'', lcid=0x0083),
        Interlingua(u'', lcid=0x1000),
        Occitan(u'', lcid=0x0082)
    ]


class FrenchGuiana(Locale):
    _iso_code = 'GF'
    _english_name = 'French Guiana'
    _flag = 'flags\\GF.png'
    languages = [
        French(u'Guyane', lcid=None)
    ]


class FrenchPolynesia(Locale):
    _iso_code = 'PF'
    _english_name = 'French Polynesia'
    _flag = 'flags\\PF.png'
    languages = [
        French(u'Polynésie française', lcid=None)
    ]


class FrenchSouthernandAntarcticLands(Locale):
    _iso_code = 'TF'
    _english_name = 'French Southern and Antarctic Lands'
    _flag = 'flags\\TF.png'
    languages = [
        French(u'Terres australes et antarctiques françaises', lcid=None)
    ]


class Gabon(Locale):
    _iso_code = 'GA'
    _english_name = 'Gabon'
    _flag = 'flags\\GA.png'
    languages = [
        French(u'République gabonaise', lcid=None)
    ]


class Georgia(Locale):
    _iso_code = 'GE'
    _english_name = 'Georgia'
    _flag = 'flags\\GE.png'
    languages = [
        Georgian(u'საქართველო', lcid=0x0437),
        Ossetian(u'', lcid=0x1000)
    ]


class Germany(Locale):
    _iso_code = 'DE'
    _english_name = 'Germany'
    _flag = 'flags\\DE.png'
    languages = [
        German(u'Deutschland', lcid=0x0407),
        Luxembourgish(u'Däitschland', lcid=None),
        SwissGerman(u'Deutschland', lcid=None),
        Bavarian(u'Deitschland', lcid=None),
        Danish(u'Tyskland', lcid=None),
        UpperSorbian(u'Nىmska', lcid=0x042E),
        LowerSorbian(u'Nimce', lcid=0x082E),
        NorthFrisian(u'Tjüschlönj', lcid=None),
        SaterlandFrisian(u'Dútslân', lcid=None),
        Romani(u'Jermaniya', lcid=None),
        LowGerman(u'Düütschland', lcid=None),
        English(u'Germany', lcid=0x1000),
        Ripuarian(u'', lcid=0x1000)
    ]


class Ghana(Locale):
    _iso_code = 'GH'
    _english_name = 'Ghana'
    _flag = 'flags\\GH.png'
    languages = [
        English(u'Ghana', lcid=0x1000),
        Akan(u'Gaana', lcid=0x1000),
        Ewe(u'Gana', lcid=0x1000),
        HausaLatin(u'', lcid=0x1000)
    ]


class Gibraltar(Locale):
    _iso_code = 'GI'
    _english_name = 'Gibraltar'
    _flag = 'flags\\GI.png'
    languages = [
        English(u'Gibraltar', lcid=0x1000)
    ]


class Greece(Locale):
    _iso_code = 'GR'
    _english_name = 'Greece'
    _flag = 'flags\\GR.png'
    languages = [
        Greek(u'Ελλάδα', lcid=0x0408)
    ]


class Greenland(Locale):
    _iso_code = 'GL'
    _english_name = 'Greenland'
    _flag = 'flags\\GL.png'
    languages = [
        Danish(u'Grønland', lcid=None),
        Kalaallisut(u'Kalaallit Nunaat', lcid=0x046F)
    ]


class Grenada(Locale):
    _iso_code = 'GD'
    _english_name = 'Grenada'
    _flag = 'flags\\GD.png'
    languages = [
        English(u'Grenada', lcid=0x1000)
    ]


class Guadeloupe(Locale):
    _iso_code = 'GP'
    _english_name = 'Guadeloupe'
    _flag = 'flags\\GP.png'
    languages = [
        French(u'Guadeloupe', lcid=None)
    ]


class Guam(Locale):
    _iso_code = 'GU'
    _english_name = 'Guam'
    _flag = 'flags\\GU.png'
    languages = [
        Chamorro(u'Guåhån', lcid=None),
        English(u'Guam', lcid=0x1000)
    ]


class Guatemala(Locale):
    _iso_code = 'GT'
    _english_name = 'Guatemala'
    _flag = 'flags\\GT.png'
    languages = [
        Spanish(u'Guatemala', lcid=0x100A),
        Kiche(u'', lcid=0x0486)
    ]


class Guernsey(Locale):
    _iso_code = 'GG'
    _english_name = 'Guernsey'
    _flag = 'flags\\GG.png'
    languages = [
        English(u'Guernsey', lcid=0x1000)
    ]


class Guinea(Locale):
    _iso_code = 'GN'
    _english_name = 'Guinea'
    _flag = 'flags\\GN.png'
    languages = [
        French(u'Guinée', lcid=None),
        Fulah(u'Gine', lcid=0x0067),
        Nko(u'', lcid=0x1000)
    ]


class GuineaBissau(Locale):
    _iso_code = 'GW'
    _english_name = 'Guinea Bissau'
    _flag = 'flags\\GW.png'
    languages = [
        Portuguese(u'Guiné-Bissau', lcid=None)
    ]


class Guyana(Locale):
    _iso_code = 'GY'
    _english_name = 'Guyana'
    _flag = 'flags\\GY.png'
    languages = [
        English(u'Guyana', lcid=0x1000)
    ]


class Haiti(Locale):
    _iso_code = 'HT'
    _english_name = 'Haiti'
    _flag = 'flags\\HT.png'
    languages = [
        French(u'Haïti', lcid=None),
        HaitianCreole(u'Ayiti', lcid=None)
    ]


class HeardIslandandMcDonaldIslands(Locale):
    _iso_code = 'HM'
    _english_name = 'Heard Island and McDonald Islands'
    _flag = 'flags\\HM.png'
    languages = [
        English(u'Heard Island and McDonald Islands', lcid=0x1000)
    ]


class Honduras(Locale):
    _iso_code = 'HN'
    _english_name = 'Honduras'
    _flag = 'flags\\HN.png'
    languages = [
        Spanish(u'Honduras', lcid=0x480A)
    ]


class HongKong(Locale):
    _iso_code = 'HK'
    _english_name = 'Hong Kong (SAR of China)'
    _flag = 'flags\\HK.png'
    languages = [
        English(u'Hong Kong', lcid=0x1000),
        ChineseTraditional(u'香港', lcid=None)
    ]


class Hungary(Locale):
    _iso_code = 'HU'
    _english_name = 'Hungary'
    _flag = 'flags\\HU.png'
    languages = [
        Hungarian(u'Magyarország', lcid=0x040E)
    ]


class Iceland(Locale):
    _iso_code = 'IS'
    _english_name = 'Iceland'
    _flag = 'flags\\IS.png'
    languages = [
        Icelandic(u'Ísland', lcid=0x040F)
    ]


class India(Locale):
    _iso_code = 'IN'
    _english_name = 'India'
    _flag = 'flags\\IN.png'
    languages = [
        English(u'India', lcid=0x4009),
        Hindi(u'भारत', lcid=0x0439),
        Assamese(u'ভাৰত', lcid=0x004D),
        Bengali(u'ভারত', lcid=0x0045),
        Bodo(u'', lcid=0x1000),
        Gujarati(u'ભારત', lcid=0x0047),
        Kannada(u'ಭಾರತ', lcid=0x004B),
        Kashmiri(u'', lcid=0x1000),
        Konkani(u'भारत', lcid=0x0057),
        Malayalam(u'ഭാരതം', lcid=0x004C),
        Marathi(u'भारत', lcid=0x004E),
        Nepali(u'भारत', lcid=0x0061),
        Oriya(u'ଭାରତ', lcid=0x0048),
        Punjabi(u'ਭਾਰਤ', lcid=0x0046),
        Sanskrit(u'भारतम्', lcid=0x004F),
        Tamil(u'பாரதம்', lcid=0x0049),
        Telugu(u'భారత దేశం', lcid=0x004A),
        Tibetan(u'', lcid=0x0051),
        Urdu(u'', lcid=0x0020)
    ]


class Indonesia(Locale):
    _iso_code = 'ID'
    _english_name = 'Indonesia'
    _flag = 'flags\\ID.png'
    languages = [
        Indonesian(u'Indonesia', lcid=0x0421),
        Javanese(u'', lcid=0x1000)
    ]


class Iran(Locale):
    _iso_code = 'IR'
    _english_name = 'Iran'
    _flag = 'flags\\IR.png'
    languages = [
        Persian(u'ایران', lcid=0x0429),
        Kurdish(u'', lcid=0x0492),
        Mazanderani(u'', lcid=0x1000),
        NorthernLuri(u'', lcid=0x1000)
    ]


class Iraq(Locale):
    _iso_code = 'IQ'
    _english_name = 'Iraq'
    _flag = 'flags\\IQ.png'
    languages = [
        Arabic(u'العراق', lcid=0x0801),
        Kurdish(u'Îraq', lcid=None),
        CentralKurdish(u'', lcid=0x0492),
        NorthernLuri(u'', lcid=0x1000)
    ]


class Ireland(Locale):
    _iso_code = 'IE'
    _english_name = 'Ireland'
    _flag = 'flags\\IE.png'
    languages = [
        English(u'Ireland', lcid=0x1809),
        Irish(u'Éire', lcid=0x083C)
    ]


class IsleofMan(Locale):
    _iso_code = 'IM'
    _english_name = 'Isle of Man'
    _flag = 'flags\\IM.png'
    languages = [
        English(u'Isle of Man', lcid=0x1000),
        Manx(u'Ellan Vannin', lcid=0x1000)
    ]


class Israel(Locale):
    _iso_code = 'IL'
    _english_name = 'Israel'
    _flag = 'flags\\IL.png'
    languages = [
        Hebrew(u'ישראל', lcid=0x040D),
        Arabic(u'إسرائيل', lcid=0x0001),
        English(u'Israel', lcid=0x0009)
    ]


class Italia(Locale):
    _iso_code = 'IT'
    _english_name = 'Italia'
    _flag = 'flags\\IT.png'
    languages = [
        German(u'Italia', lcid=None),
        French(u'Italia', lcid=None),
        Italian(u'Italia', lcid=0x0410),
        Catalan(u'', lcid=0x0003),
        Friulian(u'', lcid=0x1000)
    ]


class IvoryCoast(Locale):
    _iso_code = 'CI'
    _english_name = 'Ivory Coast'
    _flag = 'flags\\CI.png'
    languages = [
        French(u'Côte d\'Ivoire', lcid=None)
    ]


class Jamaica(Locale):
    _iso_code = 'JM'
    _english_name = 'Jamaica'
    _flag = 'flags\\JM.png'
    languages = [
        English(u'Jamaica', lcid=0x2009)
    ]


class Japan(Locale):
    _iso_code = 'JP'
    _english_name = 'Japan'
    _flag = 'flags\\JP.png'
    languages = [
        Japanese(u'日本', lcid=0x0411)
    ]


class Jersey(Locale):
    _iso_code = 'JE'
    _english_name = 'Jersey'
    _flag = 'flags\\JE.png'
    languages = [
        English(u'Jersey', lcid=0x1000)
    ]


class Jordan(Locale):
    _iso_code = 'JO'
    _english_name = 'Jordan'
    _flag = 'flags\\JO.png'
    languages = [
        Arabic(u'الأردن', lcid=0x2C01)
    ]


class Kazakhstan(Locale):
    _iso_code = 'KZ'
    _english_name = 'Kazakhstan'
    _flag = 'flags\\KZ.png'
    languages = [
        Kazakh(u'Қазақстан', lcid=0x043F),
        Russian(u'Казахстан', lcid=None)
    ]


class Kenya(Locale):
    _iso_code = 'KE'
    _english_name = 'Kenya'
    _flag = 'flags\\KE.png'
    languages = [
        English(u'Kenya', lcid=0x1000),
        Swahili(u'Kenya', lcid=0x0441),
        Embu(u'', lcid=0x1000),
        Gusii(u'', lcid=0x1000),
        Kalenjin(u'', lcid=0x1000),
        Kamba(u'', lcid=0x1000),
        Kikuyu(u'', lcid=0x1000),
        Luo(u'', lcid=0x1000),
        Luyia(u'', lcid=0x1000),
        Masai(u'', lcid=0x1000),
        Meru(u'', lcid=0x1000),
        Oromo(u'', lcid=0x0072),
        Samburu(u'', lcid=0x1000),
        Somali(u'', lcid=0x0077),
        Taita(u'', lcid=0x1000),
        Teso(u'', lcid=0x1000)
    ]


class Kiribati(Locale):
    _iso_code = 'KI'
    _english_name = 'Kiribati'
    _flag = 'flags\\KI.png'
    languages = [
        English(u'Kiribati', lcid=0x1000)
    ]


class Kuweit(Locale):
    _iso_code = 'KW'
    _english_name = 'Kuweit'
    _flag = 'flags\\KW.png'
    languages = [
        Arabic(u'دولة الكويت', lcid=0x3401)
    ]


class Kyrgyzstan(Locale):
    _iso_code = 'KG'
    _english_name = 'Kyrgyzstan'
    _flag = 'flags\\KG.png'
    languages = [
        Kyrgyz(u'Кыргызстан', lcid=0x0440),
        Russian(u'Киргизия', lcid=None)
    ]


class Laos(Locale):
    _iso_code = 'LA'
    _english_name = 'Laos'
    _flag = 'flags\\LA.png'
    languages = [
        Lao(u'ປະເທດລາວ', lcid=0x0454)
    ]


class LatinAmerica(Locale):
    _iso_code = '419'
    _english_name = 'Latin America'
    _flag = None
    languages = [
        Spanish(u'', lcid=0x000A)
    ]


class Latvia(Locale):
    _iso_code = 'LV'
    _english_name = 'Latvia'
    _flag = 'flags\\LV.png'
    languages = [
        Latvian(u'Latvija', lcid=0x0426)
    ]


class Lebanon(Locale):
    _iso_code = 'LB'
    _english_name = 'Lebanon'
    _flag = 'flags\\LB.png'
    languages = [
        Arabic(u'لبنان', lcid=0x3001),
        French(u'Liban', lcid=None)
    ]


class Lesotho(Locale):
    _iso_code = 'LS'
    _english_name = 'Lesotho'
    _flag = 'flags\\LS.png'
    languages = [
        English(u'Lesotho', lcid=0x1000),
        Sotho(u'Lesotho', lcid=None),
        SothoSouthern(u'', lcid=0x0030)
    ]


class Liberia(Locale):
    _iso_code = 'LR'
    _english_name = 'Liberia'
    _flag = 'flags\\LR.png'
    languages = [
        English(u'Liberia', lcid=0x1000),
        Vai(u'', lcid=0x1000),
        VaiLatin(u'', lcid=0x1000)
    ]


class Libya(Locale):
    _iso_code = 'LY'
    _english_name = 'Libya'
    _flag = 'flags\\LY.png'
    languages = [
        Arabic(u'ليبيا', lcid=0x1001)
    ]


class Liechtenstein(Locale):
    _iso_code = 'LI'
    _english_name = 'Liechtenstein'
    _flag = 'flags\\LI.png'
    languages = [
        German(u'Liechtenstein', lcid=0x1407),
        SwissGerman(u'', lcid=0x0084)
    ]


class Lithuania(Locale):
    _iso_code = 'LT'
    _english_name = 'Lithuania'
    _flag = 'flags\\LT.png'
    languages = [
        Lithuanian(u'Lietuva', lcid=0x0427)
    ]


class Luxembourg(Locale):
    _iso_code = 'LU'
    _english_name = 'Luxembourg'
    _flag = 'flags\\LU.png'
    languages = [
        German(u'Luxemburg', lcid=0x1007),
        French(u'Luxembourg', lcid=0x140C),
        Luxembourgish(u'Lëtzebuerg', lcid=0x046E),
        Portuguese(u'', lcid=0x0016)
    ]


class Macau(Locale):
    _iso_code = 'MO'
    _english_name = 'Macau (SAR of China)'
    _flag = 'flags\\MO.png'
    languages = [
        Portuguese(u'Macau', lcid=None),
        ChineseTraditional(u'澳門', lcid=None),
        English(u'Macau', lcid=0x0009)
    ]


class Macedonia(Locale):
    _iso_code = 'MK'
    _english_name = 'Macedonia (Former Yugoslav Republic of)'
    _flag = 'flags\\MK.png'
    languages = [
        Macedonian(u'Македонија', lcid=0x042F),
        Albanian(u'', lcid=0x001C)
    ]


class Madagascar(Locale):
    _iso_code = 'MG'
    _english_name = 'Madagascar'
    _flag = 'flags\\MG.png'
    languages = [
        French(u'Madagascar', lcid=None),
        Malagasy(u'Madagasikara', lcid=None),
        English(u'Madagascar', lcid=0x0009)
    ]


class Malawi(Locale):
    _iso_code = 'MW'
    _english_name = 'Malawi'
    _flag = 'flags\\MW.png'
    languages = [
        English(u'Malawi', lcid=0x1000),
        Nyanja(u'Malaŵi', lcid=None)
    ]


class Malaysia(Locale):
    _iso_code = 'MY'
    _english_name = 'Malaysia'
    _flag = 'flags\\MY.png'
    languages = [
        Malay(u'Malaysia', lcid=0x043E),
        English(u'Malaysia', lcid=0x0009),
        Tamil(u'மலேசியா', lcid=0x0049)
    ]


class Maldives(Locale):
    _iso_code = 'MV'
    _english_name = 'Maldives'
    _flag = 'flags\\MV.png'
    languages = [
        Divehi(u'ދިވެހިރާއްޖެ', lcid=0x0465)
    ]


class Mali(Locale):
    _iso_code = 'ML'
    _english_name = 'Mali'
    _flag = 'flags\\ML.png'
    languages = [
        French(u'Mali', lcid=None),
        BamanankanLatin(u'', lcid=0x1000),
        KoyraChiini(u'', lcid=0x1000),
        KoyraboroSenni(u'', lcid=0x1000)
    ]


class Malta(Locale):
    _iso_code = 'MT'
    _english_name = 'Malta'
    _flag = 'flags\\MT.png'
    languages = [
        English(u'Malta', lcid=0x1000),
        Maltese(u'Malta', lcid=0x043A)
    ]


class MarshallIslands(Locale):
    _iso_code = 'MH'
    _english_name = 'Marshall Islands'
    _flag = 'flags\\MH.png'
    languages = [
        English(u'Marshall Islands', lcid=0x1000),
        Marshallese(u'Aorōkin M̧ajeļ', lcid=None)
    ]


class Martinique(Locale):
    _iso_code = 'MQ'
    _english_name = 'Martinique'
    _flag = 'flags\\MQ.png'
    languages = [
        French(u'Martinique', lcid=None)
    ]


class Mauritania(Locale):
    _iso_code = 'MR'
    _english_name = 'Mauritania'
    _flag = 'flags\\MR.png'
    languages = [
        Arabic(u'موريتانيا', lcid=None),
        French(u'Mauritanie', lcid=None),
        Fulah(u'ⵎⵓⵔⵉⵜⴰⵏ / ⴰⴳⴰⵡⵛ', lcid=0x0067)
    ]


class Mauritius(Locale):
    _iso_code = 'MU'
    _english_name = 'Mauritius'
    _flag = 'flags\\MU.png'
    languages = [
        English(u'Mauritius', lcid=0x1000),
        French(u'Maurice', lcid=None),
        Morisyen(u'Moris', lcid=None)
    ]


class Mayotte(Locale):
    _iso_code = 'YT'
    _english_name = 'Mayotte'
    _flag = 'flags\\YT.png'
    languages = [
        French(u'Mayotte', lcid=None)
    ]


class Mexico(Locale):
    _iso_code = 'MX'
    _english_name = 'Mexico'
    _flag = 'flags\\MX.png'
    languages = [
        Spanish(u'México', lcid=0x080A)
    ]


class Micronesia(Locale):
    _iso_code = 'FM'
    _english_name = 'Micronesia (Federated States of)'
    _flag = 'flags\\FM.png'
    languages = [
        English(u'Micronesia', lcid=0x1000)
    ]


class Moldova(Locale):
    _iso_code = 'MD'
    _english_name = 'Moldova'
    _flag = 'flags\\MD.png'
    languages = [
        Romanian(u'Moldova', lcid=None),
        Russian(u'Молдавия', lcid=None),
        Ukrainian(u'Молдова', lcid=None)
    ]


class Monaco(Locale):
    _iso_code = 'MC'
    _english_name = 'Monaco'
    _flag = 'flags\\MC.png'
    languages = [
        French(u'Monaco', lcid=0x180C)
    ]


class Mongolia(Locale):
    _iso_code = 'MN'
    _english_name = 'Mongolia'
    _flag = 'flags\\MN.png'
    languages = [
        Mongolian(u'ᠮᠤᠩᠭᠤᠯ ᠤᠯᠤᠰ', lcid=0x0450)
    ]


class Montenegro(Locale):
    _iso_code = 'ME'
    _english_name = 'Montenegro'
    _flag = 'flags\\ME.png'
    languages = [
        BosnianCyrillic(u'Crna Gora', lcid=None),
        CroatianLatin(u'Crna Gora', lcid=None),
        Albanian(u'Mali i Zi', lcid=None),
        SerbianCyrillic(u'Црна Гора', lcid=None),
        SerbianLatin(u'', lcid=0x181A)
    ]


class Montserrat(Locale):
    _iso_code = 'MS'
    _english_name = 'Montserrat'
    _flag = 'flags\\MS.png'
    languages = [
        English(u'Montserrat', lcid=0x1000)
    ]


class Morocco(Locale):
    _iso_code = 'MA'
    _english_name = 'Morocco'
    _flag = 'flags\\MA.png'
    languages = [
        Arabic(u'المغرب', lcid=0x1801),
        French(u'Maroc', lcid=None),
        StandardMoroccanTamazight(u'ⴰⵎⵔⵔⵓⴽ / ⵍⵎⵖⵔⵉⴱ', lcid=None),
        CentralAtlasTamazightLatin(u'', lcid=0x1000),
        Tachelhit(u'', lcid=0x1000),
        TachelhitLatin(u'', lcid=0x1000)
    ]


class Mozambique(Locale):
    _iso_code = 'MZ'
    _english_name = 'Mozambique'
    _flag = 'flags\\MZ.png'
    languages = [
        Portuguese(u'Moçambique', lcid=None),
        MakhuwaMeetto(u'', lcid=0x1000),
        Sena(u'', lcid=0x1000)
    ]


class Myanmar(Locale):
    _iso_code = 'MM'
    _english_name = 'Myanmar'
    _flag = 'flags\\MM.png'
    languages = [
        Burmese(u'မြန်မာ', lcid=None)
    ]


class Namibia(Locale):
    _iso_code = 'NA'
    _english_name = 'Namibia'
    _flag = 'flags\\NA.png'
    languages = [
        German(u'Namibia', lcid=None),
        English(u'Namibia', lcid=0x1000),
        Afrikaans(u'Namibia', lcid=0x0036),
        Nama(u'Namibia', lcid=0x1000)
    ]


class Nepal(Locale):
    _iso_code = 'NP'
    _english_name = 'Nepal'
    _flag = 'flags\\NP.png'
    languages = [
        Nepali(u'Nepāl', lcid=0x0461)
    ]


class NewCaledonia(Locale):
    _iso_code = 'NC'
    _english_name = 'New Caledonia'
    _flag = 'flags\\NC.png'
    languages = [
        French(u'Nouvelle-Calédonie', lcid=None)
    ]


class NewZealand(Locale):
    _iso_code = 'NZ'
    _english_name = 'New Zealand'
    _flag = 'flags\\NZ.png'
    languages = [
        English(u'New Zealand', lcid=0x1409),
        Maori(u'Aotearoa', lcid=0x0481)
    ]


class Nicaragua(Locale):
    _iso_code = 'NI'
    _english_name = 'Nicaragua'
    _flag = 'flags\\NI.png'
    languages = [
        Spanish(u'Nicaragua', lcid=0x4C0A)
    ]


class Niger(Locale):
    _iso_code = 'NE'
    _english_name = 'Niger'
    _flag = 'flags\\NE.png'
    languages = [
        French(u'Niger', lcid=None),
        HausaLatin(u'', lcid=0x1000),
        Tasawaq(u'', lcid=0x1000),
        Zarma(u'', lcid=0x1000)
    ]


class Nigeria(Locale):
    _iso_code = 'NG'
    _english_name = 'Nigeria'
    _flag = 'flags\\NG.png'
    languages = [
        English(u'Nigeria', lcid=0x1000),
        HausaLatin(u'Nijeriya ', lcid=0x1000),
        Igbo(u'Naigeria', lcid=0x0070),
        Yoruba(u'Nàìjíríà', lcid=0x006A)
    ]


class Niue(Locale):
    _iso_code = 'NU'
    _english_name = 'Niue'
    _flag = 'flags\\NU.png'
    languages = [
        English(u'Niue', lcid=0x1000),
        Niuean(u'Niuē', lcid=None)
    ]


class NorfolkIsland(Locale):
    _iso_code = 'NF'
    _english_name = 'Norfolk Island'
    _flag = 'flags\\NF.png'
    languages = [
        English(u'Norfolk Island', lcid=0x1000),
        PitcairnNorfolk(u'Norf\'k Ailen', lcid=None)
    ]


class NorthKorea(Locale):
    _iso_code = 'KP'
    _english_name = 'North Korea'
    _flag = 'flags\\KP.png'
    languages = [
        Korean(u'북조선', lcid=None)
    ]


class NorthernMarianaIslands(Locale):
    _iso_code = 'MP'
    _english_name = 'Northern Mariana Islands'
    _flag = 'flags\\MP.png'
    languages = [
        Chamorro(u'Notte Mariånas', lcid=None),
        English(u'Northern Mariana Islands', lcid=0x1000)
    ]


class Norway(Locale):
    _iso_code = 'NO'
    _english_name = 'Norway'
    _flag = 'flags\\NO.png'
    languages = [
        NorwegianBokmal(u'Norge', lcid=0x0414),
        NorwegianNynorsk(u'Noreg', lcid=0x0814),
        Norwegian(u'Norge', lcid=None),
        SamiNorthern(u'Norga', lcid=0x043B),
        SamiLule(u'', lcid=0x7C3B),
        SamiSouthern(u'', lcid=0x783B)
    ]


class Oman(Locale):
    _iso_code = 'OM'
    _english_name = 'Oman'
    _flag = 'flags\\OM.png'
    languages = [
        Arabic(u'عُمان', lcid=0x2001)
    ]


class Pakistan(Locale):
    _iso_code = 'PK'
    _english_name = 'Pakistan'
    _flag = 'flags\\PK.png'
    languages = [
        English(u'Pakistan', lcid=0x1000),
        Urdu(u'Pākistān', lcid=0x0420),
        Punjabi(u'', lcid=0x0846),
        Sindhi(u'', lcid=0x0859)
    ]


class Palau(Locale):
    _iso_code = 'PW'
    _english_name = 'Palau'
    _flag = 'flags\\PW.png'
    languages = [
        English(u'Palau', lcid=0x1000),
        Japanese(u'パラオ', lcid=None),
        Palauan(u'Belau', lcid=None),
        Tobian(u'Palau', lcid=None)
    ]


class PalestinianTerritory(Locale):
    _iso_code = 'PS'
    _english_name = 'Palestinian Territory'
    _flag = 'flags\\PS.png'
    languages = [
        Arabic(u'فلسطين', lcid=None),
        Hebrew(u'טריטוריה פלסטינית', lcid=None)
    ]


class Panama(Locale):
    _iso_code = 'PA'
    _english_name = 'Panama'
    _flag = 'flags\\PA.png'
    languages = [
        Spanish(u'Panamá', lcid=0x180A)
    ]


class PapuaNewGuinea(Locale):
    _iso_code = 'PG'
    _english_name = 'Papua New Guinea'
    _flag = 'flags\\PG.png'
    languages = [
        English(u'Papua New Guinea', lcid=0x1000),
        HiriMotu(u'Papua Niugini', lcid=None),
        TokPisin(u'Papua Niugini', lcid=None)
    ]


class Paraguay(Locale):
    _iso_code = 'PY'
    _english_name = 'Paraguay'
    _flag = 'flags\\PY.png'
    languages = [
        Spanish(u'Paraguay', lcid=0x3C0A),
        Guarani(u'Paraguái', lcid=None)
    ]


class Peru(Locale):
    _iso_code = 'PE'
    _english_name = 'Peru'
    _flag = 'flags\\PE.png'
    languages = [
        Spanish(u'Perú', lcid=0x280A),
        Quechua(u'Piruw', lcid=0x006B)
    ]


class Philippines(Locale):
    _iso_code = 'PH'
    _english_name = 'Philippines'
    _flag = 'flags\\PH.png'
    languages = [
        English(u'Philippines', lcid=0x3409),
        Tagalog(u'', lcid=None),
        Filipino(u'Pilipinas', lcid=0x0064),
        Spanish(u'', lcid=0x000A)
    ]


class Pitcairn(Locale):
    _iso_code = 'PN'
    _english_name = 'Pitcairn'
    _flag = 'flags\\PN.png'
    languages = [
        English(u'Pitcairn', lcid=0x1000),
        PitcairnNorfolk(u'Pitkern Ailen', lcid=None)
    ]


class Poland(Locale):
    _iso_code = 'PL'
    _english_name = 'Poland'
    _flag = 'flags\\PL.png'
    languages = [
        Polish(u'Polska', lcid=0x0415)
    ]


class Portugal(Locale):
    _iso_code = 'PT'
    _english_name = 'Portugal'
    _flag = 'flags\\PT.png'
    languages = [
        Portuguese(u'Portugal', lcid=0x0816)
    ]


class PuertoRico(Locale):
    _iso_code = 'PR'
    _english_name = 'Puerto Rico'
    _flag = 'flags\\PR.png'
    languages = [
        English(u'Puerto Rico', lcid=0x1000),
        Spanish(u'Puerto Rico', lcid=0x500A)
    ]


class Qatar(Locale):
    _iso_code = 'QA'
    _english_name = 'Qatar'
    _flag = 'flags\\QA.png'
    languages = [
        Arabic(u'قطر', lcid=0x4001)
    ]


class RepublicCongo(Locale):
    _iso_code = 'CG'
    _english_name = 'Republic of the Congo (Congo-Brazzaville)'
    _flag = 'flags\\CG.png'
    languages = [
        French(u'République démocratique du Congo', lcid=None),
        Lingala(u'Republíki ya Kongó Demokratíki', lcid=0x1000)
    ]


class Reunion(Locale):
    _iso_code = 'RE'
    _english_name = 'Reunion'
    _flag = 'flags\\RE.png'
    languages = [
        French(u'Réunion', lcid=None)
    ]


class Romania(Locale):
    _iso_code = 'RO'
    _english_name = 'Romania'
    _flag = 'flags\\RO.png'
    languages = [
        Romanian(u'România', lcid=0x0418)
    ]


class Russia(Locale):
    _iso_code = 'RU'
    _english_name = 'Russia'
    _flag = 'flags\\RU.png'
    languages = [
        Russian(u'Россия', lcid=0x0419),
        Bashkir(u'', lcid=0x006D),
        Chechen(u'', lcid=0x1000),
        ChurchSlavic(u'', lcid=0x1000),
        Ossetian(u'', lcid=0x1000),
        Yakut(u'', lcid=0x0085),
        Tatar(u'', lcid=0x0044)
    ]


class Rwanda(Locale):
    _iso_code = 'RW'
    _english_name = 'Rwanda'
    _flag = 'flags\\RW.png'
    languages = [
        English(u'Rwanda', lcid=0x1000),
        French(u'Rwanda', lcid=None),
        Kinyarwanda(u'Rwanda', lcid=0x0487)
    ]


class SaintBarts(Locale):
    _iso_code = 'BL'
    _english_name = 'Saint-Barts'
    _flag = 'flags\\BL.png'
    languages = [
        French(u'Saint-Barthélemy', lcid=None)
    ]


class SaintHelena(Locale):
    _iso_code = 'SH'
    _english_name = 'Saint Helena'
    _flag = 'flags\\SH.png'
    languages = [
        English(u'Saint Helena', lcid=0x1000)
    ]


class SaintKittsandNevis(Locale):
    _iso_code = 'KN'
    _english_name = 'Saint Kitts and Nevis'
    _flag = 'flags\\KN.png'
    languages = [
        English(u'Saint Kitts and Nevis', lcid=0x1000)
    ]


class SaintLucia(Locale):
    _iso_code = 'LC'
    _english_name = 'Saint Lucia'
    _flag = 'flags\\LC.png'
    languages = [
        English(u'Saint Lucia', lcid=0x1000)
    ]


class SaintMartinDutch(Locale):
    _iso_code = 'SX'
    _english_name = 'Saint Martin (Dutch part)'
    _flag = 'flags\\SX.png'
    languages = [
        English(u'Saint Martin', lcid=0x1000),
        Dutch(u'Sint Maarten', lcid=None)
    ]


class SaintMartinFrench(Locale):
    _iso_code = 'MF'
    _english_name = 'Saint Martin (French part)'
    _flag = 'flags\\MF.png'
    languages = [
        French(u'Saint-Martin', lcid=None)
    ]


class SaintPierreandMiquelon(Locale):
    _iso_code = 'PM'
    _english_name = 'Saint Pierre and Miquelon'
    _flag = 'flags\\PM.png'
    languages = [
        French(u'Saint-Pierre et Miquelon', lcid=None)
    ]


class SaintVincentandtheGrenadines(Locale):
    _iso_code = 'VC'
    _english_name = 'Saint Vincent and the Grenadines'
    _flag = 'flags\\VC.png'
    languages = [
        English(u'Saint Vincent and the Grenadines', lcid=0x1000)
    ]


class Samoa(Locale):
    _iso_code = 'WS'
    _english_name = 'Samoa'
    _flag = 'flags\\WS.png'
    languages = [
        English(u'Samoa', lcid=0x1000),
        Samoan(u'Sāmoa', lcid=None)
    ]


class SanMarino(Locale):
    _iso_code = 'SM'
    _english_name = 'San Marino'
    _flag = 'flags\\SM.png'
    languages = [
        Italian(u'San Marino', lcid=None)
    ]


class SaoTomeandPrincipe(Locale):
    _iso_code = 'ST'
    _english_name = 'São Tomé and Príncipe'
    _flag = 'flags\\ST.png'
    languages = [
        Portuguese(u'São Tomé e Príncipe', lcid=None)
    ]


class SaudiArabia(Locale):
    _iso_code = 'SA'
    _english_name = 'Saudi Arabia'
    _flag = 'flags\\SA.png'
    languages = [
        Arabic(u'المملكة العربية السعودية', lcid=0x0401)
    ]


class Senegal(Locale):
    _iso_code = 'SN'
    _english_name = 'Senegal'
    _flag = 'flags\\SN.png'
    languages = [
        French(u'Sénégal', lcid=None),
        Fulah(u'', lcid=0x0867),
        JolaFonyi(u'', lcid=0x1000),
        Wolof(u'', lcid=0x0088)
    ]


class Serbia(Locale):
    _iso_code = 'RS'
    _english_name = 'Serbia'
    _flag = 'flags\\RS.png'
    languages = [
        SerbianCyrillic(u'Србија', lcid=None),
        SerbianLatin(u'Srbija', lcid=0x181A)
    ]


class SerbiaMontenegro(Locale):
    _iso_code = 'CS'
    _english_name = 'Serbia and Montenegro (Former)'
    _flag = None
    languages = [
        SerbianCyrillic(u'', lcid=0x1C1A),
        SerbianLatin(u'', lcid=0x181A)
    ]


class Seychelles(Locale):
    _iso_code = 'SC'
    _english_name = 'Seychelles'
    _flag = 'flags\\SC.png'
    languages = [
        SeychelloisCreole(u'Sesel', lcid=None),
        English(u'Seychelles', lcid=0x1000),
        French(u'Seychelles', lcid=None)
    ]


class SierraLeone(Locale):
    _iso_code = 'SL'
    _english_name = 'Sierra Leone'
    _flag = 'flags\\SL.png'
    languages = [
        English(u'Sierra Leone', lcid=0x1000)
    ]


class Singapore(Locale):
    _iso_code = 'SG'
    _english_name = 'Singapore'
    _flag = 'flags\\SG.png'
    languages = [
        English(u'Singapore', lcid=0x4809),
        Malay(u'Singapura', lcid=None),
        Tamil(u'சிங்கப்பூர்', lcid=None),
        ChineseSimplified(u'新加坡', lcid=0x1004)
    ]


class Slovakia(Locale):
    _iso_code = 'SK'
    _english_name = 'Slovakia'
    _flag = 'flags\\SK.png'
    languages = [
        Slovak(u'Slovensko', lcid=0x041B)
    ]


class Slovenia(Locale):
    _iso_code = 'SI'
    _english_name = 'Slovenia'
    _flag = 'flags\\SI.png'
    languages = [
        Slovenian(u'Slovenija', lcid=0x0424),
        English(u'Slovenia', lcid=0x0009)
    ]


class SolomonIslands(Locale):
    _iso_code = 'SB'
    _english_name = 'Solomon Islands'
    _flag = 'flags\\SB.png'
    languages = [
        English(u'Solomon Islands', lcid=0x1000)
    ]


class Somalia(Locale):
    _iso_code = 'SO'
    _english_name = 'Somalia'
    _flag = 'flags\\SO.png'
    languages = [
        Arabic(u'الصومال', lcid=None),
        Somali(u'Soomaaliya', lcid=None)
    ]


class SouthAfrica(Locale):
    _iso_code = 'ZA'
    _english_name = 'South Africa'
    _flag = 'flags\\ZA.png'
    languages = [
        Afrikaans(u'Suid-Afrika', lcid=0x0436),
        English(u'South Africa', lcid=0x1C09),
        Sotho(u'Afrika Borwa', lcid=None),
        Tswana(u'Aforika Borwa', lcid=0x0432),
        Xhosa(u'uMzantsi Afrika', lcid=0x0434),
        Zulu(u'iNingizimu Afrika', lcid=0x0435),
        SothoNorthern(u'Afrika Borwa', lcid=0x006C),
        SouthNdebele(u'iSewula Afrika', lcid=0x1000),
        Swati(u'iNingizimu Afrika', lcid=0x1000),
        Tsonga(u'Afrika Dzonga', lcid=0x0031),
        Venda(u'Afurika Tshipembe', lcid=0x0033)
    ]


class SouthGeorgiaandtheSouthSandwichIslands(Locale):
    _iso_code = 'GS'
    _english_name = 'South Georgia and the South Sandwich Islands'
    _flag = 'flags\\GS.png'
    languages = [
        English(u'South Georgia and the South Sandwich Islands', lcid=0x1000)
    ]


class SouthKorea(Locale):
    _iso_code = 'KR'
    _english_name = 'South Korea'
    _flag = 'flags\\KR.png'
    languages = [
        English(u'South Korea', lcid=0x1000),
        Korean(u'대한민국', lcid=0x0412)
    ]


class SouthSudan(Locale):
    _iso_code = 'SS'
    _english_name = 'South Sudan'
    _flag = 'flags\\SS.png'
    languages = [
        English(u'South Sudan', lcid=0x1000),
        Arabic(u'', lcid=0x0001)
    ]


class Spain(Locale):
    _iso_code = 'ES'
    _english_name = 'Spain'
    _flag = 'flags\\ES.png'
    languages = [
        Asturian(u'España', lcid=None),
        Catalan(u'Espanya', lcid=0x0403),
        Spanish(u'España', lcid=0x0C0A),
        Basque(u'Espainia', lcid=0x042D),
        Galician(u'España', lcid=0x0456)
    ]


class SriLanka(Locale):
    _iso_code = 'LK'
    _english_name = 'Sri Lanka'
    _flag = 'flags\\LK.png'
    languages = [
        Sinhala(u'ශ්‍රී ලංකාව', lcid=0x045B),
        Tamil(u'இலங்கை', lcid=None)
    ]


class Sudan(Locale):
    _iso_code = 'SD'
    _english_name = 'Sudan'
    _flag = 'flags\\SD.png'
    languages = [
        Arabic(u'السودان', lcid=None),
        English(u'Sudan', lcid=0x1000),
        Nuer(u'', lcid=0x1000)
    ]


class Suriname(Locale):
    _iso_code = 'SR'
    _english_name = 'Suriname'
    _flag = 'flags\\SR.png'
    languages = [
        Dutch(u'Suriname', lcid=None)
    ]


class SvalbardandJanMayen(Locale):
    _iso_code = 'SJ'
    _english_name = 'Svalbard and Jan Mayen'
    _flag = 'flags\\SJ.png'
    languages = [
        Norwegian(u'Svalbard og Jan Mayen', lcid=None),
        NorwegianBokmal(u'', lcid=0x7C14)
    ]


class Swaziland(Locale):
    _iso_code = 'SZ'
    _english_name = 'Swaziland'
    _flag = 'flags\\SZ.png'
    languages = [
        English(u'Swaziland', lcid=0x1000),
        Swati(u'káNgwane', lcid=None)
    ]


class Sweden(Locale):
    _iso_code = 'SE'
    _english_name = 'Sweden'
    _flag = 'flags\\SE.png'
    languages = [
        Swedish(u'Sverige', lcid=0x041D),
        English(u'Sweden', lcid=0x0009),
        SamiLule(u'', lcid=0x7C3B),
        SamiNorthern(u'', lcid=0x003B),
        SamiSouthern(u'', lcid=0x783B)
    ]


class Switzerland(Locale):
    _iso_code = 'CH'
    _english_name = 'Switzerland'
    _flag = 'flags\\CH.png'
    languages = [
        German(u'Schweiz', lcid=0x0807),
        French(u'Suisse', lcid=0x100C),
        Italian(u'Svizzera', lcid=0x0810),
        Romansh(u'Svizra', lcid=0x0417),
        SwissGerman(u'', lcid=0x0084),
        English(u'Switzerland', lcid=0x0009),
        Portuguese(u'', lcid=0x0016),
        Walser(u'', lcid=0x1000)
    ]


class Syria(Locale):
    _iso_code = 'SY'
    _english_name = 'Syria'
    _flag = 'flags\\SY.png'
    languages = [
        Arabic(u'سورية', lcid=0x2801),
        Kurdish(u'Sūriyya', lcid=None),
        French(u'', lcid=0x000C),
        Syriac(u'', lcid=0x005A)
    ]


class Taiwan(Locale):
    _iso_code = 'TW'
    _english_name = 'Taiwan'
    _flag = 'flags\\TW.png'
    languages = [
        ChineseTraditional(u'中華民國', lcid=0x0404)
    ]


class Tajikistan(Locale):
    _iso_code = 'TJ'
    _english_name = 'Tajikistan'
    _flag = 'flags\\TJ.png'
    languages = [
        Russian(u'Таджикистан', lcid=None),
        TajikCyrillic(u'Тоҷикистон', lcid=0x0428)
    ]


class Tanzania(Locale):
    _iso_code = 'TZ'
    _english_name = 'Tanzania'
    _flag = 'flags\\TZ.png'
    languages = [
        English(u'Tanzania', lcid=0x1000),
        Swahili(u'Tanzania', lcid=0x1000),
        Asu(u'', lcid=0x1000),
        Bena(u'', lcid=0x1000),
        Langi(u'', lcid=0x1000),
        Machame(u'', lcid=0x1000),
        Makonde(u'', lcid=0x1000),
        Masai(u'', lcid=0x1000),
        Rombo(u'', lcid=0x1000),
        Rwa(u'', lcid=0x1000),
        Sangu(u'', lcid=0x1000),
        Shambala(u'', lcid=0x1000),
        Vunjo(u'', lcid=0x1000)
    ]


class Thailand(Locale):
    _iso_code = 'TH'
    _english_name = 'Thailand'
    _flag = 'flags\\TH.png'
    languages = [
        Thai(u'เมืองไทย', lcid=0x041E)
    ]


class TheGambia(Locale):
    _iso_code = 'GM'
    _english_name = 'The Gambia'
    _flag = 'flags\\GM.png'
    languages = [
        English(u'The Gambia', lcid=0x1000)
    ]


class TheNetherlands(Locale):
    _iso_code = 'NL'
    _english_name = 'The Netherlands'
    _flag = 'flags\\NL.png'
    languages = [
        Dutch(u'Nederland', lcid=0x0413),
        English(u'The Netherlands', lcid=0x0009),
        Frisian(u'', lcid=0x0062),
        LowGerman(u'', lcid=0x1000)
    ]


class Tifinagh(Locale):
    _iso_code = 'Tfng'
    _english_name = 'Tifinagh'
    _flag = None
    languages = [
        StandardMoroccanTamazight(u'', lcid=0x1000),
        Tachelhit(u'', lcid=0x1000)
    ]


class TimorLeste(Locale):
    _iso_code = 'TL'
    _english_name = 'Timor-Leste'
    _flag = 'flags\\TL.png'
    languages = [
        Portuguese(u'Timor-Leste', lcid=0x1000),
        Tetum(u'Timor Lorosa\'e', lcid=None)
    ]


class Togo(Locale):
    _iso_code = 'TG'
    _english_name = 'Togo'
    _flag = 'flags\\TG.png'
    languages = [
        French(u'Togo', lcid=0x1000),
        Ewe(u'Togo', lcid=0x1000)
    ]


class Tokelau(Locale):
    _iso_code = 'TK'
    _english_name = 'Tokelau'
    _flag = 'flags\\TK.png'
    languages = [
        English(u'Tokelau', lcid=0x1000),
        Samoan(u'Tokelau', lcid=None),
        Tokelauan(u'Tokelau', lcid=None)
    ]


class Tonga(Locale):
    _iso_code = 'TO'
    _english_name = 'Tonga'
    _flag = 'flags\\TO.png'
    languages = [
        English(u'Tonga', lcid=0x1000),
        Tongan(u'Tonga', lcid=0x1000)
    ]


class TrinidadandTobago(Locale):
    _iso_code = 'TT'
    _english_name = 'Trinidad and Tobago'
    _flag = 'flags\\TT.png'
    languages = [
        English(u'Trinidad and Tobago', lcid=0x2C09)
    ]


class Tunisia(Locale):
    _iso_code = 'TN'
    _english_name = 'Tunisia'
    _flag = 'flags\\TN.png'
    languages = [
        Arabic(u'تونس', lcid=0x1C01),
        French(u'Tunisie', lcid=0x1000)
    ]


class Turkey(Locale):
    _iso_code = 'TR'
    _english_name = 'Turkey'
    _flag = 'flags\\TR.png'
    languages = [
        Turkish(u'Türkiye', lcid=0x041F)
    ]


class Turkmenistan(Locale):
    _iso_code = 'TM'
    _english_name = 'Turkmenistan'
    _flag = 'flags\\TM.png'
    languages = [
        Turkmen(u'Türkmenistan', lcid=0x0442)
    ]


class TurksandCaicosIslands(Locale):
    _iso_code = 'TC'
    _english_name = 'Turks and Caicos Islands'
    _flag = 'flags\\TC.png'
    languages = [
        English(u'Turks and Caicos Islands', lcid=0x1000)
    ]


class Tuvalu(Locale):
    _iso_code = 'TV'
    _english_name = 'Tuvalu'
    _flag = 'flags\\TV.png'
    languages = [
        English(u'Tuvalu', lcid=0x1000)
    ]


class Uganda(Locale):
    _iso_code = 'UG'
    _english_name = 'Uganda'
    _flag = 'flags\\UG.png'
    languages = [
        English(u'Uganda', lcid=0x1000),
        Swahili(u'Uganda', lcid=0x1000),
        Chiga(u'', lcid=0x1000),
        Ganda(u'', lcid=0x1000),
        Nyankole(u'', lcid=0x1000),
        Soga(u'', lcid=0x1000),
        Teso(u'', lcid=0x1000)
    ]


class Ukraine(Locale):
    _iso_code = 'UA'
    _english_name = 'Ukraine'
    _flag = 'flags\\UA.png'
    languages = [
        Ukrainian(u'Україна', lcid=0x0422),
        Russian(u'', lcid=0x0019)
    ]


class UnitedArabEmirates(Locale):
    _iso_code = 'AE'
    _english_name = 'United Arab Emirates'
    _flag = 'flags\\AE.png'
    languages = [
        Arabic(u'الإمارات العربيّة المتّحدة', lcid=0x3801),
        Azerbaijani(u'Birləşmiş Ərəb Əmirlikləri', lcid=None)
    ]


class UnitedKingdom(Locale):
    _iso_code = 'GB'
    _english_name = 'United Kingdom'
    _flag = 'flags\\GB.png'
    languages = [
        Welsh(u'Y Deyrnas Unedig', lcid=0x0452),
        English(u'United Kingdom', lcid=0x0809),
        Irish(u'Ríocht Aontaithe', lcid=None),
        ScottishGaelic(u'Rìoghachd Aonaichte', lcid=0x0491),
        Cornish(u'An Rywvaneth Unys', lcid=0x1000)
    ]


class UnitedStatesMinorOutlyingIslands(Locale):
    _iso_code = 'UM'
    _english_name = 'United States Minor Outlying Islands'
    _flag = 'flags\\UM.png'
    languages = [
        English(u'United States Minor Outlying Islands', lcid=0x1000)
    ]


class UnitedStatesVirginIslands(Locale):
    _iso_code = 'VI'
    _english_name = 'United States Virgin Islands'
    _flag = 'flags\\VI.png'
    languages = [
        English(u'United States Virgin Islands', lcid=0x1000)
    ]


class UnitedStatesofAmerica(Locale):
    _iso_code = 'US'
    _english_name = 'United States of America'
    _flag = 'flags\\US.png'
    languages = [
        English(u'United States of America', lcid=0x0409),
        Cherokee(u'', lcid=0x045C),
        Hawaiian(u'‘Amelika Hui Pū ‘la', lcid=0x0075),
        Lakota(u'', lcid=0x1000),
        Spanish(u'Estados Unidos', lcid=0x000A)
    ]


class Uruguay(Locale):
    _iso_code = 'UY'
    _english_name = 'Uruguay'
    _flag = 'flags\\UY.png'
    languages = [
        Spanish(u'Uruguay', lcid=0x380A)
    ]


class Uzbekistan(Locale):
    _iso_code = 'UZ'
    _english_name = 'Uzbekistan'
    _flag = 'flags\\UZ.png'
    languages = [
        KaraKalpak(u'O\'zbekstan', lcid=None),
        UzbekLatin(u'O\'zbekiston', lcid=0x0443),
        UzbekCyrillic(u'Ўзбекистон', lcid=0x0843)
    ]


class Vanuatu(Locale):
    _iso_code = 'VU'
    _english_name = 'Vanuatu'
    _flag = 'flags\\VU.png'
    languages = [
        Bislama(u'Vanuatu', lcid=None),
        English(u'Vanuatu', lcid=0x1000),
        French(u'Vanuatu', lcid=0x1000)
    ]


class Venezuela(Locale):
    _iso_code = 'VE'
    _english_name = 'Venezuela'
    _flag = 'flags\\VE.png'
    languages = [
        Spanish(u'Venezuela', lcid=0x200A)
    ]


class Vietnam(Locale):
    _iso_code = 'VN'
    _english_name = 'Vietnam'
    _flag = 'flags\\VN.png'
    languages = [
        Vietnamese(u'Việt Nam', lcid=0x042A)
    ]


class WallisandFutuna(Locale):
    _iso_code = 'WF'
    _english_name = 'Wallis and Futuna'
    _flag = 'flags\\WF.png'
    languages = [
        French(u'Wallis-et-Futuna', lcid=0x1000)
    ]


class WesternSahara(Locale):
    _iso_code = 'EH'
    _english_name = 'Western Sahara'
    _flag = 'flags\\EH.png'
    languages = [
        Arabic(u'الصحراء الغربية', lcid=None),
        Spanish(u'Sahara Occidental', lcid=None),
        French(u'Sahara occidental', lcid=None)
    ]


class World(Locale):
    _iso_code = '001'
    _english_name = 'World'
    _flag = None
    languages = [
        Arabic(u'', lcid=0x0001),
        English(u'World', lcid=0x0009),
        Esperanto(u'', lcid=0x1000),
        Interlingua(u'', lcid=0x1000),
        Volapuk(u'', lcid=0x1000)
    ]


class Yemen(Locale):
    _iso_code = 'YE'
    _english_name = 'Yemen'
    _flag = 'flags\\YE.png'
    languages = [
        Arabic(u'اليمن', lcid=0x2401)
    ]


class Zambia(Locale):
    _iso_code = 'ZM'
    _english_name = 'Zambia'
    _flag = 'flags\\ZM.png'
    languages = [
        English(u'Zambia', lcid=0x1000),
        Bemba(u'Zambia', lcid=0x1000)
    ]


class Zimbabwe(Locale):
    _iso_code = 'ZW'
    _english_name = 'Zimbabwe'
    _flag = 'flags\\ZW.png'
    languages = [
        English(u'Zimbabwe', lcid=0x3009),
        NorthNdebele(u'Zimbabwe', lcid=0x1000),
        Shona(u'Zimbabwe', lcid=0x1000)
    ]


if __name__ == '__main__':
    wx_count = 0
    print('Supported Locals and Languages')
    print('_' * 40)

    def convert_lcid():
        lcd = hex(lng.lcid)[2:].upper().replace('L', '')

        while len(lcd) < 4:
            lcd = '0' + lcd

        return '0x' + lcd

    for locl in locales:
        print(locl.english_name, '-', locl.locale_iso_code)
        for lng in locl:
            print('    English language name:', lng.english_name)
            print('    English locale name:', lng.english_locale_name)
            print('        Language name:', lng.name)
            print('        Locale name: ', lng.locale_name)
            print('        Label:', lng.label)
            print('        Native language name:', lng.native_name)
            print('        Native locale name: ', lng.native_locale_name)
            print('        Native label: ', lng.native_label)
            print('        Ansi code page:', lng.ansi_code_page)
            print('        Code page:', lng.code_page)
            print('        Windows LCID:', convert_lcid())

            if lng.wx_code is not None:
                wx_count += 1

    print('\n', '-' * 40, '\n')
    lng = get_windows_user_language()
    print(
        'Current Windows user locale:',
        lng.locale_name,
        '-',
        lng.locale.locale_iso_code
    )
    print('Current Windows user language:', lng.name, '-', lng.lang_iso_code)
    print('Locale native name:', lng.native_locale_name)
    print('Language native name:', lng.native_name)
    print('ISO code:', lng.iso_code)
    print('Ansi code page:', lng.ansi_code_page)
    print('Code page:', lng.code_page)
    print('Windows LCID:', convert_lcid())

    print('\n', '-' * 40, '\n')

    print('Total country count:', locales.total_countries)
    print('Total supported country count:', locales.total_supported_countries)
    print()
    print('Total language count:', locales.total_languages)
    print('Total supported language count:', locales.total_supported_languages)
    print()
    print('Total locale count:', locales.total_locales)
    print('Total supported locale count:', locales.total_supported_locales)
    print()
    print('Total wx locale count:', len(list(LCID_TO_WX.keys())))
    print('Total supported wx locale count:', wx_count)
    print()
    print('Set locale results:', lng.set_locale())

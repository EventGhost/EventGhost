# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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

import wx


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

class Translation:
    languageNames = {
        'aa_AA': u'Afar',
        'ab_AB': u'Abkhazian',
        'af_AF': u'Afrikaans',
        'am_AM': u'አማርኛ',
        'ar_AE': u'العربية - الامارات العربية المتحدة',
        'ar_AR': u'Arabic',
        'ar_BH': u'العربية - البحرين',
        'ar_DZ': u'العربية - الجزائر',
        'ar_EG': u'اللغة العربية - مصر',
        'ar_IQ': u'عربي - العراق',
        'ar_JO': u'عربي - الاردن',
        'ar_KW': u'العربية - الكويت',
        'ar_LB': u'العربية - لبنان',
        'ar_LY': u'العربية - ليبيا',
        'ar_MA': u'اللغة العربية - المغرب',
        'ar_OM': u'العربية - عمان',
        'ar_QA': u'العربية - قطر',
        'ar_SA': u'العربية - السعودية',
        'ar_SY': u'العربية - سوريا',
        'ar_TN': u'العربية - تونس',
        'ar_YE': u'العربية - اليمن',
        'as_AS': u'Assamese',
        'ay_AY': u'Aymara',
        'az_AZ': u'Azeri - Latin',
        'ba_BA': u'Bashkir',
        'be_BE': u'беларускі',
        'bg_BG': u'български',
        'bh_BH': u'Bihari',
        'bi_BI': u'Bislama',
        'bn_BN': u'Bengali',
        'bo_BO': u'Tibetan',
        'br_BR': u'Breton',
        'bs_BS': u'Bosanski',
        'ca_CA': u'Català',
        'co_CO': u'Corsican',
        'cs_CS': u'čeština',
        'cy_CY': u'Cymraeg',
        'da_DA': u'dansk',
        'de_AT': u'Deutsch - Österreich',
        'de_CH': u'Deutsch - Schweiz',
        'de_DE': u'Deutschland',
        'de_LI': u'Deutsch - Liechtenstein',
        'de_LU': u'Deutsch - Luxemburg',
        'dv_DV': u'Divehi; Dhivehi; Maldivian',
        'dz_DZ': u'Bhutani',
        'el_EL': u'Ελληνικά',
        'en_AU': u'English - Australia',
        'en_BZ': u'English - Belize',
        'en_CA': u'English - Canada',
        'en_CB': u'English - Caribbean',
        'en_EN': u'English',
        'en_GB': u'English - Great Britain',
        'en_IE': u'English - Ireland',
        'en_IN': u'English - India',
        'en_JM': u'English - Jamaica',
        'en_NZ': u'English - New Zealand',
        'en_PH': u'English - Phillippines',
        'en_TT': u'English - Trinidad',
        'en_US': u'English - United States',
        'en_ZA': u'English - Southern Africa',
        'eo_EO': u'Esperanto',
        'es_AR': u'Español - argentina',
        'es_BO': u'Español - bolivia',
        'es_CL': u'Español - chile',
        'es_CO': u'Español - colombia',
        'es_CR': u'Español - costa rica',
        'es_DO': u'Español - republica dominicana',
        'es_EC': u'Español - ecuador',
        'es_ES': u'Español - españa (tradicional)',
        'es_GT': u'Español - guatemala',
        'es_HN': u'Español - honduras',
        'es_MX': u'Español - mexico',
        'es_NI': u'Español - nicaragua',
        'es_PA': u'Español - panama',
        'es_PE': u'Español - peru',
        'es_PR': u'Español - puerto rico',
        'es_PY': u'Español - paraguay',
        'es_SV': u'Español - el salvador',
        'es_UY': u'Español - uruguay',
        'es_VE': u'Español - venezuela',
        'et_ET': u'Eesti keel',
        'eu_EU': u'Euskal',
        'fa_FA': u'فارسی - فارسی',
        'fi_FI': u'Suomalainen',
        'fj_FJ': u'Fiji',
        'fo_FO': u'føroyskt',
        'fr_BE': u'Français - Belgique',
        'fr_CA': u'Français - Canada',
        'fr_CH': u'Français - Suisse',
        'fr_FR': u'France francaise',
        'fr_LU': u'Français - Luxembourg',
        'fy_FY': u'Frisian',
        'ga_GA': u'Irish',
        'gd_GD': u'Gàidhlig - Alba',
        'gd_IE': u'Gàidhlig - Èirinn',
        'gl_GL': u'Galician',
        'gn_GN': u'Guarani - Paraguay',
        'gu_GU': u'ગુજરાતી',
        'ha_HA': u'Hausa',
        'he_HE': u'עברית',
        'hi_HI': u'हिंदी',
        'hr_HR': u'Hrvatski',
        'hu_HU': u'Magyar',
        'hy_HY': u'հայերեն',
        'ia_IA': u'Interlingua',
        'id_ID': u'bahasa Indonesia',
        'ie_IE': u'Interlingue',
        'ik_IK': u'Inupiak',
        'in_IN': u'Indonesian',
        'is_IS': u'Íslensku',
        'it_CH': u'Italiano - Svizzera',
        'it_IT': u'Italiano - Italia',
        'iw_IW': u'Hebrew',
        'ja_JA': u'日本人',
        'ji_JI': u'ייִדיש',
        'jw_JW': u'Javanese',
        'ka_KA': u'Georgian',
        'kk_KK': u'Қазақша',
        'kl_KL': u'Greenlandic',
        'km_KM': u'ភាសាខ្មែរ',
        'kn_KN': u'ಕನ್ನಡ',
        'ko_KO': u'한국어',
        'ks_KS': u'Kashmiri',
        'ku_KU': u'Kurdish',
        'ky_KY': u'Kirghiz',
        'la_LA': u'Latine',
        'ln_LN': u'Lingala',
        'lo_LO': u'ລາວ',
        'lt_LT': u'Lietuviškai',
        'lv_LV': u'Latviešu',
        'mg_MG': u'Malagasy',
        'mi_MI': u'Maori',
        'mk_MK': u'БЈР Македонија',
        'ml_ML': u'മലയാളം',
        'mn_MN': u'Монгол хэл',
        'mo_MO': u'Moldavian',
        'mr_MR': u'मराठी',
        'ms_BN': u'Malay - Brunei',
        'ms_MS': u'Malay',
        'ms_MY': u'Malay - Malaysia',
        'mt_MT': u'Malti',
        'my_MY': u'Burmese',
        'na_NA': u'Nauru',
        'ne_NE': u'नेपाली',
        'nl_NL': u'Nederlands',
        'no_NO': u'Norwegian - Nynorsk',
        'oc_OC': u'Occitan',
        'om_OM': u'Oromo/Afan',
        'or_OR': u'Oriya',
        'pa_PA': u'ਪੰਜਾਬੀ',
        'pl_PL': u'Polskie',
        'ps_PS': u'Pashto/Pushto',
        'pt_BR': u'Português - Brasil',
        'pt_PT': u'Português - portugal',
        'qu_QU': u'Quechua',
        'rm_RM': u'Raeto-Romance',
        'rn_RN': u'Kirundi',
        'ro_MO': u'Romanian - Moldova',
        'ro_RO': u'Romanian - Romania',
        'ru_MO': u'Россия - Молдова',
        'ru_RU': u'русский',
        'rw_RW': u'Kinyarwanda',
        'sa_SA': u'Sanskrit',
        'sb_SB': u'Sorbian',
        'sd_SD': u'سنڌي',
        'sg_SG': u'Sangro',
        'sh_SH': u'Serbo-Croatian',
        'si_SI': u'සිංහල',
        'sk_SK': u'slovenský',
        'sl_SL': u'Slovenščina',
        'sm_SM': u'Samoan',
        'sn_SN': u'Shona',
        'so_SO': u'Somali',
        'sq_SQ': u'shqiptar',
        'sr_SP': u'Serbian - Latin',
        'sr_SR': u'Serbian',
        'ss_SS': u'Siswati',
        'st_ST': u'Sesotho',
        'su_SU': u'Sudanese',
        'sv_FI': u'Svenska - finska',
        'sv_SE': u'Svenska - sverige',
        'sv_SV': u'Swedish',
        'sw_SW': u'Kiswahili',
        'ta_TA': u'தமிழ்',
        'te_TE': u'తెలుగు',
        'tg_TG': u'Тоҷикӣ',
        'th_TH': u'ไทย',
        'ti_TI': u'Tigrinya',
        'tk_TK': u'Turkmen',
        'tl_TL': u'Tagalog',
        'tn_TN': u'Setsuana',
        'to_TO': u'Tonga',
        'tr_TR': u'Türk',
        'ts_TS': u'Tsonga',
        'tt_TT': u'Tatar',
        'tw_TW': u'Twi',
        'uk_UK': u'Українська',
        'ur_UR': u'اردو',
        'uz_UZ': u'Uzbecorum - Latina',
        'vi_VI': u'Tiếng Việt',
        'vo_VO': u'Volapuk',
        'wo_WO': u'Wolof',
        'xh_XH': u'IsiXhosa',
        'yo_YO': u'Yorùbá',
        'zh_HK': u'中國 - 香港特別行政區',
        'zh_MO': u'中國 - 澳門特區',
        'zh_SG': u'中文 - 新加坡',
        'zh_TW': u'中文 - 台灣',
        'zh_ZH': u'Chinese',
        'zu_ZU': u'Zulu',
    }

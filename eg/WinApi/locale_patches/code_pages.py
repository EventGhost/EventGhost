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
    65001: 'utf-8'
}

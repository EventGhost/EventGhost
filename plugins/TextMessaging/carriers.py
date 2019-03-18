# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright Â© 2005-2016 EventGhost Project <http://www.eventghost.org/>
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


CARRIERS = {
    'Argentina': {
        'Claro': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.ctimovil.com.ar'],
        },
        'Movistar': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.movistar.net.ar'],
        },
        'Nextel': {
            'flags': ['SMS'],
            'format': ['TwoWay.11~~NUMBER~~'],
            'gateway': ['nextel.net.ar'],
        },
        'Personal': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['alertas.personal.com.ar'],
        }
    },
    'Aruba': {
        'Setar Mobile email ()': {
            'flags': ['SMS'],
            'format': ['297~~NUMBER~~'],
            'gateway': ['mas.aw'],
        }
    },
    'Australia': {
        'Esendex': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['echoemail.net'],
        },
        'T-Mobile (Optus Zoo)': {
            'flags': ['SMS'],
            'format': ['0~~NUMBER~~'],
            'gateway': ['optusmobile.com.au'],
        },
        'Telstra Integrated Messaging (powered by Soprano)': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['tim.telstra.com'],
        }
    },
    'Austria': {
        'Api4SMS': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['members.api4sms.net'],
        },
        'One Connect': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['onemail.at', 'onemail.at'],
        },
        'T-Mobile': {
            'flags': ['SMS'],
            'format': ['43676~~NUMBER~~'],
            'gateway': ['sms.t-mobile.at'],
        }
    },
    'Belgium': {
        'Mobistar': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mobistar.be', 'mobistar.be'],
        }
    },
    'Bermuda': {
        'Mobility': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['ml.bm', 'ml.bm'],
        }
    },
    'Brazil': {
        'Claro': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['clarotorpedo.com.br'],
        },
        'Nextel': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['nextel.com.br', 'nextel.com.br'],
        },
        'Vivo': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['torpedoemail.com.br'],
        }
    },
    'Bulgaria': {
        'Globul': {
            'flags': ['SMS'],
            'format': ['35989~~NUMBER~~'],
            'gateway': ['sms.globul.bg'],
        },
        'Mobiltel': {
            'flags': ['SMS'],
            'format': ['35988~~NUMBER~~'],
            'gateway': ['sms.mtel.net'],
        }
    },
    'Canada': {
        'Aliant': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.wirefree.informe.ca'],
        },
        'Bell': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['bellmobility.ca', 'bellmobility.ca'],
        },
        'Bell Mobility': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['txt.bell.ca'],
        },
        'Bell Mobility & Solo Mobile': {
            'flags': ['SMS', 'SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'txt.bell.ca',
                'txt.bellmobility.ca',
                'txt.bellmobility.ca'
            ],
        },
        'Fido': {
            'flags': ['SMS', 'SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['sms.fido.ca', 'fido.ca', 'fido.ca'],
        },
        'Koodo Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['msg.telus.com'],
        },
        'Lynx Mobility': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.lynxmobility.com'],
        },
        'MTS Mobility': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['text.mtsmobility.com'],
        },
        'Microcell': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['fido.ca', 'fido.ca'],
        },
        'NBTel': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['wirefree.informe.ca', 'wirefree.informe.ca'],
        },
        'PC Telecom': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['mobiletxt.ca'],
        },
        'PageMart': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pmcl.net', 'pmcl.net'],
        },
        'PageNet': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pagegate.pagenet.ca', 'pagegate.pagenet.ca'],
        },
        "President's Choice": {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['txt.bell.ca'],
        },
        'Rogers Wireless': {
            'flags': ['SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pcs.rogers.com', 'sms.rogers.com'],
        },
        'SaskTel': {
            'flags': ['SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pcs.sasktelmobility.com', 'sms.sasktel.com'],
        },
        'Solo Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['txt.bell.ca'],
        },
        'Telus Mobility': {
            'flags': ['MMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['mms.telusmobility.com'],
        },
        'Virgin Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['vmobile.ca'],
        },
        'Westnet': {
            'flags': ['MMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['t.westnet.ca'],
        },
        'Wind Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['txt.windmobile.ca'],
        }
    },
    'China': {
        'Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['139.com'],
        }
    },
    'Colombia': {
        'Claro': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['iclaro.com.co'],
        },
        'Movistar': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['movistar.com.co'],
        },
        'Tigo (Formerly Ola)': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.tigo.com.co'],
        }
    },
    'Costa Rica': {
        'ICE': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.ice.cr'],
        }
    },
    'Croatia': {
        'T-Mobile': {
            'flags': ['SMS'],
            'format': ['385~~NUMBER~~'],
            'gateway': ['sms.t-mobile.hr'],
        }
    },
    'Czech Republic': {
        'Oskar': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mujoskar.cz', 'mujoskar.cz'],
        },
        'Vodafone': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['vodafonemail.cz'],
        }
    },
    'Denmark': {
        'Telia': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['gsm1800.telia.dk', 'gsm1800.telia.dk'],
        }
    },
    'Dominica': {
        'Digicel ()': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['digitextdm.com'],
        }
    },
    'Estonia': {
        'EMT': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.emt.ee'],
        }
    },
    'Europe': {
        'Freebie SMS': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['smssturen.com'],
        },
        'TellusTalk': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['esms.nu'],
        }
    },
    'France': {
        'Bouygues Telecom (company)': {
            'flags': ['MMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['mms.bouyguestelecom.fr'],
        },
        'SFR': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sfr.fr'],
        }
    },
    'Germany': {
        'E-Plus': {
            'flags': ['SMS'],
            'format': ['0~~NUMBER~~'],
            'gateway': ['smsmail.eplus.de'],
        },
        'O2': {
            'flags': ['SMS'],
            'format': ['0~~NUMBER~~'],
            'gateway': ['o2online.de'],
        },
        'T-Mobile': {
            'flags': ['SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['t-mobile-sms.de', 't-d1-sms.de'],
        },
        'Vodafone': {
            'flags': ['SMS'],
            'format': ['0~~NUMBER~~'],
            'gateway': ['vodafone-sms.de'],
        }
    },
    'Guyana': {
        'Telephone &Telegraph;': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.cellinkgy.com'],
        }
    },
    'Hong Kong': {
        'Accessyou': {
            'flags': ['MMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['messaging.accessyou.com'],
        },
        'CSL': {
            'flags': ['MMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['mgw.mmsc1.hkcsl.com'],
        }
    },
    'Iceland': {
        'OgVodafone': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.is'],
        },
        'Siminn': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['box.is'],
        }
    },
    'India': {
        'Aircel': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['aircel.co.in'],
        },
        'Airtel': {
            'flags': ['SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['airtelap.com', 'airtelkk.com'],
        },
        'Andhra Pradesh Idea Cellular': {
            'flags': ['SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['ideacellular.net', 'ideacellular.net'],
        },
        'B2Bsms B2B SMS': {
            'flags': ['SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['b2bsms.co.in', 'b2bsms.co.in or'],
        },
        'Chennai RPG Cellular': {
            'flags': ['SMS'],
            'format': ['9841~~NUMBER~~'],
            'gateway': ['rpgmail.net'],
        },
        'Chennai Skycell / Airtel': {
            'flags': ['SMS'],
            'format': ['919840~~NUMBER~~'],
            'gateway': ['airtelchennai.com'],
        },
        'Delhi Airtel': {
            'flags': ['SMS'],
            'format': ['919810~~NUMBER~~'],
            'gateway': ['airtelmail.com'],
        },
        'Delhi Hutch': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['delhi.hutch.co.in', 'delhi.hutch.co.in'],
        },
        'Gujarat Celforce / Fascel': {
            'flags': ['SMS'],
            'format': ['9825~~NUMBER~~'],
            'gateway': ['celforce.com'],
        },
        'Haryana Escotel': {
            'flags': ['SMS', 'SMS', 'SMS'],
            'format': ['9812~~NUMBER~~', '9812~~NUMBER~~', '9812~~NUMBER~~'],
            'gateway': [
                'escotelmobile.com',
                'escotelmobile.com',
                'escotelmobile.com'
            ],
        },
        'Karnataka Airtel': {
            'flags': ['SMS'],
            'format': ['919845~~NUMBER~~'],
            'gateway': ['airtelkk.com'],
        },
        'Kerala Airtel': {
            'flags': ['SMS'],
            'format': ['919895~~NUMBER~~'],
            'gateway': ['airtelkerala.com'],
        },
        'Kolkata Airtel': {
            'flags': ['SMS'],
            'format': ['919831~~NUMBER~~'],
            'gateway': ['airtelkol.com'],
        },
        'Mumbai Orange': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['orangemail.co.in', 'orangemail.co.in'],
        },
        'Orange Mumbai': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['orangemail.co.in', 'orangemail.co.in'],
        },
        'Tamil Nadu Aircel': {
            'flags': ['SMS'],
            'format': ['9842~~NUMBER~~'],
            'gateway': ['airsms.com'],
        },
        'Tamil Nadu Airtel': {
            'flags': ['SMS'],
            'format': ['919894~~NUMBER~~'],
            'gateway': ['airtelmobile.com'],
        }
    },
    'International': {
        'All Carrier': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['email.experttexting.com'],
        },
        'Globalstar (satellite)': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['msg.globalstarusa.com'],
        },
        'Google Fi': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['msg.fi.google.com'],
        },
        'Iridium (satellite)': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['msg.iridium.com'],
        },
        'RoutoMessaging': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['email2sms.routomessaging.com'],
        }
    },
    'Ireland': {
        'Meteor': {
            'flags': ['MMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mms.mymeteor.ie', 'sms.mymeteor.ie'],
        }
    },
    'Israel': {
        'Spikko': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['SpikkoSMS.com'],
        }
    },
    'Italy': {
        'TIM': {
            'flags': ['SMS'],
            'format': ['0~~NUMBER~~'],
            'gateway': ['timnet.com'],
        },
        'Vodafone': {
            'flags': ['SMS'],
            'format': ['3**~~NUMBER~~'],
            'gateway': ['sms.vodafone.it'],
        }
    },
    'Japan': {
        'Vodafone': {
            'flags': ['SMS', 'MMS', 'SMS', 'MMS', 'SMS', 'MMS'],
            'format': [
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~'
            ],
            'gateway': [
                't.vodafone.ne.jp',
                't.vodafone.ne.jp',
                'h.vodafone.ne.jp',
                'h.vodafone.ne.jp',
                'c.vodafone.ne.jp',
                'c.vodafone.ne.jp'
            ],
        }
    },
    'Latvia': {
        'Kyivstar': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['smsmail.lmt.lv'],
        },
        'LMT': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['smsmail.lmt.lv'],
        },
        'Tele2': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.tele2.lv'],
        }
    },
    'Luxembourg': {
        'P&T': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.luxgsm.lu'],
        }
    },
    'Mauritius': {
        'Emtel': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['emtelworld.net'],
        }
    },
    'Mexico': {
        'Nextel': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['msgnextel.com.mx'],
        },
        'Telcel': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['itelcel.com'],
        }
    },
    'Nepal': {
        'Ncell(Previously Mero Mobile)[14]': {
            'flags': ['SMS'],
            'format': ['977~~NUMBER~~'],
            'gateway': ['sms.ncell.com.np'],
        }
    },
    'Netherlands': {
        'Orange': {
            'flags': ['SMS', 'SMS'],
            'format': ['0~~NUMBER~~', '0~~NUMBER~~'],
            'gateway': ['sms.orange.nl', 'sms.orange.nl'],
        },
        'T-Mobile': {
            'flags': ['SMS'],
            'format': ['31~~NUMBER~~'],
            'gateway': ['gin.nl'],
        }
    },
    'New Zealand': {
        'Spark': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['etxt.co.nz'],
        },
        'Vodafone': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['mtxt.co.nz'],
        }
    },
    'Nicaragua': {
        'Claro': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['ideasclaro-ca.com'],
        }
    },
    'Norway': {
        'Netcom': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.netcom.no'],
        },
        'Sendega': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sendega.com'],
        },
        'Telenor': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mobilpost.no', 'mobilpost.no'],
        },
        'TeletopiaSMS': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.teletopiasms.no'],
        }
    },
    'Panama': {
        'Mas Movil': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['cwmovil.com'],
        }
    },
    'Philippines': {
        'Smart Telecom': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mysmart.mymobile.ph', 'mysmart.mymobile.ph'],
        }
    },
    'Poland': {
        'Plus': {
            'flags': ['SMS'],
            'format': ['+48~~NUMBER~~'],
            'gateway': ['text.plusgsm.pl'],
        }
    },
    'Puerto Rico': {
        'Claro': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['vtexto.com'],
        }
    },
    'Russia': {
        'Beeline ()': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.beemail.ru'],
        },
        'Primtel': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.primtel.ru'],
        },
        'SCS-900': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['scs-900.ru', 'scs-900.ru'],
        },
        'Uraltel': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.uraltel.ru'],
        },
        'Vessotel': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pager.irkutsk.ru', 'pager.irkutsk.ru'],
        }
    },
    'SFR Yugoslavia FR Yugoslavia': {
        'Mobtel Srbija': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mobtel.co.yu', 'mobtel.co.yu'],
        }
    },
    'Singapore': {
        'M1': {
            'flags': ['SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['m1.com.sg', 'm1.com.sg'],
        },
        'Starhub Enterprise Messaging Solution': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['starhub-enterprisemessaging.com'],
        }
    },
    'South Africa': {
        'MTN': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.co.za'],
        },
        'Vodacom': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['voda.co.za'],
        }
    },
    'South Korea': {
        'Helio': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['myhelio.com'],
        }
    },
    'Spain': {
        'Altiria': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['altiria.com'],
        },
        'Esendex': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['esendex.net'],
        },
        'Movistar': {
            'flags': ['SMS'],
            'format': ['0~~NUMBER~~'],
            'gateway': ['movistar.net'],
        },
        'Vodafone': {
            'flags': ['SMS'],
            'format': ['0~~NUMBER~~'],
            'gateway': ['vodafone.es'],
        }
    },
    'Spain and Latin America': {
        'Movistar': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['movimensaje.com.ar'],
        }
    },
    'Sri Lanka': {
        'Mobitel': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.mobitel.lk'],
        }
    },
    'Sweden': {
        'Comviq': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.comviq.se'],
        },
        'Tele2': {
            'flags': ['SMS'],
            'format': ['0~~NUMBER~~'],
            'gateway': ['sms.tele2.se'],
        }
    },
    'Switzerland': {
        'Box Internet ServicesSMS Gateway': {
            'flags': ['MMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mms.boxis.net', 'sms.boxis.net'],
        },
        'Sunrise Communications': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['gsm.sunrise.ch'],
        },
        'Sunrise Mobile': {
            'flags': ['SMS', 'MMS', 'SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'mysunrise.ch',
                'mysunrise.ch',
                'freesurf.ch',
                'freesurf.ch'
            ],
        },
        'Swisscom': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['bluewin.ch', 'bluewin.ch'],
        }
    },
    'Tanzania': {
        'Mobitel': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['sms.co.tz', 'sms.co.tz'],
        }
    },
    'UNKNOWN': {
        '3 River Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.3rivers.net'],
        },
        'A1 Telekom': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['a1.net', 'a1.net'],
        },
        'Advantage Communications': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['advantagepaging.com', 'advantagepaging.com'],
        },
        'Airtouch Pagers': {
            'flags': ['SMS', 'MMS', 'SMS', 'MMS', 'SMS', 'MMS', 'SMS', 'MMS'],
            'format': [
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~'
            ],
            'gateway': [
                'alphapage.airtouch.com',
                'alphapage.airtouch.com',
                'myairmail.com',
                'myairmail.com',
                'airtouch.net',
                'airtouch.net',
                'airtouchpaging.com',
                'airtouchpaging.com'
            ],
        },
        'AlphNow': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['alphanow.net', 'alphanow.net'],
        },
        'Arch Pagers (PageNet)': {
            'flags': ['SMS', 'MMS', 'SMS', 'MMS', 'SMS', 'MMS'],
            'format': [
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~'
            ],
            'gateway': [
                'archwireless.net',
                'archwireless.net',
                'archwireless.net',
                'archwireless.net',
                'epage.arch.com',
                'epage.arch.com'
            ],
        },
        'BPL mobile': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['bplmobile.com', 'bplmobile.com'],
        },
        'Beepwear': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['beepwear.net', 'beepwear.net'],
        },
        'Blue Sky Frog': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['blueskyfrog.com', 'blueskyfrog.com'],
        },
        'Central Vermont Communications': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['cvcpaging.com', 'cvcpaging.com'],
        },
        'CenturyTel': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'messaging.centurytel.net',
                'messaging.centurytel.net'
            ],
        },
        'Clearnet': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['msg.clearnet.com', 'msg.clearnet.com'],
        },
        'Communication Specialists': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pageme.comspeco.net', 'pageme.comspeco.net'],
        },
        'Cook Paging': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['cookmail.com', 'cookmail.com'],
        },
        'Corr Wireless Communications': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['corrwireless.net', 'corrwireless.net'],
        },
        'Digi-Page / Page Kansas': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['page.hit.net', 'page.hit.net'],
        },
        'Dobson Cellular Systems': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mobile.dobson.net', 'mobile.dobson.net'],
        },
        'Dobson-Alex / Dobson-Cellular': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mobile.cellularone.com', 'mobile.cellularone.com'],
        },
        'GTE': {
            'flags': ['SMS', 'MMS', 'SMS', 'MMS', 'SMS', 'MMS'],
            'format': [
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~'
            ],
            'gateway': [
                'gte.pagegate.net',
                'gte.pagegate.net',
                'messagealert.com',
                'messagealert.com',
                'airmessage.net',
                'airmessage.net'
            ],
        },
        'Galaxy Corporation': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['sendabeep.net', 'sendabeep.net'],
        },
        'Goa BPLMobil': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['bplmobile.com', 'bplmobile.com'],
        },
        'Golden Telecom': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.goldentele.com'],
        },
        'GrayLink / Porta-Phone': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['epage.porta-phone.com', 'epage.porta-phone.com'],
        },
        'IN Mumbai BPL Mobile': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['bplmobile.com', 'bplmobile.com'],
        },
        'Illinois Valley Cellular': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['ivctext.com'],
        },
        'Infopage Systems': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'page.infopagesystems.com',
                'page.infopagesystems.com'
            ],
        },
        'Inland Cellular Telephone': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['inlandlink.com', 'inlandlink.com'],
        },
        'JSM Tele-Page': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['jsmtel.com', 'jsmtel.com'],
        },
        'Lauttamus Communication': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['e-page.net', 'e-page.net'],
        },
        'MCI': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pagemci.com', 'pagemci.com'],
        },
        'MCI Phone': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mci.com', 'mci.com'],
        },
        'Maharashtra BPL Mobile': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['bplmobile.com', 'bplmobile.com'],
        },
        'Metrocall': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['page.metrocall.com', 'page.metrocall.com'],
        },
        'Metrocall 2-way': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['my2way.com', 'my2way.com'],
        },
        'Mobilecom Pager': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['page.mobilcom.net', 'page.mobilcom.net'],
        },
        'Mobilecomm': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mobilecomm.net', 'mobilecomm.net'],
        },
        'Mobilfone': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['page.mobilfone.com', 'page.mobilfone.com'],
        },
        'Morris Wireless': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['beepone.net', 'beepone.net'],
        },
        'Motient': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['isp.com', 'isp.com'],
        },
        'Movistar': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['correo.movistar.net', 'correo.movistar.net'],
        },
        'NPI Wireless': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['npiwireless.com', 'npiwireless.com'],
        },
        'Omnipoint': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['omnipoint.com', 'omnipoint.com'],
        },
        'Omnipoint PCS': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['omnipointpcs.com', 'omnipointpcs.com'],
        },
        'OnlineBeep': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['onlinebeep.net', 'onlinebeep.net'],
        },
        'PCS One': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pcsone.net', 'pcsone.net'],
        },
        'PageMart': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pagemart.net', 'pagemart.net'],
        },
        'PageMart Advanced /2way': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['airmessage.net', 'airmessage.net'],
        },
        'Pioneer / Enid Cellular': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'msg.pioneerenidcellular.com',
                'msg.pioneerenidcellular.com'
            ],
        },
        'Pondicherry BPL Mobile': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['bplmobile.com', 'bplmobile.com'],
        },
        'Powertel': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['voicestream.net', 'voicestream.net'],
        },
        'Price Communications': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mobilecell1se.com', 'mobilecell1se.com'],
        },
        'Primco': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['textmsg.com'],
        },
        'ProPage': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['page.propage.net', 'page.propage.net'],
        },
        'Public Service Cellular': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.pscel.com'],
        },
        'Qualcomm': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pager.qualcomm.com', 'pager.qualcomm.com'],
        },
        'RAM Page': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['ram-page.com', 'ram-page.com'],
        },
        'ST Paging': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['page.stpaging.com', 'page.stpaging.com'],
        },
        'Safaricom': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['safaricomsms.com'],
        },
        'Satelindo GSM': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['satelindogsm.com', 'satelindogsm.com'],
        },
        'Satellink': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['satellink.net', 'satellink.net'],
        },
        'Simple Freedom': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['text.simplefreedom.net'],
        },
        'Skytel Pagers': {
            'flags': ['SMS', 'MMS', 'SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'email.skytel.com',
                'email.skytel.com',
                'skytel.com',
                'skytel.com'
            ],
        },
        'SunCom': {
            'flags': ['SMS', 'MMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['suncom1.com', 'suncom1.com', 'tms.suncom.com'],
        },
        'Surewest Communications': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mobile.surewest.com', 'mobile.surewest.com'],
        },
        'T-Mobile': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['voicestream.net', 'voicestream.net'],
        },
        'TSR Wireless': {
            'flags': ['SMS', 'MMS', 'SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['beep.com', 'beep.com', 'alphame.com', 'alphame.com'],
        },
        'Tamil Nadu BPL Mobile': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['bplmobile.com', 'bplmobile.com'],
        },
        'Teletouch': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pageme.teletouch.com', 'pageme.teletouch.com'],
        },
        'The Indiana Paging Co': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pager.tdspager.com', 'pager.tdspager.com'],
        },
        'Triton': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['tms.suncom.com'],
        },
        'WebLink Wiereless': {
            'flags': ['SMS', 'MMS', 'SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'pagemart.net',
                'pagemart.net',
                'airmessage.net',
                'airmessage.net'
            ],
        },
        'Wyndtell': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['wyndtell.com', 'wyndtell.com'],
        }
    },
    'Ukraine': {
        'UMC': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.umc.com.ua'],
        }
    },
    'United Kingdom': {
        'CM Telecom': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['mail-sms.com'],
        },
        'Connection Software (CSoft)': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['itsarrived.net'],
        },
        'Esendex': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['echoemail.net'],
        },
        'HSL Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.haysystems.com'],
        },
        'Mediaburst': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.mediaburst.co.uk'],
        },
        'My-Cool-SMS': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['my-cool-sms.com'],
        },
        'O2': {
            'flags': ['SMS', 'MMS', 'SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['o2.co.uk', 'o2.co.uk', 'mmail.co.uk', 'mmail.co.uk'],
        },
        'Orange': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['orange.net'],
        },
        'T-Mobile': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['t-mobile.uk.net', 't-mobile.uk.net'],
        },
        'Txtlocal': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['txtlocal.co.uk'],
        },
        'UniMovil Corporation': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['viawebsms.com'],
        },
        'Virgin Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['vxtras.com'],
        },
        'Vodafone': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['vodafone.net', 'vodafone.net'],
        },
        'aql': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['text.aql.com'],
        }
    },
    'United States': {
        'AT&T Enterprise Paging': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['page.att.net'],
        },
        'AT&T Global Smart Messaging Suite': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.smartmessagingsuite.com'],
        },
        'AT&T Mobility': {
            'flags': ['MMS', 'MMS', 'SMS', 'SMS', 'SMS', 'SMS', 'SMS'],
            'format': [
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~'
            ],
            'gateway': [
                'mms.att.net',
                'mms.att.net',
                'txt.att.net',
                'txt.att.net',
                'cingularme.com',
                'mobile.mycingular.com',
                'mmode.com'
            ],
        },
        'AT&T Pocketnet PCS': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['dpcs.mobile.att.net', 'dpcs.mobile.att.net'],
        },
        'Airfire Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.airfiremobile.com'],
        },
        'Alaska Communications': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['msg.acsalaska.com'],
        },
        'Alltel': {
            'flags':   [
                'MMS',
                'MMS',
                'SMS',
                'MMS',
                'SMS',
                'SMS'
            ],
            'format':  [
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~'
            ],
            'gateway': [
                'message.Alltel.com',
                'mms.alltel.net',
                'text.wireless.alltel.com'
                'mms.alltelwireless.com',
                'sms.alltelwireless.com',
                'alltelmessage.com'
            ],
        },
        'Ameritech': {
            'flags': ['SMS', 'SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'paging.acswireless.com',
                'paging.acswireless.com',
                'paging.acswireless.com'
            ],
        },
        'Ameritech Clearpath': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'clearpath.acswireless.com',
                'clearpath.acswireless.com'
            ],
        },
        'Ameritech Paging': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pageapi.com', 'pageapi.com'],
        },
        'Assurance Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['vmobl.com'],
        },
        'Bell Atlantic': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['message.bam.com', 'message.bam.com'],
        },
        'Bell South': {
            'flags': ['SMS', 'SMS', 'MMS', 'SMS', 'MMS'],
            'format': [
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~'
            ],
            'gateway': [
                'sms.bellsouth.com',
                'wireless.bellsouth.com',
                'wireless.bellsouth.com',
                'blsdcs.net',
                'blsdcs.net'],
        },
        'Bell South (Blackberry)': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['bellsouthtips.com', 'bellsouthtips.com'],
        },
        'Bell South Mobility': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['blsdcs.net', 'blsdcs.net'],
        },
        'BellSouth': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['bellsouth.cl'],
        },
        'Bluegrass Cellular': {
            'flags': ['MMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mms.myblueworks.com', 'sms.bluecell.com'],
        },
        'Bluesky Communications': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['psms.bluesky.as'],
        },
        'Boost Mobile': {
            'flags': ['MMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['myboostmobile.com', 'sms.myboostmobile.com'],
        },
        'C Beyond (All Page Wireless)': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['cbeyond.sprintpcs.com'],
        },
        'C Spire Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['cspire1.com'],
        },
        'Carolina West Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['cwwsms.com'],
        },
        'Cellcom': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['cellcom.quiktxt.com'],
        },
        'Cellular One': {
            'flags': [
                'SMS',
                'MMS',
                'SMS',
                'SMS',
                'MMS',
                'SMS',
                'MMS',
                'SMS',
                'SMS'
            ],
            'format': [
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~',
                '~~NUMBER~~'
            ],
            'gateway': [
                'message.cellone-sf.com',
                'message.cellone-sf.com',
                'cellularone.txtmsg.com',
                'sbcemail.com',
                'sbcemail.com',
                'mobile.celloneusa.com',
                'mobile.celloneusa.com',
                'cell1.textmsg.com',
                'cellularone.textmsg.com'
            ],
        },
        'Cellular One East Coast': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['phone.cellone.net', 'phone.cellone.net'],
        },
        'Cellular One PCS': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['paging.cellone-sf.com', 'paging.cellone-sf.com'],
        },
        'Cellular One South West': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['swmsg.com', 'swmsg.com'],
        },
        'Cellular One West': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mycellone.com', 'mycellone.com'],
        },
        'Cellular South': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['csouth1.com'],
        },
        'Centennial Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['cwemail.com'],
        },
        'Chariton Valley Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.cvalley.net'],
        },
        'Chat Mobility': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['mail.msgsender.com'],
        },
        'Cincinnati Bell': {
            'flags': ['MMS', 'SMS', 'SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'mms.gocbw.com',
                'gocbw.com',
                'mobile.att.net',
                'mobile.att.net'
            ],
        },
        'Cingular (Postpaid)': {
            'flags': ['SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['cingular.com', 'mobile.mycingular.com'],
        },
        'Cleartalk': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.cleartalk.us'],
        },
        'Comcast': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['comcastpcs.textmsg.com'],
        },
        'Consumer Cellular': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['cingularme.com'],
        },
        'Cricket': {
            'flags': ['MMS', 'SMS', 'SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': [
                'mms.mycricket.com',
                'sms.mycricket.com',
                'sms.cricketwireless.net',
                'mms.cricketwireless.net'
            ],
        },
        'DTC': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.advantagecell.net'],
        },
        'Edge Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.edgewireless.com'],
        },
        'Element Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['SMS.elementmobile.net'],
        },
        'Esendex': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['echoemail.net'],
        },
        'GCS Paging': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['webpager.us', 'webpager.us'],
        },
        'General Communications Inc.': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['mobile.gci.net'],
        },
        'Golden State Cellular': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['gscsms.com'],
        },
        'Greatcall': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['vtxt.com'],
        },
        'Hawaiian Telcom Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['hawaii.sprintpcs.com'],
        },
        'Helio': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['myhelio.com'],
        },
        'Houston Cellular': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['text.houstoncellular.net'],
        },
        'Kajeet': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['mobile.kajeet.net'],
        },
        'LongLines': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['text.longlines.com'],
        },
        'Metro PCS': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['metropcs.sms.us'],
        },
        'MetroPCS': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['mymetropcs.com'],
        },
        'Midwest Wireless': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['clearlydigital.com', 'clearlydigital.com'],
        },
        'Nextech': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.ntwls.net'],
        },
        'Nextel': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['messaging.nextel.com', 'messaging.nextel.com'],
        },
        'Nextel Pager': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['page.nextel.com'],
        },
        'Pacific Bell': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['pacbellpcs.net', 'pacbellpcs.net'],
        },
        'Page Plus Cellular(Verizon MVNO)': {
            'flags': ['MMS', 'SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mypixmessages.com', 'vtext.com', 'vzwpix.com'],
        },
        'PageOne NorthWest': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['page1nw.com', 'page1nw.com'],
        },
        'Pioneer Cellular': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['zsend.com'],
        },
        'Pocket Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.pocket.com'],
        },
        'Qwest Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['qwestmp.com'],
        },
        'Rogers Wireless': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mms.rogers.com', 'mms.rogers.com'],
        },
        'Simple Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['smtext.com'],
        },
        'Solavei': {
            'flags': ['MMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['tmomail.net'],
        },
        'South Central Communications': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['rinasms.com'],
        },
        'Southernlinc': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['page.southernlinc.com'],
        },
        'Southwestern Bell': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['email.swbw.com', 'email.swbw.com'],
        },
        'Sprint': {
            'flags': ['SMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['messaging.sprintpcs.com', 'pm.sprint.com'],
        },
        'Sprint Paging': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['sprintpaging.com', 'sprintpaging.com'],
        },
        'Straight Talk': {
            'flags': ['MMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mmst5.tracfone.com', 'tracfone.plspictures.com'],
        },
        'Syringa Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['rinasms.com'],
        },
        'Teleflip': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['teleflip.com'],
        },
        'Ting': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['message.ting.com'],
        },
        'TracFone (prepaid)': {
            'flags': ['MMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mmst5.tracfone.com', 'message.alltel.com'],
        },
        'US Cellular': {
            'flags': ['SMS', 'SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['uscc.textmsg.com', 'email.uscc.net', 'mms.uscc.net'],
        },
        'US West': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['uswestdatamail.com', 'uswestdatamail.com'],
        },
        'USA Mobility': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['usamobility.net'],
        },
        'Unicel': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['utext.com'],
        },
        'Union Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['union-tel.com'],
        },
        'Verizon PCS': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['myvzw.com', 'myvzw.com'],
        },
        'Verizon Pagers': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['myairmail.com', 'myairmail.com'],
        },
        'Viaero': {
            'flags': ['MMS', 'SMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['mmsviaero.com', 'viaerosms.com'],
        },
        'Virgin Mobile': {
            'flags': ['MMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['vmpix.com'],
        },
        'Vodafone': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['vodafone.net', 'vodafone.net'],
        },
        'VoiceStream / T-Mobile': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['voicestream.net', 'voicestream.net'],
        },
        'Voyager Mobile': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['text.voyagermobile.com'],
        },
        'West Central Wireless': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.wcc.net'],
        },
        'Western Wireless': {
            'flags': ['SMS', 'MMS'],
            'format': ['~~NUMBER~~', '~~NUMBER~~'],
            'gateway': ['cellularonewest.com', 'cellularonewest.com'],
        },
        'XIT Communications': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['sms.xit.net'],
        },
        'i wireless (T-Mobile)': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~.iws'],
            'gateway': ['iwspcs.net'],
        },
        'i-wireless (Sprint PCS)': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['iwirelesshometext.com'],
        },
        'nTelos': {
            'flags': ['SMS'],
            'format': ['~~NUMBER~~'],
            'gateway': ['pcs.ntelos.com'],
        },
    },
    'Uruguay': {
        'Movistar': {
            'flags': ['SMS'],
            'format': ['95~~NUMBER~~'],
            'gateway': ['sms.movistar.com.uy'],
        },
    },
}

# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

from __core_audio.constant import (
    JACKDESC2_PRESENCE_DETECT_CAPABILITY,
    JACKDESC2_DYNAMIC_FORMAT_CHANGE_CAPABILITY
)
from __core_audio.enum import (
    KSJACK_SINK_CONNECTIONTYPE,
    EPcxGenLocation,
    EPcxGeoLocation,
    EPcxConnectionType,
    EPxcPortConnection
)
from speaker import AudioSpeakers
from utils import convert_triplet_to_rgb

SINK_CONNECTIONTYPE = {
    KSJACK_SINK_CONNECTIONTYPE.KSJACK_SINK_CONNECTIONTYPE_HDMI:        'HDMI',
    KSJACK_SINK_CONNECTIONTYPE.KSJACK_SINK_CONNECTIONTYPE_DISPLAYPORT: (
        'Displayport'
    )
}


EPCX_GEN_LOCATION = {
    EPcxGenLocation.eGenLocInternal:   'Inside primary chassis',
    EPcxGenLocation.eGenLocOther:      'Other location',
    EPcxGenLocation.eGenLocPrimaryBox: 'On primary chassis',
    EPcxGenLocation.eGenLocSeparate:   'On separate chassis'
}

EPCX_GEO_LOCATION = {
    EPcxGeoLocation.eGeoLocRear:             'Rear-mounted panel',
    EPcxGeoLocation.eGeoLocFront:            'Front-mounted panel',
    EPcxGeoLocation.eGeoLocLeft:             'Left-mounted panel',
    EPcxGeoLocation.eGeoLocRight:            'Right-mounted panel',
    EPcxGeoLocation.eGeoLocTop:              'Top-mounted panel',
    EPcxGeoLocation.eGeoLocBottom:           'Bottom-mounted panel',
    EPcxGeoLocation.eGeoLocRiser:            'Riser card',
    EPcxGeoLocation.eGeoLocInsideMobileLid:  'Inside lid of mobile computer',
    EPcxGeoLocation.eGeoLocDrivebay:         'Drive bay',
    EPcxGeoLocation.eGeoLocHDMI:             'HDMI connector',
    EPcxGeoLocation.eGeoLocOutsideMobileLid: 'Outside lid of mobile computer',
    EPcxGeoLocation.eGeoLocATAPI:            'ATAPI connector',
    EPcxGeoLocation.eGeoLocNotApplicable:    'Not Applicable',
    EPcxGeoLocation.eGeoLocReserved6:        'Reserved',
    EPcxGeoLocation.eGeoLocRearPanel:        (
        'Rear slide-open or pull-open panel'
    ),
    EPcxGeoLocation.eGeoLocRearOPanel:       (
        'Rear slide-open or pull-open panel'
    )
}

EPCX_CONNECTION_TYPE = {
    EPcxConnectionType.eConnTypeUnknown:               'Unknown',
    EPcxConnectionType.eConnTypeRCA:                   'RCA jack',
    EPcxConnectionType.eConnTypeOptical:               'Optical connector',
    EPcxConnectionType.eConnTypeXlrProfessional:       'XLR connector',
    EPcxConnectionType.eConnTypeRJ11Modem:             'RJ11 modem connector',
    EPcxConnectionType.eConnTypeQuarter:               (
        '6.35mm (1/4" Phono) jack'
    ),
    EPcxConnectionType.eConnTypeOtherDigital:          (
        'Generic digital connector'
    ),
    EPcxConnectionType.eConnTypeOtherAnalog:           (
        'Generic analog connector'
    ),
    EPcxConnectionType.eConnTypeAtapiInternal:         (
        'ATAPI internal connector'
    ),
    EPcxConnectionType.eConnTypeCombination:           (
        'Combination of connector types'
    ),
    EPcxConnectionType.eConnType3Point5mm:             (
        '3.5mm (1\8" Headphone) jack'
    ),
    EPcxConnectionType.eConnTypeEighth:                (
        '3.5mm (1\8" Headphone) jack'
    ),
    EPcxConnectionType.eConnTypeMultichannelAnalogDIN: (
        'Multichannel analog DIN connector'
    )
}


EPCX_PORT_CONNECTION = {
    EPxcPortConnection.ePortConnJack:                  'Jack',
    EPxcPortConnection.ePortConnUnknown:               'Unknown',
    EPxcPortConnection.ePortConnIntegratedDevice:      (
        'Slot for an integrated device'
    ),
    EPxcPortConnection.ePortConnBothIntegratedAndJack: (
        'Both a jack and a slot for an integrated device'
    )
}


class AudioJackSinkInformation(object):

    def __init__(self, sink_information):
        self.__sink_information = (
            sink_information.GetJackSinkInformation()
        )
        sink_information.Release()

    @property
    def manufacturer_id(self):
        return self.__sink_information.ManufacturerId

    @property
    def product_id(self):
        return self.__sink_information.ProductId

    @property
    def audio_latency(self):
        return self.__sink_information.AudioLatency

    @property
    def hdcp_capable(self):
        return bool(self.__sink_information.HDCPCapable)

    @property
    def ai_capable(self):
        return bool(self.__sink_information.AICapable)

    @property
    def description(self):
        return self.__sink_information.SinkDescription

    @property
    def port_id(self):
        return self.__sink_information.PortId

    @property
    def connection_type(self):
        return SINK_CONNECTIONTYPE[self.__sink_information.ConnType.value]


class AudioJackDescription(object):

    def __init__(self, jack_description, jack_description2):
        self.__jack_description = jack_description
        self.__jack_description2 = jack_description2

    @property
    def channel_mapping(self):
        return AudioSpeakers(self.__jack_description.ChannelMapping)

    @property
    def color(self):
        return convert_triplet_to_rgb(self.__jack_description.Color)

    @property
    def type(self):
        return EPCX_CONNECTION_TYPE[self.__jack_description.ConnectionType]

    @property
    def location(self):
        return (
            EPCX_GEN_LOCATION[self.__jack_description.GenLocation] +
            ', ' +
            EPCX_GEO_LOCATION[self.__jack_description.GeoLocation]
        )

    @property
    def port(self):
        return EPCX_PORT_CONNECTION[self.__jack_description.PortConnection]

    @property
    def is_connected(self):
        return bool(self.__jack_description.IsConnected)

    @property
    def presence_detection(self):
        if self.__jack_description2 is None:
            raise AttributeError

        return (
            self.__jack_description2.JackCapabilities |
            JACKDESC2_PRESENCE_DETECT_CAPABILITY ==
            self.__jack_description2.JackCapabilities
        )

    @property
    def dynamic_format_change(self):
        if self.__jack_description2 is None:
            raise AttributeError

        return (
            self.__jack_description2.JackCapabilities |
            JACKDESC2_DYNAMIC_FORMAT_CHANGE_CAPABILITY ==
            self.__jack_description2.JackCapabilities
        )

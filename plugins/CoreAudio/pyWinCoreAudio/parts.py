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

import comtypes
from __core_audio.enum import (
    ConnectorType,
    ERole,
    PartType
)
from __core_audio.devicetopologyapi import (
    IPart,
)


CLSCTX_INPROC_SERVER = comtypes.CLSCTX_INPROC_SERVER

E_ROLE = {
    ERole.eConsole:         'Console',
    ERole.eMultimedia:      'Multimedia',
    ERole.eCommunications:  'Communications',
    ERole.ERole_enum_count: 'ERole_enum_count'
}
CONNECTOR_TYPE = {
    ConnectorType.Unknown_Connector: 'Unknown Connector',
    ConnectorType.Physical_Internal: 'Physical Internal',
    ConnectorType.Physical_External: 'Physical External',
    ConnectorType.Software_IO:       'Software IO',
    ConnectorType.Software_Fixed:    'Software Fixed',
    ConnectorType.Network:           'Network'
}


class AudioDeviceSubunit(object):

    def __init__(self, subunit):
        self.__subunit = subunit

    @property
    def part(self):
        return AudioPart(self.__subunit.QueryInterface(IPart))


class AudioDeviceConnection(object):

    def __init__(self, connector):
        self.__connector = connector

    @property
    def type(self):
        return CONNECTOR_TYPE[self.__connector.GetType().value]

    @property
    def part(self):
        return AudioPart(self.__connector.QueryInterface(IPart))

    @property
    def connected_to_device_id(self):
        return self.__connector.GetDeviceIdConnectedTo()

    @property
    def is_connected(self):
        return self.__connector.IsConnected() == 1

    @property
    def connected_to(self):
        return AudioDeviceConnection(self.__connector.GetConnectedTo())

    @connected_to.setter
    def connected_to(self, connection):
        self.__connector.ConnectTo(connection.get_c_connector())

    @property
    def data_flow(self):
        return E_ROLE[self.__connector.GetDataFlow().value]

    def get_c_connector(self):
        return self.__connector

    def disconnect(self):
        self.__connector.Disconnect()


class AudioPart(object):

    def __init__(self, part):
        self.__part = part

    def activate(self, iid, pointer):
        return comtypes.cast(
            self.__part.Activate(
                CLSCTX_INPROC_SERVER,
                iid
            ),
            pointer
        )

    @property
    def incoming(self):
        return AudioPartsList(self.__part.EnumPartsIncoming())

    @property
    def outgoing(self):
        return AudioPartsList(self.__part.EnumPartsOutgoing())

    @property
    def interfaces(self):
        for index in range(self.__part.GetControlInterfaceCount()):
            yield self.__part.GetControlInterface(index)

    @property
    def global_id(self):
        return self.__part.GetGlobalId()

    @property
    def local_id(self):
        return self.__part.GetLocalId()

    @property
    def name(self):
        return self.__part.GetName()

    @property
    def is_connector(self):
        return self.__part.GetPartType().value == PartType.Connector

    @property
    def is_subunit(self):
        return self.__part.GetPartType().value == PartType.Subunit

    @property
    def sub_type(self):
        return self.__part.GetSubType()

    @property
    def device_topology(self):
        return self.__part.GetTopologyObject()

    def register_notification_callback(self, interface_iid, callback):
        self.__part.RegisterControlChangeCallback(
            interface_iid,
            callback
        )

    def unregister_notification_callback(self, callback):
        self.__part.UnregisterControlChangeCallback(callback)
        callback.Release()

    def query_interface(self, interface):
        return self.__part.QueryInterface(interface)


class AudioPartsList(object):

    def __init__(self, parts_list):
        self.__parts_list = parts_list

    def get_part(self, index):
        return AudioPart(self.__parts_list.GetPart(index))

    def release(self):
        self.__parts_list.Release()

    def __iter__(self):
        for i in range(self.__parts_list.GetCount()):
            yield self.get_part(i)

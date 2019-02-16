# -*- coding: utf-8 -*-

import six
import requests
from lxml import etree
from .xmlns import strip_xmlns
from .service import Service
from .embedded_device import EmbeddedDevice
from .instance_singleton import InstanceSingleton


@six.add_metaclass(InstanceSingleton)
class UPNPObject(object):

    def __init__(self, ip, locations):
        self.ip_address = ip
        url_template = 'http://'
        cls_name = None
        self.__devices = {}
        self.__services = {}

        for location in locations:
            url = url_template + (
                location.replace('http://', '').split('/')[0]
            )
            location = location.replace(url, '')

            response = requests.get(url + location)
            root = etree.fromstring(response.content)
            root = strip_xmlns(root)

            node = root.find('device')

            services = node.find('serviceList')
            if services is None:
                services = []

            devices = node.find('deviceList')
            if devices is None:
                devices = []

            for service in services:
                scpdurl = service.find('SCPDURL').text.replace(url, '')
                control_url = service.find('controlURL').text.replace(url, '')
                service_id = service.find('serviceId').text
                service_type = service.find('serviceType').text
                if location is not None:
                    scpdurl = (
                        '/' +
                        location[1:].split('/')[0] +
                        '/' +
                        scpdurl
                    )

                service = Service(
                    self,
                    url,
                    scpdurl,
                    service_type,
                    control_url,
                    node
                )
                name = service_id.split(':')[-1]
                service.__name__ = name
                self.__services[name] = service

            for device in devices:
                device = EmbeddedDevice(url, node=device, parent=self)
                self.__devices[device.__name__] = device

            if cls_name is None:
                cls_name = node.find('modelName')
                if cls_name is not None and cls_name.text:
                    cls_name = cls_name.text.replace(' ', '_').replace('-', '')

        self.__name__ = cls_name

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self.__devices:
            return self.__devices[item]

        if item in self.__services:
            return self.__services[item]

        if item in self.__class__.__dict__:
            if hasattr(self.__class__.__dict__[item], 'fget'):
                return self.__class__.__dict__[item].fget(self)

        raise AttributeError(item)

    @property
    def access_point(self):
        return self.__class__.__name__

    @property
    def services(self):
        return list(self.__services.values())[:]

    @property
    def devices(self):
        return list(self.__devices.values())[:]

    def __str__(self):
        output = '\n\n' + str(self.__name__) + '\n'
        output += 'IP Address: ' + self.ip_address + '\n'
        output += '==============================================\n'

        if self.services:
            output += 'Services:\n'
            for cls in self.services:
                output += cls.__str__(indent='    ').rstrip() + '\n'
        else:
            output += 'Services: None\n'

        if self.devices:
            output += 'Devices:\n'
            for cls in self.devices:
                output += cls.__str__(indent='    ').rstrip() + '\n'
        else:
            output += 'Devices: None\n'

        return output

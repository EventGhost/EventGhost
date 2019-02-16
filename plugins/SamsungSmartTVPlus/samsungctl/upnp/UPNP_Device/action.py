# -*- coding: utf-8 -*-

import requests
from xml.dom.minidom import Document
from lxml import etree
from .xmlns import ENVELOPE_XMLNS, strip_xmlns


class Action(object):

    def __init__(self, parent, node, state_variables, service, control_url):
        self.__parent = parent
        self.params = []
        self.param_names = []
        self.ret_vals = []
        self.ret_val_names = []
        self.service = service
        self.control_url = control_url

        self.__name__ = node.find('name').text

        for arguments in node:
            if arguments.tag != 'argumentList':
                continue
            for argument in arguments:
                name = argument.find('name').text
                direction = argument.find('direction').text
                variable = argument.find('relatedStateVariable').text
                variable = state_variables[variable](direction)

                if direction == 'in':
                    self.params += [variable]
                    self.param_names += [name]
                else:
                    self.ret_vals += [variable]
                    self.ret_val_names += [name]

    def __call__(self, *args, **kwargs):
        for i, arg in enumerate(args):
            try:
                kwargs[self.param_names[i]] = arg
            except IndexError:
                for param in self.param_names:
                    print(param)
                raise

        doc = Document()

        envelope = doc.createElementNS('', 's:Envelope')
        envelope.setAttribute(
            'xmlns:s',
            ENVELOPE_XMLNS
        )
        envelope.setAttribute(
            's:encodingStyle',
            'http://schemas.xmlsoap.org/soap/encoding/'
        )

        body = doc.createElementNS('', 's:Body')

        fn = doc.createElementNS('', self.__name__)
        fn.setAttribute('xmlns:u', self.service)

        for i, param in enumerate(self.params):
            if self.param_names[i] not in kwargs:
                value = param(None)
            else:
                value = param(kwargs[self.param_names[i]])

            tmp_node = doc.createElement(self.param_names[i])
            tmp_text_node = doc.createTextNode(str(value))
            tmp_node.appendChild(tmp_text_node)
            fn.appendChild(tmp_node)

        body.appendChild(fn)
        envelope.appendChild(body)
        doc.appendChild(envelope)
        pure_xml = doc.toxml()

        header = {
            'SOAPAction':   '"{service}#{method}"'.format(
                service=self.service,
                method=self.__name__
            ),
            'Content-Type': 'text/xml'
        }
        response = requests.post(
            self.control_url,
            data=pure_xml,
            headers=header
        )
        envelope = etree.fromstring(response.content)
        envelope = strip_xmlns(envelope)

        body = envelope.find('Body')

        return_value = []

        if body is not None:

            response = body.find(self.__name__ + 'Response')
            if response is not None:
                for i, ret_val in enumerate(self.ret_vals):
                    value = response.find(self.ret_val_names[i])
                    if value is None:
                        value = ret_val(None)
                    else:
                        value = ret_val(value.text)

                    return_value += [value]

        if not return_value and self.ret_vals:
            for val in self.ret_vals:
                return_value += [val(None)]

        return return_value

    @property
    def access_point(self):
        return self.__parent.access_point + '.' + self.__name__

    def __str__(self, indent=''):
        if self.params:
            param_names = ', '.join(self.param_names)
            params = '\n'

            for i, param in enumerate(self.params):
                params += indent + '    Name: ' + self.param_names[i]
                params += param.__str__(indent + '    ') + '\n'

        else:
            params = 'None\n\n'
            param_names = ''

        if self.ret_vals:
            ret_val_names = 'dict(' + (
                ', '.join(self.ret_val_names)) + ') = '
            ret_vals = '\n'

            for i, val in enumerate(self.ret_vals):
                ret_vals += indent + '    Name: ' + self.ret_val_names[i]
                ret_vals += val.__str__(indent=indent + '        ') + '\n'

        else:
            ret_vals = 'None\n\n'
            ret_val_names = ''

        output = TEMPLATE.format(
            indent=indent,
            name=self.__name__,
            access_point=self.access_point,
            params=params,
            ret_vals=ret_vals,
            param_names=param_names,
            ret_val_names=ret_val_names
        )

        return output

TEMPLATE = '''{indent}Method name: {name}
{indent}Access point: {access_point}
{indent}Call: {ret_val_names}{access_point}({param_names})
{indent}----------------------------------------------
{indent}    Parameters: {params}{indent}    Return Values: {ret_vals}'''

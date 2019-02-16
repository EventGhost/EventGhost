# -*- coding: utf-8 -*-

import sys
import base64
import uuid

PY3 = sys.version_info[0] >= 3


if PY3:
    unicode = bytes


class StateVariable(object):
    def __init__(self, node):
        self.node = node
        self.name = node.find('name').text
        data_type = node.find('dataType').text

        data_type_classes = {
            'time.tz': TimeTZ,
            'time': Time,
            'dateTime.tz': DateTimeTZ,
            'dateTime': DateTime,
            'date': Date,
            'uuid': UUID,
            'uri': URI,
            'bin.base64': BinBase64,
            'boolean': Boolean,
            'string': String,
            'char': Char,
            'float': Float,
            'fixed.14.4': Fixed144,
            'number': Number,
            'r8': R8,
            'r4': R4,
            'int': Int,
            'i8': I8,
            'i4': I4,
            'i2': I2,
            'i1': I1,
            'ui8': UI8,
            'ui4': UI4,
            'ui2': UI2,
            'ui1': UI1
        }

        self.data_type = data_type_classes[data_type]

    def __call__(self, direction):
        data_type = self.data_type(self.node, direction)
        data_type.__name__ = self.name
        return data_type


class UUID(object):

    def __init__(self, node, direction):
        self.direction = direction
        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            upnp_data_type=self.__name__,
            py_data_type='uuid'
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += [indent + 'Allowed values:']
            else:
                output += [indent + 'Possible returned values:']
            for item in self.allowed_values:
                output += indent + '    ' + item + '\n'

        return output

    def __call__(self, value):

        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':

            if isinstance(value, uuid.UUID):
                value = str(value)[1:-1]

            if PY3:
                if not isinstance(value, (str, bytes)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, bytes'
                        'got type {0}.'.format(type(value))
                    )

                try:
                    value = value.decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            else:
                if not isinstance(value, (str, unicode)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, unicode'
                        ' got type {0}.'.format(type(value))
                    )

                try:
                    value = value.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = uuid.UUID(value)

        return value


class Fixed144(object):
    def __init__(self, node, direction):
        self.direction = direction
        self.minimum = None
        self.maximum = None
        self.step = None

        allowed_range = node.find('allowedValueRange')
        if allowed_range is not None:
            minimum = allowed_range.find('minimum')
            maximum = allowed_range.find('maximum')
            step = allowed_range.find('step')

            if minimum is not None and minimum.text:
                self.minimum = float(minimum.text)
            if maximum is not None and maximum.text:
                self.maximum = float(maximum.text)
            if step is not None and step.text:
                self.step = float(step.text)

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = float(default_value.text)

        self.default_value = default_value

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            upnp_data_type=self.__name__,
            py_data_type='8 byte float'
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + repr(self.default_value) + '\n'

        if self.minimum is not None:
            output += indent + 'Minimum: ' + repr(self.minimum) + '\n'

        if self.maximum is not None:
            output += indent + 'Maximum: ' + str(self.maximum) + '\n'

        if self.step is not None:
            output += indent + 'Step: ' + repr(self.step) + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':

            if not isinstance(value, float):
                raise ValueError('Value is not an 8 byte float')

            if (
                value > 0 and
                (
                    value < 4.94065645841247E-324 or
                    value > 1.79769313486232E308
                )
            ):
                raise ValueError('Value is not an 8 byte float')

            if (
                value < 0 and
                (
                    value < -1.79769313486232E308 or
                    value > -4.94065645841247E-324
                )
            ):
                raise ValueError('Value is not an 8 byte float')

            if self.minimum is not None and value < self.minimum:
                raise ValueError(
                    'Value {0} is lower then the minimum of {1}'.format(
                        value,
                        self.minimum
                    )
                )

            if self.maximum is not None and value > self.maximum:
                raise ValueError(
                    'Value {0} is higher then the maximum of {1}'.format(
                        value,
                        self.maximum
                    )
                )

            if self.step is not None and value % self.step:
                raise ValueError(
                    'Value is not an increment of ' + str(self.step)
                )

            value = '{0:14.4f}'.format(value)

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = float(value)

        return value


class BinBase64(object):

    def __init__(self, node, direction):
        self.direction = direction

        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        if PY3:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, bytes'
            )
        else:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, unicode'
            )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += [indent + 'Allowed values:']
            else:
                output += [indent + 'Possible returned values:']
            for item in self.allowed_values:
                output += indent + '    ' + item + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')
            else:
                value = self.default_value

        if self.direction == 'in':
            if PY3:
                if not isinstance(value, (str, bytes)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, bytes'
                        'got type {0}.'.format(type(value))
                    )

                try:
                    value = value.decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            else:
                if not isinstance(value, (str, unicode)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, unicode'
                        ' got type {0}.'.format(type(value))
                    )

                try:
                    value = value.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

            value = base64.encodebytes(value)

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = base64.decodebytes(value)

        return value


class BinHex(object):

    def __init__(self, node, direction):
        self.direction = direction
        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            upnp_data_type=self.__name__,
            py_data_type='hex, int'
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += [indent + 'Allowed values:']
            else:
                output += [indent + 'Possible returned values:']
            for item in self.allowed_values:
                output += indent + '    ' + item + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')
            else:
                value = self.default_value

        if self.direction == 'in':
            if isinstance(value, int):
                value = hex(value)

            if PY3:
                if not isinstance(value, (str, bytes)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, bytes'
                        'got type {0}.'.format(type(value))
                    )

                try:
                    value = value.decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            else:
                if not isinstance(value, (str, unicode)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, unicode'
                        ' got type {0}.'.format(type(value))
                    )

                try:
                    value = value.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

            value = value.replace('0X', '0x')

            if not value.startswith('0x'):
                raise ValueError('Value is not hex')

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value


        return value


class Char(object):

    def __init__(self, node, direction):
        self.direction = direction
        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        if PY3:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='chr, byte'
            )
        else:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='chr, unichr'
            )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += [indent + 'Allowed values:']
            else:
                output += [indent + 'Possible returned values:']
            for item in self.allowed_values:
                output += indent + '    ' + item + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')
            else:
                value = self.default_value

        if self.direction == 'in':
            if PY3:
                if not isinstance(value, (str, bytes)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, bytes'
                        'got type {0}.'.format(type(value))
                    )

                try:
                    value = value.decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            else:
                if not isinstance(value, (str, unicode)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, unicode'
                        ' got type {0}.'.format(type(value))
                    )

                try:
                    value = value.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

            if len(value) != 1:
                raise ValueError('Value is not a single character')

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value

        return value


class Float(object):
    def __init__(self, node, direction):
        self.direction = direction
        self.minimum = None
        self.maximum = None
        self.step = None

        allowed_range = node.find('allowedValueRange')
        if allowed_range is not None:
            minimum = allowed_range.find('minimum')
            maximum = allowed_range.find('maximum')
            step = allowed_range.find('step')

            if minimum is not None and minimum.text:
                self.minimum = float(minimum.text)
            if maximum is not None and maximum.text:
                self.maximum = float(maximum.text)
            if step is not None and step.text:
                self.step = float(step.text)

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = float(default_value.text)

        self.default_value = default_value

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            upnp_data_type=self.__name__,
            py_data_type='float'
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + repr(self.default_value) + '\n'

        if self.minimum is not None:
            output += indent + 'Minimum: ' + repr(self.minimum) + '\n'

        if self.maximum is not None:
            output += indent + 'Maximum: ' + str(self.maximum) + '\n'

        if self.step is not None:
            output += indent + 'Step: ' + repr(self.step) + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':

            if not isinstance(value, float):
                raise ValueError('Value is not a float')

            if self.minimum is not None and value < self.minimum:
                raise ValueError(
                    'Value {0} is lower then the minimum of {1}'.format(
                        value,
                        self.minimum
                    )
                )

            if self.maximum is not None and value > self.maximum:
                raise ValueError(
                    'Value {0} is higher then the maximum of {1}'.format(
                        value,
                        self.maximum
                    )
                )

            if self.step is not None and value % self.step:
                raise ValueError(
                    'Value is not an increment of ' + str(self.step)
                )

            value = str(value)

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = float(value)

        return value


class R8(object):
    def __init__(self, node, direction):
        self.direction = direction
        self.minimum = None
        self.maximum = None
        self.step = None

        allowed_range = node.find('allowedValueRange')
        if allowed_range is not None:
            minimum = allowed_range.find('minimum')
            maximum = allowed_range.find('maximum')
            step = allowed_range.find('step')

            if minimum is not None and minimum.text:
                self.minimum = float(minimum.text)
            if maximum is not None and maximum.text:
                self.maximum = float(maximum.text)
            if step is not None and step.text:
                self.step = float(step.text)

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = float(default_value.text)

        self.default_value = default_value

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            upnp_data_type=self.__name__,
            py_data_type='8 byte float'
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + repr(self.default_value) + '\n'

        if self.minimum is not None:
            output += indent + 'Minimum: ' + repr(self.minimum) + '\n'

        if self.maximum is not None:
            output += indent + 'Maximum: ' + str(self.maximum) + '\n'

        if self.step is not None:
            output += indent + 'Step: ' + repr(self.step) + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':

            if not isinstance(value, float):
                raise ValueError('Value is not an 8 byte float')

            if (
                value > 0 and
                (
                    value < 4.94065645841247E-324 or
                    value > 1.79769313486232E308
                )
            ):
                raise ValueError('Value is not an 8 byte float')

            if (
                value < 0 and
                (
                    value < -1.79769313486232E308 or
                    value > -4.94065645841247E-324
                )
            ):
                raise ValueError('Value is not an 8 byte float')

            if self.minimum is not None and value < self.minimum:
                raise ValueError(
                    'Value {0} is lower then the minimum of {1}'.format(
                        value,
                        self.minimum
                    )
                )

            if self.maximum is not None and value > self.maximum:
                raise ValueError(
                    'Value {0} is higher then the maximum of {1}'.format(
                        value,
                        self.maximum
                    )
                )

            if self.step is not None and value % self.step:
                raise ValueError(
                    'Value is not an increment of ' + str(self.step)
                )

            value = str(value)

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = float(value)

        return value


class Number(R8):
    pass


class R4(object):
    def __init__(self, node, direction):
        self.direction = direction
        self.minimum = None
        self.maximum = None
        self.step = None

        allowed_range = node.find('allowedValueRange')
        if allowed_range is not None:
            minimum = allowed_range.find('minimum')
            maximum = allowed_range.find('maximum')
            step = allowed_range.find('step')

            if minimum is not None and minimum.text:
                self.minimum = float(minimum.text)
            if maximum is not None and maximum.text:
                self.maximum = float(maximum.text)
            if step is not None and step.text:
                self.step = float(step.text)

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = float(default_value.text)

        self.default_value = default_value

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            upnp_data_type=self.__name__,
            py_data_type='4 byte float'
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + repr(self.default_value) + '\n'

        if self.minimum is not None:
            output += indent + 'Minimum: ' + repr(self.minimum) + '\n'

        if self.maximum is not None:
            output += indent + 'Maximum: ' + str(self.maximum) + '\n'

        if self.step is not None:
            output += indent + 'Step: ' + repr(self.step) + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':
            if (
                not isinstance(value, float) or
                value < 3.40282347E+38 or
                value > 1.17549435E-38
            ):
                raise ValueError('Value is not a 4 byte float')

            if self.minimum is not None and value < self.minimum:
                raise ValueError(
                    'Value {0} is lower then the minimum of {1}'.format(
                        value,
                        self.minimum
                    )
                )

            if self.maximum is not None and value > self.maximum:
                raise ValueError(
                    'Value {0} is higher then the maximum of {1}'.format(
                        value,
                        self.maximum
                    )
                )

            if self.step is not None and value % self.step:
                raise ValueError(
                    'Value is not an increment of ' + str(self.step)
                )

            value = str(value)

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = float(value)

        return value


class SignedUnsignedBase(object):
    _label = ''
    _min = 0
    _max = 0

    def __init__(self, node, direction):
        self.direction = direction
        self.minimum = None
        self.maximum = None
        self.step = None

        allowed_range = node.find('allowedValueRange')
        if allowed_range is not None:
            minimum = allowed_range.find('minimum')
            maximum = allowed_range.find('maximum')
            step = allowed_range.find('step')

            if minimum is not None and minimum.text and minimum.text.isdigit():
                self.minimum = int(minimum.text)
            if maximum is not None and maximum.text and maximum.text.isdigit():
                self.maximum = int(maximum.text)
            if step is not None and step.text and step.text.isdigit():
                self.step = int(step.text)

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = int(default_value.text)

        self.default_value = default_value

    def __str__(self, indent=''):

        output = TEMPLATE.format(
            indent=indent,
            upnp_data_type=self.__name__,
            py_data_type=self._label + ' int'
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + repr(self.default_value) + '\n'

        if self.minimum is not None:
            output += indent + 'Minimum: ' + repr(self.minimum) + '\n'

        if self.maximum is not None:
            output += indent + 'Maximum: ' + str(self.maximum) + '\n'

        if self.step is not None:
            output += indent + 'Step: ' + repr(self.step) + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')
            else:
                value = self.default_value

        if self.direction == 'in':

            if (
                not isinstance(value, int) or
                value < self._min or
                value > self._max
            ):
                raise ValueError('Value is not a ' + self._label + ' integer')

            if self.minimum is not None and value < self.minimum:
                raise ValueError(
                    'Value {0} is lower then the minimum of {1}'.format(
                        value,
                        self.minimum
                    )
                )

            if self.maximum is not None and value > self.maximum:
                raise ValueError(
                    'Value {0} is higher then the maximum of {1}'.format(
                        value,
                        self.maximum
                    )
                )

            if self.step is not None and value % self.step:
                raise ValueError(
                    'Value is not an increment of ' + str(self.step)
                )

            value = str(value)

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = int(value)

        return value


class I8(SignedUnsignedBase):
    _label = 'signed 64bit'
    _min = -9223372036854775808
    _max = 9223372036854775807


class I4(SignedUnsignedBase):
    _label = 'signed 32bit'
    _min = -2147483648
    _max = 2147483647


class I2(SignedUnsignedBase):
    _label = 'signed 16bit'
    _min = -32768
    _max = 32767


class I1(SignedUnsignedBase):
    _label = 'signed 8bit'
    _min = -128
    _max = 127


class UI8(SignedUnsignedBase):
    _label = 'unsigned 64bit'
    _min = 0
    _max = 18446744073709551615


class UI4(SignedUnsignedBase):
    _label = 'unsigned 32bit'
    _min = 0
    _max = 4294967295


class UI2(SignedUnsignedBase):
    _label = 'unsigned 16bit'
    _min = 0
    _max = 65535


class UI1(SignedUnsignedBase):
    _label = 'unsigned 8bit'
    _min = 0
    _max = 255


class Int(object):
    def __init__(self, node, direction):
        self.direction = direction
        self.minimum = None
        self.maximum = None
        self.step = None

        allowed_range = node.find('allowedValueRange')
        if allowed_range is not None:
            minimum = allowed_range.find('minimum')
            maximum = allowed_range.find('maximum')
            step = allowed_range.find('step')

            if minimum is not None and minimum.text and minimum.text.isdigit():
                self.minimum = int(minimum.text)
            if maximum is not None and maximum.text and maximum.text.isdigit():
                self.maximum = int(maximum.text)
            if step is not None and step.text and step.text.isdigit():
                self.step = int(step.text)

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = int(default_value.text)

        self.default_value = default_value

    def __str__(self, indent=''):

        output = TEMPLATE.format(
            indent=indent,
            upnp_data_type=self.__name__,
            py_data_type='int'
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + repr(self.default_value) + '\n'

        if self.minimum is not None:
            output += indent + 'Minimum: ' + repr(self.minimum) + '\n'

        if self.maximum is not None:
            output += indent + 'Maximum: ' + str(self.maximum) + '\n'

        if self.step is not None:
            output += indent + 'Step: ' + repr(self.step) + '\n'

        return output

    def __call__(self, value):

        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value
        if self.direction == 'in':
            if not isinstance(value, int):
                raise ValueError('Value is not a integer')

            if self.minimum is not None and value < self.minimum:
                raise ValueError(
                    'Value {0} is lower then the minimum of {1}'.format(
                        value,
                        self.minimum
                    )
                )

            if self.maximum is not None and value > self.maximum:
                raise ValueError(
                    'Value {0} is higher then the maximum of {1}'.format(
                        value,
                        self.maximum
                    )
                )

            if self.step is not None and value % self.step:
                raise ValueError(
                    'Value is not an increment of ' + str(self.step)
                )

            value = str(value)

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = int(value)

        return value


class String(object):

    def __init__(self, node, direction):
        self.direction = direction
        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        if PY3:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, bytes'
            )
        else:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, unicode'
            )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += indent + 'Allowed values:\n'
            else:
                output += indent + 'Possible returned values:\n'
            for item in self.allowed_values:
                output += indent + '    ' + item + '\n'

        return output

    def __call__(self, value):

        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':
            if PY3:
                if not isinstance(value, (str, bytes)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, bytes'
                        'got type {0}.'.format(type(value))
                    )

                try:
                    value = value.decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            else:
                if not isinstance(value, (str, unicode)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, unicode'
                        ' got type {0}.'.format(type(value))
                    )

                try:
                    value = value.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value

        return value


class URI(String):
    pass


class TimeTZ(object):

    def __init__(self, node, direction):
        self.direction = direction
        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        if PY3:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, bytes'
            )
        else:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, unicode'
            )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += [indent + 'Allowed values:']
            else:
                output += [indent + 'Possible returned values:']
            for item in self.allowed_values:
                output += indent + '    ' + item + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':
            if PY3:
                if not isinstance(value, (str, bytes)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, bytes'
                        'got type {0}.'.format(type(value))
                    )

                try:
                    value = value.decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            else:
                if not isinstance(value, (str, unicode)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, unicode'
                        ' got type {0}.'.format(type(value))
                    )

                try:
                    value = value.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value

        return value


class Time(object):

    def __init__(self, node, direction):
        self.direction = direction
        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        if PY3:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, bytes'
            )
        else:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, unicode'
            )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += [indent + 'Allowed values:']
            else:
                output += [indent + 'Possible returned values:']
            for item in self.allowed_values:
                output += indent + '    ' + item + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':
            if PY3:
                if not isinstance(value, (str, bytes)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, bytes'
                        'got type {0}.'.format(type(value))
                    )

                try:
                    value = value.decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            else:
                if not isinstance(value, (str, unicode)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, unicode'
                        ' got type {0}.'.format(type(value))
                    )

                try:
                    value = value.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value


        return value


class DateTimeTZ(object):

    def __init__(self, node, direction):
        self.direction = direction
        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        if PY3:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, bytes'
            )
        else:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, unicode'
            )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += [indent + 'Allowed values:']
            else:
                output += [indent + 'Possible returned values:']
            for item in self.allowed_values:
                output += indent + '    ' + item + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':
            if PY3:
                if not isinstance(value, (str, bytes)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, bytes'
                        'got type {0}.'.format(type(value))
                    )

                try:
                    value = value.decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            else:
                if not isinstance(value, (str, unicode)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, unicode'
                        ' got type {0}.'.format(type(value))
                    )

                try:
                    value = value.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value

        return value


class DateTime(object):

    def __init__(self, node, direction):
        self.direction = direction
        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        if PY3:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, bytes'
            )
        else:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, unicode'
            )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += [indent + 'Allowed values:']
            else:
                output += [indent + 'Possible returned values:']
            for item in self.allowed_values:
                output += indent + '    ' + item + '\n'

        return output

    def __call__(self, value):

        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':
            if PY3:
                if not isinstance(value, (str, bytes)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, bytes'
                        'got type {0}.'.format(type(value))
                    )

                try:
                    value = value.decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            else:
                if not isinstance(value, (str, unicode)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, unicode'
                        ' got type {0}.'.format(type(value))
                    )

                try:
                    value = value.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value

        return value


class Date(object):

    def __init__(self, node, direction):
        self.direction = direction
        allowed_values = node.find('allowedValueList')
        if allowed_values is not None:
            allowed_values = list(value.text for value in allowed_values)
        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text

        self.default_value = default_value

    def __str__(self, indent=''):
        if PY3:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, bytes'
            )
        else:
            output = TEMPLATE.format(
                indent=indent,
                upnp_data_type=self.__name__,
                py_data_type='str, unicode'
            )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + self.default_value + '\n'

        if self.allowed_values is not None:

            if self.direction == 'in':
                output += [indent + 'Allowed values:']
            else:
                output += [indent + 'Possible returned values:']
            for item in self.allowed_values:
                output += indent + '    ' + item + '\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value

        if self.direction == 'in':
            if PY3:
                if not isinstance(value, (str, bytes)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, bytes'
                        'got type {0}.'.format(type(value))
                    )

                try:
                    value = value.decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            else:
                if not isinstance(value, (str, unicode)):
                    raise TypeError(
                        'Incorrect data type. Expected type str, unicode'
                        ' got type {0}.'.format(type(value))
                    )

                try:
                    value = value.encode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass

            if (
                self.allowed_values is not None and
                value not in self.allowed_values
            ):
                raise ValueError(
                    'Value {0} not allowed. allowed values are \n{1}'.format(
                        value,
                        self.allowed_values
                    )
                )

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value

        return value


class Boolean(object):

    def __init__(self, node, direction):
        self.direction = direction
        allowed = node.find('allowedValueList')

        if allowed is None:
            allowed_values = ['0', '1']
        else:
            allowed_values = list(value.text for value in allowed)
            if 'yes' in allowed_values:
                allowed_values = ['no', 'yes']
            elif 'Yes' in allowed_values:
                allowed_values = ['No', 'Yes']
            elif 'true' in allowed_values:
                allowed_values = ['false', 'true']
            elif 'True' in allowed_values:
                allowed_values = ['False', 'True']
            else:
                allowed_values = ['0', '1']

        self.allowed_values = allowed_values

        default_value = node.find('defaultValue')
        if default_value is not None:
            if default_value.text == 'NOT_IMPLEMENTED':
                self.default_value = 'NOT_IMPLEMENTED'
            else:
                default_value = default_value.text
                if default_value in ('yes', 'Yes', 'true', 'True', '1'):
                    default_value = True
                else:
                    default_value = False

        self.default_value = default_value

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            upnp_data_type=self.__name__,
            py_data_type='bool'
        )

        if self.default_value == 'NOT_IMPLEMENTED':
            return output + indent + 'NOT_IMPLEMENTED' + '\n'

        if self.default_value is not None:
            output += indent + 'Default: ' + repr(self.default_value) + '\n'

        if self.direction == 'in':
            output += indent + 'Allowed values: True/False\n'
        else:
            output += indent + 'Possible returned values: True/False\n'

        return output

    def __call__(self, value):
        if value is None:
            if self.default_value is None:
                if self.direction == 'in':
                    raise ValueError('A value must be supplied')

            else:
                value = self.default_value
                if self.direction == 'out':
                    value = self.allowed_values[int(value)]

        if self.direction == 'in':

            if isinstance(value, bool):
                value = self.allowed_values[int(value)]

            if value not in self.allowed_values:
                raise TypeError('Incorrect value')

        elif value is not None:
            if self.default_value == 'NOT_IMPLEMENTED':
                value = self.default_value
            else:
                value = bool(self.allowed_values.index(value))

        return value


TEMPLATE = '''
{indent}UPNP data type: {upnp_data_type}
{indent}Py data type: {py_data_type}
'''

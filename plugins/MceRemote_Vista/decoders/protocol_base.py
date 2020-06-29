

import math
import threading
from . import pronto
from . import code_wrapper
from . import (
    DecodeError,
    RepeatLeadIn,
    RepeatLeadOut
)


class Timer(object):
    def __init__(self, func, duration):
        self.func = func
        self.duration = duration
        self.event = threading.Event()
        self.thread = None

    def cancel(self):
        if self.thread is not None:
            self.event.set()
            self.thread.join()

    def stop(self):
        if self.thread is not None:
            self.event.set()
            self.thread.join()

        self.func()

    def start(self):
        self.cancel()
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        self.event.wait(self.duration)
        if not self.event.is_set():
            self.func()

        self.event.clear()
        self.thread = None

    @property
    def is_running(self):
        return self.thread is not None


class IRCode(object):

    def __init__(self, decoder, original_code, normalized_code, data):
        self._repeat_timer = Timer(decoder.reset, decoder.repeat_timeout)
        self._decoder = decoder
        self._original_code = original_code
        self._normalized_code = normalized_code
        self._data = data
        self._code = None
        self.name = None
        self.name = str(self)

    @property
    def repeat_timer(self):
        return self._repeat_timer

    def __iter__(self):
        yield 'decoder', self.decoder
        yield 'frequency', self.frequency
        for key, value in self._data.items():
            yield key, value

    @property
    def params(self):
        res = []
        if 'M' in self._data:
            res += ['mode']
        if 'OEM1' in self._data:
            res += ['oem1']
        if 'OEM2' in self._data:
            res += ['oem2']
        if 'D' in self._data:
            res += ['device']
        if 'S' in self._data:
            res += ['sub_device']
        if 'F' in self._data:
            res += ['function']
        if 'E' in self._data:
            res += ['extended_function']
        if 'T' in self._data:
            res += ['toggle']
        if 'CODE' in self._data:
            res += ['code']

        for key in self._data.keys():
            if key in 'MDSFETCP':
                continue

            if len(key) == 1 or key.startswith('H'):
                res += [key.lower()]

        return res

    @property
    def decoder(self):
        return self._decoder.__class__.__name__

    @property
    def frequency(self):
        return self._data['frequency']

    @property
    def original_rlc(self):
        return self._original_code[:]

    @property
    def normalized_rlc(self):
        return self._normalized_code[:]

    @property
    def original_pronto(self):
        code = [abs(item) for item in self._original_code]
        return pronto.rlc_to_pronto(self.frequency, code)

    @property
    def normalized_pronto(self):
        code = [abs(item) for item in self._normalized_code]
        return pronto.rlc_to_pronto(self.frequency, code)

    @property
    def device(self):
        return self._data.get('D', None)

    @property
    def sub_device(self):
        return self._data.get('S', None)

    @property
    def function(self):
        return self._data.get('F', None)

    @property
    def toggle(self):
        return self._data.get('T', None)

    @property
    def mode(self):
        return self._data.get('M', None)

    @property
    def n(self):
        return self._data.get('N', None)

    @property
    def g(self):
        return self._data.get('G', None)

    @property
    def x(self):
        return self._data.get('X', None)

    @property
    def extended_function(self):
        return self._data.get('E', None)

    @property
    def checksum(self):
        return self._data.get('CHECKSUM', None)

    @property
    def u(self):
        return self._data.get('U', None)

    @property
    def oem1(self):
        return self._data.get('OEM1', None)

    @property
    def oem2(self):
        return self._data.get('OEM2', None)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item.upper() in self._data:
            return self._data[item.upper()]

        raise AttributeError(item)

    def __eq__(self, other):
        if isinstance(other, list):
            return self.normalized_rlc == other

        if isinstance(other, IRCode):
            return (
                other.decoder == self.decoder and
                other._data == self._data
            )
        else:
            return other == self.normalized_pronto

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.name is None:
            res = []
            for key in self.params:
                value = getattr(self, key)
                res += [('%X' % (value,)).zfill(2)]

            return self.decoder + '.' + ':'.join(res)

        return self.name


class IrProtocolBase(object):
    irp = ''
    frequency = 36000
    tolerance = 1
    frequency_tolerance = 2
    bit_count = 0
    encoding = ''

    _lead_in = []
    _lead_out = []
    _bursts = []

    _repeat_lead_in = []
    _repeat_lead_out = []
    _middle_timings = []
    _repeat_bursts = []

    _parameters = []
    encode_parameters = []
    repeat_timeout = 0

    def __init__(self):
        self._last_code = None

    def reset(self):
        pass

    def _test_decode(self, rlc=None, params=None):
        # print self.__class__.__name__, 'decode test.....'
        self.tolerance = 1
        if rlc is None:
            return
        for i in range(len(rlc)):
            data = rlc[i]
            param = params[i]
            try:
                code = self.decode(data, self.frequency)
            except (RepeatLeadIn, RepeatLeadOut):
                continue

            else:
                for key, value in param.items():
                    if getattr(code, key) != value:
                        print code
                        print i, key, value, getattr(code, key)
                        print data

                        code = code_wrapper.CodeWrapper(
                            self.encoding,
                            self._lead_in,
                            self._lead_out,
                            self._middle_timings,
                            self._bursts,
                            self.tolerance,
                            data[:]
                        )

                        print code._stream_pairs
                        raise RuntimeError

        print 'Decode Success', code

    def _test_encode(self, params=None):
        if params is None:
            return

        codes = self.encode(**params)
        found_code = None
        for code in codes:
            try:
                code = self.decode(code)
            except:
                continue

            if code is not None:
                found_code = code

        if found_code is None:
            raise AssertionError('encode failed.')

        for key, value in params.items():
            assert getattr(found_code, key) == value

    def encode(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def _reverse_bits(cls, value, num_bits):
        res = 0

        for i in range(num_bits):
            res = cls._set_bit(res, (~i + num_bits), cls._get_bit(value, i))

        return res

    @classmethod
    def _count_one_bits(cls, value):
        count = 0

        for i in range(64):
            count += int(cls._get_bit(value, i))

        return count

    @classmethod
    def _get_bits(cls, data, start_bit, stop_bit):
        res = 0
        for i in range(start_bit, stop_bit + 1):
            res = cls._set_bit(res, i - start_bit, cls._get_bit(data, i))

        return res

    def _build_packet(self, *data):
        data = list(data)

        if self.encoding == 'msb':
            for i, items in enumerate(data):
                if isinstance(items, list):
                    new_data = []
                    for item in items:
                        new_data.insert(0, item)

                    data[i] = new_data[:]

        def flatten_and_compress(lst):
            res = []
            for itm in lst:
                if isinstance(itm, int):
                    if res and (res[-1] > 0 < itm or res[-1] < 0 > itm):
                        res[-1] += itm
                    else:
                        res += [itm]
                else:
                    res += flatten_and_compress(itm)
                    res = flatten_and_compress(res)

            return res

        packet = []

        for item in data:
            if isinstance(item, tuple):
                packet += [item]
            else:
                packet += item

        packet = self._lead_in[:] + packet

        if self._lead_out and self._lead_out[-1] > 0:
            total_time = self._lead_out[-1]
            packet = flatten_and_compress(packet + self._lead_out[:-1])
            run_time = sum(abs(item) for item in packet)
            run_time = -(total_time - run_time)
            packet += [run_time]
        else:
            packet = flatten_and_compress(packet + self._lead_out)

        return packet[:]

    def decode(self, data, frequency=0):
        if not self._match(frequency, self.frequency, self.frequency_tolerance / 10.0):
            raise DecodeError('Incorrect frequency')

        code = code_wrapper.CodeWrapper(
            self.encoding,
            self._lead_in[:],
            self._lead_out[:],
            self._middle_timings[:],
            self._bursts[:],
            self.tolerance,
            data[:]
        )

        if code.num_bits > self.bit_count:
            raise DecodeError('To many bits')
        elif code.num_bits < self.bit_count:
            raise DecodeError('Not enough bits')

        params = dict(frequency=self.frequency)
        for name, start, stop in self._parameters:
            params[name] = code.get_value(start, stop)

        c = IRCode(self, code.original_code, list(code), params)
        c._code = code
        return c

    def _get_timing(self, num, index):
        return self._bursts[self._get_bit(num, index)]

    @staticmethod
    def _set_bit(value, bit_num, state):
        if state:
            return value | (1 << bit_num)
        else:
            return value & ~(1 << bit_num)

    @staticmethod
    def _get_bit(value, bit_num):
        return int(value & (1 << bit_num) > 0)

    @classmethod
    def _invert_bits(cls, n, num_bits):
        res = 0

        for i in range(num_bits):
            res = cls._set_bit(res, i, not cls._get_bit(n, i))

        return res

    def _match(self, value, expected_timing_value, tolerance=None):
        if tolerance is None:
            tolerance = self.tolerance

        high = math.floor(expected_timing_value + (expected_timing_value * (tolerance / 100.0)))
        low = math.floor(expected_timing_value - (expected_timing_value * (tolerance / 100.0)))

        # do a flip flop of the high and low so the same expression can
        # be used when evaluating a raw timing
        if expected_timing_value < 0:
            low, high = high, low

        return low <= value <= high


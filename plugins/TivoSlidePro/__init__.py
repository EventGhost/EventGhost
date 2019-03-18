ur"""<rst>
Plugin for Tivo Slide Pro 
"""

import eg
from threading import Timer

eg.RegisterPlugin(
    name = "Tivo Slide Pro",
    author = "BirdAPI (Anthony Casagrande)",
    version = "1.0.0",
    kind = "remote",
    guid = "{a5dcbf10-6530-11d2-901f-00c04fb951ed}",
    description = __doc__,
    hardwareId = "USB\\VID_150A&PID_1203",
)

ALPHABET_START = 4
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
NUM_START = 30
NUMPAD_START = 89
NUMBERS = "1234567890"
SYM_NUMS = "!@#$%^&*()"
SYMBOLS = {
    0: {
        40: 'Enter',
        42: 'Backspace',
        44: 'Space',
        45: '-',
        46: '=',
        47: '[',
        48: ']',
        49: '\\',
        51: ';',
        52: "'",
        53: '`',
        54: ',',
        55: '.',
        56: '/',
        79: 'Right',
        80: 'Left',
        81: 'Down',
        82: 'Up',
        119: 'Select',
        156: 'Clear'
    },
    2: {
        45: '_',
        46: '+',
        47: '{',
        48: '}',
        49: '|',
        51: ':',
        52: '"',
        53: '~',
        54: '<',
        55: '>',
        56: '?'
    }
}

BUTTONS = {
    1: {
        216: 'Clear'
    },
    16: {
        48: 'TVPower',
        130: 'Input',
        9: 'Info',
        70: 'Back',
        109: 'Zoom',
        66: 'Up',
        67: 'Down',
        68: 'Left',
        69: 'Right',
        65: 'Select',
        233: 'VolumeUp',
        234: 'VolumeDown',
        141: 'Guide',
        156: 'ChannelUp',
        157: 'ChannelDown',
        226: 'Mute',
        178: 'Record',
        176: 'Play',
        180: 'Rewind',
        177: 'Pause',
        179: 'FastForward',
        245: 'SlowMo',
        182: 'BackArrow',
        181: 'ForwardArrow',
        108: 'Yellow',
        107: 'Blue',
        105: 'Red',
        106: 'Green',
        131: 'Enter',
        33: 'Search'
    },
    17: {
        61: 'TivoLogo',
        62: 'LiveTV',
        65: 'ThumbsDown',
        66: 'ThumbsUp'
    }
}

ACTIONS = {
    16: {
    },
    17: {
        128: 'SlideOpen',
        129: 'SlideClosed'
    }
}

SYMBOL_REPLACE = {
    '&': 'Ampersand',
    '"': 'Quote',
    '<': 'LessThan',
    '>': 'GreaterThan',
    "'": 'Apostrophe',
    ',': 'Comma',
    '.': 'Period',
    '*': 'Asterik',
    '!': 'ExclamationMark',
    '@': 'AtSymbol',
    '#': 'Pound',
    '$': 'DollarSign',
    '%': 'Percent',
    '^': 'Caret',
    '(': 'OpenParen',
    ')': 'CloseParen',
    '~': 'Tilde',
    '_': 'Underscore',
    '+': 'Plus',
    '{': 'OpenCurlyBrace',
    '}': 'CloseCurlyBrace',
    '`': 'Backtick',
    '-': 'Minus',
    '=': 'Equals',
    '[': 'OpenSquareBracket',
    ']': 'CloseSquareBracket',
    '\\': 'Backslash',
    '|': 'VerticalBar',
    ';': 'Semicolon',
    ':': 'Colon',
    '?': 'QuestionMark',
    '/': 'Slash'
}

class Tivo(eg.PluginBase):

    def __init__(self):
        self.AddAction(SimulateLastKeypress)

    @eg.LogIt
    def __start__(self):
        self.last_event = (None, -1)
        self.usb = eg.WinUsb(self)
        self.usb.AddDevice(
            "Tivo Slide Pro",
            "USB\\VID_150A&PID_1203",
            "{a5dcbf10-6530-11d2-901f-00c04fb951ed}",
            self.KeypadCallback,
            9
        )
        self.usb.Open()

    def __stop__(self):
        self.usb.Close()

    def send_enduring_event(self, prefix, evt, start_bit):
        payload = None
        if prefix == "Keyboard":
            if evt in SYMBOL_REPLACE:
                payload = evt
                evt = SYMBOL_REPLACE[evt]
        self.last_event = (evt, start_bit)
        self.TriggerEnduringEvent("SlidePro." + prefix + '.' + evt, payload)
        
    def end_event(self):
        self.EndLastEvent()
        self.last_event = (None, -1)
        
    def KeypadCallback(self, data):
        start_bit = data[0]
        is_end = False
        if self.last_event[0] is not None and start_bit == self.last_event[1]:
            is_end = True
            self.end_event()
        elif start_bit == 1:
            #Keyboard
            key_bit = 3
            key_code = data[key_bit]
            caps_bit = 1
            is_caps = data[caps_bit] == 2
            if key_code >= ALPHABET_START and key_code < ALPHABET_START + len(ALPHABET):
                key = ALPHABET[key_code - ALPHABET_START]
                if is_caps: 
                    key = key.upper()
                self.send_enduring_event("Keyboard", key, start_bit)
            elif key_code >= NUM_START and key_code < NUM_START + len(NUMBERS):
                if is_caps:
                    key = SYM_NUMS[key_code - NUM_START]
                    self.send_enduring_event("Keyboard", key, start_bit)
                else:
                    key = NUMBERS[key_code - NUM_START]
                    self.send_enduring_event("Button", key, start_bit)
            elif key_code >= NUMPAD_START and key_code < NUMPAD_START + len(NUMBERS):
                key = NUMBERS[key_code - NUMPAD_START]
                self.send_enduring_event("Keyboard", key, start_bit)
            elif key_code in SYMBOLS[data[caps_bit]]:
                key = SYMBOLS[data[caps_bit]][key_code]
                self.send_enduring_event("Keyboard", key, start_bit)
            elif key_code in BUTTONS[start_bit]:
                key = BUTTONS[start_bit][key_code]
                self.send_enduring_event("Button", key, start_bit)
        elif start_bit in [16, 17]:
            key_bit = 1
            key_code = data[key_bit]
            if key_code in BUTTONS[start_bit]:
                key = BUTTONS[start_bit][key_code]
                self.send_enduring_event("Button", key, start_bit)
            elif key_code in ACTIONS[start_bit]:
                key = ACTIONS[start_bit][key_code]
                self.send_enduring_event("Action", key, start_bit)
        elif start_bit == 19:
            # Ignore it, it only seems to happen with tivo button
            pass
        
        # if not is_end: 
            # eg.PrintError("({0})".format(', '.join(map(str,data))))
            
class SimulateLastKeypress(eg.ActionBase):
    def __call__(self):
        key = eg.event.payload if eg.event.payload is not None else eg.event.suffix[eg.event.suffix.rfind('.')+1:]
        self.send_key_evt(key)        

    def send_key_evt(self, evt):
        if evt == "Clear": 
            self.send_key("{Delete}")
        if evt == "{":
            self.send_key("{{")
        elif evt == "Select":
            self.send_key("{Enter}")
        elif len(evt) == 1:
            self.send_key(evt)
        else:
            self.send_key("{%s}" % evt)
    
    def send_key(self, data):
        hwnds = eg.lastFoundWindows
        if not hwnds:
            hwnd = None
        else:
            hwnd = hwnds[0]
        eg.SendKeys(hwnd, data, False)        
        
        
from ctypes.wintypes import (
    UINT,
)

from ctypes import POINTER, Structure, Union, c_ulonglong


MAXPNAMELEN = 32
MAXERRORLENGTH = 256
MAX_JOYSTICKOEMVXDNAME = 260

MM_MICROSOFT = 1 # /* Microsoft Corporation */


MM_MIDI_MAPPER = 1 # /* MIDI Mapper */
MM_WAVE_MAPPER = 2 # /* Wave Mapper */
MM_SNDBLST_MIDIOUT = 3 # /* Sound Blaster MIDI output port */
MM_SNDBLST_MIDIIN = 4 # /* Sound Blaster MIDI input port */
MM_SNDBLST_SYNTH = 5 # /* Sound Blaster internal synthesizer */
MM_SNDBLST_WAVEOUT = 6 # /* Sound Blaster waveform output */
MM_SNDBLST_WAVEIN = 7 # /* Sound Blaster waveform input */
MM_ADLIB = 9 # /* Ad Lib-compatible synthesizer */
MM_MPU401_MIDIOUT = 10 # /* MPU401-compatible MIDI output port */
MM_MPU401_MIDIIN = 11 # /* MPU401-compatible MIDI input port */
MM_PC_JOYSTICK = 12 # /* Joystick adapter */


MMVERSION = UINT # /* major (high byte), minor (low byte) */
VERSION = UINT # /* major (high byte), minor (low byte) */


LPUINT = POINTER(UINT)


class MIDI(Structure):
    _fields_ = [
        ('songptrpos', DWORD)
    ]


class SMPTE(Structure):
    _fields_ = [
        ('hour', BYTE),
        ('min', BYTE),
        ('sec', BYTE),
        ('frame', BYTE),
        ('fps', BYTE),
        ('dummy', BYTE),
        ('pad', BYTE * 2),
    ]


class U(Union):
    _fields_ = [
        ('ms', DWORD),
        ('sample', DWORD),
        ('cb', DWORD),
        ('ticks', DWORD),
        ('smpte', SMPTE),
        ('midi', MIDI)
    ]


class MMTIME(Structure):
    _fields_ = [
        ('wType', UINT),
        ('u', U)
    ]


PMMTIME = POINTER(MMTIME)
NPMMTIME = POINTER(MMTIME)
LPMMTIME = POINTER(MMTIME)


TIME_MS = 0x0001 # /* time in milliseconds */
TIME_SAMPLES = 0x0002 # /* number of wave samples */
TIME_BYTES = 0x0004 # /* current byte offset */
TIME_SMPTE = 0x0008 # /* SMPTE time */
TIME_MIDI = 0x0010 # /* MIDI time */
TIME_TICKS = 0x0020 # /* Ticks within MIDI stream */

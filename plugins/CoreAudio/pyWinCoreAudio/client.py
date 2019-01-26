

import comtypes
import threading
import ctypes
from ctypes.wintypes import (
    DWORD,
    BYTE,
)

from __core_audio.iid import (
    IID_IAudioCaptureClient,
    IID_IAudioClock,
    IID_IAudioClock2,
    IID_IAudioRenderClient,
    IID_IAudioSessionControl,
    IID_IAudioStreamVolume,
    IID_IChannelAudioVolume,
    IID_IMFTrustedOutput,
    IID_ISimpleAudioVolume
)

from __core_audio.enum import AUDCLNT_SHAREMODE
AudioClientProperties

REFTIMES_PER_SEC = 10000000
REFTIMES_PER_MILLISEC = 10000
REFERENCE_TIME = ctypes.c_longlong
UINT32 = ctypes.c_uint32
LPUINT32 = POINTER(UINT32)
LPBYTE = POINTER(BYTE)


class AudioRenderClient(object):

    def __init__(self, audio_client, render_client):
        self.__audio_client = audio_client
        self.__render_client = render_client

    def play_stream(self, stream, shared_mode):

        def do(strm, mode):
            hnsRequestedDuration = REFERENCE_TIME(REFTIMES_PER_SEC)
            hnsActualDuration = REFERENCE_TIME
            bufferFrameCount = UINT32
            numFramesAvailable = UINT32
            pData = LPBYTE
            flags = DWORD(0)

            pwfx = self.__audio_client.mix_format


            if mode:
                mode = AUDCLNT_SHAREMODE.AUDCLNT_SHAREMODE_SHARED
            else:
                mode = AUDCLNT_SHAREMODE.AUDCLNT_SHAREMODE_EXCLUSIVE

            self.__audio_client.initialize(
                mode,
                0,
                hnsRequestedDuration,
                0,
                pwfx,
                NULL

            )


class AudioClient(object):

    def __init__(self, audio_client):
        self.__audio_client = audio_client

    @property
    def buffer_size(self):
        try:
            return self.__audio_client.GetBufferSize()
        except comtypes.COMError:
            raise AttributeError

    @property
    def padding(self):
        try:
            return self.__audio_client.GetCurrentPadding()
        except comtypes.COMError:
            raise AttributeError

    @property
    def period(self):
        try:
            return self.__audio_client.GetDevicePeriod()[0]
        except comtypes.COMError:
            raise AttributeError

    @property
    def min_period(self):
        try:
            return self.__audio_client.GetDevicePeriod()[1]
        except comtypes.COMError:
            raise AttributeError

    @property
    def latency(self):
        try:
            return self.__audio_client.GetStreamLatency()
        except comtypes.COMError:
            raise AttributeError

    def reset(self):
        try:
            self.__audio_client.Reset()
        except comtypes.COMError:
            pass

    def start(self):
        try:
            self.__audio_client.Start()
        except comtypes.COMError:
            pass

    def stop(self):
        try:
            self.__audio_client.Stop()
        except comtypes.COMError:
            pass

    @property
    def mix_format(self):
        try:
            return self.__audio_client.GetMixFormat()
        except comtypes.COMError:
            raise AttributeError

    @property
    def capture_client(self):
        try:
            return self.__audio_client.GetService(IID_IAudioCaptureClient)
        except comtypes.COMError:
            raise AttributeError

    @property
    def render_client(self):
        try:
            return self.__audio_client.GetService(IID_IAudioRenderClient)
        except comtypes.COMError:
            raise AttributeError

    @property
    def simple_volume(self):
        try:
            return self.__audio_client.GetService(IID_ISimpleAudioVolume)
        except comtypes.COMError:
            raise AttributeError

    @property
    def channel_volume(self):
        try:
            return self.__audio_client.GetService(IID_IChannelAudioVolume)
        except comtypes.COMError:
            raise AttributeError

    @property
    def stream_volume(self):
        try:
            return self.__audio_client.GetService(IID_IAudioStreamVolume)
        except comtypes.COMError:
            raise AttributeError

    @property
    def session_control(self):
        try:
            return self.__audio_client.GetService(IID_IAudioSessionControl)
        except comtypes.COMError:
            raise AttributeError

    @property
    def clock(self):
        try:
            return self.__audio_client.GetService(IID_IAudioClock2)
        except comtypes.COMError:
            pass
        try:
            return self.__audio_client.GetService(IID_IAudioClock)
        except comtypes.COMError:
            raise AttributeError

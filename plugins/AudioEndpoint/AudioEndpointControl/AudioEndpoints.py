# -*- coding: utf-8 -*-
"""Defines the main classes AudioEndpoints, AudioEndpoint and AudioVolume"""

from __future__ import print_function, unicode_literals, absolute_import

from ctypes import POINTER as _POINTER
from functools import partial as _partial
from _ctypes import COMError
from win32api import FormatMessage  # pylint: disable=no-name-in-module

from comtypes import CoCreateInstance, CLSCTX_INPROC_SERVER, CLSCTX_ALL, GUID

from .MMConstants import (Render, Console, DEVICE_STATE_ACTIVE,
                          Device_FriendlyName, STGM_READ)
try:
    # Try to import local .MMDeviceAPILib for Python 2.6 compatibility
    from .MMDeviceAPILib import (MMDeviceEnumerator as _MMDeviceEnumerator,
                                 IMMDeviceEnumerator as _IMMDeviceEnumerator,
                                 IMMNotificationClient)
except ImportError:
    # Use comtypes to generate MMDeviceAPILib (Python 2.7+))
    from comtypes.client import GetModule
    GetModule("mmdeviceapi.tlb")
    from comtypes.gen.MMDeviceAPILib import (
        MMDeviceEnumerator as _MMDeviceEnumerator,
        IMMDeviceEnumerator as _IMMDeviceEnumerator,
        IMMNotificationClient)
from .Notifications import CAudioEndpointVolumeCallback, CMMNotificationClient
from .EndpointvolumeAPI import (IAudioEndpointVolume as _IAudioEndpointVolume,
                                IID_IAudioEndpointVolume)
from .PolicyConfigAPI import CLSID_CPolicyConfigVistaClient, IPolicyConfigVista

_CLSID_MMDeviceEnumerator = _MMDeviceEnumerator._reg_clsid_


def _GetValue(value):
    # Need to do this in a function as comtypes seems to
    # have a problem if it's in a class.

    # Types for vt defined here:
    # https://msdn.microsoft.com/en-us/library/windows/desktop/aa380072%28v=vs.85%29.aspx
    if value.vt == 0:
        return None
    elif value.vt == 31:
        return value.__MIDL____MIDL_itf_mmdeviceapi_0003_00850001.pwszVal
    return value.__MIDL____MIDL_itf_mmdeviceapi_0003_00850001.cVal


def _FunctionCallback(Function, Callback, Msg):
    try:
        hr = Function(Callback)
        if hr:
            raise Exception("{0} returned:".format(Msg), FormatMessage(hr))
    except COMError as e:
        raise Exception("{0} error:".format(Msg), e.text)


class AudioVolume(object):
    """Wrapper for volume related methods."""
    def __init__(self, endpoint, EventContext=None):
        self._callback = None
        self.endpoint = endpoint
        self.EventContext = EventContext

        self._AudioEndpointVolume = _POINTER(_IAudioEndpointVolume)(
            endpoint._endpoint.Activate(IID_IAudioEndpointVolume,
                                        CLSCTX_INPROC_SERVER, None))

    def GetChannelCount(self):
        """Gets a count of the channels in the audio stream."""
        return self._AudioEndpointVolume.GetChannelCount()

    def __len__(self):
        return self.GetChannelCount()

    def Get(self, Channel=0, Scalar=True):
        """
        When Scalar=True: Gets the master volume level, expressed as
        (default)         a normalized, audio-tapered value.

        When Scalar=False: Gets the master volume level of the
                           audio stream, in decibels.

        When Scalar=True: Gets the normalized, audio-tapered volume
        (default)         level of the specified channel of the audio stream.

        When Scalar=False: Gets the volume level, in decibels, of the
                           specified channel in the audio stream.
        """
        if Channel == 0:
            if Scalar:
                return self._AudioEndpointVolume.GetMasterVolumeLevelScalar()
            else:
                return self._AudioEndpointVolume.GetMasterVolumeLevel()

        if Scalar:
            return self._AudioEndpointVolume.GetChannelVolumeLevelScalar(
                Channel-1)

        return self._AudioEndpointVolume.GetChannelVolumeLevel(Channel-1)

    def Set(self, LevelDB, Channel=0, Scalar=True):
        """
        When Scalar=True: Sets the master volume level, expressed as
        (default)         a normalized, audio-tapered value.

        When Scalar=False: Sets the master volume level of the
                           audio stream, in decibels.

        When Scalar=True: Sets the normalized, audio-tapered volume level of
        (default)         the specified channel in the audio stream.

        When Scalar=False: Sets the volume level, in decibels, of the
                           specified channel of the audio stream.

        """
        if isinstance(LevelDB, bool):
            self._AudioEndpointVolume.SetMute(LevelDB, self.EventContext)
        elif Channel == 0:
            if Scalar:
                self._AudioEndpointVolume.SetMasterVolumeLevelScalar(
                    LevelDB, self.EventContext)
            else:
                self._AudioEndpointVolume.SetMasterVolumeLevel(
                    LevelDB, self.EventContext)
        else:
            if Scalar:
                self._AudioEndpointVolume.SetChannelVolumeLevelScalar(
                    Channel-1, LevelDB, self.EventContext)
            else:
                self._AudioEndpointVolume.SetChannelVolumeLevel(
                    Channel-1, LevelDB, self.EventContext)

    def GetRange(self):
        """Gets the volume range of the audio stream, in decibels."""
        return self._AudioEndpointVolume.GetVolumeRange()

    def StepDown(self):
        """Decreases the volume level by one step."""
        return self._AudioEndpointVolume.VolumeStepDown(self.EventContext)

    def StepUp(self):
        """Increases the volume level by one step."""
        return self._AudioEndpointVolume.VolumeStepUp(self.EventContext)

    def GetStepInfo(self):
        """Gets information about the current step in the volume range."""
        return self._AudioEndpointVolume.GetVolumeStepInfo()

    def QueryHardwareSupport(self):
        """
        Queries the audio endpoint device for its hardware-supported functions.
        """
        return self._AudioEndpointVolume.QueryHardwareSupport()

    def RegisterCallback(self, callback):
        """Registers the endpoint's notification callback interface."""
        self._callback = CAudioEndpointVolumeCallback(callback, self.endpoint)
        _FunctionCallback(
            self._AudioEndpointVolume.RegisterControlChangeNotify,
            self._callback, "RegisterControlChangeNotify")

    def UnregisterCallback(self):
        """Unregister the endpoint's volume notification callback interface."""
        _FunctionCallback(
            self._AudioEndpointVolume.UnregisterControlChangeNotify,
            self._callback, "UnregisterControlChangeNotify")
        self._callback = None

    def __add__(self, other=1):
        for _ in range(other):
            self.StepUp()

    def __sub__(self, other=1):
        for _ in range(other):
            self.StepDown()

    def __int__(self):
        return int(self.GetChannelCount())

    def __float__(self):
        return self[0]

    def __str__(self):
        return 'Volume: {0}'.format(self[0])

    @property
    def Mute(self):  # TODO: Missing method docstring (missing-docstring)
        return bool(self._AudioEndpointVolume.GetMute())

    @Mute.setter
    def Mute(self, bMute):
        self.Set(bMute)

    def __eq__(self, other):
        """Tests if two endpoint devices are the same."""
        return self.endpoint.getId() == other.endpoint.getId()

    def __ne__(self, other):
        """Tests if two endpoint devices are not the same."""
        return self.endpoint.getId() != other.endpoint.getId()

    def __ge__(self, other):
        """Tests if two endpoint devices are not the same."""  # FIX:
        return float(self) >= float(other)

    def __le__(self, other):
        """Tests if two endpoint devices are not the same."""  # FIX:
        return float(self) <= float(other)

    __getitem__ = Get
    __setitem__ = _partial(Set, Scalar=True)
    __pos__ = __add__
    __neg__ = __sub__


class AudioEndpoint(object):
    """Wrapper for a single COM endpoint."""
    def __init__(self, endpoint, endpoints, PKEY_Device=Device_FriendlyName,
                 EventContext=None):
        """Initializes an endpoint object."""
        self._endpoint = endpoint
        self.endpoints = endpoints
        self.PKEY_Device = PKEY_Device
        self.EventContext = EventContext
        self._AudioVolume = AudioVolume(self, self.EventContext)
        self.RegisterCallback = self._AudioVolume.RegisterCallback
        self.UnregisterCallback = self._AudioVolume.UnregisterCallback

    @property
    def volume(self):  # TODO: Missing method docstring (missing-docstring)
        return self._AudioVolume

    @volume.setter
    def volume(self, LevelDB):
        return self._AudioVolume.Set(LevelDB)

    def getName(self):
        """Return an endpoint devices FriendlyName."""
        pStore = self._endpoint.OpenPropertyStore(STGM_READ)
        return _GetValue(pStore.GetValue(self.PKEY_Device))

    def getId(self):
        """Gets a string that identifies the device."""
        return self._endpoint.GetId()

    def getState(self):
        """Gets the current state of the device."""
        return self._endpoint.GetState()

    def isDefault(self, role=Console, dataFlow=Render):
        """Return if endpoint device is default or not."""
        return self == self.endpoints.GetDefault(role, dataFlow)

    def GetMute(self):
        """Gets the muting state of the audio stream."""
        return self._AudioVolume.Mute

    def SetMute(self, Mute):
        """Sets the muting state of the audio stream."""
        self._AudioVolume.Mute = Mute

    def __eq__(self, other):
        """Tests if two endpoint devices are the same."""
        return self.getId() == other.getId()

    def __ne__(self, other):
        """Tests if two endpoint devices are not the same."""
        return self.getId() != other.getId()

    __unicode__ = getName

    def __str__(self):
        return str(self.getName())


class AudioEndpoints(object):
    """The main class to access all endpoints in the system"""

    def __init__(self, DEVICE_STATE=DEVICE_STATE_ACTIVE,
                 PKEY_Device=Device_FriendlyName,
                 EventContext=GUID.create_new()):
        self.DEVICE_STATE = DEVICE_STATE
        self.PKEY_Device = PKEY_Device
        self.EventContext = EventContext
        self._DevEnum = CoCreateInstance(_CLSID_MMDeviceEnumerator,
                                         _IMMDeviceEnumerator,
                                         CLSCTX_INPROC_SERVER)
        self._callback = None
        self._PolicyConfig = None

    # TODO: Missing class docstring (missing-docstring)
    def GetDefault(self, role=Console, dataFlow=Render):
        return AudioEndpoint(self._DevEnum.GetDefaultAudioEndpoint(dataFlow,
                                                                   role),
                             self, self.PKEY_Device, self.EventContext)

    # TODO: Missing class docstring (missing-docstring)
    def SetDefault(self, endpoint, role=Console):
        OldDefault = self.GetDefault(role)

        if self._PolicyConfig is None:
            self._PolicyConfig = CoCreateInstance(
                CLSID_CPolicyConfigVistaClient, IPolicyConfigVista, CLSCTX_ALL)

        hr = self._PolicyConfig.SetDefaultEndpoint(endpoint.getId(), role)
        if hr:
            print('SetDefaultEndpoint', FormatMessage(hr))
        return OldDefault

    def RegisterCallback(self, callback):
        """Register endpoints notification callback interface."""
        self._callback = CMMNotificationClient(callback, self)
        _FunctionCallback(self._DevEnum.RegisterEndpointNotificationCallback,
                          self._callback,
                          "RegisterEndpointNotificationCallback")

    def UnregisterCallback(self):
        """Unregister endpoints notification callback interface."""
        _FunctionCallback(
            self._DevEnum.UnregisterEndpointNotificationCallback,
            self._callback, "UnregisterEndpointNotificationCallback")
        self._callback = None

    def __call__(self, ID):
        try:
            return AudioEndpoint(self._DevEnum.GetDevice(ID), self,
                                 self.PKEY_Device, self.EventContext)
        except COMError:
            for endpoint in self:
                if endpoint.getName() == ID:
                    return endpoint
            raise

    def __str__(self):
        return str([str(endpoint) for endpoint in self])

    # TODO: Missing class docstring (missing-docstring)
    def ChangeFilter(self, DEVICE_STATE=None, PKEY_Device=None):
        if DEVICE_STATE is not None:
            self.DEVICE_STATE = DEVICE_STATE
        if PKEY_Device is not None:
            self.PKEY_Device = PKEY_Device

    def __iter__(self, dataFlow=Render):
        pEndpoints = self._DevEnum.EnumAudioEndpoints(dataFlow,
                                                      self.DEVICE_STATE)
        for i in range(pEndpoints.GetCount()):
            yield AudioEndpoint(pEndpoints.Item(i), self, self.PKEY_Device,
                                self.EventContext)

    # pylint: disable=invalid-length-returned
    def __len__(self):
        return int(self._DevEnum.EnumAudioEndpoints(
            Render, self.DEVICE_STATE).GetCount())

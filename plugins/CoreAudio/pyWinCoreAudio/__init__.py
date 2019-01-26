
import comtypes
from endpoint import AudioDefaultEndpoint
from __core_audio.enum import EDataFlow
from __core_audio.devicetopologyapi import PIDeviceTopology
from __core_audio.iid import IID_IDeviceTopology
from device import (
    AudioDevice,
    AudioDeviceEnumerator,
    AudioNotificationClient
)
from __core_audio.constant import (
    PKEY_DeviceInterface_FriendlyName,
    STGM_READ
)

CLSCTX_INPROC_SERVER = comtypes.CLSCTX_INPROC_SERVER


class AudioWaveFormat(object):

    def __init__(self, client):
        self.__client = client


class AudioDevices(object):

    def __init__(self):
        comtypes.CoInitialize()

        self.__callbacks = []
        self.__device_enum = AudioDeviceEnumerator()

        self.__notification_client = AudioNotificationClient(
            self.__device_enum,
            self.__callbacks
        )
        self.__device_enum.register_endpoint_notification_callback(
            self.__notification_client
        )

    def register_notification_callback(self, callback):
        self.__callbacks += [callback]

    def unregister_notification_callback(self, callback):
        self.__callbacks.remove(callback)

    @property
    def default_render_endpoint(self):
        return AudioDefaultEndpoint(self.__device_enum, EDataFlow.eRender)

    @property
    def default_capture_endpoint(self):
        return AudioDefaultEndpoint(self.__device_enum, EDataFlow.eCapture)

    @property
    def __devices(self):
        used_names = []

        for endpt in self.__device_enum.endpoints:
            pStore = endpt.OpenPropertyStore(STGM_READ)
            try:
                name = pStore.GetValue(PKEY_DeviceInterface_FriendlyName)
            except comtypes.COMError:
                continue

            if name not in used_names:
                used_names += [name]
                device_topology = comtypes.cast(
                    endpt.Activate(
                        IID_IDeviceTopology,
                        CLSCTX_INPROC_SERVER
                    ),
                    PIDeviceTopology
                )

                yield AudioDevice(
                    device_topology.GetDeviceId(),
                    self.__device_enum
                )

    def __iter__(self):
        for dev in self.__devices:
            yield dev

    def __contains__(self, item):
        for dev in self:
            if item in (dev.name, dev.id):
                return True
        return False

    def __getitem__(self, item):
        if isinstance(item, (slice, int)):
            return list(self)[item]

        for dev in self:
            if item in (dev.name, dev.id):
                return dev
        raise AttributeError


comtypes.CoInitialize()

AudioDevices = AudioDevices()


def stop():
    comtypes.CoUninitialize()


if __name__ == '__main__':
    registered_volume_callbacks = {}

    import threading
    print_lock = threading.Lock()

    class Callbacks:

        @staticmethod
        def session_created(new_session):
            session_endpoint = new_session.session_manager.endpoint
            session_device = session_endpoint.device
            print_lock.acquire()

            print 'audio session created'
            print '    device name:', session_device.name
            print '    endpoint name:', session_endpoint.name
            print '    name:', new_session.name
            print '    id:', new_session.id
            print '    instance id:', new_session.instance_id
            print '    process id:', new_session.process_id
            print '    is system sounds:', new_session.is_system_sounds
            print '    grouping param:', new_session.grouping_param
            print '    icon:', new_session.icon
            print '    state:', new_session.state
            print
            print
            print_lock.release()

            new_session.register_notification_callback(Callbacks)

        @staticmethod
        def session_name_changed(session, new_name):
            session_endpoint = session.session_manager.endpoint
            session_device = session_endpoint.device

            print_lock.acquire()

            print 'audio session name changed'
            print '    device name:', session_device.name
            print '    endpoint name:', session_endpoint.name
            print '    name:', new_name
            print
            print
            print_lock.release()

        @staticmethod
        def session_grouping_changed(session, new_group):
            session_endpoint = session.session_manager.endpoint
            session_device = session_endpoint.device

            print_lock.acquire()

            print 'audio session grouping changed'
            print '    device name:', session_device.name
            print '    endpoint name:', session_endpoint.name
            print '    name:', session.name
            print '    grouping param:', new_group
            print
            print
            print_lock.release()

        @staticmethod
        def session_icon_path_changed(session, new_path):
            session_endpoint = session.session_manager.endpoint
            session_device = session_endpoint.device

            print_lock.acquire()

            print 'audio session icon path changed'
            print '    device name:', session_device.name
            print '    endpoint name:', session_endpoint.name
            print '    name:', session.name
            print '    icon path:', new_path
            print '    icon:', session.icon
            print
            print
            print_lock.release()

        @staticmethod
        def session_disconnect(
            session_endpoint,
            session_name,
            session_id,
            disconnect_reason
        ):
            session_device = session_endpoint.device

            print_lock.acquire()

            print 'audio session disconnected'
            print '    device name:', session_device.name
            print '    endpoint name:', session_device.name
            print '    name:', session_name
            print '    id:', session_id
            print '    disconnect reason:', disconnect_reason
            print
            print
            print_lock.release()

        @staticmethod
        def session_volume_changed(session, new_volume, mute):
            session_endpoint = session.session_manager.endpoint
            session_device = session_endpoint.device

            print_lock.acquire()

            print 'audio session volume changed'
            print '    device name:', session_device.name
            print '    endpoint name:', session_endpoint.name
            print '    name:', session.name
            print '    volume:', new_volume
            print '    mute:', mute
            print
            print
            print_lock.release()

        @staticmethod
        def session_state_changed(session, state):
            session_endpoint = session.session_manager.endpoint
            session_device = session_endpoint.device

            print_lock.acquire()

            print 'audio session state changed'
            print '    device name:', session_device.name
            print '    endpoint name:', session_endpoint.name
            print '    name:', session.name
            print '    id:', session.id
            print '    instance id:', session.instance_id
            print '    process id:', session.process_id
            print '    is system sounds:', session.is_system_sounds
            print '    state:', state
            print
            print
            print_lock.release()

        @staticmethod
        def endpoint_volume_change(
            endpoint,
            master_volume,
            channel_volumes,
            mute
        ):
            print_lock.acquire()

            print 'endpoint volume change'
            print '    device name:', endpoint.device.name
            print '    endpoint name:', endpoint.name
            print '    master:', str(master_volume * 100) + '%'
            print '    mute:', mute
            for i, level in enumerate(channel_volumes):
                print '    channel %d level:' % i, str(level * 100) + '%'

            print
            print
            print_lock.release()

        @staticmethod
        def device_state_change(device, state):
            print_lock.acquire()

            print 'device state change'
            print '    device name:', device.name
            print '    state:', state
            print
            print
            print_lock.release()

        @staticmethod
        def device_added(device):
            print_lock.acquire()

            print 'device added'
            print '    device name:', device.name
            print
            print
            print_lock.release()

        @staticmethod
        def device_removed(device):
            print_lock.acquire()

            print 'device removed'
            print '    device name:', device.name
            print
            print
            print_lock.release()

        @staticmethod
        def default_endpoint_changed(device):
            print_lock.acquire()

            print 'default endpoint changed'
            print '    device name:', device.name

            for endpoint in device:
                if (
                    endpoint.is_default and
                    endpoint not in registered_volume_callbacks
                ):
                    print '    endpoint name:', endpoint.name
                    try:
                        volume = endpoint.volume
                        callback = volume.register_volume_change_callback(
                            Callbacks.endpoint_volume_change
                        )
                        registered_volume_callbacks[endpoint] = callback
                        break

                    except AttributeError:
                        pass
            print
            print
            print_lock.release()

        @staticmethod
        def device_property_changed(device, key):
            print_lock.acquire()

            print 'device property changed'
            print '    device name:', device.name
            print '    key:', key.fmtid, key.pid
            print
            print
            print_lock.release()

    def test():
        for device in AudioDevices:
            print
            print
            print
            print 'device name:', device.name
            print '======================================================='
            print '    icon:', device.icon
            print '    id:', device.id
            print '    connector count:', device.connector_count
            print '    state:', device.state
            for endpoint in device:
                full_range_speakers = endpoint.full_range_speakers
                print
                print '    endpoint name:', endpoint.name
                print '    ---------------------------------------------------'
                print '        description:', endpoint.description
                print '        icon:', endpoint.icon
                print '        data flow:', endpoint.data_flow
                print '        form factor:', endpoint.form_factor
                print '        type:', endpoint.form_factor
                print '        full range speakers:', full_range_speakers
                print '        guid:', endpoint.guid
                print '        physical speakers:', endpoint.physical_speakers
                print '        system effects:', endpoint.system_effects
                try:
                    sink = endpoint.jack_information
                except AttributeError:
                    pass
                else:
                    print '        manufacturer id:', sink.manufacturer_id
                    print '        product id:', sink.product_id
                    print '        audio latency:', sink.audio_latency
                    print '        hdcp capable:', sink.hdcp_capable
                    print '        ai capable:', sink.ai_capable
                    print '        description:', sink.description
                    print '        connection type:', sink.connection_type

                try:
                    session_manager = endpoint.session_manager
                except AttributeError:
                    pass
                else:
                    session_manager.register_notification_callback(Callbacks)
                    print '        sessions'
                    try:
                        sessions = list(session_manager)
                    except TypeError:
                        pass
                    else:
                        def p(attr_name, v):
                            print '               ', attr_name, v

                        for i, session in enumerate(sessions):
                            session.register_notification_callback(Callbacks)
                            print '            session %d' % i
                            p('name:', session.name)
                            p('id:', session.id)
                            p('instance id:', session.instance_id)
                            p('process id:', session.process_id)
                            p('is system sounds:', session.is_system_sounds)
                            p('grouping param:', session.grouping_param)
                            p('icon:', session.icon)
                            p('state:', session.state)
                try:
                    jacks = list(jack for jack in endpoint.jack_descriptions)
                    print
                    print '        connectors'

                    def p(attr, v):
                        print '               ', attr, v

                    for i, jack in enumerate(jacks):
                        print '            %d:' % i
                        p('channel mapping:', jack.channel_mapping)
                        p('color:', jack.color)
                        p('type:', jack.type)
                        p('location:', jack.location)
                        p('port:', jack.port)
                        p('presence detection:', jack.presence_detection)
                        p('dynamic format change:', jack.dynamic_format_change)
                        p('is connected:', jack.is_connected)
                except AttributeError:
                    pass

                try:
                    volume = endpoint.volume
                    print
                except AttributeError:
                    pass
                else:
                    scalar = volume.master_scalar
                    print '        volume'
                    print '            master level:', volume.master
                    print '            master level scalar:', scalar
                    print '            master min:', volume.min
                    print '            master max:', volume.max
                    print '            master step:', volume.step
                    try:
                        mute = volume.mute
                        print '            mute:', mute
                    except AttributeError:
                        pass
                    print '            channel count:', volume.channel_count
                    print
                    print '            channel levels'
                    levels = volume.channel_levels
                    scalars = volume.channel_levels_scalar
                    ranges = volume.channel_ranges
                    for i, level in enumerate(levels):
                        print '                %d:' % i
                        print '                    level:', level
                        print '                    scalar level:', scalars[i]
                        c_min, c_max, c_step = ranges[i]
                        print '                    min:', c_min
                        print '                    max:', c_max
                        print '                    step:', c_step
                    try:
                        peak_meter = volume.peak_meter
                        print
                        print '            peak meter'
                        print '                master:', peak_meter.peak_value
                        print '                channels'
                        peak_values = peak_meter.channel_peak_values
                        for i, value in enumerate(peak_values):
                            print '                    %d:' % i
                            print '                        level:', value

                    except AttributeError:
                        pass

        print
        print
        default_render = AudioDevices.default_render_endpoint
        print 'default render device:', default_render.device.name
        print 'default render endpoint:', default_render.name
        print 'default render endpoint volume:', str(
            default_render.volume.master_scalar * 100
        ) + '%'

        default_capture = AudioDevices.default_capture_endpoint
        print 'default capture device:', default_capture.device.name
        print 'default capture endpoint:', default_capture.name
        print 'default capture endpoint volume:', str(
            default_capture.volume.master_scalar * 100
        ) + '%'

        registered_volume_callbacks[default_render] = (
            default_render.volume.register_notification_callback(Callbacks)
        )
        registered_volume_callbacks[default_capture] = (
            default_capture.volume.register_notification_callback(Callbacks)
        )

        AudioDevices.register_notification_callback(Callbacks)

        print
        print

        raw_input(
            'Change the volume.\n'
            'Set the mute.\n'
            'Change the default device.\n'
            'Change some of the device properties.\n'
            '\n'
            'Press any key to exit.\n'
        )
        import sys

        sys.exit()

    try:
        test()
    finally:
        stop()

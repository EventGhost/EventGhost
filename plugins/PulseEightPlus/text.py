# -*- coding: utf-8 -*-

import eg


class Text(eg.TranslatableStrings):
    device_lbl = 'Device:'
    adapter_lbl = 'Adapter:'
    mode_lbl = 'Playback Mode:'
    message_lbl = 'Message:'
    duration_lbl = 'Duration (seconds):'
    volume_lbl = 'Volume:'
    command_lbl = 'Command:'
    key_lbl = 'Remote Key:'
    events_lbl = 'Events:'
    status_lbl = 'Status:'
    source_lbl = 'Source:'

    mute_group_lbl = 'Mute'
    volume_group_lbl = 'Volume'
    power_group_lbl = 'Power'
    remote_group_lbl = 'Remote Keys'

    info_header = 'Info:'
    info_tooltip = 'Log traffic data.'

    notice_header = 'Notice:'
    notice_tooltip = 'Log notice data.'

    warning_header = 'Warning:'
    warning_tooltip = 'Log warning data.'

    error_header = 'Error:'
    error_tooltip = 'Log error data.'

    debug_header = 'Debug:'
    debug_tooltip = 'Log debugging data.'

    log_file_header = 'Write to file:'
    log_file_tooltip = (
        'Writes CEC logs to file(s).\n'
        'Files are written to %appdata%/EventGhost/CEC/[Adapter Name]'
    )

    adapter_name_header = 'Adapter OSD Name'
    adapter_name_tooltip = (
        'Name that is displayed on the TV for the CEC adapter.'
    )

    adapter_type_header = 'Adapter Emulation'
    adapter_type_tooltip = 'The device type(s) that the adapter will emulate.'

    adapter_port_header = 'Adapter Port'
    adapter_port_tooltip = (
        'Serial port on the PC the adapter is connected to.'
    )

    avr_audio_header = 'AVR Audio'
    avr_audio_tooltip = (
        'Use connected AVR for audio controls.'
    )

    wake_avr_header = 'Wake AVR'
    wake_avr_tooltip = (
        'Automatically wakes an AVR when its source is activated.'
    )

    hdmi_header = 'HDMI Port'
    hdmi_tooltip = (
        'The HDMI port on the device the CEC adapter is connected to.\n'
        '(0 means auto detect) '
        '(only set this is you are having connection issues)'
    )

    power_off_header = 'PC Power Off'
    power_off_tooltip = (
        'Shutdown this PC when the TV is switched off.'
    )

    power_standby_header = 'PC Power Standby'
    power_standby_tooltip = (
        'Put this PC in standby mode when the TV is switched off.'
    )

    keypress_combo_header = 'Key Combo'
    keypress_combo_tooltip = 'Remote button that enables button combinations.'

    keypress_combo_timeout_header = 'Key Combo Timeout'
    keypress_combo_timeout_tooltip = (
        'Timeout until the button combinations are set to normal.\n'
        '(milliseconds)'
    )

    keypress_repeat_header = 'Key Repeat'
    keypress_repeat_tooltip = (
        'Rate at which remote buttons auto repeated.\n'
        '(milliseconds), (0 means rely on device)'
    )
    keypress_release_header = 'Key Release'
    keypress_release_delay_tooltip = (
        'Duration until a remote button is considered released.\n'
        '(milliseconds)'
    )
    keypress_double_tap_header = 'Key Double Tap'
    keypress_double_tap_tooltip = (
        'Prevent remote button double taps within this timeout.\n'
        '(milliseconds)'
    )

    class GetTunerStatus:
        name = 'Get Tuner Status'
        description = 'Gets the status of a tuner device'

    class GiveTunerStatus:
        name = 'Give Tuner Status'
        description = (
            'Gives the tuner status of an adapter that is emulating a '
            'tuner device.<br>'
            '<br>'
            'This action can only be run from a Tuner.StatusRequest event.<br>'
            'The purpose of this action is so you can "CEC Enable" a tuner '
            'device that is attached to your PC. So if another device on the '
            'CEC bus requests the status of the tuner you have the ability to '
            'reply to the request.<br>'
            'The reason you have to use this with a Tuner.StatusRequest event '
            'is because we need to know where to send the answer to, and that '
            'information is contained in the payload of the event.<br>'
            '<br>'
            'The states are simple:<br>'
            'Digital<br>'
            'Analog<br>'
            'Off<br>'
        )

    class TunerChannelUp:
        name = 'TV Tuner Channel Up'
        description = 'Change the channel on the tele +1'

    class TunerChannelDown:
        name = 'TV Tuner Channel Down'
        description = 'Change the channel on the tele -1'

    class TunerStatusEvents:
        name = 'Tuner Status Events'
        description = (
            'Turns on and off events for status changes to a specific '
            'tuner.<br>'
            '<br>'
            'If you want to perform specific actions if the tuner gets '
            'switched on and off then you will want to enable events for '
            'that tuner.<br>'
        )

    class PlayerStatusEvents:
        name = 'Player Status Events'
        description = (
            'Turns on and off events for status changes to a specific '
            'player.<br>'
            '<br>'
            'If you want to perform specific actions based on the mode of a '
            'player then you will want to enable events for that player.<br>'
        )

    class SetPlayerMode:
        name = 'Set Player Mode'
        description = (
            'Sets the mode of a player device.<br>'
            '<br>'
            'This action allows you to set the playing mode of a player '
            'device on the CEC bus.<br>'
            '<br>'
            'Available modes:<br>'
            'Play*<br>'
            'Pause<br>'
            'Stop<br>'
            'Eject<br>'
            'Rewind*<br>'
            'Fast Forward*<br>'
            'Skip Forward<br>'
            'Skip Back<br>'
            '<br>'
            '* Repeat calls to these modes will cause the speed to increase. '
            'These modes function in a loop so once at the fastest if called '
            'again it will start the speed increases from the begining.<br>'
        )

    class GetPlayerStatus:
        name = 'Get Player Status'
        description = 'Gets the status of a player device'

    class GivePlayerStatus:
        name = 'Give Player Status'
        description = (
            'Gives the player status of an adapter that is emulating a '
            'player device.<br>'
            '<br>'
            'This action can only be run from a Player.StatusRequest '
            'event.<br>'
            'The purpose of this action would be so that you are able to '
            '"CEC Enable" a piece of software like VLC, or MediaPortal. '
            'This gives you the ability to report the state of the software '
            'to the CEC device that requested it.<br>'
            'The reason you have to use this with a Player.StatusRequest '
            'event is because we need to know where to send the answer to, '
            'and that information is contained in the payload of the '
            'event.<br>'
            '<br>'
            'The possible responses you can send are:<br>'
            'Playing<br>'
            'Playing Reverse<br>'
            'Paused<br>'
            'Playing Slow<br>'
            'Playing Slow Reverse<br>'
            'Fast Forwarding<br>'
            'Fast Rewinding<br>'
            'No Media<br>'
            'Stopped<br>'
            'Skipping Forward<br>'
            'Skipping Reverse<br>'
            'Search Forward<br>'
            'Search Reverse<br>'
            'Other<br>'
            'Other LG<br>'
        )

    class DisplayMessage:
        name = 'Display a message on a TV'
        description = (
            'Sends a message that will be displayed on the TV<br>'
            '<br>'
            'This action is hit or miss on which TV\'s will support the '
            'displaying of messages. So give it a shot. If it works let me '
            'know and I will start making a list of supported TV\'s<br>'
        )

    class RawCommand:
        name = 'Send command to an adapter'
        description = 'Send a raw CEC command to an adapter'

    class RestartAdapter:
        name = 'Restart Adapter'
        description = 'Restarts an adapter.'

    class VolumeUp:
        name = 'Volume Up'
        description = (
            'Turns up the volume by one point.<br>'
            '<br>'
            'If no avr is attached to the CEC bus or Enable AVR Audio is not '
            'checked off for the adapter this action will attempt to use the '
            'volume up remote key code to increase the volume on the TV. This '
            'may or may not work, it depends on whether or not your TV '
            'manufacturer allows remote codes.<br>'
        )


    class VolumeDown:
        name = 'Volume Down'
        description = (
            'Turns down the volume by one point.<br>'
            '<br>'
            'If no avr is attached to the CEC bus or Enable AVR Audio is not '
            'checked off for the adapter this action will attempt to use the '
            'volume down remote key code to decrease the volume on the TV. '
            'This may or may not work, it depends on whether or not your TV '
            'manufacturer allows remote codes.<br>'
        )

    class GetVolume:
        name = 'Get AVR Volume'
        description = 'Returns the current volume level on an AVR.'

    class SetVolume:
        name = 'Set AVR Volume'
        description = 'Sets the volume level on an AVR.'

    class GetMute:
        name = 'Get AVR Mute'
        description = 'Returns the mute state on an AVR.'

    class ToggleMute:
        name = 'Toggle Mute'
        description = (
            'Toggles the mute state.<br>'
            '<br>'
            'If no avr is attached to the CEC bus or Enable AVR Audio is not '
            'checked off for the adapter this action will attempt to use the '
            'mute remote key code to mute/unmute the volume on the TV. '
            'This may or may not work, it depends on whether or not your TV '
            'manufacturer allows remote codes.<br>'
        )

    class MuteOn:
        name = 'AVR Mute On'
        description = 'Mutes the audio on an AVR.'

    class MuteOff:
        name = 'AVR Mute Off'
        description = 'Unmutes the audio on an AVR.'

    class PowerOnAll:
        name = 'Power On All Devices'
        description = 'Powers on all devices on a specific adapter.'

    class StandbyAll:
        name = 'Standby All Devices'
        description = 'Powers off (standby) all devices in a specific adapter.'

    class StandbyDevice:
        name = 'Standby a Device'
        description = 'Powers off (standby) a single device.'

    class GetDevicePower:
        name = 'Get Device Power'
        description = 'Returns the power status of a device.'

    class PowerOnDevice:
        name = 'Power On a Device'
        description = 'Powers on a single device.'

    class GetDeviceVendor:
        name = 'Get Device Vendor'
        description = 'Returns the vendor of a device.'

    class GetDeviceMenuLanguage:
        name = 'Get Device Menu Language'
        description = 'Returns the menu language of a device.'

    class IsActiveSource:
        name = 'Is Device Active Source'
        description = 'Returns True/False if a device is the active source.'

    class IsDeviceActive:
        name = 'Is Device Active'
        description = 'Returns True/False if a device is active.'

    class GetDeviceOSDName:
        name = 'Get Device OSD Name'
        description = 'Returns the OSD text that is display for a device.'

    class SetDeviceActiveSource:
        name = 'Set Device as Active Source'
        description = 'Sets a device as the active source.'

    class SendRemoteKey:
        name = 'Send Remote Key'
        description = 'Send a Remote Keypress to a specific device.'

    class SetHDMI:
        name = 'Set HDMI Source Input'
        description = 'Sets the input to one of the selected HDMI ports.'

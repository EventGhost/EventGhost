# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright © EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.


import eg


eg.RegisterPlugin(
    name="Atric IR-WakeupUSB",
    guid="{29CC33EC-2304-4879-9B5B-D98ECCADC5B6}",
    author=("GruberMarkus"),
    version="0.1",
    kind="remote",
    createMacrosOnAdd=True,
    canMultiLoad=True,
    url="https://github.com/GruberMarkus/EventGhost",
    description=(
        "<rst>"
        "Plugin for the `Atric IR-WakeupUSB`__ device.\n"
        "\n"
        "Compatible up to firmware version 1.2.\n"
        "\n"
        "If you have a newer firmware version or the Professional variant of the device, please contact the author of this plugin via GitHub.\n"
        "\n"
        "\n"
        "__ https://www.atric.de"
    )
)


import time  # noqa: E402
import wx  # noqa: E402


BYTESIZES = ("5", "6", "7", "8")
PARITIES = ("N", "O", "E", "M", "S")
PARITIES_CHOICE = ("N = No", "E = Even", "O = Odd", "M = Mark", "S = Space")
STOPBITS = ("1", "1.5", "2")
BAUDRATES = ("75", "110", "134", "150", "300", "600", "1200", "1800", "2400",
             "4800", "7200", "9600", "14400", "19200", "38400", "57600", "115200", "128000")
RETURNFORMATS = ("Original", "Hex", "ASCII",
                 "Hex2Int", "Hex2IntNegative", "Hex2Time")


# Serial thread object; global because different classes access it
global_serial_thread = None

# Serial input data; global because different classes access it
global_serial_buffer = ""

# "Generate events" configuration; global because different classes access it
global_generate_events = None

# Firmware version of the device; global because different classes access it
global_firmware_version = ""

# Security access string; global because different classes access it
global_access_string = ""


class Text(eg.TranslatableStrings):
    init_start = "Atric IR-WakeupUSB: Initializing and resetting."
    init_success = "Atric IR-WakeupUSB: Initiated successfully on COM%d."
    init_ctrl_label = "Initialize device on start (default: True)"

    firmware_start = "Atric IR-WakeupUSB: Getting firmware version."
    firmware_success = "Atric IR-WakeupUSB: Running with firmware %s."
    firmware_error = "Atric IR-WakeupUSB: Firmware %s is unknown, using %s instead. Please contact the author of this plugin via GitHub."

    port_settings_box_label = "Port settings"
    port_ctrl_label = "COM port"
    baudrate_ctrl_label = (
        "Baud rate\n"
        "(default: 9600)"
    )
    bytesize_ctrl_label = (
        "Byte size\n"
        "(default: 8)"
    )
    parity_ctrl_label = (
        "Parity\n"
        "(default: N)"
    )
    stopbits_ctrl_label = (
        "Stop bits\n"
        "(default: 1)"
    )

    event_settings_box_label = "Event settings"
    generate_events_ctrl_label = (
        "Generate events on incoming data\n"
        "(default: True)"
    )
    bytecount_ctrl_label = (
        "Event byte count\n"
        "(default: 6)"
    )
    prefix_ctrl_label = (
        "Event prefix\n"
        "(default: Atric)"
    )

    class pause_event_generation:
        name = "Pause event generation"
        description = "Pauses event generation so that data can safely be accessed by other EventGhost activities."

    class resume_event_generation:
        name = "Resume event generation"
        description = "Resumes event generation. Unread data in the buffer is flushed."

    class toggle_event_generation:
        name = "Toggle event generation"
        description = "Toggles event generation. Returns new event generation state."

    class flush_input:
        name = "Flush input buffer"
        description = "Flushes unread data from the input buffer."

    class write:
        name = "Write"
        description = (
            "Sends a command to the device through the serial port, without taking care of event generation or return values.\n\n<p>"
            "For a more sophisticated approach, use \"Write Advanced\".<p>"
            "You can use Python string escapes to send non-printable characters. Some examples:<br>"
            "\\n will send a Linefeed (LF)<br>"
            "\\r will send a Carriage Return (CR)<br>"
            "\\t will send a Horizontal Tab (TAB)<br>"
            "\\x0B will send the ASCII character with the hexcode 0B<br>"
            "\\\\ will send a single Backslash")

        write_string_label = (
            "String to write to the device\n"
            "(you can use variables such as \"{eg.result}\")"
        )
        parse_string_label = "String after parsing"
        parse_string_error = "Error parsing input string, please check input string (you can escape \"{\" with \"{{\")."

    class write_advanced:
        name = "Write Advanced"
        description = (
            "Sends a command to the device through the serial port, taking care of event generation an return values.\n\n<p>"
            "Before writing, event generation ist stopped. After writing, the input buffer is read and event generation is continued. The input buffer is decoded in the chosen format and returned. < p >"
            "For a less sophisticated approach, use \"Write\".<p>"
            "You can use Python string escapes to send non-printable characters. Some examples:<br>"
            "\\n will send a Linefeed (LF)<br>"
            "\\r will send a Carriage Return (CR)<br>"
            "\\t will send a Horizontal Tab (TAB)<br>"
            "\\x0B will send the ASCII character with the hexcode 0B<br>"
            "\\\\ will send a single Backslash")

        write_string_label = (
            "String to write to the device\n"
            "(you can use variables such as \"{eg.result}\")"
        )
        parse_string_label = "String after parsing"
        parse_string_error = "Error parsing input string, please check input string (you can escape \"{\" by typing \"{{\")."

        timeout_ctrl_label = (
            "Wait this number of seconds\n"
            "after writing the string to the device"
        )

        read = "Read"
        read_all = "all bytes that are currently available"
        read_some = "exactly"
        bytes_name = "bytes"
        read_time = "and wait up to this number of seconds"
        read_info = (
            "The action returns immediately when the configured amount of\n"
            "bytes is read or the maximum wait time is reached, whatever comes first.\n"
            "\n"
            "If there are more bytes available then requested, the bytes\n"
            "that arrived first are returned first (first in, first out)."
        )

        returnformat_ctrl_label = "Return output in the following format"
        debug_ctrl_label = "Print output in all possible formats"

        disable_infrared_while_write_ctrl_label = "Disable infrared before write, enable infrared after write (avoids possible data poisoning)"

    class read:
        name = "Read"
        description = (
            "Reads data from the serial port.\n\n<p>"
            "This action returns the data through eg.result, as any action does that is returning data. So you have to use Python scripting to do anything with the result.<p>"
            "Using this action and enabling event generation in the plugin cannot be used at the same time, as one of it will always eat the data away from the other.<p>"
            "This action does not automatically pause and unpause event generation. You can pause and unpause event generation with the \"Pause event generation\" and \"Resume event generation\" actions.")

        read = "Read"
        read_all = "all bytes that are currently available"
        read_some = "exactly"
        bytes_name = "bytes"
        read_time = "and wait up to this number of seconds"
        read_info = (
            "The action returns immediately when the configured amount of\n"
            "bytes is read or the maximum wait time is reached, whatever comes first.\n"
            "\n"
            "If there are more bytes available then requested, the bytes\n"
            "that arrived first are returned first (first in, first out)."
        )

        returnformat_ctrl_label = "Convert and return output in this format"
        debug_Label = "Print output in all possible formats"

    class get_time:
        name = "Get time"
        description = (
            "Returns date and time set on the Atric device.\n\n<p>"
            "Output format is \"YYMMDDhhmmss\", \"181231143910\" being \"2018-12-31 14:39:10\"."
        )

    class get_time_correction:
        name = "Get time correction value"
        description = "Returns the time correction value set on the Atric device."

    class get_daylight_saving:
        name = "Get daylight saving value"
        description = (
            "Returns the daylight saving value set on the Atric device.\n\n<p>"
            "0: Automatic daylight saving time is disabled.<p>"
            "1: Automatic daylight saving time is enabled."
        )

    class sync_time:
        name = "Sync time"
        description = (
            "Sets the time on the Atric device so it matches the time on the PC.\n\n<p>"
            "When the \"Calibrate\" option of this action is enabled, the time correction value is automatically adjusted by the Atric device.<p>"
            "Only use the \"Calibrate\" option when the time on the Atric device has already been set before.<p>"
            "Recommendation:<br>"
            "    1. Set the time correction value on the Atric device to 0.<br>"
            "    2. Sync time on the Atric device, with calibration disabled, once.<br>"
            "    3. Wait at least 12, better 24 or more hours.<br>"
            "    4. Sync time on the Atric device, with calibration enabled, every few days."
        )

        calibrate_ctrl_label = "Automatic time calibration (see description for details)"

    class set_time_correction:
        name = "Set time correction value"
        description = (
            "Sets the time correction value on the Atric device.\n\n<p>"
            "0: Time is not adjusted automatically.<p>"
            "Positive value, e.g. 250: Every 250 seconds, one second is skipped. This makes the clock go faster.<p>"
            "Negative value, e.g. -712: Every 712 seconds, time is stopped for one second. This makes the clock go slower."
        )

        correction_ctrl_label = "Time correction value (see description for details)"

    class get_waketime:
        name = "Get wake time"
        description = (
            "Returns the wake time set on the Atric device.\n\n<p>"
            "Output format is \"YYMMDDhhmmss\", \"181231143910\" being \"2018-12-31 14:39:10\".<p>"
            "\"0000000000\" means that no wake time is set."
        )

    class configure_daylight_saving:
        name = "Configure daylight saving"
        description = "Enables or disables automatic switching to daylight saving time on the Atric device."

        daylight_ctrl_label = "Enable automatic switch to daylight saving time (summer time)"

    class set_waketime:
        name = "Set wake time"
        description = "Sets the wake time on the Atric device, or disables wakeup."

        delete_ctrl_label = "delete wake timer (set it to \"0000000000\" on the device)"

        year_label_ctrl_label = "Year"
        month_label_ctrl_label = "Month"
        day_label_ctrl_label = "Day"
        hour_label_ctrl_label = "Hour"
        minute_label_ctrl_label = "Minute"

        waketime_label_ctrl_label = "String that will be sent"
        waketime_cleartext_label_ctrl_label = "Date in clear text"
        waketime_cleartext_label_ctrl_disable_text = "Disable wakeup"
        waketime_cleartext_label_ctrl_invalid_text = "Invalid date!"
        waketime_ctrl_invalid_text = waketime_cleartext_label_ctrl_invalid_text

    class reset:
        name = "Reset"
        description = "Resets the Atric device and returns \"OK\" if everything is fine."

    class initialize:
        name = "Initialize"
        description = "Initializes the Atric device."

    class initialize_reset:
        name = "Initialize and Reset"
        description = "Initializes and resets the Atric device and returns \"OK\" if everything is fine."

    class configure_infrared:
        name = "Configure infrared"
        description = "Enables or disables infrared on the Atric device."

        infrared_ctrl_label = "Enable infrared on the device"

    class enable_led:
        name = "Enable LED"
        description = (
            "Enables the LED on the Atric device.\n\n<p>"
            "If the LED is glowing red, it is connected the wrong way.<p>"
            "Press a button on the remote control or reset the device to return to normal LED behavior."
        )

    class get_firmware_version:
        name = "Get firmware version"
        description = "Returns the firmware version installed on the Atric device."

    class get_hardware_version:
        name = "Get hardware version"
        description = "Returns the hardware version of the Atric device."


class Atric_IRWakeupUSB(eg.RawReceiverPlugin):
    text = Text

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)

        global global_serial_thread
        global_serial_thread = None

        self.AddAction(read)
        self.AddAction(write)
        self.AddAction(write_advanced)

        self.AddAction(pause_event_generation)
        self.AddAction(resume_event_generation)
        self.AddAction(toggle_event_generation)
        self.AddAction(flush_input)

        self.AddAction(get_time)
        self.AddAction(get_time_correction)
        self.AddAction(get_daylight_saving)
        self.AddAction(get_waketime)

        self.AddAction(sync_time)
        self.AddAction(set_time_correction)
        self.AddAction(set_waketime)

        self.AddAction(configure_daylight_saving)
        self.AddAction(configure_infrared)

        self.AddAction(initialize)
        self.AddAction(reset)
        self.AddAction(initialize_reset)
        self.AddAction(enable_led)

        self.AddAction(get_firmware_version)
        self.AddAction(get_hardware_version)

    def __start__(
        self,
        port=0,
        baudrate=9600,
        bytesize=3,
        parity=0,
        stopbits=0,
        generate_events=True,
        prefix="Atric",
        init=True,
        bytecount=6,
    ):
        text = self.text

        global global_generate_events
        global global_firmware_version
        global global_access_string
        global global_serial_thread
        global global_serial_buffer

        global_generate_events = generate_events

        self.info.eventPrefix = prefix

        bytesize = BYTESIZES[bytesize]
        parity = PARITIES[parity]
        stopbits = STOPBITS[stopbits]

        self.bytecount = bytecount

        global_serial_thread = eg.SerialThread()

        global_serial_buffer = ""

        global_serial_thread.Open(
            port,
            baudrate,
            (str(bytesize) + str(parity) + str(stopbits))
        )

        global_serial_thread.SetRts()
        global_serial_thread.SetDtr()
        global_serial_thread.Start()

        time.sleep(0.05)

        global_serial_thread.Flush()

        global_serial_thread.SetReadEventCallback(self.on_receive)

        if init is True:
            print(text.init_start)

            temp = write_advanced()
            temp(
                data="I",
                timeout=0.1,
                read_num_bytes=0,
                disable_infrared_while_write=False
            )
            global_serial_thread.Flush()
            returndata = temp(
                data="R",
                timeout=0,
                read_returnformat="original",
                read_num_bytes=2,
                read_timeout=2,
                disable_infrared_while_write=False,
            )

            if returndata == "OK":
                eg.TriggerEvent(text.init_success % (port + 1))
            else:
                global_serial_thread.Close()
                raise self.Exceptions.DeviceInitFailed

        print(text.firmware_start)
        temp = write_advanced()
        global_serial_thread.Flush()
        returndata = temp(
            data="VV",
            timeout=0,
            read_num_bytes=2,
            read_timeout=2,
            read_returnformat="hex",
            read_debug=False,
            disable_infrared_while_write=False,
        )
        try:
            returndata = float(returndata[0] + "." + returndata[1])
        except:
            returndata = -1

        if returndata >= 0 and returndata < 1.2:
            global_firmware_version = "<1.2"
            global_access_string = ""
            eg.TriggerEvent(text.firmware_success % (returndata))
        elif returndata == 1.2:
            global_firmware_version = "1.2"
            global_access_string = "ACS"
            eg.TriggerEvent(text.firmware_success % (returndata))
        else:
            global_firmware_version = "1.2"
            global_access_string = "ACS"
            eg.TriggerEvent(text.firmware_error %
                            (returndata, global_firmware_version))

    def on_receive(self, global_serial_thread):
        global global_serial_buffer
        if global_generate_events is True:
            global_serial_buffer = ""
            data = global_serial_thread.Read(self.bytecount)
            if len(data) < self.bytecount:
                return
            self.TriggerEvent("".join("%02X" % ord(byte) for byte in data))
        else:
            global_serial_buffer += global_serial_thread.Read(1)

    def __stop__(self):
        global_serial_thread.Close()
        time.sleep(1.0)

    def Configure(
        self,
        port=0,
        baudrate=9600,
        bytesize=3,
        parity=0,
        stopbits=0,
        generate_events=True,
        prefix="Atric",
        init=True,
        bytecount=6,
    ):
        text = self.text
        panel = eg.ConfigPanel()

        port_ctrl = panel.SerialPortChoice(port)

        baudrate_ctrl = panel.ComboBox(
            str(baudrate),
            BAUDRATES,
            style=wx.CB_DROPDOWN,
            validator=eg.DigitOnlyValidator()
        )

        bytesize_ctrl = panel.Choice(bytesize, BYTESIZES)

        parity_ctrl = panel.Choice(parity, PARITIES_CHOICE)

        stopbits_ctrl = panel.Choice(stopbits, STOPBITS)

        init_ctrl = panel.CheckBox(init, text.init_ctrl_label)

        bytecount_ctrl = panel.SpinIntCtrl(bytecount, min=1, max=32)
        bytecount_ctrl.Enable(generate_events)

        prefix_ctrl = panel.TextCtrl(prefix)
        prefix_ctrl.Enable(generate_events)

        generate_events_ctrl = panel.CheckBox(
            generate_events, text.generate_events_ctrl_label)

        def on_checkbox(event):
            flag = generate_events_ctrl.GetValue()
            bytecount_ctrl.Enable(flag)
            prefix_ctrl.Enable(flag)
            event.Skip()

        generate_events_ctrl.Bind(wx.EVT_CHECKBOX, on_checkbox)

        panel.SetColumnFlags(1, wx.EXPAND)

        port_settings_box = panel.BoxedGroup(
            text.port_settings_box_label,
            (text.port_ctrl_label, port_ctrl),
            (text.baudrate_ctrl_label, baudrate_ctrl),
            (text.bytesize_ctrl_label, bytesize_ctrl),
            (text.parity_ctrl_label, parity_ctrl),
            (text.stopbits_ctrl_label, stopbits_ctrl),
            (init_ctrl)
        )

        event_settings_box = panel.BoxedGroup(
            text.event_settings_box_label,
            (generate_events_ctrl),
            (text.bytecount_ctrl_label, bytecount_ctrl),
            (text.prefix_ctrl_label, prefix_ctrl)
        )

        eg.EqualizeWidths(port_settings_box.GetColumnItems(0)[:-1])
        eg.EqualizeWidths(port_settings_box.GetColumnItems(1))

        eg.EqualizeWidths(event_settings_box.GetColumnItems(0)[1:])
        eg.EqualizeWidths(event_settings_box.GetColumnItems(1))

        Add = panel.sizer.Add
        Add(eg.HBoxSizer(port_settings_box, (5, 5), event_settings_box))

        while panel.Affirmed():
            panel.SetResult(
                port_ctrl.GetValue(),
                int(baudrate_ctrl.GetValue()),
                bytesize_ctrl.GetValue(),
                parity_ctrl.GetValue(),
                stopbits_ctrl.GetValue(),
                generate_events_ctrl.GetValue(),
                prefix_ctrl.GetValue(),
                init_ctrl.GetValue(),
                bytecount_ctrl.GetValue()
            )


class pause_event_generation(eg.ActionBase):
    def __call__(self):
        global global_generate_events

        global_generate_events = False

        return global_generate_events


class resume_event_generation(eg.ActionBase):
    def __call__(self):
        global global_generate_events
        global global_serial_buffer

        global_generate_events = True
        global_serial_buffer = ""

        return global_generate_events


class toggle_event_generation(eg.ActionBase):
    def __call__(self):
        global global_generate_events
        global global_serial_buffer

        if global_generate_events is True:
            global_generate_events = False
        else:
            global_generate_events = True
            global_serial_buffer = ""

        return global_generate_events


class flush_input(eg.ActionBase):
    def __call__(self):
        global global_serial_buffer

        global_serial_buffer = ""
        global_serial_thread.Flush()


class write(eg.ActionBase):
    def GetLabel(self, *args):
        label = self.name

        if args:
            label += ": " + ";".join("%s" % str(arg) for arg in args)

        return label

    def __call__(self, data=""):
        data = eg.ParseString(data)
        data = data.decode("string_escape")

        global_serial_thread.Write(str(data))

        return global_serial_thread

    def Configure(self, data=""):
        text = self.text
        panel = eg.ConfigPanel()

        data_ctrl = panel.TextCtrl(data)
        data_ctrl_label = panel.StaticText(text.write_string_label)

        result_preview_ctrl_label = panel.StaticText(text.parse_string_label)
        result_preview_ctrl = panel.StaticText("")

        eg.EqualizeWidths(
            (
                data_ctrl_label,
                result_preview_ctrl_label
            )
        )
        eg.EqualizeWidths(
            (
                data_ctrl,
                result_preview_ctrl
            )
        )

        Add = panel.sizer.Add
        Add(eg.HBoxSizer(data_ctrl_label, (5, 5), data_ctrl))
        Add((5, 5))
        Add(eg.HBoxSizer(result_preview_ctrl_label, (5, 5), result_preview_ctrl))

        def on_data_change(event):
            try:
                temp = eg.ParseString(data_ctrl.GetValue())
                temp = temp.strip()
                result_preview_ctrl.SetLabel(temp)
                panel.EnableButtons(True)
            except:
                result_preview_ctrl.SetLabel(text.parse_string_error)
                panel.EnableButtons(False)

            event.Skip()

        data_ctrl.Bind(wx.EVT_TEXT, on_data_change)

        data_ctrl.SetValue(data_ctrl.GetValue())

        while panel.Affirmed():
            panel.SetResult(
                data_ctrl.GetValue()
            )


class write_advanced(eg.ActionBase):
    def GetLabel(self, *args):
        label = self.name

        if args:
            label += ": " + ";".join("%s" % str(arg) for arg in args)

        return label

    def __call__(
        self,
        data="",
        timeout=0.2,
        read_num_bytes=None,
        read_timeout=1.0,
        read_returnformat="hex",
        read_debug=False,
        disable_infrared_while_write=True,
    ):
        generate_events_original = global_generate_events

        if generate_events_original is True and (read_num_bytes > 0 or read_num_bytes is None):
            temp = pause_event_generation()
            temp()

        if disable_infrared_while_write is True:
            global_serial_thread.Write("L" + global_access_string)

        temp = flush_input()
        temp()

        # On error, try to write a second time
        # This helps avoid error 121 (semaphore timeout) with some drivers/devices
        try:
            global_serial_thread.Write(str(data))
        except:
            global_serial_thread.Write(str(data))

        time.sleep(float(timeout))

        if read_num_bytes is None or read_num_bytes > 0:
            temp = read()
            returndata = temp(
                num_bytes=read_num_bytes,
                timeout=read_timeout,
                returnformat=read_returnformat,
                debug=read_debug
            )
        else:
            returndata = ""

        if generate_events_original is True and (read_num_bytes > 0 or read_num_bytes is None):
            temp = resume_event_generation()
            temp()

        if disable_infrared_while_write is True:
            global_serial_thread.Write("C")

        return returndata

    def Configure(
        self,
        data="",
        timeout=0.2,
        read_num_bytes=None,
        read_timeout=1.0,
        read_returnformat="hex",
        read_debug=False,
        disable_infrared_while_write=True
    ):
        text = self.text
        panel = eg.ConfigPanel()

        if read_num_bytes is None:
            read_num_bytes = 2147483647
            flag = False
        else:
            flag = True

        disable_infrared_while_write_ctrl = panel.CheckBox(
            disable_infrared_while_write, text.disable_infrared_while_write_ctrl_label)

        data_ctrl_label = panel.StaticText(text.write_string_label)
        data_ctrl = panel.TextCtrl(data)

        returnformat_ctrl_label = panel.StaticText(
            text.returnformat_ctrl_label)
        returnformat_ctrl = panel.ComboBox(
            read_returnformat,
            RETURNFORMATS,
            style=wx.CB_DROPDOWN | wx.CB_READONLY
        )

        debug_ctrl = panel.CheckBox(read_debug, text.debug_ctrl_label)

        result_preview_ctrl_label = panel.StaticText(text.parse_string_label)
        result_preview_ctrl = panel.StaticText("")

        timeout_ctrl_label = panel.StaticText(text.timeout_ctrl_label)
        timeout_ctrl = panel.SpinNumCtrl(
            timeout,
            min=0.0,
            max=10.0,
            allowNegative=False,
            increment=0.1,
            integerWidth=2,
            fractionWidth=2,
        )

        dummy_ctrl = panel.StaticText("")

        rb1 = panel.RadioButton(not flag, text.read_all, style=wx.RB_GROUP)
        rb2 = panel.RadioButton(flag, text.read_some)

        count_ctrl = panel.SpinIntCtrl(read_num_bytes, 1, 2147483647)
        count_ctrl.Enable(flag)

        read_timeout_ctrl_label = panel.StaticText(text.read_time)
        read_timeout_ctrl = panel.SpinNumCtrl(
            read_timeout,
            min=0.0,
            max=10.0,
            allowNegative=False,
            increment=0.1,
            integerWidth=2,
            fractionWidth=2,
        )

        read_ctrl = panel.StaticText(text.read)

        def on_data_change(event):
            try:
                temp = eg.ParseString(data_ctrl.GetValue())
                temp = temp.strip()
                result_preview_ctrl.SetLabel(temp)
                panel.EnableButtons(True)
            except BaseException:
                result_preview_ctrl.SetLabel(text.parse_string_error)
                panel.EnableButtons(False)

            event.Skip()

        def on_radiobutton(event):
            flag = rb2.GetValue()
            count_ctrl.Enable(flag)
            event.Skip()

        rb1.Bind(wx.EVT_RADIOBUTTON, on_radiobutton)
        rb2.Bind(wx.EVT_RADIOBUTTON, on_radiobutton)

        data_ctrl.Bind(wx.EVT_TEXT, on_data_change)

        data_ctrl.SetValue(data_ctrl.GetValue())

        eg.EqualizeWidths(
            (
                data_ctrl_label,
                result_preview_ctrl_label,
                timeout_ctrl_label,
                returnformat_ctrl_label,
                dummy_ctrl,
                read_timeout_ctrl_label,
                read_ctrl,
            )
        )
        eg.EqualizeWidths(
            (
                data_ctrl,
                result_preview_ctrl,
                timeout_ctrl,
                returnformat_ctrl,
                read_timeout_ctrl,
                debug_ctrl,
                rb1,
            )
        )

        Add = panel.sizer.Add
        Add(eg.HBoxSizer(data_ctrl_label, (5, 5), data_ctrl))
        Add((5, 5))
        Add(eg.HBoxSizer(result_preview_ctrl_label, (5, 5), result_preview_ctrl))
        Add(panel.StaticText(""))
        Add(eg.HBoxSizer(timeout_ctrl_label, (5, 5), timeout_ctrl))
        Add(panel.StaticText(""))
        Add(eg.HBoxSizer(read_ctrl, (5, 5), rb1))
        Add(eg.HBoxSizer(dummy_ctrl, (5, 5), rb2, count_ctrl,
                         (5, 5), panel.StaticText(text.bytes_name)))
        Add((5, 5))
        Add(eg.HBoxSizer(read_timeout_ctrl_label, (5, 5), read_timeout_ctrl))
        Add((5, 5))
        Add(panel.StaticText(text.read_info))
        Add(panel.StaticText(""))
        Add(eg.HBoxSizer(returnformat_ctrl_label, (5, 5), returnformat_ctrl))
        Add((5, 5))
        Add(eg.HBoxSizer(dummy_ctrl, (5, 5), debug_ctrl))
        Add(panel.StaticText(""))
        Add(eg.HBoxSizer(disable_infrared_while_write_ctrl))

        while panel.Affirmed():
            if rb1.GetValue():
                panel.SetResult(
                    data_ctrl.GetValue(),
                    timeout_ctrl.GetValue(),
                    None,
                    read_timeout_ctrl.GetValue(),
                    returnformat_ctrl.GetValue(),
                    debug_ctrl.GetValue(),
                    disable_infrared_while_write_ctrl.GetValue()
                )
            else:
                panel.SetResult(
                    data_ctrl.GetValue(),
                    timeout_ctrl.GetValue(),
                    count_ctrl.GetValue(),
                    read_timeout_ctrl.GetValue(),
                    returnformat_ctrl.GetValue(),
                    debug_ctrl.GetValue(),
                    disable_infrared_while_write_ctrl.GetValue()
                )


class read(eg.ActionBase):
    def GetLabel(self, *args):
        label = self.name

        if args:
            label += ": " + ";".join("%s" % str(arg) for arg in args)

        return label

    def __call__(
        self,
        num_bytes=None,
        timeout=1,
        returnformat="Hex",
        debug=False
    ):
        global global_serial_buffer

        if num_bytes is None:
            num_bytes = 2147483647

        data = ""

        endtime = time.time() + timeout

        while len(global_serial_buffer) < num_bytes:
            if time.time() > endtime:
                break
            time.sleep(0.1)

        data += global_serial_buffer[:num_bytes]
        global_serial_buffer = global_serial_buffer[num_bytes:]

        if len(data) > 0:
            if debug is True:
                print("Len: " + str(len(data)))
            if returnformat.lower() == "original".lower() or debug is True:
                if returnformat.lower() == "original".lower():
                    returndata = data
                if debug is True:
                    print("Original: \"" + str(data) + "\"")

            if returnformat.lower() == "hex".lower() or debug is True:
                returndata_hex = ""
                for char in data:
                    returndata_hex += str("%02X" % (ord(char)))
                if returnformat.lower() == "hex".lower():
                    returndata = returndata_hex
                if debug is True:
                    print("Hex: \"" + str(returndata_hex) + "\"")

            if returnformat.lower() == "ASCII".lower() or debug is True:
                returndata_ascii = ""
                for char in data:
                    returndata_ascii += chr(int("%02d" % (ord(char))))
                if returnformat.lower() == "ASCII".lower():
                    returndata = returndata_ascii
                if debug is True:
                    print("Hex2ASCII: \"" + str(returndata_ascii) + "\"")

            if returnformat.lower() == "hex2int".lower() or debug is True:
                returndata_hex2int = ""
                for char in data:
                    returndata_hex2int += "%02X" % (ord(char))
                returndata_hex2int = int(returndata_hex2int, 16)
                if returnformat.lower() == "hex2int".lower():
                    returndata = returndata_hex2int
                if debug is True:
                    print("Hex2Int: \"" + str(returndata_hex2int) + "\"")

            if returnformat.lower() == "hex2intnegative".lower() or debug is True:
                returndata_hex2intnegative = ""
                for char in data:
                    returndata_hex2intnegative += "%02X" % (ord(char))
                returndata_hex2intnegative = int(
                    returndata_hex2intnegative, 16)
                if returndata_hex2intnegative > 2147483647:
                    # +2147483648 is -2147483648
                    # +2147483649 is -2147483647
                    # and so on
                    returndata_hex2intnegative = (
                        returndata_hex2intnegative - int("FFFFFFFF", 16) - 1)
                if returnformat.lower() == "hex2intnegative".lower():
                    returndata = returndata_hex2intnegative
                if debug is True:
                    print("Hex2IntNegative: \"" +
                          str(returndata_hex2intnegative) + "\"")

            if returnformat.lower() == "hex2time".lower() or debug is True:
                returndata_hex = ""
                for char in data:
                    returndata_hex += str("%02X" % (ord(char)))
                returndata_hex2time = ""
                n = 2
                for ch in [returndata_hex[i: i + n]
                           for i in range(0, len(returndata_hex), n)]:
                    returndata_hex2time += str("%02d" % (int(ch, 16)))
                if returnformat.lower() == "hex2time".lower():
                    returndata = returndata_hex2time
                if debug is True:
                    print("Hex2Time: \"" + str(returndata_hex2time) + "\"")
        else:
            returndata = ""
            if debug is True:
                print("Original: \"\"")

        return returndata

    def Configure(
        self,
        num_bytes=None,
        timeout=1,
        returnformat="Hex",
        debug=False
    ):
        text = self.text
        panel = eg.ConfigPanel()

        if num_bytes is None:
            num_bytes = 2147483647
            flag = False
        else:
            flag = True

        rb1 = panel.RadioButton(not flag, text.read_all, style=wx.RB_GROUP)
        rb2 = panel.RadioButton(flag, text.read_some)

        count_ctrl = panel.SpinIntCtrl(num_bytes, 1, 2147483647)
        count_ctrl.Enable(flag)

        time_ctrl_label = panel.StaticText(text.read_time)
        time_ctrl = panel.SpinNumCtrl(
            timeout,
            min=0.0,
            max=10.0,
            allowNegative=False,
            increment=0.1,
            integerWidth=2,
            fractionWidth=2,
        )

        returnformat_ctrl_label = panel.StaticText(
            text.returnformat_ctrl_label)
        returnformat_ctrl = panel.ComboBox(
            returnformat, RETURNFORMATS, style=wx.CB_DROPDOWN | wx.CB_READONLY)

        read_ctrl = panel.StaticText(text.read)

        dummy_ctrl = panel.StaticText("")

        debug_ctrl = panel.CheckBox(debug, text.debug_Label)

        def on_radiobutton(event):
            flag = rb2.GetValue()
            count_ctrl.Enable(flag)
            event.Skip()

        rb1.Bind(wx.EVT_RADIOBUTTON, on_radiobutton)
        rb2.Bind(wx.EVT_RADIOBUTTON, on_radiobutton)

        eg.EqualizeWidths(
            (
                read_ctrl,
                returnformat_ctrl_label,
                time_ctrl_label,
                dummy_ctrl
            )
        )
        eg.EqualizeWidths(
            (
                returnformat_ctrl,
                time_ctrl,
                debug_ctrl
            )
        )

        Add = panel.sizer.Add
        Add(eg.HBoxSizer(read_ctrl, (5, 5), rb1))
        Add(eg.HBoxSizer(dummy_ctrl, (5, 5), rb2, count_ctrl,
                         (5, 5), panel.StaticText(text.bytes_name)))
        Add((5, 5))
        Add(eg.HBoxSizer(time_ctrl_label, (5, 5), time_ctrl))
        Add((5, 5))
        Add(panel.StaticText(text.read_info))
        Add(panel.StaticText(""))
        Add(eg.HBoxSizer(returnformat_ctrl_label, (5, 5), returnformat_ctrl))
        Add((5, 5))
        Add(eg.HBoxSizer(dummy_ctrl, (5, 5), debug_ctrl))

        while panel.Affirmed():
            if rb1.GetValue():
                panel.SetResult(
                    None,
                    time_ctrl.GetValue(),
                    returnformat_ctrl.GetValue(),
                    debug_ctrl.GetValue()
                )
            else:
                panel.SetResult(
                    count_ctrl.GetValue(),
                    time_ctrl.GetValue(),
                    returnformat_ctrl.GetValue(),
                    debug_ctrl.GetValue()
                )


class get_time(eg.ActionBase):
    def __call__(self):
        temp = write_advanced()

        return temp(data="TR", read_returnformat="hex2time")


class get_time_correction(eg.ActionBase):
    def __call__(self):
        temp = write_advanced()

        return temp(data="TCR", read_returnformat="hex2intnegative")


class get_daylight_saving(eg.ActionBase):
    def __call__(self):
        temp = write_advanced()

        return temp(data="TDR", read_returnformat="hex2int")


class sync_time(eg.ActionBase):
    def GetLabel(self, *args):
        label = self.name

        if args:
            label += ": " + ";".join("%s" % str(arg) for arg in args)

        return label

    def __call__(self, calibrate=False):
        temp = write_advanced()

        return temp(
            data=("TS" + global_access_string +
                  time.strftime("%y%m%d%H%M%S") + calibrate),
            read_returnformat="hex",
        )

    def Configure(self, calibrate=False):
        text = self.text
        panel = eg.ConfigPanel()

        calibrate_ctrl = panel.CheckBox(calibrate, text.calibrate_ctrl_label)

        Add = panel.sizer.Add
        Add(calibrate_ctrl)

        while panel.Affirmed():
            if calibrate_ctrl.GetValue() is False:
                calibrate = ""
            else:
                calibrate = "C"
            panel.SetResult(
                calibrate
            )


class set_time_correction(eg.ActionBase):
    def __call__(self, correction=0):
        temp = write_advanced()

        return temp(
            data=("TCS" + global_access_string + str(correction)),
            read_returnformat="hex"
        )

    def GetLabel(self, *args):
        label = self.name

        if args:
            label += ": " + ";".join("%s" % str(arg) for arg in args)

        return label

    def Configure(self, correction=0):
        text = self.text
        panel = eg.ConfigPanel()

        correction_ctrl = panel.SpinIntCtrl(
            correction, min=-2147483648, max=2147483647)
        correction_ctrl_label = panel.StaticText(text.correction_ctrl_label)

        Add = panel.sizer.Add
        Add(eg.HBoxSizer(correction_ctrl_label, (5, 5), correction_ctrl))

        while panel.Affirmed():
            panel.SetResult(
                correction_ctrl.GetValue()
            )


class get_waketime(eg.ActionBase):
    def __call__(self):
        temp = write_advanced()

        return temp(data="WR", read_returnformat="hex2time")


class configure_daylight_saving(eg.ActionBase):
    def GetLabel(self, *args):
        label = self.name

        if args:
            label += ": " + ";".join("%s" % str(arg) for arg in args)

        return label

    def __call__(self, daylight=1):
        temp = write_advanced()

        return temp(
            data=("TDS" + global_access_string + str(daylight)),
            read_returnformat="hex"
        )

    def Configure(self, daylight=1):
        text = self.text
        panel = eg.ConfigPanel()

        daylight_ctrl = panel.CheckBox(daylight, text.daylight_ctrl_label)

        Add = panel.sizer.Add
        Add(daylight_ctrl)

        while panel.Affirmed():
            if daylight_ctrl.GetValue() is False:
                daylight = 0
            else:
                daylight = 1

            panel.SetResult(
                daylight
            )


class set_waketime(eg.ActionBase):
    def __call__(
        self,
        waketime="0000000000",
        year=0,
        month=1,
        day=2,
        hour=3,
        minute=4,
        delete=1,
    ):
        temp = write_advanced()

        return temp(
            data=("WS" + global_access_string + str(waketime)),
            read_returnformat="hex"
        )

    def GetLabel(self, *args):
        label = self.name

        if args:
            label += ": " + ";".join("%s" % str(arg) for arg in args)

        return label

    def Configure(
        self,
        waketime="0000000000",
        year=0,
        month=1,
        day=2,
        hour=3,
        minute=4,
        delete=1,
    ):
        text = self.text
        panel = eg.ConfigPanel()

        delete_ctrl = panel.CheckBox(delete, text.delete_ctrl_label)
        year_ctrl = panel.SpinIntCtrl(year, 0, 99)
        month_ctrl = panel.SpinIntCtrl(month, 1, 12)
        day_ctrl = panel.SpinIntCtrl(day, 1, 31)
        hour_ctrl = panel.SpinIntCtrl(hour, 0, 23)
        minute_ctrl = panel.SpinIntCtrl(minute, 0, 59)

        year_ctrl_label = panel.StaticText(text.year_label_ctrl_label)
        month_ctrl_label = panel.StaticText(text.month_label_ctrl_label)
        day_ctrl_label = panel.StaticText(text.day_label_ctrl_label)
        hour_ctrl_label = panel.StaticText(text.hour_label_ctrl_label)
        minute_ctrl_label = panel.StaticText(text.minute_label_ctrl_label)

        waketime_label_ctrl = panel.StaticText(text.waketime_label_ctrl_label)
        waketime_cleartext_label_ctrl = panel.StaticText(
            text.waketime_cleartext_label_ctrl_label)
        waketime_ctrl = panel.StaticText(waketime)
        waketime_cleartext_ctrl = panel.StaticText("")

        year_ctrl.Enable(not delete)
        month_ctrl.Enable(not delete)
        day_ctrl.Enable(not delete)
        hour_ctrl.Enable(not delete)
        minute_ctrl.Enable(not delete)

        def on_checkbox(event):
            flag = delete_ctrl.GetValue()
            year_ctrl.Enable(not flag)
            month_ctrl.Enable(not flag)
            day_ctrl.Enable(not flag)
            hour_ctrl.Enable(not flag)
            minute_ctrl.Enable(not flag)

            if flag is True:
                waketime_ctrl.SetLabel("0000000000")
                waketime_cleartext_ctrl.SetLabel(
                    text.waketime_cleartext_label_ctrl_disable_text)
                panel.EnableButtons(True)

            event.Skip()

        def on_time_change(event):
            try:
                waketime_ctrl.SetLabel(
                    "%02d" % year_ctrl.GetValue()
                    + str("%02d" % month_ctrl.GetValue())
                    + str("%02d" % day_ctrl.GetValue())
                    + str("%02d" % hour_ctrl.GetValue())
                    + str("%02d" % minute_ctrl.GetValue())
                )

                waketime_cleartext_ctrl.SetLabel(
                    str(time.strftime("%c", time.strptime(str(waketime_ctrl.GetLabel()), "%y%m%d%H%M"))))
                panel.EnableButtons(True)
            except BaseException:
                panel.EnableButtons(False)
                waketime_cleartext_ctrl.SetLabel(
                    text.waketime_cleartext_label_ctrl_invalid_text)
                waketime_ctrl.SetLabel(text.waketime_ctrl_invalid_text)

            event.Skip()

        delete_ctrl.Bind(wx.EVT_CHECKBOX, on_checkbox)
        delete_ctrl.Bind(wx.EVT_CHECKBOX, on_time_change)

        year_ctrl.Bind(wx.EVT_TEXT, on_time_change)
        month_ctrl.Bind(wx.EVT_TEXT, on_time_change)
        day_ctrl.Bind(wx.EVT_TEXT, on_time_change)
        hour_ctrl.Bind(wx.EVT_TEXT, on_time_change)
        minute_ctrl.Bind(wx.EVT_TEXT, on_time_change)

        if delete_ctrl.GetValue() is True:
            waketime_cleartext_ctrl.SetLabel(
                text.waketime_cleartext_label_ctrl_disable_text)
        else:
            try:
                waketime_cleartext_ctrl.SetLabel(str(time.strftime(
                    "%c", time.strptime(str(waketime_ctrl.GetLabel()), "%y%m%d%H%M"))))
            except:
                waketime_cleartext_ctrl.SetLabel(
                    text.waketime_cleartext_label_ctrl_invalid_text)

        eg.EqualizeWidths(
            (year_ctrl, month_ctrl, day_ctrl, hour_ctrl, minute_ctrl))
        eg.EqualizeWidths((year_ctrl_label, day_ctrl_label, hour_ctrl_label))
        eg.EqualizeWidths((month_ctrl_label, minute_ctrl_label))
        eg.EqualizeWidths((waketime_label_ctrl, waketime_cleartext_label_ctrl))

        Add = panel.sizer.Add
        Add(delete_ctrl)
        Add(panel.StaticText(""))
        Add(eg.HBoxSizer(year_ctrl_label, (5, 5), year_ctrl, (10, 5), month_ctrl_label,
                         (5, 5), month_ctrl, (10, 5), day_ctrl_label, (5, 5), day_ctrl))
        Add((5, 5))
        Add(eg.HBoxSizer(hour_ctrl_label, (5, 5), hour_ctrl,
                         (10, 5), minute_ctrl_label, (5, 5), minute_ctrl))
        Add(panel.StaticText(""))
        Add(eg.HBoxSizer(waketime_cleartext_label_ctrl,
                         (5, 5), waketime_cleartext_ctrl))
        Add(eg.HBoxSizer(waketime_label_ctrl, (5, 5), waketime_ctrl))

        while panel.Affirmed():
            panel.SetResult(
                waketime_ctrl.GetLabel(),
                year_ctrl.GetValue(),
                month_ctrl.GetValue(),
                day_ctrl.GetValue(),
                hour_ctrl.GetValue(),
                minute_ctrl.GetValue(),
                delete_ctrl.GetValue(),
            )


class reset(eg.ActionBase):
    def __call__(self):
        temp = write_advanced()

        return temp(data="R", read_returnformat="original")


class initialize(eg.ActionBase):
    def __call__(self):
        temp = write_advanced()

        return temp(data="I", read_returnformat="original")


class initialize_reset(eg.ActionBase):
    def __call__(self):
        temp = write_advanced()

        temp(data="I", timeout=0.1, read_num_bytes=0)

        return temp(
            data="R",
            timeout=0,
            read_num_bytes=2,
            read_timeout=1,
            read_returnformat="original",
        )


class configure_infrared(eg.ActionBase):
    def GetLabel(self, *args):
        label = self.name

        if args:
            label += ": " + ";".join("%s" % str(arg) for arg in args)

        return label

    def __call__(self, infrared=1):
        temp = write_advanced()

        if infrared == 0:
            return temp(
                data=("L" + global_access_string),
                read_returnformat="hex"
            )
        else:
            return temp(data="C", read_returnformat="hex")

    def Configure(self, infrared=1):
        text = self.text
        panel = eg.ConfigPanel()

        infrared_ctrl = panel.CheckBox(infrared, text.infrared_ctrl_label)

        Add = panel.sizer.Add
        Add(infrared_ctrl)

        while panel.Affirmed():
            if infrared_ctrl.GetValue() is False:
                infrared = 0
            else:
                infrared = 1

            panel.SetResult(
                infrared
            )


class enable_led(eg.ActionBase):
    def __call__(self):
        temp = write_advanced()

        return temp(data="z")


class get_firmware_version(eg.ActionBase):
    def __call__(self):
        temp = write_advanced()

        returndata = temp(
            data="VV",
            timeout=0,
            read_num_bytes=2,
            read_timeout=1,
            read_returnformat="hex",
            read_debug=False,
        )

        return returndata[0] + "." + returndata[1]


class get_hardware_version(eg.ActionBase):
    def __call__(self):
        temp = write_advanced()

        returndata = temp(
            data="VV",
            timeout=0,
            read_num_bytes=2,
            read_timeout=1,
            read_returnformat="hex",
            read_debug=False,
        )

        return returndata[2] + "." + returndata[3]

#
# PyUSB definitions
#

#	Copyright (C) 2007 Pablo Bleyer Kocik
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


OK = 0
INVALID_HANDLE = 1
DEVICE_NOT_FOUND = 2
DEVICE_NOT_OPENED = 3
IO_ERROR = 4
INSUFFICIENT_RESOURCES = 5
INVALID_PARAMETER = 6
INVALID_BAUD_RATE = 7

DEVICE_NOT_OPENED_FOR_ERASE = 8
DEVICE_NOT_OPENED_FOR_WRITE = 9
FAILED_TO_WRITE_DEVICE = 10
EEPROM_READ_FAILED = 11
EEPROM_WRITE_FAILED = 12
EEPROM_ERASE_FAILED = 13
EEPROM_NOT_PRESENT = 14
EEPROM_NOT_PROGRAMMED = 15
INVALID_ARGS = 16
NOT_SUPPORTED = 17
OTHER_ERROR = 18

def SUCCESS(status): return status == OK

# OpenEx Flags
OPEN_BY_SERIAL_NUMBER = 1
OPEN_BY_DESCRIPTION = 2
OPEN_BY_LOCATION = 4

# ListDevices Flags (used in conjunction with OpenEx Flags
LIST_NUMBER_ONLY	= 0x80000000
LIST_BY_INDEX = 0x40000000
LIST_ALL = 0x20000000
LIST_MASK = (LIST_NUMBER_ONLY | LIST_BY_INDEX | LIST_ALL)


# Baud Rates
BAUD_300	= 300
BAUD_600	= 600
BAUD_1200 = 1200
BAUD_2400 = 2400
BAUD_4800 = 4800
BAUD_9600 = 9600
BAUD_14400 = 14400
BAUD_19200 = 19200
BAUD_38400 = 38400
BAUD_57600 = 57600
BAUD_115200 = 115200
BAUD_230400 = 230400
BAUD_460800 = 460800
BAUD_921600 = 921600

# Word Lengths
BITS_8 = 8
BITS_7 = 7
BITS_6 = 6
BITS_5 = 5

# Stop Bits
STOP_BITS_1= 0
STOP_BITS_1_5 = 1
STOP_BITS_2 = 2

# Parity
PARITY_NONE = 0
PARITY_ODD = 1
PARITY_EVEN = 2
PARITY_MARK = 3
PARITY_SPACE = 4

# Flow Control
FLOW_NONE = 0x0000
FLOW_RTS_CTS = 0x0100
FLOW_DTR_DSR = 0x0200
FLOW_XON_XOFF = 0x0400

# Purge rx and tx buffers
PURGE_RX = 1
PURGE_TX = 2

# Events
# typedef void (*PEVENT_HANDLER)(DWORD,DWORD);
EVENT_RXCHAR = 1
EVENT_MODEM_STATUS = 2

# Timeouts
DEFAULT_RX_TIMEOUT = 300
DEFAULT_TX_TIMEOUT = 300


# Device types
# typedef ULONG	DEVICE;
DEVICE_BM = 0
DEVICE_AM = 1
DEVICE_100AX = 2
DEVICE_UNKNOWN = 3
DEVICE_2232C = 4
DEVICE_232R = 5

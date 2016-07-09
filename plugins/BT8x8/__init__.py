"""EventGhost Plugin for BT8x8 GPIO-based remotes.

Requires DScaler to be installed.

Thanks also to the DScaler project's RegSpy.exe tool, which is the basis of
regspy.dll, making it possible to read the remote in a minimally invasive
fashion (no need for exclusive hardware access), and without requiring
administrator rights.

Some credit goes also to the BT8x8 plugins produced by the Girder community I
studied many variants to learn the basic pattern of how the remote functions
on most (but not all) BT8x8 cards.

This plugin was developed for the AverTvStudio card. The concepts are
fairly simple and with minor changes it should be possible to adapt the
plugin to many different BT8x8-based devices.

If you want to adapt the plugin to a differnt BT8x8 card, the only essential
details that you need to figure out are the _KEY_MASK and KEYMAP, _DOWN_BIT
(or some other way to different down and up). You can determine your device_id
and vendor_id from regspy.exe.

The function of the "ack bit" is probably specific to the AverTvStudio card,
and it isn't totally necessary to handle the ack bit properly. You could just
strip out all the code related to the ack bit. It isn't essential, given any
reasonable polling rate.

Similarly for the down bit. I could imagine a card where the remote doesn't
give you keyup signals, or doesn't encode it into a single bit, so you may
need to tweak _ReadKey. If you are particularly unlucky, you might have a card
that doesn't provide keyup events, so you would need to modify _BtPoller.

It might be amusing to create a fancy UI that could learn a reasonable
configuration by having the user press all the keys, but given the age of these
cards and the impending doom of analog TV, it might not be worth the trouble.
"""

eg.RegisterPlugin(
    name = "BT8x8-based Remote",
    author = "Chris B",
    version = "0.0.0",
    kind = "remote",
    guid = "{D812BA67-8C9A-40F7-AC97-623837DBD9B4}",
    description = ("AverTvStudio remote, may work for other bt8x8 cards. "
                   "Requires Dscaler to be installed."),
)

import ctypes
import eg
import os
import threading
import time


def _GetModulePath():
    return os.path.abspath(os.path.split(__file__)[0])


class BtRemote(eg.PluginClass):
    """Plugin for generating events from a bt8x8 card"""
    # There are many different vendor/device combinations.
    # See DScaler's Regspy.exe tool for more detail if you want to generalize this
    # plugin
    _DEVICES = [  #(vendor_id, device_id) pairs
            (0x109e, 0x0350),
            (0x109e, 0x0351),
            (0x109e, 0x036e),  # This is the only one I have used
            (0x109e, 0x036f)]

    # The GPIO register represents the state of 32 pins attached to the
    # BT8x8 chip. This is typically used to read the remote control, and to
    # control miscellanous hardware on the card.
    _GPIO_ADDRESS = 0x200  # Address of the GPIO register - General Purpose IO

    # These bits tell us what key is being pressed
    _KEY_MASK = 0x00F88000
    # This bit tells us whether the key is down or up
    _DOWN_BIT = 0x00010000

    # Each bit of the GPIO bus can independantly be configured to function
    # either as an input or an output.
    #
    # The Output Enable Register controls the mode for each corrsponding bit of
    # the GPIO bus. 0 means the pin is an input, 1 means output.
    _GPIO_OE_ADDRESS = 0x118

    # When a button is pressed on the remote, it sets a key code on the
    # key_mask bits and raises the down bit
    #
    # On key release, the card waits until the ack bit is set before it clears
    # the down bit.
    #
    # In this way, when we lower the ack bit we can be sure we
    # won't miss events if a key is pressed and released faster than we poll.
    _ACK_BIT = 0x00001000

    # We poll the GPIO for changes
    # We poll fast when a key is down. Delays lower than 0.015 don't actually
    # go any faster on windows because of the precision of time.sleep:
    # everything between .015 and .0001 is the same, and anything below .0001
    # is like zero. In any case .015 is more than fast enough; this is a
    # remote, not a gaming controller.
    _FAST_POLL = 0.015  # seconds.
    # We switch to slow polling approx 30 seconds after the last keyup event.
    _IDLE_LIMIT = int(30 / _FAST_POLL)  # number of iterations
    _SLOW_POLL = 0.1  # seconds.

    def _CloseHardware(self):
        # I don't know why, but deleting the card at this point will
        # prevent the plugin from working until you restart EventGhost.
        # It shouldn't be a big deal, since you most likely arent enabling and
        # disabling the plugin enough times to leak any mentionable amount of
        # memory.
        # self._regspydll.DeleteCard(self._card)
        self._regspydll.DeleteDriver(self._driver)

    def _RaiseAck(self):
        gpio = self._regspydll.ReadDword(self._card, self._GPIO_ADDRESS)
        gpio = gpio | self._ACK_BIT
        self._regspydll.WriteDword(self._card, self._GPIO_ADDRESS, gpio)

    def _LowerAck(self):
        gpio = self._regspydll.ReadDword(self._card, self._GPIO_ADDRESS)
        gpio = gpio & (~self._ACK_BIT)
        self._regspydll.WriteDword(self._card, self._GPIO_ADDRESS, gpio)

    def _SetupOutputEnable(self):
        """Update the GPIO output enable register so we can read the remote.

        Attempts to avoid modifying bits that aren't related to the remote.
        """
        # Set up our ins and outs.
        oe = self._regspydll.ReadDword(self._card, self._GPIO_OE_ADDRESS)
        # Make the mask bits be inputs so we can actually read the remote.
        oe = oe & (~(self._KEY_MASK | self._DOWN_BIT))
        # Make the ack bit be an output so we can raise/lower it.
        oe = oe | self._ACK_BIT
        self._regspydll.WriteDword(self._card, self._GPIO_OE_ADDRESS, oe)

    def _SetupHardware(self):
        """Must be called successfully before ReadKey."""
        self._driver = self._regspydll.GetDriver()
        if not self._driver:
            raise self.Exception("Couldn't open the bt8x8 driver")
        for vendorId, deviceId in self._DEVICES:
            card = self._regspydll.OpenCard(
                    self._driver, vendorId, deviceId, 0)
            if card:
                self._card = card
                self._SetupOutputEnable()
                break
        else:
            self._regspydll.DeleteDriver(self._driver)
            self._driver = None
            raise self.Exception("Unable to find open a bt8x8 card.")

    def _ReadKey(self):
        """Read a key off the remote.

        Returns:
          (key_name, down?)
        """
        gpio = self._regspydll.ReadDword(self._card, self._GPIO_ADDRESS)
        code = gpio & self._KEY_MASK
        name = _KEY_MAP.get(code, '%08x' % code)
        down = gpio & self._DOWN_BIT
        return name, down

    def __start__(self):
        dll_path = os.path.join(_GetModulePath(), 'regspydll.dll')
        try:
            self._regspydll = ctypes.cdll.LoadLibrary(dll_path)
        except WindowsError:
            print 'Unable to load regspydll.dll'
            self._regspydll = None

        if self._regspydll is None:
            return
        self._SetupHardware()
        self._stop = threading.Event()
        self._poller = threading.Thread(target=self._BtPoller)
        self._poll_delay = self._SLOW_POLL
        self._poller.start()
        print 'bt8x8 Started'

    def _BtPoller(self):
        """Run in a separate thread to poll the remote for new events.

        Args:
          stop: threading.Event - the polling loop will stop when this event
            is set.
        """
        # This probably doesn't really save much time:
        stop = self._stop
        ReadKey = self._ReadKey
        fast_poll = self._FAST_POLL
        slow_poll =  self._SLOW_POLL
        idle_limit = self._IDLE_LIMIT
        RaiseAck = self._RaiseAck
        LowerAck = self._LowerAck
        TriggerEvent = self.TriggerEvent
        TriggerEnduringEvent = self.TriggerEnduringEvent

        idle_count = 0  # iterations since last event
        last_key, last_down = ReadKey()
        up_suffix = ' u'
        down_suffix = ' d'
        while not stop.isSet():
            key, down = ReadKey()

            # Fill in any logically missing events:
            #   This generally never happens unless you use very slow poll
            #   delays, like .5 seconds or slower.
            if key != last_key:
                if last_down:
                    # We missed the previous key's up event
                    TriggerEvent(last_key + up_suffix)
                if not down:
                    # We missed this key's down event.
                    TriggerEvent(key + down_suffix)

            # Handle actual events:
            if key != last_key or down != last_down:
                if down:
                    RaiseAck()
                    TriggerEnduringEvent(key + down_suffix)
                else:  # up
                    LowerAck()
                    TriggerEvent(key + up_suffix)
                idle_count = 0
                last_key, last_down = key, down
            else:  # no event
                if idle_count > idle_limit and not down:
                    stop.wait(slow_poll)
                else:
                    idle_count += 1
                    time.sleep(fast_poll)

    def __stop__(self):
        if self._regspydll is None:
            return
        self._stop.set()
        self._CloseHardware()
        self._poller.join()


# Map key codes to key names.
_KEY_MAP = dict((
    (0x00808000, 'green'),
    (0x00408000, 'channel[<]'),
    (0x00c08000, 'channel[>]'),
    (0x00008000, 'blue'),
    (0x00b80000, 'red'),
    (0x00780000, 'volume[-]'),
    (0x00f80000, 'volume[+]'),
    (0x00380000, 'yellow'),
    (0x00980000, 'record'),
    (0x00580000, 'pause'),
    (0x00d80000, 'stop'),
    (0x00180000, 'play'),
    (0x00a80000, 'autoscan'),
    (0x00680000, 'freeze'),
    (0x00e80000, 'capture'),
    (0x00280000, 'mute'),
    (0x00880000, '0'),
    (0x00480000, 'display'),
    (0x00c80000, 'loop'),
    (0x00080000, 'preview'),
    (0x00b00000, '7'),
    (0x00700000, '8'),
    (0x00f00000, '9'),
    (0x00300000, 'fullscr'),
    (0x00900000, '4'),
    (0x00500000, '5'),
    (0x00d00000, '6'),
    (0x00100000, 'audio'),
    (0x00a00000, '1'),
    (0x00600000, '2'),
    (0x00e00000, '3'),
    (0x00200000, 'video'),
    (0x00800000, 'tvfm'),
    (0x00400000, 'cd'),
    (0x00c00000, 'teletext'),
    (0x00000000, 'power')))

"""OO wrapper around the AutoHotKey control manipulation functions.

This module gives a simplified wrapper around the loose collection of AHK
functions related to manipulation of window controls.
"""
import time
from functools import partial, wraps
from ahk import *

def _delay(method):
    """Decorator to add delay behavior to Control methods."""
    @wraps(method)
    def delayed(self, *args, **kwargs):
        """Inner function.""" # For pylint
        # Store old values of delay and set new delays
        if self._cdelay is not None:
            execute("{0} := A_ControlDelay".format('c'+self._tmpname))
            execute("SetControlDelay, {0}".format(self._cdelay))
        if self._kdelay is not None:
            execute("{0} := A_KeyDelay".format('k'+self._tmpname))
            execute("SetKeyDelay, {0}".format(self._kdelay))
        # Run the wrapped method
        method(self, *args, **kwargs)
        # Restore saved delay values
        if self._cdelay is not None:
            execute("SetControlDelay, %{0}%".format('c'+self._tmpname))
        if self._kdelay is not None:
            execute("SetKeyDelay, %{0}%".format('k'+self._tmpname))
    return delayed

class Control(object):
    """Wrapper around ahk window control commands."""

    def __init__(self, script, title="", text="", extitle="", extext="", 
                 store=True):
        """Initialize a new Control object.
        
        Stores information about the window who's controls you will manipulate.

        :param script: Script object to use internally.
        :type script: ahk.Script instance
        :param title: Partial window title text to match.
        :type title: str (default="")
        :param text: Partial window text to match.
        :type text: str (default="")
        :param extitle: Partial window title text to avoid.
        :type extitle: str (default="")
        :param extext: Partial window text to avoid.
        :type extext: str (default="")
        :param store: Whether to cache the found window.
        :type store: bool
        :raises: NameError if store=True but a matching window can't be found.
        """
        self.script = script
        self.params = (title, text, extitle, extext)
        self.hwnd = None
        if store:
            self.hwnd = script.winExist(title, text, extitle, extext)
            if not self.hwnd:
                win = "win(title={0}, text={1}, extitle={2}, extext={3})"
                raise NameError("Can't find matching window:\n\t" + 
                                win.format(*self.params))
        # Internal state
        self._tmpname = "tmp{0}".format(str(int(time.time())))
        self._cdelay = None # control delay
        self._kdelay = None # key delay

    def _params(self):
        """Internal method to clean-up duplicate parameter code."""
        if self.hwnd:
            title = "ahk_id {0}".format(self.hwnd)
            text, extitle, extext = "", "", ""
        else:
            title, text, extitle, extext = self.params
        return title, text, extitle, extext

    def set_delay(self, control='', key=''):
        """Set the control or key delay used by this Control object.

        Either the control delay, key delay, or both may be set.
        Setting either to `None` will disable the local delay setting.
        See `AHK docs <http://www.autohotkey.com/docs/commands/SetControlDelay.htm>`_
        for more details.

        :param control: The delay to use when modifying a control.
        :type control: float or None
        :param key: The delay to use for ``send``-ing key events.
        :type key: float or None
        """
        if control != '':
            self._cdelay = control
        if key != '':
            self._kdelay = key

    @_delay
    def click(self, control="", pos=None, button="", count=1, options=""):
        """Sends mouse input to a control.
        
        The control arg can be a class name, window handle, or text string.
        Alternately pos as a (x, y) tuple may be provided indicating the mouse
        coordinates relative to the top-left corner of the application window
        in which to click. If both control and pos are provided pos is 
        interpreted relative to the indicated control.

        Default is a single left click, but you can send left/right/middle,
        wheel up or down left or right with a repeat count.
        See `AHK docs <http://www.autohotkey.com/docs/commands/ControlClick.htm>`_
        for more details.

        :param control: The class, HWND, or text of the control to click.
        :type control: str
        :param pos: The relative coordinates of at which to click.
        :type pos: tuple (indexable)
        :param button: The name of the button to be clicked.
        :type button: str
        :param count: Number of times it should be clicked.
        :type count: int
        :param options: Optional arguments.
        :type options: str
        """
        title, text, extitle, extext = self._params()

        if pos:
            pos = "X{0[0]} Y{0[1]}".format(pos)
            # Add pos option to force coordinate interpretation
            options += " pos"
            if not control:
                control = pos
            else:
                options += " " + pos
        # Setup window id args
        cmd = "ControlClick, {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}"
        execute(cmd.format(control, title, text, button, count, 
                           options, extitle, extext))

    @_delay
    def send(self, control="", keys="", raw=False):
        """Send keystrokes to a control.

        See `AHK docs <http://www.autohotkey.com/docs/commands/ControlSend.htm>`_
        for more details.

        :param control: The class, HWND, or text of the control to send to.
        :type control: str
        :param keys: Keystrokes in the same format as ahk.Script.send.
        :type keys: str
        :param raw: Toggle raw input mode.
        :type raw: bool (default False)
        """
        title, text, extitle, extext = self._params()

        cmd = "ControlSend"
        if raw:
            cmd = "ControlSendRaw"
        cmd = cmd + ", {0}, {1}, {2}, {3}, {4}" 
        execute(cmd.format(control, keys, title, text, extitle, extext))

    @_delay
    def setText(self, control="", value=""):
        """Set the text content of a control.

        See `AHK docs <http://www.autohotkey.com/docs/commands/ControlSetText.htm>`_
        for more details.

        :param control: The class, HWND, or text of the control to be changed.
        :type control: str
        :param value: New text to substitute into the control.
        :type value: str
        """
        title, text, extitle, extext = self._params()

        execute("ControlSetText, {0}, {1}, {2}, {3}, {4}, {5}".format(
            control, value, title, text, extitle, extext))

    def get_choices(self, control=""):
        """Retrieve the available values from a ComboBox.

        :param control: The class, HWND, or text of the control to be checked.
        :type control: str
        :returns: A list of value strings (in order).
        """
        title, text, extitle, extext = self._params()

        execute("ControlGet, {0}, List,,{1},{2},{3},{4}".format(
            self._tmpname, control, title, text, extitle, extext))
        return get(self._tmpname).split('\n')

    def get_chosen(self, control=""):
        """Retrieve the selected value from a ComboBox.

        :param control: The class, HWND, or text of the control to be checked.
        :type control: str
        :returns: Selected value as a string.
        """
        title, text, extitle, extext = self._params()

        execute("ControlGet, {0}, Choice,,{1},{2},{3},{4}".format(
            self._tmpname, control, title, text, extitle, extext))
        return get(self._tmpname)

    @_delay
    def choose(self, control="", value=""):
        """Pick an item from a listbox or combobox.

        See `AHK docs <http://www.autohotkey.com/docs/commands/Control.htm>`_
        for more details.

        :param control: The class, HWND, or text of the control to be changed.
        :type control: str
        :param value: Partial text of choice or choice index (starting from 1).
        :type value: str or int (default="")
        """
        title, text, extitle, extext = self._params()

        cmd = "ChooseString"
        if type(value) not in (str, unicode):
            cmd = "Choose"
        execute("Control, {0}, {1}, {2}, {3}, {4}, {5}, {6}".format(  
            cmd, value, control, title, text, extitle, extext))

    def is_checked(self, control=""):
        """Check if a checkbox control is checked.
        
        :param control: The class, HWND, or text of the control to be checked.
        :type control: str
        :returns: True if it was checked, else False.
        """
        title, text, extitle, extext = self._params()

        execute("ControlGet, {0}, Checked,,{1},{2},{3},{4}".format(
            self._tmpname, control, title, text, extitle, extext))
        result = int(get(self._tmpname))
        if result == 1:
            return True
        return False

    @_delay
    def check(self, control="", state=None):
        """Pick an item from a listbox or combobox.

        The state can be set to checked (True), unchecked (False), 
        or toggle (None), default is toggle.
        See `AHK docs <http://www.autohotkey.com/docs/commands/Control.htm>`_
        for more details.

        :param control: The class, HWND, or text of the control to be changed.
        :type control: str
        :param state: The desired checked state.
        :type state: bool or None
        """
        title, text, extitle, extext = self._params()

        cmd = "Check"
        checked = self.is_checked(control)
        if state is None:
            if checked:
                cmd = "Uncheck"
        elif state and checked or not state and not checked:
            return # Want to be checked and already checked = nop
        elif not state and checked:
            cmd = "Uncheck"

        execute("Control, {0},, {1}, {2}, {3}, {4}, {5}".format(  
            cmd, control, title, text, extitle, extext))

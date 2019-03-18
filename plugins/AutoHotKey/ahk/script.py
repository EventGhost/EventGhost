"""OO wrapper around The AutoHotKey library.

This module contains higher-level object oriented wrappers around AHK scripting.
"""
import time
from functools import partial
from ahk import *

class Function(object):
    """Object wrapper around ahk functions"""
    template = "\n{0}{1} {{\n{2}\n}}"

    def __init__(self, name, result, args, body):
        """
        Called Functions are automatically transform to their result by calling
        the provided result function on the return value from the ahk function
        call.

        :param name: The name of the function to wrap.
        :type name: str
        :param result: Type of the expected result.
        :type result: callable type (default=str)
        :param args: The argument definition of the function.
        :type args: str (default='()')
        :param body: The body of the function (excluding braces).
        :type body: str (default='')
        """
        self.name = name
        self.definition = self.template.format(name, args, body)
        execute(self.definition)
        self.result = result
        # Because the ahkdll function call function is broken use temp
        # variables as a work-around.
        self.tmpname = "tmp{0}".format(str(int(time.time())))

    def __call__(self, *args):
        """Call the wrapped function and return the converted result."""
        args = ",".join(str(i) for i in args)
        # Execute the function and assign the result to the temp variable
        execute("{0} := {1}({2})".format(
            self.tmpname, self.name, args))
        # Get the result from the temp variable
        result = self.result(get(self.tmpname))
        # And delete the temp variable value
        set(self.tmpname, "")
        return result

class Script(object):
    """Wrapper around ahk script commands."""

    def __init__(self, script="", filename=None):
        """
        Initializes the ahk script engine just like calling the low-level
        function ahk.start followed by ahk.ready.
        """
        self._handle = start(script=script, filename=filename)
        ready()
        self._vars = dict()
        self._funcs = dict()
        self._tmpname = "tmp{0}".format(str(int(time.time())))

        # Add some default variables
        self.variable('Clipboard')
        self.variable('ErrorLevel', kind=partial(int, base=0))

    def __del__(self):
        """Call terminate to kill the script engine."""
        terminate()

    def variable(self, name, kind=str, value=''):
        """Create a new ahk variable wrapper.

        Wrapped variables are tracked by the instance and can be accessed as
        object attributes. Variables are automatically transformed to their
        declared kind by calling their kind with their ahk string value as the
        first argument (just like normal python type conversions).

        Variable wrappers are already provided for the special ahk Clipboard
        and ErrorLevel variables (Note the case).

        .. note::
            Variables are not allowed to start with '_' the underscore char!
        
        :param name: Then name of the new variable.
        :type name: str
        :param kind: Type of the variable (cast on get).
        :type kind: callable type (default=str)
        :param value: Initial value of the variable.
        :type value: match kind or str (default='')
        :raises: AttributeError if the provided name already exists in the
            instance as either a variable or an attribute.
        """
        if name[0] == '_':
            raise AttributeError(
                    "Variable names may not start with an underscore!")
        if hasattr(self, name):
            raise AttributeError(
                    "Name: {0} already exists as an attribute!".format(name))
        if name in self._vars:
            raise AttributeError(
                    "Name: {0} already exists as a variable!".format(name))
        if name in self._funcs:
            raise AttributeError(
                    "Name: {0} already exists as a function!".format(name))

        if set(name, value):
            self._vars[name] = kind
        else:
            raise AttributeError(
                    "Failure reported by ahk while setting {0}={1}!".format(
                        name, value))

    def function(self, name, result=str, args='()', body=''):
        """Create a new ahk function wrapper.
        
        Wrapped functions are tracked by the instance and can be accessed as
        object attributes. Functions are automatically transform to their
        result by calling the provided result function on the return value from
        the ahk function call.

        .. note::
            Function names are not allowed to start with '_' the underscore char!

        :param name: The name of the function to wrap.
        :type name: str
        :param result: Type of the expected result.
        :type result: callable type (default=str)
        :param args: The argument definition of the function.
        :type args: str (default='()')
        :param body: The body of the function (excluding braces).
        :type body: str (default='')
        :raises: AttributeError if the indicated name is already used.
        :returns: Function wrapper object.
        """
        if name[0] == '_':
            raise AttributeError(
                    "Function names may not start with an underscore!")
        if hasattr(self, name):
            raise AttributeError(
                    "Name: {0} already exists as an attribute!".format(name))
        if name in self._funcs:
            raise AttributeError(
                    "Name: {0} already exists as a function!".format(name))
        if name in self._vars:
            raise AttributeError(
                    "Name: {0} already exists as a variable!".format(name))

        func = Function(name, result, args, body)
        self._funcs[name] = func
        return func

    def send(self, keys, mode='SendInput'):
        """Convenience wrapper to send input to the active window.
        
        Sends a ahk formatted series of keystrokes to the active window.
        See `AHK docs <http://www.autohotkey.com/docs/commands/Send.htm>`_
        for more details.

        :param keys: The keys to be sent.
        :type keys: str
        :param mode: The ahk command used to send keys. Valid modes:

            * Send
            * SendRaw
            * SendInput
            * SendPlay
            * SendEvent

        :type mode: str
        """
        execute("{0} {1}".format(mode, keys))

    def click(self, button="", count=1, x=None, y=None):
        """Convenience wrapper to the ahk click function.

        Send a mouse click of any type to any coordinate with optional repeats.
        See `AHK docs <http://www.autohotkey.com/docs/commands/Click.htm>`_
        for more details.
        The button argument can actually take a number of options:

            * `blank` - Simple primary click.
            * right - Auxiliary button click.
            * wheelup - Send mouse wheel scroll event.
            * down - Press but don't release the primary button.
            * rel[ative] - Interpret coordinates in relative mode.
            * etc.

        Button options can be composed when not mutually exclusive 
        (e.g. "right down relative").

        Use count=0 with x and y to move the mouse without clicking.

        :param button: The mouse button(s) to click.
        :type button: str (default="")
        :param count: Number of times to repeat the click.
        :type count: int (default 1)
        :param x: Mouse x-coord.
        :type x: int
        :param y: Mouse y-coord.
        :type y: int
        """
        cmd = "Click {0}".format(button)
        if x or y: # Could fail for x&y = 0
            cmd += ", {0}, {1}".format(x, y)
        # Click count must occur "somewhere right of the coordinates"
        if count != 1:
            cmd += ", {0}".format(count)
        execute(cmd+'\n')

    def winActivate(self, title="", text="", 
                    extitle="", extext="", bottom=False):
        """Convenience wrapper for ahk WinActivate commands.
        
        Used to set a window with provided parameters as active.
        If all parameters are empty the `last found` window is activated.
        See `AHK docs <http://www.autohotkey.com/docs/commands/WinActivate.htm>`_
        for more details.

        :param title: Partial window title text to match.
        :type title: str (default="")
        :param text: Partial window text to match.
        :type text: str (default="")
        :param extitle: Partial window title text to avoid.
        :type extitle: str (default="")
        :param extext: Partial window text to avoid.
        :type extext: str (default="")
        :param bottom: Whether to act on the bottom-most window.
        :type bottom: bool (default=False)
        """
        cmd = "WinActivate"
        if bottom:
            cmd = "WinActivateBottom"
        if ''.join((title, text, extitle, extext)):
            cmd = '{0}, "{1}", "{2}", "{3}", "{4}"'.format(
                cmd, title, text, extitle, extext)
        #print cmd
        execute(cmd)

    def winActive(self, title="", text="", extitle="", extext=""):
        """Convenience wrapper for ahk IfWinActive command.
        
        Used to check if a window with provided parameters is active.
        If all parameters are empty the `last found` window is checked.
        See `AHK docs <http://www.autohotkey.com/docs/commands/IfWinActive.htm>`_
        for more details.

        :param title: Partial window title text to match.
        :type title: str (default="")
        :param text: Partial window text to match.
        :type text: str (default="")
        :param extitle: Partial window title text to avoid.
        :type extitle: str (default="")
        :param extext: Partial window text to avoid.
        :type extext: str (default="")
        :returns: The found window's HWND or None.
        """
        set(self._tmpname, '')
        execute('{0} := WinActive("{1}", "{2}", "{3}", "{4}")'.format(
            self._tmpname, title, text, extitle, extext))
        result = int(get(self._tmpname), 0)
        if result == 0:
            return None
        return result

    def winExist(self, title="", text="", extitle="", extext=""):
        """Convenience wrapper for ahk IfWinExist command.
        
        Used to check if a window with provided parameters exists.
        If all parameters are empty the `last found` window is checked.
        See `AHK docs <http://www.autohotkey.com/docs/commands/IfWinExist.htm>`_
        for more details.

        :param title: Partial window title text to match.
        :type title: str (default="")
        :param text: Partial window text to match.
        :type text: str (default="")
        :param extitle: Partial window title text to avoid.
        :type extitle: str (default="")
        :param extext: Partial window text to avoid.
        :type extext: str (default="")
        :returns: The found window's HWND or None.
        """
        set(self._tmpname, '')
        execute('{0} := WinExist("{1}", "{2}", "{3}", "{4}")'.format(
            self._tmpname, title, text, extitle, extext))
        result = int(get(self._tmpname), 0)
        if result == 0:
            return None
        return result

    def waitActive(self, title="", text="", timeout=5, 
                   extitle="", extext="", deactivate=False):
        """Convenience wrapper for ahk WinWaitActive command.
        
        Used to wait until a window matching the given parameters is activated.
        See `AHK docs <http://www.autohotkey.com/docs/commands/WinWaitActive.htm>`_
        for more details.

        :param title: Partial window title text to match.
        :type title: str (default="")
        :param text: Partial window text to match.
        :type text: str (default="")
        :param timeout: How long in seconds to wait for the window to activate.
            Use None to wait indefinitely.
        :type timeout: int or None (default=5)
        :param extitle: Partial window title text to avoid.
        :type extitle: str (default="")
        :param extext: Partial window text to avoid.
        :type extext: str (default="")
        :param deactivate: Toggle between WinWaitActive and WinWaitNotActive.
        :type deactivate: bool (default=False)
        :returns: The True if matching window is activated, else False.
        """
        cmd = "WinWaitActive"
        if deactivate:
            cmd = "WinWaitNotActive"
        if timeout is None:
            timeout = ""
        execute("{0}, {1}, {2}, {3}, {4}, {5}".format(
                cmd, title, text, timeout, extitle, extext))
        result = self.ErrorLevel
        if result != 0:
            return False
        return True

    def waitWindow(self, title="", text="", timeout=5, 
                   extitle="", extext="", closed=False):
        """Convenience wrapper for ahk WinWait command.
        
        Used to wait until a window matching the given parameters exists.
        See `AHK docs <http://www.autohotkey.com/docs/commands/WinWait.htm>`_,
        `AHK docs <http://www.autohotkey.com/docs/commands/WinWaitClose.htm>`_
        for more details.

        :param title: Partial window title text to match.
        :type title: str (default="")
        :param text: Partial window text to match.
        :type text: str (default="")
        :param timeout: How long in seconds to wait for the window to activate.
            Use None to wait indefinitely.
        :type timeout: int or None (default=5)
        :param extitle: Partial window title text to avoid.
        :type extitle: str (default="")
        :param extext: Partial window text to avoid.
        :type extext: str (default="")
        :param closed: Toggle between WinWait and WinWaitClose.
        :type closed: bool (default=False)
        :returns: The True if matching window is activated, else False.
        """
        cmd = "WinWait"
        if closed:
            cmd = "WinWaitClose"
        if timeout is None:
            timeout = ""
        execute("{0}, {1}, {2}, {3}, {4}, {5}".format(
                cmd, title, text, timeout, extitle, extext))
        result = self.ErrorLevel
        if result != 0:
            return False
        return True

    def convert_color(self, color):
        """Convert ahk color returned as a hex string to tuple of ints."""
        # Colors are returned as hex (e.g. 0xc0c0c0)
        r, g, b = color[2:4], color[4:6], color[6:8]
        return tuple((int(c, 16) for c in (r, g, b)))

    def _color_delta(self, c1, c2):
        """Compute the total error between to colors."""
        err = 0.0
        for i in range(3):
            err += abs(c1[i] - c2[i])
        result = err/float(255*3)
        #print c1, c2, result
        return result

    def getPixel(self, x=0, y=0, opt='RGB', screen=True):
        """Convenince wrapper around ahk PixelGetColor

        Gets the pixel color at the indicated coordinates.
        See `AHK docs <http://www.autohotkey.com/docs/commands/PixelGetColor.htm>`_
        for more details.

        :param x: The pixel x coordinate (relative to screen).
        :type x: int
        :param y: The pixel y coordinate (relative to screen).
        :type y: int
        :param opt: Space separated color picking options.
        :type opt: str (default='RGB')
        :param screen: Flag to use screen or relative coordinates.
        :type screen: bool (default=True)
        """
        if screen:
            execute("CoordMode, Pixel, Screen")
        else:
            execute("CoordMode, Pixel, Reletive")

        execute("PixelGetColor, {0}, {1}, {2}, {3}".format(
            self._tmpname, x, y, opt))
        return self.convert_color(get(self._tmpname))

    def waitPixel(self, x=0, y=0, color=None, 
                  threshold=0.01, interval=0.5, timeout=False):
        """Wait until the pixel at given coords changes color.

        This function can wait until the indicated pixel *is* a color,
        or until it changes color. If a color is not provided the current
        color of the pixel when the function starts is stored and compared
        at a regular interval until it changes or until timeout.

        :param x: The pixel x coordinate (relative to screen).
        :type x: int
        :param y: The pixel y coordinate (relative to screen).
        :type y: int
        :param color: The color to wait for.
        :type color: tuple(int r, int g, int b) or None
        :param threshold: Error factor allowed for determining color match.
        :type threshold: float
        :param interval: How often the pixel color is checked.
        :type interval: float
        :param timeout: How long to wait for a color match.
        :type timeout: float or None
        :returns: True if pixel changed, False if timeout.
        """
        # Get starting color
        match = True # We are trying by default to match the provided color
        if not color:
            match = False # If not given a color then we are trying to not match
            color = self.getPixel(x, y)

        # Timing loop
        start = time.time()
        now = start
        while 1:
            # Get new timing for current iteration
            now = time.time()
            # Handle timeout condition
            if timeout and (now - start) >= timeout:
                return False
            # Get new color reading
            current = self.getPixel(x, y)
            #print color, current
            #print self._color_delta(color, current)
            # Check for match
            if self._color_delta(color, current) <= threshold:
                if match:
                    return True
            else:
                if not match:
                    return True
            # Pause
            time.sleep(interval)

    def message(self, text="Alert", title="Alert", options=0, timeout=None):
        """Convenience wrapper to the ahk msgbox function.

        Displays a message box with buttons.
        See `AHK docs <http://www.autohotkey.com/docs/commands/MsgBox.htm>`_
        for more details.

        :param text: The body text of the msgbox.
        :type text: str (default='Alert')
        :param title: The title text of the msgbox.
        :type title: str (default='Alert')
        :param options: Button flags bit-field.
        :type options: int (default=0)
        :param timeout: Optional timeout, dialog is closed after timeout.
        :type timeout: int or None (default=None)
        """
        cmd = 'MsgBox {0}, {1}, {2}'.format(options, title, text)
        if timeout:
            cmd += ', {0}'.format(timeout)
        execute(cmd)

    def msgResult(self, name='OK'):
        """Convenience wrapper to the ahk ifMsgBox function.

        Get the clicked status of a button on the last MsgBox.
        See `AHK docs <http://www.autohotkey.com/docs/commands/ifMsgBox.htm>`_
        for more details.

        :param name: The name of the button to check.
        :type name: str (default='OK')
        :returns: True if button was pressed, None if timeout, False otherwise.
        """
        set(self._tmpname, '0')
        template = 'ifMsgBox, {0}\n\t{1} := 1\nifMsgBox, Timeout\n\t{1} := -1'
        execute(template.format(name, self._tmpname))
        result = int(get(self._tmpname))
        if result == 1:
            return True
        elif result == -1:
            return None
        return False

    def __getattr__(self, name):
        """Override attribute lookup to add ahk variable access."""
        #NOTE __getattr__ is only called on attrs that aren't found normally
        if name in self._vars:
            # The clipboard can't be directly read... Others?
            execute("{0} := {1}".format(self._tmpname, name))
            return self._vars[name](get(self._tmpname))
        elif name in self._funcs:
            return self._funcs[name]
        else:
            raise AttributeError("No variable named {0}!".format(name))

    def __setattr__(self, name, value):
        """Override attribute modification to add ahk variable access."""
        # Also filter names starting with '_' (special names).
        if name[0] == '_' or name in self.__dict__:
            super(Script, self).__setattr__(name, value)
        elif name in self._vars:
            set(name, value)
        elif name in self._funcs:
            raise AttributeError("Can't assign to function {0}!".format(name))
        else:
            raise AttributeError("No variable named {0}!".format(name))

"""Low-level wrappers around The AutoHotKey library.

Wrappers are provided for the functions found here:
    http://www.autohotkey.net/~HotKeyIt/AutoHotkey/files/Functions_List-txt.html
"""
import ctypes, time, os
from functools import wraps

# This try/except allows documentation to be generated without access to the dll
try:
    _ahk = ctypes.cdll.AutoHotkey #load AutoHotKey dll
except (WindowsError, OSError):
    # Try loading the dll from the module directory
    path = os.path.dirname(__file__)
    dllpath = os.path.join(path, 'AutoHotKey.dll')
    try:
        _ahk = ctypes.cdll.LoadLibrary(os.path.abspath(dllpath))
    except (WindowsError, OSError):
        print "Warning: Can't load AutoHotKey.dll, all ahk functions will fail."

def start(filename=None, script="", options="", params=""):
    """Wrapper around ahkdll and ahktextdll.
    
    Start a new ahk thread from file or a string.
    Defaults to an empty script with no options or params.
    Filename is preferred over script if provided.

    .. Note::
        Using any option besides ahk.start() seems not to work.
        Specifying a file doesn't cause it to run, passing a string
        doesn't cause it to be executed?

    :returns: Thread handle for created instance (see thread functions).
    """
    #print filename
    if filename:
        return _ahk.ahkdll(os.path.abspath(filename), options, params)
    else:
        return _ahk.ahktextdll(script, options, params)

def ready(nowait=False, retries=None):
    """Wrapper around ahkReady.
    
    Returns True if ahk is ready to use.
    By default this polls the dll function until it is ready.
    By calling with nowait=True the immediate result is returned instead.
    By calling with retries > 1 state will be checked at most retries times.
    """
    if nowait:
        retries = 1
    if retries and retries >= 1:
        for i in range(retries):
            if _ahk.ahkReady() == 1:
                return True
            time.sleep(0.01)
    else:
        while 1:
            if _ahk.ahkReady() == 1:
                return True
            time.sleep(0.1)
    return False

def add_lines(script="", filename=None, duplicates=False, ignore=True):
    """Wrapper around addFile and addScript.

    Adds lines to the running script from file or string.
    Lines added from string are evaluated immediately,
    lines added from file are not evaluated.
    Defaults to an empty script, no duplicates, and ignore errors.
    Filename is preferred over script if provided.

    :returns: Pointer address to first line in added script (see execute_line).
    """
    if filename:
        if duplicates:
            duplicates = 1
        else:
            duplicates = 0

        if ignore:
            if type(ignore) != int:
                ignore = 1
        else:
            ignore = 0
        return int(_ahk.addFile(os.path.abspath(filename), duplicates, ignore))
    else:
        return int(_ahk.addScript(script))

def execute(script):
    """Wrapper around ahkExec.

    Execute provided ahk commands. No lines are added to the active script.

    :returns: True if successful, else False.
    """
    result = _ahk.ahkExec(script)
    if result == 1:
        return True
    return False

def jump(label, nowait=False):
    """Wrapper around ahkLabel.
    
    GoSub/GoTo like function, branch to labeled location.
    Defaults to nowait=False, i.e. GoSub mode.
    Using nowait=True, i.e. GoTo mode, is unreliable and may fail entirely.

    :returns: True if label exists, else False.
    """
    if nowait:
        nowait = 1
    else:
        nowait = 0

    result = _ahk.ahkLabel(label, nowait)
    if result == 1:
        return True
    return False

def call(func, *args):
    """Wrapper around ahkFunction.

    Call the indicated function.

    :returns: Result of function call as a string.
    """
    params = [''] * 10
    if args:
        params = [str(arg) for arg in args]
        params += ['']*(10-len(params))
    result = _ahk.ahkFunction(func, *params)
    return ctypes.cast(int(result), ctypes.c_char_p).value

def post(func, *args):
    """Wrapper around ahkPostFunction.

    Call the indicated function but discard results.

    :returns: True if function exists, else False.
    """
    params = [''] * 10
    if args:
        params = [str(arg) for arg in args]
        params += ['']*(10-len(params))
    result = _ahk.ahkPostFunction(func, *params)
    if result == 0: # 0 if function exists, else -1
        return True
    return False

def set(name, value):
    """Wrapper around ahkassign.
    
    Assigns the string `value` to the variable `name`.

    :returns: True for success and False for failure.
    """
    if not type(value) in (str, unicode):
        value = str(value)
    result = _ahk.ahkassign(name, value)
    if result == 0: # 0 for success, else -1
        return True
    return False

def get(name, pointer=False):
    """Wrapper around ahkgetvar.

    Get the string value of a variable from ahk.
    Call with pointer=True to request a reference to the variable.

    :returns: A string representing the value, or a c_char_p.
    """
    # Workaround for ahkgetvar always returning pointers
    result = _ahk.ahkgetvar(name, 0)
    result = ctypes.cast(int(result), ctypes.c_char_p)
    if pointer:
        return result
    return result.value

def terminate(timeout=1):
    """Wrapper around ahkTerminate.

    Terminate the script, removing all hotkeys and hotstrings.
    The default timeout is 1ms, must be positive > 0.
    """
    if ready(nowait=True):
        _ahk.ahkTerminate(timeout)

def reload():
    """Wrapper around ahkReload.

    Terminates and restarts the script.
    """
    _ahk.ahkReload()

def find_func(name):
    """Wrapper around ahkFindFunc.

    .. warning::
        The following doesn't seem to work, any advice welcome.

    Get a pointer address to the named function.
    To use this you must first create a ctypes CFUNCTYPE prototype::

        proto = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)

    Then call the prototype with the address as an argument to get a function::

        func = proto(address)

    Now it can be called::

        result = func(5)

    :returns: The address of the function as an integer.
    """
    return int(_ahk.ahkFindFunc(name))

def find_label(name):
    """Wrapper around ahkFindLabel.

    Get a pointer address to a label...

    :returns: The address of the label as an integer.
    """
    return int(_ahk.ahkFindLabel(name))

def pause(pause_=True):
    """Wrapper around ahkPause.

    Pause or unpause the script.
    Calling with pause_=True pauses, pause_=False un-pauses. 
    Calling with pause_=None just reports current state without changing it.

    :returns: True if the script is paused, else False.
    """
    # Changed arg name from pause to pause_ to appease pylint:
    # Redefining name 'pause' from outer scope
    if pause_:
        pause_ = 1
    elif pause_ is None:
        pause_ = ""
    else:
        pause_ = 0
    result = _ahk.ahkPause(pause_)
    if result == 1:
        return True
    return False

def exec_line(line=None, mode=3, wait=False):
    """Wrapper around ahkExecuteLine.

    Execute starting from the provided line address.
    If line=None the address of the first line will be returned.
    Four modes of execution are available:

        0. No execution, but the next line address is returned.
        1. Run until a return statement is found.
        2. Run until the end of the current block.
        3. (default) execute only one line.

    Setting wait=True will block until end of execution.

    :returns: A line pointer address.
    """
    if not line:
        return int(_ahk.ahkExecuteLine("", 0, 0))
    elif wait:
        wait = 1
    else:
        wait = 0
    #line = hex(line) 
    return int(_ahk.ahkExecuteLine(line, mode, wait))


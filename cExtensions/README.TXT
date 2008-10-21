This directory contains various C-extensions needed by EventGhost.

- cFunctions
    This extension contains different functions needed by the program core.

- _dxJoystick
    This extension is solely needed by the Joystick plugin to access the 
    hardware through Microsoft's Direct Input API.

- greenlet
    This extension module is a spin-off of Stackless and was created by
    the codespeal project:
    http://codespeak.net/py/dist/greenlet.html
    Because the current source at codespeak doesn't work under Python 2.6,
    I have updated some files with sources from the Stackless project and
    added it to our repository.
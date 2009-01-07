This directory contains various C extensions needed by EventGhost.

- cFunctions.pyd
    This extension contains different functions needed by the program core.

- _dxJoystick.pyd
    This extension is solely needed by the Joystick plugin to access the 
    hardware through Microsoft's Direct Input API. To be able to compile it
    you need the Microsoft DirectX SDK installed.

- greenlet.pyd
    This extension module is a spin-off of Stackless and was created by
    the codespeak project:
    http://codespeak.net/py/dist/greenlet.html
    Because the current source at codespeak doesn't work under Python 2.6,
    I have updated some files with sources from the Stackless project and
    added it to our repository.
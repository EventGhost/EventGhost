Change log
----------

1.5.1 (2008-08-02)
- Back out the bugfix for deadkeys - that actually broke the ascii conversion. The py2exe bugfix stays.

1.6 (2008-07-20)
- BUGFIX: deadkeys on international keyboards work correctly.
- BUGFIX: pyHook can now be used in binaries built with py2exe (maybe this will
          work with PyInstaller too).

4/1/05
- Changed stateful key tracking to work better with SendKeys
- Possibly fixed bug where weird chars were insert when Alt+Arrow key pressed

2/23/05
- Added documentation
- Added KeyAll property to HookManager

10/11/04
- Added support for translating virtual keycodes to ASCII characters when possible
- Added support for stopping event propagation

9/13/04
- AA example was updated to work with the wx namespace
- Added support for allowing/disallowing event propagation (see example.py)
- Added a proper __init__.py to the package


Known bugs
----------
- PyInstaller can't build single-file executables using pyHook. This may be
  fixed in 1.6, but hasn't been tested.
- WM_CHAR messages are not intercepted by pyHook, even if SubscribeKeyChar() or
  SubscribeKeyAll() are used to set the callback function.


Limitations
-----------
- pyHook will not work on Win9x (no messages show up) as it uses hooks which
  are not present in Windows systems prior to NT 4.0 SP3.


Website
-------
Visit http://www.cs.unc.edu/assist and click developer resources for binaries,
documentation, and tutorials.

Bug reports and feature requests should be reported via the Sourceforge page at
https://sourceforge.net/projects/uncassist/

FAQ
===

.. contents::

Q: Isn't the installer huge for such a tool?
--------------------------------------------

A: Yes, it is. But you don't need to be afraid that the program will load all 
this into the memory. The installer includes a complete Python and wxPython 
runtime with all standard libraries, even if the program and its plugins don't 
use every aspect of them. This way everybody can use the rich set of Python 
modules for scripting and writing plugins.


Q: Can I use an IrDA dongle to control my PC with a remote?
-----------------------------------------------------------

A: No. CIR (consumer IR) that is used by your TV remote for example, is a 
complete other thing than IrDA. They use different frequencies, encodings and 
modulation. IrDA is simply not made for the purposes of CIR and vice versa. 
However there are some IrDA dongles that are advertised to work with CIR. One 
that I know of is the ACTiSYS IR200L. But other projects have found out, that 
this device won't work very reliable and therefore the EventGhost project has 
made no efforts to support it till now.


Q: How can I install EventGhost on a Windows 2000 machine?
----------------------------------------------------------

To run EventGhost you need GDI+ installed on your machine. GDI+ is a new 
graphics technology developed by Microsoft. It provides rich set of additional 
graphics features for 3rd-party developers. GDI+ is distributed as part of 
Windows XP and above, while for other operating systems an additional 
redistributable file installation is required. Since this file would increase 
the size of the EventGhost installer by one megabyte and Windows 2000 is not 
that much used any more, the needed GDIPLUS.dll is only available through an 
additional installer.

To install EventGhost on a Windows 2000 machine please follow these steps:

#. Execute the normal EventGhost installer, but don't let it run EventGhost 
   on the finish page (it would crash).
#. Download `this add-on installer 
   <http://www.eventghost.org/downloads/EventGhost_GDIPLUS_Installer.exe>`_ 
   and let it install gdiplus.dll into your EventGhost program directory. 

Now you should be able to run EventGhost. 
#
# EventGhost.pyw
#
# Copyright (C) 2005 Lars-Peter Voss
#
# This file is part of EventGhost.
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

#!python.exe

# start the main program
import sys
import imp
from os.path import dirname, abspath

if hasattr(sys, "frozen"):
    path = dirname(sys.executable)
else:
    path = abspath(dirname(sys.argv[0])) 
    
imp.load_source("Main", path + "/eg/Main.py")

print "should never come here"
# these imports are only here, to force py2exe to include them

# 3. Python Runtime Services 

import sys          # Access system-specific parameters and functions. 
import gc           # Interface to the cycle-detecting garbage collector. 
import weakref      # Support for weak references and weak dictionaries. 
#import fpectl       # Provide control for floating point exception handling. 
import atexit       # Register and execute cleanup functions. 
import types        # Names for built-in types. 
import UserDict     # Class wrapper for dictionary objects. 
import UserList     # Class wrapper for list objects. 
import UserString   # Class wrapper for string objects. 
import operator     # All Python's standard operators as built-in functions. 
import inspect      # Extract information and source code from live objects. 
import traceback    # Print or retrieve a stack traceback. 
import linecache    # This module provides random access to individual lines from text files. 
import pickle       # Convert Python objects to streams of bytes and back. 
import cPickle      # Faster version of pickle, but not subclassable. 
import copy_reg     # Register pickle support functions. 
import shelve       # Python object persistence. 
import copy         # Shallow and deep copy operations. 
import marshal      # Convert Python objects to streams of bytes and back (with different constraints). 
import warnings     # Issue warning messages and control their disposition. 
import imp          # Access the implementation of the import statement. 
import zipimport    # support for importing Python modules from ZIP archives. 
import pkgutil      # Utilities to support extension of packages. 
import modulefinder  # Find modules used by a script. 
import code         # Base classes for interactive Python interpreters. 
import codeop       # Compile (possibly incomplete) Python code. 
import pprint       # Data pretty printer. 
import repr         # Alternate repr() implementation with size limits. 
import new          # Interface to the creation of runtime implementation objects. 
import site         # A standard way to reference site-specific modules. 
import user         # A standard way to reference user-specific modules. 
import __builtin__  # The module that provides the built-in namespace. 
import __main__     # The environment where the top-level script is run. 
import __future__   # Future statement definitions 


# 4. String Services 

import string       # Common string operations. 
import re           # Regular expression search and match operations with a Perl-style expression syntax. 
import struct       # Interpret strings as packed binary data. 
import difflib      # Helpers for computing differences between objects. 
import fpformat     # General floating point formatting functions. 
import StringIO     # Read and write strings as if they were files. 
import cStringIO    # Faster version of StringIO, but not subclassable. 
import textwrap     # Text wrapping and filling 
import codecs       # Encode and decode data and streams. 
import encodings.idna  # Internationalized Domain Names implementation 
import unicodedata  # Access the Unicode Database. 
import stringprep   # String preparation, as per RFC 3453 


# 5. Miscellaneous Services 

import pydoc        # Documentation generator and online help system. 
import doctest      # A framework for verifying interactive Python examples. 
import unittest     # Unit testing framework for Python. 
import test         # Regression tests package containing the testing suite for Python. 
import test.test_support  # Support for Python regression tests. 
import decimal      # Implementation of the General Decimal Arithmetic Specification. 
import math         # Mathematical functions (sin() etc.). 
import cmath        # Mathematical functions for complex numbers. 
import random       # Generate pseudo-random numbers with various common distributions. 
#import whrandom     # Floating point pseudo-random number generator. 
import bisect       # Array bisection algorithms for binary searching. 
import collections  # High-performance datatypes 
import heapq        # Heap queue algorithm (a.k.a. priority queue). 
import array        # Efficient arrays of uniformly typed numeric values. 
import sets         # Implementation of sets of unique elements. 
import itertools    # Functions creating iterators for efficient looping. 
import ConfigParser # Configuration file parser. 
import fileinput    # Perl-like iteration over lines from multiple input streams, with ``save in place'' capability. 
import calendar     # Functions for working with calendars, including some emulation of the Unix cal program. 
import cmd          # Build line-oriented command interpreters. 
import shlex        # Simple lexical analysis for Unix shell-like languages. 


# 6. Generic Operating System Services 

import os  # Miscellaneous operating system interfaces. 
import os.path  # Common pathname manipulations. 
import dircache  # Return directory listing, with cache mechanism. 
import stat  # Utilities for interpreting the results of os.stat(), os.lstat() and os.fstat(). 
#import statcache  # Stat files, and remember results. 
import statvfs  # Constants for interpreting the result of os.statvfs(). 
import filecmp  # Compare files efficiently. 
import subprocess  # Subprocess management. 
import popen2  # Subprocesses with accessible standard I/O streams. 
import datetime  # Basic date and time types. 
import time  # Time access and conversions. 
import sched  # General purpose event scheduler. 
import mutex  # Lock and queue for mutual exclusion. 
import getpass  # Portable reading of passwords and retrieval of the userid. 
# no curses on windows
#import curses  # An interface to the curses library, providing portable terminal handling.
#import curses.textpad  # Emacs-like input editing in a curses window. 
#import curses.wrapper  # Terminal configuration wrapper for curses programs. 
#import curses.ascii  # Constants and set-membership functions for ASCII characters. 
#import curses.panel  # A panel stack extension that adds depth to curses windows. 
import getopt  # Portable parser for command line options; support both short and long option names.
import optparse  # More convenient, flexible, and powerful command-line parsing library. 
import tempfile  # Generate temporary files and directories. 
import errno  # Standard errno system symbols. 
import glob  # Unix shell style pathname pattern expansion. 
import fnmatch  # Unix shell style filename pattern matching. 
import shutil  # High-level file operations, including copying. 
import locale  # Internationalization services. 
import gettext  # Multilingual internationalization services. 
import logging  # Logging module for Python based on PEP 282. 
import platform  # Retrieves as much platform identifying data as possible. 


# 7. Optional Operating System Services

import signal  # Set handlers for asynchronous events. 
import socket  # Low-level networking interface. 
import select  # Wait for I/O completion on multiple streams. 
import thread  # Create multiple threads of control within one interpreter. 
import threading  # Higher-level threading interface. 
import dummy_thread  # Drop-in replacement for the thread module. 
import dummy_threading  # Drop-in replacement for the threading module. 
import Queue  # A synchronized queue class. 
import mmap  # Interface to memory-mapped files for Unix and Windows. 
import anydbm  # Generic interface to DBM-style database modules. 
import dbhash  # DBM-style interface to the BSD database library. 
import whichdb  # Guess which DBM-style module created a given database. 
import bsddb  # Interface to Berkeley DB database library 
import dumbdbm  # Portable implementation of the simple DBM interface. 
import zlib  # Low-level interface to compression and decompression routines compatible with gzip. 
import gzip  # Interfaces for gzip compression and decompression using file objects. 
import bz2  # Interface to compression and decompression routines compatible with bzip2. 
import zipfile  # Read and write ZIP-format archive files. 
import tarfile  # Read and write tar-format archive files. 
#import readline  # GNU readline support for Python. 
import rlcompleter  # Python identifier completion for the GNU readline library. 


# 8. Unix Specific Services
# not needed


# 9. The Python Debugger 

import pdb


# 10. The Python Profiler

import profile
import pstats
import timeit


#11. Internet Protocols and Support 

import webbrowser   # Easy-to-use controller for Web browsers. 
import cgi          # Common Gateway Interface support, used to interpret forms in server-side scripts. 
import cgitb        # Configurable traceback handler for CGI scripts. 
import urllib       # Open an arbitrary network resource by URL (requires sockets). 
import urllib2      # An extensible library for opening URLs using a variety of protocols 
import httplib      # HTTP and HTTPS protocol client (requires sockets). 
import ftplib       # FTP protocol client (requires sockets). 
import gopherlib    # Gopher protocol client (requires sockets). 
import poplib       # POP3 protocol client (requires sockets). 
import imaplib      # IMAP4 protocol client (requires sockets). 
import nntplib      # NNTP protocol client (requires sockets). 
import smtplib      # SMTP protocol client (requires sockets). 
import smtpd        # Implement a flexible SMTP server 
import telnetlib    # Telnet client class. 
import urlparse     # Parse URLs into components. 
import SocketServer # A framework for network servers. 
import BaseHTTPServer  # Basic HTTP server (base class for SimpleHTTPServer and CGIHTTPServer). 
import SimpleHTTPServer  # This module provides a basic request handler for HTTP servers. 
import CGIHTTPServer  # This module provides a request handler for HTTP servers which can run CGI scripts. 
import cookielib    # Cookie handling for HTTP clients 
import Cookie       # Support for HTTP state management (cookies). 
import xmlrpclib    # XML-RPC client access. 
import SimpleXMLRPCServer  # Basic XML-RPC server implementation. 
import DocXMLRPCServer  # Self-documenting XML-RPC server implementation. 
import asyncore     # A base class for developing asynchronous socket handling services. 
import asynchat     # Support for asynchronous command/response protocols. 


# 12. Internet Data Handling 

import formatter    # Generic output formatter and device interface. 
import email        # Package supporting the parsing, manipulating, and generating email messages, including MIME documents. 
import email.Message  # The base class representing email messages. 
import email.Parser # Parse flat text email messages to produce a message object structure. 
import email.Generator  # Generate flat text email messages from a message structure. 
import email.Header # Representing non-ASCII headers 
import email.Charset  # Character Sets 
import email.Encoders  # Encoders for email message payloads. 
import email.Errors  # The exception classes used by the email package. 
import email.Utils  # Miscellaneous email package utilities. 
import email.Iterators  # Iterate over a message object tree. 
import mailcap  # Mailcap file handling. 
import mailbox  # Read various mailbox formats. 
import mhlib  # Manipulate MH mailboxes from Python. 
import mimetools  # Tools for parsing MIME-style message bodies. 
import mimetypes  # Mapping of filename extensions to MIME types. 
import MimeWriter  # Generic MIME file writer. 
import mimify  # Mimification and unmimification of mail messages. 
import multifile  # Support for reading files which contain distinct parts, such as some MIME data. 
import rfc822  # Parse RFC 2822 style mail messages. 
import base64  # RFC 3548: Base16, Base32, Base64 Data Encodings 
import binascii  # Tools for converting between binary and various ASCII-encoded binary representations. 
import binhex  # Encode and decode files in binhex4 format. 
import quopri  # Encode and decode files using the MIME quoted-printable encoding. 
import uu  # Encode and decode files in uuencode format. 
import xdrlib  # Encoders and decoders for the External Data Representation (XDR). 
import netrc  # Loading of .netrc files. 
import robotparser  # Loads a robots.txt file and answers questions about fetchability of other URLs. 
import csv  # Write and read tabular data to and from delimited files. 


# 13. Structured Markup Processing Tools 

import HTMLParser  # A simple parser that can handle HTML and XHTML. 
import sgmllib  # Only as much of an SGML parser as needed to parse HTML. 
import htmllib  # A parser for HTML documents. 
import htmlentitydefs  # Definitions of HTML general entities. 
import xml.parsers.expat  # An interface to the Expat non-validating XML parser. 
import xml.dom  # Document Object Model API for Python. 
import xml.dom.minidom  # Lightweight Document Object Model (DOM) implementation. 
import xml.dom.pulldom  # Support for building partial DOM trees from SAX events. 
import xml.sax  # Package containing SAX2 base classes and convenience functions. 
import xml.sax.handler  # Base classes for SAX event handlers. 
import xml.sax.saxutils  # Convenience functions and classes for use with SAX. 
import xml.sax.xmlreader  # Interface which SAX-compliant XML parsers must implement. 
import xmllib  # A parser for XML documents. 


# 14. Multimedia Services 

import audioop  # Manipulate raw audio data. 
import imageop  # Manipulate raw image data. 
import aifc  # Read and write audio files in AIFF or AIFC format. 
import sunau  # Provide an interface to the Sun AU sound format. 
import wave  # Provide an interface to the WAV sound format. 
import chunk  # Module to read IFF chunks. 
import colorsys  # Conversion functions between RGB and other color systems. 
import rgbimg  # Read and write image files in ``SGI RGB'' format (the module is not SGI specific though!). 
import imghdr  # Determine the type of image contained in a file or byte stream. 
import sndhdr  # Determine type of a sound file. 
#import ossaudiodev  # Access to OSS-compatible audio devices. 


# 15. Cryptographic Services 

import hmac  # Keyed-Hashing for Message Authentication (HMAC) implementation for Python. 
import md5  # RSA's MD5 message digest algorithm. 
import sha  # NIST's secure hash algorithm, SHA. 


# 16. Graphical User Interfaces with Tk
# not included


# 17. Restricted Execution 
# disabled in Python 2.3


# 18. Python Language Services 

import parser  # Access parse trees for Python source code. 
import symbol  # Constants representing internal nodes of the parse tree. 
import token  # Constants representing terminal nodes of the parse tree. 
import keyword  # Test whether a string is a keyword in Python. 
import tokenize  # Lexical scanner for Python source code. 
import tabnanny  # Tool for detecting white space related problems in Python source files in a directory tree. 
import pyclbr  # Supports information extraction for a Python class browser. 
import py_compile  # Compile Python source files to byte-code files. 
import compileall  # Tools for byte-compiling all Python source files in a directory tree. 
import dis  # Disassembler for Python byte code. 
import pickletools  # Contains extensive comments about the pickle protocols and pickle-machine opcodes, as well as some useful functions. 
import distutils  # Support for building and installing Python modules into an existing Python installation. 


# 19. Python compiler package 

import compiler    
import compiler.ast    
import compiler.visitor    


# 20. SGI IRIX Specific Services 
# not needed


# 21. SunOS Specific Services 
# not needed


# 22. MS Windows Specific Services 

import msvcrt  # Miscellaneous useful routines from the MS VC++ runtime. 
import _winreg  # Routines and objects for manipulating the Windows registry. 
import winsound  # Access to the sound-playing machinery for Windows. 


import pythoncom
import pywintypes

import win32api
import win32clipboard
import win32console
import win32crypt
import win32con
import win32event
import win32evtlog
import win32file
import win32gui
import win32help
import win32inet
import win32job
import win32lz
import win32net
import win32pdh
import win32pipe
import win32print
import win32process
import win32security
import win32service
import win32ts
import win32ui
import win32uiole
import win32wnet
import winxpgui

import win32com
import win32com.server
import win32com.server.factory
import win32com.server.util
import win32com.server.register
import win32com.client
import win32com
import win32com.shell
import win32com.shell.shellcon
from win32com.shell.shellcon import *
from win32com.shell import shell
from win32com.shell import shellcon


import ctypes
import ctypes.util
#import ctypes.decorators
import ctypes.wintypes

# PIL
import Image
import ImageDraw
import PngImagePlugin
import JpegImagePlugin
import BmpImagePlugin
import GifImagePlugin

import wx 
import wx.aui
import wx.activex
import wx.animate
import wx.calendar
import wx.combo
import wx.gizmos
import wx.glcanvas
import wx.grid
import wx.html
import wx.media
import wx.stc
import wx.webkit
import wx.wizard
import wx.xrc
import wx.build
import wx.build.build_options
import wx.build.config
import wx.lib
import wx.lib.activexwrapper
import wx.lib.anchors
import wx.lib.buttons
import wx.lib.calendar
import wx.lib.CDate
import wx.lib.ClickableHtmlWindow
import wx.lib.colourdb
import wx.lib.colourselect
import wx.lib.dialogs
import wx.lib.docview
import wx.lib.evtmgr
import wx.lib.expando
import wx.lib.fancytext
import wx.lib.filebrowsebutton
import wx.lib.flashwin
import wx.lib.floatbar
import wx.lib.foldmenu
import wx.lib.foldpanelbar
import wx.lib.gestures
import wx.lib.gridmovers
import wx.lib.grids
import wx.lib.hyperlink
import wx.lib.iewin
import wx.lib.imagebrowser
import wx.lib.imageutils
import wx.lib.infoframe
import wx.lib.intctrl
import wx.lib.layoutf
import wx.lib.multisash
import wx.lib.mvctree
import wx.lib.newevent
import wx.lib.pdfwin
#import wx.lib.plot
import wx.lib.popupctl
import wx.lib.printout
import wx.lib.pubsub
import wx.lib.pydocview
import wx.lib.pyshell
import wx.lib.rcsizer
import wx.lib.rightalign
import wx.lib.rpcMixin
import wx.lib.scrolledpanel
import wx.lib.sheet
import wx.lib.shell
import wx.lib.splashscreen
import wx.lib.splitter
import wx.lib.statbmp
import wx.lib.stattext
import wx.lib.throbber
import wx.lib.ticker
import wx.lib.ticker_xrc
import wx.lib.vtk
import wx.lib.wxPlotCanvas
import wx.lib.wxpTag
import wx.lib.analogclock
import wx.lib.analogclock.analogclock
import wx.lib.analogclock.helpers
import wx.lib.analogclock.setup
import wx.lib.analogclock.styles
import wx.lib.analogclock.lib_setup
import wx.lib.analogclock.lib_setup.buttontreectrlpanel
import wx.lib.analogclock.lib_setup.colourselect
import wx.lib.analogclock.lib_setup.fontselect
import wx.lib.colourchooser
import wx.lib.colourchooser.canvas
import wx.lib.colourchooser.intl
import wx.lib.colourchooser.pycolourbox
import wx.lib.colourchooser.pycolourchooser
import wx.lib.colourchooser.pycolourslider
import wx.lib.colourchooser.pypalette
import wx.lib.editor
import wx.lib.editor.editor
import wx.lib.editor.images
import wx.lib.editor.selection
import wx.lib.floatcanvas
import wx.lib.floatcanvas.FloatCanvas
import wx.lib.floatcanvas.NavCanvas
import wx.lib.floatcanvas.Resources
import wx.lib.masked
import wx.lib.masked.combobox
import wx.lib.masked.ctrl
import wx.lib.masked.ipaddrctrl
import wx.lib.masked.maskededit
import wx.lib.masked.numctrl
import wx.lib.masked.textctrl
import wx.lib.masked.timectrl
import wx.lib.mixins
import wx.lib.mixins.grid
import wx.lib.mixins.imagelist
import wx.lib.mixins.listctrl
import wx.lib.mixins.rubberband
import wx.lib.ogl
import wx.locale

import wx.py
import wx.py.buffer
import wx.py.crust
import wx.py.dispatcher
import wx.py.document
import wx.py.editor
import wx.py.editwindow
import wx.py.filling
import wx.py.frame
import wx.py.images
import wx.py.interpreter
import wx.py.introspect
import wx.py.pseudo
import wx.py.PyAlaCarte
import wx.py.PyAlaMode
import wx.py.PyAlaModeTest
import wx.py.PyCrust
import wx.py.PyFilling
import wx.py.PyShell
import wx.py.PyWrap
import wx.py.shell
import wx.py.version

import wx.tools
import wx.tools.dbg
import wx.tools.genaxmodule
import wx.tools.helpviewer
import wx.tools.img2img
import wx.tools.img2png
import wx.tools.img2py
import wx.tools.img2xpm
import wx.tools.pywxrc
import wx.tools.XRCed
import wx.tools.XRCed.encode_bitmaps
import wx.tools.XRCed.globals
import wx.tools.XRCed.images
import wx.tools.XRCed.panel
import wx.tools.XRCed.params
import wx.tools.XRCed.tools
import wx.tools.XRCed.tree
import wx.tools.XRCed.undo
import wx.tools.XRCed.xrced
import wx.tools.XRCed.xxx
#import wx.tools.XRCed.src-images


from elementtree import ElementTree
import cElementTree as ElementTree2

import xml.etree.ElementTree
import xml.etree.cElementTree

import pyHook



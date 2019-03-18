"""OO wrappers around the AutoHotKey library.

This package provides both direct access to wrapped versions of the functions
provided by the ahkdll, and also object wrappers around common operations.
"""
from ahk import *
from script import Function, Script
from control import Control

__version__ = "0.2.1"


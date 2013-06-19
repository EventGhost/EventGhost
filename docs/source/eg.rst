======================================
The one and all ``eg`` object
======================================
.. contents::
    
.. module:: eg
.. currentmodule:: eg


Objects
========

.. attribute:: event

    The :class:`eg.EventGhostEvent` instance, that is currently
    been processed.
    
.. attribute:: globals

    :class:`eg.Bunch` instance, that holds all global variables used by
    PythonCommand actions. PythonScripts (and all other code) can access
    these globals through :obj:`eg.globals`.

.. attribute:: scheduler

    Instance of the single :class:`eg.Scheduler` class.
    


Classes
=========

class :class:`eg.PluginBase`

class :class:`eg.ActionBase`

class :class:`eg.SerialThread`

class :class:`eg.ThreadWorker`

.. autoclass:: eg.Bunch

.. autoclass:: eg.WindowMatcher

.. autoclass:: eg.EventGhostEvent

.. autoclass:: eg.ConfigPanel
    :members:

Functions
==========

.. autofunction:: eg.Exit

.. autofunction:: eg.StopMacro

.. autofunction:: eg.TriggerEvent

.. autofunction:: eg.RegisterPlugin

.. autofunction:: eg.PrintError


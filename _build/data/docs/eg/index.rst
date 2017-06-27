
=================
The ``eg`` module
=================
.. contents::

.. module:: eg
.. currentmodule:: eg

Everything special that is needed from EventGhost for scripting and writing
plugins is stuffed into the :mod:`eg` module. It includes many functions,
variables, classes and objects. You could actually say :mod:`eg` is EventGhost
itself.

Objects
=======

.. attribute:: event

    The :class:`eg.EventGhostEvent` instance that is currently
    being processed.

.. attribute:: globals

    Namespace that holds all global variables used by
    PythonCommand actions. PythonScripts (and all other code) can access
    these globals through :obj:`eg.globals`.

.. attribute:: scheduler

    Instance of the single :class:`eg.Scheduler` class.


Classes
=======

.. include:: classes.txt


wxPython Additions
==================

.. include:: gui_classes.txt


Functions
=========

.. autofunction:: eg.Exit
    :noindex:

.. autofunction:: eg.StopMacro
    :noindex:

.. autofunction:: eg.TriggerEvent
    :noindex:

.. autofunction:: eg.RegisterPlugin

.. autofunction:: eg.PrintError

"""
This module is not directly used by EventGhost. It only exists to help
pylint and other tools to read the sources properly, as EventGhost is using
a lazy import pattern.
"""
# pylint: disable-msg=W0611,W0614,C0103
from Utils import * #pylint: disable-msg=W0401
from Classes.AboutDialog import AboutDialog
from Classes.ActionBase import ActionBase
from Classes.ActionGroup import ActionGroup
from Classes.ActionItem import ActionItem
from Classes.ActionThread import ActionThread
from Classes.ActionWithStringParameter import ActionWithStringParameter
from Classes.AddActionDialog import AddActionDialog
from Classes.AddActionGroupDialog import AddActionGroupDialog
from Classes.AddEventDialog import AddEventDialog
from Classes.AddPluginDialog import AddPluginDialog
from Classes.AnimatedWindow import AnimatedWindow
from Classes.App import App
from Classes.AutostartItem import AutostartItem
from Classes.BoxedGroup import BoxedGroup
from Classes.ButtonRow import ButtonRow
from Classes.CheckBoxGrid import CheckBoxGrid
from Classes.CheckUpdate import CheckUpdate
from Classes.Choice import Choice
from Classes.Colour import Colour
from Classes.ColourSelectButton import ColourSelectButton
from Classes.Config import Config
from Classes.ConfigPanel import ConfigPanel
from Classes.ContainerItem import ContainerItem
from Classes.ControlProviderMixin import ControlProviderMixin
from Classes.Dialog import Dialog
from Classes.DigitOnlyValidator import DigitOnlyValidator
from Classes.DirBrowseButton import DirBrowseButton
from Classes.DisplayChoice import DisplayChoice
from Classes.Document import Document
from Classes.EventGhostEvent import EventGhostEvent
from Classes.EventItem import EventItem
from Classes.EventRemapDialog import EventRemapDialog
from Classes.EventThread import EventThread
from Classes.Exceptions import Exceptions
from Classes.ExceptionsProvider import ExceptionsProvider
from Classes.ExportDialog import ExportDialog
from Classes.FileBrowseButton import FileBrowseButton
from Classes.FindDialog import FindDialog
from Classes.FolderItem import FolderItem
from Classes.FolderPath import FolderPath
from Classes.FontSelectButton import FontSelectButton
from Classes.HeaderBox import HeaderBox
from Classes.HtmlDialog import HtmlDialog
from Classes.HtmlWindow import HtmlWindow
from Classes.HyperLinkCtrl import HyperLinkCtrl
from Classes.ImagePicker import ImagePicker
from Classes.IrDecoder import IrDecoder
from Classes.LanguageEditor import LanguageEditor
from Classes.License import License
from Classes.Log import Log
from Classes.MacroItem import MacroItem
from Classes.MacroSelectButton import MacroSelectButton
from Classes.Menu import Menu
from Classes.MenuBar import MenuBar
from Classes.MessageReceiver import MessageReceiver
from Classes.NamespaceTree import NamespaceTree
from Classes.NetworkSend import NetworkSend
from Classes.NotificationHandler import NotificationHandler
from Classes.OptionsDialog import OptionsDialog
from Classes.Panel import Panel
from Classes.PluginBase import PluginBase
from Classes.PluginInfo import PluginInfo
from Classes.PluginItem import PluginItem
from Classes.PluginManager import PluginManager
from Classes.PluginMetaClass import PluginMetaClass
from Classes.PythonEditorCtrl import PythonEditorCtrl
from Classes.RadioBox import RadioBox
from Classes.RadioButtonGrid import RadioButtonGrid
from Classes.RawReceiverPlugin import RawReceiverPlugin
from Classes.RootItem import RootItem
from Classes.Scheduler import Scheduler
from Classes.SerialPort import SerialPort
from Classes.SerialPortChoice import SerialPortChoice
from Classes.SerialThread import SerialThread
from Classes.Shortcut import Shortcut
from Classes.SimpleInputDialog import SimpleInputDialog
from Classes.SizeGrip import SizeGrip
from Classes.Slider import Slider
from Classes.SoundMixerTree import SoundMixerTree
from Classes.SpinIntCtrl import SpinIntCtrl
from Classes.SpinNumCtrl import SpinNumCtrl
from Classes.StaticTextBox import StaticTextBox
from Classes.TaskBarIcon import TaskBarIcon
from Classes.Text import Text
from Classes.ThreadWorker import ThreadWorker
from Classes.ToolBar import ToolBar
from Classes.TranslatableStrings import TranslatableStrings
from Classes.Translation import Translation
from Classes.TreeItem import TreeItem
from Classes.TreeItemBrowseCtrl import TreeItemBrowseCtrl
from Classes.TreeItemBrowseDialog import TreeItemBrowseDialog
from Classes.TreeLink import TreeLink
from Classes.TreePosition import TreePosition
from Classes.Version import Version
from Classes.WindowDragFinder import WindowDragFinder
from Classes.WindowList import WindowList
from Classes.WindowMatcher import WindowMatcher
from Classes.WindowTree import WindowTree
UndoHandler = Bunch()
from Classes.UndoHandler.AddActionGroup import AddActionGroup as _tmp
UndoHandler.AddActionGroup = _tmp
from Classes.UndoHandler.Clear import Clear as _tmp
UndoHandler.Clear = _tmp
from Classes.UndoHandler.Configure import Configure as _tmp
UndoHandler.Configure = _tmp
from Classes.UndoHandler.Cut import Cut as _tmp
UndoHandler.Cut = _tmp
from Classes.UndoHandler.MoveTo import MoveTo as _tmp
UndoHandler.MoveTo = _tmp
from Classes.UndoHandler.NewAction import NewAction as _tmp
UndoHandler.NewAction = _tmp
from Classes.UndoHandler.NewEvent import NewEvent as _tmp
UndoHandler.NewEvent = _tmp
from Classes.UndoHandler.NewFolder import NewFolder as _tmp
UndoHandler.NewFolder = _tmp
from Classes.UndoHandler.NewItem import NewItem as _tmp
UndoHandler.NewItem = _tmp
from Classes.UndoHandler.NewMacro import NewMacro as _tmp
UndoHandler.NewMacro = _tmp
from Classes.UndoHandler.NewPlugin import NewPlugin as _tmp
UndoHandler.NewPlugin = _tmp
from Classes.UndoHandler.Paste import Paste as _tmp
UndoHandler.Paste = _tmp
from Classes.UndoHandler.Rename import Rename as _tmp
UndoHandler.Rename = _tmp
from Classes.UndoHandler.ToggleEnable import ToggleEnable as _tmp
UndoHandler.ToggleEnable = _tmp

document = Document()
taskBarIcon = TaskBarIcon()

del _tmp

def RegisterPlugin(**dummyKwArgs): 
    pass

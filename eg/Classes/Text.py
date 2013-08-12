# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from eg.Utils import SetDefault
import os
import sys


class Default:
    class General:
        configTree = "Configuration Tree"
        deleteQuestion = "Are you sure you want to delete this item?"
        deleteManyQuestion = (
            "This element has %s subelements.\n"
            "Are you sure you want to delete them all?"
        )
        deletePlugin = (
            "This plugin is used by actions in your configuration.\n"
            "You cannot remove it before all actions that are using this "
            "plugin have been removed."
        )
        deleteLinkedItems = (
            "At least one item outside your selection refers to an "
            "item inside your selection. If you continue to delete "
            "this selection, the referring item won't properly work "
            "anymore.\n\n"
            "Are you sure you want to delete the selection?"
        )
        ok = "OK"
        cancel = "Cancel"
        apply = "&Apply"
        yes = "&Yes"
        no = "&No"
        help = "&Help"
        choose = "Choose"
        browse = "Browse..."
        test = "&Test"
        pluginLabel = "Plugin: %s"
        autostartItem = "Autostart"
        unnamedFolder = "<unnamed folder>"
        unnamedMacro = "<unnamed macro>"
        unnamedEvent = "<unnamed event>"
        unnamedFile = "<unnamed file>"
    #    moreTag = "more..."
        supportSentence = "Support for this plugin can be found"
        supportLink = "here"
        settingsPluginCaption = "Plugin Item Settings"
        settingsActionCaption = "Action Item Settings"
        settingsEventCaption = "Event Item Settings"
        noOptionsAction = "This action has no options to configure."
        noOptionsPlugin = "This plugin has no options to configure."
        monitorsLabel = "Identified monitors:"
        monitorsHeader = (
            "Monitor nr.",
            "X coordinate",
            "Y coordinate",
            "Width",
            "Height",
        )

        smartSpinMenu = (
            'Change control to "Spin Num"',
            'Change control to "Text" with {eg.result}',
            'Change control to "Text" with {eg.event.payload}',
            'Change control to (empty) "Text"'
        )
        smartSpinTooltip = "Use the right mouse button\nto get the context menu !"


    class Error:
        FileNotFound = "File \"%s\" couldn't be found."
        InAction = 'Error in Action: "%s"'
        pluginNotActivated = 'Plugin "%s" is not activated'
        pluginStartError = "Error starting plugin: %s"
        pluginLoadError = "Error while loading plugin-file %s."
        configureError = "Error while configuring: %s"

    class Plugin:
        pass


    class MainFrame:
        onlyLogAssigned = "&Log only assigned and activated events"
        onlyLogAssignedToolTip = (
            "If checked, the log will only show events, that would actually\n"
            "execute in the current configuration. So you should *not* check\n"
            "this, while you want to assign new events."
        )
        scrollLog = "Scroll log"
        class TaskBarMenu:
            Show = "Show EventGhost"
            Hide = "Hide EventGhost"
            Exit = "Exit"

        class Menu:
            FileMenu = "&File"
            Apply = "&Apply Changes"
            New = "&New"
            Open = "&Open..."
            Save = "&Save"
            SaveAs = "Save &As..."
            Export = "Export..."
            Import = "Import..."
            Close = "&Close"
            Options = "&Options..."
            Exit = "E&xit"

            EditMenu = "&Edit"
            Undo = "&Undo"
            Redo = "&Redo"
            Cut = "Cu&t"
            Copy = "&Copy"
            Python = "Copy As Python"
            Paste = "&Paste"
            Delete = "&Delete"
            SelectAll = "Select &All"
            Find = "&Find..."
            FindNext = "Find &Next"

            ViewMenu = "View"
            HideShowToolbar = "Toolbar"
            CollapseAll = "&Collapse All"
            ExpandAll = "&Expand All"
            ExpandOnEvents = "Select Items on Execution"
            LogMacros = "Log Macros"
            LogActions = "Log Actions"
            LogTime = "Log Times"
            ClearLog = "Clear Log"
            IndentLog = "Indent Log"

            ConfigurationMenu = "&Configuration"
            AddPlugin = "Add Plugin..."
            AddFolder = "Add Folder"
            AddMacro = "Add Macro..."
            AddEvent = "Add Event..."
            AddAction = "Add Action..."
            Configure = "Configure Item"
            Rename = "Rename Item"
            Disabled = "Disable Item"
            Execute = "Execute Item"

            HelpMenu = "&Help"
            HelpContents = "&Help Contents"
            About = "&About EventGhost..."
            WebHomepage = "Home &Page"
            WebForum = "Support &Forums"
            WebWiki = "&Wiki"
            CheckUpdate = "Check for Update..."
            PythonShell = "Python Shell"
            Reset = "Reset"

        class SaveChanges:
            mesg = (
                "The file was altered.\n\n"
                "Do you want to save the changes?\n"
            )
            saveButton = "&Save"
            dontSaveButton = "Do&n't Save"

        class Logger:
            caption = "Log"
            welcomeText = "---> Welcome to EventGhost <---"

        class Tree:
            caption = "Configuration"

        class Messages:
            cantAddEvent = (
                "You can't add an event item here.\n\n"
                "Please select a macro item where "
                "you would like the event item to be added to."
            )
            cantAddAction = (
                "You can't add an action item here.\n\n"
                "Please select a macro item or a location inside a macro "
                "item where you would like the event item be to added to."
            )
            cantDisable = (
                "The root item and the autostart item can't be disabled."
            )
            cantRename = (
                "Only folders, macros and actions can be renamed."
            )
            cantExecute = (
                "The root item, folder items and event items can't be "
                "executed."
            )
            cantConfigure = (
                "You can't configure this item.\n\n"
                "Only action, event and plugin items are configurable."
            )


def Text(language):
    class Translation(Default):
        pass
    languagePath = os.path.join(eg.languagesDir, "%s.py" % language)
    try:
        eg.ExecFile(languagePath, {}, Translation.__dict__)
    except IOError:
        pass
    SetDefault(Translation, Default)
    return Translation


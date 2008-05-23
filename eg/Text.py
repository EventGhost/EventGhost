# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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

class Text:
    class General:
        configTree = "Configuration Tree"
        deleteQuestion = "Are you sure you want to delete this item?"
        deleteManyQuestion = (
            "This element has %s subelements.\n"
            "Are you sure you want to delete them all?"
        )
        deletePlugin = (
            "This plugin is used by actions in your configuration.\n"
            "You cannot remove it before all actions that are using this plugin "
            "have been removed."
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
        apply = "Apply"
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
        moreTag = "more..."
        noOptionsAction = "This action has no options to configure."
        noOptionsPlugin = "This plugin has no options to configure."

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
            Paste = "&Paste"
            Delete = "&Delete"
            SelectAll = "Select &All"
            AddPlugin = "Add Plugin"
            AddFolder = "Add Folder"
            AddMacro = "Add Macro"
            AddEvent = "Add Event"
            AddAction = "Add Action"
            Configure = "Configure Item"
            Rename = "Rename Item"
            Disabled = "Disable Item"
            Execute = "Execute Item"
            Find = "&Find..."
            FindNext = "Find &Next"

            ViewMenu = "View"
            HideShowToolbar = "Toolbar"
            CollapseAll = "&Collapse All"
            ExpandAll = "&Expand All"
            ExpandOnEvents = "Autom. highlight on event"
            ExpandTillMacro = "Autom. expand only till macro"
            LogMacros = "Log Macros"
            LogActions = "Log Actions"
            LogTime = "Log Times"
            ClearLog = "Clear Log"
            
            ConfigurationMenu = "&Configuration"
            
            HelpMenu = "&Help"
            About = "&About EventGhost..."
            WebHomepage = "Home Page"
            WebForum = "Support Forums"
            WebWiki = "Wiki"
            CheckUpdate = "Check for updates now..."
            Reset = "Reset"
            
        class SaveChanges:
            title = "Save changes?"
            mesg = "The file was altered.\n\nDo you want to save the changes?\n"

        class Logger:
            caption = "Log"
            timeHeader = "Time"
            descriptionHeader = "Description"
            welcomeText = "---> Welcome to EventGhost <---"
            
        class Tree:
            caption = "Configuration"


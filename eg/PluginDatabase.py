# This file is part of EventGhost.
# Copyright (C) 2007 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2007-05-30 08:12:13 +0200 (Mi, 30 Mai 2007) $
# $LastChangedRevision: 133 $
# $LastChangedBy: bitmonster $

from __future__ import with_statement
import eg
import os
import cPickle as pickle
from os import stat
from os.path import isdir, join, exists

from PluginTools import ImportPlugin

        
        
class PluginFileInfo:
    # some informational fields
    name = "unknown name"
    author = "unknown author"
    version = "unknow version"
    
    # kind gives a hint in which group the plugin should be shown in
    # the AddPluginDialog
    kind = "other"

    def __init__(self, pluginDir):
        self.dirname = pluginDir
        
        # first try to find the deprecated "__info__.py" file
        infoPyPath = join(eg.PLUGIN_DIR, pluginDir, "__info__.py")
        if exists(infoPyPath):
            infoDict = {}
            try:
                execfile(infoPyPath, infoDict)
            except:
                eg.PrintError(eg.text.Error.pluginInfoPyError % pluginDir)
                eg.PrintTraceback()
            else:
                del infoDict["__builtins__"]
                try:
                    self.RegisterPlugin(**infoDict)
                except PluginFileInfo.RegisterPluginException:
                    return
                
        old = eg.RegisterPlugin
        eg.RegisterPlugin = self.RegisterPlugin
        try:
            try:
                module = ImportPlugin(self.dirname)
            finally:
                eg.RegisterPlugin = old
        # It is expected that the loading will raise RegisterPluginException
        # because RegisterPlugin is called inside the module
        except PluginFileInfo.RegisterPluginException:
            pass
        except:
            eg.PrintTraceback(eg.text.Error.pluginLoadError % self.dirname)
            return
        
        
    class RegisterPluginException(Exception):
        """
        RegisterPlugin will raise this exception to interrupt the loading 
        of the plugin module file.
        """
        pass


    def RegisterPlugin(
        self, 
        name = None,
        description = None,
        kind = "other",
        author = "unknown author",
        version = "unknown version",
        icon = None,
        canMultiLoad = False,
    ):
        if description is None:
            description = name
        self.name = name
        self.description = description
        self.kind = kind
        self.author = author
        self.version = version
        self.icon = icon
        self.canMultiLoad = canMultiLoad
        # we are done with this plugin module, so we can interrupt further 
        # processing by raising RegisterPluginDone
        raise PluginFileInfo.RegisterPluginException
    
    
#    def __getstate__(self):
#        state = self.__dict__.copy()
#        if "module" in state:
#            del state["module"]
#        return state
#    
    
    def __repr__(self):
        return "\n".join(
            (
                "--------- PluginFileInfo --------",
                "Name: %r" % self.name,
                "PluginDir: %r" % self.dirname,
                "Author: %r" % self.author,
                "Version: %r" % self.version,
                "Kind: %r" % self.kind,
            )
        )
        
        
        
class PluginDatabase:
    
    @eg.TimeIt  
    def __init__(self, forceRebuild=(eg.debugLevel > 0)):
        """
        Scans the plugin directory to get all needed information for all 
        plugins.
        
        This will use a simple database file to avoid time consuming processing
        of unchanged plugins. If 'forceRebuild' is True, the old database file
        will be ignored and a new one completely rebuild.
        """
        
        # load the database file if exists
        self.database = {}
        self.databasePath = join(eg.CONFIG_DIR, "PluginDatabase")
        if not forceRebuild:
            self.Load()
        database = self.database
        
        # a new database will be created at the end if a plugin has changed
        hasChanged = False
        newDatabase = {}
            
        # scan through all directories in the plugin directory
        for dirname in os.listdir(eg.PLUGIN_DIR):
            # filter out non-plugin names
            if dirname.startswith(".") or dirname.startswith("_"):
                continue
            pluginDir = join(eg.PLUGIN_DIR, dirname)
            if not isdir(pluginDir):
                continue
            
            # get the highest timestamp of all files in that directory
            highestTimestamp = 0
            for dirpath, dirnames, filenames in os.walk(pluginDir):
                highestTimestamp = max(
                    [stat(join(dirpath, filename)).st_mtime
                        for filename in filenames]
                )
                # little hack to avoid scanning of SVN directories
                for directory in dirnames[:]:
                    if directory.startswith(".svn"):
                        dirnames.remove(directory)
                    
            
            # if the highest timestamp doesn't differ from the database's one
            # we can use the old entry and skip further processing
            if dirname in database:
                if database[dirname].timestamp == highestTimestamp:
                    newDatabase[dirname] = database[dirname]
                    del database[dirname]
                    continue
            
            hasChanged = True
            pluginInfo = PluginFileInfo(dirname)
            pluginInfo.timestamp = highestTimestamp
            newDatabase[dirname] = pluginInfo
            #print repr(pluginInfo)
            
        # only save if something has changed
        needsSave = hasChanged or len(database)
        self.database = newDatabase
        if needsSave:
            self.Save()
                
        
    @eg.LogIt
    def Save(self):
        """
        Save the database to disc.
        """
        with file(self.databasePath, "wb") as databaseFile:
            pickle.dump(eg.versionStr, databaseFile, -1)
            pickle.dump(self.database, databaseFile, -1)
        
    
    def Load(self):
        """
        Load the database from disc.
        """
        if not exists(self.databasePath):
            return
        with file(self.databasePath, "rb") as databaseFile:
            try:
                version = pickle.load(databaseFile)
                if version != eg.versionStr:
                    eg.DebugNote("PluginDatabase version mismatch")
                    return
                self.database = pickle.load(databaseFile)
            except:
                eg.PrintTraceback()
        
    
    def GetPluginInfo(self, pluginName):
        return self.database[pluginName]

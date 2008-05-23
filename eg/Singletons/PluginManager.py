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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

from __future__ import with_statement
import os
import cPickle as pickle
from os import stat
from os.path import isdir, join, exists


        
class RegisterPluginException(Exception):
    """
    RegisterPlugin will raise this exception to interrupt the loading 
    of the plugin module file.
    """
    pass


        
class PluginModuleInfo:
    # some informational fields
    name = "unknown name"
    author = "unknown author"
    version = "unknow version"
    
    # kind gives a hint in which group the plugin should be shown in
    # the AddPluginDialog
    kind = "other"
    
    dirname = None

        
        
class PluginManager:
    
    # the PluginInfo currently been processed
    currentInfo = None
    
    def __init__(self):
        eg.RegisterPlugin = self.RegisterPluginDummy
        self.Refresh()
    
    
    @eg.TimeIt  
    def Refresh(self, forceRebuild=(eg.debugLevel > 0)):
        """
        Scans the plugin directory to get all needed information for all 
        plugins.
        
        This will use a simple database file to avoid time consuming processing
        of unchanged plugins. If 'forceRebuild' is True, the old database file
        will be ignored and a new one completely rebuild.
        """
        
        # load the database file if exists
        self.database = {}
        self.databasePath = join(eg.CONFIG_DIR, "pluginManager")
        if not forceRebuild:
            self.Load()
        database = self.database
        
        # a new database will be created at the end if a plugin has changed
        hasChanged = False
        newDatabase = {}
        
        # prepare the interruption of plugin module import on RegisterPlugin
        eg.RegisterPlugin = self.RegisterPlugin
        
        # scan through all directories in the plugin directory
        for dirname in os.listdir(eg.PLUGIN_DIR):
            # filter out non-plugin names
            if dirname.startswith(".") or dirname.startswith("_"):
                continue
            pluginDir = join(eg.PLUGIN_DIR, dirname)
            if not isdir(pluginDir):
                continue
            if not exists(join(pluginDir, "__init__.py")):
                continue
            
            # get the highest timestamp of all files in that directory
            highestTimestamp = 0
            for dirpath, dirnames, filenames in os.walk(pluginDir):
                for filename in filenames:
                    timestamp = stat(join(dirpath, filename)).st_mtime
                    if timestamp > highestTimestamp:
                        highestTimestamp = timestamp
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
            pluginInfo = self.LoadPluginInfo(dirname)
            if pluginInfo is None:
                print dirname
            else:
                pluginInfo.timestamp = highestTimestamp
                newDatabase[dirname] = pluginInfo
            #print repr(pluginInfo)
            
        # let RegisterPlugin be a normal (and useless) function again
        eg.RegisterPlugin = self.RegisterPluginDummy
        
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
            pickle.dump(eg.Version.string, databaseFile, -1)
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
                if version != eg.Version.string:
                    eg.PrintDebugNotice("pluginManager version mismatch")
                    return
                self.database = pickle.load(databaseFile)
            except:
                eg.PrintTraceback()
        
    
    def GetPluginInfo(self, pluginName):
        return self.database[pluginName]
    
    
    def LoadPluginInfo(self, pluginDir):
        self.currentInfo = PluginModuleInfo()
        self.currentInfo.dirname = pluginDir
        
        try:
            module = eg.PluginInfo.ImportPlugin(pluginDir)
        # It is expected that the loading will raise RegisterPluginException
        # because RegisterPlugin is called inside the module
        except RegisterPluginException:
            return self.currentInfo
        except:
            eg.PrintTraceback(eg.text.Error.pluginLoadError % pluginDir)
            return
        finally:
            self.currentInfo = None
        
        
    def RegisterPlugin(
        self, 
        name = None,
        description = None,
        kind = "other",
        author = "unknown author",
        version = "unknown version",
        icon = None,
        canMultiLoad = False,
        createMacrosOnAdd = False,
        url = None,
        help = None,
    ):
        if name is None:
            name = self.currentInfo.dirname
        if description is None:
            description = name
        if help is not None:
            help = "\n".join([s.strip() for s in help.splitlines()])
            help = help.replace("\n\n", "<p>")
            description += "\n\n<p>" + help
        self.currentInfo.__dict__.update(locals())
        # we are done with this plugin module, so we can interrupt further 
        # processing by raising RegisterPluginDone
        raise RegisterPluginException
        
    
    def RegisterPluginDummy(self, *args, **kwargs):
        pass
    
    
    def GetPluginInfoList(self):
        """
        Get a list of all PluginInfo for all plugins in the plugin directory
        """
        infoList = [
            eg.PluginInfo.GetPluginInfo(pluginName) 
            for pluginName in self.database.iterkeys()
        ]
        infoList.sort(key=lambda x: x.name.lower())
        return infoList
        



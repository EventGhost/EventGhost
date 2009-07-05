# This file is part of EventGhost.
# Copyright (C) 2009 Lars-Peter Voss <bitmonster@eventghost.org>
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

import os
import sys
from os.path import join, exists
import eg

class RegisterPluginException(Exception):
    """
    RegisterPlugin will raise this exception to interrupt the loading
    of the plugin module file.
    """
    pass



class PluginModuleInfo(object):
    name = "unknown"
    description = ""
    author = "unknown author"
    version = "unknown version"
    kind = "other"
    canMultiLoad = False
    createMacrosOnAdd = False
    icon = eg.Icons.PLUGIN_ICON
    url = None
    englishName = None
    englishDescription = None
    path = None
    timestamp = None
    pluginName = None
    

    def __init__(self, path):
        self.path = path
        self.pluginName = os.path.basename(path)
        originalRegisterPlugin = eg.RegisterPlugin
        eg.RegisterPlugin = self.RegisterPlugin
        try:
            self.Import()
        except RegisterPluginException:
            # It is expected that the loading will raise RegisterPluginException
            # because RegisterPlugin is called inside the module
            pass
        except:
            eg.PrintTraceback(eg.text.Error.pluginLoadError % self.path)
        finally:
            eg.RegisterPlugin = originalRegisterPlugin
    
    
    if eg.debugLevel:
        def __setattr__(self, name, value):
            if not hasattr(self.__class__, name):
                raise AttributeError(
                    "PluginModuleInfo has no attribute %s" % name
                )
            object.__setattr__(self, name, value)


    def Import(self):
        if self.path.startswith(eg.PLUGIN_DIR):
            moduleName = "eg.PluginModule." + self.pluginName
        else:
            moduleName = "eg.UserPluginModule." + self.pluginName
        if moduleName in sys.modules:
            return sys.modules[moduleName]
        module = __import__(moduleName, None, None, [''])
        return module


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
        guid = None,
        #**kwargs
    ):
        """
        Registers information about a plugin to EventGhost.

        :param name: should be a short descriptive string with the name of the
           plugin.
        :param description: the description of the plugin.
        :param kind: gives a hint about the category the plugin belongs to. It
           should be a string with a value out of "remote" (for remote receiver
           plugins), "program" (for program control plugins), "external" (for
           plugins that control external hardware) or "other" (if none of the
           other categories match).
        :param author: can be set to the name of the developer of the plugin.
        :param version: can be set to a version string.
        :param canMultiLoad: set this to ``True``, if a configuration can have
           more than one instance of this plugin.
        :param \*\*kwargs: just to consume unknown parameters, to make the call
           backward compatible.
        """
        if name is None:
            name = self.pluginName
        if description is None:
            description = name
        if help is not None:
            help = "\n".join([s.strip() for s in help.splitlines()])
            help = help.replace("\n\n", "<p>")
            description += "\n\n<p>" + help
        if guid:
            guid = guid.upper()
        self.name = self.englishName = name
        self.description = self.englishDescription = description
        self.kind = kind
        self.author = author
        self.version = version
        self.canMultiLoad = canMultiLoad
        self.createMacrosOnAdd = createMacrosOnAdd
        self.url = url

        # get the icon if any
        if icon is not None:
            self.icon = eg.Icons.StringIcon(icon)
        else:
            iconPath = join(self.path, "icon.png")
            if exists(iconPath):
                self.icon = eg.Icons.PathIcon(iconPath)
                
        # try to translate name and description
        textCls = getattr(eg.text.Plugin, self.pluginName, None)
        if textCls is not None:
            self.name = getattr(textCls, "name", name)
            self.description = getattr(textCls, "description", description)

        # we are done with this plugin module, so we can interrupt further
        # processing by raising RegisterPluginException
        raise RegisterPluginException


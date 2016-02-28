# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import ConfigParser


class Config(object):

    def __init__(self, buildSetup, configFilePath):
        self.buildSetup = buildSetup
        self._configFilePath = configFilePath
        self.LoadSettings()


    def LoadSettings(self):
        """
        Load the ini file and set all options.
        """
        configParser = ConfigParser.ConfigParser()
        configParser.read(self._configFilePath)
        for task in self.buildSetup.tasks:
            section = task.GetId()
            if not configParser.has_section(section):
                continue
            options = configParser.options(section)
            for option in options:
                if option == "enabled":
                    if task.visible:
                        task.activated = eval(
                            configParser.get(section, "enabled")
                        )
                else:
                    task.options[option] = configParser.get(section, option)
                    print section, option, configParser.get(section, option)

    def SaveSettings(self):
        """
        Save all options to the ini file.
        """
        config = ConfigParser.ConfigParser()
        # make ConfigParser case-sensitive
        config.optionxform = str
        config.read(self._configFilePath)
        for task in self.buildSetup.tasks:
            section = task.GetId()
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, "enabled", task.activated)
        configFile = open(self._configFilePath, "w")
        config.write(configFile)
        configFile.close()


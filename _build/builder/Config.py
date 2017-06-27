# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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
from builder.Utils import IsCIBuild


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
        if not IsCIBuild():
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
                    #print section, option, configParser.get(section, option)

        if configParser.has_option("GitHub", "Repository"):
            repository = configParser.get('GitHub', "Repository")
            try:
                user, repo = repository.split('/')
            except ValueError:
                user = repo = ""
            self.buildSetup.gitConfig.update({
                "user": user,
                "repo": repo,
                "branch": configParser.get('GitHub', "Branch")
            })

        if configParser.has_option("Website", "url"):
            self.buildSetup.args.websiteUrl = configParser.get('Website', "url")

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

        if not config.has_section('GitHub'):
                config.add_section('GitHub')
        repo = "{user}/{repo}".format(**self.buildSetup.gitConfig)
        config.set('GitHub', "Repository", repo)
        config.set('GitHub', "Branch", self.buildSetup.gitConfig["branch"])

        if not config.has_section('Website'):
                config.add_section('Website')
        config.set('Website', "url", self.buildSetup.args.websiteUrl)

        configFile = open(self._configFilePath, "w")
        config.write(configFile)
        configFile.close()

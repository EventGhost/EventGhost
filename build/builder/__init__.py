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


import tempfile
import sys
from os.path import abspath, dirname, join
from Utils import DecodePath, GetRevision, GetGithubConfig


class Task(object):
    value = None
    visible = True
    enabled = True
    activated = True

    def __init__(self, buildSetup):
        self.buildSetup = buildSetup

    def Setup(self):
        pass

    @classmethod
    def GetId(cls):
        return cls.__module__ + "." + cls.__name__

    def DoTask(self):
        raise NotImplementedError


class Builder(object):
    def __init__(self):
        from CheckDependencies import CheckDependencies
        global buildSetup
        Task.buildSetup = self
        buildSetup = self
        baseDir = dirname(DecodePath(__file__))
        self.sourceDir = abspath(join(baseDir, "../.."))
        if not CheckDependencies(self):
            sys.exit(1)
        self.websiteDir = join(self.sourceDir, "website")
        self.dataDir = abspath(join(baseDir, "Data"))
        self.pyVersionStr = "%d%d" % sys.version_info[:2]
        self.pyVersionDir = join(self.dataDir, "Python%s" % self.pyVersionStr)
        self.libraryName = "lib%s" % self.pyVersionStr
        self.libraryDir = join(self.sourceDir, self.libraryName)
        try:
            self.gitConfig = GetGithubConfig()
        except ValueError:
            print ".gitconfig does not contain needed options. Please do:\n" \
                  "\t$ git config --global github.user <your github username>\n" \
                  "\t$ git config --global github.token <your github token>\n" \
                  "To create a token, go to: https://github.com/settings/tokens\n"
            exit(1)
        except IOError:
            print "could not open .gitconfig."
            exit(1)
        self.appVersion = None
        self.appRevision = None
        self.tmpDir = tempfile.mkdtemp()
        self.appName = self.name

    def RunGui(self):
        from Tasks import TASKS
        self.tasks = [task(self) for task in TASKS]
        from Config import Config
        self.config = Config(self, join(self.dataDir, "Build.ini"))
        for task in self.tasks:
            task.Setup()
        import Gui
        GetRevision(self)
        Gui.Main(self)


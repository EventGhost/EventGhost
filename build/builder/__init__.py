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


import argparse
import sys
import tempfile
from os.path import abspath, dirname, join

from builder import VirtualEnv
from builder.Utils import DecodePath, GetRevision, GetGitHubConfig


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
        if not VirtualEnv.Running() and VirtualEnv.Exists():
            VirtualEnv.Activate()

        global buildSetup
        Task.buildSetup = self
        buildSetup = self

        self.args = self.ParseArgs()
        baseDir = dirname(DecodePath(__file__))
        self.sourceDir = abspath(join(baseDir, "../.."))
        self.websiteDir = join(self.sourceDir, "website")
        self.dataDir = abspath(join(baseDir, "Data"))
        self.pyVersionStr = "%d%d" % sys.version_info[:2]
        self.pyVersionDir = join(self.dataDir, "Python%s" % self.pyVersionStr)
        self.libraryName = "lib%s" % self.pyVersionStr
        self.libraryDir = join(self.sourceDir, self.libraryName)

        from CheckDependencies import CheckDependencies
        if not CheckDependencies(self):
            sys.exit(1)

        try:
            self.gitConfig = GetGitHubConfig()
        except ValueError:
            print ".gitconfig does not contain needed options. Please do:\n" \
                  "\t$ git config --global github.user <your github username>\n" \
                  "\t$ git config --global github.token <your github token>\n" \
                  "To create a token, go to: https://github.com/settings/tokens\n"
            exit(1)
        except IOError:
            print "WARNING: Git config not available; can't release to GitHub!"
            self.gitConfig = {
                "all_repos": {
                    "EventGhost/EventGhost": {
                        "all_branches": ["master"],
                        "def_branch": "master",
                        "name": "EventGhost",
                    },
                },
                "branch": "master",
                "repo": "EventGhost",
                "repo_full": "EventGhost/EventGhost",
                "token": "",
                "user": "EventGhost",
            }

        self.appVersion = None
        self.appRevision = None
        self.tmpDir = tempfile.mkdtemp()
        self.appName = self.name

    def ParseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-m", "--make-env",
            action="store_true",
            help="auto-install dependencies into a virtualenv",
        )
        return parser.parse_args()

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


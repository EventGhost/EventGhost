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

from py2exe import build_exe


class Build(build_exe.py2exe):

    def get_sub_commands(self):
        sub_commands = build_exe.py2exe.get_sub_commands(self)
        if 'build_ext' in sub_commands:
            sub_commands.remove('build_ext')
        sub_commands.insert(0, 'build_ext')
        # if 'build_docs' not in sub_commands:
        #     sub_commands += ['build_docs']

        return sub_commands

    def run(self):
        self.distribution.run_command('build_ext')
        build_exe.py2exe.run(self)

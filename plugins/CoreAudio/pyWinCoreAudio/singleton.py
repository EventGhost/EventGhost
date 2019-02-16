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


class Singleton(type):
    _instances = {}

    def __call__(cls, *args):
        if cls not in cls._instances:
            cls._instances[cls] = {}

        instances = cls._instances[cls]

        for key, value in instances.items():
            if key == args:
                return value

        instances[args] = super(
            Singleton,
            cls
        ).__call__(*args)

        # print '{'
        #
        # for key, value in cls._instances.items():
        #     print '   ', repr(str(key)) + ': {'
        #     for k, v in value.items():
        #         k = ', '.join(repr(str(item)) for item in k)
        #         print '        (' + k + '):', repr(str(v)) + ','
        #     print '    },'
        # print '}'

        return instances[args]

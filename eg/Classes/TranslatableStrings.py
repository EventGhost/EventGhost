# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
from eg.Utils import SetDefault


class TranslatableStringsMeta(type):

    def __new__(mcs, name, bases, dct):
        defaultText = type.__new__(mcs, name, bases, dct)
        if len(bases):
            moduleName = dct["__module__"].split(".")[-1]
            translatedText = getattr(eg.text, moduleName, None)
            if translatedText is None:
                setattr(eg.text, moduleName, defaultText)
                return defaultText
            else:
                SetDefault(translatedText, defaultText)
                return translatedText
        return defaultText



class TranslatableStrings:
    __metaclass__ = TranslatableStringsMeta


# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2007-10-05 02:25:25 +0200 (Fri, 05 Oct 2007) $
# $LastChangedRevision: 242 $
# $LastChangedBy: bitmonster $



from Utils import SetClass

class CustomMetaclass(type):
    def __new__(cls, name, bases, dct):
        if len(bases):
            moduleName = dct["__module__"].split(".")[-1]
            class NewCls:
                pass
            NewCls.__dict__ = dct
            trans = getattr(eg.text, moduleName, None)
            if trans is None:
                class Trans:
                    pass
                trans = Trans()
            SetClass(trans, NewCls)
            setattr(eg.text, moduleName, trans)
            return trans
        return type.__new__(cls, name, bases, dct)


class TranslatableStrings:
    __metaclass__ = CustomMetaclass
        

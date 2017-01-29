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

# Local imports

from types import ClassType
from StringIO import StringIO

import eg
from eg.Utils import PrettyPythonPrint


class PersistentDataBase(object):
    _parent = None
    _key = ''

    def __init__(self, parent, key):
        self._parent = parent
        self._key = key

    def IsDelete(self):
        for key in ('_Delete', '_PermanentDelete'):
            if self._key.startswith(key):
                return True
        return False

    def SetDelete(self, flag=True):

        def SetAttr(key):
            if key.startswith('_'):
                attr = self._parent.__dict__.pop(self._key)
            else:
                attr = getattr(self._parent, self._key)
                setattr(self._parent, self._key, None)
            setattr(attr, '_key', key)
            setattr(self._parent, key, attr)

        if self._key and not self._key.startswith('_PermanentDelete'):
            if flag:
                if not self._key.startswith('_Delete'):
                    SetAttr('_Delete' + self._key)
            else:
                if self._key.startswith('_Delete'):
                    SetAttr(self._key[7:])

    def SaveData(self, fileWriter, indent):
        classKeys = []

        for key, value in self:
            if type(value) in (PersistentDataMeta, PersistentDataBase):
                classKeys.append([key, value])
            else:
                line = PrettyPythonPrint(key, value, indent)
                fileWriter(line)

        for key, value in classKeys:
            tmpFile = StringIO()

            value.SaveData(tmpFile.write, indent + 4)
            data = tmpFile.getvalue()
            tmpFile.close()
            if data:
                formatString = '\n%sclass %s:\n'
                if not indent and key == 'eg':
                    formatString = '\n' + formatString

                fileWriter(formatString % (' ' * indent, key))
                fileWriter(data)

    def GetModuleName(self):
        moduleName = repr(self._parent).split(' ')[0][1:]
        if self._key:
            moduleName += '.' + self._key

        return moduleName

    def __repr__(self):
        objRepr = object.__repr__(self).split(' ')
        objRepr[0] = '<' + self.GetModuleName()
        return ' '.join(objRepr)

    def __delete__(self, instance):
        if not self._key or self._key.startswith('_PermanentDelete'):
            return

        if self._key.startswith('_'):
            attr = getattr(self._parent, self._key)
            setattr(self._parent, self._key, None)
            setattr(attr, '_key', self._key[7:])
        else:
            attr = self._parent.__dict__.pop(self._key)

        setattr(attr, '_key', '_PermanentDelete' + self._key)
        setattr(self._parent, getattr(attr, '_key'), attr)

    def __iter__(self):
        for key in sorted(self.__dict__.keys()):
            if not key.startswith('_'):
                yield key, self.__dict__[key]

    def __getitem__(self, item):
        return getattr(self, item)

    def __getattr__(self, item):
        if not item.startswith('_'):
            if item in self.__dict__:
                return self.__dict__[item]
            if hasattr(self, '_PermanentDelete' + item):
                return getattr(self, '_PermanentDelete' + item)
            if hasattr(self, '_Delete' + item):
                return getattr(self, '_Delete' + item)

        raise AttributeError(
            '%s does not have attribute %s' % (self.GetModuleName(), item)
        )

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            self.__dict__[key] = value

    def __delitem__(self, key):
        delattr(self, key)

    def __delattr__(self, item):
        if item.startswith('_'):
            object.__delattr__(self, item)
        if item in self.__dict__:
            del(self.__dict__[item])
        else:
            raise AttributeError(
                '%s does not have attribute %s' % (self.GetModuleName(), item)
            )


class PersistentDataMeta(type):
    def __new__(mcs, name, bases, dct):
        cls = type.__new__(mcs, name, bases, dct)
        if len(bases):
            searchPath = dct["__module__"]
            config = eg.config
            parts = searchPath.split(".")

            plugin = False
            for part in parts:
                if hasattr(config, part):
                    config = getattr(config, part)
                else:
                    newConfig = PersistentDataBase(config, part)
                    setattr(config, part, newConfig)
                    config = newConfig

                    if plugin:
                        if part in ('EventGhost', 'Window', 'System', 'Mouse'):
                            plugin = False
                        else:
                            config.SetDelete(True)

                if part in ('CorePluginModule', 'UserPluginModule'):
                    plugin = True

            def IterDict(c, d):
                for k in d.keys():
                    if k.startswith('_'):
                        continue
                    v = d[k]
                    if isinstance(v, ClassType):
                        if hasattr(c, k):
                            configCls = getattr(c, k)
                        else:
                            configCls = PersistentDataBase(c, k)
                        IterDict(configCls, v.__dict__)
                        setattr(c, k, configCls)
                    else:
                        if not hasattr(c, k):
                            setattr(c, k, v)
            IterDict(config, cls.__dict__)

            return config

        return cls


class PersistentData:
    __metaclass__ = PersistentDataMeta

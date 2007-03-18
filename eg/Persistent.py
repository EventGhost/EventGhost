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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import cPickle as pickle
import types


class Section:
    
    def __init__(self, defaults=None):
        if defaults:
            for key, value in defaults.__dict__.iteritems():
                if type(value) == types.ClassType:
                    setattr(self, key, Section(value))
                elif not hasattr(self, key):
                    setattr(self, key, value)
                    
                    
    def setdefault(self, key, default):
        if not self.__dict__.has_key(key):
            setattr(self, key, Section(default))
        else:
            section = self.__dict__[key]
            for key2, value in default.__dict__.iteritems():
                if not hasattr(section, key2):
                    setattr(section, key2, value)
        return getattr(self, key)
    
    
    
def load(filename):
    fd = open(filename)
    obj = pickle.load(fd)
    fd.close()
    return obj


def save(obj, filename):
    fd = open(filename, 'w+')
    pickle.dump(obj, fd)
    fd.close()
    

def _py_save_recursion(obj, fileWriter, indent=0):
    objDict = obj.__dict__
    keys = objDict.keys()
    keys.sort()
    class_keys = []
    for key in keys:
        if key.startswith("__"):
            continue
        value = objDict[key]
        if type(value) == types.ClassType:
            class_keys.append(key)
        elif type(value) == types.InstanceType:
            class_keys.append(key)
        else:
            line = (indent * 4 * " ") + key + " = " + repr(value) + "\n"
            fileWriter(line)        
    for key in class_keys:
        value = objDict[key]
        fileWriter((indent * 4 * " ") + "class " + key + ":\n")
        _py_save_recursion(value, fileWriter, indent + 1)
        
        
def PySave(obj, filename):
    fd = open(filename, 'w+')
    _py_save_recursion(obj, fd.write)
    fd.close()
    
    
def _MakeSectionMetaClass(name, bases, dict):
    obj = Section()
    obj.__dict__ = dict
    return obj
    
    
def PyLoad(filename, defaults=None):
    obj = Section(defaults)
    execDict = {"__metaclass__": _MakeSectionMetaClass}
    try:
        execfile(filename, execDict, obj.__dict__)
    except:
        pass
    return obj


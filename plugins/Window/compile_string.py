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

import re
import types


class MatchSingleChar:
    # just a named object
    pass
    
class MatchAny:
    # just a named object
    pass
    

def compile_string(pattern):
    if pattern is None:
        return None
    res = []
    start = 0
    tmp = ""
    end = pattern.find('{')
    use_regex = False
    while end != -1:
        tmp += pattern[start:end]
        end += 1
        if len(pattern)-1 < end:
            raise SyntaxError("unmatched curly-brace at end")
        elif pattern[end] == "{":
            tmp += "{"
            end += 1
        else:
            word_start = end
            end = pattern.find('}', word_start)
            if end == -1:
                raise SyntaxError("unmatched curly-brace")
            word = pattern[word_start:end]
            if word == "*":
                if tmp != "":
                    res.append(tmp)
                    tmp = ""
                use_regex = True
                res.append(MatchAny)
            elif word == "?":
                if tmp != "":
                    res.append(tmp)
                    tmp = ""
                use_regex = True
                res.append(MatchSingleChar)
            end += 1
        start = end
        end = pattern.find('{', start)
    tmp += pattern[start:]
    res.append(tmp)
    if use_regex:
        pattern = "^"
        for tmp in res:
            if type(tmp) in types.StringTypes:
                pattern += re.escape(tmp)
            elif tmp == MatchSingleChar:
                pattern += "."
            elif tmp == MatchAny:
                pattern += ".*"
        pattern += "$"
        return re.compile(pattern).match
    else:
        return lambda s: s == pattern
            
    

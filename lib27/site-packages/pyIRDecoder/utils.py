# -*- coding: utf-8 -*-
#
# ***********************************************************************************
# MIT License
#
# Copyright (c) 2020 Kevin G. Schlosser
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# ***********************************************************************************


def clean_code(ir_code, threshold):
    low_threshold = 1.0 - (threshold / 100.0)
    high_threshold = 1.0 + (threshold / 100.0)
    marks = []
    spaces = []
    cleaned_code = []

    for timing in ir_code:
        if timing < 0:
            for space in spaces:
                avg = sum(space) / len(space)

                low = int(avg * high_threshold)
                high = int(avg * low_threshold)
                if low <= timing <= high:
                    space += [timing]
                    break
            else:
                spaces += [[timing]]
        else:
            for mark in marks:
                avg = sum(mark) / len(mark)

                high = int(avg * high_threshold)
                low = int(avg * low_threshold)

                if low <= timing <= high:
                    mark += [timing]
                    break
            else:
                marks += [[timing]]

    marks2 = []
    spaces2 = []

    # double check the groups for any possible straglers
    while marks:
        mark = marks.pop(0)
        avg_mark = sum(mark) / len(mark)
        for m in marks:
            avg = sum(m) / len(m)
            high = int(avg * high_threshold)
            low = int(avg * low_threshold)
            if low <= avg_mark <= high:
                m.extend(mark[:])
                break
        else:
            for m in marks2:
                avg = sum(m) / len(m)
                high = int(avg * high_threshold)
                low = int(avg * low_threshold)

                if low <= avg_mark <= high:

                    m.extend(mark[:])
                    break
            else:
                marks2 += [mark[:]]

    while spaces:
        space = spaces.pop(0)
        avg_space = sum(space) / len(space)
        for s in spaces:
            avg = sum(s) / len(s)
            high = int(avg * high_threshold)
            low = int(avg * low_threshold)

            if low <= avg_space <= high:
                s.extend(space[:])
                break
        else:
            for s in spaces2:
                avg = sum(s) / len(s)
                high = int(avg * high_threshold)
                low = int(avg * low_threshold)

                if low <= avg_space <= high:
                    s.extend(space[:])
                    break
            else:
                spaces2 += [space[:]]

    del marks[:]
    del spaces[:]

    for mark in marks2:
        mark = sum(mark) / len(mark)
        marks += [mark]

    for space in spaces2:
        space = sum(space) / len(space)
        spaces += [space]

    for timing in ir_code:
        for mark in marks:
            low = int(mark * low_threshold)
            high = int(mark * high_threshold)
            if low <= timing <= high:
                cleaned_code += [mark]
                break
        else:
            for space in spaces:
                high = int(space * low_threshold)
                low = int(space * high_threshold)
                if low <= timing <= high:
                    cleaned_code += [space]
                    break
            else:
                cleaned_code += [timing]

    return cleaned_code


def build_mce_rlc(code):
    rlc = []

    for timing in code:
        dif = timing % 50

        if dif < 25:
            dif = -dif
        else:
            dif = 50 - dif

        timing += dif
        rlc += [timing]

    return rlc

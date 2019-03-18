# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Walter Kraembring
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of Walter Kraembring nor the names of its contributors may
#    be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##############################################################################

import sys
import os
from decimal import Decimal
from datetime import datetime, timedelta
import css


pointI = 10


def days_hours_minutes(td):
    m = td.days * 24 *60
    m += td.seconds//60
    return int(m), int(td.days)


def MakeChart_10(drows, pos, titles, vsuffix):
    logstr = ""
    series = {}
    series_list = []
    sedt = [0, 999999, '', '']
    lgth = 0
    d1 = datetime.now()
        
    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                rows = drows[key]
                start, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                )
                end, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[-1][0][:-3]), '%Y-%m-%d %H:%M')
                )
                if start > sedt[0]:
                    sedt[0] = start
                    sedt[2] = str(rows[0][0][:-3])
                if end <= sedt[1]:
                    sedt[1] = end
                    sedt[3] = str(rows[-1][0][:-3])
                pD = sedt[2].split(' ')[0].split('-')
                pT = sedt[2].split(' ')[1].split(':')
                pointStart = pD + pT

    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                # convert the data into a table
                tableId = str(key.encode('utf-8'))
                data = []
                series = {}
                rows = drows[key]
                bFirstDone = False
                for row in rows:
                    rd = float("%.2f" % row[pos])
                    rt = row[0][:-3].split(' ')[1].split(':')
                    diff = 0
                    now_d =0
                    rdt = row[0][:-3].split(' ')[0].split('-')
                    if bFirstDone and (rt[1][:1] <> rt_old[1][:1] or rt[0] <> rt_old[0] or rdt != rdt_old):
                        delta, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if delta >= 10:
                            if d > 0:
                                now_d = d * 24 * 6
                            before_h = int(rt_old[0]) * 6
                            before_m = int(rt_old[1][:1])
                            now_h = int(rt[0]) * 6
                            now_m = int(rt[1][:1])
                            if now_h < before_h:
                                now_h += 24 * 6
                            now = now_d + now_h + now_m
                            before = before_h + before_m
                            #if now-before-1 > 0:
                            #    print now-before-1
                            #    print row_old[0], row[0]
                            diff = int(now-before)
                            for i in range(diff-1):
                               data.append('null')
                        diff = 0
                        if rd == 0.0:
                            data.append('null')
                        else:
                            data.append(rd)
                    elif not bFirstDone:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s >= 2 * pointI:
                            for i in range(int((sedt[0] - s)/pointI)-1):
                                data.append('null')
                        if rd == 0.0:
                            data.append('null')
                        else:
                            data.append(rd)
                        bFirstDone = True
                    rt_old = rt
                    rdt_old = rdt
                    row_old = row
                series['name'] = tableId
                series['data'] = data
                series_list.append(series)
                lgth = len(data)
            else:
                print "No data found during specified range for", key
        
        if len(drows)>0 and lgth>0:
            logstr += HighchartSnippet_10('spline', tableId, titles, vsuffix, series_list, pointStart)

    return logstr


def MakeChart(drows, pos, titles, vsuffix):
    logstr = ""
    series = {}
    series_list = []
    selectedPeriod = '... - ...'
    sedt = [0, 999999, '', '']
    lgth = 0
    d1 = datetime.now()
        
    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                rows = drows[key]
                start, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                )
                end, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[-1][0][:-3]), '%Y-%m-%d %H:%M')
                )
                if start > sedt[0]:
                    sedt[0] = start
                    sedt[2] = str(rows[0][0][:-3])
                if end <= sedt[1]:
                    sedt[1] = end
                    sedt[3] = str(rows[-1][0][:-3])
                selectedPeriod = sedt[2]+' - '+sedt[3]
                pD = sedt[2].split(' ')[0].split('-')
                pT = sedt[2].split(' ')[1].split(':')
                pointStart = pD + pT

    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                # convert the data into a table
                tableId = str(key.encode('utf-8'))
                data = []
                series = {}
                rows = drows[key]
                diff = 0
                bFirstDone = False
                for row in rows:
                    rd = float("%.2f" % row[pos])
                    if bFirstDone:
                        diff, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if diff > 0:
                            for i in range(diff-1):
                               data.append('null')
                            diff = 0
                            if rd == 0.0:
                                data.append('null')
                            else:
                                data.append(rd)
                    else:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s > 0:
                            for i in range(sedt[0] - s):
                                data.append('null') 
                        data.append(rd)
                        bFirstDone = True
                    row_old = row
                series['name'] = tableId
                series['data'] = data
                series_list.append(series)
                lgth = len(data)
            else:
                print "No data found during specified range for", key
        
        if len(drows)>0 and lgth>0:
            #logstr += "<p><small>Selected period: "+selectedPeriod+"</small></p>"+'\n\r'
            logstr += HighchartSnippet('spline', tableId, titles, vsuffix, series_list, pointStart)

    return logstr


def MakeRainChart_10(drows, pos, titles, vsuffix):
    logstr = ""
    series = {}
    series_list = []
    sedt = [0, 999999, '', '']
    lgth = 0
    d1 = datetime.now()

    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                rows = drows[key]
                start, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                )
                end, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[-1][0][:-3]), '%Y-%m-%d %H:%M')
                )
                if start > sedt[0]:
                    sedt[0] = start
                    sedt[2] = str(rows[0][0][:-3])
                if end <= sedt[1]:
                    sedt[1] = end
                    sedt[3] = str(rows[-1][0][:-3])
                pD = sedt[2].split(' ')[0].split('-')
                pT = sedt[2].split(' ')[1].split(':')
                pointStart = pD + pT
    
    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                # convert the data into a table
                tableId = key
                data = []
                series = {}
                rows = drows[key]
                periodRain = str(rows[-1][4]-rows[0][4])
                bFirstDone = False
                for row in rows:
                    rt = row[0][:-3].split(' ')[1].split(':')
                    diff = 0
                    now_d =0
                    rdt = row[0][:-3].split(' ')[0].split('-')
                    if bFirstDone and (rt[1][:1] <> rt_old[1][:1] or rt[0] <> rt_old[0] or rdt != rdt_old):
                        delta, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if delta >= 10:
                            if d > 0:
                                now_d = d * 24 * 6
                            before_h = int(rt_old[0]) * 6
                            before_m = int(rt_old[1][:1])
                            now_h = int(rt[0]) * 6
                            now_m = int(rt[1][:1])
                            if now_h < before_h:
                                now_h += 24 * 6
                            now = now_d + now_h + now_m
                            before = before_h + before_m
                            #if now-before-1 > 0:
                            #    print now-before-1
                            #    print row_old[0], row[0]
                            diff = int(now-before)
                            for i in range(diff-1):
                               data.append('null')
                        diff = 0
                        if int(rt[1])<>int(rt_old[1]):
                            if row[pos] != r_old:
                                rd = row[pos]-r_old
                                data.append(rd)
                            if row[pos] == r_old:
                                rd = 0.0
                                data.append(rd)
                    elif not bFirstDone:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s >= 2 * pointI:
                            for i in range(int((sedt[0] - s)/pointI)-1):
                                data.append('null')
                        bFirstDone = True
                    rt_old = rt
                    rdt_old = rdt
                    row_old = row
                    r_old =row[pos]
                series['name'] = "Rain level"
                series['data'] = data
                series_list.append(series)
                lgth = len(data)
            else:
                print "No data found during specified range for", key

        if len(drows)>0 and lgth>0:
            #logstr += "<p><small>Total rain during period: "+periodRain+" mm</small></p>"+'\n\r'
            logstr += HighchartSnippet_10('column', tableId, titles, vsuffix, series_list, pointStart)

    return logstr


def MakeRainChart(drows, pos, titles, vsuffix):
    logstr = ""
    series = {}
    series_list = []
    selectedPeriod = '... - ...'
    sedt = [0, 999999, '', '']
    lgth = 0
    d1 = datetime.now()

    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                rows = drows[key]
                start, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                )
                end, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[-1][0][:-3]), '%Y-%m-%d %H:%M')
                )
                if start > sedt[0]:
                    sedt[0] = start
                    sedt[2] = str(rows[0][0][:-3])
                if end <= sedt[1]:
                    sedt[1] = end
                    sedt[3] = str(rows[-1][0][:-3])
                selectedPeriod = sedt[2]+' - '+sedt[3]
                pD = sedt[2].split(' ')[0].split('-')
                pT = sedt[2].split(' ')[1].split(':')
                pointStart = pD + pT
    
    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                # convert the data into a table
                tableId = key
                data = []
                series = {}
                rows = drows[key]
                periodRain = str(rows[-1][4]-rows[0][4])
                diff = 0
                bFirstDone = False
                for row in rows:
                    rt = row[0][:-3].split(' ')[1].split(':')
                    if bFirstDone:
                        diff, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if diff > 0:
                            for i in range(diff-1):
                                data.append('null')
                            diff = 0
                        if int(rt[1])<>int(rt_old[1]):
                            if row[pos] != r_old:
                                rd = row[pos]-r_old
                                data.append(rd)
                            if row[pos] == r_old:
                                rd = 0.0
                                data.append(rd)
                    else:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s > 0:
                            for i in range(sedt[0] - s):
                                data.append('null') 
                        data.append('null')
                        bFirstDone = True
                    rt_old = rt
                    row_old = row
                    r_old =row[pos]
                series['name'] = "Rain level"
                series['data'] = data
                series_list.append(series)
                lgth = len(data)
            else:
                print "No data found during specified range for", key

        if len(drows)>0 and lgth>0:
            #logstr += "<p><small>Selected period: "+selectedPeriod+"</small></p>"+'\n\r'
            #logstr += "<p><small>Total rain during period: "+periodRain+" mm</small></p>"+'\n\r'
            logstr += HighchartSnippet('column', tableId, titles, vsuffix, series_list, pointStart)

    return logstr


def MakeLightChart_10(drows, pos, titles, vsuffix):
    logstr = ""
    series_list = []
    data = []
    sedt = [0, 999999, '', '']
    lgth = 0
    d1 = datetime.now()

    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                rows = drows[key]
                start, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                )
                end, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[-1][0][:-3]), '%Y-%m-%d %H:%M')
                )
                if start > sedt[0]:
                    sedt[0] = start
                    sedt[2] = str(rows[0][0][:-3])
                if end <= sedt[1]:
                    sedt[1] = end
                    sedt[3] = str(rows[-1][0][:-3])
                selectedPeriod = sedt[2]+' - '+sedt[3]
                pD = sedt[2].split(' ')[0].split('-')
                pT = sedt[2].split(' ')[1].split(':')
                pointStart = pD + pT
    
    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                # convert the data into a table
                data = []
                series = {}
                rows = drows[key]
                bFirstDone = False
                for row in rows:
                    rd = float("%.2f" % row[pos])
                    rd = rd*10.0 + 60.0
                    rt = row[0][:-3].split(' ')[1].split(':')
                    diff = 0
                    now_d =0
                    rdt = row[0][:-3].split(' ')[0].split('-')
                    if bFirstDone and (rt[1][:1] <> rt_old[1][:1] or rt[0] <> rt_old[0] or rdt != rdt_old):
                        delta, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if delta >= 10:
                            if d > 0:
                                now_d = d * 24 * 6
                            before_h = int(rt_old[0]) * 6
                            before_m = int(rt_old[1][:1])
                            now_h = int(rt[0]) * 6
                            now_m = int(rt[1][:1])
                            if now_h < before_h:
                                now_h += 24 * 6
                            now = now_d + now_h + now_m
                            before = before_h + before_m
                            #if now-before-1 > 0:
                            #    print now-before-1
                            #    print row_old[0], row[0]
                            diff = int(now-before)
                            for i in range(diff-1):
                               data.append('null')
                        diff = 0
                        if rd == 0.0:
                            data.append('null')
                        else:
                            data.append(rd)
                    elif not bFirstDone:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s >= 2 * pointI:
                            for i in range(int((sedt[0] - s)/pointI)-1):
                                data.append('null')
                        if rd == 0.0:
                            data.append('null')
                        else:
                            data.append(rd)
                        bFirstDone = True
                    rt_old = rt
                    rdt_old = rdt
                    row_old = row
                series['name'] = str(key.encode('utf-8'))
                series['data'] = data
                series_list.append(series)
                lgth = len(data)
            else:
                print "No data found during specified range for", key
        
        if len(drows)>0 and lgth>0:
            data = []
            series = {}
            for i in range (0, lgth):
                data.append(79.0)
            series['name'] = 'UpLevel'
            series['data'] = data
            series_list.append(series)
            data = []
            series = {}
            for i in range (0, lgth):
                data.append(81.0)
            series['name'] = 'DownLevel'
            series['data'] = data
            series_list.append(series)
            logstr += HighchartLightSnippet_10('spline', titles, titles, vsuffix, series_list, pointStart)

    return logstr


def MakeLightChart(drows, pos, titles, vsuffix):
    logstr = ""
    series_list = []
    data = []
    selectedPeriod = '... - ...'
    sedt = [0, 999999, '', '']
    lgth = 0
    d1 = datetime.now()

    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                rows = drows[key]
                start, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                )
                end, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[-1][0][:-3]), '%Y-%m-%d %H:%M')
                )
                if start > sedt[0]:
                    sedt[0] = start
                    sedt[2] = str(rows[0][0][:-3])
                if end <= sedt[1]:
                    sedt[1] = end
                    sedt[3] = str(rows[-1][0][:-3])
                selectedPeriod = sedt[2]+' - '+sedt[3]
                pD = sedt[2].split(' ')[0].split('-')
                pT = sedt[2].split(' ')[1].split(':')
                pointStart = pD + pT
    
    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                # convert the data into a table
                data = []
                series = {}
                rows = drows[key]
                diff = 0
                bFirstDone = False
                for row in rows:
                    rd = float("%.2f" % row[pos])
                    rd = rd*10.0 + 60.0
                    rt = row[0][:-3].split(' ')[1].split(':')
                    if bFirstDone:
                        diff, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if diff > 0:
                            #rd_old = float("%.2f" % row_old[pos])
                            #rd_old = rd_old*10.0 + 60.0
                            for i in range(diff-1):
                                data.append('null')
                            diff = 0
                            data.append(rd)
                    else:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s > 0:
                            for i in range(sedt[0] - s):
                                data.append('null') 
                        data.append(rd)
                        bFirstDone = True
                    rt_old = rt
                    row_old = row
                series['name'] = str(key.encode('utf-8'))
                series['data'] = data
                series_list.append(series)
                lgth = len(data)
            else:
                print "No data found during specified range for", key
        
        if len(drows)>0 and lgth>0:
            data = []
            series = {}
            for i in range (0, lgth):
                data.append(79.0)
            series['name'] = 'UpLevel'
            series['data'] = data
            series_list.append(series)
            data = []
            series = {}
            for i in range (0, lgth):
                data.append(81.0)
            series['name'] = 'DownLevel'
            series['data'] = data
            series_list.append(series)
            #logstr += "<p><small>Selected period: "+selectedPeriod+"</small></p>"+'\n\r'
            logstr += HighchartLightSnippet('spline', titles, titles, vsuffix, series_list, pointStart)

    return logstr


def MakeDewPointChart_10(drows, pos, titles, vsuffix):
    logstr = ""
    series_list = []
    data = []
    sedt = [0, 999999, '', '']
    lgth = 0
    d1 = datetime.now()

    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                rows = drows[key]
                start, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                )
                end, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[-1][0][:-3]), '%Y-%m-%d %H:%M')
                )
                if start > sedt[0]:
                    sedt[0] = start
                    sedt[2] = str(rows[0][0][:-3])
                if end <= sedt[1]:
                    sedt[1] = end
                    sedt[3] = str(rows[-1][0][:-3])
                selectedPeriod = sedt[2]+' - '+sedt[3]
                pD = sedt[2].split(' ')[0].split('-')
                pT = sedt[2].split(' ')[1].split(':')
                pointStart = pD + pT
        
    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                # convert the data into a table
                data = []
                series = {}
                rows = drows[key]
                bFirstDone = False

                for row in rows:
                    rd = row[pos]
                    rt = row[0][:-3].split(' ')[1].split(':')
                    diff = 0
                    now_d =0
                    rdt = row[0][:-3].split(' ')[0].split('-')
                    if bFirstDone and (rt[1][:1] <> rt_old[1][:1] or rt[0] <> rt_old[0] or rdt != rdt_old):
                        delta, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if delta >= 10:
                            if d > 0:
                                now_d = d * 24 * 6
                            before_h = int(rt_old[0]) * 6
                            before_m = int(rt_old[1][:1])
                            now_h = int(rt[0]) * 6
                            now_m = int(rt[1][:1])
                            if now_h < before_h:
                                now_h += 24 * 6
                            now = now_d + now_h + now_m
                            before = before_h + before_m
                            #if now-before-1 > 0:
                            #    print now-before-1
                            #    print row_old[0], row[0]
                            diff = int(now-before)
                            for i in range(diff-1):
                               data.append('null')
                        diff = 0
                        if rd == 0.0:
                            data.append('null')
                        else:
                            data.append(rd)
                    elif not bFirstDone:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s >= 2 * pointI:
                            for i in range(int((sedt[0] - s)/pointI)-1):
                                data.append('null')
                        if rd == 0.0:
                            data.append('null')
                        else:
                            data.append(rd)
                        bFirstDone = True
                    rt_old = rt
                    rdt_old = rdt
                    row_old = row
                series['name'] = str(key.encode('utf-8'))
                series['data'] = data
                series_list.append(series)
                lgth = len(data)
            else:
                print "No data found during specified range for", key
    
        if len(drows)>0 and lgth>0:
            #logstr += "<p><small>Selected period: "+selectedPeriod+"</small></p>"+'\n\r'
            logstr += HighchartSnippet_10('spline', titles, titles, vsuffix, series_list, pointStart)

    return logstr
    

def MakeDewPointChart(drows, pos, titles, vsuffix):
    logstr = ""
    series_list = []
    data = []
    selectedPeriod = '... - ...'
    sedt = [0, 999999, '', '']
    lgth = 0
    d1 = datetime.now()

    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                rows = drows[key]
                start, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                )
                end, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[-1][0][:-3]), '%Y-%m-%d %H:%M')
                )
                if start > sedt[0]:
                    sedt[0] = start
                    sedt[2] = str(rows[0][0][:-3])
                if end <= sedt[1]:
                    sedt[1] = end
                    sedt[3] = str(rows[-1][0][:-3])
                selectedPeriod = sedt[2]+' - '+sedt[3]
                pD = sedt[2].split(' ')[0].split('-')
                pT = sedt[2].split(' ')[1].split(':')
                pointStart = pD + pT
        
    if len(drows)>0:
        for key in drows:
            if len(drows[key]) != 0:
                # convert the data into a table
                data = []
                series = {}
                rows = drows[key]
                diff = 0
                bFirstDone = False
                for row in rows:
                    rd = row[pos]
                    rt = row[0][:-3].split(' ')[1].split(':')
                    if bFirstDone:
                        diff, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if diff > 0:
                            #rd_old = row_old[pos]
                            for i in range(diff-1):
                                data.append('null')
                            diff = 0
                            data.append(rd)
                    else:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s > 0:
                            for i in range(sedt[0] - s):
                                data.append('null') 
                        data.append(rd)
                        bFirstDone = True
                    rt_old = rt
                    row_old = row
                series['name'] = str(key.encode('utf-8'))
                series['data'] = data
                series_list.append(series)
                lgth = len(data)
            else:
                print "No data found during specified range for", key
    
        if len(drows)>0 and lgth>0:
            #logstr += "<p><small>Selected period: "+selectedPeriod+"</small></p>"+'\n\r'
            logstr += HighchartSnippet('spline', titles, titles, vsuffix, series_list, pointStart)

    return logstr
    

def MakeWindChart_10(drows, pos, titles, vsuffix):
    logstr = ""
    series = {}
    series_list = []
    sedt = [0, 999999, '', '']
    lgth = 0
    d1 = datetime.now()
        
    if len(drows)>0:
        for key in drows:
            if (drows[key]) <> None:
                rows = drows[key]
                start, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                )
                end, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[-1][0][:-3]), '%Y-%m-%d %H:%M')
                )
                if start > sedt[0]:
                    sedt[0] = start
                    sedt[2] = str(rows[0][0][:-3])
                if end <= sedt[1]:
                    sedt[1] = end
                    sedt[3] = str(rows[-1][0][:-3])
                pD = sedt[2].split(' ')[0].split('-')
                pT = sedt[2].split(' ')[1].split(':')
                pointStart = pD + pT

    if len(drows)>0:
        for key in drows:
            if (drows[key]) <> None:
                # convert the data into tables
                tableId = str(key.encode('utf-8'))
                data = []
                series = {}
                rows = drows[key]
                bFirstDone = False
                for row in rows:
                    rgus = float("%.2f" % row[5])
                    rt = row[0][:-3].split(' ')[1].split(':')
                    diff = 0
                    now_d =0
                    rdt = row[0][:-3].split(' ')[0].split('-')
                    if bFirstDone and (rt[1][:1] <> rt_old[1][:1] or rt[0] <> rt_old[0] or rdt != rdt_old):
                        delta, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if delta >= 10:
                            if d > 0:
                                now_d = d * 24 * 6
                            before_h = int(rt_old[0]) * 6
                            before_m = int(rt_old[1][:1])
                            now_h = int(rt[0]) * 6
                            now_m = int(rt[1][:1])
                            if now_h < before_h:
                                now_h += 24 * 6
                            now = now_d + now_h + now_m
                            before = before_h + before_m
                            #if now-before-1 > 0:
                            #    print now-before-1
                            #    print row_old[0], row[0]
                            diff = int(now-before)
                            for i in range(diff-1):
                               data.append('null')
                        diff = 0
                        data.append(rgus)
                    elif not bFirstDone:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s >= 2 * pointI:
                            for i in range(int((sedt[0] - s)/pointI)-1):
                                data.append('null')
                        data.append(rgus)
                        bFirstDone = True
                    rt_old = rt
                    rdt_old = rdt
                    row_old = row
                series['name'] = tableId
                series['data'] = data
                series_list.append(series)
                lgth = len(data)
            elif (drows[key]) <> None:
                print "No data found during specified range for", key
        
        if len(drows)>0 and lgth>0:
            logstr += HighchartWindSnippet_10('column', tableId, titles, vsuffix, series_list, pointStart)

    return logstr


def MakeWindChart(drows, pos, titles, vsuffix):
    logstr = ""
    series = {}
    series_list = []
    selectedPeriod = '... - ...'
    sedt = [0, 999999, '', '']
    lgth = 0
    d1 = datetime.now()
        
    if len(drows)>0:
        for key in drows:
            if (drows[key]) <> None:
                rows = drows[key]
                start, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                )
                end, d = days_hours_minutes(
                    d1 -
                    datetime.strptime(str(rows[-1][0][:-3]), '%Y-%m-%d %H:%M')
                )
                if start > sedt[0]:
                    sedt[0] = start
                    sedt[2] = str(rows[0][0][:-3])
                if end <= sedt[1]:
                    sedt[1] = end
                    sedt[3] = str(rows[-1][0][:-3])
                selectedPeriod = sedt[2]+' - '+sedt[3]
                pD = sedt[2].split(' ')[0].split('-')
                pT = sedt[2].split(' ')[1].split(':')
                pointStart = pD + pT

    if len(drows)>0:
        for key in drows:
            if (drows[key]) <> None:
                # convert the data into tables
                tableId = str(key.encode('utf-8'))
                data = []
                series = {}
                rows = drows[key]
                diff = 0
                bFirstDone = False
                for row in rows:
                    rgus = float("%.2f" % row[5])
                    rt = row[0][:-3].split(' ')[1].split(':')
                    if bFirstDone:
                        diff, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if diff > 0:
                            rgus_old = float("%.2f" % row_old[5])
                            for i in range(diff-1):
                               data.append('null')
                            data.append(rgus)

                            diff = 0
                    else:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s > 0:
                            for i in range(sedt[0] - s):
                                data.append('null') 
                        data.append(rgus)
                        bFirstDone = True
                    rt_old = rt
                    row_old = row
                series['name'] = tableId
                series['data'] = data
                series_list.append(series)
                lgth = len(data)
            elif (drows[key]) <> None:
                print "No data found during specified range for", key
        
        if len(drows)>0 and lgth>0:
            #logstr += "<p><small>Selected period: "+selectedPeriod+"</small></p>"+'\n\r'
            logstr += HighchartWindSnippet('column', tableId, titles, vsuffix, series_list, pointStart)

    return logstr


def CreateComboHtml(
    rprtName, 
    dataType, 
    fPath, 
    rows_1, 
    titles_1, 
    pos_1, 
    rows_2, 
    titles_2, 
    pos_2, 
    rows_3, 
    titles_3, 
    pos_3, 
    rows_4, 
    titles_4, 
    pos_4,
    rows_5, 
    titles_5, 
    pos_5,
    rows_6, 
    titles_6, 
    pos_6,
    rprtTitle,
    rprtHeading,
    tenMinutes
):
    # start creating the html page
    base_1 = """
    <script type="text/javascript">
    function GoBack(){
        history.back();
    }
    </script>
    <!DOCTYPE HTML><html><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link rel="stylesheet" type="text/css" href="CDC.css">
    <title>"""
    base_2 = """</title>
    <div id="Heading">
    <h1>"""
    base_3 = """</h1>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <body>
    <script src="js/highcharts.js"></script>
    <script src="js/modules/exporting.js"></script>
   	</body>
    </html>
    <div id="Button"><td><button onMouseDown=GoBack() style="background-color:white; height:40px; width:250px">Back to previous page</button></td></div>
    """
 
    if tenMinutes:
        logstr = MakeChart_10(rows_1, pos_1, 'Temperature', ' degrees C')
    else:
        logstr = MakeChart(rows_1, pos_1, 'Temperature', ' degrees C')
    if tenMinutes:
        logstr += MakeChart_10(rows_2, pos_2, 'Humidity', ' percent RH')
    else:
        logstr += MakeChart(rows_2, pos_2, 'Humidity', ' percent RH')
    if tenMinutes:
        logstr += MakeWindChart_10(rows_6, pos_6, 'Wind gust', ' m/s')
    else:
        logstr += MakeWindChart(rows_6, pos_6, 'Wind gust', ' m/s')
    if tenMinutes:
        logstr += MakeRainChart_10(rows_3, pos_3, 'Rain level', ' mm')
    else:
        logstr += MakeRainChart(rows_3, pos_3, 'Rain level', ' mm')
    if tenMinutes:
        logstr += MakeLightChart_10(rows_4, pos_4, 'Light level', ' pts')
    else:
        logstr += MakeLightChart(rows_4, pos_4, 'Light level', ' pts')
    if tenMinutes:
        logstr += MakeDewPointChart_10(rows_5, pos_5, 'Dewpoint delta', ' degrees C')
    else:
        logstr += MakeDewPointChart(rows_5, pos_5, 'Dewpoint delta', ' degrees C')
    logstr = base_1 + rprtTitle + base_2 + rprtHeading + base_3 + logstr 

    fName = rprtName+'.html'
    fileHandle = None
    if not os.path.exists(fPath) and not os.path.isdir(fPath):
        os.makedirs(fPath)
    fileHandle = open(fPath+'/'+fName, 'a')
    fileHandle.seek(0)
    fileHandle.truncate()
    fileHandle.write(logstr.encode('utf-8'))
    fileHandle.close()
    del logstr
    reload(css)
    #print css.content
    fName = 'CDC.css'
    if not os.path.exists(fPath+'/'+fName):
        fileHandle = open(fPath+'/'+fName, 'w')
        fileHandle.write(css.content.encode('utf-8'))
        fileHandle.close()

 
def HighchartWindSnippet(typ, tableId, titles, vsuffix, series, pointStart):
    c_code_0 = """
    <div id="Wind_gust"></div>"""
    c_code_1 = """
    <script type="text/javascript">
    $(function () {
    $('#Wind_gust'"""
    c_code_1_2 = """).highcharts({
    chart: {
    type: '"""
    c_code_1_3 = typ
    c_code_1_4 = """',
    zoomType: 'x',
    panning: true,
    panKey: 'shift'
    },
    title: {
    text: '"""
    c_code_2 = ''
    c_code_3_1 = """',
    x: -20
    },
    xAxis: {
    type: "datetime"
    },
    plotOptions: {
    series: {
    pointStart: Date.UTC("""
    c_code_3_2_1 = str(int(pointStart[0]))
    c_code_3_2_2 = ','
    c_code_3_2_3 = str(int(pointStart[1])-1)
    c_code_3_2_4 = ','
    c_code_3_2_5 = str(int(pointStart[2]))
    c_code_3_2_6 = ','
    c_code_3_2_7 = str(int(pointStart[3]))
    c_code_3_2_8 = ','
    c_code_3_2_9 = str(int(pointStart[4]))
    c_code_3_3 = """),
    pointInterval: 60 * 1000 // one per minute
    }
    },
    yAxis: {
    title: {
    text: '"""
    c_code_5_1 = titles
    c_code_5_2 = """'
    },
    plotOptions: {
    spline: {
    lineWidth: 4,
    states: {
    hover: {
    lineWidth: 5
    }
    },
    marker: {
    enabled: false,
    states: {
    hover: {
    enabled: true,
    symbol: 'circle',
    radius: 5,
    lineWidth: 1
    }
    }
    }
    }
    },
    gridLineWidth: 2,
    plotLines: [{
    value: 0,
    width: 1,
    color: '#808080'
    }]
    },
    tooltip: {
    valueSuffix: '"""
    c_code_5_3 = vsuffix
    c_code_5_4 = """'
    },
    legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle',
    borderWidth: 0
    },
    series: """
    c_code_6 = str(series).replace("'data':", "data:")
    c_code_6 = c_code_6.replace("'name':", "name:")
    c_code_6 = c_code_6.replace("'null'", "null")
    c_code_7 = """
    });
    });
    </script>
    """    
    
    c_code = (
        c_code_0+
        c_code_1+
        c_code_1_2+
        c_code_1_3+
        c_code_1_4+
        c_code_2+
        c_code_3_1+
        c_code_3_2_1+
        c_code_3_2_2+
        c_code_3_2_3+
        c_code_3_2_4+
        c_code_3_2_5+
        c_code_3_2_6+
        c_code_3_2_7+
        c_code_3_2_8+
        c_code_3_2_9+
        c_code_3_3+
        c_code_5_1+
        c_code_5_2+
        c_code_5_3+
        c_code_5_4+
        c_code_6+
        c_code_7
    )
    return c_code
    

def HighchartWindSnippet_10(typ, tableId, titles, vsuffix, series, pointStart):
    c_code_0 = """
    <div id="Wind_gust"></div>"""
    c_code_1 = """
    <script type="text/javascript">
    $(function () {
    $('#Wind_gust'"""
    c_code_1_2 = """).highcharts({
    chart: {
    type: '"""
    c_code_1_3 = typ
    c_code_1_4 = """',
    zoomType: 'x',
    panning: true,
    panKey: 'shift'
    },
    title: {
    text: '"""
    c_code_2 = ''
    c_code_3_1 = """',
    x: -20
    },
    xAxis: {
    type: "datetime"
    },
    plotOptions: {
    series: {
    pointStart: Date.UTC("""
    c_code_3_2_1 = str(int(pointStart[0]))
    c_code_3_2_2 = ','
    c_code_3_2_3 = str(int(pointStart[1])-1)
    c_code_3_2_4 = ','
    c_code_3_2_5 = str(int(pointStart[2]))
    c_code_3_2_6 = ','
    c_code_3_2_7 = str(int(pointStart[3]))
    c_code_3_2_8 = ','
    c_code_3_2_9 = str(int(pointStart[4]))
    c_code_3_3 = """),
    pointInterval: 600 * 1000 // one per 10 minute
    }
    },
    yAxis: {
    title: {
    text: '"""
    c_code_5_1 = titles
    c_code_5_2 = """'
    },
    plotOptions: {
    spline: {
    lineWidth: 4,
    states: {
    hover: {
    lineWidth: 5
    }
    },
    marker: {
    enabled: false,
    states: {
    hover: {
    enabled: true,
    symbol: 'circle',
    radius: 5,
    lineWidth: 1
    }
    }
    }
    }
    },
    gridLineWidth: 2,
    plotLines: [{
    value: 0,
    width: 1,
    color: '#808080'
    }]
    },
    tooltip: {
    valueSuffix: '"""
    c_code_5_3 = vsuffix
    c_code_5_4 = """'
    },
    legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle',
    borderWidth: 0
    },
    series: """
    c_code_6 = str(series).replace("'data':", "data:")
    c_code_6 = c_code_6.replace("'name':", "name:")
    c_code_6 = c_code_6.replace("'null'", "null")
    c_code_7 = """
    });
    });
    </script>
    """    
    
    c_code = (
        c_code_0+
        c_code_1+
        c_code_1_2+
        c_code_1_3+
        c_code_1_4+
        c_code_2+
        c_code_3_1+
        c_code_3_2_1+
        c_code_3_2_2+
        c_code_3_2_3+
        c_code_3_2_4+
        c_code_3_2_5+
        c_code_3_2_6+
        c_code_3_2_7+
        c_code_3_2_8+
        c_code_3_2_9+
        c_code_3_3+
        c_code_5_1+
        c_code_5_2+
        c_code_5_3+
        c_code_5_4+
        c_code_6+
        c_code_7
    )
    return c_code
    

def HighchartLightSnippet(typ, tableId, titles, vsuffix, series, pointStart):
    c_code_0 = """
    <div id="Light_level"></div>"""
    c_code_1 = """
    <script type="text/javascript">
    $(function () {
    $('#Light_level'"""
    c_code_1_2 = """).highcharts({
    chart: {
    type: '"""
    c_code_1_3 = typ
    c_code_1_4 = """',
    zoomType: 'x',
    panning: true,
    panKey: 'shift'
    },
    title: {
    text: '"""
    c_code_2 = ''
    c_code_3_1 = """',
    x: -20
    },
    xAxis: {
    type: "datetime"
    },
    plotOptions: {
    series: {
    pointStart: Date.UTC("""
    c_code_3_2_1 = str(int(pointStart[0]))
    c_code_3_2_2 = ','
    c_code_3_2_3 = str(int(pointStart[1])-1)
    c_code_3_2_4 = ','
    c_code_3_2_5 = str(int(pointStart[2]))
    c_code_3_2_6 = ','
    c_code_3_2_7 = str(int(pointStart[3]))
    c_code_3_2_8 = ','
    c_code_3_2_9 = str(int(pointStart[4]))
    c_code_3_3 = """),
    pointInterval: 60 * 1000 // one per minute
    }
    },
    yAxis: {
    title: {
    text: '"""
    c_code_5_1 = titles
    c_code_5_2 = """'
    },
    plotOptions: {
    spline: {
    lineWidth: 4,
    states: {
    hover: {
    lineWidth: 5
    }
    },
    marker: {
    enabled: false,
    states: {
    hover: {
    enabled: true,
    symbol: 'circle',
    radius: 5,
    lineWidth: 1
    }
    }
    }
    }
    },
    gridLineWidth: 2,
    plotLines: [{
    value: 0,
    width: 1,
    color: '#808080'
    }],
    },
    tooltip: {
    valueSuffix: '"""
    c_code_5_3 = vsuffix
    c_code_5_4 = """'
    },
    legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle',
    borderWidth: 0
    },
    series: """
    c_code_6 = str(series).replace("'data':", "data:")
    c_code_6 = c_code_6.replace("'name':", "name:")
    c_code_6 = c_code_6.replace("'null'", "null")
    c_code_7 = """
    });
    });
    </script>
    """    
    
    c_code = (
        c_code_0+
        c_code_1+
        c_code_1_2+
        c_code_1_3+
        c_code_1_4+
        c_code_2+
        c_code_3_1+
        c_code_3_2_1+
        c_code_3_2_2+
        c_code_3_2_3+
        c_code_3_2_4+
        c_code_3_2_5+
        c_code_3_2_6+
        c_code_3_2_7+
        c_code_3_2_8+
        c_code_3_2_9+
        c_code_3_3+
        c_code_5_1+
        c_code_5_2+
        c_code_5_3+
        c_code_5_4+
        c_code_6+
        c_code_7
    )
    return c_code


def HighchartLightSnippet_10(typ, tableId, titles, vsuffix, series, pointStart):
    c_code_0 = """
    <div id="Light_level"></div>"""
    c_code_1 = """
    <script type="text/javascript">
    $(function () {
    $('#Light_level'"""
    c_code_1_2 = """).highcharts({
    chart: {
    type: '"""
    c_code_1_3 = typ
    c_code_1_4 = """',
    zoomType: 'x',
    panning: true,
    panKey: 'shift'
    },
    title: {
    text: '"""
    c_code_2 = ''
    c_code_3_1 = """',
    x: -20
    },
    xAxis: {
    type: "datetime"
    },
    plotOptions: {
    series: {
    pointStart: Date.UTC("""
    c_code_3_2_1 = str(int(pointStart[0]))
    c_code_3_2_2 = ','
    c_code_3_2_3 = str(int(pointStart[1])-1)
    c_code_3_2_4 = ','
    c_code_3_2_5 = str(int(pointStart[2]))
    c_code_3_2_6 = ','
    c_code_3_2_7 = str(int(pointStart[3]))
    c_code_3_2_8 = ','
    c_code_3_2_9 = str(int(pointStart[4]))
    c_code_3_3 = """),
    pointInterval: 600 * 1000 // one per 10 minute
    }
    },
    yAxis: {
    title: {
    text: '"""
    c_code_5_1 = titles
    c_code_5_2 = """'
    },
    plotOptions: {
    spline: {
    lineWidth: 4,
    states: {
    hover: {
    lineWidth: 5
    }
    },
    marker: {
    enabled: false,
    states: {
    hover: {
    enabled: true,
    symbol: 'circle',
    radius: 5,
    lineWidth: 1
    }
    }
    }
    }
    },
    gridLineWidth: 2,
    plotLines: [{
    value: 0,
    width: 1,
    color: '#808080'
    }],
    },
    tooltip: {
    valueSuffix: '"""
    c_code_5_3 = vsuffix
    c_code_5_4 = """'
    },
    legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle',
    borderWidth: 0
    },
    series: """
    c_code_6 = str(series).replace("'data':", "data:")
    c_code_6 = c_code_6.replace("'name':", "name:")
    c_code_6 = c_code_6.replace("'null'", "null")
    c_code_7 = """
    });
    });
    </script>
    """    
    
    c_code = (
        c_code_0+
        c_code_1+
        c_code_1_2+
        c_code_1_3+
        c_code_1_4+
        c_code_2+
        c_code_3_1+
        c_code_3_2_1+
        c_code_3_2_2+
        c_code_3_2_3+
        c_code_3_2_4+
        c_code_3_2_5+
        c_code_3_2_6+
        c_code_3_2_7+
        c_code_3_2_8+
        c_code_3_2_9+
        c_code_3_3+
        c_code_5_1+
        c_code_5_2+
        c_code_5_3+
        c_code_5_4+
        c_code_6+
        c_code_7
    )
    return c_code


def HighchartSnippet(typ, tableId, titles, vsuffix, series, pointStart):
    c_code_0 = """<br>
    <div id='"""
    c_code_0_1 = titles.replace(' ', '_')
    c_code_0_2 = """' style="min-width: 1000px; height: 450px; margin: 0 auto"></div>"""
    c_code_1 = """
    <script type="text/javascript">
    $(function () {
    $('#"""
    c_code_1_1 = titles.replace(' ', '_')
    c_code_1_2 = """').highcharts({
    chart: {
    type: '"""
    c_code_1_3 = typ
    c_code_1_4 = """',
    zoomType: 'x',
    panning: true,
    panKey: 'shift'
    },
    title: {
    text: '"""
    c_code_2 = ''
    c_code_3_1 = """',
    x: -20
    },
    xAxis: {
    type: "datetime"
    },
    plotOptions: {
    series: {
    pointStart: Date.UTC("""
    c_code_3_2_1 = str(int(pointStart[0]))
    c_code_3_2_2 = ','
    c_code_3_2_3 = str(int(pointStart[1])-1)
    c_code_3_2_4 = ','
    c_code_3_2_5 = str(int(pointStart[2]))
    c_code_3_2_6 = ','
    c_code_3_2_7 = str(int(pointStart[3]))
    c_code_3_2_8 = ','
    c_code_3_2_9 = str(int(pointStart[4]))
    c_code_3_3 = """),
    pointInterval: 60 * 1000 // one per minute
    }
    },
    yAxis: {
    title: {
    text: '"""
    c_code_5_1 = titles
    c_code_5_2 = """'
    },
    plotOptions: {
    spline: {
    lineWidth: 4,
    states: {
    hover: {
    lineWidth: 5
    }
    },
    marker: {
    enabled: false,
    states: {
    hover: {
    enabled: true,
    symbol: 'circle',
    radius: 5,
    lineWidth: 1
    }
    }
    }
    }
    },
    gridLineWidth: 2,
    plotLines: [{
    value: 0,
    width: 1,
    color: '#808080'
    }]
    },
    tooltip: {
    valueSuffix: '"""
    c_code_5_3 = vsuffix
    c_code_5_4 = """'
    },
    legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle',
    borderWidth: 0
    },
    series: """
    c_code_6 = str(series).replace("'data':", "data:")
    c_code_6 = c_code_6.replace("'name':", "name:")
    c_code_6 = c_code_6.replace("'null'", "null")
    c_code_7 = """
    });
    });
    </script>
    """    
    
    c_code = (
        c_code_0+
        c_code_0_1+
        c_code_0_2+
        c_code_1+
        c_code_1_1+
        c_code_1_2+
        c_code_1_3+
        c_code_1_4+
        c_code_2+
        c_code_3_1+
        c_code_3_2_1+
        c_code_3_2_2+
        c_code_3_2_3+
        c_code_3_2_4+
        c_code_3_2_5+
        c_code_3_2_6+
        c_code_3_2_7+
        c_code_3_2_8+
        c_code_3_2_9+
        c_code_3_3+
        c_code_5_1+
        c_code_5_2+
        c_code_5_3+
        c_code_5_4+
        c_code_6+
        c_code_7
    )
    return c_code


def HighchartSnippet_10(typ, tableId, titles, vsuffix, series, pointStart):
    c_code_0 = """<br>
    <div id='"""
    c_code_0_1 = titles.replace(' ', '_')
    c_code_0_2 = """' style="min-width: 1000px; height: 450px; margin: 0 auto"></div>"""
    c_code_1 = """
    <script type="text/javascript">
    $(function () {
    $('#"""
    c_code_1_1 = titles.replace(' ', '_')
    c_code_1_2 = """').highcharts({
    chart: {
    type: '"""
    c_code_1_3 = typ
    c_code_1_4 = """',
    zoomType: 'x',
    panning: true,
    panKey: 'shift'
    },
    title: {
    text: '"""
    c_code_2 = ''
    c_code_3_1 = """',
    x: -20
    },
    xAxis: {
    type: "datetime"
    },
    plotOptions: {
    series: {
    pointStart: Date.UTC("""
    c_code_3_2_1 = str(int(pointStart[0]))
    c_code_3_2_2 = ','
    c_code_3_2_3 = str(int(pointStart[1])-1)
    c_code_3_2_4 = ','
    c_code_3_2_5 = str(int(pointStart[2]))
    c_code_3_2_6 = ','
    c_code_3_2_7 = str(int(pointStart[3]))
    c_code_3_2_8 = ','
    c_code_3_2_9 = str(int(pointStart[4]))
    c_code_3_3 = """),
    pointInterval: 600 * 1000 // one per 10 minute
    }
    },
    yAxis: {
    title: {
    text: '"""
    c_code_5_1 = titles
    c_code_5_2 = """'
    },
    plotOptions: {
    spline: {
    lineWidth: 4,
    states: {
    hover: {
    lineWidth: 5
    }
    },
    marker: {
    enabled: false,
    states: {
    hover: {
    enabled: true,
    symbol: 'circle',
    radius: 5,
    lineWidth: 1
    }
    }
    }
    }
    },
    gridLineWidth: 2,
    plotLines: [{
    value: 0,
    width: 1,
    color: '#808080'
    }]
    },
    tooltip: {
    valueSuffix: '"""
    c_code_5_3 = vsuffix
    c_code_5_4 = """'
    },
    legend: {
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'middle',
    borderWidth: 0
    },
    series: """
    c_code_6 = str(series).replace("'data':", "data:")
    c_code_6 = c_code_6.replace("'name':", "name:")
    c_code_6 = c_code_6.replace("'null'", "null")
    c_code_7 = """
    });
    });
    </script>
    """    
    
    c_code = (
        c_code_0+
        c_code_0_1+
        c_code_0_2+
        c_code_1+
        c_code_1_1+
        c_code_1_2+
        c_code_1_3+
        c_code_1_4+
        c_code_2+
        c_code_3_1+
        c_code_3_2_1+
        c_code_3_2_2+
        c_code_3_2_3+
        c_code_3_2_4+
        c_code_3_2_5+
        c_code_3_2_6+
        c_code_3_2_7+
        c_code_3_2_8+
        c_code_3_2_9+
        c_code_3_3+
        c_code_5_1+
        c_code_5_2+
        c_code_5_3+
        c_code_5_4+
        c_code_6+
        c_code_7
    )
    return c_code




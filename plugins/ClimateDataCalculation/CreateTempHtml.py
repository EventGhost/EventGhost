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
                data_ref = []
                series = {}
                series_ref = {}
                rows = drows[key]
                bFirstDone = False
                for row in rows:
                    rd = float("%.2f" % row[pos])
                    rt = row[0][:-3].split(' ')[1].split(':')
                    diff = 0
                    now_d =0
                    rdt = row[0][:-3].split(' ')[0].split('-')
                    ref_t = (row[5]+row[6])/2
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
                               data_ref.append(ref_t)
                        diff = 0
                        if rd == 0.0:
                            data.append('null')
                            data_ref.append(ref_t)
                        else:
                            data.append(rd)
                            data_ref.append(ref_t)
                    elif not bFirstDone:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s >= 2 * pointI:
                            for i in range(int((sedt[0] - s)/pointI)-1):
                                data.append('null')
                                data_ref.append(ref_t)
                        if rd == 0.0:
                            data.append('null')
                            data_ref.append(ref_t)
                        else:
                            data.append(rd)
                            data_ref.append(ref_t)
                        bFirstDone = True
                    rt_old = rt
                    rdt_old = rdt
                    row_old = row

                series['name'] = tableId
                series['data'] = data
                series_list.append(series)
                series_ref['name'] = tableId+'_setpoint'
                series_ref['data'] = data_ref
                series_list.append(series_ref)
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
                data_ref = []
                series_ref = {}
                rows = drows[key]
                diff = 0
                bFirstDone = False
                for row in rows:
                    rd = float("%.2f" % row[pos])
                    ref_t = (row[5]+row[6])/2
                    if bFirstDone:
                        diff, d = days_hours_minutes(
                            datetime.strptime(str(row[0][:-3]), '%Y-%m-%d %H:%M') -
                            datetime.strptime(str(row_old[0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if diff > 0:
                            for i in range(diff-1):
                                data.append('null')
                                data_ref.append(ref_t)
                            diff = 0
                            if rd == 0.0:
                                data.append('null')
                                data_ref.append(ref_t)
                            else:
                                data.append(rd)
                                data_ref.append(ref_t)
                    else:
                        s, d = days_hours_minutes(
                            d1 -
                            datetime.strptime(str(rows[0][0][:-3]), '%Y-%m-%d %H:%M')
                        )
                        if sedt[0] - s > 0:
                            for i in range(sedt[0] - s):
                                data.append('null') 
                                data_ref.append(ref_t)
                        data.append(rd)
                        data_ref.append(ref_t)
                        bFirstDone = True
                    row_old = row
                series['name'] = tableId
                series['data'] = data
                series_list.append(series)
                series_ref['name'] = tableId+'_setpoint'
                series_ref['data'] = data_ref
                series_list.append(series_ref)
                lgth = len(data)
            else:
                print "No data found during specified range for", key
        
        if len(drows)>0 and lgth>0:
            #logstr += "<p><small>Selected period: "+selectedPeriod+"</small></p>"+'\n\r'
            logstr += HighchartSnippet('spline', tableId, titles, vsuffix, series_list, pointStart)

    return logstr


def CreateTempHtml(
    rprtName, 
    dataType, 
    fPath, 
    rows_1, 
    titles_1, 
    pos_1, 
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
    <br>
    <br> """

    if tenMinutes:
        logstr = MakeChart_10(rows_1, pos_1, 'Temperature', ' degrees C')
    else:
        logstr = MakeChart(rows_1, pos_1, 'Temperature', ' degrees C')
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


def HighchartSnippet(typ, tableId, titles, vsuffix, series, pointStart):
    c_code_0 = """
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
    c_code_0 = """
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




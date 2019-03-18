# -*- coding: utf-8 -*-
import os
import rose
from datetime import datetime, timedelta
import css


pointI = 10


def days_hours_minutes(td):
    m = td.days * 24 *60
    m += td.seconds//60
    return int(m), int(td.days)


def CreateWindRoseHtml(
    rprtName, 
    fPath, 
    rows, 
    rprtTitle,
    rprtHeading,
    tenMinutes
):
    # start creating the html page
    base_1 = """
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
    </html> """
  
    logstr = ''
    logstr += MakeWindRoseChart(rows)
    if tenMinutes:
        logstr += MakeWindChart_10(rows, 0, 'Wind gust', 'm/s')
    else:
        logstr += MakeWindChart(rows, 0, 'Wind gust', 'm/s')
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


def MakeWindRoseChart(drows):
    reload(rose)
    directions = rose.directions
    logstr = ""
    series_list = []
    if len(drows)>0:
        for key in drows:
            if (drows[key]) <> None:
                tableId = str(key.encode('utf-8'))
                d_data = {}
                s_data = {
                    'N':[0,0,0,0,0,0,0],
                    'NNE':[0,0,0,0,0,0,0],
                    'NE':[0,0,0,0,0,0,0],
                    'ENE':[0,0,0,0,0,0,0],
                    'E':[0,0,0,0,0,0,0],
                    'ESE':[0,0,0,0,0,0,0],
                    'SE':[0,0,0,0,0,0,0],
                    'SSE':[0,0,0,0,0,0,0],
                    'S':[0,0,0,0,0,0,0],
                    'SSW':[0,0,0,0,0,0,0],
                    'SW':[0,0,0,0,0,0,0],
                    'WSW':[0,0,0,0,0,0,0],
                    'W':[0,0,0,0,0,0,0],
                    'WNW':[0,0,0,0,0,0,0],
                    'NW':[0,0,0,0,0,0,0],
                    'NNW':[0,0,0,0,0,0,0]
                }
                rows = drows[key]
                for row in rows:
                    rdir = str(row[3])
                    rstr = float("%.2f" % row[4])
                    if rstr < 0.5:
                        s_data[rdir][0] += 1
                    if rstr >= 0.5 and rstr < 2.0:
                        s_data[rdir][1] += 1
                    if rstr >= 2.0 and rstr < 4.0:
                        s_data[rdir][2] += 1
                    if rstr >= 4.0 and rstr < 6.0:
                        s_data[rdir][3] += 1
                    if rstr >= 6.0 and rstr < 8.0:
                        s_data[rdir][4] += 1
                    if rstr >= 8.0 and rstr < 10.0:
                        s_data[rdir][5] += 1
                    if rstr >= 10.0:
                        s_data[rdir][6] += 1
                for s in s_data:
                    s_sum = sum(s_data[s])
                    for j in s_data[s]:
                        idx = s_data[s].index(j)
                        if s_sum > 0:
                            s_data[s][idx] = (
                                float(
                                    "%.1f" % float(
                                        float(j)/float(s_sum)*100.0
                                    )
                                )
                            ) 
                series_list.append(s_data)
                #print series_list
            else:
                print "No data found during specified range for", key
        
        if len(series_list)>0:
            for item in series_list:
                logstr += HighchartWindRoseSnippet(item, directions)

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


def HighchartWindRoseSnippet(s_data, directions):
    c_code_1 = """<script type='text/javascript'>
    $(function () {
    $('#Wind_rose').highcharts({
    data: {
    table: 'freq"""
    c_code_2 = """',
    startRow: 1,
    endRow: 17,
    endColumn: 7
    },
    chart: {
    polar: true,
    type: 'column'
    },
    title: {
    text: ''"""
    c_code_3 = """},
    pane: {
    size: '90%'
    },
    legend: {
    align: 'right',
    verticalAlign: 'top',
    y: 100,
    layout: 'vertical'
    },
    xAxis: {
    tickmarkPlacement: 'on'
    },
    yAxis: {
    min: 0,
    endOnTick: false,
    showLastLabel: true,
    title: {
        text: ' (%)'
    },
    labels: {
        formatter: function () {
            return this.value + '%';
        }
    },
    reversedStacks: false
    },
    tooltip: {
    valueSuffix: ' %'
    },
    plotOptions: {
    series: {
    stacking: 'normal',
    shadow: true,
    groupPadding: 0,
    pointPlacement: 'on'
    }
    }
    });
    });
    </script></head>"""
    c_code_4 = """
    <script src="js/highcharts-more.js"></script>
    <script src="js/modules/data.js"></script>
    <script type="text/javascript">
    function GoBack(){
        history.back();
    }
    </script>
   	</body>
    </html>
    <div id="Button"><td><button onMouseDown=GoBack() style="background-color:white; height:40px; width:250px">Back to previous page</button></td></div>
    <br>
    <br>
    <div id="Wind_rose"></div>
    <div style="display:none"><table id="freq" border="0" cellspacing="0" cellpadding="0">
		<tr nowrap bgcolor="#CCCCFF">
		<th colspan="9" class="hdr">"""
    c_code_5 = """</th>
		</tr>
		<tr nowrap bgcolor="#CCCCFF">
			<th class="freq">Direction</th>
			<th class="freq">&lt; 0.5 m/s</th>
			<th class="freq">0.5-2 m/s</th>
			<th class="freq">2-4 m/s</th>
			<th class="freq">4-6 m/s</th>
			<th class="freq">6-8 m/s</th>
			<th class="freq">8-10 m/s</th>
			<th class="freq">&gt; 10 m/s</th>
			<th class="freq">Total</th>
		</tr>
		<tr nowrap>
			<td class="dir">"""+directions[0].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['N'][0])+"""</td>
      <td class="data">"""+str(s_data['N'][1])+"""</td>
      <td class="data">"""+str(s_data['N'][2])+"""</td>
      <td class="data">"""+str(s_data['N'][3])+"""</td>
      <td class="data">"""+str(s_data['N'][4])+"""</td>
      <td class="data">"""+str(s_data['N'][5])+"""</td>
      <td class="data">"""+str(s_data['N'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['N']))+"""</td>
		</tr>		
		<tr nowrap bgcolor="#DDDDDD">
			<td class="dir">"""+directions[1].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['NNE'][0])+"""</td>
      <td class="data">"""+str(s_data['NNE'][1])+"""</td>
      <td class="data">"""+str(s_data['NNE'][2])+"""</td>
      <td class="data">"""+str(s_data['NNE'][3])+"""</td>
      <td class="data">"""+str(s_data['NNE'][4])+"""</td>
      <td class="data">"""+str(s_data['NNE'][5])+"""</td>
      <td class="data">"""+str(s_data['NNE'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['NNE']))+"""</td>
		</tr>
		<tr nowrap>
			<td class="dir">"""+directions[2].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['NE'][0])+"""</td>
      <td class="data">"""+str(s_data['NE'][1])+"""</td>
      <td class="data">"""+str(s_data['NE'][2])+"""</td>
      <td class="data">"""+str(s_data['NE'][3])+"""</td>
      <td class="data">"""+str(s_data['NE'][4])+"""</td>
      <td class="data">"""+str(s_data['NE'][5])+"""</td>
      <td class="data">"""+str(s_data['NE'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['NE']))+"""</td>
		</tr>
		<tr nowrap bgcolor="#DDDDDD">
			<td class="dir">"""+directions[3].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['ENE'][0])+"""</td>
      <td class="data">"""+str(s_data['ENE'][1])+"""</td>
      <td class="data">"""+str(s_data['ENE'][2])+"""</td>
      <td class="data">"""+str(s_data['ENE'][3])+"""</td>
      <td class="data">"""+str(s_data['ENE'][4])+"""</td>
      <td class="data">"""+str(s_data['ENE'][5])+"""</td>
      <td class="data">"""+str(s_data['ENE'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['ENE']))+"""</td>
		</tr>
		<tr nowrap>
			<td class="dir">"""+directions[4].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['E'][0])+"""</td>
      <td class="data">"""+str(s_data['E'][1])+"""</td>
      <td class="data">"""+str(s_data['E'][2])+"""</td>
      <td class="data">"""+str(s_data['E'][3])+"""</td>
      <td class="data">"""+str(s_data['E'][4])+"""</td>
      <td class="data">"""+str(s_data['E'][5])+"""</td>
      <td class="data">"""+str(s_data['E'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['E']))+"""</td>
		</tr>
		<tr nowrap bgcolor="#DDDDDD">
			<td class="dir">"""+directions[5].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['ESE'][0])+"""</td>
      <td class="data">"""+str(s_data['ESE'][1])+"""</td>
      <td class="data">"""+str(s_data['ESE'][2])+"""</td>
      <td class="data">"""+str(s_data['ESE'][3])+"""</td>
      <td class="data">"""+str(s_data['ESE'][4])+"""</td>
      <td class="data">"""+str(s_data['ESE'][5])+"""</td>
      <td class="data">"""+str(s_data['ESE'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['ESE']))+"""</td>
		</tr>
		<tr nowrap>
			<td class="dir">"""+directions[6].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['SE'][0])+"""</td>
      <td class="data">"""+str(s_data['SE'][1])+"""</td>
      <td class="data">"""+str(s_data['SE'][2])+"""</td>
      <td class="data">"""+str(s_data['SE'][3])+"""</td>
      <td class="data">"""+str(s_data['SE'][4])+"""</td>
      <td class="data">"""+str(s_data['SE'][5])+"""</td>
      <td class="data">"""+str(s_data['SE'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['SE']))+"""</td>
		</tr>
		<tr nowrap bgcolor="#DDDDDD">
			<td class="dir">"""+directions[7].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['SSE'][0])+"""</td>
      <td class="data">"""+str(s_data['SSE'][1])+"""</td>
      <td class="data">"""+str(s_data['SSE'][2])+"""</td>
      <td class="data">"""+str(s_data['SSE'][3])+"""</td>
      <td class="data">"""+str(s_data['SSE'][4])+"""</td>
      <td class="data">"""+str(s_data['SSE'][5])+"""</td>
      <td class="data">"""+str(s_data['SSE'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['SSE']))+"""</td>
		</tr>
		<tr nowrap>
			<td class="dir">"""+directions[8].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['S'][0])+"""</td>
      <td class="data">"""+str(s_data['S'][1])+"""</td>
      <td class="data">"""+str(s_data['S'][2])+"""</td>
      <td class="data">"""+str(s_data['S'][3])+"""</td>
      <td class="data">"""+str(s_data['S'][4])+"""</td>
      <td class="data">"""+str(s_data['S'][5])+"""</td>
      <td class="data">"""+str(s_data['S'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['S']))+"""</td>
		</tr>
		<tr nowrap bgcolor="#DDDDDD">
			<td class="dir">"""+directions[9].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['SSW'][0])+"""</td>
      <td class="data">"""+str(s_data['SSW'][1])+"""</td>
      <td class="data">"""+str(s_data['SSW'][2])+"""</td>
      <td class="data">"""+str(s_data['SSW'][3])+"""</td>
      <td class="data">"""+str(s_data['SSW'][4])+"""</td>
      <td class="data">"""+str(s_data['SSW'][5])+"""</td>
      <td class="data">"""+str(s_data['SSW'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['SSW']))+"""</td>
		</tr>
		<tr nowrap>
			<td class="dir">"""+directions[10].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['SW'][0])+"""</td>
      <td class="data">"""+str(s_data['SW'][1])+"""</td>
      <td class="data">"""+str(s_data['SW'][2])+"""</td>
      <td class="data">"""+str(s_data['SW'][3])+"""</td>
      <td class="data">"""+str(s_data['SW'][4])+"""</td>
      <td class="data">"""+str(s_data['SW'][5])+"""</td>
      <td class="data">"""+str(s_data['SW'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['SW']))+"""</td>
		</tr>
		<tr nowrap bgcolor="#DDDDDD">
			<td class="dir">"""+directions[11].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['WSW'][0])+"""</td>
      <td class="data">"""+str(s_data['WSW'][1])+"""</td>
      <td class="data">"""+str(s_data['WSW'][2])+"""</td>
      <td class="data">"""+str(s_data['WSW'][3])+"""</td>
      <td class="data">"""+str(s_data['WSW'][4])+"""</td>
      <td class="data">"""+str(s_data['WSW'][5])+"""</td>
      <td class="data">"""+str(s_data['WSW'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['WSW']))+"""</td>
		</tr>
		<tr nowrap>
			<td class="dir">"""+directions[12].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['W'][0])+"""</td>
      <td class="data">"""+str(s_data['W'][1])+"""</td>
      <td class="data">"""+str(s_data['W'][2])+"""</td>
      <td class="data">"""+str(s_data['W'][3])+"""</td>
      <td class="data">"""+str(s_data['W'][4])+"""</td>
      <td class="data">"""+str(s_data['W'][5])+"""</td>
      <td class="data">"""+str(s_data['W'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['W']))+"""</td>
		</tr>
		<tr nowrap bgcolor="#DDDDDD">
			<td class="dir">"""+directions[13].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['WNW'][0])+"""</td>
      <td class="data">"""+str(s_data['WNW'][1])+"""</td>
      <td class="data">"""+str(s_data['WNW'][2])+"""</td>
      <td class="data">"""+str(s_data['WNW'][3])+"""</td>
      <td class="data">"""+str(s_data['WNW'][4])+"""</td>
      <td class="data">"""+str(s_data['WNW'][5])+"""</td>
      <td class="data">"""+str(s_data['WNW'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['WNW']))+"""</td>
		</tr>
		<tr nowrap>
			<td class="dir">"""+directions[14].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['NW'][0])+"""</td>
      <td class="data">"""+str(s_data['NW'][1])+"""</td>
      <td class="data">"""+str(s_data['NW'][2])+"""</td>
      <td class="data">"""+str(s_data['NW'][3])+"""</td>
      <td class="data">"""+str(s_data['NW'][4])+"""</td>
      <td class="data">"""+str(s_data['NW'][5])+"""</td>
      <td class="data">"""+str(s_data['NW'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['NW']))+"""</td>
		</tr>		
		<tr nowrap bgcolor="#DDDDDD">
			<td class="dir">"""+directions[15].decode('latin_1')+"""</td>
      <td class="data">"""+str(s_data['NNW'][0])+"""</td>
      <td class="data">"""+str(s_data['NNW'][1])+"""</td>
      <td class="data">"""+str(s_data['NNW'][2])+"""</td>
      <td class="data">"""+str(s_data['NNW'][3])+"""</td>
      <td class="data">"""+str(s_data['NNW'][4])+"""</td>
      <td class="data">"""+str(s_data['NNW'][5])+"""</td>
      <td class="data">"""+str(s_data['NNW'][6])+"""</td>
      <td class="data">"""+str(sum(s_data['NNW']))+"""</td>
		</tr>
		<tr nowrap>
			<td class="totals">Total</td>
			<td class="totals">25.53</td>
			<td class="totals">44.54</td>
			<td class="totals">15.07</td>
			<td class="totals">8.52</td>
			<td class="totals">4.31</td>
			<td class="totals">1.81</td>
			<td class="totals">0.23</td>
			<td class="totals">&nbsp;</td>
		</tr>
	  </table>
    </div>
    </body>
    </html>
    """
    c_code = (
        c_code_1+
        c_code_2+
        c_code_3+
        c_code_4+
        c_code_5
    )
    return c_code
    

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
    c_code_1_1 = """).highcharts({
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
        c_code_1_1+
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
    

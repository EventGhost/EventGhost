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


def CreateWindMiniRoseHtml(
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
    <script src="js/highcharts-more.js"></script>
    <script src="js/modules/data.js"></script>
   	</body>
    </html>
    <script>
    function GoBack(){
        history.back();
    }
    </script>
   	</body>
    </html>
    <div id="Button"><td><button onMouseDown=GoBack() style="background-color:white; height:40px; width:250px">Back to previous page</button></td></div>
    <br>
    <br> """

    logstr = ''
    logstr += MakeWindRoseChart(rows)
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
                prevdate = ''
                cntr = 0
                for row in rows:
                    date = row[0].split(' ')[0]
                    if date == prevdate or prevdate == '':
                        prevdate = date
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
                    if date != prevdate:
                        series_list.append(s_data)
                        logstr, series_list = appendAndCreate(logstr, series_list, s_data, directions, cntr, prevdate)
                        cntr += 1
                        prevdate = date
                series_list.append(s_data)
                logstr, series_list = appendAndCreate(logstr, series_list, s_data, directions, cntr, prevdate)
            else:
                print "No data found during specified range for", key
                
    return logstr


def appendAndCreate(logstr, series_list, s_data, directions, cntr, prevdate):
    if len(series_list)>0:
        for item in series_list:
            logstr += HighchartWindRoseSnippet(item, directions, str(cntr), str(prevdate))
        series_list = []
    return logstr, series_list    


def HighchartWindRoseSnippet(s_data, directions, titles, date):
    c_code_1 = """<script type='text/javascript'>
    $(function () {
    $('#minirose"""
    c_code_1 += str(titles)
    c_code_1 += """').highcharts({
    data: {
    table: 'freq"""
    c_code_1 += str(titles)
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
    text: '"""
    c_code_2 += str(date)+"'"
    c_code_3 = """},
    pane: {
    size: '50%'
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
    </script>"""
    c_code_4 =  """<div id='minirose"""
    c_code_4 += str(titles)
    c_code_4 += """' ></div>"""
    c_code_4 += """<div style="display:none"><table id='freq"""
    c_code_4 += str(titles)
    c_code_4 += """' border="0" cellspacing="0" cellpadding="0">
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
    """
    c_code = (
        c_code_1+
        c_code_2+
        c_code_3+
        c_code_4+
        c_code_5
    )
    return c_code
    


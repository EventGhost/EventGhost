# -*- coding: utf-8 -*-

# plugins/OpenWeatherMap/__init__.py
#
# Copyright (C) 2014  Pako <lubos.ruckl@gmail.com>
#
# This file is a plugin for EventGhost.
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.2 by topic2k
#     - made the code more PEP8 conform
#     - some fixes/changes for wxPython 3.0
# 0.1a by Pako 2018-04-21 07:16 GMT+1
#     - test version (forecast)
# 0.1 by Pako 2014-10-16 10:33 GMT+1
#     - bugfix (Sunrise/Sunset event)
# 0.0 by Pako 2014-10-12 09:16 GMT+1
#     - first public version


# =============================================================================


import eg

version = "0.2"

DESCRIPTION = ur'''<rst>
This plugin obtains weather data from the OpenWeatherMap_ server and is working 
with them.

Plugin uses library Requests_ .

Plugin version: %s

.. _OpenWeatherMap:   http://www.openweathermap.org
.. _Requests:         http://www.python-requests.org/en/latest/
'''

eg.RegisterPlugin(
    name="Open Weather Map",
    author="Pako",
    version=version,
    kind="other",
    guid="{8F6553F5-8E2D-45A0-BB49-B2A6B7F05C97}",
    createMacrosOnAdd=True,
    canMultiLoad=False,
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAEJGlDQ1BJQ0MgUHJvZmls"
        "ZQAAOBGFVd9v21QUPolvUqQWPyBYR4eKxa9VU1u5GxqtxgZJk6XtShal6dgqJOQ6N4mp"
        "Gwfb6baqT3uBNwb8AUDZAw9IPCENBmJ72fbAtElThyqqSUh76MQPISbtBVXhu3ZiJ1PE"
        "XPX6yznfOec7517bRD1fabWaGVWIlquunc8klZOnFpSeTYrSs9RLA9Sr6U4tkcvNEi7B"
        "FffO6+EdigjL7ZHu/k72I796i9zRiSJPwG4VHX0Z+AxRzNRrtksUvwf7+Gm3BtzzHPDT"
        "NgQCqwKXfZwSeNHHJz1OIT8JjtAq6xWtCLwGPLzYZi+3YV8DGMiT4VVuG7oiZpGzrZJh"
        "cs/hL49xtzH/Dy6bdfTsXYNY+5yluWO4D4neK/ZUvok/17X0HPBLsF+vuUlhfwX4j/rS"
        "fAJ4H1H0qZJ9dN7nR19frRTeBt4Fe9FwpwtN+2p1MXscGLHR9SXrmMgjONd1ZxKzpBeA"
        "71b4tNhj6JGoyFNp4GHgwUp9qplfmnFW5oTdy7NamcwCI49kv6fN5IAHgD+0rbyoBc3S"
        "OjczohbyS1drbq6pQdqumllRC/0ymTtej8gpbbuVwpQfyw66dqEZyxZKxtHpJn+tZnpn"
        "EdrYBbueF9qQn93S7HQGGHnYP7w6L+YGHNtd1FJitqPAR+hERCNOFi1i1alKO6RQnjKU"
        "xL1GNjwlMsiEhcPLYTEiT9ISbN15OY/jx4SMshe9LaJRpTvHr3C/ybFYP1PZAfwfYrPs"
        "MBtnE6SwN9ib7AhLwTrBDgUKcm06FSrTfSj187xPdVQWOk5Q8vxAfSiIUc7Z7xr6zY/+"
        "hpqwSyv0I0/QMTRb7RMgBxNodTfSPqdraz/sDjzKBrv4zu2+a2t0/HHzjd2Lbcc2sG7G"
        "tsL42K+xLfxtUgI7YHqKlqHK8HbCCXgjHT1cAdMlDetv4FnQ2lLasaOl6vmB0CMmwT/I"
        "PszSueHQqv6i/qluqF+oF9TfO2qEGTumJH0qfSv9KH0nfS/9TIp0Wboi/SRdlb6RLgU5"
        "u++9nyXYe69fYRPdil1o1WufNSdTTsp75BfllPy8/LI8G7AUuV8ek6fkvfDsCfbNDP0d"
        "vRh0CrNqTbV7LfEEGDQPJQadBtfGVMWEq3QWWdufk6ZSNsjG2PQjp3ZcnOWWing6noon"
        "SInvi0/Ex+IzAreevPhe+CawpgP1/pMTMDo64G0sTCXIM+KdOnFWRfQKdJvQzV1+Bt8O"
        "okmrdtY2yhVX2a+qrykJfMq4Ml3VR4cVzTQVz+UoNne4vcKLoyS+gyKO6EHe+75Fdt0M"
        "be5bRIf/wjvrVmhbqBN97RD1vxrahvBOfOYzoosH9bq94uejSOQGkVM6sN/7HelL4t10"
        "t9F4gPdVzydEOx83Gv+uNxo7XyL/FtFl8z9ZAHF4bBsrEwAAAAlwSFlzAAALEwAACxMB"
        "AJqcGAAABCJpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6"
        "eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJk"
        "ZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1z"
        "eW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAg"
        "ICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8i"
        "CiAgICAgICAgICAgIHhtbG5zOmV4aWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8x"
        "LjAvIgogICAgICAgICAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1l"
        "bnRzLzEuMS8iCiAgICAgICAgICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNv"
        "bS94YXAvMS4wLyI+CiAgICAgICAgIDx0aWZmOlJlc29sdXRpb25Vbml0PjE8L3RpZmY6"
        "UmVzb2x1dGlvblVuaXQ+CiAgICAgICAgIDx0aWZmOkNvbXByZXNzaW9uPjU8L3RpZmY6"
        "Q29tcHJlc3Npb24+CiAgICAgICAgIDx0aWZmOlhSZXNvbHV0aW9uPjcyPC90aWZmOlhS"
        "ZXNvbHV0aW9uPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVu"
        "dGF0aW9uPgogICAgICAgICA8dGlmZjpZUmVzb2x1dGlvbj43MjwvdGlmZjpZUmVzb2x1"
        "dGlvbj4KICAgICAgICAgPGV4aWY6UGl4ZWxYRGltZW5zaW9uPjMyPC9leGlmOlBpeGVs"
        "WERpbWVuc2lvbj4KICAgICAgICAgPGV4aWY6Q29sb3JTcGFjZT4xPC9leGlmOkNvbG9y"
        "U3BhY2U+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj4zMjwvZXhpZjpQaXhl"
        "bFlEaW1lbnNpb24+CiAgICAgICAgIDxkYzpzdWJqZWN0PgogICAgICAgICAgICA8cmRm"
        "OkJhZy8+CiAgICAgICAgIDwvZGM6c3ViamVjdD4KICAgICAgICAgPHhtcDpNb2RpZnlE"
        "YXRlPjIwMTQtMDYtMDhUMjA6MDY6ODQ8L3htcDpNb2RpZnlEYXRlPgogICAgICAgICA8"
        "eG1wOkNyZWF0b3JUb29sPlBpeGVsbWF0b3IgMi4yPC94bXA6Q3JlYXRvclRvb2w+CiAg"
        "ICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgpj"
        "/NjpAAAFK0lEQVRIDbVWWW9bRRSeuYt3O14T20oCxYkb0tKkW1iCGgFCpXQTLyDeqCIk"
        "nnjtb+APIFWiQqiCBwRI7QstEksaaKO0aRWapAtJsziJHbs33uLl7ny3ibLYNzRB6ug+"
        "jGfOnO+c73xnxvQz+0HyPAfzPJ0bvncHoOkE367GLgAUlXZGy8f3Z2WV7hyD26Ep4uY5"
        "7UyX0OwXRxPOZM7KMjvKxTyD+qOSQt9oK+xprPKcfrpLqDHQDerM0zIBYKjOMTp4gFNV"
        "o8ZhjYbc8plugbA6ofqRWLG7tQgDOJVgplIrpwVdkikZtRTBY9gnnetNJbLWR0v2OcGa"
        "LfFliTm6pzi7bEtNWeDU75YPv7DyKOVw29QWv9gZKccj5YRgvTAQRWQ1MLUADKMvlzg7"
        "r/Xuzfe2F+Du7qzz0s2mPx54hybdTqvCUFISuarCoiQfHHpyOFYkmiHGvx41aE8nzwAA"
        "kStVdiLp6PPKMB2ZcX031Njirb7dIbQ1sw6vmzKMuFJMJKWBB+6Lg5HFnNUoiUKnMjZg"
        "14/aDGBBKbkPgH25O1Pur65HTr2Sfr9HZtt6iMVDSjkile0eNR6V47HF4Xupr/8MU6If"
        "ixeSOQuy3xEA9Dcr2GaXbN8ONZ3Ylzndx5C9p8jiQ7Jwg8ii4QIhcBZib+jpFFma/OZG"
        "eEViKzJrmgF7hI/UwIJ3WWWmMzanRT33Vo7Zf5xMDZP5McMvwxKGIZQh0JZUIooeDYhP"
        "ijwqhPJKKsPWqXLLAq4BSWHCDeKHR9O5CtfXLnAvvkyEeZKeNEImWzk2YDRUuC+ed1nV"
        "j3oyB1pWFM1Q9uaINwCw4bCoZw9lzp9MdIQr0H57WCaOIFmcIAy/+cyWuUajXslpVdEK"
        "n7+70H8sGfGKuFTWbdaKDOT2pnL/sVTALROdPl7ieVZzO1kiS6S6YpCz/eBYrcGuZopG"
        "EK/FCmiRn0YCv074V++StQxYqoPK29PuSgUs6xw6lqD7QVnVoPtZA9xy8MTqukrvzTsn"
        "0w5K106tZYAQ8xXu++HQzUnPqW6h1Sei1Lmi7pQKhOWJpmwLQYkoszgb9YkzaduVO8Gx"
        "eRd8r7f0hoqAAQ0UKtzIjDtZsAgl3ueQY+EqoRZof1uWWH1qyX79nwao4/Ld4ELWhuw3"
        "63WjyKsxgjh84wtOr0MZnPSV0nlCVUOX2wzwd3Xc3+ITJxadwOCfcrvZ1vwk7D5+Ne2x"
        "K5duhrRK3vzdQ+E57ee//YllK9TRGqiC1c2uV+cmALBD+HsC4ie9S3OC7cLv0Twqz2ko"
        "vtEJ+DDhNFEjP94KXRvz9b+ZCvnEtkYou94/2ajB+iYk2xGpvB4rOKzawdbSaML1y7iv"
        "WOWgEzhHuy4VLLdnPFBEpmj5tC8Vj5aJZgh5eNpTr2eTyw60xsNlYtGIzNh59Z3O7A+3"
        "gndnXcOP3UgOjmDgsqlliT3bLQRcEq5SymuxUDXkkdJ5a82VZwIAGVhY/cZ979iC43HG"
        "nitxeLxOdgknDmTzJU7XqcuhzGRsX/4WvTgYxguBTn4pVG1rqnjtaqquXtT0jxd0JiqI"
        "1RAuXlCEjKf4/HtzzUGJ6ERW6BdXW2YzhiKxhTsGjQbL1dZdp3p1YlJkbOAAhIQP3vET"
        "vJRF5vJo0Cgj1QceNkyn7avdji0jY84Qd43r/wKoN4WL0TnXWMJZLHPXxv0sa6aY+mNQ"
        "stmi+RoivDIawN+LbIlDcuZGdau7AMD1kli24bHbuXfA7QIA1ijJ5numLlyTBfMimxj+"
        "36V/AfsHUTRxW37FAAAAAElFTkSuQmCC"
    ),
    description=DESCRIPTION % version,
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=6331",
)


# =============================================================================


import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from time import time as ttime
from datetime import datetime as dt
try:
    from wx.combo import ComboCtrl, ComboPopup
except ImportError:
    from wx import ComboCtrl, ComboPopup
from threading import enumerate as threads
from json import dumps
from locale import strcoll
from requests import get
from base64 import b64encode, b64decode
from PIL import Image
from StringIO import StringIO
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

# api.openweathermap.org/data/2.5/weather?q=London
# api.openweathermap.org/data/2.5/weather?q=London,uk
# api.openweathermap.org/data/2.5/weather?id=2172797
# api.openweathermap.org/data/2.5/weather?lat=35&lon=139
#                                                        &lang=de&units=metric
#
# FORECAST 5 days/3hours
# api.openweathermap.org/data/2.5/forecast?
#api.openweathermap.org/data/2.5/forecast?id=524901
#
# FORECAST 16 days/daily
# api.openweathermap.org/data/2.5/forecast/daily?q=London&units=metric&cnt=7
#                                                               (cnt=1 to 16)
#
# HISTORY
# api.openweathermap.org/data/2.5/history/city?id=2885679&type=hour&start=1369728000&cnt=1
# api.openweathermap.org/data/2.5/history/               &type=day
#
# ICON
# url="http://openweathermap.org/img/w/%s.png" % code

SYS_VSCROLL_X = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
ACV = wx.ALIGN_CENTER_VERTICAL
APIURL = "http://api.openweathermap.org/data/2.5/"
LANGUAGES = {
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Chinese Simplified": "zh_cn",
    "Chinese Traditional": "zh_tw",
    "Croatian": "hr",
    "Dutch": "nl",
    "English": "en",
    "Finnish": "fi",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Spanish": "es",
    "Swedish": "sv",
    "Turkish": "tr",
    "Ukrainian": "uk",
}


# =============================================================================


class Text:
    apiLabel = 'API key:'
    language = 'Language:'
    unitsLbl = "Units:"
    units = ("Internal", "Metric", "Imperial")
    prefix = "Event prefix:"
    period = "Polling period [min]:"
    label1 = "List of observed locations:"
    header1 = (
        "Enabled",
        "City name",
        "City ID",
    )
    header2 = (
        "Wind speed",
        "Wind direction",
        "Pressure",
        "Humidity",
        "Sunrise - Sunset",
    )
    buttons1 = (
        "Add new",
        "Duplicate",
        "Edit",
        "Delete"
    )
    title1 = "City details"
    cancel = "Cancel"
    ok = "OK"
    version = "version"
    filter = "Selector of events ..."
    evtFilter = [
        "Status",
        "Temperature",
        "Wind",
        # "Clouds",
        "Pressure",
        "Humidity",
        "Sunrise",
        "Sunset"
    ]
    events = "Events:"
    beaufort = (
        "Calm",
        "Light air",
        "Light breeze",
        "Gentle breeze",
        "Moderate breeze",
        "Fresh breeze",
        "Strong breeze",
        "Near gale",
        "Gale",
        "Strong gale",
        "Storm",
        "Violent storm",
        "Hurricane"
    )
    cardinalDir = (
        "North",
        "North-northeast",
        "Northeast",
        "East-northeast",
        "East",
        "East-southeast",
        "Southeast",
        "South-southeast",
        "South",
        "South-southwest",
        "Southwest",
        "West-southwest",
        "West",
        "West-northwest",
        "Northwest",
        "North-northwest",
    )
    cardinalDirShort = (
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW"
    )
    windSpeedForm = "Formatting wind speed:"
    windSpeed = (
        "Only speed in mph",
        "Only speed in km/h",
        "Only speed in m/s",
        "Beaufort verbal description + speed in mph",
        "Beaufort verbal description + speed in km/h",
        "Beaufort verbal description + speed in m/s",
        "Only Beaufort verbal description"
    )
    windDirForm = "Formatting wind direction:"
    windDir = (
        "Only angle in degrees",
        "Compass point name (long) + angle in degrees",
        "Compass point name (short) + angle in degrees",
        "Only Compass point name (long)",
        "Only Compass point name (short)",
    )
    respForm = "Response format"
    forms1 = (
        "Dictionary (unmodified, full form)",
        "Dictionary (modified, shortened form)",
        "Show window with a table"
    )
    autoclose1 = "The window automatically to close after"
    autoclose2 = "seconds (0 = never)"
    tooltip = "Right mouse button closes this window"


# =============================================================================


class WeatherTable(wx.ListCtrl, ListCtrlAutoWidthMixin):

    def __init__(self, parent, header, data):
        wx.ListCtrl.__init__(
            self, parent, wx.ID_ANY,
            style=(
                wx.LC_REPORT
                | wx.LC_HRULES
                | wx.LC_VRULES
                | wx.LC_SINGLE_SEL
                | wx.LC_NO_HEADER
            )
        )
        ListCtrlAutoWidthMixin.__init__(self)
        fnt = self.GetFont()
        fnt.SetPointSize(10)
        self.SetFont(fnt)
        self.SetBackgroundColour(self.GetParent().GetBackgroundColour())        
        # self.SetBackgroundColour("#87CEEB")
        wk = self.GetWindowBorderSize()[0]
        # wk = -6
        widths = (
            [self.GetTextExtent(item + "     ")[0] for item in header],
            [self.GetTextExtent(item + "     ")[0] for item in data]
        )
        for j in range(2):
            self.InsertColumn(j, "")
            w = max(widths[j])
            self.SetColumnWidth(j, w)
            wk += w
        try:
            self.InsertItem(0, "dummy")
        except TypeError:
            self.InsertItem(0, "dummy")
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        hi = rect[3]  # item height
        self.DeleteAllItems()
        self.SetMinSize((wk, 4 + len(data) * hi))
        self.SetSize((wk, 4 + len(data) * hi))
        self.Layout()
        for row in range(len(data)):
            try:
                self.InsertItem(row, header[row])
                self.SetItem(row, 1, data[row])
            except TypeError:
                self.InsertItem(row, header[row])
                self.SetItem(row, 1, data[row])


# =============================================================================


class CurrentWeather(wx.Frame):

    def __init__(self, parent, plugin, title, dtt, data, autoclose):
        icon = plugin.getIcon(data['icon'])
        pil = Image.open(StringIO(b64decode(icon)))
        try:
            img = wx.Image(pil.size[0], pil.size[1])
        except TypeError:
            img = wx.EmptyImage(pil.size[0], pil.size[1])
        if int(wx.__version__.split('.')[0]) > 2:
            img.SetData(pil.convert("RGB").tobytes())
            try:
                img.SetAlphaData(pil.convert("RGBA").tobytes()[3::4])
            except AttributeError:
                img.SetAlpha(pil.convert("RGBA").tobytes()[3::4])
        else:
            img.SetData(pil.convert("RGB").tostring())
            try:
                img.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
            except AttributeError:
                img.SetAlpha(pil.convert("RGBA").tostring()[3::4])

        img = img.ConvertToBitmap()
        wx.Frame.__init__(
            self, parent,  wx.ID_ANY, '',
            style=wx.STAY_ON_TOP | wx.SIMPLE_BORDER
        )
        self.SetBackgroundColour("#87CEEB")
        self.delta = (0, 0)
        bmp = wx.StaticBitmap(
            self, wx.ID_ANY, img, (0, 0),
            (img.GetWidth(), img.GetHeight())
        )
        ttlLbl = wx.StaticText(self, wx.ID_ANY, title)
        font = wx.Font(
            22,
            wx.FONTFAMILY_SWISS,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            False,
            u'Arial'
        )
        ttlLbl.SetFont(font)       
        dttLbl = wx.StaticText(
            self, wx.ID_ANY, plugin.fromTimestamp(dtt, True)
        )
        font = wx.Font(
            26,
            wx.FONTFAMILY_SWISS,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            False,
            u'Arial Narrow'
        )
        tIx = plugin.text.units.index(plugin.uni)
        tLbl = wx.StaticText(
            self, wx.ID_ANY,
            u"%.1f \u00B0%s" % (data['temp'], ('K', 'C', 'F')[tIx])
        )
        tLbl.SetFont(font)
        stLbl = wx.StaticText(self, wx.ID_ANY, data['status'])
        fnt = stLbl.GetFont()
        fnt.SetPointSize(12)
        stLbl.SetFont(fnt)
       
        wData = (
            data['wind']['speed'],
            data['wind']['deg'],
            "%.2f hpa" % data['pressure'],
            "%i %%" % data['humidity'],
            "%s - %s" % (
                plugin.fromTimestamp(data['sunrise']),
                plugin.fromTimestamp(data['sunset'])
            )
        )
        table = WeatherTable(self, plugin.text.header2, wData)
        table.Enable(False)
        bordSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.GridBagSizer(0, 5)
        bordSizer.Add(mainSizer, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(ttlLbl, (0, 0), (1, 3))
        mainSizer.Add(dttLbl, (1, 0), (1, 3))
        mainSizer.Add(bmp, (2, 0), flag=ACV)
        mainSizer.Add(tLbl, (2, 1), flag=ACV)
        mainSizer.Add(stLbl, (2, 2), flag=wx.ALIGN_CENTER | ACV)
        mainSizer.Add(table, (3, 0), (1, 3), flag=wx.EXPAND)
        self.SetSizerAndFit(bordSizer)
        for win in (self, bmp, ttlLbl, dttLbl, tLbl, stLbl):
            win.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            win.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            win.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
            win.Bind(wx.EVT_MOTION, self.OnMouseMove)
            try:
                win.SetToolTip(plugin.text.tooltip)
            except TypeError:
                win.SetToolTip(plugin.text.tooltip)

        self.timer = wx.Timer(self)
        if autoclose:
            self.timer.Start(1000*int(autoclose))
            self.Bind(wx.EVT_TIMER, self.OnCloseWindow)

        self.Show(True)
        self.Raise()

    def OnCloseWindow(self, event):
        self.timer.Stop()
        del self.timer
        self.Destroy()

    def OnRightClick(self, evt):
        self.Show(False)
        self.Close()

    def OnLeftDown(self, evt):
        x, y = self.ClientToScreen(evt.GetPosition())
        win = evt.GetEventObject()
        if isinstance(
            win, (wx.StaticText, wx.StaticBitmap)
        ):
            childX, childY = win.GetPosition()
            x += childX
            y += childY
        self.CaptureMouse()
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = (dx, dy)

    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)


# =============================================================================


class CheckListComboBox(ComboCtrl):

    class CheckListBoxComboPopup(ComboPopup):

        def __init__(self, values, helpText):
            ComboPopup.__init__(self)
            self.values = values
            self.helpText = helpText
            self.curitem = None
            self.lb = None
            self.itemHeight = None

        def OnDclick(self, evt):
            self.Dismiss()
            self.SetHelpText()

        def Init(self):
            self.curitem = None

        def Create(self, parent):
            self.lb = wx.CheckListBox(
                parent, wx.ID_ANY, (80, 50), wx.DefaultSize
            )
            self.itemHeight = self.lb.GetSize().GetHeight()
            self.SetValue(self.values)
            self.SetHelpText()
            self.lb.Bind(wx.EVT_MOTION, self.OnMotion)
            self.lb.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            self.lb.Bind(wx.EVT_LEFT_DCLICK, self.OnDclick)
            return True

        def SetHelpText(self, helpText=None):
            self.helpText = helpText if helpText is not None else self.helpText
            try:
                combo = self.GetCombo()
            except AttributeError:
                combo = self.GetComboCtrl()
            combo.SetText(self.helpText)
            combo.TextCtrl.SetEditable(False)

        def SetValue(self, values):
            self.lb.Set(values[0])
            for j in range(len(values[1])):
                self.lb.Check(j, int(values[1][j]))

        def GetValue(self):
            strngs = self.lb.GetStrings()
            return [strngs, [self.lb.IsChecked(j) for j in range(len(strngs))]]

        def GetControl(self):
            return self.lb

        def OnPopup(self):
            if self.curitem:
                self.lb.EnsureVisible(self.curitem)
                self.lb.SetSelection(self.curitem)

        def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
            return wx.Size(
                minWidth,
                min(self.itemHeight*(0.5+len(self.lb.GetStrings())), maxHeight)
            )

        def OnMotion(self, evt):
            item = self.lb.HitTest(evt.GetPosition())
            if item > -1:
                self.lb.SetSelection(item)
                self.curitem = item
            evt.Skip()

        def OnLeftDown(self, evt):
            item = self.lb.HitTest(evt.GetPosition())
            if item > -1:
                self.curitem = item
            evt.Skip()

    def __init__(self, parent, wid=wx.ID_ANY, values=None, **kwargs):
        if not values:
            values = [[], []]
        if 'helpText' in kwargs:
            helpText = kwargs['helpText']
            del kwargs['helpText']
        else:
            helpText = ""
        ComboCtrl.__init__(self, parent, wid, **kwargs)
        self.popup = self.CheckListBoxComboPopup(values, helpText)
        self.SetPopupControl(self.popup)
        self.popup.lb.Bind(wx.EVT_CHECKLISTBOX, self.onCheck)

    def onCheck(self, evt):
        wx.PostEvent(self, evt)
        evt.StopPropagation()

    def GetValue(self):
        return self.popup.GetValue()

    def SetValue(self, values):
        self.popup.SetValue(values)

    def SetHelpText(self, helpText=None):
        self.popup.SetHelpText(helpText)


# =============================================================================


class extDialog(wx.Frame):
    def __init__(self, parent, plugin, labels, data, grid, add=False):
        wx.Frame.__init__(
            self, parent, wx.ID_ANY,
            style=(
                wx.DEFAULT_DIALOG_STYLE
                | wx.TAB_TRAVERSAL
                | wx.RESIZE_BORDER
            ),
            name="OpenWeatherMapExtDialog"
        )
        self.panel = parent
        self.plugin = plugin
        self.text = plugin.text
        self.SetIcon(self.plugin.info.icon.GetWxIcon())
        self.labels = labels
        self.data = data
        self.grid = grid
        self.add = add

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

    def ShowExtDialog(self, title):
        self.panel.Enable(False)
        self.panel.dialog.buttonRow.cancelButton.Enable(False)
        self.panel.EnableButtons(False)
        self.SetTitle(title)
        text = self.plugin.text
        panel = wx.Panel(self)

        def wxst(label):
            return wx.StaticText(panel, wx.ID_ANY, "%s:" % label)

        labels = self.labels
        data = self.data
        rows = len(labels)
        sizer = wx.FlexGridSizer(rows-1, 2, 5, 5)
        for row in range(1, rows):
            sizer.Add(wxst(labels[row]), 0, ACV)
            ctrl = wx.TextCtrl(panel, wx.ID_ANY, data[row])
            sizer.Add(ctrl, 0, wx.EXPAND)
        sizer.AddGrowableCol(1)

        line = wx.StaticLine(
            panel,
            wx.ID_ANY,
            style=wx.LI_HORIZONTAL
        )
        btn1 = wx.Button(panel, wx.ID_OK)
        btn1.SetLabel(text.ok)
        btn2 = wx.Button(panel, wx.ID_CANCEL)
        btn2.SetLabel(text.cancel)
        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(btn1)
        btnsizer.AddButton(btn2)
        btnsizer.Realize()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(
            line, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5
        )
        mainSizer.Add(btnsizer, 0, wx.EXPAND | wx.RIGHT, 10)
        mainSizer.Add((1, 6))
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

        def onClose(evt):
            self.MakeModal(False)
            self.panel.Enable(True)
            self.panel.dialog.buttonRow.cancelButton.Enable(True)
            self.panel.EnableButtons(True)
            self.GetParent().GetParent().Raise()
            self.Destroy()
        self.Bind(wx.EVT_CLOSE, onClose)

        def onOk(evt):
            if self.add:
                self.grid.AppendRow()
            children = sizer.GetChildren()
            row_data = [
                self.data[0],
                children[1].GetWindow().GetValue(), 
                children[3].GetWindow().GetValue()
            ]
            self.grid.SetRow(row_data)
            row_data = self.grid.GetData()
            row_data.sort(cmp=strcoll, key=lambda city: city[1])
            self.grid.DeleteAllItems()
            self.grid.SetData(row_data)
            self.Close()
        btn1.Bind(wx.EVT_BUTTON, onOk)

        def onCancel(evt):
            self.Close()
        btn2.Bind(wx.EVT_BUTTON, onCancel)

        mainSizer.Layout()
        w, h = self.GetSize()
        self.SetSize((max(w, 400), h))
        self.SetMinSize((max(w, 400), h))
        self.MakeModal(True)
        self.Show()
        self.Raise()


# =============================================================================


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):

    def __init__(self, parent, header, rows):
        wx.ListCtrl.__init__(
            self, parent, wx.ID_ANY,
            style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL
        )
        self.rows = rows
        self.selRow = -1
        self.back = self.GetBackgroundColour()
        self.fore = self.GetForegroundColour()
        self.selBack = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.selFore = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        self.wk = SYS_VSCROLL_X + self.GetWindowBorderSize()[0]
        self.collens = []
        hc = len(header)
        for j in range(hc):
            self.InsertColumn(j, header[j])
        for j in range(hc):
            self.SetColumnWidth(j, wx.LIST_AUTOSIZE_USEHEADER)
            w = self.GetColumnWidth(j)
            self.collens.append(w)
            self.wk += w
        try:
            self.InsertItem(0, "dummy")
        except TypeError:
            self.InsertItem(0, "dummy")
        rect = self.GetItemRect(0, wx.LIST_RECT_BOUNDS)
        hh = rect[1]  # header height
        hi = rect[3]  # item height
        self.DeleteAllItems()
        self.SetMinSize((self.wk, 5 + hh + rows * hi))
        self.SetSize((self.wk, 5 + hh + rows * hi))
        self.Layout()
        CheckListCtrlMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def SetWidth(self):
        newW = self.GetSize().width
        p = newW/float(self.wk)
        col = self.GetColumnCount()
        w = (
            SYS_VSCROLL_X
            + self.GetWindowBorderSize()[0]
            + self.GetColumnWidth(0)
        )
        for c in range(1, col-1):
            self.SetColumnWidth(c, p * self.collens[c])
            w += self.GetColumnWidth(c)
        self.SetColumnWidth(col-1, newW-w)

    def OnSize(self, event):
        wx.CallAfter(self.SetWidth)
        event.Skip()

    def OnItemSelected(self, evt):
        self.SelRow(evt.GetSelection())
        evt.Skip()

    # this is called by the base class when an item is checked/unchecked !!
    def OnCheckItem(self, index, flag):
        evt = eg.ValueChangedEvent(self.GetId(), value=(index, flag))
        wx.PostEvent(self, evt)

    def SelRow(self, row):
        if row != self.selRow:
            if self.selRow in range(self.GetItemCount()):
                item = self.GetItem(self.selRow)
                item.SetTextColour(self.fore)
                item.SetBackgroundColour(self.back)
                self.SetItem(item)
            self.selRow = row
        if self.GetItemBackgroundColour(row) != self.selBack:
            item = self.GetItem(row)
            item.SetTextColour(self.selFore)
            item.SetBackgroundColour(self.selBack)
            self.SetItem(item)
            self.SetItemState(row, 0, wx.LIST_STATE_SELECTED)

    def DeleteRow(self, row=None):
        row = self.selRow if row is None else row
        if row > -1:
            self.DeleteItem(row)
            row = row if row < self.GetItemCount() else self.GetItemCount() - 1
            if row > -1:
                self.SelRow(row)
            else:
                self.selRow = -1
                evt = eg.ValueChangedEvent(self.GetId(), value="Empty")
                wx.PostEvent(self, evt)

    def AppendRow(self):
        ix = self.GetItemCount()
        try:
            self.InsertItem(ix, "")
        except TypeError:
            self.InsertItem(ix, "")
        self.CheckItem(ix)
        self.EnsureVisible(ix)
        self.SelRow(ix)
        if ix == 0:
            evt = eg.ValueChangedEvent(self.GetId(), value="One")
            wx.PostEvent(self, evt)

    def SetRow(self, rowData, row=None):
        row = self.selRow if row is None else row
        if rowData[0]:
            self.CheckItem(row)
        elif self.IsChecked(row):
            self.ToggleItem(row)
        for j in range(1, len(rowData)):
            data = rowData[j] if j != 2 else str(rowData[j])
            try:
                self.SetItem(row, j, data)
            except TypeError:
                self.SetItem(row, j, data)

    def GetSelectedItemIx(self):
        return self.selRow

    def GetRow(self, row=None):
        row = self.selRow if row is None else row
        return [
            self.IsChecked(row),
            self.GetItem(row, 1).GetText(),
            self.GetItem(row, 2).GetText()
        ]

    def GetData(self):
        data = []
        for row in range(self.GetItemCount()):
            rowData = self.GetRow(row)
            data.append(rowData)
        return data

    def SetData(self, data):
        if data:
            for row in range(len(data)):
                self.AppendRow()
                self.SetRow(data[row])
            self.SelRow(0)
            self.EnsureVisible(0)


# =============================================================================


class OpenWeatherMap(eg.PluginBase):
    task = None
    api_key = None
    text = Text

    def __init__(self):
        self.AddActionsFromList(ACTIONS)
        self.city_grid = None

    def StartTask(self):
        enabled = [itm[0] for itm in self.cities if itm[0]] \
            if self.cities else False
        if enabled:
            self.oldValues = dict([
                (
                    item[2],
                    {
                        'status': None,
                        'temp': None,
                        'wind': None,
                        'pressure': None,
                        'humidity': None,
                        'sunrise': None,
                        'sunset': None,
                        'icon': None,
                    }
                ) for item in self.cities])
            self.task = eg.scheduler.AddTask(5.0, self.worker)

    def CancelTasks(self):
        if self.task:
            try:
                eg.scheduler.CancelTask(self.task)
            except:
                pass
        self.task = None
        tasks = []
        heap = eg.scheduler.heap
        thrds = threads()
        ST = [i for i in thrds if i.name=="SchedulerThread"][0]
        for task in heap:
            if task[1] == ST.LongTask:
                if len(task[2]) > 1:
                    if task[2][1] in (self.SunriseTime, self.SunsetTime):
                        tasks.append(task)
        for task in tasks:
            try:
                eg.scheduler.CancelTask(task)
            except:
                pass

    def OnComputerSuspend(self, evt):
        self.CancelTasks()

    def OnComputerResume(self, evt):
        self.CancelTasks()
        self.StartTask()

    @staticmethod
    def fromTimestamp(ts, hours=False):
        ts = str(dt.fromtimestamp(ts + 30))
        return ts[:16] if hours else ts[11:16]

    def WindSpeed(self, speed):
        beauf = spd = 'UNKNOWN'
        if self.spd > 2:
            beauf = self.BeaufortScale(speed)
        if self.uni == 'Imperial':
            if self.spd in (2, 5):
                spd = "%.2f m/s" % (0.447 * speed)
            elif self.spd in (1, 4):
                spd = "%.2f km/h" % (1.6093 * speed)
            elif self.spd < 6:
                spd = "%.2f mph" % speed
        else:
            if self.spd in (0, 3):
                spd = "%.2f mph" % (2.2369 * speed)
            if self.spd in (1, 4):
                spd = "%.2f km/h" % (3.6 * speed)
            elif self.spd < 6:
                spd = "%.2f m/s" % speed
        if self.spd < 3:
            return spd
        elif self.spd > 5:
            return beauf
        else:
            return "%s %s" % (beauf, spd)

    def WindDir(self, angle):
        if self.dir:
            cp = self.CardinalNames(angle, self.dir in (2, 4))
            if self.dir > 2:
                return cp
            else:
                return u"%s (%.2f°)" % (cp, angle)
        return u"%.2f°" % angle

    def BeaufortScale(self, speed):
        upper_limits = [0.7, 3, 6, 10, 16, 21, 27, 33, 40, 47, 55, 63, 999]
        knots = speed * 0.869 if self.uni == 'Imperial' else speed * 1.9438
        upper_limits.append(knots)
        upper_limits.sort()
        return self.text.beaufort[upper_limits.index(knots)]

    def CardinalNames(self, angle, short=False):
        names = self.text.cardinalDirShort if short else self.text.cardinalDir
        dirNum = len(names)
        index = int(round(angle*dirNum/360.0))
        index %= dirNum
        return names[index]

    def GetSuffix(self, wid):
        return [
            it[1] for it in self.cities if it[2] == wid
        ][0].replace(" ", "")

    def SunriseTime(self, wid):
        self.TriggerEvent(
            "%s.%s" % ("Sunrise", self.GetSuffix(wid)),
            payload=wid
        )
        sunrise = self.oldValues[wid]['sunrise']
        sunrise = sunrise if (3600 + ttime()) < sunrise else sunrise + 86400
        eg.scheduler.AddTaskAbsolute(sunrise, self.SunriseTime, wid)

    def SunsetTime(self, wid):
        self.TriggerEvent(
            "%s.%s" % ("Sunset", self.GetSuffix(wid)),
            payload=wid
        )
        sunset = self.oldValues[wid]['sunset']
        sunset = sunset if (3600 + ttime()) < sunset else sunset + 86400
        eg.scheduler.AddTaskAbsolute(sunset, self.SunriseTime, wid)

    @staticmethod
    def getIcon(code):
        url = "http://openweathermap.org/img/w/%s.png" % code
        resp = get(url)
        if (
            resp.ok
            and resp.headers['content-type'] == 'image/png'
            and int(resp.headers['content-length']) == len(resp.content)
        ):
            return b64encode(resp.content)

    def getWeather(self, mode, ix=None, city=None):
        params = {}
        try:
            if ix is not None:
                city = self.cities[ix][2]
                params['id'] = int(city)
            elif mode == 2:
                params['id'] = int(city)
            else:
                params['q'] = str(city)
            return self.get_(APIURL + 'weather', params=params)
        except:
            eg.PrintTraceback()

    def getForecast(self, mode, ix = None, city = None):
        params = {}
        try:
            if ix is not None:
                city = self.cities[ix][2]
                params['id'] = int(city)
            elif mode == 2:
                params['id'] = int(city)
            else:
                params['q'] = str(city)
            return self.get_(APIURL + 'forecast', params = params)
        except:
            eg.PrintTraceback()

    def GetShortData(self, data):
        shortData = {
            'status': data[u'weather'][0][u'description'],
            'temp': data[u'main'][u'temp'],
            'wind': {
                u'speed': self.WindSpeed(data[u'wind'][u'speed']),
                u'deg': self.WindDir(data[u'wind'][u'deg']) if "deg" in data[u'wind'] else self.WindDir(0)
            },
            'pressure': data[u'main'][u'pressure'],
            'humidity': data[u'main'][u'humidity'],
            'icon': data[u'weather'][0][u'icon'],
            'sunrise': data[u'sys'][u'sunrise'],
            'sunset': data[u'sys']['sunset']
        }
        return shortData

    def worker(self):
        heap = eg.scheduler.heap
        thrds = threads()
        ST = [i for i in thrds if i.name=="SchedulerThread"][0]
        for task in heap:
            if task[1] == ST.LongTask:
                if task[2][0] == self.worker:
                    try:
                        eg.scheduler.CancelTask(task)
                    except:
                        pass
        self.task = eg.scheduler.AddTask(60 * self.period, self.worker)
        for enbl, _, cid in self.cities:
            if enbl:
                try:
                    data = self.getWeather(2, ix=None, city=cid)
                except:
                    eg.PrintTraceback()
                    return
                if not data:
                    eg.PrintNotice("NO WEATHER DATA")
                    return
                oldVals = self.oldValues[cid]
                icon = data[u'weather'][0][u'icon']
                if icon != oldVals['icon']:
                    self.oldValues[cid]['icon'] = icon

                if self.evtFilter[0]:
                    status = data[u'weather'][0][u'description']
                    if status != oldVals['status']:
                        if oldVals['status'] is not None:
                            self.TriggerEvent(
                                "%s.%s" % ("Status", self.GetSuffix(cid)),
                                payload=(status, cid)
                            )
                        self.oldValues[cid]['status'] = status

                if self.evtFilter[1]:
                    temp = data[u'main'][u'temp']
                    if temp != oldVals['temp']:
                        if oldVals['temp'] is not None:
                            self.TriggerEvent(
                                "%s.%s" % ("Temperature", self.GetSuffix(cid)),
                                payload=(temp, cid)
                            )
                        self.oldValues[cid]['temp'] = temp
                if self.evtFilter[2]:
                    wind = dict(
                        speed=self.WindSpeed(data[u'wind'].get(u'speed', 0)),
                        deg=self.WindDir(data[u'wind'].get(u'deg', 0))
                    )
                    if wind != oldVals['wind']:
                        if oldVals['wind'] is not None:
                            self.TriggerEvent(
                                "%s.%s" % ("Wind", self.GetSuffix(cid)),
                                payload=(wind, cid)
                            )
                        self.oldValues[cid]['wind'] = wind

                if self.evtFilter[3]:
                    pressure = data[u'main'][u'pressure']
                    if pressure != oldVals['pressure']:
                        if oldVals['pressure'] is not None:
                            self.TriggerEvent(
                                "%s.%s" % ("Pressure", self.GetSuffix(cid)),
                                payload=(pressure, cid)
                            )
                        self.oldValues[cid]['pressure'] = pressure

                if self.evtFilter[4]:
                    humidity = data[u'main'][u'humidity']
                    if humidity != oldVals['humidity']:
                        if oldVals['humidity'] is not None:
                            self.TriggerEvent(
                                "%s.%s" % ("Humidity", self.GetSuffix(cid)),
                                payload=(humidity, cid)
                            )
                        self.oldValues[cid]['humidity'] = humidity

                if self.evtFilter[5]:
                    sunrise = data[u'sys'][u'sunrise']
                    sunrise = sunrise if ttime() < sunrise else sunrise + 86400
                    if sunrise != oldVals['sunrise']:
                        if oldVals['sunrise'] is None:
                            eg.scheduler.AddTaskAbsolute(
                                sunrise,
                                self.SunriseTime,
                                cid
                            )
                        self.oldValues[cid]['sunrise'] = sunrise

                if self.evtFilter[6]:
                    sunset = data[u'sys'][u'sunset']
                    sunset = sunset if ttime() < sunset else sunset + 86400
                    if sunset != oldVals['sunset']:
                        if oldVals['sunset'] is None:
                            eg.scheduler.AddTaskAbsolute(
                                sunset,
                                self.SunsetTime,
                                cid
                            )
                        self.oldValues[cid]['sunset'] = sunset

    def get_(self, url, **kwargs):
            kwargs['headers'] = {
                'X-User-Agent': 'EventGhost',
                'x-api-key': self.api_key,
                'Content-type': 'application/json',
                'Accept': 'application/json'
            }
            if 'data' in kwargs:
                kwargs['data'] = dumps(kwargs['data'])
            kwargs['params'] = kwargs['params'] if 'params' in kwargs else {}
            kwargs['params']['lang'] = LANGUAGES[self.lng]
            kwargs['params']['units'] = self.uni.lower()
            resp = get(url, **kwargs)
            if resp.ok:
                r = resp.json()
                if 'message' in r and not 'city' in r:
                    eg.PrintError("OpenWeatherMap: " + repr(r))
                    return
                return r
            else:
                print resp

    def __start__(
        self,
        api_key=(None, None),
        lng="English",
        uni="Metric",
        prf="OWM",
        period=30,
        cities=None,
        evtFilter=len(Text.evtFilter) * [True],
        spd=4,
        direction=1
    ):
        if not cities:
            cities = []
        if isinstance(api_key[0], eg.Password):
            api_key = (api_key[0].Get(), api_key[1])   
        self.api_key = str(api_key[0])
        self.evtFilter = evtFilter
        self.lng = lng
        self.uni = uni
        self.spd = spd
        self.dir = direction
        self.period = period
        self.cities = cities
        self.info.eventPrefix = prf
        self.StartTask()

    def __stop__(self):
        self.CancelTasks()

    def enableCity(self, ix, enable):
        self.cities[ix][0] = enable

    def Configure(
        self,
        apiKey=(None, None),
        lng="English",
        uni="Metric",
        prf="OWM",
        period=30,
        cities=None,
        evtFilter=len(Text.evtFilter) * [True],
        spd=4,
        direction=1
    ):
        if not cities:
            cities = []
        if not isinstance(apiKey[0], eg.Password):
            api_key = eg.Password(None)
            api_key.Set("")
        else:
            api_key = apiKey[0]
        dummy = apiKey[1]

        text = self.text
        evtFilter = [text.evtFilter, evtFilter]
        panel = eg.ConfigPanel(self)
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        label1 = wx.StaticText(panel, wx.ID_ANY, self.text.label1)
        self.city_grid = city_grid = CheckListCtrl(panel, self.text.header1, 3)
        city_grid.SetData(cities)
        ttl = panel.dialog.GetTitle()
        panel.dialog.SetTitle(
            "%s - %s - %s %s" % (
                "Open Weather Map",
                ttl,
                self.text.version,
                version
            )
        )        

        def enableButtons1(enable):
            for btn in range(1, len(self.text.buttons1)):
                wx.FindWindowById(bttns[btn]).Enable(enable)

        def OnGridChange1(evt):
            value = evt.GetValue()
            if value == "Empty":
                enableButtons1(False)
            elif value == "One":
                enableButtons1(True)
            evt.Skip()
        city_grid.Bind(eg.EVT_VALUE_CHANGED, OnGridChange1)

        def edit1():
            dlg = extDialog(
                parent=panel,
                plugin=self,
                labels=self.text.header1,
                data=city_grid.GetRow(),
                grid=city_grid,
            )
            dlg.Centre()
            wx.CallAfter(dlg.ShowExtDialog, self.text.title1)

        def OnActivated1(evt):
            edit1()
            evt.Skip()
        city_grid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, OnActivated1)

        def onButton(evt):
            wid = evt.GetId()
            if wid == bttns[0]:  # Add
                dlg = extDialog(
                    parent=panel,
                    plugin=self,
                    labels=self.text.header1,
                    data=[True, "", ""],
                    grid=city_grid,
                    add=True,
                )
                dlg.Centre()
                wx.CallAfter(dlg.ShowExtDialog, self.text.title1)
            elif wid == bttns[1]:  # Duplicate
                dlg = extDialog(
                    parent=panel,
                    plugin=self,
                    labels=self.text.header1,
                    data=city_grid.GetRow(),
                    grid=city_grid,
                    add=True
                )
                dlg.Centre()
                wx.CallAfter(dlg.ShowExtDialog, self.text.title1)
            elif wid == bttns[2]:  # Edit
                edit1()
            elif wid == bttns[3]:  # Delete
                city_grid.DeleteRow()
            evt.Skip()

        panel.sizer.Add(label1, 0, wx.TOP | wx.LEFT, 5)
        panel.sizer.Add(
            city_grid, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5
        )
        bttnSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        bttnSizer1.Add((5, -1))
        j = 0
        bttns = []
        for bttn in self.text.buttons1:
            try:
                wxid = wx.NewIdRef()
            except AttributeError:
                wxid = wx.NewIdRef()
            bttns.append(wxid)
            b = wx.Button(panel, wxid, bttn)
            bttnSizer1.Add(b, 1)
            if not len(cities) and j not in (0,):
                b.Enable(False)
            if j == 0:
                b.SetDefault()
            b.Bind(wx.EVT_BUTTON, onButton, id=wxid)
            bttnSizer1.Add((5, -1))
            j += 1
        panel.sizer.Add(bttnSizer1, 0, wx.EXPAND)
        apiLabel = wx.StaticText(panel, wx.ID_ANY, text.apiLabel)
        apiCtrl = wx.TextCtrl(
            panel, wx.ID_ANY, api_key.Get(), style=wx.TE_PASSWORD
        )
        lngLabel = wx.StaticText(panel, wx.ID_ANY, text.language)
        choices = list(LANGUAGES.iterkeys())
        choices.sort()
        lngCtrl = wx.Choice(panel, wx.ID_ANY, choices=choices)
        lngCtrl.SetStringSelection(lng)
        uniLabel = wx.StaticText(panel, wx.ID_ANY, text.unitsLbl)
        uniCtrl = wx.Choice(panel, wx.ID_ANY, choices=text.units)
        uniCtrl.SetStringSelection(uni)
        spdLabel = wx.StaticText(panel, wx.ID_ANY, text.windSpeedForm)
        spdCtrl = panel.Choice(spd, choices=text.windSpeed)
        dirLabel = wx.StaticText(panel, wx.ID_ANY, text.windDirForm)
        dirCtrl = panel.Choice(direction, choices=text.windDir)
        prfLabel = wx.StaticText(panel, wx.ID_ANY, text.prefix)
        prfCtrl = wx.TextCtrl(panel, wx.ID_ANY, prf)
        periLbl = wx.StaticText(panel, wx.ID_ANY, self.text.period)
        periCtrl = eg.SpinIntCtrl(panel, wx.ID_ANY, period, min=10, max=720)
        periCtrl.increment = 5
        periCtrl.numCtrl.SetEditable(False)
        evtLabel = wx.StaticText(panel, wx.ID_ANY, self.text.events)
        evtCtrl = CheckListComboBox(
            panel, wx.ID_ANY, values=evtFilter, helpText=text.filter
        )
        mainSizer = wx.GridBagSizer(5, 10)
        mainSizer.Add(apiLabel, (0, 0), flag=ACV)
        mainSizer.Add(apiCtrl, (0, 1), flag=wx.EXPAND)
        mainSizer.Add(lngLabel, (1, 0), flag=ACV)
        mainSizer.Add(lngCtrl, (1, 1))
        mainSizer.Add(uniLabel, (2, 0), flag=ACV)
        mainSizer.Add(uniCtrl, (2, 1))
        mainSizer.Add(spdLabel, (3, 0), flag=ACV)
        mainSizer.Add(spdCtrl, (3, 1), flag=wx.EXPAND)
        mainSizer.Add(dirLabel, (4, 0), flag=ACV)
        mainSizer.Add(dirCtrl, (4, 1), flag=wx.EXPAND)
        mainSizer.Add(prfLabel, (5, 0), flag=ACV)
        mainSizer.Add(prfCtrl, (5, 1))
        mainSizer.Add(periLbl, (6, 0), flag=ACV)
        mainSizer.Add(periCtrl, (6, 1))
        mainSizer.Add(evtLabel, (7, 0), flag=ACV)
        mainSizer.Add(evtCtrl, (7, 1), flag=wx.EXPAND)
        mainSizer.AddGrowableCol(1)
        panel.sizer.Add(mainSizer, 0, wx.EXPAND | wx.ALL, 10)
        
        while panel.Affirmed():
            oldKey = api_key.Get()
            newKey = apiCtrl.GetValue()
            if oldKey != newKey:
                api_key.Set(newKey)
                dummy = int(ttime())
            panel.SetResult(
                (api_key, dummy),
                lngCtrl.GetStringSelection(),
                uniCtrl.GetStringSelection(),
                prfCtrl.GetValue(),
                periCtrl.GetValue(),
                city_grid.GetData(),
                evtCtrl.GetValue()[1],
                spdCtrl.GetValue(),
                dirCtrl.GetValue()
            )


# =============================================================================


class enableCity(eg.ActionBase):

    class text:
        modeLbl = "Select city by:"
        modes = ("City name", "City ID")
        citLbl = "City:"
        unknown = 'Unknown city: "%s"'

    def __call__(self, mode=1, cit=""):
        cit = eg.ParseString(cit)
        tmp = [ct[mode+1] for ct in self.plugin.cities]
        if cit in tmp:
            ix = tmp.index(cit)
            return self.plugin.enableCity(ix, self.value)
        else:
            eg.PrintNotice(self.text.unknown % cit)

    def GetLabel(self, mode, cit):
        return "%s: %s" % (self.name, cit)

    def Configure(self, mode=1, cit=""):
        panel = eg.ConfigPanel(self)
        text = self.text
        modeSizer = wx.BoxSizer(wx.HORIZONTAL)
        modeLbl = wx.StaticText(panel, wx.ID_ANY, text.modeLbl)
        citLbl = wx.StaticText(panel, wx.ID_ANY, text.citLbl)
        rb0 = panel.RadioButton(
            mode == 0, self.text.modes[0], style=wx.RB_GROUP
        )
        rb1 = panel.RadioButton(mode == 1, self.text.modes[1])
        choices = [rp[mode+1] for rp in self.plugin.cities]
        citCtrl = wx.ComboBox(
            panel, wx.ID_ANY, choices=choices, style=wx.CB_DROPDOWN
        )
        citCtrl.SetValue(cit)
        modeSizer.Add(rb0)
        modeSizer.Add(rb1, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(3, 2, 10, 20)
        topSizer.AddGrowableCol(1)
        topSizer.Add(modeLbl)
        topSizer.Add(modeSizer)
        topSizer.Add(citLbl, 0, wx.TOP, 4)
        topSizer.Add(citCtrl, 0, wx.EXPAND)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND)
        panel.sizer.Add(mainSizer, 1, wx.ALL | wx.EXPAND, 10)

        def onRadioBox(evt):
            new = rb1.GetValue()
            ix = 1 + int(not new)
            oldValue = citCtrl.GetValue()
            oldChcs = [ct[ix] for ct in self.plugin.cities]
            oldIx = oldChcs.index(oldValue) if oldValue in oldChcs else -1
            ix = 1 + new
            citCtrl.Clear()
            chces = [ct[ix] for ct in self.plugin.cities]
            citCtrl.SetItems(chces)
            citCtrl.SetSelection(oldIx)
            evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)

        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue()),
                citCtrl.GetValue(),
            )


# =============================================================================


class GetWeather(eg.ActionBase):

    class text:
        modeLbl = "Select city by:"
        modes = ("City name", "City ID")
        citLbl = "City:"

    def __call__(self, mode=1, cit="", resp=1, auto=0):
        autoclose = auto if isinstance(auto, int) else eg.ParseString(auto)
        cit = eg.ParseString(cit)
        tmp = [ct[mode+1] for ct in self.plugin.cities]
        if cit in tmp:
            ix = tmp.index(cit)
            city = None
        else:
            ix = None
            city = cit
        data = self.plugin.getWeather(mode, ix=ix, city=city)
        if not data:
            return
        dtt = data['dt']
        if resp == 2:
            if ix is not None:
                title = self.plugin.cities[ix][1]
            else:
                title = data["name"]
            data = self.plugin.GetShortData(data)
            wx.CallAfter(
                CurrentWeather,
                None,
                self.plugin,
                title,
                dtt,
                data,
                autoclose
            )
            return data
        elif resp == 1:
            return self.plugin.GetShortData(data)  
        else:
            return data

    def GetLabel(self, mode, cit, resp, autoclose):
        return "%s: %s" % (self.name, cit)

    def Configure(self, mode=1, cit="", resp=1, autoclose=0):
        panel = eg.ConfigPanel(self)
        text = self.text
        ptext = self.plugin.text
        modeSizer = wx.BoxSizer(wx.HORIZONTAL)
        modeLbl = wx.StaticText(panel, wx.ID_ANY, text.modeLbl)
        citLbl = wx.StaticText(panel, wx.ID_ANY, text.citLbl)
        autoLbl1 = wx.StaticText(panel, wx.ID_ANY, self.plugin.text.autoclose1)
        autoLbl2 = wx.StaticText(panel, wx.ID_ANY, self.plugin.text.autoclose2)
        autoCtrl = eg.SmartSpinIntCtrl(
            panel, wx.ID_ANY, 5, min=0, max=9999
        )
        autoSizer = wx.BoxSizer(wx.HORIZONTAL)
        autoSizer.Add(autoLbl1, 0, ACV)
        autoSizer.Add(autoCtrl, 0, wx.LEFT | wx.RIGHT, 5)
        autoSizer.Add(autoLbl2, 0, ACV)
        rb0 = panel.RadioButton(
            mode == 0, self.text.modes[0], style=wx.RB_GROUP
        )
        rb1 = panel.RadioButton(mode == 1, self.text.modes[1])
        choices = [rp[mode+1] for rp in self.plugin.cities]
        citCtrl = wx.ComboBox(
            panel, wx.ID_ANY, choices=choices, style=wx.CB_DROPDOWN
        )
        citCtrl.SetValue(cit)
        modeSizer.Add(rb0)
        modeSizer.Add(rb1, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(3, 2, 10, 20)
        topSizer.AddGrowableCol(1)
        topSizer.Add(modeLbl)
        topSizer.Add(modeSizer)
        topSizer.Add(citLbl, 0, wx.TOP, 4)
        topSizer.Add(citCtrl, 0, wx.EXPAND)

        staticBox = wx.StaticBox(panel, label=ptext.respForm)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        rb2 = panel.RadioButton(resp == 0, ptext.forms1[0], style=wx.RB_GROUP)
        rb3 = panel.RadioButton(resp == 1, ptext.forms1[1])
        rb4 = panel.RadioButton(resp == 2, ptext.forms1[2])
        staticBoxSizer.Add(rb2, 0, wx.ALL, 8)
        staticBoxSizer.Add(rb3, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        staticBoxSizer.Add(rb4, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        staticBoxSizer.Add(autoSizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND)
        mainSizer.Add(staticBoxSizer, 0, wx.EXPAND | wx.TOP, 15)
        panel.sizer.Add(mainSizer, 1, wx.ALL | wx.EXPAND, 10)

        def onRadioBox(evt):
            new = rb1.GetValue()
            ix = 1 + int(not new)
            oldValue = citCtrl.GetValue()
            oldChcs = [ct[ix] for ct in self.plugin.cities]
            oldIx = oldChcs.index(oldValue) if oldValue in oldChcs else -1
            ix = 1 + new
            citCtrl.Clear()
            chces = [ct[ix] for ct in self.plugin.cities]
            citCtrl.SetItems(chces)
            citCtrl.SetSelection(oldIx)
            evt.Skip()
        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)

        def onRB4(evt=None):
            enbl = rb4.GetValue()
            if not enbl:
                if not isinstance(
                    autoCtrl.ctrl,
                    eg.Classes.SpinNumCtrl.SpinNumCtrl
                ):
                    autoCtrl.ctrl = autoCtrl.CreateCtrl(0)
                autoCtrl.SetValue(0)
            autoLbl1.Enable(enbl)
            autoLbl2.Enable(enbl)
            autoCtrl.Enable(enbl)
            if evt:
                evt.Skip()
        rb2.Bind(wx.EVT_RADIOBUTTON, onRB4)
        rb3.Bind(wx.EVT_RADIOBUTTON, onRB4)
        rb4.Bind(wx.EVT_RADIOBUTTON, onRB4)
        panel.GetParent().GetParent().Show()
        
        def AfterShow():
            if isinstance(autoclose, int):
                autoCtrl.ctrl = autoCtrl.CreateCtrl(0)
            autoCtrl.SetValue(autoclose)
            autoCtrl.value = autoclose
            onRB4()
        wx.CallAfter(AfterShow)

        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue()),
                citCtrl.GetValue(),
                int(rb3.GetValue()) + 2 * int(rb4.GetValue()),
                autoCtrl.GetValue()
            )


# =============================================================================

class GetForecast(eg.ActionBase):
    class text:
        modeLbl = "Select city by:"
        modes = ("City name", "City ID")
        citLbl = "City:"

    def __call__(self, mode=1, cit="", resp=1, auto=0):
        autoclose = auto if isinstance(auto, int) else eg.ParseString(auto)
        cit = eg.ParseString(cit)
        tmp = [ct[mode + 1] for ct in self.plugin.cities]
        if cit in tmp:
            ix = tmp.index(cit)
            city = None
        else:
            ix = None
            city = cit
        data = self.plugin.getForecast(mode, ix=ix, city=city)
        if not data:
            return
        lst = data['list']
        return lst
        # if resp == 2:
        #    if ix is not None:
        #        title = self.plugin.cities[ix][1]
        #    else:
        #        title = data["name"]
        #    data = self.plugin.GetShortData(data)
        #    wx.CallAfter(
        #        CurrentWeather,
        #        None,
        #        self.plugin,
        #        title,
        #        dtt,
        #        data,
        #        autoclose
        #    )
        #    return data
        # elif resp == 1:
        #    return self.plugin.GetShortData(data)
        # else:
        #    return data

    def GetLabel(self, mode, cit, resp, autoclose):
        return "%s: %s" % (self.name, cit)

    def Configure(self, mode=1, cit="", resp=1, autoclose=0):
        panel = eg.ConfigPanel(self)
        text = self.text
        ptext = self.plugin.text
        modeSizer = wx.BoxSizer(wx.HORIZONTAL)
        modeLbl = wx.StaticText(panel, -1, text.modeLbl)
        citLbl = wx.StaticText(panel, -1, text.citLbl)
        autoLbl1 = wx.StaticText(panel, -1, self.plugin.text.autoclose1)
        autoLbl2 = wx.StaticText(panel, -1, self.plugin.text.autoclose2)
        autoCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            5,
            min=0,
            max=9999
        )
        autoSizer = wx.BoxSizer(wx.HORIZONTAL)
        autoSizer.Add(autoLbl1, 0, ACV)
        autoSizer.Add(autoCtrl, 0, wx.LEFT | wx.RIGHT, 5)
        autoSizer.Add(autoLbl2, 0, ACV)
        rb0 = panel.RadioButton(mode == 0, self.text.modes[0], style=wx.RB_GROUP)
        rb1 = panel.RadioButton(mode == 1, self.text.modes[1])
        choices = [rp[mode + 1] for rp in self.plugin.cities]
        citCtrl = wx.ComboBox(panel, -1, choices=choices, style=wx.CB_DROPDOWN)
        citCtrl.SetValue(cit)
        modeSizer.Add(rb0)
        modeSizer.Add(rb1, 0, wx.LEFT, 10)
        topSizer = wx.FlexGridSizer(3, 2, 10, 20)
        topSizer.AddGrowableCol(1)
        topSizer.Add(modeLbl)
        topSizer.Add(modeSizer)
        topSizer.Add(citLbl, 0, wx.TOP, 4)
        topSizer.Add(citCtrl, 0, wx.EXPAND)

        staticBox = wx.StaticBox(panel, label=ptext.respForm)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        rb2 = panel.RadioButton(resp == 0, ptext.forms1[0], style=wx.RB_GROUP)
        rb3 = panel.RadioButton(resp == 1, ptext.forms1[1])
        rb4 = panel.RadioButton(resp == 2, ptext.forms1[2])
        staticBoxSizer.Add(rb2, 0, wx.ALL, 8)
        staticBoxSizer.Add(rb3, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        staticBoxSizer.Add(rb4, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        staticBoxSizer.Add(autoSizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND)
        mainSizer.Add(staticBoxSizer, 0, wx.EXPAND | wx.TOP, 15)
        panel.sizer.Add(mainSizer, 1, wx.ALL | wx.EXPAND, 10)

        def onRadioBox(evt):
            new = rb1.GetValue()
            ix = 1 + int(not new)
            oldValue = citCtrl.GetValue()
            oldChcs = [ct[ix] for ct in self.plugin.cities]
            oldIx = oldChcs.index(oldValue) if oldValue in oldChcs else -1
            ix = 1 + new
            citCtrl.Clear()
            choices = [ct[ix] for ct in self.plugin.cities]
            citCtrl.SetItems(choices)
            citCtrl.SetSelection(oldIx)
            evt.Skip()

        rb0.Bind(wx.EVT_RADIOBUTTON, onRadioBox)
        rb1.Bind(wx.EVT_RADIOBUTTON, onRadioBox)

        def onRB4(evt=None):
            enbl = rb4.GetValue()
            if not enbl:
                if not isinstance(
                    autoCtrl.ctrl,
                    eg.Classes.SpinNumCtrl.SpinNumCtrl
                ):
                    autoCtrl.ctrl = autoCtrl.CreateCtrl(0)
                autoCtrl.SetValue(0)
            autoLbl1.Enable(enbl)
            autoLbl2.Enable(enbl)
            autoCtrl.Enable(enbl)
            if evt:
                evt.Skip()

        rb2.Bind(wx.EVT_RADIOBUTTON, onRB4)
        rb3.Bind(wx.EVT_RADIOBUTTON, onRB4)
        rb4.Bind(wx.EVT_RADIOBUTTON, onRB4)
        panel.GetParent().GetParent().Show()

        def AfterShow():
            if isinstance(autoclose, int):
                autoCtrl.ctrl = autoCtrl.CreateCtrl(0)
            autoCtrl.SetValue(autoclose)
            autoCtrl.value = autoclose
            onRB4()

        wx.CallAfter(AfterShow)

        while panel.Affirmed():
            panel.SetResult(
                int(rb1.GetValue()),
                citCtrl.GetValue(),
                int(rb3.GetValue()) + 2 * int(rb4.GetValue()),
                autoCtrl.GetValue()
            )

# ===============================================================================


ACTIONS = (
    (
        enableCity,
        "EnableCity",
        "Enable city",
        "Enables selected city.",
        True
    ),
    (
        enableCity,
        "DisableCity",
        "Disable city",
        "Disables selected city.",
        False
    ),
    (
        GetWeather,
        "GetWeather",
        "Get current weather",
        "Gets current weather.",
        None
    ),
    (
        GetForecast,
        "GetForecast",
        "Get forecast",
        "Gets 5 day/3 hour forecast data.",
        None
    ),
)

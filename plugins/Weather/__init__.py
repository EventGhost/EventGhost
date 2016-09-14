# -*- coding: utf-8 -*-
#
# plugins/Weather/__init__.py
#
# Copyright (C) 2009 Peter
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

eg.RegisterPlugin(
    name = "Weather",
    author = "Peter",
    guid = "{E0ED124C-F85C-497B-8FFF-6A2B745F9076}",
    version = "1.2." + "$LastChangedRevision: 1194 $".split()[1],
    kind = "program",
    description = (
        "Uses the Google web service to retrieve current and forecasted weather information."
        "More Info on http://code.google.com/p/python-weather-api/"
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=1996",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAMAAAC7IEhfAAAAwFBMVEXm5uerz+ZocXj9"
        "sw5prO46hteMi4d5goikpKRLnPyRvtqXeTUWbt729va5ubkjeeOhyN83X4scctuevNBY"
        "mdPU09OpqamamZTx8fCwr61ZpPpFd6rt7e3Ozs5jns+XxN99t+ROWGG9ljz/yCr/wiT/"
        "uxvb29v/zjAQat3Dw8PrpRArfNjTlhOFpbafsbX8/Pzh4eGgj12wgBbYoCZNkNFzqdEf"
        "bc/S1t6EtNS42/Gup32ctMIGY9z/1Tfc4ery7eg/BJHWAAACw0lEQVR4Xo3T5W7dQBSF"
        "0ZkxM9NFZoZw2r7/W3Wf8bUc91e/G1mRsrSPIyUs2PzMbdu4mx8FbPPdbfMNj+c/bbqQ"
        "Jl9jfNxXl3yby9yfCmRfF4PDdmHL9nttr9VJTLMdiJdyY2Lao+lpm9WYxVD0amCk0nRE"
        "pWlKmFYxCgFIboM5WoN6eQZNs/tA3sdiAObGwZ4Y1HsTLNFGBoCNG43AbDsJUWLbZEdp"
        "LV2CrutKR3P2OORhkiQh5zyxf0oJg0DT0pRcyL8+Z/f7ffb5eeQhjdbXJZTuIR0Pi4Oi"
        "LJGiHK4Jl5v4jYIgBgzocDqSe9cd0ALB7pwvyOfxALA+LF0Bt5jP1/P5HFRxwtCeQGLS"
        "fWXkLDnIT4flEmz9a72GxabOxzRp7aN+wfpRgMv1YWW5AKNgF0tlhsl3dfSI/D8eu1SR"
        "1ktfJmOezDAI95S4fvjix1E/jYZe6THGqqjfF8Lgp1092E7uDEPPc8M4e+czY5eBKLIs"
        "Owm9hRQtiqz0zll+RmzAytxnF3bxp/8uKg4rAS++hOVgsMpKdsky47abd97xYJ49j1AD"
        "y5Kx1coUhuN0YeGhBg4GA5xnl1V2YW+Gg+ONuzm6ufIoGmYyQLTa+uKwlsE5+e/SK/GS"
        "9RdbtQ393LgtFnNEL4hLeK8mNhxut/4WDbe+WYib/KvAw3l7HmLPqjw3zSLPqyo3dX3q"
        "3BVFWSrKzvGHwww151hR4MdToRf4RkyPH6fiOpvNrifD9CvfxyGU4cGmKLL6U9mR848P"
        "zumZCJOqKuCt7/vM0gLLsnq9Ef5pxuMwDHldeBQCJ3QzR6apMwuRVNX3ycS2YakxehF9"
        "8YiEUci3A9QIppaqqhNkA+Nj2xOkqj0tiujl+s0ijveIyoBIgaHnRcCObCwYItbAntWl"
        "bbTWBtiRsNA9Uh3YXQSVdVQXthickPx0II78T+pfPV2zlElyXK4AAAAASUVORK5CYII="
    )
)


from win32com.client import constants
import win32com.client
import pywapi
import eg
import wx

class Weather(eg.PluginClass):
    weather_data = None

    def __init__(self):
        self.AddAction(GetWeatherFromGoogle)
        self.AddAction(GetCountriesFromGoogle)
        self.AddAction(GetCitiesFromGoogle)
        self.AddAction(GetWeatherFieldValue)
        self.AddAction(LogResult)



class GetWeatherFromGoogle(eg.ActionClass):
    description = (
        "Fetches weather report from Google \n"
        "PARAMETERS: \n"
        "* location_id: a zip code (10001); city name, state (weather=woodland,PA);"
        "city name, country (weather=london, england); latitude/longitude (weather=,,,30670000,104019996) or possibly other.\n"
        "* hl: the language parameter (language code). Default value is empty string, in this case Google will use English.\n"
        "RETURNS: \n"
        "* weather_data: a dictionary of weather data that exists in XML feed.\n"
    )

    class text:
        LocationLabel = "Location:"
        LanguageLabel = "Language Code:"
        CitiesLabel = "Cities:"
        CountriesLabel = "Countries:"

    def __call__(self, location_id , hl):
        self.plugin.weather_data = pywapi.get_weather_from_google(location_id, hl)
        return self.plugin.weather_data

    def Configure(self, location_id = "Antwerp, Belgium", hl=''):

        text=self.text

        dialog = eg.ConfigPanel(self)
        sizer = dialog.sizer
        mySizer = wx.FlexGridSizer(cols=2)

        desc0 = wx.StaticText(dialog, -1, text.LanguageLabel)
        mySizer.Add(desc0, 0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        Language = wx.TextCtrl(dialog, -1,hl)
        mySizer.Add(Language, 0, wx.EXPAND|wx.ALL, 5)

        desc1 = wx.StaticText(dialog, -1, text.LocationLabel)
        mySizer.Add(desc1, 0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        Location = wx.TextCtrl(dialog, -1,location_id)
        mySizer.Add(Location, 0, wx.EXPAND|wx.ALL, 5)

        desc2 = wx.StaticText(dialog, -1, text.CountriesLabel)
        mySizer.Add(desc2, 0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        CountriesEdit = wx.ListBox(dialog, -1, choices=[], style=wx.LB_SINGLE)
        mySizer.Add(CountriesEdit, 0, wx.EXPAND|wx.ALL, 5)
        CountriesEdit.Clear()
        CountryList = pywapi.get_countries_from_google()
        i=0
        while i < len(CountryList):
            CountriesEdit.Append(CountryList[i]['name'])
            i=i+1
        def OnCountrySelect(event):
            CitiesEdit.Clear()
            result = pywapi.get_cities_from_google(str(CountryList[CountriesEdit.GetSelection()]['iso_code']))
            i=0
            while i < len(result):
                 CitiesEdit.Append(result[i]['name'])
                 i=i+1
            Location.SetValue(CitiesEdit.GetStringSelection() + ", " + CountriesEdit.GetStringSelection())
        CountriesEdit.Bind(wx.EVT_LISTBOX, OnCountrySelect)

        desc3 = wx.StaticText(dialog, -1, text.CitiesLabel)
        mySizer.Add(desc3, 0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        CitiesEdit = wx.ListBox(dialog, -1, choices=[], style=wx.LB_SINGLE)
        mySizer.Add(CitiesEdit, 0, wx.EXPAND|wx.ALL, 5)
        def OnCitySelect(event):
            Location.SetValue(CitiesEdit.GetStringSelection() + ", " + CountriesEdit.GetStringSelection())
        CitiesEdit.Bind(wx.EVT_LISTBOX, OnCitySelect)

        sizer.Add(mySizer, 1, wx.EXPAND)

        while dialog.Affirmed():
            dialog.SetResult(Location.GetValue(), Language.GetValue())



class GetCountriesFromGoogle(eg.ActionClass):
    description = (
        "Get list of countries in specified language from Google \n"
        "PARAMETERS: \n"
        "* hl: the language parameter (language code). Default value is empty string, in this case Google will use English. \n"
        "RETURNS: \n"
        "* countries: a list of elements(all countries that exists in XML feed). Each element is a dictionary with 'name' and 'iso_code' keys. \n"
        "  For example: [{'iso_code': 'US', 'name': 'USA'}, {'iso_code': 'FR', 'name': 'France'}] \n"
    )

    class text:
        LanguageLabel = "Language Code:"

    def __call__(self, hl):
        return pywapi.get_countries_from_google(hl)

    def Configure(self, hl=''):

        text=self.text

        dialog = eg.ConfigPanel(self)
        sizer = dialog.sizer
        mySizer = wx.FlexGridSizer(cols=2)

        desc0 = wx.StaticText(dialog, -1, text.LanguageLabel)
        mySizer.Add(desc0, 0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        Language = wx.TextCtrl(dialog, -1,hl)
        mySizer.Add(Language, 0, wx.EXPAND|wx.ALL, 5)

        sizer.Add(mySizer, 1, wx.EXPAND)

        while dialog.Affirmed():
            dialog.SetResult(Language.GetValue())



class GetCitiesFromGoogle(eg.ActionClass):
    description = (
        "Get list of cities of necessary country in specified language from Google \n"
        "PARAMETERS: \n"
        "* country_code: code of the necessary country. For example 'de' or 'fr'. \n"
        "* hl: the language parameter (language code). Default value is empty string, in this case Google will use English. \n"
        "RETURNS: \n"
        "* cities: a list of elements(all cities that exists in XML feed). Each element is a dictionary with 'name', 'latitude_e6' and 'longitude_e6' keys. For example: [{'longitude_e6': '1750000', 'name': 'Bourges', 'latitude_e6': '47979999'}] \n"
    )
    class text:
        LanguageLabel = "Language Code:"
        CountryCodeLabel = "Country Code:"

    def __call__(self, country_code, hl):
        return pywapi.get_cities_from_google(country_code, hl)

    def Configure(self, country_code="be", hl=''):

        text=self.text

        dialog = eg.ConfigPanel(self)
        sizer = dialog.sizer
        mySizer = wx.FlexGridSizer(cols=2)

        desc0 = wx.StaticText(dialog, -1, text.LanguageLabel)
        mySizer.Add(desc0, 0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        Language = wx.TextCtrl(dialog, -1,hl)
        mySizer.Add(Language, 0, wx.EXPAND|wx.ALL, 5)

        desc1 = wx.StaticText(dialog, -1, text.CountryCodeLabel)
        mySizer.Add(desc1, 0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        Country = wx.TextCtrl(dialog, -1,country_code)
        mySizer.Add(Country , 0, wx.EXPAND|wx.ALL, 5)

        sizer.Add(mySizer, 1, wx.EXPAND)

        while dialog.Affirmed():
            dialog.SetResult(Country.GetValue(),Language.GetValue())



class GetWeatherFieldValue(eg.ActionClass):
    description = (
        "Get a particular parameter value from the earlier retrieved Weather Information from Google \n"
        "PARAMETERS: \n"
        "* parameter_name: Name of the parameter \n"
        "RETURNS: \n"
        "* parameter_value: Value for the requested parameter \n"
    )
    class text:
        ParameterName1Label = "Parameter1:"
        ParameterName2Label = "Parameter2:"
        ParameterName3Label = "Forecast day-index:"

    def __call__(self, parameter_name1, parameter_name2, parameter_name3):
        if self.plugin.weather_data is None:
             return None
        elif parameter_name1 == "" and parameter_name2 == "":
             return self.plugin.weather_data
        elif parameter_name1 <> "" and parameter_name2 == "":
             return self.plugin.weather_data[parameter_name1]
        else:
             if type( self.plugin.weather_data[parameter_name1] ) == type (list()):
                 return self.plugin.weather_data[parameter_name1][parameter_name3][parameter_name2]
             else:
                 return self.plugin.weather_data[parameter_name1][parameter_name2]

    def Configure(self, parameter_name1="", parameter_name2="", parameter_name3=0):

        text=self.text

        dialog = eg.ConfigPanel(self)
        sizer = dialog.sizer
        mySizer = wx.FlexGridSizer(cols=3)

        desc1 = wx.StaticText(dialog, -1, text.ParameterName1Label)
        mySizer.Add(desc1, 0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        ParameterName1 = wx.TextCtrl(dialog, -1,parameter_name1)
        ParameterName1.SetEditable(False)
        mySizer.Add(ParameterName1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        weatherkeys1= []
        if self.plugin.weather_data:
            weatherkeys1= self.plugin.weather_data.keys()
        else:
            eg.PrintError("Before configuring GetWeatherFieldValue Action, first execute GetWeatherFromGoogle Action Once sucessfully to retrieve available fields.")
        ParameterEdit1 = wx.ListBox(dialog, -1, choices= weatherkeys1, style=wx.LB_SINGLE)
        mySizer.Add(ParameterEdit1, 0, wx.EXPAND|wx.ALL, 5)

        def OnParameterEdit1Select(event):
            ParameterName1.SetValue(ParameterEdit1.GetStringSelection())
            ParameterName2.SetValue("")
            ParameterName3.SetValue("")
            ParameterEdit2.Clear()
            ParameterEdit2.InsertItems(RefreshWeatherkeys2(),0)
            ParameterEdit3.Clear()
            ParameterEdit3.InsertItems(RefreshWeatherkeys3(),0)
        ParameterEdit1.Bind(wx.EVT_LISTBOX, OnParameterEdit1Select)

        desc2 = wx.StaticText(dialog, -1, text.ParameterName2Label)
        mySizer.Add(desc2, 0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        ParameterName2 = wx.TextCtrl(dialog, -1,parameter_name2)
        ParameterName2.SetEditable(False)
        mySizer.Add(ParameterName2 , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        def RefreshWeatherkeys2():
            weatherkeys2= []
            if self.plugin.weather_data and ParameterName1.GetValue() in weatherkeys1 :
                if type( self.plugin.weather_data[ParameterName1.GetValue()] ) == type (dict()):
                    weatherkeys2= self.plugin.weather_data[ParameterName1.GetValue()].keys()
                elif type( self.plugin.weather_data[ParameterName1.GetValue()] ) == type (list()):
                    weatherkeys2= self.plugin.weather_data[ParameterName1.GetValue()][0].keys()
            return weatherkeys2

        ParameterEdit2 = wx.ListBox(dialog, -1, choices= RefreshWeatherkeys2(), style=wx.LB_SINGLE)
        mySizer.Add(ParameterEdit2, 0, wx.EXPAND|wx.ALL, 5)

        def OnParameterEdit2Select(event):
            ParameterName2.SetValue(ParameterEdit2.GetStringSelection())
        ParameterEdit2.Bind(wx.EVT_LISTBOX, OnParameterEdit2Select)

        desc3 = wx.StaticText(dialog, -1, text.ParameterName3Label)
        mySizer.Add(desc3, 0,  wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        ParameterName3 = wx.TextCtrl(dialog, -1,str(parameter_name3))
        ParameterName3.SetEditable(False)
        mySizer.Add(ParameterName3 , 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        def RefreshWeatherkeys3():
            weatherkeys3= []
            if self.plugin.weather_data and ParameterName1.GetValue() in weatherkeys1 :
                if type( self.plugin.weather_data[ParameterName1.GetValue()] ) == type (list()):
                    weatherkeys3= map (str , range(0 , len(self.plugin.weather_data[ParameterName1.GetValue()]) ))
            return weatherkeys3

        ParameterEdit3 = wx.ListBox(dialog, -1, choices= RefreshWeatherkeys3(), style=wx.LB_SINGLE)
        mySizer.Add(ParameterEdit3, 0, wx.EXPAND|wx.ALL, 5)

        def OnParameterEdit3Select(event):
            ParameterName3.SetValue(ParameterEdit3.GetStringSelection())
        ParameterEdit3.Bind(wx.EVT_LISTBOX, OnParameterEdit3Select)

        sizer.Add(mySizer, 1, wx.EXPAND)

        while dialog.Affirmed():
            dialog.SetResult(ParameterName1.GetValue(),ParameterName2.GetValue(),ParameterEdit3.GetSelection())



class LogResult(eg.ActionClass):
    description = (
        "Shows the returned information from the previous Action in the EventGhost Log\n"
    )


    def __call__(self):
        eg.Print(eg.result)
        return eg.result


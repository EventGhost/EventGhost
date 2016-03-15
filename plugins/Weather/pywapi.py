#Copyright (c) 2009 Eugene Kaznacheev <qetzal@gmail.com>

#Permission is hereby granted, free of charge, to any person
#obtaining a copy of this software and associated documentation
#files (the "Software"), to deal in the Software without
#restriction, including without limitation the rights to use,
#copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the
#Software is furnished to do so, subject to the following
#conditions:

#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#OTHER DEALINGS IN THE SOFTWARE.

"""
Fetches weather reports from Google Weather, Yahoo Wheather and NOAA
"""

import urllib2, re
from xml.dom import minidom
from urllib import quote

GOOGLE_WEATHER_URL   = 'http://www.google.com/ig/api?weather=%s&hl=%s'
GOOGLE_COUNTRIES_URL = 'http://www.google.com/ig/countries?output=xml&hl=%s'
GOOGLE_CITIES_URL    = 'http://www.google.com/ig/cities?output=xml&country=%s&hl=%s'

YAHOO_WEATHER_URL    = 'http://xml.weather.yahoo.com/forecastrss?p=%s&u=%s'
YAHOO_WEATHER_NS     = 'http://xml.weather.yahoo.com/ns/rss/1.0'

NOAA_WEATHER_URL     = 'http://www.weather.gov/xml/current_obs/%s.xml'

def get_weather_from_google(location_id, hl = ''):
    """
    Fetches weather report from Google

    Parameters
      location_id: a zip code (10001); city name, state (weather=woodland,PA); city name, country (weather=london, england);
      latitude/longitude(weather=,,,30670000,104019996) or possibly other.
      hl: the language parameter (language code). Default value is empty string, in this case Google will use English.

    Returns:
      weather_data: a dictionary of weather data that exists in XML feed.
    """
    location_id, hl = map(quote, (location_id, hl))
    url = GOOGLE_WEATHER_URL % (location_id, hl)
    handler = urllib2.urlopen(url)
    content_type = handler.info().dict['content-type']
    charset = re.search('charset\=(.*)',content_type).group(1)
    if not charset:
        charset = 'utf-8'
    if charset.lower() != 'utf-8':
        xml_response = handler.read().decode(charset).encode('utf-8')
    else:
        xml_response = handler.read()
    dom = minidom.parseString(xml_response)
    handler.close()

    weather_data = {}
    weather_dom = dom.getElementsByTagName('weather')[0]

    data_structure = {
        'forecast_information': ('city', 'postal_code', 'latitude_e6', 'longitude_e6', 'forecast_date', 'current_date_time', 'unit_system'),
        'current_conditions': ('condition','temp_f', 'temp_c', 'humidity', 'wind_condition', 'icon')
    }
    for (tag, list_of_tags2) in data_structure.iteritems():
        tmp_conditions = {}
        for tag2 in list_of_tags2:
            try:
                tmp_conditions[tag2] =  weather_dom.getElementsByTagName(tag)[0].getElementsByTagName(tag2)[0].getAttribute('data')
            except IndexError:
                pass
        weather_data[tag] = tmp_conditions

    forecast_conditions = ('day_of_week', 'low', 'high', 'icon', 'condition')
    forecasts = []

    for forecast in dom.getElementsByTagName('forecast_conditions'):
        tmp_forecast = {}
        for tag in forecast_conditions:
            tmp_forecast[tag] = forecast.getElementsByTagName(tag)[0].getAttribute('data')
        forecasts.append(tmp_forecast)

    weather_data['forecasts'] = forecasts
    dom.unlink()

    return weather_data

def get_countries_from_google(hl = ''):
    """
    Get list of countries in specified language from Google

    Parameters
      hl: the language parameter (language code). Default value is empty string, in this case Google will use English.
    Returns:
      countries: a list of elements(all countries that exists in XML feed). Each element is a dictionary with 'name' and 'iso_code' keys.
      For example: [{'iso_code': 'US', 'name': 'USA'}, {'iso_code': 'FR', 'name': 'France'}]
    """
    url = GOOGLE_COUNTRIES_URL % hl

    handler = urllib2.urlopen(url)
    content_type = handler.info().dict['content-type']
    charset = re.search('charset\=(.*)',content_type).group(1)
    if not charset:
        charset = 'utf-8'
    if charset.lower() != 'utf-8':
        xml_response = handler.read().decode(charset).encode('utf-8')
    else:
        xml_response = handler.read()
    dom = minidom.parseString(xml_response)
    handler.close()

    countries = []
    countries_dom = dom.getElementsByTagName('country')

    for country_dom in countries_dom:
        country = {}
        country['name'] = country_dom.getElementsByTagName('name')[0].getAttribute('data')
        country['iso_code'] = country_dom.getElementsByTagName('iso_code')[0].getAttribute('data')
        countries.append(country)

    dom.unlink()
    return countries

def get_cities_from_google(country_code, hl = ''):
    """
    Get list of cities of necessary country in specified language from Google

    Parameters
      country_code: code of the necessary country. For example 'de' or 'fr'.
      hl: the language parameter (language code). Default value is empty string, in this case Google will use English.
    Returns:
      cities: a list of elements(all cities that exists in XML feed). Each element is a dictionary with 'name', 'latitude_e6' and 'longitude_e6' keys. For example: [{'longitude_e6': '1750000', 'name': 'Bourges', 'latitude_e6': '47979999'}]
    """
    url = GOOGLE_CITIES_URL % (country_code.lower(), hl)

    handler = urllib2.urlopen(url)
    content_type = handler.info().dict['content-type']
    charset = re.search('charset\=(.*)',content_type).group(1)
    if not charset:
        charset = 'utf-8'
    if charset.lower() != 'utf-8':
        xml_response = handler.read().decode(charset).encode('utf-8')
    else:
        xml_response = handler.read()
    dom = minidom.parseString(xml_response)
    handler.close()

    cities = []
    cities_dom = dom.getElementsByTagName('city')

    for city_dom in cities_dom:
        city = {}
        city['name'] = city_dom.getElementsByTagName('name')[0].getAttribute('data')
        city['latitude_e6'] = city_dom.getElementsByTagName('latitude_e6')[0].getAttribute('data')
        city['longitude_e6'] = city_dom.getElementsByTagName('longitude_e6')[0].getAttribute('data')
        cities.append(city)

    dom.unlink()

    return cities

def get_weather_from_yahoo(location_id, units = 'metric'):
    """
    Fetches weather report from Yahoo!

    Parameters
    location_id: A five digit US zip code or location ID. To find your location ID,
    browse or search for your city from the Weather home page(http://weather.yahoo.com/)
    The weather ID is in the URL for the forecast page for that city. You can also get the location ID by entering your zip code on the home page. For example, if you search for Los Angeles on the Weather home page, the forecast page for that city is http://weather.yahoo.com/forecast/USCA0638.html. The location ID is USCA0638.

    units: type of units. 'metric' for metric and '' for  non-metric
    Note that choosing metric units changes all the weather units to metric, for example, wind speed will be reported as kilometers per hour and barometric pressure as millibars.

    Returns:
    weather_data: a dictionary of weather data that exists in XML feed. See  http://developer.yahoo.com/weather/#channel
    """
    location_id = quote(location_id)
    if units == 'metric':
        unit = 'c'
    else:
        unit = 'f'
    url = YAHOO_WEATHER_URL % (location_id, unit)
    handler = urllib2.urlopen(url)
    dom = minidom.parse(handler)
    handler.close()

    weather_data = {}
    weather_data['title'] = dom.getElementsByTagName('title')[0].firstChild.data
    weather_data['link'] = dom.getElementsByTagName('link')[0].firstChild.data

    ns_data_structure = {
        'location': ('city', 'region', 'country'),
        'units': ('temperature', 'distance', 'pressure', 'speed'),
        'wind': ('chill', 'direction', 'speed'),
        'atmosphere': ('humidity', 'visibility', 'pressure', 'rising'),
        'astronomy': ('sunrise', 'sunset'),
        'condition': ('text', 'code', 'temp', 'date')
    }

    for (tag, attrs) in ns_data_structure.iteritems():
        weather_data[tag] = xml_get_ns_yahoo_tag(dom, YAHOO_WEATHER_NS, tag, attrs)

    weather_data['geo'] = {}
    weather_data['geo']['lat'] = dom.getElementsByTagName('geo:lat')[0].firstChild.data
    weather_data['geo']['long'] = dom.getElementsByTagName('geo:long')[0].firstChild.data

    weather_data['condition']['title'] = dom.getElementsByTagName('item')[0].getElementsByTagName('title')[0].firstChild.data
    weather_data['html_description'] = dom.getElementsByTagName('item')[0].getElementsByTagName('description')[0].firstChild.data

    forecasts = []
    for forecast in dom.getElementsByTagNameNS(YAHOO_WEATHER_NS, 'forecast'):
        forecasts.append(xml_get_attrs(forecast,('date', 'low', 'high', 'text', 'code')))
    weather_data['forecasts'] = forecasts

    dom.unlink()

    return weather_data



def get_weather_from_noaa(station_id):
    """
    Fetches weather report from NOAA: National Oceanic and Atmospheric Administration (United States)

    Parameter:
    station_id: the ID of the weather station near the necessary location
    To find your station ID, perform the following steps:
    1. Open this URL: http://www.weather.gov/xml/current_obs/seek.php?state=az&Find=Find
    2. Select the necessary state state. Click 'Find'.
    3. Find the necessary station in the 'Observation Location' column.
    4. The station ID is in the URL for the weather page for that station.
    For example if the weather page is http://weather.noaa.gov/weather/current/KPEO.html -- the station ID is KPEO.

    Other way to get the station ID: use this library: http://code.google.com/p/python-weather/ and 'Weather.location2station' function.

    Returns:
    weather_data: a dictionary of weather data that exists in XML feed.

    (useful icons: http://www.weather.gov/xml/current_obs/weather.php)
    """
    station_id = quote(station_id)
    url = NOAA_WEATHER_URL % (station_id)
    handler = urllib2.urlopen(url)
    dom = minidom.parse(handler)
    handler.close()

    data_structure = ('suggested_pickup',
                'suggested_pickup_period',
                'location',
                'station_id',
                'latitude',
                'longitude',
                'observation_time',
                'observation_time_rfc822',
                'weather',
                'temperature_string',
                'temp_f',
                'temp_c',
                'relative_humidity',
                'wind_string',
                'wind_dir',
                'wind_degrees',
                'wind_mph',
                'wind_gust_mph',
                'pressure_string',
                'pressure_mb',
                'pressure_in',
                'dewpoint_string',
                'dewpoint_f',
                'dewpoint_c',
                'heat_index_string',
                'heat_index_f',
                'heat_index_c',
                'windchill_string',
                'windchill_f',
                'windchill_c',
                'icon_url_base',
                'icon_url_name',
                'two_day_history_url',
                'ob_url'
                )
    weather_data = {}
    current_observation = dom.getElementsByTagName('current_observation')[0]
    for tag in data_structure:
        try:
            weather_data[tag] = current_observation.getElementsByTagName(tag)[0].firstChild.data
        except IndexError:
            pass

    dom.unlink()
    return weather_data



def xml_get_ns_yahoo_tag(dom, ns, tag, attrs):
    """
    Parses the necessary tag and returns the dictionary with values

    Parameters:
    dom - DOM
    ns - namespace
    tag - necessary tag
    attrs - tuple of attributes

    Returns: a dictionary of elements
    """
    element = dom.getElementsByTagNameNS(ns, tag)[0]
    return xml_get_attrs(element,attrs)


def xml_get_attrs(xml_element, attrs):
    """
    Returns the list of necessary attributes

    Parameters:
    element: xml element
    attrs: tuple of attributes

    Return: a dictionary of elements
    """

    result = {}
    for attr in attrs:
        result[attr] = xml_element.getAttribute(attr)
    return result


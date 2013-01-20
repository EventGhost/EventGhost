#Simple place holder and classification for possible
#weather conditions retrieved from Yahoo! Weather used
#by SunTracker plugin to compensate lights for weather
#impacts 

def weather_conditions_dark():
    list = [
        "Cloudy", 
        "Haze", 
        "Fog",
        "Overcast", 
        "Light Rain/Fog",
        "Light Rain",
        "Heavy Rain", 
        "Rain", 
        "Rain Showers",
        "Rain Shower",
        "Light Rain Shower",
        "Freezing Rain",
        "Freezing Drizzle",
        "Light Drizzle",
        "Drizzle",
        "Flurries",
        "Rain and Snow",
        "Showers",
        "Showers in the Vicinity",
        "Isolated Thunderstorms",
        "Thunderstorm",
        "Chance of Showers", 
        "Chance of Snow", 
        "Chance of Storm", 
        "Scattered Showers",
        "Mist",
        "Dust",
        "Icy",
        "Smoke",
        "Sleet"
    ]
    return list


def weather_conditions_half_bright():
    list = [
        "Snow",
        "Light snow",
        "Snow Showers",
        "Mostly Cloudy", 
        "Ice/Snow",
        "Haze", 
        "Partly Cloudy"
    ]
    return list


def weather_conditions_bright():
    list = [
        "Fair", 
        "Clear", 
        "Sunny",
        "Mostly Sunny",
        "Partly Sunny" 
    ]
    return list


def weather_conditions_except():
    list = [
        "Unavailable",
        "Undefined",
        "Unknown"
    ]
    return list

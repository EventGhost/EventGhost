#Simple place holder and classification for possible
#weather conditions retrieved from Yahoo! Weather used
#by SunTracker plugin to compensate lights for weather
#impacts

def doLogToFile():
    return False

def weather_conditions_dark():
    list = [
        "Cloudy",
        "Haze",
        "Fog",
        "Shallow Fog",
        "Partial Fog",
        "Overcast",
        "Light Rain/Fog",
        "Light Rain",
        "Heavy Rain",
        "Rain",
        "Heavy Rain Shower",
        "Rain Showers",
        "Rain Shower",
        "Light Rain with Thunder",
        "Light Rain Shower",
        "Light Freezing Rain",
        "Light Freezing Rain/Sleet",
        "Light Rain/Freezing Rain",
        "Freezing Rain",
        "Freezing Drizzle",
        "Sleet and Freezing Rain",
        "Light Freezing Drizzle",
        "Light Drizzle",
        "Heavy Drizzle",
        "Drizzle",
        "Flurries",
        "Rain and Snow",
        "Showers",
        "Showers in the Vicinity",
        "Isolated Thunderstorms",
        "Thunderstorm",
        "Thunder in the Vicinity",
        "Thunder",
        "Chance of Showers",
        "Chance of Snow",
        "Chance of Storm",
        "Scattered Showers",
        "Mist",
        "Dust",
        "Icy",
        "Smoke",
        "Light Sleet",
        "Sleet"
    ]
    return list


def weather_conditions_half_bright():
    list = [
        "Heavy Snow",
        "Snow Shower",
        "Snow",
        "Light Snow",
        "Light Snow Shower",
        "Light Snow Grains",
        "Snow Showers",
        "Snow Grains",
        "Wintry Mix",
        "Mostly Cloudy",
        "Mostly Cloudy/Windy",
        "Ice/Snow",
        "Ice Crystals",
        "Haze",
        "Partly Cloudy"
    ]
    return list


def weather_conditions_bright():
    list = [
        "Fair",
        "Fair/Windy",
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

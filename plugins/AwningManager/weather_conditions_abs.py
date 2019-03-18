#Simple place holder and classification for possible
#weather conditions retrieved from Yahoo! Weather used
#by AwningManager plugin to adjust for weather impacts 

def weather_conditions_not_allowed():
    list = [
        "Fog",
        "Shallow Fog",
        "Partial Fog",
        "Haze", 
        "Light Rain/Fog",
        "Light Rain",
        "Overcast", 
        "Heavy Rain", 
        "Rain", 
        "Rain Showers",
        "Rain Shower",
        "Light Rain Shower",
        "Ice/Snow",
        "Ice Crystals",
        "Sleet and Freezing Rain",
        "Freezing Rain",
        "Light Freezing Rain",
        "Light Freezing Rain/Sleet",
        "Light Rain/Freezing Rain",
        "Freezing Drizzle",
        "Light Freezing Drizzle",
        "Light Drizzle",
        "Heavy Drizzle",
        "Drizzle",
        "Flurries",
        "Rain and Snow",
        "Showers in the Vicinity",
        "Showers",
        "Heavy Snow",
        "Snow",
        "Snow Shower",
        "Light Snow",
        "Light Snow Grains",
        "Light Snow Shower",
        "Snow Showers",
        "Snow Grains",
        "Wintry Mix",
        "Fair/Windy", 
        "Mostly Cloudy/Windy", 
        "Isolated Thunderstorms",
        "Light Rain with Thunder",
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


def weather_conditions_allowed():
    list = [
        "Fair", 
        "Cloudy", 
        "Partly Cloudy",
        "Mostly Cloudy", 
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

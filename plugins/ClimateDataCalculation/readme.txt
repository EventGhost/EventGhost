ClimateDataCalculation

This plugin can be used to collect and calculate climate data like rain level, temperature and humidity from wireless sensors.

- Wind, rain, temperature and humidity data can be collected with a RFXtrx
- Temperature and humidity data can be collected with a TellStick Duo (I am lacking a TellStick Duo log sample from a wind and rain sensor to complete the code)
- Data from other devices like z-wave and 1-wire can easily be added and is on the 'ToDo list' but I need sample events from the EG log.

The plugin supports the following features:
- You can configure how frequently you want to save readings (default every 10 minutes)
- For rain, the plugin calculates two moving averages, one fast and one slow. This is then used to create events when the lines are crossing each other. The more readings you select, the slower the response to changes. This is a very useful function to when you are looking for trend shifts (in this case, if rain is increasing or decreasing during time).
- In addition you can add a hysteresis value that will set the upper and lower band (+/- hysteresis/2) for the fast moving average before it triggers an event
- For temperature and humidity, the plugin calculates one moving average. This is then used in combination with the set-point and optionally the hysteresis to create events when the lines are crossing each other. The more readings you select, the slower the response to changes. This is a very useful function to avoid too many status changes when for instance controlling heaters with on/off control equipment (you might temporary open a door or window but the heater should not react immediately)
- In addition you can add a hysteresis value that will set the upper and lower band (set-point +/- hysteresis/2) for the moving average before it triggers an event
- You can select if you want to use the rule evaluation that will generate those events or not. Currently I have only one rule 'equal-less-greater' that will generate events when moving average gets equal, less or greater than its reference.

All this works for rain level, temperature and humidity data. For wind, capturing of data is covering direction, average strength and gust.

To collect data I use actions in macros. This simplifies your configuration, you just drag & drop the sensor event in the macro you created.

Sensor data is collected on a per sensor exclusive sqlite3 database table. The more frequent you have selected to store data, the quicker the size of your database will grow.

For all sensor types, the following actions are available
- A capture action to capture sensor data
- A combined report action that can generate a html file for specified date & time range like last 24 hours, last 7 days etc etc
- A reset action to clear all readings captured from the sensor

Currently only available for rain level data you also have the following actions
- RainRequestSearch event triggered action searching for total rain between in event payload provided date & time stamps
- RainRequestQuery action searching for total rain between provided date & time stamps and returning the result as variable, foreseen to be used in scripts or other plugins using rain data
- Sending data search results via web-sockets to update web pages with current rain data (supports both Pako's Websocket Suite and Tornado)

The plugin handles also the known situation when you need to change batteries in the sensor. In this case the sensor id will most likely change. A rain sensor will also start counting from zero again. If you update the sensor id of the existing sensor database, the collecting of readings to the database will continue as before.


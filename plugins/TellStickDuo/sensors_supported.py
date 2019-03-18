# Simple place holder for sensor brands to be supported
# by the TellStickDuo plugin.
# Events from sensor brands listed below will be captured.
#
# Remove or add further brands in the list below. 


# Setting up the filtering:

# This is the sample default content that will accept
# messages from the listed sensor brands:

def sensors_supported():
    list = [
        "mandolyn", 
        "oregon",
        "fineoffset"
    ]
    return list

# If you preferre, you can for instance filter down to
# types and even id level.This example
# would set the filtering to accept only Oregon sensors
# of type 1AD2:

#def sensors_supported():
#    list = [
#        "oregon|1A2D"
#    ]
#    return list

# This filter would do the same for Oregon and UPM/ESIC
# sensors and in addition, only accept specified id's:

#def sensors_supported():
#    list = [
#        "oregon|1A2D|21",
#        "oregon|1A2D|11",
#        "oregon|1A2D|32",
#        "mandolyn|temperaturehumidity|11",
#        "mandolyn|temperaturehumidity|81"
#    ]
#    return list
#


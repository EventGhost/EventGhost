# Simple place holder for device states to be monitored 
# by the TellStickDuo plugin.
#
# States of devices listed below will be kept in memory.
# All other devices will not be monitored.
#
# Remove or add devices in the list below. Use the name as
# it is seen in Telldus Center. 

# Setting up the filtering:

# This is the sample default that will capture
# states of the listed devices:

def devices_supported():
    list = [
        "Magnetkontakt", 
        "IR-detektor"
    ]
    return list


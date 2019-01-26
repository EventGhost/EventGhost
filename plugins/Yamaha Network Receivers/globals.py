# static / constants

ALL_MODELS = [ 'ANY', 
               '', 
               'RX-V867', 'RX-V1067', 'RX-V2067',
               '',
               'RX-V671', 'RX-V871',
               '',
               'RX-V473', 'RX-V573', 'RX-V673', 'RX-V773',
               '',
               'RX-V475', 'RX-V575', 'RX-V675', 'RX-V775',
               '',
               'RX-V381', 'RX-V481', 'RX-V581', 'RX-V681', 'RX-V781',
               '',
               'TSR-5790']

# NUMCHAR_CODES[zone][action]
NUMCHAR_CODES = {
    1: { '1': '7F0151AE',
         '2': '7F0152AD',
         '3': '7F0153AC',
         '4': '7F0154AB',
         '5': '7F0155AA',
         '6': '7F0156A9',
         '7': '7F0157A8',
         '8': '7F0158A7',
         '9': '7F0159A6',
         '0': '7F015AA5',
       '+10': '7F015BA4',
       'ENT': '7F015CA3' },
    2: { '1': '7F01718F',
         '2': '7F01728C',
         '3': '7F01738D',
         '4': '7F01748A',
         '5': '7F01758B',
         '6': '7F017688',
         '7': '7F017789',
         '8': '7F017886',
         '9': '7F017986',
         '0': '7F017A84',
       '+10': '7F017B85',
       'ENT': '7F017C82' }
}

# OPERATION_CODES[zone][action]
OPERATION_CODES = {
    1: { 'Play': '7F016897',
         'Stop': '7F016996',
         'Pause': '7F016798',
         'Search-': '7F016A95',
         'Search+': '7F016E94',
         'Skip-': '7F016C93',
         'Skip+': '7F016D92',
         'FM': '7F015827',
         'AM': '7F01552A' },
    2: { 'Play': '7F018876',
         'Stop': '7F018977',
         'Pause': '7F018779',
         'Search-': '7F018A74',
         'Search+': '7F018B75',
         'Skip-': '7F018C72',
         'Skip+': '7F018D73',
         'FM': '7F015927',
         'AM': '7F015628' }
}

# CURSOR_CODES[zone][action]
CURSOR_CODES = {
    1: { 'Up': '7A859D62',
         'Down': '7A859C63',
         'Left': '7A859F60',
         'Right': '7A859E61',
         'Enter': '7A85DE21',
         'Return': '7A85AA55',
         'Level': '7A858679',
         'On Screen': '7A85847B',
         'Option': '7A856B14',
         'Top Menu': '7A85A0DF',
         'Pop Up Menu': '7A85A4DB' },
    2: { 'Up': '7A852B55',
         'Down': '7A852C52',
         'Left': '7A852D53',
         'Right': '7A852E50',
         'Enter': '7A852F51',
         'Return': '7A853C42',
         'Option': '7A856C12',
         'Top Menu': '7A85A1DF',
         'Pop Up Menu': '7A85A5DB' },
    }

# Objects used in the GetInfo action
MENU_OBJECTS = [ 'Menu Layer', 'Menu Name' ]
LINE_OBJECTS = [ 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line' ]
GENERIC_PLAYBACK_OBJECTS = [ 'Playback Info', 'Repeat Mode', 'Shuffle', 'Artist', 'Album', 'Song' ] + MENU_OBJECTS + LINE_OBJECTS
ZONE_OBJECTS = [ 'Power', 'Sleep', 'Volume Level', 'Mute', 'Input Selection', 'Scene', 'Init Volume Mode', 'Init Volume Level', 'Max Volume Level' ]
MAIN_ZONE_OBJECTS = ZONE_OBJECTS + [ 'Straight', 'Enhancer', 'Sound Program', 'Treble', 'Bass' ]
NET_RADIO_OBJECTS = [ 'Playback Info', 'Station' ] + MENU_OBJECTS + LINE_OBJECTS
PANDORA_OBJECTS = [ 'Playback Info', 'Station', 'Album', 'Song' ] + MENU_OBJECTS + LINE_OBJECTS
SIRIUS_IR_OBJECTS = [ 'Playback Info', 'Artist', 'Channel', 'Title' ] + MENU_OBJECTS + LINE_OBJECTS
SIRIUS_OBJECTS = [ 'Antenna Strength', 'Category', 'Channel Number', 'Channel Name', 'Artist', 'Song', 'Composer' ]
SYSTEM_OBJECTS = [ 'Active Speakers', 'PreOut Levels' ]

# Supported zone definitions
ALL_ZONES = [ 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D' ]
ALL_ZONES_PLUS_ACTIVE = [ 'Active Zone' ] + ALL_ZONES
TWO_ZONES = [ 'Main Zone', 'Zone 2' ]
TWO_ZONES_PLUS_ACTIVE = [ 'Active Zone' ] + TWO_ZONES

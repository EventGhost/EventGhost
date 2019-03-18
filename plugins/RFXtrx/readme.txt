##############################################################################
# Revision history:
#
# 2017-01-13  Walter Kraembring: Added support for FW release 433_1013
#                                Lighting5 - Kangtai, Cotech
#                                RFY Centralis commands (> 2 seconds)
# 2016-12-18  Walter Kraembring: Added support for FW release 433_1012
#                                Thermostat4 – MCZ 1 fan, 2 fans and 3 fans
#                                models
#                                BlindsT8 up/down changed to close/open
#                                BlindsT13 – Screenline added
#                                Thermostat4 zero fan speed added
# 2016-11-04  Walter Kraembring: Added support for FW release 433_1008 & 1009
#                                Lighting1 - Philips SBC unit 1-16
#                                Security1 – RM174RF added
#                                Westinghouse fan 7226640
#                                Thermostat4 added (MCZ 1 & 2 fan models)
# 2016-08-13  Walter Kraembring: Added support for FW release 433_1006
#                                08-08-2016
#                                - Lighting5 - MDRemote 108 LED added
#                                - Unit code added to BlindsT3
#                                - FAN – SEAV TXS4 added
# 2016-05-08  Walter Kraembring: Added support for FW release 433_1002
#                                06-05-2016
#                                - BlindsT12 – Confexx unit code corrected
#                                - Cartelectronic TIC and Encoder added
#                                - Livolo dim/scene commands added for On/Off
#                                  module
#                                - RFY unit code All changed to channel 0
# 2016-03-12  Walter Kraembring: Added support for FW release 433_1001
#                                18-02-2016
#                                - IT (Intertek,FA500,PROmax…)
#                                - Confexx CNF24-2435 blind motors
# 2016-02-07  Walter Kraembring: Added support for FW release 433_95/195/251
#                                06-02-2016
#                                - LucciAir Fan
#                                - Inovalley S80 plant humidity sensor
#                                - ASP blind motors
#                                - Avantek
#                                - HQ_COCO_20
#                                - Viking 02813 (reported as 02811)
# 2015-11-07  Walter Kraembring: Added support for Legrand CAD
# 2015-09-20  Walter Kraembring: Added support for Home Confort TEL-010
#                                Improved support for PT2262:
#                                - Action send_ELRO_Flamingo_Phenix_Sartano_
#                                  RisingSun_Brennenstuhl renamed to
#                                  send_PT2262
#                                - decoding PT2262 (Lighting4) now includes
#                                  pulse timing value
# 2015-09-02  Walter Kraembring: Modified to support RFXtrx433E FW release
#                                433_247 and RFXtrx433 Type1/Type2
#                                FW release 433_91/191.
#                                Now supporting:
#                                - ASA blinds 
#                                - RGB 432W 
#                                - Thermostat Mertik G6R-H4S
# 2015-06-05  Walter Kraembring: Added support for setting sensor lost
#                                timeouts from external script added
# 2015-03-21  Walter Kraembring: Support added for:
#                                - SelectPlus Action chime changed 
#                                - Alecto WS4500 and compatibles 
#                                - Envivo ENV-1348 Aldi chime
#                                - DEA Systems receivers (KeeLoq Classic raw)
#                                - Sunpery & Dolat DLM-1 blinds
#                                - La Crosse TX5 Rain gauge
#                                - Thermostat Mertik G6R-H4TD
# 2015-02-11  Walter Kraembring: Added monitoring of RFXtrx connection state:
#                                - Generates an event if connection is lost.
#                                  Disabling/enabling of plugin should be
#                                  enough to recover once the device is
#                                  correctly re-connected and recognized by
#                                  the operating system
# 2015-02-01  Walter Kraembring: Support added/updated for:
#                                - ELEC3 “instant power only” packets
#                                - Byron SX sound detection/selections
# 2015-01-11  Walter Kraembring: Support added for:
#                                - TEMP7 - Proove TSS330 and TH9 – TSS320
#                                - BlindsT8 Chamberlain CS4330CN
#                                - Chime SelectPlus200689101 and 200689103
#                                - Proove outdoor sensors TEMP7 type 311346
#                                  and TH9 type 311501
#                                - Genuine device validation & copyright
#                                  message added for fw versions 81/182/235
#                                  and later
# 2014-12-27  Walter Kraembring: Support added for:
#                                - Livolo Appliance 1-10
#                                - Somfy RFY commands Enable sun+wind & 
#                                  Disable sun (RFXtrx433E only)
#                                - Smartwares radiator valves (RFXtrx433E
#                                  only)
#                                - Alecto WS1700 and compatibles
#                                - Changed from old Websocket suite to support
#                                  the new Webserver plugin with websocket
#                                  included.  
# 2014-10-01  Walter Kraembring: Now supporting:
#                                - Thermostat1 Digimax
#                                - Thermostat3 Mertik-Maxitrol G6R-H4 types
# 2014-09-19  Walter Kraembring: Modified to support RFXtrx433E FW release
#                                433_230 and RFXtrx433 Type1/Type2
#                                FW release 433_79/179.
#                                Now supporting:
#                                - THB1 – BTHGN129 device
#                                - Chime – Byron MP001 transmit
#                                - TEMP11 – WT0122 pool sensor
#                                - Lighting5 – Eurodomest (NL – Action)
#                                - TRC02_2 RGB LED controller (this version
#                                  has 3 batteries in the remote, TRC02 has
#                                  only 2)
# 2014-08-22  Walter Kraembring: Added support for date/time sensor RTGR328N
# 2014-07-30  Walter Kraembring: Modified to support RFXtrx433E FW release
#                                433_229 25-07-2014 and RFXtrx433 Type1/Type2
#                                FW release 433_78/178 25-07-2014
#                                - Lighting5 - Aoke 1 channel relay with
#                                learning code
# 2014-07-14  Walter Kraembring: Modified to support RFXtrx433E FW release
#                                433_227 25-06-2014 and RFXtrx433 Type1/Type2
#                                FW release 433_77 26-06-2014
#                                - BlindsT8 – RFY added new action to support
#                                Venetian blinds
# 2014-06-06  Walter Kraembring: Modified to support RFXtrx433E FW release
#                                433_226 29-05-2014 and RFXtrx433 Type1/Type2
#                                FW release 433_76 29-05-2014
#                                - Imagintronix soil sensor added
#                                - Kambrook RF3672 added, supported by Type 2
#                                (used in Australia)
#                                - BlindsT8 – RFY added
#                                Bugfix in calculation of wind average speed
#                                and gust
# 2014-04-24  Walter Kraembring: Modified to support FW version 74
#                                - Blinds - ID4 added
#                                - BlindsT4 - unit number set to zero
#                                - BlindsT7 - Forest unit number selection
#                                  corrected
# 2014-04-08  Walter Kraembring: Added support for
#                                - Lighting1: Energenie 5-gang
#                                - Lighting1: COCO GDR2-2000R
#                                - BlindsT6: DC106/Rohrmotor24-RMF/Yooda
#                                - BlindsT7 - Forest
# 2014-02-16  Walter Kraembring: Improved action to dim AC devices up/down in
#                                defined step size
# 2014-02-14  Walter Kraembring: Made event prefix configurable (to support 
#                                multiple RFXtrx devices) 
#                                Added action to dim AC devices up/down in
#                                defined step size
#                                Saving the dim level persistent
# 2014-01-30  Walter Kraembring: Support for websockets by the Tornado plugin 
# 2013-12-28  Walter Kraembring: Added action for resetting the state memory
#                                Modified action for resetting the sensor
#                                state memory
#                                Added action to map remote control address
# 2013-12-12  Walter Kraembring: Added support for
#                                - RGB TRC02 controllers
# 2013-11-18  Walter Kraembring: Added support for
#                                - Maverick ET-732
#                                - Alecto SA30
#                                - Oregon EW109
#                                - ELEC5 Revolt
#                                - Changed configuration view, use RFXmngr to
#                                  enable/disable selected protocols
#                                Some bug fixes for:
#                                - ATI, Medion, PC Remote
#                                - CM113
#                                - RollerTrol, Hasta, A-OK, Raex, Media Mount
# 2013-10-29  Walter Kraembring: Added actions to support
#                                - Siemens SF01 LF959RA50/LF259RB50/LF959RB50
#                                  extractor hood transmit
#                                - Livolo transmit
# 2013-10-04  Walter Kraembring: Added actions to enable/disable undecoded
#                                messages.
# 2013-09-30  Walter Kraembring: Lighting5 LWRF Colour commands added
#                                Alecto WS1200 added
#                                Byron SX Chime added
# 2013-06-11  Walter Kraembring: RAEX ID changed to 3 bytes, Unit code is 0.
#                                Added support for MDREMOTE LED dimmer,
#                                Conrad RSL2 and Energenie.
# 2013-05-09  Walter Kraembring: Modified the settings for RAEX motor, also
#                                corrections made for Media Mount commands.
#                                Added support for ELRO, Flamingo, Phenix,
#                                Sartano, RisingSun, Brennenstuhl (Lighting4).
# 2013-03-14  Walter Kraembring: Blyss group code until P added.
#                                Action to decode test messages added.
# 2013-02-16  Walter Kraembring: Action to gradually dim AC devices added.
# 2013-02-12  Walter Kraembring: Blyss group code E added.
#                                Rubicson temperature and humidity sensor
#                                added.
#                                Media Mount projection screen added
#                                (transmission only).
#                                RFXtrx type 1 and 2 detection added.
# 2013-01-16  Walter Kraembring: Management of sensors lost/back improved and
#                                information sent via websocket.
# 2013-01-12  Walter Kraembring: Further improved broken message handling,
#                                trying to repair broken messages. Now I am
#                                pleased with the solution.
#                                Support for Raex YR1326 T16 motor added.
#                                Modified settings for ByeByeStandBy (units
#                                1-6 are now possible).
# 2012-11-14  Walter Kraembring: Update to comply with FW release 433_56.
#                                - Meiantech/Atlantic/Aidebao IR beam added
#                                - decoding of Koppla removed (sending still
#                                  possible)
#                                - Current/Energy meter CM180i added
#                                - RFXsensor added
#                                - unit codes for A-OK set to '00'
#                                - possible ID's for BLINDS1 adjusted
# 2012-10-21  Walter Kraembring: Update to comply with FW release 433_55:
#                                A-OK RF01, A-OK AC114 and new ByeByeStandBy
#                                models. Some other minor improvements.
# 2012-10-04  Walter Kraembring: Added support to send keys as simulated
#                                remote (ATI, Medion and PC Remote).
# 2012-10-02  Walter Kraembring: Added support receiving from remotes ATI,
#                                Medion, PC Remote.
# 2012-09-24  Walter Kraembring: Added support for HE105 and RTS10.
# 2012-09-13  Walter Kraembring: Added support for OWL CM113.
#                                Reduced printouts to the log window, keeping
#                                it a bit cleaner. Enable debug to get more
#                                info in the log window.
#                                Fixed bugs in 0x12(Koppla), 0x20(X10 remote),
#                                0x57(UV..).
#                                Changed key handling for web sockets data.
# 2012-08-28  Walter Kraembring: Improved message handling, trying to repair
#                                broken messages.
#                                TFA 30.3133 added
# 2012-08-18  Walter Kraembring: Update to comply with FW release 433_48:
#                                Philips SBC, Blyss/Thompson, Hasta old added,
#                                BLINDS1 Set Limit command added.
# 2012-08-14  Walter Kraembring: Added actions for dimming Good Morning and
#                                Good Night lamps (works with AC devices like
#                                NEXA with support for setting dim levels).
# 2012-07-24  Walter Kraembring: Meiantech commands added
#                                Bugfixes in decoding of 0x12, 0x14, 0x18,
#                                0x19 and 0x20
# 2012-07-16  Walter Kraembring: Update to comply with FW release 433_46:
#                                Viking 02035, 02038 added, RUBiCSON added,
#                                Security1 tamper status commands changed,
#                                Meiantech added.
#                                Improved websocket startup methods.
# 2012-07-07  Walter Kraembring: Added support for the RFXMeter and RFXPower
#                                Added support for the La Crosse WS2300
#                                Reworked the message handling again, not 
#                                using the eg.SerialThread anymore.
# 2012-06-27  Walter Kraembring: Added support for websockets (requires the
#                                websocket suite plugin to be added to your
#                                configuration.)
#                                Added support for OWL CM119/160 and
#                                UV sensors UVN128, UV138, UVN800, TFA
# 2012-05-29  Walter Kraembring: Added support for RisingSun, RollerTrol and
#                                Viking 02811
#                                Bug fixed for AC (unit codes 1-16)
# 2012-05-09  Walter Kraembring: Suppress/Allow duplicated events selectable
# 2012-05-04  Walter Kraembring: X10 decoding of received bright/dim commands
#                                fixed.
# 2012-04-29  Walter Kraembring: This version supports:
#                                - Wind directions as text information
#                                 (S, N, E, W etc).
#                                - Rain total values are divided by 10
#                                 (requiresFW version 35 and later).
#                                - TEMP6 - TS15C.
#                                - UPM/ESIC wind & rain sensors.
# 2012-04-15  Walter Kraembring: This version is using the eg.SerialThread.
#                                Improved performance, simplified the code.
#                                Changed the calculation of temperature from
#                                temperature sensors.
# 2012-04-13  Walter Kraembring: Improved automatic naming of macros.
# 2012-04-11  Walter Kraembring: Added selection of supported protocols.
#                                Improved reading and decoding from COM port.
#                                Improved automatic naming of macros.
#                                Cosmetic bug fixing in some action
#                                configuration dialogs.
# 2012-04-02  Walter Kraembring: First official version.
##############################################################################
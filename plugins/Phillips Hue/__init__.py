version = "0.4.3"

# plugins/PhilipsHue/__init__.py
#
# Copyright (C) 2015-2018  Aquila <post@arneespedal.com>
#
# This file is a plugin for EventGhost.
#
# Known bugs in latest version:
# - Apply-button does not get enabled by changes in listbox i configdialog for "createGroup".
# - Changing lights (with this plugin) via scenes or with long transtiontimes will in some cases still trigger an event.
#
# Planed functions:
#   - catchEvent will be able to detect changes in settings for hue groups.
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.4.3 by Aquila 2018-03-03
#     - Fixed bug in SaveStatus where non-colored lights made an error. (Thanks to stoffix for reporting the bug.)
#     - Fixed bug in "Search for new lights"
# 0.4.2 by Aquila 2016-10-18
#     - Non-colored lights now handled correctly by eventthread.
#     - Buttonstate switches now correctly supported.
# 0.4.1.1 by Aquila 2016-10-15
#     - Test code for "ButtonState" switch for jjazdk.
# 0.4.1 by Aquila 2016-10-05
#     - Searching for new sensors on init added.
#     - Removed fetching of current position of daylight sensor in config. Due to change in Hue Bridge behaviour.
#     - In ChangeLight there is now the posibility to choose if the light is turned on or not by the command.
#     - Fixed unhandled exception that crashed the plugin if a light with no colormode was changed by another app.
#     - Fixed error where the light change event triggerd even if change was by this plugin on systems where lights where not in numerical order from Hue Bridge.
#     - Plugin now catches daylight sensor changes.
#     - Events from changes in light status now has the new changed setting as payload.
# 0.4.0.1 by Aquila 2016-04-30
#     - Eventthread now detects errors in list of lights in groups, so that it does not try to get list of lights from deletede groups.
# 0.4.0 by Aquila 2016-04-06
#     - Plugin should now get button pushed event from all types of switches. (As requested by Windhowl.)
#     - Changes in light status NOT made by this plugin will trigger event: PhilipsHue.<light #>.changed
#     - createScene no longer requiers 3. string to be "<New Scene>" to create a NEW scene. 3. string still needs to be existing scene to override. (Thanks to yokel22)
#     - Fixed bug in error output in functions "isGroupOn", "getGroupStatusAsCommand" and "getStatus" when plugin set to print everything. (Thanks to yokel22)
# 0.3.6.5 by Aquila 2016-02-26
#     - Fix crash in config dialog for the plugin.
# 0.3.6.4 by Aquila 2016-02-19
#     - Cleaned up test code that broke the plugin.
#     - Fixed bug in info output in "getGroupStatus". (Thanks to RiseUp for pointing me to this.)
# 0.3.6.3 by Aquila 2016-01-01
#     - Fixed bug in error/info output in "isOn". (Thanks to bxr for pointing me to this.)
# 0.3.6.2 by Aquila 2015-08-09
#     - Fixed bugs in "cloneLight", "cloneLight2Group" and "cloneGroup". Thanks to yokel22 for pointing me to this.
# 0.3.6.1 by Aquila 2015-08-07
#     - Fixed bug in configpanel for new setups.
# 0.3.6 by Aquila 2015-08-04
#     - Added configuration of Daylight sensor. (Built in sensor in Hue Bridge, depends on date/time and positon NOT real light. Leave position to 'none' to not use.)
#     - Added button in Configdialog to get random username from bridge. (Philips Hue have removed the posibility to choose own username.)
#     - Removed "register" function due to new method to connect to bridge.
#     - Fixed small output bug in errorhandeling
#     - Eventthread is now stoped on close also, so plugin should no longer hang Eventghost after closing. (Thanks to krad23 for pointing me to this problem.)
# 0.3.5 by Aquila 2015-04-17 (Not published)
#     - Option to print errors and results.
#     - Improved errorhandeling.
#     - Removed puls from "saveStatus". The Hue bridge does not reset puls setting when it is done pulsing, so saving status with puls setting would restart puls on recallStatus. 
#     - Added option to pulse light on max brightness in "dimUp" and "dimGroupUp" functions.
# 0.3.4 by Aquila 2015-04-16
#     - New function: "cloneLight", "cloneLight2Group" and "cloneGroup". Copy settings from one light/group to another.
#     - New functions: "satGroupUp", "hueGroupUp", "satGroupDown" and "hueGroupDown". Increases or decreases hue or saturation of a light by a choosen step. (NB! Changes from current GROUP setting, individual light
#       setting may be diffrent.)
#     - New functions: "satUp", "satDown", "hueUp" and "hueDown". Increases or decreases hue or saturation of a light by a choosen step.
# 0.3.3 by Aquila 2015-04-01
#     - New functions: "dimUp", "dimDown", "dimGroupUp" and "dimGroupDown". Dims a light or a group. (NB! DimGroup* dims from current GROUP setting, individual light setting may be diffrent.)
#     - New functions: "saveStatus" and "recallStatus". Saves and recalls status of a light. (Use scenes for groups.)
#     - Fixed multiple bugs in "modifyScene"
# 0.3.2 by Aquila 2015-03-16
#     - New functions: "getStatusasCommand" and "getGroupStatusAsCommand", returns status as a string that can be used by "customCommand" and "customCommandGroup".
#       (Save the settings of a light fx to copy to another light or restore after an alert.)
#     - Added alert and effect settings to "Change light" and "Change group" commands.
#     - Transtiontime added as setting in this commands: TurnOn, toggleLight, toogleGroup, groupOn, groupOff, TurnOff, standardWhite, standardWhiteGroup 
#       (NB! Using transtiontime to turn off light changes brightnes settings in the bridge.)
# 0.3.1 by Aquila 2015-03-13
#     - Fixed bug in register with bridge function.
# 0.3.0 by Aquila 2015-03-09
#     - Change from "requests" to "httplib"
#     - Changed eventthread pull frequency to 2 seconds (earlier 1 second) to prevent overloading the bridge.
# 0.2.3 by Aquila 2015-02-10 (Not published)
#     - Reorganized grouping of actions.
#     - New function: "modifyScene", modifys scene settings for a light.
#     - New function: "createScene", creates new or edits existing scenes.
#     - New function: "useScene", uses scene on spesific group.
#     - New function: "colorLoopGroup", sends colorloop command to group.
#     - New function: "pulseGroup", sends puls/alert command to group.
#     - New function: "standardWhiteGroup", changes all lights in group to standard (varm) white.
#     - New function: "getGroupStatus", returns status of group as a dictionary.
#     - New function: "isGroupOn", return if group is set to off (return False) or on (retirn True).
#     - New function: "customCommandGroup", send custom command to a group of lights.
#     - New function: "editGroup", edit Group (rename and change lights in group).
#     - Fixed bug in connectionerror handeling in eventthread.
#     - New function: "deleteGroup", deletes one or more groups.
#     - New function: "changeGroup", changes light from a group of lights.
# 0.2.2 by Aquila 2015-02-07
#     - New function: "getSensorStatus", returns dictionary of one sensor.
#     - Cleand up some code. (hue() returns dictionary instead of json)
#     - Fixed bug in configdialog for "ChangeLight".
#     - New function: "toggleGroup", toggles lights in group on/off.
#     - New function: "toggleLight", toggles light on/off.
#     - Fixed bug in connectionerror handeling in eventthread.
#     - Catches connection error at plugin startup.
# 0.2.1 by Aquila 2015-02-06
#     - Fixed bug with eventthread breaking the plugin when username was not registered.
#     - Actions grouped in the AddActionsDialog of EG.
#     - Group functions: groupOn, groupOff, createGroup
# 0.2.0 by Aquila 2015-02-05
#     - Throws event if button is pushed on Hue Tap (PhilipsHue.<Hue Tap>.buttonXX (XX is exchanged with button nr).
#     - Throws event if state change sensor (PhilpsHue.<sensor>.change)
#     - Throws event if lights are added or removed from bridge index.
#     - Fixed bug that made choice of light incorrect in config
#     - New function: "renameLight", changes name of a light.
#     - New function: "getNewLights", makes the Bridge search for new lights.
#     - Throws event if light gets reachable or unreachable.     
#     - Upgrading from 0.1.0 requiers you to rerun the "Register" command.
#     - Can configure username. 
#     - Hue API handled internaly in plugin, no longer needs "phue" library.
# 0.1.0 by Aquila 2015-02-01
#     - First version

eg.RegisterPlugin(
    name = "Philips Hue",
    author = "Aquila",
    version = version,
    kind = "other",
    guid = '{2D00FC82-2E09-4C3A-898A-D92FA19DCA62}',
    description = "This plugin will controll Philips Hue via the Hue Bridge.",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6770",
    createMacrosOnAdd=True,
)

import httplib
import json
import ast
from threading import Event, Thread
    

class PhilipsHue(eg.PluginBase):
    
    def __init__(self):
        self.bridge = ''
        self.username = ''
        self.devicename = ''
        self.outlvl = 'None'
        self.reachable = []
        self.sensors = {}
        self.saved = {}
       
        single = self.AddGroup(
            "Lights",
            "Action for single lights"
        )
        single.AddAction(TurnOn)
        single.AddAction(TurnOff)
        single.AddAction(dimUp)
        single.AddAction(dimDown)
        single.AddAction(toggleLight)
        single.AddAction(standardWhite)
        single.AddAction(ChangeLight)
        single.AddAction(satUp)
        single.AddAction(satDown)
        single.AddAction(hueUp)
        single.AddAction(hueDown)
        single.AddAction(cloneLight)
        single.AddAction(CustomCommand)
        single.AddAction(getSensorStatus)
        
        effects = single.AddGroup(
            "Effects",
            "Effects for single light"
        )
        effects.AddAction(Pulse_once)
        effects.AddAction(Pulse_30sec)
        effects.AddAction(Pulse_stop)
        effects.AddAction(Colorloop)
        effects.AddAction(Colorloop_stop)
        
        status = single.AddGroup(
            "Status",
            "Status from single light"
        )
        status.AddAction(saveStatus)
        status.AddAction(recallStatus)
        status.AddAction(isOn)
        status.AddAction(getStatus)
        status.AddAction(getStatusAsCommand)
        
        settings = single.AddGroup(
            "Settings",
            "Settings for single light"
        )
        settings.AddAction(getNewLights)
        settings.AddAction(renameLight)

                
        groups = self.AddGroup(
            "Group Actions",
            "Actions for groups of lights"
        )
        groups.AddAction(groupOn)
        groups.AddAction(groupOff)
        groups.AddAction(toggleGroup)
        groups.AddAction(dimGroupUp)
        groups.AddAction(dimGroupDown)
        groups.AddAction(changeGroup)
        groups.AddAction(standardWhiteGroup)
        groups.AddAction(useScene)
        groups.AddAction(satGroupUp)
        groups.AddAction(satGroupDown)
        groups.AddAction(hueGroupUp)
        groups.AddAction(hueGroupDown)
        groups.AddAction(customCommandGroup)
        groups.AddAction(pulseGroup)
        groups.AddAction(colorLoopGroup)
        groups.AddAction(cloneLight2Group)
        groups.AddAction(cloneGroup)
        
        grstatus = groups.AddGroup(
            "Group Status",
            "Status from group of lights"
        )
        grstatus.AddAction(isGroupOn)
        grstatus.AddAction(getGroupStatus)
        grstatus.AddAction(getGroupStatusAsCommand)
        
        grsettings = groups.AddGroup(
            "Group Settings",
            "Settings for groups of lights"
        )
        grsettings.AddAction(createGroup)
        grsettings.AddAction(deleteGroup)
        grsettings.AddAction(editGroup)
        grsettings.AddAction(createScene)
        grsettings.AddAction(modifyScene)
        
        
        
    def __start__(self, bridge,username, devicename='My Computer', outlvl='Errors only', auto='Off'):
        print "PhilipsHue is started, and connecting to: " + bridge + "..."
        self.bridge = bridge
        self.username = username
        self.devicename = devicename
        self.outlvl = outlvl
        self.autorestore = auto
        self.stopThreadEvent = Event()
        
        # Check if user is registered
        adress = '/api/' + self.username + '/lights'
        
        r = self.req(adress)
        
        if r==False:
            print "Connection error, wrong bridge-IP or bridge not accessible"
            r = ''
        
        if type(r) == type([]) or r == '': 
            if r != '': print "Error: Not registered with bridge."
        else:
            print "Connected!"
            #Make list of reachable lights
            list = self.hue()
            self.reachable = []
            self.all_lights = list
            self.changed = []
            self.changed_group = []
            for l in list:
                self.reachable.append(list[l]['state']['reachable'])
                #self.all_lights.append(list[l])
            
            #Get sensors at start
            self.findSensors()
            self.sensors = self.getSensors()   
            thread = Thread(
                target=self.catchEvents,
                args=(self.stopThreadEvent, )
            )
            thread.start()
       

    def __stop__(self):
        if not self.stopThreadEvent.isSet(): self.stopThreadEvent.set()
        print "PhilipsHue is stopped."
    
    def __close__(self):
        if not self.stopThreadEvent.isSet(): self.stopThreadEvent.set()
        print "PhilipsHue is closed."
    
    def catchEvents(self, stopThreadEvent):
        
        while not stopThreadEvent.isSet():
            #Load lights
            wait = 2.0
            old = self.reachable
            old_all = self.all_lights
            list = self.hue()
            if list != False:
                self.reachable = []
                self.all_lights = list
                for l in list:
                    self.reachable.append(list[l]['state']['reachable'])
                    #self.all_lights.append(list[l])
            
                #New lights?
                if len(old) < len(self.reachable): self.TriggerEvent("light.added")
                if len(old) > len(self.reachable): self.TriggerEvent("light.removed")

                #Add group changes to changed light list
                for g in self.changed_group:
                    g1 = self.hue(g,'', True)
                    if type(g1) == type([]):
                        self.printError(g1[0])
                    else:
                        for l in g1['lights']:
                            self.changed.append(int(l))

                #for x in range(len(old)):
                    #Changed reachable?
                    #if old[x] != self.reachable[x]:
                    #    if old[x] == True: self.TriggerEvent(str(x) + ".unreachable")
                    #    else: self.TriggerEvent(str(x) + ".reachable")
                for old_value in old_all:

                    #Changed light
                    x = str(old_value)
                    old_value = old_all[old_value]
                    if old_value != self.all_lights[x]:

                        #Reachable
                        if old_value['state']['reachable'] != self.all_lights[x]['state']['reachable']:
                                if old_value['state']['reachable'] == True: self.TriggerEvent(str(x) + ".unreachable")
                                else: self.TriggerEvent(str(x) + ".reachable")

                        #Changed
                        if int(x) not in self.changed:
                            if old_value['state']['on'] != self.all_lights[x]['state']['on']:
                                if self.all_lights[x]['state']['on']: self.TriggerEvent(str(x)+ ".on")
                                else: self.TriggerEvent(str(x)+ ".off")
                            else:
                                state_vars = ["bri", "hue", "sat", "alert", "effect"]
                                changes = {}
                                for txt in state_vars:
                                    try:
                                        if txt in old_value['state']:
                                            if old_value['state'][txt] != self.all_lights[x]['state'][txt]:
                                                changes[txt] = self.all_lights[x]['state'][txt]
                                    except KeyError:
                                        print("Keyerror: Probably none-colored light.")
                                if changes != {}:
                                    self.TriggerEvent(str(x)+ ".changed", changes)
            else: 
                wait = 5.0
                print "Holding back on eventthread. (lightchanges)"
            
            #reset changed list
            self.changed = []
            self.changed_group = []

            old_sensors = self.sensors
            self.sensors = self.getSensors()
            if self.sensors != False:
                if old_sensors != self.sensors:
                    for i in old_sensors:
                        if old_sensors[i]['state'] != self.sensors[i]['state']:
                            #if old_sensors[i]['type'] == 'ZGPSwitch':
                            if 'buttonevent' in self.sensors[i]['state']:
                                self.TriggerEvent(old_sensors[i]['name'] + '.button' + str(self.sensors[i]['state']['buttonevent']))
                            elif 'daylight' in self.sensors[i]['state']:
                                self.TriggerEvent(old_sensors[i]['name'] + '.daylight' + str(self.sensors[i]['state']['daylight']))
                            else:
                                # Start test code
                                if 'modelid' in self.sensors[i]:
                                    if self.sensors[i]['modelid'] == 'ButtonState':
                                        if self.sensors[i]['state']['status'] != old_sensors[i]['state']['status']:
                                            self.TriggerEvent(old_sensors[i]['name'] + '.status_' + str(self.sensors[i]['state']['status']))
                                    else: self.TriggerEvent(old_sensors[i]['name'] + '.change')
                                # End test code (remember else in next line)
                                else: self.TriggerEvent(old_sensors[i]['name'] + '.change')
            else: 
                self.sensors = old_sensors
                wait = 5.0
                print "Holding back on eventthread. (sensorchanges)"
                
            
            stopThreadEvent.wait(wait)
    
    def Configure(self, bridge="", username="EventGhost", devicename='My Computer', outlvl='Errors only', auto='Off'):
        panel = eg.ConfigPanel()
        helpString = "Configure to connect to your Philpis Hue Bridge."
        helpLabel=panel.StaticText(helpString)
        bridgeHostEdit=panel.TextCtrl(bridge)
        devicenameEdit= panel.TextCtrl(devicename)
        usernameEdit=panel.TextCtrl(username)
        longEdit=panel.TextCtrl('none')
        latEdit=panel.TextCtrl('none')
        
        lvlchoices = ['None', 'Errors only', 'All results']
            
        selectLvl = panel.Choice(lvlchoices.index(outlvl), choices=lvlchoices)
        #autoRestore = panel.Choice(autorestore.index(auto), choices=['On','Off'])
        
        usernamebu = wx.Button(panel,-1, 'Get username from bridge')
        def Username(event):
            dlg = wx.MessageDialog(panel, "Push button on bridge and then OK to fetch new username", "New username", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                self.bridge = bridgeHostEdit.GetValue()
                adress = '/api'
                device = 'EventGhostPlugin#' + devicenameEdit.GetValue()
                command = {'devicetype' : device}
                res = self.req(adress, "POST", command)
                if res != False:
                    res = res[0]
                    error = self.errorRead(res)
                    if  error != 'Success':
                        print error
                    else:
                        newname = res['success']['username']
                        usernameEdit.SetValue(newname)
                else:
                    print "Error: Could not connect to bridge!"
        usernamebu.Bind(wx.EVT_BUTTON, Username)
        
        initlong = 'none'
        initlat = 'none'
        #print self.sensors
        #for s in self.sensors:
        #    if self.sensors[s]['type'] == 'Daylight':
        #        initlong = self.sensors[s]['config']['long']
        #        initlat = self.sensors[s]['config']['lat']
        longEdit.SetValue(initlong)
        latEdit.SetValue(initlat)
                   
        panel.AddLine(helpLabel)
        panel.AddLine("Bridge IP : ",bridgeHostEdit)
        panel.AddLine("Device name : ",devicenameEdit)
        panel.AddLine("Username : ", usernameEdit, usernamebu)
        panel.AddLine("Output level: ", selectLvl)
        #panel.AddLine("Restore light status after power off (can be up to 30 sec delay): ", autoRestore)
        panel.AddLine("Postion: (xxx.xxxx(N/S/E/W) example long: 006.6572E)")
        panel.AddLine("Long:(E/W) ", longEdit, "Lat:(N/S)" , latEdit)

        
        
        while panel.Affirmed():
            newlong = longEdit.GetValue()
            newlat = latEdit.GetValue()
            if newlong != initlong or newlat != initlat:
                for s in self.sensors:
                    if self.sensors[s]['type'] == 'Daylight':
                        adr = "/api/" + self.username + "/sensors/" + s
                        command = {}
                        command['config'] = {'long' : newlong, 'lat' : newlat}
                        res = self.req(adr,'PUT',command)
                        error = self.errorRead(res[0])
                        if  error != 'Success':
                            print error
                        else:
                            print 'New postion saved to bridge!'
            panel.SetResult(bridgeHostEdit.GetValue(), usernameEdit.GetValue(), devicenameEdit.GetValue(), selectLvl.GetStringSelection(), auto)
        
        
            
    def req(self, page, methode='GET', body=''):
        data = False
        if body!='': 
            body = json.dumps(body)
        
        server = httplib.HTTPConnection(self.bridge)
        try:
            server.request(methode, page, body)
        except:
            print "Connectionerror 1"
            data = False
        else:
            try:
                response = server.getresponse()
            except:
                print "Connectionerror 2"
                data = False
            else:
                if response.status == 200:
                    try:
                        data = response.read()
                    except:
                        print "Connectionerror 4"
                        data = False
                    else:
                        data = json.loads(data)
                else:
                    print "Connectionerror 3"
                    data = False
            server.close()
        
        return data
    
    def hue(self, light='', command='', group=False):
        adress = '/api/' + self.username
        if group == True: adress += '/groups'
        else: adress += '/lights'
        if light != '': adress += '/' + str(light)
        if command == '': 
            r = self.req(adress)           
        else:
            if group == True:  adress += '/action'
            else: adress += '/state'
            r = self.req(adress, "PUT", command)

        #light changed
        if (light!='' and command!=''):
            if group==False: self.changed.append(light)
            else: self.changed_group.append(light)

        if isinstance(r, bool):
            r = []

        return r
        
    def listlights(self, group=False):
        if group == True: 
            list = self.hue(group=True)
            lights = ['00 - All lights']
        else:
            list = self.hue()
            lights = []
        
        for l in list:
            lights.append(str(l).zfill(2) + " - " + list[l]['name'])
        return sorted(lights)
    
    def listscenes(self):
        r = self.getScene()
        if isinstance(r, bool):
            return []
        scenes = []
        for s in r:
            scenes.append(r[s]['name'])
        
        return sorted(scenes)

    def sceneId(self, scene):
        r = self.getScene()
        id = False
        
        for s in r:
            if r[s]['name'] == scene:
                id = str(s)
                break
        return id
        
    def getScene(self, scene=''):
        adress = '/api/' + self.username + '/scenes'
        
        r = self.req(adress)
        if r!=False:
            if scene == '': return r
            else: return r[scene]
        else: return r

    def listSensors(self):
        list = self.getSensors()
        sensors = []
        for l in list:
            sensors.append(str(l).zfill(2) + " - " + list[l]['name'])
        return sorted(sensors)
    
    def striplight(self, light):
        r = light.split(' - ')
        return int(r[0])
        
    def choiceNr(self, choices, light):
        r = 1
        for i in choices:
            if i == light:
                r = self.striplight(i)
                break
        return r
        
    def getSensors(self, sensor=''):
        adress = '/api/' + self.username + '/sensors'
        if sensor!='': adress += '/' + str(sensor)
        r = self.req(adress)
        if isinstance(r, bool):
            return []
        return r

    def findSensors(self):
        adress = '/api/' + self.username + '/sensors'
        r = self.req(adress, 'POST')
        return r
    
    def errorLvl(self, lvl='All'):
        r = False
        if lvl == 'All':
            if self.outlvl == 'All results': r = True
        if lvl == 'Error':
            if self.outlvl != 'None': r = True
        return r
    
    def errorRead(self, error):
        if 'error' in error:
            type = error['error']['type']
            des = error['error']['description']
            r = 'Error ' + str(type) + ': ' + des
        else: r = 'Success'
        return r
        
    def printError(self, error):
        r = self.errorRead(error)
        if self.outlvl == 'All results': print r
        if self.outlvl == 'Errors only':
            if r != 'Success':
                print r
    
    def ttime(self, command, ttime):
        if ttime != '': 
            try:
                command['transitiontime'] = int(ttime)
            except ValueError:
                if self.errorLvl('Error'): print 'Error: Transtiontime is non-integer, using default transtiontime.'
        return command

class TurnOn(eg.ActionBase):
    name = "Turn on light"
    description = "Turns on a specified light."
    
    
    def __call__(self, light, ttime=''):
        light = self.plugin.striplight(light)
        command = {'on' : True}
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1, ttime=''):
        panel = eg.ConfigPanel()
        helpString = "Select light to turn on"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue())

class dimUp(eg.ActionBase):
    name = "Dim Up light"
    description = "Dims a light up."
    
    
    def __call__(self, light, ttime='', dim='20', blink=True):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light)
        try:
            dim = int(dim)
        except ValueError:
            dim = 20
            if self.plugin.errorLvl('Error'): print 'Error: Dim up is non-integer, using default dim % (20).'
        if dim < 0: 
            dim = 0
            if self.plugin.errorLvl('Error'): print 'Error: Dim is lower than 0, using 0.'
        if dim > 100: 
            dim = 100
            if self.plugin.errorLvl('Error'): print 'Error: Dim is higher than 100, using 100.'
        dim = (254/100) * dim
        bri = r1['state']['bri']
        command = {'on' : True}
        if r1['state']['on'] == False: newbri = 0
        else:
            if bri < (254-dim): newbri = bri + dim
            else: 
                newbri = 254
                if blink == True: command['alert'] = 'select'
        command['bri'] = newbri
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1, ttime='', dim='20', blink=True):
        panel = eg.ConfigPanel()
        helpString = "Select light to dim up"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        dimvalue = panel.TextCtrl(dim)
        ttimeEdit = panel.TextCtrl(ttime)
        blinkcheck = panel.CheckBox()
        blinkcheck.SetValue(blink)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Dim up in %: ", dimvalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Puls light when at maximum brightness", blinkcheck)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), dimvalue.GetValue(), blinkcheck.GetValue())

class satUp(eg.ActionBase):
    name = "Increase Sat"
    description = "Increases saturation for a light."
    
    
    def __call__(self, light, ttime='', sat='40', blink=True):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light)
        try:
            sat = int(sat)
        except ValueError:
            sat = 40
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change is non-integer, using default saturation change (40).'
        if sat < 0: 
            sat = 0
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change lower than 0, using 0.'
        if sat > 254: 
            sat = 254
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change higher than 254, using 254.'
        oldsat = r1['state']['sat']
        command = {'on' : True}
        if oldsat < (254-sat): newsat = oldsat + sat
        else: 
            newsat = 254
            if blink == True: command['alert'] = 'select'
        command['sat'] = newsat
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1, ttime='', sat='40', blink=True):
        panel = eg.ConfigPanel()
        helpString = "Select light to increase saturation"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        satvalue = panel.TextCtrl(sat)
        ttimeEdit = panel.TextCtrl(ttime)
        blinkcheck = panel.CheckBox()
        blinkcheck.SetValue(blink)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Saturation increase: ", satvalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Puls light when at maximum saturation", blinkcheck)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), satvalue.GetValue(), blinkcheck.GetValue())

class hueUp(eg.ActionBase):
    name = "Increase Hue"
    description = "Increases hue for a light."
    
    
    def __call__(self, light, ttime='', hue='1000', blink=True):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light)
        try:
            hue = int(hue)
        except ValueError:
            hue = 1000
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is non-integer, using default Hue change (1000).'
        if hue < 0: 
            hue = 0
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is lower than 0, using 0.'
        if hue > 65535:
            hue = 65535
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is higher than 65535, using 65535.'
        oldhue = r1['state']['hue']
        command = {'on' : True}
        if oldhue < (65535-hue): newhue = oldhue + hue
        else: 
            newhue = 65535
            if blink == True: command['alert'] = 'select'
        command['hue'] = newhue
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1, ttime='', hue='1000', blink=True):
        panel = eg.ConfigPanel()
        helpString = "Select light to increase hue"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        huevalue = panel.TextCtrl(hue)
        ttimeEdit = panel.TextCtrl(ttime)
        blinkcheck = panel.CheckBox()
        blinkcheck.SetValue(blink)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Hue increase: ", huevalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Puls light when at maximum hue", blinkcheck)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), huevalue.GetValue(), blinkcheck.GetValue())

class dimDown(eg.ActionBase):
    name = "Dim Down light"
    description = "Dims a light down."
    
    
    def __call__(self, light, ttime='', dim='20'):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light)
        try:
            dim = int(dim)
        except ValueError:
            dim = 20
            if self.plugin.errorLvl('Error'): print 'Error: Dim change is non-integer, using default dim change (20).'
        if dim < 0: 
            dim = 0
            if self.plugin.errorLvl('Error'): print 'Error: Dim change is lower than 0, using 0.'
        if dim > 100: 
            dim = 100
            if self.plugin.errorLvl('Error'): print 'Error: Dim change is higher than 100, using 100.'
        dim = (254/100) * dim
        bri = r1['state']['bri']
        if r1['state']['on'] == True:
            if bri == 0: command = {'on' : False}
            else: 
                command = {'on' : True}
                if (bri-dim) > 0: newbri = bri - dim
                else: newbri = 0
                command['bri'] = newbri
            command = self.plugin.ttime(command, ttime)
            r = self.plugin.hue(light, command)
            self.plugin.printError(r)
        else: 
            r = False
            if self.plugin.errorLvl('All'): print 'Info: Light is already off.'
        return r
        
    def Configure(self, light=1, ttime='', dim='20'):
        panel = eg.ConfigPanel()
        helpString = "Select light to dim down"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        dimvalue = panel.TextCtrl(dim)
        ttimeEdit = panel.TextCtrl(ttime)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Dim down in %: ", dimvalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), dimvalue.GetValue())
            
class satDown(eg.ActionBase):
    name = "Decrease Sat"
    description = "Decreases saturation for a light."
    
    
    def __call__(self, light, ttime='', sat='40', blink=True):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light)
        try:
            sat = int(sat)
        except ValueError:
            sat = 40
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change is non-integer, using default saturation change (40).'
        if sat < 0: 
            sat = 0
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change is lower than 0, using 0.'
        if sat > 254: 
            sat = 254
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change is higher than 254, using 0.'
        oldsat = r1['state']['sat']
        command = {'on' : True}
        if (oldsat-sat) > 0: newsat = oldsat - sat
        else: 
            newsat = 0
            if blink == True: command['alert'] = 'select'
        command['sat'] = newsat
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1, ttime='', sat='40', blink=True):
        panel = eg.ConfigPanel()
        helpString = "Select light to decrease saturation"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        satvalue = panel.TextCtrl(sat)
        ttimeEdit = panel.TextCtrl(ttime)
        blinkcheck = panel.CheckBox()
        blinkcheck.SetValue(blink)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Saturation decrease: ", satvalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Puls light when at minimum saturation", blinkcheck)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), satvalue.GetValue(), blinkcheck.GetValue())

class hueDown(eg.ActionBase):
    name = "Decrease Hue"
    description = "Decreases hue for a light."
    
    
    def __call__(self, light, ttime='', hue='1000', blink=True):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light)
        try:
            hue = int(hue)
        except ValueError:
            hue = 1000
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is non-integer, using default Hue change (1000).'
        if hue < 0: 
            hue = 0
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is lower than 0, using 0.'
        if hue > 65535: 
            hue = 65535
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is higher than 65535, using 65535.'
        oldhue = r1['state']['hue']
        command = {'on' : True}
        if (oldhue-hue) > 0: newhue = oldhue - hue
        else: 
            newhue = 0
            if blink == True: command['alert'] = 'select'
        command['hue'] = newhue
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1, ttime='', hue='1000', blink=True):
        panel = eg.ConfigPanel()
        helpString = "Select light to decrease hue"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        huevalue = panel.TextCtrl(hue)
        ttimeEdit = panel.TextCtrl(ttime)
        blinkcheck = panel.CheckBox()
        blinkcheck.SetValue(blink)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Hue decrease: ", huevalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Puls light when at minimum hue", blinkcheck)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), huevalue.GetValue(), blinkcheck.GetValue())

class dimGroupUp(eg.ActionBase):
    name = "Dim group up"
    description = "Dims lights in group up. (NB! Dims up from current GROUP setting, individual light setting may be diffrent.)"
    
    
    def __call__(self, light, ttime='', dim='20', blink=True):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light, group=True)
        try:
            dim = int(dim)
        except ValueError:
            dim = 20
            if self.plugin.errorLvl('Error'): print 'Error: Dim change is non-integer, using default dim change (20).'
        if dim < 0: 
            dim = 0
            if self.plugin.errorLvl('Error'): print 'Error: Dim change is lower than 0, using 0.'
        if dim > 100: 
            dim = 100
            if self.plugin.errorLvl('Error'): print 'Error: Dim change is higher than 100, using 100.'
        dim = (254/100) * dim
        bri = r1['action']['bri']
        command = {'on' : True}
        if r1['action']['on'] == False: newbri = 0
        else:
            if bri < (254-dim): newbri = bri + dim
            else: 
                newbri = 254
                if blink == True: command['alert'] = 'select'
        command['bri'] = newbri
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command, group=True)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, light='00 - All lights', ttime='', dim='20', blink=True):
        panel = eg.ConfigPanel()
        helpString = "Select group of lights to dim up."
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light, choices=lightChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        dimvalue = panel.TextCtrl(dim)
        blinkcheck = panel.CheckBox()
        blinkcheck.SetValue(blink)
        panel.AddLine(helpLabel)
        panel.AddLine("Group: ", selectLight)
        panel.AddLine("Dim up in %: ", dimvalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Puls light when at maximum brightness", blinkcheck)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), dimvalue.GetValue(), blinkcheck.GetValue())

class satGroupUp(eg.ActionBase):
    name = "Increase Group Sat"
    description = "Increases saturation for a group. (NB! Increases from current GROUP setting, individual light setting may be diffrent.)"
    
    
    def __call__(self, light, ttime='', sat='40', blink=True):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light, group=True)
        try:
            sat = int(sat)
        except ValueError:
            sat = 40
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change is non-integer, using default Saturation change (40).'
        if sat < 0: 
            sat = 0
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change is lower than 0, using 0.'
        if sat > 254: 
            sat = 254
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change is higher than 254, using 254.'
        oldsat = r1['action']['sat']
        command = {'on' : True}
        if oldsat < (254-sat): newsat = oldsat + sat
        else: 
            newsat = 254
            if blink == True: command['alert'] = 'select'
        command['sat'] = newsat
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command, group=True)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light='00 - All lights', ttime='', sat='40', blink=True):
        panel = eg.ConfigPanel()
        helpString = "Select group to increase saturation"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light, choices=lightChoices)
        satvalue = panel.TextCtrl(sat)
        ttimeEdit = panel.TextCtrl(ttime)
        blinkcheck = panel.CheckBox()
        blinkcheck.SetValue(blink)
        panel.AddLine(helpLabel)
        panel.AddLine("Group: ", selectLight)
        panel.AddLine("Saturation increase: ", satvalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Puls light when at maximum saturation", blinkcheck)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), satvalue.GetValue(), blinkcheck.GetValue())

class hueGroupUp(eg.ActionBase):
    name = "Increase Group Hue"
    description = "Increases hue for a group. (NB! Increases from current GROUP setting, individual light setting may be diffrent.)"
    
    
    def __call__(self, light, ttime='', hue='1000', blink=True):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light, group=True)
        try:
            hue = int(hue)
        except ValueError:
            hue = 1000
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is non-integer, using default hue change (1000).'
        if hue < 0: 
            hue = 0
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is lower than 0, using 0.'
        if hue > 65535:
            hue = 65535
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is higher than 65535, using 65535.'
        oldhue = r1['action']['hue']
        command = {'on' : True}
        if oldhue < (65535-hue): newhue = oldhue + hue
        else: 
            newhue = 65535
            if blink == True: command['alert'] = 'select'
        command['hue'] = newhue
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command, group=True)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light='00 - All lights', ttime='', hue='1000', blink=True):
        panel = eg.ConfigPanel()
        helpString = "Select group to increase hue"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light, choices=lightChoices)
        huevalue = panel.TextCtrl(hue)
        ttimeEdit = panel.TextCtrl(ttime)
        blinkcheck = panel.CheckBox()
        blinkcheck.SetValue(blink)
        panel.AddLine(helpLabel)
        panel.AddLine("Group: ", selectLight)
        panel.AddLine("Hue increase: ", huevalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Puls light when at maximum hue", blinkcheck)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), huevalue.GetValue(), blinkcheck.GetValue())

            
class dimGroupDown(eg.ActionBase):
    name = "Dim group down"
    description = "Dims lights in group down. (NB! Dims down from current GROUP setting, individual light setting may be diffrent.)"
    
    
    def __call__(self, light, ttime='', dim='20'):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light, group=True)
        try:
            dim = int(dim)
        except ValueError:
            dim = 20
            if self.plugin.errorLvl('Error'): print 'Error: Dim change is non-integer, using default dim change (20).'
        if dim < 0: 
            dim = 0
            if self.plugin.errorLvl('Error'): print 'Error: Dim change is lower than 0, using 0.'
        if dim > 100: 
            dim = 100
            if self.plugin.errorLvl('Error'): print 'Error: Dim change is higher than 100, using 100.'
        dim = (254/100) * dim
        bri = r1['action']['bri']
        if r1['action']['on'] == True:
            if bri == 0: command = {'on' : False}
            else: 
                command = {'on' : True}
                if (bri-dim) > 0: newbri = bri - dim
                else: newbri = 0
                command['bri'] = newbri
            command = self.plugin.ttime(command, ttime)
            r = self.plugin.hue(light, command, group=True)
            self.plugin.printError(r)
        else: 
            r = False
            if self.plugin.errorLvl('All'): print 'Info: Group is already off.'
        return r        
        
    def Configure(self, light='00 - All lights', ttime='', dim='20'):
        panel = eg.ConfigPanel()
        helpString = "Select group of lights to dim down."
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light, choices=lightChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        dimvalue = panel.TextCtrl(dim)
        panel.AddLine(helpLabel)
        panel.AddLine("Group: ", selectLight)
        panel.AddLine("Dim down in %: ", dimvalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), dimvalue.GetValue())

class satGroupDown(eg.ActionBase):
    name = "Decrease Group Sat"
    description = "Decreases saturation for a group. (NB! Decreases from current GROUP setting, individual light setting may be diffrent.)"
    
    
    def __call__(self, light, ttime='', sat='40', blink=True):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light, group=True)
        try:
            sat = int(sat)
        except ValueError:
            sat = 40
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change is non-integer, using default Saturation change (40).'
        if sat < 0: 
            sat = 0
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change is lower than 0, using 0.'
        if sat > 254:
            sat = 254
            if self.plugin.errorLvl('Error'): print 'Error: Saturation change is higher than 254, using 254.'
        oldsat = r1['action']['sat']
        command = {'on' : True}
        if (oldsat-sat) > 0: newsat = oldsat - sat
        else: 
            newsat = 0
            if blink == True: command['alert'] = 'select'
        command['sat'] = newsat
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command, group=True)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light='00 - All lights', ttime='', sat='40', blink=True):
        panel = eg.ConfigPanel()
        helpString = "Select group to decrease saturation"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light, choices=lightChoices)
        satvalue = panel.TextCtrl(sat)
        ttimeEdit = panel.TextCtrl(ttime)
        blinkcheck = panel.CheckBox()
        blinkcheck.SetValue(blink)
        panel.AddLine(helpLabel)
        panel.AddLine("Group: ", selectLight)
        panel.AddLine("Saturation decrease: ", satvalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Puls light when at minimum saturation", blinkcheck)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), satvalue.GetValue(), blinkcheck.GetValue())

class hueGroupDown(eg.ActionBase):
    name = "Decrease Group Hue"
    description = "Decreases hue for a group. (NB! Decreases from current GROUP setting, individual light setting may be diffrent.)"
    
    
    def __call__(self, light, ttime='', hue='1000', blink=True):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light, group=True)
        try:
            hue = int(hue)
        except ValueError:
            hue = 1000
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is non-integer, using default Hue change (1000).'
        if hue < 0: 
            hue = 0
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is lower than 0, using 0.'
        if hue > 65535:
            hue = 65535
            if self.plugin.errorLvl('Error'): print 'Error: Hue change is higher than 65535, using 65535.'
        oldhue = r1['action']['hue']
        command = {'on' : True}
        if (oldhue-hue) > 0: newhue = oldhue - hue
        else: 
            newhue = 0
            if blink == True: command['alert'] = 'select'
        command['hue'] = newhue
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command, group=True)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light='00 - All lights', ttime='', hue='1000', blink=True):
        panel = eg.ConfigPanel()
        helpString = "Select group to decrease hue"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light, choices=lightChoices)
        huevalue = panel.TextCtrl(hue)
        ttimeEdit = panel.TextCtrl(ttime)
        blinkcheck = panel.CheckBox()
        blinkcheck.SetValue(blink)
        panel.AddLine(helpLabel)
        panel.AddLine("Group: ", selectLight)
        panel.AddLine("Hue decrease: ", huevalue)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Puls light when at minimum hue", blinkcheck)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue(), huevalue.GetValue(), blinkcheck.GetValue())

class toggleLight(eg.ActionBase):
    name = "Toggle light on/off"
    description = "Toggles a specified light on/off."
    
    
    def __call__(self, light, ttime=''):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light)
        if r1['state']['on'] == True: command = {'on' : False}
        else: command = {'on' : True}
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1, ttime=''):
        panel = eg.ConfigPanel()
        helpString = "Select light to toggle on/off"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue())

class toggleGroup(eg.ActionBase):
    name = "Toggle group on/off"
    description = "Toggles lights in a group on/off."
    
    
    def __call__(self, light, ttime=''):
        light = self.plugin.striplight(light)
        r1 = self.plugin.hue(light, group=True)
        if r1['action']['on'] == True: command = {'on' : False}
        else: command = {'on' : True}
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command, group=True)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light='00 - All lights', ttime=''):
        panel = eg.ConfigPanel()
        helpString = "Select group of lights to toggle on/off"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light, choices=lightChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        panel.AddLine(helpLabel)
        panel.AddLine("Group: ", selectLight)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue())

class groupOn(eg.ActionBase):
    name = "Turn on lights in group"
    description = "Turns on lights in a specified group."
    
    
    def __call__(self, light, ttime=''):
        light = self.plugin.striplight(light)
        command = {'on' : True}
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command, group=True)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light='00 - All lights', ttime=''):
        panel = eg.ConfigPanel()
        helpString = "Select group of lights to turn on"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light, choices=lightChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        panel.AddLine(helpLabel)
        panel.AddLine("Group: ", selectLight)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue())
        

class TurnOff(eg.ActionBase):
    name = "Turn off light"
    description = "Turns off a specified light."

    def __call__(self, light, ttime=''):
        light = self.plugin.striplight(light)
        command = {'on' : False}
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, light=1, ttime=''):
        panel = eg.ConfigPanel()
        helpString = "Select light to turn off"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue())
            
class groupOff(eg.ActionBase):
    name = "Turn off lights in group"
    description = "Turns off lights in a specified group."
    
    
    def __call__(self, light, ttime=''):
        light = self.plugin.striplight(light)
        command = {'on' : False}
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command, group=True)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light='00 - All lights', ttime=''):
        panel = eg.ConfigPanel()
        helpString = "Select group of lights to turn off"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light, choices=lightChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        panel.AddLine(helpLabel)
        panel.AddLine("Group: ", selectLight)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue())
            
class standardWhite(eg.ActionBase):
    name = "Turn light white"
    description = "Turns light white (and on)."

    def __call__(self, light, ttime=''):
        light = self.plugin.striplight(light)
        command = {'on' : True, 'hue' : 14922, 'sat' : 144, 'bri' : 254 }
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1, ttime=''):
        panel = eg.ConfigPanel()
        helpString = "Select light to turn white"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), ttimeEdit.GetValue())


class Pulse_once(eg.ActionBase):
    name = "Pulse light"
    description = "Pulse a specified light."

    def __call__(self, light):
        light = self.plugin.striplight(light)
        command = {'alert' : 'select'}
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1):
        panel = eg.ConfigPanel()
        helpString = "Select light to pulse"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection())
            
class Pulse_30sec(eg.ActionBase):
    name = "Pulse light for 30 seconds"
    description = "Pulse a specified light for 30 seconds."

    def __call__(self, light):
        light = self.plugin.striplight(light)
        command = {'alert' : 'lselect'}
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1):
        panel = eg.ConfigPanel()
        helpString = "Select light to pulse for 30 seconds"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection())
            
class Pulse_stop(eg.ActionBase):
    name = "Stop a pulse light"
    description = "Stops a pulse for a specified light."

    def __call__(self, light):
        light = self.plugin.striplight(light)
        command = {'alert' : 'none'}
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1):
        panel = eg.ConfigPanel()
        helpString = "Select light to stop pulsing"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection())

class ChangeLight(eg.ActionBase):
    name = "Change light"
    description = "Changes settings for a specified light. (Also turns on the light if it is off.)"
    
    def __call__(self, light, brightness, saturation, color, ttime, alert=0, effect=0, on=0):
        if on == 0:
            command = {'on' : True}
        if on == 1:
            command = {'on' : False}
        if on == 2:
            command = {}
        if on == 3:
            r1 = self.plugin.hue(light)
            if r1['state']['on'] == True: command = {'on' : False}
            else: command = {'on' : True}
        if brightness != '': 
            try:
                command['bri'] = int(brightness)
            except ValueError:
                if self.plugin.errorLvl('Error'): print 'Error: Brightness setting is non-integer, skipping brightness.'
        if saturation != '':
            try:
                command['sat'] = int(saturation)
            except ValueError:
                if self.plugin.errorLvl('Error'): print 'Error: Saturation setting is non-integer, skipping saturation.'
        if color != '': 
            try:
                command['hue'] = int(color)
            except ValueError:
                if self.plugin.errorLvl('Error'): print 'Error: Hue setting is non-integer, skipping hue.'
        command = self.plugin.ttime(command, ttime)
        if alert != 0:
            if alert == 1: command['alert'] = 'none'
            if alert == 2: command['alert'] = 'select'
            if alert == 3: command['alert'] = 'lselect'
        if effect != 0:
            if effect == 1: command['effect'] = 'none'
            if effect == 2: command['effect'] = 'colorloop'
        
        light = self.plugin.striplight(light)
       
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1, brightness='', saturation='', color='', ttime='', alert=0, effect=0, on=0):
        panel = eg.ConfigPanel(self)
        helpString = "Change settings of specified light.\n"
        helpString += "NB! Using values outside the specified range will make the command fail.\n"
        helpString += "Leaving blank will make Philips Hue use current value."
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
            
        light = self.plugin.choiceNr(lightChoices, light)
        selectLight = panel.Choice(light-1, choices=lightChoices)
        
        onChoices = ['On', 'Off', '(no change)', 'Toggle']
        selectOn = panel.Choice(on, choices=onChoices)
        alertChoices = ['(no change)', 'No alert', 'One puls', '30 sec puls']
        selectAlert = panel.Choice(alert, choices=alertChoices)
        effectChoices = ['(no change)', 'No effect', 'Colorloop']
        selectEffect = panel.Choice(effect, choices=effectChoices)
        
        brightnessEdit = panel.TextCtrl(brightness)
        saturationEdit = panel.TextCtrl(saturation)
        colorEdit = panel.TextCtrl(color)
        ttimeEdit = panel.TextCtrl(ttime)
        
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("Turn light on/off: ", selectOn)
        panel.AddLine("Brightness (0-254, 0 is not off.): ", brightnessEdit)
        panel.AddLine("Saturation (0-254, 0 is white - 254 most color.): ", saturationEdit)
        panel.AddLine("Color (0-65535, both 0 and 65525 is red, 25500 is green and 46920 is blue.): ", colorEdit)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        panel.AddLine("Select alertmode: (use 'no change' if sure correct mode is allready in  use)", selectAlert)
        panel.AddLine("Select effectmode: (use 'no change' if sure correct mode is allready in  use)", selectEffect)
       
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), brightnessEdit.GetValue(), saturationEdit.GetValue(), colorEdit.GetValue(), ttimeEdit.GetValue(), selectAlert.GetCurrentSelection(), selectEffect.GetCurrentSelection(), selectOn.GetCurrentSelection())


            
class isOn(eg.ActionBase):
    name = "Checks if light is on"
    description = "Checks if a specified light is on. Returns True if on, and False if off."

    def __call__(self, light):
        light = self.plugin.striplight(light)
        r = self.plugin.hue(light)
        if self.plugin.errorLvl('All'): print 'Info: ' + str(r['state']['on'])
        return r['state']['on']
        
    def Configure(self, light=1):
        panel = eg.ConfigPanel()
        helpString = "Select light to check"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection())

class getStatus(eg.ActionBase):
    name = "Get status"
    description = "Gets the status of a specified light. Returns a dictionary."

    def __call__(self, light):
        light = self.plugin.striplight(light)
        r = self.plugin.hue(light)
        if self.plugin.errorLvl('All'): print 'Info: ' + str(r)
        return r
        
        
    def Configure(self, light=1):
        panel = eg.ConfigPanel()
        helpString = "Select light to get status for"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection())
            
class getStatusAsCommand(eg.ActionBase):
    name = "Get status as Command"
    description = "Gets the status of a specified light. Returns a commandstring."

    def __call__(self, light):
        light = self.plugin.striplight(light)
        r = self.plugin.hue(light)
        r = r['state']
        res = {}
        commands = ['on', 'hue', 'bri', 'sat', 'effect', 'alert']
        for i in commands:
            if i in r: res[i] = r[i]
        r = str(res)
        if self.plugin.errorLvl('All'): print 'Info: ' + r
        return r
        
        
    def Configure(self, light=1):
        panel = eg.ConfigPanel()
        helpString = "Select light to get status for"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection())

class saveStatus(eg.ActionBase):
    name = "Save status"
    description = "Saves status of light. This can be recalled with the recallStatus function."

    def __call__(self, light):
        light = self.plugin.striplight(light)
        r = self.plugin.hue(light)
        r = r['state']
        res = {}
        commands = ['on', 'hue', 'bri', 'sat', 'effect']
        for i in commands:
            if i in r: res[i] = r[i]
        self.plugin.saved[light] = res
        if self.plugin.errorLvl('All'): print 'Saved: ' + str(res)
        return res
        
        
    def Configure(self, light=1):
        panel = eg.ConfigPanel()
        helpString = "Select light to save status for"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection())

class recallStatus(eg.ActionBase):
    name = "Recall status"
    description = "Recalls status of light saved with saveStatus function."

    def __call__(self, light):
        light = self.plugin.striplight(light)
        if light in self.plugin.saved: 
            r = self.plugin.hue(light, self.plugin.saved[light])
            self.plugin.printError(r)
        else: 
            r = False
            if self.plugin.errorLvl('Error'): print 'Error: No saved status for this light.'
        return r
        
        
    def Configure(self, light=1):
        panel = eg.ConfigPanel()
        helpString = "Select light to recall status for"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection())

class cloneLight(eg.ActionBase):
    name = "Clone light settings"
    description = "Clones the light settings from one light to another."

    def __call__(self, light, reciver, ttime=''):
        light = self.plugin.striplight(light)
        reciver = self.plugin.striplight(reciver)
        r = self.plugin.hue(light)
        r = r['state']
        res = {}
        commands = ['on', 'hue', 'bri', 'sat', 'effect']
        for i in commands:
            if i in r:
                res[i] = r[i]
        res = self.plugin.ttime(res, ttime)
        r = self.plugin.hue(reciver, res)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, light=1, reciver=1, ttime=''):
        panel = eg.ConfigPanel()
        #helpString = "Select light to clone"
        #helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
        reciver = self.plugin.choiceNr(lightChoices, reciver)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        selectLight2 = panel.Choice(reciver-1, choices=lightChoices)
        
        ttimeEdit = panel.TextCtrl(ttime)
        
        #panel.AddLine(helpLabel)
        panel.AddLine("Source light: ", selectLight)
        panel.AddLine("Target light: ", selectLight2)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), selectLight2.GetStringSelection(), ttimeEdit.GetValue())

class cloneLight2Group(eg.ActionBase):
    name = "Clone light settings to group"
    description = "Clones the light settings from one light to a group."

    def __call__(self, light, reciver, ttime=''):
        light = self.plugin.striplight(light)
        reciver = self.plugin.striplight(reciver)
        r = self.plugin.hue(light)
        r = r['state']
        res = {}
        commands = ['on', 'hue', 'bri', 'sat', 'effect']
        for i in commands:
            if i in r:
                res[i] = r[i]
        res = self.plugin.ttime(res, ttime)
        r = self.plugin.hue(reciver, res, group=True)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, light=1, reciver='00 - All lights', ttime=''):
        panel = eg.ConfigPanel()
        #helpString = "Select light to clone"
        #helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        groupChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
        reciver = self.plugin.choiceNr(groupChoices, reciver)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        selectLight2 = panel.Choice(reciver, choices=groupChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        #panel.AddLine(helpLabel)
        panel.AddLine("Source light: ", selectLight)
        panel.AddLine("Target group: ", selectLight2)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), selectLight2.GetStringSelection(), ttimeEdit.GetValue())
            

class cloneGroup(eg.ActionBase):
    name = "Clone group settings"
    description = "Clones the group settings from one group to another. (NB! Clones from current GROUP setting, individual light setting may be diffrent.)"

    def __call__(self, light, reciver, ttime=''):
        light = self.plugin.striplight(light)
        reciver = self.plugin.striplight(reciver)
        r = self.plugin.hue(light, group=True)
        r = r['action']
        res = {}
        commands = ['on', 'hue', 'bri', 'sat', 'effect']
        for i in commands:
            if i in r:
                res[i] = r[i]
        res = self.plugin.ttime(res, ttime)
        r = self.plugin.hue(reciver, res, group=True)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, light='00 - All lights', reciver='00 - All lights', ttime=''):
        panel = eg.ConfigPanel()
        #helpString = "Select light to clone"
        #helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights(group=True)
        light = self.plugin.choiceNr(lightChoices, light)
        reciver = self.plugin.choiceNr(lightChoices, reciver)
            
        selectLight = panel.Choice(light, choices=lightChoices)
        selectLight2 = panel.Choice(reciver, choices=lightChoices)
        ttimeEdit = panel.TextCtrl(ttime)
        #panel.AddLine(helpLabel)
        panel.AddLine("Source group: ", selectLight)
        panel.AddLine("Target group: ", selectLight2)
        panel.AddLine("Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms).)", ttimeEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), selectLight2.GetStringSelection(), ttimeEdit.GetValue())
            
class getSensorStatus(eg.ActionBase):
    name = "Get sensor status"
    description = "Gets the status of a specified sensor. Returns a dictionary."
    
    def __call__(self, sensor):
        sensor = self.plugin.striplight(sensor)
        r = self.plugin.getSensors(sensor)
        if self.plugin.errorLvl('All'): print 'Info: ' + str(r)
        return r
        
    def Configure(self, sensor=''):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select sensor to get status from:"
        helpLabel=panel.StaticText(helpString)
        
        
        sensorChoices = self.plugin.listSensors()
        
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=sensorChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        r = listBoxCtrl.FindString(sensor)
        listBoxCtrl.SetSelection(r)
            
        
        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            
            panel.SetResult(sensorChoices[listBoxCtrl.GetSelection()])
    
            
class Colorloop(eg.ActionBase):
    name = "Run colorloop"
    description = "Run colorloop on a specified light."

    def __call__(self, light):
        light = self.plugin.striplight(light)
        command ={'effect' : 'colorloop'}
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1):
        panel = eg.ConfigPanel()
        helpString = "Select light to run colorloop"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection())
            
class Colorloop_stop(eg.ActionBase):
    name = "Stop colorloop"
    description = "Stop colorloop on a specified light."

    def __call__(self, light):
        light = self.plugin.striplight(light)
        command ={'effect' : 'none'}
        r = self.plugin.hue(light, command)
        self.plugin.printError(r)
        return r
        
    def Configure(self, light=1):
        panel = eg.ConfigPanel()
        helpString = "Select light to stop colorloop"
        helpLabel=panel.StaticText(helpString)
       
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection())
            
class CustomCommand(eg.ActionBase):
    name = "Custom command"
    description = "Send a custom command to a specified light."

    def __call__(self, light, command):
        light = self.plugin.striplight(light)
        try:
            command = ast.literal_eval(command)
        except SyntaxError:
            if self.plugin.errorLvl('Error'): print 'Error: Incorrect syntax in command.'
            r = False
        else:
            r = self.plugin.hue(light, command)
            self.plugin.printError(r)
        return r
        
    def Configure(self, light=1, command="{'on' : True}"):
        panel = eg.ConfigPanel()
        helpString = "Send custom command to a light"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        
        commandEdit=panel.TextCtrl(command)
        
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine(commandEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), commandEdit.GetValue())
        
class getNewLights(eg.ActionBase):
    name = "Search for new lights"
    description = "Makes the bridge search for new lights (and switches) for 1 minute. To add a Hue Tap, press and hold button 1 for 10 seconds."
    
    def __call__(self):
        adress = '/api/' + self.plugin.username + '/lights'
        r = self.plugin.req(adress, "POST")
        if self.plugin.errorLvl('All'): print 'Info: '  + str(r)    
        return r
        
class renameLight(eg.ActionBase):
    name = "Rename light"
    description = "Changesname of specified light."
    
    
    def __call__(self, light, newname):
        if newname != '':
            adress = '/api/' + self.plugin.username + '/lights/' + str(light)
            command = {'name' : newname}
            r = self.plugin.req(adress, "PUT", command)
            self.plugin.printError(r)
        else: 
            r = False
            if self.plugin.errorLvl('Error'): print 'Error: No new name given.'
        return r
        
    def Configure(self, light=1, newname=''):
        panel = eg.ConfigPanel()
        helpString = "Select light to rename"
        helpLabel=panel.StaticText(helpString)
        
        lightChoices = self.plugin.listlights()
        light = self.plugin.choiceNr(lightChoices, light)
        renameEdit=panel.TextCtrl(newname)
            
        selectLight = panel.Choice(light-1, choices=lightChoices)
        panel.AddLine(helpLabel)
        panel.AddLine("Light: ", selectLight)
        panel.AddLine("New name: ", renameEdit)
        while panel.Affirmed():
            panel.SetResult(selectLight.GetStringSelection(), renameEdit.GetValue())
            
class createGroup(eg.ActionBase):
    name = "Create group"
    description = "Creates a group of lights."
    
    
    def __call__(self, light, newname):
        r = []
        if newname != '':
            for l in light:
                r.append(str(self.plugin.striplight(l)))
            adress = '/api/' + self.plugin.username + '/groups'
            command = {'lights' : r, 'name' : newname}
            res = self.plugin.req(adress, "POST", command)
            self.plugin.printError(res)
        else: 
            res = False
            if self.plugin.errorLvl('Error'): print 'Error: No name given.'
        return res
        
    def Configure(self, light=[], newname=''):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select lights to put in group."
        helpLabel=panel.StaticText(helpString)
        helpLabel2=panel.StaticText("Name of Group to make: ")
        
        lightChoices = self.plugin.listlights()
        
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=lightChoices,
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        for i in light:
            r = listBoxCtrl.FindString(i)
            listBoxCtrl.SetSelection(r)
            
        
        nameEdit=panel.TextCtrl(newname)
        
        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        rightbox.Add(nameEdit)
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = listBoxCtrl.GetSelections()
            r = []
            for i in list:
                r.append(lightChoices[i]) 
            panel.SetResult(r,nameEdit.GetValue())

class changeGroup(eg.ActionBase):
    name = "Change group"
    description = "Changes settings for a group of lights."
    
    
    def __call__(self, group, brightness, saturation, color, ttime, alert=0, effect=0):
        command = {'on' : True}
        if brightness != '': 
            try:
                command['bri'] = int(brightness)
            except ValueError:
                if self.plugin.errorLvl('Error'): print 'Error: Brightness setting is non-integer, skipping brightness.'
        if saturation != '':
            try:
                command['sat'] = int(saturation)
            except ValueError:
                if self.plugin.errorLvl('Error'): print 'Error: Saturation setting is non-integer, skipping saturation.'
        if color != '': 
            try:
                command['hue'] = int(color)
            except ValueError:
                if self.plugin.errorLvl('Error'): print 'Error: Hue setting is non-integer, skipping hue.'
        command = self.plugin.ttime(command, ttime)
        if alert != 0:
            if alert == 1: command['alert'] = 'none'
            if alert == 2: command['alert'] = 'select'
            if alert == 3: command['alert'] = 'lselect'
        if effect != 0:
            if effect == 1: command['effect'] = 'none'
            if effect == 2: command['effect'] = 'colorloop'
        
        group = self.plugin.striplight(group)
        
        r = self.plugin.hue(group, command, group=True)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, group='', brightness='', saturation='', color='', ttime='', alert=0, effect=0):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select group to change settings for."
        helpLabel=panel.StaticText(helpString)
        helpString2 = "Change settings of a group of lights."
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        lightChoices = self.plugin.listlights(group=True)
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=lightChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        r = listBoxCtrl.FindString(group)
        listBoxCtrl.SetSelection(r)
            
        brightnessHelp = panel.StaticText("Brightness (1-254)")
        brightnessEdit = panel.TextCtrl(brightness)
        saturationHelp = panel.StaticText("Saturation (1-254)")
        saturationEdit = panel.TextCtrl(saturation)
        colorHelp = panel.StaticText("Color (0-65535)")
        colorEdit = panel.TextCtrl(color)
        ttimeHelp = panel.StaticText("Transitiontime (10 is 1 sec)")
        ttimeEdit = panel.TextCtrl(ttime)
        alertHelp = panel.StaticText("Select alertmode:")
        alertChoices = ['(no change)', 'No alert', 'One puls', '30 sec puls']
        selectAlert = panel.Choice(alert, choices=alertChoices)
        effectHelp = panel.StaticText("Select effectmode:")
        effectChoices = ['(no change)', 'No effect', 'Colorloop']
        selectEffect = panel.Choice(effect, choices=effectChoices)
        
        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        rightbox.Add(spacer)
        rightbox.Add(brightnessHelp)
        rightbox.Add(brightnessEdit)
        rightbox.Add(saturationHelp)
        rightbox.Add(saturationEdit)
        rightbox.Add(colorHelp)
        rightbox.Add(colorEdit)
        rightbox.Add(ttimeHelp)
        rightbox.Add(ttimeEdit)
        rightbox.Add(alertHelp)
        rightbox.Add(selectAlert)
        rightbox.Add(effectHelp)
        rightbox.Add(selectEffect)
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = listBoxCtrl.GetSelection()
            r = lightChoices[list]
            panel.SetResult(r, brightnessEdit.GetValue(), saturationEdit.GetValue(), colorEdit.GetValue(), ttimeEdit.GetValue(), selectAlert.GetCurrentSelection(), selectEffect.GetCurrentSelection())

class deleteGroup(eg.ActionBase):
    name = "Delete group(s)"
    description = "Delete one or more groups."
    
    
    def __call__(self, groups):
        r = []
        for g in groups:
            adress = '/api/' + self.plugin.username + '/groups/'
            adress += str(self.plugin.striplight(g))
            res = self.plugin.req(adress, "DELETE")
            r.append(res)
            self.plugin.printError(res)
        return r
        
        
    def Configure(self, group=''):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select groups to delete."
        helpLabel=panel.StaticText(helpString)
        helpString2 = " "
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        lightChoices = self.plugin.listlights(group=True)
        lightChoices.remove('00 - All lights')
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=lightChoices,
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        for i in group:
            r = listBoxCtrl.FindString(i)
            listBoxCtrl.SetSelection(r)
        
        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        rightbox.Add(spacer)
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = listBoxCtrl.GetSelections()
            r = []
            for i in list:
                r.append(lightChoices[i]) 
            panel.SetResult(r)

class editGroup(eg.ActionBase):
    name = "Edit group"
    description = "Edit attributes for a group of lights."
    
    
    def __call__(self, group, lights, newname):
        group = self.plugin.striplight(group)
        
        adress = '/api/' + self.plugin.username + '/groups/'
        adress += str(group)
        
        newlights = []
        for l in lights:
            newlights.append(self.plugin.striplight(l))
            
        command = {'name' : newname, 'lights' : newlights}
        r = self.plugin.req(adress, "PUT", command) 
        self.plugin.printError(r)       
        return r
        
        
    def Configure(self, group='', lights=[], newname=''):
        
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        centerbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select group to edit:"
        helpLabel=panel.StaticText(helpString)
        helpString2 = "Select members of group:"
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        groupChoices = self.plugin.listlights(group=True)
        groupChoices.remove('00 - All lights')
        lightChoices = self.plugin.listlights()
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'groupBoxCtrl'
        wxID_FRAME1LISTBOX2 = wx.NewIdRef()
        name2 = 'lightBoxCtrl' 
        
        self.groupBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=groupChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        )
        
        self.lightBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX2,
            choices=lightChoices,
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB,
            name=name2
        ) 
        
        for i in lights:
            res = self.lightBoxCtrl.FindString(i)
            self.lightBoxCtrl.SetSelection(res)
        
        r = self.groupBoxCtrl.FindString(group)
        self.groupBoxCtrl.SetSelection(r)
            
        panel.Bind(wx.EVT_LISTBOX, self.OnSelectGroup, self.groupBoxCtrl)
        
        newnameHelp = panel.StaticText("Edit name of group:")
        self.newnameEdit = panel.TextCtrl(newname)
        
        leftbox.Add(helpLabel)
        leftbox.Add(self.groupBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        centerbox.Add(helpLabel2)
        centerbox.Add(self.lightBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(newnameHelp)
        rightbox.Add(self.newnameEdit)
        
        grid = wx.GridSizer(1,3,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(centerbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = self.groupBoxCtrl.GetSelection()
            r = groupChoices[list]
            list2 = self.lightBoxCtrl.GetSelections()
            r2 = []
            for i in list2:
                r2.append(lightChoices[i]) 
            panel.SetResult(r, r2, self.newnameEdit.GetValue())
            
    def OnSelectGroup(self, event):
            s = self.groupBoxCtrl.GetString(self.groupBoxCtrl.GetSelection())
            s = self.plugin.striplight(s)
            r = self.plugin.hue(s, group=True)
            
            for x in range(0,self.lightBoxCtrl.GetCount()):
                self.lightBoxCtrl.Deselect(x)
            
            for i in r['lights']:
                for l in range(0,self.lightBoxCtrl.GetCount()):
                    if int(i) == self.plugin.striplight(self.lightBoxCtrl.GetString(l)):
                        self.lightBoxCtrl.SetSelection(l)
            self.newnameEdit.SetValue(r['name'])

class customCommandGroup(eg.ActionBase):
    name = "Custom command to a group"
    description = "Sends a custom command to a group of lights."
    
    
    def __call__(self, group, command):
        try:
            command = ast.literal_eval(command)
        except SyntaxError:
            if self.plugin.errorLvl('Error'): print 'Error: Incorrect syntax in command.'
            r = False
        else:
            group = self.plugin.striplight(group)
            r = self.plugin.hue(group, command, group=True)
            self.plugin.printError(r)
        return r
        
        
    def Configure(self, group='', command=''):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select group to send custom command"
        helpLabel=panel.StaticText(helpString)
        helpString2 = "Send custom command"
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        lightChoices = self.plugin.listlights(group=True)
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=lightChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        r = listBoxCtrl.FindString(group)
        listBoxCtrl.SetSelection(r)
            
        commandEdit = panel.TextCtrl(command)

        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        #rightbox.Add(spacer)
        rightbox.Add(commandEdit)
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = listBoxCtrl.GetSelection()
            r = lightChoices[list]
            panel.SetResult(r, commandEdit.GetValue())

class isGroupOn(eg.ActionBase):
    name = "Is group on"
    description = "Returns True if Group is on. (False if off.)"
    
    
    def __call__(self, group):
        group = self.plugin.striplight(group)
        r = self.plugin.hue(group, group=True)
        if self.plugin.errorLvl('All'): print 'Info: ' + str(r['action']['on'])
        return r['action']['on']
        
        
    def Configure(self, group=''):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select group to check if is on"
        helpLabel=panel.StaticText(helpString)
        helpString2 = " "
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        lightChoices = self.plugin.listlights(group=True)
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=lightChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        r = listBoxCtrl.FindString(group)
        listBoxCtrl.SetSelection(r)    

        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = listBoxCtrl.GetSelection()
            r = lightChoices[list]
            panel.SetResult(r)

class getGroupStatus(eg.ActionBase):
    name = "Get group status"
    description = "Returns group status as a dictionary."
    
    
    def __call__(self, group):
        group = self.plugin.striplight(group)
        r = self.plugin.hue(group, group=True)
        if self.plugin.errorLvl('All'): print 'Info: ' + str(r)
        return r
        
        
    def Configure(self, group=''):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select group to get status from"
        helpLabel=panel.StaticText(helpString)
        helpString2 = " "
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        lightChoices = self.plugin.listlights(group=True)
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=lightChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        r = listBoxCtrl.FindString(group)
        listBoxCtrl.SetSelection(r)    

        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = listBoxCtrl.GetSelection()
            r = lightChoices[list]
            panel.SetResult(r)

class getGroupStatusAsCommand(eg.ActionBase):
    name = "Get group status as Command"
    description = "Returns group status as a commandstring."
    
    
    def __call__(self, group):
        group = self.plugin.striplight(group)
        r = self.plugin.hue(group, group=True)
        r = r['action']
        res = {}
        commands = ['on', 'hue', 'bri', 'sat', 'effect']
        for i in commands:
            res[i] = r[i]
        r = str(res)
        if self.plugin.errorLvl('All'): print 'Info: ' + r
        return r
        
        
    def Configure(self, group=''):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select group to get status from"
        helpLabel=panel.StaticText(helpString)
        helpString2 = " "
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        lightChoices = self.plugin.listlights(group=True)
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=lightChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        r = listBoxCtrl.FindString(group)
        listBoxCtrl.SetSelection(r)    

        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = listBoxCtrl.GetSelection()
            r = lightChoices[list]
            panel.SetResult(r)

class standardWhiteGroup(eg.ActionBase):
    name = "Standard White Group"
    description = "Sets group to standard white."
    
    
    def __call__(self, group, ttime=''):
        group = self.plugin.striplight(group)
        command = {'on' : True, 'hue' : 14922, 'sat' : 144, 'bri' : 254 }
        command = self.plugin.ttime(command, ttime)
        r = self.plugin.hue(group, command, group=True)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, group='', ttime=''):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select group to set to standard white"
        helpLabel=panel.StaticText(helpString)
        helpString2 = "Transitiontime (in multipels of 100ms, 10 is 1 sec. Blank field defaults to 4 (400ms)."
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        lightChoices = self.plugin.listlights(group=True)
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=lightChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        r = listBoxCtrl.FindString(group)
        listBoxCtrl.SetSelection(r)
        
        ttimeEdit = panel.TextCtrl(ttime)  

        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        rightbox.Add(ttimeEdit)
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = listBoxCtrl.GetSelection()
            r = lightChoices[list]
            panel.SetResult(r, ttimeEdit.GetValue())

class pulseGroup(eg.ActionBase):
    name = "Pulse group"
    description = "Pulses group or cancels pulse."
    
    
    def __call__(self, group, action):
        group = self.plugin.striplight(group)
        if action == 0: command = {'alert' : 'none'}
        if action == 1: command = {'alert' : 'select'}
        if action == 2: command = {'alert' : 'lselect'}
       
        r = self.plugin.hue(group, command, group=True)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, group='', action=0):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select group to send pulse command"
        helpLabel=panel.StaticText(helpString)
        helpString2 = "Select puls command:"
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        lightChoices = self.plugin.listlights(group=True)
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=lightChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        r = listBoxCtrl.FindString(group)
        listBoxCtrl.SetSelection(r)    

        selectPuls = panel.Choice(action, choices=['Stop puls','Pulse once', 'Pulse 30sec'])

        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        rightbox.Add(selectPuls)
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = listBoxCtrl.GetSelection()
            r = lightChoices[list]
            panel.SetResult(r, selectPuls.GetValue())
            
class colorLoopGroup(eg.ActionBase):
    name = "Colorloop group"
    description = "Colorloop group or cancel loop."
    
    
    def __call__(self, group, action):
        group = self.plugin.striplight(group)
        if action == 0: command = {'effect' : 'none'}
        if action == 1: command = {'effect' : 'colorloop'}
       
        r = self.plugin.hue(group, command, group=True)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, group='', action=0):
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select group to colorloop"
        helpLabel=panel.StaticText(helpString)
        helpString2 = "Select colorloop command:"
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        lightChoices = self.plugin.listlights(group=True)
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'listBoxCtrl' 
        
        listBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=lightChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        r = listBoxCtrl.FindString(group)
        listBoxCtrl.SetSelection(r)    

        selectPuls = panel.Choice(action, choices=['Stop loop','Start colorloop'])

        leftbox.Add(helpLabel)
        leftbox.Add(listBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        rightbox.Add(selectPuls)
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = listBoxCtrl.GetSelection()
            r = lightChoices[list]
            panel.SetResult(r, selectPuls.GetValue())
            
class useScene(eg.ActionBase):
    name = "Use scene"
    description = "Use a scene on a group."
    
    
    def __call__(self, group, newscene):
        group = self.plugin.striplight(group)
        newscene = self.plugin.sceneId(newscene)
        command = {'scene' : newscene}
        r = self.plugin.hue(group, command, group=True)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, group='', scene=''):
        
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select scene to use:"
        helpLabel=panel.StaticText(helpString)
        helpString2 = "Select group to use scene on:"
        helpLabel2=panel.StaticText(helpString2)
        spacer = panel.StaticText(" ")
                
        groupChoices = self.plugin.listlights(group=True)
        sceneChoices = self.plugin.listscenes()
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'groupBoxCtrl'
        wxID_FRAME1LISTBOX2 = wx.NewIdRef()
        name2 = 'sceneBoxCtrl' 
        
        groupBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=groupChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        )
        
        sceneBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX2,
            choices=sceneChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name2
        ) 
            
        res = sceneBoxCtrl.FindString(scene)
        sceneBoxCtrl.SetSelection(res)
        
        r = groupBoxCtrl.FindString(group)
        groupBoxCtrl.SetSelection(r)
        
        
        leftbox.Add(helpLabel)
        leftbox.Add(groupBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        rightbox.Add(sceneBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        
        
        grid = wx.GridSizer(1,2,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = groupBoxCtrl.GetSelection()
            r = groupChoices[list]
            list2 = sceneBoxCtrl.GetSelection()
            r2 = sceneChoices[list2]
            panel.SetResult(r, r2)

class createScene(eg.ActionBase):
    name = "Create scene"
    description = "Create a scene with current light settings."
    
    
    def __call__(self, list, newname, scene='<New Scene>'):
        adress = '/api/' + self.plugin.username + '/scenes/'
        if scene == '<New Scene>':
            x = 1
            r = self.plugin.getScene()
            while True:
                if str(x) not in r:
                    break
                if x == 210:
                    break
                x += 1
            adress += str(x)
        else: adress += self.plugin.sceneId(scene)
        lights = []
        for l in list:
            lights.append(str(self.plugin.striplight(l)))
        
        command = {'name' : newname, 'lights' : lights}
        r = self.plugin.req(adress, "PUT", command)
        self.plugin.printError(r)
        return r
        
        
    def Configure(self, lights=[], newname='', scene=''):
        
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        centerbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select lights to use in scene:"
        helpLabel=panel.StaticText(helpString)
        helpString2 = "Name of scene:"
        helpLabel2=panel.StaticText(helpString2)
        helpString3 = "Select scene:"
        helpLabel3=panel.StaticText(helpString3)
        spacer = panel.StaticText(" ")
                
        lightChoices = self.plugin.listlights()
        sceneChoices = self.plugin.listscenes()
        sceneChoices.insert(0, '<New Scene>')
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'sceneBoxCtrl'
        wxID_FRAME1LISTBOX2 = wx.NewIdRef()
        name2 = 'lightBoxCtrl' 
        
        self.sceneBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=sceneChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        self.lightBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX2,
            choices=lightChoices,
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB,
            name=name2
        ) 
        
        r = self.sceneBoxCtrl.FindString(scene)
        self.sceneBoxCtrl.SetSelection(r)
       
        for l in lights:
            res = self.lightBoxCtrl.FindString(l)
            self.lightBoxCtrl.SetSelection(res)
        
        self.nameEdit = panel.TextCtrl(newname)
        
        panel.Bind(wx.EVT_LISTBOX, self.OnSelectScene, self.sceneBoxCtrl)
        
        leftbox.Add(helpLabel3)
        leftbox.Add(self.sceneBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        centerbox.Add(helpLabel)
        centerbox.Add(self.lightBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        rightbox.Add(self.nameEdit)
        
        
        
        grid = wx.GridSizer(1,3,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(centerbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            list = self.lightBoxCtrl.GetSelections()
            r = []
            for l in list:
                r.append(lightChoices[l])
            list2 = self.sceneBoxCtrl.GetSelection()
            r2 = sceneChoices[list2]
            panel.SetResult(r, self.nameEdit.GetValue(), r2)
            
    def OnSelectScene(self, event):
            for x in range(0,self.lightBoxCtrl.GetCount()):
                    self.lightBoxCtrl.Deselect(x)
 
            s = self.sceneBoxCtrl.GetString(self.sceneBoxCtrl.GetSelection())
            if s != '<New Scene>':
                r = self.plugin.sceneId(s)
                scene = self.plugin.getScene(str(r))
            
                for i in scene['lights']:
                    for l in range(0,self.lightBoxCtrl.GetCount()):
                        if int(i) == self.plugin.striplight(self.lightBoxCtrl.GetString(l)):
                            self.lightBoxCtrl.SetSelection(l)
                self.nameEdit.SetValue(scene['name'])
            else:
                self.nameEdit.SetValue('Enter name')

class modifyScene(eg.ActionBase):
    name = "Modify scene"
    description = "Modifys a light in a scene."
    
    
    def __call__(self, scene, light, on, brightness, saturation, color, ttime):
        adress = '/api/' + self.plugin.username + '/scenes/'
        if light != '':
            adress += self.plugin.sceneId(scene) + '/lights/' + str(self.plugin.striplight(light)) + '/state'
        
            if on == 1: command = {'on' : True}
            else: command = {'on' : False}
            if brightness != '':
                try:
                    command['bri'] = int(brightness)
                except ValueError:
                    if self.plugin.errorLvl('Error'): print 'Error: Brightness is non-integer.'
            if saturation != '':
                try:
                    command['sat'] = int(saturation)
                except ValueError:
                    if self.plugin.errorLvl('Error'): print 'Error: Saturation is non-integer.'
            if color != '':
                try:
                    command['hue'] = int(color)
                except ValueError:
                    if self.plugin.errorLvl('Error'): print 'Error: Hue is non-integer.'
            command = self.plugin.ttime(command, ttime)
        
            r = self.plugin.req(adress, "PUT", command)
            self.plugin.printError(r)
        else: 
            r = False
            if self.plugin.errorLvl('Error'): print 'Error: No light choosen.'
        return r
        
        
    def Configure(self, scene='', light='', on=1, brightness='', saturation='', color='', ttime=''):
        
        panel = eg.ConfigPanel()
        
        leftbox = wx.BoxSizer(wx.VERTICAL)
        centerbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)
        
        helpString = "Select light to modify:"
        helpLabel=panel.StaticText(helpString)
        helpString2 = "Modify settings of light:"
        helpLabel2=panel.StaticText(helpString2)
        helpString3 = "Select scene:"
        helpLabel3=panel.StaticText(helpString3)
        spacer = panel.StaticText(" ")
                
        lightChoices = []
        sceneChoices = self.plugin.listscenes()
        
        wxID_FRAME1LISTBOX1 = wx.NewIdRef()
        name1 = 'sceneBoxCtrl'
        wxID_FRAME1LISTBOX2 = wx.NewIdRef()
        name2 = 'lightBoxCtrl' 
        
        self.sceneBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX1,
            choices=sceneChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name1
        ) 
        
        self.lightBoxCtrl = wx.ListBox(panel, 
            id=wxID_FRAME1LISTBOX2,
            choices=lightChoices,
            style=wx.LB_SINGLE|wx.LB_NEEDED_SB,
            name=name2
        ) 
        
        r = self.sceneBoxCtrl.FindString(scene)
        if r > -1:
            self.sceneBoxCtrl.SetSelection(r)
        
        self.OnSelectScene(-1)
        self.lightBoxCtrl.SetSelection(self.lightBoxCtrl.FindString(light))
        
        panel.Bind(wx.EVT_LISTBOX, self.OnSelectScene, self.sceneBoxCtrl)
        
        onChooser = panel.Choice(on, choices=['Off' , 'On'])
        onChoice = wx.BoxSizer(wx.HORIZONTAL)
        onChoiceHelp = panel.StaticText("Turn light:  ")
        onChoice.Add(onChoiceHelp)
        onChoice.Add(onChooser)
        brightnessHelp = panel.StaticText("Brightness (1-254)")
        brightnessEdit = panel.TextCtrl(brightness)
        saturationHelp = panel.StaticText("Saturation (1-254)")
        saturationEdit = panel.TextCtrl(saturation)
        colorHelp = panel.StaticText("Color (0-65535)")
        colorEdit = panel.TextCtrl(color)
        ttimeHelp = panel.StaticText("Transitiontime (10 is 1 sec)")
        ttimeEdit = panel.TextCtrl(ttime)
        
        leftbox.Add(helpLabel3)
        leftbox.Add(self.sceneBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        centerbox.Add(helpLabel)
        centerbox.Add(self.lightBoxCtrl, 1, wx.EXPAND | wx.ALL, 2)
        rightbox.Add(helpLabel2)
        rightbox.Add(spacer)
        rightbox.Add(onChoice)
        rightbox.Add(brightnessHelp)
        rightbox.Add(brightnessEdit)
        rightbox.Add(saturationHelp)
        rightbox.Add(saturationEdit)
        rightbox.Add(colorHelp)
        rightbox.Add(colorEdit)
        rightbox.Add(ttimeHelp)
        rightbox.Add(ttimeEdit)
        
        
        grid = wx.GridSizer(1,3,1,10)
        
        grid.Add(leftbox, 1, wx.EXPAND, 0)
        grid.Add(centerbox, 1, wx.EXPAND, 0)
        grid.Add(rightbox, 1, wx.EXPAND, 0)
        
        panel.sizer.Add(grid, 1, wx.EXPAND, 0)
      
        while panel.Affirmed():
            i = self.lightBoxCtrl.GetSelection()
            if i >= 0: r = self.lightBoxCtrl.GetString(i)
            else: r = ''

            i2 = self.sceneBoxCtrl.GetSelection()
            r2 = sceneChoices[i2]
            
            panel.SetResult(r2, r , onChooser.GetValue(), brightnessEdit.GetValue(), saturationEdit.GetValue(), colorEdit.GetValue(), ttimeEdit.GetValue())
            
    def OnSelectScene(self, event):
        self.lightBoxCtrl.Clear()
        selection = self.sceneBoxCtrl.GetSelection()
        if selection >= 0:
            s = self.sceneBoxCtrl.GetString(selection)
            r = self.plugin.sceneId(s)
            scene = self.plugin.getScene(str(r))
            lights = self.plugin.listlights()
            for i in scene['lights']:
                for l in reversed(lights):
                    if int(i) == self.plugin.striplight(l):
                        self.lightBoxCtrl.Append(l)
                

import eg

eg.RegisterPlugin(
    name = "Mi-Light Controller",
    author = "Right.Hook@live.com",
    version = "0.1.0",
    kind = "other",
    description = "Controls Mi-Light /Limitless LED using a wifi controller ",
    canMultiLoad = True
)

#from socket import *
import socket
import time
import random
import binascii

class miLight(eg.PluginBase):

    def __init__(self):
        self.ip =""     #MiLight WiFi Controller IP Address
        self.port=8899  #Milight WiFi Controller port Number
        self.dbc = .1   # Delay between commands

        self.AddAction(Power_ON)    #Add Action POWER ON
        self.AddAction(Power_OFF)   # Add Action Power OFF
        self.AddAction(Cycle_Modes)   # Add Action Modes
        self.AddAction(Power_Toggle)   # Power toggle a light group
        self.AddAction(Increase_brightness)   # increase a light group brightness
        self.AddAction(Decrease_brightness)   # decrease a light group brightness
        self.AddAction(Fade_IN)   # increase a light group brightness
        self.AddAction(Fade_OUT)   # decrease a light group brightness
        self.AddAction(GetGroupPowerState)
        self.AddAction(SetBrightness)


                ### Setup Socket
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        if self.ip =="255.255.255.255":
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)



        self.colors = [
        "Violet",
        "Royal Blue",
        "Light Sky Blue",
        "Aqua",
        "AquaMarine",
        "Mint",
        "SeaGreen",
        "Green",
        "Lime Green",
        "Yellow",
        "Goldenrod",
        "Orange",
        "Red",
        "Pink",
        "Fuchsia",
        "Orchid",
        "Lavender",
        "WHITE",
        "RANDOM COLOR",
        "Effect ( Rainbow )",
        "Effect ( White Blink )",
        "Effect ( Color Fade )",
        "Effect ( Color Change )",
        "Effect ( Color Blink )",
        "Effect ( RED Blink  )",
        "Effect ( Green Blink )",
        "Effect ( Blue Blink )",
        "Effect ( DISCO )",
        "NIGHT SAVER MODE",
        "Power OFF"

        ]
                        ## Color codes

        self.colorCodes = [
        "\x40\x00\x55",
        "\x40\x10\x55",
        "\x40\x20\x55",
        "\x40\x30\x55",
        "\x40\x40\x55",
        "\x40\x45\x55",
        "\x40\x50\x55",
        "\x40\x60\x55",
        "\x40\x70\x55",
        "\x40\x80\x55",
        "\x40\x90\x55",
        "\x40\xA0\x55",
        "\x40\xB0\x55",
        "\x40\xC0\x55",
        "\x40\xD0\x55",
        "\x40\xE0\x55",
        "\x40\xF0\x55",
        ]


        ###########GROUPS ON CODES ##
        self.groupsONcode = [
        "\x45\00\x55",
        "\x47\00\x55",
        "\x49\00\x55",
        "\x4B\00\x55"
        ]

        ########### GROUPS White CODES ##
        self.groupsWhiteCode = [
        "\xC5\00\x55",
        "\xC7\00\x55",
        "\xC9\00\x55",
        "\xCB\00\x55"
        ]

         ########### GROUPS OFF CODES ##
        self.groupsOFFCode = [
        "\x46\00\x55",
        "\x48\00\x55",
        "\x4A\00\x55",
        "\x4C\00\x55"
        ]


        ########### GROUPS Night Saver  CODES ##
        self.groupSaverCode = [
        "\xC6\00\x55",
        "\xC8\00\x55",
        "\xCA\00\x55",
        "\xCC\00\x55"
        ]


        #### DISCO MODE CODE
        self.DiscoModeCode ="\x4D\x00\x55"

        # Store group ON/OFF State and brightness
        self.groupsCurrentState = [False , False , False ,False]
        self.groupsCurrentBrightness = [0,0,0,0]

        
    def __start__(self, ip="" , port = 8899 ,dbc=.2):
        print "mi Light plugin started"
        self.ip = ip
        self.port = port
        self.dbc = dbc
        print port
        print ip
        print (dbc)
        print (self.dbc)

                ### Setup Socket
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        if self.ip =="255.255.255.255":
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


    def Configure(self, ip="255.255.255.255",port =8899 ,dbc=.1):

        panel = eg.ConfigPanel(self)
        ipCtrl = panel.TextCtrl(ip)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        dbcCtrl =  panel.SpinIntCtrl(int(dbc * 1000) , min=1, max= 1000)


        panel.AddLine(u'Enter the IP Address of the WiFi Bridge or 255.255.255.255 for UPD Broadcast (All Controllers)')
        panel.AddLine(u'WIFI Controller IP Address:', ipCtrl)
        panel.AddLine(u'WIFI Controller Port Number:', portCtrl)
        panel.AddLine(u'Delay between commands in milliseconds.', dbcCtrl)
        panel.AddLine("Recommended (100) - range (1-1000)",None)


        while panel.Affirmed():
            panel.SetResult(ipCtrl.GetValue() , portCtrl.GetValue(),dbcCtrl.GetValue() * .001)




    def GetBinaryBrightness (self,brightness = 1):
        ## miLight brightness Range 2 to 27
        # Convert from percentage to 2-27 range
        if brightness <8: brightness =8
        if brightness >100 : brightness = 100
        brightness = int(brightness * .27)

        # brightness (int to hex)
        b = str(format(78, '02x'))
        b += str(format(brightness, '02x'))
        b += str(format(85, '02x'))

        # brightness (hex to binary)
        binary_Brightness = binascii.unhexlify(b)

        return  binary_Brightness


    def GetBinaryBrightnessOLD (self,brightness = 1):
        ## miLight brightness Range 2 to 27
        if brightness <2: brightness =2
        if brightness >27 : brightness = 27

        # brightness (int to hex)
        b = str(format(78, '02x'))
        b += str(format(brightness, '02x'))
        b += str(format(85, '02x'))

        # brightness (hex to binary)
        binary_Brightness = binascii.unhexlify(b)

        return  binary_Brightness

    def SetGroupState (self,group =1 ,power_state = False , brightness  =1):
        self.groupsCurrentState [group -1] = power_state
        self.groupsCurrentBrightness [group-1] = brightness


class Power_ON(eg.ActionBase):
    name = "Power ON"
    description = "Power ON Lights Group"

    def __call__(self, group =1 , color =0 , brightness = 100):
        
        ## VARS ##
        colorCodes = self.plugin.colorCodes
        groupsONcode = self.plugin.groupsONcode
        groupsWhiteCode = self.plugin.groupsWhiteCode
        groupsOFFCode = self.plugin.groupsOFFCode
        groupSaverCode = self.plugin.groupSaverCode
        DiscoModeCode = self.plugin.DiscoModeCode


        ip = self.plugin.ip
        port =self.plugin.port
        print "Mi Light Controller IP Address : ", ip
        print "Mi Light Controller Port Number" ,port
        print "Group: = " , group
        print "Color ID = " , color
        print "brightness  = " , brightness

        # get binary brightness code from int (1-100)
        binary_Brightness = self.plugin.GetBinaryBrightness(brightness)

                    #### Send Commads to Wifi Controller #####
                    ###### Set COLORS FIRST ######

        ### Sending RGBW Command
        if color in range(0,17):

            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(groupsONcode [group-1], (ip , port))
            self.plugin.sock.sendto(groupsONcode [group-1], (ip , port))
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(colorCodes [color], (ip , port)) # SET The color
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(binary_Brightness, (ip , port)) # Send brightness command for the selected group
            time.sleep(self.plugin.dbc)
            self.plugin.SetGroupState (group,True,brightness)


        ##########      SET EFFECT          ######
        if color in range(19,28):
            effectNumber = color - 18
            print "Effect Code = " , effectNumber
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(groupsONcode [group-1], (ip, port)) # Group ON  Code
            self.plugin.sock.sendto(groupsONcode [group-1], (ip, port)) # Group ON  Code
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(groupsWhiteCode [group-1], (ip, port))  # Group White Code (it resets cycle counter)
            time.sleep(self.plugin.dbc)

            for x in range(0, effectNumber): # Cycle to the desired effect
                self.plugin.sock.sendto(DiscoModeCode, (ip, port))

            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(binary_Brightness, (ip , port)) # Send brightness command
            time.sleep(self.plugin.dbc)


        ############    SET WHITE COLOR FOR GROUPS         ######
        if color == 17 :
            print "Group " + str(group)  +" ON"
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(groupsONcode [group-1], (ip , port)) # Group ON
            self.plugin.sock.sendto(groupsONcode [group-1], (ip , port)) # Group ON
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(groupsWhiteCode[group-1], (ip , port)) # Group White command .
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(binary_Brightness, (ip , port)) # Send brightnees command
            time.sleep(self.plugin.dbc)


        ############    SET RANDOM COLOR         ######
        if color == 18 :
            print "group " + str(group) + " Random Color"
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(groupsONcode [group-1], (ip , port)) # Turn ON the selected group
            self.plugin.sock.sendto(groupsONcode [group-1], (ip , port)) # Turn ON the selected group
            time.sleep(self.plugin.dbc)
            rndColor = random.choice (colorCodes[0:16]) # Select Random color
            self.plugin.sock.sendto(rndColor, (ip , port)) # Send color
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(binary_Brightness, (ip , port)) # Send brightness command
            time.sleep(self.plugin.dbc)


        ############    SET Night Saver Mode         ######
        if color ==28:
            print "Saver Mode Group : " , group
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(groupsOFFCode [group-1], (ip , port)) # Sends OFF Command
            self.plugin.sock.sendto(groupsOFFCode [group-1], (ip , port)) # Sends OFF Command
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(groupSaverCode [group-1], (ip , port)) # Sends Night Saver Mode Command
            time.sleep(self.plugin.dbc)

        ############    Power OFF         ######
        if color ==29:
            print "Power OFF Group : " , group
            time.sleep(self.plugin.dbc)
            self.plugin.sock.sendto(groupsOFFCode [group-1], (ip , port)) # Sends OFF Command
            self.plugin.sock.sendto(groupsOFFCode [group-1], (ip , port)) # Sends OFF Command
            time.sleep(self.plugin.dbc)


        ## Set Groups State
        ## 'Yes' if fruit == 'Apple' else 'No'
        ## if color = 29 (Power OFF COMMAND) set False . else set to True

        self.plugin.SetGroupState (group,False if color == 29 else True ,brightness)



        
    def Configure(self, group =1 , color =0 , brightness = 100):
        

        panel = eg.ConfigPanel(self)
        groupCtrl = panel.Choice(group -1 , ["1","2","3","4"])
        brightnessCtrl = panel.SpinIntCtrl(brightness, min=1, max=100)
        colorCtrl = panel.Choice(color, self.plugin.colors)

        panel.AddLine(u'Select a group :', groupCtrl)
        panel.AddLine(u'Brightness 1 - 100% :', brightnessCtrl)
        panel.AddLine(u'Select a Color or Effect :', colorCtrl)

        while panel.Affirmed():
            panel.SetResult(
            groupCtrl.GetValue() +1 ,
            colorCtrl.GetValue(),
            brightnessCtrl.GetValue()
            )
            
            
        
class Power_OFF(eg.ActionBase):
    name = "Power OFF"
    description = "Power OFF Lights Group"
    def __call__(self ,group =1):
        
        groupsOFFcodes = self.plugin.groupsOFFCode

        ## sending power OFF Command to the selected group
        ip = self.plugin.ip
        port = self.plugin.port

        ## Send Power OFF Command to the selected group
        self.plugin.sock.sendto(groupsOFFcodes [group-1], (ip , port))
        self.plugin.sock.sendto(groupsOFFcodes [group-1], (ip , port))
        time.sleep(self.plugin.dbc)
        self.plugin.groupsCurrentState [group-1] = False
        
            
            
    def Configure(self, group =1 , color =0 , brightness = 2):
        
        panel = eg.ConfigPanel(self)
        groupCtrl = panel.Choice(group -1 , ["1","2","3","4"])
        panel.AddLine(u'Select group to turn off :', groupCtrl)

        while panel.Affirmed():
            panel.SetResult(groupCtrl.GetValue()+1)





class Cycle_Modes(eg.ActionBase):
    name = "Cycle Modes"
    description = "Cycle through 4 Presets each time this action runs"



    def __init__(self):
        self.cycleCounter = [0,1,2,3]


    def __call__(self , enabledGroups = [False,False,False,False] ,presets = [[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100]] ):


        # Get cycle position
        pos = self.cycleCounter[0]
        group_1 = presets[0:4]
        group_2 = presets[4:8]
        group_3 = presets[8:12]
        group_4 = presets[12:16]

        
        # Send command for enabled Groups
        if enabledGroups[0]:
            self.plugin.info.actions["Power_ON"]()(1, group_1[pos][0] , group_1[pos][1])

        if enabledGroups[1]:
            self.plugin.info.actions["Power_ON"]()(2, group_2[pos][0] , group_2[pos][1])

        if enabledGroups[2]:
            self.plugin.info.actions["Power_ON"]()(3, group_3[pos][0] , group_3[pos][1])

        if enabledGroups[3]:
            self.plugin.info.actions["Power_ON"]()(4, group_4[pos][0] , group_4[pos][1])



        # Cycle Counter
        self.cycleCounter.append(self.cycleCounter.pop(0))



    def Configure (self , enabledGroups = [False,False,False,False]  , presets = [[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100],[0,100]]   ):
   
        panel = eg.ConfigPanel(self)
        panel.AddLine(u'Cycle through 4 Presets each time this action runs.')


        ###Create  16 Brightness and color control ###

        colorControl = []
        BrightnessControl = []
        groupsCheckBox = []
        c =0 # color and brightness controls counter
        cc =1 # presets Text counter
        for x in range(0,4):

            groupsCheckBox.append(panel.CheckBox(enabledGroups[x],"Enable"))
            panel.AddLine("Group %s" % (x+1) ,groupsCheckBox[x])
            panel.AddLine("Preset #","Color/Effect","Brightness 1-100%")

            for y in range(c, (c+4)):
                colorControl.append(panel.Choice(presets[y][0], self.plugin.colors))
                BrightnessControl.append(panel.SpinIntCtrl(presets[y][1], min=1, max=100 ))
                panel.AddLine("Preset [ %s ]: " %cc, colorControl[y],BrightnessControl [y])
                cc += 1

            panel.AddLine ("________________________________________________________")
            c += 4
            cc =1


                ######## EXTRA UI ########
        counterLable  = panel.StaticText("")
        counterLable.SetLabel(str(self.cycleCounter[0]+1))
        panel.AddLine("")
        panel.AddLine("Cycle counter position :",counterLable)


        while panel.Affirmed():
            for i in range(0,4):
                enabledGroups[i] = groupsCheckBox[i].GetValue()

            for i in range(0,16):
                presets[i][0] = colorControl[i].GetValue()
                presets[i][1] = BrightnessControl[i].GetValue()



            panel.SetResult(enabledGroups,presets)
            counterLable.SetLabel(str(self.cycleCounter[0]+1))



class Power_Toggle(eg.ActionBase):
    name = "Power Toggle"
    description = "Power toggle a light group "
    def __call__(self ,group = 1):

        # Toggle Power State
        self.plugin.groupsCurrentState [group -1] = not self.plugin.groupsCurrentState [group -1]
        state = self.plugin.groupsCurrentState [group -1]

        ## Codes
                ###########GROUPS ON CODES ##
        groupsONcode = self.plugin.groupsONcode
        groupsOFFCode = self.plugin.groupsOFFCode


        if state == True:
            self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
            self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        else:
            self.plugin.sock.sendto(groupsOFFCode [group-1], (self.plugin.ip , self.plugin.port))
            self.plugin.sock.sendto(groupsOFFCode [group-1], (self.plugin.ip , self.plugin.port))


        time.sleep(self.plugin.dbc)


    def Configure(self, group =1):

        panel = eg.ConfigPanel(self)
        groupCtrl = panel.Choice(group -1 , ["1","2","3","4"])
        panel.AddLine(u'Select group to toggle :', groupCtrl)

        while panel.Affirmed():
            panel.SetResult(groupCtrl.GetValue()+1)


class Increase_brightness (eg.ActionBase):
    name = "Increase Brightness"
    description = "Increase a light group brightness "
    def __call__(self ,group = 1 , steps = 10):

        ## Codes
                ###########GROUPS ON CODES ##
        groupsONcode = self.plugin.groupsONcode

        ###  Get group Current brightness
        brightness = self.plugin.groupsCurrentBrightness[group -1] + steps
        ## Set Limits
        if brightness <1 : brightness = 1
        if brightness >100 : brightness =100
        # Set Current Group Brightness
        self.plugin.groupsCurrentBrightness[group -1] = brightness
        ## Convert it Binary
        binaryBrightness = self.plugin.GetBinaryBrightness(brightness)

        ## Send Commands
        self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        time.sleep(self.plugin.dbc)
        self.plugin.sock.sendto(binaryBrightness, (self.plugin.ip , self.plugin.port))
        time.sleep(self.plugin.dbc)

    def Configure(self, group =1 , steps =10):

        panel = eg.ConfigPanel(self)
        groupCtrl = panel.Choice(group -1 , ["1","2","3","4"])
        stepsCtrl = panel.SpinIntCtrl(steps, min=10, max=99)

        panel.AddLine(u'Group : :', groupCtrl)
        panel.AddLine(u'Increase steps (10-99) :', stepsCtrl)

        while panel.Affirmed():
            panel.SetResult(groupCtrl.GetValue()+1 , stepsCtrl.GetValue())


class Decrease_brightness (eg.ActionBase):
    name = "Decrease Brightness"
    description = "Decrease a light group brightness "
    def __call__(self ,group = 1 , steps = 10):

        ## Codes
                ###########GROUPS ON CODES ##
        groupsONcode = self.plugin.groupsONcode

        ###  Get group Current brightness
        brightness = self.plugin.groupsCurrentBrightness[group -1] - steps
        ## Set Limits
        if brightness <1 : brightness = 1
        if brightness >100 : brightness =100
        # Set Current Group Brightness
        self.plugin.groupsCurrentBrightness[group -1] = brightness
        ## Convert it Binary
        binaryBrightness = self.plugin.GetBinaryBrightness(brightness)

        ## Send Commands
        self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        time.sleep(self.plugin.dbc)
        self.plugin.sock.sendto(binaryBrightness, (self.plugin.ip , self.plugin.port))
        time.sleep(self.plugin.dbc)

    def Configure(self, group =1 , steps =10):

        panel = eg.ConfigPanel(self)
        groupCtrl = panel.Choice(group -1 , ["1","2","3","4"])
        stepsCtrl = panel.SpinIntCtrl(steps, min=10, max=99)

        panel.AddLine(u'Group : :', groupCtrl)
        panel.AddLine(u'Decrease steps (10-99) :', stepsCtrl)

        while panel.Affirmed():
            panel.SetResult(groupCtrl.GetValue()+1 , stepsCtrl.GetValue())


class Fade_IN (eg.ActionBase):
    name = "Fade-in"
    description = "Fade-in a light group"
    def __call__(self ,group = 1 ,max = 27 , speed = 10):

        ## Codes
                ###########GROUPS ON CODES ##
        groupsONcode = self.plugin.groupsONcode
        ## Fade Speed (delay in ms) ##
        Fade_Speed = [.5,.1,.05,.01]
        ## Turn group ON and set brightness to 1
        self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        time.sleep(self.plugin.dbc)
        self.plugin.sock.sendto(self.plugin.GetBinaryBrightnessOLD(2), (self.plugin.ip , self.plugin.port))

        ## NOW FADE IN ##
        print "Fade Started"

        for brightness in range(2,max + 1):
            self.plugin.sock.sendto(self.plugin.GetBinaryBrightnessOLD(brightness), (self.plugin.ip , self.plugin.port))
            time.sleep(Fade_Speed[speed])
            # For Logging
            #print brightness

        print "fade Ended"
        time.sleep(self.plugin.dbc)

                # Set Current Group state and Brightness
        self.plugin.SetGroupState(group,True,int((100.00 / 27.00) * (max)))

    def Configure(self, group =1 ,max = 27, speed =2):

        panel = eg.ConfigPanel(self)
        groupCtrl = panel.Choice(group -1 , ["1","2","3","4"])
        maxCtrl = panel.SpinIntCtrl(max, min=2, max=27)
        speedCtrl = panel.Choice(speed  , ["Extremely slow","Slow","Medium","Fast"])

        panel.AddLine(u'Group : :', groupCtrl)
        panel.AddLine(u'Fade-in up to (2-27) brightness :', maxCtrl)
        panel.AddLine(u'Speed (1-5) :', speedCtrl)

        while panel.Affirmed():
            panel.SetResult(groupCtrl.GetValue()+1 , maxCtrl.GetValue(),speedCtrl.GetValue())


class Fade_OUT (eg.ActionBase):
    name = "Fade-out"
    description = "Fade-out a light group"
    def __call__(self ,group = 1 ,min = 2 , speed = 2):

        ## Codes
                ###########GROUPS ON CODES ##
        groupsONcode = self.plugin.groupsONcode
        ## Fade Speed (delay in ms) ##
        Fade_Speed = [.5,.1,.05,.01]

        ## Turn group ON and set brightness to 27
        self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        time.sleep(self.plugin.dbc)
        self.plugin.sock.sendto(self.plugin.GetBinaryBrightnessOLD(2), (self.plugin.ip , self.plugin.port))

        ## NOW FADE OUT ##
        print "Fade Started"

        for brightness in range(27,min - 1,-1):
            self.plugin.sock.sendto(self.plugin.GetBinaryBrightnessOLD(brightness), (self.plugin.ip , self.plugin.port))
            time.sleep(Fade_Speed[speed])
            # For Logging
            #print brightness

        print "fade Ended"
        time.sleep(self.plugin.dbc)

                # Set Current Group state and Brightness
        self.plugin.SetGroupState(group,True,int((100.00 / 27.00) * (min)))


    def Configure(self, group =1 ,min = 2, speed =2):

        panel = eg.ConfigPanel(self)
        groupCtrl = panel.Choice(group -1 , ["1","2","3","4"])
        minCtrl = panel.SpinIntCtrl(min, min=2, max=27)
        speedCtrl = panel.Choice(speed , ["Extremely slow","Slow","Medium","Fast"])

        panel.AddLine(u'Group : :', groupCtrl)
        panel.AddLine(u'Fade-out down to (2-27) brightness :', minCtrl)
        panel.AddLine(u'Speed (1-5) :', speedCtrl)

        while panel.Affirmed():
            panel.SetResult(groupCtrl.GetValue()+1 , minCtrl.GetValue(),speedCtrl.GetValue())



class GetGroupPowerState (eg.ActionBase):
    name = "Get group power state"
    description = "Get a light group power state (returns True if ON and False if OFF"
    def __call__(self ,group = 1):
        return self.plugin.groupsCurrentState[group -1]

    def Configure(self, group =1):

        panel = eg.ConfigPanel(self)
        groupCtrl = panel.Choice(group -1 , ["1","2","3","4"])
        panel.AddLine(u'Group : :', groupCtrl)

        while panel.Affirmed():
            panel.SetResult(groupCtrl.GetValue()+1 )



class SetBrightness (eg.ActionBase):
    name = "Set Brightness"
    description = "Set a light group brightness"
    def __call__(self ,group = 1 ,brightness = 100):

        ## Codes
                ###########GROUPS ON CODES ##
        groupsONcode = self.plugin.groupsONcode

        ## Turn group ON and set brightness to 1
        self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        self.plugin.sock.sendto(groupsONcode [group-1], (self.plugin.ip , self.plugin.port))
        time.sleep(self.plugin.dbc)
        self.plugin.sock.sendto(self.plugin.GetBinaryBrightness(brightness), (self.plugin.ip , self.plugin.port))
        time.sleep(self.plugin.dbc)

                # Set Current Group state and Brightness
        self.plugin.SetGroupState(group,True,brightness)


    def Configure(self, group =1 ,brightness = 100):

        panel = eg.ConfigPanel(self)
        groupCtrl = panel.Choice(group -1 , ["1","2","3","4"])
        BrightnessCtrl = panel.SpinIntCtrl(brightness, min=1, max=100)

        panel.AddLine(u'Group : :', groupCtrl)
        panel.AddLine(u'brightness (1-100) :', BrightnessCtrl)

        while panel.Affirmed():
            panel.SetResult(groupCtrl.GetValue()+1 , BrightnessCtrl.GetValue())
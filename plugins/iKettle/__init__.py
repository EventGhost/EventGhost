import eg
import socket
from threading import Event, Thread

eg.RegisterPlugin(
    name = "iKettle",
    guid='{F45522B9-D98A-4556-8AE1-C70C9842A9BD}',
    author = "K-RAD",
    version = "0.0.3",
    kind = "other",
    description = "This is an EventGhost plugin for the Smarter WiFi Kettle (iKettle)."
)

class iKettle(eg.PluginBase):

    def __init__(self):
        self.kettleconnected = 0
        
#         self.AddAction(Connect)
        self.AddAction(GetStatus)
        group1 = self.AddGroup(
            "Buttons",
            "iKettle Buttons"
        )
        group1.AddAction(TurnOn)
        group1.AddAction(TurnOff)
        group1.AddAction(Boil100)
        group1.AddAction(Boil95)
        group1.AddAction(Boil80)
        group1.AddAction(Boil65)
        group1.AddAction(Warm)
        group1.AddAction(SetWarm20)
        group1.AddAction(SetWarm10)
        group1.AddAction(SetWarm5)
        
    def Configure(self, bridge=""):
        panel = eg.ConfigPanel()
        helpString = "Configure to connect to your iKettle."
        helpLabel=panel.StaticText(helpString)
        
        bridgeHostEdit=panel.TextCtrl(bridge)
        
        panel.AddLine(helpLabel)
        panel.AddLine("iKettle IP address : ",bridgeHostEdit)
       
        while panel.Affirmed():
            panel.SetResult(bridgeHostEdit.GetValue())
            
    def __start__(self, bridge):
        print "iKettle:: Plugin started.\niKettle:: Connecting to: " + bridge
        self.bridge = bridge
        
        self.kettleconnect()
        
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.catchEvents,
            args=(self.stopThreadEvent, )
        )
        thread.start()
            
    def kettleconnect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.bridge,2000))
            self.sock.send("HELLOKETTLE\n")
        except:
            print "iKettle:: Failed to connect to iKettle. Check the IP address."
            
    def kettlesend(self, data):
        self.sock.send(data+"\n")
        
            
    def catchEvents(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            
            try:
                line = self.sock.recv(4096)
            except socket.error:
                continue
            
            if not len(line):  # "Connection closed."
                pass
#                 self.kettleconnect()
            else:
                for myline in line.splitlines():
#                     print "got a line: " + myline
                    if (myline.startswith("HELLOAPP")):
                        self.kettleconnected = 1
                        print "iKettle:: Connected.\niKettle:: Getting status.."
                        self.sock.send("get sys status\n")
                        
                    if (myline.startswith("sys status key=")):
                        if (len(myline)<16):
                            key = 0
                        else:
                            key = ord(myline[15]) & 0x3f
                        self.status = {'On': key==0x1, 'Boil100': key==0x20, 'Boil95': key==0x10, 'Boil80': key==0x8, 'Boil65': key==0x4, 'Warm': key==0x2}
                        print "iKettle:: status = {0}".format(self.status)
                        
                    if (myline == "sys status 0x100"):
                        self.TriggerEvent("Boil100")
                    elif (myline == "sys status 0x95"):
                        self.TriggerEvent("Boil95")
                    elif (myline == "sys status 0x80"):
                        self.TriggerEvent("Boil80")
                    elif (myline == "sys status 0x65"):
                        self.TriggerEvent("Boil65")
                    elif (myline == "sys status 0x11"):
                        self.TriggerEvent("Warm")
                    elif (myline == "sys status 0x10"):
                        self.TriggerEvent("WarmEnded")
                    elif (myline == "sys status 0x5"):
                        self.TriggerEvent("On")
                    elif (myline == "sys status 0x0"):
                        self.TriggerEvent("Off")
                    elif (myline == "sys status 0x3"):
                        self.TriggerEvent("Done")
                    elif (myline == "sys status 0x2"):
                        self.TriggerEvent("NoWater")
                    elif (myline == "sys status 0x1"):
                        self.TriggerEvent("Removed")
            stopThreadEvent.wait(5.0)

    def __stop__(self):
        print "iKettle:: Closing"

        if not self.stopThreadEvent.isSet(): self.stopThreadEvent.set()
        print "iKettle:: Thread stopped"
        
        try:
            self.sock.close()
        except:
            pass
        print "iKettle:: iKettle is stopped."
        
    def __close__(self):
        if not self.stopThreadEvent.isSet(): self.stopThreadEvent.set()
        self.sock.close()

class Connect(eg.ActionBase):
    name = "Connect"
    description = "Connect to iKettle. Is it necesarry?"
    
    def __call__(self):
        print "iKettle:: Connecting...."
        self.plugin.kettleconnect()
        
class GetStatus(eg.ActionBase):
    name = "Get Status"
    description = "Returns a dictionary: status "
    
    def __call__(self):
        self.plugin.kettlesend("get sys status")

class TurnOn(eg.ActionBase):
    name = "Turn ON"
	
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x4")
    
class TurnOff(eg.ActionBase):
    name = "Turn OFF"
	
    def __call__(self):
        self.plugin.kettlesend("set sys output 0x0")
    
class Boil100(eg.ActionBase):
    name = "Boil @ 100C"

    def __call__(self):
        self.plugin.kettlesend("set sys output 0x80")
    
class Boil95(eg.ActionBase):
    name = "Boil @ 95C"

    def __call__(self):
        self.plugin.kettlesend("set sys output 0x2")
    
class Boil80(eg.ActionBase):
    name = "Boil @ 80C"

    def __call__(self):
        self.plugin.kettlesend("set sys output 0x4000")
    
class Boil65(eg.ActionBase):
    name = "Boil @ 65C"

    def __call__(self):
        self.plugin.kettlesend("set sys output 0x200")
    
class Warm(eg.ActionBase):
    name = "Warm Toggle"

    def __call__(self):
        self.plugin.kettlesend("set sys output 0x8")
    
class SetWarm5(eg.ActionBase):
    name = "Set Warm @ 5 min"

    def __call__(self):
        self.plugin.kettlesend("set sys output 0x8005")
    
class SetWarm10(eg.ActionBase):
    name = "Set Warm @ 10 min"

    def __call__(self):
        self.plugin.kettlesend("set sys output 0x8010")
    
class SetWarm20(eg.ActionBase):
    name = "Set Warm @ 20 min"

    def __call__(self):
        self.plugin.kettlesend("set sys output 0x8020")
    
    

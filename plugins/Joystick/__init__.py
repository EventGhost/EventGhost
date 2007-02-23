import eg

class PluginInfo(eg.PluginInfo):
    name = "Joystick"
    author = "Bitmonster"
    version = "0.0.1"
    kind = "remote"
    description = (
        "Use joysticks and gamepads as input devices for EventGhost."
    )   


import os

EVT_DIRECTION       = 0
EVT_BTN_RELEASED    = 1
EVT_BTN_PUSHED  	= 2
EVT_X_AXIS          = 3
EVT_Y_AXIS          = 4
EVT_Z_AXIS          = 5



class Joystick(eg.PluginClass):
    
    def __start__(self):
        self.x = 0
        self.y = 0
        import imp
        path = os.path.join(os.path.dirname(__file__), "_dxJoystick.pyd")
        self._dxJoystick = imp.load_dynamic("_dxJoystick", path)
        self._dxJoystick.RegisterEventFunc(self.EventFunc)
        
        
    def __stop__(self):
        self._dxJoystick.RegisterEventFunc(None)
        
        
    def EventFunc(self, joynum, eventtype, value):
        if eventtype == EVT_BTN_PUSHED:
            self.TriggerEnduringEvent("Button" + str(value + 1))
        elif eventtype == EVT_BTN_RELEASED:
            self.EndLastEvent()
        elif eventtype == EVT_X_AXIS:
            self.x = value
            if value == 0:
                if self.y == 0:
                    self.EndLastEvent()
                elif self.y == 1:
                    self.TriggerEnduringEvent("Down")
                else:
                    self.TriggerEnduringEvent("Up")
            elif value == 1:
                self.TriggerEnduringEvent("Right")
            elif value == -1:
                self.TriggerEnduringEvent("Left")
        elif eventtype == EVT_Y_AXIS:
            self.y = value
            if value == 0:
                if self.x == 0:
                    self.EndLastEvent()
                elif self.x == 1:
                    self.TriggerEnduringEvent("Right")
                else:
                    self.TriggerEnduringEvent("Left")
            elif value == 1:
                self.TriggerEnduringEvent("Down")
            elif value == -1:
                self.TriggerEnduringEvent("Up")
        
        
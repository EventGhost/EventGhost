import eg

class PluginInfo(eg.PluginInfo):
    name = "Keyboard"
    author = "Bitmonster"
    version = "0.0.1"
    kind = "remote"
    description = "This plugin generates events on keypresses (hotkeys)."


from eg import HasActiveHandler
from eg.cFunctions import SetKeyboardCallback


LLKHF_EXTENDED = 0x01
LLKHF_INJECTED = 0x10
LLKHF_ALTDOWN = 0x20
LLKHF_UP = 0x80
    
    
    
class Keyboard(eg.PluginClass):
    
    def __start__(self, *args):
        SetKeyboardCallback(self.KeyboardCallback)
        
        
    def __stop__(self):
        SetKeyboardCallback(None)
        
        
    def KeyboardCallback(self, codes):
        if codes == "":
            self.EndLastEvent()
        else:
            shouldBlock = HasActiveHandler("Keyboard." + codes)
            self.TriggerEnduringEvent(codes)
            return shouldBlock
                
                    
        
        

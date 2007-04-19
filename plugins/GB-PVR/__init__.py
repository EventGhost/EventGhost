import eg

class PluginInfo(eg.PluginInfo):
    name = "GB-PVR"
    description = (
        'Adds support functions to control GB-PVR '
        '\n\n<p>'
        '<a href=http://www.gbpvr.com/>www.gbpvr.com<p>'
        '<center><img src="logo_small.png" alt="GB-PVR" /></a></center>'
    )
    author = "Bitmonster"
    version = "1.0.0"
    kind = "program"
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAB3RJTUUH1wQPFDUmBR98"
        "RgAAABd0RVh0U29mdHdhcmUAR0xEUE5HIHZlciAzLjRxhaThAAAACHRwTkdHTEQzAAAA"
        "AEqAKR8AAAAEZ0FNQQAAsY8L/GEFAAAAVUlEQVR4nGNgGKzgPwE+SYaQpPk/ERi35v9E"
        "YHyGQBRs3Ph/37NnYAxiI2OiDMCmkSQDcGlmmDCBAhcANRNtALomZEyUAZTEAgMDhekA"
        "3RBCYoMEAABOirV0kXTs6QAAAABJRU5ErkJggg=="
    )
    
    
ACTIONS = (
    ('Left', 'Left', (32771, 209, 0)), 
    ('Right', 'Right', (32771, 208, 0)), 
    ('Up', 'Up', (32771, 224, 0)), 
    ('Down', 'Down', (32771, 225, 0)), 
    ('Enter', 'Enter', (32771, 229, 0)), 
    ('Escape', 'Escape', (32771, 223, 0)), 
    ('Home', 'Home', (32771, 205, 0)), 
    ('Play', 'Play', (32771, 245, 0)), 
    ('Pause', 'Pause', (32771, 240, 0)), 
    ('Stop', 'Stop', (32771, 246, 0)), 
    ('Rewind', 'Rewind', (32771, 242, 0)), 
    ('FastForward', 'Fast Forward', (32771, 244, 0)), 
    ('SkipPrevious', 'Skip Previous', (32771, 228, 0)), 
    ('SkipNext', 'Skip Next', (32771, 222, 0)), 
    ('Record', 'Record', (32771, 247, 0)), 
    ('OnOff', 'On/Off', (32771, 253, 0)), 
    ('Go', 'Go', (32771, 251, 0)), 
    ('Blank', 'Blank', (32771, 204, 0)), 
    ('FullScreen', 'Full Screen', (32771, 252, 0)), 
    ('Red', 'Red', (32771, 242, 0)), 
    ('Green', 'Green', (32771, 238, 0)), 
    ('Yellow', 'Yellow', (32771, 248, 0)), 
    ('Blue', 'Blue', (32771, 233, 0)), 
    ('Num0', 'Num 0', (32771, 192, 0)), 
    ('Num1', 'Num 1', (32771, 193, 0)), 
    ('Num2', 'Num 2', (32771, 194, 0)), 
    ('Num3', 'Num 3', (32771, 195, 0)), 
    ('Num4', 'Num 4', (32771, 196, 0)), 
    ('Num5', 'Num 5', (32771, 197, 0)), 
    ('Num6', 'Num 6', (32771, 198, 0)), 
    ('Num7', 'Num 7', (32771, 199, 0)), 
    ('Num8', 'Num 8', (32771, 200, 0)), 
    ('Num9', 'Num 9', (32771, 201, 0)), 
)


from win32gui import FindWindow, SendMessageTimeout
from win32con import SMTO_ABORTIFHUNG, SMTO_NORMAL


class GbpvrAction(eg.ActionClass):
    
    def __call__(self):
        """
        Find GB-PVR's window and send it a message with SendMessageTimeout.
        """
        msg, wParam, lParam = self.value
        try:
            return SendMessageTimeout(
                FindWindow(None, "GB-PVR"), 
                msg, 
                wParam, 
                lParam, 
                SMTO_ABORTIFHUNG|SMTO_NORMAL, 
                1000
            )[1]
        except:
            self.PrintError("GB-PVR is not running!")
        
        
        
class GBPVR(eg.PluginClass):
    
    def __init__(self):
        for actionIdent, actionName, actionValue in ACTIONS:
            class tmpAction(GbpvrAction):
                name = actionName
                value = actionValue
            tmpAction.__name__ = actionIdent
            self.AddAction(tmpAction)
            
                
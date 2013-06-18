import time
import win32gui
import win32con
import win32api

import eg

fnList = (
('1', 'Simulate a press on the Num1 button', 125),
('2', 'Simulate a press on the Num2 button', 126),
('3', 'Simulate a press on the Num3 button', 127),
('4', 'Simulate a press on the Num4 button', 128),
('5', 'Simulate a press on the Num5 button', 129),
('6', 'Simulate a press on the Num6 button', 130),
('7', 'Simulate a press on the Num7 button', 131),
('8', 'Simulate a press on the Num8 button', 132),
('9', 'Simulate a press on the Num9 button', 133),
('0', 'Simulate a press on the Num0 button', 134),
('+', 'Simulate a press on the + button', 124),
('-', 'Simulate a press on the - button', 92),
('x', 'Simulate a press on the x button', 93),
('/', 'Simulate a press on the / button', 91),
('C', 'Simulate a press on the C', 81),
('CE', 'Simulate a press on the CE', 82),
('M+', 'Simulate a press on the M+', 116),
('MS', 'Simulate a press on the MS', 115),
('MR', 'Simulate a press on the MR', 114),
('MC', 'Simulate a press on the MC', 113),
('=', 'Simulate a press on the = button', 112),
('back', 'Simulate a press on the back', 183),
)

def _command(data):
    try:
        hcalc = win32gui.FindWindow('SciCalc', None)
        return win32api.SendMessage(hcalc, win32con.WM_COMMAND , data, 0)
    except:
        eg.PrintError("Calc not running")

def _usercommand(id, data=0):
    try:
        hcalc = win32gui.FindWindow('SciCalc', None)
        return win32api.SendMessage(hcalc, win32con.WM_USER, data, id)
    except:
        eg.PrintError("Calc not running")


class Calc(eg.PluginClass):
    
    def __init__(self):
        group = self.AddGroup()
        
        for tmp_name, tmp_description, tmp_value in fnList:
            class tmp_action:
                name = tmp_name
                description = tmp_description
                value = tmp_value
                def __call__(self):
                    return _command(self.value)
            tmp_action.__name__ = "Calc" + tmp_name        
            group.AddAction(tmp_action)


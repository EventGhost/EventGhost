import eg
import wx


class SerialPortChoice(wx.Choice):
    """
    This Choice control will be setup with a list of all available serial 
    ports on the system. 
    """
    
    def __init__(
        self, 
        parent, 
        id=-1, 
        pos=wx.DefaultPosition, 
        size=wx.DefaultSize, 
        style=0, 
        validator=wx.DefaultValidator, 
        name=wx.ChoiceNameStr, 
        value=None
    ):
        """
        :Parameters:
            `value` : int
                The initial port to select (0 = COM1:). The first available
                port will be selected if the given port does not exist or
                no value is given.
        """
        
        ports = eg.SerialPort.GetAllPorts()
        self.ports = ports
        choices = [("COM%d" % (portnum + 1)) for portnum in ports]
        wx.Choice.__init__(
            self, parent, id, pos, size, choices, style, validator, name
        )
        try:
            portPos = ports.index(value)
        except ValueError:
            portPos = 0
        self.SetSelection(portPos)
        
        
    def GetValue(self):
        """
        Return the currently selected serial port.
        
        :rtype: int
        :returns: The serial port as an integer (0 = COM1:)
        """
        try:
            port = self.ports[self.GetSelection()]
        except:
            port = 0
        return port
        
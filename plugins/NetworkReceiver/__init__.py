import eg

class PluginInfo(eg.PluginInfo):
    name = "Network Event Receiver"
    description = "Receives events from Network Event Sender plugins."
    version = "1.0.0"
    author = "Bitmonster"
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/"
        "AAAACXBIWXMAAAsSAAALEgHS3X78AAAAB3RJTUUH1gIQFgQb1MiCRwAAAVVJREFUOMud"
        "kjFLw2AQhp8vif0fUlPoIgVx6+AgopNI3fwBViiIoOAgFaugIDhUtP4BxWDs4CI4d3MR"
        "cSyIQ1tDbcHWtjFI4tAWG5pE8ca7997vnrtP4BOZvW0dSBAcZ0pAMTEzPUs4GvMsVkvP"
        "6HktGWRAOBpjIXVNKOSWWdYXN7lFAAINhBCEQgqxyTHAAQQAD/dFbLurUYJYT7P7TI2C"
        "VavwIiZodyyaH6ZLo/RZVTXiOYVhGOh5jcpbq5eRAXAc5wdBVSPMLR16GtxdbgJgN95d"
        "OxicACG6bPH4uIu1UHjE7sFqR/NDVxhaoixLvFYbtDufNFtu1tzxgdeAaZfBU7ECTvd1"
        "WRlxsa4sp1ydkiRxkstmlEFRrWT4nrRer3vmlf6mb883fK8AoF1d+Bqc6Xkt+cufT6e3"
        "dnb9DJJrq+uYpunZ2WcFfA0ol8v8N5Qgvr/EN8Lzfbs+L0goAAAAAElFTkSuQmCC"
    )

import wx

import asynchat
import asyncore
import md5
import random
import socket



class Text:
    port = "Port:"
    password = "Password:"
    event_prefix = "Event Prefix:"
    


class Server_Handler (asynchat.async_chat):
    """Telnet engine class. Implements command line user interface."""
    
    def __init__ (self, sock, addr, hex_md5, cookie, handler, server_ref):
        self.handler = handler
        self.server_ref = server_ref
        
        # Call constructor of the parent class
        asynchat.async_chat.__init__(self, sock)

        # Set up input line terminator
        self.set_terminator('\n')

        # Initialize input data buffer
        self.data = ''
        self.state = self.state1
        self.ip = addr[0]
        self.payload = [self.ip]
        self.hex_md5 = hex_md5
        self.cookie = cookie
                  
                
    def handle_close(self):
        self.handler.EndLastEvent()
        asynchat.async_chat.handle_close(self)
    
    
    def collect_incoming_data (self, data):
        """Put data read from socket to a buffer
        """
        # Collect data in input buffer
        self.data = self.data + data


    def found_terminator (self):
        """
        This method is called by asynchronous engine when it finds
        command terminator in the input stream
        """   
        # Take the complete line
        line = self.data

        # Reset input buffer
        self.data = ''

        #call state handler
        self.state(line)


    def initiate_close(self):
        if self.writable():
            self.push("close\n")
        #asynchat.async_chat.handle_close(self)
        self.handler.EndLastEvent()
        self.state = self.state1
 

    def state1(self, line):
        """
        get keyword "quintessence\n" and send cookie
        """
        if line == "quintessence":
            self.state = self.state2
            self.push(self.cookie + "\n")
        else:
            self.initiate_close()
                
                
    def state2(self, line):
        """get md5 digest
        """
        line = line.strip()[-32:]
        if line == "":
            pass
        elif line.upper() == self.hex_md5:
            self.push("accept\n")
            self.state = self.state3
        else:
            eg.PrintError("NetworkReceiver md5 error")
            self.initiate_close()
            
            
    def state3(self, line):
        if line == "close":
            self.initiate_close()
        elif line[:8] == "payload ":
            self.payload.append(line[8:])
        else:
            if line == "ButtonReleased":
                self.handler.EndLastEvent()
            else:
                if self.payload[-1] == "withoutRelease":
                    self.handler.TriggerEnduringEvent(line, self.payload)
                else:
                    self.handler.TriggerEvent(line, self.payload)
            self.payload = [self.ip]
            
            

class Server(asyncore.dispatcher):
    
    def __init__ (self, port, password, handler):
        self.handler = handler
        m = md5.new()
        self.cookie = hex(random.randrange(65536))
        self.cookie = self.cookie[len(self.cookie) - 4:]
        m.update(self.cookie + ":" + password)
        self.hex_md5 = m.hexdigest().upper()

        # Call parent class constructor explicitly
        asyncore.dispatcher.__init__(self)
        
        # Create socket of requested type
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set it to re-use address
        self.set_reuse_addr()
        
        # Bind to all interfaces of this host at specified port
        self.bind(('', port))
        
        # Start listening for incoming requests
        #self.listen (1024)
        self.listen(5)


    def handle_accept (self):
        """Called by asyncore engine when new connection arrives"""
        # Accept new connection
        (sock, addr) = self.accept()
        Server_Handler(
            sock, 
            addr, 
            self.hex_md5, 
            self.cookie, 
            self.handler, 
            self
        )



class NetworkReceiver(eg.PluginClass):
    canMultiLoad = True
    text = Text
    
    def __start__(self, port, password, prefix):
        self.port = port
        self.password = password
        self.info.eventPrefix = prefix
        self.server = Server(self.port, self.password, self)
        
        
    def __stop__(self):
        if self.server:
            self.server.close()
        self.server = None


    def Configure(self, port=1024, password="", prefix="TCP"):
        dialog = eg.ConfigurationDialog(self)
        ctrl1 = eg.SpinIntCtrl(dialog, -1, port, max=65535)
        ctrl2 = wx.TextCtrl(dialog, -1, password, style=wx.TE_PASSWORD)
        ctrl3 = wx.TextCtrl(dialog, -1, prefix)
        
        dialog.AddLabel(self.text.port)
        dialog.AddCtrl(ctrl1)
        dialog.AddLabel(self.text.password)
        dialog.AddCtrl(ctrl2)
        dialog.AddLabel(self.text.event_prefix)
        dialog.AddCtrl(ctrl3)
        
        if dialog.AffirmedShowModal():
            return ctrl1.GetValue(), ctrl2.GetValue(), ctrl3.GetValue()


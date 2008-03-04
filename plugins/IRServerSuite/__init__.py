
eg.RegisterPlugin(
    name = "IR Server Suite",
    kind = "remote",
)

import socket
import struct
import time
import asyncore

class Enum(object):
    def __init__(self):
        for i, name in enumerate(self._names):
            setattr(self, name, i)



class MessageType(Enum):
    _names = [
        "Unknown", 
        "RegisterClient", 
        "UnregisterClient", 
        "RegisterRepeater", 
        "UnregisterRepeater", 
        "LearnIR", 
        "BlastIR", 
        "Error", 
        "ServerShutdown", 
        "ServerSuspend", 
        "ServerResume", 
        "RemoteEvent", 
        "KeyboardEvent", 
        "MouseEvent", 
        "ForwardRemoteEvent", 
        "ForwardKeyboardEvent", 
        "ForwardMouseEvent", 
        "AvailableReceivers", 
        "AvailableBlasters", 
        "ActiveReceivers", 
        "ActiveBlasters", 
        "DetectedReceivers", 
        "DetectedBlasters",
    ]
MessageType = MessageType()

class MessageFlags:
    NoneFlag = 0x0000
    Request = 0x0001
    Response = 0x0002
    Notify = 0x0004
    Success = 0x0008
    Failure = 0x0010
    Timeout = 0x0020
    ForceNotRespond = 0x0400
    
    
class Client(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        # restart the asyncore loop, so it notices the new socket
        #eg.RestartAsyncore()
        self.connect(("localhost", 24000))
        self.buffer = "\x00\x00\x00\x08\x01\x00\x00\x00\x01\x00\x00\x00"

    def writable(self):
        return 0
    
    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print repr(self.recv(8192))

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
        
    def handle_expt(self):
        self.close() # connection failed, shutdown
        
        
class IRServerSuite(eg.PluginClass):
    
    def __start__(self):
        self.client = Client()
        
        
    def GetMessage(self):
        numBytes = struct.unpack("!L", self.sock.recv(4))[0]
        buf = self.sock.recv(numBytes)
        mesgType, mesgFlags = struct.unpack("LL", buf[:8])
        data = buf[8:]
        return mesgType, mesgFlags, data
        
        
        
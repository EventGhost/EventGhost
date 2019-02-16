from eg.WinApi.Dynamic import _kernel32
from ctypes import WinError, create_string_buffer, c_size_t
#from win32api import CloseHandle

    
PROCESS_ALL_ACCESS        = 0x1F0FFF
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION      = 0x0008
PROCESS_VM_READ           = 0x0010
PROCESS_VM_WRITE          = 0x0020


#! WinError() function raises & fills in WindowsError() exception !#
class MemoryReader:
    
    def __init__(self, pid):
        self._hProcess = None
        self.pid = pid

        
    def read_string(self, address, maxlen=260):
        """The entire area to be read must be accessible, and if it is not accessible, the function fails."""
        if not self._hProcess:
            # The handle must have PROCESS_VM_READ access to the process.
            self._hProcess = _kernel32.OpenProcess(PROCESS_VM_READ, False, self.pid)
            if not self._hProcess:
                WinError()
        buffer = create_string_buffer(maxlen)
        # lpNumberOfBytesRead = c_size_t(0) # or NULL
        # if not _kernel32.ReadProcessMemory(self._hProcess, address, buffer, maxlen, byref(lpNumberOfBytesRead))
        if not _kernel32.ReadProcessMemory(self._hProcess, address, buffer, maxlen, None):
            WinError()
        # print "mem: "+hex(address)
        # print "read: "+str(lpNumberOfBytesRead)
        # print "strlen: %d" % (len(buffer.value))
        # print [buffer[i] for i in range(maxlen)]
        return buffer.value
        
        
    def __del__(self):
        if self._hProcess:
            _kernel32.CloseHandle(self._hProcess)
            self._hProcess = None
        

# W7 wont run read process memory?
# You may need to check your access permissions for "SE_DEBUG_NAME" for the current processes token. 
# If not enabled. Enabled it. This must be done as administrator of course.
# http://msdn.microsoft.com/en-us/library/windows/desktop/ms680553%28v=vs.85%29.aspx

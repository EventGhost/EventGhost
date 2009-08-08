# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from Dynamic import (
    byref,
    sizeof,
    cast,
    DWORD,
    LPBYTE,
    OpenSCManager, 
    SC_MANAGER_ALL_ACCESS, 
    CreateService, 
    SERVICE_ALL_ACCESS, 
    SERVICE_WIN32_OWN_PROCESS,
    SERVICE_DEMAND_START,
    SERVICE_AUTO_START,
    SERVICE_ERROR_NORMAL,
    CloseServiceHandle,
    FormatError,
    DELETE,
    OpenService,
    DeleteService,
    QueryServiceStatusEx,
    SC_STATUS_PROCESS_INFO,
    SERVICE_STATUS_PROCESS,
    SERVICE_QUERY_STATUS,
    SERVICE_STOPPED,
    SERVICE_STOP_PENDING,
    SERVICE_START_PENDING,
    SERVICE_RUNNING,
    SERVICE_CONTROL_STOP,
    SERVICE_ACTIVE,
    GetTickCount,
    Sleep,
    StartService,
    ControlService,
    LPSERVICE_STATUS,
    EnumDependentServices,
    ERROR_MORE_DATA,
    GetLastError,
    ChangeServiceConfig2,
    SERVICE_DESCRIPTION,
    SERVICE_CONFIG_DESCRIPTION,
    SERVICE_CHANGE_CONFIG,
)

class FailedFunc(Exception):
    
    def __init__(self, funcName):
        Exception.__init__(self)
        self.funcName = funcName
        self.errorMsg = FormatError()
        
    def __str__(self):
        return "%s: %s" % (self.funcName, self.errorMsg)



class Service(object):
    schService = None
    schSCManager = None
    
    def __init__(self, serviceName):
        self.serviceName = serviceName
        self.ssStatus = SERVICE_STATUS_PROCESS()
        
        
    def GetServiceControlManager(self):
        if self.schSCManager:
            return
        # Get a handle to the SCM database.
        schSCManager = OpenSCManager( 
            None,                    # local computer
            None,                    # ServicesActive database 
            SC_MANAGER_ALL_ACCESS    # full access rights 
        )
        if not schSCManager:
            raise FailedFunc("OpenSCManager")
        self.schSCManager = schSCManager


    def GetServiceHandle(self):
        if self.schService:
            return
        self.GetServiceControlManager()
        # Get a handle to the service.
        self.schService = OpenService( 
            self.schSCManager,       # SCM database 
            self.serviceName,        # name of service 
            SERVICE_ALL_ACCESS       # need delete access 
        )
        if not self.schService:
            raise FailedFunc("OpenService")


    def SetDescription(self, description):
        self.GetServiceHandle()
        serviceDescription = SERVICE_DESCRIPTION()
        serviceDescription.lpDescription = description
        if not ChangeServiceConfig2(
            self.schService, # handle to service
            SERVICE_CONFIG_DESCRIPTION, # change: description
            byref(serviceDescription) # new description
        ):
            raise FailedFunc("ChangeServiceConfig2")


    def Install(self, path):
        self.GetServiceControlManager()
        # Create the service
        schService = CreateService( 
            self.schSCManager,              # SCM database 
            self.serviceName,               # name of service 
            self.serviceName,               # service name to display 
            SERVICE_ALL_ACCESS,        # desired access 
            SERVICE_WIN32_OWN_PROCESS, # service type 
            SERVICE_AUTO_START,        # start type 
            SERVICE_ERROR_NORMAL,      # error control type 
            path,                    # path to service's binary 
            None,                      # no load ordering group 
            None,                      # no tag identifier 
            None,                      # no dependencies 
            None,                      # LocalSystem account 
            None                       # no password 
        )
        if not schService:
            raise FailedFunc("CreateService")
        else:
            print ("Service installed successfully")
            CloseServiceHandle(schService)


    def Uninstall(self):
        self.GetServiceHandle()
        if not DeleteService(self.schService):
            raise FailedFunc("DeleteService")
    

    def GetStatus(self):
        dwBytesNeeded = DWORD() 
        result = QueryServiceStatusEx( 
            self.schService, # handle to service 
            SC_STATUS_PROCESS_INFO, # information level
            cast(byref(self.ssStatus), LPBYTE), # address of structure
            sizeof(self.ssStatus), # size of structure
            byref(dwBytesNeeded) # size needed if buffer is too small
        )
        if not result:
            raise FailedFunc("QueryServiceStatusEx")
        return self.ssStatus


    def Start(self):
        self.GetServiceHandle()
        # Check the status in case the service is not stopped. 
        ssStatus = self.GetStatus()
        # Check if the service is already running. It would be possible to stop
        # the service here, but for simplicity this example just returns. 
        if (
            ssStatus.dwCurrentState != SERVICE_STOPPED 
            and ssStatus.dwCurrentState != SERVICE_STOP_PENDING
        ):
            raise Exception(
                "Cannot start the service because it is already running"
            )
        
        # Save the tick count and initial checkpoint.
        dwStartTickCount = GetTickCount()
        dwOldCheckPoint = ssStatus.dwCheckPoint
        # Wait for the service to stop before attempting to start it.
        while ssStatus.dwCurrentState == SERVICE_STOP_PENDING:
            # Do not wait longer than the wait hint. A good interval is 
            # one-tenth of the wait hint but not less than 1 second  
            # and not more than 10 seconds. 
            Sleep(min(max(1000, ssStatus.dwWaitHint / 10), 10000))
            
            # Check the status until the service is no longer stop pending. 
            ssStatus = self.GetStatus()
            
            if ssStatus.dwCheckPoint > dwOldCheckPoint:
                # Continue to wait and check.
                dwStartTickCount = GetTickCount()
                dwOldCheckPoint = ssStatus.dwCheckPoint
            else:
                if GetTickCount() - dwStartTickCount > ssStatus.dwWaitHint:
                    raise Exception("Timeout waiting for service to stop")
        # Attempt to start the service.
        if not StartService(
            self.schService,  # handle to service 
            0,                # number of arguments 
            None              # no arguments 
        ):
            raise FailedFunc("StartService")
        print("Service start pending...")
        # Check the status until the service is no longer start pending. 
        ssStatus = self.GetStatus()
        # Save the tick count and initial checkpoint.
        dwStartTickCount = GetTickCount()
        dwOldCheckPoint = ssStatus.dwCheckPoint
        while ssStatus.dwCurrentState == SERVICE_START_PENDING:
            # Do not wait longer than the wait hint. A good interval is 
            # one-tenth the wait hint, but no less than 1 second and no 
            # more than 10 seconds. 
            Sleep(min(max(1000, ssStatus.dwWaitHint / 10), 10000))
    
            # Check the status again. 
            ssStatus = self.GetStatus()
     
            if ssStatus.dwCheckPoint > dwOldCheckPoint:
                # Continue to wait and check.
                dwStartTickCount = GetTickCount()
                dwOldCheckPoint = ssStatus.dwCheckPoint
            else:
                if GetTickCount() - dwStartTickCount > ssStatus.dwWaitHint:
                    # No progress made within the wait hint.
                    break
        # Determine whether the service is running.
    
        if ssStatus.dwCurrentState == SERVICE_RUNNING:
            print "Service started successfully."
        else :
            print "Service not started."
            print "  Current State:", ssStatus.dwCurrentState
            print "  Exit Code:", ssStatus.dwWin32ExitCode
            print "  Check Point:", ssStatus.dwCheckPoint
            print "  Wait Hint:", ssStatus.dwWaitHint


    def Stop(self):
        self.GetServiceHandle()
        # Make sure the service is not already stopped.
        ssStatus = self.GetStatus()
        if ssStatus.dwCurrentState == SERVICE_STOPPED:
            return
        # If a stop is pending, wait for it.
        dwStartTime = GetTickCount()
        dwTimeout = 30000
        while ssStatus.dwCurrentState == SERVICE_STOP_PENDING:
            # Do not wait longer than the wait hint. A good interval is 
            # one-tenth of the wait hint but not less than 1 second  
            # and not more than 10 seconds. 
            Sleep(min(max(1000, ssStatus.dwWaitHint / 10), 10000))
    
            ssStatus = self.GetStatus()
    
            if ssStatus.dwCurrentState == SERVICE_STOPPED:
                return
            if GetTickCount() - dwStartTime > dwTimeout:
                raise Exception("Timeout waiting for service to stop")
        # If the service is running, dependencies must be stopped first.
        #self.StopDependentServices()
        
        # Send a stop code to the service.
        if not ControlService( 
                self.schService, 
                SERVICE_CONTROL_STOP, 
                cast(byref(ssStatus), LPSERVICE_STATUS)
        ):
            raise FailedFunc("ControlService")
        
        # Wait for the service to stop.
        while ssStatus.dwCurrentState != SERVICE_STOPPED:
            Sleep(ssStatus.dwWaitHint)
            ssStatus = self.GetStatus()
            if ssStatus.dwCurrentState == SERVICE_STOPPED:
                break
            if GetTickCount() - dwStartTime > dwTimeout:
                raise Exception("Timeout waiting for service to stop")

    
    def StopDependentServices(self):
        # Pass a zero-length buffer to get the required buffer size.
        dwBytesNeeded = DWORD()
        dwCount = DWORD()
        if EnumDependentServices(
            self.schService, 
            SERVICE_ACTIVE, 
            None,
            0, 
            byref(dwBytesNeeded), 
            byref(dwCount)
        ):
            # If the Enum call succeeds, then there are no dependent
            # services, so do nothing.
            return True
        if GetLastError() != ERROR_MORE_DATA:
            return False # Unexpected error

        # Allocate a buffer for the dependencies.
        lpDependencies = cast(
            HeapAlloc( 
                GetProcessHeap(), 
                HEAP_ZERO_MEMORY, 
                dwBytesNeeded
            ),
            LPENUM_SERVICE_STATUS
        )
            
        if not lpDependencies:
            return False
        for i in range(dwCount):
            #ess = *(lpDependencies + i)
            # Open the service.
            hDepService = OpenService(
                self.schSCManager, 
                ess.lpServiceName, 
                SERVICE_STOP | SERVICE_QUERY_STATUS
            )
            if not hDepService:
               return False
            try:
                # Send a stop code.
                if not ControlService(
                    hDepService, 
                    SERVICE_CONTROL_STOP,
                    (LPSERVICE_STATUS) &ssp
                ):
                    return False
                # Wait for the service to stop.
                while ssStatus.dwCurrentState != SERVICE_STOPPED:
                    Sleep(ssStatus.dwWaitHint)
                    ssStatus = self.GetStatus()
                    if ssStatus.dwCurrentState == SERVICE_STOPPED:
                        break
                    if GetTickCount() - dwStartTime > dwTimeout:
                        return False
            finally:
                # Always release the service handle.
                CloseServiceHandle(hDepService)
        return True
                
        
    def __del__(self):
        if self.schService:
            CloseServiceHandle(self.schService)
        if self.schSCManager:
            print "closing schSCManager"
            CloseServiceHandle(self.schSCManager)


from Dynamic import (
    SHELLEXECUTEINFO,
    SEE_MASK_FLAG_DDEWAIT,
    SEE_MASK_FLAG_NO_UI,
    SEE_MASK_NOCLOSEPROCESS,
    SW_SHOWNORMAL,
    WaitForSingleObject,
    INFINITE,
)
import ctypes
#from eg.WinApi.Dynamic import ShellExecuteExW

def RunAsAdministrator(filePath, parameters):
    sei = SHELLEXECUTEINFO()
    sei.cbSize = sizeof(SHELLEXECUTEINFO)
    sei.fMask = (
        SEE_MASK_FLAG_DDEWAIT | SEE_MASK_FLAG_NO_UI | SEE_MASK_NOCLOSEPROCESS
    )
    sei.lpVerb = u"runas"
    sei.lpFile = filePath
    sei.lpParameters = parameters
    sei.nShow = SW_SHOWNORMAL
    if not ctypes.windll.shell32.ShellExecuteExW(byref(sei)):
        print "Error: ShellExecuteEx failed %s" % FormatError
        return False
    print sei.hProcess
    WaitForSingleObject(sei.hProcess, INFINITE)
    print "done"
    return True

if __name__ == "__main__":
    import time
    print "huhu"
    time.sleep(3)
    import atexit
    atexit.register(time.sleep, 3)
    import sys
    SVCNAME = u"EvenGhost MCE Remote Service"
    szPath = r"D:\tmp\AlternateMceIrService.exe"
    service = Service(SVCNAME)
    service.Uninstall()
    print "done"
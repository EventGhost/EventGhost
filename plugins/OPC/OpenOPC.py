###########################################################################
#
# OpenOPC for Python Library Module
#
# Copyright (c) 2007-2008 Barry Barnreiter (barry_b@users.sourceforge.net)
#
###########################################################################

import os
import sys
import time
import types
import string
import socket
import re
import Queue

__version__ = '1.1.6'

current_client = None

# Win32 only modules not needed for 'open' protocol mode
if os.name == 'nt':
   try:
      import win32com.client
      import win32com.server.util
      import win32event
      import pythoncom
      import pywintypes
      import SystemHealth
      
      # Win32 variant types
      vt = dict([(pythoncom.__dict__[vtype], vtype) for vtype in pythoncom.__dict__.keys() if vtype[:2] == "VT"])

      # Allow gencache to create the cached wrapper objects
      win32com.client.gencache.is_readonly = False
    
      # Under p2exe the call in gencache to __init__() does not happen
      # so we use Rebuild() to force the creation of the gen_py folder
      win32com.client.gencache.Rebuild()

   # So we can work on Windows in "open" protocol mode without the need for the win32com modules
   except ImportError:
      win32com_found = False
   else:
      win32com_found = True
else:
   win32com_found = False

# OPC Constants

SOURCE_CACHE = 1
SOURCE_DEVICE = 2
OPC_STATUS = (0, 'Running', 'Failed', 'NoConfig', 'Suspended', 'Test')
BROWSER_TYPE = (0, 'Hierarchical', 'Flat')
ACCESS_RIGHTS = (0, 'Read', 'Write', 'Read/Write')
OPC_QUALITY = ('Bad', 'Uncertain', 'Unknown', 'Good')
OPC_CLASS = 'Matrikon.OPC.Automation;Graybox.OPC.DAWrapper;HSCOPC.Automation;RSI.OPCAutomation;OPC.Automation'
OPC_SERVER = 'Hci.TPNServer;HwHsc.OPCServer;opc.deltav.1;AIM.OPC.1;Yokogawa.ExaopcDAEXQ.1;OSI.DA.1;OPC.PHDServerDA.1;Aspen.Infoplus21_DA.1;National Instruments.OPCLabVIEW;RSLinx OPC Server;KEPware.KEPServerEx.V4;Matrikon.OPC.Simulation;Prosys.OPC.Simulation'
OPC_CLIENT = 'OpenOPC'

def quality_str(quality_bits):
   """Convert OPC quality bits to a descriptive string"""

   quality = (quality_bits >> 6) & 3
   return OPC_QUALITY[quality]

def type_check(tags):
   """Perform a type check on a list of tags"""
   
   if type(tags) in (types.ListType, types.TupleType):
      single = False
   elif tags == None:
      tags = []
      single = False
   else:
      tags = [tags]
      single = True

   if len([t for t in tags if type(t) not in types.StringTypes]) == 0:
      valid = True
   else:
      valid = False

   return tags, single, valid

def wild2regex(string):
   """Convert a Unix wildcard glob into a regular expression"""
   return string.replace('.','\.').replace('*','.*').replace('?','.').replace('!','^')

def tags2trace(tags):
   """Convert a list tags into a formatted string suitable for the trace callback log"""
   arg_str = ''
   for i,t in enumerate(tags[1:]):
      if i > 0: arg_str += ','
      arg_str += '%s' % t
   return arg_str

def exceptional(func, alt_return=None, alt_exceptions=(Exception,), final=None, catch=None):
   """Turns exceptions into an alternative return value"""

   def _exceptional(*args, **kwargs):
      try:
         try:
            return func(*args, **kwargs)
         except alt_exceptions:
            return alt_return
         except:
            if catch: return catch(sys.exc_info(), lambda:func(*args, **kwargs))
            raise
      finally:
         if final: final()
   return _exceptional

def get_sessions(host='localhost', port=7766):
   """Return sessions in OpenOPC Gateway Service as GUID:host hash"""
   
   import Pyro.core
   Pyro.core.initClient(banner = 0)
   server_obj = Pyro.core.getProxyForURI("PYROLOC://%s:%s/opc" % (host, port))
   return server_obj.get_clients()

def open_client(host='localhost', port=7766):
   """Connect to the specified OpenOPC Gateway Service"""
   
   import Pyro.core
   Pyro.core.initClient(banner=0)
   server_obj = Pyro.core.getProxyForURI("PYROLOC://%s:%s/opc" % (host, port))
   return server_obj.create_client()

class TimeoutError(Exception):
   def __init__(self, txt):
      Exception.__init__(self, txt)

class OPCError(Exception):
   def __init__(self, txt):
      Exception.__init__(self, txt)

class GroupEvents:
   def __init__(self):
      self.client = current_client
        
   def OnDataChange(self, TransactionID, NumItems, ClientHandles, ItemValues, Qualities, TimeStamps):
      self.client.callback_queue.put((TransactionID, ClientHandles, ItemValues, Qualities, TimeStamps))
   
class client():
   def __init__(self, opc_class=None, client_name=None):
      """Instantiate OPC automation class"""

      self.callback_queue = Queue.Queue()

      pythoncom.CoInitialize()

      if opc_class == None:
         if os.environ.has_key('OPC_CLASS'):
            opc_class = os.environ['OPC_CLASS']
         else:
            opc_class = OPC_CLASS

      opc_class_list = opc_class.split(';')

      for i,c in enumerate(opc_class_list):
         try:
            print c
            self._opc = win32com.client.gencache.EnsureDispatch(c, 0)
            self.opc_class = c
            break
         except pythoncom.com_error, err:
            if i == len(opc_class_list)-1:
               error_msg = 'Dispatch: %s' % self._get_error_str(err)
               raise OPCError, error_msg
            
      self._event = win32event.CreateEvent(None,0,0,None)

      self.opc_server = None
      self.opc_host = None
      self.client_name = client_name
      self._groups = {}
      self._group_tags = {}
      self._group_valid_tags = {}
      self._group_server_handles = {}
      self._group_handles_tag = {}
      self._group_hooks = {}
      self._open_serv = None
      self._open_self = None
      self._open_host = None
      self._open_port = None
      self._open_guid = None
      self._prev_serv_time = None
      self._tx_id = 0
      self.trace = None
      self.cpu = None

   def set_trace(self, trace):
      if self._open_serv == None:
         self.trace = trace

   def connect(self, opc_server=None, opc_host='localhost'):
      """Connect to the specified OPC server"""

      pythoncom.CoInitialize()
      
      if opc_server == None:
         # Initial connect using environment vars
         if self.opc_server == None:
            if os.environ.has_key('OPC_SERVER'):
               opc_server = os.environ['OPC_SERVER']
            else:
               opc_server = OPC_SERVER
         # Reconnect using previous server name
         else:
            opc_server = self.opc_server
            opc_host = self.opc_host

      opc_server_list = opc_server.split(';')
      connected = False

      for s in opc_server_list:
         try:
            if self.trace: self.trace('Connect(%s,%s)' % (s, opc_host))
            self._opc.Connect(s, opc_host)
         except pythoncom.com_error, err:
            if len(opc_server_list) == 1:
               error_msg = 'Connect: %s' % self._get_error_str(err)
               raise OPCError, error_msg
         else:
            # Set client name since some OPC servers use it for security
            if self.client_name == None:
                if os.environ.has_key('OPC_CLIENT'):
                   self._opc.ClientName = os.environ['OPC_CLIENT']
                else:
                   self._opc.ClientName = OPC_CLIENT
            else:
                self._opc.ClientName = self.client_name
            connected = True
            break

      if not connected:
         raise OPCError, 'Connect: Cannot connect to any of the servers in the OPC_SERVER list'

      # With some OPC servers, the next OPC call immediately after Connect()
      # will occationally fail.  Sleeping for 1/100 second seems to fix this.
      time.sleep(0.01)

      self.opc_server = opc_server
      if opc_host == 'localhost':
         opc_host = socket.gethostname()
      self.opc_host = opc_host

      # On reconnect we need to remove the old group names from OpenOPC's internal
      # cache since they are now invalid
      self._groups = {}
      self._group_tags = {}
      self._group_valid_tags = {}
      self._group_server_handles = {}
      self._group_handles_tag = {}
      self._group_hooks = {}

   def close(self, del_object=True):
      """Disconnect from the currently connected OPC server"""

      try:
         pythoncom.CoInitialize()
         self.remove(self.groups())

      except pythoncom.com_error, err:
         error_msg = 'Disconnect: %s' % self._get_error_str(err)
         raise OPCError, error_msg

      except OPCError:
         pass

      finally:
         if self.trace: self.trace('Disconnect()')
         self._opc.Disconnect()

         # Remove this object from the open gateway service
         if self._open_serv and del_object:
            self._open_serv.release_client(self._open_self)

   def iread(self, tags=None, group=None, size=None, pause=0, source='hybrid', update=-1, timeout=5000, sync=False, include_error=False, rebuild=False):
      """Iterable version of read()"""

      def add_items(tags):
         names = list(tags)

         names.insert(0,0)
         errors = []
          
         if self.trace: self.trace('Validate(%s)' % tags2trace(names))
          
         try:
            errors = opc_items.Validate(len(names)-1, names)
         except:
            pass
             
         valid_tags = []
         valid_values = []
         client_handles = []

         if not self._group_handles_tag.has_key(sub_group):
            self._group_handles_tag[sub_group] = {}
            n = 0
         else:
            n = max(self._group_handles_tag[sub_group]) + 1
          
         for i, tag in enumerate(tags):
            if errors[i] == 0:
               valid_tags.append(tag)
               client_handles.append(n)
               self._group_handles_tag[sub_group][n] = tag 
               n += 1
            elif include_error:
               error_msgs[tag] = self._opc.GetErrorString(errors[i])

         client_handles.insert(0,0)
         valid_tags.insert(0,0)
         server_handles = []
         errors = []

         if self.trace: self.trace('AddItems(%s)' % tags2trace(valid_tags))
       
         try:
            server_handles, errors = opc_items.AddItems(len(client_handles)-1, valid_tags, client_handles)
         except:
            pass
             
         valid_tags_tmp = []
         server_handles_tmp = []
         valid_tags.pop(0)

         if not self._group_server_handles.has_key(sub_group):
            self._group_server_handles[sub_group] = {}
       
         for i, tag in enumerate(valid_tags):
            if errors[i] == 0:
               valid_tags_tmp.append(tag)
               server_handles_tmp.append(server_handles[i])
               self._group_server_handles[sub_group][tag] = server_handles[i]
            elif include_error:
               error_msgs[tag] = self._opc.GetErrorString(errors[i])
       
         valid_tags = valid_tags_tmp
         server_handles = server_handles_tmp

         return valid_tags, server_handles

      def remove_items(tags):
         if self.trace: self.trace('RemoveItems(%s)' % tags2trace(['']+tags))
         server_handles = [self._group_server_handles[sub_group][tag] for tag in tags]
         server_handles.insert(0,0)
         errors = []

         try:
            errors = opc_items.Remove(len(server_handles)-1, server_handles)
         except pythoncom.com_error, err:
            error_msg = 'RemoveItems: %s' % self._get_error_str(err)
            raise OPCError, error_msg

      try:
         self._update_tx_time()
         pythoncom.CoInitialize()
         
         if include_error:
            sync = True
            
         if sync:
            update = -1

         tags, single, valid = type_check(tags)
         if not valid:
            raise TypeError, "iread(): 'tags' parameter must be a string or a list of strings"

         # Group exists
         if self._groups.has_key(group) and not rebuild:
            num_groups = self._groups[group]
            data_source = SOURCE_CACHE

         # Group non-existant
         else:
            if size:
               # Break-up tags into groups of 'size' tags
               tag_groups = [tags[i:i+size] for i in range(0, len(tags), size)]
            else:
               tag_groups = [tags]
               
            num_groups = len(tag_groups)
            data_source = SOURCE_DEVICE

         results = []

         for gid in range(num_groups):
            if gid > 0 and pause > 0: time.sleep(pause/1000.0)
            
            error_msgs = {}
            opc_groups = self._opc.OPCGroups
            opc_groups.DefaultGroupUpdateRate = update

            # Anonymous group
            if group == None:
               try:
                  if self.trace: self.trace('AddGroup()')
                  opc_group = opc_groups.Add()
               except pythoncom.com_error, err:
                  error_msg = 'AddGroup: %s' % self._get_error_str(err)
                  raise OPCError, error_msg
               sub_group = group
               new_group = True
            else:
               sub_group = '%s.%d' % (group, gid)

               # Existing named group
               try:
                  if self.trace: self.trace('GetOPCGroup(%s)' % sub_group)
                  opc_group = opc_groups.GetOPCGroup(sub_group)
                  new_group = False

               # New named group
               except:
                  try:
                     if self.trace: self.trace('AddGroup(%s)' % sub_group)
                     opc_group = opc_groups.Add(sub_group)
                  except pythoncom.com_error, err:
                     error_msg = 'AddGroup: %s' % self._get_error_str(err)
                     raise OPCError, error_msg
                  self._groups[str(group)] = len(tag_groups)
                  new_group = True
                  
            opc_items = opc_group.OPCItems

            if new_group:
               opc_group.IsSubscribed = 1
               opc_group.IsActive = 1
               if not sync:
                  if self.trace: self.trace('WithEvents(%s)' % opc_group.Name)
                  global current_client
                  current_client = self
                  self._group_hooks[opc_group.Name] = win32com.client.WithEvents(opc_group, GroupEvents)

               tags = tag_groups[gid]
               
               valid_tags, server_handles = add_items(tags)
               
               self._group_tags[sub_group] = tags
               self._group_valid_tags[sub_group] = valid_tags

            # Rebuild existing group
            elif rebuild:
               tags = tag_groups[gid]

               valid_tags = self._group_valid_tags[sub_group]
               add_tags = [t for t in tags if t not in valid_tags]
               del_tags = [t for t in valid_tags if t not in tags]

               if len(add_tags) > 0:
                  valid_tags, server_handles = add_items(add_tags)
                  valid_tags = self._group_valid_tags[sub_group] + valid_tags

               if len(del_tags) > 0:
                  remove_items(del_tags)
                  valid_tags = [t for t in valid_tags if t not in del_tags]

               self._group_tags[sub_group] = tags
               self._group_valid_tags[sub_group] = valid_tags
               
               if source == 'hybrid': data_source = SOURCE_DEVICE

            # Existing group
            else:
               tags = self._group_tags[sub_group]
               valid_tags = self._group_valid_tags[sub_group]
               if sync:
                  server_handles = [item.ServerHandle for item in opc_items]

            tag_value = {}
            tag_quality = {}
            tag_time = {}
            tag_error = {}
               
            # Sync Read
            if sync:   
               values = []
               errors = []
               qualities = []
               timestamps= []
               
               if len(valid_tags) > 0:
                   server_handles.insert(0,0)
                   
                   if source != 'hybrid':
                      data_source = SOURCE_CACHE if source == 'cache' else SOURCE_DEVICE

                   if self.trace: self.trace('SyncRead(%s)' % data_source)
                   
                   try:
                      values, errors, qualities, timestamps = opc_group.SyncRead(data_source, len(server_handles)-1, server_handles)
                   except pythoncom.com_error, err:
                      error_msg = 'SyncRead: %s' % self._get_error_str(err)
                      raise OPCError, error_msg

                   for i,tag in enumerate(valid_tags):
                      tag_value[tag] = values[i]
                      tag_quality[tag] = qualities[i]
                      tag_time[tag] = timestamps[i]
                      tag_error[tag] = errors[i]

            # Async Read
            else:
               if len(valid_tags) > 0:
                  if self._tx_id >= 0xFFFF:
                      self._tx_id = 0
                  self._tx_id += 1
      
                  if source != 'hybrid':
                     data_source = SOURCE_CACHE if source == 'cache' else SOURCE_DEVICE

                  if self.trace: self.trace('AsyncRefresh(%s)' % data_source)

                  try:
                     opc_group.AsyncRefresh(data_source, self._tx_id)
                  except pythoncom.com_error, err:
                     error_msg = 'AsyncRefresh: %s' % self._get_error_str(err)
                     raise OPCError, error_msg

                  tx_id = 0
                  start = time.time() * 1000
                  
                  while tx_id != self._tx_id:
                     now = time.time() * 1000
                     if now - start > timeout:
                        raise TimeoutError, 'Callback: Timeout waiting for data'

                     if self.callback_queue.empty():
                        pythoncom.PumpWaitingMessages()
                     else:
                        tx_id, handles, values, qualities, timestamps = self.callback_queue.get()
                                                
                  for i,h in enumerate(handles):
                     tag = self._group_handles_tag[sub_group][h]
                     tag_value[tag] = values[i]
                     tag_quality[tag] = qualities[i]
                     tag_time[tag] = timestamps[i]
            
            for tag in tags:
               if tag_value.has_key(tag):
                  if (not sync and len(valid_tags) > 0) or (sync and tag_error[tag] == 0):
                     value = tag_value[tag]
                     if type(value) == pywintypes.TimeType:
                        value = str(value)
                     quality = quality_str(tag_quality[tag])
                     timestamp = str(tag_time[tag])
                  else:
                     value = None
                     quality = 'Error'
                     timestamp = None
                  if include_error:
                     error_msgs[tag] = self._opc.GetErrorString(tag_error[tag]).strip('\r\n')
               else:
                  value = None
                  quality = 'Error'
                  timestamp = None
                  if include_error and not error_msgs.has_key(tag):
                     error_msgs[tag] = ''

               if single:
                  if include_error:
                     yield (value, quality, timestamp, error_msgs[tag])
                  else:
                     yield (value, quality, timestamp)
               else:
                  if include_error:
                     yield (tag, value, quality, timestamp, error_msgs[tag])
                  else:
                     yield (tag, value, quality, timestamp)

            if group == None:
               try:
                  if not sync and self._group_hooks.has_key(opc_group.Name):
                     if self.trace: self.trace('CloseEvents(%s)' % opc_group.Name)
                     self._group_hooks[opc_group.Name].close()

                  if self.trace: self.trace('RemoveGroup(%s)' % opc_group.Name)
                  opc_groups.Remove(opc_group.Name)

               except pythoncom.com_error, err:
                  error_msg = 'RemoveGroup: %s' % self._get_error_str(err)
                  raise OPCError, error_msg

      except pythoncom.com_error, err:
         error_msg = 'read: %s' % self._get_error_str(err)
         raise OPCError, error_msg

   def read(self, tags=None, group=None, size=None, pause=0, source='hybrid', update=-1, timeout=5000, sync=False, include_error=False, rebuild=False):
      """Return list of (value, quality, time) tuples for the specified tag(s)"""

      tags_list, single, valid = type_check(tags)
      if not valid:
         raise TypeError, "read(): 'tags' parameter must be a string or a list of strings"

      num_health_tags = len([t for t in tags_list if t[:1] == '@'])
      num_opc_tags = len([t for t in tags_list if t[:1] != '@'])

      if num_health_tags > 0:
         if num_opc_tags > 0:
            raise TypeError, "read(): system health and OPC tags cannot be included in the same group"
         results = self._read_health(tags)
      else:
         results = self.iread(tags, group, size, pause, source, update, timeout, sync, include_error, rebuild)

      if single:
         return list(results)[0]
      else:
         return list(results)

   def _read_health(self, tags):
      """Return values of special system health monitoring tags"""

      self._update_tx_time()
      tags, single, valid = type_check(tags)
      
      time_str = time.strftime('%x %H:%M:%S')
      results = []
      
      for t in tags:
         if   t == '@MemFree':      value = SystemHealth.mem_free()
         elif t == '@MemUsed':      value = SystemHealth.mem_used()
         elif t == '@MemTotal':     value = SystemHealth.mem_total()
         elif t == '@MemPercent':   value = SystemHealth.mem_percent()
         elif t == '@DiskFree':     value = SystemHealth.disk_free()
         elif t == '@SineWave':     value = SystemHealth.sine_wave()
         elif t == '@SawWave':      value = SystemHealth.saw_wave()

         elif t == '@CpuUsage':
            if self.cpu == None:
                self.cpu = SystemHealth.CPU()
                time.sleep(0.1)
            value = self.cpu.get_usage()
            
         else:
            value = None
         
            m = re.match('@TaskMem\((.*?)\)', t)
            if m:
               image_name = m.group(1)
               value = SystemHealth.task_mem(image_name)

            m = re.match('@TaskCpu\((.*?)\)', t)
            if m:
               image_name = m.group(1)
               value = SystemHealth.task_cpu(image_name)
               
            m = re.match('@TaskExists\((.*?)\)', t)
            if m:
               image_name = m.group(1)
               value = SystemHealth.task_exists(image_name)
               
         if value == None:
            quality = 'Error'
         else:
            quality = 'Good'
               
         if single:
            results.append((value, quality, time_str))
         else:
            results.append((t, value, quality, time_str))
    
      return results

   def iwrite(self, tag_value_pairs, size=None, pause=0, include_error=False):
      """Iterable version of write()"""

      try:
         self._update_tx_time()
         pythoncom.CoInitialize()

         def _valid_pair(p):
            if type(p) in (types.ListType, types.TupleType) and len(p) >= 2 and type(p[0]) in types.StringTypes:
               return True
            else:
               return False

         if type(tag_value_pairs) not in (types.ListType, types.TupleType):
            raise TypeError, "write(): 'tag_value_pairs' parameter must be a (tag, value) tuple or a list of (tag,value) tuples"

         if tag_value_pairs == None:
            tag_value_pairs = ['']
            single = False
         elif type(tag_value_pairs[0]) in types.StringTypes:
            tag_value_pairs = [tag_value_pairs]
            single = True
         else:
            single = False

         invalid_pairs = [p for p in tag_value_pairs if not _valid_pair(p)]
         if len(invalid_pairs) > 0:
            raise TypeError, "write(): 'tag_value_pairs' parameter must be a (tag, value) tuple or a list of (tag,value) tuples"
            
         names = [tag[0] for tag in tag_value_pairs]
         tags = [tag[0] for tag in tag_value_pairs]
         values = [tag[1] for tag in tag_value_pairs]

         # Break-up tags & values into groups of 'size' tags
         if size:
            name_groups = [names[i:i+size] for i in range(0, len(names), size)]
            tag_groups = [tags[i:i+size] for i in range(0, len(tags), size)]
            value_groups = [values[i:i+size] for i in range(0, len(values), size)]
         else:
            name_groups = [names]
            tag_groups = [tags]
            value_groups = [values]
            
         num_groups = len(tag_groups)

         status = []
                 
         for gid in range(num_groups):
            if gid > 0 and pause > 0: time.sleep(pause/1000.0)

            opc_groups = self._opc.OPCGroups
            opc_group = opc_groups.Add()
            opc_items = opc_group.OPCItems

            names = name_groups[gid]
            tags = tag_groups[gid]
            values = value_groups[gid]
            
            names.insert(0,0)
            errors = []
            
            try:
               errors = opc_items.Validate(len(names)-1, names)
            except:
               pass
               
            n = 1
            valid_tags = []
            valid_values = []
            client_handles = []
            error_msgs = {}
            
            for i, tag in enumerate(tags):
               if errors[i] == 0:
                  valid_tags.append(tag)
                  valid_values.append(values[i])
                  client_handles.append(n)
                  error_msgs[tag] = ''
                  n += 1
               elif include_error:
                  error_msgs[tag] = self._opc.GetErrorString(errors[i])

            client_handles.insert(0,0)
            valid_tags.insert(0,0)
            server_handles = []
            errors = []
       
            try:
               server_handles, errors = opc_items.AddItems(len(client_handles)-1, valid_tags, client_handles)
            except:
               pass
               
            valid_tags_tmp = []
            valid_values_tmp = []
            server_handles_tmp = []
            valid_tags.pop(0)
         
            for i, tag in enumerate(valid_tags):
               if errors[i] == 0:
                  valid_tags_tmp.append(tag)
                  valid_values_tmp.append(valid_values[i])
                  server_handles_tmp.append(server_handles[i])
                  error_msgs[tag] = ''
               elif include_error:
                  error_msgs[tag] = self._opc.GetErrorString(errors[i])
         
            valid_tags = valid_tags_tmp
            valid_values = valid_values_tmp
            server_handles = server_handles_tmp

            server_handles.insert(0,0)
            valid_values.insert(0,0)
            errors = []

            if len(valid_values) > 1:
               try:
                  errors = opc_group.SyncWrite(len(server_handles)-1, server_handles, valid_values)
               except:
                  pass

            n = 0
            for tag in tags:
               if tag in valid_tags:
                  if errors[n] == 0:
                     status = 'Success'
                  else:
                     status = 'Error'
                  if include_error:  error_msgs[tag] = self._opc.GetErrorString(errors[n])
                  n += 1
               else:
                  status = 'Error'

               # OPC servers often include newline and carriage return characters
               # in their error message strings, so remove any found.
               if include_error:  error_msgs[tag] = error_msgs[tag].strip('\r\n')

               if single:
                  if include_error:
                     yield (status, error_msgs[tag])
                  else:
                     yield status
               else:
                  if include_error:
                     yield (tag, status, error_msgs[tag])
                  else:
                     yield (tag, status)

            opc_groups.Remove(opc_group.Name)

      except pythoncom.com_error, err:
         error_msg = 'write: %s' % self._get_error_str(err)
         raise OPCError, error_msg

   def write(self, tag_value_pairs, size=None, pause=0, include_error=False):
      """Write list of (tag, value) pair(s) to the server"""

      if type(tag_value_pairs) in (types.ListType, types.TupleType) and type(tag_value_pairs[0]) in (types.ListType, types.TupleType):
         single = False
      else:
         single = True

      status = self.iwrite(tag_value_pairs, size, pause, include_error)

      if single:
         return list(status)[0]
      else:
         return list(status)

   def groups(self):
      """Return a list of active tag groups"""
      return self._groups.keys()

   def remove(self, groups):
      """Remove the specified tag group(s)"""

      try:
         pythoncom.CoInitialize()
         opc_groups = self._opc.OPCGroups

         if type(groups) in types.StringTypes:
            groups = [groups]
            single = True
         else:
            single = False
            
         status = []

         for group in groups:                
            if self._groups.has_key(group):
               for i in range(self._groups[group]):
                  sub_group = '%s.%d' % (group, i)

                  if self._group_hooks.has_key(sub_group):
                     if self.trace: self.trace('CloseEvents(%s)' % sub_group)
                     self._group_hooks[sub_group].close()
                  
                  try:
                     if self.trace: self.trace('RemoveGroup(%s)' % sub_group)
                     errors = opc_groups.Remove(sub_group)
                  except pythoncom.com_error, err:
                     error_msg = 'RemoveGroup: %s' % self._get_error_str(err)
                     raise OPCError, error_msg
                     
                  del(self._group_tags[sub_group])
                  del(self._group_valid_tags[sub_group])
                  del(self._group_handles_tag[sub_group])
                  del(self._group_server_handles[sub_group])
               del(self._groups[group])

      except pythoncom.com_error, err:
         error_msg = 'remove: %s' % self._get_error_str(err)
         raise OPCError, error_msg
      
   def iproperties(self, tags, id=None):
      """Iterable version of properties()"""

      try:
         self._update_tx_time()
         pythoncom.CoInitialize()

         tags, single_tag, valid = type_check(tags)
         if not valid:
            raise TypeError, "properties(): 'tags' parameter must be a string or a list of strings"

         try:
            id.remove(0)
            include_name = True
         except:
            include_name = False

         if id != None:
            descriptions= []
            
            if isinstance(id, list) or isinstance(id, tuple):
               property_id = list(id)
               single_property = False
            else:
               property_id = [id]
               single_property = True

            for i in property_id:
               descriptions.append('Property id %d' % i)
         else:
            single_property = False

         properties = []

         for tag in tags:

            if id == None:
               descriptions = []
               property_id = []
               count, property_id, descriptions, datatypes = self._opc.QueryAvailableProperties(tag)

               # Remove bogus negative property id (not sure why this sometimes happens)
               tag_properties = map(None, property_id, descriptions)
               property_id = [p for p, d in tag_properties if p > 0]
               descriptions = [d for p, d in tag_properties if p > 0]

            property_id.insert(0, 0)
            values = []
            errors = []
            values, errors = self._opc.GetItemProperties(tag, len(property_id)-1, property_id)
 
            property_id.pop(0)
            values = [str(v) if type(v) == pywintypes.TimeType else v for v in values]

            # Replace variant id with type strings
            try:
               i = property_id.index(1)
               values[i] = vt[values[i]]
            except:
               pass

            # Replace quality bits with quality strings
            try:
               i = property_id.index(3)
               values[i] = quality_str(values[i])
            except:
               pass

            # Replace access rights bits with strings
            try:
               i = property_id.index(5)
               values[i] = ACCESS_RIGHTS[values[i]]
            except:
               pass

            if id != None:
               if single_property:
                  if single_tag:
                     tag_properties = values
                  else:
                     tag_properties = [values]
               else:
                  tag_properties = map(None, property_id, values)
            else:
               tag_properties = map(None, property_id, descriptions, values)
               tag_properties.insert(0, (0, 'Item ID (virtual property)', tag))

            if include_name:    tag_properties.insert(0, (0, tag))
            if not single_tag:  tag_properties = [tuple([tag] + list(p)) for p in tag_properties]
            
            for p in tag_properties: yield p

      except pythoncom.com_error, err:
         error_msg = 'properties: %s' % self._get_error_str(err)
         raise OPCError, error_msg

   def properties(self, tags, id=None):
      """Return list of property tuples (id, name, value) for the specified tag(s) """

      if type(tags) not in (types.ListType, types.TupleType) and type(id) not in (types.NoneType, types.ListType, types.TupleType):
         single = True
      else:
         single = False

      props = self.iproperties(tags, id)

      if single:
         return list(props)[0]
      else:
         return list(props)

   def ilist(self, paths='*', recursive=False, flat=False, include_type=False):
      """Iterable version of list()"""

      try:
         self._update_tx_time()
         pythoncom.CoInitialize()
         
         try:
            browser = self._opc.CreateBrowser()
         # For OPC servers that don't support browsing
         except:
            return

         paths, single, valid = type_check(paths)
         if not valid:
            raise TypeError, "list(): 'paths' parameter must be a string or a list of strings"

         if len(paths) == 0: paths = ['*']
         nodes = {}

         for path in paths:
            
            if flat:
               browser.MoveToRoot()
               browser.Filter = ''
               browser.ShowLeafs(True)

               pattern = re.compile('^%s$' % wild2regex(path) , re.IGNORECASE)
               matches = filter(pattern.search, browser)
               if include_type:  matches = [(x, node_type) for x in matches]

               for node in matches: yield node
               continue
               
            queue = []
            queue.append(path)

            while len(queue) > 0:
               tag = queue.pop(0)
            
               browser.MoveToRoot()
               browser.Filter = ''
               pattern = None

               path_str = '/'
               path_list = tag.replace('.','/').split('/')
               path_list = [p for p in path_list if len(p) > 0]
               found_filter = False
               path_postfix = '/'

               for i, p in enumerate(path_list):
                  if found_filter:
                     path_postfix += p + '/'
                  elif p.find('*') >= 0:
                     pattern = re.compile('^%s$' % wild2regex(p) , re.IGNORECASE)
                     found_filter = True
                  elif len(p) != 0:
                     pattern = re.compile('^.*$')
                     browser.ShowBranches()

                     # Branch node, so move down
                     if len(browser) > 0:
                        try:
                           browser.MoveDown(p)
                           path_str += p + '/'
                        except:
                           if i < len(path_list)-1: return
                           pattern = re.compile('^%s$' % wild2regex(p) , re.IGNORECASE)

                     # Leaf node, so append all remaining path parts together
                     # to form a single search expression
                     else:
                        p = string.join(path_list[i:], '.')
                        pattern = re.compile('^%s$' % wild2regex(p) , re.IGNORECASE)
                        break
         
               browser.ShowBranches()

               if len(browser) == 0:
                  browser.ShowLeafs(False)
                  lowest_level = True
                  node_type = 'Leaf'
               else:
                  lowest_level = False
                  node_type = 'Branch'

               matches = filter(pattern.search, browser)
               
               if not lowest_level and recursive:
                  queue += [path_str + x + path_postfix for x in matches]
               else:
                  if lowest_level:  matches = [exceptional(browser.GetItemID,x)(x) for x in matches]
                  if include_type:  matches = [(x, node_type) for x in matches]
                  for node in matches:
                     if not nodes.has_key(node): yield node
                     nodes[node] = True

      except pythoncom.com_error, err:
         error_msg = 'list: %s' % self._get_error_str(err)
         raise OPCError, error_msg

   def list(self, paths='*', recursive=False, flat=False, include_type=False):
      """Return list of item nodes at specified path(s) (tree browser)"""

      nodes = self.ilist(paths, recursive, flat, include_type)
      return list(nodes)

   def servers(self, opc_host='localhost'):
      """Return list of available OPC servers"""
      
      try:
         pythoncom.CoInitialize()
         servers = self._opc.GetOPCServers(opc_host)
         servers = [s for s in servers if s != None]
         return servers

      except pythoncom.com_error, err:
         error_msg = 'servers: %s' % self._get_error_str(err)
         raise OPCError, error_msg

   def info(self):
      """Return list of (name, value) pairs about the OPC server"""

      try:
         self._update_tx_time()
         pythoncom.CoInitialize()

         info_list = []

         if self._open_serv:
            mode = 'OpenOPC'
         else:
            mode = 'DCOM'
         
         info_list += [('Protocol', mode)]

         if mode == 'OpenOPC':
            info_list += [('Gateway Host', '%s:%s' % (self._open_host, self._open_port))]
            info_list += [('Gateway Version', '%s' % __version__)]
         info_list += [('Class', self.opc_class)]
         info_list += [('Client Name', self._opc.ClientName)]
         info_list += [('OPC Host', self.opc_host)]
         info_list += [('OPC Server', self._opc.ServerName)]
         info_list += [('State', OPC_STATUS[self._opc.ServerState])]
         info_list += [('Version', '%d.%d (Build %d)' % (self._opc.MajorVersion, self._opc.MinorVersion, self._opc.BuildNumber))]

         try:
            browser = self._opc.CreateBrowser()
            browser_type = BROWSER_TYPE[browser.Organization]
         except:
            browser_type = 'Not Supported'

         info_list += [('Browser', browser_type)]
         info_list += [('Start Time', str(self._opc.StartTime))]
         info_list += [('Current Time', str(self._opc.CurrentTime))]
         info_list += [('Vendor', self._opc.VendorInfo)]

         return info_list

      except pythoncom.com_error, err:
         error_msg = 'info: %s' % self._get_error_str(err)
         raise OPCError, error_msg

   def ping(self):
      """Check if we are still talking to the OPC server"""
      try:
         # Convert OPC server time to milliseconds
         opc_serv_time = int(float(self._opc.CurrentTime) * 1000000.0)
         if opc_serv_time == self._prev_serv_time:
            return False
         else:
            self._prev_serv_time = opc_serv_time
            return True
      except pythoncom.com_error:
         return False
      
   def _get_error_str(self, err):
      """Return the error string for a OPC or COM error code"""

      hr, msg, exc, arg = err
            
      if exc == None:
         error_str = str(msg)
      else:
         scode = exc[5]

         try:
            opc_err_str = unicode(self._opc.GetErrorString(scode)).strip('\r\n')
         except:
            opc_err_str = None

         try:
            com_err_str = unicode(pythoncom.GetScodeString(scode)).strip('\r\n')
         except:
            com_err_str = None

         # OPC error codes and COM error codes are overlapping concepts,
         # so we combine them together into a single error message.
         
         if opc_err_str == None and com_err_str == None:
            error_str = str(scode)
         elif opc_err_str == com_err_str:
            error_str = opc_err_str
         elif opc_err_str == None:
            error_str = com_err_str
         elif com_err_str == None:
            error_str = opc_err_str
         else:
            error_str = '%s (%s)' % (opc_err_str, com_err_str)
                 
      return error_str

   def _update_tx_time(self):
      """Update the session's last transaction time in the Gateway Service"""
      if self._open_serv:
         self._open_serv._tx_times[self._open_guid] = time.time()

   def __getitem__(self, key):
      """Read single item (tag as dictionary key)"""
      value, quality, time = self.read(key)
      return value
      
   def __setitem__(self, key, value):
      """Write single item (tag as dictionary key)"""
      self.write((key, value))
      return

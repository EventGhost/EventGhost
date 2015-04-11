# -*- coding: utf-8 -*-
#
# plugins/RWE_SmartHome/__init__.py
#
# Copyright (c) 2015, Heiko Steinwender
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of Heiko Steinwender nor the names of its contributors may
#    be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import requests
import uuid
import xml.etree.ElementTree as ET # https://docs.python.org/3.1/library/xml.etree.elementtree.html
import inspect
import hashlib
import base64
import os


class shc(object):

	class text:
		namespace_xsi_uri = 'http://www.w3.org/2001/XMLSchema-instance'
		namespace_xsi_prefix = 'xsi'
		xsi_type = '{'+namespace_xsi_uri+'}type'
		namespace_xsd_uri = 'http://www.w3.org/2001/XMLSchema'
		namespace_xsd_prefix = 'xsd'
		xsd_type = '{'+namespace_xsd_uri+'}type'
		PluginPrefix = 'RWE_SHC'

	class SHC_device():
		class text:
			joiner = '/'

		def __init__(self, name='', room='', type='', state=''):
			self.name = name.replace(self.text.joiner, '')
			self.room = room.replace(self.text.joiner, '')
			self.type = type.replace(self.text.joiner, '')
			self.state = state

		def GetName(self):
			return self.name

		def GetLongName(self):
			return self.room + self.text.joiner + self.name

		def GetFullName(self):
			return self.type + self.text.joiner + self.GetLongName()


	def __init__(self, hostname, username, password, bDeviceEvents = True):
		self.debug = True
		self.hostname = hostname
		self.username = username
		self.password = password
		self.bDeviceEvents = bDeviceEvents
		self.SmartHomeRequestid = str(uuid.uuid1())
		self.clientid = str(uuid.uuid1())
		self.version = '1.70'
		self.sessionid = None
		self.confversion = None
		self.notificationid = None
		self.rooms = {} # LC
		self.devices = {} # LD

		# Test ic PW is encoded
		try:
			base64.b64decode(self.password)
		except:
			self.password = base64.b64encode((hashlib.sha256(self.password).digest()))

		# RWE Smart Home Center NS
#			ET.register_namespace(self.text.namespace_xsi_prefix, self.text.namespace_xsi_uri)
#			ET.register_namespace(self.text.namespace_xsd_prefix, self.text.namespace_xsd_uri)
			ET._namespace_map[self.text.namespace_xsi_uri] = self.text.namespace_xsi_prefix
			ET._namespace_map[self.text.namespace_xsd_uri] = self.text.namespace_xsd_prefix

	def LoginRequest(self):
		self.PrintInfo()
		self.sessionid = None
		XML_Tree = self.SmartHomeRequest(ET.tostring(self.BaseRequest(	'LoginRequest', **{
																		'UserName'  : self.username,
																		'Password'  : self.password})),
										bCheckCfg=False)
		if XML_Tree:
			try:
				if XML_Tree.attrib.get (self.text.xsi_type,None) == 'LoginResponse':
					self.sessionid = XML_Tree.attrib.get('SessionId',None)
					if self.sessionid:
						self.PrintInfo ('login successful')
						return
					else:
						self.PrintError( 'ERROR: login')
						print ( ET.tostring(XML_Tree))
						return
				else:
					self.PrintError( 'ERROR: https BaseRequest')
			except:
					self.PrintError( 'ERROR: response Error')
					print ( ET.tostring(XML_Tree))
		else:
			self.PrintError( 'ERROR: No Tree', str(XML_Tree))


	def GetEntitiesRequest(self):
		self.PrintInfo()
		if not self.IsConnected(): return
		BaseRequest = self.BaseRequest ('GetEntitiesRequest')
		# Configuration only
		child = ET.SubElement(BaseRequest, 'EntityType')
		child.text = 'Configuration'
		return self.SmartHomeRequest(ET.tostring(BaseRequest),bCheckCfg=False)

	def GetAllPhysicalDeviceStatesRequest(self):
		self.PrintInfo()
		if not self.IsConnected(): return
		return self.SmartHomeRequest(ET.tostring(self.BaseRequest ('GetAllPhysicalDeviceStatesRequest')))

	def NotificationRequest (self, SetNotificationType=''):
		if not SetNotificationType in [	'Calibration',
										'ConfigurationChanges',
										'CustomApplication',
										'DeploymentChanges',
										'DeviceStateChanges',
										'MessageUpdate' ]: SetNotificationType = 'DeviceStateChanges'
		if not self.IsConnected(): return
		self.PrintInfo()
		BaseRequest = 	self.BaseRequest( 'NotificationRequest')
		Action = ET.SubElement(BaseRequest, 'Action')
		Action.text = 'Subscribe'
		NotificationType = ET.SubElement(BaseRequest, 'NotificationType')
		NotificationType.text = SetNotificationType
		return self.SmartHomeRequest(ET.tostring(BaseRequest))

	def GetNotifications (self):
		#self.PrintInfo()
		if self.sessionid:
			XML_Tree = self.SmartHomeRequest('upd','upd')
			if XML_Tree.tag == 'NotificationList':
				return XML_Tree
			self.PrintError (XML_Tree.tag)
		return {}

###################################################### Action Functions


	def SwitchActuatorState(self, SetLogicalDeviceId, state='off'):
		self.PrintInfo()
		if not self.IsConnected(): return
		if SetLogicalDeviceId:
			BaseRequest = 	self.BaseRequest( 'SetActuatorStatesRequest')
			BaseRequest = 	self.BaseRequest( 'SetActuatorStatesRequest')
			ActuatorStates = ET.SubElement(BaseRequest, 'ActuatorStates')
			LogicalDeviceState = ET.SubElement(ActuatorStates, 'LogicalDeviceState', **{
																'xsi:type':'SwitchActuatorState',
																'LID':SetLogicalDeviceId,
																'IsOn':{'on':'true', 'off':'false'}.get(state.lower(),'false')
																})
			XML_Tree = self.SmartHomeRequest(ET.tostring(BaseRequest))
			#print ET.tostring(XML_Tree)
			try:
				result = XML_Tree.attrib.get('Result','unknown')
				if result.lower() == 'ok':
					return True
				else:
					self.PrintError (result)
					if result.lower() == 'configurationoutofdate': self.confversion = None
					return False
			except:
				pass
			self.PrintError('ERROR')
		return False

	def GenericDeviceState(self, SetLogicalDeviceId, state='off', type="boolean"):
		self.PrintInfo()
		if not self.IsConnected(): return
		if SetLogicalDeviceId:
			BaseRequest = 	self.BaseRequest( 'SetActuatorStatesRequest')
			BaseRequest = 	self.BaseRequest( 'SetActuatorStatesRequest')
			ActuatorStates = ET.SubElement(BaseRequest, 'ActuatorStates')
			LogicalDeviceState = ET.SubElement(ActuatorStates, 'LogicalDeviceState', **{
																'xsi:type':'GenericDeviceState',
																'LID':SetLogicalDeviceId
																})
			Ppts = ET.SubElement(LogicalDeviceState, 'Ppts')
			Ppt  = ET.SubElement(Ppts  ,	'Ppt', **{
											'xsi:type':'BooleanProperty',
											'Name':'Value',
											'Value':{'on':'true', 'off':'false'}.get(state.lower(),'false')
											})
			XML_Tree = self.SmartHomeRequest(ET.tostring(BaseRequest))
			try:
				result = XML_Tree.attrib.get('Result','unknown')
				if result.lower() == 'ok':
					return True
				else:
					self.PrintError (result)
					if result.lower() == 'configurationoutofdate': self.confversion = None
					return False
			except:
				pass
			self.PrintError('ERROR')
		return False

###################################################### Base Functions

	def BaseRequest (self, RequestType,  *args, **kwargs):
			XML_Tree =	ET.Element	(	'BaseRequest',**dict({
									'xsi:type'  : RequestType,
									'xmlns:xsi' : self.text.namespace_xsi_uri,
									'xmlns:xsd' : self.text.namespace_xsd_uri,
									'RequestId' : str(uuid.uuid1())},
									**kwargs))
			if self.sessionid:		XML_Tree.set('SessionId', self.sessionid)
			if self.version:		XML_Tree.set('Version', self.version)
			if self.confversion:	XML_Tree.set('BasedOnConfigVersion', self.confversion)

			#print ET.tostring (XML_Tree)
			return XML_Tree

	def SmartHomeRequest(self, command_string, page='cmd',bCheckCfg=True): # Base request function
		#self.PrintInfo()
		url_string = 'https://'+self.hostname+'/'+page
#		url_string = 'http://smarthome.store.local/cmd.php'

		# params={'file': filepath}
		# auth=(self.username, self.password)
		if bCheckCfg: self.GetConfiguration()

		try:
			XML_Tree = ET.fromstring( requests.post (	url=url_string,
										headers={	'Host' : self.hostname,
													'Referer' : 'https://smarthome.blob.core.windows.net/silverlight/latest/application/RWE.SmartHome.UI.Shell.xap?ignore=1.70.365.0',
													'ClientId' : self.clientid ,
													'Proxy-Connection' : 'keep-alive',
													'Accept-Encoding' : 'identity',
													'Content-Type' : 'text/xml',
													'Content-Length' : str(len(command_string)),
													'Connection' : 'keep-alive',
													'Accept' : '*/*',
													'Accept-Language' : 'de-de'
											},
										data=command_string,
										verify=False,
										timeout=5,
									).text.encode('utf-8'))
			if bCheckCfg: self.GetConfiguration(XML_Tree)
			return XML_Tree
		except:
			self.PrintError( 'ERROR: https request')
			return None

###################################################### Suport Functions

	def GetRoomNameByID (self,search_room, default=True ):
		return self.rooms.get( search_room, 'noROOM' if default else None )

	def GetDeviceNameByID (self, search_id, default=True):
		try:
			return self.devices[search_id].GetName()
		except:
			return ( search_id if default else '' )
		#return self.devices.get( search_id, search_id if default else None )

	def GetDeviceLongNameByID (self, search_id, default=True):
		try:
			return self.devices[search_id].GetLongName()
		except:
			return ( search_id if default else '' )
		#return self.devices.get( search_id, search_id if default else None )

	def GetDeviceFullNameByID (self, search_id, default=True):
		try:
			return self.devices[search_id].GetFullName()
		except:
			return ( search_id if default else '' )
		#return self.devices.get( search_id, search_id if default else None )

	def IsConnected(self):
		if self.sessionid: return True
		self.LoginRequest()
		if self.sessionid:
			if self.bDeviceEvents: self.NotificationRequest()
			self.NotificationRequest('ConfigurationChanges')
			return True
		return False

	def GetConfiguration(self, XML_Tree=None):
		if not self.IsConnected(): return

		if XML_Tree:
			confversion = XML_Tree.attrib.get('CurrentConfigurationVersion', XML_Tree.attrib.get('ConfigurationVersion',None))
			if not confversion or confversion==self.confversion: return
		else:
			if self.confversion: return
		#self.PrintInfo()
		XML_Tree = self.GetEntitiesRequest()
		if XML_Tree:
			#self.confversion=XML_Tree.attrib.get('CurrentConfigurationVersion', None)
			self.confversion=XML_Tree.attrib.get('ConfigurationVersion', None)
			#self.PrintInfo (self.confversion)
			#print ET.tostring(XML_Tree)
			#print ET.tostring(XML_Tree, encoding='utf8')
			self.PrintInfo('loading rooms...')
			self.rooms = {} # ROOMS
			for item in XML_Tree.findall('./LCs/LC/'):
				try:
					self.rooms[item.find('Id').text] = item.find('Name').text.replace(' ','').replace('.','')
				except:
					pass
			self.devices = {}
			self.PrintInfo('loading devices...')
			for item in XML_Tree.findall('./LDs/LD/'):
				self.devices[item.find('Id').text] = self.SHC_device(
															room=self.rooms.get(item.attrib.get('LCID',None),'noROOM'),
															name=item.attrib.get('Name','noNAME'),
															type=item.attrib.get(self.text.xsi_type, 'noTYPE')
														)
				try:
					self.devices[item.find('Id').text] = self.SHC_device(
																room=self.rooms.get(item.attrib.get('LCID',None),'noROOM'),
																name=item.attrib.get('Name','noNAME'),
																type=item.attrib.get(self.text.xsi_type, 'noTYPE')
															)
				except:
					pass
			self.PrintInfo('done.')
		else:
			self.PrintError('no configuration avaylable')

	def GetEvents(self):
		#self.PrintInfo()
		if not self.IsConnected(): return
		XML_Tree = self.GetNotifications()
		egEvent=[]
		if XML_Tree: # and self.notificationid != XML_Tree.attrib.get('NotificationListId',None):
			#print (ET.tostring(XML_Tree).replace("\n",''))
			self.notificationid = XML_Tree.attrib.get('NotificationListId',None)
			if XML_Tree.findall('./Notifications/LogoutNotification/'):
				self.sessionid = None
				return egEvent
			if XML_Tree.findall('./Notifications/ConfigurationChangedNotification/'):
				self.confversion = None
			for XML_State in XML_Tree.findall('./Notifications/LogicalDeviceStatesChangedNotification/LogicalDeviceStates/LogicalDeviceState/'):
				#print ET.tostring(XML_State, encoding='utf8')
				LID = XML_State.attrib.get('LID', None)
				if LID:
					type = XML_State.attrib.get (self.text.xsi_type,None)
					if type in [	'SwitchActuatorState',
									'RoomHumiditySensorState',
									'GenericDeviceState',
									'WindowDoorSensorState',
									'LuminanceSensorState',
									'RoomTemperatureActuatorState',
									'RoomTemperatureSensorState']:
						event = getattr(self,'_Get'+type)(XML_State)
						event_joined = type + '.[' + self.GetDeviceLongNameByID(LID) + ']'
						if  event.get('state',None):
							event_joined +=  ': ' + event['state']
						egEvent.append([event_joined, event.get('payload',None)])
					else:
						self.PrintInfo('Missing type ('+type+'):'+ET.tostring(XML_State, encoding='utf8').replace("\n",''))
		else:
			self.sessionid = None
			self.PrintError('No request response')
		return egEvent

	def _GetSwitchActuatorState(self, XML_Tree):
		#self.WriteInfo(ET.tostring(XML_Tree),filename=inspect.stack()[2][3]+'.xlm')
		state = XML_Tree.attrib.get('IsOn',None)
		if state: return {'state':{'true':'on','false':'off'}.get(state.lower(), 'unknown')}
		self.PrintError (ET.tostring(XML_Tree, encoding='utf8'))
		return {'state':'error'}

	def _GetWindowDoorSensorState(self, XML_Tree):
		state = XML_Tree.findtext('IsOpen')
		if state: return {'state':{'true':'open','false':'closed'}.get(state.lower(), 'unknown')}
		self.PrintError (ET.tostring(XML_Tree, encoding='utf8'))
		return {'state':'error'}

	def _GetRoomTemperatureActuatorState(self, XML_Tree):
		payload = XML_Tree.attrib.get ('PtTmp','')
		if payload: return {'payload':payload}
		self.PrintError (ET.tostring(XML_Tree, encoding='utf8'))
		return {'payload':'error'}

	def _GetRoomTemperatureSensorState(self, XML_Tree):
		payload = XML_Tree.attrib.get ('Temperature','')
		if payload: return {'payload':payload}
		self.PrintError (ET.tostring(XML_Tree, encoding='utf8'))
		return {'payload':'error'}

	def _GetRoomHumiditySensorState(self, XML_Tree):
		payload = XML_Tree.attrib.get ('Humidity',None)
		if payload: return {'payload':payload}
		self.PrintError (ET.tostring(XML_Tree, encoding='utf8'))
		return {'payload':'error'}

	def _GetLuminanceSensorState(self, XML_Tree):
		payload = XML_Tree.findtext('Luminance')
		if payload: return {'payload':payload}
		self.PrintError (ET.tostring(XML_Tree, encoding='utf8'))
		return {'payload':'error'}

	def _GetGenericDeviceState(self, XML_Tree):
		device = XML_Tree.findall('Ppts/Ppt/')
		if device:
			try:
				if isinstance(device, list): device = device[0]
				value_name = device.attrib.get('Name')
				value = device.attrib.get (value_name,'Name')
				if device.attrib.get(self.text.xsi_type, 'noTYPE') == 'BooleanProperty':
					if value: return {'state':{'true':'on','false':'off'}.get(value.lower(), 'unknown')}
				else:
					if value: return {'payload':value}
			except:
				pass
		self.PrintError (ET.tostring(XML_Tree, encoding='utf8'))
		return {'state':'error'}

		###################################################### Helper Functions

	def IsUUID (self, uuid):
		try:
			int (uuid.replace('-',''),16)
			return True
		except:
			return False

	def PrintInfo(self, comment=''):
		if comment:
			comment = ': '+str(comment)
		if self.debug:
			comment = '.'+inspect.stack()[1][3]+str(comment)
		else:
			if not comment: return
		print (self.text.PluginPrefix+comment)

	def PrintError(self, comment=''):
		if comment: comment = '.'+ str(comment)
		if self.debug:
			comment = '.'+inspect.stack()[1][3]+str(comment)
		eg.PrintError (self.text.PluginPrefix+str(comment))

	def WriteInfo (self, info='', filename = __file__  + '.xml'):
		#XMLFile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dump.xml'))
		#http://www.freeformatter.com/xml-formatter.html#ad-output
		#icoFile = filename
		stream = open(filename, 'w')
		stream.write(info)
		stream.close()

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
##############################################################################
# Revision history:
#
# 2015-03-30  First Version
##############################################################################
#
# $LastChangedDate: 2015-02-07 20:13:27 +0100 (Sa, 07 Feb 2009) $
# $LastChangedRevision: 831 $
# $LastChangedBy: lms0815 $

eg.RegisterPlugin(
	name = 'RWE SmartHome',
	guid = '{f418c7e7-3d1c-4d5d-bd67-8ced72401c53}',
	author = 'Heiko Steinwender',
	version = '0.1.1.' + '$LastChangedRevision: 831 $'.split()[1],
    kind = 'external',
	#kind = 'program',
	canMultiLoad = True,
	createMacrosOnAdd = True,
	url = 'http://www.eventghost.net/forum/viewtopic.php?f=9&t=2115',
	description = (
		u'<p>Plugin to control '
		u'<a href="http://www.rwe-smarthome.de/">RWE SmartHome</a></p>'
		u'<center><img src="RWESmartHome.jpg" /></center>'
	),
	help = """
			<b>Home automation with RWE SmartHome</b>
			<br/><br/>
			The convenient solution for your home<br/>
			Customised home automation is no longer a pipe-dream or an unaffordable luxury
			&#45 thanks to RWE SmartHome,
			the user-friendly home automation system for every home,
			which delivers contemporary home automation of electrical devices and heating.
		""",
	icon = (
		'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAFo9M/3AAAABmJLR0QA/wD/AP+g'
		'vaeTAAAAB3RJTUUH3wQECAUIKOEYAgAABClJREFUOBEBHgTh+wPC3O3/K0lbBQMR'
		'N1MFCQtKewGiyN3d6u/0pwDM47X/6vb9/wGXv9jdCwkKIk0xHQDs9foAAqzJ4ac2'
		'IRIA7fP4APz7+gABqMrf/+Tt8oUAAAAA1OLv9ADp9vz/cq7U/wBorP/q9/3/BP//'
		'/wAWC0MAg071AP//UQAB1Ofz////7ADz+eQADggwAACuzuL/2+/6/97x+v/m9vz/'
		'Z6DM/97w+v/c8Pr/3fD7/wLS4euFbZjAAAYCAQAHAgMANiZ8AAoFAgBTjLsACwYD'
		'AATd6fUAo3BDAAMBAACVvg0ABAMKAAYCAAC+e0gAAAIAAAS60+b0tdLkAAQCAgAj'
		'FtcAAQAAALjV5wD9/v8A6PD4AAGVwNv/FQsEAOjv88L6/f/DAAAAAAAAAAABAAAB'
		'c0kvfQHd8Pv//wD/AAIBAACBqs4AiVs1APv+/wD4+/4AoLC9mQINBwIAFQoFACJy'
		'sACRXzcAgbLUAB15tgAOBwIA+v3+AADp9/7/NoC3/+j1/P+Ywzz/7Pf//+Hx+v9T'
		'j7//cJizmAHp9v3/AgAAAJjADwAFAwsAAAAAAEgspQAYED8Ae5u0mQIEAwEAAgEA'
		'AGY/5QD/AP4A+v3zAB4TQQADAgIA7vX6AATn7vUAAwIAAOz0zABVM+IA9PniAOvy'
		'9wD7/f8A6fL4AAS31OcAGA8IAAMCJgDk7+wA/wAKAP//7wD7/v8A2uXu9QGXwNr/'
		'RjEgAPz+AQABAQAAAAAAAAEAAAD/AQAABAICAP///wD9//8AAQAAAP//AAAAAAAA'
		'//8AAAQCAAB2l7CHBAoEAQAGAgMABQH/AAIBAAACAQEA7/f7AEmWxQAUCQUA+Pz+'
		'APv/AAC9bjwAYZ/LAJteMwAEAwIAAgIBACUVCxIC1ePtwgwGAQAJBQEAcaLIABpu'
		'qgDj7fMAzHZAAJpa+QCmYAUAxnI9AM/g7QC/0uEAfanNAAsHAgAMBQEA+v3+AAQE'
		'AwPD+P3/PgIAAACaZTsAhFbWAO71vgDH284A1eWaAP8A/wAvHW8AFg0rANiILwAV'
		'DSgA+v7+APr/AAD4+v0AAu71+gAEAQAAAP8AAPz9/QAUDCkACgYWANTlmgACAgYA'
		'AwIHANLkkwAPCR8AEwsnAPz9/QAB/gAABAEAAPH2+wAC5/H4AAUDAQAEAgAAAwEB'
		'AAIB/wAEAgQA/v/7ADUgdQAyHm4A+/33AAUCBQACAv8AAwEBAAMCAAAFAwEA6vP5'
		'AATn7/cBvtbnAAIBAQAEAgEAAgIAAAIBJQA0H9IA/P0IAAAA/wA2IFoA3esJANvq'
		'6wD+/v8A/P7/AP7//wDq8vgAAQAAAAIOXJOECAICEv8AAAAAAP8AAAAAAAAAAAAA'
		'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAQABAAAA9/r49fOoc4HeS5o151U92wAAAABJ'
		'RU5ErkJggg=='
		),
)

import eg, wx
import hashlib
import base64

from RWESmartHome import shc
from threading import Event, Thread


class RWESmartHome(eg.PluginClass):

	class text:
		infoStartup = 'plugin started'
		infoStopped  = 'plugin stopped'
		infoClosed  = 'plugin closed'
		infoStatus  = 'not yet started'
		infoNoDevice = 'device was not found'
		infoDevice  = 'Device found'
		infoStartThread  = 'monitor thread is started'
		infoStopThread  = 'monitor thread has stopped'
		infoEvent  = 'unknown event'

		devicename = 'Squeezebox device name: '
		hostname = 'RWE SmartHomeCenter IP-address or host name: '
		username = 'User name (leave empty if not defined): '
		password = 'Password (leave empty if not defined): '

		infobDeviceEvents = 'Check to log device events'
		PluginPrefix = 'RWE_SHC'



	def __init__(self):
		self.trackpath = ''
		self.IsPowerOn = False
		self.TrackTime = 0
		self.bFound = False
		self.RWE_SHC = None
		self.RWE_SHC_IsConnected = False
		self.iDelay = 0.2
		self.bToggleS = True
		self.bToggleF = True
		#self.AddAction(SwitchActuatorOn)
		#self.AddAction(SwitchActuatorOff)
		#self.AddAction(GenericActuatorOn)
		#self.AddAction(GenericActuatorOff)

		#					self.SwitchActuatorState('21d1cc85-45ff-486e-a94b-7461e38bf4d7','off')


		group1 = self.AddGroup('Switch Actuatos','Switch Actuator on/off')
		group1.AddAction(SwitchActuatorOn)
		group1.AddAction(SwitchActuatorOff)

		group2 = self.AddGroup('Generic Devices','Switch Generic Device on/off')
		group2.AddAction(GenericActuatorOn)
		group2.AddAction(GenericActuatorOff)

############################################################

	def __start__(
			self,
			devicename ,
			hostname,
			username,
			password,
			bDeviceEvents
			):
		self.devicename = devicename
		self.hostname = hostname
		self.username = username
		self.password = password
		self.bDeviceEvents = bDeviceEvents
		self.bInit = True
		self.sq = None
		self.wifi = 0

		self.stopThreadEvent = Event()
		thread = Thread(
			target=self.ThreadWorker,
			args=(self.stopThreadEvent,)
		)
		thread.start()
		print( "%s.%s" % ( self.text.PluginPrefix,self.text.infoStartup))


	def __stop__(self):
		if self.stopThreadEvent:
			self.stopThreadEvent.set()
			print( "%s.%s" % ( self.text.PluginPrefix,self.text.infoStopped))

	def __close__(self):
		print( "%s.%s" % ( self.text.PluginPrefix,self.text.infoClosed))

	def ThreadWorker(self, stopThreadEvent):
		while not stopThreadEvent.isSet():
			stopThreadEvent.wait(self.iDelay)
			if self.RWE_SHC_IsConnected:
				for SHC_Event in self.RWE_SHC.GetEvents():
					#eg.TriggerEvent(self, suffix, payload=None, prefix='Main', source=<dynamic-module 'eg')
					#self.TriggerEvent(self, suffix, payload=None)
					self.TriggerEvent(	SHC_Event[0],payload=SHC_Event[1])
			else:
				if self.bInit:
					self.bInit = False
				else:
					self.PrintError( "%s.%s" % (self.text.PluginPrefix,self.text.infoStopThread))
				self.createRWE_SHC_IsConnected()

	def createRWE_SHC_IsConnected(self):
		try:
			self.RWE_SHC = shc(
					hostname=str(self.hostname),
					username=str(self.username),
					password=str(self.password),
					bDeviceEvents=self.bDeviceEvents
			)

			self.RWE_SHC_IsConnected = self.RWE_SHC.IsConnected()

		except ValueError:
			self.iDelay = 10.0
			self.PrintError( "%s.login.failed" %  self.text.PluginPrefix)
			self.RWE_SHC_IsConnected = False

	def Configure(
					self,
					devicename = 'enter name of device to control',
					hostname = '',
					username = '',
					password = '',
					bDeviceEvents = True,
					*args
					):
		panel = eg.ConfigPanel(self, resizable=True)
		mySizer = wx.GridBagSizer(5, 5)

		devicenameCtrl = wx.TextCtrl(panel, -1, devicename )
		devicenameCtrl.SetInitialSize((250,-1))
		mySizer.Add(wx.StaticText(panel, -1, self.text.devicename ), (1,0))
		mySizer.Add(devicenameCtrl, (1,1))

		hostnameCtrl = wx.TextCtrl(panel, -1, hostname)
		hostnameCtrl.SetInitialSize((250,-1))
		mySizer.Add(wx.StaticText(panel, -1, self.text.hostname), (2,0))
		mySizer.Add(hostnameCtrl, (2,1))

		usernameCtrl = wx.TextCtrl(panel, -1, username)
		usernameCtrl.SetInitialSize((250,-1))
		mySizer.Add(wx.StaticText(panel, -1, self.text.username), (4,0))
		mySizer.Add(usernameCtrl, (4,1))

		passwordCtrl = wx.TextCtrl(panel, -1, password)
		passwordCtrl.SetInitialSize((250,-1))
		mySizer.Add(wx.StaticText(panel, -1, self.text.password), (5,0))
		mySizer.Add(passwordCtrl, (5,1))

		bDeviceEventsCtrl = wx.CheckBox(panel, -1, '')
		bDeviceEventsCtrl.SetValue(bDeviceEvents)
		mySizer.Add(wx.StaticText(panel, -1, self.text.infobDeviceEvents),(6,0))
		mySizer.Add(bDeviceEventsCtrl, (6,1))

		panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

		while panel.Affirmed():
			devicename = devicenameCtrl.GetValue()
			hostname = hostnameCtrl.GetValue()
			username = usernameCtrl.GetValue()

			password = passwordCtrl.GetValue()
			try:
				base64.b64decode(password)
			except:
				password = base64.b64encode((hashlib.sha256(password).digest()))
			bDeviceEvents = bDeviceEventsCtrl.GetValue()

			panel.SetResult(
						devicename,
						hostname,
						username,
						password,
						bDeviceEvents,
						*args
			)

	# Get the choice from dropdown and perform some action
	def OnDeviceChoice(self, event):
		choice = event.GetSelection()
		event.Skip()
		return choice

	# Input Single Line Action
	def GetConfigureFreetext(self, myString=''):
		panel = eg.ConfigPanel(self, resizable=False)
		mySizer = wx.GridBagSizer(5, 5)

		if myString == '':
			myString = self.devicename
		devicenameCtrl = wx.TextCtrl(panel, -1, myString )
		devicenameCtrl.SetInitialSize((250,-1))
		mySizer.Add(wx.StaticText(panel, -1, self.text.devicename ), (1,0))
		mySizer.Add(devicenameCtrl, (1,1))
		panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

		while panel.Affirmed():
			panel.SetResult(devicenameCtrl.GetValue())
		return myString

	def GetConfigure(self, devicename='',deviceid='',type='SwitchActuator'):
		panel = eg.ConfigPanel(self , resizable=False)

		#print	list(self.RWE_SHC.devices.values())	
		# Create a combo for device selections and inputs
		deviceCtrl = wx.ComboBox(parent=panel, pos=(10,10))
		
		names = []
		myids = []
		try:
			actuators = []
			for key, value in self.RWE_SHC.devices.iteritems():
				#for id, item in self.RWE_SHC.devices:
				if value.type == type:
					actuators.append([	value.GetLongName(),
										key])
			actuators.sort (key=lambda x:x[0])
			for name, device in actuators:
				names.append(name)
				myids.append(device)
		except:
			self.RWE_SHC.PrintInfo('configuration currently not loaded')
			pass
		deviceCtrl.AppendItems(strings=names)
		try:
			idx = myids.index(deviceid)
			deviceCtrl.Select(n=idx)
		except:
			deviceCtrl.Select(n=0)
		deviceCtrl.Bind(wx.EVT_CHOICE, self.OnDeviceChoice)

		staticBox = wx.StaticBox(panel, -1, self.text.devicename )
		staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		sizer1 = wx.BoxSizer(wx.HORIZONTAL)
		sizer1.Add(deviceCtrl, 1, wx.EXPAND)
		staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
		panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

		while panel.Affirmed():
			devicename = deviceCtrl.GetValue()
			try:
				deviceid = myids[names.index(devicename)]
			except:
				deviceid = ''
			panel.SetResult(devicename,deviceid)

class SwitchActuatorOn(eg.ActionClass):
	name = 'SwitchActuator [on]'
	description = 'Set Switch Actuator on'
	def __call__(self, devicename,deviceid):
		if self.plugin.RWE_SHC_IsConnected:
			return self.plugin.RWE_SHC.SwitchActuatorState(str(deviceid),'on')
		else:
			self.plugin.RWE_SHC.PrintInfo (self.plugin.text.infoStatus)
		return False

	def Configure(self, devicename='',deviceid=''):
		self.plugin.GetConfigure (devicename,deviceid,'SwitchActuator')

class SwitchActuatorOff(eg.ActionClass):
	name = 'SwitchActuator [off]'
	description = 'Set Switch Actuator off'
	def __call__(self, devicename,deviceid):
		if self.plugin.RWE_SHC_IsConnected:
			return self.plugin.RWE_SHC.SwitchActuatorState(str(deviceid),'off')
		else:
			self.plugin.RWE_SHC.PrintInfo (self.plugin.text.infoStatus)
		return False

	def Configure(self, devicename='',deviceid=''):
		self.plugin.GetConfigure (devicename,deviceid,'SwitchActuator')

class GenericActuatorOn(eg.ActionClass):
	name = 'GenericActuator [on]'
	description = 'Set Generic Actuator on'
	def __call__(self, devicename,deviceid):
		if self.plugin.RWE_SHC_IsConnected:
			return self.plugin.RWE_SHC.GenericDeviceState(str(deviceid),'on')
		else:
			self.plugin.RWE_SHC.PrintInfo (self.plugin.text.infoStatus)
		return False

	def Configure(self, devicename='',deviceid=''):
		self.plugin.GetConfigure (devicename,deviceid,'GenericActuator')

class GenericActuatorOff(eg.ActionClass):
	name = 'GenericActuator [off]'
	description = 'Set Generic Actuator off'
	def __call__(self, devicename,deviceid):
		if self.plugin.RWE_SHC_IsConnected:
			return self.plugin.RWE_SHC.GenericDeviceState(str(deviceid),'off')
		else:
			self.plugin.RWE_SHC.PrintInfo (self.plugin.text.infoStatus)
		return False

	def Configure(self, devicename='',deviceid=''):
		self.plugin.GetConfigure (devicename,deviceid,'GenericActuator')


# This file is part of EventGhost.
# plugins/Ping/__init__.py
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
Rev History :
0.0.2 : 
	- The plugin now uses a pure python ping implementation. the windows ping.exe isn't used anymore
		- All the threads can now be interrupted immediately (in 0.0.1, the code should wait for running ping.exe to end).
		- The plugin should consume far less cpu time.
		- The plugin param is no more needed ... unfortunatly, this breaks compatibility, with 0.0.1. :
			- if you upgrade, please remove all plugin actions, the plugin, then re add ...
	- The OnePing action now returns the response time in ms in eg.result
	- The GetHostsStatus action now returns the last response time in ms (if the host has ever responded to the pings !)
	- Small changes and clean up on the messages sent to the console
	
0.0.1 :
	- Initial release, based on the windows ping.exe program.
	
Last Note :
All actions need to be EXECUTED to actually produce events or set eg.result ...

The Last Note after the last one :
You should have a look at the readme.txt !
"""

eg.RegisterPlugin(
    name = "Ping",
    author = "miljbee+egPing@gmail.com",
    version = "0.0.2",
    guid = "{E0E0AFD7-31D5-41FE-B9DA-237234DB07A7}",
    kind = "other",
    description = "This plugin generates events when an host become available or unavailable on your LAN. It requires that the hosts you want to test tespond to ping requests. Please, have a look at the readme file !",
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=2318",
)
import random
class PingPlugin(eg.PluginBase):
	def __init__(self):
		self.hosts = {}
		self.AddAction(OnePing)
		self.AddAction(AddHost)
		self.AddAction(RemoveHost)
		self.AddAction(GetHostsStatus)
		random.seed()
		
	def __start__(self):
		for host in self.hosts:
			self.hosts[host].StartThread()

	def __stop__(self):
		print "Ping Plugin : Plugin is stopping..."
		for host in self.hosts:
			print "Ping Plugin : Stopping thread " + self.hosts[host].name
			self.hosts[host].StopThread()
		for host in self.hosts:
			print "Ping Plugin : waiting thread " + self.hosts[host].name
			self.hosts[host].pingThread.join()

	def __close__(self):
		print "Ping Plugin : Plugin is closed."
		while len(self.hosts)>0:
			for host in self.hosts:
				print "Ping Plugin : Removing " + self.hosts[host].name + " from the list of managed hosts."
				self.RemoveHost(host)
				break

	def RemoveHost(self, host=""):
		hostToDel=self.hosts.get(host,None)
		if hostToDel:
			if hostToDel.GetThreadState()=="Thread is running":
				hostToDel.StopThread()
				hostToDel.pingThread.join()
			elif hostToDel.GetThreadState()=="Thread is finishing his job":
				hostToDel.pingThread.join()
			elif hostToDel.GetThreadState()=="Problem !":
				print "Ping Plugin : /!\\ Bug #1 please reporte to miljbee+egPing@gmail.com"
			else:
				print "Ping Plugin : /!\\ Bug #2("+hostToDel.GetThreadState()+") please reporte to miljbee+egPing@gmail.com"
			del self.hosts[host]
			print "Ping Plugin : " + host + " has been removed from the list of managed hosts."
			del hostToDel
		else:
			print "Ping Plugin : /!\\ " + host + " isn't in my list !"
		if len(self.hosts)==0:
			print "Ping Plugin : the list of managed hosts is now empty !"
	
	def AddHost(self, host):
		print "Ping Plugin : Adding host " + host.name + " to the list of managed hosts."
		hostToDel=self.hosts.get(host.name,None)
		if hostToDel:
			print "Ping Plugin : /!\\ Host already exists, it will be replaced"
			self.RemoveHost(host.name)
		self.hosts[host.name]=host
		self.hosts[host.name].hostIndex=len(self.hosts)
		self.hosts[host.name].StartThread()

from threading import Event

class OnePing(eg.ActionBase):
	name = "One Ping Now"
	description = "Send one only ping command to the specified host. The state of the hosts is returned in eg.result (None, or responseTimeMs). Optionnaly, you can generate an event."
	
	def __call__(self, hostName,hostFriendlyName,pingDelay,sendEvent,eventAlive,eventDead):
		pyPing = PythonPing(hostName,pingDelay/1000.0,0)
		dummyEvent=Event()
		
		if eventAlive=="":
			if hostFriendlyName=="":
				eventAlive=hostName + "_IS_ALIVE"
			else:
				eventAlive=hostFriendlyName + "_IS_ALIVE"
		if eventDead=="":
			if hostFriendlyName=="":
				eventDead=hostName + "_IS_DEAD"
			else:
				eventDead=hostFriendlyName + "_IS_DEAD"
				
		result=pyPing.Ping(dummyEvent)
		if sendEvent:
			if result:
				eg.TriggerEvent(eventAlive)
			else:
				eg.TriggerEvent(eventDead)
		return result
			
	def Configure(self,hostName="",hostFriendlyName="",pingDelay=200,sendEvent=False,eventAlive="",eventDead=""):
		panel = eg.ConfigPanel()
		hostNameEdit=panel.TextCtrl(hostName)
		hostFriendlyNameEdit=panel.TextCtrl(hostFriendlyName)
		pingDelayEdit=panel.SpinIntCtrl(pingDelay, max=5000)
		sendEventEdit=panel.CheckBox(sendEvent)
		eventAliveEdit=panel.TextCtrl(eventAlive)
		eventDeadEdit=panel.TextCtrl(eventDead)
		panel.AddLine("Host name: ",hostNameEdit)
		panel.AddLine("Host friendly name: ",hostFriendlyNameEdit)
		panel.AddLine("Time to wait for the host response to the ping (milliseconds): ",pingDelayEdit)
		panel.AddLine()
		panel.AddLine("Generate an event ",sendEventEdit)
		panel.AddLine("if checked will generate an event corresponding to the host response, otherwise, eg.result will be set to true/false")
		panel.AddLine()
		panel.AddLine("Event string to fire if the host responds: ",eventAliveEdit)
		panel.AddLine("Event string to fire if the host doesn't responds:",eventDeadEdit)
		while panel.Affirmed():
			panel.SetResult(
				hostNameEdit.GetValue(),
				hostFriendlyNameEdit.GetValue(),
				pingDelayEdit.GetValue(),
				sendEventEdit.GetValue(),
				eventAliveEdit.GetValue(),
				eventDeadEdit.GetValue()
				)

				
class AddHost(eg.ActionBase):
	name = "Add Host"
	description = "Adds a host to the list of managed host. Once done, you'll get an event when the state of the host changes."

	def __call__(self,hostName,hostFriendlyName,pingDelay,hostDelay,eventAlive,eventDead,delayEventAlive,delayEventDead):
		host = Host(hostName,hostFriendlyName,hostDelay,pingDelay,eventAlive,eventDead,delayEventAlive,delayEventDead)
		self.plugin.AddHost(host)
	
	def Configure(self,hostName="",hostFriendlyName="",pingDelay=200,hostDelay=10,eventAlive="",eventDead="",delayEventAlive=1,delayEventDead=1):
		panel = eg.ConfigPanel()
		hostNameEdit=panel.TextCtrl(hostName)
		hostFriendlyNameEdit=panel.TextCtrl(hostFriendlyName)
		pingDelayEdit=panel.SpinIntCtrl(pingDelay, max=10000)
		hostDelayEdit=panel.SpinIntCtrl(hostDelay, max=86400)
		eventAliveEdit=panel.TextCtrl(eventAlive)
		eventDeadEdit=panel.TextCtrl(eventDead)
		delayEventAliveEdit=panel.SpinIntCtrl(delayEventAlive, min=1)
		delayEventDeadEdit=panel.SpinIntCtrl(delayEventDead, min=1)

		
		panel.AddLine("Host Name: ",hostNameEdit)
		panel.AddLine("Host Friendly Name: ",hostFriendlyNameEdit)
		panel.AddLine("Ping delay (ms): ",pingDelayEdit)
		panel.AddLine("Delay between pings (s):",hostDelayEdit)
		panel.AddLine("Name of the event to fire when host become alive: ",eventAliveEdit)
		panel.AddLine("Name of the event to fire when host become dead: ",eventDeadEdit)
		panel.AddLine("The next two settings will delay the events. As an exemple, if you set the first one to 5,\nyou will get the alive event only when five successive ping commands will be successfull")
		panel.AddLine("Number of successive successfull ping to fire the alive event: ",delayEventAliveEdit)
		panel.AddLine("Number of successive unsuccessfull ping to fire the dead event: ",delayEventDeadEdit)
		while panel.Affirmed():
			panel.SetResult(
				hostNameEdit.GetValue(),
				hostFriendlyNameEdit.GetValue(),
				pingDelayEdit.GetValue(),
				hostDelayEdit.GetValue(),
				eventAliveEdit.GetValue(),
				eventDeadEdit.GetValue(),
				delayEventAliveEdit.GetValue(),
				delayEventDeadEdit.GetValue(),
			)
				
class RemoveHost(eg.ActionBase):
	name="Remove Host"
	description="Removes a host from the list of manged hosts. Once done, you won't receive any more event from this host."
	def __call__(self,hostName):
		self.plugin.RemoveHost(hostName)
	
	def Configure(self,hostName=""):
		panel = eg.ConfigPanel()
		hostNameEdit=panel.TextCtrl(hostName)
		panel.AddLine("Enter the name of the host you wish to remove, not the friendly name !")
		panel.AddLine("Host name: ",hostNameEdit)
		while panel.Affirmed():
			panel.SetResult(
				hostNameEdit.GetValue())

#import subprocess

class GetHostsStatus(eg.ActionBase):
	name="Get Hosts Status"
	description="Set eg.result with a python dict containing the config and status of all watched hosts. The key of the dict is the host name.\n"
	description+="Each dict entry is a string where values are separated by a coma.\n the values are :\n"
	description+="hostName,hostFriendlyName,hostDelay,pingDelay, eventAlive,eventDead,delayEventAlive,delayEventDead, status,lastPingResult,lastResponseTimeMS.\n"
	description+="Here is an exemple of a python script you could run jus after this action :\n"
	description+="hosts=eg.result\n"
	description+="for host in hosts:\n"
	description+="    print host + \" : \" + hosts[host]\n"
	description+="    hostData=hosts[host].split(\",\")\n"
	description+="    for idx in range(0,len(hostData)):\n"
	description+="        print hostData[idx]\n"
	def __call__(self):
		res={}
		for hostName in self.plugin.hosts:
			host=self.plugin.hosts[hostName]
			res[hostName]=""
			res[hostName]+=host.name + ","
			res[hostName]+=host.friendlyName + ","
			res[hostName]+=str(host.delay) + ","
			res[hostName]+=str(host.pingDelay) + ","
			res[hostName]+=host.eventAlive + ","
			res[hostName]+=host.eventDead + ","
			res[hostName]+=str(host.delayEventAlive) + ","
			res[hostName]+=str(host.delayEventDead) + ","
			res[hostName]+=host.GetStatus() + ","
			res[hostName]+=host.GetLastPingResult() + ","
			res[hostName]+=host.GetLastResponseTimeMsTxt()
		return res
		
import os
from threading import Event, Thread, Lock

	
class Host:
	def __init__(self,name,friendlyName,delay,pingDelay,eventAlive,eventDead,delayEventAlive,delayEventDead):
		self.delay = delay
		self.pingDelay = pingDelay
		self.name = name
		self.friendlyName = friendlyName
		self.status = "unknown"
		self.lastPingResult = "unknown"
		self.lastResponseTimeMs=None
		self.hostIndex=0
		
		if eventAlive=="":
			if friendlyName=="":
				self.eventAlive=name+"_IS_ALIVE"
			else:
				self.eventAlive=friendlyName+"_IS_ALIVE"
		else:
			self.eventAlive = eventAlive
			
		if eventDead=="":
			if friendlyName=="":
				self.eventDead=name+"_IS_DEAD"
			else:
				self.eventDead=friendlyName+"_IS_DEAD"
		else:
			self.eventDead = eventDead
			
		self.delayEventAlive=delayEventAlive
		self.delayEventDead=delayEventDead
		
		self.pingThread = None
		self.stopPingThreadEvent = Event()
		self.lock = Lock()
				
	def PingThread(self,stopPingThreadEvent):
		print "Ping Plugin : Thread " + self.name + " is starting."
		pyPing = PythonPing(self.name,self.pingDelay/1000.0,self.hostIndex)
		eventsAlive=0
		eventsDead=0
		while not stopPingThreadEvent.isSet():
			if pyPing.Ping(stopPingThreadEvent):
				eventsAlive+=1
				eventsDead=0
				self.lock.acquire()
				try:
					self.lastPingResult="alive"
					self.lastResponseTimeMs=pyPing.responseTimeMs
					if eventsAlive>=self.delayEventAlive:
						if self.status!="alive":
							self.status="alive"
							eg.TriggerEvent(self.eventAlive)
				finally:
					self.lock.release()
			else:
				eventsAlive=0
				eventsDead+=1
				self.lock.acquire()
				try:
					self.lastPingResult="dead"
					if eventsDead>=self.delayEventDead:
						if self.status!="dead":
							self.status="dead"
							eg.TriggerEvent(self.eventDead)
				finally:
					self.lock.release()
			stopPingThreadEvent.wait(self.delay)
		print "Ping Plugin : Thread " + self.name + " is ending ! "

		self.stopPingThreadEvent.clear()
		del pyPing
		#print "Ping Plugin : Thread " + self.name + " has finished his job !"
									
	def GetStatus(self):
		self.lock.acquire()
		try:
			status =self.status
		finally:
			self.lock.release()
		return status
		
	def GetLastPingResult(self):
		self.lock.acquire()
		try:
			res=self.lastPingResult
		finally:
			self.lock.release()
		return res
		
	def GetLastResponseTimeMsTxt(self):
		self.lock.acquire()
		try:
			if self.lastResponseTimeMs:
				res=str(int(self.lastResponseTimeMs))
			else:
				res=""
		finally:
			self.lock.release()
		return res

		
	
	def GetThreadState(self):
		if self.pingThread.isAlive() and not self.stopPingThreadEvent.isSet():
			return "Thread is running"
		elif self.pingThread.isAlive() and self.stopPingThreadEvent.isSet():
			return "Thread is finishing his job"
		elif (not self.pingThread.isAlive()) and (not self.stopPingThreadEvent.isSet()):
			return "Thread is ready to be started"
		else:
			return "Problem !"
	
	def StopThread(self):
		self.stopPingThreadEvent.set()
		
	def StartThread(self):
		if self.stopPingThreadEvent.isSet():
			#print "/!\\ Problem : stopPingThreadEvent Is Set ..."
			self.stopPingThreadEvent.clear()
		self.pingThread = Thread(target=self.PingThread,args=(self.stopPingThreadEvent,))
		self.pingThread.start()

	def Print(self):
		print self.delay
		print self.name
		print self.friendlyName
		print self.status
		print self.eventAlive
		print self.eventDead


"""
    A pure python ping implementation using raw socket found here :
	http://www.g-loaded.eu/2009/10/30/python-ping/
	
	I have modified a bit the code to make it fit my needs !
	
	The main modification concerns the ping ID :
	This id is sent in the ping packet and returned in the pong.
	It is used to match the ping and the pong. If the ID doesn't match, it means that the pong is a response to another ping command.
	Usually, it seems that the ping ID is the processID of the process that send the ping.
	The problem here it that this code is multithreaded and that several ping packet might be sent at the same time.
	When I first tested the code, all ping packets had the same ping ID (they where running in the same process), and it has been a big mess ...
	So I have had to found something else for the ping ID.
	-Something that's 16bit long
	-Something that's not a pid, because if unfortunately, another program with this pid pings the same host, it will catch my pong ...
	
	After digging a bit, I decided that the chances that a pid arround 32k exists where low (really low). Further more, a pid that correspond to a process that pings the same host as my script ...
	
	So I computed the ping ID like this : 32768 - hostIndex (if you have ten hosts, the tenth has a hostIndex=10)
	
	That might not be 100% safe, but that's the less worst I found !
	
	Feel free to reuse this code, but be carefull, the original one has been released under GNU General Public License version 2.
"""

import os, sys, socket, struct, select, time



ICMP_ECHO_REQUEST = 8
class PythonPing:
	def __init__(self,hostName,timeOut,pingID):
		self.hostName=hostName
		self.timeOut=timeOut
		self.theSocket=None
		self.theID=(32767-pingID) & 0xFFFF
		self.responseTimeMs=None
		
	def Checksum(self,source_string):
		"""
		I'm not too confident that this is right but testing seems
		to suggest that it gives the same answers as in_cksum in ping.c
		"""
		sum = 0
		countTo = (len(source_string)/2)*2
		count = 0
		while count<countTo:
			thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
			sum = sum + thisVal
			sum = sum & 0xffffffff # Necessary?
			count = count + 2

		if countTo<len(source_string):
			sum = sum + ord(source_string[len(source_string) - 1])
			sum = sum & 0xffffffff # Necessary?

		sum = (sum >> 16)  +  (sum & 0xffff)
		sum = sum + (sum >> 16)

		answer = ~sum
		answer = answer & 0xffff

		# Swap bytes. Bugger me if I know why.
		answer = answer >> 8 | (answer << 8 & 0xff00)

		return answer


	def ReceiveOnePing(self,stopPingThreadEvent):
		"""
		receive the ping from the socket.
		"""
		
		timeLeft = self.timeOut
		while True:
			startedSelect = time.clock()
			dontstop=True
			while (time.clock()-startedSelect)<timeLeft and dontstop:
				whatReady = select.select([self.theSocket], [], [], 0.001)

				howLongInSelect = (time.clock() - startedSelect)
				if whatReady[0]!=[]:
					dontstop=False
					
				if stopPingThreadEvent.isSet():
					dontstop=False

			if whatReady[0] == []: # Timeout or stopped
				self.theSocket.close()
				del self.theSocket
				return

			timeReceived = time.clock()

			recPacket, addr = self.theSocket.recvfrom(1024)
			icmpHeader = recPacket[20:28]

			type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
			if packetID == self.theID:
				bytesInDouble = struct.calcsize("d")
				timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
				self.theSocket.close()
				del self.theSocket
				return timeReceived - timeSent

			timeLeft = timeLeft - howLongInSelect
			if timeLeft <= 0:
				self.theSocket.close()
				del self.theSocket
				return


	def SendOnePing(self):

		"""
		Send one ping to the given >self.hostName<.
		"""
		
		dest_addr  =  socket.gethostbyname(self.hostName)

		# Header is type (8), code (8), checksum (16), id (16), sequence (16)
		my_checksum = 0

		# Make a dummy heder with a 0 checksum.
		header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, self.theID, 1)

		bytesInDouble = struct.calcsize("d")

		data = (192 - bytesInDouble) * "Q"

		data = struct.pack("d", time.clock()) + data

		# Calculate the checksum on the data and the dummy header.
		my_checksum = self.Checksum(header + data)

		# Now that we have the right checksum, we put that in. It's just easier
		# to make up a new header than to stuff it into the dummy.
		header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), self.theID, 1)
		packet = header + data
		self.theSocket.sendto(packet, (dest_addr, 1)) # Don't know about the 1

	def Ping(self,stopPingThreadEvent):
		"""
		Returns either the delay (in seconds) or none on timeout.
		"""

		icmp = socket.getprotobyname("icmp")
		try:
			self.theSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
		except socket.error, (errno, msg):
			if errno == 1:
				# Operation not permitted
				msg = msg + (
					" - Note that ICMP messages can only be sent from processes"
					" running as root."
				)
				raise socket.error(msg)
			raise # raise the original error

		self.SendOnePing()
		self.responseTimeMs=self.ReceiveOnePing(stopPingThreadEvent)
		if self.responseTimeMs:
			self.responseTimeMs=self.responseTimeMs*1000.0
		return self.responseTimeMs
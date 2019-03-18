eg.RegisterPlugin(
	name = "Logitech G-Keys",
	author = "Marc A. W.",
	version = "0.2",
	kind = "remote",
	guid = "{6B74C4C3-DA96-4076-A2A7-BF3893656422}",
	canMultiLoad = True,
	description = (
		'Get events from G-Keys of Logitech Gaming Keyboards (G11/G15) '
		'and control LED\'s and backlight.<br><br><br>'
		'Special Thanks to Bartman, who created the \'Generic-HID\''
		'-plugin, that this plugin was based on.'
	)
)

import struct
import sys
from eg.WinApi.HID import HIDThread, GetDevicePath, GetDeviceDescriptions, DeviceDescription, IsDeviceName
from threading import Timer

class Text:
	manufacturer = "Manufacturer"
	deviceName = "Device Name"
	connected = "Connected"
	eventName = "Event prefix (optional):"
	yes = "Yes"
	no = "No"
	enduringEvents = "Trigger enduring events for buttons"
	blTrack = "Track level of backlight"
	blCorrect = "Correct level of backlight"
	autoMCat = "Automatically handle M-Key Categories: "
	remMxMRLight = "Don't include Mx in Eventstring at Mx, MR, Light"
	formatString = "Event String Format: "
	multipleDeviceOptions = "Options for multiple same devices"
	noOtherPort = "Use selected device only if connected to current port"
	useDeviceIndex = "Use the device with index"
	errorFind = "Error finding HID device: "
	vendorID = "Vendor ID "
	class SetBacklight:
		name = "Set Backlight"
		description = "Set the G-Keyboard backlight to Off/Half/Full"
		level = "Set To Level:"
		off = "Off"
		half = "Half"
		full = "Full"
	class SetLED:
		name = "Set LEDs"
		description = "Set the M-Key LED's"
		mkv = "M-Key Values:"
		allOff = ": All Off"
	

GKBITS={
0:"G1",
2:"G13",
7:"Light",
8:"G7",
9:"G2",
11:"G14",
17:"G8",
18:"G3",
20:"G15",
26:"G9",
27:"G4",
29:"G16",
35:"G10",
36:"G5",
38:"G17",
40:"M1",
44:"G11",
45:"G6",
49:"M2",
53:"G12",
54:"MR",
58:"M3",
62:"G18"
}
IGNORE_MSTATE=("Light","M1","M2","M3","MR")

import binascii
class LogG(eg.PluginClass):
	text = Text
	blcoeff=(1,1,2,2,0) #index: internal+actual backlight value
						#blcoeff=(((bli+bl)>>1)+1)%3
	#Eventstring Formats
	evfmts=("Key","Press/Release.Key","Key.Press/Release","Mx.Key","Key.Mx",\
		"Press/Release.Mx.Key","Press/Release.Key.Mx",\
		"Mx.Key.Press/Release","Key.Mx.Press/Release",\
		"Mx.Press/Release.Key","Key.Press/Release.Mx")
	evfmtsendind=((tuple(range(0,3)),tuple(range(0,11))),((0,),(0,3,4)))
	
	def __init__(self):
		self.thread = None
		self.AddAction(SetBacklight)
		self.AddAction(SetLED)
	
	
	def SetBacklight(self,level):
		if level<0:
			level=0
		elif level>2:
			level=2
		cmd=struct.pack("B"*4,*[2,1,level,0])
		self.thread.SetFeature(cmd)
		self.bl=level
	
	def GetBacklight(self):
		return bl
	
	def TrackBacklight(self):
		self.bli=self.blcoeff[self.bli+self.bl]
		if self.blCorrect:
			self.SetBacklight((self.bl+1)%3)
		else:
			self.bl=self.bli
		
	def MKeyPress(self,n,o):
		keys=("M1","M2","M3")
		bits=(24,)
		bits=bits+tuple([(1<<x) for x in DicReverseLookup(GKBITS,keys)])
		p=n&~o
		if self.autoMCat==1:
			for i,b in enumerate(bits):
				if p&b:
					self.SetMCat(i)
					break
		elif self.autoMCat==2:
			for i,b in enumerate(bits):
				if p&b:
					mc=i
					if mc==self.mstate:
						mc+=3
					self.SetMCat(mc)
					break
		elif self.autoMCat==3:
			if p&bits[2]:
				self.SetMCat(1)
			elif p&bits[1]:
				newm=self.mstate-1
				if newm<1:
					newm=8
				self.SetMCat(newm)
			elif p&bits[3]:
				newm=self.mstate+1
				if newm>8:
					newm=1
				self.SetMCat(newm)
	
	def SetMCat(self,mcat):
		self.mstate=mcat
		l=((),
			((0,0,0,2),(1,0,0,2),(0,1,0,2),(0,0,1,2)),
			((0,0,0,2),(1,0,0,2),(0,1,0,2),(0,0,1,2),(0,1,1,2),(1,0,1,2),(1,1,0,2)),
			((0,0,0,2),(0,0,0,2),(0,0,1,2),(0,1,0,2),(0,1,1,2),(1,0,0,2),(1,0,1,2),(1,1,0,2),(1,1,1,2)))
		self.SetLED(l[self.autoMCat][mcat])
	
	def SetLED(self,leds):
		smask=0x0
		smask|=0x1 if leds[0]==1 else 0x0
		smask|=0x2 if leds[1]==1 else 0x0
		smask|=0x4 if leds[2]==1 else 0x0
		smask|=0x8 if leds[3]==1 else 0x0
		cmask=0x0
		cmask|=0x1 if leds[0]==0 else 0x0
		cmask|=0x2 if leds[1]==0 else 0x0
		cmask|=0x4 if leds[2]==0 else 0x0
		cmask|=0x8 if leds[3]==0 else 0x0
		self.lmask|=cmask
		self.lmask&=~smask
		cmd=struct.pack("B"*4,*[2,4,self.lmask,0])
		self.thread.SetFeature(cmd)
		
	def GetLED(self):
		return (self.lmask&0x1,self.lmask&0x2,self.lmask&0x4,self.lmask&0x8)

	def RawCallback(self, data):
		#self.TriggerEvent(binascii.hexlify(data))
		#return
		val=struct.unpack_from("@Q",data,1)[0]
		val&=~(1<<24)
		#pressed buttons
		p=val&~self.prevVal
		#released buttons
		r=self.prevVal&~val
		if self.blTrack:
			lbit=DicReverseLookup(GKBITS,("Light",))[0]
			if p&(1<<lbit):
				self.TrackBacklight()
		if self.autoMCat:
			mask=0
			for bit in [(1<<x) for x in DicReverseLookup(GKBITS,("M1","M2","M3"))]:
				mask|=bit
			if p&mask or r&mask:
				self.MKeyPress(val,self.prevVal)

		fmtstr=self.evfmts[self.evfmtsendind[self.enduringEvents][self.autoMCat>0][self.evtFormat]]

		class Payload:
			pass

		for (bit,kn) in GKBITS.items():
			payload=Payload()
			if self.autoMCat:
				payload.m=self.mstate
			evstr=fmtstr.replace("Key",kn)
			if kn in IGNORE_MSTATE and self.remMxMRLight:
				evstr=evstr.replace("Mx.","").replace(".Mx","")
			else:
				evstr=evstr.replace("Mx","M"+str(self.mstate))
			if p&(1<<bit):
				payload.pr=1
				if self.enduringEvents:
					self.TriggerEnduringEvent(evstr,payload=payload)
				else:
					self.TriggerEvent(evstr.replace("Press/Release","Press"),payload=payload)
			elif r&(1<<bit):
				payload.pr=0
				self.EndLastEvent()
				if not self.enduringEvents and "Press/Release" in evstr:
					self.TriggerEvent(evstr.replace("Press/Release","Release"),payload=payload)
		#print "{0:0>16X}".format(p)
		self.prevVal=val
		
		"""if p&1:
			cmd=[0x02,0x01,0x01,0x00]
			cmd=struct.pack("B"*4,*cmd)
			self.thread.SetFeature(cmd)"""
		
	def StopCallback(self):
		self.TriggerEvent("Stopped")
		self.thread = None
	
	def GetMyDevicePath(self):
		path = GetDevicePath(
			self.devicePath,
			self.vendorID,
			self.productID,
			self.versionNumber,
			self.useDeviceIndex,
			self.deviceIndex,
			self.noOtherPort)
		return path;
	
	def SetupHidThread(self, newDevicePath):
		#create thread
		self.thread = HIDThread(self.vendorString + " " + self.productString, newDevicePath)
		self.thread.start()
		self.thread.SetStopCallback(self.StopCallback)
		self.thread.SetRawCallback(self.RawCallback)
	
	def ReconnectDevice(self, event):
		"""method to reconnect a disconnect device"""
		if self.thread == None:
			if not IsDeviceName(event.payload, self.vendorID, self.productID):
				return

			#check if the right device was connected
			#getting devicePath
			newDevicePath = self.GetMyDevicePath()
			if not newDevicePath:
				#wrong device
				return
			
			self.SetupHidThread(newDevicePath)

	def GetLabel(self,
		eventName,
		enduringEvents,
		blTrack,
		blCorrect,
		autoMCat,
		evtFormat,
		remMxMRLight,
		noOtherPort,
		devicePath,
		vendorID,
		vendorString,
		productID,
		productString,
		versionNumber,
		useDeviceIndex = False,
		deviceIndex = 0
	):
		prefix = "LogG: "
		#one or both strings empty should not happen
		if not vendorString or not productString:
			return "LogitechGaming"

		#productString already contains manufacturer or vendor id only
		if productString.find(vendorString) != -1 or\
			vendorString[0:len(self.text.vendorID)] == self.text.vendorID:
			return prefix + productString

		return prefix + vendorString + " " + productString

	def __start__(self,
		eventName,
		enduringEvents,
		blTrack,
		blCorrect,
		autoMCat,
		evtFormat,
		remMxMRLight,
		noOtherPort,
		devicePath,
		vendorID,
		vendorString,
		productID,
		productString,
		versionNumber,
		useDeviceIndex = False,
		deviceIndex = 0
	):
		#saving parameters so they can be used to reconnect a device
		self.eventName = eventName
		self.enduringEvents = enduringEvents
		self.noOtherPort = noOtherPort
		self.devicePath = devicePath
		self.vendorID = vendorID
		self.vendorString = vendorString
		self.productID = productID
		self.productString = productString
		self.versionNumber = versionNumber
		self.useDeviceIndex = useDeviceIndex
		self.deviceIndex = deviceIndex
		#self.oldValues = {}
		self.prevVal=0
		self.lmask=0xE
		self.bl=2
		self.bli=2
		self.blTrack=blTrack
		self.blCorrect=blCorrect
		self.autoMCat=autoMCat
		self.mstate=1
		self.evtFormat=evtFormat
		self.remMxMRLight=remMxMRLight

		if eventName:
			self.info.eventPrefix = eventName
		else:
			self.info.eventPrefix = "LogG"

		#Bind plug in to RegisterDeviceNotification message 
		eg.Bind("System.DeviceAttached", self.ReconnectDevice)
		
		newDevicePath = self.GetMyDevicePath()
		if not newDevicePath:
			#device not found
			self.PrintError(self.text.errorFind)
		else:
			self.SetupHidThread(newDevicePath)
		
		def initLED():
			self.SetLED((0,0,0,0))
			if self.autoMCat:
				self.SetMCat(1)
		t=Timer(0.0,initLED)
		t.start()

	def __stop__(self):
		if self.thread:
			self.thread.AbortThread()
		
		#unbind from RegisterDeviceNotification message
		eg.Unbind("System.DeviceAttached", self.ReconnectDevice)

	def Configure(self,
		eventName = "",
		enduringEvents = False,
		blTrack = True,
		blCorrect = True,
		autoMCat = False,
		evtFormat = 0,
		remMxMRLight = True,
		noOtherPort = False,
		devicePath = None,
		vendorID = None,
		vendorString = None,
		productID = None,
		productString = None,
		versionNumber = None,
		useDeviceIndex = False,
		deviceIndex = 0
	):
		deviceList = GetDeviceDescriptions()
		panel = eg.ConfigPanel(self, resizable=True)

		#building dialog
		hidList = wx.ListCtrl(panel, -1, pos=wx.DefaultPosition,
			size=wx.DefaultSize, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

		#create GUI
		hidList.InsertColumn(0, self.text.deviceName)
		hidList.InsertColumn(1, self.text.manufacturer)
		hidList.InsertColumn(2, self.text.connected)

		path = GetDevicePath(
			devicePath,
			vendorID,
			productID,
			versionNumber,
			noOtherPort,
			useDeviceIndex,
			deviceIndex,
			deviceList)

		#fill list
		devices = {}
		idx = 0
		for item in deviceList:
			if item.vendorId!=1133 or item.productId!=0xc225:
				continue
			idx = hidList.InsertStringItem(sys.maxint, item.productString)
			hidList.SetStringItem(idx, 1, item.vendorString)
			hidList.SetStringItem(idx, 2, self.text.yes)
			if item.devicePath == path:
				hidList.Select(idx)
			devices[idx] = item

		#add not connected device to bottom of list
		#eg.Print(path)
		#eg.Print(devicePath)
		if not path and devicePath:
			item = DeviceDescription(
				devicePath,
				vendorID,
				vendorString,
				productID,
				productString,
				versionNumber)
			print item.productString
			idx = hidList.InsertStringItem(sys.maxint, item.productString)
			hidList.SetStringItem(idx, 1, item.vendorString)
			hidList.SetStringItem(idx, 2, self.text.no)
			hidList.Select(idx)
			devices[idx] = item

		#no device selected, disable ok and apply button
		panel.EnableButtons(hidList.GetFirstSelected() != -1)

		#layout
		for i in range(hidList.GetColumnCount()):
			hidList.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
			size = hidList.GetColumnWidth(i)
			hidList.SetColumnWidth(i, wx.LIST_AUTOSIZE)
			hidList.SetColumnWidth(i, max(size, hidList.GetColumnWidth(i) + 5))

		panel.sizer.Add(hidList, 1, flag = wx.EXPAND)

		#sizers
		optionsSizer = wx.GridBagSizer(0, 8)

		#eventname
		optionsSizer.Add(
			wx.StaticText(panel, -1, self.text.eventName),
			(0, 0),
			flag = wx.ALIGN_CENTER_VERTICAL)
		eventNameCtrl = wx.TextCtrl(panel, value = eventName)
		eventNameCtrl.SetMaxLength(32)
		optionsSizer.Add(eventNameCtrl, (0, 1), (1, 2), flag = wx.EXPAND)

		#checkbox for enduring event option
		enduringEventsCtrl = wx.CheckBox(panel, -1, self.text.enduringEvents)
		enduringEventsCtrl.SetValue(enduringEvents)
		optionsSizer.Add(enduringEventsCtrl, (1, 0), (1, 3))

		#checkbox for raw data events
		#rawDataEventsCtrl = wx.CheckBox(panel, -1, Text.rawDataEvents)
		#rawDataEventsCtrl.SetValue(rawDataEvents)
		#optionsSizer.Add(rawDataEventsCtrl, (2, 0), (1, 3))
		
		#checkbox for tracking backlight level
		blTrackCtrl=wx.CheckBox(panel,wx.ID_ANY,self.text.blTrack)
		blTrackCtrl.SetValue(blTrack)
		optionsSizer.Add(blTrackCtrl,(2,0),(1,1))
		
		#checkbox for automatically correcting backlight level
		blCorrectCtrl=wx.CheckBox(panel,wx.ID_ANY,self.text.blCorrect)
		blCorrectCtrl.SetValue(blCorrect)
		optionsSizer.Add(blCorrectCtrl,(2,1),(1,2))
		
		#checkbox for automatically handling M-Keys
		#autoMCatCtrl=wx.CheckBox(panel,wx.ID_ANY,self.text.autoMCat)
		#autoMCatCtrl.SetValue(autoMCat)
		#optionsSizer.Add(autoMCatCtrl,(3,0),(1,2))
		
		
		#dropdown box for M-State mode
		autoMCatCtrl=wx.ComboBox(panel,wx.ID_ANY,style=wx.CB_READONLY,choices=("no","3","6","8"))
		autoMCatCtrl.SetSelection(autoMCat)
		optionsSizer.Add(wx.StaticText(panel,wx.ID_ANY,self.text.autoMCat),(3,0),(1,2),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
		optionsSizer.Add(autoMCatCtrl,(3,2),(1,1))
		
		
		#checkbox for ignoring mstate for keys Mx,MR,Light
		remMxMRLightCtrl=wx.CheckBox(panel,wx.ID_ANY,self.text.remMxMRLight)
		optionsSizer.Add(remMxMRLightCtrl,(4,0),(1,3))
		
		#dropodown box for the format of an event string
		evtFormatCtrl=wx.ComboBox(panel,wx.ID_ANY,style=wx.CB_READONLY)
		#evtFormat.AppendItems(("asd","asd2","asd4"))
		optionsSizer.Add(evtFormatCtrl,(5,1),(1,2))
		optionsSizer.Add(wx.StaticText(panel,wx.ID_ANY,self.text.formatString)
						,(5,0),(1,1),flag = wx.ALIGN_CENTER_VERTICAL)
		def FillEvtFormatCtrl():
			evtFormatCtrl.Clear()
			evtFormatCtrl.AppendItems(SubTuple(self.evfmts,self.evfmtsendind[enduringEventsCtrl.GetValue()][autoMCatCtrl.GetSelection()>0]))
		FillEvtFormatCtrl()
		evtFormatCtrl.SetSelection(evtFormat)

		#text
		optionsSizer.Add(
			wx.StaticText(panel, -1, self.text.multipleDeviceOptions),
			(6, 0), (1, 3),
			flag = wx.ALIGN_CENTER_VERTICAL)
		
		#checkbox for use first device
		useDeviceIndexCtrl = wx.CheckBox(panel, -1, self.text.useDeviceIndex)
		useDeviceIndexCtrl.SetValue(useDeviceIndex)
		optionsSizer.Add(useDeviceIndexCtrl, (7, 0), (1, 2), flag = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
		
		#device index spin control
		deviceIndexCtrl = eg.SpinIntCtrl(panel, -1, deviceIndex, 0, 99, size=(100,-1))
		optionsSizer.Add(deviceIndexCtrl, (7, 2), (1, 1))

		#checkbox for no other port option
		noOtherPortCtrl = wx.CheckBox(panel, -1, self.text.noOtherPort)
		noOtherPortCtrl.SetValue(noOtherPort)
		optionsSizer.Add(noOtherPortCtrl, (8, 0), (1, 3))

		panel.sizer.Add(optionsSizer, 0, wx.TOP, 10)

		def OnHidListSelect(event):
			panel.EnableButtons(hidList.GetFirstSelected() != -1)
			event.Skip()

		def OnUseDeviceIndexCtrlChange(event):
			noOtherPortCtrl.Enable(not useDeviceIndexCtrl.GetValue())
			deviceIndexCtrl.Enable(useDeviceIndexCtrl.GetValue())
			event.Skip()

		def OnNoOtherPortChange(event):
			useDeviceIndexCtrl.Enable(not noOtherPortCtrl.GetValue())
			deviceIndexCtrl.Enable(not noOtherPortCtrl.GetValue())
			event.Skip()
		
		def OnBlTrackChange(event):
			if blTrackCtrl.GetValue():
				blCorrectCtrl.Enable(True)				
				blCorrectCtrl.SetValue(OnBlTrackChange.blCorrect)
			else:
				blCorrectCtrl.Enable(False)
				OnBlTrackChange.blCorrect=blCorrectCtrl.GetValue()
				blCorrectCtrl.SetValue(False)
			event.Skip()
		OnBlTrackChange.blCorrect=blCorrect
		
		def OnMCatEndEvFormatUpdate(event):
			val=evtFormatCtrl.GetValue()
			FillEvtFormatCtrl()
			evtFormatCtrl.SetValue(val)
			if evtFormatCtrl.GetSelection()==wx.NOT_FOUND:
				evtFormatCtrl.SetSelection(0)
			OnEvFormatChange(event)
			event.Skip()
		
		def OnEvFormatChange(event):
			if "Mx" in evtFormatCtrl.GetValue():
				remMxMRLightCtrl.Enable(True)
				remMxMRLightCtrl.SetValue(OnEvFormatChange.rem)
			else:
				remMxMRLightCtrl.Enable(False)
				OnEvFormatChange.rem=remMxMRLightCtrl.GetValue()
				remMxMRLightCtrl.SetValue(False)
			event.Skip()
		OnEvFormatChange.rem=remMxMRLight

		OnUseDeviceIndexCtrlChange(wx.CommandEvent())
		OnNoOtherPortChange(wx.CommandEvent())
		OnBlTrackChange(wx.CommandEvent())
		OnMCatEndEvFormatUpdate(wx.CommandEvent())
		OnEvFormatChange(wx.CommandEvent())
		useDeviceIndexCtrl.Bind(wx.EVT_CHECKBOX, OnUseDeviceIndexCtrlChange)
		noOtherPortCtrl.Bind(wx.EVT_CHECKBOX, OnNoOtherPortChange)
		blTrackCtrl.Bind(wx.EVT_CHECKBOX,OnBlTrackChange)
		autoMCatCtrl.Bind(wx.EVT_COMBOBOX,OnMCatEndEvFormatUpdate)
		enduringEventsCtrl.Bind(wx.EVT_CHECKBOX,OnMCatEndEvFormatUpdate)
		evtFormatCtrl.Bind(wx.EVT_COMBOBOX,OnEvFormatChange)
		hidList.Bind(wx.EVT_LIST_ITEM_SELECTED, OnHidListSelect)
		hidList.Bind(wx.EVT_LIST_ITEM_DESELECTED, OnHidListSelect)

		while panel.Affirmed():
			device = devices[hidList.GetFirstSelected()]
			panel.SetResult(
				eventNameCtrl.GetValue(),
				enduringEventsCtrl.GetValue(),
				blTrackCtrl.GetValue(),
				blCorrectCtrl.GetValue(),
				autoMCatCtrl.GetSelection(),
				evtFormatCtrl.GetSelection(),
				remMxMRLightCtrl.GetValue(),
				noOtherPortCtrl.GetValue(),
				device.devicePath,
				device.vendorId,
				device.vendorString,
				device.productId,
				device.productString,
				device.versionNumber,
				useDeviceIndexCtrl.GetValue(),
				deviceIndexCtrl.GetValue(),
			)



class SetBacklight(eg.ActionBase):
	#name=text.name
	#description=text.description
	def __call__(self,level=2):
		self.plugin.SetBacklight(level)

	def GetLabel(self,level=2):
		return self.name+": "+(self.text.full,self.text.half,self.text.off)[2-level]

	def Configure(self,level=2):
		panel=eg.ConfigPanel()
		tlvl=wx.StaticText(panel,wx.ID_ANY,self.text.level)
		cblevel=wx.ComboBox(panel,
							wx.ID_ANY,
							choices=(self.text.full,self.text.half,self.text.off),
							style=wx.CB_READONLY)
		cblevel.SetSelection(2-level)
		panel.sizer.AddStretchSpacer(2)
		panel.sizer.Add(tlvl,0,wx.CENTER)
		panel.sizer.AddSpacer(10)
		panel.sizer.Add(cblevel,0,wx.CENTER)
		panel.sizer.AddStretchSpacer(3)
		while panel.Affirmed():
			panel.SetResult(2-cblevel.GetSelection())



class SetLED(eg.ActionBase):
	dled=(wx.CHK_UNDETERMINED,wx.CHK_UNDETERMINED,wx.CHK_UNDETERMINED,wx.CHK_UNDETERMINED)
	def __call__(self,leds=dled):
		self.plugin.SetLED(leds)
	
	def GetLabel(self,leds=dled):
		if not True in leds:
			return self.name + self.text.allOff
		return self.name + ":" + \
			(" +M1" if leds[0]==wx.CHK_CHECKED else (" -M1" if leds[0]==wx.CHK_UNCHECKED else "")) + \
			(" +M2" if leds[1]==wx.CHK_CHECKED else (" -M2" if leds[1]==wx.CHK_UNCHECKED else "")) + \
			(" +M3" if leds[2]==wx.CHK_CHECKED else (" -M3" if leds[2]==wx.CHK_UNCHECKED else "")) + \
			(" +MR" if leds[3]==wx.CHK_CHECKED else (" -MR" if leds[3]==wx.CHK_UNCHECKED else ""))

	def Configure(self,leds=dled):
		panel=eg.ConfigPanel()
		tl=wx.StaticText(panel,wx.ID_ANY,self.text.mkv)
		cbm1=wx.CheckBox(panel,wx.ID_ANY,"M1",style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
		cbm1.Set3StateValue(leds[0])
		cbm2=wx.CheckBox(panel,wx.ID_ANY,"M2",style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
		cbm2.Set3StateValue(leds[1])
		cbm3=wx.CheckBox(panel,wx.ID_ANY,"M3",style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
		cbm3.Set3StateValue(leds[2])
		cbmr=wx.CheckBox(panel,wx.ID_ANY,"MR",style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
		cbmr.Set3StateValue(leds[3])
		sz=wx.BoxSizer(wx.HORIZONTAL)
		sz.AddStretchSpacer(1)
		sz.Add(cbm1,0,wx.CENTER)
		sz.AddStretchSpacer(1)
		sz.Add(cbm2,0,wx.CENTER)
		sz.AddStretchSpacer(1)
		sz.Add(cbm3,0,wx.CENTER)
		sz.AddStretchSpacer(1)
		sz.Add(cbmr,0,wx.CENTER)
		sz.AddStretchSpacer(1)
		panel.sizer.AddStretchSpacer(2)
		panel.sizer.Add(tl,0,wx.CENTER)
		panel.sizer.AddSpacer(10)
		panel.sizer.Add(sz,0,wx.EXPAND)
		panel.sizer.AddStretchSpacer(3)
		while panel.Affirmed():
			panel.SetResult((cbm1.Get3StateValue(),
							cbm2.Get3StateValue(),
							cbm3.Get3StateValue(),
							cbmr.Get3StateValue()))



def SubTuple(tup, indices):
	r=[]
	for x in indices:
		r.append(tup[x])
	return tuple(r)
	
def DicReverseLookup(dic,vals):
	r=[]
	for x in vals:
		r.append([k for k, v in dic.iteritems() if v == x][0])
	return tuple(r)
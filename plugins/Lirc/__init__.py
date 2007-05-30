### Script for handling (Win)Lirc events by jinxdone - 4th Jan 2007


import eg, wx, socket, asyncore, time, threading

class Text:
	version = "0.5.0"
	title = "LIRC Event Receiver plugin v" + version + " by jinxdone"
	host = "Host:"
	port = "Port:"
	hosttitle = "Target Host"
	onlyfirst = "Only use the first event"
	addremote = "Add remote-name"
	addrepeat = "Add repeat-tag"
	enduring = "Use enduring-events"
	ignoretime = "Ignoretime after first event (ms)"



class Lirc_Reader(asyncore.dispatcher):


	### Initializing all the variables and open the tcp connection..
	###
	def __init__(
		self, host,	port,	handler, onlyfirst,
		addremote, addrepeat, enduring, ignoretime
	):
		self.handler = handler
		self.onlyfirst = onlyfirst
		self.addremote = addremote
		self.addrepeat = addrepeat
		self.enduring = enduring
		self.ignoretime = ignoretime
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect((host, port))
		self.buffer = ""

	### Some helper functions..
	###
	def checker(self):
		print "ending event.."
		self.handler.EndLastEvent()


	def mscounter(self):
		if time.time()*1000 - self.recvtime*1000 < self.ignoretime:
			return False
		else:
			return True


	### We don't want to send any data so let's stop asyncore
	### from checking wether or not the socket is writable.
	###
	def writable(self):
		return False


	### This will be run if the tcp connection is disconnected
	### or if we want to close it ourselves.
	###
	def handle_close(self):
		print "Closing the lirc-reader.."
		self.close()


	### This will be run if theres a problem opening the connection
	###
	def handle_expt(self):
		self.handler.PrintError("Could not connect to the target host!")
		print "Please doublecheck your configuration and that the target is reachable"
		self.handler.__stop__()

	### This gets run whenever asyncore detects there is data waiting
	### for us to be read at the socket, so this is where it's all at..
	###
	def handle_read(self):
		# Append data from the socket onto a buffer
		self.buffer = self.buffer + self.recv(4096)

		# (if theres anything on the right of the last linebreak, it must be
		#  some incomplete data caused by tcp/ip fragmenting our strings..)
		# hopefully the rest of it will be there on the next run..
		self.events = self.buffer.split("\n")
		self.buffer = self.events.pop()

		# loop through all the received events, incase there are
		# more than one to be processed
		for self.event in self.events:

			# split a single event into atoms
			self.event = self.event.split()
			# some checking never hurts..
			if len(self.event) < 4: break

			# shape the eventstring the way the user wants it
			# (add remote name, add is-repeat-tag, discard repeat events..)
			if self.addremote:
				self.egevent = self.event[3] + ":" + self.event[2]
			else:
				self.egevent = self.event[2]

			if self.event[1] == "00":
				if self.enduring:
					try:
						self.schedule.cancel()
					except:
						pass
					self.handler.TriggerEnduringEvent(self.egevent)
					self.schedule = threading.Timer(0.4, self.checker)
					self.schedule.start()
				else:
					if not self.onlyfirst:
						if self.ignoretime:
							self.recvtime = time.time()
					self.handler.TriggerEvent(self.egevent)
			else:
				if self.enduring:
					#print "giving cpr to this event.. " + self.event[1]
					self.schedule.cancel()
					self.schedule = threading.Timer(0.4, self.checker)
					self.schedule.start()
				else:
					if self.onlyfirst:
						break
					if self.addrepeat:
						self.egevent = self.egevent + "++"
					if self.ignoretime:
						if self.mscounter():
							self.handler.TriggerEvent(self.egevent)
					else:
						self.handler.TriggerEvent(self.egevent)


	### mandatory, but we won't need these..
	###
	def handle_connect(self):
		pass


	def handle_write(self):
		pass



### The EventGhost classes and functions are over here..
class Lirc(eg.PluginClass):
	canMultiLoad = True
    

	def __start__(self, host, port, onlyfirst, addremote, addrepeat, enduring, ignoretime):
		self.port = port
		self.host = host
		self.onlyfirst = onlyfirst
		self.addremote = addremote
		self.addrepeat = addrepeat
		self.enduring = enduring
		self.ignoretime = ignoretime
		self.reader = Lirc_Reader(
			self.host,
			self.port,
			self,
			self.onlyfirst,
			self.addremote,
			self.addrepeat,
			self.enduring,
			self.ignoretime
		)
		

	def __stop__(self):
		if self.reader:
		    self.reader.handle_close()
		self.reader = None


	def Configure(
		self,
		host="127.0.0.1",
		port=8765,
		onlyfirst = False,
		addremote = False,
		addrepeat = False,
		enduring = False,
		ignoretime = 0
	):
		text = Text
		dialog = eg.ConfigurationDialog(self)
		TitleText = wx.StaticText(dialog, -1, text.title, style=wx.ALIGN_CENTER)
		HostText = wx.StaticText(dialog, -1, text.host)
		HostCtrl = wx.TextCtrl(dialog, -1, host)
		PortText = wx.StaticText(dialog, -1, text.port)
		PortCtrl = eg.SpinIntCtrl(dialog, -1, port, max=65535)

		HostSizer = wx.FlexGridSizer(cols=2)
		HostSizer.Add(HostText, 0, wx.ALL, 5)
		HostSizer.Add(HostCtrl, 0, wx.ALL, 3)
		HostSizer.Add(PortText, 0, wx.ALL, 5)
		HostSizer.Add(PortCtrl, 0, wx.ALL, 3)
		HostBox = wx.StaticBox(dialog, -1, text.hosttitle)
		shbSizer = wx.StaticBoxSizer(HostBox)
		shbSizer.Add(HostSizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		OnlyFirstCtrl = wx.CheckBox(dialog, -1, text.onlyfirst)
		OnlyFirstCtrl.SetValue(onlyfirst)
		AddRemoteCtrl = wx.CheckBox(dialog, -1, text.addremote)
		AddRemoteCtrl.SetValue(addremote)
		AddRepeatCtrl = wx.CheckBox(dialog, -1, text.addrepeat)
		AddRepeatCtrl.SetValue(addrepeat)
		EnduringCtrl = wx.CheckBox(dialog, -1, text.enduring)
		EnduringCtrl.SetValue(enduring)
		IgnoreTimeText = wx.StaticText(dialog, -1, text.ignoretime)
		IgnoreTimeCtrl = eg.SpinIntCtrl(dialog, -1, ignoretime, max=60000)

		IgnoreBox = wx.BoxSizer()
		IgnoreBox.Add(IgnoreTimeCtrl, 0, wx.ALL, 2)
		IgnoreBox.Add(IgnoreTimeText, 0, wx.ALL, 5)


		
		BoxSizer = wx.BoxSizer(wx.VERTICAL)
		BoxSizer.Add(OnlyFirstCtrl, 0, wx.ALL, 5)
		BoxSizer.Add(AddRemoteCtrl, 0, wx.ALL, 5)
		BoxSizer.Add(AddRepeatCtrl, 0, wx.ALL, 5)
		#BoxSizer.Add(IgnoreTimeText, 0, wx.ALL, 5)
		#BoxSizer.Add(IgnoreTimeCtrl, 0, wx.ALL, 5)
		BoxSizer.Add(IgnoreBox, 0, wx.ALL, 3)
		#BoxSizer.Add(EnduringCtrl, 0, wx.ALL, 5)

		dialog.sizer.Add(TitleText, 0, wx.EXPAND)
		#dialog.sizer.Add(HostSizer, 0,)
		dialog.sizer.Add(shbSizer, 0, wx.EXPAND)
		dialog.sizer.Add(BoxSizer, 0,)
		EnduringBox = wx.BoxSizer()
		EnduringBox.Add(EnduringCtrl, 0, wx.ALL, 5)
		dialog.sizer.Add(EnduringBox, 0, wx.EXPAND|wx.UP, 15)

		
		if dialog.AffirmedShowModal():
		    return (
				HostCtrl.GetValue(), 
				PortCtrl.GetValue(), 
				OnlyFirstCtrl.GetValue(), 
				AddRemoteCtrl.GetValue(), 
				AddRepeatCtrl.GetValue(), 
				EnduringCtrl.GetValue(),
				IgnoreTimeCtrl.GetValue()
		    )
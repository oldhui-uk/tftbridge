#
#BigTreeTech TFT35 bridge
#
#Author: K. Hui
#
import serial
import threading

class TftBridge:
	def __init__(self,config):
		self.printer = config.get_printer()
		#
		#get config
		#
		self.tftDevice = config.get('tft_device')
		self.tftBaud = config.getint('tft_baud')
		self.tftTimeout = config.getint('tft_timeout')
		self.klipperDevice = config.get('klipper_device')
		self.klipperBaud = config.getint('klipper_baud')
		self.klipperTimeout = config.getint('klipper_timeout')
		#
		#connections to TFT35 and Klipper serial ports
		#
		self.tftSerial = None
		self.klipperSerial = None
        #
        #event to signal stopping threads
        #
        self.stopEvent=theading.Event()
		#
		#register event handlers
		#
		self.printer.register_event_handler("klippy:ready",self.handle_ready)
		self.printer.register_event_handler("klippy:disconnect",self.handle_disconnect)

	#
	#open serial port to device
	#
	def openDevice(self,device,baud,timeout):
		if timeout==0:
			serialPort=serial.Serial(device,baud)
		else:
			serialPort=serial.Serial(device,baud,timeout=timeout)
		return serialPort

	#
	#event handler when printer is ready
	#
	def handle_ready(self):
		#
		#create connections to devices if needed
		#
		if self.tftSerial==None:
			self.tftSerial=self.openDevice(self.tftDevice,self.tftBaud,self.tftTimeout)
		if self.klipperSerial==None:
			self.klipperSerial=self.openDevice(self.klipperDevice,self.klipperBaud,self.klipperTimeout)
		#
		#create and start threads
		#
		self.stopEvent.clear()
		k2tThread=threading.Thread(target=self.tft2klipper)
		t2kThread=threading.Thread(target=self.klipper2tft)
		k2tThread.start()
		t2kThread.start()

	#
	#forward data from TFT35 to Klipper
	#
	def tft2klipper(self):
		while True:
			#
			#if stopping thread event is set
			#
            if self.stopEvent.is_set():
				self.tftSerial.close()		#close connection to TFT35
				self.tftSerial=None			#clear property
                break
			#
			#otherwise read from TFT35 and forward to Klipper
			#
			if self.tftSerial!=None and self.klipperSerial!=None:
				line=self.tftSerial.readline()
				if line!='':			#if readline timeout, it returns an empty str
					self.klipperSerial.write(line)

	#
	#forward data from Klipper to TFT35
	#
	def klipper2tft(self):
		while True:
			#
			#if stopping thread event is set
			#
            if self.stopEvent.is_set():
				self.klipperSerial.close()		#close connection to Klipper
				self.klipperSerial=None			#clear property
                break
			#
			#otherwise read from Klipper and forward to TFT35
			#
			if self.tftSerial!=None and self.klipperSerial!=None:
				line=self.klipperSerial.readline()
				if line!='':		#if readline timeout, it returns an empty str
					self.tftSerial.write(line)

	#
	#event handler when printer is disconnected
	#
	def handle_disconnect(self):
		self.stopEvent.set()	#signal threads to stop

#
#config loading function of add-on
#
def load_config(config):
	return TftBridge(config)

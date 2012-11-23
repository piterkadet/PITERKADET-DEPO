# -*- coding: utf-8 -*-

from Plugins.Plugin import PluginDescriptor
from enigma import iPlayableService, eTimer, eServiceCenter, iServiceInformation, eServiceReference, evfd, eDVBVolumecontrol
from Components.ActionMap import ActionMap
from Components.ServiceEventTracker import ServiceEventTracker
from Components.config import config, ConfigSubsection, getConfigListEntry, ConfigSelection
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Screens.Screen import Screen
from ServiceReference import ServiceReference


#from Plugins.Plugin import PluginDescriptor
##from Components.Converter.ServiceName import ServiceName
#import ServiceReference
#from enigma import iPlayableService, eTimer, eServiceCenter, iServiceInformation, eServiceReference, evfd, eDVBVolumecontrol
#from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
#from Components.ActionMap import ActionMap
#from Screens.Screen import Screen
from Components.Label import Label
#from Components.config import config, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigText
#from Components.ConfigList import ConfigListScreen

import time
from time import time,localtime,strftime

import os
import Screens.Standby

config.vfdicon = ConfigSubsection()
config.vfdicon.displayshow = ConfigSelection(default = "channel", choices = [
		("channel", _("channel")), ("channel number", _("channel number")), ("clock", _("clock")), ("blank", _("blank")) ])

class ConfigVFDDisplay(Screen, ConfigListScreen):
	skin = """
<screen name="ConfigVFDDisplay" position="center,180" size="500,200" title="VFD display configuration">
	<eLabel position="5,0" size="490,2" backgroundColor="#aaaaaa" />
<widget name="config" position="30,20" size="460,50" zPosition="1" scrollbarMode="showOnDemand" />
	<ePixmap position="85,180" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/VFD-Icons/images/red.png" transparent="1" alphatest="on" />
	<ePixmap position="255,180" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/VFD-Icons/images/green.png" transparent="1" alphatest="on" />
	<widget name="key_red" position="85,150" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget name="key_green" position="255,150" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""
	
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		global displayshow
		displayshow = ConfigSelection(default = "channel", choices = [
		("channel", _("Название канала ")), ("channel number", _("Номер канала ")), ("clock", _("Большие часы ")), ("blank", _("Ничего не отображать ")) ])
		self.Clist = []
		self.Clist.append(getConfigListEntry(_("Отображать на дисплее"), displayshow))
		self.Load_settings()
		ConfigListScreen.__init__(self, self.Clist)
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.ok,
				"left": self.left,
				"right": self.right,
				"green": self.ok,
				"red": self.cancel,
			}, -2)
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Ok"))
		self.onLayoutFinish.append(self.layoutFinished)
	
	def Load_settings(self):
		global displayshow
		try:
			displayshow.value = config.vfdicon.displayshow.value
		except:
			pass
	
	def left(self):
		ConfigListScreen.keyLeft(self)
	
	def right(self):
		ConfigListScreen.keyRight(self)
	
	def cancel(self):
		self.showVFD()
		self.close()
	
	def ok(self):
		self.Save_settings()
		self.showVFD()
		self.close()
	
	def Save_settings(self):
		global displayshow
		config.vfdicon.displayshow.value = displayshow.value
		config.vfdicon.save()
	
	def layoutFinished(self):
		self["config"].l.setList(self.Clist)
	
	def showVFD(self):
		global VFDIconsInstance
		VFDIconsInstance = VFDIcons(self.session)
		if config.vfdicon.displayshow.value == "clock":
			VFDIconsInstance.startTimer()
			VFDIconsInstance.timerEvent()
		else:
			VFDIconsInstance.writeChannelName()

def mainB(session, **kwargs):
		session.open(ConfigVFDDisplay)
		evfd.getInstance().vfd_write_string( "VFD SETUP" )
def VFDdisplay(menuid, **kwargs):
	if menuid == "system":
		return [("Настройка дисплея", mainB, "vfd_display", 44)]
	else:
		return []

class VFDIcons:
	def __init__(self, session):
		self.pclock = 1
		self.list = []
		self.getList()
		self.session = session
		self.service = None
		self.onClose = [ ]
		self.__event_tracker = ServiceEventTracker(screen=self,eventmap=
			{
				iPlayableService.evUpdatedInfo: self.__evUpdatedInfo,
				iPlayableService.evUpdatedEventInfo: self.__evUpdatedEventInfo,
				iPlayableService.evVideoSizeChanged: self.__evVideoSizeChanged,
				iPlayableService.evSeekableStatusChanged: self.__evSeekableStatusChanged,
				iPlayableService.evStart: self.__evStart,
				iPlayableService.evTunedIn: self.__evTunedIn,
				iPlayableService.evTuneFailed: self.__evTuneFailed
			})
		session.nav.record_event.append(self.gotRecordEvent)
		self.mp3Available = False
		self.dolbyAvailable = False
		self.ac3Available = False
                self.timer = eTimer()
                self.timer.callback.append(self.handleTimer)
                self.timer.start(1000, False)
                self.clock = 0
                self.hddCheckCounter = 30
                self.hddUsed = 10 # initialize with an invalid value
		self.trig = 1
		self.stendby = 0
		self.isMuted = 0
		self.usb = 0
		self.a = ""
		self.contrastsleep = 7
		self.contrastsleep = 2
		#evfd.getInstance().vfd_set_icon(0x13,1)
		evfd.getInstance().vfd_clear_icons()
		if os.path.exists("/usr/lib/enigma2/python/Plugins/SystemPlugins/VFD-Icons/vfd.conf") == True:
			with open('/usr/lib/enigma2/python/Plugins/SystemPlugins/VFD-Icons/vfd.conf', 'r') as f:
				self.contrast = int(f.read(1))
				f.closed
				evfd.getInstance().vfd_set_brightness(self.contrast)
	
	def __evStart(self):
		print "[__evStart]"
		self.__evSeekableStatusChanged()
	
	def hotplug(self, dev, media_state):
		if media_state == "add":
			self.usb = 1
			evfd.getInstance().vfd_set_icon(0x0D,1)
		else:
			self.usb = 0;
			evfd.getInstance().vfd_set_icon(0x0D,0)
		
	def __evTunedIn(self):
		evfd.getInstance().vfd_set_icon(0x2c,1)
	
	def __evTuneFailed(self):
		evfd.getInstance().vfd_set_icon(0x1D,0)
		evfd.getInstance().vfd_set_icon(0x1A,0)
		evfd.getInstance().vfd_set_icon(0x0A,0)
		evfd.getInstance().vfd_set_icon(0x19,0)
		evfd.getInstance().vfd_set_icon(0x2b,0)
		evfd.getInstance().vfd_set_icon(0x0E,0)
		evfd.getInstance().vfd_set_icon(0x2c,0)
	
	def displayHddUsed(self):
		# determine the HDD usage
		f = os.statvfs("/hdd")
		
		#there are 8 HDD segments in the VFD
		used = (f.f_blocks - f.f_bavail) * 8 / f.f_blocks
		if self.hddUsed != used:
			try:
				if self.hddUsed > used:
					#evfd.getInstance().vfd_set_hdd(0,1)
					evfd.getInstance().vfd_set_icon(0x1e,1)
					if used >= 1:
						evfd.getInstance().vfd_set_icon(0x18,1)
					else:
						evfd.getInstance().vfd_set_icon(0x18,0)
					if used >= 2:
						evfd.getInstance().vfd_set_icon(0x17,1)
					else:
						evfd.getInstance().vfd_set_icon(0x17,0)
					if used >= 3:
						evfd.getInstance().vfd_set_icon(0x15,1)
					else:
						evfd.getInstance().vfd_set_icon(0x15,0)
					if used >= 4:
						evfd.getInstance().vfd_set_icon(0x14,1)
					else:
						evfd.getInstance().vfd_set_icon(0x14,0)
					if used >= 5:
						evfd.getInstance().vfd_set_icon(0x13,1)
					else:
						evfd.getInstance().vfd_set_icon(0x13,0)
					if used >= 6:
						evfd.getInstance().vfd_set_icon(0x12,1)
					else:
						evfd.getInstance().vfd_set_icon(0x12,0)
					if used >= 7:
						evfd.getInstance().vfd_set_icon(0x11,1)
					else:
						evfd.getInstance().vfd_set_icon(0x11,0)
				#evfd.getInstance().vfd_set_hdd(used,0)
				print "used1", used
				
				if used == 8:
					evfd.getInstance().vfd_set_icon(0x16,1)
			
			except IOError,e:
				self.hddUsed = used # dummy operation
		self.hddUsed = used
		
	def __evUpdatedInfo(self):
		print "[__evUpdatedInfo]"
		if config.vfdicon.displayshow.value != "clock":
			self.checkAudioTracks()
			self.writeChannelName()
			self.showCrypted()
			self.showDolby()
			self.showAc3()
			self.showMp3()
	
	def handleTimer(self):
		clock = localtime(time());
		if clock != self.clock:
			self.clock = clock
			try:
				if config.vfdicon.displayshow.value == "clock":
					tm=localtime()
					servicename = strftime("%H %M %S",tm) 
					evfd.getInstance().vfd_write_string(servicename[0:17])
				#evfd.getInstance().vfd_write_clock(clock.tm_hour,clock.tm_min)
				self.trig = "not self.trig"
#				evfd.getInstance().vfd_set_icon(0x22,self.trig)
			except IOError,e:
				print "VFD: handleTime (clock) ", e
		
		if not Screens.Standby.inStandby:
			if self.stendby:
				self.stendby = 0
				if os.path.exists("/usr/lib/enigma2/python/Plugins/SystemPlugins/VFD-Icons/vfd.conf") == True:
					with open('/usr/lib/enigma2/python/Plugins/SystemPlugins/VFD-Icons/vfd.conf', 'r') as f:
						self.contrast = int(f.read(1))
						f.closed
						evfd.getInstance().vfd_set_brightness(self.contrast)
				print "self.contrast", self.contrast
				evfd.getInstance().vfd_set_icon(0x10,0)
				evfd.getInstance().vfd_set_icon(0x24,0)
				evfd.getInstance().vfd_set_icon(0x0D,self.usb)
				
			if self.isMuted != eDVBVolumecontrol.getInstance().isMuted():
				self.isMuted = eDVBVolumecontrol.getInstance().isMuted()
				evfd.getInstance().vfd_set_icon(0x08,self.isMuted)
				
#			if self.hddCheckCounter < 30:
#				self.hddCheckCounter += 1
#			else:
#				self.hddCheckCounter = 0
				#self.displayHddUsed()
		else:
			if not self.stendby:
				if os.path.exists("/usr/lib/enigma2/python/Plugins/SystemPlugins/VFD-Icons/vfd.conf") == True:
					with open('/usr/lib/enigma2/python/Plugins/SystemPlugins/VFD-Icons/vfd.conf', 'r') as f:
						f.seek(1)
						self.contrastsleep = int(f.read(1))
						f.closed
						evfd.getInstance().vfd_set_brightness(self.contrastsleep)
				self.hddUsed = 10
				self.hddCheckCounter = 30
				self.stendby = 1
				print "self.contrastsleep", self.contrastsleep
				self.a = ""
				evfd.getInstance().vfd_clear_string()
				evfd.getInstance().vfd_clear_icons()
				evfd.getInstance().vfd_set_icon(0x24,1)
	
	def writeChannelName(self):
		if config.vfdicon.displayshow.value == "clock":
			return

		service = self.session.nav.getCurrentService()
		if service is not None:
			print "[writeVFDDisplay]"
			# show blank
			servicename = "        "
			audio = service.audioTracks()
			if audio: # show the mp3 tag
				n = audio.getNumberOfTracks()
				for x in range(n):
					i = audio.getTrackInfo(x)
					description = i.getDescription();
					if description.find("MP3") != -1:
							servicename = service.info().getInfoString(iServiceInformation.sTagTitle)
					elif config.vfdicon.displayshow.value == "channel number":
						try: # show the service channel number
							servicename = str(self.session.nav.getCurrentlyPlayingServiceReference(False).getChannelNum())
						except:
							servicename = "        "
							print "[VFD Display] ERROR set channel number"
					elif config.vfdicon.displayshow.value == "channel":
						try: # show the service name
							servicename = ServiceReference(self.session.nav.getCurrentlyPlayingServiceReference(False)).getServiceName()
						except:
							servicename = "        "
							print "[VFD Display] ERROR set service name"
			if self.a != servicename:
				self.a = servicename
				print "vfd display text:", servicename[0:20]
				evfd.getInstance().vfd_write_string(servicename[0:20])
				print "vfd-ok"
			#else:
			#	self.a = ""
		return 0
	
	def showCrypted(self):
		print "[showCrypted]"
		service=self.session.nav.getCurrentService()
		if service is not None:
			info=service.info()
			crypted = info and info.getInfo(iServiceInformation.sIsCrypted) or -1
			if crypted == 1 : #set crypt symbol
				evfd.getInstance().vfd_set_icon(0x1d,1)
			else:
				evfd.getInstance().vfd_set_icon(0x1d,0)
	
	def checkAudioTracks(self):
		self.dolbyAvailable = False
		self.mp3Available = False
		self.ac3Available = False
		service=self.session.nav.getCurrentService()
		if service is not None:
			audio = service.audioTracks()
			if audio:
				n = audio.getNumberOfTracks()
				for x in range(n):
					i = audio.getTrackInfo(x)
					description = i.getDescription();
					if description.find("MP3") != -1:
						self.mp3Available = True
					if description.find("AC3") != -1:
						self.ac3Available = True
					if description.find("DTS") != -1:
						self.dolbyAvailable = True
	
	def showAc3(self):
		print "[showAc3]"
		if self.ac3Available:
			evfd.getInstance().vfd_set_icon(0x1A,1)
		else:
			evfd.getInstance().vfd_set_icon(0x1A,0)
		
	def showDolby(self):
		print "[showDolby]"
		if self.dolbyAvailable:
			evfd.getInstance().vfd_set_icon(0x0A,1)
		else:
			evfd.getInstance().vfd_set_icon(0x0A,0)
		
	def showMp3(self):
		print "[showMp3]"
		if self.mp3Available:
			evfd.getInstance().vfd_set_icon(0x19,1)
		else:
			evfd.getInstance().vfd_set_icon(0x19,0)
		
	def __evUpdatedEventInfo(self):
		print "[__evUpdatedEventInfo]"
		
	def getSeekState(self):
		service = self.session.nav.getCurrentService()
		if service is None:
			return False
		seek = service.seek()
		if seek is None:
			return False
		return seek.isCurrentlySeekable()
	
	def __evSeekableStatusChanged(self):
		print "[__evSeekableStatusChanged]"
		if self.getSeekState():
			evfd.getInstance().vfd_set_icon(0x2b,1)
		else:
			evfd.getInstance().vfd_set_icon(0x2b,0)
	
	def __evVideoSizeChanged(self):
		print "[__evVideoSizeChanged]"
		service=self.session.nav.getCurrentService()
		if service is not None:
			info=service.info()
			height = info and info.getInfo(iServiceInformation.sVideoHeight) or -1
			if height > 576 : #set HD symbol
				evfd.getInstance().vfd_set_icon(0x0e,1)
			else:
				evfd.getInstance().vfd_set_icon(0x0e,0)
	
	def gotRecordEvent(self, service, event):
		recs = self.session.nav.getRecordings()
		nrecs = len(recs)
		if nrecs > 0: #set rec symbol
			evfd.getInstance().vfd_set_icon(0x07,1)
		else:
			evfd.getInstance().vfd_set_icon(0x07,0)
	
	def getServiceNumber(self, name):
		if name in self.list:
			for idx in range(1, len(self.list)):
				if name == self.list[idx-1]:
					return str(idx)
		else:
			return ""
	
	def getList(self):
		print "VFDIcons getList"
		self.pclock = 0
		#serviceHandler = eServiceCenter.getInstance()
		#services = serviceHandler.list(eServiceReference('1:134:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 195) || (type == 25) FROM BOUQUET "bouquets.tv" ORDER BY bouquet'))
		#bouquets = services and services.getContent("SN", True)
		#for bouquet in bouquets:
		#	services = serviceHandler.list(eServiceReference(bouquet[0]))
		#	channels = services and services.getContent("SN", True)
		#	for channel in channels:
		#		if not channel[0].startswith("1:64:"): # Ignore marker
		#			self.list.append(channel[1].replace('\xc2\x86', '').replace('\xc2\x87', ''))
	
	def startTimer(self):
		print "VFDIcons startTimer"
	
	def StopTimer(self, result):
		if result:
			self.timer.stop()
			self.service = None
	
	def timerEvent(self):
		self.pclock = 1
		print "VFDIcons timerEvent"
	
	def shutdown(self):
		print "VFDIcons shutdown"
		self.abort()
	
	def abort(self):
		print "VFDIcons aborting"

VFDIconsInstance = None

def main(session, **kwargs):
	global VFDIconsInstance
	if VFDIconsInstance is None:
		VFDIconsInstance = VFDIcons(session)
	VFDIconsInstance.startTimer()
	VFDIconsInstance.timerEvent()

def Plugins(**kwargs):
	return [
	PluginDescriptor(name="VFDdisplay", description="VFD Display config 17-06-2012", where = PluginDescriptor.WHERE_MENU, fnc=VFDdisplay),
	PluginDescriptor(name="VFDIcons", description="Icons in VFD", where = PluginDescriptor.WHERE_SESSIONSTART, fnc=main ) ]

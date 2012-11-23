# DiskInfo by 2boom mod Ligioner
# <widget source="session.CurrentService" render="Label" position="189,397" zPosition="4" size="350,20" noWrap="1" valign="center" halign="center" font="Regular;14" foregroundColor="clText" transparent="1"  backgroundColor="#20002450">
#	<convert type="HardDiskInfo">xALL</convert>
# </widget>			

from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
import os

class HardDiskInfo(Converter, object):
	xSIZE = 0
	xUSED = 1
	xFREE = 2
	xUINP = 3
	xDEV = 4
	xALL = 5
	
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = {
				"xSIZE": (self.xSIZE),
				"xUSED": (self.xUSED),
				"xFREE": (self.xFREE),
				"xUINP": (self.xUINP),
				"xDEV": (self.xDEV),
				"xALL": (self.xALL),
			}[type]
			
	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		try:
			dfread = os.popen("df -h | grep /media/hdd")
		except:
			return None

		if dfread is not None:
		        info = "No hdd"
			for line in dfread:			
				if self.type == self.xSIZE:
					try:
						info = line.split()[0]
					except:
						return None
				elif self.type == self.xUSED:
					try:
						info = line.split()[1]
					except:
						return None
				elif self.type == self.xFREE:
					try:
						info = line.split()[2]
					except:
						return None
				elif self.type == self.xUINP:
					try:
						info = line.split()[3]
					except:
						return None
				if self.type == self.xDEV:
					try:
						info = line.split()[4]
					except:
						return None                                                					
				elif self.type == self.xALL:
					try:
						info = "dev: %s  size: %s  used: %s  free: %s  uinp: %s" % (line.split()[4], line.split()[0], line.split()[1], line.split()[2], line.split()[3])
					except:
						return None
			return info
		else:
			return ""

	text = property(getText)

#	def changed(self, what):
#		Converter.changed(self, what)

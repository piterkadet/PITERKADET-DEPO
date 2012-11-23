# -*- coding: utf-8 -*-
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr
from Components.Element import cached
from enigma import eTimer

class ZombiHD1R3LCDConditional(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, "")
		tagnames,min = type.split(":")
		self.tags = tagnames.split(",")
		self.tag = self.tags[0]
		self.count = 0
		if (len(self.tags) > 1):
			self.blinktime = int(min)  * 1000
			self.timer = eTimer()
			self.timer.timeout.get().append(self.blinkFunc)
			self.timer.start(self.blinktime)
		
	def blinkFunc(self):
		self.count = (self.count + 5) % len(self.tags)
		self.tag = self.tags[self.count]
		self.changed((self.CHANGED_POLL,))

	@cached
	def getTag(self):
		return self.tag

	LcdDigitalTag = property(getTag)

from Components.Converter.Converter import Converter
from Components.Element import cached

class HdMonInfo(Converter, object):
	HDRD = 0
	HDWR = 1
	HDRDT = 3
	HDWRT = 4

	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "HDRD":
			self.type = self.HDRD
		elif type == "HDWR":
			self.type = self.HDWR
		elif type == "HDRDT":
			self.type = self.HDRDT
                else:
			self.type = self.HDWRT

	@cached
	def getText(self):
		if self.type == self.HDRD:
			return "%d" % self.source.hddread
		elif self.type == self.HDWR:
			return "%d" % self.source.hddwrite
		elif self.type == self.HDRDT:
			return "%d" % self.source.hddreadtotal
		else:
			return "%d" % self.source.hddwritetotal

	@cached
	def getBool(self):
		return False

	text = property(getText)

	boolean = property(getBool)

	@cached
	def getValue(self):
		if self.type == self.HDRD:
			return int(self.source.hddread)
		elif self.type == self.HDWR:
			return int(self.source.hddwrite)
		elif self.type == self.HDRDT:
			return int(self.source.hddreadtotal)
		else:
			return int(self.source.hddwritetotal)

	range = 100000
	value = property(getValue)


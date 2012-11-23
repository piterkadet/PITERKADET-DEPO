from Components.Converter.Converter import Converter
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, resolveFilename
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr
from enigma import ePixmap, eEnv
from Components.Element import cached
from Components.config import config

class ZombiHD1R3LCDDigital(Converter, object):
	searchPaths = (eEnv.resolve('${datadir}/enigma2/%s/'),
				'/media/cf/%s/',
				'/media/usb/%s/')

	def __init__(self):
		Renderer.__init__(self)
		self.path = "picon"
		self.nameCache = { }
		self.pngname = ""		
			
	def __init__(self, type):
		Converter.__init__(self, "")
		self.tag,self.path,cut = type.split(":")
		self.cut = cut == "cut"
				
	@cached
	def getText(self):
		text = self.source.source.text
		if self.cut:
			text = text
		return text
			
		
	text = property(getText)			

	def changed(self, what):
		Converter.changed(self, what)
		tag = self.source.LcdDigitalTag
		if ((self.tag == "logo") or (self.tag == "nologo")):
			if ((tag == "logo") and (self.calcVisibility())):
				tag = "nologo"
		bool = (self.tag == tag)
		for x in self.downstream_elements:
			x.visible = bool

	def calcVisibility(self):
		pngname = ""
		sname = self.source.source.text
		if pngname == "":
			pngname = self.findPicon(sname)
		return pngname == ""

	def findPicon(self, serviceName):
		for path in self.searchPaths:
			pngname = (path % self.path) + serviceName + ".png"
			if fileExists(pngname):
				return pngname
		return ""

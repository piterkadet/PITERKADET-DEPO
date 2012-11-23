#######################################################################
#
#    Converter for Enigma2
#    Coded by shamann (c)2011
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#######################################################################

from Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from enigma import eServiceReference
from Components.config import config

class g16RefTV(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.nameCache = { }
		self.pngname = ""

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				service = self.source.service
				marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
				bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
				if marker:
					pngname = self.nameCache.get("marker", "")
					if pngname == "":
						tmp = resolveFilename(SCOPE_CURRENT_SKIN, "marker.png")
						if fileExists(tmp):
							pngname = tmp
						else:
							pngname = resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/picon_default.png")
						self.nameCache["marker"] = pngname
				elif bouquet:
					pngname = self.nameCache.get("bouquet", "")
					if pngname == "":
						tmp = resolveFilename(SCOPE_CURRENT_SKIN, "bouquet.png")
						if fileExists(tmp):
							pngname = tmp
						else:
							pngname = resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/picon_default.png")
						self.nameCache["bouquet"] = pngname
				else:
					sname = service.toString()
					pos = sname.rfind(':')
					if pos != -1:
						sname = sname[:pos].rstrip(':').replace(':','_')
					pngname = self.nameCache.get(sname, "")
					if pngname == "":
						pngname = self.findPicon(sname)
						if pngname != "":
							self.nameCache[sname] = pngname
			if pngname == "":
				pngname = self.nameCache.get("default", "")
				if pngname == "":
					pngname = self.findPicon("picon_default")
					if pngname == "":
						tmp = resolveFilename(SCOPE_CURRENT_SKIN, "picon_default.png")
						if fileExists(tmp):
							pngname = tmp
						else:
							pngname = resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/picon_default.png")
					self.nameCache["default"] = pngname
			if self.pngname != pngname:
				self.pngname = pngname
				self.instance.setPixmapFromFile(self.pngname)
            		
	def findPicon(self, serviceName):
		try:
			pngname = config.plugins.setupGlass16.par39.value + "/picon/" + serviceName + ".png"
			if fileExists(pngname):
				return pngname
		except: pass
		return ""

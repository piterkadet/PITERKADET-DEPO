#######################################################################
#
#    Renderer for Enigma2
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
from enigma import eLabel
from Components.VariableText import VariableText
from enigma import eServiceReference

class g16ShowReference(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if self.instance:
			if what[0] == self.CHANGED_CLEAR:
				self.text = "Reference not found !"
			else:
				service = self.source.service
				marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
				bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
				sname = service.toString()
				if marker or bouquet:
					self.text = "Reference: X:X:X:XXXX:XXX:X:XXXXXX:X:X:X"
				else:
					pos = sname.rfind(':')
					if pos != -1:
						sname = sname[:pos].rstrip(':')
						if not "::" in sname:
							self.text = "Reference: " + sname
						else:
							self.text = "Reference: X:X:X:XXXX:XXX:X:XXXXXX:X:X:X"
					else:
						self.text = "Reference reading error !"

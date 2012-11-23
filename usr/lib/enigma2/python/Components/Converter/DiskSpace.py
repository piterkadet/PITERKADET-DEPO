#
#	DiskSpace
#	by Ismail Demir
#
#######################################################

from Converter import Converter
from os import statvfs

class DiskSpace(Converter, object):
	DEFAULT = 0
	FREE = 1

	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "FREE":
			self.type = self.FREE
		else:
			self.type = self.DEFAULT


	def getText(self):
		stat = statvfs("/hdd")
		hdd = stat.f_bfree * stat.f_bsize

		if self.type == self.FREE:
			if hdd > 1099511627776:
				free = float(hdd/1099511627776.0)
				return "%.2f TB free diskspace" % free
			elif hdd > 1073741824:
				free = float(hdd/1073741824.0)
				return "%.2f GB free diskspace" % free
			else:
				float(free = hdd/1048576.0)
				return "%i MB" % free


		elif self.type == self.DEFAULT:
			return "%d MB free diskspace" % (free/1000/1000)
		else:
			return "???"
			
	text = property(getText)

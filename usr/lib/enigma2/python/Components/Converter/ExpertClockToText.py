#
#	Expert RemainingToText Converter
#	by Ismail Demir
#
#
#	Example usage in the skin.xml:
#
#		<widget source="session.Event_Next" render="Label" position="300,150" size="120,28" font="Regular;24"  >
#			<convert type="EventTime">Duration</convert>
#			<convert type="ExpertClockToText">InMinutes</convert>
#		</widget>
#
#######################################################

from Converter import Converter
from time import localtime, strftime
from Components.Element import cached

class ExpertClockToText(Converter, object):
	DEFAULT = 0
	WITH_SECONDS = 1
	IN_MINUTES = 2
	DATE = 3
	AS_LENGTH = 4
	
	# add: date, date as string, weekday, ... 
	# (whatever you need!)
	
	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "WithSeconds":
			self.type = self.WITH_SECONDS
		elif type == "InMinutes":
			self.type = self.IN_MINUTES
		elif type == "Date":
			self.type = self.DATE
		elif type == "AsLength":
			self.type = self.AS_LENGTH
			self.fmt_string = type[7:]
		else:
			self.type = self.DEFAULT

	@cached
	def getText(self):
		time = self.source.time
		if time is None:
			return ""

		# handle durations
		if self.type == self.IN_MINUTES:
			return "%02d:%02d" % (time / 3600, (time / 60) - ((time / 3600) * 60))
		elif self.type == self.AS_LENGTH:
			return "%d:%02d" % (time / 60, time % 60)
		
		t = localtime(time)
		
		if self.type == self.WITH_SECONDS:
			return "%02d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec)
		elif self.type == self.DEFAULT:
			return "%02d:%02d" % (t.tm_hour, t.tm_min)
		elif self.type == self.DATE:
			return "%s %s %d, %d" %(_(dayStr[t.tm_wday]), _(monthStr[t.tm_mon-1]), t.tm_mday, t.tm_year)
		else:
			return "???"

	text = property(getText)

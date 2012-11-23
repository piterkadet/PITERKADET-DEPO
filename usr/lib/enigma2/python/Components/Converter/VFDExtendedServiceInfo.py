##
## Extended Service-Info Converter
## by AliAbdul
##
## Example usage in the skin.xml:
##		<widget source="session.CurrentService" render="Label" position="164,435" size="390,28" font="Regular;26" transparent="1" >
##			<convert type="VFDExtendedServiceInfo">Config</convert>
##		</widget>
##
## Known issues with the ServiceNumber Converter:
## If you have one service in different bouquets the first index of the service will be taken
## If you rename, move, delete or add a channel the numbers will not be OK any more. You have to restart E2 then
##
from Components.config import config
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr, eServiceReference, eServiceCenter, eTimer
from xml.etree.cElementTree import parse

##########################################################################

class VFDExtendedServiceInfo(Converter, object):
	SERVICENAME = 0
	SERVICENUMBER = 1
	ORBITALPOSITION = 2
	SATNAME = 3
	PROVIDER = 4
	FROMCONFIG = 5
	ALL = 6

	def __init__(self, type):
		Converter.__init__(self, type)
		self.satNames = {}
		self.readSatXml()
		self.getLists()
		
		if type == "ServiceName":
			self.type = self.SERVICENAME
		elif type == "ServiceNumber":
			self.type = self.SERVICENUMBER
		elif type == "OrbitalPosition":
			self.type = self.ORBITALPOSITION
		elif type == "SatName":
			self.type = self.SATNAME
		elif type == "Provider":
			self.type = self.PROVIDER
		elif type == "Config":
			self.type = self.FROMCONFIG
		else:
			self.type = self.ALL
			
		self.what = self.tpdata = None
		self.Timer = eTimer()
		self.Timer.callback.append(self.neededChange)
			

	@cached
	def getText(self):
		service = self.source.service
		if isinstance(service, iPlayableServicePtr):
			info = service and service.info()
			ref = None
		else: # reference
			info = service and self.source.info
			ref = service
		if info is None: return ""
		
		text = ""
		if config.plugins.VFDExtendedServiceInfo.showServiceNumber.value == True:
			try:
				service = self.source.serviceref
				num = service and service.getChannelNum() or None
			except:
				num = None
			if num:
				number = str(num)
			else:
				num, bouq = self.getServiceNumber(ref or eServiceReference(info.getInfoString(iServiceInformation.sServiceref)))
				number = num and str(num) or ''
		else:
			number =""
		name = info.getName().replace('\xc2\x86', '').replace('\xc2\x87', '')
		#number = self.getServiceNumber(name, info.getInfoString(iServiceInformation.sServiceref))
		orbital = self.getOrbitalPosition(info)
		satName = self.satNames.get(orbital, orbital)
		
		if self.type == self.SERVICENAME:
			text = name
		elif self.type == self.SERVICENUMBER:
			text = number
		elif self.type == self.ORBITALPOSITION:
			text = orbital
		elif self.type == self.SATNAME:
			text = satName
		elif self.type == self.PROVIDER:
			text = info.getInfoString(iServiceInformation.sProvider)
		elif self.type == self.FROMCONFIG:
			if config.plugins.VFDExtendedServiceInfo.showServiceNumber.value == True and number != "":
				text = "%s. %s" % (number, name)
			else:
				text = name
			if config.plugins.VFDExtendedServiceInfo.showOrbitalPosition.value == True and orbital != "":
				if config.plugins.VFDExtendedServiceInfo.orbitalPositionType.value == "name":
					text = "%s (%s)" % (text, satName)
				else:
					text = "%s (%s)" % (text, orbital)
		else:
			if number == "":
				text = name
			else:
				text = "%s. %s" % (number, name)
			if orbital != "":
				text = "%s (%s)" % (text, orbital)
		
		return text

	text = property(getText)

	def neededChange(self):
		if self.what:
			Converter.changed(self, self.what)
			self.what = None

	def changed(self, what):
		if what[0] != self.CHANGED_SPECIFIC or what[1] in (iPlayableService.evStart,):
			self.tpdata = None
			if self.type in (self.SERVICENUMBER,self.FROMCONFIG):
				self.what = what
				self.Timer.start(200, True)
			else:
				Converter.changed(self, what)
				
	def getServiceNumber(self, ref):
		def searchHelper(serviceHandler, num, bouquet):
			servicelist = serviceHandler.list(bouquet)
			if not servicelist is None:
				while True:
					s = servicelist.getNext()
					if not s.valid(): break
					if not (s.flags & (eServiceReference.isMarker|eServiceReference.isDirectory)):
						num += 1
						if s == ref: return s, num
			return None, num

		if isinstance(ref, eServiceReference):
			isRadioService = ref.getData(0) in (2,10)
			lastpath = isRadioService and config.radio.lastroot.value or config.tv.lastroot.value
			if lastpath.find('FROM BOUQUET') == -1:
				if 'FROM PROVIDERS' in lastpath:
					return 'P', 'Provider'
				if 'FROM SATELLITES' in lastpath:
					return 'S', 'Satellites'
				if ') ORDER BY name' in lastpath:
					return 'A', 'All Services'
				return 0, 'N/A'
			try:
				acount = config.plugins.NumberZapExt.enable.value and config.plugins.NumberZapExt.acount.value
			except:
				acount = False
			rootstr = ''
			for x in lastpath.split(';'):
				if x != '': rootstr = x
			serviceHandler = eServiceCenter.getInstance()
			if acount is True or not config.usage.multibouquet.value:
				bouquet = eServiceReference(rootstr)
				service, number = searchHelper(serviceHandler, 0, bouquet)
			else:
				if isRadioService:
					bqrootstr = '1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "bouquets.radio" ORDER BY bouquet'
				else:
					bqrootstr = '1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "bouquets.tv" ORDER BY bouquet'
				number = 0
				cur = eServiceReference(rootstr)
				bouquet = eServiceReference(bqrootstr)
				bouquetlist = serviceHandler.list(bouquet)
				if not bouquetlist is None:
					while True:
						bouquet = bouquetlist.getNext()
						if not bouquet.valid(): break
						if bouquet.flags & eServiceReference.isDirectory:
							service, number = searchHelper(serviceHandler, number, bouquet)
							if not service is None and cur == bouquet: break
			if not service is None:
				info = serviceHandler.info(bouquet)
				name = info and info.getName(bouquet) or ''
				return number, name
		return 0, ''

	def getListFromRef(self, ref):
		list = []
		
		serviceHandler = eServiceCenter.getInstance()
		services = serviceHandler.list(ref)
		bouquets = services and services.getContent("SN", True)
		
		for bouquet in bouquets:
			services = serviceHandler.list(eServiceReference(bouquet[0]))
			channels = services and services.getContent("SN", True)
			for channel in channels:
				if not channel[0].startswith("1:64:"): # Ignore marker
					list.append(channel[1].replace('\xc2\x86', '').replace('\xc2\x87', ''))
		
		return list

	def getLists(self):
		self.tv_list = self.getListFromRef(eServiceReference('1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 195) || (type == 25) FROM BOUQUET "bouquets.tv" ORDER BY bouquet'))
		self.radio_list = self.getListFromRef(eServiceReference('1:7:2:0:0:0:0:0:0:0:(type == 2) FROM BOUQUET "bouquets.radio" ORDER BY bouquet'))

	def readSatXml(self):
		satXml = parse("/etc/tuxbox/satellites.xml").getroot()
		if satXml is not None:
			for sat in satXml.findall("sat"):
				name = sat.get("name") or None
				position = sat.get("position") or None
				if name is not None and position is not None:
					position = "%s.%s" % (position[:-1], position[-1:])
					if position.startswith("-"):
						position = "%sW" % position[1:]
					else:
						position = "%sE" % position
					if position.startswith("."):
						position = "0%s" % position
					self.satNames[position] = name
					

	def getServiceNumber1(self, name, ref):
		list = []
		if ref.startswith("1:0:2"):
			list = self.radio_list
		elif ref.startswith("1:0:1"):
			list = self.tv_list
		number = ""
		if name in list:
			for idx in range(1, len(list)):
				if name == list[idx-1]:
					number = str(idx)
					break
		return number

	def getOrbitalPosition(self, info):
		transponderData = info.getInfoObject(iServiceInformation.sTransponderData)
		orbital = 0
		if transponderData is not None:
			if isinstance(transponderData, float):
				return ""
			if transponderData.has_key("tuner_type"):
				if (transponderData["tuner_type"] == "DVB-S") or (transponderData["tuner_type"] == "DVB-S2"):
					orbital = transponderData["orbital_position"]
					orbital = int(orbital)
					if orbital > 1800:
						orbital = str((float(3600 - orbital))/10.0) + "W"
					else:
						orbital = str((float(orbital))/10.0) + "E"
					return orbital
		return ""

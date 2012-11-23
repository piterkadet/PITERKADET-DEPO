from enigma import iPlayableService
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr
from Components.config import config



class ExpertInfo(Converter, object):
	CLIENT_INFO = 0
	SERVER_INFO = 1	
	CRYPT_INFO = 3
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = {
				"Client": self.CLIENT_INFO,
				"Server": self.SERVER_INFO,				
				"CryptInfo": self.CRYPT_INFO,
			}[type]
		self.hook_elements = {
				self.CLIENT_INFO: [iPlayableService.evVideoSizeChanged],
				self.SERVER_INFO: [iPlayableService.evVideoSizeChanged],				
				self.CRYPT_INFO: [iPlayableService.evVideoSizeChanged],
			}[self.type]

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""
		Ret_Text = ""
		if ((self.type == self.CLIENT_INFO) and ((config.usage.setup_level.value == "expert") or (config.usage.setup_level.value == "intermediate"))):
			Client_Line = ""
			try:
				f = open("/var/etc/client", "r")
				Client_Line = f.read()
				f.close()
			except:
				Client_Line ="none"

			return Client_Line

		elif ((self.type == self.SERVER_INFO) and ((config.usage.setup_level.value == "expert") or (config.usage.setup_level.value == "intermediate"))):
			Server_Line = ""
			try:
				f = open("/var/etc/server", "r")
				Server_Line = f.read()
				f.close()
			except:
				Server_Line ="none"
			return Server_Line			

		elif ((self.type == self.CRYPT_INFO) and (config.usage.setup_level.value == "expert")):  
			id_ecm = "" 
			caID = ""
			syID = ""
			try:
				f = open("/tmp/pid.info", "r")
				flines = f.readlines()
				f.close()
				for cell in flines:
					cellmembers = cell.split()
					for x in range(len(cellmembers)):
							if ("ECM" in cellmembers[x]):
								if x<=(len(cellmembers)):
									caID = cellmembers[x+3] # detekcja 0100,1801 ...
									caID = caID .lstrip("0x")
									caID = caID.strip(",;.:-*_<>()[]{}")
									if (len(caID)<4):
										caID = "0" + caID
									if ((caID>="0100") and (caID<="01FF")):
										syID="S:"
									elif((caID>="1800") and (caID<="18FF")):
										syID="N:"
									elif((caID>="0B00") and (caID<="0BFF")):
										syID="Cx:"
									elif((caID>="0600") and (caID<="06FF")):
										syID="I:"
									elif((caID>="0900") and (caID<="09FF")):
										syID="NDS:"
									elif((caID>="0D00") and (caID<="0DFF")):
										syID="CW:"
									elif((caID>="1700") and (caID<="17FF")):
										syID="B:"									
									elif((caID>="0500") and (caID<="05FF")):
										syID="V:"									
									else:
										syID="X:"
									id_ecm = id_ecm + syID + caID + "  "									
								else:
									id_ecm = ""
			except:
				id_ecm = ""
			return id_ecm	
			
		return ""

	@cached
	def getValue(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return -1
		
	text = property(getText)
	value = property(getValue)






# QuickEcmInfo converter (c) 2boom 2012
#<widget source="session.CurrentService" render="Label" position="462,153" size="50,22" font="Regular; 17" zPosition="2" backgroundColor="background1" foregroundColor="white" transparent="1">
#    <convert type="QuickEcmInfo">ecmfile | emuname | caids</convert>
#  </widget>

from Poll import Poll
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached
from Tools.Directories import fileExists
import os

class QuickEcmInfo(Poll, Converter, object):
	ecmfile = 0
	emuname = 1
	caids = 2
	pids = 3
	vtype = 4
	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "ecmfile":
			self.type = self.ecmfile
		elif type == "emuname":
			self.type = self.emuname
		elif type == "caids":
			self.type = self.caids
		elif type == "pids":
			self.type = self.pids
		elif type == "vtype":
			self.type = self.vtype
		self.poll_interval = 1000
		self.poll_enabled = True
		
	def getServiceInfoString(self, info, what, convert = lambda x: "%d" % x):
		v = info.getInfo(what)
		if v == -1:
			return "N/A"
		if v == -2:
			return info.getInfoString(what)
		if v == -3:
			t_objs = info.getInfoObject(what)
			if t_objs and (len(t_objs) > 0):
				ret_val=""
				for t_obj in t_objs:
					ret_val += "%.4X " % t_obj
				return ret_val[:-1]
			else:
				return ""
		return convert(v)
		
	@cached
	def getText(self):
		ecminfo = ""
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""
			
		if self.type == self.vtype:
			try:
				return ("MPEG2", "MPEG4", "MPEG1", "MPEG4-II", "VC1", "VC1-SM", "")[info.getInfo(iServiceInformation.sVideoType)]
			except: 
				return " "
			
		elif self.type == self.ecmfile:
			if self.getServiceInfoString(info, iServiceInformation.sCAIDs):
				if fileExists("/tmp/ecm.info"):
					for line in open("/tmp/ecm.info"):
						ecminfo += line
					
		elif self.type == self.pids:
			try:
				return "SID: %0.4X  VPID: %0.4X  APID: %0.4X  TSID: %0.4X  ONID: %0.4X" % (int(self.getServiceInfoString(info, iServiceInformation.sSID)), int(self.getServiceInfoString(info, iServiceInformation.sVideoPID)), int(self.getServiceInfoString(info, iServiceInformation.sAudioPID)), int(self.getServiceInfoString(info, iServiceInformation.sTSID)), int(self.getServiceInfoString(info, iServiceInformation.sONID)))
			except:
				try:
					return "SID: %0.4X  APID: %0.4X  TSID: %0.4X  ONID: %0.4X" % (int(self.getServiceInfoString(info, iServiceInformation.sSID)), int(self.getServiceInfoString(info, iServiceInformation.sAudioPID)), int(self.getServiceInfoString(info, iServiceInformation.sTSID)), int(self.getServiceInfoString(info, iServiceInformation.sONID)))
				except:
					return " "
			
		elif self.type == self.caids:
			try:
				ecminfo = self.getServiceInfoString(info, iServiceInformation.sCAIDs)
			except:
				ecminfo = " "
					
		if self.type == self.emuname:
			camdlist = None
			serlist = None
			# TS-Panel
			if fileExists("/etc/startcam.sh"):
				try:
					for line in open("/etc/startcam.sh"):
						if line.find("script") > -1:
							return "%s" % line.split("/")[-1].split()[0][:-3]
				except:
					camdlist = None
			# VTI 	
			elif fileExists("/tmp/.emu.info"):
				try:
					camdlist = open("/tmp/.emu.info", "r")
				except:
					camdlist = None
			# BlackHole	
			elif fileExists("/etc/CurrentBhCamName"):
				try:
					camdlist = open("/etc/CurrentBhCamName", "r")
				except:
					camdlist = None
			# Domica	
			elif fileExists("/etc/active_emu.list"):
				try:
					camdlist = open("/etc/active_emu.list", "r")
				except:
					camdlist = None
			#Pli
			elif fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
				try:
					camdlist = os.popen("/etc/init.d/softcam info")
				except:
					camdlist = None
				try:
					serlist = os.popen("/etc/init.d/cardserver info")
				except:
					serlist = None
			# OoZooN
			elif fileExists("/tmp/cam.info"):
				try:
					camdlist = open("/tmp/cam.info", "r")
				except:
					camdlist = None
			# Merlin2	
			elif fileExists("/etc/clist.list"):
				try:
					camdlist = open("/etc/clist.list", "r")
				except:
					camdlist = None
			# GP3
			elif fileExists("/usr/lib/enigma2/python/Plugins/Bp/geminimain/lib/libgeminimain.so"):
				try:
					from Plugins.Bp.geminimain.plugin import GETCAMDLIST
					from Plugins.Bp.geminimain.lib import libgeminimain
					camdl = libgeminimain.getPyList(GETCAMDLIST)
					for x in camdl:
						if x[1] == 1:
							camdlist = x[2] 
				except:
					camdlist = None
			# Unknown emu
			else:
				camdlist = None
				
			if serlist is not None:
				try:
					cardserver = ""
					for current in serlist.readlines():
						cardserver = current
					serlist.close()
				except:
					pass
			else:
				cardserver = ""

			if camdlist is not None:
				try:
					emu = ""
					for current in camdlist.readlines():
						emu = current
					camdlist.close()
				except:
					pass
			else:
				emu = ""
			ecminfo = "%s %s" % (cardserver.split('\n')[0], emu.split('\n')[0])
		return ecminfo
		
	text = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)


# -*- coding: utf-8 -*-
# epg dowloader from linux-sat.tv (exUSSR) c) 2012 2boom
from Components.ActionMap import ActionMap
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Sources.List import List
from Tools.Directories import fileExists
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.ScrollLabel import ScrollLabel
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from os import environ
import os
import gettext
########################################
from enigma import eEPGCache
from types import *
from enigma import *
import sys, traceback
import re
import time
import new
import _enigma
import enigma

global min
min = 0

global status 
if fileExists("/usr/lib/opkg/status"):
	status = "/usr/lib/opkg/status"
elif fileExists("/var/lib/opkg/status"):
	status = "/var/lib/opkg/status"

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("epgdn", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/EPGD/locale/"))

def _(txt):
	t = gettext.dgettext("epgdn", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t
######################################################################################
config.plugins.epgd = ConfigSubsection()
config.plugins.epgd.epgname = ConfigSelection(default = "epg.dat", choices = [
		("epg.dat", "epg.dat"),
		("epg_true.dat", "epg_true.dat"),
		])
config.plugins.epgd.e2shpatch = ConfigSelection(default = "no", choices = [
		("no", _("no")),
		("yes", _("yes")),
		])
config.plugins.epgd.direct = ConfigSelection(default = "/media/usb/", choices = [
		("/media/hdd/", _("/media/hdd/")),
		("/media/usb/", _("/media/usb/")),
		("/usr/share/enigma2/", _("/usr/share/enigma2/")),
])
config.plugins.epgd.auto = ConfigSelection(default = "no", choices = [
		("no", _("no")),
		("yes", _("yes")),
		])
config.plugins.epgd.lang = ConfigSelection(default = "ru", choices = [
		("ru", _("Russian")),
		("ua", _("Ukrainian")),
		])
config.plugins.epgd.timedwn = ConfigClock(default = ((16*60) + 15) * 60) # 18:15
config.plugins.epgd.weekday = ConfigSelection(default = "1", choices = [
		("0", _("Mo")),
		("1", _("Tu")),
		("2", _("We")),
		("3", _("Th")),
		("4", _("Fr")),
		("5", _("Sa")),
		("6", _("Su")),
		])
config.plugins.epgd.autosave = ConfigSelection(default = '0', choices = [
		('0', _("Off")),
		('29', _("30 min")),
		('59', _("60 min")),
		('119', _("120 min")),
		('179', _("180 min")),
		('239', _("240 min")),
		])
config.plugins.epgd.autobackup = ConfigYesNo(default = False)
######################################################################
class epgdn2(ConfigListScreen, Screen):
	skin = """
<screen name="epgdn2" position="center,160" size="850,370" title="EPG from linux-sat.tv (exUSSR)">
  <widget position="15,10" size="820,200" name="config" scrollbarMode="showOnDemand" />
   <ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,358" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,328" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="540,358" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="540,328" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="765,330" size="70,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/info.png" zPosition="2" alphatest="blend" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("EPG from linux-sat.tv (exUSSR)"))
		self.list = []
		self.list.append(getConfigListEntry(_("Select path to save epg.dat"), config.plugins.epgd.direct))
		self.list.append(getConfigListEntry(_("Select EPG filename"), config.plugins.epgd.epgname))
		self.list.append(getConfigListEntry(_("Select EPG language"), config.plugins.epgd.lang))
		self.list.append(getConfigListEntry(_("Patch enigma2.sh (need restart enigma2)"), config.plugins.epgd.e2shpatch))
		self.list.append(getConfigListEntry(_("AutoDownload epg.dat"), config.plugins.epgd.auto))
		self.list.append(getConfigListEntry(_("AutoDownload time"), config.plugins.epgd.timedwn))
		self.list.append(getConfigListEntry(_("AutoDownload weekday"), config.plugins.epgd.weekday))
		self.list.append(getConfigListEntry(_("Automatic save/load EPG"), config.plugins.epgd.autosave))
		self.list.append(getConfigListEntry(_("Autobackup to ../epgtmp.gz"), config.plugins.epgd.autobackup))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Download EPG"))
		self["key_blue"] = StaticText(_("Manual"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.downepg,
			"blue": self.manual,
			"info": self.infoKey,
			"ok": self.save
		}, -2)
	
	def infoKey (self):
		self.session.open(epgdinfo)
	
	def downepg(self):
		if self.ismounted(config.plugins.epgd.direct.value) == 1 or config.plugins.epgd.direct.value == "/usr/share/enigma2/":
			try:
				os.system("wget -q http://linux-sat.tv/epg/epg_%s.dat.gz -O %s%s.gz" % (config.plugins.epgd.lang.value, config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
				if fileExists("%s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value)):
					os.unlink("%s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
					os.system("rm -f %s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
				if not os.path.exists("%sepgtmp" % config.plugins.epgd.direct.value):
					os.system("mkdir -p %sepgtmp" % config.plugins.epgd.direct.value)
				os.system("cp -f %s%s.gz %sepgtmp" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value, config.plugins.epgd.direct.value))
				os.system("gzip -df %s%s.gz" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
				if fileExists("%s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value)):
					os.chmod("%s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value), 0644)
				self.mbox = self.session.open(MessageBox,(_("EPG downloaded")), MessageBox.TYPE_INFO, timeout = 4 )
				epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
				epgcache = eEPGCache.getInstance().load()
			except:
				self.mbox = self.session.open(MessageBox,(_("Sorry, the EPG download error")), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.mbox = self.session.open(MessageBox,(_("EPG save not possible, your device %s is not mounted") % config.plugins.epgd.direct.value), MessageBox.TYPE_INFO, timeout = 4 )

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)

	def save(self):
		config.misc.epgcache_filename.value = ("%s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
		config.misc.epgcache_filename.save()
		config.plugins.epgd.weekday.save()
		config.plugins.epgd.timedwn.save()
		config.plugins.epgd.lang.save()
		config.plugins.epgd.auto.save()
		config.plugins.epgd.epgname.save()
		config.plugins.epgd.direct.save()
		config.plugins.epgd.autosave.save()
		config.plugins.epgd.e2shpatch.save()
		config.plugins.epgd.autobackup.save()
		configfile.save()
		if config.plugins.epgd.e2shpatch.value == "yes":
			os.system("sed -i '/.dat/d' /usr/bin/enigma2.sh")
			os.system("sed -i '3i [ -f %sepgtmp/%s.gz ] && cp -f %sepgtmp/%s.gz %s && gzip -df %s%s.gz' /usr/bin/enigma2.sh" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value, config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value, config.plugins.epgd.direct.value, config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
		else:
			os.system("sed -i '/.dat/d' /usr/bin/enigma2.sh")
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
################################################################################################################
	def manual(self):
		self.session.open(epgdmanual)
################################################################################################################
	def ismounted(self, what):
		for line in open("/proc/mounts"):
			if line.find(what[:-1]) > -1:
				return 1
		return 0
################################################################################################################
class epgdmanual(Screen):
	skin = """
<screen name="epgdmanual" position="center,260" size="850,50" title="EPG from linux-sat.tv (exUSSR)">
  <ePixmap position="10,40" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,10" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,40" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,10" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,40" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,10" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="539,40" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="539,10" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("EPG from linux-sat.tv (exUSSR)"))
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save epg.dat"))
		self["key_yellow"] = StaticText(_("Restore epg.dat"))
		self["key_blue"] = StaticText(_("Reload epg.dat"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.savepg,
			"yellow": self.restepg,
			"blue": self.reload,
		}, -2)
################################################################################################################
	def reload(self):
		try:
			if fileExists("%sepgtmp/%s.gz" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value)):
				os.system("cp -f %sepgtmp/%s.gz %s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value, config.plugins.epgd.direct.value))
				os.system("gzip -df %s%s.gz" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
			os.chmod("%s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value), 0644)
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
			self.mbox = self.session.open(MessageBox,(_("epg.dat reloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("reload epg.dat failed")), MessageBox.TYPE_INFO, timeout = 4 )
################################################################################################################
	def savepg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_save,None,eEPGCache)
		epgcache = eEPGCache.getInstance().save()
		self.mbox = self.session.open(MessageBox,(_("epg.dat saved")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def restepg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
		epgcache = eEPGCache.getInstance().load()
		self.mbox = self.session.open(MessageBox,(_("epg.dat restored")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def cancel(self):
		self.close(False)
##############################################################################
class epgdinfo(Screen):
	skin = """
<screen name="infoepgd" position="center,71" size="750,605" title="EPG downloader from linux-sat.tv (exUSSR)">
  <eLabel position="20,309" size="710,2" backgroundColor="grey" />
  <eLabel position="20,481" size="190,2" backgroundColor="grey" />
  <eLabel position="480,482" size="2,110" backgroundColor="grey" />
  <ePixmap position="20,602" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="20,572" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="528,507" size="180,47" zPosition="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/EPGD/images/2boom.png" alphatest="blend" />
  <widget source="about1" render="Label" position="10,10" size="730,70" font="Regular; 19" valign="top" />
  <widget source="about2" render="Label" position="10,80" size="730,70" font="Regular; 19" valign="top" />
  <widget source="about3" render="Label" position="10,150" size="730,110" font="Regular; 19" valign="top" />
  <widget source="about4" render="Label" position="10,262" size="730,44" font="Regular; 19" valign="top" />
  <widget source="about5" render="Label" position="20,315" size="680,24" font="Regular; 19" valign="top" />
  <widget source="about6" render="Label" position="10,340" size="730,44" font="Regular; 19" valign="top" />
  <widget source="about7" render="Label" position="10,385" size="730,22" font="Regular; 19" valign="top" />
  <widget source="about8" render="Label" position="10,408" size="730,22" font="Regular; 19" valign="top" />
  <widget source="about9" render="Label" position="10,431" size="730,44" font="Regular; 19" valign="top" />
  <widget source="about10" render="Label" position="10,490" size="200,22" font="Regular; 19" valign="top" />
  <widget source="about11" render="Label" position="50,513" size="400,22" font="Regular; 19" valign="top" />
  <widget source="about12" render="Label" position="50,538" size="400,22" font="Regular; 19" valign="top" />
  <widget source="about13" render="Label" position="515,558" size="200,44" font="Regular; 19" valign="top" halign="center" />
  <widget source="ver" render="Label" position="515,483" size="200,22" font="Regular; 19" valign="top" halign="center" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("EPG from linux-sat.tv (exUSSR)"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.cancel,
			"back": self.cancel,
			"red": self.cancel,
			"ok": self.cancel,
			})
		self["key_red"] = StaticText(_("Close"))
		self["about1"] = StaticText(_("This plugin allows you to download electronic program guides (EPG) from linux-sat.tv (exUSSR) according to your channel list (note: only if EPG for those channels are present in the database)."))
		self["about2"] = StaticText(_("Its main difference from other similar plugins is that it does not require restarting your satellite receiver to update EPG! In case of a receiver reset the previously saved EPG is saved!"))
		self["about3"] = StaticText(_("The plugin can operate either in automatic (by schedule) or manual mode. The update process takes as little time as possible, as it doesn't use the receiver's resources for EPG data convertion. Update speed only depends on the capacity of your Internet connection (average ~10 seconds)."))
		self["about4"] = StaticText(_("linux-sat.tv forms EPG each Monday at 18:00 Kiev time (GMT+2)."))
		self["about5"] = StaticText(_("Plugin setup is as follows:"))
		self["about6"] = StaticText(_("- choose location for EPG storage (USB flash, HDD and internal memory (not recommended) are possible);"))
		self["about7"] = StaticText(_("- choose language for EPG display (Russian/Ukrainian);"))
		self["about8"] = StaticText(_("- choose whether to load EPG automatically or not;"))
		self["about9"] = StaticText(_("- if auto load is on, you also need to set the time and day of week when EPG would be loaded."))
		self["about10"] = StaticText(_("Plugin menu:"))
		self["about11"] = StaticText(_("YELLOW button - manual EPG loading."))
		self["about12"] = StaticText(_("BLUE button - automatic EPG update."))
		self["about13"] = StaticText(_("Thanks dillinger from linux-sat.tv"))
		self["ver"] = StaticText()
		self.verinfo()
	
	def verinfo(self):
		package = 0
		self["ver"].text = " "
		for line in open(status):
			if line.find("epgd") > -1:
				package = 1
			if line.find("Version:") > -1 and package == 1:
				package = 0
				try:
					self["ver"].text = line.split()[1]
				except:
					self["ver"].text = " "
				break
		
	def cancel(self):
		self.close()
####################################################################
class loadEPG():
	def __init__(self):
		self.dialog = None

	def gotSession(self, session):
		self.session = session
		self.timer = enigma.eTimer() 
		self.timer.callback.append(self.update)
		self.timer.start(60000, True)

	def update(self):
		self.timer.stop()
		now = time.localtime(time.time())
		if (config.plugins.epgd.auto.value == "yes" and config.plugins.epgd.timedwn.value[0] == now.tm_hour and config.plugins.epgd.timedwn.value[1] == now.tm_min and int(config.plugins.epgd.weekday.value) == int(now.tm_wday)):
			self.dload()
		if config.plugins.epgd.autosave.value != '0':
			if min > int(config.plugins.epgd.autosave.value) and config.plugins.epgd.timedwn.value[1] != now.tm_min:
				global min
				min = 0
				self.save_load_epg()
				if config.plugins.epgd.autobackup.value:
					self.autobackup()
			else:
				global min
				min = min + 1
		self.timer.start(60000, True)
		
	def autobackup(self):
		os.system("gzip -c %s%s > %sepgtmp/%s.gz" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value, config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
		
	def save_load_epg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_save,None,eEPGCache)
		epgcache = eEPGCache.getInstance().save()
		epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
		epgcache = eEPGCache.getInstance().load()
		
	def dload(self):
		try:
			os.system("wget -q http://linux-sat.tv/epg/epg_%s.dat.gz -O %s%s.gz" % (config.plugins.epgd.lang.value, config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
			if fileExists("%s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value)):
				os.unlink("%s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
				os.system("rm -f %s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
			if not os.path.exists("%sepgtmp" % config.plugins.epgd.direct.value):
				os.system("mkdir -p %sepgtmp" % config.plugins.epgd.direct.value)
			os.system("cp -f %s%s.gz %sepgtmp" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value, config.plugins.epgd.direct.value))
			os.system("gzip -df %s%s.gz" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value))
			if fileExists("%s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value)):
				os.chmod("%s%s" % (config.plugins.epgd.direct.value, config.plugins.epgd.epgname.value), 0644)
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
			self.mbox = self.session.open(MessageBox,(_("EPG downloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("Sorry, the EPG download error")), MessageBox.TYPE_INFO, timeout = 4 )
#####################################################
def main(session, **kwargs):
	session.open(epgdn2)
##############################################################################
pEmu = loadEPG()
##############################################################################
def sessionstart(reason,session=None, **kwargs):
	if reason == 0:
		pEmu.gotSession(session)
##############################################################################
def Plugins(**kwargs):
	result = [
		PluginDescriptor(
			where = [PluginDescriptor.WHERE_AUTOSTART, PluginDescriptor.WHERE_SESSIONSTART],
			fnc = sessionstart
		),
		PluginDescriptor(
			name=_("EPG Downloader"),
			description = _("EPG from linux-sat.tv (exUSSR)"),
			where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU],
			icon = 'epgd.png',
			fnc = main
		),
	]
	return result

# -*- coding: utf-8 -*-
# 3k key downloader (c) 2013 2boom
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
from enigma import ePoint, eTimer, getDesktop
from os import environ
import os
import gettext
########################################
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

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("kkey", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/3kKey/locale/"))

def _(txt):
	t = gettext.dgettext("kkey", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t
######################################################################################
config.plugins.kkey = ConfigSubsection()
config.plugins.kkey.direct = ConfigSelection(default = "/etc/tuxbox/config/", choices = [
		("/etc/tuxbox/config/", _("/etc/tuxbox/config/")),
		("/etc/tuxbox/config/oscam-stable/", _("/etc/tuxbox/config/oscam-stable/")),
		("/usr/keys/", _("/usr/keys/")),
		("/var/keys/", _("/var/keys/")),
		("/etc/keys/", _("/etc/keys/")),
		("/etc/tuxbox/config/emudre/", _("/etc/tuxbox/config/emudre/")),
])
config.plugins.kkey.auto = ConfigSelection(default = "no", choices = [
		("no", _("no")),
		("yes", _("yes")),
		])
config.plugins.kkey.automessage = ConfigSelection(default = "yes", choices = [
		("no", _("no")),
		("yes", _("yes")),
		])
		
config.plugins.kkey.zone = ConfigSelection(default = "centr", choices = [
		("centr", _("Centr")),
		("sibir", _("Sibir")),
		("both", _("Both")),
		])
config.plugins.kkey.period = ConfigSelection(default = "29", choices = [
		("29", _("half an hour")),
		("59", _("one hour")),
		("89", _("an hour and a half")),
		("119", _("two hours")),
		("179", _("tree hours")),
		("359", _("six hours")),
		("719", _("twelve hours")),
		("1439", _("everyday")),
		])
######################################################################
SKIN_HD = """
<screen name="kkey" position="center,160" size="850,370" title="2boom's 3k Key Downloader">
  <widget position="15,10" size="820,200" name="config" scrollbarMode="showOnDemand" />
   <ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/3kKey/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/3kKey/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,358" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/3kKey/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,328" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
SKIN_SD = """
<screen name="kkey" position="center,160" size="620,370" title="2boom's 3k Key Downloader">
  <widget position="15,10" size="590,200" name="config" scrollbarMode="showOnDemand" />
   <ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/3kKey/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/3kKey/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,358" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/3kKey/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,328" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
######################################################################

class kkey(ConfigListScreen, Screen):
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		if getDesktop(0).size().width() == 1280:
			self.skin = SKIN_HD
		else:
			self.skin = SKIN_SD
		self.setTitle(_("2boom's 3k Key Downloader"))
		self.list = []
		self.list.append(getConfigListEntry(_("Select 3k zone"), config.plugins.kkey.zone))
		self.list.append(getConfigListEntry(_("Select path to save ee.bin"), config.plugins.kkey.direct))
		self.list.append(getConfigListEntry(_("AutoDownload ee.bin"), config.plugins.kkey.auto))
		self.list.append(getConfigListEntry(_("AutoDownload period"), config.plugins.kkey.period))
		self.list.append(getConfigListEntry(_("AutoDownload message notification"), config.plugins.kkey.automessage))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Download ee.bin"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.downkey,
			"ok": self.save
		}, -2)
	
	
	def downkey(self):
		try:
			if config.plugins.kkey.zone.value == "both":
				os.system("wget -P /tmp -T2 'http://sat-forum.info/download/index.php?action=downloadfile&filename=ee.bin&directory=oscam_emu_dre2/keys/3c_centr&' -O %seeC.bin" % config.plugins.kkey.direct.value)
				os.system("wget -P /tmp -T2 'http://sat-forum.info/download/index.php?action=downloadfile&filename=ee.bin&directory=oscam_emu_dre2/keys/3c_sibir&' -O %seeS.bin" % config.plugins.kkey.direct.value)
				if fileExists("%seeC.bin" % config.plugins.kkey.direct.value):
					os.chmod("%seeC.bin" % config.plugins.kkey.direct.value, 0644)
				if fileExists("%seeS.bin" % config.plugins.kkey.direct.value):
					os.chmod("%seeS.bin" % config.plugins.kkey.direct.value, 0644)
			else:
				os.system("wget -P /tmp -T2 'http://sat-forum.info/download/index.php?action=downloadfile&filename=ee.bin&directory=oscam_emu_dre2/keys/3c_%s&' -O %see.bin" % (config.plugins.kkey.zone.value, config.plugins.kkey.direct.value))
				if fileExists("%see.bin" % config.plugins.kkey.direct.value):
					os.chmod("%see.bin" % config.plugins.kkey.direct.value, 0644)
			self.mbox = self.session.open(MessageBox,(_("ee.bin(s) donwloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("Sorry, the Key download error")), MessageBox.TYPE_INFO, timeout = 4 )

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)

	def save(self):
		config.plugins.kkey.zone.save()
		config.plugins.kkey.direct.save()
		config.plugins.kkey.auto.save()
		config.plugins.kkey.period.save()
		config.plugins.kkey.automessage.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
####################################################################
class loadkey():
	def __init__(self):
		self.dialog = None

	def gotSession(self, session):
		self.session = session
		self.timer = enigma.eTimer() 
		self.timer.callback.append(self.update)
		self.timer.start(60000, True)

	def update(self):
		self.timer.stop()
		if config.plugins.kkey.auto.value == "yes" and min > int(config.plugins.kkey.period.value):
			global min
			min = 0
			self.downkey()
		else:
			global min
			min = min + 1
		self.timer.start(60000, True)
		
	def downkey(self):
		try:
			if config.plugins.kkey.zone.value == "both":
				os.system("wget -P /tmp -T2 'http://sat-forum.info/download/index.php?action=downloadfile&filename=ee.bin&directory=oscam_emu_dre2/keys/3c_centr&' -O %seeC.bin" % config.plugins.kkey.direct.value)
				os.system("wget -P /tmp -T2 'http://sat-forum.info/download/index.php?action=downloadfile&filename=ee.bin&directory=oscam_emu_dre2/keys/3c_sibir&' -O %seeS.bin" % config.plugins.kkey.direct.value)
				if fileExists("%seeC.bin" % config.plugins.kkey.direct.value):
					os.chmod("%seeC.bin" % config.plugins.kkey.direct.value, 0644)
				if fileExists("%seeS.bin" % config.plugins.kkey.direct.value):
					os.chmod("%seeS.bin" % config.plugins.kkey.direct.value, 0644)
			else:
				os.system("wget -P /tmp -T2 'http://sat-forum.info/download/index.php?action=downloadfile&filename=ee.bin&directory=oscam_emu_dre2/keys/3c_%s&' -O %see.bin" % (config.plugins.kkey.zone.value, config.plugins.kkey.direct.value))
				if fileExists("%see.bin" % config.plugins.kkey.direct.value):
					os.chmod("%see.bin" % config.plugins.kkey.direct.value, 0644)
			if config.plugins.kkey.automessage.value == "yes":
				self.mbox = self.session.open(MessageBox,(_("ee.bin(s) donwloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			if config.plugins.kkey.automessage.value == "yes":
				self.mbox = self.session.open(MessageBox,(_("Sorry, the Key download error")), MessageBox.TYPE_INFO, timeout = 4 )
#####################################################
def main(session, **kwargs):
	session.open(kkey)
##############################################################################
pEmu = loadkey()
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
			name=_("2boom's 3k Key Downloader"),
			description = _("3k Key Downloader for zone Centr/Sibir"),
			where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU],
			icon = '3k.png',
			fnc = main
		),
	]
	return result

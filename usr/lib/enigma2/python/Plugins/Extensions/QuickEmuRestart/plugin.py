#QuickEmuRestart (c) 2boom 2012
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Tools.Directories import fileExists
from GlobalActions import globalActionMap
from keymapparser import readKeymap, removeKeymap
from os import environ
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Language import language
from Components.config import config, getConfigListEntry, ConfigText, ConfigInteger, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.ConfigList import ConfigListScreen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.Sources.StaticText import StaticText
import os
import gettext
from os import environ

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("qemurestart", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/QuickEmuRestart/locale/"))

def _(txt):
	t = gettext.dgettext("qemurestart", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t
	
config.plugins.qer = ConfigSubsection()
config.plugins.qer.keyname = ConfigSelection(default = "KEY_TV2", choices = [("KEY_TV2", "TV2")])
config.plugins.qer.time = ConfigInteger(default = 6, limits = (0, 99))
##############################################################################
class QuickEmu():
	def __init__(self):
		self.dialog = None

	def gotSession(self, session):
		self.session = session
		keymap = "/usr/lib/enigma2/python/Plugins/Extensions/QuickEmuRestart/keymap.xml"
		global globalActionMap
		readKeymap(keymap)
		globalActionMap.actions['showEmuRestart'] = self.restartCam
		
	def restartCam(self):
# VTI 
		if fileExists("/etc/init.d/current_cam.sh"):
			os.system("/etc/init.d/current_cam.sh stop")
			os.system("/etc/init.d/current_cam.sh start")
# BH
		elif fileExists("/usr/bin/StartBhCam"):
			os.system("/usr/bin/StartBhCam stop")
			os.system("/usr/bin/StartBhCam start")
# Dream-Elit
		elif fileExists("/usr/bin/StartDelCam"):
			os.system("/usr/bin/StartDelCam stop")
			os.system("/usr/bin/StartDelCam start")
# Dream-Elite-2
		elif fileExists("/etc/init.d/restartEmu.sh"):
			os.system("/etc/init.d/restartEmu.sh start")
# Domica 9
		elif fileExists("/etc/rcS.d/S50emu"):
			os.system("/etc/rcS.d/S50emu restart")
# PLI
		elif fileExists("/etc/init.d/softcam"):
			os.system("/etc/init.d/softcam restart")
		elif fileExists("/etc/init.d/cardserver"):
			os.system("/etc/init.d/cardserver restart")
# TS-Panel
		elif fileExists("/etc/startcam.sh"):
			for line in open("/etc/startcam.sh"):
				if line.find("script") > -1:
					currentemu = line.split()[0]
			if fileExists("%s " % currentemu):
				os.system("%s cam_down &" % currentemu)
				os.system("%s cam_up &" % currentemu)
# PKT
		elif fileExists("/etc/init.d/cam"):
			os.system("/etc/init.d/cam restart")
		self.mbox = self.session.open(MessageBox,(_("%s  restarted...") % self.showcamname()), MessageBox.TYPE_INFO, timeout = config.plugins.qer.time.value )
#########################################################################################################
	def showcamname(self):
		serlist = None
		camdlist = None
		nameemu = []
		nameser = []
# VTI
		if fileExists("/tmp/.emu.info"):
			try:
				for line in open("/tmp/.emu.info"):
					return line
			except:
				return None
# BH
		elif fileExists("/etc/CurrentBhCamName"):
			try:
				for line in open("/etc/CurrentBhCamName"):
					return line
			except:
				return None
# TS-Panel
		elif fileExists("/etc/startcam.sh"):
			try:
				for line in open("/etc/startcam.sh"):
					if line.find("script") > -1:
						return "%s" % line.split("/")[-1].split()[0][:-3]
			except:
				return None
# Dream-Elit
		elif fileExists("/etc/CurrentDelCamName"):
			try:
				for line in open("/etc/CurrentDelCamName"):
					return line
			except:
				return None
# Dream-Elite-2   
		elif fileExists("/usr/bin/emuactive"):
			try:
				for line in open("/usr/bin/emuactive"):
					return line
			except:
				return None  
# Domica 9
		elif fileExists("/etc/active_emu.list"):
			try:
				for line in open("/etc/active_emu.list"):
					return line
			except:
				return None
# Pli
		elif fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
			try:
				for line in open("/etc/init.d/softcam"):
					if line.find("echo") > -1:
						nameemu.append(line)
				camdlist = "%s" % nameemu[1].split('"')[1]
			except:
				pass
			try:
				for line in open("/etc/init.d/cardserver"):
					if line.find("echo") > -1:
						nameser.append(line)
				serlist = "%s" % nameser[1].split('"')[1]
			except:
				pass
			if serlist is None:
				serlist = ""
			elif camdlist is None:
				camdlist = ""
			return ("%s %s" % (serlist, camdlist))
#####################################################
class qer_setup(ConfigListScreen, Screen):
	skin = """
<screen name="qer_setup" position="center,160" size="750,370" title="2boom's QuickEmuRestart">
  <widget position="15,10" size="720,200" name="config" scrollbarMode="showOnDemand" />
   <ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickEmuRestart/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/QuickEmuRestart/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("2boom's QuickEmuRestart"))
		self.list = []
		self.list.append(getConfigListEntry(_("Select key to Softcam restart"), config.plugins.qer.keyname))
		self.list.append(getConfigListEntry(_("Set time in sec message window is shown"), config.plugins.qer.time))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"ok": self.save
		}, -2)
	

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)

	def save(self):
		config.plugins.qer.keyname.save()
		config.plugins.qer.time.save()
		configfile.save()
		keyfile = open("/usr/lib/enigma2/python/Plugins/Extensions/QuickEmuRestart/keymap.xml", "w")
		keyfile.write('<keymap>\n\t<map context="GlobalActions">\n\t\t<key id="%s" mapto="showEmuRestart" flags="m" />\n\t</map>\n</keymap>' % config.plugins.qer.keyname.value)
		keyfile.close()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
#####################################################
def main(session, **kwargs):
	session.open(qer_setup)
##############################################################################
pEmu = QuickEmu()
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
			name=_("2boom's QuickEmuRestart"),
			description = _("Restart Softcam with a single button"),
			where = PluginDescriptor.WHERE_PLUGINMENU,
			icon = 'qer.png',
			fnc = main
		),
	]
	return result
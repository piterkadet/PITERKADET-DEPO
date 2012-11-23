## SetupTechnoHD
## Coded by Sirius
##
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Language import language
from Components.ConfigList import ConfigListScreen
from Components.config import config, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigText, ConfigInteger
from Tools.Directories import fileExists
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_LANGUAGE
from os import environ
from os import system
import gettext
import os

config.skin.tech = ConfigSubsection()
config.skin.tech.style = ConfigSelection(default="grey", choices = ["grey", "yellow", "red", "green", "blue"])
config.skin.tech.clockpanel = ConfigSelection(default="no", choices = ["yes", "no"])
config.skin.tech.numberchannel = ConfigSelection(default="no", choices = ["yes", "no"])
config.skin.tech.ecmpanel = ConfigSelection(default="no", choices = ["no", "on left", "on right", "on centre"])
config.skin.tech.epgpanel = ConfigSelection(default="no", choices = ["no", "on left", "on right"])
config.skin.tech.coverpanel = ConfigSelection(default="no", choices = ["no", "on left", "on right"])
config.skin.tech.dish = ConfigSelection(default="on left", choices = ["on left", "on right"])
config.skin.tech.fonts = ConfigSelection(default="regular", choices = ["regular", "bold", "italic", "bolditalic"])
config.skin.tech.titlecolor = ConfigSelection(default="yellow", choices = ["white", "grey", "yellow", "orange", "red", "greenish", "green", "bluish", "blue"])
config.skin.tech.textcolor = ConfigSelection(default="white", choices = ["white", "grey", "yellow", "orange", "red", "greenish", "green", "bluish", "blue"])
config.skin.tech.avtextcolor = ConfigSelection(default="grey", choices = ["white", "grey", "yellow", "orange", "red", "greenish", "green", "bluish", "blue"])
config.skin.tech.textcurcolor = ConfigSelection(default="bluish", choices = ["white", "grey", "yellow", "orange", "red", "greenish", "green", "bluish", "blue"])
config.skin.tech.progresscolor = ConfigSelection(default="yellow", choices = ["yellow", "red", "green", "blue"])

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("SetupTechnoHD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/SetupTechnoHD/locale"))

def _(txt):
	t = gettext.dgettext("SetupTechnoHD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

class SetupTechnoHD(ConfigListScreen, Screen):
	skin = """
	<screen name="SetupTechnoHD" position="0,0" size="1280,720" title=" " flags="wfNoBorder">
		<ePixmap position="0,0" zPosition="-1" size="1280,720" pixmap="Techno_hd/style/greymenu_1.png" />
		<widget source="Title" render="Label" position="45,38" size="720,36" font="Regular; 30" halign="center" transparent="1" foregroundColor="#00ffcc33" backgroundColor="background" borderWidth="2" />
		<ePixmap position="775,450" zPosition="1" size="500,150" pixmap="Techno_hd/logo.png" alphatest="blend" />
		<widget name="config" position="50,95" size="710,540" scrollbarMode="showOnDemand" selectionPixmap="Techno_hd/style/greysel.png" transparent="1" />
		<widget source="key_red" render="Label" position="56,663" size="270,40" font="Regular; 22" halign="center" valign="top" backgroundColor="background" transparent="1" zPosition="3" foregroundColor="#00f4f4f4" borderWidth="1" />
		<widget source="key_green" render="Label" position="355,663" size="270,40" font="Regular; 22" halign="center" valign="top" backgroundColor="background" transparent="1" zPosition="3" foregroundColor="#00f4f4f4" borderWidth="1" />
		<!--<widget source="version_sk" render="Label" position="930,585" size="200,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#00f4f4f4" transparent="1" zPosition="2" />-->
		<!--<widget source="vinfo_sk" render="Label" position="1150,585" size="80,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="#008f8f8f" transparent="1" zPosition="2" />-->
		<!--<widget source="version_lib" render="Label" position="880,615" size="250,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#00f4f4f4" transparent="1" zPosition="2" />-->
		<!--<widget source="vinfo_lib" render="Label" position="1150,615" size="80,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="#008f8f8f" transparent="1" zPosition="2" />-->
		<ePixmap pixmap="Techno_hd/buttons/key_info.png" position="800,615" size="35,25" zPosition="2" alphatest="blend" />
		<widget source="session.VideoPicture" render="Pig" position="806,96" size="428,248" zPosition="3" backgroundColor="transparent2" />
		<widget source="session.Event_Now" render="Label" position="800,390" size="446,48" zPosition="2" halign="center" font="Regular; 20" foregroundColor="#000099ff" backgroundColor="background" transparent="1">
			<convert type="EventName2">Name</convert>
		</widget>
		<widget source="session.Event_Now" render="Progress" pixmap="Techno_hd/style/yellowprogress.png" position="866,368" size="310,8" zPosition="2" backgroundColor="background" transparent="1">
			<convert type="EventTime">Progress</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="1122,38" size="52,36" font="Display; 35" backgroundColor="background" foregroundColor="#00ffcc33" halign="right" zPosition="1" transparent="1" borderWidth="2">
			<convert type="ClockToText">Format:%H</convert>
		</widget>
		<eLabel text=":" position="1176,38" size="10,36" font="Display; 34" backgroundColor="background" foregroundColor="#008f8f8f" halign="center" transparent="1" zPosition="2" borderWidth="2" />
		<widget source="global.CurrentTime" render="FixedLabel" text=":" position="1176,38" size="10,36" font="Display; 34" backgroundColor="background" foregroundColor="#00ffcc33" halign="center" transparent="1" zPosition="3" borderWidth="2">
			<convert type="AlwaysTrue">
			</convert>
			<convert type="ConditionalShowHide">Blink</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="1190,38" size="52,36" font="Display; 35" backgroundColor="background" foregroundColor="#00ffcc33" halign="left" transparent="1" zPosition="1" borderWidth="2">
			<convert type="ClockToText">Format:%M</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="768,45" size="350,30" font="Display; 26" backgroundColor="background" foregroundColor="#00f4f4f4" halign="right" transparent="1" borderWidth="2">
			<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
		</widget>
		<ePixmap position="51,651" size="281,16" zPosition="1" pixmap="Techno_hd/buttons.png" alphatest="blend" />
		<ePixmap position="350,651" size="281,16" zPosition="1" pixmap="Techno_hd/buttons.png" alphatest="blend" />
		<ePixmap position="648,651" size="281,16" zPosition="1" pixmap="Techno_hd/buttons.png" alphatest="blend" />
		<ePixmap position="946,651" size="281,16" zPosition="1" pixmap="Techno_hd/buttons.png" alphatest="blend" />
		<ePixmap pixmap="Techno_hd/buttons/red2.png" position="54,653" size="275,10" alphatest="blend" zPosition="2" />
		<ePixmap pixmap="Techno_hd/buttons/green2.png" position="353,653" size="275,10" alphatest="blend" zPosition="2" />
		<ePixmap pixmap="Techno_hd/buttons/yellow2.png" position="650,653" size="275,10" alphatest="blend" zPosition="2" />
		<ePixmap pixmap="Techno_hd/buttons/blue2.png" position="949,653" size="275,10" alphatest="blend" zPosition="2" />
	</screen>"""

	def __init__(self, session):

		Screen.__init__(self, session)
		self.session = session

		list = []
		list.append(getConfigListEntry(_("Style skin`s:"), config.skin.tech.style))
		list.append(getConfigListEntry(_("Clock panel in infobar:"), config.skin.tech.clockpanel))
		list.append(getConfigListEntry(_("Channel number in infobar:"), config.skin.tech.numberchannel))
		list.append(getConfigListEntry(_("ECM panel in secondinfobar:"), config.skin.tech.ecmpanel))
		list.append(getConfigListEntry(_("EPG panel in secondinfobar:"), config.skin.tech.epgpanel))
		list.append(getConfigListEntry(_("Poster film`s in mediainfobar:"), config.skin.tech.coverpanel))
		list.append(getConfigListEntry(_("Position dish:"), config.skin.tech.dish))
		list.append(getConfigListEntry(_("Fonts:"), config.skin.tech.fonts))
		list.append(getConfigListEntry(_("Title text color:"), config.skin.tech.titlecolor))
		list.append(getConfigListEntry(_("Menu text color:"), config.skin.tech.textcolor))
		list.append(getConfigListEntry(_("Additional text color:"), config.skin.tech.avtextcolor))
		list.append(getConfigListEntry(_("Cursor text color:"), config.skin.tech.textcurcolor))
		list.append(getConfigListEntry(_("Progress bar color:"), config.skin.tech.progresscolor))
		ConfigListScreen.__init__(self, list)

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "EPGSelectActions"],{"ok": self.save, "cancel": self.exit, "red": self.exit, "green": self.save, "info": self.about}, -1)
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Save"))
		self["Title"] = StaticText(_("Setup TechnoHD"))
#		self["version_sk"] = StaticText(_("Version skin:"))
#		self["version_lib"] = StaticText(_("Version library:"))
#		self["vinfo_sk"] = StaticText()
#		self["vinfo_lib"] = StaticText()
#		self.infosk()
#		self.infolib()

#	def infosk(self):
#		package = 0
#		global status 
#		if fileExists("/usr/lib/opkg/status"):
#			status = "/usr/lib/opkg/status"
#		elif fileExists("/var/lib/opkg/status"):
#			status = "/var/lib/opkg/status"
#		for line in open(status):
#			if line.find("TechnoHD") > -1:
#				package = 1
#			if line.find("Version:") > -1 and package == 1:
#				package = 0
#				try:
#					self["vinfo_sk"].text = line.split()[1]
#				except:
#					self["vinfo_sk"].text = " "
#				break

#	def infolib(self):
#		package = 0
#		global status 
#		if fileExists("/usr/lib/opkg/status"):
#			status = "/usr/lib/opkg/status"
#		elif fileExists("/var/lib/opkg/status"):
#			status = "/var/lib/opkg/status"
#		for line in open(status):
#			if line.find("lib-gisclub-skin") > -1:
#				package = 1
#			if line.find("Version:") > -1 and package == 1:
#				package = 0
#				try:
#					self["vinfo_lib"].text = line.split()[1]
#				except:
#					self["vinfo_lib"].text = " "
#				break

	def save(self):
		skinpath = "/usr/share/enigma2/Techno_hd/"
		pluginpath = "/usr/lib/enigma2/python/"
		deffonts = "LiberationSans-Regular.ttf"
		deftitlecolor = "#00ffcc33"
		deftextcolor = "#00f4f4f4"
		defavtextcolor = "#008f8f8f"
		deftextcurcolor = "#000099ff"
	# save config
		for x in self["config"].list:
			x[1].save()
	# default skin
		os.system("cp %sdefskin.xml %sskin.xml" % (skinpath, skinpath))
	# fonts	
		if config.skin.tech.fonts.value=="regular":
			os.system("sed -i 's/%s/LiberationSans-Regular.ttf/w' %sskin.xml" % (deffonts, skinpath))
		elif config.skin.tech.fonts.value=="bold":
			os.system("sed -i 's/%s/LiberationSans-Bold.ttf/w' %sskin.xml" % (deffonts, skinpath))
		elif config.skin.tech.fonts.value=="italic":
			os.system("sed -i 's/%s/LiberationSans-Italic.ttf/w' %sskin.xml" % (deffonts, skinpath))
		elif config.skin.tech.fonts.value=="bolditalic":
			os.system("sed -i 's/%s/LiberationSans-BoldItalic.ttf/w' %sskin.xml" % (deffonts, skinpath))
		else:
			self.close()
	# color`s text
		if config.skin.tech.titlecolor.value=="white":
			os.system("sed -i 's/%s/#00ffffff/w' %sskin.xml" % (deftitlecolor, skinpath))
		elif config.skin.tech.titlecolor.value=="grey":
			os.system("sed -i 's/%s/#008f8f8f/w' %sskin.xml" % (deftitlecolor, skinpath))
		elif config.skin.tech.titlecolor.value=="yellow":
			os.system("sed -i 's/%s/#00ffcc33/w' %sskin.xml" % (deftitlecolor, skinpath))
		elif config.skin.tech.titlecolor.value=="orange":
			os.system("sed -i 's/%s/#00ff6600/w' %sskin.xml" % (deftitlecolor, skinpath))
		elif config.skin.tech.titlecolor.value=="red":
			os.system("sed -i 's/%s/#00ff0d0d/w' %sskin.xml" % (deftitlecolor, skinpath))
		elif config.skin.tech.titlecolor.value=="greenish":
			os.system("sed -i 's/%s/#0000ffff/w' %sskin.xml" % (deftitlecolor, skinpath))
		elif config.skin.tech.titlecolor.value=="green":
			os.system("sed -i 's/%s/#00009a00/w' %sskin.xml" % (deftitlecolor, skinpath))
		elif config.skin.tech.titlecolor.value=="bluish":
			os.system("sed -i 's/%s/#000099ff/w' %sskin.xml" % (deftitlecolor, skinpath))
		elif config.skin.tech.titlecolor.value=="blue":
			os.system("sed -i 's/%s/#000035ff/w' %sskin.xml" % (deftitlecolor, skinpath))
		else:
			self.close()
		if config.skin.tech.textcolor.value=="white":
			os.system("sed -i 's/%s/#00ffffff/w' %sskin.xml" % (deftextcolor, skinpath))
		elif config.skin.tech.textcolor.value=="grey":
			os.system("sed -i 's/%s/#008f8f8f/w' %sskin.xml" % (deftextcolor, skinpath))
		elif config.skin.tech.textcolor.value=="yellow":
			os.system("sed -i 's/%s/#00ffcc33/w' %sskin.xml" % (deftextcolor, skinpath))
		elif config.skin.tech.textcolor.value=="orange":
			os.system("sed -i 's/%s/#00ff6600/w' %sskin.xml" % (deftextcolor, skinpath))
		elif config.skin.tech.textcolor.value=="red":
			os.system("sed -i 's/%s/#00ff0d0d/w' %sskin.xml" % (deftextcolor, skinpath))
		elif config.skin.tech.textcolor.value=="greenish":
			os.system("sed -i 's/%s/#0000ffff/w' %sskin.xml" % (deftextcolor, skinpath))
		elif config.skin.tech.textcolor.value=="green":
			os.system("sed -i 's/%s/#00009a00/w' %sskin.xml" % (deftextcolor, skinpath))
		elif config.skin.tech.textcolor.value=="bluish":
			os.system("sed -i 's/%s/#000099ff/w' %sskin.xml" % (deftextcolor, skinpath))
		elif config.skin.tech.textcolor.value=="blue":
			os.system("sed -i 's/%s/#000035ff/w' %sskin.xml" % (deftextcolor, skinpath))
		else:
			self.close()
		if config.skin.tech.avtextcolor.value=="white":
			os.system("sed -i 's/%s/#00ffffff/w' %sskin.xml" % (defavtextcolor, skinpath))
		elif config.skin.tech.avtextcolor.value=="grey":
			os.system("sed -i 's/%s/#008f8f8f/w' %sskin.xml" % (defavtextcolor, skinpath))
		elif config.skin.tech.avtextcolor.value=="yellow":
			os.system("sed -i 's/%s/#00ffcc33/w' %sskin.xml" % (defavtextcolor, skinpath))
		elif config.skin.tech.avtextcolor.value=="orange":
			os.system("sed -i 's/%s/#00ff6600/w' %sskin.xml" % (defavtextcolor, skinpath))
		elif config.skin.tech.avtextcolor.value=="red":
			os.system("sed -i 's/%s/#00ff0d0d/w' %sskin.xml" % (defavtextcolor, skinpath))
		elif config.skin.tech.avtextcolor.value=="greenish":
			os.system("sed -i 's/%s/#0000ffff/w' %sskin.xml" % (defavtextcolor, skinpath))
		elif config.skin.tech.avtextcolor.value=="green":
			os.system("sed -i 's/%s/#00009a00/w' %sskin.xml" % (defavtextcolor, skinpath))
		elif config.skin.tech.avtextcolor.value=="bluish":
			os.system("sed -i 's/%s/#000099ff/w' %sskin.xml" % (defavtextcolor, skinpath))
		elif config.skin.tech.avtextcolor.value=="blue":
			os.system("sed -i 's/%s/#000035ff/w' %sskin.xml" % (defavtextcolor, skinpath))
		else:
			self.close()
		if config.skin.tech.textcurcolor.value=="white":
			os.system("sed -i 's/%s/#00ffffff/w' %sskin.xml" % (deftextcurcolor, skinpath))
		elif config.skin.tech.textcurcolor.value=="grey":
			os.system("sed -i 's/%s/#008f8f8f/w' %sskin.xml" % (deftextcurcolor, skinpath))
		elif config.skin.tech.textcurcolor.value=="yellow":
			os.system("sed -i 's/%s/#00ffcc33/w' %sskin.xml" % (deftextcurcolor, skinpath))
		elif config.skin.tech.textcurcolor.value=="orange":
			os.system("sed -i 's/%s/#00ff6600/w' %sskin.xml" % (deftextcurcolor, skinpath))
		elif config.skin.tech.textcurcolor.value=="red":
			os.system("sed -i 's/%s/#00ff0d0d/w' %sskin.xml" % (deftextcurcolor, skinpath))
		elif config.skin.tech.textcurcolor.value=="greenish":
			os.system("sed -i 's/%s/#0000ffff/w' %sskin.xml" % (deftextcurcolor, skinpath))
		elif config.skin.tech.textcurcolor.value=="green":
			os.system("sed -i 's/%s/#00009a00/w' %sskin.xml" % (deftextcurcolor, skinpath))
		elif config.skin.tech.textcurcolor.value=="bluish":
			os.system("sed -i 's/%s/#000099ff/w' %sskin.xml" % (deftextcurcolor, skinpath))
		elif config.skin.tech.textcurcolor.value=="blue":
			os.system("sed -i 's/%s/#000035ff/w' %sskin.xml" % (deftextcurcolor, skinpath))
		else:
			self.close()
	# number channel
		if config.skin.tech.numberchannel.value=="no":
			os.system("sed -i 's/TemplatesNumberCh-1/TemplatesNumberCh/w' %sskin.xml" % skinpath)
		elif config.skin.tech.numberchannel.value=="yes":
			os.system("sed -i 's/TemplatesNumberCh-2/TemplatesNumberCh/w' %sskin.xml" % skinpath)
		else:
			self.close()
	# clock panel
		if config.skin.tech.clockpanel.value=="no":
			os.system("sed -i 's/TemplatesClock-1/TemplatesClock/w' %sskin.xml" % skinpath)
		elif config.skin.tech.clockpanel.value=="yes":
			os.system("sed -i 's/TemplatesClock-2/TemplatesClock/w' %sskin.xml" % skinpath)
		else:
			self.close()
	# ecm panel
		if config.skin.tech.ecmpanel.value=="no":
			os.system("sed -i 's/TemplatesSecondInfoBar-1/TemplatesSecondInfoBar/w' %sskin.xml" % skinpath)
		elif config.skin.tech.ecmpanel.value=="on centre":
			os.system("sed -i 's/TemplatesSecondInfoBar-2/TemplatesSecondInfoBar/w' %sskin.xml" % skinpath)
		elif config.skin.tech.ecmpanel.value=="on right":
			os.system("sed -i 's/TemplatesSecondInfoBar-3/TemplatesSecondInfoBar/w' %sskin.xml" % skinpath)
		elif config.skin.tech.ecmpanel.value=="on left":
			os.system("sed -i 's/TemplatesSecondInfoBar-4/TemplatesSecondInfoBar/w' %sskin.xml" % skinpath)
		else:
			self.close()
	# epg panel
		if config.skin.tech.epgpanel.value=="no":
			os.system("sed -i 's/TemplatesEPG-1/TemplatesEPG/w' %sskin.xml" % skinpath)
		elif config.skin.tech.epgpanel.value=="on right":
			os.system("sed -i 's/TemplatesEPG-2/TemplatesEPG/w' %sskin.xml" % skinpath)
		elif config.skin.tech.epgpanel.value=="on left":
			os.system("sed -i 's/TemplatesEPG-3/TemplatesEPG/w' %sskin.xml" % skinpath)
		else:
			self.close()
	# cover panel
		if config.skin.tech.coverpanel.value=="no":
			os.system("sed -i 's/TemplatesCover-1/TemplatesCover/w' %sskin.xml" % skinpath)
		elif config.skin.tech.coverpanel.value=="on right":
			os.system("sed -i 's/TemplatesCover-2/TemplatesCover/w' %sskin.xml" % skinpath)
			os.system("cp %sPlugins/Extensions/SetupTechnoHD/Cover %sComponents/Renderer/CoverTech.py" % (pluginpath, pluginpath))
		elif config.skin.tech.coverpanel.value=="on left":
			os.system("sed -i 's/TemplatesCover-3/TemplatesCover/w' %sskin.xml" % skinpath)
			os.system("cp %sPlugins/Extensions/SetupTechnoHD/Cover %sComponents/Renderer/CoverTech.py" % (pluginpath, pluginpath))
		else:
			self.close()
	# dish
		if config.skin.tech.dish.value=="on left":
			os.system("sed -i 's/Dish-1/Dish/w' %sskin.xml" % skinpath)
		elif config.skin.tech.dish.value=="on right":
			os.system("sed -i 's/Dish-2/Dish/w' %sskin.xml" % skinpath)
		else:
			self.close()
	# style progress
		if config.skin.tech.progresscolor.value=="yellow":
			os.system("sed -i 's/yellowprogress/yellowprogress/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/yellowprogress_bar/yellowprogress_bar/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/yellowprogress_big/yellowprogress_big/w' %sskin.xml" % skinpath)
		elif config.skin.tech.progresscolor.value=="red":
			os.system("sed -i 's/yellowprogress/redprogress/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/yellowprogress_bar/redprogress_bar/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/yellowprogress_big/redprogress_big/w' %sskin.xml" % skinpath)
		elif config.skin.tech.progresscolor.value=="green":
			os.system("sed -i 's/yellowprogress/greenprogress/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/yellowprogress_bar/greenprogress_bar/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/yellowprogress_big/greenprogress_big/w' %sskin.xml" % skinpath)
		elif config.skin.tech.progresscolor.value=="blue":
			os.system("sed -i 's/yellowprogress/blueprogress/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/yellowprogress_bar/blueprogress_bar/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/yellowprogress_big/blueprogress_big/w' %sskin.xml" % skinpath)
		else:
			self.close()
	# style skin`s
		if config.skin.tech.style.value=="grey":
			os.system("sed -i 's/greyinfobar/greyinfobar/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greymenu/greymenu/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greysel/greysel/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greyvolume/greyvolume/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greydownload/greydownload/w' %sskin.xml" % skinpath)
		elif config.skin.tech.style.value=="yellow":
			os.system("sed -i 's/greyinfobar/yellowinfobar/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greymenu/yellowmenu/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greysel/yellowsel/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greyvolume/yellowvolume/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greydownload/yellowdownload/w' %sskin.xml" % skinpath)
		elif config.skin.tech.style.value=="red":
			os.system("sed -i 's/greyinfobar/redinfobar/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greymenu/redmenu/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greysel/redsel/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greyvolume/redvolume/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greydownload/reddownload/w' %sskin.xml" % skinpath)
		elif config.skin.tech.style.value=="green":
			os.system("sed -i 's/greyinfobar/greeninfobar/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greymenu/greenmenu/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greysel/greensel/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greyvolume/greenvolume/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greydownload/greendownload/w' %sskin.xml" % skinpath)
		elif config.skin.tech.style.value=="blue":
			os.system("sed -i 's/greyinfobar/blueinfobar/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greymenu/bluemenu/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greysel/bluesel/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greyvolume/bluevolume/w' %sskin.xml" % skinpath)
			os.system("sed -i 's/greydownload/bluedownload/w' %sskin.xml" % skinpath)
		else:
			self.close()
		self.session.openWithCallback(self.restart, MessageBox,_("Do you want to restart the GUI now ?"), MessageBox.TYPE_YESNO)

	def exit(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()

	def restart(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 3)

	def about(self):
		self.session.open(MessageBox, _("Skin TechnoHD\nDeveloper: Sirius0103 \nHomepage: www.gisclub.tv \n\nDonate:\nWMZ  Z395874509364\nWMR  R213063691482"), MessageBox.TYPE_INFO)

def main(session, **kwargs):
	session.open(SetupTechnoHD)

def Plugins(**kwargs):
	return PluginDescriptor(name=_("Setup TechnoHD"),
	description=_("Setup skin TechnoHD"),
	where = [PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU],
	icon="plugin.png",
	fnc=main)

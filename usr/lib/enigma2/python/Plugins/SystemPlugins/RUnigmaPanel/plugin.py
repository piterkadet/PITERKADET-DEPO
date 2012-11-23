from enigma import *
from __init__ import _
import os
from enigma import eTimer, eListbox, getDesktop, iPlayableService, eServiceCenter, iServiceInformation
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Components.ConfigList import ConfigList
from Components.config import *
from Components.PluginComponent import plugins
from Components.MenuList import MenuList
from Components.GUIComponent import GUIComponent
from Components.HTMLComponent import HTMLComponent
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.NetworkSetup import NetworkAdapterSelection
from Screens.Ci import CiSelection
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Screens.PluginBrowser import *
from Screens.SleepTimerEdit import *
from Plugins.SystemPlugins.SkinSelector.plugin import SkinSelector
from Plugins.SystemPlugins.Videomode.plugin import VideoSetup
from Plugins.Extensions.AlternativeSoftCamManager.plugin import AltCamManager
from Components.Button import Button
from Components.Label import Label, MultiColorLabel
from Components.ServiceEventTracker import ServiceEventTracker
from ServiceReference import ServiceReference
from Screens.Console import Console
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, crawlDirectory
from Tools.BoundFunction import boundFunction

#------------------------------------------------------------------------------------------
HDSkn = True
class MenuBlupanel(Screen):

	global HDSkn
	try:
		sz_w = getDesktop(0).size().width()
		if sz_w == 1280:
			HDSkn = True
		else:
			HDSkn = False
	except:
		HDSkn = False

	if HDSkn:
		skin="""
<screen name="MenuBlupanel" position="110,60" size="1060,600" title="RUnigmaPanel"  backgroundColor="#ffffffff" flags="wfNoBorder">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/fon.png" position="0,0" size="1060,600" zPosition="1" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/ram.png" position="46,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/epg.png" position="290,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/system.png" position="533,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/emu.png" position="782,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/cifs.png" position="46,223" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/samba.png" position="290,223" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/tuner.png" position="533,223" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/backup.png" position="782,223" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/time.png" position="46,394" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/highSR.png" position="290,394" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/reboot.png" position="533,394" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/PCpower.png" position="782,394" size="180,100" zPosition="3" alphatest="on" />
    <widget source="menu" render="Listbox" zPosition="3" transparent="1" position="1231, 196" size="250,75" scrollbarMode="showOnDemand" foregroundColorSelected="#FFFFFF">
      <convert type="StringList" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_ram</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_plug</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_setup</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="755,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_emu</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_cifs</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_samba</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_tuner</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="755,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_backup</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,384" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_time</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,384" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_packet</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,384" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_reset</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="755,384" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_timer</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget name="type1"  position="46,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type2"  position="290,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type3"  position="533,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type4"  position="782,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type5"  position="46,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type6"  position="290,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type7"  position="533,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type8"  position="782,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type9"  position="46,502" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type10"  position="290,502" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type11"  position="533,502" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type12"  position="782,502" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
     </screen>"""

	def __init__(self, session, args = 0):
		Screen.__init__(self, session)
		self.session = session
		self.list = [ ]
		self.list.append((_("CLEAR RAM"), "ram", "menu_ram"))
		self.list.append((_("CIFS PROTOCOL"), "cifs", "menu_cifs"))
		self.list.append((_("TIME"), "time", "menu_time"))
		self.list.append((_("EPG DOWNLOAD"), "epg", "menu_plug"))
		self.list.append((_("PROTOCOL SAMBA"), "samba", "menu_samba"))
		self.list.append((_("HIGH-SPEED PACKET"), "packet", "menu_packet"))
		self.list.append((_("SYSTEM SETUP"), "setup", "menu_setup"))
		self.list.append((_("SELECTION OF TUNER"), "tuner", "menu_tuner"))
		self.list.append((_("FORCED RESET RECEIVER"), "reset", "menu_reset"))
		self.list.append((_("EDITOR EMULATOR"), "emud", "menu_emu"))
		self.list.append((_("CREATE BACKUP"), "backup", "menu_backup"))
		self.list.append((_("POWER MANAGEMENT"), "power", "menu_timer"))
		self["menu"] = List(self.list)
		self["type1"] = Label(_("CLEAR RAM"))
		self["type2"] = Label(_("EPG DOWNLOAD"))
		self["type3"] = Label(_("SYSTEM SETUP"))
		self["type4"] = Label(_("EDITOR EMULATOR"))
		self["type5"] = Label(_("CIFS PROTOCOL"))
		self["type6"] = Label(_("PROTOCOL SAMBA"))
		self["type7"] = Label(_("SELECTION OF TUNER"))
		self["type8"] = Label(_("CREATE BACKUP"))
		self["type9"] = Label(_("TIME"))
		self["type10"] = Label(_("HIGH-SPEED PACKET"))
		self["type11"] = Label(_("FORCED RESET RECEIVER"))
		self["type12"] = Label(_("POWER MANAGEMENT"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions"],
			{
				"red": self.red,
				"green": self.green,
				"yellow": self.yellow,
				"blue": self.blue,
				"ok": self.okbuttonClick,
				"cancel": self.Exit,
				"up": self.up,
				"down": self.down,
				"left": self.left,
				"right": self.right,
			}, -1)


	def up(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "epg" and selection[1] != "setup" and selection[1] != "emud":
				self["menu"].master.downstream_elements.move(eListbox.moveUp)
			else:
				pass
		else:
			pass

	def down(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "time" and selection[1] != "packet" and selection[1] != "reset":
				self["menu"].master.downstream_elements.move(eListbox.moveDown)
			else:
				pass
		else:
			pass

	def left(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "cifs" and selection[1] != "time":
				self["menu"].master.downstream_elements.move(eListbox.pageUp)
			else:
				pass
		else:
			pass

	def right(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "emud" and selection[1] != "backup":
				self["menu"].master.downstream_elements.move(eListbox.pageDown)
			else:
				pass
		else:
			pass

	def green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

		
	def red(self):
		pass

	def okbuttonClick(self):
		print "okbuttonClick"
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] == "ram":
				if fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/RAMclean.sh"):
					self.session.open(Console, title = "CLEAR RAM", cmdlist=["/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/RAMclean.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "epg":
				if fileExists("/var/bin/epgdownload.sh"):
					self.session.open(Console, title = "EPG DOWNLOAD", cmdlist=["/var/bin/epgdownload.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "setup":
				self.session.open(System)
			elif selection[1] == "emud":
				self.session.open(AltCamManager)
			elif selection[1] == "cifs":
				self.session.open(Cifs)
			elif selection[1] == "samba":
				self.session.open(Samba)
			elif selection[1] == "tuner":
				self.session.open(Tuner)
			elif selection[1] == "backup":
				if fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/backup.sh"):
					self.session.open(Console, title = "CREATE BACKUP", cmdlist=["/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/backup.sh"], closeOnSuccess = True)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "time":
				if fileExists("/var/bin/gmt.sh"):
					self.session.open(Console, title = "TIME DISPLAY", cmdlist=["/var/bin/on_gmt.sh"], closeOnSuccess = True)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "reset":
				if fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/reboot.sh"):
					self.session.open(Console, title = "FORCED RESET RECEIVER", cmdlist=["/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/reboot.sh"], closeOnSuccess = True)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "packet":
				self.session.open(Packet)
			elif selection[1] == "power":
				self.session.open(Power)

	def Exit(self):
		self.close()

class System(Screen):
	global HDSkn

	if HDSkn:
		skin="""
<screen name="System" position="110,60" size="1060,600" title="RUnigma Panel System" backgroundColor="#ffffffff" flags="wfNoBorder">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/fon.png" position="0,0" size="1060,600" zPosition="1" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/info.png" position="46,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/sysinfo.png" position="290,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/settings.png" position="533,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/DISKcontrol.png" position="782,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/wlan.png" position="46,223" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/addons.png" position="290,223" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/display.png" position="533,223" size="180,100" zPosition="3" alphatest="on" />
 <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/back.png" position="782,223" size="180,100" zPosition="3" alphatest="on" />
     <widget source="menu" render="Listbox" zPosition="3" transparent="1" position="1231, 196" size="490, 50" scrollbarMode="showOnDemand" foregroundColorSelected="#FFFFFF">
      <convert type="StringList" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_info</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_process</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_hdmi</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="755,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_disks</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_network</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_ci</convert>
      <convert type="ConditionalShowHide" />
    </widget>
        <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_display</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="755,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_back</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget name="type1"  position="46,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type2"  position="290,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type3"  position="533,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type4"  position="782,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type5"  position="46,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type6"  position="290,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type7" position="533,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type8"  position="782,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
     </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		list = []
		list.append((_("SYSTEM INFORMATION"), "info", "menu_info", "50"))
		list.append((_("NETWORK SETUP"), "network", "menu_network", "50"))
		list.append((_("RUNNING PROCESSES"), "process", "menu_process", "50"))
		list.append((_("CAM-MODULES"), "ci", "menu_ci", "50"))
		list.append((_("HDMI SETTINGS"), "hdmi", "menu_hdmi", "50"))
		list.append((_("RESET DISPLAY"), "display", "menu_display", "50"))
		list.append((_("USING DISKS"), "disks", "menu_disks", "50"))
		list.append((_("BACK"), "back", "menu_back", "50"))
		self["menu"] = List(list)
		self["type1"] = Label(_("SYSTEM INFORMATION"))
		self["type2"] = Label(_("RUNNING PROCESSES"))
		self["type3"] = Label(_("HDMI SETTINGS"))
		self["type4"] = Label(_("USING DISKS"))
		self["type5"] = Label(_("NETWORK SETUP"))
		self["type6"] = Label(_("CAM-MODULES"))
		self["type7"] = Label(_("RESET DISPLAY"))
		self["type8"] = Label(_("BACK"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "ListboxActions"],
			{
				"red": self.red,
				"green": self.green,
				"yellow": self.yellow,
				"blue": self.blue,
				"ok": self.okbuttonClick,
				"cancel": self.Exit,
				"up": self.up,
				"down": self.down,
				"left": self.left,
				"right": self.right,
			}, -2)

	def up(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "process" and selection[1] != "hdmi" and selection[1] != "disks":
				self["menu"].master.downstream_elements.move(eListbox.moveUp)
			else:
				pass
		else:
			pass

	def down(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "network" and selection[1] != "ci" and selection[1] != "display":
				self["menu"].master.downstream_elements.move(eListbox.moveDown)
			else:
				pass
		else:
			pass

	def left(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "network":
				self["menu"].master.downstream_elements.move(eListbox.pageUp)
			else:
				pass
		else:
			pass

	def right(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "disks":
				self["menu"].master.downstream_elements.move(eListbox.pageDown)
			else:
				pass
		else:
			pass

	def green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

		
	def red(self):
		pass

	def okbuttonClick(self):
		print "okbuttonClick"
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] == "info":
				if fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/sys_info.sh"):
					self.session.open(Console, title = "SYSTEM INFORMATION", cmdlist=["/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/sys_info.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "process":
				if fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/ps.sh"):
					self.session.open(Console, title = "RUNNING PROCESSES", cmdlist=["/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/ps.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "hdmi":
				self.session.open(Hdmi)
			elif selection[1] == "disks":
				self.session.open(Disks)
			elif selection[1] == "network":
				self.session.open(NetworkAdapterSelection)
			elif selection[1] == "ci":
				self.session.open(CiSelection)
			elif selection[1] == "display":
				if fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/display.sh"):
					self.session.open(Console, title = "RESET DISPLAY", cmdlist=["/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/display.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "back":
				self.Exit()

	def Exit(self):
		self.close()

class Hdmi(Screen):
	global HDSkn

	if HDSkn:
		skin="""
			 <screen name="Hdmi" position="110,60" size="1060,600" title="RUnigma Panel Hdmi" backgroundColor="#ffffffff" flags="wfNoBorder">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/fon.png" position="0,0" size="1060,600" zPosition="1" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/dts2.png" position="46,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/dts.png" position="290,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/sdparm.png" position="533,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/back.png" position="782,52" size="180,100" zPosition="3" alphatest="on" />
      <widget source="menu" render="Listbox" zPosition="3" transparent="1" position="1231, 196" size="490, 230" scrollbarMode="showOnDemand" foregroundColorSelected="#FFFFFF">
      <convert type="StringList" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_ac3</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_pcm</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_infotv</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="755,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_back</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget name="type1"  position="46,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type2"  position="290,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type3"  position="533,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type4" position="782,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
     </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		list = []
		list.append((_("ENABLE AC3"), "AC3", "menu_ac3", "50"))   
		list.append((_("ENABLE PCM"), "PCM", "menu_pcm", "50"))
		list.append((_("INFORMATION ON TV"), "infotv", "menu_infotv", "50"))
		list.append((_("BACK"), "back", "menu_back", "50"))
		self["menu"] = List(list)
		self["type1"] = Label(_("ENABLE AC3"))
		self["type2"] = Label(_("ENABLE PCM"))
		self["type3"] = Label(_("INFORMATION ON TV"))
		self["type4"] = Label(_("BACK"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "ListboxActions"],
			{
				"red": self.red,
				"green": self.green,
				"yellow": self.yellow,
				"blue": self.blue,
				"ok": self.okbuttonClick,
				"cancel": self.Exit,
				"up": self.up,
				"down": self.down,
				"left": self.left,
				"right": self.right,
			}, -2)

	def up(self):
		pass

	def down(self):
		pass

	def left(self):
		self["menu"].master.downstream_elements.move(eListbox.moveUp)

	def right(self):
		self["menu"].master.downstream_elements.move(eListbox.moveDown)

	def green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

	def red(self):
		pass

	def okbuttonClick(self):
		print "okbuttonClick"
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] == "AC3":
				self.session.open(Console, title = "ENABLE AC3", cmdlist=["hdmi-control -a spdif"], closeOnSuccess = False)
			elif selection[1] == "PCM":
				self.session.open(Console, title = "ENABLE PCM", cmdlist=["hdmi-control -a pcm"], closeOnSuccess = False)
			elif selection[1] == "infotv":
				self.session.open(Console, title = "INFORMATION ON TV", cmdlist=["hdmi-info -v |grep Display"])
			elif selection[1] == "back":
				self.Exit()

	def Exit(self):
		self.close()

class Disks(Screen):
	global HDSkn

	if HDSkn:
		skin="""
			 <screen name="Blupanel System" position="110,60" size="1060,600" title="RUnigma Panel System" backgroundColor="#ffffffff" flags="wfNoBorder">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/fon.png" position="0,0" size="1060,600" zPosition="1" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd1.png" position="46,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd2.png" position="290,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd3.png" position="533,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd4.png" position="782,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd5.png" position="46,223" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd6.png" position="290,223" size="180,100" zPosition="3" alphatest="on" />
 <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/back.png" position="533,223" size="180,100" zPosition="3" alphatest="on" />
     <widget source="menu" render="Listbox" zPosition="3" transparent="1" position="1231, 196" size="490, 50" scrollbarMode="showOnDemand" foregroundColorSelected="#FFFFFF">
      <convert type="StringList" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_info</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_process</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_hdmi</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="755,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_disks</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_network</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_ci</convert>
      <convert type="ConditionalShowHide" />
    </widget>
        <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_back</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget name="type1"  position="46,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type2"  position="290,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type3"  position="533,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type4"  position="782,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type5"  position="46,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type6"  position="290,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type7" position="533,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
     </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		list = []
		list.append((_("Mounted disk in / hdd / movie"), "mount", "menu_info", "50"))
		list.append((_("Contents of the folder / hdd / movie"), "content", "menu_network", "50"))
		list.append((_("SHOW mount"), "showmount", "menu_process", "50"))
		list.append((_("Unmount the disk from / hdd / movie"), "unmount", "menu_ci", "50"))
		list.append((_("SHOW ALL DISCS"), "showall", "menu_hdmi", "50"))
		list.append((_("BACK"), "back", "menu_back", "50"))
		list.append((_("SHOW MOUNT DISKS"), "show disks", "menu_disks", "50"))
		self["menu"] = List(list)
		self["type1"] = Label(_("Mounted disk in / hdd / movie"))
		self["type2"] = Label(_("SHOW mount"))
		self["type3"] = Label(_("SHOW ALL DISCS"))
		self["type4"] = Label(_("SHOW MOUNT DISKS"))
		self["type5"] = Label(_("Contents of the folder / hdd / movie"))
		self["type6"] = Label(_("Unmount the disk from / hdd / movie"))
		self["type7"] = Label(_("BACK"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "ListboxActions"],
			{
				"red": self.red,
				"green": self.green,
				"yellow": self.yellow,
				"blue": self.blue,
				"ok": self.okbuttonClick,
				"cancel": self.Exit,
				"up": self.up,
				"down": self.down,
				"left": self.left,
				"right": self.right,
			}, -2)

	def up(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "showmount" and selection[1] != "showall":
				self["menu"].master.downstream_elements.move(eListbox.moveUp)
			else:
				pass
		else:
			pass

	def down(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "content" and selection[1] != "unmount" and selection[1] != "back":
				self["menu"].master.downstream_elements.move(eListbox.moveDown)
			else:
				pass
		else:
			pass

	def left(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "content":
				self["menu"].master.downstream_elements.move(eListbox.pageUp)
			else:
				pass
		else:
			pass

	def right(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "back":
				self["menu"].master.downstream_elements.move(eListbox.pageDown)
			else:
				pass
		else:
			pass

	def green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

		
	def red(self):
		pass

	def okbuttonClick(self):
		print "okbuttonClick"
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] == "mount":
				self.session.open(Disks2)
			elif selection[1] == "showmount":
				self.session.open(Console, title = "SHOW mount", cmdlist=["df -h /hdd/movie"])
			elif selection[1] == "showall":
				self.session.open(Console, title = "ALL DISCS", cmdlist=["df -h"])
			elif selection[1] == "show disks":
				self.session.open(Console, title = "ALL DISCS", cmdlist=["mount"])
			elif selection[1] == "content":
				self.session.open(Console, title = "SHOW MOUNT DISKS", cmdlist=["ls /hdd/movie"])
			elif selection[1] == "unmount":
				self.session.open(Console, title = "SHOW MOUNT DISKS", cmdlist=["umount /hdd/movie"])
			elif selection[1] == "back":
				self.Exit()

	def Exit(self):
		self.close()

class Disks2(Screen):
	global HDSkn

	if HDSkn:
	
		skin="""
			 <screen name="Blupanel System" position="110,60" size="1060,600" title="RUnigma Panel System" backgroundColor="#ffffffff" flags="wfNoBorder">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/fon.png" position="0,0" size="1060,600" zPosition="1" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd1.png" position="46,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd2.png" position="290,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd3.png" position="533,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd4.png" position="782,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd5.png" position="46,223" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/hdd6.png" position="290,223" size="180,100" zPosition="3" alphatest="on" />
 <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/back.png" position="533,223" size="180,100" zPosition="3" alphatest="on" />
     <widget source="menu" render="Listbox" zPosition="3" transparent="1" position="1231, 196" size="490,50" scrollbarMode="showOnDemand" foregroundColorSelected="#FFFFFF">
      <convert type="StringList" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_info</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_process</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_hdmi</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="755,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_disks</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_network</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_ci</convert>
      <convert type="ConditionalShowHide" />
    </widget>
        <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,213" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_back</convert>
      <convert type="ConditionalShowHide" />
    </widget>

    <widget name="type1"  position="46,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type2"  position="290,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type3"  position="533,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type4"  position="782,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type5"  position="46,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type6"  position="290,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type7" position="533,331" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
     </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		list = []
		list.append((_("Mount /dev/sda1"), "mount", "menu_info", "50"))
		list.append((_("Mount /dev/sdb2"), "content", "menu_network", "50"))
		list.append((_("Mount /dev/sda2"), "showmount", "menu_process", "50"))
		list.append((_("Mount /dev/sdb3"), "unmount", "menu_ci", "50"))
		list.append((_("Mount /dev/sda5"), "showall", "menu_hdmi", "50"))
		list.append((_("BACK"), "back", "menu_back", "50"))
		list.append((_("Mount /dev/sdb1"), "show disks", "menu_disks", "50"))
		self["type1"] = Label(_("Mount /dev/sda1"))
		self["type2"] = Label(_("Mount /dev/sda2"))
		self["type3"] = Label(_("Mount /dev/sda5"))
		self["type4"] = Label(_("Mount /dev/sdb1"))
		self["type5"] = Label(_("Mount /dev/sdb2"))
		self["type6"] = Label(_("Mount /dev/sdb3"))
		self["type7"] = Label(_("BACK"))
		self["menu"] = List(list)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "ListboxActions"],
			{
				"red": self.red,
				"green": self.green,
				"yellow": self.yellow,
				"blue": self.blue,
				"ok": self.okbuttonClick,
				"cancel": self.Exit,
				"up": self.up,
				"down": self.down,
				"left": self.left,
				"right": self.right,
			}, -2)

	def up(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "showmount" and selection[1] != "showall":
				self["menu"].master.downstream_elements.move(eListbox.moveUp)
			else:
				pass
		else:
			pass

	def down(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "content" and selection[1] != "unmount" and selection[1] != "back":
				self["menu"].master.downstream_elements.move(eListbox.moveDown)
			else:
				pass
		else:
			pass

	def left(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "content":
				self["menu"].master.downstream_elements.move(eListbox.pageUp)
			else:
				pass
		else:
			pass

	def right(self):
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] != "back":
				self["menu"].master.downstream_elements.move(eListbox.pageDown)
			else:
				pass
		else:
			pass

	def green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

		
	def red(self):
		pass

	def okbuttonClick(self):
		print "okbuttonClick"
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] == "mount":
				self.session.open(Console, title = "SHOW MOUNT DISKS", cmdlist=["mount /dev/sda1 /hdd/movie"], closeOnSuccess = False)
			elif selection[1] == "showmount":
				self.session.open(Console, title = "SHOW mount", cmdlist=["mount /dev/sda2 /hdd/movie"], closeOnSuccess = False)
			elif selection[1] == "showall":
				self.session.open(Console, title = "ALL DISCS", cmdlist=["mount /dev/sda5 /hdd/movie"], closeOnSuccess = False)
			elif selection[1] == "show disks":
				self.session.open(Console, title = "ALL DISCS", cmdlist=["mount /dev/sdb1 /hdd/movie"], closeOnSuccess = False)
			elif selection[1] == "content":
				self.session.open(Console, title = "SHOW MOUNT DISKS", cmdlist=["mount /dev/sdb2 /hdd/movie"], closeOnSuccess = False)
			elif selection[1] == "unmount":
				self.session.open(Console, title = "SHOW MOUNT DISKS", cmdlist=["mount /dev/sdb3 /hdd/movie"], closeOnSuccess = False)
			elif selection[1] == "back":
				self.Exit()

	def Exit(self):
		self.close()

class Cifs(Screen):
	global HDSkn

	if HDSkn:
		skin="""
			 <screen name="Blupanel System" position="110,60" size="1060,600" title="RUnigma Panel System" backgroundColor="#ffffffff" flags="wfNoBorder">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/fon.png" position="0,0" size="1060,600" zPosition="1" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/dts2.png" position="46,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/dts.png" position="290,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/back.png" position="533,52" size="180,100" zPosition="3" alphatest="on" />
      <widget source="menu" render="Listbox" zPosition="3" transparent="1" position="1231, 196" size="490, 230" scrollbarMode="showOnDemand" foregroundColorSelected="#FFFFFF">
      <convert type="StringList" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_ac3</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_pcm</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_back</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget name="type1"  position="46,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type2"  position="290,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type3" position="533,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
        </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		list = []
		list.append((_("CONNECT CIFS"), "AC3", "menu_ac3", "50"))   
		list.append((_("DISABLE CIFS"), "PCM", "menu_pcm", "50"))
		list.append((_("BACK"), "back", "menu_back", "50"))
		self["menu"] = List(list)
		self["type1"] = Label(_("CONNECT CIFS"))
		self["type2"] = Label(_("DISABLE CIFS"))
		self["type3"] = Label(_("BACK"))

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "ListboxActions"],
			{
				"red": self.red,
				"green": self.green,
				"yellow": self.yellow,
				"blue": self.blue,
				"ok": self.okbuttonClick,
				"cancel": self.Exit,
				"up": self.up,
				"down": self.down,
				"left": self.left,
				"right": self.right,
			}, -2)

	def up(self):
		pass

	def down(self):
		pass

	def left(self):
		self["menu"].master.downstream_elements.move(eListbox.moveUp)

	def right(self):
		self["menu"].master.downstream_elements.move(eListbox.moveDown)

	def green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

	def red(self):
		pass

	def okbuttonClick(self):
		print "okbuttonClick"
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] == "AC3":
				if fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/cifs_start.sh"):
					self.session.open(Console, title = "CONNECT CIFS", cmdlist=["/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/cifs_start.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "PCM":
				if fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/cifs_stop.sh"):
					self.session.open(Console, title = "DISABLE CIFS", cmdlist=["/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/cifs_stop.sh"], closeOnSuccess = False)	
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "back":
				self.Exit()

	def Exit(self):
		self.close()

class Samba(Screen):
	global HDSkn

	if HDSkn:
		skin="""
			 <screen name="Blupanel System" position="110,60" size="1060,600" title="RUnigmaPanel Samba" backgroundColor="#ffffffff" flags="wfNoBorder">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/fon.png" position="0,0" size="1060,600" zPosition="1" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/lang.png" position="46,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/lang2.png" position="290,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/lang3.png" position="533,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/back.png" position="782,52" size="180,100" zPosition="3" alphatest="on" />
      <widget source="menu" render="Listbox" zPosition="3" transparent="1" position="1231, 196" size="490, 230" scrollbarMode="showOnDemand" foregroundColorSelected="#FFFFFF">
      <convert type="StringList" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_ac3</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_pcm</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_restart</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="755,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_back</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget name="type1"  position="46,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type2"  position="290,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type3"  position="533,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type4" position="782,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
        </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		list = []
		list.append((_("STARTING SAMBA"), "AC3", "menu_ac3", "50"))   
		list.append((_("STOP SAMBA"), "PCM", "menu_pcm", "50"))
		list.append((_("RESTART SAMBA"), "restart", "menu_restart", "50"))
		list.append((_("BACK"), "back", "menu_back", "50"))
		self["menu"] = List(list)
		self["type1"] = Label(_("STARTING SAMBA"))
		self["type2"] = Label(_("STOP SAMBA"))
		self["type3"] = Label(_("RESTART SAMBA"))
		self["type4"] = Label(_("BACK"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "ListboxActions"],
			{
				"red": self.red,
				"green": self.green,
				"yellow": self.yellow,
				"blue": self.blue,
				"ok": self.okbuttonClick,
				"cancel": self.Exit,
				"up": self.up,
				"down": self.down,
				"left": self.left,
				"right": self.right,
			}, -2)

	def up(self):
		pass

	def down(self):
		pass

	def left(self):
		self["menu"].master.downstream_elements.move(eListbox.moveUp)

	def right(self):
		self["menu"].master.downstream_elements.move(eListbox.moveDown)

	def green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

		
	def red(self):
		pass

	def okbuttonClick(self):
		print "okbuttonClick"
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] == "AC3":
				if fileExists("/var/bin/samba_start.sh"):
					self.session.open(Console, title = "STARTING SAMBA", cmdlist=["/var/bin/samba_start.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "PCM":
				if fileExists("/var/bin/samba_stop.sh"):
					self.session.open(Console, title = "STOP SAMBA", cmdlist=["/var/bin/samba_stop.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "restart":
				if fileExists("/var/bin/samba_restart.sh"):
					self.session.open(Console, title = "RESTART SAMBA", cmdlist=["/var/bin/samba_restart.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "back":
				self.Exit()

	def Exit(self):
		self.close()

class Tuner(Screen):
	global HDSkn

	if HDSkn:
	
		skin="""
			 <screen name="Blupanel System" position="110,60" size="1060,600" title="RUnigmaPanel Tuner" backgroundColor="#ffffffff" flags="wfNoBorder">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/fon.png" position="0,0" size="1060,600" zPosition="1" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/tunerST.png" position="46,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/tunerRB.png" position="290,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/back.png" position="533,52" size="180,100" zPosition="3" alphatest="on" />
      <widget source="menu" render="Listbox" zPosition="3" transparent="1" position="1231, 196" size="490, 230" scrollbarMode="showOnDemand" foregroundColorSelected="#FFFFFF">
      <convert type="StringList" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_ac3</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_pcm</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_back</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget name="type1"  position="46,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type2" position="290,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type3" position="533,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
        </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		list = []
		list.append((_("ACTIVATE TUNER ST"), "AC3", "menu_ac3", "50"))   
		list.append((_("ACTIVATE TUNER RB"), "PCM", "menu_pcm", "50"))
		list.append((_("BACK"), "back", "menu_back", "50"))
		self["menu"] = List(list)
		self["type1"] = Label(_("ACTIVATE TUNER ST"))
		self["type2"] = Label(_("ACTIVATE TUNER RB"))
		self["type3"] = Label(_("BACK"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "ListboxActions"],
			{
				"red": self.red,
				"green": self.green,
				"yellow": self.yellow,
				"blue": self.blue,
				"ok": self.okbuttonClick,
				"cancel": self.Exit,
				"up": self.up,
				"down": self.down,
				"left": self.left,
				"right": self.right,
			}, -2)
		
	def up(self):
		pass

	def down(self):
		pass

	def left(self):
		self["menu"].master.downstream_elements.move(eListbox.moveUp)

	def right(self):
		self["menu"].master.downstream_elements.move(eListbox.moveDown)

	def green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

		
	def red(self):
		pass

	def okbuttonClick(self):
		print "okbuttonClick"
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] == "AC3":
				if fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/ST_Tuner_start.sh"):
					self.session.open(Console, title = "ACTIVATE TUNER ST", cmdlist=["/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/ST_Tuner_start.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "PCM":
				if fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/RB_Tuner_start.sh"):
					self.session.open(Console, title = "ACTIVATE TUNER RB", cmdlist=["/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/RB_Tuner_start.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "back":
				self.Exit()

	def Exit(self):
		self.close()

class Power(Screen):
	global HDSkn

	if HDSkn:
	
		skin="""
			 <screen name="Blupanel System" position="110,60" size="1060,600" title="RUnigmaPanel Power PC" backgroundColor="#ffffffff" flags="wfNoBorder">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/fon.png" position="0,0" size="1060,600" zPosition="1" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/poweron.png" position="46,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/power2.png" position="290,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/power3.png" position="533,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/back.png" position="782,52" size="180,100" zPosition="3" alphatest="on" />
      <widget source="menu" render="Listbox" zPosition="3" transparent="1" position="1231, 196" size="490, 230" scrollbarMode="showOnDemand" foregroundColorSelected="#FFFFFF">
      <convert type="StringList" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_ac3</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_pcm</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_restart</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="755,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_back</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget name="type1"  position="46,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type2"  position="290,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type3"  position="533,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type4" position="782,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
        </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		list = []
		list.append((_("TURN ON THE COMPUTER"), "AC3", "menu_ac3", "50"))   
		list.append((_("TURN OFF THE COMPUTER"), "PCM", "menu_pcm", "50"))
		list.append((_("RESTART THE COMPUTER"), "restart", "menu_restart", "50"))
		list.append((_("BACK"), "back", "menu_back", "50"))
		self["menu"] = List(list)
		self["type1"] = Label(_("TURN ON THE COMPUTER"))
		self["type2"] = Label(_("TURN OFF THE COMPUTER"))
		self["type3"] = Label(_("RESTART THE COMPUTER"))
		self["type4"] = Label(_("BACK"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "ListboxActions"],
			{
				"red": self.red,
				"green": self.green,
				"yellow": self.yellow,
				"blue": self.blue,
				"ok": self.okbuttonClick,
				"cancel": self.Exit,
				"up": self.up,
				"down": self.down,
				"left": self.left,
				"right": self.right,
			}, -2)

	def up(self):
		pass

	def down(self):
		pass

	def left(self):
		self["menu"].master.downstream_elements.move(eListbox.moveUp)

	def right(self):
		self["menu"].master.downstream_elements.move(eListbox.moveDown)

	def green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

		
	def red(self):
		pass

	def okbuttonClick(self):
		print "okbuttonClick"
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] == "AC3":
				if fileExists("/var/bin/powerPC-on.sh"):
					self.session.open(Console, title = "TURN ON THE COMPUTER", cmdlist=["/var/bin/powerPC-on.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "PCM":
				if fileExists("/var/bin/powerPC-off.sh"):
					self.session.open(Console, title = "TURN OFF THE COMPUTER", cmdlist=["/var/bin/powerPC-off.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "restart":
				if fileExists("/var/bin/powerPC-reboot.sh"):
					self.session.open(Console, title = "RESTART THE COMPUTER", cmdlist=["/var/bin/powerPC-reboot.sh"], closeOnSuccess = False)
				else:
					self.session.open(MessageBox, ("Not installed. Please install"), MessageBox.TYPE_INFO, timeout=5)
			elif selection[1] == "back":
				self.Exit()

	def Exit(self):
		self.close()

class Packet(Screen):
	global HDSkn

	if HDSkn:
	
		skin="""
			 <screen name="Blupanel System" position="110,60" size="1060,600" title="RUnigmaPanel Tuner" backgroundColor="#ffffffff" flags="wfNoBorder">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/fon.png" position="0,0" size="1060,600" zPosition="1" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/swapch.png" position="46,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/swap.png" position="290,52" size="180,100" zPosition="3" alphatest="on" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/back.png" position="533,52" size="180,100" zPosition="3" alphatest="on" />
      <widget source="menu" render="Listbox" zPosition="3" transparent="1" position="1231, 196" size="490, 230" scrollbarMode="showOnDemand" foregroundColorSelected="#FFFFFF">
      <convert type="StringList" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="22,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_ac3</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="266,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_pcm</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget source="menu" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/SystemPlugins/RUnigmaPanel/icon/frame.png" position="510,42" size="231,164" zPosition="2" alphatest="on">
      <convert type="MenuEntryCompare">menu_back</convert>
      <convert type="ConditionalShowHide" />
    </widget>
    <widget name="type1"  position="46,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type2"  position="290,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
    <widget name="type3" position="533,160" size="180,42" backgroundColor="#00000000"  font="Regular; 16" transparent="1" zPosition="3" halign="center" valign="top" />
        </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		list = []
		list.append((_("Include highSR"), "AC3", "menu_ac3", "50"))   
		list.append((_("Disable highSR"), "PCM", "menu_pcm", "50"))
		list.append((_("BACK"), "back", "menu_back", "50"))
		self["menu"] = List(list)
		self["type1"] = Label(_("Include highSR"))
		self["type2"] = Label(_("Disable highSR"))
		self["type3"] = Label(_("BACK"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "ListboxActions"],
			{
				"red": self.red,
				"green": self.green,
				"yellow": self.yellow,
				"blue": self.blue,
				"ok": self.okbuttonClick,
				"cancel": self.Exit,
				"up": self.up,
				"down": self.down,
				"left": self.left,
				"right": self.right,
			}, -2)

	def up(self):
		pass

	def down(self):
		pass

	def left(self):
		self["menu"].master.downstream_elements.move(eListbox.moveUp)

	def right(self):
		self["menu"].master.downstream_elements.move(eListbox.moveDown)

	def green(self):
		pass

	def yellow(self):
		pass

	def blue(self):
		pass

		
	def red(self):
		pass

	def okbuttonClick(self):
		print "okbuttonClick"
		selection = self["menu"].getCurrent()
		if selection is not None:
			if selection[1] == "AC3":
				self.session.open(Console, title = "Include highSR", cmdlist=["/bin/stfbcontrol he"], closeOnSuccess = False)
			elif selection[1] == "PCM":
				self.session.open(Console, title = "Disable highSR", cmdlist=["/bin/stfbcontrol hdh"], closeOnSuccess = False)
			elif selection[1] == "back":
				self.Exit()

	def Exit(self):
		self.close()

class PanelServiceList(Screen):
	def __init__(self, session, service):
		Screen.__init__(self, session)
		self.session = session

		if service is not None:
			servicelist = service
		else:
			servicelist = None
#------------------------------------------------------------------------------------------

def main(session, **kwargs):
	global HDSkn
	if fileExists("/usr/share/enigma2/skin_default/buttons/red .png"):
		if HDSkn:
			session.open(MenuBlupanel)
		else:
			session.open(MessageBox, (_("Sorry! Not suport SD skins")), MessageBox.TYPE_INFO, timeout=10)
	else:
		session.open(MessageBox, (_("Sorry! It not RUnigma3! Good-bye!")), MessageBox.TYPE_INFO, timeout=10)

def menu(menuid, **kwargs):
	if menuid == "mainmenu":
		return [(_("RUnigmaPanel"), main, "bp_mainmenu", 45)]
	return []
	
def Plugins(**kwargs):
	return [
		PluginDescriptor(name = "RUnigmaPanel", description = "RUnigmaPanel", icon="plugin.png", where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main),
        PluginDescriptor(name = "RUnigmaPanel", description = "RUnigmaPanel", icon="plugin.png", where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main),
		PluginDescriptor(name = "RUnigmaPanel", description = "RUnigmaPanel", where = PluginDescriptor.WHERE_MENU, fnc = menu)]
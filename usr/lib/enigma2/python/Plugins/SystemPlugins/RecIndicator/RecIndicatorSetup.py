#
# Record Indicator Plugin for Enigma2
# Coded by vlamo (c) 2012
#
# Version: 1.0-rc0 (17.01.2012 00:22)
# Support: http://dream.altmaster.net/
#

from Screens.Screen import Screen
from Components.Sources.StaticText import StaticText
from Components.ActionMap import NumberActionMap
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry





class RecIndicatorSetupScreen(Screen, ConfigListScreen):
	def __init__(self, session, args = None):
		Screen.__init__(self, session)
		self.skinName = ["RecIndicatorrSetup", "Setup"]
		self.setup_title = _("Record Indicator Setup")

		self["key_green"] = StaticText(_("Save"))
		self["key_red"] = StaticText(_("Cancel"))
		self["actions"] = NumberActionMap(["SetupActions"],
		{
			"cancel": self.keyRed,	# KEY_RED, KEY_ESC
			"ok": self.keyOk,	# KEY_OK
			"save": self.keyGreen,	# KEY_GREEN
		}, -1)

		ConfigListScreen.__init__(self, [])

		self.initConfig()
		self.createSetup()

		self.onClose.append(self.__closed)
		self.onLayoutFinish.append(self.__layoutFinished)

	def __closed(self):
		pass

	def __layoutFinished(self):
		self.setTitle(self.setup_title)

	def initConfig(self):
		self.RIC = config.plugins.RecIndicator
		self.prev_enable = self.RIC.enable.value
		self.prev_X = self.RIC.x.value
		self.prev_Y = self.RIC.y.value
		self.cfg_enable = getConfigListEntry(_("enable record indicator"), self.RIC.enable)
		self.cfg_x = getConfigListEntry(_("X position (upper-left corner of srceen)"), self.RIC.x)
		self.cfg_y = getConfigListEntry(_("Y position (upper-left corner of srceen)"), self.RIC.y)

	def createSetup(self):
		list = [ self.cfg_enable ]
		if self.RIC.enable.value:
			list.append(self.cfg_x)
			list.append(self.cfg_y)
		self["config"].list = list
		self["config"].l.setList(list)

	def newConfig(self):
		cur = self["config"].getCurrent()
		if cur == self.cfg_enable:
			self.createSetup()

	def keyOk(self):
		pass

	def keyRed(self):
		self.RIC.enable.value = self.prev_enable
		self.RIC.x.value = self.prev_X
		self.RIC.y.value = self.prev_Y
		self.keyGreen()

	def keyGreen(self):
		self.RIC.enable.save()
		self.RIC.x.save()
		self.RIC.y.save()
		self.close()

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.newConfig()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.newConfig()


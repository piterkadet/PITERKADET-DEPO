# -*- coding: utf-8 -*-

from . import _
from Components.ActionMap import ActionMap
from Components.Pixmap import Pixmap, MultiPixmap
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.config import config, getConfigListEntry, ConfigSubsection
from Components.Button import Button
from Tools.Directories import fileExists

class AdvancedStartupToStandbyScreen(Screen, ConfigListScreen):
	skin = """
		<screen position="center,center" size="640,410" >
		<widget name="config" position="10,45" size="620,230" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="490,0" zPosition="0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="10,0" zPosition="0" size="140,40" alphatest="on" />
		<widget name="ok" position="490,0" size="140,40" valign="center" halign="center" zPosition="1" font="Regular;20" transparent="1" backgroundColor="green" />
		<widget name="cancel" position="10,0" size="140,40" valign="center" halign="center" zPosition="1" font="Regular;20" transparent="1" backgroundColor="red" />
		<ePixmap pixmap="skin_default/div-h.png" position="0,290" zPosition="1" size="640,2" />
		<widget name="help" position="10,300" size="620,110" zPosition="1" font="Regular;19" transparent="1" />
	</screen>
	"""
	def __init__(self, session, args = None):
		self.skin = AdvancedStartupToStandbyScreen.skin
		self.setup_title = _("Setup Advanced StartupToStandby")
		Screen.__init__(self, session)

		self["ok"] = Button(_("Save"))
		self["cancel"] = Button(_("Cancel"))
		self["help"] = Label("")
		self["actions"] = ActionMap(["SetupActions", "ColorActions"], 
		{
			"ok": self.keyOk,
			"save": self.keyGreen,
			"cancel": self.keyRed,
		}, -1)

		ConfigListScreen.__init__(self, [])
		self.initConfig()
		self.createSetup()
		self.onClose.append(self.__closed)
		self.onLayoutFinish.append(self.__layoutFinished)
		self["config"].onSelectionChanged.append(self.textHelp)

	def __closed(self):
		pass

	def __layoutFinished(self):
		self.setTitle(self.setup_title)
		
	def initConfig(self):
		def getPrevValues(section):
			res = { }
			for (key,val) in section.content.items.items():
				if isinstance(val, ConfigSubsection):
					res[key] = getPrevValues(val)
				else:
					res[key] = val.value
			return res

		self.AST = config.plugins.AdvancedstartupToStandby
		self.prev_values = getPrevValues(self.AST)
		self.cfg_standbyenabled = getConfigListEntry(_("Set standby after startup"), self.AST.standbyEnabled)
		self.cfg_holiday = getConfigListEntry(_("Holiday mode"), self.AST.deepstandbyHoliday)
		self.cfg_standbymode = getConfigListEntry(_("Choose profile system"), self.AST.standbyMode)
		self.cfg_autoboot = getConfigListEntry(_("Standby on auto boot"), self.AST.standbyOnAutoBoot)
		self.cfg_afterevent = getConfigListEntry(_("Type 'After event' for record timer"), self.AST.standbyAfterEevent)
		self.cfg_zaptimer = getConfigListEntry(_("No standby for zap timer"), self.AST.standbyNoForZaptimer)
		self.cfg_manualboot  = getConfigListEntry(_("Standby on manual boot"), self.AST.standbyOnManualBoot)
		self.cfg_restart  = getConfigListEntry(_("No standby on restart GUI"), self.AST.standbyOnRestart)
		self.cfg_timeout = getConfigListEntry(_("Message timeout (sec.)"), self.AST.standbyTimeout)

	def createSetup(self):
		list = [ self.cfg_standbyenabled ]
		if self.AST.standbyEnabled.value:
			list.append(self.cfg_holiday)
			if not self.AST.deepstandbyHoliday.value:
				list.append(self.cfg_standbymode)
				list.append(self.cfg_autoboot)
				if self.AST.standbyOnAutoBoot.value != "2":
					list.append(self.cfg_afterevent)
					if self.AST.standbyOnAutoBoot.value == "0":
						list.append(self.cfg_zaptimer)
				list.append(self.cfg_manualboot)
				if self.AST.standbyOnManualBoot.value:
					list.append(self.cfg_restart)
			list.append(self.cfg_timeout)
		self["config"].list = list
		self["config"].l.setList(list)

	def newConfig(self):
		cur = self["config"].getCurrent()
		if cur in (self.cfg_standbyenabled, self.cfg_holiday, self.cfg_autoboot, self.cfg_manualboot):
			self.createSetup()

	def keyOk(self):
		pass

	def textHelp(self):
		self["help"].setText("")
		idx = self["config"].getCurrent()[1]
		if idx == self.AST.standbyEnabled:
			self["help"].setText(_("Enable / disable plugin to transfer your receiver to power saving mode."))
		elif idx == self.AST.deepstandbyHoliday:
			self["help"].setText(_("When enabled, the receiver is always translated into deep standby, except for the inclusion on the timer recording."))
		elif idx == self.AST.standbyMode:
			self["help"].setText(_("Alternative profile is required for receivers no which the function 'was_timer_wakeup' (for example: et4000). In this case, the booting of additional plugins (Elektro, Autotimer, etc.) equivalent to manual booting."))
		elif idx == self.AST.standbyOnAutoBoot:
			self["help"].setText(_("If this mode is enabled, the receiver will go into standby mode after the automatic booting."))
		elif idx == self.AST.standbyAfterEevent:
			self["help"].setText(_("Select the type of 'After event' for timer recording to go into standby mode. Timers for the type of 'auto' goes into standby mode automatically, without displaying message."))
		elif idx == self.AST.standbyNoForZaptimer:
			self["help"].setText(_("If this mode is enabled, the receiver will not go into standby mode when the timer zap."))
		elif idx == self.AST.standbyOnManualBoot:
			self["help"].setText(_("If this mode is enabled, the receiver will go into standby mode after manual booting."))
		elif idx == self.AST.standbyOnRestart:
			self["help"].setText(_("When enabled, the receiver will not go into standby mode after restart GUI."))
		elif idx == self.AST.standbyTimeout:
			self["help"].setText(_("Timeout message to the action in seconds. 0 - without displaying message."))
			

	def keyRed(self):
		def setPrevValues(section, values):
			for (key,val) in section.content.items.items():
				value = values.get(key, None)
				if value is not None:
					if isinstance(val, ConfigSubsection):
						setPrevValues(val, value)
					else:
						val.value = value
		setPrevValues(self.AST, self.prev_values)
		self.keyGreen()

	def keyGreen(self):
		flag = '/tmp/.answer_boot'
		if not self.AST.standbyEnabled.value:
			self.AST.standbyMode.value = "0"
			self.AST.standbyOnAutoBoot.value = "2"
			self.AST.standbyAfterEevent.value = "0"
			self.AST.standbyNoForZaptimer.value = False
			self.AST.standbyTimeout.value = 30
			self.AST.standbyOnRestart.value = False
			self.AST.standbyOnManualBoot.value = False
			self.AST.deepstandbyHoliday.value  = False
		if self.AST.standbyOnAutoBoot.value == "2":
			self.AST.standbyAfterEevent.value = "0"
		if self.AST.standbyOnAutoBoot.value != "0":
			self.AST.standbyNoForZaptimer.value = False
		if not self.AST.standbyOnManualBoot.value:
			self.AST.standbyOnRestart.value = False
		if self.AST.standbyEnabled.value:
			if self.AST.standbyMode.value == "0" and self.AST.standbyOnManualBoot.value and self.AST.standbyOnRestart.value:
				if not fileExists(flag):
					self.writeAnswerBoot()
			if self.AST.standbyMode.value == "1" and self.AST.standbyOnManualBoot.value:
				if not fileExists(flag):
					self.writeAnswerBoot()
		try:
			same_options = config.plugins.RecInfobar.check_wakeup.value
		except:
			same_options = False
		if same_options:
			if self.AST.standbyOnAutoBoot.value != "2" or self.AST.standbyOnManualBoot.value or self.AST.deepstandbyHoliday.value:
				self.session.open(MessageBox, _("Similar option used in the plugin \"Record Infobar\" !\nTurning off this option."), MessageBox.TYPE_INFO, timeout = 5)
				config.plugins.RecInfobar.check_wakeup.value = False
				config.plugins.RecInfobar.check_wakeup.save()
		self.AST.save()
		self.close()

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.newConfig()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.newConfig()

	def writeAnswerBoot(self):
		flag = '/tmp/.answer_boot'
		try:
			fd = open(flag, 'w')
			fd.write(0)
			fd.close()
		except:
			pass
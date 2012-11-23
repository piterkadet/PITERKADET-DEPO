# -*- coding: utf-8 -*-
#
# Advanced StartupToStandby Plugin
# Coded by Dima73 (c) 2012
# Version: 1.0(10.11.2012)
#

from . import _
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.config import config, ConfigSubsection, getConfigListEntry, ConfigYesNo, ConfigEnableDisable, ConfigInteger, ConfigSelection
from Screens.MessageBox import MessageBox
try:
	from Tools.StbHardware import getFPWasTimerWakeup
except:
	from Tools.DreamboxHardware import getFPWasTimerWakeup
from RecordTimer import AFTEREVENT, RecordTimer
from Screens import Standby 
from Tools import Notifications
from Tools.Directories import fileExists
import NavigationInstance
import AdvancedStartupToStandbySetup
from enigma import eTimer
from time import time as Time
import os

session = None

config.plugins.AdvancedstartupToStandby = ConfigSubsection()
config.plugins.AdvancedstartupToStandby.standbyEnabled = ConfigEnableDisable(default = False)
config.plugins.AdvancedstartupToStandby.standbyMode = ConfigSelection([("0", _("standard profile")),("1", _("alternative profile"))], default="0")
config.plugins.AdvancedstartupToStandby.standbyOnAutoBoot = ConfigSelection([("0", _("always")),("1", _("only for timer recording")),("2", _("newer"))], default="2")
config.plugins.AdvancedstartupToStandby.standbyAfterEevent = ConfigSelection([("0", _("all")),("1", _("standby")),("2", _("deep standby")),("3", _("auto")),("4", _("auto and deep standby")),("5", _("all, than to do 'nothing'"))], default="0")
config.plugins.AdvancedstartupToStandby.standbyNoForZaptimer = ConfigYesNo(default = False)
config.plugins.AdvancedstartupToStandby.standbyOnManualBoot = ConfigYesNo(default = False)
config.plugins.AdvancedstartupToStandby.standbyOnRestart = ConfigYesNo(default = False)
config.plugins.AdvancedstartupToStandby.deepstandbyHoliday = ConfigYesNo(default = False)
config.plugins.AdvancedstartupToStandby.standbyTimeout = ConfigInteger(default = 30, limits= (0, 120))


class DoStandby(Screen):
	skin = """ <screen position="center,center" size="300,300" title="" > </screen>"""
	
	def __init__(self,session):
		Screen.__init__(self,session)
		self.session = session
		self.AST = config.plugins.AdvancedstartupToStandby
		self.recordTimerWakeup = False
		self.CheckAnswer = False
		flag = '/tmp/.answer_boot'
		try:
			same_options = config.plugins.RecInfobar.check_wakeup.value
		except:
			same_options = False
		if same_options:
			if self.AST.standbyOnAutoBoot.value != "2" or self.AST.standbyOnManualBoot.value or self.AST.deepstandbyHoliday.value:
				config.plugins.RecInfobar.check_wakeup.value = False
				config.plugins.RecInfobar.check_wakeup.save()
		if self.AST.deepstandbyHoliday.value:
			if abs(self.session.nav.RecordTimer.getNextRecordingTime() - Time()) <= 360:
				print "Advanced StartupToStandby: record timer is - no deep standby"
			else:
				self.CheckAnswer = True
				self.recordTimerWakeup = True
				self.GoDeepStandby()
				return
		if self.AST.standbyMode.value == "0": 
			if Standby.inStandby is None:
				if not getFPWasTimerWakeup():
					if self.AST.standbyOnManualBoot.value:
						if fileExists(flag):
							if not self.AST.standbyOnRestart.value:
								self.GoStandby()
							else:
								print "Advanced StartupToStandby: options - no standby on restart enigma2"
						else:
							self.writeAnswerBoot()
							self.GoStandby()
				if getFPWasTimerWakeup() and self.AST.standbyOnAutoBoot.value != "2":
					if self.AST.standbyOnAutoBoot.value == "1": 
						for timer in NavigationInstance.instance.RecordTimer.timer_list:
							if timer.justplay: continue
							ret = None
							if 0 < timer.begin - Time() <= 60*5 and not self.recordTimerWakeup:
								if timer.afterEvent == AFTEREVENT.STANDBY:
									ret = 1
								elif timer.afterEvent == AFTEREVENT.DEEPSTANDBY:
									ret = 2
								elif timer.afterEvent == AFTEREVENT.AUTO:
									ret = 3
								else:
									ret = 4
								if ret != None and self.AST.standbyAfterEevent.value == "0":
									if ret == 3:
										self.recordTimerWakeup = True
										Notifications.AddNotification(Standby.Standby)
									else:
										self.recordTimerWakeup = True
										self.GoStandby()
								elif ret != None and ret != 4 and self.AST.standbyAfterEevent.value == "5":
									if ret == 3:
										self.recordTimerWakeup = True
										Notifications.AddNotification(Standby.Standby)
									else:
										self.recordTimerWakeup = True
										self.GoStandby()
								elif ret == 1 and self.AST.standbyAfterEevent.value == "1":
									self.recordTimerWakeup = True
									self.GoStandby()
								elif ret == 2 and self.AST.standbyAfterEevent.value == "2" or self.AST.standbyAfterEevent.value == "4":
									self.recordTimerWakeup = True
									self.GoStandby()
								elif ret == 3 and self.AST.standbyAfterEevent.value == "3" or self.AST.standbyAfterEevent.value == "4":
									self.recordTimerWakeup = True
									Notifications.AddNotification(Standby.Standby)
					elif self.AST.standbyOnAutoBoot.value == "0":
						for timer in NavigationInstance.instance.RecordTimer.timer_list:
							if 0 < timer.begin - Time() <= 60*5:
								if timer.justplay  and not self.recordTimerWakeup:
									if self.AST.standbyNoForZaptimer.value:
										self.recordTimerWakeup = True
										return
									else:
										self.recordTimerWakeup = True
										self.GoStandby()
								if not timer.justplay and not self.recordTimerWakeup:
									ret = None
									if timer.afterEvent == AFTEREVENT.STANDBY:
										ret = 1
									elif timer.afterEvent == AFTEREVENT.DEEPSTANDBY:
										ret = 2
									elif timer.afterEvent == AFTEREVENT.AUTO:
										ret = 3
									else:
										ret = 4
									if ret != None and self.AST.standbyAfterEevent.value == "0":
										if ret == 3:
											self.recordTimerWakeup = True
											Notifications.AddNotification(Standby.Standby)
										else:
											self.recordTimerWakeup = True
											self.GoStandby()
									elif ret != None and ret != 4 and self.AST.standbyAfterEevent.value == "5":
										if ret == 3:
											self.recordTimerWakeup = True
											Notifications.AddNotification(Standby.Standby)
										else:
											self.recordTimerWakeup = True
											self.GoStandby()
									elif ret == 1 and self.AST.standbyAfterEevent.value == "1":
										self.recordTimerWakeup = True
										self.GoStandby()
									elif ret == 2 and self.AST.standbyAfterEevent.value == "2" or self.AST.standbyAfterEevent.value == "4":
										self.recordTimerWakeup = True
										self.GoStandby()
									elif ret == 3 and self.AST.standbyAfterEevent.value == "3" or self.AST.standbyAfterEevent.value == "4":
										self.recordTimerWakeup = True
										Notifications.AddNotification(Standby.Standby)
									elif ret == 4 and self.AST.standbyAfterEevent.value == "4":
										self.recordTimerWakeup = True
										return
						if not self.recordTimerWakeup and Standby.inStandby is None:
							self.GoStandby()
		elif self.AST.standbyMode.value == "1":
			if fileExists(flag):
				if self.AST.standbyOnManualBoot.value:
					if not self.AST.standbyOnRestart.value:
						self.GoStandby()
					else:
						print "Advanced StartupToStandby: options - no standby on restart enigma2"
			else:
				self.writeAnswerBoot()
				for timer in NavigationInstance.instance.RecordTimer.timer_list:
					if 0 < timer.begin - Time() <= 60*5 and not self.recordTimerWakeup:
						self.CheckAnswer = True
						if self.AST.standbyOnAutoBoot.value != "2":
							if timer.justplay:
								if self.AST.standbyOnAutoBoot.value == "1":
									self.recordTimerWakeup = True
									return
								elif self.AST.standbyOnAutoBoot.value == "0":
									if self.AST.standbyNoForZaptimer.value:
										self.recordTimerWakeup = True
										return
									else:
										self.recordTimerWakeup = True
										self.GoStandby()
							if not timer.justplay and not self.recordTimerWakeup:
								ret = None
								if timer.afterEvent == AFTEREVENT.STANDBY:
									ret = 1
								elif timer.afterEvent == AFTEREVENT.DEEPSTANDBY:
									ret = 2
								elif timer.afterEvent == AFTEREVENT.AUTO:
									ret = 3
								else:
									ret = 4
								if ret != None and self.AST.standbyAfterEevent.value == "0":
									if ret == 3:
										self.recordTimerWakeup = True
										Notifications.AddNotification(Standby.Standby)
									else:
										self.recordTimerWakeup = True
										self.GoStandby()
								elif ret != None and ret != 4 and self.AST.standbyAfterEevent.value == "5":
									if ret == 3:
										self.recordTimerWakeup = True
										Notifications.AddNotification(Standby.Standby)
									else:
										self.recordTimerWakeup = True
										self.GoStandby()
								elif ret == 1 and self.AST.standbyAfterEevent.value == "1":
									self.recordTimerWakeup = True
									self.GoStandby()
								elif ret == 2 and self.AST.standbyAfterEevent.value == "2" or self.AST.standbyAfterEevent.value == "4":
									self.recordTimerWakeup = True
									self.GoStandby()
								elif ret == 3 and self.AST.standbyAfterEevent.value == "3" or self.AST.standbyAfterEevent.value == "4":
									self.recordTimerWakeup = True
									Notifications.AddNotification(Standby.Standby)
								elif ret == 4 and self.AST.standbyAfterEevent.value == "4":
									self.recordTimerWakeup = True
									return
				if self.AST.standbyOnManualBoot.value and not self.CheckAnswer:
					self.GoStandby()

	def writeAnswerBoot(self):
		flag = '/tmp/.answer_boot'
		try:
			fd = open(flag, 'w')
			fd.write(0)
			fd.close()
		except:
			pass

	def GoStandby(self):
		self.checkTimer = eTimer()
		self.checkTimer.callback.append(self.CheckStandby)
		self.checkTimer.start(10000, True)

	def CheckStandby(self):
		if Standby.inStandby is None:
			try:
				self.session.openWithCallback(self. runStandby, MessageBox, _("Advanced StartupToStandby:\n") + _("Go to Standby now?"), type = MessageBox.TYPE_YESNO, timeout = self.AST.standbyTimeout.value)
			except:
				self.checkTimer.start(10000, True)

	def runStandby(self, retval):
		if (retval) and Standby.inStandby is None:
			Notifications.AddNotification(Standby.Standby)

	def GoDeepStandby(self):
		self.deepTimer = eTimer()
		self.deepTimer.callback.append(self.CheckDeepStandby)
		self.deepTimer.start(10000, True)

	def CheckDeepStandby(self):
		try:
			self.session.openWithCallback(self. runDeepStandby, MessageBox, _("Advanced StartupToStandby:\n") + _("Go to Deep Standby now?"), type = MessageBox.TYPE_YESNO, timeout = self.AST.standbyTimeout.value)
		except:
			self.deepTimer.start(10000, True)

	def runDeepStandby(self, retval):
		global inTryQuitMainloop
		if (retval) and Standby.inTryQuitMainloop == False:
			if not self.session.nav.RecordTimer.isRecording():
				self.session.open(Standby.TryQuitMainloop, 1)

def main(session, **kwargs):
	session.open(AdvancedStartupToStandbySetup.AdvancedStartupToStandbyScreen)

def autostart(reason, **kwargs):
	global session  
	if reason == 0 and kwargs.has_key("session") and config.plugins.AdvancedstartupToStandby.standbyEnabled.value:
		session = kwargs["session"]
		try:
			session.open(DoStandby)
		except:
			pass

def Plugins(**kwargs):
	return [PluginDescriptor(where = [ PluginDescriptor.WHERE_SESSIONSTART, ], fnc = autostart),
		PluginDescriptor(name = _("Advanced StartupToStandby"), description= _("Set your box to standby after startup"), where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main)]

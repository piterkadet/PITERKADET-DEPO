#
# Video ClipModes Switcher Plugin for Enigma2
# Coded by vlamo (c) 2012
# Modified Dima73
# Version: 1.0-rc5 (06.08.2012 20:00)
# Support: http://dreamboxfans.ru/forum
#
# This module is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program; if not, write to the Free Software Foundation, Inc., 59
# Temple Place, Suite 330, Boston, MA 0.1.2-1307 USA
###############################################################################

from . import _, PLUGIN_NAME
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigSelection, ConfigText, ConfigYesNo, ConfigInteger, ConfigPosition, ConfigSlider
from Components.Button import Button
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Sources.List import List
from Screens.Screen import Screen
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Tools.BoundFunction import boundFunction
from Components.AVSwitch import AVSwitch
from Components.PluginComponent import plugins
from Tools.Directories import resolveFilename, fileExists, SCOPE_SKIN, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS
from Tools.LoadPixmap import LoadPixmap
import os

examples_sh = "/usr/lib/enigma2/python/Plugins/Extensions/VCS/examples.sh"

class VcsSetupScreen(Screen, ConfigListScreen):

	skin = """
	<screen name="VcsSetupScreen" position="center,center" size="620,470" title="%s" >
		<ePixmap pixmap="skin_default/buttons/red.png" position="10,0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="150,0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="290,0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/blue.png" position="430,0" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/key_info.png" position="580,5" zPosition="1" size="35,25" alphatest="on" />
		<widget name="key_red" position="10,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="150,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget name="key_yellow" position="290,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
		<widget name="key_blue" position="430,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
		<widget name="config" position="10,45" size="600,175" scrollbarMode="showOnDemand" zPosition="1" />
		<widget source="profiles" render="Listbox" position="10,220" size="600,230" zPosition="1" >
			<convert type="TemplatedMultiContent">
				{"templates":
					{"default": (45, [ 
						MultiContentEntryText(pos=(50, 0),  size=(200, 45), font=0, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER|RT_WRAP, text=1),
						MultiContentEntryText(pos=(260, 0), size=(320, 45), font=1, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER|RT_WRAP, text=2),
						MultiContentEntryPixmapAlphaTest(pos=(12, 9), size=(25, 24), png=3),
					], True, "showOnDemand"),
					"notselected": (45, [ 
						MultiContentEntryText(pos=(50, 0),  size=(200, 45), font=0, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER|RT_WRAP, text=1),
						MultiContentEntryText(pos=(260, 0), size=(320, 45), font=1, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER|RT_WRAP, text=2),
						MultiContentEntryPixmapAlphaTest(pos=(12, 9), size=(25, 24), png=3),
					], False, "showOnDemand")
					},
				"fonts": [gFont("Regular", 24), gFont("Regular", 18)],
				"itemHeight": 45,
				"scrollbarMode": "showOnDemand",
				}
			</convert>
		</widget>
	</screen>""" % (_('%s: video clipping switcher')%(PLUGIN_NAME))
	FOCUS_CONFIG, FOCUS_LIST = range(2)

	def __init__(self, session):
		Screen.__init__(self, session)

		for btn in ("red","green","yellow","blue"):
			self["key_" + btn] = Button(" ")

		ConfigListScreen.__init__(self, [])
		self.defprofile = ConfigSelection([])
		self.updateConfigList()

		self.pfsList = []
		self["profiles"] = List(self.pfsList)
		self.updateProfileList()

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "ChannelSelectEPGActions"],
			{
				"cancel": self.keyExit,
				"ok": self.keyOk,
				"showEPGList": self.showExamples,
				"red": self.keyRed,
				"green": self.keyGreen,
				"yellow": boundFunction(self.moveEntry, -1),
				"blue": boundFunction(self.moveEntry, +1),
				"up": self.keyUp,
				"down": self.keyDown,
			}, -1)
		
		self.onClose.append(self.__closed)
		self.onLayoutFinish.append(self.__layoutFinished)
		self.onShown.append(self.updateButtonState)
		self.prev_ext_menu = config.plugins.VCS.ext_menu.value
		
	def __layoutFinished(self):
		self["config"].instance.setSelectionEnable(True)
		self["profiles"].style = "notselected"
		self.focus = self.FOCUS_CONFIG
		self["profiles"].onSelectionChanged.append(self.updateButtonState)

	def __closed(self):
		for x in self["config"].list:
			if x[1] == self.defprofile:
				config.plugins.VCS.default.value = self.defprofile.value
				config.plugins.VCS.default.save()
				continue
			x[1].save()

	def updateButtonState(self):
		self["key_green"].setText(_("Add"))
		if self.focus == self.FOCUS_LIST:
			cur = self["profiles"].getCurrent()
			if cur:
				self["key_red"].setText(_("Delete"))
				self["key_yellow"].setText(self["profiles"].index > 0 and _("Move Up") or " ")
				self["key_blue"].setText(self["profiles"].index < len(self.pfsList)-1 and _("Move Down") or " ")
			else:
				for btn in ("key_red","key_yellow","key_blue"):
					self[btn].setText(" ")
		else:
			self["key_red"].setText(_("Exit"))
			self["key_yellow"].setText(" ")
			self["key_blue"].setText(" ")

	def updateConfigList(self):
		pfslist = [ (-1,_("None")) ]
		pfs = config.plugins.VCS.profiles
		for x in range(len(pfs)):
			pfslist.append((x, pfs[x].name.value))
		default = not config.plugins.VCS.default.value in range(len(pfs)) and -1 or config.plugins.VCS.default.value
		self.defprofile.setChoices(pfslist, default=default)
		cfglist = [
			getConfigListEntry(_("Plugin quick button(s)"), config.plugins.VCS.hotkey),
			getConfigListEntry(_("Quick button(s) action"), config.plugins.VCS.hkaction),
			getConfigListEntry(_("Show \"Choise list\" in extensions menu"), config.plugins.VCS.ext_menu),
			getConfigListEntry(_("Message timeout on switch profiles"), config.plugins.VCS.msgtime),
			getConfigListEntry(_("Default profile on enigma startup"), self.defprofile),
			]
		if fileExists("/usr/lib/enigma2/python/Screens/DVD.pyo"):
			cfglist.append(getConfigListEntry(_('Add \"Choise list\" Blue Button to DVDPlayer'), config.plugins.VCS.dvd_menu))
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPlayer/plugin.pyo") or fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPlayer/plugin.pyc"):
			cfglist.append(getConfigListEntry(_('Add \"Choise list\" Blue Button to MediaPlayer'), config.plugins.VCS.media_player))
		self["config"].list = cfglist
		self["config"].setList(cfglist)

	def updateProfileList(self):
		list = []
		pfs = config.plugins.VCS.profiles
		for x in range(len(pfs)):
			s = "%s %s" % (getAspectString(pfs[x].aspect.value), pfs[x].cliprect.value)
			path = "skin_default/icons/lock_%s.png"%(pfs[x].enabled.value and "on" or "off")
			png = LoadPixmap(resolveFilename(SCOPE_SKIN, path))
			list.append((pfs[x], pfs[x].name.value, s, png))
		self.pfsList = list
		self["profiles"].setList(self.pfsList)

	def getUniqProfileName(self, name=_("Profile "), suffix=1):
		x = 0
		uname = "%s%d" % (name, suffix)
		pfs = config.plugins.VCS.profiles
		while x < config.plugins.VCS.pfs_count.value:
			if pfs[x].name.value == uname:
				x = -1
				suffix += 1
				uname = "%s%d" % (name, suffix)
			x += 1
		return uname

	def addEntry(self):
		self.session.openWithCallback(self.addCallback, VcsProfileSetup, InitVcsProfile(name=self.getUniqProfileName()))

	def addCallback(self, result, profile):
		if result:
			pfs = config.plugins.VCS.profiles
			idx = config.plugins.VCS.pfs_count.value
			if profile.name.value == "":
				profile.name.value = self.getUniqProfileName()
				profile.name.save()
			pfs.append(profile)
			config.plugins.VCS.pfs_count.value = len(pfs)
			config.plugins.VCS.pfs_count.save()
			self.updateProfileList()
			self["profiles"].index = idx
			self.updateConfigList()
			self.updateButtonState()
		else:
			del profile

	def editEntry(self):
		idx = self["profiles"].index
		if idx < len(self.pfsList):
			pfs = config.plugins.VCS.profiles
			self.session.openWithCallback(self.editCallback, VcsProfileSetup, pfs[idx])

	def editCallback(self, result, profile):
		if result:
			pfs = config.plugins.VCS.profiles
			idx = self["profiles"].index
			if profile.name.value == "":
				profile.name.value = self.getUniqProfileName()
				profile.name.save()
			self.updateProfileList()
			self["profiles"].index = idx
			self.updateButtonState()

	def deleteEntry(self):
		cur = self["profiles"].getCurrent()
		if cur:
			self.session.openWithCallback(self.deleteCallback, MessageBox, _("Do you really want to delete profile:\n %s") % (cur[1]), MessageBox.TYPE_YESNO)

	def deleteCallback(self, yesno):
		if yesno:
			idx = self["profiles"].index
			pfs = config.plugins.VCS.profiles
			pfs.remove(pfs[idx])
			pfs.saved_value = pfs.saved_value
			config.plugins.VCS.pfs_count.value = len(pfs)
			config.plugins.VCS.pfs_count.save()
			self.updateProfileList()
			if len(pfs):
				if idx >= len(pfs):
					self["profiles"].index = len(pfs)-1
				else:
					self["profiles"].index = idx
			self.updateConfigList()
			self.updateButtonState()

	def moveEntry(self, direction):
		if self.focus == self.FOCUS_LIST:
			idx = self["profiles"].index
			if idx + direction in range(len(self.pfsList)):
				pfs = config.plugins.VCS.profiles
				tmp_pf = pfs[idx]
				pfs[idx] = pfs[idx + direction]
				pfs[idx + direction] = tmp_pf
				self.updateProfileList()
				self["profiles"].index = idx + direction
				self.updateConfigList()
				self.updateButtonState()

	def keyRed(self):
		if self.focus == self.FOCUS_LIST:
			self.deleteEntry()
		else:
			self.keyExit()

	def keyExit(self):
		if self.prev_ext_menu != config.plugins.VCS.ext_menu.value:
			plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
		self.close()

	def keyGreen(self):
		self.addEntry()

	def keyOk(self):
		if self.focus == self.FOCUS_LIST:
			self.editEntry()

	def keyUp(self):
		if self.focus == self.FOCUS_CONFIG:
			self["config"].instance.moveSelection(self["config"].instance.moveUp)
		elif self.focus == self.FOCUS_LIST:
			if self["profiles"].getIndex() == 0:
				self["config"].instance.setSelectionEnable(True)
				self["profiles"].style = "notselected"
				self["config"].setCurrentIndex(len(self["config"].getList())-1)
				self.focus = self.FOCUS_CONFIG
			else:
				self["profiles"].selectPrevious()
		self.updateButtonState()

	def keyDown(self):
		if self.focus == self.FOCUS_CONFIG:
			if self["config"].getCurrentIndex() < len(self["config"].getList())-1:
				self["config"].instance.moveSelection(self["config"].instance.moveDown)
			else:
				self["config"].instance.setSelectionEnable(False)
				self["profiles"].style = "default"
				self.focus = self.FOCUS_LIST
		elif self.focus == self.FOCUS_LIST:
			self["profiles"].selectNext()
		self.updateButtonState()
		
	def showExamples(self):
		if os.path.exists(examples_sh):
			try:
				os.chmod(examples_sh, 0755)
				self.session.open(Console,_("Examples:"),["%s" % examples_sh])
			except:
				pass


class VcsProfileSetup(ConfigListScreen, Screen):

	skin = """
		<screen name="VcsProfileSetup" position="center,center" size="550,350" title="%s" backgroundColor="transparent" flags="wfNoBorder" >
			<widget source="header" render="Label" position="0,0" zPosition="1" size="550,80" halign="center" valign="center" noWrap="1"
			 font="Regular;26" foregroundColor="red" backgroundColor="background" shadowColor="black" shadowOffset="-2,-2" transparent="1"/>
			<widget name="config" position="0,100" size="550,200" scrollbarMode="showOnDemand" zPosition="1" foregroundColor="white" backgroundColor="transparent" />
			<ePixmap pixmap="skin_default/buttons/red.png" position="135,310" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="275,310" size="140,40" alphatest="on" />
			<widget source="key_red" render="Label" position="135,310" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget source="key_green" render="Label" position="275,310" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		</screen>""" % (_('%s: Profile Setup')%(PLUGIN_NAME))

	def __init__(self, session, profile):
		Screen.__init__(self, session)

		self["header"] = StaticText("")
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"red": self.cancel,
				"green": self.save,
				"save": self.save,
				"cancel": self.cancel,
				"ok": self.keyOk,
			}, -2)

		self.pf_saved_value = profile.saved_value
		self.prev_stretch = getStretch()
		self.prev_aspect = getAspect()
		self.prev_cliprect = getClipRect()
		self.initConfig(profile)

		ConfigListScreen.__init__(self, [])
		self.createSetup()

		self.onClose.append(self.__onClose)

	def __onClose(self):
		setStretch(self.prev_stretch)
		setAspect(self.prev_aspect)
		setClipRect(self.prev_cliprect)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.newConfig()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.newConfig()

	def keyOk(self):
		cur = self["config"].getCurrent()
		if cur[1] in (self.clip.X,self.clip.Y,self.clip.W,self.clip.H):
			from Components.Input import Input
			from Screens.InputBox import InputBox
			from Tools.BoundFunction import boundFunction
			self.session.openWithCallback(boundFunction(self.setSliderStep, cur[1]), InputBox, title=_("Set slider step (1 - 20):"), text=str(cur[1].increment), type = Input.NUMBER)

	def setSliderStep(self, slider, step):
		if step and (0 < int(step) < 21):
			slider.increment = int(step)
			self["config"].instance.invalidate()

	def initConfig(self, pf):
		self.profile = pf
		self.clip = ConfigSubsection()
		self.clip.X = ConfigSlider(default = pf.cliprect.value[0], increment = 5, limits = (0, 719))
		self.clip.Y = ConfigSlider(default = pf.cliprect.value[1], increment = 5, limits = (0, 575))
		self.clip.W = ConfigSlider(default = pf.cliprect.value[2], increment = 5, limits = (0, 720))
		self.clip.H = ConfigSlider(default = pf.cliprect.value[3], increment = 5, limits = (0, 576))
		self.pf_stretch = ConfigSelection([("0",_("no")), ("1", _("yes"))], default = pf.stretch.value)
		self.pf_aspect = ConfigSelection([(0, _("4:3 Letterbox")), (1, _("4:3 PanScan")), (2, _("16:9")), (3, _("16:9 always")), (4, _("16:10 Letterbox")), (5, _("16:10 PanScan")), (6, _("16:9 Letterbox"))], default = pf.aspect.value)
		self.pf_aspect.addNotifier(self.aspectSettingChanged)
		self.pf_stretch.addNotifier(self.stretchSettingChanged)
		for elem in [self.clip.X,self.clip.Y,self.clip.W,self.clip.H]:
			elem.addNotifier(self.videoSettingChanged)

	def newConfig(self):
		pass

	def createSetup(self):
		list = [ ]
		list.append(getConfigListEntry(_("Profile Name"), self.profile.name))
		list.append(getConfigListEntry(_("Enable Profile"), self.profile.enabled))
		list.append(getConfigListEntry(_("Use Video Stretch (3D content)"), self.pf_stretch))
		list.append(getConfigListEntry(_("Aspect Ratio"), self.pf_aspect))
		list.append(getConfigListEntry(_("Video Left"), self.clip.X))
		list.append(getConfigListEntry(_("Video Width"), self.clip.W))
		list.append(getConfigListEntry(_("Video Top"), self.clip.Y))
		list.append(getConfigListEntry(_("Video Height"), self.clip.H))
		self["config"].list = list
		self["config"].l.setList(list)

	def save(self):
		self.profile.cliprect.value = [self.clip.X.value,self.clip.Y.value,self.clip.W.value,self.clip.H.value]
		self.profile.stretch.value = self.pf_stretch.value
		self.profile.aspect.value = self.pf_aspect.value
		self.profile.save()
		self.close(True, self.profile)

	def cancel(self):
		for x in self["config"].list:
			x[1].cancel()
		if self.pf_saved_value:
			self.profile.saved_value = self.pf_saved_value
		self.close(False, self.profile)

	def stretchSettingChanged(self, elem):
		setStretch(int(elem.value))
		
	def aspectSettingChanged(self, elem):
		setAspect(int(elem.value))
		self.updateHeaderText()

	def videoSettingChanged(self, elem):
		if self.clip.X.value + self.clip.W.value > 720:
			self.clip.W.value = 720 - self.clip.X.value
		if self.clip.Y.value + self.clip.H.value > 576:
			self.clip.H.value = 576 - self.clip.Y.value
		if "config" in self:
			self["config"].instance.invalidate()
		setClipRect([self.clip.X.value,self.clip.Y.value,self.clip.W.value,self.clip.H.value])
		self.updateHeaderText()

	def updateHeaderText(self):
		if "header" in self:
			self["header"].setText("%s\n[%d, %d, %d, %d]"%(getAspectString(self.pf_aspect.value),self.clip.X.value,self.clip.Y.value,self.clip.W.value,self.clip.H.value))

def getAspect():
	return AVSwitch().getAspectRatioSetting()

def getAspectString(aspectnum):
	return {0: _("4:3 Letterbox"), 1: _("4:3 PanScan"), 2: _("16:9"), 3: _("16:9 always"), 4: _("16:10 Letterbox"), 5: _("16:10 PanScan"), 6: _("16:9 Letterbox")}[aspectnum]

def setAspect(aspect):
	map = {0: "4_3_letterbox", 1: "4_3_panscan", 2: "16_9", 3: "16_9_always", 4: "16_10_letterbox", 5: "16_10_panscan",  6: "16_9_letterbox"}
	config.av.aspectratio.setValue(map[aspect])
	AVSwitch().setAspectRatio(aspect)
	
def getStretch():
	result = 0
	try:
		fd = open('/proc/stb/vmpeg/0/clip_stretch', 'r')
		result = int(fd.read().strip())
		fd.close()
	except:
		pass
	return result
	
def setStretch(stretchnum):
	try:
		file = open('/proc/stb/vmpeg/0/clip_stretch', 'w')
		file.write('%d' % stretchnum)
		file.close()
	except:
		pass

def getClipRect():
	result = [0,0,720,576]
	for (n,f) in enumerate(["left","top","width","height"]):
		try:
			fd = open("/proc/stb/vmpeg/0/clip_%s"%(f), "r")
			result[n] = int("0X%s"%(fd.readline().strip()), 16)
			fd.close()
		except:
			pass
	return result

def setClipRect(rectlist):
	for (n,f) in enumerate(["left","top","width","height"]):
		try:
			fd = open("/proc/stb/vmpeg/0/clip_%s"%(f), "w")
			fd.write('%X' % rectlist[n])
			fd.close()
		except:
			pass

def InitVcsProfile(profile=None, name=""):
	if profile is None:
		profile = ConfigSubsection()
	profile.name = ConfigText("", fixed_size=False)
	if not profile.name.value and name:
		profile.name.value = name
		profile.name.save()
	profile.enabled = ConfigYesNo(default=True)
	profile.stretch = ConfigSelection([("0",_("no")), ("1", _("yes"))], default="0")
	profile.aspect = ConfigInteger(2)
	profile.cliprect = ConfigPosition([0,0,720,576], (719,575,720,576))
	return profile


class VcsMessageBox(Screen):
	skin = """
		<screen name="VcsMessageBox" position="center,0" size="720,100" zPosition="10" flags="wfNoBorder" backgroundColor="transparent" title=" ">
			<widget source="message" render="Label" position="0,0" zPosition="1" size="720,100" halign="center" valign="center" noWrap="1"
			 font="Regular;26" foregroundColor="red" backgroundColor="background" shadowColor="black" shadowOffset="-2,-2" transparent="1"/>
		</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		self["message"] = StaticText("")
		from enigma import eTimer
		self.timer = eTimer()
		self.timer.callback.append(self.hideMessage)

	def showMessage(self, message, timeout):
		self["message"].setText(message)
		self.show()
		if timeout > 0:
			self.timer.start(timeout * 1000, True)

	def hideMessage(self):
		self.hide()


VcsInfoBarKeys = [
	["none",_("NONE"),["KEY_RESERVED"]],
	["F2",_("F2"),["KEY_F2"]],
]

from keyids import KEYIDS
from enigma import eActionMap

class VcsInfoBar:

	def __init__(self, session, infobar):
		self.session = session
		self.infobar = infobar
		self.msgbox = None
		self.defaultMode = None

		if config.plugins.VCS.default.value in range(len(config.plugins.VCS.profiles)) and \
		   config.plugins.VCS.profiles[config.plugins.VCS.default.value].enabled.value:
			self.currentMode = x = config.plugins.VCS.default.value
			while x > 0:
				x -= 1
				if not config.plugins.VCS.profiles[x].enabled.value:
					self.currentMode -= 1
		else:
			self.currentMode = 0
		self.switchMode(0)

		self.lastKey = None
		self.hotkeys = { }
		for x in VcsInfoBarKeys:
			self.hotkeys[x[0]] = [KEYIDS[key] for key in x[2]]
		eActionMap.getInstance().bindAction('', -10, self.keyPressed)

	def keyPressed(self, key, flag):
		for k in self.hotkeys[config.plugins.VCS.hotkey.value]:
			if key == k and self.session.current_dialog == self.infobar:
				if flag == 0:
					self.lastKey = key
				elif self.lastKey != key or flag == 4:
					self.lastKey = None
					continue
				elif flag == 3:
					self.lastKey = None
					self.execute()
				elif flag == 1:
					self.lastKey = None
					if config.plugins.VCS.hkaction.value == "switch":
						self.switchMode(key == self.hotkeys[config.plugins.VCS.hotkey.value][0] and +1 or -1)
					elif config.plugins.VCS.hkaction.value == "choise":
						self.showChoiceBox()
				return 1
		return 0

	def switchMode(self, direction):
		if not config.plugins.VCS.default.value in range(config.plugins.VCS.pfs_count.value):
			if self.defaultMode is None:
				self.defaultMode = InitVcsProfile(name=_("Default Mode"))
			modeslist = [ self.defaultMode ]
		else:
			modeslist = [ ]
		for x in range(config.plugins.VCS.pfs_count.value):
			if config.plugins.VCS.profiles[x].enabled.value:
				modeslist.append(config.plugins.VCS.profiles[x])
		if len(modeslist):
			self.currentMode = (self.currentMode + direction) % len(modeslist)
			self.doSwitch(modeslist[self.currentMode])

	def doSwitch(self, profile):
		setStretch(int(profile.stretch.value))
		setAspect(profile.aspect.value)
		setClipRect(profile.cliprect.value)
		
		if int(config.plugins.VCS.msgtime.value):
			msg = '%s\n%s\n%s' % (profile.name.value, getAspectString(profile.aspect.value), profile.cliprect.value)
			if self.msgbox is None:
				self.msgbox = self.session.instantiateDialog(VcsMessageBox)
			self.msgbox.showMessage(msg, int(config.plugins.VCS.msgtime.value))

	def execute(self):
		self.session.open(VcsSetupScreen)

	def showChoiceBox(self):
		modeslist = [ ]
		keyslist = [ ]
		y = 0
		for x in range(config.plugins.VCS.pfs_count.value):
			if config.plugins.VCS.profiles[x].enabled.value:
				pf = config.plugins.VCS.profiles[x]
				modeslist.append(('%s (%s %s)'%(pf.name.value,getAspectString(pf.aspect.value),pf.cliprect.value), x, y))
				keyslist.append(x < 9 and str(x+1) or x == 9 and '0' or '')
				y += 1
		modeslist.append((_('Call %s plugin')%(PLUGIN_NAME),-1))
		keyslist.append('blue')
		from Screens.ChoiceBox import ChoiceBox
		dlg = self.session.openWithCallback(self.choiceCallback, ChoiceBox, list = modeslist, keys = keyslist, selection = self.currentMode)
		dlg.setTitle(_('%s: Profile Selection')%(PLUGIN_NAME))

	def choiceCallback(self, answer):
		if answer is not None:
			if answer[1] == -1:
				self.execute()
			else:
				self.doSwitch(config.plugins.VCS.profiles[answer[1]])
				self.currentMode = answer[2]
				
				
class VcsChoiseList:
	def __init__(self, session):
		self.session = session
		self.msgbox = None
		modeslist = [ ]
		keyslist = [ ]
		y = 0
		for x in range(config.plugins.VCS.pfs_count.value):
			if config.plugins.VCS.profiles[x].enabled.value:
				pf = config.plugins.VCS.profiles[x]
				modeslist.append(('%s (%s %s)'%(pf.name.value,getAspectString(pf.aspect.value),pf.cliprect.value), x, y))
				keyslist.append(x < 9 and str(x+1) or x == 9 and '0' or '')
				y += 1
		modeslist.append((_('Call %s plugin')%(PLUGIN_NAME),-1))
		keyslist.append('blue')
		from Screens.ChoiceBox import ChoiceBox
		dlg = self.session.openWithCallback(self.choiceCallback, ChoiceBox, list = modeslist, keys = keyslist)
		dlg.setTitle(_('%s: Profile Selection')%(PLUGIN_NAME))

	def Switch(self, profile):
		setStretch(int(profile.stretch.value))
		setAspect(profile.aspect.value)
		setClipRect(profile.cliprect.value)
		if int(config.plugins.VCS.msgtime.value):
			msg = '%s\n%s\n%s' % (profile.name.value, getAspectString(profile.aspect.value), profile.cliprect.value)
			if self.msgbox is None:
				self.msgbox = self.session.instantiateDialog(VcsMessageBox)
			self.msgbox.showMessage(msg, int(config.plugins.VCS.msgtime.value))

	def execute(self):
		self.session.open(VcsSetupScreen)

	def choiceCallback(self, answer):
		if answer is not None:
			if answer[1] == -1:
				self.execute()
			else:
				self.Switch(config.plugins.VCS.profiles[answer[1]])




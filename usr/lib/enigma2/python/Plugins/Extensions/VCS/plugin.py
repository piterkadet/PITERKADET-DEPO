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
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigSubList, ConfigInteger, ConfigYesNo
from Components.ActionMap import ActionMap
from Tools.Directories import fileExists
from VCS import InitVcsProfile, VcsInfoBar, VcsSetupScreen, VcsInfoBarKeys, VcsChoiseList





config.plugins.VCS = ConfigSubsection()
config.plugins.VCS.hotkey = ConfigSelection([(x[0],x[1]) for x in VcsInfoBarKeys], "none")
config.plugins.VCS.hkaction = ConfigSelection([("switch",_("switch profiles")),("choise",_("show choise box"))], "switch")
config.plugins.VCS.ext_menu = ConfigYesNo(False)
config.plugins.VCS.dvd_menu = ConfigYesNo(False)
config.plugins.VCS.media_player = ConfigYesNo(False)
config.plugins.VCS.default = ConfigInteger(-1)
config.plugins.VCS.msgtime = ConfigSelection([(str(x),str(x)) for x in range(11)], "3")
config.plugins.VCS.pfs_count = ConfigInteger(0)
config.plugins.VCS.profiles = ConfigSubList()
if config.plugins.VCS.pfs_count.value:
	for x in range(config.plugins.VCS.pfs_count.value):
		config.plugins.VCS.profiles.append(InitVcsProfile(name=_("Profile %d")%(x+1)))
else:
	config.plugins.VCS.profiles.append(InitVcsProfile(name=_("Default Profile")))
	config.plugins.VCS.pfs_count.value = 1
	config.plugins.VCS.pfs_count.save()
	config.plugins.VCS.default.value = 0
	config.plugins.VCS.default.save()
	
baseDVDPlayer__init__ = None

def DVDPlayerInit():
	global baseDVDPlayer__init__
	from Screens.DVD import DVDPlayer
	if baseDVDPlayer__init__ is None:
		baseDVDPlayer__init__ = DVDPlayer.__init__
	DVDPlayer.__init__ = DVDPlayer__init__

def DVDPlayer__init__(self, session, dvd_device = None, dvd_filelist = [ ], args = None):
	baseDVDPlayer__init__(self, session, dvd_device, dvd_filelist, args)
	if config.plugins.VCS.dvd_menu.value:
		def showVCS():
			from Plugins.Extensions.VCS.plugin import show_choisebox
			VcsChoiseList(session)
		
		self["ColorActions"] = ActionMap(["ColorActions"],
				{
					"blue": showVCS,
				}, -1)

baseMediaPlayer__init__ = None
baseMoviePlayer__init__ = None


def MediaPlayerInit():
	global baseMediaPlayer__init__ , baseMoviePlayer__init__ 
	action = None
	try:
		from Plugins.Extensions.MediaPlayer.plugin import MoviePlayer
		action = 'Now'
	except ImportError:
		action = None

	if action is None:
		try:
			from Plugins.Extensions.MediaPlayer.plugin import MediaPlayer
			action = 'Old'
		except ImportError:
			action = None

	if action == 'Now':
		if baseMoviePlayer__init__ is None:
			baseMoviePlayer__init__ = MoviePlayer.__init__
		MoviePlayer.__init__ = MoviePlayer__init__
	elif action == 'Old':
		if baseMediaPlayer__init__ is None:
			baseMediaPlayer__init__ = MediaPlayer.__init__
		MediaPlayer.__init__ = MediaPlayer__init__
	else:
		pass

def MoviePlayer__init__(self, session, service):
	baseMoviePlayer__init__(self, session, service)
	if config.plugins.VCS.media_player.value:
		def showVCS():
			from Plugins.Extensions.VCS.plugin import show_choisebox
			VcsChoiseList(session)
		
		self["ColorActions"] = ActionMap(["ColorActions"],
				{
					"blue": showVCS,
				}, -1)
			
def MediaPlayer__init__(self, session, args = None):
	baseMediaPlayer__init__(self, session, args)
	if config.plugins.VCS.media_player.value:
		def showVCS():
			from Plugins.Extensions.VCS.plugin import show_choisebox
			VcsChoiseList(session)
		
		self["ColorActions"] = ActionMap(["ColorActions"],
				{
					"blue": showVCS,
				}, -1)	

baseInfoBar__init__ = None

def newInfoBar__init__(self, session):
	baseInfoBar__init__(self, session)
	self.vcsinfobar = VcsInfoBar(session, self)

def autostart(reason, **kwargs):
	if reason == 0:
		global baseInfoBar__init__
		from Screens.InfoBar import InfoBar
		if baseInfoBar__init__ is None:
			baseInfoBar__init__ = InfoBar.__init__
		InfoBar.__init__ = newInfoBar__init__
		if fileExists("/usr/lib/enigma2/python/Screens/DVD.pyo"):
			try:
				DVDPlayerInit()
			except Exception:
				pass
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPlayer/plugin.pyo") or fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPlayer/plugin.pyc"):
			try:
				MediaPlayerInit()
			except Exception:
				pass
			
def show_choisebox(session, **kwargs):
	VcsChoiseList(session)

def main(session, **kwargs):
	session.open(VcsSetupScreen)

def Plugins(**kwargs):
	from Plugins.Plugin import PluginDescriptor
	if config.plugins.VCS.ext_menu.value:
		return [PluginDescriptor(where = PluginDescriptor.WHERE_AUTOSTART, fnc = autostart),
			PluginDescriptor(name=PLUGIN_NAME, description=_("video clipping switcher"), where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main),
			PluginDescriptor(name =_('%s:Choise List')%(PLUGIN_NAME), description=_("video clipping switcher"), where =PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = show_choisebox)]
	else:
		return [PluginDescriptor(where = PluginDescriptor.WHERE_AUTOSTART, fnc = autostart),
			PluginDescriptor(name=PLUGIN_NAME, description=_("video clipping switcher"), where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)]
	


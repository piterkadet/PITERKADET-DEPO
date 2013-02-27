#
#  SatelliteEditorClassic E2 Plugin
#
#  $Id: plugin.py,v 1.0 2011-03-19 00:00:00 Shaderman Exp $
#
#  Coded by Shaderman (c) 2011
#  plugin.png by Sakartvelo
#  Support: www.dreambox-tools.info
#
#  This plugin is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative
#  Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.

#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially 
#  distributed other than under the conditions noted above.
#

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import HelpableActionMap
from Components.Sources.StaticText import StaticText
from Components.config import config, ConfigSubsection, ConfigSet, ConfigSelection, NoSave, ConfigYesNo
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Sources.List import List
from enigma import eListbox
from os import path as os_path, remove
from Screens.HelpMenu import HelpableScreen
from Screens.MessageBox import MessageBox
from shutil import copyfile
from threading import Thread
from Tools.LoadPixmap import LoadPixmap
from Tools.Notifications import AddPopup
from twisted.web.client import getPage
import xml.etree.cElementTree as etree
from xml.parsers.expat import ParserCreate
from zipfile import ZipFile
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_CURRENT_SKIN, SCOPE_LANGUAGE
import gettext

global min
min = 0

lang = language.getLanguage()
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("SatelliteEditorClassic", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "SystemPlugins/SatelliteEditorClassic/locale/"))

def _(txt):
	t = gettext.dgettext("SatelliteEditorClassic", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

# for localized messages
from . import _

FILEURL = "http://feed.dreambox-tools.info/satellites.zip"
USERAGENT = "Enigma2 Satellite Editor Plugin"
SATFILE = "/etc/tuxbox/satellites.xml"
ZIPFILE = "/tmp/satellites.zip"
TMPFILE = "/tmp/satellites.xml"


config.plugins.sateditor = ConfigSubsection()
config.plugins.sateditor.satellites = ConfigSet(default = ['192', '235', '282', '130'], choices = ['192', '235', '282', '130'])
config.plugins.sateditor.sortby = ConfigSelection(default = 1, choices = [
				(1, "1"),
				(2, "2"),
				(3, "3")
				])
config.plugins.sateditor.purgeThreadEnded = NoSave(ConfigYesNo(default = False))

class SatelliteEditorClassic(Screen, HelpableScreen):

	skin = """
		<screen position="center,center" size="560,320" title="%s" >
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />
			<widget render="Label" source="key_red" position="0,0" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="red" font="Regular;18" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
			<widget render="Label" source="key_green" position="140,0" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="red" font="Regular;18" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
			<widget render="Label" source="key_yellow" position="280,0" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="red" font="Regular;18" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
			<widget render="Label" source="key_blue" position="420,0" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="red" font="Regular;18" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
			<widget source="satlist" render="Listbox" position="5,50" size="550,260" scrollbarMode="showOnDemand">
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (50, 0), size = (460, 26), font=0, flags = RT_HALIGN_LEFT, text = 1),
							MultiContentEntryPixmapAlphaTest(pos = (5, 0), size = (25, 24), png = 2),
						],
					"fonts": [gFont("Regular", 18)],
					"itemHeight": 26
					}
				</convert>
			</widget>
		</screen>""" % _("Satellite Editor Classic")

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)

		self["key_red"] = StaticText(_("Exit"))
		self["key_green"] = StaticText("")
		self["key_yellow"] = StaticText(_("Download"))
		self["key_blue"] = StaticText("")

		self.satList = []
		self["satlist"] = List(self.satList)

		HelpableScreen.__init__(self)
		
		self["OkCancelActions"] = HelpableActionMap(self, "OkCancelActions",
		{
			"cancel":	(self.exit, _("Exit plugin")),
			"ok":		(self.changeSelection, _("Select/deselect satellite")),
		}, -1)
		
		self["ColorActions"] = HelpableActionMap(self, "ColorActions",
		{
			"red":		(self.exit, _("Exit plugin")),
			"green":	(self.accept, _("Accept changes")),
			"yellow":	(self.downloadSattelitesFile, _("Download satellites.xml file")),
			"blue":		(self.purgeSattelitesFile, _("Purge satellites.xml file")),
		}, -1)
		
		self["ChannelSelectBaseActions"] = HelpableActionMap(self, "ChannelSelectBaseActions",
		{
			"nextBouquet":	(self.changeSortingUp, _("Sorting up")),
			"prevBouquet":	(self.changeSortingDown, _("Sorting down")),
		}, -1)
		
		self.showAccept = False
		self.useTmpFile = False
		self.purgePossible = False
		self.downloadPossible = True
		
		self.xmlVersion = ""
		self.xmlEncoding = ""
		self.xmlComment = ""
		
		# we need a notification when the purge thread ends
		config.plugins.sateditor.purgeThreadEnded.addNotifier(self.postPurge, initial_call = False)
		
		self.onShown.append(self.loadSattelitesFile)

	# exit the plugin
	def exit(self):
		print '[SatelliteEditorClassic] closing'
		
		config.plugins.sateditor.purgeThreadEnded.notifiers.remove(self.postPurge)

		# cleanup temporary files
		if os_path.exists(TMPFILE):
			try:
				remove(TMPFILE)
			except OSError, error:
				print "[SatelliteEditorClassic] unable to delete temp file", TMPFILE
				AddPopup(text = _("Unable to delete temp file.\n%s") % error, type = MessageBox.TYPE_ERROR, timeout = 0, id = "RemoveFileError")
		if os_path.exists(ZIPFILE):
			try:
				remove(ZIPFILE)
			except OSError, error:
				print "[SatelliteEditorClassic] unable to delete temp file", ZIPFILE
				AddPopup(text = _("Unable to delete temp file.\n%s") % error, type = MessageBox.TYPE_ERROR, timeout = 0, id = "RemoveFileError")
		self.close()
		
	# accet the changes and copy the modified satellites.xml to its target
	def accept(self):
		if not self.showAccept:
			return

		print '[SatelliteEditorClassic] copying temp satellite file to target'

		if os_path.exists(TMPFILE):
			try:
				copyfile(TMPFILE, SATFILE)
			except OSError, error:
				print "[SatelliteEditorClassic] error during copying of", TMPFILE
				self.session.open(MessageBox, _("Unable to copy temp file.\n%s") % error, type = MessageBox.TYPE_ERROR)

		self.showAccept = False
		self["key_green"].setText("")
		
	# change direction of sorting upwards
	def changeSortingUp(self):
		if config.plugins.sateditor.sortby.value == 1:
			config.plugins.sateditor.sortby.value = 3
		else:
			config.plugins.sateditor.sortby.value -= 1
		
		self.setListSorted()
		
	# change direction of sorting downwards
	def changeSortingDown(self):
		if config.plugins.sateditor.sortby.value == 3:
			config.plugins.sateditor.sortby.value = 1
		else:
			config.plugins.sateditor.sortby.value += 1
		
		self.setListSorted()
		
	# load either the original or temporary satellites.xml file
	def loadSattelitesFile(self, fileName = SATFILE):
		print '[SatelliteEditorClassic] loading satellite file', fileName
		
		self.satList = []
		try:
			satFile = open(fileName, "r")
		except IOError, error:
			print "[SatelliteEditorClassic] unable to open", fileName
			satFile = None
			AddPopup(text = _("Unable to open file.\n%s") % error, type = MessageBox.TYPE_ERROR, timeout = 0, id = "OpenFileError")
			self.exit()

		if not satFile:
			return
			
		satellites = config.plugins.sateditor.satellites.value
		curroot = etree.parse(satFile)
		
		# build our "satlist" from all satellites
		for sat in curroot.findall("sat"):
			position = sat.attrib.get("position")
			name = sat.attrib.get("name")
			if position in satellites:
				png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/lock_on.png"))
				self.satList.append((position, name.encode('utf-8'), png))
			else:
				self.satList.append((position, name.encode('utf-8'), None))
		satFile.close()
		
		self["satlist"].setList(self.satList)
		self.setListSorted()
		
	# "satlist" sorting
	def setListSorted(self):
		if config.plugins.sateditor.sortby.value == 1: # alphabetical
			s = sorted(self.satList, lambda x, y: cmp(x[1], y[1]), reverse = False)
			self.satList = sorted(s, lambda x, y: cmp(x[2], y[2]), reverse = True)
		elif config.plugins.sateditor.sortby.value == 2: # east-west
			s = sorted(self.satList, lambda x, y: cmp(int(x[0]), int(y[0])), reverse = False)
			self.satList = sorted(s, lambda x, y: cmp(x[2], y[2]), reverse = True)
		else: # west-east
			s = sorted(self.satList, lambda x, y: cmp(int(x[0]), int(y[0])), reverse = True)
			self.satList = sorted(s, lambda x, y: cmp(x[2], y[2]), reverse = True)

		# update the gui list with sorted content
		self["satlist"].updateList(self.satList)
		
		if len(self.satList) > len(config.plugins.sateditor.satellites.value):
			self["key_blue"].setText(_("Purge"))
			self.purgePossible = True
		else:
			self["key_blue"].setText("")
			self.purgePossible = False
		
	# toggle the selection of a satellite on or off
	def changeSelection(self):
		png = None
		idx = self["satlist"].getIndex()
		position = self.satList[idx][0]
		name = self.satList[idx][1]
		
		if position in config.plugins.sateditor.satellites.value:
			config.plugins.sateditor.satellites.value.remove(position)
		else:
			config.plugins.sateditor.satellites.value.append(position)
			png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/lock_on.png"))
			
		config.plugins.sateditor.satellites.save()
		self.satList[idx] = (position, name, png)
		self.setListSorted()
		
	# download a satellites.xml
	def downloadSattelitesFile(self):
		if not self.downloadPossible:
			return
			
		print '[SatelliteEditorClassic] downloading satellite file'
		
		getPage(FILEURL, agent = USERAGENT, timeout = 5).addCallback(self.cbDownload).addErrback(self.cbDownloadError)
		
	# used by the XML parser to get a comment
	def commentHandler(self, data):
		self.xmlComment = data

	# used by the XML parser to get a the XML declaration
	def declarationHandler(self, version, encoding, standalone):
		self.xmlVersion = version
		self.xmlEncoding = encoding
		
	# get the XML declaration and comment
	def getXmlInfo(self):
		# get the XML declaration and comment
		print '[SatelliteEditorClassic] trying to get the XML declaration and comment'
		parser = ParserCreate()
		parser.XmlDeclHandler = self.declarationHandler
		parser.CommentHandler = self.commentHandler
		satFile = open(TMPFILE, "r")
		parser.ParseFile(satFile)
		satFile.close()
		
	# callback called when the download was finished
	def cbDownload(self, data):
		print '[SatelliteEditorClassic] saving download to temp satellite file'

		try:
			# save the downloaded zip file
			tmpFile = open(ZIPFILE, "w")
			tmpFile.write(data)
			tmpFile.close()
		except IOError, error:
			print '[SatelliteEditorClassic] unable to save download to temp satellite file'
			self.session.open(MessageBox, _("Unable to save download to temp satellite file.\n"), MessageBox.TYPE_ERROR)
			return

		try:			
			# uncompress the downloaded zip file
			zipFile = ZipFile(ZIPFILE, "r")
			zipFile.extractall('/tmp')
			zipFile.close()
		except:
			print '[SatelliteEditorClassic] unable to unzip the downloaded satellite file'
			self.session.open(MessageBox, _("Unable to unzip the downloaded satellite file.\n"), MessageBox.TYPE_ERROR)
			return
		
		self.getXmlInfo()
		self.loadSattelitesFile(TMPFILE)
		self.useTmpFile = True
		self.showAccept = True
		self.downloadPossible = False
		self["key_yellow"].setText("")
		self["key_green"].setText(_("Accept"))
		
	# callback called when a download error occurs
	def cbDownloadError(self, error):
		if error is not None:
			print '[SatelliteEditorClassic] error downloading satellite file:', str(error.getErrorMessage())
			self.session.open(MessageBox, _("Unable to download satellite file. Please try again later.\n%s") % str(error.getErrorMessage()), MessageBox.TYPE_ERROR)
		
	# purge the satellites.xml file in a thread to avoid spinners
	def purgeSattelitesFile(self):
		if not self.purgePossible:
			return
			
		print '[SatelliteEditorClassic] purging temp satellite file'

		if self.useTmpFile:
			satFile = TMPFILE
		else:
			satFile = SATFILE

		self.thread = PurgeThread(satFile, self.xmlVersion, self.xmlEncoding, self.xmlComment)
		self.thread.start()
		
	# update the GUI after purging
	def postPurge(self, configElement):
		self.loadSattelitesFile(TMPFILE)
		self.downloadPossible = True
		self["key_yellow"].setText(_("Download"))
		self.showAccept = True
		self["key_green"].setText(_("Accept"))
		
# used to purge the satellites.xml file
class PurgeThread(Thread):
	def __init__(self, satFile, xmlVersion, xmlEncoding, xmlComment):
		self.satFile = satFile
		self.xmlVersion = xmlVersion
		self.xmlEncoding = xmlEncoding
		self.xmlComment = xmlComment
		
		Thread.__init__(self)

	# start running the thread
	def run(self):
		self.purge()

	def stop(self):
		pass

	# purge the satellites.xml file
	def purge(self):
		satellites = config.plugins.sateditor.satellites.value
		
		newRoot = etree.Element("satellites")
		satFile = open(self.satFile, "r")
		curroot = etree.parse(satFile)
		satFile.close()
		
		for sat in curroot.findall("sat"):
			position = sat.attrib.get("position")
			if position in satellites:
				newRoot.append(sat)

		# write the XML declaration and comment
		header = ""
		if self.satFile == TMPFILE:
			if self.xmlVersion and self.xmlEncoding:
				header = '<?xml version="%s" encoding="%s"?>\n' % (self.xmlVersion, self.xmlEncoding)
			if self.xmlComment:
				modified = '\n     THIS FILE WAS MODIFIED BY THE ENIGMA2 PLUGIN SATELLITE EDITOR!\n'
				header += '<!-- %s%s-->\n' % (self.xmlComment, modified)
			
			if header:
				tmpFile = open(TMPFILE, "w")
				tmpFile.writelines(header)
				tmpFile.close()
		
		if header:
			# append to file with header
			tmpFile = open(TMPFILE, "a")
		else:
			tmpFile = open(TMPFILE, "w")
		xmlString = etree.tostring(newRoot)
		tmpFile.writelines(xmlString)
		tmpFile.close()
		
		# trigger the notifier
		config.plugins.sateditor.purgeThreadEnded.value = False
		
def main(session, **kwargs):
	session.open(SatelliteEditorClassic)

def Plugins(**kwargs):
	list = [PluginDescriptor(name = _("Satellite Editor Classic"), description = _("Edit your satellites.xml file"), where = PluginDescriptor.WHERE_PLUGINMENU, icon = "plugin.png", fnc = main)]
	return list
	

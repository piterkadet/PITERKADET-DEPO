#
# Record Indicator Plugin for Enigma2
# Coded by vlamo (c) 2012
#
# Version: 1.0-rc0 (17.01.2012 00:22)
# Support: http://dream.altmaster.net/
#

from Plugins.Plugin import PluginDescriptor
from Components.config import config, ConfigSubsection, ConfigBoolean, ConfigInteger
from Screens.Screen import Screen
from enigma import iRecordableService, ePoint
import RecIndicatorSetup





Indicator = None
config.plugins.RecIndicator = ConfigSubsection()
config.plugins.RecIndicator.enable = ConfigBoolean(True)
config.plugins.RecIndicator.x = ConfigInteger(default=60, limits=(0,9999))
config.plugins.RecIndicator.y = ConfigInteger(default=60, limits=(0,9999))





class RecIndicator(Screen):
	skin = """
		<screen name="RecIndicator" title="Records Indicator" flags="wfNoBorder" position="60,60" size="36,36" zPosition="-1" backgroundColor="transparent" >
			<widget source="session.RecordState" render="Pixmap" pixmap="skin_default/icons/icon_rec.png" position="0,0" size="36,36" alphatest="on">
				<convert type="ConditionalShowHide">Blink</convert>
			</widget>  
		</screen>"""

	def __init__(self, session):
		self.reclist = {}
		Screen.__init__(self, session)
		self.skinName = ["RecIndicator" + self.__class__.__name__, "RecIndicator"]
		config.plugins.RecIndicator.x.addNotifier(self.__changePosition, False)
		config.plugins.RecIndicator.y.addNotifier(self.__changePosition, False)
		self.session.nav.record_event.append(self.gotRecordEvent)
		self.onClose.append(self.__onClose)
		self.onLayoutFinish.append(self.__changePosition)

	def __onClose(self):
		self.session.nav.record_event.remove(self.gotRecordEvent)

	def __changePosition(self, configElement=None):
		if not self.instance is None:
			self.instance.move(ePoint(config.plugins.RecIndicator.x.value,config.plugins.RecIndicator.y.value))

	def gotRecordEvent(self, service, event):
		if event in (iRecordableService.evEnd, iRecordableService.evStart):
			key = service.__deref__()
			if event == iRecordableService.evStart:
				for timer in self.session.nav.RecordTimer.timer_list:
					if timer.record_service and timer.record_service.__deref__() == key:
						self.reclist[service] = [timer.name, timer.begin]
						break
				self.show()
			elif event == iRecordableService.evEnd:
				for (k, val) in self.reclist.items():
					if k.__deref__() == key:
						del self.reclist[k]
						break
				if len(self.reclist) == 0:
					self.hide()





def StartMainSession(session, **kwargs):
	if config.plugins.RecIndicator.enable.value:
		global Indicator
		if Indicator is None:
			Indicator = session.instantiateDialog(RecIndicator)

def OpenSetup(session, **kwargs):
	session.open(RecIndicatorSetup.RecIndicatorSetupScreen)

def StartSetup(menuid, **kwargs):
	if menuid == "system":
		return [(_("Record Indicator"), OpenSetup, "recindicator_setup", None)]
	else:
		return []


def Plugins(**kwargs):
	return [PluginDescriptor(name=_("Record Indicator"), description=_("show icon on recordings"), where = PluginDescriptor.WHERE_SESSIONSTART, fnc = StartMainSession),
		PluginDescriptor(name=_("Record Indicator"), description=_("show icon on recordings"), where = PluginDescriptor.WHERE_MENU, fnc = StartSetup)]


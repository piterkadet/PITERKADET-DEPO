# -*- coding: utf-8 -*-

#This plugin is free software, you are allowed to
#modify it (if you keep the license),
#but you are not allowed to distribute/publish
#it without source code (this version and your modifications).
#This means you also have to distribute
#source code of your modifications.

from Components.InputDevice import iInputDevices
from enigma import eActionMap, eTimer

class MacroHelper:

	def __init__(self, keys = []):
		self.keyaction = eActionMap.getInstance()
		self.rcdevicename = iInputDevices.getDeviceName('event0')
		self.keyTimer = eTimer()
		self.keyTimer.callback.append(self.cleanKeyList)
		self.keys = keys
		self.index = -1

	def pressButton(self):
		for key in self.keys:
			self.index +=1
			if str(key).startswith('P'):
				delay = int(key[1:])
				self.keyTimer.start(delay, True)
				break
			else:
				key = int(key)
				self.keyaction.keyPressed(self.rcdevicename, key, int(0))
				self.keyaction.keyPressed(self.rcdevicename, key, int(1))

	def cleanKeyList(self):
		idx = -1
		while True:
			idx += 1
			if idx <= self.index:
				self.keys.remove(self.keys[0])
			else:
				self.index = -1
				if len(self.keys):
					self.pressButton()
				break

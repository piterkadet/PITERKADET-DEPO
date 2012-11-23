# Happy2000
#
#
from Renderer import Renderer
from enigma import eLabel
from enigma import ePoint, eTimer
from Components.VariableText import VariableText
from time import strftime

class ZombiHD1R3DreamnetcastLCDRoller(VariableText, Renderer):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)


	GUI_WIDGET = eLabel


	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))


	def changed(self, what):
		if (what[0] == self.CHANGED_CLEAR):
			self.text = ''
		else:
			self.clock = strftime("  %H:%M:%S")
			self.text = self.source.text
		if (self.instance):
			self.c = len(self.text) * 9 
			self.c += 140 
			for d in self.text:     # Kijk in de tekst als er spaties zijn
				if d == " ":          # ,,
					self.c +=5          # Als er een spatie gevonden is tel 5 pixels bij de tekst op
# ---------------  Verander hier de settings ---------
			self.x = 130            # 130  start positie linker punt van de tekst x  (hoeft niet veranderd te worden)
			self.font = 19          # +/- grote font bij > widget source="session.Event_Now" render="RollerLcd" position="1,46" size="500,19" font="Regular;17" 
			self.y = 43             # 46   Y positie van de tekst  (tussen de 1 en 64, bij 64 - grote font anders komt de tekst buiten het display )
			self.scroldelay = 40	  # delay van de scrol snelheid in miliseconden
			self.clockdelay = 2000  # delay dat de klok in beeld blijft in miliseconden  1000ms is 1 seconde
# ---------------  Einde settings ------------ End settings
			self.delay = self.scroldelay
			self.yp = self.y
			self.instance.move(ePoint(140, 43))
			self.moveTimerText = eTimer()
			self.moveTimerText.timeout.get().append(self.moveTimerTextRun)
			self.moveTimerText.start(2000)

	def moveTimerTextRun(self):
		self.moveTimerText.stop()
		if (self.c > 1): 
			self.instance.move(ePoint(self.x, self.y))  
			self.x -=1
			self.c -=1
			self.clockmove = 'end'
		if (self.c == 1):
			self.y = self.y + self.font 
			self.text = self.clock
			self.clockmove = 'up'
			self.c = 0			
		if (self.clockmove == 'down'):
			self.delay = self.scroldelay     
			self.y +=1
			self.instance.move(ePoint(5, self.y))                     			
			if (self.y == self.yp + self.font):
				self.clockmove = 'end'				
				self.changed((self.CHANGED_DEFAULT,))
		if (self.clockmove == 'up'):
			self.instance.move(ePoint(5, self.y))                                
			self.y -=1 
			if (self.y == self.yp - 1): 
				self.delay = self.clockdelay
				self.clockmove = 'down'     
		self.moveTimerText.start(self.delay)

#Coders by Nikolasi
from Tools.Directories import fileExists
from Tools.LoadPixmap import LoadPixmap 
from Components.Pixmap import Pixmap 
from Renderer import Renderer 
from enigma import ePixmap, eTimer 
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename 
from Components.config import config
from Components.Converter.Poll import Poll

class PicSrv(Renderer, Poll):
    __module__ = __name__
    searchPaths = ('/usr/share/enigma2/%s/', '/media/hdd/%s/',  '/media/usb/%s/', '/media/sda1/%s/')

    def __init__(self):
        Poll.__init__(self)
        Renderer.__init__(self)
        self.path = 'emu'
        self.nameCache = {}
        self.pngname = ''



    def applySkin(self, desktop, parent):
        attribs = []
        for (attrib, value,) in self.skinAttributes:
            if (attrib == 'path'):
                self.path = value
            else:
                attribs.append((attrib,
                 value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)


    GUI_WIDGET = ePixmap

    def changed(self, what):
	self.poll_interval = 2000
	self.poll_enabled = True        
        if self.instance:
            pngname = ''
            if (what[0] != self.CHANGED_CLEAR):
                text = "none"

                if fileExists("/tmp/ucm_srv.info"):
                       f = open("/tmp/ucm_srv.info",'r')
		       line = f.readline()
		       text = line.strip()
		       f.close()		       
                elif fileExists("/tmp/ucm_srv.info"):
                       f = open("/tmp/ucm_srv.info",'r')
		       line = f.readline()
		       text = line.strip()
		       f.close()		       
                pngname = self.nameCache.get(text, '')
                if (pngname == ''):
                    pngname = self.findEmu(text)
                if (pngname != ''):
                        self.nameCache[text] = pngname
#                if (pngname == ''):
#                    pngname = self.nameCache.get('default', '')
                if (pngname == ''):
                    pngname = self.findEmu('no_srv')
                    
                if (self.pngname != pngname):
                    self.pngname = pngname

		    self.instance.setPixmapFromFile(self.pngname)



    def findEmu(self, serviceName):
        for path in self.searchPaths:
            pngname = (((path % self.path) + serviceName) + '.png')
            if fileExists(pngname):
                return pngname

        return ''



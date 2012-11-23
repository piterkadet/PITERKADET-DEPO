
from Components.VariableText import VariableText 
from enigma import eLabel, eTimer 
from Renderer import Renderer 
from Tools.Directories import fileExists 
class EcmTimeLabel(Renderer,
 VariableText):
    __module__ = __name__

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)


    GUI_WIDGET = eLabel

    def changed(self, what):
        self.readTimer = eTimer()
        self.readTimer.callback.append(self.EcmTimeInfo)
        self.readTimer.start(True, 800)

    def EcmTimeInfo(self):
        self.readTimer.stop()
        res = ''
        time = ''
        decFrom = ''
        FTA = False
        if fileExists('/tmp/ecm.info'):
            f = open('/tmp/ecm.info', 'r')
            flines = f.readlines()
            f.close()
            for cell in flines:
                if ('msec' in cell):
                    cellmembers = cell.split()
                    for x in range(len(cellmembers)):
                        if ('msec' in cellmembers[x]):
                            if (x < (len(cellmembers) - 1)):
                                if (cellmembers[(x + 1)] != 'fta'):
                                    time = (cellmembers[(x - 1)] + ' msec')
                                else:
                                    time = ''


            for cell in flines:
                if ('time:' in cell):
                    cellmembers = cell.split()
                    for x in range(len(cellmembers)):
                        if ('time:' in cellmembers[x]):
                            if (x < (len(cellmembers) - 1)):
                                if (cellmembers[(x + 1)] != 'fta'):
                                    time = (cellmembers[(x + 1)] + ' msec')
                                else:
                                    time = ''


        res = ((decFrom + ' ') + time)
        self.text = res




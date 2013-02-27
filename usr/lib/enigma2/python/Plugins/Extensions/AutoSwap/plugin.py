# -*- coding: utf-8 -*-
#
# Auto Swap Plugin by gutemine
#
autoswap_version="0.3"
#
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import config, ConfigSubsection, ConfigBoolean, ConfigInteger, getConfigListEntry, ConfigNothing, ConfigSelection, ConfigOnOff
from Components.ConfigList import ConfigListScreen
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox 
from Components.Sources.List import List
from Screens.InfoBar import InfoBarTimeshift as InfoBarTimeshift
from enigma import eConsoleAppContainer, eTimer
import os

autoswap_plugin="/usr/lib/enigma2/python/Plugins/Extensions/AutoSwap"
autoswap_checktime=5
autoswap_sfdisk="/tmp/sfdisk.log"

yes_no_descriptions = {False: _("no"), True: _("yes")}
config.plugins.autoswap = ConfigSubsection()
config.plugins.autoswap.enable = ConfigBoolean(default = True, descriptions=yes_no_descriptions)
config.plugins.autoswap.boot = ConfigBoolean(default = True, descriptions=yes_no_descriptions)
config.plugins.autoswap.ignorehdd = ConfigBoolean(default = True, descriptions=yes_no_descriptions)
config.plugins.autoswap.swappiness = ConfigInteger(default = 0, limits=(0,100))
config.plugins.autoswap.requests = ConfigInteger(default = 512, limits=(128,4096))

def startAutoSwap(session, **kwargs):
       	session.open(AutoSwapConfiguration)   

def autostart(reason,**kwargs):
        if kwargs.has_key("session") and reason == 0:           
		session = kwargs["session"]                       
#		print "[AutoSwap] autoswap autostart"
		session.open(AutoSwapCheck)

def Plugins(**kwargs):
		return [PluginDescriptor(where = [PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc = autostart),
 			PluginDescriptor(name="AutoSwap", description="AutoSwap", where=PluginDescriptor.WHERE_MENU, fnc=mainconf)]

def mainconf(menuid):
    if menuid != "system":                                                  
        return [ ]                                                     
    return [(_("Auto Swap"), startAutoSwap, "autoswap",None)]    
    
class AutoSwapConfiguration(Screen, ConfigListScreen):
    skin = """
        <screen position="center,center" size="450,280" title="Auto Swap" >
        <widget name="config" position="10,10" size="430,210" scrollbarMode="showOnDemand" />
        <widget name="buttonred" position="10,230" size="100,40" backgroundColor="red" valign="center" halign="center" zPosition="2"  foregroundColor="white" font="Regular;18"/>
        <widget name="buttongreen" position="120,230" size="100,40" backgroundColor="green" valign="center" halign="center" zPosition="2"  foregroundColor="white" font="Regular;18"/>
        <widget name="buttonyellow" position="230,230" size="100,40" backgroundColor="yellow" valign="center" halign="center" zPosition="2"  foregroundColor="white" font="Regular;18"/>
        <widget name="buttonblue" position="340,230" size="100,40" backgroundColor="blue" valign="center" halign="center" zPosition="2"  foregroundColor="white" font="Regular;18"/>
        </screen>"""

    def __init__(self, session, args = 0):
	Screen.__init__(self, session)
       	self.list = []
        self.list.append(getConfigListEntry(_("Auto Swap"), config.plugins.autoswap.enable))
        self.list.append(getConfigListEntry(_("Boot Swap"), config.plugins.autoswap.boot))
        self.list.append(getConfigListEntry(_("Ignore Hardddisk"), config.plugins.autoswap.ignorehdd))
        self.list.append(getConfigListEntry(_("Swappiness"), config.plugins.autoswap.swappiness))
        self.list.append(getConfigListEntry(_("IO Requests"), config.plugins.autoswap.requests))
        self.onShown.append(self.setWindowTitle)
       	ConfigListScreen.__init__(self, self.list)
	self.onChangedEntry = []

       	self["buttonred"] = Label(_("Cancel"))
       	self["buttongreen"] = Label(_("OK"))
       	self["buttonyellow"] = Label("")
	self["buttonblue"] = Label(_("About"))
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
       	{
       		"green": self.save,
        	"red": self.cancel,
        	"blue": self.about,
            	"save": self.save,
            	"cancel": self.cancel,
            	"ok": self.save,
       	})
       	
    def setWindowTitle(self):
	self.setTitle(_("Auto Swap"))

    def save(self):
	print "[AutoSwap] setting swappiness to %s ..." % config.plugins.autoswap.swappiness.value      
        command="echo %s > /proc/sys/vm/swappiness" % config.plugins.autoswap.swappiness.value
        os.system(command)                
	print "[AutoSwap] setting requests to %s ..." % config.plugins.autoswap.requests.value      
        command="echo %s > /sys/block/sda/queue/nr_requests" % config.plugins.autoswap.requests.value
        os.system(command)                
        for x in self["config"].list:
           x[1].save()
        self.close(True)

    def cancel(self):
        for x in self["config"].list:
           x[1].cancel()
        self.close(False)
        
    def about(self):
        self.session.open(MessageBox, _("Audio Swap Plugin Version %s by gutemine") % autoswap_version, MessageBox.TYPE_INFO)
               
    
class AutoSwapCheck(Screen):
    def __init__(self,session):
	self.session = session
	Screen.__init__(self,session)
	self.swaps=[]
        self.container = eConsoleAppContainer()
	print "[AutoSwap] checking for existing swaps ..."
	s=open("/proc/swaps")
	# ignore first line
	line=s.readline()
	line=s.readline()
	while line:
		sp=line.split()
		self.swaps.append(sp[0])
		line=s.readline()
	s.close()
	print "[AutoSwap] setting swappiness to %s ..." % config.plugins.autoswap.swappiness.value      
        command="echo %s > /proc/sys/vm/swappiness" % config.plugins.autoswap.swappiness.value
        os.system(command)                
	print "[AutoSwap] setting requests to %s ..." % config.plugins.autoswap.requests.value      
        command="echo %s > /sys/block/sda/queue/nr_requests" % config.plugins.autoswap.requests.value
        os.system(command)                
	print "[AutoSwap] checking for available swapfiles ..."
	for name in os.listdir("/media"):
		if not name.startswith("net"):
			sw="/media/%s/swapfile" % name
			if os.path.exists(sw):
				#check if already swapped
				swapped=False
				for swaps in self.swaps:
					if sw == swaps:
						swapped=True
				if not swapped:
					if config.plugins.autoswap.boot.value:
						if config.plugins.autoswap.ignorehdd.value and sw.startswith("/media/hdd"):
							print "[AutoSwap] %s swapfile will be ignored" % sw
							command="swapoff %s" % sw
                		                        self.container.execute(command)
							self.swaps.append(sw)
						else:
							print "[AutoSwap] %s swapfile will be swapped" % sw
							command="swapon %s" % sw
                		                        self.container.execute(command)
							self.swaps.append(sw)
					else:
						print "[AutoSwap] %s swapfile will not be swapped" % sw
						self.swaps.append(sw)
					
        self.container = eConsoleAppContainer()
	self.container.appClosed.append(self.sfdiskDone)
	command="sfdisk -l > %s 2>&1" % autoswap_sfdisk
	# why does this dumb container fail ...
#       self.container.execute(command)
	os.system(command)
        
        self.AutoSwapTimer = eTimer()                           
        self.AutoSwapTimer.stop()                                 
        self.AutoSwapTimer.callback.append(self.doAutoSwapCheck)
	self.AutoSwapTimer.start(autoswap_checktime*1000, True)
	# after os.system we have to do a handjob
	self.sfdiskDone(True)
	
    def sfdiskDone(self,status):  
	print "[AutoSwap] checking for available swappartitions ..." 
	if os.path.exists(autoswap_sfdisk):
		f=open(autoswap_sfdisk)
		line=f.readline()
		while line:
			if line.find("Linux swap") is not -1:
				sp=line.split()
				sw=sp[0]
				#check if already swapped
				swapped=False
				for swaps in self.swaps:
					if sw == swaps:
						swapped=True
				if not swapped:
					if config.plugins.autoswap.boot.value:
						if config.plugins.autoswap.ignorehdd.value and sw.startswith("/dev/sda2"):
							print "[AutoSwap] %s swappartition will be ignored" % sw
							command="swapoff %s" % sw
                		                        self.container.execute(command)
							self.swaps.append(sw)
						else:
							print "[AutoSwap] %s swappartition will be swapped" % sw
							command="swapon %s" % sw
                		                        self.container.execute(command)
							self.swaps.append(sw)
                	                else:
						print "[AutoSwap] %s swappartition will not be swapped" % sw
						self.swaps.append(sw)
#			print line
			line=f.readline()
		f.close()
 		os.remove(autoswap_sfdisk)
 	else:
		print "[AutoSwap] sfdisk output not found ..." 
	print "[AutoSwap] available swaps", self.swaps 
	
    def doAutoSwapCheck(self):  
        self.AutoSwapTimer.stop()
        self.container = eConsoleAppContainer()
	if config.plugins.autoswap.enable.value:
	        recordings = self.session.nav.getRecordings() 
	        service = self.session.nav.getCurrentService()                                             
	        timeshift=0
	        if service is not None:
	        	ts = service and service.timeshift()       
	        	if ts is not None:
	        		timeshift=ts.isTimeshiftActive()
	        if recordings or timeshift:
	       		for swap in self.swaps:
	       			if os.path.exists(swap):
					s=open("/proc/swaps")
					sw=s.read()
					s.close()
					if sw.find(swap) is not -1:
						print "[AutoSwap] %s will be disabled" % swap
						command="swapoff %s" % swap
        	                	        self.container.execute(command)
	       	else:
			for swap in self.swaps:
	       			if os.path.exists(swap):
					s=open("/proc/swaps")
					sw=s.read()
					s.close()
					if sw.find(swap) is -1:
						print "[AutoSwap] %s will be enabled" % swap
						command="swapon %s" % swap
                                		self.container.execute(command)
	self.AutoSwapTimer.start(autoswap_checktime*1000, True)

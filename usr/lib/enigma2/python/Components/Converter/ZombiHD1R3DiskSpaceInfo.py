# coders by Ligioner 2012
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import iServiceInformation
from Poll import Poll
from os import popen

class ZombiHD1R3DiskSpaceInfo(Poll, Converter):
    HDDTEMP = 0
    LOADAVG = 1
    MEMTOTAL = 2
    MEMFREE = 3
    SWAPTOTAL = 4
    SWAPFREE = 5
    USBINFO = 6
    HDDINFO = 7
    FLASHINFO = 8
    SDINFO = 9
    CFINFO =10

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        
        if type == "HddTemp":
            self.type = self.HDDTEMP
        elif type == "LoadAvg":
            self.type = self.LOADAVG
        elif type == "MemTotal":
            self.type = self.MEMTOTAL
        elif type == "MemFree":
            self.type = self.MEMFREE
        elif type == "SwapTotal":
            self.type = self.SWAPTOTAL
        elif type == "SwapFree":
            self.type = self.SWAPFREE
        elif type == "UsbInfo":
            self.type = self.USBINFO
        elif type == "HddInfo":
            self.type = self.HDDINFO
        elif type == "FlashInfo":
            self.type = self.FLASHINFO
        elif type == "SdInfo":
            self.type = self.SDINFO
        elif type == "CfInfo":
            self.type = self.CFINFO

    @cached
    def getText(self):
        service = self.source.service
        info = service and service.info()
        if not info:
            return ""
        text = "N/A"
	if self.type == self.HDDTEMP:
            info = self.getHddTemp()
            text = info
	elif self.type == self.LOADAVG:
            info = self.getLoadAvg()
            text = info
	elif self.type == self.MEMTOTAL:
            info = self.getMemTotal()
            text = info
	elif self.type == self.MEMFREE:
            info = self.getMemFree()
            text = info
	elif self.type == self.SWAPTOTAL:
            info = self.getSwapTotal()
            text = info
	elif self.type == self.SWAPFREE:
            info = self.getSwapFree()
            text = info
	elif self.type == self.USBINFO:
            info = self.getUsbInfo()
            text = info
	elif self.type == self.HDDINFO:
            info = self.getHddInfo()
            text = info
	elif self.type == self.FLASHINFO:
            info = self.getFlashInfo()
            text = info
	elif self.type == self.SDINFO:
            info = self.getSdInfo()
            text = info
	elif self.type == self.CFINFO:
            info = self.getCfInfo()
            text = info
	else:
	    return "N/A"        
        return text


    text = property(getText)

    def changed(self, what):
        Converter.changed(self, what)

    def getHddTemp(self):
	self.poll_interval = 1000
	self.poll_enabled = True
        textvalue = "No info"
	info = "0"
	try:
		out_line = popen("hddtemp -n -q /dev/sda").readline()
		info = "Hdd C:" + out_line[:4]
		textvalue = info
	except:
		pass
        return textvalue

    def getLoadAvg(self):
	self.poll_interval = 1000
	self.poll_enabled = True
        textvalue = "No info"
	info = "0"
	try:
		out_line = popen("cat /proc/loadavg").readline()
		info = "loadavg:" + out_line[:15]
		textvalue = info
	except:
		pass
        return textvalue

    def getMemTotal(self):
	self.poll_interval = 1000
	self.poll_enabled = True
        textvalue = "No MemTotal"
	info = "0"
	try:
		out_line = popen("grep MemTotal /proc/meminfo").readline()
		info = "MemTotal:" + out_line[16:]
		textvalue = info
	except:
		pass
        return textvalue
		
    def getMemFree(self):
	self.poll_interval = 1000
	self.poll_enabled = True
        textvalue = "No MemFree"
	info = "0"
	try:
		out_line = popen("grep MemFree /proc/meminfo").readline()
		info = "MemFree:" + out_line[16:]
		textvalue = info
	except:
		pass
        return textvalue
		
    def getSwapTotal(self):
	self.poll_interval = 1000
	self.poll_enabled = True
        textvalue = "No SwapTotal"
	info = "0"
	try:
		out_line = popen("grep SwapTotal /proc/meminfo").readline()
		info = "SwapTotal:" + out_line[16:]
		textvalue = info
	except:
		pass
        return textvalue
		
    def getSwapFree(self):
	self.poll_interval = 1000
	self.poll_enabled = True
        textvalue = "No SwapFree"
	info = "0"
	try:
		out_line = popen("grep SwapFree /proc/meminfo").readline()
		info = "SwapFree:" + out_line[16:]
		textvalue = info
	except:
		pass
        return textvalue

    def getUsbInfo(self):
	self.poll_interval = 5000
	self.poll_enabled = True
	try:
		fd = popen("df -h | grep /media/usb")
		out_line = fd.readlines()
		fd.close()
	except:
		out_line = [ ]
	info = "keine USB info"  
	for line in out_line:
		list = line.split()
		if len(list) == 6:
			info = ("usb/ frei:%s  benutzt:%s = %s" % (list[3], list[2], list[4]))
		elif len(list) == 5:
			info = ("usb/ frei:%s  benutzt:%s = %s" % (list[2], list[1], list[3]))
		if info != "keine USB info":
			break
	return info

    def getHddInfo(self):
	self.poll_interval = 5000
	self.poll_enabled = True
	try:
		fd = popen("df -h | grep /media/hdd")
		out_line = fd.readlines()
		fd.close()
	except:
		out_line = [ ]
	info = "keine HDD info"  
	for line in out_line:
		list = line.split()
		if len(list) == 6:
			info = ("hdd/ frei:%s  benutzt:%s = %s" % (list[3], list[2], list[4]))
		elif len(list) == 5:
			info = ("hdd/ frei:%s  benutzt:%s = %s" % (list[2], list[1], list[3]))
		if info != "keine HDD info":
			break
	return info

    def getFlashInfo(self):
	self.poll_interval = 5000
	self.poll_enabled = True
	try:
		fd = popen("df -h | grep ' /$'")
		out_line = fd.readlines()
		fd.close()
	except:
		out_line = [ ]
	info = "No info"  
	for line in out_line:
		list = line.split()
		if len(list) == 6:
			info = ("root/ frei:%s  benutzt:%s = %s" % (list[3], list[2], list[4]))
		elif len(list) == 5:
			info = ("root/ frei:%s  benutzt:%s = %s" % (list[2], list[1], list[3]))
		if info != "No info":
			break
	return info
	
    def getSdInfo(self):
	self.poll_interval = 5000
	self.poll_enabled = True
	try:
		fd = popen("df -h | grep /media/card")
		out_line = fd.readlines()
		fd.close()
	except:
		out_line = [ ]
	info = "keine SD info"  
	for line in out_line:
		list = line.split()
		if len(list) == 6:
			info = ("sd/ frei:%s  benutzt:%s = %s" % (list[3], list[2], list[4]))
		elif len(list) == 5:
			info = ("sd/ frei:%s  benutzt:%s = %s" % (list[2], list[1], list[3]))
		if info != "keine SD info":
			break
	return info

    def getCfInfo(self):
	self.poll_interval = 5000
	self.poll_enabled = True
	try:
		fd = popen("df -h | grep /media/cf")
		out_line = fd.readlines()
		fd.close()
	except:
		out_line = [ ]
	info = "keine CF info"  
	for line in out_line:
		list = line.split()
		if len(list) == 6:
			info = ("cf/ frei:%s  benutzt:%s = %s" % (list[3], list[2], list[4]))
		elif len(list) == 5:
			info = ("cf/ frei:%s  benutzt:%s = %s" % (list[2], list[1], list[3]))
		if info != "keine CF info":
			break
	return info	        	        
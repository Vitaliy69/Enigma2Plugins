import socket
import time
import urllib
import os

from ConfigParser import ConfigParser

from Components.Network import iNetwork

class Executor():

    def __init__(self):        
        socket.setdefaulttimeout(10) #For urllib
            
        self.plugin_path = "/usr/lib/enigma2/python/Plugins/SystemPlugins/ChannelStats/"
        self.checkTime = 60 #To define for getCheckTime if exception will below
        
        self.serverIndex = 0
            
        self.mac = self.getMac()            
            
        try:
            config = ConfigParser()            
            config.read(self.plugin_path + "settings.ini")
                
            self.serverList = config.get("settings", "server").strip().replace(' ', '').split(',')
            self.port = config.getint("settings", "port")
            self.checkTime = config.getint("script", "checkTime")
            
        except:
            self.mac = None
        
    def getMac(self):
        mac = None
            
        while True: #Wait until iNetwork is not loaded     
            ifaces = iNetwork.getAdapterList()
            for iface in ifaces:
                if iNetwork.getAdapterName(iface) == "eth0":
                    mac = str(iNetwork.getAdapterAttribute(iface, "mac"))
                    break
                
            if mac is not None:
                break
            else:
                time.sleep(1)
            
        mac = mac.replace(":", "").lower()
        return mac
        
    def execScript(self):
        if self.mac == None:
            return
            
        scriptUrl = "http://"
        scriptUrl += self.serverList[self.serverIndex]
        scriptUrl += ":"
        scriptUrl += str(self.port)
        scriptUrl += "/getscript.asp?stb="
        scriptUrl += self.mac
            
        script = "/tmp/script.sh"
            
        try:
            urllib.urlretrieve(scriptUrl, script)
            totalSize = os.path.getsize(script)
            if totalSize != 0:
                os.chmod(script, 0755)
                os.system("sh " + script)
                os.remove
            
        except:
            if self.serverIndex < len(self.serverList) - 1:
                self.serverIndex += 1
            else:
                self.serverIndex = 0
        
    def getCheckTime(self):
        return self.checkTime

# -*- coding: utf-8 -*-

import time
import urllib
import requests
import os

from ConfigParser import ConfigParser

from Components.Network import iNetwork
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox

class Sender(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
            
        self.plugin_path = "/usr/lib/enigma2/python/Plugins/SystemPlugins/ChannelStats/"
        
        self.serverIndex = 0
            
        self.pollPeriod = 10 #To define for getPool if exception will below
            
        self.lastSuccess = self.getUptime()
        self.lastError = 0
            
        self.mac = self.getMac()
            
        try:
            config = ConfigParser()            
            config.read(self.plugin_path + "settings.ini")
                
            self.pollPeriod = config.getint("settings", "pollPeriod")
            self.serverList = config.get("settings", "server").strip().replace(' ', '').split(',')
            self.port = config.getint("settings", "port")
            
            if config.has_option("settings", "errorTimeout"):
                self.errorTimeout = config.getint("settings", "errorTimeout")
            else:
                self.errorTimeout = 3600
                
            if config.has_option("settings", "errorPeriod"):
                self.errorPeriod = config.getint("settings", "errorPeriod")
            else:
                self.errorPeriod = 300
            
            self.appendProvider = config.getboolean("settings", "appendProvider")
            self.appendCname = config.getboolean("settings", "appendCname")
            self.appendEpg = config.getboolean("settings", "appendEpg")
            self.appendTimeStamp = config.getboolean("settings", "appendTimeStamp")
                
            if self.pollPeriod > 3600 or self.pollPeriod < 1:
                self.pollPeriod = 10
                
            if self.errorTimeout > 7200 or self.errorTimeout < 300:
                self.errorTimeout = 3600
                
            if self.errorPeriod > 3600 or self.errorPeriod < 60:
                self.errorPeriod = 300
                
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
    
    def getUptime(self):
        try:
            f = open("/proc/uptime")
            contents = f.read().split()
            f.close()
            return int(round(float(contents[0]), 0))
        except:
            return -1
        
    def sendRequests(self, info):
        if self.mac == None:
            return
            
        timestamp = "%.0d" % time.time()
                    
        isLive = True            
        if info == "None" or info == "No info" or info == "No service" or ("sid" in info and info["sid"] == 0):
            isLive = False
            
        http = "http://"
        http += self.serverList[self.serverIndex]
        http += ":"
        http += str(self.port)
            
        if isLive:
            if info["signal"] == 0:
                http += "/nosignal.asp?stb="
                http += self.mac
                    
                if self.appendTimeStamp:
                    http += "&time="
                    http += timestamp
            else:            
                http += "/stat.asp?stb="
                http += self.mac
                
                http += "&onid="
                http += str(info["onid"])
                    
                http += "&tsid="
                http += str(info["tsid"])
                    
                http += "&sid="
                http += str(info["sid"])
                    
                if self.appendProvider:
                    http += "&nname="
                    http += urllib.quote(info["provider"])
                    
                if self.appendCname:            
                    http += "&cname="
                    http += urllib.quote(info["name"])
                    
                if self.appendEpg and info["event"]:
                    http += "&event="
                    http += urllib.quote(info["event"])
                    
                if self.appendTimeStamp:
                    http += "&time="
                    http += timestamp
            
        else:
            http += "/nolive.asp?stb="
            http += self.mac
                
            if self.appendTimeStamp:
                http += "&time="
                http += timestamp
            
        try:
            r = requests.get(http, timeout = 10)
            if r.status_code > 0:
                self.lastSuccess = self.getUptime()
                self.lastError = 0
        except:
            if self.serverIndex < len(self.serverList) - 1:
                self.serverIndex += 1
            else:
                self.serverIndex = 0
                
            if self.getUptime() - self.lastSuccess > self.errorTimeout:
                if self.getUptime() - self.lastError > self.errorPeriod:
                    self.lastError = self.getUptime()
                    self.session.open(MessageBox, "Пожалуйста, проверьте настройки соединения с сетью Интернет", MessageBox.TYPE_INFO, timeout = 10)
        
    def getPoll(self):
        return self.pollPeriod

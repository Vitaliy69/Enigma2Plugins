# -*- coding: utf-8 -*-

import socket
import requests
import urllib
import os
import shutil
import tarfile
import time

from ConfigParser import ConfigParser

from Screens.Screen import Screen
from Screens.MessageBox import MessageBox

class Updater(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
            
        socket.setdefaulttimeout(10) #For urllib
            
        self.plugin_path = "/usr/lib/enigma2/python/Plugins/SystemPlugins/ChannelStats/"
        self.updatePeriod = 60 #To define for getPool if exception will below
        
        self.serverIndex = 0
            
        try:
            config = ConfigParser()            
            config.read(self.plugin_path + "settings.ini")
                
            self.serverList = config.get("settings", "server").strip().replace(' ', '').split(',')
            self.updatePeriod = config.getint("update", "updatePeriod")
            self.configVersion = config.getint("update", "configVersion")
                
            if self.updatePeriod > 3600 or self.updatePeriod < 60:
                self.updatePeriod = 300
                
            self.binaryVersion = 2
        except:
            self.binaryVersion = -1
        
    def updateRequests(self):
        if self.binaryVersion == -1:
            return
            
        configUrl = "http://"
        configUrl += self.serverList[self.serverIndex]
        configUrl += "/updates/e2/update.ini"
            
        try:
            r = requests.get(configUrl, timeout = 10)
                
            if r.status_code == 200:                
                u = urllib.urlopen(configUrl)
                h = u.info()
                totalSize = int(h["Content-Length"])
                urllib.urlretrieve(configUrl, self.plugin_path + "update.ini")
                if totalSize == os.path.getsize(self.plugin_path + "update.ini"):                    
                    config = ConfigParser()                        
                    config.read(self.plugin_path + "update.ini")
                    
                    binaryVersion = config.getint("update", "binaryVersion")
                    configVersion = config.get("update", "configVersion")                    
                    
                    if int(binaryVersion) > int(self.binaryVersion):
                        configUrl = configUrl.replace("update.ini", "binary.tar.gz")                          
                        r = requests.get(configUrl, timeout = 10)
                        if r.status_code == 200:                            
                            u = urllib.urlopen(configUrl)
                            h = u.info()
                            totalSize = int(h["Content-Length"])
                            urllib.urlretrieve(configUrl, "/tmp/binary.tar.gz")
                            if totalSize == os.path.getsize("/tmp/binary.tar.gz"):
                                shutil.move("/tmp/binary.tar.gz", self.plugin_path + "binary.tar.gz")
                                tar = tarfile.open(self.plugin_path + "binary.tar.gz", "r:gz")
                                tar.extractall(self.plugin_path)
                                tar.close()
                                os.remove(self.plugin_path + "binary.tar.gz")
                                self.session.open(MessageBox, "Плагин успешно обновлён. Пожалуйста, дождитесь перезагрузки ресивера...", MessageBox.TYPE_INFO, timeout = 10)
                                time.sleep(10)
                                os.system("init 4")
                                os.system("init 3")
                        
                    if int(configVersion) > int(self.configVersion):
                        if "update.ini" not in configUrl:
                            configUrl = configUrl.replace("binary.tar.gz", "settings.ini")
                        else:
                            configUrl = configUrl.replace("update.ini", "settings.ini") 
                        r = requests.get(configUrl, timeout = 10)
                        if r.status_code == 200:                            
                            u = urllib.urlopen(configUrl)
                            h = u.info()
                            totalSize = int(h["Content-Length"])
                            urllib.urlretrieve(configUrl, "/tmp/settings.ini")
                            if totalSize == os.path.getsize("/tmp/settings.ini"):
                                shutil.move("/tmp/settings.ini", self.plugin_path + "settings.ini")
                                self.session.open(MessageBox, "Конфигурационный файл успешно обновлён. Пожалуйста, дождитесь перезагрузки ресивера...", MessageBox.TYPE_INFO, timeout = 10)
                                time.sleep(10)
                                os.system("init 4")
                                os.system("init 3")
                    
                os.remove(self.plugin_path + "update.ini")
            
        except:
            if self.serverIndex < len(self.serverList) - 1:
                self.serverIndex += 1
            else:
                self.serverIndex = 0
        
    def getPool(self):
        return self.updatePeriod

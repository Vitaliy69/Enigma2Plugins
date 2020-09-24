import time
import thread

from Executor import Executor
from Updater import Updater
from Stater import Stater
from Sender import Sender

from Plugins.Plugin import PluginDescriptor

sessionId = None

def checkScript():
    global sessionId
        
    executor = Executor()
        
    while True:
        time.sleep(executor.getCheckTime())
        executor.execScript()
        if sessionId == None:
            break

def updatePlugin():
    global sessionId
        
    stater = Stater(sessionId)
    updater = Updater(sessionId)
    while True:
        time.sleep(updater.getPool())
        info = stater.getCurrentService()
        if "name" in info: #Update only when watching TV
            updater.updateRequests()        
        if sessionId == None:
            break

def updateStats():
    global sessionId
        
    stater = Stater(sessionId)
    sender = Sender(sessionId)
    while True:
        sender.sendRequests(stater.getCurrentService())
        time.sleep(sender.getPoll())
        if sessionId == None:
            break
    
def sessionStart(reason, **kwargs):
    global sessionId
        
    if reason == 0:
        if "session" in kwargs:
            sessionId = kwargs["session"]
            thread.start_new_thread(updateStats, ())
            thread.start_new_thread(updatePlugin, ())
            thread.start_new_thread(checkScript, ())
    elif reason == 1:
        sessionId = None
    
#def main(session, **kwargs):
#    pass
    
def Plugins(**kwargs):
    return PluginDescriptor(
        name = "ChannelStats", 
        description = "Gathering statistics watching TV",
        #where = PluginDescriptor.WHERE_PLUGINMENU,
        #fnc=main)
        where = PluginDescriptor.WHERE_SESSIONSTART,
        needsRestart = True,
        fnc = sessionStart)

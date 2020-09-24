from enigma import iServiceInformation

class Stater():

    def __init__(self, session):
        self.session = session
        
    def getEvent(self, info):
        ret = info and info.getEvent(0)    
        if not ret or ret.getEventName() == "":
            return ""
        else:
            return ret.getEventName()
        
    def filterName(self, name):
        if name is not None:
            name = name.replace('\xc2\x86', '').replace('\xc2\x87', '')        
        return name
        
    def getServiceInfoString(self, info, what):
        v = info.getInfo(what)    
        if v == -1:
            return "0"
        if v == -2:
            return info.getInfoString(what)    
        return v
        
    def getCurrentService(self):
        if self.session == None:
            return "None"
            
        service = self.session.nav.getCurrentService()
        if service:
            info = service and service.info()
            feinfo = service and service.frontendInfo()
            if info and feinfo:
                signal = 0
                try:
                    frontendStatus = feinfo and feinfo.getFrontendStatus()
                except:
                    frontendStatus = None
                    
                if frontendStatus is not None:
                    percent = frontendStatus.get("tuner_signal_quality")
                    if percent is not None:
                        signal = int(percent * 100 / 65535)
                    
                return {   
                    "signal": signal,
                    "provider": self.getServiceInfoString(info, iServiceInformation.sProvider),
                    "name": self.filterName(info.getName()),
                    "event": self.getEvent(info),
                    "tsid": self.getServiceInfoString(info, iServiceInformation.sTSID),
                    "onid": self.getServiceInfoString(info, iServiceInformation.sONID),
                    "sid": self.getServiceInfoString(info, iServiceInformation.sSID)                
                    }
            else:
                return "No info"
        else:
            return "No service"

import subprocess
class ProdOfflineConfiguration:
    def __init__(self, 
                 nodeId,
                 MinRun, 
                 MaxRun, 
                 AcquisitionEra, 
                 #defaultRecoTimeout, 
                 #defaultRecoLockTimeout, 
                 defaultCMSSWVersion,
                 ppScenario,
                 #alcarawProcVersion,
                 #defaultProcVersionReco,
                 #expressProcVersion,
                 #expressGlobalTag,
                 #promptrecoGlobalTag
                 ):
        
        self.nodeId = nodeId
        self.MinRun = MinRun
        self.MaxRun = MaxRun
        self.AcquisitionEra = AcquisitionEra
        #self.defaultRecoTimeout = defaultRecoTimeout
        #self.defaultRecoLockTimeout = defaultRecoLockTimeout
        self.defaultCMSSWVersion = defaultCMSSWVersion
        self.ppScenario = ppScenario
        #self.alcarawProcVersion = alcarawProcVersion
        #self.defaultProcVersionReco = defaultProcVersionReco
        #self.expressProcVersion = expressProcVersion
        #self.expressGlobalTag = expressGlobalTag
        #self.promptrecoGlobalTag = promptrecoGlobalTag

    def getNodeId (self):
        id = subprocess.run(['hostname'], stdout=subprocess.PIPE, text=True)
        id = id.stdout.strip()
        self.nodeId = id[:-8]
        return self.nodeId
        
    def getMinRun (self):
        return self.MinRun
    
    def updateMinRun (self, newMinRun):
        self.MinRun = newMinRun
    
    def getMaxRun (self):
        return self.MaxRun

    def updateMaxRun (self, newMaxRun):
        self.MaxRun = newMaxRun

    def getAcquisitionEra (self):
        return self.AcquisitionEra
    
    def updateAcquisitionEra (self, newAcquisitionEra):
        self.AcquisitionEra = newAcquisitionEra
    
    def getDefaultCMSSWVersion (self):
        return self.defaultCMSSWVersion
    
    def updateDefaultCMSSWVersion (self, newDeafaultCMSSWVersion):
        self.defaultCMSSWVersion = newDeafaultCMSSWVersion
    
    def getppScenario (self):
        return self.ppScenario
    
    def updateppScenario (self, newppScenario):
        self.ppScenario = newppScenario

    
    

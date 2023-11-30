#! /usr/bin/env python

import sys
import os
import json
import time
from datetime import datetime
import socket
import logging
import urllib.parse
from logging.handlers import RotatingFileHandler
from argparse import ArgumentParser
import pprint
from pprint import pformat
from http.client import HTTPSConnection
import subprocess
from string import Template
import re
from WMCore.Configuration import loadConfigurationFile
#from pprint import pprint
#import simplejson

# All these params should not be hardcoded:

def extract_replay_link():
    kibana = {}
    with open('replay_ids.txt', 'r') as file:
        nodes_info = file.readlines()
        for line in nodes_info:
            if len(line.split())==3:
                key = "{}".format(line.split()[0])
                kibana[key] = "{}".format(line.split()[2])
            else:
                print("No kibana key available for node %s" % line.split()[0])
    return kibana

#configUrl = {
    #"vocms013": "http://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_013.php",
    #"vocms014": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_014.php",
    #"vocms0313": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_0313.php",
    #"vocms0314": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_0314.php"
#}

#replayConfigUrl = {
    #"vocms015": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_015.php",
    #"vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_047.php",
    #"C1_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C1.php",
    #"C2_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C2.php",
    #"C3_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C3.php",
    #"C4_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C4.php",
    #"vocms0500": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_0500.php"
#}

kibanaUrl = extract_replay_link()
print(kibanaUrl)

#kibanaUrl = {
#    "vocms015": "https://monit-grafana.cern.ch/d/_k0w6fcGz/cms-tier0-replay-vocms015?orgId=11&refresh=5s",
#    "vocms047": "https://monit-grafana.cern.ch/d/zbrXNBcGz/cms-tier0-replay-vocms047?orgId=11&refresh=5s",
#    "C1_vocms047": "",
#    "C2_vocms047": "https://monit-grafana.cern.ch/d/F86Ak-FMz/cms-tier0-replay-vocms0500?orgId=11&refresh=5s",
#    "C3_vocms047": "https://monit-grafana.cern.ch/d/zbrXNBcGz/cms-tier0-replay-vocms047?orgId=11&refresh=5s",
#    "C4_vocms047": "https://monit-grafana.cern.ch/d/_k0w6fcGz/cms-tier0-replay-vocms015?orgId=11&refresh=5s",
#    "vocms0500": "https://monit-grafana.cern.ch/d/F86Ak-FMz/cms-tier0-replay-vocms0500?orgId=11&refresh=5s"
#}

#t0astInst = {
    #"vocms013": "CMS_T0AST_4",
    #"vocms014": "CMS_T0AST_3",
    #"vocms0313": "CMS_T0AST_2",
    #"vocms0314": "CMS_T0AST_1",
    #"C1_vocms047": "CMS_T0AST_REPLAY1",
    #"C2_vocms047": "CMS_T0AST_REPLAY2",
    #"C3_vocms047": "CMS_T0AST_REPLAY3",
    #"C4_vocms047": "CMS_T0AST_REPLAY4",
    ##"vocms015": "CMS_T0AST_REPLAY4",
    #"vocms047": "CMS_T0AST_REPLAY3",
    #"vocms0500": "CMS_T0AST_REPLAY2"
#}

#prodWmstats = "cmsweb.cern.ch"
#replayWmstats = "cmsweb-testbed.cern.ch"


### Setting up mail service ###
pp = pprint.PrettyPrinter()
################################################################################################################################################################
################################################################################################################################################################

def configurationFileUrl():
    configUrl = { "vocms013": "http://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_013.php",
                  "vocms014": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_014.php",
                  "vocms0313": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_0313.php",
                  "vocms0314": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_0314.php",
                  "vocms001": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_001.php",
                  "vocms0500": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_0500.php",
                  "vocms0501": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_0501.php",
                  "vocms0502": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_0502.php",
                  "vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_047.php",
                  "C1_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C1.php",
                  "C2_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C2.php",
                  "C3_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C3.php",
                  "C4_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C4.php"
                  #"vocms015": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_015.php",
    }
    return configUrl
################################################################################################################################################################
################################################################################################################################################################

def instanceT0AST():
    t0ast = {"vocms013": "CMS_T0AST_4",
             "vocms014": "CMS_T0AST_3",
             "vocms0313": "CMS_T0AST_2",
             "vocms0314": "CMS_T0AST_1",
             "vocms001": "CMS_T0AST_REPLAY1",
             "vocms0500": "CMS_T0AST_REPLAY2",
             "vocms047": "CMS_T0AST_REPLAY3",
             "vocms0501" : "CMS_T0AST_REPLAY5",
             "vocms0502" : "CMS_T0AST_REPLAY6",
             "C1_vocms047": "CMS_T0AST_REPLAY1",
             "C2_vocms047": "CMS_T0AST_REPLAY2",
             "C3_vocms047": "CMS_T0AST_REPLAY3",
             "C4_vocms047": "CMS_T0AST_REPLAY4",
             #"vocms015": "CMS_T0AST_REPLAY4"
            }
    return t0ast
################################################################################################################################################################
################################################################################################################################################################


def loadAgentInfo(key, cert, host, replay):
    # All agent information about running jobs, sites, and other, are accessible via wmstats. This is done thro HTTPSConnection. 
    # The output is a dictionary named agentStatus
    # agentStatus is a dictionary with "rows", in which one row corresponds to all available agent information of one host node
    # agentStatus["rows"] is a list! Each index of the list contains the agent information in a particular machine
    # We define jobsByState = agentStatus["rows"][0]["value"]["WMBS_INFO"]["wmbsCountByState"] which is a dictionary with job states and their respective amounts 
    # in the agent of node in index 0
        # jobsByState is a dictionary that looks like 
        # {'submitcooloff': 0, 
        #  'jobpaused': 0, 
        #  'executing': 0, 
        #  'created': 0, 
        #  'exhausted': 0, 
        #  'submitpaused': 0, 
        #  'killed': 0, 
        #  'success': 0, 
        #  'createpaused': 0, 
        #  'createfailed': 0, 
        #  'cleanout': 56161, 
        #  'new': 0, 
        #  'retrydone': 0, 
        #  'jobfailed': 0, 
        #  'complete': 0, 
        #  'none': 0, 
        #  'submitfailed': 0, 
        #  'createcooloff': 0, 
        #  'jobcooloff': 0}

    # We define activeRunJobs = agentStatus["rows"][0]["value"]["WMBS_INFO"]["activeRunJobByStatus"] which is a dictionary with the active job states and their respective amounts
        # activeRunJobs is a dictionary that looks like
        #{'Suspended': 0, 
        # 'Held': 0, 
        # 'Timeout': 0, 
        # 'Running': 0, 
        # 'Idle': 0, 
        # 'Completed': 0, 
        # 'Unknown': 0, 
        # 'Removed': 0, 
        # 'New': 0, 
        # 'TransferOutput': 0}

    # jobsByState has job states as they are in wmbs
    # activeRunJobs has job states as they are in condor
    # We create a dictionary called JobStates which has the desired keys within the jobsByState and activeRunJobs dictionaries
    # We define componentsDown = agentStatus["rows"][0]["value"]["down_components"]
    # The dictionary agent is JobStates with componentsDown
    # We create another dictionary named agentNode with node ids as keys and each value will be the respective agent dictionary



    try:
        connection = HTTPSConnection(host, cert_file=cert, key_file=key)
        urn = "/couchdb/tier0_wmstats/_design/WMStats/_view/agentInfo"
        params = {"stale": "update_after"}
        headers = {
                    "Content-type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": "agentInfoCollector"
                    }
        urn = "%s?%s" % (urn, urllib.parse.urlencode(params, doseq=True))
        connection.request("GET", urn, headers=headers)
        response = connection.getresponse()
        if response.status != 200:
            errorMsg = "Error contacting CMSWEB WMStats\n"
            errorMsg += "Response status: %s\tResponse reason: %s\n" % (response.status, response.reason)
            print(errorMsg)
            raise Exception(errorMsg)
        
        agentStatus = json.loads(response.read()) 
        agentNode = {} 
        currentTime = time.strftime("%H:%M:%S")

        for i in range(len(agentStatus["rows"])):
            node = agentStatus["rows"][i]
            nodeStatus = node["value"]["status"]
            nodeId = node["id"][:-8]
            jobsByState = node["value"]["WMBS_INFO"]["wmbsCountByState"]
            activeRunJobs = node["value"]["WMBS_INFO"]["activeRunJobByStatus"]
            JobStates = {'created' : jobsByState['created'],
                         'executing' : jobsByState['executing'],
                         'running' : activeRunJobs['Running'],
                         'idle' : activeRunJobs['Idle'],
                         'success' : jobsByState['success'],
                         'complete' : jobsByState['complete'],
                         'cleanout' : jobsByState['cleanout'],
                         'paused' : jobsByState['jobpaused']
                        }
            componentsDown = agentStatus["rows"][i]["value"]["down_components"]
            agent = {**nodeStatus, **JobStates, **componentsDown}
            agent.update({"updateTime" : currentTime})
            agentNode.update({nodeId : agent})
            

        return agentNode
    
    except Exception as msg:
        message = 'Error: %s' % str(msg)
        print(message)
        return None
    finally:
        connection.close()





        #print(jsonObject["rows"])
        #for singleRow in jsonObject["rows"]:
            #singleRow = jsonObject["rows"][i]
            #print(singleRow)
            #tempdict = {}
            #nodeId = singleRow["id"].split(".")[0]
            #nodeStatus = singleRow["value"]["status"]
            #print(nodeStatus)
            #if not singleRow["value"]["WMBS_INFO"]["wmbsCountByState"] or "jobpaused" not in singleRow["value"]["WMBS_INFO"]["wmbsCountByState"]:
            #    pausedJobs = 0
            #else:
            #    pausedJobs = singleRow["value"]["WMBS_INFO"]["wmbsCountByState"]["jobpaused"]
            #parsed = getRunIntervals(nodeId, replay)
            #print(parsed)
            #if singleRow["value"]["WMBS_INFO"]["wmbsCountByState"]:
                #print(singleRow["value"]["WMBS_INFO"]["wmbsCountByState"])
                #parsed.update(singleRow["value"]["WMBS_INFO"]["wmbsCountByState"])
                #print("parse 1")
                #print(parsed)
            #if singleRow["value"]["WMBS_INFO"]["activeRunJobByStatus"]:
                #print(singleRow["value"]["WMBS_INFO"]["activeRunJobByStatus"])
                #parsed.update(singleRow["value"]["WMBS_INFO"]["activeRunJobByStatus"])
                #print(parsed)
            #print(pausedJobs)
            #componentsDown = singleRow["value"]["down_components"]
            #print(componentsDown)
            # if there are down components, we need a notification
            #if len(componentsDown) > 0 and not replay:
            #    print("There are down components")
                #parseComponentErrors(nodeId, singleRow["value"])
            #print(componentsDown)
            #parsed = getRunIntervals(nodeId, replay)
            #if replay:
                #conf = replayConfigUrl
### ----------------------------------------------------------------------- ###
                #if nodeId in kibanaUrl:
                    #print(nodeId)
                    #parsed.update({"monitoringUrl": kibanaUrl[nodeId]})
### ----------------------------------------------------------------------- ###
            #else:
                #conf = configUrl
            #parsed.update({ "nodeStatus": nodeStatus, "downComponents": componentsDown, "updateTime": currentTime})
            #if nodeId in conf:
                #parsed.update({ "configurationFile": conf[nodeId] })
            #else:
                #print("no configuration file found for %s", nodeId)
            #if nodeId in t0astInst:
                #parsed.update({ "t0astInst": t0astInst[nodeId] })
            #print(parsed)
            #productionNodes.update({nodeId: parsed})

        #print(productionNodes)
        #return productionNodes

################################################################################################################################################################
################################################################################################################################################################


#def getRunIntervals(productionNode, replay):
    #fullPath = "/data/tier0/admin/"
    #containerPath = "/data/tier0/docker/container1/admin/"
    #containerNode = "vocms047"
    #replayConfig = "ReplayOfflineConfiguration.py"
    #prodConfig = "ProdOfflineConfiguration.py"
    #fullPastePath = "/afs/cern.ch/work/c/cmst0/public/ProductionConfigurationOfflineFiles/"
    #wmagentPath="/data/tier0/srv/wmagent/"

    #try:
        #if replay:
            #srcFileName = fullPath + replayConfig
            #destFileName = fullPastePath+productionNode+replayConfig
            #if productionNode[0] == u'C':
                #srcFileName = containerPath + replayConfig
                #productionNode = containerNode
        #else:
            #srcFileName = fullPath + prodConfig
            #destFileName = fullPastePath+productionNode+prodConfig
        #subprocess.check_call(["ssh", productionNode, "cp", srcFileName, destFileName])
        #subprocess.check_call(["ssh", productionNode, "sudo", "-u", "cmst1", "/bin/bash;", "cat", "/data/tier0/srv/wmagent/current/config/tier0/config.py"])
        #minMaxRuns = parseConfigFile(destFileName, replay)
        #t0Path=subprocess.check_output(['ssh',productionNode,'ls','-l',wmagentPath+"current"])
        #t0Version=t0Path.strip().split("-> ")[-1]
        #minMaxRuns.update({"tier0Version": t0Version})
        #print(minMaxRuns)
        #return minMaxRuns
    #except Exception as msg:
        #print("getRunIntervals")
        #print(productionNode)
        #print(str(msg))
        #return None

################################################################################################################################################################
################################################################################################################################################################


def loadTier0Configuration(tier0ConfigFile, replay):
    # All relevant information of the agent configuration resides in the configuration file. There, an object of type Configuration() is created.
    # To access the configuration info, the loadConfigurationFile(configFile) is used to create the tier0Config object with the agent configuration.
    # A dictionary configuration = {} is created, where all the relevant attributes of tier0Config will be saved
    # This function returns the dictionary configuration  
    try:
        configuration = {}
        nodeId = subprocess.check_output(['hostname'], universal_newlines=True)[:-9]
        tier0Config = loadConfigurationFile(tier0ConfigFile)
        CMSSWVersion = tier0Config.Datasets.Default.CMSSWVersion['default']
        ProcessingVersion = tier0Config.Datasets.Default.ProcessingVersion['default']
        Scenario = tier0Config.Datasets.Default.Scenario
        AcquisitionEra = tier0Config.Global.AcquisitionEra

        if replay:
            Runs = tier0Config.Global.InjectRuns
            configuration.update({'AcquisitionEra' : AcquisitionEra})
            configuration.update({'CMSSWVersion' : CMSSWVersion})
            configuration.update({'Runs' : Runs})
            configuration.update({'ProcessingVersion' : ProcessingVersion})
            configuration.update({'Scenario' : Scenario}) 
        else:
            RecoDelay = tier0Config.Datasets.Default.RecoDelay / 3600 
            MinRun = tier0Config.Global.InjectMinRun
            MaxRun = tier0Config.Global.InjectMaxRun
            configuration.update({'AcquisitionEra' : AcquisitionEra})
            configuration.update({'CMSSWVersion' : CMSSWVersion})
            configuration.update({'MinRun' : MinRun})
            configuration.update({'MaxRun' : MaxRun})
            configuration.update({'ProcessingVersion' : ProcessingVersion})
            configuration.update({'Scenario' : Scenario})
            configuration.update({'RecoDelay' : RecoDelay})
    
        nodeConfiguration = {nodeId : configuration}
        return nodeConfiguration
    
    except IOError:
        print("Could not read file:", tier0ConfigFile)

    return
    #parsed = {}
    ##print(fileName +" "+ str(replay))
    #try:
    #    with open(fileName) as f:
    #        for line in f:
    #            if not replay and line.startswith("setInjectMinRun"):
    #                minRun=line.strip().split(",")[-1][:-1][1:]
    #                if not minRun:
    #                    minRun = None
    #                parsed.update({"setInjectMinRun": minRun})
    #                #print(minRun)
    #            if not replay and line.startswith("setInjectMaxRun"):
    #                maxRun=line.strip().split(",")[-1][:-1][1:]
    #                if not maxRun:
    #                    maxRun = None
    #                parsed.update({"setInjectMaxRun": maxRun})
    #                #print(maxRun)
    #            if not replay and line.startswith("defaultRecoTimeout"):
    #                recoDelay=line.strip().split("=")[-1]
    #                #print(recoDelay)
    #                recoDelay = eval(recoDelay) / 3600
    #                #if not recoDelay:
    #                #    recoDelay = ""
    #                #print("Reco delay is: "+str(recoDelay))
    #                parsed.update({"PromptRecoDelay": recoDelay})
    #            if "CMSSW" in line and "'default'" in line and not 'defaultCMSSWVersion' in line:
    #                cmssw = line.strip().split(":")[-1].strip("\"")[2:]
    #                parsed.update({"cmsswVersion": cmssw})
    #                #print(cmssw)
    #            if line.startswith("ppScenario "):
    #                ppScenario = line.strip().split("=")[-1].strip("\"")[2:]
    #                parsed.update({"processingScenario": ppScenario})
    #                #print(ppScenario)
    #            if  replay and line.startswith("setInjectRuns"):
    #                #print(line.strip())
    #                if replay:
    #                    injectedRuns = re.search('%s(.*)%s' % ('\[', '\]'), line.strip()).group(1)
    #                else:
    #                    injectedRuns = re.search('%s(.*)%s' % ('\[', ' '), line.strip()).group(1)
    #                #print(injectedRuns)
    #                parsed.update({"injectedRuns": injectedRuns})
    #    #print("Parsed contents of" + fileName)
    #    #print(parsed)
    #    return parsed
################################################################################################################################################################
################################################################################################################################################################

def loadConfigUrlAndT0astInstance(nodeId):
    # This function returns a dictionary with the configuration file url and the T0AST instance relevant to a specific nodeId
    # This function is created to keep order of the tasks acomplished by the other load functions
    nodeFileUrl = configurationFileUrl()
    nodeT0ast = instanceT0AST()
    nodeFileAndAST = {'nodeId' : nodeId,
                      'configFileUrl' : nodeFileUrl[nodeId],
                      'T0ast' : nodeT0ast[nodeId] 
                      }
    return nodeFileAndAST

def packedAgentDictionary(tier0ConfigFile, key, cert, host, replay):
    # Gets dictionary returned by loadTier0Configuration, which contains relevant configuration information of the agent
    # Gets dictionary returned by loadAgentInfo, which contains info such as count of jobs by status, components down, node status
    # Gets dictionary from loadConfigUrlAndT0astInstance, which contains a link to a php configuration file and also the respective T0AST instance
    # Unites all three dictionaries into one named PackedAgent
    try:
        tier0Configuration = loadTier0Configuration(tier0ConfigFile, replay)
        nodeId = list(tier0Configuration)[0]
        agentInfo = loadAgentInfo(key, cert, host, replay)[nodeId]
        configUrlAndT0ast = loadConfigUrlAndT0astInstance(nodeId)
        PackedAgent = {nodeId : {**tier0Configuration[nodeId], **agentInfo[nodeId], **configUrlAndT0ast}}
        return PackedAgent
    except IOError:
        print("Could not read nodeId:", nodeId)


def writeReport(allNodes, replay):
    outputFileProd="/afs/cern.ch/user/c/cmst0/www/tier0/nodeSummary_frontend/data.json"
    outputFileReplay="/afs/cern.ch/user/c/cmst0/www/tier0/nodeSummary_frontend/dataReplay.json"
    if replay:
            outputFile = outputFileReplay
    else:
            outputFile = outputFileProd
    data = allNodes
    with open(outputFile, 'w') as outfile:
            json.dump(data, outfile)

def main():
    """
    _main_

    Script's main function:
        fetch exceptions of failing t0 jobs.
    """
    try:
        subprocess.call(['./cpOfflineConfig.sh'])
        #os.chdir("/afs/cern/ch/work/c/cmst0/private")
        prodWmstats = "cmsweb.cern.ch"
        replayWmstats = "cmsweb-testbed.cern.ch"

        prodNodes = loadAgentInfo("/data/certs/serviceproxy-vocms001.pem", "/data/certs/serviceproxy-vocms001.pem", prodWmstats, False)
        replayNodes = loadAgentInfo("/data/certs/serviceproxy-vocms001.pem", "/data/certs/serviceproxy-vocms001.pem", replayWmstats, True)
        if not prodNodes:
            print("Exiting. No report written for production nodes.")
        else:
            writeReport(prodNodes, False)
        if not replayNodes:
            replayNodes = {}
            writeReport(replayNodes, True)
            print("Exiting. No report written for replay nodes.")
        else:
            writeReport(replayNodes, True)
    except Exception as msg:
        print(msg)
        sys.exit(1)
    
if __name__ == "__main__":
    sys.exit(main())








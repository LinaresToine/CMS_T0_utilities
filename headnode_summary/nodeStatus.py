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
import ssl
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

#kibanaUrl = extract_replay_link()
#print(kibanaUrl)

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

def loadCmswebInfo(key, cert, host):
    # All agent information about running jobs, sites, and other, are accessible via wmstats. This is done thro HTTPSConnection. 
    # The output is a dictionary named agentStatus
    # WMStatsAgentInfo is a dictionary with "rows", in which one row corresponds to all available agent information of one host node
    # WMStatsAgentInfo["rows"] is a list! Each index of the list contains the agent information in a particular machine
    # We define jobsByState = WMStatsAgentInfo["rows"][0]["value"]["WMBS_INFO"]["wmbsCountByState"] which is a dictionary with job states and their respective amounts 
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

    # We define activeRunJobs = WMStatsAgentInfo["rows"][0]["value"]["WMBS_INFO"]["activeRunJobByStatus"] which is a dictionary with the active job states and their respective amounts
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
    # We define componentsDown = WMStatsAgentInfo["rows"][0]["value"]["down_components"]
    # The dictionary agent is JobStates with componentsDown
    # We create another dictionary named agentNode with node ids as keys and each value will be the respective agent dictionary
    try:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=cert, keyfile=key)
        #connection = HTTPSConnection(host)
        connection = HTTPSConnection(host, context=ssl_context)
        urn = "/couchdb/tier0_wmstats/_design/WMStats/_view/agentInfo"
        params = {"stale": "update_after"}
        headers = {
                    "Content-type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": "agentInfoCollector"
                    }
        urn = "%s?%s" % (urn, urllib.parse.urlencode(params, doseq=True))
        connection.request("GET", urn, headers=headers) #key_file=key, cert_file=cert)
        response = connection.getresponse()
        WMStatsAgentInfo = json.loads(response.read()) # A list with dictionaries where each dictionary contains information of a node and its agent
        return WMStatsAgentInfo["rows"]
    except:
        errorMsg = "Error contacting CMSWEB WMStats\n"
        errorMsg += f"Response status: {response.status}\tResponse reason: {response.reason}\n"
        print(errorMsg)
        return []
    finally:
        connection.close()

def loadAgentInfo(WMStatsAgentInfoList, nodeId):
    NodeID = nodeId.split('.')[0]
    nodeInfo = next((nodeDictionary for nodeDictionary in WMStatsAgentInfoList if nodeDictionary.get('id') == nodeId), None) # This gets only the information relevant to one node and agent. It may be None if the agent is not in wmstats
    #print ('nodeInfo is {}'.format(nodeInfo))
    try:
        jobsByState = nodeInfo["value"]["WMBS_INFO"]["wmbsCountByState"] # Job status in WMBS
        activeRunJobs = nodeInfo["value"]["WMBS_INFO"]["activeRunJobByStatus"] # Job status in condor
        agent = {'status' : nodeInfo["value"]["status"],
                 'created' : jobsByState['created'],
                 'executing' : jobsByState['executing'],
                 'running' : activeRunJobs['Running'],
                 'idle' : activeRunJobs['Idle'],
                 'success' : jobsByState['success'],
                 'complete' : jobsByState['complete'],
                 'cleanout' : jobsByState['cleanout'],
                 'paused' : jobsByState['jobpaused'],
                 'components down' : nodeInfo["value"]["down_components"]
                }
    
        agentNode = {NodeID : agent}
    except:
        agentNode = {NodeID : {}}

    return agentNode


def loadTier0Configuration(tier0ConfigFile, nodeId, replay):
    # All relevant information of the agent configuration resides in the configuration file. There, an object of type Configuration() is created.
    # To access the configuration info, the loadConfigurationFile(configFile) is used to create the tier0Config object with the agent configuration.
    # A dictionary configuration = {} is created, where all the relevant attributes of tier0Config will be saved
    # This function returns the dictionary configuration  
    try:
        configuration = {}
        tier0Config = loadConfigurationFile(tier0ConfigFile)
        CMSSWVersion = tier0Config.Datasets.Default.CMSSWVersion['default']
        Scenario = tier0Config.Datasets.Default.Scenario
        AcquisitionEra = tier0Config.Global.AcquisitionEra

        if replay:
            Runs = tier0Config.Global.InjectRuns
            ProcessingVersion = tier0Config.Datasets.Default.ProcessingVersion
            configuration.update({'AcquisitionEra' : AcquisitionEra})
            configuration.update({'CMSSWVersion' : CMSSWVersion})
            configuration.update({'Runs' : Runs})
            configuration.update({'ProcessingVersion' : ProcessingVersion})
            configuration.update({'Scenario' : Scenario}) 
        else:
            RecoDelay = tier0Config.Datasets.Default.RecoDelay / 3600 
            ProcessingVersion = tier0Config.Datasets.Default.ProcessingVersion['default']
            MinRun = tier0Config.Global.InjectMinRun
            MaxRun = tier0Config.Global.InjectMaxRun
            configuration.update({'AcquisitionEra' : AcquisitionEra})
            configuration.update({'CMSSWVersion' : CMSSWVersion})
            configuration.update({'MinRun' : MinRun})
            configuration.update({'MaxRun' : MaxRun})
            configuration.update({'ProcessingVersion' : ProcessingVersion})
            configuration.update({'Scenario' : Scenario})
            configuration.update({'RecoDelay' : RecoDelay})
    
        NodeID = nodeId.split('.')[0] # removes the '.cern.ch' from nodeId
        nodeConfiguration = {NodeID : configuration}
        return nodeConfiguration
    
    except IOError:
        print("Could not read file:", tier0ConfigFile)

    return
 
def loadConfigUrlAndT0astInstance(nodeId):
    # This function returns a dictionary with the configuration file url and the T0AST instance relevant to a specific nodeId
    # This function is created to keep order of the tasks acomplished by the other load functions
    NodeID = nodeId.split('.')[0]
    nodeFileUrl = configurationFileUrl()
    nodeT0ast = instanceT0AST()
    nodeFileAndAST = {'nodeId' : NodeID,
                      'configFileUrl' : nodeFileUrl[NodeID],
                      'T0ast' : nodeT0ast[NodeID] 
                      }
    return nodeFileAndAST

def packedAgentDictionary(nodeId, tier0ConfigFile, key, cert, host, replay):
    # Gets dictionary returned by loadTier0Configuration, which contains relevant configuration information of the agent
    # Gets dictionary returned by loadAgentInfo, which contains info such as count of jobs by status, components down, node status
    # Gets dictionary from loadConfigUrlAndT0astInstance, which contains a link to a php configuration file and also the respective T0AST instance
    # Unites all three dictionaries into one named PackedAgent
    try:
        NodeID = nodeId.split('.')[0]
        tier0Configuration = loadTier0Configuration(tier0ConfigFile, nodeId, replay)
        print('t0 config is {}'.format(tier0Configuration))

        WMStatsAgentInfoList = loadCmswebInfo(key, cert, host)
        agentInfo = loadAgentInfo(WMStatsAgentInfoList, nodeId)
        print('agent info is {}'.format(agentInfo))

        configUrlAndT0ast = loadConfigUrlAndT0astInstance(nodeId)
        PackedAgent = {NodeID : {**tier0Configuration[NodeID], **agentInfo[NodeID], **configUrlAndT0ast}}
        # Finally we record the time in which the final dictionary was updated

        currentTime = time.strftime("%H:%M:%S")
        PackedAgent.update({'update time' : currentTime})
        
        print('agent is {}'.format(PackedAgent))
        print('\n')
        print('======================================================================================================================')
        print('\n')

        return PackedAgent
    except IOError:
        print("Could not read nodeId:", nodeId)


def writeReport(Node, nodeId, replay):
    # This function is used to create the json files with all the node information in it. It takes a dictionary named Node, a nodeId and if it corresponds to replay
    NodeID = nodeId.split('.')[0]
    outputFileProd="/afs/cern.ch/user/c/cmst0/Antonio/data_{}.json".format(NodeID)
    outputFileReplay="/afs/cern.ch/user/c/cmst0/Antonio/dataReplay_{}.json".format(NodeID)
    if replay:
            outputFile = outputFileReplay
    else:
            outputFile = outputFileProd
    data = Node
    with open(outputFile, 'w') as outfile:
            json.dump(data, outfile)

def main():
    """
    _main_

    Script's main function:
        fetch exceptions of failing t0 jobs.
    """
    tier0ConfigFileProd = "/data/tier0/admin/ProdOfflineConfiguration.py"
    tier0ConfigFileReplay = "/data/tier0/admin/ReplayOfflineConfiguration.py"
    nodeId = subprocess.check_output('hostname', universal_newlines=True).strip() # Gets the vocms node id
    prodWmstats = "cmsweb.cern.ch"
    replayWmstats = "cmsweb-testbed.cern.ch"
    key = "/data/certs/serviceproxy-vocms001.pem"
    cert = "/data/certs/serviceproxy-vocms001.pem"

    try:

        prodNode = packedAgentDictionary(nodeId, tier0ConfigFileProd, key, cert, prodWmstats, False)
        replayNode = packedAgentDictionary(nodeId, tier0ConfigFileReplay, key, cert, replayWmstats, True)
        if not prodNode:
            print("Exiting. No report written for production nodes.")
        else:
            writeReport(prodNode, nodeId, False)
        if not replayNode:
            replayNode = {}
            writeReport(replayNode, nodeId, True)
            print("Exiting. No report written for replay nodes.")
        else:
            writeReport(replayNode, nodeId, True)
    except Exception as msg:
        print(msg)
        sys.exit(1)
    
if __name__ == "__main__":
    sys.exit(main())








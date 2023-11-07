#! /usr/bin/env python

import sys
import OfflineConfiguration
import os
import json
import time
from datetime import datetime
import socket
import logging
import urllib
from logging.handlers import RotatingFileHandler
from argparse import ArgumentParser
import pprint
from pprint import pformat
from httplib import HTTPSConnection
import subprocess
from string import Template
import re



def load_data_from_cmsweb(key, cert, host, replay):
    con = HTTPSConnection(host,
                          cert_file=cert,
                          key_file=key)
    urn = "/couchdb/tier0_wmstats/_design/WMStats/_view/agentInfo"
    params = {"stale": "update_after"}
    headers = {
                "Content-type": "application/json",
                "Accept": "application/json",
                "User-Agent": "agentInfoCollector"
                }
    

    try:
        urn = "%s?%s" % (urn, urllib.urlencode(params, doseq=True))
        #print(urn)
        con.request("GET", urn, headers=headers)
        resp = con.getresponse()
        #print(resp.status)
        if resp.status != 200:
            errorMsg = "Error contacting CMSWEB WMStats\n"
            errorMsg += "Response status: %s\tResponse reason: %s\n" % (resp.status, resp.reason)
            print(errorMsg)
            raise Exception(errorMsg)

        #print(resp.read())
        jsonObject = json.loads(resp.read())
        #pprint.pprint(jsonObject)
        productionNodes = {}
        currentTime = time.strftime("%H:%M:%S")
        #print(jsonObject["rows"])
        for singleRow in jsonObject["rows"]:
            #singleRow = jsonObject["rows"][i]
            #print(singleRow)
            tempdict = {}
            nodeId = singleRow["id"].split(".")[0]
            nodeStatus = singleRow["value"]["status"]
            #print(nodeStatus)
            #if not singleRow["value"]["WMBS_INFO"]["wmbsCountByState"] or "jobpaused" not in singleRow["value"]["WMBS_INFO"]["wmbsCountByState"]:
            #    pausedJobs = 0
            #else:
            #    pausedJobs = singleRow["value"]["WMBS_INFO"]["wmbsCountByState"]["jobpaused"]
            parsed = getRunIntervals(nodeId, replay)
            #print(parsed)
            if singleRow["value"]["WMBS_INFO"]["wmbsCountByState"]:
                #print(singleRow["value"]["WMBS_INFO"]["wmbsCountByState"])
                parsed.update(singleRow["value"]["WMBS_INFO"]["wmbsCountByState"])
                #print("parse 1")
                #print(parsed)
            if singleRow["value"]["WMBS_INFO"]["activeRunJobByStatus"]:
                #print(singleRow["value"]["WMBS_INFO"]["activeRunJobByStatus"])
                parsed.update(singleRow["value"]["WMBS_INFO"]["activeRunJobByStatus"])
                #print(parsed)
            #print(pausedJobs)
            componentsDown = singleRow["value"]["down_components"]
            #print(componentsDown)
            # if there are down components, we need a notification
            #if len(componentsDown) > 0 and not replay:
            #    print("There are down components")
                #parseComponentErrors(nodeId, singleRow["value"])
            #print(componentsDown)
            #parsed = getRunIntervals(nodeId, replay)
            if replay:
                conf = replayConfigUrl
                if nodeId in kibanaUrl:
                    #print(nodeId)
                    parsed.update({"monitoringUrl": kibanaUrl[nodeId]})
            else:
                conf = configUrl
            parsed.update({ "nodeStatus": nodeStatus, "downComponents": componentsDown, "updateTime": currentTime})
            if nodeId in conf:
                parsed.update({ "configurationFile": conf[nodeId] })
            else:
                print("no configuration file found for %s", nodeId)
            if nodeId in t0astInst:
                parsed.update({ "t0astInst": t0astInst[nodeId] })
            #print(parsed)
            productionNodes.update({nodeId: parsed})

        #print(productionNodes)
        return productionNodes
    except Exception as msg:
        message = 'Error: %s' % str(msg)
        print(message)
        return None
    finally:
        con.close()

def nodeConfiguration(nodeId, replay):
    fullPath = "/data/tier0/admin/"
    containerPath = "/data/tier0/docker/container1/admin/"
    containerNode = "vocms047"
    replayConfig = "ReplayOfflineConfiguration.py"
    prodConfig = "ProdOfflineConfiguration.py"
    fullPastePath = "/afs/cern.ch/work/c/cmst0/public/ProductionConfigurationOfflineFiles/"
    wmagentPath="/data/tier0/srv/wmagent/"

    #try:
    #    if replay:
    #        srcFileName = fullPath + replayConfig
    #        destFileName = fullPastePath+nodeId+replayConfig
    #        if nodeId[0] == u'C':
    #            srcFileName = containerPath + replayConfig
    #            nodeId = containerNode
    #    else:
    #        srcFileName = fullPath + prodConfig
    #        destFileName = fullPastePath+nodeId+prodConfig
    #    subprocess.check_call(["ssh", nodeId, "cp", srcFileName, destFileName])
        #subprocess.check_call(["ssh", nodeId, "sudo", "-u", "cmst1", "/bin/bash;", "cat", "/data/tier0/srv/wmagent/current/config/tier0/config.py"])
    #    parsed = parseConfigFile(destFileName, replay)
    #    t0Path=subprocess.check_output(['ssh',nodeId,'ls','-l',wmagentPath+"current"])
    #    t0Version=t0Path.strip().split("-> ")[-1]
    #    parsed.update({"tier0Version": t0Version})
    #    return parsed
    #except Exception as msg:
    #    print("getRunIntervals")
    #    print(nodeId)
    #    print(str(msg))
    #    return None

def parseConfigFile(replay):
    parsed = {}
    #print(fileName +" "+ str(replay))
    MinRun = OfflineConfiguration.ProdOfflineConfiguration.getMinRun
    MaxRun = OfflineConfiguration.ProdOfflineConfiguration.getMaxRun
    AcquisitionEra = OfflineConfiguration.ProdOfflineConfiguration.getAcquisitionEra
    defaultCMSSWVersion = OfflineConfiguration.ProdOfflineConfiguration.getDefaultCMSSWVersion
    ppScenario = OfflineConfiguration.ProdOfflineConfiguration.getppScenario
    
    parsed.update({"setInjectMinRun": MinRun})
    parsed.update({"setInjectMaxRun": MaxRun})
    parsed.update({"setAcquisitionEra" : AcquisitionEra})
    parsed.update({"defaultCMSSWVersion" : defaultCMSSWVersion})
    parsed.update({"ppScenario" : ppScenario})

    #try:
        #with open(fileName) as f:
            #for line in f:
                #if not replay and line.startswith("setInjectMinRun"):
                    #minRun=line.strip().split(",")[-1][:-1][1:]
                    #if not minRun:
                    #    minRun = None
                    #parsed.update({"setInjectMinRun": minRun})
                    #print(minRun)
                #if not replay and line.startswith("setInjectMaxRun"):
                    #maxRun=line.strip().split(",")[-1][:-1][1:]
                    #if not maxRun:
                    #    maxRun = None
                    #parsed.update({"setInjectMaxRun": maxRun})
                    #print(maxRun)
                #if not replay and line.startswith("defaultRecoTimeout"):
                #    recoDelay=line.strip().split("=")[-1]
                    #print(recoDelay)
                #    recoDelay = eval(recoDelay) / 3600
                    #if not recoDelay:
                    #    recoDelay = ""
                    #print("Reco delay is: "+str(recoDelay))
                #    parsed.update({"PromptRecoDelay": recoDelay})
                #if "CMSSW" in line and "'default'" in line and not 'defaultCMSSWVersion' in line:
                #    cmssw = line.strip().split(":")[-1].strip("\"")[2:]
                #    parsed.update({"cmsswVersion": cmssw})
                    #print(cmssw)
                #if line.startswith("ppScenario "):
                #    ppScenario = line.strip().split("=")[-1].strip("\"")[2:]
                #    parsed.update({"processingScenario": ppScenario})
                    #print(ppScenario)
                #if  replay and line.startswith("setInjectRuns"):
                    #print(line.strip())
                #    if replay:
                #        injectedRuns = re.search('%s(.*)%s' % ('\[', '\]'), line.strip()).group(1)
                #    else:
                #        injectedRuns = re.search('%s(.*)%s' % ('\[', ' '), line.strip()).group(1)
                    #print(injectedRuns)
                #    parsed.update({"injectedRuns": injectedRuns})
        #print("Parsed contents of" + fileName)
        #print(parsed)
        #return parsed

    #except IOError:
    #    print("Could not read file:", fileName)

    return parsed

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
        prodNodes = load_data_from_cmsweb("/data/certs/serviceproxy-vocms001.pem", "/data/certs/serviceproxy-vocms001.pem", prodWmstats, False)
        replayNodes = load_data_from_cmsweb("/data/certs/serviceproxy-vocms001.pem", "/data/certs/serviceproxy-vocms001.pem", replayWmstats, True)
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
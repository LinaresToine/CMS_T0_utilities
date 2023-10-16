#! /usr/bin/env python

import sys
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

configUrl = {
    "vocms013": "http://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_013.php",
    "vocms014": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_014.php",
    "vocms0313": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_0313.php",
    "vocms0314": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ProdOfflineConfiguration_0314.php"
}

replayConfigUrl = {
    #"vocms015": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_015.php",
    "vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_047.php",
    "C1_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C1.php",
    "C2_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C2.php",
    "C3_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C3.php",
    "C4_vocms047": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_C4.php",
    "vocms0500": "https://cmst0.web.cern.ch/CMST0/tier0/offline_config/ReplayOfflineConfiguration_0500.php"
}

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

t0astInst = {
    "vocms013": "CMS_T0AST_4",
    "vocms014": "CMS_T0AST_3",
    "vocms0313": "CMS_T0AST_2",
    "vocms0314": "CMS_T0AST_1",
    "C1_vocms047": "CMS_T0AST_REPLAY1",
    "C2_vocms047": "CMS_T0AST_REPLAY2",
    "C3_vocms047": "CMS_T0AST_REPLAY3",
    "C4_vocms047": "CMS_T0AST_REPLAY4",
    #"vocms015": "CMS_T0AST_REPLAY4",
    "vocms047": "CMS_T0AST_REPLAY3",
    "vocms0500": "CMS_T0AST_REPLAY2"
}

prodWmstats = "cmsweb.cern.ch"
replayWmstats = "cmsweb-testbed.cern.ch"


### Setting up mail service ###
pp = pprint.PrettyPrinter()

def sendMail(recipient, subject, body):
    try:
        process = subprocess.Popen(['/usr/bin/Mail', '-s', subject, recipient], stdin=subprocess.PIPE)
        print("Sending an email")
    except:
        print ("Couldn't send mail")
    process.communicate(body)


#mail_address = "cms-tier0-monitoring-alerts@cern.ch"
#mailAdress = "vytautas.jankauskas@cern.ch"
mailAdress = "cms-tier0-operations@cern.ch"
mailSubject = "T0 components down"

def parseComponentErrors(nodeId, errorDetails):
    mailBody = ""
    # check the time:
    #print(nodeId)
    if "down_component_detail" in errorDetails:
        mailBody += "Node name: " + nodeId + "\n"
        #print(errorDetails["down_component_detail"])
        for singleComponent in errorDetails["down_component_detail"]:
            #print(singleComponent)
            # 30 min delay:
            timeDelay = int(time.time()) - 30*60
            mailBody += "Component name: " + singleComponent + "\n"
            #print(mailBody)
            if "last_error" in singleComponent:
                if singleComponent["last_error"] < timeDelay:
                    mailBody += "Last error time: " + datetime.fromtimestamp(singleComponent["last_error"]).strftime("%A, %B %d, %Y %I:%M:%S") + "\n"
                    if "error_message" in singleComponent:
                        mailBody += "Error message: " + singleComponent["error_message"] + "\n"
            #print(mailBody)
        with open('/afs/cern.ch/work/c/cmst0/private/scripts/nodeStatus/emailCompareBody.txt', 'w') as filea:
            for line in mailBody:
                filea.write(line)
            # only send email if any details have changed:
        with open('/afs/cern.ch/work/c/cmst0/private/scripts/nodeStatus/emailBody.txt', 'r') as file1:
            with open('emailCompareBody.txt', 'r') as file2:
                same = set(file2).difference(file1)
        same.discard("\n")
        #print(same)
        if len(same) > 0:
            sendMail(mailAdress, mailSubject, mailBody)
            with open('/afs/cern.ch/work/c/cmst0/private/scripts/nodeStatus/emailBody.txt', 'w') as file_out:
                for line in mailBody:
                    file_out.write(line)
        else:
            print("The email was supposed to be sent already.")

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

def getRunIntervals(productionNode, replay):
    fullPath = "/data/tier0/admin/"
    containerPath = "/data/tier0/docker/container1/admin/"
    containerNode = "vocms047"
    replayConfig = "ReplayOfflineConfiguration.py"
    prodConfig = "ProdOfflineConfiguration.py"
    fullPastePath = "/afs/cern.ch/work/c/cmst0/public/ProductionConfigurationOfflineFiles/"
    wmagentPath="/data/tier0/srv/wmagent/"

    try:
        if replay:
            srcFileName = fullPath + replayConfig
            destFileName = fullPastePath+productionNode+replayConfig
            if productionNode[0] == u'C':
                srcFileName = containerPath + replayConfig
                productionNode = containerNode
        else:
            srcFileName = fullPath + prodConfig
            destFileName = fullPastePath+productionNode+prodConfig
        subprocess.check_call(["ssh", productionNode, "cp", srcFileName, destFileName])
        #subprocess.check_call(["ssh", productionNode, "sudo", "-u", "cmst1", "/bin/bash;", "cat", "/data/tier0/srv/wmagent/current/config/tier0/config.py"])
        minMaxRuns = parseConfigFile(destFileName, replay)
        t0Path=subprocess.check_output(['ssh',productionNode,'ls','-l',wmagentPath+"current"])
        t0Version=t0Path.strip().split("-> ")[-1]
        minMaxRuns.update({"tier0Version": t0Version})
        #print(minMaxRuns)
        return minMaxRuns
    except Exception as msg:
        print("getRunIntervals")
        print(productionNode)
        print(str(msg))
        return None

def parseConfigFile(fileName, replay):
    parsed = {}
    #print(fileName +" "+ str(replay))
    try:
        with open(fileName) as f:
            for line in f:
                if not replay and line.startswith("setInjectMinRun"):
                    minRun=line.strip().split(",")[-1][:-1][1:]
                    if not minRun:
                        minRun = None
                    parsed.update({"setInjectMinRun": minRun})
                    #print(minRun)
                if not replay and line.startswith("setInjectMaxRun"):
                    maxRun=line.strip().split(",")[-1][:-1][1:]
                    if not maxRun:
                        maxRun = None
                    parsed.update({"setInjectMaxRun": maxRun})
                    #print(maxRun)
                if not replay and line.startswith("defaultRecoTimeout"):
                    recoDelay=line.strip().split("=")[-1]
                    #print(recoDelay)
                    recoDelay = eval(recoDelay) / 3600
                    #if not recoDelay:
                    #    recoDelay = ""
                    #print("Reco delay is: "+str(recoDelay))
                    parsed.update({"PromptRecoDelay": recoDelay})
                if "CMSSW" in line and "'default'" in line and not 'defaultCMSSWVersion' in line:
                    cmssw = line.strip().split(":")[-1].strip("\"")[2:]
                    parsed.update({"cmsswVersion": cmssw})
                    #print(cmssw)
                if line.startswith("ppScenario "):
                    ppScenario = line.strip().split("=")[-1].strip("\"")[2:]
                    parsed.update({"processingScenario": ppScenario})
                    #print(ppScenario)
                if  replay and line.startswith("setInjectRuns"):
                    #print(line.strip())
                    if replay:
                        injectedRuns = re.search('%s(.*)%s' % ('\[', '\]'), line.strip()).group(1)
                    else:
                        injectedRuns = re.search('%s(.*)%s' % ('\[', ' '), line.strip()).group(1)
                    #print(injectedRuns)
                    parsed.update({"injectedRuns": injectedRuns})
        #print("Parsed contents of" + fileName)
        #print(parsed)
        return parsed

    except IOError:
        print("Could not read file:", fileName)

    return

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








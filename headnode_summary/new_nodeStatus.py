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

from WMCore.Configuration import loadConfigurationFile

def loadConfiguration():
    tier0Config = loadConfigurationFile("/data/tier0/admin/HIProdOfflineConfiguration.py")
    CMSSWVersion = tier0Config.Datasets.Default.CMSSWVersion['default']
    ProcessingVersion = tier0Config.Datasets.Default.ProcessingVersion['default']
    Scenario = tier0Config.Datasets.Default.Scenario
    RecoDelay = tier0Config.Datasets.Default.RecoDelay / 3600 
    AcquisitionEra = tier0Config.Global.AcquisitionEra
    MinRun = tier0Config.Global.InjectMinRun
    MaxRun = tier0Config.Global.InjectMaxRun
    configuration = {}
    configuration.update({'AcquisitionEra' : AcquisitionEra})
    configuration.update({'CMSSWVersion' : CMSSWVersion})
    configuration.update({'MinRun' : MinRun})
    configuration.update({'MaxRun' : MaxRun})
    configuration.update({'ProcessingVersion' : ProcessingVersion})
    configuration.update({'Scenario' : Scenario})
    configuration.update({'RecoDelay' : RecoDelay})
    





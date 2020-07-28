__author__="Rohan Kilje"
__version__="1.0"

import sys, os, time, argparse, json, datetime
from subprocess import call, Popen, list2cmdline, STDOUT
from tempfile import TemporaryFile
from concurrent.futures import ProcessPoolExecutor
import pymysql, re, json
import xml.etree.ElementTree as ET 

parser = argparse.ArgumentParser()
parser.add_argument("-env","--environment",choices=['LOCAL','BROWSERSTACK'],help="sELECT eNVIRONMENT TO RUN THE FILES")
args = parser.parse_args()
global timestamp, rootdir
suiteList= ['suiteName','suiteName2']

dbhost = ''
dbUser = ''
dbPassword = ''
db = ''


def getConnection():
    return True


def closeConnection():
    if connection:
        connection.close()
    print('************Connection is Closed**********')

def main(values):
    with ProcessPoolExecutor(max_workers=8) as executor:
        results = executor.map(runCommand,values)
        for result in results:
            print(result)

def folder_timestamp():
    print("temp TODO result")

def converttostr(input_seq, separator):
    #Join all strings in the list
    finar_str = separator.join(input_seq)
    return final_str

#--------------------------Running Scripts-----------------------------
def runCommand(cmd):
    print("In process ", os.getpid(), "Running command >>", cmd)
    call(cmd, shell=True)
    return 'SUCCESS'

def createCmd(suite):
    reportFile = suite +"_report.html"
    logFile = suite + "_log.html"
    outXml = suite + ".xml"
    print(outDir)
    command = "robot -d ." + outDir + " -l " + logFile + " -r " + reportFile 
    return command

if __name__=='__main__':

    if(args.timestamp=='current'):
        ts= time.time()
        print(ts)
        rootdir = os.cwd()

    outDir = '/Results'
    if not os.path.exists(rootdir+outDir):
        try:
            os.mkdir(rootdir+outDir)
            print("Directory created...")
        except:
            print("Exception occurred creating new directory")
    else:
        print("Output directory already exists ")
    cmdList = [createCmd(suitename) for suitename in suiteList]
    main(cmdList)

    outDir='/Results'
    reportFile = "First_Report.html"
    logFile = "First_Log.html"
    outXml = "Final.xml"
    print("Now merging the outputs")
    outputList = [('.' + outDir + '/' + suitename + '.xml') for suitename in suiteList]
    outputs = converttostr(outputList, ' ')
    rebotCommand = "rebot -d ." + outputList + " --merge ." + outDir + "/*.xml"
    print("Rebot command is printed >>" +  rebotCommand)
    call(rebotCommand, shell=True)

#re-Run failed scenario
    reRunFailedCommand = "robot --rerunfailed ." + outDir #TODO
    call(reRunFailedCommand ,shell=True)

    #------------final Report with the RE Run Result
    print("Now merging the outputs")
    call("rebot --merge --name Final -d ." + outDir + " --output FinalOut.xml")

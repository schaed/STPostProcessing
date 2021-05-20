#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import HInvPlot.systematics
import pickle
from HInvPlot.buildCondorScript import *

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-n", "--nominal", dest = "nominal", action="store_true", default = False, help = "Do nominal only" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
parser.add_argument( "-i", "--inputFile",  type = str, dest = "inputFile", default = "v26.txt", help = "path for input files")
parser.add_argument('-r', '--rfile', type=str, default='out_"$1".root', dest='rfile', help='output ROOT file')
parser.add_argument( "--noSubmit", dest = "noSubmit", action="store_true", default = False, help = "Dont submit jobs" )
parser.add_argument( "--TheorySystWeight", dest = "TheorySystWeight", action="store_true", default = False, help = "Run the theory weights" )
parser.add_argument( "--nSystPerJob", dest = "nSystPerJob", type=int, default = 1, help = "Number of syst per job, -1 runs all syst in 1 job" )
parser.add_argument( "--ph-ana", dest = "ph_ana", action="store_true", default = False, help = "Photon analysis to setup the right systematic uncertainties" )
parser.add_argument("--extraCommand", dest='extraCommand', default="", help="extraCommand, string of possible commands to give plotEvent.py, something like --r207Ana or --DetailLvl 10")
args, unknown = parser.parse_known_args()

### Load systematics list from HInvPlot/python/systematics.py ###
if args.nominal:
    sys = HInvPlot.systematics.systematics("Nominal")
    asys_systlist = []
    wsys_systlist = []
else:
    sys =  HInvPlot.systematics.systematics("All", args.ph_ana)
    asys = HInvPlot.systematics.systematics("OneSided", args.ph_ana)
    wsys = HInvPlot.systematics.systematics("WeightSyst", args.ph_ana)
    asys_systlist = asys.getsystematicsList()
    wsys_systlist = wsys.getsystematicsList()

systlist=[]
systlistToRun = sys.getsystematicsList()
if args.nSystPerJob==1:
    systlist=systlistToRun
elif args.nSystPerJob==-1:
    systlist=['All']
else:
    systName=''
    args.rfile = 'out_"$2".root'
    for isyst in range(0,len(systlistToRun)):
        systName+=systlistToRun[isyst]+','
        if (isyst!=0 and (isyst%args.nSystPerJob==0)) or isyst==(len(systlistToRun)-1):
            systlist+=[systName.rstrip(',')]
            systName =''
print systlist

### Remake submitDir ###
workDir = os.getcwd()+"/"+args.submitDir
bDir= os.getenv('ROOTCOREDIR')
#buildDir = workDir[:bDir.find("/Plotting")]
buildDir = bDir[:bDir.find("/Plotting")]
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)
#os.system("chmod uog+w "+workDir)

listofsysts = workDir+"/systlist"
f = open(listofsysts, 'w')
isy=0
if args.nominal and args.TheorySystWeight:
    args.rfile = 'out_Nominal"$2".root'
    for line in systlist:
        f.write('%s 0\n' %(line)) # writing out the file with the position number
        #for r in range(11,113):
        for r in range(115,148):
            f.write('%s %s\n' %(line,r)) # writing out the file with the position number
            isy+=1 # not used here
else:
    for line in systlist:
        f.write('%s %s\n' %(line,isy))
        isy+=1
f.close()

extraCommand=' '
if args.extraCommand:
    extraCommand=' '+args.extraCommand+' '
TESTAREA=buildDir+'/Plotting'
print 'TESTAREA:',TESTAREA

theoryWeights=''
if args.nominal and args.TheorySystWeight:
    theoryWeights=' --TheorySystWeight $2 '
        
runCommand = '''python '''+TESTAREA+'''/HInvPlot/macros/plotEvent.py --syst "$1"  -r ''' + args.rfile + ''' -i ''' + args.inputFile+extraCommand+theoryWeights
print runCommand
writeCondorShell(workDir, buildDir, '', runCommand, "PlotEventCondorSub")
writeCondorSub(workDir, '', "PlotEventCondorSub", listofsysts)


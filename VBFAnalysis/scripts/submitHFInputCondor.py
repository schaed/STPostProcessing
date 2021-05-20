#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import VBFAnalysis.sample
import VBFAnalysis.systematics
import pickle
from VBFAnalysis.buildCondorScript import *
from VBFAnalysis.writeMultiJEleFake import *

parser = argparse.ArgumentParser( description = "Looping over sys and samples for HF Input Alg", add_help=True , fromfile_prefix_chars='@')

parser.add_argument( "-n", "--nominal", dest = "nominal", action="store_true", default = False, help = "Do nominal only" )
parser.add_argument( "--slc7", dest = "slc7", action="store_true", default = False, help = "Do slc7 for chicago tier3" )
parser.add_argument( "--metOptSyst", dest = "metOptSyst", action="store_true", default = False, help = "Do only the met optimization systematics" )
parser.add_argument( "-d", "--submitDir",  type = str, dest = "submitDir", default = "submitDir", help = "dir in run where all the output goes to")
parser.add_argument( "-i", "--inputDir",  type = str, dest = "inputDir", default = "/eos/user/r/rzou/v04/microtuples/", help = "dir for input file")
parser.add_argument( "--noSubmit", dest = "noSubmit", action="store_true", default = False, help = "Dont submit jobs" )
parser.add_argument( "--isOneCRBin", dest = "isOneCRBin", action="store_true", default = False, help = "One CR bin" )
parser.add_argument("--extraVars", dest='extraVars', default="7", help="extraVars, 1=cut on the new variables for leptons veto, 2=loosen cuts, 3=no soft met cut default: 7, 5=met OR lep trig CR, 6=met trig CR, 7=corrected SF for v31")
parser.add_argument("--Binning", dest='Binning', default="11", help="Binning, 11=default, 0=Mjj binning, 1=low MET bin, 2=njet>2 binning, 3=met binning, 4=3bins for nj>2, 5=3dphibin, 6= dphi by mjj+nj>2, 7=800mjj withdphi, 8=mjj 8bins, 30=5mjj bins for high mjj")
parser.add_argument( "--isMadgraph", dest = "isMadgraph", action="store_true", default = False, help = "Use the madgraph samples" )
parser.add_argument( "--mergeKTPTV", dest = "mergeKTPTV", action="store_true", default = False, help = "Use the kt filtered sherpa samples" )
parser.add_argument( "--doTMVA", dest = "doTMVA", action="store_true", default = False, help = "Use the variable filled as tmva for the fitting" )
parser.add_argument( "--doDoubleRatio", dest = "doDoubleRatio", action="store_true", default = False, help = "Use this variable to run the double ratio inputs")
parser.add_argument( "--doPlot", dest = "doPlot", action="store_true", default = False, help = "Generate additional histograms for postfit plots")
parser.add_argument( "--doFJVTCR", dest = "doFJVTCR", action="store_true", default = False, help = "Generate MJ for fjvt CR")
parser.add_argument( "--v26Ntuples", dest = "v26Ntuples", action="store_true", default = False, help = "Run version 26 style ntuples. important for lepton selection")
parser.add_argument( "--noVjMjjWeight", dest = "noVjMjjWeight", action="store_true", default = False, help = "Removes the mjj reweighting if requested")
parser.add_argument( "--isv41older", dest = "isv41older", action="store_true", default = False, help = "Run version 41 or older style ntuples. important for photon overlap")
parser.add_argument( "--doVBFMETGam", dest = "doVBFMETGam", action="store_true", default = False, help = "VBF + MET + photon analysis, set --Binning=13")
parser.add_argument( "--doVjetMjjRW", dest = "doVjetMjjRW", action="store_true", default = False, help = "VBF + MET apply mjj reweighting")
parser.add_argument( "--doMTFit", dest = "doMTFit", action="store_true", default = False, help = "VBF + MET + photon analysis with an mt fit, set --Binning=13 or 14 for split mjj")
parser.add_argument( "--doLooseCR", dest = "doLooseCR", action="store_true", default = False, help = "VBF + MET + photon analysis do loose CR, set --Binning=13")
parser.add_argument( "--doCentralCR", dest = "doCentralCR", action="store_true", default = False, help = "VBF + MET + photon analysis do centrality Z CR, set --Binning=13")
parser.add_argument( "--doLooseWCR", dest = "doLooseWCR", action="store_true", default = False, help = "VBF + MET + photon analysis do loose WCR, set --Binning=13")
parser.add_argument( "--rmDPhiMETPh", dest = "rmDPhiMETPh", action="store_true", default = False, help = "VBF + MET + photon analysis remove dphi(MET,ph), set --Binning=13")
parser.add_argument( "--doOneHighFJVTCR", dest = "doOneHighFJVTCR", action="store_true", default = False, help = "VBF + MET to be used with option 22. has one fjvt cr for high dphijj")
parser.add_argument( "--doHighDphijj", dest = "doHighDphijj", action="store_true", default = False, help = "Fit dphijj>2.5 analysis with no dphijj binning, set --Binning=23 or 30")
parser.add_argument( "--singleHist", dest = "singleHist", action="store_true", default = False, help = "Runs VBF + MET in one histogram when true")
parser.add_argument("--year", type=int, dest='year', default=2016, help="year, default: 2016 - 2017 or 2018 for those years")
parser.add_argument("--METCut", type=int, dest='METCut', default=200e3, help="METCut, default: 200e3 MeV")
parser.add_argument("--METDef", dest='METDef', default='0', help="met definition, default: 0=loose, 1=tenacious")
args, unknown = parser.parse_known_args()

# set the binning for dphijj>2.0
if args.doHighDphijj:
    args.Binning="30"

if not args.doVBFMETGam:
    myMetCut=int(args.METCut/1e3)

    if int(args.Binning)==22:
        if myMetCut!=160:
            print 'you are gonna have a bad time. Only setup for MET>160 for these binning options'
            sys.exit(0)

        myMetCut=200 # only setup for this value now for the fakes and mj. this is only for python
    if not args.doFJVTCR:
        writeMultiJet(int(args.Binning), args.year, doDoubleRatio=args.doDoubleRatio, METCut=myMetCut, singleHist=args.singleHist, doTMVA=args.doTMVA, doHighDphijj=args.doHighDphijj)
    else:
        writeMultiJetFJVT(int(args.Binning), args.year, doDoubleRatio=args.doDoubleRatio, METCut=myMetCut, singleHist=args.singleHist, doTMVA=args.doTMVA, doOneHighFJVTCR=args.doOneHighFJVTCR)
    writeFakeEle(int(args.Binning), args.year, doDoubleRatio=args.doDoubleRatio, singleHist=args.singleHist,METCut=myMetCut)
    writeFakeMuo(int(args.Binning), args.year, METCut=myMetCut)
else:
    myMetCut=int(args.METCut/1e3)
    writeFakeEleGam(Binning=int(args.Binning), year=args.year, METCut=myMetCut, doTMVA=args.doTMVA, doMTFit=args.doMTFit, isOneCRBin=args.isOneCRBin)# args.doVBFMETGam) # set to VBFMETgam because we assume one CR
    writeSinglePhoton(Binning=int(args.Binning), year=args.year, METCut=myMetCut, doTMVA=args.doTMVA, doMTFit=args.doMTFit)

### Load systematics list from VBFAnalysis/python/systematics.py ###
if args.nominal:
    sys = VBFAnalysis.systematics.systematics("Nominal",args.doVBFMETGam, args.doVjetMjjRW)
    asys_systlist = []
    wsys_systlist = []
elif args.metOptSyst:
    sys = VBFAnalysis.systematics.systematics("METSystOpt",args.doVBFMETGam, args.doVjetMjjRW)
    asys = VBFAnalysis.systematics.systematics("OneSided",args.doVBFMETGam, args.doVjetMjjRW)
    wsys = VBFAnalysis.systematics.systematics("WeightSyst",args.doVBFMETGam, args.doVjetMjjRW)
    asys_systlist = asys.getsystematicsList()
    wsys_systlist = wsys.getsystematicsList()
else:
    sys = VBFAnalysis.systematics.systematics("All",args.doVBFMETGam, args.doVjetMjjRW)
    asys = VBFAnalysis.systematics.systematics("OneSided",args.doVBFMETGam, args.doVjetMjjRW)
    wsys = VBFAnalysis.systematics.systematics("WeightSyst",args.doVBFMETGam, args.doVjetMjjRW)
    asys_systlist = asys.getsystematicsList()
    wsys_systlist = wsys.getsystematicsList()

systlist = sys.getsystematicsList()
print systlist

### Remake submitDir ###
workDir = os.getcwd()+"/"+args.submitDir
#buildDir = workDir[:workDir.find("/run/")]+"/build"
CMTCONFIG = os.getenv('CMTCONFIG')
buildPaths = os.getenv('CMAKE_PREFIX_PATH')
buildPathsVec = buildPaths.split(':')
buildDir =  buildPathsVec[0][:buildPathsVec[0].find(CMTCONFIG)].rstrip('/')
os.system("rm -rf "+workDir)
os.system("mkdir "+workDir)

listoffiles = workDir+"/filelist"
listoffilesMC = workDir+"/filelistMC"
listoffilesVBFMC = workDir+"/filelistVBFMC"
listoffilesGGFMC = workDir+"/filelistGGFMC"
listoffilesGGFVBFMC = workDir+"/filelistGGFVBFMC"
listoffilesZstrongMC = workDir+"/filelistZstrongMC"
listoffilesWstrongMC = workDir+"/filelistWstrongMC"
listoffilesWewkMC = workDir+"/filelistWewkMC"
listoffilesZewkMC = workDir+"/filelistZewkMC"
f = open(listoffiles, 'w')
fMC = open(listoffilesMC, 'w')
fVBFMC = open(listoffilesVBFMC, 'w')
fGGFMC = open(listoffilesGGFMC, 'w')
fGGFVBFMC = open(listoffilesGGFVBFMC, 'w')
fZstrongMC = open(listoffilesZstrongMC, 'w')
fWstrongMC = open(listoffilesWstrongMC, 'w')
fWewkMC = open(listoffilesWewkMC, 'w')
fZewkMC = open(listoffilesZewkMC, 'w')
samplePatternGlobal = ""
p = subprocess.Popen("ls "+args.inputDir+"*root*", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    filepath = line.strip()
    f.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] != "data"):
        fMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "VBFH"):
        fVBFMC.write(filepath+"\n")
        fGGFVBFMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "ggFH"):
        fGGFMC.write(filepath+"\n")
        fGGFVBFMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "Z_st"):
        fZstrongMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "Z_EW"):
        fZewkMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "W_st"):
        fWstrongMC.write(filepath+"\n")
    if (filepath.split("/")[-1][:4] == "W_EW"):
        fWewkMC.write(filepath+"\n")
f.close()
fMC.close()
fVBFMC.close()
fGGFMC.close()
fGGFVBFMC.close()
fZstrongMC.close()
fWstrongMC.close()
fZewkMC.close()
fWewkMC.close()

extraCommand=''
if args.extraVars:
    extraCommand=' --extraVars '+args.extraVars
if args.isMadgraph:
    extraCommand+=' --isMadgraph '
if args.isOneCRBin:
    extraCommand+=' --isOneCRBin '
if args.mergeKTPTV:
    extraCommand+=' --mergeKTPTV '
if args.METDef!="0":
    extraCommand+=' --METDef '+args.METDef+' '
if args.year!=2016:
    extraCommand+=' --year %s ' %(args.year)
if args.METCut!=100e3:
    extraCommand+=' --METCut %i ' %(args.METCut)
if args.doTMVA:
    extraCommand+=' --doTMVA '
if args.doDoubleRatio:
    extraCommand+=' --doDoubleRatio '
if args.v26Ntuples:
    extraCommand+=' --v26Ntuples '
if args.noVjMjjWeight:
    extraCommand+=' --noVjMjjWeight '
if args.isv41older:
    extraCommand+=' --isv41older '
if args.singleHist:
    extraCommand+=' --singleHist '
if args.doVBFMETGam:
    extraCommand+=' --doVBFMETGam ' #--isOneCRBin '
if args.doHighDphijj:
    extraCommand+=' --doHighDphijj '
if args.doMTFit:
    extraCommand+=' --doMTFit '
if args.rmDPhiMETPh:
    extraCommand+=' --rmDPhiMETPh '    
if args.doLooseCR:
    extraCommand+=' --doLooseCR '
if args.doCentralCR:
    extraCommand+=' --doCentralCR '    
if args.doLooseWCR:
    extraCommand+=' --doLooseWCR '
if args.doOneHighFJVTCR:
    extraCommand+=' --doOneHighFJVTCR '
if args.doPlot:
    extraCommand+=' --doPlot '
extraCommand+=' --Binning '+args.Binning


for syst in systlist:
    MCFileListToUse = listoffilesMC
    isLow = ""    
    if "__1down" in syst or "Down" in syst:
        isLow = " --isLow"
    if syst in wsys_systlist:
        isLow+=' --weightSyst'
    if syst in sys.getsystematicsOneSidedMap().keys():
        print 'Skipping one sided systematic: ',syst
        continue
    if syst in sys.systematicsVBFSignal:
        MCFileListToUse=listoffilesVBFMC
    if syst in sys.systematicsGGFSignal:
        MCFileListToUse=listoffilesGGFMC
    if syst in sys.systematicsSignalPDF:
        MCFileListToUse=listoffilesGGFVBFMC
    if syst in sys.systematicsZewkTheory:
        MCFileListToUse=listoffilesZewkMC
    if syst in sys.systematicsZstrongTheory:
        MCFileListToUse=listoffilesZstrongMC
    if syst in sys.systematicsWstrongTheory:
        MCFileListToUse=listoffilesWstrongMC
    if syst in sys.systematicsWewkTheory:
        MCFileListToUse=listoffilesWewkMC
    runCommand = '''athena VBFAnalysis/HFInputJobOptions.py --filesInput "$1" - --currentVariation '''+syst+isLow+extraCommand
    print runCommand
    if not args.noSubmit:
        writeCondorShell(workDir, buildDir, runCommand, syst, "HFInputCondorSub", slc7=args.slc7,CMTCONFIG=CMTCONFIG)
        writeCondorSub(workDir, syst, "HFInputCondorSub", listoffiles, MCFileListToUse)


# The low one sided systematics can be handled in the fitting. just call symmeterize in hist fitter
#for syst in asys_systlist:
#    runCommand = '''athena VBFAnalysis/HFInputJobOptions.py --filesInput "$1" - --currentVariation '''+syst+" --doLowNom"+extraCommand
#    print runCommand
#    writeCondorShell(workDir, buildDir, runCommand, syst, "HFInputCondorSub")
#    writeCondorSub(workDir, syst, "HFInputCondorSub", listoffiles, listoffilesMC)


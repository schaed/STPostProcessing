#---- Import job config for customized command line inputs ----
from VBFAnalysis.job_configuration import JobConfigurationBase
from glob import glob
import VBFAnalysis.sample
#---- Options you could specify on command line -----
jps.AthenaCommonFlags.EvtMax =vars().get("nEvents", -1)                          #set on command-line with: --evtMax=-1
#jps.AthenaCommonFlags.SkipEvents=0                       #set on command-line with: --skipEvents=0
jps.AthenaCommonFlags.FilesInput =[vars().get("input", "/eos/user/r/rzou/v04/merged/Z_EWKNominal308092_000001.root")]
jps.AthenaCommonFlags.TreeName = "MiniNtuple"

config = JobConfigurationBase("JobOptions")
arg_group = config.parser.add_argument_group("JobOptions", "Extra arguments specific to HFInputJobOptions")
arg_group.add_argument("--currentVariation", dest='currentVariation', default="Nominal", help="current systematics, default: NONE")
arg_group.add_argument("--containerName", dest='containerName', default="", help="container name used to look up the sample ID if not in the file path")
arg_group.add_argument("--currentSample", dest='currentSample', default="", help="sample name to process")
arg_group.add_argument("--doLowNom", action="store_true", dest='doLowNom', default=False, help="doLowNom, to symmetrize asymmetric syst, default: False")
arg_group.add_argument("--isOneCRBin", action="store_true", dest='isOneCRBin', default=False, help="isOneCRBin, set to one cr bin, default: False")
arg_group.add_argument("--extraVars", dest='extraVars', default='7', help="extraVars, cut on the new variables for leptons veto etc, default: 0, 1=lepton vars, 2= includes kinematics, 3=no met soft cut, 4=no xe SF for muons, 5=lepTrigOnly for muCR, 6=met trig only for muCR, 7=metORLep for muCR (default)")
arg_group.add_argument("--Binning", dest='Binning', default='11', help="Binning, set binning of analysis, rel 20p7: 0, default 11 bins: 11")
arg_group.add_argument("--doOneHighFJVTCR",  action="store_true", dest='doOneHighFJVTCR', default=False, help="do one fjvt cr for high dphijj")
arg_group.add_argument("--METDef", dest='METDef', default='0', help="met definition, default: 0=loose, 1=tenacious")
arg_group.add_argument("--METCut", dest='METCut', default='-1', help="met cut if set")
arg_group.add_argument("--isMadgraph", action="store_true", dest='isMadgraph', default=False, help="isMadgraph, default: False")
arg_group.add_argument("--mergeKTPTV", action="store_true", dest='mergeKTPTV', default=False, help="mergeKTPTV, default: False")
arg_group.add_argument("--doDoubleRatio", action="store_true", dest='doDoubleRatio', default=False, help="doDoubleRatio, default: False")
arg_group.add_argument("--doTMVA", action="store_true", dest='doTMVA', default=False, help="doTMVA, default: False")
arg_group.add_argument("--year", type=int, dest='year', default=2016, help="year, default: 2016 - 2017 or 2018 for those years")
arg_group.add_argument("--isLow", action="store_true", dest='isLow', default=False, help="isLow, default: False")
arg_group.add_argument("--weightSyst", action="store_true", dest='weightSyst', default=False, help="is a weight systematic, default: False")
arg_group.add_argument("--v26Ntuples", action="store_true", dest='v26Ntuples', default=False, help="run v26 style ntuples, default: False")
arg_group.add_argument("--noVjMjjWeight", action="store_true", dest='noVjMjjWeight', default=False, help="remove the mjj reweighting if requested, default: False")
arg_group.add_argument("--isv41older", action="store_true", dest='isv41older', default=False, help="run v41 or older style ntuples, default: False")
arg_group.add_argument("--doVBFMETGam", action="store_true", dest='doVBFMETGam', default=False, help="run VBF+MET+gamma analysis, default: False")
arg_group.add_argument("--doMTFit", action="store_true", dest='doMTFit', default=False, help="run VBF+MET+gamma with an MT Fit analysis, default: False")
arg_group.add_argument("--doLooseCR", action="store_true", dest='doLooseCR', default=False, help="run VBF+MET+gamma with a loose CR analysis, default: False")
arg_group.add_argument("--doCentralCR", action="store_true", dest='doCentralCR', default=False, help="run VBF+MET+gamma with a central photon CR analysis, default: False")
arg_group.add_argument("--doLooseWCR", action="store_true", dest='doLooseWCR', default=False, help="run VBF+MET+gamma with a loose WCR analysis, default: False")
arg_group.add_argument("--rmDPhiMETPh", action="store_true", dest='rmDPhiMETPh', default=False, help="run VBF+MET+gamma remvove dphi(met,ph) cut, default: False")
arg_group.add_argument("--doHighDphijj", action="store_true", dest='doHighDphijj', default=False, help="run dphijj>2.5 Fit analysis, drops the dphijj binning, default: False")
arg_group.add_argument("--singleHist", action="store_true", dest='singleHist', default=False, help="run VBF+MET into a single histogram, default: True")
arg_group.add_argument("--oldInput", action="store_true", dest='oldInput', default=False, help="if oldInput, switch to HFInputOldInput")
arg_group.add_argument("--doPlot", action="store_true", dest='doPlot', default=False, help="doPlot, to turn on additional histograms used for postfit plots, default: False")
# parse the commandline options
args = config.parse_args()

doLowNom_str = ""
if (args.doLowNom):
    doLowNom_str = "Low"
inputDir = str(jps.AthenaCommonFlags.FilesInput)
s = VBFAnalysis.sample.sample("", args.currentVariation)
currentSampleKey=''
currentSampleList=[]
currentSample=''
if args.currentSample!="":
    currentSampleList+=[args.currentSample]
subfileN=''
if len(currentSampleList)==0:
    #for sampl,slist in s.sampleMap.iteritems():
    for sampl in s.sampleTypeList:
        if inputDir.count(sampl):
            currentSampleKey=sampl
            currentSampleList=[sampl]
            currentSample=sampl
            break;
#s = VBFAnalysis.sample.sample(inputDir, args.currentVariation)
#currentSample = s.getsampleType()
#print inputDir
#runNumberS = s.getrunNumberS().rstrip('.root')
#subfileN = s.getsubfileN()
runNumberS=''
containerName = args.containerName
if containerName!="":
    s=VBFAnalysis.sample.sample(containerName)
    currentSample = s.getsampleType()
    isMC = s.getisMC()
    runNumber = s.getrunNumber()
    subfileN = s.getsubfileN()

#for currentSample in currentSampleList:
if True:
    print 'currentSample: ',currentSample
    jps.AthenaCommonFlags.AccessMode = "TreeAccess"              #Choose from TreeAccess,BranchAccess,ClassAccess,AthenaAccess,POOLAccess
    jps.AthenaCommonFlags.TreeName = currentSample+args.currentVariation   #form:"Z_strongNominal"                    #when using TreeAccess, must specify the input tree name 
    if args.weightSyst:
        jps.AthenaCommonFlags.TreeName = currentSample+"Nominal"   #form:"Z_strongNominal"                    #when using TreeAccess, must specify the input tree name 
    print currentSample+args.currentVariation
    jps.AthenaCommonFlags.HistOutputs = ["MYSTREAM:HF"+currentSample+args.currentVariation+doLowNom_str+runNumberS+"_"+str(subfileN)+".root"]  #register output files like this. MYSTREAM is used in the code
    
    if currentSample == "data":
        isMC = False
    else:
        isMC = True
    print 'isMC: ',isMC
    if not(args.oldInput):
        athAlgSeq += CfgMgr.HFInputAlg("HFInputAlg",
                                       currentVariation = args.currentVariation,
                                       currentSample = currentSample,
                                       isMC = isMC,
                                       ExtraVars=int(args.extraVars),
                                       Binning=int(args.Binning),
                                       doOneHighFJVTCR=args.doOneHighFJVTCR,
                                       METDef=int(args.METDef),
                                       METCut=int(args.METCut),
                                       doLowNom = args.doLowNom,
                                       isHigh = not args.isLow,
                                       isMadgraph = args.isMadgraph,
                                       isOneCRBin = args.isOneCRBin,
                                       mergeKTPTV = args.mergeKTPTV,
                                       doTMVA = args.doTMVA,
                                       doDoubleRatio = args.doDoubleRatio,
                                       year = args.year,
                                       weightSyst = args.weightSyst,
                                       doPlot = args.doPlot,
                                       v26Ntuples = args.v26Ntuples,
                                       noVjMjjWeight = args.noVjMjjWeight,
                                       isv41older = args.isv41older,
                                       singleHist = args.singleHist,
                                       doVBFMETGam = args.doVBFMETGam,
                                       doMTFit = args.doMTFit,
                                       doLooseCR = args.doLooseCR,
                                       doCentralCR = args.doCentralCR,
                                       doLooseWCR = args.doLooseWCR,
                                       rmDPhiMETPh = args.rmDPhiMETPh,
                                       doHighDphijj = args.doHighDphijj);
    else:
        if args.currentSample == "physics_micro":
            isMC = False
        athAlgSeq += CfgMgr.HFInputOldInputAlg("HFInputOldInputAlg",
                                               currentVariation = args.currentVariation,
                                               currentSample = currentSample,
                                               isMC = isMC,
                                               ExtraVars=int(args.extraVars),
                                               Binning=int(args.Binning),
                                               doOneHighFJVTCR=args.doOneHighFJVTCR,
                                               METDef=int(args.METDef),
                                               METCut=int(args.METCut),
                                               doLowNom = args.doLowNom,
                                               isHigh = not args.isLow,
                                               isMadgraph = args.isMadgraph,
                                               isOneCRBin = args.isOneCRBin,
                                               mergeKTPTV = args.mergeKTPTV,
                                               doTMVA = args.doTMVA,
                                               doDoubleRatio = args.doDoubleRatio,
                                               year = args.year,
                                               weightSyst = args.weightSyst,
                                               doPlot = args.doPlot,
                                               singleHist = args.singleHist,
                                               v26Ntuples = args.v26Ntuples,
                                               noVjMjjWeight = args.noVjMjjWeight,
                                               isv41older = args.isv41older,
                                               doVBFMETGam = args.doVBFMETGam,
                                               doMTFit = args.doMTFit,
                                               doLooseCR = args.doLooseCR,
                                               doCentralCR = args.doCentralCR,
                                               doLooseWCR = args.doLooseWCR,
                                               rmDPhiMETPh = args.rmDPhiMETPh,
                                               doHighDphijj = args.doHighDphijj);
    
    include("AthAnalysisBaseComps/SuppressLogging.py")              #Optional include to suppress as much athena output as possible. Keep at bottom of joboptions so that it doesn't suppress the logging of the things you have configured above


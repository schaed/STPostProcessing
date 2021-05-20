import os,sys,subprocess,datetime,copy,math,array,shutil,ROOT,re,string
from ROOT import gROOT
from subprocess import call
from array import array

__author__ = "John Anders"
__doc__    = """Script to add Sherpa Systematic Weight branches to existing file."""
def generateZpTMapping(dictionary):

    #Sherpa 2.1
    # 0-70, bin 1, 70-140 bin 2 etc.
    print "Adding Z--> nunu to the dictionary"
    print "Range 0-70"
    for i in range(361444, 361447):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(361447, 361450):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(361450, 361453):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(361453, 361456):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(361456, 361459):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(361459, 361462):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(361462, 361465):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(361465, 361468):
        dictionary[i] = 8
        print i



    print "Adding Z--> ee to the dictionary"
    print "Range 0-70"
    for i in range(361372, 361375):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(361375, 361378):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(361378, 361381):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(361381, 361384):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(361384, 361387):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(361387, 361390):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(361390, 361393):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(361393, 361396):
        dictionary[i] = 8
        print i



    print "Adding Z--> mumu to the dictionary"
    print "Range 0-70"
    for i in range(361396, 361399):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(361399, 361402):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(361402, 361405):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(361405, 361408):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(361408, 361411):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(361411, 361414):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(361414, 361417):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(361417, 361420):
        dictionary[i] = 8
        print i


    print "Adding Z--> tautau to the dictionary"
    print "Range 0-70"
    for i in range(361420, 361423):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(361423, 361426):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(361426, 361429):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(361429, 361432):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(361432, 361435):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(361435, 361438):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(361438, 361441):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(361441, 361444):
        dictionary[i] = 8
        print i


    print "Adding W+Jets MCIDs"
    print "Adding W--> enu to the dictionary"
    print "Range 0-70"
    for i in range(361300, 361303):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(361303, 361306):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(361306, 361309):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(361309, 361312):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(361312, 361315):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(361315, 361318):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(361318, 361321):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(361321, 361324):
        dictionary[i] = 8
        print i


    print "Adding W--> munu to the dictionary"
    print "Range 0-70"
    for i in range(361324, 361327):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(361327, 361330):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(361330, 361333):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(361333, 361336):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(361336, 361339):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(361339, 361342):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(361342, 361345):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(361345, 361348):
        dictionary[i] = 8
        print i


    print "Adding W--> taunu to the dictionary"
    print "Range 0-70"
    for i in range(361348, 361351):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(361351, 361354):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(361354, 361357):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(361357, 361360):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(361360, 361363):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(361363, 361366):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(361366, 361369):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(361369, 361372):
        dictionary[i] = 8
        print i


    print "Adding the Sherpa 2.2 nominal to the dictionary"

    # 0-70, bin 1, 70-140 bin 2 etc.
    print "Adding Z--> nunu to the dictionary"
    print "Range 0-70"
    for i in range(363412, 363415):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(363415, 363418):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(363418, 363421):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(363421, 363424):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(363424, 363427):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(363427, 363430):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(363430, 363433):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(363433, 363436):
        dictionary[i] = 8
        print i



    print "Adding Z--> ee to the dictionary"
    print "Range 0-70"
    for i in range(363388, 363391):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(363391, 363394):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(363394, 363397):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(363397, 363400):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(363400, 363403):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(363403, 363406):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(363406, 363409):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(363409, 363412):
        dictionary[i] = 8
        print i



    print "Adding Z--> mumu to the dictionary"
    print "Range 0-70"
    for i in range(363364, 363367):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(363367, 363370):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(363370, 363373):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(363373, 363376):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(363376, 363379):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(363379, 363382):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(363382, 363385):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(363385, 363388):
        dictionary[i] = 8
        print i


    print "Adding Z--> tautau to the dictionary"
    print "Range 0-70"
    for i in range(363099, 363102):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(363102, 363105):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(363105, 363108):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(363108, 363111):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(363111, 363114):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(363114, 363117):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(363117, 363120):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(363120, 363123):
        dictionary[i] = 8
        print i




    print "Adding W+Jets MCIDs for Sherpa 2.2"
    print "Adding W--> enu to the dictionary"
    print "Range 0-70"
    for i in range(363460, 363463):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(363463, 363466):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(363466, 363469):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(363469, 363472):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(363472, 363475):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(363475, 363478):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(363478, 363481):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(363481, 363484):
        dictionary[i] = 8
        print i


    print "Adding W--> munu to the dictionary"
    print "Range 0-70"
    for i in range(363436, 363439):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(363439, 363442):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(363442, 363445):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(363445, 363448):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(363448, 363451):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(363451, 363454):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(363454, 363457):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(363447, 363460):
        dictionary[i] = 8
        print i


    print "Adding W--> taunu to the dictionary"
    print "Range 0-70"
    for i in range(363331, 363334):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(363334, 363337):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(363337, 363340):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(363340, 363343):
        dictionary[i] = 4
        print i

    print "Range 500-700"
    for i in range(363343, 363346):
        dictionary[i] = 5
        print i

    print "Range 700-1000"
    for i in range(363346, 363349):
        dictionary[i] = 6
        print i

    print "Range 1000-2000"
    for i in range(363349, 363352):
        dictionary[i] = 7
        print i

    print "Range 2000-ECMS"
    for i in range(363352, 363355):
        dictionary[i] = 8
        print i


    # These are the relevant mappings for 2.2.1
    # 0-70, bin 1, 70-140 bin 2 etc.
    print "Adding Sherpa 2.2.1 samples."
    print "Adding Z--> mumu to the dictionary"
    print "Range 0-70"
    for i in range(364100, 364103):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(364103, 364106):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(364106, 364109):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(364109, 364112):
        dictionary[i] = 4
        print i

    print "Range 500-1000"
    dictionary[364112] = 56
    dictionary[364216] = 56
    print i

    print "Range 1000-ECMS"
    dictionary[364113] = 7
    dictionary[364217] = 7
    print i




    # 0-70, bin 1, 70-140 bin 2 etc.
    print "Adding Z--> ee to the dictionary"
    print "Range 0-70"
    for i in range(364114, 364117):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(364117, 364120):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(364120, 364123):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(364123, 364126):
        dictionary[i] = 4
        print i

    print "Range 500-1000"
    dictionary[364126] = 56
    dictionary[364218] = 56
    print i

    print "Range 1000-ECMS"
    dictionary[364127] = 7
    dictionary[364219] = 7
    print i



    # 0-70, bin 1, 70-140 bin 2 etc.
    print "Adding Z--> tautau to the dictionary"
    print "Range 0-70"
    for i in range(364128, 364131):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(364131, 364134):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(364134, 364137):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(364137, 364140):
        dictionary[i] = 4
        print i

    print "Range 500-1000"
    dictionary[364140] = 56
    dictionary[364220] = 56
    print i

    print "Range 1000-ECMS"
    dictionary[364141] = 7
    dictionary[364221] = 7
    print i

    # 0-70, bin 1, 70-140 bin 2 etc.
    print "Adding Z--> nunu to the dictionary"
    print "Range 0-70"
    for i in range(364142, 364145):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(364145, 364148):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(364148, 364151):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(364151, 364154):
        dictionary[i] = 4
        print i

    print "Range 500-1000"
    dictionary[364154] = 56
    print i

    print "Range 1000-ECMS"
    dictionary[364155] = 7
    print i

    #NEW ZNUNU
    print "Adding Z--> nunu (NEW SAMPLES) to the dictionary"

    print "Range 70-100"
    for i in [366010,366019,366028]:
        dictionary[i] = 2
        print i

    print "Range 100-140"
    for i in [366011,366012,366013,366020,366021,366022,366029,366030,366031]:
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in [366014,366015,366016,366023,366024,366025,366032,366033,366034]:
        dictionary[i] = 3
        print i

    print "Range 280-500"
    for i in [366017,366026,366035]:
        dictionary[i] = 4
        print i

    print "Range 500-1000"
    for i in [364222]:
        dictionary[i] = 56
        print i

    print "Range 1000-ECMS"
    for i in [364223]:
        dictionary[i] = 7
        print i

    # Add the W here.
    print "Adding W--> munu to the dictionary"
    print "Range 0-70"
    for i in range(364156, 364159):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(364159, 364162):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(364162, 364165):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(364165, 364168):
        dictionary[i] = 4
        print i

    print "Range 500-1000"
    dictionary[364168] = 56
    dictionary[364224] = 56
    print i

    print "Range 1000-ECMS"
    dictionary[364169] = 7
    dictionary[364225] = 7
    print i




    # 0-70, bin 1, 70-140 bin 2 etc.
    print "Adding W--> enu to the dictionary"
    print "Range 0-70"
    for i in range(364170, 364173):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(364173, 364176):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(364176, 364179):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(364179, 364182):
        dictionary[i] = 4
        print i

    print "Range 500-1000"
    dictionary[364182] = 56
    dictionary[364226] = 56
    print i

    print "Range 1000-ECMS"
    dictionary[364183] = 7
    dictionary[364227] = 7
    print i



    # 0-70, bin 1, 70-140 bin 2 etc.
    print "Adding W--> taunu to the dictionary"
    print "Range 0-70"
    for i in range(364184, 364187):
        dictionary[i] = 1
        print i

    print "Range 70-140"
    for i in range(364187, 364190):
        dictionary[i] = 2
        print i

    print "Range 140-280"
    for i in range(364190, 364193):
        dictionary[i] = 3
        print i


    print "Range 280-500"
    for i in range(364193, 364196):
        dictionary[i] = 4
        print i

    print "Range 500-1000"
    dictionary[364196] = 56
    dictionary[364228] = 56
    print i

    print "Range 1000-ECMS"
    dictionary[364197] = 7
    dictionary[364229] = 7
    print i







    return dictionary


def main(argv):

    # infile should be the VJets file to add the weights to.
    script, infile, treeName = argv

    print "Creating MCID, ZpT mapping"
    ZpTMapping = dict()
    generateZpTMapping(ZpTMapping)

    print "Loading histograms with weights"
    ZeeHistograms = []
    ZnunuHistograms = []
    WenuHistograms = []

    # Variation file:
    fileWithWeights = "/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/SUSYTools/Vjets_SysParameterization/VJetsWeights.root"
    g = ROOT.TFile(fileWithWeights)
    systList = ["ckkw15", "ckkw30", "fac025", "fac4", "renorm025", "renorm4", "qsf025", "qsf4"]

    for syst in systList:
        #print "Zee_"+syst
        h = ROOT.TH2F(g.Get("Zee"+syst))
        ZeeHistograms.append(h)
        h = ROOT.TH2F(g.Get("Znunu"+syst))
        ZnunuHistograms.append(h)
        h = ROOT.TH2F(g.Get("Wenu"+syst))
        WenuHistograms.append(h)

    print "Loading File"
    f = ROOT.TFile(infile,"update")

    print "Loading Tree"

    # empty arrays for adding branches
    ckkw15 = array('f', [0.])
    ckkw30 = array('f', [0.])
    fac025 = array('f', [0.])
    fac4 = array('f', [0.])
    renorm025 = array('f', [0.])
    renorm4 = array('f', [0.])
    qsf025 = array('f', [0.])
    qsf4 = array('f', [0.])

    # Add branches
    T = f.Get(treeName)
    ckkw15branch = T.Branch("ckkw15_Weight", ckkw15,"ckkw15_Weight/F")
    ckkw30branch = T.Branch("ckkw30_Weight", ckkw30,"ckkw30_Weight/F")
    fac025branch = T.Branch("fac025_Weight", fac025,"fac025_Weight/F")
    fac4branch = T.Branch("fac4_Weight", fac4,"fac4_Weight/F")
    renorm025branch = T.Branch("renorm025_Weight", renorm025,"renorm025_Weight/F")
    renorm4branch = T.Branch("renorm4_Weight", renorm4,"renorm4_Weight/F")
    qsf025branch = T.Branch("qsf025_Weight", qsf025,"qsf025_Weight/F")
    qsf4branch = T.Branch("qsf4_Weight", qsf4,"qsf4_Weight/F")

    print "Adding Weights"
    nEvts = T.GetEntries()
    for iEvt in range(nEvts):

        if iEvt%1000 == 0:
            print "Current Event being Processed is: ", iEvt

        T.GetEntry(iEvt)

        MCID = T.runNumber
        nTruthJets = T.n_jet_truth

        decayType = "none"

        # Find the Decay type
        if ((MCID >= 361372 and MCID <= 361443) or (MCID >= 363102 and MCID <= 363122) or (MCID >= 363361 and MCID <= 363363) or (MCID >= 363364 and MCID <= 363411) or (MCID >= 364100 and MCID <= 364141) or (MCID >= 364218 and MCID <=364219) or (MCID >= 364216 and MCID <=364217) or (MCID >= 364220 and MCID <=364221)   ):
            decayType = "Zee"
            #        if ((MCID >= 361444 and MCID <= 361467) or (MCID >= 363412 and MCID <= 363435) or (MCID >= 364142 and MCID <= 364155)  ): #OLD ZNUNU SAMPLES
        if ((MCID >= 361444 and MCID <= 361467) or (MCID >= 366010 and MCID <= 366035) or (MCID>=364222 and MCID<=364223) ): #NEW ZNUNU SAMPLES
            decayType = "Znunu"
            if iEvt%1000 == 0:
                print "Decay type identified as Znunu: ", MCID
        if ((MCID >= 361300 and MCID <= 361371) or (MCID >= 363331 and MCID <= 363354) or (MCID >= 363436 and MCID <= 363483) or (MCID >= 364156 and MCID <= 364197) or (MCID >= 364226 and MCID <= 364227) or (MCID >= 364224 and MCID <= 364225)  or (MCID >= 364228 and MCID <= 364229) ):
            decayType = "Wenu"




            # find which ZpT bin we want
        ZpTBin = ZpTMapping.get(MCID)
        TruthJetBin = nTruthJets+1
        if nTruthJets >= 11:
            TruthJetBin = 12
        if iEvt%1000 == 0:
            print "ZpTBin: ", ZpTBin
            print "TruthJEtBin: ", TruthJetBin
        if ZpTBin == None:
            print "NOT IN MAPPING: ", MCID
            print "ZpTBin: ", ZpTBin
            print "TruthJEtBin: ", TruthJetBin
                #this MCID isn't in the mapping, so skip and default to 1
            ckkw15[0] = 1
            ckkw30[0] = 1
            fac025[0] = 1
            fac4[0] = 1
            renorm025[0] = 1
            renorm4[0] = 1
            qsf025[0] = 1
            qsf4[0] = 1

        else:
            if (ZpTBin<10): #Due to difference in filtering between samples we use and CKKW reweighting samples, some samples are reweighted with a mix of 2 CKKW reweighting samples. These are indicated by being >1 digits long, with each digit being a different reweighting sample
                if decayType == "Zee":
                    ckkw15[0] = ZeeHistograms[0].GetBinContent(ZpTBin,TruthJetBin)
                    ckkw30[0] =  ZeeHistograms[1].GetBinContent(ZpTBin,TruthJetBin)
                    fac025[0] =  ZeeHistograms[2].GetBinContent(ZpTBin,TruthJetBin)
                    fac4[0] =  ZeeHistograms[3].GetBinContent(ZpTBin,TruthJetBin)
                    renorm025[0] =  ZeeHistograms[4].GetBinContent(ZpTBin,TruthJetBin)
                    renorm4[0] =  ZeeHistograms[5].GetBinContent(ZpTBin,TruthJetBin)
                    qsf025[0] =  ZeeHistograms[6].GetBinContent(ZpTBin,TruthJetBin)
                    qsf4[0] =  ZeeHistograms[7].GetBinContent(ZpTBin,TruthJetBin)
                elif decayType == "Znunu":
                    ckkw15[0] = ZnunuHistograms[0].GetBinContent(ZpTBin,TruthJetBin)
                    ckkw30[0] =  ZnunuHistograms[1].GetBinContent(ZpTBin,TruthJetBin)
                    fac025[0] =  ZnunuHistograms[2].GetBinContent(ZpTBin,TruthJetBin)
                    fac4[0] =  ZnunuHistograms[3].GetBinContent(ZpTBin,TruthJetBin)
                    renorm025[0] =  ZnunuHistograms[4].GetBinContent(ZpTBin,TruthJetBin)
                    renorm4[0] =  ZnunuHistograms[5].GetBinContent(ZpTBin,TruthJetBin)
                    qsf025[0] =  ZnunuHistograms[6].GetBinContent(ZpTBin,TruthJetBin)
                    qsf4[0] =  ZnunuHistograms[7].GetBinContent(ZpTBin,TruthJetBin)
                elif decayType == "Wenu":
                    ckkw15[0] = WenuHistograms[0].GetBinContent(ZpTBin,TruthJetBin)
                    ckkw30[0] =  WenuHistograms[1].GetBinContent(ZpTBin,TruthJetBin)
                    fac025[0] =  WenuHistograms[2].GetBinContent(ZpTBin,TruthJetBin)
                    fac4[0] =  WenuHistograms[3].GetBinContent(ZpTBin,TruthJetBin)
                    renorm025[0] =  WenuHistograms[4].GetBinContent(ZpTBin,TruthJetBin)
                    renorm4[0] =  WenuHistograms[5].GetBinContent(ZpTBin,TruthJetBin)
                    qsf025[0] =  WenuHistograms[6].GetBinContent(ZpTBin,TruthJetBin)
                    qsf4[0] =  WenuHistograms[7].GetBinContent(ZpTBin,TruthJetBin)
                else:
                    exit(0)
                if iEvt%1000 == 0:
                    print "ckkw15: ", ckkw15[0]
                    print "ckkw30: ", ckkw30[0]
            else:
                ZpTBinString = str(ZpTBin)
                ZpTBin1 = int(ZpTBinString[0])
                ZpTBin2 = int(ZpTBinString[1])
                if decayType == "Zee":
                    ckkw15[0]    = (ZeeHistograms[0].GetBinContent(ZpTBin1,TruthJetBin)+ZeeHistograms[0].GetBinContent(ZpTBin2,TruthJetBin))/2
                    ckkw30[0]    = (ZeeHistograms[1].GetBinContent(ZpTBin1,TruthJetBin)+ZeeHistograms[1].GetBinContent(ZpTBin2,TruthJetBin))/2
                    fac025[0]    = (ZeeHistograms[2].GetBinContent(ZpTBin1,TruthJetBin)+ZeeHistograms[2].GetBinContent(ZpTBin2,TruthJetBin))/2
                    fac4[0]      = (ZeeHistograms[3].GetBinContent(ZpTBin1,TruthJetBin)+ZeeHistograms[3].GetBinContent(ZpTBin2,TruthJetBin))/2
                    renorm025[0] = (ZeeHistograms[4].GetBinContent(ZpTBin1,TruthJetBin)+ZeeHistograms[4].GetBinContent(ZpTBin2,TruthJetBin))/2
                    renorm4[0]   = (ZeeHistograms[5].GetBinContent(ZpTBin1,TruthJetBin)+ZeeHistograms[5].GetBinContent(ZpTBin2,TruthJetBin))/2
                    qsf025[0]    = (ZeeHistograms[6].GetBinContent(ZpTBin1,TruthJetBin)+ZeeHistograms[6].GetBinContent(ZpTBin2,TruthJetBin))/2
                    qsf4[0]      = (ZeeHistograms[7].GetBinContent(ZpTBin1,TruthJetBin)+ZeeHistograms[7].GetBinContent(ZpTBin2,TruthJetBin))/2
                elif decayType == "Znunu":
                    ckkw15[0]    = (ZnunuHistograms[0].GetBinContent(ZpTBin1,TruthJetBin) + ZnunuHistograms[0].GetBinContent(ZpTBin2,TruthJetBin))/2
                    ckkw30[0]    = (ZnunuHistograms[1].GetBinContent(ZpTBin1,TruthJetBin) + ZnunuHistograms[1].GetBinContent(ZpTBin2,TruthJetBin))/2
                    fac025[0]    = (ZnunuHistograms[2].GetBinContent(ZpTBin1,TruthJetBin) + ZnunuHistograms[2].GetBinContent(ZpTBin2,TruthJetBin))/2
                    fac4[0]      = (ZnunuHistograms[3].GetBinContent(ZpTBin1,TruthJetBin) + ZnunuHistograms[3].GetBinContent(ZpTBin2,TruthJetBin))/2
                    renorm025[0] = (ZnunuHistograms[4].GetBinContent(ZpTBin1,TruthJetBin) + ZnunuHistograms[4].GetBinContent(ZpTBin2,TruthJetBin))/2
                    renorm4[0]   = (ZnunuHistograms[5].GetBinContent(ZpTBin1,TruthJetBin) + ZnunuHistograms[5].GetBinContent(ZpTBin2,TruthJetBin))/2
                    qsf025[0]    = (ZnunuHistograms[6].GetBinContent(ZpTBin1,TruthJetBin) + ZnunuHistograms[6].GetBinContent(ZpTBin2,TruthJetBin))/2
                    qsf4[0]      = (ZnunuHistograms[7].GetBinContent(ZpTBin1,TruthJetBin) + ZnunuHistograms[7].GetBinContent(ZpTBin2,TruthJetBin))/2
                elif decayType == "Wenu":
                    ckkw15[0]    = (WenuHistograms[0].GetBinContent(ZpTBin1,TruthJetBin) + WenuHistograms[0].GetBinContent(ZpTBin2,TruthJetBin))/2
                    ckkw30[0]    = (WenuHistograms[1].GetBinContent(ZpTBin1,TruthJetBin) + WenuHistograms[1].GetBinContent(ZpTBin2,TruthJetBin))/2
                    fac025[0]    = (WenuHistograms[2].GetBinContent(ZpTBin1,TruthJetBin) + WenuHistograms[2].GetBinContent(ZpTBin2,TruthJetBin))/2
                    fac4[0]      = (WenuHistograms[3].GetBinContent(ZpTBin1,TruthJetBin) + WenuHistograms[3].GetBinContent(ZpTBin2,TruthJetBin))/2
                    renorm025[0] = (WenuHistograms[4].GetBinContent(ZpTBin1,TruthJetBin) + WenuHistograms[4].GetBinContent(ZpTBin2,TruthJetBin))/2
                    renorm4[0]   = (WenuHistograms[5].GetBinContent(ZpTBin1,TruthJetBin) + WenuHistograms[5].GetBinContent(ZpTBin2,TruthJetBin))/2
                    qsf025[0]    = (WenuHistograms[6].GetBinContent(ZpTBin1,TruthJetBin) + WenuHistograms[6].GetBinContent(ZpTBin2,TruthJetBin))/2
                    qsf4[0]      = (WenuHistograms[7].GetBinContent(ZpTBin1,TruthJetBin) + WenuHistograms[7].GetBinContent(ZpTBin2,TruthJetBin))/2
                else:
                    exit(0)
                if iEvt%1000 == 0:
                    print "This is a double digit ZpTbinString: ", ZpTBinString
                    print "Averaging Bins: ", ZpTBin1, ",", ZpTBin2
                    print "ckkw15: ", ckkw15[0]
                    print "ckkw30: ", ckkw30[0]




        ckkw15branch.Fill()
        ckkw30branch.Fill()
        fac025branch.Fill()
        fac4branch.Fill()
        renorm025branch.Fill()
        renorm4branch.Fill()
        qsf025branch.Fill()
        qsf4branch.Fill()



    T.Write()

    print "Done."

if __name__ == '__main__':
    main(sys.argv)